#!/usr/bin/env python3
"""ATOM-EMO.LEX.002-07 — Mila et le doudou rose (F-NAR-019, N1, EMO.LEX.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.002-07"
TITLE = "Mila et le doudou rose"
N1 = LIMITS["N1"]
CHARS = "Mila, papa, maman"
SETTING = (
    "chambre, soir, housse, lit, doudou, panier, "
    "oreiller, radiateur, fenêtre, veilleuse, verre"
)
INDICE = "éclat de housse"
FIL = (
    "Un tic léger traverse la chambre. Sur la housse, "
    "un éclat de housse luit. Mila veut le doudou rose, "
    "maintenant. Le doudou n'est pas là. Sourire parti. "
    "Poitrine serrée. Yeux chauds. Papa s'accroupit. "
    "Mila dit qu'elle est triste. Elle pleure. Elle demande "
    "un câlin. Merci vécu. Deuxième ruse : le doudou vu, "
    "puis disparu, oreille coincée dans le panier. "
    "Elle refuse de foncer. Papa trouve. "
    "Un éclat de housse tient sur le tissu."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(merle|miel|couverture|plaid|coussin|lampe|tapis|"
    r"fauteuil|paillasson|coffre|haie|capuche|treille|moule|"
    r"chaussette|table|savon|maîtresse|maitresse|"
    r"grand-père|grand-pere|jardinier|bibliothécaire|bibliothecaire|"
    r"gardienne|céline|celine)\b",
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
    "c'est de la tristesse",
    "c est de la tristesse",
    "c'est de la joie",
    "pleurer est permis",
    "le câlin aide",
    "le calin aide",
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
    "éclat de couverture",
    "éclat de panier",
    "éclat de lit",
    "éclat de plaid",
    "éclat de coussin",
    "éclat de lampe",
    "éclat de tapis",
    "éclat de fauteuil",
    "éclat de paillasson",
    "éclat de coffre",
    "éclat de haie",
    "éclat de capuche",
    "éclat de treille",
    "éclat de moule",
    "éclat de doudou",
    "éclat de tour",
    "éclat de cube",
    "éclat de rideau",
    "toute calme",
    "tout calme",
)

# N1 : mêmes champs que GES.002-01 (voix N1, tempos plus lents).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat de housse",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis tristesse; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_doudou_maintenant; "
            "tempo=posé puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=104, speed=0.80, piper=1.36, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=780,
        sentence=360, energy="focused", contour="rising", noise=0.30,
        emphasis="Mila",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=mila_a_les_yeux_chauds_que_dit_elle; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=122, speed=0.88, piper=1.24, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=620,
        sentence=310, energy="bright", contour="falling", noise=0.33,
        emphasis="câlin",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis soulagement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_demande_un_calin_sans_slogan; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de housse",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=doudou_vu_puis_disparu_oreille_coincée_panier; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de housse",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_soulagement; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_tissu; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "triste",
    "accepted_examples": "triste | je suis triste | câlin | un câlin",
    "retry_prompt": "Mila peut demander un câlin. Que dit-elle ?",
    "engine_ok_text": "Oui, triste.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "",
        [
            "narrateur|Un tic léger traverse la chambre.",
            "enfant-f|Je l'entends, papa.",
            "papa|Tu l'entends, le tic ?",
            "enfant-f|Oui, papa.",
            "narrateur|La housse du lit sent le linge.",
            "enfant-f|Ça sent le linge, maman.",
            "maman|Tu le sens, le linge tiède ?",
            "enfant-f|Oui, maman.",
            "narrateur|La veilleuse dessine un rond rose.",
            "enfant-f|Il est sur le mur.",
            "maman|Tu le vois, le rond ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le lit de Mila est un peu défait.",
            "enfant-f|L'oreiller est tiède.",
            "papa|On range le lit, Mila ?",
            "enfant-f|Oui, avec le doudou.",
            "maman|Le doudou rose ?",
            "enfant-f|Le rose, maman.",
            "narrateur|Sur la housse, un éclat de housse luit.",
            "enfant-f|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-f|Oui, un point clair.",
            "papa|La veilleuse le touche.",
            "narrateur|Un rayon glisse sur le bord.",
            "narrateur|La fenêtre est un peu embuée.",
            "papa|J'apporte le verre d'eau.",
            "enfant-f|Le doudou d'abord.",
            "narrateur|En ce moment, Mila cherche le doudou rose.",
            "enfant-f|Je le veux, maintenant !",
            "papa|Tout de suite ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila fouille sous l'oreiller, trop vite.",
            "narrateur|Sa main sort, vide.",
            "enfant-f|Pas là.",
            "maman|Sous le lit ?",
            "enfant-f|Je regarde.",
            "narrateur|Elle se baisse trop vite, près du bois.",
            "narrateur|Le doudou n'est pas là.",
            "enfant-f|Maman, il n'est pas là.",
            "maman|On cherche, Mila ?",
            "enfant-f|Oui.",
            "narrateur|Elle regarde le panier, près de la porte.",
            "narrateur|Rien de rose, sous ses genoux.",
            "enfant-f|Il est parti.",
            "narrateur|Mila avance trop vite vers le panier.",
            "narrateur|Sa main heurte le bord.",
            "enfant-f|Aïe.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, ça se serre.",
            "narrateur|L'envie et la peur se heurtent.",
            "narrateur|Ses épaules tombent un peu.",
            "enfant-f|J'ai mal au ventre.",
            "narrateur|Ses yeux deviennent chauds.",
            "narrateur|Une larme tombe sur le tissu.",
            "enfant-f|Je suis triste.",
            "narrateur|Mila pleure un peu, sans crier.",
            "narrateur|Les larmes coulent sur ses joues.",
            "papa|Tu as les yeux chauds, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "maman|Tes mains sont chaudes, Mila ?",
            "enfant-f|Un peu, maman.",
            "enfant-f|Je veux un câlin.",
            "maman|Viens.",
            "narrateur|Maman ouvre les bras.",
            "narrateur|Mila se blottit contre maman.",
            "narrateur|Le câlin est chaud, près du cou.",
            "narrateur|Ça sent le linge de maman.",
            "narrateur|L'éclat de housse tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Mila a les yeux chauds.",
            "narrateur|Que dit-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Mila reste contre maman, un moment.",
            "enfant-f|Le doudou, maintenant.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Je le prends.",
            "narrateur|Mila avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe la chambre, un instant.",
            "narrateur|Elle écoute le soir, près du lit.",
            "papa|Tu restes un peu, Mila ?",
            "enfant-f|Oui, papa.",
            "papa|Merci, Mila.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le câlin est tiède, sous les bras.",
            "enfant-f|Il est chaud.",
            "narrateur|La poitrine de Mila ralentit un peu.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tes joues sont mouillées, Mila ?",
            "enfant-f|Un peu, maman.",
            "papa|On cherche sans se presser ?",
            "enfant-f|Oui.",
            "narrateur|Maman essuie une larme du pouce.",
            "enfant-f|Ça pique les yeux.",
            "maman|La veilleuse éclaire la housse ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le ventre de Mila se desserre.",
            "papa|On regarde près du panier ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila tient le tissu de maman.",
            "enfant-f|Je reste un peu.",
            "narrateur|Ils se lèvent, sans se bousculer.",
            "enfant-f|Le rose, papa.",
            "papa|On y va, sans se presser.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Papa se baisse près du panier.",
            "narrateur|Un bout rose passe, une seconde.",
            "enfant-f|Le doudou !",
            "narrateur|Mila avance trop vite, tout de suite.",
            "narrateur|Le bout rose disparaît.",
            "enfant-f|Il part !",
            "narrateur|L'oreille glisse sous le linge.",
            "narrateur|Mila avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Mila refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le panier, un instant.",
            "narrateur|Elle écoute la chambre, près du bois.",
            "narrateur|Sur la housse, un éclat de housse luit.",
            "enfant-f|Là, sur le tissu.",
            "papa|On tient le bord ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le linge du panier pend un peu.",
            "narrateur|Une oreille rose reste coincée.",
            "enfant-f|Elle est coincée !",
            "maman|Tu la vois, l'oreille ?",
            "enfant-f|Oui, maman.",
            "narrateur|Mila veut tirer, tout de suite.",
            "narrateur|Puis elle lâche le tissu.",
            "papa|J'y vais, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa glisse la main, sans se presser.",
            "narrateur|L'oreille faillit partir plus loin.",
            "enfant-f|Doucement.",
            "papa|Je la tiens.",
            "narrateur|Papa tire le doudou, tout petit à petit.",
            "narrateur|Le rose revient vers le panier.",
            "enfant-f|Mon doudou !",
            "narrateur|Mila le serre contre elle.",
            "maman|Le tissu est tiède, Mila ?",
            "enfant-f|Un peu.",
            "papa|L'oreille est un peu froissée.",
            "enfant-f|Elle a une trace.",
            "papa|Tu vois le point, Mila ?",
            "enfant-f|Oui, papa.",
            "papa|On reste près du lit ?",
            "enfant-f|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du lit.",
            "narrateur|Maman essuie un peu de linge.",
            "enfant-f|Papa a trouvé le doudou.",
            "papa|Tu l'as vu, toi ?",
            "enfant-f|Oui, dans le panier.",
            "maman|On est bien, ici.",
            "narrateur|Mila tapote le tissu du doigt.",
            "enfant-f|Il a une oreille froissée.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|Le doudou est resté, Mila.",
            "enfant-f|Oui, avec l'oreille.",
            "narrateur|Ça sent le linge, un peu tiède.",
            "enfant-f|Et le rose, maman.",
            "maman|Oui, dans l'air.",
            "papa|La chambre est douce, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le doudou reste contre le lit.",
            "narrateur|Un éclat de housse tient sur le tissu.",
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
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Mila = enfant-f)")
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
        "pleurer est permis",
        "le câlin aide",
        "le calin aide",
        "c'est de la tristesse",
        "c est de la tristesse",
        "j'ai dit",
        "j ai dit",
        "tu as nommé",
        "tu as nomme",
        "l'histoire est finie",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Mila a les yeux chauds. Que dit-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "triste":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "triste | je suis triste | câlin | un câlin"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Mila peut demander un câlin. Que dit-elle ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    if "céline" in retry.lower() or "celine" in retry.lower():
        raise SystemExit(f"{SID}: Céline resté dans retry")
    for c in chunks:
        if c["chunk_id"] == "CHK_T0000_P0000_Q0001":
            continue
        if c.get("expected_answer") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: expected hors Q")
        if c.get("accepted_examples") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: accepted hors Q")
        if c.get("retry_prompt") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: retry hors Q")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "je suis triste" not in opening:
        raise SystemExit(f"{SID}: nommage absent avant la question")
    n_triste = blob.count("je suis triste")
    if n_triste != 1:
        raise SystemExit(f"{SID}: je suis triste ×{n_triste}")
    if "câlin" not in opening and "calin" not in opening:
        raise SystemExit(f"{SID}: câlin absent avant la question")
    if "doudou" not in blob:
        raise SystemExit(f"{SID}: manque doudou")
    if "panier" not in blob:
        raise SystemExit(f"{SID}: manque panier")
    if "lit" not in blob:
        raise SystemExit(f"{SID}: manque lit")
    if "housse" not in blob:
        raise SystemExit(f"{SID}: manque housse")
    if "s'accroupit" not in opening and "s accroupit" not in opening:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    if "sourire" not in opening:
        raise SystemExit(f"{SID}: manque sourire parti")
    if "poitrine" not in opening:
        raise SystemExit(f"{SID}: manque poitrine")
    if "coincée" not in by["CHK_T0000_P0000_END"]["text"].lower() and (
        "coincee" not in by["CHK_T0000_P0000_END"]["text"].lower()
    ):
        raise SystemExit(f"{SID}: manque oreille coincée")
    if "disparaît" not in by["CHK_T0000_P0000_END"]["text"].lower() and (
        "disparait" not in by["CHK_T0000_P0000_END"]["text"].lower()
    ):
        raise SystemExit(f"{SID}: manque doudou disparu")
    if "panier" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: papa doit trouver dans le panier")
    if "papa" not in by["CHK_T0000_P0000_END"]["script"].lower():
        raise SystemExit(f"{SID}: papa absent au 2e imprévu")
    for ban in (
        "éclat de doudou",
        "éclat de lampe",
        "éclat de tapis",
        "éclat de lit",
        "éclat de plaid",
        "éclat de coussin",
        "éclat de couverture",
        "éclat de panier",
        "éclat de fauteuil",
        "éclat de paillasson",
        "éclat de coffre",
        "éclat de haie",
        "éclat de capuche",
        "éclat de treille",
        "éclat de moule",
        "tout doux",
        "tout calme",
        "toute calme",
        "merle",
        "miel",
        "céline",
        "celine",
        "couverture",
        " plaid",
        "coussin",
        "lampe",
        "tapis",
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
        "- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans\n"
        "- **Leçon :** EMO.LEX.002 — nommer la tristesse + demander un "
        "câlin (vécue : doudou perdu, sourire parti, poitrine serrée, "
        "yeux chauds, Mila dit je suis triste, pleure, demande un câlin, "
        "maman ouvre les bras ; 2e ruse : doudou vu puis disparu, oreille "
        "coincée dans le panier, elle refuse de foncer, papa trouve). "
        "JAMAIS dite dans le récit. Pas « pleurer est permis ». Pas "
        "« le câlin aide ». Pas « c'est de la tristesse ». Pas "
        "« j'ai dit : je suis ».\n"
        "- **Personnages :** Mila, papa, maman. Dump Céline → D16 Mila = "
        "enfant-f (veut le doudou maintenant). Pas de copain (dump sans "
        "camarade). Troupe D16. Pas de maîtresse. Distinct 002-01 "
        "(Aniss, doudou bleu).\n"
        "- **Lieu :** chambre, soir, housse, lit, doudou, panier, "
        "oreiller, radiateur, fenêtre, veilleuse, verre. Dump doudou / "
        "panier / lit gardés. BAN couverture / plaid / coussin / lampe / "
        "tapis (indice pris ailleurs).\n"
        "- **Indice unique :** éclat de housse (luit à l'ouverture → "
        "tremble aux larmes → luit quand l'oreille est coincée → tient "
        "sur le tissu). BAN éclat de doudou / couverture / panier / lit / "
        "plaid / coussin / lampe / tapis. Pas fauteuil / paillasson / "
        "coffre / haie / capuche / treille / moule.\n"
        "- **Question moteur :** « Mila a les yeux chauds. Que dit-elle ? » "
        "expected dump **triste**. accepted dump "
        "`triste | je suis triste | câlin | un câlin`. "
        "retry dump Céline → Mila (dit-elle). Non récitée dans les autres "
        "chunks. Hors Q : expected / accepted / retry nuls.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un tic léger traverse la chambre. Linge, veilleuse, rond rose, "
        "fenêtre embuée. Sur la housse, un éclat de housse luit. "
        "Mila veut le doudou **maintenant**. Le doudou n'est pas là. "
        "Sourire parti. Poitrine serrée. Yeux chauds. Papa s'accroupit. "
        "Je suis triste. Un câlin. Merci vécu. Deuxième ruse : bout rose "
        "vu, puis disparu, oreille coincée dans le panier. Elle s'arrête, "
        "lit l'éclat. Papa trouve. Un éclat de housse tient sur le tissu.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chambre, soir, housse, lit, panier, veilleuse.\n"
        "- Désir : retrouver le doudou rose, maintenant.\n"
        "- Objet : doudou rose, puis oreille coincée dans le panier.\n"
        "- Indice unique : éclat de housse, vu dès l'ouverture, payé "
        "sur le tissu. Pas éclat de doudou / couverture / panier / lit.\n"
        "- Urgence douce : elle fouille trop vite, trop bas.\n"
        "- Imprévu 1 : doudou absent, sourire parti, poitrine serrée, "
        "larmes.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le câlin.\n"
        "- Imprévu 2 (plus rusé) : doudou vu dans le panier, puis disparu, "
        "oreille coincée sous le linge.\n"
        "- Résolution : elle refuse de foncer, observe, écoute la chambre, "
        "retrouve l'éclat. Papa tire tout petit à petit.\n"
        "- Retour : oreille froissée, doudou contre le lit, éclat sur le "
        "tissu. Dénouement qui a failli : l'oreille partait plus loin.\n\n"
        "## Vécu\n\n"
        "Mila veut le doudou **maintenant**. Impatience, puis lit vide, "
        "sourire parti. Elle dit je suis triste, pleure, demande un câlin. "
        "Maman ouvre les bras. Papa se baisse, pose une question, ne "
        "récite pas la règle. Ils agissent : chercher sans se presser, "
        "tenir le bord, papa trouve dans le panier. Merci vécu. Fin : "
        "l'éclat du début tient sur le tissu.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Mila et le doudou rose (noyau dump). Relance : "
        "Que dit-elle ? expected triste.\n"
        "- Lieu du dump-meta (chambre, soir). Maman et papa. "
        "Mila = héros enfant-f. Dump doudou / panier / lit.\n"
        "- Ouverture inventée (tic du radiateur, soir), pas un "
        "gabarit v2, pas « Céline cherche son doudou », pas « L'histoire "
        "est finie », pas « La veilleuse dessine des lunes » en tête.\n"
        "- Indice unique : éclat de housse. BAN éclat de doudou / "
        "couverture / panier / lit / plaid / coussin / lampe / tapis. "
        "Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme/toute calme et "
        "`aujourd'hui` retirés. Strip « pleurer est permis » et "
        "« j'ai dit : je suis » du dump.\n"
        "- Leçon non dite : on la voit quand les yeux sont chauds, "
        "quand Mila dit je suis triste, quand elle pleure, quand elle "
        "demande un câlin. Pas « pleurer est permis ». Pas « le câlin "
        "aide ». Pas « j'ai dit : je suis ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Mila a les yeux chauds. Que dit-elle ? ». "
        "expected triste. 5 chunks, kinds inchangés. expected/accepted "
        "dump conservés. retry Céline → Mila (dit-elle). Hors Q : null.\n"
        "- example4 067 / 099 / 031 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N1.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers l'oreille coincée.\n"
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
