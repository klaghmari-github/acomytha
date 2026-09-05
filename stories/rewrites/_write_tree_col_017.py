#!/usr/bin/env python3
"""TREE-COL-017 — L'escargot de la boulangerie (F-NAR-019)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-COL-017"
LIM = 16
TICS = (
    "tout doux",
    "tout calme",
    "on lève la main",
    "puis on parle",
    "c'est du bon travail",
    "on va apprendre",
    "si malaise",
    "l'histoire est finie",
    "aujourd'hui,",
    "j'ai compris",
    "mission accomplie",
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
        note="arc=installation; intention=émerveiller; emotion=curiosité_impatiente; intensite=1; destinataire=enfant; sous_texte=la_virgule_de_farine_attend; tempo=naturel; sourire=léger; respiration=ample",
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
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_la_virgule; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=joie_discrete; intensite=1; destinataire=enfant; sous_texte=on_t_a_entendu; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=trop_vite_l_escargot_se_cache; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=inquietude_legere; intensite=2; destinataire=enfant; sous_texte=il_veut_rentrer_chez_lui; tempo=resserre; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=resolution; intention=faire_vivre_la_reussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=la_virgule_pointait_le_volet; tempo=naturel; sourire=franc; respiration=relachee",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierte_calme; intensite=1; destinataire=enfant; sous_texte=le_sachet_porte_la_trace; tempo=pose; sourire=léger; respiration=ample",
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


# --- récit ---
OPENING = L(
    ("narrateur", "Au coin de la rue, une odeur de pain marche devant eux."),
    ("narrateur", "La boutique reste cachée, et le souffle est chaud."),
    ("narrateur", "Puis le volet blond apparaît, à moitié levé."),
    ("narrateur", "Les clés de papa répondent au claquement du bois."),
    ("narrateur", "Sur le bois, une virgule de farine brille."),
    ("narrateur", "Elle a la forme d'une toute petite lune."),
    ("papa", "Le petit pain est tiède, Amir."),
    ("narrateur", "Le sachet kraft froisse dans la main de papa."),
    ("narrateur", "En ce moment, un escargot grimpe le bois blond."),
    ("narrateur", "La même virgule de farine orne sa coquille."),
    ("enfant-m", "Papa, il veut venir à l'école avec nous !"),
    ("narrateur", "Papa parle de la poire à maman."),
    ("narrateur", "Leurs mots couvrent le cri d'Amir."),
    ("narrateur", "Amir tend le sachet vers la coquille."),
    ("narrateur", "L'escargot rentre toute sa tête, d'un coup."),
    ("enfant-m", "Il s'est caché !"),
    ("narrateur", "Amir referme la bouche, les joues chaudes."),
    ("narrateur", "Il attend que maman finisse sa phrase."),
    ("maman", "Tu voulais nous dire quelque chose ?"),
    ("enfant-m", "L'escargot a une virgule de farine, comme le volet."),
    ("papa", "Alors on le suit, sans le prendre."),
    ("narrateur", "L'escargot ressort, et glisse vers le petit parc."),
    ("narrateur", "Le parc du volet blond s'ouvre, juste avant l'école."),
    ("maman", "La poire attend dans le sac, pour plus tard."),
)

T1 = {
    1: dict(
        name="le bac à sable",
        passage=L(
            ("narrateur", "Amir s'agenouille au bord du bac à sable."),
            ("narrateur", "Le sable est frais, gris, et sent la terre."),
            ("narrateur", "Un râteau de bois repose près du bord."),
            ("narrateur", "Le sachet kraft reste contre sa hanche, tiède."),
            ("enfant-m", "Je le pousse avec le râteau, vite !"),
            ("narrateur", "Le bois soulève un nuage de grains."),
            ("narrateur", "L'escargot disparaît sous le sable."),
            ("enfant-m", "Il est parti !"),
            ("narrateur", "Papa parle du petit pain à maman."),
            ("narrateur", "Leurs voix recouvrent le mot parti."),
            ("narrateur", "Amir pose le râteau, les épaules basses."),
            ("narrateur", "Il attend que la phrase de papa se termine."),
            ("maman", "C'est à toi, on t'écoute."),
            ("enfant-m", "La virgule de farine est sur sa coquille."),
            ("papa", "Je la vois, collée comme sur le volet."),
            ("narrateur", "Les grains retombent, et l'escargot reprend sa route."),
        ),
        question="Quelle trace blanche orne la coquille de l'escargot ?",
        expected="farine",
        accepted="farine | virgule | virgule de farine | de la farine | une virgule de farine",
        retry="Regarde ce qui brille sur la coquille.",
        ok="Oui, c'est de la farine.",
        confirm=L(
            ("enfant-m", "De la farine, une virgule !"),
            ("narrateur", "Oui, une virgule de farine."),
            ("maman", "Merci, j'ai entendu toute ta phrase."),
            ("narrateur", "Le sachet kraft froisse, et l'escargot contourne le râteau."),
        ),
        sons="sable,pain",
        choice=L(
            ("narrateur", "Près du bac, trois objets du sac peuvent aider, ou gêner."),
            ("papa", "Le ballon, le seau, ou le doudou ?"),
        ),
    ),
    2: dict(
        name="le toboggan",
        passage=L(
            ("narrateur", "Amir pose une main sur le toboggan."),
            ("narrateur", "Le métal est froid, et un peu mouillé."),
            ("narrateur", "Une feuille jaune tremble tout en haut."),
            ("narrateur", "L'escargot grimpe la pente, très lent."),
            ("narrateur", "Le sachet kraft bat contre sa jambe."),
            ("enfant-m", "Je souffle, il va glisser jusqu'à moi !"),
            ("narrateur", "Son souffle trop fort fait rentrer la tête."),
            ("narrateur", "Maman décrit le petit pain à papa."),
            ("narrateur", "Amir ouvre la bouche, puis la referme."),
            ("papa", "Tu disais, Amir ?"),
            ("enfant-m", "Il grimpe le toboggan, avec sa virgule de farine."),
            ("maman", "On le regarde, sans le faire glisser."),
            ("narrateur", "L'escargot ressort, et reprend le métal froid."),
        ),
        question="Sur quoi l'escargot grimpe-t-il ?",
        expected="toboggan",
        accepted="toboggan | le toboggan | métal | le métal | la pente",
        retry="Regarde la pente froide sous ses pattes.",
        ok="Oui, sur le toboggan.",
        confirm=L(
            ("enfant-m", "Sur le toboggan !"),
            ("narrateur", "Oui, sur le métal froid."),
            ("papa", "Merci d'avoir gardé ton souffle."),
            ("narrateur", "La feuille jaune tremble, et le sachet reste tiède."),
        ),
        sons="metal,pain",
        choice=L(
            ("narrateur", "Au pied du toboggan, trois objets du sac attendent."),
            ("maman", "Le ballon, le seau, ou le doudou ?"),
        ),
    ),
    3: dict(
        name="les balançoires",
        passage=L(
            ("narrateur", "Les chaînes des balançoires font un petit clic."),
            ("narrateur", "Le siège est lisse, un peu froid."),
            ("narrateur", "L'escargot s'accroche à une chaîne, au bas."),
            ("narrateur", "Le sachet kraft repose sur le banc, près des pieds."),
            ("enfant-m", "Je pousse, il va danser !"),
            ("narrateur", "La chaîne bouge, et l'escargot se plaque."),
            ("narrateur", "Amir lâche, le cœur serré."),
            ("narrateur", "Papa compte les minutes avant l'école, à maman."),
            ("narrateur", "Amir attend la fin du compte."),
            ("maman", "Nous t'écoutons, maintenant."),
            ("enfant-m", "Il s'est accroché à la chaîne, avec sa virgule."),
            ("papa", "Je vois la virgule, elle ne bouge pas."),
            ("narrateur", "Une flaque tremble sous le siège vide."),
        ),
        question="Où l'escargot s'est-il accroché ?",
        expected="chaîne",
        accepted="chaîne | la chaîne | chaines | les chaînes | chaine | la chaine",
        retry="Écoute le petit clic, tout en bas.",
        ok="Oui, à la chaîne.",
        confirm=L(
            ("enfant-m", "À la chaîne !"),
            ("narrateur", "Oui, tout en bas de la chaîne."),
            ("maman", "Merci, tu as parlé sans pousser."),
            ("narrateur", "La flaque tremble, et le sachet attend sur le banc."),
        ),
        sons="chaine,pain",
        choice=L(
            ("narrateur", "Près des chaînes, trois objets du sac peuvent changer la suite."),
            ("papa", "Le ballon, le seau, ou le doudou ?"),
        ),
    ),
}


def t2_ballon(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Amir pose le ballon comme un mur, dans le sable."),
            ("narrateur", "Le caoutchouc est un peu sablé, et sent chaud."),
            ("enfant-m", "Comme ça, il reste avec nous !"),
            ("narrateur", "Le ballon roule, et ouvre un passage vers la rue."),
            ("narrateur", "L'escargot tourne vers la boulangerie, pas vers l'école."),
            ("narrateur", "Le sourire d'Amir disparaît."),
            ("enfant-m", "Il ne veut pas venir ?"),
            ("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
            ("papa", "On s'accroupit, à sa hauteur."),
            ("narrateur", "Amir refuse de courir après le ballon."),
            ("narrateur", "Il regarde la virgule de farine, sur la coquille."),
            ("enfant-m", "Elle pointe vers le volet, pas vers le sac."),
        )
    if a == 2:
        return L(
            ("narrateur", "Amir pose le ballon au bas du toboggan."),
            ("narrateur", "Le ballon fait poum contre le métal froid."),
            ("enfant-m", "Il tombera dans un nid moelleux !"),
            ("narrateur", "Le ballon rebondit de travers, trop près de la tête."),
            ("narrateur", "L'escargot recule, puis redescend vers la boutique."),
            ("narrateur", "Les épaules d'Amir tombent."),
            ("enfant-m", "Il fuit mon nid."),
            ("maman", "Peut-être qu'il n'a pas demandé de nid."),
            ("narrateur", "Amir attrape le ballon, sans foncer."),
            ("narrateur", "La virgule de farine vise le volet blond."),
            ("enfant-m", "Il veut rentrer, pas glisser."),
        )
    return L(
        ("narrateur", "Amir glisse le ballon sous la balançoire."),
        ("narrateur", "Le siège cliquette au-dessus du caoutchouc."),
        ("enfant-m", "S'il tombe, le ballon l'attrape !"),
        ("narrateur", "Un coup de vent pousse le siège."),
        ("narrateur", "Le ballon part vers la rue, trop vite."),
        ("narrateur", "L'escargot quitte la chaîne, du côté du four."),
        ("enfant-m", "Pas la rue, le pain !"),
        ("narrateur", "Amir serre le kraft, et il n'envoie pas le pied."),
        ("papa", "Tu as vu sa direction, toi."),
        ("narrateur", "La virgule blanche vise le claquement du volet."),
        ("enfant-m", "Il rentre à la boulangerie."),
    )


def t2_seau(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Amir penche le seau rouge au-dessus du sable."),
            ("narrateur", "Un peu d'eau tremble au fond, tiède."),
            ("enfant-m", "Je lui fais une rivière, pour nous suivre !"),
            ("narrateur", "L'eau creuse un filet vers la gouttière de la rue."),
            ("narrateur", "L'escargot s'arrête au bord, antennes levées."),
            ("narrateur", "Le sourire d'Amir se plie."),
            ("enfant-m", "Ma rivière l'emporte trop loin."),
            ("papa", "On pose le seau, on regarde."),
            ("narrateur", "Amir recule le plastique, sans verser le reste."),
            ("narrateur", "La virgule de farine reste tournée vers le volet."),
            ("enfant-m", "Il n'a pas soif de gouttière."),
        )
    if a == 2:
        return L(
            ("narrateur", "Amir verse une goutte sur le toboggan."),
            ("narrateur", "Le métal devient une glissade trop vive."),
            ("enfant-m", "Il arrivera plus vite !"),
            ("narrateur", "L'escargot glisse d'un cran, trop brusque."),
            ("narrateur", "Il se plaque, puis rebrousse vers le haut."),
            ("narrateur", "Du haut, on voit le volet blond."),
            ("enfant-m", "Il monte pour rentrer ?"),
            ("narrateur", "Maman s'accroupit au pied de la pente."),
            ("narrateur", "Amir tient le seau immobile, collé au kraft."),
            ("narrateur", "La virgule de farine vise la boutique, au-dessus."),
            ("enfant-m", "Plus d'eau : il choisit le bois."),
        )
    return L(
        ("narrateur", "Amir pose le seau sous la balançoire."),
        ("narrateur", "Une flaque s'étale, ronde, entre les pieds."),
        ("enfant-m", "Un miroir, pour qu'il nous voie !"),
        ("narrateur", "Le siège passe au-dessus, et l'eau tremble."),
        ("narrateur", "L'escargot descend de la chaîne, loin de la flaque."),
        ("narrateur", "Il prend le trottoir du four, pas le miroir."),
        ("enfant-m", "Mon eau l'a fait peur."),
        ("narrateur", "Amir pose le seau droit, sans en rajouter."),
        ("papa", "Sa virgule n'a pas bougé de côté."),
        ("narrateur", "Elle pointe le claquement du volet, derrière la haie."),
        ("enfant-m", "Chez lui, pas dans l'eau."),
    )


def t2_doudou(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Amir sort le doudou du sac, près du bac."),
            ("narrateur", "Une oreille est plus usée que l'autre."),
            ("enfant-m", "Une maison, pour l'emmener !"),
            ("narrateur", "L'oreille tombe sur la coquille, trop sombre."),
            ("narrateur", "L'escargot rentre, et le sable reste vide."),
            ("narrateur", "Un nœud lui prend la gorge."),
            ("enfant-m", "Je l'ai caché trop fort."),
            ("maman", "On soulève l'oreille, sans le prendre."),
            ("narrateur", "Amir lève le tissu, tout seul, sans foncer."),
            ("narrateur", "Une antenne reparaît, virgule tournée vers le volet."),
            ("enfant-m", "Il veut sa boutique, pas ma poche."),
        )
    if a == 2:
        return L(
            ("narrateur", "Amir pose le doudou au bas du toboggan."),
            ("narrateur", "Le tissu sent la maison, un peu chaud."),
            ("enfant-m", "Coussin, s'il glisse !"),
            ("narrateur", "L'escargot arrive sur le tissu, puis s'arrête."),
            ("narrateur", "Il rebrousse le métal, vers le ciel du volet."),
            ("narrateur", "Les doigts d'Amir serrent trop le kraft."),
            ("enfant-m", "Mon coussin n'est pas son lit."),
            ("papa", "On le laisse choisir le bois."),
            ("narrateur", "Amir recule le doudou, sans le tirer sous lui."),
            ("narrateur", "La virgule de farine vise le blond de la boutique."),
            ("enfant-m", "Il rentre, tout seul."),
        )
    return L(
        ("narrateur", "Amir installe le doudou sur le siège de la balançoire."),
        ("narrateur", "L'oreille balaie la chaîne, trop près."),
        ("enfant-m", "Il voyage avec nous, collé !"),
        ("narrateur", "La fourrure recouvre la coquille un instant."),
        ("narrateur", "L'escargot se plaque, puis fuit vers le banc."),
        ("narrateur", "Du banc, le volet blond se voit, entre les feuilles."),
        ("enfant-m", "Je l'ai trop serré."),
        ("narrateur", "Amir reprend le doudou, et le pose dans le sac."),
        ("maman", "Sa virgule n'a pas demandé le siège."),
        ("narrateur", "Elle pointe le four, pas l'école."),
        ("enfant-m", "Il rentre au pain, pas dans ma poche."),
    )


T2_FN = {1: t2_ballon, 2: t2_seau, 3: t2_doudou}
T2_SONS = {1: "ballon", 2: "seau,eau", 3: "tissu"}
T2_NAME = {1: "le ballon", 2: "le seau", 3: "le doudou"}
T3_NAME = {1: "le galet", 2: "la plume", 3: "l'escargot"}


def t3_choice(b: int) -> list[tuple[str, str]]:
    if b == 1:
        return L(
            ("narrateur", "Le ballon a ouvert le mauvais chemin."),
            ("papa", "Qui l'aide à rentrer : le galet, la plume, ou l'escargot ?"),
        )
    if b == 2:
        return L(
            ("narrateur", "L'eau a presque trop tiré."),
            ("maman", "Qui l'aide sans le forcer : le galet, la plume, ou l'escargot ?"),
        )
    return L(
        ("narrateur", "Le doudou a fait trop d'ombre."),
        ("papa", "Qui l'aide à choisir : le galet, la plume, ou l'escargot ?"),
    )


# 27 climaxes : autre geste, autre paiement de la virgule.
T3 = {
    (1, 1, 1): L(
        ("narrateur", "Amir ramasse un galet chaud, lisse, près du bac."),
        ("narrateur", "Le ballon reste de côté, loin de la rue."),
        ("enfant-m", "Un petit chemin, vers le volet."),
        ("narrateur", "Trois galets s'alignent dans le sable, vers la boutique."),
        ("narrateur", "L'escargot suit les creux, sans qu'on le pousse."),
        ("narrateur", "La virgule de farine vise le bois blond, pas le kraft."),
        ("maman", "Il a lu ta route, tout seul."),
        ("papa", "Merci d'avoir laissé le ballon dormir."),
        ("narrateur", "Au dernier galet, le mur de la boulangerie commence."),
    ),
    (1, 1, 2): L(
        ("narrateur", "Une plume grise tremble au bord du bac."),
        ("narrateur", "Le vent la pousse vers le volet, pas vers la rue."),
        ("enfant-m", "Elle montre sa maison."),
        ("narrateur", "Amir ne court pas après le ballon."),
        ("narrateur", "La plume se pose, puis reprend, vers le four."),
        ("narrateur", "L'escargot suit ce fil d'air, virgule en avant."),
        ("papa", "Le ballon a ouvert la rue, la plume a fermé le doute."),
        ("narrateur", "Sur le kraft, un duvet gris reste collé."),
    ),
    (1, 1, 3): L(
        ("narrateur", "Amir s'assoit, le ballon calé sous le genou."),
        ("enfant-m", "Toi, tu choisis."),
        ("narrateur", "Personne ne parle, un long moment."),
        ("narrateur", "L'escargot contourne le caoutchouc, vers le mur."),
        ("narrateur", "Sa virgule de farine pointe le claquement du volet."),
        ("maman", "Il n'avait pas demandé l'école."),
        ("narrateur", "Un fil humide part du sable vers la boutique."),
        ("papa", "Tu l'as regardé jusqu'au bout."),
    ),
    (1, 2, 1): L(
        ("narrateur", "Amir pose des galets en travers du filet d'eau."),
        ("narrateur", "Le seau reste droit, plus une goutte."),
        ("enfant-m", "Un pont, pas une rivière."),
        ("narrateur", "L'escargot gravit les pierres, antennes au volet."),
        ("narrateur", "La virgule de farine ne trempe pas."),
        ("maman", "Tu as barré la gouttière, pas sa route."),
        ("narrateur", "Derrière le bac, le bois blond se rapproche."),
        ("papa", "Le seau peut rentrer dans le sac."),
    ),
    (1, 2, 2): L(
        ("narrateur", "Une plume grise flotte sur l'eau du bac."),
        ("narrateur", "Elle dérive vers le volet, pas vers la rue."),
        ("enfant-m", "Suis-la, sans te presser."),
        ("narrateur", "Amir tient le seau loin, collé au kraft."),
        ("narrateur", "L'escargot borde le filet, virgule tournée au four."),
        ("papa", "Ta rivière a failli, la plume a dit le mur."),
        ("narrateur", "La plume s'échoue au pied du volet blond."),
        ("maman", "Il a choisi le pain, pas la gouttière."),
    ),
    (1, 2, 3): L(
        ("narrateur", "Amir pose le seau, et il ne verse plus."),
        ("enfant-m", "Je te regarde, c'est tout."),
        ("narrateur", "L'escargot contourne le rond humide, pas à pas."),
        ("narrateur", "Sa virgule de farine avance vers le mur, sèche."),
        ("narrateur", "Le filet d'eau s'arrête dans le sable, sans lui."),
        ("papa", "Il a évité ta rivière, tout seul."),
        ("narrateur", "Au bord du bac, le claquement du volet l'appelle."),
        ("maman", "Tu n'as rien ajouté, et ça a suffi."),
    ),
    (1, 3, 1): L(
        ("narrateur", "Amir glisse un galet sous l'oreille du doudou."),
        ("narrateur", "Le tissu se soulève, sans toucher la coquille."),
        ("enfant-m", "De l'air, et un chemin."),
        ("narrateur", "Trois galets partent du bac vers le volet."),
        ("narrateur", "L'escargot sort de l'ombre, virgule au bois blond."),
        ("maman", "Tu as levé la maison, pas l'animal."),
        ("narrateur", "Le doudou reprend sa place dans le sac."),
        ("papa", "Le galet garde un peu de sable, tout chaud."),
    ),
    (1, 3, 2): L(
        ("narrateur", "Une plume grise était restée dans la fourrure."),
        ("narrateur", "Amir la libère, et le vent la prend vers le volet."),
        ("enfant-m", "Sors, suis la plume."),
        ("narrateur", "L'oreille du doudou ne retombe pas."),
        ("narrateur", "L'escargot suit le duvet, virgule en avant."),
        ("papa", "Ta poche était trop sombre, le four est clair."),
        ("narrateur", "La plume se colle au kraft, tournée vers la boutique."),
        ("maman", "Il rentre, et le doudou reste à toi."),
    ),
    (1, 3, 3): L(
        ("narrateur", "Amir tient le doudou contre lui, loin du sable."),
        ("enfant-m", "Je te laisse l'ombre."),
        ("narrateur", "Une antenne paraît, puis l'autre."),
        ("narrateur", "L'escargot choisit le mur, virgule au claquement."),
        ("narrateur", "Personne ne pose une main."),
        ("maman", "Il a dit non à ta poche, tout seul."),
        ("narrateur", "Le bac garde un creux vide, du côté de la rue."),
        ("papa", "Toi, tu as attendu qu'il finisse."),
    ),
    (2, 1, 1): L(
        ("narrateur", "Au bas du toboggan, Amir aligne trois galets."),
        ("narrateur", "Le ballon reste sous le banc, loin de la pente."),
        ("enfant-m", "Un escalier, vers le four."),
        ("narrateur", "L'escargot quitte le métal, pierre après pierre."),
        ("narrateur", "La virgule de farine vise le volet, au-dessus de la haie."),
        ("papa", "Ton nid a rebondi, tes galets tiennent."),
        ("narrateur", "La feuille jaune tremble, et ne tombe pas sur lui."),
        ("maman", "Il descend pour rentrer, pas pour jouer."),
    ),
    (2, 1, 2): L(
        ("narrateur", "Une plume grise glisse le long du métal."),
        ("narrateur", "Le vent la pousse du côté du four, pas du ballon."),
        ("enfant-m", "Pas le poum, le blond."),
        ("narrateur", "Amir retient le ballon sous le genou."),
        ("narrateur", "L'escargot suit la plume, redescend, virgule au volet."),
        ("maman", "Le rebond a fait peur, le duvet a dit le mur."),
        ("narrateur", "La plume s'arrête au pied du toboggan, tournée boutique."),
        ("papa", "Tu n'as pas rattrapé le ballon trop tôt."),
    ),
    (2, 1, 3): L(
        ("narrateur", "Amir s'assoit au bas, le ballon calé."),
        ("enfant-m", "Toi d'abord, la pente ensuite."),
        ("narrateur", "L'escargot redescend le métal, sans le poum."),
        ("narrateur", "Sa virgule de farine pointe le volet, pas le sac."),
        ("narrateur", "Le ballon ne bouge plus."),
        ("papa", "Il n'a pas voulu ton nid."),
        ("narrateur", "Au bout de la pente, le trottoir du pain commence."),
        ("maman", "Tu l'as laissé finir sa descente."),
    ),
    (2, 2, 1): L(
        ("narrateur", "Amir cale des galets en travers de la pente mouillée."),
        ("narrateur", "Le seau reste fermé, contre le kraft."),
        ("enfant-m", "Plus de glissade, un pas après l'autre."),
        ("narrateur", "L'escargot gravit les pierres, hors du filet d'eau."),
        ("narrateur", "La virgule de farine reste sèche, tournée au volet."),
        ("maman", "Tu as cassé ta rivière, pas sa route."),
        ("narrateur", "Du haut, le bois blond se voit, tout proche."),
        ("papa", "Le métal peut sécher, lui rentre."),
    ),
    (2, 2, 2): L(
        ("narrateur", "Une plume grise colle au métal mouillé."),
        ("narrateur", "Elle indique le haut, où le volet se découpe."),
        ("enfant-m", "Monte, le four est là."),
        ("narrateur", "Amir tient le seau loin de la goutte."),
        ("narrateur", "L'escargot rebrousse, virgule au blond."),
        ("papa", "L'eau allait trop vite, la plume a ralenti le regard."),
        ("narrateur", "La feuille jaune s'envole, et lui reste sur le bois du haut."),
        ("maman", "Il a choisi le volet, pas la glissade."),
    ),
    (2, 2, 3): L(
        ("narrateur", "Amir pose le seau dans l'herbe, et il attend."),
        ("enfant-m", "Sans goutte, à toi."),
        ("narrateur", "L'escargot redescend, loin de l'eau, vers le four."),
        ("narrateur", "Sa virgule de farine ne tremble plus."),
        ("narrateur", "Le métal garde une trace humide, vide."),
        ("maman", "Ta goutte a failli, son choix a tenu."),
        ("narrateur", "Au pied du toboggan, le trottoir sent le pain."),
        ("papa", "Tu n'as rien versé de plus."),
    ),
    (2, 3, 1): L(
        ("narrateur", "Amir pose un galet sur le doudou, au bas."),
        ("narrateur", "Le tissu reste un coussin vide, plus une maison."),
        ("enfant-m", "Toi, les pierres, pas ma poche."),
        ("narrateur", "Trois galets mènent du métal au mur du four."),
        ("narrateur", "L'escargot les prend, virgule au volet."),
        ("papa", "Ton coussin peut dormir, lui rentre."),
        ("narrateur", "La fourrure sent le zinc, plus la coquille."),
        ("maman", "Tu as changé le nid en chemin."),
    ),
    (2, 3, 2): L(
        ("narrateur", "Une plume dépasse le doudou, au bas du toboggan."),
        ("narrateur", "Le vent la tire vers le blond du volet."),
        ("enfant-m", "Sors du tissu, suis ça."),
        ("narrateur", "Amir recule le doudou d'une main, sans tirer l'animal."),
        ("narrateur", "L'escargot suit le duvet, virgule en avant."),
        ("maman", "Le coussin était trop doux, le four est son dur."),
        ("narrateur", "La plume se colle à la feuille jaune, côté boutique."),
        ("papa", "Tu as ouvert l'ombre, pas ses pattes."),
    ),
    (2, 3, 3): L(
        ("narrateur", "Amir range le doudou, tout au fond du sac."),
        ("enfant-m", "La pente est à toi."),
        ("narrateur", "L'escargot quitte le métal, vers la rue de la boutique."),
        ("narrateur", "Sa virgule de farine pointe le claquement, pas l'école."),
        ("narrateur", "Personne ne pose le tissu sous lui."),
        ("papa", "Il n'a pas voulu ton lit."),
        ("narrateur", "Le toboggan reste vide, et le four l'appelle."),
        ("maman", "Tu l'as laissé finir sa phrase à lui."),
    ),
    (3, 1, 1): L(
        ("narrateur", "Amir cale des galets au bas de la chaîne."),
        ("narrateur", "Le ballon reste sous le banc, loin du siège."),
        ("enfant-m", "Un sentier, vers le claquement."),
        ("narrateur", "L'escargot quitte la chaîne, pierre après pierre."),
        ("narrateur", "La virgule de farine vise le volet, entre les feuilles."),
        ("maman", "Le ballon allait à la rue, tes galets vont au four."),
        ("narrateur", "La flaque tremble, et lui passe à côté."),
        ("papa", "Tu n'as pas poussé le siège."),
    ),
    (3, 1, 2): L(
        ("narrateur", "Une plume grise tourne avec le vent, sous les chaînes."),
        ("narrateur", "Elle part vers le claquement du volet, pas vers la rue."),
        ("enfant-m", "Pas le ballon, le bois."),
        ("narrateur", "Amir retient le caoutchouc du pied, sans frapper."),
        ("narrateur", "L'escargot suit la plume, descend, virgule au four."),
        ("papa", "Le vent a parlé plus juste que le poum."),
        ("narrateur", "La plume se pose sur le banc, à côté du kraft."),
        ("maman", "Il rentre, et la balançoire se tait."),
    ),
    (3, 1, 3): L(
        ("narrateur", "Amir s'assoit sur le banc, le ballon calé."),
        ("enfant-m", "La chaîne est à toi."),
        ("narrateur", "L'escargot descend, virgule tournée à la boulangerie."),
        ("narrateur", "Le siège cliquette, vide, au-dessus de lui."),
        ("narrateur", "Personne ne pousse."),
        ("maman", "Il n'avait pas demandé de danser."),
        ("narrateur", "Au bas, le trottoir du pain reprend."),
        ("papa", "Tu as regardé sa virgule, pas ton jeu."),
    ),
    (3, 2, 1): L(
        ("narrateur", "Amir entoure la flaque du seau avec des galets."),
        ("narrateur", "Un pont de pierres part vers le mur du four."),
        ("enfant-m", "Pas le miroir, le chemin."),
        ("narrateur", "L'escargot évite l'eau, et prend les creux."),
        ("narrateur", "La virgule de farine reste sèche, au volet."),
        ("papa", "Ton miroir tremblait, tes galets tiennent."),
        ("narrateur", "Le seau rentre dans le sac, sans une goutte de plus."),
        ("maman", "La chaîne peut cliqueter, lui rentre."),
    ),
    (3, 2, 2): L(
        ("narrateur", "Une plume dérive sur la flaque, sous la balançoire."),
        ("narrateur", "Elle file du côté du pain, pas du siège."),
        ("enfant-m", "Suis l'eau jusqu'au four, pas dessous."),
        ("narrateur", "Amir tient le seau haut, loin de la chaîne."),
        ("narrateur", "L'escargot borde la flaque, virgule au blond."),
        ("maman", "Le miroir a fait peur, la plume a dit le mur."),
        ("narrateur", "La plume s'échoue contre un galet, tournée boutique."),
        ("papa", "Tu n'as pas rajouté d'eau."),
    ),
    (3, 2, 3): L(
        ("narrateur", "Amir recule le seau, et la flaque s'arrête."),
        ("enfant-m", "Sans miroir, à toi."),
        ("narrateur", "L'escargot quitte la chaîne, loin de l'eau."),
        ("narrateur", "Sa virgule de farine reprend le trottoir du four."),
        ("narrateur", "Le siège passe au-dessus, vide."),
        ("papa", "Il n'a pas voulu se voir."),
        ("narrateur", "Sous les balançoires, le claquement du volet revient."),
        ("maman", "Tu as retiré l'eau, et lui a fini."),
    ),
    (3, 3, 1): L(
        ("narrateur", "Amir glisse un galet sous l'oreille, sur le siège."),
        ("narrateur", "Le doudou se soulève, et l'escargot a de l'air."),
        ("enfant-m", "Un sentier, plus une poche."),
        ("narrateur", "Les galets descendent de la chaîne vers le volet."),
        ("narrateur", "L'escargot les suit, virgule au bois blond."),
        ("maman", "Tu as libéré l'oreille, pas l'animal."),
        ("narrateur", "Le doudou reprend le sac, un peu de chaîne au poil."),
        ("papa", "Le galet garde le clic, tout lisse."),
    ),
    (3, 3, 2): L(
        ("narrateur", "Une plume s'échappe du doudou, sous les chaînes."),
        ("narrateur", "Le vent la tire vers le bois blond, entre les feuilles."),
        ("enfant-m", "Sors, le four est là."),
        ("narrateur", "Amir range le tissu, sans frotter la coquille."),
        ("narrateur", "L'escargot suit le duvet, descend, virgule au claquement."),
        ("papa", "Ta poche a fait trop d'ombre, le volet est clair."),
        ("narrateur", "La plume se pose sur le banc, près du kraft."),
        ("maman", "Il rentre, et le doudou reste à l'école dans le sac."),
    ),
    (3, 3, 3): L(
        ("narrateur", "Amir reprend le doudou, et le siège se vide."),
        ("enfant-m", "Toi, tu pars où tu veux."),
        ("narrateur", "L'escargot quitte la chaîne, virgule tournée vers chez lui."),
        ("narrateur", "Personne ne le colle, personne ne le pousse."),
        ("narrateur", "Le claquement du volet lui répond, derrière la haie."),
        ("maman", "Il n'avait pas demandé le voyage."),
        ("narrateur", "Sous la balançoire, la flaque redevient un ciel."),
        ("papa", "Tu as attendu qu'il finisse, et il a fini."),
    ),
}


def ending(a: int, b: int, c: int) -> list[tuple[str, str]]:
    recap = {
        (1, 1, 1): "On a fait un chemin de galets, et le ballon a dormi.",
        (1, 1, 2): "La plume a montré le volet, pas la rue du ballon.",
        (1, 1, 3): "J'ai regardé, et il a contourné le ballon tout seul.",
        (1, 2, 1): "Les galets ont barré l'eau, et il a pris le pont.",
        (1, 2, 2): "La plume a flotté vers le four, loin de la gouttière.",
        (1, 2, 3): "J'ai posé le seau, et il a évité le rond.",
        (1, 3, 1): "Le galet a levé l'oreille, et le chemin a parlé.",
        (1, 3, 2): "La plume est sortie du doudou, vers le bois blond.",
        (1, 3, 3): "J'ai gardé le doudou, et lui a choisi le mur.",
        (2, 1, 1): "Les galets ont fait un escalier, hors du poum.",
        (2, 1, 2): "La plume a glissé le métal, du côté du pain.",
        (2, 1, 3): "J'ai calé le ballon, et il a fini sa descente.",
        (2, 2, 1): "Les galets ont cassé la glissade, pierre après pierre.",
        (2, 2, 2): "La plume a montré le haut, où le volet se voit.",
        (2, 2, 3): "Sans goutte de plus, il a pris le trottoir du four.",
        (2, 3, 1): "Le galet a changé le nid en chemin.",
        (2, 3, 2): "La plume a tiré le doudou vers le blond.",
        (2, 3, 3): "J'ai rangé le doudou, et la pente lui est restée.",
        (3, 1, 1): "Les galets ont calé la chaîne, un sentier au sol.",
        (3, 1, 2): "La plume a tourné avec le vent, vers le claquement.",
        (3, 1, 3): "J'ai gardé le ballon, et la chaîne lui est restée.",
        (3, 2, 1): "Les galets ont entouré la flaque, un pont vers le mur.",
        (3, 2, 2): "La plume a dérivé sur l'eau, du côté du pain.",
        (3, 2, 3): "J'ai reculé le seau, et il a repris le trottoir.",
        (3, 3, 1): "Le galet a libéré l'oreille, et marqué le sentier.",
        (3, 3, 2): "La plume a fui le doudou, entre les feuilles.",
        (3, 3, 3): "J'ai vidé le siège, et il est rentré chez lui.",
    }
    keepsake = {
        1: "Contre la hanche, le sachet kraft a pris un grain de sable.",
        2: "Sur le kraft, la feuille jaune a laissé une nervure tiède.",
        3: "Le sachet kraft sent le clic des chaînes, un peu froid.",
    }
    tails = {
        (1, 1, 1): "Dans la poche, le galet garde le creux du bac.",
        (1, 1, 2): "Un duvet gris orne le kraft, tourné vers la boutique.",
        (1, 1, 3): "Un fil humide relie le sable au pied du volet.",
        (1, 2, 1): "Les galets barrent le filet, secs du côté four.",
        (1, 2, 2): "La plume sèche au pied du volet, comme une virgule.",
        (1, 2, 3): "Le rond du seau s'efface, et le mur reste.",
        (1, 3, 1): "Le galet chaud a du sable, et le doudou a de l'air.",
        (1, 3, 2): "Le kraft porte la plume, collée côté pain.",
        (1, 3, 3): "Le creux du bac reste vide, du côté de la rue.",
        (2, 1, 1): "L'escalier de pierres mène du zinc au trottoir du four.",
        (2, 1, 2): "La plume et la feuille se touchent, côté boutique.",
        (2, 1, 3): "Le métal est vide, et le pain appelle.",
        (2, 2, 1): "Les galets tiennent la pente, hors de l'eau.",
        (2, 2, 2): "Du haut, le volet blond a repris sa virgule d'ombre.",
        (2, 2, 3): "Une trace humide sèche sur le zinc, sans lui.",
        (2, 3, 1): "La fourrure sent le zinc, plus la coquille.",
        (2, 3, 2): "La plume et la feuille jaune regardent le four.",
        (2, 3, 3): "Le toboggan reste seul, et le claquement répond.",
        (3, 1, 1): "Les galets gardent le bas de la chaîne, hors de la rue.",
        (3, 1, 2): "La plume du banc frôle le kraft, côté volet.",
        (3, 1, 3): "Le siège cliquette, vide, au-dessus du trottoir du pain.",
        (3, 2, 1): "Le pont de pierres contourne la flaque, vers le mur.",
        (3, 2, 2): "La plume s'est échouée contre un galet, tournée boutique.",
        (3, 2, 3): "Sous les chaînes, le claquement du volet est revenu.",
        (3, 3, 1): "Le galet du siège a gardé le clic, tout lisse.",
        (3, 3, 2): "La plume du banc attend près du petit pain.",
        (3, 3, 3): "La flaque sous la balançoire redevient un ciel.",
    }
    last = {
        (1, 1, 1): "Sur le volet, une virgule neuve a remplacé la première.",
        (1, 1, 2): "Le sachet kraft froisse, et la virgule du volet s'est déplacée.",
        (1, 1, 3): "L'escargot reprend le bois blond, sans le sachet.",
        (1, 2, 1): "Le petit pain reste tiède, et le volet a son locataire.",
        (1, 2, 2): "Une virgule de farine orne le kraft, minuscule.",
        (1, 2, 3): "Les clés de papa répondent au volet, plus bas.",
        (1, 3, 1): "Le doudou sent le four, plus le sable.",
        (1, 3, 2): "La lune de farine a glissé du volet au papier.",
        (1, 3, 3): "Amir serre le kraft vide d'escargot, plein de pain.",
        (2, 1, 1): "La feuille jaune s'est posée sur le volet, près de lui.",
        (2, 1, 2): "Le sachet kraft a une nervure, et le volet a sa virgule.",
        (2, 1, 3): "Le métal s'est tu, et le bois blond reprend le tap-tap.",
        (2, 2, 1): "Le seau dans le sac ne cliquette plus.",
        (2, 2, 2): "Du parc, on voit la virgule, revenue sur le volet.",
        (2, 2, 3): "Le souffle de pain marche avec eux, jusqu'à la grille.",
        (2, 3, 1): "Le doudou a un peu de zinc au poil, rien d'autre.",
        (2, 3, 2): "Le kraft froisse, et le volet claque plus bas.",
        (2, 3, 3): "L'escargot est au bois, et le petit pain à l'école.",
        (3, 1, 1): "Les chaînes se taisent, et le volet reprend le rythme.",
        (3, 1, 2): "Le kraft porte un duvet, et le volet porte sa lune.",
        (3, 1, 3): "Amir lâche le ballon dans le sac, les mains libres.",
        (3, 2, 1): "La flaque sèche, et le volet garde sa virgule.",
        (3, 2, 2): "Le seau sent l'eau, le kraft sent le four.",
        (3, 2, 3): "Les manches jaunes d'Amir ont pris le souffle du pain.",
        (3, 3, 1): "Le galet de poche tinte contre les clés, tout lisse.",
        (3, 3, 2): "La poire attend, et la plume aussi, sur le kraft.",
        (3, 3, 3): "Le volet blond est remonté, et la virgule brille ailleurs.",
    }
    invite = {
        1: "Raconte le bac, on a fini nos phrases.",
        2: "Raconte le toboggan, on t'écoute jusqu'au bout.",
        3: "Raconte les chaînes, c'est ton tour.",
    }
    return L(
        ("narrateur", "Plus tard, devant l'école, le sachet kraft reste tiède."),
        ("maman", invite[a]),
        ("enfant-m", recap[(a, b, c)]),
        ("narrateur", keepsake[a]),
        ("narrateur", tails[(a, b, c)]),
        ("narrateur", last[(a, b, c)]),
    )


T3_SONS = {1: "galet", 2: "vent", 3: "escargot"}
FIN_SONS = {1: "pain,pas", 2: "pain,metal", 3: "pain,chaine"}


def path_len(by: dict, a: int, b: int, c: int) -> int:
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


def build() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "volet,pain", "emphasis": "virgule de farine"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Le parc du volet blond a trois coins pour le suivre."),
            ("papa", "Le bac à sable, le toboggan, ou les balançoires ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "le bac à sable",
            "option_2_label": "le toboggan",
            "option_3_label": "les balançoires",
        }},
    )

    for a, t1 in T1.items():
        base = f"CHK_T0001_P000{a}"
        by[base] = voice(by_old[base], t1["passage"], "action", extra={"sons": t1["sons"], "emphasis": "virgule"})
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
                "engine_near_text": "Tu es tout près. Reprenons l'indice.",
            }},
        )
        cid = f"{base}_C0001"
        by[cid] = voice(by_old[cid], t1["confirm"], "confirm", extra={"sons": "", "emphasis": "Merci"})
        tid = f"{base}_T0002_P0000"
        by[tid] = voice(
            by_old[tid], t1["choice"], "choice",
            extra={"sons": "", "fields": {
                "option_1_label": "le ballon",
                "option_2_label": "le seau",
                "option_3_label": "le doudou",
            }},
        )
        for b in (1, 2, 3):
            p2 = f"{base}_T0002_P000{b}"
            by[p2] = voice(
                by_old[p2], T2_FN[b](a), "obstacle",
                extra={"sons": T2_SONS[b], "emphasis": "virgule de farine"},
            )
            t3q = f"{p2}_T0003_P0000"
            by[t3q] = voice(
                by_old[t3q], t3_choice(b), "choice",
                extra={"sons": "", "fields": {
                    "option_1_label": "le galet",
                    "option_2_label": "la plume",
                    "option_3_label": "l'escargot",
                }},
            )
            for c in (1, 2, 3):
                leaf = f"{p2}_T0003_P000{c}"
                by[leaf] = voice(
                    by_old[leaf], T3[(a, b, c)], "resolution",
                    extra={"sons": T3_SONS[c], "emphasis": T3_NAME[c].split()[-1]},
                )
                fin = f"{leaf}_F0001"
                by[fin] = voice(
                    by_old[fin], ending(a, b, c), "ending",
                    extra={"sons": FIN_SONS[c], "emphasis": "sachet kraft"},
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
        "Au coin de la rue, l'odeur du pain arrive avant la boutique. "
        "Amir voit une virgule de farine sur le volet blond, puis la même "
        "sur la coquille d'un escargot. Il tend le sachet kraft du petit pain : "
        "l'animal rentre sa tête. Papa et maman parlent ; Amir attend, on l'entend. "
        "Mission : ramener l'escargot au volet sans le prendre, et porter le pain "
        "à l'école. Bac, toboggan ou balançoires ; ballon, seau ou doudou gênent "
        "plus qu'ils n'aident ; galet, plume ou regard rendent le chemin du four. "
        "La virgule pointait la maison de l'escargot, pas l'école. Devant la grille, "
        "Amir raconte, et on l'écoute jusqu'au bout."
    )
    out["title"] = "L'escargot de la boulangerie"
    out["characters"] = "Amir, papa, maman"
    out["setting"] = "rue, boulangerie, petit parc avant l'école"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    low = "\n".join(c["script"] for c in out["chunks"]).lower()
    for tic in TICS + ("papa sourit", "maman sourit", "on attend. puis"):
        if tic in low:
            raise SystemExit(f"tic global: {tic}")
    n_enc = len(re.findall(r"\bencore\b", low))
    n_dej = len(re.findall(r"\bdéjà\b", low))
    if n_enc > 2 or n_dej > 2:
        raise SystemExit(f"tics encore={n_enc} déjà={n_dej}")

    lengths = [path_len(by, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins {min(lengths)}–{max(lengths)} moy {sum(lengths)//len(lengths)}")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        "# TREE-COL-017 — L'escargot de la boulangerie\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Vécu\n"
        "Rue : l'odeur du pain marche avant la boutique. Volet blond, virgule de "
        "farine (indice unique), sachet kraft du petit pain. Amir croit que "
        "l'escargot veut l'école ; il tend le sachet, l'animal se cache. Les voix "
        "des adultes couvrent son cri ; il attend, on l'entend. Au parc du volet "
        "blond, râteau / souffle / chaîne échouent. Ballon, seau, doudou rendent "
        "un deuxième piège (rue, gouttière, ombre). Galet, plume ou regard "
        "paient la virgule : elle pointait le four, pas le sac. 27 fins : le "
        "sachet, le volet ou la virgule ont changé. Tours de parole vécus. "
        "Monde ≠ TREE-COL-015 (pas de jardin, pas de trace d'argent).\n\n"
        "## Vu et corrigé\n"
        "- Titre noyau conservé. N3 ≤ 16. Troupe D16 : Amir, papa, maman.\n"
        "- T3 Tom/Léa/Sami → galet / plume / escargot.\n"
        "- Leçon COL.ECO.001 vécue (envie de couper, retenue, écoute, plaisir "
        "d'être entendu), jamais récitée. Pas « maîtresse / si malaise ».\n"
        "- 27 fins textuellement distinctes. Un merci vécu (T1), pas un refrain Bravo.\n"
        "- TTS par chunk (profils opening/choice/clue/confirm/action/obstacle/resolution/ending).\n"
        f"- Mots par chemin : {min(lengths)}–{max(lengths)} (moy {sum(lengths)//len(lengths)}).\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés. Pas apply.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(f"OK {SID} {nwords} mots  fins={len(set(fins))}")


if __name__ == "__main__":
    build()
