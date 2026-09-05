#!/usr/bin/env python3
"""ATOM-DIF.COR.001-02 — Le carton du marché (F-NAR-019, N3, DIF.COR.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.001-02"
TITLE = "Le carton du marché"
N3 = LIMITS["N3"]
INDICE = "éclat de samare"
CHARS = "Sarah, Nino, papa, maman"
SETTING = "square sous le tilleul, carton d'oranges, banc"
FIL = (
    "Une aile sèche tape le banc. Sur l'aile, un éclat de samare "
    "brille. Sarah veut le ballon jaune dans le carton, maintenant. "
    "Nino est plus grand : il pousse trop haut, le ballon part sous "
    "le banc. Sarah refuse de foncer. Ils rapprochent le carton, "
    "visent ensemble. Merci vécu. Un éclat de samare reste pâle."
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
    "voisine",
    "fraise",
    "cerisier",
    "plaid",
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
    "tailles différentes",
    "on peut jouer ensemble",
    "vous jouez ensemble",
    "tache de couleur",
    "ombre en forme de flèche",
    "marque fine",
    "minuscule symbole",
    "grain de miette",
    "grain de laine",
    "bande bleue",
    "éclat de carton",
    "éclat de poire",
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
    "éclat de grille",
    "éclat de plaque",
    "éclat de bol",
)


PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de samare",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_ballon_dans_le_carton_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="plus petite",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=ils_jouent_ensemble_malgre_la_taille; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="carton",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_tir_haut_echoue_le_carton_rapproche_ouvre; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de samare",
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
        emphasis="éclat de samare",
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
    "expected_answer": "jouer ensemble",
    "accepted_examples": (
        "jouer ensemble | ensemble | ils jouent | inviter | le ballon"
    ),
    "retry_prompt": "Ils jouent ensemble. Que font Sarah et Nino ?",
    "engine_ok_text": "Oui, jouer ensemble.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc",
        [
            "narrateur|Une aile sèche tape le bois du banc.",
            "narrateur|Elle tourne une fois, puis s'arrête.",
            "enfant-f|Elle a tourné, papa.",
            "papa|Tu l'as vue, Sarah ?",
            "narrateur|C'est une samare, pâle et légère.",
            "narrateur|Le tilleul ombre le square.",
            "narrateur|Ça sent l'orange, près du carton.",
            "maman|C'est le carton du marché.",
            "narrateur|Papa pose le carton près du banc.",
            "narrateur|Le carton est vide, un peu froissé.",
            "enfant-f|Il sent l'orange.",
            "maman|Les oranges étaient dedans.",
            "narrateur|Un filet dort contre le pied du banc.",
            "narrateur|Dedans, un ballon jaune attend.",
            "enfant-f|Il est jaune !",
            "papa|Tu le vois, dans le filet ?",
            "narrateur|Sur l'aile, un éclat de samare brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, sur l'aile ?",
            "narrateur|Sarah touche l'éclat de samare.",
            "narrateur|L'aile est sèche, un peu froide.",
            "enfant-f|Elle est froide.",
            "enfant-f|Je veux viser le carton, maintenant !",
            "maman|Tu restes près de nous ?",
            "enfant-f|Oui, maman.",
            "papa|Tu tiens ma manche, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nino arrive près du banc.",
            "narrateur|Nino est plus grand, près du carton.",
            "narrateur|Sarah est plus petite, contre le bois.",
            "enfant-f|Tu viens viser avec moi ?",
            "narrateur|Nino regarde le carton, sans parler.",
            "enfant-m|Oui.",
            "narrateur|En ce moment, Sarah ouvre le filet.",
            "narrateur|Le ballon est un peu froid.",
            "narrateur|Il sent le caoutchouc.",
            "enfant-f|Il est froid.",
            "enfant-f|Je le mets dedans !",
            "narrateur|Sarah pousse le ballon, tout près.",
            "narrateur|Le carton fait un bruit mou.",
            "enfant-f|Il est dedans !",
            "papa|Oui.",
            "narrateur|Nino pousse plus fort, d'en haut.",
            "narrateur|Le ballon passe au-dessus du carton.",
            "narrateur|Il roule sous le banc.",
            "enfant-f|Il est parti !",
            "enfant-m|Oh.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Les épaules de Sarah tombent un peu.",
            "narrateur|Ça serre, dans son ventre.",
            "enfant-f|Je le prends !",
            "narrateur|Sarah se baisse trop vite.",
            "narrateur|Son bras cherche, sans voir.",
            "narrateur|Nino tend le bras, trop long.",
            "narrateur|Le ballon recule sous le bois.",
            "enfant-f|Je n'arrive pas.",
            "papa|Tu le vois, sous le banc ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "maman|Tes mains sont froides, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'herbe est fraîche sous les genoux.",
            "enfant-m|Il est loin.",
            "papa|On avance.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Sarah est plus petite.",
            "narrateur|Nino est plus grand.",
            "narrateur|Que font-ils ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "carton,herbe",
        [
            "narrateur|Sarah veut le ballon, toute seule.",
            "enfant-f|Je le prends, maintenant !",
            "narrateur|Elle avance trop vite sous le banc.",
            "narrateur|Le ballon glisse plus loin.",
            "enfant-f|Oh.",
            "narrateur|Nino veut pousser d'en haut.",
            "enfant-m|Je vise fort.",
            "narrateur|Sa main passe au-dessus.",
            "narrateur|Le carton tremble, vide.",
            "enfant-m|Il n'entre pas.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle referme les mains.",
            "narrateur|Elle écoute le square, un instant.",
            "papa|Tu veux venir près du carton ?",
            "narrateur|Papa reste à la même hauteur.",
            "narrateur|Sarah pose un pied dans l'herbe.",
            "narrateur|L'herbe est fraîche, un peu mouillée.",
            "enfant-f|On le rapproche ?",
            "narrateur|Nino attend, puis prend l'autre bord.",
            "enfant-m|Oui.",
            "narrateur|Sarah tire le carton, tout près.",
            "narrateur|Nino pousse l'autre bord.",
            "narrateur|Le carton glisse sur l'herbe.",
            "enfant-f|Il sent l'orange.",
            "maman|Il est près de vous.",
            "narrateur|Sarah se baisse sous le bois.",
            "narrateur|Son bras court passe sous le banc.",
            "narrateur|Nino tient le banc, plus haut.",
            "enfant-f|Je le touche !",
            "enfant-m|Doucement.",
            "narrateur|Le ballon revient, un peu poussiéreux.",
            "narrateur|Une samare est collée dessus.",
            "enfant-f|Tu tiens le bord ?",
            "enfant-m|Oui.",
            "narrateur|Sarah pousse le ballon, plus bas.",
            "narrateur|Nino le guide, sans le lancer.",
            "narrateur|Le ballon entre, avec un bruit mou.",
            "enfant-f|Il est dedans !",
            "enfant-m|Oui.",
            "papa|Merci, Sarah.",
            "narrateur|Papa a vu les deux, près du carton.",
            "narrateur|Le ventre de Sarah se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tu as les mains au chaud ?",
            "enfant-f|Un peu, maman.",
            "papa|Nino, tu tiens le bord ?",
            "enfant-m|Oui, papa.",
            "narrateur|Un pigeon marche près du filet.",
            "narrateur|Sarah souffle un peu.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "enfants_parc",
        [
            "narrateur|Sarah veut un autre but, d'un coup.",
            "enfant-f|Je recommence !",
            "narrateur|Elle tire le ballon trop vite.",
            "narrateur|Nino pousse trop haut, d'élan.",
            "narrateur|Le carton penche sur l'herbe.",
            "enfant-f|Oh.",
            "enfant-m|Il tombe !",
            "narrateur|Le ballon sort, puis roule.",
            "narrateur|Sarah avance les mains.",
            "narrateur|Puis elle s'arrête net.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Nino attend, sans parler.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Sarah observe le carton, écoute le square.",
            "narrateur|Sur l'aile, un éclat de samare luit.",
            "enfant-f|Là, sur l'aile.",
            "narrateur|Sarah tient le ballon des deux mains.",
            "enfant-f|Tu tiens le bord, Nino ?",
            "enfant-m|Oui.",
            "narrateur|Nino pose les mains sur le carton.",
            "narrateur|Sarah pousse plus bas, près de l'herbe.",
            "narrateur|Le ballon entre, sans sauter.",
            "enfant-f|Il reste dedans.",
            "papa|Tu le vois, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|On avance ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le tilleul laisse une ombre ronde.",
            "narrateur|L'air froid revient sur les joues.",
            "enfant-f|J'ai les joues froides.",
            "papa|On marche.",
            "narrateur|Sarah passe le long du banc.",
            "narrateur|Le bois craque, un peu.",
            "narrateur|Le carton a un coin froissé.",
            "enfant-f|Il a une trace.",
            "maman|Il a travaillé, le carton.",
            "enfant-m|On laisse le filet ?",
            "papa|On le prend.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "enfant-f|L'aile brillait, papa.",
            "papa|Tu la vois, comme sur le carton ?",
            "enfant-f|Oui, dans l'herbe.",
            "narrateur|Sarah pose le ballon contre le filet.",
            "maman|On le glisse dans le filet ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Le carton sentait l'orange.",
            "maman|Il est derrière nous.",
            "narrateur|Une samare n'est plus sur le bois.",
            "narrateur|Sarah respire, plus large.",
            "papa|On rentre ?",
            "enfant-f|Oui.",
            "enfant-m|À demain.",
            "enfant-f|À demain.",
            "narrateur|Les joues de Sarah se réchauffent.",
            "narrateur|Le filet est sur l'épaule de papa.",
            "narrateur|Un éclat de samare reste pâle.",
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
    if "maman|" not in blob:
        raise SystemExit(f"{SID}: maman absente")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "éclat de carton" in blob:
        raise SystemExit(f"{SID}: BAN éclat de carton")
    if "fraise" in blob or "cerisier" in blob or "plaid" in blob:
        raise SystemExit(f"{SID}: collision 001-01")
    if "tout doux" in blob or "tout calme" in blob:
        raise SystemExit(f"{SID}: tic tout doux/calme")
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
    if qtext != "Sarah est plus petite. Nino est plus grand. Que font-ils ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "jouer ensemble":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt", "").lower()
    if "sarah" not in retry or "nino" not in retry:
        raise SystemExit(f"{SID}: retry sans Sarah/Nino")
    if "jouent ensemble" not in retry:
        raise SystemExit(f"{SID}: retry sans jouent ensemble")
    if "maitresse|" in blob or "maîtresse|" in blob:
        raise SystemExit(f"{SID}: maîtresse parle")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain au lieu d'enfant-m")

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
        "- **Public :** N3 (≤16 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.COR.001 — jouer ensemble malgré la taille "
        "(vécue : Nino pousse trop haut ; Sarah trop vite sous le banc ; "
        "ils rapprochent le carton, elle passe dessous, il tient le bord)\n"
        "- **Personnages :** Sarah, Nino, papa, maman. Maman ajoutée. "
        "Nino = enfant-m (rythme lent). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** square sous le tilleul, carton d'oranges, banc, "
        "filet, ballon jaune. ≠ 001-01 bol / fraises / plaid / cerisier.\n"
        "- **Indice unique :** éclat de samare (brille à l'ouverture, "
        "touché, luit au refus, reste pâle). BAN éclat de carton.\n"
        "- **Question moteur :** « Sarah est plus petite. Nino est plus "
        "grand. Que font-ils ? » expected **jouer ensemble**.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une aile sèche tape le banc. Le tilleul ombre le square. Ça sent "
        "l'orange. Sur l'aile, un éclat de samare brille. Sarah veut le "
        "ballon dans le carton **maintenant**. Première idée : pousser "
        "seule, puis Nino d'en haut. Le ballon part sous le banc. Sourire "
        "parti, épaules basses. Elle refuse de foncer. Ils rapprochent le "
        "carton. Merci vécu. Elle veut un autre but d'un coup : le carton "
        "penche. Elle s'arrête, lit l'éclat. Un éclat de samare reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : square sous le tilleul, carton d'oranges, banc, filet, "
        "ballon jaune, herbe fraîche. ≠ 001-01 jardin / fraises / plaid.\n"
        "- Désir : le ballon jaune dans le carton, maintenant.\n"
        "- Objet : carton du marché, ballon, filet, samare, banc.\n"
        "- Indice unique : éclat de samare, vu dès l'ouverture, payé pâle. "
        "Pas éclat de carton.\n"
        "- Urgence douce : joues froides, ballon sous le bois.\n"
        "- Imprévu 1 : Nino trop haut, Sarah trop vite ; le ballon recule.\n"
        "- Cue : papa à la même hauteur, près du carton. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : autre but d'un coup, carton qui penche.\n"
        "- Résolution : elle refuse de foncer, Nino tient le bord, elle "
        "pousse plus bas.\n"
        "- Retour : filet sur l'épaule, éclat de samare pâle, orange "
        "derrière eux.\n\n"
        "## Vécu\n\n"
        "Sarah veut viser **maintenant**. Impatience, puis sourire qui "
        "disparaît. Nino prend son temps, pose sa limite (doucement, "
        "attendre). Papa se baisse, pose une question, ne récite pas la "
        "règle. Ils agissent : carton rapproché, bras court sous le banc, "
        "mains sur le bord. Merci vécu après le but. Fin : l'éclat du "
        "début reste pâle.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le carton du marché (noyau dump). Relance : Que font "
        "Sarah et Nino ?\n"
        "- Lieu du dump (square sous le tilleul, carton d'oranges, banc). "
        "Maman ajoutée. ≠ 001-01 bol de fraises.\n"
        "- Ouverture inventée (aile sèche qui tape le banc), pas un "
        "gabarit v2, pas « Sarah est au square ».\n"
        "- Indice unique : éclat de samare. BAN éclat de carton. Distinct "
        "001-01. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » du dump.\n"
        "- Leçon non dite : on la voit quand le tir haut échoue, puis "
        "quand ils tiennent le carton à deux. Pas « vous jouez ensemble ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Sarah est plus petite. Nino est "
        "plus grand. Que font-ils ? ». expected jouer ensemble. "
        "5 chunks, kinds inchangés.\n"
        "- example4 094 / 026 / 058 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_col_pol_001_05.py` (Sarah).\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Confirm plus vif vers le carton.\n"
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
