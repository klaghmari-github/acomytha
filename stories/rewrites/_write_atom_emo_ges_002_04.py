#!/usr/bin/env python3
"""ATOM-EMO.GES.002-04 — Sarah souffle et fait une pause (F-NAR-019, N2, EMO.GES.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.002-04"
TITLE = "Sarah souffle et fait une pause"
N2 = LIMITS["N2"]
CHARS = "Sarah, papa, maman"
SETTING = (
    "cuisine, table, pâte, rouleau, bois, fenêtre, rayon, "
    "beurre, moule, formes"
)
INDICE = "éclat de rouleau"
FIL = (
    "Le bois du rouleau luit près de la fenêtre. Près du bois, "
    "un éclat de rouleau brille. Sarah veut coller, maintenant. "
    "Forme cassée, poitrine trop vite, sourire parti, papa "
    "accroupi. Elle souffle, pause. Merci vécu. 2e ruse : le "
    "cœur se plie sous le rouleau. Un éclat de rouleau tient "
    "sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(farine|pot|comptoir|cubes|château|chateau|tapis|coussin|"
    r"canapé|canape|lampe|toboggan|balançoire|balancoire|rideau|"
    r"banc|sable|seau|parc|portail|gouttière|gouttiere|cabane|"
    r"thé|tasse|plateau|cacao|dessin|livre|horloge|parquet|"
    r"chaise|tiroir|nappe|drap|ballon|entrée|entree|casserole|"
    r"soupe|carotte|chiffon|commode|gond|confiture|fraise|"
    r"camion|pupitre|rambarde|pelle|gourde|flaque|piquet|"
    r"rotin|crochet|platane|cageot|résine|resine|botte|bottes|"
    r"limace|perron|fraisier|cuivre|buis|cerceau|grille|cour|"
    r"pierre|figue|robinet|planche|émail|email|samare|bassine|"
    r"lunettes|corde|sauge|lacet|plaid|savon|jardin|terre|"
    r"pain|bol|tour)\b",
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
    "on peut souffler",
    "tu peux souffler",
    "tu as soufflé",
    "tu as souffle",
    "tu as fait une pause",
    "souffler, puis une pause",
    "on peut faire une pause",
    "tu peux faire une pause",
    "ton corps ralentit",
    "souffle comme le vent",
    "on peut reprendre",
    "c'est le bon geste",
    "tu as repris le geste",
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
    "éclat d'horloge",
    "éclat d horloge",
    "éclat de pupitre",
    "éclat de rambarde",
    "éclat de parquet",
    "éclat de verre",
    "éclat de cacao",
    "éclat de dessin",
    "éclat de table",
    "éclat de plateau",
    "éclat de toboggan",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de rideau",
    "éclat de canapé",
    "éclat de canape",
    "éclat de lampe",
    "éclat de livre",
    "éclat d'assiette",
    "éclat d assiette",
    "éclat de coquillage",
    "éclat de cabane",
    "éclat de thé",
    "éclat de the",
    "éclat de pot",
    "éclat de tour",
    "éclat de comptoir",
    "éclat de plaid",
    "éclat de savon",
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
        emphasis="éclat de rouleau",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis gêne; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_coller_maintenant; "
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
            "sous_texte=le_corps_de_sarah_va_vite_que_fait_elle; "
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
            "emotion=gêne puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_souffle_elle_fait_une_pause; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de rouleau",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=coeur_plie_sous_le_rouleau_elle_souffle; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de rouleau",
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
    "accepted_examples": (
        "souffler | pause | une pause | s'asseoir | respirer"
    ),
    "retry_prompt": "Papa dit de souffler. Que fait Sarah ensuite ?",
    "engine_ok_text": "Oui, souffler.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "cuisine,pate",
        [
            "narrateur|Le bois du rouleau luit près de la fenêtre.",
            "narrateur|Ça sent le beurre, un peu.",
            "enfant-f|Ça sent bon, papa.",
            "papa|Tu le sens, le beurre, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un rayon glisse sur le bois.",
            "enfant-f|Il brille, maman.",
            "maman|Le rouleau est lisse ?",
            "enfant-f|Un peu, maman.",
            "maman|La pâte attend sur la table.",
            "papa|On colle des formes, d'accord ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un fil de pâte pend vers le bois.",
            "enfant-f|Il pend, papa.",
            "papa|Tu le vois, le fil ?",
            "enfant-f|Oui.",
            "narrateur|La pâte est froide contre la peau.",
            "enfant-f|Elle colle, maman.",
            "maman|Tu la sens, la pâte ?",
            "enfant-f|Oui.",
            "narrateur|Près du bois, un éclat de rouleau brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Une poussière danse au-dessus du bois.",
            "enfant-f|Elle vole, maman.",
            "maman|Au-dessus du rouleau ?",
            "enfant-f|Oui, au-dessus.",
            "narrateur|Papa pose le moule près de la pâte.",
            "narrateur|Le moule est un peu lourd.",
            "enfant-f|On colle l'étoile, papa ?",
            "narrateur|Le saladier tape le bois.",
            "narrateur|La pâte s'étale un peu.",
            "enfant-f|C'est blanc, papa.",
            "papa|Comme un nuage ?",
            "enfant-f|Oui, comme un nuage.",
            "narrateur|En ce moment, Sarah appuie le moule sur la pâte.",
            "enfant-f|Je veux coller, maintenant !",
            "enfant-f|L'étoile, tout de suite.",
            "papa|Tu vois le moule, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah appuie trop fort.",
            "narrateur|La pâte se déchire.",
            "narrateur|La forme se casse.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules montent un peu.",
            "papa|Elle casse, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|Tes lèvres sont serrées, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de rouleau tremble, puis tient.",
            "narrateur|Sarah serre le moule contre elle.",
            "enfant-f|C'est trop, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Sarah regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Le corps de Sarah va vite.",
            "narrateur|Que fait-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "cuisine,pate",
        [
            "narrateur|Sarah veut coller, tout de suite.",
            "enfant-f|Je colle, maintenant !",
            "narrateur|Elle appuie trop vite sur la pâte.",
            "narrateur|Le moule déchire la forme.",
            "narrateur|Sarah baisse les yeux.",
            "narrateur|Sa poitrine est coincée.",
            "enfant-f|C'est trop.",
            "narrateur|Sarah souffle, un filet d'air.",
            "narrateur|Une fois.",
            "narrateur|Deux fois.",
            "narrateur|Elle fait une pause.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le rouleau, un instant.",
            "narrateur|Elle écoute le silence de la cuisine.",
            "papa|Tu veux coller l'étoile ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Papa, on fait quoi ?",
            "papa|On laisse un peu d'air ?",
            "enfant-f|D'accord.",
            "narrateur|Sarah reste un moment, les mains ouvertes.",
            "narrateur|Elle souffle, plus loin.",
            "narrateur|La pâte s'arrête de bouger.",
            "enfant-f|L'étoile.",
            "enfant-f|J'aime l'étoile.",
            "narrateur|Maman pose le moule sur la table.",
            "papa|Merci, Sarah.",
            "narrateur|Papa reste près du bois.",
            "maman|La pâte est tiède, sous les doigts.",
            "enfant-f|Elle est froide.",
            "narrateur|La forme tient, un peu de travers.",
            "enfant-f|L'étoile.",
            "papa|Elle a cinq branches, là ?",
            "enfant-f|Oui, là.",
            "narrateur|Sarah glisse la main près du rouleau.",
            "narrateur|Le bois est lisse, contre la peau.",
            "maman|Tes mains sont au chaud, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Sarah s'assoit, puis se relève.",
            "enfant-f|On la pose au bord ?",
            "maman|La pâte va jusqu'à la plaque.",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "cuisine",
        [
            "narrateur|Ils restent près de la table.",
            "narrateur|La pâte tombe d'un côté.",
            "enfant-f|Le cœur, maintenant !",
            "narrateur|Sarah appuie le moule trop vite.",
            "narrateur|La forme colle au bois.",
            "enfant-f|Elle part !",
            "narrateur|Le cœur se plie, sous le rouleau.",
            "narrateur|La pâte tire trop fort, cette fois.",
            "enfant-f|Oh.",
            "narrateur|Sarah souffle, un filet d'air.",
            "narrateur|Elle fait une pause, sous le rayon.",
            "narrateur|Sarah avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Sarah souffle, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le bois, un instant.",
            "narrateur|Elle écoute le silence de la cuisine.",
            "narrateur|Au bord du bois, un éclat de rouleau luit.",
            "enfant-f|Là, sur le rouleau.",
            "enfant-f|Tu veux le cœur, maman ?",
            "narrateur|Maman ne presse plus.",
            "narrateur|Elle tend le moule, sans serrer.",
            "maman|Je prends le cœur.",
            "narrateur|Sarah étale la pâte, sans se presser.",
            "narrateur|Maman la reçoit, plus loin.",
            "narrateur|La pâte est lisse et froide.",
            "papa|Tu le vois, le cœur ?",
            "enfant-f|Oui, papa.",
            "maman|La forme est près de la plaque ?",
            "enfant-f|Oui, maman.",
            "narrateur|Maman pose un bord.",
            "narrateur|Sarah pose une main sur le bois.",
            "papa|La forme tient, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|Un rayon passe sur le rouleau.",
            "enfant-f|Il allume le bois.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la table.",
            "maman|L'étoile est arrivée, Sarah ?",
            "enfant-f|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah souffle, un filet d'air.",
            "enfant-f|La pâte sent le beurre.",
            "maman|Tu le sens, le beurre ?",
            "enfant-f|Oui, maman.",
            "papa|La forme reste un peu, de travers.",
            "enfant-f|Elle a tenu, sur la plaque.",
            "maman|La plaque.",
            "narrateur|La pâte est froide, sous les mains.",
            "narrateur|Le rouleau de bois fait de l'ombre.",
            "enfant-f|On y retourne, après.",
            "narrateur|Un éclat de rouleau tient sur le bois.",
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
    if "souffle" not in blob:
        raise SystemExit(f"{SID}: manque souffle")
    if "pause" not in blob:
        raise SystemExit(f"{SID}: manque pause")
    if "poitrine" not in blob:
        raise SystemExit(f"{SID}: manque poitrine")
    if "accroupit" not in blob:
        raise SystemExit(f"{SID}: manque accroupit")
    if "plie" not in blob:
        raise SystemExit(f"{SID}: manque 2e ruse (cœur plié)")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Sarah = enfant-f)")
    if "copine|" in blob or "copain|" in blob:
        raise SystemExit(f"{SID}: copain/copine (troupe = Sarah, papa, maman)")
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
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on peut souffler",
        "tu peux souffler",
        "tu as soufflé",
        "tu as fait une pause",
        "souffler, puis une pause",
        "on peut faire une pause",
        "ton corps ralentit",
        "souffle comme le vent",
        "bravo",
        "c'est le bon geste",
        "tu as repris le geste",
        "on doit souffler",
        "il faut souffler",
        "il faut faire une pause",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Le corps de Sarah va vite. Que fait-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "souffler":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "souffler | pause | une pause | s'asseoir | respirer"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Papa dit de souffler. Que fait Sarah ensuite ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    if "pâte" not in blob and "pate" not in blob:
        raise SystemExit(f"{SID}: manque pâte")
    if "rouleau" not in blob:
        raise SystemExit(f"{SID}: manque rouleau")
    if "cuisine" not in blob:
        raise SystemExit(f"{SID}: manque cuisine")
    if "table" not in blob:
        raise SystemExit(f"{SID}: manque table")
    if "coller" not in blob:
        raise SystemExit(f"{SID}: manque coller (désir)")
    if "maintenant" not in blob:
        raise SystemExit(f"{SID}: manque maintenant")
    for ban in (
        "éclat de pot",
        "éclat de tour",
        "éclat de comptoir",
        "éclat de farine",
        "farine",
        "tout doux",
        "tout calme",
        "paloma",
        "mila",
        "zélie",
        "zelie",
        "chouchou",
        "nino",
        "aniss",
        "comptoir",
        "cubes",
    ):
        if ban in blob:
            raise SystemExit(f"{SID}: BAN {ban}")
    for ban in ("pot", "tour"):
        if re.search(rf"\b{ban}\b", blob):
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
        "- **Leçon :** EMO.GES.002 — corps trop vite → souffler, pause "
        "(vécue : Sarah veut coller **maintenant**, forme cassée, "
        "poitrine trop vite, sourire parti, papa accroupi ; elle "
        "souffle, fait une pause ; 2e ruse : le cœur se plie sous le "
        "rouleau). JAMAIS dite dans le récit. Pas « on peut souffler ». "
        "Pas « tu as fait une pause ». Pas « souffler, puis une pause ».\n"
        "- **Personnages :** Sarah, papa, maman. Dump Paloma/papa → D16. "
        "Sarah = enfant-f (veut coller maintenant, trop vite, puis "
        "souffle et fait une pause). Troupe D16. Pas de maîtresse. "
        "Pas de copain.\n"
        "- **Lieu :** cuisine, table, pâte, rouleau, bois, fenêtre, "
        "rayon, beurre, moule, formes. ≠ 002-01 tour / cubes. ≠ 002-02 "
        "comptoir / pain. ≠ 002-03 pot / jardin. ≠ dump farine.\n"
        "- **Indice unique :** éclat de rouleau (brille à l'ouverture "
        "près du bois → tremble quand la forme casse → luit au refus "
        "sous le cœur plié → tient sur le bois). BAN éclat de pot / "
        "tour / comptoir / farine.\n"
        "- **Question moteur :** « Le corps de Sarah va vite. Que "
        "fait-elle ? » expected dump **souffler**. accepted dump "
        "`souffler | pause | une pause | s'asseoir | respirer`. retry "
        "dump (Paloma → Sarah). expected/accepted/retry des autres "
        "chunks restent **null**. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le bois du rouleau luit près de la fenêtre. Près du bois, un "
        "éclat de rouleau brille. Fil de pâte, beurre, rayon. Sarah "
        "veut coller **maintenant**. Elle appuie trop fort. Forme "
        "cassée. Sourire parti. Papa s'accroupit. Elle souffle, fait "
        "une pause. Merci vécu. Deuxième ruse : cœur trop vite, forme "
        "pliée sous le rouleau. Elle s'arrête, lit l'éclat. Un éclat "
        "de rouleau tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine, table, pâte, rouleau, bois, fenêtre, rayon, "
        "beurre. ≠ dump farine. ≠ pot / tour / comptoir.\n"
        "- Désir : coller maintenant, une étoile dans la pâte.\n"
        "- Objet : pâte, rouleau, moule, formes, plaque.\n"
        "- Indice unique : éclat de rouleau, vu dès l'ouverture près "
        "du bois, payé sur le bois. Pas éclat de farine.\n"
        "- Urgence douce : Sarah accélère, appuie trop.\n"
        "- Imprévu 1 : le moule déchire la pâte. Poitrine trop vite, "
        "sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : cœur trop vite, forme pliée sous "
        "le rouleau.\n"
        "- Résolution : elle souffle, fait une pause, observe, écoute, "
        "retrouve l'éclat, reprend sans se presser.\n"
        "- Retour : forme de travers, beurre, éclat sur le bois.\n\n"
        "## Vécu\n\n"
        "Sarah veut coller **maintenant**. Impatience, puis forme "
        "cassée, sourire parti. Papa se baisse, pose une question, ne "
        "récite pas la règle. Elle agit : souffle, pause. Merci vécu. "
        "Fin : l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Sarah souffle et fait une pause (noyau + D16). "
        "Relance : Que fait-elle ? expected souffler.\n"
        "- Lieu du dump (cuisine, pâte, formes) sans farine / pot / "
        "tour / comptoir. Papa et maman présents.\n"
        "- Ouverture inventée (bois du rouleau près de la fenêtre), "
        "pas un gabarit v2, pas « Dans la cuisine, un rayon traverse "
        "la farine » du dump en première ligne.\n"
        "- Indice unique : éclat de rouleau. BAN éclat de pot / tour / "
        "comptoir / farine. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip farine / « On peut souffler » / « Bravo » du "
        "dump. Une phrase par ligne, ponctuation, pas de puces.\n"
        "- Leçon non dite : on la voit quand Sarah souffle, fait une "
        "pause. Pas « on peut souffler ». Pas « tu as fait une pause ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Le corps de Sarah va vite. Que "
        "fait-elle ? ». expected souffler. retry dump (Sarah). 5 "
        "chunks, kinds inchangés. expected/accepted/retry null hors Q.\n"
        "- example4 049 / 081 / 013 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_001_04.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le cœur plié.\n"
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
