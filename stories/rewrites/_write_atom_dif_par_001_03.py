#!/usr/bin/env python3
"""ATOM-DIF.PAR.001-03 — La petite voiture verte (F-NAR-019, N3, DIF.PAR.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.001-03"
TITLE = "La petite voiture verte"
N3 = LIMITS["N3"]
CHARS = "Mila, Aniss, papa, maman"
SETTING = (
    "école puis parc : casiers, manteau, vitre embuée, "
    "voiture verte, sable, seau"
)
INDICE = "éclat de rond"
FIL = (
    "Un petit rond de doigt s'ouvre sur la vitre. Au bord, un "
    "éclat de rond brille. Mila veut jouer à la voiture, maintenant. "
    "Elle pose trop de questions. Aniss se tait, recule. Sourire "
    "parti, poitrine, papa accroupi. Elle refuse de foncer, referme "
    "la bouche, tend la voiture, attend. Merci vécu. Au parc, seau "
    "trop vite. Un éclat de rond tient au bord."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(parquet|banc|tartine|puits|cigale|flaque|piquet|bol|"
    r"maîtresse|maitresse|valentine|nino|merle|miel)\b",
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
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "on peut jouer",
    "on peut attendre",
    "on n'imite pas",
    "on n imite pas",
    "on ne force pas la parole",
    "ne force pas la parole",
    "tu as su attendre",
    "on peut tendre",
    "ce n'est pas une faute",
    "vous jouez",
    "on joue",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "trois notes",
    "lumière couleur de miel",
    "lumiere couleur de miel",
    "éclat de casier",
    "éclat de vitre",
    "éclat de buée",
    "éclat de buee",
    "éclat de lacet",
    "éclat de cartable",
    "éclat de tapis",
    "éclat de banc",
    "éclat de cube",
    "éclat de parquet",
    "éclat de seau",
    "éclat de manteau",
    "éclat de voiture",
    "éclat de sable",
    "éclat de doigt",
    "éclat de bol",
    "éclat de chiffon",
    "éclat de pinceau",
    "éclat de flaque",
    "éclat de piquet",
    "éclat de casserole",
    "éclat de coussin",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de nappe",
    "éclat de table",
    "éclat de laine",
    "éclat de craie",
    "éclat de moufle",
    "éclat de tableau",
    "éclat de croûte",
    "éclat de croute",
    "éclat de grain",
    "éclat de carreau",
    "éclat de couloir",
    "éclat de bois",
    "éclat de plaque",
    "éclat de dalle",
    "éclat de pierre",
    "éclat de grille",
    "éclat de couvercle",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de poussière",
    "éclat de poussiere",
    "éclat de cour",
    "éclat de galet",
    "éclat de boule",
    "éclat de carte",
    "éclat de sac",
    "éclat de panier",
    "éclat de cloche",
    "éclat de volet",
    "éclat de poire",
    "éclat de pavé",
    "éclat de pave",
    "éclat de parapluie",
    "éclat de bâche",
    "éclat de bache",
    "éclat de crayon",
    "éclat de wagon",
    "éclat de tasse",
    "éclat de lampe",
    "éclat de citron",
    "éclat de fraise",
    "éclat de quille",
    "éclat de clé",
    "éclat de cle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de caillou",
    "éclat de liste",
    "éclat de sonnette",
    "éclat de marche",
    "éclat de pince",
    "éclat de chaise",
    "éclat de tiroir",
    "éclat de botte",
    "éclat de perron",
    "éclat de limace",
    "éclat de robinet",
    "éclat de planche",
    "éclat de cerceau",
    "éclat de drap",
    "éclat de ballon",
    "éclat de figue",
    "éclat de samare",
    "éclat de bassine",
    "éclat d'émail",
    "éclat d'email",
    "éclat d'enveloppe",
    "éclat de enveloppe",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de rond",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_voiture_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="peu",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=aniss_parle_peu_que_fait_mila; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="attend",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_referme_la_bouche_tend_attend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de rond",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=seau_trop_vite_elle_refuse_de_foncer; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de rond",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_au_bord; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "attendre",
    "accepted_examples": "attendre | tendre un jouet | un jouet | elle attend",
    "retry_prompt": "Elle tend un jouet. Elle attend. Que fait Mila ?",
    "engine_ok_text": "Oui, attendre.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "casiers,manteau",
        [
            "narrateur|La fermeture du manteau rouge accroche un casier.",
            "enfant-f|Elle tient, papa.",
            "papa|Tu la tires, Mila ?",
            "enfant-f|Oui, il est froid.",
            "narrateur|Papa libère la fermeture, d'un coup.",
            "narrateur|Une goutte saute sur la vitre.",
            "enfant-f|Elle est ronde.",
            "maman|Tu as vu la goutte, Mila ?",
            "enfant-f|Oui, maman.",
            "narrateur|La vitre est embuée, un peu.",
            "narrateur|Mila pose un doigt au milieu.",
            "narrateur|Un petit rond s'ouvre, net.",
            "narrateur|Au bord, un éclat de rond brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, ce petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Les casiers sentent le bois mouillé.",
            "enfant-f|Ça sent la pluie, maman.",
            "maman|Le goûter est dans la poche ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le bois du casier est froid, sous la paume.",
            "enfant-f|Il pique un peu.",
            "papa|Tes doigts sont froids, Mila ?",
            "enfant-f|Un peu, papa.",
            "narrateur|Un cube jaune attend sur le tapis.",
            "narrateur|Puis un cube bleu, plus loin.",
            "enfant-f|Ils sont lisses.",
            "papa|Le tapis est prêt, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|En ce moment, Mila pose les cubes.",
            "enfant-f|Je veux jouer à la voiture, maintenant !",
            "enfant-f|Pour la maison, au bout du tapis.",
            "maman|Une maison au bout du tapis ?",
            "enfant-f|Oui.",
            "enfant-f|Elle doit arriver tout de suite.",
            "narrateur|La voiture verte est dans sa main.",
            "narrateur|Les roues sont lisses, un peu froides.",
            "narrateur|Aniss arrive près du tapis.",
            "narrateur|Il s'arrête, sans parler.",
            "enfant-f|Tu viens, Aniss ?",
            "enfant-f|On fait la maison ?",
            "enfant-f|Tu prends la voiture ?",
            "narrateur|Les questions tombent trop vite.",
            "enfant-f|Prends-la !",
            "narrateur|Mila tend la voiture trop vite.",
            "narrateur|Aniss recule d'un pas.",
            "narrateur|Ses épaules se serrent.",
            "narrateur|Il ne dit rien.",
            "enfant-f|Aniss ?",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Aniss, Mila ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains tiennent la voiture, Mila ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le petit rond, un instant.",
            "narrateur|L'éclat de rond tremble, puis tient.",
            "enfant-f|L'éclat, papa ?",
            "papa|Tu le vois, toi ?",
            "enfant-f|Oui, sur la vitre.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss parle peu.",
            "narrateur|Que fait Mila ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "voiture,cubes",
        [
            "narrateur|Mila tend la voiture, sans se presser.",
            "enfant-f|Pour la maison.",
            "narrateur|Elle attend, les mains ouvertes.",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Il regarde les roues.",
            "narrateur|Puis il avance un doigt.",
            "narrateur|Il prend la voiture.",
            "narrateur|Il la fait rouler, lentement.",
            "narrateur|Les roues font un petit rrr.",
            "enfant-f|Elle roule.",
            "papa|Tu entends les roues, Mila ?",
            "enfant-f|Oui, papa.",
            "maman|La maison a un toit ?",
            "enfant-f|On pose un cube.",
            "narrateur|Mila pose le jaune, sans se presser.",
            "narrateur|Aniss pose le bleu, plus tard.",
            "copain|Maison.",
            "enfant-f|Maison.",
            "narrateur|La voiture entre sous le toit.",
            "enfant-f|Elle est arrivée.",
            "papa|Elle est arrivée, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le ventre de Mila se desserre.",
            "maman|Merci, Mila.",
            "narrateur|Maman a vu les mains ouvertes.",
            "papa|Le petit rond est sur la vitre ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un éclat de rond luit au bord.",
            "enfant-f|Il est là.",
            "narrateur|Plus tard, ils vont au parc.",
            "enfant-f|Le sable, maman ?",
            "maman|Le seau est dans le sac.",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "sable,seau",
        [
            "narrateur|Le sable du parc est frais, sous les doigts.",
            "enfant-f|Il est froid, papa.",
            "papa|Tu le sens, le sable ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila tient le seau, trop près d'Aniss.",
            "enfant-f|On fait un chemin, maintenant !",
            "narrateur|Elle pousse le seau trop vite.",
            "narrateur|Le sable s'envole un peu.",
            "narrateur|Aniss recule, les épaules hautes.",
            "enfant-f|Oh.",
            "narrateur|Mila refuse de foncer, cette fois.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le seau, un instant.",
            "narrateur|Elle écoute le sable qui tombe.",
            "narrateur|Elle revoit l'éclat de rond.",
            "enfant-f|Le seau, Aniss ?",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Mila tend le seau, sans se presser.",
            "narrateur|Elle attend.",
            "narrateur|Aniss pousse le seau, tout seul.",
            "narrateur|Un chemin de sable s'allonge.",
            "copain|Chemin.",
            "enfant-f|Chemin.",
            "papa|Le chemin va jusqu'au bac, Mila ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains sont sablées, Mila ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Aniss souffle, longuement.",
            "enfant-f|Il a poussé, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-f|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "manteau,vitre",
        [
            "narrateur|Ils reviennent près des casiers.",
            "maman|Le manteau est un peu sec, Mila ?",
            "enfant-f|Oui, maman.",
            "papa|La maison reste au bout du tapis ?",
            "enfant-f|Oui, papa.",
            "narrateur|La voiture verte dort sous le toit.",
            "enfant-f|Elle est arrivée.",
            "copain|Maison.",
            "enfant-f|Le seau a fait un chemin.",
            "papa|Deux jeux, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila pose un doigt sur la vitre.",
            "narrateur|Le petit rond est toujours là.",
            "narrateur|Un éclat de rond tient au bord.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-f", "copain"):
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
    if n_clue != 5:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 5)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Mila = enfant-f, Aniss = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Aniss absent (copain)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f", "copain") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "copain" for r in roles):
        raise SystemExit(f"{SID}: copain absent")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on n'imite pas",
        "on ne force pas la parole",
        "tu as su attendre",
        "on peut attendre",
        "on peut tendre",
        "on peut jouer",
        "on joue",
        "vous jouez",
        "il faut attendre",
        "on doit demander",
        "il faut demander",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Aniss parle peu. Que fait Mila ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "attendre | tendre un jouet | un jouet | elle attend"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Elle tend un jouet. Elle attend. Que fait Mila ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    copain_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    ).lower()
    if len(copain_txt.split()) > 6:
        raise SystemExit(f"{SID}: Aniss parle trop: {copain_txt}")
    for need in (
        "casier",
        "manteau",
        "vitre",
        "voiture",
        "sable",
        "seau",
        "tapis",
        "cube",
    ):
        if need not in blob:
            raise SystemExit(f"{SID}: manque {need}")
    if "embuée" not in blob and "embuee" not in blob:
        raise SystemExit(f"{SID}: manque vitre embuée")
    for ban in (
        "éclat de casier",
        "éclat de vitre",
        "éclat de buée",
        "éclat de buee",
        "éclat de lacet",
        "éclat de cartable",
        "éclat de tapis",
        "éclat de banc",
        "éclat de cube",
        "éclat de parquet",
        "valentine",
        "nino",
        "tout doux",
        "tout calme",
        "parquet",
        "banc",
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
    slow_ids = {
        c["chunk_id"]
        for c in chunks
        if c.get("rate_label") == "slow"
    }
    if slow_ids != {"CHK_T0000_P0000_Q0001", "CHK_T0000_P0000_END_F0001"}:
        raise SystemExit(f"{SID}: slow mal placé: {slow_ids}")

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
        "- **Public :** N3 (≤16 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.PAR.001 — Aniss parle peu (vécue : Mila pose trop "
        "de questions, il recule, elle refuse de foncer, referme la bouche, "
        "tend la voiture, attend ; au parc, seau trop vite, elle attend). "
        "JAMAIS dite. Pas « on n'imite pas ». Pas « on ne force pas la "
        "parole ». Pas « on peut attendre ». Pas « tu as su attendre ».\n"
        "- **Personnages :** Mila, Aniss, papa, maman. Troupe D16. Mila = "
        "enfant-f (veut maintenant, questions, refuse de foncer). Aniss = "
        "copain (parle peu : Maison, Chemin). Papa et maman parlent. Pas "
        "de maîtresse. Valentine / Nino absents.\n"
        "- **Lieu :** école puis parc (casiers, manteau, vitre embuée, "
        "voiture verte, sable, seau). Noyau dump : maison au bout du tapis. "
        "≠ 001-01 parquet / 001-02 banc.\n"
        "- **Indice unique :** éclat de rond (petit rond de doigt sur la "
        "vitre → brille → tremble → luit → revoit → tient au bord). BAN "
        "éclat de casier / vitre / buée / lacet / cartable / tapis / banc / "
        "cube / parquet.\n"
        "- **Question moteur :** « Aniss parle peu. Que fait Mila ? » "
        "expected **attendre**. accepted `attendre | tendre un jouet | un "
        "jouet | elle attend`. retry dump (label, Mila). Non récitée comme "
        "slogan dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La fermeture du manteau rouge accroche un casier. Un doigt ouvre "
        "un petit rond sur la vitre embuée. Au bord, un éclat de rond "
        "brille. Cubes, tapis. Mila veut jouer à la voiture **maintenant**, "
        "pour la maison au bout du tapis. Elle pose trop de questions, tend "
        "trop vite. Aniss se tait, recule. Sourire parti, poitrine, papa "
        "accroupi. Elle refuse de foncer, referme la bouche. Question. Elle "
        "tend la voiture, attend. Maison. Merci vécu. Deuxième ruse : seau "
        "trop vite, sable qui s'envole, Aniss recule. Elle s'arrête, revoit "
        "l'éclat. Un éclat de rond tient au bord.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : école puis parc, casiers, manteau, vitre embuée, cubes, "
        "tapis. ≠ 001-01 parquet / 001-02 banc.\n"
        "- Désir : la voiture verte à la maison, maintenant.\n"
        "- Objet : voiture verte, cubes, seau, sable.\n"
        "- Indice unique : éclat de rond, vu dès l'ouverture, payé au bord "
        "de la vitre. Pas éclat de casier / vitre / buée / tapis / banc.\n"
        "- Urgence douce : elle doit arriver tout de suite.\n"
        "- Imprévu 1 : trop de questions, voiture trop vite, Aniss recule.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après les mains "
        "ouvertes.\n"
        "- Imprévu 2 (plus rusé) : parc, seau trop vite, sable qui s'envole.\n"
        "- Résolution : elle refuse de foncer, referme la bouche, tend, "
        "attend. Aniss pousse le seau.\n"
        "- Retour : maison au bout du tapis, chemin de sable, éclat au "
        "bord.\n\n"
        "## Vécu\n\n"
        "Mila veut **maintenant**. Impatience, questions, Aniss qui recule, "
        "sourire parti. Le silence compte. Papa se baisse, pose une "
        "question, ne récite pas « on peut attendre ». Elle agit : bouche "
        "refermée, voiture tendue, attente. Merci vécu. Fin : l'éclat du "
        "début tient au bord. Le dénouement a failli : Aniss a reculé deux "
        "fois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : La petite voiture verte (roster). Noyau dump conservé : "
        "la maison au bout du tapis. Relance : Que fait Mila ? expected "
        "attendre.\n"
        "- Lieu du dump (école puis parc, casiers, manteau, vitre, voiture, "
        "sable, seau). Maman présente. Aniss = copain.\n"
        "- Ouverture inventée (fermeture du manteau accrochée à un casier), "
        "pas un gabarit v2, pas « Une goutte tombe du manteau rouge » du "
        "dump en première ligne.\n"
        "- Indice unique : éclat de rond. BAN éclat de casier / vitre / "
        "buée / lacet / cartable / tapis / banc / cube / parquet. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés. "
        "Strip slogans du dump : on peut attendre, tu peux tendre un jouet, "
        "on ne force pas la parole, tu as su attendre, bravo.\n"
        "- Leçon non dite : on la voit quand Aniss recule, quand Mila "
        "referme la bouche, quand elle tend et attend. Pas « on n'imite "
        "pas ». Pas « on peut attendre » hors retry label.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Aniss parle peu. Que fait Mila ? ». "
        "expected attendre. retry dump. 5 chunks, kinds inchangés.\n"
        "- example4 026 / 058 / 090 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_ene_001_03.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le seau.\n"
        f"- {nwords} mots. N3 ≤ 16. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n"
        "- 1 × `en ce moment`, 1 × merci adulte, 5 × éclat de rond\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")


if __name__ == "__main__":
    main()
