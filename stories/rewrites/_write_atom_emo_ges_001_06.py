#!/usr/bin/env python3
"""ATOM-EMO.GES.001-06 — Amir dit stop (F-NAR-019, N1, EMO.GES.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.001-06"
TITLE = "Amir dit stop"
N1 = LIMITS["N1"]
CHARS = "Amir, Nina, papa, maman"
SETTING = (
    "salon, table, lampe, fenêtre, cadre, "
    "coussin, sol, orange, mur, bol"
)
INDICE = "éclat de cadre"
FIL = (
    "Ça sent l'orange près de la table. Sur le mur, un "
    "éclat de cadre luit. Amir veut jouer, maintenant. "
    "Nina met le coussin trop près. Sourire parti. Papa "
    "s'accroupit. Stop, un pas. Merci vécu. Deuxième ruse : "
    "le coussin glisse. Un éclat de cadre tient sur le mur."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(plateau|étal|etal|carotte|pupitre|canapé|canape|"
    r"merle|miel|maîtresse|maitresse|pépin|pepin|"
    r"bateau|cerceau|piquet|gond|flaque|grille|"
    r"plaid|rideau|livre|balançoire|balancoire|toboggan|"
    r"tapis|cabane|radiateur|volet|volets|horloge|"
    r"pain|nappe|assiette|évier|evier|frigo)\b",
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
    "on peut attendre",
    "on peut jouer",
    "vous jouez",
    "on joue",
    "dire stop",
    "dit stop",
    "tu as dit",
    "j'ai dit",
    "on s'éloigne",
    "s'éloigner",
    "s'eloigner",
    "on va vers un adulte",
    "vers un adulte",
    "c'est permis",
    "c est permis",
    "tu t'es éloigné",
    "tu t'es eloigne",
    "tu te recules",
    "il faut dire",
    "on recule",
    "puis on s'éloigne",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de plateau",
    "éclat d'étal",
    "éclat d'etal",
    "éclat de carotte",
    "éclat de pupitre",
    "éclat de canapé",
    "éclat de canape",
    "éclat de pomme",
    "éclat de nappe",
    "éclat de bol",
    "éclat de verre",
    "éclat d'évier",
    "éclat d'evier",
    "éclat de quartier",
    "éclat de jus",
    "éclat de pierre",
    "éclat de cerceau",
    "éclat de flaque",
    "éclat de grille",
    "éclat de cour",
    "éclat de botte",
    "éclat de piquet",
    "éclat de gond",
    "éclat de table",
    "éclat de parquet",
    "éclat de zinc",
    "éclat de rambarde",
    "éclat de coussin",
    "éclat de tapis",
    "éclat de plaid",
    "éclat de rideau",
    "éclat de livre",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de toboggan",
    "éclat d'assiette",
    "éclat d'assiette",
    "grain de pomme",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

# N1 : mêmes champs que 002-05 / 001-09 (voix lente).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat de cadre",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis gêne; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_jouer_maintenant; "
            "tempo=posé puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=104, speed=0.80, piper=1.36, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=780,
        sentence=360, energy="focused", contour="rising", noise=0.30,
        emphasis="trop",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=c_est_trop_pour_amir_que_fait_il; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=122, speed=0.88, piper=1.24, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=620,
        sentence=310, energy="bright", contour="falling", noise=0.33,
        emphasis="Stop",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis soulagement; intensite=2; "
            "destinataire=enfant; sous_texte=il_dit_stop_il_recule_d_un_pas; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de cadre",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=le_coussin_glisse_il_dit_stop_encore; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de cadre",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_mur; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": None,
    "accepted_examples": None,
    "retry_prompt": None,
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "",
        [
            "narrateur|Ça sent l'orange, près de la table.",
            "enfant-m|Ça sent bon, papa.",
            "papa|Tu le sens, le fruit ouvert ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le jus brille un peu.",
            "maman|J'ai ouvert l'orange.",
            "enfant-m|Elle brille, maman.",
            "narrateur|Maman pose le bol rond.",
            "narrateur|Le bol est froid, un peu lisse.",
            "enfant-m|Il est froid.",
            "papa|Tu le touches, Amir ?",
            "enfant-m|Oui, du doigt.",
            "narrateur|Sur le mur, un éclat de cadre luit.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, sur le verre ?",
            "enfant-m|Oui, un petit point.",
            "papa|Le soleil le touche.",
            "narrateur|Un rayon glisse sur le bois.",
            "narrateur|Le bois de la table gratte un peu.",
            "enfant-m|Il gratte, papa.",
            "maman|Tu t'assois, Amir ?",
            "enfant-m|Un peu.",
            "narrateur|Une peau d'orange dort sur le bois.",
            "enfant-m|Une peau, maman.",
            "maman|Elle est sèche ?",
            "enfant-m|Oui.",
            "narrateur|La lampe chauffe le mur, tout près.",
            "enfant-m|Elle chauffe, papa.",
            "papa|Tu la sens, la lampe ?",
            "enfant-m|Oui, elle chauffe.",
            "narrateur|Une goutte tombe dans le bol.",
            "enfant-m|Ploc.",
            "maman|C'est une goutte.",
            "narrateur|Les pieds d'Amir touchent le sol.",
            "enfant-m|Mes pieds, papa.",
            "papa|Tu es bien assis, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le sol est lisse, un peu froid.",
            "enfant-m|Il est lisse.",
            "narrateur|Nina arrive près de la table.",
            "narrateur|Ses pieds glissent sur le bois.",
            "copine|Le coussin.",
            "enfant-m|Tu viens, Nina ?",
            "copine|Oui.",
            "narrateur|Maman pose le gros coussin.",
            "narrateur|Il est mou, un peu lourd.",
            "enfant-m|Je veux jouer, maintenant !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|En ce moment, Amir tend le coussin.",
            "maman|Tu le donnes à Nina ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nina prend le coussin.",
            "narrateur|Elle le met trop près.",
            "copine|Près.",
            "narrateur|Le coussin appuie sur Amir.",
            "enfant-m|Oh.",
            "narrateur|Nina pousse plus fort.",
            "copine|Joue.",
            "narrateur|Amir baisse les yeux.",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dans sa poitrine, ça se serre.",
            "narrateur|L'envie et l'inquiétude se heurtent.",
            "narrateur|Ses épaules montent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu es serré, Amir ?",
            "enfant-m|Un peu, papa.",
            "maman|Tes mains sont froides, Amir ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de cadre tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|C'est trop pour Amir.",
            "narrateur|Que fait-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Amir veut jouer, tout de suite.",
            "enfant-m|Je joue, maintenant !",
            "narrateur|Il avance trop vite vers Nina.",
            "narrateur|Le coussin reste collé à sa poitrine.",
            "copine|Viens.",
            "narrateur|Nina pousse le coussin.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "enfant-m|C'est trop.",
            "enfant-m|Stop.",
            "narrateur|Amir recule d'un pas.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le coussin, un instant.",
            "narrateur|Il écoute le bruit de la lampe.",
            "papa|Tu veux de l'air, Amir ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Plus loin.",
            "narrateur|Nina ne dit rien, d'abord.",
            "narrateur|Elle tire le coussin vers elle.",
            "copine|Loin.",
            "enfant-m|Loin, oui.",
            "papa|Merci, Amir.",
            "narrateur|Papa a vu les deux, près du bol.",
            "maman|Le coussin colle un peu, sous les doigts.",
            "enfant-m|Il est mou.",
            "narrateur|Nina pose le coussin au sol.",
            "narrateur|Amir souffle par le nez.",
            "copine|Doux.",
            "enfant-m|Doux, oui.",
            "papa|Tu le vois, le coussin ?",
            "enfant-m|Oui, papa.",
            "maman|Tu restes ici, Amir ?",
            "enfant-m|Oui.",
            "narrateur|Ils restent près de la table.",
            "narrateur|Ça sent l'orange, un peu tiède.",
            "enfant-m|Elle est là.",
            "copine|Elle est là.",
            "papa|Le bois est calme ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le ventre d'Amir se desserre.",
            "narrateur|Les épaules descendent un peu.",
            "papa|On reste près de la table ?",
            "enfant-m|Oui.",
            "maman|Tes mains sont au frais ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Maman pose le petit bol.",
            "narrateur|Le bol est un peu flou.",
            "enfant-m|Je joue, maintenant !",
            "narrateur|Nina lève le coussin.",
            "copine|Hop.",
            "narrateur|Le coussin glisse trop près.",
            "enfant-m|Il glisse, maintenant !",
            "narrateur|Amir avance le ventre, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Amir refuse de rester collé.",
            "enfant-m|Stop.",
            "narrateur|Amir recule d'un pas.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe la table, un instant.",
            "narrateur|Il écoute le bruit de la lampe.",
            "narrateur|Sur le mur, un éclat de cadre luit.",
            "enfant-m|Là, sur le verre.",
            "enfant-m|Plus loin, Nina ?",
            "narrateur|Nina ne dit rien.",
            "narrateur|Elle souffle, puis tire.",
            "copine|Il glisse.",
            "papa|On pose le coussin ?",
            "enfant-m|Oui, papa.",
            "narrateur|Amir pousse le coussin.",
            "narrateur|Nina le pose, sans se presser.",
            "enfant-m|Il tient.",
            "copine|Il tient.",
            "papa|Le jus est froid, Nina ?",
            "copine|Un peu.",
            "maman|Tu bois, Amir ?",
            "enfant-m|Oui, maman.",
            "narrateur|Ils boivent près de la table.",
            "narrateur|Le bois chatouille les poignets.",
            "enfant-m|C'est plus facile.",
            "papa|La lampe est calme ?",
            "enfant-m|Oui, papa.",
            "maman|Un rayon passe sur le mur.",
            "enfant-m|Il allume le cadre.",
            "narrateur|Nina souffle sur le bol.",
            "copine|Le jus.",
            "enfant-m|Le jus, oui.",
            "narrateur|Le bol laisse un rond.",
            "enfant-m|Un rond d'eau.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la table.",
            "narrateur|Maman essuie un peu de jus.",
            "enfant-m|Le coussin est loin, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, près du sol.",
            "maman|On est bien, ici.",
            "narrateur|Amir tapote le bois du doigt.",
            "enfant-m|Il a une trace d'eau.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|Le coussin est resté, Amir.",
            "enfant-m|Oui, avec Nina.",
            "copine|Le coussin est resté.",
            "narrateur|Ça sent l'orange, un peu tiède.",
            "enfant-m|Et le jus, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|L'orange reste dans le bol.",
            "narrateur|Un éclat de cadre tient sur le mur.",
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
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        if not skip_lesson:
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
    if "stop." not in blob:
        raise SystemExit(f"{SID}: manque Stop vécu")
    if "recule d'un pas" not in blob and "recule d’un pas" not in blob:
        raise SystemExit(f"{SID}: manque un pas")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Amir = enfant-m, Nina = copine)")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Nina absente (copine)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m", "copine") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "copine" for r in roles):
        raise SystemExit(f"{SID}: copine absente")
    if not any(r == "enfant-m" for r in roles):
        raise SystemExit(f"{SID}: enfant-m absent")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "dire stop",
        "dit stop",
        "tu as dit stop",
        "j'ai dit stop",
        "on s'éloigne",
        "s'éloigner",
        "on va vers un adulte",
        "vers un adulte",
        "c'est permis",
        "stop, puis",
        "puis on s'éloigne",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "C'est trop pour Amir. Que fait-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") is not None:
        raise SystemExit(f"{SID}: expected_answer doit rester null")
    if q.get("accepted_examples") is not None:
        raise SystemExit(f"{SID}: accepted_examples doit rester null")
    if q.get("retry_prompt") is not None:
        raise SystemExit(f"{SID}: retry_prompt doit rester null")
    if "c'est trop pour amir" in body:
        raise SystemExit(f"{SID}: question récitée hors Q")
    if "coussin" not in blob:
        raise SystemExit(f"{SID}: manque coussin")
    if "salon" not in blob and "table" not in blob:
        raise SystemExit(f"{SID}: manque salon/table")
    for ban in (
        "éclat de coussin",
        "éclat de canapé",
        "éclat de tapis",
        "éclat de plaid",
        "éclat de rideau",
        "éclat de livre",
        "éclat de balançoire",
        "éclat de toboggan",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "canapé",
        "tapis",
        "plaid",
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
        "- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans\n"
        "- **Leçon :** EMO.GES.001 — trop près → stop, reculer "
        "(vécue : Nina met le coussin trop près, poitrine, sourire parti, "
        "Amir dit Stop, recule d'un pas ; 2e ruse : le coussin glisse, "
        "il dit Stop, un pas). JAMAIS dite. Pas « dire stop ». Pas "
        "« on s'éloigne ». Pas « on va vers un adulte ».\n"
        "- **Personnages :** Amir, Nina, papa, maman. Dump François/Nina/"
        "maman → D16 Amir = enfant-m (veut jouer maintenant). Nina = copine "
        "(coussin trop près, Près, Joue, Hop, souffle). Troupe D16. Pas de "
        "maîtresse.\n"
        "- **Lieu :** salon, table, lampe, fenêtre, cadre, coussin, sol, "
        "orange, mur, bol. ≠ 001-04 plaid/cabane. ≠ 001-05 radiateur/"
        "chaussettes. ≠ 001-01 balançoire. ≠ 001-02 rideau. ≠ 001-03 "
        "toboggan.\n"
        "- **Indice unique :** éclat de cadre (luit à l'ouverture → "
        "tremble au coussin trop près → luit quand le coussin glisse → "
        "tient sur le mur). BAN éclat de coussin / canapé / tapis / "
        "plaid / rideau / livre / balançoire / toboggan.\n"
        "- **Question moteur :** « C'est trop pour Amir. Que fait-il ? » "
        "expected / accepted / retry **null** (consigne). Non récitée "
        "dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Ça sent l'orange près de la table. Sur le mur, un éclat "
        "de cadre luit. Goutte, lampe, sol. Amir veut jouer "
        "**maintenant**. Nina met le coussin trop près. Sourire parti. "
        "Papa s'accroupit. Stop, un pas. Merci vécu. Deuxième ruse : "
        "le coussin glisse. Il dit Stop, recule, lit l'éclat. Un "
        "éclat de cadre tient sur le mur.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon, table, lampe, fenêtre, cadre, coussin, sol, "
        "orange. ≠ 001-04 plaid. ≠ 001-05 radiateur. ≠ dump volets/"
        "pain grillé/canapé.\n"
        "- Désir : jouer, maintenant.\n"
        "- Objet : gros coussin, puis le coussin qui glisse.\n"
        "- Indice unique : éclat de cadre, vu dès l'ouverture, payé "
        "sur le mur. Pas éclat de coussin / canapé / tapis / plaid / "
        "rideau / livre / balançoire / toboggan.\n"
        "- Urgence douce : le jeu est là, tout prêt, trop près.\n"
        "- Imprévu 1 : Nina met le coussin trop près, poitrine, "
        "sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "Stop et le pas.\n"
        "- Imprévu 2 (plus rusé) : bol, le coussin glisse, Amir "
        "avance le ventre.\n"
        "- Résolution : Stop, un pas, observe, écoute la lampe, "
        "retrouve l'éclat, Nina tire.\n"
        "- Retour : rond d'eau, orange dans le bol, éclat sur le "
        "mur.\n\n"
        "## Vécu\n\n"
        "Amir veut jouer **maintenant**. Impatience, puis coussin "
        "trop près, sourire parti. Nina pousse, pose sa ruse "
        "(Près, Joue, Hop). Papa se baisse, pose une question, ne "
        "récite pas la règle. Ils agissent : Stop, un pas, coussin "
        "tiré, coussin posé. Merci vécu. Fin : l'éclat du début "
        "tient sur le mur.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Amir dit stop (noyau « dit stop », prénom D16). "
        "Relance : Que fait-il ? expected null.\n"
        "- Lieu du dump (salon, coussin). Maman et papa. Nina = "
        "copine. Amir = héros. Dump François/Nina/maman remappé : "
        "François→Amir, Nina reste Nina.\n"
        "- Ouverture inventée (odeur d'orange près de la table), pas "
        "un gabarit v2, pas « Les volets font des rayures » du dump.\n"
        "- Indice unique : éclat de cadre (salon). BAN éclat de "
        "coussin / canapé / tapis (BAN ou pris) / plaid (001-04) / "
        "rideau (001-02) / livre (001-05) / balançoire (001-01) / "
        "toboggan (001-03). Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « encore » du dump.\n"
        "- Leçon non dite : on la voit quand Amir dit Stop, quand "
        "il recule d'un pas, quand le coussin glisse. Pas « dire "
        "stop ». Pas « on s'éloigne ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « C'est trop pour Amir. Que fait-il ? ». "
        "expected/accepted/retry null. 5 chunks, kinds inchangés.\n"
        "- example4 043 / 075 / 007 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_par_002_05.py`, profiles N1 lents.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers le coussin qui glisse.\n"
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
