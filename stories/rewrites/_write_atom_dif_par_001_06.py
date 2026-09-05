#!/usr/bin/env python3
"""ATOM-DIF.PAR.001-06 — Le puzzle sous la pluie (F-NAR-019, N2, DIF.PAR.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.001-06"
TITLE = "Le puzzle sous la pluie"
N2 = LIMITS["N2"]
CHARS = "Victorino, Sarah, papa, maman"
SETTING = (
    "chambre, jour de pluie, gouttière, zinc, carreau mouillé, "
    "ours en tissu, puzzle, tapis beige"
)
INDICE = "éclat de zinc"
FIL = (
    "La gouttière chante sur le zinc. Sous la gouttière, un "
    "éclat de zinc brille. Victorino veut le puzzle, maintenant. "
    "Sarah ne dit rien. Pièce trop vite. Sourire parti, adulte "
    "accroupi. Il refuse de foncer, tend, attend. Merci vécu. "
    "Pièce du ciel, goutte sur le tapis. Un éclat de zinc tient "
    "sous la gouttière."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(flaque|piquet|portail|rotin|crochet|platane|cageot|résine|"
    r"resine|botte|bottes|limace|perron|chaise|tiroir|fraisier|"
    r"cuivre|buis|cerceau|grille|cour|pierre|nappe|figue|robinet|"
    r"planche|émail|email|samare|bassine|lunettes|corde|drap|"
    r"ballon|horloge|bol|casserole|soupe|carotte|"
    r"chiffon|sauge|lacet|commode|gond|banc|coussin|confiture|"
    r"tartine|fraise|romarin|parquet|wagon|locomotive|gare|quai|"
    r"rail|craie|cartable|classe|école|ecole|maîtresse|maitresse|"
    r"merle|miel)\b",
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
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de carreau",
    "éclat de romarin",
    "éclat de table",
    "éclat de rond",
    "éclat de banc",
    "éclat de parquet",
    "éclat de tapis",
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
    "éclat de vapeur",
    "éclat de bol",
    "éclat de chiffon",
    "éclat de sauge",
    "éclat de lacet",
    "éclat de commode",
    "éclat de gond",
    "éclat d'horloge",
    "éclat d horloge",
    "éclat d'ours",
    "éclat de ours",
    "éclat de puzzle",
    "éclat d'oreiller",
    "éclat de oreiller",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
    "tapent, tapent, tapent",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de zinc",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_puzzle_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Sarah",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=sarah_parle_peu_que_fait_victorino; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="puzzle",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_refuse_de_foncer_attend_tend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de zinc",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=piece_du_ciel_goutte_il_s_arrete; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de zinc",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sous_la_gouttiere; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "attendre",
    "accepted_examples": (
        "attendre | tendre un jouet | un jouet | elle attend"
    ),
    "retry_prompt": "Il tend un jouet. Il attend. Que fait Victorino ?",
    "engine_ok_text": "Oui, attendre.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "pluie",
        [
            "narrateur|La gouttière chante sur le zinc.",
            "narrateur|Ça fait un bruit mince, un peu froid.",
            "enfant-m|J'ai entendu le zinc, papa.",
            "papa|La gouttière, Victorino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Sous la gouttière, un éclat de zinc brille.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|Le carreau est mouillé, du bord jusqu'en bas.",
            "enfant-m|Une goutte glisse, papa.",
            "papa|Sur le carreau ?",
            "enfant-m|Oui.",
            "narrateur|Un ours en tissu dort sur l'oreiller.",
            "enfant-m|Il a un œil en bouton.",
            "maman|Il garde le lit, Victorino ?",
            "enfant-m|Oui, maman.",
            "narrateur|Maman ouvre la boîte du puzzle.",
            "narrateur|Le carton sent le papier, un peu.",
            "enfant-m|Je veux le puzzle, maintenant !",
            "enfant-m|Les animaux, tout de suite.",
            "papa|Le puzzle sur le tapis ?",
            "enfant-m|Oui.",
            "enfant-m|Avec le chat.",
            "narrateur|En ce moment, Victorino est sur le tapis.",
            "narrateur|Le tapis est beige, un peu rêche.",
            "narrateur|Une pièce du chat attend près de lui.",
            "enfant-m|Elle est lisse, papa.",
            "papa|Tu la tiens, Victorino ?",
            "enfant-m|Oui, papa.",
            "narrateur|La porte s'ouvre.",
            "narrateur|Sarah arrive avec son sac.",
            "narrateur|Le sac est mouillé sur le bord.",
            "enfant-m|Tu poses le chat avec moi ?",
            "narrateur|Une goutte tombe sur le tapis.",
            "narrateur|Sarah regarde le sol.",
            "narrateur|Elle ne dit rien.",
            "narrateur|Victorino a envie de tout dire.",
            "enfant-m|Le zinc !",
            "enfant-m|L'ours !",
            "enfant-m|Le puzzle !",
            "narrateur|Victorino pousse trop vite vers elle.",
            "narrateur|La pièce tape la boîte.",
            "enfant-m|Oh.",
            "narrateur|Le sourire de Victorino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Sarah, Victorino ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains tiennent la pièce, Victorino ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de zinc tremble, puis tient.",
            "narrateur|Sarah reste près du sac.",
            "enfant-m|Elle ne dit rien, papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Sarah parle peu.",
            "narrateur|Que fait Victorino ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "pluie",
        [
            "narrateur|Victorino veut le puzzle, tout de suite.",
            "enfant-m|Je la pose, maintenant !",
            "narrateur|Il avance trop vite vers Sarah.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "narrateur|Sarah baisse les yeux.",
            "narrateur|Elle serre le sac contre elle.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Victorino refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe la pièce, un instant.",
            "narrateur|Il écoute la gouttière sur le zinc.",
            "papa|Tu veux le puzzle avec Sarah ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Papa, on fait quoi ?",
            "papa|On pose la pièce, puis on reste.",
            "enfant-m|D'accord.",
            "narrateur|Victorino reste un moment, les mains ouvertes.",
            "narrateur|Il attend.",
            "narrateur|Il tend la pièce du chat.",
            "enfant-m|Pour toi.",
            "narrateur|Sarah ne dit rien.",
            "narrateur|Elle prend la pièce, sans parler.",
            "copine|Oui.",
            "narrateur|Victorino pose les mains sur le tapis.",
            "narrateur|Il reste, sans se presser.",
            "narrateur|Sarah pose le chat, plus lentement.",
            "papa|Merci, Victorino.",
            "narrateur|Papa a vu les deux, dans la chambre.",
            "maman|Le carton est tiède, sous les doigts.",
            "enfant-m|Il est chaud.",
            "narrateur|Le chat tient, un peu de travers.",
            "enfant-m|Le chat.",
            "papa|Il a une oreille, là ?",
            "enfant-m|Oui, là.",
            "narrateur|Victorino glisse le doigt sur le carton.",
            "narrateur|Le papier est doux, contre la peau.",
            "maman|Tes mains sont au chaud, Victorino ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Sarah s'assoit, puis se relève.",
            "copine|Chat.",
            "enfant-m|On va jusqu'au bord ?",
            "maman|Le tapis beige va jusqu'au mur.",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pluie",
        [
            "narrateur|Ils restent sur le tapis beige.",
            "narrateur|Une pièce du ciel manque, au milieu.",
            "enfant-m|Je la mets, maintenant !",
            "narrateur|Victorino pousse trop vite.",
            "narrateur|La pièce glisse vers la goutte.",
            "enfant-m|Ça tombe !",
            "narrateur|Sarah tend les mains, sans parler.",
            "narrateur|Victorino avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Victorino refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe la pièce, un instant.",
            "narrateur|Il écoute la gouttière, sur le zinc.",
            "narrateur|Près du carreau, un éclat de zinc luit.",
            "enfant-m|Là, sur le zinc.",
            "enfant-m|Tu prends le ciel, Sarah ?",
            "narrateur|Sarah ne dit rien.",
            "narrateur|Elle tend les mains, sans parler.",
            "copine|Oui.",
            "narrateur|Victorino passe la pièce, sans se presser.",
            "narrateur|Sarah la pose, plus lentement.",
            "narrateur|Le carton est lisse et un peu froid.",
            "papa|Tu le vois, le ciel ?",
            "enfant-m|Oui, papa.",
            "maman|Le tapis beige est près du mur ?",
            "enfant-m|Oui, maman.",
            "narrateur|La pièce entre dans le trou.",
            "narrateur|Victorino pose une main sur le carton.",
            "narrateur|Sarah pose la suivante.",
            "papa|Le puzzle tient, Victorino ?",
            "enfant-m|Oui, papa.",
            "maman|Une goutte passe sur le carreau.",
            "enfant-m|Elle allume le zinc.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du tapis.",
            "maman|Le puzzle est arrivé, Victorino ?",
            "enfant-m|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-m|Oui, papa.",
            "narrateur|Victorino souffle, un filet d'air.",
            "enfant-m|Le carton sent le papier.",
            "maman|Tu le sens, le puzzle ?",
            "enfant-m|Oui, maman.",
            "papa|Le chat reste un peu, de travers.",
            "enfant-m|Il a tenu, sur le tapis.",
            "copine|Chat.",
            "narrateur|Le tapis est tiède, sous les mains.",
            "narrateur|L'ours regarde depuis l'oreiller.",
            "enfant-m|On y retourne, après.",
            "narrateur|Un éclat de zinc tient sous la gouttière.",
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
    if "tend la pièce" not in blob and "tend la piece" not in blob:
        raise SystemExit(f"{SID}: manque tend la pièce")
    if "il attend." not in blob:
        raise SystemExit(f"{SID}: manque il attend")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Victorino = enfant-m, Sarah = copine)")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Sarah absente (copine)")
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
        "ce n'est pas une faute",
        "n'est pas une faute",
        "on peut jouer",
        "on peut attendre",
        "on peut demander",
        "on joue",
        "vous jouez",
        "il faut attendre",
        "on doit demander",
        "il faut demander",
        "parle peu",
        "elle parle peu",
        "forcer la parole",
        "tu as su attendre",
        "tendre un jouet",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Sarah parle peu. Que fait Victorino ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "attendre | tendre un jouet | un jouet | elle attend"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Il tend un jouet. Il attend. Que fait Victorino ?":
        raise SystemExit(f"{SID}: retry dump altéré: {retry}")
    copine_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    ).lower()
    if "chat" not in copine_txt:
        raise SystemExit(f"{SID}: Sarah sans chat")
    n_copine = sum(
        1
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    )
    if n_copine > 5:
        raise SystemExit(f"{SID}: Sarah parle trop ({n_copine})")
    if "puzzle" not in blob:
        raise SystemExit(f"{SID}: manque puzzle")
    if "gouttière" not in blob and "gouttiere" not in blob:
        raise SystemExit(f"{SID}: manque gouttière")
    if "zinc" not in blob:
        raise SystemExit(f"{SID}: manque zinc")
    if "carreau" not in blob:
        raise SystemExit(f"{SID}: manque carreau")
    if "ours" not in blob:
        raise SystemExit(f"{SID}: manque ours")
    if "tapis" not in blob:
        raise SystemExit(f"{SID}: manque tapis")
    if "ne dit rien" not in blob:
        raise SystemExit(f"{SID}: manque silence vécu")
    if "s'accroupit" not in blob and "s accroupit" not in blob:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    for ban in (
        "éclat de gouttière",
        "éclat de gouttiere",
        "éclat de carreau",
        "éclat de romarin",
        "éclat de table",
        "éclat de rond",
        "éclat de banc",
        "éclat de parquet",
        "éclat de tapis",
        "tout doux",
        "tout calme",
        "aline",
        "denis",
        "bon travail",
        "aujourd'hui",
        "miel",
        "merle",
        "tapent, tapent, tapent",
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
        "- **Leçon :** DIF.PAR.001 — quand l'autre parle peu, on attend, "
        "on tend le jouet (vécue : pièce trop vite, sourire parti, il "
        "refuse de foncer, attend, tend la pièce du chat, Sarah prend "
        "sans parler). JAMAIS dite dans le récit. Pas « il faut attendre ». "
        "Pas « elle parle peu » hors question moteur.\n"
        "- **Personnages :** Victorino, Sarah, papa, maman. Dump Aline/"
        "Denis → D16. Victorino = enfant-m (veut le puzzle maintenant, "
        "trop vite, puis refuse de foncer). Sarah = copine (parle peu, "
        "regarde le sol, oui, chat). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** chambre, jour de pluie, gouttière, zinc, carreau "
        "mouillé, ours en tissu, puzzle, tapis beige. ≠ PAR.001-04 "
        "puzzle école / bateau / classe. ≠ dump gare / rails / wagon.\n"
        "- **Indice unique :** éclat de zinc (brille à l'ouverture sous "
        "la gouttière → tremble à la pièce trop vite → luit près du "
        "carreau → tient sous la gouttière). BAN éclat de gouttière / "
        "carreau (BAN) + romarin / table / rond / banc / parquet.\n"
        "- **Question moteur :** « Sarah parle peu. Que fait "
        "Victorino ? » expected **attendre**. accepted `attendre | "
        "tendre un jouet | un jouet | elle attend` (dump, même si "
        "« elle »). retry dump. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La gouttière chante sur le zinc. Sous la gouttière, un éclat "
        "de zinc brille. Carreau mouillé, ours en tissu, boîte du "
        "puzzle. Victorino veut le puzzle **maintenant**. Sarah arrive, "
        "ne dit rien. Il pousse trop vite, la pièce tape la boîte. "
        "Sourire parti. Papa s'accroupit. Il refuse de foncer. Il "
        "attend, tend la pièce du chat. Merci vécu. Deuxième ruse : "
        "pièce du ciel, goutte sur le tapis. Il s'arrête, lit l'éclat. "
        "Un éclat de zinc tient sous la gouttière.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chambre, jour de pluie, gouttière sur le zinc, "
        "carreau mouillé, ours en tissu, puzzle, tapis beige.\n"
        "- Désir : le puzzle d'animaux, maintenant, sur le tapis.\n"
        "- Objet : puzzle, pièce du chat, pièce du ciel, sac mouillé, "
        "ours en tissu.\n"
        "- Indice unique : éclat de zinc, vu dès l'ouverture sous la "
        "gouttière, payé sous la gouttière. Pas éclat de gouttière / "
        "carreau / romarin / table / rond / banc / parquet.\n"
        "- Urgence douce : Sarah arrive, Victorino accélère les mots.\n"
        "- Imprévu 1 : il pousse trop vite, la pièce tape la boîte. "
        "Sarah ne dit rien.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : pièce du ciel, elle glisse vers la "
        "goutte du sac, sur le tapis.\n"
        "- Résolution : il refuse de foncer, observe, écoute la "
        "gouttière, retrouve l'éclat, tend, Sarah reçoit.\n"
        "- Retour : chat de travers, ours sur l'oreiller, éclat sous "
        "la gouttière.\n\n"
        "## Vécu\n\n"
        "Victorino veut le puzzle **maintenant**. Impatience, puis "
        "pièce trop vite, sourire parti. Sarah pose sa limite (yeux "
        "bas, silence, oui, chat). Papa se baisse, pose une question, "
        "ne récite pas la règle. Ils agissent : attendre, tendre la "
        "pièce, poser sans se presser. Merci vécu. Fin : l'éclat du "
        "début tient sous la gouttière.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le puzzle sous la pluie (noyau mission, dump Aline/"
        "Denis puzzle sous la pluie). Relance : Que fait Victorino ? "
        "expected attendre.\n"
        "- Lieu : chambre, jour de pluie (gouttière, zinc, carreau, "
        "ours, puzzle). Maman et papa. Victorino = enfant-m. Sarah = "
        "copine. Aline/Denis dump-meta retirés. Pas de maîtresse. ≠ "
        "PAR.001-04 puzzle école.\n"
        "- Ouverture inventée (gouttière qui chante sur le zinc), pas "
        "un gabarit v2, pas « Les gouttes tapent, tapent, tapent » du "
        "dump, pas la gare / locomotive.\n"
        "- Indice unique : éclat de zinc (gouttière sur le zinc à "
        "l'ouverture, payé). BAN éclat de gouttière / carreau + "
        "romarin / table / rond / banc / parquet. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tapent, tapent, tapent » / « encore » / "
        "« on peut attendre » du dump.\n"
        "- Leçon non dite : on la voit quand la pièce tape, quand il "
        "refuse de foncer, quand il attend, quand il tend, quand Sarah "
        "prend sans parler. Pas « il faut attendre ». Pas « elle parle "
        "peu » hors question. Pas « on peut attendre » hors retry "
        "label.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Sarah parle peu. Que fait "
        "Victorino ? ». expected attendre. accepted dump (elle attend). "
        "retry dump. 5 chunks, kinds inchangés.\n"
        "- example4 029 / 061 / 093 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_ene_001_06.py` / "
        "`_write_atom_dif_ene_001_07.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers la pièce du ciel.\n"
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
