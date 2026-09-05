#!/usr/bin/env python3
"""ATOM-DIF.ENE.001-06 — La file du cerceau (F-NAR-019, N3, DIF.ENE.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.ENE.001-06"
TITLE = "La file du cerceau"
N3 = LIMITS["N3"]
CHARS = "Amir, Chouchou, papa, maman"
SETTING = (
    "cour d'école puis jardin, ombre d'arbre, cloche lointaine, "
    "cerceau rouge dans l'herbe, lacet, gourde, file"
)
INDICE = "éclat de lacet"
FIL = (
    "Le lacet glisse. Papa noue. Sur le nœud, un éclat de lacet "
    "brille. Cloche lointaine, ombre, cerceau rouge dans l'herbe. "
    "Amir veut la file, maintenant. Chouchou saute trop. Le cerceau "
    "part. Sourire parti. Il refuse de foncer. Merci vécu. Racine, "
    "elle veut passer. Il s'arrête, lit l'éclat. Un éclat de lacet "
    "tient sur le nœud."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(flaque|piquet|bol|chiffon|sauge|miel|merle|"
    r"craie|poussière|poussiere|botte|bottes|limace|perron|"
    r"tiroir|fraisier|cuivre|buis|coussin|figue|robinet|"
    r"planche|émail|email|samare|bassine|résine|resine|"
    r"maîtresse|maitresse|lunettes|drap|pinceau|carotte|"
    r"entrée|entree|portail|rotin|crochet|platane|cageot|"
    r"baptiste|noa)\b",
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
    "ce n'est pas une faute",
    "ce n est pas une faute",
    "pas une faute",
    "on peut jouer",
    "on peut attendre",
    "on peut demander",
    "demander à un adulte",
    "demander a un adulte",
    "beaucoup d'énergie",
    "beaucoup d'energie",
    "beaucoup d energie",
    "c'est son énergie",
    "c'est son energie",
    "vous jouez",
    "on joue",
    "chacun son tour",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de cerceau",
    "éclat de cour",
    "éclat de cloche",
    "éclat de poussière",
    "éclat de poussiere",
    "éclat de craie",
    "éclat de flaque",
    "éclat de piquet",
    "éclat de bol",
    "éclat de chiffon",
    "éclat de sauge",
    "éclat de grille",
    "éclat de botte",
    "éclat de pierre",
    "éclat de plaque",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de tiroir",
    "éclat de fraisier",
    "éclat de chaise",
    "éclat de perron",
    "éclat de limace",
    "éclat de résine",
    "éclat de resine",
    "éclat de cageot",
    "éclat de platane",
    "éclat de crochet",
    "éclat de rotin",
    "éclat de portail",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de pin",
    "éclat de casserole",
    "éclat de citron",
    "éclat de coquille",
    "éclat de zeste",
    "éclat de coussin",
    "éclat de figue",
    "éclat de robinet",
    "éclat de planche",
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
    "éclat de dalle",
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
    "éclat de gourde",
    "éclat d'herbe",
    "éclat de herbe",
    "éclat d'arbre",
    "éclat de arbre",
    "éclat de nœud",
    "éclat de noeud",
    "éclat de file",
    "éclat de racine",
    "éclat de tronc",
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
        emphasis="éclat de lacet",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_file_du_cerceau_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="énergie",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=chouchou_a_de_l_energie_que_peut_on_faire; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="cerceau",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_refuse_reste_dans_la_file_avec_elle; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de lacet",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_racine_elle_souffle; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de lacet",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_noeud; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer",
    "accepted_examples": "jouer | attendre | un adulte | demander",
    "retry_prompt": (
        "On peut jouer, attendre, ou demander à un adulte. Que fait Amir ?"
    ),
    "engine_ok_text": "Oui, jouer.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc",
        [
            "narrateur|Le lacet glisse entre les doigts de papa.",
            "narrateur|Le bout plastique fait clic, sec et petit.",
            "enfant-m|Ça a fait clic !",
            "papa|Ton lacet, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa noue le nœud, un peu serré.",
            "narrateur|Sur le nœud, un éclat de lacet brille.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, sur le nœud ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|La cour sent l'herbe chaude, un peu.",
            "enfant-m|Ça sent l'herbe, maman.",
            "maman|Tes chaussures tiennent, Amir ?",
            "enfant-m|Oui, maman.",
            "narrateur|Une cloche lointaine fait ding, loin dans l'air.",
            "enfant-m|J'ai entendu le ding.",
            "papa|La cloche, Amir ?",
            "enfant-m|Oui, loin.",
            "narrateur|L'ombre de l'arbre est longue, sur la cour.",
            "narrateur|Maman glisse une gourde dans le sac.",
            "maman|L'eau est fraîche.",
            "enfant-m|Elle est froide, maman.",
            "narrateur|Ils passent de la cour au jardin.",
            "narrateur|L'herbe est haute, un peu sèche.",
            "enfant-m|Je veux le cerceau, maintenant !",
            "papa|Le cerceau dans l'herbe ?",
            "enfant-m|Oui, tout de suite.",
            "maman|Jusqu'à l'arbre ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un cerceau rouge repose dans l'herbe.",
            "narrateur|Le plastique est tiède, un peu rêche.",
            "enfant-m|Il est chaud, papa.",
            "papa|Tu le tiens, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|En ce moment, Amir tient le cerceau.",
            "narrateur|Ils font une file vers l'arbre.",
            "enfant-m|Moi d'abord, maintenant !",
            "narrateur|Les chaussures tapent le sol, depuis la cour.",
            "narrateur|Chouchou arrive en sautant.",
            "copine|J'arrive !",
            "enfant-m|Chouchou !",
            "narrateur|Elle saute sur place, trop vite.",
            "copine|Le cerceau !",
            "enfant-m|Moi, le cerceau, maintenant !",
            "narrateur|Chouchou prend le cerceau rouge.",
            "narrateur|Elle le fait tourner trop vite.",
            "narrateur|Le cerceau part vers la gourde.",
            "enfant-m|Il part !",
            "copine|Oh.",
            "narrateur|Le cerceau tombe dans l'herbe.",
            "narrateur|Ça fait un bruit mou.",
            "enfant-m|Il est tombé !",
            "narrateur|L'éclat de lacet tremble, puis tient.",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Chouchou, Amir ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains sont chaudes, Amir ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Chouchou a de l'énergie.",
            "narrateur|Que peut-on faire ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "enfants_parc",
        [
            "narrateur|Amir veut le cerceau, tout de suite.",
            "enfant-m|Je le prends, maintenant !",
            "narrateur|Il avance trop vite vers Chouchou.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copine|Attends.",
            "narrateur|Chouchou saute, trop près de l'herbe.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Amir refuse de foncer.",
            "narrateur|Il referme les mains.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le cerceau, un instant.",
            "narrateur|Il écoute la cloche, loin dans l'air.",
            "papa|Tu veux le cerceau avec Chouchou ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Papa, on fait quoi ?",
            "papa|On reste dans la file ?",
            "enfant-m|Oui.",
            "maman|On marche jusqu'à l'arbre ?",
            "enfant-m|Oui, maman.",
            "papa|Viens, Chouchou.",
            "copine|J'y vais.",
            "narrateur|Ils restent dans la file, un moment.",
            "narrateur|L'herbe froisse, sous les chaussures.",
            "enfant-m|L'herbe, papa.",
            "papa|Tu poses les mains ?",
            "enfant-m|Oui.",
            "narrateur|Amir pose les mains sur le plastique.",
            "narrateur|Le cerceau est tiède.",
            "narrateur|Chouchou pose les mains aussi.",
            "copine|Il est chaud.",
            "narrateur|Elle souffle.",
            "papa|Merci, Amir.",
            "narrateur|Papa a vu les deux, dans l'herbe.",
            "maman|L'ombre de l'arbre a bougé, un peu.",
            "enfant-m|Elle est longue.",
            "narrateur|Chouchou pose le cerceau, sans se presser.",
            "copine|À toi.",
            "enfant-m|D'accord.",
            "narrateur|Amir fait rouler le cerceau.",
            "narrateur|Le cerceau passe dans l'herbe.",
            "enfant-m|Il roule !",
            "copine|Oui.",
            "papa|Tu le vois, le rond rouge ?",
            "enfant-m|Oui, papa.",
            "maman|Tes chaussures tiennent ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le ventre d'Amir se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près de l'arbre ?",
            "enfant-m|Oui.",
            "maman|Tes mains sont chaudes ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "enfants_parc",
        [
            "narrateur|Ils vont sous l'arbre, dans le jardin.",
            "enfant-m|Une file, maintenant !",
            "narrateur|L'ombre glisse sur l'herbe.",
            "narrateur|Chouchou veut passer, trop vite.",
            "narrateur|Elle saute vers le tronc.",
            "copine|Moi d'abord !",
            "narrateur|Le cerceau penche vers une racine.",
            "enfant-m|Ça tombe !",
            "narrateur|Amir avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Amir refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le cerceau, un instant.",
            "narrateur|Il écoute la cloche, loin dans l'air.",
            "narrateur|Sur le nœud, un éclat de lacet luit.",
            "enfant-m|Là, sur le nœud.",
            "enfant-m|Tu restes, Chouchou ?",
            "narrateur|Chouchou ne dit rien.",
            "narrateur|Elle souffle, sans parler.",
            "copine|Oui.",
            "narrateur|Elle reste derrière lui.",
            "enfant-m|Le cerceau, maman ?",
            "maman|Le rouge, Amir.",
            "narrateur|Amir pousse, sans se presser.",
            "narrateur|Le cerceau contourne la racine.",
            "copine|À moi.",
            "narrateur|Chouchou pousse à son tour.",
            "papa|Tu as soufflé, Chouchou ?",
            "copine|Un peu.",
            "maman|L'ombre est fraîche, Amir ?",
            "enfant-m|Un peu, maman.",
            "papa|Vous roulez ensemble ?",
            "enfant-m|Oui, papa.",
            "narrateur|Ils roulent le cerceau jusqu'au tronc.",
            "narrateur|Le plastique tape le bois, sans bruit.",
            "enfant-m|Il est arrivé.",
            "copine|Il est arrivé.",
            "maman|Le cerceau a de l'herbe, Amir ?",
            "enfant-m|Sur le bord.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de l'arbre.",
            "narrateur|Maman essuie un peu d'herbe.",
            "enfant-m|On a eu le cerceau, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, jusqu'au tronc.",
            "maman|On est bien, ici.",
            "narrateur|Amir tapote le plastique du doigt.",
            "enfant-m|Il a une trace d'herbe.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|Le cerceau est resté, Amir.",
            "enfant-m|Oui, avec Chouchou.",
            "copine|Le cerceau est resté.",
            "narrateur|Ça sent l'herbe, un peu tiède.",
            "enfant-m|Et le lacet, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|Les chaussures restent dans l'herbe.",
            "narrateur|Un éclat de lacet tient sur le nœud.",
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
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Amir = enfant-m, Chouchou = copine)")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Chouchou absente (copine)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain")
    if "enfant-m|" not in blob:
        raise SystemExit(f"{SID}: Amir absent (enfant-m)")
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
        "pas une faute",
        "on peut jouer",
        "on peut attendre",
        "on peut demander",
        "demander à un adulte",
        "beaucoup d'énergie",
        "beaucoup d'energie",
        "on joue",
        "vous jouez",
        "un adulte",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    if re.search(r"\bénergie\b", body) or re.search(r"\benergie\b", body):
        raise SystemExit(f"{SID}: énergie hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Chouchou a de l'énergie. Que peut-on faire ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != "jouer | attendre | un adulte | demander":
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "On peut jouer, attendre, ou demander à un adulte. Que fait Amir ?":
        raise SystemExit(f"{SID}: retry dump altéré: {retry}")
    copine_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    ).lower()
    if "attends" not in copine_txt:
        raise SystemExit(f"{SID}: Chouchou sans attends")
    if "souffle" not in blob:
        raise SystemExit(f"{SID}: manque souffle")
    if "cerceau" not in blob:
        raise SystemExit(f"{SID}: manque cerceau")
    if "lacet" not in blob:
        raise SystemExit(f"{SID}: manque lacet")
    if "file" not in blob:
        raise SystemExit(f"{SID}: manque file")
    if "herbe" not in blob:
        raise SystemExit(f"{SID}: manque herbe")
    if "cloche" not in blob:
        raise SystemExit(f"{SID}: manque cloche")
    if "gourde" not in blob:
        raise SystemExit(f"{SID}: manque gourde")
    if "jardin" not in blob:
        raise SystemExit(f"{SID}: manque jardin")
    if "cour" not in blob:
        raise SystemExit(f"{SID}: manque cour")
    if "papa noue" not in blob:
        raise SystemExit(f"{SID}: papa ne noue pas à l'ouverture")
    for ban in (
        "éclat de cerceau",
        "éclat de cour",
        "éclat de cloche",
        "éclat de poussière",
        "éclat de poussiere",
        "éclat de craie",
        "éclat de flaque",
        "éclat de piquet",
        "éclat de bol",
        "éclat de chiffon",
        "éclat de sauge",
        "tout doux",
        "tout calme",
        "baptiste",
        "noa",
        "maîtresse",
        "maitresse",
        "bon travail",
        "aujourd'hui",
        "miel",
        "merle",
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
        "- **Leçon :** DIF.ENE.001 — beaucoup d'énergie n'est pas une faute ; "
        "on peut jouer, attendre, ou demander à un adulte (vécue : file, "
        "cerceau qui part, sourire parti, racine, souffle). JAMAIS dite "
        "dans le récit.\n"
        "- **Personnages :** Amir, Chouchou, papa, maman. Dump Baptiste/"
        "Noa → D16. Amir = enfant-m (veut le cerceau maintenant). "
        "Chouchou = copine (saute, trop vite, attends, souffle). "
        "Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** cour d'école puis jardin, ombre d'arbre, cloche "
        "lointaine, cerceau rouge dans l'herbe, lacet, gourde, file. "
        "Monde xlsx.\n"
        "- **Indice unique :** éclat de lacet (brille sur le nœud à "
        "l'ouverture, papa noue → tremble quand le cerceau part → luit "
        "à la racine → tient sur le nœud). BAN éclat de cerceau / cour / "
        "cloche / poussière / craie + flaque / piquet / bol / chiffon / "
        "sauge.\n"
        "- **Question moteur :** « Chouchou a de l'énergie. Que peut-on "
        "faire ? » expected **jouer**. accepted jouer | attendre | un "
        "adulte | demander. Retry dump (label, pas leçon). Non récitée "
        "dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le lacet glisse. Papa noue. Sur le nœud, un éclat de lacet "
        "brille. Cloche lointaine, ombre d'arbre, cour puis jardin. "
        "Cerceau rouge dans l'herbe. Amir veut la file **maintenant**. "
        "Chouchou saute, trop vite : le cerceau part vers la gourde. "
        "Sourire parti. Papa s'accroupit. Il refuse de foncer. Ils "
        "restent dans la file. Merci vécu. Deuxième ruse : ombre qui "
        "glisse, racine, elle veut passer. Il s'arrête, lit l'éclat. "
        "Un éclat de lacet tient sur le nœud.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cour d'école puis jardin, ombre d'arbre, cloche "
        "lointaine, cerceau rouge, lacet, gourde, file.\n"
        "- Désir : le cerceau, maintenant, dans la file jusqu'à l'arbre.\n"
        "- Objet : cerceau rouge, lacet, gourde, nœud.\n"
        "- Indice unique : éclat de lacet, vu dès l'ouverture sur le "
        "nœud, payé sur le nœud. Pas éclat de cerceau / cour / cloche / "
        "poussière / craie.\n"
        "- Urgence douce : Chouchou arrive, Amir accélère.\n"
        "- Imprévu 1 : Chouchou tourne trop vite, le cerceau part vers "
        "la gourde, tombe dans l'herbe.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après la file.\n"
        "- Imprévu 2 (plus rusé) : ombre qui glisse, file sous l'arbre, "
        "elle veut passer, cerceau qui penche vers une racine.\n"
        "- Résolution : il refuse de foncer, observe, écoute la cloche, "
        "retrouve l'éclat, elle souffle, ils roulent jusqu'au tronc.\n"
        "- Retour : trace d'herbe sur le cerceau, éclat sur le nœud.\n\n"
        "## Vécu\n\n"
        "Amir veut le cerceau **maintenant**. Impatience, puis cerceau "
        "qui part, sourire parti. Chouchou prend son élan, pose sa "
        "limite (attends, silence, souffle). Papa se baisse, pose une "
        "question, ne récite pas la règle. Ils agissent : file, poussée "
        "sans se presser, racine contournée. Merci vécu. Fin : l'éclat "
        "du début tient sur le nœud.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : La file du cerceau (noyau mission, dump Baptiste/Noa "
        "file du cerceau). Relance : Que peut-on faire ? expected jouer.\n"
        "- Lieu : cour puis jardin (ombre, cloche lointaine, cerceau "
        "dans l'herbe). Maman et papa. Amir = enfant-m. Chouchou = "
        "copine. Baptiste/Noa dump-meta retirés. Pas de maîtresse.\n"
        "- Ouverture inventée (lacet qui glisse, clic du bout), pas un "
        "gabarit v2, pas « Une craie blanche a roulé sous le banc » du "
        "dump, pas le bateau-feuille.\n"
        "- Indice unique : éclat de lacet (papa noue à l'ouverture, "
        "payé). BAN éclat de cerceau / cour / cloche / poussière / "
        "craie + flaque / piquet / bol / chiffon / sauge. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » / « ce n'est pas une "
        "faute » du dump.\n"
        "- Leçon non dite : on la voit quand le cerceau part, quand il "
        "refuse de foncer, quand ils restent dans la file, quand elle "
        "souffle sous l'arbre. Pas « ce n'est pas une faute ». Pas "
        "« on peut jouer / attendre / demander ». Pas « beaucoup "
        "d'énergie » en slogan.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Chouchou a de l'énergie. Que "
        "peut-on faire ? ». expected jouer. Retry dump (label). 5 "
        "chunks, kinds inchangés.\n"
        "- example4 020 / 052 / 084 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_ene_001_01.py` / "
        "`_write_atom_dif_cor_003_07.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers la racine.\n"
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
