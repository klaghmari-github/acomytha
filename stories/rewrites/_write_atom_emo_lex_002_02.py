#!/usr/bin/env python3
"""ATOM-EMO.LEX.002-02 — Nino et le bateau de papier (F-NAR-019, N2, EMO.LEX.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.002-02"
TITLE = "Nino et le bateau de papier"
N2 = LIMITS["N2"]
CHARS = "Nino, papa, maman"
SETTING = "parc, après la pluie"
INDICE = "éclat de capuche"
FIL = (
    "Une goutte tape la capuche. Sur le tissu, un éclat de capuche luit. "
    "Nino veut le bateau de papier, maintenant. L'eau l'emporte. "
    "Le papier se déchire. Poitrine trop vite. Sourire parti. "
    "Yeux chauds. Je suis triste. Nino pleure. Papa s'accroupit. "
    "Deuxième ruse : le papier se déchire plus loin, le bateau part. "
    "Il refuse de foncer. Je veux un câlin. Merci vécu. "
    "Un éclat de capuche tient sur le tissu."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tapis|rideau|plaid|balançoire|balancoire|plinthe|marelle|"
    r"banc|cour|grille|bac|botte|bottes|limace|perron|"
    r"tiroir|fraisier|cuivre|buis|coussin|figue|robinet|planche|"
    r"émail|email|samare|bassine|entrée|entree|merle|miel|"
    r"piquet|cerceau|drap|savon|bol|feuille|pierre|commode|"
    r"lacet|sauge|chiffon|parquet|gond|portail|canapé|"
    r"canape|oiseau|toboggan|comptoir|treille|moule|tuteur|"
    r"saladier|gomme|berge|brouette|couverture|torchon|"
    r"tabouret|lit|maîtresse|maitresse)\b",
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
    "j'ai dit : je suis",
    "j'ai dit: je suis",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "c'est de la tristesse",
    "c est de la tristesse",
    "c'est de la joie",
    "tu as nommé",
    "tu as nomme",
    "pleurer est permis",
    "le câlin aide",
    "le calin aide",
    "être triste, c'est permis",
    "etre triste, c'est permis",
    "tu es triste",
    "c'est permis",
    "tu as dit",
    "tu as demandé un câlin",
    "tu as demande un calin",
    "bravo, nino",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de flaque",
    "éclat de bateau",
    "éclat de papier",
    "éclat de grille",
    "éclat de banc",
    "éclat de tapis",
    "éclat de treille",
    "éclat de moule",
    "éclat de tuteur",
    "éclat de saladier",
    "éclat de gomme",
    "éclat de berge",
    "éclat de brouette",
    "éclat de couverture",
    "éclat de torchon",
    "éclat de tabouret",
    "éclat de lit",
    "éclat de manteau",
    "éclat de poche",
    "éclat d'allée",
    "éclat d'allee",
    "éclat de herbe",
    "éclat d'herbe",
    "éclat de goutte",
    "éclat de tissu",
    "éclat de tour",
    "éclat de comptoir",
    "éclat de pot",
    "éclat de rouleau",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de capuche",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=élan puis tristesse; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_bateau_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Nino",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=nino_a_les_yeux_chauds_que_dit_il; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="papier",
        note=(
            "arc=confirmation; intention=relancer_sans_leçon; "
            "emotion=retenue puis souffle_plus_large; intensite=1; "
            "destinataire=enfant; sous_texte=il_s_arrete_le_papier_tient; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de capuche",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=papier_se_dechire_bateau_part_il_refuse_de_foncer; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de capuche",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_tissu; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "triste",
    "accepted_examples": "triste | je suis triste | câlin | un câlin | pleurer",
    "retry_prompt": "Nino peut demander un câlin. Que dit-il ?",
    "engine_ok_text": "Oui, triste.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc",
        [
            "narrateur|Une goutte tape la capuche de Nino.",
            "enfant-m|Elle tape, papa.",
            "papa|Tu l'entends, la goutte ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le parc, après la pluie, goutte partout.",
            "maman|Tu le sens, l'air mouillé ?",
            "enfant-m|Oui, maman.",
            "narrateur|Sur le tissu, un éclat de capuche luit.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, sur le tissu ?",
            "enfant-m|Oui, un petit point.",
            "papa|La goutte le touche.",
            "narrateur|L'air sent la terre, un peu mouillée.",
            "enfant-m|Ça sent l'eau.",
            "maman|Tes mains sont froides, Nino ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Nino met les mains dans sa poche.",
            "enfant-m|Il est là.",
            "maman|C'est ton bateau de papier ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le papier est un peu froid.",
            "enfant-m|Il colle aux doigts.",
            "papa|Tu le sors, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le bateau a un pli au milieu.",
            "enfant-m|Deux bouts, comme des ailes.",
            "maman|Il est petit, Nino ?",
            "enfant-m|Oui, tout petit.",
            "narrateur|Une flaque ronde attend près de l'allée.",
            "enfant-m|Elle est ronde !",
            "papa|Tu la vois, la flaque ?",
            "enfant-m|Oui, papa.",
            "narrateur|L'herbe est lourde, près de l'eau.",
            "enfant-m|Elle colle aux chaussures.",
            "maman|Tes chaussures sont mouillées, Nino ?",
            "enfant-m|Un peu, maman.",
            "narrateur|En ce moment, Nino avance vers la flaque.",
            "enfant-m|Je veux le bateau, maintenant !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|Il pose le bateau sur l'eau.",
            "narrateur|L'eau emporte le bateau d'un petit coup.",
            "narrateur|Le papier se ramollit.",
            "narrateur|Le papier se déchire.",
            "enfant-m|Mon bateau !",
            "narrateur|Nino reste surpris, les mains ouvertes.",
            "narrateur|Sa gorge se serre un peu.",
            "narrateur|Sa poitrine va trop vite.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et l'inquiétude se heurtent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Ses yeux deviennent chauds.",
            "narrateur|Une larme tombe.",
            "enfant-m|Je suis triste.",
            "narrateur|Nino pleure un peu.",
            "narrateur|Les larmes sont chaudes, sur ses joues.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois le bateau, Nino ?",
            "enfant-m|Oui, papa.",
            "maman|Tes yeux sont chauds, Nino ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de capuche tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino a les yeux chauds.",
            "narrateur|Que dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "",
        [
            "narrateur|Nino veut le bateau, tout de suite.",
            "enfant-m|Je le prends, maintenant !",
            "narrateur|Le bateau reste un peu loin, dans l'eau.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-m|Trop vite.",
            "narrateur|Nino avance les mains, trop vite.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe la flaque, un instant.",
            "narrateur|Il écoute le parc, près de l'allée.",
            "enfant-m|Il est mouillé.",
            "papa|Tu restes un peu, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le papier est mou, sous les doigts.",
            "enfant-m|Il pique un peu.",
            "narrateur|Nino reprend le bord du papier, sans se presser.",
            "papa|Tu le vois, le bateau ?",
            "enfant-m|Oui, papa.",
            "maman|Il tient, Nino ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Le ventre de Nino se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près de la flaque ?",
            "enfant-m|Oui.",
            "maman|La goutte tape la capuche ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un pli du bateau attend sur l'eau.",
            "enfant-m|Je le prends.",
            "papa|Tu le poses, Nino ?",
            "enfant-m|Pas tout de suite.",
            "narrateur|Le papier a une petite déchirure.",
            "enfant-m|Il est déchiré.",
            "maman|Tes genoux sont au chaud ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Maman pousse un peu l'herbe près de l'eau.",
            "narrateur|L'herbe est un peu froide.",
            "enfant-m|Le bateau, maintenant !",
            "narrateur|Nino approche la main, trop vite.",
            "narrateur|Le papier se déchire, plus loin.",
            "enfant-m|Il se déchire !",
            "narrateur|Le bateau part vers le milieu.",
            "enfant-m|Il part !",
            "narrateur|Nino avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Nino refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe la flaque, un instant.",
            "narrateur|Il écoute le parc, près de l'allée.",
            "narrateur|Sur le tissu, un éclat de capuche luit.",
            "enfant-m|Là, sur le tissu.",
            "narrateur|Nino attend, les mains ouvertes.",
            "enfant-m|Je veux un câlin.",
            "maman|Tu viens, Nino ?",
            "enfant-m|Oui, maman.",
            "narrateur|Maman ouvre les bras.",
            "narrateur|Nino se blottit contre le manteau.",
            "papa|Merci, Nino.",
            "narrateur|Le manteau sent la pluie, un peu tiède.",
            "enfant-m|Il est chaud.",
            "narrateur|Nino pose la joue sur le manteau.",
            "enfant-m|Ça sent la pluie.",
            "maman|La capuche est mouillée, Nino ?",
            "enfant-m|Un peu.",
            "papa|Tu vois le point, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le bateau tient, un peu déchiré.",
            "enfant-m|On le garde.",
            "maman|Une goutte passe sur la capuche.",
            "enfant-m|Elle tape.",
            "papa|On reste ici, Nino ?",
            "enfant-m|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la flaque.",
            "narrateur|Maman essuie une larme sur la joue.",
            "enfant-m|Le bateau est parti, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, près de l'eau.",
            "maman|On est bien, ici.",
            "narrateur|Nino tapote le tissu du doigt.",
            "enfant-m|Il a une trace d'eau.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nino pose sa capuche contre maman.",
            "enfant-m|Elle est mouillée.",
            "papa|Le bateau est resté, Nino.",
            "enfant-m|Oui, un peu déchiré.",
            "narrateur|Ça sent la terre, un peu mouillée.",
            "enfant-m|Et le papier, maman.",
            "maman|Oui, dans l'air.",
            "papa|La goutte tape, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le bateau reste près de l'allée.",
            "narrateur|Un éclat de capuche tient sur le tissu.",
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
            extra_kw["fields"] = {
                "expected_answer": None,
                "accepted_examples": None,
                "retry_prompt": None,
            }
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
    if "c'est trop" in adults or "c est trop" in adults:
        raise SystemExit(f"{SID}: refrain adulte c'est trop")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "luit" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: manque luit à l'ouverture")
    if "tremble" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: manque tremble à l'ouverture")
    if "luit" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: manque luit au climax")
    if "tient" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: manque tient à la fin")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "je suis triste" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: manque je suis triste (acte) à l'ouverture")
    if blob.count("je suis triste") != 1:
        raise SystemExit(f"{SID}: je suis triste ×{blob.count('je suis triste')}")
    if "je veux un câlin" not in blob and "je veux un calin" not in blob:
        raise SystemExit(f"{SID}: manque je veux un câlin")
    if blob.count("je veux un câlin") != 1:
        raise SystemExit(f"{SID}: je veux un câlin ×{blob.count('je veux un câlin')}")
    if "nino pleure" not in blob:
        raise SystemExit(f"{SID}: manque nino pleure")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Nino = enfant-m)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé")
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
        "pleurer est permis",
        "le câlin aide",
        "c'est de la tristesse",
        "j'ai dit : je suis",
        "tu as nommé",
        "l'histoire est finie",
        "c'est permis",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Nino a les yeux chauds. Que dit-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "triste":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "triste | je suis triste | câlin | un câlin | pleurer"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Nino peut demander un câlin. Que dit-il ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    for c in chunks:
        if c["chunk_id"] == "CHK_T0000_P0000_Q0001":
            continue
        if c.get("expected_answer") not in (None, ""):
            raise SystemExit(f"{SID}: expected hors Q ({c['chunk_id']})")
        if c.get("accepted_examples") not in (None, ""):
            raise SystemExit(f"{SID}: accepted hors Q ({c['chunk_id']})")
        if c.get("retry_prompt") not in (None, ""):
            raise SystemExit(f"{SID}: retry hors Q ({c['chunk_id']})")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "nino est au parc" in opening:
        raise SystemExit(f"{SID}: ouverture dump (nino est au parc)")
    if opening.splitlines()[0].startswith("narrateur|après la pluie"):
        raise SystemExit(f"{SID}: ouverture dump (après la pluie)")
    if "parc" not in blob:
        raise SystemExit(f"{SID}: manque parc")
    if "bateau" not in blob:
        raise SystemExit(f"{SID}: manque bateau")
    if "papier" not in blob:
        raise SystemExit(f"{SID}: manque papier")
    if "flaque" not in blob:
        raise SystemExit(f"{SID}: manque flaque")
    if "pluie" not in blob:
        raise SystemExit(f"{SID}: manque pluie")
    for ban in (
        "éclat de flaque",
        "éclat de bateau",
        "éclat de papier",
        "éclat de grille",
        "éclat de banc",
        "éclat de tapis",
        "tout doux",
        "tout calme",
        "tout doucement",
        "merle",
        "miel",
    ):
        if ban in blob:
            raise SystemExit(f"{SID}: BAN {ban}")
    if re.search(r"\b(banc|grille|tapis)\b", blob):
        raise SystemExit(f"{SID}: BAN banc/grille/tapis")
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
    if not (700 <= nwords <= 850):
        raise SystemExit(f"{SID}: {nwords} mots hors 700-850")

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
        "- **Leçon :** EMO.LEX.002 — nommer la tristesse + demander un "
        "câlin (vécue : Nino dit « je suis triste », pleure, demande un "
        "câlin ; bateau emporté, papier déchiré, poitrine trop vite, "
        "sourire parti, papa accroupi ; 2e ruse : papier qui se déchire "
        "plus loin, bateau qui part, il refuse de foncer). JAMAIS dite "
        "dans le récit. Pas « pleurer est permis ». Pas « le câlin aide ». "
        "Pas « c'est de la tristesse ». Pas « tu as nommé ». Pas "
        "« j'ai dit : je suis ».\n"
        "- **Personnages :** Nino, papa, maman. Nino = enfant-m. Pas de "
        "copain. Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** parc, après la pluie, flaque, bateau, papier, "
        "capuche, allée, herbe, manteau, poche, tissu. BAN banc / grille "
        "/ tapis (indice et mot). Bateau / flaque / papier = dump.\n"
        "- **Indice unique :** éclat de capuche (luit à l'ouverture → "
        "tremble à la déchirure → luit quand le bateau part → tient sur "
        "le tissu). BAN éclat de flaque / bateau / papier / grille / "
        "banc / tapis.\n"
        "- **Question moteur :** « Nino a les yeux chauds. Que dit-il ? » "
        "expected dump **triste**. accepted dump "
        "`triste | je suis triste | câlin | un câlin | pleurer`. "
        "retry dump gardé. Non récitée dans les autres chunks. Hors Q : "
        "expected / accepted / retry = null.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte tape la capuche. Un détail paraît : sur le tissu, un "
        "éclat de capuche luit. Bateau de papier, flaque ronde. Il veut "
        "le bateau **maintenant**. L'eau l'emporte. Le papier se déchire. "
        "Poitrine trop vite. Sourire parti. Yeux chauds. « je suis "
        "triste ». Il pleure. Papa s'accroupit. Merci vécu, après le "
        "câlin. Deuxième ruse : papier qui se déchire plus loin, bateau "
        "qui part. Il s'arrête, lit l'éclat, demande un câlin. Un éclat "
        "de capuche tient sur le tissu.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : parc après la pluie, goutte sur la capuche, allée, "
        "herbe lourde.\n"
        "- Désir : faire partir le bateau de papier, maintenant.\n"
        "- Objet : bateau, papier, flaque (objets dump, pas l'indice).\n"
        "- Indice unique : éclat de capuche, vu dès l'ouverture, payé "
        "sur le tissu. Pas éclat de flaque / bateau / papier.\n"
        "- Urgence douce : il pose le bateau trop vite.\n"
        "- Imprévu 1 : l'eau emporte, le papier se déchire, poitrine "
        "trop vite, sourire parti, yeux chauds.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le câlin.\n"
        "- Imprévu 2 (plus rusé) : le papier se déchire plus loin, le "
        "bateau part vers le milieu.\n"
        "- Résolution : il refuse de foncer, observe, écoute le parc, "
        "retrouve l'éclat, demande un câlin.\n"
        "- Retour : bateau un peu déchiré, goutte sur la capuche, éclat "
        "sur le tissu.\n\n"
        "## Vécu\n\n"
        "Nino veut le bateau **maintenant**. Il dit « je suis triste » "
        "(acte, une fois). Il pleure. Impatience, puis bateau parti, "
        "sourire parti. Il s'arrête, observe. Papa se baisse, pose une "
        "question, ne récite pas la règle. Papier qui se déchire plus "
        "loin, bateau qui part. Il refuse de foncer. Il demande un "
        "câlin. Merci vécu. Fin : l'éclat du début tient sur le tissu.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Nino et le bateau de papier (noyau dump). Relance : "
        "Que dit-il ? expected triste.\n"
        "- Lieu du dump-meta (parc, après la pluie). Maman et papa. "
        "Nino = héros enfant-m.\n"
        "- Ouverture inventée (goutte sur la capuche), pas un gabarit "
        "v2, pas « Après la pluie, le parc sent », pas « Nino est au "
        "parc ».\n"
        "- Indice unique : éclat de capuche. BAN éclat de flaque / "
        "bateau / papier / grille / banc / tapis. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doucement » du dump. BAN banc / grille / "
        "tapis.\n"
        "- Leçon non dite : on la voit quand il dit « je suis triste », "
        "quand il pleure, quand il demande un câlin. Pas « pleurer est "
        "permis ». Pas « le câlin aide ». Pas « c'est de la tristesse ». "
        "Pas « tu as nommé ». Pas « j'ai dit : je suis ». Pas "
        "« L'histoire est finie ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Nino a les yeux chauds. Que dit-il ? ». "
        "expected triste. 5 chunks, kinds inchangés. expected/accepted/"
        "retry dump conservés. Hors Q : null.\n"
        "- example4 062 / 094 / 026 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N2 / raw.js.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers le bateau qui part.\n"
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
