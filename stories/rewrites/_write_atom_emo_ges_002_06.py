#!/usr/bin/env python3
"""ATOM-EMO.GES.002-06 — Mila souffle et fait une pause (F-NAR-019, N3, EMO.GES.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.002-06"
TITLE = "Mila souffle et fait une pause"
N3 = LIMITS["N3"]
CHARS = "Mila, papa, maman"
SETTING = (
    "maison, chambre, étagère, bois, fenêtre, rayon, "
    "cire, panier, cubes, tour"
)
INDICE = "éclat d'étagère"
FIL = (
    "Le bois de l'étagère sent la cire. Près du bord, un "
    "éclat d'étagère brille. Mila veut la tour, maintenant. "
    "Les cubes glissent. La tour tombe. Épaules serrées, "
    "sourire parti, maman accroupie. Elle souffle, pause. "
    "Merci vécu. Cube derrière l'étagère, trop vite. Elle "
    "s'arrête, lit l'éclat. Un éclat d'étagère tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tapis|coussin|canapé|canape|lampe|toboggan|balançoire|"
    r"balancoire|rideau|banc|sable|seau|parc|portail|gouttière|"
    r"gouttiere|cabane|thé|tasse|plateau|cacao|dessin|livre|"
    r"horloge|parquet|chaise|tiroir|nappe|drap|ballon|entrée|"
    r"entree|casserole|soupe|carotte|chiffon|commode|gond|"
    r"confiture|fraise|camion|pupitre|rambarde|pelle|gourde|"
    r"flaque|piquet|rotin|crochet|platane|cageot|résine|resine|"
    r"botte|bottes|limace|perron|fraisier|cuivre|buis|cerceau|"
    r"grille|cour|pierre|figue|robinet|planche|émail|email|"
    r"samare|bassine|lunettes|corde|sauge|lacet|puzzle|"
    r"chaussette|chaussettes|radiateur|doudou|oreiller|plaid|"
    r"farine|saladier|pain|lit|rouleau|comptoir|"
    r"merle|miel|savon|pull|verre)\b",
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
    "on peut souffler",
    "on peut faire une pause",
    "tu as soufflé",
    "tu as souffle",
    "tu as fait une pause",
    "souffle comme le vent",
    "on souffle",
    "il faut souffler",
    "fais une pause",
    "on fait une pause",
    "je souffle",
    "je fais une pause",
    "bravo",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de tour",
    "éclat de lit",
    "éclat de pot",
    "éclat de rouleau",
    "éclat de comptoir",
    "éclat de cube",
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
    "éclat de pupitre",
    "éclat de rambarde",
    "éclat de parquet",
    "éclat de verre",
    "éclat de cacao",
    "éclat de dessin",
    "éclat de table",
    "éclat de plateau",
    "éclat de toboggan",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de rideau",
    "éclat de canapé",
    "éclat de canape",
    "éclat de lampe",
    "éclat de livre",
    "éclat d'assiette",
    "éclat d assiette",
    "éclat de coquillage",
    "éclat de cabane",
    "éclat de thé",
    "éclat de the",
    "éclat de plaid",
    "éclat de cadre",
    "éclat de marelle",
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
        emphasis="éclat d'étagère",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis gêne; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_tour_maintenant; "
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
            "sous_texte=la_tour_tombe_que_fait_elle; "
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
            "emotion=gêne puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_souffle_elle_reste; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat d'étagère",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=cube_derriere_etagere_elle_souffle; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat d'étagère",
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
    "expected_answer": "souffler",
    "accepted_examples": "souffler | une pause | s'asseoir | pause",
    "retry_prompt": (
        "Elle s'assoit. Elle souffle. Elle fait une pause. Que fait Mila ?"
    ),
    "engine_ok_text": "Oui, souffler.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "chambre,cubes",
        [
            "narrateur|Le bois de l'étagère sent la cire.",
            "narrateur|Ça sent le bois, un peu.",
            "enfant-f|Ça sent bon, papa.",
            "papa|Tu le sens, le bois, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un rayon glisse sur le bord.",
            "enfant-f|Il brille, maman.",
            "maman|Le bois est chaud ?",
            "enfant-f|Un peu, maman.",
            "maman|Les cubes attendent, dans le panier.",
            "enfant-f|Oui, maman.",
            "narrateur|Un fil de poussière danse près du bois.",
            "enfant-f|Il vole, papa.",
            "papa|Tu le vois, le fil ?",
            "enfant-f|Oui.",
            "narrateur|Le panier est lisse contre les doigts.",
            "enfant-f|Il est froid, maman.",
            "maman|Tu le sens, le panier ?",
            "enfant-f|Oui.",
            "narrateur|Près du bord, un éclat d'étagère brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Une poussière dore au-dessus du bois.",
            "enfant-f|Elle dore, maman.",
            "maman|Au-dessus du bord ?",
            "enfant-f|Oui, au-dessus.",
            "narrateur|Mila pose les mains sur le panier.",
            "narrateur|Les cubes sont un peu froids.",
            "enfant-f|On fait la tour, papa ?",
            "papa|Tu veux la tour, Mila ?",
            "enfant-f|Oui, une tour.",
            "narrateur|Les cubes tapent le bois.",
            "enfant-f|C'est dur, papa.",
            "papa|Comme une maison ?",
            "enfant-f|Oui, comme une maison.",
            "narrateur|En ce moment, Mila tire le panier vers le bois.",
            "enfant-f|Je veux la tour, maintenant !",
            "enfant-f|La tour, tout de suite.",
            "papa|Tu vois les cubes, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila pose un cube, trop vite.",
            "narrateur|Puis un autre, trop haut.",
            "narrateur|Les cubes glissent.",
            "narrateur|La tour tombe.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules se serrent.",
            "papa|Elle est tombée, Mila ?",
            "enfant-f|Oui, papa.",
            "maman|Tes lèvres sont serrées, Mila ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat d'étagère tremble, puis tient.",
            "narrateur|Les cubes restent au sol, mêlés.",
            "enfant-f|C'est trop, maman.",
            "narrateur|Maman s'accroupit à la même hauteur.",
            "narrateur|Mila regarde maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|La tour de Mila tombe.",
            "narrateur|Que fait-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "cubes",
        [
            "narrateur|Mila veut la tour, tout de suite.",
            "enfant-f|Je construis, maintenant !",
            "narrateur|Elle avance trop vite vers les cubes.",
            "narrateur|Un cube bascule.",
            "narrateur|Mila baisse les yeux.",
            "narrateur|Sa poitrine est coincée.",
            "enfant-f|C'est trop.",
            "narrateur|Mila s'assoit près du bois.",
            "narrateur|Elle souffle une fois.",
            "narrateur|Elle souffle, plus long.",
            "narrateur|Ses mains se posent sur ses genoux.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe l'étagère, un instant.",
            "narrateur|Elle écoute le silence de la chambre.",
            "papa|Tu veux la tour, Mila ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Papa, on fait quoi ?",
            "papa|On laisse un peu d'air ?",
            "enfant-f|D'accord.",
            "narrateur|Mila reste un moment, sans bouger.",
            "narrateur|Ses épaules redescendent.",
            "maman|Le bois est tiède, sous les doigts.",
            "enfant-f|Il est chaud.",
            "papa|Merci, Mila.",
            "narrateur|Papa a vu les deux, dans la chambre.",
            "narrateur|Mila reprend un cube.",
            "narrateur|Elle le pose, sans se presser.",
            "enfant-f|La tour.",
            "maman|Elle a un toit, là ?",
            "enfant-f|Oui, là.",
            "narrateur|Mila glisse la main près du panier.",
            "narrateur|Le bois est lisse, contre la peau.",
            "maman|Tes mains sont au chaud, Mila ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Papa s'assoit, puis se relève.",
            "enfant-f|On la pose au bord ?",
            "maman|La tour va jusqu'à l'étagère.",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "cubes",
        [
            "narrateur|Ils restent près de l'étagère.",
            "narrateur|La tour penche d'un côté.",
            "enfant-f|Le toit, maintenant !",
            "narrateur|Mila tire un cube trop vite.",
            "narrateur|Le cube part derrière l'étagère.",
            "enfant-f|Je ne le vois plus !",
            "narrateur|Elle se penche, trop vite.",
            "narrateur|La tour tremble, cette fois.",
            "enfant-f|Oh !",
            "narrateur|Mila s'arrête net.",
            "narrateur|Elle souffle, un filet d'air.",
            "narrateur|Elle reste un moment, les mains ouvertes.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le bord, un instant.",
            "narrateur|Elle écoute le silence de la chambre.",
            "narrateur|Au bord du bois, un éclat d'étagère luit.",
            "enfant-f|Là, sur le bois.",
            "enfant-f|Le cube est derrière, papa ?",
            "papa|Tu le vois, derrière l'étagère ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila prend le cube, sans se presser.",
            "narrateur|Elle le pose sur la tour.",
            "narrateur|Le bois est lisse et tiède.",
            "maman|Tu le vois, le bord ?",
            "enfant-f|Oui, maman.",
            "papa|La tour est près de l'étagère ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila pose un cube.",
            "narrateur|Papa pose une main sur le bois.",
            "maman|La tour tient, Mila ?",
            "enfant-f|Oui, maman.",
            "papa|Un rayon passe sur l'étagère.",
            "enfant-f|Il allume le bois.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de l'étagère.",
            "maman|La tour est arrivée, Mila ?",
            "enfant-f|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila souffle, un filet d'air.",
            "enfant-f|Le bois sent la cire.",
            "maman|Tu le sens, le bois ?",
            "enfant-f|Oui, maman.",
            "papa|La tour reste un peu, de travers.",
            "enfant-f|Elle a tenu, sur le bois.",
            "narrateur|Le bois est chaud, sous les mains.",
            "narrateur|L'étagère fait une petite ombre.",
            "enfant-f|On y retourne, après.",
            "narrateur|Un éclat d'étagère tient sur le bois.",
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
    if "s'assoit" not in blob and "s assoit" not in blob:
        raise SystemExit(f"{SID}: manque s'assoit")
    if "épaules" not in blob and "epaules" not in blob:
        raise SystemExit(f"{SID}: manque épaules")
    if "sourire" not in blob:
        raise SystemExit(f"{SID}: manque sourire")
    if "poitrine" not in blob:
        raise SystemExit(f"{SID}: manque poitrine")
    if "accroupit" not in blob:
        raise SystemExit(f"{SID}: manque accroupit")
    if "derrière l'étagère" not in blob and "derriere l'etagere" not in blob:
        raise SystemExit(f"{SID}: manque 2e ruse (derrière l'étagère)")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Mila = enfant-f)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine inventée")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain")
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
        "on peut souffler",
        "on peut faire une pause",
        "tu as soufflé",
        "tu as fait une pause",
        "souffle comme le vent",
        "bravo",
        "on souffle",
        "il faut souffler",
        "fais une pause",
        "on fait une pause",
        "je souffle",
        "je fais une pause",
        "c'est le bon geste",
        "tu as repris le geste",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "La tour de Mila tombe. Que fait-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "souffler":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != "souffler | une pause | s'asseoir | pause":
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Elle s'assoit. Elle souffle. Elle fait une pause. Que fait Mila ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    if "étagère" not in blob and "etagere" not in blob:
        raise SystemExit(f"{SID}: manque étagère")
    if "chambre" not in blob:
        raise SystemExit(f"{SID}: manque chambre")
    if "tour" not in blob:
        raise SystemExit(f"{SID}: manque tour")
    if "maintenant" not in blob:
        raise SystemExit(f"{SID}: manque maintenant")
    for ban in (
        "éclat de tour",
        "éclat de lit",
        "éclat de pot",
        "éclat de rouleau",
        "éclat de comptoir",
        "éclat de cube",
        "éclat de tapis",
        "tout doux",
        "tout calme",
        "flore",
        "sarah",
        "nino",
        "zélie",
        "zelie",
        "géraldine",
        "geraldine",
        "tapis",
        "lampe",
        "puzzle",
        "chaussette",
        "radiateur",
        "rideau",
        "doudou",
        "oreiller",
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
        "- **Leçon :** EMO.GES.002 — corps trop vite → souffler, pause "
        "(vécue : Mila veut la tour **maintenant**, cubes glissent, "
        "épaules serrées, sourire parti, maman accroupie ; elle souffle, "
        "reste ; 2e ruse derrière l'étagère). JAMAIS dite dans le récit. "
        "Pas « on peut souffler ». Pas « on peut faire une pause ». "
        "Pas « tu as soufflé ».\n"
        "- **Personnages :** Mila, papa, maman. Dump Flore/Sarah/maman → "
        "D16. Mila = enfant-f (veut la tour maintenant, trop vite, puis "
        "souffle et reste). Troupe D16. Pas de copine. Pas de maîtresse.\n"
        "- **Lieu :** maison, chambre, étagère, bois, fenêtre, rayon, "
        "cire, panier, cubes, tour. ≠ 002-05 rideau / doudou / oreiller / "
        "tapis. ≠ dump lampe / chaussettes / radiateur / puzzle.\n"
        "- **Indice unique :** éclat d'étagère (brille à l'ouverture "
        "près du bord → tremble quand la tour tombe → luit au refus "
        "derrière l'étagère → tient sur le bois). BAN éclat de tour / "
        "lit / pot / rouleau / comptoir / cube.\n"
        "- **Question moteur :** « La tour de Mila tombe. Que fait-elle "
        "? » expected dump **souffler**. accepted dump `souffler | une "
        "pause | s'asseoir | pause`. retry dump (Flore → Mila). "
        "expected/accepted/retry des autres chunks restent **null**. "
        "Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le bois de l'étagère sent la cire. Près du bord, un éclat "
        "d'étagère brille. Fil de poussière, rayon, panier. Mila veut "
        "la tour **maintenant**. Cubes trop vite, trop haut. La tour "
        "tombe. Sourire parti. Maman s'accroupit. Elle souffle, reste. "
        "Merci vécu. Deuxième ruse : cube derrière l'étagère, trop vite, "
        "tour qui tremble. Elle s'arrête, lit l'éclat. Un éclat "
        "d'étagère tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : maison, chambre, étagère, bois, fenêtre, rayon, "
        "cire. ≠ dump lampe / tapis / chaussettes / radiateur. ≠ 002-05 "
        "rideau / doudou / oreiller.\n"
        "- Désir : la tour, maintenant, avec les cubes du panier.\n"
        "- Objet : cubes, tour, étagère, panier.\n"
        "- Indice unique : éclat d'étagère, vu dès l'ouverture près "
        "du bord, payé sur le bois. Pas éclat de cube / tour / lit.\n"
        "- Urgence douce : Mila accélère, pose trop haut.\n"
        "- Imprévu 1 : les cubes glissent, la tour tombe. Poitrine "
        "coincée, sourire parti, épaules serrées.\n"
        "- Cue : maman à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : cube trop vite, derrière l'étagère, "
        "tour qui tremble.\n"
        "- Résolution : elle s'assoit, souffle, reste, observe, écoute, "
        "retrouve l'éclat, pose sans se presser.\n"
        "- Retour : tour de travers, cire, éclat sur le bois.\n\n"
        "## Vécu\n\n"
        "Mila veut la tour **maintenant**. Impatience, puis chute, "
        "sourire parti. Maman se baisse, pose une question, ne récite "
        "pas la règle. Mila agit : s'asseoir, souffler, rester. Merci "
        "vécu. Fin : l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Mila souffle et fait une pause (noyau + D16). "
        "Relance : Que fait-elle ? expected souffler.\n"
        "- Lieu du dump (chambre, tour de cubes) sans tapis / lampe / "
        "chaussettes / radiateur / puzzle. Papa et maman présents.\n"
        "- Ouverture inventée (cire du bois de l'étagère), pas un "
        "gabarit v2, pas « Le soir, la lampe ronde » du dump en "
        "première ligne.\n"
        "- Indice unique : éclat d'étagère. BAN éclat de tour / lit / "
        "pot / rouleau / comptoir / cube. Pas tache/flèche/marque/"
        "symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip dump « On peut souffler » / « Bravo » / puzzle. "
        "Une phrase par ligne, ponctuation, pas de puces.\n"
        "- Leçon non dite : on la voit quand Mila s'assoit, souffle, "
        "reste. Pas « on peut souffler ». Pas « tu as fait une pause ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « La tour de Mila tombe. Que fait-elle "
        "? ». expected dump souffler. retry dump (Mila). 5 chunks, "
        "kinds inchangés. expected/accepted/retry null hors Q.\n"
        "- example4 051 / 083 / 015 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_001_04.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers l'étagère.\n"
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
