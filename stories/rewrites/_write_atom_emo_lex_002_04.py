#!/usr/bin/env python3
"""ATOM-EMO.LEX.002-04 — Raphaël et la tour de cubes (F-NAR-019, N2, EMO.LEX.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.002-04"
TITLE = "Raphaël et la tour de cubes"
N2 = LIMITS["N2"]
CHARS = "Raphaël, papa, maman"
SETTING = (
    "salon, après-midi, cubes, tour, chat, fauteuil, "
    "soleil, bois, pain, bol, pull"
)
INDICE = "éclat de fauteuil"
FIL = (
    "Le chat frotte le dossier, puis s'en va. Sur le tissu, "
    "un éclat de fauteuil luit. Raphaël veut la tour, maintenant. "
    "La queue du chat balaie les cubes. Poitrine trop vite. "
    "Sourire parti. Yeux chauds. Papa s'accroupit. Je suis triste. "
    "Un câlin. Merci vécu. Deuxième ruse : le chat revient, "
    "un cube roule. Il refuse de foncer. Une petite tour "
    "recommence. Un éclat de fauteuil tient sur le tissu."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tapis|canapé|canape|coussin|rideau|plaid|treille|moule|"
    r"tuteur|saladier|gomme|berge|brouette|couverture|capuche|"
    r"paillasson|merle|miel|maîtresse|maitresse|grand-père|"
    r"grand-pere|jardinier|bibliothécaire|bibliothecaire|"
    r"gardienne|mateo)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "maîtresse",
    "maitresse",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai dit",
    "j ai dit",
    "tu as nommé",
    "tu as nomme",
    "c'est de la tristesse",
    "c est de la tristesse",
    "c'est de la joie",
    "pleurer est permis",
    "le câlin aide",
    "le calin aide",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "les trois mots",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "il ne faut pas rire",
    "on ne rit pas",
    "bravo. tu as",
    "tu as dit : je suis",
    "tu as bien demandé",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de cube",
    "éclat de tour",
    "éclat de tapis",
    "éclat de canapé",
    "éclat de canape",
    "éclat de coussin",
    "éclat de treille",
    "éclat de moule",
    "éclat de tuteur",
    "éclat de saladier",
    "éclat de gomme",
    "éclat de berge",
    "éclat de brouette",
    "éclat de couverture",
    "éclat de capuche",
    "éclat de paillasson",
    "éclat de rideau",
    "éclat de plaid",
    "éclat de tissu",
    "éclat de dossier",
    "éclat de bois",
    "éclat de soleil",
    "éclat de chat",
    "éclat de pain",
    "éclat de bol",
    "éclat de pull",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de fauteuil",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis tristesse; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_tour_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Raphaël",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=raphael_a_les_yeux_chauds_que_dit_il; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="câlin",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis soulagement; intensite=2; "
            "destinataire=enfant; sous_texte=il_demande_un_calin_sans_slogan; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de fauteuil",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=chat_revient_cube_roule_il_refuse_de_foncer; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de fauteuil",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_soulagement; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_tissu; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "triste",
    "accepted_examples": "triste | je suis triste | câlin | un câlin | pleurer",
    "retry_prompt": "Raphaël peut demander un câlin. Que dit-il ?",
    "engine_ok_text": "Oui, triste.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "cubes_tombent,chat",
        [
            "narrateur|Le chat frotte le dossier, puis s'en va.",
            "enfant-m|Il part, papa.",
            "papa|Tu l'as vu, le chat ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le dossier du fauteuil reste chaud, sous le soleil.",
            "enfant-m|Il est chaud, maman.",
            "maman|Tu le touches, le dossier ?",
            "enfant-m|Oui.",
            "narrateur|Le tissu sent le soleil d'après-midi.",
            "enfant-m|Ça sent le chaud.",
            "narrateur|Dans la cuisine, le bol du chat tinte.",
            "enfant-m|Il boit, maman.",
            "maman|Tu l'entends, le bol ?",
            "enfant-m|Oui, maman.",
            "narrateur|Des cubes bleus attendent près du fauteuil.",
            "enfant-m|Les bleus et les jaunes !",
            "papa|Tu as tes cubes, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Sur le tissu, un éclat de fauteuil luit.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-m|Oui, un point clair.",
            "papa|Le soleil le touche.",
            "narrateur|Un cube jaune pèse dans sa main.",
            "enfant-m|Il est lisse.",
            "narrateur|En ce moment, Raphaël pose un cube.",
            "enfant-m|Je veux la tour, maintenant !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|Il pose un cube trop vite, trop haut.",
            "enfant-m|Plus haut !",
            "narrateur|Puis un autre, plus haut que le premier.",
            "enfant-m|Elle est haute, papa.",
            "papa|Elle est haute, oui.",
            "narrateur|La tour penche un peu vers le fauteuil.",
            "enfant-m|Elle tient !",
            "maman|Tes mains vont trop vite, Raphaël ?",
            "enfant-m|Un peu.",
            "narrateur|Le chat revient du bol, tout près.",
            "narrateur|Sa queue balaie le bas de la tour.",
            "narrateur|Les cubes tombent sur le bois.",
            "enfant-m|Ma tour !",
            "narrateur|Ils font un bruit sourd, près des pieds.",
            "narrateur|Raphaël reste surpris, les mains ouvertes.",
            "narrateur|Sa gorge se serre d'un coup.",
            "enfant-m|Oh.",
            "narrateur|Ses yeux deviennent chauds.",
            "narrateur|Une larme tombe sur le bois.",
            "enfant-m|Je suis triste.",
            "narrateur|Raphaël pleure un peu, sans crier.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se heurtent.",
            "papa|Tu as les yeux chauds, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Sa poitrine va trop vite.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "enfant-m|Je veux un câlin.",
            "papa|Viens.",
            "narrateur|Papa ouvre les bras, tout près du fauteuil.",
            "narrateur|Raphaël se blottit contre papa.",
            "narrateur|Le câlin est chaud, près du cou.",
            "enfant-m|Ton pull sent le pain.",
            "narrateur|L'éclat de fauteuil tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Raphaël a les yeux chauds.",
            "narrateur|Que dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Raphaël reste contre papa, un moment.",
            "enfant-m|La tour, maintenant.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-m|Je la refais.",
            "narrateur|Raphaël avance les mains, trop vite.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Raphaël refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle, près du fauteuil.",
            "narrateur|Il observe les cubes, un instant.",
            "enfant-m|Ils sont par terre.",
            "papa|Tu restes un peu, Raphaël ?",
            "enfant-m|Oui, papa.",
            "papa|Merci, Raphaël.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le câlin est tiède, sous les bras.",
            "enfant-m|Il est chaud.",
            "narrateur|La poitrine de Raphaël ralentit un peu.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près des cubes ?",
            "enfant-m|Oui.",
            "narrateur|Maman essuie une larme du pouce.",
            "maman|Le soleil touche le dossier ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le ventre de Raphaël se desserre.",
            "papa|On pose un cube, sans se presser ?",
            "enfant-m|Oui, papa.",
            "narrateur|Raphaël tient le pull de papa.",
            "enfant-m|Je reste un peu.",
            "narrateur|Ils se baissent, sans se bousculer.",
            "enfant-m|Un bleu, papa.",
            "papa|On le pose, sans se presser.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "chat,cubes",
        [
            "narrateur|Maman pousse un cube bleu près du bois.",
            "narrateur|Le bois est un peu poudreux.",
            "enfant-m|La tour, maintenant !",
            "narrateur|Raphaël prend trop de cubes, tout de suite.",
            "narrateur|Un cube jaune glisse de sa main.",
            "enfant-m|Il glisse !",
            "narrateur|Le cube continue de rouler vers le fauteuil.",
            "enfant-m|Il roule !",
            "narrateur|Le chat revient vers les cubes.",
            "narrateur|Sa queue passe tout près du bois.",
            "enfant-m|Le chat !",
            "narrateur|La petite tour penche vers le dossier.",
            "narrateur|Raphaël avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Raphaël refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "enfant-m|J'attends.",
            "narrateur|Il observe les cubes, un instant.",
            "narrateur|Il écoute le salon, près du fauteuil.",
            "narrateur|Sur le tissu, un éclat de fauteuil luit.",
            "enfant-m|Là, sur le tissu.",
            "papa|On tient le cube ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le cube jaune s'arrête contre le dossier.",
            "narrateur|Raphaël le prend, sans se presser.",
            "enfant-m|Il est lisse.",
            "papa|Le chat reste près de nous ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le chat s'assoit, loin des cubes.",
            "enfant-m|Il regarde.",
            "maman|Tu poses le cube, Raphaël ?",
            "enfant-m|Oui, maman.",
            "narrateur|Papa pose un cube bleu.",
            "papa|Un cube pour toi.",
            "narrateur|Raphaël pose un cube jaune.",
            "enfant-m|Un cube pour moi.",
            "narrateur|Une petite tour recommence, près du fauteuil.",
            "enfant-m|Elle est petite.",
            "papa|Elle est petite, à nous.",
            "papa|Tu vois le point, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les cubes tiennent, l'un sur l'autre.",
            "enfant-m|C'est plus facile.",
            "papa|On reste ici, Raphaël ?",
            "enfant-m|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "chat",
        [
            "narrateur|Ils restent près du fauteuil.",
            "narrateur|Maman essuie un peu de bois.",
            "enfant-m|Les cubes sont tombés, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, près de la tour.",
            "narrateur|Raphaël tapote le tissu du doigt.",
            "enfant-m|Il a une trace de soleil.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|La petite tour est restée, Raphaël.",
            "enfant-m|Oui, avec les cubes.",
            "narrateur|Ça sent le pain, un peu tiède.",
            "enfant-m|Et le bois, maman.",
            "papa|Le salon est doux, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le chat se couche au soleil, loin des cubes.",
            "enfant-m|Il dort.",
            "papa|On laisse la tour, Raphaël ?",
            "enfant-m|Oui, tout près.",
            "narrateur|La petite tour reste près du fauteuil.",
            "narrateur|Un éclat de fauteuil tient sur le tissu.",
        ],
    ),
}


def vet(lines: list[str], cid: str = "") -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    skip_lesson = cid == "CHK_T0000_P0000_Q0001"
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
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        if not skip_lesson:
            for bad in EXTRA_BAD:
                if bad in low:
                    raise SystemExit(f"extra {bad}: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-m"):
            raise SystemExit(f"rôle {role}: {raw}")
        tok = ph.split()[0].lower() if role == "narrateur" else ""
        starts.append(tok)
        out.append(f"{role}|{ph}")
    run = 1
    for i in range(1, len(starts)):
        if starts[i] and starts[i] == starts[i - 1]:
            run += 1
            if run >= 4:
                raise SystemExit(f"puces {starts[i]}")
        else:
            run = 1
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
    cid = src.get("chunk_id") or ""
    lines = vet(lines, cid)
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if extra.get("note"):
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
    out["night_policy"] = extra.get("night_policy", "play")
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    out.update(extra.get("fields") or {})
    return out


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in SCRIPTS]
    extra = set(SCRIPTS) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{SID} chunks missing={missing} extra={extra}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        profile, sons, lines = SCRIPTS[cid]
        extra_kw: dict = {}
        if cid == "CHK_T0000_P0000_Q0001":
            extra_kw["pause_before_ms"] = 200
            extra_kw["fields"] = Q_FIELDS
        elif cid != "CHK_T0000_P0000":
            extra_kw["pause_before_ms"] = 200
            extra_kw["fields"] = {
                "expected_answer": None,
                "accepted_examples": None,
                "retry_prompt": None,
            }
        by[cid] = voice(c, lines, profile, sons, extra_kw)
        if c.get("kind") != by[cid].get("kind"):
            raise SystemExit(f"{cid}: kind changé")
    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    adults = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
    ).lower()
    if adults.count("merci") != 1:
        raise SystemExit(f"{SID}: merci ×{adults.count('merci')}")
    if "bravo" in adults:
        raise SystemExit(f"{SID}: bravo en trop")
    if "c'est trop" in adults or "c est trop" in adults:
        raise SystemExit(f"{SID}: refrain adulte c'est trop")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Raphaël = enfant-m)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé (dump sans camarade)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    if "mateo" in blob:
        raise SystemExit(f"{SID}: Mateo du dump")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "enfant-m" for r in roles):
        raise SystemExit(f"{SID}: enfant-m absent")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "pleurer est permis",
        "le câlin aide",
        "le calin aide",
        "c'est de la tristesse",
        "c est de la tristesse",
        "j'ai dit",
        "j ai dit",
        "tu as nommé",
        "tu as nomme",
        "l'histoire est finie",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Raphaël a les yeux chauds. Que dit-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "triste":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "triste | je suis triste | câlin | un câlin | pleurer"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Raphaël peut demander un câlin. Que dit-il ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    for c in chunks:
        if c["chunk_id"] == "CHK_T0000_P0000_Q0001":
            continue
        if c.get("expected_answer") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: expected hors Q")
        if c.get("accepted_examples") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: accepted hors Q")
        if c.get("retry_prompt") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: retry hors Q")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "je suis triste" not in opening:
        raise SystemExit(f"{SID}: nommage absent avant la question")
    n_triste = blob.count("je suis triste")
    if n_triste != 1:
        raise SystemExit(f"{SID}: je suis triste ×{n_triste}")
    if "câlin" not in opening and "calin" not in opening:
        raise SystemExit(f"{SID}: câlin absent avant la question")
    if "s'accroupit" not in opening and "s accroupit" not in opening:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    if "sourire" not in opening:
        raise SystemExit(f"{SID}: manque sourire parti")
    if "poitrine" not in opening:
        raise SystemExit(f"{SID}: manque poitrine")
    if "salon" not in blob:
        raise SystemExit(f"{SID}: manque salon")
    if "cube" not in blob:
        raise SystemExit(f"{SID}: manque cube")
    if "tour" not in blob:
        raise SystemExit(f"{SID}: manque tour")
    if "chat" not in blob:
        raise SystemExit(f"{SID}: manque chat")
    if "fauteuil" not in blob:
        raise SystemExit(f"{SID}: manque fauteuil")
    if "rideau" in opening:
        raise SystemExit(f"{SID}: ouverture dump (rideau)")
    end_txt = by["CHK_T0000_P0000_END"]["text"].lower()
    if "chat" not in end_txt:
        raise SystemExit(f"{SID}: manque 2e ruse (chat)")
    if "roule" not in end_txt:
        raise SystemExit(f"{SID}: manque 2e ruse (cube qui roule)")
    if "petite tour" not in end_txt:
        raise SystemExit(f"{SID}: manque petite tour")
    if "refuse de foncer" not in end_txt:
        raise SystemExit(f"{SID}: manque refuse de foncer au 2e imprévu")
    for ban in (
        "éclat de cube",
        "éclat de tour",
        "éclat de tapis",
        "éclat de canapé",
        "éclat de canape",
        "éclat de coussin",
        "éclat de treille",
        "éclat de moule",
        "éclat de tuteur",
        "éclat de saladier",
        "éclat de gomme",
        "éclat de berge",
        "éclat de brouette",
        "éclat de couverture",
        "éclat de capuche",
        "éclat de paillasson",
        "tout doux",
        "tout calme",
        "tout doucement",
        "merle",
        "miel",
        "mateo",
        "pleurer est permis",
        "j'ai dit",
    ):
        if ban in blob:
            raise SystemExit(f"{SID}: BAN {ban}")
    tts_ok = all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_xai_tags"] != c["text"]
        and c["text_ssml"].startswith("<speak>")
        for c in chunks
    )
    if not tts_ok:
        raise SystemExit(f"{SID}: TTS incomplet")
    nwords = sum(words(c["text"]) for c in chunks)
    if not (700 <= nwords <= 850):
        raise SystemExit(f"{SID}: {nwords} mots hors 700-850")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N2 (≤15 mots/phrase), audio familial, voc 4–5 ans\n"
        "- **Leçon :** EMO.LEX.002 — nommer la tristesse + câlin "
        "(vécue : cubes tombent, gorge serrée, yeux chauds, sourire parti, "
        "papa accroupi, Raphaël dit je suis triste, pleure, demande un "
        "câlin, pull de papa sent le pain ; 2e ruse : chat revient, cube "
        "qui roule, il refuse de foncer, petite tour recommence). "
        "JAMAIS dite dans le récit. Pas « pleurer est permis ». Pas "
        "« le câlin aide ». Pas « j'ai dit : je suis ».\n"
        "- **Personnages :** Raphaël, papa, maman. Dump Mateo → D16 "
        "Raphaël = enfant-m (veut la tour maintenant). Chat du dump = "
        "imprévu. Pas de copain. Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** salon, après-midi, cubes, tour, chat, fauteuil, "
        "soleil, bois, pain, bol, pull. BAN tapis / canapé / coussin / "
        "rideau. Cubes / tour / chat = dump. ≠ dump rideau / tapis.\n"
        "- **Indice unique :** éclat de fauteuil (luit à l'ouverture → "
        "tremble aux larmes → luit quand le chat revient et le cube "
        "roule → tient sur le tissu). BAN éclat de cube / tour / tapis / "
        "canapé / coussin / treille / moule / tuteur / saladier / gomme / "
        "berge / brouette / couverture / capuche / paillasson.\n"
        "- **Question moteur :** « Raphaël a les yeux chauds. Que "
        "dit-il ? » expected dump **triste**. accepted dump "
        "`triste | je suis triste | câlin | un câlin | pleurer`. "
        "retry dump Mateo → Raphaël. Non récitée dans les autres "
        "chunks. Hors Q : expected / accepted / retry = null.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le chat frotte le dossier, puis s'en va. Le tissu du fauteuil "
        "sent le soleil d'après-midi. Sur le tissu, un éclat de fauteuil "
        "luit. Cubes bleus et jaunes. Raphaël veut la tour **maintenant**. "
        "Il pose trop vite, trop haut. Le chat revient du bol. Sa queue "
        "balaie. Les cubes tombent. Gorge serrée. Yeux chauds. Sourire "
        "parti. Papa s'accroupit. Je suis triste. Un câlin. Merci vécu. "
        "Deuxième ruse : cube qui roule, chat qui revient. Il s'arrête, "
        "lit l'éclat. Une petite tour recommence. Un éclat de fauteuil "
        "tient sur le tissu.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon, après-midi, fauteuil chaud, bol du chat, "
        "cubes bleus et jaunes. BAN tapis / canapé / coussin / rideau.\n"
        "- Désir : empiler la tour, maintenant.\n"
        "- Objet : cubes, puis tour qui tombe, puis petite tour.\n"
        "- Indice unique : éclat de fauteuil, vu dès l'ouverture, payé "
        "sur le tissu. Pas éclat de cube / tour / tapis / canapé / "
        "coussin.\n"
        "- Urgence douce : il pose trop vite, trop haut.\n"
        "- Imprévu 1 : queue du chat, cubes par terre, poitrine trop "
        "vite, sourire parti, larmes.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le câlin.\n"
        "- Imprévu 2 (plus rusé) : cube qui roule vers le fauteuil, "
        "chat qui revient, petite tour qui penche.\n"
        "- Résolution : il refuse de foncer, observe, écoute le salon, "
        "retrouve l'éclat, pose sans se presser.\n"
        "- Retour : petite tour près du fauteuil, chat au soleil, éclat "
        "sur le tissu. Dénouement qui a failli : le cube roulait, le "
        "chat revenait.\n\n"
        "## Vécu\n\n"
        "Raphaël veut la tour **maintenant**. Impatience, puis cubes par "
        "terre, sourire parti. Il dit je suis triste, pleure, demande un "
        "câlin. Papa ouvre les bras. Le pull sent le pain. Papa se baisse, "
        "pose une question, ne récite pas la règle. Chat revient, cube "
        "roule. Il refuse de foncer. Petite tour. Merci vécu. Fin : "
        "l'éclat du début tient sur le tissu.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Raphaël et la tour de cubes (noyau dump). Relance : "
        "Que dit-il ? expected triste.\n"
        "- Lieu du dump-meta (salon, après-midi). Maman et papa. "
        "Raphaël = héros enfant-m. Chat du dump = imprévu. Dump Mateo "
        "retiré.\n"
        "- Ouverture inventée (chat qui frotte le dossier, puis s'en va), "
        "pas un gabarit v2, pas « Le rideau se lève », pas « joue au "
        "salon ».\n"
        "- Indice unique : éclat de fauteuil. BAN éclat de cube / tour / "
        "tapis / canapé / coussin / treille / moule / tuteur / saladier / "
        "gomme / berge / brouette / couverture / capuche / paillasson. "
        "Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doucement » du dump.\n"
        "- Leçon non dite : on la voit quand les yeux sont chauds, "
        "quand il dit je suis triste, quand il demande un câlin, quand "
        "papa ouvre les bras. Pas « pleurer est permis ». Pas « le câlin "
        "aide ». Pas « j'ai dit : je suis ». Pas « Bravo, Raphaël ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Raphaël a les yeux chauds. Que dit-il ? ». "
        "expected triste. 5 chunks, kinds inchangés. expected/accepted "
        "dump conservés. retry Mateo → Raphaël. Hors Q : null.\n"
        "- example4 064 / 096 / 028 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N2 / raw.js.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers le chat et le cube qui roule.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")


if __name__ == "__main__":
    main()
