#!/usr/bin/env python3
"""ATOM-AUT.AFF.003-05 — La feuille qui danse (F-NAR-019, N2, AUT.AFF.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.003-05"
TITLE = "La feuille qui danse"
N2 = LIMITS["N2"]
CHARS = "Nino, maman"
SETTING = "fenêtre de la maison, puis aire de jeux"
FIL = (
    "Nino connaît le toc de la fenêtre. Un éclat de vitre cligne sur le verre. "
    "Il veut une feuille dans le seau vert, maintenant. Il plaque trop vite : "
    "la feuille s'envole, manche tordue, ours au toboggan. Il reprend seau, "
    "manteau, ours. Merci vécu. À la maison il veut glisser trop fort. Il "
    "refuse de foncer, retrouve l'éclat, pose le seau. La feuille tapote."
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
    "maîtresse",
    "maitresse",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "grain de sable",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de marche",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cuillère",
    "éclat d'orange",
    "éclat de colle",
    "éclat de lessive",
    "éclat de sonnette",
    "trait de craie",
    "trait de vitre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de vitre",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_feuille_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Avant de partir",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; sous_texte=avant_de_partir_il_reprend; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="manteau",
        note=(
            "arc=confirmation; intention=relancer; emotion=fierté_calme; "
            "intensite=1; destinataire=enfant; sous_texte=il_reprend_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de vitre",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis prudence; intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de vitre",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_reste_pale_le_seau_sous_la_fenetre; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "reprendre",
    "accepted_examples": "reprendre | ses affaires | il reprend | elle reprend | avant de partir",
    "retry_prompt": "Il reprend ses affaires. Que fait Nino ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "fenetre,enfants_parc",
        [
            "narrateur|Une ombre orange traverse le plancher, lente.",
            "narrateur|Elle grimpe le mur, jusqu'au rebord.",
            "narrateur|Derrière le verre, une feuille tapote.",
            "narrateur|Toc, toc.",
            "narrateur|Le soleil d'après-midi la rend orange.",
            "narrateur|Maman ouvre un peu la fenêtre.",
            "narrateur|Un souffle d'air entre, tiède.",
            "maman|Tu as vu la feuille, Nino ?",
            "enfant-m|Elle danse !",
            "narrateur|Sur la vitre, un éclat de vitre cligne.",
            "maman|Tu vois l'éclat ?",
            "enfant-m|Il brille, sur le verre.",
            "narrateur|Maman pose la feuille sur le rebord.",
            "enfant-m|Je veux une feuille, maintenant !",
            "enfant-m|Dans mon seau vert !",
            "maman|On va à l'aire de jeux.",
            "narrateur|Ils prennent le sac, près de la porte.",
            "narrateur|La rue sent le sable chaud.",
            "narrateur|En ce moment, Nino pose le seau vert au bac.",
            "narrateur|Le sable est tiède, un peu collant.",
            "narrateur|Maman s'assoit au bord, à sa hauteur.",
            "narrateur|Le bac du toboggan tiède sent le sable.",
            "narrateur|Le manteau bleu attend au bord, plié.",
            "narrateur|L'ours doudou s'appuie au petit toboggan.",
            "enfant-m|Le toboggan est chaud.",
            "maman|Le soleil l'a touché.",
            "narrateur|Nino verse le sable.",
            "narrateur|Ça fait chh, dans le seau.",
            "narrateur|Une feuille orange passe, basse.",
            "enfant-m|La mienne, maintenant !",
            "narrateur|Elle se pose dans le seau vert.",
            "narrateur|Nino plaque la main dessus, vite.",
            "narrateur|Le seau bascule.",
            "narrateur|Du sable glisse, chaud.",
            "narrateur|La feuille s'envole au-dessus du bac.",
            "enfant-m|Elle est partie !",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Nino veut courir après la feuille.",
            "narrateur|Il tire le seau et le manteau, ensemble.",
            "narrateur|La manche se tord, à l'envers.",
            "narrateur|L'ours bascule, près du toboggan.",
            "enfant-m|Ça reste coincé !",
            "maman|C'est l'heure.",
            "enfant-m|La feuille aussi ?",
            "maman|La feuille peut voler.",
            "maman|Toi, tu reprends le seau ?",
            "narrateur|Nino cherche le seau.",
            "narrateur|Le seau est vert, un peu sableux.",
            "narrateur|Il le prend.",
            "enfant-m|J'ai le seau.",
            "narrateur|Le manteau est au bord.",
            "narrateur|Une manche est à l'envers.",
            "narrateur|L'ours est près du toboggan.",
            "maman|Tu poses le seau un moment ?",
            "narrateur|Maman s'accroupit à sa hauteur.",
            "maman|Tu regardes tes affaires ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino prépare le départ.",
            "narrateur|Le seau, le manteau, l'ours attendent.",
            "narrateur|Avant de partir, que fait Nino ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "manteau,porte",
        [
            "narrateur|Nino refuse de tirer plus fort.",
            "narrateur|Il pose le seau vert, net.",
            "enfant-m|Je pose le seau.",
            "narrateur|Nino reprend le manteau bleu.",
            "narrateur|Il tourne la manche, lente.",
            "enfant-m|Le manteau est bleu.",
            "narrateur|Il le passe, sans courir.",
            "maman|Et l'ours ?",
            "narrateur|Nino va près du toboggan.",
            "narrateur|L'ours est tiède, comme le plastique.",
            "enfant-m|L'ours est là.",
            "narrateur|Il reprend l'ours contre lui.",
            "maman|Tu as tes affaires, Nino ?",
            "enfant-m|Oui, maman.",
            "maman|Merci, Nino.",
            "maman|On rentre vers la fenêtre ?",
            "enfant-m|Oui.",
            "narrateur|Ils marchent vers la maison.",
            "narrateur|Le seau cogne un peu, sableux.",
            "narrateur|Contre lui, le doudou reste chaud.",
            "maman|Je marche à côté.",
            "enfant-m|Moi aussi.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "porte",
        [
            "narrateur|Nino tient le seau, devant la porte.",
            "narrateur|Maman ouvre.",
            "narrateur|La feuille du rebord est là, orange.",
            "enfant-m|Elle a attendu !",
            "enfant-m|Dans le seau, maintenant !",
            "narrateur|Il penche le seau trop vite.",
            "narrateur|Du sable saute sur le rebord.",
            "narrateur|La feuille bascule vers la fenêtre ouverte.",
            "enfant-m|Elle va partir !",
            "narrateur|Nino veut la rattraper d'un coup.",
            "narrateur|Il refuse de foncer.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Maman attend, sans parler.",
            "narrateur|Il observe le seau, puis la vitre.",
            "narrateur|Sur le verre, un éclat de vitre cligne.",
            "enfant-m|C'est celui du début.",
            "maman|Tu le vois, à la fenêtre ?",
            "enfant-m|Oui, il est resté.",
            "narrateur|Nino pose le seau sous le rebord, lent.",
            "narrateur|Il glisse la feuille orange, sans brusquer.",
            "narrateur|Elle tapote le fond.",
            "narrateur|Toc.",
            "enfant-m|Elle visite.",
            "maman|Tu poses le manteau ?",
            "narrateur|Nino pose le manteau près de la porte.",
            "narrateur|L'ours reste dans son bras.",
            "narrateur|La fenêtre se ferme un peu.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "porte",
        [
            "enfant-m|La feuille a sa place.",
            "narrateur|Le seau vert reste sous la fenêtre.",
            "narrateur|Nino raccroche le manteau.",
            "enfant-m|Il est à sa place.",
            "maman|Tu as fini de poser tes chaussures ?",
            "enfant-m|Oui, maman.",
            "narrateur|La trace tiède de la paume a disparu.",
            "narrateur|L'éclat de vitre reste, pâle, sur le verre.",
            "narrateur|L'ours regarde le seau.",
        ],
    ),
}


def vet(lines: list[str]) -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    for raw in lines:
        if "|" not in raw:
            raise SystemExit(f"sans | : {raw}")
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
        extra: dict = {}
        if cid == "CHK_T0000_P0000_Q0001":
            extra["pause_before_ms"] = 200
            extra["fields"] = Q_FIELDS
        elif cid != "CHK_T0000_P0000":
            extra["pause_before_ms"] = 200
        by[cid] = voice(c, lines, profile, sons, extra)
    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if blob.count("merci") != 1:
        raise SystemExit(f"{SID}: merci ×{blob.count('merci')}")
    if "éclat de vitre" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de vitre" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé au climax")
    if "éclat de vitre" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "reprend" not in by["CHK_T0000_P0000_C0001"]["text"].lower():
        raise SystemExit(f"{SID}: leçon reprendre absente de C0001")
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
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** AUT.AFF.003 — reprendre ses affaires (vécue, jamais dite)\n"
        "- **Personnages :** Nino, maman. Troupe D16.\n"
        "- **Lieu :** fenêtre de la maison, puis aire de jeux "
        "(bac du toboggan tiède, coin du rebord)\n"
        "- **Indice unique :** éclat de vitre (verre de la fenêtre → seau trop "
        "penché → pâle au retour)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une ombre orange traverse le plancher. Une feuille tapote la vitre. "
        "Un éclat de vitre cligne sur le verre. Nino veut **une feuille dans "
        "le seau vert, maintenant**. Première idée : plaquer la main. Le seau "
        "bascule, la feuille s'envole. Il tire seau et manteau ensemble : "
        "coincé. Il reprend le seau, puis le manteau, puis l'ours. Merci "
        "vécu. À la maison il penche trop vite : la feuille du rebord bascule "
        "vers la fenêtre ouverte. Il refuse de foncer, retrouve l'éclat, pose "
        "le seau. Toc. Retour : manteau raccroché, éclat pâle, seau sous la "
        "fenêtre.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : fenêtre, ombre orange sur le plancher, rebord, aire du "
        "petit toboggan, sable tiède.\n"
        "- Désir : une feuille dans le seau vert, maintenant, pour la fenêtre.\n"
        "- Objet : seau vert (sableux, mission : porter la feuille jusqu'au "
        "rebord).\n"
        "- Indice unique : éclat de vitre, vu dès l'ouverture, payé au climax "
        "et à la fin.\n"
        "- Urgence douce : la feuille danse, tout de suite.\n"
        "- Imprévu 1 : main plaquée, seau basculé, feuille partie, manche "
        "tordue.\n"
        "- Cue : maman à la même hauteur, une question. Un merci vécu, après "
        "le manteau et l'ours.\n"
        "- Imprévu 2 (plus rusé) : seau trop penché, feuille du rebord vers "
        "la fenêtre ouverte.\n"
        "- Résolution : il refuse de foncer, lit l'éclat, pose le seau, toc.\n"
        "- Retour : manteau raccroché, ours au bras, éclat pâle.\n\n"
        "## Vécu\n\n"
        "Nino veut la feuille **maintenant**. Impatience, puis sourire qui "
        "disparaît quand le seau bascule. Maman se baisse, pose une question, "
        "ne récite pas la règle. Nino agit : seau posé, manteau repris, ours "
        "repris. Merci vécu après les affaires. À la fenêtre, il refuse de "
        "foncer. Fin : l'éclat du début est pâle sur le verre. Le seau est "
        "sous le rebord.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : fenêtre de la maison, puis "
        "aire de jeux. ≠ 003-01 (parc, bac à sable, seau jaune). ≠ 003-02 "
        "(cuisine puis parc, lapin). ≠ 003-03 (maison, parc, pique-nique, "
        "capitaine). ≠ 003-04 (maison après la pluie, square, chaussettes).\n"
        "- Ouverture inventée (ombre orange sur le plancher, toc, éclat), "
        "pas un gabarit v2, pas « Nino est dans l'entrée ».\n"
        "- Indice unique : éclat de vitre (roster). Pas grain de miette/foin/"
        "feuille/paille/pin/pépin/sable, pas éclat de pince/thermos/coquille/"
        "bouton/ticket/goutte/boucle/corde/caisse/marche/caillou/liste/clé/"
        "cuillère/orange/colle/lessive/sonnette, pas trait de craie/vitre, "
        "merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : il reprend seau, manteau, ours, les pose. Pas de "
        "morale.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée (reprendre). 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle plus tendu. Action plus vive à l'ouverture.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
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
