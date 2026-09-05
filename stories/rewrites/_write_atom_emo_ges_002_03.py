#!/usr/bin/env python3
"""ATOM-EMO.GES.002-03 — Victorino souffle au jardin (F-NAR-019, N2, EMO.GES.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.002-03"
TITLE = "Victorino souffle au jardin"
N2 = LIMITS["N2"]
CHARS = "Victorino, papa, maman"
SETTING = (
    "jardin, château de terre, pots, terre, bord, soleil, "
    "ombre, poussière, fourmi, basilic"
)
INDICE = "éclat de pot"
FIL = (
    "Les pots tièdes font une ombre étroite. Près du bord, un "
    "éclat de pot brille. Victorino veut le château, maintenant. "
    "La terre trop vite, le château s'effondre. Sourire parti, "
    "poitrine trop vite, papa accroupi. Il souffle, pause. Merci "
    "vécu. Pot trop vite, terre qui glisse. Il s'arrête, lit "
    "l'éclat. Un éclat de pot tient sur la terre."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(rambarde|comptoir|cubes|cube|tapis|plaid|rideau|paillasson|"
    r"pelle|coccinelle|linge|arrosoir|planche|abeille|feuille|"
    r"canapé|canape|lampe|toboggan|balançoire|balancoire|banc|"
    r"sable|seau|parc|portail|gouttière|gouttiere|cabane|thé|"
    r"tasse|plateau|cacao|dessin|livre|horloge|parquet|chaise|"
    r"tiroir|nappe|drap|ballon|entrée|entree|casserole|soupe|"
    r"carotte|chiffon|commode|gond|confiture|fraise|camion|"
    r"pupitre|gourde|flaque|piquet|rotin|crochet|platane|cageot|"
    r"résine|resine|botte|bottes|limace|perron|fraisier|cuivre|"
    r"buis|cerceau|grille|cour|pierre|figue|robinet|émail|email|"
    r"samare|bassine|lunettes|corde|sauge|lacet|farine|pâte|pate|"
    r"saladier|coussin|thym|zinc|tour)\b",
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
    "tu peux souffler",
    "tu peux faire une pause",
    "on peut souffler",
    "on peut faire une pause",
    "tu as soufflé",
    "tu as souffle",
    "tu as fait une pause",
    "souffler, puis une pause",
    "souffler puis une pause",
    "ton corps ralentit",
    "j'ai soufflé",
    "j'ai souffle",
    "j'ai fait une pause",
    "c'est bien",
    "c est bien",
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
    "éclat de tour",
    "éclat de comptoir",
    "éclat de pelle",
    "éclat de paillasson",
    "éclat de plaid",
    "éclat de cubes",
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
        emphasis="éclat de pot",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis gêne; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_chateau_maintenant; "
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
            "sous_texte=le_corps_va_vite_que_fait_il; "
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
            "destinataire=enfant; sous_texte=il_souffle_il_fait_une_pause; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de pot",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=pot_trop_vite_terre_glisse_il_souffle; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de pot",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_terre; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "souffler",
    "accepted_examples": (
        "souffler | pause | une pause | s'asseoir | respirer"
    ),
    "retry_prompt": "Papa dit de souffler. Que fait Victorino ensuite ?",
    "engine_ok_text": "Oui, souffler.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "jardin,terre",
        [
            "narrateur|Les pots tièdes font une ombre étroite.",
            "narrateur|Ça sent la terre chaude, un peu.",
            "enfant-m|Ça sent bon, papa.",
            "papa|Tu la sens, la terre, Victorino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Un rayon glisse sur un bord fêlé.",
            "enfant-m|Il brille, maman.",
            "maman|Le pot est chaud ?",
            "enfant-m|Un peu, maman.",
            "maman|Le château va commencer.",
            "maman|La terre et les pots, d'accord ?",
            "enfant-m|Oui, maman.",
            "narrateur|Une fourmi avance le long du bord.",
            "enfant-m|Elle marche, papa.",
            "papa|Tu la vois, la fourmi ?",
            "enfant-m|Oui.",
            "narrateur|La terre est sèche contre la peau.",
            "enfant-m|Elle pique, maman.",
            "maman|Tu la sens, la terre ?",
            "enfant-m|Oui.",
            "narrateur|Près du bord, un éclat de pot brille.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|Une poussière danse au-dessus des pots.",
            "enfant-m|Elle vole, maman.",
            "maman|Au-dessus du bord ?",
            "enfant-m|Oui, au-dessus.",
            "narrateur|Papa pose les mains près de la terre.",
            "narrateur|La terre est un peu lourde.",
            "enfant-m|On fait le château, papa ?",
            "narrateur|Papa prend un peu de terre.",
            "narrateur|Un mur tombe un peu.",
            "enfant-m|C'est marron, papa.",
            "papa|Comme une maison ?",
            "enfant-m|Oui, comme une maison.",
            "narrateur|En ce moment, Victorino tire la terre vers les pots.",
            "enfant-m|Je veux le château, maintenant !",
            "enfant-m|Le château, tout de suite.",
            "papa|Tu vois la terre, Victorino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Victorino ouvre les mains trop vite.",
            "narrateur|Il presse la terre trop fort.",
            "narrateur|Les murs collent trop près.",
            "enfant-m|Oh.",
            "narrateur|Le sourire de Victorino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Sa poitrine va trop vite.",
            "papa|Ça tombe, Victorino ?",
            "enfant-m|Oui, papa.",
            "maman|Tes lèvres sont serrées, Victorino ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de pot tremble, puis tient.",
            "narrateur|Le château s'effondre en tas.",
            "enfant-m|C'est trop, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Victorino regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Le corps de Victorino va vite.",
            "narrateur|Que fait-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "jardin",
        [
            "narrateur|Victorino veut le château, tout de suite.",
            "enfant-m|Je le fais, maintenant !",
            "narrateur|Il avance trop vite vers la terre.",
            "narrateur|Les murs se referment, trop hauts.",
            "narrateur|Victorino baisse les yeux.",
            "narrateur|Sa poitrine est coincée.",
            "enfant-m|C'est trop.",
            "narrateur|Victorino s'assoit près des pots.",
            "narrateur|Victorino souffle, un filet d'air.",
            "narrateur|Il reste un moment, sans bouger.",
            "narrateur|Il fait une pause.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe les pots, un instant.",
            "narrateur|Il écoute le silence du jardin.",
            "papa|Tu veux le château avec la terre ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Papa, on fait quoi ?",
            "papa|Tu veux t'asseoir un peu ?",
            "enfant-m|D'accord.",
            "narrateur|Victorino reste un moment, les mains ouvertes.",
            "narrateur|Il souffle, plus long.",
            "narrateur|La terre s'affaisse, puis tient.",
            "papa|Merci, Victorino.",
            "narrateur|Papa a vu le geste, au jardin.",
            "maman|La terre est tiède, sous les doigts.",
            "enfant-m|Elle est chaude.",
            "narrateur|Le mur tient, un peu de travers.",
            "enfant-m|Le château.",
            "papa|Il a un toit, là ?",
            "enfant-m|Oui, là.",
            "narrateur|Victorino glisse la main près du pot.",
            "narrateur|La terre est douce, contre la peau.",
            "maman|Tes mains sont au chaud, Victorino ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Papa pose un peu de terre.",
            "enfant-m|On le pose au bord ?",
            "maman|Le château va jusqu'aux pots.",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "jardin,terre",
        [
            "narrateur|Ils restent près des pots.",
            "narrateur|La terre tombe d'un côté.",
            "enfant-m|Le toit, maintenant !",
            "narrateur|Victorino presse la terre trop vite.",
            "narrateur|Un pot penche vers le château.",
            "enfant-m|Ça glisse !",
            "narrateur|La terre cache un bout du mur.",
            "narrateur|Victorino avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Il souffle, cette fois.",
            "narrateur|Il fait une pause, plus longue.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le bord, un instant.",
            "narrateur|Il écoute le silence du jardin.",
            "narrateur|Au bord du pot, un éclat de pot luit.",
            "enfant-m|Là, sur le pot.",
            "enfant-m|Tu veux le château, papa ?",
            "narrateur|Papa ne presse plus.",
            "narrateur|Il tend les mains, sans presser.",
            "papa|Je veux le château.",
            "narrateur|Victorino pousse la terre, sans se presser.",
            "narrateur|Papa la reçoit, plus loin.",
            "narrateur|La terre est lisse et tiède.",
            "papa|Tu le vois, le mur ?",
            "enfant-m|Oui, papa.",
            "maman|Le château est près des pots ?",
            "enfant-m|Oui, maman.",
            "narrateur|Papa pose un bord de terre.",
            "narrateur|Victorino pose une main sur le pot.",
            "papa|Le mur tient, Victorino ?",
            "enfant-m|Oui, papa.",
            "maman|Un rayon passe sur le pot.",
            "enfant-m|Il allume la terre.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près des pots.",
            "maman|Le château est arrivé, Victorino ?",
            "enfant-m|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-m|Oui, papa.",
            "narrateur|Victorino souffle, un filet d'air.",
            "enfant-m|La terre sent le basilic.",
            "maman|Tu la sens, la terre ?",
            "enfant-m|Oui, maman.",
            "papa|Le mur reste un peu, de travers.",
            "enfant-m|Il a tenu, près des pots.",
            "papa|Le château.",
            "narrateur|Le pot est chaud, sous les mains.",
            "narrateur|L'ombre des pots fait un abri.",
            "enfant-m|On y retourne, après.",
            "narrateur|Un éclat de pot tient sur la terre.",
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
    if "poitrine" not in blob:
        raise SystemExit(f"{SID}: manque poitrine")
    if "accroupit" not in blob:
        raise SystemExit(f"{SID}: manque accroupit")
    if "sourire" not in blob:
        raise SystemExit(f"{SID}: manque sourire")
    if "s'effondre" not in blob and "seffondre" not in blob.replace("'", ""):
        raise SystemExit(f"{SID}: manque s'effondre")
    if "trop vite" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: manque 2e ruse (trop vite)")
    if "penche" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: manque 2e ruse (pot penche)")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Victorino = enfant-m)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain")
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
        "tu peux souffler",
        "tu peux faire une pause",
        "on peut souffler",
        "on peut faire une pause",
        "tu as soufflé",
        "tu as fait une pause",
        "souffler, puis une pause",
        "souffler puis une pause",
        "bravo",
        "ton corps ralentit",
        "j'ai soufflé",
        "j'ai fait une pause",
        "c'est bien",
        "tu as repris",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Le corps de Victorino va vite. Que fait-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "souffler":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "souffler | pause | une pause | s'asseoir | respirer"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Papa dit de souffler. Que fait Victorino ensuite ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    if "château" not in blob and "chateau" not in blob:
        raise SystemExit(f"{SID}: manque château")
    if "jardin" not in blob:
        raise SystemExit(f"{SID}: manque jardin")
    if "pot" not in blob:
        raise SystemExit(f"{SID}: manque pot")
    if "maintenant" not in blob:
        raise SystemExit(f"{SID}: manque maintenant")
    for ban in (
        "éclat de tour",
        "éclat de comptoir",
        "éclat de rambarde",
        "rambarde",
        "comptoir",
        "tout doux",
        "tout calme",
        "william",
        "victorina",
        "zélie",
        "zelie",
        "lila",
        "sarah",
        "nino",
        "mila",
        "aniss",
        "raphaël",
        "raphael",
        "chouchou",
        "amir",
        "nina",
        "linge",
        "arrosoir",
        "planche",
        "paillasson",
        "pelle",
        "coccinelle",
        "cubes",
        "tapis",
        "plaid",
        "rideau",
        "farine",
        "pâte",
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
        "- **Public :** N2 (≤15 mots/phrase), audio familial\n"
        "- **Leçon :** EMO.GES.002 — corps trop vite → souffler, pause "
        "(vécue : Victorino veut le château **maintenant**, s'effondre, "
        "poitrine trop vite, sourire parti, papa accroupi ; il souffle, "
        "pause ; 2e ruse pot trop vite). JAMAIS dite dans le récit. Pas "
        "« tu peux souffler ». Pas « tu peux faire une pause ». Pas "
        "« bravo, tu as soufflé ».\n"
        "- **Personnages :** Victorino, papa, maman. Dump William/papa "
        "→ D16 Victorino (héros enfant-m) + papa/maman. Troupe D16. Pas "
        "de maîtresse. Pas de copain.\n"
        "- **Lieu :** jardin, château de terre, pots, terre, bord, "
        "soleil, ombre, poussière, fourmi, basilic. ≠ 002-01 tour / "
        "cubes. ≠ 002-02 comptoir / pain. ≠ PAR.001-07 rambarde / "
        "paillasson / pelle. ≠ dump arrosoir / linge / planche.\n"
        "- **Indice unique :** éclat de pot (brille à l'ouverture près "
        "du bord fêlé → tremble à l'effondrement → luit au refus du "
        "second tas → tient sur la terre). BAN éclat de tour / "
        "comptoir / rambarde.\n"
        "- **Question moteur :** « Le corps de Victorino va vite. Que "
        "fait-il ? » expected dump **souffler**. accepted dump "
        "`souffler | pause | une pause | s'asseoir | respirer`. retry "
        "dump (William → Victorino). expected/accepted/retry des autres "
        "chunks restent **null**. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Les pots tièdes font une ombre étroite. Près du bord, un "
        "éclat de pot brille. Fourmi, basilic, poussière, terre chaude. "
        "Victorino veut le château **maintenant**. Il presse trop vite. "
        "Le château s'effondre. Sourire parti. Papa s'accroupit. Il "
        "souffle, fait une pause. Merci vécu. Deuxième ruse : toit trop "
        "vite, pot qui penche, terre qui glisse. Il s'arrête, lit "
        "l'éclat. Un éclat de pot tient sur la terre.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin, pots, terre, bord fêlé, soleil, ombre, "
        "fourmi, basilic. ≠ dump arrosoir / linge / planche. ≠ "
        "rambarde / pelle / paillasson.\n"
        "- Désir : le château de terre, maintenant.\n"
        "- Objet : pots, terre, château, bord.\n"
        "- Indice unique : éclat de pot, vu dès l'ouverture près du "
        "bord, payé sur la terre. Pas éclat de tour / comptoir / "
        "rambarde.\n"
        "- Urgence douce : Victorino accélère, presse trop.\n"
        "- Imprévu 1 : château trop vite, s'effondre. Poitrine trop "
        "vite, sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : toit trop vite, pot penche, terre "
        "glisse.\n"
        "- Résolution : il s'assoit, souffle, fait une pause, observe, "
        "écoute, retrouve l'éclat, reprend sans presser.\n"
        "- Retour : mur de travers, basilic, éclat sur la terre.\n\n"
        "## Vécu\n\n"
        "Victorino veut le château **maintenant**. Impatience, puis "
        "effondrement, sourire parti. Papa se baisse, pose une "
        "question, ne récite pas la règle. Victorino agit : souffler, "
        "pause. Merci vécu. Fin : l'éclat du début tient sur la terre.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Victorino souffle au jardin (noyau + D16). Relance : "
        "Que fait-il ? expected souffler.\n"
        "- Lieu du dump (jardin, château, pots) sans arrosoir / linge / "
        "planche / rambarde. Papa et maman présents. Victorino = "
        "enfant-m.\n"
        "- Ouverture inventée (pots tièdes, ombre étroite), pas un "
        "gabarit v2, pas « L'arrosoir penche encore » du dump en "
        "première ligne.\n"
        "- Indice unique : éclat de pot. BAN éclat de tour / comptoir / "
        "rambarde. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip dump « tout doux » / « bravo » / « tu peux "
        "souffler ». Une phrase par ligne, ponctuation, pas de puces.\n"
        "- Leçon non dite : on la voit quand Victorino souffle, s'assoit, "
        "fait une pause. Pas « tu peux souffler ». Pas « tu as fait "
        "une pause ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Le corps de Victorino va vite. Que "
        "fait-il ? ». expected souffler. retry dump (Victorino). 5 "
        "chunks, kinds inchangés. expected/accepted/retry null hors Q.\n"
        "- example4 048 / 080 / 012 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_001_04.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le pot.\n"
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
