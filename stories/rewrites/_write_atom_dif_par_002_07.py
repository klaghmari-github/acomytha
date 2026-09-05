#!/usr/bin/env python3
"""ATOM-DIF.PAR.002-07 — Nino laisse le temps à Aniss (F-NAR-019, N1, DIF.PAR.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.002-07"
TITLE = "Nino laisse le temps à Aniss"
N1 = LIMITS["N1"]
CHARS = "Nino, Aniss, papa, maman"
SETTING = (
    "salon, lampe, table, boîte, fenêtre, rideau, "
    "coquillage beige, ligne rose"
)
INDICE = "éclat de coquillage"
FIL = (
    "La lampe fait un rond chaud. Sur le bord, un "
    "éclat de coquillage luit. Nino veut raconter, "
    "maintenant, ce qu'il y a dedans. Aniss dit j'ai "
    "vu, cherche le mot. Nino connaît, ouvre la bouche "
    "maintenant, la referme, attend. Escargot. Merci "
    "vécu. Deuxième ruse : l'oreille, la mer. Un éclat "
    "de coquillage tient sur le bord."
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
    r"lacet|tapis|sauge|chiffon|parquet|canapé|canape|"
    r"assiette|étal|etal|plateau|chat|papillon|carotte|"
    r"pupitre|poule|pomme|bateau|canard|couverture|"
    r"paillasson|rambarde|gond|portail|ballon)\b",
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
    "j'ai attendu",
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
    "ce n'est pas une faute",
    "ce n est pas une faute",
    "on peut jouer",
    "on peut attendre",
    "on peut laisser",
    "laisser le temps",
    "on laisse le temps",
    "n'achève pas",
    "n acheve pas",
    "fin de la phrase",
    "tu as laissé",
    "tu as laisse",
    "vous avez laissé",
    "vous avez laisse",
    "tu as su attendre",
    "on attend la fin",
    "vous jouez",
    "on joue",
    "chacun son tour",
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
    "éclat d'assiette",
    "éclat d assiette",
    "éclat d'étal",
    "éclat d'etal",
    "éclat de plateau",
    "éclat de pupitre",
    "éclat de gond",
    "éclat de rambarde",
    "éclat de table",
    "éclat de lampe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de fenêtre",
    "éclat de fenetre",
    "éclat de rideau",
    "éclat de bord",
    "éclat de rond",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

# N1 : mêmes champs que ENE.001-09 (voix, tempos plus lents).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat de coquillage",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis retenue; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_raconter_maintenant; "
            "tempo=posé puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=104, speed=0.80, piper=1.36, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=780,
        sentence=360, energy="focused", contour="rising", noise=0.30,
        emphasis="mot",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=aniss_cherche_un_mot_que_fait_nino; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=122, speed=0.88, piper=1.24, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=620,
        sentence=310, energy="bright", contour="falling", noise=0.33,
        emphasis="escargot",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_referme_la_bouche_aniss_trouve; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de coquillage",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=l_oreille_la_mer_il_referme_encore; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de coquillage",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bord; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

# Dump Q : expected/accepted/retry conservés ; Didier → Nino.
Q_FIELDS = {
    "expected_answer": "attendre",
    "accepted_examples": "attendre | laisser le temps | il attend | écouter",
    "retry_prompt": "On n'achève pas à sa place. Que fait Nino ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "",
        [
            "narrateur|La lampe fait un rond chaud.",
            "enfant-m|Il est chaud, papa.",
            "papa|Tu le vois, le rond, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le rond pose sur la table.",
            "maman|La table est claire, ce soir.",
            "enfant-m|Oui, maman.",
            "narrateur|La fenêtre est bleue, dehors.",
            "papa|Tu vois le bleu, Nino ?",
            "enfant-m|Oui, il est bleu.",
            "narrateur|Papa ouvre une petite boîte.",
            "narrateur|La boîte sent le bois sec.",
            "enfant-m|Ça sent le bois, papa.",
            "papa|Tu entends le couvercle ?",
            "enfant-m|Oui, il claque.",
            "narrateur|Un coquillage beige sort.",
            "narrateur|Il est un peu rugueux.",
            "enfant-m|Il pique un peu, maman.",
            "maman|Sous le doigt ?",
            "enfant-m|Oui.",
            "narrateur|Une ligne rose tourne dedans.",
            "enfant-m|Elle est rose.",
            "papa|Tu la vois, la ligne ?",
            "enfant-m|Oui, papa.",
            "narrateur|Sur le bord, un éclat de coquillage luit.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-m|Oui, un petit point.",
            "papa|La lampe le touche.",
            "narrateur|Nino pose la paume dessus.",
            "narrateur|Le coquillage est froid.",
            "enfant-m|Il est froid.",
            "maman|Tu le tiens, Nino ?",
            "enfant-m|Oui.",
            "narrateur|En ce moment, Nino le lève.",
            "enfant-m|Je veux raconter, maintenant !",
            "enfant-m|Ce qu'il y a dedans.",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|Aniss arrive près de la table.",
            "narrateur|Il regarde le coquillage.",
            "copain|J'ai vu.",
            "narrateur|Aniss cherche le mot.",
            "narrateur|Sa bouche reste ouverte.",
            "narrateur|Nino connaît le mot.",
            "narrateur|Il ouvre la bouche, maintenant.",
            "narrateur|Le mot pousse, tout près.",
            "narrateur|Ses lèvres bougent.",
            "enfant-m|Oh.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et l'attente se heurtent.",
            "narrateur|Il referme la bouche.",
            "narrateur|Il pose ses mains.",
            "narrateur|Personne ne dit le mot.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Aniss, Nino ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains sont froides, Nino ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de coquillage tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss cherche un mot.",
            "narrateur|Que fait Nino ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Nino garde la bouche fermée.",
            "narrateur|Aniss cherche, un instant.",
            "copain|J'ai vu un escargot.",
            "enfant-m|Dans le coquillage ?",
            "copain|Oui.",
            "papa|Merci, Nino.",
            "narrateur|Papa a vu les deux, près de la table.",
            "maman|La ligne rose est là, Aniss ?",
            "copain|Oui.",
            "enfant-m|Elle tourne.",
            "narrateur|Nino approche l'oreille.",
            "narrateur|Le coquillage est calme.",
            "papa|Tu entends un bruit, Nino ?",
            "enfant-m|Un petit bruit.",
            "maman|Aniss, tu entends aussi ?",
            "copain|Un peu.",
            "narrateur|Le ventre de Nino se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "enfant-m|Il est petit.",
            "copain|Oui, petit.",
            "papa|On reste près de la table ?",
            "enfant-m|Oui.",
            "maman|Tes mains sont au chaud ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Ils posent le coquillage.",
            "narrateur|La lampe tient le rond.",
            "enfant-m|Il brille.",
            "papa|Tu le vois, le bord ?",
            "enfant-m|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Maman approche le coquillage.",
            "narrateur|Elle le tend vers Aniss.",
            "enfant-m|J'écoute, maintenant !",
            "narrateur|Aniss le pose contre l'oreille.",
            "copain|J'entends.",
            "narrateur|Aniss cherche le mot.",
            "narrateur|Sa bouche reste ouverte.",
            "narrateur|Nino connaît le mot.",
            "narrateur|Il ouvre la bouche, trop vite.",
            "narrateur|Le mot pousse, tout près.",
            "enfant-m|Oh.",
            "narrateur|Nino referme la bouche.",
            "narrateur|Il pose ses mains.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Sur le bord, un éclat de coquillage luit.",
            "enfant-m|Là, sur le bord.",
            "enfant-m|Tu entends, Aniss ?",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Il souffle, puis écoute.",
            "copain|La mer.",
            "enfant-m|Dans le coquillage ?",
            "copain|Oui.",
            "papa|On range la boîte ?",
            "enfant-m|Oui, papa.",
            "narrateur|La boîte sent le bois sec.",
            "narrateur|Le coquillage glisse dedans.",
            "enfant-m|Il est à sa place.",
            "maman|Le couvercle, Aniss ?",
            "copain|Oui.",
            "papa|La lampe est calme, Nino ?",
            "enfant-m|Oui, papa.",
            "maman|Un rond reste sur la table.",
            "enfant-m|Il allume le bord.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la table.",
            "narrateur|Maman ferme un peu la boîte.",
            "enfant-m|Le coquillage est dedans, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, près de la lampe.",
            "maman|On est bien, ici.",
            "narrateur|Nino tapote le couvercle du doigt.",
            "enfant-m|Il a une trace de bois.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|Le coquillage est resté, Nino.",
            "enfant-m|Oui, avec Aniss.",
            "copain|Le coquillage est resté.",
            "narrateur|Ça sent le bois, un peu tiède.",
            "enfant-m|Et la lampe, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|La boîte reste sur la table.",
            "narrateur|Un éclat de coquillage tient sur le bord.",
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
    if "ouvre la bouche, maintenant" not in blob:
        raise SystemExit(f"{SID}: manque ouvre la bouche maintenant")
    if "referme la bouche" not in blob:
        raise SystemExit(f"{SID}: manque referme la bouche")
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
        "laisser le temps",
        "on laisse le temps",
        "on peut laisser",
        "n'achève pas",
        "fin de la phrase",
        "tu as laissé",
        "vous avez laissé",
        "tu as su attendre",
        "j'ai attendu",
        "on attend la fin",
        "il faut attendre",
        "on peut attendre",
        "ce n'est pas une faute",
        "on joue",
        "vous jouez",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Aniss cherche un mot. Que fait Nino ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "attendre | laisser le temps | il attend | écouter"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "On n'achève pas à sa place. Que fait Nino ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    if "coquillage" not in blob:
        raise SystemExit(f"{SID}: manque coquillage")
    if "escargot" not in blob:
        raise SystemExit(f"{SID}: manque escargot")
    if "lampe" not in blob:
        raise SystemExit(f"{SID}: manque lampe")
    if "boîte" not in blob and "boite" not in blob:
        raise SystemExit(f"{SID}: manque boîte")
    if "la mer" not in blob:
        raise SystemExit(f"{SID}: manque la mer")
    for ban in (
        "éclat de canapé",
        "éclat d'assiette",
        "éclat d'étal",
        "éclat de plateau",
        "éclat de pupitre",
        "éclat de carotte",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "canapé",
        "assiette",
        "étal",
        "plateau",
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
        "- **Leçon :** DIF.PAR.002 — Aniss cherche un mot, Nino laisse "
        "le temps (vécue : Nino connaît le mot, ouvre la bouche "
        "maintenant, la referme, attend ; Aniss dit escargot, puis la "
        "mer). JAMAIS dite dans le récit. Pas « laisser le temps ». Pas "
        "« on n'achève pas à sa place » hors retry moteur.\n"
        "- **Personnages :** Nino, Aniss, papa, maman. Dump Didier/Jules "
        "→ D16 Nino = enfant-m (veut raconter maintenant, ouvre la "
        "bouche, la referme). Aniss = copain (cherche le mot, j'ai vu, "
        "escargot, la mer). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** salon, lampe, table, boîte, fenêtre, rideau, "
        "coquillage beige, ligne rose. ≠ PAR.002-03 plateau. ≠ "
        "PAR.002-04 étal. ≠ PAR.002-05 assiette. ≠ PAR.002-06 canapé.\n"
        "- **Indice unique :** éclat de coquillage (luit à l'ouverture "
        "→ tremble à la bouche ouverte → luit à l'oreille → tient sur "
        "le bord). BAN éclat de canapé / assiette / étal / plateau.\n"
        "- **Question moteur :** « Aniss cherche un mot. Que fait "
        "Nino ? » expected **attendre**. accepted dump `attendre | "
        "laisser le temps | il attend | écouter`. retry dump adapté "
        "(Didier → Nino). Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La lampe fait un rond chaud. Couvercle, bois sec. Sur le bord, "
        "un éclat de coquillage luit. Nino veut raconter **maintenant**. "
        "Aniss dit j'ai vu, cherche le mot. Nino connaît, ouvre la "
        "bouche maintenant, sourire parti, la referme, pose ses mains. "
        "Papa s'accroupit. Escargot. Merci vécu. Deuxième ruse : "
        "l'oreille, Aniss cherche, Nino ouvre trop vite, referme. La "
        "mer. Un éclat de coquillage tient sur le bord.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon, lampe, table, boîte, fenêtre, coquillage. ≠ "
        "002-03 plateau. ≠ 002-04 étal. ≠ 002-05 assiette. ≠ 002-06 "
        "canapé. Pas merle.\n"
        "- Désir : raconter ce qu'il y a dedans, maintenant.\n"
        "- Objet : coquillage beige, ligne rose, boîte, lampe.\n"
        "- Indice unique : éclat de coquillage, vu dès l'ouverture, "
        "payé sur le bord. Pas éclat de canapé / assiette / étal / "
        "plateau.\n"
        "- Urgence douce : Aniss arrive, cherche le mot, Nino le "
        "connaît.\n"
        "- Imprévu 1 : Nino ouvre la bouche maintenant, le mot pousse, "
        "sourire parti, il referme.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« escargot ».\n"
        "- Imprévu 2 (plus rusé) : l'oreille, Aniss cherche, Nino ouvre "
        "trop vite.\n"
        "- Résolution : il referme, pose les mains, Aniss dit la mer.\n"
        "- Retour : boîte, bois tiède, éclat sur le bord.\n\n"
        "## Vécu\n\n"
        "Nino veut raconter **maintenant**. Impatience, puis bouche "
        "ouverte, sourire parti. Aniss cherche, souffle, trouve. Papa "
        "se baisse, pose une question, ne récite pas la règle. Ils "
        "agissent : bouche refermée, oreille, mer, boîte. Merci vécu. "
        "Fin : l'éclat du début tient sur le bord.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Nino laisse le temps à Aniss (noyau laisse le temps, "
        "prénoms D16). Relance : Que fait Nino ? expected attendre.\n"
        "- Lieu du dump-meta (salon, coquillage). Maman et papa. "
        "Aniss = copain. Nino = héros.\n"
        "- Ouverture inventée (lampe, rond chaud), pas un gabarit v2, "
        "pas « Un coquillage beige repose sur la table basse » du dump, "
        "pas canapé.\n"
        "- Indice unique : éclat de coquillage. BAN éclat de canapé / "
        "assiette / étal / plateau. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » / « déjà » du dump.\n"
        "- Leçon non dite : on la voit quand Nino ouvre, referme, quand "
        "Aniss trouve escargot, puis la mer. Pas « laisser le temps ». "
        "Pas « on n'achève pas » hors retry moteur.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Aniss cherche un mot. Que fait Nino ? ». "
        "expected attendre. dump accepted/retry (Didier → Nino). 5 "
        "chunks, kinds inchangés.\n"
        "- example4 037 / 069 / 001 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_ene_001_09.py`, profiles N1.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers l'oreille.\n"
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
