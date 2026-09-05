#!/usr/bin/env python3
"""ATOM-DIF.PAR.001-04 — La pièce du puzzle (F-NAR-019, N3, DIF.PAR.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.001-04"
TITLE = "La pièce du puzzle"
N3 = LIMITS["N3"]
CHARS = "Amir, Victorina, papa, maman"
SETTING = (
    "école : classe, crayon jaune sous la table, craie, vitre, "
    "cartable, puzzle d'animaux ; puis parc"
)
INDICE = "éclat de table"
FIL = (
    "Un crayon jaune roule sous la table. Sur le bord, un éclat "
    "de table brille. Amir veut finir le puzzle, maintenant. "
    "Victorina parle peu. Il pousse trop vite : la pièce tombe. "
    "Sourire parti, poitrine, papa accroupi. Il refuse de foncer, "
    "tend la pièce, attend. 2e ruse au parc. Merci vécu. Un éclat "
    "de table tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(bateau|iris|ruben|merle|miel|maîtresse|maitresse|"
    r"seau|camion|tartine|puits|garage|haricot|coussin|"
    r"voiture|banc|parquet|grand-père|grand-pere)\b",
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
    "on peut attendre",
    "on peut jouer",
    "tu as su attendre",
    "on n'imite pas",
    "on n imite pas",
    "on ne force pas",
    "tu peux tendre",
    "tendre un jouet",
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
    "éclat de crayon",
    "éclat de craie",
    "éclat de vitre",
    "éclat de cartable",
    "éclat de rond",
    "éclat de parquet",
    "éclat de banc",
    "éclat de puzzle",
    "éclat de pièce",
    "éclat de piece",
    "éclat de chat",
    "éclat de chien",
    "éclat de pinceau",
    "éclat de buée",
    "éclat de buee",
    "éclat de flaque",
    "éclat de piquet",
    "éclat de bol",
    "éclat de robinet",
    "éclat de cerceau",
    "éclat de drap",
    "éclat de sauge",
    "éclat de chaise",
    "éclat de miette",
    "éclat de pince",
    "éclat de marche",
    "éclat de corde",
    "éclat de caisse",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de tasse",
    "éclat d'orange",
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat d'ombre",
    "éclat de laine",
    "éclat de lampe",
    "éclat de citron",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de pavé",
    "éclat de pave",
    "éclat de bâche",
    "éclat de bache",
    "éclat de poire",
    "éclat de volet",
    "éclat de croissant",
    "éclat de réverbère",
    "éclat de reverbere",
    "éclat de cloche",
    "éclat de corbeille",
    "éclat de sac",
    "éclat de panier",
    "éclat de dorure",
    "éclat de carte",
    "éclat de boule",
    "éclat de galet",
    "éclat de cube",
    "éclat de bois",
    "éclat de couloir",
    "éclat de poussière",
    "éclat de poussiere",
    "éclat de cour",
    "éclat de plaque",
    "éclat de pierre",
    "éclat de grille",
    "éclat de couvercle",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de dalle",
    "éclat d'enveloppe",
    "éclat de enveloppe",
    "éclat d'émail",
    "éclat d'email",
    "éclat de samare",
    "éclat de bassine",
    "éclat de planche",
    "éclat de figue",
    "éclat de coussin",
    "éclat de tiroir",
    "éclat de perron",
    "éclat de limace",
    "éclat de botte",
    "éclat de résine",
    "éclat de resine",
    "éclat de cageot",
    "éclat de platane",
    "éclat de chiffon",
    "grain de pin",
    "lune d'étain",
    "lune d'etain",
    "point de gouttière",
    "point de gouttiere",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de table",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_finir_le_puzzle_maintenant; "
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
            "sous_texte=victorina_parle_peu_que_fait_amir; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="pièce",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_tend_la_piece_il_attend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de table",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis prudence; intensite=2; destinataire=enfant; "
            "sous_texte=2e_ruse_au_parc_il_refuse_de_foncer; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de table",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "attendre",
    "accepted_examples": "attendre | tendre un jouet | un jouet | il attend",
    "retry_prompt": "Il tend un jouet. Il attend. Que fait Amir ?",
    "engine_ok_text": "Oui, attendre.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "crayon,craie",
        [
            "narrateur|Un toc sec court sous le bois.",
            "narrateur|Un crayon jaune file, puis s'arrête.",
            "enfant-m|Il roule, papa !",
            "papa|Il est passé sous la table ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa se penche près du pied.",
            "narrateur|L'air de la classe sent la craie.",
            "enfant-m|Ça sent la craie, maman.",
            "maman|Tu le sens, toi ?",
            "enfant-m|Oui, maman.",
            "narrateur|Une vitre laisse un carré de soleil.",
            "papa|Tu vois le carré, Amir ?",
            "enfant-m|Oui, sur le bois.",
            "narrateur|Le cartable penche contre une jambe.",
            "maman|Le cartable tient tout seul ?",
            "enfant-m|Oui, maman.",
            "narrateur|Sur le bord, un éclat de table brille.",
            "enfant-m|Il brille, papa !",
            "papa|Tu le vois, ce petit point ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|Un puzzle d'animaux attend sur le bois.",
            "enfant-m|Le chat n'a pas de tête.",
            "maman|Il manque une pièce, Amir ?",
            "enfant-m|Oui, la tête.",
            "narrateur|En ce moment, Amir veut finir le puzzle.",
            "enfant-m|Je veux le finir, maintenant !",
            "enfant-m|Toute la tête, maman.",
            "papa|Avec Victorina, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Victorina s'assoit près de la table.",
            "narrateur|Victorina parle peu.",
            "narrateur|Elle regarde ses mains.",
            "enfant-m|Victorina !",
            "narrateur|Amir ouvre la bouche trop vite.",
            "narrateur|Les questions montent, serrées.",
            "narrateur|Il pousse la tête du chat.",
            "enfant-m|La tête, vite !",
            "narrateur|La pièce glisse trop fort.",
            "narrateur|Elle tombe sous la table.",
            "enfant-m|Oh !",
            "narrateur|Elle rejoint le crayon jaune.",
            "enfant-m|Elle est tombée !",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu, lourdes.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu veux le chat avec Victorina ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains sont serrées, Amir ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Amir refuse de foncer.",
            "narrateur|Il ramasse la pièce, sans se presser.",
            "narrateur|Le crayon jaune reste sous le bois.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le bord, un instant.",
            "narrateur|L'éclat de table tremble, puis tient.",
            "enfant-m|L'éclat, papa ?",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur le bois.",
            "narrateur|Amir tend la pièce, la main ouverte.",
            "narrateur|Victorina ne dit rien.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorina parle peu.",
            "narrateur|Que fait Amir ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "puzzle,craie",
        [
            "narrateur|Amir tend la pièce, sans se presser.",
            "enfant-m|Pour toi.",
            "narrateur|Sa main reste ouverte.",
            "narrateur|Il attend.",
            "narrateur|Victorina regarde la pièce.",
            "narrateur|Elle ne parle pas.",
            "narrateur|Elle prend la pièce, sans bruit.",
            "narrateur|Elle pose la tête du chat.",
            "enfant-m|Le chat, papa.",
            "papa|Tu le vois, le chat ?",
            "enfant-m|Oui, papa.",
            "copine|Chat.",
            "enfant-m|Chat.",
            "maman|Le museau est gris, Amir ?",
            "enfant-m|Oui, maman.",
            "narrateur|Amir veut demander le chien.",
            "narrateur|Il referme un peu la bouche.",
            "narrateur|Il glisse une autre pièce, plus lente.",
            "papa|C'est le dos, Amir ?",
            "enfant-m|Le dos du chien.",
            "narrateur|Victorina pose sa main à côté.",
            "narrateur|Elle reste les mains sur le bois.",
            "enfant-m|À toi.",
            "narrateur|Elle pose une oreille.",
            "copine|Chien.",
            "enfant-m|Chien.",
            "narrateur|Le ventre d'Amir se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|Le puzzle avance, vous deux ?",
            "enfant-m|Oui, papa.",
            "maman|Tes doigts sont moins serrés, Amir ?",
            "enfant-m|Oui, maman.",
            "narrateur|Il observe l'éclat de table.",
            "enfant-m|Le point, papa.",
            "papa|Sur le bois, Amir ?",
            "enfant-m|Oui, il tient.",
            "maman|On met le puzzle dans le cartable ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le crayon jaune reste sous la table.",
            "enfant-m|Il reste là.",
            "papa|On le laisse, Amir ?",
            "enfant-m|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "enfants_parc",
        [
            "narrateur|Au parc, une table de bois se tient près de l'herbe.",
            "papa|Tu poses le puzzle ici, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Maman ouvre le cartable sur l'herbe.",
            "maman|Le chat est entier, Amir ?",
            "enfant-m|Le chien n'est pas fini.",
            "narrateur|Victorina s'assoit, sans un mot.",
            "enfant-m|Je finis, maintenant !",
            "narrateur|Il pousse la dernière pièce trop vite.",
            "narrateur|La pièce part dans l'herbe.",
            "enfant-m|Oh.",
            "copine|Non.",
            "narrateur|Victorina recule les mains.",
            "narrateur|Amir avance trop, d'un pas.",
            "narrateur|Amir refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il cherche dans l'herbe, sans se jeter.",
            "narrateur|La pièce a un brin collé.",
            "enfant-m|Elle a de l'herbe, papa.",
            "papa|Tu la vois, la pièce ?",
            "enfant-m|Oui, papa.",
            "narrateur|Il tend la pièce, la main ouverte.",
            "narrateur|Il reste près de l'herbe.",
            "narrateur|Victorina regarde longtemps.",
            "narrateur|Elle prend la pièce.",
            "narrateur|Elle la pose dans le trou.",
            "copine|Chien.",
            "enfant-m|Chien.",
            "maman|Merci, Amir.",
            "narrateur|Maman a vu la main ouverte.",
            "papa|Le chien est entier, vous deux ?",
            "enfant-m|Oui, papa.",
            "narrateur|Un éclat de table luit sur le bord.",
            "enfant-m|L'éclat, maman ?",
            "maman|Tu le vois, sur le bois ?",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "crayon,cartable",
        [
            "narrateur|De retour, le crayon jaune est sur le bois.",
            "enfant-m|Il n'est plus sous la table.",
            "papa|Tu l'as vu, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le puzzle rentre dans le cartable.",
            "maman|Le brin d'herbe est resté, Amir ?",
            "enfant-m|Sur le chien, maman.",
            "copine|Chat.",
            "enfant-m|Chat.",
            "papa|Le chat a sa tête, vous deux ?",
            "enfant-m|Oui, papa.",
            "narrateur|Un carré de soleil tient sur la vitre.",
            "enfant-m|La craie, maman.",
            "maman|Tu la sens, la craie ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Un éclat de table tient sur le bois.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-m", "copine"):
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
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Amir = enfant-m, Victorina = copine)")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Victorina absente (copine)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m", "copine") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "copine" for r in roles):
        raise SystemExit(f"{SID}: copine absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on n'imite pas",
        "on ne force pas",
        "tu as su attendre",
        "on peut attendre",
        "il faut attendre",
        "tu peux tendre",
        "tendre un jouet",
        "on peut jouer",
        "bon travail",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Victorina parle peu. Que fait Amir ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "attendre | tendre un jouet | un jouet | il attend"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Il tend un jouet. Il attend. Que fait Amir ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    copine_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    )
    if len(copine_txt.split()) > 8:
        raise SystemExit(f"{SID}: Victorina parle trop: {copine_txt}")
    for need in (
        "crayon",
        "craie",
        "vitre",
        "cartable",
        "puzzle",
        "table",
        "pièce",
        "parc",
    ):
        if need not in blob:
            raise SystemExit(f"{SID}: manque {need}")
    for ban in (
        "éclat de crayon",
        "éclat de craie",
        "éclat de vitre",
        "éclat de cartable",
        "éclat de rond",
        "éclat de parquet",
        "éclat de banc",
        "iris",
        "ruben",
        "bateau",
        "tout doux",
        "tout calme",
        "aujourd'hui",
        "merle",
        "miel",
        "bon travail",
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
        "- **Leçon :** DIF.PAR.001 — attendre / tendre un jouet "
        "(vécue : Amir refuse de foncer, tend la pièce, main ouverte, "
        "attend). JAMAIS dite dans le récit. Pas « on n'imite pas », "
        "pas « on ne force pas la parole », pas « tu as su attendre ».\n"
        "- **Personnages :** Amir, Victorina, papa, maman. Troupe D16. "
        "Amir = enfant-m (veut maintenant, refuse de foncer). Victorina "
        "= copine (parle peu, Non, Chat, Chien). Papa et maman "
        "parlent. Pas de maîtresse. Ruben / Iris absents.\n"
        "- **Lieu :** école puis parc (crayon jaune sous la table, "
        "craie, vitre, cartable, puzzle). ≠ 001-01 coussins / camion. "
        "≠ 001-02 seau / puits. ≠ 001-03 voiture / tapis. Pas bateau / "
        "bac d'eau du dump.\n"
        "- **Indice unique :** éclat de table (crayon qui roule sous "
        "la table → brille → tremble → observé → luit au parc → tient "
        "sur le bois). Pas éclat de crayon / craie / vitre / cartable / "
        "rond / parquet / banc.\n"
        "- **Question moteur :** « Victorina parle peu. Que fait "
        "Amir ? » expected **attendre**. accepted `attendre | tendre un "
        "jouet | un jouet | il attend`. Retry dump : Il tend un jouet. "
        "Il attend. Que fait Amir ? Non récité dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / "
        "graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin "
        "heureuse. `chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un toc sous le bois. Un crayon jaune roule sous la table. "
        "Craie, vitre, cartable. Sur le bord, un éclat de table brille. "
        "Amir veut finir le puzzle **maintenant**. Victorina parle peu. "
        "Il pousse trop vite, la pièce tombe près du crayon. Sourire "
        "parti, poitrine, papa accroupi. Il refuse de foncer, tend la "
        "pièce, main ouverte. Question. Il attend. Elle pose la tête "
        "du chat. Deuxième ruse au parc : dernière pièce dans l'herbe, "
        "Non. Il refuse, tend, attend. Merci vécu. Le crayon n'est plus "
        "sous la table. Un éclat de table tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : classe, toc, crayon jaune, craie, vitre, cartable, "
        "puzzle, puis parc.\n"
        "- Désir : finir le puzzle, maintenant, la tête du chat.\n"
        "- Objet : pièce du puzzle, crayon sous la table.\n"
        "- Indice unique : éclat de table, vu dès l'ouverture, payé "
        "sur le bois. Pas éclat de crayon.\n"
        "- Urgence douce : le chat sans tête, maintenant ; Victorina "
        "ne dit rien.\n"
        "- Imprévu 1 : pièce trop vite ; elle tombe sous la table, "
        "près du crayon.\n"
        "- Cue : papa à la même hauteur ; un merci vécu après la main "
        "ouverte au parc.\n"
        "- Imprévu 2 (plus rusé) : dernière pièce dans l'herbe ; Non.\n"
        "- Résolution : il refuse de foncer, tend la pièce, attend.\n"
        "- Retour : crayon sur le bois, brin d'herbe sur le chien, "
        "éclat qui tient.\n\n"
        "## Vécu\n\n"
        "Amir veut **maintenant**. Victorina parle peu, pose sa limite "
        "(Non). Le silence compte. Papa s'accroupit, ne récite pas "
        "« on ne force pas la parole ». La leçon se voit : la main "
        "ouverte, la pièce tendue, l'attente. Merci vécu après la "
        "main ouverte. Fin : l'éclat du début tient sur le bois. Le "
        "dénouement a failli : la pièce est tombée, puis perdue dans "
        "l'herbe.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : La pièce du puzzle (roster F-NAR-019). Dump avait "
        "« Le bateau sur le rebord ». Lieu mission : école puis parc, "
        "crayon, craie, vitre, cartable, puzzle. Pas bateau / bac "
        "d'eau. ≠ PAR.001-01..03.\n"
        "- Ouverture inventée (toc, crayon qui roule sous la table), "
        "pas « Amir est en classe », pas un gabarit v2. example4 027 / "
        "059 / 091 : corps (sourire parti, poitrine, accroupi), 2e "
        "ruse, refuse de foncer, fin qui a failli.\n"
        "- Indice unique : éclat de table. Pas merle-trois-notes, "
        "miel, tache / flèche / marque / symbole. Pas éclat de crayon / "
        "craie / vitre / cartable / rond / parquet / banc.\n"
        "- Tics encore / déjà / tout doux / tout calme et `aujourd'hui` "
        "retirés. Morale « on n'imite pas » / « on ne force pas » / "
        "« tu as su attendre » hors récit. Ruben / Iris → Amir / "
        "Victorina. Pas de maîtresse.\n"
        "- Question moteur inchangée. expected **attendre**. 5 chunks, "
        "kinds inchangés.\n"
        "- Voix : `_write_atom_dif_ene_001_04.py` / "
        "`_write_atom_dif_ene_001_05.py` (profiles, ssml, xai).\n"
        f"- {nwords} mots. N3 ≤ 16. TTS : notes, ssml, xai, piper par "
        "chunk. `slow` = question + fin.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n"
        "- 1 × `en ce moment`, 1 × merci adulte, 5 × éclat de table\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
