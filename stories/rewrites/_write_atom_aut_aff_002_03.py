#!/usr/bin/env python3
"""ATOM-AUT.AFF.002-03 — Le pain doré de Sarah (F-NAR-019, N2, AUT.AFF.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.AFF.002-03"
TITLE = "Le pain doré de Sarah"
N2 = LIMITS["N2"]
CHARS = "Sarah, papa"
SETTING = "hall au clou des clés, rue, vitrine de la boulangerie"
FIL = (
    "Un filet d'air passe sous la porte du hall. Il sent le pain de la rue. "
    "Sur le clou, un éclat de clé brille. Sarah veut le pain doré de la "
    "vitrine, maintenant. Elle tire le manteau jaune : la manche est à "
    "l'envers. Elle refuse de foncer, ouvre la manche, sort. Un cageot "
    "bloque la vitrine ; l'éclat de clé montre un trou. Sur la croûte, "
    "l'éclat de clé brille. Le manteau rentre au crochet."
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
    "grain de pomme",
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
    "trait de craie",
    "trait de vitre",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de clé",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_pain_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="dehors",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; sous_texte=elle_prend_le_manteau; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="manche",
        note=(
            "arc=confirmation; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=elle_ouvre_la_manche_sans_forcer; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de clé",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; "
            "emotion=élan puis prudence puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_refuse_de_foncer_l_éclat_montre_le_trou; "
            "tempo=vif puis posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de clé",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_éclat_du_clou_est_sur_la_croute; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "le manteau",
    "accepted_examples": "le manteau | manteau | elle l'enfile | le manteau jaune",
    "retry_prompt": "Avant de sortir, que prend Sarah ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "cles,porte",
        [
            "narrateur|Un filet d'air passe sous la porte du hall.",
            "narrateur|Il sent le pain chaud, venu de la rue.",
            "narrateur|Sarah connaît ce hall.",
            "narrateur|Les crochets, la rampe, le clou des clés.",
            "narrateur|Sur le clou, un éclat de clé brille.",
            "narrateur|Les clés tintent, légères.",
            "enfant-f|Il brille, papa.",
            "papa|Sarah, tu as vu l'éclat ?",
            "enfant-f|Oui, sur la petite clé.",
            "narrateur|Le manteau jaune attend au crochet.",
            "narrateur|Le tissu est épais, un peu rêche.",
            "narrateur|Un foulard rayé dort sur la rampe.",
            "narrateur|Il est bleu et blanc.",
            "narrateur|Le carrelage du hall est froid.",
            "papa|Sarah, tu sens le pain ?",
            "enfant-f|Oui, papa.",
            "enfant-f|Je le veux à la vitrine, maintenant !",
            "papa|La vitrine est au bout de la rue.",
            "enfant-f|On y va !",
            "papa|On prend le manteau, d'abord.",
            "narrateur|En ce moment, Sarah saisit le manteau jaune.",
            "narrateur|Elle le tire d'un coup, trop vite.",
            "narrateur|Une manche est tordue, à l'envers.",
            "narrateur|Le bras de Sarah ne glisse pas.",
            "enfant-f|Ça coince !",
            "narrateur|Elle tire plus fort.",
            "narrateur|La manche refuse.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Sarah va dehors.",
            "narrateur|Que prend-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "manteau,foulard",
        [
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu regardes la manche ?",
            "enfant-f|Je veux le pain, papa.",
            "narrateur|Sarah refuse de tirer plus fort.",
            "narrateur|Elle pose un genou au sol.",
            "narrateur|La manche est plate, à l'envers.",
            "enfant-f|Je la tourne.",
            "narrateur|Elle retourne le tissu, sans forcer.",
            "narrateur|Le bras glisse, petit à petit.",
            "enfant-f|Elle est ouverte.",
            "papa|Merci, Sarah.",
            "narrateur|Elle enfile l'autre manche.",
            "narrateur|Le tissu est chaud sur ses bras.",
            "papa|Tu veux le foulard aussi ?",
            "enfant-f|Oui, il est rayé.",
            "narrateur|Papa noue le foulard, près du cou.",
            "papa|On ouvre la porte ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa ouvre la porte du hall.",
            "narrateur|L'air de la rue est frais.",
            "narrateur|Ça sent le pain chaud.",
            "narrateur|Sarah tient la main de papa.",
            "enfant-f|J'ai chaud dans le manteau.",
            "papa|Oui, parce que tu l'as pris.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "resolution",
        "rue,pas",
        [
            "narrateur|Ils marchent près, sur le trottoir.",
            "narrateur|Le manteau jaune tape contre sa hanche.",
            "enfant-f|Je le vois, papa ?",
            "papa|Bientôt.",
            "narrateur|Une enseigne claque, plus loin.",
            "narrateur|Le trottoir sent la farine.",
            "enfant-f|Je cours jusqu'à la vitrine !",
            "narrateur|Sarah veut glisser entre un cageot et le mur.",
            "narrateur|Le cageot de sacs bloque le passage.",
            "narrateur|Elle pousse, d'un coup.",
            "narrateur|La manche jaune s'accroche à une latte.",
            "enfant-f|Ça tient !",
            "narrateur|Elle tire.",
            "narrateur|Le cageot penche un peu.",
            "narrateur|Sarah s'arrête net.",
            "enfant-f|Je n'aime pas ça.",
            "narrateur|Elle refuse de foncer.",
            "enfant-f|Attends, je regarde.",
            "narrateur|Papa ne parle pas.",
            "narrateur|Sarah observe les clés, puis le cageot.",
            "narrateur|Dans la main de papa, les clés tintent.",
            "narrateur|L'éclat de clé brille dans un trou, à droite.",
            "enfant-f|Par là, papa.",
            "papa|Tu vois le trou ?",
            "enfant-f|Oui, l'éclat le montre.",
            "narrateur|Ils contournent le cageot, sans se presser.",
            "narrateur|La vitrine est libre.",
            "narrateur|Le pain doré attend derrière le verre.",
            "enfant-f|Il est là.",
            "papa|Oui, il est près.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "vitrine,cles",
        [
            "narrateur|Sarah pose le front près de la vitre.",
            "narrateur|La vitre est un peu froide.",
            "enfant-f|Le pain est doré.",
            "papa|Oui, il est chaud.",
            "narrateur|Papa tient les clés contre le verre.",
            "narrateur|Sur la croûte, un éclat de clé brille.",
            "enfant-f|Comme sur le clou, papa !",
            "papa|Tu le vois, toi ?",
            "enfant-f|Oui, il est sur le pain.",
            "narrateur|Ils rentrent vers le hall.",
            "narrateur|Sarah retire le manteau jaune.",
            "narrateur|Elle le raccroche au crochet.",
            "narrateur|Le crochet fait un petit bruit.",
            "narrateur|Elle pose le foulard sur la rampe.",
            "papa|Tu as fini de poser le foulard ?",
            "enfant-f|Oui, sur la rampe.",
            "narrateur|Les clés retrouvent le clou.",
            "narrateur|Le pain sent sous la porte.",
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
    if emp and emp in text:
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
    nwords = sum(words(c["text"]) for c in chunks)
    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "éclat de clé" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de clé" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
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
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** AUT.AFF.002 — prendre son manteau (vécue)\n"
        "- **Personnages :** Sarah, papa\n"
        "- **Lieu :** hall au clou des clés, rue, vitrine de la boulangerie\n"
        "- **Indice unique :** éclat de clé (clou du hall → trou près du "
        "cageot → croûte du pain)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "## Promesse narrative\n\n"
        "Un filet d'air passe sous la porte du hall. Il sent le pain de la "
        "rue. Sarah connaît ce hall. Sur le clou, un éclat de clé brille, "
        "nouveau. Elle veut le pain doré de la vitrine **maintenant**. Elle "
        "tire le manteau jaune d'un coup : la manche est à l'envers. Première "
        "idée ratée. Papa s'accroupit. Elle refuse de foncer, ouvre la manche, "
        "tient la main. Dans la rue, un cageot bloque la vitrine ; elle pousse, "
        "la manche s'accroche. Elle refuse de foncer. L'éclat de clé montre un "
        "trou. Ils contournent. À la vitre, l'éclat de clé brille sur la "
        "croûte. Le manteau rentre au crochet. Les clés retrouvent le clou.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : hall, filet d'air, pain de la rue, clou, manteau jaune, "
        "foulard rayé, carrelage froid.\n"
        "- Désir : le pain doré de la vitrine, maintenant.\n"
        "- Objet : manteau jaune, foulard, clés de papa.\n"
        "- Indice unique : éclat de clé, vu dès l'ouverture, payé au climax "
        "et sur la croûte.\n"
        "- Urgence douce : le pain est au bout de la rue, elle veut y aller "
        "tout de suite.\n"
        "- Imprévu 1 : manteau tiré trop vite, manche à l'envers.\n"
        "- Cue : papa à la même hauteur, « Tu regardes la manche ? ». Un "
        "merci vécu, après la manche ouverte.\n"
        "- Imprévu 2 (plus rusé) : cageot devant la vitrine ; elle veut "
        "glisser, la manche s'accroche.\n"
        "- Résolution : elle refuse de foncer, lit l'éclat, contourne le "
        "cageot. Main dans la main.\n"
        "- Retour : front contre la vitre froide, éclat sur la croûte, "
        "manteau au crochet, clés au clou, le pain sent sous la porte.\n\n"
        "## Vécu\n\n"
        "Sarah veut le pain **maintenant**. Impatience, puis épaules et "
        "sourire qui tombent quand la manche refuse. Papa se baisse, pose "
        "une question, ne récite pas la règle. Sarah agit : genou au sol, "
        "manche, manteau, main. Merci vécu après la manche. Rue : elle "
        "refuse de foncer. Fin : l'éclat du début est sur la croûte.\n\n"
        "Leçon AUT.AFF.002 greffée, jamais dite. La première idée échoue. "
        "Le choix de Sarah change l'action. Un « en ce moment ». Un merci "
        "vécu. Adulte + question. Troupe D16 : Sarah, papa.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu : hall, rue, vitrine. ≠ four du "
        "village (001-01), ≠ pommes de Chouchou (002-02).\n"
        "- Ouverture inventée (filet d'air, éclat de clé), pas un gabarit v2, "
        "pas « Sarah joue au salon ».\n"
        "- Indice unique : éclat de clé. Pas grain de miette/foin/feuille/"
        "paille/pin/pépin/pomme, pas éclat de pince/thermos/coquille/bouton/"
        "ticket/goutte/boucle/corde/caisse/marche/caillou/liste, pas trait de "
        "craie/vitre, merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Question moteur inchangée (le manteau). 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` (arc, "
        "intention, émotion, intensité, destinataire, sous-texte, tempo, "
        "sourire, respiration). `slow` = question et fin. Action plus vive.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots  path={path}")


if __name__ == "__main__":
    main()
