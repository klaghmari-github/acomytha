#!/usr/bin/env python3
"""ATOM-AUT.AFF.003-04 — La route des chaussettes jaunes (F-NAR-019, N2, AUT.AFF.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.003-04"
TITLE = "La route des chaussettes jaunes"
N2 = LIMITS["N2"]
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
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pomme",
    "grain de sable",
    "grain de lessive",
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
    "éclat de horloge",
    "éclat d'horloge",
    "éclat de tasse",
    "éclat de orange",
    "éclat d'orange",
    "éclat de colle",
    "trait de craie",
    "trait de vitre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de lessive",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_route_jaune_maintenant; "
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
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=avant_de_partir_elle_prend_ses_affaires; "
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
            "intensite=1; destinataire=enfant; "
            "sous_texte=pelle_manteau_doudou_reviennent_avec_elle; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de lessive",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_l_éclat_montre_la_chaise; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de lessive",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_éclat_porte_une_trace_de_sable; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "reprendre",
    "accepted_examples": "reprendre | ses affaires | il reprend | elle reprend | avant de partir",
    "retry_prompt": "Elle reprend ses affaires. Que fait Mila ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "radiateur,pluie,enfants_parc",
        [
            "narrateur|Le radiateur du couloir fait clic.",
            "narrateur|L'air tiède sent la laine mouillée.",
            "narrateur|Sur une chaussette jaune, un éclat de lessive brille.",
            "narrateur|Il est blanc, sec, et il pique un peu.",
            "narrateur|Mila connaît ce couloir, ses dalles, ses bruits.",
            "narrateur|Après la pluie, l'éclat paraît nouveau.",
            "narrateur|Les bottes gouttent près de la porte.",
            "enfant-f|Je veux la route, maintenant !",
            "papa|Quelle route, Mila ?",
            "enfant-f|La route jaune, pour le doudou.",
            "papa|On met les chaussettes ?",
            "narrateur|Mila enfile la première, puis l'autre.",
            "narrateur|L'éclat reste collé au fil.",
            "papa|Elles sont chaudes ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ils ferment la porte.",
            "narrateur|La rue sent la pluie et la terre.",
            "narrateur|Une flaque brille entre deux dalles.",
            "narrateur|En ce moment, Mila est au square.",
            "narrateur|Le bac à sable luit, un peu sombre.",
            "narrateur|Papa s'assoit près du bord.",
            "narrateur|Le doudou gris attend au bout.",
            "narrateur|Le manteau bleu repose sur le banc.",
            "narrateur|Une pelle rouge est dans le sable.",
            "enfant-f|Je fais la route, tout de suite !",
            "papa|Je t'écoute.",
            "narrateur|Mila verse tout le sable, d'un coup.",
            "narrateur|Ça fait chh, trop fort.",
            "narrateur|La route glisse et s'effondre.",
            "narrateur|Le doudou tombe sur le flanc.",
            "enfant-f|Elle est cassée !",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Le sable a glissé ?",
            "enfant-f|Oui.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|On peut en faire un bout.",
            "narrateur|Mila tasse un petit chemin, lentement.",
            "enfant-f|Il peut marcher un peu.",
            "papa|C'est l'heure.",
            "enfant-f|La route n'est pas finie.",
            "narrateur|Mila saisit le doudou, rien d'autre.",
            "narrateur|Elle court vers la grille.",
            "narrateur|Le sable mouillé fait glisser le pied.",
            "enfant-f|Aïe !",
            "narrateur|La pelle reste dans le bac.",
            "narrateur|Le manteau reste sur le banc.",
            "narrateur|Mila s'arrête.",
            "enfant-f|Attends.",
            "narrateur|Elle revient vers le bac.",
            "narrateur|Elle prend la pelle rouge.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Mila tient la pelle.",
            "narrateur|Avant de partir, que fait Mila ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "tissu,banc",
        [
            "narrateur|Mila cherche le manteau.",
            "narrateur|Le tissu est un peu frais.",
            "narrateur|Elle le prend.",
            "enfant-f|Le manteau aussi.",
            "papa|Et le doudou ?",
            "narrateur|Mila va au bout du bac.",
            "narrateur|Le doudou a du sable sur l'oreille.",
            "enfant-f|Il est gris.",
            "enfant-f|Il est là.",
            "narrateur|Elle le prend.",
            "papa|Tu as la pelle ?",
            "enfant-f|Oui.",
            "papa|On peut rentrer.",
            "narrateur|Ils marchent vers la maison.",
            "narrateur|La rue luit, un peu froide.",
            "narrateur|Papa tient le sac.",
            "narrateur|Mila tient le doudou.",
            "papa|Tu es prête ?",
            "enfant-f|Je suis prête.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "resolution",
        "porte,radiateur,chaussettes",
        [
            "narrateur|Ils arrivent à la porte.",
            "narrateur|Les chaussettes jaunes ne sont plus au radiateur.",
            "papa|Elles sont à tes pieds.",
            "enfant-f|La route, maintenant !",
            "narrateur|Mila tire les deux chaussettes, d'un coup.",
            "narrateur|La pelle glisse entre ses bras.",
            "narrateur|Le manteau tombe avec le doudou.",
            "narrateur|Les chaussettes font un tas jaune.",
            "enfant-f|Elles se mélangent !",
            "narrateur|Mila refuse de foncer.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Personne ne dit le chemin.",
            "narrateur|Mila écoute le couloir.",
            "enfant-f|Le radiateur chuchote.",
            "narrateur|Sur la dalle, l'éclat de lessive tremble.",
            "narrateur|Il penche vers la chaise.",
            "enfant-f|C'est là !",
            "narrateur|Mila pose la pelle près de la porte.",
            "narrateur|Elle pose le manteau sur la chaise.",
            "narrateur|Le doudou reste contre elle.",
            "narrateur|Elle retire une chaussette, puis l'autre.",
            "narrateur|Elle les pose en ligne sur le plancher.",
            "narrateur|L'éclat revient sur le fil.",
            "enfant-f|C'est la route.",
            "papa|Le doudou peut marcher.",
            "narrateur|Mila fait avancer le doudou.",
            "narrateur|Pas à pas, sur le jaune.",
            "enfant-f|Il arrive.",
            "papa|Merci, Mila.",
            "papa|On a fait la route ?",
            "enfant-f|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "radiateur,plancher",
        [
            "narrateur|Le doudou s'arrête au bout du jaune.",
            "narrateur|Mila pose les pieds sur le plancher tiède.",
            "papa|Tes pieds sont au chaud ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le radiateur du couloir fait clic.",
            "narrateur|L'éclat de lessive porte une trace de sable.",
            "enfant-f|Il a voyagé.",
            "papa|Comme toi.",
            "narrateur|Les chaussettes jaunes restent en ligne.",
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
        "Le radiateur du couloir fait clic. Un éclat de lessive blanc brille "
        "sur une chaussette jaune. Mila veut la route jaune pour le doudou, "
        "maintenant. Au square, elle verse tout le sable d'un coup : la route "
        "s'effondre. Elle court avec le doudou seul, glisse, revient. Pelle, "
        "manteau, doudou. À la maison, elle tire les chaussettes d'un coup : "
        "tout tombe. Elle refuse de foncer. L'éclat penche vers la chaise. "
        "Elle pose, aligne, et l'éclat porte une trace de sable."
    )
    merged["title"] = TITLE
    merged["characters"] = "Mila, papa"
    merged["setting"] = "maison après la pluie, puis square"
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
    if "éclat de lessive" not in joined:
        raise SystemExit("indice éclat de lessive absent")
    if "grain de lessive" in joined.lower():
        raise SystemExit("grain de lessive banni")
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "## Promesse narrative\n\n"
        "Le radiateur du couloir fait clic après la pluie. Un éclat de lessive "
        "blanc, sec, pique un peu sur une chaussette jaune. Mila veut la route "
        "jaune pour le doudou, maintenant. Au square, elle verse tout le sable "
        "d'un coup : la route s'effondre, le doudou tombe. Elle court avec le "
        "doudou seul, glisse, revient. Elle prend la pelle, le manteau, le "
        "doudou. À la maison, elle tire les deux chaussettes d'un coup : tout "
        "tombe. Elle refuse de foncer. L'éclat penche vers la chaise. Elle "
        "pose, aligne, et l'éclat porte une trace de sable.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : couloir du radiateur après la pluie, laine mouillée, "
        "bottes, flaque, square, bac à sable.\n"
        "- Désir : la route jaune pour le doudou, maintenant.\n"
        "- Objet : chaussettes jaunes, pelle rouge, manteau bleu, doudou gris.\n"
        "- Indice unique : éclat de lessive, vu dès l'ouverture, payé au "
        "climax et sur le fil de la chaussette.\n"
        "- Urgence douce : c'est l'heure, la route n'est pas finie.\n"
        "- Imprévu 1 : tout le sable d'un coup, route cassée ; elle part "
        "avec le doudou seul et glisse.\n"
        "- Cue : papa à la même hauteur, un bout de chemin. Un merci vécu, "
        "quand la route tient enfin.\n"
        "- Imprévu 2 (plus rusé) : à la maison, elle tire les chaussettes "
        "en tenant tout ; le tas tombe.\n"
        "- Résolution : elle refuse de foncer, lit l'éclat vers la chaise, "
        "pose pelle et manteau, aligne les chaussettes.\n"
        "- Retour : doudou au bout du jaune, pieds au chaud, l'éclat a une "
        "trace de sable.\n\n"
        "## Vécu\n\n"
        "Leçon AUT.AFF.003 (reprendre ses affaires avant de partir) greffée, "
        "jamais dite. La première idée (tout d'un coup, puis le doudou seul) "
        "échoue. Le choix de Mila change l'action. Un « en ce moment ». Un "
        "merci vécu. Adulte + question. Troupe D16 : Mila, papa.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu : maison après la pluie, puis square. "
        "≠ seau de 003-01, ≠ lapin de 003-02, ≠ capitaine de 003-03.\n"
        "- Ouverture inventée (clic du radiateur, laine mouillée), pas un "
        "gabarit v2.\n"
        "- Indice unique : éclat de lessive. Pas grain de lessive, pas grain "
        "de miette/foin/feuille/paille/pin/pépin/pomme/sable, pas éclat de "
        "pince/thermos/coquille/bouton/ticket/goutte/boucle/corde/caisse/"
        "marche/caillou/liste/clé/cuillère/sonnette/horloge/tasse/orange/"
        "colle, pas trait de craie/vitre, merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Question moteur inchangée (reprendre). 5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N2 ≤ 15. TTS : notes, ssml, xai, piper par chunk.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
