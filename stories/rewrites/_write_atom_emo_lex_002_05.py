#!/usr/bin/env python3
"""ATOM-EMO.LEX.002-05 — Victorino et le train en bois (F-NAR-019, N3, EMO.LEX.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.002-05"
TITLE = "Victorino et le train en bois"
N3 = LIMITS["N3"]
CHARS = "Victorino, Amir, papa, maman"
SETTING = (
    "chambre, puis salon, coffre, train en bois, wagon, "
    "rail, lit, tapis, canapé, manteau, tasse"
)
INDICE = "éclat de coffre"
FIL = (
    "La poignée du coffre est tiède. Sur le couvercle, "
    "un éclat de coffre luit. Victorino veut le train en bois, "
    "maintenant, avec Amir. Le train n'est pas là. Sourire parti. "
    "Poitrine serrée. Yeux chauds. Papa s'accroupit. "
    "Victorino dit qu'il est triste. Il pleure. Il demande un câlin. "
    "Merci vécu. Deuxième ruse : Amir rentre chez lui, train toujours "
    "perdu. Il refuse de foncer. Un éclat de coffre tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(merle|miel|treille|moule|tuteur|saladier|gomme|berge|"
    r"brouette|fauteuil|paillasson|capuche|plaid|coussin|"
    r"grand-père|grand-pere|jardinier|bibliothécaire|bibliothecaire|"
    r"gardienne|maîtresse|maitresse|étienne|etienne|nora)\b",
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
    "éclat de wagon",
    "éclat de bois",
    "éclat de lit",
    "éclat de tapis",
    "éclat de canapé",
    "éclat de canape",
    "éclat de fauteuil",
    "éclat de paillasson",
    "éclat de couverture",
    "éclat de capuche",
    "éclat de treille",
    "éclat de moule",
    "éclat de tuteur",
    "éclat de saladier",
    "éclat de gomme",
    "éclat de berge",
    "éclat de brouette",
    "éclat de chaise",
    "éclat de manteau",
    "éclat de tasse",
    "éclat de rail",
    "éclat de tour",
    "éclat de cube",
    "éclat de doudou",
    "éclat de lampe",
    "éclat de plaid",
    "éclat de coussin",
    "toute calme",
    "tout calme",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de coffre",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis tristesse; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_train_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Victorino",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=victorino_a_les_yeux_chauds_que_dit_il; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
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
        emphasis="éclat de coffre",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=amir_rentre_train_perdu_il_refuse_de_foncer; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de coffre",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_soulagement; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "triste",
    "accepted_examples": "triste | je suis triste | câlin | un câlin | pleurer",
    "retry_prompt": "Victorino peut demander un câlin. Que dit-il ?",
    "engine_ok_text": "Oui, triste.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "coffre",
        [
            "narrateur|La poignée du coffre est tiède, sous la fenêtre.",
            "enfant-m|Elle est chaude, papa.",
            "papa|Tu la sens, la poignée ?",
            "enfant-m|Oui, papa.",
            "narrateur|Amir est assis près du tapis, les genoux pliés.",
            "copain|Ça sent le vernis.",
            "maman|Tu le sens, Amir ?",
            "copain|Oui, maman.",
            "narrateur|La chambre sent le vernis, un peu.",
            "enfant-m|On fait le train, Amir ?",
            "copain|Le train en bois, oui.",
            "narrateur|Un wagon rouge attend sur la chaise, tout seul.",
            "enfant-m|Il manque le train.",
            "narrateur|Un rail court un peu, près du lit.",
            "copain|On va jusqu'au salon ?",
            "enfant-m|Oui, maintenant !",
            "maman|Vous partez tout de suite ?",
            "enfant-m|Oui, maman.",
            "narrateur|Sur le couvercle, un éclat de coffre luit.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-m|Oui, un grain clair.",
            "copain|Il est sur le bois.",
            "narrateur|Papa plie une couverture, près du lit.",
            "papa|Je plie ça, d'accord ?",
            "enfant-m|Le train d'abord.",
            "narrateur|En ce moment, Victorino cherche le train en bois.",
            "enfant-m|Je le veux, maintenant !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|Victorino fouille sous le lit trop vite, et sa main sort vide.",
            "enfant-m|Pas là.",
            "copain|Sous le tapis ?",
            "enfant-m|Je regarde.",
            "narrateur|Il soulève le tapis, trop vite.",
            "narrateur|Le train n'est pas là.",
            "enfant-m|Papa, il n'est pas là.",
            "papa|On cherche ensemble ?",
            "enfant-m|Oui.",
            "narrateur|Amir ouvre le coffre trop fort, et le couvercle claque contre le mur.",
            "copain|Aïe, le bois.",
            "enfant-m|Il n'est pas dedans.",
            "maman|Vous avez regardé au fond ?",
            "enfant-m|Vite, oui.",
            "narrateur|Le sourire de Victorino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "enfant-m|J'ai mal au ventre.",
            "narrateur|Ses yeux deviennent chauds.",
            "narrateur|Une larme tombe sur le tapis.",
            "enfant-m|Je suis triste.",
            "narrateur|Victorino pleure un peu, sans crier.",
            "narrateur|Les larmes coulent sur ses joues.",
            "papa|Tu as les yeux chauds, Victorino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "maman|Tes mains sont chaudes, Victorino ?",
            "enfant-m|Un peu, maman.",
            "enfant-m|Je veux un câlin.",
            "maman|Viens.",
            "narrateur|Papa ouvre les bras.",
            "narrateur|Victorino se blottit contre papa.",
            "narrateur|Le câlin est chaud, près du cou.",
            "narrateur|Ça sent le savon de papa.",
            "narrateur|L'éclat de coffre tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorino a les yeux chauds.",
            "narrateur|Que dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Victorino reste contre papa, un moment.",
            "enfant-m|Le train, maintenant.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-m|Je le prends.",
            "narrateur|Victorino avance les mains, trop vite.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Victorino refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe la chambre, un instant.",
            "narrateur|Il écoute le coffre, près du tapis.",
            "papa|Tu restes un peu, Victorino ?",
            "enfant-m|Oui, papa.",
            "papa|Merci, Victorino.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le câlin est tiède, sous les bras.",
            "enfant-m|Il est chaud.",
            "copain|On va au salon ?",
            "enfant-m|Oui, Amir.",
            "narrateur|La poitrine de Victorino ralentit un peu.",
            "maman|Tes joues sont mouillées, Victorino ?",
            "enfant-m|Un peu, maman.",
            "papa|On cherche sans se presser ?",
            "enfant-m|Oui.",
            "narrateur|Maman essuie une larme du pouce.",
            "enfant-m|Ça pique les yeux.",
            "narrateur|Le ventre de Victorino se desserre.",
            "papa|On porte le coffre au salon ?",
            "enfant-m|Oui, papa.",
            "copain|Je prends un bord.",
            "narrateur|Papa soulève le coffre, sans se bousculer.",
            "enfant-m|Le train, papa.",
            "papa|On y va, sans se presser.",
            "maman|Vous marchez jusqu'au salon ?",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Ils posent le coffre près du canapé.",
            "narrateur|Une tasse vide attend sur la table.",
            "enfant-m|Le train, maintenant !",
            "narrateur|Amir boutonne son manteau, trop vite.",
            "copain|Je rentre chez moi.",
            "enfant-m|Pas maintenant !",
            "narrateur|Le train n'est pas là, au salon.",
            "narrateur|Victorino avance trop vite vers la porte.",
            "enfant-m|Amir, attends !",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Victorino refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le coffre, un instant.",
            "narrateur|Il écoute le salon, près du canapé.",
            "narrateur|Sur le couvercle, un éclat de coffre luit.",
            "enfant-m|Là, sur le bois.",
            "papa|On tient le bord ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa ouvre le coffre, sans se presser.",
            "narrateur|Un rail glisse, puis un wagon.",
            "enfant-m|Le train !",
            "narrateur|Le train en bois reste coincé sous un rabat.",
            "enfant-m|Il est coincé !",
            "maman|Tu le vois, le bois ?",
            "enfant-m|Oui, maman.",
            "narrateur|Victorino veut tirer, tout de suite.",
            "narrateur|Puis il lâche le rabat.",
            "papa|J'y vais, Victorino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa glisse la main, sans se presser.",
            "narrateur|Le train faillit rester coincé.",
            "enfant-m|Doucement.",
            "papa|Je le tiens.",
            "narrateur|Papa tire le train, tout petit à petit.",
            "enfant-m|Mon train !",
            "narrateur|Victorino le serre contre lui.",
            "maman|Le bois est tiède, Victorino ?",
            "enfant-m|Un peu.",
            "papa|Une roue est un peu marquée.",
            "enfant-m|Elle a une trace.",
            "papa|Tu vois le point, Victorino ?",
            "enfant-m|Oui, papa.",
            "papa|On reste près du coffre ?",
            "enfant-m|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du coffre.",
            "narrateur|Maman essuie un peu de vernis.",
            "enfant-m|Amir est rentré, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, près de la porte.",
            "maman|On est bien, ici.",
            "narrateur|Victorino tapote le bois du doigt.",
            "enfant-m|Il a une roue marquée.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|Le train est resté, Victorino.",
            "enfant-m|Oui, avec la roue.",
            "narrateur|Ça sent le vernis, un peu tiède.",
            "enfant-m|Et le bois, maman.",
            "maman|Oui, dans l'air.",
            "papa|Le salon est doux, Victorino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le train reste contre le coffre.",
            "narrateur|Un éclat de coffre tient sur le bois.",
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
        if not skip_q:
            for bad in EXTRA_BAD:
                if bad in low:
                    raise SystemExit(f"extra {bad}: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-m", "copain"):
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
        if cid != "CHK_T0000_P0000_Q0001":
            by[cid]["expected_answer"] = None
            by[cid]["accepted_examples"] = None
            by[cid]["retry_prompt"] = None
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
    if INDICE not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé au climax")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Victorino = enfant-m, Amir = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Amir absent (copain)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m", "copain") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "enfant-m" for r in roles):
        raise SystemExit(f"{SID}: enfant-m absent")
    if not any(r == "copain" for r in roles):
        raise SystemExit(f"{SID}: copain absent")
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
    if q["text"] != "Victorino a les yeux chauds. Que dit-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "triste":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "triste | je suis triste | câlin | un câlin | pleurer"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Victorino peut demander un câlin. Que dit-il ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    if "étienne" in retry.lower() or "etienne" in retry.lower():
        raise SystemExit(f"{SID}: retry Étienne non renommé")
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
    if "train" not in blob:
        raise SystemExit(f"{SID}: manque train")
    if "bois" not in blob:
        raise SystemExit(f"{SID}: manque bois")
    if "chambre" not in blob:
        raise SystemExit(f"{SID}: manque chambre")
    if "salon" not in blob:
        raise SystemExit(f"{SID}: manque salon")
    if "wagon" not in blob:
        raise SystemExit(f"{SID}: manque wagon")
    if "lit" not in blob:
        raise SystemExit(f"{SID}: manque lit")
    if "tapis" not in blob:
        raise SystemExit(f"{SID}: manque tapis")
    if "canapé" not in blob and "canape" not in blob:
        raise SystemExit(f"{SID}: manque canapé")
    if "je rentre chez moi" not in blob:
        raise SystemExit(f"{SID}: manque Amir rentre chez lui")
    if "s'accroupit" not in opening and "s accroupit" not in opening:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    if "sourire" not in opening or "disparaît" not in opening:
        if "disparait" not in opening:
            raise SystemExit(f"{SID}: manque sourire parti")
    if "poitrine" not in opening:
        raise SystemExit(f"{SID}: manque poitrine")
    if "n'est pas là" not in by["CHK_T0000_P0000_END"]["text"].lower() and (
        "n est pas la" not in by["CHK_T0000_P0000_END"]["text"].lower()
    ):
        raise SystemExit(f"{SID}: manque train toujours perdu au salon")
    if "papa" not in by["CHK_T0000_P0000_END"]["script"].lower():
        raise SystemExit(f"{SID}: papa absent au 2e imprévu")
    for ban in (
        "éclat de wagon",
        "éclat de bois",
        "éclat de lit",
        "éclat de tapis",
        "éclat de canapé",
        "éclat de canape",
        "éclat de fauteuil",
        "éclat de paillasson",
        "éclat de couverture",
        "éclat de capuche",
        "éclat de treille",
        "éclat de moule",
        "éclat de tuteur",
        "éclat de saladier",
        "éclat de gomme",
        "éclat de berge",
        "éclat de brouette",
        "tout doux",
        "tout calme",
        "toute calme",
        "merle",
        "miel",
        "étienne",
        "etienne",
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
        "- **Public :** N3 (≤16 mots/phrase), audio familial, voc 5–6 ans\n"
        "- **Leçon :** EMO.LEX.002 — nommer la tristesse + demander un "
        "câlin (vécue : train perdu, sourire parti, poitrine serrée, "
        "yeux chauds, Victorino dit je suis triste, pleure, demande un "
        "câlin, papa ouvre les bras ; 2e ruse : Amir rentre chez lui, "
        "train toujours perdu, il refuse de foncer, éclat de coffre, "
        "papa trouve). JAMAIS dite dans le récit. Pas « pleurer est "
        "permis ». Pas « le câlin aide ». Pas « c'est de la tristesse ». "
        "Pas « j'ai dit : je suis ».\n"
        "- **Personnages :** Victorino, Amir, papa, maman. Victorino = "
        "héros enfant-m (veut le train maintenant). Amir = copain "
        "(deux D16). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** chambre, puis salon. Dump train / bois / wagon / "
        "lit / tapis / canapé gardés comme objets, pas comme indice.\n"
        "- **Indice unique :** éclat de coffre (luit à l'ouverture → "
        "tremble aux larmes → luit quand Amir part et le train manque → "
        "tient sur le bois). BAN éclat de wagon / bois / lit / tapis / "
        "canapé / fauteuil / paillasson / couverture / capuche. Pas "
        "treille / moule / tuteur / saladier / gomme / berge / brouette.\n"
        "- **Question moteur :** « Victorino a les yeux chauds. Que "
        "dit-il ? » expected dump **triste**. accepted dump "
        "`triste | je suis triste | câlin | un câlin | pleurer`. "
        "retry dump Étienne → Victorino. Non récitée dans les autres "
        "chunks. Hors Q : expected / accepted / retry nuls.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La poignée du coffre est tiède, sous la fenêtre. Vernis. Amir "
        "près du tapis. Wagon rouge. Sur le couvercle, un éclat de coffre "
        "luit. Victorino veut le train **maintenant**, jusqu'au salon. "
        "Le train n'est pas là. Sourire parti. Poitrine serrée. Yeux "
        "chauds. Papa s'accroupit. Je suis triste. Un câlin. Merci vécu. "
        "Deuxième ruse : Amir rentre, train toujours perdu. Il s'arrête, "
        "lit l'éclat. Papa trouve. Un éclat de coffre tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chambre, poignée tiède, vernis, tapis, lit, wagon.\n"
        "- Désir : faire rouler le train en bois jusqu'au salon, "
        "maintenant, avec Amir.\n"
        "- Objet : train en bois, wagon, rail, coffre.\n"
        "- Indice unique : éclat de coffre, vu dès l'ouverture, payé "
        "sur le bois. Pas éclat de wagon / bois / lit / tapis / canapé.\n"
        "- Urgence douce : il fouille trop vite, trop fort.\n"
        "- Imprévu 1 : train absent, coffre claqué, sourire parti, "
        "poitrine serrée, larmes.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le câlin.\n"
        "- Imprévu 2 (plus rusé) : Amir rentre chez lui, train toujours "
        "perdu au salon, coincé sous un rabat.\n"
        "- Résolution : il refuse de foncer, observe, écoute le salon, "
        "retrouve l'éclat. Papa tire tout petit à petit.\n"
        "- Retour : roue marquée, train contre le coffre, éclat sur le "
        "bois. Dénouement qui a failli : Amir est parti, le train "
        "faillit rester coincé.\n\n"
        "## Vécu\n\n"
        "Victorino veut le train **maintenant**. Impatience, puis lit "
        "vide, sourire parti. Il dit je suis triste, pleure, demande un "
        "câlin. Papa ouvre les bras. Papa se baisse, pose une question, "
        "ne récite pas la règle. Ils agissent : chercher sans se presser, "
        "porter le coffre, tenir le bord, papa trouve. Merci vécu. Fin : "
        "l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Victorino et le train en bois (noyau dump). Relance : "
        "Que dit-il ? expected triste.\n"
        "- Lieu du dump-meta (chambre, puis salon). Maman et papa. "
        "Victorino = héros enfant-m. Amir = copain. Dump train / bois / "
        "wagon / lit / tapis / canapé.\n"
        "- Ouverture inventée (poignée tiède, vernis), pas un gabarit "
        "v2, pas « Une poussière danse », pas « L'histoire est finie ».\n"
        "- Indice unique : éclat de coffre ×4. BAN éclat de wagon / "
        "bois / lit / tapis / canapé / fauteuil / paillasson / "
        "couverture / capuche. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « j'ai dit : je suis », « pleurer est permis ».\n"
        "- Leçon non dite : on la voit quand les yeux sont chauds, "
        "quand Victorino dit je suis triste, quand il pleure, quand il "
        "demande un câlin. Pas « pleurer est permis ». Pas « le câlin "
        "aide ». Pas « j'ai dit : je suis ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Victorino a les yeux chauds. Que dit-il ? ». "
        "expected triste. 5 chunks, kinds inchangés. expected/accepted "
        "dump conservés. retry Étienne → Victorino. Hors Q : null.\n"
        "- example4 065 / 097 / 029 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N3.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers Amir qui part.\n"
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
