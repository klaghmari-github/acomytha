#!/usr/bin/env python3
"""ATOM-COL.POL.001-12 — Le panier de Mila (F-NAR-019, N3, linéaire)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "ATOM-COL.POL.001-12"
LIM = 16
TITLE = "Le panier de Mila"
CHARS = "Mila, papa, maman"
SETTING = (
    "marché, chat sous table, caisse de fromages, "
    "petite balance, panier"
)
INDICE = "éclat de panier"
FIL = (
    "Une moustache du chat touche le pied de table. Sur le bord, "
    "un éclat de panier brille. Mila veut le rond pâle maintenant. "
    "Elle parle trop vite, sans le mot : la dame n'a pas levé les "
    "yeux. Elle refuse de foncer, dit bonjour. Merci vécu. Le panier "
    "penche vers le chat. Un éclat de panier reste pâle."
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
    "on dit bonjour",
    "tu as dit les mots",
    "les trois mots",
    "tu as dit merci",
    "tu as dit s'il te plaît",
    "tu as dit s'il te plait",
    "tu demandes",
    "honoré",
    "honore",
    "fanny",
    "gaufre",
    "pavé",
    "pave",
    "petit pain",
    "croissant",
    "farine",
    "cloche",
    "corbeille",
    "réverbère",
    "reverbere",
    "bâche",
    "bache",
    "volet",
    "zeste",
    "parapluie",
    "poire",
    "œuf",
    "oeuf",
    "poule",
    "paille",
    "gâteau",
    "gateau",
    "éclat de sac",
    "éclat de cloche",
    "éclat de corbeille",
    "éclat de croissant",
    "éclat de farine",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de poisson",
    "éclat de parapluie",
    "éclat de citron",
    "éclat de bâche",
    "éclat de bache",
    "éclat de volet",
    "éclat de poire",
    "grain de miette",
    "tache de couleur",
    "ombre en forme",
    "marque fine",
    "minuscule symbole",
    "une chose, puis",
    "une chose puis",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "vanille",
    "pigeon",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "maîtresse",
    "maitresse",
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
            "destinataire=enfant; sous_texte=elle_veut_le_rond_pale_maintenant; "
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
            "sous_texte=elle_dit_bonjour_a_la_dame; "
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
            "destinataire=enfant; sous_texte=bonjour_ouvre_le_panier; "
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
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat_de_panier; "
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
            "sous_texte=l_eclat_de_panier_reste_pale; "
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
    ("narrateur", "Une moustache du chat touche le pied de table."),
    ("narrateur", "Le chat dort, rond, sous le bois."),
    ("narrateur", "Sa queue frôle une caisse de fromages."),
    ("narrateur", "Ça sent le lait, et un peu le foin."),
    ("enfant-f", "Ça sent le lait, papa."),
    ("papa", "Tu le sens, toi ?"),
    ("enfant-f", "Oui, et le foin."),
    ("maman", "Le soleil touche tes joues."),
    ("enfant-f", "Elles sont tièdes, maman."),
    ("narrateur", "Papa tient la main de Mila."),
    ("narrateur", "Sa paume sent un peu le foin."),
    ("papa", "Tu as du foin, Mila ?"),
    ("enfant-f", "Un peu, papa."),
    ("narrateur", "Maman tend le panier, vide et léger."),
    ("enfant-f", "Il est léger, maman."),
    ("maman", "Parce qu'il est vide."),
    ("papa", "Tu as vu le chat, Mila ?"),
    ("enfant-f", "Il dort sous la table."),
    ("papa", "On le laisse."),
    ("narrateur", "Des voix passent, plus loin, sur la place."),
    ("narrateur", "Une petite balance fait tic, près de la caisse."),
    ("enfant-f", "Elle fait tic, maman."),
    ("maman", "C'est la balance, près des ronds."),
    ("narrateur", "Le bois de la table sent le soleil."),
    ("enfant-f", "Il est chaud, maman."),
    ("maman", "Et le plateau, lui, est froid."),
    ("narrateur", "Un filet de soleil tombe sur le bord."),
    ("narrateur", "Sur le bord, un éclat de panier brille."),
    ("enfant-f", "Il brille, papa !"),
    ("papa", "Tu le vois, sur le panier ?"),
    ("enfant-f", "Oui, près du bord."),
    ("narrateur", "Les ronds de la caisse sont pâles, un peu froids."),
    ("enfant-f", "Celui-là, papa."),
    ("papa", "Celui près de la queue ?"),
    ("enfant-f", "Oui, le pâle."),
    ("enfant-f", "Je le veux, maintenant."),
    ("narrateur", "En ce moment, Mila avance vers la table."),
    ("narrateur", "La dame essuie le plateau de la balance."),
    ("narrateur", "Le métal est froid, malgré le soleil."),
    ("enfant-f", "Celui-là !"),
    ("narrateur", "Mila parle trop vite vers la table."),
    ("narrateur", "Sa voix se mélange au tic de la balance."),
    ("narrateur", "La dame n'a pas levé les yeux."),
    ("enfant-f", "Oh."),
    ("narrateur", "Le rond pâle reste dans la caisse."),
    ("narrateur", "Le sourire de Mila disparaît."),
    ("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
    ("enfant-f", "Je le prends !"),
    ("maman", "Le fromage est sur la table."),
    ("papa", "Tu le vois, Mila ?"),
    ("narrateur", "Les épaules de Mila tombent un peu."),
    ("narrateur", "Ça serre, dans son ventre."),
    ("narrateur", "Papa se baisse à sa hauteur."),
)

QUESTION = L(
    ("narrateur", "Mila parle à la dame."),
    ("narrateur", "Quels mots dit-elle ?"),
)

CONFIRM = L(
    ("narrateur", "Mila avance trop vite vers la table."),
    ("enfant-f", "Celui-là, maintenant !"),
    ("narrateur", "Sa voix se mélange au tic."),
    ("enfant-f", "Oh."),
    ("narrateur", "Le rond pâle reste dans la caisse."),
    ("narrateur", "La dame essuie, sans lever les yeux."),
    ("narrateur", "Mila refuse de foncer."),
    ("narrateur", "Elle referme la main sur le panier."),
    ("narrateur", "Elle écoute la balance, un instant."),
    ("papa", "Tu veux venir près de la table ?"),
    ("narrateur", "Papa s'accroupit à la même hauteur."),
    ("narrateur", "Mila pose un pied près du bois."),
    ("narrateur", "Le plateau de la balance est froid."),
    ("enfant-f", "Bonjour."),
    ("enfant-f", "Celui-là."),
    ("enfant-f", "S'il te plaît."),
    ("narrateur", "La dame pose le chiffon."),
    ("narrateur", "Elle lève les yeux."),
    ("narrateur", "Une main coupe un rond pâle."),
    ("narrateur", "La petite balance fait tic."),
    ("narrateur", "Elle glisse le rond dans le panier."),
    ("narrateur", "Le papier est froid, un peu gras."),
    ("papa", "Merci, Mila."),
    ("narrateur", "Papa a entendu toute la phrase."),
    ("narrateur", "Le ventre de Mila se desserre."),
    ("narrateur", "Les épaules se relèvent un peu."),
    ("maman", "Tu as les mains au frais ?"),
    ("enfant-f", "Un peu, maman."),
    ("narrateur", "Ça sent le lait, près d'elle."),
    ("enfant-f", "Le fromage est à moi."),
    ("maman", "Il est dans ton panier."),
    ("narrateur", "Mila pose une main sur le bord."),
    ("narrateur", "Le bord est un peu rêche."),
    ("narrateur", "Sur le bord, un éclat de panier tient."),
    ("narrateur", "La balance se tait."),
)

GARDEN = L(
    ("narrateur", "Mila lève le panier trop vite."),
    ("enfant-f", "Je le montre, d'un coup !"),
    ("narrateur", "Le bord penche entre les doigts."),
    ("narrateur", "Le fromage penche vers le chat."),
    ("enfant-f", "Oh."),
    ("narrateur", "Mila avance les mains."),
    ("narrateur", "Puis elle s'arrête net."),
    ("enfant-f", "Attends, je regarde."),
    ("narrateur", "Papa attend, sans parler."),
    ("narrateur", "Mila refuse de foncer, cette fois."),
    ("narrateur", "Elle observe le panier, écoute le marché."),
    ("narrateur", "Sur le bord, un éclat de panier luit."),
    ("enfant-f", "Là, près du bord."),
    ("narrateur", "Mila tient le panier des deux mains."),
    ("narrateur", "Le bord est rêche, un peu froid."),
    ("enfant-f", "Il est froid, papa."),
    ("papa", "Tu le portes jusqu'à la place ?"),
    ("enfant-f", "Oui, papa."),
    ("maman", "On marche ?"),
    ("enfant-f", "Oui, maman."),
    ("narrateur", "Le chat ouvre un œil, puis se recouche."),
    ("enfant-f", "Il dort."),
    ("papa", "On le laisse."),
    ("narrateur", "Mila serre le panier contre elle."),
    ("enfant-f", "Le fromage reste."),
    ("narrateur", "Le panier penche, puis se cale."),
    ("enfant-f", "Je le tiens."),
    ("maman", "On avance."),
    ("narrateur", "Mila passe près de la table."),
    ("narrateur", "La caisse reste derrière."),
)

ENDING = L(
    ("enfant-f", "Le panier brillait, papa."),
    ("papa", "Tu le vois, comme à la table ?"),
    ("enfant-f", "Oui, sur le bord."),
    ("narrateur", "Mila pose le panier contre son bras."),
    ("maman", "On le garde au frais ?"),
    ("enfant-f", "Oui, maman."),
    ("enfant-f", "Le lait sentait bon."),
    ("maman", "Il est contre toi."),
    ("narrateur", "Une odeur de foin reste dans le panier."),
    ("narrateur", "Mila respire, plus large."),
    ("papa", "On rentre ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "Les joues de Mila se réchauffent."),
    ("narrateur", "Le panier reste froid sous la main."),
    ("narrateur", "Le chat dort sous la table."),
    ("enfant-f", "Il n'a pas bougé."),
    ("maman", "Comme tout à l'heure ?"),
    ("enfant-f", "Oui, maman."),
    ("papa", "Le soleil est sur le bord, toi ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "Un éclat de panier reste pâle."),
)


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: c for c in src["chunks"]}
    scripts = {
        "CHK_T0000_P0000": (
            "opening",
            OPENING,
            "chat,balance",
            {"emphasis": "éclat de panier"},
        ),
        "CHK_T0000_P0000_Q0001": (
            "clue",
            QUESTION,
            "",
            {
                "emphasis": "dame",
                "pause_before": 200,
                "fields": {
                    "expected_answer": "bonjour",
                    "accepted_examples": (
                        "bonjour | s'il te plaît | merci | bonjour merci"
                    ),
                    "retry_prompt": (
                        "Elle dit bonjour. Quels mots dit Mila ?"
                    ),
                    "engine_ok_text": "Oui, bonjour.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": (
            "resolution",
            CONFIRM,
            "papier,balance",
            {"emphasis": "Bonjour"},
        ),
        "CHK_T0000_P0000_END": (
            "obstacle",
            GARDEN,
            "panier,pas",
            {"emphasis": "éclat de panier"},
        ),
        "CHK_T0000_P0000_END_F0001": (
            "ending",
            ENDING,
            "pas",
            {"emphasis": "éclat de panier", "pause_before": 200},
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
    bans = (
        "honoré",
        "honore",
        "fanny",
        "croissant",
        "farine",
        "cloche",
        "corbeille",
        "réverbère",
        "reverbere",
        "bâche",
        "volet",
        "pavé",
        "pave",
        "zeste",
        "parapluie",
        "poire",
        "œuf",
        "oeuf",
        "poule",
        "paille",
        "gâteau",
        "gateau",
        "gaufre",
        "sachet",
    )
    for ban in bans:
        if ban in joined:
            raise SystemExit(f"BAN « {ban} »")
    if re.search(r"\bsac\b", joined):
        raise SystemExit("BAN POL.001-11 : sac")
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
    qtext = chunks[1]["text"]
    if qtext != "Mila parle à la dame. Quels mots dit-elle ?":
        raise SystemExit(f"question moteur altérée: {qtext}")
    if chunks[1].get("expected_answer") != "bonjour":
        raise SystemExit("expected_answer altéré")
    retry = str(chunks[1].get("retry_prompt") or "")
    if "honoré" in retry.lower() or "honore" in retry.lower():
        raise SystemExit("retry Honoré resté")
    if "mila" not in retry.lower():
        raise SystemExit("retry sans Mila")
    if "enfant-m|" in joined:
        raise SystemExit("enfant-m (Mila = enfant-f)")
    if "maitresse|" in joined or "maîtresse" in joined:
        raise SystemExit("maîtresse inventée")
    dame_speech = [
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("maitresse|")
    ]
    if dame_speech:
        raise SystemExit("la dame a un rôle parlé")
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
    relecture(
        SID,
        TITLE,
        (
            "Mila veut le rond pâle de la caisse. Éclat de panier sur le "
            "bord. Marché, chat sous table, caisse de fromages, petite "
            "balance. Elle parle trop vite, sans bonjour : la dame n'a "
            "pas levé les yeux. Sourire parti. Elle refuse de foncer, "
            "dit bonjour, puis s'il te plaît. Le rond glisse dans le "
            "panier. Merci vécu. Elle veut montrer d'un coup : le panier "
            "penche vers le chat. Elle s'arrête, lit l'éclat. Un éclat "
            "de panier reste pâle."
        ),
        (
            f"Réécriture éditoriale F-NAR-019, example4 v2 (076, 008, "
            f"040). `chunk_id` / `kind` inchangés. Texte seulement. Pas "
            f"d'apply. Pas de git. Pas d'audio. Ouverture par la "
            f"moustache du chat sous la table, pas la ferme ni l'œuf "
            f"(xlsx). Monde du dump marché : chat sous table, caisse de "
            f"fromages, petite balance, panier. ≠ POL.001-07 croissant / "
            f"farine. ≠ POL.001-09 fromagerie / cloche. ≠ POL.001-11 "
            f"poires / sac. Pas éclat de cloche / sac / corbeille / "
            f"croissant / bâche / volet / pavé / zeste / parapluie. "
            f"Indice unique éclat de panier, nommé puis payé pâle. "
            f"Héros Mila. Dump Honoré → INTERDIT. `enfant-f`. « la dame "
            f"» = label narré (essuie, pose le chiffon, lève les yeux), "
            f"pas de leçon récitée. Pas de maîtresse. Papa ajouté. "
            f"Leçon COL.POL.001 vécue : bonjour ouvre le panier, jamais "
            f"« on dit bonjour d'abord ». Question moteur : « Mila "
            f"parle à la dame. Quels mots dit-elle ? » expected "
            f"bonjour. retry Honoré→Mila. Tics encore/déjà/tout doux/"
            f"tout calme absents. Un « en ce moment ». Un merci vécu. "
            f"{nwords} mots. N3 ≤ 16. TTS notes+ssml+xai+piper par "
            f"chunk."
        ),
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
