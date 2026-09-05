#!/usr/bin/env python3
"""ATOM-EMO.LEX.003-02 — Amir, le canard et le miel (F-NAR-019, N3, EMO.LEX.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.003-02"
TITLE = "Amir, le canard et le miel"
N3 = LIMITS["N3"]
CHARS = "Amir, papa, maman"
SETTING = (
    "parc, puis cuisine, kiosque, volet, crochet, herbe, "
    "eau, pain, placard, canard, bateau, confiture, miel"
)
INDICE = "éclat de kiosque"
FIL = (
    "Une cheville de bois tient le volet. Sur le bois peint, "
    "un éclat de kiosque luit. Amir veut le bateau bleu, "
    "maintenant. Le crochet est vide. Sourire parti. Papa "
    "s'accroupit. Je suis déçu. Merci vécu. Un canard en bois. "
    "Deuxième ruse : plus de confiture, le pot glisse. Il refuse "
    "de foncer. Il propose le miel. Un éclat de kiosque tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(merle|treille|moule|tuteur|saladier|gomme|berge|"
    r"brouette|couverture|capuche|paillasson|fauteuil|coffre|"
    r"haie|housse|cagette|banc|flaque|tasse|casserole|"
    r"maîtresse|maitresse|grand-père|grand-pere|jardinier|"
    r"bibliothécaire|bibliothecaire|gardienne|fontaine|"
    r"tabouret|torchon|plaid|coussin)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "maîtresse",
    "maitresse",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai dit",
    "j ai dit",
    "tu as nommé",
    "tu as nomme",
    "on nomme",
    "c'est de la joie",
    "c est de la joie",
    "être déçu, ce n'est pas",
    "etre decu, ce n'est pas",
    "un souhait peut attendre",
    "on peut chercher une autre idée",
    "on peut chercher une autre idee",
    "c'est une autre idée",
    "c est une autre idee",
    "lumière couleur de miel",
    "lumiere couleur de miel",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "les trois mots",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "il ne faut pas rire",
    "on ne rit pas",
    "bravo. tu as",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de cagette",
    "éclat de bateau",
    "éclat de miel",
    "éclat de banc",
    "éclat de flaque",
    "éclat de treille",
    "éclat de moule",
    "éclat de tuteur",
    "éclat de saladier",
    "éclat de gomme",
    "éclat de berge",
    "éclat de brouette",
    "éclat de couverture",
    "éclat de capuche",
    "éclat de paillasson",
    "éclat de fauteuil",
    "éclat de coffre",
    "éclat de haie",
    "éclat de housse",
    "éclat de tasse",
    "éclat de casserole",
    "éclat de tour",
    "éclat de cube",
    "éclat de rideau",
    "éclat de tapis",
    "éclat de comptoir",
    "éclat de canard",
    "éclat de crochet",
    "éclat de volet",
    "éclat de pain",
    "éclat de placard",
    "éclat de pot",
    "toute calme",
    "tout calme",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de kiosque",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis déception; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_bateau_bleu_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Amir",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_bateau_n_est_plus_la_que_dit_amir; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="canard",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_prend_le_canard_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de kiosque",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=plus_de_confiture_il_refuse_de_foncer_il_propose_le_miel; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de kiosque",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "déçu",
    "accepted_examples": (
        "déçu | je suis déçu | autre idée | un canard | une autre idée"
    ),
    "retry_prompt": "Amir cherche une autre idée. Que dit-il d'abord ?",
    "engine_ok_text": "Oui, déçu.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc",
        [
            "narrateur|Une cheville de bois tient le volet du kiosque.",
            "enfant-m|Elle est coincée, papa.",
            "papa|Tu la vois, la cheville ?",
            "enfant-m|Oui, papa.",
            "narrateur|La sandale d'Amir tord sa lanière.",
            "enfant-m|Elle serre, maman.",
            "maman|Tu la lâches, la lanière ?",
            "enfant-m|Oui, maman.",
            "narrateur|Papa défait le nœud, près du kiosque.",
            "enfant-m|Mes orteils bougent.",
            "papa|Ils sont libres, Amir ?",
            "enfant-m|Oui.",
            "narrateur|C'est le kiosque des petits bateaux.",
            "enfant-m|Des petits bateaux.",
            "maman|Tu le vois, le kiosque ?",
            "enfant-m|Oui, maman.",
            "narrateur|La peinture du kiosque est tiède, un peu poudreuse.",
            "enfant-m|Elle colle un peu.",
            "papa|Tu la touches, la peinture ?",
            "enfant-m|Oui, papa.",
            "narrateur|Sur le bois peint, un éclat de kiosque luit.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-m|Oui, un point clair.",
            "narrateur|Un sac en papier froisse dans la main de maman.",
            "enfant-m|Il fait du bruit.",
            "maman|Tu l'entends, le papier ?",
            "enfant-m|Oui.",
            "narrateur|Une corde pend sous le volet, trop courte.",
            "enfant-m|Elle ne touche pas.",
            "papa|Tu la vois, la corde ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le parc sent l'herbe coupée, près des genoux.",
            "enfant-m|Ça sent l'herbe.",
            "maman|Tu la sens, l'herbe chaude ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un crochet vide attend sous le volet.",
            "enfant-m|Il n'a rien.",
            "papa|On regarde le crochet ?",
            "enfant-m|Oui.",
            "narrateur|En ce moment, Amir cherche un bateau bleu.",
            "enfant-m|Le bleu, pour l'eau !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|Amir se hausse vers le crochet, trop vite.",
            "narrateur|Sa main trouve du vide.",
            "enfant-m|Il n'y en a plus.",
            "maman|Le bateau bleu ?",
            "enfant-m|Parti.",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "enfant-m|J'ai mal au ventre.",
            "papa|Tu as les épaules lourdes, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "maman|Tes mains sont chaudes, Amir ?",
            "enfant-m|Un peu, maman.",
            "enfant-m|Je suis déçu.",
            "narrateur|L'éclat de kiosque tremble, puis tient.",
            "papa|Tu vois le crochet vide ?",
            "enfant-m|Oui.",
            "narrateur|Amir serre les poings, puis les ouvre.",
            "papa|Tes poings, Amir ?",
            "enfant-m|Ils se desserrent.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Le bateau n'est plus là.",
            "narrateur|Que dit Amir ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Amir avance la main vers le bois, trop vite.",
            "enfant-m|Je prends tout, maintenant !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-m|N'importe quoi.",
            "narrateur|Amir avance les mains, trop vite.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Amir refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le kiosque, un instant.",
            "narrateur|Il écoute le parc, près du volet.",
            "enfant-m|Celui-là.",
            "narrateur|Un canard en bois attend, près du crochet.",
            "papa|Tu le prends, Amir ?",
            "enfant-m|Oui, le canard.",
            "papa|Merci, Amir.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le bois est froid, sous les doigts.",
            "enfant-m|Il est lisse.",
            "narrateur|Ils marchent vers l'eau, sans se presser.",
            "narrateur|Amir pose le canard, tout petit.",
            "enfant-m|Il glisse !",
            "papa|Tu le vois, sur l'eau ?",
            "enfant-m|Oui, papa.",
            "maman|Le bois tient, Amir ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le ventre d'Amir se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On rentre, après l'eau ?",
            "enfant-m|Oui.",
            "narrateur|Amir reprend le canard, sans se bousculer.",
            "enfant-m|Il vient avec nous.",
            "maman|Tes mains sont au chaud, Amir ?",
            "enfant-m|Un peu, maman.",
            "papa|La cuisine, plus tard.",
            "enfant-m|Oui, papa.",
            "narrateur|Le canard reste contre sa chemise.",
            "enfant-m|Il est un peu mouillé.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|La cuisine sent le pain chaud.",
            "enfant-m|Ça sent le pain, maman.",
            "maman|Tu le sens, le pain ?",
            "enfant-m|Oui.",
            "narrateur|Le canard repose près du pain.",
            "enfant-m|De la confiture, maintenant !",
            "narrateur|Amir ouvre le placard, trop vite.",
            "narrateur|Un pot de fraise tremble, presque vide.",
            "enfant-m|Il n'y en a plus.",
            "maman|La confiture de fraise ?",
            "enfant-m|Parti.",
            "narrateur|Les épaules d'Amir retombent.",
            "enfant-m|Je la prends, tout de suite !",
            "narrateur|Amir avance trop vite vers le pot.",
            "narrateur|Le pot glisse au bord.",
            "enfant-m|Il part !",
            "narrateur|Amir avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Amir refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le placard, un instant.",
            "narrateur|Il écoute la cuisine, près du pain.",
            "narrateur|Sur le bois du canard, un éclat de kiosque luit.",
            "enfant-m|Là, sur le bois.",
            "papa|On tient le pot ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le couvercle du miel résiste, un moment.",
            "enfant-m|Le miel, alors.",
            "maman|Tu le vois, le pot ?",
            "enfant-m|Oui, maman.",
            "narrateur|Papa tourne le couvercle, sans se presser.",
            "narrateur|Le couvercle cède, tout petit.",
            "enfant-m|Il s'ouvre !",
            "narrateur|Ils tartinent le pain, ensemble.",
            "papa|Le pain est prêt, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le miel colle un peu au pain.",
            "enfant-m|Ça tient.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la table.",
            "narrateur|Maman essuie un peu de pain.",
            "enfant-m|Le bateau n'était pas là, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, le crochet vide.",
            "maman|On est bien, ici.",
            "narrateur|Amir tapote le canard du doigt.",
            "enfant-m|Il a une trace de peinture.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|Le canard est resté, Amir.",
            "enfant-m|Oui, avec le pain.",
            "narrateur|Ça sent le pain, un peu tiède.",
            "enfant-m|Et le bois, maman.",
            "maman|Oui, dans l'air.",
            "papa|La cuisine est calme, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le canard reste près du pain.",
            "narrateur|Un éclat de kiosque tient sur le bois.",
        ],
    ),
}


def vet(lines: list[str], cid: str = "") -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    skip_q = cid == "CHK_T0000_P0000_Q0001"
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
        if not skip_q and TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        if not skip_q:
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
    cid = src.get("chunk_id") or ""
    lines = vet(lines, cid)
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
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Amir = enfant-m)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé (dump sans camarade)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "enfant-m" for r in roles):
        raise SystemExit(f"{SID}: enfant-m absent")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "j'ai dit",
        "j ai dit",
        "tu as nommé",
        "tu as nomme",
        "on nomme",
        "être déçu, ce n'est pas",
        "un souhait peut attendre",
        "on peut chercher une autre idée",
        "c'est une autre idée",
        "lumière couleur de miel",
        "lumiere couleur de miel",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Le bateau n'est plus là. Que dit Amir ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "déçu":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "déçu | je suis déçu | autre idée | un canard | une autre idée"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Amir cherche une autre idée. Que dit-il d'abord ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    for c in chunks:
        if c["chunk_id"] == "CHK_T0000_P0000_Q0001":
            continue
        if c.get("expected_answer") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: expected hors Q")
        if c.get("accepted_examples") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: accepted hors Q")
        if c.get("retry_prompt") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: retry hors Q")
        if c.get("engine_ok_text") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: engine_ok hors Q")
        if c.get("engine_near_text") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: engine_near hors Q")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "je suis déçu" not in opening:
        raise SystemExit(f"{SID}: nommage absent avant la question")
    n_decu = blob.count("je suis déçu")
    if n_decu != 1:
        raise SystemExit(f"{SID}: je suis déçu ×{n_decu}")
    if "s'accroupit" not in opening and "s accroupit" not in opening:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    if "sourire" not in opening or "disparaît" not in opening:
        raise SystemExit(f"{SID}: manque sourire disparu")
    if "parc" not in blob:
        raise SystemExit(f"{SID}: manque parc")
    if "cuisine" not in blob:
        raise SystemExit(f"{SID}: manque cuisine")
    if "bateau" not in blob:
        raise SystemExit(f"{SID}: manque bateau")
    if "canard" not in blob:
        raise SystemExit(f"{SID}: manque canard")
    if "confiture" not in blob:
        raise SystemExit(f"{SID}: manque confiture")
    if "miel" not in blob:
        raise SystemExit(f"{SID}: manque miel")
    if "kiosque" not in blob:
        raise SystemExit(f"{SID}: manque kiosque")
    if INDICE not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé au climax")
    for ban in (
        "éclat de bateau",
        "éclat de miel",
        "éclat de tasse",
        "éclat de casserole",
        "éclat de banc",
        "éclat de flaque",
        "éclat de cagette",
        "éclat de treille",
        "éclat de moule",
        "éclat de tuteur",
        "éclat de saladier",
        "éclat de gomme",
        "éclat de berge",
        "éclat de brouette",
        "éclat de couverture",
        "éclat de capuche",
        "tout doux",
        "tout calme",
        "merle",
        "lumière couleur de miel",
        "j'ai dit : je suis",
    ):
        if ban in blob:
            raise SystemExit(f"{SID}: BAN {ban}")
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
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 700 or nwords > 850:
        raise SystemExit(f"{SID}: {nwords} mots hors 700–850")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N3 (≤16 mots/phrase), audio familial, voc 5–6 ans\n"
        "- **Leçon :** EMO.LEX.003 — nommer la déception + autre idée "
        "(vécue : crochet vide, sourire parti, poitrine qui se bouscule, "
        "papa accroupi, Amir dit « je suis déçu », prend le canard ; "
        "2e ruse : plus de confiture, le pot glisse, il refuse de "
        "foncer, propose le miel). JAMAIS dite en slogan. Pas « j'ai "
        "dit : je suis ». Pas « tu as nommé ». Pas « un souhait peut "
        "attendre ». Pas « lumière couleur de miel ».\n"
        "- **Personnages :** Amir, papa, maman. Dump Ilyes → D16 Amir "
        "= enfant-m (veut le bateau bleu maintenant). Pas de copain "
        "(dump sans camarade). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** parc, puis cuisine (2 lieux). Coin nommé : "
        "kiosque des petits bateaux. Dump : bateau, canard, "
        "confiture, miel (objet, pas refrain sensoriel). Indice "
        "PAS bateau / miel / tasse / casserole / banc / flaque.\n"
        "- **Indice unique :** éclat de kiosque (luit sur le bois "
        "peint → tremble au crochet vide → luit sur le canard au "
        "climax cuisine → tient sur le bois). BAN éclat de bateau / "
        "miel / tasse / casserole / banc / flaque / cagette.\n"
        "- **Question moteur :** « Le bateau n'est plus là. Que dit "
        "Amir ? » expected dump **déçu**. accepted dump `déçu | je "
        "suis déçu | autre idée | un canard | une autre idée`. retry "
        "dump Ilyes → Amir : `Amir cherche une autre idée. Que "
        "dit-il d'abord ?`. Hors Q : null. Non récitée ailleurs.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / "
        "graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin "
        "heureuse. `chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une cheville de bois tient le volet du kiosque. Sandale, "
        "lanière, peinture tiède. Sur le bois peint, un éclat de "
        "kiosque luit. Amir veut le bateau bleu **maintenant**. "
        "Le crochet est vide. Sourire parti. Envie et inquiétude. "
        "Papa s'accroupit. Je suis déçu. Merci vécu. Un canard en "
        "bois glisse sur l'eau. Deuxième ruse : plus de confiture, "
        "le pot glisse. Il s'arrête, lit l'éclat, propose le miel. "
        "Le couvercle résiste, puis cède. Un éclat de kiosque tient "
        "sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : parc, kiosque des petits bateaux, volet, "
        "cheville, sandale, herbe, puis cuisine, pain, placard.\n"
        "- Désir : un bateau bleu pour l'eau, maintenant.\n"
        "- Objet : bateau manquant, canard en bois, pot de "
        "confiture vide, pot de miel.\n"
        "- Indice unique : éclat de kiosque, vu dès l'ouverture, "
        "payé sur le bois du canard. Pas éclat de bateau / miel / "
        "tasse / casserole / banc / flaque.\n"
        "- Urgence douce : il se hausse trop vite vers le crochet.\n"
        "- Imprévu 1 : bateau parti, crochet vide, sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "qu'il refuse de foncer et prend le canard.\n"
        "- Imprévu 2 (plus rusé) : plus de confiture, le pot "
        "glisse, le couvercle du miel résiste.\n"
        "- Résolution : il refuse de foncer, observe, écoute la "
        "cuisine, retrouve l'éclat, propose le miel.\n"
        "- Retour : pain tartiné, canard près du pain, éclat sur "
        "le bois. La fin a failli (couvercle coincé, pot qui glisse).\n\n"
        "## Vécu\n\n"
        "Amir veut le bateau **maintenant**. Impatience, puis "
        "crochet vide, sourire parti. Il dit je suis déçu. Papa se "
        "baisse, pose une question, ne récite pas la leçon. Ils "
        "agissent : canard sur l'eau, puis cuisine, pot vide, il "
        "s'arrête. Merci vécu. Fin : l'éclat du début tient sur "
        "le bois du canard.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Amir, le canard et le miel (noyau dump, miel "
        "dans le titre = objet dump OK). Relance : Que dit Amir ? "
        "expected déçu.\n"
        "- Lieu du dump-meta (parc, puis cuisine). Maman et papa. "
        "Amir = héros enfant-m. Dump bateau / canard / confiture / "
        "miel gardés comme objets, pas comme indice.\n"
        "- Ouverture inventée (cheville de bois, volet, sandale), "
        "pas un gabarit v2, pas gouttes/fontaine du merged, pas "
        "« Ilyes marche au parc ».\n"
        "- Indice unique : éclat de kiosque ×4. BAN éclat de "
        "bateau / miel / tasse / casserole / banc / flaque / "
        "cagette. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « j'ai dit : je suis ». Strip « lumière "
        "couleur de miel » (miel = pot, pas refrain sensoriel).\n"
        "- Leçon non dite : on la voit quand le crochet est vide, "
        "quand il dit je suis déçu, quand il prend le canard, "
        "quand il propose le miel. Pas « tu as nommé ». Une seule "
        "« je suis déçu ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Le bateau n'est plus là. Que dit "
        "Amir ? ». expected/accepted dump. retry Ilyes → Amir. "
        "Hors Q : null. 5 chunks, kinds inchangés.\n"
        "- example4 069 / 001 / 033 (manière volée, gabarit non "
        "collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N3.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, "
        "sous-texte, tempo, sourire, respiration). `slow` = "
        "question et fin. Action un peu plus vive vers le pot "
        "qui glisse.\n"
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
