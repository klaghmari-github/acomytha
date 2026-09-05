#!/usr/bin/env python3
"""ATOM-COL.POL.001-07 — Le croissant de Mila (F-NAR-019, N1, linéaire)."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "ATOM-COL.POL.001-07"
LIM = 10
TITLE = "Le croissant de Mila"
CHARS = "Mila, papa, maman"
SETTING = (
    "rue tiède, farine sur la vitre, rayon blanc, "
    "boulangerie, comptoir de marbre, croissant"
)
INDICE = "éclat de croissant"
FIL = (
    "Un rayon blanc tient sur la vitre. La farine y reste. "
    "Sur la pointe, un éclat de croissant brille. Mila veut "
    "le croissant maintenant. Elle parle trop vite, sans le mot : "
    "la dame n'a pas levé les yeux. Elle refuse de foncer, dit "
    "bonjour. Merci vécu. Le sac glisse. Un éclat de croissant "
    "reste pâle."
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
    "fanny",
    "gaufre",
    "pavé",
    "pave",
    "petit pain",
    "éclat de farine",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de poisson",
    "éclat de parapluie",
    "éclat de citron",
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
            "destinataire=enfant; sous_texte=elle_veut_le_croissant_maintenant; "
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
            "destinataire=enfant; sous_texte=bonjour_ouvre_le_sac; "
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
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat_de_croissant; "
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
            "sous_texte=l_eclat_de_croissant_reste_pale; "
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
    ("narrateur", "Un rayon blanc tient sur la vitre."),
    ("narrateur", "La farine y reste, sans tomber."),
    ("narrateur", "Sous les chaussures, la rue est tiède."),
    ("enfant-f", "Ça sent le beurre, papa."),
    ("papa", "Tu le sens, toi ?"),
    ("enfant-f", "Oui, chaud."),
    ("maman", "Le soleil touche tes joues."),
    ("enfant-f", "Elles sont tièdes, maman."),
    ("narrateur", "Papa tient la main de Mila."),
    ("narrateur", "Sa paume a un peu de farine."),
    ("papa", "Tu as vu la farine, Mila ?"),
    ("enfant-f", "Elle ne tombe pas, papa."),
    ("papa", "Non."),
    ("papa", "Elle reste sur la vitre."),
    ("narrateur", "Derrière le verre, les croissants dorés attendent."),
    ("narrateur", "Un croissant a une pointe plus brune."),
    ("enfant-f", "Celui-là, papa."),
    ("narrateur", "Sur la pointe, un éclat de croissant brille."),
    ("enfant-f", "Il brille, maman !"),
    ("maman", "Tu le vois, sur le croissant ?"),
    ("enfant-f", "Oui, près de la pointe."),
    ("enfant-f", "Je le veux, maintenant."),
    ("narrateur", "En ce moment, Mila pousse la porte."),
    ("narrateur", "Une cloche fait ding."),
    ("narrateur", "La chaleur entre dans les manches."),
    ("enfant-f", "Il est chaud ici."),
    ("papa", "On reste près du marbre ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "La dame essuie le comptoir de marbre."),
    ("narrateur", "Le marbre est froid, malgré le four."),
    ("narrateur", "Elle a un torchon gris à la main."),
    ("enfant-f", "Celui-là !"),
    ("narrateur", "Mila parle trop vite vers le marbre."),
    ("narrateur", "Sa voix se mélange au torchon."),
    ("narrateur", "La dame n'a pas levé les yeux."),
    ("enfant-f", "Oh."),
    ("narrateur", "Le croissant reste derrière le verre."),
    ("narrateur", "Le sourire de Mila disparaît."),
    ("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
    ("enfant-f", "Je le prends !"),
    ("maman", "Le croissant est derrière le verre."),
    ("papa", "Tu le vois, Mila ?"),
    ("narrateur", "Les épaules de Mila tombent un peu."),
    ("narrateur", "Ça serre, dans son ventre."),
    ("narrateur", "Papa se baisse à sa hauteur."),
)

QUESTION = L(
    ("narrateur", "Mila parle à la dame."),
    ("narrateur", "Que dit-elle ?"),
)

CONFIRM = L(
    ("narrateur", "Mila avance trop vite vers le marbre."),
    ("enfant-f", "Celui-là, maintenant !"),
    ("narrateur", "Sa voix se mélange au torchon."),
    ("enfant-f", "Oh."),
    ("narrateur", "Le croissant reste derrière le verre."),
    ("narrateur", "La dame essuie, sans lever les yeux."),
    ("narrateur", "Mila refuse de foncer."),
    ("narrateur", "Elle referme la main."),
    ("narrateur", "Elle écoute la cloche, un instant."),
    ("papa", "Tu veux venir près du marbre ?"),
    ("narrateur", "Papa s'accroupit à la même hauteur."),
    ("narrateur", "Mila pose un pied sur le pas."),
    ("narrateur", "Le marbre est froid sous l'air chaud."),
    ("enfant-f", "Bonjour."),
    ("enfant-f", "Celui-là."),
    ("enfant-f", "S'il te plaît."),
    ("narrateur", "La dame pose le torchon."),
    ("narrateur", "Elle lève les yeux."),
    ("narrateur", "Une main glisse le croissant dans un sac."),
    ("narrateur", "Le sac est chaud, un peu gras."),
    ("papa", "Merci, Mila."),
    ("narrateur", "Papa a entendu toute la phrase."),
    ("narrateur", "Le ventre de Mila se desserre."),
    ("narrateur", "Les épaules se relèvent un peu."),
    ("maman", "Tu as les mains au chaud ?"),
    ("enfant-f", "Un peu, maman."),
    ("narrateur", "Ça sent le beurre et le four."),
    ("enfant-f", "Le croissant est à moi."),
    ("maman", "Il est dans tes mains."),
    ("narrateur", "Mila pose une main sur le sac."),
    ("narrateur", "Le papier est un peu rêche."),
    ("narrateur", "Sur le sac, un éclat de croissant tient."),
    ("narrateur", "La cloche se tait."),
)

GARDEN = L(
    ("narrateur", "Mila tire le sac trop vite."),
    ("enfant-f", "Je le montre, d'un coup !"),
    ("narrateur", "Le papier glisse entre les doigts."),
    ("narrateur", "Le croissant penche vers le sol."),
    ("enfant-f", "Oh."),
    ("narrateur", "Mila avance les mains."),
    ("narrateur", "Puis elle s'arrête net."),
    ("enfant-f", "Attends, je regarde."),
    ("narrateur", "Papa attend, sans parler."),
    ("narrateur", "Mila observe le pas, écoute la rue."),
    ("narrateur", "Sur la pointe, un éclat de croissant luit."),
    ("enfant-f", "Là, près de la pointe."),
    ("narrateur", "Mila tient le sac des deux mains."),
    ("narrateur", "Le papier est rêche, un peu chaud."),
    ("enfant-f", "Il est chaud, papa."),
    ("papa", "Tu le portes jusqu'à la rue ?"),
    ("enfant-f", "Oui, papa."),
    ("maman", "On sort ?"),
    ("enfant-f", "Oui, maman."),
    ("narrateur", "La porte s'ouvre."),
    ("narrateur", "La cloche fait ding."),
    ("narrateur", "L'air tiède revient sur les joues."),
    ("narrateur", "Mila serre le sac contre elle."),
    ("enfant-f", "Il reste chaud."),
    ("papa", "On marche."),
    ("narrateur", "Le sac penche, puis se cale."),
    ("enfant-f", "Je le tiens."),
    ("maman", "On avance."),
    ("narrateur", "Mila passe le pas."),
    ("narrateur", "Le marbre reste derrière."),
)

ENDING = L(
    ("enfant-f", "Le croissant brillait, papa."),
    ("papa", "Tu le vois, comme dans la boutique ?"),
    ("enfant-f", "Oui, sur la pointe."),
    ("narrateur", "Mila pose le sac contre le manteau."),
    ("maman", "On le garde au chaud ?"),
    ("enfant-f", "Oui, maman."),
    ("enfant-f", "Le four sentait bon."),
    ("maman", "Il est contre toi."),
    ("narrateur", "Une vapeur monte du papier."),
    ("narrateur", "Mila respire, plus large."),
    ("papa", "On rentre ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "Les joues de Mila se réchauffent."),
    ("narrateur", "Le sac reste tiède sous la main."),
    ("narrateur", "La farine tient sur la vitre."),
    ("enfant-f", "Elle ne tombe pas."),
    ("maman", "Comme tout à l'heure ?"),
    ("enfant-f", "Oui, maman."),
    ("papa", "Le rayon est blanc, toi ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "Un éclat de croissant reste pâle."),
)


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: c for c in src["chunks"]}
    scripts = {
        "CHK_T0000_P0000": (
            "opening",
            OPENING,
            "cloche,pas",
            {"emphasis": "éclat de croissant"},
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
                        "Bonjour, s'il te plaît, merci. Que dit Mila ?"
                    ),
                    "engine_ok_text": "Oui, bonjour.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": (
            "resolution",
            CONFIRM,
            "papier,cloche",
            {"emphasis": "Bonjour"},
        ),
        "CHK_T0000_P0000_END": (
            "obstacle",
            GARDEN,
            "pas,papier",
            {"emphasis": "éclat de croissant"},
        ),
        "CHK_T0000_P0000_END_F0001": (
            "ending",
            ENDING,
            "pas",
            {"emphasis": "éclat de croissant", "pause_before": 200},
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
    if "éclat de farine" in joined:
        raise SystemExit("BAN RAN.001-03 : éclat de farine")
    if "pavé" in joined or "pave" in joined:
        raise SystemExit("BAN POL.001-01 : pavé")
    if "petit pain" in joined:
        raise SystemExit("BAN POL.001-01 : petit pain")
    if "gaufre" in joined:
        raise SystemExit("BAN xlsx gaufre")
    if joined.count("en ce moment") != 1:
        raise SystemExit("en ce moment doit apparaître une fois")
    if "fanny" in joined:
        raise SystemExit("prénom interdit Fanny")
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
    if qtext != "Mila parle à la dame. Que dit-elle ?":
        raise SystemExit(f"question moteur altérée: {qtext}")
    if chunks[1].get("expected_answer") != "bonjour":
        raise SystemExit("expected_answer altéré")
    retry = str(chunks[1].get("retry_prompt") or "")
    if "fanny" in retry.lower():
        raise SystemExit("retry Fanny restée")
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
            "Mila veut le croissant à la pointe brune. Éclat de croissant "
            "sur la pointe. Rue tiède, farine sur la vitre, rayon blanc. "
            "Elle parle trop vite, sans bonjour : la dame n'a pas levé les "
            "yeux. Sourire parti. Elle refuse de foncer, dit bonjour, puis "
            "s'il te plaît. Le sac arrive. Merci vécu. Elle veut montrer "
            "d'un coup : le papier glisse. Elle s'arrête, lit l'éclat. "
            "Un éclat de croissant reste pâle."
        ),
        (
            f"Ouverture par le rayon blanc sur la farine, pas la place ni "
            f"le fer à gaufres (xlsx). Monde du dump croissant : "
            f"boulangerie, farine sur vitre, rayon blanc, rue tiède, "
            f"marbre, cloche. ≠ POL.001-01 Nino pavé / petit pain. "
            f"Pas éclat de farine (BAN RAN.001-03). Pas pavé. Indice "
            f"unique éclat de croissant, nommé puis payé pâle. "
            f"Héros Mila. Dump Fanny → INTERDIT. `enfant-f`. "
            f"« la dame » = label narré (essuie, pose le torchon, lève "
            f"les yeux), pas de leçon récitée. Pas de maîtresse. "
            f"Leçon COL.POL.001 vécue : bonjour ouvre le sac, jamais "
            f"« on dit bonjour d'abord ». Question moteur : « Mila parle "
            f"à la dame. Que dit-elle ? » expected bonjour. retry "
            f"Fanny→Mila. Tics encore/déjà/tout doux/tout calme absents. "
            f"Un « en ce moment ». Un merci vécu. {nwords} mots. N1 ≤ 10. "
            f"TTS notes+ssml+xai+piper par chunk. Pas apply, pas git, "
            f"pas audio."
        ),
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
