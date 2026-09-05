#!/usr/bin/env python3
"""ATOM-DIF.COR.002-07 — Le carton-tunnel d'Aniss (F-NAR-019, N3, DIF.COR.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.002-07"
TITLE = "Le carton-tunnel d'Aniss"
N3 = LIMITS["N3"]
CHARS = "Aniss, Chouchou, papa, maman"
SETTING = "chemin du parc après la pluie, terre, fil d'argent, limace"
INDICE = "éclat de limace"
FIL = (
    "Une odeur de champignon monte du chemin. Sur le fil d'argent, un "
    "éclat de limace brille. Aniss veut un tunnel pour le ballon jaune, "
    "maintenant. Il pousse trop vite : le carton mouillé s'écrase. "
    "Chouchou veut la limace. Un rire commence, puis s'arrête. Il refuse "
    "de foncer. Ils tiennent les bords. Merci vécu. Il se glisse trop "
    "vite : ça colle. Il refuse, retrouve l'éclat. Un éclat de limace "
    "tient sur le fil."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(drap|chaise|lanterne|lanternes|biscuit|biscuits|cheval|"
    r"guirlande|fraise|fraises|perron|cuivre|buis|figue|coussin|"
    r"planche|robinet|cerceau|émail|email|samare|gouttière|"
    r"gouttiere|merle|miel|pince|torchon)\b",
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
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "il ne faut pas rire",
    "l'amitié ne dépend pas",
    "l'amitie ne depend pas",
    "vous jouez ensemble",
    "on joue ensemble",
    "tailles différentes",
    "tailles differentes",
    "corps plus rond",
    "corps plus mince",
    "pas une blague",
    "n'est pas une blague",
    "n est pas une blague",
    "le corps n'est",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de carton",
    "éclat de chaise",
    "éclat de drap",
    "éclat de perron",
    "éclat de fil",
    "éclat d'argent",
    "éclat de terre",
    "éclat de banc",
    "éclat de ballon",
    "éclat de papier",
    "éclat de pierre",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de figue",
    "éclat de planche",
    "éclat de robinet",
    "éclat de coussin",
    "éclat de cerceau",
    "éclat de samare",
    "éclat de fraisier",
    "éclat de casserole",
    "éclat de citron",
    "éclat de coquille",
    "éclat de nappe",
    "éclat de farine",
    "éclat de pompon",
    "éclat de carotte",
    "éclat de mousse",
    "éclat de laine",
    "éclat de tasse",
    "éclat de crayon",
    "éclat de cartable",
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
    "éclat de manteau",
    "éclat de seau",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de couloir",
    "éclat de plaque",
    "éclat de dalle",
    "éclat de grille",
    "éclat de couvercle",
    "éclat de caisse",
    "éclat de sonnette",
    "éclat de vitre",
    "éclat de grain",
    "éclat de liste",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de limace",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_tunnel_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="carton",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=ils_tiennent_le_carton_ils_jouent; "
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
            "destinataire=enfant; sous_texte=ils_tiennent_les_bords_a_deux; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de limace",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_sous_le_carton; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de limace",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_fil; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer",
    "accepted_examples": (
        "jouer | ensemble | tenir | le carton | on joue | à deux"
    ),
    "retry_prompt": "Ils tiennent le carton ensemble. Que font-ils ?",
    "engine_ok_text": "Oui, jouer.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc,ballon",
        [
            "narrateur|Une odeur de champignon monte du chemin.",
            "enfant-m|Ça sent la terre, papa !",
            "papa|Tu le sens, après la pluie ?",
            "enfant-m|Oui, un peu froid.",
            "narrateur|Un fil d'argent brille sur la pierre.",
            "enfant-m|Il brille, maman.",
            "maman|C'est la limace, sur la pierre ?",
            "enfant-m|Oui, un petit fil.",
            "narrateur|La limace avance, très lente.",
            "narrateur|Sur le fil, un éclat de limace brille.",
            "enfant-m|Il est petit, papa.",
            "papa|C'est l'eau, sous la lumière.",
            "enfant-m|Oui, un petit point.",
            "narrateur|Le banc garde une tache d'eau.",
            "enfant-m|Elle est froide.",
            "maman|On reste près du banc ?",
            "enfant-m|Oui, maman.",
            "narrateur|Papa pose un carton sur l'herbe.",
            "narrateur|Le carton sent le papier humide.",
            "enfant-m|Il est mou.",
            "papa|La pluie l'a mouillé, Aniss ?",
            "enfant-m|Oui, papa.",
            "narrateur|Maman pose le ballon jaune près du carton.",
            "maman|Le caoutchouc est froid, Aniss.",
            "enfant-m|Il est lisse.",
            "enfant-m|Je veux un tunnel, maintenant !",
            "papa|Avec le carton, sur l'herbe ?",
            "enfant-m|Oui.",
            "enfant-m|Le ballon passe dedans.",
            "maman|Et il sort de l'autre côté ?",
            "enfant-m|Oui, maman.",
            "narrateur|Chouchou arrive près du chemin.",
            "narrateur|Ses bottes font un bruit mou.",
            "enfant-m|Chouchou !",
            "enfant-f|J'arrive.",
            "enfant-m|Le tunnel, maintenant, Chouchou !",
            "narrateur|En ce moment, Aniss pousse le carton trop vite.",
            "narrateur|L'herbe mouille ses genoux.",
            "narrateur|Le carton s'écrase, tout plat.",
            "enfant-m|Oh.",
            "enfant-m|Tu tiens le bord, tout de suite !",
            "narrateur|Aniss attrape la manche de Chouchou.",
            "enfant-f|Non.",
            "narrateur|Chouchou recule vers la pierre.",
            "narrateur|Elle regarde la limace, longtemps.",
            "enfant-m|Oh.",
            "narrateur|Le carton mouillé reste sur le dos de Chouchou.",
            "enfant-m|Il est drôle, sur toi !",
            "narrateur|Un rire commence dans la bouche d'Aniss.",
            "narrateur|Chouchou ne dit rien.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "enfant-m|Pousse, maintenant !",
            "enfant-f|Non.",
            "enfant-m|Oh.",
            "narrateur|Aniss pousse le ballon tout seul.",
            "narrateur|Le ballon reste coincé, sous le papier.",
            "enfant-m|Il reste coincé !",
            "enfant-f|Oh.",
            "narrateur|L'éclat de limace tremble, puis tient.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "papa|Le carton est plat, Aniss ?",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "enfant-m|Oui, papa.",
            "maman|Chouchou est près de la pierre, Aniss.",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Le carton s'écrase.",
            "narrateur|Que font Aniss et Chouchou ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "ballon,carton",
        [
            "narrateur|Aniss veut le tunnel, tout de suite.",
            "enfant-m|Tu tiens, maintenant !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-f|Non.",
            "narrateur|Chouchou reste près de la pierre.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Aniss refuse de foncer.",
            "narrateur|Il lâche la manche, un peu.",
            "papa|Le carton est plat, Aniss ?",
            "narrateur|Papa reste à sa hauteur.",
            "maman|La limace avance, près de la pierre.",
            "narrateur|Aniss attend que le silence arrive.",
            "enfant-m|On joue, Chouchou ?",
            "enfant-m|Tu tiens le bord, si tu veux ?",
            "narrateur|Chouchou ne dit rien.",
            "narrateur|Elle regarde le carton, longtemps.",
            "enfant-f|Je regarde.",
            "enfant-m|D'accord.",
            "narrateur|Aniss redresse un bord du carton.",
            "narrateur|L'autre bord reste dans l'herbe.",
            "enfant-f|Je tiens.",
            "narrateur|Chouchou tient le bord, sans presser.",
            "narrateur|Aniss pousse le ballon, plus léger.",
            "narrateur|Le caoutchouc glisse sur le papier.",
            "enfant-m|Il entre !",
            "papa|Merci, Aniss.",
            "narrateur|Papa a vu les deux, près du carton.",
            "maman|Tes genoux sont mouillés, Aniss ?",
            "enfant-m|Un peu, maman.",
            "enfant-f|Le ballon est dedans.",
            "papa|Tu as entendu le papier ?",
            "enfant-m|Oui, papa.",
            "maman|On reste près du banc, Aniss ?",
            "enfant-m|Oui.",
            "narrateur|Le ventre d'Aniss se desserre.",
            "enfant-m|Il va sortir ?",
            "maman|Un peu, Aniss.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "ballon,herbe",
        [
            "narrateur|Aniss veut passer dans le tunnel.",
            "enfant-m|Moi, maintenant !",
            "narrateur|Il se glisse trop vite sous le carton.",
            "narrateur|Le carton mouillé colle à son dos.",
            "enfant-m|Oh.",
            "enfant-f|Il reste collé.",
            "narrateur|Un rire revient dans la bouche d'Aniss.",
            "narrateur|Chouchou ne rit pas.",
            "enfant-f|Attends.",
            "narrateur|Chouchou lâche le bord.",
            "narrateur|Le carton s'écrase, une fois.",
            "enfant-m|Ça tombe !",
            "narrateur|Aniss avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Aniss refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le carton, un instant.",
            "narrateur|Il écoute l'herbe, près du fil.",
            "narrateur|Sur le fil, un éclat de limace luit.",
            "enfant-m|Il est là.",
            "enfant-m|On tient, si tu veux ?",
            "enfant-f|Plus tard.",
            "enfant-m|D'accord.",
            "narrateur|Chouchou s'approche, sans se presser.",
            "narrateur|Ils tiennent les deux bords, à deux.",
            "narrateur|Aniss pousse le ballon, plus lent.",
            "narrateur|Le ballon sort de l'autre côté.",
            "narrateur|Il fait poum dans l'herbe.",
            "enfant-m|Il est passé !",
            "enfant-f|Poum.",
            "papa|Tu restes un peu ?",
            "enfant-m|Oui, papa.",
            "maman|Le carton est près du banc.",
            "enfant-m|On le laisse ?",
            "papa|Oui, contre le bois.",
            "narrateur|Une goutte tombe du banc.",
            "narrateur|Elle fait un rond dans l'eau.",
            "enfant-m|Un rond, maman.",
            "maman|Oui, dans l'eau.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "terre,limace",
        [
            "narrateur|Le carton repose contre le banc.",
            "narrateur|Le ballon jaune attend dans l'herbe.",
            "enfant-m|Comme tout à l'heure, papa !",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, dans l'herbe.",
            "maman|On est bien, ici.",
            "narrateur|Aniss glisse le doigt sur le fil, sans se presser.",
            "enfant-m|On le voit, maman.",
            "maman|Tu le vois sur le fil ?",
            "enfant-m|Oui, l'éclat.",
            "papa|La limace a bougé, Aniss.",
            "enfant-m|Oui, d'un doigt.",
            "enfant-f|Elle est partie un peu.",
            "narrateur|L'odeur de champignon reste sur le chemin.",
            "enfant-m|Il est là, maman.",
            "maman|Oui, sur le fil.",
            "narrateur|Un éclat de limace tient sur le fil.",
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
        raise SystemExit(f"{SID}: Aniss absent (enfant-m)")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "le corps n'est pas une blague",
        "le corps n est pas une blague",
        "pas une blague",
        "il ne faut pas rire",
        "l'amitié ne dépend pas",
        "corps plus rond",
        "corps plus mince",
        "vous jouez ensemble",
        "on joue ensemble",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Le carton s'écrase. Que font Aniss et Chouchou ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Ils tiennent le carton ensemble. Que font-ils ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
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
        raise SystemExit(f"{SID}: Aniss n'invite pas")
    for must in (
        "fil d'argent",
        "limace",
        "chemin",
        "pluie",
        "terre",
        "carton",
        "ballon",
    ):
        if must not in blob:
            raise SystemExit(f"{SID}: manque monde dump ({must})")
    for ban in (
        "éclat de carton",
        "éclat de chaise",
        "éclat de drap",
        "éclat de perron",
        "drap",
        "chaise",
        "tout doux",
        "tout calme",
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
        "- **Leçon :** DIF.COR.002 — le corps n'est pas une blague "
        "(vécue : carton sur le dos, rire qui commence, Chouchou se tait, "
        "carton écrasé, ils tiennent les bords). JAMAIS dite dans le récit.\n"
        "- **Personnages :** Aniss, Chouchou, papa, maman. Maman ajoutée. "
        "Aniss = enfant-m (propose, trop vite). Chouchou = enfant-f "
        "(silence, non, je regarde, plus tard). Troupe D16. Pas de "
        "maîtresse.\n"
        "- **Lieu :** chemin du parc après la pluie, terre, fil d'argent, "
        "limace, banc mouillé, carton, ballon jaune. ≠ 002-05 drap/chaise. "
        "≠ 002-01 cuisine/cuivre. ≠ 002-06 lanternes/perron.\n"
        "- **Indice unique :** éclat de limace (brille à l'ouverture → "
        "tremble à l'écrasement → luit au refus → tient sur le fil). BAN "
        "éclat de carton / chaise / drap / perron.\n"
        "- **Question moteur :** « Le carton s'écrase. Que font Aniss et "
        "Chouchou ? » expected **jouer**. Slogan non récité (Q autre).\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une odeur de champignon monte du chemin. Sur le fil d'argent, un "
        "éclat de limace brille. Aniss veut un tunnel pour le ballon "
        "**maintenant**. Première idée : pousser trop vite, tirer la "
        "manche. Chouchou : non, la limace. Le carton s'écrase. Un rire "
        "commence, sur toi. Chouchou se tait. Sourire parti. Papa "
        "s'accroupit. Il refuse de foncer. On joue. Ils tiennent. Merci "
        "vécu. Deuxième ruse : il se glisse, ça colle, rire qui revient. "
        "Il refuse, retrouve l'éclat. Poum. Un éclat de limace tient sur "
        "le fil.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chemin du parc après la pluie, terre, champignon, fil "
        "d'argent, limace, banc, herbe mouillée. ≠ 002-05 salon/drap/"
        "chaise.\n"
        "- Désir : un tunnel de carton pour le ballon jaune, maintenant.\n"
        "- Objet : carton mouillé, ballon jaune, bords, fil, limace.\n"
        "- Indice unique : éclat de limace, vu dès l'ouverture, payé "
        "sur le fil. Pas éclat de carton (BAN).\n"
        "- Urgence douce : Chouchou arrive, le tunnel attend, Aniss "
        "accélère.\n"
        "- Imprévu 1 : carton écrasé, manche tirée, rire sur le dos, "
        "Chouchou absente au moment du ballon, ballon coincé.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après « d'accord ».\n"
        "- Imprévu 2 (plus rusé) : il se glisse trop vite, carton collé "
        "au dos, rire qui revient, Chouchou lâche, carton à plat.\n"
        "- Résolution : il refuse de foncer, invite, tient avec elle, "
        "pousse plus lent, poum.\n"
        "- Retour : carton contre le banc, ballon dans l'herbe, éclat "
        "sur le fil.\n\n"
        "## Vécu\n\n"
        "Aniss veut le tunnel **maintenant**. Impatience, puis rire qui "
        "commence, sourire de Chouchou qui part. Chouchou prend son "
        "temps, pose sa limite (non, je regarde, plus tard, attends). "
        "Papa se baisse, pose une question, ne récite pas la règle. Ils "
        "agissent : bords tenus, ballon poussé sans se presser. Merci "
        "vécu. Fin : l'éclat du début tient sur le fil.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le carton-tunnel d'Aniss (noyau dump). Relance dump : "
        "Le carton s'écrase. Que font Aniss et Chouchou ? expected "
        "jouer.\n"
        "- Lieu du dump (chemin du parc après la pluie, terre, fil "
        "d'argent, limace). Maman ajoutée. Chouchou = enfant-f.\n"
        "- Ouverture inventée (une odeur de champignon monte du chemin), "
        "pas un gabarit v2, pas « La terre du chemin sent le champignon » "
        "du dump.\n"
        "- Indice unique : éclat de limace. BAN éclat de carton (roster). "
        "Distinct 002-05 (drap/chaise). Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » du dump.\n"
        "- Leçon non dite : on la voit quand le rire s'arrête, quand "
        "Chouchou recule, quand ils tiennent les bords. Pas « le corps "
        "n'est pas une blague » (Q autre). Pas « vous jouez ensemble » "
        "en morale.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Maman parle. Papa parle.\n"
        "- 5 chunks, kinds inchangés. example4 : 007, 039, 071. "
        "Voix : `_write_atom_col_eco_002_05.py` (Aniss).\n"
        f"- {nwords} mots. N3 ≤ 16. TTS : notes, ssml, xai, piper par "
        "chunk.\n\n"
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
