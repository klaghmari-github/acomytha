#!/usr/bin/env python3
"""ATOM-EMO.LEX.001-05 — Sarah et le dessin du soleil (F-NAR-019, N3, EMO.LEX.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.001-05"
TITLE = "Sarah et le dessin du soleil"
N3 = LIMITS["N3"]
CHARS = "Sarah, papa, maman"
SETTING = (
    "salon, fin d'après-midi, tapis, poussière, crayons, "
    "feuille, vitre, pince, gomme, fenêtre, table basse"
)
INDICE = "éclat de gomme"
FIL = (
    "La laine du tapis sent le soleil. Près de la feuille, "
    "un éclat de gomme luit. Sarah veut montrer le soleil "
    "à maman, maintenant. Maman n'est pas rentrée. Le crayon "
    "jaune casse. Sourire parti. Papa s'accroupit. Elle attend, "
    "puis montre : je suis contente. Merci vécu. Deuxième ruse : "
    "la feuille se plie à la vitre. Elle refuse de foncer. "
    "Un éclat de gomme tient sur le papier."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(merle|miel|treille|moule|tuteur|saladier|comptoir|"
    r"rouleau|étagère|etagere|torchon|tabouret|tableau|cadre|"
    r"livre|plaid|balançoire|balancoire|rideau|toboggan|"
    r"grand-père|grand-pere|jardinier|maîtresse|maitresse)\b",
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
    "tu as nommé",
    "c'est de la joie",
    "c est de la joie",
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
    "tu as partagé",
    "tu as partage",
    "tu partages ta joie",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de treille",
    "éclat de moule",
    "éclat de tuteur",
    "éclat de saladier",
    "éclat de crayon",
    "éclat de pince",
    "éclat de vitre",
    "éclat de poussière",
    "éclat de poussiere",
    "éclat de tapis",
    "éclat de tableau",
    "éclat de cadre",
    "éclat de livre",
    "éclat de tour",
    "éclat de comptoir",
    "éclat de pot",
    "éclat de rouleau",
    "éclat de lit",
    "éclat d'étagère",
    "éclat d'etagere",
    "éclat de torchon",
    "éclat de tabouret",
    "éclat de cube",
    "éclat de plaid",
    "éclat de rideau",
    "éclat de canapé",
    "éclat de canape",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de gomme",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis inquiétude; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_montrer_le_soleil_maintenant; "
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
            "sous_texte=sarah_sourit_la_feuille_chaude_que_dit_elle; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="feuille",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_attend_elle_montre_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de gomme",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=la_feuille_se_plie_elle_refuse_de_foncer; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de gomme",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_papier; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "contente",
    "accepted_examples": "contente | je suis contente | joie",
    "retry_prompt": "Sarah sourit. Que dit-elle ?",
    "engine_ok_text": "Oui, contente.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "crayon",
        [
            "narrateur|La laine du tapis sent le soleil.",
            "enfant-f|Ça sent la laine, papa.",
            "papa|Tu la sens, la laine chaude ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah connaît ce salon, ses recoins.",
            "narrateur|Cette fin d'après-midi, un coin brille autrement.",
            "narrateur|La poussière danse près de la table basse.",
            "enfant-f|Elle danse, papa.",
            "papa|Tu la vois, près des crayons ?",
            "enfant-f|Oui.",
            "narrateur|La boîte en fer est froide, un peu cabossée.",
            "enfant-f|Elle claque.",
            "narrateur|Sarah ouvre la boîte près des genoux.",
            "narrateur|Les crayons roulent, un petit bruit.",
            "papa|Sarah, tu as choisi une feuille ?",
            "enfant-f|La grande, blanche.",
            "enfant-f|C'est pour maman.",
            "papa|Maman n'est pas rentrée.",
            "enfant-f|Je lui fais un soleil.",
            "narrateur|Près de la feuille, un éclat de gomme luit.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un grain blanc.",
            "narrateur|Papa coud un bouton, près de la fenêtre.",
            "narrateur|Dehors, un vélo passe, très loin.",
            "enfant-f|Maman revient ?",
            "papa|Bientôt.",
            "narrateur|En ce moment, Sarah s'assoit au bas du canapé.",
            "narrateur|Elle pose la feuille sur le tapis.",
            "narrateur|Le crayon jaune fait un bruit sec.",
            "enfant-f|Un soleil rond !",
            "narrateur|Des rayons partent, puis une petite maison.",
            "narrateur|Une porte, deux fenêtres.",
            "enfant-f|C'est notre maison.",
            "papa|Tu as de la place, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah appuie trop fort, trop vite.",
            "narrateur|Le crayon jaune casse, net.",
            "enfant-f|Oh.",
            "papa|Il en reste un bout.",
            "narrateur|La mine tombe sur le tapis.",
            "enfant-f|Maman va voir le trou ?",
            "papa|Elle verra la maison.",
            "narrateur|Sarah veut finir, tout de suite.",
            "enfant-f|Je montre, maintenant !",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois le bout, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|L'éclat de gomme tremble, puis tient.",
            "narrateur|Sarah finit le toit avec le bout.",
            "enfant-f|Un rayon manque.",
            "papa|La maison est là.",
            "narrateur|La porte clique, dans le couloir.",
            "narrateur|Maman pose son sac.",
            "maman|Je rentre.",
            "maman|Ça sent les crayons.",
            "enfant-f|Attends.",
            "narrateur|Sarah attend que maman s'assoie.",
            "narrateur|Ses joues sont chaudes.",
            "narrateur|Elle tend la feuille, sans bousculer.",
            "enfant-f|C'est notre maison.",
            "enfant-f|Je suis contente.",
            "maman|Le soleil est très jaune.",
            "papa|On le met où ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Sarah sourit, la feuille encore chaude.",
            "maman|Que dit-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Maman tient la feuille par les bords.",
            "narrateur|Elle ne plie pas le soleil.",
            "enfant-f|Le vrai soleil est à la fenêtre.",
            "maman|On va le voir ensemble ?",
            "narrateur|Ils se lèvent.",
            "narrateur|Le sac de maman reste près de la porte.",
            "enfant-f|Je le mets, maintenant !",
            "narrateur|Sarah avance trop vite vers la vitre.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|La pince !",
            "narrateur|Sarah avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe la feuille, un instant.",
            "narrateur|Elle écoute le salon.",
            "papa|Tu restes un peu, Sarah ?",
            "enfant-f|Oui, papa.",
            "papa|Merci, Sarah.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|La feuille est tiède, sous les doigts.",
            "enfant-f|Elle est chaude.",
            "papa|J'apporte la pince à linge ?",
            "enfant-f|Oui.",
            "narrateur|Papa prend une pince sur le radiateur.",
            "narrateur|La pince est un peu tiède.",
            "enfant-f|Comme le rayon.",
            "maman|Tes mains sont au chaud, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le ventre de Sarah se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On va près de la vitre ?",
            "enfant-f|Oui.",
            "papa|On marche sans se presser ?",
            "enfant-f|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "clic",
        [
            "narrateur|Ils collent le dessin contre la vitre.",
            "narrateur|La pince tient le coin.",
            "enfant-f|Il garde la fenêtre.",
            "narrateur|Sarah pousse trop vite, tout de suite.",
            "narrateur|La feuille se plie, net.",
            "enfant-f|Elle plie !",
            "narrateur|Un coin se recroqueville contre la vitre.",
            "narrateur|Sarah avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Sarah refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe la feuille, un instant.",
            "narrateur|Elle écoute le salon, près de la vitre.",
            "narrateur|Sur le papier, un éclat de gomme luit.",
            "enfant-f|Là, sur le papier.",
            "narrateur|Sarah lisse le pli, sans se presser.",
            "papa|On tient le coin ?",
            "enfant-f|Oui, papa.",
            "narrateur|La pince reprend le bord.",
            "narrateur|La feuille se déplie.",
            "enfant-f|Poumf.",
            "maman|Le soleil est à sa place, Sarah ?",
            "enfant-f|Oui, maman.",
            "papa|Dehors, le vrai soleil est plus pâle.",
            "enfant-f|Le mien est plus rond.",
            "maman|Le tien attendait, sur le tapis.",
            "papa|Le crayon cassé reste dans la boîte.",
            "narrateur|Sarah range les autres crayons, un par un.",
            "narrateur|Le jaune cassé rentre le dernier.",
            "narrateur|La boîte fait un petit clac.",
            "papa|On laisse le dessin pour la nuit ?",
            "enfant-f|Oui.",
            "enfant-f|Il garde la fenêtre.",
            "papa|Tu vois le point, Sarah ?",
            "enfant-f|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la vitre.",
            "narrateur|Maman essuie un peu de poussière.",
            "enfant-f|Maman a vu la maison, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-f|Oui, près du soleil.",
            "maman|On est bien, ici.",
            "narrateur|Sarah tapote le papier du doigt.",
            "enfant-f|Il a une trace de crayon.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|Le dessin est resté, Sarah.",
            "enfant-f|Oui, avec le soleil.",
            "narrateur|Ça sent les crayons, un peu tièdes.",
            "enfant-f|Et la laine, maman.",
            "maman|Oui, dans l'air.",
            "papa|Le salon est calme, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le dessin reste contre la vitre.",
            "narrateur|Un éclat de gomme tient sur le papier.",
        ],
    ),
}


def vet(lines: list[str], cid: str = "") -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    skip_q = cid == "CHK_T0000_P0000_Q0001"
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
        if not skip_q and TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        if not skip_q:
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
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
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
        "c'est de la joie",
        "c est de la joie",
        "j'ai dit",
        "j ai dit",
        "tu as nommé",
        "tu as nomme",
        "tu as partagé",
        "tu partages ta joie",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Sarah sourit, la feuille encore chaude. Que dit-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "contente":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != "contente | je suis contente | joie":
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Sarah sourit. Que dit-elle ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
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
    if "je suis contente" not in opening:
        raise SystemExit(f"{SID}: nommage absent avant la question")
    n_contente = blob.count("je suis contente")
    if n_contente != 1:
        raise SystemExit(f"{SID}: je suis contente ×{n_contente}")
    if "crayon" not in blob:
        raise SystemExit(f"{SID}: manque crayon")
    if "pince" not in blob:
        raise SystemExit(f"{SID}: manque pince")
    if "vitre" not in blob:
        raise SystemExit(f"{SID}: manque vitre")
    if "poussière" not in blob and "poussiere" not in blob:
        raise SystemExit(f"{SID}: manque poussière")
    if "tapis" not in blob:
        raise SystemExit(f"{SID}: manque tapis")
    if "casse" not in opening:
        raise SystemExit(f"{SID}: manque crayon casse")
    if "n'est pas rentrée" not in opening and "n est pas rentree" not in opening:
        raise SystemExit(f"{SID}: manque maman pas rentrée")
    if "plie" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: manque feuille qui se plie")
    if "s'accroupit" not in opening and "s accroupit" not in opening:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    for ban in (
        "éclat de crayon",
        "éclat de pince",
        "éclat de vitre",
        "éclat de poussière",
        "éclat de tapis",
        "éclat de tableau",
        "éclat de cadre",
        "éclat de livre",
        "éclat de treille",
        "éclat de moule",
        "éclat de tuteur",
        "éclat de saladier",
        "éclat de tour",
        "éclat de comptoir",
        "éclat de pot",
        "éclat de rouleau",
        "éclat de lit",
        "éclat d'étagère",
        "éclat de torchon",
        "éclat de tabouret",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
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
        "- **Public :** N3 (≤16 mots/phrase), audio familial, voc 5–6 ans\n"
        "- **Leçon :** EMO.LEX.001 — nommer la joie + partager "
        "(vécue : crayon cassé, maman pas rentrée, sourire parti, "
        "papa accroupi, Sarah attend, tend la feuille, dit "
        "« je suis contente » ; 2e ruse : feuille qui se plie à la "
        "vitre, elle refuse de foncer). JAMAIS dite en slogan. "
        "Pas « c'est de la joie ». Pas « j'ai dit : je suis ». "
        "Pas « tu as nommé ».\n"
        "- **Personnages :** Sarah, papa, maman. Sarah = enfant-f "
        "(veut montrer le soleil maintenant). Pas de copain "
        "(dump sans camarade). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** salon, fin d'après-midi, coin de la table "
        "basse. Dump : crayon, pince, vitre, poussière, tapis. "
        "Indice PAS crayon / pince / vitre / poussière / tapis / "
        "tableau / cadre / livre.\n"
        "- **Indice unique :** éclat de gomme (luit près de la "
        "feuille → tremble au casse → luit quand la feuille se "
        "plie → tient sur le papier). BAN éclat de crayon / pince / "
        "vitre / poussière / tapis / treille / moule / tuteur / "
        "saladier / tour / comptoir / pot / rouleau / lit / "
        "étagère / torchon / tabouret.\n"
        "- **Question moteur :** « Sarah sourit, la feuille encore "
        "chaude. Que dit-elle ? » expected dump **contente**. "
        "accepted dump `contente | je suis contente | joie`. "
        "retry dump `Sarah sourit. Que dit-elle ?`. Hors Q : null. "
        "Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / "
        "graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin "
        "heureuse. `chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La laine du tapis sent le soleil. Poussière. Boîte en fer. "
        "Près de la feuille, un éclat de gomme luit. Sarah veut "
        "montrer un soleil à maman **maintenant**. Maman n'est pas "
        "rentrée. Le crayon jaune casse. Sourire parti. Envie et "
        "inquiétude. Papa s'accroupit. Elle attend, tend, dit "
        "je suis contente. Merci vécu. Deuxième ruse : la feuille "
        "se plie à la vitre. Elle s'arrête, lit l'éclat. Un éclat "
        "de gomme tient sur le papier. Dessin à la vitre, fragile.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon, fin d'après-midi, tapis, poussière, "
        "boîte en fer, table basse, fenêtre.\n"
        "- Désir : montrer le dessin du soleil à maman, maintenant.\n"
        "- Objet : feuille blanche, crayon jaune, pince, vitre.\n"
        "- Indice unique : éclat de gomme, vu dès l'ouverture, "
        "payé sur le papier. Pas éclat de crayon / pince / vitre.\n"
        "- Urgence douce : maman n'est pas rentrée, Sarah appuie "
        "trop fort.\n"
        "- Imprévu 1 : crayon jaune casse, trou dans le soleil, "
        "sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "qu'elle refuse de foncer vers la vitre.\n"
        "- Imprévu 2 (plus rusé) : feuille qui se plie contre la "
        "vitre, le soleil va se casser en deux.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le "
        "salon, retrouve l'éclat, lisse le pli.\n"
        "- Retour : dessin à la vitre, pince au coin, éclat sur "
        "le papier. La fin a failli (la feuille a plié).\n\n"
        "## Vécu\n\n"
        "Sarah veut montrer **maintenant**. Impatience, puis crayon "
        "cassé, sourire parti. Elle attend que maman s'assoie, tend "
        "la feuille, dit je suis contente. Papa se baisse, pose une "
        "question, ne récite pas le mot joie. Ils agissent : pince "
        "tiède, feuille qui plie, elle s'arrête. Merci vécu. Fin : "
        "l'éclat du début tient sur le papier.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Sarah et le dessin du soleil (noyau dump). "
        "Relance : Que dit-elle ? expected contente.\n"
        "- Lieu du dump-meta (salon, fin d'après-midi). Maman et "
        "papa. Sarah = héros enfant-f. Dump crayon / pince / vitre / "
        "poussière / tapis gardés comme objets, pas comme indice.\n"
        "- Ouverture inventée (laine du tapis, coin de table basse, "
        "éclat de gomme), pas un gabarit v2, pas « Un rayon "
        "traverse la poussière » en tête, pas « Sarah joue au "
        "salon ».\n"
        "- Indice unique : éclat de gomme ×4. BAN éclat de crayon / "
        "pince / vitre / poussière / tapis / tableau / cadre / "
        "livre. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés hors Q. Q garde « la feuille encore chaude » "
        "(texte moteur).\n"
        "- Leçon non dite : on la voit quand elle attend, quand "
        "elle tend, quand elle dit je suis contente. Pas « c'est "
        "de la joie ». Pas « tu as nommé ». Une seule « je suis "
        "contente ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur conservée. expected/accepted/retry dump. "
        "Hors Q : null. 5 chunks, kinds inchangés.\n"
        "- example4 058 / 090 / 022 (manière volée, gabarit non "
        "collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N3.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, "
        "sous-texte, tempo, sourire, respiration). `slow` = "
        "question et fin. Action un peu plus vive vers la feuille "
        "qui se plie.\n"
        f"- {nwords} mots. N3 ≤ 16. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
