#!/usr/bin/env python3
"""ATOM-EMO.GES.002-05 — Nina souffle et fait une pause (F-NAR-019, N1, EMO.GES.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.002-05"
TITLE = "Nina souffle et fait une pause"
N1 = LIMITS["N1"]
CHARS = "Nina, papa, maman"
SETTING = (
    "chambre, lit, bois, barre, pied du lit, cubes, "
    "coton, rayon, point de lumière"
)
INDICE = "éclat de lit"
FIL = (
    "Un rayon tiède dort sur le bois. Sur le pied du lit, "
    "un éclat de lit luit. Nina veut empiler, maintenant. "
    "Cubes tombent, poitrine trop vite, sourire parti. Maman "
    "s'accroupit. Elle souffle. Pause. Merci vécu. Les cubes "
    "glissent sur le coton du lit. Elle refuse d'empiler, "
    "souffle, pause. Un éclat de lit tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(flaque|grille|botte|bottes|limace|perron|tiroir|"
    r"fraisier|cuivre|buis|coussin|figue|robinet|planche|"
    r"émail|email|samare|bassine|entrée|entree|merle|miel|"
    r"piquet|cerceau|drap|savon|bol|feuille|pierre|commode|"
    r"lacet|tapis|sauge|chiffon|parquet|canapé|canape|plaid|"
    r"balançoire|balancoire|rideau|toboggan|radiateur|"
    r"chaussette|chaussettes|bateau|cabane|seau|chatouille|"
    r"chatouilles|gond|portail|ballon|cour|oiseau|doudou|"
    r"sieste|comptoir|rouleau|tour|pot)\b",
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
    "on peut faire une pause",
    "tu as soufflé",
    "tu as souffle",
    "tu as fait une pause",
    "j'ai soufflé",
    "j'ai souffle",
    "j'ai fait une pause",
    "souffler, puis",
    "puis une pause",
    "bravo",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de pierre",
    "éclat de cerceau",
    "éclat de flaque",
    "éclat de grille",
    "éclat de cour",
    "éclat de botte",
    "éclat de portail",
    "éclat de feuille",
    "éclat de piquet",
    "éclat de commode",
    "éclat de lacet",
    "éclat de tapis",
    "éclat de sauge",
    "éclat de chiffon",
    "éclat de parquet",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de pin",
    "éclat de pomme",
    "éclat de sève",
    "éclat de seve",
    "éclat de limace",
    "éclat de perron",
    "éclat de chaise",
    "éclat de tiroir",
    "éclat de fraisier",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de casserole",
    "éclat de citron",
    "éclat de coquille",
    "éclat de zeste",
    "éclat de coussin",
    "éclat de figue",
    "éclat de robinet",
    "éclat de planche",
    "éclat d'émail",
    "éclat d'email",
    "éclat de samare",
    "éclat de bassine",
    "éclat de nappe",
    "éclat de farine",
    "éclat de bol",
    "éclat de tablier",
    "éclat de biscuit",
    "éclat de toit",
    "éclat de volet",
    "éclat de pavé",
    "éclat de pave",
    "éclat de parapluie",
    "éclat de bâche",
    "éclat de bache",
    "éclat de poire",
    "éclat de seau",
    "éclat de pompon",
    "éclat de carotte",
    "éclat de carton",
    "éclat de mousse",
    "éclat de laine",
    "éclat de tasse",
    "éclat de crayon",
    "éclat de cartable",
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
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de couloir",
    "éclat de plaque",
    "éclat de dalle",
    "éclat de couvercle",
    "éclat de thermos",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de caillou",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat de lessive",
    "éclat de carreau",
    "éclat de coton",
    "éclat de gravier",
    "éclat de gilet",
    "éclat de lunettes",
    "éclat de résine",
    "éclat de resine",
    "éclat de canapé",
    "éclat de canape",
    "éclat de plaid",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de rideau",
    "éclat de toboggan",
    "éclat de gond",
    "éclat de page",
    "éclat de lampe",
    "éclat de table",
    "éclat de cube",
    "éclat de cubes",
    "éclat de tour",
    "éclat de comptoir",
    "éclat de pot",
    "éclat de rouleau",
    "éclat de bois",
    "éclat de barre",
    "éclat de doudou",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

# N1 : mêmes champs que DIF.ENE.001-09 / emo_ges_001_05 (voix, tempos plus lents).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat de lit",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis gêne; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_empiler_maintenant; "
            "tempo=posé puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=104, speed=0.80, piper=1.36, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=780,
        sentence=360, energy="focused", contour="rising", noise=0.30,
        emphasis="vite",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_corps_va_vite_que_fait_elle; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=122, speed=0.88, piper=1.24, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=620,
        sentence=310, energy="bright", contour="falling", noise=0.33,
        emphasis="cubes",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_pose_plus_bas_ils_tiennent; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de lit",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=les_cubes_glissent_sur_le_coton; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de lit",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
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
        "cubes",
        [
            "narrateur|Un rayon tiède dort sur le bois.",
            "enfant-f|Il est chaud, papa.",
            "papa|Tu le vois, le rayon ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ça sent le coton, un peu sec.",
            "maman|Tu le sens, le coton ?",
            "enfant-f|Oui, maman.",
            "narrateur|Une barre du lit tinte.",
            "enfant-f|Elle sonne, maman.",
            "maman|Le lit est là, sous le rayon.",
            "enfant-f|Je le vois.",
            "narrateur|Papa tapote le pied du lit.",
            "narrateur|Toc, toc, sur le bois.",
            "papa|Tu entends le bois, Nina ?",
            "enfant-f|Oui, il sonne.",
            "narrateur|Maman pose la main près du bois.",
            "narrateur|Le bois est lisse, un peu tiède.",
            "narrateur|Sur le bois, un éclat de lit luit.",
            "enfant-f|Il luit, papa.",
            "papa|Tu le vois, sur le bois ?",
            "enfant-f|Oui, un petit point.",
            "maman|La lumière le touche.",
            "narrateur|Un rayon glisse le long du lit.",
            "narrateur|Nina connaît cette chambre.",
            "enfant-f|Le point est nouveau.",
            "maman|Tu t'assois près du lit ?",
            "enfant-f|Un peu.",
            "narrateur|Un cube bleu brille près du bois.",
            "enfant-f|Il est bleu.",
            "papa|Les cubes sont là, tu vois ?",
            "enfant-f|Oui, papa.",
            "narrateur|En ce moment, Nina prend un cube.",
            "enfant-f|Je veux empiler, maintenant !",
            "papa|Tout de suite ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le cube est lisse, un peu froid.",
            "maman|Tu poses un cube ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina pose un cube trop vite.",
            "narrateur|Puis un autre, trop haut.",
            "narrateur|La pile penche.",
            "enfant-f|Elle monte !",
            "narrateur|Les cubes tombent.",
            "narrateur|Ça fait un bruit sec.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, ça va trop vite.",
            "narrateur|L'envie et la peur se heurtent.",
            "narrateur|Ses épaules montent un peu.",
            "narrateur|Maman s'accroupit à la même hauteur.",
            "maman|Tu vois les cubes, Nina ?",
            "enfant-f|Oui, maman.",
            "papa|Ta poitrine va vite, Nina ?",
            "enfant-f|Un peu, papa.",
            "enfant-f|C'est trop.",
            "narrateur|Nina souffle vers ses mains.",
            "enfant-f|Fouu.",
            "narrateur|Elle fait une pause, près du lit.",
            "narrateur|L'éclat de lit tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Le corps de Nina va vite.",
            "narrateur|Que fait-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Nina pose un cube sur le bois.",
            "enfant-f|Un, maman.",
            "narrateur|Elle pose un autre, plus bas.",
            "papa|Tu veux la pile avec moi ?",
            "enfant-f|Oui, chacun un cube.",
            "narrateur|Papa ne dit rien, d'abord.",
            "papa|Je tiens le mien.",
            "enfant-f|Moi aussi.",
            "papa|Merci, Nina.",
            "narrateur|Papa a vu les deux, près du lit.",
            "maman|Le bois colle un peu, sous les doigts.",
            "enfant-f|Il est lisse.",
            "narrateur|Ils essuient le cube du plat de la main.",
            "narrateur|Nina tient son cube, plus bas.",
            "enfant-f|Il tient !",
            "papa|Tu le vois, le bleu ?",
            "enfant-f|Oui, papa.",
            "maman|Au milieu, Nina ?",
            "enfant-f|J'y vais.",
            "narrateur|Nina pousse le cube, sans se presser.",
            "narrateur|Papa suit le bois des yeux.",
            "narrateur|La pile danse une fois.",
            "enfant-f|Un.",
            "papa|Deux.",
            "narrateur|Le ventre de Nina se desserre.",
            "narrateur|Les épaules descendent un peu.",
            "maman|On reste près du lit ?",
            "enfant-f|Oui.",
            "papa|Tes mains sont au chaud ?",
            "enfant-f|Un peu, papa.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "cubes",
        [
            "narrateur|Maman pousse les cubes vers le lit.",
            "narrateur|La pile est un peu haute.",
            "enfant-f|Les cubes, maintenant !",
            "narrateur|Nina avance trop, tout de suite.",
            "narrateur|Elle monte les cubes sur le lit.",
            "enfant-f|Plus haut !",
            "narrateur|Le coton est mou, sous les cubes.",
            "enfant-f|Ils partent !",
            "narrateur|Les cubes glissent vers le bord.",
            "narrateur|Nina avance les mains, trop vite.",
            "narrateur|La pile s'effondre sur le coton.",
            "enfant-f|Oh.",
            "narrateur|Nina refuse d'empiler, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le lit, un instant.",
            "narrateur|Elle écoute le bois du lit.",
            "narrateur|Sur le bois, un éclat de lit luit.",
            "enfant-f|Là, sur le bois.",
            "narrateur|Nina souffle vers le bois.",
            "enfant-f|Fouu.",
            "narrateur|Elle fait une pause, sur le bois.",
            "enfant-f|Tu tends le cube, papa ?",
            "narrateur|Papa ne dit rien.",
            "narrateur|Il souffle, puis tend le cube.",
            "papa|Oui.",
            "maman|On arrête la pile ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le bois sent le coton tiède.",
            "narrateur|Les cubes sont là, un peu au bord.",
            "narrateur|Nina les pose près de papa.",
            "narrateur|Papa les rend, sans presser.",
            "enfant-f|Clic.",
            "papa|Clic.",
            "maman|Le cube est bien posé ?",
            "enfant-f|Oui, maman.",
            "papa|Le bois est lisse, Nina ?",
            "enfant-f|Un peu.",
            "narrateur|Ils se passent un cube, près d'eux.",
            "narrateur|Le bois est lisse, sous les genoux.",
            "enfant-f|C'est plus facile.",
            "maman|Le rayon est calme ?",
            "enfant-f|Oui, maman.",
            "papa|Un rayon passe sur le bois.",
            "enfant-f|Il allume le point.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du lit.",
            "narrateur|Maman lisse un coin de coton.",
            "enfant-f|Les cubes ont glissé, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-f|Oui, près du lit.",
            "maman|On est bien, ici.",
            "narrateur|Nina tapote le bois du doigt.",
            "enfant-f|Il a une trace de doigt.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|Le lit est resté, Nina.",
            "enfant-f|Oui, avec les cubes.",
            "maman|Les cubes sont restés.",
            "narrateur|Ça sent le coton, un peu tiède.",
            "enfant-f|Et le bois, papa.",
            "papa|Oui, dans l'air.",
            "narrateur|Le lit reste sous le rayon.",
            "narrateur|Un éclat de lit tient sur le bois.",
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
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Nina = enfant-f)")
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
    if any(r not in ("narrateur", "papa", "maman", "enfant-f") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "enfant-f" for r in roles):
        raise SystemExit(f"{SID}: enfant-f absent")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on peut souffler",
        "on peut faire une pause",
        "tu as soufflé",
        "tu as fait une pause",
        "j'ai soufflé",
        "j'ai fait une pause",
        "bravo",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Le corps de Nina va vite. Que fait-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") is not None:
        raise SystemExit(f"{SID}: expected_answer doit rester null")
    if q.get("accepted_examples") is not None:
        raise SystemExit(f"{SID}: accepted_examples doit rester null")
    if q.get("retry_prompt") is not None:
        raise SystemExit(f"{SID}: retry_prompt doit rester null")
    if "souffle" not in blob:
        raise SystemExit(f"{SID}: manque souffle vécu")
    if "pause" not in blob:
        raise SystemExit(f"{SID}: manque pause vécue")
    if "cube" not in blob:
        raise SystemExit(f"{SID}: manque cubes")
    if "chambre" not in blob:
        raise SystemExit(f"{SID}: manque chambre")
    if "lit" not in blob:
        raise SystemExit(f"{SID}: manque lit")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: manque Nina")
    for ban in (
        "éclat de cube",
        "éclat de cubes",
        "éclat de tapis",
        "éclat de tour",
        "éclat de comptoir",
        "éclat de pot",
        "éclat de rouleau",
        "éclat de bois",
        "éclat de barre",
        "éclat de coton",
        "éclat de rideau",
        "tapis",
        "rideau",
        "savon",
        "oiseau",
        "doudou",
        "sieste",
        "tout doux",
        "tout calme",
        "gaëlle",
        "gaelle",
        "nino",
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
        "- **Leçon :** EMO.GES.002 — corps trop vite → souffler, pause "
        "(vécue : cubes tombent, poitrine trop vite, sourire parti, "
        "Fouu, pause près du lit, puis cubes sur le coton, Fouu, "
        "pause sur le bois). JAMAIS dite dans le récit. Pas « on peut "
        "souffler ». Pas « on peut faire une pause ». Pas « tu as "
        "soufflé / j'ai fait une pause ».\n"
        "- **Personnages :** Nina, papa, maman. Dump Gaëlle/Nino/maman "
        "→ D16 Nina = enfant-f (veut empiler maintenant). Troupe D16. "
        "Pas de copain. Pas de maîtresse.\n"
        "- **Lieu :** chambre, lit, bois, barre, pied du lit, cubes, "
        "coton, rayon. ≠ 002-01 tour. ≠ 002-02 comptoir. ≠ 002-03 pot. "
        "≠ 002-04 rouleau. PAS tapis / rideau / doudou / sieste.\n"
        "- **Indice unique :** éclat de lit (luit à l'ouverture → "
        "tremble à la chute → luit quand les cubes glissent → tient "
        "sur le bois). BAN éclat de cube / tapis / tour / comptoir / "
        "pot / rouleau / bois / barre / coton.\n"
        "- **Question moteur :** « Le corps de Nina va vite. Que "
        "fait-elle ? » expected / accepted / retry **null** (consigne). "
        "Non récitée comme consigne dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un rayon tiède dort sur le bois. Toc toc sur le pied du lit. "
        "Sur le bois, un éclat de lit luit. Coton sec, barre qui tinte. "
        "Nina veut empiler **maintenant**. Cubes trop vite, trop haut. "
        "Sourire parti. Maman s'accroupit. Fouu. Pause. Ils tiennent "
        "plus bas. Merci vécu. Deuxième ruse : cubes sur le coton du "
        "lit, ça glisse. Elle refuse d'empiler, souffle, pause. Un "
        "éclat de lit tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chambre, lit, bois, barre, cubes, coton, rayon. ≠ "
        "002-01 tour. ≠ 002-02 comptoir. ≠ 002-03 pot. ≠ 002-04 "
        "rouleau.\n"
        "- Désir : empiler les cubes, maintenant.\n"
        "- Objet : cubes près du bois, puis cubes sur le coton du lit.\n"
        "- Indice unique : éclat de lit, vu dès l'ouverture, payé "
        "sur le bois. Pas éclat de cube / tapis / tour / comptoir / "
        "pot / rouleau.\n"
        "- Urgence douce : elle pose trop vite, trop haut, la pile "
        "penche.\n"
        "- Imprévu 1 : cubes tombent, bruit sec, poitrine trop vite.\n"
        "- Cue : maman à la même hauteur. Fouu. Pause. Un merci "
        "vécu, après « chacun un cube ».\n"
        "- Imprévu 2 (plus rusé) : cubes sur le lit, coton mou, ça "
        "glisse vers le bord.\n"
        "- Résolution : elle refuse d'empiler, observe, écoute le "
        "bois, retrouve l'éclat, papa tend le cube.\n"
        "- Retour : clic tout près, lit sous le rayon, éclat sur "
        "le bois.\n\n"
        "## Vécu\n\n"
        "Nina veut empiler **maintenant**. Impatience, puis chute, "
        "sourire parti. Papa pose avec elle, plus bas. Maman se "
        "baisse, pose une question, ne récite pas la règle. Ils "
        "agissent : souffle vers les mains, pause près du lit, cube "
        "plus bas, puis souffle vers le bois quand le coton trahit. "
        "Merci vécu. Fin : l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Nina souffle et fait une pause (noyau dump "
        "« souffle et fait une pause » + prénom D16). Relance : Que "
        "fait-elle ? expected null.\n"
        "- Lieu du dump-meta (chambre, cubes). Maman et papa. Nina = "
        "héroïne. Pas Nino. Pas Gaëlle.\n"
        "- Ouverture inventée (rayon sur le bois, coton, barre), pas "
        "un gabarit v2, pas sieste/rideau/oiseau/savon/tapis du "
        "source, pas « Gaëlle joue dans sa chambre ».\n"
        "- Indice unique : éclat de lit (chambre, pied du lit). BAN "
        "éclat de cube / tapis / tour / comptoir / pot / rouleau / "
        "bois / barre / coton. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « encore » du dump.\n"
        "- Leçon non dite : on la voit quand les cubes tombent, "
        "quand la poitrine va trop vite, quand elle souffle, quand "
        "elle fait une pause, quand la pile tient. Pas « on peut "
        "souffler ». Pas « tu as soufflé / j'ai fait une pause ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Le corps de Nina va vite. Que "
        "fait-elle ? ». expected/accepted/retry null. 5 chunks, "
        "kinds inchangés.\n"
        "- example4 050 / 082 / 014 (manière volée, gabarit non "
        "collé). Voix : `_write_atom_emo_ges_001_05.py`, profiles N1.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers les cubes qui glissent.\n"
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
