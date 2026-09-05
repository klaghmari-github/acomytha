#!/usr/bin/env python3
"""ATOM-COL.ECO.002-05 — Le pompon d'Aniss (F-NAR-019, N1, COL.ECO.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.002-05"
TITLE = "Le pompon d'Aniss"
N1 = LIMITS["N1"]
CHARS = "Aniss, papa, maman, maîtresse"
SETTING = "entrée, classe, puis maison"
INDICE = "éclat de pompon"
FIL = (
    "Un nuage de lait pousse jusqu'au manteau. Sur le pompon rouge, un "
    "éclat de pompon brille. Aniss veut parler du rouge, maintenant. Il "
    "coupe papa : les mots se perdent. Il tire trop vite : la fermeture "
    "se coince. À l'école, sa phrase se cogne à la classe. Il refuse de "
    "foncer, lève la main, attend, dit le rouge. Merci vécu. Sur la "
    "laine, l'éclat de pompon tient."
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
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "tu attends ton tour",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "éclat de carotte",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de laine",
    "éclat de tasse",
    "éclat de crayon",
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
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de pompon",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_parler_du_rouge_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="parler",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_attend_avant_de_parler; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="silence",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_leve_la_main_puis_on_l_entend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="manteau",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_sur_le_manteau; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de pompon",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_laine; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "attendre",
    "accepted_examples": (
        "attendre | il attend | lever la main | la main | il lève la main "
        "| son tour | il attend son tour"
    ),
    "retry_prompt": "Il lève la main et il attend. Que fait Aniss ?",
    "engine_ok_text": "Oui, il attend.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "pompon,porte",
        [
            "narrateur|Un nuage de lait pousse jusqu'au manteau.",
            "narrateur|Le pompon rouge tape la fermeture.",
            "narrateur|La laine est rêche sous le pouce.",
            "narrateur|L'air sent le lait chaud.",
            "narrateur|Une tasse laisse un rond.",
            "narrateur|Le rond brille sur le bois.",
            "narrateur|Sur le pompon, un éclat de pompon brille.",
            "enfant-m|Il est petit, papa.",
            "papa|C'est la laine, sous la lumière.",
            "narrateur|Papa tient la main d'Aniss.",
            "papa|Ta main est bien dans la mienne.",
            "maman|Le doudou attend sur la chaise.",
            "narrateur|Le doudou a une oreille pliée.",
            "enfant-m|Je veux parler du rouge !",
            "maman|Pendant que je prends le sac ?",
            "enfant-m|Oui, tout de suite !",
            "narrateur|En ce moment, Aniss tire la fermeture.",
            "narrateur|Le pompon rebondit contre le métal.",
            "narrateur|Papa parle à maman, près de la porte.",
            "papa|Le cartable est près du banc.",
            "maman|Oui, avec le doudou.",
            "enfant-m|Papa, le rouge !",
            "narrateur|Les mots d'Aniss se cognent aux leurs.",
            "narrateur|Personne ne tourne la tête.",
            "papa|Tu disais quelque chose, Aniss ?",
            "enfant-m|Le pompon va partir.",
            "narrateur|Aniss tire trop vite.",
            "narrateur|La fermeture se coince.",
            "narrateur|Le pompon penche, puis retombe.",
            "enfant-m|Oh.",
            "narrateur|L'éclat de pompon tremble, puis tient.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et l'inquiétude se heurtent.",
            "enfant-m|Ça ne veut pas, maman.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|Le manteau va sur tes épaules ?",
            "enfant-m|Oui, papa.",
            "narrateur|Aniss glisse un bras, puis l'autre.",
            "narrateur|La laine rêche touche le cou.",
            "papa|On y va ?",
            "enfant-m|On y va.",
            "enfant-m|Au revoir, maman.",
            "maman|Au revoir, Aniss.",
            "narrateur|Dehors, le pas sonne sous les pieds.",
            "narrateur|L'école sent le savon et le bois.",
            "narrateur|Aniss s'assoit sur le tapis.",
            "narrateur|Le tapis est doux sous les genoux.",
            "narrateur|Le pompon reste sur le manteau.",
            "narrateur|Ça sent les crayons.",
            "narrateur|Une chaise grince près du mur.",
            "narrateur|Un cube rouge est près du genou.",
            "narrateur|Aniss le pousse un peu.",
            "narrateur|La maîtresse parle près d'un ballon.",
            "maitresse|Bonjour les enfants.",
            "enfant-m|Bonjour, maîtresse.",
            "narrateur|Le ballon est rouge, un peu lisse.",
            "narrateur|Il sent le caoutchouc.",
            "enfant-m|Le ballon est rouge, comme le pompon !",
            "narrateur|Ses mots se cognent à la classe.",
            "narrateur|Personne ne comprend le rouge.",
            "narrateur|Aniss referme la bouche.",
            "narrateur|Il serre le manteau près du genou.",
            "narrateur|Le soir, la porte s'ouvre.",
            "narrateur|Ça sent le lait chaud.",
            "papa|Te voilà, Aniss.",
            "papa|Ton manteau est un peu froid.",
            "maman|Viens près de la tasse.",
            "narrateur|Aniss pose le manteau sur la chaise.",
            "narrateur|Il s'assoit.",
            "narrateur|Le ventre est serré, très petit.",
            "narrateur|Il regarde papa.",
            "narrateur|Il ouvre la bouche.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss veut parler.",
            "narrateur|Que fait-il d'abord ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "tasse,lait",
        [
            "narrateur|Aniss ouvre la bouche trop vite.",
            "enfant-m|Papa, le pompon.",
            "narrateur|Papa n'a pas fini sa phrase.",
            "papa|Le lait est chaud, Aniss.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Aniss refuse de foncer.",
            "narrateur|Sa bouche se referme.",
            "narrateur|Les mains se posent à plat.",
            "narrateur|Une main se lève, un peu.",
            "narrateur|Aniss écoute la cuisine, un instant.",
            "papa|Le manteau sèche près de la chaise.",
            "narrateur|Papa pose sa tasse.",
            "maman|Le lait fume un peu.",
            "narrateur|Maman n'a pas fini non plus.",
            "narrateur|Aniss attend que le silence arrive.",
            "narrateur|Sur le pompon, l'éclat de pompon brille.",
            "enfant-m|Il est là.",
            "enfant-m|Je peux te montrer quelque chose ?",
            "maman|Oui, nous t'écoutons.",
            "enfant-m|Le ballon était rouge.",
            "enfant-m|Comme mon pompon.",
            "papa|Merci, Aniss.",
            "narrateur|Papa a entendu toute la phrase.",
            "maman|Tu as fini ta tasse ?",
            "enfant-m|Presque, maman.",
            "narrateur|Le ventre d'Aniss se desserre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "manteau,pompon",
        [
            "narrateur|Aniss prend le manteau sur la chaise.",
            "narrateur|La laine est froide, un peu rêche.",
            "enfant-m|Je te montre le pompon.",
            "papa|Tu lui fais une place ?",
            "enfant-m|Oui.",
            "enfant-m|Ici, sur le dossier.",
            "narrateur|Aniss veut poser tout de suite.",
            "narrateur|Il jette le manteau trop vite.",
            "narrateur|Le manteau glisse du bois.",
            "narrateur|Le pompon se cache sous le col.",
            "enfant-m|Oh.",
            "narrateur|Aniss s'arrête.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Aniss refuse de foncer.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe la laine, un instant.",
            "narrateur|Il écoute le clic de la fermeture.",
            "narrateur|Il soulève le col, plus léger.",
            "narrateur|Le pompon reparaît, bien rond.",
            "enfant-m|Il est là.",
            "maman|On voit le rouge.",
            "papa|Et le doudou, à côté ?",
            "enfant-m|Il a l'oreille pliée.",
            "narrateur|Le doudou rejoint le manteau.",
            "enfant-m|Fffff.",
            "narrateur|Aniss souffle sur le pompon.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "lait,pompon",
        [
            "narrateur|Le manteau repose sur la chaise.",
            "narrateur|Le pompon reste sur la fermeture.",
            "enfant-m|Comme tout à l'heure, papa !",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur le rouge.",
            "maman|On est bien, ici.",
            "narrateur|Le lait fume un peu, près de la fenêtre.",
            "narrateur|Aniss glisse le pompon sans se presser.",
            "narrateur|La laine repose contre le métal.",
            "enfant-m|On le voit, maman.",
            "maman|Tu le vois sur le rouge ?",
            "enfant-m|Oui, l'éclat.",
            "narrateur|Le soir reste dans l'air.",
            "narrateur|L'éclat de pompon tient sur la laine.",
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
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    maitresse = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("maitresse|")
    ).lower()
    if "attendre" in maitresse or "tour" in maitresse or "merci" in maitresse:
        raise SystemExit(f"{SID}: maîtresse leçon")
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
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** COL.ECO.002 — attendre / lever la main avant de "
        "parler (vécue : veut parler maintenant ; coupe ; tire trop vite ; "
        "à l'école la phrase se perd ; refuse de foncer ; main levée ; "
        "silence ; phrase entendue)\n"
        "- **Personnages :** Aniss, papa, maman. Troupe D16. Maîtresse = "
        "label dump (bonjour près du ballon), pas de leçon récitée. "
        "Adultes parlants = papa/maman.\n"
        "- **Lieu :** entrée, classe, puis maison, pompon rouge sur la "
        "fermeture, laine rêche, cuisine au lait chaud, tasse. ≠ "
        "COL.ECO.002-01..04 (carotte, seau, carton, mousse).\n"
        "- **Indice unique :** éclat de pompon (laine au matin → tremble "
        "quand la fermeture se coince → brille au silence → tient sur "
        "la laine). Pas éclat de laine. Pas éclat de tasse.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un nuage de lait pousse jusqu'au manteau. Sur le pompon rouge, "
        "un éclat de pompon brille. Aniss veut parler du rouge "
        "**maintenant**. Il coupe papa : les mots se cognent. Il tire trop "
        "vite : la fermeture se coince, le pompon penche. Sourire parti, "
        "épaules basses. Papa se baisse. À l'école, il parle pendant la "
        "classe : le rouge se perd. Le soir, il ouvre la bouche trop vite : "
        "les voix se mélangent. Il refuse de foncer, lève la main, attend "
        "le silence, dit le ballon et le pompon. Merci vécu. Il jette le "
        "manteau trop vite : le pompon se cache sous le col. Il observe, "
        "écoute le clic, soulève. Sur la laine, l'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : entrée, fermeture, pompon rouge, laine rêche, lait "
        "chaud, tasse, doudou à l'oreille pliée, classe, ballon, maison.\n"
        "- Désir : parler du rouge **maintenant**.\n"
        "- Objet : pompon sur la fermeture, manteau, ballon, tasse, doudou.\n"
        "- Indice unique : éclat de pompon, vu dès l'ouverture, payé "
        "sur la laine.\n"
        "- Urgence douce : les mots appuient, papa n'a pas fini.\n"
        "- Imprévu 1 : il coupe, tire trop vite ; à l'école sa phrase "
        "se cogne à la classe.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après la phrase entière.\n"
        "- Imprévu 2 (plus rusé) : il jette le manteau pour montrer ; "
        "le pompon se cache sous le col.\n"
        "- Résolution : il refuse de foncer, lève la main, attend, "
        "observe, soulève le col.\n"
        "- Retour : lait qui fume, doudou à côté, éclat sur la laine.\n\n"
        "## Vécu\n\n"
        "Aniss veut parler **maintenant**. Impatience (coupe, fermeture "
        "trop vite, bouche ouverte en classe), puis sourire qui "
        "disparaît, épaules qui tombent. Papa se baisse, pose une "
        "question, ne récite pas la règle. Aniss agit : bouche fermée, "
        "mains à plat, main levée, phrase entière. Merci vécu après "
        "l'écoute. Fin : l'éclat du début tient sur la laine.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau : Le pompon d'Aniss. Lieu du dump : entrée, "
        "classe, puis maison, pompon rouge, laine rêche, lait chaud, "
        "tasse. Relance : Aniss veut parler. Que fait-il d'abord ? "
        "expected attendre.\n"
        "- Ouverture inventée (nuage de lait jusqu'au manteau), pas un "
        "gabarit v2, pas « joue au salon », pas « est dans l'entrée ».\n"
        "- Indice unique : éclat de pompon (roster). Pas carotte/seau/"
        "carton/mousse, pas éclat de laine, pas éclat de tasse, pas "
        "merle, miel, marque fine.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` "
        "retirés.\n"
        "- Leçon non dite : on l'entend quand il lève la main et attend. "
        "Pas « il faut attendre », pas « tu attends ton tour », pas "
        "« on écoute la maîtresse ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Maîtresse = label, pas de réplique de leçon.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive vers le manteau.\n"
        f"- {nwords} mots. N1 ≤ 10. `check()` OK. Pas apply.\n\n"
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
