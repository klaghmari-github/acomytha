#!/usr/bin/env python3
"""ATOM-DIF.BES.002-07 — La lettre de Mila (F-NAR-019, N1, linéaire)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.002-07"
LIM = 10
TITLE = "La lettre de Mila"
CHARS = "Mila, Victorina, papa, maman"
SETTING = (
    "bureau près du salon, porte de la cuisine, tiroir, "
    "gomme rose, rayon, volet, enveloppe"
)
INDICE = "éclat d'enveloppe"
FIL = (
    "Le tiroir sent le papier. Une gomme rose roule. Un rayon entre "
    "par le volet. Sur le rabat, un éclat d'enveloppe luit. Mila veut "
    "glisser la lettre-soleil sous la porte, maintenant, avec Victorina. "
    "Elle tend trop vite : non, l'autocollant colle, le soleil reste hors. "
    "Sourire parti. Elle refuse de foncer, attend le silence, dit d'accord. "
    "Merci vécu. Elle pousse d'un coup : l'enveloppe se coince. Elle "
    "s'arrête, lit l'éclat. Un éclat d'enveloppe reste pâle."
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
    r"\b(dalle|plaque|pierre|grille|couvercle|cheminée|cheminee|"
    r"couloir|cour|poussière|poussiere)\b",
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
            "destinataire=enfant; sous_texte=elle_veut_la_lettre_et_victorina_maintenant; "
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
            "sous_texte=mila_invite_sans_forcer; "
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
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat_d_enveloppe; "
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
            "sous_texte=l_eclat_d_enveloppe_reste_pale; "
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
    ("narrateur", "Le tiroir du bureau sent le papier."),
    ("narrateur", "Une gomme rose roule, sans bruit."),
    ("narrateur", "Le bureau est près du salon."),
    ("narrateur", "Mila connaît ce tiroir, ce bureau."),
    ("narrateur", "Un rayon entre par le volet."),
    ("enfant-f", "Il est chaud, maman."),
    ("maman", "Tu le sens, sur tes mains ?"),
    ("enfant-f", "Oui, un peu."),
    ("narrateur", "Le rayon fait un rectangle clair."),
    ("narrateur", "Il tient sur le bureau."),
    ("papa", "J'épluche les carottes, là."),
    ("papa", "Derrière la porte, dans la cuisine."),
    ("enfant-f", "Je t'écris, papa."),
    ("maman", "Une lettre, pour lui ?"),
    ("enfant-f", "Oui, maintenant."),
    ("narrateur", "Une enveloppe jaune attend."),
    ("narrateur", "Le rabat est un peu luisant."),
    ("narrateur", "Sur le rabat, un éclat d'enveloppe luit."),
    ("enfant-f", "Il brille, maman !"),
    ("maman", "Tu le vois, sur l'enveloppe ?"),
    ("enfant-f", "Oui, près du rabat."),
    ("narrateur", "Mila touche l'éclat d'enveloppe, un instant."),
    ("narrateur", "Le papier est lisse, un peu chaud."),
    ("enfant-f", "Elle est tiède."),
    ("papa", "Tu restes près du bureau ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "En ce moment, Mila prend le crayon."),
    ("narrateur", "Le crayon est lisse, bleu."),
    ("narrateur", "Elle dessine un soleil."),
    ("narrateur", "Le soleil a des rayons ronds."),
    ("maman", "Il est beau, ce soleil."),
    ("enfant-f", "Il est pour papa."),
    ("narrateur", "Maman ouvre la porte de la cuisine."),
    ("narrateur", "Victorina arrive, près du tapis."),
    ("narrateur", "Elle reste un moment, les mains collées."),
    ("enfant-f", "Tu viens ?"),
    ("enfant-f", "On colle le soleil."),
    ("copine", "Non."),
    ("narrateur", "Mila tend l'autocollant trop vite."),
    ("narrateur", "Il colle à son doigt."),
    ("enfant-f", "Il reste !"),
    ("enfant-f", "Tu le prends, maintenant !"),
    ("copine", "Non."),
    ("narrateur", "Victorina recule d'un pas."),
    ("narrateur", "Le soleil reste hors de l'enveloppe."),
    ("narrateur", "Le sourire de Mila disparaît."),
    ("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
    ("enfant-f", "Je le mets !"),
    ("maman", "L'enveloppe n'est pas fermée."),
    ("papa", "Tu le vois, Mila ?"),
    ("narrateur", "Les épaules de Mila tombent un peu."),
    ("narrateur", "Ça serre, dans son ventre."),
    ("narrateur", "Maman se baisse à sa hauteur."),
)

QUESTION = L(
    ("narrateur", "Mila invite Victorina."),
    ("narrateur", "Que fait-on ?"),
)

CONFIRM = L(
    ("narrateur", "Mila avance trop vite vers l'enveloppe."),
    ("enfant-f", "Tu viens, maintenant !"),
    ("narrateur", "Sa voix se mélange au papier."),
    ("enfant-f", "Oh."),
    ("narrateur", "Victorina reste près du tapis."),
    ("narrateur", "Mila refuse de foncer."),
    ("narrateur", "Elle referme la main."),
    ("maman", "Tu veux venir près du bureau ?"),
    ("narrateur", "Maman s'accroupit à la même hauteur."),
    ("narrateur", "Mila pose un genou près du tiroir."),
    ("enfant-f", "Tu regardes ?"),
    ("narrateur", "Victorina ne dit rien."),
    ("narrateur", "Ses mains restent collées."),
    ("enfant-f", "Plus tard, tu viens ?"),
    ("copine", "Je regarde."),
    ("enfant-f", "D'accord."),
    ("papa", "Merci, Mila."),
    ("narrateur", "Papa a entendu toute la phrase."),
    ("narrateur", "Le ventre de Mila se desserre."),
    ("narrateur", "Les épaules se relèvent un peu."),
    ("maman", "Tu as les mains au chaud ?"),
    ("enfant-f", "Un peu, maman."),
    ("narrateur", "Mila frotte le doigt au bureau."),
    ("narrateur", "L'autocollant se décolle."),
    ("enfant-f", "Il vient !"),
    ("maman", "Le soleil est là."),
    ("narrateur", "Mila pose le soleil dans l'enveloppe."),
    ("narrateur", "Elle colle le rouge, sans presser."),
    ("enfant-f", "Tu veux fermer ?"),
    ("copine", "Plus tard."),
    ("enfant-f", "D'accord."),
    ("narrateur", "Victorina s'assoit près du tapis."),
    ("narrateur", "Elle regarde le rabat."),
    ("papa", "Ça sent la carotte, ici."),
    ("enfant-f", "Ma lettre aussi."),
    ("narrateur", "Le crayon roule un peu."),
    ("narrateur", "Mila le rattrape."),
    ("maman", "Tu as fini de dessiner ?"),
    ("enfant-f", "Presque."),
)

GARDEN = L(
    ("narrateur", "Mila pousse l'enveloppe trop vite."),
    ("enfant-f", "Je la glisse, d'un coup !"),
    ("narrateur", "Le papier se plie sous la porte."),
    ("narrateur", "L'enveloppe reste coincée."),
    ("enfant-f", "Oh."),
    ("narrateur", "Le soleil ne passe pas."),
    ("enfant-f", "Je la prends !"),
    ("narrateur", "Mila avance la main vers Victorina."),
    ("maman", "Tu l'attends, Mila ?"),
    ("narrateur", "Victorina ne bouge pas."),
    ("narrateur", "Ses mains restent sur ses genoux."),
    ("enfant-f", "Attends, je regarde."),
    ("narrateur", "Mila s'arrête net."),
    ("narrateur", "Maman attend, sans parler."),
    ("enfant-f", "Je regarde."),
    ("narrateur", "Mila observe l'enveloppe, écoute la cuisine."),
    ("narrateur", "Sur le rabat, un éclat d'enveloppe luit."),
    ("enfant-f", "Là, près du rabat."),
    ("narrateur", "Mila tient l'enveloppe des deux mains."),
    ("narrateur", "Le papier est lisse, un peu tiède."),
    ("enfant-f", "Elle est tiède, papa."),
    ("papa", "Tu la portes jusqu'à la porte ?"),
    ("enfant-f", "Oui, papa."),
    ("maman", "On avance ?"),
    ("enfant-f", "Oui, maman."),
    ("narrateur", "Mila aplatit le papier, sans forcer."),
    ("narrateur", "Elle glisse l'enveloppe, très peu."),
    ("enfant-f", "Elle passe."),
    ("copine", "Le rabat aussi, après."),
    ("narrateur", "Victorina tend la main."),
    ("narrateur", "Elle pousse un tout petit bord."),
    ("papa", "Il y a une lettre !"),
    ("enfant-f", "C'est le soleil !"),
    ("papa", "Je l'ouvre ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "La porte s'ouvre un peu."),
    ("narrateur", "Ça sent la carotte chaude."),
    ("papa", "Le soleil est pour moi ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "Mila pose le crayon près du tiroir."),
    ("narrateur", "Victorina pose la gomme rose."),
)

ENDING = L(
    ("enfant-f", "L'enveloppe brillait, papa."),
    ("papa", "Tu le vois, comme tout à l'heure ?"),
    ("enfant-f", "Oui, sur le rabat."),
    ("narrateur", "Mila pose le soleil près des carottes."),
    ("maman", "On le garde près de nous ?"),
    ("enfant-f", "Oui, maman."),
    ("enfant-f", "Ça sentait le papier."),
    ("maman", "Le tiroir est là."),
    ("narrateur", "L'enveloppe reste ouverte, vide."),
    ("narrateur", "Mila respire, plus large."),
    ("papa", "On reste un peu ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "Les joues de Mila se réchauffent."),
    ("narrateur", "Le crayon reste tiède sous la main."),
    ("narrateur", "Le rayon a glissé sur le bureau."),
    ("enfant-f", "Il est pâle."),
    ("maman", "Comme tout à l'heure ?"),
    ("enfant-f", "Oui, maman."),
    ("papa", "Le rabat est luisant, toi ?"),
    ("enfant-f", "Un peu, papa."),
    ("narrateur", "La gomme rose ne roule plus."),
    ("enfant-f", "Elle est tiède."),
    ("maman", "On la laisse au bureau ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "Un éclat d'enveloppe reste pâle."),
)


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: c for c in src["chunks"]}
    scripts = {
        "CHK_T0000_P0000": (
            "opening",
            OPENING,
            "tiroir,papier",
            {"emphasis": "éclat d'enveloppe"},
        ),
        "CHK_T0000_P0000_Q0001": (
            "clue",
            QUESTION,
            "",
            {
                "emphasis": "Victorina",
                "pause_before": 200,
                "fields": {
                    "expected_answer": "proposer",
                    "accepted_examples": (
                        "proposer | inviter | accepter | d'accord"
                    ),
                    "retry_prompt": (
                        "On peut proposer. On peut accepter. Que fait-on ?"
                    ),
                    "engine_ok_text": "Oui, proposer.",
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
            "papier,porte",
            {"emphasis": "éclat d'enveloppe", "pause_before": 200},
        ),
        "CHK_T0000_P0000_END_F0001": (
            "ending",
            ENDING,
            "cuisine",
            {"emphasis": "éclat d'enveloppe", "pause_before": 200},
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
    for ban in (
        "dalle", "plaque", "pierre", "grille", "couvercle",
        "cheminée", "cheminee", "couloir", "cour", "poussière", "poussiere",
    ):
        if re.search(rf"\b{ban}\b", joined):
            raise SystemExit(f"{SID}: BAN {ban}")
    if joined.count("en ce moment") != 1:
        raise SystemExit("en ce moment doit apparaître une fois")
    if "refuse de foncer" not in joined:
        raise SystemExit("manque refuse de foncer")
    if "victorina ne dit rien" not in joined:
        raise SystemExit("silence Victorina absent")
    if "gomme rose" not in joined:
        raise SystemExit("gomme rose du dump absente")
    if "tiroir" not in joined:
        raise SystemExit("tiroir du dump absent")
    if "volet" not in joined:
        raise SystemExit("volet du dump absent")
    if "enveloppe" not in joined:
        raise SystemExit("enveloppe du dump absente")
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
    if qtext != "Mila invite Victorina. Que fait-on ?":
        raise SystemExit(f"question moteur altérée: {qtext}")
    if chunks[1].get("expected_answer") != "proposer":
        raise SystemExit("expected_answer altéré")
    retry = str(chunks[1].get("retry_prompt") or "")
    if "proposer" not in retry.lower():
        raise SystemExit("retry sans proposer")
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
        raise SystemExit("Victorina absente (copine)")
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
        "on peut proposer",
        "on peut accepter",
        "plusieurs réponses",
        "j'ai proposé",
        "j'ai accepté",
        "proposer",
        "inviter",
        "accepter",
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
        "- **Public :** N1 (≤10 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.BES.002 — inviter / proposer / accepter "
        "(vécue : Mila tend trop vite, Victorina dit non ; elle attend "
        "son silence, dit d'accord ; Victorina pousse un bord plus tard)\n"
        "- **Personnages :** Mila, Victorina, papa, maman. Troupe D16 "
        "gardée. Deux rythmes : Mila propose, Victorina prend son temps "
        "ou pose sa limite. Le silence compte. Adultes parlants = "
        "papa/maman.\n"
        "- **Lieu :** bureau près du salon, porte de la cuisine, tiroir, "
        "gomme rose, rayon, volet, enveloppe (monde dump, pas indice).\n"
        "- **Indice unique :** éclat d'enveloppe (luit à l'ouverture, "
        "touché, luit au refus, reste pâle). Pas éclat de volet "
        "(BAN POL.001-06). Pas dalle / plaque / pierre / grille / "
        "couvercle / cheminée / couloir / cour / poussière.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le tiroir du bureau sent le papier. Une gomme rose roule. Un "
        "rayon entre par le volet. Sur le rabat, un éclat d'enveloppe "
        "luit. Mila veut glisser la lettre-soleil sous la porte "
        "**maintenant**, avec Victorina. Première idée : « Tu viens ? "
        "On colle le soleil. » trop vite, autocollant collé au doigt. "
        "Elle dit non. Le soleil reste hors. Sourire parti, épaules "
        "basses. Maman se baisse. Elle refuse de foncer. Elle attend "
        "son silence. « Tu regardes ? » Elle regarde. « D'accord. » "
        "Merci vécu. Elle pousse d'un coup : l'enveloppe se coince. "
        "Elle tend la main : Victorina ne bouge pas. Elle s'arrête, "
        "lit l'éclat. L'enveloppe passe. Papa ouvre. Un éclat "
        "d'enveloppe reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : bureau près du salon, tiroir, gomme rose, rayon par "
        "le volet, enveloppe jaune, porte de la cuisine, carottes.\n"
        "- Désir : la lettre-soleil sous la porte, maintenant, avec "
        "Victorina.\n"
        "- Objet : enveloppe, soleil dessiné, autocollant, crayon, gomme.\n"
        "- Indice unique : éclat d'enveloppe, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : Victorina au tapis, le message qui doit passer.\n"
        "- Imprévu 1 : invitation trop vite, autocollant collé, non, "
        "soleil hors de l'enveloppe. Le message n'est pas fini.\n"
        "- Cue : maman à la même hauteur. Un merci vécu, après d'accord.\n"
        "- Imprévu 2 (plus rusé) : enveloppe coincée sous la porte ; "
        "elle veut sa main ; elle ne bouge pas.\n"
        "- Résolution : elle refuse de foncer, attend, dit d'accord ; "
        "Victorina pousse un bord quand elle veut.\n"
        "- Retour : soleil près des carottes, gomme qui ne roule plus, "
        "éclat pâle.\n\n"
        "## Vécu\n\n"
        "Mila veut la lettre et Victorina **maintenant**. Impatience "
        "(main trop vite, voix trop grande), puis sourire qui disparaît. "
        "Maman se baisse, pose une question, ne récite pas la règle. "
        "Victorina dit non, puis rien, puis je regarde, puis plus tard. "
        "Mila dit d'accord. Merci vécu après l'écoute. Fin : l'éclat du "
        "début reste pâle.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : La lettre de Mila (noyau dump). Troupe D16 gardée : "
        "Mila, Victorina, papa, maman. Pas Amandine / Nora du TTS source.\n"
        "- Lieu du dump (bureau près du salon, porte de la cuisine, "
        "tiroir, gomme rose, rayon, volet, enveloppe). Volet = monde, "
        "pas indice. ≠ POL.001-06 éclat de volet. ≠ BES.002-01 plaque. "
        "≠ BES.002-06 dalle / cour.\n"
        "- Ouverture inventée (tiroir qui sent le papier, gomme qui "
        "roule), pas un gabarit v2, pas « Mila est dans le bureau ».\n"
        "- Indice unique : éclat d'enveloppe. Pas éclat de volet, pas "
        "dalle, plaque, pierre, grille, couvercle, cheminée, couloir, "
        "cour, poussière.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « déjà » du dump.\n"
        "- Leçon non dite : pas « on peut proposer », pas « plusieurs "
        "réponses », pas « tu as proposé ». On la voit quand elle attend "
        "le silence et dit d'accord.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Mila invite Victorina. Que fait-on ? » "
        "expected proposer. retry inchangé. 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers l'enveloppe.\n"
        f"- {nwords} mots. N1 ≤ 10. `check()` OK. Pas apply.\n\n"
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
