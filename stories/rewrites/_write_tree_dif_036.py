#!/usr/bin/env python3
"""TREE-DIF-036 — Le poisson de bois de Raphaël au lavoir (N2, DIF.COR.003, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-036"
LIM = 15
TITLE = "Le poisson de bois de Raphaël au lavoir"
CHARS = "Raphaël, Aniss, papa, maman"
SETTING = "lavoir du village après la pluie : bassin, ruisseau, géraniums"
FIL = (
    "Après la pluie, la gouttière du lavoir compte les gouttes. "
    "Raphaël veut que son poisson de bois nage avant que l'eau parte. "
    "Sur le dos, une écaille d'étain cliquette. "
    "Aniss arrive lent : lunettes voilées, cheveux mouillés, manteau trop long. "
    "Raphaël veut poser maintenant. Aniss veut regarder. Silence = réponse. "
    "T1 = poisson / filet vert / seau bleu, les trois partent. "
    "T2 = bassin (buée) / ruisseau (mèches) / géraniums (manches). "
    "L'écaille disparaît. Ils refusent de foncer, la retrouvent. "
    "Le poisson nage. Ça a failli ne pas nager."
)
TICS = (
    "tout doux",
    "tout calme",
    "tout lent",
    "on va apprendre",
    "voici le geste",
    "l'histoire est finie",
    "il faut attendre",
    "bravo tu as",
    "bon travail",
    "j'ai compris",
    "mission accomplie",
    "aujourd'hui,",
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
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=l_ecaille_d_etain_paiera_la_fin; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_le_geste; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_porte; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
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
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=trop_vite_la_premiere_idee_rate; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_inquiétude; intensite=2; destinataire=enfant; sous_texte=l_ecaille_disparait_aniss_pose_sa_limite; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=ils_refusent_de_foncer_retrouvent_l_ecaille; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_poisson_nage_l_ecaille_porte_une_goutte; tempo=posé; sourire=léger; respiration=ample",
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
        if re.search(r"\b(encore|déjà|deja)\b", low):
            raise SystemExit(f"{where} tic encore/déjà: {ph}")
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


def path_words(by: dict, a: int, b: int, c: int) -> int:
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
    return sum(words(by[i]["text"]) for i in ids)


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


OPENING = L(
    ("narrateur", "Une gouttière du lavoir compte les gouttes, une par une."),
    ("narrateur", "Raphaël les entend depuis le seuil de pierre."),
    ("narrateur", "Ça sent la pierre mouillée, et le savon."),
    ("narrateur", "L'eau du bassin baisse, lente, vers le trou."),
    ("enfant-m", "Mon poisson va nager, avant qu'elle parte."),
    ("narrateur", "Il sort le poisson de bois, de sa poche."),
    ("narrateur", "Sur le dos, une écaille d'étain cliquette."),
    ("papa", "Tu as vu cette écaille, Raphaël ?"),
    ("enfant-m", "Elle brille, petite, grise."),
    ("maman", "Le filet vert et le seau bleu attendent."),
    ("narrateur", "En ce moment, Raphaël serre le bois peint."),
    ("enfant-m", "Vite, Aniss, on le pose dans l'eau !"),
    ("narrateur", "Des pas lents sonnent sur les dalles."),
    ("copain", "J'arrive."),
    ("narrateur", "Aniss s'arrête, sans un mot."),
    ("narrateur", "Ses lunettes gardent un rond d'eau."),
    ("narrateur", "Ses cheveux gouttent sur le manteau trop long."),
    ("enfant-m", "On nage, maintenant ?"),
    ("narrateur", "Aniss secoue la tête, un peu."),
    ("copain", "Moi, je veux regarder."),
    ("papa", "Merci, tu as attendu sa voix."),
    ("maman", "On emporte les trois affaires, alors ?"),
)

T1 = {
    1: dict(
        name="le poisson de bois",
        expected="poche",
        accepted="poche | la poche | dans la poche | sa poche",
        retry="Le poisson est dans la poche.",
        ok="Oui, il est dans la poche.",
        sons="bois,poche",
        emphasis="poisson de bois",
        passage=L(
            ("narrateur", "Raphaël glisse le poisson dans sa poche."),
            ("enfant-m", "Le bois est froid, contre le tissu."),
            ("narrateur", "Il le sort trop vite, pour nager."),
            ("narrateur", "Aniss recule, les lunettes qui tremblent."),
            ("enfant-m", "Pardon, je n'ai pas vu."),
            ("copain", "J'ai besoin d'un moment."),
            ("narrateur", "Raphaël serre le poisson, sans bouger."),
            ("maman", "Garde-le dans la poche, bien droit."),
            ("papa", "Le filet, ensuite, au bras."),
            ("narrateur", "Aniss prend le seau bleu, par l'anse."),
            ("narrateur", "Les trois affaires partent, vers l'eau."),
            ("papa", "Le poisson d'abord, vous l'avez."),
        ),
        question=L(
            ("narrateur", "Le poisson de bois est dans la poche."),
            ("maman", "Le poisson est où ?"),
        ),
        confirm=L(
            ("narrateur", "La poche porte le poisson, contre le tissu."),
            ("copain", "Je vois un œil, un peu flou."),
            ("enfant-m", "C'est pour qu'il nage."),
            ("narrateur", "L'écaille d'étain voyage sous le tissu."),
            ("narrateur", "L'eau du lavoir baisse, loin."),
            ("maman", "L'eau vous attend, plus loin."),
            ("papa", "On avance avec le poisson ?"),
            ("enfant-m", "Oui, papa."),
        ),
        choice=L(
            ("narrateur", "Le bassin fume un peu, bas."),
            ("narrateur", "Sous l'arche, le ruisseau file."),
            ("narrateur", "Les géraniums pendent contre le mur."),
            ("papa", "Vous allez où, pour le poisson ?"),
        ),
    ),
    2: dict(
        name="le filet vert",
        expected="bras",
        accepted="bras | le bras | au bras | son bras",
        retry="Le filet est au bras.",
        ok="Oui, il est au bras.",
        sons="filet,mailles",
        emphasis="filet vert",
        passage=L(
            ("narrateur", "Raphaël enroule le filet vert, au bras."),
            ("enfant-m", "Les mailles grattent un peu, contre le coude."),
            ("narrateur", "Il le jette trop vite, vers l'eau."),
            ("narrateur", "Le filet accroche une mèche d'Aniss."),
            ("copain", "Mes lunettes ont bougé."),
            ("narrateur", "Raphaël ramène le filet, lentement."),
            ("enfant-m", "Je ralentis, promis."),
            ("papa", "Garde-le au bras, sans le jeter."),
            ("maman", "Le poisson, ensuite, dans la poche."),
            ("narrateur", "Aniss prend le seau bleu, par l'anse."),
            ("narrateur", "Les trois affaires restent ensemble."),
            ("maman", "Le filet d'abord, il est prêt."),
        ),
        question=L(
            ("narrateur", "Le filet vert est au bras."),
            ("maman", "Le filet est où ?"),
        ),
        confirm=L(
            ("narrateur", "Le bras porte le filet, contre la manche."),
            ("copain", "Ça gratte quand je marche."),
            ("enfant-m", "Ne le perds pas."),
            ("narrateur", "Une goutte tombe d'une mèche."),
            ("narrateur", "L'écaille d'étain voyage dans la poche."),
            ("papa", "Ça sent le savon, sur tes cheveux."),
            ("maman", "Vos mains, au-dessus du filet ?"),
            ("copain", "Oui, maman."),
        ),
        choice=L(
            ("narrateur", "Le filet froisse, contre la manche."),
            ("narrateur", "Le bassin fume un peu, bas."),
            ("narrateur", "Sous l'arche, le ruisseau file."),
            ("narrateur", "Les géraniums pendent contre le mur."),
            ("maman", "Vous allez où, pour nager ?"),
        ),
    ),
    3: dict(
        name="le seau bleu",
        expected="main",
        accepted="main | la main | dans la main | sa main",
        retry="Le seau est dans la main.",
        ok="Oui, il est dans la main.",
        sons="seau,metal",
        emphasis="seau bleu",
        passage=L(
            ("narrateur", "Raphaël saisit le seau bleu, par l'anse."),
            ("enfant-m", "Il sonne un peu, vide."),
            ("narrateur", "Il le balance trop vite, un coup."),
            ("narrateur", "Le métal claque près des lunettes."),
            ("copain", "Attends, je n'aime pas ça."),
            ("narrateur", "Raphaël baisse le seau, contre sa hanche."),
            ("enfant-m", "Je m'arrête."),
            ("maman", "Serre-le dans ta main, bien droit."),
            ("papa", "Le poisson et le filet, avec vous."),
            ("narrateur", "Il les pose près des dalles."),
            ("narrateur", "Les trois affaires restent ensemble."),
            ("papa", "Le seau d'abord, il est prêt."),
        ),
        question=L(
            ("narrateur", "Le seau bleu est dans la main."),
            ("maman", "Le seau est où ?"),
        ),
        confirm=L(
            ("narrateur", "L'anse porte le seau, légère."),
            ("copain", "Il a une goutte, au bord."),
            ("enfant-m", "On va le remplir."),
            ("narrateur", "Le manteau d'Aniss cache ses poignets."),
            ("narrateur", "L'écaille d'étain voyage dans la poche."),
            ("maman", "Les géraniums attendent, devant."),
            ("papa", "On y va, tous les quatre ?"),
            ("enfant-m", "Oui."),
        ),
        choice=L(
            ("narrateur", "Le seau tape sa hanche, à chaque pas."),
            ("narrateur", "Le bassin fume un peu, bas."),
            ("narrateur", "Sous l'arche, le ruisseau file."),
            ("narrateur", "Les géraniums pendent contre le mur."),
            ("papa", "Vous allez où, pour nager ?"),
        ),
    ),
}

T2_LABS = ("le bassin", "le ruisseau", "les géraniums")
T3_LABS = {
    1: ("le torchon de maman", "les mains d'Aniss", "un pas en arrière"),
    2: ("l'élastique de maman", "la serviette", "Aniss tient le filet"),
    3: ("les manches retroussées", "Raphaël tient le seau", "maman noue les poignets"),
}


def t2_bassin(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Raphaël pose le poisson au bord du bassin.",
        2: "Raphaël plonge le filet dans le bassin.",
        3: "Raphaël penche le seau vers le bassin.",
    }[a]
    mishap = {
        1: "Le poisson glisse, trop loin.",
        2: "Le filet vise à côté, trop bas.",
        3: "Le seau éclabousse, trop bas.",
    }[a]
    ruse = {
        1: "L'écaille d'étain disparaît dans la buée.",
        2: "L'écaille d'étain se perd dans les mailles floues.",
        3: "L'écaille d'étain tombe dans le jet, cachée.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-m", "Vite, il nage, Aniss !"),
        ("narrateur", "Le jet frappe la pierre, fin."),
        ("copain", "Je vois un nuage sur mes lunettes."),
        ("narrateur", "Un rond d'eau cache le bassin."),
        ("narrateur", mishap),
        ("enfant-m", "Il n'attendait pas ça."),
        ("narrateur", "Le sourire de Raphaël disparaît."),
        ("papa", "Je m'accroupis, à votre hauteur."),
        ("narrateur", ruse),
        ("enfant-m", "On plonge, on la reprend !"),
        ("copain", "Attends, je ne plonge pas."),
        ("papa", "Toi tu vois net, lui un peu flou."),
        ("maman", "L'eau est floue, vous faites quoi ?"),
    )


def t2_ruisseau(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Raphaël pose le poisson sous l'arche.",
        2: "Raphaël tend le filet sous l'arche.",
        3: "Raphaël penche le seau sous l'arche.",
    }[a]
    mishap = {
        1: "Une mèche mouillée couvre le poisson.",
        2: "Le filet accroche une mèche, pas l'eau.",
        3: "Une goutte de cheveu tombe dans le seau.",
    }[a]
    ruse = {
        1: "L'écaille d'étain part avec le courant, sous l'arche.",
        2: "L'écaille d'étain s'accroche à une mèche, puis file.",
        3: "L'écaille d'étain glisse au fond du courant.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-m", "Ici, l'eau file, Aniss."),
        ("copain", "Mes cheveux sont trop lourds."),
        ("narrateur", mishap),
        ("narrateur", "Une goutte tape la dalle, toc."),
        ("enfant-m", "On peut jouer avec lui ?"),
        ("narrateur", "Dans sa poitrine, l'envie se bouscule."),
        ("maman", "Je m'accroupis, à votre hauteur."),
        ("narrateur", ruse),
        ("enfant-m", "Vite, on la rattrape !"),
        ("copain", "Non, je reste là."),
        ("papa", "Toi tes cheveux tiennent, les siens gouttent."),
        ("maman", "Les mèches tombent, vous faites quoi ?"),
    )


def t2_geraniums(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Raphaël tend le poisson vers les fleurs.",
        2: "Raphaël glisse le filet entre les pots.",
        3: "Raphaël pose le seau près des pots.",
    }[a]
    mishap = {
        1: "Une manche trop longue emporte le poisson.",
        2: "Une manche trop longue balaie le filet.",
        3: "Une manche trop longue renverse un peu d'eau.",
    }[a]
    objet = {1: "Le poisson", 2: "Le filet", 3: "Le seau"}[a]
    ruse = {
        1: "L'écaille d'étain disparaît sous un pétale rouge.",
        2: "L'écaille d'étain se cache sous une feuille.",
        3: "L'écaille d'étain s'enfonce dans la terre mouillée.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-m", "Les fleurs sont notre port, Aniss."),
        ("copain", "Mon manteau me suit jusqu'aux genoux !"),
        ("narrateur", mishap),
        ("narrateur", f"{objet} disparaît un instant, sous le tissu."),
        ("enfant-m", "Je n'aime pas ça."),
        ("narrateur", "L'inquiétude suit, juste derrière."),
        ("papa", "Je m'accroupis, à votre hauteur."),
        ("narrateur", ruse),
        ("enfant-m", "On la cherche, tout de suite !"),
        ("copain", "Moi, je ne rentre pas dans les pots."),
        ("papa", "Toi tes manches s'arrêtent, les siennes voyagent."),
        ("maman", "Le manteau et l'eau, vous faites comment ?"),
    )


T2_FN = {1: t2_bassin, 2: t2_ruisseau, 3: t2_geraniums}
T2_SONS = {1: "bassin,jet,pierre", 2: "ruisseau,goutte,arche", 3: "feuilles,tissu,terre"}
T2_EMPH = {1: "bassin", 2: "ruisseau", 3: "géraniums"}


def t3_choice(t2: int) -> list[tuple[str, str]]:
    if t2 == 1:
        return L(
            ("narrateur", "La buée reste sur les verres, fine."),
            ("narrateur", "L'écaille d'étain manque, dans l'eau."),
            ("papa", "Le torchon, les mains, ou un pas en arrière ?"),
        )
    if t2 == 2:
        return L(
            ("narrateur", "Une mèche mouillée touche l'eau."),
            ("narrateur", "L'écaille d'étain manque, sous l'arche."),
            ("maman", "L'élastique, la serviette, ou tenir le filet ?"),
        )
    return L(
        ("narrateur", "Les manches cachent le bois peint."),
        ("narrateur", "L'écaille d'étain manque, entre les pots."),
        ("papa", "Les manches, le seau, ou nouer les poignets ?"),
    )


T3_EMPH = {
    1: {1: "torchon", 2: "mains d'Aniss", 3: "pas en arrière"},
    2: {1: "élastique", 2: "serviette", 3: "filet"},
    3: {1: "manches", 2: "seau", 3: "poignets"},
}
T3_SONS = {
    (1, 1): "linge,verre",
    (1, 2): "mains,eau",
    (1, 3): "pas,air",
    (2, 1): "elastique,cheveux",
    (2, 2): "serviette,linge",
    (2, 3): "filet,mains",
    (3, 1): "tissu,coude",
    (3, 2): "seau,anse",
    (3, 3): "elastique,poignet",
}


def t3(a: int, b: int, c: int) -> list[tuple[str, str]]:
    table = {
        (1, 1, 1): L(
            ("enfant-m", "Maman, le torchon, s'il te plaît."),
            ("maman", "Tiens, sans presser, sur les verres."),
            ("narrateur", "Aniss frotte un rond, puis un autre."),
            ("narrateur", "Raphaël veut plonger, puis s'arrête."),
            ("enfant-m", "Je ne fonce pas."),
            ("papa", "Personne ne dit où chercher."),
            ("narrateur", "Raphaël écoute le jet, puis la pierre."),
            ("narrateur", "L'écaille d'étain brille, au bord, grise."),
            ("copain", "Je vois l'eau !"),
            ("enfant-m", "L'œil peint est à toi, maintenant."),
            ("narrateur", "Les lunettes rendent le bleu, net."),
            ("papa", "Vous jouez, chacun avec ce qu'il a."),
        ),
        (1, 1, 2): L(
            ("enfant-m", "Tu joues avec tes mains, Aniss."),
            ("copain", "Je touche, toi tu dis où."),
            ("narrateur", "Aniss palpe le poisson, Raphaël parle."),
            ("narrateur", "Papa s'accroupit, à leur hauteur."),
            ("enfant-m", "À gauche, tout froid."),
            ("copain", "Je le tiens !"),
            ("narrateur", "Personne ne donne la réponse."),
            ("narrateur", "L'écaille d'étain chauffe la paume."),
            ("enfant-m", "On a trouvé, sans plonger."),
            ("maman", "Les mains ont vu, à la place des verres."),
            ("narrateur", "Le poisson guide le geste, au milieu."),
        ),
        (1, 1, 3): L(
            ("enfant-m", "On recule un peu, papa ?"),
            ("papa", "Un pas, hors du jet, pas plus."),
            ("narrateur", "L'air sec chasse la buée, lent."),
            ("narrateur", "Le poisson attend au bord, puis glisse."),
            ("copain", "Ça redevient clair !"),
            ("enfant-m", "On ne plonge pas vers l'écaille."),
            ("narrateur", "Raphaël écoute le bassin, puis l'eau."),
            ("narrateur", "L'écaille d'étain clignote, sur la pierre sèche."),
            ("copain", "Je la vois, nette."),
            ("maman", "Vous avez attendu le verre clair."),
            ("narrateur", "Le jet reprend, plus loin."),
        ),
        (1, 2, 1): L(
            ("enfant-m", "On met l'élastique, plus haut."),
            ("copain", "Mes cheveux restent en arrière, alors."),
            ("narrateur", "Maman noue l'élastique, sans serrer."),
            ("narrateur", "Raphaël pose le poisson, hors des mèches."),
            ("enfant-m", "Tu peux te pencher, maintenant."),
            ("copain", "L'eau ne m'attrape plus."),
            ("narrateur", "Raphaël refuse de courir sous l'arche."),
            ("narrateur", "L'écaille d'étain brille, coincée dans une mèche."),
            ("copain", "Là, près du col."),
            ("papa", "Chacun a sa hauteur, près de l'arche."),
            ("narrateur", "Le poisson nage, hors des cheveux."),
        ),
        (1, 2, 2): L(
            ("enfant-m", "La serviette, maman ?"),
            ("maman", "Frotte, pas trop fort."),
            ("narrateur", "Aniss essuie une mèche, puis une autre."),
            ("narrateur", "Le poisson attend, le temps d'un frottement."),
            ("copain", "Elles sont plus légères !"),
            ("enfant-m", "On pose le poisson, maintenant."),
            ("narrateur", "Raphaël cherche l'écaille, sans foncer."),
            ("narrateur", "L'écaille d'étain était dans une mèche."),
            ("copain", "Elle brillait dans mes cheveux !"),
            ("papa", "Vous avez laissé l'eau des cheveux."),
            ("narrateur", "L'eau file, sans emporter de cheveu."),
        ),
        (1, 2, 3): L(
            ("enfant-m", "Tu tiens le filet, moi je pose."),
            ("copain", "Mes mains font le bord, alors."),
            ("narrateur", "Aniss tient le filet, Raphaël glisse le poisson."),
            ("narrateur", "L'eau s'ouvre quand Aniss recule."),
            ("narrateur", "Elle se ferme quand il avance."),
            ("enfant-m", "C'est toi le port, Aniss !"),
            ("copain", "Et toi le poisson."),
            ("enfant-m", "On ne court pas sous l'arche."),
            ("narrateur", "L'écaille d'étain reste au fond du filet, au sec."),
            ("papa", "Vous jouez avec ce que vous avez."),
            ("maman", "Les cheveux n'ont plus besoin d'être dans l'eau."),
        ),
        (1, 3, 1): L(
            ("enfant-m", "On retrousse, Aniss."),
            ("copain", "Jusqu'au coude, comme papa."),
            ("narrateur", "Deux rouleaux de tissu tiennent, épais."),
            ("narrateur", "Les manches remontent, le poisson redevient libre."),
            ("enfant-m", "Je te vois les mains, maintenant."),
            ("copain", "Le poisson n'est plus dans le manteau."),
            ("narrateur", "Raphaël s'arrête, au bord des pots."),
            ("narrateur", "L'écaille d'étain luit sous un pétale, puis se pose."),
            ("copain", "On attend qu'il s'arrête."),
            ("papa", "Les manches ont laissé l'eau passer."),
            ("narrateur", "Le bleu avance entre les pots."),
        ),
        (1, 3, 2): L(
            ("enfant-m", "Moi je tiens le seau."),
            ("copain", "Moi je guide, près des fleurs."),
            ("narrateur", "Raphaël tient le seau, Aniss pose le poisson."),
            ("narrateur", "Les manches trop longues bougent le tissu, seulement."),
            ("narrateur", "Le bois peint reste hors du manteau."),
            ("copain", "Le port s'ouvre !"),
            ("enfant-m", "On ne rentre pas dans les pots."),
            ("narrateur", "Personne ne dit le geste."),
            ("narrateur", "L'écaille d'étain clignote, entre deux feuilles."),
            ("papa", "Chacun a pris sa part, à sa taille."),
            ("maman", "Les fleurs ont tenu l'eau."),
        ),
        (1, 3, 3): L(
            ("enfant-m", "Maman, ton élastique, s'il te plaît."),
            ("maman", "Un pour chaque manche, sans trop serrer."),
            ("narrateur", "Aniss tend les poignets, maman noue."),
            ("narrateur", "L'élastique tient une manche, le poisson l'autre main."),
            ("copain", "Mes mains sont nues, maintenant."),
            ("enfant-m", "Le poisson peut nager."),
            ("narrateur", "Raphaël refuse de foncer entre les pots."),
            ("narrateur", "L'écaille d'étain brille, au creux d'une terre mouillée."),
            ("copain", "Je la prends, sans presser."),
            ("papa", "Vous avez demandé, et ça tient."),
            ("maman", "Mes élastiques ont gardé le manteau."),
        ),
        (2, 1, 1): L(
            ("enfant-m", "Maman, le torchon, pour ses verres."),
            ("maman", "Sans presser, Aniss, un rond après l'autre."),
            ("narrateur", "Aniss frotte, le filet au bras."),
            ("narrateur", "Raphaël lève un pied, puis le repose."),
            ("enfant-m", "On ne plonge pas."),
            ("papa", "Regarde le filet, pas le jet."),
            ("narrateur", "Raphaël écoute les mailles, puis la pierre."),
            ("narrateur", "L'écaille d'étain tapote une maille, tic."),
            ("copain", "Elle est là, dans le filet !"),
            ("enfant-m", "Le filet l'a gardée."),
            ("narrateur", "Le jet laisse le filet, net."),
            ("maman", "Le torchon a rendu le bassin."),
        ),
        (2, 1, 2): L(
            ("enfant-m", "Tes mains voient, Aniss."),
            ("copain", "Je palpe le bord, tu parles."),
            ("narrateur", "Aniss palpe le filet, Raphaël parle."),
            ("narrateur", "Maman s'accroupit, à leur hauteur."),
            ("enfant-m", "Le froid, c'est l'écaille."),
            ("copain", "Je la sens !"),
            ("narrateur", "Personne ne donne la réponse."),
            ("narrateur", "L'écaille d'étain roule contre le pouce."),
            ("enfant-m", "Sans les verres, tu as trouvé."),
            ("papa", "Les mains ont vu, à la place des lunettes."),
            ("narrateur", "Le filet reste droit, au sec."),
        ),
        (2, 1, 3): L(
            ("enfant-m", "Un pas, hors du jet."),
            ("papa", "Pas plus, l'air sèche les verres."),
            ("narrateur", "Le filet claque un peu, puis s'apaise."),
            ("copain", "Ça redevient clair !"),
            ("enfant-m", "Le poisson peut nager."),
            ("narrateur", "Aniss ajuste ses lunettes, nettes."),
            ("narrateur", "Raphaël cherche l'écaille, sans foncer."),
            ("narrateur", "L'écaille d'étain brille, sur une dalle sèche."),
            ("copain", "Je la vois, enfin."),
            ("maman", "Le pas en arrière a rendu l'eau."),
            ("papa", "Vous avez laissé le temps aux lunettes."),
        ),
        (2, 2, 1): L(
            ("enfant-m", "L'élastique, plus haut que les yeux."),
            ("copain", "Mes cheveux restent libres, alors."),
            ("narrateur", "Maman noue, Aniss penche le filet."),
            ("narrateur", "Raphaël tend le filet, hors des mèches."),
            ("enfant-m", "Tu peux te pencher, maintenant."),
            ("copain", "L'eau ne m'attrape plus."),
            ("narrateur", "Raphaël refuse de chasser le courant."),
            ("narrateur", "L'écaille d'étain brille, collée à une maille."),
            ("copain", "Elle est restée avec nous."),
            ("papa", "Chacun a sa hauteur, sous l'arche."),
            ("narrateur", "Le filet vert tient, sans une mèche."),
        ),
        (2, 2, 2): L(
            ("enfant-m", "La serviette, pour tes mèches."),
            ("maman", "Frotte, sans trop tirer."),
            ("narrateur", "Aniss essuie, le filet entre les genoux."),
            ("narrateur", "Le filet attend, le temps d'un frottement."),
            ("copain", "Elles sont plus légères !"),
            ("enfant-m", "On tend le filet, maintenant."),
            ("narrateur", "Raphaël observe la dalle, pas le courant."),
            ("narrateur", "L'écaille d'étain était sous une mèche lourde."),
            ("copain", "Elle brillait contre mon cou !"),
            ("papa", "Vous avez laissé l'eau des cheveux."),
            ("narrateur", "Le ruisseau file, sans emporter de cheveu."),
        ),
        (2, 2, 3): L(
            ("enfant-m", "Tu tiens le filet à deux mains."),
            ("copain", "Sans me pencher, alors."),
            ("narrateur", "Aniss tient le filet à deux mains, sans se pencher."),
            ("narrateur", "Le poisson glisse dedans, cette fois."),
            ("enfant-m", "C'est toi le port vivant !"),
            ("copain", "Et toi, tu poses."),
            ("narrateur", "Raphaël pose, sans courir."),
            ("narrateur", "L'écaille d'étain reste au fond, au chaud."),
            ("copain", "Je la garde, ici."),
            ("papa", "Vous jouez avec ce que vous avez."),
            ("maman", "Les cheveux n'ont plus besoin d'être dans l'eau."),
        ),
        (2, 3, 1): L(
            ("enfant-m", "On retrousse, jusqu'au coude."),
            ("copain", "Comme papa, deux rouleaux."),
            ("narrateur", "Deux rouleaux de tissu tiennent, épais."),
            ("narrateur", "Les manches remontent, le filet redevient visible."),
            ("enfant-m", "Je te vois les mains, maintenant."),
            ("copain", "Le filet n'est plus dans le manteau."),
            ("narrateur", "Raphaël s'arrête, le filet au bord."),
            ("narrateur", "L'écaille d'étain luit, puis revient."),
            ("copain", "On attend qu'elle s'arrête."),
            ("papa", "Les manches ont laissé l'eau passer."),
            ("narrateur", "Le filet reprend sa place, au milieu."),
        ),
        (2, 3, 2): L(
            ("enfant-m", "Moi je tiens le seau."),
            ("copain", "Moi je glisse le filet."),
            ("narrateur", "Raphaël tient le seau, Aniss y glisse le filet."),
            ("narrateur", "Les manches trop longues bougent le tissu, seulement."),
            ("narrateur", "Les mailles restent hors du manteau."),
            ("copain", "Le port s'ouvre !"),
            ("enfant-m", "On ne rentre pas dans les pots."),
            ("narrateur", "Personne ne dit le geste."),
            ("narrateur", "L'écaille d'étain clignote, contre l'anse."),
            ("papa", "Chacun a pris sa part, à sa taille."),
            ("maman", "Les fleurs ont tenu l'eau."),
        ),
        (2, 3, 3): L(
            ("enfant-m", "Maman, tes élastiques, pour ses manches."),
            ("maman", "Un pour chaque poignet, sans trop serrer."),
            ("narrateur", "Aniss tend les poignets, maman noue."),
            ("narrateur", "L'élastique tient une manche, le filet l'autre main."),
            ("copain", "Mes mains sont nues, maintenant."),
            ("enfant-m", "Le poisson peut nager."),
            ("narrateur", "Raphaël refuse de foncer entre les pots."),
            ("narrateur", "L'écaille d'étain brille, au creux d'une terre mouillée."),
            ("copain", "Je la prends, sans presser."),
            ("papa", "Vous avez demandé, et ça tient."),
            ("maman", "Mes élastiques ont gardé le manteau."),
        ),
        (3, 1, 1): L(
            ("enfant-m", "Le torchon, maman, pour ses verres."),
            ("maman", "Un rond, puis l'autre, Aniss."),
            ("narrateur", "Aniss frotte, Raphaël reprend l'anse du seau."),
            ("narrateur", "Raphaël veut plonger, puis s'arrête."),
            ("enfant-m", "On ne fonce pas."),
            ("papa", "Le seau peut verser, sans éclabousser."),
            ("narrateur", "Raphaël penche l'anse, bas."),
            ("narrateur", "L'écaille d'étain brille, au fond du seau."),
            ("copain", "Je vois le bleu !"),
            ("enfant-m", "Le seau l'a gardée."),
            ("narrateur", "Le jet laisse le métal, net."),
            ("maman", "Le torchon a rendu le bassin."),
        ),
        (3, 1, 2): L(
            ("enfant-m", "Tes mains, Aniss, moi je parle."),
            ("copain", "Je palpe, tu dis où."),
            ("narrateur", "Aniss palpe l'anse, Raphaël parle."),
            ("narrateur", "Papa s'accroupit, à leur hauteur."),
            ("enfant-m", "Le froid, sous le métal."),
            ("copain", "Je la tiens !"),
            ("narrateur", "Personne ne donne la réponse."),
            ("narrateur", "L'écaille d'étain chauffe la paume."),
            ("enfant-m", "On a trouvé, sans plonger."),
            ("maman", "Les mains ont vu, à la place des verres."),
            ("narrateur", "Le seau reste droit, au milieu."),
        ),
        (3, 1, 3): L(
            ("enfant-m", "Un pas, hors du jet."),
            ("papa", "L'air sèche, pas plus loin."),
            ("narrateur", "Le seau sonne, puis le métal se tait."),
            ("copain", "Ça redevient clair !"),
            ("enfant-m", "Le poisson peut nager."),
            ("narrateur", "Aniss ajuste ses lunettes, nettes."),
            ("narrateur", "Raphaël cherche l'écaille, sans foncer."),
            ("narrateur", "L'écaille d'étain clignote, sur le métal sec."),
            ("copain", "Je la vois, nette."),
            ("maman", "Vous avez attendu le verre clair."),
            ("papa", "Le seau a marqué la dalle sèche."),
        ),
        (3, 2, 1): L(
            ("enfant-m", "L'élastique, plus haut."),
            ("copain", "Mes cheveux restent en arrière, alors."),
            ("narrateur", "Maman noue l'élastique, sans serrer."),
            ("narrateur", "Raphaël penche le seau, hors des mèches."),
            ("enfant-m", "Tu peux te pencher, maintenant."),
            ("copain", "L'eau ne m'attrape plus."),
            ("narrateur", "Raphaël refuse de courir sous l'arche."),
            ("narrateur", "L'écaille d'étain brille, collée à l'anse."),
            ("copain", "Elle est restée au seau."),
            ("papa", "Chacun a sa hauteur, près de l'arche."),
            ("narrateur", "Le seau bleu tient, sans une mèche."),
        ),
        (3, 2, 2): L(
            ("enfant-m", "La serviette, pour tes mèches."),
            ("maman", "Frotte, sans trop tirer."),
            ("narrateur", "Aniss essuie, le seau entre les genoux."),
            ("narrateur", "Le seau attend, le temps d'un frottement."),
            ("copain", "Elles sont plus légères !"),
            ("enfant-m", "On penche le seau, maintenant."),
            ("narrateur", "Raphaël observe la dalle, pas le courant."),
            ("narrateur", "L'écaille d'étain était sous une mèche lourde."),
            ("copain", "Elle brillait contre mon cou !"),
            ("papa", "Vous avez laissé l'eau des cheveux."),
            ("narrateur", "Le ruisseau file, sans emporter de cheveu."),
        ),
        (3, 2, 3): L(
            ("enfant-m", "Tu tiens le filet, moi le seau."),
            ("copain", "Mes mains font le bord, alors."),
            ("narrateur", "Aniss tient le filet, Raphaël penche le seau."),
            ("narrateur", "L'eau s'ouvre quand Aniss recule."),
            ("narrateur", "Elle se ferme quand il avance."),
            ("enfant-m", "C'est toi le port, Aniss !"),
            ("copain", "Et toi le seau."),
            ("enfant-m", "On ne court pas sous l'arche."),
            ("narrateur", "L'écaille d'étain reste au fond du seau, au sec."),
            ("papa", "Vous jouez avec ce que vous avez."),
            ("maman", "Les cheveux n'ont plus besoin d'être dans l'eau."),
        ),
        (3, 3, 1): L(
            ("enfant-m", "On retrousse, Aniss."),
            ("copain", "Jusqu'au coude, comme papa."),
            ("narrateur", "Deux rouleaux de tissu tiennent, épais."),
            ("narrateur", "Les manches remontent, le seau redevient visible."),
            ("enfant-m", "Je te vois les mains, maintenant."),
            ("copain", "Le seau n'est plus dans le manteau."),
            ("narrateur", "Raphaël s'arrête, le seau au bord."),
            ("narrateur", "L'écaille d'étain luit, puis revient."),
            ("copain", "On attend qu'elle s'arrête."),
            ("papa", "Les manches ont laissé l'eau passer."),
            ("narrateur", "Le seau reprend sa place, au milieu."),
        ),
        (3, 3, 2): L(
            ("enfant-m", "Moi je tiens le seau."),
            ("copain", "Moi je guide, près des fleurs."),
            ("narrateur", "Raphaël tient le seau, Aniss verse, sans presser."),
            ("narrateur", "Les manches trop longues bougent le tissu, seulement."),
            ("narrateur", "Le métal reste hors du manteau."),
            ("copain", "Le port s'ouvre !"),
            ("enfant-m", "On ne rentre pas dans les pots."),
            ("narrateur", "Personne ne dit le geste."),
            ("narrateur", "L'écaille d'étain clignote, contre l'anse."),
            ("papa", "Chacun a pris sa part, à sa taille."),
            ("maman", "Les fleurs ont tenu l'eau."),
        ),
        (3, 3, 3): L(
            ("enfant-m", "Maman, tes élastiques, pour ses manches."),
            ("maman", "Un pour chaque poignet, sans trop serrer."),
            ("narrateur", "Aniss tend les poignets, maman noue."),
            ("narrateur", "L'élastique tient une manche, le seau reste droit."),
            ("copain", "Mes mains sont nues, maintenant."),
            ("enfant-m", "Le poisson peut nager."),
            ("narrateur", "Raphaël refuse de foncer entre les pots."),
            ("narrateur", "L'écaille d'étain brille, au creux d'une terre mouillée."),
            ("copain", "Je la prends, sans presser."),
            ("papa", "Vous avez demandé, et ça tient."),
            ("maman", "Mes élastiques ont gardé le manteau."),
        ),
    }
    if (a, b, c) not in table:
        raise SystemExit(f"T3 manquant {(a, b, c)}")
    return table[(a, b, c)]


def fin(a: int, b: int, c: int) -> list[tuple[str, str]]:
    table = {
        (1, 1, 1): L(
            ("narrateur", "Le bassin sent le torchon, tiède."),
            ("copain", "J'ai vu l'œil peint, net."),
            ("enfant-m", "Tes lunettes ont trouvé le bleu."),
            ("narrateur", "L'écaille d'étain porte une goutte, ronde."),
            ("papa", "Vous avez joué, chacun avec sa vue."),
            ("narrateur", "Ça a failli glisser trop loin."),
            ("enfant-m", "On rentre, Aniss."),
            ("narrateur", "Une goutte tient sur l'écaille d'étain."),
        ),
        (1, 1, 2): L(
            ("narrateur", "Sous le jet, l'air est un peu froid."),
            ("enfant-m", "Tu as touché, moi j'ai dit où."),
            ("copain", "Mes mains ont vu le bleu."),
            ("narrateur", "L'écaille d'étain sèche dans la paume."),
            ("papa", "Les verres flous n'ont pas arrêté l'eau."),
            ("narrateur", "Un instant, le poisson filait."),
            ("enfant-m", "À demain, l'eau."),
            ("narrateur", "Une ombre de poisson reste au fond."),
        ),
        (1, 1, 3): L(
            ("narrateur", "Un filet d'air sec reste près du bassin."),
            ("copain", "La buée est partie, seule."),
            ("enfant-m", "On a attendu le verre clair."),
            ("narrateur", "L'écaille d'étain luit sur la dalle sèche."),
            ("maman", "Le pas en arrière a rendu l'eau."),
            ("narrateur", "L'eau partait, presque."),
            ("copain", "Il brille."),
            ("narrateur", "Raphaël souffle sur l'œil peint."),
        ),
        (1, 2, 1): L(
            ("narrateur", "L'arche garde un peu d'ombre."),
            ("enfant-m", "L'élastique était trop bas, d'abord."),
            ("copain", "Mes cheveux sont restés libres."),
            ("narrateur", "L'écaille d'étain sèche contre le col."),
            ("papa", "Chacun a eu sa hauteur, près de l'eau."),
            ("narrateur", "Le courant a failli l'emporter."),
            ("enfant-m", "On rentre, l'arche reste."),
            ("narrateur", "Une mèche sèche contre le col."),
        ),
        (1, 2, 2): L(
            ("narrateur", "La serviette sent le savon, un peu."),
            ("copain", "Tu as frotté, sans presser."),
            ("enfant-m", "Puis on a posé, sans emporter de cheveu."),
            ("narrateur", "L'écaille d'étain luit, propre, au dos."),
            ("maman", "L'eau des cheveux s'en est allée."),
            ("narrateur", "Un instant, une mèche couvrait tout."),
            ("copain", "Elle part."),
            ("narrateur", "Le savon s'efface de la pierre."),
        ),
        (1, 2, 3): L(
            ("narrateur", "Les mains d'Aniss gardent le pli du filet."),
            ("enfant-m", "Tu étais le port vivant."),
            ("copain", "Toi le poisson, moi l'ouverture."),
            ("narrateur", "L'écaille d'étain reste au fond du filet."),
            ("papa", "Vous avez joué avec ce que vous aviez."),
            ("narrateur", "Ça a failli filer sous l'arche."),
            ("enfant-m", "On se dit au revoir, arche."),
            ("narrateur", "Un rebord vide attend, bas."),
        ),
        (1, 3, 1): L(
            ("narrateur", "Deux rouleaux de manches tiennent."),
            ("enfant-m", "Tes mains sont sorties du manteau."),
            ("copain", "Le poisson n'était plus avalé."),
            ("narrateur", "L'écaille d'étain porte un grain de terre."),
            ("papa", "Les manches ont laissé l'eau passer."),
            ("narrateur", "Un instant, le manteau gagnait."),
            ("enfant-m", "On rentre, Aniss."),
            ("narrateur", "Un pétale rouge reste sur le bois."),
        ),
        (1, 3, 2): L(
            ("narrateur", "Une goutte tombe d'une feuille."),
            ("copain", "Tu tenais le seau, moi le bord."),
            ("enfant-m", "Tes manches bougeaient seulement le tissu."),
            ("narrateur", "L'écaille d'étain sèche entre deux feuilles."),
            ("maman", "Chacun a pris sa part, à sa taille."),
            ("narrateur", "Ça a failli se perdre sous un pétale."),
            ("copain", "Il a bien nagé."),
            ("narrateur", "Raphaël lisse le dos du poisson."),
        ),
        (1, 3, 3): L(
            ("narrateur", "Deux élastiques veillent aux poignets."),
            ("enfant-m", "On a demandé, et ça tenait."),
            ("copain", "Mes mains étaient nues, pour l'eau."),
            ("narrateur", "L'écaille d'étain brille, au creux de la terre."),
            ("papa", "Vous avez demandé, rien de plus."),
            ("narrateur", "Les pots ont failli tout cacher."),
            ("enfant-m", "L'eau est à nous."),
            ("narrateur", "Un peu de terre reste au rebord."),
        ),
        (2, 1, 1): L(
            ("narrateur", "Le bassin sent le linge, tiède."),
            ("copain", "J'ai vu les mailles, nettes."),
            ("enfant-m", "Le filet a gardé l'écaille."),
            ("narrateur", "L'écaille d'étain tapote une maille, une fois."),
            ("maman", "Le torchon a rendu le bleu."),
            ("narrateur", "Ça a failli viser trop bas."),
            ("enfant-m", "On rentre, Aniss."),
            ("narrateur", "Le filet vert sèche sur le rebord."),
        ),
        (2, 1, 2): L(
            ("narrateur", "Sous le jet, les mailles restent froides."),
            ("enfant-m", "Tu as palpé, moi j'ai dit froid."),
            ("copain", "Mes mains ont vu le filet."),
            ("narrateur", "L'écaille d'étain sèche contre le pouce."),
            ("papa", "Les verres flous n'ont pas arrêté le filet."),
            ("narrateur", "Un instant, les mailles partaient."),
            ("enfant-m", "À demain, l'eau."),
            ("narrateur", "Une maille garde une goutte ronde."),
        ),
        (2, 1, 3): L(
            ("narrateur", "Un filet d'air sec reste près du bassin."),
            ("copain", "La buée est partie, seule."),
            ("enfant-m", "On a attendu le verre clair."),
            ("narrateur", "L'écaille d'étain luit dans le filet."),
            ("maman", "Le pas en arrière a rendu les mailles."),
            ("narrateur", "L'eau partait, presque."),
            ("copain", "Je la vois."),
            ("narrateur", "L'écaille d'étain luit dans le filet, grise."),
        ),
        (2, 2, 1): L(
            ("narrateur", "L'arche garde un peu d'ombre."),
            ("enfant-m", "L'élastique tenait, plus haut."),
            ("copain", "Mes cheveux sont restés libres."),
            ("narrateur", "L'écaille d'étain sèche sur une maille."),
            ("papa", "Chacun a eu sa hauteur, sous l'arche."),
            ("narrateur", "Le courant a failli prendre le filet."),
            ("enfant-m", "On rentre, l'arche reste."),
            ("narrateur", "L'élastique tient une mèche, libre."),
        ),
        (2, 2, 2): L(
            ("narrateur", "La serviette sent le ruisseau, un peu."),
            ("copain", "Tu as frotté, sans presser."),
            ("enfant-m", "Puis on a tendu, sans emporter de cheveu."),
            ("narrateur", "L'écaille d'étain luit, propre, dans le filet."),
            ("maman", "L'eau des cheveux s'en est allée."),
            ("narrateur", "Un instant, une mèche couvrait tout."),
            ("copain", "Elles sont légères."),
            ("narrateur", "La serviette sent le ruisseau, froide."),
        ),
        (2, 2, 3): L(
            ("narrateur", "Les mains d'Aniss gardent le pli du filet."),
            ("enfant-m", "Tu étais le port vivant."),
            ("copain", "Toi tu poses, moi j'ouvre."),
            ("narrateur", "L'écaille d'étain reste au fond, au chaud."),
            ("papa", "Vous avez joué avec ce que vous aviez."),
            ("narrateur", "Ça a failli filer sous l'arche."),
            ("enfant-m", "On se dit au revoir, arche."),
            ("narrateur", "Les mains d'Aniss gardent le pli du filet, tiède."),
        ),
        (2, 3, 1): L(
            ("narrateur", "Deux rouleaux de manches tiennent."),
            ("enfant-m", "Tes mains sont sorties du manteau."),
            ("copain", "Le filet n'était plus avalé."),
            ("narrateur", "L'écaille d'étain porte un grain de terre."),
            ("papa", "Les manches ont laissé l'eau passer."),
            ("narrateur", "Un instant, le manteau gagnait."),
            ("enfant-m", "On rentre, Aniss."),
            ("narrateur", "Deux rouleaux de manches tiennent, épais."),
        ),
        (2, 3, 2): L(
            ("narrateur", "Une goutte tombe d'une feuille."),
            ("copain", "Tu tenais le seau, moi le filet."),
            ("enfant-m", "Tes manches bougeaient seulement le tissu."),
            ("narrateur", "L'écaille d'étain sèche contre l'anse."),
            ("maman", "Chacun a pris sa part, à sa taille."),
            ("narrateur", "Ça a failli se perdre sous une feuille."),
            ("copain", "Les mailles ont nagé."),
            ("narrateur", "Une feuille de géranium colle au filet."),
        ),
        (2, 3, 3): L(
            ("narrateur", "Deux élastiques veillent aux poignets."),
            ("enfant-m", "On a demandé, et ça tenait."),
            ("copain", "Mes mains étaient nues, pour l'eau."),
            ("narrateur", "L'écaille d'étain brille, au creux de la terre."),
            ("papa", "Vous avez demandé, rien de plus."),
            ("narrateur", "Les pots ont failli tout cacher."),
            ("enfant-m", "L'eau est à nous."),
            ("narrateur", "Deux élastiques veillent aux poignets, serrés."),
        ),
        (3, 1, 1): L(
            ("narrateur", "Le bassin sent le métal, tiède."),
            ("copain", "J'ai vu le bleu, net."),
            ("enfant-m", "Le seau a gardé l'écaille."),
            ("narrateur", "L'écaille d'étain tremble dans l'eau du seau."),
            ("maman", "Le torchon a rendu le jet."),
            ("narrateur", "Ça a failli éclabousser trop bas."),
            ("enfant-m", "On rentre, Aniss."),
            ("narrateur", "Le seau bleu garde une goutte, au fond."),
        ),
        (3, 1, 2): L(
            ("narrateur", "Sous le jet, l'anse reste froide."),
            ("enfant-m", "Tu as palpé, moi j'ai dit froid."),
            ("copain", "Mes mains ont vu le seau."),
            ("narrateur", "L'écaille d'étain sèche contre le pouce."),
            ("papa", "Les verres flous n'ont pas arrêté le seau."),
            ("narrateur", "Un instant, le métal partait."),
            ("enfant-m", "À demain, l'eau."),
            ("narrateur", "L'anse sonne une fois, puis se tait."),
        ),
        (3, 1, 3): L(
            ("narrateur", "Un filet d'air sec reste près du bassin."),
            ("copain", "La buée est partie, seule."),
            ("enfant-m", "On a attendu le verre clair."),
            ("narrateur", "L'écaille d'étain luit sur le métal sec."),
            ("maman", "Le pas en arrière a rendu le seau."),
            ("narrateur", "L'eau partait, presque."),
            ("copain", "Je la vois."),
            ("narrateur", "L'écaille d'étain tremble dans l'eau du seau, ronde."),
        ),
        (3, 2, 1): L(
            ("narrateur", "L'arche garde un peu d'ombre."),
            ("enfant-m", "L'élastique tenait, plus haut."),
            ("copain", "Mes cheveux sont restés libres."),
            ("narrateur", "L'écaille d'étain sèche sur l'anse."),
            ("papa", "Chacun a eu sa hauteur, près de l'eau."),
            ("narrateur", "Le courant a failli prendre le seau."),
            ("enfant-m", "On rentre, l'arche reste."),
            ("narrateur", "Une mèche sèche sur l'anse bleue."),
        ),
        (3, 2, 2): L(
            ("narrateur", "La serviette sent le ruisseau, un peu."),
            ("copain", "Tu as frotté, sans presser."),
            ("enfant-m", "Puis on a penché, sans emporter de cheveu."),
            ("narrateur", "L'écaille d'étain luit, propre, au fond."),
            ("maman", "L'eau des cheveux s'en est allée."),
            ("narrateur", "Un instant, une mèche couvrait tout."),
            ("copain", "Elles sont légères."),
            ("narrateur", "Une goutte tombe de la serviette, seule."),
        ),
        (3, 2, 3): L(
            ("narrateur", "Les mains d'Aniss gardent le pli du filet."),
            ("enfant-m", "Tu étais le port vivant."),
            ("copain", "Toi le seau, moi l'ouverture."),
            ("narrateur", "L'écaille d'étain reste au fond du seau."),
            ("papa", "Vous avez joué avec ce que vous aviez."),
            ("narrateur", "Ça a failli filer sous l'arche."),
            ("enfant-m", "On se dit au revoir, arche."),
            ("narrateur", "Le filet et le seau se touchent, mouillés."),
        ),
        (3, 3, 1): L(
            ("narrateur", "Deux rouleaux de manches tiennent."),
            ("enfant-m", "Tes mains sont sorties du manteau."),
            ("copain", "Le seau n'était plus avalé."),
            ("narrateur", "L'écaille d'étain porte un grain de terre."),
            ("papa", "Les manches ont laissé l'eau passer."),
            ("narrateur", "Un instant, le manteau gagnait."),
            ("enfant-m", "On rentre, Aniss."),
            ("narrateur", "Un pétale rouge flotte dans le seau."),
        ),
        (3, 3, 2): L(
            ("narrateur", "Une goutte tombe d'une feuille."),
            ("copain", "Tu tenais le seau, moi le bord."),
            ("enfant-m", "Tes manches bougeaient seulement le tissu."),
            ("narrateur", "L'écaille d'étain sèche contre l'anse."),
            ("maman", "Chacun a pris sa part, à sa taille."),
            ("narrateur", "Ça a failli se perdre sous un pétale."),
            ("copain", "Le seau a bien versé."),
            ("narrateur", "Raphaël pose le seau, sans une goutte de trop."),
        ),
        (3, 3, 3): L(
            ("narrateur", "Deux élastiques veillent aux poignets."),
            ("enfant-m", "On a demandé, et ça tenait."),
            ("copain", "Mes mains étaient nues, pour l'eau."),
            ("narrateur", "L'écaille d'étain brille, au creux de la terre."),
            ("papa", "Vous avez demandé, rien de plus."),
            ("narrateur", "Les pots ont failli tout cacher."),
            ("enfant-m", "L'eau est à nous."),
            ("narrateur", "Les poignets noués s'ouvrent, libres."),
        ),
    }
    if (a, b, c) not in table:
        raise SystemExit(f"FIN manquante {(a, b, c)}")
    return table[(a, b, c)]


FIN_SONS = {
    1: "bassin,goutte,pierre",
    2: "ruisseau,arche,silence",
    3: "feuilles,terre,silence",
}


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "gouttiere,pierre,pas", "emphasis": "écaille d'étain"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Près de la pierre, le poisson attend."),
            ("narrateur", "Le filet vert dort, plié."),
            ("narrateur", "Le seau bleu penche, vide."),
            ("narrateur", "L'écaille d'étain cliquette, une fois."),
            ("maman", "Tu prends quoi d'abord, Raphaël ?"),
        ),
        "choice",
        extra={"sons": "", "fields": t3lab("le poisson de bois", "le filet vert", "le seau bleu")},
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
            extra={"sons": "", "emphasis": "écaille d'étain"},
        )
        tid = f"{base}_T0002_P0000"
        by[tid] = voice(
            by_old[tid], t1["choice"], "choice",
            extra={"sons": "", "fields": t3lab(*T2_LABS)},
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
                extra={"sons": "", "fields": t3lab(*labs)},
            )
            for c in (1, 2, 3):
                leaf = f"{p2}_T0003_P000{c}"
                by[leaf] = voice(
                    by_old[leaf], t3(a, b, c), "resolution",
                    extra={"sons": T3_SONS[(b, c)], "emphasis": T3_EMPH[b][c]},
                )
                fin_id = f"{leaf}_F0001"
                by[fin_id] = voice(
                    by_old[fin_id], fin(a, b, c), "ending",
                    extra={"sons": FIN_SONS[b], "emphasis": "écaille d'étain"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra_ids = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    story = dict(src)
    story["fil_rouge"] = FIL
    story["title"] = TITLE
    story["characters"] = CHARS
    story["setting"] = SETTING
    story["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, story["age_band"], story["chunks"])

    blob = "\n".join(c["script"] for c in story["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in story["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for tic in TICS:
        if tic in whole:
            raise SystemExit(f"tic global: {tic}")
    if re.search(r"\b(encore|déjà|deja)\b", blob):
        raise SystemExit(f"{SID}: tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "raphaël" not in blob and "raphael" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "écaille d'étain" not in blob:
        raise SystemExit(f"{SID}: écaille d'étain absente")
    if "lavoir" not in blob or "poisson" not in blob:
        raise SystemExit(f"{SID}: lavoir/poisson absents")
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "j'ai compris",
        "mission accomplie",
        "merle",
        "miel",
        "grand-père",
        "maîtresse",
        "jardinier",
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "volet jaune",
        "tarte",
        "théâtre",
        "theatre",
        "marionnette",
        "bateau",
        "hugo",
        "zoé",
        "zoe",
        "sami",
        "ancre minuscule",
        "étoile brune",
        "fil pâle",
        "marque fine",
        "ombre-flèche",
        "perle de verre",
        "œillet de cuivre",
        "bouton de nacre",
        "nœud de raphia",
        "pois ivoire",
        "grain de savon",
        "bouton de lavande",
        "grain d'ambre",
        "virgule de buée",
        "croissant d'eau",
        "anneau de zinc",
        "larme de bronze",
        "bracelet d'écorce",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")

    fins = [c["text"] for c in story["chunks"] if c["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes {len(set(fins))}/27")
    lasts = []
    for c in story["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(last_n[-1])
        low = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in low or "bravo" in low or "bon travail" in low:
            raise SystemExit(f"fin mécanique: {last_n[-1]}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images {len(set(lasts))}/27")

    t3s = [c["text"] for c in story["chunks"] if re.search(r"T0003_P000[123]$", c["chunk_id"])]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"T3 distincts {len(set(t3s))}/27")

    t2s = [c["text"] for c in story["chunks"] if re.search(r"T0002_P000[123]$", c["chunk_id"])]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"T2 distincts {len(set(t2s))}/9")

    counts = [path_words(by, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    if any(c["text_xai_tags"] == c["text"] for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")
    if len(story["chunks"]) != 86:
        raise SystemExit(f"chunks {len(story['chunks'])}≠86")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-036 — Le poisson de bois de Raphaël au lavoir\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.COR.003 — jouer avec Aniss tel qu'il est "
        "(lunettes voilées, cheveux mouillés, manteau trop long) ; "
        "vécue, jamais dite. Raphaël propose, Aniss prend son temps. "
        "Le silence compte comme une réponse.\n"
        "- **Personnages :** Raphaël, Aniss, papa, maman (troupe D16)\n"
        "- **Lieu :** lavoir du village après la pluie : bassin, ruisseau, géraniums\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La gouttière du lavoir compte les gouttes. L'eau baisse. "
        "Raphaël veut que son **poisson de bois** nage avant que l'eau parte. "
        "Sur le dos, une **écaille d'étain** cliquette (indice unique, payé au climax). "
        "Aniss arrive lent : lunettes voilées, cheveux mouillés, manteau trop long. "
        "Raphaël veut poser maintenant ; Aniss veut regarder. "
        "Papa remercie Raphaël d'avoir attendu sa voix. "
        "T1 = poisson de bois / filet vert / seau bleu (les trois partent ; "
        "première idée trop vite : poisson sorti, filet jeté, seau balancé). "
        "T2 = bassin (buée) / ruisseau (mèches) / géraniums (manches) : "
        "l'écaille disparaît, Raphaël veut foncer, Aniss pose sa limite. "
        "T3 : torchon / mains / pas ; élastique / serviette / Aniss tient le filet ; "
        "manches / Raphaël tient le seau / maman noue les poignets. "
        "Ils refusent de foncer, retrouvent l'écaille, le poisson nage. "
        "Ça a failli ne pas nager. L'objet porte une trace.\n\n"
        "## Vécu\n\n"
        "Le sourire disparaît. L'envie et l'inquiétude se bousculent. "
        "Papa ou maman s'accroupit à la même hauteur. Personne ne donne la réponse. "
        "Raphaël observe l'écaille, écoute le lavoir, invente un geste à la taille d'Aniss. "
        "La leçon se voit : on joue ensemble, sans forcer l'autre à aller plus vite, "
        "sans rire des lunettes, des cheveux, du manteau.\n\n"
        "## Vu et corrigé\n\n"
        "- Gabarit 55 % et tics « encore / déjà / tout doux / tout calme » jetés.\n"
        "- Slogan « pas rire de l'apparence » / Hugo / bac-toboggan jetés.\n"
        "- Monde ≠ TREE-AUT-001 (pas de bateau-jardin) : lavoir, poisson de bois, géraniums.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (papa : tu as attendu sa voix). Question d'adulte. Un « en ce moment ».\n"
        "- Indice unique : écaille d'étain (inventée, payée au climax). Pas de gabarit v2 collé.\n"
        "- Ouverture : la gouttière compte les gouttes (pas les cinq manières recyclées).\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N2 ≤ 15. `check()` OK. Pas apply. Pas git. Pas audio.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks, 27 chemins, 27 fins distinctes, 27 dernières images\n"
        f"- {min(counts)} à {max(counts)} mots par chemin (moyenne {sum(counts)//len(counts)})\n"
        "- `text` = `script` collé ; graphe inchangé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
