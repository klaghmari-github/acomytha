#!/usr/bin/env python3
"""ATOM-COL.POL.001-10 — Le croissant d'Amir (F-NAR-019, N1, COL.POL.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.POL.001-10"
TITLE = "Le croissant d'Amir"
N1 = LIMITS["N1"]
INDICE = "éclat de corbeille"
CHARS = "Amir, papa, maman"
SETTING = (
    "boulangerie, corbeille d'osier, vitrine, sésame, marbre, cloche"
)
FIL = (
    "Une graine de sésame tape le marbre. Sur l'osier, un éclat de "
    "corbeille brille. Amir veut le croissant au sésame maintenant. "
    "Il parle trop vite, sans le mot : la dame ne lève pas les yeux. "
    "Il refuse de foncer, dit bonjour, s'il te plaît, obtient le "
    "sachet. Merci vécu. Un sachet trop vite : les graines tombent. "
    "Un éclat de corbeille reste pâle."
)
TIC_PHRASES = (
    "tout doux",
    "tout calme",
    "tout lent",
    "tout bas",
    "tout doucement",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)
BAN_WORDS = re.compile(
    r"\b(pavé|pave|réverbère|reverbere|farine|félix|felix|fanny|"
    r"tom|paillasson|flaque)\b",
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
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "trois notes",
    "une chose, puis la suivante",
    "une chose puis l'autre",
    "une étape après l'autre",
    "mie",
    "pli",
    "poisson",
    "page",
    "escargot",
    "croûte",
    "croute",
    "nappe",
    "casserole",
    "givre",
    "moineau",
    "radiateur",
    "éclat de croissant",
    "éclat de pavé",
    "éclat de pave",
    "éclat de réverbère",
    "éclat de reverbere",
    "éclat de farine",
    "éclat de vitre",
    "éclat de cloche",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de bâche",
    "éclat de bache",
    "éclat de poire",
    "éclat de volet",
    "éclat de sac",
    "éclat de casier",
    "éclat de laine",
    "éclat de marche",
    "éclat de nappe",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de crayon",
    "éclat de croûte",
    "éclat de seau",
    "éclat de page",
    "c'est du bon travail",
    "tu as fait du bon travail",
    "on aime écouter",
    "même leçon",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "tu as dit les mots",
    "tu as dit s'il te plaît",
    "tu as dit bonjour",
    "tu as dit merci",
    "les trois mots",
    "on dit bonjour",
    "on dit au revoir",
    "tu demandes",
    "tache de couleur",
    "ombre en forme de flèche",
    "marque fine",
    "minuscule symbole",
    "grain de miette",
    "grain de laine",
    "bande bleue",
    "lune d'étain",
    "lune d'etain",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de corbeille",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_croissant_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="dame",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_dit_bonjour_a_la_dame; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="Bonjour",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=bonjour_s_il_te_plait_merci_vecus; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de corbeille",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_sans_regarder_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de corbeille",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pale; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "bonjour",
    "accepted_examples": (
        "bonjour | s'il te plaît | merci | bonjour merci"
    ),
    "retry_prompt": "Il dit bonjour. Quels mots dit Amir ?",
    "engine_ok_text": "Oui, bonjour.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "cloche,osier",
        [
            "narrateur|Une graine de sésame tape le marbre.",
            "narrateur|Elle roule près de l'osier.",
            "narrateur|Amir connaît cette odeur de beurre.",
            "narrateur|La corbeille d'osier paraît neuve.",
            "narrateur|Sur l'osier, un éclat de corbeille brille.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, sur l'osier ?",
            "narrateur|Amir touche l'éclat de corbeille, un instant.",
            "narrateur|L'osier pique un peu le doigt.",
            "enfant-m|Il est rêche.",
            "maman|Le col, un bouton de plus.",
            "papa|Voilà.",
            "narrateur|Le soleil pose un carré sur le marbre.",
            "enfant-m|Il est jaune.",
            "papa|On avance.",
            "narrateur|La vitrine tient des pains dorés.",
            "narrateur|Des graines collent à la vitrine.",
            "enfant-m|Ça sent le beurre !",
            "maman|Tu sens, Amir ?",
            "enfant-m|Oui.",
            "narrateur|Une odeur de sésame arrive.",
            "enfant-m|Ça sent les graines.",
            "maman|Tu restes près de nous ?",
            "enfant-m|Oui, maman.",
            "narrateur|La porte de bois attend.",
            "papa|On entre.",
            "narrateur|Une petite cloche fait ding.",
            "narrateur|L'air chaud touche les joues.",
            "enfant-m|J'ai les joues chaudes.",
            "narrateur|En ce moment, Amir serre le manteau.",
            "narrateur|Le marbre est froid sous ses doigts.",
            "narrateur|La dame range la corbeille d'osier.",
            "narrateur|Des croissants dorés dorment dans l'osier.",
            "enfant-m|Je le veux, maintenant.",
            "papa|On s'approche du bois.",
            "enfant-m|Celui du bout !",
            "narrateur|Un croissant au sésame attend au bout.",
            "narrateur|Amir parle trop vite vers l'osier.",
            "narrateur|Les mots se perdent dans la cloche.",
            "enfant-m|Oh.",
            "narrateur|La dame ne lève pas les yeux.",
            "narrateur|Ses mains tiennent la corbeille.",
            "enfant-m|Je le prends !",
            "narrateur|Le croissant reste dans l'osier.",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Les épaules d'Amir tombent un peu.",
            "narrateur|Ça serre, dans son ventre.",
            "maman|Le croissant est dans l'osier.",
            "papa|Tu le vois, Amir ?",
            "narrateur|Papa se baisse à sa hauteur.",
            "maman|Tu parles à la dame, Amir.",
            "papa|Elle t'écoute, Amir ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Amir parle à la dame.",
            "narrateur|Quels mots dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "papier,cloche",
        [
            "narrateur|Amir avance trop vite vers l'osier.",
            "enfant-m|Celui du bout, maintenant !",
            "narrateur|Sa voix se mélange à la cloche.",
            "enfant-m|Oh.",
            "narrateur|Le croissant reste dans l'osier.",
            "narrateur|Il refuse de foncer.",
            "narrateur|Amir referme la bouche.",
            "narrateur|Il écoute la cloche, un instant.",
            "papa|Tu veux venir près de l'osier ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Amir pose un pied sur le pas.",
            "narrateur|Le bois est tiède, un peu lisse.",
            "enfant-m|Bonjour.",
            "papa|Bonjour.",
            "enfant-m|Celui du bout, s'il te plaît.",
            "narrateur|La dame tend le croissant.",
            "narrateur|Le papier enveloppe le croissant.",
            "narrateur|Le sachet est chaud contre le manteau.",
            "enfant-m|Merci.",
            "papa|Merci, Amir.",
            "narrateur|Papa a entendu toute la phrase.",
            "narrateur|Le ventre d'Amir se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tu as les mains au chaud ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Ça sent le beurre et le sésame.",
            "enfant-m|Le croissant est à moi.",
            "maman|Il est dans tes mains.",
            "narrateur|Amir pose une main sur le sachet.",
            "narrateur|Le papier est un peu rêche.",
            "narrateur|La cloche se tait.",
            "enfant-m|Il est chaud, papa.",
            "papa|Tu le portes jusqu'à la rue ?",
            "enfant-m|Oui, papa.",
            "narrateur|Des graines tiennent sur le papier.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pas,papier",
        [
            "narrateur|Amir tire le sachet trop vite.",
            "enfant-m|Je le mange, d'un coup !",
            "narrateur|Le papier glisse entre les doigts.",
            "narrateur|Des graines de sésame tombent au marbre.",
            "narrateur|Le croissant penche vers le sol.",
            "enfant-m|Oh.",
            "narrateur|Amir avance les mains.",
            "narrateur|Puis il s'arrête net.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Papa attend, sans parler.",
            "narrateur|Amir refuse de foncer.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Amir observe l'osier, écoute la boutique.",
            "narrateur|Sur l'osier, un éclat de corbeille brille.",
            "enfant-m|Là, près de la corbeille.",
            "narrateur|Amir tient le sachet des deux mains.",
            "narrateur|Le papier est rêche, un peu chaud.",
            "enfant-m|Il est chaud, papa.",
            "papa|Tu le portes jusqu'à la porte ?",
            "enfant-m|Oui, papa.",
            "maman|On sort ?",
            "enfant-m|Oui, maman.",
            "narrateur|La porte s'ouvre.",
            "narrateur|La cloche fait ding.",
            "narrateur|L'air plus frais revient sur les joues.",
            "narrateur|Amir serre le sachet contre lui.",
            "enfant-m|Il reste chaud.",
            "papa|On marche.",
            "narrateur|Le sachet penche, puis se cale.",
            "enfant-m|Je le tiens.",
            "maman|On avance.",
            "narrateur|Amir passe le pas de bois.",
            "narrateur|Le bois craque, un peu.",
            "enfant-m|Les graines sont à moi.",
            "maman|Elles sont dans le papier.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "pas",
        [
            "enfant-m|L'osier brillait, papa.",
            "papa|Tu le vois, comme dans la boutique ?",
            "enfant-m|Oui, sur l'osier.",
            "narrateur|Amir pose le sachet contre le manteau.",
            "maman|On le garde au chaud ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Le four sentait bon.",
            "maman|Il est contre toi.",
            "narrateur|Une vapeur monte du papier.",
            "narrateur|Amir respire, plus large.",
            "papa|On rentre ?",
            "enfant-m|Oui.",
            "narrateur|Les joues d'Amir se réchauffent.",
            "narrateur|Le sachet reste tiède sous la main.",
            "enfant-m|Il sent le sésame.",
            "papa|Tu le sens, près du nez ?",
            "enfant-m|Oui, papa.",
            "maman|On est bien, ici.",
            "narrateur|Un éclat de corbeille reste pâle.",
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
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"tic {tic!r}: {ph}")
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"tic {m.group(0)!r}: {ph}")
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"extra {bad}: {ph}")
        if BAN_WORDS.search(low):
            raise SystemExit(f"ban {BAN_WORDS.search(low).group(0)!r}: {ph}")
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
    merged = dict(src)
    merged["fil_rouge"] = FIL
    merged["title"] = TITLE
    merged["characters"] = CHARS
    merged["setting"] = SETTING
    merged["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    nwords = sum(words(c["text"]) for c in merged["chunks"])
    blob = "\n".join(c["script"] for c in merged["chunks"]).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: refuse de foncer absent")
    if re.search(r"\bfélix\b", blob) or re.search(r"\bfelix\b", blob):
        raise SystemExit(f"{SID}: Félix interdit")
    if "éclat de croissant" in blob:
        raise SystemExit(f"{SID}: éclat de croissant (BAN 001-07)")
    if "sésame" not in blob or "vitrine" not in blob:
        raise SystemExit(f"{SID}: monde corbeille/vitrine/sésame incomplet")
    adults = " ".join(
        ln.split("|", 1)[1]
        for c in merged["chunks"]
        for ln in c["script"].splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
    ).lower()
    if adults.count("merci") != 1:
        raise SystemExit(f"{SID}: merci ×{adults.count('merci')}")
    if "bravo" in adults:
        raise SystemExit(f"{SID}: bravo en trop")
    roles = [
        ln.split("|", 1)[0]
        for c in merged["chunks"]
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m") for r in roles):
        raise SystemExit(f"{SID}: rôle hors papa/maman")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    enfant_p0 = " ".join(
        ln.split("|", 1)[1]
        for ln in by["CHK_T0000_P0000"]["script"].splitlines()
        if ln.startswith("enfant-")
    ).lower()
    if "s'il te plaît" in enfant_p0 or "s'il te plait" in enfant_p0:
        raise SystemExit(f"{SID}: s'il te plaît déjà dans P0000")
    if re.search(r"\bbonjour\b", enfant_p0):
        raise SystemExit(f"{SID}: bonjour enfant déjà dans P0000")
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Amir parle à la dame. Quels mots dit-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "bonjour":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt") or ""
    if "félix" in retry.lower() or "felix" in retry.lower():
        raise SystemExit(f"{SID}: retry Félix")
    if "amir" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans Amir")
    c1 = by["CHK_T0000_P0000_C0001"]["script"].lower()
    if "bonjour" not in c1 or "s'il te plaît" not in c1 or "merci" not in c1:
        raise SystemExit(f"{SID}: leçon non vécue dans C0001")
    if "la dame" not in blob:
        raise SystemExit(f"{SID}: dame absente (label)")
    tts_ok = all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_xai_tags"] != c["text"]
        and c["text_ssml"].startswith("<speak>")
        for c in merged["chunks"]
    )
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N1 (≤10 mots/phrase), audio familial\n"
        "- **Leçon :** COL.POL.001 — bonjour / s'il te plaît / merci "
        "(vécus : veut le croissant au sésame maintenant ; parle trop vite ; "
        "la dame ne lève pas les yeux ; refuse de foncer ; dit bonjour ; "
        "s'il te plaît ; merci ; sachet trop vite, graines au marbre)\n"
        "- **Personnages :** Amir, papa, maman. « la dame » = label "
        "(tend le croissant, pas de leçon parlée). Dump Félix → Amir. "
        "Papa ajouté. Troupe D16.\n"
        "- **Lieu :** boulangerie, corbeille d'osier, vitrine, sésame, "
        "marbre, cloche\n"
        "- **Indice unique :** éclat de corbeille (osier dès l'ouverture → "
        "touché → revu quand le sachet glisse → reste pâle)\n"
        "- **Question moteur :** Amir parle à la dame. Quels mots dit-il ? "
        "→ bonjour. retry : Quels mots dit Amir ?\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une graine de sésame tape le marbre. Amir connaît l'odeur de "
        "beurre ; la corbeille d'osier paraît neuve. Sur l'osier, un éclat "
        "de corbeille brille. Vitrine, graines, cloche. Amir veut le "
        "croissant au sésame du bout **maintenant**. Première idée : parler "
        "trop vite, sans le mot. La dame ne lève pas les yeux. Sourire "
        "parti, épaules basses. Papa se baisse. Il refuse de foncer. Près "
        "de l'osier, il dit bonjour, puis s'il te plaît. Le sachet arrive. "
        "Merci vécu. Il veut mordre d'un coup : le papier glisse, les "
        "graines tombent. Il s'arrête, lit l'éclat. Un éclat de corbeille "
        "reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : boulangerie, osier, sésame, vitrine, marbre, cloche, "
        "sachet. ≠ COL.POL.001-07 Mila farine/vitre / éclat de croissant. "
        "≠ 001-01 Nino pavé / petit pain. ≠ 001-08 Raphaël réverbère / "
        "brioche.\n"
        "- Désir : le croissant au sésame du bout, maintenant.\n"
        "- Objet : croissant au sésame, corbeille d'osier, sachet, vitrine.\n"
        "- Indice unique : éclat de corbeille, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : les mots trop vite, le croissant dans l'osier.\n"
        "- Imprévu 1 : parler trop vite, sans bonjour ; la dame ne lève "
        "pas les yeux.\n"
        "- Cue : papa à la même hauteur, près de l'osier. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : mordre d'un coup, sachet qui glisse, "
        "graines de sésame au marbre.\n"
        "- Résolution : il refuse de foncer, dit bonjour, s'il te plaît, "
        "tient le sachet des deux mains.\n"
        "- Retour : sachet tiède contre le manteau, éclat de corbeille pâle.\n\n"
        "## Vécu\n\n"
        "Leçon COL.POL.001 (dire bonjour, s'il te plaît, merci, jamais dite "
        "comme règle) greffée. La première idée (prendre maintenant, sans "
        "le mot) échoue. Le choix d'Amir change l'action. Un « en ce "
        "moment ». Un merci vécu. Adulte + question. Troupe D16 : Amir, "
        "papa, maman. Dump Félix → Amir. Papa ajouté. Pas de maîtresse. "
        "Question moteur : Amir parle à la dame. Quels mots dit-il ?\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le croissant d'Amir. Lieu du dump : boulangerie. "
        "Détail propre : corbeille d'osier, vitrine, sésame, marbre. "
        "Sans farine, sans vitre-neige, sans pavé, sans réverbère, sans "
        "paillasson, sans flaque.\n"
        "- Ouverture inventée (graine de sésame sur le marbre), pas un "
        "gabarit v2, pas « la rue est froide », pas farine sur la vitre.\n"
        "- Indice unique : éclat de corbeille. Pas éclat de croissant "
        "(001-07), pas pavé/réverbère/farine, pas merle-trois-notes, miel, "
        "gouttes, pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : pas « on dit bonjour », pas « tu as dit les "
        "mots ». Amir dit bonjour, le croissant vient.\n"
        "- Question moteur : Amir parle à la dame. Quels mots dit-il ? "
        "expected bonjour. retry Félix→Amir. 5 chunks, kinds inchangés.\n"
        "- example4 074 / 006 / 038 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_col_eco_002_10.py` (Amir).\n"
        f"- {nwords} mots. N1 ≤ 10. TTS : notes, ssml, xai, piper par chunk.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
