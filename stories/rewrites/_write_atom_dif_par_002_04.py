#!/usr/bin/env python3
"""ATOM-DIF.PAR.002-04 — Raphaël laisse le temps à Nina (F-NAR-019, N3, DIF.PAR.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.002-04"
TITLE = "Raphaël laisse le temps à Nina"
N3 = LIMITS["N3"]
CHARS = "Raphaël, Nina, papa, maman"
SETTING = (
    "marché : étals, toile, balance, fraises, sac en papier, "
    "poule, poires, tentes"
)
INDICE = "éclat d'étal"
FIL = (
    "Une goutte glisse sur la balance. Au bord, un éclat d'étal "
    "brille. Raphaël connaît le mot de la poule, maintenant. Nina "
    "s'arrête. Il ouvre la bouche, dit trop vite. Sourire parti, "
    "poitrine, papa accroupi. Il referme, attend. Merci vécu. Aux "
    "poires, sac trop vite, tente qui claque, mot qui tombe. Il "
    "revoit l'éclat. Un éclat d'étal tient au bord."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(cageot|rotin|panier|caisse|plateau|carotte|pupitre|"
    r"parquet|banc|tartine|puits|cigale|flaque|piquet|bol|"
    r"maîtresse|maitresse|valentine|nino|merle|miel|octave|tess)\b",
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
    "il faut demander",
    "on peut jouer",
    "on peut attendre",
    "on n'imite pas",
    "on n imite pas",
    "on ne force pas la parole",
    "ne force pas la parole",
    "tu as su attendre",
    "on peut tendre",
    "on peut laisser",
    "on laisse le temps",
    "laisser le temps",
    "laisse le temps",
    "fin de la phrase",
    "n'achève pas",
    "n acheve pas",
    "l'un après l'autre",
    "l un apres l autre",
    "vous parlez",
    "j'ai laissé le temps",
    "j'ai laisse le temps",
    "j'ai attendu la fin",
    "ce n'est pas une faute",
    "vous jouez",
    "on joue",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "trois notes",
    "lumière couleur de miel",
    "lumiere couleur de miel",
    "éclat de plateau",
    "éclat de carotte",
    "éclat de pupitre",
    "éclat de cageot",
    "éclat de rotin",
    "éclat de panier",
    "éclat de caisse",
    "éclat de toile",
    "éclat de balance",
    "éclat de fraise",
    "éclat de poire",
    "éclat de sac",
    "éclat de tente",
    "éclat de plume",
    "éclat de pain",
    "éclat de poule",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat d'étal",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_connait_le_mot_ouvre_la_bouche; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Nina",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=nina_cherche_un_mot_que_fait_raphael; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="attend",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_referme_la_bouche_attend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat d'étal",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=sac_trop_vite_mot_qui_tombe_il_referme; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat d'étal",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_au_bord; "
            "tempo=posé; sourire=léger; respiration=ample"
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
        "balance,toile",
        [
            "narrateur|Une goutte glisse sur le métal de la balance.",
            "enfant-m|Elle brille, papa.",
            "papa|Tu la vois, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|La goutte s'étire, puis tombe sur la toile.",
            "enfant-m|Elle a fait un rond.",
            "maman|La toile est tendue, Raphaël ?",
            "enfant-m|Oui, maman.",
            "narrateur|Ça sent le pain chaud, tout près.",
            "enfant-m|Ça sent le pain, papa.",
            "papa|Tu le sens, toi ?",
            "enfant-m|Oui, fort.",
            "narrateur|Des fraises rouges tiennent sur la toile.",
            "enfant-m|Elles sont lisses.",
            "maman|Elles sentent fort, tu trouves ?",
            "enfant-m|Oui, maman.",
            "narrateur|Au bord, un éclat d'étal brille.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, ce petit point ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|Un sac en papier froisse, crac.",
            "enfant-m|Il est rêche.",
            "maman|Tu le tiens, Raphaël ?",
            "enfant-m|Oui, maman.",
            "narrateur|Au loin, une poule fait cot-cot.",
            "enfant-m|J'entends la poule !",
            "papa|Elle est derrière l'étal ?",
            "enfant-m|Oui, papa.",
            "narrateur|Nina arrive près de la toile.",
            "narrateur|Elle regarde les fraises, puis la poule.",
            "narrateur|Une plume jaune tient sous la toile.",
            "enfant-m|La plume, papa.",
            "papa|Tu la vois, la plume ?",
            "enfant-m|Oui, jaune.",
            "narrateur|En ce moment, Raphaël veut dire le mot.",
            "enfant-m|Je le dis, maintenant !",
            "enfant-m|Le mot de la poule, tout de suite.",
            "maman|Tu le connais, Raphaël ?",
            "enfant-m|Oui, maman.",
            "copine|J'ai vu.",
            "narrateur|Nina s'arrête.",
            "narrateur|Ses lèvres bougent, sans le mot.",
            "narrateur|Raphaël connaît le mot.",
            "narrateur|Il ouvre la bouche.",
            "enfant-m|Poule !",
            "narrateur|Nina baisse les yeux.",
            "narrateur|Ses épaules se serrent.",
            "enfant-m|Oh.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Nina, Raphaël ?",
            "enfant-m|Oui, papa.",
            "maman|Ta bouche est ouverte, Raphaël ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Raphaël refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le bord, un instant.",
            "narrateur|L'éclat d'étal tremble, puis tient.",
            "enfant-m|L'éclat, papa ?",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur le bord.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nina cherche un mot.",
            "narrateur|Que fait Raphaël ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "sac,poule",
        [
            "narrateur|Raphaël tient le sac, sans parler.",
            "narrateur|Sa bouche reste fermée.",
            "narrateur|Il attend.",
            "narrateur|Nina respire, un peu plus large.",
            "copine|J'ai vu une poule.",
            "enfant-m|Une poule.",
            "copine|Elle faisait cot-cot.",
            "enfant-m|Cot-cot.",
            "papa|Tu l'as entendue, Raphaël ?",
            "enfant-m|Oui, papa.",
            "maman|Tu as entendu Nina ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le ventre de Raphaël se desserre.",
            "maman|Merci, Raphaël.",
            "narrateur|Maman a vu la bouche fermée.",
            "papa|Les poires sont plus loin ?",
            "enfant-m|Oui, papa.",
            "narrateur|Ils avancent vers les poires.",
            "narrateur|Les poires sont vertes, un peu bosselées.",
            "enfant-m|Elles sont dures.",
            "maman|Tu les touches, Raphaël ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Un éclat d'étal luit au bord.",
            "enfant-m|Le point, papa.",
            "papa|Sur la toile, Raphaël ?",
            "enfant-m|Oui, il tient.",
            "narrateur|Le sac froisse contre la jambe.",
            "enfant-m|Il est rêche, maman.",
            "maman|On le garde ouvert ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le sol colle un peu, sous les pas.",
            "enfant-m|Il colle, papa.",
            "papa|Tu le sens, le sol ?",
            "enfant-m|Oui.",
            "narrateur|Nina marche à côté, le sac trop grand.",
            "enfant-m|Elle tient le bord.",
            "narrateur|Le papier est tiède, à cause du soleil.",
            "enfant-m|Il est chaud, maman.",
            "maman|Le soleil est dessus ?",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "tente,sac",
        [
            "narrateur|Ils s'arrêtent près des poires.",
            "enfant-m|Je prends, maintenant !",
            "narrateur|Raphaël avance le sac trop vite.",
            "narrateur|Le papier froisse trop fort.",
            "narrateur|Nina recule d'un pas.",
            "enfant-m|Oh.",
            "narrateur|Raphaël refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe une poire, un instant.",
            "narrateur|La toile claque, légère.",
            "narrateur|Il revoit l'éclat d'étal.",
            "narrateur|Une tente claque au-dessus d'eux.",
            "copine|Je veux.",
            "narrateur|Nina sursaute.",
            "narrateur|Le mot tombe.",
            "narrateur|Raphaël connaît le mot.",
            "narrateur|Il ouvre la bouche.",
            "narrateur|Puis il la referme.",
            "narrateur|Il attend.",
            "copine|Je veux une poire.",
            "papa|Une poire, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa prend une poire dans le papier.",
            "narrateur|Le papier est rêche, contre les doigts.",
            "copine|Elle est.",
            "narrateur|Nina s'arrête.",
            "narrateur|Raphaël garde la bouche fermée.",
            "copine|Elle est douce.",
            "enfant-m|Douce, oui.",
            "maman|Tes mains tiennent le sac, Raphaël ?",
            "enfant-m|Oui, maman.",
            "papa|On a la poire, vous deux ?",
            "enfant-m|Oui, papa.",
            "narrateur|Nina souffle, longuement.",
            "enfant-m|Elle a dit, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-m|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "toile",
        [
            "narrateur|Ils restent près de la toile.",
            "maman|La poule est restée, Raphaël ?",
            "enfant-m|Oui, maman.",
            "papa|Tu donnes la main, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Raphaël donne la main.",
            "narrateur|Nina porte le petit sac.",
            "enfant-m|La poire est dedans.",
            "copine|Poule.",
            "enfant-m|Poule.",
            "papa|Le sac est un peu lourd ?",
            "enfant-m|Un peu, papa.",
            "maman|On rentre entre les tentes ?",
            "enfant-m|Oui, maman.",
            "narrateur|Au loin, la poule fait cot-cot.",
            "enfant-m|Je l'entends.",
            "narrateur|Un éclat d'étal tient au bord.",
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
    if n_clue != 5:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 5)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "ouvre la bouche" not in blob:
        raise SystemExit(f"{SID}: manque ouvre la bouche")
    if "referme la bouche" not in blob and "la referme" not in blob:
        raise SystemExit(f"{SID}: manque referme la bouche")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Raphaël = enfant-m, Nina = copine)")
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
        "on n'imite pas",
        "on ne force pas la parole",
        "tu as su attendre",
        "on peut attendre",
        "on peut laisser",
        "on laisse le temps",
        "laisser le temps",
        "laisse le temps",
        "fin de la phrase",
        "n'achève pas",
        "l'un après l'autre",
        "vous parlez",
        "on peut tendre",
        "on peut jouer",
        "on joue",
        "vous jouez",
        "il faut attendre",
        "on doit demander",
        "il faut demander",
        "cherche un mot",
        "j'ai laissé le temps",
        "j'ai attendu la fin",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Nina cherche un mot. Que fait Raphaël ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") is not None:
        raise SystemExit(f"{SID}: expected_answer doit rester null")
    if q.get("accepted_examples") is not None:
        raise SystemExit(f"{SID}: accepted_examples doit rester null")
    if q.get("retry_prompt") is not None:
        raise SystemExit(f"{SID}: retry_prompt doit rester null")
    for need in (
        "balance",
        "toile",
        "fraise",
        "poule",
        "poire",
        "sac",
        "tente",
    ):
        if need not in blob:
            raise SystemExit(f"{SID}: manque {need}")
    for ban in (
        "cageot",
        "rotin",
        "panier",
        "caisse",
        "éclat de plateau",
        "éclat de carotte",
        "éclat de pupitre",
        "tout doux",
        "tout calme",
        "octave",
        "tess",
        "mila",
        "aniss",
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
    slow_ids = {
        c["chunk_id"]
        for c in chunks
        if c.get("rate_label") == "slow"
    }
    if slow_ids != {"CHK_T0000_P0000_Q0001", "CHK_T0000_P0000_END_F0001"}:
        raise SystemExit(f"{SID}: slow mal placé: {slow_ids}")

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
        "- **Public :** N3 (≤16 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.PAR.002 — ne pas finir la phrase de l'autre "
        "(vécue : Raphaël connaît le mot, ouvre la bouche **maintenant**, "
        "dit trop vite, Nina baisse les yeux ; il refuse de foncer, "
        "referme, attend ; aux poires, sac trop vite, tente qui claque, "
        "mot qui tombe, il referme). JAMAIS dite. Pas « on laisse le "
        "temps ». Pas « on n'achève pas ». Pas « tu as su attendre ».\n"
        "- **Personnages :** Raphaël, Nina, papa, maman. Dump Octave/"
        "Tess → D16. Raphaël = enfant-m (connaît le mot, ouvre la "
        "bouche maintenant, referme, attend). Nina = copine (cherche "
        "un mot : J'ai vu / Je veux / Elle est, puis finit). Papa et "
        "maman parlent. Pas de maîtresse.\n"
        "- **Lieu :** marché (étals, toile, balance, fraises, sac en "
        "papier, poule, poires, tentes). Noyau dump : poule du marché. "
        "≠ 002-01 carotte / 002-02 pupitre / 002-03 plateau. BAN "
        "cageot / rotin / panier / caisse.\n"
        "- **Indice unique :** éclat d'étal (brille à l'ouverture sur "
        "le bord → tremble → luit → revoit → tient au bord). BAN "
        "éclat de plateau / carotte / pupitre / cageot / toile / "
        "balance / fraise / poire / sac / tente.\n"
        "- **Question moteur :** « Nina cherche un mot. Que fait "
        "Raphaël ? » (dump Tess/Octave → Nina/Raphaël). expected / "
        "accepted / retry **null** (laissés null). Non récitée comme "
        "slogan dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte glisse sur le métal de la balance, puis tombe sur "
        "la toile. Au bord, un éclat d'étal brille. Fraises, sac, "
        "poule au loin, plume jaune. Raphaël veut dire le mot "
        "**maintenant**. Nina s'arrête : J'ai vu. Il connaît le mot, "
        "ouvre la bouche, dit trop vite. Nina baisse les yeux. Sourire "
        "parti, poitrine, papa accroupi. Il refuse de foncer, referme "
        "la bouche. Question. Il attend. Nina finit : une poule. Merci "
        "vécu. Deuxième ruse : sac trop vite, tente qui claque, le mot "
        "tombe. Il ouvre, referme, attend. Un éclat d'étal tient au "
        "bord.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : marché, toile, balance, fraises, sac en papier, "
        "poule, poires, tentes. ≠ 002-01 carotte / 002-02 pupitre / "
        "002-03 plateau. Pas cageot / rotin / panier / caisse.\n"
        "- Désir : dire le mot de la poule, maintenant.\n"
        "- Objet : poule entendue, sac en papier, poire.\n"
        "- Indice unique : éclat d'étal, vu dès l'ouverture au bord, "
        "payé au bord. Pas éclat de plateau / carotte / pupitre.\n"
        "- Urgence douce : le mot, tout de suite.\n"
        "- Imprévu 1 : il finit « poule », Nina baisse les yeux.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après la "
        "bouche fermée.\n"
        "- Imprévu 2 (plus rusé) : sac trop vite, tente qui claque, "
        "le mot tombe.\n"
        "- Résolution : il refuse de foncer, ouvre, referme, attend. "
        "Nina dit la poire, puis douce.\n"
        "- Retour : sac un peu lourd, poule au loin, éclat au bord.\n\n"
        "## Vécu\n\n"
        "Raphaël connaît le mot **maintenant**. Impatience, bouche "
        "ouverte, mot trop vite, Nina qui se ferme. Le silence compte. "
        "Papa se baisse, pose une question, ne récite pas « on laisse "
        "le temps ». Il agit : bouche refermée, attente. Merci vécu. "
        "Fin : l'éclat du début tient au bord. Le dénouement a failli : "
        "Nina a reculé deux fois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Raphaël laisse le temps à Nina (noyau « laisse le "
        "temps », prénoms D16). Noyau dump : poule du marché. Relance : "
        "Que fait Raphaël ? expected null.\n"
        "- Lieu du dump (marché) sans cageot / rotin / panier / caisse. "
        "Maman présente. Nina = copine.\n"
        "- Ouverture inventée (goutte sur le métal de la balance), pas "
        "un gabarit v2, pas « Les tentes du marché claquent un peu au "
        "vent » du dump en première ligne.\n"
        "- Indice unique : éclat d'étal. BAN éclat de plateau / "
        "carotte / pupitre / cageot / toile / balance. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip slogans du dump : on peut laisser le temps, "
        "on attend la fin de la phrase, tu as su attendre, bravo, "
        "vous parlez l'un après l'autre.\n"
        "- Leçon non dite : on la voit quand il dit trop vite, quand "
        "Nina baisse les yeux, quand il referme, quand il attend. Pas "
        "« on laisse le temps ». Pas « on n'achève pas ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Nina cherche un mot. Que fait "
        "Raphaël ? ». expected / accepted / retry **null**. 5 chunks, "
        "kinds inchangés.\n"
        "- example4 034 / 066 / 098 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_par_001_03.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers les poires.\n"
        f"- {nwords} mots. N3 ≤ 16. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n"
        "- 1 × `en ce moment`, 1 × merci adulte, 5 × éclat d'étal\n"
        "- expected / accepted / retry null\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")


if __name__ == "__main__":
    main()
