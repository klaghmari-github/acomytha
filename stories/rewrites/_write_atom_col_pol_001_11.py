#!/usr/bin/env python3
"""ATOM-COL.POL.001-11 — Les poires de Chouchou (F-NAR-019, N3, COL.POL.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.POL.001-11"
TITLE = "Les poires de Chouchou"
N3 = LIMITS["N3"]
CHARS = "Chouchou, papa, maman"
SETTING = (
    "marché, sacs en toile au clou, pluie d'hier, goutte, rond, "
    "filet, poires jaunes, étal"
)
INDICE = "éclat de sac"
FIL = (
    "Les sacs en toile pendent à un clou. Ils sentent la pluie d'hier. "
    "Une goutte fait un rond. Sur un sac, un éclat de sac brille. "
    "Chouchou veut des poires maintenant. Elle avance trop vite : "
    "l'éclat glisse, la dame ne se tourne pas. Elle refuse de foncer, "
    "dit bonjour. Merci vécu. Une poire trop vite : le filet penche. "
    "Elle refuse, demande. Sur la toile, l'éclat de sac tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(cloche|corbeille|pavé|pave|zeste|parapluie|bâche|bache|"
    r"volet|croissant|réverbère|reverbere|pli|mie|poisson|page|"
    r"escargot|pompon|manteau|seau|carton|mousse|carotte|ballon|"
    r"lampion|moulinet)\b",
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
    "lise",
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
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "on aime écouter",
    "on aime ecouter",
    "tu as bien écouté",
    "tu as bien ecoute",
    "tu as bien fait",
    "bon travail",
    "tu as dit les mots",
    "les trois mots",
    "on dit bonjour",
    "tu as suivi",
    "éclat de poire",
    "éclat de cloche",
    "éclat de corbeille",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de bâche",
    "éclat de bache",
    "éclat de volet",
    "éclat de croissant",
    "éclat de réverbère",
    "éclat de reverbere",
    "éclat de citron",
    "éclat de pli",
    "éclat de mie",
    "éclat de poisson",
    "éclat de page",
    "éclat d'escargot",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de carotte",
    "éclat de tapis",
    "éclat de buée",
    "éclat de buee",
    "éclat de crayon",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de cartable",
    "éclat de pinceau",
    "éclat de casserole",
    "éclat de wagon",
    "éclat de nappe",
    "éclat de vitre",
    "éclat de tasse",
    "éclat de goutte",
    "éclat de laine",
    "éclat de grain",
    "éclat de liste",
    "éclat de sonnette",
    "éclat de ballon",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
    "grain de miette",
    "grain de sable",
    "marque fine",
    "minuscule symbole",
    "ombre en forme",
    "tache de couleur",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de sac",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_les_poires_maintenant; "
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
            "sous_texte=elle_dit_bonjour_en_parlant_a_la_dame; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="Bonjour",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_attend_puis_dit_bonjour; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="filet",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_sur_la_poire; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de sac",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_toile; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "bonjour",
    "accepted_examples": (
        "bonjour | s'il te plaît | merci | s'il te plait"
    ),
    "retry_prompt": "Elle dit bonjour. Que dit Chouchou ?",
    "engine_ok_text": "Oui, bonjour.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "goutte,cagettes,marche",
        [
            "narrateur|Un clou tient des sacs en toile, lourds d'eau.",
            "narrateur|Ils sentent la pluie d'hier.",
            "narrateur|Une goutte tombe du rebord.",
            "narrateur|Elle fait un petit rond dans la flaque.",
            "narrateur|Sur un sac, un éclat de sac brille.",
            "enfant-f|Il brille, papa !",
            "papa|C'est l'eau, sur la toile ?",
            "enfant-f|Oui, tout petit.",
            "narrateur|Chouchou connaît cette place, un peu.",
            "narrateur|Les cagettes claquent sur la pierre.",
            "narrateur|Une pêche roule, puis s'arrête.",
            "maman|Tu as entendu les cagettes ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Ça claque.",
            "papa|On va voir les poires ?",
            "enfant-f|Les jaunes, maintenant !",
            "narrateur|Le filet vide tape contre sa jambe.",
            "enfant-f|Il est léger.",
            "maman|On le remplit, tout à l'heure.",
            "enfant-f|Tout de suite !",
            "narrateur|Ça sent la menthe, près des herbes.",
            "enfant-f|Ça sent les pommes aussi.",
            "narrateur|En ce moment, Chouchou marche vers les poires.",
            "narrateur|La dame range des poires jaunes.",
            "narrateur|Elles sont rondes, avec des taches dorées.",
            "enfant-f|Celles-là, maman !",
            "papa|Tu les prends, Chouchou ?",
            "enfant-f|Oui, maintenant !",
            "narrateur|Chouchou avance le filet trop vite.",
            "narrateur|Les sacs se balancent au clou.",
            "narrateur|L'éclat de sac glisse sur la toile.",
            "enfant-f|Oh.",
            "narrateur|La dame ne se tourne pas.",
            "narrateur|Ses mains restent dans les poires.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Tu parles à la dame, Chouchou ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "enfant-f|Oui, papa.",
            "narrateur|Les mots se perdent près des poires.",
            "narrateur|Personne n'entend la fin.",
            "narrateur|Chouchou referme la bouche, un instant.",
            "narrateur|Le filet reste vide, un peu lourd.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Chouchou parle à la dame.",
            "narrateur|Que dit-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "marche,filet",
        [
            "narrateur|Chouchou avance le filet trop vite.",
            "enfant-f|Les poires, les jaunes, pour nous !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "narrateur|La dame ne prend pas le filet.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Chouchou refuse de foncer.",
            "narrateur|Elle recule le filet, un peu.",
            "papa|Le filet est vide, Chouchou ?",
            "narrateur|Papa reste à sa hauteur.",
            "maman|La flaque ronde est sous tes pieds.",
            "narrateur|Maman n'a pas fini non plus.",
            "narrateur|Chouchou attend que le silence arrive.",
            "narrateur|Sur la toile, l'éclat de sac brille.",
            "enfant-f|Il est là.",
            "enfant-f|Bonjour.",
            "papa|Bonjour.",
            "enfant-f|Des poires, s'il te plaît.",
            "enfant-f|Les jaunes, s'il te plaît.",
            "narrateur|La dame pose des poires dans le filet.",
            "narrateur|Le filet penche, un peu.",
            "enfant-f|Merci.",
            "papa|Merci, Chouchou.",
            "narrateur|Papa a entendu toute la phrase.",
            "maman|Tu tiens le filet des deux mains ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Elles sont fraîches.",
            "papa|Tu parles du rond, si tu veux ?",
            "enfant-f|La goutte a fait un rond.",
            "maman|On rentre, Chouchou ?",
            "enfant-f|Oui.",
            "narrateur|Une lumière jaune vient des poires.",
            "narrateur|L'odeur de menthe reste sur la place.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "marche,table",
        [
            "narrateur|Chouchou quitte la place avec papa et maman.",
            "narrateur|Une flaque brille, ronde, près de la pierre.",
            "narrateur|La menthe reste dans l'air.",
            "enfant-f|Le filet est lourd, papa.",
            "papa|Les poires sont dedans, oui.",
            "narrateur|À la maison, la table sent les poires.",
            "enfant-f|Je prends une poire, maintenant !",
            "narrateur|Chouchou avance la main trop vite.",
            "narrateur|Une poire roule vers le bord du filet.",
            "enfant-f|Oh.",
            "narrateur|Papa n'a pas fini sa phrase.",
            "papa|Le filet penche, Chouchou.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-f|Oh.",
            "narrateur|Chouchou refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Elle écoute la cuisine, un instant.",
            "narrateur|Elle pose la main, sans presser.",
            "enfant-f|S'il te plaît, une poire ?",
            "maman|Oui, une petite.",
            "enfant-f|Elle est fraîche, maman.",
            "papa|Tu restes un peu ?",
            "enfant-f|Oui, papa.",
            "maman|Le filet est près de l'évier.",
            "enfant-f|On le pose ?",
            "papa|Oui, sur le bois.",
            "narrateur|La poire sent le sucré.",
            "enfant-f|Elle colle aux doigts.",
            "maman|Comme la toile, oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "sac,cuisine",
        [
            "narrateur|Ils restent près de la table.",
            "narrateur|Maman accroche le sac en toile au clou.",
            "enfant-f|Comme au marché, papa.",
            "papa|Tu le vois, toi ?",
            "enfant-f|Oui, sur la toile.",
            "maman|On est bien, ici.",
            "narrateur|Chouchou glisse le doigt, sans se presser.",
            "enfant-f|On le sent, maman.",
            "maman|Tu le sens sur tes doigts ?",
            "enfant-f|Oui, il colle.",
            "papa|Le filet est rentré lourd.",
            "enfant-f|Oui, avec les poires.",
            "narrateur|L'odeur de menthe reste dans la cuisine.",
            "enfant-f|Il est là, maman.",
            "maman|Oui, sur la toile.",
            "narrateur|L'éclat de sac tient sur la toile.",
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
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
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
    if "s'il te plaît" not in blob:
        raise SystemExit(f"{SID}: manque s'il te plaît vécu")
    if "lise" in blob:
        raise SystemExit(f"{SID}: Lise restée")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Chouchou = enfant-f)")
    if "que dit-il" in blob:
        raise SystemExit(f"{SID}: Que dit-il ? (fille)")
    if "éclat de poire" in blob:
        raise SystemExit(f"{SID}: éclat de poire (BAN POL.001-05)")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f") for r in roles):
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
    q = by["CHK_T0000_P0000_Q0001"]
    if q.get("retry_prompt") and "lise" in str(q["retry_prompt"]).lower():
        raise SystemExit(f"{SID}: Lise dans retry")
    if "que dit-elle" not in q["text"].lower():
        raise SystemExit(f"{SID}: question moteur pas au féminin")
    if q.get("expected_answer") != "bonjour":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if "chouchou" not in str(q.get("retry_prompt") or "").lower():
        raise SystemExit(f"{SID}: retry sans Chouchou")
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
        "- **Public :** N3 (5–6 ans), audio familial, ≤16 mots/phrase\n"
        "- **Leçon :** COL.POL.001 — bonjour (puis s'il te plaît / merci), "
        "vécue : veut des poires maintenant ; première idée échoue ; "
        "refuse de foncer ; dit bonjour. Jamais dite comme règle.\n"
        "- **Personnages :** Chouchou, papa, maman. Troupe D16. Dump Lise "
        "→ INTERDIT. `enfant-f`. Papa ajouté (dump : Lise, maman). "
        "Adultes parlants = papa/maman. La dame = label, narrée, sans "
        "réplique.\n"
        "- **Lieu :** marché, sacs en toile au clou, pluie d'hier, goutte, "
        "rond, filet, poires jaunes. ≠ POL.001-05 La poire de Sarah "
        "(jardin / éclat de poire / une poire). Ici plusieurs poires, "
        "sacs toile. Pas éclat de poire.\n"
        "- **Indice unique :** éclat de sac (toile dès l'ouverture → glisse "
        "quand elle fonce → brille au silence → tient sur la toile). "
        "Pas éclat de poire (BAN POL.001-05).\n"
        "- **Question moteur :** « Chouchou parle à la dame. Que dit-elle ? » "
        "(dump : Que dit-il ?). expected **bonjour**. retry Lise→Chouchou.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un clou tient des sacs en toile, lourds d'eau. Pluie d'hier, "
        "goutte, petit rond dans la flaque. Sur un sac, un éclat de sac "
        "brille. Chouchou veut des poires jaunes **maintenant**. Elle "
        "avance trop vite : les sacs se balancent, l'éclat glisse, la "
        "dame ne se tourne pas. Sourire parti. Papa s'accroupit. Les mots "
        "se perdent. Elle refuse de foncer, attend le silence, dit "
        "bonjour, puis s'il te plaît. Des poires dans le filet. Merci "
        "vécu. À la maison, une poire trop vite : le filet penche. Elle "
        "refuse, demande. Maman accroche le sac au clou. Sur la toile, "
        "l'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : marché, sacs en toile au clou, pluie d'hier, goutte, "
        "rond, cagettes, pêche, menthe, filet, poires jaunes. ≠ 001-05 "
        "jardin/poirier/éclat de poire.\n"
        "- Désir : des poires jaunes, maintenant, plusieurs, dans le filet.\n"
        "- Objet : filet, poires jaunes, sacs en toile, clou, goutte, rond.\n"
        "- Indice unique : éclat de sac, vu dès l'ouverture, payé au "
        "silence du stand et sur la toile au retour.\n"
        "- Urgence douce : le filet vide, les poires sous les mains de "
        "la dame.\n"
        "- Imprévu 1 : tout de suite, filet trop vite, éclat qui glisse, "
        "dame qui ne se tourne pas, mots perdus.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après la phrase "
        "entière près de l'étal.\n"
        "- Imprévu 2 (plus rusé) : à la maison, une poire maintenant ; "
        "le filet penche, les voix se mélangent.\n"
        "- Résolution : elle refuse de foncer, attend, dit bonjour, "
        "demande une poire.\n"
        "- Retour : sac au clou, doigt sans se presser, l'éclat tient "
        "sur la toile.\n\n"
        "## Vécu\n\n"
        "Leçon COL.POL.001 (bonjour pour ouvrir, s'il te plaît pour les "
        "poires, merci pour le filet) greffée, jamais annoncée. La "
        "première idée (tendre d'un coup) échoue. Le choix de Chouchou "
        "change l'action. Un « en ce moment ». Un merci vécu. Adulte + "
        "question. Troupe D16 : Chouchou, papa, maman. N3.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Les poires de Chouchou (noyau dump).\n"
        "- Héros Chouchou, fille. Dump Lise → INTERDIT. `enfant-f`. "
        "Retry Lise→Chouchou.\n"
        "- Papa ajouté (dump : Lise, maman). La dame = label, sans "
        "réplique, non nommée.\n"
        "- Question moteur : « Chouchou parle à la dame. Que dit-elle ? » "
        "(dump : Que dit-il ?). Fond **bonjour** conservé.\n"
        "- Ouverture inventée (clou, sacs lourds d'eau), pas un gabarit "
        "v2, pas « va à l'école », pas le ballon F-NAR-015.\n"
        "- Indice unique : éclat de sac. Pas cloche/corbeille/pavé/zeste/"
        "parapluie/bâche/volet/croissant/réverbère, pas éclat de poire.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés.\n"
        "- Interdit « bon travail / histoire finie / tu as dit les mots / "
        "les trois mots / on dit bonjour ».\n"
        "- 5 chunks, kinds inchangés. example4 : 075, 007, 039.\n"
        f"- {nwords} mots. N3 ≤ 16. TTS : notes, ssml, xai, piper par "
        "chunk.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
