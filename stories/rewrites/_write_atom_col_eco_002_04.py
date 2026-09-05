#!/usr/bin/env python3
"""ATOM-COL.ECO.002-04 — F-NAR-019. La pomme de pin de Nina. N3. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.002-04"
N3 = LIMITS["N3"]
TITLE = "La pomme de pin de Nina"
INDICE = "éclat de mousse"
FIL = (
    "Un filet d'escargot brille sur le mur. Sur une écaille, un éclat "
    "de mousse brille. Nina veut montrer la pomme de pin, maintenant. "
    "Elle tire trop vite : les mots se perdent. À la classe, elle ouvre "
    "la bouche trop tôt. Elle refuse de foncer, lève la main, attend, "
    "parle. Merci vécu. L'éclat de mousse tient sur l'écaille."
)
CHARS = "Nina, papa, maman"
SETTING = "entrée, classe, goûter, puis maison"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent", "tout bas")
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
    "tu as attendu",
    "cacao",
    "refuge",
    "vapeur",
    "boulangerie",
    "petit pain",
    "fromage",
    "coquille",
    "mouette",
    "grain de pin",
    "grain de",
    "éclat de pin",
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
    "éclat de moufle",
    "éclat de cartable",
    "éclat de casier",
    "éclat de craie",
    "éclat de lessive",
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
        emphasis="éclat de mousse",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_montrer_la_pomme_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="parler",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_attend_puis_parle; "
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
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de mousse",
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
        emphasis="éclat de mousse",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_l_ecaille; "
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
    "narrateur|Un filet d'escargot brille sur le mur.",
    "narrateur|Il est argenté, un peu visqueux.",
    "narrateur|L'air sent la mousse froide.",
    "narrateur|Nina connaît ce mur de l'entrée.",
    "narrateur|Ce filet, lui, est nouveau.",
    "narrateur|Une pomme de pin roule dans la poche.",
    "narrateur|Elle chatouille les doigts, sèche.",
    "narrateur|Sur une écaille, un éclat de mousse brille.",
    "enfant-f|Il est vert, maman.",
    "maman|C'est la mousse du sentier.",
    "papa|Le cartable est un peu humide, dehors.",
    "narrateur|Maman tient le cartable de Nina.",
    "narrateur|Le tissu sent la pluie et le bois.",
    "enfant-f|Je veux montrer la pomme de pin, maintenant !",
    "enfant-f|Près du hérisson.",
    "papa|La pomme verte est pour le goûter.",
    "narrateur|Papa parle près du cartable, une main sur le tissu.",
    "enfant-f|Je la sors !",
    "narrateur|Nina tire trop vite.",
    "narrateur|La pomme de pin glisse, presque.",
    "narrateur|Les mots se cognent à ceux de papa.",
    "narrateur|Personne ne tourne la tête.",
    "enfant-f|Oh.",
    "narrateur|L'éclat de mousse tremble, puis tient.",
    "narrateur|Le sourire de Nina disparaît.",
    "narrateur|Dans sa poitrine, envie et inquiétude se bousculent.",
    "enfant-f|Ça ne veut pas.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Papa se baisse à sa hauteur.",
    "papa|Tu veux la montrer ?",
    "enfant-f|Oui, papa.",
    "maman|Tu vas t'asseoir sur le tapis ?",
    "enfant-f|D'accord, maman.",
    "narrateur|En ce moment, Nina entre dans la classe.",
    "maman|Au revoir, Nina.",
    "enfant-f|Au revoir, maman.",
    "narrateur|Nina s'assoit sur le tapis.",
    "narrateur|Le tapis est un peu froid, sous les genoux.",
    "narrateur|La pomme de pin reste dans la poche.",
    "narrateur|Près du tableau, la maîtresse montre une affiche.",
    "narrateur|C'est un hérisson.",
    "narrateur|Les piquants sont dessinés au crayon brun.",
    "narrateur|La classe écoute l'affiche.",
    "narrateur|Nina a une idée.",
    "narrateur|Les piquants ressemblent à la pomme de pin.",
    "enfant-f|Je veux parler des piquants.",
]

Q0001 = [
    "narrateur|Nina veut parler.",
    "narrateur|Que fait-elle d'abord ?",
]

C0001 = [
    "narrateur|Nina ouvre la bouche trop vite.",
    "enfant-f|Les piquants, comme ma pomme de pin !",
    "narrateur|Un camarade parle, près de l'affiche.",
    "copain|Le hérisson a des piquants.",
    "narrateur|Les deux voix se mélangent.",
    "enfant-f|Oh.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Nina refuse de foncer.",
    "narrateur|Elle referme la bouche.",
    "narrateur|Elle lève la main, près du tapis.",
    "narrateur|Sa main reste en l'air.",
    "narrateur|Le camarade finit sa phrase.",
    "narrateur|Nina attend que le silence arrive.",
    "narrateur|Sur l'écaille, l'éclat de mousse brille.",
    "enfant-f|Je peux dire quelque chose ?",
    "narrateur|La classe tourne un peu la tête.",
    "enfant-f|Le hérisson a des piquants.",
    "enfant-f|Comme ma pomme de pin.",
    "narrateur|Elle la pose près de l'affiche.",
    "narrateur|Les piquants et les écailles se regardent.",
    "narrateur|Plus tard, c'est le goûter.",
    "narrateur|Les boîtes s'ouvrent.",
    "narrateur|Ça sent la pomme verte.",
    "narrateur|Nina a envie de raconter son goûter.",
    "enfant-f|J'ai une pomme !",
    "narrateur|Les voix se mélangent, près des boîtes.",
    "narrateur|Nina referme la bouche.",
    "narrateur|Elle lève la main.",
    "narrateur|Elle attend.",
    "narrateur|Une boîte se ferme, un peu plus loin.",
    "enfant-f|J'ai une pomme verte.",
    "narrateur|Le soir, la porte s'ouvre.",
    "maman|Te voilà, Nina.",
    "papa|Le manteau sent la mousse.",
    "narrateur|Nina pose le cartable contre le mur.",
    "enfant-f|J'ai montré la pomme de pin.",
    "enfant-f|Les piquants, comme les écailles.",
    "papa|Merci, Nina.",
    "narrateur|Papa a entendu toute la phrase.",
    "maman|Tu veux ta pomme ?",
    "enfant-f|Oui, maman.",
    "narrateur|Le ventre de Nina se desserre.",
]

END = [
    "narrateur|Nina veut tout dire, d'un coup.",
    "narrateur|Elle prend la pomme et la pomme de pin.",
    "narrateur|La pomme verte glisse vers le sol.",
    "narrateur|La pomme de pin roule vers le rebord.",
    "enfant-f|Ça tombe !",
    "narrateur|Nina veut foncer, d'un coup.",
    "narrateur|Nina refuse de foncer.",
    "narrateur|Ses épaules se serrent un peu.",
    "narrateur|Ça tape, dans sa poitrine.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Elle regarde la pomme de pin.",
    "narrateur|Elle écoute l'entrée, un instant.",
    "narrateur|Le filet d'escargot sèche un peu, sur le mur.",
    "narrateur|Sur le rebord, l'éclat de mousse brille.",
    "enfant-f|Comme ce matin !",
    "papa|Tu le vois, toi ?",
    "enfant-f|Oui, sur cette écaille.",
    "narrateur|Nina pose la pomme de pin, d'abord.",
    "narrateur|Puis elle rattrape la pomme verte.",
    "maman|La pomme, Nina ?",
    "enfant-f|Oui.",
    "narrateur|Elle s'assoit.",
    "narrateur|La pomme est lisse, un peu froide.",
    "narrateur|Elle croque.",
    "narrateur|Le jus est doux.",
]

FIN = [
    "narrateur|La pomme de pin attend sur le rebord.",
    "narrateur|Le filet d'escargot sèche sur le mur.",
    "enfant-f|L'éclat est là, papa.",
    "papa|Tu le vois sur l'écaille ?",
    "enfant-f|Oui, papa.",
    "maman|On est bien, ici.",
    "narrateur|La pomme verte repose près de la fenêtre.",
    "narrateur|La fenêtre tremble moins.",
    "enfant-f|On m'a entendue.",
    "maman|On t'a entendue, Nina.",
    "enfant-f|Oui, maman.",
    "narrateur|Nina pose la joue près des écailles.",
    "narrateur|Les écailles sont sèches, un peu rudes.",
    "enfant-f|C'est froid.",
    "narrateur|Dehors, la mousse reste sur le sentier.",
    "narrateur|L'éclat de mousse tient sur l'écaille.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "poche,porte",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "attendre",
                    "accepted_examples": (
                        "attendre | elle attend | lever la main | la main"
                    ),
                    "retry_prompt": "Elle lève la main et elle attend. Que fait Nina ?",
                    "engine_ok_text": "Oui, elle attend.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "boite,pomme",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "obstacle", "pomme,rebord",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "rebord,mousse",
            extra={"pause_before_ms": 200},
        ),
    }

    chunks = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, src["age_band"], chunks)

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 5:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 5)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "grain de pin" in blob:
        raise SystemExit(f"{SID}: BAN grain de pin")
    if "cacao" in blob or "refuge" in blob:
        raise SystemExit(f"{SID}: BAN cacao/refuge (002-04 implicite)")
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
        raise SystemExit(f"{SID}: maîtresse parle (label seulement)")

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
        "- **Public :** N3 (5–6 ans), audio familial, ≤16 mots/phrase\n"
        "- **Leçon :** COL.ECO.002 — attendre son tour de parole "
        "(vécue : ouvrir la bouche trop vite → mots perdus ; lever la "
        "main, attendre le silence → phrase entendue)\n"
        "- **Personnages :** Nina, papa, maman. Maîtresse = label dump, "
        "pas de leçon récitée. Troupe D16.\n"
        "- **Lieu :** entrée, classe, goûter, puis maison. Pomme de pin "
        "dans la poche, filet d'escargot, mousse froide.\n"
        "- **Indice unique :** éclat de mousse (écaille du matin → "
        "écaille du soir sur le rebord)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un filet d'escargot brille sur le mur de l'entrée. L'air sent la "
        "mousse froide. Sur une écaille, un éclat de mousse brille. Nina "
        "veut montrer la pomme de pin **maintenant**. Première idée : la "
        "sortir d'un coup, parler par-dessus papa. La pomme glisse, les "
        "mots se perdent. Sourire parti, épaules basses. Papa se baisse. "
        "À la classe, l'affiche du hérisson : elle veut parler des "
        "piquants. Elle ouvre trop vite : un camarade parle. Elle refuse "
        "de foncer, lève la main, attend, pose la pomme de pin. Merci "
        "vécu. Pomme et pomme de pin d'un coup : ça tombe. Elle refuse, "
        "retrouve l'éclat. L'éclat de mousse tient sur l'écaille.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : entrée, filet d'escargot, mousse froide, poche, "
        "cartable humide, tapis, affiche du hérisson, goûter, rebord.\n"
        "- Désir : montrer la pomme de pin, parler des piquants, "
        "maintenant.\n"
        "- Objet : pomme de pin, pomme verte, cartable, affiche, rebord.\n"
        "- Indice unique : éclat de mousse, vu dès l'ouverture, payé à "
        "la fin.\n"
        "- Urgence douce : les mots prêts, la classe qui écoute l'affiche.\n"
        "- Imprévu 1 : elle tire trop vite ; la pomme glisse. À la "
        "classe, elle coupe le camarade.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : tout dire et tout prendre d'un coup ; "
        "pomme et pomme de pin tombent.\n"
        "- Résolution : elle refuse de foncer, lève la main, attend, "
        "parle.\n"
        "- Retour : joue près des écailles, éclat du début sur l'écaille.\n\n"
        "## Vécu\n\n"
        "Nina veut montrer la pomme de pin **maintenant**. Impatience, "
        "puis sourire qui disparaît. Un camarade parle ; elle veut "
        "parler. Papa se baisse, pose une question, ne récite pas la "
        "règle. Nina agit : bouche fermée, main levée, phrase entière. "
        "Merci vécu après l'écoute. Fin : l'éclat du début tient sur "
        "l'écaille.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump (entrée, classe, goûter, "
        "maison, pomme de pin, filet d'escargot, mousse froide). "
        "≠ COL.ECO.002-01 pain/boulangerie. ≠ 002-02 mer/coquille. "
        "≠ 002-03 fromage/marché. ≠ cacao/refuge (ancienne implicite).\n"
        "- Maîtresse : label dump seulement, pas de leçon récitée, pas "
        "de réplique « il faut attendre / tu as attendu ».\n"
        "- Ouverture inventée (filet d'escargot sur le mur), pas un "
        "gabarit v2, pas « Nina est dans l'entrée ».\n"
        "- Indice unique : éclat de mousse. Pas grain de pin (BAN). "
        "≠ RAN.001 nappe/farine/laine.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` "
        "retirés.\n"
        "- Leçon non dite : on l'entend quand elle attend, puis parle. "
        "Pas de morale, pas « on lève la main / puis on parle ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Nina veut parler. Que fait-elle "
        "d'abord ? ». expected attendre. 5 chunks, kinds inchangés.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle plus tendu à la pomme qui tombe.\n"
        f"- {nwords} mots. N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
