#!/usr/bin/env python3
"""ATOM-AUT.AFF.002-06 — Le sac à pain de Nino (F-NAR-019, N3, AUT.AFF.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.002-06"
TITLE = "Le sac à pain de Nino"
N3 = LIMITS["N3"]
CHARS = "Nino, maman"
SETTING = "cuisine, jardin, boulangerie"
FIL = (
    "Le tic de l'horloge répond dans le cuivre. Un éclat d'horloge cligne "
    "sur le sac à pain vide. Nino veut le pain du fournil, maintenant. Il "
    "court sans manteau : le sac accroche le crochet, tombe. Il refuse de "
    "forcer, enfile le gris, passe au thym. Au fournil, il pousse trop vite. "
    "Il refuse de foncer, retrouve l'éclat sur la croûte. Le sac paie le début."
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
    "pain doré",
    "pain dore",
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "grain de pomme",
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
    "trait de craie",
    "trait de vitre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat d'horloge",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_pain_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="sortir",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; sous_texte=le_manteau_avant_la_porte; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="manteau",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_prend_le_manteau_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat d'horloge",
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
        emphasis="éclat d'horloge",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_cadran_est_sur_la_croute; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "manteau",
    "accepted_examples": "manteau | le manteau | son manteau",
    "retry_prompt": "Il prend le manteau. Que prend Nino ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "horloge,casserole,porte",
        [
            "narrateur|Le tic de l'horloge répond dans le cuivre de la casserole.",
            "narrateur|La casserole est vide, froide sous le doigt.",
            "narrateur|Nino connaît cette cuisine, ses recoins.",
            "narrateur|Un filet de farine dessine un chemin sur la table.",
            "narrateur|Sur la chaise, un sac à pain pend, vide.",
            "narrateur|Le lin du sac sent la farine sèche.",
            "narrateur|Un éclat d'horloge cligne sur le lin.",
            "narrateur|Nino ne sait pas à quoi il servira.",
            "narrateur|Maman plie le torchon, près de la planche.",
            "narrateur|Le torchon sent le levain.",
            "narrateur|La porte du jardin laisse un filet d'air.",
            "narrateur|Ça sent le fournil du village.",
            "maman|Nino, tu as vu le sac vide ?",
            "enfant-m|Oui.",
            "enfant-m|Il n'y a plus de pain.",
            "enfant-m|Je veux le pain, maintenant !",
            "maman|On y va, avec le sac.",
            "narrateur|En ce moment, Nino saisit le sac vide.",
            "narrateur|Le lin est rêche sous les doigts.",
            "narrateur|Son manteau gris attend au crochet.",
            "narrateur|Les pieds de Nino tapent le carrelage.",
            "enfant-m|Je sors, maman !",
            "narrateur|Nino court vers la porte du jardin.",
            "narrateur|Il veut le pain, sans attendre.",
            "narrateur|Le sac accroche le crochet, d'un coup.",
            "enfant-m|Oh.",
            "narrateur|Nino tire plus fort.",
            "narrateur|Le sac tombe, plat, sur le carrelage.",
            "enfant-m|Ça reste coincé !",
            "narrateur|La sangle reste tordue, près du crochet.",
            "narrateur|Le manteau gris n'a pas bougé.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|L'air du jardin pique les poignets, sans manteau.",
            "narrateur|Maman se baisse à sa hauteur.",
            "maman|Tu regardes le crochet ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino veut sortir.",
            "narrateur|Avant de sortir, que prend Nino ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "manteau,jardin,arrosoir",
        [
            "narrateur|Nino refuse de tirer plus fort.",
            "narrateur|Il pose un genou au carrelage.",
            "narrateur|Le sac est plat, la sangle tordue.",
            "enfant-m|Je le pose.",
            "narrateur|Il pose le sac sur la chaise.",
            "narrateur|Le crochet montre le manteau gris.",
            "maman|Tu le prends, Nino ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nino glisse un bras, puis l'autre.",
            "narrateur|Le tissu est épais, un peu rêche.",
            "narrateur|Les boutons sont froids sous le doigt.",
            "maman|Merci, Nino.",
            "maman|Le manteau est prêt ?",
            "enfant-m|Oui, maman.",
            "narrateur|Maman lace les chaussures, sans se presser.",
            "maman|On ouvre le jardin ?",
            "enfant-m|Oui.",
            "narrateur|Ils passent la porte du jardin.",
            "narrateur|L'air pique les joues, pas les poignets.",
            "enfant-m|J'ai chaud, maman.",
            "maman|Tu le sens sur tes bras ?",
            "enfant-m|Oui.",
            "narrateur|Un arrosoir goutte près du thym.",
            "narrateur|Le thym sent fort, près de la grille.",
            "enfant-m|Il goutte, maman.",
            "maman|Tu l'entends, Nino ?",
            "narrateur|Nino écoute la goutte, un instant.",
            "narrateur|La grille du jardin grince, un peu.",
            "maman|On rentre.",
            "narrateur|Nino entre.",
            "narrateur|Il retire le manteau gris.",
            "narrateur|Il le raccroche au crochet.",
            "enfant-m|Il est à sa place.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "porte,fournil,pelle",
        [
            "maman|On prend le sac, Nino ?",
            "enfant-m|Le pain, maintenant.",
            "narrateur|Maman prend le sac vide.",
            "narrateur|Nino va vers le crochet, seul.",
            "narrateur|Il prend le manteau gris.",
            "enfant-m|Le manteau, maman.",
            "maman|Tu l'as pris, toi.",
            "narrateur|Ils traversent le jardin, puis la rue.",
            "narrateur|Le fournil sent le chaud, si près.",
            "enfant-m|Je le prends !",
            "narrateur|Nino pousse la porte, trop vite.",
            "narrateur|Le sac se coince dans le battant.",
            "enfant-m|Oh.",
            "narrateur|Il veut foncer vers le pain chaud.",
            "narrateur|Nino refuse de foncer.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Au-dessus du comptoir, un cadran brille.",
            "narrateur|Un éclat d'horloge cligne sur la croûte.",
            "enfant-m|Comme à la cuisine !",
            "maman|Tu le vois, toi ?",
            "enfant-m|Oui, sur ce pain.",
            "narrateur|Nino s'arrête, lent.",
            "narrateur|Il écoute le fournil, un instant.",
            "narrateur|Une pelle racle la pierre, plus loin.",
            "narrateur|Le pain attend derrière le bois.",
            "maman|On le prend ensemble ?",
            "enfant-m|Celui-là.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "sac,crochet",
        [
            "narrateur|Maman glisse le pain dans le sac.",
            "narrateur|Le lin se tend, un peu chaud.",
            "enfant-m|Il sent le fournil, maman.",
            "maman|Tu le portes, toi ?",
            "enfant-m|Oui, contre moi.",
            "narrateur|Nino serre le sac contre le manteau.",
            "narrateur|Sur la croûte, l'éclat d'horloge reste.",
            "enfant-m|Comme sur le lin, maman.",
            "maman|Tu le ramènes à la maison ?",
            "enfant-m|Oui.",
            "narrateur|Ils rentrent par le jardin.",
            "narrateur|Nino raccroche le manteau au crochet.",
            "narrateur|Le sac repose sur la chaise.",
            "enfant-m|Il n'est plus vide.",
            "maman|Tu as fini de poser le sac ?",
            "enfant-m|Oui, maman.",
            "narrateur|L'éclat d'horloge laisse une trace claire, sur la croûte.",
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
    if "éclat d'horloge" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat d'horloge" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
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
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** AUT.AFF.002 — prendre le manteau (vécue, jamais dite)\n"
        "- **Personnages :** Nino, maman. Troupe D16.\n"
        "- **Lieu :** cuisine, jardin, boulangerie (fournil du village, "
        "coin du thym). ≠ ATOM-AUT.AFF.002-03 (pain doré, hall, rue, vitrine). "
        "≠ ATOM-AUT.AFF.001-01 (four, grain de miette).\n"
        "- **Indice unique :** éclat d'horloge (cadran de cuisine → cadran "
        "du fournil → trace claire sur la croûte)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le tic de l'horloge répond dans le cuivre vide. Un éclat d'horloge "
        "cligne sur le sac à pain. Nino veut le pain du fournil **maintenant**. "
        "Il saisit le sac, court sans manteau. Le sac accroche le crochet, "
        "tombe. Première idée ratée. Sourire disparu. Maman se baisse. Il "
        "refuse de forcer, pose le sac, enfile le gris. Merci vécu. Au jardin, "
        "l'air pique les joues, pas les poignets. Il raccroche. Au fournil, "
        "il pousse trop vite : le sac se coince. Il refuse de foncer, retrouve "
        "l'éclat du cadran sur la croûte. Le sac plein paie le début : l'éclat "
        "laisse une trace claire sur la croûte.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine, casserole de cuivre, farine, cadran, porte du jardin.\n"
        "- Désir : le pain du fournil, maintenant, dans le sac à pain.\n"
        "- Objet : sac de lin, manteau gris, arrosoir, thym.\n"
        "- Indice unique : éclat d'horloge, vu dès l'ouverture, payé au climax.\n"
        "- Urgence douce : plus de pain, le fournil sent si près.\n"
        "- Imprévu 1 : il court sans manteau ; le sac accroche, tombe.\n"
        "- Cue : maman à la même hauteur, une question. Un merci vécu, après "
        "le manteau enfilé.\n"
        "- Imprévu 2 (plus rusé) : il pousse la porte du fournil trop vite ; "
        "le sac se coince dans le battant.\n"
        "- Résolution : il refuse de foncer, lit l'éclat, choisit le pain.\n"
        "- Retour : pain dans le sac, manteau au crochet, éclat en trace "
        "claire sur la croûte.\n\n"
        "## Vécu\n\n"
        "Nino veut le pain **maintenant**. Impatience (pieds qui tapent), "
        "puis sourire qui disparaît quand le sac tombe. Maman se baisse, "
        "pose une question, ne récite pas la règle. Nino agit : genou au "
        "sol, sac sur la chaise, manteau, jardin. Merci vécu après "
        "l'enfilage. Au fournil, il refuse de foncer. Fin : l'éclat du "
        "début est sur la croûte. Pas de pain doré. Pas de grain de miette. "
        "Pas de four du village comme destination.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu : cuisine, jardin, boulangerie. "
        "≠ ATOM-AUT.AFF.002-03 (Sarah, hall, rue, vitrine, pain doré). "
        "≠ ATOM-AUT.AFF.001-01 (Amir, four, grain de miette).\n"
        "- Ouverture inventée (tic dans le cuivre), pas un gabarit v2, pas "
        "« Nino est dans la cuisine ».\n"
        "- Indice unique : éclat d'horloge. Pas grain de miette/foin/feuille/"
        "paille/pin/pépin/pomme, pas éclat de pince/thermos/coquille/bouton/"
        "ticket/goutte/boucle/corde/caisse/marche/caillou/liste/clé/cuillère/"
        "sonnette, pas trait de craie/vitre, merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : il prend le manteau, deux sorties. Pas de morale.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée (manteau). 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle plus tendu. Action plus vive à l'ouverture.\n"
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
