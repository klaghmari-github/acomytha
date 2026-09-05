#!/usr/bin/env python3
"""ATOM-COL.ECO.002-01 — F-NAR-019. Le nez rose d'Amir. N2. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.002-01"
N2 = 15
TITLE = "Le nez rose d'Amir"
INDICE = "éclat de carotte"
FIL = (
    "Un sac en papier craque. Une carotte sent la terre. Sur la carotte, "
    "un éclat de carotte brille. Amir veut montrer le nez rose, maintenant. "
    "Il parle trop vite : les mots se perdent. Il lève le sac : personne "
    "ne regarde. Il refuse de foncer, lève la main, attend, puis dit. "
    "Merci vécu. Sur la table, l'éclat de carotte tient."
)
CHARS = "Amir, papa, maman"
SETTING = "cuisine, classe, puis maison"
TIC_PHRASES = (
    "tout doux",
    "tout calme",
    "tout lent",
    "tout bas",
    "tout doucement",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)
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
    "ninon",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai levé la main",
    "j'ai leve la main",
    "j'ai attendu",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "on range les feutres",
    "tu ranges",
    "tu as bien écouté",
    "tu as bien ecoute",
    "on aime écouter",
    "on aime ecouter",
    "écoute la maîtresse",
    "ecoute la maitresse",
    "tu as bien fait",
    "bon travail",
    "une chose, puis",
    "une chose puis",
    "il faut attendre",
    "tu attends ton tour",
    "c'est ton tour",
    "on doit demander",
    "gouttière",
    "gouttiere",
    "crayon",
    "tapis",
    "crochet",
    "buée",
    "buee",
    "croûte",
    "croute",
    "tableau",
    "casier",
    "moufle",
    "craie",
    "cartable",
    "pinceau",
    "casserole",
    "grain de",
    "éclat de terre",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de marche",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de tasse",
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de farine",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de laine",
    "éclat de orange",
    "éclat de lampe",
    "éclat de citron",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de pin",
    "éclat de crayon",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de craie",
    "éclat de tapis",
    "éclat de moufle",
    "éclat de casier",
    "éclat de tableau",
    "éclat de cartable",
    "éclat de pinceau",
    "pli de voile",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "malaise",
    "secret",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de carotte",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_montrer_le_nez_maintenant; "
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
            "sous_texte=il_leve_la_main_avant_de_parler; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="main",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_attend_puis_dit_le_nez_rose; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="carotte",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_couper_papa; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de carotte",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_table; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}


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


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
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
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"tic {tic!r}: {ph}")
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"tic {m.group(0)!r}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"interdit {bad!r}: {ph}")
        out.append(f"{role}|{ph}")
    return out


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


P0000 = [
    "narrateur|La cuisine sent la terre, un peu.",
    "narrateur|Un sac en papier craque sur la table.",
    "narrateur|Dedans, une carotte sent la terre.",
    "narrateur|Un peu de terre est sur le carreau.",
    "narrateur|Une chaussette blanche a une oreille de lapin.",
    "narrateur|Le jardin, derrière la porte, sent l'herbe mouillée.",
    "maman|La carotte est pour plus tard, Amir.",
    "enfant-m|Le lapin du livre a un nez rose.",
    "enfant-m|Tout petit.",
    "papa|Tu le montres à l'école ?",
    "enfant-m|Oui, papa.",
    "narrateur|Sur la carotte, un éclat de carotte brille.",
    "enfant-m|Je le mets sur mon nez, maintenant !",
    "narrateur|En ce moment, Amir saisit la carotte.",
    "narrateur|L'éclat de carotte saute près du sac.",
    "enfant-m|Le nez est rose, papa !",
    "narrateur|Papa n'a pas fini sa phrase.",
    "narrateur|Les deux voix se mélangent.",
    "enfant-m|Oh.",
    "narrateur|Le sourire d'Amir disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "enfant-m|Ça ne veut pas !",
    "papa|Ta main est trop vite ?",
    "narrateur|Papa s'accroupit à la même hauteur.",
    "narrateur|Amir parle trop fort, trop vite.",
    "narrateur|Les mots se perdent près du sac.",
    "enfant-m|Oh.",
    "narrateur|Ses épaules tombent un peu.",
    "papa|Tes pieds sont sur le carreau ?",
    "enfant-m|Oui, papa.",
    "maman|Ta chaussette blanche est à l'endroit ?",
    "enfant-m|Oui, maman.",
    "papa|Tu vois l'oreille de lapin ?",
    "enfant-m|Oui.",
    "enfant-m|Elle est blanche.",
    "maman|On la laisse sur la table ?",
    "enfant-m|Oui, elle est jolie.",
    "papa|On y va ?",
    "enfant-m|On y va.",
    "enfant-m|Au revoir, maman.",
    "maman|Au revoir, Amir.",
    "narrateur|Dehors, le jardin sent l'herbe mouillée.",
    "narrateur|Le sac en papier tape la hanche.",
    "narrateur|La classe sent le papier et la pomme.",
    "narrateur|La maîtresse parle près des chaises.",
    "maitresse|Bonjour.",
    "enfant-m|Bonjour, maîtresse.",
    "narrateur|Amir pose le sac près de sa chaise.",
    "narrateur|Une image montre un lapin blanc.",
    "narrateur|Les oreilles sont trop longues.",
    "narrateur|Le nez est rose, tout petit.",
    "narrateur|Les mots lui chatouillent la bouche.",
    "enfant-m|Je veux parler du nez.",
    "narrateur|Plus tard, une voix s'approche.",
    "narrateur|Elle parle des oreilles du lapin.",
    "enfant-m|Le nez est rose, maintenant !",
    "narrateur|Ses mots se cognent à ceux de la classe.",
    "narrateur|Personne ne tourne la tête.",
    "narrateur|Amir referme la bouche.",
    "narrateur|Il repose les mains sur ses genoux.",
    "narrateur|Le sac reste près de la chaise.",
]

Q0001 = [
    "narrateur|Amir veut parler.",
    "narrateur|Que fait-il d'abord ?",
]

C0001 = [
    "narrateur|Amir veut montrer la carotte, tout de suite.",
    "narrateur|Il lève le sac trop vite.",
    "narrateur|La carotte penche, puis retombe.",
    "enfant-m|Oh.",
    "narrateur|Personne ne regarde le sac.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Il referme la bouche.",
    "narrateur|Il lève la main.",
    "narrateur|Sa main reste en l'air.",
    "narrateur|Une autre voix parle des oreilles.",
    "narrateur|Amir reste près de sa chaise.",
    "narrateur|Il regarde le petit nez rose.",
    "narrateur|L'éclat de carotte brille dans le sac.",
    "maitresse|Amir.",
    "narrateur|Un silence arrive, tout petit.",
    "enfant-m|Le lapin a un nez rose.",
    "enfant-m|Tout petit.",
    "enfant-m|Comme la carotte.",
    "narrateur|Une tête se tourne vers lui.",
    "narrateur|Les oreilles écoutent jusqu'au bout.",
    "narrateur|Le soir, la porte s'ouvre.",
    "narrateur|Ça sent la terre et le papier.",
    "papa|Te voilà, Amir.",
    "maman|Le sac est rentré.",
    "narrateur|La carotte attend sur la table.",
    "narrateur|La chaussette blanche est là.",
    "narrateur|Amir regarde papa.",
    "narrateur|Il ouvre la bouche.",
]

END = [
    "narrateur|Amir veut dire le nez, tout de suite.",
    "enfant-m|Papa, le nez rose.",
    "narrateur|Papa n'a pas fini sa phrase.",
    "papa|Le sac est sur la table, Amir.",
    "narrateur|Les deux voix se mélangent.",
    "enfant-m|Oh.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Il referme la bouche.",
    "narrateur|Il pose les mains à plat.",
    "papa|Tes pieds sont près de la table ?",
    "narrateur|Papa pose le sac contre le bois.",
    "maman|La chaussette blanche est sous la chaise.",
    "narrateur|Maman n'a pas fini non plus.",
    "narrateur|Amir reste jusqu'au silence.",
    "enfant-m|Je peux te dire quelque chose ?",
    "maman|Oui, nous t'écoutons.",
    "enfant-m|Le lapin a un nez rose.",
    "enfant-m|Tout petit, comme la carotte.",
    "papa|Merci, Amir.",
    "narrateur|Papa a entendu toute la phrase.",
    "maman|Tu veux un peu d'eau ?",
    "enfant-m|Oui, maman.",
    "narrateur|Amir veut poser l'éclat, tout de suite.",
    "narrateur|Il le saisit trop vite.",
    "narrateur|L'éclat glisse entre ses doigts.",
    "enfant-m|Oh.",
    "narrateur|Amir s'arrête.",
    "narrateur|Ses mains se ferment, puis s'ouvrent.",
    "narrateur|Il refuse de foncer.",
    "narrateur|Il pose l'éclat plus lentement.",
    "narrateur|Le nez d'Amir devient un peu rose.",
    "enfant-m|Il est rose, maman !",
]

FIN = [
    "narrateur|Ils restent près de la table.",
    "narrateur|La carotte repose dans le sac.",
    "enfant-m|Comme ce matin, papa !",
    "papa|Tu le vois, toi ?",
    "enfant-m|Oui, sur la carotte.",
    "maman|On est bien, ici.",
    "narrateur|Le sac sent la terre, un peu.",
    "narrateur|Amir glisse le pied, sans se presser.",
    "enfant-m|On le sent, maman.",
    "maman|Tu le sens sur tes joues ?",
    "enfant-m|Oui, il est frais.",
    "narrateur|La chaussette blanche repose contre le bois.",
    "enfant-m|Elle a une oreille de lapin.",
    "papa|On la laisse ?",
    "enfant-m|Oui.",
    "narrateur|L'éclat de carotte tient sur la table.",
]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    wanted = {
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_Q0001",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    }
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in wanted]
    if missing:
        raise SystemExit(f"{SID} chunks inattendus: {missing}")

    by = {
        "CHK_T0000_P0000": voice(
            by_src["CHK_T0000_P0000"], P0000, "opening", "sac,porte",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "attendre",
                    "accepted_examples": (
                        "attendre | il attend | lever la main | la main"
                    ),
                    "retry_prompt": (
                        "Amir veut parler. Que fait-il d'abord ?"
                    ),
                    "engine_ok_text": "Oui, il attend.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "chaise,voix",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "table,eau",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "sac,carotte",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "ninon" in blob:
        raise SystemExit(f"{SID}: Ninon interdite")
    if not all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in chunks):
        raise SystemExit(f"{SID}: TTS incomplet")
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
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Amir veut parler. Que fait-il d'abord ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    mait = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("maitresse|")
    ).lower()
    if any(x in mait for x in ("écoute", "range", "merci", "règle", "leçon", "tour")):
        raise SystemExit(f"{SID}: maîtresse leçon parlée: {mait}")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nwords = sum(words(c["text"]) for c in chunks)
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** COL.ECO.002 — attendre son tour / lever la main "
        "avant de parler (vécue : parler trop vite → mots perdus ; lever "
        "le sac → personne ne regarde ; lever la main, attendre, puis dire)\n"
        "- **Personnages :** Amir, papa, maman (maîtresse = label, pas de "
        "leçon parlée)\n"
        "- **Lieu :** cuisine, classe, puis maison ; sac papier, carotte "
        "qui sent la terre, terre sur le carreau, chaussette blanche\n"
        "- **Indice unique :** éclat de carotte (table du matin → sac en "
        "classe → table du soir)\n"
        "- **Question moteur :** Amir veut parler. Que fait-il d'abord ? "
        "→ attendre (lever la main)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La cuisine sent la terre. Un sac en papier craque. Dedans, une "
        "carotte sent la terre. Un peu de terre est sur le carreau. Une "
        "chaussette blanche a une oreille de lapin. Sur la carotte, un "
        "éclat de carotte brille. Amir veut le nez rose **maintenant**. Il "
        "saisit trop vite : l'éclat saute. Il coupe papa : les voix se "
        "mélangent. Sourire parti, épaules basses. Papa s'accroupit. À la "
        "classe, une voix parle des oreilles. Il dit le nez tout de suite : "
        "les mots se cognent, personne n'entend. Il lève le sac : la "
        "carotte retombe, personne ne regarde. Il refuse de foncer, lève "
        "la main, reste, dit le nez rose. Une tête se tourne. Le soir, il "
        "coupe papa, refuse, attend le silence, dit. Merci vécu. Il pose "
        "l'éclat trop vite, s'arrête, pose plus lentement. Le nez d'Amir "
        "devient rose. Sur la table, l'éclat tient.\n\n"
        "## Vécu\n\n"
        "Amir veut montrer le nez rose **maintenant**. Impatience, puis "
        "épaules qui tombent quand les mots se perdent. Papa s'accroupit, "
        "pose une question, ne récite pas la règle. Amir agit : bouche "
        "fermée, main en l'air, phrase entière. Merci vécu après l'écoute. "
        "Fin : l'éclat du début tient sur la table, le nez est rose.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau « Le nez rose d'Amir » (dump col_eco_09_05), pas "
        "« Le petit pain d'Amir » (xlsx / audit example2). Monde dump : "
        "cuisine, classe, maison, sac papier, carotte, terre, carreau, "
        "chaussette blanche.\n"
        "- Ouverture inventée (cuisine qui sent la terre, éclat sur la "
        "carotte), pas « joue au salon », pas gabarit v2.\n"
        "- Distinct de COL.ECO.001-* (raconter un malaise). Ici : attendre "
        "son tour / lever la main avant de parler, vécu en classe puis à "
        "la maison.\n"
        "- Maîtresse = label (bonjour, Amir), pas de leçon parlée. Pas "
        "« il faut attendre / c'est ton tour / tu as attendu ».\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent / "
        "tout bas » retirés. Pas de merle, pas de miel.\n"
        "- Pas crayon, tapis, crochet, buée, croûte, tableau, casier, "
        "moufle, craie, cartable, pinceau, casserole, grain.\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- Indice unique « éclat de carotte » nommé à l'ouverture, revu "
        "quand il saute, revu dans le sac, payé à la fin.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive.\n"
        "- N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        f"- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
