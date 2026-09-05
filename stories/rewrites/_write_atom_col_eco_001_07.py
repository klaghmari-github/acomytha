#!/usr/bin/env python3
"""ATOM-COL.ECO.001-07 — F-NAR-019. La craie d'Amir. N2. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.001-07"
N2 = 15
TITLE = "La craie d'Amir"
FIL = (
    "La craie d'hier poudre le pas de la porte. Sur la pierre, un éclat "
    "de craie brille. Amir veut la garder, maintenant. Il la saisit trop "
    "vite : elle casse, la poudre pique. À l'école, une voix parle d'un "
    "secret. Il veut le dire tout de suite : les mots se perdent. Il "
    "refuse de foncer, raconte le soir. Merci vécu. Sur la pierre, "
    "l'éclat de craie tient."
)
CHARS = "Amir, papa, maman"
SETTING = "école puis maison, pas de la porte, platane du village"
TIC_PHRASES = (
    "tout doux",
    "tout calme",
    "tout lent",
    "tout bas",
    "tout doucement",
)
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
    "ninon",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "on range les feutres",
    "tu ranges",
    "tu as bien écouté",
    "tu as bien ecoute",
    "on aime écouter",
    "on aime ecouter",
    "écoute la maîtresse",
    "ecoute la maitresse",
    "tu as bien fait",
    "bon travail",
    "une chose, puis",
    "une chose puis",
    "il faut attendre",
    "on doit demander",
    "gouttière",
    "gouttiere",
    "chaussette",
    "moufle",
    "grain de miette",
    "grain de sable",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "grain de pomme",
    "grain de carotte",
    "grain de lavande",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de marche",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de tasse",
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de farine",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de laine",
    "éclat de orange",
    "éclat de lampe",
    "éclat de citron",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de pin",
    "éclat de crayon",
    "éclat de gouttière",
    "éclat de gouttiere",
    "pli de voile",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de craie",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis malaise; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_craie_maintenant; "
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
            "sous_texte=il_raconte_a_la_maison; "
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
            "destinataire=enfant; sous_texte=il_attend_puis_raconte; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="poudre",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_souffler_trop_fort; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de craie",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_pierre; "
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
    "narrateur|La craie d'hier poudre le pas de la porte.",
    "narrateur|Le platane du village bouge ses branches.",
    "narrateur|Une feuille jaune tourne, puis s'arrête.",
    "narrateur|Papa secoue le tapis.",
    "narrateur|Un nuage gris s'envole.",
    "narrateur|Maman ferme la boîte des feutres, clic.",
    "narrateur|Ça sent le bois du tapis et l'air du matin.",
    "papa|Il reste de la marelle, d'hier.",
    "maman|La craie a fait un petit chemin blanc.",
    "narrateur|Sur la pierre, un éclat de craie brille.",
    "enfant-m|Il est petit, papa.",
    "papa|C'est la craie d'hier.",
    "enfant-m|Je la prends, maintenant !",
    "narrateur|En ce moment, Amir saisit la craie.",
    "narrateur|La craie casse entre ses doigts.",
    "narrateur|La poudre vole, puis retombe.",
    "enfant-m|Elle pique le nez, papa !",
    "narrateur|L'éclat de craie tremble, puis tient.",
    "narrateur|Le sourire d'Amir disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "enfant-m|Ça ne veut pas !",
    "papa|Tu souffles à côté ?",
    "narrateur|Papa s'accroupit à la même hauteur.",
    "narrateur|Amir souffle trop fort, trop vite.",
    "narrateur|La poudre lui revient au visage.",
    "enfant-m|Oh.",
    "narrateur|Ses épaules tombent un peu.",
    "papa|Tes pieds sont sur la pierre ?",
    "enfant-m|Oui, papa.",
    "maman|Tes feutres sont dans la boîte ?",
    "enfant-m|Oui, maman.",
    "enfant-m|Clic.",
    "papa|Tu vois la feuille jaune ?",
    "enfant-m|Oui.",
    "enfant-m|Elle est tombée.",
    "maman|On la laisse par terre ?",
    "enfant-m|Oui, elle est jolie.",
    "papa|On y va ?",
    "enfant-m|On y va.",
    "enfant-m|Au revoir, maman.",
    "maman|Au revoir, Amir.",
    "narrateur|Dehors, le chemin sent la pierre froide.",
    "narrateur|Une feuille jaune tape le platane.",
    "narrateur|L'école sent les feutres et le papier.",
    "narrateur|La maîtresse parle près du tableau.",
    "maitresse|Bonjour.",
    "enfant-m|Bonjour, maîtresse.",
    "narrateur|Amir pose le feutre vert, bouchon fermé.",
    "narrateur|Le vert sent un peu fort, tout près.",
    "narrateur|Une poussière de tableau flotte dans l'air.",
    "narrateur|Plus tard, une voix s'approche.",
    "narrateur|Elle parle bas, d'un secret.",
    "narrateur|Amir sent un malaise.",
    "narrateur|Son ventre se serre.",
    "enfant-m|Je le dis, maintenant !",
    "narrateur|Ses mots se cognent à ceux de la classe.",
    "narrateur|Personne ne tourne la tête.",
    "narrateur|Amir referme la bouche.",
    "narrateur|Il repose les mains sur ses genoux.",
    "narrateur|Il reste près de sa chaise.",
    "narrateur|Le soir, la porte s'ouvre.",
    "narrateur|Ça sent le tapis et la pierre.",
    "papa|Te voilà, Amir.",
    "papa|Le tapis est rentré.",
    "narrateur|La craie attend sur la pierre.",
    "narrateur|La feuille jaune est là.",
    "narrateur|Le ventre est serré, tout petit.",
    "narrateur|Amir regarde papa.",
    "narrateur|Il ouvre la bouche.",
]

Q0001 = [
    "narrateur|Amir a un malaise.",
    "narrateur|Que fait-il ?",
]

C0001 = [
    "narrateur|Amir ouvre la bouche trop vite.",
    "enfant-m|Papa, un secret.",
    "narrateur|Papa n'a pas fini sa phrase.",
    "papa|Le tapis est sec, Amir.",
    "narrateur|Les deux voix se mélangent.",
    "enfant-m|Oh.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Il referme la bouche.",
    "narrateur|Il pose les mains à plat.",
    "narrateur|Le pas de la porte est calme.",
    "papa|Tes pieds sont sur la pierre ?",
    "narrateur|Papa pose le tapis contre le mur.",
    "maman|La feuille jaune est sous le platane.",
    "narrateur|Maman n'a pas fini non plus.",
    "narrateur|Amir attend que le silence arrive.",
    "narrateur|Sur la pierre, l'éclat de craie brille.",
    "enfant-m|Il est là.",
    "enfant-m|Je peux te dire quelque chose ?",
    "maman|Oui, nous t'écoutons.",
    "enfant-m|Une voix a parlé d'un secret.",
    "enfant-m|Mon ventre s'est serré.",
    "papa|Merci, Amir.",
    "narrateur|Papa a entendu toute la phrase.",
    "maman|Tu veux un peu d'eau ?",
    "enfant-m|Oui, maman.",
    "narrateur|Amir pose la main sur la pierre froide.",
    "narrateur|Le ventre d'Amir se desserre.",
]

END = [
    "narrateur|Maman verse de l'eau dans un verre.",
    "narrateur|L'eau fait un petit bruit clair.",
    "enfant-m|C'est froid.",
    "papa|Tes pieds sont au chaud ?",
    "enfant-m|Oui, sur la pierre.",
    "narrateur|Amir boit une gorgée.",
    "narrateur|Amir veut souffler la craie, tout de suite.",
    "narrateur|Il souffle trop fort.",
    "narrateur|La poudre lui pique les yeux.",
    "enfant-m|Oh.",
    "narrateur|Amir s'arrête.",
    "narrateur|Ses mains se ferment, puis s'ouvrent.",
    "narrateur|Il refuse de foncer.",
    "narrateur|Il écoute le platane, un instant.",
    "narrateur|Il souffle à côté, plus léger.",
    "narrateur|Un peu de poudre s'envole vers l'arbre.",
    "enfant-m|Elle ne pique plus.",
    "maman|On laisse la feuille jaune ?",
    "enfant-m|Oui, par terre.",
    "papa|On reste un peu ?",
    "enfant-m|Oui, papa.",
    "narrateur|Le platane bouge ses branches.",
]

FIN = [
    "narrateur|Ils restent sur le pas de la porte.",
    "narrateur|La poudre blanche repose sur la pierre.",
    "enfant-m|Comme ce matin, papa !",
    "papa|Tu le vois, toi ?",
    "enfant-m|Oui, sur la pierre.",
    "maman|On est bien, ici.",
    "narrateur|Le tapis sent le bois, un peu.",
    "narrateur|Amir glisse le pied, sans se presser.",
    "narrateur|La craie repose contre la pierre.",
    "enfant-m|On le sent, maman.",
    "maman|Tu le sens sur tes joues ?",
    "enfant-m|Oui, il est frais.",
    "narrateur|Le platane repose contre le ciel.",
    "narrateur|Une feuille jaune ne bouge plus.",
    "enfant-m|Elle est jolie par terre.",
    "papa|On la laisse ?",
    "enfant-m|Oui.",
    "narrateur|L'éclat de craie tient sur la pierre.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "craie,tapis",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "raconter",
                    "accepted_examples": (
                        "raconter | il raconte | à papa | à la maison "
                        "| il dit | le secret | il parle | papa maman"
                    ),
                    "retry_prompt": (
                        "Amir a un malaise à la maison. Que fait-il ?"
                    ),
                    "engine_ok_text": "Oui, il raconte.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "pierre,voix",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "eau,poudre",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "platane,pierre",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "éclat de craie" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de craie" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count("éclat de craie")
    if n_clue != 4:
        raise SystemExit(f"{SID}: éclat de craie ×{n_clue} (voulu 4)")
    if "ninon" in blob:
        raise SystemExit(f"{SID}: Ninon interdite")
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
    mait = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("maitresse|")
    ).lower()
    if any(x in mait for x in ("écoute", "range", "merci", "règle", "leçon")):
        raise SystemExit(f"{SID}: maîtresse leçon parlée: {mait}")

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
        "- **Leçon :** COL.ECO.001 — écouter / en parler à la maison "
        "(vécue : dire trop vite → mots perdus ; attendre, raconter le malaise)\n"
        "- **Personnages :** Amir, papa, maman (maîtresse = label, pas de leçon parlée)\n"
        "- **Lieu :** école puis maison, pas de la porte, platane du village, "
        "feuille jaune, tapis\n"
        "- **Indice unique :** éclat de craie (pierre du matin → pierre du soir)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La craie d'hier poudre le pas de la porte. Le platane bouge. Une "
        "feuille jaune s'arrête. Papa secoue le tapis. Sur la pierre, un "
        "éclat de craie brille. Amir veut la craie **maintenant**. Il la "
        "saisit trop vite : elle casse, la poudre pique. Première idée : "
        "souffler trop fort. La poudre revient au visage. Sourire parti, "
        "épaules basses. Papa s'accroupit. À l'école, une voix parle d'un "
        "secret. Il veut le dire tout de suite : les mots se cognent, "
        "personne n'entend. Le soir, il ouvre la bouche trop vite : les "
        "voix se mélangent. Il refuse de foncer, attend, raconte. Merci "
        "vécu. Il souffle trop fort sur la craie, s'arrête, souffle à "
        "côté. Sur la pierre, l'éclat tient.\n\n"
        "## Vécu\n\n"
        "Amir veut la craie **maintenant**. Impatience, puis épaules qui "
        "tombent quand la poudre pique. À l'école, le ventre se serre. "
        "Papa s'accroupit, pose une question, ne récite pas la règle. "
        "Amir agit : bouche fermée, mains à plat, phrase entière. Merci "
        "vécu après l'écoute. Fin : l'éclat du début tient sur la pierre.\n\n"
        "## Vu et corrigé\n\n"
        "- Ouverture inventée (craie d'hier, éclat sur la pierre), pas "
        "« joue au salon », pas « Tout doucement ».\n"
        "- Monde du dump (école puis maison, craie blanche, pas de la "
        "porte, platane, feuille jaune, tapis), distinct de COL.ECO.001-01..006 "
        "(gouttière, rayon, pain, soleil, chaussette, moufles).\n"
        "- Ninon retirée. Héros Amir. Maîtresse = label (bonjour), pas de "
        "leçon parlée.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent / "
        "tout bas » retirés. Pas de merle, pas de miel.\n"
        "- Leçon non dite : le malaise se dit à la maison, après l'attente. "
        "Pas de morale, pas « j'ai écouté / bon travail / histoire finie ».\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- Indice unique « éclat de craie » nommé à l'ouverture, revu "
        "quand la craie casse, revu sur la pierre, payé à la fin.\n"
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
