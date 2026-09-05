#!/usr/bin/env python3
"""ATOM-DIF.ENE.001-08 — Le ruban rouge (F-NAR-019, N3, DIF.ENE.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.ENE.001-08"
TITLE = "Le ruban rouge"
N3 = LIMITS["N3"]
CHARS = "Aniss, Sarah, papa, maman"
SETTING = (
    "salon, radio sur la commode, chanson, ruban rouge, "
    "linge près de la fenêtre, clic du bois"
)
INDICE = "éclat de commode"
FIL = (
    "Le bois de la commode fait clic sous la radio. Sur le bois, "
    "un éclat de commode brille. Aniss veut un grand rond lent, "
    "maintenant, pendant la chanson. Sarah saute trop, le ruban "
    "s'enroule au pied. Sourire parti, poitrine, papa accroupi. "
    "Aniss refuse de foncer, attend, demande. Merci vécu. Ruban "
    "trop vite vers la radio. Un éclat de commode tient sur le bois."
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
    r"ballon|entrée|entree|lacet|sauge|chiffon|gond|poussière|"
    r"poussiere|rayon|bol|coussin|casserole|merle|miel|"
    r"maîtresse|maitresse)\b",
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
    "ils jouent",
    "beaucoup d'énergie",
    "beaucoup d'energie",
    "c'est son énergie",
    "c'est son energie",
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
    "éclat de lacet",
    "éclat de sauge",
    "éclat de chiffon",
    "éclat de gond",
    "éclat de ruban",
    "éclat de radio",
    "éclat de linge",
    "éclat de chanson",
    "éclat de fenêtre",
    "éclat de fenetre",
    "éclat de poussière",
    "éclat de poussiere",
    "éclat de bois",
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
        emphasis="éclat de commode",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_un_grand_rond_maintenant; "
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
            "sous_texte=sarah_a_de_l_energie; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="ruban",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_refuse_de_foncer_attend_demande; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de commode",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=ruban_trop_vite_vers_la_radio; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de commode",
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
    "expected_answer": "jouer",
    "accepted_examples": "jouer | attendre | un adulte | demander",
    "retry_prompt": (
        "On peut jouer, attendre, ou demander à un adulte. Que fait Aniss ?"
    ),
    "engine_ok_text": "Oui, jouer.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "radio,commode",
        [
            "narrateur|Le bois de la commode fait clic, sous la radio.",
            "narrateur|Ça craque une fois, sec et chaud.",
            "enfant-m|J'ai entendu le clic.",
            "papa|Près de la radio, Aniss ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa tourne le bouton, lisse sous le doigt.",
            "narrateur|Une chanson arrive, un peu voilée.",
            "enfant-m|Elle est douce.",
            "papa|Tu l'entends, la chanson ?",
            "enfant-m|Oui.",
            "maman|On danse un peu, alors.",
            "narrateur|Maman plie un linge près de la fenêtre.",
            "narrateur|L'air sent le linge sec.",
            "enfant-m|Ça sent le savon, maman.",
            "maman|Tu le sens, Aniss ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Sur le bois, un éclat de commode brille.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|Un ruban rouge dort contre la radio.",
            "narrateur|Le tissu est long, un peu tiède.",
            "enfant-m|Il est chaud, papa.",
            "papa|Le bois est dessous ?",
            "enfant-m|Oui.",
            "narrateur|En ce moment, Aniss prend le ruban.",
            "enfant-m|Je veux danser, maintenant !",
            "enfant-m|Un grand rond, lent, pendant la chanson.",
            "papa|Un petit rond, là ?",
            "enfant-m|Un grand rond.",
            "maman|La radio reste sur la commode.",
            "enfant-m|Après le rond.",
            "narrateur|Aniss lève le bras.",
            "narrateur|Le ruban dessine un arc, bas.",
            "narrateur|Sarah arrive dans le salon.",
            "narrateur|Elle court un peu, pieds légers.",
            "enfant-f|Je saute !",
            "narrateur|Sarah saute trop, trop près du ruban.",
            "enfant-m|Tu danses avec moi ?",
            "enfant-f|Oui.",
            "narrateur|Sarah tourne trop vite.",
            "narrateur|Le ruban s'enroule au pied de la commode.",
            "narrateur|La radio penche, un peu.",
            "enfant-m|Oh.",
            "enfant-m|Le rond.",
            "enfant-f|Il est tombé.",
            "narrateur|Aniss tient le ruban contre lui.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Sarah, Aniss ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains tiennent le ruban, Aniss ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de commode tremble, puis tient.",
            "narrateur|Sarah tape des pieds près de la commode.",
            "enfant-m|Elle saute partout, papa.",
            "narrateur|Aniss regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Sarah a de l'énergie.",
            "narrateur|Que peut-on faire ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "ruban",
        [
            "narrateur|Aniss veut le grand rond, tout de suite.",
            "enfant-m|Je le refais, maintenant !",
            "narrateur|Il avance trop vite vers Sarah.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Attends.",
            "narrateur|Sarah tape des pieds, trop près.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Aniss refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le ruban, un instant.",
            "narrateur|Il écoute la chanson de la radio.",
            "papa|Tu veux le rond avec Sarah ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Papa, on fait quoi ?",
            "papa|On passe le ruban, puis on tourne.",
            "enfant-m|D'accord.",
            "narrateur|Aniss tend le ruban, sans se presser.",
            "narrateur|Il reste un moment, les mains ouvertes.",
            "narrateur|Sarah souffle.",
            "enfant-f|Le mien.",
            "narrateur|Sarah prend le ruban, plus lentement.",
            "papa|Merci, Aniss.",
            "narrateur|Papa a vu les deux, au salon.",
            "maman|Le tissu est tiède, sous les doigts.",
            "enfant-m|Il est chaud.",
            "narrateur|Le ruban se défait du pied de la commode.",
            "enfant-m|Le rond.",
            "papa|Il fait un cercle, là ?",
            "enfant-m|Oui, là.",
            "narrateur|Aniss lève le bras, sans se presser.",
            "narrateur|Le tissu est doux, contre la peau.",
            "maman|Tes mains sont au chaud, Aniss ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Sarah s'assoit, puis se relève.",
            "enfant-f|J'y vais.",
            "enfant-m|On tourne près de la radio ?",
            "maman|La radio reste sur le bois.",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "radio,ruban",
        [
            "narrateur|Ils restent près de la commode.",
            "narrateur|La radio fait clic, sous le bois.",
            "enfant-f|À moi !",
            "narrateur|Sarah tire le ruban trop vite.",
            "maman|On se passe le ruban, près du bois ?",
            "enfant-m|Oui, maman.",
            "narrateur|Aniss envoie le ruban trop vite.",
            "narrateur|Le ruban penche vers la radio.",
            "enfant-m|Ça tombe !",
            "enfant-f|Attends.",
            "narrateur|Aniss avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Aniss refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le bois, un instant.",
            "narrateur|Il écoute le clic de la radio.",
            "narrateur|Sur le bois, un éclat de commode luit.",
            "enfant-m|Là, sur la commode.",
            "enfant-m|Tu prends le ruban, Sarah ?",
            "narrateur|Sarah ne dit rien.",
            "narrateur|Elle tend les mains, sans parler.",
            "enfant-f|Oui.",
            "narrateur|Aniss envoie le ruban, sans se presser.",
            "narrateur|Sarah le renvoie, plus lentement.",
            "narrateur|Le ruban est lisse et chaud.",
            "papa|Tu le vois, le ruban ?",
            "enfant-m|Oui, papa.",
            "maman|La radio est sur le bois ?",
            "enfant-m|Oui, maman.",
            "narrateur|Ils font un rond, plus lent.",
            "narrateur|Aniss lève le bras.",
            "narrateur|Sarah lève le sien.",
            "papa|Le rond tient, Aniss ?",
            "enfant-m|Oui, papa.",
            "maman|Un filet de chanson passe sur le tissu.",
            "enfant-m|Il allume le ruban.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "radio",
        [
            "narrateur|Ils s'assoient près du bois.",
            "maman|La chanson s'arrête, Aniss ?",
            "enfant-m|Oui, maman.",
            "papa|Tu poses le ruban sur le bois ?",
            "enfant-m|Oui, papa.",
            "narrateur|Aniss pose le ruban, près de la radio.",
            "enfant-m|Le rouge sent le bois.",
            "maman|Tu le sens, le bois ?",
            "enfant-m|Oui, maman.",
            "papa|Le rond reste un peu, de travers.",
            "enfant-m|Il a tenu, pendant la chanson.",
            "enfant-f|Le ruban est resté.",
            "narrateur|La radio fait un petit souffle.",
            "narrateur|Le ruban rouge fait de l'ombre.",
            "enfant-m|On y retourne, après.",
            "narrateur|Un éclat de commode tient sur le bois.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-m", "enfant-f"):
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
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine (Sarah = enfant-f)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m", "enfant-f") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "enfant-m" for r in roles):
        raise SystemExit(f"{SID}: Aniss absent (enfant-m)")
    if not any(r == "enfant-f" for r in roles):
        raise SystemExit(f"{SID}: Sarah absente (enfant-f)")
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
        "ils jouent",
        "il faut attendre",
        "on doit demander",
        "il faut demander",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Sarah a de l'énergie. Que peut-on faire ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != "jouer | attendre | un adulte | demander":
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "On peut jouer, attendre, ou demander à un adulte. Que fait Aniss ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    sarah_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("enfant-f|")
    ).lower()
    if "attends" not in sarah_txt:
        raise SystemExit(f"{SID}: Sarah sans attends")
    if "radio" not in blob:
        raise SystemExit(f"{SID}: manque radio")
    if "commode" not in blob:
        raise SystemExit(f"{SID}: manque commode")
    if "ruban" not in blob:
        raise SystemExit(f"{SID}: manque ruban")
    if "chanson" not in blob:
        raise SystemExit(f"{SID}: manque chanson")
    if "chaise" in blob:
        raise SystemExit(f"{SID}: chaise (BAN)")
    if "poussière" in blob or "poussiere" in blob:
        raise SystemExit(f"{SID}: poussière (BAN)")
    for ban in (
        "éclat de ruban",
        "éclat de radio",
        "éclat de bouton",
        "éclat de chaise",
        "éclat de poussière",
        "éclat de poussiere",
        "éclat de tapis",
        "éclat de lacet",
        "éclat de sauge",
        "éclat de chiffon",
        "éclat de bol",
        "éclat de flaque",
        "éclat de piquet",
        "tout doux",
        "tout calme",
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
        "- **Leçon :** DIF.ENE.001 — l'énergie de Sarah (vécue : elle saute "
        "trop, le ruban s'enroule, Aniss refuse de foncer, attend, demande, "
        "passe le ruban sans se presser). JAMAIS dite dans le récit. "
        "Pas « ce n'est pas une faute ». Pas « on peut jouer / attendre / "
        "demander ».\n"
        "- **Personnages :** Aniss, Sarah, papa, maman. Aniss = enfant-m "
        "(propose, trop vite, puis refuse de foncer). Sarah = enfant-f "
        "(énergie, saute, attends, silence). Troupe D16. Pas de maîtresse. "
        "Bruno / Noé du dump remplacés.\n"
        "- **Lieu :** salon, radio sur la commode, chanson, ruban rouge, "
        "linge, clic du bois. ≠ 001-01 flaque / 001-02 piquet / 001-03 bol. "
        "≠ 001-04 chiffon / 001-05 sauge / 001-06 lacet / 001-07 tapis. "
        "Pas poussière, pas chaise.\n"
        "- **Indice unique :** éclat de commode (brille à l'ouverture sous "
        "la radio → tremble au pied → luit au refus → tient sur le bois). "
        "BAN éclat de ruban / radio / bouton / chaise / poussière / tapis / "
        "lacet / sauge / chiffon / bol / flaque / piquet.\n"
        "- **Question moteur :** « Sarah a de l'énergie. Que peut-on "
        "faire ? » expected **jouer**. accepted `jouer | attendre | un "
        "adulte | demander`. retry dump (label). Non récitée dans les "
        "autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le bois de la commode fait clic, sous la radio. Sur le bois, un "
        "éclat de commode brille. Ruban rouge, chanson, linge. Aniss veut "
        "un grand rond **maintenant**, pendant la chanson. Sarah saute trop, "
        "le ruban s'enroule au pied, la radio penche. Sourire parti. Papa "
        "s'accroupit. Il refuse de foncer. Ils passent le ruban, puis "
        "tournent. Merci vécu. Deuxième ruse : clic, ruban trop vite vers "
        "la radio. Il s'arrête, lit l'éclat. Un éclat de commode tient sur "
        "le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon, radio sur la commode, chanson, ruban rouge, "
        "linge, clic du bois. ≠ 001-01 flaque / 001-02 piquet / 001-03 bol. "
        "Pas poussière / chaise.\n"
        "- Désir : un grand rond lent, maintenant, pendant la chanson.\n"
        "- Objet : ruban rouge, radio, commode.\n"
        "- Indice unique : éclat de commode, vu dès l'ouverture, payé sur "
        "le bois. Pas éclat de ruban / radio / chaise / poussière.\n"
        "- Urgence douce : la chanson joue, le rond doit tenir pendant.\n"
        "- Imprévu 1 : Sarah saute trop, tourne trop vite, le ruban "
        "s'enroule au pied, la radio penche.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« d'accord ».\n"
        "- Imprévu 2 (plus rusé) : clic, ruban trop vite, il penche vers "
        "la radio.\n"
        "- Résolution : il refuse de foncer, observe, écoute le clic, "
        "retrouve l'éclat, Sarah tend les mains.\n"
        "- Retour : ruban près de la radio, chanson arrêtée, éclat sur "
        "le bois.\n\n"
        "## Vécu\n\n"
        "Aniss veut le rond **maintenant**. Impatience, puis ruban "
        "enroulé, sourire parti. Sarah prend son élan, pose sa limite "
        "(attends, silence). Papa se baisse, pose une question, ne "
        "récite pas la règle. Ils agissent : le ruban passé, puis le "
        "rond lent. Merci vécu. Fin : l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le ruban rouge (noyau dump « Le ruban dans le rayon », "
        "sans poussière / chaise). Relance : Que peut-on faire ? expected "
        "jouer.\n"
        "- Lieu du dump (salon, radio, musique) sans rayon de poussière "
        "ni chaise. Radio sur la commode. Maman présente. Sarah = "
        "enfant-f.\n"
        "- Ouverture inventée (clic du bois sous la radio), pas un "
        "gabarit v2, pas « La radio craque, puis trouve une chanson » du "
        "dump en première ligne.\n"
        "- Indice unique : éclat de commode. BAN éclat de ruban / radio / "
        "bouton / chaise / poussière / tapis / lacet / sauge / chiffon / "
        "bol / flaque / piquet. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout bas » / « encore » du dump.\n"
        "- Leçon non dite : on la voit quand le ruban s'enroule, quand "
        "Aniss s'arrête, quand ils passent à tour. Pas « ce n'est pas une "
        "faute ». Pas « on peut jouer / attendre / demander » hors "
        "retry label.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Sarah a de l'énergie. Que "
        "peut-on faire ? ». expected jouer. retry dump. 5 chunks, kinds "
        "inchangés.\n"
        "- example4 022 / 054 / 086 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_ene_001_03.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le ruban trop vite.\n"
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
