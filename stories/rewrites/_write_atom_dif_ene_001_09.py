#!/usr/bin/env python3
"""ATOM-DIF.ENE.001-09 — Le ballon jaune de la cour (F-NAR-019, N1, DIF.ENE.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.ENE.001-09"
TITLE = "Le ballon jaune de la cour"
N1 = LIMITS["N1"]
CHARS = "Raphaël, Aniss, papa, maman"
SETTING = (
    "cour, portail de bois, gond, lattes, poussière chaude, "
    "mouche, caisse, ballon jaune"
)
INDICE = "éclat de gond"
FIL = (
    "Le bois du portail sent le soleil. Sur le gond, un "
    "éclat de gond luit. Raphaël veut le ballon jaune, "
    "maintenant. Aniss court trop. Le ballon tape le bois. "
    "Sourire parti. Papa s'accroupit. Il refuse de foncer. "
    "Merci vécu. Le ballon roule sous le portail. Il s'arrête. "
    "Un éclat de gond tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(flaque|grille|botte|bottes|limace|perron|tiroir|"
    r"fraisier|cuivre|buis|coussin|figue|robinet|planche|"
    r"émail|email|samare|bassine|entrée|entree|merle|miel|"
    r"piquet|cerceau|drap|savon|bol|feuille|pierre|commode|"
    r"lacet|tapis|sauge|chiffon|parquet)\b",
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
    "ce n'est pas une faute",
    "ce n est pas une faute",
    "on peut jouer",
    "on peut attendre",
    "vous jouez",
    "on joue",
    "chacun son tour",
    "beaucoup d'énergie",
    "beaucoup d'energie",
    "c'est son énergie",
    "c'est son energie",
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
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

# N1 : mêmes champs que 001-02 (voix COR.003-02, tempos plus lents).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat de gond",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_ballon_maintenant; "
            "tempo=posé puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=104, speed=0.80, piper=1.36, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=780,
        sentence=360, energy="focused", contour="rising", noise=0.30,
        emphasis="énergie",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=aniss_court_trop_que_fait_raphael; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=122, speed=0.88, piper=1.24, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=620,
        sentence=310, energy="bright", contour="falling", noise=0.33,
        emphasis="ballon",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_refuse_de_foncer_ils_tiennent; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de gond",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=le_ballon_sous_le_portail_il_s_arrete; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de gond",
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
    "expected_answer": "jouer",
    "accepted_examples": "jouer | attendre | maman | un adulte | papa | demander",
    "retry_prompt": "On peut jouer. On peut attendre. Que fait Raphaël ?",
    "engine_ok_text": "Oui, jouer.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc",
        [
            "narrateur|Le bois du portail sent le soleil.",
            "enfant-m|Ça sent le bois, papa.",
            "papa|Tu le sens, le bois chaud ?",
            "enfant-m|Oui, papa.",
            "narrateur|Une latte claque un peu.",
            "maman|Le portail est presque fermé.",
            "enfant-m|Il claque, maman.",
            "narrateur|Papa tapote le gond.",
            "narrateur|Toc, toc, sur le fer.",
            "papa|Tu entends le gond, Raphaël ?",
            "enfant-m|Oui, il grince.",
            "narrateur|Maman pose la main sur le bois.",
            "narrateur|Le bois est chaud, un peu rêche.",
            "narrateur|Sur le gond, un éclat de gond luit.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, sur le gond ?",
            "enfant-m|Oui, un petit point.",
            "papa|Le soleil le touche.",
            "narrateur|Un rayon glisse entre les lattes.",
            "narrateur|La poussière dore, près du mur.",
            "narrateur|Elle chatouille le pantalon.",
            "enfant-m|Elle est chaude.",
            "maman|Tu t'assois, Raphaël ?",
            "enfant-m|Un peu.",
            "narrateur|Une mouche visite une chaussure.",
            "narrateur|Elle fait un petit bzz.",
            "enfant-m|Elle part.",
            "papa|La mouche a fini.",
            "narrateur|Le ballon jaune dort près du mur.",
            "narrateur|En ce moment, Raphaël le prend.",
            "enfant-m|Je veux le ballon, maintenant !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le caoutchouc est tiède, un peu poudreux.",
            "maman|Tu le fais rouler ?",
            "enfant-m|Oui, maman.",
            "narrateur|Aniss arrive dans la cour.",
            "narrateur|Il court trop.",
            "narrateur|Il saute près du portail.",
            "copain|Le ballon !",
            "enfant-m|Tu viens, Aniss ?",
            "copain|Oui.",
            "narrateur|Raphaël pousse le ballon trop vite.",
            "narrateur|Aniss court dessus.",
            "narrateur|Le ballon tape le bois.",
            "narrateur|Il ne roule plus.",
            "enfant-m|Oh.",
            "copain|Il est tombé.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et la peur se heurtent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Aniss, Raphaël ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains sont chaudes, Raphaël ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de gond tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss a de l'énergie.",
            "narrateur|Que fait Raphaël ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "enfants_parc",
        [
            "narrateur|Raphaël veut le ballon, tout de suite.",
            "enfant-m|Je pousse, maintenant !",
            "narrateur|Il avance trop vite vers Aniss.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copain|Attends.",
            "narrateur|Aniss recule d'un pas.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Raphaël refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le ballon, un instant.",
            "narrateur|Il écoute le gond du portail.",
            "papa|Tu veux le ballon avec Aniss ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Tu tiens le bord ?",
            "narrateur|Aniss ne dit rien, d'abord.",
            "narrateur|Il pose les mains sur le caoutchouc.",
            "copain|Je le tiens.",
            "enfant-m|D'accord.",
            "papa|Merci, Raphaël.",
            "narrateur|Papa a vu les deux, près du gond.",
            "maman|La poussière colle un peu, sous les doigts.",
            "enfant-m|Elle est tiède.",
            "narrateur|Ils essuient le ballon sur le sol.",
            "narrateur|Aniss tient le bord, plus près.",
            "narrateur|Le ballon redevient plus léger, cette fois.",
            "enfant-m|Il roule !",
            "copain|Oui.",
            "papa|Tu le vois, le ballon ?",
            "enfant-m|Oui, papa.",
            "maman|Au milieu, Aniss ?",
            "copain|J'y vais.",
            "narrateur|Raphaël pousse, sans se presser.",
            "narrateur|Aniss suit le ballon des yeux.",
            "narrateur|Le ballon danse une fois.",
            "copain|Un.",
            "enfant-m|Deux.",
            "narrateur|Le ventre de Raphaël se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près du portail ?",
            "enfant-m|Oui.",
            "maman|Tes mains sont au chaud ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "enfants_parc",
        [
            "narrateur|Maman sort une caisse du coin.",
            "narrateur|Elle est un peu poudreuse.",
            "enfant-m|Le ballon, maintenant !",
            "narrateur|Aniss court trop, tout de suite.",
            "narrateur|Il saute vers le ballon.",
            "copain|À moi !",
            "narrateur|Le ballon roule sous le portail.",
            "enfant-m|Il est dessous !",
            "narrateur|Raphaël avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Raphaël refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le ballon, un instant.",
            "narrateur|Il écoute le gond du portail.",
            "narrateur|Sur le gond, un éclat de gond luit.",
            "enfant-m|Là, sur le gond.",
            "enfant-m|Tu tends les mains, Aniss ?",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Il souffle, puis tend les mains.",
            "copain|Oui.",
            "papa|On soulève la latte ?",
            "enfant-m|Oui, papa.",
            "narrateur|La latte sent le bois chaud.",
            "narrateur|Le ballon est là, un peu tiède.",
            "narrateur|Raphaël le pose près d'Aniss.",
            "narrateur|Aniss le rend, sans courir.",
            "enfant-m|Poumf.",
            "copain|Poumf.",
            "papa|Le ballon est bien gonflé ?",
            "enfant-m|Oui, papa.",
            "maman|La poussière est chaude, Aniss ?",
            "copain|Un peu.",
            "narrateur|Ils se passent le ballon, tout près.",
            "narrateur|Le sol chatouille les genoux.",
            "enfant-m|C'est plus facile.",
            "papa|Le portail est calme ?",
            "enfant-m|Oui, papa.",
            "maman|Un rayon passe entre les lattes.",
            "enfant-m|Il allume le gond.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du gond.",
            "narrateur|Maman essuie un peu de poussière.",
            "enfant-m|Le ballon a roulé, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, près du portail.",
            "maman|On est bien, ici.",
            "narrateur|Raphaël tapote le ballon du doigt.",
            "enfant-m|Il a une trace de poussière.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|Le ballon est resté, Raphaël.",
            "enfant-m|Oui, avec Aniss.",
            "copain|Le ballon est resté.",
            "narrateur|Ça sent le bois, un peu tiède.",
            "enfant-m|Et le gond, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|Le ballon reste près du mur.",
            "narrateur|Un éclat de gond tient sur le bois.",
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
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Raphaël = enfant-m, Aniss = copain)")
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
        "on joue",
        "vous jouez",
        "on peut jouer",
        "on peut attendre",
        "ce n'est pas une faute",
        "chacun son tour",
        "beaucoup d'énergie",
        "beaucoup d'energie",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    if "énergie" in body or "energie" in body:
        raise SystemExit(f"{SID}: énergie hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Aniss a de l'énergie. Que fait Raphaël ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "jouer | attendre | maman | un adulte | papa | demander"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "On peut jouer. On peut attendre. Que fait Raphaël ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    copain_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    ).lower()
    if "attends" not in copain_txt:
        raise SystemExit(f"{SID}: Aniss sans attends")
    if "ballon" not in blob:
        raise SystemExit(f"{SID}: manque ballon")
    if "gond" not in blob:
        raise SystemExit(f"{SID}: manque gond")
    if "mouche" not in blob:
        raise SystemExit(f"{SID}: manque mouche")
    if "portail" not in blob:
        raise SystemExit(f"{SID}: manque portail")
    if "cour" not in blob:
        raise SystemExit(f"{SID}: manque cour")
    if "caisse" not in blob:
        raise SystemExit(f"{SID}: manque caisse")
    for ban in (
        "éclat de portail",
        "éclat de feuille",
        "éclat de cour",
        "éclat de pierre",
        "éclat de commode",
        "éclat de lacet",
        "éclat de tapis",
        "éclat de sauge",
        "éclat de piquet",
        "éclat de flaque",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
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
        "- **Leçon :** DIF.ENE.001 — Aniss a de l'énergie "
        "(vécue : il court trop, ballon contre le bois, ballon sous le "
        "portail, Raphaël refuse de foncer, ils se passent le ballon). "
        "JAMAIS dite dans le récit. Pas « ce n'est pas une faute ». Pas "
        "« on peut jouer / on peut attendre ».\n"
        "- **Personnages :** Raphaël, Aniss, papa, maman. Dump Amélie/Loïc "
        "→ D16 Raphaël = enfant-m (veut le ballon maintenant). Aniss = "
        "copain (court, saute, attends, souffle). Troupe D16. Pas de "
        "maîtresse.\n"
        "- **Lieu :** cour, portail de bois, gond, lattes, poussière "
        "chaude, mouche, caisse, ballon jaune. ≠ 001-01 cour/flaques. "
        "≠ 001-02 jardin/linge. ≠ COR.003-07 portail de fer.\n"
        "- **Indice unique :** éclat de gond (luit à l'ouverture → "
        "tremble au ballon → luit sous le portail → tient sur le bois). "
        "BAN éclat de portail / feuille / cour / pierre / commode / "
        "lacet / tapis / sauge.\n"
        "- **Question moteur :** « Aniss a de l'énergie. Que fait "
        "Raphaël ? » expected **jouer**. accepted `jouer | attendre | "
        "maman | un adulte | papa | demander`. retry dump adapté. Non "
        "récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le bois du portail sent le soleil. Toc toc. Sur le gond, un "
        "éclat de gond luit. Mouche, poussière chaude. Raphaël veut "
        "le ballon **maintenant**. Aniss court trop. Le ballon tape le "
        "bois. Sourire parti. Papa s'accroupit. Il refuse de foncer. "
        "Ils tiennent le bord. Merci vécu. Deuxième ruse : le ballon "
        "sous le portail. Il s'arrête, lit l'éclat. Un éclat de gond "
        "tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cour, portail de bois, gond, lattes, poussière, "
        "mouche. ≠ 001-01 flaques. ≠ 001-02 linge. ≠ 003-07 fer.\n"
        "- Désir : le ballon jaune, maintenant.\n"
        "- Objet : ballon jaune, puis ballon sous le portail.\n"
        "- Indice unique : éclat de gond, vu dès l'ouverture, payé "
        "sur le bois. Pas éclat de portail / feuille / cour / pierre.\n"
        "- Urgence douce : Aniss arrive, court trop, le ballon attend.\n"
        "- Imprévu 1 : poussée trop vite, Aniss dessus, ballon contre "
        "le bois.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« d'accord ».\n"
        "- Imprévu 2 (plus rusé) : caisse, Aniss court, le portail "
        "avale le ballon.\n"
        "- Résolution : il refuse de foncer, observe, écoute le gond, "
        "retrouve l'éclat, Aniss tend les mains.\n"
        "- Retour : poumf tout près, ballon près du mur, éclat sur "
        "le bois.\n\n"
        "## Vécu\n\n"
        "Raphaël veut le ballon **maintenant**. Impatience, puis "
        "ballon contre le bois, sourire parti. Aniss prend son élan, "
        "pose sa limite (attends, souffle). Papa se baisse, pose une "
        "question, ne récite pas la règle. Ils agissent : bord tenu, "
        "poussée sans se presser, ballon rendu. Merci vécu. Fin : "
        "l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le ballon jaune de la cour (noyau dump). Relance : "
        "Que fait Raphaël ? expected jouer.\n"
        "- Lieu du dump-meta (cour, portail). Maman et papa. Aniss = "
        "copain. Raphaël = héros.\n"
        "- Ouverture inventée (bois du portail, soleil, gond), pas un "
        "gabarit v2, pas cuisine/raisins du source, pas « Amélie est "
        "dans la cour ».\n"
        "- Indice unique : éclat de gond (portail de bois). BAN éclat "
        "de portail (003-07) / feuille / cour / pierre / commode / "
        "lacet / tapis / sauge. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « encore » du dump.\n"
        "- Leçon non dite : on la voit quand Aniss court, quand le "
        "ballon tape le bois, quand il s'arrête, quand le ballon "
        "revient. Pas « ce n'est pas une faute ». Pas « on peut jouer "
        "/ on peut attendre » hors retry moteur.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Aniss a de l'énergie. Que fait "
        "Raphaël ? ». expected jouer. 5 chunks, kinds inchangés.\n"
        "- example4 023 / 055 / 087 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_ene_001_02.py`, profiles N1.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers le ballon sous le portail.\n"
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
