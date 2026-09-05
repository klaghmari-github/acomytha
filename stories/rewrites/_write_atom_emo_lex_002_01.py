#!/usr/bin/env python3
"""ATOM-EMO.LEX.002-01 — Aniss et le doudou bleu (F-NAR-019, N1, EMO.LEX.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.002-01"
TITLE = "Aniss et le doudou bleu"
N1 = LIMITS["N1"]
CHARS = "Aniss, papa, maman"
SETTING = (
    "chambre, soir, lampe, tapis, lit, doudou, "
    "couverture, oreiller, table"
)
INDICE = "éclat de couverture"
FIL = (
    "Une chaussette glisse du bord du lit. Sur la couverture, "
    "un éclat de couverture luit. Aniss veut le doudou bleu, "
    "maintenant. Le doudou n'est pas là. Sourire parti. "
    "Poitrine serrée. Yeux chauds. Papa s'accroupit. "
    "Aniss dit qu'il est triste. Il pleure. Il demande un câlin. "
    "Merci vécu. Deuxième ruse : le doudou vu, puis disparu, "
    "oreille coincée. Il refuse de foncer. Papa trouve. "
    "Un éclat de couverture tient sur le tissu."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(merle|miel|treille|moule|tuteur|saladier|gomme|berge|"
    r"brouette|torchon|tabouret|plaid|coussin|maîtresse|maitresse|"
    r"grand-père|grand-pere|jardinier|bibliothécaire|bibliothecaire|"
    r"gardienne|norah?)\b",
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
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de treille",
    "éclat de moule",
    "éclat de tuteur",
    "éclat de saladier",
    "éclat de gomme",
    "éclat de berge",
    "éclat de brouette",
    "éclat de torchon",
    "éclat de tabouret",
    "éclat de lit",
    "éclat de tapis",
    "éclat de lampe",
    "éclat de plaid",
    "éclat de coussin",
    "éclat de doudou",
    "éclat de tour",
    "éclat de cube",
    "éclat de rideau",
    "toute calme",
    "tout calme",
)

# N1 : mêmes champs que GES.002-01 (voix N1, tempos plus lents).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat de couverture",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis tristesse; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_doudou_maintenant; "
            "tempo=posé puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=104, speed=0.80, piper=1.36, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=780,
        sentence=360, energy="focused", contour="rising", noise=0.30,
        emphasis="Aniss",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=aniss_a_les_yeux_chauds_que_dit_il; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=122, speed=0.88, piper=1.24, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=620,
        sentence=310, energy="bright", contour="falling", noise=0.33,
        emphasis="câlin",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis soulagement; intensite=2; "
            "destinataire=enfant; sous_texte=il_demande_un_calin_sans_slogan; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de couverture",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=doudou_vu_puis_disparu_oreille_coincée; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de couverture",
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
    "retry_prompt": "Aniss peut demander un câlin. Que dit-il ?",
    "engine_ok_text": "Oui, triste.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "vent",
        [
            "narrateur|Une chaussette glisse du bord du lit.",
            "enfant-m|Elle tombe, papa.",
            "papa|Tu la prends, Aniss ?",
            "enfant-m|Oui, papa.",
            "narrateur|La laine de la couverture sent le savon.",
            "enfant-m|Ça sent le savon, maman.",
            "maman|Tu le sens, le savon tiède ?",
            "enfant-m|Oui, maman.",
            "narrateur|La lampe fait un rond jaune.",
            "enfant-m|Il est sur le tapis.",
            "maman|Tu le vois, le rond ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le lit d'Aniss est un peu défait.",
            "enfant-m|L'oreiller est chaud.",
            "papa|On va lire, Aniss ?",
            "enfant-m|Oui, avec le doudou.",
            "maman|Le doudou bleu ?",
            "enfant-m|Le bleu, maman.",
            "narrateur|Sur la couverture, un éclat de couverture luit.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-m|Oui, un point clair.",
            "papa|La lampe le touche.",
            "narrateur|Un rayon glisse sur le bord.",
            "narrateur|La chambre sent le savon, un peu.",
            "enfant-m|Le doudou d'abord.",
            "narrateur|En ce moment, Aniss cherche le doudou bleu.",
            "enfant-m|Je le veux, maintenant !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|Aniss fouille sous l'oreiller, trop vite.",
            "narrateur|Sa main sort, vide.",
            "enfant-m|Pas là.",
            "maman|Sous la couverture ?",
            "enfant-m|Je regarde.",
            "narrateur|Il soulève la couverture, trop vite.",
            "narrateur|Le doudou n'est pas là.",
            "enfant-m|Maman, il n'est pas là.",
            "maman|On cherche, Aniss ?",
            "enfant-m|Oui.",
            "narrateur|Il regarde le tapis, près du lit.",
            "narrateur|Rien de bleu, sous ses genoux.",
            "enfant-m|Il est parti.",
            "papa|Tu le cherches où ?",
            "enfant-m|Partout.",
            "narrateur|Aniss avance trop vite vers la table.",
            "narrateur|Sa main heurte une chaise.",
            "enfant-m|Aïe.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Dans sa poitrine, ça se serre.",
            "narrateur|L'envie et la peur se heurtent.",
            "narrateur|Ses épaules tombent un peu.",
            "enfant-m|J'ai mal au ventre.",
            "narrateur|Ses yeux deviennent chauds.",
            "narrateur|Une larme tombe sur le tissu.",
            "enfant-m|Je suis triste.",
            "narrateur|Aniss pleure un peu, sans crier.",
            "narrateur|Les larmes coulent sur ses joues.",
            "papa|Tu as les yeux chauds, Aniss ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "maman|Tes mains sont chaudes, Aniss ?",
            "enfant-m|Un peu, maman.",
            "enfant-m|Je veux un câlin.",
            "maman|Viens.",
            "narrateur|Maman ouvre les bras.",
            "narrateur|Aniss se blottit contre maman.",
            "narrateur|Le câlin est chaud, près du cou.",
            "narrateur|Ça sent le savon de maman.",
            "narrateur|L'éclat de couverture tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss a les yeux chauds.",
            "narrateur|Que dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Aniss reste contre maman, un moment.",
            "enfant-m|Le doudou, maintenant.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-m|Je le prends.",
            "narrateur|Aniss avance les mains, trop vite.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Aniss refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe la chambre, un instant.",
            "narrateur|Il écoute le soir, près du lit.",
            "papa|Tu restes un peu, Aniss ?",
            "enfant-m|Oui, papa.",
            "papa|Merci, Aniss.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le câlin est tiède, sous les bras.",
            "enfant-m|Il est chaud.",
            "narrateur|La poitrine d'Aniss ralentit un peu.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tes joues sont mouillées, Aniss ?",
            "enfant-m|Un peu, maman.",
            "papa|On cherche sans se presser ?",
            "enfant-m|Oui.",
            "narrateur|Maman essuie une larme du pouce.",
            "enfant-m|Ça pique les yeux.",
            "maman|La lampe éclaire le tapis ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le ventre d'Aniss se desserre.",
            "papa|On regarde près de la table ?",
            "enfant-m|Oui, papa.",
            "narrateur|Aniss tient le tissu de maman.",
            "enfant-m|Je reste un peu.",
            "narrateur|Ils se lèvent, sans se bousculer.",
            "enfant-m|Le bleu, papa.",
            "papa|On y va, sans se presser.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Papa se baisse près de la table.",
            "narrateur|Un bout bleu passe, une seconde.",
            "enfant-m|Le doudou !",
            "narrateur|Aniss avance trop vite, tout de suite.",
            "narrateur|Le bout bleu disparaît.",
            "enfant-m|Il part !",
            "narrateur|L'oreille glisse sous le lit.",
            "narrateur|Aniss avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Aniss refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le bord, un instant.",
            "narrateur|Il écoute la chambre, près du tapis.",
            "narrateur|Sur la couverture, un éclat de couverture luit.",
            "enfant-m|Là, sur le tissu.",
            "papa|On tient le bord ?",
            "enfant-m|Oui, papa.",
            "narrateur|La couverture pend un peu, sous le lit.",
            "narrateur|Une oreille bleue reste coincée.",
            "enfant-m|Elle est coincée !",
            "maman|Tu la vois, l'oreille ?",
            "enfant-m|Oui, maman.",
            "narrateur|Aniss veut tirer, tout de suite.",
            "narrateur|Puis il lâche le tissu.",
            "papa|J'y vais, Aniss ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa glisse la main, sans se presser.",
            "narrateur|L'oreille part presque plus loin.",
            "enfant-m|Doucement.",
            "papa|Je la tiens.",
            "narrateur|Papa tire le doudou, tout petit à petit.",
            "narrateur|Le bleu revient vers le tapis.",
            "enfant-m|Mon doudou !",
            "narrateur|Aniss le serre contre lui.",
            "maman|Le tissu est tiède, Aniss ?",
            "enfant-m|Un peu.",
            "papa|L'oreille est un peu froissée.",
            "enfant-m|Elle a une trace.",
            "narrateur|Le doudou sent le savon, un peu.",
            "enfant-m|Et la laine.",
            "papa|On reste près du lit ?",
            "enfant-m|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du lit.",
            "narrateur|Maman essuie un peu de laine.",
            "enfant-m|Papa a trouvé le doudou.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, sous le bord.",
            "maman|On est bien, ici.",
            "narrateur|Aniss tapote le tissu du doigt.",
            "enfant-m|Il a une oreille froissée.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|Le doudou est resté, Aniss.",
            "enfant-m|Oui, avec l'oreille.",
            "narrateur|Ça sent le savon, un peu tiède.",
            "enfant-m|Et la laine, maman.",
            "maman|Oui, dans l'air.",
            "papa|La chambre est douce, Aniss ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le doudou reste contre le lit.",
            "narrateur|Un éclat de couverture tient sur le tissu.",
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
        raise SystemExit(f"{SID}: enfant-f (Aniss = enfant-m)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé (dump sans camarade)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
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
    if q["text"] != "Aniss a les yeux chauds. Que dit-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "triste":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "triste | je suis triste | câlin | un câlin | pleurer"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Aniss peut demander un câlin. Que dit-il ?":
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
    if "doudou" not in blob:
        raise SystemExit(f"{SID}: manque doudou")
    if "lampe" not in blob:
        raise SystemExit(f"{SID}: manque lampe")
    if "tapis" not in blob:
        raise SystemExit(f"{SID}: manque tapis")
    if "lit" not in blob:
        raise SystemExit(f"{SID}: manque lit")
    if "s'accroupit" not in opening and "s accroupit" not in opening:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    if "sourire" not in opening:
        raise SystemExit(f"{SID}: manque sourire parti")
    if "poitrine" not in opening:
        raise SystemExit(f"{SID}: manque poitrine")
    if "coincée" not in by["CHK_T0000_P0000_END"]["text"].lower() and (
        "coincee" not in by["CHK_T0000_P0000_END"]["text"].lower()
    ):
        raise SystemExit(f"{SID}: manque oreille coincée")
    if "disparaît" not in by["CHK_T0000_P0000_END"]["text"].lower() and (
        "disparait" not in by["CHK_T0000_P0000_END"]["text"].lower()
    ):
        raise SystemExit(f"{SID}: manque doudou disparu")
    if "papa" not in by["CHK_T0000_P0000_END"]["script"].lower():
        raise SystemExit(f"{SID}: papa absent au 2e imprévu")
    for ban in (
        "éclat de doudou",
        "éclat de lampe",
        "éclat de tapis",
        "éclat de lit",
        "éclat de plaid",
        "éclat de coussin",
        "éclat de treille",
        "éclat de moule",
        "éclat de tuteur",
        "éclat de saladier",
        "éclat de gomme",
        "éclat de berge",
        "éclat de brouette",
        "éclat de torchon",
        "éclat de tabouret",
        "tout doux",
        "tout calme",
        "toute calme",
        "merle",
        "miel",
        "nora",
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
        "- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans\n"
        "- **Leçon :** EMO.LEX.002 — nommer la tristesse + demander un "
        "câlin (vécue : doudou perdu, sourire parti, poitrine serrée, "
        "yeux chauds, Aniss dit je suis triste, pleure, demande un câlin, "
        "maman ouvre les bras ; 2e ruse : doudou vu puis disparu, oreille "
        "coincée, il refuse de foncer, papa trouve). JAMAIS dite dans le "
        "récit. Pas « pleurer est permis ». Pas « le câlin aide ». Pas "
        "« c'est de la tristesse ». Pas « j'ai dit : je suis ».\n"
        "- **Personnages :** Aniss, papa, maman. Dump Nora → D16 Aniss = "
        "enfant-m (veut le doudou maintenant). Pas de copain (dump sans "
        "camarade). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** chambre, soir, lampe, tapis, lit, doudou, "
        "couverture, oreiller, table. Dump doudou / lampe / tapis / lit "
        "gardés. ≠ plaid / coussin.\n"
        "- **Indice unique :** éclat de couverture (luit à l'ouverture → "
        "tremble aux larmes → luit quand l'oreille est coincée → tient "
        "sur le tissu). BAN éclat de doudou / lampe / tapis / lit / "
        "plaid / coussin. Pas treille / moule / tuteur / saladier / "
        "gomme / berge / brouette / torchon / tabouret.\n"
        "- **Question moteur :** « Aniss a les yeux chauds. Que dit-il ? » "
        "expected dump **triste**. accepted dump "
        "`triste | je suis triste | câlin | un câlin | pleurer`. "
        "retry dump Nora → Aniss (dit-il). Non récitée dans les autres "
        "chunks. Hors Q : expected / accepted / retry nuls.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une chaussette glisse du bord du lit. Savon, lampe, rond jaune "
        "sur le tapis. Sur la couverture, un éclat de couverture luit. "
        "Aniss veut le doudou **maintenant**. Le doudou n'est pas là. "
        "Sourire parti. Poitrine serrée. Yeux chauds. Papa s'accroupit. "
        "Je suis triste. Un câlin. Merci vécu. Deuxième ruse : bout bleu "
        "vu, puis disparu, oreille coincée. Il s'arrête, lit l'éclat. "
        "Papa trouve. Un éclat de couverture tient sur le tissu.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chambre, soir, lampe, tapis, lit, couverture.\n"
        "- Désir : retrouver le doudou bleu, maintenant.\n"
        "- Objet : doudou bleu, puis oreille coincée.\n"
        "- Indice unique : éclat de couverture, vu dès l'ouverture, payé "
        "sur le tissu. Pas éclat de doudou / lampe / tapis / lit.\n"
        "- Urgence douce : il fouille trop vite, trop haut.\n"
        "- Imprévu 1 : doudou absent, sourire parti, poitrine serrée, "
        "larmes.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le câlin.\n"
        "- Imprévu 2 (plus rusé) : doudou vu sous la table, puis disparu, "
        "oreille coincée sous le bord.\n"
        "- Résolution : il refuse de foncer, observe, écoute la chambre, "
        "retrouve l'éclat. Papa tire tout petit à petit.\n"
        "- Retour : oreille froissée, doudou contre le lit, éclat sur le "
        "tissu. Dénouement qui a failli : l'oreille partait plus loin.\n\n"
        "## Vécu\n\n"
        "Aniss veut le doudou **maintenant**. Impatience, puis lit vide, "
        "sourire parti. Il dit je suis triste, pleure, demande un câlin. "
        "Maman ouvre les bras. Papa se baisse, pose une question, ne "
        "récite pas la règle. Ils agissent : chercher sans se presser, "
        "tenir le bord, papa trouve. Merci vécu. Fin : l'éclat du début "
        "tient sur le tissu.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Aniss et le doudou bleu (noyau dump). Relance : "
        "Que dit-il ? expected triste.\n"
        "- Lieu du dump-meta (chambre, soir). Maman et papa. "
        "Aniss = héros enfant-m. Dump doudou / lampe / tapis / lit.\n"
        "- Ouverture inventée (chaussette qui glisse, soir), pas un "
        "gabarit v2, pas « Nora cherche son doudou », pas « L'histoire "
        "est finie ».\n"
        "- Indice unique : éclat de couverture. BAN éclat de doudou / "
        "lampe / tapis / lit / plaid / coussin. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme/toute calme et "
        "`aujourd'hui` retirés. Strip « toute calme » du dump.\n"
        "- Leçon non dite : on la voit quand les yeux sont chauds, "
        "quand Aniss dit je suis triste, quand il pleure, quand il "
        "demande un câlin. Pas « pleurer est permis ». Pas « le câlin "
        "aide ». Pas « j'ai dit : je suis ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Aniss a les yeux chauds. Que dit-il ? ». "
        "expected triste. 5 chunks, kinds inchangés. expected/accepted "
        "dump conservés. retry Nora → Aniss (dit-il). Hors Q : null.\n"
        "- example4 061 / 093 / 025 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N1.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers l'oreille coincée.\n"
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
