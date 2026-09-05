#!/usr/bin/env python3
"""ATOM-AUT.AFF.002-04 — Les carottes d'Amir (F-NAR-019, N3, AUT.AFF.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.002-04"
TITLE = "Les carottes d'Amir"
N3 = LIMITS["N3"]
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
    "grain de miette",
    "grain de foin",
    "grain de paille",
    "grain de toile",
    "grain de pépin",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "éclat de corde",
    "éclat de clé",
    "éclat de liste",
    "éclat de caisse",
    "éclat de caillou",
    "éclat de sonnette",
    "trait de craie",
    "trait de vitre",
    "grain de pin",
    "grain de feuille",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de cuillère",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_les_carottes_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="sortir",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=avant_de_sortir_il_prend_le_manteau; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="manteau",
        note=(
            "arc=confirmation; intention=relancer; emotion=élan_impatient; intensite=1; "
            "destinataire=enfant; sous_texte=le_sac_cache_le_manteau; "
            "tempo=naturel; sourire=léger puis tendu; respiration=fluide"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de cuillère",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_l_éclat_montre_le_crochet; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de cuillère",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_éclat_porte_une_trace_orange; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "manteau",
    "accepted_examples": "manteau | le manteau | son manteau",
    "retry_prompt": "Il prend le manteau. Que prend Amir ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "evier,casserole,porte",
        [
            "narrateur|La cuillère en bois tient dans un verre.",
            "narrateur|Elle sèche, un peu penchée, près de l'évier.",
            "narrateur|Un éclat de cuillère brille sur le bois.",
            "narrateur|Il est pâle, lisse, et il sent la soupe.",
            "narrateur|La casserole fume, trop claire.",
            "enfant-m|Il manque l'orange, papa.",
            "papa|Les carottes, Amir ?",
            "enfant-m|Oui, maintenant !",
            "narrateur|La buée dessine un trait tordu sur la vitre.",
            "narrateur|Dehors, le tuyau d'arrosage dort enroulé.",
            "narrateur|Papa plie le sac de toile, près du crochet.",
            "papa|Amir, tu as vu l'éclat ?",
            "enfant-m|Oui, il brille.",
            "narrateur|En ce moment, Amir veut les carottes.",
            "enfant-m|On y va, tout de suite !",
            "papa|D'abord le jardin.",
            "papa|Une carotte est peut-être prête.",
            "narrateur|Amir saisit le sac de toile.",
            "narrateur|Il court vers la porte, sans le manteau.",
            "enfant-m|Je sors, papa !",
            "narrateur|La porte s'ouvre.",
            "narrateur|L'air froid pique les poignets.",
            "narrateur|La sangle glisse, le sac tombe.",
            "enfant-m|Aïe !",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tes poignets sont froids ?",
            "enfant-m|Oui.",
            "enfant-m|Le sac est tombé.",
            "narrateur|Le manteau vert attend au crochet.",
            "narrateur|Ce manteau est un peu épais.",
            "narrateur|Le tissu gratte sous les doigts.",
            "narrateur|Amir glisse un bras, puis l'autre.",
            "papa|Tu es prêt ?",
            "enfant-m|Oui, papa.",
            "narrateur|Ils passent au jardin.",
            "narrateur|Une dalle est froide sous la semelle.",
            "enfant-m|Le sol pique.",
            "narrateur|Le coin du tuyau sent l'eau.",
            "narrateur|L'air sent l'herbe mouillée.",
            "narrateur|Amir touche une feuille lisse.",
            "enfant-m|Elle sent le jardin.",
            "papa|Regarde les fanes.",
            "narrateur|Les fanes sont petites, trop vertes.",
            "enfant-m|Je peux tirer ?",
            "papa|Elles sont trop petites.",
            "narrateur|Amir lâche la fane.",
            "enfant-m|Pas d'orange.",
            "papa|Pas cette fois.",
            "papa|Le marché a des carottes.",
            "narrateur|Le tuyau d'arrosage est froid sous le doigt.",
            "enfant-m|Il est froid !",
            "papa|On rentre.",
            "narrateur|Amir retire le manteau.",
            "narrateur|Il le raccroche au crochet.",
            "narrateur|Le crochet fait un petit tic.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Avant de sortir, que prend Amir ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "sac,crochet",
        [
            "narrateur|Amir a pris le manteau vert.",
            "narrateur|Au jardin, les fanes étaient trop vertes.",
            "narrateur|Le manteau est revenu au crochet.",
            "papa|Le marché, maintenant.",
            "papa|Pour les carottes de la soupe.",
            "narrateur|Papa prend le sac de toile.",
            "narrateur|Il le pose devant le crochet.",
            "narrateur|Le sac cache le manteau vert.",
            "enfant-m|Je ne vois plus le manteau.",
            "enfant-m|On y va avec le sac !",
            "narrateur|Amir tire le sac, d'un coup.",
            "narrateur|Le sac reste coincé contre le crochet.",
            "enfant-m|Ça ne veut pas.",
            "narrateur|Ses épaules tombent.",
            "papa|Tu regardes le crochet ?",
            "narrateur|Amir serre le sac, puis le lâche.",
            "narrateur|La buée revient sur la vitre.",
            "narrateur|Elle cache un peu le crochet.",
            "enfant-m|Je sors avec le sac !",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "resolution",
        "marche,sac,caisse",
        [
            "narrateur|Amir refuse de foncer.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Personne ne dit le chemin.",
            "narrateur|Amir écoute la cuisine.",
            "enfant-m|La casserole chuchote.",
            "narrateur|Sur le verre, l'éclat de cuillère tremble.",
            "narrateur|Il penche vers le crochet.",
            "enfant-m|C'est là !",
            "narrateur|Amir pousse le sac de côté.",
            "narrateur|Le manteau vert réapparaît.",
            "narrateur|Il glisse un bras, puis l'autre.",
            "papa|Merci, Amir.",
            "papa|On ouvre la porte ?",
            "enfant-m|Oui, avec le manteau.",
            "narrateur|Au marché, ça sent le pain.",
            "narrateur|L'étal orange est bas, près des caisses.",
            "narrateur|Une caisse craque sous une botte.",
            "papa|Tu vois les carottes ?",
            "enfant-m|Elles sont orange.",
            "narrateur|Papa achète une botte de carottes.",
            "narrateur|Ils les glissent dans le sac.",
            "narrateur|Le sac de toile sent la terre.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "casserole,evier",
        [
            "narrateur|Amir pose les chaussures près de la porte.",
            "narrateur|Le manteau vert reste au crochet.",
            "narrateur|Papa pose les carottes près de l'évier.",
            "papa|Tu as fini de poser tes chaussures ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa coupe un rond orange.",
            "narrateur|Le rond tombe dans la vapeur.",
            "narrateur|La cuillère reprend sa place dans le verre.",
            "enfant-m|L'éclat a une trace.",
            "papa|La soupe la prend.",
            "narrateur|La buée a quitté la vitre.",
            "narrateur|L'éclat de cuillère porte une trace orange.",
        ],
    ),
}


def vet(lines: list[str]) -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
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
        by[cid] = voice(c, lines, profile, sons, extra)
    merged = dict(src)
    merged["fil_rouge"] = (
        "La cuillère en bois tient dans un verre. Un éclat de cuillère "
        "brille, pâle. La soupe est trop claire. Amir veut des carottes, "
        "maintenant. Il court sans le manteau : l'air pique, le sac tombe. "
        "Papa s'accroupit. Le manteau vert, le jardin, des fanes trop "
        "vertes. Au crochet, le sac cache le manteau. Amir refuse de "
        "foncer. L'éclat penche vers le crochet. Il reprend le manteau. "
        "Au marché, les carottes. Dans le verre, l'éclat porte une trace "
        "orange."
    )
    merged["title"] = TITLE
    merged["characters"] = "Amir, papa"
    merged["setting"] = "cuisine, jardin, marché"
    merged["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    nwords = sum(words(c["text"]) for c in merged["chunks"])
    tts_ok = all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_xai_tags"] != c["text"]
        and c["text_ssml"].startswith("<speak>")
        for c in merged["chunks"]
    )
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    joined = " ".join(c["text"] for c in merged["chunks"])
    if "éclat de cuillère" not in joined:
        raise SystemExit("indice éclat de cuillère absent")
    if joined.lower().count("éclat de cuillère") < 3:
        raise SystemExit("indice trop peu payé")
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "## Promesse narrative\n\n"
        "La cuillère en bois tient dans un verre, près de l'évier. Un éclat "
        "de cuillère pâle brille sur le bois. La casserole fume, trop claire. "
        "Amir veut des carottes orange, maintenant. Il court sans le manteau : "
        "l'air pique, le sac tombe. Papa s'accroupit. Manteau vert, jardin, "
        "fanes trop vertes. Le sac cache le crochet. Amir refuse de foncer. "
        "L'éclat penche vers le crochet. Il reprend le manteau. Au marché, "
        "les carottes. Dans le verre, l'éclat porte une trace orange.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine (verre, évier, buée), coin du tuyau au jardin, "
        "étal orange du marché.\n"
        "- Désir : porter des carottes à la soupe trop claire, maintenant.\n"
        "- Objet : sac de toile, manteau vert, botte de carottes.\n"
        "- Indice unique : éclat de cuillère, vu dès l'ouverture, payé au "
        "climax (il penche vers le crochet) et dans le verre (trace orange).\n"
        "- Urgence douce : la soupe attend l'orange ; le froid à la porte.\n"
        "- Imprévu 1 : courir sans manteau ; sangle, sac à terre, poignets "
        "piqués.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le manteau "
        "repris tout seul.\n"
        "- Imprévu 2 (plus rusé) : le sac cache le manteau, la buée cache le "
        "crochet ; Amir veut tirer et sortir.\n"
        "- Résolution : il refuse de foncer, lit l'éclat, pousse le sac, "
        "enfile le manteau. L'étal orange, les carottes dans le sac.\n"
        "- Retour : chaussures, crochet, rond orange dans la vapeur, l'éclat "
        "porte une trace orange.\n\n"
        "## Vécu\n\n"
        "Leçon AUT.AFF.002 (prendre le manteau) greffée, jamais dite. Deux "
        "sorties, le même manteau vert. La première idée (sans manteau, tout "
        "de suite) échoue. Le choix d'Amir change l'action. Un « en ce "
        "moment ». Un merci vécu. Adulte + question. Troupe D16 : Amir, papa.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : cuisine, jardin, marché. "
        "≠ feuille rouge, ≠ pommes, ≠ pain doré.\n"
        "- Ouverture inventée (la cuillère tient dans un verre), pas un "
        "gabarit v2.\n"
        "- Indice unique : éclat de cuillère. Pas grain de miette/foin/"
        "paille/toile/pépin, pas éclat de pince/thermos/coquille/bouton/"
        "ticket/goutte/boucle/corde/clé/liste, pas trait de craie, merle, "
        "miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Question moteur inchangée (manteau). 5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N3 ≤ 16. TTS : notes, ssml, xai, piper par chunk.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
