#!/usr/bin/env python3
"""ATOM-EMO.LEX.003-07 — Le train de Sarah (F-NAR-019, N2, EMO.LEX.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.003-07"
TITLE = "Le train de Sarah"
N2 = LIMITS["N2"]
CHARS = "Sarah, papa, maman"
SETTING = (
    "maison, après-midi de vent, salon, jardin, balançoire, "
    "porte, vitre, rail, train, wagon, gare du salon"
)
INDICE = "éclat de rail"
FIL = (
    "La vitre du salon vibre sous le vent. Sur le bois, "
    "un éclat de rail luit. Sarah veut la balançoire, "
    "maintenant. Le vent est trop fort. Sourire parti. "
    "Poitrine trop pleine. Papa s'accroupit. Je suis déçue. "
    "Merci vécu. Un train en bois, alors. Deuxième ruse : "
    "le wagon rouge manque. Elle refuse de foncer. Elle "
    "prend le bleu. Un éclat de rail tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(merle|miel|treille|moule|tuteur|saladier|gomme|berge|"
    r"brouette|couverture|capuche|paillasson|fauteuil|coffre|"
    r"haie|housse|cagette|kiosque|pelle|ficelle|store|napperon|"
    r"cube|chaussette|gaëtane|gaetane|maîtresse|maitresse|"
    r"grand-père|grand-pere|jardinier|bibliothécaire|bibliothecaire|"
    r"gardienne)\b",
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
    "c'est de la déception",
    "c est de la deception",
    "c'est de la deception",
    "c'est de la joie",
    "c est de la joie",
    "on peut chercher une autre idée",
    "on peut chercher une autre idee",
    "c'est une autre idée",
    "c est une autre idee",
    "une autre idée peut venir",
    "une autre idee peut venir",
    "un souhait peut attendre",
    "ce n'est pas honteux",
    "ce n est pas honteux",
    "être déçu",
    "etre decu",
    "être déçue",
    "etre decue",
    "tu as trouvé une autre idée",
    "tu as trouve une autre idee",
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
    "tu as dit : je suis",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de wagon",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de bois",
    "éclat de cube",
    "éclat de tour",
    "éclat de coffre",
    "éclat de store",
    "éclat de napperon",
    "éclat de cagette",
    "éclat de kiosque",
    "éclat de pelle",
    "éclat de ficelle",
    "éclat de train",
    "éclat de vitre",
    "éclat de porte",
    "éclat de volet",
    "toute calme",
    "tout calme",
    "gaëtane",
    "gaetane",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de rail",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis déception; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_balancoire_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Sarah",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_vent_est_trop_fort_que_dit_sarah; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="train",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis soulagement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_prend_le_train_sans_slogan; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de rail",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=wagon_rouge_manque_elle_refuse_de_foncer_prend_le_bleu; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de rail",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_soulagement; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "déçue",
    "accepted_examples": (
        "déçue | je suis déçue | autre idée | le wagon bleu | une autre idée"
    ),
    "retry_prompt": "Sarah cherche une autre idée. Que dit-elle d'abord ?",
    "engine_ok_text": "Oui, déçue.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "vent",
        [
            "narrateur|La vitre du salon vibre sous le vent.",
            "enfant-f|Elle tremble, papa.",
            "papa|Tu l'entends, la vitre ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah connaît cette maison, ses bruits d'après-midi.",
            "maman|Tu la connais, cette pièce ?",
            "enfant-f|Oui, maman.",
            "narrateur|Un rail de bois attend près de la porte.",
            "enfant-f|Il est nouveau.",
            "papa|Tu le vois, le rail ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sur le bois, un éclat de rail luit.",
            "enfant-f|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-f|Oui, un point clair.",
            "papa|Le vent le touche.",
            "narrateur|Le volet tape une fois contre le mur.",
            "enfant-f|Il tape fort.",
            "maman|Tu l'entends, le volet ?",
            "enfant-f|Oui, maman.",
            "narrateur|La porte laisse passer un souffle froid.",
            "enfant-f|Ça sent le dehors.",
            "papa|Tu le sens, le vent ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah pose la main sur la poignée.",
            "enfant-f|Elle est froide.",
            "maman|Tes doigts sont froids, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Par la porte, le jardin bouge.",
            "enfant-f|Les branches bougent.",
            "papa|Tu vois le jardin ?",
            "enfant-f|Oui, papa.",
            "narrateur|En ce moment, Sarah veut le jardin.",
            "enfant-f|La balançoire, maintenant !",
            "papa|Tout de suite ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah pousse la porte trop vite.",
            "narrateur|Le vent entre d'un coup.",
            "enfant-f|Il pousse !",
            "maman|On regarde par la porte ?",
            "enfant-f|Oui, maman.",
            "narrateur|La balançoire va toute seule, dans le jardin.",
            "enfant-f|Elle part sans moi.",
            "papa|Les chaînes tintent, Sarah ?",
            "enfant-f|Oui, fort.",
            "narrateur|Le vent est trop fort, près des chaînes.",
            "enfant-f|Je veux y aller.",
            "narrateur|Sarah avance un pied dehors, trop vite.",
            "narrateur|Le vent lui rentre dans les cheveux.",
            "enfant-f|Ça pique les yeux.",
            "maman|Tu recules, Sarah ?",
            "enfant-f|Un peu.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "enfant-f|J'ai mal au ventre.",
            "papa|Ta gorge est serrée, Sarah ?",
            "enfant-f|Un peu, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "maman|Tes mains sont chaudes, Sarah ?",
            "enfant-f|Un peu, maman.",
            "enfant-f|Je suis déçue.",
            "narrateur|L'éclat de rail tremble, puis tient.",
            "papa|Tu vois le jardin, Sarah ?",
            "enfant-f|Oui.",
            "narrateur|Sarah serre les poings, puis les ouvre.",
            "papa|Tes poings, Sarah ?",
            "enfant-f|Ils se desserrent.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Le vent est trop fort.",
            "narrateur|Que dit Sarah ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Sarah avance un pied vers le jardin, trop vite.",
            "enfant-f|J'y vais, maintenant !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|La balançoire.",
            "narrateur|Sarah avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le rail, un instant.",
            "narrateur|Elle écoute la maison, près de la porte.",
            "enfant-f|Un train en bois, alors.",
            "papa|Tu le vois, le train ?",
            "enfant-f|Oui, papa.",
            "papa|Merci, Sarah.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le bois du rail est froid, sous les doigts.",
            "enfant-f|Il est lisse.",
            "narrateur|Ils posent les rails, sans se presser.",
            "enfant-f|Ça fait clic.",
            "papa|Tu entends le clic, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|Le train tient, Sarah ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le ventre de Sarah se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "enfant-f|Jusqu'à la gare du salon.",
            "papa|On y va, sans se presser ?",
            "enfant-f|Oui.",
            "narrateur|Sarah pose une locomotive, très petite.",
            "enfant-f|Elle attend.",
            "maman|Tes joues sont chaudes, Sarah ?",
            "enfant-f|Un peu, maman.",
            "papa|Le premier wagon, plus tard.",
            "enfant-f|Oui, papa.",
            "narrateur|Le vent tape plus loin, plus faible.",
            "enfant-f|Il est dehors.",
            "maman|On reste près des rails ?",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Sarah cherche dans la boîte, trop vite.",
            "enfant-f|Le wagon rouge, maintenant !",
            "narrateur|Sa main trouve du vide.",
            "enfant-f|Il n'y en a plus.",
            "maman|Le wagon rouge ?",
            "enfant-f|Parti.",
            "narrateur|Les épaules de Sarah retombent.",
            "enfant-f|Je le prends, tout de suite !",
            "narrateur|Sarah avance trop vite vers la boîte.",
            "narrateur|La boîte bascule au bord.",
            "enfant-f|Elle part !",
            "narrateur|Sarah avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Sarah refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le rail, un instant.",
            "narrateur|Elle écoute la maison, près du train.",
            "narrateur|Sur le bois, un éclat de rail luit.",
            "enfant-f|Là, sur le bois.",
            "papa|Tu vois le point, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un wagon bleu attend au fond de la boîte.",
            "enfant-f|Le bleu, alors.",
            "maman|Tu le vois, le wagon ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sarah prend le wagon bleu, sans se presser.",
            "narrateur|Elle le pose sur le rail.",
            "enfant-f|Il glisse !",
            "papa|Tu le tiens, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le wagon penche, presque tombé.",
            "enfant-f|Il reste.",
            "maman|Il tient, Sarah ?",
            "enfant-f|Oui, maman.",
            "narrateur|Ils poussent le train, ensemble.",
            "papa|Le train est prêt, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le wagon bleu avance, un peu de travers.",
            "enfant-f|Ça tient.",
            "maman|La gare du salon est proche, Sarah ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le bleu s'arrête juste avant de tomber.",
            "enfant-f|Il a failli partir.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près des rails.",
            "narrateur|Maman essuie un peu de poussière.",
            "enfant-f|Le rouge n'était pas là, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-f|Oui, la boîte vide.",
            "maman|On est bien, ici.",
            "narrateur|Sarah tapote le wagon bleu du doigt.",
            "enfant-f|Il a une petite trace.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|Le bleu est resté, Sarah.",
            "enfant-f|Oui, avec le train.",
            "narrateur|Ça sent le bois, un peu tiède.",
            "enfant-f|Et le vent, maman.",
            "maman|Oui, dans l'air.",
            "papa|La maison est calme, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le wagon bleu reste sur le rail.",
            "narrateur|Un éclat de rail tient sur le bois.",
        ],
    ),
}


def vet(lines: list[str], cid: str = "") -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    skip_lesson = cid == "CHK_T0000_P0000_Q0001"
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
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        if not skip_lesson:
            for bad in EXTRA_BAD:
                if bad in low:
                    raise SystemExit(f"extra {bad}: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-f"):
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
        if cid != "CHK_T0000_P0000_Q0001":
            for key in (
                "expected_answer",
                "accepted_examples",
                "retry_prompt",
                "engine_ok_text",
                "engine_near_text",
            ):
                by[cid][key] = None
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
    if "accroupit" not in blob:
        raise SystemExit(f"{SID}: manque accroupit")
    if "poitrine" not in blob:
        raise SystemExit(f"{SID}: manque poitrine")
    if "sourire" not in blob:
        raise SystemExit(f"{SID}: manque sourire")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Sarah = enfant-f)")
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
    if any(r not in ("narrateur", "papa", "maman", "enfant-f") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "enfant-f" for r in roles):
        raise SystemExit(f"{SID}: enfant-f absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on peut chercher une autre idée",
        "c'est de la déception",
        "c est de la deception",
        "c'est une autre idée",
        "j'ai dit",
        "j ai dit",
        "tu as nommé",
        "tu as nomme",
        "l'histoire est finie",
        "un souhait peut attendre",
        "ce n'est pas honteux",
        "être déçu",
        "etre decu",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Le vent est trop fort. Que dit Sarah ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "déçue":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "déçue | je suis déçue | autre idée | le wagon bleu | une autre idée"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Sarah cherche une autre idée. Que dit-elle d'abord ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    if "gaëtane" in retry.lower() or "gaetane" in retry.lower():
        raise SystemExit(f"{SID}: retry encore Gaëtane")
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
    if "je suis déçue" not in opening:
        raise SystemExit(f"{SID}: nommage absent avant la question")
    n_decue = blob.count("je suis déçue")
    if n_decue != 1:
        raise SystemExit(f"{SID}: je suis déçue ×{n_decue}")
    if "train" not in by["CHK_T0000_P0000_C0001"]["text"].lower():
        raise SystemExit(f"{SID}: train absent après la question")
    if "balançoire" not in blob and "balancoire" not in blob:
        raise SystemExit(f"{SID}: manque balançoire")
    if "train" not in blob:
        raise SystemExit(f"{SID}: manque train")
    if "wagon" not in blob:
        raise SystemExit(f"{SID}: manque wagon")
    if "vent" not in blob:
        raise SystemExit(f"{SID}: manque vent")
    if "maintenant" not in blob:
        raise SystemExit(f"{SID}: manque maintenant")
    if "s'accroupit" not in opening and "s accroupit" not in opening:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    if "sourire" not in opening or "disparaît" not in opening:
        raise SystemExit(f"{SID}: manque sourire disparu")
    if "poitrine" not in opening:
        raise SystemExit(f"{SID}: manque poitrine")
    end_txt = by["CHK_T0000_P0000_END"]["text"].lower()
    if "wagon rouge" not in end_txt:
        raise SystemExit(f"{SID}: manque 2e ruse (wagon rouge)")
    if "wagon bleu" not in end_txt:
        raise SystemExit(f"{SID}: manque 2e ruse (wagon bleu)")
    if INDICE not in end_txt:
        raise SystemExit(f"{SID}: indice non payé au climax")
    if "papa" not in by["CHK_T0000_P0000_END"]["script"].lower():
        raise SystemExit(f"{SID}: papa absent au 2e imprévu")
    if "triste" in blob:
        raise SystemExit(f"{SID}: tristesse LEX.002-05 collée")
    for ban in (
        "éclat de wagon",
        "éclat de balançoire",
        "éclat de bois",
        "éclat de cube",
        "éclat de tour",
        "éclat de coffre",
        "éclat de store",
        "éclat de napperon",
        "éclat de cagette",
        "éclat de kiosque",
        "éclat de pelle",
        "éclat de ficelle",
        "éclat de train",
        "tout doux",
        "tout calme",
        "toute calme",
        "merle",
        "miel",
        "gaëtane",
        "gaetane",
        "chaussette",
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
    notes_ok = all(
        all(
            k in (c.get("notes") or "")
            for k in (
                "arc=",
                "intention=",
                "emotion=",
                "intensite=",
                "destinataire=",
                "sous_texte=",
                "tempo=",
                "sourire=",
                "respiration=",
            )
        )
        for c in chunks
    )
    if not notes_ok:
        raise SystemExit(f"{SID}: notes incomplètes")

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
        "- **Public :** N2 (≤15 mots/phrase), audio familial, voc 4–5 ans\n"
        "- **Leçon :** EMO.LEX.003 — nommer la déception + chercher une "
        "autre idée (vécue : Sarah veut la balançoire **maintenant**, vent "
        "trop fort, sourire parti, poitrine qui se bouscule, papa accroupi ; "
        "« Je suis déçue » ; train en bois ; 2e ruse : wagon rouge manque, "
        "elle refuse de foncer, prend le bleu). JAMAIS dite dans le récit. "
        "Pas « on peut chercher une autre idée ». Pas « c'est de la "
        "déception ». Pas « j'ai dit : je suis ». Distinct de LEX.002-05 "
        "(train perdu, tristesse).\n"
        "- **Personnages :** Sarah, papa, maman. Dump papa seulement → "
        "ajoute maman. D16 Sarah = enfant-f (veut la balançoire maintenant). "
        "Pas de copain (dump sans camarade). Troupe D16. Pas de maîtresse. "
        "Dump Gaëtane → Sarah.\n"
        "- **Lieu :** maison, après-midi de vent, salon, jardin, "
        "balançoire, porte, vitre, rail, train, wagon. Coin nommé : "
        "gare du salon. Vent / balançoire / train / wagon = dump.\n"
        "- **Indice unique :** éclat de rail (luit à l'ouverture → "
        "tremble à la déception → luit au climax wagon manquant → tient "
        "sur le bois). BAN éclat de wagon / balançoire / bois / cube / "
        "tour / coffre / store / napperon / cagette / kiosque / pelle / "
        "ficelle.\n"
        "- **Question moteur :** « Le vent est trop fort. Que dit "
        "Sarah ? » expected dump **déçue**. accepted dump "
        "`déçue | je suis déçue | autre idée | le wagon bleu | une autre "
        "idée`. retry dump Gaëtane → Sarah : `Sarah cherche une autre "
        "idée. Que dit-elle d'abord ?`. Hors Q : null. Non récitée "
        "ailleurs.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / "
        "graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin "
        "heureuse. `chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La vitre du salon vibre sous le vent. Sarah connaît la maison ; "
        "un rail de bois paraît nouveau près de la porte. Sur le bois, "
        "un éclat de rail luit. Sarah veut la balançoire **maintenant**. "
        "Le vent est trop fort. Sourire parti. Envie et inquiétude. "
        "Papa s'accroupit. Je suis déçue. Merci vécu. Un train en bois, "
        "alors. Deuxième ruse : le wagon rouge manque, la boîte bascule. "
        "Elle s'arrête, lit l'éclat, prend le bleu. Le bleu penche, "
        "presque tombé. Un éclat de rail tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : maison, après-midi de vent, vitre, volet, porte, "
        "jardin, rail près de la porte, gare du salon.\n"
        "- Désir : la balançoire du jardin, maintenant.\n"
        "- Objet : balançoire impossible, train en bois, wagon rouge "
        "manquant, wagon bleu à la trace.\n"
        "- Indice unique : éclat de rail, vu dès l'ouverture, payé au "
        "climax sur le bois. Pas éclat de wagon / balançoire / bois / "
        "cube / tour / coffre.\n"
        "- Urgence douce : elle pousse la porte trop vite, un pied "
        "dehors.\n"
        "- Imprévu 1 : vent trop fort, balançoire seule, sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après qu'elle "
        "refuse de foncer et prend le train.\n"
        "- Imprévu 2 (plus rusé) : wagon rouge manque, boîte qui "
        "bascule, bleu qui penche.\n"
        "- Résolution : elle refuse de foncer, observe, écoute la "
        "maison, retrouve l'éclat, prend le bleu.\n"
        "- Retour : wagon bleu sur le rail, petite trace, éclat sur le "
        "bois. Dénouement qui a failli : le bleu glisse, presque tombé.\n\n"
        "## Vécu\n\n"
        "Sarah veut la balançoire **maintenant**. Impatience, puis vent "
        "trop fort, sourire parti, poitrine qui se bouscule. Elle dit "
        "je suis déçue. Elle s'arrête, regarde le rail, dit un train. "
        "Papa se baisse, pose une question, ne récite pas la leçon. "
        "Merci vécu. Fin : l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le train de Sarah (noyau dump). Relance : Que dit "
        "Sarah ? expected déçue.\n"
        "- Lieu du dump-meta (maison, après-midi de vent). Maman ajoutée "
        "(dump papa seulement). Sarah = héros enfant-f. Vent / "
        "balançoire / train / wagon conservés.\n"
        "- Ouverture inventée (vitre qui vibre, rail nouveau près de "
        "la porte), pas un gabarit v2, pas chaussette rouge du dump, "
        "pas « Gaëtane veut la balançoire ».\n"
        "- Indice unique : éclat de rail ×4. BAN éclat de wagon / "
        "balançoire / bois / cube / tour / coffre / store / napperon / "
        "cagette / kiosque / pelle / ficelle. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « j'ai dit : je suis ». Strip « un souhait "
        "peut attendre ». Strip « être déçue n'est pas honteux ».\n"
        "- Leçon non dite : on la voit quand le vent est trop fort, "
        "quand elle dit je suis déçue, quand elle prend le train, "
        "quand elle prend le bleu. Pas « tu as nommé ». Une seule "
        "« je suis déçue ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Le vent est trop fort. Que dit "
        "Sarah ? ». expected/accepted dump. retry Gaëtane → Sarah. "
        "Hors Q : null. 5 chunks, kinds inchangés.\n"
        "- example4 074 / 006 / 038 (manière volée, gabarit non "
        "collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N2.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, "
        "sous-texte, tempo, sourire, respiration). `slow` = "
        "question et fin. Action un peu plus vive vers la boîte.\n"
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
