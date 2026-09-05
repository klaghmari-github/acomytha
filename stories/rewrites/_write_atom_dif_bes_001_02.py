#!/usr/bin/env python3
"""ATOM-DIF.BES.001-02 — F-NAR-019. La boule de pâte d'Amir. N3. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.001-02"
N3 = LIMITS["N3"]
TITLE = "La boule de pâte d'Amir"
INDICE = "éclat de boule"
FIL = (
    "Le robinet de l'atelier fait tic. Une goutte ronde tombe. "
    "Sur une petite boule, un éclat de boule brille. Amir veut "
    "sa boule ronde, maintenant, près de la vitre. Il serre trop "
    "fort : la pâte s'écrase, l'éclat saute. Il refuse de foncer, "
    "regarde, roule le même geste. Merci vécu. À la maison, une "
    "boule file vers la vitre. L'éclat de boule tient."
)
CHARS = "Amir, papa, maman"
SETTING = (
    "atelier de pâte à l'école, table près de la fenêtre, "
    "cuisine à la maison"
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
    r"\b(carte|cartes|panier|dorure|poire|sac|cloche|corbeille|"
    r"croissant|réverbère|reverbere|bâche|bache|volet|farine|"
    r"léo|leo|amina|victorina|escargot|spirale|arrosoir)\b",
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
    "tu as su répéter",
    "observer d'abord, c'est possible",
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
        emphasis="éclat de boule",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_sa_boule_ronde_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="calme",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_regarde_puis_roule_le_meme_geste; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="même geste",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_regarde_puis_roule_pareil; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="boule",
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
        emphasis="éclat de boule",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_pate; "
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
    "narrateur|Le robinet de l'atelier fait tic.",
    "narrateur|Une goutte tombe dans l'évier.",
    "narrateur|Elle est ronde, presque.",
    "narrateur|Dehors, la cour sent la terre mouillée.",
    "narrateur|La vitre a des traces de pluie.",
    "narrateur|Amir pose les mains sur la table.",
    "narrateur|L'atelier sent le bois mouillé.",
    "maman|Tu as vu la cour, par la vitre ?",
    "enfant-m|Elle est mouillée.",
    "enfant-m|Ça sent la terre.",
    "papa|On reste un moment, ici.",
    "narrateur|La table est froide, un peu collante.",
    "narrateur|Un tas de pâte attend au milieu.",
    "narrateur|Au bord, une poudre blanche dort.",
    "narrateur|Une planche de bois attend sous la vitre.",
    "narrateur|Une petite boule repose près du tas.",
    "narrateur|Sur la boule, un éclat de boule brille.",
    "enfant-m|Il est blanc, maman.",
    "maman|Tu le vois sur la pâte ?",
    "enfant-m|Oui, il brille.",
    "papa|C'est une boule de pâte.",
    "enfant-m|Je veux la mienne, maintenant !",
    "maman|Tes mains, Amir.",
    "maman|On les passe sous l'eau.",
    "enfant-m|L'eau est froide.",
    "papa|Comme la pâte.",
    "enfant-m|Je veux une boule ronde.",
    "maman|Tu la veux ronde ?",
    "enfant-m|Ronde comme la goutte.",
    "papa|Près de la fenêtre, elle peut sécher.",
    "enfant-m|Oui, près de la vitre.",
    "narrateur|En ce moment, Amir prend la pâte.",
    "narrateur|Il en arrache un gros morceau.",
    "narrateur|Ses paumes ferment trop fort.",
    "narrateur|La pâte s'écrase entre les doigts.",
    "narrateur|Elle devient plate, avec une fente.",
    "enfant-m|Ça ne veut pas.",
    "narrateur|L'éclat de boule saute près de la poudre.",
    "narrateur|Le sourire d'Amir disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Papa s'accroupit à la même hauteur.",
    "papa|Tu veux la boule ronde ?",
    "enfant-m|Oui, papa.",
    "maman|Tes mains sont collantes ?",
    "enfant-m|Oui, maman.",
    "papa|Tu tiens ma manche ?",
    "enfant-m|Oui.",
    "narrateur|Amir veut recommencer tout de suite.",
    "narrateur|Ses doigts foncent vers le tas.",
    "narrateur|La pâte plate reste là, fendue.",
    "enfant-m|Je la veux maintenant !",
]

Q0001 = [
    "narrateur|Amir a besoin de calme.",
    "narrateur|Que peut-on faire ?",
]

C0001 = [
    "narrateur|Amir ouvre les mains trop vite.",
    "narrateur|Il veut coller la pâte plate.",
    "narrateur|Les bords se déchirent.",
    "enfant-m|Oh.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Il pose les paumes à plat.",
    "narrateur|Le morceau fendu reste sous ses yeux.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Il écoute le tic du robinet.",
    "narrateur|Un petit morceau se détache.",
    "narrateur|Les paumes roulent la pâte.",
    "narrateur|Amir s'arrête, il regarde.",
    "enfant-m|Une boule.",
    "enfant-m|Puis je regarde.",
    "narrateur|Il roule le même geste.",
    "narrateur|La pâte devient ronde, peu à peu.",
    "narrateur|Sur sa boule, l'éclat de boule revient.",
    "maman|Elle est ronde, Amir ?",
    "enfant-m|Comme la goutte.",
    "papa|Merci, Amir.",
    "narrateur|Papa a regardé jusqu'au bout.",
    "narrateur|Amir pose la boule sur la planche.",
    "narrateur|La planche est sous la vitre.",
    "maman|On rentre ?",
    "enfant-m|La boule vient avec nous.",
    "maman|Je la porte, à deux mains.",
    "enfant-m|Pas trop vite.",
    "narrateur|Dehors, le chemin sent la terre mouillée.",
    "narrateur|La pluie a laissé des ronds.",
    "enfant-m|Des gouttes, papa.",
    "papa|Des ronds, comme ta boule.",
    "narrateur|La boule reste ronde, contre la paume.",
    "narrateur|À la maison, la cuisine est tiède.",
    "papa|La porte, Amir.",
    "papa|Je la pousse.",
    "enfant-m|La cuisine sent le bois.",
    "narrateur|Maman pose la boule près de la vitre.",
    "maman|Tu veux de l'eau ?",
    "enfant-m|Oui, maman.",
    "narrateur|Papa pose un tas de pâte sur la table.",
    "enfant-m|Je veux une autre, maintenant !",
    "narrateur|Le ventre d'Amir se desserre.",
]

END = [
    "narrateur|Amir veut la deuxième boule, d'un coup.",
    "narrateur|Il pousse la pâte trop vite.",
    "narrateur|La boule file vers le bord.",
    "enfant-m|Ça roule !",
    "narrateur|Elle s'arrête près de la vitre.",
    "narrateur|Amir veut la rattraper, d'un coup.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Ses épaules se serrent un peu.",
    "narrateur|Ça tape, dans sa poitrine.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Il regarde la boule au bord.",
    "narrateur|La cuisine fait tic, un instant.",
    "narrateur|Le robinet de la maison répond.",
    "enfant-m|Comme à l'atelier, papa !",
    "papa|Tu l'entends, toi ?",
    "enfant-m|Oui, le tic.",
    "narrateur|Amir regarde la première boule.",
    "narrateur|Elle est ronde, près de la vitre.",
    "narrateur|Amir reprend la pâte, plus lentement.",
    "narrateur|Il roule le même geste.",
    "narrateur|Il s'arrête, il regarde.",
    "narrateur|La deuxième boule tient, ronde.",
    "maman|Les deux sont près de la vitre ?",
    "enfant-m|Oui, maman.",
    "papa|Tes pieds sont sous la table ?",
    "enfant-m|Oui, papa.",
    "narrateur|Il s'assoit au bord de la chaise.",
    "narrateur|Les deux boules se tiennent.",
    "narrateur|Le tic continue, petit.",
    "papa|Le tic est là.",
    "enfant-m|Les boules, elles, restent.",
]

FIN = [
    "narrateur|Ils restent près de la table.",
    "narrateur|Les deux boules reposent près de la vitre.",
    "enfant-m|L'éclat est là, papa.",
    "papa|Tu le vois sur la pâte ?",
    "enfant-m|Oui, papa.",
    "maman|On est bien, ici.",
    "narrateur|La vitre fait un rond, plus petit.",
    "narrateur|La cuisine sent la terre, un peu.",
    "enfant-m|Elle est ronde, ma boule.",
    "maman|Elle est ronde, Amir.",
    "enfant-m|Oui, maman.",
    "narrateur|Amir pose la joue près de la pâte.",
    "narrateur|La pâte est froide, un peu.",
    "enfant-m|C'est froid.",
    "papa|Tu le sens sur tes joues ?",
    "enfant-m|Oui, elle est froide.",
    "narrateur|La première boule porte une trace de paume.",
    "narrateur|Dehors, la cour s'endort.",
    "narrateur|L'éclat de boule tient sur la pâte.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "pate,robinet,goutte",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "répéter",
                    "accepted_examples": (
                        "répéter | observer d'abord | observer | attendre | "
                        "répéter la règle"
                    ),
                    "retry_prompt": (
                        "On peut répéter. On peut observer d'abord. Que fait Amir ?"
                    ),
                    "engine_ok_text": "Oui, on répète.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "pate",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "pate,table",
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
    for bad_name in ("brice", "ninon", "léo", "leo", "amina", "victorina"):
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
    if qtext != "Amir a besoin de calme. Que peut-on faire ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "répéter":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt") or ""
    if "victorina" in retry.lower() or "amina" in retry.lower():
        raise SystemExit(f"{SID}: retry 2e enfant")
    if "amir" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans Amir")
    if "répéter" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans répéter")

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
        "- **Leçon :** DIF.BES.001 — besoin de calme / répéter / observer "
        "d'abord (vécue : serrer trop fort → pâte plate ; regarder, "
        "roule le même geste ; à la maison, boule qui file → même geste)\n"
        "- **Personnages :** Amir, papa, maman. Dump Léo, Amina → INTERDIT. "
        "Dump / xlsx Victorina → INTERDIT (pas de 2e enfant). Troupe D16.\n"
        "- **Lieu :** atelier de pâte à l'école, table près de la fenêtre, "
        "poudre blanche au bord (pas indice), terre mouillée, cuisine à "
        "la maison. Distinct 001-01 cartes/école.\n"
        "- **Indice unique :** éclat de boule (petite boule du matin → "
        "saute près de la poudre → revient sur sa boule → tient à la fin)\n"
        "- **Question moteur :** Amir a besoin de calme. Que peut-on faire ? "
        "→ répéter. retry : Que fait Amir ?\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le robinet de l'atelier fait tic. Une goutte ronde tombe. La cour "
        "sent la terre mouillée. Sur une petite boule, un éclat de boule "
        "brille. Amir veut sa boule ronde **maintenant**, près de la vitre, "
        "comme la goutte. Il arrache trop, serre trop : la pâte s'écrase, "
        "une fente, l'éclat saute. Sourire parti, épaules basses. Papa "
        "s'accroupit. Il veut recommencer tout de suite. Question. Il colle "
        "trop vite : les bords se déchirent. Il refuse de foncer, écoute le "
        "tic, regarde, roule le même geste. L'éclat revient. Merci vécu. "
        "Maman porte la boule à deux mains. À la maison, un tas de pâte. "
        "Il pousse trop vite : la boule file vers la vitre. Il refuse, "
        "écoute le tic, regarde la première, roule le même geste. L'éclat "
        "de boule tient. Trace de paume.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : atelier, robinet tic, goutte ronde, terre mouillée, "
        "vitre de pluie, table froide, poudre blanche au bord, planche.\n"
        "- Désir : une boule ronde comme la goutte, à sécher près de la "
        "vitre, maintenant.\n"
        "- Objet : pâte, boule, planche, vitre, robinet.\n"
        "- Indice unique : éclat de boule, vu dès l'ouverture, payé à la "
        "fin.\n"
        "- Urgence douce : la goutte est ronde, la vitre attend la boule.\n"
        "- Imprévu 1 : il serre trop ; la pâte s'écrase, l'éclat saute.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : pousser d'un coup ; la boule file vers "
        "le bord de la vitre.\n"
        "- Résolution : il refuse de foncer, regarde, roule le même geste.\n"
        "- Retour : deux boules près de la vitre, éclat du début, trace "
        "de paume.\n\n"
        "## Vécu\n\n"
        "Amir veut sa boule ronde **maintenant**. Impatience, puis épaules "
        "qui tombent quand la pâte s'écrase. Papa s'accroupit, pose une "
        "question, ne récite pas la règle. Amir agit : paumes à plat, "
        "regard, même geste. Merci vécu après le regard jusqu'au bout. "
        "Fin : l'éclat du début tient sur la pâte, près de la vitre.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre mission « La boule de pâte d'Amir » (xlsx : « L'escargot "
        "de pâte d'Amir »). Monde dump : école puis maison, table de pâte, "
        "poudre blanche au bord (pas indice — ban éclat de farine), terre "
        "mouillée, fenêtre.\n"
        "- Héros Amir. Dump Léo, Amina → INTERDIT. Victorina dump/xlsx → "
        "INTERDIT. Un héros + papa/maman.\n"
        "- Question dump « Victorina a besoin de calme » → « Amir a "
        "besoin de calme. Que peut-on faire ? ». expected répéter.\n"
        "- Ouverture inventée (robinet tic, goutte ronde), pas « joue au "
        "salon », pas gabarit v2, pas escargot/spirale/cartes.\n"
        "- Distinct de DIF.BES.001-01 cartes/tortue/tapis/école.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent / "
        "tout bas » retirés. Pas de merle, pas de miel, pas de secret.\n"
        "- Ban : carte, panier, dorure, poire, sac, cloche, corbeille, "
        "croissant, réverbère, bâche, volet, farine.\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- Indice unique « éclat de boule » nommé à l'ouverture, revu "
        "quand il saute, revu sur sa boule, payé à la fin.\n"
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
