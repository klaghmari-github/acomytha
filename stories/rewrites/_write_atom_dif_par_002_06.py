#!/usr/bin/env python3
"""ATOM-DIF.PAR.002-06 — Mila laisse le temps à Victorino (F-NAR-019, N2, DIF.PAR.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.002-06"
TITLE = "Mila laisse le temps à Victorino"
N2 = LIMITS["N2"]
CHARS = "Mila, Victorino, papa, maman"
SETTING = (
    "salon, canapé, papillon de papier, ailes jaunes, "
    "rideau, linge séché, fenêtre"
)
INDICE = "éclat de canapé"
FIL = (
    "Une aile jaune tremble sur le canapé. Sur le tissu, un "
    "éclat de canapé brille. Mila veut le faire voler, maintenant. "
    "Victorino dit : j'ai vu. Le mot coincé. Elle connaît, ouvre "
    "la bouche maintenant, Papillon trop tôt. Sourire parti, "
    "papa accroupi. Elle referme, attend. Merci vécu. 2e ruse, "
    "Dis-le, ailes jaunes. Un éclat de canapé tient sur le tissu."
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
    r"chiffon|sauge|lacet|commode|gond|assiette|étal|etal|"
    r"plateau|carotte|pupitre|serviette|cacao|chat|canard|"
    r"poule|pomme|bol|cuillère|cuillere|compote|romarin|"
    r"thym|seau|tomate|abeille)\b",
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
    "on peut laisser",
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
    "tu as laissé le temps",
    "tu as laisse le temps",
    "on laisse le temps",
    "laisser le temps",
    "on attend la fin",
    "on n'achève pas",
    "on n acheve pas",
    "on écoute jusqu'au bout",
    "on ecoute jusqu'au bout",
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
    "éclat d'assiette",
    "éclat d assiette",
    "éclat d'étal",
    "éclat d'etal",
    "éclat de plateau",
    "éclat de pupitre",
    "éclat de romarin",
    "éclat de zinc",
    "éclat de rambarde",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
    "faustine",
    "marceau",
    "hortense",
    "eliott",
    "léa",
    "lea",
    "adam",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de canapé",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_voler_maintenant; "
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
            "sous_texte=victorino_cherche_un_mot_que_fait_mila; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="papillon",
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
        emphasis="éclat de canapé",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=dis_le_ailes_jaunes_elle_referme; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de canapé",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_tissu; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "salon,papier",
        [
            "narrateur|Le soleil pose une bande chaude sur le canapé.",
            "narrateur|Le tissu sent le linge séché.",
            "enfant-f|Il est chaud, papa.",
            "papa|Tu le sens, le canapé ?",
            "enfant-f|Oui, papa.",
            "narrateur|Une aile de papier tremble, jaune.",
            "enfant-f|Elle bouge, maman.",
            "maman|Le papillon est en papier, Mila ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sur le tissu, un éclat de canapé brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Le rideau laisse passer l'air.",
            "enfant-f|Ça sent le propre.",
            "maman|Le linge a séché, Mila ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le papillon de papier attend sur le bras.",
            "narrateur|Le papier est lisse, contre la paume.",
            "enfant-f|Il est lisse, maman.",
            "maman|Tu le tiens, Mila ?",
            "enfant-f|Oui.",
            "narrateur|En ce moment, Mila pose le papillon.",
            "enfant-f|Je veux le faire voler, maintenant !",
            "enfant-f|Jusqu'à la fenêtre, tout de suite.",
            "papa|Le papillon jaune, là ?",
            "enfant-f|Oui, le jaune.",
            "maman|Les ailes sont un peu froissées ?",
            "enfant-f|Un peu.",
            "narrateur|Victorino arrive près du canapé.",
            "narrateur|Il marche sans bruit.",
            "enfant-f|Tu l'as vu, toi ?",
            "narrateur|Victorino ouvre la bouche.",
            "copain|J'ai vu.",
            "narrateur|Il s'arrête.",
            "narrateur|Le mot reste coincé.",
            "narrateur|Mila connaît le mot.",
            "narrateur|Le mot monte très vite.",
            "narrateur|Elle ouvre la bouche, maintenant.",
            "enfant-f|Papillon !",
            "narrateur|Le mot sort trop tôt.",
            "narrateur|Victorino recule un peu.",
            "narrateur|Il serre les lèvres.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Victorino, Mila ?",
            "enfant-f|Oui, papa.",
            "maman|Tes lèvres sont ouvertes, Mila ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de canapé tremble, puis tient.",
            "narrateur|Victorino reste près du bras.",
            "enfant-f|Le mot manque, papa.",
            "narrateur|Mila regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorino cherche un mot.",
            "narrateur|Que fait Mila ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "salon,papier",
        [
            "narrateur|Mila veut le mot, tout de suite.",
            "enfant-f|Papillon, maintenant !",
            "narrateur|Elle ouvre la bouche.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "narrateur|Victorino recule un peu.",
            "narrateur|Il serre les mains contre lui.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Mila referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le papillon, un instant.",
            "narrateur|Elle écoute le rideau, tout près.",
            "papa|Tu veux voler avec Victorino ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Papa, on fait quoi ?",
            "papa|On pose le papillon, puis on reste.",
            "enfant-f|D'accord.",
            "narrateur|Mila reste un moment, les lèvres fermées.",
            "narrateur|Elle attend.",
            "copain|J'ai vu un papillon.",
            "enfant-f|Il est en papier.",
            "copain|Oui.",
            "copain|Papier.",
            "papa|Merci, Mila.",
            "narrateur|Papa a vu les deux, au salon.",
            "maman|Le papier est lisse, sous les doigts.",
            "enfant-f|Il est lisse.",
            "narrateur|Une aile jaune repose sur le bras.",
            "enfant-f|Le papillon.",
            "papa|Il a des ailes, là ?",
            "enfant-f|Oui, là.",
            "narrateur|Mila glisse la main sur le tissu.",
            "narrateur|Le canapé est doux, contre la peau.",
            "maman|Tes mains sont au chaud, Mila ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Victorino s'assoit, puis se relève.",
            "copain|Papillon.",
            "enfant-f|On va jusqu'à la fenêtre ?",
            "maman|La fenêtre est près du rideau.",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "salon,papier",
        [
            "narrateur|Ils restent près du canapé.",
            "narrateur|Le papillon jaune penche vers le bras.",
            "enfant-f|Je le fais voler, maintenant !",
            "narrateur|Mila pousse trop vite.",
            "narrateur|L'aile glisse sur le tissu.",
            "enfant-f|Ça glisse !",
            "enfant-f|Dis-le, Victorino !",
            "narrateur|Victorino serre les lèvres.",
            "narrateur|Mila avance les mots, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Mila referme la bouche, cette fois.",
            "narrateur|Ses lèvres se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le papillon, un instant.",
            "narrateur|Elle écoute le rideau, tout près.",
            "narrateur|Près du bras, un éclat de canapé luit.",
            "enfant-f|Là, sur le canapé.",
            "enfant-f|Tu prends le papillon, Victorino ?",
            "narrateur|Victorino ne dit rien.",
            "narrateur|Il tend les mains, sans parler.",
            "copain|Les ailes sont.",
            "narrateur|Mila attend.",
            "copain|Les ailes sont jaunes.",
            "enfant-f|Jaunes, oui.",
            "narrateur|Mila passe le papillon, sans se presser.",
            "narrateur|Victorino le reçoit, plus lentement.",
            "narrateur|Le papier est lisse et tiède.",
            "papa|Tu le vois, le papillon ?",
            "enfant-f|Oui, papa.",
            "maman|L'aile est tiède, Mila ?",
            "enfant-f|Oui, maman.",
            "narrateur|Victorino souffle, un filet d'air.",
            "narrateur|L'aile se lève un peu, puis retombe.",
            "papa|L'aile bouge, Mila ?",
            "enfant-f|Oui, papa.",
            "copain|Il veut.",
            "narrateur|Mila attend.",
            "copain|Il veut voler.",
            "enfant-f|Il vole un peu.",
            "maman|Un rayon passe sur le canapé.",
            "enfant-f|Il allume le tissu.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "salon,canapé",
        [
            "narrateur|Ils restent près du canapé.",
            "maman|Le papillon est là, Mila ?",
            "enfant-f|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila souffle, un filet d'air.",
            "enfant-f|Le papier sent bon.",
            "maman|Tu le sens, le papillon ?",
            "enfant-f|Oui, maman.",
            "papa|Le tissu reste un peu, chaud.",
            "enfant-f|Il a tenu, sous l'aile.",
            "copain|Papillon.",
            "narrateur|Le papillon jaune fait de l'ombre.",
            "narrateur|Le rideau s'éloigne, sans bruit.",
            "enfant-f|On le fait voler, après.",
            "narrateur|Un éclat de canapé tient sur le tissu.",
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
    if "ouvre la bouche" not in blob:
        raise SystemExit(f"{SID}: manque ouvre la bouche")
    if "referme la bouche" not in blob:
        raise SystemExit(f"{SID}: manque referme la bouche")
    if "maintenant" not in blob:
        raise SystemExit(f"{SID}: manque maintenant")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Mila = enfant-f, Victorino = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Victorino absent (copain)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "enfant-f|" not in blob:
        raise SystemExit(f"{SID}: Mila absente (enfant-f)")
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
        "on peut laisser",
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
        "tu as laissé le temps",
        "on laisse le temps",
        "laisser le temps",
        "on attend la fin",
        "on n'achève pas",
        "on écoute jusqu'au bout",
        "cherche un mot",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Victorino cherche un mot. Que fait Mila ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    src_q = next(c for c in src["chunks"] if c["chunk_id"] == "CHK_T0000_P0000_Q0001")
    for fld in ("expected_answer", "accepted_examples", "retry_prompt"):
        if q.get(fld) != src_q.get(fld):
            raise SystemExit(f"{SID}: {fld} altéré (dump laissé tel quel)")
    n_copain = sum(
        1
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    )
    if n_copain < 2:
        raise SystemExit(f"{SID}: Victorino muet ({n_copain})")
    if "j'ai vu" not in blob:
        raise SystemExit(f"{SID}: manque j'ai vu (mot cherché)")
    for need in (
        "papillon",
        "canapé",
        "aile",
        "salon",
        "papier",
        "rideau",
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
        "éclat d'assiette",
        "éclat d'étal",
        "éclat de plateau",
        "éclat de carotte",
        "éclat de pupitre",
        "éclat de tapis",
        "faustine",
        "marceau",
        "hortense",
        "eliott",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "trois notes",
        "haricot",
        "châssis",
        "buée",
        "tapis",
        "assiette",
        "pupitre",
        "plateau",
        "carotte",
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
        "- **Leçon :** DIF.PAR.002 — chercher un mot, attendre (vécue : "
        "Mila connaît le mot, ouvre la bouche maintenant, Papillon trop "
        "tôt, sourire parti ; elle referme, attend ; 2e ruse Dis-le, "
        "ailes jaunes). JAMAIS dite dans le récit. Pas « on n'achève "
        "pas à sa place ». Pas « on peut laisser le temps ». Pas « tu "
        "as su attendre ».\n"
        "- **Personnages :** Mila, Victorino, papa, maman. Hortense/"
        "Eliott dump-xai → D16. Mila = enfant-f (veut faire voler le "
        "papillon maintenant, ouvre la bouche, puis referme). "
        "Victorino = copain (cherche un mot, j'ai vu, ailes, voler). "
        "Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** salon, canapé, papillon de papier, ailes jaunes, "
        "rideau, linge séché, fenêtre. ≠ 002-01 cuisine / carotte. ≠ "
        "002-02 pupitre. ≠ 002-03 salon plateau / tapis / chat. ≠ "
        "002-04 étal. ≠ 002-05 assiette. ≠ dump serviette / table / "
        "coussin.\n"
        "- **Indice unique :** éclat de canapé (brille à l'ouverture "
        "sur le tissu → tremble après Papillon trop tôt → luit au "
        "refus Dis-le → tient sur le tissu). BAN éclat d'assiette / "
        "étal / plateau / carotte / pupitre / tapis.\n"
        "- **Question moteur :** « Victorino cherche un mot. Que fait "
        "Mila ? » expected / accepted / retry **dump laissés tels "
        "quels** (pas inventés, pas mis à null). Non récitée dans les "
        "autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une aile jaune tremble sur le canapé. Sur le tissu, un éclat "
        "de canapé brille. Linge séché, rideau, papillon de papier. "
        "Mila veut le faire voler **maintenant**. Victorino arrive, "
        "dit j'ai vu, le mot reste coincé. Elle connaît, ouvre la "
        "bouche maintenant, Papillon trop tôt. Sourire parti. Papa "
        "s'accroupit. Elle referme la bouche. Elle attend. Merci vécu. "
        "Deuxième ruse : je le fais voler, Dis-le, lèvres serrées. "
        "Elle s'arrête, lit l'éclat. Un éclat de canapé tient sur le "
        "tissu.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon, canapé chaud, linge séché, aile de papier "
        "jaune, rideau, fenêtre. ≠ tapis / assiette / étal / plateau / "
        "carotte / pupitre. ≠ serviette / table dump.\n"
        "- Désir : faire voler le papillon de papier, maintenant, "
        "jusqu'à la fenêtre.\n"
        "- Objet : papillon de papier, ailes jaunes, canapé.\n"
        "- Indice unique : éclat de canapé, vu dès l'ouverture, payé "
        "sur le tissu. Pas éclat de tapis (BAN).\n"
        "- Urgence douce : Victorino arrive, Mila accélère le mot.\n"
        "- Imprévu 1 : Mila ouvre la bouche maintenant, le mot sort "
        "trop tôt. Victorino recule, lèvres serrées.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : elle pousse trop vite, Dis-le, il "
        "serre les lèvres, l'aile glisse.\n"
        "- Résolution : elle referme la bouche, observe, écoute le "
        "rideau, retrouve l'éclat, attend, il dit jaunes, puis voler.\n"
        "- Retour : papillon sur le canapé, éclat sur le tissu.\n\n"
        "## Vécu\n\n"
        "Mila veut le papillon **maintenant**. Impatience, puis mot "
        "trop tôt, sourire parti. Victorino pose sa limite (silence, "
        "recul, lèvres serrées, j'ai vu, papier, jaunes, voler). Papa "
        "se baisse, pose une question, ne récite pas la règle. Ils "
        "agissent : refermer la bouche, attendre, souffler sans se "
        "presser. Merci vécu. Fin : l'éclat du début tient sur le "
        "tissu.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Mila laisse le temps à Victorino (noyau laisse le "
        "temps, prénoms D16). Relance : Que fait Mila ? expected dump.\n"
        "- Lieu mission (salon, canapé, papillon de papier, ailes "
        "jaunes). Maman et papa. Mila = enfant-f. Victorino = copain. "
        "Hortense/Eliott dump-xai retirés. Dump plat « J'ai vu.. » "
        "réécrit en arc. Serviette / table / coussin retirés.\n"
        "- Ouverture inventée (bande chaude sur le canapé), pas un "
        "gabarit v2, pas « Un rayon traverse le salon tout entier ».\n"
        "- Indice unique : éclat de canapé. BAN éclat d'assiette / "
        "étal / plateau / carotte / pupitre / tapis. Pas tache/"
        "flèche/marque/symbole. Pas merle-trois-notes, pas miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « on peut laisser le temps » / « on n'achève "
        "pas » / « tu as su attendre » / bravo du dump.\n"
        "- Leçon non dite : on la voit quand le mot sort trop tôt, "
        "quand elle referme, quand elle attend, quand il finit. Pas "
        "« il faut attendre ». Pas « cherche un mot » hors question.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Victorino cherche un mot. Que fait "
        "Mila ? ». expected / accepted / retry dump laissés. 5 "
        "chunks, kinds inchangés.\n"
        "- example4 036 / 068 / 100 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_par_001_05.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers Dis-le.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n"
        "- 1 × `en ce moment`, 1 × merci adulte, 4 × éclat de canapé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
