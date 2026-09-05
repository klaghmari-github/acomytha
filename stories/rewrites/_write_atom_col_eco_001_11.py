#!/usr/bin/env python3
"""ATOM-COL.ECO.001-11 — Le crayon de Sarah (F-NAR-019, N1, COL.ECO.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.001-11"
TITLE = "Le crayon de Sarah"
N1 = LIMITS["N1"]
INDICE = "éclat de crochet"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
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
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "sylvain",
    "loïc",
    "loic",
    "oiseau",
    "salière",
    "saliere",
    "on aime écouter",
    "on aime ecouter",
    "si tu as un malaise",
    "tu as bien fait",
    "tu as bien écouté",
    "tu as bien ecoute",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
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
    "grain de miette",
    "grain de foin",
    "grain de paille",
    "grain de toile",
    "grain de pépin",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de crayon",
    "éclat de tapis",
    "éclat de bec",
    "éclat de marche",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de casserole",
    "éclat de wagon",
    "éclat de citron",
    "éclat de lampe",
    "éclat de nappe",
    "éclat de farine",
    "éclat de ombre",
    "éclat d'ombre",
    "éclat de écorce",
    "éclat d'écorce",
    "éclat de laine",
    "éclat de carreau",
    "éclat de grain",
    "éclat de pince",
    "éclat de corde",
    "éclat de caisse",
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
    "trait de craie",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de crochet",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_dessiner_le_malaise_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="malaise",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_raconte_au_gouter; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="goûter",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_puis_raconte; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de crochet",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; "
            "emotion=fierté_calme; intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_l_eclat_tient; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de crochet",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_tient_sur_le_metal; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "elle raconte",
    "accepted_examples": (
        "elle raconte | raconter | au goûter | au gouter | à papa | "
        "à la maison | elle attend | elle dit | papa | malaise"
    ),
    "retry_prompt": "Sarah a un malaise. Elle raconte au goûter. Que fait-elle ?",
    "engine_ok_text": "Oui, elle raconte.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "vestiaire,manteau",
        [
            "narrateur|Le vestiaire sent le pain du goûter.",
            "narrateur|Les crochets portent des prénoms.",
            "narrateur|Le prénom de Sarah est écrit.",
            "narrateur|Un manteau rouge attend dans les bras.",
            "narrateur|Les manches sont un peu froides.",
            "narrateur|Maman lève le manteau vers le crochet.",
            "narrateur|Le métal des crochets luit.",
            "narrateur|Sur le métal, un éclat de crochet tremble.",
            "enfant-f|Il est petit, papa.",
            "papa|C'est la lumière, sur le crochet.",
            "narrateur|Papa accroche le manteau rouge.",
            "narrateur|Le crochet tient le tissu.",
            "narrateur|L'éclat de crochet brille, sous le manteau.",
            "maman|Tes lacets sont faits, Sarah ?",
            "enfant-f|Oui, maman.",
            "narrateur|Maman noue un lacet, puis l'autre.",
            "narrateur|Les chaussures font un petit clac.",
            "papa|Tu as senti le pain ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Il sent le goûter.",
            "narrateur|Sarah tient un crayon vert.",
            "narrateur|Le bois est un peu râpeux.",
            "enfant-f|Je veux dessiner, maintenant !",
            "maman|Une maison, au coin tapis ?",
            "enfant-f|Oui, avec le crayon !",
            "papa|À tout à l'heure, Sarah.",
            "enfant-f|À tout à l'heure, papa.",
            "narrateur|En ce moment, Sarah s'assoit.",
            "narrateur|Le coin tapis est tiède.",
            "narrateur|Un rayon fait un carré d'or.",
            "narrateur|Les cubes attendent dans leur bac.",
            "narrateur|La maîtresse parle près des chaises.",
            "maitresse|Bonjour les enfants.",
            "enfant-f|Bonjour, maîtresse.",
            "narrateur|Sarah veut le crayon, tout de suite.",
            "narrateur|Elle ouvre la boîte trop vite.",
            "narrateur|Le crayon roule sous un cube.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Elle reste près du groupe.",
            "narrateur|Elle reprend le crayon, sans presser.",
            "narrateur|Le bois est râpeux, un peu chaud.",
            "enfant-f|Je dessine la maison.",
            "narrateur|Le vert sent le bois.",
            "narrateur|La maison tient sur la feuille.",
            "narrateur|Plus tard, une voix parle trop près.",
            "narrateur|Sarah sent un malaise.",
            "narrateur|Son ventre se serre, tout petit.",
            "narrateur|Elle serre le crayon, puis le pose.",
            "enfant-f|Je le dirai à la maison.",
            "narrateur|Le soir, le vestiaire est vide.",
            "narrateur|Le manteau rouge revient.",
            "narrateur|Papa coupe du pain.",
            "narrateur|Ça sent le four.",
            "papa|Te voilà.",
            "papa|Tu as faim, Sarah ?",
            "narrateur|Sarah veut le dire, tout de suite.",
            "enfant-f|Papa, à l'école !",
            "narrateur|Papa parle à maman, près du pain.",
            "narrateur|Les mots de Sarah se cognent aux leurs.",
            "narrateur|Personne ne tourne la tête.",
            "papa|Tu disais quelque chose, Sarah ?",
            "enfant-f|Mon ventre s'est serré.",
            "narrateur|Le sourire part, d'un coup.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-f|Ça ne sort pas, maman.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à sa hauteur.",
            "papa|Tu veux du pain ?",
            "narrateur|Sarah ouvre la bouche.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Sarah a un malaise.",
            "narrateur|Que fait-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "pain,verre",
        [
            "narrateur|Sarah ouvre la bouche trop vite.",
            "enfant-f|Papa, à l'école, quelqu'un parlait !",
            "narrateur|Papa n'a pas fini sa phrase.",
            "papa|Le pain, sur la planche, Sarah.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Elle pose les mains à plat.",
            "narrateur|Elle écoute la maison, un instant.",
            "maman|Le goûter est près de la fenêtre.",
            "narrateur|Papa pose un verre d'eau.",
            "narrateur|Maman pose le pain.",
            "narrateur|Sarah attend que le silence arrive.",
            "narrateur|Sur le crochet, l'éclat de crochet brille.",
            "enfant-f|Je peux te dire quelque chose ?",
            "maman|Oui, nous t'écoutons.",
            "enfant-f|À l'école, quelqu'un a parlé trop près.",
            "enfant-f|Mon ventre s'est serré.",
            "papa|Merci, Sarah.",
            "narrateur|Papa a entendu toute la phrase.",
            "maman|Tu as soif ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le ventre de Sarah se desserre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "resolution",
        "pain,crayon",
        [
            "narrateur|Sarah range son crayon près de la porte.",
            "papa|On s'assoit près de la fenêtre ?",
            "enfant-f|Oui.",
            "narrateur|On voit le manteau rouge.",
            "narrateur|Le pain est tiède, un peu doré.",
            "enfant-f|Il sent le goûter, maman.",
            "maman|Tes pieds sont sous la table ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sarah veut raconter l'école, d'un coup.",
            "narrateur|Elle saisit le crayon trop vite.",
            "narrateur|Le crayon roule vers le pain.",
            "enfant-f|Oh.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Attends.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Elle reprend le crayon, sans presser.",
            "enfant-f|Le coin tapis était tiède.",
            "enfant-f|J'ai dessiné la maison.",
            "papa|Avec le crayon vert ?",
            "enfant-f|Oui, et l'éclat était là.",
            "narrateur|Sarah croque le pain.",
            "narrateur|Une miette reste sur le doigt.",
            "maman|Il est bon ?",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "manteau,crochet",
        [
            "enfant-f|Le manteau rouge est rentré.",
            "maman|Il pend, près de la porte.",
            "narrateur|Le crochet de la maison garde un peu de lumière.",
            "enfant-f|Comme à l'école, papa !",
            "papa|Tu le vois, toi ?",
            "enfant-f|Oui, sur le métal.",
            "narrateur|Le pain du goûter attend sur la planche.",
            "enfant-f|On est bien, ici.",
            "maman|Le crayon est rangé ?",
            "enfant-f|Près de la porte, maman.",
            "narrateur|Sarah pose la miette dans la coupelle.",
            "narrateur|L'éclat de crochet tient sur le métal.",
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
        by[cid] = voice(c, lines, profile, sons, extra_kw)
        if c.get("kind") != by[cid].get("kind"):
            raise SystemExit(f"{cid}: kind changé")
    merged = dict(src)
    merged["fil_rouge"] = (
        "Le vestiaire sent le pain du goûter. Sur le métal, un éclat de "
        "crochet tremble. Sarah veut dessiner, maintenant. Le crayon "
        "roule. À l'école, une voix trop près : malaise. Elle veut le "
        "dire tout de suite : les mots se cognent. Elle refuse de foncer, "
        "raconte au goûter. Merci vécu. Sur le métal, l'éclat tient."
    )
    merged["title"] = TITLE
    merged["characters"] = "Sarah, papa, maman"
    merged["setting"] = "école, coin tapis, vestiaire, puis maison"
    merged["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    nwords = sum(words(c["text"]) for c in merged["chunks"])
    tts_ok = all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_xai_tags"] != c["text"]
        and c["text_ssml"].startswith("<speak>")
        for c in merged["chunks"]
    )
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    joined = " ".join(c["text"] for c in merged["chunks"])
    blob = joined.lower()
    if INDICE not in by["CHK_T0000_P0000"]["text"]:
        raise SystemExit("indice éclat de crochet absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"]:
        raise SystemExit("indice éclat de crochet non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if blob.count("en ce moment") != 1:
        raise SystemExit("en ce moment doit apparaître une fois")
    adults = " ".join(
        ln.split("|", 1)[1]
        for c in merged["chunks"]
        for ln in c["script"].splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
    ).lower()
    if adults.count("merci") != 1:
        raise SystemExit(f"merci ×{adults.count('merci')}")
    if "bravo" in adults:
        raise SystemExit("bravo en trop")
    if "sylvain" in blob:
        raise SystemExit("Sylvain interdit")
    if "éclat de crayon" in blob:
        raise SystemExit("éclat de crayon interdit (001-01)")
    if "crayon" not in blob:
        raise SystemExit("crayon (objet du monde) absent")
    if "coin tapis" not in blob:
        raise SystemExit("coin tapis (monde dump) absent")
    if "refuse de foncer" not in blob:
        raise SystemExit("manque refuse de foncer")
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "## Promesse narrative\n\n"
        "Le vestiaire sent le pain du goûter. Les crochets portent des "
        "prénoms. Un manteau rouge attend. Sur le métal, un éclat de "
        "crochet tremble. Sarah veut dessiner, maintenant, avec le crayon "
        "vert. Première idée : ouvrir la boîte trop vite. Le crayon roule. "
        "Sourire parti. Elle reprend, sans presser, dessine la maison. Une "
        "voix parle trop près : malaise, ventre serré. Elle veut le dire "
        "tout de suite. Les mots se cognent au pain. Papa s'accroupit. "
        "Elle ouvre trop vite : les voix se mélangent. Elle refuse de "
        "foncer, attend le goûter, raconte. Merci vécu. Elle veut "
        "raconter l'école d'un coup, saisit le crayon trop vite : il "
        "roule. Elle reprend. Sur le métal, l'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : vestiaire, crochets à prénoms, manteau rouge, pain du "
        "goûter, coin tapis, puis maison. ≠ gouttière/crayon (001-01), ≠ "
        "buée, ≠ croûte, ≠ tableau, ≠ casier, ≠ moufle, ≠ craie, ≠ "
        "cartable, ≠ pinceau, ≠ casserole.\n"
        "- Désir : dessiner avec le crayon, puis dire le malaise, maintenant.\n"
        "- Objet : crayon vert, manteau rouge, pain du goûter.\n"
        "- Indice unique : éclat de crochet, vu dès l'ouverture, payé au "
        "climax (crochet de la maison pendant le silence) et sur le métal "
        "au retour.\n"
        "- Urgence douce : la voix trop près, le ventre qui serre.\n"
        "- Imprévu 1 : tout de suite, elle coupe papa ; les mots se perdent.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après la phrase "
        "entière au goûter.\n"
        "- Imprévu 2 (plus rusé) : elle veut raconter l'école d'un coup ; "
        "le crayon roule vers le pain.\n"
        "- Résolution : elle refuse de foncer, attend le silence, dit "
        "l'école, reprend le crayon.\n"
        "- Retour : manteau au crochet, pain du goûter, l'éclat tient sur "
        "le métal.\n\n"
        "## Vécu\n\n"
        "Leçon COL.ECO.001 (dire le malaise à la maison, au bon moment) "
        "greffée, jamais annoncée. La première idée (tout dire d'un coup) "
        "échoue. Le choix de Sarah change l'action. Un « en ce moment ». "
        "Un merci vécu. Adulte + question. Troupe D16 : Sarah, papa, maman. "
        "Maîtresse : salut de classe, pas de leçon récitée. N1.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé : Le crayon de Sarah. Crayon = objet du "
        "monde, pas l'indice. Lieu : vestiaire, coin tapis, maison. Monde "
        "du dump, ≠ ECO-001-01 Aniss.\n"
        "- Héros Sarah. Sylvain retiré du dump TTS.\n"
        "- Ouverture inventée (le vestiaire sent le pain du goûter), pas "
        "un gabarit v2.\n"
        "- Indice unique : éclat de crochet. Pas crayon/tapis/buée/croûte/"
        "tableau/casier/moufle/craie/cartable/pinceau/casserole, pas "
        "bec/marche/fraise/quille/promenade/gouttière/wagon/citron/lampe/"
        "nappe/farine/ombre/écorce/laine/carreau/grain/pince/corde/caisse.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés.\n"
        "- Interdit « bon travail / histoire finie / j'ai écouté ».\n"
        "- Question moteur inchangée (Sarah a un malaise. Que fait-elle ?). "
        "Retry Sylvain → Sarah. 5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N1 ≤ 10. TTS : notes, ssml, xai, piper par "
        "chunk.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
