#!/usr/bin/env python3
"""ATOM-EMO.LEX.002-06 — Chouchou et la petite fleur (F-NAR-019, N3, EMO.LEX.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.002-06"
TITLE = "Chouchou et la petite fleur"
N3 = LIMITS["N3"]
CHARS = "Chouchou, papa, maman"
SETTING = (
    "jardin, puis salon, haie, fleur, terre, verre, "
    "tige, crayon, papier, table, vitre"
)
INDICE = "éclat de haie"
FIL = (
    "La terre du jardin sent le soleil. Près des fleurs, "
    "un éclat de haie luit. Chouchou veut donner l'eau, maintenant. "
    "Le vent couche la tige. Poitrine trop vite. Sourire parti. "
    "Yeux chauds. Papa s'accroupit. Je suis triste. Un câlin. "
    "Merci vécu. Deuxième ruse : le dessin se déchire au salon. "
    "Il refuse de foncer. Un éclat de haie tient près des fleurs."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(treille|tuteur|panier|fauteuil|paillasson|coffre|"
    r"couverture|capuche|gomme|berge|brouette|housse|"
    r"merle|miel|feuille|feuilles|escargot|grand-père|"
    r"grand-pere|jardinier|maîtresse|maitresse|bibliothécaire|"
    r"bibliothecaire|gardienne)\b",
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
    "pleurer est permis",
    "c'est permis",
    "c est permis",
    "tu as nommé",
    "tu as nomme",
    "tu as dit tes larmes",
    "tu as demandé un câlin",
    "tu as demande un calin",
    "on peut demander un câlin",
    "tu as bien demandé",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de treille",
    "éclat de tuteur",
    "éclat de feuille",
    "éclat de panier",
    "éclat de fauteuil",
    "éclat de paillasson",
    "éclat de coffre",
    "éclat de couverture",
    "éclat de capuche",
    "éclat de gomme",
    "éclat de berge",
    "éclat de brouette",
    "éclat de housse",
    "éclat de crayon",
    "éclat de vitre",
    "éclat de table",
    "éclat de verre",
    "éclat de fleur",
    "éclat de tige",
    "éclat de terre",
    "éclat de gilet",
    "éclat de papier",
    "éclat de dessin",
    "éclat de tour",
    "éclat de cube",
    "éclat de tapis",
    "éclat de rideau",
    "éclat de plaid",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de haie",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis tristesse; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_donner_l_eau_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Chouchou",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=chouchou_a_les_yeux_chauds_que_dit_il; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="câlin",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_nomme_triste_il_demande_un_calin; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de haie",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=le_dessin_se_dechire_il_refuse_de_foncer; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de haie",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pres_des_fleurs; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "triste",
    "accepted_examples": "triste | je suis triste | câlin | un câlin | pleurer",
    "retry_prompt": "Chouchou peut demander un câlin. Que dit-il ?",
    "engine_ok_text": "Oui, triste.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "jardin",
        [
            "narrateur|La terre du jardin sent le soleil.",
            "enfant-m|Ça sent la terre, papa.",
            "papa|Tu la sens, la terre chaude ?",
            "enfant-m|Oui, papa.",
            "narrateur|Chouchou connaît ce jardin, ses coins, ses odeurs.",
            "narrateur|Cette fin de matin, un coin brille autrement.",
            "narrateur|Un vélo passe, très loin, derrière la haie.",
            "maman|Tu entends le vélo, Chouchou ?",
            "enfant-m|Oui, maman.",
            "narrateur|Près des fleurs, un éclat de haie luit.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-m|Oui, sur la haie.",
            "narrateur|La petite fleur attend dans la terre.",
            "narrateur|La tige est verte, un peu fine.",
            "enfant-m|Une tête jaune se tient droite.",
            "papa|Elle est belle, Chouchou ?",
            "enfant-m|Elle est belle, oui.",
            "narrateur|Chouchou tient un verre d'eau, un peu lourd.",
            "enfant-m|C'est pour ma fleur.",
            "maman|Tu lui donnes l'eau, Chouchou ?",
            "enfant-m|Oui, maintenant !",
            "narrateur|En ce moment, Chouchou penche le verre.",
            "narrateur|Une goutte tombe près de la tige.",
            "enfant-m|Bois, petite fleur.",
            "papa|Le vent arrive, Chouchou.",
            "enfant-m|On reste près de la haie ?",
            "papa|Oui, on reste.",
            "narrateur|Le vent pousse les branches de la haie.",
            "narrateur|La tige se couche dans la terre.",
            "enfant-m|Ma fleur !",
            "narrateur|La tête jaune touche la terre humide.",
            "enfant-m|Elle est par terre !",
            "narrateur|Chouchou veut la redresser, tout de suite.",
            "enfant-m|Je la remets, maintenant !",
            "narrateur|Il tire trop vite sur la tige.",
            "narrateur|La tige plie, plus bas qu'avant.",
            "enfant-m|Oh.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Sa gorge se serre.",
            "narrateur|Ses yeux deviennent chauds.",
            "narrateur|Une larme tombe sur le verre.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois la fleur, Chouchou ?",
            "enfant-m|Oui, papa.",
            "maman|Tes yeux sont chauds, Chouchou ?",
            "enfant-m|Un peu, maman.",
            "enfant-m|Je suis triste.",
            "narrateur|Maman s'accroupit aussi, près de lui.",
            "enfant-m|Je veux un câlin.",
            "maman|Viens.",
            "narrateur|Maman ouvre les bras.",
            "narrateur|Chouchou se blottit contre le gilet.",
            "narrateur|Le gilet sent l'herbe chaude.",
            "papa|On reste un peu ?",
            "enfant-m|Oui, papa.",
            "narrateur|L'éclat de haie tremble, puis tient.",
            "narrateur|La tige reste couchée, un peu.",
            "enfant-m|Elle est molle.",
            "papa|On la verra tout à l'heure.",
            "maman|On rentre un moment ?",
            "enfant-m|Oui.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Chouchou a les yeux chauds.",
            "narrateur|Que dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Chouchou sèche une larme avec sa manche.",
            "enfant-m|Le câlin est chaud.",
            "maman|Tes épaules se desserrent ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Ils restent accroupis près de la haie.",
            "papa|On va au salon, Chouchou ?",
            "enfant-m|Oui.",
            "narrateur|Chouchou veut courir vers la porte.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-m|Le dessin, maintenant !",
            "narrateur|Il avance trop vite vers le seuil.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Chouchou refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe la fleur, un instant.",
            "narrateur|Il écoute le jardin.",
            "papa|Tu restes un peu, Chouchou ?",
            "enfant-m|Oui, papa.",
            "papa|Merci, Chouchou.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le verre est tiède, sous les doigts.",
            "enfant-m|Il est vide.",
            "papa|On marche sans se presser ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le ventre de Chouchou se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|On prend le crayon rouge ?",
            "enfant-m|Oui, pour la fleur.",
            "narrateur|Ils passent la porte du salon.",
            "enfant-m|La table est là.",
            "papa|Tu as de la place, Chouchou ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le crayon rouge attend près du bord.",
            "maman|Tu fais ta fleur, Chouchou ?",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "papier",
        [
            "narrateur|Un papier blanc attend sur la table.",
            "enfant-m|Je dessine ma fleur.",
            "narrateur|Le crayon rouge a un bout usé.",
            "papa|Tu fais la tige, Chouchou ?",
            "enfant-m|Oui, papa.",
            "narrateur|Chouchou trace une tige, trop vite.",
            "enfant-m|Et la tête jaune !",
            "narrateur|Il appuie trop fort sur le papier.",
            "narrateur|Un coin du dessin se fend.",
            "enfant-m|Il se déchire !",
            "narrateur|Le papier s'ouvre un peu, net.",
            "enfant-m|Ma fleur !",
            "narrateur|Chouchou veut coller le coin, tout de suite.",
            "enfant-m|Je le tiens, maintenant !",
            "narrateur|Il avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Chouchou refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le dessin, un instant.",
            "narrateur|Il écoute le salon, près de la table.",
            "narrateur|Derrière la vitre, un éclat de haie luit.",
            "enfant-m|Là, sur la haie.",
            "narrateur|Chouchou pose les mains à plat.",
            "enfant-m|Je veux un câlin.",
            "papa|Viens.",
            "narrateur|Papa le serre, sans se presser.",
            "enfant-m|Le coin est fendu.",
            "maman|On le lisse un peu ?",
            "enfant-m|Oui, maman.",
            "narrateur|Chouchou lisse le papier, sans se presser.",
            "papa|On tient le coin ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le dessin reste, un peu fendu.",
            "enfant-m|Poumf.",
            "maman|La tête jaune est là, Chouchou ?",
            "enfant-m|Oui, maman.",
            "papa|Tu vois le point, Chouchou ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le crayon rouge a roulé près du bord.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "jardin",
        [
            "narrateur|Ils reviennent près de la haie.",
            "narrateur|Maman redresse un peu la tige.",
            "enfant-m|Elle se tient.",
            "maman|Elle se tient, oui.",
            "narrateur|Chouchou pose son dessin près de lui.",
            "enfant-m|Le coin est fendu, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, près de la tige.",
            "maman|On est bien, ici.",
            "narrateur|Chouchou tapote le papier du doigt.",
            "enfant-m|Il a une trace de crayon.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|La fleur est restée, Chouchou.",
            "enfant-m|Oui, avec le dessin.",
            "narrateur|Ça sent la terre, un peu tiède.",
            "enfant-m|Et l'herbe, maman.",
            "maman|Oui, dans l'air.",
            "papa|Le jardin est calme, Chouchou ?",
            "enfant-m|Oui, papa.",
            "narrateur|La petite fleur reste dans la terre.",
            "narrateur|Un éclat de haie tient près des fleurs.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-m"):
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
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Chouchou dump = enfant-m)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé (dump sans camarade)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    if "félix" in blob or "felix" in blob:
        raise SystemExit(f"{SID}: Félix resté (dump xai)")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "enfant-m" for r in roles):
        raise SystemExit(f"{SID}: enfant-m absent")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "pleurer est permis",
        "j'ai dit",
        "j ai dit",
        "tu as nommé",
        "tu as nomme",
        "c'est permis",
        "c est permis",
        "on peut demander un câlin",
        "tu as demandé un câlin",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Chouchou a les yeux chauds. Que dit-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "triste":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "triste | je suis triste | câlin | un câlin | pleurer"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Chouchou peut demander un câlin. Que dit-il ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    if "félix" in retry.lower() or "felix" in retry.lower():
        raise SystemExit(f"{SID}: retry Félix")
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
    if "fleur" not in blob:
        raise SystemExit(f"{SID}: manque fleur")
    if "vent" not in blob:
        raise SystemExit(f"{SID}: manque vent")
    if "dessin" not in blob:
        raise SystemExit(f"{SID}: manque dessin")
    if "jardin" not in blob:
        raise SystemExit(f"{SID}: manque jardin")
    if "salon" not in blob:
        raise SystemExit(f"{SID}: manque salon")
    if "s'accroupit" not in opening and "s accroupit" not in opening:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    if "yeux" not in opening or "chauds" not in opening:
        raise SystemExit(f"{SID}: manque yeux chauds avant Q")
    if "câlin" not in opening and "calin" not in opening:
        raise SystemExit(f"{SID}: manque câlin avant Q")
    end_txt = by["CHK_T0000_P0000_END"]["text"].lower()
    if "déchire" not in end_txt and "dechire" not in end_txt and "fend" not in end_txt:
        raise SystemExit(f"{SID}: manque dessin qui se déchire")
    for ban in (
        "éclat de treille",
        "éclat de tuteur",
        "éclat de feuille",
        "éclat de panier",
        "éclat de fauteuil",
        "éclat de paillasson",
        "éclat de coffre",
        "éclat de couverture",
        "éclat de capuche",
        "éclat de gomme",
        "éclat de berge",
        "éclat de brouette",
        "éclat de housse",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "pleurer est permis",
        "j'ai dit",
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
        "- **Leçon :** EMO.LEX.002 — nommer la tristesse + câlin "
        "(vécue : vent couche la tige, sourire parti, yeux chauds, "
        "papa accroupi, Chouchou dit « je suis triste », demande un "
        "câlin ; 2e ruse : dessin qui se déchire au salon, il refuse "
        "de foncer). JAMAIS dite en slogan. Pas « j'ai dit : je suis ». "
        "Pas « pleurer est permis ».\n"
        "- **Personnages :** Chouchou, papa, maman. Dump Félix → "
        "Chouchou. Dump `enfant-m` + Q « Que dit-il ? » conservés "
        "(garçon pour cet atome). Pas de copain (dump sans camarade). "
        "Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** jardin, puis salon. Dump : fleur, vent, dessin, "
        "crayon, tige, terre. Indice PAS treille / tuteur / feuille / "
        "panier (haie n'est pas un tuteur).\n"
        "- **Indice unique :** éclat de haie (luit près des fleurs → "
        "tremble à la chute → luit derrière la vitre au salon → "
        "tient près des fleurs). BAN éclat de treille / tuteur / "
        "feuille / panier / fauteuil / paillasson / coffre / "
        "couverture / capuche / gomme / berge / brouette / housse.\n"
        "- **Question moteur :** « Chouchou a les yeux chauds. Que "
        "dit-il ? » expected dump **triste**. accepted dump "
        "`triste | je suis triste | câlin | un câlin | pleurer`. "
        "retry dump Félix → Chouchou. Hors Q : null. Non récitée "
        "dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / "
        "graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin "
        "heureuse. `chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La terre du jardin sent le soleil. Vélo loin. Près des "
        "fleurs, un éclat de haie luit. Chouchou veut donner l'eau "
        "**maintenant**. Le vent couche la tige. Il tire trop vite. "
        "Sourire parti. Yeux chauds. Papa s'accroupit. Je suis triste. "
        "Un câlin. Merci vécu. Deuxième ruse : le dessin se déchire "
        "au salon. Il s'arrête, lit l'éclat derrière la vitre. Un "
        "éclat de haie tient près des fleurs. Tige un peu molle, "
        "papier fendu. La fin a failli.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin connu, coin de la haie, terre chaude, "
        "verre d'eau, puis salon et table.\n"
        "- Désir : donner l'eau à la petite fleur, maintenant.\n"
        "- Objet : petite fleur (tige verte, tête jaune), puis "
        "dessin au crayon rouge.\n"
        "- Indice unique : éclat de haie, vu dès l'ouverture, payé "
        "près des fleurs. Pas éclat de treille / tuteur / feuille.\n"
        "- Urgence douce : il penche le verre, le vent arrive, il "
        "tire trop vite.\n"
        "- Imprévu 1 : vent couche la tige, sourire parti, yeux "
        "chauds, une larme.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "qu'il refuse de foncer vers la porte.\n"
        "- Imprévu 2 (plus rusé) : dessin qui se déchire au salon, "
        "le coin se fend.\n"
        "- Résolution : il refuse de foncer, observe, écoute le "
        "salon, retrouve l'éclat, demande un câlin, lisse le papier.\n"
        "- Retour : tige un peu redressée, dessin fendu, éclat près "
        "des fleurs. La fin a failli (la tige a plié, le papier "
        "s'est fendu).\n\n"
        "## Vécu\n\n"
        "Chouchou veut donner l'eau **maintenant**. Impatience, puis "
        "tige couchée, sourire parti, yeux chauds. Il dit je suis "
        "triste, demande un câlin, se blottit. Papa se baisse, pose "
        "une question, ne récite pas « pleurer est permis ». Ils "
        "agissent : marche sans se presser, dessin, papier qui se "
        "fend, il s'arrête. Merci vécu. Fin : l'éclat du début tient "
        "près des fleurs.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Chouchou et la petite fleur (noyau dump). Relance : "
        "Que dit-il ? expected triste.\n"
        "- Lieu du dump-meta (jardin, puis salon). Maman et papa. "
        "Chouchou = héros enfant-m (dump + Q masculine). Dump fleur / "
        "vent / dessin gardés comme objets, pas comme indice.\n"
        "- Ouverture inventée (terre du jardin, coin qui brille, "
        "éclat de haie), pas un gabarit v2, pas « Un escargot "
        "avance sur la pierre », pas « Chouchou joue au salon ».\n"
        "- Indice unique : éclat de haie ×4. BAN éclat de treille / "
        "tuteur / feuille / panier / fauteuil / paillasson / coffre / "
        "couverture / capuche / gomme / berge / brouette. Pas "
        "tache/flèche/marque/symbole. Haie n'est pas un tuteur.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doucement » du dump.\n"
        "- Leçon non dite : on la voit quand les yeux sont chauds, "
        "quand il dit je suis triste, quand il demande un câlin. "
        "Pas « pleurer est permis ». Pas « j'ai dit : je suis ». "
        "Une seule « je suis triste ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur conservée. expected/accepted dump. retry "
        "Félix → Chouchou. Hors Q : null. 5 chunks, kinds inchangés.\n"
        "- example4 066 / 098 / 030 (manière volée, gabarit non "
        "collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N3.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, "
        "sous-texte, tempo, sourire, respiration). `slow` = "
        "question et fin. Action un peu plus vive vers le dessin "
        "qui se déchire.\n"
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
