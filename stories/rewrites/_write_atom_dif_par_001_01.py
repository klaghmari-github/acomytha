#!/usr/bin/env python3
"""ATOM-DIF.PAR.001-01 — Le camion rouge sur le tapis (F-NAR-019, N2, DIF.PAR.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.001-01"
TITLE = "Le camion rouge sur le tapis"
N2 = LIMITS["N2"]
CHARS = "Sarah, Victorina, papa, maman"
SETTING = (
    "maison, salon, camion rouge, tapis bleu, parquet, "
    "rayon, sac, boîte en bois"
)
INDICE = "éclat de parquet"
FIL = (
    "Un rayon glisse sur le parquet. Près du tapis bleu, un "
    "éclat de parquet brille. Sarah veut le camion rouge, "
    "maintenant. Victorina ne dit rien. Sarah pousse trop vite. "
    "Sourire parti, poitrine, papa accroupi. Elle refuse de "
    "foncer, attend, tend le camion. Merci vécu. Boîte en bois, "
    "camion trop vite. Un éclat de parquet tient sur le bois."
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
    r"ballon|entrée|entree|horloge|bol|casserole|soupe|carotte|"
    r"chiffon|sauge|lacet|commode|gond|banc|coussin|confiture|"
    r"tartine|fraise)\b",
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
        emphasis="éclat de parquet",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_camion_maintenant; "
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
            "sous_texte=victorina_parle_peu_que_fait_sarah; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="camion",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_refuse_de_foncer_attend_tend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de parquet",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=boite_camion_trop_vite_elle_attend; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de parquet",
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
    "accepted_examples": (
        "attendre | tendre un jouet | un jouet | le camion | elle attend"
    ),
    "retry_prompt": "Elle tend un jouet. Elle attend. Que fait Sarah ?",
    "engine_ok_text": "Oui, attendre.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "camion",
        [
            "narrateur|Un rayon glisse sur le parquet.",
            "narrateur|Ça fait une ligne chaude, étroite.",
            "enfant-f|Il chauffe le bois, papa.",
            "papa|Tu le vois, le rayon, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le tapis bleu tient un carré de soleil.",
            "narrateur|Le poil est tiède, contre la paume.",
            "enfant-f|Il est chaud, maman.",
            "maman|Le soleil est dessus ?",
            "enfant-f|Oui.",
            "narrateur|Près du tapis, un éclat de parquet brille.",
            "enfant-f|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Une poussière danse dans le rayon.",
            "enfant-f|Elle vole, papa.",
            "papa|Au-dessus du tapis ?",
            "enfant-f|Oui, au-dessus.",
            "narrateur|Le camion rouge reste au bord du tapis.",
            "narrateur|Ses roues sont froides, un peu poussiéreuses.",
            "enfant-f|Il sent le plastique, papa.",
            "papa|Tu le tiens, Sarah ?",
            "enfant-f|Oui.",
            "narrateur|En ce moment, Sarah pose le camion.",
            "enfant-f|Je veux le camion, maintenant !",
            "enfant-f|Sur le tapis bleu, tout de suite.",
            "papa|Une petite route, là ?",
            "enfant-f|Oui, une route.",
            "maman|Les roues touchent le poil bleu.",
            "enfant-f|Il doit partir.",
            "narrateur|La porte s'ouvre.",
            "narrateur|Victorina arrive avec son sac.",
            "narrateur|Le sac frotte le parquet.",
            "narrateur|Elle regarde le sol.",
            "narrateur|Elle ne dit rien.",
            "enfant-f|Tu pousses avec moi ?",
            "narrateur|Victorina serre le sac.",
            "narrateur|Sarah a envie de tout raconter.",
            "narrateur|Les mots montent très vite.",
            "enfant-f|Le rayon !",
            "enfant-f|Le tapis !",
            "enfant-f|Le camion !",
            "narrateur|Sarah pousse trop vite vers elle.",
            "narrateur|Le camion tape le sac.",
            "enfant-f|Oh.",
            "narrateur|Le camion bascule sur le parquet.",
            "enfant-f|Le camion.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Victorina, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains tiennent le camion, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de parquet tremble, puis tient.",
            "narrateur|Victorina reste près du sac.",
            "enfant-f|Elle ne dit rien, papa.",
            "narrateur|Sarah regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorina parle peu.",
            "narrateur|Que fait Sarah ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "tapis",
        [
            "narrateur|Sarah veut le camion, tout de suite.",
            "enfant-f|Je le pousse, maintenant !",
            "narrateur|Elle avance trop vite vers Victorina.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "narrateur|Victorina baisse les yeux.",
            "narrateur|Elle serre le sac contre elle.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le camion, un instant.",
            "narrateur|Elle écoute le rayon sur le bois.",
            "papa|Tu veux la route avec Victorina ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Papa, on fait quoi ?",
            "papa|On pose le camion, puis on reste.",
            "enfant-f|D'accord.",
            "narrateur|Sarah reste un moment, les mains ouvertes.",
            "narrateur|Elle attend.",
            "narrateur|Elle tend le camion.",
            "enfant-f|Pour toi.",
            "narrateur|Victorina ne dit rien.",
            "narrateur|Elle prend le camion, sans parler.",
            "copine|Oui.",
            "narrateur|Sarah pose les mains sur le tapis.",
            "narrateur|Elle reste, sans se presser.",
            "narrateur|Victorina pousse le camion, plus lentement.",
            "papa|Merci, Sarah.",
            "narrateur|Papa a vu les deux, au salon.",
            "maman|Le poil est tiède, sous les doigts.",
            "enfant-f|Il est chaud.",
            "narrateur|La route tient, un peu de travers.",
            "enfant-f|Le camion.",
            "papa|Il a une porte, là ?",
            "enfant-f|Oui, là.",
            "narrateur|Sarah glisse la main sur le toit.",
            "narrateur|Le plastique est doux, contre la peau.",
            "maman|Tes mains sont au chaud, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Victorina s'assoit, puis se relève.",
            "copine|Vroom.",
            "enfant-f|On va jusqu'au bout ?",
            "maman|Le tapis bleu va jusqu'au parquet.",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "boîte",
        [
            "narrateur|Ils restent sur le tapis bleu.",
            "narrateur|Une boîte en bois fait un garage.",
            "enfant-f|Il entre, maintenant !",
            "narrateur|Sarah pousse trop vite.",
            "narrateur|Le camion penche vers le parquet.",
            "enfant-f|Ça tombe !",
            "narrateur|Victorina tend les mains, sans parler.",
            "narrateur|Sarah avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Sarah refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le camion, un instant.",
            "narrateur|Elle écoute le silence du salon.",
            "narrateur|Au bord du tapis, un éclat de parquet luit.",
            "enfant-f|Là, sur le bois.",
            "enfant-f|Tu prends le camion, Victorina ?",
            "narrateur|Victorina ne dit rien.",
            "narrateur|Elle tend les mains, sans parler.",
            "copine|Oui.",
            "narrateur|Sarah pousse le camion, sans se presser.",
            "narrateur|Victorina le reçoit, plus lentement.",
            "narrateur|Le plastique est lisse et tiède.",
            "papa|Tu le vois, le camion ?",
            "enfant-f|Oui, papa.",
            "maman|Le tapis bleu est près du parquet ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le camion entre dans la boîte.",
            "narrateur|Sarah pose une main sur le toit.",
            "narrateur|Victorina pose la suivante.",
            "papa|La boîte tient, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|Un rayon passe sur le parquet.",
            "enfant-f|Il allume le bois.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du tapis.",
            "maman|Le camion est arrivé, Sarah ?",
            "enfant-f|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah souffle, un filet d'air.",
            "enfant-f|Le plastique sent bon.",
            "maman|Tu le sens, le camion ?",
            "enfant-f|Oui, maman.",
            "papa|La route reste un peu, de travers.",
            "enfant-f|Elle a tenu, sur le tapis.",
            "copine|Vroom.",
            "narrateur|Le tapis est chaud, sous les mains.",
            "narrateur|Le camion rouge fait de l'ombre.",
            "enfant-f|On y retourne, après.",
            "narrateur|Un éclat de parquet tient sur le bois.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-f", "copine"):
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
    if "tend le camion" not in blob:
        raise SystemExit(f"{SID}: manque tend le camion")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Sarah = enfant-f, Victorina = copine)")
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
    if any(r not in ("narrateur", "papa", "maman", "enfant-f", "copine") for r in roles):
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
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Victorina parle peu. Que fait Sarah ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "attendre | tendre un jouet | un jouet | le camion | elle attend"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Elle tend un jouet. Elle attend. Que fait Sarah ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    copine_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    ).lower()
    if "vroom" not in copine_txt:
        raise SystemExit(f"{SID}: Victorina sans vroom")
    n_copine = sum(
        1
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    )
    if n_copine > 5:
        raise SystemExit(f"{SID}: Victorina parle trop ({n_copine})")
    if "tapis bleu" not in blob:
        raise SystemExit(f"{SID}: manque tapis bleu")
    if "camion rouge" not in blob:
        raise SystemExit(f"{SID}: manque camion rouge")
    if "rayon" not in blob:
        raise SystemExit(f"{SID}: manque rayon")
    if "parquet" not in blob:
        raise SystemExit(f"{SID}: manque parquet")
    if "horloge" in blob:
        raise SystemExit(f"{SID}: BAN horloge")
    if "ne dit rien" not in blob:
        raise SystemExit(f"{SID}: manque silence vécu")
    for ban in (
        "éclat de tapis",
        "éclat d'horloge",
        "éclat de bol",
        "éclat de flaque",
        "éclat de piquet",
        "éclat de chiffon",
        "éclat de gond",
        "éclat de sauge",
        "éclat de lacet",
        "éclat de commode",
        "éclat de banc",
        "tout doux",
        "tout calme",
        "kenzo",
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
        "- **Public :** N2 (≤15 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.PAR.001 — quand l'autre parle peu, on attend, "
        "on tend le jouet (vécue : camion trop vite, sourire parti, elle "
        "refuse de foncer, attend, tend le camion, Victorina prend sans "
        "parler). JAMAIS dite dans le récit. Pas « il faut attendre ». "
        "Pas « elle parle peu » hors question moteur.\n"
        "- **Personnages :** Sarah, Victorina, papa, maman. Dump Kenzo/"
        "Maya → D16. Sarah = enfant-f (veut le camion maintenant, trop "
        "vite, puis refuse de foncer). Victorina = copine (parle peu, "
        "regarde le sol, oui, vroom). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** maison, salon, camion rouge, tapis bleu, parquet, "
        "rayon, sac, boîte en bois. ≠ ENE.001-03 bol / cuisine. ≠ dump "
        "confiture / tartine / horloge.\n"
        "- **Indice unique :** éclat de parquet (brille à l'ouverture "
        "sous le rayon → tremble au camion basculé → luit au refus "
        "boîte → tient sur le bois). BAN éclat de tapis (ENE.001-07) / "
        "horloge (BAN) / bol / flaque / piquet / gond / chiffon.\n"
        "- **Question moteur :** « Victorina parle peu. Que fait "
        "Sarah ? » expected **attendre**. accepted `attendre | tendre "
        "un jouet | un jouet | le camion | elle attend`. retry dump. "
        "Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un rayon glisse sur le parquet. Près du tapis bleu, un éclat "
        "de parquet brille. Camion rouge, poil tiède, poussière. Sarah "
        "veut le camion **maintenant**. Victorina arrive, ne dit rien. "
        "Sarah pousse trop vite, le camion tape le sac. Sourire parti. "
        "Papa s'accroupit. Elle refuse de foncer. Elle attend, tend le "
        "camion. Merci vécu. Deuxième ruse : boîte en bois, camion trop "
        "vite, le parquet. Elle s'arrête, lit l'éclat. Un éclat de "
        "parquet tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : maison, salon, tapis bleu, rayon sur le parquet, "
        "camion rouge, sac, boîte en bois. ≠ ENE flaque / piquet / bol. "
        "≠ dump confiture / horloge.\n"
        "- Désir : le camion rouge, maintenant, sur le tapis bleu.\n"
        "- Objet : camion rouge, tapis bleu, boîte en bois, sac.\n"
        "- Indice unique : éclat de parquet, vu dès l'ouverture sous "
        "le rayon, payé sur le bois. Pas éclat de tapis / horloge.\n"
        "- Urgence douce : Victorina arrive, Sarah accélère les mots.\n"
        "- Imprévu 1 : Sarah pousse trop vite, le camion tape le sac, "
        "bascule. Victorina ne dit rien.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : boîte-garage, camion trop vite, il "
        "penche vers le parquet.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le "
        "silence, retrouve l'éclat, tend, Victorina reçoit.\n"
        "- Retour : route de travers, vroom vécu, éclat sur le bois.\n\n"
        "## Vécu\n\n"
        "Sarah veut le camion **maintenant**. Impatience, puis camion "
        "qui bascule, sourire parti. Victorina pose sa limite (yeux "
        "bas, silence, oui, vroom). Papa se baisse, pose une question, "
        "ne récite pas la règle. Elles agissent : attendre, tendre le "
        "camion, pousser sans se presser. Merci vécu. Fin : l'éclat du "
        "début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le camion rouge sur le tapis (roster). Relance : "
        "Que fait Sarah ? expected attendre.\n"
        "- Lieu du dump (maison, salon) sans confiture / tartine / "
        "horloge. Maman présente. Victorina = copine.\n"
        "- Ouverture inventée (rayon sur le parquet), pas un gabarit "
        "v2, pas « Le couvercle du pot de confiture résiste » du dump "
        "en première ligne.\n"
        "- Indice unique : éclat de parquet. BAN éclat de tapis / "
        "horloge / bol / flaque / piquet / gond / chiffon. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » / « horloge » du "
        "dump.\n"
        "- Leçon non dite : on la voit quand le camion bascule, quand "
        "Sarah s'arrête, quand elle tend, quand Victorina prend sans "
        "parler. Pas « il faut attendre ». Pas « elle parle peu » hors "
        "question. Pas « on peut attendre » hors retry label.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Victorina parle peu. Que "
        "fait Sarah ? ». expected attendre. retry dump. 5 chunks, "
        "kinds inchangés.\n"
        "- example4 024 / 056 / 088 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_ene_001_03.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers la boîte.\n"
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
