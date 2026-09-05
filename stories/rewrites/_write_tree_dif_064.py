#!/usr/bin/env python3
"""TREE-DIF-064 — Le cerf-volant d'Amir, sur la dune (F-NAR-019, N3, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-064"
N3 = LIMITS["N3"]
TITLE = "Le cerf-volant d'Amir, sur la dune"
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="cerf-volant",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le rouge veut voir la mer avant le vent; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change la suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="cerf-volant",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde ce qu'il tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="dune",
        note="arc=confirmation; intention=relancer; emotion=élan; intensite=1; destinataire=enfant; sous_texte=les trois affaires viennent; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il veut lancer trop vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=le premier lancer rate; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=le calme a ouvert l'air; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="cerf-volant",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le rouge a vu la mer; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"fin: {ph}")
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        out.append(f"{role}|{ph}")
    return out


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp:
        e = esc(emp)
        if e in body:
            body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
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
    tag = m.get("pitchTag")
    if tag:
        body = f"<{tag}>{body}</{tag}>"
    pause = m["pause"]
    suffix = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + suffix).strip()


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if "note" in extra:
        m["note"] = extra["note"]
    text, script = from_script(lines)
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
    out = deepcopy(src)
    out["text"] = text
    out["script"] = script
    out["sons"] = sons if sons is not None else (src.get("sons") or "")
    if out["sons"] is None:
        out["sons"] = ""
    out["text_ssml"] = ssml(text, m)
    out["text_xai_tags"] = xai(text, m)
    out["rate_wpm"] = m["wpm"]
    out["rate_label"] = m["rate"]
    out["speed_xai"] = m["speed"]
    out["length_scale_piper"] = m["piper"]
    out["pitch_label"] = m["pitch"]
    out["pitch_ssml"] = m["pitchSsml"]
    out["pitch_xai_tag"] = m["pitchTag"]
    out["volume_label"] = m["volume"]
    out["volume_db"] = m["db"]
    out["emphasis_words"] = m.get("emphasis") or ""
    out["pause_before_ms"] = extra.get("pause_before_ms", 0)
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
    out["notes"] = m["note"]
    out["night_policy"] = "play"
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.items():
        if k in ("emphasis", "note", "pause_before_ms"):
            continue
        out[k] = v
    return out


def ending_note(a: int, b: int, c: int) -> str:
    times = {1: "posé", 2: "lent", 3: "ample"}
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=le_rouge_a_vu_la_mer; "
        f"tempo={times[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


OPENING = vet(
    [
        "narrateur|Sur le bois de la cabane, un grain de sel brille.",
        "narrateur|Le fil du linge claque, sec, contre le pin.",
        "narrateur|Ça sent la résine chaude, et la mer.",
        "narrateur|Amir vit là, avec papa et maman.",
        "narrateur|La queue rouge tape la marche, impatiente.",
        "narrateur|Une mouette crie, trop haute pour le rouge.",
        "papa|Tu as vu la queue, Amir ?",
        "enfant-m|Elle veut partir !",
        "maman|C'est le cerf-volant, tout rouge.",
        "narrateur|En ce moment, Amir déplie un coin du tissu.",
        "enfant-m|Je veux qu'il voie la mer.",
        "narrateur|Il lance trop vite, depuis la marche.",
        "narrateur|Le nez rouge se plie contre le bois.",
        "narrateur|Amir souffle, les joues chaudes de dépit.",
        "enfant-m|Il ne vole pas !",
        "papa|Le vent va se coucher, tout à l'heure.",
        "maman|On prend les affaires, alors ?",
        "papa|Merci, tu as dénoué la ficelle.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|Trois affaires attendent près du sable.",
        "narrateur|Le cerf-volant, la ficelle, et le piquet.",
        "maman|Tu prends quoi d'abord, Amir ?",
    ]
)

T1 = {
    1: dict(
        lab="le cerf-volant",
        ans="cerf-volant",
        acc="cerf-volant | le cerf-volant | d'abord le cerf-volant | le tissu | le rouge",
        retry="Amir prend le cerf-volant d'abord.",
        sons="tissu,vent",
        emp="tissu",
        passage=vet(
            [
                "narrateur|Amir prend le tissu rouge, chaud de soleil.",
                "enfant-m|Toi, tu vas voir la mer.",
                "narrateur|Il déplie trop vite, et le tissu claque.",
                "maman|Tiens le nez, pas la queue.",
                "narrateur|La queue rouge lui fouette le cou.",
                "papa|Ta queue me chatouille !",
                "enfant-m|Elle est trop contente.",
                "narrateur|Amir serre les lèvres, puis il ralentit.",
                "narrateur|Le tissu sent le soleil, contre ses paumes.",
                "narrateur|Maman glisse la ficelle contre son poignet.",
                "narrateur|Le piquet roule contre son genou, lourd.",
                "enfant-m|Nez en avant, queue derrière.",
                "papa|Le rouge est à toi.",
            ]
        ),
        question=vet(
            [
                "narrateur|Amir a pris le cerf-volant.",
                "maman|Il a pris quoi, d'abord ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Le tissu rouge reste contre sa poitrine, chaud.",
                "enfant-m|On va jusqu'à la dune.",
                "maman|Le vent n'attendra pas longtemps.",
                "papa|Tu tiens bien, Amir ?",
                "enfant-m|Oui, papa.",
                "narrateur|Un coin du tissu cherche l'air.",
            ]
        ),
        hip={
            1: "Entre ses doigts, le tissu rouge est chaud.",
            2: "Le tissu se tord, trop vite, trop fort.",
            3: "Un pli du tissu s'accroche, trop serré.",
            4: "Le tissu pèse, trop lourd, trop salé.",
        },
    ),
    2: dict(
        lab="la ficelle",
        ans="ficelle",
        acc="ficelle | la ficelle | d'abord la ficelle | le fil",
        retry="Amir prend la ficelle d'abord.",
        sons="ficelle",
        emp="ficelle",
        passage=vet(
            [
                "narrateur|Amir enroule la ficelle autour du poignet.",
                "enfant-m|Tu vas tenir le rouge.",
                "narrateur|Il serre trop, et ça marque la peau.",
                "papa|Pas trop serré, laisse un peu d'air.",
                "narrateur|Un tour glisse, puis tient.",
                "narrateur|La ficelle sent le sel, un peu collante.",
                "maman|Tu m'as fait un anneau.",
                "enfant-m|C'est pour tenir.",
                "narrateur|Papa pose le tissu plié contre le seau.",
                "narrateur|Le piquet reste planté, un peu de travers.",
                "enfant-m|Fil, tu restes avec moi.",
                "maman|La ficelle est prête.",
            ]
        ),
        question=vet(
            [
                "narrateur|Amir a pris la ficelle.",
                "papa|Il a pris quoi, d'abord ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|La ficelle fait un bracelet lâche, au poignet.",
                "enfant-m|Elle va tenir le rouge.",
                "papa|Ça sent le sel, toi.",
                "maman|Tes mains sont prêtes ?",
                "enfant-m|Oui, maman.",
                "narrateur|Un tour se desserre, puis se tait.",
            ]
        ),
        hip={
            1: "Au poignet, la ficelle colle un peu, de sel.",
            2: "La ficelle siffle, trop tendue, trop vive.",
            3: "La ficelle fait un nœud, trop vite.",
            4: "La ficelle goutte, trop mouillée, trop froide.",
        },
    ),
    3: dict(
        lab="le piquet",
        ans="piquet",
        acc="piquet | le piquet | d'abord le piquet | le bois",
        retry="Amir prend le piquet d'abord.",
        sons="bois,sable",
        emp="piquet",
        passage=vet(
            [
                "narrateur|Amir lève le piquet, le bois chaud.",
                "enfant-m|Tu vas tenir le fil.",
                "narrateur|Il plante trop fort, et le bois penche.",
                "maman|Pointe vers le bas, sans forcer.",
                "narrateur|Le bois tape le sable, un toc.",
                "narrateur|Amir essuie le sable sur sa paume.",
                "papa|Il a tracé une ligne, comme un serpent.",
                "enfant-m|C'est le chemin.",
                "narrateur|Maman glisse le tissu sous son autre bras.",
                "narrateur|La ficelle pend contre sa manche.",
                "enfant-m|Piquet, je te porte.",
                "papa|Le piquet est prêt, on avance.",
            ]
        ),
        question=vet(
            [
                "narrateur|Amir a pris le piquet.",
                "maman|Il a pris quoi, d'abord ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Le piquet reste contre son bras, lourd.",
                "enfant-m|Il va tenir le fil.",
                "maman|Le bois sent le soleil.",
                "papa|On y va, tous les trois ?",
                "enfant-m|Oui.",
                "narrateur|La pointe du piquet attend le sable.",
            ]
        ),
        hip={
            1: "Dans sa paume, le bois du piquet est tiède.",
            2: "Le piquet penche, trop léger dans l'air.",
            3: "Le piquet disparaît dans l'herbe, trop caché.",
            4: "Le piquet s'enfonce, trop mou dans le sable.",
        },
    ),
}

T2_CHOICE = {
    1: vet(
        [
            "narrateur|Le tissu tape sa poitrine, tout bas.",
            "narrateur|Devant, la crête soulève trop de vent.",
            "narrateur|L'herbe, elle, accroche les fils.",
            "narrateur|Plus bas, l'écume mouille le sable.",
            "papa|Amir, vous partez où ?",
        ]
    ),
    2: vet(
        [
            "narrateur|La ficelle frotte son poignet, un peu serrée.",
            "narrateur|Devant, la crête soulève trop de vent.",
            "narrateur|L'herbe, elle, accroche les fils.",
            "narrateur|Plus bas, l'écume mouille le sable.",
            "maman|Amir, vous partez où ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Le piquet tape son bras, sans bruit.",
            "narrateur|Devant, la crête soulève trop de vent.",
            "narrateur|L'herbe, elle, accroche les fils.",
            "narrateur|Plus bas, l'écume mouille le sable.",
            "papa|Amir, vous partez où ?",
        ]
    ),
}

T2 = {
    1: dict(
        sons="vent,dune",
        emp="crête",
        head="La crête de la dune souffle trop fort.",
        fail="Amir lance tout de suite, face au vent.",
        cry="Il va se déchirer !",
        mid1="La queue claque, trop prise.",
        mid2="Le nez rouge se plie, minuscule.",
        papa="Ici, le vent est trop grand.",
        maman="Le rouge a besoin d'un vent plus petit.",
        hip_key=2,
    ),
    2: dict(
        sons="herbe",
        emp="herbe",
        head="L'herbe de la dune tient trop, trop verte.",
        fail="Amir court, et l'herbe attrape le fil.",
        cry="Le fil est coincé !",
        mid1="Une tige tire, puis une autre.",
        mid2="Le rouge n'a plus d'air, trop bas.",
        papa="Ici, ça s'accroche trop.",
        maman="Le fil n'avance plus.",
        hip_key=3,
    ),
    3: dict(
        sons="vague,ecume",
        emp="écume",
        head="L'écume lèche le sable, trop près.",
        fail="Amir avance trop près, et une vague lèche.",
        cry="Il est tout mouillé !",
        mid1="Une vague revient, trop blanche.",
        mid2="Le rouge n'a plus de vent, trop lourd.",
        papa="Ici, ça mouille trop.",
        maman="Le rouge est trop lourd, trop mouillé.",
        hip_key=4,
    ),
}

T3_LABS = {
    1: ("plus bas", "attendre", "de côté"),
    2: ("plus court", "à genoux", "le sable"),
    3: ("plus haut", "après la vague", "loin de l'eau"),
}

T3_Q = {
    1: vet(
        [
            "narrateur|La crête n'a pas fini de souffler.",
            "papa|Plus bas, attendre, ou de côté ?",
        ]
    ),
    2: vet(
        [
            "narrateur|L'herbe n'a pas fini d'accrocher.",
            "maman|Plus court, à genoux, ou le sable ?",
        ]
    ),
    3: vet(
        [
            "narrateur|L'écume n'a pas fini de lécher.",
            "papa|Plus haut, après la vague, ou loin de l'eau ?",
        ]
    ),
}


def t2_scene(t1: int, t2: int) -> list[str]:
    o = T1[t1]
    d = T2[t2]
    return vet(
        [
            f"narrateur|{o['hip'][1]}",
            f"narrateur|{d['head']}",
            f"narrateur|{d['fail']}",
            f"narrateur|{o['hip'][d['hip_key']]}",
            f"enfant-m|{d['cry']}",
            f"narrateur|{d['mid1']}",
            f"narrateur|{d['mid2']}",
            "narrateur|Amir souffle, les épaules basses.",
            f"papa|{d['papa']}",
            f"maman|{d['maman']}",
            "enfant-m|Alors on fait quoi ?",
            "papa|Tu vois comment, Amir ?",
        ]
    )


RES = {
    (1, 1, 1): vet(
        [
            "enfant-m|Plus bas, d'abord.",
            "narrateur|Il baisse le tissu, loin de la crête.",
            "narrateur|Amir descend la pente, les genoux au sable.",
            "narrateur|L'air est plus petit, contre la dune.",
            "narrateur|Il compte un, deux, sans lancer.",
            "narrateur|Un coin du tissu cherche l'air.",
            "papa|Ici, le vent est plus petit.",
            "enfant-m|Ici, tu ne te déchires plus.",
            "maman|Plus bas, ça tenait mieux.",
        ]
    ),
    (1, 1, 2): vet(
        [
            "enfant-m|On attend le vent.",
            "narrateur|Il tient le tissu contre lui, sans le lancer.",
            "narrateur|Le souffle passe, une fois, puis plus.",
            "enfant-m|Tu peux partir, maintenant.",
            "narrateur|Le tissu reste plié, contre lui.",
            "papa|Le vent s'est tu.",
            "narrateur|Le rouge se lève, sans se tordre.",
            "maman|Le rouge se tient, sans claquer.",
        ]
    ),
    (1, 1, 3): vet(
        [
            "enfant-m|De côté, pas face au vent.",
            "narrateur|Il tourne le tissu de côté, sans forcer.",
            "narrateur|Le nez rouge prend moins d'air.",
            "narrateur|Amir compte tout bas, un, deux.",
            "narrateur|Le tissu reste plié, le temps d'un souffle.",
            "papa|De côté, ça n'a pas trop tiré.",
            "enfant-m|Tu es à l'abri.",
            "maman|Le nez a moins tiré, comme ça.",
        ]
    ),
    (1, 2, 1): vet(
        [
            "enfant-m|Plus court, d'abord.",
            "narrateur|Il tient le tissu tout près, ficelle courte.",
            "narrateur|L'herbe n'atteint plus le fil.",
            "narrateur|Le rouge se lève, tout petit.",
            "narrateur|Le tissu reste plié un instant, puis s'ouvre.",
            "maman|Le fil n'a plus accroché.",
            "enfant-m|Maintenant, tu me vois.",
            "papa|Le rouge est parti, tout près.",
        ]
    ),
    (1, 2, 2): vet(
        [
            "enfant-m|À genoux, on dénoue.",
            "narrateur|À genoux, il dénoue le tissu, sans tirer.",
            "narrateur|Un nœud lâche, puis un autre.",
            "narrateur|L'herbe se tait, plus loin, toute seule.",
            "narrateur|Un coin du tissu cherche l'air.",
            "papa|Le nœud a lâché sans crier.",
            "enfant-m|C'est pour toi.",
            "maman|Le nœud a lâché tout seul.",
        ]
    ),
    (1, 2, 3): vet(
        [
            "enfant-m|Le sable, pas l'herbe.",
            "narrateur|Amir recule vers le sable nu, sans courir.",
            "narrateur|Sur le sable nu, le tissu ne s'accroche plus.",
            "narrateur|Plus de tiges, plus de nœuds.",
            "narrateur|Le tissu reste un moment, puis s'ouvre.",
            "papa|Tu t'es mis où c'est vide.",
            "enfant-m|Le fil est libre.",
            "maman|Le sable nu était plus simple.",
        ]
    ),
    (1, 3, 1): vet(
        [
            "enfant-m|Plus haut, d'abord.",
            "narrateur|Plus haut, le tissu n'a plus d'écume.",
            "narrateur|Amir gravit la dune, le sable qui glisse.",
            "narrateur|L'écume reste en bas, trop loin pour lécher.",
            "narrateur|Le tissu sèche un peu, contre lui.",
            "papa|La vague n'a plus touché.",
            "enfant-m|Maintenant, tu peux rester.",
            "maman|Le sable était plus sec, là-haut.",
        ]
    ),
    (1, 3, 2): vet(
        [
            "enfant-m|On attend la vague, d'abord.",
            "narrateur|Il tient le tissu, puis regarde la vague.",
            "narrateur|L'eau va, revient, puis se tait.",
            "narrateur|Le sable redevient ferme, tout net.",
            "narrateur|Un coin du tissu cherche l'air.",
            "papa|Tes pieds sont restés sur le sable.",
            "enfant-m|Tu es sec, maintenant.",
            "maman|La vague a fini toute seule.",
        ]
    ),
    (1, 3, 3): vet(
        [
            "enfant-m|Loin de l'eau, tout sec.",
            "narrateur|Loin de l'eau, le tissu reste sec, tout rouge.",
            "narrateur|Amir recule vers les cabanes, sans se presser.",
            "narrateur|L'écume se tait, plus loin, toute seule.",
            "narrateur|Le tissu sèche au vent du pin.",
            "papa|Le sec était assez large.",
            "enfant-m|Tu restes, rouge.",
            "maman|Loin de l'eau, ça suffisait.",
        ]
    ),
    (2, 1, 1): vet(
        [
            "enfant-m|Plus bas, d'abord.",
            "narrateur|Il baisse la ficelle, loin de la crête.",
            "narrateur|Amir descend, le fil lâche au poignet.",
            "narrateur|L'air est plus petit, contre la pente.",
            "narrateur|Il compte un, deux, le fil sans siffler.",
            "narrateur|Un bout de ficelle brille, prêt à tenir.",
            "papa|Ici, le vent est plus petit.",
            "enfant-m|Ici, tu ne te déchires plus.",
            "maman|Plus bas, le fil tenait mieux.",
        ]
    ),
    (2, 1, 2): vet(
        [
            "enfant-m|On attend le vent.",
            "narrateur|Il tient la ficelle, sans la dérouler.",
            "narrateur|Le souffle passe, une fois, puis plus.",
            "enfant-m|Tu peux partir, maintenant.",
            "narrateur|Enroulée, la ficelle attend contre sa manche.",
            "papa|Le vent s'est tu.",
            "narrateur|Le rouge se lève, le fil sans crier.",
            "maman|Le fil se tient, sans siffler.",
        ]
    ),
    (2, 1, 3): vet(
        [
            "enfant-m|De côté, pas face au vent.",
            "narrateur|Il tourne la ficelle de côté, sans forcer.",
            "narrateur|Le fil prend moins d'air, moins de bruit.",
            "narrateur|Amir compte tout bas, un, deux.",
            "narrateur|Enroulée, la ficelle attend un souffle.",
            "papa|De côté, ça n'a pas trop tiré.",
            "enfant-m|Tu es à l'abri.",
            "maman|Le fil a moins tiré, comme ça.",
        ]
    ),
    (2, 2, 1): vet(
        [
            "enfant-m|Plus court, d'abord.",
            "narrateur|Il déroule peu de ficelle, tout court.",
            "narrateur|L'herbe n'atteint plus le fil.",
            "narrateur|Le rouge se lève, tout petit.",
            "narrateur|Enroulée, la ficelle reste sage un instant.",
            "maman|Le fil n'a plus accroché.",
            "enfant-m|Maintenant, tu me vois.",
            "papa|Le rouge est parti, tout près.",
        ]
    ),
    (2, 2, 2): vet(
        [
            "enfant-m|À genoux, on dénoue.",
            "narrateur|À genoux, il dénoue la ficelle, sans tirer.",
            "narrateur|Un nœud lâche, puis un autre.",
            "narrateur|L'herbe se tait, plus loin, toute seule.",
            "narrateur|Un bout de ficelle brille, prêt à tenir.",
            "papa|Le nœud a lâché sans crier.",
            "enfant-m|C'est pour toi.",
            "maman|Le nœud a lâché tout seul.",
        ]
    ),
    (2, 2, 3): vet(
        [
            "enfant-m|Le sable, pas l'herbe.",
            "narrateur|Amir recule vers le sable nu, sans courir.",
            "narrateur|Sur le sable nu, la ficelle ne s'accroche plus.",
            "narrateur|Plus de tiges, plus de nœuds.",
            "narrateur|Enroulée, la ficelle attend, puis s'ouvre.",
            "papa|Tu t'es mis où c'est vide.",
            "enfant-m|Le fil est libre.",
            "maman|Le sable nu était plus simple.",
        ]
    ),
    (2, 3, 1): vet(
        [
            "enfant-m|Plus haut, d'abord.",
            "narrateur|Plus haut, la ficelle n'a plus d'écume.",
            "narrateur|Amir gravit la dune, le fil contre la manche.",
            "narrateur|L'écume reste en bas, trop loin pour lécher.",
            "narrateur|La ficelle sèche un peu, au poignet.",
            "papa|La vague n'a plus touché.",
            "enfant-m|Maintenant, tu peux rester.",
            "maman|Le sable était plus sec, là-haut.",
        ]
    ),
    (2, 3, 2): vet(
        [
            "enfant-m|On attend la vague, d'abord.",
            "narrateur|Il tient la ficelle, puis regarde la vague.",
            "narrateur|L'eau va, revient, puis se tait.",
            "narrateur|Le sable redevient ferme, tout net.",
            "narrateur|Un bout de ficelle brille, prêt à tenir.",
            "papa|Tes pieds sont restés sur le sable.",
            "enfant-m|Tu es sec, maintenant.",
            "maman|La vague a fini toute seule.",
        ]
    ),
    (2, 3, 3): vet(
        [
            "enfant-m|Loin de l'eau, tout sec.",
            "narrateur|Loin de l'eau, la ficelle reste sèche.",
            "narrateur|Amir recule vers les cabanes, sans se presser.",
            "narrateur|L'écume se tait, plus loin, toute seule.",
            "narrateur|La ficelle sent le pin, au poignet.",
            "papa|Le sec était assez large.",
            "enfant-m|Tu restes, rouge.",
            "maman|Loin de l'eau, ça suffisait.",
        ]
    ),
    (3, 1, 1): vet(
        [
            "enfant-m|Plus bas, d'abord.",
            "narrateur|Il plante le piquet plus bas, loin de la crête.",
            "narrateur|Amir descend, le bois contre le sable.",
            "narrateur|L'air est plus petit, contre la pente.",
            "narrateur|Il compte un, deux, le bois sans trembler.",
            "narrateur|La pointe du piquet attend le sable.",
            "papa|Ici, le vent est plus petit.",
            "enfant-m|Ici, tu ne te déchires plus.",
            "maman|Plus bas, le bois tenait mieux.",
        ]
    ),
    (3, 1, 2): vet(
        [
            "enfant-m|On attend le vent.",
            "narrateur|Il tient le piquet, sans le planter.",
            "narrateur|Le souffle passe, une fois, puis plus.",
            "enfant-m|Tu peux partir, maintenant.",
            "narrateur|Planté, le piquet reste droit, sans bouger.",
            "papa|Le vent s'est tu.",
            "narrateur|Le rouge se lève, le bois sans pencher.",
            "maman|Le bois se tient, sans trembler.",
        ]
    ),
    (3, 1, 3): vet(
        [
            "enfant-m|De côté, pas face au vent.",
            "narrateur|Il plante le piquet de côté, sans forcer.",
            "narrateur|Le bois prend moins d'air, moins de bruit.",
            "narrateur|Amir compte tout bas, un, deux.",
            "narrateur|Planté, le piquet attend un souffle.",
            "papa|De côté, ça n'a pas trop tiré.",
            "enfant-m|Tu es à l'abri.",
            "maman|Le bois a moins tiré, comme ça.",
        ]
    ),
    (3, 2, 1): vet(
        [
            "enfant-m|Plus court, d'abord.",
            "narrateur|Il plante le piquet tout près, fil court.",
            "narrateur|L'herbe n'atteint plus le fil.",
            "narrateur|Le rouge se lève, tout petit.",
            "narrateur|Planté, le piquet reste un instant, puis tient.",
            "maman|Le fil n'a plus accroché.",
            "enfant-m|Maintenant, tu me vois.",
            "papa|Le rouge est parti, tout près.",
        ]
    ),
    (3, 2, 2): vet(
        [
            "enfant-m|À genoux, on dénoue.",
            "narrateur|À genoux, il dégage le piquet, sans tirer.",
            "narrateur|Un nœud lâche, puis un autre.",
            "narrateur|L'herbe se tait, plus loin, toute seule.",
            "narrateur|La pointe du piquet attend le sable.",
            "papa|Le nœud a lâché sans crier.",
            "enfant-m|C'est pour toi.",
            "maman|Le nœud a lâché tout seul.",
        ]
    ),
    (3, 2, 3): vet(
        [
            "enfant-m|Le sable, pas l'herbe.",
            "narrateur|Amir recule vers le sable nu, sans courir.",
            "narrateur|Sur le sable nu, le piquet trouve sa place.",
            "narrateur|Plus de tiges, plus de nœuds.",
            "narrateur|Planté, le piquet attend, puis tient.",
            "papa|Tu t'es mis où c'est vide.",
            "enfant-m|Le fil est libre.",
            "maman|Le sable nu était plus simple.",
        ]
    ),
    (3, 3, 1): vet(
        [
            "enfant-m|Plus haut, d'abord.",
            "narrateur|Plus haut, le piquet n'a plus d'eau.",
            "narrateur|Amir gravit la dune, le bois contre le bras.",
            "narrateur|L'écume reste en bas, trop loin pour lécher.",
            "narrateur|Le bois sèche un peu, dans sa paume.",
            "papa|La vague n'a plus touché.",
            "enfant-m|Maintenant, tu peux rester.",
            "maman|Le sable était plus sec, là-haut.",
        ]
    ),
    (3, 3, 2): vet(
        [
            "enfant-m|On attend la vague, d'abord.",
            "narrateur|Il tient le piquet, puis regarde la vague.",
            "narrateur|L'eau va, revient, puis se tait.",
            "narrateur|Le sable redevient ferme, tout net.",
            "narrateur|La pointe du piquet attend le sable.",
            "papa|Tes pieds sont restés sur le sable.",
            "enfant-m|Tu es sec, maintenant.",
            "maman|La vague a fini toute seule.",
        ]
    ),
    (3, 3, 3): vet(
        [
            "enfant-m|Loin de l'eau, tout sec.",
            "narrateur|Loin de l'eau, le piquet tient, sans s'enfoncer.",
            "narrateur|Amir recule vers les cabanes, sans se presser.",
            "narrateur|L'écume se tait, plus loin, toute seule.",
            "narrateur|Le bois sent le pin, près des marches.",
            "papa|Le sec était assez large.",
            "enfant-m|Tu restes, rouge.",
            "maman|Loin de l'eau, ça suffisait.",
        ]
    ),
}

FIN = {
    (1, 1, 1): vet(
        [
            "narrateur|Plus bas, le cerf-volant voit la mer.",
            "enfant-m|On s'est baissés.",
            "papa|Le vent, en bas, était plus petit.",
            "maman|Essuie tes genoux, sur le maillot.",
            "narrateur|Le tissu rouge sèche près du seau, un pli salé.",
            "narrateur|Un carré rouge reste bas, face à l'eau.",
        ]
    ),
    (1, 1, 2): vet(
        [
            "narrateur|Quand le vent s'est tu, le rouge a vu la mer.",
            "enfant-m|On a compté le souffle.",
            "papa|Le nez est parti, sans claquer.",
            "maman|Rentrez, le pin sent le chaud.",
            "narrateur|Le tissu rouge sèche près du seau, un pli salé.",
            "narrateur|Une poussière de sable tourne, puis s'arrête.",
        ]
    ),
    (1, 1, 3): vet(
        [
            "narrateur|De côté, le cerf-volant tient, sans se tordre.",
            "enfant-m|Je n'ai pas fait face.",
            "papa|De côté, ça n'a pas trop tiré.",
            "maman|Le bois des cabanes est retombé, plus loin.",
            "narrateur|Le tissu rouge sèche près du seau, un pli salé.",
            "narrateur|La mer se tait, derrière le tissu tiède.",
        ]
    ),
    (1, 2, 1): vet(
        [
            "narrateur|Tout près, le rouge a repris l'air.",
            "enfant-m|On a commencé tout court.",
            "papa|Les tiges n'ont plus accroché.",
            "maman|L'herbe sent le sel, moins fort.",
            "narrateur|Le tissu rouge sèche près du seau, un pli salé.",
            "narrateur|Un brin d'herbe se recouche, lent.",
        ]
    ),
    (1, 2, 2): vet(
        [
            "narrateur|Quand le nœud s'est tu, le rouge a volé.",
            "enfant-m|On a dénoué, à genoux.",
            "papa|Le nœud a lâché sans crier.",
            "maman|Le fil a parlé tout seul.",
            "narrateur|Le tissu rouge sèche près du seau, un pli salé.",
            "narrateur|Un nœud vide reste dans sa paume.",
        ]
    ),
    (1, 2, 3): vet(
        [
            "narrateur|Sur le sable nu, le rouge touche le bleu.",
            "enfant-m|Je me suis mis où c'est vide.",
            "papa|Tu t'es glissé, comme le vent.",
            "maman|Vous rentrez, les mains pleines de sable.",
            "narrateur|Le tissu rouge sèche près du seau, un pli salé.",
            "narrateur|L'herbe reste derrière, sans rien tenir.",
        ]
    ),
    (1, 3, 1): vet(
        [
            "narrateur|Plus haut, le cerf-volant a tenu, tout sec.",
            "enfant-m|On a gravi la dune.",
            "papa|La vague n'a plus touché.",
            "maman|Vos manches sentent le sel.",
            "narrateur|Le tissu rouge sèche près du seau, un pli salé.",
            "narrateur|Un grain de sable sèche sur le bois.",
        ]
    ),
    (1, 3, 2): vet(
        [
            "narrateur|Après la vague, le rouge a vu la mer.",
            "enfant-m|On a laissé l'eau se taire.",
            "papa|Tes pieds sont restés sur le sable.",
            "maman|Tes doigts sentent le sel.",
            "narrateur|Le tissu rouge sèche près du seau, un pli salé.",
            "narrateur|La vague reste à sa place, plus loin.",
        ]
    ),
    (1, 3, 3): vet(
        [
            "narrateur|Loin de l'eau, le rouge tient, face aux cabanes.",
            "enfant-m|On a reculé vers les cabanes.",
            "papa|Le sec était assez large.",
            "maman|Rentrez, le maillot est sec.",
            "narrateur|Le tissu rouge sèche près du seau, un pli salé.",
            "narrateur|L'écume se tait, vers les cabanes.",
        ]
    ),
    (2, 1, 1): vet(
        [
            "narrateur|Plus bas, le fil tient le rouge au-dessus de l'eau.",
            "enfant-m|On s'est baissés, le fil lâche.",
            "papa|Le vent, en bas, était plus petit.",
            "maman|Essuie tes genoux, sur le maillot.",
            "narrateur|La ficelle reste enroulée, un bout collant de sel.",
            "narrateur|La ficelle laisse un anneau tiède au poignet.",
        ]
    ),
    (2, 1, 2): vet(
        [
            "narrateur|Quand le vent s'est tu, le fil a laissé le rouge.",
            "enfant-m|On a compté, le fil sans siffler.",
            "papa|Le nez est parti, sans claquer.",
            "maman|Rentrez, le pin sent le chaud.",
            "narrateur|La ficelle reste enroulée, un bout collant de sel.",
            "narrateur|Le fil ne siffle plus, et le rouge tient.",
        ]
    ),
    (2, 1, 3): vet(
        [
            "narrateur|De côté, le fil tient, sans trop tirer.",
            "enfant-m|Je n'ai pas fait face.",
            "papa|De côté, ça n'a pas trop tiré.",
            "maman|Le bois des cabanes est retombé, plus loin.",
            "narrateur|La ficelle reste enroulée, un bout collant de sel.",
            "narrateur|Un côté du tissu, à l'abri, voit la mer.",
        ]
    ),
    (2, 2, 1): vet(
        [
            "narrateur|Tout près, le fil court, net, au-dessus des tiges.",
            "enfant-m|On a commencé tout court.",
            "papa|Les tiges n'ont plus accroché.",
            "maman|L'herbe sent le sel, moins fort.",
            "narrateur|La ficelle reste enroulée, un bout collant de sel.",
            "narrateur|Le fil court, net, au-dessus des tiges.",
        ]
    ),
    (2, 2, 2): vet(
        [
            "narrateur|Quand le nœud s'est tu, le fil a parlé.",
            "enfant-m|On a dénoué, à genoux.",
            "papa|Le nœud a lâché sans crier.",
            "maman|Le fil a parlé tout seul.",
            "narrateur|La ficelle reste enroulée, un bout collant de sel.",
            "narrateur|Un tour de ficelle s'endort contre sa manche.",
        ]
    ),
    (2, 2, 3): vet(
        [
            "narrateur|Sur le sable nu, le fil garde une ligne.",
            "enfant-m|Je me suis mis où c'est vide.",
            "papa|Tu t'es glissé, comme le vent.",
            "maman|Vous rentrez, les mains pleines de sable.",
            "narrateur|La ficelle reste enroulée, un bout collant de sel.",
            "narrateur|Le sable nu garde une ligne de fil.",
        ]
    ),
    (2, 3, 1): vet(
        [
            "narrateur|Plus haut, le fil, sec, tremble un peu, puis tient.",
            "enfant-m|On a gravi la dune.",
            "papa|La vague n'a plus touché.",
            "maman|Vos manches sentent le sel.",
            "narrateur|La ficelle reste enroulée, un bout collant de sel.",
            "narrateur|Le fil, sec, tremble un peu, puis tient.",
        ]
    ),
    (2, 3, 2): vet(
        [
            "narrateur|Après la vague, le fil a vu la mer, sec.",
            "enfant-m|On a laissé l'eau se taire.",
            "papa|Tes pieds sont restés sur le sable.",
            "maman|Tes doigts sentent le sel.",
            "narrateur|La ficelle reste enroulée, un bout collant de sel.",
            "narrateur|Un bout collant de sel sèche au poignet.",
        ]
    ),
    (2, 3, 3): vet(
        [
            "narrateur|Loin de l'eau, le fil sent le pin.",
            "enfant-m|On a reculé vers les cabanes.",
            "papa|Le sec était assez large.",
            "maman|Rentrez, le maillot est sec.",
            "narrateur|La ficelle reste enroulée, un bout collant de sel.",
            "narrateur|La ficelle sent le pin, loin de l'eau.",
        ]
    ),
    (3, 1, 1): vet(
        [
            "narrateur|Plus bas, le piquet garde le fil, face à l'eau.",
            "enfant-m|On s'est baissés, le bois droit.",
            "papa|Le vent, en bas, était plus petit.",
            "maman|Essuie tes genoux, sur le maillot.",
            "narrateur|Le piquet garde un peu de sable, près du fil.",
            "narrateur|Le piquet, plus bas, garde le fil.",
        ]
    ),
    (3, 1, 2): vet(
        [
            "narrateur|Quand le vent s'est tu, le bois est resté droit.",
            "enfant-m|On a compté, le bois sans pencher.",
            "papa|Le nez est parti, sans claquer.",
            "maman|Rentrez, le pin sent le chaud.",
            "narrateur|Le piquet garde un peu de sable, près du fil.",
            "narrateur|Le bois reste droit, sans trembler.",
        ]
    ),
    (3, 1, 3): vet(
        [
            "narrateur|De côté, une ombre de piquet, sur le sable.",
            "enfant-m|Je n'ai pas fait face.",
            "papa|De côté, ça n'a pas trop tiré.",
            "maman|Le bois des cabanes est retombé, plus loin.",
            "narrateur|Le piquet garde un peu de sable, près du fil.",
            "narrateur|Une ombre de piquet, de côté, sur le sable.",
        ]
    ),
    (3, 2, 1): vet(
        [
            "narrateur|Tout près, la pointe du piquet, dans le sable nu.",
            "enfant-m|On a commencé tout court.",
            "papa|Les tiges n'ont plus accroché.",
            "maman|L'herbe sent le sel, moins fort.",
            "narrateur|Le piquet garde un peu de sable, près du fil.",
            "narrateur|La pointe du piquet, près, dans le sable nu.",
        ]
    ),
    (3, 2, 2): vet(
        [
            "narrateur|Quand le nœud s'est tu, un toc de bois, puis plus.",
            "enfant-m|On a dénoué, à genoux.",
            "papa|Le nœud a lâché sans crier.",
            "maman|Le fil a parlé tout seul.",
            "narrateur|Le piquet garde un peu de sable, près du fil.",
            "narrateur|Un toc de bois, puis plus rien.",
        ]
    ),
    (3, 2, 3): vet(
        [
            "narrateur|Sur le sable nu, le piquet tient, hors de l'herbe.",
            "enfant-m|Je me suis mis où c'est vide.",
            "papa|Tu t'es glissé, comme le vent.",
            "maman|Vous rentrez, les mains pleines de sable.",
            "narrateur|Le piquet garde un peu de sable, près du fil.",
            "narrateur|Le piquet tient, hors de l'herbe.",
        ]
    ),
    (3, 3, 1): vet(
        [
            "narrateur|Plus haut, le bois, sec, n'a plus d'eau.",
            "enfant-m|On a gravi la dune.",
            "papa|La vague n'a plus touché.",
            "maman|Vos manches sentent le sel.",
            "narrateur|Le piquet garde un peu de sable, près du fil.",
            "narrateur|Le bois, plus haut, n'a plus d'eau.",
        ]
    ),
    (3, 3, 2): vet(
        [
            "narrateur|Après la vague, un trait de piquet, sec.",
            "enfant-m|On a laissé l'eau se taire.",
            "papa|Tes pieds sont restés sur le sable.",
            "maman|Tes doigts sentent le sel.",
            "narrateur|Le piquet garde un peu de sable, près du fil.",
            "narrateur|Un trait de piquet, sec, après la vague.",
        ]
    ),
    (3, 3, 3): vet(
        [
            "narrateur|Loin de l'eau, le piquet, près des cabanes, sent le pin.",
            "enfant-m|On a reculé vers les cabanes.",
            "papa|Le sec était assez large.",
            "maman|Rentrez, le maillot est sec.",
            "narrateur|Le piquet garde un peu de sable, près du fil.",
            "narrateur|Le piquet, près des cabanes, sent le pin.",
        ]
    ),
}


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple[list[str], str, str, dict]] = {}

    scripts["CHK_T0000_P0000"] = (OPENING, "opening", "mer,linge", {"emphasis": "cerf-volant"})
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "le cerf-volant",
            "option_2_label": "la ficelle",
            "option_3_label": "le piquet",
        },
    )

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        t1 = T1[a]
        scripts[base] = (t1["passage"], "action", t1["sons"], {"emphasis": t1["emp"]})
        scripts[f"{base}_Q0001"] = (
            t1["question"],
            "clue",
            "",
            {
                "expected_answer": t1["ans"],
                "accepted_examples": t1["acc"],
                "retry_prompt": t1["retry"],
                "engine_ok_text": "Oui, c'est ça.",
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
                "emphasis": t1["ans"],
            },
        )
        scripts[f"{base}_C0001"] = (t1["confirm"], "confirm", t1["sons"], {"emphasis": "dune"})
        scripts[f"{base}_T0002_P0000"] = (
            T2_CHOICE[a],
            "choice",
            "",
            {
                "option_1_label": "la crête",
                "option_2_label": "l'herbe",
                "option_3_label": "l'écume",
            },
        )
        for b in (1, 2, 3):
            leaf2 = f"{base}_T0002_P000{b}"
            t2d = T2[b]
            scripts[leaf2] = (t2_scene(a, b), "obstacle", t2d["sons"], {"emphasis": t2d["emp"]})
            scripts[f"{leaf2}_T0003_P0000"] = (
                T3_Q[b],
                "choice",
                "",
                {
                    "option_1_label": T3_LABS[b][0],
                    "option_2_label": T3_LABS[b][1],
                    "option_3_label": T3_LABS[b][2],
                },
            )
            for c in (1, 2, 3):
                leaf3 = f"{leaf2}_T0003_P000{c}"
                scripts[leaf3] = (
                    RES[(a, b, c)],
                    "resolution",
                    "vent,cerf-volant",
                    {"emphasis": "rouge"},
                )
                scripts[f"{leaf3}_F0001"] = (
                    FIN[(a, b, c)],
                    "ending",
                    "mer,pin",
                    {"emphasis": "cerf-volant", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra)[:8]}")

    chunks = []
    for c in src["chunks"]:
        cid = c["chunk_id"]
        lines, profile, sons, extra = scripts[cid]
        chunks.append(voice(by_src[cid], lines, profile, sons, extra))

    fins = [ch["text"] for ch in chunks if ch["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(fins))}/27")
    last_n = []
    for ch in chunks:
        if ch.get("kind") != "passage_fin":
            continue
        last = [x for x in ch["script"].splitlines() if x.startswith("narrateur|")][-1]
        last_n.append(last.split("|", 1)[1])
        last_low = last.split("|", 1)[1].lower()
        if "histoire" in last_low or "bravo" in last_low or "bon travail" in last_low:
            raise SystemExit(f"{ch['chunk_id']} fin mécanique: {last_low}")
    if len(set(last_n)) != 27:
        raise SystemExit(f"dernières images: {len(set(last_n))}/27")
    res_txt = [
        ch["text"]
        for ch in chunks
        if ch["kind"] == "passage"
        and "_T0003_P000" in ch["chunk_id"]
        and "_F0001" not in ch["chunk_id"]
        and not ch["chunk_id"].endswith("_T0003_P0000")
    ]
    if len(res_txt) != 27 or len(set(res_txt)) != 27:
        raise SystemExit(f"résolutions distinctes: {len(set(res_txt))}/{len(res_txt)}")

    blob = "\n".join(c["script"] for c in chunks).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in chunks
    ).lower()
    whole = blob + "\n" + labels
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "plus de temps ou de calme",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "hugo",
        "kenzo",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "plic",
        "volet jaune",
        "il faut attendre",
        "escargot",
        "balcon",
        "veau",
        "étable",
        "abreuvoir",
        "le four",
        "marché",
        "fort de coussins",
        "étoile",
        "bulle",
        "bronze",
        "tilleul",
        "moulinet",
        "carrousel",
        "marelle",
        "pain",
        "zoé",
        "zoe",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "amir" not in blob:
        raise SystemExit(f"{SID}: Amir absent")
    if "cerf-volant" not in blob:
        raise SystemExit(f"{SID}: cerf-volant absent")

    out = dict(src)
    out["fil_rouge"] = (
        "Au bord de la mer, Amir veut que son cerf-volant rouge voie la mer, "
        "avant que le vent se couche. Il lance trop vite depuis la marche : le nez "
        "se plie. Il prend d'abord le cerf-volant, la ficelle ou le piquet ; les trois "
        "viennent. La crête souffle trop, l'herbe accroche trop, l'écume mouille trop. "
        "Neuf façons de laisser du temps. Le rouge vole."
    )
    out["title"] = TITLE
    out["characters"] = "Amir, papa, maman"
    out["setting"] = "bord de mer : cabanes, dune, crête, herbe, écume"
    out["chunks"] = chunks
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
        mp = {ch["chunk_id"]: ch for ch in chunks}
        return sum(words(mp[i]["text"]) for i in ids)

    ws = [path_words(a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(ws)} max={max(ws)} moy={sum(ws)//len(ws)}")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"""# {SID} — {TITLE}

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Au bord de la mer, un grain de sel brille sur le bois de la cabane. Amir veut que son cerf-volant rouge voie la mer avant que le vent se couche. Il lance trop vite depuis la marche : le nez se plie. Il prend d'abord le cerf-volant, la ficelle ou le piquet ; les trois viennent. La crête souffle trop, l'herbe accroche trop, l'écume mouille trop. Neuf façons de laisser du temps. Le rouge vole.

## Vécu

Amir veut que le rouge voie la mer. Il lance trop tôt : le tissu claque le bois. Sur la crête, dans l'herbe ou près de l'écume, le premier lancer rate. Il compte, il tient sans lancer, il laisse le nœud ou la vague finir. La leçon se voit : trop de vent, trop d'accroche, trop d'eau — puis un air plus petit, et le rouge part. Un merci de papa, lié à la ficelle dénouée, pas un refrain scolaire.

## Vu et corrigé

- Titre noyau conservé. Troupe D16 : Amir, papa, maman. N3 ≤ 16.
- 86 nœuds, graphe et libellés d'options conservés.
- 27 fins textuellement distinctes, 27 résolutions distinctes, 27 dernières images.
- Première tentative échoue (marche, puis lieu choisi). Chaque choix change l'obstacle, le climax, la dernière image.
- Retour du tissu rouge, de la mer, du pin, des cabanes.
- TTS par fonction (ouverture, choix, indice, action, obstacle, résolution, retour).
- `slow` réservé aux choix, à l'indice et aux fins.
- Slogan « Plus de temps ou de calme », Hugo, Tom/Léa/Sami, bac/toboggan/balançoires, « bon travail » jetés.
- Récit autre que DIF-020 (escargot/balcon), DIF-030 (pain/four), DIF-040 (veau/ferme), DIF-048 (étoile/fenêtre), DIF-056 (bulle/bronze).
- Tics « tout doux / encore / déjà / tout calme » interdits. Morales collées remplacées par des faits vus.
- Chemins : {min(ws)}–{max(ws)} mots (moyenne {sum(ws)//len(ws)}). `check()` OK. Pas d'apply.

## Direction vocale

`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, tempo, sourire, respiration. Adulte conversationnel, pas maître. Obstacle en `low-pitch` ; fins `soft` / `slow` / `low-pitch`.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'apply.
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
