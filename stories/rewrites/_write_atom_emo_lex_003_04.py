#!/usr/bin/env python3
"""ATOM-EMO.LEX.003-04 — Le moulinet de Mila (F-NAR-019, N3, EMO.LEX.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.003-04"
TITLE = "Le moulinet de Mila"
N3 = LIMITS["N3"]
CHARS = "Mila, papa, maman"
SETTING = (
    "marché puis jardin, stand des ailes, table de bois, "
    "miel, moulinet, farine, pain, ficelle, vent"
)
INDICE = "éclat de ficelle"
FIL = (
    "Les pièces cliquettent. Le sac de pain craque. Sur le bois, "
    "un éclat de ficelle luit. Mila veut le cerf-volant bleu, maintenant. "
    "Plus d'aile. Épaules basses. Sourire parti. Papa s'accroupit. "
    "Je suis déçue. Un moulinet jaune. Merci vécu. Deuxième ruse : "
    "plus de farine au jardin. Elle refuse de foncer. Tartines au miel. "
    "Un éclat de ficelle tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(cagette|kiosque|étal|etal|citron|pelle|paillasson|fauteuil|"
    r"coffre|haie|housse|capuche|couverture|tapis|canapé|canape|"
    r"coussin|rideau|plaid|merle|maîtresse|maitresse|grand-père|"
    r"grand-pere|jardinier|bibliothécaire|bibliothecaire|"
    r"gardienne|cléa|clea)\b",
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
    "c'est de la joie",
    "c est de la joie",
    "ce n'est pas honteux",
    "ce n est pas honteux",
    "on nomme",
    "un souhait peut attendre",
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
    "lumière couleur de miel",
    "lumiere couleur de miel",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de farine",
    "éclat de miel",
    "éclat de cagette",
    "éclat de kiosque",
    "éclat d'étal",
    "éclat d'etal",
    "éclat de citron",
    "éclat de pelle",
    "éclat de paillasson",
    "éclat de fauteuil",
    "éclat de coffre",
    "éclat de haie",
    "éclat de housse",
    "éclat de capuche",
    "éclat de couverture",
    "éclat de stand",
    "éclat de pain",
    "éclat de moulinet",
    "éclat de cerf",
    "éclat de table",
    "éclat de bois",
    "éclat de pot",
    "éclat de pale",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de ficelle",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis déception; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_cerf_volant_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Mila",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_cerf_volant_n_est_plus_la_que_dit_mila; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="moulinet",
        note=(
            "arc=résolution; intention=faire_vivre_l_autre_idée; "
            "emotion=retenue puis soulagement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_prend_le_moulinet_sans_slogan; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de ficelle",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=plus_de_farine_elle_refuse_de_foncer_tartines; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de ficelle",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_soulagement; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "déçu",
    "accepted_examples": (
        "déçu | déçue | je suis déçue | autre idée | un moulinet | une autre idée"
    ),
    "retry_prompt": "Mila cherche une autre idée. Que dit-elle d'abord ?",
    "engine_ok_text": "Oui, déçu.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "marche,vent",
        [
            "narrateur|Les pièces de papa cliquettent dans sa paume.",
            "enfant-f|Ça fait tic, papa.",
            "papa|Tu entends les pièces, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le sac de pain de maman craque contre la joue.",
            "enfant-f|Il est chaud, maman.",
            "maman|Tu le sens, le pain ?",
            "enfant-f|Oui, il sent le chaud.",
            "narrateur|Le vent du marché tire une ficelle blanche.",
            "enfant-f|Elle danse, maman.",
            "maman|Elle tape le clou, tu vois ?",
            "enfant-f|Oui, un petit tic.",
            "narrateur|Sur le bois, un éclat de ficelle luit.",
            "enfant-f|Il brille, papa.",
            "papa|Le soleil le touche.",
            "enfant-f|Un point clair.",
            "narrateur|Des pots de miel attendent, collants et lourds.",
            "enfant-f|Ça sent le sucré.",
            "maman|Tu veux un doigt de miel ?",
            "enfant-f|Un tout petit, maman.",
            "narrateur|Mila pose un doigt sur le pot ouvert.",
            "narrateur|Le miel file, lent, sur la peau.",
            "enfant-f|Il colle.",
            "papa|Il est épais, oui.",
            "narrateur|Une pale de papier tremble, loin, au-dessus.",
            "enfant-f|C'est bleu, papa.",
            "papa|Tu le vois, là-haut ?",
            "enfant-f|Oui, ça danse.",
            "narrateur|En ce moment, Mila cherche le bleu du ciel.",
            "enfant-f|Le cerf-volant, maintenant !",
            "papa|Celui qui danse, là-haut ?",
            "enfant-f|Oui, le bleu, papa.",
            "narrateur|Ils marchent vers le stand des ailes.",
            "enfant-f|Je le prends, maman.",
            "maman|On va demander, Mila ?",
            "enfant-f|Oui, tout de suite.",
            "narrateur|Le stand est presque vide, sous le vent.",
            "narrateur|Il reste des ficelles, pas d'aile bleue.",
            "papa|Il n'y en a plus, Mila.",
            "enfant-f|Plus de bleu ?",
            "narrateur|Mila reste surprise, les mains ouvertes.",
            "narrateur|Ses épaules tombent d'un coup.",
            "narrateur|Sa gorge se serre, près du stand.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et l'inquiétude se heurtent.",
            "papa|Tu as les épaules basses, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "maman|Tes mains sont chaudes, Mila ?",
            "enfant-f|Un peu, maman.",
            "enfant-f|Je suis déçue.",
            "narrateur|Un moulinet jaune tourne sur la table.",
            "narrateur|Ses pales font un petit cliquetis.",
            "enfant-f|Celui-là, alors.",
            "narrateur|L'éclat de ficelle tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Le cerf-volant n'est plus là.",
            "narrateur|Que dit Mila ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "moulinet",
        [
            "narrateur|Mila reste près du stand, un moment.",
            "enfant-f|Le bleu n'est plus là.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Je veux le jaune, alors.",
            "narrateur|Mila avance la main, trop vite.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Elle referme la bouche, près des pales.",
            "narrateur|Personne ne parle, sous le vent.",
            "narrateur|Elle observe le moulinet, un instant.",
            "enfant-f|Il tourne, papa.",
            "papa|Tu le prends, Mila ?",
            "enfant-f|Oui, une autre idée.",
            "papa|Merci, Mila.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Les pales sont jaunes, Mila ?",
            "enfant-f|Oui, maman.",
            "narrateur|Papa donne une pièce au stand.",
            "narrateur|Le moulinet passe dans la main de Mila.",
            "enfant-f|Il est léger.",
            "papa|Tu le sens, le vent ?",
            "enfant-f|Oui, papa.",
            "maman|On rentre au jardin, Mila ?",
            "enfant-f|Oui, avec le jaune.",
            "narrateur|Le ventre de Mila se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On marche, sans se presser ?",
            "enfant-f|Oui.",
            "narrateur|Le sac de pain tape la hanche de maman.",
            "enfant-f|Le pain est chaud.",
            "maman|Il sent le four, Mila ?",
            "enfant-f|Oui, maman.",
            "papa|Le jaune tourne contre le ciel ?",
            "enfant-f|Oui, papa.",
            "narrateur|Une pale cliquette contre le pouce.",
            "enfant-f|Ça chatouille.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "placard",
        [
            "narrateur|Au jardin, la table de bois est tiède.",
            "enfant-f|Le gâteau au miel, maintenant !",
            "narrateur|Mila court vers le placard, trop vite.",
            "enfant-f|La farine, papa !",
            "papa|Je l'ouvre, le placard.",
            "narrateur|Papa ouvre le placard, près de l'eau.",
            "narrateur|Le sachet de farine est plat, vide.",
            "papa|Il n'y a plus de farine.",
            "enfant-f|Plus de gâteau ?",
            "narrateur|Mila avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Mila refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "enfant-f|J'attends.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le moulinet, un instant.",
            "narrateur|Elle écoute le jardin, près de la table.",
            "narrateur|Sur le bois, un éclat de ficelle luit.",
            "enfant-f|Là, sur le bois.",
            "papa|Tu vois le point, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|La ficelle du moulinet brille au soleil.",
            "enfant-f|C'est la même, maman.",
            "maman|Tu la reconnais ?",
            "enfant-f|Oui, du marché.",
            "narrateur|Mila regarde le pot de miel.",
            "enfant-f|Des tartines, alors.",
            "maman|Le pain du sac, Mila ?",
            "enfant-f|Oui, maman.",
            "papa|On tartine, sans se presser ?",
            "enfant-f|Oui, papa.",
            "narrateur|Maman pose le pain sur le bois.",
            "narrateur|Le miel file, lent, sur la tartine.",
            "enfant-f|Il colle aux doigts.",
            "maman|Il est sucré, Mila ?",
            "enfant-f|Oui, maman.",
            "papa|Le jaune tourne près du pot ?",
            "enfant-f|Oui, tout près.",
            "narrateur|Une miette reste collée au pouce de Mila.",
            "enfant-f|Elle est sucrée.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "moulinet",
        [
            "narrateur|Ils restent près de la table.",
            "narrateur|Maman essuie un peu de miel.",
            "enfant-f|Le bleu n'était plus là, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-f|Oui, près du stand.",
            "maman|On est bien, ici.",
            "narrateur|Mila tapote une pale du doigt.",
            "enfant-f|Elle a une trace de miel.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|Le moulinet est resté, Mila.",
            "enfant-f|Oui, avec le jaune.",
            "narrateur|Ça sent le pain, un peu tiède.",
            "enfant-f|Et le miel, maman.",
            "maman|Oui, dans l'air.",
            "papa|Le jardin est doux, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le moulinet reste près du pot.",
            "enfant-f|Il tourne, tout seul.",
            "papa|On laisse le jaune, Mila ?",
            "enfant-f|Oui, tout près.",
            "narrateur|Un éclat de ficelle tient sur le bois.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-f"):
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
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Mila = enfant-f)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé (dump sans camarade)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    if "cléa" in blob or "clea" in blob:
        raise SystemExit(f"{SID}: Cléa du dump")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "enfant-f" for r in roles):
        raise SystemExit(f"{SID}: enfant-f absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "j'ai dit",
        "j ai dit",
        "tu as nommé",
        "tu as nomme",
        "on nomme",
        "ce n'est pas honteux",
        "un souhait peut attendre",
        "l'histoire est finie",
        "lumière couleur de miel",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Le cerf-volant n'est plus là. Que dit Mila ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "déçu":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "déçu | déçue | je suis déçue | autre idée | un moulinet | une autre idée"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Mila cherche une autre idée. Que dit-elle d'abord ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    if "cléa" in retry.lower() or "clea" in retry.lower():
        raise SystemExit(f"{SID}: retry Cléa")
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
    if "je suis déçue" not in opening:
        raise SystemExit(f"{SID}: nommage absent avant la question")
    n_decue = blob.count("je suis déçue")
    if n_decue != 1:
        raise SystemExit(f"{SID}: je suis déçue ×{n_decue}")
    if "moulinet" not in opening:
        raise SystemExit(f"{SID}: moulinet absent avant la question")
    if "s'accroupit" not in opening and "s accroupit" not in opening:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    if "sourire" not in opening:
        raise SystemExit(f"{SID}: manque sourire parti")
    if "poitrine" not in opening:
        raise SystemExit(f"{SID}: manque poitrine")
    if "marché" not in blob and "marche" not in blob:
        raise SystemExit(f"{SID}: manque marché")
    if "jardin" not in blob:
        raise SystemExit(f"{SID}: manque jardin")
    if "cerf-volant" not in blob and "cerf volant" not in blob:
        raise SystemExit(f"{SID}: manque cerf-volant")
    if "miel" not in blob:
        raise SystemExit(f"{SID}: manque miel (objet dump)")
    if "farine" not in blob:
        raise SystemExit(f"{SID}: manque farine")
    if "tartine" not in blob:
        raise SystemExit(f"{SID}: manque tartines")
    end_txt = by["CHK_T0000_P0000_END"]["text"].lower()
    if "farine" not in end_txt:
        raise SystemExit(f"{SID}: manque 2e ruse (farine)")
    if "tartine" not in end_txt:
        raise SystemExit(f"{SID}: manque tartines au 2e imprévu")
    if "refuse de foncer" not in end_txt:
        raise SystemExit(f"{SID}: manque refuse de foncer au 2e imprévu")
    if INDICE not in end_txt:
        raise SystemExit(f"{SID}: indice non payé au climax")
    for ban in (
        "éclat de farine",
        "éclat de miel",
        "éclat de cagette",
        "éclat de kiosque",
        "éclat de citron",
        "éclat de pelle",
        "éclat de paillasson",
        "éclat de fauteuil",
        "éclat de coffre",
        "éclat de haie",
        "éclat de housse",
        "éclat de capuche",
        "éclat de couverture",
        "tout doux",
        "tout calme",
        "tout doucement",
        "merle",
        "cléa",
        "j'ai dit",
        "lumière couleur de miel",
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
        "- **Public :** N3 (≤16 mots/phrase), audio familial, voc 5–6 ans\n"
        "- **Leçon :** EMO.LEX.003 — nommer la déception + autre idée "
        "(vécue : plus de cerf-volant bleu, épaules basses, gorge serrée, "
        "sourire parti, papa accroupi, Mila dit je suis déçue, choisit le "
        "moulinet jaune ; 2e ruse : plus de farine au jardin, elle refuse "
        "de foncer, tartines au miel). JAMAIS dite dans le récit. Pas "
        "« j'ai dit : je suis ». Pas « tu as nommé ». Pas « ce n'est pas "
        "honteux ». Pas « on nomme : déçue ».\n"
        "- **Personnages :** Mila, papa, maman. Dump Cléa → D16 Mila = "
        "enfant-f (veut le cerf-volant maintenant). Dump papa + maman "
        "ajoutée (check papa/maman parlent). Pas de copain. Troupe D16. "
        "Pas de maîtresse.\n"
        "- **Lieu :** marché puis jardin (2 lieux). Stand des ailes, "
        "table de bois. Cerf-volant / moulinet / farine / miel = dump. "
        "Miel = tartines (objet), pas le tic « lumière couleur de miel ». "
        "BAN cagette / kiosque / étal / citron.\n"
        "- **Indice unique :** éclat de ficelle (luit à l'ouverture → "
        "tremble quand le bleu manque → luit au jardin, plus de farine → "
        "tient sur le bois). BAN éclat de farine / miel / cagette / "
        "kiosque / étal / citron / pelle / paillasson / fauteuil / coffre "
        "/ haie / housse / capuche / couverture.\n"
        "- **Question moteur :** « Le cerf-volant n'est plus là. Que "
        "dit Mila ? » expected dump **déçu**. accepted dump "
        "`déçu | déçue | je suis déçue | autre idée | un moulinet | "
        "une autre idée`. retry dump Cléa → Mila. Non récitée dans les "
        "autres chunks. Hors Q : expected / accepted / retry = null.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Les pièces de papa cliquettent. Le sac de pain craque. Le vent "
        "tire une ficelle blanche. Sur le bois, un éclat de ficelle luit. "
        "Miel collant. Mila veut le cerf-volant bleu **maintenant**. Le "
        "stand est vide. Épaules. Gorge. Sourire parti. Papa s'accroupit. "
        "Je suis déçue. Un moulinet jaune. Merci vécu. Deuxième ruse : "
        "sachet de farine plat. Elle s'arrête, lit l'éclat. Tartines au "
        "miel. Un éclat de ficelle tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : marché, pièces, sac de pain, ficelle au clou, pots "
        "de miel. Puis jardin, table de bois.\n"
        "- Désir : le cerf-volant bleu, maintenant.\n"
        "- Objet : cerf-volant manquant, puis moulinet jaune, puis "
        "tartines au miel.\n"
        "- Indice unique : éclat de ficelle, vu dès l'ouverture, payé "
        "sur le bois. Pas éclat de farine / miel / cagette.\n"
        "- Urgence douce : elle veut le bleu tout de suite.\n"
        "- Imprévu 1 : plus d'aile, poitrine trop vite, sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le "
        "moulinet.\n"
        "- Imprévu 2 (plus rusé) : plus de farine, gâteau impossible.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le "
        "jardin, retrouve l'éclat, propose des tartines.\n"
        "- Retour : moulinet près du pot, pale à trace de miel, éclat "
        "sur le bois. Dénouement qui a failli : le sachet était vide.\n\n"
        "## Vécu\n\n"
        "Mila veut le bleu **maintenant**. Impatience, puis stand vide, "
        "sourire parti. Elle dit je suis déçue, regarde le moulinet. "
        "Papa se baisse, pose une question, ne récite pas la règle. "
        "Jardin, plus de farine. Elle refuse de foncer. Tartines. Merci "
        "vécu. Fin : l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le moulinet de Mila (noyau dump). Relance : Que dit "
        "Mila ? expected déçu.\n"
        "- Lieu du dump-meta (marché puis jardin). Maman ajoutée et "
        "papa. Mila = héros enfant-f. Dump Cléa retiré.\n"
        "- Ouverture inventée (pièces qui cliquettent, sac de pain), "
        "pas un gabarit v2, pas « Cléa marche au marché ».\n"
        "- Indice unique : éclat de ficelle. BAN éclat de farine / miel "
        "/ cagette / kiosque / étal / citron / pelle / paillasson / "
        "fauteuil / coffre / haie / housse / capuche / couverture. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » du dump. Strip « j'ai dit : je "
        "suis ». Miel objet (tartines) conservé, pas lumière couleur "
        "de miel.\n"
        "- Leçon non dite : on la voit quand les épaules tombent, quand "
        "elle dit je suis déçue, quand elle prend le moulinet, quand "
        "elle propose des tartines. Pas « ce n'est pas honteux ». Pas "
        "« on nomme : déçue ». Pas « Bravo, Mila ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Le cerf-volant n'est plus là. Que dit "
        "Mila ? ». expected déçu. 5 chunks, kinds inchangés. expected/"
        "accepted dump conservés. retry Cléa → Mila. Hors Q : null.\n"
        "- example4 071 / 003 / 035 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N3 / raw.js.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers le placard vide.\n"
        f"- {nwords} mots. N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
