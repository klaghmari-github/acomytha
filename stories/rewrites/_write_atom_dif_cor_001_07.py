#!/usr/bin/env python3
"""ATOM-DIF.COR.001-07 — Les caisses d'oranges de Victorina (F-NAR-019, N2)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.001-07"
TITLE = "Les caisses d'oranges de Victorina"
N2 = LIMITS["N2"]
CHARS = "Victorina, Aniss, papa, maman"
SETTING = "cour après le marché, figue, pierre, caisses"
INDICE = "éclat de figue"
FIL = (
    "Un jus collant tient sur la pierre. Sur la peau, un éclat de figue "
    "luit. Cour après le marché, caisses, figuier. Victorina veut la "
    "boutique d'oranges maintenant. Elle tire trop vite, enseigne trop "
    "haute. Aniss : attends. L'éclat glisse. Elle refuse de foncer, "
    "invite. Aniss regarde, tend le bras. Merci vécu. L'orange file sous "
    "la pile. Elle refuse, se glisse. Un éclat de figue reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tilleul|samare|ballon|carton|cerceau|robinet|planche|"
    r"fraise|tarte|bassine|cheval|pont|cerf-volant|lavande|"
    r"cigale|raisin|gâteau|gateau|vanille|collier|dentelle|"
    r"perle|couture|plaque|dalle|filet)\b",
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
    "tailles différentes",
    "tailles differentes",
    "à sa taille",
    "a sa taille",
    "chacun aide",
    "on peut jouer",
    "vous jouez ensemble",
    "jouer ensemble",
    "tache de couleur",
    "ombre en forme",
    "marque fine",
    "minuscule symbole",
    "éclat de caisse",
    "éclat d'orange",
    "éclat de carton",
    "éclat de pierre",
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
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de samare",
    "éclat d'émail",
    "éclat d'email",
    "éclat de planche",
    "éclat de robinet",
    "grain de",
    "point de gouttière",
    "point de gouttiere",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de figue",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_boutique_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Aniss",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_invite_aniss_ils_jouent; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="Tu veux la boutique",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_invite_aniss_regarde; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de figue",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_sous_la_pile; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de figue",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pale; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer ensemble",
    "accepted_examples": (
        "jouer ensemble | ensemble | ils jouent | on joue | jouer | la boutique"
    ),
    "retry_prompt": "Ils jouent ensemble. Que font Victorina et Aniss ?",
    "engine_ok_text": "Oui, jouer ensemble.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "figue,caisse",
        [
            "narrateur|Un jus collant tient sur la pierre.",
            "enfant-f|C'est sucré, papa.",
            "papa|Tu le sens, sous le doigt ?",
            "enfant-f|Oui, un peu chaud.",
            "narrateur|Sur la peau, un éclat de figue luit.",
            "enfant-f|Il brille, maman.",
            "maman|C'est le soleil, sur la figue ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|L'ombre du figuier est fraîche.",
            "enfant-f|Ça sent l'orange.",
            "papa|Les caisses viennent du marché.",
            "enfant-f|Oui, papa.",
            "narrateur|Le store de toile claque un peu.",
            "narrateur|Une guêpe tourne près d'une écorce.",
            "enfant-f|Elle tourne, là.",
            "maman|On reste près des caisses ?",
            "enfant-f|Oui, maman.",
            "narrateur|Maman pose un panier contre le mur.",
            "narrateur|Trois oranges dorment au fond.",
            "enfant-f|Je les vois.",
            "papa|Tu les comptes, Victorina ?",
            "enfant-f|Trois.",
            "enfant-f|Je veux une boutique, maintenant !",
            "papa|Une boutique d'oranges, ici ?",
            "enfant-f|Oui.",
            "enfant-f|Avec une enseigne.",
            "narrateur|Victorina a un papier.",
            "narrateur|Dessus, une orange un peu penchée.",
            "enfant-f|Elle va tout en haut !",
            "narrateur|En ce moment, Victorina tire une caisse trop vite.",
            "narrateur|Le bois est rêche et chaud.",
            "narrateur|La pile penche.",
            "enfant-f|Oh.",
            "narrateur|Ses doigts touchent seulement le bord.",
            "enfant-f|Je n'arrive pas.",
            "narrateur|L'éclat de figue glisse sur la pierre.",
            "enfant-f|Il part.",
            "narrateur|Le sourire de Victorina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Aniss arrive dans la cour.",
            "narrateur|Ses sandales font un bruit sec.",
            "enfant-f|Aniss !",
            "enfant-f|La boutique, tout de suite !",
            "copain|Attends.",
            "narrateur|Aniss reste près du mur.",
            "enfant-f|Oh.",
            "papa|Tu parles à Aniss, Victorina ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "enfant-f|Oui, papa.",
            "narrateur|La phrase se perd dans le store.",
            "narrateur|Personne n'entend la fin.",
            "narrateur|Victorina referme la bouche, un instant.",
            "narrateur|Le papier reste par terre, un peu lourd.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorina invite Aniss.",
            "narrateur|Que font-ils ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "orange",
        [
            "narrateur|Victorina avance trop vite vers le papier.",
            "enfant-f|Tu mets l'enseigne, maintenant !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copain|Non.",
            "narrateur|Aniss reste près du mur.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Victorina refuse de foncer.",
            "narrateur|Elle pose le papier, un peu.",
            "papa|Le papier est par terre, Victorina ?",
            "narrateur|Papa reste à sa hauteur.",
            "maman|Les caisses sont chaudes, sous tes mains.",
            "enfant-f|Tu veux la boutique ?",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Il regarde le haut de la pile.",
            "copain|Je regarde.",
            "enfant-f|D'accord.",
            "papa|Merci, Victorina.",
            "narrateur|Papa a entendu toute la phrase.",
            "maman|Tu tiens le papier des deux mains ?",
            "enfant-f|Oui, maman.",
            "enfant-f|L'orange est penchée.",
            "papa|Tu parles du store, si tu veux ?",
            "enfant-f|Le store claque un peu.",
            "maman|On reste dans la cour, Victorina ?",
            "enfant-f|Oui.",
            "narrateur|Aniss tend le bras, sans presser.",
            "narrateur|Il pose le papier sur la caisse.",
            "narrateur|L'orange dessinée regarde la cour.",
            "enfant-f|La boutique est ouverte !",
            "copain|Elle est en haut.",
            "enfant-f|Moi, le comptoir.",
            "narrateur|Victorina s'assoit derrière la petite caisse.",
            "narrateur|Elle aligne les trois oranges.",
            "papa|Une orange, s'il te plaît.",
            "enfant-f|Voilà.",
            "narrateur|Victorina tend le fruit.",
            "narrateur|Il est lisse et un peu froid.",
            "maman|Tu as les mains au frais ?",
            "enfant-f|Un peu, maman.",
            "enfant-f|La peau est lisse.",
            "papa|Tu la mets dans le panier ?",
            "enfant-f|Celle du comptoir.",
            "narrateur|Victorina pose une main sur l'orange.",
            "narrateur|Le fruit colle un peu aux doigts.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "bois",
        [
            "narrateur|Victorina pousse une orange trop vite.",
            "enfant-f|La dernière, maintenant !",
            "narrateur|L'orange roule sous la pile.",
            "enfant-f|Oh.",
            "copain|Je ne la vois plus.",
            "narrateur|Aniss se baisse, trop grand.",
            "narrateur|Son épaule tape le bois.",
            "enfant-f|Oh.",
            "narrateur|Papa n'a pas fini sa phrase.",
            "papa|L'orange file, Victorina.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-f|Oh.",
            "narrateur|Victorina refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Elle écoute la cour, un instant.",
            "narrateur|Elle observe le bois, écoute le store.",
            "narrateur|Sur la pierre, un éclat de figue luit.",
            "enfant-f|Il est là.",
            "enfant-f|Tu tiens la pile, si tu veux ?",
            "copain|Oui.",
            "narrateur|Aniss tient la grande caisse.",
            "narrateur|Victorina se glisse près du bois.",
            "narrateur|Elle attrape l'orange.",
            "enfant-f|Te voilà.",
            "papa|Tu restes un peu ?",
            "enfant-f|Oui, papa.",
            "maman|Le panier est près du mur.",
            "copain|Et moi, le sac ?",
            "narrateur|Aniss tient le panier.",
            "narrateur|Victorina pose l'orange dedans.",
            "enfant-f|Elle est à nous.",
            "maman|Elle est dans le panier.",
            "enfant-f|Je la tiens bien.",
            "papa|On marche.",
            "narrateur|Le panier penche, puis se cale.",
            "enfant-f|Je la tiens.",
            "maman|On avance.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "figue",
        [
            "enfant-f|La figue brillait, papa.",
            "papa|Tu le vois, comme dans la cour ?",
            "enfant-f|Oui, sur la pierre.",
            "narrateur|Victorina pose le panier contre elle.",
            "maman|On la garde au frais ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Les oranges sentaient bon.",
            "maman|Elle est contre toi.",
            "narrateur|Une odeur d'orange monte du panier.",
            "narrateur|Victorina respire, plus large.",
            "papa|On rentre ?",
            "enfant-f|Oui.",
            "narrateur|Les joues de Victorina se réchauffent.",
            "enfant-f|On le voit, maman.",
            "maman|Tu le vois sur la pierre ?",
            "enfant-f|Oui, l'éclat.",
            "narrateur|Un éclat de figue reste pâle.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-f", "copain"):
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
        raise SystemExit(f"{SID}: refuse de foncer absent")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Victorina = enfant-f)")
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
    if any(r not in ("narrateur", "papa", "maman", "enfant-f", "copain") for r in roles):
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
        "tailles différentes",
        "tailles differentes",
        "on peut jouer",
        "vous jouez ensemble",
        "jouer ensemble",
        "chacun aide",
        "à sa taille",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Victorina invite Aniss. Que font-ils ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer ensemble":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = str(q.get("retry_prompt") or "").lower()
    if "victorina" not in retry:
        raise SystemExit(f"{SID}: retry sans Victorina")
    if "aniss" not in retry:
        raise SystemExit(f"{SID}: retry sans Aniss")
    if "ensemble" not in retry:
        raise SystemExit(f"{SID}: retry sans ensemble")
    copain_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    ).lower()
    if "attends" not in copain_txt:
        raise SystemExit(f"{SID}: Aniss sans attends")
    if "non" not in copain_txt:
        raise SystemExit(f"{SID}: Aniss sans non")
    if "regarde" not in copain_txt:
        raise SystemExit(f"{SID}: Aniss sans je regarde")
    if "d'accord" not in body:
        raise SystemExit(f"{SID}: Victorina n'accepte pas")
    for ban in (
        "éclat de caisse",
        "éclat d'orange",
        "éclat de carton",
        "éclat de pierre",
        "tilleul",
        "samare",
        "ballon",
        "carton",
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
        "- **Leçon :** DIF.COR.001 — tailles différentes, jouer ensemble "
        "(vécue : Aniss tend le bras en haut ; Victorina se glisse sous la "
        "pile ; boutique ouverte à deux). Jamais dite comme règle.\n"
        "- **Personnages :** Victorina, Aniss, papa, maman. Troupe D16. "
        "Victorina = `enfant-f`. Aniss = `copain`. Papa ajouté (dump n'avait "
        "que maman). Adultes parlants = papa/maman.\n"
        "- **Lieu :** cour après le marché, figue, pierre, caisses, figuier, "
        "store de toile, guêpe, écorce, panier, papier-enseigne, oranges. "
        "≠ 001-02 square/tilleul/carton d'oranges/banc/ballon.\n"
        "- **Indice unique :** éclat de figue (luit à l'ouverture → glisse "
        "quand elle fonce → luit sous la pile → reste pâle). Pas éclat de "
        "caisse (BAN) ni éclat d'orange (BAN) ni éclat de carton (001-02).\n"
        "- **Question moteur :** « Victorina invite Aniss. Que font-ils ? » "
        "expected **jouer ensemble**. retry avec Victorina et Aniss.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un jus collant tient sur la pierre. Sur la peau, un éclat de figue "
        "luit. Cour après le marché, caisses, figuier. Victorina veut la "
        "boutique d'oranges **maintenant**. Première idée : tirer trop vite, "
        "accrocher l'enseigne seule. Trop haute. Aniss arrive : tout de "
        "suite. Attends. L'éclat glisse. Sourire parti. Papa s'accroupit. "
        "Elle refuse de foncer, invite. Aniss regarde, tend le bras. Merci "
        "vécu. Deuxième ruse : l'orange file sous la pile. Aniss trop grand. "
        "Elle refuse, retrouve l'éclat, se glisse. Un éclat de figue reste "
        "pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cour après le marché, figue, pierre, caisses, store, "
        "guêpe, figuier. ≠ 001-02 tilleul/carton/banc.\n"
        "- Désir : la boutique d'oranges, avec enseigne, maintenant.\n"
        "- Objet : papier-enseigne, caisses, oranges, panier, pile.\n"
        "- Indice unique : éclat de figue, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : les bras, l'enseigne en haut, Aniss qui arrive.\n"
        "- Imprévu 1 : caisse trop haute, Aniss manque le tempo, attends, "
        "éclat qui glisse, mots perdus dans le store.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après « d'accord ».\n"
        "- Imprévu 2 (plus rusé) : dernière orange sous la pile ; Aniss trop "
        "grand, épaule contre le bois, voix mélangées.\n"
        "- Résolution : elle refuse de foncer, invite, se glisse, Aniss "
        "tient la grande caisse.\n"
        "- Retour : panier contre elle, éclat de figue pâle.\n\n"
        "## Vécu\n\n"
        "Leçon DIF.COR.001 greffée, jamais annoncée. Victorina propose, "
        "Aniss prend son temps. Le silence compte. La première idée "
        "(accrocher seule, trop vite) échoue. Le choix de Victorina change "
        "l'action. Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Troupe D16 : Victorina, Aniss, papa, maman. N2.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Les caisses d'oranges de Victorina (noyau dump).\n"
        "- Héros Victorina, fille. Aniss conservé, `copain`. Papa ajouté. "
        "Deux rythmes, sans voix caricaturale.\n"
        "- Question moteur : « Victorina invite Aniss. Que font-ils ? » "
        "Fond **jouer ensemble** conservé. retry Victorina + Aniss.\n"
        "- Ouverture inventée (un jus collant tient sur la pierre), pas un "
        "gabarit v2, pas « La figue trop mûre a taché la pierre ».\n"
        "- Indice unique : éclat de figue. Pas éclat de caisse / orange / "
        "carton. Distinct 001-02 (tilleul / oranges / samare).\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Dump « encore / tout doux » jeté.\n"
        "- Leçon non dite : pas « ils ont des tailles différentes », pas "
        "« on peut jouer ensemble », pas « chacun aide à sa taille ».\n"
        "- 5 chunks, kinds inchangés. example4 : 099, 031, 063. "
        "Voix : `_write_atom_col_pol_001_04.py` (Victorina).\n"
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
