#!/usr/bin/env python3
"""ATOM-COL.ECO.001-01 — F-NAR-019. La gouttière et le crayon d'Aniss. N2. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.001-01"
N2 = 15
TITLE = "La gouttière et le crayon d'Aniss"
FIL = (
    "La maison boit la pluie par la gouttière. Sur le crayon jaune, un "
    "éclat de crayon brille. Aniss veut dessiner la chanson, maintenant. "
    "Il coupe papa : les mots se perdent. Il pose la feuille trop vite : "
    "le papier boit une goutte. À l'école, sa phrase se cogne à la classe. "
    "Il refuse de foncer, attend la tasse, dit la chanson. Merci vécu. "
    "Sur la ligne jaune, l'éclat de crayon tient."
)
CHARS = "Aniss, papa, maman, maîtresse"
SETTING = "cuisine sous la pluie, école, puis table du soir"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent", "tout bas")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)
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
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "éclat de nappe",
    "éclat de wagon",
    "éclat de casserole",
    "éclat de goutte",
    "éclat de vitre",
    "éclat de tasse",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
    "grain de miette",
    "grain de sable",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de crayon",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_dessiner_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="chanson",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_attend_la_fin_de_la_phrase; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="tasse",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_attend_puis_on_l_entend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="gouttière",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_sur_la_feuille; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de crayon",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_ligne; "
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
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
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
    "narrateur|La maison boit la pluie par la gouttière.",
    "narrateur|Une goutte glisse sur la vitre de la cuisine.",
    "narrateur|La vapeur du cacao fait un petit nuage.",
    "papa|La gouttière fait une vraie chanson, Aniss.",
    "maman|Tes bottes jaunes attendent près de la flaque.",
    "narrateur|Une petite flaque brille sous la fenêtre.",
    "narrateur|Papa range les cuillères dans le tiroir.",
    "narrateur|Maman essuie la table en bois.",
    "narrateur|Le bois reste un peu humide sous le torchon.",
    "narrateur|Sur le rebord, le crayon jaune attend.",
    "narrateur|Sur le bois lisse, un éclat de crayon brille.",
    "enfant-m|Il est petit, papa.",
    "papa|C'est la pluie sur le jaune.",
    "narrateur|Le crayon sent le bois, un peu froid.",
    "enfant-m|Je dessine la gouttière, maintenant !",
    "maman|Pendant que je finis la table ?",
    "enfant-m|Oui, tout de suite !",
    "narrateur|En ce moment, Aniss saisit le crayon.",
    "narrateur|Le bois est lisse sous ses doigts.",
    "narrateur|Papa parle à maman, près du tiroir.",
    "papa|Le cartable est près de la porte.",
    "maman|Oui, avec le capuchon.",
    "enfant-m|Papa, la gouttière !",
    "narrateur|Les mots d'Aniss se cognent aux leurs.",
    "narrateur|Personne ne tourne la tête.",
    "papa|Tu disais quelque chose, Aniss ?",
    "enfant-m|La chanson va partir.",
    "narrateur|Aniss pose une feuille trop vite.",
    "narrateur|Le papier boit une goutte de la table.",
    "narrateur|Le crayon glisse.",
    "narrateur|La ligne jaune part de travers.",
    "enfant-m|Oh.",
    "narrateur|L'éclat de crayon tremble, puis tient.",
    "narrateur|Le sourire d'Aniss disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "enfant-m|Ça ne veut pas, maman.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Papa se baisse à sa hauteur.",
    "papa|Le crayon va dans le cartable ?",
    "enfant-m|Oui, papa.",
    "narrateur|Aniss glisse le crayon dans la poche.",
    "narrateur|Le cartable sent le papier.",
    "papa|On enfile les bottes ?",
    "enfant-m|Oui.",
    "narrateur|La botte gauche est froide, un peu lisse.",
    "enfant-m|Elle colle, maman.",
    "maman|Tire vers toi.",
    "narrateur|La botte droite entre, plus facile.",
    "papa|On y va ?",
    "enfant-m|On y va.",
    "enfant-m|Au revoir, maman.",
    "maman|Au revoir, Aniss.",
    "narrateur|Dehors, la rue brille sous les gouttes.",
    "narrateur|Les gouttes tapent le capuchon.",
    "narrateur|L'école sent le savon et le bois des casiers.",
    "narrateur|Un carré d'eau coule sur la vitre de la classe.",
    "narrateur|La maîtresse parle près du tableau.",
    "maitresse|Bonjour les enfants.",
    "enfant-m|Bonjour, maîtresse.",
    "enfant-m|La gouttière, elle chante !",
    "narrateur|Ses mots se cognent à ceux de la classe.",
    "narrateur|Personne ne comprend la chanson.",
    "narrateur|Aniss referme la bouche.",
    "narrateur|Il serre le crayon dans sa poche.",
    "narrateur|Le soir, la gouttière reprend sa chanson.",
    "narrateur|La porte s'ouvre.",
    "narrateur|Ça sent le cacao.",
    "papa|Te voilà, Aniss.",
    "papa|Tes bottes sont mouillées.",
    "maman|Viens près de la tasse.",
    "narrateur|Aniss pose les bottes près de la flaque.",
    "narrateur|Il s'assoit.",
    "narrateur|Le ventre est serré, tout petit.",
    "narrateur|Il regarde papa.",
    "narrateur|Il ouvre la bouche.",
]

Q0001 = [
    "narrateur|Aniss veut dire la chanson.",
    "narrateur|Que fait-il ?",
]

C0001 = [
    "narrateur|Aniss ouvre la bouche trop vite.",
    "enfant-m|Papa, la gouttière.",
    "narrateur|Papa n'a pas fini sa phrase.",
    "papa|Le cacao est chaud, Aniss.",
    "narrateur|Les deux voix se mélangent.",
    "enfant-m|Oh.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Aniss refuse de foncer.",
    "narrateur|Il referme la bouche.",
    "narrateur|Il pose les mains à plat.",
    "narrateur|Il écoute la cuisine, un instant.",
    "papa|Tes bottes sèchent près de la porte.",
    "narrateur|Papa pose sa tasse.",
    "maman|Le cacao fume un peu.",
    "narrateur|Maman n'a pas fini non plus.",
    "narrateur|Aniss attend que le silence arrive.",
    "narrateur|Sur le rebord, l'éclat de crayon brille.",
    "enfant-m|Il est là.",
    "enfant-m|Je peux te montrer quelque chose ?",
    "maman|Oui, nous t'écoutons.",
    "enfant-m|La gouttière chante sur le toit.",
    "enfant-m|Mon crayon a vu la pluie.",
    "papa|Merci, Aniss.",
    "narrateur|Papa a entendu toute la phrase.",
    "maman|Tu as fini ta tasse ?",
    "enfant-m|Presque, maman.",
    "narrateur|Le ventre d'Aniss se desserre.",
]

END = [
    "narrateur|Aniss sort le crayon jaune du cartable.",
    "narrateur|Le bois est froid, un peu lisse.",
    "enfant-m|Je dessine la gouttière.",
    "papa|Tu lui fais une place sur la feuille ?",
    "enfant-m|Oui.",
    "enfant-m|Ici, au milieu.",
    "narrateur|Aniss veut tracer tout de suite.",
    "narrateur|Il appuie trop fort.",
    "narrateur|Le papier se plisse.",
    "enfant-m|Oh.",
    "narrateur|Aniss s'arrête.",
    "narrateur|Ses mains se ferment, puis s'ouvrent.",
    "narrateur|Il refuse de foncer.",
    "narrateur|Il écoute la gouttière, un instant.",
    "narrateur|Il reprend le crayon, plus léger.",
    "narrateur|Une ligne jaune descend, comme l'eau.",
    "maman|On entend presque la chanson.",
    "narrateur|Aniss ajoute une petite flaque ronde.",
    "papa|Et les bottes, à côté ?",
    "enfant-m|Deux bottes jaunes.",
    "narrateur|Il souffle sur la feuille.",
    "enfant-m|Fffff.",
    "narrateur|La pluie ralentit derrière la vitre.",
]

FIN = [
    "narrateur|Les bottes sèchent près de la porte.",
    "narrateur|La feuille jaune reste sur la table.",
    "enfant-m|Comme sur le rebord, papa !",
    "papa|Tu le vois, toi ?",
    "enfant-m|Oui, sur le jaune.",
    "maman|On est bien, ici.",
    "narrateur|Le cacao fume un peu, près de la fenêtre.",
    "narrateur|Aniss glisse le crayon sans se presser.",
    "narrateur|Le bois repose contre la feuille.",
    "enfant-m|On l'entend, maman.",
    "maman|Tu l'entends sur le papier ?",
    "enfant-m|Oui, la chanson.",
    "narrateur|La pluie reste dans l'air.",
    "narrateur|L'éclat de crayon tient sur la ligne.",
]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    wanted = {
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_Q0001",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    }
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in wanted]
    if missing:
        raise SystemExit(f"{SID} chunks inattendus: {missing}")

    by = {
        "CHK_T0000_P0000": voice(
            by_src["CHK_T0000_P0000"], P0000, "opening", "pluie,porte",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "il attend",
                    "accepted_examples": (
                        "il attend | attendre | son tour | il écoute "
                        "| il attend son tour | attendre la fin"
                    ),
                    "retry_prompt": (
                        "Papa n'a pas fini sa phrase. Que fait Aniss ?"
                    ),
                    "engine_ok_text": "Oui, il attend.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "tasse,cacao",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "crayon,papier",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "gouttiere,pluie",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "éclat de crayon" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de crayon" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count("éclat de crayon")
    if n_clue != 4:
        raise SystemExit(f"{SID}: éclat de crayon ×{n_clue} (voulu 4)")
    if not all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in chunks):
        raise SystemExit(f"{SID}: TTS incomplet")
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
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** COL.ECO.001 — écouter / attendre son tour "
        "(vécue : couper → mots perdus ; attendre la tasse → phrase entendue)\n"
        "- **Personnages :** Aniss, papa, maman, maîtresse\n"
        "- **Lieu :** cuisine sous la pluie, école, puis table du soir\n"
        "- **Indice unique :** éclat de crayon (bois lisse au rebord → "
        "ligne jaune du soir)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La maison boit la pluie par la gouttière. Un nuage de cacao contre "
        "la vitre. Sur le crayon jaune, un éclat de crayon brille. Aniss "
        "veut dessiner la chanson **maintenant**. Il coupe papa : les mots "
        "se cognent, personne n'entend. Première idée : poser la feuille "
        "trop vite. Le papier boit une goutte, la ligne part de travers. "
        "Sourire parti, épaules basses. Papa se baisse. À l'école, il parle "
        "pendant la classe : la chanson se perd. Le soir, il ouvre la "
        "bouche trop vite : les voix se mélangent. Il refuse de foncer, "
        "attend la tasse, dit la chanson. Merci vécu. Il appuie trop fort "
        "sur la feuille, s'arrête, écoute, trace. Sur la ligne, l'éclat "
        "tient.\n\n"
        "## Vécu\n\n"
        "Aniss veut la gouttière **maintenant**. Impatience, puis épaules "
        "qui tombent quand personne n'entend. Papa se baisse, pose une "
        "question, ne récite pas la règle. Aniss agit : bouche fermée, "
        "mains à plat, phrase entière. Merci vécu après l'écoute. Fin : "
        "l'éclat du début tient sur la ligne.\n\n"
        "## Vu et corrigé\n\n"
        "- Ouverture inventée (maison qui boit la pluie, cacao, éclat), "
        "pas « joue au salon ».\n"
        "- Monde du dump (cuisine sous la pluie, école, table du soir, "
        "crayon jaune, bottes, gouttière), distinct de AUT.ROU (allée, "
        "wagon) et AUT.RAN (nappe, cubes).\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés. Pas de "
        "merle.\n"
        "- Leçon non dite : on l'entend quand il attend la fin. Pas de "
        "morale, pas « il faut attendre », pas « on écoute la maîtresse ».\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive.\n"
        "- N2 ≤ 15. `check()` OK. Pas apply.\n\n"
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
