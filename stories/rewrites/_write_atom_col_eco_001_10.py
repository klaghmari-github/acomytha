#!/usr/bin/env python3
"""ATOM-COL.ECO.001-10 — Le tapis bleu de Chouchou (F-NAR-019, N1, COL.ECO.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.001-10"
TITLE = "Le tapis bleu de Chouchou"
N1 = LIMITS["N1"]
CHARS = "Chouchou, papa, maman, maîtresse"
SETTING = (
    "école, coin tapis, puis maison. Couloir savon, chaussons bleus, "
    "radiateur, buée"
)
INDICE = "éclat de tapis"
FIL = (
    "Un tic vient du radiateur. Sur un poil, un éclat de tapis brille. "
    "Chouchou veut parler maintenant. Elle s'assoit trop vite : l'éclat "
    "se cache. Une voix trop près : malaise. Elle ouvre trop vite : les "
    "mots se perdent. Elle refuse de foncer, attend, raconte. Merci vécu. "
    "Sur le poil, l'éclat de tapis tient."
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
    "hadrien",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "on aime écouter",
    "on aime ecouter",
    "écoute la maîtresse",
    "ecoute la maitresse",
    "tu as bien écouté",
    "tu as bien ecoute",
    "tu as bien fait",
    "bon travail",
    "si tu as un malaise",
    "un chuchotement serre",
    "casserole",
    "crayon",
    "cartable",
    "moufle",
    "craie",
    "pinceau",
    "casier",
    "croûte",
    "croute",
    "wagon",
    "livre rouge",
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
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
    "grain de miette",
    "grain de sable",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de tapis",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis malaise; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_parler_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="malaise",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_raconte_quand_on_l_entend; "
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
            "destinataire=enfant; sous_texte=elle_attend_puis_on_l_entend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="genou",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_sur_le_tapis; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de tapis",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_poil; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "raconter",
    "accepted_examples": (
        "raconter | elle raconte | à papa | à la maison | "
        "écouter | elle attend | attendre | son tour | malaise"
    ),
    "retry_prompt": "Elle raconte à papa. Que fait Chouchou ?",
    "engine_ok_text": "Oui, elle raconte.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "radiateur,chaussons",
        [
            "narrateur|Un tic vient du radiateur.",
            "narrateur|La vitre est tiède, un peu floue.",
            "narrateur|Une buée ronde tient sur le verre.",
            "narrateur|Le savon du couloir pique le nez.",
            "papa|Tes chaussons bleus sont près du banc.",
            "enfant-f|Ils sont froids, papa.",
            "maman|Enfile-les, un pied puis l'autre.",
            "narrateur|Le chausson gauche colle un peu.",
            "enfant-f|Il colle, maman.",
            "maman|Tire vers toi.",
            "narrateur|Le pied droit entre, plus facile.",
            "papa|On va au coin tapis ?",
            "enfant-f|Oui, tout de suite !",
            "narrateur|Chouchou marche dans le couloir.",
            "narrateur|Les chaussons bleus font un petit choc.",
            "narrateur|Le tapis bleu attend au fond.",
            "narrateur|Les poils sont courts, un peu rèches.",
            "narrateur|Sur un poil, un éclat de tapis brille.",
            "enfant-f|Il brille, papa !",
            "papa|C'est le bleu, sous la lumière.",
            "enfant-f|Je m'assois, maintenant !",
            "maman|Pendant que je pose les sacs ?",
            "enfant-f|Oui, tout de suite !",
            "narrateur|En ce moment, Chouchou s'assoit.",
            "narrateur|Elle pose le genou trop vite.",
            "narrateur|L'éclat se cache sous le genou.",
            "enfant-f|Il est parti !",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, ça tape fort.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Tu le cherches, Chouchou ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa se baisse à sa hauteur.",
            "narrateur|Elle lève le genou, lente.",
            "narrateur|L'éclat de tapis tremble, puis tient.",
            "enfant-f|Il est là.",
            "papa|On dit bonjour ?",
            "enfant-f|Oui.",
            "narrateur|La maîtresse parle près des chaises.",
            "maitresse|Bonjour les enfants.",
            "enfant-f|Bonjour, maîtresse.",
            "narrateur|Chouchou pose les genoux sur le bleu.",
            "narrateur|Ça chatouille un peu les genoux.",
            "narrateur|Un camarade s'approche près du tapis.",
            "narrateur|Il parle près de l'oreille.",
            "narrateur|Chouchou sent un malaise dans le ventre.",
            "narrateur|Son ventre se serre, tout petit.",
            "enfant-f|Je veux le dire, maintenant.",
            "narrateur|Elle ouvre la bouche, trop vite.",
            "narrateur|Les mots se perdent dans la classe.",
            "narrateur|Personne n'entend le malaise.",
            "narrateur|Chouchou referme la bouche, un instant.",
            "narrateur|Le nœud reste dans le ventre.",
            "narrateur|Le soir, la porte s'ouvre.",
            "narrateur|Ça sent le savon de la maison.",
            "narrateur|Le radiateur fait tic, près de la vitre.",
            "narrateur|Une buée mince tient sur le verre.",
            "papa|Te voilà, Chouchou.",
            "papa|Tes chaussons bleus sont mouillés ?",
            "enfant-f|Un peu, papa.",
            "maman|Viens près de la table.",
            "narrateur|Chouchou pose les chaussons près du radiateur.",
            "narrateur|Le ventre est serré, tout petit.",
            "narrateur|Elle regarde papa, près de la table.",
            "narrateur|Elle ouvre la bouche, un peu.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Chouchou a un malaise.",
            "narrateur|Que fait-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "tasse,table",
        [
            "narrateur|Chouchou ouvre la bouche trop vite.",
            "enfant-f|Papa, l'oreille, le nœud, le tapis !",
            "narrateur|Papa n'a pas fini sa phrase.",
            "papa|Les chaussons sèchent, Chouchou.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Chouchou refuse de foncer sur les mots.",
            "narrateur|Elle referme la bouche, un instant.",
            "narrateur|Elle pose les mains à plat.",
            "narrateur|Elle écoute la maison, un instant.",
            "papa|Le radiateur fait tic, près de toi.",
            "narrateur|Papa pose sa tasse sur la table.",
            "maman|La buée tient sur la vitre.",
            "narrateur|Maman n'a pas fini non plus.",
            "narrateur|Chouchou attend que le silence arrive.",
            "narrateur|Sur le poil, l'éclat de tapis brille.",
            "enfant-f|Il est là.",
            "enfant-f|Je peux te dire quelque chose ?",
            "maman|Oui, nous t'écoutons.",
            "enfant-f|Un camarade a parlé près de mon oreille.",
            "enfant-f|Ça a serré, ici.",
            "narrateur|Chouchou montre son ventre, tout petit.",
            "papa|Merci, Chouchou.",
            "narrateur|Papa a entendu toute la phrase.",
            "maman|Tu as faim, un peu ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le ventre de Chouchou se desserre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "tapis,radiateur",
        [
            "papa|Tu t'assois, près du tapis ?",
            "enfant-f|Oui, le bleu.",
            "narrateur|Un petit tapis bleu attend près du radiateur.",
            "narrateur|Chouchou veut s'asseoir tout de suite.",
            "narrateur|Elle pose le genou trop vite.",
            "narrateur|Le tapis glisse un peu.",
            "enfant-f|Oh.",
            "narrateur|Elle veut tout dire d'un coup.",
            "enfant-f|L'école, l'oreille, le bleu !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "narrateur|Personne n'entend la fin.",
            "enfant-f|Oh.",
            "narrateur|Chouchou refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Elle écoute le radiateur, un instant.",
            "narrateur|Elle lève le genou, lente.",
            "narrateur|Un poil brille, pâle, sous le genou.",
            "enfant-f|Comme à l'école, papa.",
            "papa|Tu le vois, toi ?",
            "enfant-f|Oui, sur le bleu.",
            "narrateur|Elle s'assoit, sans presser.",
            "maman|On entend presque le couloir.",
            "enfant-f|Le savon, et les chaussons.",
            "papa|Tu restes un peu ?",
            "enfant-f|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "radiateur,vitre",
        [
            "narrateur|Les chaussons sèchent près du radiateur.",
            "narrateur|Le petit tapis bleu reste au sol.",
            "enfant-f|Comme au coin tapis, maman.",
            "maman|Tu le vois, toi ?",
            "enfant-f|Oui, sur un poil.",
            "papa|On est bien, ici.",
            "narrateur|La buée tient, mince, sur la vitre.",
            "narrateur|Chouchou glisse la main, sans se presser.",
            "enfant-f|On l'entend, papa.",
            "papa|Tu l'entends sur le bleu ?",
            "enfant-f|Oui, le tic.",
            "narrateur|Le savon reste dans l'air.",
            "narrateur|L'éclat de tapis tient sur le poil.",
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
    if "hadrien" in blob:
        raise SystemExit(f"{SID}: Hadrien resté")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Chouchou = enfant-f)")
    if "que fait-il" in blob:
        raise SystemExit(f"{SID}: Que fait-il ? (fille)")
    q = by["CHK_T0000_P0000_Q0001"]
    if q.get("retry_prompt") and "hadrien" in str(q["retry_prompt"]).lower():
        raise SystemExit(f"{SID}: Hadrien dans retry")
    if "que fait-elle" not in q["text"].lower():
        raise SystemExit(f"{SID}: question moteur pas au féminin")
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
        "- **Public :** N1 (3–4 ans), audio familial, ≤10 mots/phrase, viser ~8\n"
        "- **Leçon :** COL.ECO.001 — écouter / attendre / raconter "
        "(vécue : veut parler maintenant ; première idée échoue ; refuse "
        "de foncer ; raconte quand le silence arrive)\n"
        "- **Personnages :** Chouchou, papa, maman. Troupe D16. Maîtresse = "
        "label (bonjour près des chaises), pas de leçon récitée. Adultes "
        "parlants = papa/maman. Hadrien retiré (dump TTS → Chouchou, "
        "enfant-f).\n"
        "- **Lieu :** école, coin tapis, puis maison. Couloir savon, "
        "chaussons bleus, radiateur, buée (texture, pas l'indice). ≠ "
        "COL.ECO.001-01..09 (gouttière/crayon, rayon/buée, pain/croûte, "
        "soleil/tableau, chaussette/casier, moufle, craie, cartable, "
        "pinceau).\n"
        "- **Indice unique :** éclat de tapis (poil du coin tapis → "
        "tremble sous le genou → brille au silence → tient sur le poil "
        "du petit tapis)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un tic vient du radiateur. Vitre tiède, buée ronde, savon du "
        "couloir. Chaussons bleus. Sur un poil, un éclat de tapis brille. "
        "Chouchou veut s'asseoir **maintenant**. Elle pose le genou trop "
        "vite : l'éclat se cache. Sourire parti. Papa se baisse. À l'école, "
        "une voix trop près : malaise, ventre serré. Elle ouvre trop vite : "
        "les mots se perdent. Le soir, elle ouvre la bouche trop vite : "
        "les voix se mélangent. Elle refuse de foncer, attend le silence, "
        "raconte le malaise. Merci vécu. Elle s'assoit trop vite : le tapis "
        "glisse, les mots se bousculent. Elle refuse de foncer, écoute le "
        "tic, s'assoit sans presser. Sur le poil, l'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : couloir savon, chaussons bleus, radiateur, buée, coin "
        "tapis, puis maison. ≠ 001-01 gouttière, ≠ 001-02 éclat de buée, "
        "≠ 001-09 pinceau/casserole.\n"
        "- Désir : s'asseoir sur le bleu, dire le malaise, maintenant.\n"
        "- Objet : tapis bleu, chaussons bleus, radiateur.\n"
        "- Indice unique : éclat de tapis, vu dès l'ouverture, payé au "
        "climax (poil pendant le silence) et sur le poil au retour.\n"
        "- Urgence douce : la voix trop près, le ventre qui serre.\n"
        "- Imprévu 1 : tout de suite, genou trop vite, mots perdus en classe.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après la phrase "
        "entière près de la table.\n"
        "- Imprévu 2 (plus rusé) : à la maison, elle s'assoit trop vite ; "
        "le tapis glisse, elle veut tout dire d'un coup.\n"
        "- Résolution : elle refuse de foncer, attend le silence, dit "
        "l'oreille, reprend plus lentement.\n"
        "- Retour : chaussons près du radiateur, buée mince, l'éclat tient "
        "sur le poil.\n\n"
        "## Vécu\n\n"
        "Leçon COL.ECO.001 (dire le malaise à la maison, au bon moment) "
        "greffée, jamais annoncée. La première idée (tout dire d'un coup) "
        "échoue. Le choix de Chouchou change l'action. Un « en ce moment ». "
        "Un merci vécu. Adulte + question. Troupe D16 : Chouchou, papa, "
        "maman. Maîtresse : salut de classe, pas de leçon récitée. N1.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le tapis bleu de Chouchou (pas le livre rouge du dump).\n"
        "- Héros Chouchou, fille. Dump Hadrien → INTERDIT. `enfant-f`. "
        "Retry Hadrien→Chouchou.\n"
        "- Question moteur : « Chouchou a un malaise. Que fait-elle ? » "
        "(dump : Que fait-il ?). Fond malaise / raconter conservé.\n"
        "- Ouverture inventée (un tic vient du radiateur), pas un gabarit "
        "v2, pas « va à l'école ».\n"
        "- Indice unique : éclat de tapis. Pas crayon/buée/croûte/tableau/"
        "casier/moufle/craie/cartable/pinceau/casserole/wagon.\n"
        "- Buée = texture (radiateur, vitre), pas l'indice (001-02).\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés.\n"
        "- Interdit « bon travail / histoire finie / j'ai écouté / on aime "
        "écouter ».\n"
        "- 5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N1 ≤ 10. TTS : notes, ssml, xai, piper par "
        "chunk.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
