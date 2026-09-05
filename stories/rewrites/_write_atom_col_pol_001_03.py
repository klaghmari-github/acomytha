#!/usr/bin/env python3
"""ATOM-COL.POL.001-03 — Le livre de trains d'Aniss (F-NAR-019, N3, COL.POL.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.POL.001-03"
TITLE = "Le livre de trains d'Aniss"
N3 = LIMITS["N3"]
CHARS = "Aniss, papa, maman"
SETTING = "bibliothèque puis marché"
INDICE = "éclat de parapluie"
FIL = (
    "Une goutte court sur le tissu sombre. Sur le parapluie fermé, un "
    "éclat de parapluie brille. Aniss veut le livre de trains, maintenant. "
    "Il parle trop vite : les mots se cognent au tampon. La dame ne lève "
    "pas les yeux. Sourire parti. Papa se baisse. Bonjour, s'il te plaît, "
    "merci vécus. Au marché, le papier mouillé glisse. Il refuse de foncer. "
    "Sur le tissu, l'éclat de parapluie tient."
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
    "maîtresse",
    "maitresse",
    "malik",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai dit bonjour",
    "j'ai dit s'il te plaît",
    "j'ai dit s'il te plait",
    "j'ai dit merci",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "les trois mots",
    "tu as dit les mots",
    "tu te souviens des mots",
    "on dit bonjour d'abord",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "tu attends ton tour",
    "crayon",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "éclat de seau",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de pompon",
    "éclat de carotte",
    "éclat de carton",
    "éclat de mousse",
    "éclat de laine",
    "éclat de tasse",
    "éclat de crayon",
    "éclat de cartable",
    "éclat de casserole",
    "éclat de nappe",
    "éclat de wagon",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de pinceau",
    "éclat de ballon",
    "éclat de manteau",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de parapluie",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_livre_de_trains_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="dame",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_parle_a_la_dame_avec_bonjour; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="bonjour",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=bonjour_s_il_te_plait_merci_vecus; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="papier mouillé",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_sur_la_poire; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de parapluie",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_tissu; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "bonjour",
    "accepted_examples": (
        "bonjour | s'il te plaît | merci | bonjour merci | s'il vous plaît"
    ),
    "retry_prompt": "Il dit bonjour. Quels mots dit-il ?",
    "engine_ok_text": "Oui, bonjour.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "pluie,parapluie",
        [
            "narrateur|Une goutte court sur le tissu sombre.",
            "narrateur|Un parapluie fermé penche vers le zinc.",
            "narrateur|Les parapluies gouttent dans un seau de zinc.",
            "narrateur|Ça sent le papier mouillé et le bois.",
            "narrateur|Une lampe pose un rond jaune sur une table.",
            "narrateur|Le tapis est épais, un peu rêche sous les bottes.",
            "narrateur|Les étagères montent jusqu'au plafond.",
            "narrateur|Sur le tissu, un éclat de parapluie brille.",
            "enfant-m|Il brille, papa.",
            "papa|C'est l'eau, sous la lumière.",
            "narrateur|Papa tient la main d'Aniss.",
            "papa|Ta main est bien dans la mienne.",
            "maman|Le foulard bleu sèche près du radiateur.",
            "narrateur|Le foulard est lourd d'eau de pluie.",
            "enfant-m|Je veux un livre de trains !",
            "maman|Celui avec la locomotive ?",
            "enfant-m|Oui, tout de suite !",
            "narrateur|En ce moment, Aniss s'arrête près d'une étagère basse.",
            "narrateur|Ses doigts glissent sur les couvertures lisses.",
            "narrateur|Les dos des livres sont verts, rouges, bruns.",
            "narrateur|Une horloge pousse un tic, au fond.",
            "papa|Tu entends l'horloge, Aniss ?",
            "enfant-m|Tic.",
            "enfant-m|Tac.",
            "maman|On est au chaud, ici.",
            "enfant-m|Maman, un train.",
            "enfant-m|Il est rouge.",
            "maman|Celui avec la locomotive.",
            "papa|On s'approche du bureau.",
            "narrateur|La dame tamponne des cartes.",
            "narrateur|Un tampon repose près d'une pile de cartes.",
            "narrateur|Le tampon fait toc, toc.",
            "narrateur|Le livre rouge est sur le chariot.",
            "narrateur|Juste derrière le bureau de bois.",
            "enfant-m|Le train !",
            "narrateur|Les mots d'Aniss se cognent au tampon.",
            "narrateur|La dame ne lève pas les yeux.",
            "narrateur|Ses mains sont pleines de cartes.",
            "enfant-m|Oh.",
            "narrateur|L'éclat de parapluie tremble, puis tient.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et l'inquiétude se heurtent.",
            "enfant-m|Elle ne me voit pas, papa.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|Le livre est derrière le bois ?",
            "enfant-m|Oui, papa.",
            "narrateur|Aniss montre le livre rouge, avec une locomotive.",
            "maman|Tu parles à la dame, Aniss.",
            "narrateur|Le tampon se pose enfin.",
            "narrateur|La dame lève les yeux.",
            "enfant-m|Il est là.",
            "papa|Elle te regarde, Aniss ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss parle à la dame.",
            "narrateur|Quels mots dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "papier,livre",
        [
            "enfant-m|Le train.",
            "narrateur|Aniss referme la bouche.",
            "narrateur|Aniss refuse de foncer.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le tampon, un instant.",
            "narrateur|Il écoute le silence du bureau.",
            "enfant-m|Bonjour.",
            "papa|Bonjour.",
            "enfant-m|Le livre de trains, s'il te plaît.",
            "enfant-m|Celui avec la locomotive.",
            "narrateur|La dame tend le livre rouge.",
            "narrateur|La couverture est lisse, un peu froide.",
            "enfant-m|Merci.",
            "papa|Merci, Aniss.",
            "narrateur|Aniss ouvre une page.",
            "narrateur|Un train bleu roule sur un pont.",
            "enfant-m|Il est tout bleu, papa.",
            "papa|Oui.",
            "narrateur|Aniss tourne une page, sans se presser.",
            "enfant-m|Le pont est petit.",
            "papa|Il tient au-dessus de l'eau.",
            "maman|Tu l'as dans les mains.",
            "narrateur|Ils restent sous la lampe jaune.",
            "narrateur|La pluie continue contre la vitre.",
            "narrateur|Le papier sent le neuf.",
            "enfant-m|Il roule sur le pont.",
            "maman|On le voit bien.",
            "narrateur|Aniss serre le livre contre son manteau.",
            "papa|Le foulard est près de la porte.",
            "enfant-m|On sort, maman ?",
            "maman|Oui, avec le livre.",
            "narrateur|Le seau de zinc est plein de gouttes.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "poire,marche",
        [
            "narrateur|Ils sortent, le livre sous le bras.",
            "narrateur|Les bottes sonnent sur les dalles mouillées.",
            "narrateur|Le marché est plus loin, sous une bâche claire.",
            "narrateur|Ça sent les poires et la terre humide.",
            "narrateur|Les caisses sont mouillées, luisantes.",
            "enfant-m|Une poire jaune !",
            "maman|Celle-là, bien ronde ?",
            "enfant-m|Oui, maman.",
            "narrateur|Aniss tend la main trop vite.",
            "narrateur|Le papier mouillé glisse sous ses doigts.",
            "narrateur|La poire penche, puis retombe.",
            "enfant-m|Oh.",
            "narrateur|Aniss s'arrête.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Aniss refuse de foncer.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe la caisse, un instant.",
            "narrateur|Il écoute la pluie sur la bâche.",
            "narrateur|Sur le parapluie de papa, l'éclat de parapluie brille.",
            "enfant-m|Bonjour.",
            "narrateur|Le marchand incline la tête.",
            "enfant-m|Une poire, s'il te plaît.",
            "narrateur|Le marchand pose la poire dans un petit sac.",
            "narrateur|Le sac est un peu rêche.",
            "enfant-m|Merci.",
            "maman|On rentre, maintenant.",
            "papa|Tu tiens le livre des deux mains ?",
            "enfant-m|Oui, papa.",
            "narrateur|Aniss tient le livre sous le bras.",
            "narrateur|Il tient le sac de l'autre main.",
            "narrateur|La poire sent le sucré, près du nez.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "parapluie",
        [
            "narrateur|Ils rentrent sous un parapluie partagé.",
            "narrateur|Les gouttes tapent le tissu, une par une.",
            "narrateur|À la maison, maman pose le livre sur la table.",
            "narrateur|Aniss pose la poire dans une assiette.",
            "maman|Tu veux un bout de poire ?",
            "enfant-m|Oui, maman.",
            "narrateur|La poire est juteuse, un peu froide.",
            "enfant-m|Comme tout à l'heure, papa !",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur le tissu.",
            "maman|On est bien, ici.",
            "narrateur|Aniss glisse le parapluie près de la porte.",
            "narrateur|Le tissu repose contre le zinc.",
            "enfant-m|On le voit, maman.",
            "maman|Tu le vois sur le tissu ?",
            "enfant-m|Oui, l'éclat.",
            "narrateur|Le train bleu attend sur la page.",
            "narrateur|La pluie finit, plus loin.",
            "narrateur|L'éclat de parapluie tient sur le tissu.",
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
    if "papier mouillé" not in blob:
        raise SystemExit(f"{SID}: manque papier mouillé")
    if "seau de zinc" not in blob:
        raise SystemExit(f"{SID}: manque seau de zinc")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m") for r in roles):
        raise SystemExit(f"{SID}: rôle hors papa/maman")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    enfant_p0 = " ".join(
        ln.split("|", 1)[1]
        for ln in by["CHK_T0000_P0000"]["script"].splitlines()
        if ln.startswith("enfant-")
    ).lower()
    if "s'il te plaît" in enfant_p0 or "s'il te plait" in enfant_p0:
        raise SystemExit(f"{SID}: s'il te plaît déjà dans P0000")
    if re.search(r"\bbonjour\b", enfant_p0):
        raise SystemExit(f"{SID}: bonjour enfant déjà dans P0000")
    q_text = by["CHK_T0000_P0000_Q0001"]["text"]
    if q_text != "Aniss parle à la dame. Quels mots dit-il ?":
        raise SystemExit(f"{SID}: question labels changés: {q_text}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "bonjour":
        raise SystemExit(f"{SID}: expected_answer ≠ bonjour")
    c1 = by["CHK_T0000_P0000_C0001"]["script"].lower()
    if "bonjour" not in c1 or "s'il te plaît" not in c1 or "merci" not in c1:
        raise SystemExit(f"{SID}: leçon non vécue dans C0001")
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
        "- **Leçon :** COL.POL.001 — bonjour / s'il te plaît / merci (vécus : "
        "veut le livre maintenant ; parle trop vite ; tampon toc-toc ; dame "
        "sans les yeux ; refuse de foncer ; bonjour ; s'il te plaît ; merci ; "
        "au marché le papier mouillé glisse ; mêmes mots vécus)\n"
        "- **Personnages :** Aniss, papa, maman. Troupe D16. Dump Malik → "
        "Aniss. Papa ajouté. La dame = label du dump (tampon, chariot, tend "
        "le livre), pas de réplique, pas de leçon récitée. Marchand = geste "
        "du lieu (incline la tête, pose la poire), muet. Adultes parlants = "
        "papa/maman.\n"
        "- **Lieu :** bibliothèque puis marché. Pluie, parapluies, seau de "
        "zinc, papier mouillé, lampe jaune, foulard bleu, livre de trains, "
        "poire. ≠ POL.001-01 (pain/pavé) ≠ POL.001-02 (citron/zeste). Pas "
        "boutique de crayons.\n"
        "- **Indice unique :** éclat de parapluie (tissu dès l'ouverture → "
        "tremble au tampon → brille sur le parapluie de papa → tient sur le "
        "tissu). Pas éclat de seau (BAN 002-02). Pas éclat de pavé. Pas "
        "éclat de zeste.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte court sur le tissu sombre. Sur le parapluie fermé, un "
        "éclat de parapluie brille. Aniss veut le livre de trains "
        "**maintenant**. Il crie le train : les mots se cognent au tampon. "
        "La dame ne lève pas les yeux. Sourire parti, épaules basses. Papa "
        "se baisse. Il refuse de foncer, dit bonjour, s'il te plaît, merci. "
        "Le livre rouge arrive. Merci vécu. Au marché, il tend trop vite : "
        "le papier mouillé glisse, la poire retombe. Il observe, écoute la "
        "bâche, retrouve l'éclat. Bonjour, s'il te plaît, merci. Sur le "
        "tissu, l'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : bibliothèque sous la pluie, zinc, parapluies, papier "
        "mouillé, lampe jaune, tapis rêche, foulard, horloge, puis marché "
        "sous la bâche, poires, caisses.\n"
        "- Désir : le livre de trains **maintenant**.\n"
        "- Objet : livre rouge à locomotive, train bleu sur le pont, poire "
        "jaune, parapluie, seau de zinc.\n"
        "- Indice unique : éclat de parapluie, vu dès l'ouverture, payé "
        "sur le tissu.\n"
        "- Urgence douce : les mots appuient, le tampon n'a pas fini.\n"
        "- Imprévu 1 : il parle trop vite ; la dame ne lève pas les yeux.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après la phrase entière.\n"
        "- Imprévu 2 (plus rusé) : il tend trop vite vers la poire ; le "
        "papier mouillé glisse.\n"
        "- Résolution : il refuse de foncer, observe, écoute, dit les mots "
        "dans la scène.\n"
        "- Retour : parapluie partagé, livre sur la table, poire dans "
        "l'assiette, éclat sur le tissu.\n\n"
        "## Vécu\n\n"
        "Aniss veut le livre **maintenant**. Impatience (le train crié, "
        "main trop vite sur la poire), puis sourire qui disparaît, épaules "
        "qui tombent. Papa se baisse, pose une question, ne récite pas la "
        "règle. La dame ne parle pas. Aniss agit : bouche fermée, bonjour, "
        "s'il te plaît, merci. Merci vécu après l'écoute. Fin : l'éclat du "
        "début tient sur le tissu.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau : Le livre de trains d'Aniss. Lieu du dump : "
        "bibliothèque puis marché, pluie, parapluies, seau de zinc, papier "
        "mouillé. Relance : Aniss parle à la dame. Quels mots dit-il ? "
        "expected bonjour. Labels Q gardés.\n"
        "- Ouverture inventée (goutte sur le tissu sombre), pas un gabarit "
        "v2, pas « joue au salon », pas « la pluie dessine des fils », pas "
        "radiateur qui cliquette tout bas.\n"
        "- Indice unique : éclat de parapluie (roster). Pas pavé/zeste/"
        "seau, pas merle, miel, marque fine.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` "
        "retirés.\n"
        "- Leçon non dite : on l'entend quand il dit bonjour, s'il te "
        "plaît, merci. Pas « on dit bonjour d'abord », pas « tu te "
        "souviens des mots », pas « les trois mots ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. Dame = "
        "label, pas de réplique. Papa ajouté (dump n'avait que maman).\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive vers la poire.\n"
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
