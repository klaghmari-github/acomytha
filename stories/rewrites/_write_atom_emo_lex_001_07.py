#!/usr/bin/env python3
"""ATOM-EMO.LEX.001-07 — Mila et la fraise tiède (F-NAR-019, N2, EMO.LEX.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.001-07"
TITLE = "Mila et la fraise tiède"
N2 = LIMITS["N2"]
CHARS = "Mila, papa, maman"
SETTING = (
    "jardin, fraisiers, fin de journée, arrosoir, seau, "
    "brouette, terre, feuilles, fer"
)
INDICE = "éclat de brouette"
FIL = (
    "Une goutte reste au bec de l'arrosoir. Sur le fer, "
    "un éclat de brouette luit. Mila veut la fraise tiède, "
    "maintenant. Elle tire trop vite. La fraise est trop molle. "
    "Jus sur les doigts. Sourire parti. Papa s'accroupit. "
    "Elle tend, dit : je suis contente. Merci vécu. "
    "Deuxième ruse : un oiseau, le jus, la fraise trop molle. "
    "Elle refuse de foncer. Un éclat de brouette tient sur le fer."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(merle|miel|treille|moule|tuteur|saladier|gomme|berge|"
    r"torchon|tabouret|panier|maîtresse|maitresse|"
    r"grand-père|grand-pere|jardinier)\b",
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
    "tu as nommé",
    "c'est de la joie",
    "c est de la joie",
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
    "tu as partagé",
    "tu as partage",
    "tu partages ta joie",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de fraise",
    "éclat d'arrosoir",
    "éclat de seau",
    "éclat de panier",
    "éclat de treille",
    "éclat de moule",
    "éclat de tuteur",
    "éclat de saladier",
    "éclat de gomme",
    "éclat de berge",
    "éclat de torchon",
    "éclat de tabouret",
    "éclat de tour",
    "éclat de feuille",
    "éclat de terre",
    "éclat de goutte",
    "éclat de fer",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de brouette",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis inquiétude; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_fraise_tiède_maintenant; "
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
            "sous_texte=mila_sourit_que_dit_elle; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="fraise",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_tend_sans_foncer_ils_goûtent; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de brouette",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=oiseau_jus_fraise_molle_elle_refuse_de_foncer; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de brouette",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_fer; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "content",
    "accepted_examples": (
        "content | contente | je suis contente | joie | de la joie | partager"
    ),
    "retry_prompt": "Mila sent de la joie. Que dit-elle ?",
    "engine_ok_text": "Oui, content.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "oiseau",
        [
            "narrateur|Une goutte reste au bec de l'arrosoir.",
            "enfant-f|Elle pend, papa.",
            "papa|Tu la vois, la goutte ?",
            "enfant-f|Oui, elle brille.",
            "narrateur|La terre du rang sent le soleil.",
            "enfant-f|Ça sent la terre, maman.",
            "maman|Tu la sens, la terre chaude ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le seau de bois est mouillé, près des pieds.",
            "enfant-f|Il sent l'eau.",
            "papa|Il a bu le rang.",
            "narrateur|Maman pose l'arrosoir contre la brouette.",
            "narrateur|Le fer de la brouette est tiède.",
            "enfant-f|Il est chaud !",
            "maman|Le soleil l'a touché.",
            "narrateur|Sur le fer, un éclat de brouette luit.",
            "enfant-f|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Papa a de la terre aux mains.",
            "narrateur|Les feuilles des fraisiers sont poussiéreuses.",
            "enfant-f|Elles cachent des rouges.",
            "maman|Tu veux chercher, Mila ?",
            "enfant-f|Oui, maintenant !",
            "narrateur|En ce moment, Mila s'accroupit.",
            "narrateur|La terre est tiède sous ses genoux.",
            "enfant-f|Elle chauffe.",
            "papa|Tes genoux sont bien ?",
            "enfant-f|Oui, papa.",
            "narrateur|Une feuille sent le vert, tout près.",
            "maman|Tu la lèves, Mila ?",
            "enfant-f|Oui.",
            "narrateur|Sous la feuille, une fraise rouge.",
            "enfant-f|Elle est petite !",
            "narrateur|Elle est tiède, sous la feuille.",
            "enfant-f|Je la prends, maintenant !",
            "narrateur|Mila tire trop vite, trop fort.",
            "narrateur|La fraise est trop molle.",
            "enfant-f|Oh.",
            "narrateur|Le jus rougit ses doigts.",
            "narrateur|La fraise glisse, presque.",
            "enfant-f|Elle glisse !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et la peur se heurtent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois tes doigts, Mila ?",
            "enfant-f|Ils sont rouges.",
            "maman|La fraise est molle, Mila ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de brouette tremble, puis tient.",
            "narrateur|Mila referme les doigts, sans serrer.",
            "enfant-f|Elle est chaude.",
            "papa|Tu la tiens ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila veut croquer, tout de suite.",
            "enfant-f|Je la mange, maintenant !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "narrateur|Elle avance la fraise vers sa bouche.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Elle regarde papa, puis maman.",
            "enfant-f|Pour vous aussi.",
            "narrateur|Ses joues sont chaudes.",
            "narrateur|Elle tend la fraise, sans bousculer.",
            "enfant-f|Je suis contente.",
            "maman|Elle sent le soleil.",
            "papa|On la goûte où ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Mila sourit.",
            "narrateur|Que dit-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Maman se baisse vers la fraise.",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Un bout pour maman.",
            "maman|Tout petit, Mila ?",
            "enfant-f|Oui, elle est molle.",
            "narrateur|Mila avance trop vite vers maman.",
            "narrateur|Le jus coule sur le pouce.",
            "enfant-f|Il coule !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Vite, le bout !",
            "narrateur|Mila avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe la fraise, un instant.",
            "narrateur|Elle écoute le jardin.",
            "papa|Tu restes un peu, Mila ?",
            "enfant-f|Oui, papa.",
            "papa|Merci, Mila.",
            "narrateur|Mila tend un bout, sans serrer.",
            "narrateur|Maman croque un tout petit bout.",
            "maman|Elle est tiède, sous la langue.",
            "enfant-f|Comme le soleil.",
            "papa|Un bout pour moi ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa croque, sans serrer.",
            "enfant-f|Il reste le mien.",
            "maman|Tes doigts sont rouges, Mila ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le ventre de Mila se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près de la brouette ?",
            "enfant-f|Oui.",
            "narrateur|Mila tient le dernier bout à deux mains.",
            "enfant-f|Je ne serre pas.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "oiseau",
        [
            "narrateur|Mila veut poser le bout dans le seau.",
            "narrateur|Le bois est mouillé, un peu sombre.",
            "enfant-f|Il la garde !",
            "narrateur|Mila pousse trop vite, tout de suite.",
            "narrateur|La fraise est trop molle.",
            "enfant-f|Elle s'écrase !",
            "narrateur|Le jus file entre les lattes du seau.",
            "enfant-f|Il part !",
            "narrateur|Un oiseau se pose sur la brouette.",
            "narrateur|Il penche la tête vers le jus.",
            "enfant-f|Il veut ma fraise !",
            "narrateur|Mila avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Mila refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe la fraise, un instant.",
            "narrateur|Elle écoute le jardin, près du fer.",
            "narrateur|Sur le fer, un éclat de brouette luit.",
            "enfant-f|Là, sur le fer.",
            "narrateur|L'oiseau picore la goutte de l'arrosoir.",
            "narrateur|La goutte tombe dans l'herbe.",
            "enfant-f|Il a l'eau.",
            "papa|On tient le bout ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila lève la fraise hors du seau.",
            "narrateur|Le bout est chaud, un peu plat.",
            "enfant-f|Poumf.",
            "maman|Il reste sucré, Mila ?",
            "enfant-f|Oui, maman.",
            "papa|L'oiseau est parti vers le rang.",
            "enfant-f|Il a la goutte.",
            "maman|Toi, tu as le bout.",
            "papa|On le goûte ici ?",
            "enfant-f|Oui, près du fer.",
            "narrateur|Mila croque le dernier bout, sans se presser.",
            "enfant-f|Il est tiède.",
            "maman|Tes genoux sont au chaud ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le jus laisse une trace sur le fer.",
            "enfant-f|Il allume le point.",
            "papa|Tu vois le point, Mila ?",
            "enfant-f|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la brouette.",
            "narrateur|Maman essuie un peu de jus.",
            "enfant-f|On a goûté, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-f|Oui, sous la feuille.",
            "maman|On est bien, ici.",
            "narrateur|Mila tapote le fer du doigt.",
            "enfant-f|Il a une trace de fraise.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|La goutte est tombée, Mila.",
            "enfant-f|Oui, dans l'herbe.",
            "narrateur|Ça sent la terre, un peu tiède.",
            "enfant-f|Et le bois, maman.",
            "maman|Oui, dans l'air.",
            "papa|Le jardin est calme, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|L'arrosoir reste contre la brouette.",
            "narrateur|Un éclat de brouette tient sur le fer.",
        ],
    ),
}


def vet(lines: list[str], cid: str = "") -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    skip_q = cid == "CHK_T0000_P0000_Q0001"
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
        if not skip_q and TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        if not skip_q:
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
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Mila = enfant-f)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé (dump sans camarade)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    if "émeline" in blob:
        raise SystemExit(f"{SID}: Émeline restée")
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
        "c'est de la joie",
        "c est de la joie",
        "j'ai dit",
        "j ai dit",
        "tu as nommé",
        "tu as nomme",
        "tu as partagé",
        "tu partages ta joie",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Mila sourit. Que dit-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "content":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "content | contente | je suis contente | joie | de la joie | partager"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Mila sent de la joie. Que dit-elle ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    if "émeline" in retry.lower():
        raise SystemExit(f"{SID}: retry Émeline")
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
    if "je suis contente" not in opening:
        raise SystemExit(f"{SID}: nommage absent avant la question")
    n_contente = blob.count("je suis contente")
    if n_contente != 1:
        raise SystemExit(f"{SID}: je suis contente ×{n_contente}")
    if "fraise" not in blob:
        raise SystemExit(f"{SID}: manque fraise")
    if "arrosoir" not in blob:
        raise SystemExit(f"{SID}: manque arrosoir")
    if "seau" not in blob:
        raise SystemExit(f"{SID}: manque seau")
    if "molle" not in opening:
        raise SystemExit(f"{SID}: manque fraise molle")
    if "jus" not in blob:
        raise SystemExit(f"{SID}: manque jus")
    if "oiseau" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: manque oiseau (2e ruse)")
    if "s'accroupit" not in opening and "s accroupit" not in opening:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    if "luit" not in opening:
        raise SystemExit(f"{SID}: manque luit à l'ouverture")
    if "tremble" not in opening:
        raise SystemExit(f"{SID}: manque tremble")
    end = by["CHK_T0000_P0000_END"]["text"].lower()
    if "luit" not in end:
        raise SystemExit(f"{SID}: manque luit au climax")
    fin = by["CHK_T0000_P0000_END_F0001"]["text"].lower()
    if "tient" not in fin:
        raise SystemExit(f"{SID}: manque tient à la fin")
    for ban in (
        "éclat de fraise",
        "éclat d'arrosoir",
        "éclat de seau",
        "éclat de panier",
        "éclat de treille",
        "éclat de moule",
        "éclat de tuteur",
        "éclat de saladier",
        "éclat de gomme",
        "éclat de berge",
        "éclat de torchon",
        "éclat de tabouret",
        "éclat de tour",
        "tout doux",
        "tout calme",
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
    if nwords < 700 or nwords > 850:
        raise SystemExit(f"{SID}: {nwords} mots hors 700–850")

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
        "(vécue : fraise trop molle, jus aux doigts, sourire parti, "
        "papa accroupi, Mila s'arrête, tend, dit "
        "« je suis contente » ; 2e ruse : oiseau, jus, fraise molle "
        "dans le seau, elle refuse de foncer). JAMAIS dite en slogan. "
        "Pas « c'est de la joie ». Pas « j'ai dit : je suis ». "
        "Pas « tu as nommé ».\n"
        "- **Personnages :** Mila, papa, maman. Mila = enfant-f "
        "(veut la fraise tiède maintenant). Dump Émeline → Mila. "
        "Pas de copain (dump sans camarade). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** jardin, fraisiers, fin de journée, coin de la "
        "brouette. Dump : fraise, arrosoir, seau. Indice PAS fraise / "
        "arrosoir / seau / panier / treille / torchon.\n"
        "- **Indice unique :** éclat de brouette (luit sur le fer → "
        "tremble à la fraise molle → luit quand l'oiseau se pose → "
        "tient sur le fer). BAN éclat de fraise / arrosoir / seau / "
        "panier / treille / moule / tuteur / saladier / gomme / berge / "
        "torchon / tabouret / tour.\n"
        "- **Question moteur :** « Mila sourit. Que dit-elle ? » "
        "expected dump **content**. accepted dump "
        "`content | contente | je suis contente | joie | de la joie | "
        "partager`. retry dump Émeline → Mila : "
        "`Mila sent de la joie. Que dit-elle ?`. Hors Q : null. "
        "Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / "
        "graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin "
        "heureuse. `chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte reste au bec de l'arrosoir. Seau mouillé. "
        "Sur le fer, un éclat de brouette luit. Mila veut la "
        "fraise tiède **maintenant**. Elle tire trop vite. Fraise "
        "trop molle. Jus. Sourire parti. Envie et peur. Papa "
        "s'accroupit. Elle s'arrête, tend, dit je suis contente. "
        "Merci vécu. Deuxième ruse : oiseau sur la brouette, jus "
        "dans le seau. Elle s'arrête, lit l'éclat. Un éclat de "
        "brouette tient sur le fer. La goutte tombe. Fin fragile.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin, fraisiers, fin de journée, arrosoir, "
        "seau, brouette, fer tiède.\n"
        "- Désir : cueillir la fraise tiède, maintenant.\n"
        "- Objet : fraise, arrosoir, seau. Coin nommé : le fer "
        "de la brouette.\n"
        "- Indice unique : éclat de brouette, vu dès l'ouverture, "
        "payé sur le fer. Pas éclat de fraise / arrosoir / seau.\n"
        "- Urgence douce : elle tire trop vite, trop fort.\n"
        "- Imprévu 1 : fraise trop molle, jus aux doigts, sourire "
        "parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "qu'elle refuse de foncer vers le bout.\n"
        "- Imprévu 2 (plus rusé) : oiseau sur la brouette, jus "
        "dans le seau, la fraise s'écrase.\n"
        "- Résolution : elle refuse de foncer, observe, écoute "
        "le jardin, retrouve l'éclat, l'oiseau prend la goutte.\n"
        "- Retour : trace de fraise sur le fer, goutte tombée, "
        "éclat qui tient. La fin a failli (jus, oiseau).\n\n"
        "## Vécu\n\n"
        "Mila veut prendre **maintenant**. Impatience, puis fraise "
        "molle, sourire parti. Elle s'arrête, tend, dit je suis "
        "contente. Papa se baisse, pose une question, ne récite "
        "pas le mot joie. Ils agissent : bouts tièdes, seau, "
        "oiseau, elle s'arrête. Merci vécu. Fin : l'éclat du "
        "début tient sur le fer.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Mila et la fraise tiède (noyau dump). Relance : "
        "Que dit-elle ? expected content.\n"
        "- Lieu du dump-meta (jardin, fraisiers, fin de journée). "
        "Maman et papa. Mila = héros enfant-f. Dump fraise / "
        "arrosoir / seau gardés comme objets, pas comme indice.\n"
        "- Ouverture inventée (goutte au bec de l'arrosoir, fer "
        "tiède, éclat de brouette), pas un gabarit v2, pas "
        "« Émeline est dans le jardin ».\n"
        "- Indice unique : éclat de brouette ×4. BAN éclat de "
        "fraise / arrosoir / seau / panier / treille / moule / "
        "tuteur / saladier / gomme / berge / torchon / tabouret / "
        "tour. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Q moteur sans tic.\n"
        "- Leçon non dite : on la voit quand elle s'arrête, quand "
        "elle tend, quand elle dit je suis contente. Pas « c'est "
        "de la joie ». Pas « tu as nommé ». Une seule « je suis "
        "contente ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur conservée (Émeline → Mila). "
        "expected/accepted dump. retry Émeline → Mila. Hors Q : "
        "null. 5 chunks, kinds inchangés.\n"
        "- example4 060 / 092 / 024 (manière volée, gabarit non "
        "collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N2.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, "
        "sous-texte, tempo, sourire, respiration). `slow` = "
        "question et fin. Action un peu plus vive vers l'oiseau.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
