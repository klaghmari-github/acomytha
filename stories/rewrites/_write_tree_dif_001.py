#!/usr/bin/env python3
"""TREE-DIF-001 — Le coquillage d'Aniss pour Sarah (F-NAR-019, N1, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-001"
LIM = 10
TITLE = "Le coquillage d'Aniss pour Sarah"
CHARS = "Aniss, Sarah, papa, maman"
SETTING = "maison près de la mer, sable mouillé"
FIL = (
    "Le cri d'une mouette entre dans la cuisine. Sur la coquille rose d'Aniss, "
    "un point d'écume tient, blanc. Il veut le montrer à Sarah, au bord, maintenant. "
    "Sarah arrive et s'arrête, sans un mot. T1 = seau / filet / linge, les trois partent. "
    "Première idée trop vite : toc, maille ouverte, tissu trop serré. "
    "T2 = rochers trop hauts / laisse trop loin / mare trop profonde. "
    "La mouette pique le point d'écume, au lieu de prendre la coquille. "
    "Aniss veut chasser. Sarah pose sa limite. Silence = réponse. "
    "T3 : ils refusent de foncer, retrouvent le point, font avec. "
    "Sarah tient le rose. Ça a failli ne pas arriver."
)
TICS = (
    "tout doux",
    "tout calme",
    "on va apprendre",
    "voici le geste",
    "l'histoire est finie",
    "il faut attendre",
    "bravo tu as",
    "bon travail",
    "j'ai compris",
    "mission accomplie",
    "aujourd'hui,",
    "aujourd'hui ",
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
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_point_d_ecume_tient_sur_la_coquille; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_colore_le_voyage; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ou_voyage_la_coquille; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=trop_vite_la_coquille_resiste; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_inquiétude; intensite=2; destinataire=enfant; sous_texte=la_mouette_pique_l_ecume_sarah_pose_sa_limite; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=ils_refusent_de_foncer_retrouvent_le_point; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_point_d_ecume_paie_le_debut; tempo=posé; sourire=léger; respiration=ample",
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
        for tic in ("encore", "déjà", "deja", "tout doux", "tout calme"):
            if tic in low:
                raise SystemExit(f"{where} tic corpus « {tic} »: {ph}")
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
    ("narrateur", "Le cri d'une mouette entre dans la cuisine."),
    ("narrateur", "Le sable mouillé suce le bas de la porte."),
    ("narrateur", "Une ombre d'aile passe sur la table."),
    ("narrateur", "La maison sent le linge, et le sel."),
    ("narrateur", "Papa pose les sandales, près du palier."),
    ("maman", "Sarah va arriver, Aniss."),
    ("narrateur", "Aniss ouvre la paume, vers le rebord."),
    ("narrateur", "C'est le rebord du volet, face à l'eau."),
    ("narrateur", "Sa coquille rose y tient, légère."),
    ("narrateur", "Un point d'écume y reste, blanc."),
    ("enfant-m", "Il ne sèche pas."),
    ("papa", "Tu l'as vue, cette petite tache ?"),
    ("enfant-m", "Je veux la montrer à Sarah."),
    ("enfant-m", "Au bord de l'eau."),
    ("narrateur", "En ce moment, des pas sonnent dehors."),
    ("enfant-f", "Aniss, me voilà."),
    ("narrateur", "Sarah s'arrête, sans un mot."),
    ("enfant-m", "Viens, on court !"),
    ("narrateur", "Sarah ne bouge pas."),
    ("narrateur", "Aniss sent ça, dans sa poitrine."),
    ("enfant-m", "On va au bord, ensemble."),
    ("papa", "Merci, tu as vu son silence."),
    ("maman", "On prépare le sac, alors ?"),
)

T1 = {
    1: dict(
        name="le seau",
        expected="seau",
        accepted="seau | le seau | dans le seau | au fond du seau",
        retry="Le coquillage est dans le seau.",
        ok="Oui, il est dans le seau.",
        sons="seau,sable",
        emphasis="seau",
        passage=L(
            ("narrateur", "Aniss glisse la coquille dans le seau."),
            ("enfant-m", "Elle ira au fond, Sarah !"),
            ("narrateur", "Il la pousse trop vite."),
            ("narrateur", "La coquille tape, toc."),
            ("narrateur", "Sarah recule, un pas."),
            ("enfant-f", "Attends."),
            ("narrateur", "Elle ne dit rien de plus."),
            ("enfant-m", "Je ralentis."),
            ("maman", "Garde le seau, sans le vider."),
            ("papa", "Le filet, ensuite, dans le sac."),
            ("narrateur", "Maman plie le linge, contre le seau."),
            ("narrateur", "Les trois affaires partent ensemble."),
            ("papa", "Le seau d'abord, vous l'avez."),
        ),
        question=L(
            ("narrateur", "Aniss a glissé la coquille dans le seau."),
            ("maman", "Il est où, le coquillage ?"),
        ),
        confirm=L(
            ("narrateur", "Le seau porte la coquille, au fond."),
            ("enfant-f", "J'entends le toc, un peu."),
            ("enfant-m", "C'est pour toi, Sarah."),
            ("narrateur", "Le point d'écume tient, contre le plastique."),
            ("narrateur", "Le filet et le linge voyagent aussi."),
            ("maman", "Le sable mouillé vous attend."),
            ("papa", "On sort par le petit chemin ?"),
            ("enfant-m", "Oui, papa."),
        ),
        choice=L(
            ("narrateur", "L'anse du seau tape, sur le sable."),
            ("narrateur", "Des rochers fumants attendent à gauche."),
            ("narrateur", "Au milieu, une ligne d'algues."),
            ("narrateur", "À droite, une mare ronde tremble."),
            ("papa", "Où montrez-vous la coquille ?"),
        ),
    ),
    2: dict(
        name="le filet",
        expected="filet",
        accepted="filet | le filet | dans le filet | au fond du filet",
        retry="Le coquillage est dans le filet.",
        ok="Oui, il est dans le filet.",
        sons="filet,mailles",
        emphasis="filet",
        passage=L(
            ("narrateur", "Aniss ouvre le filet, trop large."),
            ("enfant-m", "La coquille va ici, Sarah."),
            ("narrateur", "Le rose penche, presque dehors."),
            ("narrateur", "Sarah tend la main, puis la retire."),
            ("enfant-f", "Non."),
            ("narrateur", "Elle reste là, les lèvres fermées."),
            ("enfant-m", "Je referme, plus lent."),
            ("papa", "Les mailles sont fines, Aniss."),
            ("maman", "Le seau, ensuite, près du sac."),
            ("narrateur", "Elle glisse le linge par-dessus."),
            ("narrateur", "Les trois affaires partent ensemble."),
            ("maman", "Le filet d'abord, il est prêt."),
        ),
        question=L(
            ("narrateur", "Aniss a glissé la coquille dans le filet."),
            ("papa", "Il est où, le coquillage ?"),
        ),
        confirm=L(
            ("narrateur", "Le filet tient la coquille, entre les mailles."),
            ("enfant-f", "Je vois le rose !"),
            ("enfant-m", "Ne touche pas, pas maintenant."),
            ("narrateur", "Le point d'écume brille, entre deux fils."),
            ("narrateur", "Le seau et le linge voyagent aussi."),
            ("papa", "Le vent sent le sel, dehors."),
            ("maman", "Vos pieds, dans les sandales ?"),
            ("enfant-f", "Oui, maman."),
        ),
        choice=L(
            ("narrateur", "Les mailles sentent le sel, un peu."),
            ("narrateur", "Des rochers fumants attendent à gauche."),
            ("narrateur", "Au milieu, une ligne d'algues."),
            ("narrateur", "À droite, une mare ronde tremble."),
            ("maman", "Où montrez-vous la coquille ?"),
        ),
    ),
    3: dict(
        name="le linge",
        expected="linge",
        accepted="linge | le linge | dans le linge | le linge rayé",
        retry="Le coquillage est dans le linge.",
        ok="Oui, il est dans le linge.",
        sons="linge,tissu",
        emphasis="linge",
        passage=L(
            ("narrateur", "Aniss prend le linge, tiède de soleil."),
            ("enfant-m", "Je cache la coquille, Sarah."),
            ("narrateur", "Il enroule trop fort, trop vite."),
            ("narrateur", "Le point d'écume s'écrase, un peu."),
            ("enfant-f", "Stop."),
            ("narrateur", "Sarah pose sa paume, sans parler."),
            ("enfant-m", "Je desserre."),
            ("maman", "Enroule-la, comme un secret."),
            ("papa", "Le seau et le filet, avec vous."),
            ("narrateur", "Il les pose près des sandales."),
            ("narrateur", "Les trois affaires partent ensemble."),
            ("papa", "Le linge d'abord, il est chaud."),
        ),
        question=L(
            ("narrateur", "Aniss a caché la coquille dans le linge."),
            ("maman", "Il est où, le coquillage ?"),
        ),
        confirm=L(
            ("narrateur", "Le linge rayé cache la coquille, au milieu."),
            ("enfant-f", "Ça sent le chaud."),
            ("enfant-m", "Elle est là, au creux."),
            ("narrateur", "Le point d'écume tient, sous le tissu."),
            ("narrateur", "Le seau et le filet voyagent aussi."),
            ("maman", "La mer est calme, devant."),
            ("papa", "On y va, tous les quatre ?"),
            ("enfant-m", "Oui."),
        ),
        choice=L(
            ("narrateur", "Le linge rayé frotte son poignet."),
            ("narrateur", "Des rochers fumants attendent à gauche."),
            ("narrateur", "Au milieu, une ligne d'algues."),
            ("narrateur", "À droite, une mare ronde tremble."),
            ("papa", "Où montrez-vous la coquille ?"),
        ),
    ),
}

T2_LABS = ("les rochers", "la laisse", "la mare")
T3_LABS = {
    1: ("la main de Sarah", "les bras de papa", "un nid plus bas"),
    2: ("les petites traces", "le geste de loin", "la petite vague"),
    3: ("les chevilles", "l'eau qui recule", "tendre ensemble"),
}
OBJ = {1: "le seau", 2: "le filet", 3: "le linge"}
CAP = {1: "Le seau", 2: "Le filet", 3: "Le linge"}


def t2_rochers(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Aniss pose le seau au pied du roc.",
        2: "Aniss pose le filet au pied du roc.",
        3: "Aniss pose le linge au pied du roc.",
    }[a]
    mishap = {
        1: "L'anse tape, trop bas pour la fente.",
        2: "Les mailles n'accrochent pas, trop basses.",
        3: "Le tissu glisse, trop bas pour la fente.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-m", "Je la pose en haut, Sarah !"),
        ("narrateur", "Les rochers fumants sentent l'algue."),
        ("narrateur", "Aniss se hausse, d'un coup."),
        ("narrateur", mishap),
        ("enfant-m", "Ma main n'y arrive pas."),
        ("narrateur", "Une mouette se pose, sur le roc."),
        ("enfant-m", "Elle va prendre ma coquille !"),
        ("narrateur", "La mouette pique le point d'écume."),
        ("narrateur", "Puis elle saute de côté, et attend."),
        ("enfant-m", "Chasse-la, Sarah !"),
        ("narrateur", "Sarah ne bouge pas."),
        ("narrateur", "Le sourire d'Aniss disparaît."),
        ("narrateur", "L'envie et l'inquiétude se bousculent."),
        ("papa", "Je m'accroupis, à votre hauteur."),
        ("maman", "Vous faites comment, tous les deux ?"),
    )


def t2_laisse(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Le seau penche, trop vite, vers les algues.",
        2: "Le filet s'ouvre, un peu trop, vers les algues.",
        3: "Le linge se défait, un coin, vers les algues.",
    }[a]
    return L(
        ("narrateur", pose),
        ("narrateur", "La coquille glisse vers la laisse."),
        ("enfant-m", "Elle part trop loin !"),
        ("enfant-f", "Je la vois, entre les bulles."),
        ("narrateur", "Une ligne d'écume barre le sable."),
        ("enfant-m", "On court, Sarah !"),
        ("narrateur", "Une mouette saute le long de l'écume."),
        ("enfant-m", "Elle va la prendre !"),
        ("narrateur", "La mouette s'arrête sur le point d'écume."),
        ("narrateur", "Elle ne prend pas la coquille."),
        ("narrateur", "Elle les regarde, puis se tait."),
        ("narrateur", "Sarah reste plantée, sans un mot."),
        ("narrateur", "Le sourire d'Aniss n'est plus là."),
        ("narrateur", "Ça serre, juste sous la gorge."),
        ("papa", "Je m'accroupis, près de la ligne."),
        ("papa", "Vous la reprenez comment ?"),
    )


def t2_mare(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Aniss tapote l'eau avec le seau, trop fort.",
        2: "Aniss frôle la mare avec le filet, trop vite.",
        3: "Aniss pose le linge au bord, un peu sec.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-m", "On rince la coquille, Sarah."),
        ("enfant-f", "Pour qu'elle brille vraiment."),
        ("narrateur", "La mare ronde tremble, trop profonde."),
        ("narrateur", "Aniss pose un pied, puis recule."),
        ("enfant-m", "L'eau me monte trop vite."),
        ("narrateur", "Une mouette boit, au milieu."),
        ("enfant-m", "Elle va partir avec !"),
        ("narrateur", "La mouette pose une plume, sur l'écume."),
        ("narrateur", "Elle ne vole pas, elle attend."),
        ("narrateur", "Sarah reste au bord, les lèvres closes."),
        ("narrateur", "Le sourire d'Aniss s'en va."),
        ("narrateur", "Dans sa poitrine, deux envies se poussent."),
        ("maman", "Je m'accroupis, face à l'eau."),
        ("papa", "Vous rincez comment, tous les deux ?"),
    )


T2_FN = {1: t2_rochers, 2: t2_laisse, 3: t2_mare}
T2_SONS = {1: "rocher,oiseau", 2: "vague,sable", 3: "eau,oiseau"}
T2_EMPH = {1: "mouette", 2: "laisse", 3: "mare"}


def t3_choice(t2: int) -> list[tuple[str, str]]:
    if t2 == 1:
        return L(
            ("narrateur", "Le roc reste trop haut."),
            ("narrateur", "Aniss pose une main, sans sauter."),
            ("papa", "La main de Sarah, mes bras, ou un nid ?"),
        )
    if t2 == 2:
        return L(
            ("narrateur", "La coquille a roulé trop loin."),
            ("narrateur", "Aniss pose un pied, sans courir."),
            ("maman", "Les traces, le geste de loin, ou la vague ?"),
        )
    return L(
        ("narrateur", "L'eau de la mare est profonde."),
        ("narrateur", "Aniss pose un orteil, sans entrer."),
        ("papa", "Les chevilles, l'eau qui recule, ou tendre ?"),
    )


def t3(a: int, b: int, c: int) -> list[tuple[str, str]]:
    o = OBJ[a]
    cap = CAP[a]
    table = {
        (1, 1): L(
            ("enfant-m", "On n'y court pas."),
            ("enfant-f", "Ma main passe à côté."),
            ("narrateur", "Sarah glisse les doigts dans la fente."),
            ("narrateur", f"Aniss pousse {o} contre le roc."),
            ("narrateur", "Papa se tait, accroupi."),
            ("narrateur", "Aniss écoute le roc, puis l'eau."),
            ("narrateur", "Le point d'écume brille, dans la fente."),
            ("enfant-f", "Je la touche !"),
            ("narrateur", "La mouette saute, et laisse le rose."),
            ("papa", "Ta main allait jusque-là, Sarah."),
            ("enfant-m", "Regarde, elle est à nous."),
            ("enfant-f", "Elle est froide."),
        ),
        (1, 2): L(
            ("enfant-m", "Pas de saut, papa."),
            ("papa", "Je vous tiens, tous les deux."),
            ("narrateur", "Aniss pose la coquille sur le roc."),
            ("narrateur", f"{cap} attend en bas, plein de sable."),
            ("enfant-f", "Je la vois, tout près."),
            ("narrateur", "Sarah tend les deux mains."),
            ("narrateur", "Aniss refuse de chasser la mouette."),
            ("narrateur", "Le point d'écume penche, à hauteur d'yeux."),
            ("enfant-m", "C'est lui, je le reconnais."),
            ("narrateur", "La coquille glisse vers Sarah."),
            ("maman", "Vous la partagez."),
            ("enfant-f", "Elle est à moi, un moment."),
        ),
        (1, 3): L(
            ("enfant-m", "On fait un nid ici."),
            ("enfant-f", "Avec les petits cailloux."),
            ("narrateur", "Ils empilent, caillou après caillou."),
            ("narrateur", "Le nid arrive sous leur menton."),
            ("narrateur", f"{cap} garde le pied du nid."),
            ("narrateur", "Aniss ne fonce pas vers le roc haut."),
            ("narrateur", "Le point d'écume clignote, au centre."),
            ("enfant-m", "Je la pose là, Sarah."),
            ("enfant-f", "Elle n'est plus trop haut."),
            ("papa", "Votre trône est à votre taille."),
            ("narrateur", "La mouette regarde, puis s'en va."),
            ("maman", "Vous l'avez baissé, ensemble."),
        ),
        (2, 1): L(
            ("enfant-m", "On suit les petites traces."),
            ("enfant-f", "Celles de la mouette, tout étroites."),
            ("narrateur", "Ils marchent dans leurs propres pas."),
            ("narrateur", "Une bulle d'écume cache le rose."),
            ("enfant-f", "Là !"),
            ("narrateur", f"Aniss pose la coquille dans {o}."),
            ("narrateur", "Aniss ne court pas vers l'eau."),
            ("narrateur", "Le point d'écume réapparaît, sur le sable."),
            ("papa", "Vos pieds allaient assez loin."),
            ("enfant-m", "On l'a, Sarah."),
            ("enfant-f", "Elle est froide."),
            ("maman", "Vous avez suivi ce qui était petit."),
        ),
        (2, 2): L(
            ("enfant-f", "On reste ici."),
            ("enfant-m", "On attrape de loin."),
            ("narrateur", f"Sarah tend {o}, bras tout longs."),
            ("narrateur", "Aniss guide le bord, sans avancer."),
            ("narrateur", "Papa ne dit pas le geste."),
            ("narrateur", f"Aniss écoute la laisse, puis {o}."),
            ("narrateur", "Le point d'écume marque le bord, blanc."),
            ("narrateur", "La coquille rentre, un peu sableuse."),
            ("enfant-m", "Je la tiens !"),
            ("maman", "Vous n'avez pas couru trop loin."),
            ("enfant-f", "Elle sent les algues."),
            ("papa", "Soufflez dessus, sans presser."),
        ),
        (2, 3): L(
            ("enfant-m", "On attend la petite vague."),
            ("enfant-f", "Moi aussi, j'attends."),
            ("narrateur", "L'eau avance, puis recule."),
            ("narrateur", "La coquille revient, tout près."),
            ("narrateur", f"{cap} cueille la coquille, au bord."),
            ("narrateur", "Aniss refuse de foncer dans l'écume."),
            ("narrateur", "Le point d'écume voyage avec la vague."),
            ("papa", "Elle est venue vers vous."),
            ("enfant-f", "On l'a reprise."),
            ("enfant-m", "Regarde, elle brille, Sarah."),
            ("maman", "Vos poches sont un peu mouillées."),
            ("narrateur", "La mouette s'envole, sans rien prendre."),
        ),
        (3, 1): L(
            ("enfant-m", "J'entre jusqu'aux chevilles."),
            ("narrateur", f"Sarah garde {o} au bord."),
            ("narrateur", "L'eau froide lui pince la peau."),
            ("enfant-m", "Passe-moi la coquille."),
            ("enfant-f", "La voilà."),
            ("narrateur", "Aniss la plonge, un tout petit peu."),
            ("narrateur", "Il ne va pas plus loin."),
            ("narrateur", "Le point d'écume redevient net, au creux."),
            ("enfant-f", "Elle brille pour de vrai."),
            ("papa", "Tu es rentré juste assez."),
            ("maman", "Sarah tenait bien le bord."),
            ("narrateur", "La mouette boit, plus loin, sans eux."),
        ),
        (3, 2): L(
            ("enfant-f", "On attend que l'eau recule."),
            ("enfant-m", "Oui, un peu."),
            ("narrateur", "La mare se fait plus petite."),
            ("narrateur", "Un anneau mouillé reste au bord."),
            ("enfant-m", "Maintenant, on peut."),
            ("narrateur", "Ils trempent la coquille, tous les deux."),
            ("narrateur", f"Ils posent {o} sur le sable sec."),
            ("narrateur", "Aniss n'entre pas trop tôt."),
            ("narrateur", "Le point d'écume tient, propre, au centre."),
            ("enfant-f", "Elle est propre."),
            ("papa", "L'eau vous a laissé la place."),
            ("maman", "Vous avez regardé ensemble."),
        ),
        (3, 3): L(
            ("enfant-m", "On rince ici, sur le sable."),
            ("enfant-f", "Sans entrer trop."),
            ("narrateur", f"Papa tend {o}, plein d'eau."),
            ("narrateur", "Aniss et Sarah tiennent le bord."),
            ("narrateur", "L'eau coule sur la coquille rose."),
            ("narrateur", "Personne ne pousse, ici."),
            ("narrateur", "Le point d'écume redevient blanc, net."),
            ("enfant-m", "Elle brille, Sarah."),
            ("enfant-f", "Je la vois trop bien."),
            ("maman", "Vous avez tiré ensemble."),
            ("papa", "La mare reste à sa place."),
            ("narrateur", "La mouette s'éloigne, plume à terre."),
        ),
    }
    return table[(b, c)]


def fin(a: int, b: int, c: int) -> list[tuple[str, str]]:
    cap = CAP[a]
    last = {
        (1, 1, 1): "Le seau sèche, un rond blanc au fond.",
        (1, 1, 2): "L'anse du seau garde une poudre de roc.",
        (1, 1, 3): "Le seau borde le nid, près des sandales.",
        (1, 2, 1): "Le seau pose une feuille d'algue au palier.",
        (1, 2, 2): "L'anse du seau sent l'algue, à la porte.",
        (1, 2, 3): "Le seau laisse un trait salé sur le carreau.",
        (1, 3, 1): "Une auréole salée reste sous le seau.",
        (1, 3, 2): "Un anneau mouillé cerne le seau, au carrelage.",
        (1, 3, 3): "Le seau brille, plein d'eau, au rebord.",
        (2, 1, 1): "Le filet sèche, une maille blanche au sel.",
        (2, 1, 2): "Une maille du filet garde la poudre de roc.",
        (2, 1, 3): "Le filet ombre le nid, près des sandales.",
        (2, 2, 1): "Le filet pose une algue au palier.",
        (2, 2, 2): "Les mailles sentent l'algue, à la porte.",
        (2, 2, 3): "Le filet laisse un fil salé sur le carreau.",
        (2, 3, 1): "Le filet sèche au seuil, un peu lourd.",
        (2, 3, 2): "Un anneau mouillé cerne le filet, au carrelage.",
        (2, 3, 3): "Le filet brille, lourd d'eau, au rebord.",
        (3, 1, 1): "Le linge rayé garde un rond d'écume.",
        (3, 1, 2): "Le linge rayé garde une poudre de roc.",
        (3, 1, 3): "Le linge borde le nid, près des sandales.",
        (3, 2, 1): "Le linge pose une algue au palier.",
        (3, 2, 2): "Le linge rayé sent l'algue, à la porte.",
        (3, 2, 3): "Le linge laisse un trait salé sur le carreau.",
        (3, 3, 1): "Le linge sèche au seuil, un coin mouillé.",
        (3, 3, 2): "Un anneau mouillé cerne le linge, au carrelage.",
        (3, 3, 3): "Le linge rayé brille, lourd d'eau, au rebord.",
    }[(a, b, c)]
    cores = {
        (1, 1): L(
            ("narrateur", "Ils rentrent, la coquille au creux."),
            ("enfant-f", "Elle sent le roc."),
            ("enfant-m", "Ta main l'a fait descendre."),
            ("papa", "Vous l'avez montrée, enfin."),
            ("maman", "Posez-la sur le rebord, au sel."),
            ("narrateur", "Le volet garde le point d'écume, minuscule."),
            ("narrateur", "Une mouette crie, plus loin."),
            ("enfant-m", "Tu l'as vue, Sarah."),
            ("enfant-f", "Oui."),
        ),
        (1, 2): L(
            ("narrateur", "Du haut du roc, la maison était petite."),
            ("enfant-m", "Sarah, tu l'as vue briller."),
            ("enfant-f", "Oui, tout près de mes yeux."),
            ("papa", "Je vous ai tenus, pas trop longtemps."),
            ("maman", "Vos traces rentrent, grandes et petites."),
            ("narrateur", "La coquille reste dans la paume de Sarah."),
            ("narrateur", "Le point d'écume y tient, un peu plat."),
            ("enfant-f", "Je la tiens, Aniss."),
            ("narrateur", "La table sent le linge chaud."),
        ),
        (1, 3): L(
            ("narrateur", "Le nid de cailloux voyage jusqu'à la porte."),
            ("enfant-f", "Notre trône rentre à la maison."),
            ("enfant-m", "La coquille n'a plus trop haut."),
            ("maman", "Elle dort à votre hauteur, maintenant."),
            ("papa", "Les petits cailloux restent au paillasson."),
            ("narrateur", "Le point d'écume veille, au centre du nid."),
            ("enfant-m", "On a failli la poser trop haut."),
            ("enfant-f", "Là, je la vois."),
            ("narrateur", "Une odeur d'algue reste dans l'entrée."),
        ),
        (2, 1): L(
            ("narrateur", "Ils rentrent avec du sable aux genoux."),
            ("enfant-m", "Les petites traces savaient le chemin."),
            ("enfant-f", "La mouette aussi, peut-être."),
            ("papa", "Vous avez suivi ce qui était à vous."),
            ("maman", "Soufflez la dernière bulle, dehors."),
            ("enfant-m", "Elle est pour Sarah, maintenant."),
            ("enfant-f", "Elle est un peu froide."),
            ("narrateur", "Le point d'écume sèche sur le palier."),
            ("narrateur", "Sarah pose le rose contre le bois."),
        ),
        (2, 2): L(
            ("narrateur", "Ils n'ont pas couru jusqu'à l'eau."),
            ("enfant-f", "On l'a attrapée de loin."),
            ("enfant-m", "Tes bras étaient assez longs."),
            ("maman", "L'algue sent fort, sur vos mains."),
            ("papa", "Lavez-les, au bac, sans presser."),
            ("narrateur", f"{cap} garde une feuille d'algue."),
            ("enfant-f", "Je la tiens, Aniss."),
            ("narrateur", "Le point d'écume reste au creux, blanc."),
            ("narrateur", "Le bac se tait, puis la fenêtre."),
        ),
        (2, 3): L(
            ("narrateur", "Leurs poches mouillent l'entrée, un peu."),
            ("enfant-m", "La vague nous l'a rendue."),
            ("enfant-f", "On a attendu, tous les deux."),
            ("papa", "Elle est venue vers vos mains."),
            ("maman", "Changez le linge des poches, d'abord."),
            ("narrateur", "Une ligne salée marque le carreau."),
            ("enfant-m", "Regarde-la, Sarah, elle brille."),
            ("narrateur", "Sur la table, le point d'écume tient."),
            ("narrateur", "Près du pain, le rose reste au chaud."),
        ),
        (3, 1): L(
            ("narrateur", "Les chevilles d'Aniss sont froides."),
            ("enfant-f", "Tu l'as rincée pour moi."),
            ("enfant-m", "Tu tenais le bord."),
            ("maman", "Essuie tes pieds, sur le paillasson."),
            ("papa", "La coquille est nette, maintenant."),
            ("narrateur", "Sarah la pose contre la vitre."),
            ("narrateur", "Un rai de soleil traverse le rose."),
            ("narrateur", "Le point d'écume y fait un éclat."),
            ("enfant-m", "Tu l'as vue, enfin."),
        ),
        (3, 2): L(
            ("narrateur", "Un anneau mouillé les suit jusqu'à la porte."),
            ("enfant-m", "L'eau a reculé pour nous."),
            ("enfant-f", "On a rincé ensemble, après."),
            ("papa", "La mer vous a laissé le temps."),
            ("maman", "Le sable sèche sur vos mollets."),
            ("narrateur", f"{cap} pose une auréole au carrelage."),
            ("enfant-f", "Elle brille trop, Aniss."),
            ("enfant-m", "C'est pour ça."),
            ("narrateur", "Le point d'écume tient, tout proche de la vitre."),
        ),
        (3, 3): L(
            ("narrateur", "Un peu d'eau de mare reste au seuil."),
            ("enfant-m", "On a tiré ensemble."),
            ("enfant-f", "Sans trop entrer."),
            ("papa", "La mare est restée à sa place."),
            ("maman", "Vos mains sentent le sel."),
            ("narrateur", "Sarah pose la coquille au rebord."),
            ("enfant-m", "Tu l'as vue, enfin."),
            ("narrateur", "Le point d'écume s'endort, contre le bois."),
            ("narrateur", "Dehors, la mouette se tait."),
        ),
    }
    rows = list(cores[(b, c)])
    rows.append(("narrateur", last))
    return rows


T3_EMPH = {
    1: {1: "main", 2: "bras", 3: "nid"},
    2: {1: "traces", 2: "loin", 3: "vague"},
    3: {1: "chevilles", 2: "eau", 3: "ensemble"},
}
T3_SONS = {
    1: {1: "rocher,main", 2: "rocher,pas", 3: "cailloux,nid"},
    2: {1: "sable,pas", 2: "filet,vague", 3: "vague,ecume"},
    3: {1: "eau,pas", 2: "eau,sable", 3: "eau,linge"},
}
FIN_SONS = {1: "oiseau,porte", 2: "vague-loin,porte", 3: "eau,silence"}


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "oiseau,mer", "emphasis": "point d'écume"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Le sac attend, près des sandales."),
            ("narrateur", "Le seau, le filet, et le linge."),
            ("narrateur", "Aniss serre la coquille, puis la pose."),
            ("maman", "Tu prends quoi d'abord, Aniss ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "le seau",
            "option_2_label": "le filet",
            "option_3_label": "le linge",
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
                "engine_near_text": "Tu es très proche. Reprenons l'indice.",
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
                "option_1_label": T2_LABS[0],
                "option_2_label": T2_LABS[1],
                "option_3_label": T2_LABS[2],
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
                    by_old[leaf], t3(a, b, c), "resolution",
                    extra={"sons": T3_SONS[b][c], "emphasis": "point d'écume"},
                )
                fin_id = f"{leaf}_F0001"
                by[fin_id] = voice(
                    by_old[fin_id], fin(a, b, c), "ending",
                    extra={"sons": FIN_SONS[b], "emphasis": "point d'écume"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra_ids = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    fins = [by[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(set(fins)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fins))}/27")

    out = dict(src)
    out["fil_rouge"] = FIL
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
    if n_enc or n_dej:
        raise SystemExit(f"tics encore={n_enc} déjà={n_dej}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"en ce moment ×{blob.count('en ce moment')}")
    if "aniss" not in blob or "sarah" not in blob:
        raise SystemExit("Aniss/Sarah absents")
    if "point d'écume" not in blob and "point d'ecume" not in blob:
        raise SystemExit("indice point d'écume absent")
    if "mouette" not in blob:
        raise SystemExit("mouette absente")
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "bravo tu as",
        "bon travail",
        "j'ai compris",
        "mission accomplie",
        "merle",
        "miel",
        "grand-père",
        "maîtresse",
        "jardinier",
        "bibliothécaire",
        "gardienne",
        "grain d'ambre",
        "écaille de nacre",
        "ecaille de nacre",
        "fil pâle",
        "fil pale",
        "étoile brune",
        "etoile brune",
        "ancre minuscule",
        "marque fine",
        "ombre-flèche",
        "ombre-fleche",
        "tache de couleur",
        "phare",
        "jetée",
        "jetee",
        "crabe vert",
        "tailles sont différentes",
        "tailles sont differentes",
        "on peut jouer ensemble",
    ):
        if bad in whole:
            raise SystemExit(f"calque: {bad}")
    for c in out["chunks"]:
        if not c.get("text_xai_tags") or not c.get("notes") or not c.get("style_energy"):
            raise SystemExit(f"{c['chunk_id']}: TTS incomplet")
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{c['chunk_id']} fin mécanique: {last}")
        if c["text_xai_tags"] == c["text"]:
            raise SystemExit(f"{c['chunk_id']}: text_xai_tags = text")

    nwords = sum(words(c["text"]) for c in out["chunks"])
    byw = {c["chunk_id"]: c for c in out["chunks"]}

    def _walk(t1: int, t2: int, t3: int) -> int:
        ids = [
            "CHK_T0000_P0000",
            "CHK_T0001_P0000",
            f"CHK_T0001_P000{t1}",
            f"CHK_T0001_P000{t1}_Q0001",
            f"CHK_T0001_P000{t1}_C0001",
            f"CHK_T0001_P000{t1}_T0002_P0000",
            f"CHK_T0001_P000{t1}_T0002_P000{t2}",
            f"CHK_T0001_P000{t1}_T0002_P000{t2}_T0003_P0000",
            f"CHK_T0001_P000{t1}_T0002_P000{t2}_T0003_P000{t3}",
            f"CHK_T0001_P000{t1}_T0002_P000{t2}_T0003_P000{t3}_F0001",
        ]
        return sum(words(byw[i]["text"]) for i in ids)

    plens = [_walk(a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    pmin, pmax = min(plens), max(plens)
    pavg = round(sum(plens) / len(plens))

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés. Graphe `option_*_next` conservé.\n\n"
        "## Vécu\n"
        "Maison près de la mer, sable mouillé. Le cri d'une mouette entre "
        "dans la cuisine. Coin nommé : le rebord du volet. Sur la coquille rose, "
        "un point d'écume tient, blanc. Mission : le montrer à Sarah, au bord, "
        "maintenant. Sarah arrive et s'arrête, sans un mot. Aniss propose de "
        "courir ; son silence compte. Papa remercie Aniss d'avoir vu ce silence. "
        "T1 = seau / filet / linge (les trois partent ; trop vite : toc, maille "
        "ouverte, tissu trop serré). T2 = rochers (trop haut) / laisse (trop loin) "
        "/ mare (trop profonde). La mouette pique le point d'écume au lieu de "
        "prendre la coquille. Aniss veut chasser ; Sarah pose sa limite. Sourire "
        "parti, poitrine serrée, adulte accroupi. T3 : ils refusent de foncer, "
        "retrouvent le point du début, font avec. 27 fins : le rose est vu, "
        "l'objet porte une trace, ça a failli ne pas arriver. Leçon DIF.COR.001 "
        "vécue (faire avec l'autre, pas sans elle), jamais dite. "
        "Monde ≠ TREE-AUT-021 (nacre), ≠ TREE-DIF-052 (phare, ambre).\n\n"
        "## Vu et corrigé\n"
        f"`python3 stories/rewrites/_write_tree_dif_001.py` → `OK {SID} {nwords} mots`. "
        "N1 ≤ 10. `_lib.check` vert.\n"
        f"- 86 chunks, 27 chemins, 27 fins distinctes, {pmin} à {pmax} mots "
        f"(moyenne {pavg}).\n"
        "- Ouverture inventée (cri de mouette, pas « encore »).\n"
        "- Indice unique : point d'écume, payé au climax et en coda.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js. "
        "`slow` = choix, question, retour.\n"
        "- Tics encore / déjà / tout doux / tout calme jetés. "
        "Merle, miel, Mission accomplie, J'ai compris jetés.\n"
        "- Un merci vécu (voir le silence de Sarah). Pas apply. Audio non cuit.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )
    print(f"OK {SID} {nwords} mots  1re: {out['chunks'][0]['script'].splitlines()[0].split('|',1)[1]}")


if __name__ == "__main__":
    main()
