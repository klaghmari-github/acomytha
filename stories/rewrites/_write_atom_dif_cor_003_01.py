#!/usr/bin/env python3
"""ATOM-DIF.COR.003-01 — Le bateau de papier de Mila (F-NAR-019, N2, linéaire)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.003-01"
LIM = 15
TITLE = "Le bateau de papier de Mila"
CHARS = "Mila, Sarah, papa, maman"
SETTING = (
    "entrée puis cour après la pluie, radiateur, manteaux, botte jaune"
)
INDICE = "éclat de botte"
FIL = (
    "La laine sent la pluie. Un tic chaud. Sur le caoutchouc, un "
    "éclat de botte luit. Mila veut un bateau dans la flaque, "
    "maintenant, avec Sarah. Elle tend trop vite vers les lunettes : "
    "non. Le bateau penche, n'atteint pas. Sourire parti. Elle refuse "
    "de foncer. Merci vécu. Elle pose d'un coup : le papier reste au "
    "bord. Elle s'arrête, lit l'éclat. Un éclat de botte reste pâle."
)
TICS = (
    "tout doux",
    "tout calme",
    "tout lent",
    "tout bas",
    "tout doucement",
    "encore",
    "déjà",
    "deja",
    "aujourd'hui,",
    "aujourd'hui ",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "merle",
    "miel",
    "grand-père",
    "grand-pere",
    "bon travail",
    "l'histoire est finie",
    "c'est du bon travail",
    "tu as fait du bon travail",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "il ne faut pas rire",
    "on peut proposer",
    "on peut accepter",
    "plusieurs réponses",
    "plusieurs reponses",
    "c'est une réponse",
    "c'est une reponse",
    "on joue",
    "vous jouez",
    "jouer ensemble",
    "tu as des lunettes",
    "lunettes aident",
    "apparence",
    "pas rire",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "une chose, puis",
    "une chose puis",
    "éclat de volet",
    "éclat de plaque",
    "éclat de dalle",
    "éclat de pierre",
    "éclat de grille",
    "éclat de couvercle",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de farine",
    "éclat de croissant",
    "éclat de carte",
    "éclat de boule",
    "éclat de galet",
    "éclat de cube",
    "éclat de bois",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de carotte",
    "éclat de gomme",
    "éclat de crayon",
    "éclat de tiroir",
    "éclat de rayon",
    "éclat de tapis",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de fraisier",
    "éclat de chaise",
    "éclat de coussin",
    "éclat de limace",
    "éclat de perron",
    "éclat de manteau",
    "éclat de radiateur",
    "éclat de flaque",
    "éclat de papier",
    "éclat de feuille",
    "éclat de capuchon",
    "éclat de lunette",
    "fanny",
    "amandine",
    "nora",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "maîtresse",
    "maitresse",
)
BAN_WORDS = re.compile(
    r"\b(limace|perron|chaise|tiroir|fraisier|cuivre|buis|coussin|"
    r"haie|cheval|guirlande|fraise|drap|lanterne|biscuit|casserole|"
    r"figue|samare|bassine|cerceau|robinet|planche|émail|email)\b",
    re.I,
)


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
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
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
    if m.get("pitch_tag"):
        body = f"<{m['pitch_tag']}>{body}</{m['pitch_tag']}>"
    pause = m["pause"]
    tail = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return f"{body}{tail}".strip()


PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_bateau_et_sarah_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=mila_plie_avec_sarah_sans_commenter; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_attend_le_silence_puis_dit_d_accord; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis prudence; intensite=2; "
            "destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat_de_botte; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_de_botte_reste_pale; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}


def vet(pairs: list[tuple[str, str]], where: str) -> None:
    prev = ""
    run = 1
    skip_lesson = where == "CHK_T0000_P0000_Q0001"
    for role, ph in pairs:
        n = words(ph)
        if n > LIM:
            raise SystemExit(f"{where} {n}>{LIM}: {ph}")
        if n == 0:
            raise SystemExit(f"{where} vide")
        if "|" in ph:
            raise SystemExit(f"{where} pipe: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"{where} ponctuation: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"{where} {marks} phrases: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"{where} interdit « {bad} »: {ph}")
        if not skip_lesson:
            for tic in TICS:
                if tic in low:
                    raise SystemExit(f"{where} tic « {tic} »: {ph}")
        if BAN_WORDS.search(ph):
            raise SystemExit(f"{where} ban: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-f", "copine"):
            raise SystemExit(f"{where} rôle {role}: {ph}")
        if role == "narrateur":
            tok = ph.split()[0].lower()
            if tok == prev:
                run += 1
                if run >= 4:
                    raise SystemExit(f"{where} puces « {tok} »")
            else:
                run = 1
                prev = tok
        else:
            run = 1
            prev = ""


def voice(old: dict, pairs: list[tuple[str, str]], profile: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    vet(pairs, old["chunk_id"])
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    elif "emphasis" not in m:
        m["emphasis"] = None
    lines = [f"{r}|{p}" for r, p in pairs]
    text, script = from_script(lines)
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
    out = deepcopy(old)
    out["text"] = text
    out["script"] = script
    out["sons"] = extra.get("sons", old.get("sons") or "")
    if out["sons"] is None:
        out["sons"] = ""
    out["text_ssml"] = ssml(text, m)
    out["text_xai_tags"] = xai(text, m)
    out["rate_wpm"] = m["wpm"]
    out["rate_label"] = m["rate"]
    out["speed_xai"] = m["speed"]
    out["length_scale_piper"] = m["piper"]
    out["pitch_label"] = m["pitch"]
    out["pitch_ssml"] = m["pitch_ssml"]
    out["pitch_xai_tag"] = m["pitch_tag"]
    out["volume_label"] = m["volume"]
    out["volume_db"] = m["db"]
    out["emphasis_words"] = m.get("emphasis") or ""
    out["pause_before_ms"] = extra.get("pause_before", 0)
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
    out["notes"] = extra.get("note", m["note"])
    out["night_policy"] = extra.get("night_policy", "play")
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        out[k] = v
    return out


def L(*rows: tuple[str, str]) -> list[tuple[str, str]]:
    return list(rows)


OPENING = L(
    ("narrateur", "La laine des manteaux sent la pluie."),
    ("enfant-f", "Ça sent mouillé, maman."),
    ("maman", "Tu le sens, sur le tissu ?"),
    ("enfant-f", "Oui, un peu froid."),
    ("narrateur", "Le radiateur fait un tic chaud."),
    ("papa", "Tu l'entends, près des crochets ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "Papa égoutte un manteau, sans parler."),
    ("narrateur", "Une botte jaune est couchée."),
    ("narrateur", "Sur le caoutchouc, un éclat de botte luit."),
    ("enfant-f", "Il brille, papa !"),
    ("papa", "Tu le vois, sur la botte ?"),
    ("enfant-f", "Oui, un petit point."),
    ("narrateur", "Une goutte tombe du capuchon."),
    ("narrateur", "Elle fait un rond sur le bois."),
    ("enfant-f", "Le bois est luisant."),
    ("maman", "La pluie a fini, dehors."),
    ("enfant-f", "La cour brille."),
    ("papa", "Il y a une flaque, Mila."),
    ("enfant-f", "Je veux un bateau, maintenant !"),
    ("maman", "Un bateau de papier ?"),
    ("enfant-f", "Oui, pour la flaque."),
    ("narrateur", "Maman pose une feuille blanche."),
    ("narrateur", "La feuille est un peu rêche."),
    ("enfant-f", "Elle sent le bois."),
    ("papa", "Tu restes près des bottes ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "En ce moment, Mila plie la feuille trop vite."),
    ("narrateur", "Un coin se replie tout seul."),
    ("enfant-f", "Il penche !"),
    ("maman", "Le milieu, Mila ?"),
    ("enfant-f", "J'y vais."),
    ("narrateur", "Sarah arrive près des bottes."),
    ("narrateur", "Son manteau est bleu vif."),
    ("narrateur", "Sarah a les cheveux courts."),
    ("enfant-f", "Sarah !"),
    ("narrateur", "Sarah a des lunettes."),
    ("narrateur", "Elles brillent un peu."),
    ("enfant-f", "Elles brillent !"),
    ("narrateur", "Mila avance la main vers les lunettes."),
    ("copine", "Non."),
    ("narrateur", "Sarah recule d'un pas."),
    ("enfant-f", "Oh."),
    ("narrateur", "Mila plie toute seule, trop vite."),
    ("narrateur", "Le papier fait frrt."),
    ("narrateur", "Le bateau penche, de travers."),
    ("enfant-f", "Il ne tient pas."),
    ("narrateur", "Le sourire de Mila disparaît."),
    ("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
    ("narrateur", "L'éclat de botte tremble, puis tient."),
    ("papa", "Tu vois Sarah, Mila ?"),
    ("narrateur", "Papa s'accroupit à la même hauteur."),
    ("enfant-f", "Oui, papa."),
    ("maman", "Tes mains sont froides, Mila ?"),
    ("enfant-f", "Un peu, maman."),
)

QUESTION = L(
    ("narrateur", "Sarah a des lunettes."),
    ("narrateur", "Que fait Mila ?"),
)

CONFIRM = L(
    ("narrateur", "Mila avance trop vite vers la feuille."),
    ("enfant-f", "Tu plies, maintenant !"),
    ("narrateur", "Les mots se bousculent dans sa bouche."),
    ("copine", "Non."),
    ("narrateur", "Sarah reste près des bottes."),
    ("enfant-f", "Oh."),
    ("narrateur", "Le sourire ne revient pas."),
    ("narrateur", "Mila refuse de foncer."),
    ("narrateur", "Elle referme la main."),
    ("papa", "Tu veux le bateau avec Sarah ?"),
    ("narrateur", "Papa reste à la même hauteur."),
    ("enfant-f", "Tu regardes ?"),
    ("narrateur", "Sarah ne dit rien, d'abord."),
    ("narrateur", "Elle pose un genou près du bois."),
    ("copine", "Je plie."),
    ("enfant-f", "D'accord."),
    ("papa", "Merci, Mila."),
    ("narrateur", "Papa a vu les deux, près de la feuille."),
    ("maman", "Le papier est rêche, sous les doigts."),
    ("enfant-f", "Il sent le bois."),
    ("narrateur", "Elles replient le milieu, sans se presser."),
    ("narrateur", "Sarah montre un pli, du doigt."),
    ("copine", "Là."),
    ("enfant-f", "Je le vois."),
    ("narrateur", "Le bateau se tient droit."),
    ("enfant-f", "Il est prêt !"),
    ("copine", "La flaque ?"),
    ("maman", "Les bottes d'abord, Mila."),
    ("narrateur", "Mila enfile la botte jaune."),
    ("narrateur", "Sarah enfile les siennes."),
    ("enfant-f", "Elle colle, maman."),
    ("maman", "Tire un peu."),
    ("enfant-f", "Elle vient."),
    ("papa", "La poignée est froide, toi ?"),
    ("enfant-f", "Oui, papa."),
    ("enfant-f", "J'ouvre ?"),
    ("maman", "Oui."),
    ("narrateur", "L'air de la cour entre."),
    ("enfant-f", "Ça sent la pluie."),
    ("papa", "La flaque est là."),
    ("enfant-f", "On y va."),
    ("narrateur", "Le ventre de Mila se desserre."),
    ("narrateur", "Les épaules se relèvent un peu."),
)

GARDEN = L(
    ("narrateur", "La cour brille, après la pluie."),
    ("narrateur", "La flaque est ronde, un peu lisse."),
    ("enfant-f", "Je le mets, d'un coup !"),
    ("narrateur", "Mila pose le bateau trop vite."),
    ("narrateur", "Le papier tremble, puis s'arrête au bord."),
    ("enfant-f", "Il n'avance pas !"),
    ("copine", "Attends."),
    ("narrateur", "Sarah reste un pas plus loin."),
    ("narrateur", "Mila avance la main, trop vite."),
    ("enfant-f", "Tu souffles, maintenant !"),
    ("copine", "Non."),
    ("enfant-f", "Oh."),
    ("narrateur", "Le bateau reste collé au bord."),
    ("narrateur", "Mila refuse de foncer, cette fois."),
    ("narrateur", "Ses mains se ferment, puis s'ouvrent."),
    ("narrateur", "Elle observe la flaque, un instant."),
    ("enfant-f", "J'écoute."),
    ("narrateur", "Elle écoute le tic, derrière la porte."),
    ("narrateur", "Sur le caoutchouc, un éclat de botte luit."),
    ("enfant-f", "Là, sur la botte."),
    ("enfant-f", "Tu souffles, si tu veux ?"),
    ("narrateur", "Sarah ne dit rien."),
    ("narrateur", "Elle se baisse près de l'eau."),
    ("copine", "Oui."),
    ("narrateur", "Elles soufflent, sans se presser."),
    ("narrateur", "La voile se gonfle un peu."),
    ("enfant-f", "Il avance !"),
    ("copine", "Il tourne."),
    ("papa", "Tu le vois, au milieu ?"),
    ("enfant-f", "Oui, papa."),
    ("maman", "Une feuille passe sur l'eau."),
    ("enfant-f", "Il l'évite."),
    ("copine", "Il est fort."),
    ("enfant-f", "C'est notre bateau."),
    ("papa", "Tu restes un peu ?"),
    ("enfant-f", "Oui, papa."),
    ("maman", "Tes bottes sont froides ?"),
    ("enfant-f", "Un peu, maman."),
)

ENDING = L(
    ("enfant-f", "Le bateau a flotté, papa."),
    ("papa", "Tu le vois, comme tout à l'heure ?"),
    ("enfant-f", "Oui, au milieu."),
    ("maman", "On le garde près de nous ?"),
    ("enfant-f", "Oui, maman."),
    ("narrateur", "La botte jaune attend près du seuil."),
    ("enfant-f", "Elle est tiède."),
    ("papa", "Le caoutchouc luit, toi ?"),
    ("enfant-f", "Un peu, papa."),
    ("narrateur", "Mila pose un doigt sur la botte."),
    ("enfant-f", "Ça sentait la laine."),
    ("maman", "Les manteaux sèchent, près du radiateur."),
    ("enfant-f", "Il fait tic."),
    ("papa", "On reste un peu ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "Les joues de Mila se réchauffent."),
    ("copine", "Il tourne."),
    ("enfant-f", "Oui."),
    ("narrateur", "Le papier reste mouillé, au milieu."),
    ("narrateur", "Un éclat de botte reste pâle."),
)


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: c for c in src["chunks"]}
    scripts = {
        "CHK_T0000_P0000": (
            "opening",
            OPENING,
            "feuilles,manteaux",
            {"emphasis": "éclat de botte"},
        ),
        "CHK_T0000_P0000_Q0001": (
            "clue",
            QUESTION,
            "",
            {
                "emphasis": "lunettes",
                "pause_before": 200,
                "fields": {
                    "expected_answer": "jouer",
                    "accepted_examples": (
                        "jouer | ensemble | inviter | plier | on joue | pas rire"
                    ),
                    "retry_prompt": "Mila invite Sarah. Que fait-elle ?",
                    "engine_ok_text": "Oui, jouer.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": (
            "resolution",
            CONFIRM,
            "papier",
            {"emphasis": "D'accord", "pause_before": 200},
        ),
        "CHK_T0000_P0000_END": (
            "obstacle",
            GARDEN,
            "eau,papier",
            {"emphasis": "éclat de botte", "pause_before": 200},
        ),
        "CHK_T0000_P0000_END_F0001": (
            "ending",
            ENDING,
            "radiateur",
            {"emphasis": "éclat de botte", "pause_before": 200},
        ),
    }
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{SID} chunks missing={missing} extra={extra}")
    chunks = []
    for c in src["chunks"]:
        cid = c["chunk_id"]
        profile, pairs, sons, extra = scripts[cid]
        extra = dict(extra)
        extra["sons"] = sons
        chunks.append(voice(by[cid], pairs, profile, extra))
    for c in chunks:
        if not c.get("notes") or not c.get("text_ssml") or not c.get("text_xai_tags"):
            raise SystemExit(f"{c['chunk_id']}: TTS incomplet")
        if c["text_xai_tags"] == c["text"]:
            raise SystemExit(f"{c['chunk_id']}: text_xai_tags = text")
        if "<speak>" not in c["text_ssml"]:
            raise SystemExit(f"{c['chunk_id']}: ssml nu")
        if c.get("kind") != by[c["chunk_id"]].get("kind"):
            raise SystemExit(f"{c['chunk_id']}: kind changé")
    joined = "\n".join(c["script"] for c in chunks).lower()
    if INDICE not in joined:
        raise SystemExit(f"indice {INDICE} manquant")
    if INDICE not in chunks[0]["text"].lower():
        raise SystemExit("indice absent à l'ouverture")
    if INDICE not in chunks[-1]["text"].lower():
        raise SystemExit("indice non payé à la fin")
    n_clue = joined.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "éclat de volet" in joined:
        raise SystemExit("BAN : éclat de volet")
    for ban in (
        "limace", "perron", "chaise", "tiroir", "fraisier", "cuivre",
        "buis", "coussin",
    ):
        if re.search(rf"\b{ban}\b", joined):
            raise SystemExit(f"{SID}: BAN {ban}")
    if joined.count("en ce moment") != 1:
        raise SystemExit("en ce moment doit apparaître une fois")
    if "refuse de foncer" not in joined:
        raise SystemExit("manque refuse de foncer")
    if "sarah ne dit rien" not in joined:
        raise SystemExit("silence Sarah absent")
    if "botte jaune" not in joined:
        raise SystemExit("botte jaune du dump absente")
    if "radiateur" not in joined:
        raise SystemExit("radiateur du dump absent")
    if "manteaux" not in joined:
        raise SystemExit("manteaux du dump absents")
    if "flaque" not in joined:
        raise SystemExit("flaque du dump absente")
    adults = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
    ).lower()
    if adults.count("merci") != 1:
        raise SystemExit(f"merci ×{adults.count('merci')}")
    if "bravo" in adults:
        raise SystemExit("bravo en trop")
    qtext = chunks[1]["text"]
    if qtext != "Sarah a des lunettes. Que fait Mila ?":
        raise SystemExit(f"question moteur altérée: {qtext}")
    if chunks[1].get("expected_answer") != "jouer":
        raise SystemExit("expected_answer altéré")
    retry = str(chunks[1].get("retry_prompt") or "")
    if "sarah" not in retry.lower():
        raise SystemExit("retry sans Sarah")
    if "enfant-m|" in joined:
        raise SystemExit("enfant-m (Mila = enfant-f)")
    if "maitresse|" in joined or "maîtresse" in joined:
        raise SystemExit("maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if "copine" not in roles:
        raise SystemExit("Sarah absente (copine)")
    if "enfant-f" not in roles:
        raise SystemExit("Mila absente")
    if not any(r == "papa" for r in roles):
        raise SystemExit("papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit("maman absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "tu as des lunettes",
        "lunettes aident",
        "on ne va pas rire",
        "il ne faut pas rire",
        "apparence",
        "on joue",
        "vous jouez",
        "pas rire",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    copine_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    ).lower()
    if "non" not in copine_txt:
        raise SystemExit("Sarah sans non")
    if "attends" not in copine_txt:
        raise SystemExit("Sarah sans attends")
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    check(SID, out["age_band"], out["chunks"])
    nwords = sum(words(c["text"]) for c in chunks)
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N2 (≤15 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.COR.003 — Sarah a des lunettes, jouer avec "
        "(vécue : Mila tend trop vite vers les lunettes, Sarah dit non ; "
        "elle attend le silence, dit d'accord ; elles plient, puis "
        "soufflent). JAMAIS dite dans le récit. Pas « tu as des lunettes » "
        "en morale.\n"
        "- **Personnages :** Mila, Sarah, papa, maman. Papa ajouté. "
        "Troupe D16 gardée. Deux rythmes : Mila propose, Sarah prend "
        "son temps ou pose sa limite. Le silence compte. Adultes "
        "parlants = papa/maman.\n"
        "- **Lieu :** entrée puis cour après la pluie, radiateur, "
        "manteaux, botte jaune, feuille, flaque (monde dump, pas "
        "indice). ≠ COR.002 cuisine/cuivre, haie, guirlande, fraises.\n"
        "- **Indice unique :** éclat de botte (luit à l'ouverture, "
        "tremble au refus, luit au bord, reste pâle). Pas éclat de "
        "cuivre / buis / tiroir / fraisier / chaise / coussin. Pas "
        "limace / perron.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La laine des manteaux sent la pluie. Le radiateur fait un tic "
        "chaud. Sur le caoutchouc, un éclat de botte luit. Mila veut un "
        "bateau de papier dans la flaque **maintenant**, avec Sarah. "
        "Première idée : elle tend vers les lunettes. Sarah dit non, "
        "recule. Mila plie trop vite, seule. Le bateau penche. Sourire "
        "parti, épaules basses. Papa se baisse. Elle refuse de foncer. "
        "Elle attend son silence. « Tu regardes ? » Sarah plie. "
        "« D'accord. » Merci vécu. Elle pose d'un coup : le papier "
        "reste au bord. Sarah : attends. Elle s'arrête, lit l'éclat. "
        "Elles soufflent. Un éclat de botte reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : entrée après la pluie, radiateur, manteaux mouillés, "
        "botte jaune, goutte du capuchon, cour, flaque. ≠ COR.002.\n"
        "- Désir : le bateau de papier dans la flaque, maintenant, avec "
        "Sarah.\n"
        "- Objet : feuille, bateau, bottes, lunettes (fait du monde, "
        "pas morale).\n"
        "- Indice unique : éclat de botte, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : Sarah près des bottes, la flaque qui attend.\n"
        "- Imprévu 1 : main vers les lunettes, non, bateau de travers. "
        "Le bateau n'atteint pas la flaque.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après d'accord.\n"
        "- Imprévu 2 (plus rusé) : bateau posé d'un coup, collé au bord ; "
        "elle veut un souffle ; Sarah dit non.\n"
        "- Résolution : elle refuse de foncer, attend, dit d'accord ; "
        "Sarah souffle quand elle veut.\n"
        "- Retour : bateau au milieu, laine qui sèche, éclat pâle.\n\n"
        "## Vécu\n\n"
        "Mila veut le bateau et Sarah **maintenant**. Impatience "
        "(main trop vite vers les lunettes, voix trop grande), puis "
        "sourire qui disparaît. Papa se baisse, pose une question, ne "
        "récite pas la règle. Sarah dit non, puis rien, puis je plie, "
        "puis attends. Mila dit d'accord. Merci vécu après l'écoute. "
        "Fin : l'éclat du début reste pâle. Pas « tu as des lunettes » "
        "en morale.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le bateau de papier de Mila (noyau dump). Troupe D16 "
        "gardée : Mila, Sarah, papa, maman. Papa ajouté.\n"
        "- Lieu du dump (entrée puis cour après la pluie, radiateur, "
        "manteaux, botte jaune). ≠ COR.002 cuivre / buis / tiroir / "
        "fraisier / chaise / coussin.\n"
        "- Ouverture inventée (laine des manteaux qui sent la pluie), "
        "pas un gabarit v2, pas « Le radiateur de l'entrée fait un tic "
        "chaud » du dump.\n"
        "- Indice unique : éclat de botte. Pas éclat de cuivre, buis, "
        "tiroir, fraisier, chaise, coussin. Pas limace, perron.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » du dump.\n"
        "- Leçon non dite : pas « tu as des lunettes », pas « lunettes "
        "aident », pas « on joue », pas « on ne va pas rire ». On la "
        "voit quand elle attend le silence et plie avec Sarah.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Sarah a des lunettes. Que fait Mila ? » "
        "expected jouer. retry inchangé. 5 chunks, kinds inchangés.\n"
        "- example4 008 / 040 / 072 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_bes_002_07.py` (Mila).\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers la flaque.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
