#!/usr/bin/env python3
"""ATOM-DIF.ENE.001-03 — Le château avant la soupe (F-NAR-019, N3, DIF.ENE.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.ENE.001-03"
TITLE = "Le château avant la soupe"
N3 = LIMITS["N3"]
CHARS = "Sarah, Mila, papa, maman"
SETTING = (
    "salon puis cuisine, soupe de carotte, vitre embuée, "
    "cuillère en bois, coussin rayé, casseroles tin tin"
)
INDICE = "éclat de bol"
FIL = (
    "La cuillère en bois tape un bol. Au bord, un éclat de bol "
    "brille. Sarah veut un château de coussins, maintenant, avant "
    "la soupe. Mila saute trop, le mur tombe. Sourire parti, "
    "poitrine, papa accroupi. Sarah refuse de foncer, attend, "
    "demande. Merci vécu. Casseroles tin tin, cuillère trop vite. "
    "Un éclat de bol tient au bord."
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
    r"ballon|entrée|entree)\b",
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
    "ce n'est pas une faute",
    "n'est pas une faute",
    "pas une faute",
    "vous jouez",
    "on joue",
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
        emphasis="éclat de bol",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_un_chateau_maintenant; "
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
            "sous_texte=mila_a_de_l_energie; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="château",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_refuse_de_foncer_attend_demande; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de bol",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=casseroles_cuillere_trop_vite; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de bol",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_au_bord; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer",
    "accepted_examples": "jouer | attendre | un adulte | papa",
    "retry_prompt": "On peut jouer. On peut attendre. Que fait Sarah ?",
    "engine_ok_text": "Oui, jouer.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "coussin",
        [
            "narrateur|La cuillère en bois tape une fois contre un bol.",
            "narrateur|Ça fait toc, sec et chaud.",
            "enfant-f|J'ai entendu le toc.",
            "papa|Près des bols, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un filet de vapeur monte vers la vitre.",
            "narrateur|Papa essuie un petit trou avec le doigt.",
            "enfant-f|Le jardin est flou.",
            "papa|Tu as senti la soupe, Sarah ?",
            "enfant-f|Ça sent la carotte.",
            "maman|On mange bientôt.",
            "narrateur|Maman plie une serviette chaude.",
            "narrateur|Au bord du bol, un éclat de bol brille.",
            "enfant-f|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Au salon, un coussin rayé tient un carré de soleil.",
            "narrateur|Le tissu est tiède, contre le visage.",
            "enfant-f|Il est chaud, papa.",
            "papa|Le soleil est dessus ?",
            "enfant-f|Oui.",
            "narrateur|En ce moment, Sarah pose un coussin.",
            "enfant-f|Je veux un château, maintenant !",
            "enfant-f|Un château de coussins, avant la soupe.",
            "papa|Un petit mur, là ?",
            "enfant-f|Oui, un mur.",
            "maman|Les bols attendent, près de la vitre.",
            "enfant-f|Après le château.",
            "narrateur|Sarah pose un autre coussin, plus haut.",
            "narrateur|Le mur est bas, un peu de travers.",
            "narrateur|Mila arrive dans le salon.",
            "narrateur|Elle court un peu, pieds légers.",
            "copine|Je saute !",
            "narrateur|Mila saute trop, trop près du mur.",
            "enfant-f|Tu poses avec moi ?",
            "copine|Oui.",
            "narrateur|Mila pose un coussin trop vite.",
            "narrateur|Le mur bascule.",
            "narrateur|Un coussin glisse sur le tapis.",
            "enfant-f|Oh.",
            "enfant-f|Le château.",
            "copine|Il est tombé.",
            "narrateur|Sarah tient un coussin contre elle.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Mila, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains tiennent le coussin, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de bol tremble, puis tient.",
            "narrateur|Mila tape des pieds sur le tapis.",
            "enfant-f|Elle saute partout, papa.",
            "narrateur|Sarah regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Mila a de l'énergie.",
            "narrateur|Que fait-on ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "coussin",
        [
            "narrateur|Sarah veut le château, tout de suite.",
            "enfant-f|Je le refais, maintenant !",
            "narrateur|Elle avance trop vite vers Mila.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copine|Attends.",
            "narrateur|Mila tape des pieds, trop près.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le coussin, un instant.",
            "narrateur|Elle écoute le toc de la cuillère.",
            "papa|Tu veux le mur avec Mila ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Papa, on fait quoi ?",
            "papa|On pose un coussin, puis l'autre.",
            "enfant-f|D'accord.",
            "narrateur|Sarah pose le sien, sans se presser.",
            "narrateur|Elle reste un moment, les mains ouvertes.",
            "narrateur|Mila souffle.",
            "copine|Le mien.",
            "narrateur|Mila pose le suivant, plus lentement.",
            "papa|Merci, Sarah.",
            "narrateur|Papa a vu les deux, au salon.",
            "maman|Le tissu est tiède, sous les doigts.",
            "enfant-f|Il est chaud.",
            "narrateur|Le mur tient, un peu de travers.",
            "enfant-f|Le château.",
            "papa|Il a une porte, là ?",
            "enfant-f|Oui, là.",
            "narrateur|Sarah glisse la main dans le trou.",
            "narrateur|Le tissu est doux, contre la peau.",
            "maman|Tes mains sont au chaud, Sarah ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Mila s'assoit, puis se relève.",
            "copine|J'y vais.",
            "enfant-f|On va à la cuisine ?",
            "maman|La cuillère en bois est près des bols.",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "casserole",
        [
            "narrateur|Ils vont dans la cuisine.",
            "narrateur|Les casseroles font tin tin.",
            "copine|À moi !",
            "narrateur|Mila tape un rythme trop vite.",
            "maman|On se passe la cuillère en bois ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sarah envoie la cuillère trop vite.",
            "narrateur|La cuillère penche vers le bol.",
            "enfant-f|Ça tombe !",
            "copine|Attends.",
            "narrateur|Sarah avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Sarah refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le bol, un instant.",
            "narrateur|Elle écoute le tin tin des casseroles.",
            "narrateur|Au bord du bol, un éclat de bol luit.",
            "enfant-f|Là, sur le bol.",
            "enfant-f|Tu prends la cuillère, Mila ?",
            "narrateur|Mila ne dit rien.",
            "narrateur|Elle tend les mains, sans parler.",
            "copine|Oui.",
            "narrateur|Sarah envoie la cuillère, sans se presser.",
            "narrateur|Mila la renvoie, plus lentement.",
            "narrateur|La cuillère est lisse et chaude.",
            "papa|Tu la vois, la cuillère ?",
            "enfant-f|Oui, papa.",
            "maman|Les bols sont près de la vitre ?",
            "enfant-f|Oui, maman.",
            "narrateur|Elles reviennent au salon.",
            "narrateur|Sarah pose un coussin.",
            "narrateur|Mila pose le suivant.",
            "papa|Le mur tient, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|Un rayon passe sur le tissu rayé.",
            "enfant-f|Il allume le château.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "soupe",
        [
            "narrateur|Ils restent près de la table.",
            "maman|La soupe est prête, Sarah ?",
            "enfant-f|Oui, maman.",
            "papa|Tu souffles sur ta cuillère ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sarah souffle, un filet de vapeur.",
            "enfant-f|La carotte sent bon.",
            "maman|Tu la sens, la carotte ?",
            "enfant-f|Oui, maman.",
            "papa|Le château reste un peu, de travers.",
            "enfant-f|Il a tenu, avant la soupe.",
            "copine|Le château est resté.",
            "narrateur|Les bols sont chauds, sous les mains.",
            "narrateur|Le château de coussins fait de l'ombre.",
            "enfant-f|On y retourne, après.",
            "narrateur|Un éclat de bol tient au bord.",
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
        raise SystemExit(f"{SID}: enfant-m (Sarah = enfant-f, Mila = copine)")
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
        "ce n'est pas une faute",
        "n'est pas une faute",
        "on peut jouer",
        "on peut attendre",
        "on peut demander",
        "on joue",
        "vous jouez",
        "il faut attendre",
        "on doit demander",
        "il faut demander",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Mila a de l'énergie. Que fait-on ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != "jouer | attendre | un adulte | papa":
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "On peut jouer. On peut attendre. Que fait Sarah ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    copine_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    ).lower()
    if "attends" not in copine_txt:
        raise SystemExit(f"{SID}: Mila sans attends")
    if "carotte" not in blob:
        raise SystemExit(f"{SID}: manque carotte")
    if "coussin rayé" not in blob and "coussin raye" not in blob:
        raise SystemExit(f"{SID}: manque coussin rayé")
    if "cuillère en bois" not in blob and "cuillere en bois" not in blob:
        raise SystemExit(f"{SID}: manque cuillère en bois")
    if "tin tin" not in blob:
        raise SystemExit(f"{SID}: manque tin tin")
    if "soupe" not in blob:
        raise SystemExit(f"{SID}: manque soupe")
    for ban in (
        "éclat de cuillère",
        "éclat de cuillere",
        "éclat de coussin",
        "éclat de casserole",
        "éclat de buée",
        "éclat de buee",
        "éclat de nappe",
        "éclat de flaque",
        "éclat de piquet",
        "tout doux",
        "tout calme",
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
        "- **Leçon :** DIF.ENE.001 — l'énergie de Mila (vécue : elle saute "
        "trop, le mur tombe, Sarah refuse de foncer, attend, demande, "
        "passe la cuillère sans se presser). JAMAIS dite dans le récit. "
        "Pas « ce n'est pas une faute ». Pas « on peut jouer / attendre / "
        "demander ».\n"
        "- **Personnages :** Sarah, Mila, papa, maman. Sarah = enfant-f "
        "(propose, trop vite, puis refuse de foncer). Mila = copine "
        "(énergie, saute, attends, silence). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** salon puis cuisine, soupe de carotte, vitre, "
        "cuillère en bois, coussin rayé, casseroles tin tin. ≠ 001-01 "
        "flaque / 001-02 piquet. ≠ COR.001-08 train de coussins.\n"
        "- **Indice unique :** éclat de bol (brille à l'ouverture près "
        "de la soupe → tremble au mur → luit au refus cuisine → tient "
        "au bord). BAN éclat de cuillère / coussin / casserole / buée / "
        "nappe / flaque / piquet.\n"
        "- **Question moteur :** « Mila a de l'énergie. Que fait-on ? » "
        "expected **jouer**. accepted `jouer | attendre | un adulte | "
        "papa`. retry dump (label). Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La cuillère en bois tape un bol. Au bord, un éclat de bol "
        "brille. Coussin rayé, soleil, carotte. Sarah veut un château "
        "**maintenant**, avant la soupe. Mila saute trop, le mur tombe. "
        "Sourire parti. Papa s'accroupit. Elle refuse de foncer. Elles "
        "posent un coussin, puis l'autre. Merci vécu. Deuxième ruse : "
        "casseroles tin tin, cuillère trop vite, le bol penche. Elle "
        "s'arrête, lit l'éclat. Un éclat de bol tient au bord.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon puis cuisine, soupe de carotte, vitre, toc de "
        "cuillère, coussin rayé, casseroles tin tin. ≠ 001-01 flaque / "
        "001-02 piquet.\n"
        "- Désir : un château de coussins, maintenant, avant la soupe.\n"
        "- Objet : coussins, cuillère en bois, bols, casseroles.\n"
        "- Indice unique : éclat de bol, vu dès l'ouverture, payé au "
        "bord. Pas éclat de cuillère / coussin / casserole / buée.\n"
        "- Urgence douce : la soupe arrive, le château doit tenir avant.\n"
        "- Imprévu 1 : Mila saute trop, pose trop vite, le mur tombe.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« d'accord ».\n"
        "- Imprévu 2 (plus rusé) : cuisine, tin tin, cuillère trop vite, "
        "le bol penche.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le tin "
        "tin, retrouve l'éclat, Mila tend les mains.\n"
        "- Retour : château de travers, soupe prête, éclat au bord.\n\n"
        "## Vécu\n\n"
        "Sarah veut le château **maintenant**. Impatience, puis mur qui "
        "tombe, sourire parti. Mila prend son élan, pose sa limite "
        "(attends, silence). Papa se baisse, pose une question, ne "
        "récite pas la règle. Elles agissent : un coussin puis l'autre, "
        "cuillère passée sans se presser. Merci vécu. Fin : l'éclat du "
        "début tient au bord du bol.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le château avant la soupe (noyau dump). Relance : "
        "Que fait-on ? expected jouer.\n"
        "- Lieu du dump (salon puis cuisine, soupe de carotte). Maman "
        "présente. Mila = copine.\n"
        "- Ouverture inventée (toc de cuillère contre un bol), pas un "
        "gabarit v2, pas « Un rond de vapeur s'ouvre sur la vitre » du "
        "dump en première ligne.\n"
        "- Indice unique : éclat de bol. BAN éclat de cuillère / "
        "coussin / casserole / buée / nappe / flaque / piquet. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout bas » / « encore » du dump.\n"
        "- Leçon non dite : on la voit quand le mur tombe, quand Sarah "
        "s'arrête, quand elles posent à tour. Pas « ce n'est pas une "
        "faute ». Pas « on peut jouer / attendre / demander » hors "
        "retry label.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Mila a de l'énergie. Que "
        "fait-on ? ». expected jouer. retry dump. 5 chunks, kinds "
        "inchangés.\n"
        "- example4 017 / 049 / 081 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_cor_003_02.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers les casseroles.\n"
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
