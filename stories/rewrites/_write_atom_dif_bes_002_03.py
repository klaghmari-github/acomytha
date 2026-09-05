#!/usr/bin/env python3
"""ATOM-DIF.BES.002-03 — F-NAR-019. Les raisins du gâteau. N3. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.002-03"
N3 = LIMITS["N3"]
TITLE = "Les raisins du gâteau"
INDICE = "éclat de grille"
FIL = (
    "Le four rend un nuage de vanille. Un petit gâteau repose sur la "
    "grille. Sur un fil, un éclat de grille brille. Amir veut un rond "
    "de raisins, maintenant, avec Sarah. Il tend trop vite : le raisin "
    "roule, l'éclat saute. Il refuse de foncer, propose, accepte je "
    "regarde. Merci vécu. Au balcon, le gâteau glisse. Il attend. Sarah "
    "pose un raisin, s'arrête. L'éclat de grille tient."
)
CHARS = "Amir, Sarah, papa, maman"
SETTING = (
    "cuisine puis balcon, vanille, gâteau sur grille, raisins"
)
TIC_PHRASES = (
    "tout doux",
    "tout calme",
    "tout lent",
    "tout bas",
    "tout doucement",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)
BAN_WORDS = re.compile(
    r"\b(plaque|pierre|boule|carte|galet|cube|bois|farine|"
    r"panier|dorure|poire|sac|cloche|corbeille|"
    r"croissant|réverbère|reverbere|bâche|bache|volet|"
    r"léo|leo|amina|victorina|nino|escargot|spirale|arrosoir|"
    r"cheval|pont)\b",
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
    "ninon",
    "brice",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai proposé",
    "j'ai propose",
    "j'ai accepté",
    "j'ai accepte",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "on range les feutres",
    "tu ranges",
    "tu as bien écouté",
    "tu as bien ecoute",
    "tu as fait du bon travail",
    "c'est du bon travail",
    "tu as bien fait",
    "bon travail",
    "une chose, puis",
    "une chose puis",
    "il faut attendre",
    "tu attends ton tour",
    "c'est ton tour",
    "on doit demander",
    "il faut demander",
    "tu as attendu",
    "tu as su proposer",
    "tu as su accepter",
    "plusieurs réponses",
    "plusieurs reponses",
    "regarder, c'est une réponse",
    "regarder, c'est une reponse",
    "on peut proposer",
    "on peut accepter",
    "même leçon",
    "même règle",
    "c'est la règle",
    "tu peux dire la règle",
    "comme un secret",
    "gouttière",
    "gouttiere",
    "croûte",
    "croute",
    "casier",
    "moufle",
    "craie",
    "cartable",
    "pinceau",
    "casserole",
    "grain de",
    "éclat de farine",
    "éclat de plaque",
    "éclat de pierre",
    "éclat de boule",
    "éclat de carte",
    "éclat de galet",
    "éclat de cube",
    "éclat de bois",
    "éclat de page",
    "éclat de carotte",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de terre",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de marche",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de tasse",
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de laine",
    "éclat de orange",
    "éclat de lampe",
    "éclat de citron",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de pin",
    "éclat de crayon",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de craie",
    "éclat de tapis",
    "éclat de moufle",
    "éclat de casier",
    "éclat de tableau",
    "éclat de cartable",
    "éclat de pinceau",
    "éclat de crochet",
    "éclat de buée",
    "éclat de buee",
    "éclat de corbeille",
    "éclat de croissant",
    "éclat de poire",
    "éclat de sac",
    "éclat de cloche",
    "éclat de volet",
    "éclat de bâche",
    "éclat de bache",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "lune d'étain",
    "lune d'etain",
    "trois notes",
    "lumière couleur de miel",
    "lumiere couleur de miel",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de grille",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_rond_avec_sarah_maintenant; "
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
            "sous_texte=inviter_c_est_proposer_sans_forcer; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="D'accord",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_propose_puis_accepte_je_regarde; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="raisin",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_rattraper_trop_vite; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de grille",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_fil; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}


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


def vet(lines: list[str]) -> list[str]:
    out = []
    starts: list[str] = []
    for raw in lines:
        role, ph = raw.split("|", 1)
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
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"tic {tic!r}: {ph}")
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"tic {m.group(0)!r}: {ph}")
        b = BAN_WORDS.search(low)
        if b:
            raise SystemExit(f"interdit {b.group(0)!r}: {ph}")
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad!r}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"interdit {bad!r}: {ph}")
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


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    lines = vet(lines)
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


P0000 = [
    "narrateur|Le four rend un nuage de vanille.",
    "narrateur|Le nuage s'étale sur la vitre.",
    "narrateur|La vitre donne sur le balcon.",
    "narrateur|L'air du balcon entre, plus frais.",
    "maman|Tu as senti la vanille, Amir ?",
    "enfant-m|Oui, maman.",
    "enfant-m|C'est sucré.",
    "papa|On reste un moment, ici.",
    "narrateur|La table est tiède, un peu collante.",
    "narrateur|Un petit gâteau repose sur la grille.",
    "narrateur|La grille fait un tic, très fin.",
    "narrateur|Sur un fil, un éclat de grille brille.",
    "enfant-m|Il est blanc, maman.",
    "maman|Tu le vois sur le fil ?",
    "enfant-m|Oui, il brille.",
    "papa|C'est la grille du gâteau.",
    "enfant-m|Je veux un rond, maintenant !",
    "maman|Tes mains, Amir.",
    "maman|On les passe sous l'eau.",
    "enfant-m|L'eau est tiède.",
    "papa|Comme le gâteau.",
    "enfant-m|Un rond de raisins.",
    "maman|Tu le veux autour ?",
    "enfant-m|Oui, autour.",
    "papa|Près de la vanille, il peut reposer.",
    "enfant-m|Oui, près de la grille.",
    "narrateur|Un bol de raisins attend au milieu.",
    "narrateur|Les raisins sont sombres, un peu collants.",
    "papa|Les raisins sont prêts.",
    "papa|Le gâteau aussi.",
    "maman|On décore un peu ?",
    "enfant-m|D'accord.",
    "narrateur|En ce moment, Amir tient un raisin.",
    "narrateur|Il est collant, entre deux doigts.",
    "narrateur|Maman ouvre la porte.",
    "narrateur|Sarah arrive.",
    "narrateur|Elle a une barrette bleue.",
    "enfant-m|Tu viens ?",
    "enfant-m|Le rond, maintenant !",
    "copine|Non.",
    "narrateur|Amir tend le raisin trop vite.",
    "narrateur|Le raisin glisse sous le bol.",
    "enfant-m|Il est parti.",
    "narrateur|L'éclat de grille saute près du bol.",
    "narrateur|Le sourire d'Amir disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Papa s'accroupit à la même hauteur.",
    "papa|Tu veux le rond avec Sarah ?",
    "enfant-m|Oui, papa.",
    "maman|Tes doigts sont collants ?",
    "enfant-m|Oui, maman.",
    "papa|Tu tiens ma manche ?",
    "enfant-m|Oui.",
    "narrateur|Amir veut recommencer tout de suite.",
    "narrateur|Ses doigts foncent vers Sarah.",
    "enfant-m|Je veux qu'elle pose un raisin !",
]

Q0001 = [
    "narrateur|Amir invite Sarah.",
    "narrateur|Que fait-on ?",
]

C0001 = [
    "narrateur|Amir pousse le raisin vers la main de Sarah.",
    "narrateur|Le raisin colle à son doigt.",
    "copine|Non.",
    "narrateur|Sarah retire la main.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Il pose le raisin près du bol.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Il écoute le tic de la grille.",
    "narrateur|Il regarde le gâteau, puis Sarah.",
    "narrateur|Sur un fil, l'éclat de grille revient.",
    "enfant-m|Tu as vu le gâteau, Sarah ?",
    "copine|Je regarde.",
    "narrateur|Sarah s'assoit près du buffet.",
    "narrateur|Elle regarde le rond, sans bouger.",
    "enfant-m|D'accord.",
    "narrateur|Amir penche le bol.",
    "narrateur|Le raisin revient, collant.",
    "narrateur|Il pose un raisin sur le gâteau.",
    "narrateur|Le rond a trois raisins.",
    "maman|Il en manque, hein ?",
    "enfant-m|Oui.",
    "enfant-m|Tu veux un raisin ?",
    "copine|Plus tard.",
    "enfant-m|D'accord.",
    "papa|Merci, Amir.",
    "narrateur|Papa a regardé jusqu'au bout.",
    "maman|On sort un moment ?",
    "enfant-m|Le gâteau vient avec nous.",
    "papa|Je porte la grille, à deux mains.",
    "enfant-m|Pas trop vite.",
    "narrateur|Le ventre d'Amir se desserre.",
]

END = [
    "narrateur|Au balcon, l'air est frais.",
    "narrateur|La vanille suit, plus légère.",
    "narrateur|Papa pose la grille sur la table.",
    "narrateur|Une jardinière sent la terre.",
    "enfant-m|Le rond, Sarah !",
    "narrateur|Amir veut le dernier raisin, d'un coup.",
    "narrateur|Il pousse le bol trop vite.",
    "narrateur|Un raisin file vers le bord.",
    "enfant-m|Ça roule !",
    "narrateur|Le gâteau glisse d'un fil.",
    "enfant-m|Oh.",
    "narrateur|Amir veut le rattraper, d'un coup.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Ses épaules se serrent un peu.",
    "narrateur|Ça tape, dans sa poitrine.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Il regarde la grille, il écoute le balcon.",
    "narrateur|Un oiseau passe, loin.",
    "enfant-m|Tu poses celui-là ?",
    "narrateur|Sarah ne dit rien.",
    "narrateur|Elle garde les mains sur ses genoux.",
    "enfant-m|D'accord.",
    "narrateur|Amir attend.",
    "copine|Plus tard.",
    "enfant-m|Oui.",
    "narrateur|Le gâteau se cale, sans glisser.",
    "narrateur|Sarah avance un doigt.",
    "narrateur|Elle pose un raisin, puis s'arrête.",
    "enfant-m|D'accord.",
    "narrateur|Amir pose le dernier raisin.",
    "enfant-m|Il est rond, papa.",
    "papa|Tu le vois, autour ?",
    "enfant-m|Oui.",
    "maman|Tes pieds sont sous la table ?",
    "enfant-m|Oui, maman.",
    "papa|Le tic est là.",
    "enfant-m|Le rond, lui, reste.",
]

FIN = [
    "narrateur|Ils restent près de la table.",
    "narrateur|Le gâteau a son rond de raisins.",
    "enfant-m|L'éclat est là, papa.",
    "papa|Tu le vois sur le fil ?",
    "enfant-m|Oui, papa.",
    "maman|On est bien, ici.",
    "narrateur|La vanille reste, plus légère.",
    "enfant-m|Il est rond, mon gâteau.",
    "maman|Il est rond, Amir.",
    "enfant-m|Oui, maman.",
    "narrateur|Amir pose la joue près de la grille.",
    "narrateur|La grille est tiède, un peu.",
    "enfant-m|C'est tiède.",
    "papa|Tu le sens sur tes joues ?",
    "enfant-m|Oui, elle est tiède.",
    "narrateur|Un raisin porte une trace de doigt.",
    "narrateur|Dehors, le balcon s'endort.",
    "narrateur|L'éclat de grille tient sur le fil.",
]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    wanted = {
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_Q0001",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    }
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in wanted]
    if missing:
        raise SystemExit(f"{SID} chunks inattendus: {missing}")

    by = {
        "CHK_T0000_P0000": voice(
            by_src["CHK_T0000_P0000"], P0000, "opening", "four,vanille,grille",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "proposer",
                    "accepted_examples": (
                        "proposer | inviter | accepter | d'accord"
                    ),
                    "retry_prompt": (
                        "On peut proposer. On peut inviter. Que fait Amir ?"
                    ),
                    "engine_ok_text": "Oui, on propose.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "raisins,grille",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "balcon",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    for bad_name in ("brice", "ninon", "léo", "leo", "amina", "victorina", "nino"):
        if re.search(rf"\b{bad_name}\b", blob):
            raise SystemExit(f"{SID}: {bad_name} interdit")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    tts_ok = all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_xai_tags"] != c["text"]
        and str(c["text_ssml"]).startswith("<speak>")
        for c in chunks
    )
    if not tts_ok:
        raise SystemExit(f"{SID}: TTS incomplet")
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
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Amir invite Sarah. Que fait-on ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "proposer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt") or ""
    if "victorina" in retry.lower() or "amina" in retry.lower():
        raise SystemExit(f"{SID}: retry 2e enfant dump")
    if "amir" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans Amir")
    if "proposer" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans proposer")
    if "plaque" in blob or "éclat de plaque" in blob:
        raise SystemExit(f"{SID}: collision 002-01 plaque")
    kinds = {c["chunk_id"]: by_src[c["chunk_id"]].get("kind") for c in src["chunks"]}
    for c in chunks:
        if c.get("kind") != kinds[c["chunk_id"]]:
            raise SystemExit(f"{SID}: kind altéré {c['chunk_id']}")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nwords = sum(words(c["text"]) for c in chunks)
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N3 (5–6 ans), audio familial, ≤16 mots/phrase\n"
        "- **Leçon :** DIF.BES.002 — inviter / proposer / accepter (vécue : "
        "Amir tend trop vite, Sarah dit non ; il propose « tu as vu le "
        "gâteau », accepte « je regarde » et « plus tard » ; au balcon, "
        "il attend le silence, elle pose un raisin puis s'arrête)\n"
        "- **Personnages :** Amir, Sarah, papa, maman. Troupe D16. Sarah "
        "= copine (rythme lent, limites). Pas Nino, pas Victorina.\n"
        "- **Lieu :** cuisine puis balcon, vanille, gâteau sur grille, "
        "raisins collants, jardinière. Distinct 002-01 cheval/pont, "
        "éclat de plaque.\n"
        "- **Indice unique :** éclat de grille (fil du matin → saute près "
        "du bol → revient sur un fil → tient à la fin)\n"
        "- **Question moteur :** Amir invite Sarah. Que fait-on ? → "
        "proposer. retry : Que fait Amir ?\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le four rend un nuage de vanille. La vitre donne sur le balcon. "
        "Un petit gâteau repose sur la grille. Sur un fil, un éclat de "
        "grille brille. Amir veut un rond de raisins **maintenant**, avec "
        "Sarah. Il tend trop vite : elle dit non, le raisin roule, l'éclat "
        "saute. Sourire parti, épaules basses. Papa s'accroupit. Il veut "
        "lui mettre le raisin dans la main. Question. Il pousse trop vite : "
        "elle retire la main. Il refuse de foncer, écoute le tic, retrouve "
        "l'éclat, propose. Elle regarde. Merci vécu. Papa porte la grille "
        "au balcon. Il pousse le bol : le gâteau glisse. Il refuse, attend "
        "le silence. Elle pose un raisin, s'arrête. Il accepte, pose le "
        "dernier. L'éclat de grille tient. Trace de doigt.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : four, vanille sur la vitre, air du balcon, table tiède, "
        "grille qui tique, raisins collants, barrette bleue.\n"
        "- Désir : un rond de raisins autour du gâteau, avec Sarah, "
        "maintenant.\n"
        "- Objet : gâteau, grille, fil, bol, raisins.\n"
        "- Indice unique : éclat de grille, vu dès l'ouverture, payé à la "
        "fin.\n"
        "- Urgence douce : le gâteau est tiède, Sarah vient d'arriver.\n"
        "- Imprévu 1 : il tend trop vite ; Sarah dit non ; le raisin roule ; "
        "l'éclat saute.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : pousser le bol ; le gâteau glisse d'un "
        "fil ; Sarah se tait.\n"
        "- Résolution : il refuse de foncer, propose, accepte je regarde, "
        "plus tard, le silence.\n"
        "- Retour : rond fini sur le balcon, éclat du début, trace de "
        "doigt.\n\n"
        "## Vécu\n\n"
        "Amir veut le rond **maintenant**, avec Sarah. Impatience, puis "
        "épaules qui tombent quand elle dit non. Papa s'accroupit, pose une "
        "question, ne récite pas la règle. Amir agit : il propose, accepte "
        "« je regarde », attend. Merci vécu après le regard jusqu'au bout. "
        "Fin : l'éclat du début tient sur le fil, près du rond.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre mission « Les raisins du gâteau ». Monde dump : cuisine "
        "puis balcon, vanille, gâteau sur grille, raisins. Pas arrosoir, "
        "pas pierre, pas cuillère de bois.\n"
        "- Héros Amir. Autre enfant D16 : Sarah (copine). Papa, maman. "
        "Pas Nino, pas Victorina (002-01).\n"
        "- Question dump conservée : « Amir invite Sarah. Que fait-on ? ». "
        "expected proposer.\n"
        "- Ouverture inventée (four, nuage de vanille, tic de grille), pas "
        "« joue au salon », pas gabarit v2, pas cheval/pont.\n"
        "- Distinct de DIF.BES.002-01 cheval/pont/éclat de plaque.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent / "
        "tout bas » retirés. Pas de merle, pas de miel, pas de secret.\n"
        "- Ban : plaque, pierre, boule, carte, galet, cube, bois, farine, "
        "panier, dorure, poire, sac, cloche, corbeille, croissant, "
        "réverbère, bâche, volet, arrosoir.\n"
        "- Leçon non dite : pas « tu as su proposer », pas « plusieurs "
        "réponses ». Vécue dans le geste.\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- Indice unique « éclat de grille » nommé à l'ouverture, revu "
        "quand il saute, revu sur un fil, payé à la fin.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive.\n"
        f"- {nwords} mots. N3 ≤ 16. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
