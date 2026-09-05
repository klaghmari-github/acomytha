#!/usr/bin/env python3
"""TREE-DIF-069 — Le camion de carton de Raphaël, dans la cave (N2, DIF.PAR.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-069"
LIM = 15
TITLE = "Le camion de carton de Raphaël, dans la cave"
FIL = (
    "Dans la cave, Raphaël veut un camion de carton pour descendre une pomme, "
    "avec Chouchou. Il lui demande un mot : elle tape, elle pousse, elle montre. "
    "T1 = carton / crayon gras / ficelle, les trois partent. "
    "T2 = râtelier (pommes, deux désirs) / marche trop étroite / "
    "ampoule (elle reste dans le jaune). "
    "T3 = neuf façons de la lire. Le camion glisse, une pomme dessus, on remonte."
)
CHARS = "Raphaël, Chouchou, papa, maman"
SETTING = "cave sous la maison : râtelier de pommes, marche, ampoule jaune"
TICS = (
    "tout doux",
    "tout calme",
    "on lève la main",
    "puis on parle",
    "c'est du bon travail",
    "parle peu",
    "parlé peu",
    "camarade",
    "timide",
    "forcer la parole",
    "un camarade",
    "dînette",
    "dinette",
    "après la sieste",
    "cuisine",
    "nichoir",
    "locomotive",
    "gare en carton",
    "cuillère",
    "véranda",
    "galet",
    "merle",
    "capitaine",
    "bac à sable",
    "toboggan",
    "balançoire",
    "l'histoire est finie",
    "on va apprendre",
    "voici le geste",
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
        f"{body}</prosody><break time=\"{m['pause']}ms\"/></speak>"
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
        note="arc=installation; intention=émerveiller; emotion=envie_impatiente; intensite=1; destinataire=enfant; sous_texte=il_veut_un_mot_elle_pousse; tempo=naturel; sourire=léger; respiration=ample",
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
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_a_pris; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=le_camion_peut_partir; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il_veut_qu_elle_dise_le_mot; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_découragement; intensite=2; destinataire=enfant; sous_texte=deux_désirs_au_même_instant; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=lire_ses_mains_ouvre_le_camion; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_pomme_remonte_avec_le_carton; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def L(*rows: tuple[str, str]) -> list[tuple[str, str]]:
    return list(rows)


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


OPENING = L(
    ("narrateur", "L'odeur des pommes grimpe l'escalier de pierre."),
    ("narrateur", "Dans le couloir, l'air pique comme la pierre."),
    ("narrateur", "En bas, l'ampoule jaune tremble."),
    ("papa", "Tu entends ce bruit, Raphaël ?"),
    ("enfant-m", "Le carton racle contre le mur."),
    ("maman", "Chouchou est près du râtelier."),
    ("narrateur", "Un râtelier de bois tient des pommes, trop haut."),
    ("narrateur", "Une pomme rouge brille, un peu poussiéreuse."),
    ("narrateur", "En ce moment, Raphaël pose un pied sur la marche."),
    ("enfant-m", "On fait un camion, pour une pomme."),
    ("narrateur", "Chouchou tape deux fois le carton."),
    ("papa", "Elle pousse, elle."),
    ("enfant-m", "Dis camion, Chouchou !"),
    ("narrateur", "Chouchou pousse le carton, les lèvres fermées."),
    ("papa", "Merci, tu as tenu la rampe."),
)

T1Q = L(
    ("narrateur", "Trois choses attendent près de la marche."),
    ("narrateur", "Un grand carton, un crayon gras, une ficelle."),
    ("papa", "Tu prends quoi d'abord, Raphaël ?"),
)

T1 = {
    1: dict(
        name="le carton",
        expected="carton",
        accepted="carton | le carton | le grand carton",
        retry="Raphaël prend le carton.",
        ok="Oui, le grand carton.",
        sons="carton,cave",
        emphasis="carton",
        passage=L(
            ("narrateur", "Raphaël prend le grand carton."),
            ("enfant-m", "Il va devenir un camion."),
            ("papa", "Plie le bord, sans le casser."),
            ("narrateur", "Le carton racle, puis se plie."),
            ("enfant-m", "Dis camion, Chouchou !"),
            ("narrateur", "Chouchou tape deux fois le fond."),
            ("narrateur", "Le crayon et la ficelle glissent près d'elle."),
            ("maman", "Les trois viennent avec vous."),
            ("narrateur", "Papa pose le crayon contre le carton."),
            ("narrateur", "La ficelle s'enroule autour d'un coin."),
            ("enfant-m", "Chouchou, tu viens ?"),
            ("narrateur", "Elle pousse le carton vers le râtelier."),
            ("papa", "Le carton, vous l'avez."),
        ),
        question=L(
            ("narrateur", "Raphaël a pris le carton."),
            ("maman", "Il a pris quoi ?"),
        ),
        confirm=L(
            ("narrateur", "Le carton reste contre eux, plié en camion."),
            ("enfant-m", "On va chercher une pomme."),
            ("narrateur", "Chouchou pose une main dessus, toute plate."),
            ("maman", "Le râtelier n'est pas loin."),
            ("papa", "Tu tiens bien, Raphaël ?"),
            ("enfant-m", "Oui, papa."),
            ("narrateur", "Le carton attend, en forme de camion."),
        ),
        hip="Le carton racle sous ses mains.",
    ),
    2: dict(
        name="le crayon",
        expected="crayon",
        accepted="crayon | le crayon | le crayon gras",
        retry="Raphaël prend le crayon.",
        ok="Oui, le crayon gras.",
        sons="crayon,cave",
        emphasis="crayon",
        passage=L(
            ("narrateur", "Raphaël prend le crayon gras."),
            ("enfant-m", "Il va dessiner les roues."),
            ("maman", "Un trait, pas tout le crayon."),
            ("narrateur", "Un cercle jaune apparaît, un peu gras."),
            ("enfant-m", "Dis roue, Chouchou !"),
            ("narrateur", "Chouchou trace un rond, avec le doigt."),
            ("narrateur", "Le carton et la ficelle glissent près d'eux."),
            ("papa", "Les trois viennent avec vous."),
            ("narrateur", "Maman glisse le carton sous le crayon."),
            ("narrateur", "La ficelle sert de corde, un peu rêche."),
            ("enfant-m", "Chouchou, c'est ta roue ?"),
            ("narrateur", "Elle appuie le doigt au centre."),
            ("maman", "Le crayon, vous l'avez."),
        ),
        question=L(
            ("narrateur", "Raphaël a pris le crayon."),
            ("maman", "Il a pris quoi ?"),
        ),
        confirm=L(
            ("narrateur", "Le crayon pend un peu, tout gras."),
            ("enfant-m", "Les roues sont là."),
            ("narrateur", "Chouchou garde le carton contre son genou."),
            ("papa", "Ça sent le bois, ici."),
            ("maman", "Tes mains sont prêtes ?"),
            ("enfant-m", "Oui, maman."),
            ("narrateur", "Un trait de crayon montre une roue."),
        ),
        hip="Le crayon gras chauffe dans sa main.",
    ),
    3: dict(
        name="la ficelle",
        expected="ficelle",
        accepted="ficelle | la ficelle | le fil",
        retry="Raphaël prend la ficelle.",
        ok="Oui, la ficelle.",
        sons="ficelle,cave",
        emphasis="ficelle",
        passage=L(
            ("narrateur", "Raphaël prend la ficelle beige."),
            ("enfant-m", "Elle va tirer le camion."),
            ("papa", "Un nœud, pas trop serré."),
            ("narrateur", "La ficelle gratte, puis tient."),
            ("enfant-m", "Dis corde, Chouchou !"),
            ("narrateur", "Chouchou enroule un tour, paume ouverte."),
            ("narrateur", "Le carton et le crayon glissent près d'elle."),
            ("maman", "Les trois viennent avec vous."),
            ("narrateur", "Papa pose le carton contre la marche."),
            ("narrateur", "Le crayon reste au bord, tout gras."),
            ("enfant-m", "Chouchou, tu tiens ?"),
            ("narrateur", "Elle tend la ficelle, paume ouverte."),
            ("papa", "La ficelle, vous l'avez."),
        ),
        question=L(
            ("narrateur", "Raphaël a pris la ficelle."),
            ("maman", "Il a pris quoi ?"),
        ),
        confirm=L(
            ("narrateur", "La ficelle reste enroulée contre sa paume."),
            ("enfant-m", "Elle va tirer."),
            ("narrateur", "Chouchou tient le bout, tout près."),
            ("maman", "Le nœud sent le tiroir."),
            ("papa", "On avance, tous les deux ?"),
            ("enfant-m", "Oui."),
            ("narrateur", "Un bout de ficelle sert de corde."),
        ),
        hip="La ficelle gratte un peu sa paume.",
    ),
}


def t2_question(t1: int) -> list[tuple[str, str]]:
    return L(
        ("narrateur", T1[t1]["hip"]),
        ("narrateur", "Devant, le râtelier laisse rouler des pommes."),
        ("narrateur", "La marche, trop étroite, pince le carton."),
        ("narrateur", "Sous l'ampoule, une ombre arrête Chouchou."),
        ("papa", "Raphaël, tu vas où ?"),
    )


T2_SONS = {1: "pommes,râtelier", 2: "pierre,marche", 3: "ampoule,ombre"}
T2_EMP = {1: "pommes", 2: "marche", 3: "ombre"}
T3_LABS = {
    1: ("les pommes", "le bas", "son doigt"),
    2: ("le bord", "de côté", "sa main"),
    3: ("la lumière", "son ombre", "son mot"),
}


def t2_scene(t1: int, t2: int) -> list[tuple[str, str]]:
    return {
        (1, 1): L(
            ("narrateur", "Une pomme tombe du râtelier, puis une autre."),
            ("narrateur", "Le carton tremble, trop vite, trop fort."),
            ("enfant-m", "Attrape, Chouchou !"),
            ("narrateur", "Raphaël ouvre les bras, impatient."),
            ("narrateur", "Chouchou montre une pomme, du doigt."),
            ("narrateur", "Les pommes roulent, trop vite pour lui."),
            ("papa", "Ici, ça n'arrête pas."),
            ("maman", "Elle montre, avec le doigt."),
            ("enfant-m", "Alors on fait quoi ?"),
            ("papa", "Tu vois comment, Raphaël ?"),
        ),
        (2, 1): L(
            ("narrateur", "Les pommes rebondissent près du crayon gras."),
            ("narrateur", "Le crayon saute, trop sec, trop vite."),
            ("enfant-m", "Dessine la roue, Chouchou !"),
            ("narrateur", "Raphaël tend le crayon, les joues chaudes."),
            ("narrateur", "Chouchou pose le crayon, puis montre une pomme."),
            ("narrateur", "Il voulait une roue, elle voulait la pomme."),
            ("papa", "Deux envies, au même moment."),
            ("maman", "Son doigt n'a pas bougé."),
            ("enfant-m", "Alors on fait quoi ?"),
            ("maman", "Tu vois comment, Raphaël ?"),
        ),
        (3, 1): L(
            ("narrateur", "Une pomme tape la ficelle, puis file."),
            ("narrateur", "La ficelle se tend, trop vite, trop fort."),
            ("enfant-m", "Tire, Chouchou !"),
            ("narrateur", "Raphaël tire, les épaules raides."),
            ("narrateur", "Chouchou tient la ficelle, sans tirer."),
            ("narrateur", "Son doigt montre la pomme arrêtée."),
            ("papa", "Elle ne tire pas."),
            ("maman", "Elle montre celle qui s'est tue."),
            ("enfant-m", "Alors on fait quoi ?"),
            ("papa", "Tu vois comment, Raphaël ?"),
        ),
        (1, 2): L(
            ("narrateur", "La marche de pierre pince le carton, trop large."),
            ("narrateur", "Le carton plie, trop raide pour passer."),
            ("enfant-m", "Pousse, Chouchou !"),
            ("narrateur", "Raphaël pousse tout seul, et rien ne bouge."),
            ("narrateur", "Chouchou s'assoit, les deux mains à plat."),
            ("narrateur", "Ses épaules tombent, le camion reste coincé."),
            ("papa", "Ici, c'est trop étroit."),
            ("maman", "Le camion n'arrive pas."),
            ("enfant-m", "Alors on fait quoi ?"),
            ("maman", "Tu vois comment, Raphaël ?"),
        ),
        (2, 2): L(
            ("narrateur", "Raphaël trace un trait jaune sur la pierre."),
            ("narrateur", "Le crayon tombe, trop près de la marche."),
            ("enfant-m", "Passe, Chouchou !"),
            ("narrateur", "Il montre le trait, comme une route."),
            ("narrateur", "Chouchou couvre le crayon de sa paume."),
            ("narrateur", "Le trait s'arrête, et elle ne suit pas."),
            ("papa", "Sa main a dit non."),
            ("maman", "La pierre pince, même avec le trait."),
            ("enfant-m", "Alors on fait quoi ?"),
            ("papa", "Tu vois comment, Raphaël ?"),
        ),
        (3, 2): L(
            ("narrateur", "La ficelle se coince dans une fente de pierre."),
            ("narrateur", "Raphaël tire, et la ficelle racle, trop large."),
            ("enfant-m", "Tire avec moi !"),
            ("narrateur", "Il tire plus fort, et le nœud brûle sa paume."),
            ("narrateur", "Chouchou serre le nœud contre sa poitrine."),
            ("narrateur", "Elle ne lâche pas, et elle ne tire pas."),
            ("papa", "Le nœud ne veut pas."),
            ("maman", "Elle garde le fil, contre elle."),
            ("enfant-m", "Alors on fait quoi ?"),
            ("maman", "Tu vois comment, Raphaël ?"),
        ),
        (1, 3): L(
            ("narrateur", "L'ampoule jaune laisse un coin d'ombre."),
            ("narrateur", "Le carton s'arrête, trop près de l'ombre."),
            ("enfant-m", "Viens, Chouchou !"),
            ("narrateur", "Raphaël avance le carton vers le noir."),
            ("narrateur", "Chouchou recule, collée au cercle jaune."),
            ("narrateur", "L'ombre tremble, trop noire pour elle."),
            ("papa", "Ici, ça fait trop d'ombre."),
            ("maman", "Elle reste près de la lumière."),
            ("enfant-m", "Alors on fait quoi ?"),
            ("papa", "Tu vois comment, Raphaël ?"),
        ),
        (2, 3): L(
            ("narrateur", "Raphaël dessine une route jaune vers l'ombre."),
            ("narrateur", "Le trait disparaît, trop pris par le noir."),
            ("enfant-m", "Suis le trait, Chouchou !"),
            ("narrateur", "Il tend le crayon, impatient."),
            ("narrateur", "Chouchou trace un rond, dans le jaune."),
            ("narrateur", "Elle reste dans le cercle de l'ampoule."),
            ("papa", "Sa route à elle est ronde."),
            ("maman", "Le noir a mangé ton trait."),
            ("enfant-m", "Alors on fait quoi ?"),
            ("maman", "Tu vois comment, Raphaël ?"),
        ),
        (3, 3): L(
            ("narrateur", "Raphaël jette la ficelle dans l'ombre, comme un chemin."),
            ("narrateur", "La ficelle se tait, trop près du noir."),
            ("enfant-m", "Suis la corde !"),
            ("narrateur", "Il tire un peu, et rien ne vient."),
            ("narrateur", "Chouchou enroule la ficelle à son poignet."),
            ("narrateur", "Elle reste dans le jaune, le fil autour."),
            ("papa", "Le fil est à elle, maintenant."),
            ("maman", "Elle n'entre pas dans l'ombre."),
            ("enfant-m", "Alors on fait quoi ?"),
            ("papa", "Tu vois comment, Raphaël ?"),
        ),
    }[(t1, t2)]


def t3_question(t2: int) -> list[tuple[str, str]]:
    if t2 == 1:
        return L(
            ("narrateur", "Les pommes n'ont pas fini de rouler."),
            ("papa", "Les pommes, le bas, ou son doigt ?"),
        )
    if t2 == 2:
        return L(
            ("narrateur", "Le carton n'a pas fini de coincer."),
            ("maman", "Le bord, de côté, ou sa main ?"),
        )
    return L(
        ("narrateur", "L'ombre n'a pas fini de trembler."),
        ("papa", "La lumière, son ombre, ou son mot ?"),
    )


T3 = {
    (1, 1, 1): L(
        ("enfant-m", "On attend les pommes."),
        ("narrateur", "Il tient le carton, sans le pousser."),
        ("narrateur", "Les pommes se taisent, une, puis plus."),
        ("narrateur", "Chouchou pose une pomme, sans bruit."),
        ("papa", "Les pommes se sont tues."),
        ("enfant-m", "Elle a posé, toute seule."),
        ("maman", "Tu as attendu, et elle a posé."),
    ),
    (1, 1, 2): L(
        ("enfant-m", "En bas, d'abord."),
        ("narrateur", "Il baisse le carton, loin des pommes qui tombent."),
        ("narrateur", "Chouchou s'accroupit aussi, les lèvres fermées."),
        ("narrateur", "Raphaël met les genoux au sol froid."),
        ("papa", "Tu as vu le bas, avant."),
        ("enfant-m", "Ici, ça ne tombe plus."),
        ("maman", "Près du sol, ça tenait mieux."),
    ),
    (1, 1, 3): L(
        ("enfant-m", "Ton doigt, Chouchou."),
        ("narrateur", "Elle montre une pomme, tout près du râtelier."),
        ("narrateur", "Raphaël attend, puis suit le doigt."),
        ("narrateur", "Elle glisse le carton sous la pomme choisie."),
        ("papa", "Le doigt n'a pas bougé."),
        ("copine", "Pomme."),
        ("maman", "Son doigt a choisi."),
    ),
    (1, 2, 1): L(
        ("enfant-m", "On attend au bord."),
        ("narrateur", "Le carton reste collé à la marche."),
        ("narrateur", "Chouchou s'assoit, les mains à plat."),
        ("narrateur", "Puis elle penche le carton, sans bruit."),
        ("papa", "La marche n'a plus pincé."),
        ("enfant-m", "Maintenant, ça passe."),
        ("maman", "Tu as laissé le bord finir."),
    ),
    (1, 2, 2): L(
        ("enfant-m", "De côté, d'abord."),
        ("narrateur", "Chouchou tourne le carton, paume ouverte."),
        ("narrateur", "Raphaël suit ses mains, tout lent."),
        ("narrateur", "De côté, le carton n'est plus trop large."),
        ("papa", "Tu as tourné, sans forcer."),
        ("enfant-m", "Il passe de côté."),
        ("maman", "De côté, la marche était plus douce."),
    ),
    (1, 2, 3): L(
        ("enfant-m", "Ta main, Chouchou."),
        ("narrateur", "Elle pousse le carton, tout près de la marche."),
        ("narrateur", "Raphaël attend, puis pousse avec elle."),
        ("narrateur", "Sa main pousse le carton, d'un seul coup."),
        ("papa", "Sa main a guidé le bord."),
        ("copine", "Pousse."),
        ("maman", "Vous avez poussé ensemble."),
    ),
    (1, 3, 1): L(
        ("enfant-m", "On attend la lumière."),
        ("narrateur", "L'ampoule jaune tremble, puis se tient."),
        ("narrateur", "Chouchou reste collée au cercle jaune."),
        ("narrateur", "Sous la lumière, le carton ne tremble plus."),
        ("papa", "La lumière est revenue."),
        ("enfant-m", "Tu peux venir, maintenant."),
        ("maman", "Tu as laissé la lumière arriver."),
    ),
    (1, 3, 2): L(
        ("enfant-m", "Ton ombre, d'abord."),
        ("narrateur", "Raphaël se glisse près d'elle, dans le jaune."),
        ("narrateur", "Chouchou reste dans le jaune, paume ouverte."),
        ("narrateur", "Dans le jaune, le carton n'a plus d'ombre."),
        ("papa", "Tu t'es mis tout près, avec elle."),
        ("enfant-m", "On reste ici."),
        ("maman", "Près d'elle, le jaune suffisait."),
    ),
    (1, 3, 3): L(
        ("enfant-m", "Ton mot, Chouchou."),
        ("narrateur", "Raphaël attend, les lèvres fermées."),
        ("narrateur", "Chouchou ouvre la bouche, tout petit."),
        ("copine", "Viens."),
        ("narrateur", "Le carton avance d'un pas, dans le jaune."),
        ("papa", "Elle a dit le mot, toute seule."),
        ("maman", "Le mot était tout bas, à elle."),
    ),
    (2, 1, 1): L(
        ("enfant-m", "On laisse les pommes finir."),
        ("narrateur", "Il tient le crayon, sans tracer."),
        ("narrateur", "Une pomme roule, puis s'arrête contre le bois."),
        ("narrateur", "Chouchou pose cette pomme près du cercle jaune."),
        ("papa", "Celle-là s'est arrêtée."),
        ("enfant-m", "Elle a choisi la rouge."),
        ("maman", "Tu as laissé le crayon se taire."),
    ),
    (2, 1, 2): L(
        ("enfant-m", "On se baisse."),
        ("narrateur", "Il baisse le crayon, loin des pommes."),
        ("narrateur", "Chouchou s'accroupit, le doigt sur le rond jaune."),
        ("narrateur", "Raphaël a les genoux froids, et il rit."),
        ("papa", "En bas, le crayon ne saute plus."),
        ("enfant-m", "La roue est plus près du sol."),
        ("maman", "Près du sol, la pomme tient."),
    ),
    (2, 1, 3): L(
        ("enfant-m", "Je suis ton doigt."),
        ("narrateur", "Elle montre la pomme collée au bois."),
        ("narrateur", "Raphaël pose le crayon vers cette pomme."),
        ("narrateur", "Le trait jaune touche la peau rouge."),
        ("papa", "Le doigt et le trait se rejoignent."),
        ("copine", "Roue."),
        ("maman", "Elle a dit le mot de la roue."),
    ),
    (2, 2, 1): L(
        ("enfant-m", "On laisse le bord."),
        ("narrateur", "Le crayon reste collé à la marche."),
        ("narrateur", "Chouchou garde sa paume sur le bois."),
        ("narrateur", "Le trait jaune sèche, puis elle lève la main."),
        ("papa", "La pierre n'a plus pincé."),
        ("enfant-m", "Le trait peut passer."),
        ("maman", "Tu as laissé sa paume finir."),
    ),
    (2, 2, 2): L(
        ("enfant-m", "On tourne le trait."),
        ("narrateur", "Chouchou tourne le carton, le crayon dessus."),
        ("narrateur", "Raphaël suit le rond jaune, de côté."),
        ("narrateur", "De côté, le crayon n'accroche plus la pierre."),
        ("papa", "Le trait a trouvé un autre chemin."),
        ("enfant-m", "Ma roue passe."),
        ("maman", "De côté, la pierre était plus large."),
    ),
    (2, 2, 3): L(
        ("enfant-m", "Ta main, sur le crayon."),
        ("narrateur", "Elle pousse près du crayon, d'un seul coup."),
        ("narrateur", "Raphaël attend, puis pousse avec elle."),
        ("narrateur", "Le trait jaune glisse le long de la pierre."),
        ("papa", "Sa main a guidé le crayon."),
        ("copine", "Roue."),
        ("maman", "Vous avez poussé le trait ensemble."),
    ),
    (2, 3, 1): L(
        ("enfant-m", "On attend le jaune."),
        ("narrateur", "L'ampoule se tient, et le trait redevient visible."),
        ("narrateur", "Chouchou reste dans le cercle, le crayon au chaud."),
        ("narrateur", "Sous la lumière, le crayon ne glisse plus."),
        ("papa", "Le jaune a repris le trait."),
        ("enfant-m", "Ma roue est revenue."),
        ("maman", "Tu as laissé l'ampoule finir de trembler."),
    ),
    (2, 3, 2): L(
        ("enfant-m", "Je viens dans ton rond."),
        ("narrateur", "Raphaël s'assoit dans le jaune, près d'elle."),
        ("narrateur", "Chouchou lui rend le crayon, paume ouverte."),
        ("narrateur", "Dans le jaune, le crayon n'a plus d'ombre."),
        ("papa", "Tu t'es mis dans son cercle."),
        ("enfant-m", "On dessine ici."),
        ("maman", "Près d'elle, le trait tenait."),
    ),
    (2, 3, 3): L(
        ("enfant-m", "Ton mot, pour le trait."),
        ("narrateur", "Raphaël attend, le crayon posé."),
        ("narrateur", "Chouchou ouvre la bouche, tout petit."),
        ("copine", "Jaune."),
        ("narrateur", "Le crayon avance d'un pas, dans le jaune."),
        ("papa", "Le mot était à elle."),
        ("maman", "Jaune, comme l'ampoule."),
    ),
    (3, 1, 1): L(
        ("enfant-m", "On laisse la ficelle se taire."),
        ("narrateur", "Il tient la ficelle, sans tirer."),
        ("narrateur", "Les pommes s'arrêtent, une reste contre le nœud."),
        ("narrateur", "Chouchou pose cette pomme dans le carton."),
        ("papa", "Le nœud a eu le temps."),
        ("enfant-m", "Elle a mis la pomme."),
        ("maman", "Tu as laissé le fil se reposer."),
    ),
    (3, 1, 2): L(
        ("enfant-m", "On se met tout bas."),
        ("narrateur", "Il baisse la ficelle, loin des pommes."),
        ("narrateur", "Chouchou s'accroupit, le bout du fil au sol."),
        ("narrateur", "Raphaël a les genoux froids, le nœud lâche."),
        ("papa", "En bas, ça ne tape plus."),
        ("enfant-m", "La corde est plus courte."),
        ("maman", "Près du sol, le fil tenait."),
    ),
    (3, 1, 3): L(
        ("enfant-m", "Je suis ton doigt, avec le fil."),
        ("narrateur", "Elle montre la pomme arrêtée près du nœud."),
        ("narrateur", "Raphaël tend la ficelle vers cette pomme."),
        ("narrateur", "Elle glisse le fil sous la pomme choisie."),
        ("papa", "Le doigt a mené le nœud."),
        ("copine", "Fil."),
        ("maman", "Son doigt a tiré sans tirer."),
    ),
    (3, 2, 1): L(
        ("enfant-m", "On laisse le nœud."),
        ("narrateur", "La ficelle reste collée à la marche."),
        ("narrateur", "Chouchou s'assoit, le nœud contre le genou."),
        ("narrateur", "Le fil se desserre, puis elle penche le carton."),
        ("papa", "La fente n'a plus mordu."),
        ("enfant-m", "Le nœud passe."),
        ("maman", "Tu as laissé le fil se desserrer."),
    ),
    (3, 2, 2): L(
        ("enfant-m", "On tourne le fil."),
        ("narrateur", "Chouchou tourne le carton, la ficelle autour."),
        ("narrateur", "Raphaël suit le nœud, de côté."),
        ("narrateur", "De côté, la ficelle n'accroche plus la pierre."),
        ("papa", "Le fil a trouvé un autre bord."),
        ("enfant-m", "Ma corde passe."),
        ("maman", "De côté, la fente était moins profonde."),
    ),
    (3, 2, 3): L(
        ("enfant-m", "Ta main, sur le nœud."),
        ("narrateur", "Elle pousse près de la ficelle, d'un seul coup."),
        ("narrateur", "Raphaël attend, puis pousse avec elle."),
        ("narrateur", "Sa main pousse près de la ficelle, d'un seul coup."),
        ("papa", "Sa main a guidé le nœud."),
        ("copine", "Nœud."),
        ("maman", "Vous avez poussé le fil ensemble."),
    ),
    (3, 3, 1): L(
        ("enfant-m", "On attend que ça brille."),
        ("narrateur", "L'ampoule se tient, et le fil redevient beige."),
        ("narrateur", "Chouchou reste dans le jaune, le poignet libre."),
        ("narrateur", "Sous la lumière, la ficelle ne se tait plus."),
        ("papa", "Le jaune a rendu le fil."),
        ("enfant-m", "On peut tirer, un peu."),
        ("maman", "Tu as laissé l'ampoule revenir."),
    ),
    (3, 3, 2): L(
        ("enfant-m", "Je viens dans ton jaune."),
        ("narrateur", "Raphaël se glisse près d'elle, le fil entre eux."),
        ("narrateur", "Chouchou lui rend un bout, paume ouverte."),
        ("narrateur", "Dans le jaune, la ficelle n'a plus d'ombre."),
        ("papa", "Tu t'es mis dans son cercle."),
        ("enfant-m", "On tire ici."),
        ("maman", "Près d'elle, le fil suffisait."),
    ),
    (3, 3, 3): L(
        ("enfant-m", "Ton mot, pour la corde."),
        ("narrateur", "Raphaël attend, les lèvres fermées."),
        ("narrateur", "Chouchou ouvre la bouche, tout petit."),
        ("copine", "Corde."),
        ("narrateur", "La ficelle avance d'un pas, dans le jaune."),
        ("papa", "Elle a dit le mot, toute seule."),
        ("maman", "Le mot était tout bas, à elle."),
    ),
}


FINS = {
    (1, 1, 1): L(
        ("narrateur", "Le camion glisse, une pomme dessus, sans bruit."),
        ("enfant-m", "On a attendu les pommes."),
        ("papa", "Les pommes se sont tues, d'abord."),
        ("maman", "On remonte, la marche est froide."),
        ("narrateur", "Le grand carton garde un peu de poussière."),
        ("narrateur", "Une odeur de pomme suit l'escalier."),
    ),
    (1, 1, 2): L(
        ("narrateur", "Du bas du râtelier, le camion glisse, une pomme dessus."),
        ("enfant-m", "On s'est baissés."),
        ("papa", "Tu as vu le sol avant de pousser."),
        ("maman", "Essuie tes genoux, on remonte."),
        ("narrateur", "Le carton a un pli bas, près du sol."),
        ("narrateur", "Un grain de poussière retombe, puis plus rien."),
    ),
    (1, 1, 3): L(
        ("narrateur", "La pomme du doigt reste sur le camion."),
        ("enfant-m", "Elle a montré, et j'ai suivi."),
        ("papa", "Le doigt n'a pas bougé."),
        ("maman", "On remonte, le râtelier se tait."),
        ("narrateur", "Le carton porte une pomme choisie, pas deux."),
        ("narrateur", "Le râtelier se tait, derrière eux."),
    ),
    (1, 2, 1): L(
        ("narrateur", "Quand le bord a cédé, le camion a glissé."),
        ("enfant-m", "On a attendu la marche."),
        ("papa", "La marche n'a plus pincé."),
        ("maman", "Une pomme tient dessus, on remonte."),
        ("narrateur", "Le carton a une trace de pierre, au bord."),
        ("narrateur", "La marche garde une trace de carton."),
    ),
    (1, 2, 2): L(
        ("narrateur", "De côté, le camion passe, une pomme dessus."),
        ("enfant-m", "On a tourné."),
        ("papa", "Tu as tourné, sans forcer."),
        ("maman", "On remonte, la pierre est froide."),
        ("narrateur", "Le carton est de biais, plus mince."),
        ("narrateur", "Un coin de carton reste sur la pierre."),
    ),
    (1, 2, 3): L(
        ("narrateur", "Sa main a laissé le camion passer, une pomme dessus."),
        ("enfant-m", "On a poussé ensemble."),
        ("papa", "Sa main a guidé le bord."),
        ("maman", "On remonte, vos doigts sentent le carton."),
        ("narrateur", "Deux paumes ont laissé une poussière tiède."),
        ("narrateur", "La rampe de pierre reçoit leurs mains."),
    ),
    (1, 3, 1): L(
        ("narrateur", "Quand la lumière a tenu, le camion a glissé."),
        ("enfant-m", "On a attendu l'ampoule."),
        ("papa", "La lumière vous a aidés."),
        ("maman", "Une pomme brille dessus, on remonte."),
        ("narrateur", "Le carton a un rond jaune, pâle."),
        ("narrateur", "L'ampoule jaune tremble, toute seule."),
    ),
    (1, 3, 2): L(
        ("narrateur", "Dans le jaune, le camion glisse, une pomme dessus."),
        ("enfant-m", "On est restés près d'elle."),
        ("papa", "Tu t'es glissé, comme l'ombre."),
        ("maman", "On remonte, vos manches sentent la cave."),
        ("narrateur", "Le carton a quitté le cercle, sans le casser."),
        ("narrateur", "Un cercle de lumière pâlit au sol."),
    ),
    (1, 3, 3): L(
        ("narrateur", "Après son mot, le camion glisse, une pomme dessus."),
        ("enfant-m", "Elle a dit viens, tout bas."),
        ("papa", "Le mot était à elle."),
        ("maman", "On remonte, l'escalier sent la pomme."),
        ("narrateur", "Le carton avance comme si le mot tirait."),
        ("narrateur", "L'ombre de la cave reste en bas."),
    ),
    (2, 1, 1): L(
        ("narrateur", "Le camion part, une pomme sur le cercle jaune."),
        ("enfant-m", "On a laissé le crayon se taire."),
        ("papa", "La pomme a choisi le rond."),
        ("maman", "On remonte, le gras reste aux doigts."),
        ("narrateur", "Le crayon gras a laissé un trait jaune."),
        ("narrateur", "L'odeur des pommes reprend l'escalier."),
    ),
    (2, 1, 2): L(
        ("narrateur", "À ras de terre, le camion glisse, une pomme dessus."),
        ("enfant-m", "On s'est mis tout bas."),
        ("papa", "Tes genoux ont de la poussière jaune."),
        ("maman", "Essuie, on remonte."),
        ("narrateur", "Le crayon a un bout froid, trop près du sol."),
        ("narrateur", "Un grain jaune tombe de son pantalon."),
    ),
    (2, 1, 3): L(
        ("narrateur", "La pomme du doigt roule sur la roue dessinée."),
        ("enfant-m", "Elle a dit roue."),
        ("papa", "Le doigt et le trait se tenaient."),
        ("maman", "On remonte, le râtelier est vide d'une pomme."),
        ("narrateur", "Le crayon reste au centre du rond, un peu gras."),
        ("narrateur", "Derrière, le bois du râtelier ne bouge plus."),
    ),
    (2, 2, 1): L(
        ("narrateur", "Quand sa paume s'est levée, le camion a passé."),
        ("enfant-m", "On a laissé sa main."),
        ("papa", "La pierre n'a plus mordu le trait."),
        ("maman", "Une pomme tient, on remonte."),
        ("narrateur", "Le crayon a une petite étoile de pierre."),
        ("narrateur", "La marche garde un trait jaune, minuscule."),
    ),
    (2, 2, 2): L(
        ("narrateur", "De côté, le rond jaune passe, une pomme dessus."),
        ("enfant-m", "On a tourné le trait."),
        ("papa", "Le trait a trouvé un autre chemin."),
        ("maman", "On remonte, la pierre est froide."),
        ("narrateur", "Le crayon a un virage, comme une roue tournée."),
        ("narrateur", "Un trait jaune reste sur la pierre."),
    ),
    (2, 2, 3): L(
        ("narrateur", "Sa main a poussé le trait, et le camion a suivi."),
        ("enfant-m", "On a poussé la roue ensemble."),
        ("papa", "Sa main a guidé le crayon."),
        ("maman", "On remonte, vos doigts sentent le gras."),
        ("narrateur", "Deux traces jaunes, côte à côte, sur le carton."),
        ("narrateur", "La rampe reçoit une touche jaune, puis plus."),
    ),
    (2, 3, 1): L(
        ("narrateur", "Quand l'ampoule a tenu, le trait a repris."),
        ("enfant-m", "On a attendu le jaune."),
        ("papa", "Le jaune a rendu la roue."),
        ("maman", "Une pomme brille dessus, on remonte."),
        ("narrateur", "Le crayon a un bout plus clair, côté ampoule."),
        ("narrateur", "L'ampoule garde un halo gras, tout seul."),
    ),
    (2, 3, 2): L(
        ("narrateur", "Dans son rond, le camion glisse, une pomme dessus."),
        ("enfant-m", "On a dessiné ici."),
        ("papa", "Tu t'es mis dans son cercle."),
        ("maman", "On remonte, vos manches sentent le crayon."),
        ("narrateur", "Le crayon reste chaud, comme le jaune du sol."),
        ("narrateur", "Un cercle de lumière pâlit, avec un trait."),
    ),
    (2, 3, 3): L(
        ("narrateur", "Après le mot jaune, le camion glisse, une pomme dessus."),
        ("enfant-m", "Elle a dit jaune, tout bas."),
        ("papa", "Le mot était à elle."),
        ("maman", "On remonte, l'escalier sent la pomme."),
        ("narrateur", "Le crayon a écrit le mot, sans lettres."),
        ("narrateur", "L'ombre reste en bas, le jaune monte."),
    ),
    (3, 1, 1): L(
        ("narrateur", "Le camion part, une pomme contre le nœud."),
        ("enfant-m", "On a laissé le fil se reposer."),
        ("papa", "Le nœud a eu le temps."),
        ("maman", "On remonte, la marche est froide."),
        ("narrateur", "La ficelle pend, un peu tordue."),
        ("narrateur", "L'odeur des pommes tire l'escalier, comme un fil."),
    ),
    (3, 1, 2): L(
        ("narrateur", "À ras de terre, le fil tire le camion, une pomme dessus."),
        ("enfant-m", "On s'est mis tout bas."),
        ("papa", "Le nœud est plus lâche, plus doux."),
        ("maman", "Essuie tes genoux, on remonte."),
        ("narrateur", "La ficelle a un bout poussiéreux, trop près du sol."),
        ("narrateur", "Un brin beige reste sur la marche froide."),
    ),
    (3, 1, 3): L(
        ("narrateur", "La pomme du doigt tient grâce au fil."),
        ("enfant-m", "Elle a dit fil."),
        ("papa", "Le doigt a mené le nœud."),
        ("maman", "On remonte, le râtelier se tait."),
        ("narrateur", "La ficelle a un nœud plus rond, comme un doigt."),
        ("narrateur", "Derrière, plus aucune pomme ne roule."),
    ),
    (3, 2, 1): L(
        ("narrateur", "Quand le nœud s'est desserré, le camion a passé."),
        ("enfant-m", "On a laissé le fil."),
        ("papa", "La fente n'a plus mordu."),
        ("maman", "Une pomme tient, on remonte."),
        ("narrateur", "La ficelle a une ride, à l'endroit de la pierre."),
        ("narrateur", "La marche garde un fil perdu, minuscule."),
    ),
    (3, 2, 2): L(
        ("narrateur", "De côté, le fil passe, une pomme sur le camion."),
        ("enfant-m", "On a tourné la corde."),
        ("papa", "Le fil a trouvé un autre bord."),
        ("maman", "On remonte, la pierre est froide."),
        ("narrateur", "La ficelle est de biais, plus courte."),
        ("narrateur", "Un brin beige reste coincé, puis se libère."),
    ),
    (3, 2, 3): L(
        ("narrateur", "Sa main a poussé le nœud, et le camion a suivi."),
        ("enfant-m", "On a poussé la corde ensemble."),
        ("papa", "Sa main a guidé le nœud."),
        ("maman", "On remonte, vos doigts sentent le fil."),
        ("narrateur", "Deux paumes ont laissé le nœud tiède."),
        ("narrateur", "La ficelle traîne un instant, puis monte."),
    ),
    (3, 3, 1): L(
        ("narrateur", "Quand l'ampoule a tenu, le fil a repris sa couleur."),
        ("enfant-m", "On a attendu que ça brille."),
        ("papa", "Le jaune a rendu le fil."),
        ("maman", "Une pomme brille dessus, on remonte."),
        ("narrateur", "La ficelle a un bout plus clair, côté ampoule."),
        ("narrateur", "L'ampoule jaune tremble, un fil d'or autour."),
    ),
    (3, 3, 2): L(
        ("narrateur", "Dans son jaune, le camion glisse, une pomme dessus."),
        ("enfant-m", "On a tiré ici."),
        ("papa", "Tu t'es mis dans son cercle."),
        ("maman", "On remonte, vos manches sentent la cave."),
        ("narrateur", "La ficelle a quitté le poignet, sans se casser."),
        ("narrateur", "Un cercle de lumière pâlit, un fil au milieu."),
    ),
    (3, 3, 3): L(
        ("narrateur", "Après le mot corde, le camion glisse, une pomme dessus."),
        ("enfant-m", "Elle a dit corde, tout bas."),
        ("papa", "Le mot était à elle."),
        ("maman", "On remonte, l'escalier sent la pomme."),
        ("narrateur", "La ficelle avance comme si le mot tirait."),
        ("narrateur", "L'ombre de la cave reste en bas, le fil monte."),
    ),
}


T3_EMP = {
    1: {1: "pommes", 2: "bas", 3: "doigt"},
    2: {1: "bord", 2: "côté", 3: "main"},
    3: {1: "lumière", 2: "jaune", 3: "mot"},
}
FIN_EMP = {1: "carton", 2: "crayon", 3: "ficelle"}
FIN_SONS = {1: "pommes,escalier", 2: "pierre,escalier", 3: "ampoule,escalier"}


def build() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "pommes,escalier,carton", "emphasis": "camion"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"], T1Q, "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "le carton",
            "option_2_label": "le crayon",
            "option_3_label": "la ficelle",
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
                "engine_near_text": "Tu es tout près. Reprenons l'indice.",
            }},
        )
        by[f"{base}_C0001"] = voice(
            by_old[f"{base}_C0001"], t1["confirm"], "confirm",
            extra={"sons": "", "emphasis": t1["emphasis"]},
        )
        by[f"{base}_T0002_P0000"] = voice(
            by_old[f"{base}_T0002_P0000"], t2_question(a), "choice",
            extra={"sons": "", "fields": {
                "option_1_label": "le râtelier",
                "option_2_label": "la marche",
                "option_3_label": "l'ampoule",
            }},
        )
        for b in (1, 2, 3):
            p2 = f"{base}_T0002_P000{b}"
            by[p2] = voice(
                by_old[p2], t2_scene(a, b), "obstacle",
                extra={"sons": T2_SONS[b], "emphasis": T2_EMP[b]},
            )
            t3q = f"{p2}_T0003_P0000"
            by[t3q] = voice(
                by_old[t3q], t3_question(b), "choice",
                extra={"sons": "", "fields": {
                    "option_1_label": T3_LABS[b][0],
                    "option_2_label": T3_LABS[b][1],
                    "option_3_label": T3_LABS[b][2],
                }},
            )
            for c in (1, 2, 3):
                leaf = f"{p2}_T0003_P000{c}"
                by[leaf] = voice(
                    by_old[leaf], T3[(a, b, c)], "resolution",
                    extra={"sons": T2_SONS[b], "emphasis": T3_EMP[b][c]},
                )
                fin = f"{leaf}_F0001"
                by[fin] = voice(
                    by_old[fin], FINS[(a, b, c)], "ending",
                    extra={"sons": FIN_SONS[b], "emphasis": FIN_EMP[a]},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra_ids = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{SID} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    fins = [by[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(set(fins)) != 27:
        raise SystemExit(f"{SID} fins non distinctes: {len(set(fins))}/27")

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
            raise SystemExit(f"{SID} slogan/calque: {tic}")
    n_enc = len(re.findall(r"\bencore\b", blob))
    n_dej = len(re.findall(r"\bd[ée]jà\b", blob))
    if n_enc > 2 or n_dej > 2:
        raise SystemExit(f"{SID} tics encore={n_enc} déjà={n_dej}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "raphaël" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent")
    if "chouchou" not in blob:
        raise SystemExit(f"{SID}: Chouchou absente")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
        if not c.get("text_xai_tags") or c["text_xai_tags"] == c["text"]:
            raise SystemExit(f"{SID} {c['chunk_id']} TTS xai manquant")
        if not str(c.get("text_ssml") or "").startswith("<speak>"):
            raise SystemExit(f"{SID} {c['chunk_id']} SSML manquant")
        if "arc=" not in (c.get("notes") or ""):
            raise SystemExit(f"{SID} {c['chunk_id']} notes manquantes")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Vécu\n"
        "Cave sous la maison, odeur de pommes, ampoule jaune, carton qui racle. "
        "Raphaël veut un camion de carton pour descendre une pomme, avec Chouchou. "
        "Il lui demande le mot camion : elle tape, elle pousse, lèvres fermées. "
        "T1 = carton / crayon gras / ficelle (les trois partent). "
        "T2 = râtelier (deux envies : toutes les pommes / une pomme) / "
        "marche trop étroite (elle pose les mains, il pousse seul) / "
        "ampoule (elle reste dans le jaune, il veut l'ombre). "
        "T3 = neuf lectures (attendre, se baisser, suivre le doigt ; "
        "le bord, de côté, sa main ; la lumière, son ombre, son mot). "
        "Le silence de Chouchou compte : tape, doigt, paume, un mot à elle. "
        "Fin : le camion glisse, une pomme dessus, on remonte. "
        "Chaque fin paie une image du début (odeur, rampe, ampoule, poussière, fil, trait).\n\n"
        "## Vu et corrigé\n"
        "- Titre noyau conservé. N2 ≤ 15. Troupe D16 : Raphaël, Chouchou, papa, maman.\n"
        "- Leçon DIF.PAR.001 vécue, pas récitée. Pas « camarade qui parle peu ».\n"
        "- Première idée : « Dis camion » échoue. Les choix changent l'action.\n"
        "- 27 fins textuellement distinctes. Un merci vécu (rampe), pas un refrain Bravo.\n"
        "- Tics « tout doux / tout calme / encore / déjà » retirés (encore ≤ 2).\n"
        "- TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending).\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés. Pas apply.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(f"OK {SID} {nwords} mots  fins={len(set(fins))}")


if __name__ == "__main__":
    build()
