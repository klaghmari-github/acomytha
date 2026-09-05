#!/usr/bin/env python3
"""ATOM-DIF.COR.002-03 — La guirlande d'anniversaire de Mila (F-NAR-019, N3)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.002-03"
LIM = LIMITS["N3"]
TITLE = "La guirlande d'anniversaire de Mila"
CHARS = "Mila, Nino, papa, maman"
SETTING = "salle à manger le matin, volets, tiroir de papiers, colle"
INDICE = "éclat de tiroir"
FIL = (
    "Le tiroir de papiers est entrouvert. Ça sent la colle. Les volets "
    "laissent un rai mince. Sur le bois, un éclat de tiroir luit. Mila "
    "veut une guirlande jusqu'à la fenêtre, maintenant, avec Nino. Elle "
    "tire trop vite : Nino reste assis, l'anneau se déchire. Sourire "
    "parti. Elle refuse de foncer, s'assoit, dit d'accord. Merci vécu. "
    "Elle tire vers le haut : la guirlande penche. Elle s'arrête, lit "
    "l'éclat. Un éclat de tiroir reste pâle."
)
TICS = (
    "tout doux",
    "tout calme",
    "tout lent",
    "tout bas",
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
    "on peut proposer",
    "on peut accepter",
    "plusieurs réponses",
    "plusieurs reponses",
    "c'est une réponse",
    "c'est une reponse",
    "j'ai proposé",
    "j'ai propose",
    "j'ai accepté",
    "j'ai accepte",
    "j'ai invité",
    "j'ai invite",
    "tu as proposé",
    "tu as propose",
    "tu as accepté",
    "tu as accepte",
    "tu as su proposer",
    "tu as su accepter",
    "regarder, c'est une réponse",
    "regarder, c'est une reponse",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "une chose, puis",
    "une chose puis",
    "éclat de volet",
    "éclat de poussière",
    "éclat de poussiere",
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
    "éclat de rayon",
    "éclat de tapis",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de coussin",
    "éclat de figue",
    "éclat de robinet",
    "éclat de planche",
    "éclat de cerceau",
    "éclat d'émail",
    "éclat d'email",
    "éclat de fraisier",
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
    r"\b(cuivre|buis|coussin|figue|robinet|planche|cerceau|émail|email|"
    r"poussière|poussiere|dalle|plaque|pierre|grille|couvercle|"
    r"cheminée|cheminee|couloir|cour)\b",
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
            "destinataire=enfant; sous_texte=elle_veut_la_guirlande_et_nino_debout_maintenant; "
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
            "sous_texte=on_colle_ensemble_sans_rire_du_corps; "
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
            "destinataire=enfant; sous_texte=elle_s_assoit_attend_le_silence_dit_d_accord; "
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
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat_de_tiroir; "
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
            "sous_texte=l_eclat_de_tiroir_reste_pale; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}


def vet(pairs: list[tuple[str, str]], where: str) -> None:
    prev = ""
    run = 1
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
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"{where} tic « {tic} »: {ph}")
        if BAN_WORDS.search(ph):
            raise SystemExit(f"{where} ban: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-f", "copain"):
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
    ("narrateur", "Le tiroir de papiers est entrouvert."),
    ("narrateur", "Ça sent la colle, un peu sucré."),
    ("narrateur", "Les volets laissent un rai mince."),
    ("narrateur", "Le rai traverse la salle à manger."),
    ("enfant-f", "Il est fin, maman."),
    ("maman", "Tu le vois, sur la table ?"),
    ("enfant-f", "Oui, jusqu'au bois."),
    ("narrateur", "Un fil pend du buffet."),
    ("narrateur", "Les ciseaux attendent sur le bois."),
    ("narrateur", "La chaise a un fil qui dépasse."),
    ("narrateur", "Sur le bois du tiroir, un éclat de tiroir luit."),
    ("enfant-f", "Il brille, papa !"),
    ("papa", "Tu le vois, sur le tiroir ?"),
    ("enfant-f", "Oui, près du papier."),
    ("narrateur", "Mila touche l'éclat de tiroir, un instant."),
    ("narrateur", "Le bois est lisse, un peu froid."),
    ("enfant-f", "Il est froid."),
    ("maman", "Tu coupes, Mila ?"),
    ("enfant-f", "Oui, maintenant."),
    ("narrateur", "En ce moment, Mila prend les ciseaux."),
    ("narrateur", "Les ciseaux font un petit cri."),
    ("narrateur", "Le papier est rouge, un peu rêche."),
    ("enfant-f", "C'est pour toi, papa."),
    ("enfant-f", "Une guirlande."),
    ("papa", "Jusqu'à la fenêtre ?"),
    ("enfant-f", "Oui."),
    ("enfant-f", "Tout le chemin."),
    ("narrateur", "Nino arrive, en chaussettes silencieuses."),
    ("narrateur", "Il s'assoit près de la table."),
    ("narrateur", "La chaise craque, un peu."),
    ("narrateur", "Son ventre touche le bord du bois."),
    ("narrateur", "Nino reste assis."),
    ("enfant-f", "Tu viens coller, debout ?"),
    ("narrateur", "Nino ne dit rien."),
    ("narrateur", "Ses mains restent sur ses genoux."),
    ("copain", "Je reste assis."),
    ("enfant-f", "Debout, maintenant !"),
    ("narrateur", "Mila tire trop vite sur sa manche."),
    ("narrateur", "Nino se retient au dossier."),
    ("narrateur", "Le premier anneau se déchire."),
    ("enfant-f", "Oh."),
    ("narrateur", "La colle tombe sur le bois."),
    ("narrateur", "Le sourire de Mila disparaît."),
    ("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
    ("narrateur", "Les épaules de Mila tombent un peu."),
    ("narrateur", "Ça serre, dans son ventre."),
    ("maman", "Tu veux coller près de Nino ?"),
    ("narrateur", "Maman se baisse à sa hauteur."),
    ("papa", "Il tient le papier, toi ?"),
)

QUESTION = L(
    ("narrateur", "Le corps n'est pas une blague."),
    ("narrateur", "Que fait-on ?"),
)

CONFIRM = L(
    ("narrateur", "Mila veut le tirer vers la fenêtre."),
    ("enfant-f", "Debout, Nino !"),
    ("narrateur", "Sa voix se mélange à la colle."),
    ("narrateur", "Nino reste assis."),
    ("narrateur", "Mila refuse de foncer."),
    ("narrateur", "Elle referme la main."),
    ("maman", "Tu t'assois près de lui ?"),
    ("narrateur", "Maman s'accroupit à la même hauteur."),
    ("narrateur", "Mila pose un genou près de la chaise."),
    ("enfant-f", "Tu colles, assis ?"),
    ("narrateur", "Nino ne dit rien."),
    ("narrateur", "Il pousse un rectangle vers elle."),
    ("copain", "Oui."),
    ("enfant-f", "D'accord."),
    ("papa", "Merci, Mila."),
    ("narrateur", "Papa a vu les deux mains sur le papier."),
    ("narrateur", "Le ventre de Mila se desserre."),
    ("narrateur", "Les épaules se relèvent un peu."),
    ("maman", "La colle est froide, Mila ?"),
    ("enfant-f", "Un peu, maman."),
    ("narrateur", "Mila s'assoit, enfin."),
    ("narrateur", "Son ventre touche le bois, froid."),
    ("narrateur", "Ils collent le deuxième anneau."),
    ("narrateur", "Le papier frotte entre les doigts."),
    ("enfant-f", "Il est rêche."),
    ("copain", "Le rouge aussi."),
    ("narrateur", "Un anneau jaune s'ajoute au rouge."),
    ("enfant-f", "Le jaune, c'est le soleil."),
    ("copain", "Le rouge, c'est la fête."),
    ("papa", "Elle avance, la guirlande ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "La guirlande arrive au milieu."),
    ("narrateur", "Elle pèse un peu, tiède."),
    ("maman", "Il manque un bout, Mila ?"),
    ("enfant-f", "Trois, maman."),
    ("copain", "Trois."),
    ("narrateur", "Ils collent, sans se presser."),
    ("narrateur", "Le papier fait un petit bruit."),
)

GARDEN = L(
    ("narrateur", "Mila se lève trop vite."),
    ("enfant-f", "Jusqu'à la fenêtre, d'un coup !"),
    ("narrateur", "Elle tire Nino vers le haut."),
    ("narrateur", "Nino reste collé à la chaise."),
    ("copain", "Attends."),
    ("enfant-f", "Je la tends !"),
    ("narrateur", "La guirlande penche vers le buffet."),
    ("narrateur", "Un anneau rouge se fend, presque."),
    ("enfant-f", "Ça tombe !"),
    ("narrateur", "Mila veut rattraper le fil, d'un coup."),
    ("narrateur", "Mila refuse de foncer, cette fois."),
    ("narrateur", "Ses épaules se serrent un peu."),
    ("narrateur", "Ça tape fort, dans sa poitrine."),
    ("narrateur", "Personne ne dit la suite à voix haute."),
    ("narrateur", "Elle regarde le tiroir, elle écoute la salle."),
    ("narrateur", "Sur le bois du tiroir, un éclat de tiroir luit."),
    ("enfant-f", "Là, près du papier."),
    ("papa", "Tu le vois, toi ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "Mila baisse la guirlande, sans se presser."),
    ("narrateur", "Nino tient un bout, assis."),
    ("enfant-f", "Moi, près de la fenêtre."),
    ("maman", "Vous tenez les deux bouts ?"),
    ("enfant-f", "Oui, maman."),
    ("copain", "Moi, le bas."),
    ("narrateur", "Papa tient un bout près du buffet."),
    ("narrateur", "La guirlande touche la fenêtre."),
    ("enfant-f", "Elle est arrivée."),
    ("papa", "On la regarde un moment ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "Le rai traverse un anneau rouge."),
    ("copain", "Il brille."),
    ("enfant-f", "C'est ton cadeau."),
)

ENDING = L(
    ("enfant-f", "Le tiroir brillait, papa."),
    ("papa", "Tu le vois, comme tout à l'heure ?"),
    ("enfant-f", "Oui, sur le tiroir."),
    ("narrateur", "Ils essuient la colle sur le torchon."),
    ("narrateur", "Le torchon devient un peu dur."),
    ("maman", "On le laisse près de nous ?"),
    ("enfant-f", "Oui, maman."),
    ("enfant-f", "Ça sentait la colle."),
    ("maman", "Le tiroir est là."),
    ("narrateur", "Le tiroir se referme, un peu."),
    ("narrateur", "Mila respire, plus large."),
    ("papa", "On reste un peu ?"),
    ("enfant-f", "Oui."),
    ("papa", "Plus tard, le gâteau ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "Les joues de Mila se réchauffent."),
    ("narrateur", "Les ciseaux restent tièdes sous la main."),
    ("narrateur", "Le rai a glissé sur la table."),
    ("enfant-f", "Il est pâle."),
    ("maman", "Comme tout à l'heure ?"),
    ("enfant-f", "Oui, maman."),
    ("papa", "Le fil pend, toi ?"),
    ("enfant-f", "Un peu, papa."),
    ("narrateur", "La chaise ne craque plus."),
    ("enfant-f", "Elle est tiède."),
    ("maman", "On la laisse à table ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "Un éclat de tiroir reste pâle."),
    ("narrateur", "Le rouge garde un rai mince."),
)


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: c for c in src["chunks"]}
    scripts = {
        "CHK_T0000_P0000": (
            "opening",
            OPENING,
            "tiroir,papier,colle",
            {"emphasis": "éclat de tiroir"},
        ),
        "CHK_T0000_P0000_Q0001": (
            "clue",
            QUESTION,
            "",
            {
                "emphasis": "blague",
                "pause_before": 200,
                "fields": {
                    "expected_answer": "jouer",
                    "accepted_examples": (
                        "jouer | on joue | pas une blague | pas blague | "
                        "la guirlande | coller"
                    ),
                    "retry_prompt": (
                        "On joue. Le corps n'est pas une blague. Que fait-on ?"
                    ),
                    "engine_ok_text": "Oui, jouer.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": (
            "resolution",
            CONFIRM,
            "papier,colle",
            {"emphasis": "D'accord", "pause_before": 200},
        ),
        "CHK_T0000_P0000_END": (
            "obstacle",
            GARDEN,
            "papier,fenêtre",
            {"emphasis": "éclat de tiroir", "pause_before": 200},
        ),
        "CHK_T0000_P0000_END_F0001": (
            "ending",
            ENDING,
            "salle",
            {"emphasis": "éclat de tiroir", "pause_before": 200},
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
        raise SystemExit("BAN POL.001-06 : éclat de volet")
    if "éclat de poussière" in joined or "éclat de poussiere" in joined:
        raise SystemExit("BAN : éclat de poussière")
    for ban in (
        "cuivre", "buis", "coussin", "figue", "robinet", "planche",
        "cerceau", "émail", "email", "dalle", "plaque", "pierre",
        "grille", "couvercle", "cheminée", "cheminee", "couloir", "cour",
        "poussière", "poussiere",
    ):
        if re.search(rf"\b{ban}\b", joined):
            raise SystemExit(f"{SID}: BAN {ban}")
    if joined.count("en ce moment") != 1:
        raise SystemExit("en ce moment doit apparaître une fois")
    if "refuse de foncer" not in joined:
        raise SystemExit("manque refuse de foncer")
    if "nino ne dit rien" not in joined:
        raise SystemExit("silence Nino absent")
    if "tiroir" not in joined:
        raise SystemExit("tiroir du dump absent")
    if "volet" not in joined:
        raise SystemExit("volets du dump absents")
    if "colle" not in joined:
        raise SystemExit("colle du dump absente")
    if "salle à manger" not in joined:
        raise SystemExit("salle à manger du dump absente")
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
    if qtext != "Le corps n'est pas une blague. Que fait-on ?":
        raise SystemExit(f"question moteur altérée: {qtext}")
    if chunks[1].get("expected_answer") != "jouer":
        raise SystemExit("expected_answer altéré")
    retry = str(chunks[1].get("retry_prompt") or "")
    if "on joue" not in retry.lower():
        raise SystemExit("retry sans On joue")
    if "enfant-m|" in joined:
        raise SystemExit("enfant-m (Mila = enfant-f)")
    if "maitresse|" in joined or "maîtresse" in joined:
        raise SystemExit("maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if "copain" not in roles:
        raise SystemExit("Nino absent (copain)")
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
        "le corps n'est pas une blague",
        "corps n'est pas une blague",
        "pas une blague",
        "on joue",
        "vous jouez",
        "corps plus rond",
        "corps plus mince",
        "ne commente pas le corps",
        "l'amitié ne dépend",
        "l'amitie ne depend",
        "rient du jeu",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
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
        "- **Public :** N3 (≤16 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.COR.002 — le corps n'est pas une blague / jouer "
        "(vécue : Mila veut Nino debout maintenant ; il reste assis ; elle "
        "tire trop vite, l'anneau se déchire ; elle s'assoit à sa hauteur, "
        "dit d'accord ; plus tard elle tire vers le haut, la guirlande "
        "penche ; elle baisse le fil, deux bouts, deux hauteurs)\n"
        "- **Personnages :** Mila, Nino, papa, maman. Troupe D16 gardée. "
        "Maman ajoutée. Deux rythmes : Mila propose, Nino prend son temps "
        "ou pose sa limite. Le silence compte. Adultes parlants = "
        "papa/maman.\n"
        "- **Lieu :** salle à manger le matin, volets, tiroir de papiers, "
        "colle (monde dump, pas indice). Fil du buffet, ciseaux, chaise, "
        "papier rouge, fenêtre, torchon, gâteau.\n"
        "- **Indice unique :** éclat de tiroir (luit à l'ouverture, "
        "touché, luit au refus, reste pâle). Pas éclat de volet "
        "(BAN POL.001-06). Pas éclat de poussière. Pas cuivre / buis / "
        "coussin / figue / robinet / planche / cerceau / émail.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le tiroir de papiers est entrouvert. Ça sent la colle. Les volets "
        "laissent un rai mince. Sur le bois, un éclat de tiroir luit. Mila "
        "veut une guirlande jusqu'à la fenêtre **maintenant**, avec Nino. "
        "Première idée : « Tu viens coller, debout ? » trop vite, manche "
        "tirée. Il reste assis. L'anneau se déchire. Sourire parti, "
        "épaules basses. Maman se baisse. Elle refuse de foncer. Elle "
        "s'assoit. « Tu colles, assis ? » Il pousse un rectangle. "
        "« D'accord. » Merci vécu. Elle tire vers le haut : la guirlande "
        "penche. Nino dit Attends. Elle s'arrête, lit l'éclat. Deux bouts, "
        "deux hauteurs. La guirlande touche la fenêtre. Un éclat de tiroir "
        "reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salle à manger le matin, volets, rai mince, tiroir de "
        "papiers, colle sucrée, fil du buffet, ciseaux, chaise.\n"
        "- Désir : la guirlande jusqu'à la fenêtre, maintenant, avec Nino.\n"
        "- Objet : papier rouge, anneaux, colle, ciseaux, fil.\n"
        "- Indice unique : éclat de tiroir, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : l'anniversaire de papa, Nino qui vient de "
        "s'asseoir.\n"
        "- Imprévu 1 : invitation debout trop vite, manche tirée, Nino "
        "reste assis, anneau déchiré, colle sur le bois.\n"
        "- Cue : maman à la même hauteur. Un merci vécu, après d'accord.\n"
        "- Imprévu 2 (plus rusé) : elle tire vers le haut ; Nino reste "
        "collé à la chaise ; la guirlande penche ; un anneau se fend.\n"
        "- Résolution : elle refuse de foncer, s'assoit, dit d'accord ; "
        "puis baisse le fil à une hauteur que les deux tiennent.\n"
        "- Retour : torchon dur, tiroir qui se referme, chaise qui ne "
        "craque plus, éclat pâle, rai mince dans le rouge.\n\n"
        "## Vécu\n\n"
        "Mila veut la guirlande et Nino **debout, maintenant**. Impatience "
        "(manche trop vite, voix trop grande), puis sourire qui disparaît. "
        "Maman se baisse, pose une question, ne récite pas la règle. Nino "
        "dit rien, puis je reste assis, puis oui, puis attends, puis moi "
        "le bas. Mila dit d'accord. Merci vécu après l'écoute. Fin : "
        "l'éclat du début reste pâle.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : La guirlande d'anniversaire de Mila (noyau dump). "
        "Troupe D16 gardée : Mila, Nino, papa. Maman ajoutée.\n"
        "- Lieu du dump (salle à manger le matin, volets, tiroir de "
        "papiers, colle). Volets = monde, pas indice. ≠ POL.001-06 éclat "
        "de volet. ≠ rai de poussière d'or du dump (BAN poussière).\n"
        "- Ouverture inventée (tiroir entrouvert, colle sucrée, rai "
        "mince), pas un gabarit v2, pas « Mila est dans la salle ».\n"
        "- Indice unique : éclat de tiroir. Pas éclat de volet, pas "
        "poussière, cuivre, buis, coussin, figue, robinet, planche, "
        "cerceau, émail.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « encore » / « toute douce » du dump.\n"
        "- Leçon non dite : pas « le corps n'est pas une blague », pas "
        "« on joue », pas « corps plus rond / plus mince ». On la voit "
        "quand elle s'assoit à sa hauteur et baisse le fil.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Le corps n'est pas une blague. Que "
        "fait-on ? » expected jouer. retry inchangé. 5 chunks, kinds "
        "inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers la fenêtre.\n"
        "- example4 003 / 035 / 067 : corps (sourire parti, poitrine, "
        "accroupi), 2e ruse, refuse de foncer. Pas le gabarit v2.\n"
        f"- {nwords} mots. N3 ≤ 16. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n"
        "- 1 × `en ce moment`, 1 × merci adulte, 4 × éclat de tiroir\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
