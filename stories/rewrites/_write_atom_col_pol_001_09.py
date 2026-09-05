#!/usr/bin/env python3
"""ATOM-COL.POL.001-09 — Le fromage de Nina (F-NAR-019, N1, COL.POL.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.POL.001-09"
TITLE = "Le fromage de Nina"
N1 = LIMITS["N1"]
CHARS = "Nina, papa, maman"
SETTING = (
    "fromagerie, linge blanc à trous, cloche de verre, "
    "marbre froid, lait, morceau beige"
)
INDICE = "éclat de cloche"
FIL = (
    "Le verre de la cloche est froid. Sur le verre, un éclat de cloche "
    "luit. Nina veut le morceau beige maintenant. Elle tend la main trop "
    "vite, sans le mot : le verre arrête le doigt. La dame ne lève pas "
    "les yeux. Elle refuse de foncer, dit bonjour, obtient le sac. Merci "
    "vécu. Elle soulève trop vite : la cloche glisse. Un éclat de cloche "
    "reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(pavé|pave|zeste|parapluie|bâche|bache|poire|volet|"
    r"croissant|réverbère|reverbere|pli|mie|poisson|page|escargot|"
    r"pain|gâteau|gateau|tomate|brioche|gaufre|tulipe|train|"
    r"pomme|david)\b",
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
    "david",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai dit bonjour",
    "j'ai dit s'il te plaît",
    "j'ai dit s'il te plait",
    "j'ai dit merci",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "les trois mots",
    "tu as dit les mots",
    "tu te souviens des mots",
    "on dit bonjour d'abord",
    "on dit bonjour",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "tu attends ton tour",
    "tu as dit s'il te plaît",
    "tu as dit s'il te plait",
    "tu as dit merci",
    "tu as dit bonjour",
    "tu as bien fait",
    "on aime écouter",
    "on aime ecouter",
    "c'est du bon travail",
    "même leçon",
    "tu as bien fait",
    "tache de couleur",
    "ombre en forme",
    "marque fine",
    "minuscule symbole",
    "grain de",
    "grains",
    "lune d'étain",
    "lune d'etain",
    "point de gouttière",
    "point de gouttiere",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de bâche",
    "éclat de bache",
    "éclat de poire",
    "éclat de volet",
    "éclat de croissant",
    "éclat de réverbère",
    "éclat de reverbere",
    "éclat de pli",
    "éclat de mie",
    "éclat de poisson",
    "éclat de page",
    "éclat d'escargot",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de carotte",
    "éclat de tapis",
    "éclat de buée",
    "éclat de buee",
    "éclat de crayon",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de cartable",
    "éclat de pinceau",
    "éclat de casserole",
    "éclat de wagon",
    "éclat de nappe",
    "éclat de vitre",
    "éclat de tasse",
    "éclat de goutte",
    "éclat de laine",
    "éclat de grain",
    "éclat de liste",
    "éclat de sonnette",
    "éclat de marche",
    "éclat de bec",
    "éclat de fraise",
    "éclat de corbeille",
    "éclat de sac",
    "éclat de farine",
    "farine",
    "casserole",
    "radiateur",
    "moineau",
    "nappe",
    "fendu",
    "givre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de cloche",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_fromage_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="dame",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_parle_a_la_dame_avec_bonjour; "
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
            "destinataire=enfant; sous_texte=bonjour_s_il_te_plait_merci_vecus; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="cloche",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_sur_la_cloche; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de cloche",
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
        "bonjour | s'il te plaît | merci | bonjour merci | s'il vous plaît"
    ),
    "retry_prompt": "Elle dit bonjour. Que dit Nina ?",
    "engine_ok_text": "Oui, bonjour.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "cloche,porte",
        [
            "narrateur|Le verre de la cloche est froid.",
            "narrateur|Un rayon pâle y glisse.",
            "narrateur|Sur le verre, un éclat de cloche luit.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, sur le verre ?",
            "narrateur|Nina pose un doigt, un instant.",
            "narrateur|Le verre pique un peu le doigt.",
            "enfant-f|Il est froid.",
            "maman|La veste, un bouton de plus.",
            "papa|Voilà.",
            "narrateur|Un souffle frais sort de la boutique.",
            "enfant-f|J'ai les joues froides.",
            "papa|On avance.",
            "maman|Tu restes près de nous ?",
            "enfant-f|Oui, maman.",
            "narrateur|Ça sent le lait, près du verre.",
            "narrateur|Des ronds dorment sous le linge.",
            "enfant-f|Ça sent le lait !",
            "maman|Tu sens, Nina ?",
            "enfant-f|Oui.",
            "narrateur|Le linge blanc a de petits trous.",
            "narrateur|Le carrelage est froid sous les chaussures.",
            "papa|On reste près du marbre.",
            "narrateur|Le marbre du comptoir est lisse.",
            "narrateur|Le linge sent le lait, un peu.",
            "narrateur|Nina regarde par un trou du linge.",
            "enfant-f|Je vois le morceau.",
            "maman|Par un trou, Nina ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Je le veux, maintenant.",
            "narrateur|En ce moment, Nina serre la veste.",
            "narrateur|Le sol est froid sous ses chaussures.",
            "narrateur|Une feuille craque sous un morceau.",
            "enfant-f|Celui-là !",
            "narrateur|Nina se dresse sur les pointes.",
            "narrateur|Un petit morceau beige attend sous le verre.",
            "narrateur|Nina tend la main trop vite.",
            "enfant-f|Je le prends !",
            "narrateur|Le doigt tape le verre.",
            "enfant-f|Oh.",
            "narrateur|Le morceau reste sous la cloche.",
            "narrateur|La dame ne lève pas les yeux.",
            "narrateur|Le sourire de Nina disparaît.",
            "enfant-f|Il ne vient pas.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Le fromage est sous le verre.",
            "papa|Tu le vois, Nina ?",
            "narrateur|Les épaules de Nina tombent un peu.",
            "narrateur|Ça serre, dans son ventre.",
            "narrateur|L'éclat de cloche tremble, puis tient.",
            "narrateur|Papa se baisse à sa hauteur.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nina parle à la dame.",
            "narrateur|Que dit-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "papier",
        [
            "narrateur|Nina avance trop vite vers le verre.",
            "enfant-f|Celui-là, maintenant !",
            "narrateur|Sa voix se mélange près du linge.",
            "enfant-f|Oh.",
            "narrateur|Le morceau reste sous la cloche.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Nina referme la main.",
            "narrateur|Elle écoute le verre, un instant.",
            "papa|Tu veux venir près du marbre ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Nina pose un pied sur le carrelage.",
            "enfant-f|Bonjour.",
            "enfant-f|Celui-là.",
            "enfant-f|S'il te plaît.",
            "narrateur|Derrière le verre, une main se tend.",
            "narrateur|La dame glisse le morceau dans un sac.",
            "narrateur|Le papier enveloppe le fromage.",
            "narrateur|Le sac est froid contre la veste.",
            "enfant-f|Merci.",
            "papa|Merci, Nina.",
            "narrateur|Papa a entendu toute la phrase.",
            "narrateur|Le ventre de Nina se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tu as les mains au froid ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Ça sent le lait, tout près.",
            "enfant-f|Le fromage est à moi.",
            "maman|Il est dans tes mains.",
            "narrateur|Nina pose une main sur le sac.",
            "narrateur|Le papier est un peu rêche.",
            "narrateur|Le verre de la cloche se tait.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "papier,porte",
        [
            "narrateur|Nina veut soulever la cloche, d'un coup.",
            "enfant-f|Je le sens, tout près !",
            "narrateur|Elle prend le verre trop vite.",
            "narrateur|La cloche glisse sur le marbre.",
            "enfant-f|Oh.",
            "narrateur|Nina avance les mains.",
            "narrateur|Puis elle s'arrête net.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Papa attend, sans parler.",
            "narrateur|Nina observe le verre, écoute la boutique.",
            "narrateur|Sur le verre, un éclat de cloche luit.",
            "enfant-f|Là, près de la cloche.",
            "narrateur|Nina pose la cloche, sans se presser.",
            "narrateur|Le verre fait un petit toc.",
            "enfant-f|Elle reste là.",
            "papa|Tu le vois, toi ?",
            "enfant-f|Oui, sur le verre.",
            "narrateur|Nina tient le sac des deux mains.",
            "narrateur|Le papier est rêche, un peu froid.",
            "enfant-f|Il est froid, papa.",
            "papa|Tu le portes jusqu'à la porte ?",
            "enfant-f|Oui, papa.",
            "maman|On sort ?",
            "enfant-f|Oui, maman.",
            "narrateur|La porte s'ouvre.",
            "narrateur|L'air frais revient sur les joues.",
            "narrateur|Nina serre le sac contre elle.",
            "enfant-f|Il reste froid.",
            "papa|On marche.",
            "narrateur|Le sac penche, puis se cale.",
            "enfant-f|Je le tiens.",
            "maman|On avance.",
            "narrateur|Nina passe le seuil de pierre.",
            "narrateur|La pierre est froide, un peu.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "cloche",
        [
            "enfant-f|Le verre brillait, papa.",
            "papa|Tu le vois, comme dans la boutique ?",
            "enfant-f|Oui, sur la cloche.",
            "narrateur|Nina pose le sac contre la veste.",
            "maman|On le garde au froid ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Le lait sentait bon.",
            "maman|Il est contre toi.",
            "narrateur|Un souffle froid monte du papier.",
            "narrateur|Nina respire, plus large.",
            "papa|On rentre ?",
            "enfant-f|Oui.",
            "narrateur|Les joues de Nina se réchauffent.",
            "narrateur|Le sac reste froid sous la main.",
            "narrateur|Un éclat de cloche reste pâle.",
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
        if BAN_WORDS.search(low):
            raise SystemExit(f"ban: {ph}")
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
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if re.search(r"\bdavid\b", blob):
        raise SystemExit(f"{SID}: David interdit")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f") for r in roles):
        raise SystemExit(f"{SID}: rôle hors papa/maman/nina")
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
    q_text = by["CHK_T0000_P0000_Q0001"]["text"]
    if q_text != "Nina parle à la dame. Que dit-elle ?":
        raise SystemExit(f"{SID}: question labels changés: {q_text}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "bonjour":
        raise SystemExit(f"{SID}: expected_answer ≠ bonjour")
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
        "- **Leçon :** COL.POL.001 — bonjour / s'il te plaît / merci (vécus : "
        "veut le fromage maintenant ; tend trop vite ; verre ; dame sans les "
        "yeux ; refuse de foncer ; bonjour ; s'il te plaît ; merci ; la "
        "cloche glisse ; mêmes mots vécus)\n"
        "- **Personnages :** Nina, papa, maman. Troupe D16. Dump David → "
        "Nina (INTERDIT). Papa parle. La dame = label du dump (linge, verre, "
        "tend le sac), pas de réplique, pas de leçon récitée. Adultes "
        "parlants = papa/maman.\n"
        "- **Lieu :** fromagerie. Linge blanc à trous, cloche de verre, "
        "marbre, carrelage, lait, morceau beige, feuille, sac froid. ≠ "
        "POL.001-01 (pain/pavé) ≠ 02 (gâteau/zeste) ≠ 03 (trains/parapluie) "
        "≠ 04 (tomate/bâche) ≠ 05 (poire) ≠ 06 (pomme/tulipe/volet) ≠ 07 "
        "(croissant) ≠ 08 (brioche/réverbère).\n"
        "- **Indice unique :** éclat de cloche (verre dès l'ouverture → "
        "tremble au doigt → luit quand elle pose la cloche → reste pâle). "
        "Pas pavé/zeste/parapluie/bâche/poire/volet/croissant/réverbère/"
        "pli/mie/poisson/page/escargot.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le verre de la cloche est froid. Un rayon pâle y glisse. Sur le "
        "verre, un éclat de cloche luit. Lait, linge à trous, ronds, "
        "marbre. Nina veut le morceau beige **maintenant**. Première idée : "
        "tendre la main trop vite, sans le mot. Le doigt tape le verre. La "
        "dame ne lève pas les yeux. Sourire parti, épaules basses. Elle "
        "refuse de foncer. Près du marbre, elle dit bonjour, s'il te "
        "plaît. Le sac arrive. Merci vécu. Elle veut soulever la cloche "
        "d'un coup : le verre glisse. Elle s'arrête, lit l'éclat. Un éclat "
        "de cloche reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : fromagerie, cloche de verre, linge à trous, marbre, "
        "carrelage, lait, feuille, sac froid.\n"
        "- Désir : le morceau beige, maintenant.\n"
        "- Objet : fromage sous cloche, sac, verre, linge, feuille.\n"
        "- Indice unique : éclat de cloche, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : les joues froides, le fromage sous le verre.\n"
        "- Imprévu 1 : prendre / demander trop vite, sans le mot ; le "
        "verre et la dame arrêtent le geste.\n"
        "- Cue : papa à la même hauteur, près du marbre. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : soulever la cloche d'un coup ; le verre "
        "glisse sur le marbre.\n"
        "- Résolution : elle refuse de foncer, dit bonjour, tient le sac "
        "des deux mains, pose la cloche.\n"
        "- Retour : sac froid contre la veste, éclat de cloche pâle.\n\n"
        "## Vécu\n\n"
        "Nina veut le fromage **maintenant**. Impatience (main trop vite, "
        "cloche soulevée), puis sourire qui disparaît, épaules qui "
        "tombent. Papa se baisse, pose une question, ne récite pas la "
        "règle. La dame ne parle pas. Nina agit : main fermée, bonjour, "
        "s'il te plaît, merci. Merci vécu après l'écoute. Fin : l'éclat "
        "du début reste pâle.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau : Le fromage de Nina (pas Le morceau frais). Lieu "
        "du dump : fromagerie, linge blanc, cloche de verre. Relance : "
        "Nina parle à la dame. Que dit-elle ? expected bonjour. Labels Q "
        "restaurés (dump David → Nina). retry David→Nina.\n"
        "- Ouverture inventée (verre froid, rayon pâle), pas un gabarit "
        "v2, pas « joue au salon », pas le carrelage d'abord, pas « petite "
        "cloche fait ding ».\n"
        "- Indice unique : éclat de cloche (roster). Pas pavé/zeste/"
        "parapluie/bâche/poire/volet/croissant/réverbère/pli/mie/poisson/"
        "page/escargot, pas merle, miel, marque fine.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` "
        "retirés. David retiré (dump INTERDIT).\n"
        "- Leçon non dite : on l'entend quand elle dit bonjour, s'il te "
        "plaît, merci. Pas « on dit bonjour d'abord », pas « tu as dit "
        "les mots », pas « les trois mots ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. Dame = "
        "label, pas de réplique. Papa parle.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive vers la cloche.\n"
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
