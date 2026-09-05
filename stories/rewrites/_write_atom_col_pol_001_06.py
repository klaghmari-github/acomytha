#!/usr/bin/env python3
"""ATOM-COL.POL.001-06 — La pomme et la tulipe de Nino (F-NAR-019, N3, COL.POL.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.POL.001-06"
TITLE = "La pomme et la tulipe de Nino"
N3 = LIMITS["N3"]
CHARS = "Nino, papa, maman"
SETTING = (
    "épicerie puis fleuriste. Volet vert, caisse de pommes, "
    "pas de la porte, cloche de cuivre, tulipes dans l'eau"
)
INDICE = "éclat de volet"
FIL = (
    "Une poussière claire tombe du volet vert. Sur le bois, un "
    "éclat de volet luit. Nino veut la pomme à joue rose, maintenant. "
    "Il parle trop vite : les mots se cognent au bois. La dame ne "
    "lève pas les yeux. Sourire parti. Papa se baisse. Bonjour, "
    "s'il te plaît, merci vécus. Chez les fleurs, la tige glisse. "
    "Il refuse de foncer. Sur le bois, l'éclat de volet tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(pavé|pave|zeste|parapluie|bâche|bache|poire|ferdinand|"
    r"victorino|pli|mie|poisson|page|escargot|pompon)\b",
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
    "ferdinand",
    "victorino",
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
    "tu as bien fait",
    "on aime écouter",
    "on aime ecouter",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "boulangerie",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de bâche",
    "éclat de bache",
    "éclat de poire",
    "éclat de seau",
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
    "éclat de marche",
    "éclat de vitre",
    "éclat de grain",
    "éclat de liste",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pomme",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de volet",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_pomme_maintenant; "
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
        emphasis="tulipe",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_sur_la_tulipe; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de volet",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
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
        "volet,cloche",
        [
            "narrateur|Une poussière claire tombe du volet vert.",
            "narrateur|Le bois sent le soleil, un peu chaud.",
            "narrateur|Sur le bois, un éclat de volet luit.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, sur le volet ?",
            "narrateur|Un chat gris se tient sur le pas.",
            "narrateur|Il cligne, les yeux jaunes.",
            "enfant-m|Il me regarde, maman.",
            "maman|Comme les pommes.",
            "narrateur|Une caisse de pommes attend près du pas de la porte.",
            "narrateur|Les pommes sont jaunes, avec une joue rose.",
            "narrateur|Ça sent le sucré et le bois sec.",
            "enfant-m|Elles brillent, maman.",
            "maman|Tu les vois, Nino ?",
            "enfant-m|Oui, maman.",
            "papa|On avance.",
            "narrateur|La cloche de cuivre penche au-dessus du bois.",
            "narrateur|Papa pousse un peu le bois.",
            "narrateur|En ce moment, Nino pousse un peu la porte.",
            "narrateur|La cloche de cuivre fait ding.",
            "narrateur|L'air dedans est frais, un peu sucré.",
            "narrateur|Des bocaux brillent sur une étagère.",
            "enfant-m|Je la veux, maintenant.",
            "papa|Celle à joue rose ?",
            "enfant-m|Oui, tout de suite !",
            "narrateur|La dame essuie le bois du comptoir.",
            "narrateur|Le chiffon glisse, sans un bruit.",
            "narrateur|Nino se dresse sur les pointes.",
            "enfant-m|Une pomme !",
            "narrateur|Les mots de Nino se cognent au bois.",
            "narrateur|La dame ne lève pas les yeux.",
            "narrateur|Ses mains sont pleines de chiffon.",
            "enfant-m|Oh.",
            "narrateur|L'éclat de volet tremble, puis tient.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et l'inquiétude se heurtent.",
            "enfant-m|Elle ne me voit pas, papa.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|La pomme est derrière le bois ?",
            "enfant-m|Oui, papa.",
            "narrateur|Nino montre la pomme jaune, à joue rose.",
            "maman|Tu parles à la dame, Nino.",
            "narrateur|Le chiffon se pose enfin.",
            "narrateur|La dame lève les yeux.",
            "enfant-m|Elle est là.",
            "papa|Elle te regarde, Nino ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino parle à la dame.",
            "narrateur|Quels mots dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "pomme,cloche",
        [
            "enfant-m|Une pomme.",
            "narrateur|Nino referme la bouche.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le chiffon, un instant.",
            "narrateur|Il écoute le silence du bois.",
            "enfant-m|Bonjour.",
            "papa|Bonjour.",
            "enfant-m|Une pomme, s'il te plaît.",
            "enfant-m|Celle à joue rose.",
            "narrateur|La dame tend une pomme jaune.",
            "narrateur|La peau est lisse, un peu froide.",
            "enfant-m|Merci.",
            "papa|Merci, Nino.",
            "narrateur|Papa a entendu toute la phrase.",
            "narrateur|Le ventre de Nino se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "enfant-m|Elle a une joue rose.",
            "maman|Tu l'as dans les mains.",
            "narrateur|Nino tourne la pomme, sans se presser.",
            "enfant-m|Elle est froide, papa.",
            "papa|Oui.",
            "maman|On la porte jusqu'à la rue ?",
            "enfant-m|Oui, maman.",
            "narrateur|Ils restent un moment près des bocaux.",
            "narrateur|Un rayon touche le verre, étroit.",
            "narrateur|Nino serre la pomme contre lui.",
            "papa|On sort ?",
            "enfant-m|Oui, papa.",
            "maman|Avec la pomme.",
            "narrateur|La cloche de cuivre fait ding.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "eau,tulipe",
        [
            "narrateur|Ils passent le pas de la porte.",
            "narrateur|Le volet vert tape une fois.",
            "narrateur|Chez la fleuriste, l'air change.",
            "narrateur|Ça sent fort, comme un jardin serré.",
            "narrateur|Des tulipes rouges tiennent dans l'eau.",
            "narrateur|L'eau tremble un peu, dans le seau.",
            "enfant-m|Une tulipe rouge !",
            "maman|Celle-là, bien droite ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nino tend la main trop vite.",
            "narrateur|La tige glisse sous ses doigts.",
            "narrateur|La tulipe penche, puis se redresse.",
            "enfant-m|Oh.",
            "narrateur|Nino s'arrête.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le seau, un instant.",
            "narrateur|Il écoute l'eau, près du bois.",
            "narrateur|Sur le volet vert, l'éclat de volet brille.",
            "enfant-m|Bonjour.",
            "narrateur|La dame incline la tête.",
            "enfant-m|Une tulipe, s'il te plaît.",
            "narrateur|La dame tend une tulipe rouge.",
            "narrateur|La tige est lisse, un peu froide.",
            "narrateur|Une goutte glisse le long de la tige.",
            "enfant-m|Merci.",
            "maman|On rentre, maintenant.",
            "papa|Tu tiens la pomme des deux mains ?",
            "enfant-m|Oui, papa.",
            "narrateur|Nino tient la pomme contre lui.",
            "narrateur|Il tient la tulipe de l'autre main.",
            "narrateur|La tulipe sent le jardin, près du nez.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "verre",
        [
            "narrateur|Ils rentrent le long du volet vert.",
            "narrateur|Le vent se tait, près du mur.",
            "narrateur|À la maison, maman met la tulipe dans un verre.",
            "narrateur|L'eau fait un petit cercle.",
            "maman|Tu veux un bout de pomme ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nino croque.",
            "narrateur|C'est croquant, un peu sucré.",
            "enfant-m|Comme tout à l'heure, papa !",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur le bois.",
            "maman|On est bien, ici.",
            "narrateur|Nino pose la pomme près du verre.",
            "enfant-m|On le voit, maman.",
            "maman|Tu le vois sur le bois ?",
            "enfant-m|Oui, l'éclat.",
            "narrateur|La tulipe rouge se tient dans le verre.",
            "narrateur|La joue rose de la pomme brille.",
            "narrateur|L'éclat de volet tient sur le bois.",
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
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban: {ph}")
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
    if "volet vert" not in blob:
        raise SystemExit(f"{SID}: manque volet vert")
    if "caisse de pommes" not in blob:
        raise SystemExit(f"{SID}: manque caisse de pommes")
    if "pas de la porte" not in blob:
        raise SystemExit(f"{SID}: manque pas de la porte")
    if "ferdinand" in blob or "victorino" in blob:
        raise SystemExit(f"{SID}: prénom dump")
    if re.search(r"\btom\b", blob):
        raise SystemExit(f"{SID}: Tom interdit")
    if "grain de pomme" in blob:
        raise SystemExit(f"{SID}: grain de pomme (BAN)")
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
    if q_text != "Nino parle à la dame. Quels mots dit-il ?":
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
        "veut la pomme maintenant ; parle trop vite ; chiffon ; dame sans "
        "les yeux ; refuse de foncer ; bonjour ; s'il te plaît ; merci ; "
        "chez les fleurs la tige glisse ; mêmes mots vécus)\n"
        "- **Personnages :** Nino, papa, maman. Troupe D16. Dump Ferdinand "
        "/ Victorino → Nino. Papa ajouté. La dame = label du dump "
        "(chiffon, comptoir, tend la pomme, incline la tête, tend la "
        "tulipe), pas de réplique, pas de leçon récitée. Chat gris = "
        "geste du lieu (sur le pas, yeux jaunes), muet. Adultes parlants "
        "= papa/maman.\n"
        "- **Lieu :** épicerie puis fleuriste. Volet vert, caisse de "
        "pommes, pas de la porte, cloche de cuivre, bocaux, tulipes dans "
        "l'eau. ≠ POL.001-01 (pain/pavé) ≠ POL.001-02 (citron/zeste) ≠ "
        "POL.001-03 (livre/parapluie) ≠ POL.001-04/05 (marché).\n"
        "- **Indice unique :** éclat de volet (bois dès l'ouverture → "
        "tremble au chiffon → brille sur le volet vert → tient sur le "
        "bois). Pas éclat de pavé / zeste / parapluie / bâche / poire. "
        "Pas grain de pomme (BAN).\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une poussière claire tombe du volet vert. Sur le bois, un éclat "
        "de volet luit. Chat gris sur le pas, caisse de pommes, cloche de "
        "cuivre. Nino veut la pomme à joue rose **maintenant**. Il crie "
        "la pomme : les mots se cognent au bois. La dame ne lève pas les "
        "yeux. Sourire parti, épaules basses. Papa se baisse. Il refuse "
        "de foncer, dit bonjour, s'il te plaît, merci. La pomme arrive. "
        "Merci vécu. Chez la fleuriste, il tend trop vite : la tige "
        "glisse, la tulipe penche. Il observe, écoute l'eau, retrouve "
        "l'éclat. Bonjour, s'il te plaît, merci. Sur le bois, l'éclat "
        "tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : épicerie, volet vert, caisse de pommes, pas de la "
        "porte, chat gris, cloche de cuivre, bocaux, puis fleuriste, "
        "tulipes, seau, eau.\n"
        "- Désir : la pomme à joue rose **maintenant**, puis la tulipe.\n"
        "- Objet : pomme jaune à joue rose, tulipe rouge, volet, cloche, "
        "verre.\n"
        "- Indice unique : éclat de volet, vu dès l'ouverture, payé "
        "sur le bois.\n"
        "- Urgence douce : les mots appuient, le chiffon n'a pas fini.\n"
        "- Imprévu 1 : il parle trop vite ; la dame ne lève pas les yeux.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après la phrase entière.\n"
        "- Imprévu 2 (plus rusé) : il tend trop vite vers la tulipe ; "
        "la tige glisse.\n"
        "- Résolution : il refuse de foncer, observe, écoute, dit les "
        "mots dans la scène.\n"
        "- Retour : tulipe dans le verre, pomme à joue rose, éclat sur "
        "le bois.\n\n"
        "## Vécu\n\n"
        "Nino veut la pomme **maintenant**. Impatience (la pomme criée, "
        "main trop vite sur la tige), puis sourire qui disparaît, épaules "
        "qui tombent. Papa se baisse, pose une question, ne récite pas "
        "la règle. La dame ne parle pas. Nino agit : bouche fermée, "
        "bonjour, s'il te plaît, merci. Merci vécu après l'écoute. Fin : "
        "l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau : La pomme et la tulipe de Nino. Lieu du dump : "
        "épicerie puis fleuriste, volet vert, caisse de pommes, pas de "
        "la porte. Relance : Nino parle à la dame. Quels mots dit-il ? "
        "expected bonjour. Labels Q posés (dump xlsx : Victorino / "
        "pomme).\n"
        "- Ouverture inventée (poussière claire du volet vert), pas un "
        "gabarit v2, pas « un volet fait toc », pas « tape tout doux ».\n"
        "- Indice unique : éclat de volet. Pas pavé/zeste/parapluie/"
        "bâche/poire, pas grain de pomme, pas merle, miel, marque fine.\n"
        "- Tics encore/déjà/tout doux/tout calme/tout lent et "
        "`aujourd'hui,` retirés.\n"
        "- Leçon non dite : on l'entend quand il dit bonjour, s'il te "
        "plaît, merci. Pas « on dit bonjour d'abord », pas « tu te "
        "souviens des mots », pas « les trois mots ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. Dame "
        "= label, pas de réplique. Papa ajouté. Dump Ferdinand / "
        "Victorino → Nino.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive vers la tulipe.\n"
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
