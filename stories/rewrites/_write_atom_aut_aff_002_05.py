#!/usr/bin/env python3
"""ATOM-AUT.AFF.002-05 — La sonnette argentée de Nina (F-NAR-019, N2, AUT.AFF.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.002-05"
TITLE = "La sonnette argentée de Nina"
N2 = LIMITS["N2"]
CHARS = "Nina, papa"
SETTING = "entrée puis square"
FIL = (
    "Nina connaît l'entrée. Un éclat de sonnette cligne sur le métal froid. "
    "Elle veut ding au square du banc vide, maintenant. Elle roule sans le "
    "manteau : le guidon heurte le crochet, la manche cache l'éclat. Elle "
    "refuse de tirer les deux à la fois, pose la trottinette, prend le "
    "manteau. Au square, la sonnette reste muette. Elle refuse de foncer, "
    "retrouve l'éclat, fait ding. Le manteau rentre au crochet."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "merle",
    "miel",
    "grand-père",
    "grand-pere",
    "maîtresse",
    "maitresse",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de marche",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cuillère",
    "trait de craie",
    "trait de vitre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de sonnette",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_ding_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="manteau",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; sous_texte=avant_de_sortir_le_manteau; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="manteau",
        note=(
            "arc=confirmation; intention=relancer; emotion=fierté_calme; "
            "intensite=1; destinataire=enfant; sous_texte=elle_prend_le_manteau_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de sonnette",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis prudence; intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de sonnette",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_reste_sur_le_metal_le_manteau_au_crochet; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "manteau",
    "accepted_examples": "manteau | son manteau | le manteau",
    "retry_prompt": "Avant de sortir, on prend le manteau. Que prend Nina ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "sonnette,porte",
        [
            "narrateur|Une bande de soleil coupe les carreaux de l'entrée.",
            "narrateur|Nina connaît cette entrée, le crochet, les bruits du carreau.",
            "narrateur|Les chaussures de papa font une paire, près de la porte.",
            "narrateur|La trottinette s'appuie au mur, un peu penchée.",
            "narrateur|Un détail paraît nouveau, sur le métal.",
            "narrateur|Sur la sonnette argentée, un éclat de sonnette cligne.",
            "narrateur|Le métal est froid, presque blanc.",
            "papa|Nina, tu vois l'éclat ?",
            "enfant-f|Il brille, papa.",
            "enfant-f|Je veux ding au square, maintenant !",
            "narrateur|Le square du banc vide est juste en bas de la rue.",
            "papa|On y va, avec la trottinette.",
            "narrateur|En ce moment, Nina saisit le guidon froid.",
            "narrateur|Son manteau bleu attend au crochet, trop loin.",
            "enfant-f|Vite, le banc est vide !",
            "narrateur|Elle pousse la trottinette vers la porte.",
            "narrateur|Les roues font un bruit léger, sur les carreaux.",
            "narrateur|Le guidon heurte le crochet, dur.",
            "narrateur|Le manteau bleu se balance, puis retombe.",
            "narrateur|Une manche glisse sur la sonnette.",
            "narrateur|L'éclat de sonnette disparaît sous le tissu.",
            "enfant-f|Oh.",
            "enfant-f|Il est parti !",
            "papa|Pose la trottinette un moment.",
            "narrateur|Nina veut les deux, d'un coup.",
            "narrateur|Elle tire le manteau, le guidon sous l'autre bras.",
            "narrateur|La manche se tord, serrée.",
            "narrateur|Le tissu refuse de venir.",
            "enfant-f|Ça reste coincé !",
            "narrateur|Elle tire plus fort.",
            "narrateur|Le crochet penche, un peu.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Papa s'accroupit à sa hauteur.",
            "papa|Tu regardes le manteau ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nina prépare la sortie.",
            "narrateur|Le manteau bleu attend au crochet.",
            "narrateur|Avant de sortir, que prend Nina ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "manteau,porte",
        [
            "narrateur|Nina refuse de tirer plus fort.",
            "narrateur|Elle pose la trottinette contre le mur.",
            "narrateur|Les roues s'arrêtent, nettes.",
            "enfant-f|Je pose le guidon.",
            "narrateur|Elle soulève la manche, lente.",
            "narrateur|Sous le tissu, l'éclat de sonnette cligne.",
            "enfant-f|Il est là, papa.",
            "papa|Tu le vois, toi ?",
            "enfant-f|Oui, sur la sonnette.",
            "narrateur|Nina prend son manteau bleu.",
            "narrateur|Elle passe une manche, puis l'autre.",
            "narrateur|Le tissu est doux, un peu frais.",
            "papa|Tu as le manteau ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le crochet reste vide, bas.",
            "narrateur|La sonnette est libre, froide.",
            "papa|Merci, Nina.",
            "papa|On ouvre la porte ?",
            "enfant-f|Oui.",
            "narrateur|Papa ouvre la porte.",
            "narrateur|L'air est frais, un peu vif.",
            "narrateur|Ils sortent vers le square du banc vide.",
            "narrateur|Nina pose la main sur le guidon.",
            "narrateur|Le métal reste froid sous le doigt.",
            "enfant-f|On y va.",
            "papa|Oui, l'air est frais.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "sonnette,feuilles",
        [
            "narrateur|Au square, Nina pousse la trottinette.",
            "narrateur|Les roues chantent un peu, sur le gravier.",
            "narrateur|Un banc est vide, au soleil.",
            "enfant-f|Ding, maintenant !",
            "narrateur|Elle appuie trop fort, d'un coup.",
            "narrateur|La sonnette reste muette.",
            "enfant-f|Elle ne veut pas.",
            "narrateur|Les feuilles du square sont sèches.",
            "narrateur|Elles font chh, sous la roue.",
            "narrateur|Nina veut appuyer plus fort.",
            "narrateur|Elle refuse de foncer.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Papa attend, sans parler.",
            "narrateur|Elle observe la sonnette, puis le square.",
            "narrateur|Le métal est tourné, de travers.",
            "narrateur|Sur l'autre face, un éclat de sonnette cligne.",
            "enfant-f|C'est celui de l'entrée.",
            "papa|Tu le vois, au square ?",
            "enfant-f|Oui, il s'était caché.",
            "narrateur|Nina tourne le métal, sans brusquer.",
            "narrateur|L'éclat de sonnette revient face au soleil.",
            "narrateur|Elle appuie, légère.",
            "narrateur|Ça fait ding, une fois.",
            "enfant-f|Ding !",
            "papa|Tu l'as fait sonner ?",
            "enfant-f|Oui, elle était tournée.",
            "narrateur|Le banc vide reste au soleil.",
            "narrateur|Nina pose un pied par terre.",
            "papa|On rentre, Nina ?",
            "enfant-f|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "porte",
        [
            "narrateur|Ils rentrent dans l'entrée.",
            "narrateur|Papa ferme la porte.",
            "narrateur|Nina raccroche le manteau au crochet.",
            "enfant-f|Il est à sa place.",
            "narrateur|Le crochet est bas, à sa hauteur.",
            "narrateur|Elle pose la trottinette contre le mur.",
            "papa|Tu as fini de poser tes chaussures ?",
            "enfant-f|Oui, papa.",
            "narrateur|La bande de soleil a bougé, sur les carreaux.",
            "enfant-f|J'ai fait ding au banc.",
            "papa|Oui, tu l'as fait.",
            "narrateur|La sonnette argentée attend contre le mur.",
            "narrateur|L'éclat de sonnette reste, pâle, sur le métal.",
        ],
    ),
}


def vet(lines: list[str]) -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    for raw in lines:
        if "|" not in raw:
            raise SystemExit(f"sans | : {raw}")
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"fin: {ph}")
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"extra {bad}: {ph}")
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


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in SCRIPTS]
    extra = set(SCRIPTS) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{SID} chunks missing={missing} extra={extra}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        profile, sons, lines = SCRIPTS[cid]
        extra: dict = {}
        if cid == "CHK_T0000_P0000_Q0001":
            extra["pause_before_ms"] = 200
            extra["fields"] = Q_FIELDS
        elif cid != "CHK_T0000_P0000":
            extra["pause_before_ms"] = 200
        by[cid] = voice(c, lines, profile, sons, extra)
    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if blob.count("merci") != 1:
        raise SystemExit(f"{SID}: merci ×{blob.count('merci')}")
    if "éclat de sonnette" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de sonnette" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé au climax")
    if "éclat de sonnette" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "manteau" not in by["CHK_T0000_P0000_C0001"]["text"].lower():
        raise SystemExit(f"{SID}: leçon manteau absente de C0001")
    tts_ok = all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_xai_tags"] != c["text"]
        and c["text_ssml"].startswith("<speak>")
        for c in chunks
    )
    if not tts_ok:
        raise SystemExit(f"{SID}: TTS incomplet")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nwords = sum(words(c["text"]) for c in chunks)

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** AUT.AFF.002 — prendre le manteau (vécue, jamais dite)\n"
        "- **Personnages :** Nina, papa. Troupe D16.\n"
        "- **Lieu :** entrée puis square (square du banc vide, coin du crochet)\n"
        "- **Indice unique :** éclat de sonnette (métal de l'entrée → manche "
        "→ face tournée au square → pâle au retour)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Nina connaît l'entrée. Une bande de soleil coupe les carreaux. Un "
        "éclat de sonnette cligne sur le métal froid. Elle veut **ding "
        "maintenant** au square du banc vide. Première idée : rouler sans le "
        "manteau. Le guidon heurte le crochet, la manche cache l'éclat. Elle "
        "tire les deux à la fois : coincé. Elle refuse, pose la trottinette, "
        "prend le manteau. Merci vécu. Au square, elle appuie trop fort : "
        "muet. Elle refuse de foncer, retrouve l'éclat sur l'autre face, "
        "fait ding. Retour : manteau au crochet, éclat pâle sur le métal.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : entrée, bande de soleil, paire de chaussures, crochet, "
        "square en bas de la rue.\n"
        "- Désir : ding au square du banc vide, maintenant.\n"
        "- Objet : sonnette argentée (froid, cligne, mission : ding au banc).\n"
        "- Indice unique : éclat de sonnette, vu dès l'ouverture, payé au "
        "climax et à la fin.\n"
        "- Urgence douce : le banc vide, tout de suite.\n"
        "- Imprévu 1 : guidon contre le crochet, manche sur l'éclat, tissu "
        "coincé.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, après "
        "le manteau.\n"
        "- Imprévu 2 (plus rusé) : sonnette muette, tournée ; Nina veut "
        "appuyer plus fort.\n"
        "- Résolution : elle refuse de foncer, lit l'éclat, tourne le métal, "
        "ding.\n"
        "- Retour : manteau au crochet, trottinette au mur, éclat pâle.\n\n"
        "## Vécu\n\n"
        "Nina veut ding **maintenant**. Impatience, puis sourire qui "
        "disparaît quand le manteau résiste. Papa se baisse, pose une "
        "question, ne récite pas la règle. Nina agit : trottinette au mur, "
        "manche levée, manteau. Merci vécu après les manches. Au square, "
        "elle refuse de foncer. Fin : l'éclat du début est pâle sur le "
        "métal. Le manteau est au crochet.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : entrée puis square. "
        "≠ 002-01 (jardin, feuille rouge). ≠ 002-02 (marché, pommes). "
        "≠ 002-03 (boulangerie, pain). ≠ 002-04 (carottes, marché).\n"
        "- Ouverture inventée (bande de soleil, détail nouveau sur le métal), "
        "pas un gabarit v2, pas « Nina est dans l'entrée ».\n"
        "- Indice unique : éclat de sonnette. Pas grain de miette/foin/"
        "feuille/paille/pin/pépin, pas éclat de pince/thermos/coquille/"
        "bouton/ticket/goutte/boucle/corde/caisse/marche/caillou/liste/clé/"
        "cuillère, pas trait de craie/vitre, merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : elle prend le manteau pour sortir, le raccroche. "
        "Pas de morale.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée (manteau). 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle plus tendu. Action plus vive à l'ouverture.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")


if __name__ == "__main__":
    main()
