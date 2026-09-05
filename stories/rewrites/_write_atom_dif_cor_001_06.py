#!/usr/bin/env python3
"""ATOM-DIF.COR.001-06 — Le garage de la planche (F-NAR-019, N3, DIF.COR.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.001-06"
TITLE = "Le garage de la planche"
N3 = LIMITS["N3"]
CHARS = "Raphaël, Chouchou, papa, maman"
SETTING = "terrasse du soir, planche de résine, fil à linge"
INDICE = "éclat de planche"
FIL = (
    "Un torchon orange claque au fil. Sur le bord, un éclat de planche "
    "brille. Raphaël veut un garage pour le camion, maintenant, avec la "
    "caisse et la planche. Il pose trop haut : Chouchou n'atteint pas. "
    "Le camion tape. Sourire parti. Il refuse de foncer, baisse un bord. "
    "Ils jouent. Merci vécu. Il relève trop vite : ça glisse. Il refuse, "
    "baisse avec elle. L'éclat de planche tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(drap|cerceau|tunnel|pince|merle|miel)\b",
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
    "maîtresse",
    "maitresse",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "j'ai joué",
    "j'ai joue",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "c'est la règle",
    "tu as bien fait",
    "tu as su",
    "tailles différentes",
    "tailles differentes",
    "on peut jouer ensemble",
    "vous jouez ensemble",
    "on joue ensemble, c'est",
    "plus petit ou plus grand",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "éclat de pince",
    "éclat de cerceau",
    "éclat de drap",
    "éclat de fil",
    "éclat de caisse",
    "éclat de camion",
    "éclat de torchon",
    "éclat de dalle",
    "éclat de résine",
    "éclat de resine",
    "éclat de bois",
    "éclat de cube",
    "éclat de carton",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de manteau",
    "éclat de robinet",
    "éclat d'émail",
    "éclat d'email",
    "éclat de samare",
    "éclat de bassine",
    "éclat de figue",
    "éclat d'enveloppe",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de planche",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_garage_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Raphaël",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_joue_avec_elle_sans_poser_trop_haut; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="On joue",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_baisse_le_toit_ils_jouent; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de planche",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_sur_le_toit; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de planche",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bord; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer ensemble",
    "accepted_examples": (
        "jouer ensemble | jouer | inviter"
    ),
    "retry_prompt": "Ils jouent ensemble. Que fait Raphaël ?",
    "engine_ok_text": "Oui, ils jouent ensemble.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "linge,planche",
        [
            "narrateur|Un torchon orange claque au fil.",
            "enfant-m|Il claque, papa !",
            "papa|Tu l'entends, dans le vent ?",
            "enfant-m|Oui, un son court.",
            "narrateur|L'air du soir sent la résine, un peu tiède.",
            "enfant-m|Ça sent l'arbre, maman.",
            "maman|Tu le sens, près de la planche ?",
            "enfant-m|Oui, maman.",
            "narrateur|La planche de résine attend contre la caisse.",
            "narrateur|Sur le bord, un éclat de planche brille.",
            "enfant-m|Il brille, papa.",
            "papa|C'est le soir, sur la résine ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|Les dalles de la terrasse sont fraîches.",
            "enfant-m|Elles piquent les pieds.",
            "maman|On reste près de la caisse ?",
            "enfant-m|Oui, maman.",
            "narrateur|La lumière orange glisse sur les dalles.",
            "enfant-m|Elle est chaude, plus loin.",
            "papa|Le vent bouge le fil, Raphaël.",
            "enfant-m|Oui, papa.",
            "narrateur|Une caisse de bois attend près du mur.",
            "narrateur|Dedans, un camion de bois dort.",
            "enfant-m|Le camion !",
            "enfant-m|Ses roues sont rouges.",
            "papa|Tu le sors, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Raphaël sort le camion de la caisse.",
            "narrateur|Le bois est lisse, un peu chaud.",
            "enfant-m|Je veux un garage, maintenant !",
            "maman|Avec la caisse et la planche ?",
            "enfant-m|Oui, maman.",
            "papa|Le toit, c'est la planche ?",
            "enfant-m|Oui, papa.",
            "narrateur|Maman accroche un torchon au fil.",
            "maman|Le fil tient, ce soir.",
            "enfant-m|Il bouge.",
            "narrateur|Chouchou arrive sur les dalles.",
            "narrateur|Ses mains pendent plus bas, près du fil.",
            "enfant-m|Chouchou !",
            "enfant-f|J'arrive.",
            "enfant-m|Le garage, maintenant, Chouchou !",
            "narrateur|En ce moment, Raphaël pose la planche trop haut.",
            "narrateur|La planche tape le bord de la caisse.",
            "enfant-m|Pousse, tout de suite !",
            "narrateur|Raphaël attrape la manche de Chouchou.",
            "enfant-f|Non.",
            "narrateur|Chouchou recule vers le fil.",
            "enfant-m|Oh.",
            "narrateur|Chouchou pousse le camion, un peu.",
            "narrateur|Le camion tape le toit trop haut.",
            "enfant-m|C'est trop haut !",
            "enfant-f|Mes mains n'arrivent pas.",
            "narrateur|Le camion reste dehors, contre le bois.",
            "enfant-m|Oh.",
            "narrateur|L'éclat de planche tremble, puis tient.",
            "enfant-m|Il part.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Le toit est haut, Raphaël ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "enfant-m|Oui, papa.",
            "narrateur|La phrase se perd dans le vent du soir.",
            "narrateur|Personne n'entend la fin.",
            "maman|Chouchou est près du fil, Raphaël.",
            "enfant-m|Oui, maman.",
            "narrateur|Le camion reste lourd, entre leurs pieds.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Chouchou est plus petit.",
            "narrateur|Que fait Raphaël ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "roues",
        [
            "narrateur|Raphaël pose la planche trop haut, une fois.",
            "enfant-m|Pousse, Chouchou, maintenant !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Non.",
            "narrateur|Chouchou reste près du fil.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Raphaël refuse de foncer.",
            "narrateur|Il lâche la manche, un peu.",
            "papa|Le toit est haut, Raphaël ?",
            "narrateur|Papa reste à sa hauteur.",
            "maman|Les mains de Chouchou n'arrivent pas.",
            "narrateur|Maman n'a pas fini non plus.",
            "narrateur|Raphaël attend que le silence arrive.",
            "enfant-m|On joue, Chouchou ?",
            "enfant-m|Plus bas, si tu veux ?",
            "narrateur|Chouchou ne dit rien.",
            "narrateur|Elle regarde le camion, longtemps.",
            "enfant-f|Je regarde.",
            "enfant-m|D'accord.",
            "narrateur|Raphaël baisse un bord de la planche.",
            "narrateur|L'autre bord reste sur la caisse.",
            "narrateur|Le toit penche, assez bas.",
            "enfant-f|Je pousse.",
            "narrateur|Chouchou pousse le camion sans presser.",
            "narrateur|Les roues font un petit clic.",
            "enfant-m|Il est dedans !",
            "papa|Merci, Raphaël.",
            "narrateur|Papa a entendu toute la phrase.",
            "maman|Tu tiens le bord, des deux mains ?",
            "enfant-m|Oui, maman.",
            "enfant-f|Le camion est au garage.",
            "papa|Tu as entendu les roues ?",
            "enfant-m|Oui, papa.",
            "maman|On reste à la terrasse, Raphaël ?",
            "enfant-m|Oui.",
            "narrateur|Le camion sent le bois, un peu tiède.",
            "enfant-m|Il colle aux doigts.",
            "maman|Comme la résine, oui.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "linge",
        [
            "narrateur|Raphaël veut un toit plus haut.",
            "enfant-m|Un grand garage, maintenant !",
            "narrateur|Il relève la planche trop vite.",
            "narrateur|Le toit glisse sur la caisse.",
            "enfant-m|Oh.",
            "narrateur|Le camion tape le bord, puis recule.",
            "enfant-f|Il sort.",
            "enfant-m|Oh.",
            "narrateur|Les deux voix se mélangent.",
            "papa|La planche glisse, Raphaël.",
            "narrateur|Raphaël refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Il écoute la terrasse, un instant.",
            "narrateur|Il observe la planche, écoute le fil.",
            "narrateur|Sur le bord, un éclat de planche luit.",
            "enfant-m|Il est là.",
            "enfant-m|On baisse, si tu veux ?",
            "enfant-f|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Chouchou s'approche, sans se presser.",
            "narrateur|Raphaël baisse le bord, avec elle.",
            "narrateur|Le toit penche, assez bas pour deux.",
            "enfant-f|Je pousse.",
            "narrateur|Les roues passent sous la planche.",
            "narrateur|Ça fait toc.",
            "enfant-m|Il est dedans.",
            "papa|Tu restes un peu ?",
            "enfant-m|Oui, papa.",
            "maman|La planche est près de la caisse.",
            "enfant-m|On la laisse ?",
            "papa|Oui, contre le bois.",
            "narrateur|Un cube jaune attend près du mur.",
            "enfant-m|L'enseigne, plus bas ?",
            "enfant-f|Oui.",
            "narrateur|Ils posent le cube devant la caisse.",
            "enfant-m|C'est la porte, Chouchou.",
            "enfant-f|Le camion dort.",
            "maman|Le fil claque, au vent.",
            "enfant-m|Je l'entends.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "linge",
        [
            "narrateur|Ils restent près de la caisse.",
            "narrateur|Maman referme le bord, sans bruit.",
            "enfant-m|Comme un toit, papa.",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur le bord.",
            "maman|On est bien, ici.",
            "narrateur|Raphaël glisse le doigt, sans se presser.",
            "enfant-m|On le sent, maman.",
            "maman|Tu le sens sur tes doigts ?",
            "enfant-m|Oui, il colle.",
            "papa|Le toit est bas, Raphaël.",
            "enfant-m|Oui, avec Chouchou.",
            "enfant-f|Le camion dort.",
            "narrateur|L'odeur de résine reste sur la terrasse.",
            "enfant-m|Il est là, maman.",
            "maman|Oui, sur le bord.",
            "narrateur|L'éclat de planche tient sur le bord.",
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
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"extra {bad}: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-m", "enfant-f"):
            raise SystemExit(f"rôle {role}: {raw}")
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
    if "copain|" in blob or "copine|" in blob:
        raise SystemExit(f"{SID}: copain/copine (Chouchou = enfant-f)")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m", "enfant-f") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "enfant-f" for r in roles):
        raise SystemExit(f"{SID}: Chouchou absente (enfant-f)")
    if not any(r == "enfant-m" for r in roles):
        raise SystemExit(f"{SID}: Raphaël absent (enfant-m)")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "tailles différentes",
        "on peut jouer ensemble",
        "vous jouez ensemble",
        "on va apprendre",
        "c'est la règle",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Chouchou est plus petit. Que fait Raphaël ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer ensemble":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = str(q.get("retry_prompt") or "").lower()
    if "raphaël" not in retry and "raphael" not in retry:
        raise SystemExit(f"{SID}: retry sans Raphaël")
    if "jouent ensemble" not in retry and "jouer ensemble" not in retry:
        raise SystemExit(f"{SID}: retry sans jouer ensemble")
    chou = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("enfant-f|")
    ).lower()
    if "non" not in chou:
        raise SystemExit(f"{SID}: Chouchou sans non")
    if "regarde" not in chou:
        raise SystemExit(f"{SID}: Chouchou sans je regarde")
    if "plus tard" not in chou:
        raise SystemExit(f"{SID}: Chouchou sans plus tard")
    if "on joue" not in body:
        raise SystemExit(f"{SID}: Raphaël n'invite pas")
    for ban in (
        "éclat de pince",
        "éclat de cerceau",
        "éclat de drap",
        "drap",
        "cerceau",
        "kilian",
        "lise",
    ):
        if ban in blob:
            raise SystemExit(f"{SID}: BAN {ban}")
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
        "- **Public :** N3 (≤16 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.COR.001 — tailles différentes / jouer ensemble "
        "(vécue : il pose trop haut ; Chouchou n'atteint pas ; refuse de "
        "foncer ; baisse le bord ; ils jouent)\n"
        "- **Personnages :** Raphaël, Chouchou, papa, maman. Troupe D16. "
        "Maman ajoutée. Adultes parlants = papa/maman. Chouchou = enfant-f.\n"
        "- **Lieu :** terrasse du soir, planche de résine, fil à linge, "
        "torchon orange, dalles fraîches. Fil = détail de lieu, pas le jeu "
        "(≠ ATOM-DIF.COR.001-04 drap/fil/cerceau). Pas éclat de pince.\n"
        "- **Indice unique :** éclat de planche (bord au soir → tremble "
        "quand le toit est trop haut → luit après la glissade → tient "
        "sur le bord)\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un torchon orange claque au fil. Sur le bord, un éclat de planche "
        "brille. Raphaël veut un garage **maintenant** (caisse + planche). "
        "Il pose trop haut, tire la manche : Chouchou dit non. Le camion "
        "tape le toit. Sourire parti, poitrine pleine. Papa se baisse. "
        "Question. Il refuse de foncer, invite, baisse un bord. Chouchou "
        "pousse. Merci vécu. Il relève trop vite : ça glisse. Il refuse, "
        "écoute l'éclat, baisse avec elle. Cube bas. L'éclat tient.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : soir, résine tiède, torchon orange, fil, dalles, caisse, "
        "camion aux roues rouges.\n"
        "- Désir : un garage pour le camion **maintenant**.\n"
        "- Objet : planche de résine, caisse, camion, cube jaune.\n"
        "- Indice unique : éclat de planche, vu dès l'ouverture, payé "
        "au bord.\n"
        "- Urgence douce : le garage, tout de suite, avec Chouchou.\n"
        "- Imprévu 1 : toit trop haut ; manche tirée ; camion dehors.\n"
        "- Cue : papa à la même hauteur, une question. Un merci vécu, "
        "après la phrase entière.\n"
        "- Imprévu 2 (plus rusé) : il relève pour un grand garage ; "
        "la planche glisse ; Chouchou dit plus tard.\n"
        "- Résolution : il refuse de foncer, baisse avec elle, ils jouent.\n"
        "- Retour : résine sur la terrasse, toit bas, éclat sur le bord.\n\n"
        "## Vécu\n\n"
        "Raphaël veut le garage **maintenant**. Impatience (planche trop "
        "haut, manche, pousse tout de suite), puis sourire qui disparaît, "
        "épaules dans la poitrine. Papa se baisse, pose une question, "
        "ne récite pas la taille. Raphaël agit : lâche, attend, invite, "
        "baisse. Chouchou a son rythme (non, je regarde, plus tard, je "
        "pousse). Merci vécu après l'écoute. Fin : l'éclat du début tient "
        "sur le bord.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le garage de la planche (noyau dump). Relance : "
        "Chouchou est plus petit. Que fait Raphaël ? → jouer ensemble.\n"
        "- Ouverture inventée (torchon orange au fil), pas un gabarit v2, "
        "pas « joue au salon », pas drap/cerceau (001-04).\n"
        "- Indice unique : éclat de planche (roster). Pas éclat de pince, "
        "pas drap, pas cerceau, pas grains, lune d'étain, merle, miel, "
        "marque fine.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui,` "
        "retirés.\n"
        "- Leçon non dite : on la voit quand il baisse le toit. Pas "
        "« tailles différentes », pas « on peut jouer ensemble », pas "
        "« bon travail », pas « l'histoire est finie ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Maman parle. Papa parle.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. Action "
        "plus vive vers la planche.\n"
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
