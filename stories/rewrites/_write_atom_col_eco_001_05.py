#!/usr/bin/env python3
"""ATOM-COL.ECO.001-05 — La chaussette de Nino (F-NAR-019, N3, COL.ECO.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.001-05"
TITLE = "La chaussette de Nino"
N3 = LIMITS["N3"]
INDICE = "éclat de casier"
CHARS = "Nino, papa, maman"
SETTING = (
    "école puis maison, chaussette bleue sur la première marche, "
    "escalier de bois, lumière de cuisine, cacao"
)
FIL = (
    "Les casiers claquent. Sur la porte, un éclat de casier luit. "
    "Nino a un malaise, veut parler maintenant. Les mots se cognent "
    "à la classe. À la maison, la chaussette bleue tombe sur la "
    "première marche. Il parle trop vite près de la porte. Il refuse "
    "de foncer, raconte près de l'escalier. Merci vécu. Un éclat de "
    "casier reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "miel",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "trois notes",
    "une chose, puis la suivante",
    "une chose puis l'autre",
    "une étape après l'autre",
    "yasmine",
    "radiateur",
    "éclat de laine",
    "éclat de marche",
    "éclat de nappe",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de crayon",
    "c'est du bon travail",
    "tu as fait du bon travail",
    "on aime écouter",
    "si tu as un malaise",
    "même leçon",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "tache de couleur",
    "ombre en forme de flèche",
    "marque fine",
    "minuscule symbole",
    "grain de miette",
    "grain de laine",
    "bande bleue",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de casier",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis malaise; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_parler_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="malaise",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_raconte_pres_de_l_escalier; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="escalier",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_porte_echoue_l_escalier_entend; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de casier",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_sans_regarder_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de casier",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pale; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "raconter",
    "accepted_examples": (
        "raconter | il raconte | à maman | à la maison | "
        "près de l'escalier | écouter"
    ),
    "retry_prompt": "Il raconte près de l'escalier. Que fait Nino ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "casier,pas",
        [
            "narrateur|Les casiers claquent dans le couloir.",
            "narrateur|Le métal est froid, un peu lisse.",
            "narrateur|Sur la porte, un éclat de casier luit.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, sur le métal ?",
            "narrateur|Nino accroche son manteau.",
            "narrateur|Le crochet fait tic.",
            "narrateur|Une étiquette pend au cartable.",
            "narrateur|Elle est froide sous le doigt.",
            "enfant-m|Elle pique un peu.",
            "papa|Je reviens te chercher.",
            "enfant-m|Oui, papa.",
            "narrateur|Papa serre l'épaule de Nino.",
            "narrateur|Il part vers la porte.",
            "narrateur|Une chaussette bleue dépasse du pantalon.",
            "narrateur|La laine est un peu rêche.",
            "enfant-m|Elle chatouille.",
            "narrateur|La classe sent les feuilles.",
            "narrateur|Un banc de bois attend sous la fenêtre.",
            "maitresse|Bonjour.",
            "enfant-m|Bonjour, maîtresse.",
            "narrateur|Nino pose le cartable près du banc.",
            "narrateur|Il s'assoit, le dos droit.",
            "narrateur|Un camarade s'approche du banc.",
            "narrateur|Il parle tout près, d'un secret.",
            "narrateur|Nino sent un malaise.",
            "narrateur|Son ventre se serre, petit.",
            "enfant-m|Je n'aime pas ça.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-m|Je le dis, maintenant !",
            "narrateur|En ce moment, Nino ouvre la bouche.",
            "narrateur|Ses mots se cognent à la classe.",
            "narrateur|Personne ne tourne la tête.",
            "enfant-m|Oh.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Nino referme la bouche.",
            "narrateur|Les mains restent sur les genoux.",
            "narrateur|Le ventre reste serré.",
            "narrateur|À la sortie, papa attend près des casiers.",
            "papa|On rentre, Nino ?",
            "enfant-m|Oui.",
            "narrateur|Nino touche l'éclat de casier, un instant.",
            "narrateur|Le soir, la porte de la maison s'ouvre.",
            "narrateur|Une lumière ronde vient de la cuisine.",
            "narrateur|Ça sent le cacao, un peu sucré.",
            "narrateur|L'escalier en bois craque.",
            "narrateur|Nino retire la chaussette trop vite.",
            "narrateur|Elle tombe sur la première marche.",
            "maman|Te voilà, Nino.",
            "papa|Le cacao est prêt.",
            "enfant-m|J'ai quelque chose, maintenant !",
            "narrateur|Nino avance trop vite vers la cuisine.",
            "narrateur|Maman remue la casserole.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino a un malaise.",
            "narrateur|Que fait-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "cacao,escalier",
        [
            "narrateur|Nino parle trop vite, près de la porte.",
            "enfant-m|Maman, un secret !",
            "narrateur|Maman n'a pas fini sa phrase.",
            "maman|Le cacao fume, Nino.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Il refuse de foncer.",
            "narrateur|Nino referme la bouche.",
            "narrateur|Il écoute la cuisine, un instant.",
            "papa|Tu veux venir près de l'escalier ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Nino pose un pied sur la marche.",
            "narrateur|Le bois est tiède, un peu lisse.",
            "narrateur|La chaussette bleue attend à côté.",
            "enfant-m|J'ai eu un malaise.",
            "enfant-m|Quelqu'un a parlé d'un secret.",
            "maman|On t'écoute.",
            "papa|Merci, Nino.",
            "narrateur|Papa a entendu toute la phrase.",
            "narrateur|Le ventre de Nino se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tu as soif ?",
            "enfant-m|Un peu, maman.",
            "narrateur|La lumière touche le bois.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "tasse,laine",
        [
            "narrateur|Nino prend la tasse trop vite.",
            "enfant-m|Je dis tout, d'un coup !",
            "narrateur|Le cacao tremble au bord.",
            "narrateur|La chaussette glisse d'un cran.",
            "enfant-m|Oh.",
            "narrateur|Nino avance les mains.",
            "narrateur|Puis il s'arrête net.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Papa attend, sans parler.",
            "narrateur|Nino observe la marche, écoute la maison.",
            "narrateur|Sur le cartable, un éclat de casier luit.",
            "enfant-m|Là, près de l'escalier.",
            "narrateur|Nino pose d'abord la tasse.",
            "narrateur|Puis il ramasse la laine.",
            "enfant-m|Le secret, c'était trop près.",
            "papa|Tu veux le dire ici ?",
            "enfant-m|Oui, papa.",
            "narrateur|Nino s'assoit sur la marche.",
            "enfant-m|Mon ventre s'est serré.",
            "maman|On est là.",
            "narrateur|La lumière de la cuisine touche le bois.",
            "narrateur|Nino boit une gorgée.",
            "narrateur|C'est chaud, un peu sucré.",
            "papa|Tu as fini ta tasse ?",
            "enfant-m|Presque.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "casier,cacao",
        [
            "enfant-m|Le casier brillait, papa.",
            "papa|Tu le vois, comme ce matin ?",
            "enfant-m|Oui, sur le métal.",
            "narrateur|Nino pose la chaussette sur la marche.",
            "maman|On la laisse là ?",
            "enfant-m|Oui, maman.",
            "narrateur|La lumière de la cuisine touche la laine.",
            "narrateur|Une vapeur monte du cacao.",
            "narrateur|Nino respire, plus large.",
            "narrateur|L'escalier en bois se tait.",
            "narrateur|Un éclat de casier reste pâle.",
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
        elif cid != "CHK_T0000_P0000":
            extra["pause_before_ms"] = 200
        by[cid] = voice(c, lines, profile, sons, extra)
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
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "il refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: refuse de foncer absent")
    if "yasmine" in blob:
        raise SystemExit(f"{SID}: Yasmine interdite")
    merci_n = sum(
        1
        for ln in blob.splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
        if "merci" in ln or "bravo" in ln
    )
    if merci_n != 1:
        raise SystemExit(f"{SID}: merci/bravo ×{merci_n}")
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
        "Les casiers claquent dans le couloir. Sur la porte, un éclat de "
        "casier luit. Nino accroche son manteau. Une chaussette bleue "
        "dépasse du pantalon. Un camarade parle tout près, d'un secret. "
        "Nino sent un **malaise**. Il veut le dire **maintenant**. Les mots "
        "se cognent à la classe. Sourire parti, épaules basses. À la "
        "maison, lumière de cuisine, cacao. Il retire la chaussette trop "
        "vite : elle tombe sur la première marche. Première idée : parler "
        "près de la porte. Les voix se mélangent. Il refuse de foncer. "
        "Près de l'escalier, il raconte. Merci vécu. Il veut tout dire "
        "d'un coup : la tasse tremble, la laine glisse. Il s'arrête, lit "
        "l'éclat. Sur la marche, un éclat de casier reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : école puis maison, casiers, chaussette bleue sur la "
        "première marche, escalier de bois, lumière de cuisine, cacao. "
        "≠ RAN.001-06 chaussettes radiateur / éclat de laine. ≠ ROU "
        "flaque/bottes. ≠ AUT.ROU.001-03 éclat de marche.\n"
        "- Désir : dire le malaise, maintenant.\n"
        "- Objet : chaussette bleue, casier, cartable, cacao, marche.\n"
        "- Indice unique : éclat de casier, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : le ventre serré, les mots qui pressent.\n"
        "- Imprévu 1 : parler pendant la classe, puis trop vite à la porte.\n"
        "- Cue : papa à la même hauteur, près de l'escalier. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : tout dire d'un coup, tasse et laine.\n"
        "- Résolution : il refuse de foncer, raconte près de l'escalier.\n"
        "- Retour : chaussette sur la marche, cacao, éclat de casier pâle.\n\n"
        "## Vécu\n\n"
        "Leçon COL.ECO.001 (écouter à l'école, en parler à la maison, "
        "jamais dite) greffée. La première idée (parler maintenant, à la "
        "porte) échoue. Le choix de Nino change l'action. Un « en ce "
        "moment ». Un merci vécu. Adulte + question. Troupe D16 : Nino, "
        "papa, maman. Maîtresse dump = label, pas de leçon parlée. "
        "Yasmine interdite.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : école puis maison, "
        "chaussette bleue, escalier de bois, lumière cuisine, cacao. "
        "Sans radiateur, sans lumière de miel.\n"
        "- Ouverture inventée (casiers qui claquent), pas un gabarit v2.\n"
        "- Indice unique : éclat de casier. Pas merle-trois-notes, miel, "
        "gouttes, pas tache/flèche/marque/symbole, pas éclat de "
        "marche/laine.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Question moteur inchangée (Nino a un malaise. Que fait-il ?). "
        "5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N3 ≤ 16. TTS : notes, ssml, xai, piper par chunk.\n\n"
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
