#!/usr/bin/env python3
"""ATOM-DIF.BES.001-07 — Victorina observe d'abord les cartes (F-NAR-019, N2, DIF.BES.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.BES.001-07"
TITLE = "Victorina observe d'abord les cartes"
N2 = LIMITS["N2"]
INDICE = "éclat de poussière"
CHARS = "Victorina, papa, maman"
SETTING = (
    "classe, rayon de soleil, poussière, chaises de bois, "
    "table basse, cartes, horloge, foulard au crochet"
)
FIL = (
    "Un rayon coupe la classe. La poussière flotte. Dans le rayon, "
    "un éclat de poussière brille. Victorina veut montrer la pomme "
    "maintenant. Sa voix part trop fort : les cartes glissent. Elle "
    "refuse de foncer, observe, dit le mot plus bas. On le dit comme "
    "elle. Merci vécu. Un éclat de poussière reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(cube|boule|galet|couloir|tapis|tortue|manteau|bottes?|"
    r"poire|clochette|véranda|veranda|chouchou|anaïs|anais|"
    r"corentin|louise|zoé|zoe|iris|raphaël|raphael)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "miel",
    "merle",
    "grand-père",
    "grand-pere",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "maîtresse",
    "maitresse",
    "voisine",
    "panier",
    "dorure",
    "poire",
    "cloche",
    "corbeille",
    "croissant",
    "réverbère",
    "reverbere",
    "bâche",
    "bache",
    "volet",
    "pavé",
    "pave",
    "zeste",
    "parapluie",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "trois notes",
    "une chose, puis la suivante",
    "une chose puis l'autre",
    "une étape après l'autre",
    "c'est du bon travail",
    "tu as fait du bon travail",
    "on aime écouter",
    "même leçon",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "répéter la règle",
    "observer d'abord",
    "c'est la règle",
    "tu as su répéter",
    "le calme a aidé",
    "tache de couleur",
    "ombre en forme de flèche",
    "marque fine",
    "minuscule symbole",
    "grain de miette",
    "grain de laine",
    "bande bleue",
    "éclat de carte",
    "éclat de bois",
    "éclat de cube",
    "éclat de boule",
    "éclat de galet",
    "éclat de couloir",
    "éclat de panier",
    "éclat de dorure",
    "éclat de poire",
    "éclat de sac",
    "éclat de cloche",
    "éclat de corbeille",
    "éclat de croissant",
    "éclat de réverbère",
    "éclat de reverbere",
    "éclat de bâche",
    "éclat de bache",
    "éclat de volet",
    "éclat de pavé",
    "éclat de pave",
    "éclat de zeste",
    "éclat de parapluie",
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
    "éclat de tapis",
    "éclat de crochet",
    "éclat de carotte",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de pli",
    "éclat de mie",
    "éclat de poisson",
    "éclat de page",
    "éclat d'escargot",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de wagon",
    "éclat de nappe",
    "éclat de farine",
    "éclat de laine",
    "éclat de bec",
    "éclat de marche",
    "éclat de fraise",
    "éclat de quille",
    "éclat de casserole",
    "éclat de tasse",
    "éclat de vitre",
    "éclat de train",
    "éclat de gâteau",
    "éclat de gateau",
    "gâteau",
    "gateau",
    "véranda",
    "veranda",
    "magasin",
)


PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de poussière",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_montrer_la_pomme_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="calme",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=on_dit_le_mot_une_seconde_fois; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="Pomme",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_voix_forte_echoue_le_mot_revient_plus_bas; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de poussière",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_sans_regarder_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de poussière",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pale; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "répéter",
    "accepted_examples": (
        "répéter | observer d'abord | observer | attendre"
    ),
    "retry_prompt": "On peut répéter. Que peut-on faire ?",
    "engine_ok_text": "Oui, répéter.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "chaises,rayon",
        [
            "narrateur|Un rayon coupe la classe, pâle et droit.",
            "narrateur|La poussière flotte, lente.",
            "narrateur|Dans le rayon, un éclat de poussière brille.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, dans l'air ?",
            "narrateur|Les chaises de bois font un petit bruit.",
            "enfant-f|Elles craquent.",
            "maman|C'est le bois des chaises.",
            "narrateur|Le foulard de maman pend au crochet.",
            "enfant-f|Il est bleu.",
            "maman|Il pend au crochet.",
            "papa|Tu restes près de nous, Victorina ?",
            "enfant-f|Oui, papa.",
            "narrateur|L'horloge fait tic, puis tac.",
            "enfant-f|Je l'entends.",
            "papa|Elle compte, sans se presser.",
            "narrateur|Le mur est frais, près du crochet.",
            "enfant-f|Il est frais, papa.",
            "papa|Oui, le mur de la classe.",
            "narrateur|Une table basse attend au milieu.",
            "narrateur|Des cartes y sont posées, faces ouvertes.",
            "enfant-f|La pomme rouge, maman !",
            "maman|Tu la vois, sur la table ?",
            "narrateur|Une carte montre une pomme, bien ronde.",
            "enfant-f|Elle est rouge.",
            "narrateur|À côté, un canard garde le bec fermé.",
            "narrateur|Un chat aux oreilles hautes attend aussi.",
            "enfant-f|Le chat me regarde.",
            "papa|Ils sont tous sur la table.",
            "narrateur|Victorina touche l'éclat de poussière.",
            "narrateur|L'air est tiède, un peu piquant.",
            "enfant-f|Ça chatouille le nez.",
            "enfant-f|Je la montre, maintenant !",
            "maman|Tu restes près de la table ?",
            "enfant-f|Oui, maman.",
            "papa|La classe est trop grande, pour crier.",
            "enfant-f|Je parle fort, alors.",
            "narrateur|En ce moment, Victorina se penche sur la table.",
            "enfant-f|Pomme, tu vas dans le rayon !",
            "narrateur|Sa voix part trop fort, trop vite.",
            "narrateur|Les chaises de bois reculent d'un coup.",
            "narrateur|Les cartes glissent sur la table.",
            "enfant-f|Oh.",
            "narrateur|La pomme disparaît sous le canard.",
            "narrateur|L'éclat n'est plus là.",
            "narrateur|Le sourire de Victorina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-f|Je la prends !",
            "maman|La pomme est sous les autres.",
            "papa|Tu la vois, Victorina ?",
            "narrateur|Les épaules de Victorina tombent un peu.",
            "narrateur|Ça serre, dans son ventre.",
            "narrateur|Papa se baisse à sa hauteur.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorina a besoin de calme.",
            "narrateur|Que peut-on faire ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "chaises,cartes",
        [
            "narrateur|Victorina avance trop vite vers la table.",
            "enfant-f|Pomme, maintenant !",
            "narrateur|Sa voix se mélange au bruit des chaises.",
            "enfant-f|Oh.",
            "narrateur|Les cartes restent en tas.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Victorina referme la main.",
            "narrateur|Elle regarde la table, un instant.",
            "papa|Tu veux venir près de la pomme ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Victorina pose un genou près de la table.",
            "narrateur|La table est lisse, un peu froide.",
            "enfant-f|Pomme.",
            "narrateur|Elle dit le mot plus bas.",
            "papa|Pomme.",
            "narrateur|Papa dit le mot, comme elle.",
            "enfant-f|Pomme.",
            "narrateur|Victorina dit le mot, une seconde fois.",
            "maman|Merci, Victorina.",
            "narrateur|Maman a entendu toute la phrase.",
            "narrateur|Le ventre de Victorina se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|Tu as les mains au chaud ?",
            "enfant-f|Un peu, papa.",
            "narrateur|L'horloge fait tic, puis tac.",
            "enfant-f|Elle va moins vite.",
            "papa|Tu l'entends, Victorina ?",
            "enfant-f|Oui.",
            "narrateur|Victorina écarte les cartes, sans les jeter.",
            "narrateur|La pomme revient, sur le papier.",
            "enfant-f|Elle est là.",
            "maman|Elle t'écoute.",
            "narrateur|Victorina pose un doigt près de la pomme.",
            "narrateur|Le papier est un peu froid.",
            "papa|Tu la montres dans le rayon ?",
            "enfant-f|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "chaises,rayon",
        [
            "narrateur|Victorina tire la carte trop vite.",
            "enfant-f|Tu vas dans le rayon, d'un coup !",
            "narrateur|La carte glisse sous une chaise de bois.",
            "enfant-f|Oh.",
            "narrateur|Victorina avance la main.",
            "narrateur|Puis elle s'arrête net.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Papa attend, sans parler.",
            "narrateur|Victorina observe la table, écoute la classe.",
            "narrateur|Dans le rayon, un éclat de poussière luit.",
            "enfant-f|Là, près du foulard.",
            "narrateur|Victorina tient la carte des deux mains.",
            "narrateur|Le papier est lisse, un peu froid.",
            "enfant-f|Elle est froide, papa.",
            "papa|Tu la portes jusqu'au rayon ?",
            "enfant-f|Oui, papa.",
            "maman|On avance ?",
            "enfant-f|Oui, maman.",
            "narrateur|Victorina pose la pomme dans le rayon pâle.",
            "narrateur|Le papier touche l'air tiède.",
            "narrateur|L'air tiède revient sur les joues.",
            "narrateur|Victorina serre la carte contre elle.",
            "enfant-f|Elle reste froide.",
            "papa|On marche.",
            "narrateur|La carte penche, puis se cale.",
            "enfant-f|Je la tiens.",
            "maman|On avance.",
            "narrateur|Victorina passe le long des chaises.",
            "narrateur|Le bois craque, un peu.",
            "enfant-f|Je la tiens bien.",
            "papa|On marche près du crochet.",
            "enfant-f|Le foulard est là.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "rayon",
        [
            "enfant-f|Le rayon brillait, papa.",
            "papa|Tu le vois, comme dans l'air ?",
            "enfant-f|Oui, un peu pâle.",
            "narrateur|Victorina pose la carte contre le foulard.",
            "maman|On la garde près de nous ?",
            "enfant-f|Oui, maman.",
            "enfant-f|La classe sentait le bois.",
            "maman|Elle est derrière nous.",
            "narrateur|Un rayon n'est plus aussi net.",
            "narrateur|Victorina respire, plus large.",
            "papa|On rentre ?",
            "enfant-f|Oui.",
            "narrateur|Les joues de Victorina se réchauffent.",
            "narrateur|La carte reste froide sous la main.",
            "enfant-f|On le voit, maman.",
            "maman|Tu le vois dans l'air ?",
            "enfant-f|Oui, l'éclat.",
            "narrateur|Un éclat de poussière reste pâle.",
        ],
    ),
}


def vet(lines: list[str]) -> list[str]:
    out: list[str] = []
    starts: list[str] = []
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
    out["pitch_xai_tag"] = m.get("pitchTag")
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
    for name in (
        "anaïs", "anais", "corentin", "chouchou", "louise", "zoé", "zoe",
        "iris", "raphaël", "raphael",
    ):
        if re.search(rf"\b{name}\b", blob):
            raise SystemExit(f"{SID}: {name} interdit")
    if "maitresse|" in blob or "maîtresse|" in blob:
        raise SystemExit(f"{SID}: maîtresse parle")
    if "copain|" in blob or "copine|" in blob:
        raise SystemExit(f"{SID}: copain/copine")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Victorina = enfant-f)")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f") for r in roles):
        raise SystemExit(f"{SID}: rôle hors papa/maman")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "besoin de calme",
        "observer d'abord",
        "répéter la règle",
        "on peut répéter",
        "le calme a aidé",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if "répéter" in body:
        raise SystemExit(f"{SID}: répéter dans le récit")
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
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Victorina a besoin de calme. Que peut-on faire ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "répéter":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt", "").lower()
    if "anaïs" in retry or "anais" in retry or "corentin" in retry:
        raise SystemExit(f"{SID}: mauvais prénom dans retry_prompt")
    if "répéter" not in retry:
        raise SystemExit(f"{SID}: retry sans répéter")
    for ban in (
        "éclat de carte", "éclat de bois", "éclat de cube", "éclat de boule",
        "éclat de galet", "éclat de couloir", "panier", "dorure", "poire",
        "cloche", "corbeille", "croissant", "réverbère", "reverbere",
        "bâche", "bache", "volet", "pavé", "pave", "zeste", "parapluie",
        "marché", "boulangerie", "véranda", "veranda", "magasin",
    ):
        if ban in blob:
            raise SystemExit(f"{SID}: BAN {ban}")
    if "tout doux" in blob:
        raise SystemExit(f"{SID}: tic tout doux")
    if BAN_WORDS.search(blob):
        raise SystemExit(f"{SID}: BAN_WORDS {BAN_WORDS.search(blob).group(0)}")

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
        "- **Leçon :** DIF.BES.001 — besoin de calme / répéter / observer "
        "d'abord (vécue : voix trop forte → cartes qui glissent, chaises "
        "qui reculent ; le mot revient plus bas, une seconde fois)\n"
        "- **Personnages :** Victorina, papa, maman. Dump Anaïs / Corentin "
        "→ INTERDIT. Chouchou retiré (un héros). Papa ajouté / conservé. "
        "Pas de maîtresse. Troupe D16.\n"
        "- **Lieu :** classe, rayon de soleil, poussière, chaises de bois, "
        "table basse, cartes (pomme, canard, chat), horloge, foulard au "
        "crochet. ≠ 001-01 Sarah (vitre floue, soleil de doigt, manteaux, "
        "bottes, tapis, tortue, éclat de carte). ≠ 001-05 Aniss (bulle, "
        "linge, savon, chemise, éclat de bois). ≠ poire / véranda.\n"
        "- **Indice unique :** éclat de poussière (brille à l'ouverture, "
        "touché, luit au refus, reste pâle). Pas éclat de carte / bois / "
        "cube / boule / galet / couloir.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un rayon coupe la classe. La poussière flotte. Dans le rayon, un "
        "éclat de poussière brille. Les chaises de bois craquent. Le "
        "foulard pend. L'horloge fait tic. Sur la table, une pomme rouge. "
        "Victorina veut la montrer dans le rayon **maintenant**. Première "
        "idée : crier trop fort, trop vite. Les chaises reculent, les "
        "cartes glissent. Sourire parti, épaules basses. Elle refuse de "
        "foncer. Elle observe, dit le mot plus bas. Papa dit le mot, "
        "comme elle. Merci vécu. Elle tire trop vite : la carte glisse "
        "sous une chaise. Elle s'arrête, lit l'éclat. Un éclat de "
        "poussière reste pâle.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : classe, rayon pâle, poussière, chaises de bois, "
        "foulard bleu, horloge, mur frais, table basse, cartes. ≠ 001-01 "
        "manteaux / bottes / vitre / tapis. ≠ 001-05 cour / linge / bulle.\n"
        "- Désir : montrer la pomme rouge dans le rayon, maintenant.\n"
        "- Objet : carte pomme, canard, chat, table, rayon.\n"
        "- Indice unique : éclat de poussière, vu dès l'ouverture, payé pâle.\n"
        "- Urgence douce : la voix trop grande pour la classe.\n"
        "- Imprévu 1 : crier trop vite ; chaises qui reculent, cartes qui "
        "glissent, l'éclat part.\n"
        "- Cue : papa à la même hauteur, près de la table. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : tirer d'un coup, carte sous une chaise.\n"
        "- Résolution : elle refuse de foncer, observe, dit le mot plus "
        "bas ; papa le dit comme elle.\n"
        "- Retour : pomme dans le rayon pâle, éclat de poussière pâle, "
        "foulard au crochet.\n\n"
        "## Vécu\n\n"
        "Victorina veut montrer la pomme **maintenant**. Impatience, puis "
        "sourire qui disparaît. Papa se baisse, pose une question, ne "
        "récite pas la règle. Victorina agit : main fermée, mot plus bas, "
        "seconde fois. Merci vécu après l'écoute. Fin : l'éclat du début "
        "reste pâle.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Victorina observe d'abord les cartes (noyau dump : "
        "cartes / classe / rayon / poussière / chaises). Anaïs / Corentin "
        "→ INTERDIT. Chouchou retiré. Relance sans Anaïs.\n"
        "- Lieu du dump (classe, rayon, poussière, chaises de bois). "
        "≠ 001-01 cartes Sarah / éclat de carte. ≠ 001-05 carte Aniss / "
        "éclat de bois. ≠ poire du magasin / véranda.\n"
        "- Ouverture inventée (rayon pâle, poussière lente), pas un "
        "gabarit v2, pas « Victorina est en classe ».\n"
        "- Indice unique : éclat de poussière. Pas carte, bois, cube, "
        "boule, galet, couloir comme éclat. Pas panier, dorure, poire, "
        "sac, cloche, corbeille, croissant, réverbère, bâche, volet, "
        "pavé, zeste, parapluie. Pas COL.ECO.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » du dump.\n"
        "- Leçon non dite : on l'entend quand le mot revient plus bas. "
        "Pas de morale, pas « tu as su répéter », pas « observer d'abord ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Victorina a besoin de calme. Que peut-on "
        "faire ? » expected répéter. retry sans Anaïs. 5 chunks, kinds "
        "inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Confirm plus vif vers la table. voice() calqué COL.POL.001-04.\n"
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
