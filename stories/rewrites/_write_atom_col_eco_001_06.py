#!/usr/bin/env python3
"""ATOM-COL.ECO.001-06 — F-NAR-019. Les moufles de Nina. N2. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.001-06"
N2 = 15
TITLE = "Les moufles de Nina"
FIL = (
    "Sur le pouce, un éclat de moufle brille. Nina veut les moufles, "
    "maintenant. Elle tire trop vite : une moufle tombe. À l'école, un "
    "camarade veut le secret tout de suite. Elle coupe la classe : les "
    "mots se perdent. Le soir, elle ouvre la bouche trop vite. Elle "
    "refuse de foncer, attend, raconte. Merci vécu. L'éclat de moufle "
    "tient sur le pouce."
)
CHARS = "Nina, papa, maman"
SETTING = "entrée d'hiver, école, soupe du soir"
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
    "xavier",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "tu ranges",
    "une étape après",
    "il faut attendre",
    "on doit demander",
    "on aime écouter",
    "si tu as un malaise",
    "tu as bien fait de raconter",
    "éclat de laine",
    "éclat de wagon",
    "éclat de bec",
    "éclat de marche",
    "éclat de fraise",
    "éclat de quille",
    "éclat de lampe",
    "éclat de citron",
    "éclat de nappe",
    "éclat de caisse",
    "éclat de boîte",
    "éclat de boite",
    "éclat de farine",
    "éclat d'ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
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
        emphasis="éclat de moufle",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_les_moufles_maintenant; "
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
            "sous_texte=elle_attend_puis_raconte; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="secret",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_attend_puis_on_l_entend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de moufle",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis prudence; intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de moufle",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_pouce; "
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
    starts: list[str] = []
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
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad!r}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"interdit {bad!r}: {ph}")
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
    "narrateur|La fenêtre tremble contre le bois.",
    "narrateur|Dehors, le froid pique les vitres.",
    "narrateur|Dans l'entrée, un petit nuage blanc s'élève.",
    "narrateur|Les moufles sèchent sur le radiateur.",
    "narrateur|La laine sent le froid de la rue.",
    "narrateur|Sur le pouce, un éclat de moufle brille.",
    "enfant-f|Il est petit, maman.",
    "maman|C'est le chaud qui revient.",
    "papa|Le cartable est contre le mur.",
    "narrateur|Papa pose le cartable, bien droit.",
    "narrateur|Maman boutonne le manteau, une, deux, trois.",
    "narrateur|Ça sent la soupe, dans la casserole.",
    "enfant-f|Les moufles, maintenant !",
    "maman|Elles fument un peu, Nina.",
    "enfant-f|Je les prends !",
    "narrateur|En ce moment, Nina saisit les deux moufles.",
    "narrateur|La laine reste humide, un peu lourde.",
    "narrateur|Elle tire trop vite.",
    "narrateur|Une moufle glisse, tombe.",
    "narrateur|L'éclat de moufle tremble, puis tient.",
    "enfant-f|Oh.",
    "narrateur|Le sourire de Nina disparaît.",
    "narrateur|Dans sa poitrine, envie et inquiétude se bousculent.",
    "enfant-f|Ça ne veut pas.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Papa se baisse à sa hauteur.",
    "papa|Tu veux les mains au chaud ?",
    "enfant-f|Oui, papa.",
    "maman|On les met dehors, d'accord ?",
    "enfant-f|D'accord.",
    "narrateur|Nina enfile les moufles, plus lente.",
    "narrateur|La laine colle un peu aux doigts.",
    "papa|Le bouton du haut ?",
    "enfant-f|Fermé.",
    "narrateur|Dehors, l'air pique le nez.",
    "narrateur|Les pas sonnent sur les cailloux gelés.",
    "narrateur|Papa tient sa main.",
    "narrateur|L'école est plus chaude que la rue.",
    "narrateur|Ça sent les manteaux mouillés, près des crochets.",
    "narrateur|Nina pose le cartable contre le casier.",
    "narrateur|La classe pose une histoire, près du tableau.",
    "narrateur|Nina écoute, les mains sur la table.",
    "narrateur|Un camarade s'approche.",
    "copain|Regarde, maintenant.",
    "copain|C'est un secret.",
    "narrateur|Il parle trop près de son oreille.",
    "narrateur|Nina veut écouter la classe.",
    "narrateur|Le camarade veut le secret, maintenant.",
    "narrateur|Nina sent un malaise.",
    "narrateur|Son ventre se serre.",
    "enfant-f|Je le dis, maintenant !",
    "narrateur|Elle ouvre la bouche trop vite.",
    "narrateur|Ses mots se cognent à ceux de la classe.",
    "narrateur|Personne ne tourne la tête.",
    "enfant-f|Oh.",
    "narrateur|Nina referme la bouche.",
    "narrateur|Elle garde les mains sur la table.",
    "narrateur|Le soir, la porte s'ouvre.",
    "narrateur|Le manteau est lourd de froid.",
    "maman|Te voilà, Nina.",
    "papa|Les moufles sont sèches, sur le radiateur.",
    "narrateur|Le petit nuage n'est plus là.",
    "narrateur|Nina pose les moufles près du métal.",
    "narrateur|Elle ouvre la bouche.",
]

Q0001 = [
    "narrateur|Nina a un malaise.",
    "narrateur|Que fait-elle ?",
]

C0001 = [
    "narrateur|Nina ouvre la bouche trop vite.",
    "enfant-f|Maman, un secret.",
    "narrateur|Maman n'a pas fini sa phrase.",
    "maman|Le manteau est lourd, Nina.",
    "narrateur|Les deux voix se mélangent.",
    "enfant-f|Oh.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Nina refuse de foncer.",
    "narrateur|Elle referme la bouche.",
    "narrateur|Elle pose les mains à plat.",
    "narrateur|Elle écoute l'entrée, un instant.",
    "papa|Les moufles sèchent près du radiateur.",
    "narrateur|Papa pose le cartable contre le mur.",
    "maman|La soupe fume un peu.",
    "narrateur|Maman n'a pas fini non plus.",
    "narrateur|Nina attend que le silence arrive.",
    "narrateur|Sur le pouce, l'éclat de moufle brille.",
    "enfant-f|Il est là.",
    "enfant-f|Je peux te dire quelque chose ?",
    "maman|Oui, nous t'écoutons.",
    "enfant-f|Un camarade a parlé d'un secret.",
    "enfant-f|Mon ventre s'est serré.",
    "papa|Merci, Nina.",
    "narrateur|Papa a entendu toute la phrase.",
    "maman|Tu veux ta soupe ?",
    "enfant-f|Oui, maman.",
    "narrateur|Le ventre de Nina se desserre.",
]

END = [
    "narrateur|Nina veut tout dire, d'un coup.",
    "narrateur|Elle prend la cuillère et les moufles.",
    "narrateur|La cuillère tape le bol.",
    "narrateur|Une moufle glisse vers le sol.",
    "enfant-f|Ça tombe !",
    "narrateur|Nina veut foncer, d'un coup.",
    "narrateur|Nina refuse de foncer.",
    "narrateur|Ses épaules se serrent un peu.",
    "narrateur|Ça tape, dans sa poitrine.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Elle regarde les moufles.",
    "narrateur|Elle écoute le radiateur, un instant.",
    "narrateur|Le métal fait un petit bruit.",
    "narrateur|Sur le pouce, l'éclat de moufle brille.",
    "enfant-f|Comme ce matin !",
    "papa|Tu le vois, toi ?",
    "enfant-f|Oui, sur cette laine.",
    "narrateur|Nina pose la cuillère, d'abord.",
    "narrateur|Puis elle glisse les moufles au chaud.",
    "maman|La soupe, Nina ?",
    "enfant-f|Oui.",
    "narrateur|Elle s'assoit.",
    "narrateur|Le bol est lisse, un peu lourd.",
    "narrateur|Elle boit une gorgée.",
    "narrateur|La soupe est tiède.",
]

FIN = [
    "narrateur|Les moufles reposent sur le radiateur.",
    "narrateur|Le petit nuage n'est plus là.",
    "enfant-f|L'éclat est là, papa.",
    "papa|Tu le vois sur le pouce ?",
    "enfant-f|Oui, papa.",
    "maman|On est bien, ici.",
    "narrateur|La soupe fume un peu, près de la fenêtre.",
    "narrateur|La fenêtre tremble moins.",
    "enfant-f|J'ai dit le secret.",
    "maman|On t'a entendue, Nina.",
    "enfant-f|Oui, maman.",
    "narrateur|Nina pose la joue près de la laine.",
    "narrateur|La laine est tiède, un peu rêche.",
    "enfant-f|C'est chaud.",
    "narrateur|Dehors, le froid reste sur les cailloux.",
    "narrateur|L'éclat de moufle tient sur le pouce.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "radiateur,laine",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "raconter",
                    "accepted_examples": (
                        "raconter | elle raconte | à maman | à la maison | "
                        "écouter"
                    ),
                    "retry_prompt": "Elle raconte à maman. Que fait Nina ?",
                    "engine_ok_text": "Oui, elle raconte.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "soupe,moufles",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "obstacle", "cuillere,bol",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "radiateur,laine",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "éclat de moufle" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de moufle" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count("éclat de moufle")
    if n_clue != 5:
        raise SystemExit(f"{SID}: éclat de moufle ×{n_clue} (voulu 5)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "xavier" in blob:
        raise SystemExit(f"{SID}: Xavier interdit")
    if "éclat de laine" in blob:
        raise SystemExit(f"{SID}: BAN éclat de laine")
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
        "- **Leçon :** COL.ECO.001 — attendre / écouter / raconter "
        "(vécue : couper la classe → mots perdus ; attendre le silence "
        "→ phrase entendue)\n"
        "- **Personnages :** Nina, papa, maman. Maîtresse = label dump, "
        "pas de leçon récitée. Troupe D16.\n"
        "- **Lieu :** entrée d'hiver, école, soupe du soir\n"
        "- **Indice unique :** éclat de moufle (pouce du matin → pouce "
        "du soir sur le radiateur)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La fenêtre tremble. Un nuage blanc s'élève dans l'entrée. Sur le "
        "pouce, un éclat de moufle brille. Nina veut les moufles "
        "**maintenant**. Première idée : les prendre d'un coup. Une moufle "
        "tombe, laine humide. Sourire parti, épaules basses. Papa se baisse. "
        "À l'école, un camarade veut le secret tout de suite ; Nina veut "
        "écouter. Elle coupe : les mots se perdent. Le soir, elle ouvre la "
        "bouche trop vite : les voix se mélangent. Elle refuse de foncer, "
        "attend, raconte. Merci vécu. Cuillère et moufles d'un coup : ça "
        "tombe. Elle refuse, retrouve l'éclat. L'éclat de moufle tient "
        "sur le pouce.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : entrée d'hiver, radiateur, laine, fenêtre qui tremble, "
        "cartable contre le mur, froid dehors, école, soupe.\n"
        "- Désir : les moufles chaudes, maintenant.\n"
        "- Objet : moufles, laine, cartable, bol de soupe.\n"
        "- Indice unique : éclat de moufle, vu dès l'ouverture, payé à la fin.\n"
        "- Urgence douce : le froid pique derrière la vitre.\n"
        "- Imprévu 1 : elle tire trop vite ; une moufle tombe. À l'école, "
        "elle coupe la classe.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : tout dire et tout prendre d'un coup ; "
        "cuillère et moufle tombent.\n"
        "- Résolution : elle refuse de foncer, attend, raconte le secret.\n"
        "- Retour : joue près de la laine, éclat du début sur le pouce.\n\n"
        "## Vécu\n\n"
        "Nina veut les moufles **maintenant**. Impatience, puis sourire qui "
        "disparaît. Un camarade veut le secret tout de suite ; elle veut "
        "écouter. Papa se baisse, pose une question, ne récite pas la "
        "règle. Nina agit : bouche fermée, mains à plat, phrase entière. "
        "Merci vécu après l'écoute. Fin : l'éclat du début tient sur le "
        "pouce.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump (entrée d'hiver, école, "
        "soupe du soir, moufles, laine, fenêtre, cartable, froid). "
        "≠ COL.ECO.001-01 gouttière/crayon.\n"
        "- Xavier retiré (dump INTERDIT). Relance au féminin.\n"
        "- Ouverture inventée (fenêtre qui tremble, nuage blanc), pas un "
        "gabarit v2, pas « Nina joue au salon ».\n"
        "- Indice unique : éclat de moufle. Pas éclat de laine "
        "(BAN RAN.001-06).\n"
        "- Maîtresse : label dump seulement, pas de leçon récitée, pas de "
        "réplique « on range / vous avez bien écouté / si malaise ».\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : on l'entend quand elle attend, puis raconte. "
        "Pas de morale, pas « on écoute la maîtresse ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Nina a un malaise. Que fait-elle ? ». "
        "5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle plus tendu à la cuillère.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
