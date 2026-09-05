#!/usr/bin/env python3
"""TREE-DIF-002 — Le pull bleu et les deux pommes (F-NAR-019, N2, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-002"
LIM = 15
TITLE = "Le pull bleu et les deux pommes"
CHARS = "Nino, Sarah, papa, maman"
SETTING = "jardin d'automne, pommier, cabane de planches"
FIL = (
    "L'odeur d'une pomme écrasée monte du chemin. Sur le poignet du pull bleu, "
    "un grain de pépin tient, brun. Nino veut porter les deux pommes jusqu'à "
    "la cabane de planches, avant la pluie, pour le goûter. Sarah arrive et "
    "s'arrête, sans un mot. T1 = pull bleu / panier / nappe, les trois partent. "
    "Première idée trop vite : manche avalée, toc, nappe trop serrée. "
    "T2 = pommier (les deux glissent) / cabane (la porte pince) / banc (la mince roule). "
    "Le grain faillit tomber. Nino veut foncer. Sarah pose sa limite. Silence = réponse. "
    "T3 : ils refusent de foncer, retrouvent le grain, font à deux. "
    "Les pommes arrivent. Ça a failli ne pas arriver."
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
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_grain_de_pepin_tient_au_poignet; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_maniere; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_le_pull_ou_les_pommes; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
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
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=trop_vite_les_pommes_resistent; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_inquiétude; intensite=2; destinataire=enfant; sous_texte=sarah_pose_sa_limite_le_grain_faillit; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=ils_refusent_de_foncer_retrouvent_le_grain; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_de_pepin_paie_le_debut; tempo=posé; sourire=léger; respiration=ample",
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
    ("narrateur", "L'odeur d'une pomme écrasée monte du chemin."),
    ("narrateur", "Une feuille jaune colle au soulier de Nino."),
    ("narrateur", "Derrière la maison, le jardin sent l'écorce mouillée."),
    ("narrateur", "Le pommier penche vers la cabane de planches."),
    ("narrateur", "Un pull bleu pend à la branche basse."),
    ("narrateur", "Les manches tombent trop bas, trop longues."),
    ("narrateur", "Sur le poignet, un grain de pépin tient."),
    ("enfant-m", "Il brille, collé au bleu."),
    ("papa", "Tu l'as vu, ce petit grain ?"),
    ("narrateur", "Deux pommes attendent dans l'herbe froide."),
    ("narrateur", "L'une est ronde, toute jaune."),
    ("narrateur", "L'autre est mince, avec une joue verte."),
    ("enfant-m", "Je les porte à la cabane."),
    ("enfant-m", "Avant la pluie."),
    ("maman", "Sarah arrive, par le petit chemin."),
    ("narrateur", "En ce moment, une goutte tape le bois."),
    ("enfant-f", "Nino."),
    ("narrateur", "Sarah s'arrête, sans un mot."),
    ("enfant-m", "Viens, on court avec les deux !"),
    ("narrateur", "Sarah ne bouge pas."),
    ("narrateur", "Nino sent ça, juste sous la gorge."),
    ("papa", "Merci, tu as vu qu'elle s'arrêtait."),
    ("maman", "On prépare le goûter, alors ?"),
)

T1 = {
    1: dict(
        name="le pull bleu",
        expected="trop grand",
        accepted="trop grand | grand | trop large | large | énorme | trop long",
        retry="Le pull de papa tombe trop bas.",
        ok="Oui, il est trop grand.",
        sons="tissu,branche",
        emphasis="pull",
        passage=L(
            ("narrateur", "Nino tire le pull trop vite, à la branche."),
            ("narrateur", "Une manche avale sa main, trop longue."),
            ("enfant-m", "Mes doigts sont partis !"),
            ("narrateur", "Sarah recule d'un pas."),
            ("enfant-f", "Attends."),
            ("narrateur", "Elle ne dit rien de plus."),
            ("enfant-m", "Je ralentis."),
            ("maman", "Garde le pull, il tient chaud."),
            ("papa", "Le panier, ensuite, et la nappe."),
            ("narrateur", "Il glisse les deux pommes contre le bleu."),
            ("narrateur", "Le grain de pépin reste au poignet."),
            ("papa", "Le pull d'abord, vous l'avez."),
        ),
        question=L(
            ("narrateur", "Nino a enfilé le pull de papa."),
            ("maman", "Le pull, il est comment ?"),
        ),
        confirm=L(
            ("narrateur", "Les manches traînent, et Nino avance."),
            ("enfant-f", "Tes mains, je les vois un peu."),
            ("enfant-m", "Le grain est là, sur le bleu."),
            ("narrateur", "Le panier et la nappe voyagent aussi."),
            ("narrateur", "Une goutte brille sur une feuille, sans tomber."),
            ("maman", "La cabane vous attend, au sec."),
            ("papa", "On y va, tous les quatre ?"),
            ("enfant-m", "Oui, papa."),
        ),
        choice=L(
            ("narrateur", "Le bleu frotte les genoux, trop long."),
            ("narrateur", "Sous le pommier, l'herbe est froide."),
            ("narrateur", "La cabane de planches attend, un peu sombre."),
            ("narrateur", "Le banc de bois luit, mouillé."),
            ("papa", "On pose le goûter où ?"),
        ),
    ),
    2: dict(
        name="le panier",
        expected="des pommes",
        accepted="pommes | des pommes | deux pommes | les pommes | une pomme",
        retry="Nino veut des pommes dans le panier.",
        ok="Oui, des pommes.",
        sons="osier,pomme",
        emphasis="panier",
        passage=L(
            ("narrateur", "Nino saisit l'anse du panier, trop vite."),
            ("narrateur", "Les deux pommes tombent dedans, toc."),
            ("narrateur", "La mince penche, presque dehors."),
            ("enfant-f", "Non."),
            ("narrateur", "Sarah pose une main sur le bord."),
            ("narrateur", "Elle reste là, les lèvres fermées."),
            ("enfant-m", "Je pose sans me presser."),
            ("papa", "L'osier gratte, Nino."),
            ("maman", "Le pull, ensuite, près du panier."),
            ("narrateur", "Elle glisse la nappe par-dessus."),
            ("narrateur", "Les trois affaires partent ensemble."),
            ("maman", "Le panier d'abord, il est prêt."),
        ),
        question=L(
            ("narrateur", "Le panier porte deux fruits, au fond."),
            ("papa", "Nino veut mettre quoi dedans ?"),
        ),
        confirm=L(
            ("narrateur", "Le panier tient les deux pommes, au fond."),
            ("enfant-f", "La mince ne penche plus."),
            ("enfant-m", "Le grain brille, sur le pull."),
            ("narrateur", "Le pull et la nappe voyagent aussi."),
            ("narrateur", "Une goutte brille sur une feuille, sans tomber."),
            ("papa", "La cabane vous attend, au sec."),
            ("maman", "Vos mains, dans les manches ?"),
            ("enfant-m", "Oui, maman."),
        ),
        choice=L(
            ("narrateur", "L'anse du panier tape la cuisse."),
            ("narrateur", "Sous le pommier, l'herbe est froide."),
            ("narrateur", "La cabane de planches attend, un peu sombre."),
            ("narrateur", "Le banc de bois luit, mouillé."),
            ("maman", "On pose le goûter où ?"),
        ),
    ),
    3: dict(
        name="la nappe",
        expected="la nappe",
        accepted="nappe | la nappe | une nappe",
        retry="Nino a déplié la nappe.",
        ok="Oui, la nappe.",
        sons="tissu,herbe",
        emphasis="nappe",
        passage=L(
            ("narrateur", "Nino déplie la nappe trop vite, dans l'herbe."),
            ("enfant-m", "Je cache les pommes, Sarah."),
            ("narrateur", "Il enroule trop fort, trop serré."),
            ("narrateur", "Les pommes glissent, un coin."),
            ("enfant-f", "Stop."),
            ("narrateur", "Sarah pose sa paume, sans parler."),
            ("enfant-m", "Je desserre."),
            ("maman", "Plie-la, comme un secret."),
            ("papa", "Le pull et le panier, avec vous."),
            ("narrateur", "Il les pose près de l'herbe."),
            ("narrateur", "Les trois affaires partent ensemble."),
            ("papa", "La nappe d'abord, elle est prête."),
        ),
        question=L(
            ("narrateur", "Un carré rouge et blanc sent l'herbe."),
            ("maman", "Nino a déplié quoi, d'abord ?"),
        ),
        confirm=L(
            ("narrateur", "La nappe pliée cache les pommes, au creux."),
            ("enfant-f", "Ça sent l'herbe."),
            ("enfant-m", "Le grain est là, sur le bleu."),
            ("narrateur", "Le pull et le panier voyagent aussi."),
            ("narrateur", "Une goutte brille sur une feuille, sans tomber."),
            ("maman", "La cabane vous attend, au sec."),
            ("papa", "On y va, tous les quatre ?"),
            ("enfant-f", "Oui."),
        ),
        choice=L(
            ("narrateur", "La nappe fait un paquet contre le ventre."),
            ("narrateur", "Sous le pommier, l'herbe est froide."),
            ("narrateur", "La cabane de planches attend, un peu sombre."),
            ("narrateur", "Le banc de bois luit, mouillé."),
            ("papa", "On pose le goûter où ?"),
        ),
    ),
}

T2_LABS = ("le pommier", "la cabane", "le banc")
T3_LABS = {
    1: ("les deux pommes", "attendre", "essuyer"),
    2: ("rouler les manches", "la couverture", "la cape"),
    3: ("couper", "caler", "partager"),
}
OBJ = {1: "le pull", 2: "le panier", 3: "la nappe"}
CAP = {1: "Le pull", 2: "Le panier", 3: "La nappe"}


def t2_pommier(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Nino cache les pommes dans les manches, trop vite.",
        2: "Nino charge les deux pommes dans le panier, trop vite.",
        3: "Nino serre les deux pommes dans la nappe, trop vite.",
    }[a]
    mishap = {
        1: "Les manches s'ouvrent, et la mince glisse.",
        2: "L'anse penche, et la mince bascule.",
        3: "Un coin se défait, et la mince glisse.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-m", "Je les prends tout seul !"),
        ("narrateur", "Sous le pommier, l'herbe pique les chevilles."),
        ("narrateur", mishap),
        ("enfant-m", "Elle part !"),
        ("narrateur", "Une goutte tape le bleu, puis une autre."),
        ("narrateur", "Le grain de pépin bascule vers l'herbe."),
        ("enfant-m", "On court, Sarah !"),
        ("narrateur", "Sarah ne bouge pas."),
        ("narrateur", "Le sourire de Nino n'est plus là."),
        ("narrateur", "Ça serre, juste sous la gorge."),
        ("papa", "Je m'accroupis, à votre hauteur."),
        ("maman", "Vous faites comment, tous les deux ?"),
    )


def t2_cabane(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Nino pousse le pull dans l'ouverture, trop vite.",
        2: "Nino pousse le panier dans l'ouverture, trop vite.",
        3: "Nino pousse la nappe dans l'ouverture, trop vite.",
    }[a]
    mishap = {
        1: "Une manche accroche la planche, et bloque.",
        2: "L'anse accroche la planche, et bloque.",
        3: "Un coin de nappe accroche la planche, et bloque.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-m", "On goûte ici, Sarah !"),
        ("narrateur", "La cabane sent le bois sec, un peu sombre."),
        ("narrateur", mishap),
        ("enfant-m", "Je ne passe pas."),
        ("narrateur", "Le grain de pépin se prend à une pointe de bois."),
        ("enfant-m", "Pousse, Sarah !"),
        ("narrateur", "Sarah reste dehors, sans un mot."),
        ("narrateur", "Le sourire de Nino disparaît."),
        ("narrateur", "L'envie et la peur se poussent, dans sa poitrine."),
        ("papa", "Je m'accroupis, au seuil."),
        ("maman", "Vous passez comment, tous les deux ?"),
    )


def t2_banc(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Nino pose le pull sur le banc, trop vite.",
        2: "Nino pose le panier sur le banc, trop vite.",
        3: "Nino pose la nappe sur le banc, trop vite.",
    }[a]
    mishap = {
        1: "Une manche balaie la mince, qui roule.",
        2: "L'anse penche, et la mince roule.",
        3: "Un coin glisse, et la mince roule.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-m", "La nappe, ici, Sarah."),
        ("narrateur", "Le banc de bois luit, mouillé."),
        ("narrateur", mishap),
        ("enfant-m", "Elle part dans l'herbe !"),
        ("narrateur", "Le grain de pépin frotte le bois, et penche."),
        ("enfant-m", "Attrape-la !"),
        ("narrateur", "Sarah ne court pas."),
        ("narrateur", "Le sourire de Nino n'est plus là."),
        ("narrateur", "Ça serre, juste sous la gorge."),
        ("maman", "Je m'accroupis, près du banc."),
        ("papa", "Vous la reprenez comment ?"),
    )


T2_FN = {1: t2_pommier, 2: t2_cabane, 3: t2_banc}
T2_SONS = {1: "feuille,goutte", 2: "bois,planche", 3: "bois,pomme"}
T2_EMPH = {1: "pommier", 2: "cabane", 3: "banc"}


def t3_choice(t2: int) -> list[tuple[str, str]]:
    if t2 == 1:
        return L(
            ("narrateur", "Les deux pommes glissent, sous l'arbre."),
            ("narrateur", "Nino pose un pied, sans courir."),
            ("papa", "Les deux pommes, attendre, ou essuyer ?"),
        )
    if t2 == 2:
        return L(
            ("narrateur", "La porte de planches reste trop étroite."),
            ("narrateur", "Nino pose une main, sans pousser."),
            ("maman", "Les manches, la couverture, ou la cape ?"),
        )
    return L(
        ("narrateur", "La mince a roulé, sous le banc."),
        ("narrateur", "Nino pose un genou, sans foncer."),
        ("papa", "Couper, caler, ou partager ?"),
    )


def t3(a: int, b: int, c: int) -> list[tuple[str, str]]:
    o = OBJ[a]
    cap = CAP[a]
    table = {
        (1, 1): L(
            ("enfant-m", "On n'y court pas."),
            ("enfant-f", "Une pour toi, une pour moi."),
            ("narrateur", "Sarah prend la ronde, toute jaune."),
            ("narrateur", "Nino prend la mince, à joue verte."),
            ("narrateur", f"{cap} voyage entre eux, sans se presser."),
            ("narrateur", "Nino écoute l'arbre, puis le bois."),
            ("narrateur", "Le grain de pépin brille, au poignet."),
            ("enfant-m", "Je le reconnais."),
            ("papa", "Vous les portez, tous les deux."),
            ("enfant-f", "La mienne est froide."),
            ("maman", "La goutte n'a pas eu le bleu."),
            ("narrateur", "Ils marchent vers la cabane, côte à côte."),
        ),
        (1, 2): L(
            ("enfant-m", "On attend la goutte."),
            ("enfant-f", "Moi aussi, j'attends."),
            ("narrateur", "Une goutte tape la feuille, puis plus rien."),
            ("narrateur", "Ils lèvent les deux pommes, ensemble."),
            ("narrateur", f"{cap} reste au sec, contre Nino."),
            ("narrateur", "Nino refuse de foncer sous l'arbre."),
            ("narrateur", "Le grain de pépin penche, puis tient."),
            ("enfant-m", "Il est là, Sarah."),
            ("papa", "Vous avez regardé, avant de bouger."),
            ("enfant-f", "Mes mains sont prêtes."),
            ("maman", "Le bleu n'a pas bu l'eau."),
            ("narrateur", "Le chemin vers la cabane s'ouvre, étroit."),
        ),
        (1, 3): L(
            ("enfant-m", "On essuie, d'abord."),
            ("enfant-f", "Avec le bleu."),
            ("narrateur", "Ils frottent la ronde, puis la mince."),
            ("narrateur", "Un peu d'herbe tombe, et l'eau aussi."),
            ("narrateur", f"{cap} sert de linge, un moment."),
            ("narrateur", "Nino ne ramasse pas trop vite."),
            ("narrateur", "Le grain de pépin réapparaît, au poignet."),
            ("enfant-m", "C'est lui, je le vois."),
            ("enfant-f", "Elles sont propres, maintenant."),
            ("papa", "Vous les avez essuyées, tous les deux."),
            ("maman", "Vos paumes sentent le fruit."),
            ("narrateur", "Ils portent les pommes vers les planches."),
        ),
        (2, 1): L(
            ("enfant-m", "On roule les manches."),
            ("enfant-f", "Moi celle-là, toi l'autre."),
            ("narrateur", "Sarah roule une manche, lentement."),
            ("narrateur", "Nino roule l'autre, sans tirer."),
            ("narrateur", f"{cap} passe le seuil, sans accrocher."),
            ("narrateur", "Nino refuse de forcer la planche."),
            ("narrateur", "Le grain de pépin tient, sur l'ourlet."),
            ("enfant-f", "Tes mains sont là."),
            ("enfant-m", "Les pommes aussi."),
            ("papa", "La porte vous a laissés."),
            ("maman", "Vous avez reculé le bleu, ensemble."),
            ("narrateur", "L'intérieur sent le bois sec, et le fruit."),
        ),
        (2, 2): L(
            ("enfant-f", "La couverture, comme un plateau."),
            ("enfant-m", "On la tient, tous les deux."),
            ("narrateur", "Ils posent les deux pommes au milieu."),
            ("narrateur", "Quatre mains portent le tissu, sans se presser."),
            ("narrateur", f"{cap} voyage à côté, contre la hanche."),
            ("narrateur", "Nino n'essaie plus de pousser seul."),
            ("narrateur", "Le grain de pépin glisse au bord, et reste."),
            ("enfant-m", "Je le vois, Sarah."),
            ("papa", "Le plateau est passé, sans se plier."),
            ("enfant-f", "Elles n'ont pas bougé."),
            ("maman", "La porte était trop étroite, pour un seul."),
            ("narrateur", "Le bois de la cabane les accueille, tiède."),
        ),
        (2, 3): L(
            ("enfant-m", "Le pull, en cape."),
            ("enfant-f", "Moi, je porte les pommes."),
            ("narrateur", "Nino ouvre la planche, sans la brusquer."),
            ("narrateur", "Sarah glisse, les deux fruits contre elle."),
            ("narrateur", f"{cap} reste près du seuil, un instant."),
            ("narrateur", "Personne ne pousse, ici."),
            ("narrateur", "Le grain de pépin brille au bord de la cape."),
            ("enfant-m", "Tu es passée."),
            ("enfant-f", "Toi aussi, maintenant."),
            ("papa", "La cape a gardé le bleu au sec."),
            ("maman", "Vous avez changé de rôle, ensemble."),
            ("narrateur", "La cabane se ferme, sans les pincer."),
        ),
        (3, 1): L(
            ("enfant-m", "Papa, tu coupes un tout petit bout ?"),
            ("papa", "Un tout petit, pour qu'elle tienne."),
            ("narrateur", "La mince pose un côté plat, sur le bois."),
            ("narrateur", "Sarah tient la ronde, Nino tient la mince."),
            ("narrateur", f"{cap} borde le banc, comme un nid."),
            ("narrateur", "Nino ne court plus après le fruit."),
            ("narrateur", "Le grain de pépin tient, près du jus."),
            ("enfant-f", "Elle ne roule plus."),
            ("enfant-m", "On l'a, Sarah."),
            ("maman", "Le banc vous les garde, maintenant."),
            ("papa", "Un petit bout a suffi."),
            ("narrateur", "Une feuille jaune s'arrête au pied du banc."),
        ),
        (3, 2): L(
            ("enfant-f", "On cale, avec la nappe."),
            ("enfant-m", "Quatre mains, pas une."),
            ("narrateur", "Ils glissent un pli sous la mince."),
            ("narrateur", "La ronde s'appuie contre, tout près."),
            ("narrateur", f"{cap} pèse un peu, et tient le pli."),
            ("narrateur", "Nino refuse de rattraper en courant."),
            ("narrateur", "Le grain de pépin réapparaît, dans le pli."),
            ("enfant-m", "C'est lui, au creux."),
            ("papa", "Vos mains allaient assez loin."),
            ("enfant-f", "Elle reste."),
            ("maman", "Le banc n'est plus trop lisse."),
            ("narrateur", "Les deux pommes se touchent, enfin calées."),
        ),
        (3, 3): L(
            ("enfant-m", "On partage, une chacun."),
            ("enfant-f", "Moi la ronde, toi la mince."),
            ("narrateur", "Ils s'assoient sur le banc, côte à côte."),
            ("narrateur", "Chaque pomme a sa paume, et reste."),
            ("narrateur", f"{cap} repose entre eux, sur le bois."),
            ("narrateur", "Nino n'essaie plus de tout porter."),
            ("narrateur", "Le grain de pépin veille, entre les deux."),
            ("enfant-f", "La mienne sent fort."),
            ("enfant-m", "La tienne aussi."),
            ("papa", "Vous les avez, chacun la sienne."),
            ("maman", "Le banc vous a laissés vous asseoir."),
            ("narrateur", "Une goutte tombe plus loin, sans eux."),
        ),
    }
    return table[(b, c)]


def fin(a: int, b: int, c: int) -> list[tuple[str, str]]:
    cap = CAP[a]
    last = {
        (1, 1, 1): "Le pull sèche, le grain de pépin au poignet.",
        (1, 1, 2): "Une manche du pull garde le grain de pépin.",
        (1, 1, 3): "Le pull borde les deux pommes, grain de pépin au poignet.",
        (1, 2, 1): "Le pull sent le bois, le grain de pépin à l'ourlet.",
        (1, 2, 2): "Le grain de pépin tient sur la couverture, sous le pull.",
        (1, 2, 3): "Le grain de pépin brille au bord de la cape bleue.",
        (1, 3, 1): "Le pull garde un trait de jus, près du grain de pépin.",
        (1, 3, 2): "Le grain de pépin sèche sur le pull, au banc.",
        (1, 3, 3): "Le pull et le grain de pépin veillent entre les pommes.",
        (2, 1, 1): "L'anse du panier garde le grain de pépin.",
        (2, 1, 2): "Le panier sèche, le grain de pépin collé à l'osier.",
        (2, 1, 3): "Un brin d'osier tient le grain de pépin, au fond.",
        (2, 2, 1): "Le panier pose le grain de pépin contre la planche.",
        (2, 2, 2): "Le grain de pépin roule au fond du panier.",
        (2, 2, 3): "Le panier ombre le grain de pépin, près de la cape.",
        (2, 3, 1): "Le panier laisse le grain de pépin près du jus.",
        (2, 3, 2): "Le grain de pépin sèche dans l'osier, au banc.",
        (2, 3, 3): "Le panier et le grain de pépin veillent entre les pommes.",
        (3, 1, 1): "La nappe sèche, le grain de pépin au coin.",
        (3, 1, 2): "Un carré de nappe garde le grain de pépin.",
        (3, 1, 3): "La nappe borde les deux pommes, grain de pépin au pli.",
        (3, 2, 1): "La nappe sent le bois, le grain de pépin au coin.",
        (3, 2, 2): "Le grain de pépin tient sur la nappe, sous la couverture.",
        (3, 2, 3): "Le grain de pépin brille au bord de la nappe.",
        (3, 3, 1): "La nappe garde un trait de jus, près du grain de pépin.",
        (3, 3, 2): "Le grain de pépin sèche sur la nappe, au banc.",
        (3, 3, 3): "La nappe et le grain de pépin veillent entre les pommes.",
    }[(a, b, c)]
    cores = {
        (1, 1): L(
            ("narrateur", "Dans la cabane, ils posent les deux pommes."),
            ("enfant-f", "La ronde, et la mince."),
            ("enfant-m", "On les a portées, tous les deux."),
            ("papa", "Vous les avez, enfin."),
            ("maman", "Le bleu n'a pas bu la goutte."),
            ("narrateur", "Le grain de pépin tient, au poignet du pull."),
            ("enfant-m", "Tu l'as vu, Sarah."),
            ("enfant-f", "Oui."),
            ("narrateur", "Ça a failli glisser, sous l'arbre."),
        ),
        (1, 2): L(
            ("narrateur", "Ils rentrent sous les planches, les pommes au sec."),
            ("enfant-m", "On a attendu la goutte."),
            ("enfant-f", "Elle est partie, plus loin."),
            ("papa", "Vous avez regardé, avant de lever."),
            ("maman", "Croquez, maintenant, au chaud."),
            ("narrateur", f"{cap} reste près du grain de pépin."),
            ("enfant-f", "La mienne craque."),
            ("enfant-m", "La tienne aussi."),
            ("narrateur", "Ça a failli mouiller le bleu."),
        ),
        (1, 3): L(
            ("narrateur", "Les pommes essuyées brillent, dans la cabane."),
            ("enfant-f", "Elles sentent le fruit, pas l'herbe."),
            ("enfant-m", "On les a frottées, ensemble."),
            ("maman", "Vos paumes sont un peu humides."),
            ("papa", "Le goûter est là, sur le bois."),
            ("narrateur", "Le grain de pépin veille, au poignet."),
            ("enfant-m", "On a failli les porter trop sales."),
            ("enfant-f", "Là, je les prends."),
            ("narrateur", "Dehors, une feuille colle au chemin."),
        ),
        (2, 1): L(
            ("narrateur", "Les manches roulées, ils croquent sous les planches."),
            ("enfant-m", "Tes mains m'ont aidé, Sarah."),
            ("enfant-f", "Les miennes aussi, un peu."),
            ("papa", "La porte vous a laissés, tous les deux."),
            ("maman", "Le bois sent le sec, ici."),
            ("narrateur", "Le grain de pépin tient, sur l'ourlet."),
            ("enfant-m", "On a failli rester dehors."),
            ("enfant-f", "Là, on est."),
            ("narrateur", "Une goutte tape le toit, sans entrer."),
        ),
        (2, 2): L(
            ("narrateur", "La couverture repose, les pommes au milieu."),
            ("enfant-f", "On l'a portée, comme un plateau."),
            ("enfant-m", "Quatre mains, pas deux."),
            ("maman", "La porte était trop étroite, pour un seul."),
            ("papa", "Croquez, le fruit est à vous."),
            ("narrateur", f"{cap} garde une trace du seuil."),
            ("enfant-f", "Je la tiens, Nino."),
            ("narrateur", "Le grain de pépin reste au bord, brun."),
            ("narrateur", "Ça a failli coincer, à la planche."),
        ),
        (2, 3): L(
            ("narrateur", "La cape bleue sèche, contre la paroi."),
            ("enfant-m", "Tu as porté les pommes."),
            ("enfant-f", "Tu as tenu la planche."),
            ("papa", "Vous avez changé de rôle, sans vous presser."),
            ("maman", "Le bleu n'a pas accroché."),
            ("narrateur", "Le grain de pépin brille au bord de la cape."),
            ("enfant-m", "On a failli pousser trop fort."),
            ("enfant-f", "Là, on croque."),
            ("narrateur", "Le toit compte les gouttes, dehors."),
        ),
        (3, 1): L(
            ("narrateur", "Ils rentrent, la mince au côté plat."),
            ("enfant-f", "Elle ne roule plus."),
            ("enfant-m", "Papa a coupé un tout petit bout."),
            ("maman", "Le banc vous l'a gardée."),
            ("papa", "Le goûter voyage jusqu'aux planches."),
            ("narrateur", "Sarah pose la ronde contre le bois."),
            ("narrateur", "Le grain de pépin tient, près du jus."),
            ("enfant-m", "On a failli la perdre dans l'herbe."),
            ("enfant-f", "Là, je la vois."),
        ),
        (3, 2): L(
            ("narrateur", "Le pli de nappe voyage jusqu'à la cabane."),
            ("enfant-m", "On a calé, tous les deux."),
            ("enfant-f", "Elle n'est plus partie."),
            ("papa", "Vos mains allaient assez loin."),
            ("maman", "Posez-les, sur le bois sec."),
            ("narrateur", f"{cap} pose une ombre ronde, au plancher."),
            ("enfant-f", "La mince est là, Nino."),
            ("enfant-m", "C'est pour ça."),
            ("narrateur", "Le grain de pépin sèche dans le pli."),
        ),
        (3, 3): L(
            ("narrateur", "Chacun sa pomme, sous les planches."),
            ("enfant-m", "On a partagé, au banc."),
            ("enfant-f", "Une pour toi, une pour moi."),
            ("papa", "Vous les aviez, chacun la sienne."),
            ("maman", "Le banc vous a laissés vous asseoir."),
            ("narrateur", "Sarah croque la ronde, Nino croque la mince."),
            ("enfant-m", "On a failli tout porter, tout seul."),
            ("narrateur", "Le grain de pépin s'endort, entre eux."),
            ("narrateur", "Dehors, le pommier se tait."),
        ),
    }
    rows = list(cores[(b, c)])
    rows.append(("narrateur", last))
    return rows


T3_EMPH = {
    1: {1: "deux pommes", 2: "goutte", 3: "essuyer"},
    2: {1: "manches", 2: "couverture", 3: "cape"},
    3: {1: "couper", 2: "caler", 3: "partager"},
}
T3_SONS = {
    1: {1: "pomme,pas", 2: "goutte,feuille", 3: "tissu,pomme"},
    2: {1: "tissu,bois", 2: "couverture,pas", 3: "tissu,planche"},
    3: {1: "couteau,bois", 2: "tissu,banc", 3: "bois,pomme"},
}
FIN_SONS = {1: "cabane,silence", 2: "bois,goutte", 3: "pomme,silence"}


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "feuille,goutte", "emphasis": "grain de pépin"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Trois choses attendent près de l'herbe."),
            ("narrateur", "Le pull bleu, le panier, et la nappe."),
            ("narrateur", "Nino serre une pomme, puis la pose."),
            ("maman", "Tu prends quoi d'abord, Nino ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "le pull bleu",
            "option_2_label": "le panier",
            "option_3_label": "la nappe",
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
                    extra={"sons": T3_SONS[b][c], "emphasis": "grain de pépin"},
                )
                fin_id = f"{leaf}_F0001"
                by[fin_id] = voice(
                    by_old[fin_id], fin(a, b, c), "ending",
                    extra={"sons": FIN_SONS[b], "emphasis": "grain de pépin"},
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
    if "nino" not in blob or "sarah" not in blob:
        raise SystemExit("Nino/Sarah absents")
    if "grain de pépin" not in blob and "grain de pepin" not in blob:
        raise SystemExit("indice grain de pépin absent")
    if "cabane" not in blob or "pommier" not in blob:
        raise SystemExit("cabane/pommier absents")
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
        "grain de pomme",
        "cerf-volant",
        "chouchou",
        "marque fine",
        "ombre-flèche",
        "ombre-fleche",
        "tache de couleur",
        "drap de salon",
        "drap salon",
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
        if "grain de pépin" not in c["text"].lower() and "grain de pepin" not in c["text"].lower():
            raise SystemExit(f"{c['chunk_id']}: fin sans grain de pépin")

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
    if pmin < 500:
        raise SystemExit(f"chemin trop court: {pmin}")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés. Graphe `option_*_next` conservé.\n\n"
        "## Vécu\n"
        "Jardin d'automne derrière la maison. Coin nommé : la cabane de planches, "
        "sous le pommier. L'odeur d'une pomme écrasée monte du chemin. Sur le "
        "poignet du pull bleu, un grain de pépin tient, brun. Mission : porter "
        "les deux pommes jusqu'à la cabane, avant la pluie, pour le goûter. "
        "Sarah arrive et s'arrête, sans un mot. Nino propose de courir ; son "
        "silence compte. Papa remercie Nino d'avoir vu ce silence. "
        "T1 = pull bleu / panier / nappe (les trois partent ; trop vite : manche "
        "avalée, toc, nappe trop serrée). T2 = pommier (les deux glissent) / "
        "cabane (la porte pince) / banc (la mince roule). Le grain faillit "
        "tomber. Nino veut foncer ; Sarah pose sa limite. Sourire parti, "
        "gorge serrée, adulte accroupi. T3 : ils refusent de foncer, retrouvent "
        "le grain du début, font à deux. 27 fins : les pommes sont là, l'objet "
        "porte une trace, ça a failli ne pas arriver. Leçon DIF.COR.002 vécue "
        "(à deux, pas tout seul), jamais dite. "
        "Monde ≠ TREE-DIF-024 (Chouchou, cerf-volant, grain de pomme), "
        "≠ TREE-DIF-015 (drap salon).\n\n"
        "## Vu et corrigé\n"
        f"`python3 stories/rewrites/_write_tree_dif_002.py` → `OK {SID} {nwords} mots`. "
        "N2 ≤ 15. `_lib.check` vert.\n"
        f"- 86 chunks, 27 chemins, 27 fins distinctes, {pmin} à {pmax} mots "
        f"(moyenne {pavg}).\n"
        "- Ouverture inventée (odeur d'une pomme écrasée, pas le gabarit jardin).\n"
        "- Indice unique : grain de pépin, payé au climax et en coda.\n"
        "- Pair D16 : Sarah. Rythmes distincts. Silence = réponse.\n"
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
    print(f"chemins {pmin}-{pmax} moy {pavg}")


if __name__ == "__main__":
    main()
