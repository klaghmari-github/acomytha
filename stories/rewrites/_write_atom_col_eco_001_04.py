#!/usr/bin/env python3
"""ATOM-COL.ECO.001-04 — Le soleil de Sarah (F-NAR-019, N2, COL.ECO.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.001-04"
TITLE = "Le soleil de Sarah"
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
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "loïc",
    "loic",
    "grain de miette",
    "grain de foin",
    "grain de paille",
    "grain de toile",
    "grain de pépin",
    "éclat de bec",
    "éclat de marche",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de crayon",
    "éclat de casserole",
    "éclat de wagon",
    "éclat de citron",
    "éclat de lampe",
    "éclat de nappe",
    "éclat de farine",
    "éclat de ombre",
    "éclat d'ombre",
    "éclat de écorce",
    "éclat d'écorce",
    "éclat de laine",
    "éclat de carreau",
    "éclat de grain",
    "éclat de pince",
    "éclat de corde",
    "éclat de caisse",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "trait de craie",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de tableau",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_dire_le_malaise_maintenant; "
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
            "sous_texte=elle_raconte_au_gouter; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="goûter",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_puis_raconte; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de tableau",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; "
            "emotion=fierté_calme; intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_l_eclat_tient; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de tableau",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_tient_sur_le_volet; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "elle raconte",
    "accepted_examples": (
        "elle raconte | raconter | au goûter | au gouter | à papa | "
        "à la maison | elle attend | elle dit | papa | malaise"
    ),
    "retry_prompt": "Sarah a un malaise. Elle raconte au goûter. Que fait-elle ?",
    "engine_ok_text": "Oui, elle raconte.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "linge,portillon",
        [
            "narrateur|Le jardin tient le linge comme une main ouverte.",
            "narrateur|Un torchon rouge claque, puis se tait.",
            "narrateur|Le vent du matin est tiède.",
            "narrateur|Le portillon fait un petit bruit de fer.",
            "narrateur|Papa accroche une pince en bois.",
            "papa|Le torchon rouge fait comme un drapeau.",
            "maman|Tu as senti l'herbe, Sarah ?",
            "enfant-f|Elle est froide, un peu piquante.",
            "narrateur|Maman plie une serviette chaude de soleil.",
            "narrateur|Les feuilles du cerisier bougent, lentes.",
            "papa|Tu as entendu les feuilles ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Elles parlent tout haut.",
            "narrateur|Près du volet noir, quelque chose brille.",
            "narrateur|Sur le noir lisse, un éclat de tableau tremble.",
            "enfant-f|Il est petit, papa.",
            "papa|C'est le soleil sur le volet.",
            "enfant-f|Je veux poser le soleil, maintenant !",
            "maman|Celui de la classe, le rond jaune ?",
            "enfant-f|Oui, sur le tableau !",
            "narrateur|Le cartable attend près des chaussures.",
            "maman|Les chaussures, dans l'allée ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sarah pose les chaussures sur les cailloux.",
            "papa|Tes deux pieds sont sur les cailloux ?",
            "enfant-f|Oui.",
            "narrateur|En ce moment, Sarah prend le rond jaune.",
            "narrateur|Le papier est lisse, un peu chaud.",
            "enfant-f|Il sent le soleil, maman.",
            "maman|On dit au revoir au jardin ?",
            "enfant-f|Au revoir, jardin.",
            "narrateur|Le portillon cliquette derrière eux.",
            "narrateur|La classe sent les feutres et le papier.",
            "narrateur|Un carré de soleil glisse sur le tableau.",
            "narrateur|La maîtresse parle près du noir.",
            "maitresse|Bonjour les enfants.",
            "enfant-f|Bonjour, maîtresse.",
            "maitresse|Le rond jaune va sur le tableau.",
            "narrateur|Sarah pose le soleil, sans se presser.",
            "narrateur|Le papier tient.",
            "narrateur|Sous le rond, l'éclat de tableau brille.",
            "enfant-f|Il est là.",
            "narrateur|Plus tard, c'est la sortie.",
            "narrateur|La cour est chaude.",
            "narrateur|Des voix jouent, plus loin.",
            "narrateur|Près du portail, une voix parle trop près.",
            "narrateur|Sarah sent un malaise.",
            "narrateur|Son ventre se serre, tout petit.",
            "narrateur|Elle reste près du groupe.",
            "narrateur|Elle pense au jardin, au volet.",
            "narrateur|Le soir, le linge est rentré.",
            "narrateur|Le jardin est calme.",
            "narrateur|La porte s'ouvre.",
            "papa|Te voilà.",
            "papa|Tes chaussures ont un peu de poussière.",
            "narrateur|Sarah veut le dire, tout de suite.",
            "enfant-f|Papa, au portail !",
            "narrateur|Papa parle à maman, près des chaussures.",
            "narrateur|Les mots de Sarah se cognent aux leurs.",
            "narrateur|Personne ne tourne la tête.",
            "papa|Tu disais quelque chose, Sarah ?",
            "enfant-f|Mon ventre s'est serré.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-f|Ça ne sort pas, maman.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à sa hauteur.",
            "papa|Tu as faim ?",
            "narrateur|Sarah ouvre la bouche.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Sarah a un malaise.",
            "narrateur|Que fait-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "peche,verre",
        [
            "narrateur|Sarah ouvre la bouche trop vite.",
            "enfant-f|Papa, au portail, quelqu'un parlait !",
            "narrateur|Papa n'a pas fini sa phrase.",
            "papa|Les chaussures, dans l'allée, Sarah.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Elle pose les mains à plat.",
            "narrateur|Elle écoute la maison, un instant.",
            "maman|Le goûter est près de la fenêtre.",
            "narrateur|Papa pose un verre d'eau.",
            "narrateur|Maman pose une pêche.",
            "narrateur|Sarah attend que le silence arrive.",
            "narrateur|Sur le volet, l'éclat de tableau brille.",
            "enfant-f|Je peux te dire quelque chose ?",
            "maman|Oui, nous t'écoutons.",
            "enfant-f|Au portail, quelqu'un a parlé trop près.",
            "enfant-f|Mon ventre s'est serré.",
            "papa|Merci, Sarah.",
            "narrateur|Papa a entendu toute la phrase.",
            "maman|Tu as soif ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le ventre de Sarah se desserre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "resolution",
        "peche,fenetre",
        [
            "narrateur|Sarah range son cartable près de la porte.",
            "papa|On s'assoit près de la fenêtre ?",
            "enfant-f|Oui.",
            "narrateur|On voit le cerisier.",
            "narrateur|La pêche est sucrée, un peu chaude.",
            "enfant-f|Le jardin sent l'herbe sèche.",
            "maman|Tes pieds sont sur le tapis ?",
            "enfant-f|Oui, maman.",
            "narrateur|Sarah veut raconter la cour, d'un coup.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Attends.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Elle reprend, plus lentement.",
            "enfant-f|La cour était chaude.",
            "enfant-f|J'ai posé le soleil.",
            "papa|Le rond jaune, sur le tableau ?",
            "enfant-f|Oui, et l'éclat était là.",
            "narrateur|Sarah croque la pêche.",
            "narrateur|Un peu de jus reste sur le doigt.",
            "maman|Il est sucré ?",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "vent,cerisier",
        [
            "enfant-f|Le torchon rouge est rentré.",
            "maman|Il est plié, près de la porte.",
            "narrateur|Le volet noir garde un peu de soleil.",
            "enfant-f|Comme sur le tableau, papa !",
            "papa|Tu le vois, toi ?",
            "enfant-f|Oui, sur le noir.",
            "narrateur|Le vent tiède pousse une feuille du cerisier.",
            "enfant-f|On est bien, ici.",
            "maman|La pêche est finie ?",
            "enfant-f|Presque, maman.",
            "narrateur|Sarah pose le noyau dans la coupelle.",
            "narrateur|L'éclat de tableau tient sur le volet.",
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
        "Le jardin tient le linge. Sur le volet noir, un éclat de tableau "
        "tremble. Sarah veut poser le soleil, maintenant. À l'école, le rond "
        "jaune tient ; l'éclat brille. Au portail, une voix trop près : "
        "malaise. Elle veut le dire tout de suite : les mots se cognent. "
        "Elle refuse de foncer, raconte au goûter. Merci vécu. Sur le volet, "
        "l'éclat tient."
    )
    merged["title"] = TITLE
    merged["characters"] = "Sarah, papa, maman"
    merged["setting"] = "jardin au linge, classe, puis fenêtre sur le cerisier"
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
    if "éclat de tableau" not in by["CHK_T0000_P0000"]["text"]:
        raise SystemExit("indice éclat de tableau absent à l'ouverture")
    if "éclat de tableau" not in by["CHK_T0000_P0000_END_F0001"]["text"]:
        raise SystemExit("indice éclat de tableau non payé à la fin")
    if joined.lower().count("en ce moment") != 1:
        raise SystemExit("en ce moment doit apparaître une fois")
    adults = " ".join(
        ln.split("|", 1)[1]
        for c in merged["chunks"]
        for ln in c["script"].splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
    ).lower()
    if adults.count("merci") != 1:
        raise SystemExit(f"merci ×{adults.count('merci')}")
    if "bravo" in adults:
        raise SystemExit("bravo en trop")
    if "loïc" in joined.lower() or "loic" in joined.lower():
        raise SystemExit("Loïc interdit")
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "## Promesse narrative\n\n"
        "Le jardin tient le linge comme une main ouverte. Un torchon rouge "
        "claque dans le vent tiède. Sur le volet noir, un éclat de tableau "
        "tremble. Sarah veut poser le soleil de papier, maintenant. À "
        "l'école, le rond jaune tient ; sous le rond, l'éclat brille. Au "
        "portail, une voix parle trop près : malaise, ventre serré. Elle "
        "veut le dire tout de suite. Première idée : couper papa près des "
        "chaussures. Les mots se cognent, personne n'entend. Sourire parti, "
        "épaules basses. Papa s'accroupit. Elle ouvre trop vite : les voix "
        "se mélangent. Elle refuse de foncer, attend le goûter, raconte. "
        "Merci vécu. Elle veut raconter la cour d'un coup, s'arrête, reprend. "
        "Sur le volet, l'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin au linge, torchon rouge, vent tiède, portillon, "
        "cerisier, classe au soleil sur le tableau, fenêtre du soir. ≠ "
        "gouttière/crayon, ≠ rayon/carreaux, ≠ pain/nappe.\n"
        "- Désir : poser le soleil, puis dire le malaise, maintenant.\n"
        "- Objet : rond jaune, volet noir, pêche du goûter.\n"
        "- Indice unique : éclat de tableau, vu dès l'ouverture, payé au "
        "climax (volet pendant le silence) et sur le volet au retour.\n"
        "- Urgence douce : la voix trop près au portail, le ventre qui serre.\n"
        "- Imprévu 1 : tout de suite, elle coupe papa ; les mots se perdent.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après la phrase "
        "entière au goûter.\n"
        "- Imprévu 2 (plus rusé) : à la fenêtre, elle veut raconter la cour "
        "d'un coup ; les mots se bousculent.\n"
        "- Résolution : elle refuse de foncer, attend le silence, dit le "
        "portail, reprend plus lentement.\n"
        "- Retour : torchon plié, feuille du cerisier, l'éclat tient sur "
        "le volet.\n\n"
        "## Vécu\n\n"
        "Leçon COL.ECO.001 (dire le malaise à la maison, au bon moment) "
        "greffée, jamais annoncée. La première idée (tout dire d'un coup) "
        "échoue. Le choix de Sarah change l'action. Un « en ce moment ». "
        "Un merci vécu. Adulte + question. Troupe D16 : Sarah, papa, maman. "
        "Maîtresse : salut de classe, pas de leçon récitée. N2.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu : jardin au linge, classe, fenêtre "
        "sur le cerisier. Monde du dump, ≠ ECO-001-01..003.\n"
        "- Héros Sarah. Loïc retiré du dump TTS.\n"
        "- Ouverture inventée (le jardin tient le linge), pas un gabarit v2.\n"
        "- Indice unique : éclat de tableau. Pas bec/marche/fraise/quille/"
        "promenade/gouttière/crayon/casserole/wagon/citron/lampe/nappe/"
        "farine/ombre/écorce/laine/carreau/grain/pince/corde/caisse/buée/"
        "croûte.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` retirés.\n"
        "- Interdit « bon travail / histoire finie / j'ai écouté ».\n"
        "- Question moteur inchangée (Sarah a un malaise. Que fait-elle ?). "
        "5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N2 ≤ 15. TTS : notes, ssml, xai, piper par "
        "chunk.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
