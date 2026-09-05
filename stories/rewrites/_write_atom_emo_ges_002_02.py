#!/usr/bin/env python3
"""ATOM-EMO.GES.002-02 — Aniss souffle et fait une pause (F-NAR-019, N3, EMO.GES.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.002-02"
TITLE = "Aniss souffle et fait une pause"
N3 = LIMITS["N3"]
CHARS = "Aniss, papa, maman"
SETTING = (
    "salon, fenêtre, cubes, bois, soleil, pain, "
    "boulangerie, comptoir, file, papier"
)
INDICE = "éclat de comptoir"
FIL = (
    "Un air de pain chaud glisse dans le salon. Près de la "
    "fenêtre, un éclat de comptoir brille. Aniss veut la tour "
    "maintenant. Elle tremble. Ventre serré, sourire parti, "
    "papa accroupi. Il souffle, pause. Merci vécu. Deuxième "
    "ruse à la boulangerie. Un éclat de comptoir tient sur "
    "le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tapis|parquet|canapé|canape|balançoire|balancoire|banc|"
    r"thym|seau|coussin|plaid|sable|toboggan|gouttière|gouttiere|"
    r"colline|portail|trèfle|trefle|miel|moulin|plancher|"
    r"tableau|craie|casier|carotte|rambarde|zinc|"
    r"flaque|piquet|rotin|crochet|platane|cageot|résine|resine|"
    r"botte|bottes|limace|perron|chaise|tiroir|fraisier|"
    r"cuivre|buis|cerceau|grille|cour|pierre|nappe|figue|robinet|"
    r"planche|émail|email|samare|bassine|lunettes|corde|drap|"
    r"ballon|entrée|entree|horloge|bol|casserole|soupe|"
    r"chiffon|sauge|lacet|commode|gond|confiture|"
    r"tartine|fraise|camion|radiateur|manteau|pupitre|gomme|"
    r"pull|feuille|farine|croûte|croute|beurre|pantoufle|"
    r"pantoufles|rideau|vitre|carrelage|serviette|linge)\b",
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
    "dire stop, c'est permis",
    "dire stop c'est permis",
    "on s'éloigne",
    "on s eloigne",
    "on va vers un adulte",
    "tu as repris le geste",
    "tu as dit stop",
    "tu t'es éloigné",
    "tu t es eloigne",
    "tu t'es éloignée",
    "c'est le bon geste",
    "tu as bien écouté ton corps",
    "tu as bien ecoute ton corps",
    "tu peux souffler",
    "tu peux faire une pause",
    "on peut souffler",
    "on peut faire une pause",
    "souffle comme le vent",
    "tu as soufflé",
    "tu as fait une pause",
    "j'ai soufflé",
    "j'ai fait une pause",
    "même leçon",
    "souffler aide",
    "une pause aide",
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
    "éclat de canapé",
    "éclat de canape",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de pupitre",
    "éclat de feuille",
    "éclat de sac",
    "éclat de gomme",
    "éclat de pull",
    "éclat de tour",
    "éclat de rideau",
    "éclat de toboggan",
    "éclat de plaid",
    "éclat de livre",
    "éclat de cadre",
    "éclat de marelle",
    "éclat de plinthe",
    "éclat de cubes",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
    "yanis",
    "sara ",
    "victorino",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de comptoir",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis trop_plein; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_tour_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Aniss",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=corps_trop_plein_que_fait_il; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="souffle",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=trop_plein puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_souffle_il_fait_une_pause; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de comptoir",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=pain_maintenant_il_souffle_il_reste; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de comptoir",
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
    "expected_answer": None,
    "accepted_examples": None,
    "retry_prompt": None,
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "fenetre",
        [
            "narrateur|Un air de pain chaud glisse dans le salon.",
            "enfant-m|Ça sent le pain, papa.",
            "papa|Tu le sens, le pain, Aniss ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le soleil tient les cubes, près du bois.",
            "narrateur|Les cubes sont lisses, un peu froids.",
            "enfant-m|Ils sont froids, maman.",
            "maman|Tu les touches, les cubes ?",
            "enfant-m|Oui, maman.",
            "narrateur|Près de la fenêtre, un éclat de comptoir brille.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|La boulangerie est là, de l'autre côté.",
            "enfant-m|Le pain est là-bas.",
            "maman|On ira chercher le pain, plus tard.",
            "enfant-m|Oui.",
            "papa|La tour, d'abord ?",
            "enfant-m|La tour, maintenant !",
            "narrateur|Le bois sent le soleil.",
            "enfant-m|Il est chaud.",
            "papa|Le bois, sous tes mains ?",
            "enfant-m|Oui.",
            "narrateur|En ce moment, Aniss prend un cube.",
            "narrateur|Il veut une tour, très haute.",
            "enfant-m|Tout de suite.",
            "enfant-m|Elle va monter.",
            "narrateur|Il pose un cube sur le bois.",
            "narrateur|Puis un autre, trop vite.",
            "papa|Tu poses les cubes, Aniss ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains vont vite, Aniss ?",
            "enfant-m|Un peu, maman.",
            "narrateur|La tour grandit, un peu penchée.",
            "narrateur|Elle tremble sur le bois.",
            "narrateur|Un cube glisse.",
            "narrateur|La tour tombe, sourdement.",
            "enfant-m|Oh.",
            "narrateur|Aniss tremble un peu.",
            "narrateur|Son ventre se serre.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "enfant-m|C'est trop, papa.",
            "papa|Tu vois la tour, Aniss ?",
            "enfant-m|Oui, papa.",
            "maman|Tes épaules sont hautes, Aniss ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Aniss regarde papa.",
            "narrateur|L'éclat de comptoir tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss sent son corps trop plein.",
            "narrateur|Que fait-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "cubes",
        [
            "narrateur|Aniss veut la tour, maintenant.",
            "enfant-m|Tout de suite !",
            "narrateur|Il pose les cubes trop vite.",
            "narrateur|La tour penche, puis tombe.",
            "narrateur|Son ventre reste serré.",
            "narrateur|Le sourire ne revient pas.",
            "enfant-m|Oh.",
            "narrateur|Aniss s'assoit près du bois.",
            "narrateur|Il pose les mains sur ses genoux.",
            "narrateur|Il souffle, un filet d'air.",
            "narrateur|L'air sort, long.",
            "narrateur|Il fait une pause.",
            "papa|Tu restes près de nous, Aniss ?",
            "enfant-m|Je reste ici, papa ?",
            "papa|On s'assoit, puis on regarde.",
            "enfant-m|D'accord.",
            "narrateur|Aniss reste un moment, les mains ouvertes.",
            "narrateur|Sa poitrine descend, plus lente.",
            "papa|Merci, Aniss.",
            "narrateur|Papa a vu les deux, près des cubes.",
            "maman|Le bois est tiède, sous les doigts.",
            "enfant-m|Il est chaud.",
            "narrateur|Aniss reprend un cube, sans se presser.",
            "enfant-m|Sans me presser.",
            "papa|Il tient, là ?",
            "enfant-m|Oui, là.",
            "narrateur|La tour est petite.",
            "narrateur|Elle tient sur le bois.",
            "maman|Tes mains sont au chaud, Aniss ?",
            "enfant-m|Un peu, maman.",
            "enfant-m|On va au pain ?",
            "maman|Le sac est près de la porte ?",
            "enfant-m|Oui, maman.",
            "papa|Tu prends le sac, Aniss ?",
            "enfant-m|Oui, papa.",
            "narrateur|Aniss glisse la main sur le bois.",
            "enfant-m|Le petit point.",
            "papa|Il brille, là ?",
            "enfant-m|Oui, là.",
            "narrateur|Aniss pose les mains sur le bois.",
            "narrateur|Il reste, sans se presser.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "boulangerie",
        [
            "narrateur|Ils sortent vers la rue.",
            "narrateur|La porte de la boulangerie s'ouvre.",
            "enfant-m|Le pain, maintenant !",
            "narrateur|Aniss avance trop vite.",
            "narrateur|La file ne bouge pas.",
            "narrateur|Le pain tiède est là, très près.",
            "enfant-m|Je le prends !",
            "narrateur|Aniss tend la main trop vite.",
            "narrateur|Son ventre se serre.",
            "enfant-m|Oh.",
            "narrateur|Aniss refuse de foncer.",
            "narrateur|Il s'arrête net.",
            "narrateur|Il souffle, un filet d'air.",
            "narrateur|Il reste près de papa.",
            "narrateur|Personne ne parle, un moment.",
            "narrateur|Au bord du bois, un éclat de comptoir luit.",
            "enfant-m|Là, sur le bois.",
            "enfant-m|J'attends, papa ?",
            "narrateur|Papa ne dit rien, d'abord.",
            "narrateur|Il reste à la même hauteur.",
            "papa|Tu l'entends, la file ?",
            "enfant-m|Oui, papa.",
            "maman|La clochette a sonné, Aniss ?",
            "enfant-m|Oui, maman.",
            "narrateur|La file avance, un pas.",
            "narrateur|Aniss hoche la tête, sans se presser.",
            "papa|Tu sens le pain, Aniss ?",
            "enfant-m|Oui, papa.",
            "maman|Le papier est près du bois ?",
            "enfant-m|Oui, maman.",
            "narrateur|Papa tend le pain, très tiède.",
            "narrateur|Aniss pose les deux mains dessus.",
            "papa|Le pain tient, Aniss ?",
            "enfant-m|Oui, papa.",
            "maman|Un rayon passe sur le comptoir.",
            "enfant-m|Il allume le bois.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du comptoir.",
            "maman|Le pain a eu son tour, Aniss ?",
            "enfant-m|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-m|Oui, papa.",
            "narrateur|Aniss souffle, un filet d'air.",
            "enfant-m|Le pain sent bon.",
            "maman|Tu le sens, le pain ?",
            "enfant-m|Oui, maman.",
            "papa|Le papier reste un peu, à plat.",
            "enfant-m|Il a tenu, sur le bois.",
            "narrateur|La rue est calme, sous les mains.",
            "narrateur|Le papier fait une petite ombre.",
            "enfant-m|On y revient, après.",
            "narrateur|Un éclat de comptoir tient sur le bois.",
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
        for key in ("expected_answer", "accepted_examples", "retry_prompt"):
            if cid != "CHK_T0000_P0000_Q0001" and by[cid].get(key) is not None:
                raise SystemExit(f"{cid}: {key} devait rester null")
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
    if "souffle" not in blob:
        raise SystemExit(f"{SID}: manque souffle")
    if "pause" not in blob:
        raise SystemExit(f"{SID}: manque pause")
    if "ventre" not in blob:
        raise SystemExit(f"{SID}: manque ventre serré")
    if "sourire" not in blob:
        raise SystemExit(f"{SID}: manque sourire parti")
    if "accroupit" not in blob:
        raise SystemExit(f"{SID}: manque papa accroupi")
    if "tremble" not in blob:
        raise SystemExit(f"{SID}: manque tremble")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Aniss = enfant-m)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse parlante")
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
        "tu peux souffler",
        "tu peux faire une pause",
        "on peut souffler",
        "on peut faire une pause",
        "souffle comme le vent",
        "tu as soufflé",
        "tu as fait une pause",
        "même leçon",
        "souffler aide",
        "une pause aide",
        "tu as repris le geste",
        "c'est le bon geste",
        "on peut jouer",
        "on peut attendre",
        "il faut attendre",
        "l'histoire est finie",
        "mission accomplie",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Aniss sent son corps trop plein. Que fait-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") is not None:
        raise SystemExit(f"{SID}: expected_answer inventé")
    if q.get("accepted_examples") is not None:
        raise SystemExit(f"{SID}: accepted_examples inventé")
    if q.get("retry_prompt") is not None:
        raise SystemExit(f"{SID}: retry inventé")
    if "boulangerie" not in blob:
        raise SystemExit(f"{SID}: manque boulangerie")
    if "comptoir" not in blob:
        raise SystemExit(f"{SID}: manque comptoir")
    if "salon" not in blob:
        raise SystemExit(f"{SID}: manque salon")
    if "tour" not in blob:
        raise SystemExit(f"{SID}: manque tour")
    if "maintenant" not in blob:
        raise SystemExit(f"{SID}: manque maintenant")
    n_souffle = sum(
        1
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("narrateur|") and "souffle" in ln.lower()
        and c["chunk_id"] in ("CHK_T0000_P0000_C0001", "CHK_T0000_P0000_END")
    )
    if n_souffle != 2:
        raise SystemExit(f"{SID}: souffle vécu ×{n_souffle} (voulu 2)")
    for ban in (
        "éclat de tour",
        "éclat de rideau",
        "éclat de balançoire",
        "éclat de toboggan",
        "éclat de plaid",
        "éclat de farine",
        "éclat de croûte",
        "éclat de croute",
        "farine",
        "croûte",
        "croute",
        "tout doux",
        "tout calme",
        "yanis",
        "victorino",
        "sara ",
        "kenzo",
        "iris",
        "maya",
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
        "- **Leçon :** EMO.GES.002 — corps trop plein → souffler, pause "
        "(vécue : Aniss veut la tour maintenant, elle tremble, ventre "
        "serré, sourire parti, papa accroupi, il souffle, il fait une "
        "pause ; à la boulangerie le pain maintenant, il souffle, il "
        "reste). JAMAIS dite dans le récit. Pas « tu peux souffler ». "
        "Pas « tu peux faire une pause ». Pas « même leçon ».\n"
        "- **Personnages :** Aniss, papa, maman. Dump Yanis/papa → D16. "
        "Aniss = enfant-m (veut la tour maintenant, trop vite, puis "
        "souffle, pause). Troupe D16. Maman présente.\n"
        "- **Lieu :** salon puis boulangerie : fenêtre, cubes, bois, "
        "soleil, pain, comptoir, file, papier. ≠ dump tapis / flaque / "
        "radiateur / manteau / farine. ≠ 002-01 pantoufles / éclat de "
        "tour.\n"
        "- **Indice unique :** éclat de comptoir (brille à l'ouverture "
        "près de la fenêtre → tremble à la chute → luit à la "
        "boulangerie → tient sur le bois). BAN éclat de tour / croûte / "
        "farine / rideau / balançoire / toboggan / plaid.\n"
        "- **Question moteur :** « Aniss sent son corps trop plein. Que "
        "fait-il ? » expected / accepted / retry dump **null**. Non "
        "récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un air de pain chaud glisse dans le salon. Près de la fenêtre, "
        "un éclat de comptoir brille. Cubes, bois, soleil. Aniss veut "
        "la tour **maintenant**. Elle tremble. Ventre serré. Sourire "
        "parti. Papa s'accroupit. Il souffle, pause. Merci vécu. "
        "Deuxième ruse : le pain maintenant, à la boulangerie. Il "
        "souffle, il reste. Un éclat de comptoir tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon puis boulangerie, fenêtre, cubes, bois, soleil, "
        "pain, comptoir, file, papier. ≠ dump tapis / flaque / farine. "
        "≠ 002-01 pantoufles / éclat de tour.\n"
        "- Désir : la tour, maintenant, très haute.\n"
        "- Objet : cubes, bois, pain, papier, comptoir.\n"
        "- Indice unique : éclat de comptoir, vu dès l'ouverture près de "
        "la fenêtre, payé sur le bois. Pas éclat de tour / croûte / "
        "farine / rideau.\n"
        "- Urgence douce : Aniss veut la tour maintenant, pose trop vite.\n"
        "- Imprévu 1 : la tour tombe. Ventre serré. Sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : à la boulangerie, le pain maintenant, "
        "la main trop vite.\n"
        "- Résolution : il souffle, il fait une pause, il reste.\n"
        "- Retour : pain tiède, éclat sur le bois.\n\n"
        "## Vécu\n\n"
        "Aniss veut la tour **maintenant**. Impatience, puis chute, "
        "sourire parti. Papa se baisse, pose une question, ne récite "
        "pas la règle. Ils agissent : souffler, rester, pause. Merci "
        "vécu. Fin : l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Aniss souffle et fait une pause (noyau dump, D16). "
        "Relance : Que fait-il ? expected dump **null**.\n"
        "- Lieu du dump (salon puis boulangerie) sans tapis / flaque / "
        "farine / croûte. Maman présente. Aniss = enfant-m.\n"
        "- Ouverture inventée (air de pain chaud dans le salon), pas un "
        "gabarit v2, pas « La pluie tapote la vitre du salon » du dump "
        "en première ligne.\n"
        "- Indice unique : éclat de comptoir. BAN éclat de tour / croûte "
        "/ farine / rideau / balançoire. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » / « farine » / "
        "« tu peux souffler » du dump.\n"
        "- Leçon non dite : on la voit quand la tour tombe, quand Aniss "
        "souffle, quand il fait une pause, quand il le refait à la "
        "boulangerie. Pas « tu peux souffler ». Pas « même leçon ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur D16 : « Aniss sent son corps trop plein. Que "
        "fait-il ? ». expected / accepted / retry laissés **null**. 5 "
        "chunks, kinds inchangés.\n"
        "- example4 047 / 079 / 011 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_001_02.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers la boulangerie.\n"
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
