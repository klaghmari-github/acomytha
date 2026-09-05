#!/usr/bin/env python3
"""ATOM-COL.ECO.002-10 — F-NAR-019. Le livre d'Amir sous l'oreiller. N3. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-COL.ECO.002-10"
N3 = LIMITS["N3"]
TITLE = "Le livre d'Amir sous l'oreiller"
INDICE = "éclat de page"
FIL = (
    "Un papillon de nuit tape le lampadaire. Sous l'oreiller, un livre a "
    "dormi. Sur une page, un éclat de page brille. Amir veut raconter le "
    "nuage bateau, maintenant. Il parle trop vite : les mots se perdent. "
    "Il ouvre trop vite : les pages claquent. Il refuse de foncer, lève "
    "la main, attend, puis dit. Merci vécu. Sous l'oreiller, l'éclat de "
    "page tient."
)
CHARS = "Amir, papa, maman"
SETTING = "chambre à la lampe orange, classe, tapis, coin des livres"
TIC_PHRASES = (
    "tout doux",
    "tout calme",
    "tout lent",
    "tout bas",
    "tout doucement",
)
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
    "ninon",
    "brice",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai levé la main",
    "j'ai leve la main",
    "j'ai attendu",
    "j'ai su attendre",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "on va ranger",
    "on range les feutres",
    "tu ranges",
    "tu as bien écouté",
    "tu as bien ecoute",
    "on aime écouter",
    "on aime ecouter",
    "écoute la maîtresse",
    "ecoute la maitresse",
    "tu as bien fait",
    "bon travail",
    "une chose, puis",
    "une chose puis",
    "il faut attendre",
    "tu attends ton tour",
    "c'est ton tour",
    "on doit demander",
    "tu as attendu",
    "comme un secret",
    "gouttière",
    "gouttiere",
    "croûte",
    "croute",
    "casier",
    "moufle",
    "craie",
    "cartable",
    "pinceau",
    "casserole",
    "grain de",
    "éclat de carotte",
    "éclat de seau",
    "éclat de carton",
    "éclat de mousse",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de terre",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
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
    "éclat de nappe",
    "éclat de boîte",
    "éclat de boite",
    "éclat de farine",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de laine",
    "éclat de orange",
    "éclat de lampe",
    "éclat de citron",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de pin",
    "éclat de crayon",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de craie",
    "éclat de tapis",
    "éclat de moufle",
    "éclat de casier",
    "éclat de tableau",
    "éclat de cartable",
    "éclat de pinceau",
    "éclat de crochet",
    "éclat de buée",
    "éclat de buee",
    "pli de voile",
    "point de gouttière",
    "point de gouttiere",
    "trait de craie",
    "trait de vitre",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "malaise",
    "lune d'étain",
    "lune d'etain",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de page",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_raconter_le_bateau_maintenant; "
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
            "sous_texte=il_leve_la_main_avant_de_parler; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="main",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_attend_puis_dit_le_nuage_bateau; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="livre",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_couper_papa; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de page",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sous_l_oreiller; "
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
    "narrateur|Un papillon de nuit tape le lampadaire.",
    "narrateur|Toc, toc, contre l'abat-jour.",
    "narrateur|La petite lampe orange fait un rond sur le mur.",
    "narrateur|Amir connaît ce rond.",
    "narrateur|La chambre sent le papier et la laine.",
    "narrateur|Sous l'oreiller, un livre a dormi.",
    "narrateur|Les pages sentent le papier, un peu chaud.",
    "narrateur|Derrière la vitre, un nuage blanc passe.",
    "narrateur|Sur une page, un éclat de page brille.",
    "enfant-m|Il est blanc, papa.",
    "papa|C'est le bateau du livre.",
    "maman|Le livre va dans le sac, à plat.",
    "enfant-m|Il a dormi sous l'oreiller.",
    "papa|Tes chaussures, Amir.",
    "papa|Je fais le nœud.",
    "maman|Tu as vu le nuage, par la fenêtre ?",
    "enfant-m|Il ressemblait à un bateau.",
    "enfant-m|Un bateau blanc, dans le ciel.",
    "enfant-m|Je veux le raconter, maintenant !",
    "papa|Tu pourras le raconter.",
    "narrateur|Papa parle près du sac, une main sur le tissu.",
    "enfant-m|Le nuage est un bateau !",
    "narrateur|Amir ouvre trop vite.",
    "narrateur|Les pages claquent, puis se froissent.",
    "narrateur|L'éclat de page saute près de l'oreiller.",
    "narrateur|Les mots se cognent à ceux de papa.",
    "enfant-m|Oh.",
    "narrateur|Le sourire d'Amir disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "enfant-m|Ça ne veut pas.",
    "narrateur|Ses épaules tombent un peu.",
    "narrateur|Papa s'accroupit à la même hauteur.",
    "papa|Tu veux le montrer ?",
    "enfant-m|Oui, papa.",
    "maman|Tes pieds sont dans les chaussures ?",
    "enfant-m|Oui, maman.",
    "papa|Tu tiens ma manche ?",
    "enfant-m|Oui.",
    "maman|On y va ?",
    "enfant-m|On y va.",
    "enfant-m|Au revoir, maman.",
    "maman|Au revoir, Amir.",
    "narrateur|Dehors, le chemin sent le pain du fournil.",
    "narrateur|Le sac tape la hanche, un peu.",
    "maman|On marche.",
    "narrateur|La classe sent le papier et le bois.",
    "narrateur|Au fond, le coin des livres a une lampe.",
    "narrateur|La lumière est orange, comme à la maison.",
    "papa|Au revoir, Amir.",
    "papa|On revient.",
    "enfant-m|Au revoir, papa.",
    "maman|Tu poses le sac près du tapis.",
    "narrateur|En ce moment, Amir s'assoit sur le tapis.",
    "narrateur|Le tapis est un peu froid, sous les genoux.",
    "narrateur|Le livre reste dans le sac.",
    "maitresse|Bonjour.",
    "enfant-m|Bonjour, maîtresse.",
    "narrateur|Amir pose les mains sur ses genoux.",
    "narrateur|Près du tapis, une image montre un ciel.",
    "narrateur|Un camarade parle d'un oiseau.",
    "enfant-m|Je veux parler du bateau.",
]

Q0001 = [
    "narrateur|Amir veut parler.",
    "narrateur|Que fait-il d'abord ?",
]

C0001 = [
    "narrateur|Amir ouvre la bouche trop vite.",
    "enfant-m|Le nuage est un bateau, maintenant !",
    "narrateur|Un camarade parle, près de l'image.",
    "copain|J'ai vu un oiseau.",
    "narrateur|Les deux voix se mélangent.",
    "enfant-m|Oh.",
    "narrateur|Personne ne tourne la tête.",
    "narrateur|Le sourire ne revient pas.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Il referme la bouche.",
    "narrateur|Il lève la main, près du tapis.",
    "narrateur|Sa main reste en l'air.",
    "narrateur|Le camarade finit sa phrase.",
    "narrateur|Amir attend que le silence arrive.",
    "narrateur|Dans le sac, l'éclat de page brille.",
    "enfant-m|Je peux dire quelque chose ?",
    "narrateur|Une tête se tourne vers lui.",
    "enfant-m|Le nuage est blanc.",
    "enfant-m|Il ressemblait au bateau du livre.",
    "enfant-m|Le livre a dormi sous l'oreiller.",
    "narrateur|Les oreilles écoutent jusqu'au bout.",
    "narrateur|Plus tard, au coin des livres, la lampe est allumée.",
    "narrateur|Amir ouvre son livre.",
    "narrateur|Les pages sont un peu chaudes.",
    "enfant-m|Je veux montrer le bateau.",
    "narrateur|Il lève trop vite une page.",
    "narrateur|La page se plie, presque.",
    "enfant-m|Oh.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Il referme la page.",
    "narrateur|Il attend, les mains à plat.",
    "maitresse|Amir.",
    "enfant-m|Le bateau est blanc.",
    "enfant-m|Comme le rond de la lampe.",
    "narrateur|Le soir, la porte s'ouvre.",
    "papa|Te voilà, Amir.",
    "maman|Le sac est rentré.",
    "narrateur|Amir pose le sac près de l'oreiller.",
    "enfant-m|Le nuage était un bateau.",
    "enfant-m|Comme dans le livre.",
    "papa|Merci, Amir.",
    "narrateur|Papa a entendu toute la phrase.",
    "maman|Tu veux de l'eau ?",
    "enfant-m|Oui, maman.",
    "narrateur|Le ventre d'Amir se desserre.",
]

END = [
    "narrateur|Amir veut tout dire, d'un coup.",
    "narrateur|Il saisit le livre trop vite.",
    "narrateur|Les pages glissent vers le sol.",
    "enfant-m|Ça tombe !",
    "narrateur|Amir veut foncer, d'un coup.",
    "narrateur|Amir refuse de foncer.",
    "narrateur|Ses épaules se serrent un peu.",
    "narrateur|Ça tape, dans sa poitrine.",
    "narrateur|Personne ne dit la suite.",
    "narrateur|Il regarde le livre ouvert.",
    "narrateur|Il écoute la chambre, un instant.",
    "narrateur|La lampe orange tremble, un peu.",
    "enfant-m|Comme ce matin, papa !",
    "papa|Tu le vois, toi ?",
    "enfant-m|Oui, sur la page.",
    "narrateur|Amir pose le livre, plus lentement.",
    "narrateur|Il glisse le livre sous l'oreiller.",
    "maman|L'oreiller est à sa place ?",
    "enfant-m|Oui, maman.",
    "papa|Tes pieds sont près du lit ?",
    "enfant-m|Oui, papa.",
    "narrateur|Il s'assoit au bord.",
    "narrateur|Les pages se calment.",
    "narrateur|Le papillon n'est plus là.",
    "papa|Il est parti.",
    "enfant-m|Le bateau, lui, reste dans le livre.",
]

FIN = [
    "narrateur|Ils restent près du lit.",
    "narrateur|Le livre repose sous l'oreiller.",
    "enfant-m|L'éclat est là, papa.",
    "papa|Tu le vois sur la page ?",
    "enfant-m|Oui, papa.",
    "maman|On est bien, ici.",
    "narrateur|La lampe orange fait un rond, plus petit.",
    "narrateur|Le sac sent le papier, un peu.",
    "enfant-m|On m'a entendu.",
    "maman|On t'a entendu, Amir.",
    "enfant-m|Oui, maman.",
    "narrateur|Amir pose la joue près des pages.",
    "narrateur|Les pages sont tièdes, un peu.",
    "enfant-m|C'est chaud.",
    "papa|Tu le sens sur tes joues ?",
    "enfant-m|Oui, il est tiède.",
    "narrateur|Dehors, le fournil s'endort.",
    "narrateur|L'éclat de page tient sur la page.",
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
            by_src["CHK_T0000_P0000"], P0000, "opening", "pages,lampe",
        ),
        "CHK_T0000_P0000_Q0001": voice(
            by_src["CHK_T0000_P0000_Q0001"], Q0001, "clue", "",
            extra={
                "pause_before_ms": 200,
                "fields": {
                    "expected_answer": "attendre",
                    "accepted_examples": (
                        "attendre | il attend | lever la main | la main"
                    ),
                    "retry_prompt": (
                        "Il lève la main et il attend. Que fait Amir ?"
                    ),
                    "engine_ok_text": "Oui, il attend.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": voice(
            by_src["CHK_T0000_P0000_C0001"], C0001, "resolution", "pages",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END": voice(
            by_src["CHK_T0000_P0000_END"], END, "action", "pas,pages",
            extra={"pause_before_ms": 200},
        ),
        "CHK_T0000_P0000_END_F0001": voice(
            by_src["CHK_T0000_P0000_END_F0001"], FIN, "ending", "",
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
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "brice" in blob:
        raise SystemExit(f"{SID}: Brice interdit")
    if "ninon" in blob:
        raise SystemExit(f"{SID}: Ninon interdite")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    tts_ok = all(
        c.get("text_xai_tags")
        and c.get("notes")
        and c.get("style_energy")
        and c["text_xai_tags"] != c["text"]
        and str(c["text_ssml"]).startswith("<speak>")
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
    qtext = by["CHK_T0000_P0000_Q0001"]["text"]
    if qtext != "Amir veut parler. Que fait-il d'abord ?":
        raise SystemExit(f"{SID}: question moteur altérée: {qtext}")
    if by["CHK_T0000_P0000_Q0001"].get("expected_answer") != "attendre":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = by["CHK_T0000_P0000_Q0001"].get("retry_prompt") or ""
    if "brice" in retry.lower():
        raise SystemExit(f"{SID}: retry Brice")
    if "amir" not in retry.lower():
        raise SystemExit(f"{SID}: retry sans Amir")
    mait = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("maitresse|")
    ).lower()
    if any(x in mait for x in ("écoute", "range", "merci", "règle", "leçon", "tour")):
        raise SystemExit(f"{SID}: maîtresse leçon parlée: {mait}")

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
        "- **Leçon :** COL.ECO.002 — attendre son tour / lever la main "
        "avant de parler (vécue : parler trop vite → mots perdus ; ouvrir "
        "trop vite → pages qui claquent ; lever la main, attendre, puis "
        "dire)\n"
        "- **Personnages :** Amir, papa, maman (maîtresse = label, pas de "
        "leçon parlée). Dump xai Brice → Amir. Troupe D16.\n"
        "- **Lieu :** chambre à la lampe orange, classe, tapis, coin des "
        "livres ; livre sous l'oreiller, pages, papillon de nuit, nuage "
        "bateau\n"
        "- **Indice unique :** éclat de page (page du matin → saute près "
        "de l'oreiller → brille dans le sac → tient sous l'oreiller)\n"
        "- **Question moteur :** Amir veut parler. Que fait-il d'abord ? "
        "→ attendre (lever la main). retry : Que fait Amir ?\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un papillon de nuit tape le lampadaire. La lampe orange fait un "
        "rond. Amir connaît ce rond. Sous l'oreiller, un livre a dormi. "
        "Sur une page, un éclat de page brille. Le nuage de la fenêtre "
        "ressemble au bateau du livre. Amir veut le raconter "
        "**maintenant**. Il coupe papa : les voix se mélangent. Il ouvre "
        "trop vite : les pages claquent, l'éclat saute. Sourire parti, "
        "épaules basses. Papa s'accroupit. À la classe, sur le tapis, une "
        "voix parle d'un oiseau. Il dit le bateau tout de suite : les mots "
        "se cognent, personne n'entend. Il refuse de foncer, lève la main, "
        "reste, dit le nuage bateau. Une tête se tourne. Au coin des "
        "livres, une page trop vite : il refuse, attend, dit. Merci vécu. "
        "Le soir, il saisit trop vite, les pages glissent. Il refuse, "
        "glisse le livre sous l'oreiller. L'éclat de page tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chambre, papillon, lampe orange, oreiller, pages, "
        "vitre, nuage, fournil, classe, tapis, coin des livres.\n"
        "- Désir : raconter le nuage bateau, montrer le bateau du livre, "
        "maintenant.\n"
        "- Objet : livre sous l'oreiller, pages, sac, lampe, tapis.\n"
        "- Indice unique : éclat de page, vu dès l'ouverture, payé à la "
        "fin.\n"
        "- Urgence douce : les mots prêts, la classe qui parle du ciel.\n"
        "- Imprévu 1 : il coupe papa ; les pages claquent. À la classe, "
        "il coupe le camarade.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : tout dire d'un coup ; les pages "
        "glissent vers le sol.\n"
        "- Résolution : il refuse de foncer, lève la main, attend, parle.\n"
        "- Retour : joue près des pages, éclat du début sous l'oreiller.\n\n"
        "## Vécu\n\n"
        "Amir veut raconter le nuage bateau **maintenant**. Impatience, "
        "puis épaules qui tombent quand les mots se perdent. Papa "
        "s'accroupit, pose une question, ne récite pas la règle. Amir "
        "agit : bouche fermée, main en l'air, phrase entière. Merci vécu "
        "après l'écoute. Fin : l'éclat du début tient sur la page, le "
        "livre sous l'oreiller.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre mission « Le livre d'Amir sous l'oreiller » (xlsx : "
        "« Le nuage bateau d'Amir »). Monde dump : classe, tapis, coin "
        "des livres, livre sous l'oreiller, pages, lampe orange, nuage "
        "bateau, papillon, fournil.\n"
        "- Héros Amir. Dump xai Brice → INTERDIT. retry Brice→Amir. "
        "Maman parlante (dump xlsx a papa+maman ; characters writer = "
        "Amir, papa, maman).\n"
        "- Ouverture inventée (papillon contre l'abat-jour, rond connu, "
        "livre nouveau sous l'oreiller), pas « joue au salon », pas "
        "gabarit v2.\n"
        "- Distinct de COL.ECO.002-01 carotte/cuisine. ≠ 002-02 seau/"
        "coquille. ≠ 002-03 carton/farine. ≠ 002-04 mousse/pomme de pin. "
        "≠ 002-05 pompon. ≠ 002-06 manteau. ≠ 002-07 oiseau en papier. "
        "≠ 002-08 feuille brune. ≠ 002-09 poisson.\n"
        "- Maîtresse = label (bonjour, Amir), pas de leçon parlée. Pas "
        "« il faut attendre / c'est ton tour / tu as attendu ».\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent / "
        "tout bas » retirés. Pas de merle, pas de miel, pas de secret.\n"
        "- Merci vécu. Questions d'adultes. Un « en ce moment ».\n"
        "- Indice unique « éclat de page » nommé à l'ouverture, revu "
        "quand il saute, revu dans le sac, payé à la fin.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive.\n"
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
