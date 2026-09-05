#!/usr/bin/env python3
"""ATOM-AUT.AFF.002-02 — Les pommes de Chouchou (F-NAR-019, N3, AUT.AFF.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.002-02"
TITLE = "Les pommes de Chouchou"
LIM = LIMITS["N3"]
CHARS = "Chouchou, maman"
SETTING = "entrée, marché, cuisine"
FIL = (
    "Une pièce tinte. Le panier d'osier tape une botte. Un éclat de liste "
    "brille au bord du papier. Chouchou veut quatre pommes pour le saladier, "
    "maintenant. Elle tire : la capuche du manteau bleu pince l'anse. "
    "Elle pose le panier, enfile le manteau. Au marché, la pomme jaune roule ; "
    "sa manche bouscule une caisse. Elle refuse de foncer, retrouve l'éclat, "
    "pose la quatrième. Le manteau clic au crochet. L'éclat brille près du blanc."
)
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
    "maîtresse",
    "maitresse",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "grain de miette",
    "grain de paille",
    "grain de toile",
    "grain de pépin",
    "grain de laine",
    "grain de feuille",
    "grain de pin",
    "éclat de pince",
    "éclat de corde",
    "éclat de caisse",
    "éclat de caillou",
    "éclat de clé",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "trait de vitre",
    "trait de craie",
    "ombre en forme",
    "minuscule symbole",
    "marque fine",
    "tache de couleur",
    "kenzo",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de liste",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_les_pommes_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="crochet",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=près_du_crochet_avant_de_sortir; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="manteau",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; sous_texte=le_manteau_puis_le_panier; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de liste",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=deux_envies_qui_se_heurtent; intensite=2; "
            "destinataire=enfant; sous_texte=elle_refuse_de_foncer_retrouve_l_éclat; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de liste",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_éclat_du_bord_brille_près_du_saladier; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "le manteau",
    "accepted_examples": "le manteau | manteau | son manteau",
    "retry_prompt": "Elle prend le manteau. Que prend Chouchou ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "clochette,porte",
        [
            "narrateur|Une pièce tinte, dans une poche.",
            "narrateur|C'est la poche de maman.",
            "narrateur|Le panier d'osier tape une botte grise.",
            "narrateur|Chouchou connaît cette entrée.",
            "narrateur|Elle connaît les bottes, le crochet, la porte.",
            "narrateur|Pourtant, un détail paraît nouveau.",
            "narrateur|Un éclat de liste brille au bord du papier.",
            "narrateur|Le papier froissé dépasse du panier.",
            "narrateur|Un quatre est écrit, minuscule.",
            "narrateur|De la rue, une clochette de vélo passe.",
            "narrateur|L'air sent la pierre, humide.",
            "narrateur|Dans la cuisine, le saladier blanc attend.",
            "maman|Chouchou, tu as vu le panier ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Il est près des bottes.",
            "enfant-f|Je veux les pommes, maintenant !",
            "maman|Quatre, pour le saladier.",
            "narrateur|En ce moment, Chouchou saisit le panier.",
            "narrateur|Son manteau bleu pend au crochet.",
            "narrateur|Le tissu a une petite capuche.",
            "narrateur|La capuche glisse sous l'anse.",
            "narrateur|Le panier refuse de venir.",
            "enfant-f|Il tient, maman !",
            "narrateur|Elle tire plus fort, d'un coup.",
            "narrateur|L'anse pince la capuche bleue.",
            "narrateur|Rien ne bouge.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Maman s'accroupit à la même hauteur.",
            "maman|Tu veux tirer, ou regarder ?",
            "enfant-f|Je veux les pommes.",
            "narrateur|Chouchou tire une dernière fois.",
            "narrateur|Le panier reste coincé.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Avant de sortir, Chouchou s'arrête près du crochet.",
            "maman|Que prend-elle, pour le marché ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "manteau,porte",
        [
            "enfant-f|J'arrête de tirer.",
            "narrateur|Elle pose le panier près des bottes.",
            "narrateur|L'éclat de liste reste au bord.",
            "enfant-f|Le manteau, d'abord.",
            "narrateur|Elle prend le manteau bleu.",
            "narrateur|Elle glisse un bras, puis l'autre.",
            "narrateur|La capuche tapote son dos.",
            "maman|Tu as les boutons ?",
            "enfant-f|Un, deux, trois.",
            "maman|Ils tiennent bien.",
            "narrateur|Un bouton reste un peu de travers.",
            "enfant-f|Je le remets.",
            "narrateur|Elle pousse le bouton dans sa fente.",
            "narrateur|Chouchou reprend le panier d'osier.",
            "enfant-f|On va chercher les pommes ?",
            "maman|Oui, quatre, pour le saladier.",
            "narrateur|Maman ouvre la porte.",
            "narrateur|Le vent est frais, sur les joues.",
            "narrateur|Il sent un peu le pain.",
            "narrateur|Ils marchent vers le marché.",
            "narrateur|Chouchou tient une anse du panier.",
            "maman|Tu as chaud, dans le manteau ?",
            "enfant-f|Oui.",
            "enfant-f|J'ai chaud dedans.",
            "narrateur|Le tissu bleu tape contre sa hanche.",
            "narrateur|Le papier froissé fait un petit bruit.",
            "narrateur|Les pavés luisent, un peu humides.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "marche,pomme",
        [
            "narrateur|Au marché, les étals sont colorés.",
            "narrateur|Les pommes brillent sous le vent.",
            "narrateur|Une pomme est rouge.",
            "narrateur|Une autre est jaune, bien ronde.",
            "maman|On en prend quatre ?",
            "enfant-f|Quatre pommes, maintenant !",
            "narrateur|Maman pose trois pommes dans le panier.",
            "narrateur|La quatrième, jaune, roule.",
            "narrateur|Elle part vers le bord de l'étal.",
            "enfant-f|Elle part !",
            "narrateur|Chouchou veut courir d'un coup.",
            "narrateur|Sa manche bleue bouscule une caisse.",
            "narrateur|La caisse penche, un peu.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Elle s'arrête net.",
            "enfant-f|Pas maintenant.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Elle lève les yeux vers le panier.",
            "narrateur|L'éclat de liste est là.",
            "narrateur|Celui du bord, dans l'entrée.",
            "enfant-f|Quatre, comme sur le papier.",
            "maman|Tu veux la pomme jaune ?",
            "enfant-f|Celle qui brille.",
            "narrateur|Elle avance la main, sans se presser.",
            "narrateur|La pomme est lisse et froide.",
            "narrateur|Elle la pose dans le panier.",
            "enfant-f|Je l'ai.",
            "maman|Merci d'avoir regardé, Chouchou.",
            "narrateur|Le panier devient un peu lourd.",
            "narrateur|Chouchou sent le sucré des fruits.",
            "maman|C'est l'heure de rentrer ?",
            "enfant-f|Oui, on rentre.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "crochet,porte",
        [
            "narrateur|Ils rentrent.",
            "narrateur|L'entrée sent la pierre, froide.",
            "narrateur|Chouchou retire le manteau bleu.",
            "narrateur|Elle le raccroche au crochet.",
            "narrateur|Le crochet fait un petit clic.",
            "narrateur|Le manteau est à sa place.",
            "narrateur|Elle pose le panier près des bottes.",
            "narrateur|Les pommes tapotent le fond.",
            "maman|Tu as fini de poser le panier ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Les pommes sont dedans.",
            "narrateur|Maman pose les pommes sur la table.",
            "narrateur|Elles roulent un tout petit peu.",
            "enfant-f|Elles sentent le marché.",
            "maman|Tu veux les mettre dans le saladier ?",
            "narrateur|Chouchou les pose une par une.",
            "narrateur|Le saladier devient coloré.",
            "narrateur|L'éclat de liste brille près du blanc.",
            "enfant-f|Il est venu avec nous.",
            "maman|Tu l'as vu, toi ?",
            "enfant-f|Il m'a montré les quatre.",
            "narrateur|Le manteau bleu attend au crochet.",
            "narrateur|Le saladier garde les quatre pommes.",
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
        if n > LIM:
            raise SystemExit(f"{n}>{LIM}: {ph}")
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
    if emp and emp in text:
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
        extra: dict = {}
        if cid == "CHK_T0000_P0000_Q0001":
            extra["pause_before_ms"] = 200
            extra["fields"] = Q_FIELDS
        elif cid in {"CHK_T0000_P0000_C0001", "CHK_T0000_P0000_END", "CHK_T0000_P0000_END_F0001"}:
            extra["pause_before_ms"] = 200
        by[cid] = voice(c, lines, profile, sons, extra)
    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)
    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "éclat de liste" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de liste" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé au climax")
    if "éclat de liste" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    if blob.count("éclat de liste") < 3:
        raise SystemExit("indice éclat de liste trop rare")
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
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une pièce tinte dans la poche de maman. Le panier d'osier tape une "
        "botte. Chouchou connaît l'entrée ; un éclat de liste paraît nouveau "
        "au bord du papier. Elle veut quatre pommes pour le saladier, "
        "**maintenant**. Elle tire : la capuche du manteau bleu pince l'anse. "
        "Première idée ratée. Elle pose le panier, enfile le manteau, boutonne. "
        "Au marché, la pomme jaune roule ; sa manche bouscule une caisse. "
        "Elle refuse de foncer, retrouve l'éclat, pose la quatrième. Retour : "
        "clic au crochet, saladier coloré, l'éclat brille près du blanc.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : entrée (bottes, crochet, panier, liste), marché, cuisine.\n"
        "- Désir : quatre pommes pour le saladier, maintenant.\n"
        "- Objet : panier d'osier, manteau bleu à capuche, liste froissée.\n"
        "- Indice unique : éclat de liste, vu dès l'ouverture, payé au marché "
        "et près du saladier.\n"
        "- Imprévu 1 : capuche coincée, tir trop fort, panier coincé.\n"
        "- Cue : maman à la même hauteur, « tirer ou regarder ? ». "
        "Chouchou choisit le manteau. Merci vécu après la pomme regardée.\n"
        "- Imprévu 2 (plus rusé) : pomme qui roule, manche qui bouscule "
        "une caisse ; elle refuse de foncer.\n"
        "- Résolution : l'éclat du début montre les quatre ; elle avance "
        "sans se presser.\n"
        "- Retour : manteau au crochet, quatre pommes dans le saladier, "
        "éclat près du blanc.\n\n"
        "## Vécu\n\n"
        "Leçon AUT.AFF.002 (prendre le manteau) greffée, jamais dite. "
        "Impatience, épaules qui tombent, fierté calme. Un « en ce moment ». "
        "Un merci vécu. Adulte + question. Troupe D16 : Chouchou, maman.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : entrée, marché, cuisine. "
        "≠ feuille rouge, ≠ trait de vitre, ≠ Victorino.\n"
        "- Ouverture inventée (pièce qui tinte, panier qui tape), pas le salon.\n"
        "- Indice unique : éclat de liste. Pas liste bannie "
        "(ombre-flèche / tache / symbole / marque fine / grain / trait de vitre).\n"
        "- Tics « encore / déjà / tout doux / tout calme » absents.\n"
        "- Leçon non dite. Pas de morale. Pas Kenzo.\n"
        "- Merci vécu. Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle plus tendu.\n"
        f"- N3 ≤ {LIM}. `check()` OK. Pas apply.\n\n"
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
