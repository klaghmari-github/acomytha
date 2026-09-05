#!/usr/bin/env python3
"""ATOM-DIF.PAR.001-05 — Le seau tiède du jardin (F-NAR-019, N2, DIF.PAR.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.001-05"
TITLE = "Le seau tiède du jardin"
N2 = LIMITS["N2"]
CHARS = "Nina, Raphaël, papa, maman"
SETTING = (
    "jardin, tomates vertes, abeille, romarin, thym, "
    "seau bleu tiède, pots, terre"
)
INDICE = "éclat de romarin"
FIL = (
    "Une goutte tiède pend au romarin. Sur une feuille, un "
    "éclat de romarin brille. Nina veut le seau, maintenant. "
    "Raphaël ne dit rien. Elle pousse trop vite, eau. Sourire "
    "parti, poitrine, papa accroupi. Elle refuse de foncer, "
    "tend le seau, attend. Merci vécu. 2e ruse, Dis-le. Un "
    "éclat de romarin tient près des tomates."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(parquet|banc|table|haricot|châssis|chassis|buée|buee|"
    r"coccinelle|chapeau|pelle|flaque|piquet|portail|rotin|"
    r"crochet|platane|cageot|résine|resine|botte|bottes|limace|"
    r"perron|chaise|tiroir|fraisier|cuivre|buis|cerceau|grille|"
    r"cour|nappe|figue|robinet|planche|émail|email|samare|"
    r"bassine|lunettes|corde|drap|ballon|entrée|entree|merle|"
    r"miel|confiture|tartine|fraise|camion|coussin|tapis|"
    r"puzzle|bateau|voiture|wagon|sable|gourde|horloge|"
    r"chiffon|sauge|lacet|commode|gond)\b",
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
    "on peut tendre",
    "tu peux tendre",
    "tendre un jouet",
    "ce n'est pas une faute",
    "n'est pas une faute",
    "pas une faute",
    "vous jouez",
    "on joue",
    "parle peu",
    "il parle peu",
    "elle parle peu",
    "forcer la parole",
    "on ne force pas",
    "ne force pas la parole",
    "force pas la parole",
    "on n'imite pas",
    "on n imite pas",
    "tu as su attendre",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "trois notes",
    "éclat de seau",
    "éclat de parquet",
    "éclat de banc",
    "éclat de rond",
    "éclat de table",
    "éclat de tomate",
    "éclat de thym",
    "éclat d'abeille",
    "éclat d abeille",
    "éclat de pot",
    "éclat de terre",
    "éclat de feuille",
    "éclat d'eau",
    "éclat d eau",
    "éclat de goutte",
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
    "éclat d'horloge",
    "éclat d horloge",
    "éclat de haricot",
    "éclat de châssis",
    "éclat de chassis",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
    "faustine",
    "marceau",
    "léa",
    "lea",
    "adam",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de romarin",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_seau_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Nina",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=raphael_parle_peu_que_fait_nina; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="seau",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_refuse_de_foncer_tend_attend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de romarin",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=eau_trop_vite_dis_le_elle_s_arrete; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de romarin",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pres_des_tomates; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "attendre",
    "accepted_examples": "attendre | tendre | le seau | un jouet",
    "retry_prompt": "Elle tend un jouet. Elle attend. Que fait Nina ?",
    "engine_ok_text": "Oui, attendre.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "jardin,eau",
        [
            "narrateur|Une goutte tiède pend au romarin.",
            "narrateur|Elle tremble, puis tient.",
            "enfant-f|Elle est chaude, papa.",
            "papa|Tu la vois, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Les tomates sont vertes, sous les feuilles.",
            "enfant-f|Elles sont dures, maman.",
            "maman|Tu les as touchées, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sur une feuille, un éclat de romarin brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Ça sent le thym, tout près.",
            "enfant-f|Ça pique le nez.",
            "maman|Le thym est fort, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Une abeille passe près des tomates.",
            "enfant-f|Elle fait un bruit, papa.",
            "papa|Près des fleurs ?",
            "enfant-f|Oui, tout près.",
            "narrateur|Le seau bleu attend au bord de la terre.",
            "narrateur|Le plastique est tiède, contre la paume.",
            "enfant-f|Il est chaud, maman.",
            "maman|Tu le tiens, Nina ?",
            "enfant-f|Oui.",
            "narrateur|En ce moment, Nina pose le seau.",
            "enfant-f|Je veux le seau, maintenant !",
            "enfant-f|Pour les tomates, tout de suite.",
            "papa|De l'eau, là ?",
            "enfant-f|Oui, de l'eau.",
            "maman|Le seau bleu est plein ?",
            "enfant-f|Presque.",
            "narrateur|Raphaël arrive près des pots.",
            "narrateur|Il marche sans bruit.",
            "enfant-f|Tu verses avec moi ?",
            "narrateur|Raphaël ne dit rien.",
            "narrateur|Il regarde ses mains.",
            "narrateur|Nina a envie de tout expliquer.",
            "narrateur|Les mots montent très vite.",
            "enfant-f|Le seau !",
            "enfant-f|L'eau !",
            "enfant-f|Les tomates !",
            "narrateur|Nina pousse trop vite vers lui.",
            "narrateur|Le seau penche.",
            "narrateur|L'eau tombe sur la terre.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Raphaël, Nina ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains tiennent le seau, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de romarin tremble, puis tient.",
            "narrateur|Raphaël reste près des pots.",
            "enfant-f|Il ne dit rien, papa.",
            "narrateur|Nina regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Raphaël parle peu.",
            "narrateur|Que fait Nina ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "seau,eau",
        [
            "narrateur|Nina veut le seau, tout de suite.",
            "enfant-f|Prends-le, maintenant !",
            "narrateur|Elle avance trop vite vers Raphaël.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "narrateur|Raphaël recule un peu.",
            "narrateur|Il serre les mains contre lui.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Nina refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le seau, un instant.",
            "narrateur|Elle écoute l'abeille près des feuilles.",
            "papa|Tu veux l'eau avec Raphaël ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Papa, on fait quoi ?",
            "papa|On pose le seau, puis on reste.",
            "enfant-f|D'accord.",
            "narrateur|Nina reste un moment, les mains ouvertes.",
            "narrateur|Elle attend.",
            "narrateur|Elle tend le seau.",
            "enfant-f|Pour toi.",
            "narrateur|Raphaël ne dit rien.",
            "narrateur|Il prend le seau, sans parler.",
            "copain|Oui.",
            "narrateur|Nina pose les mains sur la terre.",
            "narrateur|Elle reste, sans se presser.",
            "narrateur|Raphaël tient le seau, plus lentement.",
            "papa|Merci, Nina.",
            "narrateur|Papa a vu les deux, au jardin.",
            "maman|Le plastique est tiède, sous les doigts.",
            "enfant-f|Il est chaud.",
            "narrateur|Un peu d'eau reste au fond.",
            "enfant-f|Le seau.",
            "papa|Il a de l'eau, là ?",
            "enfant-f|Oui, là.",
            "narrateur|Nina glisse la main sur le bord.",
            "narrateur|Le plastique est doux, contre la peau.",
            "maman|Tes mains sont au chaud, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Raphaël s'assoit, puis se relève.",
            "copain|Seau.",
            "enfant-f|On va jusqu'aux tomates ?",
            "maman|Les tomates vertes sont près du thym.",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "eau,tomates",
        [
            "narrateur|Ils restent près des tomates.",
            "narrateur|Le seau bleu penche vers une feuille.",
            "enfant-f|Je verse, maintenant !",
            "narrateur|Nina pousse trop vite.",
            "narrateur|L'eau gicle sur le pied de Raphaël.",
            "enfant-f|Ça mouille !",
            "enfant-f|Dis-le, Raphaël !",
            "narrateur|Raphaël serre les lèvres.",
            "narrateur|Nina avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le seau, un instant.",
            "narrateur|Elle écoute le thym, tout près.",
            "narrateur|Près des feuilles, un éclat de romarin luit.",
            "enfant-f|Là, sur le romarin.",
            "enfant-f|Tu prends le seau, Raphaël ?",
            "narrateur|Raphaël ne dit rien.",
            "narrateur|Il tend les mains, sans parler.",
            "copain|Oui.",
            "narrateur|Nina passe le seau, sans se presser.",
            "narrateur|Raphaël le reçoit, plus lentement.",
            "narrateur|Le plastique est lisse et tiède.",
            "papa|Tu le vois, le seau ?",
            "enfant-f|Oui, papa.",
            "maman|L'eau est tiède, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Raphaël verse, un filet mince.",
            "narrateur|La terre devient sombre, sous les tomates.",
            "papa|La terre boit, Nina ?",
            "enfant-f|Oui, papa.",
            "maman|Un rayon passe sur le romarin.",
            "enfant-f|Il allume la feuille.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "jardin,romarin",
        [
            "narrateur|Ils restent près des tomates.",
            "maman|Le seau est vide, Nina ?",
            "enfant-f|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina souffle, un filet d'air.",
            "enfant-f|Le plastique sent bon.",
            "maman|Tu le sens, le seau ?",
            "enfant-f|Oui, maman.",
            "papa|La terre reste un peu, sombre.",
            "enfant-f|Elle a bu, sous les tomates.",
            "copain|Seau.",
            "narrateur|Le seau bleu fait de l'ombre.",
            "narrateur|L'abeille s'éloigne, sans bruit.",
            "enfant-f|On y remet de l'eau, après.",
            "narrateur|Un éclat de romarin tient près des tomates.",
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
    if "tend le seau" not in blob:
        raise SystemExit(f"{SID}: manque tend le seau")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Nina = enfant-f, Raphaël = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent (copain)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "enfant-f|" not in blob:
        raise SystemExit(f"{SID}: Nina absente (enfant-f)")
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
        "on peut tendre",
        "tu peux tendre",
        "tendre un jouet",
        "on joue",
        "vous jouez",
        "il faut attendre",
        "on doit demander",
        "il faut demander",
        "parle peu",
        "il parle peu",
        "forcer la parole",
        "on ne force pas",
        "on n'imite pas",
        "tu as su attendre",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Raphaël parle peu. Que fait Nina ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != "attendre | tendre | le seau | un jouet":
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Elle tend un jouet. Elle attend. Que fait Nina ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    n_copain = sum(
        1
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    )
    if n_copain > 5:
        raise SystemExit(f"{SID}: Raphaël parle trop ({n_copain})")
    if n_copain < 2:
        raise SystemExit(f"{SID}: Raphaël muet ({n_copain})")
    if "ne dit rien" not in blob:
        raise SystemExit(f"{SID}: manque silence vécu")
    for need in (
        "tomate",
        "abeille",
        "romarin",
        "thym",
        "seau bleu",
        "jardin",
    ):
        if need not in blob:
            raise SystemExit(f"{SID}: manque {need}")
    for ban in (
        "éclat de seau",
        "éclat de parquet",
        "éclat de banc",
        "éclat de rond",
        "éclat de table",
        "éclat de haricot",
        "faustine",
        "marceau",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "trois notes",
        "haricot",
        "châssis",
        "buée",
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
    slow_ids = {
        c["chunk_id"]
        for c in chunks
        if c.get("rate_label") == "slow"
    }
    if slow_ids != {"CHK_T0000_P0000_Q0001", "CHK_T0000_P0000_END_F0001"}:
        raise SystemExit(f"{SID}: slow mal placé: {slow_ids}")

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
        "- **Leçon :** DIF.PAR.001 — Raphaël parle peu (vécue : Nina "
        "pousse trop vite, eau, sourire parti ; elle refuse de foncer, "
        "tend le seau, attend ; 2e ruse Dis-le, lèvres serrées). JAMAIS "
        "dite dans le récit. Pas « on n'imite pas ». Pas « on ne force "
        "pas la parole ». Pas « on peut attendre / tendre ».\n"
        "- **Personnages :** Nina, Raphaël, papa, maman. Faustine/"
        "Marceau dump-xai → D16. Nina = enfant-f (veut le seau "
        "maintenant, trop vite, puis refuse de foncer). Raphaël = "
        "copain (parle peu, silence, oui, seau). Troupe D16. Pas de "
        "maîtresse.\n"
        "- **Lieu :** jardin, tomates vertes, abeille, romarin, thym, "
        "seau bleu tiède, pots, terre. ≠ PAR.001-01 parquet / tapis. ≠ "
        "001-02 banc / sable. ≠ 001-03 rond. ≠ 001-04 table. ≠ dump "
        "haricot / châssis / buée.\n"
        "- **Indice unique :** éclat de romarin (brille à l'ouverture "
        "sur une feuille → tremble à l'eau → luit au refus Dis-le → "
        "tient près des tomates). BAN éclat de seau (trop objet) / "
        "parquet / banc / rond / table.\n"
        "- **Question moteur :** « Raphaël parle peu. Que fait Nina ? » "
        "expected **attendre**. accepted `attendre | tendre | le seau | "
        "un jouet`. retry dump. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte tiède pend au romarin. Sur une feuille, un éclat "
        "de romarin brille. Tomates vertes, thym, abeille, seau bleu "
        "tiède. Nina veut le seau **maintenant**. Raphaël arrive, ne "
        "dit rien. Elle pousse trop vite, l'eau tombe. Sourire parti. "
        "Papa s'accroupit. Elle refuse de foncer. Elle tend le seau, "
        "attend. Merci vécu. Deuxième ruse : je verse, Dis-le, lèvres "
        "serrées. Elle s'arrête, lit l'éclat. Un éclat de romarin "
        "tient près des tomates.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin, goutte au romarin, tomates vertes, thym, "
        "abeille, seau bleu tiède, pots, terre. ≠ parquet / banc / "
        "rond / table. ≠ haricot / châssis / buée.\n"
        "- Désir : le seau bleu, maintenant, pour les tomates.\n"
        "- Objet : seau bleu tiède, eau, tomates, romarin.\n"
        "- Indice unique : éclat de romarin, vu dès l'ouverture, payé "
        "près des tomates. Pas éclat de seau (objet-mission).\n"
        "- Urgence douce : Raphaël arrive, Nina accélère les mots.\n"
        "- Imprévu 1 : Nina pousse trop vite, le seau penche, l'eau "
        "tombe. Raphaël ne dit rien.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : elle verse trop vite, veut lui "
        "faire dire, il serre les lèvres.\n"
        "- Résolution : elle refuse de foncer, observe, écoute "
        "l'abeille puis le thym, retrouve l'éclat, tend, il reçoit.\n"
        "- Retour : terre sombre, seau vide, éclat près des tomates.\n\n"
        "## Vécu\n\n"
        "Nina veut le seau **maintenant**. Impatience, puis eau, "
        "sourire parti. Raphaël pose sa limite (silence, recul, lèvres "
        "serrées, oui, seau). Papa se baisse, pose une question, ne "
        "récite pas la règle. Ils agissent : attendre, tendre le seau, "
        "verser sans se presser. Merci vécu. Fin : l'éclat du début "
        "tient près des tomates.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le seau tiède du jardin (noyau mission, titre "
        "gardé). Relance : Que fait Nina ? expected attendre.\n"
        "- Lieu mission (jardin, tomates, abeille, romarin, thym, seau "
        "bleu). Maman et papa. Nina = enfant-f. Raphaël = copain. "
        "Faustine/Marceau dump-xai retirés. Dump haricot / châssis / "
        "buée / pelle retiré.\n"
        "- Ouverture inventée (goutte tiède au romarin), pas un "
        "gabarit v2, pas « La vitre du châssis est toute embuée ».\n"
        "- Indice unique : éclat de romarin. BAN éclat de seau / "
        "parquet / banc / rond / table. Pas tache/flèche/marque/"
        "symbole. Pas merle-trois-notes, pas miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « on peut attendre » / « on n'imite pas » / "
        "« on ne force pas la parole » / « tu as su attendre » / "
        "bravo du dump.\n"
        "- Leçon non dite : on la voit quand l'eau tombe, quand elle "
        "s'arrête, quand elle tend, quand il prend sans parler. Pas "
        "« il faut attendre ». Pas « il parle peu » hors question.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Raphaël parle peu. Que fait "
        "Nina ? ». expected attendre. accepted `attendre | tendre | "
        "le seau | un jouet`. retry dump. 5 chunks, kinds inchangés.\n"
        "- example4 028 / 060 / 092 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_ene_001_07.py` / "
        "`_write_atom_dif_ene_001_04.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le second versement.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n"
        "- 1 × `en ce moment`, 1 × merci adulte, 4 × éclat de romarin\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
