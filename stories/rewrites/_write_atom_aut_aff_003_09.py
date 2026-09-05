#!/usr/bin/env python3
"""ATOM-AUT.AFF.003-09 — Les grains du tapis bleu (F-NAR-019, N2, AUT.AFF.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.003-09"
TITLE = "Les grains du tapis bleu"
N2 = LIMITS["N2"]
CHARS = "Chouchou, maman"
SETTING = "entrée, square, puis jardin"
FIL = (
    "Le square a laissé un visiteur dans l'entrée. Un éclat de grain "
    "tient sur le tapis bleu. Chouchou veut la montagne, maintenant. "
    "Elle verse trop vite : le tas tombe. Elle court avec le seau : "
    "l'anse glisse. Elle refuse de foncer, vide le seau, reprend manteau "
    "et ours. Au jardin, la casquette glisse. Elle retrouve l'éclat sur "
    "la gourde. À l'entrée, l'éclat dore sur une patte."
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
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de tasse",
    "éclat d'orange",
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de carreau",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
    "feuille rouge",
    "seau jaune",
    "bac à sable",
    "on reprend ses affaires",
    "avant de partir, on reprend",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de grain",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_montagne_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="partir",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=avant_de_partir_elle_reprend; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="seau",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_reprend_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de grain",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis prudence; intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de grain",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_dore_sur_la_patte; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "reprendre",
    "accepted_examples": "reprendre | ses affaires | il reprend | elle reprend | avant de partir",
    "retry_prompt": "Elle reprend ses affaires. Que fait Chouchou ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "porte,enfants_parc",
        [
            "narrateur|Le square a laissé un visiteur, dans l'entrée.",
            "narrateur|Le tapis bleu garde des grains.",
            "narrateur|Un éclat de grain y tient la lumière.",
            "enfant-f|Il brille, maman.",
            "maman|Tu le vois, Chouchou ?",
            "enfant-f|Oui.",
            "enfant-f|Je veux la montagne, maintenant !",
            "narrateur|Le seau bleu attend près des chaussures.",
            "narrateur|Le manteau gris pend au crochet.",
            "narrateur|L'ours est assis contre le seau.",
            "maman|On va au square ?",
            "enfant-f|Oui, pour la montagne.",
            "narrateur|Chouchou glisse le manteau sur son bras.",
            "enfant-f|J'ai l'ours.",
            "narrateur|Le seau bleu tape sa jambe.",
            "maman|On ouvre ?",
            "enfant-f|Oui.",
            "narrateur|Elles ferment la porte.",
            "narrateur|L'air sent l'herbe, un peu chaude.",
            "narrateur|La rue sent le square, un peu.",
            "narrateur|En ce moment, Chouchou court vers le bac.",
            "narrateur|Le vent fraîchit, et le banc est froid.",
            "narrateur|Maman s'assoit, les mains sur les genoux.",
            "narrateur|Le bac est tiède, au bord.",
            "narrateur|Chouchou pose l'ours dans l'herbe.",
            "narrateur|L'herbe chatouille un peu.",
            "enfant-f|Je remplis le seau, tout de suite.",
            "maman|Tu fais une montagne ?",
            "enfant-f|Une grande, maman.",
            "maman|Je te vois.",
            "narrateur|Elle verse trop vite, d'un coup.",
            "narrateur|Le sable glisse contre le plastique.",
            "narrateur|Ça fait chh, trop fort.",
            "narrateur|La montagne penche, puis tombe.",
            "enfant-f|Oh.",
            "enfant-f|Elle est partie !",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-f|Je prends le seau, et je cours !",
            "narrateur|Elle tire l'anse, d'un coup.",
            "narrateur|L'anse glisse entre ses doigts.",
            "narrateur|Le seau tape le bord du bac.",
            "narrateur|Un filet de sable touche ses chaussures.",
            "enfant-f|Ça ne veut pas, maman.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Maman s'accroupit à sa hauteur.",
            "maman|Tu regardes tes affaires ?",
            "narrateur|Le manteau gris reste sur le banc.",
            "narrateur|L'ours reste dans l'herbe.",
            "enfant-f|Je reviens après !",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Chouchou prépare le retour.",
            "narrateur|Ses affaires attendent au square.",
            "narrateur|Avant de partir, que fait Chouchou ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "seau,banc",
        [
            "enfant-f|J'arrête de tirer.",
            "narrateur|Elle pose le seau près du bac.",
            "enfant-f|Il est trop lourd.",
            "maman|On le vide ici ?",
            "narrateur|Chouchou penche le seau, sans presser.",
            "narrateur|Le sable retombe en filet.",
            "enfant-f|La montagne reste au square.",
            "maman|Oui.",
            "narrateur|Elle reprend le seau bleu.",
            "narrateur|Le manteau gris attend sur le banc.",
            "narrateur|Elle le prend.",
            "narrateur|Le tissu est un peu froid.",
            "maman|Et l'ours ?",
            "enfant-f|Il est dans l'herbe.",
            "narrateur|Chouchou cherche trop vite.",
            "narrateur|L'herbe cache l'ours.",
            "enfant-f|Je ne le vois pas.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Elle s'arrête, les pieds dans l'herbe.",
            "narrateur|Une oreille dépasse, brune.",
            "enfant-f|Le voilà.",
            "narrateur|Elle le prend contre elle.",
            "narrateur|Rien ne reste sur le banc.",
            "maman|Merci, Chouchou.",
            "maman|Tu tiens tout ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le seau tape un peu sa jambe.",
            "narrateur|Le manteau pèse sur son bras.",
            "narrateur|L'ours sent l'herbe, tiède.",
            "enfant-f|On va au jardin ?",
            "maman|Oui.",
            "maman|Un peu plus tard.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "jardin,feuilles",
        [
            "narrateur|Plus tard, le jardin sent l'herbe coupée.",
            "narrateur|Chouchou a une gourde.",
            "narrateur|Elle a une casquette.",
            "narrateur|L'ours est assis près des feuilles.",
            "enfant-f|Je fais le sentier, maintenant !",
            "maman|Avec des feuilles ?",
            "enfant-f|Oui.",
            "narrateur|Elle pose trois feuilles, une par une.",
            "enfant-f|Je bois.",
            "maman|Bien.",
            "narrateur|L'eau fait glouglou.",
            "narrateur|Une abeille passe, loin.",
            "maman|On rentre.",
            "enfant-f|Le chemin n'est pas fini.",
            "maman|On le finira à la maison.",
            "enfant-f|Avec l'ours ?",
            "maman|Avec l'ours.",
            "enfant-f|On y va, maintenant !",
            "narrateur|Elle saisit l'ours d'un coup.",
            "narrateur|La gourde reste près des feuilles.",
            "narrateur|La casquette est son chapeau.",
            "narrateur|Le chapeau glisse, tombe.",
            "narrateur|L'ours penche, presque par terre.",
            "enfant-f|Oh.",
            "narrateur|Le sourire disparaît.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "enfant-f|Pas comme le seau.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Chouchou observe l'ours, puis le jardin.",
            "narrateur|Elle écoute le jardin, un instant.",
            "narrateur|Sur la gourde, un éclat de grain tient.",
            "enfant-f|C'est celui du tapis.",
            "maman|Tu le vois, sur la gourde ?",
            "enfant-f|Oui, il est resté.",
            "narrateur|L'éclat de grain allume le bord de la gourde.",
            "narrateur|Elle reprend la gourde, sans brusquer.",
            "narrateur|Elle remet la casquette.",
            "narrateur|L'ours n'a plus de chapeau.",
            "enfant-f|C'était drôle.",
            "maman|Tu tiens bien tout ?",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "porte,tapis",
        [
            "narrateur|Elles poussent la porte de l'entrée.",
            "narrateur|Le tapis bleu est lisse, presque.",
            "enfant-f|Il a attendu.",
            "maman|Tu poses la gourde ?",
            "narrateur|Chouchou pose la gourde près des chaussures.",
            "narrateur|La casquette rejoint le crochet.",
            "narrateur|Elle assied l'ours sur le tapis.",
            "enfant-f|Il garde l'entrée.",
            "maman|Oui.",
            "narrateur|Les chaussures restent dehors, sages.",
            "narrateur|Un éclat de grain tient sur une patte.",
            "enfant-f|Comme sur le tapis, maman !",
            "maman|Tu l'as vu, toi ?",
            "enfant-f|Il est venu avec nous.",
            "narrateur|Le seau bleu repose près de la porte.",
            "narrateur|Le tapis reste lisse sous les pieds.",
            "narrateur|L'éclat de grain dore sur la patte.",
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
    if "éclat de grain" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de grain" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé au climax")
    if "éclat de grain" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
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
        "- **Personnages :** Chouchou, maman. Troupe D16.\n"
        "- **Lieu :** entrée, square, puis jardin (coin du sentier des "
        "trois feuilles, tapis bleu de l'entrée)\n"
        "- **Indice unique :** éclat de grain (tapis bleu → bord de la "
        "gourde → patte de l'ours)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le square a laissé un visiteur dans l'entrée. Un éclat de grain "
        "tient la lumière sur le tapis bleu. Chouchou veut **la montagne "
        "maintenant**. Première idée : verser trop vite, puis courir avec "
        "le seau plein. L'anse glisse, le sable touche les chaussures. "
        "Sourire disparu. Elle part presque les mains vides. Elle revient, "
        "vide le seau, reprend manteau, ours. Merci vécu. Au jardin, elle "
        "veut le sentier des feuilles, saisit l'ours d'un coup : la "
        "casquette-chapeau glisse. Elle refuse de foncer, retrouve l'éclat "
        "sur la gourde. Retour : chaussures dehors, tapis lisse, éclat doré "
        "sur une patte.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : entrée au tapis bleu, square au bac tiède, jardin à "
        "l'herbe coupée.\n"
        "- Désir : une montagne au square, maintenant, puis un sentier de "
        "feuilles.\n"
        "- Objet : seau bleu, ours, gourde, casquette (mission : ramener "
        "la montagne sans porter le square sur le tapis).\n"
        "- Indice unique : éclat de grain, vu dès l'ouverture, payé au "
        "climax et à la fin.\n"
        "- Urgence douce : la montagne tombe, le sentier n'est pas fini.\n"
        "- Imprévu 1 : tas trop vite, anse qui glisse, mains vides.\n"
        "- Cue : maman à la même hauteur, une question. Un merci vécu, "
        "après les affaires.\n"
        "- Imprévu 2 (plus rusé) : casquette-chapeau qui glisse ; Chouchou "
        "veut partir avec l'ours seul.\n"
        "- Résolution : elle refuse de foncer, lit l'éclat, reprend gourde "
        "et casquette.\n"
        "- Retour : chaussures dehors, ours sur le tapis, éclat sur la "
        "patte.\n\n"
        "## Vécu\n\n"
        "Chouchou veut la montagne **maintenant**. Impatience, puis sourire "
        "qui disparaît quand l'anse glisse. Maman se baisse, pose une "
        "question, ne récite pas la règle. Chouchou agit : seau vidé, "
        "manteau, ours. Merci vécu après les trois. Au jardin, elle refuse "
        "de foncer. Fin : l'éclat du début dore sur la patte. Le tapis "
        "reste lisse.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : entrée, square, puis jardin. "
        "≠ 003-01 (Raphaël, seau jaune, grain de sable). ≠ 002-01 (feuille "
        "rouge, trait de vitre).\n"
        "- Ouverture inventée (le square a laissé un visiteur), pas un "
        "gabarit v2, pas « Chouchou est dans l'entrée ». Dump « Encore un "
        "grain » jeté.\n"
        "- Indice unique : éclat de grain. Pas grain de "
        "miette/foin/feuille/paille/pin/pépin/pomme/sable, pas éclat de "
        "pince/thermos/coquille/bouton/ticket/goutte/boucle/corde/caisse/"
        "marche/caillou/liste/clé/cuillère/sonnette/horloge/tasse/orange/"
        "colle/lessive/vitre/casserole/carreau, pas point de gouttière, "
        "pas trait de craie/vitre, merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : elle vide le seau, reprend manteau et ours, "
        "puis gourde et casquette. Pas de morale.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée (reprendre). 5 chunks, kinds inchangés.\n"
        "- Genre D16 : Chouchou = enfant-f.\n"
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
