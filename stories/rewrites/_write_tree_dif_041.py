#!/usr/bin/env python3
"""TREE-DIF-041 — Le pain tiède d'Amir, jusqu'à la mer (F-NAR-019, N1, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "TREE-DIF-041"
LIM = LIMITS["N1"]
TITLE = "Le pain tiède d'Amir, jusqu'à la mer"
FIL = (
    "Amir veut montrer la mer à Nina, depuis le wagon. "
    "Il s'installe à la vitre, à la tablette ou près de la porte. "
    "Il l'appelle trop vite : le siège reste vide. "
    "Nina dessine une vache, croque sa pomme, ou attend le sifflet. "
    "Il propose, ça rate. Puis il attend, parle bas, dessine à côté ; "
    "attend la pomme, propose le pain, ou garde le sien ; "
    "écoute, joue un peu, ou plus tard. Le pain tiède, puis le sel."
)
CHARS = "Amir, Nina, papa, maman"
SETTING = "gare du village, wagon : vitre, tablette, porte"

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=500, sentence=260, energy="warm", contour="storytelling",
        noise=0.36, emphasis="pain tiède",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=la mer est promise, Nina manque; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=900, sentence=330, energy="focused", contour="rising",
        noise=0.33, emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change la suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2,
        pause=700, sentence=320, energy="focused", contour="rising",
        noise=0.32, emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qui_vient_d_arriver; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=450, sentence=280, energy="bright", contour="falling",
        noise=0.34, emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=Nina_est_plus_loin; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=420, sentence=250, energy="lively", contour="dynamic",
        noise=0.37, emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=il_appelle_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0,
        pause=520, sentence=300, energy="tense", contour="dynamic",
        noise=0.34, emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement; intensite=2; destinataire=enfant; sous_texte=Nina_a_son_rythme; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=560, sentence=270, energy="bright", contour="falling",
        noise=0.35, emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=proposer_sans_tirer; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3,
        pause=900, sentence=340, energy="calm", contour="falling",
        noise=0.31, emphasis="pain tiède",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_pain_tiède_et_le_sel_paient_le_début; tempo=posé; sourire=léger; respiration=ample",
    ),
}

TICS = (
    "tout doux",
    "tout calme",
    "on va apprendre",
    "voici le geste",
    "l'histoire est finie",
    "inviter sans forcer",
    "accepter plusieurs",
    "bon travail",
    "bravo tu as",
    "la première",
    "la deuxième",
    "la troisième",
)


def L(*rows: str) -> list[str]:
    out: list[str] = []
    prev = ""
    run = 1
    for raw in rows:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > LIM:
            raise SystemExit(f"{n}>{LIM}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        low = ph.lower()
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"tic « {tic} »: {ph}")
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


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emph = m.get("emphasis")
    if emph:
        e = esc(emph)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict) -> str:
    body = text
    emph = m.get("emphasis")
    if emph:
        body = body.replace(emph, f"<emphasis>{emph}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitch_tag"):
        body = f"<{m['pitch_tag']}>{body}</{m['pitch_tag']}>"
    tail = " [long-pause]" if m["pause"] >= 800 else (" [pause]" if m["pause"] >= 400 else "")
    return (body + tail).strip()


def voice(text: str, profile: str, extra: dict | None = None) -> dict:
    m = dict(PROFILES[profile])
    extra = extra or {}
    if extra.get("emphasis") is not None:
        m["emphasis"] = extra["emphasis"]
    if extra.get("note"):
        m["note"] = extra["note"]
    pause_before = extra.get("pause_before", 0)
    return {
        "text_ssml": ssml(text, m),
        "text_xai_tags": xai(text, m),
        "rate_wpm": m["wpm"],
        "rate_label": m["rate"],
        "speed_xai": m["speed"],
        "length_scale_piper": m["piper"],
        "pitch_label": m["pitch"],
        "pitch_ssml": m["pitch_ssml"],
        "pitch_xai_tag": m["pitch_tag"],
        "volume_label": m["volume"],
        "volume_db": m["db"],
        "emphasis_words": m["emphasis"] or "",
        "pause_before_ms": pause_before,
        "pause_after_ms": m["pause"],
        "pause_sentence_ms": m["sentence"],
        "style_energy": m["energy"],
        "style_contour": m["contour"],
        "noise_scale_piper": m["noise"],
        "kokoro_speed": m["speed"],
        "melo_speed": m["speed"],
        "espeak_amp": 82 if m["volume"] == "soft" else 100,
        "espeak_pitch": 42 if m["pitch"] == "low" else 50,
        "espeak_word_gap": 12 if m["rate"] == "slow" else 8,
        "notes": m["note"],
        "night_policy": "play",
        "locale": "fr-FR",
        "voice_id": "fr_FR-siwis-medium",
    }


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


T1 = {
    1: {
        "lab": "la vitre",
        "ans": "champs",
        "acc": "champs | les champs | dehors | les arbres | un arbre",
        "retry": "Il regarde les champs.",
        "emph": "champs",
        "sons": "rails,vitre",
    },
    2: {
        "lab": "la tablette",
        "ans": "tablette",
        "acc": "tablette | la tablette | le bois | le pain",
        "retry": "Il a déplié la tablette.",
        "emph": "pain",
        "sons": "papier,pain",
    },
    3: {
        "lab": "la porte",
        "ans": "porte",
        "acc": "porte | la porte | près de la porte | la barre",
        "retry": "Il se tient près de la porte.",
        "emph": "barre",
        "sons": "vent,sifflet",
    },
}

T3_LABS = {
    1: ("attendre un peu", "parler tout bas", "dessiner à côté"),
    2: ("attendre la fin", "proposer le pain", "garder le sien"),
    3: ("écouter ensemble", "un tout petit jeu", "proposer plus tard"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Amir se colle à la vitre froide.",
            "enfant-m|Les champs courent, trop vite.",
            "maman|Pose ton sac, près de toi.",
            "narrateur|Un arbre passe, puis un toit rouge.",
            "papa|Tu vois la mer, Amir ?",
            "enfant-m|Pas la mer.",
            "enfant-m|Pas Nina non plus.",
            "narrateur|Le clic des rails rentre dans le ventre.",
            "enfant-m|Nina, viens voir les champs !",
            "narrateur|Le siège à côté reste vide.",
            "narrateur|Ses joues chauffent, un peu.",
            "papa|Tu l'invites, quand tu la trouves ?",
            "enfant-m|Oui, papa.",
            "narrateur|Amir pince le papier du pain.",
        )
    if t1 == 2:
        return L(
            "narrateur|Amir déplie la tablette, d'un coup.",
            "enfant-m|Elle fait un petit toc.",
            "papa|Tiens-la bien.",
            "narrateur|Elle tremble un peu.",
            "narrateur|Le pain tiède pose son papier.",
            "maman|Les miettes vont dans le sac.",
            "narrateur|Le bois sent le savon, presque.",
            "enfant-m|Nina, le pain t'attend !",
            "narrateur|Personne ne s'assoit en face.",
            "enfant-m|Il va refroidir.",
            "narrateur|Amir serre le pain trop fort.",
            "maman|Tu lui proposes, sans crier ?",
            "enfant-m|Oui, maman.",
            "papa|On est bien, ici.",
        )
    return L(
        "narrateur|Amir s'approche de la porte.",
        "enfant-m|Ça souffle un peu, ici.",
        "maman|Tiens la barre, Amir.",
        "narrateur|Le wagon penche, puis se redresse.",
        "papa|Les rails passent, très près.",
        "narrateur|Un sifflet lointain traverse l'air.",
        "enfant-m|Nina, le vent est bon !",
        "narrateur|La barre reste seule, froide.",
        "enfant-m|Elle n'est pas là.",
        "narrateur|Amir lâche un souffle, déçu.",
        "papa|Tu l'invites, sans tirer ?",
        "enfant-m|Oui.",
        "maman|La barre est froide, sous ta main.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Amir a collé son nez.",
            "maman|Il regarde quoi, Amir ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Le petit toc est fait.",
            "papa|Il a déplié quoi ?",
        )
    return L(
        "narrateur|La barre reste froide, sous la main.",
        "maman|Il se tient près de quoi ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Les champs.",
            "maman|Oui.",
            "narrateur|La vitre tremble, légère.",
            "narrateur|Un toit rouge file, loin.",
            "enfant-m|Nina est dans le wagon.",
            "papa|Je l'entends, plus loin.",
            "maman|Vous allez la trouver.",
            "enfant-m|Je lui propose la mer.",
        )
    if t1 == 2:
        return L(
            "enfant-m|La tablette.",
            "papa|Oui.",
            "narrateur|Le pain tiède chauffe le papier.",
            "narrateur|Une miette roule, puis s'arrête.",
            "enfant-m|Nina est dans le wagon.",
            "maman|Je l'entends, plus loin.",
            "papa|Le bois tient bien, maintenant.",
            "enfant-m|Je lui propose le pain.",
        )
    return L(
        "enfant-m|La porte.",
        "maman|Oui.",
        "narrateur|Un peu d'air entre, frais.",
        "narrateur|Les rails claquent, très près.",
        "enfant-m|Nina est dans le wagon.",
        "papa|Je l'entends, plus loin.",
        "maman|La barre reste sous ta main.",
        "enfant-m|Je lui propose le vent.",
    )


def t2_question(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nina est dans le wagon, plus loin.",
            "narrateur|Son carnet est ouvert, près d'un genou.",
            "narrateur|Une pomme croque, quelque part.",
            "narrateur|Le sifflet peut arriver.",
            "papa|On va vers quoi, Amir ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Nina est dans le wagon, près du bois.",
            "narrateur|Le carnet, la pomme, ou le sifflet.",
            "papa|On va vers quoi, Amir ?",
        )
    return L(
        "narrateur|Nina est dans le wagon, près du vent.",
        "narrateur|Le carnet, la pomme, ou le sifflet.",
        "maman|On va vers quoi, Amir ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        if t1 == 1:
            return L(
                "narrateur|Amir revient vers la vitre, pressé.",
                "narrateur|Nina dessine une vache, absorbée.",
                "enfant-m|Nina, la mer arrive !",
                "narrateur|Elle ne lève pas les yeux.",
                "enfant-f|Ma vache n'est pas finie.",
                "enfant-m|Tu viens voir les champs ?",
                "enfant-f|J'ai pas fini.",
                "narrateur|Amir tire un coin du carnet.",
                "narrateur|Nina le retient, serré.",
                "narrateur|Le crayon casse, net.",
                "enfant-m|Oh.",
                "maman|Elle dessine, très concentrée.",
                "papa|Tu proposes comment, Amir ?",
            )
        if t1 == 2:
            return L(
                "narrateur|Amir pose le pain près du carnet.",
                "narrateur|Nina tient son crayon, fermé.",
                "enfant-m|Nina, le pain est tiède.",
                "narrateur|Une tache bleue sèche sur le papier.",
                "enfant-f|Ma vache n'est pas finie.",
                "enfant-m|Tu viens à la tablette ?",
                "enfant-f|J'ai pas fini.",
                "narrateur|Il pousse le pain trop près.",
                "narrateur|La tache bleue bave un peu.",
                "narrateur|Nina recule son carnet.",
                "papa|Elle reste dans son dessin.",
                "maman|Tu proposes comment, Amir ?",
            )
        return L(
            "narrateur|Le papier claque, près de la porte.",
            "narrateur|Nina dessine sur ses genoux.",
            "enfant-m|Nina, le vent est bon.",
            "narrateur|Le crayon glisse, puis reprend.",
            "enfant-f|Ma vache n'est pas finie.",
            "enfant-m|Tu viens à la barre ?",
            "enfant-f|J'ai pas fini.",
            "narrateur|Le vent soulève la feuille.",
            "narrateur|Nina la plaque, fâchée.",
            "maman|Le vent agite sa feuille.",
            "papa|Tu proposes comment, Amir ?",
        )
    if t2 == 2:
        if t1 == 1:
            return L(
                "narrateur|Une pomme croque, contre la vitre.",
                "narrateur|Nina mange, les yeux dehors.",
                "enfant-m|Nina, les champs courent.",
                "enfant-f|J'ai pas fini ma pomme.",
                "enfant-m|Tu viens coller ton nez ?",
                "enfant-f|Après, peut-être.",
                "narrateur|Le jus brille au coin de la bouche.",
                "narrateur|Amir tend le pain trop vite.",
                "narrateur|Nina tourne l'épaule.",
                "narrateur|Elle ne dit rien.",
                "maman|Elle croque, sans se presser.",
                "papa|Tu proposes comment, Amir ?",
            )
        if t1 == 2:
            return L(
                "narrateur|Nina a sa pomme, à la tablette.",
                "narrateur|Le pain tiède attend, près d'elle.",
                "enfant-m|Nina, tu veux du pain ?",
                "enfant-f|J'ai ma pomme.",
                "enfant-m|On partage ?",
                "enfant-f|Pas maintenant.",
                "narrateur|Deux goûters, trop loin l'un de l'autre.",
                "narrateur|Amir pousse le pain.",
                "narrateur|Elle recule son coude.",
                "papa|Elle n'a pas fini, Amir.",
                "maman|Tu proposes comment, alors ?",
            )
        return L(
            "narrateur|Nina croque près de la porte, debout.",
            "narrateur|Le jus coule un peu, sur le pouce.",
            "enfant-m|Nina, le vent est bon.",
            "enfant-f|J'ai pas fini ma pomme.",
            "enfant-m|Tu viens à la barre ?",
            "enfant-f|Après, peut-être.",
            "narrateur|La pomme avance, lente.",
            "narrateur|Amir touche son bras.",
            "narrateur|Elle se fige, nette.",
            "maman|Elle mange, sans se presser.",
            "papa|Tu proposes comment, Amir ?",
        )
    if t1 == 1:
        return L(
            "narrateur|Nina colle l'oreille contre la vitre.",
            "enfant-f|J'attends le sifflet, Amir.",
            "enfant-m|La mer arrive, après.",
            "narrateur|Elle ne bouge pas.",
            "enfant-m|Tu viens voir les champs ?",
            "enfant-f|Quand ça siffle, d'abord.",
            "papa|Elle écoute le rail, dur.",
            "maman|Le sifflet n'est pas là.",
            "narrateur|Amir parle trop fort.",
            "narrateur|Elle se bouche l'oreille.",
            "narrateur|Le ventre d'Amir se serre.",
            "papa|Tu proposes comment, Amir ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Nina quitte la tablette, l'oreille tendue.",
            "enfant-f|J'attends le sifflet, Amir.",
            "enfant-m|Le pain est tiède.",
            "narrateur|Elle ne s'assoit plus.",
            "enfant-m|Tu reviens manger ?",
            "enfant-f|Quand ça siffle, d'abord.",
            "maman|Elle écoute le wagon, tendue.",
            "papa|Le sifflet n'est pas là.",
            "narrateur|Amir agite le papier.",
            "narrateur|Trop de bruit pour elle.",
            "maman|Tu proposes comment, Amir ?",
        )
    return L(
        "narrateur|Nina se tient près de la porte.",
        "enfant-f|J'attends le sifflet, Amir.",
        "enfant-m|Ça souffle trop, ici.",
        "narrateur|Elle serre la barre, ferme.",
        "enfant-m|Tu restes avec moi ?",
        "enfant-f|Quand ça siffle, d'abord.",
        "papa|Elle écoute le rail, très près.",
        "maman|Le sifflet n'est pas là.",
        "narrateur|Amir tire sa manche.",
        "narrateur|Elle la reprend, nette.",
        "papa|Tu proposes comment, Amir ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le crayon de Nina reste en l'air.",
            "papa|Attendre, parler tout bas, ou dessiner ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La pomme n'est pas finie.",
            "maman|Attendre, proposer le pain, ou garder ?",
        )
    return L(
        "narrateur|Le sifflet n'est pas là.",
        "papa|Écouter, un petit jeu, ou plus tard ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    table = {
        (1, 1, 1): L(
            "enfant-m|J'attends un peu.",
            "enfant-f|Merci, Amir.",
            "narrateur|Le crayon reprend la tache bleue.",
            "narrateur|Les champs courent, sans eux.",
            "narrateur|Nina pose le crayon, enfin.",
            "enfant-f|Ma vache est finie, maintenant.",
            "enfant-m|Tu viens, alors ?",
            "enfant-f|Oui.",
            "papa|Tu as laissé sa vache finir.",
            "narrateur|Amir souffle, soulagé.",
            "narrateur|Ses épaules descendent.",
        ),
        (1, 1, 2): L(
            "enfant-m|Nina, je te propose la mer.",
            "narrateur|Il parle contre la vitre, bas.",
            "narrateur|Sa voix reste près d'elle.",
            "enfant-f|J'ai entendu, Amir.",
            "enfant-m|Tu peux dire non.",
            "enfant-f|Oui, je viens.",
            "narrateur|Elle ferme le carnet, lente.",
            "papa|Ta voix est restée bas.",
            "maman|Elle a choisi d'elle-même.",
            "narrateur|Un nuage de souffle marque la vitre.",
        ),
        (1, 1, 3): L(
            "enfant-m|Je dessine à côté.",
            "narrateur|Amir s'assoit près de la vitre.",
            "narrateur|Il ne prend pas le crayon.",
            "enfant-f|Tu fais un pré, toi aussi ?",
            "enfant-m|Oui, avec toi.",
            "narrateur|Deux vaches, maintenant, sur le papier.",
            "enfant-f|Après, on va voir la mer.",
            "papa|Tu es resté près d'elle.",
            "maman|Elle a proposé la suite.",
            "narrateur|Un brin d'herbe vert joint les deux.",
        ),
        (2, 1, 1): L(
            "enfant-m|J'attends un peu.",
            "enfant-f|Merci, Amir.",
            "narrateur|Le pain tiède attend, sans bouger.",
            "narrateur|Le crayon finit une oreille ronde.",
            "enfant-f|Ma vache est finie, maintenant.",
            "enfant-m|Tu viens à la tablette ?",
            "enfant-f|Oui.",
            "papa|Tu as laissé sa vache finir.",
            "narrateur|Amir relâche le papier, enfin.",
            "maman|Le bois a gardé sa place.",
        ),
        (2, 1, 2): L(
            "enfant-m|Nina, je te propose la mer.",
            "narrateur|Il parle contre la tablette, bas.",
            "narrateur|Le bois renvoie sa voix, petite.",
            "enfant-f|J'ai entendu, Amir.",
            "enfant-m|Tu peux dire non.",
            "enfant-f|Oui, je viens.",
            "narrateur|Elle glisse le carnet sous le pain.",
            "papa|Ta voix est restée bas.",
            "maman|Elle a choisi d'elle-même.",
            "narrateur|Une miette colle au crayon bleu.",
        ),
        (2, 1, 3): L(
            "enfant-m|Je dessine à côté.",
            "narrateur|Amir s'assoit près de la tablette.",
            "narrateur|Il ne prend pas le crayon.",
            "enfant-f|Tu fais un pré, toi aussi ?",
            "enfant-m|Oui, avec toi.",
            "narrateur|Deux vaches marchent sur le bois.",
            "enfant-f|Après, on va voir la mer.",
            "papa|Tu es resté près d'elle.",
            "maman|Elle a proposé la suite.",
            "narrateur|Le pain garde un trait d'herbe.",
        ),
        (3, 1, 1): L(
            "enfant-m|J'attends un peu.",
            "enfant-f|Merci, Amir.",
            "narrateur|Le vent de la porte passe, seul.",
            "narrateur|Le crayon ferme un ventre blanc.",
            "enfant-f|Ma vache est finie, maintenant.",
            "enfant-m|Tu viens à la barre ?",
            "enfant-f|Oui.",
            "papa|Tu as laissé sa vache finir.",
            "narrateur|Amir lâche la barre, soulagé.",
            "maman|Le vent n'a plus volé la feuille.",
        ),
        (3, 1, 2): L(
            "enfant-m|Nina, je te propose la mer.",
            "narrateur|Il parle contre la barre, bas.",
            "narrateur|Sa voix se mêle au vent, mince.",
            "enfant-f|J'ai entendu, Amir.",
            "enfant-m|Tu peux dire non.",
            "enfant-f|Oui, je viens.",
            "narrateur|Elle ferme le carnet, contre le vent.",
            "papa|Ta voix est restée bas.",
            "maman|Elle a choisi d'elle-même.",
            "narrateur|La barre garde une chaleur de main.",
        ),
        (3, 1, 3): L(
            "enfant-m|Je dessine à côté.",
            "narrateur|Amir s'assoit près de la barre.",
            "narrateur|Il ne prend pas le crayon.",
            "enfant-f|Tu fais un pré, toi aussi ?",
            "enfant-m|Oui, avec toi.",
            "narrateur|Deux vaches tiennent sur les genoux.",
            "enfant-f|Après, on va voir la mer.",
            "papa|Tu es resté près d'elle.",
            "maman|Elle a proposé la suite.",
            "narrateur|Un trait d'herbe résiste au vent.",
        ),
        (1, 2, 1): L(
            "enfant-m|J'attends la fin.",
            "enfant-f|Merci, Amir.",
            "narrateur|La vitre garde les champs, dehors.",
            "narrateur|La pomme devient un petit trognon.",
            "enfant-f|C'est fini, maintenant.",
            "enfant-m|Tu viens, alors ?",
            "enfant-f|Oui.",
            "papa|Tu as laissé sa pomme finir.",
            "maman|Elle a dit oui, à son heure.",
            "narrateur|Amir range le pain, sans le pousser.",
        ),
        (1, 2, 2): L(
            "enfant-m|Nina, tu veux du pain ?",
            "narrateur|Il tend le pain, près de la vitre.",
            "narrateur|Il s'arrête avant son épaule.",
            "enfant-f|Un tout petit bout, alors.",
            "enfant-m|D'accord.",
            "narrateur|Le papier craque, léger.",
            "enfant-f|Il est tiède.",
            "enfant-m|On est deux, maintenant.",
            "papa|Le pain est resté dans sa main.",
            "maman|Elle a pris ce qu'elle voulait.",
        ),
        (1, 2, 3): L(
            "enfant-f|Pas de pain, Amir.",
            "enfant-m|D'accord.",
            "enfant-m|Je garde le mien, alors.",
            "narrateur|Le pain reste près de la vitre.",
            "narrateur|Il croque de son côté, sans insister.",
            "enfant-f|Tu peux parler, d'ici.",
            "enfant-m|Je reste près de toi.",
            "papa|Tu as gardé ton pain.",
            "maman|Vous êtes ensemble, d'ici.",
            "narrateur|Deux odeurs, pomme et pain, côte à côte.",
        ),
        (2, 2, 1): L(
            "enfant-m|J'attends la fin.",
            "enfant-f|Merci, Amir.",
            "narrateur|Le pain tiède garde son papier.",
            "narrateur|La pomme devient un petit trognon.",
            "enfant-f|C'est fini, maintenant.",
            "enfant-m|Tu viens, alors ?",
            "enfant-f|Oui.",
            "papa|Tu as laissé sa pomme finir.",
            "maman|Elle a dit oui, à son heure.",
            "narrateur|Le bois de la tablette sent le sucre.",
        ),
        (2, 2, 2): L(
            "enfant-m|Nina, tu veux du pain ?",
            "narrateur|Il tend le pain, sur la tablette.",
            "narrateur|Il le pose, sans le pousser.",
            "enfant-f|Un tout petit bout, alors.",
            "enfant-m|D'accord.",
            "narrateur|Le papier craque, léger.",
            "enfant-f|Il est tiède.",
            "enfant-m|On est deux, maintenant.",
            "papa|Le pain est resté dans sa main.",
            "maman|Elle a pris ce qu'elle voulait.",
            "narrateur|Deux miettes dorment sur le bois.",
        ),
        (2, 2, 3): L(
            "enfant-f|Pas de pain, Amir.",
            "enfant-m|D'accord.",
            "enfant-m|Je garde le mien, alors.",
            "narrateur|Le pain reste sur la tablette.",
            "narrateur|Il croque de son côté, sans insister.",
            "enfant-f|Tu peux parler, d'ici.",
            "enfant-m|Je reste près de toi.",
            "papa|Tu as gardé ton pain.",
            "maman|Vous êtes ensemble, d'ici.",
            "narrateur|La pomme et le pain gardent leur place.",
        ),
        (3, 2, 1): L(
            "enfant-m|J'attends la fin.",
            "enfant-f|Merci, Amir.",
            "narrateur|La barre reste froide, sous la main.",
            "narrateur|La pomme devient un petit trognon.",
            "enfant-f|C'est fini, maintenant.",
            "enfant-m|Tu viens, alors ?",
            "enfant-f|Oui.",
            "papa|Tu as laissé sa pomme finir.",
            "maman|Elle a dit oui, à son heure.",
            "narrateur|Le vent a séché le jus du pouce.",
        ),
        (3, 2, 2): L(
            "enfant-m|Nina, tu veux du pain ?",
            "narrateur|Il tend le pain, près de la porte.",
            "narrateur|Le papier claque, puis se tait.",
            "enfant-f|Un tout petit bout, alors.",
            "enfant-m|D'accord.",
            "narrateur|Elle croque, une main à la barre.",
            "enfant-f|Il est tiède.",
            "enfant-m|On est deux, maintenant.",
            "papa|Le pain est resté dans sa main.",
            "maman|Elle a pris ce qu'elle voulait.",
        ),
        (3, 2, 3): L(
            "enfant-f|Pas de pain, Amir.",
            "enfant-m|D'accord.",
            "enfant-m|Je garde le mien, alors.",
            "narrateur|Le pain reste près de la porte.",
            "narrateur|Il croque de son côté, sans insister.",
            "enfant-f|Tu peux parler, d'ici.",
            "enfant-m|Je reste près de toi.",
            "papa|Tu as gardé ton pain.",
            "maman|Vous êtes ensemble, d'ici.",
            "narrateur|Deux goûters tiennent, malgré le vent.",
        ),
        (1, 3, 1): L(
            "enfant-m|J'écoute avec toi.",
            "narrateur|Deux oreilles, maintenant, contre la vitre.",
            "narrateur|Le rail chante, bas.",
            "enfant-f|Tu entends, toi aussi ?",
            "enfant-m|Oui, avec toi.",
            "narrateur|Un sifflet arrive, long, enfin.",
            "enfant-f|C'est lui !",
            "papa|Tu as écouté à son heure.",
            "maman|Vous l'avez eu, tous les deux.",
            "narrateur|La vitre vibre, puis se tait.",
        ),
        (1, 3, 2): L(
            "enfant-m|Un tout petit jeu, Nina ?",
            "enfant-f|Très petit, alors.",
            "enfant-m|D'accord.",
            "narrateur|Ils comptent les arbres, à la vitre.",
            "narrateur|Ils comptent jusqu'à trois, bas.",
            "narrateur|Le sifflet coupe le trois, pile.",
            "enfant-f|C'est lui !",
            "papa|Tu as proposé court, juste assez.",
            "maman|Le sifflet a dit la fin.",
            "narrateur|Un arbre reste collé au chiffre deux.",
        ),
        (1, 3, 3): L(
            "enfant-m|On regarde plus tard, alors ?",
            "enfant-f|Oui, plus tard.",
            "enfant-m|D'accord.",
            "narrateur|La vitre garde sa place, sans lui.",
            "narrateur|Nina serre l'oreille, sans bouger.",
            "enfant-f|Garde la mer pour moi.",
            "enfant-m|Elle t'attend.",
            "papa|Tu as proposé une autre heure.",
            "maman|Elle a dit oui, pour plus tard.",
            "narrateur|Amir laisse un siège vide, à dessein.",
        ),
        (2, 3, 1): L(
            "enfant-m|J'écoute avec toi.",
            "narrateur|Deux oreilles, maintenant, près de la tablette.",
            "narrateur|Le rail chante, bas.",
            "enfant-f|Tu entends, toi aussi ?",
            "enfant-m|Oui, avec toi.",
            "narrateur|Un sifflet arrive, long, enfin.",
            "enfant-f|C'est lui !",
            "papa|Tu as écouté à son heure.",
            "maman|Vous l'avez eu, tous les deux.",
            "narrateur|Le pain a cessé de crisser.",
        ),
        (2, 3, 2): L(
            "enfant-m|Un tout petit jeu, Nina ?",
            "enfant-f|Très petit, alors.",
            "enfant-m|D'accord.",
            "narrateur|Ils comptent les miettes, à la tablette.",
            "narrateur|Ils comptent jusqu'à trois, bas.",
            "narrateur|Le sifflet coupe le trois, pile.",
            "enfant-f|C'est lui !",
            "papa|Tu as proposé court, juste assez.",
            "maman|Le sifflet a dit la fin.",
            "narrateur|Cette miette-là n'a pas bougé.",
        ),
        (2, 3, 3): L(
            "enfant-m|On regarde plus tard, alors ?",
            "enfant-f|Oui, plus tard.",
            "enfant-m|D'accord.",
            "narrateur|La tablette garde sa place, sans lui.",
            "narrateur|Nina serre l'oreille, sans bouger.",
            "enfant-f|Garde la mer pour moi.",
            "enfant-m|Elle t'attend.",
            "papa|Tu as proposé une autre heure.",
            "maman|Elle a dit oui, pour plus tard.",
            "narrateur|Le pain attend, plié, pour deux.",
        ),
        (3, 3, 1): L(
            "enfant-m|J'écoute avec toi.",
            "narrateur|Deux oreilles, maintenant, près de la porte.",
            "narrateur|Le rail chante, bas.",
            "enfant-f|Tu entends, toi aussi ?",
            "enfant-m|Oui, avec toi.",
            "narrateur|Un sifflet arrive, long, enfin.",
            "enfant-f|C'est lui !",
            "papa|Tu as écouté à son heure.",
            "maman|Vous l'avez eu, tous les deux.",
            "narrateur|La barre vibre, puis se tait.",
        ),
        (3, 3, 2): L(
            "enfant-m|Un tout petit jeu, Nina ?",
            "enfant-f|Très petit, alors.",
            "enfant-m|D'accord.",
            "narrateur|Ils comptent les clics, à la porte.",
            "narrateur|Ils comptent jusqu'à trois, bas.",
            "narrateur|Le sifflet coupe le trois, pile.",
            "enfant-f|C'est lui !",
            "papa|Tu as proposé court, juste assez.",
            "maman|Le sifflet a dit la fin.",
            "narrateur|Le vent a avalé le deux, pas le trois.",
        ),
        (3, 3, 3): L(
            "enfant-m|On regarde plus tard, alors ?",
            "enfant-f|Oui, plus tard.",
            "enfant-m|D'accord.",
            "narrateur|La porte garde sa place, sans lui.",
            "narrateur|Nina serre l'oreille, sans bouger.",
            "enfant-f|Garde la mer pour moi.",
            "enfant-m|Elle t'attend.",
            "papa|Tu as proposé une autre heure.",
            "maman|Elle a dit oui, pour plus tard.",
            "narrateur|Amir garde un bout de barre, libre.",
        ),
    }
    return table[(t1, t2, t3)]


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    table = {
        (1, 1, 1): L(
            "narrateur|Une ligne bleue arrive, au fond.",
            "enfant-f|C'est la mer, Amir ?",
            "enfant-m|Oui, elle est là.",
            "papa|Vous avez attendu le bon moment.",
            "maman|Le pain est un peu tiède.",
            "narrateur|La vitre garde un peu de sel.",
            "narrateur|Nina souffle sur le sel, minuscule.",
            "enfant-m|C'est notre mer, maintenant.",
            "narrateur|Un peu de sel reste sur le dessin.",
        ),
        (1, 1, 2): L(
            "narrateur|Le carnet est fermé, contre le genou.",
            "enfant-m|Tu as dit oui, tout bas.",
            "enfant-f|J'avais entendu, près de toi.",
            "papa|Ta voix est restée bas.",
            "maman|Mangez un peu, sans crier.",
            "narrateur|La vitre garde un peu de sel.",
            "narrateur|Nina pose sa joue, légère.",
            "enfant-m|Reste autant que tu veux.",
            "narrateur|La vache du carnet regarde la mer.",
        ),
        (1, 1, 3): L(
            "narrateur|Après le pré, la mer entre au crayon.",
            "enfant-f|On a dessiné ensemble, d'abord.",
            "enfant-m|Puis tu as dit : on y va.",
            "maman|Deux vaches, puis une ligne bleue.",
            "papa|Le wagon redevient calme.",
            "narrateur|La vitre garde un peu de sel.",
            "narrateur|Nina rit, minuscule.",
            "enfant-m|La mer t'a attendue.",
            "narrateur|Deux crayons se touchent, près du bleu.",
        ),
        (1, 2, 1): L(
            "narrateur|Le trognon part dans le sac.",
            "enfant-f|J'ai fini, Amir.",
            "enfant-m|Tu as dit oui.",
            "papa|Vous tenez tous les deux, maintenant.",
            "maman|Le pain descend jusqu'à vous.",
            "narrateur|La vitre garde un peu de sel.",
            "narrateur|Nina tape deux fois, léger.",
            "enfant-m|C'est le signal.",
            "narrateur|Le trognon de pomme sent le sucre.",
        ),
        (1, 2, 2): L(
            "narrateur|Le pain a deux bouts, maintenant.",
            "enfant-m|Le tien, et le mien.",
            "enfant-f|Il était tiède, Amir.",
            "papa|Vous avez partagé sans tout casser.",
            "maman|La mer, au fond, pour deux.",
            "narrateur|La vitre garde un peu de sel.",
            "narrateur|Nina souffle, puis Amir souffle.",
            "enfant-m|On reste un peu.",
            "narrateur|Une miette tiède dort contre la vitre.",
        ),
        (1, 2, 3): L(
            "narrateur|Deux goûters restent côte à côte.",
            "enfant-f|Tu n'as pas pris ma pomme.",
            "enfant-m|Tu avais dit non.",
            "papa|Sa pomme est restée à elle.",
            "maman|Vous vous parlez, d'ici.",
            "narrateur|La vitre garde un peu de sel.",
            "narrateur|Nina tend un bout de pomme, alors.",
            "enfant-m|Je le prends, d'à côté.",
            "narrateur|Deux goûters se parlent, près du bleu.",
        ),
        (1, 3, 1): L(
            "narrateur|Le sifflet s'en va, loin.",
            "enfant-f|On l'a eu, ensemble.",
            "enfant-m|Puis la mer est arrivée.",
            "papa|Vous avez écouté à son heure.",
            "maman|Le pain attend, tiède.",
            "narrateur|La vitre garde un peu de sel.",
            "narrateur|Nina fait un signe vers le bleu.",
            "enfant-m|La mer t'a vue, une minute.",
            "narrateur|Un oiseau blanc passe, loin.",
        ),
        (1, 3, 2): L(
            "narrateur|Le petit jeu est fini.",
            "enfant-f|Le sifflet a coupé le trois.",
            "enfant-m|Merci d'avoir joué.",
            "papa|Vous avez compté juste assez.",
            "maman|La mer entre, maintenant.",
            "narrateur|La vitre garde un peu de sel.",
            "narrateur|Nina fait un signe vers le bleu.",
            "enfant-m|On l'a vue, une minute.",
            "narrateur|Le clic des rails reprend, léger.",
        ),
        (1, 3, 3): L(
            "narrateur|Nina écoute un instant, plus tard.",
            "enfant-m|Plus tard, elle a dit.",
            "enfant-m|Garde la mer pour moi.",
            "papa|Tu as proposé une autre heure.",
            "maman|Le pain attend, tiède.",
            "narrateur|La vitre garde un peu de sel.",
            "narrateur|Amir garde une place, libre.",
            "enfant-m|Elle t'attend, Nina.",
            "narrateur|Le vent de la mer entre, salé.",
        ),
        (2, 1, 1): L(
            "narrateur|Une ligne bleue arrive, au fond.",
            "enfant-f|C'est la mer, Amir ?",
            "enfant-m|Oui, elle est là.",
            "papa|Vous avez attendu le bon moment.",
            "maman|Le pain est un peu tiède.",
            "narrateur|La tablette garde une miette tiède.",
            "narrateur|Nina souffle sur le sel, minuscule.",
            "enfant-m|C'est notre mer, maintenant.",
            "narrateur|Une miette tiède colle au crayon.",
        ),
        (2, 1, 2): L(
            "narrateur|Le carnet glisse sous le pain.",
            "enfant-m|Tu as dit oui, tout bas.",
            "enfant-f|J'avais entendu, près du bois.",
            "papa|Ta voix est restée bas.",
            "maman|Mangez un peu, sans crier.",
            "narrateur|La tablette garde une miette tiède.",
            "narrateur|Nina pose sa joue, légère.",
            "enfant-m|Reste autant que tu veux.",
            "narrateur|Le papier du pain garde une vache.",
        ),
        (2, 1, 3): L(
            "narrateur|Après le pré, la mer entre au crayon.",
            "enfant-f|On a dessiné ensemble, d'abord.",
            "enfant-m|Puis tu as dit : on y va.",
            "maman|Deux vaches, puis une ligne bleue.",
            "papa|Le wagon redevient calme.",
            "narrateur|La tablette garde une miette tiède.",
            "narrateur|Nina rit, minuscule.",
            "enfant-m|La mer t'a attendue.",
            "narrateur|Le bois de la tablette sent le sel.",
        ),
        (2, 2, 1): L(
            "narrateur|Le trognon part dans le sac.",
            "enfant-f|J'ai fini, Amir.",
            "enfant-m|Tu as dit oui.",
            "papa|Vous tenez tous les deux, maintenant.",
            "maman|Le pain descend jusqu'à vous.",
            "narrateur|La tablette garde une miette tiède.",
            "narrateur|Nina tape deux fois, léger.",
            "enfant-m|C'est le signal.",
            "narrateur|Le sac ferme le trognon, et le pain.",
        ),
        (2, 2, 2): L(
            "narrateur|Le pain a deux bouts, maintenant.",
            "enfant-m|Le tien, et le mien.",
            "enfant-f|Il était tiède, Amir.",
            "papa|Vous avez partagé sans tout casser.",
            "maman|La mer, au fond, pour deux.",
            "narrateur|La tablette garde une miette tiède.",
            "narrateur|Nina souffle, puis Amir souffle.",
            "enfant-m|On reste un peu.",
            "narrateur|Deux bouts de pain, tièdes, sur le bois.",
        ),
        (2, 2, 3): L(
            "narrateur|Deux goûters restent côte à côte.",
            "enfant-f|Tu n'as pas pris ma pomme.",
            "enfant-m|Tu avais dit non.",
            "papa|Sa pomme est restée à elle.",
            "maman|Vous vous parlez, d'ici.",
            "narrateur|La tablette garde une miette tiède.",
            "narrateur|Nina tend un bout de pomme, alors.",
            "enfant-m|Je le prends, d'à côté.",
            "narrateur|La pomme reste à elle, près du pain.",
        ),
        (2, 3, 1): L(
            "narrateur|Le sifflet s'en va, loin.",
            "enfant-f|On l'a eu, ensemble.",
            "enfant-m|Puis la mer est arrivée.",
            "papa|Vous avez écouté à son heure.",
            "maman|Le pain attend, tiède.",
            "narrateur|La tablette garde une miette tiède.",
            "narrateur|Nina fait un signe vers le bleu.",
            "enfant-m|La mer t'a vue, une minute.",
            "narrateur|Le pain reste tiède, après le sifflet.",
        ),
        (2, 3, 2): L(
            "narrateur|Le petit jeu est fini.",
            "enfant-f|Le sifflet a coupé le trois.",
            "enfant-m|Merci d'avoir joué.",
            "papa|Vous avez compté juste assez.",
            "maman|La mer entre, maintenant.",
            "narrateur|La tablette garde une miette tiède.",
            "narrateur|Nina fait un signe vers le bleu.",
            "enfant-m|On l'a vue, une minute.",
            "narrateur|Ils ont compté les miettes jusqu'au bleu.",
        ),
        (2, 3, 3): L(
            "narrateur|Nina écoute un instant, plus tard.",
            "enfant-m|Plus tard, elle a dit.",
            "enfant-m|Garde la mer pour moi.",
            "papa|Tu as proposé une autre heure.",
            "maman|Le pain attend, tiède.",
            "narrateur|La tablette garde une miette tiède.",
            "narrateur|Amir garde une place, libre.",
            "enfant-m|Elle t'attend, Nina.",
            "narrateur|Une place vide attend, près du pain.",
        ),
        (3, 1, 1): L(
            "narrateur|Une ligne bleue arrive, au fond.",
            "enfant-f|C'est la mer, Amir ?",
            "enfant-m|Oui, elle est là.",
            "papa|Vous avez attendu le bon moment.",
            "maman|Le pain est un peu tiède.",
            "narrateur|La porte garde un peu de vent.",
            "narrateur|Nina souffle sur le sel, minuscule.",
            "enfant-m|C'est notre mer, maintenant.",
            "narrateur|Le sel du vent reste sur le dessin.",
        ),
        (3, 1, 2): L(
            "narrateur|Le carnet est fermé, contre le vent.",
            "enfant-m|Tu as dit oui, tout bas.",
            "enfant-f|J'avais entendu, près de la barre.",
            "papa|Ta voix est restée bas.",
            "maman|Mangez un peu, sans crier.",
            "narrateur|La porte garde un peu de vent.",
            "narrateur|Nina pose sa joue, légère.",
            "enfant-m|Reste autant que tu veux.",
            "narrateur|La barre froide a vu le oui.",
        ),
        (3, 1, 3): L(
            "narrateur|Après le pré, la mer entre au crayon.",
            "enfant-f|On a dessiné ensemble, d'abord.",
            "enfant-m|Puis tu as dit : on y va.",
            "maman|Deux vaches, puis une ligne bleue.",
            "papa|Le wagon redevient calme.",
            "narrateur|La porte garde un peu de vent.",
            "narrateur|Nina rit, minuscule.",
            "enfant-m|La mer t'a attendue.",
            "narrateur|Deux crayons, près de la barre.",
        ),
        (3, 2, 1): L(
            "narrateur|Le trognon part dans le sac.",
            "enfant-f|J'ai fini, Amir.",
            "enfant-m|Tu as dit oui.",
            "papa|Vous tenez tous les deux, maintenant.",
            "maman|Le pain descend jusqu'à vous.",
            "narrateur|La porte garde un peu de vent.",
            "narrateur|Nina tape deux fois, léger.",
            "enfant-m|C'est le signal.",
            "narrateur|Le trognon voyage, près du vent.",
        ),
        (3, 2, 2): L(
            "narrateur|Le pain a deux bouts, maintenant.",
            "enfant-m|Le tien, et le mien.",
            "enfant-f|Il était tiède, Amir.",
            "papa|Vous avez partagé sans tout casser.",
            "maman|La mer, au fond, pour deux.",
            "narrateur|La porte garde un peu de vent.",
            "narrateur|Nina souffle, puis Amir souffle.",
            "enfant-m|On reste un peu.",
            "narrateur|Le pain se partage, contre la barre.",
        ),
        (3, 2, 3): L(
            "narrateur|Deux goûters restent côte à côte.",
            "enfant-f|Tu n'as pas pris ma pomme.",
            "enfant-m|Tu avais dit non.",
            "papa|Sa pomme est restée à elle.",
            "maman|Vous vous parlez, d'ici.",
            "narrateur|La porte garde un peu de vent.",
            "narrateur|Nina tend un bout de pomme, alors.",
            "enfant-m|Je le prends, d'à côté.",
            "narrateur|Deux goûters, et le vent entre.",
        ),
        (3, 3, 1): L(
            "narrateur|Le sifflet s'en va, loin.",
            "enfant-f|On l'a eu, ensemble.",
            "enfant-m|Puis la mer est arrivée.",
            "papa|Vous avez écouté à son heure.",
            "maman|Le pain attend, tiède.",
            "narrateur|La porte garde un peu de vent.",
            "narrateur|Nina fait un signe vers le bleu.",
            "enfant-m|La mer t'a vue, une minute.",
            "narrateur|Deux oreilles, puis la mer, puis le sel.",
        ),
        (3, 3, 2): L(
            "narrateur|Le petit jeu est fini.",
            "enfant-f|Le sifflet a coupé le trois.",
            "enfant-m|Merci d'avoir joué.",
            "papa|Vous avez compté juste assez.",
            "maman|La mer entre, maintenant.",
            "narrateur|La porte garde un peu de vent.",
            "narrateur|Nina fait un signe vers le bleu.",
            "enfant-m|On l'a vue, une minute.",
            "narrateur|Ils ont compté les clics jusqu'au bleu.",
        ),
        (3, 3, 3): L(
            "narrateur|Nina écoute un instant, plus tard.",
            "enfant-m|Plus tard, elle a dit.",
            "enfant-m|Garde la mer pour moi.",
            "papa|Tu as proposé une autre heure.",
            "maman|Le pain attend, tiède.",
            "narrateur|La porte garde un peu de vent.",
            "narrateur|Amir garde une place, libre.",
            "enfant-m|Elle t'attend, Nina.",
            "narrateur|Amir garde une place, près du vent.",
        ),
    }
    return table[(t1, t2, t3)]


def write_tree() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    scripts: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {}
    profiles: dict[str, str] = {}
    emph: dict[str, str | None] = {}

    scripts["CHK_T0000_P0000"] = L(
        "narrateur|La gare du village sent le café.",
        "narrateur|Les pierres du quai brillent, mouillées.",
        "narrateur|Un train long attend, silencieux.",
        "narrateur|Ça sent le sel, mêlé au café.",
        "narrateur|Une flaque tremble entre deux pierres.",
        "narrateur|Un sac de papier laisse filer de la chaleur.",
        "maman|Le pain tiède est à toi, Amir.",
        "papa|Les billets sont dans ma poche.",
        "narrateur|Un goéland passe, trop haut pour le quai.",
        "enfant-m|La mer est derrière, pas loin.",
        "papa|Nina est dans le wagon.",
        "enfant-m|Je veux lui montrer la mer.",
        "narrateur|En ce moment, Amir monte la marche.",
        "maman|Le marchepied est haut.",
        "papa|Merci, tu tiens le sac bien.",
        "enfant-m|On va jusqu'à la mer.",
        "narrateur|Le papier du pain craque, chaud.",
    )
    sons["CHK_T0000_P0000"] = "gare,train,papier"
    profiles["CHK_T0000_P0000"] = "opening"
    emph["CHK_T0000_P0000"] = "pain tiède"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|Le wagon sent le pain chaud.",
        "narrateur|La vitre, la tablette, ou la porte.",
        "papa|On s'assoit où, Amir ?",
    )
    profiles["CHK_T0001_P0000"] = "choice"
    extras["CHK_T0001_P0000"] = t3lab("la vitre", "la tablette", "la porte")

    t2_sons = {1: "crayon,carnet", 2: "pomme,papier", 3: "sifflet,rails"}
    t2_emph = {1: "vache", 2: "pomme", 3: "sifflet"}
    t3_emph = {
        1: {1: "vache", 2: "voix", 3: "crayon"},
        2: {1: "pomme", 2: "pain", 3: "non"},
        3: {1: "sifflet", 2: "trois", 3: "plus tard"},
    }

    for t1 in (1, 2, 3):
        meta = T1[t1]
        base = f"CHK_T0001_P000{t1}"
        scripts[base] = t1_passage(t1)
        sons[base] = meta["sons"]
        profiles[base] = "action"
        emph[base] = meta["emph"]

        qid = f"{base}_Q0001"
        scripts[qid] = t1_q(t1)
        profiles[qid] = "clue"
        extras[qid] = qf(meta["ans"], meta["acc"], meta["retry"])
        emph[qid] = meta["emph"]

        cid = f"{base}_C0001"
        scripts[cid] = t1_confirm(t1)
        profiles[cid] = "confirm"

        t2q = f"{base}_T0002_P0000"
        scripts[t2q] = t2_question(t1)
        profiles[t2q] = "choice"
        extras[t2q] = t3lab("le carnet", "la pomme", "le sifflet")

        for t2 in (1, 2, 3):
            p2 = f"{base}_T0002_P000{t2}"
            scripts[p2] = t2_scene(t1, t2)
            sons[p2] = t2_sons[t2]
            profiles[p2] = "obstacle"
            emph[p2] = t2_emph[t2]

            t3q = f"{p2}_T0003_P0000"
            scripts[t3q] = t3_question(t2)
            profiles[t3q] = "choice"
            extras[t3q] = t3lab(*T3_LABS[t2])

            for t3i in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{t3i}"
                scripts[p3] = t3_scene(t1, t2, t3i)
                sons[p3] = t2_sons[t2]
                profiles[p3] = "resolution"
                emph[p3] = t3_emph[t2][t3i]

                fin = f"{p3}_F0001"
                scripts[fin] = fin_scene(t1, t2, t3i)
                sons[fin] = "mer,rails"
                profiles[fin] = "ending"
                emph[fin] = "pain tiède"

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{SID} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        text, script = from_script(scripts[cid])
        nc = dict(c)
        nc["text"] = text
        nc["script"] = script
        nc["sons"] = sons.get(cid, c.get("sons") or "") or ""
        extra_voice = {}
        if cid in emph:
            extra_voice["emphasis"] = emph[cid]
        nc.update(voice(text, profiles[cid], extra_voice or None))
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]

    check(SID, out["age_band"], out["chunks"])

    fins = [c for c in out["chunks"] if c.get("kind") == "passage_fin"]
    texts = [c["text"] for c in fins]
    if len(texts) != 27:
        raise SystemExit(f"fins {len(texts)} != 27")
    if len(set(texts)) != 27:
        raise SystemExit("fins non distinctes")
    for c in fins:
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{c['chunk_id']} fin mécanique: {last}")

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for tic in TICS + (
        "kenzo",
        "coussin",
        "le fort",
        "tomate",
        "panier rouge",
        "figuier",
        "la cuisine",
        "le jardin",
        "la chambre",
        "les cubes",
        "dînette",
        "dinette",
        "capitaine",
        "plic",
        "volet jaune",
    ):
        if tic in whole:
            raise SystemExit(f"{SID} slogan/calque: {tic}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "amir" not in blob or "nina" not in blob:
        raise SystemExit(f"{SID}: troupe Amir/Nina absente")
    for bad in ("déjà", "encore", "tout doux", "tout calme"):
        if bad in blob:
            raise SystemExit(f"{SID} tic corpus: {bad}")
    if not all(c.get("text_xai_tags") for c in out["chunks"]):
        raise SystemExit(f"{SID}: text_xai_tags manquant")
    if not all(c.get("notes") for c in out["chunks"]):
        raise SystemExit(f"{SID}: notes manquant")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    write_tree()
    relecture(
        SID,
        TITLE,
        "Gare, café, pain tiède, sel. Amir veut montrer la mer à Nina, tout de suite. "
        "T1 = vitre (champs) / tablette (pain) / porte (vent) : il s'installe, il appelle, "
        "le siège reste vide. T2 = carnet (vache à finir) / pomme (pas prête) / sifflet "
        "(elle écoute) : il propose trop vite, elle dit non, recule, ou se bouche l'oreille. "
        "T3 = neuf manières : attendre, parler bas, dessiner à côté ; attendre la pomme, "
        "proposer le pain, garder le sien (accepter le non) ; écouter ensemble, petit jeu, "
        "plus tard. La leçon se vit : il propose, il accepte oui, non, silence, ou une autre "
        "heure. 27 fins paient le pain tiède, le sel, et un détail du chemin.",
        "F-NAR-019. N1 ≤ 10. Kenzo et le slogan « Inviter sans forcer » jetés. "
        "Tics « encore / déjà / tout doux / tout calme » jetés. Première idée échoue "
        "(siège vide, crayon cassé, épaule tournée, oreille bouchée). Choix T3 change "
        "l'action. TTS par chunk (profiles example2). Un merci de papa (tenir le sac). "
        "Pas apply. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
