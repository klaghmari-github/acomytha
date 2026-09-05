#!/usr/bin/env python3
"""ATOM-AUT.RAN.001-03 — Le pain d'Amir (F-NAR-019, N3, AUT.RAN.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.RAN.001-03"
TITLE = "Le pain d'Amir"
N3 = LIMITS["N3"]
CHARS = "Amir, papa, maman"
SETTING = "salon puis couloir, farine, clochette de vélo, après la fournée"
FIL = (
    "Une clochette de vélo traverse la rue. Ting. Sur la planche, un éclat "
    "de farine brille. Amir veut livrer le pain tiède au bout du couloir, "
    "maintenant. La maison de cubes tombe sur le doudou. Il cherche d'un "
    "coup : trou, table, tout écarter. Rien. Il refuse de foncer, met les "
    "cubes dans la caisse. Les voitures barrent le couloir. Il retrouve "
    "l'éclat près des roues. Le doudou apparaît. Sur la croûte, l'éclat "
    "garde une trace blanche."
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
    "grain de vanille",
    "grain vanille",
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pepin",
    "grain de pomme",
    "grain de sable",
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
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de tasse",
    "éclat d'orange",
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "pli de voile",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
    "nappe à carreaux",
    "cacao",
    "pain doré",
    "pain dore",
    "sac à pain",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de farine",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_pain_au_bout_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="doudou",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; sous_texte=le_doudou_est_sous_le_bazar; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de farine",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="pain",
        note=(
            "arc=action; intention=refermer_le_désir; "
            "emotion=fierté_calme et chaleur; intensite=2; "
            "destinataire=enfant; sous_texte=le_pain_arrive_au_bout; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de farine",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_de_la_planche_est_sur_la_croute; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "le doudou",
    "accepted_examples": (
        "le doudou | doudou | sous les voitures | sous les cubes | "
        "dessous | près de la porte"
    ),
    "retry_prompt": "Il cherche sous les cubes et les voitures. Où est le doudou ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "clochette,cubes,voiture",
        [
            "narrateur|Une clochette de vélo traverse la rue, nette.",
            "narrateur|Ting.",
            "narrateur|Dans la maison, l'odeur de croûte répond.",
            "narrateur|Papa a de la farine sur le tablier.",
            "narrateur|Sur la planche, un éclat de farine brille.",
            "enfant-m|Il est blanc, papa.",
            "papa|C'est un reste de la fournée.",
            "narrateur|L'éclat de farine tient comme une petite lune.",
            "narrateur|Le tapis du salon est épais, chaud.",
            "narrateur|Le couloir, plus loin, reste un peu frais.",
            "maman|Le pain est tiède, Amir.",
            "enfant-m|Je le veux au bout, maintenant.",
            "papa|Au bout du couloir ?",
            "enfant-m|Oui, on le mange là-bas.",
            "narrateur|En ce moment, Amir est à genoux.",
            "narrateur|Des cubes rouges et bleus attendent sur le tapis.",
            "enfant-m|Je fais la boulangerie, maman.",
            "maman|Une maison pour le pain ?",
            "enfant-m|Oui, avec une petite porte.",
            "narrateur|Amir pose un cube rouge, puis un bleu.",
            "narrateur|La maison grandit au milieu du tapis.",
            "narrateur|Les cubes font un bruit sec.",
            "papa|Ta maison a une porte ?",
            "enfant-m|Une petite porte, papa.",
            "narrateur|Amir laisse un trou, bien net.",
            "narrateur|C'est la porte de la boulangerie.",
            "narrateur|Le doudou beige est assis contre le mur.",
            "enfant-m|Toi, tu attends le pain.",
            "narrateur|Papa pose un morceau tiède près de la porte.",
            "enfant-m|Les voitures vont le livrer.",
            "narrateur|Amir prend une petite voiture rouge.",
            "narrateur|Les roues font un bruit léger sur le tapis.",
            "narrateur|La voiture avance trop vite.",
            "narrateur|Elle bute contre un cube.",
            "narrateur|Un pan de la maison glisse.",
            "narrateur|Des cubes tombent sur le doudou.",
            "enfant-m|Oh.",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|La maison a bougé.",
            "enfant-m|Où est mon doudou ?",
            "papa|Derrière la porte de la boulangerie ?",
            "narrateur|Amir regarde le trou, d'un coup.",
            "narrateur|Seulement le pain tiède.",
            "enfant-m|Sous la table ?",
            "narrateur|Il se penche, trop vite.",
            "narrateur|L'ombre est vide.",
            "enfant-m|Il est perdu.",
            "narrateur|Amir veut tout écarter d'un seul geste.",
            "narrateur|Les cubes glissent plus loin, plus nombreux.",
            "enfant-m|Ça ne veut pas.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Ça serre, dans son ventre.",
            "narrateur|Maman se baisse à sa hauteur.",
            "maman|Tu regardes sous les cubes ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Amir cherche son doudou.",
            "narrateur|Où est-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "caisse,voitures",
        [
            "narrateur|Amir refuse d'écarter tout d'un coup.",
            "narrateur|Il pose un genou sur le tapis.",
            "narrateur|Un cube rouge va dans la caisse.",
            "narrateur|Toc.",
            "narrateur|Le bois sent un peu la forêt.",
            "enfant-m|Je le mets, maman.",
            "maman|Tu regardes bien sous la maison ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un cube bleu rejoint le rouge.",
            "narrateur|Le tapis reparaît, un peu.",
            "narrateur|Pas de tissu beige.",
            "papa|Peut-être plus loin, vers le couloir.",
            "narrateur|Amir prend le morceau de pain.",
            "narrateur|Il le pose sur la voiture rouge.",
            "enfant-m|On va au bout.",
            "narrateur|Le couloir est un peu frais.",
            "narrateur|D'autres petites voitures attendent.",
            "narrateur|Une voiture bleue barre le chemin.",
            "narrateur|Une jaune aussi.",
            "enfant-m|Elles cachent le sol.",
            "narrateur|Amir veut les pousser d'un coup.",
            "narrateur|Puis il s'arrête.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Amir refuse de foncer.",
            "narrateur|Il écoute le couloir, un instant.",
            "narrateur|Sur le tapis, un éclat de farine brille.",
            "enfant-m|Comme sur la planche !",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, près des roues.",
            "narrateur|Amir glisse la bleue dans la caisse.",
            "narrateur|Toc.",
            "narrateur|Puis la jaune.",
            "narrateur|Un bout de tissu dépasse près de la porte.",
            "enfant-m|Mon doudou !",
            "narrateur|Le doudou était sous les voitures.",
            "narrateur|Un éclat de farine tient sur son oreille.",
            "narrateur|Amir le serre contre sa joue.",
            "papa|Merci, tu l'as trouvé.",
            "maman|Te voilà, petit.",
            "enfant-m|Il était sous les roues.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pain,couloir",
        [
            "narrateur|Amir s'assoit au bout du couloir.",
            "narrateur|Le doudou est sur ses genoux.",
            "narrateur|Papa lui tend le morceau de pain.",
            "narrateur|La croûte craque sous les dents.",
            "enfant-m|Il est chaud.",
            "maman|On le mange ici, comme prévu.",
            "papa|Tu veux une petite miette pour lui ?",
            "enfant-m|Une toute petite.",
            "narrateur|Amir pose une miette sur le tissu.",
            "narrateur|Le doudou reste bien droit.",
            "narrateur|L'odeur du pain remplit le couloir.",
            "maman|On est bien, ici.",
            "enfant-m|La voiture a fini la course.",
            "papa|Oui, jusqu'au bout.",
            "narrateur|Sur la croûte, un éclat de farine brille.",
            "enfant-m|Comme sur la planche, papa.",
            "narrateur|Au loin, la clochette de vélo reprend.",
            "narrateur|Ting.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "farine,pain",
        [
            "enfant-m|Le doudou a du pain.",
            "maman|Toi aussi.",
            "narrateur|La farine reste un peu sur le tablier.",
            "narrateur|Le couloir sent la croûte chaude.",
            "narrateur|La chaleur touche les joues d'Amir.",
            "narrateur|Sur le pain, l'éclat de farine garde une trace blanche.",
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
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
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
    if blob.count("merci") != 1:
        raise SystemExit(f"{SID}: merci ×{blob.count('merci')}")
    if "éclat de farine" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de farine" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
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
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** AUT.RAN.001 — ranger (vécue, jamais dite)\n"
        "- **Personnages :** Amir, papa, maman. Troupe D16.\n"
        "- **Lieu :** salon puis couloir, farine, clochette de vélo, après "
        "la fournée. ≠ RAN-001-01 nappe. ≠ RAN-001-02 cacao Nina. "
        "≠ AFF.002-03 pain Sarah. ≠ AFF.002-06 sac à pain Nino. "
        "≠ AFF.002-07 cacao Mila.\n"
        "- **Indice unique :** éclat de farine (planche → tapis près des "
        "roues → oreille du doudou → trace blanche sur la croûte)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une clochette de vélo traverse la rue. Ting. L'odeur de croûte "
        "répond. Sur la planche, un éclat de farine brille. Amir veut "
        "livrer le pain tiède au bout du couloir **maintenant**. Il construit "
        "une boulangerie de cubes. Le doudou attend. La voiture bute : la "
        "maison tombe sur le doudou. Première idée ratée : trou, table, tout "
        "écarter d'un geste. Rien. Sourire disparu. Maman se baisse. Il "
        "refuse de foncer, met les cubes dans la caisse. Les voitures barrent "
        "le couloir. Il s'arrête, écoute, retrouve l'éclat près des roues. "
        "Le doudou était dessous. Merci vécu. Au bout, la croûte craque. "
        "L'éclat de farine garde une trace blanche.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon, tapis chaud, couloir frais, farine, clochette.\n"
        "- Désir : livrer le pain tiède au bout du couloir, maintenant.\n"
        "- Objet : morceau de pain, cubes, voiture rouge, doudou beige.\n"
        "- Indice unique : éclat de farine, vu dès l'ouverture, payé au "
        "climax et sur la croûte.\n"
        "- Urgence douce : le pain est tiède, le doudou attend la livraison.\n"
        "- Imprévu 1 : la voiture trop vite ; cubes sur le doudou ; chercher "
        "d'un coup (trou, table, tout écarter) échoue.\n"
        "- Cue : maman à la même hauteur, une question. Un merci vécu, après "
        "le doudou retrouvé.\n"
        "- Imprévu 2 (plus rusé) : les voitures barrent le couloir et cachent "
        "le sol ; il veut les pousser d'un coup.\n"
        "- Résolution : il refuse de foncer, lit l'éclat, glisse les voitures "
        "dans la caisse. Le doudou apparaît.\n"
        "- Retour : pain au bout, miette sur le tissu, Ting au loin, éclat "
        "en trace blanche sur la croûte.\n\n"
        "## Vécu\n\n"
        "Amir veut le pain **maintenant**. Impatience (voiture trop vite), "
        "puis sourire qui disparaît, épaules qui tombent. Maman se baisse, "
        "pose une question, ne récite pas la règle. Amir agit : genou au "
        "tapis, cubes dans la caisse, voitures ensuite. Merci vécu après "
        "la trouvaille. Leçon greffée : le doudou n'apparaît que quand le "
        "bazar quitte le sol. Fin : l'éclat du début est sur la croûte. "
        "Ting n'est pas le merle à trois notes.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : salon puis couloir, farine, "
        "clochette. ≠ nappe vanille, ≠ cacao, ≠ pain doré, ≠ sac à pain, "
        "≠ fournil.\n"
        "- Ouverture inventée (clochette qui répond à la croûte), pas un "
        "gabarit v2, pas « Amir joue au salon ».\n"
        "- Indice unique : éclat de farine. Pas grain de vanille/miette/"
        "foin/feuille/paille/pin/pépin/pomme/sable, pas éclat de pince/"
        "thermos/coquille/bouton/ticket/goutte/boucle/corde/caisse/marche/"
        "caillou/liste/clé/cuillère/sonnette/horloge/tasse/orange/colle/"
        "lessive/vitre/casserole/carreau/grain/nappe/boîte, pas pli de "
        "voile, point de gouttière, trait de craie/vitre, merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : il range pour voir. Pas de morale.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée (doudou). 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive au goûter.\n"
        f"- {nwords} mots. N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
