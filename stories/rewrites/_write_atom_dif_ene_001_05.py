#!/usr/bin/env python3
"""ATOM-DIF.ENE.001-05 — Le seau de la sauge (F-NAR-019, N1, DIF.ENE.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.ENE.001-05"
TITLE = "Le seau de la sauge"
N1 = LIMITS["N1"]
CHARS = "Mila, Aniss, papa, maman"
SETTING = (
    "jardin : sauge, goutte froide, terre, caisse, "
    "seau rouge, bac d'eau, linge"
)
INDICE = "éclat de sauge"
FIL = (
    "Une goutte froide tient sur la sauge. Sur la feuille, un "
    "éclat de sauge brille. Mila veut le seau rouge, maintenant. "
    "Aniss saute trop. L'eau part partout. Sourire parti. Elle "
    "refuse de foncer. Merci vécu. Ils se passent le seau. Il "
    "veut verser tout. Elle s'arrête. Un éclat de sauge tient "
    "sur la feuille."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(flaque|piquet|bol|chiffon|grille|cour|botte|bottes|"
    r"limace|perron|tiroir|fraisier|cuivre|buis|coussin|figue|"
    r"robinet|planche|émail|email|samare|bassine|entrée|entree|"
    r"merle|miel|tania|ulysse|maîtresse|maitresse)\b",
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
    "on peut demander",
    "vous jouez",
    "on joue",
    "chacun son tour",
    "beaucoup d'énergie",
    "beaucoup d'energie",
    "c'est son énergie",
    "c'est son energie",
    "tania",
    "ulysse",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de pince",
    "éclat de marche",
    "éclat de corde",
    "éclat de caisse",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de tasse",
    "éclat d'orange",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat de farine",
    "éclat d'ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de laine",
    "éclat de lampe",
    "éclat de citron",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de crayon",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de cartable",
    "éclat de pinceau",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de pavé",
    "éclat de pave",
    "éclat de bâche",
    "éclat de bache",
    "éclat de poire",
    "éclat de volet",
    "éclat de croissant",
    "éclat de réverbère",
    "éclat de reverbere",
    "éclat de cloche",
    "éclat de corbeille",
    "éclat de sac",
    "éclat de panier",
    "éclat de dorure",
    "éclat de carte",
    "éclat de boule",
    "éclat de galet",
    "éclat de cube",
    "éclat de bois",
    "éclat de couloir",
    "éclat de poussière",
    "éclat de poussiere",
    "éclat de cour",
    "éclat de plaque",
    "éclat de pierre",
    "éclat de grille",
    "éclat de couvercle",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de dalle",
    "éclat d'enveloppe",
    "éclat d'émail",
    "éclat d'email",
    "éclat de samare",
    "éclat de bassine",
    "éclat de cerceau",
    "éclat de robinet",
    "éclat de planche",
    "éclat de figue",
    "éclat de coussin",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de tiroir",
    "éclat de fraisier",
    "éclat de chaise",
    "éclat de perron",
    "éclat de limace",
    "éclat de botte",
    "éclat de résine",
    "éclat de resine",
    "éclat de cageot",
    "éclat de platane",
    "éclat de crochet",
    "éclat de rotin",
    "éclat de portail",
    "éclat de flaque",
    "éclat de piquet",
    "éclat de bol",
    "éclat de chiffon",
    "éclat de seau",
    "éclat de bac",
    "éclat de linge",
    "éclat de terre",
    "éclat de goutte",
    "éclat de caisse",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

# N1 : mêmes champs que COR.003-04 / 003-03, tempos plus lents.
PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat de sauge",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_seau_maintenant; "
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
            "sous_texte=aniss_saute_trop_que_peut_on_faire; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=122, speed=0.88, piper=1.24, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=620,
        sentence=310, energy="bright", contour="falling", noise=0.33,
        emphasis="seau",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_refuse_ils_se_passent_le_seau; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de sauge",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_veut_verser_tout_elle_s_arrete; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de sauge",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_feuille; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer",
    "accepted_examples": "jouer | attendre | un adulte | demander",
    "retry_prompt": (
        "On peut jouer, attendre, ou demander à un adulte. Que fait Mila ?"
    ),
    "engine_ok_text": "Oui, jouer.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc",
        [
            "narrateur|Une goutte froide tient sur la sauge.",
            "narrateur|Elle tremble, ronde et claire.",
            "enfant-f|Elle est froide, papa.",
            "papa|Tu la vois, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|La feuille de sauge sent le savon.",
            "enfant-f|Ça sent fort, maman.",
            "maman|Tu le sens, le savon ?",
            "enfant-f|Oui, maman.",
            "narrateur|La terre est molle, un peu sombre.",
            "papa|Tes chaussures sont mouillées, Mila ?",
            "enfant-f|Un peu, papa.",
            "narrateur|Papa a de la terre sur une chaussure.",
            "papa|Tu as vu la terre, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Une caisse sent le bois mouillé.",
            "narrateur|Un seau rouge attend près du bac.",
            "enfant-f|Le seau est rouge.",
            "maman|Il est près du bac ?",
            "enfant-f|Oui, maman.",
            "narrateur|Maman tord un linge.",
            "narrateur|Le linge goutte sur la terre.",
            "papa|Le bac est plein, Mila ?",
            "enfant-f|L'eau tremble.",
            "narrateur|En ce moment, Mila touche la feuille.",
            "narrateur|Sur la feuille, un éclat de sauge brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "enfant-f|Je veux le seau, maintenant !",
            "maman|Pour la sauge ?",
            "enfant-f|Oui, tout de suite.",
            "papa|Avec le seau rouge ?",
            "enfant-f|Oui, papa.",
            "narrateur|Mila marche vers le bac.",
            "narrateur|L'eau du bac est claire.",
            "narrateur|Aniss arrive dans le jardin.",
            "narrateur|Il saute trop, trop vite.",
            "copain|Le seau !",
            "enfant-f|Aniss !",
            "copain|J'arrive !",
            "narrateur|Mila prend le seau trop vite.",
            "narrateur|Aniss saute contre le seau.",
            "narrateur|L'eau part partout.",
            "narrateur|Elle mouille les chaussures.",
            "enfant-f|Oh.",
            "copain|L'eau !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et la peur se heurtent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Aniss, Mila ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains sont froides, Mila ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de sauge tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Aniss a de l'énergie.",
            "narrateur|Que peut-on faire ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "enfants_parc",
        [
            "narrateur|Mila veut le seau, tout de suite.",
            "enfant-f|Je verse, maintenant !",
            "narrateur|Elle avance trop vite vers Aniss.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copain|Attends.",
            "narrateur|Aniss recule d'un pas.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le seau, un instant.",
            "narrateur|Elle écoute le linge qui goutte.",
            "papa|Tu veux le seau avec Aniss ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Tu tiens l'anse ?",
            "narrateur|Aniss ne dit rien, d'abord.",
            "narrateur|Il pose les mains sur le seau.",
            "copain|Je le tiens.",
            "enfant-f|D'accord.",
            "papa|Merci, Mila.",
            "narrateur|Papa a vu les deux, près du bac.",
            "maman|La sauge est rêche, sous les doigts.",
            "enfant-f|Elle sent le savon.",
            "narrateur|Ils se passent le seau.",
            "narrateur|Aniss tient l'anse, plus près.",
            "narrateur|Mila verse un peu, cette fois.",
            "enfant-f|Ploc.",
            "copain|Ploc.",
            "papa|Tu vois, la sauge ?",
            "enfant-f|Oui, papa.",
            "maman|Elle boit, Aniss ?",
            "copain|Un peu.",
            "narrateur|Mila verse, sans se presser.",
            "narrateur|Aniss suit le seau des yeux.",
            "narrateur|La terre devient plus sombre.",
            "copain|Un.",
            "enfant-f|Deux.",
            "narrateur|Le ventre de Mila se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près de la sauge ?",
            "enfant-f|Oui.",
            "maman|Tes mains sont mouillées, Mila ?",
            "enfant-f|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "enfants_parc",
        [
            "narrateur|Aniss lève le seau trop haut.",
            "narrateur|L'eau penche vers le bord.",
            "copain|Tout d'un coup !",
            "narrateur|Il veut verser tout, tout de suite.",
            "enfant-f|Ça va trop !",
            "narrateur|Une vague part vers la terre.",
            "narrateur|La sauge se couche un peu.",
            "enfant-f|Elle se couche !",
            "narrateur|Mila avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Mila refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le seau, un instant.",
            "narrateur|Elle écoute le linge qui goutte.",
            "narrateur|Sur la feuille, un éclat de sauge luit.",
            "enfant-f|Là, sur la sauge.",
            "enfant-f|Tu verses un peu, Aniss ?",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Il souffle, puis baisse le seau.",
            "copain|Oui.",
            "papa|On verse juste un peu ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le seau sent la terre mouillée.",
            "narrateur|L'eau tombe goutte à goutte.",
            "narrateur|Mila pose le seau près d'Aniss.",
            "narrateur|Aniss le rend, sans sauter.",
            "enfant-f|Ploc.",
            "copain|Ploc.",
            "papa|La sauge a bu, Mila ?",
            "enfant-f|Oui, papa.",
            "maman|Le linge est lourd, Aniss ?",
            "copain|Un peu.",
            "narrateur|Ils se passent le seau, tout près.",
            "narrateur|La terre chatouille les genoux.",
            "enfant-f|C'est plus facile.",
            "papa|Le seau est moins lourd ?",
            "enfant-f|Oui, papa.",
            "maman|Un rayon passe sur la sauge.",
            "enfant-f|Il allume la feuille.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la sauge.",
            "narrateur|Maman essuie un peu d'eau.",
            "enfant-f|La sauge a bu, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-f|Oui, près du bac.",
            "maman|On est bien, ici.",
            "narrateur|Mila tapote le seau du doigt.",
            "enfant-f|Il a une trace d'eau.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|Le seau est resté, Mila.",
            "enfant-f|Oui, avec Aniss.",
            "copain|Le seau est resté.",
            "narrateur|Ça sent la sauge, un peu froide.",
            "enfant-f|Et le linge, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|Le seau sèche à l'envers.",
            "narrateur|Un éclat de sauge tient sur la feuille.",
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
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Mila = enfant-f, Aniss = copain)")
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
        "on joue",
        "vous jouez",
        "on peut jouer",
        "on peut attendre",
        "on peut demander",
        "ce n'est pas une faute",
        "chacun son tour",
        "beaucoup d'énergie",
        "beaucoup d'energie",
        "c'est son énergie",
        "c'est son energie",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    if "énergie" in body or "energie" in body:
        raise SystemExit(f"{SID}: énergie hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Aniss a de l'énergie. Que peut-on faire ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != "jouer | attendre | un adulte | demander":
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "On peut jouer, attendre, ou demander à un adulte. Que fait Mila ?":
        raise SystemExit(f"{SID}: retry dump altéré: {retry}")
    copain_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    ).lower()
    if "attends" not in copain_txt:
        raise SystemExit(f"{SID}: Aniss sans attends")
    if "sauge" not in blob:
        raise SystemExit(f"{SID}: manque sauge")
    if "seau" not in blob:
        raise SystemExit(f"{SID}: manque seau")
    if "bac" not in blob:
        raise SystemExit(f"{SID}: manque bac")
    if "linge" not in blob:
        raise SystemExit(f"{SID}: manque linge")
    if "caisse" not in blob:
        raise SystemExit(f"{SID}: manque caisse")
    if "goutte" not in blob:
        raise SystemExit(f"{SID}: manque goutte")
    if "terre" not in blob:
        raise SystemExit(f"{SID}: manque terre")
    if "froide" not in blob:
        raise SystemExit(f"{SID}: manque goutte froide")
    for ban in (
        "éclat de caisse",
        "éclat de flaque",
        "éclat de piquet",
        "éclat de bol",
        "éclat de chiffon",
        "éclat de seau",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "tania",
        "ulysse",
        "mila est au jardin",
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
        raise SystemExit(f"{SID}: slow hors question/fin: {slow_ids}")

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
        "(vécue : il saute trop, eau partout, seau passé, il veut verser "
        "tout, elle refuse de foncer). JAMAIS dite dans le récit. Pas "
        "« ce n'est pas une faute ». Pas « on peut jouer / attendre / "
        "demander ».\n"
        "- **Personnages :** Mila, Aniss, papa, maman. Mila = enfant-f "
        "(veut le seau maintenant). Aniss = copain (saute, attends, "
        "souffle, veut verser tout). Troupe D16. Pas de maîtresse. "
        "Plus Tania / Ulysse.\n"
        "- **Lieu :** jardin, sauge, goutte froide, terre, caisse, seau "
        "rouge, bac d'eau, linge. ≠ 001-01 flaque, ≠ 001-02 piquet, "
        "≠ 001-03 bol, ≠ 001-04 chiffon.\n"
        "- **Indice unique :** éclat de sauge (brille à l'ouverture → "
        "tremble à l'eau partout → luit quand il veut verser tout → "
        "tient sur la feuille). BAN éclat de caisse / flaque / piquet / "
        "bol / chiffon.\n"
        "- **Question moteur :** « Aniss a de l'énergie. Que peut-on "
        "faire ? » expected **jouer**. accepted `jouer | attendre | un "
        "adulte | demander`. retry dump (label, pas leçon récitée). "
        "Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte froide tient sur la sauge. Sur la feuille, un "
        "éclat de sauge brille. Mila veut le seau **maintenant**. Aniss "
        "saute trop. L'eau part partout. Sourire parti. Papa s'accroupit. "
        "Elle refuse de foncer. Ils se passent le seau. Merci vécu. "
        "Deuxième ruse : il veut verser tout, la sauge se couche. Elle "
        "s'arrête, lit l'éclat. Un éclat de sauge tient sur la feuille.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin, sauge, goutte froide, terre, caisse, seau "
        "rouge, bac, linge. ≠ 001-01 flaque, ≠ 001-02 piquet, ≠ 001-03 "
        "bol, ≠ 001-04 chiffon.\n"
        "- Désir : le seau, maintenant, pour la sauge.\n"
        "- Objet : seau rouge près du bac, puis l'eau trop vite.\n"
        "- Indice unique : éclat de sauge, vu dès l'ouverture, payé "
        "sur la feuille. Pas éclat de caisse / flaque / piquet / bol / "
        "chiffon.\n"
        "- Urgence douce : Aniss arrive, saute trop, le seau attend.\n"
        "- Imprévu 1 : elle prend trop vite, il saute contre, eau "
        "partout, chaussures mouillées.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« d'accord ».\n"
        "- Imprévu 2 (plus rusé) : il lève trop haut, veut verser tout, "
        "la sauge se couche.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le linge, "
        "retrouve l'éclat, Aniss souffle et baisse le seau.\n"
        "- Retour : goutte à goutte, seau à l'envers, éclat sur la "
        "feuille. La fin a failli (la sauge s'est couchée).\n\n"
        "## Vécu\n\n"
        "Mila veut le seau **maintenant**. Impatience, puis eau partout, "
        "sourire parti. Aniss prend son élan, pose sa limite (attends, "
        "souffle). Papa se baisse, pose une question, ne récite pas la "
        "règle. Ils agissent : anse tenue, seau passé, verser un peu. "
        "Merci vécu. Fin : l'éclat du début tient sur la feuille.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le seau de la sauge (noyau dump). Relance : Que "
        "peut-on faire ? expected jouer.\n"
        "- Lieu du dump (jardin, terre mouillée). Maman et papa. "
        "Aniss = copain. Mila = enfant-f.\n"
        "- Ouverture inventée (goutte froide sur la sauge), pas "
        "« Mila est au jardin », pas le ver de terre du dump.\n"
        "- Indice unique : éclat de sauge (goutte sur la feuille). BAN "
        "éclat de caisse / flaque / piquet / bol / chiffon. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « encore » / « tout doucement » du dump.\n"
        "- Leçon non dite : on la voit quand Aniss saute, quand l'eau "
        "part, quand elle s'arrête, quand le seau passe. Pas « ce n'est "
        "pas une faute ». Pas « on peut jouer / attendre / demander » "
        "hors retry moteur.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Aniss a de l'énergie. Que "
        "peut-on faire ? ». expected jouer. retry dump. 5 chunks, kinds "
        "inchangés.\n"
        "- example4 019 / 051 / 083 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_cor_003_04.py` / `_write_atom_dif_ene_001_02.py`, "
        "profiles N1 plus lents.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers le seau trop haut.\n"
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
