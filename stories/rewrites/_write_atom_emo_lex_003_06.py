#!/usr/bin/env python3
"""ATOM-EMO.LEX.003-06 — Le pique-nique de Nina (F-NAR-019, N3, EMO.LEX.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.003-06"
TITLE = "Le pique-nique de Nina"
N3 = LIMITS["N3"]
CHARS = "Nina, papa, maman"
SETTING = (
    "maison, jour de pluie, salon, panier, napperon, "
    "chaises, fenêtre, pain, fraises, poire, bol, corbeille"
)
INDICE = "éclat de napperon"
FIL = (
    "L'anse du panier pince le pouce de Nina. Sur le tissu, "
    "un éclat de napperon luit. Nina veut le pique-nique dehors, "
    "maintenant. La pluie mouille les chaises. Sourire parti. "
    "Envie et inquiétude dans la poitrine. Papa s'accroupit. "
    "Je suis déçue. Merci vécu. Pique-nique au salon. "
    "Deuxième ruse : plus de fraises, le bol glisse. Elle refuse "
    "de foncer. Une poire, alors. Un éclat de napperon tient."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(nappe|tapis|canapé|canape|store|cagette|kiosque|pelle|"
    r"ficelle|vitre|gouttière|gouttiere|merle|miel|treille|moule|"
    r"tuteur|saladier|gomme|berge|brouette|couverture|capuche|"
    r"paillasson|fauteuil|coffre|haie|housse|banc|flaque|"
    r"maîtresse|maitresse|grand-père|grand-pere|jardinier|"
    r"bibliothécaire|bibliothecaire|gardienne|fontaine|"
    r"tabouret|torchon|plaid|coussin)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
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
    "j'ai dit",
    "j ai dit",
    "tu as nommé",
    "tu as nomme",
    "on nomme",
    "c'est de la joie",
    "c est de la joie",
    "c'est de la déception",
    "c est de la deception",
    "c'est de la deception",
    "être déçue",
    "etre decue",
    "être déçu",
    "etre decu",
    "un souhait peut attendre",
    "on peut chercher une autre idée",
    "on peut chercher une autre idee",
    "c'est une autre idée",
    "c est une autre idee",
    "une autre idée peut venir",
    "une autre idee peut venir",
    "ce n'est pas honteux",
    "ce n est pas honteux",
    "lumière couleur de miel",
    "lumiere couleur de miel",
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "les trois mots",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "il ne faut pas rire",
    "on ne rit pas",
    "bravo. tu as",
    "tu as dit : je suis",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de nappe",
    "éclat de tapis",
    "éclat de canapé",
    "éclat de canape",
    "éclat de store",
    "éclat de cagette",
    "éclat de kiosque",
    "éclat de pelle",
    "éclat de ficelle",
    "éclat de poire",
    "éclat de fraise",
    "éclat de vitre",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de chaise",
    "éclat de panier",
    "éclat de bol",
    "éclat de pain",
    "éclat de tasse",
    "éclat de salon",
    "éclat de fenêtre",
    "éclat de fenetre",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "toute calme",
    "tout calme",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de napperon",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis déception; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_le_pique_nique_dehors_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="Nina",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_pluie_arrive_que_dit_nina; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="salon",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis soulagement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_propose_le_salon_sans_slogan; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de napperon",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=plus_de_fraises_elle_refuse_de_foncer_elle_propose_une_poire; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de napperon",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_soulagement; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_tissu; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "déçue",
    "accepted_examples": (
        "déçue | je suis déçue | autre idée | une poire | une autre idée"
    ),
    "retry_prompt": "Nina cherche une autre idée. Que dit-elle d'abord ?",
    "engine_ok_text": "Oui, déçue.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "pluie",
        [
            "narrateur|L'anse du panier pince le pouce de Nina.",
            "enfant-f|Aïe, ça pince, papa.",
            "papa|Tu la vois, l'anse ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa écarte l'anse, près du panier.",
            "enfant-f|Mes doigts bougent.",
            "maman|Ils sont libres, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le panier sent le pain, même fermé.",
            "enfant-f|Ça sent le pain.",
            "papa|Tu le sens, le pain chaud ?",
            "enfant-f|Oui, papa.",
            "narrateur|Maman déplie un napperon, au bord du panier.",
            "enfant-f|Il est blanc, maman.",
            "maman|Tu le vois, le napperon ?",
            "enfant-f|Oui, un peu froissé.",
            "narrateur|Sur le tissu, un éclat de napperon luit.",
            "enfant-f|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-f|Oui, un point clair.",
            "narrateur|Dehors, les chaises du jardin brillent, trop mouillées.",
            "enfant-f|Elles sont mouillées.",
            "maman|Tu les vois, les chaises ?",
            "enfant-f|Oui, maman.",
            "narrateur|La pluie tape sur la fenêtre, sans s'arrêter.",
            "enfant-f|Elle chante fort.",
            "papa|C'est la pluie qui court.",
            "enfant-f|Sur le jardin.",
            "narrateur|Nina pose le nez contre la fenêtre.",
            "enfant-f|Je veux le jardin.",
            "maman|Tes pieds sont prêts, Nina ?",
            "enfant-f|Oui, maman.",
            "narrateur|En ce moment, Nina veut le pique-nique dehors.",
            "enfant-f|On pique-nique dehors ?",
            "papa|Tout de suite ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina avance trop vite vers la porte.",
            "narrateur|Sa main pousse la poignée.",
            "enfant-f|On y va !",
            "narrateur|Un filet d'eau glisse sous la porte.",
            "enfant-f|Il n'y a plus de jardin sec.",
            "maman|Les chaises, Nina ?",
            "enfant-f|Trop mouillées.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "enfant-f|J'ai mal au ventre.",
            "papa|Tes épaules sont lourdes, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "maman|Tes mains sont chaudes, Nina ?",
            "enfant-f|Un peu, maman.",
            "enfant-f|Je suis déçue.",
            "narrateur|L'éclat de napperon tremble, puis tient.",
            "papa|Tu vois les chaises mouillées ?",
            "enfant-f|Oui.",
            "narrateur|Nina serre les poings, puis les ouvre.",
            "papa|Tes poings, Nina ?",
            "enfant-f|Ils se desserrent.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|La pluie arrive.",
            "narrateur|Que dit Nina ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Nina avance trop vite vers le panier.",
            "enfant-f|Je prends tout, maintenant !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Le jardin, dehors.",
            "narrateur|Nina avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Nina refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le napperon, un instant.",
            "narrateur|Elle écoute la pluie, près de la fenêtre.",
            "papa|Tu restes un peu, Nina ?",
            "enfant-f|Oui, papa.",
            "papa|Merci, Nina.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le napperon est froid, sous les doigts.",
            "enfant-f|Il est lisse.",
            "enfant-f|Un pique-nique dans le salon ?",
            "maman|Tu le vois, le salon ?",
            "enfant-f|Oui, maman.",
            "papa|On pose le napperon au sol ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ils déplient le napperon, sans se presser.",
            "narrateur|Le tissu sent le pain, un peu.",
            "enfant-f|Ça sent le pain.",
            "maman|Tu veux une croûte ?",
            "enfant-f|Oui, maman.",
            "narrateur|Papa pose deux tasses, tout petit.",
            "narrateur|Les tasses font un petit bruit.",
            "papa|On est bien, ici.",
            "enfant-f|Presque comme dehors.",
            "narrateur|Le ventre de Nina se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "maman|Tes joues sont chaudes, Nina ?",
            "enfant-f|Un peu, maman.",
            "papa|Le pain est chaud, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le coin du napperon tient, au salon.",
            "enfant-f|On est là.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "",
        [
            "narrateur|Nina cherche les fraises, trop vite.",
            "enfant-f|Des fraises, maintenant !",
            "narrateur|Le bol du panier tremble, presque vide.",
            "enfant-f|Il n'y en a plus.",
            "maman|Les fraises, Nina ?",
            "enfant-f|Parti.",
            "narrateur|Les épaules de Nina retombent.",
            "enfant-f|Je les prends, tout de suite !",
            "narrateur|Nina avance trop vite vers le bol.",
            "narrateur|Le bol glisse au bord.",
            "enfant-f|Il part !",
            "narrateur|Nina avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe le napperon, un instant.",
            "narrateur|Elle écoute le salon, près du pain.",
            "narrateur|Sur le tissu, un éclat de napperon luit.",
            "enfant-f|Là, sur le tissu.",
            "papa|Tu vois le point, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina lève les yeux vers la corbeille.",
            "enfant-f|Une poire, alors.",
            "maman|Tu la vois, la poire ?",
            "enfant-f|Oui, maman.",
            "papa|Elle est jaune, Nina ?",
            "enfant-f|Un peu verte.",
            "narrateur|Papa coupe la poire, sans se presser.",
            "narrateur|Le cœur est doux et pâle.",
            "enfant-f|C'est juteux.",
            "narrateur|La poire a failli glisser, un moment.",
            "enfant-f|Elle a failli partir.",
            "papa|Elle tient, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina croque, sans se bousculer.",
            "maman|Tes doigts sont froids, Nina ?",
            "enfant-f|Un peu, maman.",
            "papa|On reste près du napperon ?",
            "enfant-f|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du napperon.",
            "narrateur|Maman plie un coin du tissu.",
            "enfant-f|La poire a une trace, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-f|Oui, près du bord.",
            "maman|On est bien, ici.",
            "narrateur|Nina tapote le tissu du doigt.",
            "enfant-f|Il a une trace de jus.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|La poire est restée, Nina.",
            "enfant-f|Oui, avec nous.",
            "narrateur|Ça sent le pain, un peu tiède.",
            "enfant-f|Et le tissu, maman.",
            "maman|Oui, dans l'air.",
            "papa|La pluie tape plus lentement, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le napperon reste au milieu du salon.",
            "narrateur|Un éclat de napperon tient sur le tissu.",
        ],
    ),
}


def vet(lines: list[str], cid: str = "") -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    skip_q = cid == "CHK_T0000_P0000_Q0001"
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
        if not skip_q and TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        if not skip_q:
            for bad in EXTRA_BAD:
                if re.search(rf"(?<!\w){re.escape(bad)}(?!\w)", low):
                    raise SystemExit(f"extra {bad}: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-f"):
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
    cid = src.get("chunk_id") or ""
    lines = vet(lines, cid)
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
        for key in (
            "expected_answer",
            "accepted_examples",
            "retry_prompt",
            "engine_ok_text",
            "engine_near_text",
        ):
            if cid != "CHK_T0000_P0000_Q0001":
                by[cid][key] = None
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
    if "accroupit" not in blob:
        raise SystemExit(f"{SID}: manque accroupit")
    if "poitrine" not in blob:
        raise SystemExit(f"{SID}: manque poitrine")
    if "sourire" not in blob:
        raise SystemExit(f"{SID}: manque sourire")
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Nina = enfant-f)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé (dump sans camarade)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "enfant-f" for r in roles):
        raise SystemExit(f"{SID}: enfant-f absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "j'ai dit",
        "j ai dit",
        "tu as nommé",
        "tu as nomme",
        "on nomme",
        "c'est de la déception",
        "c est de la deception",
        "c'est une autre idée",
        "on peut chercher une autre idée",
        "un souhait peut attendre",
        "ce n'est pas honteux",
        "être déçue",
        "etre decue",
        "l'histoire est finie",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "La pluie arrive. Que dit Nina ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "déçue":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "déçue | je suis déçue | autre idée | une poire | une autre idée"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Nina cherche une autre idée. Que dit-elle d'abord ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    for c in chunks:
        if c["chunk_id"] == "CHK_T0000_P0000_Q0001":
            continue
        if c.get("expected_answer") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: expected hors Q")
        if c.get("accepted_examples") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: accepted hors Q")
        if c.get("retry_prompt") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: retry hors Q")
        if c.get("engine_ok_text") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: engine_ok hors Q")
        if c.get("engine_near_text") not in (None, ""):
            raise SystemExit(f"{SID} {c['chunk_id']}: engine_near hors Q")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "je suis déçue" not in opening:
        raise SystemExit(f"{SID}: nommage absent avant la question")
    n_decue = blob.count("je suis déçue")
    if n_decue != 1:
        raise SystemExit(f"{SID}: je suis déçue ×{n_decue}")
    if "s'accroupit" not in opening and "s accroupit" not in opening:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    if "sourire" not in opening or "disparaît" not in opening:
        raise SystemExit(f"{SID}: manque sourire disparu")
    if "poitrine" not in opening:
        raise SystemExit(f"{SID}: manque poitrine")
    if "une poire" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: poire absente au 2e imprévu")
    if "fraise" not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: fraises absentes au 2e imprévu")
    if "salon" not in by["CHK_T0000_P0000_C0001"]["text"].lower():
        raise SystemExit(f"{SID}: salon absent après la question")
    if "pluie" not in blob:
        raise SystemExit(f"{SID}: manque pluie")
    if "pique-nique" not in blob and "pique nique" not in blob:
        raise SystemExit(f"{SID}: manque pique-nique")
    if "poire" not in blob:
        raise SystemExit(f"{SID}: manque poire")
    if "fraise" not in blob:
        raise SystemExit(f"{SID}: manque fraises")
    if "maintenant" not in blob:
        raise SystemExit(f"{SID}: manque maintenant")
    if "papa" not in by["CHK_T0000_P0000_END"]["script"].lower():
        raise SystemExit(f"{SID}: papa absent au 2e imprévu")
    if INDICE not in by["CHK_T0000_P0000_END"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé au climax")
    for ban in (
        "éclat de nappe",
        "éclat de tapis",
        "éclat de canapé",
        "éclat de store",
        "éclat de cagette",
        "éclat de kiosque",
        "éclat de pelle",
        "éclat de ficelle",
        "éclat de poire",
        "éclat de fraise",
        "éclat de vitre",
        "éclat de gouttière",
        "tout doux",
        "tout calme",
        "merle",
        "j'ai dit : je suis",
        "nappe",
        "tapis",
        "canapé",
        "vitre",
    ):
        if re.search(rf"(?<!\w){re.escape(ban)}(?!\w)", blob):
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
    notes_ok = all(
        all(
            k in (c.get("notes") or "")
            for k in (
                "arc=",
                "intention=",
                "emotion=",
                "intensite=",
                "destinataire=",
                "sous_texte=",
                "tempo=",
                "sourire=",
                "respiration=",
            )
        )
        for c in chunks
    )
    if not notes_ok:
        raise SystemExit(f"{SID}: notes incomplètes")
    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 700 or nwords > 850:
        raise SystemExit(f"{SID}: {nwords} mots hors 700–850")

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
        "- **Public :** N3 (≤16 mots/phrase), audio familial, voc 5–6 ans\n"
        "- **Leçon :** EMO.LEX.003 — nommer la déception + autre idée "
        "(vécue : chaises mouillées, sourire parti, poitrine qui se "
        "bouscule, papa accroupi, Nina dit « je suis déçue », propose "
        "le salon ; 2e ruse : plus de fraises, le bol glisse, elle "
        "refuse de foncer, propose une poire). JAMAIS dite en slogan. "
        "Pas « j'ai dit : je suis ». Pas « tu as nommé ». Pas « un "
        "souhait peut attendre ». Pas « on peut chercher une autre "
        "idée ». Pas « ce n'est pas honteux ».\n"
        "- **Personnages :** Nina, papa, maman. Dump Fanny → D16 Nina "
        "= enfant-f (veut le pique-nique dehors maintenant). Pas de "
        "copain (dump sans camarade). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** maison, jour de pluie, salon. Coin nommé : le "
        "coin du napperon, au salon. Dump : pluie, pique-nique, "
        "fraises, poire (objets, pas indice). Indice PAS nappe / "
        "tapis / canapé / vitre / poire / fraise.\n"
        "- **Indice unique :** éclat de napperon (luit sur le tissu "
        "→ tremble aux chaises mouillées → luit au climax des "
        "fraises → tient sur le tissu). BAN éclat de nappe / tapis / "
        "canapé / store / cagette / kiosque / pelle / ficelle / "
        "poire / vitre.\n"
        "- **Question moteur :** « La pluie arrive. Que dit Nina ? » "
        "expected dump **déçue**. accepted dump `déçue | je suis "
        "déçue | autre idée | une poire | une autre idée`. retry "
        "dump Fanny → Nina : `Nina cherche une autre idée. Que "
        "dit-elle d'abord ?`. Hors Q : null. Non récitée ailleurs.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / "
        "graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin "
        "heureuse. `chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "L'anse du panier pince le pouce de Nina. Pain, napperon, "
        "chaises mouillées. Sur le tissu, un éclat de napperon luit. "
        "Nina veut le pique-nique dehors **maintenant**. La pluie "
        "court sous la porte. Sourire parti. Envie et inquiétude. "
        "Papa s'accroupit. Je suis déçue. Merci vécu. Pique-nique "
        "au salon, croûte, tasses. Deuxième ruse : plus de fraises, "
        "le bol glisse. Elle s'arrête, lit l'éclat, propose une "
        "poire. La poire a failli glisser. Un éclat de napperon "
        "tient sur le tissu.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : maison, jour de pluie, panier, napperon, chaises "
        "du jardin, fenêtre, salon.\n"
        "- Désir : un pique-nique dehors, maintenant.\n"
        "- Objet : panier, napperon, pain, fraises manquantes, poire "
        "à la trace.\n"
        "- Indice unique : éclat de napperon, vu dès l'ouverture, "
        "payé sur le tissu. Pas éclat de nappe / tapis / canapé / "
        "store / vitre / poire / fraise.\n"
        "- Urgence douce : elle avance trop vite vers la porte.\n"
        "- Imprévu 1 : pluie, chaises trop mouillées, sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "qu'elle refuse de foncer et propose le salon.\n"
        "- Imprévu 2 (plus rusé) : plus de fraises, le bol glisse, "
        "la poire a failli glisser.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le "
        "salon, retrouve l'éclat, propose une poire.\n"
        "- Retour : poire à la trace, napperon au milieu du salon, "
        "éclat sur le tissu. La fin a failli (bol qui glisse, poire "
        "qui part).\n\n"
        "## Vécu\n\n"
        "Nina veut le pique-nique **maintenant**. Impatience, puis "
        "pluie, sourire parti. Elle dit je suis déçue. Papa se "
        "baisse, pose une question, ne récite pas la leçon. Ils "
        "agissent : napperon au salon, puis bol vide, elle "
        "s'arrête. Merci vécu. Fin : l'éclat du début tient sur "
        "le tissu.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le pique-nique de Nina (noyau dump). Relance : "
        "Que dit Nina ? expected déçue.\n"
        "- Lieu du dump-meta (maison, jour de pluie). Maman et papa. "
        "Nina = héros enfant-f. Dump pluie / pique-nique / fraises / "
        "poire gardés comme objets, pas comme indice.\n"
        "- Ouverture inventée (anse du panier qui pince), pas un "
        "gabarit v2, pas gouttière/buée du dump, pas « Fanny joue "
        "au salon ».\n"
        "- Indice unique : éclat de napperon ×4. BAN éclat de nappe "
        "/ tapis / canapé / store / cagette / kiosque / pelle / "
        "ficelle / poire / vitre. Pas tache/flèche/marque/symbole. "
        "Pas nappe (napperon à la place).\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « j'ai dit : je suis ». Strip « on peut "
        "chercher une autre idée ». Strip « ce n'est pas honteux ».\n"
        "- Leçon non dite : on la voit quand les chaises sont "
        "mouillées, quand elle dit je suis déçue, quand elle "
        "propose le salon, quand elle propose une poire. Pas "
        "« tu as nommé ». Une seule « je suis déçue ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « La pluie arrive. Que dit Nina ? ». "
        "expected/accepted dump. retry Fanny → Nina. Hors Q : "
        "null. 5 chunks, kinds inchangés.\n"
        "- example4 073 / 005 / 037 (manière volée, gabarit non "
        "collé). Voix : `_write_atom_emo_ges_002_01.py`, profiles N3.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, "
        "sous-texte, tempo, sourire, respiration). `slow` = "
        "question et fin. Action un peu plus vive vers le bol "
        "qui glisse.\n"
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
