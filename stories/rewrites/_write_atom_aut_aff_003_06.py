#!/usr/bin/env python3
"""ATOM-AUT.AFF.003-06 — Les gouttes du seau vert (F-NAR-019, N1, AUT.AFF.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.003-06"
TITLE = "Les gouttes du seau vert"
N1 = LIMITS["N1"]
CHARS = "Sarah, maman"
SETTING = "rebord de fenêtre puis jardin après la pluie"
FIL = (
    "Le zinc tic. Un point de gouttière brille sous une goutte. Sarah "
    "veut l'eau maintenant, dans le seau vert, pour le doudou. Elle "
    "pousse trop vite : l'eau gicle, le seau reste vide. Elle refuse "
    "de forcer, reprend seau, manteau, doudou. Au jardin, le seau penche. "
    "Elle refuse de foncer, retrouve le point. L'eau paie le début."
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
    "éclat de cuillère",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de tasse",
    "éclat d'orange",
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "trait de craie",
    "trait de vitre",
    "seau jaune",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="point de gouttière",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_l_eau_maintenant; "
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
            "intensite=1; destinataire=enfant; sous_texte=elle_reprend_avant_de_partir; "
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
        emphasis="point de gouttière",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis prudence; intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_retrouve_le_point; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="point de gouttière",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_point_de_gouttiere_est_sur_l_eau; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "reprendre",
    "accepted_examples": "reprendre | ses affaires | il reprend | elle reprend | avant de partir",
    "retry_prompt": "Elle reprend ses affaires. Que fait Sarah ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "gouttiere,goutte,seau",
        [
            "narrateur|Le zinc de la gouttière fait tic.",
            "narrateur|Une goutte y tient, ronde.",
            "narrateur|Sous la goutte, un point de gouttière brille.",
            "narrateur|Sarah connaît ce rebord, après la pluie.",
            "narrateur|Le bois du rebord est froid.",
            "narrateur|Ça sent le bois mouillé.",
            "narrateur|Derrière la vitre, le jardin luisant attend.",
            "narrateur|Maman essuie le rebord, sans presser.",
            "narrateur|Un carré de ciel pâle touche le zinc.",
            "enfant-f|Maman, le point brille !",
            "maman|Oui.",
            "maman|Il est sur le zinc.",
            "narrateur|La cuvette grise attend dessous.",
            "narrateur|Plic.",
            "narrateur|La goutte tombe dans la cuvette.",
            "narrateur|Un seau vert dort près des bottes.",
            "narrateur|Les bottes de Sarah sont rouges.",
            "narrateur|Le doudou beige est sur la chaise.",
            "narrateur|Un manteau rouge pend au crochet.",
            "enfant-f|Je veux l'eau, maintenant !",
            "enfant-f|Pour lui, dans le seau !",
            "maman|Tu la veux vite ?",
            "enfant-f|Oui, maman.",
            "narrateur|En ce moment, Sarah saisit le seau vert.",
            "narrateur|Le plastique est froid, un peu rêche.",
            "narrateur|Elle court vers le rebord.",
            "narrateur|Le seau tape contre sa jambe.",
            "enfant-f|Je le mets sous le zinc !",
            "narrateur|Elle pousse le seau, trop vite.",
            "narrateur|L'eau gicle sur le bois.",
            "enfant-f|Oh.",
            "narrateur|Le seau reste presque vide.",
            "narrateur|Une manche du manteau tombe.",
            "narrateur|Le manteau rouge glisse du crochet.",
            "narrateur|Le doudou beige roule vers le pot.",
            "enfant-f|Ça ne veut pas.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, envie et inquiétude se bousculent.",
            "narrateur|Maman se baisse à sa hauteur.",
            "maman|Tu regardes le seau ?",
            "narrateur|Sarah ramasse le seau, sans crier.",
            "enfant-f|Je le reprends.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Avant de partir, que fait Sarah ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "manteau,doudou,bottes",
        [
            "narrateur|Sarah refuse de pousser plus fort.",
            "narrateur|Elle pose un genou au sol.",
            "narrateur|Le seau vert est froid, vide.",
            "enfant-f|Je le tiens.",
            "maman|Le manteau, près du crochet ?",
            "narrateur|Sarah se penche.",
            "narrateur|Le manteau rouge est un peu mouillé.",
            "narrateur|Elle le prend, sans tirer.",
            "enfant-f|Le manteau.",
            "maman|Oui.",
            "narrateur|Le doudou beige attend près du pot.",
            "enfant-f|Toi aussi.",
            "narrateur|Elle le ramasse, une oreille mouillée.",
            "enfant-f|Son oreille est froide.",
            "maman|Tu le serres ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sarah appuie le seau contre sa hanche.",
            "narrateur|Le plastique fait un petit clic.",
            "maman|On met tes bottes ?",
            "narrateur|Sarah enfile ses bottes rouges.",
            "narrateur|Une semelle est froide.",
            "maman|Tu as fini tes bottes ?",
            "enfant-f|Oui, maman.",
            "maman|Tu tiens tout ?",
            "enfant-f|Oui.",
            "maman|Merci, Sarah.",
            "maman|Le seau est prêt ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sarah pose la main sur le bord.",
            "narrateur|Le bord est un peu rêche.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "porte,jardin,gouttiere",
        [
            "maman|On ouvre la porte ?",
            "enfant-f|Oui.",
            "enfant-f|Pour l'eau du tuyau.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|L'air sent la terre mouillée.",
            "narrateur|Le jardin luisant s'ouvre.",
            "narrateur|Un tuyau de zinc pend au mur.",
            "narrateur|Sarah marche près de maman.",
            "narrateur|L'herbe est un peu froide.",
            "enfant-f|Je le vois !",
            "narrateur|Le tuyau laisse une goutte, lente.",
            "narrateur|Elle tend le seau, trop vite.",
            "narrateur|Le seau penche.",
            "narrateur|L'eau tombe à côté, dans l'herbe.",
            "enfant-f|Elle part !",
            "narrateur|Sarah veut foncer, sous le tuyau.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Ses épaules se serrent un peu.",
            "narrateur|Ça tape, dans sa poitrine.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle lève les yeux vers le zinc.",
            "narrateur|Un point de gouttière brille, dehors.",
            "enfant-f|Comme au rebord !",
            "maman|Tu le vois, toi ?",
            "enfant-f|Oui, sur ce tuyau.",
            "narrateur|Sarah s'accroupit, lente.",
            "narrateur|Elle écoute le jardin, un instant.",
            "narrateur|Une goutte tic, plus loin.",
            "narrateur|Elle tient le seau, sans bouger.",
            "narrateur|La goutte tombe au fond.",
            "narrateur|Ça fait ploc.",
            "enfant-f|Ploc, maman.",
            "maman|Tu le tiens sans presser ?",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "soucoupe,eau,doudou",
        [
            "narrateur|Sarah tient le seau, un peu plein.",
            "narrateur|L'eau tremble, claire.",
            "enfant-f|Elle brille, maman.",
            "maman|Tu la portes à la maison ?",
            "enfant-f|Oui.",
            "narrateur|Elles rentrent dans la maison.",
            "narrateur|La maison est tiède.",
            "narrateur|Sarah pose le seau près de la cuvette.",
            "maman|On donne de l'eau au doudou ?",
            "enfant-f|Oui, maman.",
            "narrateur|Maman prend une soucoupe.",
            "narrateur|Sarah verse une goutte.",
            "narrateur|Ploc.",
            "enfant-f|Il boit.",
            "narrateur|Le doudou beige a le museau frais.",
            "enfant-f|Comme sur le zinc, maman.",
            "narrateur|Sur l'eau, un point de gouttière dore.",
            "maman|Tu le vois, sur l'eau ?",
            "enfant-f|Oui.",
            "enfant-f|C'est mon seau vert.",
            "narrateur|La soucoupe garde la goutte.",
            "narrateur|Le point de gouttière dore, mince.",
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
    if "point de gouttière" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "point de gouttière" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
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
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** AUT.AFF.003 — reprendre ses affaires (vécue, jamais dite)\n"
        "- **Personnages :** Sarah, maman. Troupe D16.\n"
        "- **Lieu :** rebord de fenêtre puis jardin après la pluie "
        "(cuvette, tuyau de zinc)\n"
        "- **Indice unique :** point de gouttière (zinc du rebord → tuyau "
        "du jardin → dore sur l'eau de la soucoupe)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le zinc tic. Une goutte tient. Un point de gouttière brille. Sarah "
        "connaît ce rebord, après la pluie. Elle veut l'eau **maintenant**, "
        "dans le seau vert, pour le doudou beige. Elle pousse trop vite sous "
        "le zinc : l'eau gicle, le seau reste vide. Manteau à terre, doudou "
        "vers le pot. Première idée ratée. Sourire parti. Maman se baisse, "
        "pose une question. Sarah ramasse, dit « je le reprends ». Merci "
        "vécu après bottes, manteau, doudou. Au jardin, elle tend trop vite : "
        "le seau penche. Elle refuse de foncer, retrouve le point du rebord. "
        "Elle tient sans bouger. Ploc. La soucoupe paie le début : le point "
        "de gouttière dore, mince, sur l'eau.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : rebord froid, zinc, cuvette grise, jardin luisant.\n"
        "- Désir : l'eau de la gouttière, maintenant, dans le seau vert.\n"
        "- Objet : seau vert, manteau rouge, doudou beige, bottes rouges.\n"
        "- Indice unique : point de gouttière, vu dès l'ouverture, payé au climax.\n"
        "- Urgence douce : l'eau pour le doudou, tout de suite.\n"
        "- Imprévu 1 : trop vite sous le zinc, seau vide, affaires à terre.\n"
        "- Cue : maman à la même hauteur, une question. Un merci vécu, après "
        "les affaires dans les bras.\n"
        "- Imprévu 2 (plus rusé) : le seau penche sous le tuyau ; Sarah veut "
        "foncer.\n"
        "- Résolution : elle refuse de foncer, lit le point, tient sans bouger.\n"
        "- Retour : goutte dans la soucoupe, point doré sur l'eau.\n\n"
        "## Vécu\n\n"
        "Sarah veut l'eau **maintenant**. Impatience, puis sourire qui "
        "disparaît quand le seau reste vide. Maman se baisse, pose une "
        "question, ne récite pas la règle. Sarah agit : genou au sol, seau, "
        "manteau, doudou, bottes. Merci vécu après « tu tiens tout ». Au "
        "jardin, elle refuse de foncer. Fin : le point du début dore sur "
        "l'eau. Seau vert, pas jaune. Pas de ferme, pas de sable.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu : rebord de fenêtre puis jardin après "
        "la pluie. ≠ ATOM-AUT.AFF.003-01 (seau jaune, Raphaël, parc, sable). "
        "≠ TREE-AUT-011 (seau jaune, Sarah, ferme, grain de paille).\n"
        "- Ouverture inventée (le zinc tic, goutte ronde), pas un gabarit v2, "
        "pas « Sarah est au jardin ».\n"
        "- Indice unique : point de gouttière. Pas grain de miette/foin/"
        "feuille/paille/pin/pépin/pomme/sable, pas éclat de pince/thermos/"
        "coquille/bouton/ticket/goutte/boucle/corde/caisse/marche/caillou/"
        "liste/clé/cuillère/sonnette/horloge/tasse/orange/colle/lessive/vitre, "
        "pas trait de craie/vitre, merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : elle reprend seau, manteau, doudou, bottes. "
        "Pas de morale.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée (reprendre). 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle plus tendu. Action plus vive à l'ouverture.\n"
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
