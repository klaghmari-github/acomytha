#!/usr/bin/env python3
"""ATOM-EMO.GES.001-02 — Sarah dit stop, puis encore (F-NAR-019, N3, EMO.GES.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.001-02"
TITLE = "Sarah dit stop, puis encore"
N3 = LIMITS["N3"]
CHARS = "Sarah, Aniss, papa, maman"
SETTING = (
    "maison, rideau, fenêtre, linge, soleil, bois, "
    "jardin, herbe, porte, fleurs, panier"
)
INDICE = "éclat de rideau"
FIL = (
    "Le linge tiède bouge devant le jardin. Près du tissu, "
    "un éclat de rideau brille. Sarah veut la ronde maintenant. "
    "Aniss tourne trop. Poitrine coincée, sourire parti, papa "
    "accroupi. Stop, recule. Merci vécu. Deuxième ruse : trop "
    "vite au jardin. Elle dit stop. Un éclat de rideau tient "
    "sur le tissu."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tapis|parquet|canapé|canape|balançoire|balancoire|banc|"
    r"thym|seau|coussin|plaid|sable|toboggan|gouttière|gouttiere|"
    r"colline|portail|trèfle|trefle|miel|moulin|plancher|"
    r"tableau|craie|casier|carotte|rambarde|zinc|"
    r"flaque|piquet|rotin|crochet|platane|cageot|résine|resine|"
    r"botte|bottes|limace|perron|chaise|tiroir|fraisier|"
    r"cuivre|buis|cerceau|grille|cour|pierre|nappe|figue|robinet|"
    r"planche|émail|email|samare|bassine|lunettes|corde|drap|"
    r"ballon|entrée|entree|horloge|bol|casserole|soupe|"
    r"chiffon|sauge|lacet|commode|gond|confiture|"
    r"tartine|fraise|camion|radiateur|manteau|pupitre|gomme|"
    r"pull|feuille)\b",
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
    "on peut laisser",
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
    "tu as su attendre",
    "on n'imite pas",
    "on n imite pas",
    "on n'achève pas",
    "on n acheve pas",
    "on attend la fin",
    "laisser le temps",
    "vous parlez l'un",
    "on écoute jusqu'au bout",
    "on ecoute jusqu'au bout",
    "dire stop, c'est permis",
    "dire stop c'est permis",
    "on s'éloigne",
    "on s eloigne",
    "on va vers un adulte",
    "tu as repris le geste",
    "tu as dit stop",
    "tu t'es éloigné",
    "tu t es eloigne",
    "tu t'es éloignée",
    "c'est le bon geste",
    "tu as bien écouté ton corps",
    "tu as bien ecoute ton corps",
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
    "éclat de rambarde",
    "éclat de zinc",
    "éclat de parquet",
    "éclat de canapé",
    "éclat de canape",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de pupitre",
    "éclat de feuille",
    "éclat de sac",
    "éclat de gomme",
    "éclat de pull",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
    "sara ",
    "victorino",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de rideau",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis trop_plein; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_ronde_maintenant; "
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
            "sous_texte=c_est_trop_que_dit_sarah; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="Stop",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=trop_plein puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_dit_stop_recule; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de rideau",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=jardin_trop_vite_elle_dit_stop; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de rideau",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_tissu; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "stop",
    "accepted_examples": "stop | s'éloigner | papa | adulte | vers papa",
    "retry_prompt": "Sarah dit stop. Puis elle va où ?",
    "engine_ok_text": "Oui, stop.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "rideau",
        [
            "narrateur|Le linge tiède bouge devant le jardin.",
            "narrateur|Ça sent le pain et le soleil.",
            "enfant-f|Ça sent le pain, papa.",
            "papa|Tu le sens, le linge, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un rai passe à travers le tissu.",
            "narrateur|Le tissu fait un bruit court.",
            "enfant-f|Il claque, maman.",
            "maman|Le tissu tient près du bois ?",
            "enfant-f|Oui, maman.",
            "narrateur|Près du tissu, un éclat de rideau brille.",
            "enfant-f|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|La fenêtre tient un bout de jardin pâle.",
            "enfant-f|Il est clair, papa.",
            "papa|Le jardin, là-bas ?",
            "enfant-f|Oui, là-bas.",
            "narrateur|Aniss tend les mains vers Sarah.",
            "copain|On tourne, Sarah !",
            "enfant-f|On tourne, maintenant !",
            "papa|La ronde, avec Aniss ?",
            "enfant-f|Oui.",
            "enfant-f|Tout de suite.",
            "narrateur|En ce moment, Sarah se penche vers lui.",
            "narrateur|Leurs mains se tiennent.",
            "copain|Plus vite !",
            "narrateur|Aniss tourne trop vite.",
            "narrateur|Le tissu claque un peu.",
            "narrateur|Sarah veut la ronde, elle aussi.",
            "enfant-f|Plus vite !",
            "narrateur|Le tourbillon serre trop.",
            "narrateur|Sa poitrine est coincée.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Ses épaules montent.",
            "enfant-f|Oh.",
            "papa|Tu vois Aniss, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|Tes épaules sont hautes, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de rideau tremble, puis tient.",
            "narrateur|Sarah serre les mains trop fort.",
            "enfant-f|C'est trop, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Sarah regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|C'est trop pour Sarah.",
            "narrateur|Que dit-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "tissu",
        [
            "narrateur|Sarah veut la ronde, maintenant.",
            "enfant-f|Plus vite, Aniss !",
            "narrateur|Aniss tourne trop, trop près.",
            "narrateur|Le tissu claque contre le bois.",
            "narrateur|Sa poitrine reste coincée.",
            "narrateur|Le sourire ne revient pas.",
            "enfant-f|Oh.",
            "narrateur|Sarah refuse de foncer.",
            "enfant-f|Stop.",
            "narrateur|Elle recule d'un pas.",
            "narrateur|Les mains se lâchent.",
            "narrateur|Aniss s'arrête net.",
            "copain|Ah.",
            "papa|Tu restes près de nous, Sarah ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Papa, on fait quoi ?",
            "papa|On pose les mains, puis on reste.",
            "enfant-f|D'accord.",
            "narrateur|Sarah reste un moment, les mains ouvertes.",
            "narrateur|Elle souffle.",
            "copain|On tourne moins vite ?",
            "enfant-f|Moins vite.",
            "copain|D'accord.",
            "papa|Merci, Sarah.",
            "narrateur|Papa a vu les deux, près du rideau.",
            "maman|Le tissu est tiède, sous les doigts.",
            "enfant-f|Il est chaud.",
            "narrateur|Sarah glisse la main sur le tissu.",
            "enfant-f|Le petit point.",
            "papa|Il brille, là ?",
            "enfant-f|Oui, là.",
            "narrateur|Sarah pose les mains sur le bois.",
            "narrateur|Elle reste, sans se presser.",
            "maman|Tes mains sont au chaud, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Aniss s'assoit plus droit.",
            "enfant-f|Moins vite, oui.",
            "maman|Le rideau tient près de la fenêtre ?",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "porte_jardin",
        [
            "narrateur|Ils restent près de la fenêtre.",
            "narrateur|La porte du jardin s'ouvre.",
            "copain|Et dehors, on tourne.",
            "narrateur|Aniss tend les mains.",
            "enfant-f|La ronde, maintenant !",
            "narrateur|Sarah ouvre les bras trop vite.",
            "narrateur|Le tourbillon pousse contre sa poitrine.",
            "narrateur|Sarah avance les pieds, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "enfant-f|Stop.",
            "narrateur|Elle recule d'un pas, vers l'herbe.",
            "narrateur|Personne ne tourne.",
            "narrateur|Elle observe le jardin, un instant.",
            "narrateur|Elle écoute le silence de l'herbe.",
            "narrateur|Au bord du tissu, un éclat de rideau luit.",
            "enfant-f|Là, sur le tissu.",
            "enfant-f|On tourne moins vite, Aniss ?",
            "narrateur|Aniss ne dit rien, d'abord.",
            "narrateur|Il tient ses mains, sans tourner.",
            "copain|Moins vite.",
            "narrateur|Sarah hoche la tête, sans se presser.",
            "narrateur|Aniss souffle, plus lentement.",
            "narrateur|L'herbe est lisse et tiède.",
            "papa|Tu l'entends, le jardin ?",
            "enfant-f|Oui, papa.",
            "maman|La porte est près des fleurs ?",
            "enfant-f|Oui, maman.",
            "narrateur|Un panier roule vers le bord.",
            "narrateur|Sarah pose une main dessus.",
            "narrateur|Aniss pose la suivante.",
            "papa|Le panier tient, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|Un rayon passe sur le rideau.",
            "enfant-f|Il allume le tissu.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la porte.",
            "maman|La ronde a eu son tour, Sarah ?",
            "enfant-f|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah souffle, un filet d'air.",
            "enfant-f|Le tissu sent bon.",
            "maman|Tu le sens, le linge ?",
            "enfant-f|Oui, maman.",
            "papa|Le rideau reste un peu, à plat.",
            "enfant-f|Il a tenu, sur le bois.",
            "narrateur|Le jardin est chaud, sous les mains.",
            "narrateur|L'herbe fait une petite ombre.",
            "enfant-f|On y revient, après.",
            "narrateur|Un éclat de rideau tient sur le tissu.",
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
    if "stop" not in blob:
        raise SystemExit(f"{SID}: manque stop")
    if "recule" not in blob:
        raise SystemExit(f"{SID}: manque recule")
    if "poitrine" not in blob:
        raise SystemExit(f"{SID}: manque poitrine coincée")
    if "sourire" not in blob:
        raise SystemExit(f"{SID}: manque sourire parti")
    if "accroupit" not in blob:
        raise SystemExit(f"{SID}: manque papa accroupi")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Sarah = enfant-f, Aniss = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Aniss absent (copain)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse parlante")
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
        raise SystemExit(f"{SID}: enfant-f absent")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "ce n'est pas une faute",
        "n'est pas une faute",
        "on peut jouer",
        "on peut attendre",
        "on peut demander",
        "on peut laisser",
        "on joue",
        "vous jouez",
        "il faut attendre",
        "on doit demander",
        "il faut demander",
        "dire stop, c'est permis",
        "on s'éloigne",
        "on va vers un adulte",
        "tu as repris le geste",
        "tu as dit stop",
        "c'est le bon geste",
        "même leçon",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "C'est trop pour Sarah. Que dit-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "stop":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "stop | s'éloigner | papa | adulte | vers papa"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Sarah dit stop. Puis elle va où ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    n_copain = sum(
        1
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    )
    if n_copain > 7:
        raise SystemExit(f"{SID}: Aniss parle trop ({n_copain})")
    if n_copain < 3:
        raise SystemExit(f"{SID}: Aniss trop muet ({n_copain})")
    if "rideau" not in blob:
        raise SystemExit(f"{SID}: manque rideau")
    if "jardin" not in blob:
        raise SystemExit(f"{SID}: manque jardin")
    if "panier" not in blob:
        raise SystemExit(f"{SID}: manque panier")
    if "linge" not in blob:
        raise SystemExit(f"{SID}: manque linge")
    n_stop = sum(
        1
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("enfant-f|Stop.")
    )
    if n_stop != 2:
        raise SystemExit(f"{SID}: Stop vécu ×{n_stop} (voulu 2)")
    for ban in (
        "tapis",
        "parquet",
        "canapé",
        "canape",
        "balançoire",
        "balancoire",
        "éclat de banc",
        "éclat de pupitre",
        "tout doux",
        "tout calme",
        "victorino",
        "sara ",
        "kenzo",
        "iris",
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
        "- **Public :** N3 (≤16 mots/phrase), audio familial\n"
        "- **Leçon :** EMO.GES.001 — trop fort → dire stop, reculer "
        "(vécue : Sarah veut la ronde maintenant, Aniss tourne trop, "
        "poitrine coincée, sourire parti, papa accroupi, Stop, recule ; "
        "au jardin trop vite, Stop). JAMAIS dite dans le récit. Pas "
        "« dire stop, c'est permis ». Pas « on s'éloigne ». Pas « on va "
        "vers un adulte ». Pas « tu as repris le geste ».\n"
        "- **Personnages :** Sarah, Aniss, papa, maman. Dump Sara/papa "
        "→ D16. Sarah = enfant-f (veut jouer maintenant, trop vite, "
        "puis dit stop, recule). Aniss = copain (tourne trop vite, "
        "plus vite, moins vite). Troupe D16. Maman présente.\n"
        "- **Lieu :** maison puis jardin : rideau, fenêtre, linge, "
        "soleil, bois, herbe, porte, fleurs, panier. ≠ dump tapis / "
        "parquet / canapé / thym / seau. ≠ 001-01 balançoire / banc.\n"
        "- **Indice unique :** éclat de rideau (brille à l'ouverture "
        "près du tissu → tremble au tourbillon → luit au jardin → "
        "tient sur le tissu). BAN éclat de tapis / parquet / canapé / "
        "banc / balançoire / pupitre.\n"
        "- **Question moteur :** « C'est trop pour Sarah. Que dit-"
        "elle ? » expected dump **stop**. accepted dump. retry dump "
        "Sara→Sarah. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le linge tiède bouge devant le jardin. Près du tissu, un éclat "
        "de rideau brille. Fenêtre, pain, bois. Sarah veut la ronde "
        "**maintenant**. Aniss tourne trop. Poitrine coincée. Sourire "
        "parti. Papa s'accroupit. Stop, recule. Merci vécu. Deuxième "
        "ruse : trop vite au jardin. Elle dit stop. Un éclat de rideau "
        "tient sur le tissu.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : maison puis jardin, rideau, fenêtre, linge, soleil, "
        "bois, herbe, porte, fleurs, panier. ≠ dump tapis / parquet / "
        "canapé. ≠ 001-01 balançoire / banc.\n"
        "- Désir : la ronde, maintenant, avec Aniss.\n"
        "- Objet : rideau, tissu, panier, porte, herbe.\n"
        "- Indice unique : éclat de rideau, vu dès l'ouverture près du "
        "tissu, payé sur le tissu. Pas éclat de tapis / parquet / "
        "canapé / banc / balançoire.\n"
        "- Urgence douce : Sarah veut tourner maintenant, Aniss accélère.\n"
        "- Imprévu 1 : Aniss tourne trop. Poitrine coincée. Sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : au jardin, trop vite, la ronde reprend.\n"
        "- Résolution : elle dit stop, recule, observe, retrouve l'éclat.\n"
        "- Retour : ronde vécue moins vite, éclat sur le tissu.\n\n"
        "## Vécu\n\n"
        "Sarah veut la ronde **maintenant**. Impatience, puis tourbillon "
        "trop fort, sourire parti. Aniss pose sa limite (mains, ah, "
        "moins vite). Papa se baisse, pose une question, ne récite pas "
        "la règle. Ils agissent : Stop, reculer, rester. Merci vécu. "
        "Fin : l'éclat du début tient sur le tissu.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Sarah dit stop, puis encore (noyau dump La ronde trop "
        "vite, D16). Relance : Que dit-elle ? expected stop.\n"
        "- Lieu du dump (maison puis jardin) sans tapis / parquet / "
        "canapé. Maman présente. Aniss = copain.\n"
        "- Ouverture inventée (linge tiède devant le jardin), pas un "
        "gabarit v2, pas « Une bande de soleil rampe sur le plancher » "
        "du dump en première ligne.\n"
        "- Indice unique : éclat de rideau. BAN éclat de tapis / parquet "
        "/ canapé / banc / balançoire. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout bas » / « encore » / « thym » / « seau » "
        "du dump. 2e stop au jardin sans le mot encore.\n"
        "- Leçon non dite : on la voit quand le tourbillon serre, quand "
        "Sarah dit stop, quand elle recule, quand elle le dit au jardin. "
        "Pas « dire stop, c'est permis ». Pas « on s'éloigne ». Pas "
        "« tu as repris le geste ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur D16 : « C'est trop pour Sarah. Que dit-"
        "elle ? ». expected dump stop. retry dump Sara→Sarah. 5 chunks, "
        "kinds inchangés.\n"
        "- example4 039 / 071 / 003 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_par_002_02.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le jardin.\n"
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
