#!/usr/bin/env python3
"""ATOM-COL.POL.001-08 — La brioche de Raphaël (F-NAR-019, N2, COL.POL.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.POL.001-08"
TITLE = "La brioche de Raphaël"
N2 = LIMITS["N2"]
CHARS = "Raphaël, papa, maman"
SETTING = (
    "rue mouillée, réverbère, pavés, boulangerie, odeur de beurre"
)
INDICE = "éclat de réverbère"
FIL = (
    "Une flaque ronde tient un cercle jaune. Sur le verre, un éclat de "
    "réverbère brille. Raphaël veut la brioche floue maintenant. Il "
    "avance trop vite, sans le mot : la boulangère ne tourne pas. Il "
    "refuse de foncer, dit bonjour. Merci vécu. Dehors, le vent gonfle "
    "le sachet comme des ailes. Il refuse, serre. Sur le verre, "
    "l'éclat de réverbère tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(croissant|farine|gouttière|gouttiere|seau|parapluie|pascal|"
    r"gaufre|zeste|citron)\b",
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
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai dit bonjour",
    "j'ai dit s'il te plaît",
    "j'ai dit s'il te plait",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "on aime écouter",
    "on aime ecouter",
    "tu as bien écouté",
    "tu as bien ecoute",
    "tu as bien fait",
    "bon travail",
    "tu as dit les mots",
    "les trois mots",
    "on dit bonjour",
    "on dit au revoir",
    "tu as suivi",
    "tu as dit merci",
    "tu as dit s'il te plaît",
    "tu as dit s'il te plait",
    "tu as dit bonjour",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de cloche",
    "éclat de corbeille",
    "éclat de sac",
    "éclat de citron",
    "éclat de manteau",
    "éclat de farine",
    "éclat de nappe",
    "éclat de croûte",
    "éclat de croute",
    "éclat de lampe",
    "point de gouttière",
    "point de gouttiere",
    "marque fine",
    "minuscule symbole",
    "ombre en forme",
    "tache de couleur",
    "grain de miette",
    "grain de sucre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de réverbère",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_brioche_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="salue",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_dit_bonjour; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="Bonjour",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_salue_puis_demande; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="sachet",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_quand_le_vent_prend_le_sachet; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de réverbère",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_verre; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "bonjour",
    "accepted_examples": (
        "bonjour | s'il te plaît | merci"
    ),
    "retry_prompt": "Il dit bonjour. Quels mots dit Raphaël ?",
    "engine_ok_text": "Oui, bonjour.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "pas,cloche",
        [
            "narrateur|Une flaque ronde tient un cercle jaune.",
            "narrateur|La rue est mouillée, un peu sombre.",
            "narrateur|Les pavés luisent sous les pas.",
            "enfant-m|Ils brillent, papa.",
            "papa|Tu les vois, sous tes pieds ?",
            "narrateur|Une odeur de beurre court sur le trottoir.",
            "enfant-m|Ça sent le beurre, maman.",
            "maman|Oui, tout le long de la rue.",
            "narrateur|Un sac en papier danse près d'une grille.",
            "narrateur|Maman rattrape le sac du bout des doigts.",
            "maman|Il voulait s'envoler.",
            "enfant-m|Il a des ailes, maman.",
            "papa|Des ailes de papier, oui.",
            "narrateur|Le ciel est bas, un peu gris.",
            "narrateur|Le réverbère jaune trempe l'eau de la rue.",
            "narrateur|Sur le verre, un éclat de réverbère brille.",
            "enfant-m|Il est blanc, papa.",
            "papa|C'est la lampe, dans l'eau.",
            "maman|Tu le touches, Raphaël ?",
            "narrateur|Raphaël pose un doigt sur le verre.",
            "narrateur|Le verre est froid, un peu mouillé.",
            "enfant-m|Il pique un peu.",
            "papa|On avance.",
            "narrateur|La boulangerie a une lampe ronde, au-dessus de la porte.",
            "narrateur|La vitre est embuée, tout en bas.",
            "narrateur|Une brioche dorée s'y dessine, un peu floue.",
            "enfant-m|Je la vois, maman.",
            "maman|Elle est derrière le verre.",
            "enfant-m|Je la veux, maintenant !",
            "papa|On pousse la porte ?",
            "enfant-m|Oui, maintenant !",
            "narrateur|En ce moment, Raphaël pose la main sur la porte.",
            "narrateur|La cloche fait ding, un peu fort.",
            "narrateur|L'air chaud touche les joues.",
            "narrateur|Ça sent la brioche et le beurre.",
            "narrateur|La boulangère range des pains ronds.",
            "enfant-m|Celle-là, maintenant !",
            "narrateur|Raphaël avance trop vite vers le comptoir.",
            "narrateur|Sa voix se mélange à la cloche.",
            "enfant-m|Oh.",
            "narrateur|La boulangère ne tourne pas la tête.",
            "narrateur|Le torchon reste dans ses mains.",
            "narrateur|La brioche reste floue, derrière le verre.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-m|Elle ne m'entend pas, papa.",
            "papa|Tu la vois, Raphaël ?",
            "narrateur|Papa se baisse à sa hauteur.",
            "narrateur|L'éclat de réverbère tremble, puis tient.",
            "narrateur|Les épaules de Raphaël tombent un peu.",
            "maman|Le sac de dehors danse, là.",
            "enfant-m|Le mien sera chaud.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Raphaël salue.",
            "narrateur|Quels mots dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "papier,cloche",
        [
            "narrateur|Raphaël avance trop vite vers le comptoir.",
            "enfant-m|La brioche, maintenant !",
            "narrateur|Sa voix se mélange à la cloche.",
            "enfant-m|Oh.",
            "narrateur|Le torchon ne bouge pas.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Raphaël refuse de foncer.",
            "narrateur|Il recule d'un pas, près du bois.",
            "papa|Tu veux venir près du bois ?",
            "narrateur|Papa reste à sa hauteur.",
            "narrateur|Raphaël écoute la cloche, un instant.",
            "narrateur|Par la vitre, l'éclat de réverbère brille.",
            "enfant-m|Bonjour.",
            "maman|Bonjour.",
            "enfant-m|Une brioche, s'il te plaît.",
            "enfant-m|Celle de la vitre.",
            "narrateur|Derrière le bois, une main se tend.",
            "narrateur|Le papier enveloppe la brioche.",
            "narrateur|Le sachet est chaud contre le manteau.",
            "enfant-m|Merci.",
            "papa|Merci, Raphaël.",
            "narrateur|Papa a entendu toute la phrase.",
            "narrateur|Le ventre de Raphaël se desserre.",
            "enfant-m|Elle est chaude, maman.",
            "maman|Tu as les mains dessus ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le papier est un peu gras, un peu tiède.",
            "enfant-m|Ça sent le beurre.",
            "maman|On sort ?",
            "enfant-m|Oui, maman.",
            "narrateur|Raphaël tient le sachet à deux mains.",
            "narrateur|Le fond du sac est tiède.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pas,papier",
        [
            "narrateur|Ils passent le pas de bois.",
            "narrateur|La cloche fait ding.",
            "narrateur|L'air mouillé revient sur les joues.",
            "narrateur|Le vent de la rue prend le sachet.",
            "narrateur|Le papier se gonfle, comme des ailes.",
            "enfant-m|Oh.",
            "narrateur|Le sac près de la grille danse, lui aussi.",
            "enfant-m|Il s'envole, papa !",
            "narrateur|Les deux voix se mélangent.",
            "papa|Le sac, Raphaël ?",
            "narrateur|Raphaël refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Il ramène le sachet contre sa poitrine.",
            "narrateur|Il écoute la rue, un instant.",
            "enfant-m|Il est chaud, papa.",
            "papa|Tu le portes jusqu'à la rue ?",
            "enfant-m|Oui, papa.",
            "maman|On marche ?",
            "enfant-m|Oui, maman.",
            "narrateur|Une goutte tombe du réverbère.",
            "narrateur|Elle fait un rond dans la flaque.",
            "enfant-m|Comme le cercle jaune.",
            "maman|Tu le vois, dans l'eau ?",
            "enfant-m|Oui, maman.",
            "narrateur|Raphaël serre le sachet contre lui.",
            "enfant-m|Elle reste chaude.",
            "papa|On rentre.",
            "narrateur|Les pavés sont froids, un peu ronds.",
            "enfant-m|Je les entends, papa.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "pas",
        [
            "narrateur|Ils s'arrêtent sous le réverbère jaune.",
            "narrateur|La flaque tient son cercle, dans l'eau.",
            "enfant-m|Le sac de la grille ne danse plus.",
            "papa|Le tien est fermé.",
            "enfant-m|Oui, papa.",
            "maman|On est bien, ici.",
            "enfant-m|Ça sent le beurre, maman.",
            "maman|Il est contre toi.",
            "narrateur|Une vapeur monte du papier.",
            "narrateur|Raphaël respire, plus large.",
            "papa|On rentre ?",
            "enfant-m|Oui.",
            "narrateur|Les joues de Raphaël se réchauffent.",
            "narrateur|Le sachet reste tiède sous la main.",
            "narrateur|L'éclat de réverbère tient sur le verre.",
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
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
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
    if "bonjour" not in blob:
        raise SystemExit(f"{SID}: manque bonjour vécu")
    if "s'il te plaît" not in blob:
        raise SystemExit(f"{SID}: manque s'il te plaît vécu")
    if "pascal" in blob:
        raise SystemExit(f"{SID}: Pascal resté")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Raphaël = enfant-m)")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    if "croissant" in blob:
        raise SystemExit(f"{SID}: croissant (001-07 / 001-10)")
    if "farine" in blob:
        raise SystemExit(f"{SID}: farine (001-01 / 001-07)")
    if "éclat de pavé" in blob or "éclat de pave" in blob:
        raise SystemExit(f"{SID}: éclat de pavé (BAN 001-01)")
    q = by["CHK_T0000_P0000_Q0001"]
    if "raphaël salue" not in q["text"].lower():
        raise SystemExit(f"{SID}: question moteur altérée")
    if "quels mots dit-il" not in q["text"].lower():
        raise SystemExit(f"{SID}: question moteur pas les mots")
    if q.get("expected_answer") != "bonjour":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if "pascal" in str(q.get("retry_prompt") or "").lower():
        raise SystemExit(f"{SID}: Pascal dans retry")
    if "raphaël" not in str(q.get("retry_prompt") or "").lower():
        raise SystemExit(f"{SID}: retry sans Raphaël")
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
        "- **Public :** N2 (4–5 ans), audio familial, ≤15 mots/phrase\n"
        "- **Leçon :** COL.POL.001 — bonjour (s'il te plaît et merci liés), "
        "vécue : veut la brioche maintenant ; première idée échoue ; "
        "refuse de foncer ; dit bonjour. Jamais dite comme règle.\n"
        "- **Personnages :** Raphaël, papa, maman. Troupe D16. Dump Pascal "
        "→ INTERDIT. `enfant-m`. Pas de maîtresse. Boulangère narrée, "
        "sans réplique. Adultes parlants = papa/maman. Papa ajouté.\n"
        "- **Lieu :** rue mouillée, réverbère, pavés, boulangerie, odeur "
        "de beurre. Pavés = détail de lieu, pas l'indice "
        "(≠ COL.POL.001-01 éclat de pavé). ≠ 001-07 (croissant, farine).\n"
        "- **Indice unique :** éclat de réverbère (verre dès l'ouverture → "
        "tremble à l'échec → brille au silence → tient sur le verre).\n"
        "- **Question moteur :** « Raphaël salue. Quels mots dit-il ? » "
        "expected **bonjour**. retry Pascal→Raphaël.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une flaque ronde tient un cercle jaune. Rue mouillée, pavés, "
        "odeur de beurre. Un sac en papier danse près d'une grille. Sur "
        "le verre, un éclat de réverbère brille. Vitre embuée, brioche "
        "dorée un peu floue. Raphaël veut la brioche **maintenant**. "
        "Première idée : avancer trop vite, sans le mot. La cloche "
        "mélange sa voix. La boulangère ne tourne pas. Sourire parti, "
        "épaules basses. Papa se baisse. Il refuse de foncer, dit "
        "bonjour, puis s'il te plaît. Le sachet arrive. Merci vécu. "
        "Dehors, le vent gonfle le papier comme des ailes. Il refuse, "
        "serre. Sous le réverbère, l'éclat tient sur le verre.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : flaque jaune, rue mouillée, pavés, odeur de beurre, "
        "sac qui danse, réverbère, vitre embuée, brioche floue, cloche. "
        "≠ 001-01 petit pain / éclat de pavé / farine. ≠ 001-07 "
        "croissant / farine-neige.\n"
        "- Désir : la brioche dorée, maintenant.\n"
        "- Objet : brioche, sachet, vitre, cloche, sac de la grille.\n"
        "- Indice unique : éclat de réverbère, vu dès l'ouverture, payé "
        "sur le verre.\n"
        "- Urgence douce : la brioche floue, la boulangère de dos.\n"
        "- Imprévu 1 : parler trop vite, sans bonjour ; la cloche et le "
        "torchon arrêtent le geste.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après la phrase "
        "entière.\n"
        "- Imprévu 2 (plus rusé) : le vent prend le sachet, ailes de "
        "papier, comme le sac de la grille.\n"
        "- Résolution : il refuse de foncer, dit bonjour, serre le "
        "sachet contre lui.\n"
        "- Retour : flaque, cercle jaune, sac de la grille arrêté, "
        "éclat de réverbère sur le verre.\n\n"
        "## Vécu\n\n"
        "Leçon COL.POL.001 (bonjour d'abord, s'il te plaît, merci) "
        "greffée, jamais annoncée. La première idée (prendre maintenant, "
        "sans le mot) échoue. Le choix de Raphaël change l'action. Un "
        "« en ce moment ». Un merci vécu. Adulte + question. Troupe "
        "D16 : Raphaël, papa, maman. N2.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : La brioche de Raphaël (noyau dump). Dump Pascal → "
        "INTERDIT. Papa ajouté.\n"
        "- Question moteur : « Raphaël salue. Quels mots dit-il ? » "
        "(fond **bonjour** conservé). retry Raphaël, pas Pascal.\n"
        "- Ouverture inventée (flaque ronde, cercle jaune), pas un "
        "gabarit v2, pas « Un réverbère jaune trempe », pas gouttière/"
        "seau de la passe 015.\n"
        "- Indice unique : éclat de réverbère. Pavés = lieu, pas indice. "
        "Pas farine, pas croissant, pas éclat de pavé/zeste/parapluie/"
        "cloche/lampe.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés.\n"
        "- Interdit « bon travail / histoire finie / tu as dit les "
        "mots / les trois mots / on dit bonjour ».\n"
        "- 5 chunks, kinds inchangés. example4 : 072, 004, 036.\n"
        f"- {nwords} mots. N2 ≤ 15. TTS : notes, ssml, xai, piper par "
        "chunk.\n\n"
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
