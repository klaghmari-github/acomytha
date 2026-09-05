#!/usr/bin/env python3
"""ATOM-DIF.COR.002-02 — F-NAR-019. Le cheval de bois sous la haie. N3. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.002-02"
N3 = LIMITS["N3"]
TITLE = "Le cheval de bois sous la haie"
INDICE = "éclat de buis"
FIL = (
    "Le chemin du village sent la poussière chaude. La haie de buis "
    "pique. Une abeille va d'une fleur à l'autre. Sur une feuille, un "
    "éclat de buis brille. Amir veut son cheval de bois, maintenant, "
    "sous la haie. Il écarte trop vite : le bois glisse, l'éclat saute. "
    "Victorino s'agenouille lentement. Un petit rire commence, puis "
    "s'arrête. Ils cherchent ensemble. Merci vécu. Sur la véranda, "
    "l'écurie d'argile s'affaisse. Amir refuse de foncer. L'éclat de "
    "buis tient."
)
CHARS = "Amir, Victorino, papa, maman"
SETTING = (
    "chemin du village puis véranda, haie de buis, poussière, abeille"
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
    r"biscuit|biscuits|citron|casserole|tablier|léo|leo|amina|"
    r"victorina|escargot|spirale|arrosoir)\b",
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
    "éclat de poussière",
    "éclat de poussiere",
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
    "éclat de boule",
    "éclat de cerceau",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "lune d'étain",
    "lune d'etain",
    "trois notes",
    "lumière couleur de miel",
    "lumiere couleur de miel",
    "corps plus rond",
    "corps plus mince",
    "formes différentes",
    "formes differentes",
    "l'amitié ne dépend",
    "l'amitie ne depend",
    "pas une blague",
    "n'est pas une blague",
    "n'est pas une blague",
    "vous jouez",
    "on joue",
    "on cuisine",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de buis",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis gêne; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_cheval_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="blague",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_rire_s_est_arrete_ils_cherchent_ensemble; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="écurie",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=ils_tiennent_la_branche_puis_l_argile; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de buis",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_rattraper_le_toit_trop_vite; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de buis",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_feuille; "
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


def vet(lines: list[str], *, allow_lesson: bool = False) -> list[str]:
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
        if not allow_lesson:
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
    lines = vet(lines, allow_lesson=bool(extra.get("allow_lesson")))
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
    "narrateur|Le chemin du village sent la poussière chaude.",
    "narrateur|La haie de buis est serrée, un peu piquante.",
    "narrateur|Une abeille va d'une fleur à l'autre.",
    "narrateur|Le portail de fer est tiède sous la main.",
    "papa|Tu as vu le portail, Amir ?",
    "enfant-m|Il est chaud.",
    "papa|Le soleil l'a touché.",
    "maman|La haie aussi.",
    "enfant-m|Elle pique un peu.",
    "narrateur|La poussière colle aux orteils.",
    "narrateur|Le buis sent le vert chaud.",
    "narrateur|Une feuille tremble au bord de la haie.",
    "narrateur|Sur la feuille, un éclat de buis brille.",
    "enfant-m|Il brille, papa.",
    "papa|Tu le vois, sur la feuille ?",
    "enfant-m|Oui, il brille.",
    "maman|C'est petit, cet éclat.",
    "narrateur|L'herbe est sèche, un peu dure.",
    "enfant-m|Mon cheval de bois.",
    "enfant-m|Il a roulé.",
    "maman|Sous la haie ?",
    "enfant-m|Oui, maman.",
    "enfant-m|Je le veux, maintenant !",
    "papa|On le cherche ?",
    "enfant-m|Oui, papa.",
    "narrateur|En ce moment, Amir cherche dans l'herbe.",
    "narrateur|Les tiges piquent ses paumes.",
    "narrateur|Il écarte une branche trop vite.",
    "narrateur|Le bois glisse plus loin, sous les feuilles.",
    "enfant-m|Il est parti !",
    "narrateur|L'éclat de buis saute près du portail.",
    "narrateur|Le sourire d'Amir disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Papa s'accroupit à la même hauteur.",
    "papa|Tu veux le cheval ?",
    "enfant-m|Oui, papa.",
    "maman|Tes genoux sont dans l'herbe ?",
    "enfant-m|Oui, maman.",
    "narrateur|Victorino arrive près du portail.",
    "narrateur|Il prend son temps, les pieds dans la poussière.",
    "copain|J'aide.",
    "enfant-m|Vite !",
    "narrateur|Victorino s'agenouille plus lentement.",
    "narrateur|Un petit rire commence, chez Amir.",
    "narrateur|Victorino baisse les yeux.",
    "narrateur|Ses épaules se serrent un peu.",
    "narrateur|Le rire s'arrête net.",
    "narrateur|Amir ferme la bouche.",
    "narrateur|Ses joues sont chaudes, un peu.",
    "enfant-m|On cherche le cheval ?",
    "narrateur|Victorino ne répond pas tout de suite.",
    "copain|On cherche.",
    "papa|Tu tiens la branche, Amir ?",
    "enfant-m|Oui.",
]

Q0001 = [
    "narrateur|Le corps n'est pas une blague.",
    "narrateur|Que fait-on ?",
]

C0001 = [
    "narrateur|Amir tend une branche vers Victorino.",
    "narrateur|Victorino la prend, sans se presser.",
    "enfant-m|Tu tiens ?",
    "copain|Oui.",
    "narrateur|Ils écartent les feuilles, ensemble.",
    "narrateur|Les feuilles sentent le vert.",
    "narrateur|Un caillou roule.",
    "enfant-m|Pas lui.",
    "copain|Plus bas.",
    "narrateur|Le bois du cheval apparaît.",
    "enfant-m|Te voilà.",
    "copain|Il a de la terre au nez.",
    "maman|On le lave, sur la véranda ?",
    "enfant-m|Oui, maman.",
    "papa|Je pousse le portail.",
    "narrateur|La véranda est à l'ombre, un peu froide.",
    "narrateur|Un bac d'eau attend près du banc.",
    "narrateur|Amir lave le cheval.",
    "narrateur|L'eau fait un filet brun.",
    "enfant-m|Il est propre.",
    "papa|Il a besoin d'une écurie ?",
    "enfant-m|Oui, maintenant !",
    "copain|On la fait.",
    "narrateur|L'argile attend sur une planche.",
    "narrateur|Elle est froide, un peu grise.",
    "narrateur|Amir dresse un mur trop vite.",
    "narrateur|Le mur s'affaisse, mou.",
    "enfant-m|Oh.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Il pose les paumes à plat.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Il écoute l'abeille, près de la haie.",
    "copain|Attends.",
    "narrateur|Victorino appuie de l'autre côté.",
    "narrateur|Les deux murs tiennent, un peu.",
    "enfant-m|Un toit ?",
    "copain|Pas trop vite.",
    "narrateur|Amir pose un toit plat.",
    "narrateur|Le cheval entre dans l'écurie.",
    "narrateur|Sa jambe de bois touche l'argile.",
    "copain|Il est à la maison.",
    "papa|Merci, Amir.",
    "narrateur|Papa a vu les deux mains sur l'argile.",
    "maman|Victorino, tu as vu le cheval ?",
    "copain|Oui.",
    "enfant-m|Il tient.",
    "narrateur|Le ventre d'Amir se desserre.",
]

END = [
    "narrateur|Amir veut le toit plus haut, d'un coup.",
    "narrateur|Il pousse l'argile trop vite.",
    "narrateur|Le toit glisse vers le bord.",
    "enfant-m|Ça tombe !",
    "narrateur|La jambe de bois s'enfonce un peu.",
    "copain|Attends.",
    "narrateur|Amir veut rattraper le toit, d'un coup.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Ses épaules se serrent un peu.",
    "narrateur|Ça tape, dans sa poitrine.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Il regarde la haie, par la véranda.",
    "enfant-m|L'éclat, papa ?",
    "papa|Tu le vois, toi ?",
    "enfant-m|Sur la feuille.",
    "narrateur|L'éclat de buis revient, sur la feuille.",
    "maman|Le cheval, Amir ?",
    "enfant-m|Oui.",
    "narrateur|Victorino tient le mur, sans parler.",
    "narrateur|Amir pose le toit, plus lentement.",
    "narrateur|La jambe de bois repose, droite.",
    "copain|Il tient.",
    "enfant-m|Il dort.",
    "papa|Tes mains sont propres ?",
    "enfant-m|Un peu d'argile, papa.",
    "maman|L'eau est tiède.",
    "narrateur|Ils se lavent les mains, près du bac.",
    "narrateur|Dehors, le portail reste tiède.",
    "enfant-m|L'abeille est là.",
    "papa|Près de la haie ?",
    "enfant-m|Oui, papa.",
]

FIN = [
    "narrateur|Ils restent près de la planche.",
    "narrateur|Le cheval de bois attend sous le toit.",
    "enfant-m|L'éclat est là, papa.",
    "papa|Tu le vois sur la feuille ?",
    "enfant-m|Oui, papa.",
    "maman|On est bien, ici.",
    "narrateur|Dehors, le chemin sent la poussière.",
    "narrateur|Une abeille passe près de la haie.",
    "enfant-m|Il est à la maison.",
    "maman|Il est à la maison, Amir.",
    "enfant-m|Oui, maman.",
    "narrateur|Amir pose la joue près du bois.",
    "narrateur|Le bois est froid, un peu.",
    "enfant-m|C'est froid.",
    "papa|Tu le sens sur tes joues ?",
    "enfant-m|Oui, il est froid.",
    "copain|Le nez a de la terre.",
    "narrateur|Le nez du cheval porte une trace.",
    "narrateur|La haie garde un peu de poussière.",
    "narrateur|L'éclat de buis tient sur la feuille.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "abeille,chemin,haie",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "allow_lesson": True,
                "fields": {
                    "expected_answer": "jouer",
                    "accepted_examples": (
                        "jouer | on joue | pas une blague | pas blague | "
                        "le cheval | l'écurie"
                    ),
                    "retry_prompt": "On joue. Que fait Amir ?",
                    "engine_ok_text": "Oui, on joue.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "eau,argile",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "argile",
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
    if "éclat de poussière" in blob or "eclat de poussiere" in blob:
        raise SystemExit(f"{SID}: éclat de poussière (BAN 001-07)")
    recit = "\n".join(
        c["script"]
        for c in chunks
        if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for slogan in (
        "pas une blague",
        "corps n'est pas",
        "corps n est pas",
        "on joue",
        "vous jouez",
        "corps plus rond",
        "corps plus mince",
    ):
        if slogan in recit:
            raise SystemExit(f"{SID}: récitation {slogan!r}")
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
    if "papa|" not in blob:
        raise SystemExit(f"{SID}: papa absent")
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Le corps n'est pas une blague. Que fait-on ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt") or ""
    if "victorino" in retry.lower() or "victorina" in retry.lower():
        raise SystemExit(f"{SID}: retry 2e enfant")
    if "amir" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans Amir")
    if "jouer" not in retry.lower() and "joue" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans jouer")

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
        "- **Leçon :** DIF.COR.002 — le corps n'est pas une blague / on "
        "joue (vécue : petit rire quand Victorino s'agenouille lentement "
        "; il baisse les yeux ; Amir ferme la bouche ; ils cherchent "
        "ensemble. Jamais dite dans le récit.)\n"
        "- **Personnages :** Amir, Victorino, papa, maman. Papa ajouté "
        "(dump : maman seulement). Troupe D16. Victorino = copain "
        "(rythme lent, « Attends », silence).\n"
        "- **Lieu :** chemin du village puis véranda, poussière, haie de "
        "buis, abeille, portail de fer, argile. Distinct 002-01 cuisine "
        "(biscuits, citron, casserole).\n"
        "- **Indice unique :** éclat de buis (brille à l'ouverture → saute "
        "près du portail → revient sur la feuille → tient à la fin). Pas "
        "éclat de poussière (BAN 001-07).\n"
        "- **Question moteur :** Le corps n'est pas une blague. Que "
        "fait-on ? → jouer. retry : Que fait Amir ?\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le chemin du village sent la poussière chaude. La haie de buis "
        "pique. Une abeille va d'une fleur à l'autre. Sur une feuille, un "
        "éclat de buis brille. Amir veut son cheval de bois **maintenant**, "
        "sous la haie. Il écarte trop vite : le bois glisse, l'éclat saute. "
        "Sourire parti, épaules basses. Papa s'accroupit. Victorino arrive, "
        "prend son temps. Un petit rire commence. Victorino baisse les "
        "yeux. Le rire s'arrête. Ils cherchent. Question. Branche tenue à "
        "deux. Cheval trouvé, lavé sur la véranda. Mur d'argile trop vite : "
        "il s'affaisse. Amir refuse de foncer. Merci vécu. Toit trop haut : "
        "la jambe s'enfonce. Il refuse, retrouve l'éclat. L'éclat de buis "
        "tient. Trace de terre au nez.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chemin, poussière chaude, haie de buis, abeille, "
        "portail tiède, feuille au bord.\n"
        "- Désir : le cheval de bois sous la haie, maintenant.\n"
        "- Objet : cheval de bois, haie, branche, argile, écurie.\n"
        "- Indice unique : éclat de buis, vu dès l'ouverture, payé à la "
        "fin.\n"
        "- Urgence douce : le cheval a roulé, l'herbe pique, maintenant.\n"
        "- Imprévu 1 : branche trop vite ; le bois glisse ; petit rire "
        "qui s'arrête.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : toit trop haut ; jambe de bois qui "
        "s'enfonce.\n"
        "- Résolution : il refuse de foncer, Victorino dit Attends, "
        "l'éclat revient.\n"
        "- Retour : cheval sous le toit, abeille, poussière, éclat du "
        "début, trace de terre.\n\n"
        "## Vécu\n\n"
        "Amir veut son cheval **maintenant**. Impatience, puis épaules "
        "qui tombent quand le bois glisse. Victorino s'agenouille "
        "lentement. Un petit rire commence. Victorino baisse les yeux, "
        "épaules serrées. Amir ferme la bouche, propose de chercher. "
        "Papa s'accroupit, pose une question de la scène, ne récite pas "
        "la leçon. Ils tiennent la branche. Merci vécu après les deux "
        "mains sur l'argile. Fin : l'éclat du début tient sur la feuille.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre mission « Le cheval de bois sous la haie ». Monde dump : "
        "chemin du village puis véranda, poussière, haie de buis, abeille. "
        "Pas éclat de poussière (BAN 001-07).\n"
        "- Héros Amir. Copain D16 Victorino. Papa ajouté. Maman. Troupe "
        "D16.\n"
        "- Question dump conservée : « Le corps n'est pas une blague. Que "
        "fait-on ? ». expected jouer. Pas de récitation dans le récit.\n"
        "- Ouverture inventée (poussière chaude, buis qui pique, éclat "
        "sur la feuille), pas « joue au salon », pas gabarit v2, pas "
        "cuisine 002-01.\n"
        "- Distinct de DIF.COR.002-01 cuisine / biscuits / citron / "
        "casserole.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent / "
        "tout bas » retirés. Pas de merle, pas de miel, pas de secret.\n"
        "- Ban : carte, panier, dorure, poire, sac, cloche, corbeille, "
        "croissant, réverbère, bâche, volet, farine, biscuits.\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- Indice unique « éclat de buis » nommé à l'ouverture, revu "
        "quand il saute, revu sur la feuille, payé à la fin.\n"
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
