#!/usr/bin/env python3
"""ATOM-AUT.AFF.002-01 — F-NAR-019. La feuille rouge de Victorino. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.002-01"
N1 = 10
TITLE = "La feuille rouge de Victorino"
FIL = (
    "La pluie écrit sur la vitre. Un trait de vitre descend, fin. "
    "Victorino veut la feuille rouge maintenant, pour le bol. Il tire "
    "le manteau : la manche reste à l'envers. Il refuse de foncer, "
    "dit qu'il le met, tourne la manche. Au jardin, la feuille glisse. "
    "Il suit le trait de vitre. Dans le bol, le trait brille sur la feuille."
)
CHARS = "Victorino, maman"
SETTING = "maison et jardin, vitre mouillée, sentier d'eau"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent", "tout bas")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)
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
    "eclat de pince",
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
    "trait de craie",
    "jardin gris",
    "escargot",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="trait de vitre",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_feuille_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="sortir",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; sous_texte=il_prend_le_manteau; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="manteau",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_dit_et_met_le_manteau; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="feuille",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; sous_texte=il_refuse_de_foncer; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="trait de vitre",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_trait_de_vitre_est_sur_la_feuille; "
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
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
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
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"tic {tic!r}: {ph}")
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"tic {m.group(0)!r}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"interdit {bad!r}: {ph}")
        out.append(f"{role}|{ph}")
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
    "narrateur|La pluie écrit sur la vitre.",
    "narrateur|Elle trace une ligne brillante.",
    "narrateur|Un trait de vitre descend, fin.",
    "narrateur|Derrière, une feuille rouge est collée.",
    "enfant-m|Maman, elle est rouge !",
    "maman|Oui.",
    "maman|Elle est collée au verre.",
    "narrateur|La cuisine sent le pain tiède.",
    "narrateur|Sur la table, un bol blanc attend.",
    "narrateur|Le bois de la table est lisse.",
    "narrateur|Une odeur de pain reste dans l'air.",
    "narrateur|Un carré de lumière touche le bol.",
    "narrateur|Le bol est vide, et rond.",
    "narrateur|Victorino lève les yeux vers la vitre.",
    "narrateur|La vitre est mouillée, un peu froide.",
    "narrateur|On dirait une petite étoile.",
    "narrateur|Maman essuie le rebord, sans presser.",
    "narrateur|En ce moment, Victorino s'approche.",
    "narrateur|Il pose le doigt sur le verre.",
    "narrateur|Le verre pique un peu, froid.",
    "narrateur|Son souffle fait un nuage rond.",
    "narrateur|Il essuie le nuage du pouce.",
    "enfant-m|Je la veux maintenant, pour le bol.",
    "maman|Tu la veux vite ?",
    "enfant-m|Oui, maman.",
    "maman|Elle est tombée, dans le jardin.",
    "maman|On peut aller la chercher.",
    "narrateur|Victorino court vers la porte.",
    "narrateur|Son pied tape le carreau, impatient.",
    "narrateur|La porte de bois est close.",
    "narrateur|Le manteau rouge attend au crochet.",
    "narrateur|Le crochet est bas, à sa hauteur.",
    "narrateur|Le tissu est épais, un peu rêche.",
    "narrateur|Il tire le manteau d'un coup.",
    "narrateur|Une manche est à l'envers.",
    "narrateur|Son bras ne passe pas.",
    "enfant-m|Oh.",
    "enfant-m|Ça ne veut pas.",
    "narrateur|Le manteau tombe un peu, lourd.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Ça serre, dans son ventre.",
    "narrateur|Le sourire quitte sa bouche.",
    "narrateur|Maman se baisse à sa hauteur.",
    "maman|Tu regardes la manche ?",
]

Q0001 = [
    "narrateur|Victorino veut sortir.",
    "narrateur|Que prend-il, avant la porte ?",
]

C0001 = [
    "enfant-m|Je prends le manteau.",
    "narrateur|Victorino refuse de tirer plus fort.",
    "narrateur|Il pose un genou au sol.",
    "narrateur|La manche est plate, tournée.",
    "enfant-m|Je la tourne, moi.",
    "narrateur|Il retourne le tissu, lentement.",
    "narrateur|La manche s'ouvre, large.",
    "enfant-m|Elle est libre.",
    "narrateur|Il veut courir vers la porte.",
    "narrateur|Le second bras reste coincé.",
    "enfant-m|Oh.",
    "narrateur|Il ne tire pas trop vite.",
    "narrateur|Il écoute le tissu, un instant.",
    "narrateur|Il glisse un bras, puis l'autre.",
    "narrateur|Le rouge est chaud comme une pomme.",
    "enfant-m|Il est chaud.",
    "enfant-m|Je le mets, moi.",
    "maman|Oui.",
    "maman|Il te tiendra chaud dehors.",
    "maman|Tu fermes le bouton ?",
    "narrateur|Victorino pousse le bouton, un clic.",
    "narrateur|Le manteau rouge est fermé.",
    "narrateur|Le col touche sa joue, chaud.",
    "maman|Merci, Victorino.",
    "narrateur|Victorino pose la main sur le tissu.",
    "narrateur|Le tissu est un peu rêche.",
    "maman|Le manteau est prêt ?",
    "enfant-m|Oui, maman.",
]

END = [
    "maman|On met tes chaussures ?",
    "narrateur|Victorino enfile ses chaussures.",
    "narrateur|Une semelle est froide.",
    "maman|Tu as fini tes chaussures ?",
    "enfant-m|Oui, maman.",
    "maman|On ouvre la porte ?",
    "enfant-m|Oui.",
    "enfant-m|On va chercher la feuille.",
    "narrateur|Maman ouvre la porte.",
    "narrateur|L'air sent la terre mouillée.",
    "narrateur|Le jardin est pâle, luisant.",
    "narrateur|Un sentier d'eau coupe l'herbe.",
    "narrateur|Victorino marche près de maman.",
    "narrateur|L'herbe est un peu froide.",
    "enfant-m|Je la vois !",
    "narrateur|La feuille rouge brille dans l'herbe.",
    "narrateur|Il tend la main, trop vite.",
    "narrateur|La feuille glisse sous l'herbe.",
    "enfant-m|Elle part !",
    "narrateur|Victorino recule d'un pas.",
    "narrateur|Il refuse de foncer.",
    "narrateur|Ses épaules se serrent un peu.",
    "narrateur|Ça tape, dans sa poitrine.",
    "narrateur|L'envie et l'inquiétude se bousculent.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Il lève les yeux vers la vitre.",
    "narrateur|Le trait de vitre brille, dehors.",
    "enfant-m|Il pointe vers l'herbe.",
    "maman|Tu le suis, ce trait ?",
    "enfant-m|Oui.",
    "narrateur|Il suit le trait, sans courir.",
    "narrateur|Au pied du mur, l'herbe s'ouvre.",
    "narrateur|La feuille rouge est là.",
    "enfant-m|Te voilà.",
    "maman|Tu la prends sans presser ?",
    "enfant-m|Oui, maman.",
]

FIN = [
    "narrateur|Victorino ramasse la feuille, sans presser.",
    "narrateur|Elle est lisse, un peu mouillée.",
    "narrateur|Il la glisse dans la poche.",
    "enfant-m|Elle est dans la poche.",
    "maman|Tes mains sont au chaud ?",
    "enfant-m|Oui.",
    "enfant-m|Dans les poches.",
    "narrateur|Ils rentrent dans la maison.",
    "narrateur|La maison est tiède.",
    "narrateur|La chaleur touche les joues de Victorino.",
    "narrateur|Victorino retire le manteau rouge.",
    "narrateur|Il le raccroche au crochet.",
    "narrateur|Le crochet fait un petit bruit.",
    "narrateur|Le manteau est à sa place.",
    "enfant-m|Je sors la feuille.",
    "narrateur|Il prend la feuille dans la poche.",
    "narrateur|Il la pose dans le bol blanc.",
    "enfant-m|Comme sur la vitre, maman !",
    "narrateur|Sur la feuille, un trait brille.",
    "narrateur|Le trait de vitre est sur la feuille.",
    "maman|Tu le vois, sur ta feuille ?",
    "enfant-m|Oui.",
    "enfant-m|C'est ma feuille rouge.",
    "narrateur|Le bol blanc garde la feuille.",
    "narrateur|Le trait de vitre dore, mince.",
]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    expected = {
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_Q0001",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    }
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in expected]
    if missing:
        raise SystemExit(f"{SID} chunks inattendus: {missing}")

    by = {
        "CHK_T0000_P0000": voice(
            by_src["CHK_T0000_P0000"], P0000, "opening", "pluie,vitre,porte",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "manteau",
                    "accepted_examples": "manteau | le manteau | son manteau",
                    "retry_prompt": "Il prend le manteau. Que prend Victorino ?",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "manteau,bouton",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "porte,jardin",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "bol,feuille",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "trait de vitre" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "trait de vitre" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    if "merci" not in blob:
        raise SystemExit(f"{SID}: merci absent")
    if not all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in chunks):
        raise SystemExit(f"{SID}: TTS incomplet")

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
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** AUT.AFF.002 — prendre le manteau, dire / choisir / s'affirmer (vécue)\n"
        "- **Personnages :** Victorino, maman\n"
        "- **Lieu :** maison et jardin, vitre mouillée, sentier d'eau, pied du mur\n"
        "- **Indice unique :** trait de vitre (vitre → herbe → feuille dans le bol)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La pluie écrit sur la vitre. Un trait de vitre descend. Derrière, "
        "une feuille rouge est collée. Le bol blanc attend, vide. Victorino "
        "veut la feuille **maintenant**, pour le bol. Il court, tire le manteau "
        "d'un coup : la manche est à l'envers. Première idée ratée. Épaules, "
        "ventre. Maman se baisse, pose une question. Il refuse de foncer, dit "
        "« je prends le manteau », tourne la manche, glisse les bras, ferme "
        "le bouton. Merci vécu. Dehors, il attrape trop vite : la feuille glisse. "
        "Il refuse de foncer, suit le trait de vitre jusqu'au pied du mur. "
        "Dans le bol, le trait de vitre brille sur la feuille.\n\n"
        "## Vécu\n\n"
        "Victorino veut la feuille **maintenant**. Impatience, puis épaules "
        "quand le manteau résiste. Maman se baisse, ne récite pas la règle. "
        "Il dit, choisit, met le manteau lui-même. Merci après le bouton. "
        "Au jardin, deuxième ruse : la feuille glisse. Il suit l'indice du "
        "début. Fin : le trait de la vitre est sur la feuille.\n\n"
        "## Vu et corrigé\n\n"
        "- Ouverture inventée (la pluie écrit), pas « joue au salon ».\n"
        "- ≠ ATOM-AUT.AFF.001-05 (escargot, grain de feuille, dalle du seau).\n"
        "- ≠ TREE-AUT-002 (manteau, jardin gris).\n"
        "- Tics « encore / déjà / tout doux / tout calme » absents.\n"
        "- Indice unique : trait de vitre. Pas trait de craie. Pas grain / éclat.\n"
        "- Leçon non dite : il prend le manteau, dit, choisit. Pas de morale.\n"
        "- Merci vécu. Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous_texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action plus vive.\n"
        "- N1 ≤ 10. `check()` OK. Pas apply.\n\n"
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
