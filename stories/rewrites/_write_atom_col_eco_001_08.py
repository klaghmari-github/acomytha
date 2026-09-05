#!/usr/bin/env python3
"""ATOM-COL.ECO.001-08 — Le cartable de Raphaël (F-NAR-019, N3, COL.ECO.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.001-08"
TITLE = "Le cartable de Raphaël"
N3 = LIMITS["N3"]
CHARS = "Raphaël, papa, maman"
SETTING = (
    "école puis maison, cartable contre le bois de la porte, "
    "horloge du couloir, poussière"
)
INDICE = "éclat de cartable"
FIL = (
    "Une poussière dore près du bois de la porte. Sur le fermoir, un "
    "éclat de cartable brille. Raphaël veut parler maintenant. Il coupe "
    "papa : les mots se perdent. Le cartable penche. À l'école, un secret "
    "serre le ventre ; sa phrase se cogne à la classe. Il refuse de "
    "foncer, attend le silence, raconte. Merci vécu. Sur le fermoir, "
    "l'éclat de cartable tient."
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
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "ewen",
    "casserole",
    "crayon",
    "buée",
    "buee",
    "croûte",
    "croute",
    "tableau",
    "casier",
    "moufle",
    "craie",
    "gouttière",
    "gouttiere",
    "lune d'étain",
    "lune d'etain",
    "point de gouttière",
    "point de gouttiere",
    "grain de",
    "éclat de casserole",
    "éclat de crayon",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de bec",
    "éclat de marche",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de wagon",
    "éclat de citron",
    "éclat de lampe",
    "éclat de nappe",
    "éclat de farine",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de laine",
    "éclat de carreau",
    "éclat de grain",
    "éclat de pince",
    "éclat de corde",
    "éclat de caisse",
    "éclat d'horloge",
    "éclat de tasse",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de cartable",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_parler_maintenant; "
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
            "sous_texte=il_raconte_quand_on_l_entend; "
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
            "destinataire=enfant; sous_texte=il_attend_puis_on_l_entend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="gourde",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_sur_la_gourde; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de cartable",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_fermoir; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "raconter",
    "accepted_examples": (
        "raconter | il raconte | à papa | à la maison | écouter"
    ),
    "retry_prompt": "Il raconte à papa. Que fait Raphaël ?",
    "engine_ok_text": "Oui, il raconte.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "porte,horloge",
        [
            "narrateur|Une poussière dore près du bois de la porte.",
            "narrateur|Le bois est froid, un peu lisse.",
            "narrateur|Le cartable s'appuie contre ce bois.",
            "narrateur|Sur le fermoir, un éclat de cartable brille.",
            "enfant-m|Il est blanc, papa.",
            "papa|C'est le cuir, sous la lumière.",
            "narrateur|Papa glisse une gourde dans la poche.",
            "maman|Tes lacets, Raphaël ?",
            "narrateur|Maman noue un lacet, puis l'autre.",
            "narrateur|Ça sent le cuir du cartable.",
            "narrateur|L'horloge du couloir fait tic.",
            "maman|Tu l'entends, Raphaël ?",
            "enfant-m|Tic.",
            "enfant-m|Elle est lente.",
            "papa|Elle dit l'heure.",
            "enfant-m|Papa, le fermoir brille, maintenant !",
            "narrateur|Papa parle à maman, près de la gourde.",
            "papa|La gourde est pleine, pour midi.",
            "narrateur|Les mots de Raphaël se cognent à ceux de papa et de maman.",
            "narrateur|Personne ne tourne la tête.",
            "papa|Tu disais quelque chose, Raphaël ?",
            "enfant-m|Le fermoir.",
            "enfant-m|Il brille.",
            "narrateur|En ce moment, Raphaël pose la main sur le cartable.",
            "narrateur|Le tissu est rêche, un peu lourd.",
            "enfant-m|Je le porte, maintenant !",
            "narrateur|Il soulève le cartable trop vite.",
            "narrateur|Le fermoir claque.",
            "narrateur|La gourde penche dans la poche.",
            "enfant-m|Oh.",
            "narrateur|L'éclat de cartable tremble, puis tient.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, l'envie de parler et l'inquiétude se bousculent.",
            "enfant-m|Ça ne veut pas, maman.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|On le porte ensemble ?",
            "enfant-m|Oui, papa.",
            "narrateur|Ils avancent jusqu'à la porte.",
            "maman|Tu dis bonjour, à l'école ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Au revoir, maman.",
            "maman|Au revoir, Raphaël.",
            "narrateur|Dehors, la rue brille un peu.",
            "narrateur|L'école sent les feutres.",
            "narrateur|Un feutre orange attend sur la table.",
            "narrateur|La maîtresse parle près des chaises, d'une voix claire.",
            "enfant-m|Bonjour, maîtresse.",
            "narrateur|Raphaël glisse le feutre dans la boîte.",
            "narrateur|Le bouchon est enfoncé, bien fermé.",
            "narrateur|L'orange sent fort, comme une peau.",
            "narrateur|Plus tard, quelqu'un s'approche.",
            "narrateur|Une voix d'enfant parle bas, près de l'oreille, d'un secret.",
            "narrateur|Raphaël sent un malaise.",
            "narrateur|Son ventre se serre.",
            "enfant-m|Je le dis, maintenant !",
            "narrateur|Il ouvre la bouche trop vite.",
            "narrateur|Ses mots se cognent à la classe.",
            "narrateur|Personne ne comprend.",
            "narrateur|Raphaël referme la bouche.",
            "narrateur|Il serre les mains sur la table.",
            "narrateur|Il se souvient du tic de l'horloge, à la maison.",
            "narrateur|Le soir, le cartable s'appuie contre la porte.",
            "narrateur|L'horloge du couloir fait tic.",
            "narrateur|La poussière dore, plus basse.",
            "narrateur|La porte s'ouvre.",
            "papa|Te voilà.",
            "papa|La gourde est vide ?",
            "narrateur|Raphaël pose le cartable.",
            "narrateur|Le tissu est rêche.",
            "narrateur|Le ventre est serré, minuscule.",
            "narrateur|Il regarde papa.",
            "narrateur|Il ouvre la bouche.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Raphaël a un malaise.",
            "narrateur|Que fait-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "porte,cartable",
        [
            "narrateur|Raphaël ouvre la bouche trop vite.",
            "enfant-m|Papa, un secret.",
            "narrateur|Papa n'a pas fini sa phrase.",
            "papa|La gourde est vide, Raphaël.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Raphaël refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Il pose les mains à plat.",
            "papa|Tes lacets sont un peu poussiéreux.",
            "narrateur|Papa pose la gourde sur le bois.",
            "maman|L'eau peut attendre.",
            "narrateur|Maman n'a pas fini non plus.",
            "narrateur|Raphaël attend que le silence arrive près du cartable.",
            "narrateur|Sur le fermoir, l'éclat de cartable brille.",
            "enfant-m|Il est là.",
            "enfant-m|Je peux te dire quelque chose ?",
            "maman|Oui, nous t'écoutons.",
            "enfant-m|Un camarade a parlé d'un secret.",
            "enfant-m|J'ai eu un malaise.",
            "papa|Merci, Raphaël.",
            "narrateur|Papa a entendu toute la phrase, sans la couper.",
            "maman|Tu as soif ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Le ventre de Raphaël se desserre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "gourde,eau",
        [
            "narrateur|Raphaël veut dire le reste tout de suite.",
            "enfant-m|Il a dit : garde ça.",
            "narrateur|Il saisit la gourde trop vite.",
            "narrateur|L'eau penche vers le goulot.",
            "enfant-m|Oh.",
            "narrateur|Les mots se perdent dans le couloir, sous le tic.",
            "narrateur|Raphaël s'arrête.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Il refuse de foncer.",
            "narrateur|Il pose la gourde sur le bois.",
            "narrateur|Il écoute le tic, un instant.",
            "enfant-m|Le secret m'a serré le ventre.",
            "papa|Tu le poses, le cartable ?",
            "enfant-m|Oui.",
            "narrateur|Raphaël appuie le cartable contre la porte.",
            "maman|La gourde, pour demain ?",
            "enfant-m|Je la remplis.",
            "narrateur|Maman verse l'eau.",
            "narrateur|Ça fait un petit bruit.",
            "narrateur|Raphaël glisse la gourde dans la poche.",
            "papa|Le fermoir, tu le vois ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le bois tient le cuir, sans bouger.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "porte,horloge",
        [
            "narrateur|Le cartable attend contre la porte.",
            "narrateur|L'horloge du couloir fait tic, plus loin.",
            "enfant-m|Il a fait tout le chemin.",
            "papa|Toi aussi.",
            "narrateur|La poussière dore, basse, près du bois de la porte.",
            "maman|Tu souffles ?",
            "enfant-m|Oui, maman.",
            "narrateur|Raphaël souffle.",
            "narrateur|Le ventre est large, à sa place.",
            "maman|On est bien, ici.",
            "papa|La gourde est pleine, pour demain.",
            "enfant-m|Je la verrai.",
            "narrateur|Le tic remplit le couloir.",
            "narrateur|L'éclat de cartable tient sur le fermoir.",
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
    if "ewen" in blob:
        raise SystemExit(f"{SID}: Ewen resté")
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
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** COL.ECO.001 — écouter / en parler à la maison "
        "(vécue : veut raconter maintenant ; première idée échoue ; refuse "
        "de foncer ; raconte quand le silence arrive)\n"
        "- **Personnages :** Raphaël, papa, maman. Troupe D16. Maîtresse = "
        "label (parle près des chaises), pas de leçon récitée. Adultes "
        "parlants = papa/maman. Ewen retiré.\n"
        "- **Lieu :** école puis maison, cartable contre le bois de la "
        "porte, horloge du couloir, poussière. ≠ COL.ECO.001-01..07 "
        "(gouttière/crayon, rayon/buée, pain/croûte, soleil/tableau, "
        "chaussette/casier, moufle, craie).\n"
        "- **Indice unique :** éclat de cartable (fermoir au matin → "
        "tremble quand le cartable penche → brille au silence → tient "
        "sur le fermoir)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une poussière dore près du bois de la porte. Sur le fermoir, un "
        "éclat de cartable brille. Raphaël veut parler **maintenant**. Il "
        "coupe papa : les mots se cognent. Il soulève trop vite : le "
        "fermoir claque, la gourde penche. Sourire parti, épaules basses. "
        "Papa se baisse. À l'école, un secret serre le ventre ; il parle "
        "pendant la classe : la phrase se perd. Le soir, il ouvre la "
        "bouche trop vite : les voix se mélangent. Il refuse de foncer, "
        "attend le silence, raconte le malaise. Merci vécu. Il saisit la "
        "gourde trop vite : l'eau penche, les mots se perdent. Il pose, "
        "écoute, finit. Contre la porte, l'éclat tient sur le fermoir.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : couloir, poussière, bois froid, cartable, fermoir, "
        "gourde, lacets, horloge, feutre orange, école, porte du soir.\n"
        "- Désir : parler / raconter **maintenant**.\n"
        "- Objet : cartable, fermoir, gourde, feutre orange.\n"
        "- Indice unique : éclat de cartable, vu dès l'ouverture, payé "
        "au fermoir.\n"
        "- Urgence douce : le secret serre le ventre, papa n'a pas fini.\n"
        "- Imprévu 1 : il coupe, soulève trop vite ; à l'école sa phrase "
        "se cogne à la classe.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après la phrase entière.\n"
        "- Imprévu 2 (plus rusé) : il veut dire le reste en saisissant "
        "la gourde ; l'eau penche, les mots se perdent.\n"
        "- Résolution : il refuse de foncer, pose, écoute, raconte, "
        "appuie le cartable contre la porte.\n"
        "- Retour : poussière basse, tic plus loin, gourde pleine, éclat "
        "sur le fermoir.\n\n"
        "## Vécu\n\n"
        "Raphaël veut parler **maintenant**. Impatience (coupe, cartable "
        "trop vite, bouche ouverte en classe), puis sourire qui "
        "disparaît, épaules qui tombent. Papa se baisse, pose une "
        "question, ne récite pas la règle. Raphaël agit : bouche fermée, "
        "mains à plat, phrase entière. Merci vécu après l'écoute. Fin : "
        "l'éclat du début tient sur le fermoir.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : école puis maison, "
        "cartable contre le bois, horloge du couloir, poussière. Ewen "
        "→ Raphaël. Relance : Que fait Raphaël ?\n"
        "- Ouverture inventée (poussière qui dore près du bois), pas un "
        "gabarit v2, pas « joue au salon ».\n"
        "- Indice unique : éclat de cartable (roster). Pas casserole "
        "(ROU-08), pas crayon/buée/croûte/tableau/casier/moufle/craie, "
        "pas grains, lune d'étain, point de gouttière, merle, miel, "
        "marque fine.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` "
        "retirés.\n"
        "- Leçon non dite : on l'entend quand il attend le silence. Pas "
        "« j'ai écouté », pas « bon travail », pas « l'histoire est "
        "finie », pas « on écoute la maîtresse ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Maîtresse = label, pas de réplique de leçon.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive vers la gourde.\n"
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
