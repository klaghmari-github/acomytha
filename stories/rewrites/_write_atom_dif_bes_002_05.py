#!/usr/bin/env python3
"""ATOM-DIF.BES.002-05 — Le garage en carton (F-NAR-019, N2, DIF.BES.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.002-05"
TITLE = "Le garage en carton"
N2 = LIMITS["N2"]
CHARS = "Chouchou, Mila, papa, maman"
SETTING = "couloir, carton, vent dans la cheminée"
INDICE = "éclat de cheminée"
FIL = (
    "La cheminée boit le vent. Sur la brique, un éclat de cheminée brille. "
    "Un carton ouvert attend dans le couloir. Chouchou veut la voiture rouge "
    "dans le garage maintenant. Elle tire trop vite, attrape Mila : non. "
    "Le rabat est dur, l'éclat glisse. Elle refuse de foncer, propose. "
    "Mila regarde, plus tard. Merci vécu. La voiture file trop vite. "
    "Elle refuse, propose le rabat. Toc. L'éclat de cheminée tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(cheval|pont|cerf-volant|lavande|cigale|raisin|gâteau|gateau|"
    r"vanille|collier|dentelle|perle|couture|plaque|dalle)\b",
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
    "j'ai proposé",
    "j'ai propose",
    "j'ai accepté",
    "j'ai accepte",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "c'est la règle",
    "bon travail",
    "tu as bien fait",
    "tu as su",
    "a su proposer",
    "plusieurs réponses",
    "plusieurs reponses",
    "c'est une réponse",
    "c'est une reponse",
    "on peut proposer",
    "on peut accepter",
    "regarder, c'est",
    "inviter sans forcer",
    "tache de couleur",
    "ombre en forme",
    "marque fine",
    "minuscule symbole",
    "éclat de carton",
    "éclat de couloir",
    "éclat de plaque",
    "éclat de pierre",
    "éclat de grille",
    "éclat de couvercle",
    "éclat de dalle",
    "éclat de cour",
    "éclat de sac",
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
    "éclat de bois",
    "éclat de carte",
    "éclat de cube",
    "éclat de boule",
    "éclat de galet",
    "éclat de poussière",
    "éclat de poussiere",
    "éclat de crayon",
    "éclat de buée",
    "éclat de buee",
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
    "éclat de pompon",
    "éclat de manteau",
    "éclat de seau",
    "éclat de mousse",
    "éclat de carotte",
    "éclat de tapis",
    "éclat de farine",
    "grain de",
    "point de gouttière",
    "point de gouttiere",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de cheminée",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_garage_avec_mila_maintenant; "
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
            "sous_texte=elle_invite_sans_tirer_la_manche; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="Tu veux pousser",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_propose_mila_regarde; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de cheminée",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_sur_le_rabat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de cheminée",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_brique; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "proposer",
    "accepted_examples": (
        "proposer | inviter | accepter | d'accord"
    ),
    "retry_prompt": "Chouchou peut proposer. Que fait-on ?",
    "engine_ok_text": "Oui, proposer.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "vent,carton",
        [
            "narrateur|La cheminée boit le vent, froid et creux.",
            "enfant-f|Ça souffle, papa !",
            "papa|Tu l'entends, dans la brique ?",
            "enfant-f|Oui, un son long.",
            "narrateur|Sur la brique, un éclat de cheminée brille.",
            "enfant-f|Il brille, maman.",
            "maman|C'est le vent, sur la brique ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Le carrelage du couloir est froid sous les chaussettes.",
            "enfant-f|Il pique les pieds.",
            "papa|On reste près du carton ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un carton ouvert attend contre le mur.",
            "narrateur|Il sent le papier neuf.",
            "enfant-f|Ça sent le papier.",
            "maman|Le rabat peut faire une porte.",
            "enfant-f|Une porte de garage !",
            "narrateur|Une voiture rouge de bois est par terre.",
            "narrateur|Ses roues sont noires et lisses.",
            "enfant-f|Le phare est jaune.",
            "papa|Tu la vois, Chouchou ?",
            "enfant-f|Oui, elle rentre dedans, maintenant !",
            "narrateur|Maman ouvre la porte du couloir.",
            "narrateur|Mila arrive, en chaussettes à rayures.",
            "enfant-f|Mila !",
            "copine|J'arrive.",
            "maman|Tes chaussettes ont des rayures ?",
            "copine|Oui.",
            "enfant-f|Le garage, maintenant, Mila !",
            "narrateur|En ce moment, Chouchou tire le carton trop vite.",
            "narrateur|Le carton racle le carrelage.",
            "narrateur|Une poussière s'envole.",
            "enfant-f|Tu viens, tout de suite !",
            "narrateur|Chouchou attrape la manche de Mila.",
            "copine|Non.",
            "narrateur|Mila recule vers le mur.",
            "enfant-f|Oh.",
            "narrateur|Chouchou pousse le rabat d'un coup.",
            "narrateur|Le rabat est dur, il résiste.",
            "papa|Le rabat est dur, Chouchou ?",
            "enfant-f|Oui.",
            "narrateur|La voiture tape le bord.",
            "narrateur|Elle ne rentre pas.",
            "enfant-f|Oh.",
            "narrateur|L'éclat de cheminée glisse sur la brique.",
            "enfant-f|Il part.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Tu parles à Mila, Chouchou ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "enfant-f|Oui, papa.",
            "narrateur|La phrase se perd dans le vent.",
            "narrateur|Personne n'entend la fin.",
            "narrateur|Chouchou referme la bouche, un instant.",
            "narrateur|La voiture reste dehors, un peu lourde.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Chouchou invite Mila.",
            "narrateur|Que fait-on ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "roues",
        [
            "narrateur|Chouchou avance la voiture trop vite.",
            "enfant-f|Tu pousses, Mila, maintenant !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copine|Non.",
            "narrateur|Mila reste près du mur.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Chouchou refuse de foncer.",
            "narrateur|Elle lâche la manche, un peu.",
            "papa|La voiture est dehors, Chouchou ?",
            "narrateur|Papa reste à sa hauteur.",
            "maman|Le rabat est dur, sous tes mains.",
            "narrateur|Maman n'a pas fini non plus.",
            "narrateur|Chouchou attend que le silence arrive.",
            "enfant-f|Tu veux pousser ?",
            "narrateur|Mila ne dit rien.",
            "narrateur|Elle s'assoit près du mur.",
            "copine|Je regarde.",
            "enfant-f|D'accord.",
            "papa|Merci, Chouchou.",
            "narrateur|Papa a entendu toute la phrase.",
            "maman|Tu tiens la voiture des deux mains ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Les roues sont froides.",
            "papa|Tu parles du vent, si tu veux ?",
            "enfant-f|La cheminée boit le vent.",
            "maman|On reste au couloir, Chouchou ?",
            "enfant-f|Oui.",
            "narrateur|Chouchou pousse la voiture sans presser.",
            "narrateur|Les roues font un petit bruit.",
            "narrateur|Le phare jaune avance.",
            "enfant-f|Elle va au rabat.",
            "papa|Tu as entendu les roues ?",
            "enfant-f|Oui, papa.",
            "narrateur|La voiture s'arrête devant le rabat.",
            "narrateur|Le phare jaune touche le carton.",
            "narrateur|Elle n'est pas dedans.",
            "enfant-f|Presque.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "carton",
        [
            "narrateur|Chouchou quitte le mur avec la voiture.",
            "narrateur|Le vent glisse dans la cheminée.",
            "enfant-f|Tu fermes le rabat, maintenant !",
            "narrateur|Chouchou pousse trop vite.",
            "narrateur|La voiture dépasse le carton.",
            "enfant-f|Oh.",
            "narrateur|Papa n'a pas fini sa phrase.",
            "papa|La voiture file, Chouchou.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-f|Oh.",
            "narrateur|Chouchou refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Elle écoute le couloir, un instant.",
            "narrateur|Elle observe la voiture, écoute la cheminée.",
            "narrateur|Sur la brique, un éclat de cheminée luit.",
            "enfant-f|Il est là.",
            "enfant-f|Tu fermes le rabat, si tu veux ?",
            "copine|Plus tard.",
            "enfant-f|D'accord.",
            "narrateur|Mila reste à regarder.",
            "narrateur|Chouchou pose la voiture sans presser.",
            "narrateur|Les roues passent le rabat.",
            "narrateur|Ça fait toc.",
            "enfant-f|Elle est dedans.",
            "papa|Tu restes un peu ?",
            "enfant-f|Oui, papa.",
            "maman|Le carton est près du mur.",
            "enfant-f|On le laisse ?",
            "papa|Oui, contre la brique.",
            "narrateur|La voiture sent le bois.",
            "enfant-f|Elle colle aux doigts.",
            "maman|Comme le papier, oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "vent",
        [
            "narrateur|Ils restent près du carton.",
            "narrateur|Maman referme le rabat, sans bruit.",
            "enfant-f|Comme une porte, papa.",
            "papa|Tu le vois, toi ?",
            "enfant-f|Oui, sur la brique.",
            "maman|On est bien, ici.",
            "narrateur|Chouchou glisse le doigt, sans se presser.",
            "enfant-f|On le sent, maman.",
            "maman|Tu le sens sur tes doigts ?",
            "enfant-f|Oui, il colle.",
            "papa|Le rabat est fermé, Chouchou.",
            "enfant-f|Oui, avec la voiture.",
            "narrateur|L'odeur de papier reste dans le couloir.",
            "enfant-f|Il est là, maman.",
            "maman|Oui, sur la brique.",
            "narrateur|L'éclat de cheminée tient sur la brique.",
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
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"extra {bad}: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-f", "copine"):
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
    out["pitch_xai_tag"] = m.get("pitchTag")
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
        raise SystemExit(f"{SID}: enfant-m (Chouchou = enfant-f)")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Mila absente (copine)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f", "copine") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "copine" for r in roles):
        raise SystemExit(f"{SID}: copine absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on peut proposer",
        "on peut accepter",
        "plusieurs réponses",
        "c'est une réponse",
        "a su proposer",
        "inviter sans forcer",
        "j'ai proposé",
        "j'ai accepté",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Chouchou invite Mila. Que fait-on ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "proposer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = str(q.get("retry_prompt") or "").lower()
    if "chouchou" not in retry:
        raise SystemExit(f"{SID}: retry sans Chouchou")
    if "proposer" not in retry:
        raise SystemExit(f"{SID}: retry sans proposer")
    if "lise" in retry:
        raise SystemExit(f"{SID}: Lise dans retry")
    copine_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    ).lower()
    if "non" not in copine_txt:
        raise SystemExit(f"{SID}: Mila sans non")
    if "regarde" not in copine_txt:
        raise SystemExit(f"{SID}: Mila sans je regarde")
    if "plus tard" not in copine_txt:
        raise SystemExit(f"{SID}: Mila sans plus tard")
    if "d'accord" not in body:
        raise SystemExit(f"{SID}: Chouchou n'accepte pas")
    for ban in (
        "éclat de carton",
        "éclat de couloir",
        "éclat de plaque",
        "éclat de pierre",
        "éclat de grille",
        "éclat de couvercle",
        "éclat de dalle",
        "kilian",
        "maël",
        "mael",
        "lise",
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
        "- **Public :** N2 (≤15 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.BES.002 — inviter sans forcer (vécue : proposer, "
        "accepter oui / non / je regarde / plus tard ; le silence compte). "
        "Jamais dite comme règle.\n"
        "- **Personnages :** Chouchou, Mila, papa, maman. Troupe D16. "
        "Dump `enfant-m` → `enfant-f` (Chouchou). Mila = `copine`. "
        "Adultes parlants = papa/maman.\n"
        "- **Lieu :** couloir, carton, vent dans la cheminée, brique, "
        "carrelage froid, voiture rouge de bois, phare jaune, rabat, "
        "chaussettes à rayures. ≠ 002-01 cuisine/gâteaux/cheval. "
        "≠ 002-02 terrasse/lavande/cerf-volant. ≠ 002-03 raisins/gâteau. "
        "≠ 002-04 collier/dentelle.\n"
        "- **Indice unique :** éclat de cheminée (brille à l'ouverture → "
        "glisse quand elle fonce → luit au refus → tient sur la brique). "
        "Pas éclat de carton (BAN ECO.002-03) ni éclat de couloir "
        "(BAN 001-06). Distinct 002-01..04 (plaque / pierre / grille / "
        "couvercle).\n"
        "- **Question moteur :** « Chouchou invite Mila. Que fait-on ? » "
        "expected **proposer**. retry avec Chouchou.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La cheminée boit le vent. Sur la brique, un éclat de cheminée "
        "brille. Un carton ouvert attend dans le couloir. Voiture rouge, "
        "phare jaune. Chouchou veut le garage **maintenant**, avec Mila. "
        "Elle tire trop vite, attrape la manche : non. Le rabat est dur, "
        "la voiture tape le bord, l'éclat glisse. Sourire parti. Papa "
        "s'accroupit. Elle refuse de foncer, propose. Mila regarde. "
        "Merci vécu. Deuxième ruse : la voiture file trop vite. Elle "
        "refuse, retrouve l'éclat, propose le rabat. Plus tard. Toc. "
        "Le rabat se ferme. L'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : couloir, cheminée, brique, carrelage froid, carton "
        "ouvert, papier neuf, vent creux. ≠ 002-01..04.\n"
        "- Désir : la voiture rouge dans le garage, avec Mila, maintenant.\n"
        "- Objet : carton, rabat-porte, voiture rouge, phare jaune, "
        "roues noires, manche de Mila.\n"
        "- Indice unique : éclat de cheminée, vu dès l'ouverture, payé "
        "sur la brique au retour.\n"
        "- Urgence douce : Mila vient, le garage attend, Chouchou tire.\n"
        "- Imprévu 1 : manche attrapée, non, rabat dur, voiture dehors, "
        "éclat qui glisse, mots perdus dans le vent.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après « d'accord » "
        "près du mur.\n"
        "- Imprévu 2 (plus rusé) : fermer le rabat maintenant ; la voiture "
        "dépasse le carton, les voix se mélangent.\n"
        "- Résolution : elle refuse de foncer, propose, accepte le silence, "
        "le regard, plus tard.\n"
        "- Retour : rabat fermé (le carton ouvert du début a changé), "
        "l'éclat tient sur la brique.\n\n"
        "## Vécu\n\n"
        "Leçon DIF.BES.002 greffée, jamais annoncée. Chouchou propose, "
        "Mila prend son temps ou pose sa limite. Le silence compte. "
        "La première idée (tirer, attraper) échoue. Le choix de Chouchou "
        "change l'action. Un « en ce moment ». Un merci vécu. Adulte + "
        "question. Troupe D16 : Chouchou, Mila, papa, maman. N2.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le garage en carton (noyau dump).\n"
        "- Héros Chouchou, fille. Dump `enfant-m` → `enfant-f`. Mila "
        "conservée, `copine`. Deux rythmes, sans voix caricaturale.\n"
        "- Question moteur : « Chouchou invite Mila. Que fait-on ? » "
        "Fond **proposer** conservé. retry Lise absent, Chouchou nommé.\n"
        "- Ouverture inventée (la cheminée boit le vent), pas un gabarit "
        "v2, pas « joue au salon ».\n"
        "- Indice unique : éclat de cheminée. Pas éclat de carton "
        "(ECO.002-03), pas éclat de couloir (001-06), pas plaque / "
        "pierre / grille / couvercle (002-01..04).\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Dump « tout bas / tout doux / encore / déjà » jeté.\n"
        "- Leçon non dite : pas « on peut proposer », pas « plusieurs "
        "réponses sont possibles », pas « regarder, c'est une réponse », "
        "pas « j'ai proposé ».\n"
        "- 5 chunks, kinds inchangés. example4 : 090, 022, 054. "
        "Voix : `_write_atom_col_pol_001_11.py` (Chouchou).\n"
        f"- {nwords} mots. N2 ≤ 15. TTS : notes, ssml, xai, piper par "
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
