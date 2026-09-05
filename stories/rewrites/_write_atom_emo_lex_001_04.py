#!/usr/bin/env python3
"""ATOM-EMO.LEX.001-04 — Amir et le gâteau encore chaud (F-NAR-019, N1)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.001-04"
TITLE = "Amir et le gâteau encore chaud"
N1 = LIMITS["N1"]
CHARS = "Amir, papa, maman"
SETTING = (
    "cuisine, matin, gâteau, saladier, assiette, miette, "
    "carrelage, four, fenêtre, beurre, citron, table"
)
INDICE = "éclat de saladier"
FIL = (
    "Maman pose le saladier près du gâteau. Sur le verre, "
    "un éclat de saladier luit. Amir veut un bout, maintenant. "
    "Le gâteau est trop chaud. Poitrine trop vite. Sourire parti. "
    "Papa s'accroupit. Un sourire revient. Je suis content. "
    "Merci vécu. Deux petits bouts. Deuxième ruse : le bout "
    "s'effrite. Il refuse de foncer. Un éclat de saladier tient "
    "sur le verre."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(merle|miel|farine|nappe|casserole|tasse|moule|treille|"
    r"tuteur|comptoir|rouleau|étagère|etagere|torchon|tabouret|"
    r"tapis|rideau|plaid|balançoire|balancoire|plinthe|marelle|"
    r"banc|cour|grille|bac|flaque|botte|bottes|limace|perron|"
    r"tiroir|fraisier|cuivre|buis|coussin|figue|robinet|"
    r"samare|bassine|piquet|cerceau|drap|savon|bol|"
    r"lacet|sauge|chiffon|parquet|gond|portail|canapé|"
    r"canape|oiseau|toboggan|maîtresse|maitresse|flora)\b",
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
    "tu as bien fait",
    "tu as nommé",
    "tu as dit ta joie",
    "tu as dit",
    "j'ai dit : je suis",
    "j'ai dit",
    "c'est de la joie",
    "la joie est là",
    "tu as partagé",
    "bravo",
    "flora",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de treille",
    "éclat de moule",
    "éclat de tuteur",
    "éclat d'assiette",
    "éclat d assiette",
    "éclat de farine",
    "éclat de tour",
    "éclat de comptoir",
    "éclat de pot",
    "éclat de rouleau",
    "éclat de lit",
    "éclat d'étagère",
    "éclat d'etagere",
    "éclat de torchon",
    "éclat de tabouret",
    "éclat de nappe",
    "éclat de casserole",
    "éclat de tasse",
    "éclat de miette",
    "éclat de cube",
    "éclat de tapis",
    "éclat de rideau",
    "éclat de plaid",
    "éclat de bol",
    "éclat de tablier",
    "éclat de biscuit",
    "éclat de plaque",
    "éclat de couvercle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de four",
    "éclat de gâteau",
    "éclat de gateau",
    "éclat de citron",
    "éclat de beurre",
    "éclat de table",
    "éclat de carrelage",
    "éclat de fenêtre",
    "éclat de fenetre",
    "éclat de verre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat de saladier",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_un_bout_maintenant; "
            "tempo=posé puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=104, speed=0.80, piper=1.36, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=780,
        sentence=360, energy="focused", contour="rising", noise=0.30,
        emphasis="Amir",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=amir_sourit_que_dit_il; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=122, speed=0.88, piper=1.24, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=620,
        sentence=310, energy="bright", contour="falling", noise=0.33,
        emphasis="content",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_dit_content_il_partage; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de saladier",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=le_bout_s_effrite_il_s_arrete; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de saladier",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_verre; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "content",
    "accepted_examples": (
        "content | contente | je suis contente | joie | de la joie | partager"
    ),
    "retry_prompt": "Amir sent de la joie. Que dit-il ?",
    "engine_ok_text": "Oui, content.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "four",
        [
            "narrateur|Maman pose le saladier près du gâteau.",
            "enfant-m|Il est grand, maman.",
            "maman|Tu le vois, le saladier ?",
            "enfant-m|Oui, maman.",
            "narrateur|Sur le verre, un éclat de saladier luit.",
            "enfant-m|Il brille, papa.",
            "papa|Le soleil le touche ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|Papa ouvre la fenêtre d'un cran.",
            "enfant-m|L'air arrive.",
            "maman|Tu le sens, l'air ?",
            "enfant-m|Oui, maman.",
            "narrateur|La cuisine sent le beurre.",
            "enfant-m|Ça sent le citron.",
            "papa|Le citron, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le gâteau est jaune et rond.",
            "enfant-m|Il est beau !",
            "maman|Il est chaud, Amir ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Le carrelage tient la chaleur du four.",
            "enfant-m|Il est tiède, sous les pieds.",
            "papa|Tes pieds sont au chaud ?",
            "enfant-m|Oui, papa.",
            "narrateur|Une mouche tapote le carreau.",
            "enfant-m|Toc, maman.",
            "maman|Tu l'entends, Amir ?",
            "enfant-m|Oui, maman.",
            "narrateur|Une miette glisse du bord.",
            "enfant-m|Une miette !",
            "maman|Tu la vois, Amir ?",
            "enfant-m|Oui, sur la table.",
            "narrateur|Maman pose une petite assiette.",
            "enfant-m|Pour le bout ?",
            "maman|Elle attend, Amir.",
            "narrateur|Un carré de soleil pose sur le carrelage.",
            "enfant-m|Il est chaud, le carré.",
            "papa|Tu le touches, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Amir se penche tout près.",
            "enfant-m|Ça chauffe le nez.",
            "papa|Tu le sens, le gâteau ?",
            "enfant-m|Oui, il fume.",
            "narrateur|Une petite fumée monte.",
            "enfant-m|Je veux un bout, maintenant !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|En ce moment, Amir tend la main.",
            "narrateur|Ses doigts touchent le gâteau.",
            "narrateur|Le gâteau est trop chaud.",
            "enfant-m|Aïe !",
            "narrateur|Amir retire la main, trop vite.",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Sa poitrine va trop vite.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et la peur se heurtent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois le gâteau, Amir ?",
            "enfant-m|Oui, papa.",
            "maman|Tes doigts sont chauds, Amir ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de saladier tremble, puis tient.",
            "narrateur|Les joues d'Amir redeviennent chaudes.",
            "narrateur|Son ventre est léger.",
            "narrateur|Un sourire revient, tout petit.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Amir sourit.",
            "narrateur|Que dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Amir veut un bout, tout de suite.",
            "enfant-m|Je prends, maintenant !",
            "narrateur|Sa main avance, trop vite.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Amir refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le gâteau, un instant.",
            "narrateur|Il écoute la cuisine.",
            "enfant-m|Je suis content.",
            "papa|Le gâteau est là, Amir ?",
            "enfant-m|Oui, papa.",
            "enfant-m|On peut partager ?",
            "maman|On coupe deux petits bouts ?",
            "enfant-m|Oui, deux.",
            "narrateur|Maman prend la petite assiette.",
            "narrateur|Elle coupe un bout, sans se presser.",
            "papa|Tu attends, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le bout pose une miette.",
            "enfant-m|Une miette, maman.",
            "maman|Elle reste sur l'assiette ?",
            "enfant-m|Oui, maman.",
            "narrateur|Amir prend le bout, sans se presser.",
            "enfant-m|Papa, un bout ?",
            "papa|Merci, Amir.",
            "narrateur|Papa reste à la même hauteur.",
            "narrateur|Ils goûtent ensemble, tout près.",
            "enfant-m|C'est un peu citron.",
            "papa|C'est doux, Amir ?",
            "enfant-m|Oui, papa.",
            "maman|Le citron est sur les lèvres, Amir ?",
            "enfant-m|C'est doux.",
            "narrateur|Le ventre d'Amir se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près du gâteau ?",
            "enfant-m|Oui.",
            "maman|L'assiette est tiède, Amir ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Le gâteau attend sur la table.",
            "enfant-m|Il a un trou.",
            "papa|Tu le vois, le trou ?",
            "enfant-m|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Maman pousse l'assiette près du gâteau.",
            "narrateur|Elle est un peu collante.",
            "enfant-m|L'autre bout, maintenant !",
            "narrateur|Maman coupe le deuxième bout.",
            "narrateur|Le bout s'effrite sur l'assiette.",
            "enfant-m|Il tombe !",
            "narrateur|Amir avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Amir refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le gâteau, un instant.",
            "narrateur|Il écoute la cuisine, près de la table.",
            "narrateur|Sur le verre, un éclat de saladier luit.",
            "enfant-m|Là, sur le saladier.",
            "papa|On tient le bout ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le bout sent le beurre chaud.",
            "narrateur|Une miette reste au bord.",
            "narrateur|Amir pose le bout, sans se presser.",
            "enfant-m|Pour maman.",
            "maman|Le gâteau est tiède, Amir ?",
            "enfant-m|Un peu.",
            "narrateur|Maman prend le petit bout.",
            "papa|L'assiette est calme, Amir ?",
            "enfant-m|Oui, papa.",
            "maman|Un rayon passe sur le verre.",
            "enfant-m|Il allume le point.",
            "papa|Tu vois le point, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Deux petits bouts restent entre eux.",
            "enfant-m|On a partagé.",
            "papa|Le gâteau a un trou, Amir ?",
            "enfant-m|Oui, papa.",
            "maman|Tes genoux sont au chaud ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Le saladier reste près du gâteau.",
            "enfant-m|Il sent le beurre.",
            "papa|On reste ici, Amir ?",
            "enfant-m|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la table.",
            "narrateur|Maman essuie une miette.",
            "enfant-m|Le gâteau était trop chaud, papa.",
            "papa|Tu l'as senti, toi ?",
            "enfant-m|Oui, près des doigts.",
            "maman|On est bien, ici.",
            "narrateur|Amir tapote le verre du saladier.",
            "enfant-m|Il a une trace de beurre.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|Le gâteau est resté, Amir.",
            "enfant-m|Oui, avec le trou.",
            "narrateur|Ça sent le citron, un peu tiède.",
            "enfant-m|Et le beurre, maman.",
            "maman|Oui, dans l'air.",
            "papa|La cuisine est calme, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Deux petits bouts ont suffi.",
            "narrateur|Un éclat de saladier tient sur le verre.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-m"):
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
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Amir = enfant-m)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "enfant-m" for r in roles):
        raise SystemExit(f"{SID}: enfant-m absent")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "c'est de la joie",
        "j'ai dit : je suis",
        "tu as nommé",
        "tu as dit ta joie",
        "la joie est là",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Amir sourit. Que dit-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "content":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "content | contente | je suis contente | joie | de la joie | partager"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Amir sent de la joie. Que dit-il ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    if "flora" in retry.lower():
        raise SystemExit(f"{SID}: Flora restée dans retry")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "content" in opening or "joie" in opening or "partager" in opening:
        raise SystemExit(f"{SID}: content/joie/partager trop tôt")
    if "je suis content" not in by["CHK_T0000_P0000_C0001"]["script"].lower():
        raise SystemExit(f"{SID}: manque je suis content après Q")
    for cid in (
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    ):
        if by[cid].get("expected_answer") not in (None, ""):
            raise SystemExit(f"{SID}: expected hors Q sur {cid}")
        if by[cid].get("accepted_examples") not in (None, ""):
            raise SystemExit(f"{SID}: accepted hors Q sur {cid}")
        if by[cid].get("retry_prompt") not in (None, ""):
            raise SystemExit(f"{SID}: retry hors Q sur {cid}")
    if "cuisine" not in blob:
        raise SystemExit(f"{SID}: manque cuisine")
    if "gâteau" not in blob and "gateau" not in blob:
        raise SystemExit(f"{SID}: manque gâteau")
    if "assiette" not in blob:
        raise SystemExit(f"{SID}: manque assiette")
    if "miette" not in blob:
        raise SystemExit(f"{SID}: manque miette")
    if "saladier" not in blob:
        raise SystemExit(f"{SID}: manque saladier")
    if "deux petits bouts" not in blob:
        raise SystemExit(f"{SID}: manque deux petits bouts")
    if "s'effrite" not in blob and "s’effrite" not in blob:
        raise SystemExit(f"{SID}: manque bout qui s'effrite")
    if "trop chaud" not in blob:
        raise SystemExit(f"{SID}: manque gâteau trop chaud")
    for ban in (
        "éclat de treille",
        "éclat de moule",
        "éclat de tuteur",
        "éclat d'assiette",
        "éclat de farine",
        "éclat de tour",
        "éclat de nappe",
        "éclat de casserole",
        "éclat de tasse",
        "éclat de miette",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "flora",
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
    if not (700 <= nwords <= 850):
        raise SystemExit(f"{SID}: mots {nwords} hors 700–850")

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans\n"
        "- **Leçon :** EMO.LEX.001 — nommer la joie + partager "
        "(vécue : gâteau trop chaud, poitrine trop vite, sourire parti, "
        "papa accroupi, un sourire revient, Amir dit je suis content, "
        "deux petits bouts ; 2e ruse : le bout s'effrite, il refuse de "
        "foncer). JAMAIS dite dans le récit. Pas « c'est de la joie ». "
        "Pas « j'ai dit : je suis ». Pas « tu as nommé ».\n"
        "- **Personnages :** Amir, papa, maman. Dump Amir = enfant-m "
        "(veut un bout maintenant). Pas de copain. Troupe D16. "
        "Pas de maîtresse. Flora du retry source → Amir.\n"
        "- **Lieu :** cuisine, matin, gâteau, saladier, assiette, miette, "
        "carrelage, four, fenêtre, beurre, citron, table. BAN nappe / "
        "farine / casserole / tasse (indice pris ailleurs).\n"
        "- **Indice unique :** éclat de saladier (luit à l'ouverture → "
        "tremble après le chaud → luit quand le bout s'effrite → "
        "tient sur le verre). BAN éclat de treille / moule / tuteur / "
        "assiette / farine / tour / comptoir / pot / rouleau / lit / "
        "étagère / torchon / tabouret / nappe / casserole / tasse / miette.\n"
        "- **Question moteur :** « Amir sourit. Que dit-il ? » expected "
        "dump **content**. accepted dump `content | contente | je suis "
        "contente | joie | de la joie | partager`. retry Flora → Amir "
        "(dit-il). Hors Q : null. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Maman pose le saladier près du gâteau. Sur le verre, un éclat "
        "de saladier luit. Beurre, citron, carrelage tiède. Amir veut "
        "un bout **maintenant**. Le gâteau est trop chaud. Poitrine trop "
        "vite. Sourire parti. Papa s'accroupit. Un sourire revient. Il "
        "dit je suis content. Merci vécu. Deux petits bouts. Deuxième "
        "ruse : le bout s'effrite. Il s'arrête, lit l'éclat. Un éclat "
        "de saladier tient sur le verre.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine du matin, saladier, gâteau près de la fenêtre.\n"
        "- Désir : un bout du gâteau, maintenant, à partager.\n"
        "- Objet : gâteau encore chaud, assiette, deux petits bouts.\n"
        "- Indice unique : éclat de saladier, vu dès l'ouverture, payé "
        "sur le verre. Pas éclat d'assiette / farine / nappe.\n"
        "- Urgence douce : il tend la main trop vite.\n"
        "- Imprévu 1 : gâteau trop chaud, poitrine trop vite, sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le bout offert.\n"
        "- Imprévu 2 (plus rusé) : le deuxième bout s'effrite sur l'assiette.\n"
        "- Résolution : il refuse de foncer, observe, écoute la cuisine, "
        "retrouve l'éclat, pose le bout pour maman.\n"
        "- Retour : deux petits bouts ont suffi, éclat sur le verre.\n\n"
        "## Vécu\n\n"
        "Amir veut un bout **maintenant**. Impatience, puis doigts brûlés, "
        "sourire parti. Un sourire revient, tout petit. Il dit je suis "
        "content, puis on peut partager. Papa se baisse, pose une question, "
        "ne récite pas la joie. Ils agissent : un bout sans se presser, "
        "deux petits bouts. Merci vécu. Fin : l'éclat du début tient sur "
        "le verre.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Amir et le gâteau encore chaud (noyau dump). Relance : "
        "Que dit-il ? expected content.\n"
        "- Lieu du dump-meta (cuisine, matin). Maman et papa. "
        "Amir = héros enfant-m. Gâteau / assiette / miette du dump.\n"
        "- Ouverture inventée (maman pose le saladier), pas un gabarit "
        "v2, pas « Le soleil pose des carrés chauds » du source.\n"
        "- Indice unique : éclat de saladier. BAN éclat de treille / "
        "moule / tuteur / assiette / farine / tour / nappe / casserole / "
        "tasse / miette. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « c'est de la joie », « j'ai dit : je suis », "
        "« tu as nommé », « Bravo, Amir ».\n"
        "- Leçon non dite : on la voit quand le sourire revient, quand "
        "Amir dit je suis content, quand il offre un bout. Pas « c'est "
        "de la joie ». Pas « tu as dit ta joie ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Amir sourit. Que dit-il ? ». expected "
        "content. 5 chunks, kinds inchangés. expected/accepted dump "
        "conservés. retry Flora → Amir (dit-il). Hors Q : null.\n"
        "- example4 057 / 089 / 021 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N1.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers le bout qui s'effrite.\n"
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
