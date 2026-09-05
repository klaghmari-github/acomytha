#!/usr/bin/env python3
"""ATOM-EMO.GES.001-07 — Nino dit stop et s'éloigne (F-NAR-019, N1, EMO.GES.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.001-07"
TITLE = "Nino dit stop et s'éloigne"
N1 = LIMITS["N1"]
CHARS = "Nino, Aniss, papa, maman"
SETTING = (
    "cour de récréation, marelle, craie, cases, "
    "poussière, soleil, caillou"
)
INDICE = "éclat de marelle"
FIL = (
    "Un trait rose s'étire sur le sol chaud. Sur une case, "
    "un éclat de marelle luit. Nino veut jouer, maintenant. "
    "Aniss serre trop. Sourire parti. Papa s'accroupit. "
    "Stop, recule. Merci vécu. Deuxième ruse : le caillou "
    "glisse. Il dit stop, recule. Un éclat de marelle tient "
    "sur la case."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(cour|grille|banc|seau|linge|café|cafe|"
    r"balançoire|balancoire|toboggan|plaid|cadre|livre|"
    r"merle|miel|maîtresse|maitresse|"
    r"bateau|cerceau|piquet|gond|flaque|"
    r"canapé|canape|carotte|pupitre|plateau|étal|etal)\b",
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
    "c'est permis",
    "on s'éloigne",
    "on s eloigne",
    "il peut s'éloigner",
    "il peut s eloigner",
    "on va vers un adulte",
    "vers un adulte",
    "tu as dit stop",
    "j'ai dit stop",
    "j'ai dit",
    "je me suis éloigné",
    "je me suis eloigne",
    "tu t'es éloigné",
    "tu t es eloigne",
    "il s'éloigne",
    "il s eloigne",
    "s'éloigner vers",
    "florian",
    "chouchou",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de cour",
    "éclat de grille",
    "éclat de banc",
    "éclat de cadre",
    "éclat de livre",
    "éclat de plaid",
    "éclat de toboggan",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de seau",
    "éclat de linge",
    "éclat de craie",
    "éclat de caillou",
    "éclat de case",
    "éclat de soleil",
    "éclat de poussière",
    "éclat de poussiere",
)

# N1 : mêmes champs que DIF.PAR.002-05 (voix lente).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat de marelle",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
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
            "sous_texte=c_est_trop_pour_nino_que_dit_il; "
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
            "emotion=gêne puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_dit_stop_il_recule; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de marelle",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=le_caillou_glisse_aniss_serre_pour_aider; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de marelle",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_case; "
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
            "narrateur|Un trait rose s'étire sur le sol chaud.",
            "enfant-m|Il est long, papa.",
            "papa|Tu le vois, le trait ?",
            "enfant-m|Oui, papa.",
            "narrateur|La poussière de craie pique le nez.",
            "maman|J'ai tracé la marelle.",
            "enfant-m|Elle est grande, maman.",
            "narrateur|Maman pose le caillou plat.",
            "narrateur|Le caillou est chaud, un peu lisse.",
            "enfant-m|Il est chaud.",
            "papa|Tu le touches, Nino ?",
            "enfant-m|Oui, du doigt.",
            "narrateur|Sur une case, un éclat de marelle luit.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, sur la case ?",
            "enfant-m|Oui, un petit point.",
            "papa|Le soleil le touche.",
            "narrateur|Un rayon glisse sur la craie.",
            "narrateur|La craie gratte un peu.",
            "enfant-m|Elle gratte, papa.",
            "maman|Tu t'accroupis, Nino ?",
            "enfant-m|Un peu.",
            "narrateur|Une miette de craie dort au bord.",
            "enfant-m|Une miette, maman.",
            "maman|Elle est sèche ?",
            "enfant-m|Oui.",
            "narrateur|Le vent soulève un peu de poussière.",
            "enfant-m|Ça chatouille, papa.",
            "papa|Tu l'entends, le vent ?",
            "enfant-m|Oui, il souffle.",
            "narrateur|Une feuille tourne près des cases.",
            "enfant-m|Elle tourne.",
            "maman|C'est le vent.",
            "narrateur|Les pieds de Nino tapent le sol.",
            "enfant-m|Mes pieds, papa.",
            "papa|Tu es bien prêt, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le sol de la marelle est rêche.",
            "enfant-m|Il est rêche.",
            "narrateur|Aniss arrive près des cases.",
            "narrateur|Ses baskets tapent la poussière.",
            "copain|La marelle.",
            "enfant-m|Tu viens, Aniss ?",
            "copain|Oui.",
            "narrateur|Maman tend le caillou.",
            "narrateur|Il tient chaud dans la paume.",
            "enfant-m|Je veux jouer, maintenant !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|En ce moment, Nino lève le caillou.",
            "maman|Tu le lances, Nino ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le caillou tape la première case.",
            "copain|Moi aussi !",
            "narrateur|Aniss ouvre les bras tout grand.",
            "narrateur|Il serre Nino très fort.",
            "enfant-m|Oh.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se serre.",
            "narrateur|L'envie et l'inquiétude se heurtent.",
            "narrateur|Ses épaules montent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Aniss, Nino ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains sont chaudes, Nino ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de marelle tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|C'est trop pour Nino.",
            "narrateur|Que dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Nino veut jouer, tout de suite.",
            "enfant-m|Je lance, maintenant !",
            "narrateur|Il avance trop près d'Aniss.",
            "narrateur|Les bras d'Aniss se referment.",
            "copain|Viens.",
            "narrateur|Nino ne peut plus souffler.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Nino recule d'abord les épaules.",
            "enfant-m|Stop.",
            "narrateur|Il recule d'un pas.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le caillou, un instant.",
            "narrateur|Il écoute le vent sur la craie.",
            "papa|Tu veux jouer, Nino ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Un peu loin.",
            "copain|Loin ?",
            "enfant-m|Oui.",
            "papa|Merci, Nino.",
            "narrateur|Papa a vu les deux, près des cases.",
            "maman|Le caillou colle un peu, sous les doigts.",
            "enfant-m|Il est chaud.",
            "narrateur|Aniss lâche les bras.",
            "narrateur|Nino pose le caillou.",
            "copain|Case.",
            "enfant-m|Case, oui.",
            "papa|Tu la vois, la case ?",
            "enfant-m|Oui, papa.",
            "maman|Tu sautes, Nino ?",
            "copain|J'y vais.",
            "narrateur|Ils sautent la première case.",
            "narrateur|Ça fait un petit bruit.",
            "enfant-m|Hop.",
            "copain|Hop.",
            "papa|C'est loin, la case ?",
            "narrateur|Aniss ouvre la bouche.",
            "copain|Loin.",
            "narrateur|Nino garde un pas d'air.",
            "copain|Un pas.",
            "enfant-m|Un pas, oui.",
            "narrateur|Le ventre de Nino se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près de la marelle ?",
            "enfant-m|Oui.",
            "maman|Tes pieds sont au chaud ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Maman pose la craie rose.",
            "narrateur|La craie est un peu ronde.",
            "enfant-m|La case, maintenant !",
            "narrateur|Aniss lève le caillou.",
            "copain|Loin.",
            "narrateur|Le caillou glisse sur une case.",
            "enfant-m|Il glisse, maintenant !",
            "narrateur|Aniss attrape les épaules de Nino.",
            "narrateur|Il serre trop, pour aider.",
            "enfant-m|Oh.",
            "narrateur|Nino avance les bras, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "enfant-m|Stop.",
            "narrateur|Il recule d'un pas, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe la case, un instant.",
            "narrateur|Il écoute le vent sur la craie.",
            "narrateur|Sur la case, un éclat de marelle luit.",
            "enfant-m|Là, sur la case.",
            "enfant-m|Tu sautes, Aniss ?",
            "narrateur|Aniss ne serre plus.",
            "narrateur|Il souffle, puis recule.",
            "copain|Il glisse.",
            "papa|On pose le caillou ?",
            "enfant-m|Oui, papa.",
            "narrateur|Nino pousse le caillou.",
            "narrateur|Aniss le pose, sans se presser.",
            "enfant-m|Il tient.",
            "copain|Il tient.",
            "papa|La craie est chaude, Aniss ?",
            "copain|Un peu.",
            "maman|Tu sautes, Nino ?",
            "enfant-m|Oui, maman.",
            "narrateur|Ils sautent près de la marelle.",
            "narrateur|La poussière chatouille les chevilles.",
            "enfant-m|C'est plus facile.",
            "papa|Le vent est calme ?",
            "enfant-m|Oui, papa.",
            "maman|Un rayon passe sur la case.",
            "enfant-m|Il allume la marelle.",
            "narrateur|Aniss souffle sur la craie.",
            "copain|La craie.",
            "enfant-m|La craie, oui.",
            "narrateur|La craie laisse un trait.",
            "enfant-m|Un trait rose.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la marelle.",
            "narrateur|Maman essuie un peu de poussière.",
            "enfant-m|Le caillou a sauté, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, près des cases.",
            "maman|On est bien, ici.",
            "narrateur|Nino tapote le caillou du doigt.",
            "enfant-m|Il a une trace de craie.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|Le caillou est resté, Nino.",
            "enfant-m|Oui, avec Aniss.",
            "copain|Le caillou est resté.",
            "narrateur|Ça sent la craie, un peu tiède.",
            "enfant-m|Et le soleil, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|Le caillou reste sur une case.",
            "narrateur|Un éclat de marelle tient sur la case.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-m", "copain"):
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
        elif e.lower() in body.lower():
            # Stop vs stop
            idx = body.lower().find(e.lower())
            if idx >= 0:
                orig = body[idx:idx + len(e)]
                body = body[:idx] + f'<emphasis level="moderate">{orig}</emphasis>' + body[idx + len(e):]
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict) -> str:
    body = text
    emp = m.get("emphasis")
    if emp and emp in body:
        body = body.replace(emp, f"<emphasis>{emp}</emphasis>", 1)
    elif emp:
        idx = body.lower().find(emp.lower())
        if idx >= 0:
            orig = body[idx:idx + len(emp)]
            body = body[:idx] + f"<emphasis>{orig}</emphasis>" + body[idx + len(emp):]
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
    if m.get("emphasis") and m["emphasis"].lower() not in text.lower():
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
        raise SystemExit(f"{SID}: manque stop vécu")
    if "recule d'un pas" not in blob and "recule d un pas" not in blob:
        raise SystemExit(f"{SID}: manque recule d'un pas")
    if "s'accroupit" not in blob and "s accroupit" not in blob:
        raise SystemExit(f"{SID}: manque papa accroupi")
    if "poitrine" not in blob:
        raise SystemExit(f"{SID}: manque poitrine")
    if "sourire" not in blob:
        raise SystemExit(f"{SID}: manque sourire")
    if "maintenant" not in blob:
        raise SystemExit(f"{SID}: manque maintenant")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Nino = enfant-m, Aniss = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Aniss absent (copain)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m", "copain") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "copain" for r in roles):
        raise SystemExit(f"{SID}: copain absent")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "dire stop, c'est permis",
        "dire stop c'est permis",
        "on s'éloigne",
        "on va vers un adulte",
        "tu as dit stop",
        "j'ai dit stop",
        "je me suis éloigné",
        "il peut s'éloigner",
        "c'est permis",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "C'est trop pour Nino. Que dit-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") is not None:
        raise SystemExit(f"{SID}: expected_answer doit rester null")
    if q.get("accepted_examples") is not None:
        raise SystemExit(f"{SID}: accepted_examples doit rester null")
    if q.get("retry_prompt") is not None:
        raise SystemExit(f"{SID}: retry_prompt doit rester null")
    if "marelle" not in blob:
        raise SystemExit(f"{SID}: manque marelle")
    if "craie" not in blob:
        raise SystemExit(f"{SID}: manque craie")
    if "caillou" not in blob:
        raise SystemExit(f"{SID}: manque caillou")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: manque Aniss")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: manque Nino")
    enfant_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("enfant-m|")
    ).lower()
    if enfant_txt.count("stop") < 2:
        raise SystemExit(f"{SID}: Nino doit dire stop (1 + 2e ruse)")
    if "serre" not in blob:
        raise SystemExit(f"{SID}: manque serre")
    if "glisse" not in blob:
        raise SystemExit(f"{SID}: manque 2e ruse (glisse)")
    for ban in (
        "éclat de cour",
        "éclat de grille",
        "éclat de banc",
        "éclat de cadre",
        "éclat de livre",
        "éclat de plaid",
        "éclat de toboggan",
        "éclat de balançoire",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "florian",
        "chouchou",
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
        "- **Leçon :** EMO.GES.001 — trop fort → stop, reculer "
        "(vécue : Aniss serre trop, poitrine coincée, Nino dit stop, "
        "recule d'un pas ; 2e ruse : le caillou glisse, Aniss serre "
        "pour aider, Nino dit stop, recule). JAMAIS dite. Pas "
        "« dire stop, c'est permis ». Pas « on s'éloigne ».\n"
        "- **Personnages :** Nino, Aniss, papa, maman. Dump "
        "Florian/Chouchou/papa → D16 Nino = enfant-m (veut jouer "
        "maintenant). Aniss = copain (serre trop, Viens, Loin). "
        "Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** cour de récréation, marelle, craie, cases, "
        "poussière, soleil, caillou. ≠ 001-01 balançoire. ≠ 001-03 "
        "toboggan. ≠ 001-04 plaid. ≠ 001-05 livre. ≠ 001-06 cadre. "
        "BAN cour/grille/banc dans le texte.\n"
        "- **Indice unique :** éclat de marelle (luit à l'ouverture → "
        "tremble au câlin trop fort → luit quand le caillou glisse → "
        "tient sur la case). BAN éclat de cour / grille / banc / "
        "cadre / livre / plaid / toboggan / balançoire.\n"
        "- **Question moteur :** « C'est trop pour Nino. Que dit-il ? » "
        "expected / accepted / retry **null** (consigne). Non "
        "récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un trait rose s'étire sur le sol chaud. Sur une case, un "
        "éclat de marelle luit. Craie, caillou, cases. Nino veut "
        "jouer **maintenant**. Aniss ouvre les bras, serre trop. "
        "Sourire parti. Papa s'accroupit. Stop, recule. Merci vécu. "
        "Deuxième ruse : le caillou glisse. Aniss serre pour aider. "
        "Nino dit stop, recule, lit l'éclat. Un éclat de marelle "
        "tient sur la case.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cour de récréation, marelle, craie, cases, "
        "poussière, soleil, caillou. ≠ 001-01 balançoire. ≠ 001-03 "
        "toboggan. ≠ 001-04 plaid.\n"
        "- Désir : jouer à la marelle, maintenant.\n"
        "- Objet : caillou plat, puis craie rose.\n"
        "- Indice unique : éclat de marelle, vu dès l'ouverture, payé "
        "sur la case. Pas éclat de cour / grille / banc / cadre / "
        "livre / plaid / toboggan / balançoire.\n"
        "- Urgence douce : le caillou est lancé, Aniss veut y aller "
        "aussi, tout de suite.\n"
        "- Imprévu 1 : Aniss serre trop, poitrine coincée, sourire "
        "parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« un peu loin ».\n"
        "- Imprévu 2 (plus rusé) : craie rose, le caillou glisse, "
        "Aniss attrape les épaules pour aider.\n"
        "- Résolution : Nino dit stop, recule d'un pas, observe, "
        "écoute le vent, retrouve l'éclat, Aniss dit « il glisse ».\n"
        "- Retour : trait rose, caillou sur une case, éclat qui tient.\n\n"
        "## Vécu\n\n"
        "Nino veut jouer **maintenant**. Impatience, puis bras trop "
        "forts, sourire parti. Aniss est chaleureux, trop près "
        "(Viens, Loin, souffle). Papa se baisse, pose une question, "
        "ne récite pas la règle. Ils agissent : stop, un pas, cases "
        "sautées avec de l'air. Merci vécu. Fin : l'éclat du début "
        "tient sur la case.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Nino dit stop et s'éloigne (noyau « dit stop et "
        "s'éloigne », prénom D16). Relance : Que dit-il ? expected "
        "null.\n"
        "- Lieu : cour de récréation (marelle). Maman et papa. "
        "Aniss = copain. Nino = héros. Dump Florian/Chouchou du "
        "json remappé : Florian→Nino, Chouchou→Aniss.\n"
        "- Ouverture inventée (trait rose sur le sol chaud), pas un "
        "gabarit v2, pas « Les pierres de la cour sont froides » "
        "du dump.\n"
        "- Indice unique : éclat de marelle (récré). BAN éclat de "
        "cour / grille / banc (BAN) / cadre (001-06) / livre "
        "(001-05) / plaid (001-04) / toboggan (001-03) / "
        "balançoire (001-01). Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « encore » / « tout doucement » du dump.\n"
        "- Leçon non dite : on la voit quand Aniss serre, quand "
        "Nino dit stop, quand il recule, quand le caillou glisse. "
        "Pas « dire stop, c'est permis ». Pas « on s'éloigne ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « C'est trop pour Nino. Que dit-il ? ». "
        "expected/accepted/retry null. 5 chunks, kinds inchangés.\n"
        "- example4 044 / 076 / 008 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_par_002_05.py`, profiles N1 lents.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers le caillou qui glisse.\n"
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
