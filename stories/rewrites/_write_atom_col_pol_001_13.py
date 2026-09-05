#!/usr/bin/env python3
"""ATOM-COL.POL.001-13 — Le pain chaud de Victorino (F-NAR-019, N1)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.POL.001-13"
TITLE = "Le pain chaud de Victorino"
N1 = LIMITS["N1"]
INDICE = "éclat de dorure"
FIL = (
    "Une goutte glisse sur la vitre floue. Sur le pain, un éclat de "
    "dorure brille. Victorino veut le pain chaud maintenant. Il avance "
    "trop vite, sans le mot : la dame ne tourne pas. Il refuse de "
    "foncer, dit bonjour. Merci vécu. Le sachet glisse. Sur le pain, "
    "l'éclat de dorure tient."
)
CHARS = "Victorino, papa, maman"
SETTING = "trottoir, vitre floue, pains dorés, odeur de beurre, boulangerie"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(pavé|pave|croissant|corbeille|croûte|croute|farine|"
    r"réverbère|reverbere|nappe|cacao|georges|brioche|gaufre|"
    r"petit pain)\b",
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
    "j'ai dit bonjour",
    "j'ai dit s'il te plaît",
    "j'ai dit s'il te plait",
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
    "il faut demander",
    "tu as dit les mots",
    "les trois mots",
    "on dit bonjour",
    "on dit au revoir",
    "tu as suivi",
    "tu as dit merci",
    "tu as dit s'il te plaît",
    "tu as dit s'il te plait",
    "tu as dit bonjour",
    "tu demandes",
    "gouttière",
    "gouttiere",
    "tache de couleur",
    "ombre en forme",
    "marque fine",
    "minuscule symbole",
    "grain de miette",
    "grain de sucre",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "trait de craie",
    "malaise",
    "secret",
    "éclat de pavé",
    "éclat de pave",
    "éclat de croissant",
    "éclat de corbeille",
    "éclat de croûte",
    "éclat de croute",
    "éclat de farine",
    "éclat de réverbère",
    "éclat de reverbere",
    "éclat de nappe",
    "éclat de mie",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de cloche",
    "éclat de sac",
    "éclat de citron",
    "éclat de manteau",
    "éclat de lampe",
    "éclat de vitre",
    "éclat de tasse",
    "éclat de bâche",
    "éclat de bache",
    "éclat de panier",
    "éclat de carte",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de carotte",
    "éclat de pompon",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de cartable",
    "éclat de pinceau",
    "éclat de casserole",
    "éclat de wagon",
    "éclat de buée",
    "éclat de buee",
    "éclat de caisse",
    "éclat de goutte",
    "éclat de grain",
    "éclat de liste",
    "éclat de sonnette",
    "éclat de crayon",
    "éclat de marche",
    "éclat de laine",
    "éclat de bec",
    "éclat de fraise",
    "éclat de ticket",
    "éclat de bouton",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat d'horloge",
    "éclat de colle",
    "éclat de lessive",
    "éclat de carreau",
    "éclat de boîte",
    "éclat de boite",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de orange",
    "éclat de quille",
    "éclat de promenade",
    "éclat de pin",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de tapis",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de corde",
    "éclat de pince",
    "éclat de terre",
    "éclat de volet",
    "pli de voile",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de dorure",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_pain_chaud_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="dame",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_dit_bonjour; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="Bonjour",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_salue_puis_demande; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="sachet",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_quand_le_sachet_glisse; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de dorure",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_pain; "
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
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
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
    "narrateur|Une goutte glisse sur la vitre floue.",
    "narrateur|Derrière, les pains dorés attendent.",
    "enfant-m|Ils brillent, papa.",
    "papa|Tu les vois, à travers le verre ?",
    "narrateur|Une odeur de beurre court sur le trottoir.",
    "enfant-m|Ça sent le beurre, maman.",
    "maman|Oui, le long du verre.",
    "narrateur|Le trottoir est mouillé, un peu froid.",
    "enfant-m|Mes chaussures font toc.",
    "papa|On les entend, sous tes pieds ?",
    "enfant-m|Oui, papa.",
    "maman|On reste près de la vitre ?",
    "enfant-m|Oui, maman.",
    "narrateur|Un pain rond se tient derrière le verre.",
    "narrateur|Sa peau est dorée, un peu lisse.",
    "enfant-m|Celui-là, maman.",
    "narrateur|Sur le pain, un éclat de dorure brille.",
    "enfant-m|Il est jaune, papa.",
    "papa|C'est le pain, sous la lumière.",
    "maman|Tu le touches, Victorino ?",
    "narrateur|Victorino pose un doigt sur le verre.",
    "narrateur|Le verre est tiède, un peu flou.",
    "enfant-m|Il pique un peu.",
    "papa|On pousse la porte ?",
    "enfant-m|Oui, maintenant !",
    "narrateur|En ce moment, Victorino pose la main sur la porte.",
    "narrateur|La cloche fait ding, un peu fort.",
    "narrateur|L'air chaud touche les joues.",
    "narrateur|Ça sent le pain et le beurre.",
    "enfant-m|Il est chaud ici.",
    "maman|On reste près du bois ?",
    "enfant-m|Oui.",
    "narrateur|Une baguette se tient debout, près du bois.",
    "enfant-m|Elle est grande, papa.",
    "papa|Tu la vois, à côté du pain ?",
    "enfant-m|Oui.",
    "narrateur|La dame essuie le bois du comptoir.",
    "narrateur|Le torchon reste dans ses mains.",
    "enfant-m|Celui-là, maintenant !",
    "narrateur|Victorino avance trop vite vers le bois.",
    "narrateur|Sa voix se mélange à la cloche.",
    "enfant-m|Oh.",
    "narrateur|La dame ne tourne pas la tête.",
    "narrateur|Le pain rond reste près du bois.",
    "narrateur|Le sourire de Victorino disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "enfant-m|Elle ne m'entend pas, papa.",
    "papa|Tu la vois, Victorino ?",
    "narrateur|Papa se baisse à sa hauteur.",
    "narrateur|L'éclat de dorure tremble, puis tient.",
    "narrateur|Les épaules de Victorino tombent un peu.",
    "maman|La baguette attend, là.",
    "enfant-m|Le mien sera chaud.",
]

Q0001 = [
    "narrateur|Victorino parle à la dame.",
    "narrateur|Quels mots dit-il ?",
]

C0001 = [
    "narrateur|Victorino avance trop vite vers le bois.",
    "enfant-m|Le pain, maintenant !",
    "narrateur|Sa voix se mélange à la cloche.",
    "enfant-m|Oh.",
    "narrateur|Le torchon ne bouge pas.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Victorino refuse de foncer.",
    "narrateur|Il recule d'un pas, près du bois.",
    "papa|Tu veux venir près du bois ?",
    "narrateur|Papa reste à sa hauteur.",
    "narrateur|Victorino écoute la cloche, un instant.",
    "narrateur|Par la vitre, l'éclat de dorure brille.",
    "enfant-m|Bonjour.",
    "maman|Bonjour.",
    "enfant-m|Un pain, s'il te plaît.",
    "enfant-m|Celui de la vitre.",
    "narrateur|Derrière le bois, une main se tend.",
    "narrateur|Le papier enveloppe le pain rond.",
    "narrateur|Le sachet est chaud contre la veste.",
    "enfant-m|Merci.",
    "papa|Merci, Victorino.",
    "narrateur|Papa a entendu toute la phrase.",
    "narrateur|Le ventre de Victorino se desserre.",
    "enfant-m|Il est chaud, maman.",
    "maman|Tu as les mains dessus ?",
    "enfant-m|Oui, maman.",
    "narrateur|Le papier est un peu gras, un peu tiède.",
    "enfant-m|Ça sent le beurre.",
    "maman|On sort ?",
    "enfant-m|Oui, maman.",
    "narrateur|Victorino tient le sachet à deux mains.",
    "narrateur|Le fond du sac est tiède.",
]

END = [
    "narrateur|Ils passent le pas de bois.",
    "narrateur|La cloche fait ding.",
    "narrateur|L'air du trottoir revient sur les joues.",
    "narrateur|Victorino tire le sachet trop vite.",
    "enfant-m|Je le montre, d'un coup !",
    "narrateur|Le papier glisse entre les doigts.",
    "narrateur|Le pain rond penche vers le sol.",
    "enfant-m|Oh.",
    "narrateur|Victorino avance les mains.",
    "narrateur|Puis il s'arrête net.",
    "enfant-m|Attends, je regarde.",
    "narrateur|Papa attend, sans parler.",
    "narrateur|Victorino refuse de foncer, cette fois.",
    "narrateur|Ses mains se ferment, puis s'ouvrent.",
    "narrateur|Il ramène le sachet contre sa veste.",
    "narrateur|Il écoute le trottoir, un instant.",
    "enfant-m|Il est chaud, papa.",
    "papa|Tu le portes jusqu'à la rue ?",
    "enfant-m|Oui, papa.",
    "maman|On marche ?",
    "enfant-m|Oui, maman.",
    "narrateur|Une goutte glisse du verre, dehors.",
    "narrateur|Elle fait un trait sur la vitre floue.",
    "enfant-m|Comme au début.",
    "maman|Tu la vois, sur le verre ?",
    "enfant-m|Oui, maman.",
    "narrateur|Victorino serre le sachet contre lui.",
    "enfant-m|Il reste chaud.",
    "papa|On rentre.",
    "narrateur|Le trottoir est froid, un peu lisse.",
    "enfant-m|Je l'entends, papa.",
]

FIN = [
    "narrateur|Ils s'arrêtent sous la vitre floue.",
    "narrateur|La goutte a fini sa course.",
    "enfant-m|Le pain brillait, papa.",
    "papa|Tu le vois, comme dans la boutique ?",
    "enfant-m|Oui, sur le pain.",
    "narrateur|Victorino pose le sachet contre la veste.",
    "maman|On le garde au chaud ?",
    "enfant-m|Oui, maman.",
    "enfant-m|Ça sent le beurre, maman.",
    "maman|Il est contre toi.",
    "narrateur|Une vapeur monte du papier.",
    "narrateur|Victorino respire, plus large.",
    "papa|On rentre ?",
    "enfant-m|Oui.",
    "narrateur|Les joues de Victorino se réchauffent.",
    "narrateur|Le sachet reste tiède sous la main.",
    "enfant-m|On le voit, maman.",
    "maman|Tu le vois sur le pain ?",
    "enfant-m|Oui, l'éclat.",
    "narrateur|L'éclat de dorure tient sur le pain.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "cloche,porte,pas",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "bonjour",
                    "accepted_examples": (
                        "bonjour | s'il te plaît | merci | bonjour merci"
                    ),
                    "retry_prompt": (
                        "Il dit bonjour. Quels mots dit Victorino ?"
                    ),
                    "engine_ok_text": "Oui, bonjour.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "papier,cloche",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "pas,papier",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "pain,verre",
            extra={"pause_before_ms": 200},
        ),
    }

    for c in src["chunks"]:
        cid = c["chunk_id"]
        if c.get("kind") != by[cid].get("kind"):
            raise SystemExit(f"{cid}: kind changé")

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
    if "georges" in blob:
        raise SystemExit(f"{SID}: Georges interdit")
    if "dorian" in blob:
        raise SystemExit(f"{SID}: Dorian interdit")
    if "ninon" in blob:
        raise SystemExit(f"{SID}: Ninon interdite")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "bonjour" not in blob:
        raise SystemExit(f"{SID}: manque bonjour vécu")
    if "s'il te plaît" not in blob:
        raise SystemExit(f"{SID}: manque s'il te plaît vécu")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Victorino = enfant-m)")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    if "dame|" in "\n".join(c["script"] for c in chunks):
        raise SystemExit(f"{SID}: la dame a une réplique (label seulement)")
    if "croissant" in blob:
        raise SystemExit(f"{SID}: croissant (001-07 / 001-10)")
    if "farine" in blob:
        raise SystemExit(f"{SID}: farine (001-01 / 001-07)")
    if "pavé" in blob or "pave" in blob:
        raise SystemExit(f"{SID}: pavé (001-01)")
    if "corbeille" in blob:
        raise SystemExit(f"{SID}: corbeille (001-10)")
    if "croûte" in blob or "croute" in blob:
        raise SystemExit(f"{SID}: croûte (ECO.001-03)")
    if "réverbère" in blob or "reverbere" in blob:
        raise SystemExit(f"{SID}: réverbère (001-08)")
    if "nappe" in blob:
        raise SystemExit(f"{SID}: nappe (ECO.001-03)")
    if "cacao" in blob:
        raise SystemExit(f"{SID}: cacao (ancienne passe)")
    if "éclat de pavé" in blob or "éclat de pave" in blob:
        raise SystemExit(f"{SID}: éclat de pavé (BAN 001-01)")
    if "éclat de croissant" in blob:
        raise SystemExit(f"{SID}: éclat de croissant (BAN 001-07)")
    if "éclat de corbeille" in blob:
        raise SystemExit(f"{SID}: éclat de corbeille (BAN 001-10)")
    if "éclat de croûte" in blob or "éclat de croute" in blob:
        raise SystemExit(f"{SID}: BAN éclat de croûte")
    if not all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_xai_tags"] != c["text"]
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
    if "maman|" not in blob:
        raise SystemExit(f"{SID}: maman absente")
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Victorino parle à la dame. Quels mots dit-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "bonjour":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt") or ""
    if "georges" in retry.lower():
        raise SystemExit(f"{SID}: retry Georges resté")
    if "victorino" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans Victorino: {retry}")

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
        "- **Leçon :** COL.POL.001 — bonjour (s'il te plaît et merci liés), "
        "vécue : veut le pain chaud maintenant ; première idée échoue ; "
        "refuse de foncer ; dit bonjour. Jamais dite comme règle.\n"
        "- **Personnages :** Victorino, papa, maman. Troupe D16. Dump "
        "Georges → INTERDIT. `enfant-m`. « la dame » = label, pas de "
        "réplique. Adultes parlants = papa/maman. Maman ajoutée.\n"
        "- **Lieu :** trottoir, vitre floue, pains dorés, odeur de beurre, "
        "boulangerie. ≠ POL.001-01 Nino pavé/petit pain. ≠ POL.001-07 "
        "Mila croissant/farine. ≠ POL.001-10 Amir corbeille. ≠ ECO.001-03 "
        "Victorino nappe/croûte.\n"
        "- **Indice unique :** éclat de dorure (pain dès l'ouverture → "
        "tremble à l'échec → brille au silence → tient sur le pain). "
        "Pas pavé, croissant, corbeille, croûte, farine, réverbère.\n"
        "- **Question moteur :** « Victorino parle à la dame. Quels mots "
        "dit-il ? » expected **bonjour**. retry Georges→Victorino.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte glisse sur la vitre floue. Pains dorés, odeur de "
        "beurre sur le trottoir. Chaussures qui font toc. Sur le pain "
        "rond, un éclat de dorure brille. Victorino veut le pain "
        "**maintenant**. Première idée : avancer trop vite, sans le mot. "
        "La cloche mélange sa voix. La dame ne tourne pas. Sourire parti, "
        "épaules basses. Papa se baisse. Il refuse de foncer, dit "
        "bonjour, puis s'il te plaît. Le sachet arrive. Merci vécu. "
        "Dehors, il tire trop vite : le papier glisse, le pain penche. "
        "Il refuse, serre. Sous la vitre, l'éclat de dorure tient sur "
        "le pain.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : goutte sur vitre floue, pains dorés, odeur de beurre, "
        "trottoir, chaussures toc, pain rond, baguette debout, cloche, "
        "bois, veste, sachet. ≠ 001-01 petit pain / éclat de pavé. ≠ "
        "001-07 croissant / farine. ≠ 001-10 corbeille. ≠ ECO.001-03 "
        "nappe / éclat de croûte. ≠ 001-08 réverbère / brioche.\n"
        "- Désir : le pain chaud doré, maintenant.\n"
        "- Objet : pain rond, baguette, sachet, vitre floue, cloche, veste.\n"
        "- Indice unique : éclat de dorure, vu dès l'ouverture, payé "
        "sur le pain.\n"
        "- Urgence douce : le pain derrière le verre, la dame de dos.\n"
        "- Imprévu 1 : parler trop vite, sans bonjour ; la cloche et le "
        "torchon arrêtent le geste.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après la phrase "
        "entière.\n"
        "- Imprévu 2 (plus rusé) : tirer le sachet d'un coup, papier qui "
        "glisse, pain qui penche.\n"
        "- Résolution : il refuse de foncer, dit bonjour, serre le "
        "sachet contre la veste.\n"
        "- Retour : goutte au bout de sa course, vitre floue, éclat de "
        "dorure sur le pain.\n\n"
        "## Vécu\n\n"
        "Leçon COL.POL.001 (bonjour d'abord, s'il te plaît, merci) "
        "greffée, jamais annoncée. La première idée (prendre maintenant, "
        "sans le mot) échoue. Le choix de Victorino change l'action. Un "
        "« en ce moment ». Un merci vécu. Adulte + question. Troupe "
        "D16 : Victorino, papa, maman. N1.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le pain chaud de Victorino (noyau dump). Dump Georges "
        "→ INTERDIT. Maman ajoutée. Pas « Le cacao de Victorino » "
        "(passe café).\n"
        "- Question moteur : « Victorino parle à la dame. Quels mots "
        "dit-il ? » (fond **bonjour** conservé). retry Victorino, pas "
        "Georges.\n"
        "- Ouverture inventée (goutte sur vitre floue), pas gabarit v2, "
        "pas « Georges va à la boulangerie », pas cacao/store/cuillère.\n"
        "- Indice unique : éclat de dorure. Pas pavé/croissant/corbeille/"
        "croûte/farine/réverbère/nappe. example4 : 077, 009, 041 "
        "(sourire parti, refuse de foncer, indice payé).\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés.\n"
        "- Interdit « bon travail / histoire finie / tu as dit les "
        "mots / les trois mots / on dit bonjour ».\n"
        "- « la dame » = label, sans réplique. Un « en ce moment ». Un "
        "merci vécu.\n"
        "- 5 chunks, kinds inchangés. TTS : notes, ssml, xai, piper par "
        "chunk. `slow` = question et fin.\n"
        f"- {nwords} mots. N1 ≤ 10. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
