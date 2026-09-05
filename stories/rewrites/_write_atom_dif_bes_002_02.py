#!/usr/bin/env python3
"""ATOM-DIF.BES.002-02 — Le cerf-volant de papier (F-NAR-019, N2, linéaire)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.002-02"
LIM = LIMITS["N2"]
TITLE = "Le cerf-volant de papier"
CHARS = "Mila, Aniss, papa, maman"
SETTING = (
    "terrasse, lavande, après la sieste, pierre chaude, tiges violettes"
)
INDICE = "éclat de pierre"
FIL = (
    "La pierre de la terrasse tient la chaleur. Sur la pierre, un éclat "
    "de pierre brille. Mila veut le cerf-volant au-dessus des tiges, "
    "maintenant. Elle lève trop vite : le papier tombe. Sourire parti. "
    "Elle tend la ficelle à Aniss : il retire les doigts, il regarde. "
    "Elle refuse de foncer, attend, dit d'accord. Merci vécu. Elle "
    "tire d'un coup : le papier plonge. Elle s'arrête, lit l'éclat, "
    "recule. Un éclat de pierre reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BAN_RE = re.compile(
    r"\b(plaque|carte|cartes|boule|galet|cube|bois)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "louise",
    "zoé",
    "zoe",
    "iris",
    "kenzo",
    "lila",
    "fanny",
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
    "voisine",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "trois notes",
    "une chose, puis la suivante",
    "une chose puis l'autre",
    "une étape après l'autre",
    "c'est du bon travail",
    "tu as fait du bon travail",
    "on aime écouter",
    "même leçon",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "c'est la règle",
    "c'est la regle",
    "grain de lavande",
    "grain de miette",
    "tache de couleur",
    "ombre en forme de flèche",
    "marque fine",
    "minuscule symbole",
    "éclat de lavande",
    "éclat de plaque",
    "éclat de carte",
    "éclat de boule",
    "éclat de galet",
    "éclat de cube",
    "éclat de bois",
    "éclat de croissant",
    "éclat de farine",
    "éclat de pompon",
    "cheval de bois",
    "on peut proposer",
    "on peut accepter",
    "plusieurs réponses",
    "c'est une réponse",
    "j'ai proposé",
    "j'ai accepté",
    "j'ai accepte",
    "tu as accepté",
    "tu as accepte",
    "tu as proposé",
    "tu as propose",
    "farine",
    "céréales",
    "cereales",
    "gâteau",
    "gateau",
    "collier",
    "raisins",
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
            "destinataire=enfant; sous_texte=elle_veut_le_cerf_volant_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis retenue; intensite=2; "
            "destinataire=enfant; "
            "sous_texte=aniss_regarde_ne_prend_pas_la_ficelle; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_invite_et_prend_la_reponse_d_aniss; "
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
            "destinataire=enfant; sous_texte=d_accord_laisse_aniss_regarder; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat_de_pierre; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_de_pierre_reste_pale; "
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
        if TICS.search(ph):
            raise SystemExit(f"{where} tic: {ph}")
        if BAN_RE.search(ph):
            raise SystemExit(f"{where} ban objet: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"{where} extra {bad}: {ph}")
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
    ("narrateur", "La pierre de la terrasse tient la chaleur."),
    ("narrateur", "Sous les paumes, elle brûle un peu."),
    ("enfant-f", "Elle est chaude, papa."),
    ("papa", "Tu le sens, toi ?"),
    ("enfant-f", "Oui, après la sieste."),
    ("maman", "Tes yeux sont un peu lourds."),
    ("enfant-f", "Un peu, maman."),
    ("narrateur", "Mila connaît cette terrasse."),
    ("narrateur", "Des tiges violettes bougent près du mur."),
    ("narrateur", "La lavande sent fort, près des pieds."),
    ("maman", "Je pose le chapeau sur le banc."),
    ("papa", "Je remplis le verre d'eau."),
    ("maman", "Tu entends les cigales, Mila ?"),
    ("enfant-f", "Oui, maman."),
    ("narrateur", "Des cigales chantent dans l'olivier."),
    ("narrateur", "Un cerf-volant de papier attend sur la chaise."),
    ("narrateur", "Il est bleu, avec une queue blanche."),
    ("enfant-f", "La ficelle est rêche."),
    ("papa", "Tu la tiens, Mila ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "Sur la pierre, un éclat de pierre brille."),
    ("enfant-f", "Il brille, maman !"),
    ("maman", "Tu le vois, sur la pierre ?"),
    ("enfant-f", "Oui, près de mes pieds."),
    ("enfant-f", "Je veux qu'il se lève, maintenant."),
    ("enfant-f", "Au-dessus des tiges."),
    ("maman", "Un petit vent suffit."),
    ("narrateur", "En ce moment, Mila prend le papier."),
    ("narrateur", "Il est léger et un peu froissé."),
    ("enfant-f", "Monte !"),
    ("narrateur", "Elle lève les bras trop vite."),
    ("narrateur", "La ficelle claque."),
    ("narrateur", "Le papier tombe contre les tiges."),
    ("enfant-f", "Oh."),
    ("narrateur", "Le sourire de Mila disparaît."),
    ("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
    ("enfant-f", "Je le prends !"),
    ("maman", "Le papier est dans les tiges."),
    ("papa", "Tu le vois, Mila ?"),
    ("narrateur", "Les épaules de Mila tombent un peu."),
    ("narrateur", "Ça serre, dans son ventre."),
    ("narrateur", "Papa se baisse à sa hauteur."),
)

OBSTACLE = L(
    ("narrateur", "Aniss est sur la marche."),
    ("narrateur", "Ses pieds restent à l'ombre."),
    ("enfant-f", "Tu viens ?"),
    ("narrateur", "Aniss ne dit rien."),
    ("narrateur", "Mila tient la ficelle trop près."),
    ("enfant-f", "Prends-la, maintenant !"),
    ("narrateur", "Elle pousse la ficelle vers sa main."),
    ("narrateur", "Aniss retire les doigts."),
    ("copain", "Je regarde."),
    ("enfant-f", "Oh."),
    ("narrateur", "Le papier tremble, trop bas."),
    ("narrateur", "Le papier reste sous les tiges."),
    ("papa", "Tu l'as vu, le papier ?"),
    ("enfant-f", "Il ne se lève pas."),
    ("maman", "Aniss est sur la marche."),
    ("enfant-f", "Plus tard ?"),
    ("copain", "Plus tard."),
    ("narrateur", "Mila avance d'un pas."),
    ("narrateur", "Aniss recule le pied."),
    ("enfant-f", "Tu veux la ficelle ?"),
    ("copain", "Non."),
    ("narrateur", "La queue blanche traîne."),
    ("narrateur", "Une abeille passe sur les tiges."),
    ("maman", "Tu l'entends, Mila ?"),
    ("enfant-f", "Oui."),
    ("papa", "On attend qu'elle parte."),
    ("narrateur", "Mila tient le papier bas."),
    ("narrateur", "L'abeille s'en va."),
    ("narrateur", "Les épaules restent basses."),
)

QUESTION = L(
    ("narrateur", "Mila invite Aniss."),
    ("narrateur", "Que fait-elle ?"),
)

CONFIRM = L(
    ("narrateur", "Mila avance trop vite vers Aniss."),
    ("enfant-f", "Tu viens, maintenant !"),
    ("narrateur", "Sa voix se mélange au vent."),
    ("enfant-f", "Oh."),
    ("narrateur", "Aniss reste sur la marche."),
    ("narrateur", "Mila refuse de foncer."),
    ("narrateur", "Elle referme la main."),
    ("narrateur", "Elle regarde la pierre, un instant."),
    ("papa", "Tu veux venir près de la pierre ?"),
    ("narrateur", "Papa s'accroupit à la même hauteur."),
    ("narrateur", "Mila pose un pied sur la pierre chaude."),
    ("enfant-f", "Tu viens ?"),
    ("narrateur", "Elle attend."),
    ("narrateur", "Aniss ne dit rien."),
    ("enfant-f", "D'accord."),
    ("copain", "Je regarde."),
    ("papa", "Merci, Mila."),
    ("narrateur", "Papa a entendu toute la phrase."),
    ("narrateur", "Le ventre de Mila se desserre."),
    ("narrateur", "Les épaules se relèvent un peu."),
    ("maman", "Tu as les mains au chaud ?"),
    ("enfant-f", "Un peu, maman."),
    ("narrateur", "Sur la pierre, un éclat de pierre tient."),
    ("enfant-f", "Il est là."),
    ("narrateur", "Mila lève le papier, sans tirer."),
    ("narrateur", "Un petit vent prend la queue."),
    ("copain", "Je vois."),
    ("maman", "Il tremble un peu."),
    ("enfant-f", "Il se lève."),
)

GARDEN = L(
    ("narrateur", "Mila tire la ficelle trop vite."),
    ("enfant-f", "Au-dessus des tiges, d'un coup !"),
    ("narrateur", "Le papier plonge dans les tiges."),
    ("enfant-f", "Oh."),
    ("narrateur", "Mila avance les mains."),
    ("narrateur", "Puis elle s'arrête net."),
    ("enfant-f", "Attends, je regarde."),
    ("narrateur", "Papa attend, sans parler."),
    ("narrateur", "Mila observe la pierre, écoute les cigales."),
    ("narrateur", "Sur la pierre, un éclat de pierre luit."),
    ("enfant-f", "Là, près de mes pieds."),
    ("narrateur", "Mila recule d'un pas."),
    ("narrateur", "Elle tient la ficelle des deux mains."),
    ("enfant-f", "Il est léger, papa."),
    ("papa", "Tu le portes vers le vent ?"),
    ("enfant-f", "Oui, papa."),
    ("maman", "On avance ?"),
    ("enfant-f", "Oui, maman."),
    ("narrateur", "Un petit vent arrive."),
    ("narrateur", "Le papier se lève un peu."),
    ("narrateur", "L'ombre passe sur les tiges."),
    ("enfant-f", "Tu vois l'ombre, Aniss ?"),
    ("copain", "Je regarde."),
    ("narrateur", "Aniss avance un pied."),
    ("narrateur", "Puis il le retire."),
    ("enfant-f", "D'accord."),
    ("maman", "On reste là."),
    ("narrateur", "La queue blanche danse."),
    ("narrateur", "Une tige violette se plie."),
    ("papa", "Le vent est juste assez."),
)

ENDING = L(
    ("enfant-f", "Le papier brillait, papa."),
    ("papa", "Tu le vois, comme sur la chaise ?"),
    ("enfant-f", "Oui, un peu froissé."),
    ("narrateur", "Mila pose le cerf-volant."),
    ("narrateur", "Il retrouve la chaise."),
    ("maman", "On le garde près de nous ?"),
    ("enfant-f", "Oui, maman."),
    ("enfant-f", "La lavande sentait fort."),
    ("maman", "Les tiges sont derrière nous."),
    ("narrateur", "Aniss secoue un pied."),
    ("narrateur", "Un peu de poussière tombe."),
    ("papa", "On rentre ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "Les joues de Mila se réchauffent."),
    ("narrateur", "La pierre reste chaude sous la main."),
    ("enfant-f", "Elle est chaude."),
    ("maman", "Comme tout à l'heure ?"),
    ("enfant-f", "Oui, maman."),
    ("papa", "La lumière est pâle, toi ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "Un éclat de pierre reste pâle."),
)


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: c for c in src["chunks"]}
    scripts = {
        "CHK_T0000_P0000": (
            "opening",
            OPENING,
            "terrasse,cigales",
            {"emphasis": "éclat de pierre"},
        ),
        "CHK_T0000_P0000_X": (
            "obstacle",
            OBSTACLE,
            "vent,papier",
            {"emphasis": "Je regarde", "pause_before": 200},
        ),
        "CHK_T0000_P0000_X_Q0001": (
            "clue",
            QUESTION,
            "",
            {
                "emphasis": "invite",
                "pause_before": 200,
                "fields": {
                    "expected_answer": "accepter",
                    "accepted_examples": (
                        "accepter | proposer | un non | regarder"
                    ),
                    "retry_prompt": (
                        "Elle propose. Aniss peut regarder. Que fait Mila ?"
                    ),
                    "engine_ok_text": "Oui, accepter.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_X_C0001": (
            "resolution",
            CONFIRM,
            "vent",
            {"emphasis": "D'accord", "pause_before": 200},
        ),
        "CHK_T0000_P0000_X_END": (
            "action",
            GARDEN,
            "vent,papier",
            {"emphasis": "éclat de pierre", "pause_before": 200},
        ),
        "CHK_T0000_P0000_X_END_F0001": (
            "ending",
            ENDING,
            "terrasse",
            {"emphasis": "éclat de pierre", "pause_before": 200},
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
    if joined.count("en ce moment") != 1:
        raise SystemExit("en ce moment doit apparaître une fois")
    if "refuse de foncer" not in joined:
        raise SystemExit("manque refuse de foncer")
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
    q = next(c for c in chunks if c["chunk_id"] == "CHK_T0000_P0000_X_Q0001")
    if q["text"] != "Mila invite Aniss. Que fait-elle ?":
        raise SystemExit(f"question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "accepter":
        raise SystemExit("expected_answer altéré")
    retry = str(q.get("retry_prompt") or "")
    if "mila" not in retry.lower():
        raise SystemExit("retry sans Mila")
    if "accepter" not in retry.lower() and "propose" not in retry.lower():
        raise SystemExit("retry hors moteur")
    if "enfant-m|" in joined:
        raise SystemExit("enfant-m (Mila = enfant-f, Aniss = copain)")
    if "maitresse|" in joined or "maîtresse|" in joined:
        raise SystemExit("maîtresse inventée")
    body = "\n".join(
        c["script"]
        for c in chunks
        if c["chunk_id"] != "CHK_T0000_P0000_X_Q0001"
    ).lower()
    for lesson in (
        "accepter",
        "accepte",
        "proposer",
        "propose",
        "plusieurs réponses",
        "c'est une réponse",
        "on peut proposer",
        "on peut accepter",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if "grain de lavande" in joined:
        raise SystemExit("BAN grain de lavande")
    if "éclat de lavande" in joined:
        raise SystemExit("BAN éclat de lavande")
    if "plaque" in joined:
        raise SystemExit("BAN 002-01 plaque")
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
        "- **Leçon :** DIF.BES.002 — inviter / proposer / accepter "
        "(vécue : Mila tend trop vite, Aniss retire les doigts et "
        "regarde ; elle attend, dit d'accord, laisse le silence)\n"
        "- **Personnages :** Mila, Aniss, papa, maman. Troupe D16. "
        "Mila = `enfant-f`. Aniss = `copain` (rythme lent, phrases "
        "courtes). Pas de maîtresse.\n"
        "- **Lieu :** terrasse, lavande, après la sieste, pierre chaude, "
        "tiges violettes, cigales, olivier. ≠ 002-01 cuisine / plaque / "
        "carton de céréales.\n"
        "- **Indice unique :** éclat de pierre (brille à l'ouverture, "
        "tient, luit au refus, reste pâle). Pas grain de lavande. Pas "
        "éclat de plaque / carte / boule / galet / cube / bois.\n"
        "- **Structure conservée :** 6 nœuds du dump (5 passages + "
        "question), `chunk_id` / `kind` / graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La pierre de la terrasse tient la chaleur. La sieste vient de "
        "finir. Des tiges violettes bougent. La lavande sent fort. Sur "
        "la pierre, un éclat de pierre brille. Mila veut le cerf-volant "
        "de papier **au-dessus des tiges, maintenant**. Première idée : "
        "lever trop vite. Le papier tombe. Sourire parti, épaules "
        "basses. Aniss est sur la marche, à l'ombre. Elle pousse la "
        "ficelle : il retire les doigts. « Je regarde. » « Plus tard. » "
        "« Non. » Silence. Elle refuse de foncer, attend, dit d'accord. "
        "Merci vécu. Elle tire d'un coup : le papier plonge. Elle "
        "s'arrête, lit l'éclat, recule. Un petit vent lève la queue. "
        "Aniss avance un pied, puis le retire. Un éclat de pierre reste "
        "pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : terrasse après la sieste, pierre chaude, lavande, "
        "tiges violettes, cigales, olivier, chaise, chapeau, verre d'eau. "
        "≠ 002-01 cuisine / plaque / farine / cheval.\n"
        "- Désir : lever le cerf-volant bleu au-dessus des tiges, "
        "maintenant.\n"
        "- Objet : cerf-volant de papier, ficelle rêche, queue blanche.\n"
        "- Indice unique : éclat de pierre, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : le papier doit se lever avant que le vent parte.\n"
        "- Imprévu 1 : bras trop vite ; le papier tombe. Puis Aniss ne "
        "prend pas la ficelle.\n"
        "- Cue : papa à la même hauteur, près de la pierre. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : tirer d'un coup, papier dans les tiges.\n"
        "- Résolution : elle refuse de foncer, attend, dit d'accord ; "
        "puis recule, lit l'éclat, laisse le vent.\n"
        "- Retour : cerf-volant sur la chaise, pierre chaude, éclat pâle, "
        "poussière sous le pied d'Aniss.\n\n"
        "## Vécu\n\n"
        "Mila veut le cerf-volant **maintenant**. Impatience, puis sourire "
        "qui disparaît. Aniss a un autre rythme : il regarde, il dit non, "
        "il se tait. Papa se baisse, pose une question, ne récite pas la "
        "règle. Mila agit : main fermée, attente, d'accord. Merci vécu "
        "après l'écoute. Fin : l'éclat du début reste pâle.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le cerf-volant de papier (noyau dump). Kenzo / Lila "
        "du TTS dump → INTERDIT. Aniss = copain D16.\n"
        "- Lieu du dump (terrasse, lavande, après la sieste, pierre "
        "chaude, tiges violettes). ≠ 002-01 cuisine / plaque.\n"
        "- Ouverture inventée (pierre qui tient la chaleur), pas un "
        "gabarit v2, pas « Mila est sur la terrasse ».\n"
        "- Indice unique : éclat de pierre. Pas grain de lavande. Pas "
        "plaque, carte, boule, galet, cube, bois.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « encore » du dump (pierre encore chaude, "
        "chantent encore, sent encore).\n"
        "- Leçon non dite : on la voit quand elle dit d'accord et "
        "laisse Aniss sur la marche. Pas « on peut proposer », pas "
        "« plusieurs réponses sont possibles », pas « j'ai accepté ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur gardée : « Mila invite Aniss. Que "
        "fait-elle ? » expected accepter. retry dump conservé.\n"
        "- TTS complet (6) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin.\n"
        "- example4 : 087 / 019 / 051 (ouverture sensorielle, indice "
        "payé, 2e ruse, refuse de foncer). Voix Mila = 001-07. Aniss "
        "= 002-05 (phrases courtes, rythme lent).\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 6 chunks dump, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
