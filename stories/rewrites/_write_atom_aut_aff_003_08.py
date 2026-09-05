#!/usr/bin/env python3
"""ATOM-AUT.AFF.003-08 — La miette de la couverture (F-NAR-019, N2, AUT.AFF.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.003-08"
TITLE = "La miette de la couverture"
N2 = LIMITS["N2"]
INDICE = "éclat de carreau"
CHARS = "Nina, papa, maman"
SETTING = "cuisine puis square, pique-nique"
FIL = (
    "La chaise gratte. Sur la couverture à carreaux, un éclat de carreau "
    "luit. Une miette s'arrête dessus. Nina veut le pique-nique du square, "
    "maintenant. Elle ramasse tout d'un coup : seau, ours, manteau s'emmêlent, "
    "l'éclat disparaît. Papa s'accroupit. Seau, manteau, ours. Merci vécu. "
    "Au square, elle part avec l'ours seul. Elle refuse de foncer, revient "
    "vers l'éclat. Sur la chaise, l'éclat de carreau reste pâle et sablé."
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
    "grain de pomme",
    "grain de sable",
    "grain de toile",
    "grain de laine",
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
        emphasis="éclat de carreau",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse; intensite=2; destinataire=enfant; "
            "sous_texte=elle_veut_le_pique_nique_maintenant; "
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
            "sous_texte=elle_reprend_ses_affaires_avant_de_partir; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="éclat de carreau",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=seau_puis_manteau_puis_ours; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de carreau",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_sans_la_miette; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de carreau",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_miette_repose_sur_l_eclat_du_debut; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "reprendre",
    "accepted_examples": "reprendre | ses affaires | il reprend | elle reprend | avant de partir",
    "retry_prompt": "Elle reprend ses affaires. Que fait Nina ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "chaise,pain,seau",
        [
            "narrateur|La chaise de la cuisine gratte le carrelage.",
            "narrateur|Au dossier, la couverture à carreaux pend.",
            "narrateur|Un éclat de carreau luit, pâle, au bord.",
            "enfant-f|Il brille, papa.",
            "papa|C'est un carreau plus clair.",
            "narrateur|Le pain tiède sent le four.",
            "narrateur|L'air sent la croûte, près de l'évier.",
            "papa|Une miette roule vers toi, Nina.",
            "narrateur|La miette s'arrête pile sur l'éclat.",
            "enfant-f|C'est le pain de l'ours !",
            "narrateur|L'ours brun attend près du seau bleu.",
            "maman|On emporte la couverture, Nina ?",
            "enfant-f|Oui, le square, maintenant !",
            "maman|Avec le seau, et ton manteau.",
            "narrateur|Le manteau jaune attend près de la porte.",
            "narrateur|Le zip du manteau fait un petit clic.",
            "narrateur|En ce moment, Nina ramasse tout d'un coup.",
            "narrateur|Ours, seau et manteau s'emmêlent.",
            "narrateur|Le seau tape le carrelage, toc.",
            "enfant-f|Ça tombe !",
            "narrateur|La couverture glisse et cache l'éclat.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nina veut partir au square.",
            "narrateur|Avant de partir, que fait Nina ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "zip,seau",
        [
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Le seau d'abord, Nina.",
            "narrateur|Nina ramasse le seau bleu.",
            "narrateur|Le plastique est un peu rêche.",
            "maman|Le manteau, après le seau.",
            "narrateur|Elle prend le manteau jaune.",
            "enfant-f|Et mon ours ?",
            "papa|Regarde sous la couverture ?",
            "narrateur|Nina soulève un coin du tissu.",
            "narrateur|L'éclat de carreau reparaît, pâle.",
            "narrateur|La miette est collée au carreau clair.",
            "enfant-f|Ma miette est là.",
            "narrateur|L'ours est blotti contre l'éclat.",
            "enfant-f|Il était caché.",
            "narrateur|Elle glisse l'ours sous son bras.",
            "papa|Merci, Nina.",
            "enfant-f|On y va ?",
            "maman|Tu as le seau ?",
            "enfant-f|Oui, maman.",
            "narrateur|Maman plie la couverture, coin par coin.",
            "narrateur|Nina pose la main sur le tissu.",
            "narrateur|Sous les doigts, l'éclat de carreau reste froid.",
            "papa|Le square n'est pas loin.",
            "narrateur|Le sac sent le pain, sur le chemin.",
            "narrateur|L'air dehors sent l'herbe coupée.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "herbe,vent,seau",
        [
            "narrateur|Au square, l'herbe chatouille les chevilles.",
            "maman|On pose la couverture ici ?",
            "enfant-f|Oui, pour s'asseoir.",
            "narrateur|Nina étale le tissu dans l'herbe.",
            "narrateur|L'éclat de carreau luit vers le ciel.",
            "enfant-f|La miette, pour l'ours.",
            "narrateur|Elle pose la miette sur l'éclat.",
            "papa|Il a son pain, lui.",
            "narrateur|Nina verse du sable dans le seau.",
            "narrateur|Ça fait chh, autour de la miette.",
            "enfant-f|Mon château, maintenant !",
            "narrateur|Le vent fraîchit, soulève un coin.",
            "enfant-f|Je le tiens !",
            "maman|On rentre, le vent pique.",
            "enfant-f|J'y vais avec l'ours !",
            "narrateur|Elle part, l'ours contre la joue.",
            "narrateur|Le seau reste près du bac.",
            "narrateur|Le manteau reste sur le tissu.",
            "enfant-f|Ma miette !",
            "narrateur|Nina s'arrête net.",
            "narrateur|Elle refuse de foncer.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Sur la couverture, l'éclat de carreau pâlit.",
            "narrateur|La miette est là, minuscule.",
            "papa|Tu la vois, sur le carreau ?",
            "enfant-f|Oui.",
            "narrateur|Elle revient, prend le seau.",
            "narrateur|La sangle tape sa jambe.",
            "narrateur|Elle reprend le manteau jaune.",
            "maman|Et la couverture ?",
            "enfant-f|Oui, je la tiens.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "chaise,pain",
        [
            "narrateur|La cuisine sent le pain, au retour.",
            "narrateur|Maman pose la couverture sur la chaise.",
            "narrateur|L'éclat de carreau luit, comme au départ.",
            "enfant-f|La miette ?",
            "papa|Regarde l'éclat, Nina.",
            "narrateur|Nina se penche vers le tissu.",
            "narrateur|La miette est sableuse, collée à l'éclat.",
            "enfant-f|Elle a tenu.",
            "narrateur|Nina assied l'ours devant le tissu.",
            "enfant-f|C'est son pain.",
            "maman|Tu le vois, le petit éclat ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le seau bleu repose près de la porte.",
            "narrateur|Le manteau jaune retrouve le crochet.",
            "narrateur|Sur la chaise, l'éclat de carreau reste pâle et sablé.",
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
        "La chaise de la cuisine gratte le carrelage. Sur la couverture à "
        "carreaux, un éclat de carreau luit. Une miette de pain s'arrête "
        "dessus : Nina en fait le pain de l'ours. Elle veut le pique-nique "
        "du square, **maintenant**. Elle ramasse tout d'un coup : seau, "
        "ours et manteau s'emmêlent, l'éclat disparaît. Papa s'accroupit. "
        "Seau, manteau, ours. Merci vécu, après l'ours retrouvé. Au square, "
        "la miette repose sur l'éclat. Elle part avec l'ours seul. La miette "
        "manque. Elle refuse de foncer, revient. Sur la chaise, l'éclat de "
        "carreau reste pâle et sablé, comme au départ.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine (chaise, pain tiède, évier), puis square, "
        "pique-nique.\n"
        "- Désir : porter la miette et l'ours au square, maintenant.\n"
        "- Objet : couverture à carreaux, seau bleu, manteau jaune, ours, "
        "miette.\n"
        "- Indice unique : éclat de carreau, vu dès l'ouverture, payé sur "
        "la chaise.\n"
        "- Urgence douce : le square l'appelle, puis le vent pique.\n"
        "- Imprévu 1 : tout d'un coup, seau qui tape, éclat caché.\n"
        "- Cue : papa à la même hauteur, seau puis manteau. Un merci vécu, "
        "après l'ours glissé.\n"
        "- Imprévu 2 (plus rusé) : elle part avec l'ours, laisse miette et "
        "affaires.\n"
        "- Résolution : elle refuse de foncer, lit l'éclat, reprend seau, "
        "manteau, couverture.\n"
        "- Retour : miette collée à l'éclat, ours devant le tissu, éclat pâle et sablé.\n\n"
        "## Vécu\n\n"
        "Leçon AUT.AFF.003 (reprendre ses affaires) greffée, jamais dite. "
        "La première idée (tout d'un coup) échoue. Le choix de Nina change "
        "l'action. Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Troupe D16 : Nina, papa, maman.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu : cuisine puis square, pique-nique. "
        "≠ seau jaune (parc), ≠ maison du lapin, ≠ capitaine, ≠ chaussettes, "
        "≠ feuille, ≠ gouttes, ≠ soupe.\n"
        "- Ouverture inventée (chaise qui gratte, éclat au bord), pas un "
        "gabarit v2.\n"
        "- Indice unique : éclat de carreau. Pas grain de miette/foin/"
        "feuille/paille/pin/pépin/pomme/sable, pas éclat de pince/thermos/"
        "coquille/bouton/ticket/goutte/boucle/corde/caisse/caillou/colle/"
        "lessive/vitre/casserole, pas point de gouttière, merle, miel.\n"
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
