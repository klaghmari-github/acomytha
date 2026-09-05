#!/usr/bin/env python3
"""ATOM-DIF.COR.003-06 — L'abeille en bois du marché (F-NAR-019, N2, DIF.COR.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.003-06"
TITLE = "L'abeille en bois du marché"
N2 = LIMITS["N2"]
CHARS = "Nina, Aniss, papa, maman"
SETTING = "marché, pots dorés, stand des pots, panier de rotin, pain, prunes, muret"
INDICE = "éclat de rotin"
FIL = (
    "Un rayon allume le bord du panier. Au bord, un "
    "éclat de rotin brille. Nina veut montrer l'abeille "
    "en bois, maintenant. Aniss arrive. Un rire commence. "
    "Aniss se tait. Un pot tape. Nina refuse de foncer. "
    "Ils regardent derrière, à deux. Merci vécu. Le pot "
    "glisse. L'éclat de rotin tient au bord."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(miel|merle|cageot|botte|bottes|limace|perron|chaise|tiroir|"
    r"fraisier|cuivre|buis|coussin|figue|robinet|planche|cerceau|"
    r"émail|email|samare|bassine|résine|resine|écorce|ecorce|"
    r"platane|crochet|maîtresse|maitresse)\b",
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
    "il ne faut pas rire",
    "on ne rit pas",
    "on ne va pas rire",
    "rire de l'apparence",
    "lunettes aident",
    "l'amitié ne dépend pas",
    "l'amitie ne depend pas",
    "vous jouez",
    "on joue",
    "pas une blague",
    "n'est pas une blague",
    "n est pas une blague",
    "pas rire",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de panier",
    "éclat de bois",
    "éclat de dorure",
    "éclat de cageot",
    "éclat de platane",
    "éclat de crochet",
    "éclat de pince",
    "éclat de marche",
    "éclat de corde",
    "éclat de caisse",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de horloge",
    "éclat de tasse",
    "éclat d'orange",
    "éclat de orange",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat de farine",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de laine",
    "éclat de lampe",
    "éclat de citron",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de gouttière",
    "éclat de gouttiere",
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
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de pavé",
    "éclat de pave",
    "éclat de bâche",
    "éclat de bache",
    "éclat de poire",
    "éclat de volet",
    "éclat de croissant",
    "éclat de réverbère",
    "éclat de reverberre",
    "éclat de cloche",
    "éclat de corbeille",
    "éclat de sac",
    "éclat de carte",
    "éclat de boule",
    "éclat de galet",
    "éclat de cube",
    "éclat de couloir",
    "éclat de poussière",
    "éclat de poussiere",
    "éclat de cour",
    "éclat de plaque",
    "éclat de pierre",
    "éclat de grille",
    "éclat de couvercle",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de dalle",
    "éclat d'enveloppe",
    "éclat de enveloppe",
    "éclat d'émail",
    "éclat d'email",
    "éclat de samare",
    "éclat de bassine",
    "éclat de cerceau",
    "éclat de robinet",
    "éclat de planche",
    "éclat de figue",
    "éclat de coussin",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de tiroir",
    "éclat de fraisier",
    "éclat de chaise",
    "éclat de perron",
    "éclat de limace",
    "éclat de botte",
    "éclat de résine",
    "éclat de resine",
    "éclat de pin",
    "éclat d'écorce",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de rotin",
    "éclat de lunettes",
    "éclat de gilet",
    "éclat de pot",
    "éclat d'abeille",
    "éclat de abeille",
    "éclat de muret",
    "éclat de pain",
    "éclat de prune",
    "éclat de paille",
    "éclat de plume",
    "éclat de poule",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de rotin",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_montrer_l_abeille_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="lunettes",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=aniss_a_des_lunettes_nina_ne_rit_pas; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="abeille",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=ils_regardent_derriere_a_deux; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de rotin",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de rotin",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_au_bord; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "pas rire",
    "accepted_examples": "pas rire | jouer | ensemble",
    "retry_prompt": "Nina montre l'abeille. Que fait Nina ?",
    "engine_ok_text": "Oui, pas rire.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "marche",
        [
            "narrateur|Un rayon glisse entre les toiles du marché.",
            "narrateur|Il allume le bord du panier.",
            "papa|Tu le vois, Nina ?",
            "enfant-f|Oui, ça brille.",
            "narrateur|Papa tient le panier de rotin.",
            "narrateur|Le rotin est rêche, un peu chaud.",
            "narrateur|Au bord, un éclat de rotin brille.",
            "enfant-f|Il pique un peu, papa.",
            "papa|Tu le sens, sous le doigt ?",
            "enfant-f|Oui, un petit point.",
            "maman|Le panier sent le pain, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le pain chaud tape le bras de maman.",
            "enfant-f|Il est tiède.",
            "maman|On le pose près des pots ?",
            "enfant-f|Oui.",
            "narrateur|Les pots dorés brillent, serrés.",
            "enfant-f|L'abeille en bois, maman.",
            "enfant-f|Je veux la montrer, maintenant !",
            "maman|Elle est au stand des pots ?",
            "enfant-f|Oui, collée derrière.",
            "papa|Tu la cherches, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|En ce moment, Nina cherche l'abeille.",
            "narrateur|Les pots sentent le sucré, un peu la cire.",
            "enfant-f|Elle n'est pas devant.",
            "maman|On avance sans bousculer ?",
            "enfant-f|Oui.",
            "narrateur|Aniss arrive près des pots.",
            "narrateur|Ses chaussures font un petit bruit.",
            "narrateur|Aniss a des lunettes.",
            "narrateur|Aniss a les cheveux courts.",
            "narrateur|Il porte un gilet bleu.",
            "papa|Aniss, tu regardes avec Nina ?",
            "copain|Oui.",
            "enfant-f|Tu viens voir l'abeille ?",
            "copain|Oui.",
            "narrateur|Nina regarde les lunettes, trop longtemps.",
            "narrateur|Un rire commence dans sa bouche.",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "enfant-f|Tu te penches, maintenant !",
            "copain|Non.",
            "enfant-f|Oh.",
            "narrateur|Nina avance trop vite vers les pots.",
            "narrateur|Un pot tape un autre, sec.",
            "narrateur|Ça fait un bruit dur.",
            "enfant-f|Elle n'est plus là !",
            "copain|Elle est cachée.",
            "narrateur|L'éclat de rotin tremble, puis tient.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Aniss, Nina ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains sont collantes, Nina ?",
            "enfant-f|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss a des lunettes.",
            "narrateur|Que fait Nina ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "pots",
        [
            "narrateur|Nina veut l'abeille, tout de suite.",
            "enfant-f|Je me penche, maintenant !",
            "narrateur|Elle avance trop vite vers Aniss.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copain|Non.",
            "narrateur|Aniss reste un peu plus loin.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Nina refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe les pots, un instant.",
            "narrateur|Elle écoute le rotin du panier.",
            "papa|Tu veux l'abeille avec Aniss ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Tu regardes derrière ?",
            "narrateur|Aniss ne dit rien, d'abord.",
            "narrateur|Il se penche près du gros pot.",
            "copain|Je vois les ailes.",
            "enfant-f|D'accord.",
            "papa|Merci, Nina.",
            "narrateur|Papa a vu les deux, près des pots.",
            "maman|Le pot est collant, sous les doigts.",
            "enfant-f|Il sent le sucré.",
            "narrateur|Ils regardent derrière, sans se presser.",
            "narrateur|Aniss montre les ailes peintes.",
            "copain|Là.",
            "enfant-f|Je la vois.",
            "enfant-f|Jaune.",
            "copain|Et noire.",
            "papa|Tu la vois, l'abeille ?",
            "enfant-f|Oui, papa.",
            "maman|Un petit pot, Nina ?",
            "enfant-f|Pour le pain du soir.",
            "narrateur|Maman choisit un pot doré.",
            "narrateur|Nina tient le bord, plus près.",
            "enfant-f|Il est lourd.",
            "copain|Oui.",
            "narrateur|Le ventre de Nina se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près des pots ?",
            "enfant-f|Oui.",
            "maman|Tes mains sont au chaud ?",
            "enfant-f|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pots",
        [
            "narrateur|Nina veut prendre le pot, trop vite.",
            "enfant-f|Je le mets, d'un coup !",
            "narrateur|Le pot glisse vers le bord.",
            "enfant-f|Ça tombe !",
            "copain|Attends.",
            "narrateur|Aniss recule d'un pas.",
            "narrateur|Nina avance les mains, trop vite.",
            "narrateur|Elle regarde les lunettes, trop longtemps.",
            "narrateur|Un rire revient dans sa bouche.",
            "copain|Non.",
            "enfant-f|Oh.",
            "narrateur|Le pot penche, collant.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe l'abeille, un instant.",
            "narrateur|Elle écoute le rotin du panier.",
            "narrateur|Au bord, un éclat de rotin luit.",
            "enfant-f|Là, sur le bord.",
            "enfant-f|Tu tiens avec moi ?",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Il pose les mains sur le pot.",
            "copain|Oui.",
            "narrateur|Ils posent le pot, sans se presser.",
            "narrateur|L'abeille en bois reste collée.",
            "enfant-f|Elle est là.",
            "copain|Derrière.",
            "papa|Tu l'as montrée, Nina ?",
            "enfant-f|Oui, papa.",
            "maman|Le gilet est chaud, Aniss ?",
            "copain|Un peu.",
            "narrateur|Le pot glisse dans le panier.",
            "papa|On passe près du muret ?",
            "copain|J'y vais.",
            "narrateur|Nina marche à côté d'Aniss.",
            "narrateur|Le gilet bleu bouge.",
            "narrateur|Les lunettes restent sur le nez.",
            "enfant-f|C'est plus facile.",
            "papa|Le panier est lourd ?",
            "enfant-f|Un peu, papa.",
            "maman|Un rayon passe entre les toiles.",
            "enfant-f|Il allume le pot.",
            "narrateur|Ils passent près des prunes.",
            "enfant-f|Elles sont lisses.",
            "maman|On va jusqu'au muret ?",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "marche",
        [
            "narrateur|Ils s'arrêtent près du muret.",
            "narrateur|Maman essuie un peu de sucré.",
            "enfant-f|On a vu l'abeille, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-f|Oui, derrière.",
            "maman|On est bien, ici.",
            "narrateur|Nina tapote le bord du panier.",
            "enfant-f|Il a une trace de rotin.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|Le panier est resté, Nina.",
            "enfant-f|Oui, avec Aniss.",
            "copain|Le panier est resté.",
            "narrateur|Ça sent le pain, un peu tiède.",
            "enfant-f|Et les pots, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|L'abeille en bois reste collée.",
            "narrateur|Un éclat de rotin tient au bord.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-f", "copain"):
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
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Nina = enfant-f, Aniss = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Aniss absent (copain)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f", "copain") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "copain" for r in roles):
        raise SystemExit(f"{SID}: copain absent")
    if not any(r == "enfant-f" for r in roles):
        raise SystemExit(f"{SID}: enfant-f absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on joue",
        "vous jouez",
        "il ne faut pas rire",
        "on ne rit pas",
        "on ne va pas rire",
        "lunettes aident",
        "l'amitié ne dépend pas",
        "apparence",
        "pas une blague",
        "pas rire",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    if "miel" in blob:
        raise SystemExit(f"{SID}: miel (STRIP)")
    if "merle" in blob:
        raise SystemExit(f"{SID}: merle")
    if "cageot" in blob:
        raise SystemExit(f"{SID}: cageot (003-03)")
    if "éclat de panier" in blob:
        raise SystemExit(f"{SID}: BAN éclat de panier")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Aniss a des lunettes. Que fait Nina ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "pas rire":
        raise SystemExit(f"{SID}: expected_answer altéré")
    acc = str(q.get("accepted_examples") or "")
    if acc != "pas rire | jouer | ensemble":
        raise SystemExit(f"{SID}: accepted_examples altéré: {acc}")
    retry = str(q.get("retry_prompt") or "")
    if "Que fait Nina ?" not in retry:
        raise SystemExit(f"{SID}: retry sans Que fait Nina ?")
    copain_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    ).lower()
    if "non" not in copain_txt:
        raise SystemExit(f"{SID}: Aniss sans non")
    if "attends" not in copain_txt:
        raise SystemExit(f"{SID}: Aniss sans attends")
    if "pots dorés" not in blob and "pots dores" not in blob:
        raise SystemExit(f"{SID}: manque pots dorés")
    if "abeille en bois" not in blob:
        raise SystemExit(f"{SID}: manque abeille en bois")
    if "muret" not in blob:
        raise SystemExit(f"{SID}: manque muret")
    if "gilet bleu" not in blob:
        raise SystemExit(f"{SID}: manque gilet bleu")
    if "stand des pots" not in blob:
        raise SystemExit(f"{SID}: manque stand des pots")
    for ban in (
        "éclat de panier",
        "éclat de bois",
        "éclat de cageot",
        "éclat de dorure",
        "tout doux",
        "tout calme",
        "aujourd'hui",
        "miel",
        "merle",
        "cageot",
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
        "- **Leçon :** DIF.COR.003 — Aniss a des lunettes "
        "(vécue : rire qui commence, Aniss se tait, pot qui tape, "
        "ils regardent derrière à deux). JAMAIS dite dans le récit.\n"
        "- **Personnages :** Nina, Aniss, papa, maman. Papa ajouté. "
        "Nina = enfant-f (propose, trop vite). Aniss = copain "
        "(lunettes, gilet bleu, silence, non, attends). Troupe D16. "
        "Pas de maîtresse.\n"
        "- **Lieu :** marché, pots dorés, stand des pots, panier de "
        "rotin, pain, prunes, muret. STRIP miel. ≠ 003-03 prune/cageot.\n"
        "- **Indice unique :** éclat de rotin (brille à l'ouverture → "
        "tremble au pot → luit au refus → tient au bord). BAN "
        "éclat de panier / éclat de bois / cageot / miel / merle.\n"
        "- **Question moteur :** « Aniss a des lunettes. Que fait Nina ? » "
        "expected **pas rire**. accepted `pas rire | jouer | ensemble`. "
        "Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un rayon allume le bord du panier. Au bord, un "
        "éclat de rotin brille. Pain tiède, pots dorés. "
        "Nina veut montrer l'abeille en bois **maintenant**. Aniss "
        "arrive. Un rire commence. Aniss se tait, recule : non. Nina "
        "avance toute seule : un pot tape. Sourire parti. Papa "
        "s'accroupit. Elle refuse de foncer. Ils regardent derrière. "
        "Merci vécu. Deuxième ruse : pot trop vite, rire qui revient, "
        "Aniss lâche. Elle s'arrête, lit l'éclat. Un éclat de rotin "
        "tient au bord.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : marché, toiles, pots dorés, stand des pots, panier "
        "de rotin, pain, prunes, muret. ≠ 003-03 prune/cageot.\n"
        "- Désir : montrer l'abeille en bois, collée derrière, maintenant.\n"
        "- Objet : abeille en bois sculptée, pots dorés, panier de rotin.\n"
        "- Indice unique : éclat de rotin, vu dès l'ouverture, payé "
        "au bord. Pas éclat de panier / cageot.\n"
        "- Urgence douce : Aniss arrive, l'abeille attend, Nina accélère.\n"
        "- Imprévu 1 : rire sur les lunettes, Aniss absent au moment "
        "de se pencher, un pot tape.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« d'accord ».\n"
        "- Imprévu 2 (plus rusé) : pot trop vite, rire qui revient, "
        "Aniss dit attends, pot qui penche.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le "
        "rotin, retrouve l'éclat, Aniss tient le pot.\n"
        "- Retour : pot dans le panier, muret, éclat au bord.\n\n"
        "## Vécu\n\n"
        "Nina veut montrer l'abeille **maintenant**. Impatience, puis "
        "rire qui commence, sourire d'Aniss qui part. Aniss prend son "
        "temps, pose sa limite (non, attends, silence). Papa se baisse, "
        "pose une question, ne récite pas la règle. Ils agissent : "
        "regard derrière, pot tenu, sans se presser. Merci vécu. Fin : "
        "l'éclat du début tient au bord.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : L'abeille en bois du marché (noyau dump, miel "
        "retiré). Relance : Que fait Nina ? expected pas rire.\n"
        "- Lieu du dump (marché, pots, panier rotin, pain, prunes, "
        "muret). Papa ajouté. Aniss = copain. STRIP miel : pots "
        "dorés, stand des pots, jamais le mot miel.\n"
        "- Ouverture inventée (rayon sur le bord du panier), pas un "
        "gabarit v2, pas « Une poule picore près des caisses de paille » "
        "du dump.\n"
        "- Indice unique : éclat de rotin. BAN éclat de panier / "
        "éclat de bois / cageot / miel / merle. Pas tache/flèche/"
        "marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » / « déjà » du dump.\n"
        "- Leçon non dite : on la voit quand le rire s'arrête, quand "
        "Aniss recule, quand ils regardent derrière. Pas « Aniss a des "
        "lunettes, on joue » hors question. Pas « on joue » / "
        "« vous jouez » / « il ne faut pas rire » / « pas rire ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Aniss a des lunettes. Que "
        "fait Nina ? ». expected pas rire. accepted "
        "`pas rire | jouer | ensemble`. retry « Que fait Nina ? ». "
        "5 chunks, kinds inchangés.\n"
        "- Distinct 003-03 : pas prune à choisir, pas cageot. Geste : "
        "montrer l'abeille collée, tenir le pot doré.\n"
        "- example4 013 / 045 / 077 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_cor_003_02.py`.\n"
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
