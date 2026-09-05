#!/usr/bin/env python3
"""ATOM-COL.ECO.002-11 — Le chemin d'escargot de Sarah (F-NAR-019, N3, COL.ECO.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.002-11"
TITLE = "Le chemin d'escargot de Sarah"
N3 = LIMITS["N3"]
CHARS = "Sarah, papa, maman"
SETTING = "entrée au radiateur, classe, tapis, coin des livres"
INDICE = "éclat d'escargot"
FIL = (
    "Un chemin d'argent court sur la vitre. Sur le chemin, un éclat "
    "d'escargot brille. Sarah veut le dire, maintenant. Elle coupe papa : "
    "les mots se perdent. À la classe, elle ouvre la bouche trop tôt. "
    "Elle refuse de foncer, lève la main, attend, parle. Merci vécu. "
    "L'éclat d'escargot tient sur la vitre."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "francine",
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
    "j'ai su attendre",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "tu as attendu",
    "on doit demander",
    "pomme de pin",
    "filet d'escargot",
    "filet d'escargot",
    "hérisson",
    "herisson",
    "écaille",
    "ecaille",
    "coquille",
    "mouette",
    "cacao",
    "refuge",
    "boîte aux lettres",
    "boite aux lettres",
    "grain de",
    "éclat de laine",
    "éclat de mousse",
    "éclat de pin",
    "éclat de manteau",
    "éclat de pompon",
    "éclat de carotte",
    "éclat de tableau",
    "éclat de seau",
    "éclat de carton",
    "éclat de bec",
    "éclat de marche",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de crayon",
    "éclat de casserole",
    "éclat de wagon",
    "éclat de citron",
    "éclat de lampe",
    "éclat de nappe",
    "éclat de farine",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de carreau",
    "éclat de grain",
    "éclat de pince",
    "éclat de corde",
    "éclat de caisse",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de cartable",
    "éclat de bouton",
    "éclat de tasse",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "trait de craie",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat d'escargot",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_dire_le_chemin_maintenant; "
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
            "sous_texte=elle_attend_puis_parle; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="silence",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_puis_parle; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="album",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; "
            "emotion=fierté_calme; intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_l_eclat_tient; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat d'escargot",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_tient_sur_la_vitre; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "attendre",
    "accepted_examples": (
        "attendre | elle attend | lever la main | la main"
    ),
    "retry_prompt": "Elle lève la main et elle attend. Que fait Sarah ?",
    "engine_ok_text": "Oui, elle attend.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "radiateur,echarpe",
        [
            "narrateur|Un chemin d'argent court sur la vitre.",
            "narrateur|Il est mince, un peu luisant.",
            "narrateur|L'air sent le savon de maman.",
            "narrateur|L'écharpe de laine chatouille la joue de Sarah.",
            "enfant-f|Elle pique un peu, maman.",
            "maman|C'est la laine, près du cou.",
            "papa|Le radiateur de l'entrée fait tic.",
            "papa|Tu l'entends, Sarah ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Il chante, près de nous.",
            "narrateur|Sarah connaît cette entrée.",
            "narrateur|Ce chemin, lui, est nouveau.",
            "narrateur|Sur la vitre, un éclat d'escargot brille.",
            "enfant-f|Il est petit, papa.",
            "papa|C'est le soleil sur le chemin.",
            "enfant-f|Un escargot est passé !",
            "maman|Tu as vu le petit chemin luisant ?",
            "enfant-f|Il brille.",
            "enfant-f|Je veux le dire, maintenant !",
            "papa|Tes gants sont dans la poche.",
            "papa|Tu les sens ?",
            "enfant-f|Oui.",
            "enfant-f|Ils sont chauds.",
            "narrateur|Dehors, l'air est frais.",
            "narrateur|La vitre est froide sous le doigt.",
            "enfant-f|Elle est lisse, papa.",
            "narrateur|Maman tourne l'écharpe, un tour.",
            "maman|Pas trop serré.",
            "enfant-f|D'accord, maman.",
            "narrateur|Papa parle près du crochet.",
            "papa|L'écharpe, au crochet, Sarah.",
            "narrateur|Les mots de Sarah se cognent aux siens.",
            "narrateur|Personne ne tourne la tête.",
            "enfant-f|Papa, le chemin !",
            "papa|Tu disais quelque chose, Sarah ?",
            "enfant-f|Le chemin d'argent.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|L'éclat d'escargot tremble, puis tient.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-f|Ça ne sort pas, maman.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|Tu veux raconter le chemin ?",
            "enfant-f|Oui, papa.",
            "maman|Tu vas t'asseoir sur le tapis ?",
            "enfant-f|D'accord, maman.",
            "maman|Au revoir, Sarah.",
            "enfant-f|Au revoir, maman.",
            "papa|On revient te chercher.",
            "enfant-f|Au revoir, papa.",
            "narrateur|En ce moment, Sarah entre dans la classe.",
            "narrateur|La classe sent les crayons et le lait tiède.",
            "narrateur|Sarah pose l'écharpe au crochet.",
            "narrateur|Le tapis est un peu froid, sous les genoux.",
            "narrateur|Elle s'assoit près de la fenêtre.",
            "narrateur|Elle pose les mains sur ses genoux.",
            "narrateur|Le chemin d'argent reste sur la vitre.",
            "narrateur|La maîtresse parle près du tapis.",
            "narrateur|Une affiche montre un animal lent.",
            "narrateur|Sarah a une idée.",
            "narrateur|Le chemin d'escargot brille, près d'elle.",
            "enfant-f|Je veux parler du chemin.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Sarah veut parler.",
            "narrateur|Que fait-elle d'abord ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "tapis,pages",
        [
            "narrateur|Sarah ouvre la bouche trop vite.",
            "enfant-f|L'escargot a laissé un chemin !",
            "narrateur|Un camarade parle, près du tapis.",
            "copain|J'ai vu un ver de terre.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Elle lève la main, près du tapis.",
            "narrateur|Sa main reste en l'air.",
            "narrateur|Le camarade finit sa phrase.",
            "narrateur|Sarah attend que le silence arrive.",
            "narrateur|Sur la vitre, l'éclat d'escargot brille.",
            "enfant-f|Je peux dire quelque chose ?",
            "narrateur|La classe tourne un peu la tête.",
            "enfant-f|Un escargot a laissé un chemin.",
            "enfant-f|Il brille sur la vitre.",
            "narrateur|Sarah montre la vitre du doigt.",
            "enfant-f|Il est mince, comme ça.",
            "narrateur|Les genoux restent sur le tapis.",
            "narrateur|Plus tard, c'est le coin des livres.",
            "narrateur|Un banc de bois attend.",
            "narrateur|Sarah ouvre un album aux pages épaisses.",
            "narrateur|Sur une page, un escargot avance.",
            "enfant-f|Comme sur la vitre !",
            "narrateur|Sarah a envie de le dire, d'un coup.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "resolution",
        "pages,porte",
        [
            "narrateur|Sarah veut tout dire, d'un coup.",
            "narrateur|Elle tire l'album trop vite.",
            "narrateur|Les pages se collent un peu.",
            "narrateur|L'album glisse vers le banc.",
            "enfant-f|Ça tombe !",
            "narrateur|Sarah veut foncer, d'un coup.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Ses épaules se serrent un peu.",
            "narrateur|Ça tape, dans sa poitrine.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle pose l'album à plat.",
            "narrateur|Elle écoute le coin des livres.",
            "narrateur|Un autre enfant feuillette, plus loin.",
            "narrateur|Sarah attend le silence, un instant.",
            "enfant-f|Je peux dire quelque chose ?",
            "enfant-f|Il y a un escargot, dans le livre.",
            "narrateur|La page sent le papier épais.",
            "narrateur|Le soir, la porte s'ouvre.",
            "maman|Te voilà, Sarah.",
            "papa|L'écharpe sent le savon.",
            "narrateur|Sarah pose le cartable contre le mur.",
            "enfant-f|J'ai parlé du chemin.",
            "enfant-f|Après le ver de terre.",
            "papa|Merci, Sarah.",
            "narrateur|Papa a entendu toute la phrase.",
            "maman|Tu as soif ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le ventre de Sarah se desserre.",
            "papa|L'écharpe, tu la vois ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le bois du crochet tient la laine.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "radiateur,vitre",
        [
            "narrateur|Ils s'arrêtent devant la vitre.",
            "narrateur|Le chemin d'argent est plus sec.",
            "enfant-f|L'éclat est là, papa.",
            "papa|Tu le vois sur le chemin ?",
            "enfant-f|Oui, papa.",
            "maman|On est bien, ici.",
            "narrateur|Plus tard, l'écharpe sèche près du radiateur.",
            "narrateur|Ça sent le savon, un peu.",
            "enfant-f|Comme ce matin.",
            "papa|Tu souffles ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah souffle.",
            "narrateur|Le ventre est large, à sa place.",
            "enfant-f|On m'a entendue.",
            "maman|On t'a entendue, Sarah.",
            "enfant-f|Oui, maman.",
            "narrateur|Sarah pose la joue près de l'écharpe.",
            "narrateur|La laine est sèche, un peu rêche.",
            "enfant-f|C'est chaud.",
            "narrateur|Dehors, la vitre garde le chemin.",
            "narrateur|L'éclat d'escargot tient sur la vitre.",
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
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "francine" in blob:
        raise SystemExit(f"{SID}: Francine interdite")
    if "éclat de laine" in blob:
        raise SystemExit(f"{SID}: BAN éclat de laine")
    if "éclat de mousse" in blob:
        raise SystemExit(f"{SID}: BAN éclat de mousse (002-04)")
    if "filet d'escargot" in blob or "pomme de pin" in blob:
        raise SystemExit(f"{SID}: BAN filet/pomme de pin (002-04)")
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
    if qtext != "Sarah veut parler. Que fait-elle d'abord ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if "maitresse|" in blob or "maîtresse|" in blob:
        raise SystemExit(f"{SID}: maîtresse parle (label seulement)")
    if "francine" in by["CHK_T0000_P0000_Q0001"].get("retry_prompt", "").lower():
        raise SystemExit(f"{SID}: Francine dans retry_prompt")

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
        "- **Public :** N3 (5–6 ans), audio familial, ≤16 mots/phrase\n"
        "- **Leçon :** COL.ECO.002 — attendre son tour de parole "
        "(vécue : ouvrir la bouche trop vite → mots perdus ; lever la "
        "main, attendre le silence → phrase entendue)\n"
        "- **Personnages :** Sarah, papa, maman. Francine du dump TTS "
        "retirée. Papa ajouté. Maîtresse = label dump, pas de leçon "
        "récitée. Troupe D16.\n"
        "- **Lieu :** entrée au radiateur, écharpe de laine, savon, "
        "vitre, classe, tapis, coin des livres. ≠ 002-04 pomme de pin / "
        "filet d'escargot / mousse.\n"
        "- **Indice unique :** éclat d'escargot (vitre du matin → "
        "tremble à l'échec → brille au silence → tient sur la vitre)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un chemin d'argent court sur la vitre de la classe. L'air sent "
        "le savon. L'écharpe chatouille. Le radiateur fait tic. Sur le "
        "chemin, un éclat d'escargot brille. Sarah veut le dire "
        "**maintenant**. Première idée : couper papa près du crochet. "
        "Les mots se perdent. Sourire parti, épaules basses. Papa se "
        "baisse. À la classe, un camarade parle d'un ver : elle ouvre "
        "trop vite. Elle refuse de foncer, lève la main, attend, dit le "
        "chemin. Au coin des livres, l'album glisse. Elle refuse, pose, "
        "parle. Merci vécu. Sur la vitre, l'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : vitre, chemin d'argent, écharpe de laine, savon, "
        "radiateur, gants, tapis, lait tiède, crayons, album, banc.\n"
        "- Désir : dire le chemin d'escargot, maintenant.\n"
        "- Objet : chemin sur la vitre, écharpe, album aux pages "
        "épaisses.\n"
        "- Indice unique : éclat d'escargot, vu dès l'ouverture, payé "
        "à la fin.\n"
        "- Urgence douce : le mot est là, papa n'a pas fini, un camarade "
        "parle, un autre feuillette.\n"
        "- Imprévu 1 : elle coupe papa ; à la classe, elle coupe le "
        "camarade.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : tout dire en tirant l'album ; les "
        "pages collent, l'album glisse.\n"
        "- Résolution : elle refuse de foncer, lève la main, attend, "
        "parle.\n"
        "- Retour : écharpe près du radiateur, savon, l'éclat tient sur "
        "la vitre.\n\n"
        "## Vécu\n\n"
        "Sarah veut dire le chemin **maintenant**. Impatience, puis "
        "sourire qui disparaît. Un camarade parle d'un ver ; elle veut "
        "parler de l'escargot. Papa se baisse, pose une question, ne "
        "récite pas la règle. Sarah agit : bouche fermée, main levée, "
        "phrase entière. Merci vécu après l'écoute. Fin : l'éclat du "
        "début tient sur la vitre.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le chemin d'escargot de Sarah (noyau dump : chemin "
        "d'argent / escargot sur la vitre). Francine → Sarah. Relance : "
        "Que fait Sarah ?\n"
        "- Lieu du dump (entrée, radiateur, écharpe, savon, classe, "
        "tapis, coin des livres). ≠ COL.ECO.002-04 filet/pomme de pin/"
        "mousse. ≠ 002-01 carotte. ≠ 002-02 mer. ≠ 002-05 pompon. ≠ "
        "002-06 manteau/cacao.\n"
        "- Maîtresse : label dump seulement, pas de leçon récitée, pas "
        "de réplique « il faut attendre / tu as attendu ».\n"
        "- Ouverture inventée (chemin d'argent sur la vitre), pas un "
        "gabarit v2, pas « Sarah est dans l'entrée ».\n"
        "- Indice unique : éclat d'escargot. Pas éclat de laine (BAN). "
        "Pas éclat de mousse (002-04).\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés.\n"
        "- Leçon non dite : on l'entend quand elle attend, puis parle. "
        "Pas de morale, pas « on lève la main / puis on parle ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Sarah veut parler. Que fait-elle "
        "d'abord ? ». expected attendre. 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Confirm plus vif vers l'album.\n"
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
