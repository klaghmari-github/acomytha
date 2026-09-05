#!/usr/bin/env python3
"""ATOM-EMO.LEX.003-05 — Raphaël et la porte fermée (F-NAR-019, N3, EMO.LEX.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.003-05"
TITLE = "Raphaël et la porte fermée"
N3 = LIMITS["N3"]
CHARS = "Raphaël, papa, maman"
SETTING = (
    "rue de la bibliothèque puis maison, store, façade, "
    "porte, sac, table, corbeille, fraises, pomme, livre"
)
INDICE = "éclat de store"
FIL = (
    "La barre de fer est froide. Sur les lamelles, "
    "un éclat de store luit. Raphaël veut entrer, "
    "maintenant. La porte est fermée. Sourire parti. Papa "
    "s'accroupit. Je suis déçu. Merci vécu. Ils lisent "
    "à la maison. Deuxième ruse : plus de fraises, la pomme "
    "glisse. Il refuse de foncer. Il choisit une pomme. "
    "Un éclat de store tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(merle|miel|treille|moule|tuteur|saladier|gomme|berge|"
    r"brouette|couverture|capuche|paillasson|fauteuil|coffre|"
    r"haie|housse|cagette|kiosque|pelle|ficelle|banc|flaque|"
    r"tasse|casserole|maîtresse|maitresse|grand-père|grand-pere|"
    r"jardinier|bibliothécaire|bibliothecaire|gardienne|fontaine|"
    r"tabouret|torchon|plaid|coussin|vitre|volet|sonnette|"
    r"ugo)\b",
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
    "éclat de kiosque",
    "éclat de pelle",
    "éclat de ficelle",
    "éclat de livre",
    "éclat de vitre",
    "éclat de volet",
    "éclat de sonnette",
    "éclat de clé",
    "éclat de cle",
    "éclat de porte",
    "éclat de pomme",
    "éclat de fraise",
    "éclat de sac",
    "éclat de table",
    "éclat de corbeille",
    "éclat de façade",
    "éclat de facade",
    "éclat de barre",
    "éclat de fer",
    "éclat de lamelle",
    "toute calme",
    "tout calme",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de store",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis déception; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_entrer_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Raphaël",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_bibliotheque_est_fermee_que_dit_raphael; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="livre",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_propose_de_lire_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de store",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=plus_de_fraises_il_refuse_de_foncer_il_choisit_une_pomme; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de store",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_tissu; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "déçu",
    "accepted_examples": (
        "déçu | je suis déçu | autre idée | une pomme | une autre idée"
    ),
    "retry_prompt": "Raphaël cherche une autre idée. Que dit-il d'abord ?",
    "engine_ok_text": "Oui, déçu.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "rue,store",
        [
            "narrateur|La barre de fer est froide, près du trottoir.",
            "enfant-m|Elle pique, papa.",
            "papa|Tu la touches, la barre ?",
            "enfant-m|Oui, papa.",
            "narrateur|Maman pose un sac contre sa jambe.",
            "enfant-m|Il est lourd, maman.",
            "maman|Tu le portes un peu, Raphaël ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Raphaël connaît la rue de la bibliothèque.",
            "enfant-m|C'est notre rue.",
            "papa|Tu la reconnais, la rue ?",
            "enfant-m|Oui, papa.",
            "narrateur|Un détail paraît nouveau, près de la façade.",
            "enfant-m|Le store est baissé.",
            "maman|Tu le vois, le store ?",
            "enfant-m|Oui, maman.",
            "narrateur|Les lamelles du store font un bruit sec.",
            "enfant-m|Ça claque un peu.",
            "papa|Tu l'entends, le clac ?",
            "enfant-m|Oui.",
            "narrateur|Sur les lamelles, un éclat de store luit.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-m|Oui, un point clair.",
            "narrateur|Le sac froisse, près des genoux de maman.",
            "enfant-m|Il fait du bruit.",
            "maman|Tu l'entends, le sac ?",
            "enfant-m|Oui.",
            "narrateur|Le bouton du manteau tape le sac.",
            "enfant-m|Il fait toc.",
            "papa|Tu l'entends, le toc ?",
            "enfant-m|Oui, papa.",
            "narrateur|La porte de la bibliothèque attend, trop loin.",
            "enfant-m|On y va !",
            "papa|On avance, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les chaussures tapent le trottoir, trop vite.",
            "enfant-m|J'ai hâte.",
            "maman|Tes pieds courent, Raphaël ?",
            "enfant-m|Un peu, maman.",
            "narrateur|En ce moment, Raphaël tend la main vers la porte.",
            "enfant-m|Je veux entrer, maintenant !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|Raphaël pousse la porte, trop vite.",
            "narrateur|La porte ne bouge pas.",
            "enfant-m|Elle est fermée.",
            "maman|La bibliothèque, Raphaël ?",
            "enfant-m|Fermée.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "enfant-m|J'ai mal au ventre.",
            "papa|Tu as les épaules lourdes, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "maman|Tes mains sont chaudes, Raphaël ?",
            "enfant-m|Un peu, maman.",
            "enfant-m|Je suis déçu.",
            "narrateur|L'éclat de store tremble, puis tient.",
            "papa|Tu vois la porte fermée ?",
            "enfant-m|Oui.",
            "narrateur|Raphaël serre les poings, puis les ouvre.",
            "papa|Tes poings, Raphaël ?",
            "enfant-m|Ils se desserrent.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|La bibliothèque est fermée.",
            "narrateur|Que dit Raphaël ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Raphaël avance la main vers la porte, trop vite.",
            "enfant-m|J'ouvre, maintenant !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-m|N'importe quoi.",
            "narrateur|Raphaël avance les mains, trop vite.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Raphaël refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le store, un instant.",
            "narrateur|Il écoute la rue, près de la façade.",
            "enfant-m|À la maison, alors.",
            "papa|Tu lis à la maison ?",
            "enfant-m|Oui, un livre.",
            "papa|Merci, Raphaël.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le sac est froid, sous les doigts.",
            "enfant-m|Il pique un peu.",
            "narrateur|Ils marchent vers la maison, sans se presser.",
            "narrateur|Raphaël tient le sac, tout petit.",
            "enfant-m|Il est lourd.",
            "papa|Tu le portes, Raphaël ?",
            "enfant-m|Oui, papa.",
            "maman|Tes pieds sont lents, Raphaël ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le ventre de Raphaël se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On rentre, après la rue ?",
            "enfant-m|Oui.",
            "narrateur|Raphaël reprend le sac, sans se bousculer.",
            "enfant-m|Il vient avec nous.",
            "maman|Tes mains sont au chaud, Raphaël ?",
            "enfant-m|Un peu, maman.",
            "papa|La maison, plus tard.",
            "enfant-m|Oui, papa.",
            "narrateur|Le sac reste contre sa chemise.",
            "enfant-m|Il est un peu froid.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|La maison sent le bois, près de la table.",
            "enfant-m|Ça sent le bois, maman.",
            "maman|Tu le sens, le bois ?",
            "enfant-m|Oui.",
            "narrateur|Un livre de trains attend sur la table.",
            "enfant-m|Des fraises, maintenant !",
            "narrateur|Raphaël ouvre la corbeille, trop vite.",
            "narrateur|La corbeille tremble, presque vide.",
            "enfant-m|Il n'y en a plus.",
            "maman|Les fraises, Raphaël ?",
            "enfant-m|Parti.",
            "narrateur|Les épaules de Raphaël retombent.",
            "enfant-m|Je les prends, tout de suite !",
            "narrateur|Raphaël avance trop vite vers la corbeille.",
            "narrateur|Une pomme glisse au bord.",
            "enfant-m|Elle part !",
            "narrateur|Raphaël avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Raphaël refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe la corbeille, un instant.",
            "narrateur|Il écoute la maison, près du store.",
            "narrateur|Sur le store, un éclat de store luit.",
            "enfant-m|Là, sur le store.",
            "papa|On tient la pomme ?",
            "enfant-m|Oui, papa.",
            "narrateur|La peau de la pomme résiste, un moment.",
            "enfant-m|Une pomme, alors.",
            "maman|Tu la vois, la pomme ?",
            "enfant-m|Oui, maman.",
            "narrateur|Papa coupe la pomme, sans se presser.",
            "narrateur|La pomme cède, tout petit.",
            "enfant-m|Elle s'ouvre !",
            "narrateur|Ils lisent le livre, ensemble.",
            "papa|Le train est prêt, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le jus de pomme colle un peu au doigt.",
            "enfant-m|Ça tient.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la table.",
            "narrateur|Maman essuie un peu de jus.",
            "enfant-m|La porte n'était pas ouverte, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-m|Oui, la porte fermée.",
            "maman|On est bien, ici.",
            "narrateur|Raphaël tapote le livre du doigt.",
            "enfant-m|Il a une trace de jus.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|La pomme est restée, Raphaël.",
            "enfant-m|Oui, avec le livre.",
            "narrateur|Ça sent le bois, un peu tiède.",
            "enfant-m|Et le store, maman.",
            "maman|Oui, dans l'air.",
            "papa|La maison est tiède, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le livre reste près de la pomme.",
            "narrateur|Un éclat de store tient sur le tissu.",
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
        raise SystemExit(f"{SID}: enfant-f (Raphaël = enfant-m)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé (dump sans camarade)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    if "bibliothécaire" in blob or "bibliothecaire" in blob:
        raise SystemExit(f"{SID}: bibliothécaire")
    if "ugo" in blob:
        raise SystemExit(f"{SID}: Ugo resté")
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
    if q["text"] != "La bibliothèque est fermée. Que dit Raphaël ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "déçu":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "déçu | je suis déçu | autre idée | une pomme | une autre idée"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Raphaël cherche une autre idée. Que dit-il d'abord ?":
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
    if "bibliothèque" not in blob and "bibliotheque" not in blob:
        raise SystemExit(f"{SID}: manque bibliothèque")
    if "maison" not in blob:
        raise SystemExit(f"{SID}: manque maison")
    if "porte" not in blob:
        raise SystemExit(f"{SID}: manque porte")
    if "fraise" not in blob:
        raise SystemExit(f"{SID}: manque fraises")
    if "pomme" not in blob:
        raise SystemExit(f"{SID}: manque pomme")
    if "store" not in blob:
        raise SystemExit(f"{SID}: manque store")
    if INDICE not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé au climax")
    for ban in (
        "éclat de vitre",
        "éclat de volet",
        "éclat de sonnette",
        "éclat de clé",
        "éclat de livre",
        "éclat de cagette",
        "éclat de kiosque",
        "éclat de pelle",
        "éclat de ficelle",
        "éclat de porte",
        "éclat de pomme",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "j'ai dit : je suis",
        "ugo",
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
        "(vécue : porte fermée, sourire parti, poitrine qui se bouscule, "
        "papa accroupi, Raphaël dit « je suis déçu », propose de lire "
        "à la maison ; 2e ruse : plus de fraises, la pomme glisse, il "
        "refuse de foncer, choisit une pomme). JAMAIS dite en slogan. "
        "Pas « j'ai dit : je suis ». Pas « tu as nommé ». Pas « un "
        "souhait peut attendre ». Pas de bibliothécaire qui parle.\n"
        "- **Personnages :** Raphaël, papa, maman. Dump Ugo → D16 "
        "Raphaël = enfant-m (veut entrer maintenant). Maman ajoutée. "
        "Pas de copain (dump sans camarade). Troupe D16. Pas de "
        "maîtresse. Pas de bibliothécaire.\n"
        "- **Lieu :** rue de la bibliothèque puis maison (2 lieux). "
        "Coin nommé : store de la façade. Dump : porte, fraises, "
        "pomme, livre (objet, pas indice). Indice PAS vitre / volet / "
        "sonnette / clé / livre.\n"
        "- **Indice unique :** éclat de store (luit sur les lamelles "
        "→ tremble à la porte fermée → luit sur le store au climax "
        "maison → tient sur le tissu). BAN éclat de vitre / volet / "
        "sonnette / clé / livre / cagette / kiosque / pelle / ficelle.\n"
        "- **Question moteur :** « La bibliothèque est fermée. Que dit "
        "Raphaël ? » expected dump **déçu**. accepted dump `déçu | je "
        "suis déçu | autre idée | une pomme | une autre idée`. retry "
        "dump Ugo → Raphaël : `Raphaël cherche une autre idée. Que "
        "dit-il d'abord ?`. Hors Q : null. Non récitée ailleurs.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / "
        "graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin "
        "heureuse. `chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La barre de fer est froide. Sac, manteau, lamelles. Sur les "
        "lamelles, un éclat de store luit. Raphaël veut entrer "
        "**maintenant**. La porte est fermée. Sourire parti. Envie et "
        "inquiétude. Papa s'accroupit. Je suis déçu. Merci vécu. Ils "
        "lisent à la maison. Deuxième ruse : plus de fraises, la pomme "
        "glisse. Il s'arrête, lit l'éclat, choisit une pomme. La peau "
        "résiste, puis cède. Un éclat de store tient sur le tissu.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : rue de la bibliothèque, store de la façade, barre "
        "de fer, sac, puis maison, table, corbeille, livre.\n"
        "- Désir : entrer à la bibliothèque, maintenant.\n"
        "- Objet : porte fermée, livre de trains, corbeille vide, pomme.\n"
        "- Indice unique : éclat de store, vu dès l'ouverture, payé "
        "sur le store de la maison. Pas éclat de vitre / volet / "
        "sonnette / clé / livre.\n"
        "- Urgence douce : il pousse la porte trop vite.\n"
        "- Imprévu 1 : porte fermée, sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après qu'il "
        "refuse de foncer et propose de lire à la maison.\n"
        "- Imprévu 2 (plus rusé) : plus de fraises, la pomme glisse, "
        "la peau résiste.\n"
        "- Résolution : il refuse de foncer, observe, écoute la "
        "maison, retrouve l'éclat, choisit une pomme.\n"
        "- Retour : livre ouvert, pomme coupée, éclat sur le tissu. "
        "La fin a failli (pomme qui glisse, peau coincée).\n\n"
        "## Vécu\n\n"
        "Raphaël veut entrer **maintenant**. Impatience, puis porte "
        "fermée, sourire parti. Il dit je suis déçu. Papa se baisse, "
        "pose une question, ne récite pas la leçon. Ils agissent : "
        "lire à la maison, puis corbeille vide, il s'arrête. Merci "
        "vécu. Fin : l'éclat du début tient sur le tissu du store.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Raphaël et la porte fermée (noyau dump). Relance : "
        "Que dit Raphaël ? expected déçu.\n"
        "- Lieu du dump-meta (rue de la bibliothèque puis maison). "
        "Maman et papa. Raphaël = héros enfant-m. Dump porte / "
        "fraises / pomme / livre gardés comme objets, pas comme indice.\n"
        "- Ouverture inventée (barre de fer, store baissé, sac), pas "
        "un gabarit v2, pas flaque/vitre/poignée du merged, pas "
        "« Ugo veut aller à la bibliothèque ».\n"
        "- Indice unique : éclat de store ×4. BAN éclat de vitre / "
        "volet / sonnette / clé / livre / cagette / kiosque / pelle / "
        "ficelle. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « j'ai dit : je suis ». Strip merle/miel. "
        "Strip bibliothécaire qui parle.\n"
        "- Leçon non dite : on la voit quand la porte est fermée, "
        "quand il dit je suis déçu, quand il propose le livre, "
        "quand il choisit la pomme. Pas « tu as nommé ». Une seule "
        "« je suis déçu ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « La bibliothèque est fermée. Que dit "
        "Raphaël ? ». expected/accepted dump. retry Ugo → Raphaël. "
        "Hors Q : null. 5 chunks, kinds inchangés.\n"
        "- example4 072 / 004 / 036 (manière volée, gabarit non "
        "collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N3.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, "
        "sous-texte, tempo, sourire, respiration). `slow` = "
        "question et fin. Action un peu plus vive vers la pomme "
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
