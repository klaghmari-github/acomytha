#!/usr/bin/env python3
"""TREE-COL-002 — Le banc mouillé d'Amir (F-NAR-019). N2, COL.ECO.001.

Parc, banc de fer, platane, flaque, boîte verte à clapet.
Leçon vécue : partage / tour / soin. Jamais dite.
Monde ≠ TREE-COL-023 (banc bois, pommier, pomme de Mila).
Texte + TTS. Pas apply.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, words  # noqa: E402

SID = "TREE-COL-002"
N2 = LIMITS["N2"]
TITLE = "Le banc mouillé d'Amir"
FIL = (
    "Au coin des écailles, Amir veut poser sa boîte verte à clapet "
    "sur une latte sèche, pour partager le goûter avec Nina avant que "
    "le soleil mange la flaque. Il s'assoit trop vite : le fer glisse, "
    "Nina parle en même temps. Pomme, yaourt ou pain changent le reste "
    "qui menace le banc. Cuisine, jardin ou chambre changent le second "
    "imprévu. Cubes, livre ou dînette changent le dernier geste. "
    "Le clapet, l'écaille et la graine-hélice paient la fin."
)
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="clapet",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=la_boite_va_glisser_sur_le_fer; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_le_goûter; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=le_reste_a_une_place; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrete; intensite=1; destinataire=enfant; sous_texte=le_banc_reste_net; tempo=naturel; sourire=léger; respiration=fluide",
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
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_retenue; intensite=2; destinataire=enfant; sous_texte=deux_envies_sur_la_meme_place; tempo=resserre; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis=None,
        note="arc=resolution; intention=faire_vivre_la_reussite; emotion=fierte_calme; intensite=2; destinataire=enfant; sous_texte=le_tour_a_ouvert_la_place; tempo=naturel; sourire=franc; respiration=relachee",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="clapet",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierte_calme; intensite=1; destinataire=enfant; sous_texte=le_clapet_et_l_ecaille_reviennent; tempo=pose; sourire=léger; respiration=ample",
    ),
}


def L(*rows: str) -> list[str]:
    out: list[str] = []
    prev = ""
    run = 1
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
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
    "narrateur|Après la pluie, le parc du village cligne.",
    "narrateur|Le platane lâche des graines en hélice.",
    "narrateur|Une graine tourne, puis se pose dans la flaque.",
    "narrateur|Le banc de fer luit, vert d'écailles.",
    "narrateur|Une écaille de peinture flotte, minuscule bateau.",
    "narrateur|Ça sent l'écorce mouillée, et le pain tiède.",
    "narrateur|La boîte verte d'Amir pèse contre sa hanche.",
    "narrateur|Son clapet fait clic, un petit métal.",
    "narrateur|Nina arrive, les genoux mouillés, les joues roses.",
    "enfant-f|Je veux la latte du milieu !",
    "enfant-m|Non, c'est pour le goûter, maintenant.",
    "narrateur|En ce moment, Amir pose la boîte trop vite.",
    "narrateur|Le fer glissant la chasse vers la flaque.",
    "enfant-m|Elle tombe !",
    "narrateur|Nina parle en même temps, trop fort.",
    "papa|Une latte pour toi, une pour elle.",
    "maman|Le torchon à carreaux, il est dans le sac ?",
    "narrateur|Papa essuie une seule latte, pas tout le banc.",
    "enfant-m|Mes fesses sont mouillées.",
    "maman|On peut s'asseoir, sur la latte sèche.",
    "narrateur|Le clapet a fait clic, puis plus rien.",
)

T1Q = L(
    "narrateur|Dans le sac, la boîte verte attend, un peu humide.",
    "maman|Amir, tu prends quoi, dans le sac ?",
    "narrateur|Une pomme, un yaourt, ou un morceau de pain.",
)

T1 = {
    1: L(
        "narrateur|Amir ouvre le clapet, clic, trop vite.",
        "narrateur|La pomme rouge roule vers le bord.",
        "enfant-m|Elle est à moi !",
        "enfant-f|Moi aussi, la rouge !",
        "narrateur|Leurs deux mains se cognent sur la peau.",
        "narrateur|La pelure tombe vers la latte mouillée.",
        "enfant-m|C'est rien.",
        "narrateur|La pelure colle au fer, comme une langue.",
        "papa|Le sac est ouvert, juste à côté.",
        "narrateur|Amir attend que Nina retire sa main.",
        "enfant-m|Tu veux un morceau, après ?",
        "enfant-f|Oui, quand tu as fini ta bouchée.",
        "narrateur|Il glisse la pelure dans le sac.",
        "maman|Merci, le fer reste net.",
        "narrateur|Une écaille verte tremble, près de la flaque.",
        "papa|Vous avez chacun une latte, et un morceau.",
    ),
    2: L(
        "narrateur|Amir soulève le yaourt, le couvercle frémit.",
        "narrateur|Le vent du platane le soulève, presque.",
        "enfant-m|Je le plaque sur le banc !",
        "narrateur|Le couvercle colle au fer mouillé.",
        "enfant-f|C'est un bateau, pour la flaque !",
        "narrateur|Nina tire, le blanc s'étale un peu.",
        "enfant-m|Arrête !",
        "papa|Le sac, il peut le garder.",
        "narrateur|Amir attend la fin de la phrase de Nina.",
        "enfant-f|Bon, un bateau de feuille, alors.",
        "narrateur|Il décolle le couvercle, blanc et mouillé.",
        "narrateur|Le couvercle rejoint le sac, sans voler.",
        "maman|Merci, la flaque n'a pas de blanc.",
        "narrateur|Nina pose une feuille, qui tourne, hélice.",
        "papa|Le yaourt, une cuillère, puis l'autre.",
        "enfant-m|À toi, après ma cuillerée.",
    ),
    3: L(
        "narrateur|Amir casse le pain, une miette saute.",
        "narrateur|Elle atterrit sur le bois du banc.",
        "enfant-m|Je souffle, dans la flaque.",
        "narrateur|Un pigeon gris picore, trop près.",
        "enfant-f|C'est pour mon restaurant !",
        "narrateur|Leurs souffles se croisent, la miette roule.",
        "maman|La terre, sous le platane, a faim.",
        "narrateur|Amir se tait, le temps du pigeon.",
        "enfant-m|Je la pose, sous l'arbre.",
        "narrateur|La miette rejoint la terre, au pied.",
        "enfant-f|Le reste du pain, on le partage ?",
        "papa|Une bouchée pour toi, une pour elle.",
        "maman|Merci, le bois n'a plus de miette.",
        "narrateur|La graine en hélice s'est arrêtée, dans l'eau.",
        "enfant-m|Le clapet, je le ferme.",
        "narrateur|Le clic est plus doux, cette fois.",
    ),
}

Q1 = {
    1: L(
        "narrateur|La pelure allait sur le banc.",
        "maman|Amir l'a mise où ?",
    ),
    2: L(
        "narrateur|Le couvercle voulait s'envoler.",
        "papa|Amir l'a mis où ?",
    ),
    3: L(
        "narrateur|La miette était sur le bois.",
        "maman|Amir l'a mise où ?",
    ),
}

C1 = {
    1: L(
        "enfant-m|Dans le sac !",
        "papa|Oui, dans le sac.",
        "narrateur|La pomme a un côté nu, un peu collant.",
        "enfant-f|Mon morceau, maintenant.",
        "maman|Le clapet peut se fermer.",
        "narrateur|La flaque rétrécit, un nuage s'en va.",
        "enfant-m|On rentre, le fer sèche.",
    ),
    2: L(
        "enfant-m|Dans le sac !",
        "maman|Oui, le sac l'a reçu.",
        "narrateur|Le yaourt tient, sans son chapeau.",
        "enfant-f|Ma feuille-bateau tourne, toute seule.",
        "papa|Le clapet, on le ferme ?",
        "narrateur|Le blanc du fer a disparu, essuyé.",
        "enfant-m|La flaque devient petite.",
    ),
    3: L(
        "enfant-m|Sur la terre !",
        "papa|Oui, sous le platane.",
        "narrateur|Le pain sent le sac, tiède.",
        "enfant-f|On a partagé, bouchée par bouchée.",
        "maman|Le pigeon a sa miette.",
        "narrateur|Une écaille reste collée au torchon.",
        "enfant-m|On rentre, le fer sèche.",
    ),
}

T2Q = {
    1: L(
        "narrateur|La pomme est finie, la flaque rétrécit.",
        "papa|On rentre où, après le banc ?",
        "maman|La cuisine, le jardin, ou la chambre ?",
    ),
    2: L(
        "narrateur|Le yaourt est vide, le clapet cligne.",
        "maman|On rentre où, après le banc ?",
        "papa|La cuisine, le jardin, ou la chambre ?",
    ),
    3: L(
        "narrateur|Le pain est parti, le pigeon aussi.",
        "papa|On rentre où, après le banc ?",
        "maman|La cuisine, le jardin, ou la chambre ?",
    ),
}

T2 = {
    (1, 1): L(
        "narrateur|Ils rentrent, la boîte verte mouillée sous le bras.",
        "narrateur|La cuisine sent le cacao, une tasse fume.",
        "narrateur|Amir pose la boîte sur la table, trop près.",
        "narrateur|Un cercle d'eau apparaît, autour du clapet.",
        "enfant-m|Je coupe une autre pomme !",
        "narrateur|Nina tend la main vers le couteau.",
        "maman|J'ai la casserole, une seconde.",
        "narrateur|Amir avale son mot, les joues chaudes.",
        "narrateur|La vapeur passe, maman se tourne.",
        "enfant-m|Une serviette, s'il te plaît.",
        "papa|La voilà, sous la tasse.",
        "narrateur|Ils glissent la boîte sur le tissu sec.",
        "enfant-f|Ma place, c'est le bord, près de toi.",
        "maman|Le cacao attend, lui aussi.",
    ),
    (1, 2): L(
        "narrateur|Ils passent au jardin, la boîte contre la hanche.",
        "narrateur|Une marche de pierre luit, pleine d'eau.",
        "enfant-f|On enterre le trognon, ici !",
        "narrateur|Nina creuse près de la laitue, trop fort.",
        "narrateur|De la terre saute sur le clapet.",
        "enfant-m|Ma boîte !",
        "papa|La caisse à outils, elle est sèche.",
        "narrateur|Amir recule, déçu, les mains sales.",
        "enfant-m|Le trognon, sur la terre, pas sur la pierre.",
        "narrateur|Nina pose le bâton, puis l'écoute.",
        "enfant-f|D'accord, la caisse pour la boîte.",
        "maman|Une place pour le trognon, une pour vous.",
        "narrateur|Une graine d'hélice s'est collée à l'osier.",
        "papa|Le fer du parc est loin, et sec.",
    ),
    (1, 3): L(
        "narrateur|Ils montent dans la chambre, la boîte goutte.",
        "narrateur|Amir la pose sur l'oreiller, trop vite.",
        "narrateur|Une feuille mouillée imprime le tissu, verte.",
        "enfant-f|Le lit, c'est le banc !",
        "narrateur|Nina saute, la couverture fait une vague.",
        "enfant-m|Tu mouilles tout !",
        "maman|La serviette de bain, sous la boîte.",
        "narrateur|Amir attend que la vague s'arrête.",
        "enfant-m|Toi le bord, moi le milieu.",
        "enfant-f|Et l'oreiller, c'est la flaque, on marche pas.",
        "papa|Le clapet a laissé un rond, sur l'éponge.",
        "narrateur|Ils s'assoient, chacun un côté du lit.",
        "maman|La feuille imprimée sèche, un petit dessin.",
        "narrateur|Le doudou garde le bas du lit, invité.",
    ),
    (2, 1): L(
        "narrateur|Ils rentrent, le couvercle tremble dans le sac.",
        "narrateur|La cuisine fume, le cacao chante dans la casserole.",
        "narrateur|Le couvercle glisse, tombe près de la tasse.",
        "enfant-f|Un bateau, dans le cacao !",
        "enfant-m|Non, il va fondre !",
        "narrateur|Nina a la main ouverte, au-dessus de la vapeur.",
        "papa|Le sac l'a gardé, dehors.",
        "narrateur|Amir attend que Nina pose la main.",
        "enfant-m|Le couvercle, on le remet.",
        "enfant-f|Alors une cuillère pour toi, une pour moi.",
        "maman|Le cacao, après, dans la même tasse.",
        "narrateur|Ils glissent le couvercle, le sac se ferme.",
        "papa|La table a de la place, au bord.",
        "narrateur|Le clapet fait clic, un peu de cacao sur le vert.",
    ),
    (2, 2): L(
        "narrateur|Ils vont au jardin, un souffle dans les haies.",
        "narrateur|Le couvercle s'échappe du sac, blanc et léger.",
        "enfant-f|Il vole, comme au parc !",
        "narrateur|Nina court vers l'arrosoir, trop vite.",
        "narrateur|Le blanc vise le bec, puis s'accroche.",
        "enfant-m|Attends, je le demande.",
        "papa|Tu l'as, Nina ?",
        "enfant-f|Oui, il est collé.",
        "narrateur|Amir tend la main, sans arracher.",
        "enfant-m|Le sac, s'il te plaît.",
        "narrateur|Nina souffle, puis le lui donne.",
        "maman|L'arrosoir n'a pas bu le blanc.",
        "narrateur|Une feuille de platane, dans la poche, sert de bateau.",
        "papa|Le vent du jardin s'est tu, un instant.",
    ),
    (2, 3): L(
        "narrateur|Ils arrivent dans la chambre, le yaourt sent fort.",
        "enfant-f|J'ouvre l'autre, sur le drap !",
        "narrateur|Nina bascule un pot du goûter, trop loin.",
        "narrateur|Une goutte blanche vise le drap bleu.",
        "enfant-m|Le drap !",
        "maman|Un torchon, vite, sous le pot.",
        "narrateur|Amir plaque le tissu, les dents serrées.",
        "narrateur|La goutte s'arrête, ronde, sur le carreau.",
        "enfant-m|Un pot, deux cuillères.",
        "enfant-f|D'accord, tu commences, je compte.",
        "papa|Le clapet reste fermé, sur la chaise.",
        "narrateur|Ils mangent à tour, assis sur le tapis.",
        "maman|Le drap est resté bleu, sans île blanche.",
        "narrateur|Le doudou a droit à une cuillère vide, pour de faux.",
    ),
    (3, 1): L(
        "narrateur|Ils rentrent, des miettes dans la manche d'Amir.",
        "narrateur|La cuisine a un pigeon à la vitre, qui penche.",
        "narrateur|Les miettes tombent sur la table, une pluie sèche.",
        "enfant-f|Je les jette, pour lui, maintenant !",
        "enfant-m|Attends, la vitre est fermée.",
        "narrateur|Nina a le poing plein, levé.",
        "papa|Un bol, on les met là.",
        "narrateur|Amir ouvre la main, sans souffler.",
        "enfant-m|Le bol, puis le jardin, plus tard.",
        "enfant-f|D'accord, je vide mon poing, dedans.",
        "maman|Le pigeon peut regarder, sans miettes collées.",
        "narrateur|Ils poussent le bol au bord, près du sel.",
        "papa|La table a un chemin, pour vos jeux.",
        "narrateur|Le clapet garde une miette, coincée dans le métal.",
    ),
    (3, 2): L(
        "narrateur|Ils vont au jardin, le bol de miettes à deux mains.",
        "enfant-f|Tout d'un coup, pour les oiseaux !",
        "narrateur|Nina jette une poignée, trop large.",
        "narrateur|Un moineau part, les ailes dures.",
        "enfant-m|Ils ont peur.",
        "maman|Une miette, puis on attend.",
        "narrateur|Amir se tait, le temps d'un souffle.",
        "enfant-m|La mienne, sous le buisson.",
        "narrateur|Nina pose la sienne, à côté, sans lancer.",
        "papa|Le buisson a deux grains, pas une tempête.",
        "narrateur|Le moineau revient, de loin, puis picore.",
        "enfant-f|On a laissé sa place, par terre.",
        "maman|La caisse sèche peut recevoir la boîte.",
        "narrateur|Une graine d'hélice se pose sur le pain restant.",
    ),
    (3, 3): L(
        "narrateur|Ils montent, des miettes dans la poche d'Amir.",
        "narrateur|Le tapis les reçoit, comme une pluie tiède.",
        "enfant-f|Je balaie, avec le doudou !",
        "narrateur|Nina pousse trop fort, les miettes filent sous le lit.",
        "enfant-m|On les voit plus.",
        "papa|À genoux, on les reprend, une par une.",
        "narrateur|Amir attend que Nina se baisse, avec lui.",
        "enfant-f|J'en ai une, sous la chaise.",
        "enfant-m|Moi, près du pied du lit.",
        "maman|La boîte les reprend, puis le clapet.",
        "narrateur|Le clic rassemble les miettes, dans le vert.",
        "papa|Le tapis est net, pour vos jeux.",
        "narrateur|Le doudou n'a plus de miette dans le poil.",
        "enfant-m|On joue, sans balayer avec lui.",
    ),
}

T3Q = {
    1: L(
        "narrateur|La table a un coin, assez sec.",
        "papa|Les cubes, le livre, ou la dînette ?",
        "maman|Vous jouez avec quoi, maintenant ?",
    ),
    2: L(
        "narrateur|La caisse est sèche, assez pour deux.",
        "maman|Les cubes, le livre, ou la dînette ?",
        "papa|Quel jeu, sur cette place ?",
    ),
    3: L(
        "narrateur|La serviette a pris l'eau de la boîte.",
        "papa|Les cubes, le livre, ou la dînette ?",
        "maman|Vous prenez quoi, sur le tissu ?",
    ),
}

T3 = {
    (1, 1, 1): L(
        "narrateur|Amir verse les cubes, trop vite, sur la table.",
        "enfant-f|Les longs, ils sont à moi !",
        "narrateur|Nina ramasse toutes les lattes, un tas.",
        "narrateur|La tour penche, touche la tasse de cacao.",
        "enfant-m|Elle va tomber !",
        "papa|Une latte pour toi, une pour elle.",
        "narrateur|Amir rend trois cubes, la gorge serrée.",
        "enfant-m|Le milieu, c'est pour la boîte.",
        "enfant-f|D'accord, j'en mets un, toi un.",
        "narrateur|Ils posent la boîte, le clapet clic.",
        "maman|Le cacao n'a pas bougé.",
        "narrateur|Une écaille verte, dans une fente du cube.",
    ),
    (1, 1, 2): L(
        "narrateur|Nina ouvre le livre des parcs, d'un coup.",
        "enfant-m|La page du platane, c'est la mienne !",
        "narrateur|Amir tourne trop vite, une goutte part.",
        "narrateur|La marge reçoit un point d'eau, sombre.",
        "enfant-f|Ma page !",
        "maman|Le torchon à carreaux, un tapotement.",
        "narrateur|Amir attend que Nina finisse de regarder.",
        "enfant-m|Après toi, je regarde l'hélice.",
        "narrateur|Le point sèche, un nuage pâle.",
        "papa|Vous avez vu la même feuille, chacun votre tour.",
        "narrateur|Une graine vraie roule du clapet, sur le dessin.",
        "enfant-f|Elle habite la page, maintenant.",
    ),
    (1, 1, 3): L(
        "narrateur|Nina prend les deux assiettes, d'un seul geste.",
        "enfant-m|Moi je sers !",
        "narrateur|Une petite tasse tombe, tinte.",
        "papa|Une assiette au milieu, pas deux tas.",
        "narrateur|Amir ramasse la tasse, les joues chaudes.",
        "enfant-f|Je verse, tu attends.",
        "enfant-m|Puis je verse, tu attends.",
        "narrateur|La boîte verte devient le four, clapet fermé.",
        "maman|Le cidre imaginaire n'a pas coulé.",
        "narrateur|Ils posent un rond de pomme, pour de faux.",
        "papa|Le bord de table est resté à Nina.",
        "narrateur|Le four-boîte garde une odeur de cacao froid.",
    ),
    (1, 2, 1): L(
        "narrateur|Amir bâtit une tour sur la pierre mouillée.",
        "narrateur|Le premier étage s'enfonce, les cubes luisent.",
        "enfant-f|La mienne, plus haute !",
        "enfant-m|Elle va glisser.",
        "papa|La caisse, elle, ne boit pas.",
        "narrateur|Ils déménagent, cube par cube, sans se bousculer.",
        "enfant-m|Large, comme le banc, pas haute.",
        "enfant-f|Et un brin d'herbe, pour la latte du milieu.",
        "narrateur|La boîte s'assoit, le clapet au soleil.",
        "maman|La pierre garde son eau, sans cubes.",
        "narrateur|Le brin d'herbe penche, puis tient.",
        "papa|Vous avez changé de sol, ensemble.",
    ),
    (1, 2, 2): L(
        "narrateur|Le livre s'ouvre sur la caisse, le vent passe.",
        "narrateur|La page du platane se lève, toute seule.",
        "enfant-m|Je la rattrape !",
        "narrateur|Amir plaque trop fort, le papier crie.",
        "enfant-f|Doucement, c'est ma page aussi.",
        "maman|Un doigt au coin, pas la paume.",
        "narrateur|Ils tiennent le coin, chacun un côté.",
        "narrateur|Une graine d'hélice tombe du clapet, sur l'image.",
        "enfant-m|On la laisse, c'est la vraie.",
        "papa|Le dessin a son invité, sans colle.",
        "narrateur|Le vent s'arrête, la page reste.",
        "enfant-f|On a lu avec le jardin.",
    ),
    (1, 2, 3): L(
        "narrateur|Nina pose la casserole dans la laitue.",
        "enfant-m|Elle va se salir !",
        "narrateur|De la terre entre, un peu noire.",
        "papa|Le robinet, un filet, pas un bain.",
        "narrateur|Amir attend que Nina apporte la casserole.",
        "enfant-f|Je rince, tu essuies.",
        "enfant-m|Puis la caisse, pas la laitue.",
        "narrateur|La boîte sert de panier, clapet ouvert.",
        "maman|La laitue n'a plus de casserole.",
        "narrateur|Ils servent un dîner de feuilles, à tour.",
        "enfant-f|Toi le cuisinier, moi l'invitée.",
        "papa|Ensuite on change, sans crier.",
    ),
    (1, 3, 1): L(
        "narrateur|Les cubes montent sur le lit, un banc de bois.",
        "enfant-f|L'oreiller, c'est la flaque, j'y saute !",
        "narrateur|Nina atterrit, les cubes s'éparpillent.",
        "enfant-m|Mon banc !",
        "maman|La serviette, elle, ne rebondit pas.",
        "narrateur|Amir ramasse, un cube, puis un autre.",
        "enfant-m|On reconstruit ici, et la flaque reste vide.",
        "enfant-f|D'accord, je marche à côté.",
        "narrateur|La boîte reprend le milieu, sur le tissu.",
        "papa|L'oreiller a gardé son creux, sans pieds.",
        "narrateur|Un cube long imite la latte sèche du parc.",
        "maman|Vous avez laissé de l'eau, pour de faux.",
    ),
    (1, 3, 2): L(
        "narrateur|Ils tirent le livre sous la couverture.",
        "enfant-m|Je le tiens !",
        "enfant-f|Moi aussi !",
        "narrateur|Deux paires de mains, la page se froisse.",
        "papa|Le livre sur la serviette, les mains autour.",
        "narrateur|Amir lâche, le temps que Nina pose.",
        "enfant-f|Je tourne, tu regardes.",
        "enfant-m|Après, je tourne.",
        "narrateur|L'empreinte de feuille, sur le tissu, les regarde.",
        "maman|Elle sèche, votre platane de chambre.",
        "narrateur|La boîte reste par terre, clapet fermé.",
        "papa|La page n'a pas de vague, cette fois.",
    ),
    (1, 3, 3): L(
        "narrateur|Nina sert le doudou, une tasse trop pleine.",
        "enfant-m|C'est long, à moi !",
        "narrateur|Il avance la main, la tasse penche.",
        "maman|Le doudou finit, puis toi.",
        "narrateur|Amir rentre les doigts, impatient, puis calme.",
        "enfant-f|Il a bu, c'est ton tour.",
        "enfant-m|Merci, doudou.",
        "narrateur|La boîte fait four, un clic comme une minuterie.",
        "papa|Le lit a un restaurant, sans tache.",
        "narrateur|Ils changent de rôle, cuisinier, puis client.",
        "enfant-f|Le bord, c'est ta table.",
        "maman|L'empreinte verte s'estompe, sur la serviette.",
    ),
    (2, 1, 1): L(
        "narrateur|Amir bâtit un mur de cubes, trop haut.",
        "enfant-m|Le couvercle ne volera plus !",
        "narrateur|Le mur tombe dans la tasse, un ploc.",
        "enfant-f|Le cacao !",
        "papa|Un quai bas, pas une tour.",
        "narrateur|Ils posent deux cubes, comme un bord de banc.",
        "enfant-f|La boîte dessus, le couvercle dans le sac.",
        "enfant-m|D'accord, plus de mur.",
        "narrateur|Le clapet s'assoit, stable, près du sel.",
        "maman|La tasse a eu chaud, puis plus.",
        "narrateur|Un cube long imite la latte du fer.",
        "papa|Le vent de la cuisine n'a rien emporté.",
    ),
    (2, 1, 2): L(
        "narrateur|Nina ouvre le livre du ciel, et parle.",
        "enfant-m|J'ai pas fini la page du vent !",
        "narrateur|Les mots se mélangent, au-dessus du papier.",
        "maman|Une phrase, puis l'autre.",
        "narrateur|Amir ferme la bouche, compte jusqu'à trois.",
        "enfant-f|J'ai fini, à toi.",
        "narrateur|Ils trouvent une flaque dessinée, ronde.",
        "papa|Le cercle de cacao, autour, fait hublot.",
        "enfant-m|On dirait le parc, tout petit.",
        "narrateur|Le couvercle reste dans le sac, sage.",
        "maman|La page n'a pas de blanc dessus.",
        "enfant-f|On a lu, chacun notre vent.",
    ),
    (2, 1, 3): L(
        "narrateur|Nina prend les deux cuillères de la dînette.",
        "enfant-m|Il m'en faut une !",
        "narrateur|Le bol minuscule tourne, vide, entre eux.",
        "papa|Une main tient, une main tourne, puis on change.",
        "narrateur|Amir pose sa cuillère, le temps du tour de Nina.",
        "enfant-f|Je tiens, tu remues.",
        "enfant-m|Stop, on change.",
        "narrateur|La boîte joue le frigo, clapet froid.",
        "maman|Le yaourt imaginaire n'a pas bavé.",
        "narrateur|Ils goûtent à tour, une cuillerée pour de faux.",
        "papa|Deux cuillères, un seul bol, comme au parc.",
        "enfant-f|Le bord de table, c'est ta chaise.",
    ),
    (2, 2, 1): L(
        "narrateur|Ils montent un pare-vent de cubes, autour de la boîte.",
        "enfant-m|Plus haut, le couvercle va sauter !",
        "narrateur|Nina pousse un cube, le mur s'ouvre.",
        "papa|Bas, serré, comme le banc.",
        "narrateur|Amir retire deux étages, déçu, puis voit.",
        "enfant-f|Une feuille du parc, en drapeau.",
        "narrateur|Ils piquent la feuille, elle claque, puis tient.",
        "enfant-m|Le sac garde le vrai couvercle.",
        "maman|Le vent du jardin tourne autour, sans entrer.",
        "narrateur|La boîte a une maison basse, verte.",
        "papa|Vous avez baissé, et ça tient.",
        "enfant-f|Ma latte, c'est ce cube-là.",
    ),
    (2, 2, 2): L(
        "narrateur|Nina glisse le couvercle dans le livre, signet blanc.",
        "enfant-m|La page va gondoler !",
        "narrateur|Le papier se plisse, une vague.",
        "maman|On le retire, une herbe à la place.",
        "narrateur|Amir pince le blanc, sans déchirer.",
        "enfant-f|Pardon, je le rends au sac.",
        "narrateur|Un brin d'herbe marque la page du jardin.",
        "papa|Le livre reste plat, le sac a son chapeau.",
        "narrateur|Ils lisent la page de la flaque, à deux voix.",
        "enfant-m|Toi une ligne, moi une ligne.",
        "maman|Le vent n'a pas tourné le papier.",
        "narrateur|La feuille-bateau de Nina sèche, sur la caisse.",
    ),
    (2, 2, 3): L(
        "narrateur|Nina veut le couvercle comme poêle, au soleil.",
        "enfant-m|Il va voler, vers l'arrosoir !",
        "narrateur|Un souffle le soulève, presque.",
        "papa|Une feuille, ça, ça reste.",
        "narrateur|Amir pose le couvercle dans le sac, d'abord.",
        "enfant-f|Ma poêle, c'est la feuille, alors.",
        "narrateur|Ils font cuire de l'eau de pluie, pour de faux.",
        "maman|L'arrosoir n'a rien attrapé de blanc.",
        "enfant-m|Je sers, tu goûtes.",
        "enfant-f|Puis toi.",
        "narrateur|La boîte est le fourneau, clapet tiède.",
        "papa|Deux cuisiniers, une seule poêle de feuille.",
    ),
    (2, 3, 1): L(
        "narrateur|Les cubes font une boîte, sur le tapis.",
        "enfant-f|J'ouvre le couvercle, comme au parc !",
        "narrateur|Nina soulève trop vite, la tour s'envole.",
        "enfant-m|Tout par terre.",
        "maman|On ouvre un cube, pas dix.",
        "narrateur|Amir pose un seul cube de côté, lentement.",
        "enfant-f|Clic, comme le vrai.",
        "narrateur|Le vrai clapet répond, dans la chambre.",
        "papa|Deux boîtes, un même geste.",
        "enfant-m|Toi tu ouvres, moi je ferme.",
        "narrateur|Ils s'entraînent, sans tout étaler.",
        "maman|Le tapis n'a plus de cubes sous le lit.",
    ),
    (2, 3, 2): L(
        "narrateur|Nina pose le couvercle sur le livre, bateau plat.",
        "enfant-m|L'encre, elle aime pas le blanc.",
        "narrateur|Une page menace de coller.",
        "papa|Le bateau, sur la vitre, au doigt.",
        "narrateur|Amir souffle sur le verre, un nuage.",
        "enfant-f|Je dessine la flaque, toi le banc.",
        "narrateur|Deux traces de doigt, puis ils regardent.",
        "maman|Le livre reste fermé, propre.",
        "enfant-m|Le couvercle, au sac.",
        "narrateur|Le nuage de la vitre s'en va, lent.",
        "papa|Votre parc tient, le temps d'un souffle.",
        "enfant-f|On a laissé de la place au bateau.",
    ),
    (2, 3, 3): L(
        "narrateur|Nina ouvre trop vite le pot, une goutte.",
        "enfant-m|Le tapis !",
        "narrateur|Amir plaque le torchon, juste à temps.",
        "maman|On sert avec deux cuillères, un bol.",
        "enfant-f|Le doudou d'abord, une goutte pour de faux.",
        "narrateur|Amir attend la fin du service.",
        "enfant-m|Mon tour, une cuillerée.",
        "papa|Le vrai pot reste sur la chaise, fermé.",
        "narrateur|La dînette fait le goûter, sans deuxième tache.",
        "enfant-f|Toi le cuisinier, moi la cliente.",
        "maman|Le drap bleu n'a pas d'île.",
        "narrateur|Le clapet, sur la chaise, fait un petit clic.",
    ),
    (3, 1, 1): L(
        "narrateur|Amir aligne des cubes, un chemin de miettes.",
        "enfant-f|Je casse le chemin, pour le pigeon !",
        "narrateur|Les cubes roulent, les miettes s'éparpillent.",
        "enfant-m|On les ramasse, d'abord.",
        "papa|Le bol, au bout, pas la vitre.",
        "narrateur|Ils pincent, une miette, un cube remis.",
        "enfant-m|Un chemin court, qui s'arrête au bol.",
        "enfant-f|D'accord, le pigeon regardera le bol.",
        "narrateur|La boîte garde le surplus, clapet coincé d'une miette.",
        "maman|La table a un sentier, pas une tempête.",
        "narrateur|Le pigeon penche, puis s'en va.",
        "papa|Vous avez arrêté le chemin, pile au bord.",
    ),
    (3, 1, 2): L(
        "narrateur|Nina souffle une miette hors du livre de recettes.",
        "enfant-m|Elle va dans le cacao !",
        "narrateur|La miette vise la tasse, puis s'arrête au rebord.",
        "maman|On la pince, vers l'assiette.",
        "narrateur|Amir attend que Nina souffle plus, puis non.",
        "enfant-f|Je pince, tu tiens l'assiette.",
        "narrateur|La page du pain s'ouvre, propre.",
        "papa|Vous lisez après le pincement.",
        "enfant-m|Une image pour toi, une pour moi.",
        "narrateur|Le clapet a gardé une miette, comme un trésor.",
        "maman|Le cacao n'a pas de croûte.",
        "enfant-f|Le livre sent le pain, un peu.",
    ),
    (3, 1, 3): L(
        "narrateur|Nina prend tout le pain de la dînette.",
        "enfant-m|Je voulais couper !",
        "narrateur|Le pain-jouet se casse, trop sec.",
        "papa|On dit bonjour aux clients, puis on coupe.",
        "narrateur|Amir ferme la bouche, le temps du bonjour.",
        "enfant-f|Bonjour, une tranche.",
        "enfant-m|Bonjour, une tranche.",
        "narrateur|Une vraie croûte, toute petite, sur l'assiette.",
        "maman|Le four, c'est la boîte, clic.",
        "narrateur|Ils vendent à tour, sans se prendre le pain.",
        "papa|Deux vendeurs, une seule boutique.",
        "enfant-f|Le pigeon de la vitre est le client.",
    ),
    (3, 2, 1): L(
        "narrateur|Ils bâtissent une table d'oiseaux, en cubes.",
        "enfant-f|Toutes les miettes, d'un coup !",
        "narrateur|Rien ne vient, le buisson reste vide.",
        "enfant-m|Une miette, un cube pour perchoir.",
        "maman|On attend, sans jeter.",
        "narrateur|Nina pose sa miette, puis recule.",
        "narrateur|Amir pose la sienne, plus loin.",
        "papa|Deux places, pas un tas.",
        "narrateur|Le moineau revient, picore la plus proche.",
        "enfant-f|Il a choisi, sans qu'on crie.",
        "narrateur|La boîte sèche sur la caisse, clapet au soleil.",
        "maman|La table d'oiseaux a de l'air, autour.",
    ),
    (3, 2, 2): L(
        "narrateur|Nina claque le livre, une miette marqueur saute.",
        "enfant-m|Elle est dans l'herbe !",
        "narrateur|Ils cherchent, à quatre pattes, près de la caisse.",
        "papa|Là, contre le pied.",
        "narrateur|Amir la pince, la pose sur la terre.",
        "enfant-f|Un pétale, pour la page, à la place.",
        "narrateur|Le livre s'ouvre, sans claquer.",
        "maman|Une page, puis on tourne.",
        "enfant-m|Je finis celle-ci, après toi.",
        "narrateur|La miette rejoint le buisson, comme au platane.",
        "papa|Le pétale tient, léger, sans gondoler.",
        "enfant-f|On a lu, et le jardin a son grain.",
    ),
    (3, 2, 3): L(
        "narrateur|Nina pose l'assiette sur la pierre, trop mouillée.",
        "enfant-m|Le pain-jouet glisse !",
        "narrateur|Amir le rattrape, juste avant l'eau.",
        "maman|La caisse, elle, est sèche.",
        "narrateur|Ils déménagent le café, assiette, puis pots.",
        "enfant-f|Deux chaises, deux pots retournés.",
        "enfant-m|Je cuisine, tu t'assois.",
        "papa|Puis on change, sans prendre l'assiette.",
        "narrateur|La boîte fait comptoir, clapet comme une caisse.",
        "maman|La pierre garde son eau, sans vaisselle.",
        "narrateur|Ils servent une feuille, puis un caillou, à tour.",
        "enfant-f|Le moineau est le client du bout.",
    ),
    (3, 3, 1): L(
        "narrateur|Les cubes font une boulangerie, sur le tapis.",
        "narrateur|Des miettes de poche tombent, entre les murs.",
        "enfant-f|Le doudou balaye !",
        "narrateur|Nina pousse, les miettes filent sous le lit.",
        "enfant-m|On les reprend, dans la boîte.",
        "papa|Le doudou garde ses pattes, cette fois.",
        "narrateur|Ils ramassent, à deux, cube par cube dégagé.",
        "enfant-f|Clapet, tu fermes.",
        "enfant-m|Clic.",
        "maman|La boulangerie peut ouvrir, tapis net.",
        "narrateur|Un cube long est le comptoir, partagé.",
        "papa|Chacun un côté, le pain-jouet au milieu.",
    ),
    (3, 3, 2): L(
        "narrateur|Une miette dort dans le dos du livre.",
        "enfant-f|On reste sur cette page, toujours !",
        "enfant-m|Moi je veux la suivante.",
        "narrateur|Nina plaque la page, Amir tire, le papier râpe.",
        "maman|On finit celle-ci, ensuite on tourne.",
        "narrateur|Amir lâche, le temps de la fin.",
        "enfant-f|Voilà, tu peux.",
        "papa|La miette, dans la boîte, pas dans le dos.",
        "narrateur|Ils la glissent, le clapet clic.",
        "enfant-m|La page d'après, c'est un banc.",
        "maman|Vous l'avez tournée, sans la déchirer.",
        "narrateur|Le doudou écoute, contre l'oreiller, sans parler.",
    ),
    (3, 3, 3): L(
        "narrateur|Nina remplit la tasse de miettes, trop.",
        "enfant-m|C'est un pain, pas un tas !",
        "narrateur|Les miettes débordent, sur le tapis.",
        "papa|Le surplus, dans la boîte, un grain pour le pain.",
        "narrateur|Amir attend que Nina verse, puis l'aide.",
        "enfant-f|Un grain, on le vend.",
        "enfant-m|Moi le vendeur, toi la cliente.",
        "maman|Ensuite on change, sans tout vider.",
        "narrateur|Le clapet ferme le stock, un clic de boutique.",
        "enfant-f|Le doudou achète le grain, pour de faux.",
        "papa|Le tapis n'a plus de neige de pain.",
        "narrateur|Ils ferment la boutique, tasse vide, au milieu.",
    ),
}

FINS = {
    (1, 1, 1): L(
        "narrateur|Le cube du milieu porte une écaille verte.",
        "enfant-m|C'est le banc, en tout petit.",
        "enfant-f|Le cercle d'eau, c'est notre flaque.",
        "papa|Vous avez laissé la latte du centre.",
        "maman|Le cacao n'a pas voyagé.",
        "narrateur|Le clapet fait un dernier clic, très bas.",
        "narrateur|Amir pose un doigt dessus, puis l'ôte.",
        "narrateur|Dehors, une graine d'hélice n'a plus de vent.",
    ),
    (1, 1, 2): L(
        "narrateur|Le torchon à carreaux garde un point sombre.",
        "enfant-f|La page du platane est sèche.",
        "enfant-m|La graine habite le dessin.",
        "papa|Vous avez regardé, l'un après l'autre.",
        "maman|La marge a un nuage, minuscule.",
        "narrateur|La boîte verte sent le papier, et la pomme.",
        "narrateur|Le clapet se ferme, sans goutte.",
        "narrateur|La tasse de cacao ne fume plus, ronde.",
    ),
    (1, 1, 3): L(
        "narrateur|La petite assiette a un croissant de pomme.",
        "enfant-m|Le four est vert, et fermé.",
        "enfant-f|J'ai le bord de table, pour moi.",
        "papa|Le cidre imaginaire a tenu.",
        "maman|Deux serveurs, une seule assiette.",
        "narrateur|Le clapet a froid, comme le fer du parc.",
        "narrateur|Une odeur de cacao reste sur le métal.",
        "narrateur|La latte du milieu, sur la table, est vide.",
    ),
    (1, 2, 1): L(
        "narrateur|Le brin d'herbe tient, latte du milieu.",
        "enfant-f|La caisse, c'est notre banc sec.",
        "enfant-m|La pierre, on l'a laissée à l'eau.",
        "papa|Vous avez changé de sol, sans casser.",
        "maman|Le trognon a sa terre, sous la laitue.",
        "narrateur|Le clapet luit, une poussière de jardin.",
        "narrateur|Une graine d'hélice reste collée à l'osier.",
        "narrateur|Le fer du parc, loin, n'a plus de fesses mouillées.",
    ),
    (1, 2, 2): L(
        "narrateur|La graine vraie dort sur le platane dessiné.",
        "enfant-m|On a lu avec le vent.",
        "enfant-f|Sans coller, sans crier.",
        "papa|Un doigt au coin, chacun.",
        "maman|La page n'a pas crié, cette fois.",
        "narrateur|La boîte sent l'herbe, et la pomme.",
        "narrateur|Le clapet cligne, un insecte passe.",
        "narrateur|La caisse garde un rond d'ombre, comme une flaque.",
    ),
    (1, 2, 3): L(
        "narrateur|La casserole sèche, sans terre, sur la caisse.",
        "enfant-f|J'ai rincé, tu as essuyé.",
        "enfant-m|Puis on a changé de cuisinier.",
        "papa|La laitue n'a plus d'invité en métal.",
        "maman|Le panier-boîte sent la feuille.",
        "narrateur|Une écaille verte, dans le fond, comme un bateau.",
        "narrateur|Le clapet s'ouvre, un peu de soleil entre.",
        "narrateur|Le robinet a fini son filet, goutte, silence.",
    ),
    (1, 3, 1): L(
        "narrateur|Un cube long imite la latte sèche, sur la serviette.",
        "enfant-m|L'oreiller-flaque, on n'y marche pas.",
        "enfant-f|J'ai sauté à côté, pas dessus.",
        "papa|Le banc de chambre a tenu.",
        "maman|Le creux de l'oreiller est resté rond.",
        "narrateur|La boîte a un rond d'eau, sur l'éponge, pâle.",
        "narrateur|Le clapet clic, étouffé par le tissu.",
        "narrateur|Le doudou garde le bas du lit, sans bouger.",
    ),
    (1, 3, 2): L(
        "narrateur|L'empreinte de feuille sèche, platane de chambre.",
        "enfant-f|J'ai tourné, tu as regardé.",
        "enfant-m|Après, c'était mon tour.",
        "papa|Le livre n'a pas de vague.",
        "maman|La serviette a pris l'eau, pas la page.",
        "narrateur|La boîte, par terre, a un clapet froid.",
        "narrateur|Une odeur de pomme monte, puis s'en va.",
        "narrateur|La couverture redescend, sans cacher le dessin.",
    ),
    (1, 3, 3): L(
        "narrateur|L'empreinte verte s'estompe, sur la serviette.",
        "enfant-m|Le doudou a bu, puis moi.",
        "enfant-f|Le clic du four, c'était le clapet.",
        "papa|Le restaurant du lit n'a pas taché.",
        "maman|Vous avez changé de rôle, sans prendre la tasse.",
        "narrateur|La boîte garde un souffle de cacao, très loin.",
        "narrateur|Le métal est froid, souvenir du banc.",
        "narrateur|Nina laisse le bord, Amir le milieu, et ça tient.",
    ),
    (2, 1, 1): L(
        "narrateur|Le quai de cubes tient, bas, près du sel.",
        "enfant-m|Plus de mur dans la tasse.",
        "enfant-f|Le couvercle, lui, dort dans le sac.",
        "papa|Le vent de la cuisine n'a rien pris.",
        "maman|Le cacao a fait ploc, puis s'est tu.",
        "narrateur|Le clapet a une tache brune, minuscule.",
        "narrateur|Amir la frotte, elle pâlit.",
        "narrateur|Un cube long luit, latte de fer imaginaire.",
    ),
    (2, 1, 2): L(
        "narrateur|Le hublot de cacao encadre la flaque dessinée.",
        "enfant-f|On dirait le parc, dans la tasse.",
        "enfant-m|J'ai compté jusqu'à trois, avant de parler.",
        "papa|Une phrase, puis l'autre.",
        "maman|La page n'a pas de blanc.",
        "narrateur|Le couvercle reste au sac, plat, sage.",
        "narrateur|La boîte verte sent le cacao froid.",
        "narrateur|Le clapet clic, comme un nuage qui se ferme.",
    ),
    (2, 1, 3): L(
        "narrateur|Deux cuillères reposent dans le même bol.",
        "enfant-m|J'ai tenu, tu as tourné.",
        "enfant-f|Puis on a changé.",
        "papa|Un bol, comme une seule tasse au parc.",
        "maman|Rien n'a bavé, sur le bois.",
        "narrateur|Le frigo-boîte a le clapet froid, fermé.",
        "narrateur|Une lueur de yaourt reste au fond, nacre.",
        "narrateur|Le bord de table, chaise de Nina, reste libre.",
    ),
    (2, 2, 1): L(
        "narrateur|La feuille-drapeau claque une dernière fois, puis pend.",
        "enfant-f|Le mur bas a tenu.",
        "enfant-m|Le vrai couvercle, au sac.",
        "papa|Vous avez baissé, et le vent tourne dehors.",
        "maman|La boîte a une maison, verte, petite.",
        "narrateur|Une écaille du parc, collée au cube du bas.",
        "narrateur|Le clapet luit, une goutte de jardin.",
        "narrateur|L'arrosoir, plus loin, n'a rien attrapé.",
    ),
    (2, 2, 2): L(
        "narrateur|Le brin d'herbe marque la page, plat, vivant.",
        "enfant-m|Le blanc n'a pas gondolé le livre.",
        "enfant-f|Ma feuille-bateau sèche, sur la caisse.",
        "papa|Une ligne pour toi, une pour elle.",
        "maman|Le sac a son chapeau, enfin.",
        "narrateur|Le clapet sent l'herbe coupée, un peu.",
        "narrateur|Une graine d'hélice se pose sur le brin, puis part.",
        "narrateur|Le jardin s'est tu, autour de la caisse.",
    ),
    (2, 2, 3): L(
        "narrateur|La poêle de feuille a une perle d'eau, au centre.",
        "enfant-f|On a cuit la pluie, pour de faux.",
        "enfant-m|Le couvercle n'a pas volé.",
        "papa|Deux cuisiniers, une seule feuille.",
        "maman|L'arrosoir est resté vide de blanc.",
        "narrateur|Le fourneau-boîte a le clapet tiède.",
        "narrateur|Une odeur de yaourt, et de haie, s'en va.",
        "narrateur|Le soleil sur le métal fait un petit clic de chaleur.",
    ),
    (2, 3, 1): L(
        "narrateur|Deux boîtes se taisent, la vraie et celle de cubes.",
        "enfant-f|Clic, j'ouvre un cube.",
        "enfant-m|Clic, je ferme le clapet.",
        "papa|Le même geste, sans tout étaler.",
        "maman|Le tapis n'a plus de tour sous le lit.",
        "narrateur|Le métal répond au bois, un écho court.",
        "narrateur|Une goutte de yaourt, sur la chaise, sèche.",
        "narrateur|Le doudou a regardé, sans ouvrir.",
    ),
    (2, 3, 2): L(
        "narrateur|Le nuage de la vitre s'efface, banc et flaque avec.",
        "enfant-m|On a dessiné le parc, le temps d'un souffle.",
        "enfant-f|Le livre, lui, est resté propre.",
        "papa|Le bateau de doigt a eu sa place.",
        "maman|Le couvercle a rejoint le sac.",
        "narrateur|La boîte verte sent le verre froid.",
        "narrateur|Le clapet clic, comme un volet.",
        "narrateur|Le drap bleu n'a plus peur du blanc.",
    ),
    (2, 3, 3): L(
        "narrateur|Le torchon a une lune blanche, toute petite.",
        "enfant-f|Le doudou a goûté, pour de faux.",
        "enfant-m|Puis moi, une cuillerée.",
        "papa|Le vrai pot n'a pas quitté la chaise.",
        "maman|Le drap est bleu, sans île.",
        "narrateur|Le clapet, sur le bois, fait un clic de bonne nuit.",
        "narrateur|Une odeur de yaourt reste, puis s'en va.",
        "narrateur|Nina pose sa cuillère, Amir la sienne, côte à côte.",
    ),
    (3, 1, 1): L(
        "narrateur|Le sentier de cubes s'arrête pile au bol.",
        "enfant-m|Le pigeon a regardé, sans miettes collées.",
        "enfant-f|On a ramassé, avant de jouer.",
        "papa|Un chemin court, pas une tempête.",
        "maman|La table a retrouvé son bois.",
        "narrateur|Le clapet garde une miette, coincée, trésor.",
        "narrateur|Amir la pousse du doigt, elle tombe dans le vert.",
        "narrateur|La vitre n'a plus de pigeon, seulement le ciel.",
    ),
    (3, 1, 2): L(
        "narrateur|La page du pain sent une croûte lointaine.",
        "enfant-f|On a pincé la miette, vers l'assiette.",
        "enfant-m|Le cacao n'a rien reçu.",
        "papa|Vous avez lu après le pincement.",
        "maman|Une image chacun, même livre.",
        "narrateur|Le clapet cache sa miette, comme un secret.",
        "narrateur|La tasse ne fume plus, ronde et brune.",
        "narrateur|Le livre se ferme, un souffle de cuisine.",
    ),
    (3, 1, 3): L(
        "narrateur|La vraie croûte sèche sur l'assiette minuscule.",
        "enfant-m|Bonjour, une tranche.",
        "enfant-f|Bonjour, une tranche.",
        "papa|Deux vendeurs, une boutique.",
        "maman|Le four-boîte s'est tu, après le clic.",
        "narrateur|Le pigeon-client a quitté la vitre.",
        "narrateur|Une miette reste au métal, dorée.",
        "narrateur|Le sel de la table n'a pas bougé.",
    ),
    (3, 2, 1): L(
        "narrateur|Le moineau picore la miette la plus proche, puis part.",
        "enfant-f|On a laissé de l'air, autour.",
        "enfant-m|Une miette, un perchoir, pas un tas.",
        "papa|Deux places, par terre.",
        "maman|La boîte sèche, clapet au soleil.",
        "narrateur|Une graine d'hélice tourne, s'assoit sur le vert.",
        "narrateur|Le buisson a deux grains, puis plus.",
        "narrateur|La caisse garde une ombre de banc, étroite.",
    ),
    (3, 2, 2): L(
        "narrateur|Le pétale tient dans le livre, signet vivant.",
        "enfant-m|La miette a rejoint la terre.",
        "enfant-f|Comme sous le platane.",
        "papa|Vous avez cherché, à quatre pattes.",
        "maman|La page n'a pas claqué, la deuxième fois.",
        "narrateur|Le clapet sent le pétale, un peu sucré.",
        "narrateur|Une terre sèche au coin de la boîte, fine.",
        "narrateur|Le jardin s'est assis, autour de la caisse.",
    ),
    (3, 2, 3): L(
        "narrateur|L'assiette sèche sur la caisse, plus de glissade.",
        "enfant-f|Le pain-jouet n'est pas tombé dans l'eau.",
        "enfant-m|Deux pots, deux chaises, un comptoir vert.",
        "papa|La pierre a gardé son eau, sans vaisselle.",
        "maman|Vous avez changé de cuisinier, sans prendre l'assiette.",
        "narrateur|Le clapet fait caisse enregistreuse, un clic.",
        "narrateur|Le moineau, client du bout, n'est plus là.",
        "narrateur|Une écaille de peinture, dans l'herbe, minuscule bateau.",
    ),
    (3, 3, 1): L(
        "narrateur|Le comptoir-cube a deux côtés, un pain au milieu.",
        "enfant-m|Clic, le stock est fermé.",
        "enfant-f|Le doudou n'a pas balayé, cette fois.",
        "papa|La boulangerie du tapis peut dormir.",
        "maman|Plus de miettes sous le lit.",
        "narrateur|La boîte pèse, pleine de grains, contre le pied.",
        "narrateur|Le clapet a un bruit sourd, de pain.",
        "narrateur|L'oreiller, plus loin, garde son creux de flaque.",
    ),
    (3, 3, 2): L(
        "narrateur|La page du banc reste ouverte, un souffle.",
        "enfant-f|On a fini la mienne, puis la tienne.",
        "enfant-m|La miette n'est plus dans le dos.",
        "papa|Le papier n'a pas râpé, la deuxième fois.",
        "maman|Le clapet a reçu le grain.",
        "narrateur|Le doudou écoute, contre l'oreiller, silencieux.",
        "narrateur|La boîte sent le livre, et le pain tiède.",
        "narrateur|Une ombre de platane, sur le mur, s'allonge, puis s'arrête.",
    ),
    (3, 3, 3): L(
        "narrateur|La tasse vide trône au milieu, boutique fermée.",
        "enfant-m|Un grain vendu, le reste au stock.",
        "enfant-f|Le doudou a payé, pour de faux.",
        "papa|Le tapis n'a plus de neige de pain.",
        "maman|Vous avez versé, puis aidé, puis changé.",
        "narrateur|Le clapet clic, un volet de nuit.",
        "narrateur|Une miette dorée brille au fond, puis plus.",
        "narrateur|Le fer du parc, très loin, sèche sans eux.",
    ),
}

SONS = {
    "CHK_T0000_P0000": "parc,flaque,clapet",
    "CHK_T0001_P0001": "pomme,clapet",
    "CHK_T0001_P0002": "couvercle,vent",
    "CHK_T0001_P0003": "pain,pigeon",
}
SONS_T2 = {1: "cacao,table", 2: "caisse,jardin", 3: "tissu,chambre"}
SONS_T3 = {1: "cubes,bois", 2: "page,livre", 3: "vaisselle"}
SONS_FIN = {1: "clapet,silence", 2: "platane,page", 3: "fer,tissu"}

QMETA = {
    1: qf(
        "sac",
        "sac | le sac | dans le sac | pelure",
        "La pelure. Amir l'a mise où ?",
        "Oui, dans le sac.",
    ),
    2: qf(
        "sac",
        "sac | le sac | dans le sac | couvercle",
        "Le couvercle. Amir l'a mis où ?",
        "Oui, dans le sac.",
    ),
    3: qf(
        "terre",
        "terre | la terre | sous l'arbre | sous le platane | oiseau",
        "La terre, sous l'arbre. Amir l'a mise où ?",
        "Oui, sur la terre.",
    ),
}

EMPH = {
    "CHK_T0000_P0000": "clapet",
    "CHK_T0001_P0001": "pelure",
    "CHK_T0001_P0002": "couvercle",
    "CHK_T0001_P0003": "miette",
}


def build() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {
        "CHK_T0000_P0000": DEBUT,
        "CHK_T0001_P0000": T1Q,
    }
    sons: dict[str, str] = dict(SONS)
    extras: dict[str, dict] = {
        "CHK_T0001_P0000": t3("une pomme", "un yaourt", "un morceau de pain"),
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = T1[i]
        s[f"{p}_Q0001"] = Q1[i]
        extras[f"{p}_Q0001"] = QMETA[i]
        s[f"{p}_C0001"] = C1[i]
        s[f"{p}_T0002_P0000"] = T2Q[i]
        extras[f"{p}_T0002_P0000"] = t3("la cuisine", "le jardin", "la chambre")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = T2[(i, j)]
            sons[p2] = SONS_T2[j]
            s[f"{p2}_T0003_P0000"] = T3Q[j]
            extras[f"{p2}_T0003_P0000"] = t3("les cubes", "le livre", "la dînette")
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
    out["characters"] = "Amir, Nina, papa, maman"
    out["setting"] = "parc, coin des écailles, banc de fer, platane, flaque, boîte verte à clapet, puis la maison"
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
        "merle",
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
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
        if not c.get("text_xai_tags") or not c.get("notes"):
            raise SystemExit(f"{SID} TTS manquant: {c['chunk_id']}")
    lo, hi, avg = path_words(scripts)
    print(f"chemins {lo}–{hi} mots (moyenne {avg:.0f})")
    if lo < 520 or hi > 760:
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
        "(pomme / yaourt / pain ; cuisine / jardin / chambre ; "
        "cubes / livre / dînette).\n\n"
        "## Promesse narrative\n\n"
        "Au coin des écailles, après la pluie, le banc de fer luit sous le "
        "platane. Amir veut poser sa boîte verte à clapet sur une latte sèche, "
        "pour partager le goûter avec Nina avant que le soleil mange la flaque. "
        "Il pose trop vite : le fer glisse, Nina parle en même temps. Papa "
        "essuie une seule latte. Pelure au sac, couvercle au sac, ou miette "
        "à la terre. Cuisine (cercle d'eau, couteau, cacao), jardin (terre, "
        "vent, oiseaux) ou chambre (empreinte, drap, doudou) changent le "
        "second imprévu. Cubes, livre ou dînette changent le dernier geste. "
        "Le clapet, l'écaille et la graine-hélice paient la fin.\n\n"
        "## Vécu\n\n"
        f"- Désir : poser la boîte verte, partager le goûter, maintenant.\n"
        "- Imprévu 1 : fer glissant, deux enfants la même latte, boîte vers la flaque.\n"
        "- Imprévu 2 : pelure / couvercle / miette, puis cercle d'eau, vent, "
        "terre, empreinte, miettes de poche.\n"
        "- COL.ECO.001 vécu (partage / tour / soin) : une latte chacun, reste "
        "au sac ou à la terre, pas sur le banc, attendre la phrase de l'autre. "
        "Jamais dite.\n"
        "- Nuance par chemin : offrir un morceau après la bouchée ; laisser "
        "le couvercle au sac, bateau de feuille à Nina ; miette à la terre "
        "et pain partagé ; table, caisse ou lit comme banc à soigner.\n"
        f"- 27 fins distinctes. Chemins {lo}–{hi} mots (moyenne {avg:.0f}).\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Troupe D16 : Amir, Nina, papa, maman.\n"
        "- 86 nœuds, graphe et libellés d'options conservés.\n"
        "- 27 fins, 27 T3, 9 T2 textuellement distincts.\n"
        "- Première tentative échoue. Chaque choix change l'obstacle, le climax, la dernière image.\n"
        "- Objet nommé : boîte verte à clapet (couleur, poids, clic, mission).\n"
        "- Coin inventif : le coin des écailles (banc de fer, peinture qui part).\n"
        "- Monde ≠ TREE-COL-023 (jardin, pommier, pomme de Mila, banc de bois).\n"
        "- Détail unique : graine-hélice du platane, écaille-bateau, fer froid, torchon à carreaux.\n"
        "- TTS par fonction (ouverture, choix, indice, confirmation, action, obstacle, résolution, retour).\n"
        "- `slow` réservé aux choix, à l'indice et aux fins.\n"
        "- N2 ≤ 15 mots/phrase. Pas de leçon dite. Pas de tics « tout doux / encore / déjà / tout calme ».\n"
        "- Pas de refrains example3. Pas de merle / miel. Pas apply. Pas audio.\n\n"
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
