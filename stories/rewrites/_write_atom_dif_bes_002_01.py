#!/usr/bin/env python3
"""ATOM-DIF.BES.002-01 — Le cheval et le pont (F-NAR-019, N1, DIF.BES.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.002-01"
TITLE = "Le cheval et le pont"
N1 = LIMITS["N1"]
CHARS = "Nino, Victorina, papa, maman"
SETTING = (
    "cuisine après gâteaux, carton de céréales, "
    "plaque, beurre, farine sur les manches"
)
INDICE = "éclat de plaque"
FIL = (
    "La plaque de gâteaux fume. Sur le bord, un éclat de plaque luit. "
    "Farine sur les manches. Nino veut le cheval sur le pont, maintenant, "
    "avec Victorina. Il tend trop vite : elle dit non, le pont se plie. "
    "Sourire parti. Papa à sa hauteur. Il refuse de foncer, attend son "
    "silence, dit d'accord. Merci vécu. Le cheval glisse. Il veut sa main : "
    "elle ne bouge pas. Il observe, retrouve l'éclat. Un éclat de plaque "
    "reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(carte|cartes|boule|galet|cube|bois|couloir|poussière|poussiere|"
    r"cour|pavé|pave|zeste|parapluie|bâche|bache|poire|volet|"
    r"croissant|réverbère|reverbere|cloche|corbeille|sacs?|panier|"
    r"dorure|carotte|seau|mousse|pompon|manteau|poisson|page|"
    r"escargot|tapis|casier|cartable|crochet|citron|casserole)\b",
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
    "j'ai compris",
    "j'ai proposé",
    "j'ai propose",
    "j'ai accepté",
    "j'ai accepte",
    "j'ai invité",
    "j'ai invite",
    "on peut proposer",
    "on peut accepter",
    "plusieurs réponses",
    "plusieurs reponses",
    "c'est une réponse",
    "c'est une reponse",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "les trois mots",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "tu as bien fait",
    "on aime écouter",
    "on aime ecouter",
    "même leçon",
    "c'est la règle",
    "c'est la regle",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de farine",
    "éclat de carte",
    "éclat de boule",
    "éclat de galet",
    "éclat de cube",
    "éclat de bois",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de bâche",
    "éclat de bache",
    "éclat de poire",
    "éclat de volet",
    "éclat de croissant",
    "éclat de réverbère",
    "éclat de reverbere",
    "éclat de cloche",
    "éclat de corbeille",
    "éclat de sac",
    "éclat de panier",
    "éclat de dorure",
    "éclat de carotte",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de pli",
    "éclat de mie",
    "éclat de poisson",
    "éclat de page",
    "éclat d'escargot",
    "éclat de casier",
    "éclat de tapis",
    "éclat de cartable",
    "éclat de crochet",
    "éclat de citron",
    "éclat de casserole",
    "éclat de nappe",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de tasse",
    "éclat de vitre",
    "éclat de crayon",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de moufle",
    "éclat de craie",
    "éclat de pinceau",
    "éclat de marche",
    "éclat de laine",
    "éclat de grain",
    "éclat de liste",
    "éclat de gouttière",
    "éclat de gouttiere",
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
        emphasis="éclat de plaque",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_cheval_et_victorina_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Victorina",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=nino_invite_sans_forcer; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="D'accord",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_attend_le_silence_puis_dit_d_accord; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de plaque",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_forcer_la_main_retrouve_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de plaque",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_reste_pale; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "proposer",
    "accepted_examples": (
        "proposer | inviter | accepter | d'accord"
    ),
    "retry_prompt": "On peut proposer. On peut accepter. Que fait-on ?",
    "engine_ok_text": "Oui, proposer.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "cuisine,carton",
        [
            "narrateur|La plaque de gâteaux fume un peu.",
            "narrateur|Ça sent le beurre, dans la cuisine.",
            "narrateur|Sur le bord, un éclat de plaque luit.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, sur la plaque ?",
            "narrateur|Nino touche l'éclat de plaque, un instant.",
            "narrateur|Le métal est tiède, un peu gras.",
            "enfant-m|Elle est chaude.",
            "maman|Les gâteaux attendent un peu.",
            "papa|On reste par terre.",
            "narrateur|De la farine blanche dort sur les manches.",
            "enfant-m|Sur tes manches, papa.",
            "papa|Oui, un peu.",
            "narrateur|Un carton de céréales est à plat.",
            "narrateur|Des lettres bleues restent dessus.",
            "enfant-m|Je le plie en pont.",
            "maman|Un pont, par terre ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nino plie le carton, deux bords.",
            "narrateur|Un petit cheval peint attend.",
            "narrateur|Sa crinière est brune, un peu raide.",
            "enfant-m|Le cheval va sur le pont.",
            "maman|Jusqu'à l'autre côté ?",
            "enfant-m|Oui.",
            "narrateur|Un mouton peint attend aussi.",
            "enfant-m|Le mouton après.",
            "narrateur|En ce moment, Nino pose le pont.",
            "narrateur|Le carton est rêche, un peu chaud.",
            "narrateur|Il appuie les deux bords.",
            "maman|Tu restes près de nous ?",
            "enfant-m|Oui, maman.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|Victorina arrive.",
            "narrateur|Elle a des chaussettes jaunes.",
            "enfant-m|Tu viens ?",
            "copine|Non.",
            "narrateur|Nino tend la main trop vite.",
            "narrateur|Il pousse le cheval d'un coup.",
            "papa|Tu le pousses, Nino ?",
            "narrateur|Les sabots glissent un peu.",
            "narrateur|Le pont se plie au milieu.",
            "enfant-m|Oh.",
            "papa|Tu as vu le carton, Nino ?",
            "enfant-m|Oui.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-m|Tu viens, maintenant !",
            "copine|Non.",
            "narrateur|Victorina recule d'un pas.",
            "narrateur|Ses épaules restent près de la porte.",
            "enfant-m|Je le prends !",
            "maman|Le pont s'est plié.",
            "papa|Tu le vois, Nino ?",
            "narrateur|Les épaules de Nino tombent un peu.",
            "narrateur|Ça serre, dans son ventre.",
            "narrateur|Papa se baisse à sa hauteur.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino invite Victorina.",
            "narrateur|Que fait-on ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "cheval,carton",
        [
            "narrateur|Nino avance trop vite vers le pont.",
            "enfant-m|Tu viens, maintenant !",
            "narrateur|Sa voix se mélange au carton.",
            "enfant-m|Oh.",
            "narrateur|Victorina reste près de la porte.",
            "narrateur|Il refuse de foncer.",
            "narrateur|Nino referme la main.",
            "papa|Tu veux venir près du pont ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Nino pose un genou près du carton.",
            "enfant-m|Tu regardes ?",
            "narrateur|Victorina ne dit rien.",
            "narrateur|Elle reste un moment, les mains collées.",
            "enfant-m|Plus tard, tu viens ?",
            "copine|Je regarde.",
            "enfant-m|D'accord.",
            "papa|Merci, Nino.",
            "narrateur|Papa a entendu toute la phrase.",
            "narrateur|Le ventre de Nino se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tu as les mains au chaud ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Nino aplatit le carton, sans le jeter.",
            "narrateur|Le pont redevient droit.",
            "enfant-m|Il tient.",
            "maman|Le cheval est là.",
            "narrateur|Nino pose le cheval près du bord.",
            "narrateur|Les sabots tapent le carton.",
            "papa|Tu as entendu les sabots ?",
            "enfant-m|Oui, papa.",
            "enfant-m|Tu veux le mouton ?",
            "copine|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Victorina s'assoit près du buffet.",
            "narrateur|Elle regarde le cheval.",
            "papa|Il avance ?",
            "enfant-m|Un peu.",
            "narrateur|Une miette tombe près du pont.",
            "narrateur|Nino la pousse du doigt.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "cheval,carton",
        [
            "narrateur|Nino pousse le cheval trop vite.",
            "enfant-m|Tu marches jusqu'au bout !",
            "narrateur|Le cheval glisse au milieu.",
            "narrateur|Le carton se lève d'un côté.",
            "enfant-m|Oh.",
            "narrateur|Le cheval penche vers le sol.",
            "enfant-m|Je le prends !",
            "narrateur|Nino avance la main vers Victorina.",
            "papa|Tu l'attends, Nino ?",
            "narrateur|Victorina ne bouge pas.",
            "narrateur|Ses mains restent sur ses genoux.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Nino s'arrête net.",
            "narrateur|Papa attend, sans parler.",
            "enfant-m|Je regarde.",
            "narrateur|Nino observe la plaque, écoute la cuisine.",
            "narrateur|Sur le bord, un éclat de plaque luit.",
            "enfant-m|Là, près des gâteaux.",
            "narrateur|Nino tient le cheval des deux mains.",
            "narrateur|Le carton est rêche, un peu tiède.",
            "enfant-m|Il est tiède, papa.",
            "papa|Tu le portes jusqu'au bout ?",
            "enfant-m|Oui, papa.",
            "maman|On avance ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nino pose le cheval au début.",
            "narrateur|Il pousse, très peu.",
            "enfant-m|Il passe.",
            "copine|Le mouton aussi, après.",
            "narrateur|Victorina tend la main.",
            "narrateur|Elle pose le mouton près du pont.",
            "papa|Tu le tiens, Nino ?",
            "enfant-m|Oui.",
            "narrateur|Les sabots tapent, puis se taisent.",
            "narrateur|Le cheval arrive de l'autre côté.",
            "enfant-m|Il est passé.",
            "maman|Les gâteaux sont tièdes.",
            "papa|On plie le pont ?",
            "enfant-m|Oui.",
            "narrateur|Nino plie le carton.",
            "narrateur|Les lettres bleues se plient aussi.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "cuisine",
        [
            "enfant-m|La plaque brillait, papa.",
            "papa|Tu le vois, comme tout à l'heure ?",
            "enfant-m|Oui, sur le bord.",
            "narrateur|Nino pose le cheval près du mouton.",
            "maman|On les garde près de nous ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Ça sentait le beurre.",
            "maman|Les gâteaux sont là.",
            "narrateur|La plaque ne fume plus.",
            "narrateur|Nino respire, plus large.",
            "papa|On reste un peu ?",
            "enfant-m|Oui.",
            "narrateur|Les joues de Nino se réchauffent.",
            "narrateur|Le cheval reste tiède sous la main.",
            "narrateur|Un éclat de plaque reste pâle.",
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
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"extra {bad}: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-m", "copine"):
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
    out["pitch_xai_tag"] = m.get("pitchTag")
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
    if "farine" not in blob:
        raise SystemExit(f"{SID}: farine du dump absente")
    if "éclat de farine" in blob:
        raise SystemExit(f"{SID}: éclat de farine (BAN)")
    if "carton de céréales" not in blob and "carton de cereales" not in blob:
        raise SystemExit(f"{SID}: carton de céréales absent")
    if "beurre" not in blob:
        raise SystemExit(f"{SID}: beurre absent")
    if re.search(r"\btom\b", blob):
        raise SystemExit(f"{SID}: Tom interdit")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if "copine" not in roles:
        raise SystemExit(f"{SID}: Victorina absente (copine)")
    if "enfant-m" not in roles:
        raise SystemExit(f"{SID}: Nino absent")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if "victorina ne dit rien" not in blob:
        raise SystemExit(f"{SID}: silence Victorina absent")
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Nino invite Victorina. Que fait-on ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "proposer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt", "").lower()
    if "proposer" not in retry:
        raise SystemExit(f"{SID}: retry sans proposer")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on peut proposer",
        "on peut accepter",
        "plusieurs réponses",
        "j'ai proposé",
        "j'ai accepté",
        "proposer",
        "inviter",
        "accepter",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
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
    for ban in (
        "carte", "boule", "galet", "cube", "bois", "couloir",
        "poussière", "poussiere", "cour",
    ):
        if re.search(rf"\b{ban}\b", blob):
            raise SystemExit(f"{SID}: BAN {ban}")
    if "tout doux" in blob:
        raise SystemExit(f"{SID}: tic tout doux")

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
        "- **Public :** N1 (≤10 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.BES.002 — inviter / proposer / accepter "
        "(vécue : Nino tend trop vite, Victorina dit non ; il attend "
        "son silence, dit d'accord ; elle pose le mouton plus tard)\n"
        "- **Personnages :** Nino, Victorina, papa, maman. Troupe D16 "
        "gardée. Deux rythmes : Nino propose, Victorina prend son temps "
        "ou pose sa limite. Le silence compte. Adultes parlants = "
        "papa/maman.\n"
        "- **Lieu :** cuisine après gâteaux, carton de céréales, plaque, "
        "beurre, farine sur les manches (monde dump, pas indice).\n"
        "- **Indice unique :** éclat de plaque (luit à l'ouverture, "
        "touché, luit au refus, reste pâle). Pas éclat de farine. Pas "
        "carte / boule / galet / cube / bois / couloir / poussière / "
        "cour. Pas POL/ECO.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La plaque de gâteaux fume. Ça sent le beurre. Sur le bord, un "
        "éclat de plaque luit. Farine sur les manches. Carton de céréales "
        "plié en pont. Nino veut le cheval sur le pont **maintenant**, "
        "avec Victorina. Première idée : « Tu viens ? » trop vite, cheval "
        "poussé d'un coup. Elle dit non. Le pont se plie. Sourire parti, "
        "épaules basses. Papa se baisse. Il refuse de foncer. Il attend "
        "son silence. « Tu regardes ? » Elle regarde. « D'accord. » Merci "
        "vécu. Le cheval glisse au milieu. Il tend la main vers elle : "
        "elle ne bouge pas. Il s'arrête, lit l'éclat. Le cheval passe. "
        "Elle pose le mouton. Un éclat de plaque reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine après gâteaux, plaque, beurre, farine sur les "
        "manches, carton de céréales, buffet, chaussettes jaunes.\n"
        "- Désir : le cheval sur le pont, maintenant, avec Victorina.\n"
        "- Objet : cheval peint, mouton, pont de carton, plaque.\n"
        "- Indice unique : éclat de plaque, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : Victorina à la porte, le cheval qui doit passer.\n"
        "- Imprévu 1 : invitation trop vite, cheval poussé, pont plié, non.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après d'accord.\n"
        "- Imprévu 2 (plus rusé) : cheval qui glisse ; il veut sa main ; "
        "elle ne bouge pas.\n"
        "- Résolution : il refuse de foncer, attend, dit d'accord ; elle "
        "pose le mouton quand elle veut.\n"
        "- Retour : cheval près du mouton, plaque sans fumée, éclat pâle.\n\n"
        "## Vécu\n\n"
        "Nino veut le cheval et Victorina **maintenant**. Impatience "
        "(main trop vite, voix trop grande), puis sourire qui disparaît. "
        "Papa se baisse, pose une question, ne récite pas la règle. "
        "Victorina dit non, puis rien, puis je regarde, puis plus tard. "
        "Nino dit d'accord. Merci vécu après l'écoute. Fin : l'éclat du "
        "début reste pâle.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le cheval et le pont (noyau dump). Troupe D16 gardée : "
        "Nino, Victorina, papa, maman. Pas Tom / Ava du TTS source.\n"
        "- Lieu du dump (cuisine après gâteaux, carton de céréales, "
        "farine sur les manches, plaque, beurre). Farine = monde, pas "
        "indice. ≠ POL marché / boulangerie. ≠ ECO. ≠ BES.001 carte / "
        "boule / galet / cube / bois.\n"
        "- Ouverture inventée (plaque qui fume, beurre), pas un gabarit "
        "v2, pas « Nino est dans la cuisine ».\n"
        "- Indice unique : éclat de plaque. Pas éclat de farine, pas "
        "carte, boule, galet, cube, bois, couloir, poussière, cour, pas "
        "POL/ECO.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » du dump.\n"
        "- Leçon non dite : pas « on peut proposer », pas « plusieurs "
        "réponses », pas « j'ai proposé ». On la voit quand il attend "
        "le silence et dit d'accord.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Nino invite Victorina. Que fait-on ? » "
        "expected proposer. retry inchangé. 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le cheval.\n"
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
