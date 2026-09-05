#!/usr/bin/env python3
"""ATOM-DIF.PAR.001-07 — La pelle jaune près des pots (F-NAR-019, N2, DIF.PAR.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.PAR.001-07"
TITLE = "La pelle jaune près des pots"
N2 = LIMITS["N2"]
CHARS = "Chouchou, Mila, papa, maman"
SETTING = (
    "jardin, chaussures, paillasson, coccinelle, rambarde, "
    "pelle jaune, pots"
)
INDICE = "éclat de rambarde"
FIL = (
    "Les semelles tapent le paillasson. Une coccinelle avance "
    "sur la rambarde. Près d'elle, un éclat de rambarde brille. "
    "Chouchou veut la pelle jaune, maintenant, pour le pot. Mila "
    "ne dit rien. Trop vite, la pelle tape un pot. Sourire parti, "
    "poitrine, papa accroupi. Elle refuse de foncer, attend, tend "
    "la pelle. Merci vécu. Second pot trop vite. Un éclat de "
    "rambarde tient sur le fer."
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
    r"ballon|entrée|entree|horloge|bol|casserole|soupe|carotte|"
    r"chiffon|sauge|lacet|commode|gond|banc|coussin|confiture|"
    r"tartine|fraise|parquet|camion|tapis|seau|sable|gourde|"
    r"zinc|romarin|table|châssis|chassis|thym|haricot|buée|buee|"
    r"escargot|colline|arrosoir|merle|cigale|puzzle|locomotive|"
    r"wagon|chapeau)\b",
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
    "trois notes",
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
    "éclat de parquet",
    "éclat de zinc",
    "éclat de romarin",
    "éclat de table",
    "éclat de rond",
    "éclat de pot",
    "éclat de pelle",
    "éclat de paillasson",
    "éclat de chaussure",
    "éclat de coccinelle",
    "éclat de fer",
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
        emphasis="éclat de rambarde",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_pelle_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Chouchou",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=mila_parle_peu_que_fait_chouchou; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="pelle",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_refuse_de_foncer_attend_tend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de rambarde",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=second_pot_trop_vite_elle_attend; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de rambarde",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_fer; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "attendre",
    "accepted_examples": "attendre | tendre | la pelle | un jouet | elle attend",
    "retry_prompt": "Elle tend un jouet. Elle attend. Que fait Chouchou ?",
    "engine_ok_text": "Oui, attendre.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "paillasson",
        [
            "narrateur|Les semelles tapent le paillasson.",
            "narrateur|Ça fait un bruit de paille sèche.",
            "enfant-f|Ça gratte, papa.",
            "papa|Tes chaussures, Chouchou ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le paillasson sent l'herbe tiède.",
            "narrateur|Maman pose les chaussures près du mur.",
            "narrateur|Les semelles sont un peu poussiéreuses.",
            "maman|Tu les sens, les chaussures ?",
            "enfant-f|Elles sentent le jardin.",
            "narrateur|Une coccinelle avance sur la rambarde.",
            "enfant-f|Elle marche, maman.",
            "maman|Tu la vois, la petite bête ?",
            "enfant-f|Oui, rouge.",
            "narrateur|Près d'elle, un éclat de rambarde brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Un pot terreux attend près du mur.",
            "narrateur|La terre est grise, un peu sèche.",
            "enfant-f|Je veux la pelle, maintenant !",
            "enfant-f|Pour le pot, tout de suite.",
            "papa|La pelle jaune, là ?",
            "enfant-f|Oui, la jaune.",
            "maman|Le pot est près du mur ?",
            "enfant-f|Il doit se remplir.",
            "narrateur|En ce moment, Chouchou tient la pelle jaune.",
            "enfant-f|Le manche est lisse.",
            "papa|Tu la tiens, Chouchou ?",
            "enfant-f|Oui.",
            "narrateur|La porte du jardin s'ouvre.",
            "narrateur|Mila arrive près des pots.",
            "narrateur|Elle regarde le sol.",
            "narrateur|Elle ne dit rien.",
            "enfant-f|Tu creuses avec moi ?",
            "narrateur|Mila serre les mains.",
            "narrateur|Chouchou a envie de tout raconter.",
            "narrateur|Les mots montent très vite.",
            "enfant-f|La coccinelle !",
            "enfant-f|Le pot !",
            "enfant-f|La pelle !",
            "narrateur|Chouchou pousse trop vite vers elle.",
            "narrateur|La pelle tape un pot.",
            "enfant-f|Oh.",
            "narrateur|Le pot penche sur le paillasson.",
            "enfant-f|Le pot.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Mila, Chouchou ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains tiennent la pelle, Chouchou ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de rambarde tremble, puis tient.",
            "narrateur|Mila reste près des pots.",
            "enfant-f|Elle ne dit rien, papa.",
            "narrateur|Chouchou regarde papa.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Mila parle peu.",
            "narrateur|Que fait Chouchou ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "pots",
        [
            "narrateur|Chouchou veut la pelle, tout de suite.",
            "enfant-f|Je la pousse, maintenant !",
            "narrateur|Elle avance trop vite vers Mila.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "narrateur|Mila baisse les yeux.",
            "narrateur|Elle serre les mains contre elle.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Chouchou refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe la pelle, un instant.",
            "narrateur|Elle écoute la coccinelle sur le fer.",
            "papa|Tu veux le pot avec Mila ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Papa, on fait quoi ?",
            "papa|On pose la pelle, puis on reste.",
            "enfant-f|D'accord.",
            "narrateur|Chouchou reste un moment, les mains ouvertes.",
            "narrateur|Elle attend.",
            "narrateur|Elle tend la pelle.",
            "enfant-f|Pour toi.",
            "narrateur|Mila ne dit rien.",
            "narrateur|Elle prend la pelle, sans parler.",
            "copine|Oui.",
            "narrateur|Chouchou pose les mains près du pot.",
            "narrateur|Elle reste, sans se presser.",
            "narrateur|Mila pousse la terre, plus lentement.",
            "papa|Merci, Chouchou.",
            "narrateur|Papa a vu les deux, près des pots.",
            "maman|La terre est tiède, sous les doigts.",
            "enfant-f|Elle est chaude.",
            "narrateur|Le pot se remplit, un peu de travers.",
            "enfant-f|Le pot.",
            "papa|Il a de la terre, là ?",
            "enfant-f|Oui, là.",
            "narrateur|Chouchou glisse la main sur le bord.",
            "narrateur|L'argile est douce, contre la peau.",
            "maman|Tes mains sont au chaud, Chouchou ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Mila s'assoit, puis se relève.",
            "copine|Terre.",
            "enfant-f|On va jusqu'au bord ?",
            "maman|Le pot va jusqu'au paillasson.",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pelle",
        [
            "narrateur|Ils restent près des pots.",
            "narrateur|Un second pot attend, vide.",
            "enfant-f|Il se remplit, maintenant !",
            "narrateur|Chouchou pousse trop vite.",
            "narrateur|La terre penche vers le paillasson.",
            "enfant-f|Ça tombe !",
            "narrateur|Mila tend les mains, sans parler.",
            "narrateur|Chouchou avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Chouchou refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe la pelle, un instant.",
            "narrateur|Elle écoute le silence du jardin.",
            "narrateur|Sur la rambarde, un éclat de rambarde luit.",
            "enfant-f|Là, sur le fer.",
            "enfant-f|Tu prends la pelle, Mila ?",
            "narrateur|Mila ne dit rien.",
            "narrateur|Elle tend les mains, sans parler.",
            "copine|Oui.",
            "narrateur|Chouchou pousse la pelle, sans se presser.",
            "narrateur|Mila la reçoit, plus lentement.",
            "narrateur|Le manche est lisse et tiède.",
            "papa|Tu la vois, la pelle ?",
            "enfant-f|Oui, papa.",
            "maman|Les pots sont près du paillasson ?",
            "enfant-f|Oui, maman.",
            "narrateur|La terre entre dans le second pot.",
            "narrateur|Chouchou pose une main sur le bord.",
            "narrateur|Mila pose la suivante.",
            "papa|Le pot tient, Chouchou ?",
            "enfant-f|Oui, papa.",
            "maman|Une coccinelle passe sur la rambarde.",
            "enfant-f|Elle reste sur le fer.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près des pots.",
            "maman|Le pot est rempli, Chouchou ?",
            "enfant-f|Oui, maman.",
            "papa|Tu souffles un peu ?",
            "enfant-f|Oui, papa.",
            "narrateur|Chouchou souffle, un filet d'air.",
            "enfant-f|La terre sent bon.",
            "maman|Tu la sens, la terre ?",
            "enfant-f|Oui, maman.",
            "papa|Le pot reste un peu, de travers.",
            "enfant-f|Il a tenu, près des pots.",
            "copine|Terre.",
            "narrateur|Le paillasson est chaud, sous les mains.",
            "narrateur|La pelle jaune fait de l'ombre.",
            "enfant-f|On y retourne, après.",
            "narrateur|Un éclat de rambarde tient sur le fer.",
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
    if "tend la pelle" not in blob:
        raise SystemExit(f"{SID}: manque tend la pelle")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Chouchou = enfant-f, Mila = copine)")
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
        "parle peu",
        "elle parle peu",
        "forcer la parole",
        "tu as su attendre",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Mila parle peu. Que fait Chouchou ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "attendre | tendre | la pelle | un jouet | elle attend"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Elle tend un jouet. Elle attend. Que fait Chouchou ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    n_copine = sum(
        1
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    )
    if n_copine > 5:
        raise SystemExit(f"{SID}: Mila parle trop ({n_copine})")
    if n_copine < 2:
        raise SystemExit(f"{SID}: Mila trop muette ({n_copine})")
    if "pelle jaune" not in blob:
        raise SystemExit(f"{SID}: manque pelle jaune")
    if "paillasson" not in blob:
        raise SystemExit(f"{SID}: manque paillasson")
    if "coccinelle" not in blob:
        raise SystemExit(f"{SID}: manque coccinelle")
    if "chaussure" not in blob:
        raise SystemExit(f"{SID}: manque chaussures")
    if "rambarde" not in blob:
        raise SystemExit(f"{SID}: manque rambarde")
    if "ne dit rien" not in blob:
        raise SystemExit(f"{SID}: manque silence vécu")
    for ban in (
        "éclat de zinc",
        "éclat de romarin",
        "éclat de table",
        "éclat de rond",
        "éclat de banc",
        "éclat de parquet",
        "éclat de pot",
        "éclat de pelle",
        "éclat de paillasson",
        "tout doux",
        "tout calme",
        "escargot",
        "colline",
        "gwenaëlle",
        "gwenaelle",
        "hervé",
        "herve",
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
        "- **Leçon :** DIF.PAR.001 — quand l'autre parle peu, on attend, "
        "on tend le jouet (vécue : pelle trop vite, sourire parti, elle "
        "refuse de foncer, attend, tend la pelle, Mila prend sans "
        "parler). JAMAIS dite dans le récit. Pas « il faut attendre ». "
        "Pas « elle parle peu » hors question moteur.\n"
        "- **Personnages :** Chouchou, Mila, papa, maman. Dump Gwenaëlle/"
        "Hervé → D16. Chouchou = enfant-f (veut la pelle maintenant, trop "
        "vite, puis refuse de foncer). Mila = copine (parle peu, "
        "regarde le sol, oui, terre). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** jardin, chaussures, paillasson, coccinelle, "
        "rambarde, pelle jaune, pots. ≠ PAR.001-01 parquet / camion. ≠ "
        "PAR.001-02 banc / seau. ≠ dump escargot / nappe / colline.\n"
        "- **Indice unique :** éclat de rambarde (brille à l'ouverture "
        "sous la coccinelle → tremble au pot penché → luit au refus "
        "second pot → tient sur le fer). BAN éclat de zinc / romarin / "
        "table / rond / banc / parquet.\n"
        "- **Question moteur :** « Mila parle peu. Que fait "
        "Chouchou ? » expected **attendre**. accepted `attendre | tendre "
        "| la pelle | un jouet | elle attend`. retry dump. "
        "Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Les semelles tapent le paillasson. Une coccinelle avance sur "
        "la rambarde. Près d'elle, un éclat de rambarde brille. Pelle "
        "jaune, pot terreux. Chouchou veut la pelle **maintenant**. Mila "
        "arrive, ne dit rien. Chouchou pousse trop vite, la pelle tape "
        "un pot. Sourire parti. Papa s'accroupit. Elle refuse de foncer. "
        "Elle attend, tend la pelle. Merci vécu. Deuxième ruse : second "
        "pot trop vite, la terre penche. Elle s'arrête, lit l'éclat. Un "
        "éclat de rambarde tient sur le fer.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin, chaussures, paillasson, coccinelle, rambarde, "
        "pelle jaune, pots. ≠ PAR zinc / romarin / table / rond / banc / "
        "parquet. ≠ dump escargot / nappe.\n"
        "- Désir : la pelle jaune, maintenant, pour remplir le pot.\n"
        "- Objet : pelle jaune, pots, paillasson, chaussures.\n"
        "- Indice unique : éclat de rambarde, vu dès l'ouverture sous "
        "la coccinelle, payé sur le fer. Pas éclat de pot / pelle.\n"
        "- Urgence douce : Mila arrive, Chouchou accélère les mots.\n"
        "- Imprévu 1 : Chouchou pousse trop vite, la pelle tape un pot, "
        "le pot penche. Mila ne dit rien.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le geste.\n"
        "- Imprévu 2 (plus rusé) : second pot, trop vite, la terre "
        "penche vers le paillasson.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le "
        "silence, retrouve l'éclat, tend, Mila reçoit.\n"
        "- Retour : pot de travers, terre vécue, éclat sur le fer.\n\n"
        "## Vécu\n\n"
        "Chouchou veut la pelle **maintenant**. Impatience, puis pot "
        "qui penche, sourire parti. Mila pose sa limite (yeux bas, "
        "silence, oui, terre). Papa se baisse, pose une question, "
        "ne récite pas la règle. Elles agissent : attendre, tendre la "
        "pelle, pousser sans se presser. Merci vécu. Fin : l'éclat du "
        "début tient sur le fer.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : La pelle jaune près des pots (roster). Relance : "
        "Que fait Chouchou ? expected attendre.\n"
        "- Lieu du dump (jardin, rambarde) sans escargot / nappe / "
        "colline. Maman présente. Mila = copine.\n"
        "- Ouverture inventée (semelles sur le paillasson), pas un "
        "gabarit v2, pas « Un escargot avance sur la rambarde » du dump "
        "en première ligne.\n"
        "- Indice unique : éclat de rambarde. BAN éclat de zinc / "
        "romarin / table / rond / banc / parquet. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » / « escargot » du "
        "dump.\n"
        "- Leçon non dite : on la voit quand le pot penche, quand "
        "Chouchou s'arrête, quand elle tend, quand Mila prend sans "
        "parler. Pas « il faut attendre ». Pas « elle parle peu » hors "
        "question. Pas « on peut attendre » hors retry label.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Mila parle peu. Que "
        "fait Chouchou ? ». expected attendre. retry dump. 5 chunks, "
        "kinds inchangés.\n"
        "- example4 030 / 062 / 094 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_par_001_01.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le second pot.\n"
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
