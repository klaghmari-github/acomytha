#!/usr/bin/env python3
"""TREE-DIF-063 — Le ticket rouge de Victorino, vers le lac (F-NAR-019, N2, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-063"
N2 = LIMITS["N2"]
TITLE = "Le ticket rouge de Victorino, vers le lac"
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="ticket rouge",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le grain de suie veut aller jusqu'au lac; tempo=naturel; sourire=léger; respiration=ample",
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
        emphasis="ticket",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde ce qu'il tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="lac",
        note="arc=confirmation; intention=relancer; emotion=élan; intensite=1; destinataire=enfant; sous_texte=les trois affaires montent; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il veut tout brûler d'un coup; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=la première idée rate, la seconde ruse arrive; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grain de suie",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=il a dosé son élan; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="lac",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le ticket a vu le lac; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    run = 1
    prev = ""
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
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
    emp = m.get("emphasis")
    if emp:
        e = esc(emp)
        if e in body:
            body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f"{body}</prosody><break time=\"{m['pause']}ms\"/></speak>"
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
        f"destinataire=enfant; sous_texte=le_ticket_a_vu_le_lac; "
        f"tempo={times[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


OPENING = vet(
    [
        "narrateur|Victorino connaît ce quai, ses bancs, son pigeon.",
        "narrateur|Le fer sent le savon chaud des mains de maman.",
        "narrateur|L'horloge jaune cliquette, sans se presser.",
        "narrateur|Un grain de suie repose sur le ticket rouge.",
        "enfant-m|Il est tout petit, papa.",
        "papa|Tu le vois, ce grain noir ?",
        "narrateur|Le pigeon penche la tête, près du banc.",
        "maman|Le wagon ouvre sa porte, là.",
        "enfant-m|Je garde le ticket jusqu'au lac.",
        "narrateur|Le banc du pigeon garde une chaleur ronde.",
        "narrateur|En ce moment, le sifflet perce le quai.",
        "narrateur|Victorino court trop, le ticket claque.",
        "narrateur|Le grain de suie glisse, presque tombé.",
        "narrateur|Son sourire part, les épaules basses.",
        "narrateur|L'envie tape, l'inquiétude aussi, dans la poitrine.",
        "papa|Tu veux le montrer trop vite ?",
        "narrateur|Papa s'accroupit, à la même hauteur.",
        "papa|Merci, tu as ralenti pour le grain.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|Trois affaires attendent près du banc du pigeon.",
        "narrateur|Le ticket rouge, le sac bleu, et la pomme.",
        "maman|Tu prends quoi d'abord, Victorino ?",
    ]
)

T1 = {
    1: dict(
        lab="le ticket rouge",
        ans="main",
        acc="main | la main | dans la main | sa main | les mains",
        retry="Le ticket est dans la main.",
        sons="papier,sifflet",
        emp="ticket rouge",
        passage=vet(
            [
                "narrateur|Victorino prend le ticket rouge, le grain de suie dessus.",
                "enfant-m|Toi, tu vas voir le lac.",
                "narrateur|Il le lève trop haut, trop vite.",
                "narrateur|Le papier claque, le grain penche.",
                "maman|Tiens-le bas, près de toi.",
                "narrateur|Victorino baisse le ticket, les joues chaudes.",
                "papa|Le sac bleu vient avec nous.",
                "narrateur|Maman glisse la pomme contre sa poche.",
                "enfant-m|Les trois, jusqu'au lac.",
                "narrateur|Ils marchent vers le wagon du lac.",
                "narrateur|Le grain de suie tient, tout noir.",
                "papa|Le ticket est à toi.",
                "maman|On n'oublie rien, on emporte tout.",
            ]
        ),
        question=vet(
            [
                "narrateur|Victorino a mis le ticket rouge.",
                "maman|Il est où, maintenant ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-m|Dans la main.",
                "maman|Oui, tout près.",
                "narrateur|Un sifflet réveille le quai.",
                "enfant-m|C'est mon train, pour le lac.",
                "narrateur|Victorino plie un genou, trop vite.",
                "narrateur|Le ticket dessine un pli, le grain penche.",
                "papa|On monte ici ?",
                "enfant-m|Oui, papa.",
                "narrateur|Le wagon avale leurs pas, un par un.",
                "narrateur|Une odeur de fer chaud entre avec eux.",
                "maman|On est dedans, Victorino.",
            ]
        ),
    ),
    2: dict(
        lab="le sac bleu",
        ans="bras",
        acc="bras | le bras | sous le bras | son bras",
        retry="Le sac est sous le bras.",
        sons="boucle,sifflet",
        emp="sac bleu",
        passage=vet(
            [
                "narrateur|Victorino passe le sac bleu sous le bras.",
                "enfant-m|Tu portes le voyage.",
                "narrateur|Il le lance trop vite, la sangle tourne.",
                "papa|Tiens-le contre toi, sans le jeter.",
                "narrateur|La boucle fait un petit clic.",
                "maman|Le ticket, ensuite, près de toi.",
                "narrateur|Il glisse la pomme d'une main.",
                "enfant-m|Je vais voir le lac.",
                "narrateur|Un genou rebondit, trop pressé.",
                "narrateur|Ils marchent vers le wagon du lac.",
                "narrateur|Le ticket reste au bord, le grain visible.",
                "maman|Le sac est prêt.",
                "papa|On n'oublie rien, on emporte tout.",
            ]
        ),
        question=vet(
            [
                "narrateur|Victorino a passé le sac bleu.",
                "papa|Il est où, maintenant ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-m|Sous le bras.",
                "papa|Oui.",
                "narrateur|La boucle du sac chatouille sa manche.",
                "enfant-m|C'est mon coin, pour le lac.",
                "narrateur|Victorino secoue le sac, un nuage de laine.",
                "narrateur|Un coin bleu traîne par terre, trop vite.",
                "maman|Ça sent le quai tiède.",
                "papa|Tes mains, sur le sac ?",
                "enfant-m|Oui, papa.",
                "narrateur|Ils montent, le grain de suie contre le bleu.",
                "narrateur|Une odeur de fer chaud entre avec eux.",
                "maman|On est dedans, Victorino.",
            ]
        ),
    ),
    3: dict(
        lab="la pomme",
        ans="poche",
        acc="poche | la poche | dans la poche | sa poche",
        retry="La pomme est dans la poche.",
        sons="pomme,sifflet",
        emp="pomme",
        passage=vet(
            [
                "narrateur|Victorino prend d'abord la pomme.",
                "enfant-m|Elle est froide, contre la poche.",
                "maman|Garde-la là, près de toi.",
                "narrateur|La peau sent le panier du village.",
                "papa|Le ticket et le sac, avec toi.",
                "narrateur|Il les pose près du banc du pigeon.",
                "enfant-m|Ma pomme va voyager aussi.",
                "narrateur|Ses talons frappent le quai, trop vite.",
                "narrateur|Ils marchent vers le wagon du lac.",
                "narrateur|Le ticket reste visible, le grain de suie dessus.",
                "papa|La pomme est prise.",
                "maman|On n'oublie rien, on emporte tout.",
            ]
        ),
        question=vet(
            [
                "narrateur|Victorino a pris la pomme.",
                "maman|Elle est où, maintenant ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-m|Dans la poche.",
                "maman|Oui.",
                "narrateur|La pomme roule un peu, puis s'arrête.",
                "enfant-m|Elle voyage contre moi.",
                "narrateur|Victorino la serre, la lâche, la reprend.",
                "narrateur|Un reflet rouge frotte sa poche.",
                "maman|Le wagon est prêt, devant.",
                "papa|On y va, tous les trois ?",
                "enfant-m|Oui.",
                "narrateur|Ils montent, la pomme froide, le grain noir.",
                "narrateur|Une odeur de fer chaud entre avec eux.",
                "maman|On est dedans, Victorino.",
            ]
        ),
    ),
}

T2_CHOICE = {
    1: vet(
        [
            "narrateur|Le ticket tape sa paume, trop léger.",
            "narrateur|Dans l'allée, le caoutchouc garde un pli.",
            "narrateur|À la vitre, un pré file tout vert.",
            "narrateur|Près des genoux, la tablette attend.",
            "papa|On s'installe où, Victorino ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Le sac bleu pèse à l'épaule, trop vif.",
            "narrateur|Dans l'allée, le caoutchouc garde un pli.",
            "narrateur|À la vitre, un pré file tout vert.",
            "narrateur|Près des genoux, la tablette attend.",
            "maman|On s'installe où, Victorino ?",
        ]
    ),
    3: vet(
        [
            "narrateur|La pomme frappe la poche, trop ronde.",
            "narrateur|Dans l'allée, le caoutchouc garde un pli.",
            "narrateur|À la vitre, un pré file tout vert.",
            "narrateur|Près des genoux, la tablette attend.",
            "papa|On s'installe où, Victorino ?",
        ]
    ),
}

T2 = {
    (1, 1): dict(
        sons="pas,roues",
        emp="allée",
        lines=vet(
            [
                "narrateur|Entre ses doigts, le ticket rouge est tiède.",
                "narrateur|L'allée du wagon file, trop longue.",
                "narrateur|Victorino court vers le fond, pour le lac.",
                "narrateur|Son talon accroche un pli du caoutchouc.",
                "enfant-m|Le ticket part !",
                "narrateur|Les roues changent de rythme, plus dures.",
                "narrateur|Son sourire part, la poitrine serrée.",
                "papa|Ici, ce n'est pas le lac.",
                "narrateur|Papa s'accroupit, à sa hauteur.",
                "enfant-m|Je ne fonce pas.",
                "narrateur|Personne ne dit le geste.",
                "narrateur|Il écoute les roues, puis le grain.",
                "narrateur|Il regarde le grain de suie, immobile.",
                "papa|Tu vois comment, Victorino ?",
            ]
        ),
    ),
    (1, 2): dict(
        sons="vitre,roues",
        emp="vitre",
        lines=vet(
            [
                "narrateur|Le ticket rouge colle à la vitre froide.",
                "enfant-m|Ici, je vois le lac, maman.",
                "narrateur|Dehors, le pré file trop vite.",
                "narrateur|Victorino presse le papier, trop fort.",
                "narrateur|Une mare passe, trop petite.",
                "enfant-m|L'eau, je l'ai vue !",
                "narrateur|Un éclair plus large frappe le verre.",
                "narrateur|Son sourire part, la poitrine serrée.",
                "maman|Ce n'est pas le lac, trop tôt.",
                "narrateur|Maman s'accroupit, à sa hauteur.",
                "enfant-m|J'attends le grain.",
                "narrateur|Personne ne dit le geste.",
                "narrateur|Il écoute la vitre, puis le grain.",
                "narrateur|Le grain de suie reste, seul, sur le rouge.",
            ]
        ),
    ),
    (1, 3): dict(
        sons="bois,roues",
        emp="tablette",
        lines=vet(
            [
                "narrateur|Victorino pose le ticket sur la tablette.",
                "enfant-m|Ici, c'est ma table, papa.",
                "narrateur|Le bois plié renvoie chaque secousse.",
                "narrateur|Le ticket grimpe au bord, trop vite.",
                "enfant-m|Il va tomber !",
                "narrateur|Il veut tout poser d'un coup, pomme et sac.",
                "narrateur|La tablette saute plus fort, trop chargée.",
                "narrateur|Son sourire part, la poitrine serrée.",
                "papa|Trop de choses, trop vite.",
                "narrateur|Papa s'accroupit, à sa hauteur.",
                "enfant-m|Je reste.",
                "narrateur|Personne ne dit le geste.",
                "narrateur|Il écoute le bois, puis le grain.",
                "narrateur|Il observe le grain de suie, au bord.",
            ]
        ),
    ),
    (2, 1): dict(
        sons="pas,boucle",
        emp="allée",
        lines=vet(
            [
                "narrateur|Le sac bleu tape un siège, clic trop fort.",
                "narrateur|L'allée du wagon file, trop étroite.",
                "narrateur|Victorino avance trop vite, le sac en avant.",
                "narrateur|La sangle accroche un dossier, puis lâche.",
                "enfant-m|Le sac part trop vite.",
                "narrateur|Les roues changent de rythme, plus dures.",
                "narrateur|Son sourire part, la poitrine serrée.",
                "papa|L'allée n'est pas un chemin de course.",
                "narrateur|Papa s'accroupit, à sa hauteur.",
                "enfant-m|Je ne fonce pas.",
                "narrateur|Personne ne dit le geste.",
                "narrateur|Il écoute les roues, puis le grain.",
                "narrateur|Il cherche le grain de suie, sur le ticket.",
                "maman|Le grain est là, contre le bleu.",
            ]
        ),
    ),
    (2, 2): dict(
        sons="vitre,boucle",
        emp="vitre",
        lines=vet(
            [
                "narrateur|Victorino pose le sac sous la vitre froide.",
                "enfant-m|Ici, je vois le lac, papa.",
                "narrateur|Le sac glisse comme un wagon trop pressé.",
                "narrateur|Une mare passe, trop petite, trop vite.",
                "enfant-m|L'eau, je l'ai vue !",
                "narrateur|Un éclair plus large frappe le verre.",
                "narrateur|Il veut coller le sac plus fort, tout de suite.",
                "narrateur|Son sourire part, la poitrine serrée.",
                "maman|Ce n'est pas le lac, trop tôt.",
                "narrateur|Maman s'accroupit, à sa hauteur.",
                "enfant-m|J'attends le grain.",
                "narrateur|Personne ne dit le geste.",
                "narrateur|Il écoute la vitre, puis le grain.",
                "narrateur|Le grain de suie tient, collé au ticket.",
            ]
        ),
    ),
    (2, 3): dict(
        sons="bois,boucle",
        emp="tablette",
        lines=vet(
            [
                "narrateur|Victorino pousse le sac sur la tablette.",
                "enfant-m|Ici, c'est ma table, maman.",
                "narrateur|Le bois plié renvoie chaque secousse.",
                "narrateur|Le sac se faufile sous la tablette, tout seul.",
                "enfant-m|Il disparaît !",
                "narrateur|Il veut tout coincer d'un coup, pomme et ticket.",
                "narrateur|La tablette saute plus fort, trop chargée.",
                "narrateur|Son sourire part, la poitrine serrée.",
                "papa|Trop de choses, trop vite.",
                "narrateur|Papa s'accroupit, à sa hauteur.",
                "enfant-m|Je reste.",
                "narrateur|Personne ne dit le geste.",
                "narrateur|Il écoute le bois, puis le grain.",
                "narrateur|Il observe le grain de suie, au bord du rouge.",
            ]
        ),
    ),
    (3, 1): dict(
        sons="pas,pomme",
        emp="allée",
        lines=vet(
            [
                "narrateur|La pomme tape sa poche, trop haut.",
                "narrateur|L'allée du wagon file, trop longue.",
                "narrateur|Victorino court vers le fond, la pomme qui rebondit.",
                "narrateur|Son talon accroche un pli du caoutchouc.",
                "enfant-m|Ma pomme part !",
                "narrateur|Les roues changent de rythme, plus dures.",
                "narrateur|Son sourire part, la poitrine serrée.",
                "papa|Ici, ce n'est pas le lac.",
                "narrateur|Papa s'accroupit, à sa hauteur.",
                "enfant-m|Je ne fonce pas.",
                "narrateur|Personne ne dit le geste.",
                "narrateur|Il écoute les roues, puis le grain.",
                "narrateur|Il regarde le grain de suie, sur le ticket.",
                "maman|Le grain reste, lui.",
            ]
        ),
    ),
    (3, 2): dict(
        sons="vitre,pomme",
        emp="vitre",
        lines=vet(
            [
                "narrateur|Victorino pose la pomme contre la vitre froide.",
                "enfant-m|Ici, je vois le lac, maman.",
                "narrateur|La pomme file, une bosse après l'autre.",
                "narrateur|Une mare passe, trop petite.",
                "enfant-m|L'eau, je l'ai vue !",
                "narrateur|Un éclair plus large frappe le verre.",
                "narrateur|Il veut coller la pomme plus fort, trop vite.",
                "narrateur|Son sourire part, la poitrine serrée.",
                "maman|Ce n'est pas le lac, trop tôt.",
                "narrateur|Maman s'accroupit, à sa hauteur.",
                "enfant-m|J'attends le grain.",
                "narrateur|Personne ne dit le geste.",
                "narrateur|Il écoute la vitre, puis le grain.",
                "narrateur|Le grain de suie reste, seul, sur le rouge.",
            ]
        ),
    ),
    (3, 3): dict(
        sons="bois,pomme",
        emp="tablette",
        lines=vet(
            [
                "narrateur|Victorino pose la pomme sur la tablette.",
                "enfant-m|Ici, c'est ma table, papa.",
                "narrateur|Le bois plié renvoie chaque secousse.",
                "narrateur|La pomme disparaît vers le bord, trop loin.",
                "enfant-m|Elle va tomber !",
                "narrateur|Il veut tout poser d'un coup, ticket et sac.",
                "narrateur|La tablette saute plus fort, trop chargée.",
                "narrateur|Son sourire part, la poitrine serrée.",
                "papa|Trop de choses, trop vite.",
                "narrateur|Papa s'accroupit, à sa hauteur.",
                "enfant-m|Je reste.",
                "narrateur|Personne ne dit le geste.",
                "narrateur|Il écoute le bois, puis le grain.",
                "narrateur|Il observe le grain de suie, au bord du ticket.",
            ]
        ),
    ),
}

T3_LABS = {
    1: ("les petits pas", "les roues", "papa tient"),
    2: ("les arbres", "le tunnel", "maman tient"),
    3: ("la pomme", "la tablette calme", "papa ouvre"),
}

T3_Q = {
    1: vet(
        [
            "narrateur|L'allée tremble un peu, sous les pieds.",
            "papa|Les petits pas, les roues, ou papa ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Le pré file trop vite, contre la vitre.",
            "maman|Les arbres, le tunnel, ou maman ?",
        ]
    ),
    3: vet(
        [
            "narrateur|La tablette n'a pas fini de sauter.",
            "papa|La pomme, la tablette, ou papa ?",
        ]
    ),
}


def res(a: int, b: int, c: int) -> list[str]:
    # 27 scènes : objet (ticket/sac/pomme) × lieu × geste. Grain payé.
    table = {
        (1, 1, 1): [
            "enfant-m|On fait les petits pas.",
            "papa|Toi tu poses un pied, moi je compte.",
            "narrateur|Victorino avance un pied, puis l'autre.",
            "narrateur|Le ticket reste bas, le grain visible.",
            "narrateur|Il compte un, deux, sans courir.",
            "narrateur|Les roues répondent, sous le plancher.",
            "papa|Ici, tes pieds sont plus petits.",
            "enfant-m|Le grain reste avec moi.",
            "maman|Les petits pas ont tenu le rouge.",
            "narrateur|L'allée redevient un chemin étroit.",
        ],
        (1, 1, 2): [
            "enfant-m|On attend les roues.",
            "narrateur|Victorino pose les genoux au banc.",
            "narrateur|Le ticket repose contre le dossier.",
            "narrateur|Les roues changent une fois, puis plus.",
            "enfant-m|Elles ne dansent plus ?",
            "maman|Le plancher est calme, oui.",
            "narrateur|Le grain de suie ne bouge plus.",
            "papa|Tes pieds ont trouvé le banc.",
            "narrateur|Victorino souffle, tout droit.",
            "enfant-m|Le lac peut arriver.",
        ],
        (1, 1, 3): [
            "enfant-m|Papa, tu tiens, s'il te plaît ?",
            "papa|Je tiens, tu poses tes pieds.",
            "narrateur|Papa prend l'épaule, Victorino tient le ticket.",
            "narrateur|Victorino avance, un pas, puis l'autre.",
            "narrateur|Le ticket reste dans sa main, grain noir.",
            "enfant-m|Toi tu tiens, moi je marche.",
            "maman|Vous avez demandé, et ça tient.",
            "papa|Ma main fait le rail, ici.",
            "narrateur|L'allée garde un pli mince.",
        ],
        (1, 2, 1): [
            "enfant-m|On compte les arbres.",
            "papa|Toi tu pointes, moi je compte.",
            "narrateur|Victorino pose le ticket, papa montre un arbre.",
            "narrateur|Des ombres courent sur la vitre.",
            "narrateur|Il pointe une, papa une autre, sans presser.",
            "enfant-m|Le lac est après.",
            "narrateur|Le grain de suie reste, au milieu du rouge.",
            "maman|Vous avez joué, puis posé les yeux.",
            "papa|La vitre est devenue un pré.",
            "narrateur|Un reflet vert reste, tout petit.",
        ],
        (1, 2, 2): [
            "enfant-m|J'attends le tunnel.",
            "papa|Quand il est noir, tu restes.",
            "narrateur|Victorino tient le ticket, le noir attend.",
            "narrateur|La vitre devient sombre, bout après bout.",
            "narrateur|Victorino souffle, les épaules baissent.",
            "papa|C'est à toi, Victorino.",
            "enfant-m|Je colle mon nez, sans crier.",
            "narrateur|Le grain de suie brille, même dans le noir.",
            "maman|Chacun son tour, sur la vitre.",
            "narrateur|Le jour revient, enfin.",
        ],
        (1, 2, 3): [
            "enfant-m|Maman, tu tiens, s'il te plaît ?",
            "maman|Je tiens, tu regardes le pré.",
            "narrateur|Maman tient Victorino, près du ticket.",
            "narrateur|Victorino colle le nez, les genoux se posent.",
            "narrateur|L'autre pied suit, la vitre au calme.",
            "enfant-m|Toi tu tiens, moi je vois.",
            "narrateur|Le grain de suie ne glisse plus.",
            "papa|Vous avez demandé, et ça marche.",
            "maman|Mes bras font la rambarde, maintenant.",
            "narrateur|Un carré de ciel reste bleu, autour.",
        ],
        (1, 3, 1): [
            "enfant-m|On pose la pomme, tout près.",
            "papa|Tu la poses, puis tu t'arrêtes.",
            "narrateur|La pomme voyage vers le ticket, sans rouler.",
            "narrateur|Le bois devient une pente, puis une rive.",
            "enfant-m|Doucement, la pomme tient.",
            "narrateur|Le grain de suie s'abrite sous la pomme.",
            "maman|Vous avez calmé la table.",
            "papa|La tablette est une table, maintenant.",
            "narrateur|Le ticket a trouvé son coin.",
            "enfant-m|Le goûter est là, tout bas.",
        ],
        (1, 3, 2): [
            "enfant-m|On attend la tablette.",
            "papa|Quand elle se tait, tu poses.",
            "narrateur|Une secousse, puis le bois reste calme.",
            "narrateur|Le ticket reste au creux de la table.",
            "narrateur|La tablette se tait, enfin.",
            "enfant-m|Maintenant !",
            "narrateur|Le grain de suie ne grimpe plus.",
            "maman|Le bois a fini ses vagues.",
            "papa|Tes genoux ont trouvé le banc.",
            "narrateur|Un pli du bois retombe, tout lent.",
        ],
        (1, 3, 3): [
            "enfant-m|Papa, tu ouvres le goûter ?",
            "papa|Je l'ouvre, sans me presser.",
            "narrateur|Papa ouvre le sac, près du ticket.",
            "narrateur|Victorino écoute les mains, plus que ses pieds.",
            "papa|Tu poses, et ça tient.",
            "enfant-m|Moi aussi, j'écoute.",
            "narrateur|Le grain de suie reste au bord du rouge.",
            "narrateur|La tablette devient une table.",
            "papa|Vous avez demandé l'ouverture.",
            "maman|Mes mains ont tenu le bord.",
        ],
        (2, 1, 1): [
            "enfant-m|On fait les petits pas.",
            "papa|Toi tu poses un pied, moi je compte.",
            "narrateur|Victorino avance, le sac sous le bras.",
            "narrateur|La boucle se tait, contre sa hanche.",
            "narrateur|Il compte un, deux, sans courir.",
            "narrateur|Les roues répondent, sous le plancher.",
            "papa|Ici, tes pieds sont plus petits.",
            "enfant-m|Le sac reste avec moi.",
            "narrateur|Le grain de suie tient, collé au ticket.",
            "maman|Les petits pas ont tenu le bleu.",
        ],
        (2, 1, 2): [
            "enfant-m|On attend les roues.",
            "narrateur|Victorino pose les genoux au banc.",
            "narrateur|Le sac repose contre le dossier, plié.",
            "narrateur|Les roues changent une fois, puis plus.",
            "enfant-m|Elles ne dansent plus ?",
            "maman|Le plancher est calme, oui.",
            "narrateur|Le grain de suie ne bouge plus, sur le rouge.",
            "papa|Tes pieds ont trouvé le banc.",
            "narrateur|Victorino souffle, tout droit.",
            "enfant-m|Le lac peut arriver.",
        ],
        (2, 1, 3): [
            "enfant-m|Papa, tu tiens, s'il te plaît ?",
            "papa|Je tiens, tu poses tes pieds.",
            "narrateur|Papa prend l'épaule, Victorino tient le sac.",
            "narrateur|Victorino avance, un pas, puis l'autre.",
            "narrateur|Le sac reste sous le bras, sans claquer.",
            "enfant-m|Toi tu tiens, moi je marche.",
            "narrateur|Le grain de suie voyage contre le bleu.",
            "maman|Vous avez demandé, et ça tient.",
            "papa|Ma main fait le rail, ici.",
            "narrateur|L'allée garde un pli mince.",
        ],
        (2, 2, 1): [
            "enfant-m|On compte les arbres.",
            "papa|Toi tu pointes, moi je compte.",
            "narrateur|Victorino pose le sac, papa montre un arbre.",
            "narrateur|Des ombres courent sur la vitre.",
            "narrateur|Il pointe une, papa une autre, sans presser.",
            "enfant-m|Le lac est après.",
            "narrateur|Le grain de suie reste, au bord du ticket.",
            "maman|Vous avez joué, puis posé les yeux.",
            "papa|La vitre est devenue un pré.",
            "narrateur|Un reflet vert reste sur le bleu.",
        ],
        (2, 2, 2): [
            "enfant-m|J'attends le tunnel.",
            "papa|Quand il est noir, tu restes.",
            "narrateur|Victorino tient le sac, le noir attend.",
            "narrateur|La vitre devient sombre, bout après bout.",
            "narrateur|Victorino souffle, les épaules baissent.",
            "papa|C'est à toi, Victorino.",
            "enfant-m|Je colle mon nez, sans crier.",
            "narrateur|Le grain de suie brille, même dans le noir.",
            "maman|Chacun son tour, sur la vitre.",
            "narrateur|Le jour revient, sur le bleu.",
        ],
        (2, 2, 3): [
            "enfant-m|Maman, tu tiens, s'il te plaît ?",
            "maman|Je tiens, tu regardes le pré.",
            "narrateur|Maman tient Victorino, près du sac.",
            "narrateur|Victorino colle le nez, les genoux se posent.",
            "narrateur|L'autre pied suit, la vitre au calme.",
            "enfant-m|Toi tu tiens, moi je vois.",
            "narrateur|Le grain de suie ne glisse plus, sur le rouge.",
            "papa|Vous avez demandé, et ça marche.",
            "maman|Mes bras font la rambarde, maintenant.",
            "narrateur|Un carré de ciel reste bleu, autour.",
        ],
        (2, 3, 1): [
            "enfant-m|On pose la pomme, tout près.",
            "papa|Tu la poses, puis tu t'arrêtes.",
            "narrateur|La pomme voyage vers le sac, sans rouler.",
            "narrateur|Le bois devient une pente, puis une rive.",
            "enfant-m|Doucement, la pomme tient.",
            "narrateur|Le grain de suie s'abrite près du bleu.",
            "maman|Vous avez calmé la table.",
            "papa|La tablette est une table, maintenant.",
            "narrateur|Le sac a trouvé son coin.",
            "enfant-m|Le goûter est là, tout bas.",
        ],
        (2, 3, 2): [
            "enfant-m|On attend la tablette.",
            "papa|Quand elle se tait, tu poses.",
            "narrateur|Une secousse, puis le bois reste calme.",
            "narrateur|Le sac reste fermé, au creux de la table.",
            "narrateur|La tablette se tait, enfin.",
            "enfant-m|Maintenant !",
            "narrateur|Le grain de suie ne grimpe plus, sur le rouge.",
            "maman|Le bois a fini ses vagues.",
            "papa|Tes genoux ont trouvé le banc.",
            "narrateur|Un pli du bois retombe, tout lent.",
        ],
        (2, 3, 3): [
            "enfant-m|Papa, tu ouvres le goûter ?",
            "papa|Je l'ouvre, sans me presser.",
            "narrateur|Papa ouvre le sac, tout grand.",
            "narrateur|Victorino écoute les mains, plus que ses pieds.",
            "papa|Tu poses, et ça tient.",
            "enfant-m|Moi aussi, j'écoute.",
            "narrateur|Le grain de suie reste au bord du ticket.",
            "narrateur|La tablette devient une table.",
            "papa|Vous avez demandé l'ouverture.",
            "maman|Mes mains ont tenu le bord.",
        ],
        (3, 1, 1): [
            "enfant-m|On fait les petits pas.",
            "papa|Toi tu poses un pied, moi je compte.",
            "narrateur|Victorino avance, la pomme dans la poche.",
            "narrateur|La pomme se tait, contre sa hanche.",
            "narrateur|Il compte un, deux, sans courir.",
            "narrateur|Les roues répondent, sous le plancher.",
            "papa|Ici, tes pieds sont plus petits.",
            "enfant-m|La pomme reste avec moi.",
            "narrateur|Le grain de suie tient, collé au ticket.",
            "maman|Les petits pas ont tenu la ronde.",
        ],
        (3, 1, 2): [
            "enfant-m|On attend les roues.",
            "narrateur|Victorino pose les genoux au banc.",
            "narrateur|La pomme repose contre le dossier.",
            "narrateur|Les roues changent une fois, puis plus.",
            "enfant-m|Elles ne dansent plus ?",
            "maman|Le plancher est calme, oui.",
            "narrateur|Le grain de suie ne bouge plus, sur le rouge.",
            "papa|Tes pieds ont trouvé le banc.",
            "narrateur|Victorino souffle, tout droit.",
            "enfant-m|Le lac peut arriver.",
        ],
        (3, 1, 3): [
            "enfant-m|Papa, tu tiens, s'il te plaît ?",
            "papa|Je tiens, tu poses tes pieds.",
            "narrateur|Papa prend l'épaule, Victorino tient la pomme.",
            "narrateur|Victorino avance, un pas, puis l'autre.",
            "narrateur|La pomme reste dans la poche, sans rebondir.",
            "enfant-m|Toi tu tiens, moi je marche.",
            "narrateur|Le grain de suie voyage contre la poche.",
            "maman|Vous avez demandé, et ça tient.",
            "papa|Ma main fait le rail, ici.",
            "narrateur|L'allée garde un pli mince.",
        ],
        (3, 2, 1): [
            "enfant-m|On compte les arbres.",
            "papa|Toi tu pointes, moi je compte.",
            "narrateur|Victorino pose la pomme, papa montre un arbre.",
            "narrateur|Des ombres courent sur la vitre.",
            "narrateur|Il pointe une, papa une autre, sans presser.",
            "enfant-m|Le lac est après.",
            "narrateur|Le grain de suie reste, au bord du ticket.",
            "maman|Vous avez joué, puis posé les yeux.",
            "papa|La vitre est devenue un pré.",
            "narrateur|Un reflet vert reste sur la pomme.",
        ],
        (3, 2, 2): [
            "enfant-m|J'attends le tunnel.",
            "papa|Quand il est noir, tu restes.",
            "narrateur|Victorino tient la pomme, le noir attend.",
            "narrateur|La vitre devient sombre, bout après bout.",
            "narrateur|Victorino souffle, les épaules baissent.",
            "papa|C'est à toi, Victorino.",
            "enfant-m|Je colle mon nez, sans crier.",
            "narrateur|Le grain de suie brille, même dans le noir.",
            "maman|Chacun son tour, sur la vitre.",
            "narrateur|Le jour revient, sur la pomme.",
        ],
        (3, 2, 3): [
            "enfant-m|Maman, tu tiens, s'il te plaît ?",
            "maman|Je tiens, tu regardes le pré.",
            "narrateur|Maman tient Victorino, près de la pomme.",
            "narrateur|Victorino colle le nez, les genoux se posent.",
            "narrateur|L'autre pied suit, la vitre au calme.",
            "enfant-m|Toi tu tiens, moi je vois.",
            "narrateur|Le grain de suie ne glisse plus, sur le rouge.",
            "papa|Vous avez demandé, et ça marche.",
            "maman|Mes bras font la rambarde, maintenant.",
            "narrateur|Un carré de ciel reste bleu, autour.",
        ],
        (3, 3, 1): [
            "enfant-m|On pose la pomme, tout près.",
            "papa|Tu la poses, puis tu t'arrêtes.",
            "narrateur|La pomme voyage d'un bord à l'autre, sans fuir.",
            "narrateur|Le bois devient une pente, puis une rive.",
            "enfant-m|Doucement, la pomme tient.",
            "narrateur|Le grain de suie s'abrite sous la pomme.",
            "maman|Vous avez calmé la table.",
            "papa|La tablette est une table, maintenant.",
            "narrateur|La pomme a trouvé son coin.",
            "enfant-m|Le goûter est là, tout bas.",
        ],
        (3, 3, 2): [
            "enfant-m|On attend la tablette.",
            "papa|Quand elle se tait, tu poses.",
            "narrateur|Une secousse, puis le bois reste calme.",
            "narrateur|La pomme reste au creux de la table.",
            "narrateur|La tablette se tait, enfin.",
            "enfant-m|Maintenant !",
            "narrateur|Le grain de suie ne grimpe plus, sur le rouge.",
            "maman|Le bois a fini ses vagues.",
            "papa|Tes genoux ont trouvé le banc.",
            "narrateur|Un pli du bois retombe, tout lent.",
        ],
        (3, 3, 3): [
            "enfant-m|Papa, tu ouvres le goûter ?",
            "papa|Je l'ouvre, sans me presser.",
            "narrateur|Papa ouvre le sac, près de la pomme.",
            "narrateur|Victorino écoute les mains, plus que ses pieds.",
            "papa|Tu poses, et ça tient.",
            "enfant-m|Moi aussi, j'écoute.",
            "narrateur|Le grain de suie reste au bord du ticket.",
            "narrateur|La tablette devient une table.",
            "papa|Vous avez demandé l'ouverture.",
            "maman|Mes mains ont tenu le bord.",
        ],
    }
    return vet(table[(a, b, c)])


def fin(a: int, b: int, c: int) -> list[str]:
    table = {
        (1, 1, 1): [
            "narrateur|Victorino s'assoit, le ticket contre la paume.",
            "enfant-m|On a failli le perdre, papa.",
            "papa|Tu as raconté le moment difficile.",
            "enfant-m|Surtout celui-là.",
            "maman|Le grain de suie est resté.",
            "narrateur|Le lac colle à la vitre, tout bleu.",
            "enfant-m|Bonjour, lac.",
            "narrateur|Le pli du caoutchouc garde la forme de son talon.",
        ],
        (1, 1, 2): [
            "narrateur|Victorino s'assoit, les roues plus calmes.",
            "enfant-m|J'ai attendu le plancher, d'abord.",
            "papa|Puis les roues sont restées sages.",
            "maman|Tes pieds ont trouvé le banc.",
            "narrateur|L'allée ne danse plus.",
            "narrateur|Le ticket garde un pli chaud, tout petit.",
            "enfant-m|À tout à l'heure, les rails.",
            "narrateur|Un clic des roues reste dans son genou.",
        ],
        (1, 1, 3): [
            "narrateur|Victorino s'assoit, la main de papa tout près.",
            "enfant-m|Tu tenais le rail.",
            "papa|Vous avez demandé, et ça tenait.",
            "maman|Sa main a fait le chemin.",
            "narrateur|Le wagon rend le silence.",
            "narrateur|Le ticket pose un grain de lumière.",
            "enfant-m|Le lac est à nous.",
            "narrateur|La manche de papa garde un reflet rouge.",
        ],
        (1, 2, 1): [
            "narrateur|Victorino s'assoit au bout des arbres.",
            "enfant-m|Toi tu comptais, moi je pointais.",
            "papa|Tes doigts ont fait le pré.",
            "maman|La vitre est devenue un lac.",
            "narrateur|Le verre redevient froid.",
            "narrateur|Le ticket garde un pli chaud, tout petit.",
            "enfant-m|Les arbres restent, maman.",
            "narrateur|Une bande verte dort sur la vitre.",
        ],
        (1, 2, 2): [
            "narrateur|Victorino s'assoit, le jour revenu.",
            "papa|J'ai compté le noir, puis c'était toi.",
            "enfant-m|J'ai attendu le tunnel.",
            "maman|Chacun son tour, sur la vitre.",
            "narrateur|Le lac tient, enfin.",
            "narrateur|Le ticket garde un grain de suie, plus noir.",
            "enfant-m|Bonjour, vitre.",
            "narrateur|Un rond sombre entoure le grain de suie.",
        ],
        (1, 2, 3): [
            "narrateur|Victorino s'assoit, tenu par maman.",
            "enfant-m|Tu tenais, tout près.",
            "papa|Les bras ont fait la rambarde.",
            "maman|La fenêtre est à vous.",
            "narrateur|Le verre a rendu le calme.",
            "narrateur|Le ticket garde un pli chaud, tout petit.",
            "enfant-m|Regarde, papa, il brille.",
            "narrateur|Un cercle de souffle de maman sèche sur le verre.",
        ],
        (1, 3, 1): [
            "narrateur|Victorino s'assoit devant la tablette.",
            "enfant-m|La pomme est sage, papa.",
            "papa|Tu la posais, puis tu t'arrêtais.",
            "maman|La table a son goûter, maintenant.",
            "narrateur|Le bois est redevenu plat.",
            "narrateur|Le ticket garde un pli chaud, tout petit.",
            "enfant-m|La pomme se tait.",
            "narrateur|La peau de la pomme porte une marque rouge.",
        ],
        (1, 3, 2): [
            "narrateur|Victorino s'assoit, la tablette plus calme.",
            "enfant-m|On a attendu le bois.",
            "papa|Quand il s'est tu, tu as posé.",
            "maman|La tablette a fait une table.",
            "narrateur|Tes genoux ont trouvé le banc.",
            "narrateur|Le ticket ne fait plus aucun bruit.",
            "enfant-m|Il est tiède.",
            "narrateur|Le bois de la tablette tient le coin du ticket.",
        ],
        (1, 3, 3): [
            "narrateur|Victorino s'assoit, le sac ouvert par papa.",
            "enfant-m|J'écoutais tes mains.",
            "papa|Moi aussi, j'ouvrais avec toi.",
            "maman|Tu as demandé, il a ouvert.",
            "narrateur|La tablette a rendu vos pas.",
            "narrateur|Le ticket garde un pli chaud, tout petit.",
            "enfant-m|Elle est à nous, maman.",
            "narrateur|La bouche du sac garde un éclat de lac.",
        ],
        (2, 1, 1): [
            "narrateur|Victorino s'assoit, le sac contre le banc.",
            "enfant-m|Les petits pas sont couchés, papa.",
            "papa|Toi tu tapais, moi je comptais.",
            "maman|Le wagon a sa place, maintenant.",
            "narrateur|Le quai a laissé le fer, derrière.",
            "narrateur|Le sac bleu garde une boucle tiède, près de l'épaule.",
            "enfant-m|Bonjour, lac.",
            "narrateur|La boucle du sac bleu tient un fil de suie.",
        ],
        (2, 1, 2): [
            "narrateur|Victorino s'assoit, les roues plus calmes.",
            "enfant-m|J'ai attendu le plancher, d'abord.",
            "papa|Puis les roues sont restées sages.",
            "maman|Tes pieds ont trouvé le banc.",
            "narrateur|L'allée ne danse plus.",
            "narrateur|Le sac bleu garde une boucle tiède, près de l'épaule.",
            "enfant-m|À tout à l'heure, les rails.",
            "narrateur|Un battement de roue berce le sac, contre le banc.",
        ],
        (2, 1, 3): [
            "narrateur|Victorino s'assoit, la main de papa tout près.",
            "enfant-m|Tu tenais le rail.",
            "papa|Vous avez demandé, et ça tenait.",
            "maman|Sa main a fait le chemin.",
            "narrateur|Le wagon rend le silence.",
            "narrateur|Le sac bleu garde une boucle tiède, près de l'épaule.",
            "enfant-m|Le lac est à nous.",
            "narrateur|L'épaule de papa garde la chaleur du sac.",
        ],
        (2, 2, 1): [
            "narrateur|Victorino s'assoit au bout des arbres.",
            "enfant-m|Toi tu comptais, moi je pointais.",
            "papa|Tes doigts ont fait le pré.",
            "maman|La vitre est devenue un lac.",
            "narrateur|Le verre redevient froid.",
            "narrateur|Le sac bleu garde une boucle tiède, près de l'épaule.",
            "enfant-m|Les arbres restent, maman.",
            "narrateur|Un pré déplié reste collé au bleu du sac.",
        ],
        (2, 2, 2): [
            "narrateur|Victorino s'assoit, le jour revenu.",
            "papa|J'ai compté le noir, puis c'était toi.",
            "enfant-m|J'ai attendu le tunnel.",
            "maman|Chacun son tour, sur la vitre.",
            "narrateur|Le lac tient, enfin.",
            "narrateur|Le sac bleu garde une boucle tiède, près de l'épaule.",
            "enfant-m|Bonjour, vitre.",
            "narrateur|Le noir du tunnel a laissé une ombre sur la boucle.",
        ],
        (2, 2, 3): [
            "narrateur|Victorino s'assoit, tenu par maman.",
            "enfant-m|Tu tenais, tout près.",
            "papa|Les bras ont fait la rambarde.",
            "maman|La fenêtre est à vous.",
            "narrateur|Le verre a rendu le calme.",
            "narrateur|Le sac bleu garde une boucle tiède, près de l'épaule.",
            "enfant-m|Regarde, papa, il brille.",
            "narrateur|Le souffle de maman fait un nuage sur le bleu.",
        ],
        (2, 3, 1): [
            "narrateur|Victorino s'assoit devant la tablette.",
            "enfant-m|La pomme est sage, papa.",
            "papa|Tu la posais, puis tu t'arrêtais.",
            "maman|La table a son goûter, maintenant.",
            "narrateur|Le bois est redevenu plat.",
            "narrateur|Le sac bleu garde une boucle tiède, près de l'épaule.",
            "enfant-m|La pomme se tait.",
            "narrateur|La pomme cale le sac, une bosse ronde.",
        ],
        (2, 3, 2): [
            "narrateur|Victorino s'assoit, la tablette plus calme.",
            "enfant-m|On a attendu le bois.",
            "papa|Quand il s'est tu, tu as posé.",
            "maman|La tablette a fait une table.",
            "narrateur|Tes genoux ont trouvé le banc.",
            "narrateur|Le sac bleu ne fait plus aucun bruit.",
            "enfant-m|Il est tiède.",
            "narrateur|Le bois tiède tient la sangle, sans bouger.",
        ],
        (2, 3, 3): [
            "narrateur|Victorino s'assoit, le sac ouvert par papa.",
            "enfant-m|J'écoutais tes mains.",
            "papa|Moi aussi, j'ouvrais avec toi.",
            "maman|Tu as demandé, il a ouvert.",
            "narrateur|La tablette a rendu vos pas.",
            "narrateur|Le sac bleu garde une boucle tiède, près de l'épaule.",
            "enfant-m|Elle est à nous, maman.",
            "narrateur|Papa a ouvert le sac : un coin de lac y brille.",
        ],
        (3, 1, 1): [
            "narrateur|Victorino s'assoit, la pomme contre le banc.",
            "enfant-m|Les petits pas sont couchés, papa.",
            "papa|Toi tu tapais, moi je comptais.",
            "maman|Le wagon a sa place, maintenant.",
            "narrateur|Le quai a laissé le fer, derrière.",
            "narrateur|La pomme garde une peau lisse, un peu tiède.",
            "enfant-m|Bonjour, lac.",
            "narrateur|La pomme roule une fois, puis se tait contre le banc.",
        ],
        (3, 1, 2): [
            "narrateur|Victorino s'assoit, les roues plus calmes.",
            "enfant-m|J'ai attendu le plancher, d'abord.",
            "papa|Puis les roues sont restées sages.",
            "maman|Tes pieds ont trouvé le banc.",
            "narrateur|L'allée ne danse plus.",
            "narrateur|La pomme garde une peau lisse, un peu tiède.",
            "enfant-m|À tout à l'heure, les rails.",
            "narrateur|Un jus minuscule brille, arrêté.",
        ],
        (3, 1, 3): [
            "narrateur|Victorino s'assoit, la main de papa tout près.",
            "enfant-m|Tu tenais le rail.",
            "papa|Vous avez demandé, et ça tenait.",
            "maman|Sa main a fait le chemin.",
            "narrateur|Le wagon rend le silence.",
            "narrateur|La pomme garde une peau lisse, un peu tiède.",
            "enfant-m|Le lac est à nous.",
            "narrateur|La poche de Victorino garde la rondeur froide.",
        ],
        (3, 2, 1): [
            "narrateur|Victorino s'assoit au bout des arbres.",
            "enfant-m|Toi tu comptais, moi je pointais.",
            "papa|Tes doigts ont fait le pré.",
            "maman|La vitre est devenue un lac.",
            "narrateur|Le verre redevient froid.",
            "narrateur|La pomme garde une peau lisse, un peu tiède.",
            "enfant-m|Les arbres restent, maman.",
            "narrateur|Un reflet de pomme danse, minuscule, sur le lac.",
        ],
        (3, 2, 2): [
            "narrateur|Victorino s'assoit, le jour revenu.",
            "papa|J'ai compté le noir, puis c'était toi.",
            "enfant-m|J'ai attendu le tunnel.",
            "maman|Chacun son tour, sur la vitre.",
            "narrateur|Le lac tient, enfin.",
            "narrateur|La pomme garde une peau lisse, un peu tiède.",
            "enfant-m|Bonjour, vitre.",
            "narrateur|Le grain de suie a voyagé près de la pomme.",
        ],
        (3, 2, 3): [
            "narrateur|Victorino s'assoit, tenu par maman.",
            "enfant-m|Tu tenais, tout près.",
            "papa|Les bras ont fait la rambarde.",
            "maman|La fenêtre est à vous.",
            "narrateur|Le verre a rendu le calme.",
            "narrateur|La pomme garde une peau lisse, un peu tiède.",
            "enfant-m|Regarde, papa, il brille.",
            "narrateur|Maman essuie un rond de jus sur la vitre.",
        ],
        (3, 3, 1): [
            "narrateur|Victorino s'assoit devant la tablette.",
            "enfant-m|La pomme est sage, papa.",
            "papa|Tu la posais, puis tu t'arrêtais.",
            "maman|La table a son goûter, maintenant.",
            "narrateur|Le bois est redevenu plat.",
            "narrateur|La pomme garde une peau lisse, un peu tiède.",
            "enfant-m|La pomme se tait.",
            "narrateur|La pomme pèse, poids rond, sur le ticket.",
        ],
        (3, 3, 2): [
            "narrateur|Victorino s'assoit, la tablette plus calme.",
            "enfant-m|On a attendu le bois.",
            "papa|Quand il s'est tu, tu as posé.",
            "maman|La tablette a fait une table.",
            "narrateur|Tes genoux ont trouvé le banc.",
            "narrateur|La pomme ne fait plus aucun bruit.",
            "enfant-m|Il est tiède.",
            "narrateur|Le bois a pris la forme ronde de la pomme.",
        ],
        (3, 3, 3): [
            "narrateur|Victorino s'assoit, le sac ouvert par papa.",
            "enfant-m|J'écoutais tes mains.",
            "papa|Moi aussi, j'ouvrais avec toi.",
            "maman|Tu as demandé, il a ouvert.",
            "narrateur|La tablette a rendu vos pas.",
            "narrateur|La pomme garde une peau lisse, un peu tiède.",
            "enfant-m|Elle est à nous, maman.",
            "narrateur|Le sac ouvert sent la pomme et le lac.",
        ],
    }
    return vet(table[(a, b, c)])


def path_words(mp: dict, a: int, b: int, c: int) -> int:
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
    return sum(words(mp[i]["text"]) for i in ids)


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple] = {}

    scripts["CHK_T0000_P0000"] = (OPENING, "opening", "sifflet,pigeon", {"emphasis": "ticket rouge"})
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "le ticket rouge",
            "option_2_label": "le sac bleu",
            "option_3_label": "la pomme",
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
        scripts[f"{base}_C0001"] = (t1["confirm"], "confirm", t1["sons"], {"emphasis": "lac"})
        scripts[f"{base}_T0002_P0000"] = (
            T2_CHOICE[a],
            "choice",
            "",
            {
                "option_1_label": "l'allée",
                "option_2_label": "la fenêtre",
                "option_3_label": "la tablette",
            },
        )
        for b in (1, 2, 3):
            leaf2 = f"{base}_T0002_P000{b}"
            t2d = T2[(a, b)]
            scripts[leaf2] = (t2d["lines"], "obstacle", t2d["sons"], {"emphasis": t2d["emp"]})
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
                    res(a, b, c),
                    "resolution",
                    "roues,ticket",
                    {"emphasis": "grain de suie"},
                )
                scripts[f"{leaf3}_F0001"] = (
                    fin(a, b, c),
                    "ending",
                    "lac,wagon",
                    {"emphasis": "lac", "note": ending_note(a, b, c)},
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
    t2s = [
        ch["text"]
        for ch in chunks
        if re.search(r"T0002_P000[123]$", ch["chunk_id"])
    ]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"T2 distincts {len(set(t2s))}/9")

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
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "j'ai compris",
        "mission accomplie",
        "hyperactif",
        "ce n'est pas une faute",
        "camarade qui bouge",
        "beaucoup d'énergie",
        "cuisine",
        "jardin",
        "dînette",
        "dinette",
        "les cubes",
        "après la sieste",
        "capitaine",
        "plic",
        "volet jaune",
        "boutique",
        "marelle",
        "carrousel",
        "papillon",
        "portail",
        "il faut attendre",
        "on doit demander",
        "sami",
        "citronnade",
        "grillon",
        "navire",
        "bateau",
        "camp de",
        "sous la lampe",
        "hérisson",
        "renard",
        "châle",
        "cacao",
        "colline",
        "crochet",
        "dent de fermeture",
        "merle",
        "miel",
        "aujourd'hui",
        "tout doux",
        "tout calme",
        "nino",
        "chouchou",
        "amir",
        "aniss",
        "nina",
        "mila",
        "sarah",
        "raphaël",
        "victorina",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TICS.search(blob):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "victorino" not in blob:
        raise SystemExit(f"{SID}: Victorino absent")
    if "grain de suie" not in blob:
        raise SystemExit(f"{SID}: grain de suie absent")
    if "ticket" not in blob:
        raise SystemExit(f"{SID}: ticket absent")
    adults = [ln for ln in blob.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    aj = " ".join(a.split("|", 1)[1] for a in adults)
    if aj.count("merci") + aj.count("bravo") != 1:
        raise SystemExit(f"{SID}: merci/bravo ×{aj.count('merci') + aj.count('bravo')}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in chunks)
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    if any(c.get("text_xai_tags") == c.get("text") for c in chunks):
        raise SystemExit("text_xai_tags = text")
    if len(chunks) != 86:
        raise SystemExit(f"chunks {len(chunks)}≠86")

    mp = {ch["chunk_id"]: ch for ch in chunks}
    ws = [path_words(mp, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]

    out = dict(src)
    out["fil_rouge"] = (
        "Victorino veut garder son ticket rouge, et son grain de suie, jusqu'au lac. "
        "Le sifflet le fait courir trop : le grain glisse. "
        "Il prend d'abord le ticket, le sac bleu ou la pomme ; les trois montent. "
        "Dans l'allée le talon accroche, à la fenêtre une mare trompe, à la tablette ça saute. "
        "Il refuse de foncer. Il dose son élan. Le lac arrive. Le grain reste."
    )
    out["title"] = TITLE
    out["characters"] = "Victorino, papa, maman"
    out["setting"] = "le quai, puis le wagon : allée, fenêtre, tablette"
    out["chunks"] = chunks
    check(SID, out["age_band"], out["chunks"])

    print(f"chemins mots min={min(ws)} max={max(ws)} moy={sum(ws)//len(ws)}")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"""# {SID} — {TITLE}

- **Public :** N2 (4–5 ans), audio familial
- **Leçon :** DIF.ENE.001 — attendre / ne pas tout brûler d'un coup (vécue, jamais dite)
- **Personnages :** Victorino, papa, maman (un seul enfant)
- **Lieu :** le quai, puis le wagon : allée, fenêtre, tablette
- **Structure conservée :** 86 nœuds, graphe, labels, 27 chemins, 27 fins distinctes

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Victorino connaît le quai, ses bancs, son pigeon. Un détail paraît nouveau : un **grain de suie** repose sur le ticket rouge. Mission : garder le ticket jusqu'au lac, le montrer à l'eau. Le sifflet perce. Il court trop, le ticket claque, le grain glisse. Sourire parti. Papa s'accroupit. Merci vécu : tu as ralenti pour le grain.

T1 = ticket rouge / sac bleu / pomme (les trois montent). T2 = allée (talon, pli, roues plus dures) / fenêtre (mare trompeuse, éclair plus large) / tablette (tout poser d'un coup, ça saute plus). T3 = neuf façons de doser l'élan (petits pas, roues, papa tient ; arbres, tunnel, maman tient ; pomme, tablette calme, papa ouvre). Le grain du début est payé. Le lac arrive. Chaque fin porte une trace unique.

Monde ≠ TREE-DIF-051 (Chouchou, gare colline, hérisson/renard), ≠ TREE-AUT-009 (Victorino, sac bleu, salon, crochet), ≠ TREE-DIF-047 (Nino, camp, chambre).

## Vécu

Impatience au sifflet, découragement quand le grain glisse ou l'objet résiste, fierté calme quand il refuse de foncer. L'adulte guide peu, s'accroupit. La leçon se voit : un pied, puis l'autre ; attendre les roues, les arbres, le bois. Jamais dite.

## Vu et corrigé

- Ouverture inventée (quai connu, grain de suie nouveau). Pas « déjà ». Pas les cinq gabarits v2.
- Indice unique : grain de suie, dès l'ouverture, payé au climax.
- Corps : sourire parti, poitrine serrée, adulte à la même hauteur.
- 2e ruse plus maline (rythme des roues, éclair d'eau, tout poser d'un coup). Il refuse de foncer.
- Dénouement qui a failli. 27 fins, 27 dernières images, 27 T3, 9 T2.
- T1 ne retire pas l'équipement. Labels conservés.
- Un merci de papa lié au geste (ralentir pour le grain). Question d'adulte. Un « en ce moment ».
- Tics « encore / déjà / tout doux / tout calme », merle, miel, slogans, 2e enfant : jetés.
- TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending).
- Chemins : {min(ws)}–{max(ws)} mots (moyenne {sum(ws)//len(ws)}). `check()` N2 OK. Pas d'apply.

## Direction vocale

`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, tempo, sourire, respiration. `slow` = choix, indice, fin. Obstacle en `low-pitch`. Fins `soft` / `slow` / `low-pitch`.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins distinctes, 27 dernières images
- {min(ws)} à {max(ws)} mots par chemin (moyenne {sum(ws)//len(ws)})
- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'apply.
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
