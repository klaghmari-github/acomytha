#!/usr/bin/env python3
"""ATOM-AUT.ROU.001-04 — Les fraises de Sarah (F-NAR-019, N3, AUT.ROU.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.ROU.001-04"
TITLE = "Les fraises de Sarah"
N3 = LIMITS["N3"]
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
    "grain de miette",
    "grain de foin",
    "grain de paille",
    "grain de toile",
    "grain de pépin",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "éclat de corde",
    "éclat de wagon",
    "éclat de bec",
    "éclat de marche",
    "trait de craie",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de fraise",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_les_fraises_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="fraises",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=une_chose_puis_la_suivante; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="cabas",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=t_shirt_puis_table_puis_cabas; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de fraise",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; "
            "emotion=fierté_calme; intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_l_éclat_montre_la_gourde; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de fraise",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_éclat_porte_une_goutte_de_jus; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "une chose",
    "accepted_examples": (
        "une chose | puis l'autre | d'abord | doucement | "
        "une chose puis l'autre | puis la suivante"
    ),
    "retry_prompt": "Elle fait une chose, puis la suivante. Comment se prépare Sarah ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "rideau,charrette",
        [
            "narrateur|La fenêtre respire, et le rideau bleu gonfle.",
            "narrateur|Un anneau frotte la tringle, sec.",
            "narrateur|Un carré de soleil glisse sur le plancher.",
            "narrateur|Dehors, une charrette racle le pavé.",
            "narrateur|L'odeur des fruits grimpe l'escalier.",
            "narrateur|Près de la porte, le cabas rayé attend.",
            "narrateur|Sur l'anse, un éclat de fraise brille.",
            "narrateur|C'est une graine rose, sèche, coincée dans le tissage.",
            "narrateur|Sarah la touche du doigt, puis la laisse.",
            "papa|Sarah, tu entends la charrette ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Ce sont les fraises !",
            "maman|Le marché s'installe, dans la rue.",
            "narrateur|En ce moment, Sarah saute du lit.",
            "enfant-f|On y va, maintenant !",
            "narrateur|Elle attrape le cabas vide, d'un coup.",
            "narrateur|Le tissu plat claque contre ses genoux.",
            "narrateur|Ses pieds nus cherchent le parquet.",
            "narrateur|Le bois est frais, lisse.",
            "narrateur|Elle pousse vers la porte.",
            "narrateur|L'anse glisse entre ses doigts.",
            "narrateur|Le cabas tombe à plat.",
            "enfant-f|Il part !",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Une chose, puis la suivante.",
            "narrateur|Sarah repose le cabas.",
            "narrateur|Le tissu rayé tombe contre le mur.",
            "enfant-f|J'ai trop faim pour attendre.",
            "maman|Alors on déjeune ici, d'abord.",
            "papa|On se lève ?",
            "enfant-f|Oui.",
            "narrateur|Sarah pousse le drap.",
            "narrateur|Ses orteils trouvent le parquet.",
            "maman|Le t-shirt blanc, sur la commode.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Sarah veut les fraises.",
            "narrateur|Comment se prépare-t-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "tissu,bol",
        [
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Le t-shirt, d'abord.",
            "narrateur|Sarah prend le coton sur la commode.",
            "narrateur|Le t-shirt est tiède, un peu froissé.",
            "narrateur|Elle l'enfile sans se presser.",
            "enfant-f|Je suis habillée.",
            "maman|La cuisine, maintenant.",
            "narrateur|Sarah marche vers la table.",
            "narrateur|La nappe à carreaux sent le pain.",
            "narrateur|Deux bols blancs attendent.",
            "maman|Tu veux du yaourt ?",
            "enfant-f|Oui, un peu.",
            "narrateur|Sarah s'assoit.",
            "narrateur|Elle pose les pieds par terre.",
            "narrateur|Le yaourt est froid sur la cuillère.",
            "papa|Tu as faim pour le marché ?",
            "enfant-f|Un peu, oui.",
            "maman|Alors les fraises, après.",
            "narrateur|Dehors, une caisse racle le pavé.",
            "enfant-f|Je les entends.",
            "papa|Ensuite, le cabas.",
            "narrateur|Le cabas rayé attend près du mur.",
            "narrateur|Sarah le soulève.",
            "narrateur|Le tissu tombe droit.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "resolution",
        "porte,rue",
        [
            "narrateur|Sarah met ses chaussures.",
            "papa|On prend le cabas ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa ouvre la porte.",
            "narrateur|Un souffle pousse le rideau bleu.",
            "narrateur|Le cabas se balance, vide au fond.",
            "enfant-f|Les fraises !",
            "narrateur|Sarah veut courir, l'anse à la main.",
            "narrateur|Elle veut descendre, sans regarder.",
            "narrateur|Sarah refuse de foncer.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Sur l'anse, l'éclat de fraise tremble.",
            "narrateur|La graine penche vers le fond du cabas.",
            "enfant-f|Il manque la gourde !",
            "maman|Elle est où, la gourde ?",
            "enfant-f|Dans la cuisine, au frais.",
            "narrateur|Sarah revient vers la table.",
            "narrateur|Elle glisse la gourde froide au fond.",
            "narrateur|L'éclat de fraise tient, coincé.",
            "papa|Merci, Sarah.",
            "papa|On y va ?",
            "enfant-f|Oui, le cabas est prêt.",
            "narrateur|Sarah donne la main.",
            "narrateur|La rue sent les fruits.",
            "narrateur|Un panier passe, plein.",
            "enfant-f|Les voilà !",
            "maman|Au coin des barquettes.",
            "narrateur|Sarah choisit une barquette rouge.",
            "narrateur|Une fraise est chaude sous le soleil.",
            "papa|Tu la goûtes ?",
            "enfant-f|Elle est sucrée.",
            "narrateur|Un peu de jus rouge reste sur le doigt.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "fruits",
        [
            "enfant-f|J'ai du rouge sur le doigt.",
            "maman|C'est le marché.",
            "narrateur|Sur l'anse, l'éclat de fraise porte une goutte.",
            "narrateur|La graine rose est collante, un peu chaude.",
            "enfant-f|Elle a voyagé.",
            "papa|Comme toi.",
            "narrateur|Le rideau bleu danse à la fenêtre.",
            "narrateur|Le jus sucré reste chaud sur son doigt.",
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
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
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
        extra: dict = {}
        if cid == "CHK_T0000_P0000_Q0001":
            extra["pause_before_ms"] = 200
            extra["fields"] = Q_FIELDS
        by[cid] = voice(c, lines, profile, sons, extra)
    merged = dict(src)
    merged["fil_rouge"] = (
        "La fenêtre respire, le rideau bleu gonfle. Sur l'anse du cabas "
        "rayé, un éclat de fraise — graine rose sèche — brille. Sarah veut "
        "les fraises du marché, maintenant. Elle saisit le cabas vide, "
        "pieds nus : l'anse glisse, le cabas tombe. Papa s'accroupit. Une "
        "chose, puis la suivante. À la porte, elle refuse de foncer. "
        "L'éclat penche vers le fond vide : la gourde manque. Elle la "
        "glisse. Au coin des barquettes, l'éclat porte une goutte de jus."
    )
    merged["title"] = TITLE
    merged["characters"] = "Sarah, papa, maman"
    merged["setting"] = "chambre au rideau bleu, cuisine, rue du marché le matin"
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
    if "éclat de fraise" not in joined:
        raise SystemExit("indice éclat de fraise absent")
    if joined.lower().count("en ce moment") != 1:
        raise SystemExit("en ce moment doit apparaître une fois")
    if joined.lower().count("merci") != 1:
        raise SystemExit("merci doit apparaître une fois")
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "## Promesse narrative\n\n"
        "La fenêtre respire, le rideau bleu gonfle. Sur l'anse du cabas "
        "rayé, un éclat de fraise — une graine rose sèche coincée dans le "
        "tissage — brille. Sarah veut les fraises du marché, maintenant. "
        "Elle saisit le cabas vide, pieds nus : l'anse glisse, le cabas "
        "tombe. Papa s'accroupit. Une chose, puis la suivante. À la porte, "
        "un souffle pousse le rideau, le cabas se balance vide. Sarah "
        "refuse de foncer. L'éclat penche vers le fond : la gourde manque. "
        "Elle la glisse. Au coin des barquettes, l'éclat porte une goutte "
        "de jus.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chambre au rideau bleu, charrette dans la rue, cuisine "
        "à la nappe à carreaux, coin des barquettes. ≠ allée/train, "
        "≠ oiseau/jardin, ≠ pain/escalier.\n"
        "- Désir : aller aux fraises du marché, maintenant.\n"
        "- Objet : cabas rayé, gourde froide, barquette rouge.\n"
        "- Indice unique : éclat de fraise, vu dès l'ouverture, payé au "
        "climax (fond vide) et sur l'anse au retour.\n"
        "- Urgence douce : la charrette racle, les fraises s'installent.\n"
        "- Imprévu 1 : tout d'un coup, cabas vide, pieds nus, anse qui "
        "glisse.\n"
        "- Cue : papa à la même hauteur, une chose puis la suivante. "
        "Un merci vécu, après la gourde glissée.\n"
        "- Imprévu 2 (plus rusé) : à la porte, elle veut descendre sans "
        "regarder ; le cabas se balance, vide au fond.\n"
        "- Résolution : elle refuse de foncer, lit l'éclat, revient "
        "chercher la gourde, donne la main.\n"
        "- Retour : jus rouge sur le doigt, l'éclat porte une goutte, "
        "le rideau bleu danse.\n\n"
        "## Vécu\n\n"
        "Leçon AUT.ROU.001 (une chose, puis la suivante) greffée, jamais "
        "annoncée. La première idée (partir d'un coup) échoue. Le choix "
        "de Sarah change l'action. Un « en ce moment ». Un merci vécu. "
        "Adulte + question. Troupe D16 : Sarah, papa, maman. N3.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu : maison puis rue du marché, le "
        "matin. Monde du dump, ≠ ROU-001-01..003.\n"
        "- Ouverture inventée (la fenêtre respire), pas un gabarit v2.\n"
        "- Indice unique : éclat de fraise. Pas grain de miette/foin/"
        "paille/toile/pépin, pas éclat de pince/thermos/coquille/bouton/"
        "ticket/goutte/boucle/corde/wagon/bec/marche, pas trait de craie, "
        "merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` "
        "retirés.\n"
        "- Question moteur inchangée (une chose). 5 chunks, kinds "
        "inchangés.\n"
        f"- {nwords} mots. N3 ≤ 16. TTS : notes, ssml, xai, piper par "
        "chunk.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
