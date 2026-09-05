#!/usr/bin/env python3
"""ATOM-EMO.LEX.002-03 — Sarah et le dessin mouillé (F-NAR-019, N3, EMO.LEX.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.002-03"
TITLE = "Sarah et le dessin mouillé"
N3 = LIMITS["N3"]
CHARS = "Sarah, Nina, papa, maman"
SETTING = (
    "jardin, puis porte de l'école, table, arrosoir, galet, "
    "dessin, goutte, paillasson, menthe, manteau"
)
INDICE = "éclat de paillasson"
FIL = (
    "Sarah connaît la table du jardin. Sur le paillasson, "
    "un éclat de paillasson luit. Elle veut finir le soleil "
    "pour Nina, maintenant. Une goutte tombe. Sourire parti. "
    "Poitrine serrée. Papa s'accroupit. Elle dit je suis triste. "
    "Elle demande un câlin. Merci vécu. Deuxième ruse : Nina "
    "part plus tôt, le dessin est mouillé. Elle refuse de foncer. "
    "Un éclat de paillasson tient sur le bord."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(merle|miel|treille|moule|tuteur|saladier|berge|"
    r"brouette|couverture|capuche|torchon|tabouret|gomme|"
    r"maîtresse|maitresse|grand-père|grand-pere|jardinier|"
    r"bibliothécaire|bibliothecaire|gardienne|chloé|chloe|"
    r"sac|cartable|vitre)\b",
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
    "j'ai dit",
    "j ai dit",
    "tu as nommé",
    "tu as nomme",
    "c'est de la tristesse",
    "c est de la tristesse",
    "c'est de la joie",
    "pleurer est permis",
    "le câlin aide",
    "le calin aide",
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
    "bravo. tu as",
    "tu as dit : je suis",
    "même leçon",
    "meme lecon",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de treille",
    "éclat de moule",
    "éclat de tuteur",
    "éclat de saladier",
    "éclat de gomme",
    "éclat de berge",
    "éclat de brouette",
    "éclat de couverture",
    "éclat de capuche",
    "éclat de torchon",
    "éclat de tabouret",
    "éclat de galet",
    "éclat d'arrosoir",
    "éclat de arrosoir",
    "éclat de vitre",
    "éclat de crayon",
    "éclat de sac",
    "éclat de cartable",
    "éclat de table",
    "éclat de menthe",
    "éclat de manteau",
    "éclat de porte",
    "éclat de dessin",
    "éclat de goutte",
    "toute calme",
    "tout calme",
)

# N3 : mêmes champs que LEX.001-05 / raw.js (voix N3).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de paillasson",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis tristesse; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_finir_le_soleil_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Sarah",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=sarah_est_triste_que_peut_elle_faire; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="câlin",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis soulagement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_demande_un_calin_sans_slogan; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de paillasson",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=nina_part_plus_tot_le_dessin_est_mouille; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de paillasson",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_soulagement; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bord; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "triste",
    "accepted_examples": "triste | pleurer | un câlin | câlin | demander un câlin",
    "retry_prompt": (
        "Elle peut dire je suis triste. Elle peut demander un câlin. "
        "Que fait Sarah ?"
    ),
    "engine_ok_text": "Oui, triste.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "jardin",
        [
            "narrateur|Sarah connaît la table du jardin.",
            "enfant-f|Elle est à nous, Nina.",
            "copine|Oui, Sarah.",
            "narrateur|Nina pose un galet sur le papier.",
            "enfant-f|Il tient, papa.",
            "papa|Tu le vois, le galet gris ?",
            "enfant-f|Oui, papa.",
            "narrateur|Une goutte pend au bec de l'arrosoir.",
            "copine|Elle brille, maman.",
            "maman|Tu la vois, la goutte ?",
            "copine|Oui, maman.",
            "narrateur|Ça sent la menthe, près des genoux.",
            "enfant-f|Ça sent la menthe, papa.",
            "papa|Tu la sens, la menthe tiède ?",
            "enfant-f|Oui.",
            "narrateur|Sarah connaît ce jardin, ses recoins.",
            "narrateur|Là, un coin brille autrement.",
            "narrateur|Le paillasson de la porte est un peu dur.",
            "enfant-f|Il gratte, maman.",
            "maman|Tu le sens, sous le doigt ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sur le paillasson, un éclat de paillasson luit.",
            "enfant-f|Il brille, Nina.",
            "copine|Un petit point.",
            "papa|Le soleil le touche.",
            "narrateur|Un rayon glisse sur le bord.",
            "narrateur|La table chauffe le papier.",
            "enfant-f|Il est chaud.",
            "maman|Tu dessines le soleil, Sarah ?",
            "enfant-f|Oui, un grand soleil.",
            "copine|Pour moi aussi ?",
            "enfant-f|Pour toi, Nina.",
            "narrateur|En ce moment, Sarah dessine le soleil pour Nina.",
            "enfant-f|Je finis, maintenant !",
            "papa|Tout de suite ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le jaune frotte le papier.",
            "narrateur|Un rond, puis des rayons.",
            "enfant-f|Il brille, Nina.",
            "copine|Il est rond.",
            "narrateur|Maman arrose la menthe, trop près.",
            "narrateur|Une goutte tombe sur le dessin.",
            "narrateur|Le jaune coule un peu.",
            "enfant-f|Mon soleil !",
            "copine|On souffle dessus ?",
            "narrateur|Sarah souffle trop vite, tout de suite.",
            "narrateur|Le jaune s'étale, plus large.",
            "enfant-f|Il part !",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "enfant-f|J'ai mal au ventre.",
            "narrateur|Ses yeux deviennent chauds.",
            "narrateur|Une larme tombe sur le papier.",
            "enfant-f|Je suis triste.",
            "narrateur|Sarah pleure un peu, sans crier.",
            "narrateur|Les larmes coulent sur ses joues.",
            "papa|Tu as les yeux chauds, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "maman|Tes mains sont chaudes, Sarah ?",
            "enfant-f|Un peu, maman.",
            "enfant-f|Je veux un câlin.",
            "maman|Viens.",
            "narrateur|Maman ouvre les bras.",
            "narrateur|Sarah se blottit contre maman.",
            "narrateur|Le câlin est chaud, près du cou.",
            "narrateur|Ça sent le savon de maman.",
            "narrateur|L'éclat de paillasson tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Sarah est triste.",
            "narrateur|Que peut-elle faire ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Sarah reste contre maman, un moment.",
            "enfant-f|Le soleil, maintenant.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Je le répare.",
            "narrateur|Sarah avance la main, trop vite.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le dessin, un instant.",
            "narrateur|Elle écoute le jardin, près de la table.",
            "papa|Tu restes un peu, Sarah ?",
            "enfant-f|Oui, papa.",
            "papa|Merci, Sarah.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le câlin est tiède, sous les bras.",
            "enfant-f|Il est chaud.",
            "narrateur|La poitrine de Sarah ralentit un peu.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tes joues sont mouillées, Sarah ?",
            "enfant-f|Un peu, maman.",
            "papa|On laisse le jaune, sans se presser ?",
            "enfant-f|Oui.",
            "narrateur|Maman essuie une larme du pouce.",
            "enfant-f|Ça pique les yeux.",
            "copine|Le soleil est là, un peu mouillé.",
            "enfant-f|Il est à moi.",
            "maman|Le galet tient le papier ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le ventre de Sarah se desserre.",
            "papa|On va à l'école après ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah tient le tissu de maman.",
            "enfant-f|Je reste un peu.",
            "copine|On le porte, le soleil ?",
            "enfant-f|Oui, Nina.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Près de la porte de l'école, le soir penche.",
            "narrateur|Sarah tient le dessin, un peu mouillé.",
            "enfant-f|Pour Nina, papa.",
            "papa|Tu le montres, Sarah ?",
            "enfant-f|Oui.",
            "narrateur|Nina boutonne son manteau rouge.",
            "copine|Je rentre plus tôt.",
            "enfant-f|Attends, Nina !",
            "narrateur|Sarah avance trop vite, tout de suite.",
            "narrateur|Le dessin penche, trop humide.",
            "enfant-f|Il glisse !",
            "narrateur|Le jaune n'a pas séché.",
            "narrateur|Sarah avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Sarah refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le dessin, un instant.",
            "narrateur|Elle écoute la porte, près du paillasson.",
            "narrateur|Sur le paillasson, un éclat de paillasson luit.",
            "enfant-f|Là, sur le bord.",
            "papa|On tient le papier ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina s'éloigne d'un pas, puis deux.",
            "copine|À demain, Sarah.",
            "enfant-f|À demain.",
            "narrateur|Sarah veut courir, tout de suite.",
            "narrateur|Puis elle lâche le pas.",
            "enfant-f|Je reste.",
            "maman|Tu restes près de nous, Sarah ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Je veux un câlin.",
            "maman|Viens.",
            "narrateur|Maman la serre, sans se presser.",
            "narrateur|Le câlin est chaud, près du cou.",
            "papa|Le dessin tient, Sarah ?",
            "enfant-f|Oui, un peu mouillé.",
            "maman|Le manteau de Nina part au coin.",
            "enfant-f|Je l'ai vu.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la porte.",
            "narrateur|Maman essuie un peu de jaune.",
            "enfant-f|Nina est partie, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-f|Oui, avec son manteau.",
            "maman|On est bien, ici.",
            "narrateur|Sarah tapote le papier du doigt.",
            "enfant-f|Il a une tache d'eau.",
            "maman|Tu la vois, la tache ?",
            "enfant-f|Oui, maman.",
            "papa|Le dessin est resté, Sarah.",
            "enfant-f|Oui, avec le soleil.",
            "narrateur|Ça sent la menthe, un peu tiède.",
            "enfant-f|Et le savon, maman.",
            "maman|Oui, dans l'air.",
            "papa|On reste ici, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le dessin reste contre Sarah.",
            "narrateur|Un éclat de paillasson tient sur le bord.",
        ],
    ),
}


def vet(lines: list[str], cid: str = "") -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    skip_q = cid == "CHK_T0000_P0000_Q0001"
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
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        if not skip_q:
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
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Sarah = enfant-f)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Nina = copine absente")
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
    if not any(r == "enfant-f" for r in roles):
        raise SystemExit(f"{SID}: enfant-f absente")
    if not any(r == "copine" for r in roles):
        raise SystemExit(f"{SID}: copine absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "pleurer est permis",
        "le câlin aide",
        "le calin aide",
        "c'est de la tristesse",
        "c est de la tristesse",
        "j'ai dit",
        "j ai dit",
        "tu as nommé",
        "tu as nomme",
        "l'histoire est finie",
        "même leçon",
        "meme lecon",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Sarah est triste. Que peut-elle faire ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "triste":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "triste | pleurer | un câlin | câlin | demander un câlin"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != (
        "Elle peut dire je suis triste. Elle peut demander un câlin. "
        "Que fait Sarah ?"
    ):
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    if "chloé" in retry.lower() or "chloe" in retry.lower():
        raise SystemExit(f"{SID}: retry garde Chloé")
    for c in chunks:
        if c["chunk_id"] == "CHK_T0000_P0000_Q0001":
            continue
        if c.get("expected_answer") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: expected hors Q")
        if c.get("accepted_examples") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: accepted hors Q")
        if c.get("retry_prompt") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: retry hors Q")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "je suis triste" not in opening:
        raise SystemExit(f"{SID}: nommage absent avant la question")
    if "câlin" not in opening and "calin" not in opening:
        raise SystemExit(f"{SID}: câlin absent avant la question")
    if "jardin" not in blob:
        raise SystemExit(f"{SID}: manque jardin")
    if "école" not in blob and "ecole" not in blob:
        raise SystemExit(f"{SID}: manque école")
    if "porte" not in blob:
        raise SystemExit(f"{SID}: manque porte")
    if "dessin" not in blob:
        raise SystemExit(f"{SID}: manque dessin")
    if "goutte" not in blob:
        raise SystemExit(f"{SID}: manque goutte")
    if "arrosoir" not in blob:
        raise SystemExit(f"{SID}: manque arrosoir")
    if "galet" not in blob:
        raise SystemExit(f"{SID}: manque galet")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: manque Nina")
    if "plus tôt" not in blob and "plus tot" not in blob:
        raise SystemExit(f"{SID}: manque Nina part plus tôt")
    if "mouillé" not in blob and "mouille" not in blob:
        raise SystemExit(f"{SID}: manque dessin mouillé")
    if "s'accroupit" not in opening and "s accroupit" not in opening:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    if "sourire" not in opening:
        raise SystemExit(f"{SID}: manque sourire parti")
    if "poitrine" not in opening:
        raise SystemExit(f"{SID}: manque poitrine")
    end_txt = by["CHK_T0000_P0000_END"]["text"].lower()
    if "manteau" not in end_txt:
        raise SystemExit(f"{SID}: manque manteau de Nina")
    if "paillasson" not in end_txt:
        raise SystemExit(f"{SID}: manque paillasson au climax")
    if "chloé" in blob or "chloe" in blob:
        raise SystemExit(f"{SID}: Chloé restée")
    for ban in (
        "éclat de galet",
        "éclat d'arrosoir",
        "éclat de vitre",
        "éclat de crayon",
        "éclat de gomme",
        "éclat de sac",
        "éclat de cartable",
        "éclat de treille",
        "éclat de moule",
        "éclat de tuteur",
        "éclat de saladier",
        "éclat de berge",
        "éclat de brouette",
        "éclat de couverture",
        "éclat de capuche",
        "éclat de torchon",
        "éclat de tabouret",
        "tout doux",
        "tout calme",
        "toute calme",
        "merle",
        "miel",
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
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 700 or nwords > 850:
        raise SystemExit(f"{SID}: {nwords} mots hors 700–850")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N3 (≤16 mots/phrase), audio familial, voc 5–6 ans\n"
        "- **Leçon :** EMO.LEX.002 — nommer la tristesse + demander un "
        "câlin (vécue : goutte sur le soleil, sourire parti, poitrine "
        "serrée, yeux chauds, Sarah dit je suis triste, pleure, demande "
        "un câlin, maman ouvre les bras ; 2e ruse : Nina part plus tôt, "
        "dessin mouillé, elle refuse de foncer). JAMAIS dite dans le "
        "récit. Pas « pleurer est permis ». Pas « le câlin aide ». Pas "
        "« c'est de la tristesse ». Pas « j'ai dit : je suis ».\n"
        "- **Personnages :** Sarah, Nina, papa, maman. Sarah = héros "
        "enfant-f. Nina = copine D16 (deux enfants OK). Troupe D16. "
        "Pas de maîtresse. Dump Chloé / Lila → Sarah / Nina.\n"
        "- **Lieu :** jardin, puis porte de l'école. Dump dessin / "
        "goutte / arrosoir / galet gardés. Indice PAS galet / arrosoir / "
        "vitre / crayon / gomme / sac / cartable.\n"
        "- **Indice unique :** éclat de paillasson (luit à l'ouverture → "
        "tremble aux larmes → luit à la porte de l'école → tient sur le "
        "bord). BAN éclat de galet / arrosoir / treille / moule / tuteur / "
        "saladier / gomme / berge / brouette / couverture / capuche / "
        "torchon / tabouret. Pas tache/flèche/marque/symbole.\n"
        "- **Question moteur :** « Sarah est triste. Que peut-elle "
        "faire ? » expected dump **triste**. accepted dump "
        "`triste | pleurer | un câlin | câlin | demander un câlin`. "
        "retry dump Chloé → Sarah. Non récitée dans les autres chunks. "
        "Hors Q : expected / accepted / retry nuls.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Sarah connaît la table du jardin. Galet, goutte, arrosoir, menthe. "
        "Sur le paillasson, un éclat de paillasson luit. Elle veut finir "
        "le soleil pour Nina **maintenant**. Une goutte tombe. Elle souffle "
        "trop vite. Sourire parti. Poitrine serrée. Papa s'accroupit. "
        "Je suis triste. Un câlin. Merci vécu. Deuxième ruse : à la porte "
        "de l'école, Nina part plus tôt, le dessin est mouillé. Elle "
        "s'arrête, lit l'éclat. Un éclat de paillasson tient sur le bord.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin, table, menthe, paillasson, puis porte de "
        "l'école.\n"
        "- Désir : finir le soleil pour Nina, maintenant.\n"
        "- Objet : dessin, galet, goutte, arrosoir, puis dessin mouillé.\n"
        "- Indice unique : éclat de paillasson, vu dès l'ouverture, payé "
        "sur le bord. Pas éclat de galet / arrosoir.\n"
        "- Urgence douce : elle souffle trop vite sur le jaune.\n"
        "- Imprévu 1 : goutte, jaune qui s'étale, sourire parti, larmes.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le câlin.\n"
        "- Imprévu 2 (plus rusé) : Nina part plus tôt, le dessin n'a pas "
        "séché, il glisse.\n"
        "- Résolution : elle refuse de foncer, observe, écoute la porte, "
        "retrouve l'éclat, demande un câlin.\n"
        "- Retour : tache d'eau, dessin contre Sarah, éclat sur le bord. "
        "Dénouement qui a failli : Nina part, le jaune n'a pas séché.\n\n"
        "## Vécu\n\n"
        "Sarah veut finir **maintenant**. Impatience, puis goutte, sourire "
        "parti. Elle dit je suis triste, pleure, demande un câlin. Maman "
        "ouvre les bras. Papa se baisse, pose une question, ne récite pas "
        "la règle. Ils agissent : rester sans se presser, tenir le papier "
        "mouillé, ne pas courir après Nina. Merci vécu. Fin : l'éclat du "
        "début tient sur le bord.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Sarah et le dessin mouillé (noyau dump). Relance : "
        "Que peut-elle faire ? expected triste.\n"
        "- Lieu du dump-meta (jardin, puis porte de l'école). Maman et "
        "papa. Sarah = héros enfant-f. Nina = copine. Dump dessin / "
        "goutte / arrosoir / galet.\n"
        "- Ouverture inventée (Sarah connaît la table, coin qui brille "
        "autrement), pas un gabarit v2, pas « Chloé est dans le jardin », "
        "pas « L'histoire est finie ».\n"
        "- Indice unique : éclat de paillasson ×4. BAN éclat de galet / "
        "arrosoir / vitre / crayon / gomme / sac / cartable. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme/toute calme et "
        "`aujourd'hui` retirés. Strip dump « encore humide », « tout "
        "doucement », « le câlin est chaud, encore ».\n"
        "- Leçon non dite : on la voit quand les yeux sont chauds, "
        "quand Sarah dit je suis triste, quand elle pleure, quand elle "
        "demande un câlin. Pas « pleurer est permis ». Pas « le câlin "
        "aide ». Pas « j'ai dit : je suis ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Sarah est triste. Que peut-elle faire ? ». "
        "expected triste. 5 chunks, kinds inchangés. expected/accepted "
        "dump conservés. retry Chloé → Sarah. Hors Q : null.\n"
        "- example4 063 / 095 / 027 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N3.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers Nina qui part.\n"
        f"- {nwords} mots. N3 ≤ 16. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
