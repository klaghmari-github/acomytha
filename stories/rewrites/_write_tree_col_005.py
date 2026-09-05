#!/usr/bin/env python3
"""TREE-COL-005 — La gouttière et les trois mots d'Aniss (F-NAR-019, N2, TTS)."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, words  # noqa: E402

SID = "TREE-COL-005"
N2 = LIMITS["N2"]
TITLE = "La gouttière et les trois mots d'Aniss"
FIL = (
    "Sous la pluie, Aniss veut un pain au stand de zinc avant qu'on range l'étal. "
    "Il crie trop tôt : la gouttière couvre sa voix, on n'entend que « stand ». "
    "Cuisine (vapeur), jardin (anse glissante) ou chambre (manche à l'envers) "
    "changent l'obstacle. Voisin, maîtresse ou boulangère changent l'écoute. "
    "Pain, pomme ou livre changent ce qu'il demande. Bonjour, s'il te plaît, "
    "merci au moment du besoin, jamais récités. La gouttière paie la fin."
)
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="gouttière",
        note="arc=installation; intention=émerveiller; emotion=envie_impatiente; intensite=1; destinataire=enfant; sous_texte=le stand va partir sans lui; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_voix_a_trouvé_un_creux; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="panier",
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il_veut_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_retenue; intensite=2; destinataire=enfant; sous_texte=demander_ouvre_la_main_de_l_autre; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=la_demande_a_changé_le_geste; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="zinc",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_gouttière_a_rendu_le_silence; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def L(*rows: str) -> list[str]:
    out: list[str] = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
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
    nc["pause_before_ms"] = 0
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
    "narrateur|Sous la pluie, la maison a un toit de zinc.",
    "narrateur|La gouttière fait tic, tic, tic, contre le métal.",
    "narrateur|Des rivières de pluie restent sur la vitre.",
    "narrateur|Dedans, le verre est tiède.",
    "narrateur|Dehors, l'air sent l'herbe mouillée.",
    "narrateur|Les chaussures de papa sèchent près de la porte.",
    "narrateur|Une chaussette rouge pend sur le rebord.",
    "narrateur|Dans la cuisine, la soupe sent la carotte et le thym.",
    "narrateur|Un oiseau gris secoue ses plumes sur la haie.",
    "narrateur|Au coin de la rue, un stand fume sous le zinc.",
    "enfant-m|Je veux un pain, là-bas, tout de suite.",
    "narrateur|En ce moment, Aniss trace une rivière sur la vitre.",
    "narrateur|Son doigt fait un chemin clair vers le stand.",
    "enfant-m|Papa, le stand, un pain !",
    "narrateur|La gouttière couvre sa voix, tic, tic.",
    "narrateur|Papa parle à maman de la soupe.",
    "narrateur|Leurs mots se mélangent aux gouttes.",
    "papa|Tu disais stand, Aniss ?",
    "enfant-m|Un pain, avant qu'ils rangent !",
    "narrateur|Dehors, une main plie une nappe mouillée.",
    "enfant-m|Ils n'ont pas entendu le pain.",
    "maman|On t'écoute, si tu attends un tic.",
    "narrateur|Aniss serre les poings, puis les ouvre.",
)

T1Q = L(
    "narrateur|Aniss peut recommencer, près de la gouttière.",
    "papa|La cuisine, le jardin, ou la chambre ?",
    "maman|D'où vas-tu parler, cette fois ?",
)

T1 = {
    1: L(
        "narrateur|Aniss pousse la porte de la cuisine.",
        "narrateur|La soupe fume, épaisse comme un nuage.",
        "narrateur|Une miette dorée attend près de l'assiette.",
        "narrateur|Le panier d'osier dort contre le four.",
        "enfant-m|Le panier, vite !",
        "narrateur|Sa voix se perd dans la vapeur.",
        "narrateur|Maman tourne la cuillère, sans se tourner.",
        "narrateur|Aniss ouvre la bouche, puis la referme.",
        "narrateur|Il pose les mains à plat sur la table.",
        "narrateur|La vapeur s'amincit.",
        "maman|Je t'écoute.",
        "enfant-m|Bonjour, maman.",
        "maman|Bonjour, Aniss.",
        "enfant-m|Le panier, s'il te plaît.",
        "narrateur|Maman lui tend l'anse, tiède.",
        "enfant-m|Merci.",
        "papa|Merci, j'ai entendu le bonjour.",
        "narrateur|Une goutte glisse sur la vitre, lente.",
    ),
    2: L(
        "narrateur|Aniss passe dans le jardin mouillé.",
        "narrateur|La gouttière tombe dans un seau, plic.",
        "narrateur|Une feuille collée tremble sur l'eau.",
        "narrateur|Le panier brille, trop mouillé.",
        "enfant-m|Je le prends !",
        "narrateur|Il tire l'anse.",
        "narrateur|L'osier lui échappe, glissant.",
        "narrateur|Papa range un pot, plus loin.",
        "narrateur|Aniss a envie de crier.",
        "narrateur|Il attend que le pot touche la terre.",
        "enfant-m|Bonjour, papa.",
        "papa|Bonjour.",
        "enfant-m|L'anse, s'il te plaît.",
        "papa|La voilà.",
        "enfant-m|Merci.",
        "maman|Tes bottes ont bu la flaque.",
        "papa|Merci d'avoir attendu le pot.",
        "narrateur|Une goutte rebondit sur l'osier.",
    ),
    3: L(
        "narrateur|Aniss entre dans la chambre.",
        "narrateur|Le rideau jaune bouge, un peu.",
        "narrateur|Le manteau attend sur la chaise, près de la vitre.",
        "papa|Ton manteau.",
        "narrateur|Papa le tient trop haut.",
        "enfant-m|Je le mets tout seul.",
        "narrateur|La manche se recroqueville, à l'envers.",
        "enfant-m|Non !",
        "narrateur|Maman plie un pull, près de la fenêtre.",
        "narrateur|Aniss avale son cri.",
        "narrateur|Il attend la fin du pli.",
        "enfant-m|Bonjour, maman.",
        "maman|Bonjour, Aniss.",
        "papa|La manche, tu veux de l'aide ?",
        "enfant-m|Oui.",
        "enfant-m|Merci.",
        "papa|Merci, la manche est droite.",
        "narrateur|Une rivière reste sur la vitre de la chambre.",
    ),
}

Q1 = {
    1: L(
        "narrateur|La vapeur s'est tue, près de la soupe.",
        "maman|Aniss a dit quel mot, en premier ?",
    ),
    2: L(
        "narrateur|L'anse a glissé, dans le jardin.",
        "papa|Aniss a demandé comment, pour la reprendre ?",
    ),
    3: L(
        "narrateur|La manche est droite, sur le manteau.",
        "maman|Aniss a dit quoi, à papa ?",
    ),
}

C1 = {
    1: L(
        "enfant-m|Bonjour !",
        "papa|Oui, bonjour.",
        "narrateur|Le panier est dans ses mains.",
        "narrateur|L'osier pique un peu.",
        "maman|Il sent le thym, ce bois.",
        "enfant-m|On va au stand.",
        "papa|Qui tient l'étal, sous la pluie ?",
    ),
    2: L(
        "enfant-m|S'il te plaît.",
        "maman|Oui, je t'ai entendu.",
        "narrateur|Le panier tient, contre sa poitrine.",
        "narrateur|L'herbe mouillée sent fort.",
        "papa|L'anse ne glisse plus.",
        "enfant-m|On va au stand.",
        "maman|Qui tient l'étal, sous le zinc ?",
    ),
    3: L(
        "enfant-m|Merci.",
        "papa|Oui, merci.",
        "narrateur|Le manteau est sur lui, un peu froid.",
        "narrateur|Les boutons sont ronds, contre le cou.",
        "maman|On sort ?",
        "enfant-m|Vers le stand.",
        "papa|Qui tient l'étal, près de la gouttière ?",
    ),
}

T2Q = {
    1: L(
        "narrateur|Le panier sent le thym, près de la porte.",
        "papa|Le voisin, la maîtresse, ou la boulangère ?",
        "maman|Vers qui vas-tu, maintenant ?",
    ),
    2: L(
        "narrateur|L'anse goutte un peu, dans l'herbe.",
        "maman|Le voisin, la maîtresse, ou la boulangère ?",
        "papa|Qui t'écoutera, sous le zinc ?",
    ),
    3: L(
        "narrateur|Le manteau est boutonné, près du couloir.",
        "papa|Le voisin, la maîtresse, ou la boulangère ?",
        "maman|À qui vas-tu parler, dehors ?",
    ),
}

T2 = {
    (1, 1): L(
        "narrateur|Ils sortent de la cuisine, le panier à la main.",
        "narrateur|Le banc du voisin luit sous la haie.",
        "narrateur|Des pots de thym alignés attendent dans une caisse.",
        "enfant-m|Bonjour !",
        "narrateur|Le voisin a le dos tourné, un pot à bout de bras.",
        "narrateur|Le pot penche.",
        "narrateur|Aniss rentre le mot, trop tard pour les oreilles.",
        "narrateur|Il attend que le pot pose sa terre.",
        "enfant-m|Bonjour.",
        "papa|Il s'est tourné, là.",
        "maman|Le thym pique le nez, tout près.",
        "narrateur|La gouttière tombe dans la caisse, plic.",
        "enfant-m|J'ai quelque chose à demander.",
        "narrateur|Le banc reste mouillé, froid sous les mains.",
    ),
    (1, 2): L(
        "narrateur|Ils quittent la cuisine, le panier contre la hanche.",
        "narrateur|L'auvent de l'école goutte sur les dalles.",
        "narrateur|Une nappe de papier tremble, tachée d'eau.",
        "enfant-m|Bonjour, j'ai… !",
        "maitresse|Un, deux, trois sachets.",
        "narrateur|Les mots d'Aniss se cognent aux nombres.",
        "narrateur|Il ferme la bouche, les joues chaudes.",
        "narrateur|Les sachets s'empilent, puis le silence.",
        "enfant-m|Bonjour.",
        "maitresse|Bonjour, Aniss.",
        "papa|Elle t'a vu, cette fois.",
        "maman|La craie sent un peu, sous l'auvent.",
        "narrateur|Une flaque ronde garde un morceau de ciel.",
        "enfant-m|Je peux demander, maintenant.",
    ),
    (1, 3): L(
        "narrateur|Ils quittent la cuisine, l'odeur du thym aux doigts.",
        "narrateur|Le stand de pain a un petit toit de zinc.",
        "narrateur|Une goutte tombe sur le pavé, ploc.",
        "enfant-m|Un pain !",
        "narrateur|Aniss tend le doigt, trop vite.",
        "narrateur|La boulangère plie un sachet, le dos tourné.",
        "narrateur|Le doigt montre le vide.",
        "narrateur|Aniss rentre le bras, les dents serrées.",
        "narrateur|Il attend que le papier se taise.",
        "enfant-m|Bonjour.",
        "papa|Elle s'est tournée, derrière le zinc.",
        "maman|Ça sent le beurre chaud.",
        "narrateur|L'air du four touche les joues.",
        "enfant-m|Je demande, sans le doigt.",
    ),
    (2, 1): L(
        "narrateur|Ils traversent le jardin, bottes dans l'herbe.",
        "narrateur|Le banc du voisin luit, plein d'eau.",
        "narrateur|La gouttière de la haie fait plic, plic.",
        "enfant-m|Bonjour !",
        "narrateur|Aniss marche dans une flaque.",
        "narrateur|L'eau saute jusqu'aux pots de thym.",
        "narrateur|Le voisin lève la tête, surpris.",
        "narrateur|Aniss recule, les joues serrées.",
        "narrateur|Il attend que l'eau se calme.",
        "enfant-m|Bonjour.",
        "papa|Il t'écoute, sans l'eau.",
        "maman|Les pots sont alignés, sauvés.",
        "narrateur|Une feuille reste collée à la caisse.",
        "enfant-m|Je peux parler, là.",
    ),
    (2, 2): L(
        "narrateur|Ils quittent le jardin par le portail mouillé.",
        "narrateur|L'auvent de l'école goutte, goutte, goutte.",
        "narrateur|La nappe de papier a une tache d'eau.",
        "enfant-m|Bonjour, maîtresse !",
        "narrateur|Sa voix part entre deux gouttes, puis se perd.",
        "maitresse|J'ai presque fini la nappe.",
        "narrateur|Aniss compte les gouttes, un, deux, trois.",
        "narrateur|Un creux arrive, sans plic.",
        "enfant-m|Bonjour.",
        "maitresse|Bonjour, je t'entends.",
        "papa|Le zinc s'est tu, un instant.",
        "maman|La craie blanche repose près d'une pomme.",
        "narrateur|Aniss pose le panier, sans le jeter.",
        "enfant-m|Je demande dans le creux.",
    ),
    (2, 3): L(
        "narrateur|Ils quittent le jardin, l'herbe aux bottes.",
        "narrateur|Le stand de pain fume sous le zinc.",
        "narrateur|Une goutte rebondit sur le pavé.",
        "enfant-m|Je prends !",
        "narrateur|Aniss avance la main vers un sachet.",
        "narrateur|De la farine blanche saute du bois.",
        "narrateur|Il recule, les doigts marqués.",
        "narrateur|La boulangère tourne le sachet, puis s'arrête.",
        "enfant-m|Bonjour.",
        "papa|Elle t'a vu, les mains dehors.",
        "maman|Tes joues sont tièdes, près du four.",
        "narrateur|Le panier attend, l'anse un peu rêche.",
        "enfant-m|Je demande, sans prendre.",
        "narrateur|Le zinc chante au-dessus, plus bas.",
    ),
    (3, 1): L(
        "narrateur|Aniss a le manteau, et le panier.",
        "narrateur|Ils rejoignent le banc du voisin.",
        "narrateur|Une goutte tombe du zinc sur la caisse.",
        "enfant-m|Bonjour !",
        "narrateur|Le col du manteau mange le mot.",
        "narrateur|Le voisin range un pot, sans lever les yeux.",
        "narrateur|Aniss déboutonne le col, les doigts froids.",
        "narrateur|Il attend la fin du pot.",
        "enfant-m|Bonjour.",
        "papa|Là, ta voix est sortie.",
        "maman|Le col frotte le thym, tout près.",
        "narrateur|Une abeille passe le long de la haie.",
        "enfant-m|Je peux demander, col ouvert.",
        "narrateur|Le bois du banc reste froid, sous la haie.",
    ),
    (3, 2): L(
        "narrateur|Aniss marche, le manteau boutonné, vers l'école.",
        "narrateur|L'auvent goutte sur les épaules épaisses.",
        "narrateur|La maîtresse tient un livre sous le bras.",
        "enfant-m|Bonjour, j'ai un… !",
        "narrateur|Les mots se bousculent, trop serrés.",
        "maitresse|Un instant, le livre glisse.",
        "narrateur|Aniss serre les poings dans les poches.",
        "narrateur|Le livre se cale, puis elle le regarde.",
        "enfant-m|Bonjour.",
        "maitresse|Bonjour, plus lentement.",
        "papa|Elle a le livre, et tes mots.",
        "maman|Le manteau fait un bruit de pluie.",
        "narrateur|La nappe tremble, une petite vague.",
        "enfant-m|Je demande, un mot après l'autre.",
    ),
    (3, 3): L(
        "narrateur|Le manteau est chaud, trop chaud près du four.",
        "narrateur|La petite cloche du stand fait ding.",
        "enfant-m|Un pain, s'il… !",
        "narrateur|Le ding couvre la fin de la phrase.",
        "narrateur|Aniss a les joues rouges, sous le col.",
        "narrateur|Il attend que la cloche se taise.",
        "enfant-m|Bonjour.",
        "papa|Elle a levé les yeux, derrière la farine.",
        "maman|Tu as parlé après le ding.",
        "narrateur|Le papier des sachets fait un bruit sec.",
        "enfant-m|Je recommence, sans la cloche.",
        "narrateur|Une goutte glisse du zinc au pavé.",
        "narrateur|Le panier sent le manteau, et la pluie.",
        "enfant-m|Là, j'ai de la place.",
    ),
}

T3Q = {
    1: L(
        "narrateur|Près des pots de thym, l'étal attend.",
        "papa|Le pain, une pomme, ou un livre ?",
        "maman|Que demandes-tu, sans prendre ?",
    ),
    2: L(
        "narrateur|Sous l'auvent, la nappe a un creux.",
        "maman|Le pain, une pomme, ou un livre ?",
        "papa|Que veux-tu, maintenant ?",
    ),
    3: L(
        "narrateur|Sous le zinc, le four souffle un peu.",
        "papa|Le pain, une pomme, ou un livre ?",
        "maman|Que demandes-tu, à voix claire ?",
    ),
}

T3 = {
    (1, 1, 1): L(
        "narrateur|Un pain rond dort dans la caisse, près du thym.",
        "enfant-m|Je le prends !",
        "narrateur|Aniss saisit la croûte.",
        "narrateur|La caisse penche, les pots tremblent.",
        "papa|Les pots, Aniss.",
        "narrateur|Il repose le pain, les mains ouvertes.",
        "enfant-m|Le pain, s'il te plaît.",
        "narrateur|Le voisin glisse le pain dans le panier.",
        "enfant-m|Merci.",
        "maman|La caisse ne penche plus.",
        "narrateur|Une goutte du zinc atterrit sur la croûte.",
        "papa|Elle fait une tache ronde, comme un œil.",
    ),
    (1, 1, 2): L(
        "narrateur|Une pomme rouge se cache entre deux pots.",
        "enfant-m|Elle est à moi !",
        "narrateur|Aniss la tire.",
        "narrateur|De la terre tombe sur le banc.",
        "narrateur|Il la repose, les doigts sales.",
        "enfant-m|La pomme, s'il te plaît.",
        "papa|Il te la tend, sans la terre.",
        "enfant-m|Merci.",
        "maman|Elle brille, malgré la pluie.",
        "narrateur|La pomme garde une rivière, comme la vitre.",
        "narrateur|Aniss la pose dans l'osier, tout contre.",
        "papa|Le thym sent plus fort, tout près.",
    ),
    (1, 1, 3): L(
        "narrateur|Un livre de jardin glisse sous la caisse.",
        "enfant-m|Je le sors !",
        "narrateur|Aniss tire une page.",
        "narrateur|La caisse racle le bois du banc.",
        "papa|Doucement, le livre a peur.",
        "narrateur|Aniss lâche la page.",
        "enfant-m|Le livre, s'il te plaît.",
        "narrateur|Le voisin le sort par le dos, entier.",
        "enfant-m|Merci.",
        "maman|Le coin est un peu mouillé, rien de grave.",
        "narrateur|Une page sent le thym de la soupe.",
        "papa|Tu l'as demandé, pas tiré.",
    ),
    (1, 2, 1): L(
        "narrateur|Un petit pain repose près des sachets.",
        "enfant-m|Pour moi !",
        "narrateur|Aniss parle pendant qu'elle compte.",
        "maitresse|Quatre… attends.",
        "narrateur|Il se tait, le pain trop loin.",
        "narrateur|Le dernier sachet s'empile.",
        "enfant-m|Un pain, s'il te plaît.",
        "maitresse|Le voilà.",
        "enfant-m|Merci.",
        "papa|Elle a fini les nombres, puis toi.",
        "maman|Le pain sent la cuisine, un peu.",
        "narrateur|Une goutte de l'auvent manque le sachet.",
    ),
    (1, 2, 2): L(
        "narrateur|Une pomme ronde attend sur la nappe mouillée.",
        "enfant-m|Je l'attrape !",
        "narrateur|Son bras passe au-dessus du livre.",
        "maitresse|Mon livre, Aniss.",
        "narrateur|Il rentre le bras, déçu.",
        "enfant-m|La pomme, s'il te plaît.",
        "maitresse|Je te la passe par le côté.",
        "enfant-m|Merci.",
        "papa|Le livre est resté fermé.",
        "maman|La nappe a une tache ronde, sous la pomme.",
        "narrateur|La pomme sent l'eau de l'auvent.",
        "narrateur|Aniss la cale dans le panier, sans la presser.",
    ),
    (1, 2, 3): L(
        "narrateur|Le livre de la maîtresse dépasse sous son bras.",
        "enfant-m|Je le vois !",
        "narrateur|Aniss tire le coin.",
        "maitresse|Il tient, celui-là.",
        "narrateur|Les joues d'Aniss chauffent.",
        "narrateur|Un autre livre dort sur la nappe.",
        "enfant-m|Celui de la nappe, s'il te plaît.",
        "maitresse|Oui, celui-là.",
        "enfant-m|Merci.",
        "papa|Tu as changé de livre, sans tirer.",
        "maman|La couverture a une goutte, en forme de toit.",
        "narrateur|Aniss souffle la goutte, elle part.",
    ),
    (1, 3, 1): L(
        "narrateur|Un pain chaud fume, tout près du zinc.",
        "enfant-m|Il est à moi !",
        "narrateur|Aniss touche la croûte.",
        "narrateur|La chaleur pique les doigts.",
        "enfant-m|Aïe.",
        "narrateur|Il secoue la main, puis attend.",
        "enfant-m|Le pain, s'il te plaît.",
        "papa|Elle le met dans le papier.",
        "enfant-m|Merci.",
        "maman|Le papier protège tes doigts.",
        "narrateur|Une goutte du zinc atterrit sur le papier.",
        "narrateur|Le papier fait un petit toc, puis rien.",
    ),
    (1, 3, 2): L(
        "narrateur|Une pomme roule au bord du zinc.",
        "enfant-m|Elle part !",
        "narrateur|Aniss la chasse avec la paume.",
        "narrateur|La pomme tombe vers le pavé.",
        "papa|J'ai les mains.",
        "narrateur|Papa la rattrape, Aniss recule.",
        "enfant-m|La pomme, s'il te plaît.",
        "papa|La voilà, sans la course.",
        "enfant-m|Merci.",
        "maman|Elle n'a pas de bosse.",
        "narrateur|La pomme reflète le stand, tout petit.",
        "narrateur|Aniss la pose, enfin immobile.",
    ),
    (1, 3, 3): L(
        "narrateur|Un livre d'images dort près de la caisse.",
        "narrateur|De la farine recouvre le titre.",
        "enfant-m|Je l'ouvre !",
        "narrateur|Aniss souffle trop fort.",
        "narrateur|La farine saute, un nuage blanc.",
        "narrateur|Il attend que le nuage retombe.",
        "enfant-m|Le livre, s'il te plaît.",
        "papa|Elle l'essuie, puis te le tend.",
        "enfant-m|Merci.",
        "maman|Le titre est revenu, net.",
        "narrateur|Une page sent le beurre, et la pluie.",
        "narrateur|Aniss le glisse sous l'osier, à plat.",
    ),
    (2, 1, 1): L(
        "narrateur|Un pain est posé sur la caisse, près du seau.",
        "enfant-m|Vite, avant la goutte !",
        "narrateur|Aniss avance trop.",
        "narrateur|Une goutte du seau touche la croûte.",
        "narrateur|Il recule, déçu.",
        "enfant-m|Le pain, s'il te plaît.",
        "papa|On l'essuie, puis il est à toi.",
        "enfant-m|Merci.",
        "maman|La croûte a une perle, puis plus.",
        "narrateur|Le seau du jardin ne fait plus plic.",
        "narrateur|Aniss serre le pain contre l'osier.",
        "papa|Tu as attendu la goutte, cette fois.",
    ),
    (2, 1, 2): L(
        "narrateur|Une pomme brille au fond d'une caisse d'eau.",
        "enfant-m|Je la pêche !",
        "narrateur|Son bras n'arrive pas, la flaque est large.",
        "narrateur|Il a envie de marcher dedans.",
        "narrateur|Il s'arrête au bord, bottes collées.",
        "enfant-m|La pomme, s'il te plaît.",
        "papa|Je la sors, sans la flaque.",
        "enfant-m|Merci.",
        "maman|Elle est froide, et propre.",
        "narrateur|La pomme garde une rivière, mince.",
        "narrateur|Le ciel dans la flaque n'est plus cassé.",
        "narrateur|Aniss souffle dessus, un petit nuage.",
    ),
    (2, 1, 3): L(
        "narrateur|Un livre repose sur le banc, une feuille dessus.",
        "enfant-m|Je l'enlève !",
        "narrateur|Aniss arrache la feuille.",
        "narrateur|Une page se lève avec, presque.",
        "papa|La feuille, sans tirer.",
        "narrateur|Il pose la main à plat.",
        "enfant-m|Le livre, s'il te plaît.",
        "narrateur|Le voisin glisse la feuille, puis le livre.",
        "enfant-m|Merci.",
        "maman|La page est restée attachée.",
        "narrateur|La feuille tremble, puis s'envole vers la haie.",
        "papa|Le banc a moins d'eau, sous le livre.",
    ),
    (2, 2, 1): L(
        "narrateur|Un pain sous papier attend, près de l'auvent.",
        "enfant-m|Il va être mouillé !",
        "narrateur|Aniss veut l'attraper, trop vite.",
        "narrateur|Une goutte vise le papier.",
        "maitresse|Un pas de côté.",
        "narrateur|Aniss recule, le papier reste sec.",
        "enfant-m|Le pain, s'il te plaît.",
        "maitresse|Le voilà, à l'abri.",
        "enfant-m|Merci.",
        "papa|Tu as bougé, sans prendre.",
        "maman|Le papier est sec, craquant.",
        "narrateur|L'auvent rate le sachet, goutte à côté.",
    ),
    (2, 2, 2): L(
        "narrateur|Une pomme dort dans une flaque ronde.",
        "narrateur|Le ciel s'y voit, tout petit.",
        "enfant-m|Je la sors !",
        "narrateur|L'eau part en cercles.",
        "maitresse|Le ciel se casse, Aniss.",
        "narrateur|Il attend que les cercles meurent.",
        "enfant-m|La pomme, s'il te plaît.",
        "maitresse|Je la prends par la queue.",
        "enfant-m|Merci.",
        "papa|Le ciel est revenu, entier.",
        "maman|La pomme a un goût d'eau de pluie.",
        "narrateur|Aniss la cale, loin de l'anse mouillée.",
    ),
    (2, 2, 3): L(
        "narrateur|Un livre et une craie blanche dorment ensemble.",
        "enfant-m|La craie !",
        "narrateur|Aniss saisit la craie, pas le livre.",
        "narrateur|Il s'arrête, la craie au poing.",
        "maitresse|Tu voulais le livre, non ?",
        "enfant-m|Oui.",
        "enfant-m|Le livre, s'il te plaît.",
        "maitresse|La craie, tu la reposes ?",
        "enfant-m|Merci, voilà.",
        "papa|Deux gestes, un après l'autre.",
        "maman|La couverture a une virgule de craie.",
        "narrateur|Aniss souffle, la virgule part.",
    ),
    (2, 3, 1): L(
        "narrateur|Un pain fume, trop près des bottes d'Aniss.",
        "enfant-m|J'arrive !",
        "narrateur|L'herbe des bottes tombe sur la farine.",
        "narrateur|Il recule d'un grand pas.",
        "papa|Les bottes, dehors du bois.",
        "narrateur|Aniss tape une botte contre l'autre.",
        "enfant-m|Le pain, s'il te plaît.",
        "papa|Elle le tend, loin des bottes.",
        "enfant-m|Merci.",
        "maman|La farine est restée blanche.",
        "narrateur|Le pain chauffe l'osier, un nid.",
        "narrateur|Une goutte du zinc manque le papier.",
    ),
    (2, 3, 2): L(
        "narrateur|Aniss montre une pomme, le doigt mouillé.",
        "narrateur|La pomme glisse sur le zinc, un peu.",
        "enfant-m|Elle fuit !",
        "narrateur|Il rentre le doigt, collant.",
        "enfant-m|La pomme, s'il te plaît.",
        "papa|Sans le doigt mouillé, cette fois.",
        "enfant-m|Merci.",
        "maman|Elle n'a pas roulé jusqu'au pavé.",
        "narrateur|La pomme a une trace de zinc, mince.",
        "narrateur|Aniss la pose sur un coin sec du panier.",
        "papa|Ton doigt peut sécher, maintenant.",
        "narrateur|Le four souffle, tiède, sur sa main.",
    ),
    (2, 3, 3): L(
        "narrateur|Un livre d'images est ouvert, près de la farine.",
        "enfant-m|Je tourne !",
        "narrateur|Les doigts mouillés collent à la page.",
        "narrateur|La page se lève, trop.",
        "papa|Les mains, Aniss.",
        "narrateur|Il essuie ses doigts sur l'osier.",
        "enfant-m|Le livre, s'il te plaît.",
        "papa|Elle te le ferme, puis te le donne.",
        "enfant-m|Merci.",
        "maman|La page est rentrée, sans déchirure.",
        "narrateur|Le livre a une tache d'eau en forme de toit.",
        "narrateur|Aniss le tient à plat, contre le manteau d'air.",
    ),
    (3, 1, 1): L(
        "narrateur|Un pain rond est trop large pour la poche.",
        "enfant-m|Il rentre !",
        "narrateur|Aniss le pousse dans le manteau.",
        "narrateur|La croûte s'écrase un peu.",
        "papa|Le panier, pas la poche.",
        "narrateur|Il retire le pain, les sourcils bas.",
        "enfant-m|Un sachet, s'il te plaît.",
        "papa|Le voisin te le glisse.",
        "enfant-m|Merci.",
        "maman|Le pain a repris sa rondeur.",
        "narrateur|Le manteau sent le four, plus la pluie.",
        "narrateur|Une miette reste dans la poche, secrète.",
    ),
    (3, 1, 2): L(
        "narrateur|Une pomme accroche un bouton du manteau.",
        "enfant-m|Elle est prise !",
        "narrateur|Aniss tire, le bouton résiste.",
        "narrateur|La queue de la pomme plie.",
        "maman|Le bouton, d'abord.",
        "narrateur|Il déboutonne, lentement.",
        "enfant-m|La pomme, s'il te plaît.",
        "papa|Elle vient, sans la queue cassée.",
        "enfant-m|Merci.",
        "maman|Le bouton est libre, lui aussi.",
        "narrateur|La pomme roule dans le panier, un petit bruit.",
        "narrateur|Le col ouvert laisse passer un tic de gouttière.",
    ),
    (3, 1, 3): L(
        "narrateur|Un livre glisse des mains, vers les pots.",
        "enfant-m|Non !",
        "narrateur|Le livre atterrit dans le thym.",
        "narrateur|Aniss veut le ramasser d'un coup.",
        "papa|On le sort ensemble.",
        "narrateur|Il attend, les mains au-dessus.",
        "enfant-m|Le livre, s'il te plaît.",
        "papa|Le voilà, une feuille de thym dessus.",
        "enfant-m|Merci.",
        "maman|On souffle la feuille, pas la page.",
        "narrateur|Une page sent le thym de la soupe.",
        "narrateur|Le manteau garde une odeur verte, courte.",
    ),
    (3, 2, 1): L(
        "narrateur|Le manteau étouffe la voix d'Aniss, trop près.",
        "enfant-m|Un pain… !",
        "maitresse|J'ai entendu pain, pas le reste.",
        "narrateur|Aniss ouvre le col, une bouffée d'air.",
        "narrateur|Il attend qu'elle pose le livre.",
        "enfant-m|Un pain, s'il te plaît.",
        "maitresse|Le voilà, toute la phrase.",
        "enfant-m|Merci.",
        "papa|Le col ouvert a laissé passer les mots.",
        "maman|Le pain chauffe, contre le tissu.",
        "narrateur|L'auvent goutte sur l'épaule, pas sur le pain.",
        "narrateur|Aniss respire, plus large.",
    ),
    (3, 2, 2): L(
        "narrateur|Aniss veut la pomme pour la poche du manteau.",
        "enfant-m|Dans la poche !",
        "narrateur|La pomme est trop ronde, la poche trop plate.",
        "maitresse|Le panier, peut-être ?",
        "narrateur|Il hésite, puis lâche la poche.",
        "enfant-m|La pomme, s'il te plaît.",
        "maitresse|Pour le panier, d'accord.",
        "enfant-m|Merci.",
        "papa|La poche garde tes mains, pas le fruit.",
        "maman|La pomme a de la place, dans l'osier.",
        "narrateur|Un bouton frotte l'anse, un petit clic.",
        "narrateur|La nappe ne tremble plus, sous l'auvent.",
    ),
    (3, 2, 3): L(
        "narrateur|Aniss veut le livre sous le bras de la maîtresse.",
        "enfant-m|Celui-là !",
        "maitresse|J'en ai besoin, un moment.",
        "narrateur|Un autre livre attend sur la nappe, plus petit.",
        "narrateur|Aniss avale sa déception.",
        "enfant-m|L'autre livre, s'il te plaît.",
        "maitresse|Oui, celui de la nappe.",
        "enfant-m|Merci.",
        "papa|Tu as changé d'idée, sans tirer.",
        "maman|Le petit livre entre dans le panier, juste.",
        "narrateur|La couverture a une goutte, en forme de toit.",
        "narrateur|Le manteau fait un bruit de pluie, puis se tait.",
    ),
    (3, 3, 1): L(
        "narrateur|La cloche fait ding, Aniss crie par-dessus.",
        "enfant-m|Un pain !",
        "narrateur|Personne n'a la fin du mot.",
        "narrateur|Il attend le silence après le ding.",
        "enfant-m|Le pain, s'il te plaît.",
        "papa|Elle l'a entendu, entier.",
        "enfant-m|Merci.",
        "maman|Le papier craque, chaud.",
        "narrateur|La cloche du four reste muette, après.",
        "narrateur|Le pain fume dans l'osier, un nuage court.",
        "papa|Tu as parlé dans le creux.",
        "narrateur|Une goutte glisse du zinc, sans ding.",
    ),
    (3, 3, 2): L(
        "narrateur|La manche du manteau balaie le zinc.",
        "narrateur|Deux pommes roulent, l'une vers l'autre.",
        "enfant-m|Oh !",
        "narrateur|Aniss plaque les mains contre lui.",
        "enfant-m|Les pommes, s'il te plaît.",
        "papa|Une seule, la plus proche.",
        "enfant-m|Merci.",
        "maman|L'autre est rentrée, sans bosse.",
        "narrateur|La pomme sent le manteau, et le four.",
        "narrateur|Aniss la cale loin de la manche.",
        "papa|Les manches peuvent rester collées, maintenant.",
        "narrateur|Le zinc n'a plus de course de fruits.",
    ),
    (3, 3, 3): L(
        "narrateur|Un livre d'images est collé à la vitre du stand.",
        "enfant-m|Celui de la fenêtre !",
        "narrateur|Aniss tape le verre, trop fort.",
        "narrateur|La cloche tinte, un peu.",
        "papa|Le verre, Aniss.",
        "narrateur|Il met les mains dans le dos.",
        "enfant-m|Le livre, s'il te plaît.",
        "papa|Elle le décroche, sans le verre.",
        "enfant-m|Merci.",
        "maman|La vitre a un rond de doigt, puis plus.",
        "narrateur|Le livre a une tache d'eau en forme de toit.",
        "narrateur|Aniss le serre, le manteau ouvert enfin.",
    ),
}

FINS = {
    (1, 1, 1): L(
        "narrateur|Ils rentrent, le pain rond dans l'osier.",
        "narrateur|La soupe n'a plus de vapeur sur la vitre.",
        "enfant-m|Il a une tache d'eau, mon pain.",
        "papa|Comme un œil, oui.",
        "maman|Merci, Aniss.",
        "narrateur|La gouttière fait un tic, puis plus rien.",
        "narrateur|L'oiseau gris se pose sur le zinc, sans bruit.",
        "narrateur|La miette dorée n'attend plus, près de l'assiette.",
    ),
    (1, 1, 2): L(
        "narrateur|La pomme voyage dans le panier, jusqu'à la table.",
        "narrateur|Elle garde sa rivière, mince.",
        "enfant-m|Comme ma vitre.",
        "maman|Oui.",
        "papa|Merci, elle n'a pas de terre.",
        "narrateur|Le thym de la caisse sent dans la cuisine.",
        "narrateur|La chaussette rouge sèche, vue du rebord.",
        "narrateur|Aniss croque, et la gouttière se tait.",
    ),
    (1, 1, 3): L(
        "narrateur|Le livre de jardin s'ouvre près de la soupe.",
        "narrateur|Une page sent le thym, fort.",
        "enfant-m|C'est notre odeur.",
        "papa|Oui.",
        "maman|Merci, la page est entière.",
        "narrateur|Le coin mouillé sèche, lentement.",
        "narrateur|Sur la haie, l'oiseau gris secoue une dernière plume.",
        "narrateur|La vitre n'a plus de rivière sous le doigt.",
    ),
    (1, 2, 1): L(
        "narrateur|Le petit pain rentre, près de la casserole.",
        "narrateur|Il sent la cuisine, et l'auvent.",
        "enfant-m|Elle a fini de compter.",
        "maman|Puis elle t'a entendu.",
        "papa|Merci, Aniss.",
        "narrateur|Les sachets de l'école restent dehors, empilés.",
        "narrateur|Une flaque ronde n'a plus de ciel cassé.",
        "narrateur|La gouttière laisse le zinc tranquille.",
    ),
    (1, 2, 2): L(
        "narrateur|La pomme de la nappe roule jusqu'à l'assiette.",
        "narrateur|Sa tache ronde a séché.",
        "enfant-m|Le livre n'a pas bougé.",
        "papa|Tu es passé à côté.",
        "maman|Merci, Aniss.",
        "narrateur|La nappe de papier ne tremble plus.",
        "narrateur|Dans la cuisine, la vapeur a disparu.",
        "narrateur|Une craie blanche n'a plus rien à dire.",
    ),
    (1, 2, 3): L(
        "narrateur|Le petit livre de la nappe s'ouvre sur les genoux.",
        "narrateur|La goutte en forme de toit a fui.",
        "enfant-m|J'ai soufflé dessus.",
        "maman|Oui.",
        "papa|Merci, tu n'as pas tiré l'autre.",
        "narrateur|Le livre sous le bras de la maîtresse est resté là-bas.",
        "narrateur|La vitre de la cuisine est nette, sans nuage.",
        "narrateur|Le stand, au coin, a rangé sa nappe à lui.",
    ),
    (1, 3, 1): L(
        "narrateur|Le papier du pain craque, sur la table.",
        "narrateur|La goutte du zinc a laissé un toc.",
        "enfant-m|Mes doigts n'ont plus chaud.",
        "papa|Le papier a fait le travail.",
        "maman|Merci, Aniss.",
        "narrateur|L'air du four s'est arrêté aux joues.",
        "narrateur|Les chaussures de papa ne gouttent plus, près de la porte.",
        "narrateur|Un tic, puis le zinc se tait.",
    ),
    (1, 3, 2): L(
        "narrateur|La pomme du stand ne roule plus.",
        "narrateur|Elle reflète la fenêtre, toute petite.",
        "enfant-m|Je vois la maison dedans.",
        "maman|Nous aussi.",
        "papa|Merci, elle n'a pas de bosse.",
        "narrateur|Le pavé n'a pas reçu de fruit.",
        "narrateur|La soupe sent le beurre, un peu, par erreur.",
        "narrateur|La rivière du doigt d'Aniss a séché sur la vitre.",
    ),
    (1, 3, 3): L(
        "narrateur|Le livre essuyé s'ouvre, le titre net.",
        "narrateur|Une page sent le beurre, et la pluie.",
        "enfant-m|Le nuage blanc est parti.",
        "papa|La farine est rentrée.",
        "maman|Merci, Aniss.",
        "narrateur|Le stand a baissé son zinc, un peu.",
        "narrateur|L'oiseau gris picore une miette, dehors.",
        "narrateur|La miette dorée de l'assiette a un ami.",
    ),
    (2, 1, 1): L(
        "narrateur|Le pain essuyé rentre, l'osier contre le ventre.",
        "narrateur|La perle d'eau n'est plus sur la croûte.",
        "enfant-m|Le seau s'est tu.",
        "papa|Plic, puis plus.",
        "maman|Merci, Aniss.",
        "narrateur|Les bottes laissent deux traces, près de la porte.",
        "narrateur|La feuille du seau ne tremble plus.",
        "narrateur|La gouttière du jardin rend le silence.",
    ),
    (2, 1, 2): L(
        "narrateur|La pomme froide pose sa rivière sur la table.",
        "narrateur|Aniss souffle un petit nuage, dessus.",
        "enfant-m|Le ciel de la flaque est entier.",
        "maman|Oui.",
        "papa|Merci, tes bottes sont restées au bord.",
        "narrateur|L'herbe mouillée sent dans la maison, un peu.",
        "narrateur|La chaussette rouge n'a plus d'eau à craindre.",
        "narrateur|Un oiseau gris boit la flaque, dehors.",
    ),
    (2, 1, 3): L(
        "narrateur|Le livre du banc s'ouvre, la page attachée.",
        "narrateur|La feuille s'est envolée vers la haie.",
        "enfant-m|Elle a choisi l'oiseau.",
        "papa|Peut-être.",
        "maman|Merci, tu n'as pas arraché.",
        "narrateur|Le banc a moins d'eau, sous la pluie finie.",
        "narrateur|L'anse du panier ne glisse plus, sèche.",
        "narrateur|Un dernier plic, puis le seau se tait.",
    ),
    (2, 2, 1): L(
        "narrateur|Le pain à l'abri craque, dans la cuisine.",
        "narrateur|Le papier est resté sec.",
        "enfant-m|J'ai fait un pas de côté.",
        "papa|C'était le bon pas.",
        "papa|Merci, Aniss.",
        "narrateur|L'auvent rate le sachet, loin d'ici.",
        "narrateur|Les dalles de l'école gardent leurs gouttes.",
        "narrateur|Le zinc de la maison chante plus juste.",
    ),
    (2, 2, 2): L(
        "narrateur|La pomme à la queue s'assoit près du bol.",
        "narrateur|Elle a un goût d'eau de pluie.",
        "enfant-m|Les cercles sont morts.",
        "maman|Le ciel s'est recollé.",
        "papa|Merci, tu as attendu.",
        "narrateur|La flaque ronde n'a plus de fruit.",
        "narrateur|La nappe de l'école ne tremble plus.",
        "narrateur|Aniss essuie un rond sur la vitre, net.",
    ),
    (2, 2, 3): L(
        "narrateur|Le livre sans craie s'ouvre, propre.",
        "narrateur|La virgule blanche est partie.",
        "enfant-m|J'ai reposé la craie.",
        "papa|Deux gestes, un après l'autre.",
        "maman|Merci, Aniss.",
        "narrateur|La craie reste sous l'auvent, pour demain.",
        "narrateur|Le portail mouillé brille, sans servir.",
        "narrateur|La gouttière laisse les pages au sec.",
    ),
    (2, 3, 1): L(
        "narrateur|Le pain loin des bottes chauffe l'osier.",
        "narrateur|Un nid chaud, contre le ventre.",
        "enfant-m|La farine est blanche.",
        "papa|Tes bottes ont tapé dehors.",
        "maman|Merci, Aniss.",
        "narrateur|L'herbe des jardins n'est plus sur le bois.",
        "narrateur|Le four du stand a fermé sa bouche.",
        "narrateur|Une goutte du zinc manque la maison, aussi.",
    ),
    (2, 3, 2): L(
        "narrateur|La pomme au zinc s'arrête, enfin.",
        "narrateur|La trace mince sèche sur sa peau.",
        "enfant-m|Mon doigt a séché.",
        "maman|Près du four, oui.",
        "papa|Merci, tu as rentré le doigt.",
        "narrateur|Le stand n'a plus de course de fruit.",
        "narrateur|Les bottes, près de la porte, ont fini de boire.",
        "narrateur|Aniss pose la pomme où la soupe fume, à côté.",
    ),
    (2, 3, 3): L(
        "narrateur|Le livre à plat n'a plus de page collée.",
        "narrateur|La tache en forme de toit pâlit.",
        "enfant-m|Mes doigts sont secs.",
        "papa|L'osier a aidé.",
        "maman|Merci, Aniss.",
        "narrateur|Le zinc du stand a rangé ses images.",
        "narrateur|Une farine blanche n'a plus de main mouillée.",
        "narrateur|La vitre de la maison reprend sa rivière, claire.",
    ),
    (3, 1, 1): L(
        "narrateur|Le pain du sachet reprend sa rondeur, sur la table.",
        "narrateur|Une miette secrète reste dans la poche.",
        "enfant-m|Le manteau sent le four.",
        "papa|Plus la pluie.",
        "maman|Merci, Aniss.",
        "narrateur|Le rideau jaune de la chambre ne bouge plus.",
        "narrateur|Les boutons ronds sont froids, contre le cou, plus.",
        "narrateur|La gouttière laisse le sachet tranquille.",
    ),
    (3, 1, 2): L(
        "narrateur|La pomme du bouton roule une dernière fois, puis s'arrête.",
        "narrateur|Le col ouvert laisse un tic, puis rien.",
        "enfant-m|Le bouton est libre.",
        "maman|La queue aussi.",
        "papa|Merci, tu as déboutonné.",
        "narrateur|Le manteau sèche sur la chaise, près de la vitre.",
        "narrateur|Une rivière de chambre a disparu.",
        "narrateur|L'oiseau gris n'a plus de pluie à secouer.",
    ),
    (3, 1, 3): L(
        "narrateur|Le livre du thym s'ouvre, une odeur verte.",
        "narrateur|La feuille a quitté la page.",
        "enfant-m|On a soufflé ensemble.",
        "papa|Oui.",
        "maman|Merci, tu as attendu les mains.",
        "narrateur|Le manteau garde une odeur courte, près de la chaise.",
        "narrateur|Les pots du voisin sont rentrés, sous la haie.",
        "narrateur|La vitre de la chambre est sèche, sans rivière.",
    ),
    (3, 2, 1): L(
        "narrateur|Le pain de la phrase entière chauffe le tissu.",
        "narrateur|L'auvent n'a pas touché la croûte.",
        "enfant-m|Elle a eu toute la phrase.",
        "maman|Toute la phrase, oui.",
        "papa|Merci, le col était ouvert.",
        "narrateur|Le manteau s'ouvre, une bouffée d'air de soupe.",
        "narrateur|Le livre sous le bras est resté à l'école.",
        "narrateur|Un tic de gouttière, puis le silence du pain.",
    ),
    (3, 2, 2): L(
        "narrateur|La pomme du panier a de la place, enfin.",
        "narrateur|La poche du manteau reste plate, pour les mains.",
        "enfant-m|Pas dans la poche.",
        "maman|Dans l'osier, oui.",
        "papa|Merci, tu as changé.",
        "narrateur|Un bouton a fait clic, puis plus.",
        "narrateur|La nappe de l'école ne tremble plus.",
        "narrateur|Le rideau jaune encadre le stand, loin, éteint.",
    ),
    (3, 2, 3): L(
        "narrateur|Le petit livre de la nappe s'endort dans l'osier.",
        "narrateur|La goutte-toit a séché, un cercle pâle.",
        "enfant-m|Pas celui sous le bras.",
        "papa|L'autre, oui.",
        "maman|Merci, tu n'as pas tiré.",
        "narrateur|Le manteau fait un dernier bruit de pluie, puis se tait.",
        "narrateur|La chaise de la chambre n'a plus de manteau.",
        "narrateur|Au coin, le zinc n'a plus de cloche.",
    ),
    (3, 3, 1): L(
        "narrateur|Le pain du creux fume, un nuage court, puis plus.",
        "narrateur|La cloche du four reste muette.",
        "enfant-m|J'ai parlé après le ding.",
        "papa|Toute la phrase, oui.",
        "maman|Merci, Aniss.",
        "narrateur|Le manteau trop chaud s'ouvre, près de la soupe.",
        "narrateur|Une goutte du zinc n'a plus de ding à faire.",
        "narrateur|Les chaussures près de la porte sont sèches, enfin.",
    ),
    (3, 3, 2): L(
        "narrateur|La pomme loin de la manche s'assoit, sage.",
        "narrateur|L'autre est restée au stand, sans bosse.",
        "enfant-m|Mes manches sont collées.",
        "maman|Elles peuvent.",
        "papa|Merci, tu as plaqué les mains.",
        "narrateur|Le zinc n'a plus de course de fruits.",
        "narrateur|Le rideau jaune ne balaie plus rien.",
        "narrateur|Aniss pose la pomme où la chaussette rouge sèche.",
    ),
    (3, 3, 3): L(
        "narrateur|Le livre décroché de la vitre s'ouvre, ici.",
        "narrateur|Le rond de doigt a quitté le verre du stand.",
        "enfant-m|Mes mains étaient dans le dos.",
        "papa|Oui.",
        "maman|Merci, Aniss.",
        "narrateur|Le manteau ouvert laisse l'air de la soupe.",
        "narrateur|La tache-toit pâlit sur la couverture.",
        "narrateur|La gouttière fait un tic, très loin, puis le silence.",
    ),
}


SONS = {
    "CHK_T0000_P0000": "gouttiere,soupe",
    "CHK_T0001_P0001": "soupe,vapeur",
    "CHK_T0001_P0002": "goutte,seau",
    "CHK_T0001_P0003": "tissu,rideau",
}
SONS_T2 = {1: "thym,pot", 2: "auvent,craie", 3: "zinc,four"}
SONS_T3 = {1: "pain,papier", 2: "pomme", 3: "livre,page"}
SONS_FIN = {1: "gouttiere,silence", 2: "vitre,oiseau", 3: "zinc,soupe"}

QMETA = {
    1: qf(
        "bonjour",
        "bonjour | bonjour maman | bonjour papa",
        "La vapeur s'est tue. Aniss a dit quel mot, en premier ?",
        "Oui, il a dit bonjour.",
    ),
    2: qf(
        "s'il te plaît",
        "s'il te plaît | s'il te plait | sil te plait",
        "L'anse a glissé. Aniss a demandé comment ?",
        "Oui, s'il te plaît.",
    ),
    3: qf(
        "merci",
        "merci | merci papa | merci maman",
        "La manche est droite. Aniss a dit quoi ?",
        "Oui, merci.",
    ),
}


def build() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {
        "CHK_T0000_P0000": DEBUT,
        "CHK_T0001_P0000": T1Q,
    }
    sons: dict[str, str] = dict(SONS)
    extras: dict[str, dict] = {
        "CHK_T0001_P0000": t3("la cuisine", "le jardin", "la chambre"),
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = T1[i]
        s[f"{p}_Q0001"] = Q1[i]
        extras[f"{p}_Q0001"] = QMETA[i]
        s[f"{p}_C0001"] = C1[i]
        s[f"{p}_T0002_P0000"] = T2Q[i]
        extras[f"{p}_T0002_P0000"] = t3("le voisin", "la maîtresse", "la boulangère")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = T2[(i, j)]
            sons[p2] = SONS_T2[j]
            s[f"{p2}_T0003_P0000"] = T3Q[j]
            extras[f"{p2}_T0003_P0000"] = t3("le pain", "une pomme", "un livre")
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
        voice(nc, profile_for(cid, kind), extra_note=f"chunk={cid}")
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = "Aniss, papa, maman"
    out["setting"] = "maison sous la pluie, gouttière, stand de zinc"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "les trois mots",
        "tout doux",
        "tout calme",
        "il faut demander",
        "on doit demander",
        "bravo. tu as",
        "bon travail",
        "papa sourit",
        "maman sourit",
        "tu as dit les mots",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan: {bad}")
    if TICS.search(blob):
        raise SystemExit(f"{SID} tic corpus")
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
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    lo, hi, avg = path_words(scripts)
    print(f"chemins {lo}–{hi} mots (moyenne {avg:.0f})")
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
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Sous la pluie, la gouttière fait tic contre le zinc. Aniss veut un pain "
        "au stand avant qu'on range l'étal. Il crie trop tôt : on entend « stand », "
        "pas « pain ». Il serre les poings, puis les ouvre. Cuisine, jardin ou "
        "chambre changent l'obstacle ; voisin, maîtresse ou boulangère changent "
        "l'écoute ; pain, pomme ou livre changent ce qu'il demande. La gouttière, "
        "le zinc et la vitre paient la fin.\n\n"
        "## Vécu\n\n"
        "Aniss veut un pain au stand de zinc avant qu'on range l'étal. Il crie trop "
        "tôt : la gouttière couvre sa voix, on n'entend que « stand ». Cuisine "
        "(vapeur, panier), jardin (anse glissante, seau) ou chambre (manche à "
        "l'envers) changent l'obstacle. Voisin, maîtresse ou boulangère changent "
        "l'écoute. Pain, pomme ou livre changent ce qu'il demande. Bonjour / s'il "
        "te plaît / merci au moment du besoin, jamais récités. 27 fins : la "
        f"gouttière, le zinc, la vitre. Chemins {lo}–{hi} mots (moyenne {avg:.0f}).\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Troupe D16 : Aniss, papa, maman.\n"
        "- 86 nœuds, graphe et libellés d'options conservés.\n"
        "- 27 fins textuellement distinctes, 27 résolutions distinctes, 9 T2 distincts.\n"
        "- Première tentative échoue. Chaque choix change l'obstacle, le climax, la dernière image.\n"
        "- Retour de la gouttière, du zinc, de la rivière sur la vitre, de l'oiseau gris, de la chaussette rouge.\n"
        "- TTS par fonction (ouverture, choix, indice, confirmation, action, obstacle, résolution, retour).\n"
        "- `slow` réservé aux choix, à l'indice et aux fins.\n"
        "- N2 ≤ 15 mots/phrase. Pas de leçon dite. Pas de tics « tout doux / encore / déjà / tout calme ». Pas de « les trois mots » dans le récit.\n"
        "- Monde ≠ TREE-COL-001 (pommes), ≠ TREE-COL-025 (gouttière Nina, main), ≠ TREE-COL-012 (bâche).\n"
        "- P1 F-NAR-019. Pas apply. Pas audio.\n\n"
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
