#!/usr/bin/env python3
"""ATOM-COL.ECO.002-08 — La feuille brune de Victorino (F-NAR-019, N1)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.002-08"
TITLE = "La feuille brune de Victorino"
N1 = LIMITS["N1"]
INDICE = "éclat de mie"
FIL = (
    "Le beurre fond. Le pain grillé saute. Sur le toast, un éclat de mie "
    "brille. Victorino veut montrer la feuille brune, maintenant. Il parle "
    "trop vite : les mots se perdent. Il saisit le toast : l'éclat saute. "
    "À la classe, il lève la feuille : personne ne regarde. Il refuse de "
    "foncer, lève la main, attend, puis dit. Merci vécu. L'éclat de mie "
    "tient sur le toast."
)
CHARS = "Victorino, papa, maman"
SETTING = "cuisine au toast, classe, puis maison"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "dorian",
    "merle",
    "miel",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "ninon",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai levé la main",
    "j'ai leve la main",
    "j'ai attendu",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "on range les feutres",
    "tu ranges",
    "tu as bien écouté",
    "tu as bien ecoute",
    "on aime écouter",
    "on aime ecouter",
    "écoute la maîtresse",
    "ecoute la maitresse",
    "tu as bien fait",
    "bon travail",
    "une chose, puis",
    "une chose puis",
    "il faut attendre",
    "tu attends ton tour",
    "c'est ton tour",
    "on doit demander",
    "gouttière",
    "gouttiere",
    "crayon",
    "buée",
    "buee",
    "croûte",
    "croute",
    "tableau",
    "casier",
    "moufle",
    "craie",
    "cartable",
    "pinceau",
    "casserole",
    "grain de",
    "éclat de croûte",
    "éclat de croute",
    "éclat de carotte",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de terre",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de marche",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de tasse",
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de farine",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de laine",
    "éclat de orange",
    "éclat de lampe",
    "éclat de citron",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de pin",
    "éclat de crayon",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de craie",
    "éclat de tapis",
    "éclat de moufle",
    "éclat de casier",
    "éclat de tableau",
    "éclat de cartable",
    "éclat de pinceau",
    "pli de voile",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "malaise",
    "secret",
    "feuille collée au lait",
    "bouteille de lait",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de mie",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_montrer_la_feuille_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="parler",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_leve_la_main_avant_de_parler; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="main",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_attend_puis_dit_la_feuille_brune; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="feuille",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_couper_papa; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de mie",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_toast; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}


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


def vet(lines: list[str]) -> list[str]:
    out: list[str] = []
    starts: list[str] = []
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
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"extra {bad}: {ph}")
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


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    lines = vet(lines)
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


P0000 = [
    "narrateur|Le beurre fond tout seul.",
    "narrateur|La cuisine sent le toast chaud.",
    "narrateur|Une assiette blanche attend sur la table.",
    "narrateur|Le pain grillé saute dans l'assiette.",
    "enfant-m|Il saute, papa !",
    "papa|Tu l'entends, le petit bruit ?",
    "narrateur|Sur le toast, un éclat de mie brille.",
    "enfant-m|Il brille, maman.",
    "maman|C'est la mie, sous la lumière.",
    "narrateur|Une feuille brune reste dans sa poche.",
    "enfant-m|Elle est sèche.",
    "enfant-m|Elle a un petit trou.",
    "papa|Tu la montres à l'école ?",
    "enfant-m|Oui, papa.",
    "enfant-m|Maintenant !",
    "narrateur|En ce moment, Victorino saisit le toast.",
    "narrateur|L'éclat de mie saute près de l'assiette.",
    "enfant-m|Ma feuille, papa !",
    "narrateur|Papa n'a pas fini sa phrase.",
    "papa|Une petite bouchée, Victorino.",
    "narrateur|Les deux voix se mélangent.",
    "enfant-m|Oh.",
    "narrateur|Le sourire de Victorino disparaît.",
    "narrateur|Dans sa poitrine, ça se bouscule.",
    "narrateur|L'envie et l'inquiétude se heurtent.",
    "enfant-m|Ça ne veut pas !",
    "papa|Tes doigts sont près de l'assiette ?",
    "enfant-m|Oui, papa.",
    "narrateur|Papa se baisse à sa hauteur.",
    "maman|On essuie tes doigts.",
    "maman|Voilà.",
    "enfant-m|C'est croustillant.",
    "narrateur|Un doigt reste un peu brillant.",
    "papa|C'est le beurre, Victorino.",
    "enfant-m|Il est chaud.",
    "narrateur|Le sac attend près du banc.",
    "maman|Ta veste bleue.",
    "maman|Les boutons, un par un.",
    "papa|Les feuilles du jardin sont sèches.",
    "papa|Ta veste est boutonnée ?",
    "enfant-m|Oui, papa.",
    "papa|On y va ?",
    "enfant-m|On y va.",
    "enfant-m|Au revoir, maman.",
    "maman|Au revoir, Victorino.",
    "narrateur|Dehors, les feuilles font crac.",
    "enfant-m|Crac.",
    "enfant-m|Crac.",
    "papa|On marche dessus.",
    "narrateur|On marche sur le tapis de feuilles.",
    "narrateur|L'école a une porte rouge.",
    "narrateur|Une petite cloche sonne une fois.",
    "narrateur|La veste bleue reste au crochet.",
    "narrateur|Le couloir sent le savon.",
    "narrateur|Une petite flaque brille sous la chaussure.",
    "papa|On revient.",
    "enfant-m|Au revoir, papa.",
    "narrateur|La veste est un peu chaude.",
    "narrateur|Le tapis de la classe est gris.",
    "narrateur|Victorino s'assoit, les genoux au tapis.",
    "narrateur|Il sent le toast sur ses doigts.",
    "narrateur|La feuille brune reste dans sa poche.",
    "maitresse|Bonjour.",
    "enfant-m|Bonjour, maîtresse.",
    "narrateur|Victorino a une idée.",
    "narrateur|Sa feuille est brune, avec un trou.",
    "enfant-m|Je veux parler de la feuille !",
    "narrateur|Il ouvre la bouche trop vite.",
    "narrateur|Ses mots se cognent à la classe.",
    "narrateur|Personne ne tourne la tête.",
    "narrateur|Victorino referme la bouche.",
    "narrateur|Il repose les mains sur ses genoux.",
]

Q0001 = [
    "narrateur|Victorino veut parler.",
    "narrateur|Que fait-il d'abord ?",
]

C0001 = [
    "narrateur|Victorino veut montrer la feuille, tout de suite.",
    "enfant-m|Ma feuille est brune !",
    "narrateur|Il lève la feuille trop vite.",
    "narrateur|La feuille penche, puis retombe.",
    "enfant-m|Oh.",
    "narrateur|Personne ne regarde la feuille.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Victorino refuse de foncer.",
    "narrateur|Il referme la bouche.",
    "narrateur|Une main monte, sans crier.",
    "narrateur|Sa main reste en l'air.",
    "narrateur|Une autre voix parle d'un caillou.",
    "narrateur|Victorino reste près de sa place.",
    "narrateur|Il sent la feuille dans sa poche.",
    "narrateur|Sur son doigt, l'éclat de mie brille.",
    "narrateur|Sa main ne descend pas.",
    "maitresse|Victorino.",
    "narrateur|Un silence arrive, tout petit.",
    "enfant-m|Ma feuille est brune.",
    "enfant-m|Elle fait crac.",
    "enfant-m|Elle a un petit trou.",
    "narrateur|Il sort la feuille, à deux mains.",
    "narrateur|Un peu de lumière passe dans le trou.",
    "narrateur|Une tête se tourne vers lui.",
    "narrateur|Les oreilles écoutent jusqu'au bout.",
    "narrateur|Un cube jaune attend près du tapis.",
    "narrateur|Victorino le regarde, sans le prendre.",
    "narrateur|Le cube est lisse, un peu froid.",
    "enfant-m|Une petite fenêtre, oui.",
    "narrateur|Le ventre de Victorino se desserre.",
]

END = [
    "narrateur|Plus tard, la porte rouge s'ouvre.",
    "papa|Tu as passé un bon moment ?",
    "enfant-m|Ma feuille, papa !",
    "narrateur|Papa n'a pas fini sa phrase.",
    "papa|Le sac est près du banc, Victorino.",
    "narrateur|Les deux voix se mélangent.",
    "enfant-m|Oh.",
    "narrateur|Victorino refuse de foncer.",
    "narrateur|Il referme la bouche.",
    "narrateur|Il pose les mains à plat.",
    "papa|Tes pieds sont près de la table ?",
    "narrateur|Papa pose le sac contre le bois.",
    "maman|La feuille est dans ta poche ?",
    "narrateur|Maman n'a pas fini non plus.",
    "narrateur|Victorino reste jusqu'au silence.",
    "enfant-m|Je peux te dire quelque chose ?",
    "maman|Oui, nous t'écoutons.",
    "enfant-m|Ma feuille est brune.",
    "enfant-m|Elle a un petit trou.",
    "papa|Merci, Victorino.",
    "narrateur|Papa a entendu toute la phrase.",
    "maman|Tu veux un peu d'eau ?",
    "enfant-m|Oui, maman.",
    "narrateur|Victorino veut poser la feuille, tout de suite.",
    "narrateur|Il la saisit trop vite.",
    "narrateur|La feuille glisse entre ses doigts.",
    "enfant-m|Oh.",
    "narrateur|Victorino s'arrête.",
    "narrateur|Ses mains se ferment, puis s'ouvrent.",
    "narrateur|Il refuse de foncer.",
    "narrateur|Il pose la feuille plus lentement.",
    "enfant-m|Elle est sèche, maman !",
    "maman|On voit le petit trou.",
    "papa|On rentre.",
    "narrateur|Les feuilles font crac sous les chaussures.",
    "narrateur|La porte de la maison s'ouvre.",
]

FIN = [
    "narrateur|Ils restent près de la table.",
    "narrateur|La feuille brune dort près du sel.",
    "enfant-m|Comme ce matin, papa !",
    "papa|Tu le vois, le petit trou ?",
    "enfant-m|Oui, une petite fenêtre.",
    "maman|On est bien, ici.",
    "narrateur|La cuisine sent un peu le toast froid.",
    "narrateur|Victorino glisse le pied, sans se presser.",
    "enfant-m|On le sent, maman.",
    "maman|Tu le sens sur tes joues ?",
    "enfant-m|Oui, il est tiède.",
    "narrateur|Le pain grillé repose dans l'assiette.",
    "enfant-m|L'éclat, il est là.",
    "papa|On le laisse ?",
    "enfant-m|Oui.",
    "narrateur|L'éclat de mie tient sur le toast.",
]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    wanted = {
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_Q0001",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    }
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in wanted]
    extra = wanted - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{SID} chunks inattendus missing={missing} extra={extra}")

    by = {
        "CHK_T0000_P0000": voice(
            by_src["CHK_T0000_P0000"], P0000, "opening", "feuilles,cloche,pas",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "attendre",
                    "accepted_examples": (
                        "attendre | il attend | lever la main | la main"
                    ),
                    "retry_prompt": (
                        "Il lève la main et il attend. Que fait Victorino ?"
                    ),
                    "engine_ok_text": "Oui, il attend.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "chaise,voix",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "feuilles,pas",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "toast,feuille",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "dorian" in blob:
        raise SystemExit(f"{SID}: Dorian interdit")
    if "ninon" in blob:
        raise SystemExit(f"{SID}: Ninon interdite")
    if "éclat de croûte" in blob or "éclat de croute" in blob:
        raise SystemExit(f"{SID}: BAN éclat de croûte")
    if "grain de feuille" in blob:
        raise SystemExit(f"{SID}: BAN grain de feuille")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if not all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_ssml"].startswith("<speak>")
        for c in chunks
    ):
        raise SystemExit(f"{SID}: TTS incomplet")
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
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Victorino veut parler. Que fait-il d'abord ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt") or ""
    if "dorian" in retry.lower():
        raise SystemExit(f"{SID}: retry Dorian resté")
    if "victorino" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans Victorino: {retry}")
    mait = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("maitresse|")
    ).lower()
    if any(x in mait for x in ("écoute", "range", "merci", "règle", "leçon", "tour")):
        raise SystemExit(f"{SID}: maîtresse leçon parlée: {mait}")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nwords = sum(words(c["text"]) for c in chunks)
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N1 (≤10 mots/phrase), audio familial\n"
        "- **Leçon :** COL.ECO.002 — attendre son tour / lever la main "
        "avant de parler (vécue : parler trop vite → mots perdus ; lever "
        "la feuille → personne ne regarde ; lever la main, attendre, puis dire)\n"
        "- **Personnages :** Victorino, papa, maman (maîtresse = label, pas "
        "de leçon parlée). Dorian interdit. Papa ajouté.\n"
        "- **Lieu :** cuisine au toast (pain grillé, beurre), classe, puis "
        "maison ; veste bleue, feuilles sèches, porte rouge, cloche, tapis "
        "gris, feuille brune, cube jaune\n"
        "- **Indice unique :** éclat de mie (toast du matin → doigt en "
        "classe → toast du soir). Pas éclat de croûte (BAN 001-03), pas "
        "grain de feuille (BAN). Distinct 002-01..07.\n"
        "- **Question moteur :** Victorino veut parler. Que fait-il "
        "d'abord ? → attendre. retry : Que fait Victorino ? (plus Dorian)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le beurre fond tout seul. La cuisine sent le toast chaud. Le pain "
        "grillé saute. Sur le toast, un éclat de mie brille. Victorino veut "
        "montrer la feuille brune **maintenant**. Il saisit trop vite : "
        "l'éclat saute. Il coupe papa : les voix se mélangent. Sourire "
        "parti, poitrine qui se bouscule. Papa se baisse. Dehors, les "
        "feuilles font crac. À la classe, il dit la feuille tout de suite : "
        "les mots se cognent, personne n'entend. Il lève la feuille : elle "
        "retombe, personne ne regarde. Il refuse de foncer, lève la main, "
        "reste, dit le trou. Une tête se tourne. Le soir, il coupe papa, "
        "refuse, attend le silence, dit. Merci vécu. Il pose la feuille "
        "trop vite, s'arrête, pose plus lentement. Sur le toast, l'éclat "
        "de mie tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : beurre, toast chaud, pain grillé, assiette, veste "
        "bleue, feuilles sèches, porte rouge, cloche, tapis gris, cube "
        "jaune, sel.\n"
        "- Désir : montrer la feuille brune (petit trou) **maintenant**.\n"
        "- Objet : feuille brune, toast, veste bleue.\n"
        "- Indice unique : éclat de mie, vu dès l'ouverture, payé sur le "
        "toast.\n"
        "- Urgence douce : le mot de la feuille est là, papa n'a pas fini, "
        "un camarade parle d'un caillou.\n"
        "- Imprévu 1 : il coupe, saisit le toast ; à l'école sa phrase se "
        "cogne à la classe ; il lève la feuille trop vite.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après la phrase entière.\n"
        "- Imprévu 2 (plus rusé) : à la porte il veut tout dire ; la "
        "feuille glisse. Il refuse de foncer.\n"
        "- Résolution : bouche fermée, main en l'air, phrase entière, "
        "pose plus lentement.\n"
        "- Retour : feuille près du sel, toast froid, éclat qui tient.\n\n"
        "## Vécu\n\n"
        "Victorino veut montrer la feuille brune **maintenant**. "
        "Impatience, puis épaules qui tombent quand les mots se perdent. "
        "Papa se baisse, pose une question, ne récite pas la règle. "
        "Victorino agit : bouche fermée, main en l'air, phrase entière. "
        "Merci vécu après l'écoute. Fin : l'éclat du début tient sur le "
        "toast.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau « La feuille brune de Victorino » (dump), pas "
        "« La feuille collée au lait » (xlsx / audit example2). Monde "
        "dump : pain grillé, beurre, cuisine toast, puis classe.\n"
        "- Ouverture inventée (beurre qui fond, toast qui saute, éclat "
        "de mie), pas gabarit v2, pas « joue au salon ». Craft example4 "
        "(061, 093, 025) : sourire qui disparaît, refuse de foncer, "
        "indice payé.\n"
        "- Distinct de COL.ECO.002-01..07 (carotte, seau, carton, mousse, "
        "pompon, manteau, linge). Ici : attendre son tour, vécu cuisine "
        "toast puis classe.\n"
        "- Dorian → Victorino (dump et retry). Papa ajouté. Maîtresse = "
        "label (bonjour, Victorino), pas de leçon parlée. Pas « il faut "
        "attendre / c'est ton tour / tu as attendu ».\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent / "
        "tout bas » retirés. Pas de merle, pas de miel.\n"
        "- Pas éclat de croûte (BAN 001-03), pas grain de feuille (BAN), "
        "pas cartable, craie, casserole.\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- Indice unique « éclat de mie » nommé à l'ouverture, revu "
        "quand il saute, revu sur le doigt, payé à la fin.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive.\n"
        f"- {nwords} mots. N1 ≤ 10. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        f"- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
