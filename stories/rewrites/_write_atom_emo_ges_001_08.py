#!/usr/bin/env python3
"""ATOM-EMO.GES.001-08 — Raphaël dit stop et s'éloigne (F-NAR-019, N1, EMO.GES.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.001-08"
TITLE = "Raphaël dit stop et s'éloigne"
N1 = LIMITS["N1"]
CHARS = "Raphaël, Victorino, papa, maman"
SETTING = (
    "salon, plinthe, toupie rouge, sol, fenêtre, "
    "bois, cire, trait d'or"
)
INDICE = "éclat de plinthe"
FIL = (
    "Un trait d'or file le long du bois. Sur le bois, "
    "un éclat de plinthe luit. Raphaël veut jouer, "
    "maintenant. Victorino chatouille trop. Ventre trop "
    "vite. Sourire parti. Papa s'accroupit. Raphaël dit "
    "stop, recule d'un pas. Merci vécu. Deuxième ruse : "
    "Victorino chatouille trop près du ventre. Un éclat "
    "de plinthe tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tapis|canapé|canape|coussin|marelle|cadre|livre|plaid|"
    r"rideau|toboggan|balançoire|balancoire|flaque|grille|botte|"
    r"bottes|limace|perron|tiroir|fraisier|cuivre|buis|figue|"
    r"robinet|planche|émail|email|samare|bassine|entrée|entree|"
    r"merle|miel|piquet|cerceau|drap|savon|bol|feuille|pierre|"
    r"commode|lacet|sauge|chiffon|parquet|gond|portail|orange|"
    r"journal|pelure|clochette|assiette|étal|etal|plateau|"
    r"coquillage|banc|bac)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
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
    "il ne faut pas rire",
    "on ne rit pas",
    "il peut s'éloigner",
    "il peut s eloigner",
    "elle peut s'éloigner",
    "dire stop, c'est permis",
    "dire stop c'est permis",
    "on s'éloigne",
    "on s eloigne",
    "on va vers un adulte",
    "vers un adulte",
    "vers l'adulte",
    "c'est le bon geste",
    "c est le bon geste",
    "tu as dit stop",
    "tu t'es éloignée",
    "tu t'es éloigné",
    "tu te souviens",
    "tu as quitté le jeu",
    "tu as reculé",
    "tu as recule",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de pierre",
    "éclat de cerceau",
    "éclat de flaque",
    "éclat de grille",
    "éclat de cour",
    "éclat de botte",
    "éclat de portail",
    "éclat de feuille",
    "éclat de piquet",
    "éclat de commode",
    "éclat de lacet",
    "éclat de tapis",
    "éclat de sauge",
    "éclat de chiffon",
    "éclat de parquet",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de pin",
    "éclat de pomme",
    "éclat de sève",
    "éclat de seve",
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
    "éclat de plaque",
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
    "éclat de résine",
    "éclat de resine",
    "éclat de banc",
    "éclat de bac",
    "éclat de canapé",
    "éclat de canape",
    "éclat de gond",
    "éclat de marelle",
    "éclat de cadre",
    "éclat de livre",
    "éclat de plaid",
    "éclat de rideau",
    "éclat de toboggan",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de coquillage",
    "éclat de table",
    "éclat de lampe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de fenêtre",
    "éclat de fenetre",
    "éclat de bord",
    "éclat de rond",
    "éclat de toupie",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

# N1 : mêmes champs que DIF.PAR.002-07 (voix N1, tempos plus lents).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat de plinthe",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_jouer_maintenant; "
            "tempo=posé puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=104, speed=0.80, piper=1.36, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=780,
        sentence=360, energy="focused", contour="rising", noise=0.30,
        emphasis="Raphaël",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=c_est_trop_pour_raphael_que_dit_il; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=122, speed=0.88, piper=1.24, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=620,
        sentence=310, energy="bright", contour="falling", noise=0.33,
        emphasis="stop",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_dit_stop_il_recule; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de plinthe",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=victorino_chatouille_trop_pres_il_s_arrete; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de plinthe",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

# Dump Q : expected/accepted conservés ; Hippolyte → Raphaël.
Q_FIELDS = {
    "expected_answer": "stop",
    "accepted_examples": "stop | s'éloigner | papa | adulte | vers papa",
    "retry_prompt": "Raphaël dit stop. Puis il va où ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "",
        [
            "narrateur|Un trait d'or file le long du bois.",
            "enfant-m|Il est chaud, papa.",
            "papa|Tu le vois, le trait, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le bois de la plinthe sent la cire.",
            "maman|Ça sent la cire, ce soir.",
            "enfant-m|Oui, maman.",
            "narrateur|La fenêtre laisse un air tiède.",
            "papa|Tu sens l'air, Raphaël ?",
            "enfant-m|Oui, il est tiède.",
            "narrateur|Une toupie rouge attend sur le sol.",
            "narrateur|Elle a des ronds peints.",
            "enfant-m|Elle est rouge, maman.",
            "maman|Tu la vois, la toupie ?",
            "enfant-m|Oui.",
            "narrateur|Papa pose un doigt sur le bois.",
            "narrateur|Toc, toc, contre la plinthe.",
            "papa|Tu entends le bois, Raphaël ?",
            "enfant-m|Oui, il sonne.",
            "narrateur|Sur le bois, un éclat de plinthe luit.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-m|Oui, un petit point.",
            "papa|Le soleil le touche.",
            "narrateur|Raphaël pose la paume près du bois.",
            "narrateur|La plinthe est lisse, un peu froide.",
            "enfant-m|Elle est froide.",
            "maman|Tu la touches, Raphaël ?",
            "enfant-m|Oui.",
            "narrateur|En ce moment, Raphaël prend la toupie.",
            "enfant-m|Je veux jouer, maintenant !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les doigts serrent le bois peint.",
            "maman|Tu la fais tourner ?",
            "enfant-m|Oui, maman.",
            "narrateur|Victorino arrive près de la toupie.",
            "narrateur|Il avance les doigts trop vite.",
            "copain|Des chatouilles !",
            "enfant-m|Tu viens, Victorino ?",
            "copain|Oui.",
            "narrateur|Victorino chatouille le ventre de Raphaël.",
            "narrateur|Les doigts vont trop fort, trop longtemps.",
            "enfant-m|Oh.",
            "copain|Je te tiens.",
            "narrateur|Raphaël sent son ventre bouger trop vite.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans son ventre, ça se bouscule.",
            "narrateur|L'envie et la gêne se heurtent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Victorino, Raphaël ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains sont froides, Raphaël ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de plinthe tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|C'est trop pour Raphaël.",
            "narrateur|Que dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Raphaël veut la toupie, tout de suite.",
            "enfant-m|Je tourne, maintenant !",
            "narrateur|Victorino chatouille trop, trop près.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copain|Viens.",
            "narrateur|Victorino avance d'un pas.",
            "enfant-m|Stop.",
            "narrateur|Raphaël recule d'un pas.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Raphaël refuse de rester collé.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe la toupie, un instant.",
            "narrateur|Il écoute le bois de la plinthe.",
            "papa|Tu veux la toupie avec Victorino ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Tu restes un peu loin ?",
            "narrateur|Victorino ne dit rien, d'abord.",
            "narrateur|Il ouvre les mains, puis les baisse.",
            "copain|Je m'arrête.",
            "enfant-m|D'accord.",
            "papa|Merci, Raphaël.",
            "narrateur|Papa a vu les deux, près du bois.",
            "maman|La cire colle un peu, sous les doigts.",
            "enfant-m|Elle est tiède.",
            "narrateur|Raphaël essuie la toupie du plat de la main.",
            "narrateur|Victorino reste un pas plus loin.",
            "narrateur|La toupie part sans coller, cette fois.",
            "enfant-m|Elle tourne !",
            "copain|Oui.",
            "papa|Tu la vois, la toupie ?",
            "enfant-m|Oui, papa.",
            "maman|Tu pousses, Victorino ?",
            "copain|J'y vais.",
            "narrateur|Raphaël lance, sans se presser.",
            "narrateur|Victorino suit la toupie des yeux.",
            "narrateur|La toupie danse une fois.",
            "copain|Un.",
            "enfant-m|Deux.",
            "narrateur|Le ventre de Raphaël se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près de la plinthe ?",
            "enfant-m|Oui.",
            "maman|Tes mains sont au chaud ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Maman approche la toupie.",
            "narrateur|Elle la tend vers Victorino.",
            "enfant-m|Je joue, maintenant !",
            "narrateur|Victorino court trop, tout de suite.",
            "narrateur|Il chatouille trop près du ventre.",
            "copain|Avec moi !",
            "narrateur|La toupie penche vers Victorino.",
            "enfant-m|Elle penche !",
            "narrateur|Raphaël avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Raphaël refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe la toupie, un instant.",
            "narrateur|Il écoute le bois de la plinthe.",
            "narrateur|Sur le bois, un éclat de plinthe luit.",
            "enfant-m|Là, sur le bois.",
            "enfant-m|Stop.",
            "narrateur|Raphaël recule d'un pas.",
            "narrateur|Victorino ne dit rien.",
            "narrateur|Il souffle, puis recule aussi.",
            "copain|Oui.",
            "papa|On tient la toupie ?",
            "enfant-m|Oui, papa.",
            "narrateur|La toupie sent le bois peint.",
            "narrateur|Le bois est là, un peu tiède.",
            "narrateur|Raphaël la pousse vers Victorino.",
            "narrateur|Victorino la rend, sans se coller.",
            "enfant-m|Vzz.",
            "copain|Vzz.",
            "papa|La toupie est bien calme ?",
            "enfant-m|Oui, papa.",
            "maman|La cire est chaude, Victorino ?",
            "copain|Un peu.",
            "narrateur|Ils poussent la toupie, à un pas.",
            "narrateur|Le sol chatouille les genoux.",
            "enfant-m|C'est plus facile.",
            "papa|La plinthe est calme ?",
            "enfant-m|Oui, papa.",
            "maman|Un trait d'or passe sur le bois.",
            "enfant-m|Il allume la plinthe.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la plinthe.",
            "narrateur|Maman essuie un peu de cire.",
            "enfant-m|La toupie a penché, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-m|Oui, près de la plinthe.",
            "maman|On est bien, ici.",
            "narrateur|Raphaël tapote le bois du doigt.",
            "enfant-m|Il a une trace de cire.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|La toupie est restée, Raphaël.",
            "enfant-m|Oui, avec Victorino.",
            "copain|La toupie est restée.",
            "narrateur|Ça sent la cire, un peu tiède.",
            "enfant-m|Et le bois, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|La toupie reste près du sol.",
            "narrateur|Un éclat de plinthe tient sur le bois.",
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
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
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
        if role not in ("narrateur", "papa", "maman", "enfant-m", "copain"):
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
    if "c'est trop" in adults or "c est trop" in adults:
        raise SystemExit(f"{SID}: refrain adulte c'est trop")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "recule d'un pas" not in blob and "recule d un pas" not in blob:
        raise SystemExit(f"{SID}: manque recule d'un pas")
    if "chatouille" not in blob:
        raise SystemExit(f"{SID}: manque chatouille")
    if "ventre" not in blob:
        raise SystemExit(f"{SID}: manque ventre")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Raphaël = enfant-m, Victorino = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Victorino absent (copain)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    if "hippolyte" in blob or "mila" in blob or "aniss" in blob:
        raise SystemExit(f"{SID}: prénom dump restant")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m", "copain") for r in roles):
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
        "il peut s'éloigner",
        "elle peut s'éloigner",
        "dire stop, c'est permis",
        "on s'éloigne",
        "on va vers un adulte",
        "c'est le bon geste",
        "tu as dit stop",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "C'est trop pour Raphaël. Que dit-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "stop":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "stop | s'éloigner | papa | adulte | vers papa"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Raphaël dit stop. Puis il va où ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "enfant-m|stop" in opening or "stop." in opening:
        raise SystemExit(f"{SID}: stop trop tôt (avant la question)")
    if "plinthe" not in blob:
        raise SystemExit(f"{SID}: manque plinthe")
    if "toupie" not in blob:
        raise SystemExit(f"{SID}: manque toupie")
    if "salon" not in (src.get("setting") or "").lower() and "plinthe" not in blob:
        raise SystemExit(f"{SID}: manque salon")
    if "cire" not in blob:
        raise SystemExit(f"{SID}: manque cire")
    for ban in (
        "éclat de tapis",
        "éclat de canapé",
        "éclat de coussin",
        "éclat de marelle",
        "éclat de cadre",
        "éclat de livre",
        "éclat de plaid",
        "éclat de rideau",
        "éclat de toboggan",
        "éclat de balançoire",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "canapé",
        "tapis",
        "coussin",
        "marelle",
        "plaid",
        "toboggan",
        "balançoire",
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
        "- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans\n"
        "- **Leçon :** EMO.GES.001 — trop (chatouille) → dire stop, reculer "
        "(vécue : Victorino chatouille trop, ventre trop vite, Raphaël dit "
        "stop, recule, Victorino trop près du ventre, Raphaël refuse de "
        "foncer). JAMAIS dite dans le récit. Pas « il peut s'éloigner ». "
        "Pas « c'est trop » en refrain adulte. Pas « dire stop, c'est permis ».\n"
        "- **Personnages :** Raphaël, Victorino, papa, maman. Dump "
        "Hippolyte/papa → D16 Raphaël = enfant-m (veut jouer maintenant). "
        "Victorino = copain (chatouille trop, souffle, recule). Troupe D16. "
        "Pas de maîtresse.\n"
        "- **Lieu :** salon, plinthe, toupie rouge, sol, fenêtre, bois, "
        "cire, trait d'or. BAN tapis / canapé / coussin. ≠ 001-01 "
        "balançoire. ≠ 001-02 rideau. ≠ 001-03 toboggan. ≠ 001-04 plaid. "
        "≠ 001-05 livre. ≠ 001-06 cadre. ≠ 001-07 marelle.\n"
        "- **Indice unique :** éclat de plinthe (luit à l'ouverture → "
        "tremble aux chatouilles → luit quand Victorino se colle → tient "
        "sur le bois). BAN éclat de tapis / canapé / coussin / marelle / "
        "cadre / livre / plaid / rideau / toboggan / balançoire.\n"
        "- **Question moteur :** « C'est trop pour Raphaël. Que dit-il ? » "
        "expected **stop**. accepted dump `stop | s'éloigner | papa | "
        "adulte | vers papa`. retry dump Hippolyte → Raphaël. Non récitée "
        "dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un trait d'or file le long du bois. Toc toc. Sur le bois, un "
        "éclat de plinthe luit. Cire, toupie rouge, sol du salon. Raphaël "
        "veut jouer **maintenant**. Victorino chatouille trop. Ventre trop "
        "vite. Sourire parti. Papa s'accroupit. Raphaël dit stop, recule "
        "d'un pas. Merci vécu. Deuxième ruse : Victorino chatouille trop "
        "près du ventre. La toupie penche. Il s'arrête, lit l'éclat. Un "
        "éclat de plinthe tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon, plinthe, toupie, sol, fenêtre, cire, trait d'or. "
        "BAN tapis / canapé / coussin.\n"
        "- Désir : faire tourner la toupie, maintenant.\n"
        "- Objet : toupie rouge, puis toupie qui penche.\n"
        "- Indice unique : éclat de plinthe, vu dès l'ouverture, payé sur "
        "le bois. Pas éclat de tapis / canapé / coussin.\n"
        "- Urgence douce : Victorino arrive, avance les doigts trop vite.\n"
        "- Imprévu 1 : chatouilles trop longues, ventre trop vite, sourire "
        "parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« d'accord ».\n"
        "- Imprévu 2 (plus rusé) : toupie tendue, Victorino chatouille, la "
        "toupie penche.\n"
        "- Résolution : il refuse de foncer, observe, écoute le bois, "
        "retrouve l'éclat, dit stop, recule.\n"
        "- Retour : vzz à un pas, toupie près du sol, éclat sur le bois.\n\n"
        "## Vécu\n\n"
        "Raphaël veut jouer **maintenant**. Impatience, puis chatouilles "
        "trop longues, sourire parti. Victorino prend son élan, pose sa "
        "limite (je m'arrête, souffle, recule). Papa se baisse, pose une "
        "question, ne récite pas la règle. Ils agissent : un pas plus "
        "loin, lancée sans se presser, toupie rendue. Merci vécu. Fin : "
        "l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Raphaël dit stop et s'éloigne (noyau dit stop et "
        "s'éloigne, prénom D16). Relance : Que dit-il ? expected stop.\n"
        "- Lieu du dump-meta (salon). Maman et papa. Victorino = copain. "
        "Raphaël = héros. BAN tapis / canapé / coussin (dump canapé "
        "écarté).\n"
        "- Ouverture inventée (trait d'or, bois, cire), pas un gabarit "
        "v2, pas canapé/coussins/orange du source, pas « Hippolyte joue "
        "au salon ».\n"
        "- Indice unique : éclat de plinthe. BAN éclat de tapis / canapé "
        "/ coussin / marelle / cadre / livre / plaid / rideau / toboggan "
        "/ balançoire. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout bas » / « encore » du dump.\n"
        "- Leçon non dite : on la voit quand Victorino chatouille, quand "
        "le ventre va trop vite, quand Raphaël dit stop, quand il recule. "
        "Pas « il peut s'éloigner ». Pas « c'est trop » en refrain "
        "adulte. Pas « dire stop, c'est permis ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « C'est trop pour Raphaël. Que dit-il ? ». "
        "expected stop. dump accepted. retry Hippolyte → Raphaël. 5 "
        "chunks, kinds inchangés.\n"
        "- example4 045 / 077 / 009 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_par_002_07.py`, profiles N1.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers la toupie qui penche.\n"
        f"- {nwords} mots. N1 ≤ 10. `check()` OK. Pas apply.\n\n"
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
