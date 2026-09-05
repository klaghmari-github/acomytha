#!/usr/bin/env python3
"""ATOM-COL.ECO.002-07 — L'oiseau en papier de Nina (F-NAR-019, N1, COL.ECO.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.002-07"
TITLE = "L'oiseau en papier de Nina"
N1 = LIMITS["N1"]
CHARS = "Nina, papa, maman"
SETTING = "cuisine au rayon, classe au coussin vert, puis maison"
INDICE = "éclat de pli"
FIL = (
    "Un rayon traverse la cuisine. La poussière danse. Sur une aile, un "
    "éclat de pli brille. Nina veut montrer l'oiseau en papier, maintenant. "
    "Elle tire trop vite : les mots se perdent. À la classe, elle ouvre "
    "la bouche trop tôt. Elle refuse de foncer, lève la main, attend, "
    "parle du chien. Merci vécu. L'éclat de pli tient sur l'aile."
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
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "delphine",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai attendu",
    "j'ai levé la main",
    "j'ai leve la main",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "tu attends ton tour",
    "tu as attendu",
    "c'est ton tour",
    "on lève la main",
    "on aime écouter",
    "on aime ecouter",
    "tapis",
    "crochet",
    "carotte",
    "seau",
    "carton",
    "mousse",
    "pompon",
    "manteau",
    "crayon",
    "buée",
    "buee",
    "croûte",
    "croute",
    "tableau",
    "casier",
    "moufle",
    "craie",
    "cartable",
    "pinceau",
    "casserole",
    "grain de",
    "grains",
    "lune d'étain",
    "lune d'etain",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de carotte",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de laine",
    "éclat de tasse",
    "éclat de crayon",
    "éclat de cartable",
    "éclat de casserole",
    "éclat de nappe",
    "éclat de wagon",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de pinceau",
    "éclat de farine",
    "point de gouttière",
    "point de gouttiere",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de pli",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_montrer_l_oiseau_maintenant; "
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
            "destinataire=enfant; sous_texte=elle_leve_la_main_puis_on_l_entend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de pli",
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
        emphasis="éclat de pli",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_l_aile; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "attendre",
    "accepted_examples": (
        "attendre | elle attend | lever la main | la main"
    ),
    "retry_prompt": "Elle lève la main et elle attend. Que fait Nina ?",
    "engine_ok_text": "Oui, elle attend.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "rayon,chaussure,porte",
        [
            "narrateur|Un rayon de soleil traverse la cuisine.",
            "narrateur|La poussière danse dans la lumière.",
            "narrateur|Le plancher de bois est tiède.",
            "narrateur|Le tablier de maman sent le savon.",
            "narrateur|Un pied nu touche le bois.",
            "narrateur|La chaleur monte sous le pied, lente.",
            "narrateur|Un fil de poussière va jusqu'au tablier.",
            "narrateur|Un oiseau en papier attend près du sac.",
            "enfant-f|Il a des ailes roses, maman.",
            "maman|C'est le papier, sous le rayon.",
            "papa|Tes chaussettes sont près du banc.",
            "narrateur|Papa glisse les chaussures, une, deux.",
            "enfant-f|La gauche d'abord.",
            "papa|Oui, la gauche.",
            "narrateur|Le lacet fait un petit nœud.",
            "maman|Ton sac est prêt.",
            "maman|L'oiseau en papier est dedans.",
            "narrateur|Sur une aile, un éclat de pli brille.",
            "enfant-f|Je le vois, papa !",
            "enfant-f|Je veux le montrer, maintenant !",
            "papa|On marche, Nina ?",
            "enfant-f|Je le sors !",
            "narrateur|Nina tire l'oiseau en papier trop vite.",
            "narrateur|L'oiseau en papier glisse, presque.",
            "narrateur|Les mots se cognent à ceux de papa.",
            "narrateur|Personne ne tourne la tête vers elle.",
            "enfant-f|Oh.",
            "narrateur|L'éclat de pli tremble, puis tient.",
            "narrateur|Le sourire de Nina s'en va.",
            "narrateur|Dans sa poitrine, ça tape fort.",
            "narrateur|L'envie pousse, puis l'inquiétude.",
            "enfant-f|Ça ne veut pas.",
            "narrateur|Ses épaules tombent un peu, lourdes.",
            "narrateur|Papa se met à sa hauteur.",
            "papa|Tu veux le montrer ?",
            "enfant-f|Oui, papa.",
            "maman|Tu mets tes chaussures ?",
            "enfant-f|D'accord, maman.",
            "narrateur|Nina glisse un pied, puis l'autre.",
            "narrateur|Le banc est lisse, un peu froid.",
            "papa|On marche vers la porte.",
            "narrateur|Le soleil tape sur le chemin.",
            "narrateur|Nina serre le sac contre elle.",
            "enfant-f|Il est là, dedans.",
            "papa|Oui, dans le sac.",
            "narrateur|Une abeille passe près de la haie.",
            "maman|Au revoir, Nina.",
            "enfant-f|Au revoir, maman.",
            "papa|On t'attend à la porte.",
            "narrateur|En ce moment, Nina s'assoit.",
            "narrateur|Le coussin vert est à sa place.",
            "narrateur|Le tissu vert est doux sous les genoux.",
            "narrateur|La classe sent le papier sec.",
            "narrateur|Ça sent le bois, près des chaises.",
            "narrateur|Une chaise grince près du mur, un peu.",
            "narrateur|Nina pose les genoux sur le tissu.",
            "narrateur|Un oiseau en papier tourne au plafond.",
            "narrateur|La ficelle fait un petit bruit.",
            "narrateur|Nina pose le sac contre le pied.",
            "narrateur|L'oiseau en papier reste dedans.",
            "narrateur|Elle regarde l'oiseau du plafond.",
            "narrateur|Les ailes roses, comme les siennes.",
            "narrateur|La maîtresse parle près du mur.",
            "narrateur|Nina a une idée, très nette.",
            "narrateur|Le chien de la maison est brun.",
            "enfant-f|Je veux parler du chien.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nina veut parler.",
            "narrateur|Que fait-elle d'abord ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "coussin,porte",
        [
            "narrateur|Nina ouvre la bouche trop vite.",
            "enfant-f|Mon chien est brun !",
            "narrateur|Un camarade parle, près du coussin.",
            "copain|Le chat est noir.",
            "narrateur|Les deux voix se mélangent dans l'air.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Nina ne revient pas.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Elle referme la bouche, un instant.",
            "narrateur|Elle lève la main, près du coussin.",
            "narrateur|Sa main reste en l'air.",
            "narrateur|Le camarade finit sa phrase, loin.",
            "narrateur|Un autre mot arrive, plus loin.",
            "narrateur|Nina garde la main haute, sans bouger.",
            "narrateur|Nina attend que le silence arrive.",
            "narrateur|Elle ouvre un peu le sac.",
            "narrateur|Sur l'aile, l'éclat de pli brille.",
            "enfant-f|Je peux dire quelque chose ?",
            "narrateur|La classe tourne un peu la tête.",
            "enfant-f|Le chien est brun.",
            "enfant-f|Il a les oreilles douces.",
            "narrateur|Elle pose l'oiseau près du coussin.",
            "narrateur|Les ailes roses regardent le plafond.",
            "narrateur|Plus tard, la porte s'ouvre.",
            "maman|Te voilà, Nina.",
            "papa|Le sac sent le papier.",
            "narrateur|Nina pose le sac près du banc.",
            "enfant-f|J'ai parlé du chien.",
            "enfant-f|Il a les oreilles douces.",
            "papa|Merci, Nina.",
            "narrateur|Papa a entendu toute la phrase.",
            "maman|Tu veux voir le chien ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le ventre de Nina se desserre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "chien_bonjour,papier",
        [
            "narrateur|Le chien brun vient tout près.",
            "narrateur|Nina veut tout montrer, d'un coup.",
            "narrateur|Elle prend l'oiseau en papier.",
            "enfant-f|Regarde, les ailes !",
            "narrateur|Elle déplie l'aile trop vite.",
            "narrateur|Le papier craque sous les doigts, un peu.",
            "narrateur|L'aile s'ouvre trop, d'un coup.",
            "enfant-f|Ça tombe !",
            "narrateur|Nina veut foncer, d'un coup.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Ses épaules se serrent un peu.",
            "narrateur|Ça tape fort, dans sa poitrine.",
            "narrateur|Personne ne dit la suite à voix haute.",
            "narrateur|Elle regarde l'oiseau en papier.",
            "narrateur|Elle écoute la cuisine, un instant.",
            "narrateur|La poussière danse dans le rayon.",
            "narrateur|Le pli de l'aile est trop ouvert.",
            "enfant-f|Comme ce matin ?",
            "papa|Tu le vois, toi ?",
            "enfant-f|Non, plus sur l'aile.",
            "narrateur|Nina plie l'aile, sans se presser.",
            "enfant-f|Il est là.",
            "papa|Sur cette aile ?",
            "enfant-f|Oui, sur ce pli.",
            "narrateur|L'éclat de pli revient, sur l'aile.",
            "maman|Le chien, Nina ?",
            "enfant-f|Oui.",
            "narrateur|Elle s'assoit près du chien.",
            "narrateur|Le chien pose le nez tout près.",
            "narrateur|Les oreilles sont chaudes, un peu.",
            "enfant-f|C'est doux.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "chien_bonjour",
        [
            "narrateur|L'oiseau en papier attend près du banc.",
            "narrateur|Le rayon reste dans la cuisine.",
            "enfant-f|L'éclat est là, papa.",
            "papa|Tu le vois sur le pli ?",
            "enfant-f|Oui, papa.",
            "maman|On est bien, ici.",
            "narrateur|Le tablier de maman sent le savon.",
            "narrateur|Le plancher de bois est tiède.",
            "enfant-f|On m'a entendue.",
            "maman|On t'a entendue, Nina.",
            "enfant-f|Oui, maman.",
            "narrateur|Nina pose la joue près des ailes.",
            "narrateur|Le papier est sec, un peu rêche.",
            "enfant-f|C'est froid.",
            "narrateur|Le chien ferme un peu les yeux.",
            "narrateur|L'éclat de pli tient sur l'aile.",
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
            if re.search(rf"(?<!\w){re.escape(bad)}(?!\w)", low):
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
    if n_clue != 5:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 5)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "delphine" in blob:
        raise SystemExit(f"{SID}: Delphine (BAD_NAMES)")
    if "maitresse|" in blob or "maîtresse|" in blob:
        raise SystemExit(f"{SID}: maîtresse parle (label seulement)")
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
        "- **Public :** N1 (≤10, viser ~8), audio familial\n"
        "- **Leçon :** COL.ECO.002 — attendre / lever la main avant de "
        "parler (vécue : veut montrer l'oiseau maintenant ; tire trop vite ; "
        "à la classe ouvre trop tôt ; refuse de foncer ; main levée ; "
        "silence ; phrase entendue)\n"
        "- **Personnages :** Nina, papa, maman. Troupe D16. Maîtresse = "
        "label dump (près du mur), pas de leçon récitée, pas de réplique. "
        "Papa parle (ajout). Delphine absent.\n"
        "- **Lieu :** cuisine (rayon, poussière, plancher, tablier), classe "
        "au coussin vert, puis maison. Oiseau en papier, ailes roses, "
        "chien brun. ≠ COL.ECO.002-01..06 (carotte, seau, carton, mousse, "
        "pompon, manteau). ≠ jardin au linge (xlsx intermédiaire).\n"
        "- **Indice unique :** éclat de pli (aile du matin → tremble → "
        "brille au silence → revient après le dépli trop vite → tient "
        "sur l'aile).\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un rayon traverse la cuisine. La poussière danse. Le plancher "
        "est tiède. Le tablier sent le savon. Sur une aile, un éclat de "
        "pli brille. Nina veut montrer l'oiseau **maintenant**. Première "
        "idée : le sortir d'un coup, parler par-dessus papa. L'oiseau "
        "glisse, les mots se perdent. Sourire parti, épaules basses. "
        "Papa se met à sa hauteur. À la classe, l'oiseau du plafond : "
        "elle veut parler du chien brun. Elle ouvre trop vite : un "
        "camarade parle du chat. Elle refuse de foncer, lève la main, "
        "attend, dit les oreilles douces. Merci vécu. Elle déplie trop "
        "vite : l'éclat manque. Elle refuse, replie. L'éclat de pli "
        "tient sur l'aile.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine, rayon, poussière, plancher tiède, tablier, "
        "banc, sac, coussin vert, plafond, ficelle, chien brun.\n"
        "- Désir : montrer l'oiseau en papier, parler du chien, "
        "maintenant.\n"
        "- Objet : oiseau en papier aux ailes roses, sac, coussin, chien.\n"
        "- Indice unique : éclat de pli, vu dès l'ouverture, payé à "
        "la fin.\n"
        "- Urgence douce : les mots prêts, la classe, le chien tout près.\n"
        "- Imprévu 1 : elle tire trop vite ; à la classe, elle coupe "
        "le camarade.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : tout montrer d'un coup ; elle déplie "
        "trop vite, l'éclat quitte l'aile.\n"
        "- Résolution : elle refuse de foncer, lève la main, attend, "
        "parle, replie.\n"
        "- Retour : joue près des ailes, rayon, tablier, éclat du début "
        "sur l'aile.\n\n"
        "## Vécu\n\n"
        "Nina veut montrer l'oiseau **maintenant**. Impatience, puis "
        "sourire qui s'en va. Un camarade parle ; elle veut parler. "
        "Papa se met à sa hauteur, pose une question, ne récite pas la "
        "règle. Nina agit : bouche fermée, main levée, phrase entière. "
        "Merci vécu après l'écoute. Fin : l'éclat du début tient sur "
        "l'aile.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau : L'oiseau en papier de Nina (pas Le chien et "
        "le linge). Lieu du dump cuisine : rayon, poussière, plancher, "
        "tablier, puis classe. Relance : Nina veut parler. Que fait-elle "
        "d'abord ? expected attendre. retry Delphine→Nina.\n"
        "- Ouverture inventée (rayon, poussière, pied nu sur le bois), "
        "pas un gabarit v2, pas « joue au salon », pas « est dans "
        "l'entrée ».\n"
        "- Indice unique : éclat de pli (papier/oiseau). Pas carotte/"
        "seau/carton/mousse/pompon/manteau. Pas grains, pas lune "
        "d'étain. Ban tapis, crochet, crayon, buée, croûte, tableau, "
        "casier, moufle, craie, cartable, pinceau, casserole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` "
        "retirés. Delphine retiré (BAD_NAMES).\n"
        "- Leçon non dite : on l'entend quand elle lève la main et "
        "attend. Pas « il faut attendre », pas « tu as attendu », pas "
        "de leçon maîtresse.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Papa parle. Maîtresse = label, pas de réplique.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Obstacle plus tendu au dépli.\n"
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
