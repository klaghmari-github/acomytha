#!/usr/bin/env python3
"""ATOM-DIF.ENE.001-07 — La grotte bleue (F-NAR-019, N3, DIF.ENE.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.ENE.001-07"
TITLE = "La grotte bleue"
N3 = LIMITS["N3"]
CHARS = "Nina, Nino, papa, maman"
SETTING = (
    "salle de jeux, tapis et tunnel, lampe, rond jaune, "
    "grotte de tissu bleu, chaussettes, coussins"
)
INDICE = "éclat de tapis"
FIL = (
    "Un rond jaune dort sur le tapis. À l'ouverture, un "
    "éclat de tapis brille. Nina veut la grotte, maintenant. "
    "Nino saute, trop vite. Le tunnel penche. Sourire parti. "
    "Elle refuse de foncer. Merci vécu. File des chaussettes, "
    "il veut passer. Elle s'arrête, il souffle. Un éclat de "
    "tapis tient à l'ouverture."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(flaque|piquet|bol|lacet|chiffon|sauge|cerceau|grille|"
    r"cour|botte|bottes|drap|ballon|merle|miel|limace|perron|"
    r"chaise|tiroir|fraisier|cuivre|buis|figue|robinet|planche|"
    r"émail|email|samare|bassine|lunettes|corde|pin|maîtresse|"
    r"maitresse|béatrice|beatrice|ewen)\b",
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
    "béatrice",
    "beatrice",
    "ewen",
    "léa",
    "lea",
    "sarah",
    "vous jouez",
    "on joue",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de lampe",
    "éclat de coussin",
    "éclat de laine",
    "éclat de flaque",
    "éclat de piquet",
    "éclat de bol",
    "éclat de lacet",
    "éclat de chiffon",
    "éclat de sauge",
    "éclat de cerceau",
    "éclat de grille",
    "éclat de cour",
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
    "éclat de chaussette",
    "éclat de tunnel",
    "éclat de grotte",
    "éclat de tissu",
    "éclat de rond",
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
        emphasis="éclat de tapis",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_grotte_maintenant; "
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
            "sous_texte=nino_bouge_trop_vite_que_peut_on_faire; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grotte",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_refuse_va_aux_coussins_avec_lui; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de tapis",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_il_souffle_ils_passent; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de tapis",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_a_l_ouverture; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer",
    "accepted_examples": "jouer | attendre | un adulte | demander",
    "retry_prompt": (
        "On peut jouer, attendre, ou demander à un adulte. Que fait Nina ?"
    ),
    "engine_ok_text": "Oui, jouer.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "",
        [
            "narrateur|Un rond jaune dort sur le tapis.",
            "narrateur|Il est chaud, presque rond.",
            "enfant-f|Il est chaud.",
            "papa|Tu le vois, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|La petite lampe pose ce rond, sans bruit.",
            "maman|Tes genoux sont sur le tapis, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|À l'ouverture, un éclat de tapis brille.",
            "enfant-f|Il brille, papa.",
            "papa|Près du tunnel ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Le tunnel de tissu sent le linge.",
            "narrateur|Une couture gratte un peu, sous les doigts.",
            "enfant-f|C'est une grotte.",
            "enfant-f|Elle est bleue.",
            "maman|La grotte est prête, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Papa empile deux coussins, près du tapis.",
            "enfant-f|Ils sont mous.",
            "papa|Tu les as sentis ?",
            "enfant-f|Oui, chauds.",
            "narrateur|Des chaussettes attendent, pliées.",
            "enfant-f|Elles sont chaudes, maman.",
            "maman|Tu en poses une, près du tissu ?",
            "enfant-f|Oui.",
            "narrateur|En ce moment, Nina rampe vers la grotte.",
            "enfant-f|Je veux passer, maintenant !",
            "enfant-f|Dans le tunnel, tout de suite.",
            "papa|Avec tes genoux ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le tapis pique un peu les genoux.",
            "enfant-f|Ça pique.",
            "maman|Tu glisses la main, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nino arrive près du tapis.",
            "narrateur|Ses chaussures tapent le sol.",
            "copain|J'arrive !",
            "enfant-f|Nino !",
            "narrateur|Il saute sur place, trop vite.",
            "copain|Le tunnel !",
            "enfant-f|Moi, le tunnel, maintenant !",
            "narrateur|Nino se met devant le tissu bleu.",
            "narrateur|Il rebondit, trop près de l'ouverture.",
            "narrateur|Le tunnel penche, un peu.",
            "enfant-f|Il penche !",
            "copain|Oh.",
            "narrateur|Nina avance trop, trop vite.",
            "narrateur|Son front touche le tissu, de travers.",
            "enfant-f|Je ne passe pas.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Nino, Nina ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains sont sur le tapis, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de tapis tremble, puis tient.",
            "narrateur|Nino rebondit, les pieds légers.",
            "enfant-f|Il saute, papa.",
            "narrateur|Nina regarde maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino a de l'énergie.",
            "narrateur|Que peut-on faire ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Nina veut le tunnel, tout de suite.",
            "enfant-f|Je passe, maintenant !",
            "narrateur|Elle avance trop vite vers Nino.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copain|Attends.",
            "narrateur|Nino rebondit, trop près du tissu.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Nina refuse de foncer.",
            "narrateur|Elle referme les mains.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le tunnel, un instant.",
            "narrateur|Elle écoute le tissu qui frôle.",
            "papa|Tu veux la grotte avec Nino ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|On va aux coussins ?",
            "maman|On marche jusqu'aux coussins ?",
            "enfant-f|Oui, maman.",
            "papa|Viens, Nino.",
            "copain|J'y vais.",
            "narrateur|Ils marchent vers les coussins.",
            "narrateur|Les genoux font un bruit mou.",
            "enfant-f|Ils sont mous, papa.",
            "papa|Tu t'assois ?",
            "enfant-f|Oui.",
            "narrateur|Nina s'assoit un moment.",
            "narrateur|Le tissu du coussin est tiède.",
            "narrateur|Nino s'assoit aussi.",
            "copain|Il est tiède.",
            "narrateur|Il souffle.",
            "papa|Merci, Nina.",
            "narrateur|Papa a vu les deux, près des coussins.",
            "maman|Le tapis est doux, sous les mains.",
            "enfant-f|Il est doux.",
            "narrateur|Nino reste, les mains ouvertes.",
            "copain|À toi.",
            "enfant-f|D'accord.",
            "maman|C'est à Nina.",
            "narrateur|Nina rampe dans la grotte.",
            "narrateur|Le tissu frôle ses cheveux.",
            "enfant-f|Il est doux.",
            "papa|Tu le sens, le bleu ?",
            "enfant-f|Oui, papa.",
            "narrateur|Puis Nino passe, sans se presser.",
            "copain|J'y vais.",
            "maman|Tes cheveux ont frôlé le tissu, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le ventre de Nina se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près du tapis ?",
            "enfant-f|Oui.",
            "maman|Tes genoux sont au chaud ?",
            "enfant-f|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Maman pose des chaussettes près du tapis.",
            "enfant-f|Une file, maintenant !",
            "narrateur|Nino veut passer, trop vite.",
            "narrateur|Il saute vers l'ouverture.",
            "copain|Moi d'abord !",
            "narrateur|Nina avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le tunnel, un instant.",
            "narrateur|Elle écoute le tissu qui frôle.",
            "narrateur|À l'ouverture, un éclat de tapis luit.",
            "enfant-f|Là, sur le tapis.",
            "enfant-f|Tu restes, Nino ?",
            "narrateur|Nino ne dit rien.",
            "narrateur|Il souffle, sans parler.",
            "copain|Oui.",
            "narrateur|Il reste derrière elle.",
            "enfant-f|Une chaussette, maman ?",
            "maman|La douce, Nina.",
            "narrateur|Nina pose la chaussette à l'ouverture.",
            "narrateur|Le tissu fait un petit bruit.",
            "copain|À moi.",
            "narrateur|Nino pose la sienne, sans se presser.",
            "papa|Tu as soufflé, Nino ?",
            "copain|Un peu.",
            "maman|Le tunnel est droit, Nina ?",
            "enfant-f|On passe ?",
            "papa|Vous passez ensemble ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina rampe, puis s'arrête un peu.",
            "narrateur|Nino rampe aussi, plus lentement.",
            "enfant-f|Le bleu, partout.",
            "copain|Le bleu.",
            "maman|Le tissu a une poussière, Nina ?",
            "enfant-f|Sur le bord.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du tapis.",
            "narrateur|Maman plie un coin du tissu.",
            "enfant-f|On a passé, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-f|Oui, la grotte.",
            "maman|On est bien, ici.",
            "narrateur|Nina tapote le tissu du doigt.",
            "enfant-f|Il est doux, maman.",
            "maman|Tu le sens, le bleu ?",
            "enfant-f|Oui, maman.",
            "papa|Le tunnel est resté, Nina.",
            "enfant-f|Oui, avec Nino.",
            "copain|Le tunnel est resté.",
            "narrateur|Ça sent le linge, un peu tiède.",
            "enfant-f|Et le tapis, maman.",
            "maman|Oui, sous les genoux.",
            "narrateur|Les chaussettes restent près du tissu.",
            "narrateur|Un éclat de tapis tient à l'ouverture.",
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
        raise SystemExit(f"{SID}: enfant-m (Nina = enfant-f, Nino = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Nino absent (copain)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "enfant-f|" not in blob:
        raise SystemExit(f"{SID}: Nina absente (enfant-f)")
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
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Nino a de l'énergie. Que peut-on faire ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != "jouer | attendre | un adulte | demander":
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "On peut jouer, attendre, ou demander à un adulte. Que fait Nina ?":
        raise SystemExit(f"{SID}: retry dump altéré: {retry}")
    copain_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    ).lower()
    if "attends" not in copain_txt:
        raise SystemExit(f"{SID}: Nino sans attends")
    if "souffle" not in blob:
        raise SystemExit(f"{SID}: manque souffle")
    if "tunnel" not in blob:
        raise SystemExit(f"{SID}: manque tunnel")
    if "grotte" not in blob:
        raise SystemExit(f"{SID}: manque grotte")
    if "chaussette" not in blob:
        raise SystemExit(f"{SID}: manque chaussette")
    if "coussin" not in blob:
        raise SystemExit(f"{SID}: manque coussin")
    if "tapis" not in blob:
        raise SystemExit(f"{SID}: manque tapis")
    if "lampe" not in blob:
        raise SystemExit(f"{SID}: manque lampe")
    if "rond jaune" not in blob:
        raise SystemExit(f"{SID}: manque rond jaune")
    for ban in (
        "éclat de lampe",
        "éclat de coussin",
        "éclat de laine",
        "éclat de flaque",
        "éclat de piquet",
        "éclat de bol",
        "éclat de lacet",
        "éclat de chiffon",
        "éclat de sauge",
        "tout doux",
        "tout calme",
        "béatrice",
        "ewen",
        "maîtresse",
        "maitresse",
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
        "on peut jouer, attendre, ou demander à un adulte (vécue : tunnel "
        "qui penche, sourire parti, coussins, file, souffle). JAMAIS dite "
        "dans le récit.\n"
        "- **Personnages :** Nina, Nino, papa, maman. Dump-meta Béatrice/"
        "Ewen → D16. Nina = enfant-f (veut la grotte maintenant). "
        "Nino = copain (saute, trop vite). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** salle de jeux, tapis et tunnel, lampe, rond jaune, "
        "grotte de tissu bleu, chaussettes, coussins. Monde xlsx.\n"
        "- **Indice unique :** éclat de tapis (brille à l'ouverture sur le "
        "rond jaune → tremble quand le tunnel penche → luit à la file → "
        "tient à l'ouverture). BAN éclat de lampe / coussin / laine + "
        "lacet / flaque / piquet / bol / chiffon / sauge.\n"
        "- **Question moteur :** « Nino a de l'énergie. Que peut-on "
        "faire ? » expected **jouer**. accepted jouer | attendre | un "
        "adulte | demander. Retry dump. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un rond jaune dort sur le tapis. À l'ouverture, un éclat de "
        "tapis brille. Tunnel bleu, chaussettes, coussins. Nina veut la "
        "grotte **maintenant**. Nino saute, trop vite : le tunnel penche. "
        "Sourire parti. Papa s'accroupit. Elle refuse de foncer. "
        "Elle demande les coussins. Merci vécu. Deuxième ruse : file des "
        "chaussettes, il veut passer. Elle s'arrête, il souffle. Un "
        "éclat de tapis tient à l'ouverture.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salle de jeux, tapis, tunnel de tissu, lampe, rond "
        "jaune, chaussettes, coussins.\n"
        "- Désir : passer dans la grotte bleue, maintenant.\n"
        "- Objet : tunnel bleu, chaussettes, coussins, lampe.\n"
        "- Indice unique : éclat de tapis, vu dès l'ouverture sur le "
        "rond jaune, payé à l'ouverture. Pas éclat de lampe / coussin / "
        "laine.\n"
        "- Urgence douce : Nino arrive, Nina accélère.\n"
        "- Imprévu 1 : Nino rebondit trop vite, le tunnel penche, elle "
        "ne passe pas.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après les "
        "coussins.\n"
        "- Imprévu 2 (plus rusé) : file des chaussettes, il veut passer, "
        "elle avance trop vite puis s'arrête.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le tissu, "
        "retrouve l'éclat, il souffle, ils rampent.\n"
        "- Retour : tissu plié, éclat à l'ouverture.\n\n"
        "## Vécu\n\n"
        "Nina veut la grotte **maintenant**. Impatience, puis tunnel qui "
        "penche, sourire parti. Nino prend son élan, pose sa limite "
        "(attends, silence, souffle). Papa se baisse, pose une question, "
        "ne récite pas la règle. Ils agissent : coussins, file, passages. "
        "Merci vécu. Fin : l'éclat du début tient à l'ouverture.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : La grotte bleue (noyau dump). Relance : "
        "Que peut-on faire ? expected jouer.\n"
        "- Lieu du dump (salle de jeux, tapis et tunnel). Maman et papa. "
        "Nina = enfant-f. Nino = copain (dump script le mettait enfant-m "
        "par erreur). Béatrice/Ewen dump-meta retirés.\n"
        "- Ouverture inventée (rond jaune sur le tapis), pas un gabarit "
        "v2, pas « Le tunnel bleu sent le linge propre » du dump.\n"
        "- Indice unique : éclat de tapis. BAN éclat de lampe / coussin / "
        "laine + lacet / flaque / piquet / bol / chiffon / sauge. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » / « ce n'est pas une "
        "faute » du dump.\n"
        "- Leçon non dite : on la voit quand le tunnel penche, quand elle "
        "refuse de foncer, quand ils vont aux coussins, quand il souffle "
        "dans la file. Pas « ce n'est pas une faute ». Pas « on peut "
        "jouer / attendre / demander ». Pas « beaucoup d'énergie » en "
        "slogan.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Nino a de l'énergie. Que "
        "peut-on faire ? ». expected jouer. Retry dump. 5 chunks, kinds "
        "inchangés.\n"
        "- example4 021 / 053 / 085 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_ene_001_01.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers la file.\n"
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
