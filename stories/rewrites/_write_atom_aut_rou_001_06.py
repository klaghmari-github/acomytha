#!/usr/bin/env python3
"""ATOM-AUT.ROU.001-06 — F-NAR-019. Le doudou de Mila. N1. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-AUT.ROU.001-06"
N1 = 10
TITLE = "Le doudou de Mila"
FIL = (
    "Au nid du mobile, un éclat de promenade brille sur l'oreille. "
    "Mila veut le chemin, maintenant. La porte reste fermée. Elle prend "
    "tout d'un coup : le sac bascule, le doudou roule. Elle refuse de "
    "foncer, pose le doudou, le pull, le bol. Au sac, la gourde et le "
    "doudou se coincent. Elle retrouve l'éclat. Dehors, l'éclat de "
    "promenade tient sur l'oreille."
)
CHARS = "Mila, papa, maman"
SETTING = "chambre petite, cuisine, promenade du matin"
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
    "une étape après",
    "grain de miette",
    "grain de sable",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "éclat de wagon",
    "éclat de bec",
    "éclat de marche",
    "éclat de fraise",
    "éclat de quille",
    "éclat de laine",
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
        emphasis="éclat de promenade",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_chemin_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="promenade",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=une_chose_puis_le_doudou_peut_venir; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="doudou",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=concentration puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_pose_le_doudou_sans_foncer; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de promenade",
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
        emphasis="éclat de promenade",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_l_oreille; "
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
    "narrateur|Une étoile de bois glisse sur le mur.",
    "narrateur|Le mur est couleur pêche.",
    "narrateur|Un oiseau de bois la suit.",
    "narrateur|Ça fait un vent minuscule.",
    "narrateur|Au nid du mobile, ça sent le coton.",
    "enfant-f|Il tourne, papa.",
    "papa|Oui, le mobile tourne.",
    "narrateur|Sur la chaise, le doudou rouge attend.",
    "narrateur|Une oreille penche, molle.",
    "narrateur|L'autre oreille reste droite.",
    "narrateur|Sur l'oreille molle, un éclat de promenade brille.",
    "papa|C'est un éclat de promenade.",
    "enfant-f|Il est petit, comme un chemin.",
    "maman|Il brille vers la porte.",
    "narrateur|Le nez du doudou est un fil.",
    "narrateur|Le fil est rouge, un peu rêche.",
    "enfant-f|On sort, maintenant !",
    "narrateur|Mila veut la promenade, maintenant.",
    "narrateur|Le drap du lit sent le savon.",
    "narrateur|En ce moment, elle saisit le doudou.",
    "narrateur|Elle court vers la porte.",
    "narrateur|Le pyjama frotte ses genoux.",
    "narrateur|La porte reste fermée.",
    "narrateur|Derrière la porte, l'air sent l'herbe.",
    "enfant-f|Ouvre, papa !",
    "narrateur|Elle tire la poignée, les deux mains.",
    "narrateur|Le doudou glisse, tombe.",
    "narrateur|Une oreille se plie sous la chaise.",
    "enfant-f|Oh.",
    "narrateur|Le sourire de Mila disparaît.",
    "narrateur|Dans sa poitrine, envie et inquiétude se bousculent.",
    "enfant-f|Je prends tout, d'un coup !",
    "narrateur|Elle prend le sac, une chaussure, le doudou.",
    "narrateur|Le sac bascule.",
    "narrateur|La chaussure tape le tapis.",
    "narrateur|Le doudou roule sous la chaise.",
    "enfant-f|Ça ne veut pas.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Papa se baisse à sa hauteur.",
    "papa|Tu cherches l'éclat, Mila ?",
    "enfant-f|Il est sous la chaise.",
    "maman|On se prépare, Mila ?",
    "enfant-f|Je veux le chemin.",
]

Q0001 = [
    "narrateur|Mila veut la promenade.",
    "narrateur|Comment se prépare-t-elle ?",
]

C0001 = [
    "narrateur|Mila pose le sac près du lit.",
    "narrateur|La chaussure aussi.",
    "narrateur|Elle pose un genou au tapis.",
    "narrateur|Sous la chaise, le doudou attend.",
    "enfant-f|Je le sors toute seule.",
    "narrateur|Elle tire l'oreille, trop vite.",
    "narrateur|L'oreille se plie, de travers.",
    "enfant-f|Oh.",
    "narrateur|Mila ne reprend pas trop vite.",
    "narrateur|Elle écoute la chambre, un instant.",
    "narrateur|Le mobile tourne, petit.",
    "narrateur|Sur l'oreille, l'éclat de promenade brille.",
    "enfant-f|Il est là.",
    "narrateur|Mila refuse de foncer.",
    "narrateur|Elle glisse le doudou, lente.",
    "narrateur|Le doudou sent le coton chaud.",
    "enfant-f|Sur la chaise.",
    "narrateur|Elle le pose, bien droit.",
    "maman|Le pull, Mila ?",
    "enfant-f|Oui, maman.",
    "narrateur|Le pull rose est sur le dossier.",
    "narrateur|Mila enfile le pull.",
    "narrateur|Le coton est un peu tiède.",
    "enfant-f|C'est fait.",
    "papa|Ensuite, le bol ?",
    "narrateur|Mila va à la cuisine.",
    "narrateur|Le carrelage est froid sous ses pieds.",
    "narrateur|Ça sent le lait.",
    "narrateur|À la fenêtre, une lumière ronde.",
    "maman|Tu veux le bol rouge ?",
    "enfant-f|Oui, le rouge.",
    "narrateur|Elle s'assoit.",
    "narrateur|Le bol est lisse, un peu lourd.",
    "narrateur|Elle boit une gorgée.",
    "narrateur|Le lait est tiède.",
    "papa|Le doudou t'attend sur la chaise.",
    "enfant-f|Après, dans le sac.",
    "papa|Merci, Mila.",
    "enfant-f|Il vient avec nous.",
]

END = [
    "maman|Le sac, maintenant ?",
    "narrateur|Le sac jaune est près de la porte.",
    "narrateur|Une sangle pend, un peu rêche.",
    "narrateur|Mila veut tout mettre, d'un coup.",
    "narrateur|Elle pousse le doudou et la gourde.",
    "narrateur|La gourde roule.",
    "narrateur|Le doudou se coince, de travers.",
    "enfant-f|Il ne rentre pas !",
    "narrateur|Mila veut foncer, d'un coup.",
    "narrateur|Mila refuse de foncer.",
    "narrateur|Ses épaules se serrent un peu.",
    "narrateur|Ça tape, dans sa poitrine.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Elle regarde le doudou.",
    "narrateur|Elle écoute le nid du mobile.",
    "narrateur|Le mobile fait un vent minuscule.",
    "narrateur|Sur l'oreille, l'éclat de promenade brille.",
    "enfant-f|Comme sur la chaise !",
    "papa|Tu le vois, toi ?",
    "enfant-f|Oui, sur cette oreille.",
    "narrateur|Mila pose la gourde, d'abord.",
    "narrateur|Toc, au fond du sac.",
    "narrateur|Puis elle glisse le doudou.",
    "narrateur|L'oreille dépasse, avec l'éclat.",
    "enfant-f|Il voit le chemin.",
    "narrateur|Mila met ses chaussures.",
    "maman|Le bon pied ?",
    "enfant-f|Oui.",
    "narrateur|Papa ouvre la porte.",
    "narrateur|L'air du matin entre, frais.",
    "narrateur|Le chemin sent l'herbe coupée.",
]

FIN = [
    "narrateur|Ils marchent sur le chemin de l'herbe.",
    "narrateur|Le sac tape contre la hanche.",
    "enfant-f|L'oreille dépasse.",
    "maman|Elle voit la promenade ?",
    "enfant-f|Oui, maman.",
    "narrateur|L'éclat de promenade brille, dehors.",
    "enfant-f|Comme dans la chambre !",
    "papa|Tu le vois sur l'oreille ?",
    "enfant-f|Oui, papa.",
    "narrateur|Une feuille sèche roule sur le chemin.",
    "narrateur|Mila serre la sangle.",
    "narrateur|Le doudou chauffe contre son dos.",
    "enfant-f|Le sac ne voulait pas.",
    "maman|Et là, il vient avec nous.",
    "narrateur|Le mobile, derrière eux, ne tourne plus.",
    "narrateur|Un coin de l'oreille porte une trace d'herbe.",
    "enfant-f|Une petite herbe, papa.",
    "narrateur|L'air frais reste sur ses joues.",
    "narrateur|L'éclat de promenade tient sur l'oreille.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "mobile,doudou",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "une chose",
                    "accepted_examples": (
                        "une chose | puis l'autre | d'abord | doucement | "
                        "une chose puis l'autre | puis la suivante"
                    ),
                    "retry_prompt": "Elle fait une chose, puis la suivante. Comment se prépare Mila ?",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "bol,lait",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "obstacle", "sac,porte",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "herbe,chemin",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "éclat de promenade" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if "éclat de promenade" not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
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
        "- **Leçon :** AUT.ROU.001 — une chose puis la suivante "
        "(vécue : doudou, pull, bol, gourde, sac)\n"
        "- **Personnages :** Mila, papa, maman. Troupe D16.\n"
        "- **Lieu :** chambre petite, nid du mobile, cuisine, "
        "chemin de l'herbe (promenade du matin)\n"
        "- **Indice unique :** éclat de promenade (oreille molle → "
        "sac → oreille dehors sur le chemin)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une étoile de bois glisse sur le mur pêche. Au nid du mobile, "
        "un éclat de promenade brille sur l'oreille molle du doudou rouge. "
        "Mila veut le chemin **maintenant**. Porte fermée, pyjama. Elle tire "
        "des deux mains : le doudou tombe. Première idée : tout d'un coup "
        "(sac, chaussure, doudou). Le sac bascule, le doudou roule. Sourire "
        "parti, épaules basses. Papa se baisse. Mila refuse de foncer, pose "
        "le doudou, le pull, boit le lait. Merci vécu. Au sac, gourde et "
        "doudou se coincent. Elle refuse de foncer, écoute le mobile, "
        "retrouve l'éclat, pose la gourde d'abord. Dehors, une trace d'herbe "
        "sur l'oreille. L'éclat de promenade tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chambre petite, mur pêche, nid du mobile, vent minuscule.\n"
        "- Désir : la promenade, maintenant, avec le doudou.\n"
        "- Objet : doudou rouge, sac jaune, gourde, pull rose, bol rouge.\n"
        "- Indice unique : éclat de promenade, vu dès l'ouverture, payé à la fin.\n"
        "- Urgence douce : l'herbe sent derrière la porte fermée.\n"
        "- Imprévu 1 : porte fermée ; tout d'un coup, sac et doudou par terre.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : gourde et doudou coincés dans le sac.\n"
        "- Résolution : elle refuse de foncer, lit l'éclat, gourde puis doudou.\n"
        "- Retour : chemin de l'herbe, éclat du début sur l'oreille.\n\n"
        "## Vécu\n\n"
        "Mila veut sortir **maintenant**. Impatience, puis sourire qui "
        "disparaît quand le sac bascule. Papa se baisse, pose une "
        "question, ne récite pas la règle. Mila agit : genou au tapis, "
        "doudou sur la chaise, pull, lait. Merci vécu après le bol. Au "
        "sac, elle refuse de foncer. Fin : l'éclat du début tient sur "
        "l'oreille, avec une trace d'herbe.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump (chambre petite, cuisine, "
        "promenade du matin). ≠ ROU.001-01 train/allée, ≠ 02 miettes/"
        "oiseau, ≠ 03 pain/escalier, ≠ 04 fraises/marché, ≠ 05 bateau/"
        "bassin.\n"
        "- Ouverture inventée (étoile de bois, nid du mobile), pas un "
        "gabarit v2, pas « Mila joue au salon ».\n"
        "- Indice unique : éclat de promenade. Pas éclat de wagon/bec/"
        "marche/fraise/quille/laine, pas merle, miel.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Leçon non dite : le doudou rejoint le chemin quand une chose "
        "vient après l'autre. Pas de morale, pas « on va apprendre ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée (une chose). 5 chunks, kinds "
        "inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle plus tendu au sac.\n"
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
