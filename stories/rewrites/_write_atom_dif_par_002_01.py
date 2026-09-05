#!/usr/bin/env python3
"""ATOM-DIF.PAR.002-01 — Nino finit sa phrase (F-NAR-019, N2, DIF.PAR.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.002-01"
TITLE = "Nino finit sa phrase"
N2 = LIMITS["N2"]
CHARS = "Sarah, Nino, papa, maman"
SETTING = (
    "maison, cuisine, soir, pain, carottes, dessin, "
    "papier, crayon bleu, table, lampe"
)
INDICE = "éclat de carotte"
FIL = (
    "La vitre orange tient le soir. Près du pain, un éclat de "
    "carotte brille. Sarah veut montrer le dessin, maintenant. "
    "Nino cherche un mot. Elle ouvre la bouche trop vite, pousse "
    "le papier. Sourire parti, poitrine, papa accroupi. Elle "
    "refuse de foncer, referme la bouche, attend. Nino finit. "
    "Merci vécu. Deuxième ruse : une voile. Un éclat de carotte "
    "tient près du pain."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(flaque|piquet|portail|rotin|crochet|platane|cageot|résine|"
    r"resine|botte|bottes|limace|perron|chaise|tiroir|fraisier|"
    r"cuivre|buis|cerceau|grille|cour|pierre|nappe|figue|robinet|"
    r"planche|émail|email|samare|bassine|lunettes|corde|drap|"
    r"ballon|entrée|entree|horloge|bol|casserole|soupe|"
    r"chiffon|sauge|lacet|commode|gond|banc|coussin|confiture|"
    r"tartine|fraise|parquet|tapis|camion|seau|sable|pelle|"
    r"gourde|oiseau)\b",
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
    "les trois mots",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "on peut jouer",
    "on peut attendre",
    "on peut demander",
    "on peut laisser le temps",
    "laisser le temps",
    "on attend la fin",
    "on écoute jusqu'au bout",
    "laisse-le finir",
    "laisse le finir",
    "on n'interrompt",
    "on n interrompt",
    "n'interrompt pas",
    "on n'achève pas",
    "finir sa phrase",
    "fin de la phrase",
    "tu as su attendre",
    "vous avez laissé le temps",
    "vous parlez bien",
    "ce n'est pas une faute",
    "n'est pas une faute",
    "pas une faute",
    "vous jouez",
    "on joue",
    "parle peu",
    "elle parle peu",
    "forcer la parole",
    "on ne force pas",
    "regarder, c'est",
    "on n'imite pas",
    "on n imite pas",
    "cherche un mot",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de pin",
    "éclat de pomme",
    "éclat de sève",
    "éclat de seve",
    "éclat de botte",
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
    "éclat de cerceau",
    "éclat d'émail",
    "éclat d'email",
    "éclat de samare",
    "éclat de bassine",
    "éclat de nappe",
    "éclat de farine",
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
    "éclat de pierre",
    "éclat de grille",
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
    "éclat de flaque",
    "éclat de piquet",
    "éclat de portail",
    "éclat de rotin",
    "éclat de crochet",
    "éclat de platane",
    "éclat de cageot",
    "éclat de résine",
    "éclat de resine",
    "éclat de carte",
    "éclat de tapis",
    "éclat de vapeur",
    "éclat de bol",
    "éclat de chiffon",
    "éclat de sauge",
    "éclat de lacet",
    "éclat de commode",
    "éclat de gond",
    "éclat de banc",
    "éclat de parquet",
    "éclat de rond",
    "éclat de table",
    "éclat de pain",
    "éclat de papier",
    "éclat de dessin",
    "éclat de bateau",
    "éclat de sel",
    "éclat d'horloge",
    "éclat d horloge",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de carotte",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_montrer_le_dessin_maintenant; "
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
            "sous_texte=nino_cherche_un_mot_que_fait_sarah; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="bateau",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_ouvre_referme_attend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de carotte",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=voile_trop_vite_elle_referme_la_bouche; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de carotte",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pres_du_pain; "
            "tempo=posé; sourire=léger; respiration=ample"
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
        "pain",
        [
            "narrateur|La vitre orange tient le soir dehors.",
            "narrateur|L'odeur du pain chaud remplit la cuisine.",
            "enfant-f|Ça sent bon, papa.",
            "papa|Tu le sens, le pain, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa coupe des carottes orange.",
            "narrateur|Une rondelle tombe près du pain.",
            "enfant-f|Elle est orange, maman.",
            "maman|Tu la vois, la rondelle ?",
            "enfant-f|Oui, maman.",
            "narrateur|Près du pain, un éclat de carotte brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Maman casse le pain.",
            "narrateur|La croûte craque, tiède.",
            "enfant-f|Elle est tiède.",
            "maman|Tu veux un coin de croûte ?",
            "enfant-f|Oui.",
            "narrateur|Sarah croque.",
            "narrateur|La croûte gratte un peu.",
            "papa|Le pain tient chaud, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|En ce moment, Sarah tient un papier.",
            "narrateur|Un crayon bleu a laissé une trace.",
            "enfant-f|Je veux montrer le dessin, maintenant !",
            "enfant-f|Sur la table, tout de suite.",
            "papa|Le dessin, là ?",
            "enfant-f|Oui, le dessin.",
            "maman|Tes mains tiennent le papier, Sarah ?",
            "enfant-f|Oui, maman.",
            "narrateur|La porte s'ouvre.",
            "narrateur|Nino arrive avec un papier.",
            "narrateur|Le papier tremble entre ses doigts.",
            "enfant-f|Je le montre, maintenant !",
            "narrateur|Sarah prend le papier trop vite.",
            "copain|J'ai fait.",
            "narrateur|Nino s'arrête.",
            "narrateur|Il cherche le mot.",
            "narrateur|Sarah connaît le dessin.",
            "narrateur|C'est un bateau.",
            "narrateur|Les mots montent très vite.",
            "enfant-f|Le bateau !",
            "enfant-f|La voile !",
            "enfant-f|Maintenant !",
            "narrateur|Sarah pousse le papier trop vite.",
            "narrateur|Le papier tape le pain.",
            "enfant-f|Oh.",
            "narrateur|Le dessin glisse vers l'éclat.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Nino, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|Le papier est près du pain, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de carotte tremble, puis tient.",
            "narrateur|Nino baisse les yeux.",
            "enfant-f|Il ne dit plus le mot, papa.",
            "narrateur|Sarah regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino cherche un mot.",
            "narrateur|Que fait Sarah ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "carotte",
        [
            "narrateur|Sarah veut montrer le dessin, tout de suite.",
            "enfant-f|Je le dis, maintenant !",
            "narrateur|Elle ouvre la bouche.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "narrateur|Nino baisse les yeux.",
            "narrateur|Il serre le bord du papier.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le dessin, un instant.",
            "narrateur|Elle écoute le silence de la cuisine.",
            "papa|Tu veux montrer le dessin avec Nino ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Papa, on fait quoi ?",
            "papa|On pose le papier, puis on reste.",
            "enfant-f|D'accord.",
            "narrateur|Sarah reste un moment, les mains ouvertes.",
            "narrateur|Elle attend.",
            "copain|J'ai fait un bateau.",
            "enfant-f|Il est bleu.",
            "narrateur|Nino hoche la tête.",
            "narrateur|Sarah pose le dessin contre le sel.",
            "papa|Merci, Sarah.",
            "narrateur|Papa a vu les deux, à la cuisine.",
            "maman|La croûte est tiède, sous les doigts.",
            "enfant-f|Elle est chaude.",
            "narrateur|Papa donne une rondelle de carotte.",
            "narrateur|Sarah croque.",
            "narrateur|C'est un peu sucré.",
            "narrateur|Nino croque aussi.",
            "enfant-f|Le bateau.",
            "papa|Il a une voile, là ?",
            "enfant-f|Oui, là.",
            "narrateur|Sarah glisse la main sur le papier.",
            "narrateur|Le crayon est lisse, contre la peau.",
            "maman|Tes mains sont au chaud, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Nino pose un doigt sur la voile.",
            "copain|Bleu.",
            "enfant-f|On le laisse sur la table ?",
            "maman|Le pain est près du dessin.",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pain",
        [
            "narrateur|Ils restent près de la table.",
            "narrateur|Nino reprend le papier.",
            "copain|Et il y a.",
            "enfant-f|Une voile, maintenant !",
            "narrateur|Sarah ouvre la bouche trop vite.",
            "narrateur|Nino serre les lèvres.",
            "enfant-f|Oh.",
            "narrateur|Sarah avance les mots, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Sarah refuse de foncer, cette fois.",
            "narrateur|Sa bouche se ferme, puis s'ouvre.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le dessin, un instant.",
            "narrateur|Elle écoute le silence du pain.",
            "narrateur|Près du pain, un éclat de carotte luit.",
            "enfant-f|Là, sur la table.",
            "enfant-f|Tu dis le mot, Nino ?",
            "narrateur|Nino ne dit rien.",
            "narrateur|Il tient le papier, sans parler.",
            "copain|Une voile.",
            "narrateur|Sarah referme la bouche, sans se presser.",
            "narrateur|Nino pose le papier, plus lentement.",
            "narrateur|Le crayon est lisse et tiède.",
            "papa|Tu la vois, la voile ?",
            "enfant-f|Oui, papa.",
            "maman|Le dessin est près du pain ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le bateau tient contre le sel.",
            "narrateur|Sarah pose une main sur le papier.",
            "narrateur|Nino pose la suivante.",
            "papa|Le dessin tient, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|La lampe passe sur le pain.",
            "enfant-f|Elle allume la croûte.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du pain.",
            "maman|Le bateau est arrivé, Sarah ?",
            "enfant-f|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah souffle, un filet d'air.",
            "enfant-f|Le pain sent bon.",
            "maman|Tu le sens, le pain ?",
            "enfant-f|Oui, maman.",
            "papa|La voile reste un peu, bleue.",
            "enfant-f|Elle a tenu, sur le papier.",
            "copain|Bateau.",
            "narrateur|Le pain est chaud, sous les mains.",
            "narrateur|Le dessin bleu fait de l'ombre.",
            "enfant-f|On le montre, après.",
            "narrateur|Un éclat de carotte tient près du pain.",
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
        if not skip_lesson:
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
    if "ouvre la bouche" not in blob:
        raise SystemExit(f"{SID}: manque ouvre la bouche")
    if "referme la bouche" not in blob:
        raise SystemExit(f"{SID}: manque referme la bouche")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Sarah = enfant-f, Nino = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Nino absent (copain)")
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
    if not any(r == "enfant-f" for r in roles):
        raise SystemExit(f"{SID}: enfant-f absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "ce n'est pas une faute",
        "n'est pas une faute",
        "on peut jouer",
        "on peut attendre",
        "on peut demander",
        "on peut laisser le temps",
        "laisser le temps",
        "on attend la fin",
        "on écoute jusqu'au bout",
        "laisse-le finir",
        "on n'interrompt",
        "finir sa phrase",
        "tu as su attendre",
        "on joue",
        "vous jouez",
        "il faut attendre",
        "on doit demander",
        "il faut demander",
        "parle peu",
        "elle parle peu",
        "forcer la parole",
        "cherche un mot",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Nino cherche un mot. Que fait Sarah ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") is not None:
        raise SystemExit(f"{SID}: expected_answer inventé")
    if q.get("accepted_examples") is not None:
        raise SystemExit(f"{SID}: accepted_examples inventé")
    if q.get("retry_prompt") is not None:
        raise SystemExit(f"{SID}: retry inventé")
    if "pain" not in blob:
        raise SystemExit(f"{SID}: manque pain")
    if "carotte" not in blob:
        raise SystemExit(f"{SID}: manque carotte")
    if "dessin" not in blob:
        raise SystemExit(f"{SID}: manque dessin")
    if "crayon" not in blob:
        raise SystemExit(f"{SID}: manque crayon")
    if re.search(r"\bchaise\b", blob):
        raise SystemExit(f"{SID}: BAN chaise")
    if re.search(r"\bplanche\b", blob):
        raise SystemExit(f"{SID}: BAN planche")
    for ban in (
        "éclat de parquet",
        "éclat de banc",
        "éclat de chaise",
        "éclat de planche",
        "éclat de pain",
        "éclat de tapis",
        "tout doux",
        "tout calme",
        "sara ",
        "noé",
        "noe ",
        "chouchou",
        "amir",
        "kenzo",
        "maya",
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
        "- **Leçon :** DIF.PAR.002 — quand l'autre cherche un mot, on attend, "
        "on ne finit pas sa phrase (vécue : bouche ouverte trop vite, papier "
        "sur le pain, sourire parti, elle refuse de foncer, referme la "
        "bouche, attend, Nino dit bateau, puis voile). JAMAIS dite dans le "
        "récit. Pas « laisse-le finir ». Pas « on n'interrompt pas ». Pas "
        "« Nino cherche un mot » hors question moteur.\n"
        "- **Personnages :** Sarah, Nino, papa, maman. Dump Sara/Noé/"
        "Amir/Chouchou → D16. Sarah = enfant-f (veut montrer le dessin "
        "maintenant, aide trop vite, puis referme la bouche). Nino = copain "
        "(cherche un mot, j'ai fait, bateau, voile). Troupe D16. Pas de "
        "maîtresse.\n"
        "- **Lieu :** maison, cuisine, soir, pain, carottes, dessin, papier, "
        "crayon bleu, table, lampe. ≠ PAR.001 salon / tapis / camion. ≠ "
        "dump chaise / nappe / buée-village.\n"
        "- **Indice unique :** éclat de carotte (brille à l'ouverture près "
        "du pain sous la lampe, papa coupe → tremble au papier trop vite → "
        "luit au refus voile → tient près du pain). BAN éclat de parquet "
        "(PAR.001-01) / banc / chaise / planche / pain.\n"
        "- **Question moteur :** « Nino cherche un mot. Que fait Sarah ? » "
        "expected / accepted / retry **null** (dump, non inventés). Non "
        "récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La vitre orange tient le soir. Près du pain, un éclat de carotte "
        "brille. Papa coupe, croûte tiède. Sarah veut montrer le dessin "
        "**maintenant**. Nino arrive, le papier tremble. Il dit : j'ai "
        "fait. Il cherche le mot. Sarah pousse trop vite, le papier tape "
        "le pain. Sourire parti. Papa s'accroupit. Elle refuse de foncer. "
        "Elle ouvre la bouche, la referme, attend. Nino dit : un bateau. "
        "Merci vécu. Deuxième ruse : une voile, trop vite. Elle s'arrête, "
        "lit l'éclat. Un éclat de carotte tient près du pain.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : maison, cuisine, soir, pain, carottes, dessin, lampe. "
        "≠ PAR.001 parquet / tapis / camion. ≠ dump chaise / planche.\n"
        "- Désir : montrer le dessin, maintenant, sur la table.\n"
        "- Objet : papier, crayon bleu, bateau, voile, pain, carotte.\n"
        "- Indice unique : éclat de carotte, vu dès l'ouverture près du "
        "pain, payé près du pain. Pas éclat de parquet / chaise / planche.\n"
        "- Urgence douce : Nino arrive, Sarah accélère les mots.\n"
        "- Imprévu 1 : Sarah pousse trop vite, le papier tape le pain. "
        "Nino baisse les yeux, le mot s'arrête.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : Nino reprend, « et il y a », Sarah "
        "ouvre trop vite pour la voile.\n"
        "- Résolution : elle refuse de foncer, observe, écoute, referme, "
        "attend, Nino finit.\n"
        "- Retour : voile bleue, pain chaud, éclat près du pain.\n\n"
        "## Vécu\n\n"
        "Sarah veut montrer le dessin **maintenant**. Impatience, puis "
        "papier qui glisse, sourire parti. Nino pose sa limite (yeux "
        "bas, mot coupé, bateau, voile). Papa se baisse, pose une "
        "question, ne récite pas la règle. Elle agit : ouvrir, refermer, "
        "attendre. Merci vécu. Fin : l'éclat du début tient près du pain.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Nino finit sa phrase (noyau dump, prénoms D16). "
        "Relance : Que fait Sarah ? expected null.\n"
        "- Lieu du dump (cuisine, soir, pain, carottes, dessin) sans "
        "chaise / planche. Maman présente. Nino = copain.\n"
        "- Ouverture inventée (vitre orange, soir), pas un gabarit "
        "v2, pas « La buée dessine des ronds » du dump en première "
        "ligne.\n"
        "- Indice unique : éclat de carotte. BAN éclat de parquet / "
        "banc / chaise / planche / pain. Pas tache/flèche/marque/"
        "symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doucement » / « encore » / « chaise » "
        "du dump.\n"
        "- Leçon non dite : on la voit quand le papier tape le pain, "
        "quand Sarah referme la bouche, quand Nino dit bateau, puis "
        "voile. Pas « laisse-le finir ». Pas « Nino cherche un mot » "
        "hors question.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Nino cherche un mot. Que fait Sarah ? ». "
        "expected / accepted / retry laissés null. 5 chunks, kinds "
        "inchangés.\n"
        "- example4 031 / 063 / 095 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_par_001_01.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers la voile.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
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
