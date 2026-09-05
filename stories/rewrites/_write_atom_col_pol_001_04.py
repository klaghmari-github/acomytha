#!/usr/bin/env python3
"""ATOM-COL.POL.001-04 — La tomate de Victorina (F-NAR-019, N1, COL.POL.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.POL.001-04"
TITLE = "La tomate de Victorina"
N1 = LIMITS["N1"]
INDICE = "éclat de bâche"
CHARS = "Victorina, papa, maman"
SETTING = (
    "marché au soleil, bâche rayée, caisses, tomates, "
    "terre et sucré, sac de toile"
)
FIL = (
    "Un claquement court. Sur la toile, un éclat de bâche luit. "
    "Victorina veut la tomate lisse maintenant. Elle tend la main "
    "trop vite, sans le mot : le marchand n'a pas les yeux. Elle refuse "
    "de foncer, dit bonjour, s'il te plaît, obtient la tomate. Merci vécu. "
    "Le sac glisse, la tomate penche. Elle refuse, tient des deux mains. "
    "Un éclat de bâche reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(pavé|pave|zeste|parapluie|pli|mie|poisson|page|escargot|"
    r"pompon|manteau|citron|lucien)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "miel",
    "merle",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "maîtresse",
    "maitresse",
    "lucien",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "trois notes",
    "une chose, puis la suivante",
    "une chose puis l'autre",
    "une étape après l'autre",
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
    "tu as dit merci",
    "tu as dit bonjour",
    "on dit bonjour",
    "on dit au revoir",
    "les trois mots",
    "tu as dit les trois",
    "tu demandes",
    "tache de couleur",
    "ombre en forme de flèche",
    "marque fine",
    "minuscule symbole",
    "grain de miette",
    "grain de laine",
    "bande bleue",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de citron",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de carotte",
    "éclat de casier",
    "éclat de laine",
    "éclat de marche",
    "éclat de nappe",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de crayon",
    "éclat de croûte",
    "éclat de croute",
    "éclat de caisse",
    "éclat de buée",
    "éclat de buee",
    "éclat de tableau",
    "éclat de moufle",
    "éclat de craie",
    "éclat de pinceau",
    "éclat de ballon",
    "éclat de tasse",
    "éclat de vitre",
    "éclat de goutte",
    "éclat de grain",
    "éclat de liste",
    "éclat de sonnette",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "trait de craie",
    "trait de vitre",
    "boulangerie",
    "gâteau",
    "gateau",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de bâche",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_tomate_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="marchand",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_dit_bonjour_au_marchand; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="bonjour",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_main_echoue_le_mot_ouvre; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de bâche",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_sans_regarder_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de bâche",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pale; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "bonjour",
    "accepted_examples": (
        "bonjour | s'il te plaît | merci | bonjour merci"
    ),
    "retry_prompt": "Elle dit bonjour. Quels mots dit Victorina ?",
    "engine_ok_text": "Oui, bonjour.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "bache,caisse",
        [
            "narrateur|Un claquement court au-dessus des caisses.",
            "narrateur|La bâche rayée se tend, puis relâche.",
            "narrateur|Sur la toile, un éclat de bâche luit.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, sur la toile ?",
            "narrateur|Victorina touche la toile, un instant.",
            "narrateur|La toile est chaude sous le doigt.",
            "enfant-f|Elle est chaude.",
            "maman|Le soleil tient sur les caisses.",
            "papa|Voilà.",
            "narrateur|Le soleil pique un peu les bras.",
            "enfant-f|J'ai les bras chauds.",
            "papa|On reste sous la bâche.",
            "maman|Tu as de l'ombre, là.",
            "enfant-f|Oui, maman.",
            "narrateur|Une odeur de terre arrive.",
            "narrateur|Elle sent le sucré aussi.",
            "enfant-f|Ça sent le jardin !",
            "maman|Tu sens, Victorina ?",
            "enfant-f|Oui.",
            "narrateur|Le sac de papa pend à l'épaule.",
            "narrateur|Le sac est en toile grise.",
            "papa|On marche près des caisses.",
            "maman|Tu restes près de nous ?",
            "enfant-f|Oui, maman.",
            "narrateur|Une mouche tourne près d'une feuille.",
            "narrateur|Une flaque tient un morceau de ciel.",
            "enfant-f|Le ciel est dans l'eau.",
            "papa|Oui.",
            "narrateur|Une balance de fer attend.",
            "narrateur|Le bois des caisses est clair.",
            "narrateur|En ce moment, Victorina s'arrête devant l'étal.",
            "narrateur|Une tomate lisse brille au bord.",
            "narrateur|Elle est ronde.",
            "narrateur|Elle est un peu tiède.",
            "enfant-f|Je la veux, maintenant.",
            "narrateur|Victorina tend la main trop vite.",
            "narrateur|Les doigts touchent le bois rêche.",
            "enfant-f|Celle-là !",
            "narrateur|Sa voix se mélange au marché.",
            "narrateur|Le marchand essuie une caisse.",
            "narrateur|Il n'a pas levé les yeux.",
            "enfant-f|Oh.",
            "narrateur|La tomate reste sur le bois.",
            "narrateur|L'éclat de bâche tremble, puis tient.",
            "narrateur|Le sourire de Victorina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-f|Je la prends !",
            "maman|La tomate est sur le bois.",
            "papa|Tu la vois, Victorina ?",
            "narrateur|Les épaules de Victorina tombent un peu.",
            "narrateur|Ça serre, dans son ventre.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|Tu parles au marchand, Victorina ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorina parle au marchand.",
            "narrateur|Quels mots dit-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "caisse,sac",
        [
            "narrateur|Victorina avance trop vite vers le bois.",
            "enfant-f|Celle-là, maintenant !",
            "narrateur|Sa voix se mélange aux caisses.",
            "enfant-f|Oh.",
            "narrateur|La tomate reste sur le bois.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Victorina referme la main.",
            "narrateur|Elle écoute la bâche, un instant.",
            "papa|Tu veux venir près du bois ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Victorina pose un pied près de la caisse.",
            "narrateur|Le bois est tiède, un peu rêche.",
            "enfant-f|Celle-là.",
            "enfant-f|Bonjour.",
            "papa|Bonjour.",
            "enfant-f|Une tomate, s'il te plaît.",
            "narrateur|Le marchand lève enfin les yeux.",
            "narrateur|Derrière le bois, une main se tend.",
            "narrateur|La tomate passe dans la paume.",
            "enfant-f|Merci.",
            "papa|Merci, Victorina.",
            "narrateur|Papa a entendu toute la phrase.",
            "narrateur|Le ventre de Victorina se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tu as les mains au chaud ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Ça sent la terre et le sucré.",
            "enfant-f|La tomate est à moi.",
            "maman|Elle est dans tes mains.",
            "narrateur|Victorina pose une main sur la tomate.",
            "narrateur|La peau est lisse, un peu tiède.",
            "papa|Tu la mets dans le sac ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa ouvre le sac de toile.",
            "narrateur|Victorina pose la tomate au fond.",
            "narrateur|Le sac sent la toile chaude.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "sac,marche",
        [
            "narrateur|Victorina tire le sac trop vite.",
            "enfant-f|Je la mange, d'un coup !",
            "narrateur|Le sac glisse entre les doigts.",
            "narrateur|La tomate penche vers le sol.",
            "enfant-f|Oh.",
            "narrateur|Victorina avance les mains.",
            "narrateur|Puis elle s'arrête net.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Papa attend, sans parler.",
            "narrateur|Personne ne parle.",
            "narrateur|Victorina refuse de foncer.",
            "narrateur|Elle observe la tomate, un instant.",
            "narrateur|Elle écoute le claquement de la bâche.",
            "narrateur|Sur la toile, un éclat de bâche luit.",
            "enfant-f|Là, près de la bâche.",
            "narrateur|Victorina tient le sac des deux mains.",
            "narrateur|La toile est rêche, un peu chaude.",
            "enfant-f|Elle est tiède, papa.",
            "papa|Tu la portes jusqu'à la rue ?",
            "enfant-f|Oui, papa.",
            "maman|On sort ?",
            "enfant-f|Oui, maman.",
            "narrateur|Ils marchent entre les étals.",
            "narrateur|Une feuille rouge colle à une chaussure.",
            "papa|On la laisse, celle-là.",
            "enfant-f|Elle n'est pas une tomate.",
            "papa|Non.",
            "maman|Juste une feuille.",
            "enfant-f|Je la tiens.",
            "maman|On avance.",
            "narrateur|Victorina serre le sac contre elle.",
            "enfant-f|Elle reste tiède.",
            "papa|On marche.",
            "narrateur|Le sac penche, puis se cale.",
            "enfant-f|Je la tiens bien.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "bache",
        [
            "enfant-f|La bâche brillait, papa.",
            "papa|Tu le vois, comme au marché ?",
            "enfant-f|Oui, sur la toile.",
            "narrateur|Victorina pose le sac contre elle.",
            "maman|On la garde au chaud ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Les tomates sentaient bon.",
            "maman|Elle est contre toi.",
            "narrateur|Une odeur de terre monte du sac.",
            "narrateur|Victorina respire, plus large.",
            "papa|On rentre ?",
            "enfant-f|Oui.",
            "narrateur|Les joues de Victorina se réchauffent.",
            "narrateur|Le sac reste tiède sous la main.",
            "enfant-f|On le voit, maman.",
            "maman|Tu le vois sur la toile ?",
            "enfant-f|Oui, l'éclat.",
            "narrateur|Un éclat de bâche reste pâle.",
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
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"extra {bad}: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-f"):
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
        raise SystemExit(f"{SID}: refuse de foncer absent")
    if re.search(r"\blucien\b", blob):
        raise SystemExit(f"{SID}: Lucien interdit")
    if re.search(r"\btom\b", blob):
        raise SystemExit(f"{SID}: Tom interdit")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Victorina = enfant-f)")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f") for r in roles):
        raise SystemExit(f"{SID}: rôle hors papa/maman")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    enfant_p0 = " ".join(
        ln.split("|", 1)[1]
        for ln in by["CHK_T0000_P0000"]["script"].splitlines()
        if ln.startswith("enfant-")
    ).lower()
    if "s'il te plaît" in enfant_p0 or "s'il te plait" in enfant_p0:
        raise SystemExit(f"{SID}: s'il te plaît déjà dans P0000")
    if re.search(r"\bbonjour\b", enfant_p0):
        raise SystemExit(f"{SID}: bonjour enfant déjà dans P0000")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Victorina parle au marchand. Quels mots dit-elle ?":
        raise SystemExit(f"{SID}: question labels changés: {q['text']}")
    if q.get("expected_answer") != "bonjour":
        raise SystemExit(f"{SID}: expected_answer ≠ bonjour")
    retry = str(q.get("retry_prompt") or "")
    if "lucien" in retry.lower():
        raise SystemExit(f"{SID}: Lucien dans retry")
    if "victorina" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans Victorina")
    if retry.lower().startswith("il dit"):
        raise SystemExit(f"{SID}: retry encore au masculin")
    c1 = by["CHK_T0000_P0000_C0001"]["script"].lower()
    if "bonjour" not in c1 or "s'il te plaît" not in c1 or "merci" not in c1:
        raise SystemExit(f"{SID}: leçon non vécue dans C0001")
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
        "- **Public :** N1 (≤10, viser ~8), audio familial\n"
        "- **Leçon :** COL.POL.001 — bonjour / s'il te plaît / merci "
        "(vécus : veut la tomate maintenant ; tend trop vite, sans le mot ; "
        "marchand sans les yeux ; refuse de foncer ; bonjour ; s'il te plaît ; "
        "merci ; le sac glisse, la tomate penche)\n"
        "- **Personnages :** Victorina, papa, maman. Troupe D16. Dump Lucien "
        "→ Victorina (INTERDIT). Maman ajoutée (dump n'avait que papa). "
        "Marchand = personne du lieu (essuie, lève les yeux, tend la tomate), "
        "pas de réplique. Adultes parlants = papa/maman. Pas de maîtresse.\n"
        "- **Lieu :** marché, bâche rayée, caisses, soleil, tomates, terre "
        "et sucré, sac de toile, balance de fer, flaque. ≠ POL.001-01 "
        "(boulangerie/pavé) ≠ POL.001-02 (gâteau/zeste) ≠ POL.001-03 "
        "(biblio/parapluie).\n"
        "- **Indice unique :** éclat de bâche (toile dès l'ouverture → "
        "tremble sans les yeux → luit au sac qui penche → reste pâle). "
        "Pas éclat de pavé / zeste / parapluie.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un claquement court au-dessus des caisses. Sur la toile, un éclat "
        "de bâche luit. Marché au soleil, terre et sucré, tomate lisse au "
        "bord. Victorina la veut **maintenant**. Première idée : tendre la "
        "main trop vite, sans le mot. Le marchand n'a pas les yeux. Sourire "
        "parti, épaules basses. Elle refuse de foncer. Près du bois, elle "
        "dit bonjour, s'il te plaît. La tomate arrive. Merci vécu. Elle "
        "veut mordre d'un coup : le sac glisse, la tomate penche. Elle "
        "s'arrête, lit l'éclat. Un éclat de bâche reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : marché, bâche rayée, caisses, soleil, tomates, terre/"
        "sucré, sac gris, mouche, flaque, balance.\n"
        "- Désir : la tomate lisse, maintenant.\n"
        "- Objet : tomate ronde tiède, sac de toile, bâche, caisse.\n"
        "- Indice unique : éclat de bâche, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : les bras chauds, la tomate au bord du bois.\n"
        "- Imprévu 1 : prendre / parler trop vite, sans le mot ; le "
        "marchand n'a pas les yeux.\n"
        "- Cue : papa à la même hauteur, près du bois. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : mordre d'un coup, sac qui glisse, "
        "tomate qui penche.\n"
        "- Résolution : elle refuse de foncer, dit bonjour, tient le sac "
        "des deux mains.\n"
        "- Retour : sac tiède contre elle, éclat de bâche pâle.\n\n"
        "## Vécu\n\n"
        "Leçon COL.POL.001 (bonjour / s'il te plaît / merci, jamais dite "
        "comme règle) greffée. La première idée (prendre maintenant, sans "
        "le mot) échoue. Le choix de Victorina change l'action. Un « en ce "
        "moment ». Un merci vécu. Adulte + question. Troupe D16 : "
        "Victorina, papa, maman. Dump Lucien → Victorina. Maman ajoutée. "
        "Pas de maîtresse. Question moteur inchangée.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : La tomate de Victorina. Lieu du dump : marché, bâche "
        "rayée, caisses, soleil, tomates, terre et sucré. Sans boulangerie, "
        "sans gâteau, sans bibliothèque.\n"
        "- Ouverture inventée (claquement au-dessus des caisses), pas un "
        "gabarit v2, pas « Une bâche rayée claque », pas pavés humides.\n"
        "- Indice unique : éclat de bâche. Pas merle-trois-notes, miel, "
        "gouttes, pas tache/flèche/marque/symbole, pas éclat de pavé/"
        "zeste/parapluie. Ban pavé, zeste, parapluie, pli, mie, poisson, "
        "page, escargot, pompon, manteau, citron.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : pas « on dit bonjour d'abord », pas « tu as "
        "dit les trois mots ». Victorina dit bonjour, la tomate vient.\n"
        "- Question moteur inchangée (Victorina parle au marchand. Quels "
        "mots dit-elle ?). expected bonjour. retry Lucien→Victorina. "
        "5 chunks, kinds inchangés.\n"
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
