#!/usr/bin/env python3
"""ATOM-EMO.GES.001-04 — Mila dit stop au salon (F-NAR-019, N2, EMO.GES.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.001-04"
TITLE = "Mila dit stop au salon"
N2 = LIMITS["N2"]
CHARS = "Mila, Chouchou, papa, maman"
SETTING = (
    "maison, salon, table, plaid, bois, fenêtre, rayon, "
    "savon, pli, cachette"
)
INDICE = "éclat de plaid"
FIL = (
    "Le plaid rouge tient un pli sur la table. Près du pli, un "
    "éclat de plaid brille. Mila veut jouer, maintenant. "
    "Chouchou ouvre les bras, serre trop. Sourire parti, "
    "poitrine, papa accroupi. Stop, recule. Merci vécu. "
    "Pli trop vite, bras derrière le tissu. Elle s'arrête, "
    "lit l'éclat. Un éclat de plaid tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tapis|coussin|canapé|canape|lampe|toboggan|balançoire|"
    r"balancoire|rideau|banc|sable|seau|parc|portail|gouttière|"
    r"gouttiere|cabane|thé|tasse|plateau|cacao|dessin|livre|"
    r"horloge|parquet|chaise|tiroir|nappe|drap|ballon|entrée|"
    r"entree|casserole|soupe|carotte|chiffon|commode|gond|"
    r"confiture|fraise|camion|pupitre|rambarde|pelle|gourde|"
    r"flaque|piquet|rotin|crochet|platane|cageot|résine|resine|"
    r"botte|bottes|limace|perron|fraisier|cuivre|buis|cerceau|"
    r"grille|cour|pierre|figue|robinet|planche|émail|email|"
    r"samare|bassine|lunettes|corde|sauge|lacet)\b",
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
    "dire stop",
    "c'est permis",
    "on s'éloigne",
    "on s eloigne",
    "on va vers un adulte",
    "vers un adulte",
    "tu as dit stop",
    "elle peut s'éloigner",
    "elle peut s eloigner",
    "c'est le bon geste",
    "tu as repris le geste",
    "tu t'es éloignée",
    "tu t es eloignee",
    "tu es venu vers moi",
    "tu es venue vers moi",
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
        emphasis="éclat de plaid",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis gêne; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_jouer_maintenant; "
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
            "sous_texte=cest_trop_pour_mila_que_dit_elle; "
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
            "emotion=gêne puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_dit_stop_elle_recule; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de plaid",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=pli_trop_vite_bras_derriere_elle_recule; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de plaid",
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
    "expected_answer": "stop",
    "accepted_examples": (
        "stop | s'éloigner | maman | adulte | vers maman"
    ),
    "retry_prompt": "Mila dit stop. Puis elle va où ?",
    "engine_ok_text": "Oui, stop.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "",
        [
            "narrateur|Le plaid rouge tient un pli sur la table.",
            "narrateur|Ça sent le savon, un peu.",
            "enfant-f|Ça sent bon, papa.",
            "papa|Tu le sens, le savon, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un rayon glisse sur le pli.",
            "enfant-f|Il brille, maman.",
            "maman|Le plaid est chaud ?",
            "enfant-f|Un peu, maman.",
            "maman|La cachette va commencer.",
            "maman|Le plaid et la table, d'accord ?",
            "enfant-f|Oui, maman.",
            "narrateur|Un fil de laine pend vers le bois.",
            "enfant-f|Il pend, papa.",
            "papa|Tu le vois, le fil ?",
            "enfant-f|Oui.",
            "narrateur|La laine est douce contre la peau.",
            "enfant-f|Elle pique, maman.",
            "maman|Tu la sens, la laine ?",
            "enfant-f|Oui.",
            "narrateur|Près du pli, un éclat de plaid brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Une poussière danse au-dessus du plaid.",
            "enfant-f|Elle vole, maman.",
            "maman|Au-dessus du pli ?",
            "enfant-f|Oui, au-dessus.",
            "narrateur|Chouchou pose les mains sur le plaid.",
            "narrateur|Le tissu est un peu lourd.",
            "enfant-f|On fait la cachette, Chouchou ?",
            "narrateur|Chouchou serre le bord.",
            "narrateur|Le pli tombe un peu.",
            "enfant-f|C'est rouge, papa.",
            "papa|Comme une maison ?",
            "enfant-f|Oui, comme une maison.",
            "narrateur|En ce moment, Mila tire le plaid vers la table.",
            "enfant-f|Je veux jouer, maintenant !",
            "enfant-f|La cachette, tout de suite.",
            "papa|Tu vois Chouchou, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Chouchou ouvre les bras.",
            "narrateur|Elle serre Mila trop fort.",
            "narrateur|Les bras collent trop près.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules montent un peu.",
            "papa|Elle serre, Mila ?",
            "enfant-f|Oui, papa.",
            "maman|Tes lèvres sont serrées, Mila ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de plaid tremble, puis tient.",
            "narrateur|Chouchou tient Mila contre elle.",
            "enfant-f|C'est trop, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Mila regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|C'est trop pour Mila.",
            "narrateur|Que dit-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Mila veut la cachette, tout de suite.",
            "enfant-f|Je joue, maintenant !",
            "narrateur|Elle avance trop vite vers Chouchou.",
            "narrateur|Les bras de Chouchou se referment.",
            "narrateur|Mila baisse les yeux.",
            "narrateur|Sa poitrine est coincée.",
            "enfant-f|C'est trop.",
            "enfant-f|Stop.",
            "narrateur|Mila recule d'un pas.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le plaid, un instant.",
            "narrateur|Elle écoute le silence du salon.",
            "papa|Tu veux la cachette avec Chouchou ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Papa, on fait quoi ?",
            "papa|On laisse un peu d'air ?",
            "enfant-f|D'accord.",
            "narrateur|Mila reste un moment, les bras ouverts.",
            "narrateur|Elle recule, plus loin.",
            "narrateur|Chouchou souffle.",
            "copine|La cachette.",
            "enfant-f|J'aime la cachette.",
            "narrateur|Chouchou pose le plaid sur la table.",
            "papa|Merci, Mila.",
            "narrateur|Papa a vu les deux, au salon.",
            "maman|Le tissu est tiède, sous les doigts.",
            "enfant-f|Il est chaud.",
            "narrateur|Le pli tient, un peu de travers.",
            "enfant-f|La cachette.",
            "papa|Elle a un toit, là ?",
            "enfant-f|Oui, là.",
            "narrateur|Mila glisse la main près du plaid.",
            "narrateur|La laine est douce, contre la peau.",
            "maman|Tes mains sont au chaud, Mila ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Chouchou s'assoit, puis se relève.",
            "copine|Oui.",
            "enfant-f|On le pose au bord ?",
            "maman|Le plaid va jusqu'à la table.",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Ils restent près de la table.",
            "narrateur|Le plaid tombe d'un côté.",
            "enfant-f|Le toit, maintenant !",
            "narrateur|Mila tire le plaid trop vite.",
            "narrateur|Le pli cache son visage.",
            "enfant-f|Je ne vois plus !",
            "narrateur|Chouchou ouvre les bras, derrière le tissu.",
            "narrateur|Elle serre trop fort, cette fois.",
            "enfant-f|Stop !",
            "narrateur|Mila recule d'un pas, sous le plaid.",
            "narrateur|Chouchou serre les lèvres.",
            "narrateur|Mila avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Mila recule, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le pli, un instant.",
            "narrateur|Elle écoute le silence du salon.",
            "narrateur|Au bord du pli, un éclat de plaid luit.",
            "enfant-f|Là, sur le plaid.",
            "enfant-f|Tu veux la cachette, Chouchou ?",
            "narrateur|Chouchou ne serre plus.",
            "narrateur|Elle tend les mains, sans coller.",
            "copine|Je veux la cachette.",
            "narrateur|Mila tire le plaid, sans se presser.",
            "narrateur|Chouchou le reçoit, plus loin.",
            "narrateur|Le tissu est lisse et tiède.",
            "papa|Tu le vois, le pli ?",
            "enfant-f|Oui, papa.",
            "maman|La cachette est près de la table ?",
            "enfant-f|Oui, maman.",
            "narrateur|Chouchou pose un bord.",
            "narrateur|Mila pose une main sur le bois.",
            "papa|Le pli tient, Mila ?",
            "enfant-f|Oui, papa.",
            "maman|Un rayon passe sur le plaid.",
            "enfant-f|Il allume le bois.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la table.",
            "maman|La cachette est arrivée, Mila ?",
            "enfant-f|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila souffle, un filet d'air.",
            "enfant-f|Le plaid sent le savon.",
            "maman|Tu le sens, le savon ?",
            "enfant-f|Oui, maman.",
            "papa|Le pli reste un peu, de travers.",
            "enfant-f|Il a tenu, sur la table.",
            "copine|La cachette.",
            "narrateur|Le plaid est chaud, sous les mains.",
            "narrateur|Le pli rouge fait de l'ombre.",
            "enfant-f|On y retourne, après.",
            "narrateur|Un éclat de plaid tient sur le bois.",
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
    if "stop" not in blob:
        raise SystemExit(f"{SID}: manque stop")
    if "recule" not in blob:
        raise SystemExit(f"{SID}: manque recule")
    if "serre" not in blob:
        raise SystemExit(f"{SID}: manque serre")
    if "poitrine" not in blob:
        raise SystemExit(f"{SID}: manque poitrine")
    if "accroupit" not in blob:
        raise SystemExit(f"{SID}: manque accroupit")
    if "derrière" not in blob and "derriere" not in blob:
        raise SystemExit(f"{SID}: manque 2e ruse (derrière le tissu)")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Mila = enfant-f, Chouchou = copine)")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Chouchou absente (copine)")
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
        "dire stop, c'est permis",
        "dire stop c'est permis",
        "on s'éloigne",
        "on s eloigne",
        "on va vers un adulte",
        "vers un adulte",
        "tu as dit stop",
        "elle peut s'éloigner",
        "c'est le bon geste",
        "tu as repris le geste",
        "bravo",
        "on peut jouer",
        "il faut reculer",
        "on doit reculer",
        "on recule",
        "c'est permis",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "C'est trop pour Mila. Que dit-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "stop":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "stop | s'éloigner | maman | adulte | vers maman"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Mila dit stop. Puis elle va où ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    n_copine = sum(
        1
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    )
    if n_copine > 6:
        raise SystemExit(f"{SID}: Chouchou parle trop ({n_copine})")
    if "plaid" not in blob:
        raise SystemExit(f"{SID}: manque plaid")
    if "salon" not in blob:
        raise SystemExit(f"{SID}: manque salon")
    if "table" not in blob:
        raise SystemExit(f"{SID}: manque table")
    if "jouer" not in blob:
        raise SystemExit(f"{SID}: manque jouer (désir)")
    if "maintenant" not in blob:
        raise SystemExit(f"{SID}: manque maintenant")
    for ban in (
        "éclat de tapis",
        "éclat de coussin",
        "éclat de canapé",
        "éclat de lampe",
        "éclat de toboggan",
        "éclat de balançoire",
        "éclat de rideau",
        "éclat de livre",
        "éclat de plateau",
        "tout doux",
        "tout calme",
        "zélie",
        "lila",
        "sarah",
        "victorina",
        "nino",
        "tapis",
        "coussin",
        "canapé",
        "lampe",
        "toboggan",
        "balançoire",
        "rideau",
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
        "- **Leçon :** EMO.GES.001 — trop fort → stop, reculer (vécue : "
        "Mila veut jouer **maintenant**, Chouchou serre trop, poitrine, "
        "sourire parti, papa accroupi ; elle dit stop, recule ; 2e ruse "
        "derrière le tissu). JAMAIS dite dans le récit. Pas « dire stop, "
        "c'est permis ». Pas « on s'éloigne ». Pas « on va vers un "
        "adulte ».\n"
        "- **Personnages :** Mila, Chouchou, papa, maman. Dump Zélie/"
        "Lila/maman → D16. Mila = enfant-f (veut jouer maintenant, trop "
        "vite, puis stop et recule). Chouchou = copine (câlin trop fort, "
        "puis mains ouvertes). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** maison, salon, table, plaid, bois, fenêtre, rayon, "
        "savon, pli, cachette. ≠ 001-03 parc / toboggan / banc / sable. "
        "≠ dump tapis / coussin / canapé / lampe / gouttière.\n"
        "- **Indice unique :** éclat de plaid (brille à l'ouverture "
        "près du pli → tremble quand Chouchou trop fort → luit au "
        "refus derrière le tissu → tient sur le bois). BAN éclat de "
        "tapis / coussin / canapé / lampe / toboggan / balançoire / "
        "rideau.\n"
        "- **Question moteur :** « C'est trop pour Mila. Que dit-elle "
        "? » expected **stop**. accepted dump `stop | s'éloigner | "
        "maman | adulte | vers maman`. retry dump (Zélie → Mila). "
        "expected/accepted/retry des autres chunks restent **null**. "
        "Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le plaid rouge tient un pli sur la table. Près du pli, un "
        "éclat de plaid brille. Fil de laine, savon, rayon. Mila veut "
        "jouer **maintenant**. Chouchou ouvre les bras, serre trop. "
        "Sourire parti. Papa s'accroupit. Elle dit stop, recule. Merci "
        "vécu. Deuxième ruse : pli trop vite, visage caché, bras "
        "derrière le tissu. Elle s'arrête, lit l'éclat. Un éclat de "
        "plaid tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : maison, salon, table, plaid, bois, fenêtre, rayon, "
        "savon. ≠ dump tapis / coussin / canapé / lampe. ≠ parc / "
        "toboggan / balançoire / rideau.\n"
        "- Désir : jouer maintenant, faire la cachette sous le plaid.\n"
        "- Objet : plaid rouge, pli, table, cachette.\n"
        "- Indice unique : éclat de plaid, vu dès l'ouverture près "
        "du pli, payé sur le bois. Pas éclat de tapis.\n"
        "- Urgence douce : Mila accélère, Chouchou serre.\n"
        "- Imprévu 1 : Chouchou ouvre les bras trop vite, serre. "
        "Poitrine coincée, sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : pli trop vite, visage caché, "
        "bras derrière le tissu.\n"
        "- Résolution : elle dit stop, recule, observe, écoute, "
        "retrouve l'éclat, Chouchou tend les mains sans coller.\n"
        "- Retour : pli de travers, savon, éclat sur le bois.\n\n"
        "## Vécu\n\n"
        "Mila veut jouer **maintenant**. Impatience, puis câlin trop "
        "fort, sourire parti. Chouchou pose sa limite (souffle, puis "
        "mains ouvertes). Papa se baisse, pose une question, ne "
        "récite pas la règle. Elles agissent : stop, reculer. Merci "
        "vécu. Fin : l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Mila dit stop au salon (noyau + D16). Relance : "
        "Que dit-elle ? expected stop.\n"
        "- Lieu du dump (salon, plaid) sans tapis / coussin / canapé "
        "/ lampe / gouttière. Papa présent. Chouchou = copine.\n"
        "- Ouverture inventée (pli du plaid sur la table), pas un "
        "gabarit v2, pas « La gouttière chante » du dump en première "
        "ligne.\n"
        "- Indice unique : éclat de plaid. BAN éclat de tapis / "
        "coussin / canapé / lampe / toboggan / balançoire / rideau. "
        "Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « Le.. » / « encore » / « cabane de coussins "
        "» du dump. Une phrase par ligne, ponctuation, pas de puces.\n"
        "- Leçon non dite : on la voit quand Mila dit stop, recule, "
        "quand Chouchou ouvre les mains. Pas « dire stop, c'est "
        "permis ». Pas « on s'éloigne » hors question.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « C'est trop pour Mila. Que dit-elle "
        "? ». expected stop. retry dump (Mila). 5 chunks, kinds "
        "inchangés. expected/accepted/retry null hors Q.\n"
        "- example4 041 / 073 / 005 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_par_002_03.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le pli.\n"
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
