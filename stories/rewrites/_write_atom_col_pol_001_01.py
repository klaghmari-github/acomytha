#!/usr/bin/env python3
"""ATOM-COL.POL.001-01 — Le petit pain chaud de Nino (F-NAR-019, N1, COL.POL.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.POL.001-01"
TITLE = "Le petit pain chaud de Nino"
N1 = LIMITS["N1"]
INDICE = "éclat de pavé"
CHARS = "Nino, papa, maman"
SETTING = (
    "rue froide, pavés, boulangerie, file près du bois, "
    "odeur de pain, four"
)
FIL = (
    "Les pavés sonnent. Sur la pierre, un éclat de pavé luit. "
    "Nino veut le petit pain chaud maintenant. Il tend la main "
    "trop vite, sans le mot : la vitre arrête le doigt. Il refuse "
    "de foncer, dit s'il te plaît, obtient le sachet. Merci vécu. "
    "Un éclat de pavé reste pâle."
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
    "maîtresse",
    "maitresse",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "trois notes",
    "une chose, puis la suivante",
    "une chose puis l'autre",
    "une étape après l'autre",
    "yasmine",
    "mie",
    "pli",
    "poisson",
    "page",
    "escargot",
    "croûte",
    "croute",
    "farine",
    "nappe",
    "casserole",
    "fendu",
    "givre",
    "moineau",
    "radiateur",
    "éclat de casier",
    "éclat de laine",
    "éclat de marche",
    "éclat de nappe",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de crayon",
    "éclat de croûte",
    "éclat de seau",
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
    "tu as dit les mots",
    "tu as dit s'il te plaît",
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
        emphasis="éclat de pavé",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_pain_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="pain",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_dit_s_il_te_plait; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="s'il te plaît",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_vitre_echoue_le_mot_ouvre; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de pavé",
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
        emphasis="éclat de pavé",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pale; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "s'il te plaît",
    "accepted_examples": (
        "s'il te plaît | merci | bonjour | s'il te plait"
    ),
    "retry_prompt": "Il dit s'il te plaît. Que dit Nino ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "cloche,pas",
        [
            "narrateur|Les pavés sonnent sous les pas.",
            "narrateur|Ils sont froids, un peu ronds.",
            "narrateur|Sur la pierre, un éclat de pavé luit.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, sur la rue ?",
            "narrateur|Nino touche l'éclat de pavé, un instant.",
            "narrateur|La pierre pique un peu le doigt.",
            "enfant-m|Elle est froide.",
            "maman|La veste, un bouton de plus.",
            "papa|Voilà.",
            "narrateur|Un nuage blanc sort de la bouche.",
            "enfant-m|J'ai les joues froides.",
            "papa|On marche.",
            "maman|Tu restes près de nous ?",
            "enfant-m|Oui, maman.",
            "narrateur|Une odeur de pain arrive.",
            "narrateur|Elle vient du four.",
            "enfant-m|Ça sent le four !",
            "maman|Tu sens, Nino ?",
            "enfant-m|Oui.",
            "narrateur|La porte de bois attend.",
            "narrateur|Une petite cloche fait ding.",
            "narrateur|L'air chaud touche les joues.",
            "narrateur|Une file avance près du bois.",
            "papa|On reste dans la file.",
            "narrateur|Des manteaux se touchent dans la file.",
            "narrateur|Ça sent le beurre, un peu chaud.",
            "enfant-m|Je le veux, maintenant.",
            "narrateur|En ce moment, Nino serre le manteau.",
            "narrateur|Le sol est tiède sous ses chaussures.",
            "narrateur|Le bois du comptoir est lisse.",
            "enfant-m|Le four est là.",
            "maman|Il chauffe derrière le mur.",
            "narrateur|Une lueur orange tient derrière le verre.",
            "narrateur|Nino se dresse sur les pointes.",
            "narrateur|Un petit pain doré attend derrière la vitre.",
            "enfant-m|Celui-là !",
            "narrateur|Nino tend la main trop vite.",
            "narrateur|Le doigt tape la vitre.",
            "enfant-m|Oh.",
            "narrateur|Le pain reste derrière le verre.",
            "narrateur|La file n'a pas bougé.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-m|Je le prends !",
            "maman|Le pain est derrière le verre.",
            "papa|Tu le vois, Nino ?",
            "narrateur|Les épaules de Nino tombent un peu.",
            "narrateur|Ça serre, dans son ventre.",
            "narrateur|Papa se baisse à sa hauteur.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino veut le pain.",
            "narrateur|Que dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "papier,cloche",
        [
            "narrateur|Nino avance trop vite vers le bois.",
            "enfant-m|Celui-là, maintenant !",
            "narrateur|Sa voix se mélange à la file.",
            "enfant-m|Oh.",
            "narrateur|Le petit pain reste derrière la vitre.",
            "narrateur|Il refuse de foncer.",
            "narrateur|Nino referme la main.",
            "narrateur|Il écoute la cloche, un instant.",
            "papa|Tu veux venir près du bois ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Nino pose un pied sur le pas.",
            "narrateur|Le bois est tiède, un peu lisse.",
            "enfant-m|Celui-là.",
            "enfant-m|S'il te plaît.",
            "narrateur|Derrière le bois, une main se tend.",
            "narrateur|Le papier enveloppe le pain.",
            "narrateur|Le sachet est chaud contre le manteau.",
            "papa|Merci, Nino.",
            "narrateur|Papa a entendu toute la phrase.",
            "narrateur|Le ventre de Nino se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tu as les mains au chaud ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Ça sent le beurre et le four.",
            "enfant-m|Le pain est à moi.",
            "maman|Il est dans tes mains.",
            "narrateur|Nino pose une main sur le sachet.",
            "narrateur|Le papier est un peu rêche.",
            "narrateur|La cloche se tait.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pas,papier",
        [
            "narrateur|Nino tire le sachet trop vite.",
            "enfant-m|Je le mange, d'un coup !",
            "narrateur|Le papier glisse entre les doigts.",
            "narrateur|Le pain penche vers le sol.",
            "enfant-m|Oh.",
            "narrateur|Nino avance les mains.",
            "narrateur|Puis il s'arrête net.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Papa attend, sans parler.",
            "narrateur|Nino observe le pas, écoute la rue.",
            "narrateur|Sur la pierre, un éclat de pavé luit.",
            "enfant-m|Là, près de la porte.",
            "narrateur|Nino tient le sachet des deux mains.",
            "narrateur|Le papier est rêche, un peu chaud.",
            "enfant-m|Il est chaud, papa.",
            "papa|Tu le portes jusqu'à la rue ?",
            "enfant-m|Oui, papa.",
            "maman|On sort ?",
            "enfant-m|Oui, maman.",
            "narrateur|La porte s'ouvre.",
            "narrateur|La cloche fait ding.",
            "narrateur|L'air froid revient sur les joues.",
            "narrateur|Nino serre le sachet contre lui.",
            "enfant-m|Il reste chaud.",
            "papa|On marche.",
            "narrateur|Le sachet penche, puis se cale.",
            "enfant-m|Je le tiens.",
            "maman|On avance.",
            "narrateur|Nino passe le pas de bois.",
            "narrateur|Le bois craque, un peu.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "pas",
        [
            "enfant-m|Le pavé brillait, papa.",
            "papa|Tu le vois, comme dans la rue ?",
            "enfant-m|Oui, sur la pierre.",
            "narrateur|Nino pose le sachet contre le manteau.",
            "maman|On le garde au chaud ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Le four sentait bon.",
            "maman|Il est contre toi.",
            "narrateur|Une vapeur monte du papier.",
            "narrateur|Nino respire, plus large.",
            "papa|On rentre ?",
            "enfant-m|Oui.",
            "narrateur|Les joues de Nino se réchauffent.",
            "narrateur|Le sachet reste tiède sous la main.",
            "narrateur|Un éclat de pavé reste pâle.",
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
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
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
    if re.search(r"\btom\b", blob):
        raise SystemExit(f"{SID}: Tom interdit")
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
        "Les pavés sonnent sous les pas. Sur la pierre, un éclat de pavé "
        "luit. Rue froide, nuage de souffle, odeur de four. La cloche fait "
        "ding. Une file près du bois. Nino veut le petit pain doré "
        "**maintenant**. Première idée : tendre la main trop vite, sans le "
        "mot. Le doigt tape la vitre. Sourire parti, épaules basses. Il "
        "refuse de foncer. Près du bois, il dit s'il te plaît. Le sachet "
        "arrive. Merci vécu. Il veut mordre d'un coup : le papier glisse. "
        "Il s'arrête, lit l'éclat. Sur la rue, un éclat de pavé reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : rue froide, pavés, boulangerie, file, four, cloche, "
        "sachet. ≠ AUT.ROU.001-03 Nino escalier / éclat de marche. ≠ "
        "COL.ECO.001-03 Victorino nappe / éclat de croûte.\n"
        "- Désir : le petit pain chaud, maintenant.\n"
        "- Objet : petit pain doré, sachet, vitre, cloche, pavé.\n"
        "- Indice unique : éclat de pavé, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : les joues froides, le pain derrière le verre.\n"
        "- Imprévu 1 : prendre / demander trop vite, sans le mot ; la "
        "vitre et la file arrêtent le geste.\n"
        "- Cue : papa à la même hauteur, près du bois. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : mordre d'un coup, sachet qui glisse.\n"
        "- Résolution : il refuse de foncer, dit s'il te plaît, tient "
        "le sachet des deux mains.\n"
        "- Retour : sachet tiède contre le manteau, éclat de pavé pâle.\n\n"
        "## Vécu\n\n"
        "Leçon COL.POL.001 (dire s'il te plaît, jamais dite comme règle) "
        "greffée. La première idée (prendre maintenant, sans le mot) "
        "échoue. Le choix de Nino change l'action. Un « en ce moment ». "
        "Un merci vécu. Adulte + question. Troupe D16 : Nino, papa, "
        "maman. Dump Tom → Nino. Papa ajouté (dump n'avait que maman). "
        "Pas de maîtresse. Question moteur inchangée.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le petit pain chaud de Nino. Lieu du dump : "
        "boulangerie, rue froide, pavés, odeur de pain, four. Magasin, "
        "file, pain. Sans escalier, sans nappe, sans farine, sans croûte.\n"
        "- Ouverture inventée (pavés qui sonnent), pas un gabarit v2, "
        "pas « la rue est froide », pas fleurs de givre.\n"
        "- Indice unique : éclat de pavé. Pas merle-trois-notes, miel, "
        "gouttes, pas tache/flèche/marque/symbole, pas éclat de "
        "marche/nappe/croûte. Ban mie, pli, poisson, page, escargot.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : pas « tu demandes », pas « tu as dit les "
        "mots ». Nino dit s'il te plaît, le pain vient.\n"
        "- Question moteur inchangée (Nino veut le pain. Que dit-il ?). "
        "retry Tom→Nino. 5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N1 ≤ 10. TTS : notes, ssml, xai, piper par chunk.\n\n"
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
