#!/usr/bin/env python3
"""ATOM-AUT.AFF.002-07 — Le cacao et le pain de Mila (F-NAR-019, N2, AUT.AFF.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.002-07"
TITLE = "Le cacao et le pain de Mila"
N2 = LIMITS["N2"]
CHARS = "Mila, papa"
SETTING = "cuisine, entrée, boulangerie"
FIL = (
    "La vapeur du cacao dessine un nuage sur la vitre. Sur le bord, un "
    "éclat de tasse brille, comme une lune. Mila veut le pain de la rue, "
    "maintenant. Elle pousse les deux bras d'un coup : la manche avale la "
    "moufle. Elle refuse de forcer, pose, enfile le manteau. Merci vécu. "
    "Devant la boulangerie, une flaque barre le pas. Elle refuse de foncer. "
    "Dans l'eau, l'éclat blanc pointe le pain rond. Ils rentrent. L'éclat "
    "de tasse et la lune de farine se regardent."
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
    "grain de toile",
    "grain de pépin",
    "grain de pepin",
    "grain de pomme",
    "grain de carotte",
    "grain de pin",
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
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de liste",
    "éclat de caillou",
    "trait de vitre",
    "trait de craie",
    "pain doré de sarah",
    "sac à pain",
    "sac a pain",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de tasse",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_pain_maintenant; "
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
            "intensite=1; destinataire=enfant; sous_texte=elle_prend_le_manteau; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="manteau",
        note=(
            "arc=confirmation; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=une_manche_puis_l_autre; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de tasse",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; sous_texte=elle_refuse_de_foncer_dans_la_flaque; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de tasse",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_de_la_tasse_est_sur_le_pain; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "manteau",
    "accepted_examples": "manteau | le manteau | son manteau | elle prend le manteau",
    "retry_prompt": "Elle prend le manteau. Que prend Mila ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "tasses,vapeur",
        [
            "narrateur|La vapeur du cacao dessine un nuage, sur la vitre.",
            "narrateur|Deux tasses restent tièdes, sur la table.",
            "narrateur|La table sent le lait, et le chocolat.",
            "narrateur|Un cercle brun sèche près de la nappe.",
            "narrateur|La veste de papa pèse sur le dossier.",
            "narrateur|Le radiateur cliquette près du crochet.",
            "enfant-f|Papa, mon cacao est fini.",
            "papa|Il était bon, le chaud ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Il reste un peu au fond.",
            "narrateur|Mila pose sa tasse près du cercle brun.",
            "narrateur|Elle lève le bord vers la lumière.",
            "narrateur|Sur le bord, un éclat de tasse brille.",
            "narrateur|C'est un petit éclat blanc, comme une lune.",
            "enfant-f|Il brille, papa.",
            "papa|C'est un éclat de tasse, Mila.",
            "narrateur|Dehors, l'air sent le pain, par la fente.",
            "narrateur|La fente de la porte laisse passer le chaud.",
            "enfant-f|Je veux le pain, maintenant !",
            "papa|Le four de la rue va le sortir.",
            "enfant-f|On y va ?",
            "papa|On prend le manteau, d'abord.",
            "narrateur|En ce moment, Mila court vers le crochet.",
            "narrateur|Son manteau vert attend, un peu lourd.",
            "narrateur|Elle saisit le manteau vert.",
            "narrateur|Le tissu sent le chaud du radiateur.",
            "enfant-f|Je le mets d'un coup !",
            "narrateur|Elle pousse les deux bras, trop vite.",
            "narrateur|La manche avale la moufle sèche.",
            "narrateur|Le tissu se bloque, contre le pouce.",
            "enfant-f|Ça reste coincé !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Tu regardes la manche ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Mila tient le manteau.",
            "narrateur|Avant de sortir, que prend Mila ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "tissu,radiateur",
        [
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Mila refuse de tirer plus fort.",
            "enfant-f|Je sors la moufle.",
            "narrateur|Elle tire le tissu coincé, sans forcer.",
            "narrateur|La moufle glisse, un peu froide.",
            "enfant-f|Elle était dans la manche.",
            "papa|Tu la poses où ?",
            "enfant-f|Près du radiateur.",
            "narrateur|Mila pose la moufle sèche.",
            "narrateur|Le radiateur cliquette sous la laine.",
            "papa|Et le manteau ?",
            "enfant-f|Je le mets.",
            "narrateur|Elle passe une manche, puis l'autre.",
            "narrateur|Le tissu vert gratte un peu, aux poignets.",
            "enfant-f|J'ai les bras dedans.",
            "papa|Tu as fini tes manches ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila boutonne le bas, un par un.",
            "enfant-f|C'est fermé.",
            "papa|Merci, Mila.",
            "narrateur|Papa ouvre la porte de l'entrée.",
            "narrateur|L'air frais pique les joues.",
            "enfant-f|On va au pain ?",
            "papa|Oui, à la boulangerie.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "dalles,cloche",
        [
            "narrateur|Ils marchent sur les dalles froides.",
            "narrateur|Le manteau tape contre les genoux de Mila.",
            "narrateur|Une odeur de four glisse dans la rue.",
            "papa|Tu tiens ma main ?",
            "enfant-f|Oui, papa.",
            "enfant-f|J'ai chaud dans le manteau.",
            "papa|Oui, le vent est froid.",
            "enfant-f|Je le vois !",
            "narrateur|Derrière la vitre, un pain rond attend.",
            "enfant-f|Je cours le prendre !",
            "narrateur|Mila veut foncer vers la porte.",
            "narrateur|Une flaque barre le pas, devant le seuil.",
            "narrateur|Le sourire de Mila se serre.",
            "narrateur|Ça serre, dans son ventre.",
            "enfant-f|Je n'aime pas ça.",
            "narrateur|Mila refuse de foncer.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Mila observe le pain, écoute la rue.",
            "narrateur|Dans la flaque, un éclat blanc tremble.",
            "enfant-f|Comme l'éclat de tasse, papa !",
            "papa|Tu le vois, celui-là ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Il pointe le pain rond.",
            "narrateur|Elle contourne la flaque, lentement.",
            "narrateur|La cloche de la porte tinte.",
            "narrateur|Ça sent le chaud, et la farine.",
            "papa|Tu tiens le sac ?",
            "enfant-f|Oui, il est un peu chaud.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "pain,tasse",
        [
            "narrateur|Ils rentrent dans la cuisine tiède.",
            "narrateur|Mila raccroche le manteau vert, au crochet.",
            "narrateur|Le crochet est bas, sous la veste de papa.",
            "narrateur|Papa ferme la porte de l'entrée.",
            "enfant-f|Le pain est là.",
            "papa|Oui, près des tasses.",
            "narrateur|Mila pose le sac chaud sur la table.",
            "narrateur|Le cercle brun touche le papier.",
            "enfant-f|Mon éclat de tasse, papa.",
            "narrateur|Sur le bord, l'éclat de tasse brille.",
            "narrateur|Sur la croûte, la lune de farine brille aussi.",
            "enfant-f|Ils se regardent.",
            "papa|Tu les sens, le cacao et le pain ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Le pain sent le chaud.",
            "narrateur|L'éclat de tasse reste sur le bord.",
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
        extra_kw: dict = {}
        if cid == "CHK_T0000_P0000_Q0001":
            extra_kw["pause_before_ms"] = 200
            extra_kw["fields"] = Q_FIELDS
        elif cid != "CHK_T0000_P0000":
            extra_kw["pause_before_ms"] = 200
        by[cid] = voice(c, lines, profile, sons, extra_kw)
    merged = dict(src)
    merged["fil_rouge"] = FIL
    merged["title"] = TITLE
    merged["characters"] = CHARS
    merged["setting"] = SETTING
    merged["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    nwords = sum(words(c["text"]) for c in merged["chunks"])
    blob = "\n".join(c["script"] for c in merged["chunks"]).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    opening = by["CHK_T0000_P0000"]["text"].lower()
    ending = by["CHK_T0000_P0000_END_F0001"]["text"].lower()
    if "éclat de tasse" not in opening:
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de tasse" not in ending:
        raise SystemExit(f"{SID}: indice non payé à la fin")
    if "manteau" not in opening:
        raise SystemExit(f"{SID}: manteau absent à l'ouverture")
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
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "## Promesse narrative\n\n"
        "La vapeur du cacao dessine un nuage sur la vitre. Deux tasses "
        "tièdes, un cercle brun, le radiateur. Sur le bord, un **éclat de "
        "tasse** brille, comme une lune. Mila veut le pain de la rue, "
        "**maintenant**. Elle pousse les deux bras d'un coup : la manche "
        "avale la moufle. Première idée ratée. Papa s'accroupit. Elle "
        "refuse de forcer, pose la moufle, enfile une manche puis l'autre, "
        "boutonne. Merci vécu. Dans la rue, elle a chaud dans le manteau. "
        "Elle veut courir vers le pain : une flaque barre le pas. Elle "
        "refuse de foncer. Dans l'eau, un éclat blanc tremble, comme sur "
        "la tasse, et pointe le pain rond. Ils rentrent. L'éclat de tasse "
        "et la lune de farine se regardent.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine (cacao, tasses, cercle brun), entrée (crochet, "
        "radiateur, moufle), boulangerie (vitre, flaque, cloche).\n"
        "- Désir : porter le pain chaud, maintenant, avant qu'il refroidisse.\n"
        "- Objet : manteau vert, moufle, tasse, pain rond, sac chaud.\n"
        "- Indice unique : éclat de tasse, vu dès l'ouverture, payé dans "
        "la flaque puis sur la croûte.\n"
        "- Urgence douce : l'odeur du four passe par la fente de la porte.\n"
        "- Imprévu 1 : tout d'un coup, manche qui avale la moufle, pouce coincé.\n"
        "- Cue : papa à la même hauteur, une manche puis l'autre. "
        "Un merci vécu, après le manteau fermé.\n"
        "- Imprévu 2 (plus rusé) : elle veut courir ; une flaque barre le "
        "seuil ; l'éclat dans l'eau désigne le pain.\n"
        "- Résolution : elle refuse de foncer, contourne, tient le sac.\n"
        "- Retour : cuisine, manteau au crochet, éclat de tasse face à la "
        "lune de farine.\n\n"
        "## Vécu\n\n"
        "Leçon AUT.AFF.002 (prendre le manteau) greffée, jamais dite. La "
        "première idée (tout d'un coup) échoue. Le choix de Mila change "
        "l'action. Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Troupe D16 : Mila, papa.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : cuisine, entrée, "
        "boulangerie. ≠ 002-01 jardin/feuille, ≠ 002-02 marché/pommes, "
        "≠ 002-03 hall/clés/pigeon/manteau jaune, ≠ 002-04 carottes, "
        "≠ 002-05 square/sonnette, ≠ 002-06 jardin/sac vide/manteau gris.\n"
        "- Ouverture inventée (vapeur du cacao sur la vitre), pas un "
        "gabarit v2.\n"
        "- Indice unique : éclat de tasse. Pas grain de miette/foin/"
        "feuille/paille/toile/pépin/pomme/carotte/pin, pas éclat de pince/"
        "thermos/coquille/bouton/ticket/goutte/boucle/corde/caisse/marche/"
        "clé/cuillère/sonnette/horloge/liste/caillou, pas trait de vitre/"
        "craie, merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Question moteur inchangée (manteau). 5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N2 ≤ 15. TTS : notes, ssml, xai, piper par chunk.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
