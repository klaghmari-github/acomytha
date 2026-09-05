#!/usr/bin/env python3
"""ATOM-DIF.BES.001-04 — Les cubes de Nino (F-NAR-019, N1, DIF.BES.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.001-04"
TITLE = "Les cubes de Nino"
N1 = LIMITS["N1"]
CHARS = "Nino, papa, maman"
SETTING = (
    "salon. Rayon jaune sur tapis, cube sous canapé, "
    "horloge, pain du goûter"
)
INDICE = "éclat de cube"
FIL = (
    "Un rayon jaune pose un carré sur le tapis. Sur l'arête, un "
    "éclat de cube luit. Nino veut une tour, maintenant, aussi haute "
    "que le canapé. Il prend trop de cubes : clac, la tour tombe. "
    "Le cube jaune roule sous le canapé. Sourire parti. Papa se baisse. "
    "Nino pose un cube, puis un autre. Merci vécu. Sous le canapé, "
    "la main trop vite : le cube glisse. Il refuse de foncer. "
    "Sur l'arête, l'éclat de cube tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(boule|galet|carte|panier|dorure|cloche|corbeille|sac|"
    r"croissant|réverbère|reverbere|bérénice|berenice|clément|"
    r"clement|victorina|béatrice|beatrice|cacao|pâte|pate)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "merle",
    "miel",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "maîtresse",
    "maitresse",
    "j'ai compris",
    "j'ai répété",
    "j'ai repete",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "on peut répéter",
    "on peut repeter",
    "observer d'abord",
    "c'est répéter",
    "c'est repeter",
    "tu as su répéter",
    "tu as su repeter",
    "on a pris le temps",
    "tu as nommé",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "grain de",
    "éclat d'horloge",
    "éclat de horloge",
    "éclat de carte",
    "éclat de boule",
    "éclat de galet",
    "éclat de bois",
    "éclat de volet",
    "éclat de panier",
    "éclat de dorure",
    "éclat de sac",
    "éclat de cloche",
    "point de gouttière",
    "point de gouttiere",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de cube",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_tour_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="calme",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=nino_a_besoin_de_calme_on_peut_repeter; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="cube",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=un_cube_puis_un_autre; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de cube",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis prudence; intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de cube",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_l_arete; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "répéter",
    "accepted_examples": "répéter | observer d'abord | observer | attendre",
    "retry_prompt": "On peut répéter. On peut observer d'abord. Que fait-on ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "cubes,horloge",
        [
            "narrateur|Un rayon jaune pose un carré sur le tapis.",
            "narrateur|Le pied du canapé le coupe.",
            "narrateur|Un cube jaune y reste coincé.",
            "narrateur|Sur l'arête, un éclat de cube luit.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, sur le cube ?",
            "narrateur|Ça sent le pain du goûter.",
            "narrateur|Papa coupe le pain, près de la table.",
            "narrateur|L'horloge fait tic-tac.",
            "narrateur|Le rideau bouge un peu.",
            "narrateur|Un doudou attend sur le canapé.",
            "maman|Tu as vu le cube, Nino ?",
            "enfant-m|Il est sous le canapé.",
            "maman|On le laisse un moment.",
            "narrateur|D'autres cubes sont sur le tapis.",
            "narrateur|Ils sont lisses, un peu froids.",
            "narrateur|Un bleu attend près du pied.",
            "enfant-m|Je veux une tour, maintenant !",
            "enfant-m|Aussi haute que le canapé !",
            "papa|Tu la veux vite ?",
            "enfant-m|Oui, tout de suite !",
            "narrateur|En ce moment, Nino prend trop de cubes.",
            "narrateur|Les cubes glissent entre ses doigts.",
            "narrateur|Ça fait clac, sur le tapis.",
            "narrateur|La tour tombe, trop vite.",
            "narrateur|Le cube jaune roule sous le canapé.",
            "enfant-m|Oh.",
            "narrateur|L'éclat de cube tremble, puis tient.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et l'inquiétude se heurtent.",
            "enfant-m|Ça ne veut pas, papa.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|Tu regardes les cubes ?",
            "enfant-m|Je les veux tous.",
            "maman|Tu les prends trop vite, Nino ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nino serre les mains, trop fort.",
            "narrateur|Ses doigts restent fermés.",
            "narrateur|Son souffle est court.",
            "papa|On regarde un cube ?",
            "enfant-m|Un seul ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "cubes",
        [
            "narrateur|Nino referme la bouche.",
            "narrateur|Il refuse de tout prendre.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe un cube bleu.",
            "narrateur|Il écoute le salon, un instant.",
            "enfant-m|Un cube.",
            "narrateur|Nino pose le cube bleu.",
            "narrateur|Le tapis le tient.",
            "enfant-m|Puis un autre.",
            "narrateur|Il pose un cube rouge.",
            "narrateur|Le même geste, deux fois.",
            "papa|Tu poses un, puis un ?",
            "enfant-m|Oui, papa.",
            "narrateur|La petite tour tient.",
            "papa|Merci, Nino.",
            "narrateur|Papa a vu le geste entier.",
            "narrateur|Le ventre de Nino se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "enfant-m|Elle tient, maman.",
            "maman|Tu la vois, ta tour ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le cube jaune reste sous le canapé.",
            "enfant-m|Je le vois, là.",
            "maman|Il attend, sous le bois ?",
            "enfant-m|Oui.",
            "narrateur|Nino ne tend pas la main.",
            "narrateur|Il reste près de sa tour.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "cubes",
        [
            "enfant-m|Je le veux, maintenant !",
            "narrateur|Nino se penche sous le canapé.",
            "narrateur|Sa main part trop vite.",
            "narrateur|Le cube jaune glisse plus loin.",
            "narrateur|Le tapis se plisse, sous les genoux.",
            "enfant-m|Oh.",
            "narrateur|Nino s'arrête.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le cube, un instant.",
            "narrateur|Il écoute l'horloge, près du bois.",
            "narrateur|Sous le canapé, l'éclat de cube brille.",
            "enfant-m|Il brille, comme tout à l'heure.",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur le cube.",
            "narrateur|Nino avance la main, lente.",
            "narrateur|Il regarde le cube.",
            "narrateur|Puis il le prend.",
            "enfant-m|Je le tiens.",
            "maman|Tu le poses sur la tour ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nino pose le cube jaune.",
            "narrateur|Le même geste, une fois de plus.",
            "narrateur|La tour tient, plus haute.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent assis sur le tapis.",
            "narrateur|Le vent se tait, près du rideau.",
            "maman|Tu veux un bout de pain ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nino croque.",
            "narrateur|C'est croustillant, un peu chaud.",
            "enfant-m|Comme tout à l'heure, papa !",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur le cube.",
            "maman|On est bien, ici.",
            "narrateur|Nino pose le pain près de la tour.",
            "enfant-m|On le voit, maman.",
            "maman|Tu le vois sur le cube ?",
            "enfant-m|Oui, l'éclat.",
            "narrateur|La tour se tient sur le tapis.",
            "narrateur|L'horloge pose un tic.",
            "narrateur|Le cube jaune brille, tout en haut.",
            "narrateur|L'éclat de cube tient sur l'arête.",
        ],
    ),
}


def vet(lines: list[str]) -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
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
            raise SystemExit(f"ban: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
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
    lines = vet(lines)
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
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "rayon jaune" not in blob:
        raise SystemExit(f"{SID}: manque rayon jaune")
    if "pain du goûter" not in blob and "pain du gouter" not in blob:
        raise SystemExit(f"{SID}: manque pain du goûter")
    if "sous le canapé" not in blob:
        raise SystemExit(f"{SID}: manque cube sous canapé")
    if "horloge" not in blob:
        raise SystemExit(f"{SID}: manque horloge")
    if "éclat d'horloge" in blob or "eclat d'horloge" in blob:
        raise SystemExit(f"{SID}: éclat d'horloge (BAN)")
    for dump_name in ("victorina", "bérénice", "berenice", "clément", "clement"):
        if re.search(rf"\b{dump_name}\b", blob):
            raise SystemExit(f"{SID}: prénom dump {dump_name}")
    if blob.count("besoin de calme") != 1:
        raise SystemExit(f"{SID}: besoin de calme ×{blob.count('besoin de calme')}")
    if "répéter" in blob or "repeter" in blob:
        raise SystemExit(f"{SID}: leçon dite (répéter)")
    if "observer d'abord" in blob:
        raise SystemExit(f"{SID}: leçon dite (observer d'abord)")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m") for r in roles):
        raise SystemExit(f"{SID}: rôle hors papa/maman")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    q_text = by["CHK_T0000_P0000_Q0001"]["text"]
    if q_text != "Nino a besoin de calme. Que peut-on faire ?":
        raise SystemExit(f"{SID}: question labels changés: {q_text}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "répéter":
        raise SystemExit(f"{SID}: expected_answer ≠ répéter")
    c1 = by["CHK_T0000_P0000_C0001"]["script"].lower()
    if "un cube" not in c1 or "un autre" not in c1:
        raise SystemExit(f"{SID}: leçon non vécue dans C0001")
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

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nwords = sum(words(c["text"]) for c in chunks)

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N1 (3–4 ans), audio familial, viser ~8 mots/phrase "
        "(plafond 10)\n"
        "- **Leçon :** DIF.BES.001 — besoin de calme / répéter / observer "
        "d'abord (vécus : veut la tour maintenant ; trop de cubes ; clac ; "
        "épaules ; un cube puis un autre ; sous le canapé la main trop vite ; "
        "refuse de foncer ; même geste). Jamais dite.\n"
        "- **Personnages :** Nino, papa, maman. Troupe D16. Un héros. Dump "
        "Bérénice / Clément / Victorina → Nino. Papa ajouté (dump xlsx a "
        "Victorina ; mission : un héros + papa/maman).\n"
        "- **Lieu :** salon. Rayon jaune sur tapis, cube sous canapé, "
        "horloge (détail, pas indice), pain du goûter, doudou, rideau. "
        "≠ 001-01 cartes ≠ 001-02 pâte ≠ 001-03 galets.\n"
        "- **Indice unique :** éclat de cube (arête dès l'ouverture → "
        "tremble à la chute → brille sous le canapé → tient sur l'arête). "
        "Pas éclat d'horloge / carte / boule / galet / bois. Pas boule, "
        "galet, carte, panier, dorure, cloche, corbeille, sac, croissant, "
        "réverbère.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un rayon jaune pose un carré sur le tapis. Sur l'arête, un éclat "
        "de cube luit. Pain du goûter, horloge, doudou. Nino veut une tour "
        "**maintenant**, aussi haute que le canapé. Il prend trop de cubes : "
        "clac, chute, cube jaune sous le canapé. Sourire parti, épaules "
        "basses. Papa se baisse. Question moteur : Nino a besoin de calme. "
        "Que peut-on faire ? expected répéter. Il pose un cube, puis un "
        "autre. Merci vécu. Sous le canapé, main trop vite : le cube glisse "
        "plus loin. Il refuse de foncer, retrouve l'éclat. Sur l'arête, "
        "l'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon, rayon jaune, tapis, canapé, horloge, pain du "
        "goûter, doudou, rideau.\n"
        "- Désir : une tour aussi haute que le canapé, **maintenant**.\n"
        "- Objet : cubes (bleu, rouge, jaune), tour, pain.\n"
        "- Indice unique : éclat de cube, vu dès l'ouverture, payé sur "
        "l'arête.\n"
        "- Urgence douce : tous les cubes à la fois, puis le jaune tout "
        "de suite.\n"
        "- Imprévu 1 : trop de cubes ; clac ; le jaune roule sous le "
        "canapé.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après le geste répété.\n"
        "- Imprévu 2 (plus rusé) : la main trop vite ; le cube glisse plus "
        "loin.\n"
        "- Résolution : il refuse de foncer, observe, écoute, reprend le "
        "même geste.\n"
        "- Retour : tour plus haute, cube jaune en haut, éclat sur "
        "l'arête.\n\n"
        "## Vécu\n\n"
        "Nino veut la tour **maintenant**. Impatience (tous les cubes, "
        "main trop vite sous le canapé), puis sourire qui disparaît, "
        "épaules qui tombent. Papa se baisse, pose une question, ne "
        "récite pas la règle. Nino agit : un cube, puis un autre. Merci "
        "vécu après le geste entier. Sous le canapé, il refuse de foncer. "
        "Fin : l'éclat du début tient sur l'arête.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre mission/roster : Les cubes de Nino (dump xlsx : La tour "
        "de Nino). Noyau tour conservé dans l'action. Lieu du dump : "
        "salon, rayon jaune, tapis, canapé, cube sous canapé, horloge, "
        "pain du goûter. Relance : Nino a besoin de calme. Que peut-on "
        "faire ? expected répéter. Labels Q posés (dump : Victorina a "
        "besoin de calme).\n"
        "- Ouverture inventée (le rayon pose un carré), pas un gabarit "
        "v2, pas « Nino joue au salon ».\n"
        "- Indice unique : éclat de cube. Pas éclat d'horloge (horloge = "
        "détail). Pas boule/galet/carte/panier/dorure/cloche/corbeille/"
        "sac/croissant/réverbère, pas merle, miel, marque fine.\n"
        "- Tics encore/déjà/tout doux/tout calme/tout lent et "
        "`aujourd'hui,` retirés.\n"
        "- Leçon non dite : on la voit quand il pose un cube, puis un "
        "autre, quand il s'arrête sous le canapé. Pas « on peut "
        "répéter », pas « observer d'abord », pas « c'est répéter ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. Papa "
        "ajouté. Dump Bérénice / Clément / Victorina absents.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle un peu plus tendu sous le canapé.\n"
        f"- {nwords} mots. N1 ≤ 10. `check()` OK. Pas apply.\n\n"
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
