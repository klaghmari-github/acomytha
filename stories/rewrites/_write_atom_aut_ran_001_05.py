#!/usr/bin/env python3
"""ATOM-AUT.RAN.001-05 — La voiture rouge (F-NAR-019, N2, AUT.RAN.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.RAN.001-05"
TITLE = "La voiture rouge"
N2 = LIMITS["N2"]
INDICE = "éclat d'écorce"
CHARS = "Victorino, papa, maman"
SETTING = "chambre, odeur d'orange, merle sur la gouttière, caisse à éclat d'écorce"
FIL = (
    "Le merle glisse sur le rideau. Sur la caisse, un éclat d'écorce luit. "
    "Victorino veut la rouge sur l'oreiller, maintenant, pour l'histoire. "
    "Il ramasse toute la pile : clac, l'éclat disparaît. Papa s'accroupit. "
    "Une par une. Merci vécu. Il refuse de foncer. Sous le lit, l'éclat d'écorce reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
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
    "trois notes",
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "grain de pomme",
    "grain de sable",
    "grain de toile",
    "grain de laine",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de farine",
    "éclat d'ombre",
    "éclat de carreau",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de caillou",
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de sonnette",
    "éclat de liste",
    "éclat de clé",
    "éclat de cuillère",
    "éclat de tasse",
    "éclat d'orange",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat d'écorce",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_rouge_sur_l_oreiller_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="voiture rouge",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_est_sous_les_autres; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="éclat d'écorce",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=une_par_une_le_toit_rouge_reparaît; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat d'écorce",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_sans_regarder_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat d'écorce",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_toit_rouge; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "la voiture rouge",
    "accepted_examples": (
        "la voiture rouge | la rouge | voiture rouge | "
        "sous la route | sous les voitures | dessous"
    ),
    "retry_prompt": "Il cherche sous les voitures. Où est la voiture rouge ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "rideau,merle,orange,voitures",
        [
            "narrateur|Une ombre d'oiseau glisse sur le rideau.",
            "narrateur|Le merle est sur la gouttière.",
            "narrateur|Au pied du lit, la caisse en bois attend.",
            "narrateur|Un éclat d'écorce luit sur le couvercle.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, sur le bois ?",
            "narrateur|L'air sent l'orange, depuis la cuisine.",
            "maman|J'ai pelé un fruit, Victorino.",
            "narrateur|Le tapis de la chambre est épais.",
            "narrateur|Des voitures rouges et bleues attendent.",
            "enfant-m|La rouge va jusqu'au lit, maintenant !",
            "maman|Avec le rideau ouvert, pour l'histoire ?",
            "enfant-m|Oui, elle vient sur l'oreiller.",
            "papa|Ta route est longue, jusqu'au lit.",
            "narrateur|En ce moment, Victorino pousse la rouge.",
            "narrateur|Les roues font un petit bruit sec.",
            "narrateur|Une bleue la suit, trop près.",
            "narrateur|D'autres voitures se poussent vers le lit.",
            "narrateur|La bleue passe par-dessus la pile.",
            "narrateur|La rouge disparaît sous les toits.",
            "enfant-m|Oh !",
            "narrateur|Le sourire de Victorino disparaît.",
            "enfant-m|Où est ma voiture rouge ?",
            "maman|Sous le lit, peut-être ?",
            "narrateur|Il se penche, trop vite.",
            "narrateur|De la poussière, un chausson.",
            "narrateur|Pas de rouge.",
            "enfant-m|Je prends toute la pile !",
            "narrateur|Il ramasse les voitures d'un coup.",
            "narrateur|La pile glisse, clac, contre la caisse.",
            "narrateur|Le couvercle bascule.",
            "narrateur|L'éclat d'écorce disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Elles se sont bousculées.",
            "enfant-m|Elle est perdue.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorino cherche sa voiture rouge.",
            "narrateur|Où est-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "caisse,voitures",
        [
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu regardes bien sous la route ?",
            "enfant-m|Oui, papa.",
            "narrateur|Victorino pose une bleue dans la caisse.",
            "narrateur|Toc.",
            "narrateur|Un bout de tapis reparaît.",
            "maman|Une par une, Victorino.",
            "narrateur|Il soulève une voiture noire.",
            "narrateur|Un toit rouge brille dessous.",
            "enfant-m|Ma rouge !",
            "narrateur|La voiture rouge était sous les autres.",
            "narrateur|Elle sent le tapis, un peu froide.",
            "papa|Merci, tu l'as trouvée.",
            "narrateur|Le couvercle de la caisse se rassoit.",
            "narrateur|L'éclat d'écorce reparaît, pâle.",
            "enfant-m|Il est revenu.",
            "maman|Te voilà, petite rouge.",
            "enfant-m|Elle était dessous.",
            "narrateur|Victorino la tient dans la paume.",
            "narrateur|Il essuie le tapis du toit, du pouce.",
            "papa|Le chemin du lit est presque libre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "caisse,rideau",
        [
            "narrateur|Les dernières voitures restent en tas.",
            "enfant-m|Je les pousse toutes, maintenant !",
            "narrateur|Il avance les mains vers le tas.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Il refuse de foncer.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Papa attend, sans parler.",
            "narrateur|Victorino observe la caisse, écoute la chambre.",
            "narrateur|Sur le couvercle, l'éclat d'écorce luit.",
            "enfant-m|Là, près de l'éclat.",
            "narrateur|Il soulève la dernière bleue, tout près.",
            "narrateur|Rien dessous, seulement le tapis.",
            "narrateur|Les dernières voitures vont dans la caisse.",
            "narrateur|Toc.",
            "maman|On ouvre le rideau ?",
            "enfant-m|Oui, tout grand.",
            "papa|La rouge vient avec toi ?",
            "enfant-m|Oui, sur l'oreiller.",
            "narrateur|Victorino pousse la caisse sous le lit.",
            "narrateur|Le bois glisse, l'éclat d'écorce aussi.",
            "narrateur|Un filet de soleil entre sur le tapis.",
            "narrateur|Victorino grimpe sur le lit.",
            "narrateur|La voiture rouge est sur l'oreiller.",
            "maman|Je raconte ?",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "orange,merle",
        [
            "narrateur|Maman s'assoit au bord du lit.",
            "narrateur|Sa voix est basse, tout près.",
            "papa|Tu veux un quartier d'orange ?",
            "enfant-m|Oui, papa.",
            "narrateur|L'orange sent fort, sucrée.",
            "narrateur|Le jus brille un peu sur le doigt.",
            "enfant-m|La rouge a un petit éclat.",
            "narrateur|Un éclat d'écorce tient sur le toit.",
            "maman|Tu le vois, comme sur la caisse ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le merle penche la tête, dehors.",
            "narrateur|Sous le lit, l'éclat d'écorce reste pâle.",
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
        elif cid != "CHK_T0000_P0000":
            extra["pause_before_ms"] = 200
        by[cid] = voice(c, lines, profile, sons, extra)
    merged = dict(src)
    merged["fil_rouge"] = FIL
    merged["title"] = TITLE
    merged["characters"] = CHARS
    merged["setting"] = SETTING
    merged["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    nwords = sum(words(c["text"]) for c in merged["chunks"])
    blob = "\n".join(c["script"] for c in merged["chunks"]).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
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
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "## Promesse narrative\n\n"
        "Une ombre d'oiseau glisse sur le rideau. Le merle est sur la "
        "gouttière. Au pied du lit, un éclat d'écorce luit sur le couvercle "
        "de la caisse. Victorino veut la voiture rouge sur l'oreiller, "
        "**maintenant**, pour l'histoire au rideau ouvert. Les voitures se "
        "bousculent : la rouge disparaît. Il ramasse toute la pile : clac, "
        "l'éclat disparaît. Papa s'accroupit. Une par une. Merci vécu, "
        "quand le toit rouge reparaît. Les dernières restent en tas. Il "
        "refuse de foncer, lit l'éclat. Sous le lit, l'éclat d'écorce reste "
        "pâle. Un éclat d'écorce tient sur le toit rouge.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chambre, odeur d'orange, merle sur la gouttière, caisse "
        "en bois. ≠ nappe vanille, ≠ cacao pluie, ≠ pain farine, ≠ cabane "
        "sous la table.\n"
        "- Désir : porter la rouge jusqu'à l'oreiller, maintenant.\n"
        "- Objet : voiture rouge, caisse à éclat d'écorce, rideau, orange.\n"
        "- Indice unique : éclat d'écorce, vu dès l'ouverture, payé sur le "
        "toit et sous le lit.\n"
        "- Urgence douce : l'histoire au lit, rideau ouvert.\n"
        "- Imprévu 1 : pile, rouge perdue, ramassage d'un coup, éclat caché.\n"
        "- Cue : papa à la même hauteur, une par une. Un merci vécu, après "
        "le toit rouge.\n"
        "- Imprévu 2 (plus rusé) : pousser le tas restant d'un coup.\n"
        "- Résolution : il refuse de foncer, lit l'éclat, pose les dernières.\n"
        "- Retour : orange, merle, éclat d'écorce pâle sous le lit et sur "
        "le toit.\n\n"
        "## Vécu\n\n"
        "Leçon AUT.RAN.001 (retrouver en rangeant, jamais dite) greffée. "
        "La première idée (toute la pile) échoue. Le choix de Victorino "
        "change l'action. Un « en ce moment ». Un merci vécu. Adulte + "
        "question. Troupe D16 : Victorino, papa, maman.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : chambre, orange, merle, "
        "caisse. Sans lumière de miel. ≠ RAN.001-01..004.\n"
        "- Ouverture inventée (ombre d'oiseau sur le rideau), pas un "
        "gabarit v2.\n"
        "- Indice unique : éclat d'écorce. Pas merle-trois-notes, miel, "
        "gouttes, pas grain de miette/foin/feuille, pas éclat de nappe/"
        "boîte/farine/ombre/carreau/orange.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Question moteur inchangée (la voiture rouge). 5 chunks, kinds "
        "inchangés.\n"
        f"- {nwords} mots. N2 ≤ 15. TTS : notes, ssml, xai, piper par chunk.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
