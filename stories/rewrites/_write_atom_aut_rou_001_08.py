#!/usr/bin/env python3
"""ATOM-AUT.ROU.001-08 — Le chocolat de Nina (F-NAR-019, N1, AUT.ROU.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.ROU.001-08"
TITLE = "Le chocolat de Nina"
N1 = LIMITS["N1"]
CHARS = "Nina, papa, maman"
SETTING = "chambre, radiateur, cuisine, le matin"
INDICE = "éclat de casserole"
FIL = (
    "Le radiateur fait tic. Une chaussette brune y respire. Un anneau de "
    "vapeur glisse sous la porte. Sur le bord, un éclat de casserole "
    "brille. Nina veut le chocolat maintenant. Elle saisit le bol : trop "
    "chaud, une goutte tombe. Elle refuse de foncer, chaussettes, bol sur "
    "le chariot. Les roues tournent. Près du radiateur, l'éclat tient."
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
    "une chose, puis",
    "une chose puis",
    "une étape",
    "lune d'étain",
    "lune d'etain",
    "pique-nique",
    "boîte à musique",
    "boite a musique",
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
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de farine",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de lampe",
    "éclat de citron",
    "pli de voile",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de casserole",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_chocolat_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="bol",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=le_bol_avance_quand_les_roues_touchent; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="chariot",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_pose_le_bol_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="chaussette",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_porter_le_bol; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de casserole",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bord; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "il roule",
    "accepted_examples": (
        "il roule | roule | avec le chariot | les roues | le chariot "
        "| sur les roues | le bol roule"
    ),
    "retry_prompt": (
        "Le bol est trop chaud à porter. Comment avance-t-il ?"
    ),
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "casserole",
        [
            "narrateur|Le radiateur fait tic, près du lit.",
            "narrateur|Une chaussette brune y respire.",
            "narrateur|Elle est épaisse, un peu rêche.",
            "narrateur|L'air sent le lait chaud.",
            "narrateur|Sous la porte, un anneau de vapeur glisse.",
            "narrateur|Il chatouille un peu le nez.",
            "maman|Nina, tu sens le chocolat ?",
            "enfant-f|Oui, maman.",
            "enfant-f|Je le veux maintenant !",
            "narrateur|Dans la cuisine, une casserole chante.",
            "narrateur|Elle fait de petites bulles.",
            "narrateur|Sur le bord, un éclat de casserole brille.",
            "enfant-f|Il est blanc, papa.",
            "papa|C'est le lait, sur le métal.",
            "narrateur|Près de la table, un petit chariot attend.",
            "narrateur|Ses deux roues sont en bois.",
            "narrateur|Le bois est lisse, un peu clair.",
            "narrateur|Le pyjama de Nina est chaud.",
            "narrateur|Le tapis tient ses pieds.",
            "papa|Le bol n'est pas sur la table.",
            "narrateur|En ce moment, Nina saute du lit.",
            "narrateur|Ses pieds trouvent le tapis.",
            "enfant-f|J'y vais !",
            "narrateur|Elle court vers la cuisine, en pyjama.",
            "narrateur|Le carrelage pique ses pieds.",
            "enfant-f|Le bol !",
            "narrateur|Nina saisit le bol d'un coup.",
            "narrateur|Le bol brûle ses doigts.",
            "narrateur|Elle le lâche.",
            "narrateur|Une goutte brune tombe.",
            "enfant-f|Aïe.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et l'inquiétude se heurtent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa se baisse à sa hauteur.",
            "papa|Tu regardes le chariot ?",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nina veut le chocolat.",
            "narrateur|Comment le bol avance-t-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "cacao,roue",
        [
            "narrateur|Nina recule d'un pas.",
            "narrateur|Le carrelage pique.",
            "enfant-f|Il brûle, papa.",
            "papa|Le chariot est là.",
            "narrateur|Nina regarde le petit chariot.",
            "narrateur|Ses roues touchent le sol.",
            "enfant-f|Je ne le porte pas.",
            "narrateur|Elle ouvre les mains.",
            "narrateur|Elle refuse de foncer.",
            "maman|Tes pieds, Nina ?",
            "enfant-f|Ils sont froids.",
            "narrateur|Elle revient vers le radiateur.",
            "narrateur|La chaussette brune est tiède.",
            "narrateur|Elle enfile une, puis l'autre.",
            "maman|Tu as les pieds au chaud ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le pull brun attend sur la chaise.",
            "enfant-f|Toi aussi.",
            "narrateur|Elle enfile le pull.",
            "narrateur|Le pull est lourd, un peu chaud.",
            "papa|Le bol, Nina ?",
            "enfant-f|Sur le chariot.",
            "narrateur|Maman verse le cacao.",
            "narrateur|Ça fait un petit chuchotis.",
            "narrateur|Une vapeur monte du bord.",
            "narrateur|Sur la casserole, l'éclat de casserole brille.",
            "enfant-f|Je te vois.",
            "narrateur|Nina pose le bol sur le bois.",
            "narrateur|Le chariot tient le bol.",
            "enfant-f|Roule.",
            "narrateur|Elle pousse trop fort.",
            "narrateur|Le bol penche.",
            "enfant-f|Oh.",
            "narrateur|Elle s'arrête.",
            "narrateur|Une goutte tremble au bord.",
            "narrateur|Elle donne une petite poussée.",
            "narrateur|Les roues tournent.",
            "narrateur|Toc.",
            "narrateur|Le chariot avance.",
            "enfant-f|Il roule !",
            "papa|Merci, Nina.",
            "maman|Tu le vois, toi ?",
            "enfant-f|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "chaussette,roue",
        [
            "papa|Jusqu'au radiateur ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le chariot roule vers la chambre.",
            "narrateur|Une chaussette barre le passage.",
            "narrateur|La roue s'arrête contre le tissu.",
            "enfant-f|Je le porte !",
            "narrateur|Elle saisit le bol trop vite.",
            "narrateur|Le cacao tremble au bord.",
            "enfant-f|Oh.",
            "narrateur|Nina s'arrête.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Elle refuse de foncer.",
            "narrateur|Le bol revient sur le bois.",
            "narrateur|Elle écarte la chaussette du pied.",
            "narrateur|Le passage est libre, un peu sombre.",
            "enfant-f|Roule.",
            "narrateur|Le chariot avance.",
            "narrateur|Toc.",
            "narrateur|Les roues frottent le tapis.",
            "narrateur|Ça fait un petit bruit.",
            "narrateur|L'éclat de casserole tremble, puis tient.",
            "papa|Il a passé la chaussette.",
            "maman|Le radiateur est près du lit.",
            "enfant-f|J'y vais.",
            "narrateur|Nina marche à côté, sans le porter.",
            "narrateur|Le bois continue son petit bruit.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "radiateur",
        [
            "narrateur|Ils s'arrêtent près du radiateur.",
            "narrateur|Le métal chante plus loin, faible.",
            "enfant-f|Il a fait tout le chemin.",
            "papa|Toi aussi.",
            "narrateur|Le bol est chaud, sous ses doigts.",
            "narrateur|Les chaussettes sont chaudes.",
            "maman|Tu souffles ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina souffle.",
            "narrateur|La vapeur danse, puis s'en va.",
            "narrateur|Elle boit une gorgée.",
            "narrateur|Le cacao est doux, un peu sucré.",
            "enfant-f|C'est bon.",
            "papa|Tu as une moustache.",
            "narrateur|Une ligne brune reste sur la lèvre.",
            "enfant-f|Je la garde.",
            "maman|On est bien, ici.",
            "narrateur|La vapeur n'est plus sous la porte.",
            "narrateur|L'éclat de casserole tient sur le bord.",
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
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
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
        extra_kw: dict = {}
        if cid == "CHK_T0000_P0000_Q0001":
            extra_kw["pause_before_ms"] = 200
            extra_kw["fields"] = Q_FIELDS
        elif cid != "CHK_T0000_P0000":
            extra_kw["pause_before_ms"] = 200
        by[cid] = voice(c, lines, profile, sons, extra_kw)
        if c.get("kind") != by[cid].get("kind"):
            raise SystemExit(f"{cid}: kind changé")
    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
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
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
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
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** AUT.ROU.001 — rouler / faire rouler (vécue : le bol "
        "arrive quand les roues du chariot touchent, pas quand on le porte)\n"
        "- **Personnages :** Nina, papa, maman. Troupe D16.\n"
        "- **Lieu :** chambre, radiateur, cuisine, le matin. ≠ RAN-001-02 "
        "cacao Nina (ranger, pique-nique, lune d'étain). ≠ ROU-001-01 train "
        "de l'allée.\n"
        "- **Indice unique :** éclat de casserole (bord de casserole → "
        "verse le cacao → tremble près du radiateur → tient sur le bord)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le radiateur fait tic. Une chaussette brune y respire. Un anneau "
        "de vapeur glisse sous la porte. Sur le bord, un éclat de casserole "
        "brille. Nina veut le chocolat **maintenant**. Elle court en "
        "pyjama, saisit le bol : trop chaud, une goutte tombe. Sourire "
        "parti, épaules basses. Papa se baisse. Elle refuse de foncer, "
        "chaussettes tièdes, pull, bol sur le chariot. Elle pousse trop "
        "fort : le bol penche. Petite poussée. Toc. Merci vécu. Une "
        "chaussette barre le passage : elle veut porter, le cacao tremble. "
        "Elle écarte, roule. Près du radiateur, elle souffle, boit, "
        "moustache brune. L'éclat tient sur le bord.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chambre, radiateur qui tic, chaussettes brunes, vapeur "
        "sous la porte, casserole, chariot de bois, matin.\n"
        "- Désir : le chocolat dans le bol, maintenant.\n"
        "- Objet : bol, chariot à roues de bois, chaussettes, pull brun.\n"
        "- Indice unique : éclat de casserole, vu dès l'ouverture, payé "
        "au climax et sur le bord.\n"
        "- Urgence douce : la casserole chante, le bol n'est pas à table.\n"
        "- Imprévu 1 : elle saisit le bol d'un coup ; trop chaud ; goutte "
        "brune.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après le premier toc.\n"
        "- Imprévu 2 (plus rusé) : une chaussette barre le passage ; elle "
        "veut porter le dernier mètre.\n"
        "- Résolution : elle refuse de foncer, écarte, pousse. Le bol "
        "roule jusqu'au radiateur.\n"
        "- Retour : souffle, gorgée, moustache, vapeur partie, éclat sur "
        "le bord.\n\n"
        "## Vécu\n\n"
        "Nina veut le chocolat **maintenant**. Impatience (course en "
        "pyjama), puis sourire qui disparaît, épaules qui tombent. Papa se "
        "baisse, pose une question, ne récite pas la règle. Nina agit : "
        "chaussettes, pull, bol posé, petite poussée, chaussette écartée. "
        "Merci vécu après le premier toc. Fin : l'éclat du début tient sur "
        "le bord. La moustache brune reste.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : chambre, radiateur, "
        "cuisine, le matin. Tic « déjà le cacao » jeté. ≠ RAN-001-02 "
        "(ranger, ours, caisse, lune d'étain).\n"
        "- Ouverture inventée (radiateur tic, chaussette qui respire, "
        "anneau de vapeur), pas un gabarit v2, pas « joue au salon ».\n"
        "- Indice unique : éclat de casserole (roster). Pas grain de "
        "vanille/miette/foin, pas éclat de wagon/bec/marche/fraise/"
        "quille/promenade/gouttière, pas merle, miel, marque fine.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` "
        "retirés.\n"
        "- Leçon non dite : le bol arrive quand il roule, pas porté. Pas "
        "« une chose, puis la suivante ». Pas de morale.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive vers le radiateur.\n"
        f"- {nwords} mots. N1 ≤ 10. `check()` OK. Pas apply.\n\n"
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
