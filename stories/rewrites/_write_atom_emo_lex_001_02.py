#!/usr/bin/env python3
"""ATOM-EMO.LEX.001-02 — Raphaël et le gâteau à la vanille (F-NAR-019, N2, EMO.LEX.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.001-02"
TITLE = "Raphaël et le gâteau à la vanille"
N2 = LIMITS["N2"]
CHARS = "Raphaël, papa, maman"
SETTING = "cuisine, après-midi de pluie"
INDICE = "éclat de moule"
FIL = (
    "La pluie tapote la vitre. Raphaël connaît la cuisine. "
    "Sur le métal, un éclat de moule luit. Il veut le gâteau, "
    "maintenant. Je suis content, dit-il. Le moule penche. "
    "Poitrine trop vite. Sourire parti. Papa s'accroupit. "
    "Deuxième ruse : gâteau trop chaud, fraise qui glisse. "
    "Il refuse de foncer. Il tend la fraise. Merci vécu. "
    "Un éclat de moule tient sur le métal."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tasse|nappe|farine|casserole|assiette|comptoir|rouleau|"
    r"étagère|etagere|torchon|tabouret|treille|merle|miel|"
    r"maîtresse|maitresse|gouttière|gouttiere|rampe|escalier|"
    r"serviette|tapis|rideau|plaid|casserole)\b",
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
    "j'ai dit : je suis",
    "j'ai dit: je suis",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "c'est de la joie",
    "c est de la joie",
    "tu as nommé",
    "tu as nomme",
    "la joie, on peut",
    "on partage la joie",
    "être content, c'est bien",
    "etre content, c'est bien",
    "tu as partagé",
    "tu as partage",
    "tu as bien invité",
    "tu as bien invite",
    "bravo, raphaël",
    "bravo, raphael",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de fraise",
    "éclat de vanille",
    "éclat de tasse",
    "éclat de nappe",
    "éclat de farine",
    "éclat de casserole",
    "éclat d'assiette",
    "éclat de assiette",
    "éclat de tour",
    "éclat de comptoir",
    "éclat de pot",
    "éclat de rouleau",
    "éclat de lit",
    "éclat d'étagère",
    "éclat d'etagere",
    "éclat de torchon",
    "éclat de tabouret",
    "éclat de treille",
    "éclat de gâteau",
    "éclat de gateau",
    "éclat de table",
    "éclat de four",
    "éclat de vitre",
    "éclat de pluie",
    "éclat de sucre",
    "éclat de métal",
    "éclat de metal",
    "éclat de bois",
    "éclat de cube",
    "éclat de tapis",
    "éclat de rideau",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de moule",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=joie puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_gateau_maintenant; "
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
            "sous_texte=raphael_sourit_que_dit_il; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="moule",
        note=(
            "arc=confirmation; intention=relancer_sans_leçon; "
            "emotion=retenue puis joie_discrète; intensite=1; "
            "destinataire=enfant; sous_texte=il_s_arrete_le_moule_tient; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de moule",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=gateau_trop_chaud_fraise_glisse_il_refuse_de_foncer; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de moule",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_metal; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "content",
    "accepted_examples": "content | contente | je suis contente | joie | de la joie",
    "retry_prompt": "Raphaël sent de la joie. Que dit-il ?",
    "engine_ok_text": "Oui, content.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "pluie",
        [
            "narrateur|La pluie tapote la vitre de la cuisine.",
            "enfant-m|Ça chante, papa.",
            "papa|Tu l'entends, la pluie ?",
            "enfant-m|Oui, papa.",
            "narrateur|Raphaël connaît cette cuisine, ses bruits, son air chaud.",
            "maman|Tu la connais, cette pièce ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un détail paraît nouveau, près du four.",
            "narrateur|Sur le métal, un éclat de moule luit.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, sur le métal ?",
            "enfant-m|Oui, un petit point.",
            "papa|Le four le touche.",
            "narrateur|L'air sent le chaud et le sucré.",
            "enfant-m|Ça sent le gâteau !",
            "maman|Le gâteau à la vanille est dans le moule.",
            "narrateur|Des fraises rouges brillent dessus.",
            "enfant-m|Elles sont rouges !",
            "papa|Tu les vois, les fraises ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le bois de la table est un peu collant.",
            "enfant-m|Il colle aux doigts.",
            "maman|Il est tiède, Raphaël ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Le moule pèse un peu, sur la table.",
            "enfant-m|Il est lourd.",
            "papa|Tu le sens, le poids ?",
            "enfant-m|Oui, papa.",
            "narrateur|En ce moment, Raphaël avance vers le moule.",
            "enfant-m|Je veux le gâteau, maintenant !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|Ses joues deviennent chaudes.",
            "narrateur|Son ventre est léger, très léger.",
            "narrateur|Un sourire arrive, tout seul.",
            "enfant-m|Je suis content.",
            "maman|Tes joues sont chaudes, Raphaël ?",
            "enfant-m|Oui, maman.",
            "narrateur|Il tire le moule vers lui, trop vite.",
            "narrateur|Le moule penche d'un coup.",
            "narrateur|Le gâteau reste coincé, au fond.",
            "narrateur|Ça fait un bruit sec.",
            "enfant-m|Oh.",
            "narrateur|Raphaël reste surpris, les mains ouvertes.",
            "narrateur|Sa poitrine va trop vite.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et l'inquiétude se heurtent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois le moule, Raphaël ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains sont chaudes, Raphaël ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de moule tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Raphaël sourit.",
            "narrateur|Que dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "",
        [
            "narrateur|Raphaël veut le gâteau, tout de suite.",
            "enfant-m|Je le prends, maintenant !",
            "narrateur|Le moule reste un peu penché.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-m|Trop vite.",
            "narrateur|Raphaël avance les mains, trop vite.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le moule, un instant.",
            "narrateur|Il écoute la cuisine, près du four.",
            "enfant-m|Il est coincé.",
            "papa|Tu restes un peu, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le métal est tiède, sous les doigts.",
            "enfant-m|Il pique un peu.",
            "narrateur|Raphaël reprend le bord du moule, sans se presser.",
            "papa|Tu le vois, le moule ?",
            "enfant-m|Oui, papa.",
            "maman|Il tient, Raphaël ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le ventre de Raphaël se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près du moule ?",
            "enfant-m|Oui.",
            "maman|La pluie tapote la vitre ?",
            "enfant-m|Oui, maman.",
            "narrateur|Une fraise attend sur le dessus.",
            "enfant-m|Je la prends.",
            "papa|Tu la poses, Raphaël ?",
            "enfant-m|Pas tout de suite.",
            "narrateur|Le gâteau a un dessus un peu doré.",
            "enfant-m|Il est doré !",
            "maman|Tes genoux sont au chaud ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pluie",
        [
            "narrateur|Maman pousse le moule près de Raphaël.",
            "narrateur|Le métal est un peu brûlant.",
            "enfant-m|Le gâteau, maintenant !",
            "narrateur|Raphaël approche la main, trop vite.",
            "narrateur|La chaleur pique sa paume.",
            "enfant-m|Il est trop chaud !",
            "narrateur|Il retire la main d'un coup.",
            "narrateur|Une fraise glisse du dessus.",
            "enfant-m|Elle glisse !",
            "narrateur|La fraise roule vers le bois de la table.",
            "narrateur|Raphaël avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Raphaël refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le moule, un instant.",
            "narrateur|Il écoute la cuisine, près du four.",
            "narrateur|Sur le métal, un éclat de moule luit.",
            "enfant-m|Là, sur le métal.",
            "narrateur|Raphaël attend, les mains ouvertes.",
            "papa|On prend la fraise ?",
            "enfant-m|Oui, papa.",
            "narrateur|La fraise sent le sucre, un peu tiède.",
            "narrateur|Raphaël la tend vers papa.",
            "papa|Merci, Raphaël.",
            "narrateur|Papa prend un petit bout.",
            "narrateur|Raphaël prend un petit bout.",
            "enfant-m|C'est sucré.",
            "maman|Le sucre colle un peu, Raphaël ?",
            "enfant-m|Un peu.",
            "papa|Tu vois le point, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le gâteau tient, dans le moule.",
            "enfant-m|On le garde.",
            "maman|Un peu de pluie passe sur la vitre.",
            "enfant-m|Elle tapote.",
            "papa|On reste ici, Raphaël ?",
            "enfant-m|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "pluie",
        [
            "narrateur|Ils restent près du moule.",
            "narrateur|Maman essuie un peu de sucre.",
            "enfant-m|Le moule a penché, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, près du gâteau.",
            "maman|On est bien, ici.",
            "narrateur|Raphaël tapote le métal du doigt.",
            "enfant-m|Il a une trace de sucre.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Maman, un bout pour toi.",
            "narrateur|Maman prend un petit bout.",
            "papa|Le gâteau est resté, Raphaël.",
            "enfant-m|Oui, dans le moule.",
            "narrateur|Ça sent la vanille, un peu tiède.",
            "enfant-m|Et le sucre, maman.",
            "maman|Oui, dans l'air.",
            "papa|La pluie tapote, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le moule reste près de la table.",
            "narrateur|Un éclat de moule tient sur le métal.",
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
    if "je suis content" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: manque je suis content (acte) à l'ouverture")
    if blob.count("je suis content") != 1:
        raise SystemExit(f"{SID}: je suis content ×{blob.count('je suis content')}")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Raphaël = enfant-m)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    if re.search(r"\bava\b", blob):
        raise SystemExit(f"{SID}: Ava du dump")
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
        "c'est de la joie",
        "j'ai dit : je suis",
        "tu as nommé",
        "la joie, on peut",
        "on partage la joie",
        "l'histoire est finie",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Raphaël sourit. Que dit-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "content":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "content | contente | je suis contente | joie | de la joie"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Raphaël sent de la joie. Que dit-il ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    for c in chunks:
        if c["chunk_id"] == "CHK_T0000_P0000_Q0001":
            continue
        if c.get("expected_answer") not in (None, ""):
            raise SystemExit(f"{SID}: expected hors Q ({c['chunk_id']})")
        if c.get("accepted_examples") not in (None, ""):
            raise SystemExit(f"{SID}: accepted hors Q ({c['chunk_id']})")
        if c.get("retry_prompt") not in (None, ""):
            raise SystemExit(f"{SID}: retry hors Q ({c['chunk_id']})")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "la vanille monte" in opening:
        raise SystemExit(f"{SID}: ouverture dump (vanille / escalier)")
    if "cuisine" not in blob:
        raise SystemExit(f"{SID}: manque cuisine")
    if "gâteau" not in blob and "gateau" not in blob:
        raise SystemExit(f"{SID}: manque gâteau")
    if "vanille" not in blob:
        raise SystemExit(f"{SID}: manque vanille")
    if "fraise" not in blob:
        raise SystemExit(f"{SID}: manque fraise")
    if "pluie" not in blob:
        raise SystemExit(f"{SID}: manque pluie")
    for ban in (
        "éclat de fraise",
        "éclat de vanille",
        "éclat de tasse",
        "éclat de nappe",
        "éclat de farine",
        "éclat de casserole",
        "éclat de tour",
        "éclat de comptoir",
        "tout doux",
        "tout calme",
        "tout doucement",
        "merle",
        "miel",
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
        "- **Leçon :** EMO.LEX.001 — nommer la joie + partager "
        "(vécue : Raphaël dit « je suis content », tend la fraise ; "
        "moule penche, poitrine trop vite, sourire parti, papa accroupi ; "
        "2e ruse : gâteau trop chaud, fraise qui glisse, il refuse de "
        "foncer). JAMAIS dite dans le récit. Pas « c'est de la joie ». "
        "Pas « tu as nommé ». Pas « j'ai dit : je suis ».\n"
        "- **Personnages :** Raphaël, papa, maman. Dump Ava → D16 "
        "Raphaël = enfant-m. Pas de copain. Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** cuisine, après-midi de pluie, moule, gâteau, "
        "vanille, fraise, vitre, table, four, métal. BAN tasse / nappe / "
        "farine / casserole / assiette / tour / comptoir / pot / rouleau / "
        "lit / étagère / torchon / tabouret / treille (indice). "
        "≠ dump vanille qui monte l'escalier.\n"
        "- **Indice unique :** éclat de moule (luit à l'ouverture → "
        "tremble à la pente → luit quand la fraise glisse → tient sur "
        "le métal). BAN éclat de fraise / vanille / tasse / nappe / "
        "farine / casserole / assiette / tour / comptoir.\n"
        "- **Question moteur :** « Raphaël sourit. Que dit-il ? » "
        "expected dump **content**. accepted dump "
        "`content | contente | je suis contente | joie | de la joie`. "
        "retry dump Ava → Raphaël, dit-il. Non récitée dans les autres "
        "chunks. Hors Q : expected / accepted / retry = null.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La pluie tapote la vitre. Raphaël connaît la cuisine. Un détail "
        "paraît nouveau : sur le métal, un éclat de moule luit. Vanille, "
        "gâteau, fraises. Il veut le gâteau **maintenant**. Joues chaudes, "
        "sourire, « je suis content ». Il tire le moule trop vite. Le moule "
        "penche. Poitrine trop vite. Sourire parti. Papa s'accroupit. Merci "
        "vécu, après la fraise tendue. Deuxième ruse : gâteau trop chaud, "
        "fraise qui glisse. Il s'arrête, lit l'éclat. Un éclat de moule "
        "tient sur le métal.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine, après-midi de pluie, vitre, four, moule, "
        "table collante.\n"
        "- Désir : prendre le gâteau à la vanille, maintenant.\n"
        "- Objet : moule, gâteau, fraises (objets dump, pas l'indice).\n"
        "- Indice unique : éclat de moule, vu dès l'ouverture, payé "
        "sur le métal. Pas éclat de fraise / vanille / tasse.\n"
        "- Urgence douce : il tire le moule trop vite.\n"
        "- Imprévu 1 : moule penche, gâteau coincé, poitrine trop vite, "
        "sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "la fraise tendue.\n"
        "- Imprévu 2 (plus rusé) : gâteau trop chaud, fraise qui glisse.\n"
        "- Résolution : il refuse de foncer, observe, écoute la cuisine, "
        "retrouve l'éclat, tend la fraise.\n"
        "- Retour : partage fragile, moule près de la table, éclat sur "
        "le métal.\n\n"
        "## Vécu\n\n"
        "Raphaël veut le gâteau **maintenant**. Il dit « je suis content » "
        "(acte, une fois). Impatience, puis moule penché, sourire parti. "
        "Il s'arrête, observe. Papa se baisse, pose une question, ne "
        "récite pas la règle. Gâteau trop chaud, fraise qui glisse. Il "
        "refuse de foncer. Il tend la fraise. Merci vécu. Fin : l'éclat "
        "du début tient sur le métal.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Raphaël et le gâteau à la vanille (noyau dump). "
        "Relance : Que dit-il ? expected content.\n"
        "- Lieu du dump-meta (cuisine, après-midi de pluie). Maman et "
        "papa. Raphaël = héros enfant-m. Dump Ava retiré.\n"
        "- Ouverture inventée (vitre, cuisine connue, détail nouveau), "
        "pas un gabarit v2, pas « La vanille monte l'escalier ».\n"
        "- Indice unique : éclat de moule. BAN éclat de fraise / "
        "vanille / tasse / nappe / farine / casserole / assiette / "
        "tour / comptoir. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doucement » du dump.\n"
        "- Leçon non dite : on la voit quand il dit « je suis content », "
        "quand il tend la fraise. Pas « c'est de la joie ». Pas "
        "« tu as nommé ». Pas « j'ai dit : je suis ». Pas "
        "« L'histoire est finie ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Raphaël sourit. Que dit-il ? ». "
        "expected content. 5 chunks, kinds inchangés. expected/accepted "
        "dump conservés (féminin moteur gardé). retry Ava → Raphaël, "
        "dit-il. Hors Q : null.\n"
        "- example4 055 / 087 / 019 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N2 / raw.js.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers la fraise qui glisse.\n"
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
