#!/usr/bin/env python3
"""ATOM-AUT.AFF.003-02 — La maison du lapin (F-NAR-019, N2, AUT.AFF.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.003-02"
TITLE = "La maison du lapin"
N2 = LIMITS["N2"]
CHARS = "Aniss, maman"
SETTING = "cuisine puis parc, fin d'après-midi"
FIL = (
    "Aniss connaît la cuisine. Un éclat d'orange cligne sur le bois. "
    "Il veut la maison du lapin, maintenant. Au parc, il pousse le doudou "
    "dans un tas trop mou : le lapin glisse dans l'herbe. Il part les mains "
    "vides, refuse, reprend pelle, casquette, lapin. À la cuisine, l'oreille "
    "se coince. Il refuse de foncer, suit l'éclat, plie une porte. Le lapin "
    "rentre. L'éclat reste pâle sur le bois."
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
    "écaille",
    "ecaille",
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "grain de pomme",
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
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de tasse",
    "trait de craie",
    "trait de vitre",
    "seau jaune",
    "bac à sable",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat d'orange",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_maison_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="affaires",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=avant_de_partir_il_reprend; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="pelle",
        note=(
            "arc=confirmation; intention=relancer; emotion=fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_reprend_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat d'orange",
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
        emphasis="éclat d'orange",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_reste_pale_sur_le_bois; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "reprendre",
    "accepted_examples": "reprendre | ses affaires | il reprend | elle reprend | avant de partir",
    "retry_prompt": "Il reprend ses affaires. Que fait Aniss ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "porte,enfants_parc",
        [
            "narrateur|La lumière baisse sur les carreaux de la cuisine.",
            "narrateur|Aniss connaît cette table, le bol, la porte.",
            "narrateur|La fenêtre est tiède, un peu.",
            "narrateur|Un détail paraît nouveau, sur le bois.",
            "narrateur|Après le goûter, un éclat d'orange cligne.",
            "narrateur|Le jus a attrapé le soleil, bas.",
            "maman|Aniss, tu vois l'éclat ?",
            "enfant-m|Il brille, maman.",
            "enfant-m|Je veux la maison du lapin, maintenant !",
            "narrateur|Le doudou lapin attend près de la porte.",
            "narrateur|Sa grande oreille plie un peu.",
            "narrateur|La pelle rouge est contre le mur.",
            "narrateur|La casquette verte pend au crochet.",
            "maman|On va au parc ?",
            "enfant-m|Oui.",
            "enfant-m|Avec une porte, pour lui.",
            "narrateur|Maman passe un linge tiède sur ses doigts.",
            "narrateur|Les doigts étaient collants, un peu.",
            "narrateur|Ils ferment la porte.",
            "narrateur|La rue sent l'orange, tiède.",
            "narrateur|En ce moment, Aniss court vers le banc du parc.",
            "narrateur|Le soleil baisse derrière les arbres.",
            "narrateur|Le banc est froid, un peu.",
            "narrateur|Maman s'assoit.",
            "narrateur|Aniss pose le lapin dans l'herbe.",
            "enfant-m|Sa maison, tout de suite.",
            "narrateur|Il verse du sable avec la pelle rouge.",
            "narrateur|Ça fait chh, trop vite.",
            "narrateur|Les murs tombent, mous.",
            "enfant-m|Reste là !",
            "narrateur|Il pousse le lapin dans le tas.",
            "narrateur|Le lapin glisse, sans un bruit.",
            "narrateur|Il roule dans l'herbe, oreille pliée.",
            "enfant-m|Oh.",
            "enfant-m|Il est parti !",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Maman s'accroupit à sa hauteur.",
            "maman|Tu le cherches, Aniss ?",
            "enfant-m|Il ne veut pas rentrer.",
            "maman|Le soleil baisse.",
            "maman|On rentre.",
            "enfant-m|La porte n'est pas finie.",
            "maman|La maison, on la fera à la maison.",
            "enfant-m|Avec la pelle ?",
            "maman|Avec la pelle.",
            "maman|Et le lapin.",
            "narrateur|Aniss veut partir d'un coup.",
            "narrateur|Il marche vers la grille, les mains vides.",
            "narrateur|La pelle reste dans le sable.",
            "narrateur|La casquette reste sur le banc.",
            "narrateur|Le lapin reste dans l'herbe.",
            "enfant-m|Mes mains sont vides.",
            "maman|Tu regardes tes affaires ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss prépare le retour.",
            "narrateur|Ses affaires attendent au parc.",
            "narrateur|Avant de partir, que fait Aniss ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "pelle,porte",
        [
            "narrateur|Aniss refuse de partir les mains vides.",
            "narrateur|Il revient vers le tas de sable.",
            "narrateur|La pelle rouge attend, couchée.",
            "narrateur|Il la reprend.",
            "narrateur|Un peu de sable tombe.",
            "enfant-m|J'ai la pelle.",
            "narrateur|Il va vers le banc froid.",
            "narrateur|La casquette verte est sous la main de maman.",
            "maman|Je la tenais.",
            "enfant-m|Ma casquette !",
            "narrateur|Il la prend, verte, un peu froide.",
            "narrateur|Il va dans l'herbe.",
            "narrateur|L'herbe chatouille un peu.",
            "narrateur|Le lapin a une oreille pliée.",
            "enfant-m|Le voilà.",
            "narrateur|Aniss le prend contre lui.",
            "maman|Merci, Aniss.",
            "maman|Tu tiens bien tout ?",
            "enfant-m|Oui, maman.",
            "narrateur|Ils marchent vers la maison.",
            "narrateur|La pelle tape un peu sa jambe.",
            "enfant-m|On va faire la porte.",
            "maman|Oui.",
            "maman|On ouvre la cuisine ?",
            "enfant-m|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "carton,porte",
        [
            "narrateur|Ils arrivent dans la cuisine.",
            "narrateur|Sur le bois, l'éclat d'orange cligne, pâle.",
            "enfant-m|Il a attendu.",
            "maman|Oui.",
            "maman|Comme le lapin.",
            "maman|Tu poses la pelle près des chaussures ?",
            "narrateur|Aniss pose la pelle.",
            "narrateur|Il pose la casquette.",
            "narrateur|Le lapin reste dans son bras.",
            "narrateur|Maman sort une boîte à chaussures.",
            "maman|Voici la maison.",
            "enfant-m|Et la porte, maintenant !",
            "narrateur|Il veut glisser le lapin, d'un coup.",
            "narrateur|L'oreille se coince au bord.",
            "enfant-m|Ça ne rentre pas !",
            "narrateur|Le carton refuse, dur.",
            "narrateur|Aniss veut pousser plus fort.",
            "narrateur|Cette fois, il refuse de foncer.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Il observe la boîte, puis la cuisine.",
            "narrateur|Sur le bois, l'éclat d'orange cligne.",
            "enfant-m|C'est celui du goûter.",
            "maman|Tu le vois, sur la table ?",
            "enfant-m|Oui, il montre un pli.",
            "narrateur|L'éclat d'orange allume une ligne sur le carton.",
            "narrateur|Aniss plie ce bout, sans brusquer.",
            "narrateur|Ça fait un petit clap.",
            "narrateur|Une porte s'ouvre, nette.",
            "narrateur|Il glisse le lapin par la porte.",
            "enfant-m|Il rentre.",
            "maman|Sa maison est prête ?",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "porte",
        [
            "narrateur|Ils restent un moment, sans parler.",
            "narrateur|Le lapin est dans sa maison.",
            "enfant-m|Il a sa porte.",
            "maman|Tu as posé la pelle ?",
            "enfant-m|Oui, près des chaussures.",
            "narrateur|La casquette repose au crochet.",
            "narrateur|L'éclat d'orange reste, pâle, sur le bois.",
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
    if "éclat d'orange" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat d'orange" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé au climax")
    if "éclat d'orange" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
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
        "- **Leçon :** AUT.AFF.003 — reprendre ses affaires avant de partir "
        "(vécue, jamais dite)\n"
        "- **Personnages :** Aniss, maman. Troupe D16.\n"
        "- **Lieu :** cuisine puis parc, fin d'après-midi (coin du banc froid, "
        "table au jus)\n"
        "- **Indice unique :** éclat d'orange (bois de la cuisine → pâle au "
        "retour → ligne sur le carton → pâle sur le bois)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Aniss connaît la cuisine. Un éclat d'orange cligne sur le bois après "
        "le goûter. Il veut **la maison du lapin maintenant**, avec une porte. "
        "Première idée : verser trop vite, pousser le doudou dans le tas. Le "
        "lapin glisse dans l'herbe, oreille pliée. Sourire disparu. Il part "
        "les mains vides. Il revient, reprend pelle, casquette, lapin. Merci "
        "vécu. À la cuisine, il veut glisser le lapin d'un coup : l'oreille "
        "se coince. Il refuse de foncer, retrouve l'éclat, plie une porte, "
        "clap. Retour : pelle près des chaussures, éclat pâle sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine fin d'après-midi, carreaux, fenêtre tiède, parc au "
        "banc froid.\n"
        "- Désir : maison avec porte pour le lapin, maintenant.\n"
        "- Objet : doudou lapin (oreille pliée, mission : une porte avant le "
        "soleil bas).\n"
        "- Indice unique : éclat d'orange, vu dès l'ouverture, payé au climax "
        "et à la fin.\n"
        "- Urgence douce : le soleil baisse, la porte n'est pas finie.\n"
        "- Imprévu 1 : tas trop mou, lapin qui glisse, mains vides.\n"
        "- Cue : maman à la même hauteur, une question. Un merci vécu, après "
        "les affaires.\n"
        "- Imprévu 2 (plus rusé) : oreille coincée dans la boîte ; Aniss veut "
        "pousser plus fort.\n"
        "- Résolution : il refuse de foncer, lit l'éclat, plie la porte, le "
        "lapin rentre.\n"
        "- Retour : pelle près des chaussures, casquette au crochet, éclat "
        "pâle.\n\n"
        "## Vécu\n\n"
        "Aniss veut la maison **maintenant**. Impatience, puis sourire qui "
        "disparaît quand le lapin glisse. Maman se baisse, pose une question, "
        "ne récite pas la règle. Aniss agit : pelle, casquette, lapin. Merci "
        "vécu après les trois. À la cuisine, il refuse de foncer. Fin : "
        "l'éclat du début est pâle sur le bois. La pelle est près des "
        "chaussures.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : cuisine puis parc, fin "
        "d'après-midi. ≠ 003-01 (Raphaël, seau jaune, bac à sable).\n"
        "- Ouverture inventée (lumière sur les carreaux, détail nouveau sur "
        "le bois), pas un gabarit v2, pas « Aniss est dans la cuisine ».\n"
        "- Indice unique : éclat d'orange. Pas écaille d'orange. Pas grain de "
        "miette/foin/feuille/paille/pin/pépin/pomme/sable, pas éclat de "
        "pince/thermos/coquille/bouton/ticket/goutte/boucle/corde/caisse/"
        "marche/caillou/liste/clé/cuillère/sonnette/horloge/tasse, pas trait "
        "de craie/vitre, merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : il reprend pelle, casquette, lapin avant de "
        "partir, les pose. Pas de morale.\n"
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
