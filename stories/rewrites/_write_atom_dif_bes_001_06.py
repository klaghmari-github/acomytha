#!/usr/bin/env python3
"""ATOM-DIF.BES.001-06 — Raphaël répète, Aniss observe (F-NAR-019, N1, DIF.BES.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.001-06"
TITLE = "Raphaël répète, Aniss observe"
N1 = LIMITS["N1"]
INDICE = "éclat de couloir"
CHARS = "Aniss, Raphaël, papa, maman"
SETTING = (
    "classe, tapis, vitre embuée, gouttes, manteaux, couloir"
)
FIL = (
    "Une goutte quitte un manteau bleu. Sur le rond, un éclat de "
    "couloir brille. Aniss veut le rond, maintenant. Raphaël court, "
    "sa voix part trop fort : Aniss recule. Raphaël refuse de foncer, "
    "dit les mots plus bas, une seconde fois. Merci vécu. Aniss "
    "observe, s'assoit. Ils glissent vers le rond. Un éclat de "
    "couloir reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
SAC_RE = re.compile(r"\bsacs?\b", re.I)
WORD_BAN = re.compile(
    r"\b(bois|cube|boule|galet|carte|panier|dorure|cloche|"
    r"adèle|adele|estelle)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "louise",
    "zoé",
    "zoe",
    "iris",
    "miel",
    "merle",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "maîtresse",
    "maitresse",
    "voisine",
    "poire",
    "corbeille",
    "croissant",
    "réverbère",
    "reverbere",
    "bâche",
    "bache",
    "volet",
    "pavé",
    "pave",
    "zeste",
    "parapluie",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "trois notes",
    "une chose, puis la suivante",
    "une chose puis l'autre",
    "une étape après l'autre",
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
    "répéter la règle",
    "observer d'abord",
    "c'est la règle",
    "tu as su répéter",
    "le calme a aidé",
    "tache de couleur",
    "ombre en forme de flèche",
    "marque fine",
    "minuscule symbole",
    "grain de miette",
    "grain de laine",
    "bande bleue",
    "éclat de panier",
    "éclat de dorure",
    "éclat de poire",
    "éclat de sac",
    "éclat de cloche",
    "éclat de corbeille",
    "éclat de croissant",
    "éclat de réverbère",
    "éclat de reverbere",
    "éclat de bâche",
    "éclat de bache",
    "éclat de volet",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de crayon",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de cartable",
    "éclat de pinceau",
    "éclat de tapis",
    "éclat de crochet",
    "éclat de carotte",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de pli",
    "éclat de mie",
    "éclat de poisson",
    "éclat de page",
    "éclat d'escargot",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de wagon",
    "éclat de nappe",
    "éclat de farine",
    "éclat de laine",
    "éclat de bec",
    "éclat de marche",
    "éclat de fraise",
    "éclat de quille",
    "éclat de casserole",
    "éclat de tasse",
    "éclat de vitre",
    "éclat de bois",
    "éclat de cube",
    "éclat de boule",
    "éclat de galet",
    "éclat de carte",
)


PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de couloir",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=aniss_veut_le_rond_maintenant; "
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
            "sous_texte=on_dit_les_mots_une_seconde_fois; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="Viens",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; "
            "sous_texte=raphael_dit_les_mots_plus_bas; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de couloir",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=aniss_refuse_de_glisser_sans_regarder; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de couloir",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pale; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "répéter",
    "accepted_examples": (
        "répéter | observer d'abord | observer | attendre"
    ),
    "retry_prompt": "On peut répéter. Que peut-on faire ?",
    "engine_ok_text": "Oui, répéter.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "pluie,manteaux",
        [
            "narrateur|Une goutte quitte un manteau bleu.",
            "narrateur|Elle tombe dans le couloir.",
            "narrateur|L'eau fait un rond sombre.",
            "narrateur|Sur le rond, un éclat de couloir brille.",
            "narrateur|Aniss se penche vers le rond.",
            "enfant-m|Il est petit, papa.",
            "papa|Tu le vois, Aniss ?",
            "enfant-m|Oui, sur l'eau.",
            "narrateur|Les manteaux gouttent, près de la porte.",
            "narrateur|Ça sent le savon, un peu.",
            "maman|Ton manteau va là, Aniss.",
            "narrateur|Maman accroche le manteau bleu.",
            "narrateur|La laine est lourde d'eau.",
            "enfant-m|Il goutte, maman.",
            "maman|Oui, dans le couloir.",
            "narrateur|Le sol du couloir est froid.",
            "narrateur|Une flaque luit sous les crochets.",
            "narrateur|La vitre de la classe est embuée.",
            "narrateur|Des gouttes y glissent, lentes.",
            "papa|Tu vois le jardin, Raphaël ?",
            "narrateur|Raphaël pose le nez sur la vitre.",
            "enfant-m|Oui, papa.",
            "narrateur|Maman essuie un coin de vitre.",
            "maman|Les arbres sont mouillés.",
            "narrateur|Le jardin est gris, derrière.",
            "narrateur|Le tapis rouge attend, un peu rêche.",
            "narrateur|Raphaël s'avance vers le tapis.",
            "narrateur|Raphaël se tourne vers Aniss.",
            "enfant-m|On joue, Aniss ?",
            "narrateur|Aniss reste près du mur.",
            "narrateur|Ses mains restent sur ses genoux.",
            "narrateur|Aniss ouvre la bouche.",
            "enfant-m|Je veux le rond, maintenant !",
            "papa|Tu restes près de nous ?",
            "enfant-m|Oui, papa.",
            "narrateur|En ce moment, Raphaël court vers Aniss.",
            "narrateur|Raphaël tend la main trop vite.",
            "enfant-m|Viens, Aniss !",
            "narrateur|Sa voix part trop fort, trop vite.",
            "narrateur|Aniss recule contre le mur.",
            "enfant-m|Oh.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et l'inquiétude se heurtent.",
            "narrateur|L'éclat de couloir tremble, puis tient.",
            "narrateur|Raphaël baisse les bras.",
            "enfant-m|Il ne vient pas, maman.",
            "narrateur|Les épaules d'Aniss tombent un peu.",
            "narrateur|Ça serre, dans son ventre.",
            "narrateur|Papa se baisse à sa hauteur.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "tapis,gouttes",
        [
            "narrateur|Raphaël avance trop vite vers Aniss.",
            "enfant-m|Viens, Aniss !",
            "narrateur|Sa voix se mélange au bruit des gouttes.",
            "narrateur|Aniss serre les genoux.",
            "enfant-m|Oh.",
            "narrateur|Raphaël refuse de foncer.",
            "narrateur|Il referme la main.",
            "narrateur|Il regarde Aniss, un instant.",
            "papa|Tu veux venir près du tapis ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Raphaël pose un genou près du tapis.",
            "narrateur|Le tapis est rêche, un peu froid.",
            "enfant-m|Viens, Aniss.",
            "narrateur|Il dit les mots plus bas.",
            "papa|Viens, Aniss.",
            "narrateur|Papa dit les mots, comme lui.",
            "enfant-m|Viens, Aniss.",
            "narrateur|Raphaël dit les mots, une seconde fois.",
            "maman|Merci, Raphaël.",
            "narrateur|Maman a entendu toute la phrase.",
            "narrateur|Aniss écoute.",
            "narrateur|Il regarde le tapis.",
            "narrateur|Ses mains restent un moment.",
            "narrateur|Puis il avance un pied.",
            "narrateur|Il s'assoit au bord.",
            "enfant-m|Je suis là.",
            "narrateur|Le ventre d'Aniss se desserre.",
            "papa|Tu as les mains au chaud ?",
            "enfant-m|Un peu, papa.",
            "maman|On voit le tapis ?",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "couloir,manteaux",
        [
            "narrateur|Raphaël tire Aniss trop vite.",
            "enfant-m|Le rond, maintenant !",
            "narrateur|Le pied d'Aniss glisse sur l'eau.",
            "enfant-m|Oh.",
            "narrateur|Un manteau bouge, puis retombe.",
            "narrateur|Aniss avance la main.",
            "narrateur|Puis il s'arrête net.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Papa attend, sans parler.",
            "narrateur|Aniss observe le couloir.",
            "narrateur|Il écoute les gouttes.",
            "narrateur|Sur le rond, un éclat de couloir luit.",
            "enfant-m|Là, près du manteau bleu.",
            "narrateur|Aniss tient la manche de Raphaël.",
            "narrateur|La laine est froide, un peu lourde.",
            "enfant-m|Elle est froide, papa.",
            "papa|Tu marches jusqu'au rond ?",
            "enfant-m|Oui, papa.",
            "maman|On avance ?",
            "enfant-m|Oui, maman.",
            "narrateur|Ils posent un pied, puis l'autre.",
            "narrateur|Le sol mouillé touche les chaussettes.",
            "narrateur|L'air froid revient sur les joues.",
            "enfant-m|Je le tiens.",
            "papa|On marche.",
            "narrateur|Aniss serre la manche contre lui.",
            "enfant-m|Je la tiens.",
            "maman|On avance.",
            "narrateur|Ils passent le long des manteaux.",
            "narrateur|La laine gratte, un peu.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "couloir",
        [
            "enfant-m|Le rond brillait, papa.",
            "papa|Tu le vois, comme dans le couloir ?",
            "enfant-m|Oui, un peu pâle.",
            "narrateur|Aniss pose le genou près de l'eau.",
            "maman|On le garde près de nous ?",
            "enfant-m|Oui, maman.",
            "narrateur|Raphaël s'assoit près du rond.",
            "enfant-m|Comme tout à l'heure, papa !",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur l'eau.",
            "maman|On est bien, ici.",
            "narrateur|Une goutte quitte le manteau bleu.",
            "narrateur|Elle tombe dans le même rond.",
            "enfant-m|On le voit, maman.",
            "maman|Tu le vois sur l'eau ?",
            "enfant-m|Oui, l'éclat.",
            "narrateur|Le soir reste dans l'air.",
            "narrateur|Un éclat de couloir reste pâle.",
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
        if SAC_RE.search(ph):
            raise SystemExit(f"ban sac: {ph}")
        if WORD_BAN.search(ph):
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"extra {bad}: {ph}")
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
    for name in ("adèle", "adele", "estelle", "louise", "zoé", "zoe", "iris"):
        if re.search(rf"\b{name}\b", blob):
            raise SystemExit(f"{SID}: {name} interdit")
    if "maitresse|" in blob or "maîtresse|" in blob:
        raise SystemExit(f"{SID}: maîtresse parle")
    if "copain|" in blob or "copine|" in blob:
        raise SystemExit(f"{SID}: copain/copine")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Aniss et Raphaël = enfant-m)")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "besoin de calme",
        "observer d'abord",
        "répéter la règle",
        "on peut répéter",
        "le calme a aidé",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if "répéter" in body:
        raise SystemExit(f"{SID}: répéter dans le récit")
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
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Aniss a besoin de calme. Que peut-on faire ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "répéter":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt", "").lower()
    if "adèle" in retry or "estelle" in retry:
        raise SystemExit(f"{SID}: mauvais prénom dans retry_prompt")
    if "répéter" not in retry:
        raise SystemExit(f"{SID}: retry sans répéter")
    for ban in (
        "panier", "dorure", "poire", "cloche", "corbeille", "croissant",
        "réverbère", "reverbere", "bâche", "bache", "volet", "pavé",
        "pave", "zeste", "parapluie", "marché", "boulangerie",
        "cube", "boule", "galet",
    ):
        if ban in blob:
            raise SystemExit(f"{SID}: BAN {ban}")
    if re.search(r"\bbois\b", blob):
        raise SystemExit(f"{SID}: BAN bois")
    if re.search(r"\bcarte\b", blob):
        raise SystemExit(f"{SID}: BAN carte")
    if SAC_RE.search(blob):
        raise SystemExit(f"{SID}: BAN sac")
    if "tout doux" in blob:
        raise SystemExit(f"{SID}: tic tout doux")
    if "éclat de buée" in blob or "éclat de gouttière" in blob or "éclat de manteau" in blob:
        raise SystemExit(f"{SID}: mauvais éclat")

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
        "- **Public :** N1 (≤10 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.BES.001 — besoin de calme / répéter / observer "
        "d'abord (vécue : voix trop forte → Aniss recule ; les mots "
        "reviennent plus bas, une seconde fois)\n"
        "- **Personnages :** Aniss (héros, question moteur), Raphaël, "
        "papa, maman. Adèle / Estelle du dump → INTERDIT. Maman ajoutée. "
        "Pas de maîtresse. Troupe D16.\n"
        "- **Lieu :** classe, tapis, vitre embuée, gouttes, manteaux, "
        "couloir. ≠ cuisine / train sous la table. ≠ COL.POL marché.\n"
        "- **Indice unique :** éclat de couloir (brille à l'ouverture, "
        "tremble, luit au refus, reste pâle). Pas éclat de buée / "
        "gouttière / manteau.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte quitte un manteau bleu. Sur le rond, un éclat de "
        "couloir brille. Aniss veut le rond **maintenant**. Raphaël court, "
        "voix trop forte : Aniss recule. Sourire parti, épaules basses. "
        "Raphaël refuse de foncer. Il dit les mots plus bas. Papa dit les "
        "mots, comme lui. Merci vécu. Aniss observe, s'assoit. Raphaël "
        "tire trop vite : le pied glisse. Aniss s'arrête, lit l'éclat. "
        "Un éclat de couloir reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : classe, vitre embuée, gouttes, manteaux qui gouttent, "
        "couloir, tapis rouge, savon, jardin gris. ≠ cuisine / train / "
        "cubes / panier.\n"
        "- Désir : Aniss veut le rond du couloir, maintenant.\n"
        "- Objet : goutte, manteau bleu, rond d'eau, tapis, manche.\n"
        "- Indice unique : éclat de couloir, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : la voix trop grande pour Aniss.\n"
        "- Imprévu 1 : crier trop vite ; Aniss recule, l'éclat tremble.\n"
        "- Cue : papa à la même hauteur, près du tapis. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : tirer vers le rond, pied qui glisse.\n"
        "- Résolution : Raphaël refuse de foncer, dit les mots plus "
        "bas ; Aniss observe, s'assoit.\n"
        "- Retour : goutte du manteau bleu, éclat de couloir pâle.\n\n"
        "## Vécu\n\n"
        "Aniss veut le rond **maintenant**. Impatience de Raphaël, puis "
        "sourire d'Aniss qui disparaît. Papa se baisse, pose une "
        "question, ne récite pas la règle. Raphaël agit : main fermée, "
        "mots plus bas, seconde fois. Aniss écoute, avance un pied. "
        "Merci vécu après l'écoute. Fin : l'éclat du début reste pâle.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Raphaël répète, Aniss observe (noyau dump : Adèle "
        "répète, Estelle observe). Adèle / Estelle → INTERDIT. Relance "
        "Aniss. Maman ajoutée.\n"
        "- Lieu du dump (classe, tapis, vitre embuée, gouttes, manteaux). "
        "≠ train sous la table / cuisine / nappe.\n"
        "- Ouverture inventée (goutte, manteau bleu, rond), pas un "
        "gabarit v2, pas « Aniss est à l'école », pas « joue au salon ».\n"
        "- Indice unique : éclat de couloir. Pas bois, cube, boule, "
        "galet, carte, panier, dorure, sac, cloche. Pas éclat de buée / "
        "gouttière / manteau.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » du dump.\n"
        "- Leçon non dite : on l'entend quand les mots reviennent plus "
        "bas. Pas de morale, pas « tu as su répéter », pas « observer "
        "d'abord ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Aniss a besoin de calme. Que peut-on "
        "faire ? » (Estelle → Aniss). expected répéter. retry sans "
        "Adèle / Estelle. 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le couloir.\n"
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
