#!/usr/bin/env python3
"""TREE-COL-023 — Le banc mouillé et la pomme de Mila (F-NAR-019, N1).

Jardin sous le pommier, banc de bois, puis la maison.
COL.POL.001 vécu : bonjour, s'il te plaît, merci.
Tours de parole : envie de couper, retenue, écoute, plaisir d'être entendu.
Monde ≠ TREE-COL-002 (banc de fer, clapet, Amir).
Texte + TTS. Pas apply. Pas audio. Pas git.
"""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, words  # noqa: E402

SID = "TREE-COL-023"
LIM = 10
TITLE = "Le banc mouillé et la pomme de Mila"
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=300, energy="warm", contour="storytelling", noise=0.36,
        emphasis="étoile brune",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=la pomme va rouler sur le bois mouillé; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=108, speed=0.82, piper=1.32, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=360, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change la recherche; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=110, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=340, energy="focused", contour="rising", noise=0.32,
        emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde ce qui manque; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=122, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=300, energy="bright", contour="falling", noise=0.34,
        emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la phrase est arrivée entière; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=132, speed=0.96, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=280, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle veut la pomme maintenant; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=120, speed=0.90, piper=1.20, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=320, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_retenue; intensite=2; destinataire=enfant; sous_texte=deux voix, l'étoile se cache; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=126, speed=0.93, piper=1.16, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="bright", contour="falling", noise=0.35,
        emphasis="étoile",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=l'étoile a guidé le geste; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=108, speed=0.82, piper=1.30, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=360, energy="calm", contour="falling", noise=0.31,
        emphasis="pomme",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=l'étoile et le banc reviennent; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def wc(s: str) -> int:
    return words(s)


def L(*rows: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    prev = ""
    run = 1
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = wc(ph)
        if n > LIM:
            raise SystemExit(f"{n}>{LIM}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        low = ph.lower()
        if "aujourd'hui," in low or "aujourd’hui," in low:
            raise SystemExit(f"aujourd'hui: {ph}")
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
        out.append((role, ph))
    return out


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp:
        e = esc(emp)
        i = body.lower().find(e.lower())
        if i >= 0:
            body = body[:i] + f'<emphasis level="moderate">{body[i:i + len(e)]}</emphasis>' + body[i + len(e):]
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
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
        body = f'<{m["pitchTag"]}>{body}</{m["pitchTag"]}>'
    if m["pause"] >= 800:
        pause = "[long-pause]"
    elif m["pause"] >= 400:
        pause = "[pause]"
    else:
        pause = ""
    return f"{body} {pause}".strip()


def voice(chunk: dict, ls: list[tuple[str, str]], profile: str, extra: dict | None = None) -> None:
    extra = extra or {}
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    text = " ".join(t for _, t in ls)
    script = "\n".join(f"{r}|{t}" for r, t in ls)
    chunk["text"] = text
    chunk["script"] = script
    chunk["sons"] = extra.get("sons", chunk.get("sons") or "")
    if chunk["sons"] is None:
        chunk["sons"] = ""
    chunk["text_ssml"] = ssml(text, m)
    chunk["text_xai_tags"] = xai(text, m)
    chunk["rate_wpm"] = m["wpm"]
    chunk["rate_label"] = m["rate"]
    chunk["speed_xai"] = m["speed"]
    chunk["length_scale_piper"] = m["piper"]
    chunk["pitch_label"] = m["pitch"]
    chunk["pitch_ssml"] = m["pitchSsml"]
    chunk["pitch_xai_tag"] = m["pitchTag"]
    chunk["volume_label"] = m["volume"]
    chunk["volume_db"] = m["db"]
    chunk["emphasis_words"] = m.get("emphasis") or ""
    chunk["pause_before_ms"] = extra.get("pauseBefore", 200 if profile in ("choice", "clue") else 0)
    chunk["pause_after_ms"] = m["pause"]
    chunk["pause_sentence_ms"] = m["sentence"]
    chunk["style_energy"] = m["energy"]
    chunk["style_contour"] = m["contour"]
    chunk["noise_scale_piper"] = m["noise"]
    chunk["kokoro_speed"] = m["speed"]
    chunk["melo_speed"] = m["speed"]
    chunk["espeak_amp"] = 82 if m["volume"] == "soft" else 100
    chunk["espeak_pitch"] = 42 if m["pitch"] == "low" else 50
    chunk["espeak_word_gap"] = 12 if m["rate"] == "slow" else 10
    note = extra.get("notes", m["note"])
    chunk["notes"] = note
    chunk["night_policy"] = "play"
    chunk["locale"] = "fr-FR"
    chunk["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        chunk[k] = v


def t1_passage(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            "narrateur|Mila pousse la porte de la cuisine.",
            "narrateur|Le carrelage colle un peu, sous ses pieds.",
            "enfant-f|Bonjour, l'assiette !",
            "narrateur|Papa a la tête dans le placard.",
            "narrateur|Maman compte les bols, à voix haute.",
            "narrateur|Les mots de Mila tombent par terre.",
            "enfant-f|Papa, l'assiette bleue !",
            "narrateur|Personne ne se tourne.",
            "narrateur|Mila serre la pomme, étoile contre la paume.",
            "narrateur|Dans sa poitrine, ça pousse fort.",
            "narrateur|Elle attend, près de la table.",
            "papa|Oui ?",
            "enfant-f|Bonjour, papa.",
            "enfant-f|L'assiette bleue, s'il te plaît.",
            "papa|Je t'écoute.",
            "narrateur|Papa ouvre un tiroir, puis l'autre.",
            "narrateur|Des bols, pas d'assiette bleue.",
            "maman|Elle n'est pas là.",
        )
    if a == 2:
        return L(
            "narrateur|Mila court vers la haie, pomme au creux.",
            "enfant-f|Nina, Nina !",
            "narrateur|La haie ne répond pas.",
            "narrateur|Papa parle du panier, à maman.",
            "enfant-f|Le panier, vite !",
            "narrateur|Ses mots se mêlent aux branches.",
            "narrateur|Mila s'arrête.",
            "narrateur|Ses joues chauffent.",
            "narrateur|Elle pose la pomme sur une latte sèche.",
            "enfant-f|Bonjour, haie.",
            "enfant-f|Nina, s'il te plaît.",
            "narrateur|Personne.",
            "narrateur|Un oiseau, seulement.",
            "papa|Je t'écoute, Mila.",
            "enfant-f|Nina n'est pas là.",
            "maman|Le panier est vide, anse fendue.",
            "narrateur|L'étoile brune regarde le ciel.",
        )
    return L(
        "narrateur|Mila pousse la porte de la chambre.",
        "enfant-f|La serviette !",
        "narrateur|Maman plie des chaussettes, et parle.",
        "narrateur|Papa répond, depuis le couloir.",
        "narrateur|Mila veut parler par-dessus le linge.",
        "enfant-f|La serviette au point rouge !",
        "narrateur|Les mots se perdent dans le coton.",
        "narrateur|Mila referme la bouche, près du lit.",
        "enfant-f|Bonjour, maman.",
        "enfant-f|La serviette, s'il te plaît.",
        "maman|Je t'écoute.",
        "narrateur|Maman ouvre le tiroir du bas.",
        "narrateur|Des chaussettes, pas de serviette.",
        "papa|Elle n'est pas là.",
        "enfant-f|Nina va arriver, sans nappe.",
        "narrateur|La pomme attend, étoile vers le plafond.",
    )


def t1_q(a: int) -> tuple[list[tuple[str, str]], dict]:
    if a == 1:
        return L(
            "narrateur|Sur la table, la pomme attend.",
            "papa|Qu'est-ce qui manque, pour Nina ?",
        ), dict(
            expected_answer="assiette",
            accepted_examples="assiette | l'assiette | assiette bleue | la bleue | le plat",
            retry_prompt="Regarde la table. Qu'est-ce qui manque ?",
            engine_ok_text="Oui, l'assiette bleue.",
            engine_near_text="Tu es proche. Écoute l'indice.",
        )
    if a == 2:
        return L(
            "narrateur|Devant la haie, ça reste silencieux.",
            "maman|Qui n'est pas là ?",
        ), dict(
            expected_answer="Nina",
            accepted_examples="Nina | nina | l'amie | copine | la copine",
            retry_prompt="Mila a appelé. Qui n'a pas répondu ?",
            engine_ok_text="Oui, Nina.",
            engine_near_text="Tu es proche. Écoute l'indice.",
        )
    return L(
        "narrateur|Le tiroir sent le coton propre.",
        "papa|On cherche quoi, pour la table ?",
    ), dict(
        expected_answer="serviette",
        accepted_examples="serviette | la serviette | nappe | la nappe | le linge",
        retry_prompt="Dans le tiroir, on cherche quel linge ?",
        engine_ok_text="Oui, la serviette.",
        engine_near_text="Tu es proche. Écoute l'indice.",
    )


def t1_confirm(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            "enfant-f|L'assiette bleue !",
            "narrateur|Oui, l'assiette bleue.",
            "papa|Merci, Mila.",
            "papa|J'ai entendu toute ta phrase.",
            "narrateur|La pomme garde son étoile, vers le haut.",
            "maman|On cherche, sans se presser.",
        )
    if a == 2:
        return L(
            "enfant-f|Nina !",
            "narrateur|Oui, Nina n'est pas là.",
            "papa|Merci, Mila.",
            "papa|J'ai entendu toute ta phrase.",
            "narrateur|L'étoile brune reste tournée vers le ciel.",
            "maman|On cherche, sans se presser.",
        )
    return L(
        "enfant-f|La serviette !",
        "narrateur|Oui, la serviette au point rouge.",
        "maman|Merci, Mila.",
        "maman|J'ai entendu ta phrase.",
        "narrateur|La pomme attend, étoile vers le plafond.",
        "papa|On cherche, sans se presser.",
    )


def t2_passage(a: int, b: int) -> list[tuple[str, str]]:
    """Revers allongé : 2e ruse, l'enfant refuse de foncer, retrouve l'étoile."""
    if (a, b) == (1, 1):
        return L(
            "narrateur|En attendant, Mila sort les cubes.",
            "narrateur|Un cube rouge sent le pin.",
            "enfant-f|Un pont, pour la pomme !",
            "papa|Attends, je compte les bols.",
            "narrateur|Deux voix partent ensemble.",
            "narrateur|Le pont penche.",
            "narrateur|La pomme glisse vers le bord.",
            "enfant-f|Elle tombe !",
            "narrateur|Mila attrape, trop vite.",
            "narrateur|L'étoile se cache contre la table.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Mila s'arrête, au lieu de courir.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Je finis les bols.",
            "enfant-f|Quand tu as fini, le pont.",
            "papa|Voilà, je t'écoute.",
            "narrateur|Mila retourne la pomme, étoile en haut.",
            "enfant-f|Comme ça, ça ne roule plus.",
            "narrateur|Papa pose un cube, puis Mila.",
            "narrateur|Le pont tient, petit et droit.",
            "maman|L'assiette n'est pas dans les bols.",
        )
    if (a, b) == (1, 2):
        return L(
            "narrateur|Mila ouvre le livre du pique-nique.",
            "narrateur|Une pomme dessinée a une tache.",
            "enfant-f|C'est la mienne !",
            "maman|Attends, je cherche l'assiette.",
            "narrateur|Deux mains veulent la page.",
            "narrateur|Le papier claque.",
            "narrateur|La pomme vraie roule vers le livre.",
            "enfant-f|Non !",
            "narrateur|Mila la rattrape, le cœur serré.",
            "narrateur|L'étoile se cache sous une page.",
            "narrateur|Elle pose les mains, sans se précipiter.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "enfant-f|S'il te plaît, une page.",
            "maman|Une page, puis toi.",
            "narrateur|Sous le dessin, l'étoile brune revient.",
            "enfant-f|Elle montre l'assiette, dans le livre.",
            "papa|Je vois le dessin, maintenant.",
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Mila écoute la cuisine, tiroir après tiroir.",
            "maman|L'assiette vraie n'est pas dans le livre.",
        )
    if (a, b) == (1, 3):
        return L(
            "narrateur|Mila pose la dînette sur la table.",
            "narrateur|La théière penche, un peu trop.",
            "enfant-f|Le goûter de Nina, tout de suite !",
            "papa|Je cherche, Mila.",
            "narrateur|Deux voix se mêlent aux tasses.",
            "narrateur|Un peu d'eau glisse vers la pomme.",
            "enfant-f|Ma pomme !",
            "narrateur|Mila tire la théière, trop fort.",
            "narrateur|L'étoile se mouille, puis s'efface un peu.",
            "narrateur|Le sourire disparaît.",
            "narrateur|Elle attend, au lieu de verser.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "enfant-f|La tasse, s'il te plaît.",
            "papa|La tasse, puis on écoute.",
            "narrateur|Mila essuie l'étoile, tout contre sa manche.",
            "enfant-f|La place de Nina est vide.",
            "maman|Une vraie assiette manque, pas une tasse.",
            "narrateur|Mila pose la pomme, étoile vers Nina.",
            "narrateur|La dînette se tait.",
            "papa|On cherche l'assiette, ensemble.",
        )
    if (a, b) == (2, 1):
        return L(
            "narrateur|Mila aligne des cubes, sur le banc.",
            "narrateur|Le bois mouillé fait glisser le rouge.",
            "enfant-f|Un trône, pour la pomme !",
            "papa|Attention, la latte est humide.",
            "narrateur|Maman parle du panier, en même temps.",
            "narrateur|Deux voix, et les cubes tombent.",
            "narrateur|La pomme roule vers l'herbe.",
            "enfant-f|L'étoile !",
            "narrateur|Mila s'élance, puis s'arrête.",
            "narrateur|Dans sa poitrine, envie et peur se bousculent.",
            "narrateur|Elle regarde l'étoile, sans bouger.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "enfant-f|S'il te plaît, une latte sèche.",
            "papa|Celle du bout, vois-tu ?",
            "narrateur|Mila pose l'étoile vers le ciel.",
            "narrateur|Un cube tient, sur le bois moins mouillé.",
            "enfant-f|Nina n'a pas son trône.",
            "maman|Nina n'a pas entendu, non plus.",
            "narrateur|Le panier vide attend, anse fendue.",
            "papa|On appelle, un par un.",
        )
    if (a, b) == (2, 2):
        return L(
            "narrateur|Mila ouvre le livre, sur une latte sèche.",
            "narrateur|Le vent tourne une page, tout seul.",
            "enfant-f|Nina est dans le livre !",
            "maman|Regarde, une haie dessinée.",
            "papa|Moi, je vois un panier.",
            "narrateur|Deux doigts veulent la même page.",
            "narrateur|Le livre claque, près de la pomme.",
            "narrateur|L'étoile se cache sous la couverture.",
            "enfant-f|Je ne vois plus l'étoile !",
            "narrateur|Mila veut crier vers la haie.",
            "narrateur|Elle garde la pomme, sans crier.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "enfant-f|S'il te plaît, ta page d'abord.",
            "maman|Puis la tienne.",
            "narrateur|Sous une feuille, l'étoile brune revient.",
            "enfant-f|Le dessin montre une fille, derrière la haie.",
            "papa|Peut-être la vraie Nina, au même endroit.",
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Mila écoute le jardin, pas seulement le livre.",
            "narrateur|La haie reste silencieuse.",
        )
    if (a, b) == (2, 3):
        return L(
            "narrateur|Mila pose la dînette, sur le banc mouillé.",
            "narrateur|Une tasse glisse, toc contre le bois.",
            "enfant-f|La place de Nina, là !",
            "papa|Le bois est trop humide.",
            "maman|Le panier penche, lui aussi.",
            "narrateur|Deux voix, et la tasse tombe.",
            "narrateur|Un peu d'eau touche la pomme.",
            "enfant-f|Elle va rouler !",
            "narrateur|Mila attrape, le souffle court.",
            "narrateur|L'étoile se cache contre une latte.",
            "narrateur|Mila souffle, puis elle s'arrête.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "enfant-f|La tasse, s'il te plaît, sur la latte sèche.",
            "papa|D'accord.",
            "narrateur|Mila tourne la pomme, étoile vers la haie.",
            "enfant-f|Nina, s'il te plaît.",
            "narrateur|La haie ne répond pas.",
            "maman|Le panier vide écoute, lui aussi.",
            "narrateur|Une tasse attend, vide, pour Nina.",
            "papa|On cherche, sans crier.",
        )
    if (a, b) == (3, 1):
        return L(
            "narrateur|Mila bâtit une tour, sur le tapis.",
            "narrateur|Un cube bleu sent le bois sec.",
            "enfant-f|Un lit, pour la pomme !",
            "maman|J'ai une chaussette, pas la serviette.",
            "papa|Le tiroir du haut, peut-être.",
            "narrateur|Deux voix, et la tour penche.",
            "narrateur|La pomme roule vers le lit.",
            "enfant-f|L'étoile !",
            "narrateur|Mila court, puis s'arrête.",
            "narrateur|Le sourire a disparu.",
            "narrateur|Elle ne court pas vers le lit.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "enfant-f|Quand tu as fini, le cube bleu.",
            "maman|Voilà, je t'écoute.",
            "narrateur|Mila pose l'étoile vers le plafond.",
            "enfant-f|Comme ça, elle reste.",
            "narrateur|Papa pose un cube, puis Mila.",
            "narrateur|La petite tour tient.",
            "maman|La serviette n'est pas sous les cubes.",
            "papa|On cherche le point rouge, ensemble.",
        )
    if (a, b) == (3, 2):
        return L(
            "narrateur|Mila ouvre le livre, sur le lit.",
            "narrateur|Une nappe dessinée a un point rouge.",
            "enfant-f|C'est la nôtre !",
            "maman|Attends, je plie cette chaussette.",
            "narrateur|Deux mains veulent tourner.",
            "narrateur|Une page claque près de la pomme.",
            "narrateur|L'étoile se cache sous l'oreiller.",
            "enfant-f|Je ne la vois plus !",
            "narrateur|Mila veut parler par-dessus le linge.",
            "narrateur|Mila pose un pied, puis l'autre.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "enfant-f|S'il te plaît, une page.",
            "papa|Une page, puis toi.",
            "narrateur|Sous l'oreiller, l'étoile brune revient.",
            "enfant-f|Le dessin montre un tiroir ouvert.",
            "maman|Le nôtre, peut-être.",
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Mila écoute le tiroir, pas seulement le livre.",
            "narrateur|Le tiroir sent le coton.",
            "papa|On ouvre, un tiroir après l'autre.",
        )
    return L(
        "narrateur|Mila pose la dînette, près du lit.",
        "narrateur|Une soucoupe penche sur le tapis.",
        "enfant-f|La nappe, tout de suite !",
        "maman|Je plie, Mila.",
        "papa|Le couloir, je cherche.",
        "narrateur|Deux voix, et la soucoupe glisse.",
        "narrateur|Elle tape la pomme, toc.",
        "enfant-f|Ma pomme !",
        "narrateur|Mila attrape, trop vite.",
        "narrateur|L'étoile se cache sous une chaussette.",
        "narrateur|Cette fois, elle refuse de foncer.",
        "narrateur|Maman s'accroupit, à sa hauteur.",
        "enfant-f|La soucoupe, s'il te plaît.",
        "maman|La soucoupe, puis on écoute.",
        "narrateur|Mila dégage l'étoile, tout contre le tapis.",
        "enfant-f|Nina n'a pas de nappe.",
        "papa|La vraie serviette manque, pas la soucoupe.",
        "narrateur|Mila pose la pomme, étoile vers le tiroir.",
        "narrateur|La dînette se tait.",
        "maman|On cherche le point rouge, ensemble.",
    )


def t3_q(c_unused: int = 0) -> list[tuple[str, str]]:
    return L(
        "narrateur|Le goûter peut attendre un peu.",
        "papa|Le matin, après la sieste, ou le soir ?",
    )


TIME = {
    1: "Le matin, le banc fume un peu.",
    2: "Après la sieste, la maison est tiède.",
    3: "Le soir, une lampe allume l'étoile.",
}

FIND = {
    (1, 1): (
        "Derrière le bocal, l'assiette bleue brille.",
        "Mila la montre, sans crier.",
        "enfant-f|L'assiette, s'il te plaît.",
        "papa|La voilà.",
    ),
    (1, 2): (
        "Sous la nappe pliée, l'assiette bleue attend.",
        "Mila pose un doigt dessus, puis attend.",
        "enfant-f|L'assiette, s'il te plaît.",
        "maman|Je te la tends.",
    ),
    (1, 3): (
        "Près de la lampe, l'assiette bleue luit.",
        "Mila ouvre la bouche, puis s'arrête.",
        "enfant-f|Bonjour, assiette.",
        "papa|Je t'écoute.",
    ),
    (2, 1): (
        "Derrière la haie, une voix répond.",
        "copine|Bonjour, Mila.",
        "enfant-f|Bonjour, Nina.",
        "enfant-f|S'il te plaît, viens.",
    ),
    (2, 2): (
        "Près du panier, Nina cligne des yeux.",
        "copine|J'étais là, derrière.",
        "enfant-f|Bonjour, Nina.",
        "enfant-f|On t'attendait, s'il te plaît.",
    ),
    (2, 3): (
        "Sous la lampe du jardin, Nina arrive.",
        "copine|Bonjour.",
        "enfant-f|Bonjour, Nina.",
        "papa|On t'écoute, les deux.",
    ),
    (3, 1): (
        "Sur la chaise, la serviette attend.",
        "Le point rouge luit au soleil.",
        "enfant-f|La serviette, s'il te plaît.",
        "maman|La voilà.",
    ),
    (3, 2): (
        "Sous l'oreiller, le point rouge dépasse.",
        "Mila attend que maman finisse.",
        "enfant-f|La serviette, s'il te plaît.",
        "maman|Je te la donne.",
    ),
    (3, 3): (
        "Près de la lampe, le point rouge s'allume.",
        "Mila ne fonce pas.",
        "enfant-f|Bonjour, serviette.",
        "papa|Je t'écoute, alors.",
    ),
}

GAME = {
    1: (
        "Mila pose un cube, puis papa.",
        "L'étoile s'assoit au creux du bois.",
    ),
    2: (
        "Mila garde le livre ouvert, à la bonne page.",
        "L'étoile du dessin regarde la vraie.",
    ),
    3: (
        "Mila laisse une tasse vide, pour Nina.",
        "L'étoile regarde la place vide.",
    ),
}

CALLBACKS = {
    (1, 1, 1): "L'assiette bleue tient l'étoile, au matin.",
    (1, 1, 2): "L'assiette bleue tient l'étoile, après la sieste.",
    (1, 1, 3): "L'assiette bleue tient l'étoile, sous la lampe.",
    (1, 2, 1): "Le livre reste ouvert, près de l'assiette.",
    (1, 2, 2): "Le livre reste ouvert, sur la nappe tiède.",
    (1, 2, 3): "Le livre reste ouvert, sous la lampe.",
    (1, 3, 1): "Une tasse de dînette veille près de l'assiette.",
    (1, 3, 2): "Une tasse de dînette veille, après la sieste.",
    (1, 3, 3): "Une tasse de dînette veille, le soir.",
    (2, 1, 1): "Nina touche le cube, puis l'étoile.",
    (2, 1, 2): "Nina pose un cube, tout contre l'étoile.",
    (2, 1, 3): "Nina pose un cube, sous la lampe.",
    (2, 2, 1): "Nina reconnaît l'étoile du livre, au jardin.",
    (2, 2, 2): "Nina reconnaît l'étoile du livre, tout endormie.",
    (2, 2, 3): "Nina reconnaît l'étoile du livre, le soir.",
    (2, 3, 1): "Nina s'assoit devant la tasse vide, au matin.",
    (2, 3, 2): "Nina s'assoit devant la tasse vide, sans bruit.",
    (2, 3, 3): "Nina s'assoit devant la tasse vide, le soir.",
    (3, 1, 1): "Le point rouge borde l'étoile, au matin.",
    (3, 1, 2): "Le point rouge borde l'étoile, après la sieste.",
    (3, 1, 3): "Le point rouge borde l'étoile, sous la lampe.",
    (3, 2, 1): "Le livre et la serviette gardent l'étoile.",
    (3, 2, 2): "Le livre et la serviette gardent l'étoile tiède.",
    (3, 2, 3): "Le livre et la serviette gardent l'étoile, le soir.",
    (3, 3, 1): "La soucoupe et la serviette encadrent l'étoile.",
    (3, 3, 2): "La soucoupe et la serviette encadrent l'étoile tiède.",
    (3, 3, 3): "La soucoupe et la serviette encadrent l'étoile, le soir.",
}


def t3_passage(a: int, b: int, c: int) -> list[tuple[str, str]]:
    find = FIND[(a, c)]
    g1, g2 = GAME[b]
    roles = {"papa", "maman", "enfant-f", "copine", "narrateur"}
    clean = [f"narrateur|{TIME[c]}"]
    for piece in find:
        if "|" in piece and piece.split("|", 1)[0] in roles:
            clean.append(piece)
        else:
            clean.append(f"narrateur|{piece}")
    clean.extend([
        f"narrateur|{g1}",
        f"narrateur|{g2}",
        "enfant-f|Merci.",
        f"narrateur|{CALLBACKS[(a, b, c)]}",
    ])
    return L(*clean)


CHILD1 = {
    (1, 1, 1): "L'assiette a dit oui, au matin.",
    (1, 1, 2): "L'assiette a dit oui, après la sieste.",
    (1, 1, 3): "L'assiette a dit oui, le soir.",
    (1, 2, 1): "Le livre a montré l'assiette.",
    (1, 2, 2): "Le livre a montré l'assiette tiède.",
    (1, 2, 3): "Le livre a montré l'assiette, sous la lampe.",
    (1, 3, 1): "La dînette a gardé une place.",
    (1, 3, 2): "La dînette a gardé une place tiède.",
    (1, 3, 3): "La dînette a gardé une place, le soir.",
    (2, 1, 1): "Nina a trouvé le cube, et l'étoile.",
    (2, 1, 2): "Nina a trouvé le cube, tout endormie.",
    (2, 1, 3): "Nina a trouvé le cube, sous la lampe.",
    (2, 2, 1): "Nina était dans le jardin, pas le livre.",
    (2, 2, 2): "Nina était derrière la haie, après la sieste.",
    (2, 2, 3): "Nina était sous la lampe, près du panier.",
    (2, 3, 1): "Nina a pris la tasse vide, au matin.",
    (2, 3, 2): "Nina a pris la tasse vide, sans bruit.",
    (2, 3, 3): "Nina a pris la tasse vide, le soir.",
    (3, 1, 1): "La serviette a rejoint le cube.",
    (3, 1, 2): "La serviette a rejoint le cube tiède.",
    (3, 1, 3): "La serviette a rejoint le cube, le soir.",
    (3, 2, 1): "La serviette a rejoint le livre.",
    (3, 2, 2): "La serviette a rejoint le livre, après la sieste.",
    (3, 2, 3): "La serviette a rejoint le livre, sous la lampe.",
    (3, 3, 1): "La serviette a rejoint la soucoupe.",
    (3, 3, 2): "La serviette a rejoint la soucoupe tiède.",
    (3, 3, 3): "La serviette a rejoint la soucoupe, le soir.",
}

CHILD2 = {
    (1, 1, 1): "Papa a entendu s'il te plaît.",
    (1, 1, 2): "J'ai attendu, puis l'assiette est venue.",
    (1, 1, 3): "L'étoile ne roulait plus, sur l'assiette.",
    (1, 2, 1): "Une page, puis l'autre.",
    (1, 2, 2): "Le dessin avait froid, comme ma pomme.",
    (1, 2, 3): "La lampe a montré la tache brune.",
    (1, 3, 1): "L'eau n'a pas pris ma pomme.",
    (1, 3, 2): "La tasse vide a attendu Nina.",
    (1, 3, 3): "Le soir, la dînette s'est tue.",
    (2, 1, 1): "La latte sèche a gardé le cube.",
    (2, 1, 2): "Le banc mouillé a laissé une latte.",
    (2, 1, 3): "Le cube a tenu, sous la lampe.",
    (2, 2, 1): "Le vent a tourné, puis on a lu.",
    (2, 2, 2): "La haie a répondu, après la sieste.",
    (2, 2, 3): "Le livre a montré la haie, le soir.",
    (2, 3, 1): "La tasse a fait toc, puis elle s'est arrêtée.",
    (2, 3, 2): "Le banc a gardé une tasse, pour Nina.",
    (2, 3, 3): "La tasse vide a brillé, le soir.",
    (3, 1, 1): "La tour n'est pas tombée, à la fin.",
    (3, 1, 2): "Le cube bleu a senti le coton.",
    (3, 1, 3): "Le plafond a regardé l'étoile.",
    (3, 2, 1): "Une page, puis le tiroir.",
    (3, 2, 2): "L'oreiller a rendu l'étoile.",
    (3, 2, 3): "Le point rouge s'est allumé, le soir.",
    (3, 3, 1): "La soucoupe a dit toc, puis merci.",
    (3, 3, 2): "Le tapis a gardé la pomme.",
    (3, 3, 3): "La dînette s'est tue, près de la lampe.",
}

LAST = {
    (1, 1, 1): "L'étoile sèche sur l'assiette du matin.",
    (1, 1, 2): "L'étoile sèche sur l'assiette de la sieste.",
    (1, 1, 3): "L'étoile luit sur l'assiette du soir.",
    (1, 2, 1): "Le livre reste ouvert, pomme au creux de l'assiette.",
    (1, 2, 2): "Le livre tiède touche l'assiette, étoile vers le haut.",
    (1, 2, 3): "Le livre et l'assiette se taisent, sous la lampe.",
    (1, 3, 1): "Une tasse vide veille, près de l'assiette du matin.",
    (1, 3, 2): "Une tasse vide veille, près de l'assiette tiède.",
    (1, 3, 3): "Une tasse vide veille, près de l'assiette du soir.",
    (2, 1, 1): "Le cube et l'étoile restent sur le banc.",
    (2, 1, 2): "Le cube tiède touche l'étoile du banc.",
    (2, 1, 3): "Le cube luit sous la lampe du banc.",
    (2, 2, 1): "Le livre ferme sa haie, l'étoile reste au jardin.",
    (2, 2, 2): "Le livre s'endort, l'étoile reste contre Nina.",
    (2, 2, 3): "Le livre se ferme, l'étoile reste au jardin.",
    (2, 3, 1): "La tasse vide sèche, sur une latte du banc.",
    (2, 3, 2): "La tasse vide sèche, près du panier fendu.",
    (2, 3, 3): "La tasse vide sèche, sous la lampe du pommier.",
    (3, 1, 1): "Le point rouge borde l'étoile du matin.",
    (3, 1, 2): "Le point rouge borde l'étoile du tapis tiède.",
    (3, 1, 3): "Le point rouge borde l'étoile de la chambre.",
    (3, 2, 1): "Livre et serviette gardent l'étoile, près du lit.",
    (3, 2, 2): "Livre et serviette gardent l'étoile de la sieste.",
    (3, 2, 3): "Le livre et la serviette gardent l'étoile, le soir.",
    (3, 3, 1): "La soucoupe et la serviette encadrent l'étoile du matin.",
    (3, 3, 2): "La soucoupe et la serviette encadrent l'étoile tiède.",
    (3, 3, 3): "La soucoupe et la serviette encadrent l'étoile du soir.",
}

RETURN = {
    1: "Au seuil, le banc du pommier fume un peu.",
    2: "Près de la porte, le bois du banc a séché.",
    3: "Sous la lampe, le banc du pommier se tait.",
}

KEEP = {
    1: "L'assiette bleue reste, avec une goutte de jus.",
    2: "Nina garde un bout d'étoile, dans la main.",
    3: "La serviette au point rouge a une ride de pomme.",
}


def ending(a: int, b: int, c: int) -> list[tuple[str, str]]:
    key = (a, b, c)
    lines = [
        f"narrateur|{RETURN[c]}",
        "maman|À toi, Mila.",
        "maman|Nous t'écoutons.",
        f"enfant-f|{CHILD1[key]}",
        f"enfant-f|{CHILD2[key]}",
    ]
    if a == 2:
        lines.append("copine|Merci, Mila.")
    else:
        lines.append("copine|Bonjour, et merci.")
    lines.extend([
        f"narrateur|{KEEP[a]}",
        f"narrateur|{LAST[key]}",
    ])
    return L(*lines)


def _check_maps() -> None:
    for dname, d in (
        ("CALLBACKS", CALLBACKS),
        ("CHILD1", CHILD1),
        ("CHILD2", CHILD2),
        ("LAST", LAST),
    ):
        if len(d) != 27:
            raise SystemExit(f"{dname} {len(d)}")
        for k, s in d.items():
            n = wc(s)
            if n > LIM:
                raise SystemExit(f"{dname} {k} {n}>10: {s}")
            marks = s.count(".") + s.count("?") + s.count("!")
            if marks != 1:
                raise SystemExit(f"{dname} {k} punct {marks}: {s}")
            if TICS.search(s):
                raise SystemExit(f"{dname} tic: {s}")
    for k, s in list(TIME.items()) + list(KEEP.items()) + list(RETURN.items()):
        if wc(s) > LIM:
            raise SystemExit(f"map {n if False else wc(s)}>10: {s}")
        if TICS.search(s):
            raise SystemExit(f"tic map: {s}")
    for pair in GAME.values():
        for s in pair:
            if wc(s) > LIM or TICS.search(s):
                raise SystemExit(f"GAME: {s}")
    for tup in FIND.values():
        for s in tup:
            ph = s.split("|", 1)[-1]
            if wc(ph) > LIM:
                raise SystemExit(f"FIND {wc(ph)}>10: {ph}")
            if TICS.search(ph):
                raise SystemExit(f"FIND tic: {ph}")


def main() -> None:
    _check_maps()
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: deepcopy(c) for c in src["chunks"]}

    voice(
        by["CHK_T0000_P0000"],
        L(
            "narrateur|Le banc de bois fume un peu.",
            "narrateur|Une goutte tape une latte, toc.",
            "narrateur|Ça sent l'écorce mouillée, et le sucré.",
            "narrateur|Sous le pommier, une pomme jaune attend.",
            "narrateur|Sur sa joue, une étoile brune.",
            "narrateur|Le panier d'osier penche, anse fendue.",
            "narrateur|La porte de la maison reste ouverte.",
            "narrateur|Du tiroir, un bruit de vaisselle.",
            "narrateur|Papa cherche, maman plie un torchon.",
            "narrateur|En ce moment, Mila tend la main.",
            "enfant-f|La pomme, vite, pour Nina !",
            "narrateur|Elle s'assoit trop vite, sur le banc.",
            "narrateur|Le bois mouillé glisse sous son short.",
            "narrateur|La pomme roule, étoile contre l'herbe.",
            "enfant-f|Papa !",
            "narrateur|Papa parle du tiroir, à maman.",
            "papa|Tu disais, Mila ?",
            "narrateur|Mila ouvre la bouche, puis s'arrête.",
            "narrateur|Dans sa poitrine, ça pousse fort.",
            "narrateur|Elle ramasse la pomme, sans crier.",
            "enfant-f|S'il te plaît, la pomme pour Nina.",
            "papa|Je t'écoute, maintenant.",
            "maman|L'assiette bleue manque, pour le goûter.",
        ),
        "opening",
        extra={"sons": "goutte,pommier"},
    )

    voice(
        by["CHK_T0001_P0000"],
        L(
            "narrateur|Il manque l'assiette, pour la pomme.",
            "maman|On cherche où ?",
            "papa|La cuisine, le jardin, ou la chambre ?",
        ),
        "choice",
        extra={
            "fields": {
                "option_1_label": "la cuisine",
                "option_2_label": "le jardin",
                "option_3_label": "la chambre",
            }
        },
    )

    t1_sons = {1: "tiroir,assiette", 2: "haie,oiseau", 3: "tiroir,coton"}
    t1_emp = {1: "assiette", 2: "Nina", 3: "serviette"}
    t2_sons = {1: "cubes", 2: "pages", 3: "tasse"}
    t2_emp = {1: "cubes", 2: "livre", 3: "dînette"}
    t3_emp = {1: "étoile", 2: "étoile", 3: "étoile"}
    fin_sons = {1: "oiseau,pommier", 2: "silence,pommier", 3: "lampe,pommier"}

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        voice(by[base], t1_passage(a), "action", extra={"sons": t1_sons[a], "emphasis": t1_emp[a]})
        q_lines, q_fields = t1_q(a)
        voice(
            by[f"{base}_Q0001"],
            q_lines,
            "clue",
            extra={"emphasis": t1_emp[a], "fields": q_fields},
        )
        voice(by[f"{base}_C0001"], t1_confirm(a), "confirm", extra={"emphasis": t1_emp[a]})
        voice(
            by[f"{base}_T0002_P0000"],
            L(
                "narrateur|On peut jouer, le temps de chercher.",
                "maman|Les cubes, le livre, ou la dînette ?",
            ),
            "choice",
            extra={
                "fields": {
                    "option_1_label": "les cubes",
                    "option_2_label": "le livre",
                    "option_3_label": "la dînette",
                }
            },
        )
        for b in (1, 2, 3):
            loc_id = f"{base}_T0002_P000{b}"
            voice(
                by[loc_id],
                t2_passage(a, b),
                "obstacle",
                extra={
                    "sons": t2_sons[b],
                    "emphasis": t2_emp[b],
                    "notes": PROFILES["obstacle"]["note"] + f"; revers=2e_ruse; lieu={a}; jeu={b}",
                },
            )
            voice(
                by[f"{loc_id}_T0003_P0000"],
                t3_q(),
                "choice",
                extra={
                    "fields": {
                        "option_1_label": "le matin",
                        "option_2_label": "après la sieste",
                        "option_3_label": "le soir",
                    }
                },
            )
            for c in (1, 2, 3):
                leaf = f"{loc_id}_T0003_P000{c}"
                voice(
                    by[leaf],
                    t3_passage(a, b, c),
                    "resolution",
                    extra={"sons": t2_sons[b], "emphasis": t3_emp[c]},
                )
                voice(
                    by[f"{leaf}_F0001"],
                    ending(a, b, c),
                    "ending",
                    extra={"sons": fin_sons[c], "emphasis": "étoile"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra_ids = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    fins = [by[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(fins) != 27:
        raise SystemExit(f"fins {len(fins)}")
    if len(set(fins)) != 27:
        raise SystemExit("fins non distinctes")

    t2s = [
        by[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c.get("kind") == "passage"
        and "_T0002_P000" in c["chunk_id"]
        and "_T0003_" not in c["chunk_id"]
        and not c["chunk_id"].endswith("_P0000")
    ]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"T2 distincts: {len(set(t2s))}/{len(t2s)}")

    t3s = [
        by[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c.get("kind") == "passage"
        and "_T0003_P000" in c["chunk_id"]
        and not c["chunk_id"].endswith("_P0000")
        and "_F0001" not in c["chunk_id"]
    ]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"T3 distincts: {len(set(t3s))}/{len(t3s)}")

    out = dict(src)
    out["fil_rouge"] = (
        "Sous le pommier, le banc de bois fume après la pluie. "
        "Mila veut porter sa pomme jaune à étoile brune jusqu'au goûter de Nina. "
        "Elle s'assoit trop vite : la pomme roule, papa n'entend pas. "
        "L'assiette bleue manque. Cuisine, jardin ou chambre changent la recherche. "
        "Cubes, livre ou dînette allongent le revers : l'étoile se cache, "
        "Mila refuse de foncer. Matin, sieste ou soir paient l'étoile. "
        "Le banc, la pomme et le mot merci reviennent."
    )
    out["title"] = TITLE
    out["characters"] = "Mila, Nina, papa, maman"
    out["setting"] = "jardin sous le pommier, banc de bois, puis la maison"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]

    joined = "\n".join(c["script"] for c in out["chunks"])
    if TICS.search(joined):
        raise SystemExit(f"tic global: {TICS.search(joined).group(0)}")
    for bad in ("aujourd'hui,", "mission accomplie", "j'ai compris", "on va apprendre", "voici le geste"):
        if bad in joined.lower():
            raise SystemExit(f"interdit: {bad}")

    check(SID, out["age_band"], out["chunks"])

    def path_words(a: int, b: int, c: int) -> int:
        ids = [
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
        return sum(wc(by[i]["text"]) for i in ids)

    pw = [path_words(a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    lo, hi, avg = min(pw), max(pw), sum(pw) // len(pw)
    print(f"chemins {lo}-{hi} mots, moy {avg}")
    if lo < 420:
        raise SystemExit(f"chemins trop courts: {lo}")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés. Graphe source conservé "
        "(cuisine / jardin / chambre ; cubes / livre / dînette ; "
        "matin / après la sieste / soir).\n\n"
        "## Promesse narrative\n\n"
        "Sous le pommier, le banc de bois fume après la pluie. Une goutte "
        "tape une latte, toc. Mila veut porter sa pomme jaune à étoile brune "
        "jusqu'au goûter de Nina, maintenant. Elle s'assoit trop vite : le bois "
        "glisse, la pomme roule, étoile contre l'herbe, et papa n'entend pas. "
        "L'assiette bleue manque. Cuisine (tiroir, bols), jardin (haie, panier "
        "fendu, Nina absente) ou chambre (serviette au point rouge) changent "
        "la recherche. Cubes, livre ou dînette allongent le revers : deux voix, "
        "l'étoile se cache, Mila refuse de foncer, un adulte s'accroupit. "
        "Matin, sieste ou soir paient l'étoile. Le banc, la pomme et le merci "
        "reviennent, sans morale.\n\n"
        "## Vécu\n\n"
        "- Désir : porter la pomme jaune à étoile jusqu'au goûter de Nina.\n"
        "- Imprévu 1 : banc mouillé, pomme qui roule, parole coupée.\n"
        "- Imprévu 2 (revers allongé) : cubes / livre / dînette, deux voix, "
        "étoile cachée, Mila refuse de foncer.\n"
        "- COL.POL.001 vécu : bonjour en entrant, s'il te plaît pour l'objet "
        "manquant, merci quand la phrase arrive. Jamais dite comme règle.\n"
        "- Tours de parole : envie de couper, retenue, écoute réelle, plaisir "
        "d'être entendu. Nuance : à la dînette l'eau menace, elle arrête.\n"
        f"- 27 fins distinctes. Chemins {lo}–{hi} mots (moyenne {avg}).\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Troupe D16 : Mila, Nina, papa, maman.\n"
        "- 86 nœuds, graphe et libellés d'options conservés.\n"
        "- 27 fins, 27 T3, 9 T2 textuellement distincts.\n"
        "- Première tentative échoue. Chaque choix change l'obstacle, le climax, la dernière image.\n"
        "- Objet nommé : pomme jaune à étoile brune (couleur, poids, toc, mission).\n"
        "- Coin inventif : le banc du pommier (bois, vapeur, latte sèche).\n"
        "- Monde ≠ TREE-COL-002 (banc de fer, clapet, platane, Amir).\n"
        "- Indice unique dès l'ouverture : étoile brune, payée au climax.\n"
        "- Déclencheur : un objet ou un invité manque (assiette / Nina / serviette).\n"
        "- TTS par fonction (ouverture, choix, indice, confirmation, action, obstacle, résolution, retour).\n"
        "- `slow` réservé aux choix, à l'indice et aux fins.\n"
        "- N1 ≤ 10 mots/phrase. Pas de leçon dite. Pas de tics « tout doux / encore / déjà / tout calme ».\n"
        "- Pas de refrains example3. Pas de merle / miel. Pas apply. Pas audio.\n\n"
        "## Direction vocale\n\n"
        "`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, "
        "tempo, sourire, respiration. Adulte conversationnel, pas maîtresse. Tours "
        "de parole : envie de couper, retenue, écoute réelle, plaisir d'être entendu.\n\n"
        "## Contrôles\n\n"
        "- 86 chunks, graphe `option_*_next` / `default_next` conservé\n"
        "- 27 chemins, 27 fins textuellement distinctes\n"
        f"- {lo} à {hi} mots par chemin, moyenne {avg} (N1)\n"
        "- `check()` OK (N1 ≤ 10 mots/phrase)\n"
        "- `text` et `script` synchronisés\n"
        "- `text_ssml` et `text_xai_tags` enrichis sur les 86 chunks\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
