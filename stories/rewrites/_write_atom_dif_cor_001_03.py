#!/usr/bin/env python3
"""ATOM-DIF.COR.001-03 — Les bateaux de pomme de Nino (F-NAR-019, N3)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.001-03"
TITLE = "Les bateaux de pomme"
N3 = LIMITS["N3"]
CHARS = "Nino, Mila, papa, maman"
SETTING = (
    "pierre du jardin, tarte qui refroidit, bassine sur la marche"
)
INDICE = "éclat de bassine"
FIL = (
    "Une odeur de beurre monte de la pierre du jardin. Sur le bord, "
    "un éclat de bassine luit. Nino veut le bateau de pomme jusqu'au "
    "bord d'en face, maintenant. Il pousse trop fort depuis la table : "
    "la pomme s'arrête au milieu. Mila n'atteint pas. Sourire parti. "
    "Papa s'accroupit. Il refuse de foncer, pose la bassine sur la "
    "marche, souffle avec Mila. Merci vécu. Un second bateau tape le "
    "bord. Il attend. L'éclat de bassine tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(dalle|zinc|escargot|flaque|plaid|cerisier|fraisier|fraise|"
    r"carton|tilleul|ballon|pavé|pave|zeste|parapluie|bâche|bache|"
    r"plaque|galet|cube|farine|panier|dorure|poire|sac|cloche|"
    r"corbeille|croissant|réverbère|reverbere|volet|tom |léo|leo|"
    r"victorino|ferdinand|escargot)\b",
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
    "tu as bien fait",
    "tailles différentes",
    "tailles differentes",
    "on peut jouer ensemble",
    "vous jouez ensemble",
    "vous avez des tailles",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de pierre",
    "éclat de dalle",
    "éclat de samare",
    "éclat de cerceau",
    "éclat de grille",
    "éclat de plaque",
    "éclat de carte",
    "éclat de boule",
    "éclat de volet",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de bâche",
    "éclat de bache",
    "éclat de seau",
    "éclat de pompon",
    "éclat de carton",
    "éclat de mousse",
    "éclat de laine",
    "éclat de tasse",
    "éclat de crayon",
    "éclat de wagon",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de pinceau",
    "éclat de ballon",
    "éclat de manteau",
    "éclat de marche",
    "éclat de vitre",
    "éclat de grain",
    "éclat de liste",
    "éclat de farine",
    "lune d'étain",
    "lune d'etain",
    "grain de pomme",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de bassine",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_bateau_jusqu_au_bord_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Mila",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=plus_grand_plus_petite_ils_jouent_ensemble; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="marche",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=bassine_sur_la_marche_ils_soufflent; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="pomme",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_pousser_trop_vite_du_haut; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de bassine",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bord; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer ensemble",
    "accepted_examples": (
        "jouer ensemble | ensemble | ils jouent | on joue | souffler ensemble"
    ),
    "retry_prompt": "Ils jouent ensemble. Que font Nino et Mila ?",
    "engine_ok_text": "Oui, ils jouent ensemble.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "tarte,pierre,bassine",
        [
            "narrateur|Une odeur de beurre monte de la pierre.",
            "narrateur|La pierre du jardin est froide, sous le plat.",
            "narrateur|La tarte aux pommes fume, tiède.",
            "enfant-m|Elle sent le beurre, papa.",
            "papa|Tu l'as vue, sur la pierre ?",
            "enfant-m|Oui, papa.",
            "maman|Elle va refroidir, Nino.",
            "narrateur|Une pomme tombée attend dans l'herbe.",
            "narrateur|Une feuille y est collée, un peu sucrée.",
            "narrateur|L'herbe pique un peu, sous les pieds.",
            "narrateur|Une bassine d'eau attend sur la marche.",
            "narrateur|Le soleil tape le bord, étroit.",
            "narrateur|Un rond blanc danse dans l'eau.",
            "narrateur|Sur le bord, un éclat de bassine luit.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, sur le bord ?",
            "enfant-m|Oui, il brille.",
            "papa|C'est le bord de la bassine.",
            "enfant-m|Je veux un bateau, maintenant !",
            "maman|Un bateau de pomme ?",
            "enfant-m|Oui, jusqu'au bord, là-bas.",
            "papa|Jusqu'au bord d'en face ?",
            "enfant-m|Oui, tout de suite !",
            "narrateur|En ce moment, Nino prend la pomme.",
            "narrateur|Elle est collante, un peu sucrée.",
            "narrateur|Il plante la feuille, en voile.",
            "narrateur|Maman pose la bassine sur la table.",
            "narrateur|La table est haute, près de l'arbre.",
            "narrateur|Mila arrive sous l'arbre.",
            "narrateur|Elle lève les mains vers l'eau.",
            "enfant-m|Tu viens ?",
            "copine|Oui.",
            "narrateur|Mila se dresse sur les pointes.",
            "narrateur|Ses doigts n'atteignent pas l'eau.",
            "copine|Je n'arrive pas.",
            "enfant-m|Moi, je pousse !",
            "narrateur|Nino pousse trop fort, trop loin.",
            "narrateur|La pomme tourne, puis s'arrête au milieu.",
            "enfant-m|Elle n'arrive pas.",
            "narrateur|L'éclat de bassine saute près de l'eau.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu veux le bateau jusqu'au bord ?",
            "enfant-m|Oui, papa.",
            "maman|Avec Mila, Nino ?",
            "enfant-m|Oui.",
            "papa|Elle n'atteint pas la table ?",
            "enfant-m|Non.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino est plus grand.",
            "narrateur|Mila est plus petite.",
            "narrateur|Que font-ils ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "eau,pomme",
        [
            "narrateur|Nino veut pousser, d'un coup.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe l'eau, un instant.",
            "narrateur|Il écoute le jardin, près de la pierre.",
            "narrateur|Sur le bord, l'éclat de bassine revient.",
            "enfant-m|On pose la bassine, plus bas.",
            "papa|Sur la marche ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa pose la bassine sur la marche.",
            "narrateur|L'eau tremble, puis s'arrête.",
            "narrateur|Mila touche l'eau, du bout des doigts.",
            "copine|Elle est froide.",
            "enfant-m|On souffle ?",
            "copine|Oui.",
            "narrateur|Ils soufflent du même côté de l'eau.",
            "narrateur|La pomme glisse, lente, vers le bord.",
            "enfant-m|Elle arrive !",
            "copine|Je la tiens.",
            "narrateur|Mila rattrape la pomme, près d'elle.",
            "narrateur|Nino reste de son côté, plus haut.",
            "papa|Merci, Nino.",
            "narrateur|Papa a regardé jusqu'au bout.",
            "narrateur|Le ventre de Nino se desserre.",
            "enfant-m|Un autre bateau ?",
            "maman|La tarte attend un peu.",
            "enfant-m|Le bateau d'abord.",
            "maman|Tes pieds sont sur la marche ?",
            "enfant-m|Oui, maman.",
            "papa|Et Mila ?",
            "copine|Moi aussi.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "feuille,eau",
        [
            "narrateur|Nino prépare une autre pomme.",
            "narrateur|Une feuille verte tient, collée.",
            "enfant-m|Celle-là, plus loin !",
            "narrateur|Il pousse trop vite, du haut de la marche.",
            "narrateur|L'eau saute contre le bord.",
            "narrateur|La pomme tape le bord, puis revient.",
            "enfant-m|Oh.",
            "narrateur|Mila retire les mains.",
            "copine|Non.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Nino veut rattraper, d'un coup.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Ses épaules se serrent un peu.",
            "narrateur|Ça tape, dans sa poitrine.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il regarde le bord, il écoute l'eau.",
            "narrateur|Un oiseau passe, loin.",
            "enfant-m|On souffle, Mila ?",
            "narrateur|Mila ne dit rien.",
            "narrateur|Elle garde les mains sur ses genoux.",
            "enfant-m|D'accord.",
            "narrateur|Nino attend.",
            "copine|Plus tard.",
            "enfant-m|Oui.",
            "narrateur|La pomme se cale, sans tourner.",
            "narrateur|Mila avance un doigt.",
            "narrateur|Elle pousse près d'elle, puis s'arrête.",
            "enfant-m|D'accord.",
            "narrateur|Ils soufflent, chacun de son bord.",
            "narrateur|Les deux pommes se croisent.",
            "copine|La mienne a tourné !",
            "enfant-m|La mienne aussi.",
            "maman|La tarte ne fume plus.",
            "enfant-m|Elle est prête ?",
            "maman|Presque.",
            "papa|Tes mains sont dans l'eau ?",
            "enfant-m|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "tarte",
        [
            "narrateur|Ils restent près de la marche.",
            "narrateur|Les voiles de feuilles restent mouillées.",
            "enfant-m|L'éclat est là, papa.",
            "papa|Tu le vois sur le bord ?",
            "enfant-m|Oui, papa.",
            "maman|On est bien, ici.",
            "narrateur|La tarte sent le beurre, plus légère.",
            "enfant-m|Mes bateaux ont flotté.",
            "maman|Jusqu'au bord, Nino.",
            "enfant-m|Oui, maman.",
            "narrateur|Nino pose la joue près du bord.",
            "narrateur|Le bord est tiède, un peu.",
            "enfant-m|C'est tiède.",
            "papa|Tu le sens sur tes joues ?",
            "enfant-m|Oui, il est tiède.",
            "narrateur|Une feuille porte une goutte d'eau.",
            "narrateur|Dehors, le jardin s'endort.",
            "narrateur|L'éclat de bassine tient sur le bord.",
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
    if "pierre du jardin" not in blob:
        raise SystemExit(f"{SID}: manque pierre du jardin")
    if "tarte" not in blob:
        raise SystemExit(f"{SID}: manque tarte")
    if "bassine" not in blob or "marche" not in blob:
        raise SystemExit(f"{SID}: manque bassine/marche")
    if "éclat de pierre" in blob:
        raise SystemExit(f"{SID}: éclat de pierre (BAN 002-02)")
    if "grain de pomme" in blob:
        raise SystemExit(f"{SID}: grain de pomme (BAN)")
    if "dalle" in blob:
        raise SystemExit(f"{SID}: dalle (BES.002-06)")
    if "tailles différentes" in blob or "tailles differentes" in blob:
        raise SystemExit(f"{SID}: leçon dite")
    if "ferdinand" in blob or "victorino" in blob:
        raise SystemExit(f"{SID}: prénom dump")
    if re.search(r"\btom\b", blob):
        raise SystemExit(f"{SID}: Tom interdit")
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
        raise SystemExit(f"{SID}: Mila absente")
    q_text = by["CHK_T0000_P0000_Q0001"]["text"]
    if q_text != "Nino est plus grand. Mila est plus petite. Que font-ils ?":
        raise SystemExit(f"{SID}: question labels changés: {q_text}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "jouer ensemble":
        raise SystemExit(f"{SID}: expected_answer ≠ jouer ensemble")
    c1 = by["CHK_T0000_P0000_C0001"]["script"].lower()
    if "marche" not in c1 or "souffle" not in c1:
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
        "- **Leçon :** DIF.COR.001 — tailles différentes, jouer ensemble "
        "(vécue : Nino pousse trop fort depuis la table ; le bateau "
        "s'arrête au milieu ; Mila n'atteint pas ; il pose la bassine "
        "sur la marche ; ils soufflent, chacun de son bord)\n"
        "- **Personnages :** Nino, Mila, papa, maman. Troupe D16. Mila "
        "= copine (rythme lent, limites, silence). Papa ajouté. Adultes "
        "parlants = papa/maman.\n"
        "- **Lieu :** pierre du jardin, tarte qui refroidit, bassine sur "
        "la marche. ≠ 001-01 bol de fraises / plaid / cerisier. ≠ 001-02 "
        "carton du marché / tilleul / banc. ≠ BES.002-06 bateaux de "
        "papier / dalle / flaque.\n"
        "- **Indice unique :** éclat de bassine (bord dès l'ouverture → "
        "saute près de l'eau → revient sur le bord → tient sur le bord). "
        "Pas éclat de pierre (BAN 002-02). Pas grain de pomme. Pas éclat "
        "de dalle / samare / cerceau.\n"
        "- **Question moteur :** Nino est plus grand. Mila est plus "
        "petite. Que font-ils ? → jouer ensemble.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une odeur de beurre monte de la pierre du jardin. La tarte fume, "
        "tiède. Sur le bord, un éclat de bassine luit. Nino veut le "
        "bateau de pomme jusqu'au bord d'en face **maintenant**. La "
        "bassine est sur la table. Mila se dresse : ses doigts "
        "n'atteignent pas. Il pousse trop fort : la pomme s'arrête au "
        "milieu. Sourire parti, épaules basses. Papa s'accroupit. Il "
        "refuse de foncer, pose la bassine sur la marche, souffle avec "
        "Mila. Merci vécu. Un second bateau tape le bord. Il attend le "
        "silence. Ils soufflent, chacun de son bord. L'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : pierre du jardin, tarte au beurre, herbe, bassine, "
        "rond blanc dans l'eau, table haute, marche.\n"
        "- Désir : le bateau de pomme jusqu'au bord d'en face, maintenant.\n"
        "- Objet : pomme, feuille-voile, bassine, tarte, pierre.\n"
        "- Indice unique : éclat de bassine, vu dès l'ouverture, payé "
        "sur le bord.\n"
        "- Urgence douce : la tarte refroidit, le bateau doit arriver.\n"
        "- Imprévu 1 : il pousse trop fort depuis la table ; le bateau "
        "n'atteint pas l'endroit promis ; Mila n'atteint pas l'eau.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : il pousse trop vite du haut de la "
        "marche ; la pomme tape le bord ; Mila dit non, puis se tait.\n"
        "- Résolution : il refuse de foncer, attend, souffle de son "
        "bord ; elle pousse près d'elle.\n"
        "- Retour : voiles mouillées, tarte au beurre, éclat sur le "
        "bord.\n\n"
        "## Vécu\n\n"
        "Nino veut le bateau **maintenant**, jusqu'au bord. Impatience "
        "(poussée trop forte, trop vite), puis sourire qui disparaît, "
        "épaules qui tombent. Papa s'accroupit, pose une question, ne "
        "récite pas la règle. Nino agit : bassine sur la marche, souffle "
        "avec Mila, attend son silence. Merci vécu après le regard "
        "jusqu'au bout. Fin : l'éclat du début tient sur le bord.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau : Les bateaux de pomme. Lieu du dump : pierre du "
        "jardin, tarte qui refroidit, bassine sur la marche. Relance : "
        "Nino est plus grand. Mila est plus petite. Que font-ils ? "
        "expected jouer ensemble.\n"
        "- Ouverture inventée (odeur de beurre, pierre froide, rond "
        "blanc), pas un gabarit v2, pas « joue au salon ».\n"
        "- Indice unique : éclat de bassine. Pas éclat de pierre "
        "(BES.002-02), pas grain de pomme, pas dalle (BES.002-06), pas "
        "merle, miel, marque fine.\n"
        "- Distinct 001-01 (fraises/plaid) et 001-02 (carton/tilleul).\n"
        "- Tics encore/déjà/tout doux/tout calme/tout lent/tout bas et "
        "`aujourd'hui,` retirés.\n"
        "- Leçon non dite : pas « tailles différentes », pas « on peut "
        "jouer ensemble ». Vécue dans le geste (marche, souffle, chacun "
        "de son bord).\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. Papa "
        "ajouté. Mila = copine, rythme lent.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive vers le second bateau.\n"
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
