#!/usr/bin/env python3
"""ATOM-DIF.BES.002-04 — Le collier de maman (F-NAR-019, N2, DIF.BES.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.002-04"
TITLE = "Le collier de maman"
N2 = LIMITS["N2"]
CHARS = "Nina, Victorino, papa, maman"
SETTING = "salon, boîte à couture, rideau de dentelle, pelote de laine"
INDICE = "éclat de couvercle"
FIL = (
    "Un carré de soleil perce le rideau de dentelle. Sur le couvercle, "
    "un éclat de couvercle brille. Nina veut un collier pour maman, "
    "maintenant. Elle pousse le fil trop vite : Victorino garde le rideau. "
    "Elle refuse de foncer, dit d'accord, enfile seule. Merci vécu. "
    "La rouge file dans la dentelle. L'éclat de couvercle tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(plaque|pierre|grille|cube|bois|carte|boule|galet|tapis|"
    r"crochet|carotte|seau|carton|mousse|pompon|manteau|crayon|"
    r"buée|buee|croûte|croute|tableau|casier|moufle|craie|"
    r"cartable|pinceau|casserole|tasse|wagon|farine|nappe)\b",
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
    "delphine",
    "j'ai compris",
    "j'ai proposé",
    "j'ai propose",
    "j'ai accepté",
    "j'ai accepte",
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
    "on peut proposer",
    "on peut accepter",
    "plusieurs réponses",
    "plusieurs reponses",
    "c'est une réponse",
    "c'est une reponse",
    "tu as accepté",
    "tu as accepte",
    "nina accepte",
    "regarder, c'est",
    "lune d'étain",
    "lune d'etain",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "grain de",
    "éclat de plaque",
    "éclat de pierre",
    "éclat de grille",
    "éclat de laine",
    "éclat de cube",
    "éclat de bois",
    "éclat de carte",
    "éclat de boule",
    "éclat de galet",
    "éclat de tapis",
    "éclat de crochet",
    "éclat de carotte",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de pli",
    "éclat de crayon",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de cartable",
    "éclat de pinceau",
    "éclat de casserole",
    "éclat de tasse",
    "éclat de wagon",
    "éclat de nappe",
    "éclat de farine",
    "éclat de vitre",
    "éclat de sonnette",
    "éclat de bouton",
    "éclat de caisse",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de couvercle",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_collier_et_victorino_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="invite",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_invite_puis_elle_prend_sa_reponse; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="D'accord",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_dit_daccord_et_enfile_seule; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de couvercle",
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
        emphasis="éclat de couvercle",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_couvercle; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "accepter",
    "accepted_examples": (
        "accepter | proposer | un non | regarder"
    ),
    "retry_prompt": "Elle propose. Victorino peut regarder. Que fait Nina ?",
    "engine_ok_text": "Oui, elle accepte.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "boite,perles",
        [
            "narrateur|Un carré de soleil perce le rideau de dentelle.",
            "narrateur|Des trous de lumière tombent sur le plancher.",
            "narrateur|La cire sent chaud, sous le rayon.",
            "enfant-f|Ça sent bon, maman.",
            "maman|C'est la boîte à couture.",
            "narrateur|La boîte à couture attend près du canapé.",
            "narrateur|Le couvercle est lisse, un peu chaud.",
            "narrateur|Sur le couvercle, un éclat de couvercle brille.",
            "enfant-f|Il brille, papa !",
            "papa|Tu le vois, Nina ?",
            "enfant-f|Oui, sur le couvercle.",
            "narrateur|Une pelote de laine dort dans un coin.",
            "narrateur|La pelote est grise, un peu rêche.",
            "maman|Elle reste dans la boîte ?",
            "enfant-f|Oui, maman.",
            "narrateur|Dedans, des perles dorment.",
            "narrateur|Brunes.",
            "narrateur|Beiges.",
            "narrateur|Une rouge, toute ronde.",
            "enfant-f|La rouge est pour toi.",
            "maman|Pour moi ?",
            "enfant-f|Oui.",
            "enfant-f|Je fais un collier, maintenant !",
            "papa|Tu prends le fil ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa glisse un fil vers elle.",
            "narrateur|Le fil est un peu raide.",
            "narrateur|Le coin de la dentelle est clair, sous le rayon.",
            "narrateur|En ce moment, Nina tire le fil trop vite.",
            "narrateur|Le fil se tord entre les doigts.",
            "enfant-f|Oh.",
            "narrateur|Victorino est près de la fenêtre.",
            "narrateur|Il tient un pli du rideau.",
            "narrateur|La dentelle chatouille ses doigts.",
            "enfant-f|Tu viens ?",
            "narrateur|Victorino ne dit rien.",
            "narrateur|Il garde le pli, sans bouger.",
            "enfant-f|Prends le fil !",
            "narrateur|Nina pousse le fil vers sa main.",
            "narrateur|La main de Victorino reste sur le rideau.",
            "narrateur|Le fil tombe sur le plancher.",
            "narrateur|Une perle brune glisse, presque.",
            "enfant-f|Ça ne veut pas.",
            "narrateur|Le sourire de Nina s'en va.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|L'éclat de couvercle tremble, puis tient.",
            "narrateur|Ses épaules tombent un peu, lourdes.",
            "papa|Tu veux qu'il vienne ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa se baisse à sa hauteur.",
            "maman|Le fil est là, près du pied.",
            "enfant-f|Je le reprends.",
            "narrateur|Nina ramasse le fil, un peu froissé.",
            "copain|Je regarde.",
            "enfant-f|Maintenant ?",
            "narrateur|Victorino secoue la tête, très peu.",
            "papa|Tu l'as entendu, Nina ?",
            "enfant-f|Il regarde.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nina invite Victorino.",
            "narrateur|Que fait-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "perles",
        [
            "narrateur|Nina se penche trop vite vers Victorino.",
            "enfant-f|Viens, maintenant !",
            "narrateur|Victorino reste près du rideau.",
            "copain|Plus tard.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Nina ne revient pas.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Elle referme la bouche, un instant.",
            "narrateur|Elle regarde le pli du rideau.",
            "papa|Tu le vois, près de la fenêtre ?",
            "enfant-f|Oui.",
            "narrateur|Victorino garde le silence, un moment.",
            "enfant-f|D'accord.",
            "narrateur|Nina reprend le fil, sans se presser.",
            "narrateur|Elle enfile une perle brune.",
            "narrateur|Ça fait un petit glissement.",
            "enfant-f|Tu veux la beige ?",
            "narrateur|Victorino ne tend pas la main.",
            "copain|Je regarde.",
            "enfant-f|D'accord.",
            "narrateur|Nina enfile la beige, toute seule.",
            "narrateur|Les perles tapent l'une contre l'autre.",
            "narrateur|Victorino s'assoit sur ses talons.",
            "narrateur|Il regarde le fil, sans parler.",
            "narrateur|Sur le couvercle, l'éclat de couvercle brille.",
            "enfant-f|Il est là.",
            "papa|Sur le couvercle ?",
            "enfant-f|Oui, papa.",
            "maman|Merci, Nina.",
            "narrateur|Maman a entendu toute la phrase.",
            "narrateur|Le ventre de Nina se desserre.",
            "papa|Tu as les mains prêtes ?",
            "enfant-f|Un peu, papa.",
            "narrateur|Le collier s'allonge, lentement.",
            "maman|La rouge attend ?",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "perles",
        [
            "narrateur|Nina veut la perle rouge, d'un coup.",
            "enfant-f|Regarde, la rouge !",
            "narrateur|Elle tend la perle trop vite.",
            "enfant-f|Tu veux la rouge ?",
            "copain|Non.",
            "narrateur|Nina veut la poser dans sa main.",
            "narrateur|La perle rouge file entre les doigts.",
            "enfant-f|Ça tombe !",
            "narrateur|La rouge se cache dans la dentelle.",
            "narrateur|Nina veut foncer, d'un coup.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Ses épaules se serrent un peu.",
            "narrateur|Ça tape fort, dans sa poitrine.",
            "narrateur|Personne ne dit la suite à voix haute.",
            "narrateur|Elle regarde la boîte à couture.",
            "narrateur|Elle écoute le salon, un instant.",
            "narrateur|La poussière danse dans le rayon.",
            "narrateur|Sur le couvercle, l'éclat de couvercle revient.",
            "enfant-f|Comme ce matin ?",
            "papa|Tu le vois, toi ?",
            "enfant-f|Oui, sur le couvercle.",
            "narrateur|Nina cherche dans la dentelle.",
            "narrateur|Le fil du rideau chatouille un peu.",
            "narrateur|Ses doigts trouvent la perle rouge.",
            "enfant-f|Te voilà.",
            "enfant-f|Je la mets, moi.",
            "narrateur|Elle enfile la rouge, sans se presser.",
            "papa|Au milieu ?",
            "enfant-f|Oui, papa.",
            "maman|Le collier s'allonge ?",
            "enfant-f|Oui, maman.",
            "narrateur|Victorino reste sur ses talons.",
            "narrateur|Il regarde la rouge, sans la prendre.",
            "enfant-f|Elle est lisse.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "maman|On noue le fil ?",
            "enfant-f|Oui.",
            "narrateur|Papa tient le nœud.",
            "narrateur|Nina tire, sans se presser.",
            "narrateur|Le collier est fermé.",
            "papa|Le collier est pour maman ?",
            "enfant-f|Oui, papa.",
            "narrateur|Maman baisse un peu la tête.",
            "narrateur|Nina passe le collier.",
            "narrateur|Les perles tapent contre le cou.",
            "narrateur|La perle rouge se met au milieu.",
            "maman|Il est beau.",
            "enfant-f|Victorino a regardé.",
            "papa|Tu le vois, sur maman ?",
            "enfant-f|Oui, papa.",
            "narrateur|La lumière perce la dentelle.",
            "narrateur|La boîte à couture sent la cire.",
            "enfant-f|L'éclat est là, papa.",
            "papa|Tu le vois sur le couvercle ?",
            "enfant-f|Oui, papa.",
            "maman|On est bien, ici.",
            "narrateur|Nina pose la joue près du couvercle.",
            "narrateur|Le couvercle est lisse, un peu chaud.",
            "enfant-f|C'est chaud.",
            "narrateur|Victorino lâche le pli du rideau.",
            "narrateur|L'éclat de couvercle tient sur le couvercle.",
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
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        for bad in EXTRA_BAD:
            if re.search(rf"(?<!\w){re.escape(bad)}(?!\w)", low):
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
    if n_clue != 5:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 5)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "delphine" in blob:
        raise SystemExit(f"{SID}: Delphine (BAD_NAMES)")
    if "éclat de laine" in blob:
        raise SystemExit(f"{SID}: éclat de laine BAN")
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
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Nina invite Victorino. Que fait-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "accepter":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt", "").lower()
    if "accepter" not in retry and "regarder" not in retry:
        raise SystemExit(f"{SID}: retry hors leçon")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on peut proposer",
        "on peut accepter",
        "plusieurs réponses",
        "c'est une réponse",
        "tu as accepté",
        "j'ai proposé",
        "j'ai accepté",
        "nina accepte",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Victorino muet (copain)")

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
        "- **Public :** N2 (≤15), audio familial\n"
        "- **Leçon :** DIF.BES.002 — inviter / proposer / accepter "
        "(vécue : Nina veut le collier et Victorino maintenant ; pousse "
        "le fil ; silence puis « je regarde » ; refuse de foncer ; "
        "d'accord ; enfile seule ; la rouge, un non ; d'accord encore)\n"
        "- **Personnages :** Nina, Victorino, papa, maman. Troupe D16. "
        "Rythmes distincts : Nina propose vite, Victorino prend son "
        "temps, pose sa limite, se tait. Le silence compte.\n"
        "- **Lieu :** salon, boîte à couture, rideau de dentelle, pelote "
        "de laine, coin de la dentelle. ≠ 002-01 (cuisine, cheval), "
        "≠ 002-02 (terrasse, cerf-volant), ≠ 002-03 (raisins), "
        "≠ 002-05 (couloir, carton).\n"
        "- **Indice unique :** éclat de couvercle (couvercle du matin → "
        "tremble → brille au d'accord → revient après la rouge perdue → "
        "tient sur le couvercle). Pelote de laine au monde, pas éclat "
        "de laine.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un carré de soleil perce le rideau de dentelle. La cire sent "
        "chaud. Sur le couvercle, un éclat de couvercle brille. Nina "
        "veut un collier pour maman **maintenant**, et Victorino avec "
        "elle. Première idée : pousser le fil dans sa main. Victorino "
        "garde le rideau, se tait, puis dit qu'il regarde. Le fil "
        "tombe. Sourire parti, épaules basses. Papa se baisse à sa "
        "hauteur. Elle insiste : viens maintenant. Plus tard. Elle "
        "refuse de foncer, dit d'accord, enfile la brune et la beige. "
        "Merci vécu. La rouge : il dit non ; elle veut la poser quand "
        "même ; la perle file dans la dentelle. Elle refuse, retrouve "
        "l'éclat, enfile la rouge. L'éclat de couvercle tient sur le "
        "couvercle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon, dentelle, cire, couvercle chaud, pelote "
        "grise, perles brunes beiges rouge, canapé, fenêtre.\n"
        "- Désir : collier pour maman, Victorino qui enfile avec elle, "
        "maintenant.\n"
        "- Objet : fil, perles, boîte à couture, collier.\n"
        "- Indice unique : éclat de couvercle, vu dès l'ouverture, payé "
        "à la fin.\n"
        "- Urgence douce : le collier, tout de suite, et lui avec elle.\n"
        "- Imprévu 1 : elle pousse le fil ; il ne le prend pas ; le fil "
        "tombe.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : la rouge, un non ; elle veut la "
        "poser dans sa main ; la perle se cache dans la dentelle.\n"
        "- Résolution : elle refuse de foncer, dit d'accord, enfile "
        "seule, retrouve l'éclat, noue.\n"
        "- Retour : collier sur maman, cire, joue près du couvercle, "
        "éclat du début.\n\n"
        "## Vécu\n\n"
        "Nina veut le collier **maintenant**, et Victorino avec elle. "
        "Impatience, puis sourire qui s'en va. Victorino se tait, "
        "regarde, dit plus tard, dit non. Papa se baisse, pose une "
        "question, ne récite pas la règle. Nina agit : bouche fermée, "
        "d'accord, fil à elle. Merci vécu après l'écoute. Fin : "
        "l'éclat du début tient sur le couvercle.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau : Le collier de maman. Lieu du dump : salon, "
        "boîte à couture, rideau de dentelle, pelote de laine. Relance : "
        "Nina invite Victorino. Que fait-elle ? expected accepter.\n"
        "- Ouverture inventée (carré de soleil, trous de lumière, cire), "
        "pas un gabarit v2, pas « joue au salon », pas « est dans "
        "l'entrée ».\n"
        "- Indice unique : éclat de couvercle. Pas plaque/pierre/grille/"
        "laine/cube/bois/carte/boule/galet. Pas grains, pas lune "
        "d'étain. Ban tapis, crochet, crayon, buée, croûte, tableau, "
        "casier, moufle, craie, cartable, pinceau, casserole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` "
        "retirés. Leçon non dite : on la voit quand elle dit d'accord "
        "et enfile seule. Pas « on peut proposer », pas « tu as "
        "accepté », pas « plusieurs réponses ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Papa et maman parlent. Victorino = copain, rythme lent.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle plus tendu à la rouge.\n"
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
