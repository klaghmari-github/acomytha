#!/usr/bin/env python3
"""ATOM-DIF.BES.001-03 — Les galets de Nina (F-NAR-019, N3, DIF.BES.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.001-03"
TITLE = "Les galets de Nina"
N3 = LIMITS["N3"]
CHARS = "Nina, papa, maman"
SETTING = "jardin après la pluie"
INDICE = "éclat de galet"
FIL = (
    "Une goutte froide touche le nez de Nina. Sur un galet, un éclat "
    "de galet brille. Elle veut un chemin jusqu'à l'escargot, maintenant. "
    "Trop de galets d'un coup : ils glissent. Sourire parti. Papa à sa "
    "hauteur. Elle répète : un galet, une couleur. Elle regarde d'abord, "
    "pose le gris. Merci vécu. Trois galets trop vite : l'éclat manque. "
    "Elle refuse de foncer. L'éclat de galet tient sur le bleu."
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
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "léa",
    "lea",
    "sami",
    "raphaël",
    "raphael",
    "j'ai compris",
    "j'ai répété",
    "j'ai repete",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "c'est la règle",
    "c'est la regle",
    "observer d'abord, c'est possible",
    "tu as su répéter",
    "tu as su repeter",
    "tu as laissé le temps",
    "tu as laisse le temps",
    "on a pris le temps",
    "chacun son temps",
    "gouttière",
    "gouttiere",
    "zinc",
    "bonbons",
    "seau",
    "mousse",
    "tapis",
    "cartes",
    "tortue",
    "pâte",
    "pate",
    "spirale",
    "farine",
    "arrosoir",
    "nappe",
    "bassine",
    "coquille",
    "grain de",
    "lune d'étain",
    "lune d'etain",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat d'escargot",
    "eclat d'escargot",
    "éclat de seau",
    "éclat de mousse",
    "éclat de carton",
    "éclat de pli",
    "éclat de pin",
    "éclat de laine",
    "éclat de pompon",
    "éclat de carotte",
    "éclat de caillou",
    "éclat de grain",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de galet",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_chemin_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="calme",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_a_besoin_de_calme_on_peut_repeter; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de galet",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_repète_regarde_pose_le_gris; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de galet",
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
        emphasis="éclat de galet",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bleu; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "répéter",
    "accepted_examples": (
        "répéter | observer | observer d'abord | la règle"
    ),
    "retry_prompt": "On répète. Un galet, une couleur. Que peut-on faire ?",
    "engine_ok_text": "Oui, on répète.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "jardin,feuilles",
        [
            "narrateur|Une goutte froide tombe de la branche.",
            "narrateur|Elle touche le nez de Nina.",
            "enfant-f|Oh, c'est froid !",
            "papa|C'est la pluie, dans les feuilles.",
            "narrateur|Un oiseau secoue une feuille, là-haut.",
            "narrateur|La feuille collée brille sur le banc.",
            "maman|Tu as vu la feuille, Nina ?",
            "enfant-f|Elle brille, maman.",
            "maman|Le bois est sombre, dessous.",
            "narrateur|Maman essuie le banc avec la main.",
            "narrateur|Le bois reste froid et sombre.",
            "papa|Tu as senti la terre ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Elle est mouillée.",
            "narrateur|L'herbe mouillée colle aux chaussures.",
            "narrateur|Ça sent la terre, tout près.",
            "papa|Tes chaussures sont mouillées.",
            "enfant-f|Elles collent, papa.",
            "maman|On reste près du banc.",
            "enfant-f|D'accord, maman.",
            "narrateur|Des galets luisent dans la terre noire.",
            "narrateur|Sur un galet, un éclat de galet brille.",
            "enfant-f|Il brille, papa !",
            "papa|C'est l'eau, sur la pierre.",
            "enfant-f|Je veux un chemin, maintenant !",
            "enfant-f|Jusqu'à l'escargot.",
            "maman|Un galet.",
            "maman|Une couleur.",
            "narrateur|Un escargot avance sur une pierre.",
            "maman|Tu as vu l'escargot, Nina ?",
            "enfant-f|Il va, maman.",
            "maman|On le laisse sur sa pierre.",
            "papa|On marche vers les galets ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina a une idée, très nette.",
            "enfant-f|Tous les galets, d'un coup !",
            "narrateur|Nina prend trop de galets, d'un coup.",
            "narrateur|Elle les jette vers la pierre.",
            "narrateur|Les galets glissent dans la boue.",
            "enfant-f|Oh.",
            "narrateur|Le chemin ne se fait pas.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|L'éclat de galet tremble, puis tient.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-f|Ça ne veut pas.",
            "narrateur|Ses épaules tombent, un peu lourdes.",
            "narrateur|Ça tape fort, dans sa poitrine.",
            "narrateur|Papa se met à sa hauteur.",
            "papa|Tu veux le chemin ?",
            "enfant-f|Oui, papa.",
            "narrateur|En ce moment, Nina pose les mains sur le bois.",
            "narrateur|Ses doigts restent là, sans bouger.",
            "narrateur|Le banc est lisse, un peu froid.",
            "papa|Tu restes un peu, Nina ?",
            "enfant-f|Oui.",
            "narrateur|Elle regarde l'escargot, sans avancer.",
            "narrateur|L'escargot n'a presque pas bougé.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nina a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "galets",
        [
            "narrateur|Papa parle, près du banc.",
            "papa|Un galet.",
            "papa|Une couleur.",
            "enfant-f|Un galet.",
            "enfant-f|Une couleur.",
            "narrateur|Nina veut tout prendre, d'un coup.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Elle referme les mains, un instant.",
            "narrateur|Elle regarde les galets, dans la boue.",
            "narrateur|Elle ne prend rien, d'abord.",
            "maman|Tu regardes, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Elle choisit un galet gris.",
            "enfant-f|Gris.",
            "narrateur|Le galet fait un petit bruit sur la terre.",
            "papa|Merci, Nina.",
            "narrateur|Papa a vu le gris rester.",
            "narrateur|Sur le gris, l'éclat de galet brille.",
            "enfant-f|Il est là.",
            "maman|Sur ce gris ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina pose un galet brun, plus loin.",
            "enfant-f|Brun.",
            "narrateur|Le chemin avance vers la pierre.",
            "papa|Il tient, celui-là ?",
            "enfant-f|Oui, papa.",
            "narrateur|L'escargot avance d'un tout petit pas.",
            "enfant-f|Il est là, maman.",
            "maman|Sur sa pierre ?",
            "enfant-f|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "oiseau,galets",
        [
            "narrateur|Un oiseau chante dans l'arbre.",
            "enfant-f|J'ai entendu.",
            "papa|Tu as entendu l'oiseau ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Tout haut.",
            "narrateur|Nina veut arriver, d'un coup.",
            "narrateur|Elle prend trois galets trop vite.",
            "narrateur|Un galet roule vers la pierre.",
            "enfant-f|Ça tombe !",
            "narrateur|L'éclat de galet n'est plus là.",
            "enfant-f|Il est parti.",
            "narrateur|Nina veut foncer, d'un coup.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Ses épaules se serrent un peu.",
            "narrateur|Ça tape fort, dans sa poitrine.",
            "narrateur|Personne ne dit la suite à voix haute.",
            "narrateur|Elle regarde les galets, un à un.",
            "narrateur|Elle écoute le jardin, un instant.",
            "enfant-f|Comme tout à l'heure ?",
            "papa|Tu le vois, toi ?",
            "enfant-f|Non, plus sur le gris.",
            "narrateur|Nina cherche près de la pierre.",
            "enfant-f|Il est là.",
            "papa|Sur ce bleu ?",
            "enfant-f|Oui, sur ce galet.",
            "narrateur|Elle pose le bleu, sans se presser.",
            "enfant-f|Bleu.",
            "narrateur|Le dernier galet touche la pierre.",
            "enfant-f|Le chemin est arrivé.",
            "maman|L'escargot est là ?",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "jardin",
        [
            "narrateur|Le chemin brille un peu, dans la terre.",
            "narrateur|L'escargot reste sur sa pierre.",
            "enfant-f|L'éclat est là, papa.",
            "papa|Tu le vois sur le galet ?",
            "enfant-f|Oui, papa.",
            "maman|On est bien, ici.",
            "narrateur|Les chaussures laissent des traces mouillées.",
            "papa|Elles vont sécher.",
            "enfant-f|Les galets sont froids.",
            "maman|Ils vont sécher, eux aussi.",
            "narrateur|Nina pose la joue près du banc.",
            "narrateur|Le bois est sombre, un peu froid.",
            "enfant-f|C'est froid.",
            "maman|La feuille est là, Nina.",
            "enfant-f|Oui, maman.",
            "narrateur|Un oiseau se tait, dans l'arbre.",
            "narrateur|L'éclat de galet tient sur le bleu.",
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
            if re.search(rf"(?<!\w){re.escape(bad)}(?!\w)", low):
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
        if c.get("kind") != by[cid].get("kind"):
            raise SystemExit(f"{cid}: kind changé")
    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    adults = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
    ).lower()
    if adults.count("merci") != 1:
        raise SystemExit(f"{SID}: merci ×{adults.count('merci')}")
    if "bravo" in adults:
        raise SystemExit(f"{SID}: bravo en trop")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 5:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 5)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "éclat d'escargot" in blob:
        raise SystemExit(f"{SID}: BAN éclat d'escargot (ECO.002-11)")
    for name in ("léa", "lea", "sami", "raphaël", "raphael"):
        if re.search(rf"\b{name}\b", blob):
            raise SystemExit(f"{SID}: BAD_NAMES / second enfant: {name}")
    if "copain|" in blob or "copine|" in blob:
        raise SystemExit(f"{SID}: second enfant (copain/copine)")
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Nina a besoin de calme. Que peut-on faire ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "répéter":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = (by["CHK_T0000_P0000_Q0001"].get("retry_prompt") or "").lower()
    if "léa" in retry or "lea" in retry or "raphaël" in retry:
        raise SystemExit(f"{SID}: Léa/Raphaël dans retry_prompt")
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
        "- **Public :** N3 (≤16), audio familial\n"
        "- **Leçon :** DIF.BES.001 — besoin de calme / plus de temps "
        "(vécue : veut le chemin maintenant ; trop de galets d'un coup ; "
        "ils glissent ; mains sur le banc ; elle répète un galet, une "
        "couleur ; elle regarde d'abord ; pose le gris ; refuse de "
        "foncer ; le bleu arrive)\n"
        "- **Personnages :** Nina, papa, maman. Troupe D16. Un héros. "
        "Sami / Léa dump → absents (BAD_NAMES). Raphaël dump → absent. "
        "Papa parle (ajout).\n"
        "- **Lieu :** jardin après la pluie, feuilles, escargot sur "
        "pierre, banc sombre, galets, herbe mouillée, terre. ≠ 001-01 "
        "classe/tapis/tortue. ≠ 001-02 pâte/spirale/nappe. ≠ gouttière/"
        "seau/mousse (xlsx intermédiaire). Pas éclat d'escargot "
        "(BAN ECO.002-11).\n"
        "- **Indice unique :** éclat de galet (galet du début → tremble "
        "dans la boue → brille sur le gris → manque après le roulement "
        "→ tient sur le bleu).\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte froide tombe de la branche, touche le nez. Une "
        "feuille collée brille sur le banc sombre. Sur un galet, un "
        "éclat de galet brille. Nina veut un chemin jusqu'à l'escargot "
        "**maintenant**. Première idée : tous les galets d'un coup. Ils "
        "glissent dans la boue. Sourire parti, épaules basses. Papa se "
        "met à sa hauteur. Mains sur le bois. Question : Nina a besoin "
        "de calme. Que peut-on faire ? Elle répète : un galet, une "
        "couleur. Elle regarde d'abord, pose le gris. Merci vécu. "
        "Trois galets trop vite : l'éclat manque. Elle refuse de "
        "foncer, cherche, pose le bleu. L'éclat de galet tient sur "
        "le bleu.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : goutte, branche, oiseau, feuille collée, banc sombre, "
        "terre, herbe, chaussures, galets, escargot sur pierre.\n"
        "- Désir : un chemin de galets jusqu'à l'escargot, maintenant.\n"
        "- Objet : galets, chemin, escargot, banc.\n"
        "- Indice unique : éclat de galet, vu dès l'ouverture, payé à "
        "la fin.\n"
        "- Urgence douce : le chemin, l'escargot qui avance, trois "
        "galets trop vite.\n"
        "- Imprévu 1 : trop de galets d'un coup ; ils glissent.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : arriver d'un coup ; un galet roule ; "
        "l'éclat manque.\n"
        "- Résolution : elle répète, regarde d'abord, refuse de foncer, "
        "pose un à un.\n"
        "- Retour : chemin, escargot sur sa pierre, feuille, éclat du "
        "début sur le bleu.\n\n"
        "## Vécu\n\n"
        "Nina veut le chemin **maintenant**. Impatience, puis sourire "
        "qui s'en va. Les mains restent sur le banc. Papa se met à sa "
        "hauteur, pose une question, ne récite pas la leçon. Nina agit : "
        "elle répète, elle regarde, elle pose le gris. Merci vécu après "
        "le galet qui reste. Fin : l'éclat du début tient sur le bleu.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Les galets de Nina. Lieu du dump : jardin après "
        "pluie, feuilles, escargot sur pierre, banc sombre, galets. "
        "Relance : Nina a besoin de calme. Que peut-on faire ? expected "
        "répéter. retry sans Léa.\n"
        "- Ouverture inventée (goutte froide sur le nez, oiseau, feuille "
        "collée), pas un gabarit v2, pas « la pluie a fini », pas "
        "gouttière/seau/mousse.\n"
        "- Indice unique : éclat de galet. Pas éclat d'escargot "
        "(BAN ECO.002-11). ≠ 001-01 tortue/cartes. ≠ 001-02 pâte/"
        "spirale.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Sami, Léa, Raphaël retirés.\n"
        "- Leçon non dite : on la voit quand elle répète, regarde, pose "
        "un galet. Pas « c'est la règle », pas « tu as su répéter ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Papa parle.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle plus tendu au roulement.\n"
        f"- {nwords} mots. N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
