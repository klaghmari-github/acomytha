#!/usr/bin/env python3
"""ATOM-AUT.RAN.001-06 — F-NAR-019. Les chaussettes du radiateur. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.RAN.001-06"
N1 = 10
TITLE = "Les chaussettes du radiateur"
FIL = (
    "Au campement du radiateur, un éclat de laine brille sur le métal. "
    "Mila veut les chaussettes chaudes, maintenant. La tour penche : les "
    "cubes tombent sur la laine. Elle cherche le canapé, les paumes, "
    "puis saisit toute la pile : les cubes s'éparpillent. Elle refuse de "
    "foncer, pose un cube, retrouve la laine. Sur l'orteil, l'éclat de "
    "laine tient."
)
CHARS = "Mila, papa, maman"
SETTING = "salon, soir, radiateur, laine et caisse de bois"
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
    "on va ranger",
    "tu ranges",
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
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de orange",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de farine",
    "éclat d'ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
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
        emphasis="éclat de laine",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_les_chaussettes_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="chaussettes",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=les_chaussettes_sont_sous_les_cubes; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="caisse",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_pose_un_cube_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de laine",
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
        emphasis="éclat de laine",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_l_orteil; "
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
    "narrateur|Le métal du radiateur fait psss.",
    "narrateur|Une lampe ronde pose un halo.",
    "narrateur|Mila connaît ce salon, le soir.",
    "narrateur|Un détail paraît nouveau, sur le métal.",
    "narrateur|Au campement du radiateur, ça sent le bois.",
    "narrateur|Des chaussettes de laine attendent.",
    "narrateur|Elles sont épaisses, près du canapé.",
    "narrateur|Sur le bord, un éclat de laine brille.",
    "enfant-f|Il est petit, papa.",
    "papa|C'est un éclat de laine.",
    "narrateur|La laine sent le linge propre.",
    "maman|Les chaussettes sont chaudes, Mila.",
    "papa|On les laisse près du chaud.",
    "narrateur|Une caisse en bois est là.",
    "narrateur|Elle sent un peu la forêt.",
    "narrateur|Le tapis est froid, sous les orteils.",
    "enfant-f|J'ai froid aux pieds !",
    "enfant-f|Je veux les chaussettes, maintenant !",
    "maman|Avant la tour de cubes ?",
    "enfant-f|Non, les chaussettes d'abord !",
    "narrateur|En ce moment, Mila saisit la laine.",
    "narrateur|La laine est chaude, un peu lourde.",
    "narrateur|Un cube rouge attend au sol.",
    "enfant-f|Une tour petite, aussi !",
    "narrateur|Elle pose un cube trop vite.",
    "narrateur|Ça fait clic, contre le tapis.",
    "narrateur|Puis un cube jaune.",
    "narrateur|Ça fait clic, contre le rouge.",
    "papa|Ta tour est jolie.",
    "enfant-f|Elle est petite, papa.",
    "narrateur|Mila pose un cube de plus.",
    "narrateur|La tour penche vers la laine.",
    "narrateur|Deux cubes glissent.",
    "narrateur|Ils tombent sur les chaussettes.",
    "enfant-f|Oh.",
    "narrateur|Le sourire de Mila disparaît.",
    "narrateur|Dans sa poitrine, envie et inquiétude se bousculent.",
    "enfant-f|Où sont mes chaussettes ?",
    "maman|Sur le canapé, peut-être ?",
    "narrateur|Mila monte un genou.",
    "narrateur|Le coussin est vide.",
    "enfant-f|Dans mes mains ?",
    "narrateur|Elle ouvre les paumes.",
    "narrateur|Rien.",
    "enfant-f|Elles sont perdues.",
    "enfant-f|Je prends tout, d'un coup !",
    "narrateur|Elle saisit la pile trop vite.",
    "narrateur|Les cubes glissent entre ses doigts.",
    "narrateur|Le tapis disparaît sous les cubes.",
    "enfant-f|Ça ne veut pas, papa.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Papa se baisse à sa hauteur.",
    "papa|Tu regardes sous les cubes ?",
]

Q0001 = [
    "narrateur|Mila cherche ses chaussettes.",
    "narrateur|Où sont-elles ?",
]

C0001 = [
    "narrateur|Mila refuse de prendre toute la pile.",
    "narrateur|Elle pose un genou au tapis.",
    "narrateur|Un cube rouge reste près de sa main.",
    "enfant-f|Je le mets toute seule.",
    "narrateur|Elle glisse le cube dans la caisse.",
    "narrateur|Toc.",
    "narrateur|Le bois sent un peu la forêt.",
    "maman|Tu regardes bien dessous ?",
    "enfant-f|Oui, maman.",
    "narrateur|La tour devient plus petite.",
    "narrateur|Un bout de tapis reparaît.",
    "narrateur|Le cube jaune va dans la caisse.",
    "narrateur|Toc.",
    "enfant-f|Je sors le reste, d'un coup !",
    "narrateur|Elle tire trop fort sur un cube.",
    "narrateur|Deux cubes retombent, comme un toit.",
    "enfant-f|Oh.",
    "narrateur|Mila ne reprend pas trop vite.",
    "narrateur|Elle écoute le salon, un instant.",
    "narrateur|Le radiateur fait psss, près d'elle.",
    "narrateur|Sous un cube, un éclat de laine brille.",
    "enfant-f|Il est là.",
    "narrateur|Mila refuse de foncer.",
    "narrateur|Elle écarte un cube, lentement.",
    "narrateur|Un coin de laine épaisse.",
    "enfant-f|Mes chaussettes !",
    "narrateur|Les chaussettes étaient sous la tour.",
    "narrateur|Elles sentent le savon, un peu chaud.",
    "narrateur|Mila les serre contre sa joue.",
    "papa|Merci, Mila.",
    "enfant-f|Elles étaient dessous.",
    "narrateur|La caisse a presque tous les cubes.",
    "narrateur|Une petite voiture va dedans.",
    "narrateur|Toc.",
    "narrateur|Le tapis est libre, près du chaud.",
    "maman|La laine peut s'enfiler ?",
    "enfant-f|Oui, maman.",
    "narrateur|Mila pose la main sur la laine.",
    "narrateur|Le tissu est un peu rêche.",
]

END = [
    "maman|On enfile les chaussettes ?",
    "narrateur|Maman tend la première.",
    "narrateur|Mila pousse le pied, trop vite.",
    "narrateur|La laine se plie, de travers.",
    "enfant-f|Elle ne veut pas !",
    "narrateur|Mila veut foncer, d'un coup.",
    "narrateur|Mila refuse de foncer.",
    "narrateur|Ses épaules se serrent un peu.",
    "narrateur|Ça tape, dans sa poitrine.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Elle regarde le bord de laine.",
    "narrateur|Un éclat de laine brille, au revers.",
    "enfant-f|Comme sur le métal !",
    "papa|Tu le vois, toi ?",
    "enfant-f|Oui, sur ce bord.",
    "narrateur|Mila tourne la chaussette, lente.",
    "narrateur|Elle écoute le radiateur, un instant.",
    "narrateur|Psss.",
    "narrateur|Le pied glisse, sans forcer.",
    "enfant-f|Elle est dedans.",
    "maman|Et l'autre ?",
    "narrateur|La deuxième suit, sans se presser.",
    "papa|Les orteils sont au chaud ?",
    "enfant-f|Oui, papa.",
    "narrateur|Mila s'assoit près du radiateur.",
    "narrateur|Le métal chante, petit.",
    "papa|Tu veux le livre du canard ?",
    "enfant-f|Oui, papa.",
    "narrateur|Papa ouvre le livre.",
    "narrateur|La couverture est lisse.",
    "narrateur|Les pieds touchent le tapis libre.",
]

FIN = [
    "narrateur|Ils restent près du campement du radiateur.",
    "narrateur|La chaleur touche les orteils de Mila.",
    "enfant-f|Mes pieds sont au chaud.",
    "maman|Oui, la laine est là.",
    "narrateur|Un coin de laine porte une trace claire.",
    "enfant-f|Comme l'éclat de laine, papa !",
    "papa|Tu le vois, toi ?",
    "enfant-f|Oui, sur mon orteil.",
    "narrateur|Mila glisse un pied sur l'autre.",
    "narrateur|La laine repose, un peu lourde.",
    "enfant-f|On le sent, maman.",
    "maman|Tu le sens sur tes orteils ?",
    "enfant-f|Oui, il est chaud.",
    "narrateur|Le livre du canard reste ouvert.",
    "narrateur|L'éclat de laine tient sur l'orteil.",
]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in {
        "CHK_T0000_P0000",
        "CHK_T0000_P0000_Q0001",
        "CHK_T0000_P0000_C0001",
        "CHK_T0000_P0000_END",
        "CHK_T0000_P0000_END_F0001",
    }]
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
                    "expected_answer": "les chaussettes",
                    "accepted_examples": (
                        "les chaussettes | chaussettes | la laine | sous la tour "
                        "| sous les cubes | dessous"
                    ),
                    "retry_prompt": "Elle cherche sous les cubes. Où sont les chaussettes ?",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "caisse,bois",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "obstacle", "chaussettes,livre",
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
    if "éclat de laine" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de laine" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
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
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** AUT.RAN.001 — ranger (vécue : chaussettes sous les cubes)\n"
        "- **Personnages :** Mila, papa, maman. Troupe D16.\n"
        "- **Lieu :** salon, soir, radiateur, laine et caisse de bois "
        "(campement du radiateur)\n"
        "- **Indice unique :** éclat de laine (métal du radiateur → revers "
        "de la chaussette → orteil)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le métal du radiateur fait psss. Une lampe ronde pose un halo. "
        "Mila connaît ce salon le soir ; un détail paraît nouveau. Au "
        "campement du radiateur, un éclat de laine brille sur le bord. "
        "Mila veut les chaussettes chaudes **maintenant**. Elle pose trop "
        "vite : la tour penche, les cubes tombent sur la laine. Première "
        "idée : canapé, paumes. Rien. Elle prend toute la pile d'un coup : "
        "les cubes s'éparpillent. Sourire parti, épaules basses. Papa se "
        "baisse. Mila refuse de foncer, pose un cube, tire trop fort : "
        "deux cubes retombent. Elle écoute, voit l'éclat, écarte un cube. "
        "Les chaussettes étaient dessous. Merci vécu. Une chaussette se "
        "plie : elle refuse de foncer, suit l'éclat au revers. Sur "
        "l'orteil, l'éclat de laine tient. Livre du canard ouvert.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon du soir, psss du radiateur, halo, caisse-forêt.\n"
        "- Désir : les chaussettes chaudes, maintenant, pour les orteils.\n"
        "- Objet : chaussettes de laine, cubes, caisse de bois, livre.\n"
        "- Indice unique : éclat de laine, vu dès l'ouverture, payé à la fin.\n"
        "- Urgence douce : les pieds froids, tout de suite.\n"
        "- Imprévu 1 : tour trop vite, cubes sur la laine ; pile d'un coup.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : la laine se plie ; Mila veut foncer.\n"
        "- Résolution : elle refuse de foncer, lit l'éclat, tourne le bord.\n"
        "- Retour : orteils au chaud, éclat du début sur l'orteil.\n\n"
        "## Vécu\n\n"
        "Mila veut les chaussettes **maintenant**. Impatience, puis sourire "
        "qui disparaît quand la pile résiste. Papa se baisse, pose une "
        "question, ne récite pas la règle. Mila agit : genou au tapis, "
        "cube dans la caisse, laine retrouvée. Merci vécu après les "
        "chaussettes. Au radiateur, elle refuse de foncer. Fin : l'éclat "
        "du début tient sur l'orteil.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump (salon, soir, radiateur, "
        "laine, caisse de bois). ≠ RAN.001-01 nappe/vanille, ≠ 02 cacao/"
        "pluie, ≠ 03 pain/couloir, ≠ 04 cabane sous table, ≠ 05 voiture "
        "rouge/merle/miel.\n"
        "- Ouverture inventée (psss, halo, campement du radiateur), pas "
        "un gabarit v2, pas « Mila joue au salon ».\n"
        "- Indice unique : éclat de laine. Pas grain de miette/foin/"
        "feuille/paille, pas éclat de nappe/caisse/boîte/farine/ombre/"
        "écorce, pas merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : les chaussettes reparaissent quand les cubes "
        "vont dans la caisse. Pas de morale, pas « on va ranger ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée (les chaussettes). 5 chunks, kinds "
        "inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle plus tendu à l'enfilage.\n"
        f"- {nwords} mots. N1 ≤ 10. `check()` OK. Pas apply.\n\n"
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
