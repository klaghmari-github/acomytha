#!/usr/bin/env python3
"""ATOM-EMO.LEX.001-03 — Nina et la cerise du matin (F-NAR-019, N2, EMO.LEX.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.001-03"
TITLE = "Nina et la cerise du matin"
N2 = LIMITS["N2"]
CHARS = "Nina, papa, maman"
SETTING = (
    "jardin, cerisier, portail, cerise, noyau, tuteur, "
    "herbe, bois, soleil, panier"
)
INDICE = "éclat de tuteur"
FIL = (
    "L'air près du cerisier sent le sucre. Sur le bois, un "
    "éclat de tuteur luit. Nina veut la cerise, maintenant. "
    "Branche trop haute, doigts qui glissent. Sourire parti, "
    "poitrine, papa accroupi. Une cerise plus bas. Un sourire "
    "arrive. Je suis contente. Partage, merci vécu. Deuxième "
    "ruse : jus qui coule, branche trop haute, oiseau. Elle "
    "refuse de foncer. Noyau, portail. Un éclat de tuteur "
    "tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja|aujourd'hui)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(treille|moule|fraise|grille|tour|comptoir|rouleau|"
    r"étagère|etagere|torchon|tabouret|merle|miel|cubes|cube|"
    r"tapis|plaid|rideau|paillasson|pelle|coccinelle|linge|"
    r"arrosoir|canapé|canape|toboggan|balançoire|balancoire|"
    r"banc|sable|seau|parc|gouttière|gouttiere|cabane|"
    r"casserole|soupe|carotte|chiffon|commode|gond|confiture|"
    r"camion|pupitre|gourde|flaque|piquet|rotin|crochet|"
    r"platane|cageot|résine|resine|limace|perron|fraisier|"
    r"cuivre|buis|cerceau|cour|figue|robinet|émail|email|"
    r"samare|bassine|lunettes|corde|sauge|lacet|farine|"
    r"saladier|coussin|thym|zinc|vanille|gâteau|gateau|"
    r"gomme|saladier)\b",
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
    "c'est bien",
    "c est bien",
    "c'est de la joie",
    "c est de la joie",
    "tu as nommé",
    "j'ai dit : je suis",
    "j'ai dit: je suis",
    "on peut partager",
    "tu as partagé",
    "tu as partage",
    "être content",
    "etre content",
    "la joie est là",
    "la joie est la",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de treille",
    "éclat de moule",
    "éclat de fraise",
    "éclat de portail",
    "éclat de panier",
    "éclat de tour",
    "éclat de comptoir",
    "éclat de pot",
    "éclat de rouleau",
    "éclat de lit",
    "éclat d'étagère",
    "éclat d'etagere",
    "éclat de torchon",
    "éclat de tabouret",
    "éclat de cerise",
    "éclat de noyau",
    "éclat de grille",
    "éclat de cerisier",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de tuteur",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis joie_naissante; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_la_cerise_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun puis léger; "
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
            "sous_texte=nina_sourit_que_dit_elle; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="contente",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=joie puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_dit_je_suis_contente_elle_partage; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de tuteur",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=jus_branche_oiseau_elle_refuse_de_foncer; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de tuteur",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "content",
    "accepted_examples": (
        "content | je suis contente | joie | de la joie | partager"
    ),
    "retry_prompt": "Nina sent de la joie. Que dit-elle ?",
    "engine_ok_text": "Oui, c'est la bonne réponse.",
    "engine_near_text": "Tu étais presque.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "jardin,cerisier",
        [
            "narrateur|L'air près du cerisier sent le sucre.",
            "enfant-f|Ça sent le sucre, papa.",
            "papa|Tu le sens, le sucre, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le portail de bois reste un peu ouvert.",
            "enfant-f|Il est ouvert, maman.",
            "maman|Tu entends le bois, Nina ?",
            "enfant-f|Il claque, maman.",
            "narrateur|L'herbe froide mouille les pieds de Nina.",
            "enfant-f|Elle est mouillée.",
            "maman|Elle pique un peu, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le tuteur tient une branche basse, près du portail.",
            "enfant-f|Il est en bois.",
            "papa|Tu le vois, le tuteur ?",
            "enfant-f|Oui, papa.",
            "narrateur|Sur le bois, un éclat de tuteur luit.",
            "enfant-f|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-f|Oui, un petit point.",
            "narrateur|Papa pose le panier près de l'herbe.",
            "enfant-f|Le panier est là.",
            "papa|Il attend, près de nous.",
            "enfant-f|Oui.",
            "narrateur|Une cerise rouge attend trop haut.",
            "enfant-f|Elle est rouge !",
            "papa|Tu la veux, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le soleil chauffe la peau lisse.",
            "enfant-f|Elle brille.",
            "maman|La cerise est loin, Nina ?",
            "enfant-f|Un peu loin.",
            "narrateur|En ce moment, Nina lève les deux mains.",
            "enfant-f|Je veux la cerise, maintenant !",
            "papa|Tout de suite ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina saute trop vite vers la branche.",
            "narrateur|Ses doigts glissent sur la peau lisse.",
            "narrateur|La cerise reste trop haute.",
            "enfant-f|Oh.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent sans place.",
            "narrateur|Sa poitrine va trop vite.",
            "papa|Elle est trop haute, Nina ?",
            "enfant-f|Oui, papa.",
            "maman|Tes joues sont chaudes, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|L'éclat de tuteur tremble, puis tient.",
            "narrateur|Papa s'accroupit à la même hauteur, sans parler.",
            "papa|Tu vois une autre, Nina ?",
            "enfant-f|Là, plus bas.",
            "narrateur|Une cerise plus basse brille à hauteur de main.",
            "narrateur|Nina la touche du bout du doigt.",
            "enfant-f|Elle est froide.",
            "maman|Tu la cueilles, Nina ?",
            "enfant-f|Oui.",
            "narrateur|Nina détache la cerise plus basse, sans se presser.",
            "narrateur|La queue reste entre ses doigts.",
            "enfant-f|Elle est lourde.",
            "papa|Elle tient dans ta main ?",
            "enfant-f|Oui, papa.",
            "narrateur|La cerise sent le sucre.",
            "narrateur|Ses joues deviennent chaudes.",
            "narrateur|Son ventre est léger, comme une bulle.",
            "enfant-f|Ça chatouille.",
            "maman|Tes épaules se relèvent, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Un sourire arrive.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nina sourit.",
            "narrateur|Que dit-elle ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "jardin",
        [
            "narrateur|Nina tient la cerise contre sa paume, tout près.",
            "enfant-f|Je suis contente.",
            "papa|Tu le dis, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ses joues restent chaudes.",
            "narrateur|Le ventre de Nina se desserre.",
            "enfant-f|On partage ?",
            "maman|Tu veux tendre la cerise ?",
            "enfant-f|Oui, maman.",
            "narrateur|Nina avance la cerise trop vite.",
            "narrateur|Elle ouvre la bouche, trop large.",
            "narrateur|Puis elle s'arrête.",
            "narrateur|Nina refuse de foncer.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe la cerise, un instant.",
            "narrateur|Elle écoute le jardin.",
            "narrateur|Nina tend la cerise vers papa.",
            "narrateur|Papa prend un tout petit bout.",
            "papa|Merci, Nina.",
            "narrateur|Papa a vu le geste, sous l'arbre.",
            "enfant-f|Le jus est rouge.",
            "maman|Il colle aux doigts, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Nina croque un tout petit bout.",
            "enfant-f|C'est sucré.",
            "papa|Tu le sens, le sucre ?",
            "enfant-f|Oui, papa.",
            "maman|Tes lèvres sont rouges, Nina ?",
            "enfant-f|Un peu, maman.",
            "narrateur|Le ventre de Nina reste léger.",
            "enfant-f|Maman, un bout pour toi.",
            "maman|Tu m'invites, Nina ?",
            "enfant-f|Oui.",
            "narrateur|Maman attend, la main ouverte.",
            "papa|La cerise est petite, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ils restent sous le cerisier.",
            "enfant-f|Elle tient.",
            "maman|Tes mains sont collantes, Nina ?",
            "enfant-f|Un peu.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "jardin,cerisier",
        [
            "narrateur|Le jus coule le long du doigt.",
            "enfant-f|Ça glisse !",
            "narrateur|Nina serre trop vite.",
            "narrateur|Une goutte tombe dans l'herbe.",
            "enfant-f|Une autre, pour maman !",
            "narrateur|Une branche trop haute cache d'autres cerises, plus rouges.",
            "narrateur|Un oiseau se pose sur la branche.",
            "enfant-f|Il va la prendre !",
            "narrateur|Nina avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Nina refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe la cerise, un instant.",
            "narrateur|Elle écoute le jardin, près du tuteur et du bois.",
            "narrateur|Sur le bois, un éclat de tuteur luit.",
            "enfant-f|Là, sur le bois.",
            "papa|Tu vois le point, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nina tient la cerise, sans se presser.",
            "narrateur|Le jus arrête de couler.",
            "enfant-f|Pour toi, maman.",
            "narrateur|Maman prend un tout petit bout.",
            "maman|Il est sucré, Nina ?",
            "enfant-f|Oui, maman.",
            "papa|L'oiseau reste sur la branche ?",
            "enfant-f|Oui, papa.",
            "narrateur|L'oiseau picore plus haut, puis s'en va vers le portail.",
            "enfant-f|Il est parti.",
            "maman|La cerise est restée, Nina ?",
            "enfant-f|Oui, avec nous.",
            "narrateur|Nina essuie un peu de jus.",
            "papa|Tes doigts sont rouges, Nina ?",
            "enfant-f|Un peu, papa.",
            "narrateur|Le noyau apparaît, tout petit.",
            "enfant-f|Le noyau.",
            "maman|Tu le poses, Nina ?",
            "enfant-f|Dans le panier.",
            "narrateur|Nina pose le noyau dans le panier.",
            "papa|Il est arrivé, le noyau ?",
            "enfant-f|Oui, papa.",
            "maman|Le panier sent le sucre ?",
            "enfant-f|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du cerisier.",
            "enfant-f|On a partagé, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-f|Oui, près de l'arbre.",
            "maman|On est bien, ici.",
            "narrateur|Nina tapote le bois du tuteur.",
            "enfant-f|Il a une trace de jus.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|Le portail attend, Nina.",
            "enfant-f|Oui, un peu ouvert.",
            "narrateur|Ça sent le sucre, un peu tiède.",
            "enfant-f|Et le bois, maman.",
            "maman|Oui, dans l'air.",
            "papa|Le jardin est calme, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le panier reste près de l'herbe.",
            "narrateur|Un éclat de tuteur tient sur le bois.",
        ],
    ),
}


def vet(lines: list[str], cid: str = "") -> list[str]:
    out: list[str] = []
    starts: list[str] = []
    skip_lesson = cid == "CHK_T0000_P0000_Q0001"
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
        if BAN_WORDS.search(ph):
            raise SystemExit(f"ban mot: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        if not skip_lesson:
            for bad in EXTRA_BAD:
                if bad in low:
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
        for key in ("expected_answer", "accepted_examples", "retry_prompt"):
            if cid != "CHK_T0000_P0000_Q0001" and by[cid].get(key) is not None:
                raise SystemExit(f"{cid}: {key} devait rester null")
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
        "c'est de la joie",
        "tu as nommé",
        "j'ai dit : je suis",
        "j'ai dit: je suis",
        "on peut partager",
        "tu as partagé",
        "être content",
        "la joie est là",
        "tout doux",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Nina sourit. Que dit-elle ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "content":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "content | je suis contente | joie | de la joie | partager"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Nina sent de la joie. Que dit-elle ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "je suis contente" in opening:
        raise SystemExit(f"{SID}: je suis contente trop tôt (avant la question)")
    if "contente" in opening:
        raise SystemExit(f"{SID}: contente trop tôt (avant la question)")
    if "cerise" not in blob:
        raise SystemExit(f"{SID}: manque cerise")
    if "noyau" not in blob:
        raise SystemExit(f"{SID}: manque noyau")
    if "portail" not in blob:
        raise SystemExit(f"{SID}: manque portail")
    if "jardin" not in blob:
        raise SystemExit(f"{SID}: manque jardin")
    if "cerisier" not in blob:
        raise SystemExit(f"{SID}: manque cerisier")
    if "maintenant" not in blob:
        raise SystemExit(f"{SID}: manque maintenant")
    end_txt = by["CHK_T0000_P0000_END"]["text"].lower()
    if "jus" not in end_txt:
        raise SystemExit(f"{SID}: manque 2e ruse (jus)")
    if "branche" not in end_txt:
        raise SystemExit(f"{SID}: manque 2e ruse (branche)")
    if "oiseau" not in end_txt:
        raise SystemExit(f"{SID}: manque 2e ruse (oiseau)")
    for ban in (
        "éclat de treille",
        "éclat de moule",
        "éclat de fraise",
        "éclat de portail",
        "éclat de panier",
        "éclat de tour",
        "éclat de comptoir",
        "éclat de pot",
        "éclat de rouleau",
        "éclat de lit",
        "éclat de torchon",
        "éclat de tabouret",
        "éclat de cerise",
        "éclat de noyau",
        "éclat de grille",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "emma",
        "treille",
        "moule",
        "fraise",
        "grille",
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

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nwords = sum(words(c["text"]) for c in chunks)
    if not (700 <= nwords <= 850):
        raise SystemExit(f"{SID}: {nwords} mots (voulu 700–850)")

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N2 (≤15 mots/phrase), audio familial, voc 4–5 ans\n"
        "- **Leçon :** EMO.LEX.001 — nommer la joie + partager "
        "(vécue : Nina veut la cerise **maintenant**, trop haute, "
        "sourire parti, papa accroupi ; une cerise plus bas, sourire ; "
        "« Je suis contente », elle tend, merci vécu ; 2e ruse : jus, "
        "branche trop haute, oiseau, elle refuse de foncer). JAMAIS "
        "dite dans le récit. Pas « c'est de la joie ». Pas « tu as "
        "nommé ». Pas « j'ai dit : je suis ».\n"
        "- **Personnages :** Nina, papa, maman. Dump Emma/papa → D16 "
        "Nina = enfant-f (veut la cerise maintenant). Pas de copain "
        "(dump sans camarade). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** jardin, cerisier, portail, cerise, noyau, tuteur, "
        "herbe, bois, soleil, panier. BAN treille / moule / fraise "
        "(LEX.001-01/02). Cerise/noyau/portail = dump.\n"
        "- **Indice unique :** éclat de tuteur (luit à l'ouverture → "
        "tremble à la branche trop haute → luit au jus/oiseau → "
        "tient sur le bois). BAN éclat de cerise / noyau / portail / "
        "panier / grille / treille / moule / fraise / tour / comptoir / "
        "pot / rouleau / lit / étagère / torchon / tabouret.\n"
        "- **Question moteur :** « Nina sourit. Que dit-elle ? » "
        "expected dump **content**. accepted dump "
        "`content | je suis contente | joie | de la joie | partager`. "
        "retry dump Emma → Nina. Non récitée dans les autres chunks. "
        "Hors Q : expected/accepted/retry restent **null**.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "L'air près du cerisier sent le sucre. Portail un peu ouvert. "
        "Sur le bois, un éclat de tuteur luit. Nina veut la cerise "
        "**maintenant**. Trop haute, doigts qui glissent. Sourire parti. "
        "Papa s'accroupit. Une cerise plus bas. Un sourire arrive. "
        "Je suis contente. Elle tend, merci vécu. Deuxième ruse : jus "
        "qui coule, branche trop haute, oiseau. Elle refuse de foncer. "
        "Noyau dans le panier. Un éclat de tuteur tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin, cerisier, portail, tuteur, herbe froide, "
        "panier. ≠ treille / moule / fraise.\n"
        "- Désir : cueillir la cerise du matin, maintenant.\n"
        "- Objet : cerise, puis noyau, panier.\n"
        "- Indice unique : éclat de tuteur, vu dès l'ouverture, payé "
        "sur le bois. Pas éclat de cerise / portail / panier.\n"
        "- Urgence douce : elle saute trop vite vers la branche haute.\n"
        "- Imprévu 1 : doigts qui glissent, cerise trop haute, sourire "
        "parti, poitrine trop vite.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le "
        "partage.\n"
        "- Imprévu 2 (plus rusé) : jus qui coule, branche trop haute, "
        "oiseau.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le "
        "jardin, retrouve l'éclat, tend sans se presser.\n"
        "- Retour : noyau dans le panier, portail un peu ouvert, "
        "éclat sur le bois.\n\n"
        "## Vécu\n\n"
        "Nina veut la cerise **maintenant**. Impatience, puis trop "
        "haute, sourire parti. Une cerise plus bas. Joues chaudes, "
        "ventre léger, sourire. Elle dit qu'elle est contente, tend "
        "un bout. Papa se baisse, pose une question, ne récite pas "
        "la règle. Merci vécu. Fin : l'éclat du début tient sur le "
        "bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Nina et la cerise du matin (noyau dump). Relance : "
        "Que dit-elle ? expected content.\n"
        "- Lieu du dump-meta (jardin, cerisier). Maman et papa. "
        "Nina = héros enfant-f. Cerise / noyau / portail conservés.\n"
        "- Ouverture inventée (air, sucre, portail ouvert), pas un "
        "gabarit v2, pas « Emma marche dans le jardin ».\n"
        "- Indice unique : éclat de tuteur. BAN éclat de cerise / "
        "noyau / portail / panier / grille / treille / moule / "
        "fraise. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doucement », « c'est de la joie », "
        "« tu as nommé », « j'ai dit : je suis » du dump.\n"
        "- Leçon non dite : on la voit quand le sourire arrive, "
        "quand Nina dit qu'elle est contente, quand elle tend. "
        "Pas « c'est de la joie ». Pas « tu as nommé ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Nina sourit. Que dit-elle ? ». "
        "expected content. 5 chunks, kinds inchangés. "
        "expected/accepted dump conservés. retry Emma → Nina.\n"
        "- example4 056 / 088 / 020 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N2.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers le jus et l'oiseau.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
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
