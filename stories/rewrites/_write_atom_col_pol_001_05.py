#!/usr/bin/env python3
"""ATOM-COL.POL.001-05 — La poire de Sarah (F-NAR-019, N1, COL.POL.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.POL.001-05"
TITLE = "La poire de Sarah"
N1 = LIMITS["N1"]
INDICE = "éclat de poire"
CHARS = "Sarah, papa, maman"
SETTING = (
    "marché, feuille jaune sur l'étal, vent, balance de fer, "
    "poires, torchon à carreaux, panier d'osier"
)
FIL = (
    "Une feuille jaune tremble sur l'étal. Sur la poire, un éclat de "
    "poire brille. Sarah veut la poire maintenant. Elle tend la main "
    "trop vite, sans le mot : le doigt tape la balance. Elle refuse "
    "de foncer, dit s'il te plaît, obtient la poire. Merci vécu. Un "
    "éclat de poire reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "louise",
    "miel",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "maîtresse",
    "maitresse",
    "voisine",
    "poirier",
    "arrosoir",
    "tomate",
    "bâche",
    "bache",
    "pavé",
    "pave",
    "zeste",
    "parapluie",
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
    "tu as dit s'il te plait",
    "tu as demandé",
    "on dit bonjour",
    "les trois mots",
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
    "éclat de seau",
    "éclat de tomate",
    "éclat de bâche",
    "éclat de bache",
)


PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de poire",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_poire_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="poire",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_dit_s_il_te_plait; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="S'il te plaît",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_balance_echoue_le_mot_ouvre; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de poire",
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
        emphasis="éclat de poire",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
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
    "retry_prompt": "Elle dit s'il te plaît. Que dit Sarah ?",
    "engine_ok_text": "Oui, s'il te plaît.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "vent,balance",
        [
            "narrateur|Une feuille jaune tremble sur l'étal.",
            "narrateur|Le vent la soulève, puis la repose.",
            "narrateur|Une balance de fer fait tic.",
            "enfant-f|Elle fait tic, papa.",
            "papa|Tu l'entends, Sarah ?",
            "narrateur|Des caisses s'alignent sous le vent.",
            "papa|Tu tiens ma manche, Sarah ?",
            "narrateur|Un torchon à carreaux couvre une caisse.",
            "narrateur|Le torchon claque un peu au vent.",
            "narrateur|Maman tient un panier d'osier.",
            "narrateur|L'osier gratte contre le manteau.",
            "enfant-f|Il pique un peu.",
            "maman|C'est l'osier, près du bras.",
            "papa|Le vent pousse la feuille.",
            "enfant-f|Elle est jaune.",
            "narrateur|Un oiseau picore sous l'étal.",
            "narrateur|Ça sent le sucré, près du nez.",
            "enfant-f|Ça sent bon, maman.",
            "maman|Ce sont les poires.",
            "narrateur|Les poires sont vertes, un côté doré.",
            "narrateur|Sur la poire, un éclat de poire brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, sur la peau ?",
            "narrateur|Sarah touche l'éclat de poire.",
            "narrateur|La peau est lisse, un peu froide.",
            "enfant-f|Elle est froide.",
            "enfant-f|Je la veux, maintenant !",
            "maman|Tu restes près de nous ?",
            "enfant-f|Oui, maman.",
            "papa|Le fer de la balance est froid.",
            "enfant-f|Il est froid, le fer.",
            "narrateur|Le vent pique un peu les joues.",
            "enfant-f|J'ai les joues froides.",
            "papa|On avance.",
            "narrateur|En ce moment, Sarah s'approche des poires.",
            "narrateur|Une poire courte attend, bien ronde.",
            "enfant-f|Celle-là !",
            "narrateur|Sarah tend la main trop vite.",
            "narrateur|Le doigt tape la balance de fer.",
            "enfant-f|Oh.",
            "narrateur|La poire reste sur l'étal.",
            "narrateur|La balance fait tic, puis se tait.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-f|Je la prends !",
            "maman|La poire est sur le bois.",
            "papa|Tu la vois, Sarah ?",
            "narrateur|Les épaules de Sarah tombent un peu.",
            "narrateur|Ça serre, dans son ventre.",
            "narrateur|Papa se baisse à sa hauteur.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Sarah veut la poire.",
            "narrateur|Que dit-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "panier,osier",
        [
            "narrateur|Sarah avance trop vite vers l'étal.",
            "enfant-f|Celle-là, maintenant !",
            "narrateur|Sa voix se mélange au vent.",
            "enfant-f|Oh.",
            "narrateur|La poire reste sur le bois.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Sarah referme la main.",
            "narrateur|Elle écoute la balance, un instant.",
            "papa|Tu veux venir près du bois ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Sarah pose un pied près de l'étal.",
            "narrateur|Le bois est lisse, un peu froid.",
            "enfant-f|Celle-là.",
            "enfant-f|S'il te plaît.",
            "narrateur|Derrière l'étal, une main se tend.",
            "narrateur|La poire glisse dans le panier.",
            "narrateur|L'osier craque contre la poire.",
            "papa|Merci, Sarah.",
            "narrateur|Papa a entendu toute la phrase.",
            "narrateur|Le ventre de Sarah se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tu as les mains au chaud ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Ça sent le sucré et le bois.",
            "enfant-f|La poire est à moi.",
            "maman|Elle est dans le panier.",
            "narrateur|Sarah pose une main sur la poire.",
            "narrateur|La peau est un peu froide.",
            "narrateur|La balance se tait.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "vent,panier",
        [
            "narrateur|Sarah tire la poire trop vite.",
            "enfant-f|Je la mange, d'un coup !",
            "narrateur|La poire glisse dans l'osier.",
            "narrateur|Elle penche vers le sol.",
            "enfant-f|Oh.",
            "narrateur|Sarah avance les mains.",
            "narrateur|Puis elle s'arrête net.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Papa attend, sans parler.",
            "narrateur|Sarah observe l'étal, écoute le vent.",
            "narrateur|Sur la peau, un éclat de poire luit.",
            "enfant-f|Là, près de la feuille.",
            "narrateur|Sarah tient la poire des deux mains.",
            "narrateur|La peau est lisse, un peu froide.",
            "enfant-f|Elle est froide, papa.",
            "papa|Tu la portes jusqu'à la rue ?",
            "enfant-f|Oui, papa.",
            "maman|On avance ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le vent reprend la feuille jaune.",
            "narrateur|La feuille s'envole vers la rue.",
            "narrateur|L'air froid revient sur les joues.",
            "narrateur|Sarah serre la poire contre elle.",
            "enfant-f|Elle reste froide.",
            "papa|On marche.",
            "narrateur|La poire penche, puis se cale.",
            "enfant-f|Je la tiens.",
            "maman|On avance.",
            "narrateur|Sarah passe le long de l'étal.",
            "narrateur|Le bois craque, un peu.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "vent",
        [
            "enfant-f|La feuille brillait, papa.",
            "papa|Tu la vois, comme sur l'étal ?",
            "enfant-f|Oui, dans le vent.",
            "narrateur|Sarah pose la poire contre le manteau.",
            "maman|On la garde au frais ?",
            "enfant-f|Oui, maman.",
            "enfant-f|L'étal sentait bon.",
            "maman|Il est derrière nous.",
            "narrateur|Une feuille jaune n'est plus là.",
            "narrateur|Sarah respire, plus large.",
            "papa|On rentre ?",
            "enfant-f|Oui.",
            "narrateur|Les joues de Sarah se réchauffent.",
            "narrateur|La poire reste froide sous la main.",
            "narrateur|Un éclat de poire reste pâle.",
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
    if "louise" in blob:
        raise SystemExit(f"{SID}: Louise interdite")
    if "bâche" in blob or "bache" in blob:
        raise SystemExit(f"{SID}: BAN bâche (001-04)")
    if "pavé" in blob or "pave" in blob:
        raise SystemExit(f"{SID}: BAN pavé")
    if "zeste" in blob:
        raise SystemExit(f"{SID}: BAN zeste")
    if "parapluie" in blob:
        raise SystemExit(f"{SID}: BAN parapluie")
    if "tomate" in blob:
        raise SystemExit(f"{SID}: BAN tomate (001-04)")
    if "tout doux" in blob:
        raise SystemExit(f"{SID}: tic tout doux")
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
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Sarah veut la poire. Que dit-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "s'il te plaît":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt", "").lower()
    if "louise" in retry:
        raise SystemExit(f"{SID}: Louise dans retry_prompt")
    if "sarah" not in retry:
        raise SystemExit(f"{SID}: retry sans Sarah")
    if "maitresse|" in blob or "maîtresse|" in blob:
        raise SystemExit(f"{SID}: maîtresse parle")

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
        "- **Public :** N1 (≤10 mots/phrase), audio familial\n"
        "- **Leçon :** COL.POL.001 — dire s'il te plaît "
        "(vécue : tendre trop vite → balance ; le mot ouvre la poire)\n"
        "- **Personnages :** Sarah, papa, maman. Louise du dump TTS "
        "retirée. Papa ajouté. Pas de maîtresse. Troupe D16.\n"
        "- **Lieu :** marché, feuille jaune sur l'étal, vent, balance de "
        "fer, torchon à carreaux, panier d'osier. ≠ 001-04 tomate / bâche.\n"
        "- **Indice unique :** éclat de poire (brille à l'ouverture, "
        "touché, luit au refus, reste pâle)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une feuille jaune tremble sur l'étal. Le vent la soulève. Une "
        "balance de fer fait tic. Sur la poire, un éclat de poire brille. "
        "Sarah veut la poire **maintenant**. Première idée : tendre la "
        "main trop vite, sans le mot. Le doigt tape la balance. Sourire "
        "parti, épaules basses. Elle refuse de foncer. Près du bois, elle "
        "dit s'il te plaît. La poire glisse dans l'osier. Merci vécu. Elle "
        "veut mordre d'un coup : la poire glisse. Elle s'arrête, lit "
        "l'éclat. Un éclat de poire reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : marché, feuille jaune, vent, balance de fer, torchon, "
        "osier, oiseau. ≠ 001-04 tomate / bâche / soleil. ≠ 001-01 pavé. "
        "≠ 001-02 zeste. ≠ 001-03 parapluie.\n"
        "- Désir : la poire courte, maintenant.\n"
        "- Objet : poire, étal, balance, panier d'osier, feuille jaune.\n"
        "- Indice unique : éclat de poire, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : les joues froides, la poire sur le bois.\n"
        "- Imprévu 1 : prendre trop vite, sans le mot ; la balance "
        "arrête le doigt.\n"
        "- Cue : papa à la même hauteur, près du bois. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : mordre d'un coup, poire qui glisse "
        "dans l'osier.\n"
        "- Résolution : elle refuse de foncer, dit s'il te plaît, tient "
        "la poire des deux mains.\n"
        "- Retour : poire froide contre le manteau, éclat de poire pâle, "
        "feuille partie dans le vent.\n\n"
        "## Vécu\n\n"
        "Sarah veut la poire **maintenant**. Impatience, puis sourire qui "
        "disparaît. Papa se baisse, pose une question, ne récite pas la "
        "règle. Sarah agit : main fermée, s'il te plaît, poire dans "
        "l'osier. Merci vécu après l'écoute. Fin : l'éclat du début "
        "reste pâle.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : La poire de Sarah (noyau dump : poire / marché). "
        "Louise → Sarah. Relance : Que dit Sarah ?\n"
        "- Lieu du dump (marché, feuille jaune, vent, balance de fer, "
        "torchon, osier). ≠ COL.POL.001-04 tomate/bâche. Pas jardin, "
        "pas poirier, pas voisine.\n"
        "- Ouverture inventée (feuille jaune qui tremble), pas un "
        "gabarit v2, pas « Sarah est au marché ».\n"
        "- Indice unique : éclat de poire. Pas bâche, pavé, zeste, "
        "parapluie. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » du dump.\n"
        "- Leçon non dite : on l'entend quand elle dit s'il te plaît, "
        "puis la poire vient. Pas de morale, pas « tu as dit les mots ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Sarah veut la poire. Que "
        "dit-elle ? ». expected s'il te plaît. retry Louise→Sarah. "
        "5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Confirm plus vif vers le panier.\n"
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
