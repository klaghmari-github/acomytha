#!/usr/bin/env python3
"""ATOM-DIF.BES.001-05 — La carte d'Aniss (F-NAR-019, N2, DIF.BES.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.001-05"
TITLE = "La carte d'Aniss"
N2 = LIMITS["N2"]
CHARS = "Aniss, papa, maman"
SETTING = "classe"
INDICE = "éclat de bois"
FIL = (
    "Une barre de soleil rampe sur le plancher. Sur le bois de la chaise, "
    "un éclat de bois brille. Aniss veut la carte de l'oiseau, maintenant. "
    "Il plonge trop vite : les cartes glissent, le bruit monte. Il a besoin "
    "de calme. Papa dit les deux mots trop vite. Aniss n'entend pas. Papa "
    "les dit plus lent. Aniss refuse de foncer, observe, pioche, montre. "
    "Merci vécu. Il envoie la carte sous la chaise. Il retrouve l'éclat, "
    "reprend sans brusquer. Sur le bois, l'éclat tient."
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
    "maîtresse",
    "maitresse",
    "olympe",
    "swann",
    "raphaël",
    "raphael",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai observé",
    "j'ai observe",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "c'est la règle",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "éclat de carte",
    "éclat de cube",
    "éclat de boule",
    "éclat de galet",
    "éclat de panier",
    "éclat de dorure",
    "éclat de cloche",
    "éclat de corbeille",
    "éclat de crayon",
    "éclat de carton",
    "éclat de pompon",
    "éclat de sac",
    "éclat de laine",
    "éclat de tasse",
    "éclat de chaise",
    "éclat de carotte",
    "éclat de seau",
    "éclat de mousse",
    "éclat de cartable",
    "éclat de casserole",
    "éclat de nappe",
    "éclat de wagon",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de pinceau",
    "éclat de ballon",
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
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "bulle",
    "savon",
    "chemise bleue",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de bois",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_carte_oiseau_maintenant; "
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
            "sous_texte=on_peut_redire_les_mots_plus_lent; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="oiseau",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=papa_redite_il_observe_puis_pioche; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de bois",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de bois",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_chaise; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "répéter",
    "accepted_examples": (
        "répéter | observer | observer d'abord | la règle"
    ),
    "retry_prompt": "On répète la règle. Aniss peut quoi d'abord ?",
    "engine_ok_text": "Oui, on répète.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "chaise,cartes",
        [
            "narrateur|Une barre de soleil rampe sur le plancher.",
            "narrateur|Dans la barre, un peu de poussière flotte.",
            "narrateur|Les crayons sentent le bois, près du mur.",
            "narrateur|Une chaise racle, puis s'arrête.",
            "narrateur|Le carton de cartes attend sous la lumière.",
            "narrateur|Dedans, les cartes glissent un peu.",
            "narrateur|Sur le bois de la chaise, un éclat de bois brille.",
            "enfant-m|Il est petit, papa.",
            "papa|C'est le bois, sous le soleil.",
            "narrateur|Papa tient la main d'Aniss.",
            "papa|Ta main est bien dans la mienne.",
            "maman|Le cartable attend près de la porte.",
            "narrateur|La fermeture du cartable est un peu froide.",
            "enfant-m|Je veux la carte de l'oiseau, maintenant !",
            "maman|Avant de partir ?",
            "enfant-m|Oui, tout de suite !",
            "narrateur|En ce moment, Aniss plonge la main dans le carton.",
            "narrateur|Les cartes glissent contre ses doigts.",
            "narrateur|Une carte tombe, puis une autre.",
            "narrateur|La chaise racle plus fort.",
            "narrateur|Papa parle à maman, près de la porte.",
            "papa|Le cartable est près du banc.",
            "maman|Oui, avec la fermeture.",
            "enfant-m|Papa, l'oiseau !",
            "narrateur|Les mots d'Aniss se cognent aux leurs.",
            "narrateur|Personne ne tourne la tête.",
            "papa|Tu disais quelque chose, Aniss ?",
            "enfant-m|La carte va partir.",
            "narrateur|Aniss plonge trop vite, une deuxième fois.",
            "narrateur|Le carton penche, puis se recale.",
            "narrateur|L'oiseau disparaît sous les autres cartes.",
            "enfant-m|Oh.",
            "narrateur|L'éclat de bois tremble, puis tient.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-m|Ça fait trop de bruit, maman.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Il recule jusqu'au mur.",
            "narrateur|Ses mains touchent le mur, plates.",
            "narrateur|Aniss a besoin de calme.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|Tu regardes le carton ?",
            "enfant-m|Oui, papa.",
            "maman|Les crayons sentent le bois, ici.",
            "papa|On pioche.",
            "papa|On montre.",
            "narrateur|Les deux mots passent trop vite, dans le bruit.",
            "enfant-m|Je n'ai pas entendu.",
            "narrateur|Aniss serre le mur contre ses paumes.",
            "narrateur|Il ouvre la bouche.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "cartes",
        [
            "narrateur|Papa se rapproche, sans presser.",
            "papa|On pioche.",
            "papa|On montre.",
            "narrateur|Cette fois, les mots arrivent lents.",
            "enfant-m|On pioche.",
            "enfant-m|On montre.",
            "narrateur|Aniss regarde le carton, sans y mettre la main.",
            "narrateur|Papa pioche une carte, sans brusquer.",
            "narrateur|Il la montre, près du soleil.",
            "papa|C'est un arbre.",
            "enfant-m|Je vois l'arbre.",
            "maman|Tu as regardé le carton ?",
            "enfant-m|Oui, maman.",
            "narrateur|Aniss tend la main, plus légère.",
            "narrateur|Il pioche une carte.",
            "narrateur|C'est l'oiseau.",
            "narrateur|Il la montre, sans la jeter.",
            "enfant-m|C'est mon oiseau.",
            "papa|Merci, Aniss.",
            "narrateur|Papa a vu l'oiseau, entier.",
            "maman|Tu as fini de la montrer ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le ventre d'Aniss se desserre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "chaise,cartes",
        [
            "narrateur|Aniss veut poser la carte dans le carton.",
            "enfant-m|Je la mets, maintenant !",
            "narrateur|Il envoie la carte trop vite.",
            "narrateur|La carte glisse sous la chaise.",
            "enfant-m|Oh.",
            "narrateur|L'oiseau a disparu, sous le bois.",
            "narrateur|Aniss veut ramper tout de suite.",
            "narrateur|Il refuse de foncer.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe la chaise, puis le plancher.",
            "narrateur|Il écoute le silence de la classe.",
            "narrateur|Sous le pied de la chaise, un éclat de bois brille.",
            "enfant-m|Il est là.",
            "enfant-m|Comme tout à l'heure.",
            "papa|Tu le vois, sur le bois ?",
            "enfant-m|Oui, et l'oiseau aussi.",
            "narrateur|Aniss avance la main, plus légère.",
            "narrateur|Il reprend la carte, sans brusquer.",
            "narrateur|L'oiseau est un peu poussiéreux.",
            "enfant-m|Il est là, maman.",
            "maman|On voit l'oiseau.",
            "papa|Et le carton, à côté ?",
            "enfant-m|Je le pose, sans jeter.",
            "narrateur|Aniss glisse la carte dans le carton.",
            "narrateur|Les cartes font un petit bruit, puis rien.",
            "enfant-m|Ffff.",
            "narrateur|Aniss souffle sur le bois de la chaise.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "chaise",
        [
            "narrateur|Le carton repose près de la chaise.",
            "narrateur|L'oiseau reste dedans, avec les autres.",
            "enfant-m|Comme tout à l'heure, papa !",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur le bois.",
            "maman|On est bien, ici.",
            "narrateur|La barre de soleil a bougé, sur le plancher.",
            "narrateur|Aniss glisse la chaise sans se presser.",
            "narrateur|Le bois repose contre le plancher.",
            "enfant-m|On le voit, maman.",
            "maman|Tu le vois sur le bois ?",
            "enfant-m|Oui, l'éclat.",
            "maman|Tu as fini de fermer le cartable ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le soir reste dans l'air de la classe.",
            "narrateur|L'éclat de bois tient sur la chaise.",
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
    if INDICE not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé au climax")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Aniss a besoin de calme. Que peut-on faire ?":
        raise SystemExit(f"{SID}: question changée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "répéter":
        raise SystemExit(f"{SID}: expected_answer")
    for bad_name in ("olympe", "swann", "raphaël", "raphael"):
        if bad_name in blob:
            raise SystemExit(f"{SID}: nom interdit {bad_name}")
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
        "- **Leçon :** DIF.BES.001 — besoin de calme / répéter (vécue : "
        "veut l'oiseau maintenant ; plonge trop vite ; bruit ; n'entend "
        "pas les mots ; papa les dit plus lent ; observe ; pioche ; "
        "montre ; refuse de foncer sous la chaise)\n"
        "- **Personnages :** Aniss, papa, maman. Troupe D16. Dump "
        "Olympe / Swann / Raphaël retirés. Un héros + papa/maman.\n"
        "- **Lieu :** classe (crayons, chaise, soleil sur plancher, carton "
        "de cartes). ≠ ATOM-DIF.BES.001-01 Les cartes de Sarah (éclat de "
        "carte BAN). Pas cour / linge / bulle.\n"
        "- **Indice unique :** éclat de bois (chaise au soleil → tremble "
        "quand le carton penche → sous le pied de chaise → tient sur le "
        "bois). Pas éclat de carte / crayon / carton / cube / boule / "
        "galet / panier / dorure / cloche / corbeille.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une barre de soleil rampe sur le plancher. Sur le bois de la "
        "chaise, un éclat de bois brille. Aniss veut la carte de l'oiseau "
        "**maintenant**. Il plonge trop vite : les cartes tombent, la "
        "chaise racle, les mots se cognent. L'oiseau disparaît. Sourire "
        "parti, épaules basses, mains au mur. Papa se baisse, dit les deux "
        "mots trop vite. Aniss n'entend pas. Question. Papa les dit plus "
        "lent. Aniss les dit, observe, pioche l'oiseau, montre. Merci "
        "vécu. Il envoie la carte trop vite sous la chaise. Il refuse de "
        "foncer, retrouve l'éclat, reprend sans brusquer. Sur le bois, "
        "l'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : classe, barre de soleil, poussière, crayons, chaise, "
        "carton de cartes, cartable près de la porte.\n"
        "- Désir : la carte de l'oiseau, maintenant, avant de partir.\n"
        "- Objet : carte oiseau, carton, chaise de bois.\n"
        "- Indice unique : éclat de bois, vu dès l'ouverture, payé sous "
        "la chaise et à la fin.\n"
        "- Urgence douce : partir, l'oiseau va glisser.\n"
        "- Imprévu 1 : il plonge trop vite ; le bruit mange les mots.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après l'oiseau montré entier.\n"
        "- Imprévu 2 (plus rusé) : il envoie la carte pour la ranger ; "
        "elle glisse sous la chaise.\n"
        "- Résolution : il refuse de foncer, écoute, lit l'éclat, reprend.\n"
        "- Retour : barre de soleil déplacée, cartable fermé, éclat sur "
        "le bois.\n\n"
        "## Vécu\n\n"
        "Aniss veut l'oiseau **maintenant**. Impatience (plonge, bruit, "
        "mots perdus), puis sourire qui disparaît, épaules qui tombent, "
        "mains au mur. Papa se baisse, pose une question, ne récite pas "
        "la leçon. Il redit les deux mots, plus lent. Aniss les dit, "
        "regarde, pioche, montre. Merci vécu après la phrase entière. "
        "Fin : l'éclat du début tient sur la chaise.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau : La carte d'Aniss. Lieu du dump : classe, crayons, "
        "chaise, soleil sur plancher, carton de cartes. Relance : Aniss a "
        "besoin de calme. Que peut-on faire ? expected répéter.\n"
        "- Ouverture inventée (barre de soleil sur le plancher), pas un "
        "gabarit v2, pas « joue au salon », pas « est dans l'entrée ».\n"
        "- Indice unique : éclat de bois (roster). Pas éclat de carte "
        "(001-01), pas éclat de crayon (ECO.001-01), pas éclat de carton "
        "(ECO.002-03), pas cube/boule/galet/panier/dorure/cloche/"
        "corbeille, pas merle, miel, marque fine.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` "
        "retirés. Olympe / Swann / Raphaël hors texte.\n"
        "- Leçon non dite : on l'entend quand papa redit les mots, plus "
        "lent, et qu'Aniss observe avant de piocher. Pas « c'est la "
        "règle », pas « il faut attendre ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée (répéter). 5 chunks, kinds "
        "inchangés. example4 082 / 014 / 046.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive vers la chaise.\n"
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
