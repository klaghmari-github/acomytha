#!/usr/bin/env python3
"""ATOM-DIF.COR.001-05 — F-NAR-019. Le camion sous le robinet. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.001-05"
N1 = LIMITS["N1"]
TITLE = "Le camion sous le robinet"
INDICE = "éclat de robinet"
FIL = (
    "Le robinet du jardin fait tic. Une goutte tient. Sur le métal, "
    "un éclat de robinet brille. Amir veut laver le camion de bois "
    "maintenant, pour un voyage jusqu'au plaid. Il invite Sarah. Ils "
    "ne veulent pas la même chose : les roues contre l'eau. Le camion "
    "glisse, l'éclat saute. Ils refusent de foncer, écoutent le tic. "
    "Sarah tient le toit, Amir frotte les roues. Merci vécu. Le camion "
    "file vers le plaid. Ils le prennent des deux bords. L'éclat de "
    "robinet tient."
)
CHARS = "Amir, Sarah, papa, maman"
SETTING = (
    "jardin, robinet, torchon à carreaux, plaid, camion de bois"
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
    r"\b(cerceau|émail|email|émaillé|emaille|samare|bassine|"
    r"enveloppe|dalle|carte|cartes|panier|dorure|poire|sac|"
    r"cloche|corbeille|croissant|réverbère|reverbere|bâche|"
    r"bache|volet|farine|léo|leo|amina|victorina|escargot|"
    r"spirale|arrosoir|fraise|fraises|fraisier|fraisiers|"
    r"cerisier|tilleul|orange|oranges|carton|pomme|pommes|"
    r"tarte|bateau|bateaux|drap|voiture)\b",
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
    "même leçon",
    "même règle",
    "c'est la règle",
    "tu peux dire la règle",
    "comme un secret",
    "gouttière",
    "gouttiere",
    "tailles différentes",
    "jouez ensemble",
    "jouer ensemble",
    "on peut jouer",
    "vous jouez",
    "fil à linge",
    "fil a linge",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "lune d'étain",
    "lune d'etain",
    "trois notes",
    "lumière couleur de miel",
    "lumiere couleur de miel",
    "éclat de boule",
    "éclat de carte",
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
    "éclat de dalle",
    "éclat d'enveloppe",
    "éclat de cerceau",
    "éclat de bassine",
    "éclat de samare",
    "éclat d'émail",
    "éclat d'email",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de robinet",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_invite_sarah_mais_ils_ne_veulent_pas_la_meme_chose; "
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
            "sous_texte=amir_invite_sarah_ils_jouent; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de robinet",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=sarah_tient_le_toit_amir_frotte_les_roues; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="camion",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=ils_prennent_le_camion_des_deux_bords; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de robinet",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_metal; "
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
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
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
    "narrateur|Le robinet du jardin fait tic.",
    "narrateur|Une goutte tient, ronde.",
    "narrateur|Sur le métal, un éclat de robinet brille.",
    "narrateur|Amir connaît ce jardin, après le soleil.",
    "narrateur|Un détail paraît nouveau, sur le bec.",
    "maman|Tu le vois, Amir ?",
    "enfant-m|Oui, maman.",
    "enfant-m|Il brille.",
    "papa|C'est l'eau, sur le métal.",
    "narrateur|Le torchon à carreaux sèche sur la pierre.",
    "narrateur|Il sent le savon.",
    "narrateur|Un petit camion de bois attend.",
    "narrateur|Le bois a de la poussière.",
    "narrateur|Un plaid tiède repose près des tomates.",
    "enfant-m|Je veux laver le camion, maintenant !",
    "maman|Pour un voyage, après ?",
    "enfant-m|Oui.",
    "enfant-m|Jusqu'au plaid.",
    "papa|Tes mains, Amir ?",
    "enfant-m|Elles sont prêtes.",
    "narrateur|Sarah arrive près de la pierre.",
    "enfant-m|Tu viens ?",
    "enfant-m|On lave le camion.",
    "enfant-f|Oui.",
    "narrateur|En ce moment, Amir prend le camion.",
    "narrateur|Le bois est sec, un peu rêche.",
    "narrateur|Sarah pose une main sur le toit.",
    "narrateur|Amir pose une main sur une roue.",
    "enfant-f|Moi, je mets de l'eau.",
    "enfant-m|Moi, les roues.",
    "papa|Un peu d'eau ?",
    "enfant-m|Oui, papa.",
    "narrateur|Un filet tiède tombe sur la pierre.",
    "narrateur|Amir tire vers les roues.",
    "narrateur|Sarah tire vers l'eau.",
    "enfant-m|Les roues, Sarah !",
    "enfant-f|L'eau d'abord !",
    "narrateur|Le camion glisse.",
    "narrateur|Il tape la pierre.",
    "narrateur|L'eau gicle sur le torchon.",
    "enfant-m|Oh.",
    "enfant-f|Il est parti.",
    "narrateur|L'éclat de robinet saute.",
    "narrateur|Une goutte le cache.",
    "narrateur|Le sourire d'Amir disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "narrateur|Papa s'accroupit à la même hauteur.",
    "papa|Tu veux le camion propre ?",
    "enfant-m|Oui, papa.",
    "maman|Sarah, tu le tiens ?",
    "enfant-f|Oui, maman.",
    "papa|Tu tiens ma manche, Amir ?",
    "enfant-m|Oui.",
    "narrateur|Amir veut recommencer tout de suite.",
    "narrateur|Ses doigts foncent vers le bois.",
    "enfant-m|Je le veux maintenant !",
]

Q0001 = [
    "narrateur|Amir invite Sarah.",
    "narrateur|Que font-ils ?",
]

C0001 = [
    "narrateur|Amir ouvre les mains trop vite.",
    "narrateur|Il veut tirer le camion, seul.",
    "narrateur|Le bois glisse de nouveau.",
    "enfant-m|Oh.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Sarah s'arrête aussi.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Ils écoutent le tic du robinet.",
    "narrateur|Une goutte glisse sur le métal.",
    "narrateur|L'éclat de robinet revient.",
    "enfant-m|Il est là, Sarah.",
    "enfant-f|Je le vois.",
    "papa|Tu le vois sur le bec ?",
    "enfant-m|Oui, papa.",
    "maman|Le torchon, près de la pierre ?",
    "enfant-f|Je le prends.",
    "narrateur|Sarah tient le toit, plus haut.",
    "narrateur|Amir n'atteint pas le bec.",
    "enfant-m|C'est haut.",
    "enfant-f|Je tiens.",
    "papa|Un filet, juste un peu ?",
    "enfant-f|Oui.",
    "narrateur|L'eau tiède touche le toit.",
    "narrateur|Amir frotte les roues, plus bas.",
    "narrateur|Le torchon à carreaux devient mouillé.",
    "enfant-m|Ça mousse un peu !",
    "enfant-f|Le toit brille.",
    "enfant-m|Les roues aussi.",
    "maman|Le bois a bu un peu ?",
    "enfant-m|Oui, maman.",
    "papa|Merci, Amir.",
    "narrateur|Papa a regardé jusqu'au bout.",
    "enfant-f|On fait le voyage ?",
    "enfant-m|Oui.",
    "narrateur|Un plaid attend près des tomates.",
    "narrateur|Il sent le soleil.",
    "papa|Le plaid est le garage ?",
    "enfant-m|Oui, papa.",
    "maman|Sarah, tu marches à côté ?",
    "enfant-f|Oui, maman.",
    "narrateur|Sarah garde une main sur le toit.",
    "narrateur|Amir pousse une roue, lente.",
]

END = [
    "narrateur|Amir pousse le camion trop vite.",
    "narrateur|Sarah marche trop loin, devant.",
    "narrateur|Les roues font un bruit mouillé.",
    "enfant-m|Il va au garage !",
    "narrateur|Le camion part de travers.",
    "narrateur|Le torchon tombe sur la pierre.",
    "enfant-f|Il file !",
    "narrateur|Amir veut le rattraper, d'un coup.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Ses épaules se serrent un peu.",
    "narrateur|Ça tape, dans sa poitrine.",
    "narrateur|Personne ne dit la suite.",
    "enfant-f|Toi un bord.",
    "enfant-m|Moi l'autre.",
    "narrateur|Sarah se met d'un côté.",
    "narrateur|Amir se met de l'autre.",
    "narrateur|Ils poussent, sans se presser.",
    "papa|Tes pieds sont près des roues ?",
    "enfant-m|Oui, papa.",
    "maman|Sarah, tu tiens le toit ?",
    "enfant-f|Oui, maman.",
    "narrateur|Le camion avance, droit.",
    "narrateur|Il arrive sur le plaid.",
    "enfant-m|Le garage, Sarah.",
    "enfant-f|Il est chaud.",
    "narrateur|Le plaid garde une petite trace d'eau.",
    "maman|Le bois sèche au soleil ?",
    "enfant-m|Oui, maman.",
    "papa|Le torchon, sur la pierre ?",
    "enfant-f|Je le pose.",
    "narrateur|Sarah pose le torchon à carreaux.",
    "narrateur|Amir pose le camion, deux mains.",
]

FIN = [
    "narrateur|Ils restent près du plaid.",
    "narrateur|Le camion de bois repose, propre.",
    "enfant-m|L'éclat est là, papa.",
    "papa|Tu le vois sur le bec ?",
    "enfant-m|Oui, papa.",
    "maman|On est bien, ici.",
    "narrateur|Le robinet fait tic, plus petit.",
    "narrateur|Le torchon à carreaux sèche.",
    "enfant-f|Le toit est lisse.",
    "enfant-m|Les roues aussi.",
    "narrateur|Amir pose la joue près du bois.",
    "narrateur|Le bois est froid, un peu.",
    "enfant-m|C'est froid.",
    "papa|Tu le sens sur tes joues ?",
    "enfant-m|Oui, il est froid.",
    "enfant-f|Il a voyagé.",
    "maman|Jusqu'au plaid ?",
    "enfant-m|Oui, maman.",
    "narrateur|Le capot porte une trace de paume.",
    "narrateur|Dehors, le jardin s'endort.",
    "narrateur|L'éclat de robinet tient sur le métal.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "robinet,goutte,camion",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "jouer ensemble",
                    "accepted_examples": (
                        "jouer ensemble | ensemble | ils jouent | jouer"
                    ),
                    "retry_prompt": "Ils jouent. Que font Amir et Sarah ?",
                    "engine_ok_text": "Oui, ils jouent ensemble.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "robinet,torchon",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "camion,plaid",
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
    for bad_name in ("brice", "ninon", "léo", "leo", "amina", "victorina", "copine"):
        if re.search(rf"\b{bad_name}\b", blob):
            raise SystemExit(f"{SID}: {bad_name} interdit")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "papa|" not in "\n".join(c["script"] for c in chunks):
        raise SystemExit(f"{SID}: papa absent")
    if "enfant-f|" not in "\n".join(c["script"] for c in chunks):
        raise SystemExit(f"{SID}: Sarah (enfant-f) absente")
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
    if qtext != "Amir invite Sarah. Que font-ils ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "jouer ensemble":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt") or ""
    if "victorina" in retry.lower() or "amina" in retry.lower():
        raise SystemExit(f"{SID}: retry 3e enfant")
    if "amir" not in retry.lower() or "sarah" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans Amir/Sarah")
    if "jouent" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans jouent")

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
        "- **Public :** N1 (≤10 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.COR.001 — jouer ensemble (vécue : invitation, "
        "deux désirs au même instant, camion qui glisse ; toit plus haut, "
        "roues plus bas ; deux bords vers le plaid). Jamais dite.\n"
        "- **Personnages :** Amir, Sarah, papa, maman. Dump maman seule → "
        "papa ajouté. Troupe D16. Sarah = `enfant-f` (pas copine).\n"
        "- **Lieu :** jardin, robinet, torchon à carreaux, plaid, camion "
        "de bois. Distinct 001-01 fraises/cerisier, 001-02 carton/tilleul, "
        "001-03 pomme/bassine, 001-04 drap/cerceau.\n"
        "- **Indice unique :** éclat de robinet (brille à l'ouverture → "
        "saute sous la goutte → revient sur le bec → tient à la fin)\n"
        "- **Question moteur :** Amir invite Sarah. Que font-ils ? → "
        "jouer ensemble. retry : Que font Amir et Sarah ?\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le robinet du jardin fait tic. Une goutte tient. Sur le métal, "
        "un éclat de robinet brille. Amir connaît ce jardin ; le détail "
        "sur le bec paraît nouveau. Torchon à carreaux, savon, camion de "
        "bois poussiéreux, plaid près des tomates. Amir veut laver le "
        "camion **maintenant**, pour un voyage jusqu'au plaid. Sarah "
        "arrive. Il l'invite. Ils posent les mains, toit et roue. Ils ne "
        "veulent pas la même chose : l'eau contre les roues. Le camion "
        "glisse, tape la pierre, l'eau gicle, l'éclat saute. Sourire "
        "parti, épaules, papa à la même hauteur. Question. Il tire seul : "
        "ça glisse. Il refuse de foncer. Ils écoutent le tic. L'éclat "
        "revient. Sarah tient le toit, plus haut. Amir n'atteint pas. Il "
        "frotte les roues, plus bas. Merci vécu. Le camion file de travers "
        "vers le plaid. Ils refusent, prennent les deux bords. L'éclat de "
        "robinet tient. Trace de paume.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin, robinet tic, goutte, torchon à carreaux, "
        "pierre, savon, plaid, tomates.\n"
        "- Désir : laver le camion de bois maintenant, voyage jusqu'au "
        "plaid-garage.\n"
        "- Objet : camion de bois, robinet, torchon, plaid.\n"
        "- Indice unique : éclat de robinet, vu dès l'ouverture, payé à "
        "la fin.\n"
        "- Urgence douce : le voyage attend, l'eau tombe.\n"
        "- Imprévu 1 : deux désirs au même instant ; le camion glisse, "
        "l'éclat saute.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : pousser d'un coup ; le camion file de "
        "travers, torchon à terre.\n"
        "- Résolution : ils refusent de foncer, toit et roues, puis deux "
        "bords.\n"
        "- Retour : camion propre sur le plaid, éclat du début, trace de "
        "paume.\n\n"
        "## Vécu\n\n"
        "Amir veut laver le camion **maintenant**. Il invite Sarah. "
        "Impatience, puis épaules quand le bois tape la pierre. Papa "
        "s'accroupit, pose une question, ne dit pas « jouer ensemble ». "
        "Sarah tient le toit, Amir les roues. Merci vécu après le regard "
        "jusqu'au bout. Fin : l'éclat du début tient sur le métal.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre « Le camion sous le robinet ». Monde dump : jardin, "
        "robinet, torchon à carreaux, plaid, camion de bois.\n"
        "- Héros Amir. Autre enfant D16 : Sarah. Papa ajouté. Maman "
        "garde. Troupe D16.\n"
        "- Question dump conservée : « Amir invite Sarah. Que font-ils "
        "? ». expected jouer ensemble.\n"
        "- Ouverture inventée (robinet tic, goutte, éclat), pas « joue "
        "au salon », pas gabarit v2, pas cerceau/émail/samare/bassine/"
        "enveloppe/dalle.\n"
        "- Distinct de DIF.COR.001-01..04 (fraises, carton, pomme, drap).\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent / "
        "tout bas » retirés. Pas de merle, pas de miel, pas de secret.\n"
        "- Ban : cerceau, émail, samare, bassine, enveloppe, dalle, "
        "carte, panier, dorure, poire, sac, cloche, corbeille, croissant, "
        "réverbère, bâche, volet, farine, fraise, tilleul, orange, "
        "carton, pomme, tarte, bateau, drap, voiture.\n"
        "- Leçon non dite (pas « vous jouez ensemble », pas « tailles "
        "différentes »). Hauteur vécue : toit / bec / roues.\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- Indice unique « éclat de robinet » nommé à l'ouverture, "
        "revu quand il saute, revu sur le bec, payé à la fin.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive.\n"
        f"- {nwords} mots. N1 ≤ 10. `check()` OK. Pas apply.\n\n"
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
