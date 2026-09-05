#!/usr/bin/env python3
"""TREE-DIF-052 — Le phare de coquillages de Mila (F-NAR-019, N1, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-052"
LIM = 10
TITLE = "Le phare de coquillages de Mila"
CHARS = "Mila, Sarah, papa, maman"
SETTING = "bord de mer : jetée, dune, écume, avant la marée"
FIL = (
    "Mila connaît la jetée. Un grain d'ambre brille sur un coquillage. "
    "Elle veut un phare de coquillages, allumé avant la marée. "
    "Sarah arrive : lunettes voilées, cheveux de sel, ciré trop long. "
    "Elle veut regarder, pas empiler tout de suite. "
    "T1 = clochette / seau bleu / pelle jaune, les trois partent. "
    "Première idée trop vite : la cloche sonne, le seau bascule, le sable vole. "
    "T2 = jetée (verres flous) / dune (mèches) / écume (manches). "
    "Un crabe vert emporte l'ambre. Mila veut courir. Sarah dit non. "
    "T3 : elles refusent de foncer, retrouvent le grain, posent la lanterne. "
    "Le phare tient. Ça a failli ne pas tenir."
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
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_grain_d_ambre_sera_la_lanterne; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_le_phare; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_porte; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
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
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_inquiétude; intensite=2; destinataire=enfant; sous_texte=le_crabe_prend_l_ambre_sarah_pose_sa_limite; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=elles_refusent_de_foncer_retrouvent_l_ambre; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_phare_tient_l_ambre_est_la_lanterne; tempo=posé; sourire=léger; respiration=ample",
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


OPENING = L(
    ("narrateur", "La jetée sent le sel, et le bois mouillé."),
    ("narrateur", "Une vague frappe loin, puis se tait."),
    ("narrateur", "Le vent pique le nez, un peu."),
    ("narrateur", "La marée est basse, pour un moment."),
    ("narrateur", "Mila connaît ce bord, pierre par pierre."),
    ("narrateur", "Un détail paraît neuf, près du sac."),
    ("narrateur", "Un grain d'ambre brille sur un coquillage."),
    ("papa", "Tu as vu ça, Mila ?"),
    ("enfant-f", "Ça brille, tout petit."),
    ("maman", "La clochette dort, près du seau bleu."),
    ("narrateur", "En ce moment, Mila la prend, froide."),
    ("enfant-f", "Je veux un phare, avant la marée."),
    ("narrateur", "Des pas sonnent sur le bois."),
    ("copine", "J'arrive, Mila."),
    ("narrateur", "Sarah s'arrête, sans un mot."),
    ("narrateur", "Ses lunettes gardent un rond d'eau."),
    ("enfant-f", "Tes cheveux sentent le sel."),
    ("narrateur", "Le ciré trop long cache ses poignets."),
    ("narrateur", "Un crabe vert traverse une planche."),
    ("copine", "Moi, je veux regarder."),
    ("papa", "Merci, tu as attendu sa voix."),
    ("maman", "On emporte les trois affaires, alors ?"),
)

T1 = {
    1: dict(
        name="la clochette",
        expected="main",
        accepted="main | la main | dans la main | sa main",
        retry="La cloche est dans la main.",
        ok="Oui, elle est dans la main.",
        sons="cloche,sac",
        emphasis="clochette",
        passage=L(
            ("narrateur", "Mila glisse la clochette dans sa main."),
            ("enfant-f", "Elle est froide, contre la peau."),
            ("narrateur", "Elle la secoue, trop vite."),
            ("narrateur", "Sarah recule, les lunettes qui tremblent."),
            ("enfant-f", "Pardon, je n'ai pas vu."),
            ("copine", "J'ai besoin d'un moment."),
            ("narrateur", "Mila serre la cloche, sans secouer."),
            ("maman", "Garde-la près de toi, sans secouer."),
            ("papa", "Le seau, ensuite, au bras."),
            ("narrateur", "Sarah prend la pelle, sous le bras."),
            ("narrateur", "Les trois affaires partent, vers la mer."),
            ("papa", "La cloche d'abord, vous l'avez."),
        ),
        question=L(
            ("narrateur", "La clochette est dans la main."),
            ("maman", "La cloche est où ?"),
        ),
        confirm=L(
            ("narrateur", "La main porte la cloche, contre le tissu."),
            ("copine", "Je vois le métal, un peu flou."),
            ("enfant-f", "C'est pour le phare."),
            ("narrateur", "Le grain d'ambre voyage dans le seau."),
            ("narrateur", "La marée pousse, loin."),
            ("maman", "Les coquillages vous attendent, plus loin."),
            ("papa", "On avance avec la cloche ?"),
            ("enfant-f", "Oui, papa."),
        ),
        choice=L(
            ("narrateur", "Dehors, l'eau brille, basse."),
            ("narrateur", "La marée pousse, loin."),
            ("narrateur", "Un chemin part sur la jetée."),
            ("narrateur", "Un autre grimpe la dune."),
            ("narrateur", "L'écume fait une petite île."),
            ("papa", "Quelle route, pour le phare ?"),
        ),
    ),
    2: dict(
        name="le seau bleu",
        expected="bras",
        accepted="bras | le bras | au bras | son bras",
        retry="Le seau est au bras.",
        ok="Oui, il est au bras.",
        sons="seau,plastique",
        emphasis="seau bleu",
        passage=L(
            ("narrateur", "Mila enroule le seau bleu au bras."),
            ("enfant-f", "Le bleu gratte un peu, contre le coude."),
            ("narrateur", "Elle penche trop, trop vite."),
            ("narrateur", "Deux coquillages tombent, toc toc."),
            ("copine", "Mes lunettes ont bougé."),
            ("narrateur", "Mila relève le seau, lentement."),
            ("enfant-f", "Je ralentis, promis."),
            ("papa", "Garde-le au bras, sans le vider."),
            ("maman", "La cloche, ensuite, dans la main."),
            ("narrateur", "Sarah prend la pelle, sous le bras."),
            ("narrateur", "Les trois affaires restent ensemble."),
            ("maman", "Le seau d'abord, il est prêt."),
        ),
        question=L(
            ("narrateur", "Le seau bleu est au bras."),
            ("maman", "Le seau est où ?"),
        ),
        confirm=L(
            ("narrateur", "Le bras porte le seau, contre la manche."),
            ("copine", "Ça gratte quand je marche."),
            ("enfant-f", "Ne le perds pas."),
            ("narrateur", "Une goutte tombe d'une mèche."),
            ("narrateur", "La marée pousse, loin."),
            ("papa", "Ça sent le sel, sur tes cheveux."),
            ("maman", "Vos mains, au-dessus du seau ?"),
            ("copine", "Oui, maman."),
        ),
        choice=L(
            ("narrateur", "Le seau cliquette, plein de coquillages."),
            ("narrateur", "La marée pousse, loin."),
            ("narrateur", "Un chemin part sur la jetée."),
            ("narrateur", "Un autre grimpe la dune."),
            ("narrateur", "L'écume fait une petite île."),
            ("maman", "Quelle route, pour le phare ?"),
        ),
    ),
    3: dict(
        name="la pelle jaune",
        expected="bras",
        accepted="bras | le bras | sous le bras | son bras",
        retry="La pelle est sous le bras.",
        ok="Oui, elle est sous le bras.",
        sons="bois,sable",
        emphasis="pelle jaune",
        passage=L(
            ("narrateur", "Mila glisse la pelle, sous le bras."),
            ("enfant-f", "Le bois sent le sac."),
            ("narrateur", "Elle creuse trop vite, un coup."),
            ("narrateur", "Le sable vole vers les lunettes."),
            ("copine", "Attends, je n'aime pas ça."),
            ("narrateur", "Mila baisse la pelle, contre sa hanche."),
            ("enfant-f", "Je m'arrête."),
            ("maman", "Serre-la sous le bras, tout droit."),
            ("papa", "La cloche et le seau, avec vous."),
            ("narrateur", "Il les pose près du sac."),
            ("narrateur", "Les trois affaires restent ensemble."),
            ("papa", "La pelle d'abord, elle est prête."),
        ),
        question=L(
            ("narrateur", "La pelle jaune est sous le bras."),
            ("maman", "La pelle est où ?"),
        ),
        confirm=L(
            ("narrateur", "Le bras porte la pelle, légère."),
            ("copine", "Elle a un grain de sable."),
            ("enfant-f", "On va creuser."),
            ("narrateur", "Le ciré de Sarah cache ses poignets."),
            ("narrateur", "La marée pousse, loin."),
            ("maman", "Le rocher attend, devant."),
            ("papa", "On y va, tous les quatre ?"),
            ("enfant-f", "Oui."),
        ),
        choice=L(
            ("narrateur", "La pelle racle un peu le sable."),
            ("narrateur", "La marée pousse, loin."),
            ("narrateur", "Un chemin part sur la jetée."),
            ("narrateur", "Un autre grimpe la dune."),
            ("narrateur", "L'écume fait une petite île."),
            ("papa", "Quelle route, pour le phare ?"),
        ),
    ),
}

T2_LABS = ("la jetée", "la dune", "l'écume")
T3_LABS = {
    1: ("le torchon de maman", "les mains de Sarah", "un pas hors des gouttes"),
    2: ("le bandeau de maman", "la serviette", "Sarah tient le seau"),
    3: ("les manches retroussées", "Mila tient la pelle", "maman noue les poignets"),
}


def t2_jete(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Mila pose la cloche au bord de la jetée.",
        2: "Mila pose le seau au bord de la jetée.",
        3: "Mila pose la pelle au bord de la jetée.",
    }[a]
    mishap = {
        1: "La cloche glisse, trop loin.",
        2: "Le seau vise trop bas, flou.",
        3: "La pelle part trop bas, floue.",
    }[a]
    objet = {1: "La cloche", 2: "Le seau", 3: "La pelle"}[a]
    crab = {
        1: "Un crabe vert saisit le coquillage d'ambre.",
        2: "Un crabe vert entre dans le seau.",
        3: "Un crabe vert passe sous la pelle.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-f", "Vite, on empile, Sarah !"),
        ("narrateur", "Le bois est mouillé, glissant."),
        ("copine", "Je vois un nuage sur mes lunettes."),
        ("narrateur", "Un rond d'eau cache les coquillages."),
        ("narrateur", mishap),
        ("enfant-f", f"{objet} n'attendait pas ça."),
        ("narrateur", "Le sourire de Mila disparaît."),
        ("papa", "Je m'accroupis, à votre hauteur."),
        ("narrateur", crab),
        ("enfant-f", "On court après lui !"),
        ("copine", "Attends, je ne cours pas."),
        ("papa", "Toi tu vois net, elle un peu flou."),
        ("maman", "Les coquillages sont flous, vous faites quoi ?"),
    )


def t2_dune(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Mila pose la cloche sur la dune.",
        2: "Mila pose le seau sur la dune.",
        3: "Mila pose la pelle sur la dune.",
    }[a]
    mishap = {
        1: "Une mèche collée couvre la cloche.",
        2: "Le seau accroche une mèche lourde.",
        3: "Une goutte de cheveu tombe sur la pelle.",
    }[a]
    crab = {
        1: "Un crabe vert emporte l'ambre, dans l'herbe.",
        2: "Un crabe vert tire l'ambre hors du seau.",
        3: "Un crabe vert pousse l'ambre sous la pelle.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-f", "Ici, le vent pousse, Sarah."),
        ("copine", "Mes cheveux sont trop lourds."),
        ("narrateur", mishap),
        ("narrateur", "Une goutte de sel tape le sable."),
        ("enfant-f", "On peut bâtir avec elle ?"),
        ("narrateur", "Dans sa poitrine, l'envie se bouscule."),
        ("maman", "Je m'accroupis, à votre hauteur."),
        ("narrateur", crab),
        ("enfant-f", "Vite, attrape-le !"),
        ("copine", "Non, je reste là."),
        ("papa", "Toi tes cheveux tiennent, les siens collent."),
        ("maman", "Les mèches tombent, vous faites quoi ?"),
    )


def t2_ecume(a: int) -> list[tuple[str, str]]:
    pose = {
        1: "Mila tend la cloche vers l'écume.",
        2: "Mila glisse le seau vers l'écume.",
        3: "Mila pose la pelle près de l'écume.",
    }[a]
    mishap = {
        1: "Une manche trop longue emporte la cloche.",
        2: "Une manche trop longue balaie le seau.",
        3: "Une manche trop longue cache la pelle.",
    }[a]
    objet = {1: "La cloche", 2: "Le seau", 3: "La pelle"}[a]
    crab = {
        1: "Un crabe vert fuit, l'ambre au bout.",
        2: "Un crabe vert nage, l'ambre avec lui.",
        3: "Un crabe vert cache l'ambre sous une vague.",
    }[a]
    return L(
        ("narrateur", pose),
        ("enfant-f", "Les coquillages sont notre phare, Sarah."),
        ("copine", "Mon ciré me suit jusqu'aux genoux !"),
        ("narrateur", mishap),
        ("narrateur", f"{objet} disparaît un instant, sous le tissu."),
        ("enfant-f", "Je n'aime pas ça."),
        ("narrateur", "L'inquiétude suit, juste derrière."),
        ("papa", "Je m'accroupis, à votre hauteur."),
        ("narrateur", crab),
        ("enfant-f", "On le rattrape, tout de suite !"),
        ("copine", "Moi, je ne rentre pas dans l'eau."),
        ("papa", "Toi tes manches s'arrêtent, les siennes voyagent."),
        ("maman", "Le ciré et les coquillages, vous faites comment ?"),
    )


T2_FN = {1: t2_jete, 2: t2_dune, 3: t2_ecume}
T2_SONS = {1: "bois,vague,crabe", 2: "vent,sable,crabe", 3: "ecume,ciré,crabe"}
T2_EMPH = {1: "lunettes", 2: "cheveux", 3: "ciré"}


def t3_choice(t2: int) -> list[tuple[str, str]]:
    if t2 == 1:
        return L(
            ("narrateur", "L'eau reste sur les verres, floue."),
            ("papa", "Le torchon, les mains, ou un pas dehors ?"),
        )
    if t2 == 2:
        return L(
            ("narrateur", "Une mèche touche un coquillage."),
            ("maman", "Le bandeau, la serviette, ou tenir le seau ?"),
        )
    return L(
        ("narrateur", "Les manches cachent les coquillages."),
        ("papa", "Les manches, la pelle, ou nouer les poignets ?"),
    )


def t3(a: int, b: int, c: int) -> list[tuple[str, str]]:
    o = {1: "la cloche", 2: "le seau", 3: "la pelle"}[a]
    cap = {1: "La cloche", 2: "Le seau", 3: "La pelle"}[a]
    key = (a, b, c)
    table = {
        (1, 1, 1): L(
            ("enfant-f", "Maman, le torchon, s'il te plaît."),
            ("maman", "Tiens, sur les verres, sans presser."),
            ("narrateur", "Sarah frotte un rond, puis un autre."),
            ("narrateur", "Mila veut courir, puis s'arrête."),
            ("enfant-f", "On ne fonce pas."),
            ("papa", "Personne ne dit où chercher."),
            ("narrateur", "Mila écoute le bois, puis le seau."),
            ("narrateur", "Le grain d'ambre brille, sous une pince."),
            ("copine", "Je vois le coquillage !"),
            ("enfant-f", "Le rose est à toi, maintenant."),
            ("narrateur", "Le crabe part vers l'eau, tout seul."),
            ("papa", "Vous bâtissez, chacune avec ce qu'elle a."),
        ),
        (1, 1, 2): L(
            ("enfant-f", "Tu bâtis avec tes mains, Sarah."),
            ("copine", "Je touche, toi tu dis où."),
            ("narrateur", "Sarah palpe la cloche, Mila parle."),
            ("narrateur", "Papa s'accroupit, à leur hauteur."),
            ("enfant-f", "À gauche, tout froid."),
            ("copine", "Je le tiens !"),
            ("narrateur", "Personne ne donne la réponse."),
            ("narrateur", "Le grain d'ambre chauffe la paume."),
            ("enfant-f", "On a trouvé, sans courir."),
            ("maman", "Les mains ont vu, à la place des verres."),
            ("narrateur", "La cloche guide le geste, au milieu."),
        ),
        (1, 1, 3): L(
            ("enfant-f", "On recule un peu, papa ?"),
            ("papa", "Un pas, hors des gouttes, pas plus."),
            ("narrateur", "L'air sec chasse l'eau, lent."),
            ("narrateur", "La cloche attend au bord, puis se pose."),
            ("copine", "Ça redevient clair !"),
            ("enfant-f", "On ne fonce pas vers le crabe."),
            ("narrateur", "Mila écoute la jetée, puis l'eau."),
            ("narrateur", "Le grain d'ambre clignote, sur le bois."),
            ("copine", "Je le vois, net."),
            ("maman", "Vous avez attendu le verre clair."),
            ("narrateur", "Le crabe lâche, et s'en va."),
        ),
        (1, 2, 1): L(
            ("enfant-f", "On met le bandeau, plus haut."),
            ("copine", "Mes cheveux restent en arrière, alors."),
            ("narrateur", "Maman noue le bandeau, sans serrer."),
            ("narrateur", "Mila pose la cloche, hors des mèches."),
            ("enfant-f", "Tu peux te pencher, maintenant."),
            ("copine", "Le vent ne m'attrape plus."),
            ("narrateur", "Mila refuse de courir derrière le crabe."),
            ("narrateur", "Le grain d'ambre brille, dans l'herbe."),
            ("copine", "Là, près du brin."),
            ("papa", "Chacune a sa hauteur, sur la dune."),
            ("narrateur", "La cloche sonne une fois, tout bas."),
        ),
        (1, 2, 2): L(
            ("enfant-f", "La serviette, maman ?"),
            ("maman", "Frotte, pas trop fort."),
            ("narrateur", "Sarah essuie une mèche, puis une autre."),
            ("narrateur", "La cloche attend, le temps d'un frottement."),
            ("copine", "Elles sont plus légères !"),
            ("enfant-f", "On pose la cloche, maintenant."),
            ("narrateur", "Mila cherche l'ambre, sans foncer."),
            ("narrateur", "Le grain d'ambre était dans une mèche."),
            ("copine", "Il brillait dans mes cheveux !"),
            ("papa", "Vous avez laissé l'eau des cheveux."),
            ("narrateur", "Le vent pousse, sans emporter de cheveu."),
        ),
        (1, 2, 3): L(
            ("enfant-f", "Tu tiens le seau, moi je pose."),
            ("copine", "Mes mains font le bord, alors."),
            ("narrateur", "Sarah tient le seau, Mila pose la cloche."),
            ("narrateur", "Les coquillages tombent quand Sarah recule."),
            ("narrateur", "Ils s'arrêtent quand elle avance."),
            ("enfant-f", "C'est toi le seau vivant, Sarah !"),
            ("copine", "Et toi les coquillages."),
            ("enfant-f", "On ne court pas après le crabe."),
            ("narrateur", "Le grain d'ambre reste au fond, au sec."),
            ("papa", "Vous bâtissez avec ce que vous avez."),
            ("maman", "Les cheveux n'ont plus besoin du vent."),
        ),
        (1, 3, 1): L(
            ("enfant-f", "On retrousse, Sarah."),
            ("copine", "Jusqu'au coude, comme papa."),
            ("narrateur", "Deux rouleaux de tissu tiennent, épais."),
            ("narrateur", "Les manches remontent, la cloche redevient libre."),
            ("enfant-f", "Je te vois les mains, maintenant."),
            ("copine", "Le coquillage n'est plus dans le ciré."),
            ("narrateur", "Mila s'arrête, au bord de l'écume."),
            ("narrateur", "Le grain d'ambre flotte, puis se pose."),
            ("copine", "On attend qu'il s'arrête."),
            ("papa", "Les manches ont laissé les coquillages passer."),
            ("narrateur", "La cloche reprend sa place, au milieu."),
        ),
        (1, 3, 2): L(
            ("enfant-f", "Moi je tiens la pelle."),
            ("copine", "Moi je guide, près de l'eau."),
            ("narrateur", "Mila tient la pelle, Sarah pose la cloche."),
            ("narrateur", "Les manches trop longues bougent le tissu, seulement."),
            ("narrateur", "Les coquillages restent hors du ciré."),
            ("copine", "L'écume s'ouvre !"),
            ("enfant-f", "On ne rentre pas dans l'eau."),
            ("narrateur", "Personne ne dit le geste."),
            ("narrateur", "Le grain d'ambre clignote, entre deux vagues."),
            ("papa", "Chacune a pris sa part, à sa taille."),
            ("maman", "L'eau a tenu les coquillages."),
        ),
        (1, 3, 3): L(
            ("enfant-f", "Maman, ton élastique, s'il te plaît."),
            ("maman", "Un pour chaque manche, sans trop serrer."),
            ("narrateur", "Sarah tend les poignets, maman noue."),
            ("narrateur", "L'élastique tient une manche, la cloche l'autre main."),
            ("copine", "Mes mains sont nues, maintenant."),
            ("enfant-f", "Les coquillages peuvent s'empiler."),
            ("narrateur", "Mila refuse de foncer dans l'écume."),
            ("narrateur", "Le grain d'ambre brille, au creux d'une pierre."),
            ("copine", "Je le prends, sans presser."),
            ("papa", "Vous avez demandé, et ça tient."),
            ("maman", "Mes élastiques ont gardé le ciré."),
        ),
        (2, 1, 1): L(
            ("enfant-f", "Maman, le torchon, pour ses verres."),
            ("maman", "Doucement, Sarah, un rond après l'autre."),
            ("narrateur", "Sarah frotte, le seau au bras."),
            ("narrateur", "Mila lève un pied, puis le repose."),
            ("enfant-f", "On ne court pas."),
            ("papa", "Regarde le seau, pas le crabe."),
            ("narrateur", "Mila écoute le plastique, puis le bois."),
            ("narrateur", "Le grain d'ambre tapote le fond, tic."),
            ("copine", "Il est là, au fond !"),
            ("enfant-f", "Le seau l'a gardé."),
            ("narrateur", "Le crabe sort, et laisse l'ambre."),
            ("maman", "Le torchon a rendu la jetée."),
        ),
        (2, 1, 2): L(
            ("enfant-f", "Tes mains voient, Sarah."),
            ("copine", "Je palpe le bord, tu parles."),
            ("narrateur", "Sarah palpe le seau, Mila parle."),
            ("narrateur", "Maman s'accroupit, à leur hauteur."),
            ("enfant-f", "Le froid, c'est l'ambre."),
            ("copine", "Je le sens !"),
            ("narrateur", "Personne ne donne la réponse."),
            ("narrateur", "Le grain d'ambre roule contre le pouce."),
            ("enfant-f", "Sans les verres, tu as trouvé."),
            ("papa", "Les mains ont vu, à la place des lunettes."),
            ("narrateur", "Le seau reste droit, au sec."),
        ),
        (2, 1, 3): L(
            ("enfant-f", "Un pas, hors des gouttes."),
            ("papa", "Pas plus, l'air sèche les verres."),
            ("narrateur", "Le seau craque un peu, puis s'apaise."),
            ("copine", "Ça redevient clair !"),
            ("enfant-f", "Les coquillages peuvent s'empiler."),
            ("narrateur", "Sarah ajuste ses lunettes, nettes."),
            ("narrateur", "Mila cherche l'ambre, sans foncer."),
            ("narrateur", "Le grain d'ambre brille, sur une planche sèche."),
            ("copine", "Je le vois, enfin."),
            ("maman", "Le pas en arrière a rendu les coquillages."),
            ("papa", "Vous avez laissé le temps aux lunettes."),
        ),
        (2, 2, 1): L(
            ("enfant-f", "Le bandeau, plus haut que les yeux."),
            ("copine", "Mes cheveux restent libres, alors."),
            ("narrateur", "Maman noue, Sarah penche le seau."),
            ("narrateur", "Mila tend le seau, hors des mèches."),
            ("enfant-f", "Tu peux te pencher, maintenant."),
            ("copine", "Le vent ne m'attrape plus."),
            ("narrateur", "Mila refuse de chasser le crabe."),
            ("narrateur", "Le grain d'ambre brille, collé au plastique."),
            ("copine", "Il est resté avec nous."),
            ("papa", "Chacune a sa hauteur, sous le vent."),
            ("narrateur", "Le seau bleu tient, sans une mèche."),
        ),
        (2, 2, 2): L(
            ("enfant-f", "La serviette, pour tes mèches."),
            ("maman", "Frotte, sans trop tirer."),
            ("narrateur", "Sarah essuie, le seau entre les genoux."),
            ("narrateur", "Le seau attend, le temps d'un frottement."),
            ("copine", "Elles sont plus légères !"),
            ("enfant-f", "On tend le seau, maintenant."),
            ("narrateur", "Mila observe le sable, pas le crabe."),
            ("narrateur", "Le grain d'ambre était sous une mèche salée."),
            ("copine", "Il brillait contre mon cou !"),
            ("papa", "Vous avez laissé l'eau des cheveux."),
            ("narrateur", "Le vent pousse, sans emporter de cheveu."),
        ),
        (2, 2, 3): L(
            ("enfant-f", "Tu tiens le seau à deux mains."),
            ("copine", "Sans me pencher, alors."),
            ("narrateur", "Sarah tient le seau à deux mains, sans se pencher."),
            ("narrateur", "Les coquillages restent dedans, cette fois."),
            ("enfant-f", "C'est toi le seau vivant !"),
            ("copine", "Et toi, tu poses."),
            ("narrateur", "Mila pose, sans courir."),
            ("narrateur", "Le grain d'ambre reste au fond, au chaud."),
            ("copine", "Je le garde, ici."),
            ("papa", "Vous bâtissez avec ce que vous avez."),
            ("maman", "Les cheveux n'ont plus besoin du vent."),
        ),
        (2, 3, 1): L(
            ("enfant-f", "On retrousse, jusqu'au coude."),
            ("copine", "Comme papa, deux rouleaux."),
            ("narrateur", "Deux rouleaux de tissu tiennent, épais."),
            ("narrateur", "Les manches remontent, le seau redevient visible."),
            ("enfant-f", "Je te vois les mains, maintenant."),
            ("copine", "Le coquillage n'est plus dans le ciré."),
            ("narrateur", "Mila s'arrête, le seau au bord."),
            ("narrateur", "Le grain d'ambre flotte, puis revient."),
            ("copine", "On attend qu'il s'arrête."),
            ("papa", "Les manches ont laissé les coquillages passer."),
            ("narrateur", "Le seau reprend sa place, au milieu."),
        ),
        (2, 3, 2): L(
            ("enfant-f", "Moi je tiens la pelle."),
            ("copine", "Moi je glisse un coquillage."),
            ("narrateur", "Mila tient la pelle, Sarah y glisse un coquillage."),
            ("narrateur", "Les manches trop longues bougent le tissu, seulement."),
            ("narrateur", "Les coquillages restent hors du ciré."),
            ("copine", "L'écume s'ouvre !"),
            ("enfant-f", "On ne rentre pas dans l'eau."),
            ("narrateur", "Personne ne dit le geste."),
            ("narrateur", "Le grain d'ambre clignote, contre l'anse."),
            ("papa", "Chacune a pris sa part, à sa taille."),
            ("maman", "L'eau a tenu les coquillages."),
        ),
        (2, 3, 3): L(
            ("enfant-f", "Maman, tes élastiques, pour ses manches."),
            ("maman", "Un pour chaque poignet, sans trop serrer."),
            ("narrateur", "Sarah tend les poignets, maman noue."),
            ("narrateur", "L'élastique tient une manche, le seau l'autre main."),
            ("copine", "Mes mains sont nues, maintenant."),
            ("enfant-f", "Les coquillages peuvent s'empiler."),
            ("narrateur", "Mila refuse de foncer dans l'écume."),
            ("narrateur", "Le grain d'ambre brille, au creux d'une pierre."),
            ("copine", "Je le prends, sans presser."),
            ("papa", "Vous avez demandé, et ça tient."),
            ("maman", "Mes élastiques ont gardé le ciré."),
        ),
        (3, 1, 1): L(
            ("enfant-f", "Le torchon, maman, pour ses verres."),
            ("maman", "Un rond, puis l'autre, Sarah."),
            ("narrateur", "Sarah frotte, Mila reprend le manche de la pelle."),
            ("narrateur", "Mila veut courir, puis s'arrête."),
            ("enfant-f", "On ne fonce pas."),
            ("papa", "La pelle peut montrer, sans chasser."),
            ("narrateur", "Mila pointe le bois, tout bas."),
            ("narrateur", "Le grain d'ambre brille, sous une pince."),
            ("copine", "Je vois le coquillage !"),
            ("enfant-f", "La pelle l'a montré."),
            ("narrateur", "Le crabe part vers l'eau, tout seul."),
            ("maman", "Le torchon a rendu la jetée."),
        ),
        (3, 1, 2): L(
            ("enfant-f", "Tes mains, Sarah, moi je parle."),
            ("copine", "Je palpe, tu dis où."),
            ("narrateur", "Sarah palpe la pelle, Mila parle."),
            ("narrateur", "Papa s'accroupit, à leur hauteur."),
            ("enfant-f", "Le froid, sous le bois."),
            ("copine", "Je le tiens !"),
            ("narrateur", "Personne ne donne la réponse."),
            ("narrateur", "Le grain d'ambre chauffe la paume."),
            ("enfant-f", "On a trouvé, sans courir."),
            ("maman", "Les mains ont vu, à la place des verres."),
            ("narrateur", "La pelle reste droite, au milieu."),
        ),
        (3, 1, 3): L(
            ("enfant-f", "Un pas, hors des gouttes."),
            ("papa", "L'air sèche, pas plus loin."),
            ("narrateur", "La pelle glisse, puis le bois se tait."),
            ("copine", "Ça redevient clair !"),
            ("enfant-f", "Les coquillages peuvent s'empiler."),
            ("narrateur", "Sarah ajuste ses lunettes, nettes."),
            ("narrateur", "Mila cherche l'ambre, sans foncer."),
            ("narrateur", "Le grain d'ambre clignote, sur le bois."),
            ("copine", "Je le vois, net."),
            ("maman", "Vous avez attendu le verre clair."),
            ("papa", "La pelle a marqué la planche sèche."),
        ),
        (3, 2, 1): L(
            ("enfant-f", "Le bandeau, plus haut."),
            ("copine", "Mes cheveux restent en arrière, alors."),
            ("narrateur", "Maman noue le bandeau, sans serrer."),
            ("narrateur", "Mila pose la pelle, hors des mèches."),
            ("enfant-f", "Tu peux te pencher, maintenant."),
            ("copine", "Le vent ne m'attrape plus."),
            ("narrateur", "Mila refuse de courir derrière le crabe."),
            ("narrateur", "Le grain d'ambre brille, dans l'herbe."),
            ("copine", "Là, près du brin."),
            ("papa", "Chacune a sa hauteur, sur la dune."),
            ("narrateur", "La pelle marque un cercle, dans le sable."),
        ),
        (3, 2, 2): L(
            ("enfant-f", "La serviette, maman ?"),
            ("maman", "Frotte, pas trop fort."),
            ("narrateur", "Sarah essuie une mèche, puis une autre."),
            ("narrateur", "La pelle attend, le temps d'un frottement."),
            ("copine", "Elles sont plus légères !"),
            ("enfant-f", "On pose la pelle, maintenant."),
            ("narrateur", "Mila cherche l'ambre, sans foncer."),
            ("narrateur", "Le grain d'ambre était dans une mèche."),
            ("copine", "Il brillait dans mes cheveux !"),
            ("papa", "Vous avez laissé l'eau des cheveux."),
            ("narrateur", "Le vent pousse, sans emporter de cheveu."),
        ),
        (3, 2, 3): L(
            ("enfant-f", "Tu tiens le seau, moi je pose la pelle."),
            ("copine", "Mes mains font le bord, alors."),
            ("narrateur", "Sarah tient le seau, Mila pose la pelle."),
            ("narrateur", "Les coquillages tombent quand Sarah recule."),
            ("narrateur", "Ils s'arrêtent quand elle avance."),
            ("enfant-f", "C'est toi le seau vivant, Sarah !"),
            ("copine", "Et toi la pelle."),
            ("enfant-f", "On ne court pas après le crabe."),
            ("narrateur", "Le grain d'ambre reste au fond, au sec."),
            ("papa", "Vous bâtissez avec ce que vous avez."),
            ("maman", "Les cheveux n'ont plus besoin du vent."),
        ),
        (3, 3, 1): L(
            ("enfant-f", "On retrousse, Sarah."),
            ("copine", "Jusqu'au coude, comme papa."),
            ("narrateur", "Deux rouleaux de tissu tiennent, épais."),
            ("narrateur", "Les manches remontent, la pelle redevient visible."),
            ("enfant-f", "Je te vois les mains, maintenant."),
            ("copine", "Le coquillage n'est plus dans le ciré."),
            ("narrateur", "Mila s'arrête, au bord de l'écume."),
            ("narrateur", "Le grain d'ambre flotte, puis se pose."),
            ("copine", "On attend qu'il s'arrête."),
            ("papa", "Les manches ont laissé les coquillages passer."),
            ("narrateur", "La pelle reprend sa place, au milieu."),
        ),
        (3, 3, 2): L(
            ("enfant-f", "Moi je tiens la pelle."),
            ("copine", "Moi j'ouvre le seau, près de l'eau."),
            ("narrateur", "Mila tient la pelle, Sarah ouvre le seau."),
            ("narrateur", "Les manches trop longues bougent le tissu, seulement."),
            ("narrateur", "Les coquillages restent hors du ciré."),
            ("copine", "L'écume s'ouvre !"),
            ("enfant-f", "On ne rentre pas dans l'eau."),
            ("narrateur", "Personne ne dit le geste."),
            ("narrateur", "Le grain d'ambre clignote, entre deux vagues."),
            ("papa", "Chacune a pris sa part, à sa taille."),
            ("maman", "L'eau a tenu les coquillages."),
        ),
        (3, 3, 3): L(
            ("enfant-f", "Maman, ton élastique, s'il te plaît."),
            ("maman", "Un pour chaque manche, sans trop serrer."),
            ("narrateur", "Sarah tend les poignets, maman noue."),
            ("narrateur", "L'élastique tient une manche, la pelle reste droite."),
            ("copine", "Mes mains sont nues, maintenant."),
            ("enfant-f", "Les coquillages peuvent s'empiler."),
            ("narrateur", "Mila refuse de foncer dans l'écume."),
            ("narrateur", "Le grain d'ambre brille, au creux d'une pierre."),
            ("copine", "Je le prends, sans presser."),
            ("papa", "Vous avez demandé, et ça tient."),
            ("maman", "Mes élastiques ont gardé le ciré."),
        ),
    }
    if key not in table:
        raise SystemExit(f"T3 manquant {key}")
    # keep cap/o used so unused-var linters stay quiet if a branch skips them
    _ = (o, cap)
    return table[key]


T3_SONS = {
    1: "torchon,verre",
    2: "mains,bois",
    3: "pas,air",
}
T3_SONS_DUNE = {1: "bandeau,vent", 2: "serviette,sel", 3: "seau,sable"}
T3_SONS_ECUME = {1: "manches,tissu", 2: "pelle,ecume", 3: "elastique,poignet"}
T3_EMPH = {
    1: {1: "torchon", 2: "mains", 3: "pas"},
    2: {1: "bandeau", 2: "serviette", 3: "seau"},
    3: {1: "manches", 2: "pelle", 3: "poignets"},
}


def t3_sons(b: int, c: int) -> str:
    if b == 1:
        return T3_SONS[c]
    if b == 2:
        return T3_SONS_DUNE[c]
    return T3_SONS_ECUME[c]


def fin(a: int, b: int, c: int) -> list[tuple[str, str]]:
    coda = {
        1: "La clochette rentre, salée.",
        2: "Le seau bleu sèche près de la porte.",
        3: "La pelle jaune retrouve le sac.",
    }[a]
    table = {
        (1, 1, 1): L(
            ("narrateur", "La jetée sent le torchon, tiède."),
            ("copine", "J'ai vu le coquillage, net."),
            ("enfant-f", "Tes lunettes ont trouvé le rose."),
            ("papa", "Vous avez bâti, chacune avec sa vue."),
            ("maman", "Le bois sèche, sous vos doigts."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre est la lanterne, en haut."),
            ("enfant-f", "Ça a failli ne pas tenir."),
            ("narrateur", "La jetée garde une odeur de lin."),
        ),
        (1, 1, 2): L(
            ("narrateur", "Sur le bois, l'air est un peu chaud."),
            ("enfant-f", "Tu as touché, moi j'ai dit où."),
            ("copine", "Mes mains ont vu le rose."),
            ("papa", "Les verres flous n'ont pas arrêté le phare."),
            ("maman", "La jetée se tait, enfin."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre chauffe la paume."),
            ("enfant-f", "À demain, le rocher."),
            ("narrateur", "Le rebord reste tiède, sous les doigts."),
        ),
        (1, 1, 3): L(
            ("narrateur", "Un filet d'air sec reste près du bois."),
            ("copine", "L'eau est partie, toute seule."),
            ("enfant-f", "On a attendu le verre clair."),
            ("maman", "Le pas en arrière a rendu les coquillages."),
            ("papa", "Vous avez laissé le temps aux lunettes."),
            ("narrateur", coda),
            ("narrateur", "Mila souffle sur le phare, léger."),
            ("copine", "L'ambre brille, en haut."),
            ("narrateur", "Un carré de bois reste clair, plus loin."),
        ),
        (1, 2, 1): L(
            ("narrateur", "La dune garde un peu d'ombre."),
            ("enfant-f", "Le bandeau était trop bas, d'abord."),
            ("copine", "Mes cheveux sont restés libres."),
            ("papa", "Chacune a eu sa hauteur, sous le vent."),
            ("maman", "Le sable sèche, autour du phare."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre tient dans l'herbe rase."),
            ("enfant-f", "On rentre, la dune reste."),
            ("narrateur", "Un brin d'herbe reprend sa place, bas."),
        ),
        (1, 2, 2): L(
            ("narrateur", "La serviette sent le sel, tiède."),
            ("copine", "Tu as frotté, sans tirer."),
            ("enfant-f", "Puis on a bâti, sans emporter de cheveu."),
            ("maman", "L'eau des cheveux s'en est allée."),
            ("papa", "La dune vous rend le silence."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre était dans une mèche."),
            ("copine", "Il reste, sur le phare."),
            ("narrateur", "Le sel quitte le sable, lent."),
        ),
        (1, 2, 3): L(
            ("narrateur", "Les mains de Sarah gardent le pli du seau."),
            ("enfant-f", "Tu étais le seau vivant."),
            ("copine", "Toi les coquillages, moi le bord."),
            ("papa", "Vous avez bâti avec ce que vous aviez."),
            ("maman", "Les cheveux n'avaient plus besoin d'être pris."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre dort au fond, puis en haut."),
            ("enfant-f", "On se dit au revoir, dune."),
            ("narrateur", "Les chaussons glissent vers la maison."),
        ),
        (1, 3, 1): L(
            ("narrateur", "Deux rouleaux de manches tiennent."),
            ("enfant-f", "Tes mains sont sorties du ciré."),
            ("copine", "Le coquillage n'était plus avalé."),
            ("papa", "Les manches ont laissé les coquillages passer."),
            ("maman", "L'écume redevient de l'eau, simple."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre veille, dans l'écume."),
            ("enfant-f", "On rentre, Sarah."),
            ("narrateur", "L'écume reprend sa forme, lente."),
        ),
        (1, 3, 2): L(
            ("narrateur", "Une goutte tombe d'une manche."),
            ("copine", "Tu tenais la pelle, moi le bord."),
            ("enfant-f", "Tes manches bougeaient seulement le tissu."),
            ("maman", "Chacune a pris sa part, à sa taille."),
            ("papa", "L'eau a tenu jusqu'au bout."),
            ("narrateur", coda),
            ("narrateur", "Mila lisse le phare, l'ambre en haut."),
            ("copine", "Il a bien tenu."),
            ("narrateur", "La vague reprend son silence, loin."),
        ),
        (1, 3, 3): L(
            ("narrateur", "Deux élastiques veillent aux poignets."),
            ("enfant-f", "On a demandé, et ça tenait."),
            ("copine", "Mes mains étaient nues, pour les coquillages."),
            ("papa", "Vous avez demandé, rien de plus."),
            ("maman", "Mes élastiques rentrent dans la poche."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre tient, salé, en haut."),
            ("enfant-f", "Les coquillages sont à nous."),
            ("narrateur", "La mer sent le vent, et le sel."),
        ),
        (2, 1, 1): L(
            ("narrateur", "La jetée sent le torchon, et le plastique."),
            ("copine", "Le seau a gardé l'ambre, au fond."),
            ("enfant-f", "Tes lunettes ont trouvé le tic."),
            ("papa", "Vous avez bâti, chacune avec sa vue."),
            ("maman", "Le bois sèche, sous l'anse."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre est la lanterne, posé du seau."),
            ("enfant-f", "Ça a failli rester au crabe."),
            ("narrateur", "Une goutte sèche sur le rebord, ronde."),
        ),
        (2, 1, 2): L(
            ("narrateur", "Sur le bois, le seau laisse un rond d'eau."),
            ("enfant-f", "Tu as palpé, moi j'ai dit froid."),
            ("copine", "Mes pouces ont vu le rose."),
            ("papa", "Les verres flous n'ont pas arrêté le phare."),
            ("maman", "La jetée se tait, autour de l'anse."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre garde la chaleur du pouce."),
            ("enfant-f", "À demain, le rocher."),
            ("narrateur", "Le plastique bleu reste tiède, un peu."),
        ),
        (2, 1, 3): L(
            ("narrateur", "Un filet d'air sec reste près du seau."),
            ("copine", "L'eau est partie des verres."),
            ("enfant-f", "On a attendu le verre clair."),
            ("maman", "Le pas en arrière a rendu les coquillages."),
            ("papa", "Vous avez laissé le temps aux lunettes."),
            ("narrateur", coda),
            ("narrateur", "Mila souffle sur le phare, du seau."),
            ("copine", "L'ambre brille, en haut."),
            ("narrateur", "La planche sèche garde un cercle bleu."),
        ),
        (2, 2, 1): L(
            ("narrateur", "La dune garde l'ombre du bandeau."),
            ("enfant-f", "Le bandeau était trop bas, d'abord."),
            ("copine", "Mes cheveux sont restés libres."),
            ("papa", "Chacune a eu sa hauteur, sous le vent."),
            ("maman", "Le sable sèche, autour du seau."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre tient, collé au bleu."),
            ("enfant-f", "On rentre, la dune reste."),
            ("narrateur", "Un brin d'herbe penche vers l'anse."),
        ),
        (2, 2, 2): L(
            ("narrateur", "La serviette sent le sel, et le bleu."),
            ("copine", "Tu as frotté, sans tirer."),
            ("enfant-f", "Puis on a bâti, sans emporter de cheveu."),
            ("maman", "L'eau des cheveux s'en est allée."),
            ("papa", "La dune vous rend le silence."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre a quitté la mèche."),
            ("copine", "Il reste, sur le phare."),
            ("narrateur", "Le sable garde un pli de serviette."),
        ),
        (2, 2, 3): L(
            ("narrateur", "Les mains de Sarah gardent le pli du seau."),
            ("enfant-f", "Tu étais le seau vivant."),
            ("copine", "Toi les coquillages, moi le bord."),
            ("papa", "Vous avez bâti avec ce que vous aviez."),
            ("maman", "Les cheveux n'avaient plus besoin d'être pris."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre monte du fond, en lanterne."),
            ("enfant-f", "On se dit au revoir, dune."),
            ("narrateur", "Deux empreintes restent, près du bleu."),
        ),
        (2, 3, 1): L(
            ("narrateur", "Deux rouleaux de manches tiennent, mouillés."),
            ("enfant-f", "Tes mains sont sorties du ciré."),
            ("copine", "Le coquillage n'était plus avalé."),
            ("papa", "Les manches ont laissé les coquillages passer."),
            ("maman", "L'écume redevient de l'eau, simple."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre veille, au bord du seau."),
            ("enfant-f", "On rentre, Sarah."),
            ("narrateur", "L'écume lèche l'anse, puis recule."),
        ),
        (2, 3, 2): L(
            ("narrateur", "Une goutte tombe d'une manche, dans le seau."),
            ("copine", "Tu tenais la pelle, moi le bord."),
            ("enfant-f", "Tes manches bougeaient seulement le tissu."),
            ("maman", "Chacune a pris sa part, à sa taille."),
            ("papa", "L'eau a tenu jusqu'au bout."),
            ("narrateur", coda),
            ("narrateur", "Mila lisse le phare, l'ambre du seau."),
            ("copine", "Il a bien tenu."),
            ("narrateur", "La vague laisse un sel blanc, sur le bleu."),
        ),
        (2, 3, 3): L(
            ("narrateur", "Deux élastiques veillent, près de l'anse."),
            ("enfant-f", "On a demandé, et ça tenait."),
            ("copine", "Mes mains étaient nues, pour les coquillages."),
            ("papa", "Vous avez demandé, rien de plus."),
            ("maman", "Mes élastiques rentrent dans la poche."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre tient, salé, en haut."),
            ("enfant-f", "Les coquillages sont à nous."),
            ("narrateur", "La mer sent le vent, et le plastique."),
        ),
        (3, 1, 1): L(
            ("narrateur", "La jetée sent le torchon, et le bois de pelle."),
            ("copine", "La pelle a montré l'ambre."),
            ("enfant-f", "Tes lunettes ont trouvé le rose."),
            ("papa", "Vous avez bâti, chacune avec sa vue."),
            ("maman", "Le bois sèche, sous le manche."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre est la lanterne, au bout."),
            ("enfant-f", "Ça a failli rester sous la pince."),
            ("narrateur", "Un trait de sable reste sur le manche."),
        ),
        (3, 1, 2): L(
            ("narrateur", "Sur le bois, la pelle laisse une rayure."),
            ("enfant-f", "Tu as palpé, moi j'ai dit froid."),
            ("copine", "Mes mains ont vu le rose."),
            ("papa", "Les verres flous n'ont pas arrêté le phare."),
            ("maman", "La jetée se tait, autour du manche."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre garde la chaleur du bois."),
            ("enfant-f", "À demain, le rocher."),
            ("narrateur", "Le manche jaune reste tiède, un peu."),
        ),
        (3, 1, 3): L(
            ("narrateur", "Un filet d'air sec reste près de la pelle."),
            ("copine", "L'eau est partie des verres."),
            ("enfant-f", "On a attendu le verre clair."),
            ("maman", "Le pas en arrière a rendu les coquillages."),
            ("papa", "Vous avez laissé le temps aux lunettes."),
            ("narrateur", coda),
            ("narrateur", "Mila souffle sur le phare, de la pelle."),
            ("copine", "L'ambre brille, en haut."),
            ("narrateur", "La planche sèche garde un trait jaune."),
        ),
        (3, 2, 1): L(
            ("narrateur", "La dune garde l'ombre de la pelle."),
            ("enfant-f", "Le bandeau était trop bas, d'abord."),
            ("copine", "Mes cheveux sont restés libres."),
            ("papa", "Chacune a eu sa hauteur, sous le vent."),
            ("maman", "Le sable sèche, autour du manche."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre tient dans un cercle de sable."),
            ("enfant-f", "On rentre, la dune reste."),
            ("narrateur", "Un brin d'herbe penche vers le bois jaune."),
        ),
        (3, 2, 2): L(
            ("narrateur", "La serviette sent le sel, et le bois."),
            ("copine", "Tu as frotté, sans tirer."),
            ("enfant-f", "Puis on a bâti, sans emporter de cheveu."),
            ("maman", "L'eau des cheveux s'en est allée."),
            ("papa", "La dune vous rend le silence."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre a quitté la mèche."),
            ("copine", "Il reste, sur le phare."),
            ("narrateur", "Le sable garde un ovale de serviette."),
        ),
        (3, 2, 3): L(
            ("narrateur", "Les mains de Sarah gardent le pli du seau."),
            ("enfant-f", "Tu étais le seau vivant."),
            ("copine", "Toi la pelle, moi le bord."),
            ("papa", "Vous avez bâti avec ce que vous aviez."),
            ("maman", "Les cheveux n'avaient plus besoin d'être pris."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre monte, guidé par le bois."),
            ("enfant-f", "On se dit au revoir, dune."),
            ("narrateur", "Deux empreintes restent, près du jaune."),
        ),
        (3, 3, 1): L(
            ("narrateur", "Deux rouleaux de manches tiennent, sablés."),
            ("enfant-f", "Tes mains sont sorties du ciré."),
            ("copine", "Le coquillage n'était plus avalé."),
            ("papa", "Les manches ont laissé les coquillages passer."),
            ("maman", "L'écume redevient de l'eau, simple."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre veille, au bout de la pelle."),
            ("enfant-f", "On rentre, Sarah."),
            ("narrateur", "L'écume lèche le bois jaune, puis recule."),
        ),
        (3, 3, 2): L(
            ("narrateur", "Une goutte tombe d'une manche, sur la pelle."),
            ("copine", "Tu tenais la pelle, moi le bord."),
            ("enfant-f", "Tes manches bougeaient seulement le tissu."),
            ("maman", "Chacune a pris sa part, à sa taille."),
            ("papa", "L'eau a tenu jusqu'au bout."),
            ("narrateur", coda),
            ("narrateur", "Mila lisse le phare, l'ambre du bois."),
            ("copine", "Il a bien tenu."),
            ("narrateur", "La vague laisse un sel blanc, sur le jaune."),
        ),
        (3, 3, 3): L(
            ("narrateur", "Deux élastiques veillent, près du manche."),
            ("enfant-f", "On a demandé, et ça tenait."),
            ("copine", "Mes mains étaient nues, pour les coquillages."),
            ("papa", "Vous avez demandé, rien de plus."),
            ("maman", "Mes élastiques rentrent dans la poche."),
            ("narrateur", coda),
            ("narrateur", "Le grain d'ambre tient, salé, en haut."),
            ("enfant-f", "Les coquillages sont à nous."),
            ("narrateur", "La mer sent le vent, et le bois mouillé."),
        ),
    }
    if (a, b, c) not in table:
        raise SystemExit(f"FIN manquante {(a, b, c)}")
    return table[(a, b, c)]


FIN_SONS = {
    1: "bois,vague-loin",
    2: "vent,sable",
    3: "ecume,silence",
}


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "vague,vent,cloche", "emphasis": "grain d'ambre"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Avant de sortir, trois affaires attendent."),
            ("narrateur", "La clochette, le seau bleu, la pelle jaune."),
            ("narrateur", "Le coquillage d'ambre attend, près du sac."),
            ("maman", "Tu prends quoi d'abord, Mila ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "la clochette",
            "option_2_label": "le seau bleu",
            "option_3_label": "la pelle jaune",
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
                    extra={"sons": t3_sons(b, c), "emphasis": T3_EMPH[b][c]},
                )
                fin_id = f"{leaf}_F0001"
                by[fin_id] = voice(
                    by_old[fin_id], fin(a, b, c), "ending",
                    extra={"sons": FIN_SONS[b], "emphasis": "grain d'ambre"},
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
    if n_enc > 2 or n_dej > 2:
        raise SystemExit(f"tics encore={n_enc} déjà={n_dej}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"en ce moment ×{blob.count('en ce moment')}")
    if "mila" not in blob:
        raise SystemExit("Mila absente")
    if "sarah" not in blob:
        raise SystemExit("Sarah absente")
    if "phare" not in blob or "coquillage" not in blob:
        raise SystemExit("phare/coquillages absents")
    if "grain d'ambre" not in blob:
        raise SystemExit("indice grain d'ambre absent")
    if "crabe" not in blob:
        raise SystemExit("crabe absent")
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
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "volet jaune",
        "tarte",
        "théâtre",
        "theatre",
        "marionnette",
        "lavoir",
        "groseille",
        "fil pâle",
        "maison de bois",
        "ancre minuscule",
        "étoile brune",
        "marque fine",
        "ombre-flèche",
        "bouton de nacre",
        "nœud de raphia",
        "pois ivoire",
        "grain de savon",
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

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Vécu\n"
        "Bord de mer, avant la marée : jetée mouillée, dune, écume. "
        "Mila connaît le bord ; un détail paraît neuf : un grain d'ambre "
        "sur un coquillage. Mission : construire et allumer un phare de "
        "coquillages avant la marée. Sarah arrive sans un mot, lunettes "
        "voilées, cheveux de sel, ciré trop long ; elle veut regarder, "
        "pas empiler tout de suite. Papa remercie Mila d'avoir attendu "
        "sa voix. T1 = clochette / seau bleu / pelle jaune (les trois "
        "partent ; première idée trop vite : cloche secouée, seau penché, "
        "sable vers les lunettes). T2 = jetée (verres flous) / dune "
        "(mèches) / écume (manches) : empiler trop vite échoue, un crabe "
        "vert emporte l'ambre, Mila veut courir, Sarah pose sa limite. "
        "T3 : torchon / mains / pas ; bandeau / serviette / seau tenu ; "
        "manches / pelle / poignets noués. Elles refusent de foncer, "
        "retrouvent le grain du début, posent la lanterne. 27 fins : le "
        "phare tient, l'objet porte une trace, ça a failli ne pas arriver. "
        "Leçon DIF.COR.003 vécue (jouer avec Sarah telle qu'elle est, "
        "deux rythmes, silence = réponse), jamais dite. Autre monde que "
        "TREE-DIF-010 (pas maison de bois, pas fil pâle).\n\n"
        "## Vu et corrigé\n"
        "- Titre noyau conservé. N1 ≤ 10. Troupe D16 : Mila, Sarah, papa, maman.\n"
        "- Indice unique inventé : grain d'ambre (pas ancre, étoile, fil pâle, "
        "marque fine, ombre-flèche, tache). Payé au climax.\n"
        "- Corps : sourire disparaît, envie/inquiétude dans la poitrine, "
        "adulte accroupi. 2e ruse (crabe + ambre), refuse de foncer.\n"
        "- 27 fins textuellement distinctes. Un merci vécu (attendre la voix "
        "de Sarah), pas un refrain Bravo.\n"
        "- TTS par chunk (profils opening/choice/clue/confirm/action/obstacle/"
        "resolution/ending). `slow` = choix, danger doux, émotion.\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés. Pas apply.\n"
        "- Tics « tout doux / tout calme / encore / déjà » écartés.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(f"OK {SID} {nwords} mots  fins={len(set(fins))}")


if __name__ == "__main__":
    main()
