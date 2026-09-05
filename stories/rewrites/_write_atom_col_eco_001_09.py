#!/usr/bin/env python3
"""ATOM-COL.ECO.001-09 — Le pinceau jaune de Victorina (F-NAR-019, N3)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.001-09"
N3 = 16
TITLE = "Le pinceau jaune de Victorina"
FIL = (
    "Le préau sent la laine mouillée. Sur le pinceau jaune, un "
    "éclat de pinceau brille. Victorina veut peindre les manteaux, "
    "maintenant. Elle plonge trop vite : le jaune court. Elle veut "
    "parler maintenant : les mots se perdent. Elle refuse de foncer, "
    "attend le silence, raconte. Merci vécu. Sur le jaune, l'éclat "
    "de pinceau tient."
)
CHARS = "Victorina, papa, maman, maîtresse"
SETTING = "école, atelier peinture, puis maison"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent", "tout bas")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)
PINCE_BAD = re.compile(r"éclat de pince(?!au)", re.I)
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
    "on aime écouter",
    "on aime ecouter",
    "tu as bien écouté",
    "tu as bien ecoute",
    "on écoute d'abord",
    "on ecoute d'abord",
    "tu as bien fait de raconter",
    "si tu as un malaise",
    "denis",
    "cartable",
    "casserole",
    "crayon",
    "buée",
    "buee",
    "croûte",
    "croute",
    "tableau",
    "casier",
    "moufle",
    "craie",
    "éclat de nappe",
    "éclat de wagon",
    "éclat de casserole",
    "éclat de goutte",
    "éclat de vitre",
    "éclat de tasse",
    "éclat de crayon",
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
        emphasis="éclat de pinceau",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_peindre_et_parler_maintenant; "
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
            "sous_texte=elle_raconte_quand_le_ventre_serre; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="silence",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_attend_puis_on_l_entend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="pinceau",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_sur_la_feuille; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de pinceau",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_jaune; "
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
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
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
        if PINCE_BAD.search(low):
            raise SystemExit(f"interdit éclat de pince: {ph}")
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad!r}: {ph}")
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
    "narrateur|Victorina connaît le préau, ses crochets, son zinc.",
    "narrateur|Après la pluie, un détail paraît nouveau.",
    "narrateur|Les manteaux jaunes gouttent sur les crochets.",
    "narrateur|Ça sent la laine mouillée, un peu froide.",
    "narrateur|Une goutte tombe de la gouttière de l'école.",
    "papa|Le zinc fait un petit chant, tu l'entends ?",
    "enfant-f|Oui, papa.",
    "enfant-f|Il tombe près des manteaux.",
    "maman|Tes cheveux sont prêts, Victorina.",
    "enfant-f|Oui, maman.",
    "narrateur|Maman boutonne le manteau jaune.",
    "narrateur|Le tissu est lourd, un peu froid.",
    "maman|Le manteau jaune est boutonné ?",
    "enfant-f|Oui, maman.",
    "narrateur|Maman glisse un biscuit dans la poche.",
    "narrateur|Le biscuit sent le beurre.",
    "maman|Il est pour plus tard.",
    "enfant-f|Je peins les manteaux, maintenant !",
    "papa|À l'atelier, près des pots ?",
    "enfant-f|Oui, tout de suite !",
    "papa|On y va ?",
    "enfant-f|On y va.",
    "enfant-f|Au revoir, maman.",
    "maman|Au revoir, Victorina.",
    "narrateur|Le préau brille sous les gouttes.",
    "narrateur|Les crochets claquent un peu.",
    "narrateur|En ce moment, Victorina pousse la porte de l'atelier.",
    "narrateur|Ça sent le papier mouillé et l'eau des pots.",
    "narrateur|La nappe de la table est bleue, un peu tâchée.",
    "narrateur|Les pots jaunes sont ouverts.",
    "narrateur|Un pinceau jaune attend près de l'eau.",
    "narrateur|Sur le bois mouillé, un éclat de pinceau brille.",
    "enfant-f|Le bois brille, maîtresse.",
    "maitresse|Bonjour les enfants.",
    "enfant-f|Bonjour, maîtresse.",
    "narrateur|La maîtresse parle près des pots.",
    "narrateur|Victorina saisit le pinceau jaune.",
    "narrateur|Le bois est lisse, un peu collant.",
    "narrateur|Elle plonge le poil trop vite.",
    "narrateur|L'eau gicle sur la nappe.",
    "narrateur|Le jaune court de travers.",
    "enfant-f|Oh.",
    "narrateur|L'éclat de pinceau tremble, puis tient.",
    "narrateur|Le sourire de Victorina disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "enfant-f|Ça ne veut pas.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Elle essuie la nappe avec un chiffon.",
    "narrateur|Elle reprend le pinceau, plus léger.",
    "narrateur|Une tache jaune ronde tient sur la feuille.",
    "enfant-f|C'est le manteau, maîtresse.",
    "maitresse|Oui, Victorina.",
    "narrateur|Victorina va vers le bac.",
    "narrateur|L'eau du bac devient un peu jaune.",
    "narrateur|Elle lave le poil, sans se presser.",
    "narrateur|Près du bac, quelqu'un chuchote.",
    "narrateur|Victorina entend parler d'un secret.",
    "narrateur|Son ventre se serre.",
    "narrateur|Ses joues deviennent chaudes.",
    "enfant-f|Je le dis, maintenant !",
    "narrateur|Elle ouvre la bouche trop vite.",
    "narrateur|Ses mots se cognent à ceux de l'atelier.",
    "narrateur|Personne ne tourne la tête.",
    "enfant-f|Oh.",
    "narrateur|Elle referme la bouche.",
    "narrateur|Elle pose le pinceau propre.",
    "narrateur|Elle glisse la feuille dans la poche du manteau.",
    "narrateur|Le soir, la porte de la maison s'ouvre.",
    "narrateur|Ça sent le lait chaud et le pain.",
    "narrateur|Le manteau jaune pend sur la chaise.",
    "papa|Te voilà, Victorina.",
    "papa|Tes manches sont un peu mouillées.",
    "maman|Viens près de la table.",
    "narrateur|Victorina pose le biscuit sur le bois.",
    "narrateur|Elle s'assoit.",
    "narrateur|Le ventre est serré, tout petit.",
    "narrateur|Elle regarde papa.",
    "narrateur|Elle ouvre la bouche.",
]

Q0001 = [
    "narrateur|Victorina a un malaise.",
    "narrateur|Que fait-elle ?",
]

C0001 = [
    "narrateur|Victorina ouvre la bouche trop vite.",
    "enfant-f|Papa, quelqu'un a parlé.",
    "narrateur|Papa n'a pas fini sa phrase.",
    "papa|Le lait est chaud, Victorina.",
    "narrateur|Les deux voix se mélangent.",
    "enfant-f|Oh.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Papa se baisse à sa hauteur.",
    "narrateur|Victorina refuse de foncer.",
    "narrateur|Elle referme la bouche.",
    "narrateur|Elle pose les mains à plat.",
    "narrateur|Elle écoute la cuisine, un instant.",
    "papa|Tes manches sèchent sur la chaise ?",
    "narrateur|Papa pose son bol.",
    "maman|Le lait fume un peu.",
    "narrateur|Maman n'a pas fini non plus.",
    "narrateur|Victorina attend que le silence arrive.",
    "narrateur|Sur la feuille, un éclat de pinceau brille.",
    "enfant-f|Il est là.",
    "enfant-f|Je peux te dire quelque chose ?",
    "maman|Oui, nous t'écoutons.",
    "enfant-f|Quelqu'un a parlé d'un secret.",
    "enfant-f|Mon ventre s'est serré, à l'atelier.",
    "papa|Merci, Victorina.",
    "narrateur|Papa a entendu toute la phrase.",
    "maman|Tu as fini ton lait ?",
    "enfant-f|Presque, maman.",
    "narrateur|Le ventre de Victorina se desserre.",
]

END = [
    "narrateur|Victorina sort la feuille de la poche.",
    "narrateur|Le papier est un peu gondolé.",
    "maman|Le pinceau de la boîte est là.",
    "narrateur|Maman pose un verre d'eau sur le bois.",
    "narrateur|Un petit pinceau attend dans le verre.",
    "enfant-f|Je peins les manteaux.",
    "papa|Tu leur fais une place sur la feuille ?",
    "enfant-f|Oui.",
    "enfant-f|Ici, au milieu.",
    "narrateur|Victorina veut tracer tout de suite.",
    "narrateur|Elle appuie trop fort.",
    "narrateur|Le jaune court de travers.",
    "enfant-f|Oh.",
    "narrateur|Elle s'arrête.",
    "narrateur|Ses mains se ferment, puis s'ouvrent.",
    "narrateur|Elle refuse de foncer.",
    "narrateur|Elle écoute la pluie, un instant.",
    "narrateur|Elle reprend le pinceau, plus léger.",
    "narrateur|Une ligne jaune descend, comme un manteau.",
    "maman|On voit presque les crochets.",
    "narrateur|Victorina ajoute une petite poche ronde.",
    "papa|Et le biscuit, dedans ?",
    "enfant-f|Un biscuit, oui.",
    "narrateur|Elle souffle sur la feuille.",
    "enfant-f|Fffff.",
    "narrateur|La pluie ralentit derrière la vitre.",
]

FIN = [
    "narrateur|Le manteau jaune sèche sur la chaise.",
    "narrateur|La feuille jaune reste sur la table.",
    "enfant-f|Comme à l'atelier, papa !",
    "papa|Tu le vois, toi ?",
    "enfant-f|Oui, sur le jaune.",
    "maman|On est bien, ici.",
    "narrateur|Le lait fume un peu, près de la fenêtre.",
    "narrateur|Victorina glisse le pinceau sans se presser.",
    "narrateur|Le bois repose contre la feuille.",
    "enfant-f|Il brille, maman.",
    "maman|Tu le vois sur le papier ?",
    "enfant-f|Oui, sur le jaune.",
    "narrateur|La pluie reste dans l'air.",
    "narrateur|L'éclat de pinceau tient sur le jaune.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "pluie,eau",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "raconter",
                    "accepted_examples": (
                        "raconter | elle raconte | à papa | à la maison | écouter"
                    ),
                    "retry_prompt": (
                        "Elle raconte à papa. Que fait Victorina ?"
                    ),
                    "engine_ok_text": "Oui, elle raconte.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "verre",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "pluie",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "éclat de pinceau" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de pinceau" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count("éclat de pinceau")
    if n_clue != 4:
        raise SystemExit(f"{SID}: éclat de pinceau ×{n_clue} (voulu 4)")
    if PINCE_BAD.search(blob):
        raise SystemExit(f"{SID}: éclat de pince (sans au)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "denis" in blob:
        raise SystemExit(f"{SID}: Denis resté")
    if "on aime écouter" in blob or "on aime ecouter" in blob:
        raise SystemExit(f"{SID}: gabarit maîtresse")
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
    if blob.count("merci") != 1:
        raise SystemExit(f"{SID}: merci total ×{blob.count('merci')}")
    q = by["CHK_T0000_P0000_Q0001"]
    if "denis" in (q.get("retry_prompt") or "").lower():
        raise SystemExit(f"{SID}: retry Denis")
    if "victorina" not in (q.get("retry_prompt") or "").lower():
        raise SystemExit(f"{SID}: retry sans Victorina")

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
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** COL.ECO.001 — écouter / raconter un malaise à la "
        "maison (vécue : couper → mots perdus ; attendre le silence → "
        "phrase entendue)\n"
        "- **Personnages :** Victorina, papa, maman, maîtresse (label, "
        "pas de leçon parlée)\n"
        "- **Lieu :** école, atelier peinture, puis maison (préau, "
        "manteaux jaunes, gouttière de l'école = détail du lieu, pas "
        "l'indice)\n"
        "- **Indice unique :** éclat de pinceau (bois mouillé de "
        "l'atelier → jaune de la feuille du soir)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Victorina connaît le préau. Après la pluie, un détail paraît "
        "nouveau. Les manteaux jaunes gouttent. Une goutte tombe de la "
        "gouttière de l'école (lieu, pas l'indice). À l'atelier, sur le "
        "pinceau jaune, un éclat de pinceau brille. Elle veut peindre les "
        "manteaux **maintenant**. Première idée : elle plonge trop vite, "
        "le jaune court, le sourire part. Près du bac, un chuchotement. "
        "Ventre serré. Elle veut parler **maintenant** : les mots se "
        "cognent, personne n'entend. Le soir, elle coupe papa : les voix "
        "se mélangent. Elle refuse de foncer, attend le silence, raconte. "
        "Merci vécu. Elle appuie trop fort sur la feuille, s'arrête, "
        "écoute, trace. Sur le jaune, l'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : préau mouillé, manteaux jaunes, zinc, atelier à la "
        "nappe bleue, maison au lait.\n"
        "- Désir : peindre les manteaux, et parler, maintenant.\n"
        "- Objet : pinceau jaune, feuille, biscuit, manteau.\n"
        "- Indice unique : éclat de pinceau, vu dès l'ouverture, payé "
        "au climax.\n"
        "- Urgence douce : le jaune et les mots, tout de suite.\n"
        "- Imprévu 1 : trop vite dans l'eau, puis trop vite la bouche.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après la phrase entière.\n"
        "- Imprévu 2 (plus rusé) : elle appuie trop fort, le jaune court.\n"
        "- Résolution : elle refuse de foncer, écoute la pluie, reprend "
        "plus léger.\n"
        "- Retour : l'éclat de pinceau tient sur le jaune.\n\n"
        "## Vécu\n\n"
        "Victorina veut le jaune **maintenant**, puis les mots "
        "**maintenant**. Impatience, puis épaules qui tombent quand "
        "personne n'entend. Papa se baisse, pose une question, ne "
        "récite pas la règle. Victorina agit : bouche fermée, mains à "
        "plat, phrase entière. Merci vécu après l'écoute. Fin : l'éclat "
        "du début tient sur le jaune.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre dump « Le soleil sur la buée » → « Le pinceau jaune de "
        "Victorina ». Denis du SSML dump retiré. Retry : Victorina.\n"
        "- Ouverture inventée (préau, manteaux, zinc, éclat), pas "
        "casserole / buée / « joue au salon ».\n"
        "- Monde du dump (école, atelier peinture, puis maison), "
        "distinct de 001-01 (gouttière/crayon) et 001-02..08 "
        "(rayon, pain, linge, chaussette, moufles, craie, cartable).\n"
        "- Gouttière de l'école = détail du lieu, pas l'indice.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout bas » "
        "retirés. Pas de merle.\n"
        "- Leçon non dite : on l'entend quand elle attend le silence. "
        "Pas de morale, pas « On aime écouter la maîtresse ». Maîtresse "
        "= label (bonjour), pas de leçon parlée.\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- Ban : cartable, casserole, crayon, buée, croûte, tableau, "
        "casier, moufle, craie. Pas éclat de pince.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive.\n"
        "- N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
