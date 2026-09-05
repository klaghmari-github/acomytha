#!/usr/bin/env python3
"""ATOM-DIF.PAR.002-05 — Sarah laisse le temps à Nina (F-NAR-019, N1, DIF.PAR.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.002-05"
TITLE = "Sarah laisse le temps à Nina"
N1 = LIMITS["N1"]
CHARS = "Sarah, Nina, papa, maman"
SETTING = (
    "cuisine, goûter, pomme, assiette ronde, nappe, "
    "frigo, évier, quartier, jus"
)
INDICE = "éclat d'assiette"
FIL = (
    "Ça sent la pomme près de l'évier. Sur le bord, un "
    "éclat d'assiette luit. Sarah veut aider Nina, maintenant. "
    "Elle dit le mot trop vite. Sourire parti. Papa s'accroupit. "
    "Elle ouvre la bouche, la referme, attend. Merci vécu. "
    "Deuxième ruse : le quartier glisse. Elle refuse de foncer. "
    "Un éclat d'assiette tient sur le bord."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(plateau|étal|etal|carotte|pupitre|canapé|canape|"
    r"merle|miel|maîtresse|maitresse|pépin|pepin|"
    r"bateau|cerceau|piquet|gond|flaque|grille)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "maîtresse",
    "maitresse",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "les trois mots",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "il ne faut pas rire",
    "on ne rit pas",
    "on peut attendre",
    "on peut jouer",
    "vous jouez",
    "on joue",
    "laisse le temps",
    "laissé le temps",
    "laisse le temps",
    "laisser le temps",
    "on laisse le",
    "tu as attendu",
    "j'ai attendu",
    "on attend la fin",
    "écoute jusqu'à la fin",
    "ecoute jusqu'a la fin",
    "cherche ses mots",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de plateau",
    "éclat d'étal",
    "éclat d'etal",
    "éclat de carotte",
    "éclat de pupitre",
    "éclat de canapé",
    "éclat de canape",
    "éclat de pomme",
    "éclat de nappe",
    "éclat de bol",
    "éclat de verre",
    "éclat de frigo",
    "éclat d'évier",
    "éclat d'evier",
    "éclat de quartier",
    "éclat de jus",
    "éclat de pierre",
    "éclat de cerceau",
    "éclat de flaque",
    "éclat de grille",
    "éclat de cour",
    "éclat de botte",
    "éclat de piquet",
    "éclat de gond",
    "éclat de table",
    "éclat de parquet",
    "éclat de zinc",
    "éclat de rambarde",
    "grain de pomme",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

# N1 : mêmes champs que 001-02 / 001-09 (voix lente).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat d'assiette",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_aider_maintenant; "
            "tempo=posé puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=104, speed=0.80, piper=1.36, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=780,
        sentence=360, energy="focused", contour="rising", noise=0.30,
        emphasis="mots",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=nina_cherche_ses_mots_que_fait_sarah; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=122, speed=0.88, piper=1.24, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=620,
        sentence=310, energy="bright", contour="falling", noise=0.33,
        emphasis="quartier",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_referme_la_bouche_elle_attend; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat d'assiette",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=le_quartier_glisse_elle_refuse_de_foncer; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat d'assiette",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bord; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": None,
    "accepted_examples": None,
    "retry_prompt": None,
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "",
        [
            "narrateur|Ça sent la pomme, près de l'évier.",
            "enfant-f|Ça sent bon, papa.",
            "papa|Tu le sens, le fruit froid ?",
            "enfant-f|Oui, papa.",
            "narrateur|L'eau tapote dans le fond.",
            "maman|J'ai rincé la pomme.",
            "enfant-f|Elle brille, maman.",
            "narrateur|Maman pose l'assiette ronde.",
            "narrateur|L'assiette est froide, un peu lisse.",
            "enfant-f|Elle est froide.",
            "papa|Tu la touches, Sarah ?",
            "enfant-f|Oui, du doigt.",
            "narrateur|Sur le bord, un éclat d'assiette luit.",
            "enfant-f|Il brille, maman.",
            "maman|Tu le vois, sur le bord ?",
            "enfant-f|Oui, un petit point.",
            "papa|Le soleil le touche.",
            "narrateur|Un rayon glisse sur la nappe.",
            "narrateur|La nappe gratte un peu.",
            "enfant-f|Elle gratte, papa.",
            "maman|Tu t'assois, Sarah ?",
            "enfant-f|Un peu.",
            "narrateur|Une miette dort sur la nappe.",
            "enfant-f|Une miette, maman.",
            "maman|Elle est sèche ?",
            "enfant-f|Oui.",
            "narrateur|Le frigo ronronne, tout près.",
            "enfant-f|Il ronronne, papa.",
            "papa|Tu l'entends, le frigo ?",
            "enfant-f|Oui, il ronronne.",
            "narrateur|Une goutte tombe dans l'évier.",
            "enfant-f|Ploc.",
            "maman|C'est une goutte.",
            "narrateur|Les pieds de Sarah touchent le barreau.",
            "enfant-f|Mes pieds, papa.",
            "papa|Tu es bien assise, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le bois du barreau est lisse.",
            "enfant-f|Il est lisse.",
            "narrateur|Nina arrive près de la table.",
            "narrateur|Ses chaussettes glissent sur le carreau.",
            "copine|La pomme.",
            "enfant-f|Tu viens, Nina ?",
            "copine|Oui.",
            "narrateur|Maman pose des quartiers.",
            "narrateur|Ils sont froids, un peu humides.",
            "enfant-f|Je veux aider, maintenant !",
            "papa|Tout de suite ?",
            "enfant-f|Oui, papa.",
            "narrateur|En ce moment, Sarah tend un quartier.",
            "maman|Tu le donnes à Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina prend le quartier.",
            "narrateur|Elle ouvre la bouche.",
            "copine|Po.",
            "narrateur|Sarah connaît le mot.",
            "narrateur|Elle ouvre la bouche.",
            "enfant-f|Pomme !",
            "narrateur|Nina baisse les yeux.",
            "copine|Oh.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et l'inquiétude se heurtent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Nina, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains sont froides, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat d'assiette tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nina cherche ses mots.",
            "narrateur|Que fait Sarah ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Sarah veut aider, tout de suite.",
            "enfant-f|Je dis le mot, maintenant !",
            "narrateur|Elle avance trop vite vers Nina.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copine|Attends.",
            "narrateur|Nina recule d'un pas.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le quartier, un instant.",
            "narrateur|Elle écoute le ronron du frigo.",
            "papa|Tu veux aider Nina ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Tu dis, Nina ?",
            "narrateur|Nina ne dit rien, d'abord.",
            "narrateur|Ses lèvres bougent, très lentement.",
            "copine|Pomme.",
            "enfant-f|Pomme, oui.",
            "papa|Merci, Sarah.",
            "narrateur|Papa a vu les deux, près de l'assiette.",
            "maman|Le quartier colle un peu, sous les doigts.",
            "enfant-f|Il est froid.",
            "narrateur|Nina lèche une goutte.",
            "narrateur|Sarah referme les lèvres.",
            "copine|Rouge.",
            "enfant-f|Rouge, oui.",
            "papa|Tu le vois, le quartier ?",
            "enfant-f|Oui, papa.",
            "maman|Tu croques, Nina ?",
            "copine|J'y vais.",
            "narrateur|Ils croquent la pomme.",
            "narrateur|Ça fait un petit bruit.",
            "enfant-f|Croc.",
            "copine|Croc.",
            "papa|C'est sucré, la pomme ?",
            "narrateur|Nina ouvre la bouche.",
            "copine|Su.",
            "narrateur|Sarah referme les lèvres.",
            "copine|Sucré.",
            "enfant-f|Sucré, oui.",
            "narrateur|Le ventre de Sarah se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près de l'assiette ?",
            "enfant-f|Oui.",
            "maman|Tes mains sont au frais ?",
            "enfant-f|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Maman pose le verre de jus.",
            "narrateur|Le verre est un peu flou.",
            "enfant-f|Le jus, maintenant !",
            "narrateur|Nina lève le verre.",
            "copine|Le.",
            "narrateur|Le quartier glisse sur l'assiette.",
            "enfant-f|Il glisse, maintenant !",
            "narrateur|Sarah avance les lèvres, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Sarah refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe l'assiette, un instant.",
            "narrateur|Elle écoute le ronron du frigo.",
            "narrateur|Sur le bord, un éclat d'assiette luit.",
            "enfant-f|Là, sur le bord.",
            "enfant-f|Tu dis, Nina ?",
            "narrateur|Nina ne dit rien.",
            "narrateur|Elle souffle, puis cherche.",
            "copine|Il glisse.",
            "papa|On pose le quartier ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah pousse le quartier.",
            "narrateur|Nina le pose, sans se presser.",
            "enfant-f|Il tient.",
            "copine|Il tient.",
            "papa|Le jus est froid, Nina ?",
            "copine|Un peu.",
            "maman|Tu bois, Sarah ?",
            "enfant-f|Oui, maman.",
            "narrateur|Ils boivent près de l'assiette.",
            "narrateur|La nappe chatouille les poignets.",
            "enfant-f|C'est plus facile.",
            "papa|Le frigo est calme ?",
            "enfant-f|Oui, papa.",
            "maman|Un rayon passe sur le bord.",
            "enfant-f|Il allume l'assiette.",
            "narrateur|Nina souffle sur le verre.",
            "copine|Le jus.",
            "enfant-f|Le jus, oui.",
            "narrateur|Le verre laisse un rond.",
            "enfant-f|Un rond d'eau.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de l'assiette.",
            "narrateur|Maman essuie un peu d'eau.",
            "enfant-f|La pomme a croqué, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-f|Oui, près de l'assiette.",
            "maman|On est bien, ici.",
            "narrateur|Sarah tapote le quartier du doigt.",
            "enfant-f|Il a une trace d'eau.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|Le quartier est resté, Sarah.",
            "enfant-f|Oui, avec Nina.",
            "copine|Le quartier est resté.",
            "narrateur|Ça sent la pomme, un peu tiède.",
            "enfant-f|Et le jus, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|La pomme reste dans l'assiette.",
            "narrateur|Un éclat d'assiette tient sur le bord.",
        ],
    ),
}


def vet(lines: list[str], cid: str = "") -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    skip_lesson = cid == "CHK_T0000_P0000_Q0001"
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
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        if not skip_lesson:
            for bad in EXTRA_BAD:
                if bad in low:
                    raise SystemExit(f"extra {bad}: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-f", "copine"):
            raise SystemExit(f"rôle {role}: {raw}")
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
    cid = src.get("chunk_id") or ""
    lines = vet(lines, cid)
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
    if "ouvre la bouche" not in blob:
        raise SystemExit(f"{SID}: manque ouvre la bouche")
    if "referme la bouche" not in blob:
        raise SystemExit(f"{SID}: manque referme la bouche")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Sarah = enfant-f, Nina = copine)")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Nina absente (copine)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f", "copine") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "copine" for r in roles):
        raise SystemExit(f"{SID}: copine absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "laisse le temps",
        "laissé le temps",
        "laisser le temps",
        "on laisse le",
        "on peut attendre",
        "il faut attendre",
        "cherche ses mots",
        "tu as attendu",
        "j'ai attendu",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Nina cherche ses mots. Que fait Sarah ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") is not None:
        raise SystemExit(f"{SID}: expected_answer doit rester null")
    if q.get("accepted_examples") is not None:
        raise SystemExit(f"{SID}: accepted_examples doit rester null")
    if q.get("retry_prompt") is not None:
        raise SystemExit(f"{SID}: retry_prompt doit rester null")
    copine_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    ).lower()
    if "attends" not in copine_txt:
        raise SystemExit(f"{SID}: Nina sans attends")
    if "pomme" not in blob:
        raise SystemExit(f"{SID}: manque pomme")
    if "assiette" not in blob:
        raise SystemExit(f"{SID}: manque assiette")
    if "goûter" not in blob and "gouter" not in blob:
        pass
    if "cuisine" not in blob and "évier" not in blob:
        raise SystemExit(f"{SID}: manque cuisine/évier")
    if "quartier" not in blob:
        raise SystemExit(f"{SID}: manque quartier")
    if "jus" not in blob:
        raise SystemExit(f"{SID}: manque jus")
    for ban in (
        "éclat de plateau",
        "éclat d'étal",
        "éclat de carotte",
        "éclat de pupitre",
        "grain de pomme",
        "grain de",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "pépin",
    ):
        if ban in blob:
            raise SystemExit(f"{SID}: BAN {ban}")
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
        "- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans\n"
        "- **Leçon :** DIF.PAR.002 — attendre le mot "
        "(vécue : Sarah dit « pomme » trop vite, Nina baisse les yeux, "
        "Sarah referme la bouche, Nina dit pomme puis rouge ; 2e ruse : "
        "le quartier glisse, Sarah refuse de foncer). JAMAIS dite. Pas "
        "« elle laisse le temps ». Pas « on attend la fin ».\n"
        "- **Personnages :** Sarah, Nina, papa, maman. Dump Barbara/Nina "
        "→ D16 Sarah = enfant-f (veut aider maintenant). Nina = copine "
        "(cherche, Po., Attends, souffle). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** cuisine, goûter, pomme, assiette ronde, nappe, "
        "frigo, évier, quartier, jus. ≠ 002-01 carotte. ≠ 002-02 pupitre. "
        "≠ 002-03 plateau. ≠ 002-04 étal.\n"
        "- **Indice unique :** éclat d'assiette (luit à l'ouverture → "
        "tremble au mot trop vite → luit quand le quartier glisse → "
        "tient sur le bord). BAN grain de pomme / éclat de plateau / "
        "étal / carotte / pupitre.\n"
        "- **Question moteur :** « Nina cherche ses mots. Que fait "
        "Sarah ? » expected / accepted / retry **null** (dump). Non "
        "récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Ça sent la pomme près de l'évier. Sur le bord, un éclat "
        "d'assiette luit. Goutte, frigo, nappe. Sarah veut aider "
        "**maintenant**. Nina dit Po. Sarah ouvre la bouche, dit "
        "pomme trop vite. Sourire parti. Papa s'accroupit. Elle "
        "referme la bouche, attend. Merci vécu. Deuxième ruse : le "
        "quartier glisse. Elle refuse de foncer, lit l'éclat. Un "
        "éclat d'assiette tient sur le bord.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine, goûter, pomme, assiette, nappe, frigo, "
        "évier. ≠ 002-01 carotte. ≠ 002-03 plateau. ≠ 002-04 étal.\n"
        "- Désir : aider Nina, maintenant.\n"
        "- Objet : quartier de pomme, puis verre de jus.\n"
        "- Indice unique : éclat d'assiette, vu dès l'ouverture, payé "
        "sur le bord. Pas grain de pomme / plateau / étal / carotte / "
        "pupitre.\n"
        "- Urgence douce : Nina cherche, le mot est là, tout prêt.\n"
        "- Imprévu 1 : Sarah dit pomme trop vite, Nina baisse les yeux.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« pomme, oui ».\n"
        "- Imprévu 2 (plus rusé) : jus, le quartier glisse, Sarah "
        "avance les lèvres.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le "
        "frigo, retrouve l'éclat, Nina dit « il glisse ».\n"
        "- Retour : rond d'eau, pomme dans l'assiette, éclat sur le "
        "bord.\n\n"
        "## Vécu\n\n"
        "Sarah veut aider **maintenant**. Impatience, puis mot trop "
        "vite, sourire parti. Nina prend son temps, pose sa limite "
        "(attends, souffle). Papa se baisse, pose une question, ne "
        "récite pas la règle. Elles agissent : bouche refermée, "
        "pomme dite par Nina, quartier poussé sans se presser. Merci "
        "vécu. Fin : l'éclat du début tient sur le bord.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Sarah laisse le temps à Nina (noyau « laisse le "
        "temps », prénoms D16). Relance : Que fait Sarah ? expected "
        "null.\n"
        "- Lieu du dump (cuisine, goûter, pomme). Maman et papa. "
        "Nina = copine. Sarah = héroïne. Dump Raphaël/Sarah du json "
        "remappé : Barbara→Sarah, Nina reste Nina.\n"
        "- Ouverture inventée (odeur de pomme près de l'évier), pas "
        "un gabarit v2, pas « Les pelures de pomme font une spirale » "
        "du dump.\n"
        "- Indice unique : éclat d'assiette (goûter). BAN grain de "
        "pomme / éclat de plateau (002-03) / étal (002-04) / carotte "
        "(002-01) / pupitre (002-02). Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « encore » du dump.\n"
        "- Leçon non dite : on la voit quand Sarah dit pomme trop "
        "vite, quand elle referme la bouche, quand Nina dit rouge, "
        "quand le quartier glisse. Pas « elle laisse le temps ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Nina cherche ses mots. Que fait "
        "Sarah ? ». expected/accepted/retry null. 5 chunks, kinds "
        "inchangés.\n"
        "- example4 035 / 067 / 099 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_ene_001_09.py` / "
        "`_write_atom_dif_ene_001_02.py`, profiles N1 lents.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers le quartier qui glisse.\n"
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
