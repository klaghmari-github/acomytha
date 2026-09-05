#!/usr/bin/env python3
"""ATOM-DIF.PAR.002-03 — Nina laisse le temps à Aniss (F-NAR-019, N2, DIF.PAR.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.002-03"
TITLE = "Nina laisse le temps à Aniss"
N2 = LIMITS["N2"]
CHARS = "Nina, Aniss, papa, maman"
SETTING = (
    "maison, salon, goûter, plateau, cacao, dessin, "
    "crayon bleu, verre d'eau, table"
)
INDICE = "éclat de plateau"
FIL = (
    "Le plateau du goûter pose une ombre. Près du cacao, un "
    "éclat de plateau brille. Nina veut aider Aniss, maintenant. "
    "Le mot du dessin reste dedans. Nina ouvre la bouche trop "
    "vite. Sourire parti, poitrine, papa accroupi. Elle referme "
    "la bouche, attend. Merci vécu. Verre trop vite. Elle "
    "s'arrête, lit l'éclat. Un éclat de plateau tient sur le bois."
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
    r"ballon|entrée|entree|horloge|casserole|soupe|carotte|"
    r"chiffon|sauge|lacet|commode|gond|banc|coussin|confiture|"
    r"tartine|fraise|tapis|parquet|camion|seau|pupitre|rambarde|"
    r"sable|pelle|gourde)\b",
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
    "on laisse le temps",
    "laisser le temps",
    "tu as laissé le temps",
    "tu as laisse le temps",
    "on attend la fin",
    "tu as fini ta phrase",
    "vous parlez l'un après l'autre",
    "cherche ses mots",
    "chercher ses mots",
    "parle à sa place",
    "parler à sa place",
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
    "éclat de compote",
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
        emphasis="éclat de plateau",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_aider_maintenant; "
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
            "sous_texte=aniss_cherche_ses_mots_que_fait_nina; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="chat",
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
        emphasis="éclat de plateau",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=verre_trop_vite_elle_referme_la_bouche; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de plateau",
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
    "expected_answer": "attendre",
    "accepted_examples": (
        "attendre | laisser le temps | elle attend | le temps"
    ),
    "retry_prompt": "On laisse le temps. On attend la fin. Que fait Nina ?",
    "engine_ok_text": "Oui, attendre.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "",
        [
            "narrateur|Le plateau du goûter pose une ombre chaude sur la table.",
            "narrateur|Ça sent le cacao, un peu sucré.",
            "enfant-f|Ça sent bon, papa.",
            "papa|Tu le sens, le cacao, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|La vapeur danse au-dessus des tasses.",
            "enfant-f|Elle monte, maman.",
            "maman|Le cacao fume ?",
            "enfant-f|Oui.",
            "maman|Le goûter est prêt.",
            "maman|Cacao et compote, d'accord ?",
            "enfant-f|Oui, maman.",
            "narrateur|Un crayon bleu roule vers le bord.",
            "enfant-f|Il roule, papa.",
            "papa|Tu le rattrapes, Nina ?",
            "enfant-f|Oui.",
            "narrateur|La cuillère tinte contre le bol.",
            "enfant-f|Elle chante, maman.",
            "maman|Tu l'entends, la cuillère ?",
            "enfant-f|Oui.",
            "narrateur|Près du cacao, un éclat de plateau brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Une poussière danse au-dessus du plateau.",
            "enfant-f|Elle vole, maman.",
            "maman|Au-dessus du cacao ?",
            "enfant-f|Oui, au-dessus.",
            "narrateur|Aniss pose un dessin sur la table.",
            "narrateur|Le papier est un peu plié.",
            "enfant-f|C'est ton dessin, Aniss ?",
            "narrateur|Aniss serre le crayon.",
            "narrateur|Le crayon laisse une trace bleue.",
            "enfant-f|C'est bleu, papa.",
            "papa|Comme le ciel ?",
            "enfant-f|Oui, comme le ciel.",
            "narrateur|En ce moment, Nina se penche vers la feuille.",
            "enfant-f|Je veux aider, maintenant !",
            "enfant-f|Je connais le mot.",
            "papa|Tu vois Aniss, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Aniss ouvre la bouche.",
            "narrateur|Le mot reste dedans.",
            "narrateur|Ses épaules montent un peu.",
            "enfant-f|Le chat !",
            "narrateur|Nina ouvre la bouche trop vite.",
            "narrateur|Les mots montent.",
            "narrateur|Aniss baisse les yeux.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "papa|Il cherche, Nina ?",
            "enfant-f|Oui, papa.",
            "maman|Tes lèvres sont ouvertes, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de plateau tremble, puis tient.",
            "narrateur|Aniss tient le dessin contre lui.",
            "enfant-f|Il ne dit pas le mot, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Nina regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss cherche ses mots.",
            "narrateur|Que fait Nina ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Nina veut le mot, tout de suite.",
            "enfant-f|Je le dis, maintenant !",
            "narrateur|Elle avance trop vite vers Aniss.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "narrateur|Aniss baisse les yeux.",
            "narrateur|Il serre le dessin contre lui.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Nina ouvre la bouche.",
            "narrateur|Puis elle la referme.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le dessin, un instant.",
            "narrateur|Elle écoute la vapeur du cacao.",
            "papa|Tu veux le chat avec Aniss ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Papa, on fait quoi ?",
            "papa|On pose les mains, puis on reste.",
            "enfant-f|D'accord.",
            "narrateur|Nina reste un moment, les mains ouvertes.",
            "narrateur|Elle attend.",
            "narrateur|Aniss souffle.",
            "copain|Le chat bleu.",
            "enfant-f|J'aime le chat.",
            "narrateur|Aniss pose le dessin contre le plateau.",
            "papa|Merci, Nina.",
            "narrateur|Papa a vu les deux, au salon.",
            "maman|Le papier est tiède, sous les doigts.",
            "enfant-f|Il est chaud.",
            "narrateur|Le chat bleu tient, un peu de travers.",
            "enfant-f|Le chat.",
            "papa|Il a une oreille, là ?",
            "enfant-f|Oui, là.",
            "narrateur|Nina glisse la main près du dessin.",
            "narrateur|Le papier est doux, contre la peau.",
            "maman|Tes mains sont au chaud, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Aniss s'assoit, puis se relève.",
            "copain|Oui.",
            "enfant-f|On le pose au bord ?",
            "maman|Le plateau va jusqu'à la table.",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Ils restent près du plateau.",
            "narrateur|Un verre d'eau attend près du cacao.",
            "enfant-f|L'eau, maintenant !",
            "narrateur|Nina pousse le verre trop vite.",
            "narrateur|Une goutte penche vers le bois.",
            "enfant-f|Ça tombe !",
            "narrateur|Aniss ouvre la bouche.",
            "narrateur|Le mot reste dedans.",
            "enfant-f|Dis-le, Aniss !",
            "narrateur|Aniss serre les lèvres.",
            "narrateur|Nina avance les mots, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Nina referme la bouche, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le verre, un instant.",
            "narrateur|Elle écoute le silence du salon.",
            "narrateur|Au bord du cacao, un éclat de plateau luit.",
            "enfant-f|Là, sur le plateau.",
            "enfant-f|Tu veux le verre, Aniss ?",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Il tend les mains, sans parler.",
            "copain|Je veux de l'eau.",
            "narrateur|Nina pousse le verre, sans se presser.",
            "narrateur|Aniss le reçoit, plus lentement.",
            "narrateur|Le verre est lisse et froid.",
            "papa|Tu le vois, le verre ?",
            "enfant-f|Oui, papa.",
            "maman|Le cacao est près du plateau ?",
            "enfant-f|Oui, maman.",
            "narrateur|Aniss boit une gorgée.",
            "narrateur|Nina pose une main sur la table.",
            "papa|Le verre tient, Nina ?",
            "enfant-f|Oui, papa.",
            "maman|Un rayon passe sur le plateau.",
            "enfant-f|Il allume le bois.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du plateau.",
            "maman|Le chat est arrivé, Nina ?",
            "enfant-f|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina souffle, un filet d'air.",
            "enfant-f|Le cacao sent bon.",
            "maman|Tu le sens, le cacao ?",
            "enfant-f|Oui, maman.",
            "papa|Le dessin reste un peu, de travers.",
            "enfant-f|Il a tenu, sur la table.",
            "copain|Le chat.",
            "narrateur|Le plateau est chaud, sous les mains.",
            "narrateur|Le chat bleu fait de l'ombre.",
            "enfant-f|On y retourne, après.",
            "narrateur|Un éclat de plateau tient sur le bois.",
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
    if "ouvre la bouche" not in blob:
        raise SystemExit(f"{SID}: manque ouvre la bouche")
    if "referme" not in blob:
        raise SystemExit(f"{SID}: manque referme")
    if "elle attend" not in blob and "\nnarrateur|elle attend." not in blob:
        raise SystemExit(f"{SID}: manque elle attend")
    if "verre" not in blob:
        raise SystemExit(f"{SID}: manque verre (2e ruse)")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Nina = enfant-f, Aniss = copain)")
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
        "on laisse le temps",
        "laisser le temps",
        "on attend la fin",
        "tu as fini ta phrase",
        "cherche ses mots",
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
        "parle peu",
        "elle parle peu",
        "forcer la parole",
        "tu as su attendre",
        "parle à sa place",
        "parler à sa place",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Aniss cherche ses mots. Que fait Nina ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "attendre | laisser le temps | elle attend | le temps"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "On laisse le temps. On attend la fin. Que fait Nina ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    n_copain = sum(
        1
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    )
    if n_copain > 6:
        raise SystemExit(f"{SID}: Aniss parle trop ({n_copain})")
    if "cacao" not in blob:
        raise SystemExit(f"{SID}: manque cacao")
    if "dessin" not in blob:
        raise SystemExit(f"{SID}: manque dessin")
    if "goûter" not in blob and "gouter" not in blob:
        raise SystemExit(f"{SID}: manque goûter")
    if "salon" not in blob:
        raise SystemExit(f"{SID}: manque salon")
    for ban in (
        "éclat de tapis",
        "éclat de carotte",
        "éclat de pupitre",
        "éclat de rambarde",
        "éclat de parquet",
        "éclat de banc",
        "éclat d'horloge",
        "éclat de bol",
        "éclat de flaque",
        "éclat de piquet",
        "éclat de chiffon",
        "éclat de gond",
        "éclat de sauge",
        "éclat de lacet",
        "éclat de commode",
        "tout doux",
        "tout calme",
        "céleste",
        "sami",
        "nino",
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
        "- **Leçon :** DIF.PAR.002 — chercher un mot, attendre (vécue : "
        "Nina veut aider **maintenant**, ouvre la bouche, la referme, "
        "attend ; Aniss finit « le chat bleu » ; 2e ruse du verre). "
        "JAMAIS dite dans le récit. Pas « on laisse le temps ». Pas "
        "« cherche ses mots » hors question moteur.\n"
        "- **Personnages :** Nina, Aniss, papa, maman. Dump Céleste/"
        "Sami → D16. Nina = enfant-f (veut aider maintenant, trop "
        "vite, puis referme la bouche). Aniss = copain (cherche le "
        "mot, silence, chat bleu, verre d'eau). Troupe D16. Pas de "
        "maîtresse.\n"
        "- **Lieu :** maison, salon, goûter, plateau, cacao, dessin, "
        "crayon bleu, verre d'eau, table. ≠ PAR.001-01 camion / "
        "parquet. ≠ PAR.002-01 carotte. ≠ PAR.002-02 pupitre. ≠ "
        "dump tapis / horloge / Le..\n"
        "- **Indice unique :** éclat de plateau (brille à l'ouverture "
        "près du cacao → tremble quand Nina trop vite → luit au "
        "refus du verre → tient sur le bois). BAN éclat de tapis / "
        "carotte / pupitre / rambarde.\n"
        "- **Question moteur :** « Aniss cherche ses mots. Que fait "
        "Nina ? » expected **attendre**. accepted dump `attendre | "
        "laisser le temps | elle attend | le temps`. retry dump "
        "(Céleste → Nina). expected/accepted/retry des autres chunks "
        "restent **null**. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le plateau du goûter pose une ombre chaude. Près du cacao, un "
        "éclat de plateau brille. Dessin plié, crayon bleu, vapeur. "
        "Nina veut aider **maintenant**. Aniss ouvre la bouche, le mot "
        "reste. Nina dit trop vite « le chat ». Sourire parti. Papa "
        "s'accroupit. Elle ouvre la bouche, la referme, attend. Merci "
        "vécu. Deuxième ruse : verre trop vite, « dis-le », lèvres "
        "serrées. Elle s'arrête, lit l'éclat. Un éclat de plateau "
        "tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : maison, salon, goûter, plateau, cacao, dessin, "
        "verre d'eau. ≠ dump tapis / horloge. ≠ carotte / pupitre / "
        "rambarde.\n"
        "- Désir : aider Aniss, maintenant, finir le mot du dessin.\n"
        "- Objet : dessin du chat bleu, plateau, verre d'eau.\n"
        "- Indice unique : éclat de plateau, vu dès l'ouverture près "
        "du cacao, payé sur le bois. Pas éclat de tapis.\n"
        "- Urgence douce : Aniss cherche le mot, Nina accélère.\n"
        "- Imprévu 1 : Nina ouvre la bouche trop vite, dit le chat. "
        "Aniss baisse les yeux.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : verre trop vite, goutte, « dis-le ».\n"
        "- Résolution : elle referme la bouche, observe, écoute, "
        "retrouve l'éclat, Aniss dit le verre.\n"
        "- Retour : dessin de travers, cacao, éclat sur le bois.\n\n"
        "## Vécu\n\n"
        "Nina veut aider **maintenant**. Impatience, puis mot volé, "
        "sourire parti. Aniss pose sa limite (yeux bas, silence, puis "
        "le chat bleu, le verre). Papa se baisse, pose une question, "
        "ne récite pas la règle. Elles agissent : ouvrir, refermer, "
        "attendre. Merci vécu. Fin : l'éclat du début tient sur le "
        "bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Nina laisse le temps à Aniss (noyau + D16). Relance : "
        "Que fait Nina ? expected attendre.\n"
        "- Lieu du dump (salon, goûter, dessin, verre) sans tapis / "
        "horloge / Le.. Maman présente. Aniss = copain.\n"
        "- Ouverture inventée (ombre du plateau), pas un gabarit "
        "v2, pas « La lampe du salon fait une lune ronde sur le "
        "tapis » du dump en première ligne.\n"
        "- Indice unique : éclat de plateau. BAN éclat de tapis / "
        "carotte / pupitre / rambarde. Pas tache/flèche/marque/"
        "symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « Le.. » / « encore » / « horloge » du "
        "dump. Une phrase par ligne, ponctuation, pas de puces.\n"
        "- Leçon non dite : on la voit quand Nina ouvre, referme, "
        "attend, quand Aniss finit tout seul. Pas « on laisse le "
        "temps ». Pas « cherche ses mots » hors question.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Aniss cherche ses mots. Que fait "
        "Nina ? ». expected attendre. retry dump (Nina). 5 chunks, "
        "kinds inchangés. expected/accepted/retry null hors Q.\n"
        "- example4 033 / 065 / 097 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_par_001_01.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le verre.\n"
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
