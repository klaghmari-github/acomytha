#!/usr/bin/env python3
"""ATOM-DIF.ENE.001-01 — Le cerceau sur les flaques (F-NAR-019, N2, DIF.ENE.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.ENE.001-01"
TITLE = "Le cerceau sur les flaques"
N2 = LIMITS["N2"]
CHARS = "Chouchou, Raphaël, papa, maman"
SETTING = "cour d'école après la pluie, grille, flaque, cerceau jaune, bottes, bac d'eau"
INDICE = "éclat de flaque"
FIL = (
    "Une goutte pend sous la grille. Près des bottes, un "
    "éclat de flaque brille. Chouchou veut le cerceau, "
    "maintenant. Raphaël saute, trop vite. Le cerceau part. "
    "Sourire parti. Elle refuse de foncer. Merci vécu. File "
    "des balles, il veut passer. Elle s'arrête, il souffle. "
    "Ils versent l'eau. Un éclat de flaque tient près des bottes."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(limace|perron|chaise|tiroir|fraisier|cuivre|buis|coussin|"
    r"figue|robinet|planche|émail|email|samare|bassine|résine|resine|"
    r"cageot|platane|crochet|rotin|portail|lunettes|corde|pin|"
    r"entrée|entree|maîtresse|maitresse)\b",
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
    "ce n'est pas une faute",
    "ce n est pas une faute",
    "pas une faute",
    "on peut jouer",
    "on peut attendre",
    "on peut demander",
    "demander à un adulte",
    "demander a un adulte",
    "beaucoup d'énergie",
    "beaucoup d'energie",
    "beaucoup d energie",
    "léa",
    "lea",
    "nino",
    "sarah",
    "vous jouez",
    "on joue",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de cerceau",
    "éclat de grille",
    "éclat de cour",
    "éclat de botte",
    "éclat de pierre",
    "éclat de plaque",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de tiroir",
    "éclat de fraisier",
    "éclat de chaise",
    "éclat de perron",
    "éclat de limace",
    "éclat de résine",
    "éclat de resine",
    "éclat de cageot",
    "éclat de platane",
    "éclat de crochet",
    "éclat de rotin",
    "éclat de portail",
    "éclat de piquet",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de pin",
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
        emphasis="éclat de flaque",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_cerceau_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="énergie",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=raphael_bouge_trop_vite_que_peut_on_faire; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="bac",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_refuse_va_au_bac_avec_lui; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de flaque",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_il_souffle_ils_versent; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de flaque",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pres_des_bottes; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer",
    "accepted_examples": "jouer | attendre | un adulte | demander",
    "retry_prompt": (
        "On peut jouer, attendre, ou demander à un adulte. Que fait Sarah ?"
    ),
    "engine_ok_text": "Oui, jouer.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc",
        [
            "narrateur|Une goutte pend sous la grille.",
            "narrateur|Elle tombe dans la flaque, claire et ronde.",
            "enfant-f|Elle a fait plouf !",
            "papa|Tu l'as vue, Chouchou ?",
            "enfant-f|Oui, papa.",
            "narrateur|La grille goutte, un peu, après la pluie.",
            "enfant-f|Ça sent les feuilles, maman.",
            "maman|Tes bottes sont mouillées, Chouchou ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Près des bottes, un éclat de flaque brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, près des bottes ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Un cerceau jaune s'appuie contre le mur.",
            "narrateur|Le plastique est froid, un peu mouillé.",
            "enfant-f|Il est froid, maman.",
            "maman|Le cerceau attend contre le mur ?",
            "enfant-f|Oui, maman.",
            "narrateur|Un bac d'eau reste près du mur.",
            "enfant-f|Le bac est plein.",
            "papa|L'eau du bac, Chouchou ?",
            "enfant-f|Elle brille aussi.",
            "enfant-f|Je veux le cerceau, maintenant !",
            "papa|Sur la flaque ?",
            "enfant-f|Oui, tout de suite.",
            "maman|Avec tes bottes ?",
            "enfant-f|Oui, maman.",
            "narrateur|En ce moment, Chouchou tend la main.",
            "narrateur|Le cerceau glisse un peu, trop lourd.",
            "enfant-f|Il est lourd !",
            "papa|Tu le tiens, Chouchou ?",
            "enfant-f|Oui, papa.",
            "narrateur|Raphaël arrive dans la cour.",
            "narrateur|Ses chaussures tapent le sol.",
            "copain|J'arrive !",
            "enfant-f|Raphaël !",
            "narrateur|Il saute sur place, trop vite.",
            "copain|Le cerceau !",
            "enfant-f|Moi, le cerceau, maintenant !",
            "narrateur|Raphaël prend le cerceau jaune.",
            "narrateur|Il le fait tourner trop vite.",
            "narrateur|Le cerceau part vers la flaque.",
            "enfant-f|Il part !",
            "copain|Oh.",
            "narrateur|Le cerceau tombe dans l'eau.",
            "narrateur|Ça fait un bruit mou.",
            "enfant-f|Il est tombé !",
            "narrateur|L'éclat de flaque tremble, puis tient.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Raphaël, Chouchou ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains sont mouillées, Chouchou ?",
            "enfant-f|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Raphaël a de l'énergie.",
            "narrateur|Que peut-on faire ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "enfants_parc",
        [
            "narrateur|Chouchou veut le cerceau, tout de suite.",
            "enfant-f|Je le prends, maintenant !",
            "narrateur|Elle avance trop vite vers Raphaël.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copain|Attends.",
            "narrateur|Raphaël saute, trop près de l'eau.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Chouchou refuse de foncer.",
            "narrateur|Elle referme les mains.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le cerceau, un instant.",
            "narrateur|Elle écoute la grille qui goutte.",
            "papa|Tu veux le cerceau avec Raphaël ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|On va au bac ?",
            "maman|On marche jusqu'au bac ?",
            "enfant-f|Oui, maman.",
            "papa|Viens, Raphaël.",
            "copain|J'y vais.",
            "narrateur|Ils marchent vers le bac.",
            "narrateur|Les bottes font un bruit mou.",
            "enfant-f|L'eau, papa.",
            "papa|Tu poses les mains ?",
            "enfant-f|Oui.",
            "narrateur|Chouchou pose les mains sur le bac.",
            "narrateur|L'eau est froide.",
            "narrateur|Raphaël pose les mains aussi.",
            "copain|Elle est froide.",
            "narrateur|Il souffle.",
            "papa|Merci, Chouchou.",
            "narrateur|Papa a vu les deux, près du bac.",
            "maman|L'eau coule un peu, sous les doigts.",
            "enfant-f|Elle est froide.",
            "narrateur|Raphaël pose le cerceau, sans se presser.",
            "copain|À toi.",
            "enfant-f|D'accord.",
            "narrateur|Chouchou fait tourner le cerceau.",
            "narrateur|Le cerceau passe près des flaques.",
            "enfant-f|Il tourne !",
            "copain|Oui.",
            "papa|Tu le vois, le rond jaune ?",
            "enfant-f|Oui, papa.",
            "maman|Tes bottes sont au sec ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le ventre de Chouchou se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près du bac ?",
            "enfant-f|Oui.",
            "maman|Tes mains sont froides ?",
            "enfant-f|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "enfants_parc",
        [
            "narrateur|Maman pose des balles près du bac.",
            "enfant-f|Une file, maintenant !",
            "narrateur|Raphaël veut passer, trop vite.",
            "narrateur|Il saute vers les balles.",
            "copain|Moi d'abord !",
            "narrateur|Chouchou avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Chouchou refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe les balles, un instant.",
            "narrateur|Elle écoute la grille qui goutte.",
            "narrateur|Près des bottes, un éclat de flaque luit.",
            "enfant-f|Là, près des bottes.",
            "enfant-f|Tu restes, Raphaël ?",
            "narrateur|Raphaël ne dit rien.",
            "narrateur|Il souffle, sans parler.",
            "copain|Oui.",
            "narrateur|Il reste derrière elle.",
            "enfant-f|Une balle, maman ?",
            "maman|La rouge, Chouchou.",
            "narrateur|Chouchou lance vers le panier.",
            "narrateur|Le panier fait un petit toc.",
            "copain|À moi.",
            "narrateur|Raphaël lance à son tour.",
            "papa|Tu as soufflé, Raphaël ?",
            "copain|Un peu.",
            "maman|Le bac est plein, Chouchou ?",
            "enfant-f|On verse ?",
            "papa|Vous versez ensemble ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ils versent l'eau du bac.",
            "narrateur|L'eau rejoint la flaque, sans bruit.",
            "enfant-f|Elle part.",
            "copain|Elle part.",
            "maman|Le cerceau a une goutte, Chouchou ?",
            "enfant-f|Sur le bord.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la flaque.",
            "narrateur|Maman essuie un peu d'eau.",
            "enfant-f|On a versé l'eau, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-f|Oui, dans la flaque.",
            "maman|On est bien, ici.",
            "narrateur|Chouchou tapote le cerceau du doigt.",
            "enfant-f|Il a une goutte, maman.",
            "maman|Tu la vois, la goutte ?",
            "enfant-f|Oui, maman.",
            "papa|Le cerceau est resté, Chouchou.",
            "enfant-f|Oui, avec Raphaël.",
            "copain|Le cerceau est resté.",
            "narrateur|Ça sent la pluie, un peu tiède.",
            "enfant-f|Et la grille, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|Les bottes restent près de l'eau.",
            "narrateur|Un éclat de flaque tient près des bottes.",
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
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Chouchou = enfant-f, Raphaël = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent (copain)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "enfant-f|" not in blob:
        raise SystemExit(f"{SID}: Chouchou absente (enfant-f)")
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
        "ce n'est pas une faute",
        "pas une faute",
        "on peut jouer",
        "on peut attendre",
        "on peut demander",
        "demander à un adulte",
        "beaucoup d'énergie",
        "beaucoup d'energie",
        "on joue",
        "vous jouez",
        "un adulte",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Raphaël a de l'énergie. Que peut-on faire ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != "jouer | attendre | un adulte | demander":
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "On peut jouer, attendre, ou demander à un adulte. Que fait Sarah ?":
        raise SystemExit(f"{SID}: retry dump altéré: {retry}")
    copain_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    ).lower()
    if "attends" not in copain_txt:
        raise SystemExit(f"{SID}: Raphaël sans attends")
    if "souffle" not in blob:
        raise SystemExit(f"{SID}: manque souffle")
    if "bac" not in blob:
        raise SystemExit(f"{SID}: manque bac")
    if "cerceau" not in blob:
        raise SystemExit(f"{SID}: manque cerceau")
    if "bottes" not in blob and "botte" not in blob:
        raise SystemExit(f"{SID}: manque bottes")
    if "grille" not in blob:
        raise SystemExit(f"{SID}: manque grille")
    if "versent" not in blob and "verse" not in blob:
        raise SystemExit(f"{SID}: manque verser l'eau")
    for ban in (
        "éclat de cerceau",
        "éclat de grille",
        "éclat de cour",
        "éclat de botte",
        "éclat de pierre",
        "éclat de plaque",
        "éclat de cuivre",
        "éclat de buis",
        "éclat de tiroir",
        "éclat de fraisier",
        "éclat de chaise",
        "éclat de perron",
        "éclat de limace",
        "éclat de résine",
        "éclat de cageot",
        "éclat de platane",
        "éclat de crochet",
        "éclat de rotin",
        "éclat de portail",
        "tout doux",
        "tout calme",
        "léa",
        "nino",
        "sarah",
        "maîtresse",
        "maitresse",
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
        "- **Leçon :** DIF.ENE.001 — beaucoup d'énergie n'est pas une faute ; "
        "on peut jouer, attendre, ou demander à un adulte (vécue : cerceau "
        "qui part, sourire parti, bac, file, souffle). JAMAIS dite dans le "
        "récit.\n"
        "- **Personnages :** Chouchou, Raphaël, papa, maman. Dump-meta Léa/"
        "Nino → D16. Chouchou = enfant-f (veut le cerceau maintenant). "
        "Raphaël = copain (saute, trop vite). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** cour d'école après la pluie, grille qui goutte, flaque, "
        "cerceau jaune, bottes, bac d'eau. Monde xlsx.\n"
        "- **Indice unique :** éclat de flaque (brille près des bottes à "
        "l'ouverture → tremble quand le cerceau part → luit à la file → "
        "tient près des bottes). BAN éclat de cerceau / grille / cour / "
        "botte / pierre / plaque + COR (cuivre, buis, tiroir, fraisier, "
        "chaise, perron, limace, résine, cageot, platane, crochet, rotin, "
        "portail).\n"
        "- **Question moteur :** « Raphaël a de l'énergie. Que peut-on "
        "faire ? » expected **jouer**. accepted jouer | attendre | un "
        "adulte | demander. Retry dump. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte pend sous la grille. Près des bottes, un éclat de "
        "flaque brille. Cerceau jaune, bac, bottes. Chouchou veut le "
        "cerceau **maintenant**. Raphaël saute, trop vite : le cerceau "
        "part. Sourire parti. Papa s'accroupit. Elle refuse de foncer. "
        "Elle demande le bac. Merci vécu. Deuxième ruse : file des balles, "
        "il veut passer. Elle s'arrête, il souffle. Ils versent l'eau. Un "
        "éclat de flaque tient près des bottes.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cour d'école après la pluie, grille, flaque, cerceau "
        "jaune, bottes, bac d'eau.\n"
        "- Désir : le cerceau, maintenant, sur la flaque.\n"
        "- Objet : cerceau jaune, balles, bac, bottes.\n"
        "- Indice unique : éclat de flaque, vu dès l'ouverture près des "
        "bottes, payé près des bottes. Pas éclat de cerceau / grille / "
        "cour / botte.\n"
        "- Urgence douce : Raphaël arrive, Chouchou accélère.\n"
        "- Imprévu 1 : Raphaël tourne trop vite, le cerceau part dans "
        "l'eau.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le bac.\n"
        "- Imprévu 2 (plus rusé) : file des balles, il veut passer, elle "
        "avance trop vite puis s'arrête.\n"
        "- Résolution : elle refuse de foncer, observe, écoute la grille, "
        "retrouve l'éclat, il souffle, ils versent.\n"
        "- Retour : goutte sur le cerceau, éclat près des bottes.\n\n"
        "## Vécu\n\n"
        "Chouchou veut le cerceau **maintenant**. Impatience, puis cerceau "
        "qui part, sourire parti. Raphaël prend son élan, pose sa limite "
        "(attends, silence, souffle). Papa se baisse, pose une question, "
        "ne récite pas la règle. Ils agissent : bac, file, eau versée. "
        "Merci vécu. Fin : l'éclat du début tient près des bottes.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le cerceau sur les flaques (noyau dump). Relance : "
        "Que peut-on faire ? expected jouer.\n"
        "- Lieu du dump (cour d'école après la pluie). Maman et papa. "
        "Chouchou = enfant-f (dump script la mettait enfant-m par erreur "
        "via Raphaël). Raphaël = copain. Léa/Nino dump-meta retirés.\n"
        "- Ouverture inventée (goutte sous la grille), pas un gabarit v2, "
        "pas « Un oiseau secoue une branche près du portail » du dump.\n"
        "- Indice unique : éclat de flaque. BAN éclat de cerceau / grille "
        "/ cour / botte / pierre / plaque + COR. Pas tache/flèche/marque/"
        "symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » / « ce n'est pas une "
        "faute » du dump.\n"
        "- Leçon non dite : on la voit quand le cerceau part, quand elle "
        "refuse de foncer, quand ils vont au bac, quand il souffle dans "
        "la file. Pas « ce n'est pas une faute ». Pas « on peut jouer / "
        "attendre / demander ». Pas « beaucoup d'énergie » en slogan.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Raphaël a de l'énergie. Que "
        "peut-on faire ? ». expected jouer. Retry dump. 5 chunks, kinds "
        "inchangés.\n"
        "- example4 015 / 047 / 079 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_cor_003_02.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers la file.\n"
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
