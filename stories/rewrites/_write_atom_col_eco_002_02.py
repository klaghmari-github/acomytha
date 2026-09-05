#!/usr/bin/env python3
"""ATOM-COL.ECO.002-02 — La mer dans la coquille (F-NAR-019, N3, COL.ECO.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.002-02"
TITLE = "La mer dans la coquille"
N3 = LIMITS["N3"]
INDICE = "éclat de seau"
CHARS = "Nino, papa, maman"
SETTING = (
    "entrée, classe, puis maison, grains de sable sur le paillasson, "
    "seau en fer, bottes, odeur de bord de mer"
)
FIL = (
    "Le paillasson gratte. Sur le fer, un éclat de seau luit. "
    "Nino veut parler de la mer dans la coquille, maintenant. "
    "Les mots se cognent à la classe. À la maison, près du seau, "
    "il parle trop vite. Il refuse de foncer, lève la main, attend. "
    "Merci vécu. Un éclat de seau reste pâle."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
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
    "trois notes",
    "une chose, puis la suivante",
    "une chose puis l'autre",
    "une étape après l'autre",
    "yasmine",
    "radiateur",
    "carotte",
    "casserole",
    "cuisine",
    "éclat de coquille",
    "éclat de casier",
    "éclat de laine",
    "éclat de marche",
    "éclat de nappe",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de crayon",
    "éclat de cuillère",
    "éclat de cuillere",
    "c'est du bon travail",
    "tu as fait du bon travail",
    "on aime écouter",
    "même leçon",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "tu as attendu",
    "on lève la main",
    "on doit demander",
    "tache de couleur",
    "ombre en forme de flèche",
    "marque fine",
    "minuscule symbole",
    "grain de miette",
    "grain de laine",
    "bande bleue",
    "on écoute d'abord",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de seau",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_parler_maintenant; "
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
            "sous_texte=il_leve_la_main_et_attend; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="seau",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_porte_echoue_la_main_tient; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de seau",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_sans_regarder_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de seau",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pale; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "attendre",
    "accepted_examples": (
        "attendre | il attend | lever la main | la main"
    ),
    "retry_prompt": "Il lève la main et il attend. Que fait Nino ?",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "seau,bottes",
        [
            "narrateur|Le paillasson gratte sous les pieds.",
            "narrateur|Des grains de sable restent dans les fibres.",
            "narrateur|Ils piquent un peu, très fins.",
            "narrateur|Un seau en fer est près des bottes.",
            "narrateur|Sur le fer, un éclat de seau luit.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, sur le seau ?",
            "narrateur|Le seau sent le bord de mer.",
            "narrateur|Les bottes sont rêches, un peu salées.",
            "enfant-m|Ça sent la mer.",
            "maman|Tes mains sont froides, Nino.",
            "enfant-m|Je veux entendre la mer.",
            "enfant-m|Dans une coquille.",
            "papa|On va à l'école.",
            "maman|Le cartable est près de la porte.",
            "enfant-m|Oui, maman.",
            "narrateur|Papa aide Nino à passer les bras.",
            "narrateur|Le manteau sent un peu le sel.",
            "papa|Je reviens te chercher.",
            "enfant-m|Oui, papa.",
            "narrateur|Papa serre l'épaule de Nino.",
            "narrateur|Ils poussent la porte de l'école.",
            "narrateur|La classe sent les feuilles.",
            "narrateur|Un tapis de laine attend sous la fenêtre.",
            "maitresse|Bonjour.",
            "enfant-m|Bonjour, maîtresse.",
            "narrateur|Nino pose le cartable près du tapis.",
            "narrateur|Il s'assoit, le dos droit.",
            "narrateur|La maîtresse pose une boîte sur la table.",
            "narrateur|Elle ouvre le couvercle, sans un mot.",
            "narrateur|Une coquille crème apparaît.",
            "narrateur|Elle a des lignes, un peu rêche.",
            "enfant-m|La mer est dedans !",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "enfant-m|Je le dis, maintenant !",
            "narrateur|En ce moment, Nino ouvre la bouche.",
            "narrateur|Ses mots se cognent à la classe.",
            "narrateur|Un camarade parle près de la boîte.",
            "narrateur|Personne ne tourne la tête.",
            "enfant-m|Oh.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Nino referme la bouche.",
            "narrateur|Les mains restent sur les genoux.",
            "narrateur|À la sortie, papa attend près de la porte.",
            "papa|On rentre, Nino ?",
            "enfant-m|Oui.",
            "narrateur|Le soir, le paillasson gratte de nouveau.",
            "narrateur|Nino touche l'éclat de seau, un instant.",
            "maman|Te voilà, Nino.",
            "papa|Les bottes sont là.",
            "enfant-m|J'ai quelque chose, maintenant !",
            "narrateur|Nino avance trop vite vers le seau.",
            "narrateur|Maman accroche le manteau.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino veut parler.",
            "narrateur|Que fait-il d'abord ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "confirm",
        "manteau,seau",
        [
            "narrateur|Nino parle trop vite, près du seau.",
            "enfant-m|Maman, la mer est dedans !",
            "narrateur|Maman n'a pas fini sa phrase.",
            "maman|Le manteau est humide, Nino.",
            "narrateur|Les deux voix se mélangent.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Il refuse de foncer.",
            "narrateur|Nino referme la bouche.",
            "narrateur|Il lève la main, près des bottes.",
            "narrateur|Sa main reste en l'air.",
            "narrateur|Maman finit d'accrocher le manteau.",
            "narrateur|Nino garde la main haute.",
            "papa|Tu veux venir près du seau ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "narrateur|Nino pose un pied près du fer.",
            "narrateur|Le seau est froid, un peu salé.",
            "enfant-m|La coquille est crème.",
            "enfant-m|La mer est peut-être dedans.",
            "maman|On t'écoute.",
            "papa|Merci, Nino.",
            "narrateur|Papa a entendu toute la phrase.",
            "narrateur|Le ventre de Nino se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tu veux l'écouter ?",
            "enfant-m|Un peu, maman.",
            "narrateur|La lumière touche le fer.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "bottes,coquille",
        [
            "narrateur|Nino prend la coquille trop vite.",
            "enfant-m|Je dis tout, d'un coup !",
            "narrateur|Le seau bascule d'un cran.",
            "narrateur|Une botte glisse vers le paillasson.",
            "enfant-m|Oh.",
            "narrateur|Nino avance les mains.",
            "narrateur|Puis il s'arrête net.",
            "enfant-m|Attends, je regarde.",
            "narrateur|Papa reste là, sans parler.",
            "narrateur|Nino observe le fer, écoute la maison.",
            "narrateur|Sur le seau, un éclat de seau luit.",
            "enfant-m|Là, près des bottes.",
            "narrateur|Nino pose d'abord la coquille.",
            "narrateur|Puis il redresse le seau.",
            "enfant-m|La mer, c'était trop vite.",
            "papa|Tu veux l'écouter ici ?",
            "enfant-m|Oui, papa.",
            "narrateur|Nino s'assoit près du seau.",
            "enfant-m|Mes mots se sont cognés.",
            "maman|On est là.",
            "narrateur|La lumière de l'entrée touche le fer.",
            "narrateur|Nino pose la coquille contre l'oreille.",
            "narrateur|Un hush arrive, un peu froid.",
            "papa|Tu as fini ta phrase ?",
            "enfant-m|Presque.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "seau,coquille",
        [
            "enfant-m|Le seau brillait, papa.",
            "papa|Tu le vois, comme ce matin ?",
            "enfant-m|Oui, sur le fer.",
            "narrateur|Nino pose la coquille près du seau.",
            "maman|On la laisse là ?",
            "enfant-m|Oui, maman.",
            "narrateur|La lumière de l'entrée touche le fer.",
            "narrateur|Nino pose la coquille contre son oreille.",
            "narrateur|Un hush arrive, un peu salé.",
            "enfant-m|Je l'entends.",
            "narrateur|Les bottes restent près du paillasson.",
            "narrateur|Un éclat de seau reste pâle.",
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
    merged = dict(src)
    merged["fil_rouge"] = FIL
    merged["title"] = TITLE
    merged["characters"] = CHARS
    merged["setting"] = SETTING
    merged["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    nwords = sum(words(c["text"]) for c in merged["chunks"])
    blob = "\n".join(c["script"] for c in merged["chunks"]).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "il refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: refuse de foncer absent")
    if "yasmine" in blob:
        raise SystemExit(f"{SID}: Yasmine interdite")
    if "éclat de coquille" in blob:
        raise SystemExit(f"{SID}: éclat de coquille interdit")
    if "carotte" in blob or "cuisine" in blob:
        raise SystemExit(f"{SID}: 002-01 carotte/cuisine")
    merci_n = sum(
        1
        for ln in blob.splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
        if "merci" in ln or "bravo" in ln
    )
    if merci_n != 1:
        raise SystemExit(f"{SID}: merci/bravo ×{merci_n}")
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
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "## Promesse narrative\n\n"
        "Le paillasson gratte. Des grains de sable restent dans les fibres "
        "(monde, pas indice). Un seau en fer est près des bottes. Sur le fer, "
        "un éclat de seau luit. Ça sent le bord de mer. Nino veut entendre "
        "la mer dans une coquille, **maintenant**. En classe, la maîtresse "
        "(label : bonjour) pose une boîte. Une coquille crème. Il ouvre la "
        "bouche trop tôt. Les mots se cognent. Sourire parti, épaules basses. "
        "À la maison, près du seau, il parle trop vite. Les voix se mélangent. "
        "Il refuse de foncer. Il lève la main, près des bottes. Merci vécu. "
        "Deuxième ruse : tout dire d'un coup, le seau bascule, une botte "
        "glisse. Il s'arrête, lit l'éclat. Près du paillasson, un éclat de "
        "seau reste pâle. La mer hush dans la coquille.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : entrée, classe, puis maison. Paillasson, seau en fer, "
        "bottes, odeur de bord de mer. ≠ 002-01 carotte/cuisine. ≠ 001-05 "
        "casiers/chaussette/cacao. ≠ port/mouettes de l'ancienne version.\n"
        "- Désir : parler de la mer dans la coquille, maintenant.\n"
        "- Objet : seau en fer, bottes, coquille crème, paillasson.\n"
        "- Indice unique : éclat de seau, vu dès l'ouverture, payé pâle. "
        "Pas grain de sable (monde seulement). Pas éclat de coquille.\n"
        "- Urgence douce : les mots qui pressent, la mer à dire.\n"
        "- Imprévu 1 : parler pendant la classe, puis trop vite près du seau.\n"
        "- Cue : papa à la même hauteur, près du seau. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : tout dire d'un coup, seau et botte.\n"
        "- Résolution : il refuse de foncer, lève la main, attend.\n"
        "- Retour : coquille près du seau, hush, éclat de seau pâle.\n\n"
        "## Vécu\n\n"
        "Leçon COL.ECO.002 (attendre / lever la main avant de parler, "
        "jamais dite) greffée. La première idée (parler maintenant, près "
        "du seau) échoue. Le choix de Nino change l'action. Un « en ce "
        "moment ». Un merci vécu. Adulte + question. Troupe D16 : Nino, "
        "papa, maman. Maîtresse dump = label, pas de leçon parlée.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Lieu du dump : entrée, classe, puis "
        "maison, grains de sable sur paillasson, seau en fer, bottes, "
        "odeur de bord de mer. Sans radiateur, sans carotte, sans cuisine.\n"
        "- Ouverture inventée (paillasson qui gratte), pas un gabarit v2.\n"
        "- Indice unique : éclat de seau. Pas merle-trois-notes, miel, "
        "gouttes, pas tache/flèche/marque/symbole, pas éclat de "
        "coquille, pas grain de sable comme indice.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` retirés.\n"
        "- Question moteur inchangée (Nino veut parler. Que fait-il "
        "d'abord ?). 5 chunks, kinds inchangés.\n"
        f"- {nwords} mots. N3 ≤ 16. TTS : notes, ssml, xai, piper par chunk.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
