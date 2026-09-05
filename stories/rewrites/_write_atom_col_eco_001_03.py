#!/usr/bin/env python3
"""ATOM-COL.ECO.001-03 — Le pain chaud de Victorino (F-NAR-019, N2, COL.ECO.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.001-03"
TITLE = "Le pain chaud de Victorino"
N2 = LIMITS["N2"]
CHARS = "Victorino, papa, maman"
SETTING = "école puis maison, sac de pain, nappe à carreaux, four du village, vélo au loin"
FIL = (
    "Une odeur de croûte traverse la rue. Sur le pain du four, un éclat "
    "de croûte brille. Victorino veut raconter le vélo maintenant. Il "
    "coupe papa : les mots se perdent. À l'école, un camarade parle près "
    "de l'oreille : le ventre se noue, tout dire d'un coup échoue. Il "
    "refuse de foncer, attend, raconte près du pain. Merci vécu. Sur la "
    "croûte, l'éclat de croûte garde une trace."
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
    "j'ai écouté",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "il faut attendre",
    "on doit demander",
    "on va ranger",
    "tu ranges",
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
    "éclat d'ecorce",
    "éclat de laine",
    "éclat de carreau",
    "éclat de grain",
    "éclat de buée",
    "éclat de buee",
    "éclat de boîte",
    "éclat de boite",
    "éclat de tasse",
    "éclat de vitre",
    "éclat de goutte",
    "lune d'étain",
    "lune d'etain",
    "point de gouttière",
    "point de gouttiere",
    "grain de vanille",
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "grain de pomme",
    "grain de sable",
    "marque fine",
    "ombre en forme",
    "trait de craie",
    "trait de vitre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de croûte",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_raconter_maintenant; "
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
            "sous_texte=il_raconte_quand_les_oreilles_sont_pretes; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de croûte",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_refuse_de_foncer_raconte_pres_du_pain; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="croûte",
        note=(
            "arc=action; intention=refermer_le_désir; "
            "emotion=fierté_calme et chaleur; intensite=2; "
            "destinataire=enfant; sous_texte=il_dit_une_chose_pres_du_pain; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de croûte",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_de_croute_garde_une_trace; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "raconter",
    "accepted_examples": (
        "raconter | à la maison | maman | écouter | il raconte | "
        "raconter à maman | il écoute"
    ),
    "retry_prompt": "Il raconte près du pain. Que fait Victorino ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "four,pain,velo",
        [
            "narrateur|Une odeur de croûte traverse la rue.",
            "narrateur|Le four du village respire, chaud.",
            "narrateur|Un vélo passe au loin.",
            "narrateur|Ding.",
            "narrateur|Victorino connaît cette table.",
            "narrateur|La nappe à carreaux est rouge et blanche.",
            "narrateur|Sur la table, le sac de pain craque.",
            "narrateur|Le papier du sac est chaud, un peu rêche.",
            "narrateur|Papa coupe une tartine.",
            "narrateur|La croûte est dorée, un peu cassante.",
            "narrateur|Sur la croûte, un éclat de croûte brille.",
            "enfant-m|Il est doré, papa.",
            "papa|C'est le four, Victorino.",
            "maman|Tu sens le pain, toi ?",
            "enfant-m|Oui, maman.",
            "enfant-m|Je veux le dire, maintenant !",
            "narrateur|Papa parle à maman, près du lait.",
            "papa|Le vélo a sonné, dans la rue.",
            "maman|Oui, il était loin.",
            "enfant-m|Papa, le vélo !",
            "narrateur|Les mots de Victorino se cognent aux leurs.",
            "narrateur|Personne ne tourne la tête.",
            "papa|Tu disais quelque chose ?",
            "enfant-m|Le vélo, il a sonné !",
            "narrateur|Victorino parle trop vite.",
            "narrateur|Les mots tombent, mélangés.",
            "enfant-m|Oh.",
            "narrateur|Le sourire de Victorino disparaît.",
            "narrateur|L'éclat de croûte tremble, puis tient.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|Tu regardes le pain ?",
            "narrateur|En ce moment, Victorino serre le sac.",
            "narrateur|Le papier reste chaud sous les doigts.",
            "maman|Tu essuies tes doigts ?",
            "enfant-m|Oui.",
            "narrateur|Maman verse un peu de lait.",
            "narrateur|Une moustache blanche reste sur la lèvre.",
            "narrateur|Une miette dore un carreau rouge.",
            "papa|On y va ?",
            "enfant-m|On y va.",
            "enfant-m|Au revoir, maman.",
            "maman|Au revoir, Victorino.",
            "narrateur|Dehors, la rue sent le four.",
            "narrateur|Le vélo n'est plus là.",
            "narrateur|L'école sent le papier et le savon.",
            "narrateur|Les chaises font un petit bruit.",
            "narrateur|Victorino s'assoit près du pot.",
            "narrateur|Les ciseaux brillent, pointes en bas.",
            "narrateur|Il veut raconter le vélo.",
            "enfant-m|Le vélo a sonné, dans la rue !",
            "narrateur|Sa voix se cogne à la classe.",
            "narrateur|Personne ne comprend le vélo.",
            "narrateur|Victorino referme la bouche.",
            "narrateur|Un camarade s'approche.",
            "narrateur|Il parle près de l'oreille.",
            "narrateur|Victorino sent un malaise.",
            "narrateur|Son ventre se serre, comme un nœud.",
            "enfant-m|Je veux le dire, maintenant.",
            "narrateur|Il ouvre la bouche, trop vite.",
            "narrateur|Les mots se perdent dans la classe.",
            "narrateur|Personne n'entend le malaise.",
            "narrateur|Victorino reste assis.",
            "narrateur|Le nœud reste dans le ventre.",
            "narrateur|Le soir, le sac de pain est sur la table.",
            "narrateur|Ça sent le cacao et la croûte.",
            "narrateur|La nappe à carreaux attend.",
            "narrateur|La porte s'ouvre.",
            "maman|Te voilà.",
            "papa|Tu as faim ?",
            "narrateur|Victorino pose le cartable.",
            "narrateur|Le ventre est serré, tout petit.",
            "narrateur|Il ouvre la bouche.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorino a un malaise.",
            "narrateur|Que fait-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "pain,cacao",
        [
            "narrateur|Victorino ouvre la bouche trop vite.",
            "enfant-m|Papa, un camarade, l'oreille, le nœud !",
            "narrateur|Papa n'a pas fini sa phrase.",
            "papa|Le cacao est chaud, Victorino.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Victorino refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Il pose les mains près du pain.",
            "narrateur|Il écoute la cuisine, un instant.",
            "papa|Le pain est là, sur la nappe.",
            "narrateur|Papa pose sa tasse.",
            "maman|Le cacao fume un peu.",
            "narrateur|Maman n'a pas fini non plus.",
            "narrateur|Victorino attend que le silence arrive.",
            "narrateur|Sur la croûte, l'éclat de croûte brille.",
            "enfant-m|Il est là.",
            "enfant-m|Je peux te dire quelque chose ?",
            "maman|Oui, nous t'écoutons.",
            "enfant-m|Un camarade a parlé près de mon oreille.",
            "enfant-m|Ça a serré, ici.",
            "narrateur|Victorino montre son ventre.",
            "papa|Merci, Victorino.",
            "narrateur|Papa a entendu toute la phrase.",
            "maman|Tu as faim, maintenant ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Le ventre de Victorino se desserre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pain,beurre",
        [
            "papa|Tu t'assois ?",
            "narrateur|Victorino s'assoit près du pain.",
            "maman|Une tartine ?",
            "enfant-m|Oui, une tartine.",
            "narrateur|Papa coupe la croûte.",
            "narrateur|Victorino veut tout dire d'un coup.",
            "enfant-m|Et le vélo, et l'école aussi !",
            "narrateur|Les mots se bousculent.",
            "enfant-m|Attends.",
            "narrateur|Victorino s'arrête.",
            "narrateur|Il prend une bouchée.",
            "narrateur|La croûte craque sous les dents.",
            "enfant-m|Le vélo a sonné, ce matin.",
            "papa|Tu l'as entendu, toi ?",
            "enfant-m|Oui, loin dans la rue.",
            "maman|Et à l'école ?",
            "enfant-m|J'ai gardé le nœud.",
            "enfant-m|Je le dis ici.",
            "narrateur|La chaleur touche les joues de Victorino.",
            "papa|On est bien, ici ?",
            "enfant-m|Oui, près du pain.",
            "narrateur|Victorino sent le beurre sur ses doigts.",
            "maman|On mange ici.",
            "enfant-m|Oui, ici.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "pain",
        [
            "enfant-m|Le pain était chaud.",
            "maman|Tu es venu le dire.",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur la croûte.",
            "narrateur|Le sac de pain se tait.",
            "narrateur|Victorino sent la croûte sur sa langue.",
            "narrateur|Sur la croûte, l'éclat de croûte garde une trace.",
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
    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "éclat de croûte" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de croûte" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count("éclat de croûte")
    if n_clue != 4:
        raise SystemExit(f"{SID}: éclat de croûte ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
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
    if "maitresse|" in blob or "maîtresse|" in blob:
        raise SystemExit(f"{SID}: maîtresse récite")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nwords = sum(words(c["text"]) for c in chunks)

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** COL.ECO.001 — raconter le malaise (vécue : couper / "
        "tout dire d'un coup → mots perdus ; attendre près du pain → phrase "
        "entendue)\n"
        "- **Personnages :** Victorino, papa, maman. Troupe D16. Maîtresse "
        "du dump : pas de réplique, elle ne récite pas.\n"
        "- **Lieu :** école puis maison, sac de pain, nappe à carreaux, "
        "four du village, vélo au loin. ≠ AUT.ROU.001-03 chambre/escalier "
        "le matin. ≠ COL.ECO.001-01 gouttière/crayon. ≠ COL.ECO.001-02 "
        "rayon/buée/mur rose.\n"
        "- **Indice unique :** éclat de croûte (pain du four → tremble → "
        "nappe du soir → trace sur la croûte)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une odeur de croûte traverse la rue. Le four respire. Ding : un "
        "vélo au loin. Sur le pain du sac, un éclat de croûte brille. "
        "Victorino veut raconter le vélo **maintenant**. Il coupe papa : "
        "les mots se cognent. Première idée ratée. Sourire disparu. Papa "
        "se baisse. À l'école, sa voix se cogne à la classe. Un camarade "
        "parle près de l'oreille : malaise, nœud. Tout dire d'un coup "
        "échoue. Le soir, près du pain, il ouvre trop vite : les voix se "
        "mélangent. Il refuse de foncer, attend le silence, raconte près "
        "du pain. Merci vécu. Il veut tout mélanger, s'arrête, dit le vélo, "
        "puis le nœud. Sur la croûte, l'éclat de croûte garde une trace.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : four du village, rue, vélo, sac de pain, nappe à "
        "carreaux, école (savon, chaises, ciseaux), cacao du soir.\n"
        "- Désir : raconter le vélo, puis le malaise, maintenant.\n"
        "- Objet : sac de pain, tartine, éclat de croûte.\n"
        "- Indice unique : éclat de croûte, vu dès l'ouverture, payé au "
        "climax et sur la croûte.\n"
        "- Urgence douce : les mots pressent, le ventre se noue.\n"
        "- Imprévu 1 : il coupe papa ; à l'école il jette les mots ; "
        "personne n'entend.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après la phrase entière.\n"
        "- Imprévu 2 (plus rusé) : le soir il dit camarade-oreille-nœud "
        "d'un coup ; les voix se mélangent.\n"
        "- Résolution : il refuse de foncer, attend, lit l'éclat, raconte "
        "près du pain.\n"
        "- Retour : tartine, croûte, sac qui se tait, éclat en trace. "
        "Pas « j'ai écouté / bon travail / l'histoire est finie ».\n\n"
        "## Vécu\n\n"
        "Victorino veut parler **maintenant**. Impatience (coupe papa, "
        "jette les mots en classe), puis sourire qui disparaît, épaules "
        "qui tombent, nœud. Papa se baisse, pose une question, ne récite "
        "pas la règle. Victorino agit : bouche fermée, mains près du pain, "
        "phrase entière. Merci vécu après l'écoute. Leçon greffée : le "
        "malaise se dit quand les oreilles sont prêtes. Fin : l'éclat du "
        "début est sur la croûte. Ding n'est pas le merle à trois notes.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Héros D16 : Victorino (dump chars Nino → "
        "Victorino). Adultes parlants : papa/maman. Maîtresse : pas de "
        "réplique.\n"
        "- Lieu du dump : école puis maison, sac, nappe à carreaux, four, "
        "vélo. ≠ escalier/chambre, ≠ gouttière/crayon, ≠ rayon/buée.\n"
        "- Ouverture inventée (odeur, four qui respire, Ding), pas un "
        "gabarit v2, pas « Victorino va à l'école ».\n"
        "- Indice unique : éclat de croûte (roster). Pas éclat de bec/"
        "marche/fraise/quille/promenade/gouttière/crayon/casserole/wagon/"
        "citron/lampe/nappe/farine/ombre/écorce/laine/carreau/grain/buée, "
        "pas grains divers, pas lune d'étain, pas point de gouttière.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : il referme, il attend, il raconte. Pas "
        "« j'ai écouté », pas « bon travail », pas « l'histoire est "
        "finie ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée (malaise / raconter-écouter). 5 "
        "chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive à table.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")


if __name__ == "__main__":
    main()
