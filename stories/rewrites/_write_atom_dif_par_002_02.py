#!/usr/bin/env python3
"""ATOM-DIF.PAR.002-02 — Amir laisse le temps à Victorina (F-NAR-019, N3, DIF.PAR.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.002-02"
TITLE = "Amir laisse le temps à Victorina"
N3 = LIMITS["N3"]
CHARS = "Amir, Victorina, papa, maman"
SETTING = (
    "classe, pupitre, fenêtre, sac, feuille, pull, "
    "bois, lumière, gomme"
)
INDICE = "éclat de pupitre"
FIL = (
    "La lumière pose un carré chaud sur le bois. Près du sac, "
    "un éclat de pupitre brille. Victorina cherche un mot. Amir "
    "le connaît, veut le dire maintenant, ouvre la bouche. Sourire "
    "parti. Il refuse de foncer, attend. Merci vécu. Deuxième ruse : "
    "un autre mot. Un éclat de pupitre tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tableau|craie|casier|carotte|rambarde|zinc|parquet|"
    r"flaque|piquet|portail|rotin|crochet|platane|cageot|résine|"
    r"resine|botte|bottes|limace|perron|chaise|tiroir|fraisier|"
    r"cuivre|buis|cerceau|grille|cour|pierre|nappe|figue|robinet|"
    r"planche|émail|email|samare|bassine|lunettes|corde|drap|"
    r"ballon|entrée|entree|horloge|bol|casserole|soupe|"
    r"chiffon|sauge|lacet|commode|gond|banc|coussin|confiture|"
    r"tartine|fraise|camion|tapis|radiateur|manteau)\b",
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
    "les trois mots",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "on peut jouer",
    "on peut attendre",
    "on peut demander",
    "on peut laisser",
    "ce n'est pas une faute",
    "n'est pas une faute",
    "pas une faute",
    "vous jouez",
    "on joue",
    "parle peu",
    "elle parle peu",
    "forcer la parole",
    "on ne force pas",
    "regarder, c'est",
    "tu as su attendre",
    "on n'imite pas",
    "on n imite pas",
    "on n'achève pas",
    "on n acheve pas",
    "on attend la fin",
    "laisser le temps",
    "vous parlez l'un",
    "on écoute jusqu'au bout",
    "on ecoute jusqu'au bout",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de pin",
    "éclat de pomme",
    "éclat de sève",
    "éclat de seve",
    "éclat de botte",
    "éclat de limace",
    "éclat de perron",
    "éclat de chaise",
    "éclat de tiroir",
    "éclat de fraisier",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de casserole",
    "éclat de citron",
    "éclat de coquille",
    "éclat de zeste",
    "éclat de coussin",
    "éclat de figue",
    "éclat de robinet",
    "éclat de planche",
    "éclat de cerceau",
    "éclat d'émail",
    "éclat d'email",
    "éclat de samare",
    "éclat de bassine",
    "éclat de nappe",
    "éclat de farine",
    "éclat de tablier",
    "éclat de biscuit",
    "éclat de toit",
    "éclat de volet",
    "éclat de pavé",
    "éclat de pave",
    "éclat de parapluie",
    "éclat de bâche",
    "éclat de bache",
    "éclat de poire",
    "éclat de seau",
    "éclat de pompon",
    "éclat de carotte",
    "éclat de carton",
    "éclat de mousse",
    "éclat de laine",
    "éclat de tasse",
    "éclat de crayon",
    "éclat de cartable",
    "éclat de wagon",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de pinceau",
    "éclat de ballon",
    "éclat de manteau",
    "éclat de marche",
    "éclat de vitre",
    "éclat de grain",
    "éclat de liste",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de couloir",
    "éclat de plaque",
    "éclat de dalle",
    "éclat de pierre",
    "éclat de grille",
    "éclat de couvercle",
    "éclat de thermos",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de caillou",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat de lessive",
    "éclat de carreau",
    "éclat de coton",
    "éclat de gravier",
    "éclat de gilet",
    "éclat de lunettes",
    "éclat de flaque",
    "éclat de piquet",
    "éclat de portail",
    "éclat de rotin",
    "éclat de crochet",
    "éclat de platane",
    "éclat de cageot",
    "éclat de résine",
    "éclat de resine",
    "éclat de carte",
    "éclat de tapis",
    "éclat de vapeur",
    "éclat de bol",
    "éclat de chiffon",
    "éclat de sauge",
    "éclat de lacet",
    "éclat de commode",
    "éclat de gond",
    "éclat de banc",
    "éclat d'horloge",
    "éclat d horloge",
    "éclat de rambarde",
    "éclat de zinc",
    "éclat de parquet",
    "éclat de feuille",
    "éclat de sac",
    "éclat de gomme",
    "éclat de pull",
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
        emphasis="éclat de pupitre",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_dire_le_mot_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Amir",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=victorina_cherche_un_mot_que_fait_amir; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="canard",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_refuse_de_foncer_attend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de pupitre",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=autre_mot_trop_vite_il_attend; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de pupitre",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "attendre",
    "accepted_examples": "attendre | laisser le temps | il attend | la phrase",
    "retry_prompt": "On n'achève pas à sa place. Que fait Amir ?",
    "engine_ok_text": "Oui, attendre.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "classe",
        [
            "narrateur|La lumière pose un carré chaud sur le bois.",
            "narrateur|Ça sent le papier et la laine.",
            "enfant-m|Ça sent le pull, papa.",
            "papa|Tu le sens, le bois, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Un sac glisse contre un pupitre.",
            "narrateur|Le tissu fait un bruit court.",
            "enfant-m|Il frotte, maman.",
            "maman|Le sac tient près du bois ?",
            "enfant-m|Oui, maman.",
            "narrateur|Près du sac, un éclat de pupitre brille.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|La fenêtre tient un bout de ciel pâle.",
            "enfant-m|Il est clair, papa.",
            "papa|Le ciel, là-bas ?",
            "enfant-m|Oui, là-bas.",
            "narrateur|Victorina pose une feuille sur le bois.",
            "narrateur|La feuille tremble entre ses doigts.",
            "enfant-m|Je connais le mot, maintenant !",
            "enfant-m|Je le dis, tout de suite.",
            "papa|Le mot de Victorina ?",
            "enfant-m|Oui.",
            "enfant-m|C'est facile.",
            "narrateur|En ce moment, Amir se penche vers elle.",
            "narrateur|Victorina ouvre la bouche.",
            "copine|J'ai vu.",
            "narrateur|Elle s'arrête.",
            "narrateur|Elle cherche le mot.",
            "narrateur|Amir a vu le canard, lui aussi.",
            "narrateur|Il sait le mot.",
            "narrateur|Il ouvre la bouche.",
            "enfant-m|Canard !",
            "narrateur|Le mot est sorti trop vite.",
            "narrateur|Victorina baisse les yeux.",
            "enfant-m|Oh.",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "papa|Tu vois Victorina, Amir ?",
            "enfant-m|Oui, papa.",
            "maman|Ta bouche est ouverte, Amir ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de pupitre tremble, puis tient.",
            "narrateur|Victorina serre la feuille.",
            "enfant-m|Elle cherche, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Amir regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorina cherche un mot.",
            "narrateur|Que fait Amir ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "feuille",
        [
            "narrateur|Amir connaît le mot.",
            "enfant-m|Je le dis, maintenant !",
            "narrateur|Il avance trop vite vers le mot.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "narrateur|Victorina baisse les yeux.",
            "narrateur|Elle serre la feuille contre elle.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Amir refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe la feuille, un instant.",
            "narrateur|Il écoute le silence de la classe.",
            "papa|Tu restes près d'elle, Amir ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Papa, on fait quoi ?",
            "papa|On pose les mains, puis on reste.",
            "enfant-m|D'accord.",
            "narrateur|Amir reste un moment, les mains ouvertes.",
            "narrateur|Il attend.",
            "narrateur|Victorina souffle.",
            "copine|J'ai vu un canard.",
            "enfant-m|Le canard.",
            "copine|Oui.",
            "papa|Merci, Amir.",
            "narrateur|Papa a vu les deux, près du pupitre.",
            "maman|Le papier est tiède, sous les doigts.",
            "enfant-m|Il est chaud.",
            "narrateur|Victorina glisse la main sur le dessin.",
            "enfant-m|Le canard.",
            "papa|Il a un bec, là ?",
            "enfant-m|Oui, là.",
            "narrateur|Amir pose les mains sur le bois.",
            "narrateur|Il reste, sans se presser.",
            "maman|Tes mains sont au chaud, Amir ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Victorina s'assoit plus droit.",
            "copine|Orange.",
            "enfant-m|Orange, oui.",
            "maman|La feuille tient sur le pupitre ?",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "sac",
        [
            "narrateur|Ils restent près du pupitre.",
            "narrateur|Victorina reprend la feuille.",
            "copine|Et après, il a.",
            "narrateur|Elle cherche.",
            "enfant-m|La suite, maintenant !",
            "narrateur|Amir ouvre la bouche trop vite.",
            "narrateur|Le mot pousse contre les dents.",
            "narrateur|Amir avance les lèvres, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Amir refuse de foncer, cette fois.",
            "narrateur|Sa bouche se ferme, puis s'ouvre sans bruit.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe la feuille, un instant.",
            "narrateur|Il écoute le silence du pupitre.",
            "narrateur|Au bord du bois, un éclat de pupitre luit.",
            "enfant-m|Là, sur le bois.",
            "enfant-m|Tu dis la suite, Victorina ?",
            "narrateur|Victorina ne dit rien, d'abord.",
            "narrateur|Elle tient la feuille, sans parler.",
            "copine|Il a fait coin-coin.",
            "narrateur|Amir hoche la tête, sans se presser.",
            "narrateur|Victorina souffle, plus lentement.",
            "narrateur|Le papier est lisse et tiède.",
            "papa|Tu l'entends, le canard ?",
            "enfant-m|Oui, papa.",
            "maman|La feuille est près du sac ?",
            "enfant-m|Oui, maman.",
            "narrateur|Une gomme roule vers le bord.",
            "narrateur|Amir pose une main dessus.",
            "narrateur|Victorina pose la suivante.",
            "papa|La gomme tient, Amir ?",
            "enfant-m|Oui, papa.",
            "maman|Un rayon passe sur le pupitre.",
            "enfant-m|Il allume le bois.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du pupitre.",
            "maman|Le canard a eu sa phrase, Amir ?",
            "enfant-m|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-m|Oui, papa.",
            "narrateur|Amir souffle, un filet d'air.",
            "enfant-m|Le papier sent bon.",
            "maman|Tu le sens, le dessin ?",
            "enfant-m|Oui, maman.",
            "papa|La feuille reste un peu, à plat.",
            "enfant-m|Elle a tenu, sur le bois.",
            "copine|Canard.",
            "narrateur|Le pupitre est chaud, sous les mains.",
            "narrateur|La feuille fait une petite ombre.",
            "enfant-m|On y revient, après.",
            "narrateur|Un éclat de pupitre tient sur le bois.",
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
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "ouvre la bouche" not in blob:
        raise SystemExit(f"{SID}: manque ouvre la bouche")
    if "sourire" not in blob:
        raise SystemExit(f"{SID}: manque sourire parti")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Amir = enfant-m, Victorina = copine)")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Victorina absente (copine)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse parlante")
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
    if not any(r == "enfant-m" for r in roles):
        raise SystemExit(f"{SID}: enfant-m absent")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "ce n'est pas une faute",
        "n'est pas une faute",
        "on peut jouer",
        "on peut attendre",
        "on peut demander",
        "on peut laisser",
        "on joue",
        "vous jouez",
        "il faut attendre",
        "on doit demander",
        "il faut demander",
        "parle peu",
        "elle parle peu",
        "forcer la parole",
        "tu as su attendre",
        "laisser le temps",
        "on n'achève pas",
        "on attend la fin",
        "jusqu'au bout",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Victorina cherche un mot. Que fait Amir ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "attendre | laisser le temps | il attend | la phrase"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "On n'achève pas à sa place. Que fait Amir ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    n_copine = sum(
        1
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    )
    if n_copine > 7:
        raise SystemExit(f"{SID}: Victorina parle trop ({n_copine})")
    if n_copine < 3:
        raise SystemExit(f"{SID}: Victorina trop muette ({n_copine})")
    if "pupitre" not in blob:
        raise SystemExit(f"{SID}: manque pupitre")
    if "feuille" not in blob:
        raise SystemExit(f"{SID}: manque feuille")
    if "canard" not in blob:
        raise SystemExit(f"{SID}: manque canard")
    if "il attend" not in blob:
        raise SystemExit(f"{SID}: manque il attend")
    for ban in (
        "tableau",
        "craie",
        "casier",
        "éclat de carotte",
        "éclat de rambarde",
        "éclat de zinc",
        "éclat de parquet",
        "éclat de banc",
        "tout doux",
        "tout calme",
        "kenzo",
        "iris",
        "maya",
        "sarah",
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
        "- **Leçon :** DIF.PAR.002 — quand l'autre cherche un mot, on attend "
        "(vécue : Amir connaît le mot, veut le dire maintenant, ouvre la "
        "bouche, Canard trop vite, sourire parti, il refuse de foncer, "
        "attend, Victorina finit). JAMAIS dite dans le récit. Pas « laisser "
        "le temps ». Pas « on n'achève pas ». Pas de maîtresse parlante.\n"
        "- **Personnages :** Amir, Victorina, papa, maman. Dump Kenzo/Iris/"
        "maîtresse/papa → D16. Amir = enfant-m (connaît le mot, veut le dire "
        "maintenant, trop vite, puis refuse de foncer). Victorina = copine "
        "(cherche le mot, j'ai vu, canard, coin-coin). Troupe D16. Maîtresse "
        "présente au dump : ne parle pas, absente du récit.\n"
        "- **Lieu :** classe, pupitre, fenêtre, sac, feuille, pull, bois, "
        "lumière, gomme. ≠ dump entrée / pluie / bottes. BAN tableau / craie "
        "/ casier.\n"
        "- **Indice unique :** éclat de pupitre (brille à l'ouverture près "
        "du sac → tremble au mot trop vite → luit au refus coin-coin → tient "
        "sur le bois). BAN éclat de tableau / craie / casier / carotte "
        "(002-01) / rambarde / zinc.\n"
        "- **Question moteur :** « Victorina cherche un mot. Que fait "
        "Amir ? » expected dump **attendre**. accepted dump. retry dump "
        "Kenzo→Amir. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La lumière pose un carré chaud sur le bois. Près du sac, un éclat "
        "de pupitre brille. Feuille, pull, ciel pâle. Victorina veut "
        "raconter. Amir connaît le mot, veut le dire **maintenant**. Il "
        "ouvre la bouche. Canard trop vite. Sourire parti. Papa s'accroupit. "
        "Il refuse de foncer. Il attend. Merci vécu. Deuxième ruse : la "
        "suite, coin-coin trop vite, le pupitre. Il s'arrête, lit l'éclat. "
        "Un éclat de pupitre tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : classe, pupitre, fenêtre, sac, feuille, pull, gomme. ≠ "
        "ENE flaque / piquet. ≠ dump bottes / radiateur. ≠ 002-01 carotte.\n"
        "- Désir : dire le mot, maintenant, à la place de Victorina.\n"
        "- Objet : feuille, canard dessiné, gomme, sac.\n"
        "- Indice unique : éclat de pupitre, vu dès l'ouverture près du sac, "
        "payé sur le bois. Pas éclat de tableau / craie / casier / carotte "
        "/ rambarde / zinc.\n"
        "- Urgence douce : Victorina cherche, Amir accélère le mot.\n"
        "- Imprévu 1 : Amir dit Canard trop vite. Victorina baisse les yeux.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : la suite, coin-coin trop vite, elle "
        "cherche encore.\n"
        "- Résolution : il refuse de foncer, observe, écoute le silence, "
        "retrouve l'éclat, attend, Victorina finit.\n"
        "- Retour : feuille à plat, canard vécu, éclat sur le bois.\n\n"
        "## Vécu\n\n"
        "Amir connaît le mot, veut le dire **maintenant**. Impatience, puis "
        "mot trop vite, sourire parti. Victorina pose sa limite (yeux bas, "
        "feuille serrée, souffle, canard, coin-coin). Papa se baisse, pose "
        "une question, ne récite pas la règle. Ils agissent : refermer la "
        "bouche, attendre, laisser Victorina finir. Merci vécu. Fin : "
        "l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Amir laisse le temps à Victorina (noyau dump Kenzo "
        "laisse le temps à Iris, D16). Relance : Que fait Amir ? expected "
        "attendre.\n"
        "- Lieu du dump (classe, pas entrée pluie). Maman présente. "
        "Victorina = copine. Maîtresse non parlante, non nommée.\n"
        "- Ouverture inventée (lumière sur le bois), pas un gabarit v2, "
        "pas « Les chaussures font un petit lac » du dump en première "
        "ligne.\n"
        "- Indice unique : éclat de pupitre. BAN éclat de tableau / craie "
        "/ casier / carotte / rambarde / zinc. Pas tache/flèche/marque/"
        "symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » du dump.\n"
        "- Leçon non dite : on la voit quand le mot sort trop vite, quand "
        "Amir s'arrête, quand il attend, quand Victorina finit. Pas "
        "« laisser le temps ». Pas « on n'achève pas ». Pas « tu as su "
        "attendre ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur D16 : « Victorina cherche un mot. Que fait "
        "Amir ? ». expected dump. retry dump Kenzo→Amir. 5 chunks, kinds "
        "inchangés.\n"
        "- example4 032 / 064 / 096 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_par_001_01.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers la suite du récit.\n"
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
