#!/usr/bin/env python3
"""ATOM-EMO.GES.002-08 — Le pont de Nina (F-NAR-019, N3, EMO.GES.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.002-08"
TITLE = "Le pont de Nina"
N3 = LIMITS["N3"]
CHARS = "Nina, papa, maman"
SETTING = (
    "salon puis cuisine, tabouret, cubes, voiture, "
    "soupe, pain, bois, casserole, sol"
)
INDICE = "éclat de tabouret"
FIL = (
    "La petite voiture tape le tabouret. Sur le bois, "
    "un éclat de tabouret luit. Nina veut un pont, maintenant. "
    "Le pont tombe. Poitrine trop vite. Sourire parti. "
    "Papa s'accroupit. Elle souffle, pause. Merci vécu. "
    "Deuxième ruse : la casserole glisse, bruit fort, "
    "le corps repart trop vite. Elle refuse de foncer. "
    "Un éclat de tabouret tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tapis|rideau|plaid|balançoire|balancoire|plinthe|marelle|"
    r"banc|cour|grille|bac|flaque|botte|bottes|limace|perron|"
    r"tiroir|fraisier|cuivre|buis|coussin|figue|robinet|planche|"
    r"émail|email|samare|bassine|entrée|entree|merle|miel|"
    r"piquet|cerceau|drap|savon|bol|feuille|pierre|commode|"
    r"lacet|sauge|chiffon|parquet|gond|portail|canapé|"
    r"canape|oiseau|toboggan|comptoir|torchon|chaise|farine|"
    r"nappe|cuillère|cuillere|saladier|couvercle|horloge|"
    r"sonnette|tasse|orange|lessive|vitre|carreau|laine|"
    r"lampe|citron|wagon|fraise|quille|gouttière|gouttiere|"
    r"crayon|buée|buee|croûte|croute|tableau|casier|moufle|"
    r"craie|cartable|pinceau|zeste|parapluie|pavé|pave|"
    r"bâche|bache|poire|volet|croissant|cloche|corbeille|"
    r"panier|dorure|carte|boule|galet|couloir|poussière|"
    r"poussiere|plaque|cheminée|cheminee|dalle|enveloppe|"
    r"émail|samare|cerceau|figue|lit|étagère|etagere|"
    r"rouleau|pupitre|plateau|assiette|coquillage|"
    r"cadre|livre|pot|zinc|rambarde|carotte|étal|etal|"
    r"romarin|lune|grain|miette|pin|sable|foin|paille|"
    r"pépin|pepin|pomme|lavande|pince|corde|caisse|"
    r"caillou|clé|cle|bec|promenade|réverbère|reverbere|"
    r"sac|ombre|écorce|ecorce|marches?)\b",
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
    "on peut souffler",
    "tu peux souffler",
    "il faut souffler",
    "souffle comme le vent",
    "souffle comme",
    "tu as soufflé",
    "tu as souffle",
    "tu as fait une pause",
    "fais une pause",
    "on souffle",
    "on fait une pause",
    "souffler, puis une pause",
    "souffler puis une pause",
    "on peut reprendre",
    "on reprend",
    "tu as pris ton temps",
    "tu as repris",
    "c'est le bon geste",
    "c est le bon geste",
    "tu te souviens",
    "même leçon",
    "ferdinand",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de cube",
    "éclat de tapis",
    "éclat de casserole",
    "éclat de chaise",
    "éclat de torchon",
    "éclat de farine",
    "éclat de nappe",
    "éclat de canapé",
    "éclat de canape",
    "éclat de coussin",
    "éclat de planche",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de tour",
    "éclat de lit",
    "éclat de comptoir",
    "éclat d'étagère",
    "éclat d etagere",
    "éclat de pot",
    "éclat de rouleau",
    "éclat de plinthe",
    "éclat de rideau",
    "éclat de plaid",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de marelle",
    "éclat de toboggan",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
    "trait de vitre",
    "pli de voile",
)

# N3 : profils raw.js (opening / clue / resolution / action / ending).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de tabouret",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_un_pont_maintenant; "
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
            "sous_texte=le_pont_tombe_que_fait_nina; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="souffle",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_souffle_elle_fait_une_pause; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de tabouret",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=casserole_glisse_corps_repart_elle_s_arrete; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de tabouret",
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
    "expected_answer": "souffler",
    "accepted_examples": "souffler | il souffle | pause | une pause | s'asseoir",
    "retry_prompt": "Il souffle. Il s'assoit. Que fait-il ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "voiture,cubes,soupe",
        [
            "narrateur|La petite voiture tape le tabouret.",
            "enfant-f|Toc, papa.",
            "papa|Elle a heurté le bois, Nina ?",
            "enfant-f|Oui, le tabouret.",
            "narrateur|Le bois du tabouret sent la soupe, un peu.",
            "enfant-f|Ça sent la soupe, maman.",
            "maman|Tu la sens, depuis le salon ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sur le bois, un éclat de tabouret luit.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Maman coupe le pain, dans la cuisine.",
            "maman|Le pain est tiède, sous les doigts.",
            "enfant-f|Je le sens d'ici.",
            "papa|La casserole chante un peu, Nina.",
            "enfant-f|Elle fait un petit bruit.",
            "narrateur|Le salon sent le bois et la soupe, ensemble.",
            "narrateur|Les cubes attendent au sol, lisses et froids.",
            "enfant-f|Ils sont froids, papa.",
            "papa|Tu les touches, les cubes ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina s'assoit près du tabouret, les genoux pliés.",
            "enfant-f|Je veux un pont, maintenant.",
            "papa|Un pont pour la voiture ?",
            "enfant-f|Oui, tout de suite.",
            "narrateur|En ce moment, Nina prend un cube.",
            "narrateur|Elle veut un pont, très long.",
            "enfant-f|La voiture va passer.",
            "papa|Tu poses les cubes, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina pose un cube trop vite.",
            "narrateur|Puis un autre, trop haut.",
            "enfant-f|Plus haut !",
            "narrateur|Le pont penche d'un coup, vers le sol.",
            "narrateur|Les cubes tombent près du tabouret.",
            "narrateur|Ça fait un bruit sec.",
            "enfant-f|Oh.",
            "narrateur|Nina reste surprise, les mains ouvertes.",
            "narrateur|Sa poitrine va trop vite.",
            "narrateur|Le sourire de Nina disparaît.",
            "enfant-f|C'est trop, papa.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois les cubes, Nina ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains sont chaudes, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Un éclat de tabouret tremble, près du sol.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Le pont tombe.",
            "narrateur|Que fait Nina ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "cubes",
        [
            "narrateur|Nina veut le pont, tout de suite.",
            "enfant-f|Je mets tout, maintenant !",
            "narrateur|Les cubes restent par terre, près du tabouret.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Trop vite.",
            "narrateur|Nina avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle, un moment.",
            "narrateur|Elle observe les cubes, un instant.",
            "narrateur|Elle écoute le salon, près du bois.",
            "enfant-f|Pouh.",
            "narrateur|Nina souffle une fois.",
            "narrateur|Elle souffle une deuxième fois.",
            "narrateur|Elle s'assoit près du tabouret.",
            "narrateur|Elle fait une pause.",
            "narrateur|Ses mains se posent sur ses genoux.",
            "narrateur|La poitrine ralentit un peu.",
            "papa|Tu restes un peu, Nina ?",
            "enfant-f|Oui, papa.",
            "papa|Merci, Nina.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le pain sent bon, depuis la cuisine.",
            "enfant-f|Il est tiède.",
            "narrateur|Nina reprend un cube, sans se presser.",
            "narrateur|Elle le pose sur un autre.",
            "papa|Tu le vois, le cube ?",
            "enfant-f|Oui, papa.",
            "maman|Il tient, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le pont a deux cubes, tout petits.",
            "enfant-f|Il tient !",
            "papa|Le pont est petit, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le ventre de Nina se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "narrateur|La voiture attend à côté, sans rouler.",
            "enfant-f|Elle passera après.",
            "maman|Nina, tu viens ?",
            "maman|La soupe est prête.",
            "papa|On y va, vers la cuisine ?",
            "enfant-f|Oui.",
            "narrateur|Nina glisse la main sur le bois du tabouret.",
            "enfant-f|Le petit point.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "cuisine,casserole",
        [
            "narrateur|Ils passent vers la cuisine.",
            "narrateur|La vapeur de soupe est chaude.",
            "enfant-f|Ça sent fort, maman.",
            "maman|Tu la sens, la vapeur ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le tabouret reste à la porte, vers le salon.",
            "narrateur|Une casserole glisse vers le bord.",
            "narrateur|Ça fait un bruit fort, près du feu.",
            "enfant-f|Elle glisse !",
            "narrateur|Nina avance trop vite, les mains ouvertes.",
            "narrateur|Sa poitrine repart trop vite.",
            "enfant-f|Oh.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe la casserole, un instant.",
            "narrateur|Elle écoute la cuisine, près du feu.",
            "narrateur|Sur le bois, un éclat de tabouret luit.",
            "enfant-f|Là, sur le bois.",
            "narrateur|Nina souffle une fois.",
            "narrateur|Elle attend, assise un moment.",
            "enfant-f|Pouh.",
            "papa|On tient le bord ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa pousse la casserole, sans se presser.",
            "maman|La soupe reste dans le fond, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina fait une pause, les mains sur les genoux.",
            "papa|Tu restes près de nous, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|La vapeur monte, plus lente.",
            "enfant-f|Elle est chaude.",
            "maman|Tes mains sont au chaud, Nina ?",
            "enfant-f|Un peu, maman.",
            "papa|La casserole est calme, Nina ?",
            "enfant-f|Oui, papa.",
            "maman|Un rayon passe sur le bois du tabouret.",
            "enfant-f|Il allume le bois.",
            "narrateur|Le tabouret tient à la porte, vers le salon.",
            "enfant-f|Le pont est là-bas.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "soupe",
        [
            "narrateur|Ils restent près de la soupe.",
            "maman|Tu t'assois, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina s'assoit près du tabouret.",
            "papa|Le petit pont, au salon, est petit ?",
            "enfant-f|Il tient, papa.",
            "narrateur|Le petit pont a failli rester en tas.",
            "enfant-f|Il a une trace de bois.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|La soupe est là, Nina.",
            "enfant-f|Elle sent bon.",
            "narrateur|Le pain est tiède, sous les doigts.",
            "enfant-f|Et la soupe, maman.",
            "maman|Oui, dans l'air.",
            "papa|La cuisine est calme, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un éclat de tabouret tient sur le bois.",
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
        for key in ("expected_answer", "accepted_examples", "retry_prompt"):
            if cid != "CHK_T0000_P0000_Q0001" and by[cid].get(key) is not None:
                raise SystemExit(f"{cid}: {key} devait rester null")
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
    if "souffle" not in blob:
        raise SystemExit(f"{SID}: manque souffle")
    if "pause" not in blob:
        raise SystemExit(f"{SID}: manque pause")
    if "sourire" not in blob:
        raise SystemExit(f"{SID}: manque sourire parti")
    if "accroupit" not in blob:
        raise SystemExit(f"{SID}: manque papa accroupi")
    if "poitrine" not in blob:
        raise SystemExit(f"{SID}: manque poitrine")
    if "envie" not in blob or "inquiétude" not in blob:
        raise SystemExit(f"{SID}: manque envie/inquiétude")
    if "casserole" not in blob:
        raise SystemExit(f"{SID}: manque casserole")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Nina = enfant-f)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    if "ferdinand" in blob:
        raise SystemExit(f"{SID}: Ferdinand hors D16")
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
        "on peut souffler",
        "tu peux souffler",
        "il faut souffler",
        "souffle comme le vent",
        "tu as soufflé",
        "tu as fait une pause",
        "souffler, puis une pause",
        "on peut reprendre",
        "tu as pris ton temps",
        "même leçon",
        "l'histoire est finie",
        "mission accomplie",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Le pont tombe. Que fait Nina ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "souffler":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "souffler | il souffle | pause | une pause | s'asseoir"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Il souffle. Il s'assoit. Que fait-il ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "souffle" in opening or "pause" in opening:
        raise SystemExit(f"{SID}: souffle/pause trop tôt (avant la question)")
    if "salon" not in blob:
        raise SystemExit(f"{SID}: manque salon")
    if "cuisine" not in blob:
        raise SystemExit(f"{SID}: manque cuisine")
    if "pont" not in blob:
        raise SystemExit(f"{SID}: manque pont")
    if "tabouret" not in blob:
        raise SystemExit(f"{SID}: manque tabouret")
    if "maintenant" not in blob:
        raise SystemExit(f"{SID}: manque maintenant")
    n_souffle = sum(
        1
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("narrateur|") and "souffle" in ln.lower()
        and c["chunk_id"] in ("CHK_T0000_P0000_C0001", "CHK_T0000_P0000_END")
    )
    if n_souffle < 2:
        raise SystemExit(f"{SID}: souffle vécu ×{n_souffle} (voulu ≥2)")
    for ban in (
        "éclat de cube",
        "éclat de tapis",
        "éclat de casserole",
        "éclat de chaise",
        "éclat de torchon",
        "éclat de farine",
        "éclat de canapé",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "ferdinand",
        " tapis",
        "canapé",
        "coussin",
        "torchon",
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
        raise SystemExit(f"{SID}: mots {nwords} hors 700–850")

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
        "- **Public :** N3 (≤16 mots/phrase), audio familial, voc 4–6 ans\n"
        "- **Leçon :** EMO.GES.002 — pont qui tombe, corps trop vite → "
        "souffler, faire une pause (vécue : Nina veut un pont maintenant, "
        "cubes tombent, poitrine trop vite, sourire parti, papa accroupi, "
        "elle souffle, s'assoit, pause ; 2e ruse cuisine : casserole "
        "glisse, bruit fort, le corps repart, elle refuse de foncer). "
        "JAMAIS dite dans le récit. Pas « on peut souffler ». Pas "
        "« tu peux souffler ». Pas « tu as fait une pause ».\n"
        "- **Personnages :** Nina, papa, maman. Dump Nina/papa/maman, "
        "troupe D16. Nina = enfant-f (veut le pont maintenant). Pas "
        "d'autre adulte. (002-05 a aussi Nina : chambre/lit ; ici "
        "salon puis cuisine, pont.) Zéro Ferdinand.\n"
        "- **Lieu :** salon puis cuisine, tabouret, cubes, voiture, "
        "soupe, pain, bois, casserole, sol. BAN tapis / canapé / "
        "coussin / torchon / farine comme indice. 2e temps cuisine "
        "conservé.\n"
        "- **Indice unique :** éclat de tabouret (luit à l'ouverture → "
        "tremble à la chute → luit quand la casserole glisse → tient "
        "sur le bois). BAN éclat de casserole / tapis / cube / chaise "
        "/ torchon.\n"
        "- **Question moteur :** « Le pont tombe. Que fait Nina ? » "
        "expected dump **souffler**. accepted dump `souffler | il "
        "souffle | pause | une pause | s'asseoir`. retry dump "
        "`Il souffle. Il s'assoit. Que fait-il ?` (pas de nom hors "
        "D16 à remapper). Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La petite voiture tape le tabouret. Sur le bois, un éclat "
        "de tabouret luit. Soupe, pain, cubes. Nina veut un pont "
        "**maintenant**. Le pont tombe. Poitrine trop vite. Sourire "
        "parti. Papa s'accroupit. Elle souffle, pause. Merci vécu. "
        "Deuxième ruse : casserole qui glisse, bruit fort. Elle "
        "s'arrête, lit l'éclat. Un éclat de tabouret tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon puis cuisine, tabouret, cubes, voiture, soupe, "
        "pain, bois, casserole. BAN tapis / canapé / torchon.\n"
        "- Désir : un pont pour la voiture, maintenant.\n"
        "- Objet : cubes, voiture, puis casserole qui glisse.\n"
        "- Indice unique : éclat de tabouret, vu dès l'ouverture, payé "
        "sur le bois. Pas éclat de casserole / tapis / cube.\n"
        "- Urgence douce : elle pose trop vite, trop haut.\n"
        "- Imprévu 1 : le pont tombe, poitrine trop vite, sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "la pause.\n"
        "- Imprévu 2 (plus rusé) : cuisine, casserole qui glisse, "
        "bruit fort, le corps repart trop vite.\n"
        "- Résolution : elle refuse de foncer, observe, écoute la "
        "cuisine, retrouve l'éclat, souffle, attend.\n"
        "- Retour : soupe, petit pont qui a failli rester en tas, "
        "éclat sur le bois.\n\n"
        "## Vécu\n\n"
        "Nina veut un pont **maintenant**. Impatience, puis cubes par "
        "terre, sourire parti. Elle souffle, s'assoit, les mains sur "
        "les genoux. Papa se baisse, pose une question, ne récite pas "
        "la règle. Ils agissent : un cube sans se presser, pont de "
        "deux. Merci vécu. Cuisine : la casserole glisse, elle refuse "
        "de foncer. Fin : l'éclat du début tient sur le bois. Le pont "
        "a failli rester en tas.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le pont de Nina (noyau dump). Relance dump : "
        "Que fait Nina ? expected souffler.\n"
        "- Lieu du dump (salon puis cuisine). Maman et papa. "
        "Nina = héros enfant-f. BAN tapis / canapé comme indice.\n"
        "- Ouverture inventée (voiture tape le tabouret), pas un "
        "gabarit v2, pas « Sur le toit, la pluie » du source, pas "
        "les cinq ouvertures du brief.\n"
        "- Indice unique : éclat de tabouret. BAN éclat de casserole "
        "/ tapis / cube / chaise / torchon. Pas tache/flèche/"
        "marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doucement » / « Bravo, Nina » slogan "
        "/ « L'histoire est finie » du dump.\n"
        "- Leçon non dite : on la voit quand le pont tombe, quand la "
        "poitrine va trop vite, quand Nina souffle, quand elle "
        "s'assoit, quand elle refuse de foncer. Pas « on peut "
        "souffler ». Pas « tu as fait une pause ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Le pont tombe. Que fait Nina ? ». "
        "expected souffler. 5 chunks, kinds inchangés. expected/"
        "accepted/retry dump conservés.\n"
        "- example4 053 / 085 / 017 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N3 raw.js.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers la casserole qui glisse.\n"
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
