#!/usr/bin/env python3
"""ATOM-DIF.PAR.001-02 — Le seau dans le sable chaud (F-NAR-019, N2, DIF.PAR.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.001-02"
TITLE = "Le seau dans le sable chaud"
N2 = LIMITS["N2"]
CHARS = "Nino, Mila, papa, maman"
SETTING = (
    "parc, bac à sable, couverture à carreaux, banc, "
    "oiseau gris, seau rouge, pelle jaune, gourde"
)
INDICE = "éclat de banc"
FIL = (
    "Le seau rouge tape le bac. Près du banc, un éclat de banc "
    "brille. Un oiseau gris picore. Nino veut un puits, maintenant, "
    "pour le seau. Mila parle peu. Il fonce, explique trop, le seau "
    "penche. Sourire parti. Il refuse de foncer, tend le seau, attend. "
    "Merci vécu. Gourde trop vite. Il s'arrête, lit l'éclat. Un éclat "
    "de banc tient près de l'oiseau."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(parquet|tartine|confiture|garage|camion|coussin|fraise|"
    r"flaque|piquet|portail|rotin|crochet|platane|cageot|résine|"
    r"resine|botte|bottes|limace|perron|chaise|tiroir|fraisier|"
    r"cuivre|buis|cerceau|grille|cour|pierre|nappe|figue|robinet|"
    r"planche|émail|email|samare|bassine|lunettes|corde|drap|"
    r"ballon|entrée|entree|merle)\b",
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
    "on peut tendre",
    "tu peux tendre",
    "tendre un jouet",
    "on ne force pas",
    "ne force pas la parole",
    "force pas la parole",
    "tu as su attendre",
    "on n'imite pas",
    "on n imite pas",
    "ce n'est pas une faute",
    "n'est pas une faute",
    "pas une faute",
    "vous jouez",
    "on joue",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "trois notes",
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
    "éclat de sable",
    "éclat de pelle",
    "éclat de gourde",
    "éclat de couverture",
    "éclat de bol",
    "éclat de tartine",
    "éclat de camion",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
    "grain de sable",
    "léa",
    "lea",
    "adam",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de banc",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis élan; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_un_puits_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis large; "
            "respiration=ample puis retenue"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="seau",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis découragement; intensite=2; "
            "destinataire=enfant; "
            "sous_texte=mila_retire_les_doigts_ne_dit_rien; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Nino",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=mila_parle_peu_que_fait_nino; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="seau",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_refuse_de_foncer_tend_attend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de banc",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=gourde_trop_vite_il_s_arrete; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de banc",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pres_de_l_oiseau; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "attendre",
    "accepted_examples": "attendre | tendre | le seau | un jouet | il attend",
    "retry_prompt": "Il tend un jouet. Il attend. Que fait Nino ?",
    "engine_ok_text": "Oui, attendre.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc",
        [
            "narrateur|Le plastique du seau tape le rebord du bac.",
            "narrateur|Ça fait toc, court et chaud.",
            "enfant-m|J'ai entendu le toc.",
            "papa|Près du bac, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le sable sent le soleil.",
            "narrateur|Papa pose le sac de goûter.",
            "narrateur|Le sac fait un bruit de papier.",
            "maman|Je déplie la couverture à carreaux.",
            "narrateur|Les carreaux sont bleus et blancs.",
            "enfant-m|Elle est tiède, maman.",
            "maman|Tu la sens, sous les genoux ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un oiseau gris picore près du banc.",
            "narrateur|Au bord du bois, un éclat de banc brille.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|Une cigale chante près des arbres.",
            "enfant-m|Elle chante fort.",
            "maman|Le sable est chaud, Nino ?",
            "enfant-m|Oui, il brûle un peu.",
            "enfant-m|Je veux un puits, maintenant !",
            "enfant-m|Un puits pour le seau rouge.",
            "papa|Un puits dans le bac ?",
            "enfant-m|Oui.",
            "enfant-m|Bien creux.",
            "narrateur|En ce moment, Nino s'assoit près du bac.",
            "narrateur|Le seau rouge est tiède.",
            "narrateur|Une pelle jaune est à côté.",
            "narrateur|Le manche est un peu rêche.",
            "enfant-m|Il gratte, papa.",
            "papa|Tu tiens la pelle, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Mila arrive près du bac.",
            "narrateur|Elle marche sans bruit.",
            "enfant-m|Tu creuses avec moi ?",
            "narrateur|Mila ne dit rien.",
            "narrateur|Elle regarde ses mains.",
            "narrateur|Le sable y luit un peu.",
            "enfant-m|On fait un puits.",
            "narrateur|Nino ouvre la bouche trop vite.",
            "narrateur|Les mots montent.",
            "papa|Tu vois Mila, Nino ?",
            "enfant-m|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_X": (
        "obstacle",
        "enfants_parc",
        [
            "narrateur|Nino a envie de tout expliquer.",
            "enfant-m|Le puits !",
            "enfant-m|L'eau !",
            "enfant-m|Le seau !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "narrateur|Il pousse le seau vers Mila.",
            "enfant-m|Prends-le, maintenant !",
            "narrateur|Le seau penche trop.",
            "narrateur|Le sable tombe sur le bord.",
            "narrateur|Mila retire les doigts.",
            "narrateur|Elle ne dit rien.",
            "enfant-m|Oh.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "papa|Elle a retiré les mains, Nino ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains tiennent le seau, Nino ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de banc tremble, puis tient.",
            "narrateur|Mila tape le sable du doigt.",
            "enfant-m|Elle reste là, papa.",
            "papa|Tu la vois, près du bac ?",
            "enfant-m|Oui.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Nino regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_X_Q0001": (
        "clue",
        "",
        [
            "narrateur|Mila parle peu.",
            "narrateur|Que fait Nino ?",
        ],
    ),
    "CHK_T0000_P0000_X_C0001": (
        "resolution",
        "enfants_parc",
        [
            "narrateur|Nino veut tout dire, tout de suite.",
            "enfant-m|Je t'explique, maintenant !",
            "narrateur|Il avance trop vite vers Mila.",
            "narrateur|Les mots se bousculent.",
            "narrateur|Mila recule un peu.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le seau, un instant.",
            "narrateur|Il écoute la cigale.",
            "papa|Tu veux le puits avec Mila ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Papa, on fait quoi ?",
            "papa|On pose le seau, puis la pelle.",
            "enfant-m|D'accord.",
            "narrateur|Nino tend le seau, sans se presser.",
            "narrateur|Il reste un moment, les mains ouvertes.",
            "narrateur|Mila souffle.",
            "narrateur|Elle tend les mains, sans parler.",
            "copine|Oui.",
            "narrateur|Mila prend le seau.",
            "papa|Merci, Nino.",
            "narrateur|Papa a vu les deux, près du bac.",
            "maman|Le plastique est tiède, sous les doigts.",
            "enfant-m|Il est chaud.",
            "narrateur|Mila le remplit.",
            "narrateur|Nino creuse avec la pelle jaune.",
            "narrateur|Un trou rond s'ouvre.",
            "narrateur|Mila verse le seau.",
            "narrateur|Le puits grandit.",
            "enfant-m|Le puits.",
            "copine|Puits.",
            "enfant-m|Puits.",
            "maman|Tes mains sont au chaud, Nino ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_X_END": (
        "action",
        "enfants_parc",
        [
            "narrateur|Maman ouvre la gourde.",
            "enfant-m|L'eau, maintenant !",
            "narrateur|Nino envoie la gourde trop vite.",
            "narrateur|Un filet penche hors du trou.",
            "enfant-m|Ça tombe !",
            "enfant-m|Dis-le, Mila !",
            "narrateur|Mila serre les lèvres.",
            "narrateur|Nino avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Nino refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le banc, un instant.",
            "narrateur|Il écoute l'oiseau près du bois.",
            "narrateur|Au bord du banc, un éclat de banc luit.",
            "enfant-m|Là, sur le banc.",
            "enfant-m|Tu prends la gourde, Mila ?",
            "narrateur|Mila ne dit rien.",
            "narrateur|Elle tend les mains, sans parler.",
            "copine|Oui.",
            "narrateur|Nino passe la gourde, sans se presser.",
            "narrateur|Mila verse, plus lentement.",
            "narrateur|Le fond devient sombre.",
            "copine|Eau.",
            "enfant-m|Eau.",
            "papa|Tu la vois, l'eau ?",
            "enfant-m|Oui, papa.",
            "maman|Le puits est creux, Nino ?",
            "enfant-m|Oui, maman.",
            "narrateur|Ils restent près du trou.",
            "narrateur|La couverture à carreaux est un peu sablée.",
            "papa|Le puits tient, Nino ?",
            "enfant-m|Oui, papa.",
            "maman|Un rayon passe sur le seau rouge.",
            "enfant-m|Il allume le puits.",
        ],
    ),
    "CHK_T0000_P0000_X_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du bac.",
            "maman|Une compote, Nino ?",
            "narrateur|Mila secoue la tête.",
            "enfant-m|D'accord.",
            "papa|D'accord.",
            "maman|Tu as fini le puits, Nino ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Il a de l'eau.",
            "papa|Tu souffles sur le bord ?",
            "enfant-m|Oui, papa.",
            "narrateur|Nino souffle, un peu de sable vole.",
            "enfant-m|Le sable est chaud.",
            "maman|Tu le sens, le sable ?",
            "enfant-m|Oui, maman.",
            "papa|Le puits reste un peu, rond.",
            "enfant-m|Il a tenu, dans le bac.",
            "copine|Puits.",
            "narrateur|Le seau est à l'ombre, sous le banc.",
            "narrateur|Le puits fait une petite ombre.",
            "enfant-m|On y remet de l'eau, après.",
            "narrateur|Un éclat de banc tient près de l'oiseau.",
        ],
    ),
}


def vet(lines: list[str], cid: str = "") -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    skip_lesson = cid == "CHK_T0000_P0000_X_Q0001"
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
        if cid == "CHK_T0000_P0000_X_Q0001":
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
    if INDICE not in by["CHK_T0000_P0000_X_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Nino = enfant-m, Mila = copine)")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Mila absente (copine)")
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
    if not any(r == "enfant-m" for r in roles):
        raise SystemExit(f"{SID}: enfant-m absent")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_X_Q0001"
    ).lower()
    for lesson in (
        "ce n'est pas une faute",
        "n'est pas une faute",
        "on peut jouer",
        "on peut attendre",
        "on peut demander",
        "on peut tendre",
        "tu peux tendre",
        "tendre un jouet",
        "on joue",
        "vous jouez",
        "il faut attendre",
        "on doit demander",
        "il faut demander",
        "on ne force pas",
        "tu as su attendre",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_X_Q0001"]
    if q["text"] != "Mila parle peu. Que fait Nino ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != "attendre | tendre | le seau | un jouet | il attend":
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Il tend un jouet. Il attend. Que fait Nino ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    if "seau rouge" not in blob:
        raise SystemExit(f"{SID}: manque seau rouge")
    if "couverture à carreaux" not in blob and "couverture a carreaux" not in blob:
        raise SystemExit(f"{SID}: manque couverture à carreaux")
    if "pelle jaune" not in blob:
        raise SystemExit(f"{SID}: manque pelle jaune")
    if "gourde" not in blob:
        raise SystemExit(f"{SID}: manque gourde")
    if "oiseau" not in blob:
        raise SystemExit(f"{SID}: manque oiseau")
    for ban in (
        "éclat de seau",
        "éclat de sable",
        "éclat de pelle",
        "éclat de gourde",
        "grain de sable",
        "grain de",
        "parquet",
        "tout doux",
        "tout calme",
        "merle",
        "trois notes",
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
        "- **Leçon :** DIF.PAR.001 — Mila parle peu (vécue : Nino explique "
        "trop, le seau penche, elle retire les doigts ; il refuse de foncer, "
        "tend le seau, attend, passe la gourde sans se presser). JAMAIS dite "
        "dans le récit. Pas « on peut attendre / tendre ». Pas « on ne force "
        "pas la parole ».\n"
        "- **Personnages :** Nino, Mila, papa, maman. Nino = enfant-m "
        "(propose, trop vite, puis refuse de foncer). Mila = copine "
        "(parle peu, silence, oui, puits, eau). Troupe D16. Pas de maîtresse. "
        "Léa / Adam du dump → INTERDIT.\n"
        "- **Lieu :** parc, bac à sable, couverture à carreaux, banc, "
        "oiseau gris, seau rouge, pelle jaune, gourde. ≠ PAR.001-01 "
        "cuisine / tartine / parquet / coussins / garage / camion.\n"
        "- **Indice unique :** éclat de banc (brille à l'ouverture près "
        "de l'oiseau → tremble au seau penché → luit au refus gourde → "
        "tient près de l'oiseau). BAN éclat de seau / sable / pelle / "
        "gourde. BAN grain de sable.\n"
        "- **Question moteur :** « Mila parle peu. Que fait Nino ? » "
        "expected **attendre**. accepted `attendre | tendre | le seau | "
        "un jouet | il attend`. retry dump (label). Non récitée dans les "
        "autres chunks.\n"
        "- **Structure conservée :** 6 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le seau rouge tape le bac. Au bord du bois, un éclat de banc "
        "brille. Oiseau gris, cigale, couverture à carreaux. Nino veut un "
        "puits **maintenant**, pour le seau. Mila arrive, parle peu. Il "
        "fonce, explique trop, le seau penche. Sourire parti. Papa "
        "s'accroupit. Il refuse de foncer. Il tend le seau, attend. Merci "
        "vécu. Deuxième ruse : gourde trop vite, « dis-le », lèvres "
        "serrées. Il s'arrête, lit l'éclat. Un éclat de banc tient près "
        "de l'oiseau.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : parc, bac à sable, couverture à carreaux, banc, oiseau "
        "gris, cigale, seau rouge, pelle jaune, gourde. ≠ PAR.001-01 "
        "parquet / tartine / garage.\n"
        "- Désir : un puits dans le sable chaud, maintenant, pour le seau.\n"
        "- Objet : seau rouge, pelle jaune, gourde, bac.\n"
        "- Indice unique : éclat de banc, vu dès l'ouverture, payé près "
        "de l'oiseau. Pas éclat de seau (objet-mission). Pas grain de sable.\n"
        "- Urgence douce : le puits doit tenir, le sable est chaud.\n"
        "- Imprévu 1 : Nino explique trop, pousse le seau, Mila retire "
        "les doigts.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« d'accord ».\n"
        "- Imprévu 2 (plus rusé) : gourde trop vite, il veut lui faire "
        "dire, elle serre les lèvres.\n"
        "- Résolution : il refuse de foncer, observe, écoute l'oiseau, "
        "retrouve l'éclat, Mila tend les mains.\n"
        "- Retour : puits rond, seau à l'ombre, éclat près de l'oiseau.\n\n"
        "## Vécu\n\n"
        "Nino veut le puits **maintenant**. Impatience, puis seau qui "
        "penche, sourire parti. Mila pose sa limite (silence, doigts "
        "retirés, lèvres serrées). Papa se baisse, pose une question, ne "
        "récite pas la règle. Ils agissent : seau tendu, gourde passée "
        "sans se presser. Merci vécu. Fin : l'éclat du début tient près "
        "de l'oiseau.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le seau dans le sable chaud (noyau dump : puits du "
        "seau rouge). Relance : Que fait Nino ? expected attendre.\n"
        "- Lieu du dump (parc, bac à sable, couverture à carreaux). "
        "Maman présente. Mila = copine.\n"
        "- Ouverture inventée (toc du seau contre le bac), pas un "
        "gabarit v2, pas « Nino est au parc », pas « Une cigale chante "
        "tout près du bac » du dump en première ligne.\n"
        "- Indice unique : éclat de banc (oiseau près du banc). BAN "
        "éclat de seau / sable / pelle / gourde. BAN grain de sable. "
        "Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout bas » / « encore » du dump.\n"
        "- Leçon non dite : on la voit quand le seau penche, quand Nino "
        "s'arrête, quand il tend et attend. Pas « on peut attendre / "
        "tendre ». Pas « on ne force pas la parole » hors retry label.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Mila parle peu. Que fait "
        "Nino ? ». expected attendre. retry dump. 6 chunks, kinds "
        "inchangés.\n"
        "- example4 025 / 057 / 089 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_ene_001_03.py`.\n"
        "- TTS complet (6) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers la gourde.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 6 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")


if __name__ == "__main__":
    main()
