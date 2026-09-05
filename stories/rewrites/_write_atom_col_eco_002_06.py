#!/usr/bin/env python3
"""ATOM-COL.ECO.002-06 — Le manteau jaune de Raphaël (F-NAR-019, N1, COL.ECO.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.002-06"
TITLE = "Le manteau jaune de Raphaël"
N1 = LIMITS["N1"]
CHARS = "Raphaël, papa, maman"
SETTING = (
    "maison sous la pluie, gouttière, cacao, bottes, classe"
)
INDICE = "éclat de manteau"
FIL = (
    "Une vapeur de cacao danse près de la vitre. Sur le bouton, un "
    "éclat de manteau brille. Raphaël veut parler maintenant. Il coupe "
    "papa : les mots se perdent. Il enfile trop vite : le bouton manque. "
    "À l'école, sa phrase se cogne à la classe. Il refuse de foncer, "
    "attend le silence, raconte le chat. Merci vécu. Sur le bouton, "
    "l'éclat de manteau tient."
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
    "j'ai su attendre",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "élie",
    "elie",
    "ewen",
    "pompon",
    "casserole",
    "crayon",
    "buée",
    "buee",
    "croûte",
    "croute",
    "casier",
    "moufle",
    "craie",
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
    "éclat de cartable",
    "éclat de pompon",
    "éclat de bouton",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de manteau",
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
        emphasis="parler",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_parle_quand_le_silence_arrive; "
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
        emphasis="manteau",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_sur_le_manteau; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de manteau",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bouton; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "attendre",
    "accepted_examples": (
        "attendre | il attend | lever la main | la main"
    ),
    "retry_prompt": "Il lève la main et il attend. Que fait Raphaël ?",
    "engine_ok_text": "Oui, il attend.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "pluie,gouttiere,pas",
        [
            "narrateur|Une vapeur de cacao danse près de la vitre.",
            "narrateur|La vitre est tiède, un peu floue.",
            "narrateur|Le manteau jaune attend sur la chaise.",
            "narrateur|Sur le bouton, un éclat de manteau brille.",
            "enfant-m|Il est blanc, papa.",
            "papa|C'est le fil, sous la lumière.",
            "narrateur|Papa glisse les bottes rouges près de la porte.",
            "maman|Tes lacets, Raphaël ?",
            "narrateur|Maman noue un lacet, puis l'autre.",
            "narrateur|Ça sent le cacao, chaud.",
            "narrateur|Le chat gris dort sur le radiateur.",
            "narrateur|Son nez est rose, minuscule.",
            "enfant-m|Il ronronne, papa.",
            "papa|Tu l'entends, Raphaël ?",
            "enfant-m|Oui.",
            "enfant-m|Je le dis à l'école !",
            "maman|Tu l'entends, la gouttière ?",
            "enfant-m|Elle chante.",
            "papa|Elle boit la pluie.",
            "enfant-m|Papa, le bouton brille, maintenant !",
            "narrateur|Papa parle à maman, près des bottes.",
            "papa|Les bottes sont mouillées, pour dehors.",
            "narrateur|Les mots de Raphaël se cognent aux leurs.",
            "narrateur|Personne ne tourne la tête.",
            "papa|Tu disais quelque chose, Raphaël ?",
            "enfant-m|Le bouton.",
            "enfant-m|Il brille.",
            "narrateur|En ce moment, Raphaël pose la main sur le manteau.",
            "narrateur|Le tissu est rêche, un peu froid.",
            "enfant-m|Je le mets, maintenant !",
            "narrateur|Il enfile le manteau trop vite.",
            "narrateur|Le bouton manque.",
            "narrateur|Le capuchon penche sur l'œil.",
            "enfant-m|Oh.",
            "narrateur|L'éclat de manteau tremble, puis tient.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-m|Ça ne veut pas, maman.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|On boutonne ensemble ?",
            "enfant-m|Oui, papa.",
            "narrateur|Ils avancent jusqu'à la porte.",
            "maman|Tu dis bonjour, à l'école ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Au revoir, maman.",
            "maman|Au revoir, Raphaël.",
            "narrateur|Dehors, la gouttière chante sur le toit.",
            "narrateur|La pluie dessine des fils gris.",
            "narrateur|Les gouttes tapent sur le capuchon.",
            "enfant-m|Ça chante sur ma tête.",
            "papa|Oui.",
            "papa|C'est la pluie.",
            "narrateur|L'air sent la terre.",
            "narrateur|Les bottes font un bruit mou.",
            "narrateur|L'école a une porte en bois.",
            "narrateur|Le couloir sent la laine mouillée.",
            "narrateur|Une petite flaque brille sous la botte.",
            "maman|Le crochet est à ta hauteur.",
            "narrateur|Raphaël accroche le manteau.",
            "papa|On revient te chercher.",
            "enfant-m|Au revoir, papa.",
            "narrateur|Le tapis de la classe est bleu.",
            "narrateur|Il est un peu frais sous les genoux.",
            "narrateur|Les cubes en bois sentent la forêt.",
            "narrateur|Le doudou lapin reste dans le sac.",
            "narrateur|Raphaël s'assoit sur le tapis.",
            "narrateur|Il pose les mains sur ses genoux.",
            "narrateur|La maîtresse parle près des chaises.",
            "enfant-m|Bonjour, maîtresse.",
            "narrateur|Une image d'animaux attend sur le livre.",
            "narrateur|Raphaël a une idée.",
            "narrateur|Le chat de la maison est gris.",
            "narrateur|Son nez est rose.",
            "enfant-m|Je le dis, maintenant !",
            "narrateur|Il ouvre la bouche trop vite.",
            "narrateur|Ses mots se cognent à la classe.",
            "narrateur|Personne ne comprend.",
            "narrateur|Raphaël referme la bouche.",
            "narrateur|Il serre les mains sur ses genoux.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Raphaël veut parler.",
            "narrateur|Que fait-il d'abord ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Raphaël ouvre la bouche trop vite.",
            "enfant-m|Le chat est gris !",
            "narrateur|Une voix d'enfant parle près du tapis.",
            "narrateur|On entend un lapin blanc.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Raphaël refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Les mains se posent à plat.",
            "narrateur|Une main monte, sans crier.",
            "narrateur|Sa main reste en l'air.",
            "narrateur|Il regarde la pluie sur la vitre.",
            "narrateur|Le tapis bleu est frais sous les genoux.",
            "narrateur|Un cube de bois roule, puis s'arrête.",
            "narrateur|Le lapin blanc finit sa phrase.",
            "narrateur|Un silence arrive près du tapis.",
            "narrateur|Derrière la porte, le manteau jaune attend.",
            "narrateur|Sur le bouton, l'éclat de manteau brille.",
            "enfant-m|Je peux dire quelque chose ?",
            "narrateur|La maîtresse tourne la tête, près du livre.",
            "enfant-m|Le chat est gris.",
            "enfant-m|Il a un nez rose.",
            "enfant-m|Il aime le radiateur.",
            "narrateur|La classe écoute jusqu'au bout.",
            "narrateur|Raphaël montre le bout de son doigt.",
            "enfant-m|Minuscule, comme ça.",
            "narrateur|Le ventre de Raphaël se desserre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pas",
        [
            "narrateur|Plus tard, une petite cloche sonne.",
            "narrateur|Raphaël range son cartable.",
            "narrateur|Le manteau jaune est presque sec.",
            "narrateur|La porte s'ouvre.",
            "maman|Tu as passé un bon moment ?",
            "enfant-m|Le chat !",
            "enfant-m|Le nez rose !",
            "papa|Les bottes, Raphaël ?",
            "narrateur|Les deux voix se mélangent.",
            "enfant-m|Oh.",
            "narrateur|Il saisit le manteau trop vite.",
            "narrateur|Le capuchon penche.",
            "enfant-m|Oh.",
            "narrateur|Les mots se perdent dans le couloir.",
            "narrateur|Raphaël s'arrête.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Il refuse de foncer.",
            "narrateur|Le manteau revient contre sa poitrine.",
            "narrateur|Il écoute la gouttière, un instant.",
            "enfant-m|Je peux te dire quelque chose ?",
            "maman|Oui, nous t'écoutons.",
            "enfant-m|J'ai parlé du chat.",
            "enfant-m|Après le lapin blanc.",
            "papa|Merci, Raphaël.",
            "narrateur|Papa a entendu toute la phrase.",
            "maman|Tu as soif ?",
            "enfant-m|Un peu, maman.",
            "papa|Le capuchon, tu le vois ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le bois du crochet tient le jaune.",
            "narrateur|Raphaël enfile le manteau, sans tirer.",
            "maman|Les bottes, maintenant ?",
            "enfant-m|Je les mets.",
            "narrateur|Les bottes font un petit bruit.",
            "papa|On rentre.",
            "narrateur|La pluie tape plus doucement.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Le manteau jaune sèche sur le crochet.",
            "narrateur|L'air sent le cacao, plus loin.",
            "enfant-m|Il a fait tout le chemin.",
            "papa|Toi aussi.",
            "narrateur|La pluie est plus douce, près de la vitre.",
            "maman|Tu souffles ?",
            "enfant-m|Oui, maman.",
            "narrateur|Raphaël souffle.",
            "narrateur|Le ventre est large, à sa place.",
            "maman|On est bien, ici.",
            "papa|Les bottes sèchent près de la porte.",
            "enfant-m|Je les verrai.",
            "narrateur|Le chat gris dort sur le radiateur.",
            "enfant-m|Son nez est rose.",
            "papa|Oui.",
            "narrateur|Le doudou lapin est dans le lit.",
            "narrateur|L'éclat de manteau tient sur le bouton.",
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
    if "élie" in blob or "elie" in blob:
        raise SystemExit(f"{SID}: Élie resté")
    if "pompon" in blob:
        raise SystemExit(f"{SID}: pompon (002-05)")
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
        "- **Leçon :** COL.ECO.002 — attendre son tour de parole "
        "(vécue : veut parler maintenant ; première idée échoue ; refuse "
        "de foncer ; parle quand le silence arrive)\n"
        "- **Personnages :** Raphaël, papa, maman. Troupe D16. Maîtresse = "
        "label (parle près des chaises, tourne la tête), pas de leçon "
        "récitée. Adultes parlants = papa/maman. Élie retiré. Papa ajouté.\n"
        "- **Lieu :** maison sous la pluie, gouttière, cacao, bottes, "
        "classe. Gouttière = détail de lieu, pas l'indice (≠ COL.ECO.001-01). "
        "≠ COL.ECO.002-05 (pompon, ballon, cour d'immeuble).\n"
        "- **Indice unique :** éclat de manteau (bouton au matin → "
        "tremble quand le manteau penche → brille au silence → tient "
        "sur le bouton)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une vapeur de cacao danse près de la vitre. Sur le bouton, un "
        "éclat de manteau brille. Raphaël veut parler **maintenant** (le "
        "chat gris, le nez rose). Il coupe papa : les mots se cognent. "
        "Il enfile trop vite : le bouton manque, le capuchon penche. "
        "Sourire parti, épaules basses. Papa se baisse. Dehors, gouttière, "
        "pluie, bottes. À l'école, il parle pendant la classe : la phrase "
        "se perd. Il refuse de foncer, lève la main, attend le silence, "
        "raconte le chat. Au crochet, l'éclat brille. À la porte, il "
        "coupe papa, saisit le manteau trop vite. Il refuse, pose, "
        "écoute, finit. Merci vécu. Sur le crochet, l'éclat tient sur "
        "le bouton.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : vapeur de cacao, vitre tiède, manteau jaune, bouton, "
        "bottes rouges, chat au radiateur, gouttière, pluie, flaque, "
        "tapis bleu, cubes, classe.\n"
        "- Désir : parler / raconter le chat **maintenant**.\n"
        "- Objet : manteau jaune, bouton, bottes, capuchon.\n"
        "- Indice unique : éclat de manteau, vu dès l'ouverture, payé "
        "au bouton.\n"
        "- Urgence douce : le mot du chat est là, papa n'a pas fini, "
        "un camarade parle.\n"
        "- Imprévu 1 : il coupe, enfile trop vite ; à l'école sa phrase "
        "se cogne à la classe.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après la phrase entière.\n"
        "- Imprévu 2 (plus rusé) : à la porte il veut tout dire en "
        "saisissant le manteau ; le capuchon penche, les mots se perdent.\n"
        "- Résolution : il refuse de foncer, pose, écoute, raconte, "
        "enfile sans tirer.\n"
        "- Retour : cacao plus loin, chat au radiateur, bottes, éclat "
        "sur le bouton.\n\n"
        "## Vécu\n\n"
        "Raphaël veut parler **maintenant**. Impatience (coupe, manteau "
        "trop vite, bouche ouverte en classe), puis sourire qui "
        "disparaît, épaules qui tombent. Papa se baisse, pose une "
        "question, ne récite pas la règle. Raphaël agit : bouche fermée, "
        "main en l'air, phrase entière. Merci vécu après l'écoute. Fin : "
        "l'éclat du début tient sur le bouton.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le manteau jaune de Raphaël (noyau dump : manteau "
        "jaune ; chat au nez rose = ce qu'il veut raconter). Élie → "
        "Raphaël. Relance : Que fait Raphaël ?\n"
        "- Ouverture inventée (vapeur de cacao près de la vitre), pas un "
        "gabarit v2, pas « joue au salon ».\n"
        "- Indice unique : éclat de manteau (roster). Pas pompon "
        "(002-05), pas gouttière-indice (001-01), pas casserole/crayon/"
        "buée, pas grains, lune d'étain, point de gouttière, merle, miel, "
        "marque fine.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` "
        "retirés.\n"
        "- Leçon non dite : on l'entend quand il attend le silence. Pas "
        "« j'ai su attendre », pas « bon travail », pas « l'histoire est "
        "finie », pas « il faut attendre ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Maîtresse = label, pas de réplique de leçon. Papa parle.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive vers le manteau.\n"
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
