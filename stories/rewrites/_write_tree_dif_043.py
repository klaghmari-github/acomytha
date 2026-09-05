#!/usr/bin/env python3
"""TREE-DIF-043 — Le pain de Nino et les deux canards (F-NAR-019, N1, TTS)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "TREE-DIF-043"
LIM = LIMITS["N1"]
TITLE = "Le pain de Nino et les deux canards"
FIL = (
    "Au parc du village, Nino veut porter le pain aux deux canards "
    "avant qu'ils partent. Un grain doré brille sur la croûte. "
    "Il prend d'abord le pain, la nappe ou le seau ; les trois partent. "
    "À la mare, au banc ou au kiosque, la première idée échoue. "
    "Il refuse de relancer. Le grain doré guide deux places. "
    "Les deux canards goûtent. Le grain reste."
)
CHARS = "Nino, papa, maman"
SETTING = "parc du village : mare, banc, kiosque"

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=500, sentence=260, energy="warm", contour="storytelling",
        noise=0.36, emphasis="grain doré",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le_grain_doré_et_les_deux_canards; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=900, sentence=330, energy="focused", contour="rising",
        noise=0.33, emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2,
        pause=700, sentence=320, energy="focused", contour="rising",
        noise=0.32, emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=450, sentence=280, energy="bright", contour="falling",
        noise=0.34, emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les_deux_attendent_une_place; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=420, sentence=250, energy="lively", contour="dynamic",
        noise=0.37, emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=il_prend_l_objet_et_les_trois_partent; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0,
        pause=700, sentence=320, energy="tense", contour="dynamic",
        noise=0.32, emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement; intensite=2; destinataire=enfant; sous_texte=un_seul_geste_ne_fait_pas_deux_places; tempo=suspendu; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=560, sentence=270, energy="bright", contour="falling",
        noise=0.35, emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=il_refuse_de_relancer_et_trouve_le_grain; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3,
        pause=900, sentence=340, energy="calm", contour="falling",
        noise=0.31, emphasis="grain doré",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_doré_paie_le_début; tempo=posé; sourire=léger; respiration=ample",
    ),
}

TICS = (
    "tout doux",
    "tout calme",
    "on va apprendre",
    "voici le geste",
    "l'histoire est finie",
    "bon travail",
    "bravo tu as",
    "la première",
    "la deuxième",
    "la troisième",
    "j'ai compris",
    "mission accomplie",
    "aujourd'hui",
    "merle",
    "miel",
    "grand-père",
    "maîtresse",
    "jardinier",
    "gardienne",
    "plus rond ou plus mince",
    "le corps n'est pas",
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
        "lab": "le pain",
        "ans": "pain",
        "acc": "pain | le pain | d'abord le pain | la croûte",
        "retry": "Nino a pris le pain, d'abord.",
        "emph": "pain",
        "sons": "pain,sac",
    },
    2: {
        "lab": "la nappe",
        "ans": "nappe",
        "acc": "nappe | la nappe | d'abord la nappe | le tissu",
        "retry": "Nino a pris la nappe, d'abord.",
        "emph": "nappe",
        "sons": "tissu,sac",
    },
    3: {
        "lab": "le seau",
        "ans": "seau",
        "acc": "seau | le seau | d'abord le seau | l'anse",
        "retry": "Nino a pris le seau, d'abord.",
        "emph": "seau",
        "sons": "seau,metal",
    },
}

T3_LABS = {
    1: ("le bord", "deux tas", "le pont"),
    2: ("l'herbe", "le pied", "la nappe"),
    3: ("les marches", "plus près", "l'ombre"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nino prend le pain, chaud contre la paume.",
            "enfant-m|Il sent le four.",
            "maman|Garde le grain doré, tu l'as vu.",
            "narrateur|La croûte casse un peu, entre ses doigts.",
            "enfant-m|Une miette tombe.",
            "papa|Dans le seau, Nino.",
            "narrateur|Il glisse un morceau dans le seau.",
            "narrateur|Puis il glisse la nappe sous le bras.",
            "enfant-m|Pain, nappe, seau.",
            "papa|Les trois partent avec toi.",
            "narrateur|Près du sac, plus rien n'attend.",
            "enfant-m|On va aux deux.",
            "maman|Les deux, oui.",
            "narrateur|Le grain doré tient, sur la croûte.",
            "narrateur|Nino presse le pain, impatient.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino prend la nappe, pliée, tiède.",
            "enfant-m|Elle sent l'herbe.",
            "papa|Déplie un coin, pour voir.",
            "narrateur|Le pain pose sa croûte au milieu.",
            "narrateur|Le grain doré brille, collé.",
            "maman|Le seau, dans l'autre main.",
            "narrateur|Le métal cliquette, vide.",
            "enfant-m|Nappe, pain, seau.",
            "papa|Les trois partent avec toi.",
            "narrateur|Le sac reste plat, sur l'herbe.",
            "enfant-m|On va aux deux.",
            "maman|Les deux, oui.",
            "narrateur|Un coin de nappe frotte son poignet.",
            "narrateur|Nino serre le tissu, impatient.",
        )
    return L(
        "narrateur|Nino saisit le seau, par l'anse.",
        "enfant-m|Il cliquette.",
        "maman|C'est pour porter, Nino.",
        "narrateur|Il y glisse un morceau de pain.",
        "narrateur|Le grain doré reste visible, au bord.",
        "papa|La nappe, sous le bras.",
        "narrateur|Le tissu chauffe son coude.",
        "enfant-m|Seau, pain, nappe.",
        "papa|Les trois partent avec toi.",
        "narrateur|Le sac reste plat, sur l'herbe.",
        "enfant-m|On va aux deux.",
        "maman|Les deux, oui.",
        "narrateur|Le seau tape sa jambe, à chaque pas.",
        "narrateur|Nino tient l'anse, impatient.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nino a pris le pain, d'abord.",
            "maman|Il a pris quoi, d'abord ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino a pris la nappe, d'abord.",
            "papa|Il a pris quoi, d'abord ?",
        )
    return L(
        "narrateur|Nino a pris le seau, d'abord.",
        "maman|Il a pris quoi, d'abord ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Le pain.",
            "papa|Oui, le pain.",
            "narrateur|Nino glisse la nappe sous le bras.",
            "maman|Le seau, je te le tends.",
            "enfant-m|Je le prends.",
            "narrateur|Les deux canards avancent, lents.",
            "papa|Ils viennent, les deux.",
            "enfant-m|On cherche l'endroit.",
            "narrateur|Le grain doré tient, au chaud.",
        )
    if t1 == 2:
        return L(
            "enfant-m|La nappe.",
            "maman|Oui, la nappe.",
            "narrateur|Il ramasse le pain, petit.",
            "papa|Le seau, dans l'autre main ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les deux canards tournent, près de l'eau.",
            "maman|Ils attendent, les deux.",
            "enfant-m|On va où, maintenant ?",
            "narrateur|Le grain doré brille, sur le tissu.",
        )
    return L(
        "enfant-m|Le seau.",
        "papa|Oui, le seau.",
        "narrateur|Maman lui passe le pain, tiède.",
        "maman|La nappe, sous le bras.",
        "enfant-m|Elle est là.",
        "narrateur|Les deux canards attendent l'eau.",
        "papa|On cherche l'endroit, Nino.",
        "enfant-m|On va à l'eau ?",
        "narrateur|Le grain doré tremble, au bord du seau.",
    )


def t2_question(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le pain chauffe sa paume, impatient.",
            "narrateur|Le grain doré tient, sur la croûte.",
            "papa|La mare, le banc, ou le kiosque ?",
        )
    if t1 == 2:
        return L(
            "narrateur|La nappe chauffe son poignet, pliée.",
            "narrateur|Le grain doré brille, au milieu.",
            "maman|La mare, le banc, ou le kiosque ?",
        )
    return L(
        "narrateur|Le seau tape sa jambe, à chaque pas.",
        "narrateur|Le grain doré tremble, au bord.",
        "papa|La mare, le banc, ou le kiosque ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    table = {
        (1, 1): L(
            "narrateur|Nino court vers la mare, le pain en avant.",
            "enfant-m|Pour vous deux !",
            "narrateur|Il lance un morceau, trop loin.",
            "narrateur|L'eau l'avale, d'un pli.",
            "enfant-m|Oh.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Le canard au ventre rond reste au bord.",
            "narrateur|Celui au cou mince part, léger.",
            "enfant-m|L'un reste, l'un part.",
            "papa|Ils n'ont pas la même place.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "maman|Le grain doré est resté sur ta croûte.",
            "papa|Tu fais quoi, avec les deux ?",
        ),
        (2, 1): L(
            "narrateur|Nino court vers la mare, la nappe ouverte.",
            "enfant-m|Une table, pour vous deux !",
            "narrateur|La nappe accroche l'herbe, puis lâche.",
            "narrateur|Un coin tombe dans l'eau, lourd.",
            "enfant-m|Elle est mouillée.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Le ventre rond recule, mouillé.",
            "narrateur|Le cou mince file, trop loin.",
            "enfant-m|Ils partent.",
            "maman|L'eau a pris le coin.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "papa|Le grain doré brille, au sec.",
            "maman|Tu fais quoi, avec les deux ?",
        ),
        (3, 1): L(
            "narrateur|Nino court vers la mare, le seau tendu.",
            "enfant-m|De l'eau, pour le pain !",
            "narrateur|Le seau penche, une miette tombe.",
            "narrateur|L'eau l'avale, d'un pli.",
            "enfant-m|Elle est partie.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Le ventre rond reste, loin du seau.",
            "narrateur|Le cou mince part, léger.",
            "enfant-m|Ça n'a pas tenu.",
            "papa|Le seau a penché, voilà.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "maman|Le grain doré tremble, au bord.",
            "papa|Tu fais quoi, avec les deux ?",
        ),
        (1, 2): L(
            "narrateur|Nino grimpe sur le banc, le pain haut.",
            "enfant-m|Le goûter, ici !",
            "narrateur|Des miettes tombent entre les planches.",
            "narrateur|Les fentes avalent le pain, net.",
            "enfant-m|Il tombe.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Le ventre rond bute, trop large.",
            "narrateur|Le cou mince glisse entre les planches.",
            "enfant-m|Ce n'est pas juste.",
            "papa|Le banc a des trous, voilà tout.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "maman|Le grain doré est resté dans ta main.",
            "maman|Tu les gardes comment, ensemble ?",
        ),
        (2, 2): L(
            "narrateur|Nino pose la nappe sur le banc, vite.",
            "enfant-m|Une table, ici !",
            "narrateur|La nappe glisse dans une fente, mince.",
            "narrateur|Un coin disparaît, entre les planches.",
            "enfant-m|Elle part.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Le ventre rond bute contre le bois.",
            "narrateur|Le cou mince passe dessous, léger.",
            "enfant-m|Ils ne montent pas.",
            "maman|Les planches sont trop ouvertes.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "papa|Le grain doré reste sur le tissu.",
            "papa|Tu les gardes comment, ensemble ?",
        ),
        (3, 2): L(
            "narrateur|Nino pose le seau sur le banc, d'un coup.",
            "enfant-m|Le goûter, ici !",
            "narrateur|Le seau cogne le bois, un toc.",
            "narrateur|Une miette fuit entre les planches.",
            "enfant-m|Elle tombe.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Le ventre rond bute, trop large.",
            "narrateur|Le cou mince glisse dessous, mince.",
            "enfant-m|Ils ne restent pas.",
            "papa|Le banc est trop haut, pour eux.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "maman|Le grain doré tremble, dans le seau.",
            "maman|Tu les gardes comment, ensemble ?",
        ),
        (1, 3): L(
            "narrateur|Nino monte au kiosque, le pain levé.",
            "enfant-m|Le goûter, là-haut !",
            "narrateur|Le pain sent le four, loin de l'eau.",
            "narrateur|Un vent passe, froid, sur les marches.",
            "enfant-m|Ils ne viennent pas.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Le ventre rond ne monte pas.",
            "narrateur|Le cou mince commence, puis recule.",
            "enfant-m|C'est trop loin.",
            "maman|Le kiosque est trop loin de l'eau.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "papa|Le grain doré brille, contre ta paume.",
            "papa|Tu les rassembles comment ?",
        ),
        (2, 3): L(
            "narrateur|Nino monte au kiosque, la nappe claquant.",
            "enfant-m|Une table, là-haut !",
            "narrateur|La nappe claque sur les marches, haute.",
            "narrateur|Un vent la soulève, puis la lâche.",
            "enfant-m|Elle s'envole.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Le ventre rond reste en bas.",
            "narrateur|Le cou mince commence, puis recule.",
            "enfant-m|Ils ne montent pas.",
            "papa|Trop haut, trop loin de l'eau.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "maman|Le grain doré tient, au milieu.",
            "maman|Tu les rassembles comment ?",
        ),
        (3, 3): L(
            "narrateur|Nino monte au kiosque, le seau à bout de bras.",
            "enfant-m|De l'eau, là-haut !",
            "narrateur|Le seau tape une marche, haute.",
            "narrateur|Un vent passe, froid, dans l'anse.",
            "enfant-m|Ils restent en bas.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Le ventre rond ne monte pas.",
            "narrateur|Le cou mince recule, vers l'eau.",
            "enfant-m|C'est trop loin.",
            "maman|Le kiosque est trop loin de l'eau.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "papa|Le grain doré tremble, dans le seau.",
            "papa|Tu les rassembles comment ?",
        ),
    }
    return table[(t1, t2)]


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Dans la mare, l'un reste, l'autre part.",
            "papa|Le bord, deux tas, ou le pont ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Sur le banc, les miettes tombent.",
            "maman|L'herbe, le pied, ou la nappe ?",
        )
    return L(
        "narrateur|Au kiosque, ils ne montent pas.",
        "papa|Les marches, plus près, ou l'ombre ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    table = {
        (1, 1, 1): L(
            "enfant-m|Le bord, pas l'eau.",
            "narrateur|Nino lève le pain, pour relancer.",
            "narrateur|L'eau monte d'un cran, soudain.",
            "enfant-m|Non.",
            "enfant-m|J'attends.",
            "narrateur|Il baisse le bras, sans relancer.",
            "narrateur|Il regarde le grain doré, collé.",
            "narrateur|Il écoute la mare, plate.",
            "enfant-m|Deux places, au bord.",
            "narrateur|Il pose deux morceaux, bas.",
            "narrateur|Le ventre rond s'approche, lent.",
            "narrateur|Le cou mince revient, aussi.",
            "papa|Deux places, Nino.",
            "maman|Ils goûtent, chacun.",
            "narrateur|Le grain doré reste entre les deux.",
        ),
        (1, 1, 2): L(
            "enfant-m|Deux tas, pour eux.",
            "narrateur|Nino casse le pain, trop vite.",
            "narrateur|Un tas glisse vers l'eau.",
            "enfant-m|J'arrête.",
            "narrateur|Il pose le pain.",
            "narrateur|Il souffle.",
            "narrateur|Le grain doré montre le milieu.",
            "enfant-m|Un tas ici.",
            "enfant-m|Un tas là.",
            "narrateur|Il fait deux tas, inégaux.",
            "narrateur|Le ventre rond prend le gros.",
            "narrateur|Le cou mince prend le petit.",
            "papa|Chacun a le sien.",
            "maman|Ils goûtent, chacun de leur côté.",
            "narrateur|Le grain doré brille, entre les tas.",
        ),
        (1, 1, 3): L(
            "enfant-m|Le pont, pour tous.",
            "narrateur|Une planche pourrit au bord, étroite.",
            "narrateur|Nino veut y courir.",
            "enfant-m|Non.",
            "enfant-m|Lentement.",
            "narrateur|Il pose la nappe sur le bois.",
            "narrateur|Le grain doré guide sa main.",
            "narrateur|Deux morceaux, sur le pont.",
            "narrateur|Le ventre rond monte, large.",
            "narrateur|Le cou mince monte, léger.",
            "papa|L'eau reste en dessous.",
            "maman|Ils se tiennent, les deux.",
            "narrateur|Le grain doré sèche, sur le bois.",
        ),
        (2, 1, 1): L(
            "enfant-m|Le bord, pas l'eau.",
            "narrateur|Nino veut jeter la nappe, ouverte.",
            "narrateur|L'eau lèche le coin, de nouveau.",
            "enfant-m|Je la retiens.",
            "narrateur|Il tire le tissu, sans foncer.",
            "narrateur|Il cherche le grain doré, au sec.",
            "enfant-m|Deux places, sur le bord.",
            "narrateur|Il étale la nappe, loin de l'eau.",
            "narrateur|Deux morceaux, chacun d'un côté.",
            "narrateur|Le ventre rond s'approche, lent.",
            "narrateur|Le cou mince revient, aussi.",
            "papa|Le tissu tient, au sec.",
            "maman|Ils goûtent, chacun.",
            "narrateur|Le grain doré reste, au milieu.",
        ),
        (2, 1, 2): L(
            "enfant-m|Deux tas, pour eux.",
            "narrateur|Nino veut tout mettre au même endroit.",
            "narrateur|Le ventre rond pousse le mince, net.",
            "enfant-m|J'arrête.",
            "narrateur|Il recule la nappe, il souffle.",
            "narrateur|Le grain doré sépare le tissu.",
            "enfant-m|Un tas ici.",
            "enfant-m|Un tas là.",
            "narrateur|Deux tas, sur la nappe, inégaux.",
            "narrateur|Le ventre rond prend le gros.",
            "narrateur|Le cou mince prend le petit.",
            "papa|Chacun a le sien.",
            "maman|La nappe les tient, au sec.",
            "narrateur|Le grain doré brille, entre les tas.",
        ),
        (2, 1, 3): L(
            "enfant-m|Le pont, pour tous.",
            "narrateur|Nino veut tendre la nappe, trop vite.",
            "narrateur|Un coin glisse vers l'eau, de nouveau.",
            "enfant-m|Lentement.",
            "narrateur|Il pose la nappe sur la planche.",
            "narrateur|Le grain doré guide le milieu.",
            "narrateur|Deux morceaux, au-dessus de l'eau.",
            "narrateur|Le ventre rond monte, large.",
            "narrateur|Le cou mince monte, léger.",
            "papa|Le tissu fait le pont.",
            "maman|Ils se tiennent, les deux.",
            "narrateur|Le grain doré sèche, sur le pont.",
        ),
        (3, 1, 1): L(
            "enfant-m|Le bord, pas l'eau.",
            "narrateur|Nino veut plonger le seau, d'un coup.",
            "narrateur|L'eau monte d'un cran, soudain.",
            "enfant-m|Non.",
            "enfant-m|J'attends.",
            "narrateur|Il pose le seau, sans pencher.",
            "narrateur|Il regarde le grain doré, au bord.",
            "enfant-m|Deux places, au bord.",
            "narrateur|Il sort deux morceaux, bas.",
            "narrateur|Le ventre rond s'approche, lent.",
            "narrateur|Le cou mince revient, aussi.",
            "papa|Le seau reste droit.",
            "maman|Ils goûtent, chacun.",
            "narrateur|Le grain doré tremble, au fond.",
        ),
        (3, 1, 2): L(
            "enfant-m|Deux tas, pour eux.",
            "narrateur|Nino verse le seau, trop vite.",
            "narrateur|Un morceau glisse vers l'eau.",
            "enfant-m|J'arrête.",
            "narrateur|Il pose le seau.",
            "narrateur|Il souffle.",
            "narrateur|Le grain doré montre le milieu.",
            "enfant-m|Un tas ici.",
            "enfant-m|Un tas là.",
            "narrateur|Deux tas, près du seau, inégaux.",
            "narrateur|Le ventre rond prend le gros.",
            "narrateur|Le cou mince prend le petit.",
            "papa|Chacun a le sien.",
            "maman|Le seau n'a plus penché.",
            "narrateur|Le grain doré brille, entre les tas.",
        ),
        (3, 1, 3): L(
            "enfant-m|Le pont, pour tous.",
            "narrateur|Nino veut poser le seau, d'un coup.",
            "narrateur|La planche penche, étroite.",
            "enfant-m|Lentement.",
            "narrateur|Il pose le seau au milieu, droit.",
            "narrateur|Le grain doré guide sa main.",
            "narrateur|Deux morceaux, de chaque côté.",
            "narrateur|Le ventre rond monte, large.",
            "narrateur|Le cou mince monte, léger.",
            "papa|Le seau tient le pont.",
            "maman|Ils se tiennent, les deux.",
            "narrateur|Le grain doré sèche, sur le bois.",
        ),
        (1, 2, 1): L(
            "enfant-m|L'herbe, comme une table.",
            "narrateur|Nino veut jeter du haut, trop vite.",
            "narrateur|Une fente avale une miette, nette.",
            "enfant-m|Pas d'ici.",
            "narrateur|Il descend, le pain contre lui.",
            "narrateur|Il cherche le grain doré, dans l'herbe.",
            "enfant-m|Deux places, en bas.",
            "narrateur|Il pose deux morceaux, dans l'herbe.",
            "narrateur|Le ventre rond s'assoit, large.",
            "narrateur|Le cou mince s'allonge, près de lui.",
            "papa|L'herbe a deux places.",
            "maman|Les miettes restent, cette fois.",
            "narrateur|Le grain doré penche, près du pain.",
        ),
        (1, 2, 2): L(
            "enfant-m|Le pied du banc.",
            "narrateur|Nino veut remplir les fentes, vite.",
            "narrateur|Les miettes tombent, de nouveau.",
            "enfant-m|J'arrête.",
            "narrateur|Il s'assoit au pied, le pain bas.",
            "narrateur|Le grain doré brille, contre le bois.",
            "enfant-m|Ici, sans tomber.",
            "narrateur|Il pose deux morceaux, au pied.",
            "narrateur|Le ventre rond reste, large.",
            "narrateur|Le cou mince reste, mince.",
            "papa|Le pied était assez large.",
            "maman|Ils tiennent, sans tomber.",
            "narrateur|Le grain doré tient, au pied.",
        ),
        (1, 2, 3): L(
            "enfant-m|La nappe, sur les fentes.",
            "narrateur|Nino veut cacher les trous, trop vite.",
            "narrateur|Un coin glisse dans une fente.",
            "enfant-m|Lentement.",
            "narrateur|Il étale la nappe, d'un geste large.",
            "narrateur|Le grain doré s'arrête, au milieu.",
            "narrateur|Deux places, sur le pain.",
            "narrateur|Le ventre rond s'approche, large.",
            "narrateur|Celui au cou mince s'approche.",
            "papa|Plus besoin des trous.",
            "maman|Tes mains ont tenu le tissu.",
            "narrateur|Le grain doré brille, sur la nappe.",
        ),
        (2, 2, 1): L(
            "enfant-m|L'herbe, comme une table.",
            "narrateur|Nino veut garder la nappe sur le banc.",
            "narrateur|Un coin disparaît, entre les planches.",
            "enfant-m|Pas là.",
            "narrateur|Il descend, la nappe contre lui.",
            "narrateur|Il cherche le grain doré, dans l'herbe.",
            "enfant-m|Deux places, en bas.",
            "narrateur|Il étale la nappe, dans l'herbe.",
            "narrateur|Le ventre rond s'assoit, large.",
            "narrateur|Le cou mince s'allonge, près de lui.",
            "papa|L'herbe a deux places.",
            "maman|Le tissu tient, cette fois.",
            "narrateur|Le grain doré penche, sur le tissu.",
        ),
        (2, 2, 2): L(
            "enfant-m|Le pied du banc.",
            "narrateur|Nino veut coincer la nappe, dans une fente.",
            "narrateur|Le tissu glisse, de nouveau.",
            "enfant-m|J'arrête.",
            "narrateur|Il glisse la nappe au pied, bas.",
            "narrateur|Le grain doré brille, contre le bois.",
            "enfant-m|Ici, sans tomber.",
            "narrateur|Deux morceaux, sur le tissu.",
            "narrateur|Le ventre rond reste, large.",
            "narrateur|Le cou mince reste, mince.",
            "papa|Le pied était assez large.",
            "maman|La nappe les abrite, au pied.",
            "narrateur|Le grain doré tient, au pied.",
        ),
        (2, 2, 3): L(
            "enfant-m|La nappe, sur les fentes.",
            "narrateur|Nino tire trop fort, d'un coup.",
            "narrateur|Un coin file vers une fente.",
            "enfant-m|Lentement.",
            "narrateur|Il étale la nappe, large, ferme.",
            "narrateur|Le grain doré s'arrête, au milieu.",
            "narrateur|Deux places, sur le tissu.",
            "narrateur|Le ventre rond s'approche, large.",
            "narrateur|Celui au cou mince s'approche.",
            "papa|Plus besoin des trous.",
            "maman|Tes mains ont tenu le tissu.",
            "narrateur|Le grain doré brille, sur la nappe.",
        ),
        (3, 2, 1): L(
            "enfant-m|L'herbe, comme une table.",
            "narrateur|Nino veut garder le seau sur le banc.",
            "narrateur|Une miette fuit, entre les planches.",
            "enfant-m|Pas d'ici.",
            "narrateur|Il descend, le seau contre lui.",
            "narrateur|Il cherche le grain doré, dans l'herbe.",
            "enfant-m|Deux places, en bas.",
            "narrateur|Il pose le seau, dans l'herbe.",
            "narrateur|Le ventre rond s'assoit, large.",
            "narrateur|Le cou mince s'allonge, près de lui.",
            "papa|L'herbe a deux places.",
            "maman|Le seau reste droit, cette fois.",
            "narrateur|Le grain doré penche, au bord du seau.",
        ),
        (3, 2, 2): L(
            "enfant-m|Le pied du banc.",
            "narrateur|Nino veut coincer le seau, dans une fente.",
            "narrateur|Le métal cogne, de nouveau.",
            "enfant-m|J'arrête.",
            "narrateur|Il pose le seau au pied, bas.",
            "narrateur|Le grain doré brille, contre le bois.",
            "enfant-m|Ici, sans tomber.",
            "narrateur|Deux morceaux, près du seau.",
            "narrateur|Le ventre rond reste, large.",
            "narrateur|Le cou mince reste, mince.",
            "papa|Le pied était assez large.",
            "maman|Le seau tient, sans cogner.",
            "narrateur|Le grain doré tient, au pied.",
        ),
        (3, 2, 3): L(
            "enfant-m|La nappe, sur les fentes.",
            "narrateur|Nino veut poser le seau, d'abord.",
            "narrateur|Une miette fuit, avant le tissu.",
            "enfant-m|La nappe, d'abord.",
            "narrateur|Il étale la nappe, puis le seau.",
            "narrateur|Le grain doré s'arrête, au milieu.",
            "narrateur|Deux places, sur le tissu.",
            "narrateur|Le ventre rond s'approche, large.",
            "narrateur|Celui au cou mince s'approche.",
            "papa|Plus besoin des trous.",
            "maman|Le seau pose sa place, dessus.",
            "narrateur|Le grain doré brille, sous le seau.",
        ),
        (1, 3, 1): L(
            "enfant-m|Les marches, pour tous.",
            "narrateur|Nino veut monter plus haut, d'un élan.",
            "narrateur|Le cou mince recule, vers l'eau.",
            "enfant-m|Pas là-haut.",
            "narrateur|Il redescend, le pain contre lui.",
            "narrateur|Il cherche le grain doré, sur la marche.",
            "enfant-m|La marche basse, pour vous.",
            "narrateur|Il pose deux morceaux, sur la marche.",
            "narrateur|Le ventre rond tient, large.",
            "narrateur|Le cou mince tient, une patte dans le vide.",
            "papa|La marche a deux places, maintenant.",
            "maman|Plus besoin de monter.",
            "narrateur|Le grain doré reste, sur la marche.",
        ),
        (1, 3, 2): L(
            "enfant-m|Plus près, vers l'eau.",
            "narrateur|Nino reste sur les marches, le pain levé.",
            "narrateur|Les deux canards reculent, de nouveau.",
            "enfant-m|Je viens vers vous.",
            "narrateur|Il descend, sans courir.",
            "narrateur|Le grain doré brille, près de l'eau.",
            "enfant-m|Le goûter, plus près.",
            "narrateur|Il pose deux morceaux, près de l'eau.",
            "narrateur|Les deux canards avancent, lents.",
            "papa|Rentrer vers l'eau, c'était mieux.",
            "maman|L'un près de l'autre.",
            "narrateur|Le grain doré sèche, près de l'eau.",
        ),
        (1, 3, 3): L(
            "enfant-m|Sous l'ombre, plus frais.",
            "narrateur|Nino reste au soleil, le pain chaud.",
            "narrateur|Le ventre rond cligne, puis recule.",
            "enfant-m|L'ombre, alors.",
            "narrateur|Il entre sous le kiosque, lent.",
            "narrateur|Le grain doré ne brûle plus.",
            "enfant-m|Vous avez la place, à l'abri.",
            "narrateur|Deux morceaux, dans l'ombre.",
            "narrateur|Le ventre rond s'approche, large.",
            "narrateur|Celui au cou mince s'approche.",
            "papa|L'ombre était plus fraîche.",
            "maman|Le vent reste dehors, sur les marches.",
            "narrateur|Le grain doré tient, à l'ombre.",
        ),
        (2, 3, 1): L(
            "enfant-m|Les marches, pour tous.",
            "narrateur|Nino veut tendre la nappe, tout en haut.",
            "narrateur|Le vent la soulève, de nouveau.",
            "enfant-m|Pas là-haut.",
            "narrateur|Il redescend, la nappe contre lui.",
            "narrateur|Il cherche le grain doré, sur la marche.",
            "enfant-m|La marche basse, pour vous.",
            "narrateur|Il pose la nappe, sur la marche.",
            "narrateur|Le ventre rond tient, large.",
            "narrateur|Le cou mince tient, une patte dans le vide.",
            "papa|La marche a deux places, maintenant.",
            "maman|Le vent n'a plus pris le tissu.",
            "narrateur|Le grain doré reste, sur la nappe.",
        ),
        (2, 3, 2): L(
            "enfant-m|Plus près, vers l'eau.",
            "narrateur|Nino reste haut, la nappe claquant.",
            "narrateur|Les deux canards reculent, de nouveau.",
            "enfant-m|Je viens vers vous.",
            "narrateur|Il descend, sans courir.",
            "narrateur|Le grain doré brille, près de l'eau.",
            "enfant-m|Le goûter, plus près.",
            "narrateur|Il étale la nappe, près de l'eau.",
            "narrateur|Les deux canards avancent, lents.",
            "papa|Rentrer vers l'eau, c'était mieux.",
            "maman|La nappe sent l'eau, un peu.",
            "narrateur|Le grain doré sèche, près de l'eau.",
        ),
        (2, 3, 3): L(
            "enfant-m|Sous l'ombre, plus frais.",
            "narrateur|Nino reste au soleil, la nappe chaude.",
            "narrateur|Le ventre rond cligne, puis recule.",
            "enfant-m|L'ombre, alors.",
            "narrateur|Il entre sous le kiosque, lent.",
            "narrateur|Le grain doré ne brûle plus.",
            "enfant-m|Vous avez la place, à l'abri.",
            "narrateur|Il étale la nappe, dans l'ombre.",
            "narrateur|Le ventre rond s'approche, large.",
            "narrateur|Celui au cou mince s'approche.",
            "papa|L'ombre était plus fraîche.",
            "maman|Le vent reste dehors, sur les marches.",
            "narrateur|Le grain doré tient, sur la nappe.",
        ),
        (3, 3, 1): L(
            "enfant-m|Les marches, pour tous.",
            "narrateur|Nino veut monter le seau, d'un élan.",
            "narrateur|Le métal tape, de nouveau.",
            "enfant-m|Pas là-haut.",
            "narrateur|Il redescend, le seau contre lui.",
            "narrateur|Il cherche le grain doré, sur la marche.",
            "enfant-m|La marche basse, pour vous.",
            "narrateur|Il pose le seau, sur la marche.",
            "narrateur|Le ventre rond tient, large.",
            "narrateur|Le cou mince tient, une patte dans le vide.",
            "papa|La marche a deux places, maintenant.",
            "maman|Le seau n'a plus tapé.",
            "narrateur|Le grain doré reste, dans le seau.",
        ),
        (3, 3, 2): L(
            "enfant-m|Plus près, vers l'eau.",
            "narrateur|Nino reste haut, le seau levé.",
            "narrateur|Les deux canards reculent, de nouveau.",
            "enfant-m|Je viens vers vous.",
            "narrateur|Il descend, sans courir.",
            "narrateur|Le grain doré brille, près de l'eau.",
            "enfant-m|Le goûter, plus près.",
            "narrateur|Il pose le seau, près de l'eau.",
            "narrateur|Les deux canards avancent, lents.",
            "papa|Rentrer vers l'eau, c'était mieux.",
            "maman|Une goutte tremble, au bord.",
            "narrateur|Le grain doré sèche, près de l'eau.",
        ),
        (3, 3, 3): L(
            "enfant-m|Sous l'ombre, plus frais.",
            "narrateur|Nino reste au soleil, le seau chaud.",
            "narrateur|Le ventre rond cligne, puis recule.",
            "enfant-m|L'ombre, alors.",
            "narrateur|Il entre sous le kiosque, lent.",
            "narrateur|Le grain doré ne brûle plus.",
            "enfant-m|Vous avez la place, à l'abri.",
            "narrateur|Il pose le seau, dans l'ombre.",
            "narrateur|Le ventre rond s'approche, large.",
            "narrateur|Celui au cou mince s'approche.",
            "papa|L'ombre était plus fraîche.",
            "maman|Le vent reste dehors, sur les marches.",
            "narrateur|Le grain doré tient, dans le seau.",
        ),
    }
    return table[(t1, t2, t3)]


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    table = {
        (1, 1, 1): L(
            "narrateur|Le cou mince avait tourné, vers le chemin.",
            "narrateur|Il revient, à la dernière miette.",
            "enfant-m|Vous avez eu votre pain.",
            "papa|Tes mains ont fait les deux places.",
            "maman|Ils sont ensemble, quand même.",
            "narrateur|Deux ronds d'eau restent au bord.",
            "enfant-m|On reste un peu.",
            "narrateur|Le grain doré reste au bord, collé au pain.",
        ),
        (1, 1, 2): L(
            "narrateur|Un tas avait glissé, presque perdu.",
            "narrateur|Nino l'a retenu, au dernier moment.",
            "enfant-m|Vous teniez, tous les deux.",
            "papa|La mare les a tenus.",
            "maman|Ils ont mangé, chacun.",
            "narrateur|Nino souffle sur une miette, légère.",
            "enfant-m|On rentre, maintenant.",
            "narrateur|Entre deux tas, le grain doré brille, petit.",
        ),
        (1, 1, 3): L(
            "narrateur|La planche avait penché, presque.",
            "narrateur|Le pont a tenu, grâce à la nappe.",
            "enfant-m|Un goûter, plus large.",
            "papa|L'eau n'a plus gagné.",
            "maman|Tes mains ont mis le pont.",
            "narrateur|Il pose une miette, puis une autre.",
            "enfant-m|Une dernière, pour rire.",
            "narrateur|Sur le bois du pont, le grain doré sèche.",
        ),
        (1, 2, 1): L(
            "narrateur|Du haut, le pain allait tomber, trop.",
            "narrateur|L'herbe l'a reçu, à temps.",
            "enfant-m|On a goûté ici, sans tomber.",
            "papa|L'herbe avait deux places.",
            "maman|Plus besoin des fentes.",
            "narrateur|Le mince pointe le ciel, un instant.",
            "enfant-m|On reste un peu.",
            "narrateur|L'herbe tient le grain doré, près du pain.",
        ),
        (1, 2, 2): L(
            "narrateur|Une miette avait fuité, presque.",
            "narrateur|Le pied du banc l'a arrêtée.",
            "enfant-m|Vous teniez, sans tomber.",
            "papa|Le pied était assez large.",
            "maman|Deux silhouettes, un même pain.",
            "narrateur|Le mince a une miette sur le bec.",
            "enfant-m|Le dîner, après ?",
            "narrateur|Au pied du banc, une miette garde le grain.",
        ),
        (1, 2, 3): L(
            "narrateur|Un coin de nappe avait glissé, presque.",
            "narrateur|Les mains de Nino l'ont retenu.",
            "enfant-m|Vous avez eu le pain.",
            "papa|Plus besoin des trous.",
            "maman|Tes mains ont tenu le tissu.",
            "narrateur|Il les regarde, l'un contre l'autre.",
            "enfant-m|On est arrivés.",
            "narrateur|La nappe pliée cache le grain doré, tiède.",
        ),
        (1, 3, 1): L(
            "narrateur|Le cou mince avait reculé, vers l'eau.",
            "narrateur|La marche basse l'a fait revenir.",
            "enfant-m|Vous aviez les marches.",
            "papa|La marche avait deux places.",
            "maman|Plus besoin de monter.",
            "narrateur|Nino lisse une miette, un dernier coup.",
            "enfant-m|On reste un peu.",
            "narrateur|La marche basse porte le grain, près du pain.",
        ),
        (1, 3, 2): L(
            "narrateur|Là-haut, le pain allait refroidir, seul.",
            "narrateur|Plus près, les deux sont venus.",
            "enfant-m|Vous aviez le goûter, plus près.",
            "papa|Rentrer vers l'eau, c'était mieux.",
            "maman|L'un près de l'autre.",
            "narrateur|Le rond et le mince se touchent, un peu.",
            "enfant-m|Le goûter est fini, pour de vrai.",
            "narrateur|Près de l'eau, le pain garde son grain doré.",
        ),
        (1, 3, 3): L(
            "narrateur|Au soleil, le ventre rond allait partir.",
            "narrateur|L'ombre l'a retenu, à temps.",
            "enfant-m|Vous aviez la place, à l'abri.",
            "papa|L'ombre était plus fraîche.",
            "maman|Le vent est resté dehors.",
            "narrateur|Un bec rond, un bec mince, près du pain.",
            "enfant-m|On rentre, maintenant.",
            "narrateur|Sous l'ombre, le grain doré ne brûle plus.",
        ),
        (2, 1, 1): L(
            "narrateur|Le coin mouillé avait failli tout prendre.",
            "narrateur|Nino a tiré, à temps.",
            "enfant-m|Vous avez eu votre pain.",
            "papa|Le tissu a tenu, au sec.",
            "maman|Ils sont ensemble, quand même.",
            "narrateur|Deux ronds d'eau restent, loin du tissu.",
            "enfant-m|On reste un peu.",
            "narrateur|Un coin de nappe sèche, le grain collé.",
        ),
        (2, 1, 2): L(
            "narrateur|Le ventre rond avait poussé, presque trop.",
            "narrateur|Deux tas ont calmé ça.",
            "enfant-m|Vous teniez, tous les deux.",
            "papa|Chacun a eu le sien.",
            "maman|La nappe les a tenus.",
            "narrateur|Nino lisse un pli, léger.",
            "enfant-m|On rentre, maintenant.",
            "narrateur|Deux tas sur la nappe, le grain au centre.",
        ),
        (2, 1, 3): L(
            "narrateur|Le coin avait glissé, presque dans l'eau.",
            "narrateur|Le pont de tissu a tenu.",
            "enfant-m|Un goûter, plus large.",
            "papa|L'eau n'a plus gagné.",
            "maman|Tes mains ont tendu le pont.",
            "narrateur|Une feuille s'arrête sur le bois, puis plus.",
            "enfant-m|Une miette, pour rire.",
            "narrateur|Le pont de nappe garde le grain, au sec.",
        ),
        (2, 2, 1): L(
            "narrateur|Sur le banc, le tissu allait disparaître.",
            "narrateur|L'herbe l'a reçu, à temps.",
            "enfant-m|On a goûté ici, sans tomber.",
            "papa|L'herbe avait deux places.",
            "maman|Le tissu tient, maintenant.",
            "narrateur|Le mince pointe le ciel, un instant.",
            "enfant-m|On reste un peu.",
            "narrateur|L'herbe froisse la nappe, le grain penche.",
        ),
        (2, 2, 2): L(
            "narrateur|Une fente avait pris un coin, presque.",
            "narrateur|Le pied du banc a tout arrêté.",
            "enfant-m|Vous teniez, sans tomber.",
            "papa|Le pied était assez large.",
            "maman|La nappe les abrite, au pied.",
            "narrateur|Le mince a une miette sur le bec.",
            "enfant-m|Le dîner, après ?",
            "narrateur|Au pied, la nappe tient le grain, à l'abri.",
        ),
        (2, 2, 3): L(
            "narrateur|Nino avait tiré trop fort, presque.",
            "narrateur|Le tissu s'est arrêté, au milieu.",
            "enfant-m|Vous avez eu le pain.",
            "papa|Plus besoin des trous.",
            "maman|Tes mains ont tenu le tissu.",
            "narrateur|Un pli reste, tiède, contre le bois.",
            "enfant-m|On est arrivés.",
            "narrateur|Un pli de nappe garde le grain, contre le bois.",
        ),
        (2, 3, 1): L(
            "narrateur|Le vent avait soulevé le tissu, presque.",
            "narrateur|La marche basse l'a calmé.",
            "enfant-m|Vous aviez les marches.",
            "papa|La marche avait deux places.",
            "maman|Le vent n'a plus pris le tissu.",
            "narrateur|Nino lisse un pli, un dernier coup.",
            "enfant-m|On reste un peu.",
            "narrateur|La nappe sur la marche, le grain au bord.",
        ),
        (2, 3, 2): L(
            "narrateur|Là-haut, la nappe allait claquer, seule.",
            "narrateur|Plus près, les deux sont venus.",
            "enfant-m|Vous aviez le goûter, plus près.",
            "papa|Rentrer vers l'eau, c'était mieux.",
            "maman|La nappe sent l'eau, un peu.",
            "narrateur|Le rond et le mince se touchent, un peu.",
            "enfant-m|Le goûter est fini, pour de vrai.",
            "narrateur|Plus près, la nappe sent l'eau, le grain tient.",
        ),
        (2, 3, 3): L(
            "narrateur|Au soleil, le tissu allait brûler, presque.",
            "narrateur|L'ombre l'a refroidi, à temps.",
            "enfant-m|Vous aviez la place, à l'abri.",
            "papa|L'ombre était plus fraîche.",
            "maman|Le vent est resté dehors.",
            "narrateur|Un bec rond, un bec mince, sur le tissu.",
            "enfant-m|On rentre, maintenant.",
            "narrateur|L'ombre froide tient le grain sur la nappe.",
        ),
        (3, 1, 1): L(
            "narrateur|Le seau avait penché, presque trop.",
            "narrateur|Nino l'a redressé, à temps.",
            "enfant-m|Vous avez eu votre pain.",
            "papa|Le seau est resté droit.",
            "maman|Ils sont ensemble, quand même.",
            "narrateur|Deux ronds d'eau restent, loin du seau.",
            "enfant-m|On reste un peu.",
            "narrateur|Le seau vide garde le grain, au fond.",
        ),
        (3, 1, 2): L(
            "narrateur|Un morceau avait glissé, presque perdu.",
            "narrateur|Deux tas l'ont sauvé, au bord.",
            "enfant-m|Vous teniez, tous les deux.",
            "papa|Chacun a eu le sien.",
            "maman|Le seau n'a plus penché.",
            "narrateur|Nino tapote l'anse, léger.",
            "enfant-m|On rentre, maintenant.",
            "narrateur|Deux tas, le seau à côté, le grain au milieu.",
        ),
        (3, 1, 3): L(
            "narrateur|La planche avait penché sous le seau.",
            "narrateur|Le pont a tenu, droit.",
            "enfant-m|Un goûter, plus large.",
            "papa|L'eau n'a plus gagné.",
            "maman|Le seau a tenu le pont.",
            "narrateur|Le métal sonne une fois, puis plus.",
            "enfant-m|Une miette, pour rire.",
            "narrateur|Sur le pont, le seau sonne, le grain reste.",
        ),
        (3, 2, 1): L(
            "narrateur|Sur le banc, le seau allait tout perdre.",
            "narrateur|L'herbe l'a reçu, à temps.",
            "enfant-m|On a goûté ici, sans tomber.",
            "papa|L'herbe avait deux places.",
            "maman|Le seau reste droit, maintenant.",
            "narrateur|Le mince pointe le ciel, un instant.",
            "enfant-m|On reste un peu.",
            "narrateur|Dans l'herbe, le seau penche, le grain au bord.",
        ),
        (3, 2, 2): L(
            "narrateur|Le métal avait cogné, presque trop fort.",
            "narrateur|Le pied du banc a tout calmé.",
            "enfant-m|Vous teniez, sans tomber.",
            "papa|Le pied était assez large.",
            "maman|Le seau tient, sans cogner.",
            "narrateur|Le mince a une miette sur le bec.",
            "enfant-m|Le dîner, après ?",
            "narrateur|Au pied du banc, le seau tient le grain.",
        ),
        (3, 2, 3): L(
            "narrateur|Une miette avait fuité, avant le tissu.",
            "narrateur|La nappe l'a arrêtée, à temps.",
            "enfant-m|Vous avez eu le pain.",
            "papa|Plus besoin des trous.",
            "maman|Le seau pose sa place, dessus.",
            "narrateur|Il les regarde, l'un contre l'autre.",
            "enfant-m|On est arrivés.",
            "narrateur|La nappe sous le seau, le grain brille.",
        ),
        (3, 3, 1): L(
            "narrateur|Là-haut, le seau allait taper, trop fort.",
            "narrateur|La marche basse l'a reçu, calme.",
            "enfant-m|Vous aviez les marches.",
            "papa|La marche avait deux places.",
            "maman|Le seau n'a plus tapé.",
            "narrateur|Nino lisse l'anse, un dernier coup.",
            "enfant-m|On reste un peu.",
            "narrateur|La marche, le seau, et le grain doré.",
        ),
        (3, 3, 2): L(
            "narrateur|Là-haut, le seau allait rester, seul.",
            "narrateur|Plus près, les deux sont venus.",
            "enfant-m|Vous aviez le goûter, plus près.",
            "papa|Rentrer vers l'eau, c'était mieux.",
            "maman|Une goutte tremble, puis s'arrête.",
            "narrateur|Le rond et le mince se touchent, un peu.",
            "enfant-m|Le goûter est fini, pour de vrai.",
            "narrateur|Plus près, une goutte touche le grain, puis plus.",
        ),
        (3, 3, 3): L(
            "narrateur|Au soleil, le seau allait chauffer, trop.",
            "narrateur|L'ombre l'a refroidi, à temps.",
            "enfant-m|Vous aviez la place, à l'abri.",
            "papa|L'ombre était plus fraîche.",
            "maman|Le vent est resté dehors.",
            "narrateur|Un bec rond, un bec mince, près du seau.",
            "enfant-m|On rentre, maintenant.",
            "narrateur|L'ombre du kiosque tient le seau et le grain.",
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
        "narrateur|Le seau vide tape la hanche de papa.",
        "enfant-m|Toc.",
        "papa|On arrive, Nino.",
        "narrateur|Le parc du village s'ouvre, large.",
        "narrateur|L'herbe sent le soleil, tiède.",
        "maman|Tu entends la mare, là-bas ?",
        "enfant-m|Oui, elle clapote.",
        "narrateur|Un kiosque jette une ombre, longue.",
        "narrateur|Le banc attend, vide, près de l'eau.",
        "narrateur|Une feuille sèche craque, sous le pas.",
        "enfant-m|Ça sent le pain.",
        "papa|Oui, il est tiède.",
        "narrateur|Deux canards glissent, l'un derrière l'autre.",
        "narrateur|Le premier a le ventre rond.",
        "narrateur|Le second a le cou mince.",
        "enfant-m|Ils sont deux.",
        "papa|Tu veux leur porter le pain ?",
        "enfant-m|Oui, aux deux.",
        "narrateur|Le sac chauffe le ventre de Nino.",
        "narrateur|Il ouvre un coin du sac.",
        "narrateur|Le pain, la nappe, le seau.",
        "narrateur|Sur la croûte, un grain doré brille.",
        "enfant-m|Un petit soleil, collé.",
        "maman|Tu l'as vu, ce grain ?",
        "enfant-m|Oui.",
        "narrateur|Nino le touche du doigt, léger.",
        "narrateur|Le canard mince tourne la tête, vers le chemin.",
        "papa|Ils peuvent partir, Nino.",
        "enfant-m|Avant qu'ils partent.",
        "narrateur|En ce moment, Nino serre le sac.",
        "maman|Merci d'avoir vu les deux.",
        "papa|On prépare le goûter, alors ?",
        "enfant-m|Oui.",
        "narrateur|Son sourire est large, impatient.",
        "narrateur|L'envie presse, dans sa poitrine.",
    )
    sons["CHK_T0000_P0000"] = "parc,seau,canards"
    profiles["CHK_T0000_P0000"] = "opening"
    emph["CHK_T0000_P0000"] = "grain doré"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du sac.",
        "narrateur|Le pain, la nappe, et le seau.",
        "maman|Tu commences par laquelle ?",
    )
    profiles["CHK_T0001_P0000"] = "choice"
    extras["CHK_T0001_P0000"] = t3lab("le pain", "la nappe", "le seau")

    t2_sons = {1: "eau,canards", 2: "bois,oiseaux", 3: "vent,marches"}
    t2_emph = {1: "mare", 2: "banc", 3: "kiosque"}
    t3_emph = {
        1: {1: "bord", 2: "tas", 3: "pont"},
        2: {1: "herbe", 2: "pied", 3: "nappe"},
        3: {1: "marche", 2: "près", 3: "ombre"},
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
        emph[cid] = "grain doré"

        t2q = f"{base}_T0002_P0000"
        scripts[t2q] = t2_question(t1)
        profiles[t2q] = "choice"
        extras[t2q] = t3lab("la mare", "le banc", "le kiosque")

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
                sons[fin] = "canards,parc"
                profiles[fin] = "ending"
                emph[fin] = "grain doré"

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
    lasts = []
    for c in fins:
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{c['chunk_id']} fin mécanique: {last}")
        lasts.append(last)
        if "grain doré" not in c["text"].lower() and "grain" not in last:
            raise SystemExit(f"{c['chunk_id']} grain doré non payé")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images non distinctes: {len(set(lasts))}")

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for tic in TICS + (
        "hugo",
        "kenzo",
        "bateau",
        "capitaine",
        "plic",
        "volet jaune",
        "peluche",
        "défilé",
        "poupée",
        "cuisine",
        "dînette",
        "dinette",
        "bac à sable",
        "toboggan",
        "balançoire",
        "chambre",
        "marché",
        "ancre",
        "étoile brune",
        "fil pâle",
        "marque fine",
        "ombre-flèche",
        "nœud de raphia",
        "bouton de nacre",
        "perle de verre",
        "œillet",
    ):
        if tic in whole:
            raise SystemExit(f"{SID} slogan/calque: {tic}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "nina" in blob or "amir" in blob:
        raise SystemExit(f"{SID}: second enfant inventé")
    for bad in ("déjà", "encore", "tout doux", "tout calme"):
        if bad in blob:
            raise SystemExit(f"{SID} tic corpus: {bad}")
    if "grain doré" not in out["chunks"][0]["text"].lower():
        raise SystemExit(f"{SID}: indice manquant à l'ouverture")
    if not all(c.get("text_xai_tags") for c in out["chunks"]):
        raise SystemExit(f"{SID}: text_xai_tags manquant")
    if not all(c.get("notes") for c in out["chunks"]):
        raise SystemExit(f"{SID}: notes manquant")
    if not all(c.get("style_energy") for c in out["chunks"]):
        raise SystemExit(f"{SID}: style_energy manquant")
    for c in out["chunks"]:
        if c["text_xai_tags"] == c["text"]:
            raise SystemExit(f"{c['chunk_id']}: text_xai_tags = text")
    if len(out["chunks"]) != 86:
        raise SystemExit(f"{SID}: {len(out['chunks'])} chunks != 86")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    write_tree()
    relecture(
        SID,
        TITLE,
        "Parc du village, seau qui tape, pain tiède, grain doré. Nino veut porter "
        "le pain aux deux canards (nappe + seau) avant qu'ils partent. T1 = pain / "
        "nappe / seau : les trois partent. T2 = mare (l'eau avale) / banc (fentes) / "
        "kiosque (trop haut). Première idée échoue ; sourire parti ; poitrine serrée ; "
        "adulte accroupi. T3 = bord, deux tas, pont ; herbe, pied, nappe ; marches, "
        "plus près, ombre. Nino refuse de relancer. Le grain doré du début paie le "
        "climax. 27 fins : le grain reste, l'objet porte une trace, ça a failli rater. "
        "Leçon vécue (DIF.COR.002) : deux places, pas un commentaire.",
        "F-NAR-019 / example4 v2. N1 ≤ 10. Un seul enfant (Nino). Tics « encore / "
        "déjà / tout doux / tout calme » jetés. Indice unique : grain doré. TTS par "
        "chunk (profiles example2). Un merci de maman (avoir vu les deux). Pas apply. "
        "Audio non cuit.",
    )


if __name__ == "__main__":
    main()
