#!/usr/bin/env python3
"""ATOM-DIF.ENE.001-04 — Le soleil du grand pinceau (F-NAR-019, N2, DIF.ENE.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.ENE.001-04"
TITLE = "Le soleil du grand pinceau"
N2 = LIMITS["N2"]
CHARS = "Nino, Victorino, papa, maman"
SETTING = (
    "atelier peinture : chiffon bleu, papier, fenêtre, tube jaune, "
    "grand pinceau bleu, pots, évier"
)
INDICE = "éclat de chiffon"
FIL = (
    "Une virgule jaune colle au bouchon. Sur le chiffon bleu, un "
    "éclat de chiffon brille. Nino veut le grand pinceau, maintenant, "
    "pour un soleil. Victorino saute, lève trop vite : une tache, le "
    "papier part. Sourire parti. Nino refuse de foncer, file des pots. "
    "Victorino veut passer. Nino appelle maman. Évier froid. Merci "
    "vécu. L'éclat de chiffon tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(flaque|piquet|bol|vitre|buée|buee|robinet|cerceau|drap|"
    r"sauge|chaise|maîtresse|maitresse)\b",
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
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "ce n'est pas une faute",
    "ce n est pas une faute",
    "on peut jouer",
    "on peut attendre",
    "demander à un adulte",
    "demander a un adulte",
    "on peut demander",
    "vous jouez",
    "on joue",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "trois notes",
    "lumière couleur de miel",
    "lumiere couleur de miel",
    "éclat de pinceau",
    "éclat de vitre",
    "éclat de buée",
    "éclat de buee",
    "éclat de flaque",
    "éclat de piquet",
    "éclat de bol",
    "éclat de robinet",
    "éclat de cerceau",
    "éclat de drap",
    "éclat de sauge",
    "éclat de chaise",
    "éclat de miette",
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
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat d'ombre",
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
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de cartable",
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
    "éclat de enveloppe",
    "éclat d'émail",
    "éclat d'email",
    "éclat de samare",
    "éclat de bassine",
    "éclat de planche",
    "éclat de figue",
    "éclat de coussin",
    "éclat de tiroir",
    "éclat de perron",
    "éclat de limace",
    "éclat de botte",
    "éclat de résine",
    "éclat de resine",
    "éclat de cageot",
    "grain de pin",
    "lune d'étain",
    "lune d'etain",
    "point de gouttière",
    "point de gouttiere",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de chiffon",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_grand_pinceau_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="énergie",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=victorino_saute_que_peut_on_faire; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="pots",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_refuse_de_foncer_file_des_pots; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de chiffon",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis prudence; intensite=2; destinataire=enfant; "
            "sous_texte=victorino_veut_passer_nino_appelle_maman; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de chiffon",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bleu; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer",
    "accepted_examples": (
        "jouer | attendre | un adulte | jouer ou attendre | demander"
    ),
    "retry_prompt": "On peut jouer. On peut attendre. Que fait Nino ?",
    "engine_ok_text": "Oui, jouer.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "peinture,papier",
        [
            "narrateur|Une virgule jaune colle au bouchon.",
            "narrateur|Papa tourne le tube jaune.",
            "enfant-m|Elle colle, papa !",
            "papa|Tu la sens, sur tes doigts ?",
            "enfant-m|Oui, elle est froide.",
            "narrateur|Ça sent le papier neuf, un peu.",
            "papa|Tu le sens, Nino ?",
            "enfant-m|Oui, papa.",
            "enfant-m|Ça sent le papier.",
            "narrateur|Un chiffon bleu sèche près de la fenêtre.",
            "enfant-m|Il pend, maman.",
            "maman|Tu le vois, le chiffon ?",
            "enfant-m|Oui, il est mouillé.",
            "narrateur|Sur le bleu, un éclat de chiffon brille.",
            "enfant-m|Il brille, papa !",
            "papa|Tu le vois, ce petit point ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|Maman pose de grandes feuilles.",
            "enfant-m|Elles sont rudes, maman.",
            "maman|On a de la place, tous les deux.",
            "enfant-m|Oui, maman.",
            "papa|Le coin des pots est libre, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le pot bleu fait un petit clac.",
            "enfant-m|L'eau est trouble.",
            "papa|L'eau du pot, Nino ?",
            "enfant-m|Oui, elle bouge.",
            "maman|Le grand pinceau est dans le pot ?",
            "enfant-m|Oui, il est bleu.",
            "narrateur|En ce moment, Nino veut le grand pinceau.",
            "enfant-m|Je veux le grand pinceau, maintenant !",
            "enfant-m|Pour un soleil, maman.",
            "maman|Un grand soleil jaune ?",
            "enfant-m|Oui, toute la feuille.",
            "papa|Avec Victorino, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Victorino arrive en sautant.",
            "enfant-m|Victorino !",
            "copain|J'arrive !",
            "narrateur|Il tourne près de la table.",
            "narrateur|Ses pieds tapent le sol, fort.",
            "enfant-m|Il saute, papa.",
            "papa|Tu le vois sauter, toi ?",
            "enfant-m|Oui, beaucoup.",
            "maman|Ses mains bougent vite, Nino ?",
            "enfant-m|Oui, maman.",
            "copain|Le pinceau !",
            "narrateur|Victorino prend le grand pinceau bleu.",
            "narrateur|Il le lève trop vite.",
            "enfant-m|Oh !",
            "narrateur|Une goutte jaune tombe sur la table.",
            "enfant-m|Ça tache !",
            "narrateur|Le papier glisse vers le bord.",
            "enfant-m|Il part !",
            "copain|Vite !",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu, lourdes.",
            "narrateur|Maman s'accroupit à la même hauteur.",
            "maman|Tu veux le soleil avec Victorino ?",
            "enfant-m|Oui, maman.",
            "papa|Tes mains sont collantes, Nino ?",
            "enfant-m|Un peu, papa.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Il referme les mains.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le chiffon, un instant.",
            "narrateur|L'éclat de chiffon tremble, puis tient.",
            "enfant-m|L'éclat, papa ?",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur le bleu.",
            "copain|Moi, le pinceau.",
            "narrateur|Le pinceau tremble dans sa main.",
            "narrateur|Victorino ne le pose pas.",
            "narrateur|Nino regarde maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorino a de l'énergie.",
            "narrateur|Que peut-on faire ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "pinceau,pots",
        [
            "narrateur|Nino tend la main, sans se presser.",
            "enfant-m|C'est à moi, le pinceau ?",
            "copain|Oui.",
            "narrateur|Victorino pose le pinceau dans le pot.",
            "enfant-m|Il est lourd, papa.",
            "papa|Tu le tiens bien, Nino ?",
            "enfant-m|Oui, papa.",
            "maman|La feuille est prête ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nino peint un rond jaune.",
            "enfant-m|C'est le soleil.",
            "papa|Il est grand, ce rond ?",
            "enfant-m|Presque.",
            "narrateur|Une petite tache reste près du bord.",
            "enfant-m|Elle est restée.",
            "maman|Tu la laisses, Nino ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Maintenant c'est toi.",
            "copain|Une ligne !",
            "narrateur|Victorino peint une ligne, plus lente.",
            "narrateur|La ligne part du rond.",
            "enfant-m|C'est un rayon, papa.",
            "papa|Tu le vois, le rayon ?",
            "enfant-m|Oui, il part.",
            "maman|Les pots attendent, Nino ?",
            "enfant-m|On fait une file.",
            "narrateur|Ils posent les pots, un par un.",
            "copain|Vite !",
            "narrateur|Victorino avance trop près.",
            "enfant-m|Oh.",
            "narrateur|Nino refuse de foncer, cette fois.",
            "narrateur|Il reste dans la file.",
            "narrateur|Personne ne dit la suite à voix haute.",
            "narrateur|Il regarde l'éclat de chiffon.",
            "papa|Tu vois le point, Nino ?",
            "enfant-m|Oui, sur le bleu.",
            "copain|Moi aussi.",
            "maman|Les pots sont en file, les garçons ?",
            "enfant-m|Oui, maman.",
            "papa|Chacun a de la peinture ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le ventre de Nino se desserre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "evier,eau",
        [
            "narrateur|Victorino glisse un pas sur le côté.",
            "copain|Je passe !",
            "enfant-m|Oh.",
            "narrateur|Il veut le pinceau, sans la file.",
            "narrateur|Nino ouvre la main, presque.",
            "narrateur|Nino refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "enfant-m|Maman, on fait quoi ?",
            "maman|Tu m'as appelée, Nino.",
            "maman|Victorino, viens jusqu'à l'évier.",
            "copain|Non.",
            "maman|L'eau est là, tout près.",
            "narrateur|Victorino marche, un peu raide.",
            "narrateur|Il pose les mains sous l'eau.",
            "copain|Elle pique !",
            "enfant-m|Elle est froide, papa.",
            "papa|L'eau de l'évier, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Victorino souffle, longuement.",
            "maman|Merci, Nino.",
            "narrateur|Maman a vu les mains ouvertes.",
            "papa|Tes pieds tiennent le sol, Victorino ?",
            "copain|Oui.",
            "enfant-m|On rince les pinceaux ?",
            "maman|Ensemble, Nino ?",
            "enfant-m|Oui, maman.",
            "narrateur|L'eau devient un peu jaune.",
            "enfant-m|Elle est jaune, papa.",
            "papa|La peinture part, Nino ?",
            "enfant-m|Un peu, papa.",
            "narrateur|Sur le bord, un éclat de chiffon luit.",
            "enfant-m|L'éclat, maman ?",
            "maman|Tu le vois, sur le bleu ?",
            "enfant-m|Oui, maman.",
            "copain|Moi aussi.",
            "narrateur|Le papier a failli partir.",
            "enfant-m|Il est resté.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "peinture,chiffon",
        [
            "narrateur|Le soleil jaune reste sur la table.",
            "enfant-m|Il a des rayons, papa.",
            "papa|Tu les vois, sur la feuille ?",
            "enfant-m|Oui, toute la feuille.",
            "maman|Le grand pinceau dort dans le pot bleu.",
            "enfant-m|Il est calme, maman.",
            "papa|On laisse sécher, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Nino souffle sur la feuille.",
            "narrateur|La peinture brille un peu.",
            "copain|Le rond est beau.",
            "enfant-m|Avec la petite tache.",
            "maman|La tache est restée, Nino ?",
            "enfant-m|Oui, maman.",
            "papa|Le papier a failli partir, vous deux ?",
            "enfant-m|Oui, papa.",
            "copain|Oui.",
            "narrateur|Le chiffon bleu sèche près de la fenêtre.",
            "enfant-m|L'éclat est là, maman.",
            "maman|Tu le vois sur le bleu ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un éclat de chiffon tient sur le bleu.",
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
    if n_clue != 5:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 5)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Nino = enfant-m, Victorino = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Victorino absent (copain)")
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
        "demander à un adulte",
        "demander a un adulte",
        "on peut demander",
        "il faut attendre",
        "on doit demander",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Victorino a de l'énergie. Que peut-on faire ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "jouer | attendre | un adulte | jouer ou attendre | demander"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "On peut jouer. On peut attendre. Que fait Nino ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    copain_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    ).lower()
    if "non" not in copain_txt:
        raise SystemExit(f"{SID}: Victorino sans non")
    if "je passe" not in copain_txt:
        raise SystemExit(f"{SID}: Victorino sans je passe")
    for need in (
        "chiffon",
        "papier",
        "tube",
        "pinceau",
        "pot",
        "évier",
        "fenêtre",
        "soleil",
    ):
        if need not in blob:
            raise SystemExit(f"{SID}: manque {need}")
    for ban in (
        "éclat de pinceau",
        "éclat de vitre",
        "éclat de flaque",
        "éclat de piquet",
        "éclat de bol",
        "mila",
        "rayan",
        "tout doux",
        "tout calme",
        "flaque",
        "piquet",
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
        "- **Leçon :** DIF.ENE.001 — énergie (vécue : Nino refuse de "
        "foncer, file des pots, appelle maman, évier froid). JAMAIS dite "
        "dans le récit. Pas « ce n'est pas une faute », pas « on peut "
        "jouer / attendre / demander à un adulte ».\n"
        "- **Personnages :** Nino, Victorino, papa, maman. Troupe D16. "
        "Nino = enfant-m (veut maintenant, refuse de foncer). Victorino "
        "= copain (énergie, saute, Je passe, Non). Papa et maman "
        "parlent. Mila / Rayan absents.\n"
        "- **Lieu :** atelier peinture (chiffon bleu, papier, fenêtre, "
        "tube jaune, grand pinceau bleu, pots, évier). ≠ 001-01 flaque. "
        "≠ 001-02 piquet. ≠ 001-03 bol. Pas vitre / buée / éclat de "
        "pinceau.\n"
        "- **Indice unique :** éclat de chiffon (brille sur le bleu → "
        "tremble → Nino le regarde → luit à l'évier → tient sur le "
        "bleu). Pas éclat de pinceau (BAN).\n"
        "- **Question moteur :** « Victorino a de l'énergie. Que "
        "peut-on faire ? » expected **jouer**. Retry dump : On peut "
        "jouer. On peut attendre. Que fait Nino ? Non récité dans les "
        "autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / "
        "graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin "
        "heureuse. `chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une virgule jaune colle au bouchon. Papier neuf, chiffon bleu "
        "près de la fenêtre. Sur le bleu, un éclat de chiffon brille. "
        "Nino veut le grand pinceau **maintenant**, pour un soleil. "
        "Victorino arrive en sautant, prend le pinceau trop vite. "
        "Goutte, tache, papier qui part. Sourire parti, poitrine, "
        "épaules. Maman s'accroupit. Nino refuse de foncer, observe "
        "l'éclat. Question. Il tend la main sans se presser, rond "
        "jaune, rayon, file des pots. Deuxième ruse : Je passe. Il "
        "refuse, appelle maman. Évier froid. Merci vécu. Le papier a "
        "failli partir. Un éclat de chiffon tient sur le bleu.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : atelier, virgule jaune, papier, chiffon, pots, "
        "évier.\n"
        "- Désir : le grand pinceau bleu, maintenant, pour un soleil.\n"
        "- Objet : grand pinceau bleu, tube jaune, pots, chiffon.\n"
        "- Indice unique : éclat de chiffon, vu dès l'ouverture, payé "
        "sur le bleu. Pas éclat de pinceau.\n"
        "- Urgence douce : le soleil, maintenant ; Victorino saute.\n"
        "- Imprévu 1 : pinceau trop vite ; goutte ; papier qui part.\n"
        "- Cue : maman à la même hauteur ; un merci vécu après l'évier.\n"
        "- Imprévu 2 (plus rusé) : Je passe, sans la file ; Non à "
        "l'évier.\n"
        "- Résolution : il refuse de foncer, file des pots, appelle "
        "maman, mains sous l'eau froide.\n"
        "- Retour : soleil, tache restée, papier qui a failli, éclat "
        "sur le bleu.\n\n"
        "## Vécu\n\n"
        "Nino veut **maintenant**. Victorino saute, veut passer. Le "
        "silence compte. Maman s'accroupit, ne récite pas « ce n'est "
        "pas une faute ». La leçon se voit : les mains qui se ferment, "
        "la file, l'appel, l'eau froide. Merci vécu après les mains "
        "ouvertes. Fin : l'éclat du début tient sur le bleu. Le "
        "dénouement a failli : le papier a failli partir.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé : Le soleil du grand pinceau. Lieu du "
        "dump : atelier peinture, chiffon, papier, fenêtre, tube, "
        "pinceau, pots, évier. Pas flaque / piquet / bol. Pas éclat "
        "de pinceau / vitre / buée.\n"
        "- Ouverture inventée (virgule jaune au bouchon), pas « Nino "
        "est à l'atelier », pas un gabarit v2. example4 018 / 050 / "
        "082 : corps (sourire parti, poitrine, accroupi), 2e ruse, "
        "refuse de foncer, fin qui a failli.\n"
        "- Indice unique : éclat de chiffon. Pas merle-trois-notes, "
        "miel, tache / flèche / marque / symbole.\n"
        "- Tics encore / déjà / tout doux / tout calme et `aujourd'hui` "
        "retirés. Morale énergie / faute / on peut jouer hors question. "
        "Mila / Rayan → Nino / Victorino.\n"
        "- Une phrase par ligne (plus « Oui. Ça sent le papier. » "
        "collé).\n"
        "- Question moteur inchangée. expected **jouer**. 5 chunks, "
        "kinds inchangés.\n"
        "- Voix : `_write_atom_dif_cor_003_03.py` / "
        "`_write_atom_dif_cor_003_02.py` (profiles, ssml, xai).\n"
        f"- {nwords} mots. N2 ≤ 15. TTS : notes, ssml, xai, piper par "
        "chunk. `slow` = question + fin.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n"
        "- 1 × `en ce moment`, 1 × merci adulte, 5 × éclat de chiffon\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
