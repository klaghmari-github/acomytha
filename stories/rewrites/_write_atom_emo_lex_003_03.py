#!/usr/bin/env python3
"""ATOM-EMO.LEX.003-03 — Victorina et le bac à sable (F-NAR-019, N2, EMO.LEX.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.003-03"
TITLE = "Victorina et le bac à sable"
N2 = LIMITS["N2"]
CHARS = "Victorina, papa, maman"
SETTING = (
    "parc, aiguilles de pin, bac, sable, balançoire, "
    "pelle, seau, pin, manche"
)
INDICE = "éclat de pelle"
FIL = (
    "Victorina connaît le parc. Les aiguilles de pin craquent. "
    "Sur le manche, un éclat de pelle luit. Elle veut la "
    "balançoire, maintenant. Les balançoires sont prises. "
    "Sourire parti. Poitrine trop vite. Papa s'accroupit. "
    "Elle dit je suis déçue. Elle va au bac. Elle creuse. "
    "Merci vécu. Deuxième ruse : bac occupé, pelle coincée. "
    "Elle refuse de foncer. Un éclat de pelle tient sur le manche."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(merle|miel|maîtresse|maitresse|grand-père|grand-pere|"
    r"jardinier|bibliothécaire|bibliothecaire|gardienne|"
    r"grille|banc|cagette|kiosque|capuche|couverture|"
    r"paillasson|fauteuil|coffre|haie|housse|brouette|"
    r"treille|toboggan|sonnette|tapis|rideau|plaid|"
    r"norah?|céline|celine)\b",
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
    "tu as dit",
    "on peut chercher",
    "on cherche une autre idée",
    "c'est une autre idée",
    "c est une autre idée",
    "une autre idée peut",
    "ce n'est pas honteux",
    "ce n est pas honteux",
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
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de sable",
    "éclat de pin",
    "éclat de seau",
    "éclat de grille",
    "éclat de banc",
    "éclat de cagette",
    "éclat de kiosque",
    "éclat de capuche",
    "éclat de couverture",
    "éclat de paillasson",
    "éclat de fauteuil",
    "éclat de coffre",
    "éclat de haie",
    "éclat de housse",
    "éclat de brouette",
    "éclat de treille",
    "éclat de bac",
    "éclat de tour",
    "éclat de cube",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de pelle",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=élan puis déception; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_balancoire_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="balançoires",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=les_balancoires_sont_prises_quelle_emotion; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="bac",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis souffle_plus_large; intensite=2; "
            "destinataire=enfant; sous_texte=elle_nomme_puis_elle_creuse_au_bac; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de pelle",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=bac_occupe_pelle_coincee_elle_refuse_de_foncer; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de pelle",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_manche; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "déçu",
    "accepted_examples": "déçu | déçue | autre idée | le bac",
    "retry_prompt": "Elle nomme. Puis elle cherche quoi ?",
    "engine_ok_text": "Oui, déçu.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc",
        [
            "narrateur|Victorina connaît le parc, ses odeurs, ses bruits.",
            "enfant-f|Je le connais, papa.",
            "papa|Tu le connais, le parc ?",
            "enfant-f|Oui, papa.",
            "narrateur|Les aiguilles de pin craquent sous les chaussures.",
            "enfant-f|Elles craquent, maman.",
            "maman|Tu les entends, les aiguilles ?",
            "enfant-f|Oui, maman.",
            "narrateur|Ça sent le pin, un peu tiède.",
            "enfant-f|Ça sent le pin.",
            "papa|Tu le sens, le pin ?",
            "enfant-f|Oui, papa.",
            "narrateur|Une pelle rouge attend près du bac.",
            "enfant-f|Elle est rouge !",
            "maman|Tu la vois, la pelle ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sur le manche, un éclat de pelle luit.",
            "enfant-f|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Un seau jaune repose contre le sable.",
            "enfant-f|Le seau est jaune.",
            "papa|Il attend, près du bac.",
            "enfant-f|Oui.",
            "narrateur|Les chaînes des balançoires cliquettent, plus loin.",
            "enfant-f|Je les entends.",
            "maman|Elles bougent, Victorina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Un détail paraît nouveau, sur le manche.",
            "enfant-f|Le point clair.",
            "papa|Tu le regardes, Victorina ?",
            "enfant-f|Oui, papa.",
            "narrateur|En ce moment, Victorina veut la balançoire.",
            "enfant-f|Je veux celle-là, maintenant !",
            "papa|Tout de suite ?",
            "enfant-f|Oui, papa.",
            "narrateur|Victorina court trop vite vers les chaînes.",
            "narrateur|Les deux balançoires bougent, occupées.",
            "narrateur|Il n'y a plus de place.",
            "enfant-f|Elles sont prises.",
            "narrateur|Le sourire de Victorina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Sa poitrine va trop vite.",
            "enfant-f|Oh.",
            "papa|Elles sont prises, Victorina ?",
            "enfant-f|Oui, papa.",
            "maman|Tes épaules tombent, Victorina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de pelle tremble, puis tient.",
            "narrateur|Papa s'accroupit à la même hauteur, sans parler.",
            "enfant-f|Je suis déçue.",
            "papa|Tu as une boule, Victorina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ses épaules restent basses, près des chaînes.",
            "narrateur|Elle tourne la tête vers le bac.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Les balançoires sont prises.",
            "narrateur|Quelle émotion ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Victorina reste près des chaînes, un instant.",
            "enfant-f|Je ne peux pas.",
            "papa|Tu regardes où, Victorina ?",
            "enfant-f|Le bac.",
            "narrateur|Elle avance trop vite vers le sable.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Victorina refuse de foncer.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le bac, un instant.",
            "narrateur|Elle écoute le parc, près des aiguilles.",
            "enfant-f|Le bac, alors.",
            "maman|Tu vas vers le sable ?",
            "enfant-f|Oui, maman.",
            "narrateur|Victorina s'agenouille près du bac.",
            "narrateur|Le sable est frais, un peu lourd.",
            "enfant-f|Il est froid.",
            "papa|Tes mains sont dedans ?",
            "enfant-f|Oui, papa.",
            "narrateur|Victorina creuse avec les doigts.",
            "narrateur|Un petit trou s'ouvre, tout près du seau.",
            "enfant-f|Un trou, papa.",
            "papa|Merci, Victorina.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le seau jaune est vide, Victorina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Elle pousse un peu de sable dans le seau.",
            "enfant-f|Il se remplit.",
            "papa|Le sable tient, Victorina ?",
            "enfant-f|Un peu, papa.",
            "maman|Tes doigts sont froids, Victorina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le ventre de Victorina se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "enfant-f|Je creuse.",
            "papa|On reste près du bac ?",
            "enfant-f|Oui.",
            "maman|Les aiguilles de pin restent au bord ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le trou s'agrandit, sans se presser.",
            "enfant-f|Il est à moi.",
            "papa|Le sable est lourd, Victorina ?",
            "enfant-f|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Des aiguilles de pin occupent le bac.",
            "enfant-f|Le bac est plein !",
            "narrateur|Victorina veut la pelle, tout de suite.",
            "narrateur|Le manche ne bouge pas.",
            "enfant-f|Elle est coincée !",
            "narrateur|La lame reste sous le sable lourd.",
            "narrateur|Victorina tire trop vite sur le manche.",
            "narrateur|La pelle reste coincée, au fond.",
            "enfant-f|Elle ne vient pas.",
            "narrateur|Victorina avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Victorina refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe la pelle, un instant.",
            "narrateur|Elle écoute le parc, près du bac et du sable.",
            "narrateur|Sur le manche, un éclat de pelle luit.",
            "enfant-f|Là, sur le manche.",
            "papa|Tu vois le point, Victorina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Victorina écarte les aiguilles, sans se presser.",
            "narrateur|Le sable autour de la lame s'ouvre.",
            "enfant-f|Un peu, papa.",
            "maman|La lame bouge, Victorina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Elle creuse autour, tout près de la lame.",
            "narrateur|La pelle se libère, presque.",
            "enfant-f|Elle vient !",
            "papa|Tu la tiens, Victorina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le trou a failli se refermer.",
            "narrateur|Victorina pose la pelle, sans se presser.",
            "enfant-f|Poumf.",
            "maman|Le sable est lourd, Victorina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Elle creuse un vrai trou, plus large.",
            "papa|Le seau se remplit, Victorina ?",
            "enfant-f|Oui, papa.",
            "maman|Tes genoux sont froids, Victorina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le trou tient, au bord du bac.",
            "enfant-f|Il tient.",
            "papa|On reste ici, Victorina ?",
            "enfant-f|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du bac.",
            "narrateur|Maman essuie un peu de sable.",
            "enfant-f|Les balançoires étaient prises, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-f|Oui, près des chaînes.",
            "maman|On est bien, ici.",
            "narrateur|Victorina tapote le manche du doigt.",
            "enfant-f|Il a une trace de sable.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|Le trou est resté, Victorina.",
            "enfant-f|Oui, avec le seau.",
            "narrateur|Ça sent le pin, un peu tiède.",
            "enfant-f|Et le sable, maman.",
            "maman|Oui, dans l'air.",
            "papa|Le parc est calme, Victorina ?",
            "enfant-f|Oui, papa.",
            "narrateur|La pelle reste près du trou.",
            "narrateur|Un éclat de pelle tient sur le manche.",
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
    if "luit" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: manque luit à l'ouverture")
    if "tremble" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: manque tremble à l'ouverture")
    if "luit" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: manque luit au climax")
    if "tient" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: manque tient à la fin")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "je suis déçue" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: manque je suis déçue (acte) à l'ouverture")
    if blob.count("je suis déçue") != 1:
        raise SystemExit(f"{SID}: je suis déçue ×{blob.count('je suis déçue')}")
    if "victorina creuse" not in blob:
        raise SystemExit(f"{SID}: manque victorina creuse")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Victorina = enfant-f)")
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
        "on peut chercher une autre idée",
        "on cherche une autre idée",
        "c'est une autre idée",
        "tu as nommé",
        "j'ai dit : je suis",
        "l'histoire est finie",
        "ce n'est pas honteux",
        "un souhait peut attendre",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Les balançoires sont prises. Quelle émotion ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "déçu":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != "déçu | déçue | autre idée | le bac":
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Elle nomme. Puis elle cherche quoi ?":
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
    if "des aiguilles de pin sont sur le chemin" in opening:
        raise SystemExit(f"{SID}: ouverture dump")
    if "ava arrive au parc" in opening:
        raise SystemExit(f"{SID}: ouverture dump (Ava)")
    if "balançoire" not in blob and "balancoire" not in blob:
        raise SystemExit(f"{SID}: manque balançoire")
    if "bac" not in blob:
        raise SystemExit(f"{SID}: manque bac")
    if "sable" not in blob:
        raise SystemExit(f"{SID}: manque sable")
    if "pin" not in blob:
        raise SystemExit(f"{SID}: manque pin")
    if "s'accroupit" not in blob and "s accroupit" not in blob:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    for ban in (
        "éclat de balançoire",
        "éclat de sable",
        "éclat de pin",
        "éclat de seau",
        "éclat de grille",
        "éclat de banc",
        "éclat de cagette",
        "éclat de kiosque",
        "éclat de capuche",
        "éclat de couverture",
        "éclat de paillasson",
        "éclat de fauteuil",
        "éclat de coffre",
        "éclat de haie",
        "éclat de housse",
        "éclat de brouette",
        "éclat de treille",
        "tout doux",
        "tout calme",
        "tout doucement",
        "merle",
        "miel",
    ):
        if ban in blob:
            raise SystemExit(f"{SID}: BAN {ban}")
    if re.search(r"\b(grille|banc)\b", blob):
        raise SystemExit(f"{SID}: BAN grille/banc")
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
        "- **Leçon :** EMO.LEX.003 — nommer la déception + chercher une "
        "autre idée (vécue : Victorina dit « je suis déçue », puis creuse "
        "au bac ; balançoires prises, sourire parti, poitrine trop vite, "
        "papa accroupi ; 2e ruse : bac occupé par les aiguilles, pelle "
        "coincée, elle refuse de foncer). JAMAIS dite dans le récit. Pas "
        "« on peut chercher une autre idée ». Pas « tu as nommé ». Pas "
        "« j'ai dit : je suis ».\n"
        "- **Personnages :** Victorina, papa, maman. Dump Ava → D16 "
        "Victorina = enfant-f (veut la balançoire maintenant). Pas de "
        "copain (dump sans camarade). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** parc, aiguilles de pin, bac, sable, balançoire, "
        "pelle, seau, pin. BAN grille / banc (indice et mot). "
        "Balançoires / bac / sable / pin = dump.\n"
        "- **Indice unique :** éclat de pelle (luit à l'ouverture → "
        "tremble aux balançoires prises → luit quand la pelle est "
        "coincée → tient sur le manche). BAN éclat de balançoire / "
        "sable / pin / seau / grille / banc / cagette / kiosque / "
        "capuche / couverture / paillasson / fauteuil / coffre / haie / "
        "housse / brouette / treille.\n"
        "- **Question moteur :** « Les balançoires sont prises. Quelle "
        "émotion ? » expected dump **déçu**. accepted dump "
        "`déçu | déçue | autre idée | le bac`. retry dump gardé "
        "(sans nom hors D16). Non récitée dans les autres chunks. "
        "Hors Q : expected / accepted / retry = null.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Victorina connaît le parc. Les aiguilles de pin craquent. Un "
        "détail paraît nouveau : sur le manche, un éclat de pelle luit. "
        "Seau jaune, chaînes. Elle veut la balançoire **maintenant**. "
        "Les balançoires sont prises. Poitrine trop vite. Sourire parti. "
        "Papa s'accroupit. « je suis déçue ». Elle va au bac. Elle "
        "creuse. Merci vécu. Deuxième ruse : bac occupé, pelle coincée. "
        "Elle s'arrête, lit l'éclat, creuse autour. Un éclat de pelle "
        "tient sur le manche.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : parc connu, aiguilles de pin, pelle rouge, seau jaune.\n"
        "- Désir : la balançoire, maintenant.\n"
        "- Objet : pelle, bac, sable (objets dump, pas l'indice).\n"
        "- Indice unique : éclat de pelle, vu dès l'ouverture, payé "
        "sur le manche. Pas éclat de balançoire / sable / pin / seau.\n"
        "- Urgence douce : elle court trop vite vers les chaînes.\n"
        "- Imprévu 1 : balançoires prises, poitrine trop vite, sourire "
        "parti, « je suis déçue ».\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le trou.\n"
        "- Imprévu 2 (plus rusé) : aiguilles qui occupent le bac, pelle "
        "coincée sous le sable.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le parc, "
        "retrouve l'éclat, creuse autour de la lame.\n"
        "- Retour : trou qui a failli se refermer, trace de sable sur "
        "le manche, éclat qui tient.\n\n"
        "## Vécu\n\n"
        "Victorina veut la balançoire **maintenant**. Elle dit « je suis "
        "déçue » (acte, une fois). Impatience, puis chaînes occupées, "
        "sourire parti. Elle s'arrête, observe le bac. Papa se baisse, "
        "pose une question, ne récite pas la règle. Elle creuse. Merci "
        "vécu. Pelle coincée. Elle refuse de foncer. Fin : l'éclat du "
        "début tient sur le manche.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Victorina et le bac à sable (noyau dump). Relance : "
        "Quelle émotion ? expected déçu.\n"
        "- Lieu du dump-meta (parc, aiguilles de pin). Maman et papa. "
        "Victorina = héros enfant-f. Dump Ava retiré.\n"
        "- Ouverture inventée (elle connaît le parc, détail nouveau sur "
        "le manche), pas un gabarit v2, pas « Des aiguilles de pin "
        "sont sur le chemin », pas « Ava arrive au parc ».\n"
        "- Indice unique : éclat de pelle. BAN éclat de balançoire / "
        "sable / pin / seau / grille / banc. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » du dump. BAN grille / banc.\n"
        "- Leçon non dite : on la voit quand elle dit « je suis "
        "déçue », quand elle va au bac, quand elle creuse. Pas « on "
        "peut chercher une autre idée ». Pas « tu as nommé ». Pas "
        "« j'ai dit : je suis ». Pas « L'histoire est finie ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Les balançoires sont prises. Quelle "
        "émotion ? ». expected déçu. 5 chunks, kinds inchangés. "
        "expected/accepted/retry dump conservés. Hors Q : null.\n"
        "- example4 070 / 002 / 034 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N2 / raw.js.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers la pelle coincée.\n"
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
