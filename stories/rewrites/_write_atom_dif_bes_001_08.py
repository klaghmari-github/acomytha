#!/usr/bin/env python3
"""ATOM-DIF.BES.001-08 — Sarah répète et laisse observer (F-NAR-019, N3, DIF.BES.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.001-08"
TITLE = "Sarah répète et laisse observer"
N3 = LIMITS["N3"]
INDICE = "éclat de cour"
CHARS = "Sarah, papa, maman"
SETTING = (
    "classe, tapis vert roulé, boîte en fer, anneaux, "
    "cour et marché loin, pain près de la fenêtre"
)
FIL = (
    "Ça sent le pain chaud près de la fenêtre. Un éclat de cour "
    "glisse sur le sol. Sarah veut le tapis et tous les anneaux "
    "maintenant. Elle verse trop vite : les anneaux glissent. "
    "Sourire parti. Elle refuse de foncer, dit un anneau puis un "
    "autre. Merci vécu. Le tapis trop vite cache l'éclat. Un éclat "
    "de cour reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(cube|cubes|carte|cartes|bois|poussière|poussiere|"
    r"couloir|caisse|caisses|claire|victorino|hugo|louise)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "zoé",
    "zoe",
    "iris",
    "raphaël",
    "raphael",
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
    "panier",
    "dorure",
    "poire",
    "cloche",
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
    "bassine",
    "cabanon",
    "bateau",
    "savon",
    "tortue",
    "galet",
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
    "tu as laissé le temps",
    "tu as laisse le temps",
    "tache de couleur",
    "ombre en forme de flèche",
    "marque fine",
    "minuscule symbole",
    "grain de miette",
    "grain de laine",
    "bande bleue",
    "éclat de cube",
    "éclat de carte",
    "éclat de bois",
    "éclat de poussière",
    "éclat de poussiere",
    "éclat de couloir",
    "éclat de caisse",
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
    "éclat de boule",
    "éclat de galet",
    "éclat de boîte",
    "éclat de boite",
    "éclat de fer",
    "éclat d'anneau",
    "éclat de pain",
)


PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de cour",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_tapis_et_les_anneaux_maintenant; "
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
            "sous_texte=on_dit_le_mot_une_seconde_fois; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="Un anneau",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_voix_forte_echoue_le_mot_revient_plus_bas; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de cour",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_sans_regarder_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de cour",
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
        "pain,fer",
        [
            "narrateur|Ça sent le pain chaud, près de la fenêtre.",
            "narrateur|Le marché parle, tout loin.",
            "enfant-f|J'entends le pain, papa.",
            "papa|Tu l'entends, Sarah ?",
            "narrateur|Un éclat de cour glisse sur le sol.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, près de la fenêtre ?",
            "narrateur|Sarah touche l'éclat de cour.",
            "narrateur|Le sol est lisse, un peu froid.",
            "enfant-f|Il est froid.",
            "narrateur|Maman noue le lacet de Sarah.",
            "maman|Ton lacet va là, près de la chaussure.",
            "enfant-f|Il tient, maman.",
            "narrateur|La chaussure sent un peu la cour.",
            "enfant-f|Elle est froide, maman.",
            "narrateur|Une boîte en fer attend sous la fenêtre.",
            "narrateur|Des anneaux s'y cognent.",
            "enfant-f|Ça fait clic.",
            "papa|Tu tiens ma manche, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le tapis vert est roulé dans le coin.",
            "narrateur|Un coin de laine dépasse, un peu rêche.",
            "enfant-f|Il est vert, maman.",
            "maman|Il sent la laine.",
            "enfant-f|Ça pique un peu.",
            "narrateur|Papa pose la bouteille sur l'étagère.",
            "papa|L'eau va là.",
            "enfant-f|Elle est haute.",
            "narrateur|La bouteille claque contre l'étagère.",
            "narrateur|L'air de la cour entre un peu.",
            "enfant-f|J'ai les joues froides.",
            "papa|On avance.",
            "maman|Tu restes près de nous ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Je veux le tapis, maintenant !",
            "enfant-f|Tous les anneaux, d'un coup !",
            "papa|Tu ouvres la boîte ?",
            "enfant-f|Oui, papa.",
            "narrateur|En ce moment, Sarah ouvre la boîte.",
            "narrateur|Les anneaux sentent le fer.",
            "enfant-f|Ils sont froids.",
            "narrateur|Sarah verse trop vite, trop fort.",
            "narrateur|Les anneaux glissent sur le sol.",
            "enfant-f|Oh.",
            "narrateur|L'éclat n'est plus là.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-f|Je les prends !",
            "maman|Les anneaux sont partout.",
            "papa|Tu les vois, Sarah ?",
            "narrateur|Les épaules de Sarah tombent un peu.",
            "narrateur|Ça serre, dans son ventre.",
            "narrateur|Papa se baisse à sa hauteur.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Sarah a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "fer,tapis",
        [
            "narrateur|Sarah avance trop vite vers les anneaux.",
            "enfant-f|Tous, maintenant !",
            "narrateur|Sa voix se mélange au marché.",
            "enfant-f|Oh.",
            "narrateur|Les anneaux restent en tas.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Sarah referme la main.",
            "narrateur|Elle regarde le sol, un instant.",
            "papa|Tu veux venir près de la boîte ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Sarah pose un genou près du fer.",
            "narrateur|Le fer est lisse, un peu froid.",
            "enfant-f|Un anneau.",
            "enfant-f|Puis un autre.",
            "narrateur|Elle dit les mots plus bas.",
            "papa|Un anneau.",
            "narrateur|Papa dit le mot, comme elle.",
            "enfant-f|Puis un autre.",
            "narrateur|Sarah dit le mot, une seconde fois.",
            "maman|Merci, Sarah.",
            "narrateur|Maman a entendu toute la phrase.",
            "narrateur|Le ventre de Sarah se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|Tu as les mains au chaud ?",
            "enfant-f|Un peu, papa.",
            "narrateur|Sarah pose un anneau rouge.",
            "enfant-f|Rouge.",
            "narrateur|L'anneau fait clic sur le sol.",
            "maman|Tu le vois, celui-là ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sarah pose un anneau jaune, plus loin.",
            "enfant-f|Jaune.",
            "papa|Il tient, celui-là ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un chemin d'anneaux avance vers la fenêtre.",
            "enfant-f|Il va vers la fenêtre.",
            "maman|Tu le vois, le chemin ?",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "tapis,fer",
        [
            "narrateur|Sarah tire le tapis trop vite.",
            "enfant-f|Jusqu'à la fenêtre, d'un coup !",
            "narrateur|Le tapis se roule vers le coin.",
            "enfant-f|Oh.",
            "narrateur|L'éclat n'est plus là.",
            "enfant-f|Il est parti.",
            "narrateur|Sarah avance les mains.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Elle refuse de foncer.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Papa attend, sans parler.",
            "narrateur|Sarah observe le sol, écoute la classe.",
            "narrateur|Près de la fenêtre, un éclat de cour luit.",
            "enfant-f|Là, près de la fenêtre.",
            "narrateur|Sarah tient le tapis des deux mains.",
            "narrateur|La laine est rêche, un peu froide.",
            "enfant-f|Elle est froide, papa.",
            "papa|Tu le portes jusqu'à la fenêtre ?",
            "enfant-f|Oui, papa.",
            "maman|On avance ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sarah déroule le tapis, sans se presser.",
            "narrateur|Le tapis touche le sol froid.",
            "narrateur|L'air froid revient sur les joues.",
            "narrateur|Sarah serre un anneau contre elle.",
            "enfant-f|Il reste froid.",
            "papa|On marche.",
            "narrateur|L'anneau penche, puis se cale.",
            "enfant-f|Je le tiens.",
            "maman|On avance.",
            "narrateur|Sarah pose l'anneau sur la laine.",
            "narrateur|Le clic est petit, près de l'éclat.",
            "enfant-f|Il est sur la laine.",
            "papa|Près de la fenêtre ?",
            "enfant-f|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "pain",
        [
            "enfant-f|L'éclat brillait, papa.",
            "papa|Tu le vois, comme près de la fenêtre ?",
            "enfant-f|Oui, un peu pâle.",
            "narrateur|Sarah pose l'anneau contre le tapis.",
            "maman|On le garde près de nous ?",
            "enfant-f|Oui, maman.",
            "enfant-f|La classe sentait le pain.",
            "maman|Le marché est derrière nous.",
            "narrateur|Un bruit de fer n'est plus aussi net.",
            "narrateur|Sarah respire, plus large.",
            "papa|On rentre ?",
            "enfant-f|Oui.",
            "narrateur|Les joues de Sarah se réchauffent.",
            "narrateur|L'anneau reste froid sous la main.",
            "narrateur|Un éclat de cour reste pâle.",
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
    for name in (
        "louise", "zoé", "zoe", "iris", "raphaël", "raphael",
        "claire", "victorino", "hugo",
    ):
        if re.search(rf"\b{name}\b", blob):
            raise SystemExit(f"{SID}: {name} interdit")
    if "maitresse|" in blob or "maîtresse|" in blob:
        raise SystemExit(f"{SID}: maîtresse parle")
    if "copain|" in blob or "copine|" in blob:
        raise SystemExit(f"{SID}: copain/copine")
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
    if qtext != "Sarah a besoin de calme. Que peut-on faire ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "répéter":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt", "").lower()
    if "victorino" in retry or "claire" in retry or "hugo" in retry:
        raise SystemExit(f"{SID}: mauvais prénom dans retry_prompt")
    if "répéter" not in retry:
        raise SystemExit(f"{SID}: retry sans répéter")
    for ban in (
        "cube", "carte", "bois", "poussière", "poussiere", "couloir", "caisse",
        "panier", "dorure", "poire", "cloche", "corbeille", "croissant",
        "réverbère", "reverbere", "bâche", "bache", "volet", "pavé",
        "pave", "zeste", "parapluie", "bassine", "cabanon",
    ):
        if re.search(rf"\b{re.escape(ban)}\b", blob):
            raise SystemExit(f"{SID}: BAN {ban}")
    if "tout doux" in blob:
        raise SystemExit(f"{SID}: tic tout doux")
    if "éclat de cube" in blob:
        raise SystemExit(f"{SID}: BAN éclat de cube (001-04)")

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
        "- **Leçon :** DIF.BES.001 — besoin de calme / répéter / observer "
        "d'abord (vécue : verse trop vite → anneaux qui glissent ; le mot "
        "revient plus bas, une seconde fois ; tapis trop vite cache l'éclat)\n"
        "- **Personnages :** Sarah, papa, maman. Claire dump TTS → INTERDIT. "
        "Victorino dump retiré (un héros). Hugo dump retiré. Pas de "
        "maîtresse. Troupe D16.\n"
        "- **Lieu :** classe, tapis vert roulé, boîte en fer, anneaux, "
        "cour et marché loin, pain près de la fenêtre. ≠ 001-01 cartes / "
        "vitre floue / tortue. ≠ 001-04 cubes / salon. ≠ 001-05 cour "
        "dedans / linge. ≠ 001-06 couloir / savon / tapis rouge. ≠ "
        "xlsx bassine / cabanon.\n"
        "- **Indice unique :** éclat de cour (glisse à l'ouverture, "
        "touché, luit au refus, reste pâle)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Ça sent le pain chaud près de la fenêtre. Le marché parle, tout "
        "loin. Un éclat de cour glisse sur le sol. Maman noue le lacet. "
        "Une boîte en fer attend. Le tapis vert est roulé. Sarah veut le "
        "tapis et tous les anneaux **maintenant**. Première idée : verser "
        "trop vite, trop fort. Les anneaux glissent. Sourire parti, "
        "épaules basses. Elle refuse de foncer. Elle observe, dit un "
        "anneau, puis un autre. Papa dit le mot, comme elle. Merci vécu. "
        "Elle tire le tapis trop vite : l'éclat disparaît. Elle s'arrête, "
        "lit l'éclat. Un éclat de cour reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : classe, pain, marché loin, éclat de cour, lacet, "
        "boîte en fer, anneaux, tapis vert roulé, bouteille, étagère. "
        "≠ 001-01 cartes / tortue. ≠ 001-04 cubes. ≠ COL.POL étal.\n"
        "- Désir : le tapis et tous les anneaux, maintenant.\n"
        "- Objet : anneaux, boîte en fer, tapis vert, éclat de cour.\n"
        "- Indice unique : éclat de cour, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : la voix trop grande, tout d'un coup.\n"
        "- Imprévu 1 : verser trop vite ; les anneaux glissent, l'éclat "
        "part.\n"
        "- Cue : papa à la même hauteur, près de la boîte. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : tirer le tapis d'un coup, l'éclat "
        "caché sous la laine.\n"
        "- Résolution : elle refuse de foncer, observe, dit le mot plus "
        "bas ; papa le dit comme elle.\n"
        "- Retour : anneau sur la laine, pain loin, éclat de cour pâle.\n\n"
        "## Vécu\n\n"
        "Sarah veut le tapis et les anneaux **maintenant**. Impatience, "
        "puis sourire qui disparaît. Papa se baisse, pose une question, "
        "ne récite pas la règle. Sarah agit : main fermée, mot plus bas, "
        "seconde fois. Merci vécu après l'écoute. Fin : l'éclat du début "
        "reste pâle.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre mission : Sarah répète et laisse observer. xlsx "
        "intermédiaire « Le bateau dans la bassine » non repris "
        "(bassine / cabanon BAN). Dump TTS : Claire / Hugo / cubes / "
        "classe. Claire → INTERDIT. Victorino / Hugo retirés. Relance "
        "sans Victorino / Hugo.\n"
        "- Lieu du dump TTS (classe, tapis vert, boîte en fer, cour/"
        "marché loin, pain). Caisse loin → mot BAN. Cubes dump → "
        "anneaux (pas éclat de cube 001-04). ≠ 001-01 cartes.\n"
        "- Ouverture inventée (pain chaud près de la fenêtre), pas un "
        "gabarit v2, pas « Sarah est en classe ».\n"
        "- Indice unique : éclat de cour. Pas cube, carte, bois, "
        "poussière, couloir, caisse. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » du dump.\n"
        "- Leçon non dite : on l'entend quand le mot revient plus bas. "
        "Pas de morale, pas « tu as su répéter », pas « observer d'abord ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Sarah a besoin de calme. Que peut-on "
        "faire ? » (Victorino dump → Sarah). expected répéter. retry sans "
        "Hugo. 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Confirm plus vif vers la boîte.\n"
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
