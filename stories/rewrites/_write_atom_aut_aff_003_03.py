#!/usr/bin/env python3
"""ATOM-AUT.AFF.003-03 — Le capitaine dans l'herbe (F-NAR-019, N3, AUT.AFF.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.003-03"
TITLE = "Le capitaine dans l'herbe"
LIM = LIMITS["N3"]
CHARS = "Victorina, papa"
SETTING = "maison, parc, puis pique-nique au jardin"
FIL = (
    "Sur le radiateur, un bateau de papier sèche. Un pli de voile coupe "
    "la lumière. Victorina veut que l'ours soit capitaine du seau-bateau, "
    "maintenant. Au parc, elle saisit le seau trop lourd : il glisse. "
    "Elle refuse de foncer, reprend seau, manteau, capitaine. Au jardin, "
    "la gourde roule. Le pli de voile sur la nappe penche vers le dessous. "
    "À la maison, le pli touche une oreille."
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
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de marche",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cuillère",
    "éclat de sonnette",
    "trait de craie",
    "trait de vitre",
    "ombre en forme",
    "minuscule symbole",
    "marque fine",
    "tache de couleur",
    "seau Raphaël",
    "maison du lapin",
    "on reprend ses affaires",
    "avant de partir, on reprend",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="pli de voile",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_capitaine_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="partir",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=avant_de_partir_elle_reprend; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="capitaine",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_reprend_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="pli de voile",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis prudence; intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_retrouve_le_pli; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="pli de voile",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_pli_de_voile_touche_une_oreille; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "reprendre",
    "accepted_examples": "reprendre | ses affaires | il reprend | elle reprend | avant de partir",
    "retry_prompt": "Elle reprend ses affaires. Que fait Victorina ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "radiateur,parc",
        [
            "narrateur|Sur la chaise, l'ours penche une oreille.",
            "narrateur|Il regarde le radiateur, tiède.",
            "narrateur|Un bateau de papier y dort.",
            "narrateur|Il sent la colle, un peu la poussière.",
            "narrateur|Un pli de voile coupe la lumière.",
            "narrateur|La voile est froissée, toute petite.",
            "papa|C'est le bateau d'hier, Victorina.",
            "enfant-f|Il est chaud, papa.",
            "papa|Le radiateur l'a gardé.",
            "narrateur|Dehors, le ciel se déchire.",
            "narrateur|Une goutte glisse sur la vitre.",
            "papa|La pluie s'en va.",
            "papa|On met les chaussures ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Avec l'ours, maintenant !",
            "narrateur|Papa noue une chaussure.",
            "narrateur|L'ours attend contre son bras.",
            "narrateur|Ils ferment la porte.",
            "narrateur|Le parc sent la terre, mouillée.",
            "narrateur|Le soleil revient sur le bac à sable.",
            "narrateur|Papa s'assoit sur le banc.",
            "narrateur|Victorina a un seau jaune.",
            "narrateur|Elle a un manteau bleu.",
            "narrateur|En ce moment, elle pose l'ours dans l'herbe.",
            "enfant-f|Le seau, c'est un bateau.",
            "papa|Et l'ours ?",
            "enfant-f|Le capitaine.",
            "enfant-f|Je le mets là, tout de suite.",
            "papa|Je te vois.",
            "narrateur|Elle verse le sable dans le seau.",
            "narrateur|Le seau devient lourd, très lourd.",
            "narrateur|Elle le pose près du bac.",
            "narrateur|L'ours attend dans l'herbe mouillée.",
            "papa|Le soleil baisse.",
            "papa|On rentre ?",
            "enfant-f|Le bateau reste ?",
            "papa|Le bateau peut venir.",
            "enfant-f|Je le prends, maintenant !",
            "narrateur|Elle saisit le seau d'un coup.",
            "narrateur|Le sable pèse trop.",
            "narrateur|Le seau penche, puis glisse.",
            "narrateur|Un filet de sable tombe sur ses chaussures.",
            "enfant-f|Oh.",
            "narrateur|Le sourire quitte sa bouche.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu veux tirer, ou regarder ?",
            "enfant-f|Je veux le bateau.",
            "narrateur|Victorina tire une dernière fois.",
            "narrateur|Le seau reste trop lourd.",
            "narrateur|Le manteau bleu reste sur le banc.",
            "narrateur|L'ours reste dans l'herbe.",
            "enfant-f|Je reprends tout.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Le seau penche, trop lourd, près du bac.",
            "narrateur|Avant de partir, que fait Victorina ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "sable,manteau",
        [
            "enfant-f|J'arrête de tirer.",
            "narrateur|Elle pose le seau près du bac.",
            "enfant-f|Il est trop lourd.",
            "papa|On le vide un peu ?",
            "narrateur|Victorina penche le seau, sans presser.",
            "narrateur|Le sable retombe en filet.",
            "enfant-f|Il est plus léger.",
            "narrateur|Elle reprend le seau jaune.",
            "narrateur|Le manteau bleu attend sur le banc.",
            "narrateur|Elle le prend.",
            "narrateur|Le tissu est un peu froid.",
            "enfant-f|Et le capitaine ?",
            "papa|Il est dans l'herbe.",
            "narrateur|Victorina cherche trop vite.",
            "narrateur|L'herbe cache l'ours.",
            "enfant-f|Je ne le vois pas.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Elle s'arrête, les pieds dans l'herbe.",
            "narrateur|Une feuille couvre une oreille.",
            "enfant-f|Il dormait.",
            "narrateur|Elle prend l'ours contre elle.",
            "papa|Merci, Victorina.",
            "papa|Tu tiens tout ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le seau tape un peu sa jambe.",
            "narrateur|Le manteau pèse sur son bras.",
            "narrateur|L'ours sent l'herbe mouillée.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "jardin,nappe",
        [
            "narrateur|Plus tard, le jardin sent l'herbe coupée.",
            "narrateur|Papa pose une nappe sur la table basse.",
            "papa|C'est le pique-nique du capitaine.",
            "enfant-f|Il a faim, maintenant.",
            "narrateur|Victorina a une gourde.",
            "narrateur|Elle a une casquette.",
            "narrateur|L'ours est assis sur la nappe.",
            "enfant-f|J'ai soif.",
            "papa|Bois un peu.",
            "narrateur|L'eau fait glouglou.",
            "narrateur|Une miette reste près de l'ours.",
            "papa|La soupe attend, à la maison.",
            "enfant-f|Le capitaine aussi.",
            "enfant-f|On y va, maintenant !",
            "narrateur|Elle saisit la gourde d'un coup.",
            "narrateur|La gourde roule sous la table.",
            "enfant-f|Elle part !",
            "narrateur|Victorina veut se jeter dessous.",
            "narrateur|La nappe glisse d'un coin.",
            "narrateur|Le sourire disparaît.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "enfant-f|Pas comme le seau.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe la nappe, puis la table.",
            "narrateur|Un pli de voile y court, fin.",
            "narrateur|Le même pli que sur le bateau.",
            "narrateur|Le pli penche vers le dessous.",
            "enfant-f|Là.",
            "papa|Tu suis ce pli ?",
            "enfant-f|Oui, papa.",
            "narrateur|Elle se penche, sans presser.",
            "narrateur|La gourde s'était cachée.",
            "narrateur|Elle la prend.",
            "narrateur|La casquette attend sur le banc du jardin.",
            "narrateur|Elle la prend.",
            "narrateur|L'ours garde la miette dans sa patte.",
            "enfant-f|Je le prends.",
            "narrateur|Elle le prend contre elle.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "porte,bateau",
        [
            "narrateur|Ils ouvrent la porte.",
            "narrateur|Le bateau de papier est tiède.",
            "enfant-f|Il a attendu.",
            "papa|Pose le seau à côté ?",
            "narrateur|Victorina pose le seau jaune.",
            "narrateur|Les deux bateaux se touchent.",
            "enfant-f|Le petit et le grand.",
            "narrateur|Elle pose la casquette sur la chaise.",
            "narrateur|Elle pose la gourde près de l'évier.",
            "narrateur|Victorina pose l'ours contre le bateau de papier.",
            "narrateur|Le pli de voile touche une oreille.",
            "enfant-f|Le capitaine est rentré.",
            "papa|Il a sa miette ?",
            "enfant-f|Oui.",
            "narrateur|La voile froissée garde l'oreille au chaud.",
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
        elif cid != "CHK_T0000_P0000":
            extra_kw["pause_before_ms"] = 200
        by[cid] = voice(c, lines, profile, sons, extra_kw)
    merged = dict(src)
    merged["fil_rouge"] = FIL
    merged["title"] = TITLE
    merged["characters"] = CHARS
    merged["setting"] = SETTING
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
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if joined.count("pli de voile") < 3:
        raise SystemExit("indice pli de voile trop peu payé")
    if "pli de voile" not in by["CHK_T0000_P0000"]["text"]:
        raise SystemExit("indice absent à l'ouverture")
    if "pli de voile" not in by["CHK_T0000_P0000_END_F0001"]["text"]:
        raise SystemExit("indice non payé à la fin")
    if "merci" not in blob:
        raise SystemExit("merci absent")
    kinds = {c["chunk_id"]: c.get("kind") for c in src["chunks"]}
    for c in merged["chunks"]:
        if c.get("kind") != kinds[c["chunk_id"]]:
            raise SystemExit(f"kind changé: {c['chunk_id']}")
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** AUT.AFF.003 — reprendre ses affaires avant de partir (vécue)\n"
        "- **Personnages :** Victorina, papa\n"
        "- **Lieu :** maison, parc, pique-nique au jardin (monde du dump)\n"
        "- **Indice unique :** pli de voile (radiateur → nappe → oreille de l'ours)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "## Promesse narrative\n\n"
        "L'ours penche une oreille vers le radiateur. Un bateau de papier "
        "sèche. Un pli de voile coupe la lumière. Victorina veut que l'ours "
        "soit capitaine du seau-bateau, **maintenant**. Au parc, elle saisit "
        "le seau d'un coup : trop lourd, il glisse. Sourire parti. Papa "
        "s'accroupit. Elle refuse de foncer, vide le sable, reprend seau, "
        "manteau, capitaine sous une feuille. Merci vécu. Au jardin, la "
        "gourde roule sous la table. Elle refuse de foncer. Le pli de voile "
        "sur la nappe penche vers le dessous. À la maison, les deux bateaux "
        "se touchent. Le pli de voile touche une oreille.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : radiateur tiède, colle, parc après la pluie, nappe au jardin.\n"
        "- Désir : l'ours capitaine du seau-bateau, tout de suite.\n"
        "- Objet : seau jaune, manteau bleu, ours, gourde, casquette.\n"
        "- Indice unique : pli de voile, vu dès l'ouverture, payé au climax "
        "(nappe) et sur l'oreille à la fin.\n"
        "- Urgence douce : le soleil baisse ; la soupe attend.\n"
        "- Imprévu 1 : seau trop lourd, saisi trop vite, filet de sable.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après l'ours repris.\n"
        "- Imprévu 2 (plus rusé) : gourde sous la table, nappe qui glisse.\n"
        "- Résolution : elle refuse de foncer, suit le pli, reprend gourde, "
        "casquette, capitaine.\n"
        "- Retour : seau contre le bateau de papier, pli contre une oreille.\n\n"
        "## Vécu\n\n"
        "Leçon AUT.AFF.003 (reprendre ses affaires avant de partir) greffée, "
        "jamais dite en slogan. Deux départs (parc, jardin). La première idée "
        "(saisir le seau tout de suite) échoue. Le choix de Victorina change "
        "l'action. Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Troupe D16 : Victorina, papa.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : maison, parc, pique-nique au "
        "jardin. ≠ ATOM-AUT.AFF.003-01 (seau de Raphaël). ≠ ATOM-AUT.AFF.003-02 "
        "(maison du lapin).\n"
        "- Ouverture inventée (l'ours penche une oreille), pas un gabarit v2.\n"
        "- Indice unique : pli de voile. Pas grain / éclat / trait de craie / "
        "trait de vitre / merle / miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Slogan « on reprend ses affaires » retiré. Le geste se voit.\n"
        "- Question moteur inchangée (reprendre). 5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N3 ≤ 16. TTS : notes, ssml, xai, piper par chunk.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
