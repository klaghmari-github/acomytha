#!/usr/bin/env python3
"""ATOM-DIF.COR.002-05 — La cabane de draps de Raphaël (F-NAR-019, N3, DIF.COR.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.002-05"
TITLE = "La cabane de draps de Raphaël"
N3 = LIMITS["N3"]
CHARS = "Raphaël, Aniss, papa, maman"
SETTING = "salon l'après-midi, drap, pince, chaise"
INDICE = "éclat de chaise"
FIL = (
    "Un rai de poussière traverse le salon. Sur le bois, un éclat de "
    "chaise brille. Raphaël veut une cabane, maintenant, avec le drap. "
    "Aniss arrive. Le drap gonfle. Un rire commence. Aniss se tait. "
    "Le drap trop court. Raphaël refuse de foncer. Ils tiennent les "
    "chaises, à deux. Merci vécu. Une chaise trop vite. L'éclat de "
    "chaise tient sur le bois."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tiroir|fraisier|cuivre|buis|coussin|cerceau|planche|"
    r"robinet|figue|émail|email|samare|bassine)\b",
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
    "les trois mots",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "il ne faut pas rire",
    "l'amitié ne dépend pas",
    "l'amitie ne depend pas",
    "vous jouez",
    "on joue",
    "tailles différentes",
    "tailles differentes",
    "corps plus rond",
    "corps plus mince",
    "pas une blague",
    "n'est pas une blague",
    "n est pas une blague",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "trois notes",
    "lumière couleur de miel",
    "lumiere couleur de miel",
    "éclat de pince",
    "éclat de drap",
    "éclat de tapis",
    "éclat d'horloge",
    "éclat de horloge",
    "éclat de vitre",
    "éclat de soleil",
    "éclat de biscuit",
    "éclat de miette",
    "éclat de bois",
    "éclat de dossier",
    "éclat de coin",
    "éclat de fil",
    "éclat de cerceau",
    "éclat de coussin",
    "éclat de tiroir",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de fraisier",
    "éclat de planche",
    "éclat de robinet",
    "éclat de figue",
    "éclat d'émail",
    "éclat d'email",
    "éclat de samare",
    "éclat de bassine",
    "éclat de caisse",
    "éclat de camion",
    "éclat de torchon",
    "éclat de dalle",
    "éclat de cube",
    "éclat de carton",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de manteau",
    "éclat de casserole",
    "éclat de citron",
    "éclat de coquille",
    "éclat de zeste",
    "éclat de nappe",
    "éclat de farine",
    "éclat de bol",
    "éclat de tablier",
    "éclat de volet",
    "éclat de pavé",
    "éclat de pave",
    "éclat de parapluie",
    "éclat de bâche",
    "éclat de bache",
    "éclat de poire",
    "éclat de seau",
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
    "éclat de ballon",
    "éclat de marche",
    "éclat de grain",
    "éclat de liste",
    "éclat de couloir",
    "éclat de plaque",
    "éclat de dalle",
    "éclat de pierre",
    "éclat de grille",
    "éclat de couvercle",
    "éclat de thermos",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caillou",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat de lessive",
    "éclat de carreau",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pomme",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de chaise",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_cabane_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="corps",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=on_joue_on_ne_rit_pas_du_corps; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="drap",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=ils_tiennent_les_chaises_a_deux; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de chaise",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de chaise",
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
    "expected_answer": "jouer",
    "accepted_examples": (
        "jouer | on joue | pas une blague | pas blague | la cabane"
    ),
    "retry_prompt": "On joue. Le corps n'est pas une blague. Que fait-on ?",
    "engine_ok_text": "Oui, jouer.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "horloge,drap",
        [
            "narrateur|Un rai de poussière traverse le salon.",
            "narrateur|Il brille dans le carré de soleil.",
            "enfant-m|Il brille, papa !",
            "papa|Tu le vois, près du tapis ?",
            "enfant-m|Oui, un trait clair.",
            "narrateur|L'horloge fait un tic lent.",
            "enfant-m|Je l'entends, maman.",
            "maman|Elle tic, près de la vitre ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un drap sent le fil, un peu chaud.",
            "narrateur|Il sèche sur le dossier d'une chaise.",
            "narrateur|Une pince de bois tient un coin.",
            "enfant-m|Elle pince le drap.",
            "papa|La pince est en bois, Raphaël ?",
            "enfant-m|Oui, un peu ronde.",
            "narrateur|Sur le bois, un éclat de chaise brille.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, sur la chaise ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|Le tapis garde un carré de soleil.",
            "maman|Tes pieds sont sur le tapis ?",
            "enfant-m|Oui, maman.",
            "narrateur|Une mouche se pose sur la vitre.",
            "enfant-m|Elle est là.",
            "maman|Près du soleil ?",
            "enfant-m|Oui.",
            "enfant-m|Je veux une cabane, maintenant !",
            "papa|Avec le drap ?",
            "enfant-m|Oui, au milieu.",
            "maman|Au milieu du salon ?",
            "enfant-m|Oui, maman.",
            "narrateur|En ce moment, Raphaël tire deux chaises.",
            "narrateur|Les pieds des chaises râpent le bois.",
            "enfant-m|Elles font du bruit.",
            "papa|Tu les poses, Raphaël ?",
            "enfant-m|Oui, papa.",
            "narrateur|Aniss arrive près du tapis.",
            "narrateur|Il a une chaussette un peu tordue.",
            "enfant-m|Aniss !",
            "copain|J'arrive.",
            "enfant-m|Tu tiens la chaise, maintenant !",
            "narrateur|Ils jettent le drap par-dessus.",
            "narrateur|Le drap tombe en biais.",
            "narrateur|Aniss se glisse dessous, un peu.",
            "narrateur|Le drap gonfle sur ses épaules.",
            "enfant-m|Ça gonfle drôle !",
            "narrateur|Un rire commence dans la bouche de Raphaël.",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "copain|Non.",
            "narrateur|Aniss recule vers la vitre.",
            "enfant-m|Oh.",
            "narrateur|Raphaël jette le drap trop vite, tout seul.",
            "narrateur|Le drap est trop court.",
            "enfant-m|Il y a un trou !",
            "copain|Oh.",
            "narrateur|L'éclat de chaise tremble, puis tient.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Aniss, Raphaël ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains tiennent le drap ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Le corps n'est pas une blague.",
            "narrateur|Que fait-on ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "drap,biscuit",
        [
            "narrateur|Raphaël veut le drap, tout de suite.",
            "enfant-m|Je le jette, maintenant !",
            "narrateur|Il avance trop vite vers Aniss.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copain|Non.",
            "narrateur|Aniss reste près de la vitre.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Raphaël refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe les chaises, un instant.",
            "narrateur|Il écoute le tic de l'horloge.",
            "papa|Tu veux la cabane avec Aniss ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Tu tiens la chaise ?",
            "narrateur|Aniss ne dit rien, d'abord.",
            "narrateur|Il pose les mains sur le bois.",
            "copain|Je la tiens.",
            "enfant-m|D'accord.",
            "papa|Merci, Raphaël.",
            "narrateur|Papa a vu les deux, près du drap.",
            "maman|Le drap est chaud, sous les doigts.",
            "enfant-m|Il sent le soleil.",
            "narrateur|Ils rapprochent les chaises, sans se presser.",
            "narrateur|Raphaël pince un coin, avec la pince.",
            "narrateur|Le trou se ferme, cette fois.",
            "enfant-m|Il tient !",
            "copain|Oui.",
            "papa|Tu le vois, le toit ?",
            "enfant-m|Oui, papa.",
            "maman|On entre, Raphaël ?",
            "enfant-m|On entre.",
            "copain|On entre.",
            "narrateur|Ils se glissent dessous.",
            "narrateur|La lumière devient jaune.",
            "enfant-m|On est dedans.",
            "copain|C'est chaud.",
            "papa|Deux biscuits, pour vous.",
            "narrateur|Papa passe les biscuits sous le bord.",
            "narrateur|Ça croque, un peu.",
            "narrateur|Une miette tombe sur le tapis.",
            "maman|La miette est sur le tapis ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le ventre de Raphaël se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste sous le drap ?",
            "enfant-m|Oui.",
            "maman|Tes mains sont au chaud ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "chaise",
        [
            "narrateur|Raphaël veut un toit plus grand.",
            "enfant-m|Une grande cabane, maintenant !",
            "narrateur|Il tire une chaise trop vite.",
            "narrateur|Il regarde les épaules d'Aniss, trop longtemps.",
            "narrateur|Un rire revient dans sa bouche.",
            "copain|Attends.",
            "narrateur|Aniss lâche le bois.",
            "narrateur|La chaise glisse sur le tapis.",
            "enfant-m|Ça tombe !",
            "narrateur|Le drap tombe sur Aniss.",
            "narrateur|Raphaël avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Raphaël refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe la chaise, un instant.",
            "narrateur|Il écoute le tic de l'horloge.",
            "narrateur|Sur le bois, un éclat de chaise luit.",
            "enfant-m|Là, sur le bois.",
            "enfant-m|Tu tiens, Aniss ?",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Il reprend le dossier, sans parler.",
            "copain|Oui.",
            "narrateur|Ils recalent la chaise, sans se presser.",
            "narrateur|Le drap redevient un toit.",
            "maman|Le toit est jaune ?",
            "enfant-m|Il est jaune.",
            "copain|Il est beau.",
            "narrateur|La pince tient le coin.",
            "enfant-m|Elle tient.",
            "papa|Tu restes un peu ?",
            "enfant-m|Oui, papa.",
            "maman|L'horloge tic plus loin.",
            "enfant-m|On l'entend ?",
            "papa|Oui, sous le drap.",
            "narrateur|La cabane sent le soleil.",
            "enfant-m|Elle colle aux doigts.",
            "maman|Comme le fil, oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "drap",
        [
            "narrateur|Ils restent sous le drap.",
            "narrateur|Maman recale un coin, sans bruit.",
            "enfant-m|On a fait une cabane, papa.",
            "papa|Tu la vois, toi ?",
            "enfant-m|Oui, au milieu.",
            "maman|On est bien, ici.",
            "narrateur|Raphaël glisse le doigt sur le bois.",
            "enfant-m|On le sent, maman.",
            "maman|Tu le sens sur tes doigts ?",
            "enfant-m|Oui, il est lisse.",
            "papa|Le toit est jaune, Raphaël.",
            "enfant-m|Oui, avec Aniss.",
            "copain|Le toit est resté.",
            "narrateur|Le drap sent le soleil, un peu chaud.",
            "enfant-m|Il est là, maman.",
            "maman|Oui, sur les chaises.",
            "narrateur|La mouche a quitté la vitre.",
            "narrateur|Un éclat de chaise tient sur le bois.",
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
        if not skip_lesson:
            for bad in EXTRA_BAD:
                if bad in low:
                    raise SystemExit(f"extra {bad}: {ph}")
        if role not in ("narrateur", "papa", "maman", "enfant-m", "copain"):
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
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Raphaël = enfant-m)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Aniss absent (copain)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m", "copain") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "copain" for r in roles):
        raise SystemExit(f"{SID}: copain absent")
    if not any(r == "enfant-m" for r in roles):
        raise SystemExit(f"{SID}: Raphaël absent (enfant-m)")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "le corps n'est pas une blague",
        "le corps n est pas une blague",
        "pas une blague",
        "on joue",
        "vous jouez",
        "il ne faut pas rire",
        "l'amitié ne dépend pas",
        "corps plus rond",
        "corps plus mince",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Le corps n'est pas une blague. Que fait-on ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = str(q.get("retry_prompt") or "").lower()
    if "que fait-on" not in retry:
        raise SystemExit(f"{SID}: retry sans Que fait-on")
    if "jouer" not in retry and "on joue" not in retry:
        raise SystemExit(f"{SID}: retry sans jouer")
    copain_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    ).lower()
    if "non" not in copain_txt:
        raise SystemExit(f"{SID}: Aniss sans non")
    if "attends" not in copain_txt:
        raise SystemExit(f"{SID}: Aniss sans attends")
    if "drap" not in blob:
        raise SystemExit(f"{SID}: manque drap")
    if "pince" not in blob:
        raise SystemExit(f"{SID}: manque pince")
    if "chaise" not in blob:
        raise SystemExit(f"{SID}: manque chaise")
    if "salon" not in blob:
        raise SystemExit(f"{SID}: manque salon")
    for ban in (
        "éclat de pince",
        "éclat de drap",
        "éclat de cerceau",
        "éclat de coussin",
        "éclat de tiroir",
        "éclat de cuivre",
        "éclat de buis",
        "éclat de fraisier",
        "éclat de planche",
        "cerceau",
        "coussin",
        "tiroir",
        "fraisier",
        "cuivre",
        "buis",
        "tout doux",
        "tout calme",
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
        "- **Leçon :** DIF.COR.002 — le corps n'est pas une blague "
        "(vécue : drap qui gonfle, rire qui commence, Aniss se tait, "
        "drap trop court, ils tiennent les chaises à deux). JAMAIS dite "
        "dans le récit.\n"
        "- **Personnages :** Raphaël, Aniss, papa, maman. Maman ajoutée. "
        "Raphaël = enfant-m (propose, trop vite). Aniss = copain "
        "(silence, non, attends). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** salon l'après-midi, drap, pince, chaise, horloge, "
        "rai de poussière, tapis, vitre, mouche. ≠ ATOM-DIF.COR.001-04 "
        "drap/cerceau/fil (cour, tunnel). Pas éclat de pince. ≠ 002-01 "
        "cuivre. ≠ 002-02 buis. ≠ 002-03 tiroir. ≠ 002-04 fraisier.\n"
        "- **Indice unique :** éclat de chaise (brille à l'ouverture → "
        "tremble au trou → luit au refus → tient sur le bois). BAN "
        "éclat de pince / drap / cerceau / coussin / tiroir / cuivre / "
        "buis / fraisier / planche.\n"
        "- **Question moteur :** « Le corps n'est pas une blague. Que "
        "fait-on ? » expected **jouer**. Non récitée dans les autres "
        "chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un rai de poussière traverse le salon. Sur le bois, un éclat de "
        "chaise brille. Drap, pince, horloge, après-midi. Raphaël veut "
        "une cabane **maintenant**. Aniss arrive. Le drap gonfle sur "
        "ses épaules. Un rire commence. Aniss se tait, recule : non. "
        "Raphaël jette le drap tout seul : trop court, un trou. Sourire "
        "parti. Papa s'accroupit. Il refuse de foncer. Ils tiennent les "
        "chaises. Merci vécu. Deuxième ruse : chaise trop vite, rire "
        "qui revient, Aniss lâche. Il s'arrête, lit l'éclat. Un éclat "
        "de chaise tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : salon l'après-midi, drap chaud, pince de bois, "
        "chaises, horloge, rai de poussière, tapis, vitre. ≠ 001-04 "
        "cerceau/fil. ≠ 002-01..04.\n"
        "- Désir : une cabane avec le drap, maintenant, au milieu.\n"
        "- Objet : drap, pince, deux chaises, biscuits, miette.\n"
        "- Indice unique : éclat de chaise, vu dès l'ouverture, payé "
        "sur le bois. Pas éclat de pince.\n"
        "- Urgence douce : Aniss arrive, la cabane attend, Raphaël "
        "accélère.\n"
        "- Imprévu 1 : rire sur le drap gonflé, Aniss recule, drap trop "
        "court, un trou.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« d'accord ».\n"
        "- Imprévu 2 (plus rusé) : grande cabane trop vite, rire qui "
        "revient, Aniss lâche, chaise qui glisse, drap sur Aniss.\n"
        "- Résolution : il refuse de foncer, observe, écoute le tic, "
        "retrouve l'éclat, Aniss reprend le dossier.\n"
        "- Retour : toit jaune, drap chaud, éclat sur le bois.\n\n"
        "## Vécu\n\n"
        "Raphaël veut la cabane **maintenant**. Impatience, puis rire "
        "qui commence, sourire d'Aniss qui part. Aniss prend son temps, "
        "pose sa limite (non, attends, silence). Papa se baisse, pose "
        "une question, ne récite pas la règle. Ils agissent : chaises "
        "tenues, pince au coin, toit sans se presser. Merci vécu. Fin : "
        "l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : La cabane de draps de Raphaël (noyau dump). Relance : "
        "Que fait-on ? expected jouer.\n"
        "- Lieu du dump (salon l'après-midi, drap, pince, chaise). "
        "Maman ajoutée. Aniss = copain.\n"
        "- Ouverture inventée (rai de poussière dans le salon), pas un "
        "gabarit v2, pas « Un drap sent encore le fil » du dump, pas "
        "« joue au salon ».\n"
        "- Indice unique : éclat de chaise. BAN éclat de pince / drap / "
        "cerceau / coussin / tiroir / cuivre / buis / fraisier / "
        "planche. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « encore » / « tout doux » / « bravo » du dump.\n"
        "- Leçon non dite : on la voit quand le rire s'arrête, quand "
        "Aniss recule, quand ils tiennent les chaises. Pas « le corps "
        "n'est pas une blague » hors question. Pas « on joue » / "
        "« vous jouez » / « il ne faut pas rire ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question. "
        "Maman parle. Papa parle.\n"
        "- Question moteur inchangée : « Le corps n'est pas une blague. "
        "Que fait-on ? ». expected jouer. 5 chunks, kinds inchangés.\n"
        "- example4 005 / 037 / 069 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_cor_001_06.py` (Raphaël).\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers la chaise.\n"
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
