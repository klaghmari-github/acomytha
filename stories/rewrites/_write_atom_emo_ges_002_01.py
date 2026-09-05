#!/usr/bin/env python3
"""ATOM-EMO.GES.002-01 — La tour de cubes (F-NAR-019, N1, EMO.GES.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.002-01"
TITLE = "La tour de cubes"
N1 = LIMITS["N1"]
CHARS = "Mila, papa, maman"
SETTING = (
    "maison, salon, cubes, carton, bois, fenêtre, "
    "soleil, peinture, sol"
)
INDICE = "éclat de tour"
FIL = (
    "Le bois des cubes sent le soleil. Sur le bois, "
    "un éclat de tour luit. Mila veut empiler, maintenant. "
    "Les cubes tombent. Poitrine trop vite. Sourire parti. "
    "Papa s'accroupit. Elle souffle, pause. Merci vécu. "
    "Deuxième ruse : trop de cubes, la tour penche. "
    "Elle refuse de foncer. Un éclat de tour tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tapis|rideau|plaid|balançoire|balancoire|plinthe|marelle|"
    r"banc|cour|grille|bac|flaque|botte|bottes|limace|perron|"
    r"tiroir|fraisier|cuivre|buis|coussin|figue|robinet|planche|"
    r"émail|email|samare|bassine|entrée|entree|merle|miel|"
    r"piquet|cerceau|drap|savon|bol|feuille|pierre|commode|"
    r"lacet|sauge|chiffon|parquet|gond|portail|canapé|"
    r"canape|oiseau|toboggan|comptoir)\b",
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
    "on peut souffler",
    "souffle comme le vent",
    "souffle comme",
    "tu as soufflé",
    "tu as souffle",
    "tu as fait une pause",
    "fais une pause",
    "souffler, puis une pause",
    "souffler puis une pause",
    "on peut reprendre",
    "on reprend",
    "tu as pris ton temps",
    "tu as repris",
    "c'est le bon geste",
    "c est le bon geste",
    "tu te souviens",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de cube",
    "éclat de tapis",
    "éclat de rideau",
    "éclat de plaid",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de plinthe",
    "éclat de marelle",
    "éclat de toboggan",
    "éclat de comptoir",
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
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

# N1 : mêmes champs que DIF.ENE.001-09 / GES.001-01 (voix N1, tempos plus lents).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat de tour",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_empiler_maintenant; "
            "tempo=posé puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=104, speed=0.80, piper=1.36, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=780,
        sentence=360, energy="focused", contour="rising", noise=0.30,
        emphasis="Mila",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_corps_de_mila_va_vite_que_fait_elle; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=122, speed=0.88, piper=1.24, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=620,
        sentence=310, energy="bright", contour="falling", noise=0.33,
        emphasis="souffle",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_souffle_elle_fait_une_pause; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de tour",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=trop_de_cubes_la_tour_penche_elle_s_arrete; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de tour",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "souffler",
    "accepted_examples": "souffler | pause | une pause | s'asseoir | respirer",
    "retry_prompt": "Papa dit de souffler. Que fait Mila ensuite ?",
    "engine_ok_text": "Oui, souffler.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "cubes_tombent",
        [
            "narrateur|Le bois des cubes sent le soleil.",
            "enfant-f|Ça sent le bois, papa.",
            "papa|Tu le sens, le bois chaud ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un cube tape un autre cube.",
            "narrateur|Toc, près de la fenêtre.",
            "maman|Tu entends le toc, Mila ?",
            "enfant-f|Oui, maman.",
            "narrateur|La peinture des cubes est un peu collante.",
            "enfant-f|Elle colle aux doigts.",
            "maman|Elle est tiède, Mila ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Papa ouvre le carton des cubes.",
            "narrateur|Le carton froisse, près des genoux.",
            "papa|Tu vois les cubes, Mila ?",
            "enfant-f|Oui, ils brillent.",
            "narrateur|Un cube jaune roule vers le sol.",
            "enfant-f|Il est jaune !",
            "maman|Tu le rattrapes ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sur le bois, un éclat de tour luit.",
            "enfant-f|Il brille, maman.",
            "maman|Tu le vois, sur le bois ?",
            "enfant-f|Oui, un petit point.",
            "papa|Le soleil le touche.",
            "narrateur|Un rayon glisse sur le bord.",
            "narrateur|La fenêtre chauffe le salon.",
            "enfant-f|Elle est chaude.",
            "maman|Tu poses un cube, Mila ?",
            "enfant-f|Oui.",
            "narrateur|Maman s'assoit près du carton.",
            "enfant-f|Ça chauffe les genoux.",
            "papa|Les genoux sont bien ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un cube bleu attend dans la main.",
            "enfant-f|Il est lisse.",
            "maman|Il sent la peinture ?",
            "enfant-f|Un peu, maman.",
            "narrateur|En ce moment, Mila prend un cube.",
            "enfant-f|Je veux empiler, maintenant !",
            "papa|Tout de suite ?",
            "enfant-f|Oui, papa.",
            "narrateur|Les mains serrent le bois peint.",
            "maman|Tu mets le cube dessus ?",
            "enfant-f|Oui, maman.",
            "narrateur|Mila pose un cube trop vite.",
            "narrateur|Puis un autre, trop haut.",
            "enfant-f|Plus haut !",
            "narrateur|La tour penche d'un coup.",
            "narrateur|Les cubes tombent sur le sol.",
            "narrateur|Ça fait un bruit sec.",
            "enfant-f|Oh.",
            "narrateur|Mila reste surprise, les mains ouvertes.",
            "narrateur|Sa poitrine va trop vite.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et la peur se heurtent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois les cubes, Mila ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains sont chaudes, Mila ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de tour tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Le corps de Mila va vite.",
            "narrateur|Que fait-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Mila veut empiler, tout de suite.",
            "enfant-f|Je mets tout, maintenant !",
            "narrateur|Les cubes restent par terre.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Trop vite.",
            "narrateur|Mila avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe les cubes, un instant.",
            "narrateur|Elle écoute le salon.",
            "enfant-f|Pouh.",
            "narrateur|Mila souffle une fois.",
            "narrateur|Elle souffle une deuxième fois.",
            "narrateur|Elle s'assoit près du carton.",
            "narrateur|Ses mains se posent sur ses genoux.",
            "narrateur|La poitrine ralentit un peu.",
            "papa|Tu restes un peu, Mila ?",
            "enfant-f|Oui, papa.",
            "papa|Merci, Mila.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|La peinture colle un peu, sous les doigts.",
            "enfant-f|Elle est tiède.",
            "narrateur|Mila reprend un cube, sans se presser.",
            "narrateur|Elle le pose sur un autre.",
            "papa|Tu le vois, le cube ?",
            "enfant-f|Oui, papa.",
            "maman|Il tient, Mila ?",
            "enfant-f|Oui, maman.",
            "narrateur|La tour a deux cubes.",
            "enfant-f|Elle tient !",
            "papa|La tour est calme ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains sont au chaud ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le ventre de Mila se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près des cubes ?",
            "enfant-f|Oui.",
            "maman|Le rayon touche le bord ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le cube jaune attend à côté.",
            "enfant-f|Je le prends.",
            "papa|Tu le poses, Mila ?",
            "enfant-f|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Maman pousse le carton près du sol.",
            "narrateur|Il est un peu poudreux.",
            "enfant-f|La tour, maintenant !",
            "narrateur|Mila prend trop de cubes, tout de suite.",
            "narrateur|Un cube glisse de sa main.",
            "enfant-f|Il glisse !",
            "narrateur|La tour penche vers le carton.",
            "narrateur|Mila avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Mila refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe la tour, un instant.",
            "narrateur|Elle écoute le salon, près des cubes.",
            "narrateur|Sur le bois, un éclat de tour luit.",
            "enfant-f|Là, sur le bois.",
            "narrateur|Mila souffle une fois.",
            "narrateur|Elle attend, assise un moment.",
            "enfant-f|Pouh.",
            "papa|On tient le cube ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le cube sent le bois chaud.",
            "narrateur|La tour est là, un peu penchée.",
            "narrateur|Mila pose le cube, sans se presser.",
            "narrateur|La tour se redresse.",
            "enfant-f|Poumf.",
            "maman|Le bois est tiède, Mila ?",
            "enfant-f|Un peu.",
            "narrateur|Elle pose un autre cube, au milieu.",
            "papa|La tour est bien calme ?",
            "enfant-f|Oui, papa.",
            "maman|Un rayon passe sur le bord.",
            "enfant-f|Il allume le bois.",
            "papa|Tu vois le point, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Les cubes tiennent, l'un sur l'autre.",
            "enfant-f|C'est plus facile.",
            "papa|La tour est calme ?",
            "enfant-f|Oui, papa.",
            "maman|Tes genoux sont au chaud ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le carton reste ouvert, près d'elle.",
            "enfant-f|Il sent le bois.",
            "papa|On reste ici, Mila ?",
            "enfant-f|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du carton.",
            "narrateur|Maman essuie un peu de peinture.",
            "enfant-f|Les cubes sont tombés, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-f|Oui, près de la tour.",
            "maman|On est bien, ici.",
            "narrateur|Mila tapote le bois du doigt.",
            "enfant-f|Il a une trace de peinture.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|La tour est restée, Mila.",
            "enfant-f|Oui, avec les cubes.",
            "narrateur|Ça sent le bois, un peu tiède.",
            "enfant-f|Et la peinture, maman.",
            "maman|Oui, dans l'air.",
            "papa|Le salon est calme, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|La tour reste près du carton.",
            "narrateur|Un éclat de tour tient sur le bois.",
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
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Mila = enfant-f)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé (dump sans camarade)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
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
    if not any(r == "enfant-f" for r in roles):
        raise SystemExit(f"{SID}: enfant-f absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on peut souffler",
        "souffle comme le vent",
        "tu as soufflé",
        "tu as fait une pause",
        "souffler, puis une pause",
        "on peut reprendre",
        "tu as pris ton temps",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Le corps de Mila va vite. Que fait-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "souffler":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "souffler | pause | une pause | s'asseoir | respirer"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Papa dit de souffler. Que fait Mila ensuite ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "souffle" in opening or "pause" in opening:
        raise SystemExit(f"{SID}: souffle/pause trop tôt (avant la question)")
    if "salon" not in blob:
        raise SystemExit(f"{SID}: manque salon")
    if "cube" not in blob:
        raise SystemExit(f"{SID}: manque cube")
    if "carton" not in blob:
        raise SystemExit(f"{SID}: manque carton")
    if "fenêtre" not in blob and "fenetre" not in blob:
        raise SystemExit(f"{SID}: manque fenêtre")
    for ban in (
        "éclat de cube",
        "éclat de tapis",
        "éclat de rideau",
        "éclat de balançoire",
        "éclat de plinthe",
        "éclat de marelle",
        "éclat de plaid",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        " tapis",
        "rideau",
        "balançoire",
        "plinthe",
        "marelle",
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
        "- **Leçon :** EMO.GES.002 — souffler, faire une pause "
        "(vécue : cubes tombent, poitrine trop vite, sourire parti, "
        "papa accroupi, Mila souffle, s'assoit, pause ; 2e ruse : trop "
        "de cubes, la tour penche, elle refuse de foncer). JAMAIS dite "
        "dans le récit. Pas « on peut souffler ». Pas « souffle comme "
        "le vent ». Pas « tu as fait une pause ».\n"
        "- **Personnages :** Mila, papa, maman. Dump Lila/Raphaël, papa "
        "→ D16 Mila = enfant-f (veut empiler maintenant). Pas de copain "
        "(dump sans camarade). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** maison, salon, cubes, carton, bois, fenêtre, "
        "soleil, peinture, sol. BAN tapis / rideau (pris GES.001). "
        "≠ dump pluie/gouttes/tapis. Distinct GES.001-04 plaid.\n"
        "- **Indice unique :** éclat de tour (luit à l'ouverture → "
        "tremble à la chute → luit quand la tour penche → tient sur "
        "le bois). BAN éclat de cube / tapis / rideau / balançoire / "
        "plinthe / marelle / plaid.\n"
        "- **Question moteur :** « Le corps de Mila va vite. Que "
        "fait-elle ? » expected dump **souffler**. accepted dump "
        "`souffler | pause | une pause | s'asseoir | respirer`. "
        "retry dump Lila → Mila. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le bois des cubes sent le soleil. Toc. Sur le bois, un éclat "
        "de tour luit. Carton, peinture, fenêtre chaude. Mila veut "
        "empiler **maintenant**. Les cubes tombent. Poitrine trop vite. "
        "Sourire parti. Papa s'accroupit. Elle souffle, pause. Merci "
        "vécu. Deuxième ruse : trop de cubes, la tour penche. Elle "
        "s'arrête, lit l'éclat. Un éclat de tour tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon, cubes, carton, bois, fenêtre, peinture. "
        "BAN tapis / rideau.\n"
        "- Désir : empiler la tour, maintenant.\n"
        "- Objet : cubes, puis tour qui penche.\n"
        "- Indice unique : éclat de tour, vu dès l'ouverture, payé "
        "sur le bois. Pas éclat de cube / tapis / rideau.\n"
        "- Urgence douce : elle pose trop vite, trop haut.\n"
        "- Imprévu 1 : cubes tombent, poitrine trop vite, sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "la pause.\n"
        "- Imprévu 2 (plus rusé) : carton, trop de cubes, la tour penche.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le salon, "
        "retrouve l'éclat, souffle, attend.\n"
        "- Retour : poumf, tour près du carton, éclat sur le bois.\n\n"
        "## Vécu\n\n"
        "Mila veut empiler **maintenant**. Impatience, puis cubes par "
        "terre, sourire parti. Elle souffle, s'assoit, les mains sur "
        "les genoux. Papa se baisse, pose une question, ne récite pas "
        "la règle. Ils agissent : un cube sans se presser, tour de "
        "deux. Merci vécu. Fin : l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : La tour de cubes (noyau dump). Relance : "
        "Que fait-elle ? expected souffler.\n"
        "- Lieu du dump-meta (maison/salon). Maman et papa. "
        "Mila = héros enfant-f. BAN tapis dans le récit.\n"
        "- Ouverture inventée (bois, soleil, toc), pas un gabarit "
        "v2, pas pluie/gouttes/tapis du source, pas « Lila joue "
        "dans le salon ».\n"
        "- Indice unique : éclat de tour. BAN éclat de cube / "
        "tapis / rideau / balançoire / plinthe / marelle. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doucement » du dump.\n"
        "- Leçon non dite : on la voit quand les cubes tombent, "
        "quand la poitrine va trop vite, quand Mila souffle, "
        "quand elle s'assoit. Pas « on peut souffler ». Pas "
        "« souffle comme le vent ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Le corps de Mila va vite. Que "
        "fait-elle ? ». expected souffler. 5 chunks, kinds "
        "inchangés. expected/accepted dump conservés. retry Lila "
        "→ Mila.\n"
        "- example4 046 / 078 / 010 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_001_01.py`, profiles N1.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers la tour qui penche.\n"
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
