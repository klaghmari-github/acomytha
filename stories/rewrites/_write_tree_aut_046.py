#!/usr/bin/env python3
"""TREE-AUT-046 — Le sac jaune de Victorino sur le banc (F-NAR-019, N2)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-046"
N2 = LIMITS["N2"]
TITLE = "Le sac jaune de Victorino sur le banc"
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
    "maîtresse",
    "maitresse",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "marque fine",
    "ombre-flèche",
    "ombre en forme de flèche",
    "perle de verre",
    "ancre minuscule",
    "étoile brune",
    "fil pâle",
    "virgule d'or",
    "œillet de cuivre",
    "bouton de nacre",
    "nœud de raphia",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="dent de laitue",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=sac_vide_avant_l_escargot; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note=(
            "arc=choix; intention=inviter; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=ton_choix_change_la_manière; "
            "tempo=suspendu; sourire=léger; respiration=pause_avant_choix"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="sac",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=le_goûter_voyage_dans_le_sac; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="sac",
        note=(
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=la_sangle_pèse_un_peu; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note=(
            "arc=action; intention=entraîner; emotion=impatience; intensite=2; "
            "destinataire=enfant; sous_texte=la_main_lâche_le_goûter; "
            "tempo=vif; sourire=léger; respiration=courte"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; "
            "intensite=2; destinataire=enfant; sous_texte=un_faux_jaune_ment_la_dent_dit_vrai; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="dent de laitue",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=il_ouvre_sans_foncer; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="dent de laitue",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=la_dent_et_le_banc_paient_le_début; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

FOOD = {
    1: dict(lab="une pomme", le="la pomme", un="une pomme", short="pomme", sons="pomme"),
    2: dict(lab="un yaourt", le="le yaourt", un="un yaourt", short="yaourt", sons="pot"),
    3: dict(lab="un morceau de pain", le="le pain", un="un morceau de pain", short="pain", sons="pain"),
}
LIEU = {
    1: dict(lab="la cuisine", ou="dans la cuisine", short="cuisine", sons="evier,chaise"),
    2: dict(lab="le jardin", ou="dans le jardin", short="jardin", sons="arrosoir,banc"),
    3: dict(lab="la chambre", ou="dans la chambre", short="chambre", sons="rideau,tapis"),
}
JEU = {
    1: dict(lab="les cubes", un="un cube", le="le cube", short="cubes", sons="cubes,bois"),
    2: dict(lab="le livre", un="le livre", le="le livre", short="livre", sons="page,livre"),
    3: dict(lab="la dînette", un="une tasse", le="la tasse", short="dînette", sons="tasse,dinette"),
}

Q_FIELDS = {
    1: {
        "expected_answer": "sac",
        "accepted_examples": "sac | le sac | dans le sac | le sac jaune",
        "retry_prompt": "Dans le sac jaune. Il l'a mis où ?",
    },
    2: {
        "expected_answer": "sac",
        "accepted_examples": "sac | le sac | dans le sac | le sac jaune",
        "retry_prompt": "Dans le sac jaune. Il l'a mis où ?",
    },
    3: {
        "expected_answer": "sac",
        "accepted_examples": "sac | le sac | dans le sac | le sac jaune",
        "retry_prompt": "Dans le sac jaune. Il l'a mis où ?",
    },
}


def vet(lines: list[str]) -> list[str]:
    out: list[str] = []
    starts: list[str] = []
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
    for k, v in extra.items():
        if k in ("emphasis", "note", "pause_before_ms", "night_policy", "fields"):
            continue
        out[k] = v
    return out


def path_ids(a: int, b: int, c: int) -> list[str]:
    return [
        "CHK_T0000_P0000",
        "CHK_T0001_P0000",
        f"CHK_T0001_P000{a}",
        f"CHK_T0001_P000{a}_Q0001",
        f"CHK_T0001_P000{a}_C0001",
        f"CHK_T0001_P000{a}_T0002_P0000",
        f"CHK_T0001_P000{a}_T0002_P000{b}",
        f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
        f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}",
        f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}_F0001",
    ]


# Ouverture : le banc craque sans personne. Indice unique = dent de laitue.
OPENING = [
    "narrateur|Le banc de bois craque, sans personne.",
    "narrateur|Ce n'est pas un oiseau.",
    "narrateur|C'est le sac jaune, qui a glissé.",
    "narrateur|Sur la boucle, une dent de laitue tient.",
    "narrateur|Elle est froide, un peu collée.",
    "narrateur|Papa râcle l'allée, ça parle graviers.",
    "narrateur|Maman tend le linge, près de l'arrosoir.",
    "narrateur|Le bec de zinc garde une goutte.",
    "narrateur|Un escargot avance, vers le cœur vert.",
    "maman|Tu as vu le sac, Victorino ?",
    "enfant-m|Il est à moi, je le veux !",
    "narrateur|En ce moment, il tire la sangle.",
    "narrateur|Le sac retombe, mou, vide.",
    "enfant-m|Il n'y a rien, papa !",
    "narrateur|Le sourire de Victorino disparaît.",
    "papa|Tu auras faim, près de l'escargot ?",
    "enfant-m|Le camp, avant qu'il touche la laitue !",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "papa|On glisse un goûter, alors ?",
]

T1_CHOICE = [
    "narrateur|Le goûter peut voyager, dans le sac.",
    "papa|Tu glisses quoi, pour le camp ?",
    "maman|Une pomme, un yaourt, ou un morceau de pain ?",
]

T1 = {
    1: [
        "narrateur|Victorino saisit la pomme, trop vite.",
        "narrateur|Elle est lisse, froide de la rosée.",
        "enfant-m|Je la porte, moi !",
        "papa|À la main, jusqu'au camp ?",
        "narrateur|La pomme glisse entre ses doigts.",
        "enfant-m|Elle tombe !",
        "narrateur|Le sourire de Victorino disparaît.",
        "narrateur|Dans sa poitrine, ça serre, fort.",
        "narrateur|Papa s'accroupit, près du banc.",
        "papa|Le sac est là, sur le bois.",
        "narrateur|Victorino ouvre le sac jaune.",
        "narrateur|Il glisse la pomme au fond.",
        "narrateur|Elle fait un petit choc.",
        "enfant-m|Elle est dedans, à l'abri.",
        "narrateur|Sur la boucle, la dent de laitue tient.",
        "maman|Elle voyage avec toi ?",
    ],
    2: [
        "narrateur|Victorino saisit le yaourt, trop vite.",
        "narrateur|Le pot est froid, mouillé de goutte.",
        "enfant-m|Je le serre, moi !",
        "maman|À la main, jusqu'au camp ?",
        "narrateur|Le pot glisse, et tape le bois.",
        "enfant-m|Il va rouler !",
        "narrateur|Le sourire de Victorino disparaît.",
        "narrateur|Ses épaules baissent, près du banc.",
        "narrateur|Maman s'accroupit, à sa hauteur.",
        "maman|Le sac attend, sur le bois.",
        "narrateur|Victorino ouvre le sac jaune.",
        "narrateur|Il glisse le pot au fond.",
        "narrateur|Le tissu se tend, un peu.",
        "enfant-m|Il est dedans, au frais.",
        "narrateur|Sur la boucle, la dent de laitue tient.",
        "papa|Il voyage au froid ?",
    ],
    3: [
        "narrateur|Victorino saisit le pain, trop vite.",
        "narrateur|Le papier blanc veut s'envoler.",
        "enfant-m|Je le porte, moi !",
        "papa|Le vent le prend, à la main ?",
        "narrateur|Un coin de papier file, vers l'escargot.",
        "enfant-m|Il part !",
        "narrateur|Le sourire de Victorino disparaît.",
        "narrateur|L'envie et l'inquiétude se bousculent.",
        "narrateur|Papa s'accroupit, près du banc.",
        "papa|Le sac est là, sur le bois.",
        "narrateur|Victorino ouvre le sac jaune.",
        "narrateur|Le papier froisse, au fond.",
        "narrateur|Le pain disparaît, à l'abri.",
        "enfant-m|Il est dedans, au chaud.",
        "narrateur|Sur la boucle, la dent de laitue tient.",
        "maman|Il sent le four, là ?",
    ],
}

T1_Q = {
    1: [
        "narrateur|La pomme a quitté le banc.",
        "papa|Victorino l'a mise où ?",
    ],
    2: [
        "narrateur|Le pot froid a quitté le bois.",
        "maman|Victorino l'a mis où ?",
    ],
    3: [
        "narrateur|Le pain a quitté le banc.",
        "papa|Victorino l'a mis où ?",
    ],
}

T1_C = {
    1: [
        "narrateur|La pomme n'est plus dans sa main.",
        "enfant-m|Elle voyage, dans le sac.",
        "maman|Merci, Victorino, tu l'as glissée.",
        "papa|Le camp, on le choisit où ?",
        "enfant-m|Près de l'escargot, avant la laitue.",
        "narrateur|La sangle pèse, un peu, sur l'épaule.",
        "narrateur|La dent de laitue reste à la boucle.",
        "narrateur|L'escargot avance d'un cran.",
    ],
    2: [
        "narrateur|Le pot n'est plus dans sa main.",
        "enfant-m|Il voyage, dans le sac.",
        "papa|Merci, Victorino, tu l'as glissé.",
        "maman|Le camp, on le choisit où ?",
        "enfant-m|Près de l'escargot, avant la laitue.",
        "narrateur|La sangle pèse, un peu, sur l'épaule.",
        "narrateur|La dent de laitue reste à la boucle.",
        "narrateur|Une goutte sèche sur le bois.",
    ],
    3: [
        "narrateur|Le pain n'est plus dans sa main.",
        "enfant-m|Il voyage, dans le sac.",
        "maman|Merci, Victorino, tu l'as glissé.",
        "papa|Le camp, on le choisit où ?",
        "enfant-m|Près de l'escargot, avant la laitue.",
        "narrateur|La sangle pèse, un peu, sur l'épaule.",
        "narrateur|La dent de laitue reste à la boucle.",
        "narrateur|Le papier ne s'envole plus.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Le camp de la laitue peut naître ici.",
        "papa|La cuisine, le jardin, ou la chambre ?",
        "maman|Le sac jaune vient avec toi.",
    ],
    2: [
        "narrateur|Le camp de la laitue cherche un coin.",
        "maman|La cuisine, le jardin, ou la chambre ?",
        "papa|Le sac jaune vient avec toi.",
    ],
    3: [
        "narrateur|Le camp de la laitue attend un lieu.",
        "papa|La cuisine, le jardin, ou la chambre ?",
        "maman|Le sac jaune vient avec toi.",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    table = {
        (1, 1): [
            "narrateur|Victorino porte le sac vers la cuisine.",
            "narrateur|Le carrelage pique, un peu froid.",
            "enfant-m|Le camp, sous la table !",
            "narrateur|Il pose le sac sur une chaise.",
            "narrateur|Un torchon jaune attend, plié.",
            "narrateur|La pomme roule, au fond du sac.",
            "enfant-m|Je prends le torchon, pour le toit.",
            "narrateur|Le sac glisse, derrière la chaise.",
            "narrateur|Le torchon jaune reste, seul, sur le bois.",
            "enfant-m|Mon sac !",
            "narrateur|Il saisit le torchon, trop vite.",
            "narrateur|Ce n'est pas le sac, c'est le linge.",
            "enfant-m|Il a disparu.",
            "narrateur|Le sourire de Victorino disparaît.",
            "maman|Regarde la boucle, pas le jaune.",
            "papa|Personne ne dit où courir.",
            "enfant-m|Je ne fonce pas.",
        ],
        (1, 2): [
            "narrateur|Victorino repose le sac sur le banc.",
            "narrateur|L'herbe mouille le bas des chaussures.",
            "enfant-m|Le camp, sous le bois !",
            "narrateur|Un gant jaune sèche, près de l'arrosoir.",
            "narrateur|La pomme fait un rond, au fond.",
            "enfant-m|Le gant, pour le toit du camp.",
            "narrateur|Le sac glisse, sous le banc de bois.",
            "narrateur|Le gant jaune reste, seul, sur le bois.",
            "enfant-m|Mon sac !",
            "narrateur|Il saisit le gant, trop vite.",
            "narrateur|Ce n'est pas le sac, c'est le gant.",
            "enfant-m|Il s'est caché.",
            "narrateur|Le sourire de Victorino disparaît.",
            "papa|Regarde la boucle, pas le jaune.",
            "maman|Personne ne donne la réponse.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|L'escargot n'a pas atteint le cœur.",
        ],
        (1, 3): [
            "narrateur|Victorino monte le sac vers la chambre.",
            "narrateur|Un rayon passe entre les rideaux.",
            "enfant-m|Le camp, près du lit !",
            "narrateur|Il pose le sac près de l'oreiller.",
            "narrateur|Un coussin jaune attend, rond et mou.",
            "narrateur|La pomme appuie un peu le tissu.",
            "enfant-m|Le coussin, pour le toit du camp.",
            "narrateur|Le sac glisse, entre le lit et le mur.",
            "narrateur|Le coussin jaune reste, seul, sur le drap.",
            "enfant-m|Mon sac !",
            "narrateur|Il saisit le coussin, trop vite.",
            "narrateur|Ce n'est pas le sac, c'est le coussin.",
            "enfant-m|Il a disparu.",
            "narrateur|Le sourire de Victorino disparaît.",
            "maman|Regarde la boucle, pas le jaune.",
            "papa|Personne ne dit où chercher.",
            "enfant-m|Je ne fonce pas.",
        ],
        (2, 1): [
            "narrateur|Victorino porte le sac vers la cuisine.",
            "narrateur|Le carrelage pique, un peu froid.",
            "enfant-m|Le camp, sous la table !",
            "narrateur|Il pose le sac sur une chaise.",
            "narrateur|Un torchon jaune attend, plié.",
            "narrateur|Le pot laisse un rond froid, au fond.",
            "enfant-m|Je prends le torchon, pour le toit.",
            "narrateur|Le sac glisse, derrière la chaise.",
            "narrateur|Le torchon jaune reste, seul, sur le bois.",
            "enfant-m|Mon sac !",
            "narrateur|Il saisit le torchon, trop vite.",
            "narrateur|Ce n'est pas le sac, c'est le linge.",
            "enfant-m|Le froid a disparu.",
            "narrateur|Ses épaules baissent, près de la chaise.",
            "papa|Regarde la boucle, pas le jaune.",
            "maman|Personne ne dit où courir.",
            "enfant-m|Je ne fonce pas.",
        ],
        (2, 2): [
            "narrateur|Victorino repose le sac sur le banc.",
            "narrateur|L'herbe mouille le bas des chaussures.",
            "enfant-m|Le camp, sous le bois !",
            "narrateur|Un gant jaune sèche, près de l'arrosoir.",
            "narrateur|Le pot froid touche le tissu.",
            "enfant-m|Le gant, pour le toit du camp.",
            "narrateur|Le sac glisse, sous le banc de bois.",
            "narrateur|Le gant jaune reste, seul, sur le bois.",
            "enfant-m|Mon sac !",
            "narrateur|Il saisit le gant, trop vite.",
            "narrateur|Ce n'est pas le sac, c'est le gant.",
            "enfant-m|Le froid s'est caché.",
            "narrateur|Ses épaules baissent, près du banc.",
            "maman|Regarde la boucle, pas le jaune.",
            "papa|Personne ne donne la réponse.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le bec de zinc garde sa goutte.",
        ],
        (2, 3): [
            "narrateur|Victorino monte le sac vers la chambre.",
            "narrateur|Un rayon passe entre les rideaux.",
            "enfant-m|Le camp, près du lit !",
            "narrateur|Il pose le sac près de l'oreiller.",
            "narrateur|Un coussin jaune attend, rond et mou.",
            "narrateur|Le pot laisse un rond froid, au fond.",
            "enfant-m|Le coussin, pour le toit du camp.",
            "narrateur|Le sac glisse, entre le lit et le mur.",
            "narrateur|Le coussin jaune reste, seul, sur le drap.",
            "enfant-m|Mon sac !",
            "narrateur|Il saisit le coussin, trop vite.",
            "narrateur|Ce n'est pas le sac, c'est le coussin.",
            "enfant-m|Le froid a disparu.",
            "narrateur|Ses épaules baissent, près du lit.",
            "papa|Regarde la boucle, pas le jaune.",
            "maman|Personne ne dit où chercher.",
            "enfant-m|Je ne fonce pas.",
        ],
        (3, 1): [
            "narrateur|Victorino porte le sac vers la cuisine.",
            "narrateur|Le carrelage pique, un peu froid.",
            "enfant-m|Le camp, sous la table !",
            "narrateur|Il pose le sac sur une chaise.",
            "narrateur|Un torchon jaune attend, plié.",
            "narrateur|Le pain sent le four, au fond.",
            "enfant-m|Je prends le torchon, pour le toit.",
            "narrateur|Le sac glisse, derrière la chaise.",
            "narrateur|Le torchon jaune reste, seul, sur le bois.",
            "enfant-m|Mon sac !",
            "narrateur|Il saisit le torchon, trop vite.",
            "narrateur|Ce n'est pas le sac, c'est le linge.",
            "enfant-m|L'odeur a disparu.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "maman|Regarde la boucle, pas le jaune.",
            "papa|Personne ne dit où courir.",
            "enfant-m|Je ne fonce pas.",
        ],
        (3, 2): [
            "narrateur|Victorino repose le sac sur le banc.",
            "narrateur|L'herbe mouille le bas des chaussures.",
            "enfant-m|Le camp, sous le bois !",
            "narrateur|Un gant jaune sèche, près de l'arrosoir.",
            "narrateur|Le papier du pain veut s'envoler.",
            "enfant-m|Le gant, pour le toit du camp.",
            "narrateur|Le sac glisse, sous le banc de bois.",
            "narrateur|Le gant jaune reste, seul, sur le bois.",
            "enfant-m|Mon sac !",
            "narrateur|Il saisit le gant, trop vite.",
            "narrateur|Ce n'est pas le sac, c'est le gant.",
            "enfant-m|Le pain s'est caché.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Regarde la boucle, pas le jaune.",
            "maman|Personne ne donne la réponse.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|L'escargot n'a pas atteint le cœur.",
        ],
        (3, 3): [
            "narrateur|Victorino monte le sac vers la chambre.",
            "narrateur|Un rayon passe entre les rideaux.",
            "enfant-m|Le camp, près du lit !",
            "narrateur|Il pose le sac près de l'oreiller.",
            "narrateur|Un coussin jaune attend, rond et mou.",
            "narrateur|Le pain sent le four, au fond.",
            "enfant-m|Le coussin, pour le toit du camp.",
            "narrateur|Le sac glisse, entre le lit et le mur.",
            "narrateur|Le coussin jaune reste, seul, sur le drap.",
            "enfant-m|Mon sac !",
            "narrateur|Il saisit le coussin, trop vite.",
            "narrateur|Ce n'est pas le sac, c'est le coussin.",
            "enfant-m|L'odeur a disparu.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "maman|Regarde la boucle, pas le jaune.",
            "papa|Personne ne dit où chercher.",
            "enfant-m|Je ne fonce pas.",
        ],
    }
    return table[(a, b)]


T3_CHOICE = {
    1: [
        "narrateur|Un jeu veut entrer dans le sac.",
        "papa|Les cubes, le livre, ou la dînette ?",
        "maman|On suit la dent de laitue.",
    ],
    2: [
        "narrateur|Un jeu veut voyager, avec le goûter.",
        "maman|Les cubes, le livre, ou la dînette ?",
        "papa|On suit la dent de laitue.",
    ],
    3: [
        "narrateur|Un jeu cherche une place, au fond.",
        "papa|Les cubes, le livre, ou la dînette ?",
        "maman|On suit la dent de laitue.",
    ],
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    arrive = {
        (1, 1): [
            "narrateur|Sous la table, un cube jaune brille.",
            "enfant-m|Les cubes, dans le sac, pour le camp.",
            "narrateur|Il empile trop vite, trop haut.",
        ],
        (1, 2): [
            "narrateur|Sur la table, un livre à couverture jaune.",
            "enfant-m|Le livre, dans le sac, pour le camp.",
            "narrateur|Il pousse trop vite, trop fort.",
        ],
        (1, 3): [
            "narrateur|Près de l'évier, une tasse jaune attend.",
            "enfant-m|La dînette, dans le sac, pour le camp.",
            "narrateur|Il saisit la tasse, trop vite.",
        ],
        (2, 1): [
            "narrateur|Dans l'herbe, un cube jaune brille.",
            "enfant-m|Les cubes, dans le sac, pour le camp.",
            "narrateur|Il empile trop vite, trop haut.",
        ],
        (2, 2): [
            "narrateur|Sur le banc de bois, un livre jaune.",
            "enfant-m|Le livre, dans le sac, pour le camp.",
            "narrateur|Il pousse trop vite, trop fort.",
        ],
        (2, 3): [
            "narrateur|Près de l'arrosoir, une tasse jaune attend.",
            "enfant-m|La dînette, dans le sac, pour le camp.",
            "narrateur|Il saisit la tasse, trop vite.",
        ],
        (3, 1): [
            "narrateur|Sur le tapis, un cube jaune brille.",
            "enfant-m|Les cubes, dans le sac, pour le camp.",
            "narrateur|Il empile trop vite, trop haut.",
        ],
        (3, 2): [
            "narrateur|Près de l'oreiller, un livre jaune.",
            "enfant-m|Le livre, dans le sac, pour le camp.",
            "narrateur|Il pousse trop vite, trop fort.",
        ],
        (3, 3): [
            "narrateur|Sur le coffre, une tasse jaune attend.",
            "enfant-m|La dînette, dans le sac, pour le camp.",
            "narrateur|Il saisit la tasse, trop vite.",
        ],
    }[(b, c)]
    snag = {
        1: [
            "narrateur|La tour cache la boucle, et le sac fuit.",
            "enfant-m|Il est dessous !",
            "narrateur|Il écarte un cube, trop fort.",
        ],
        2: [
            "narrateur|Le livre cache la boucle, et le sac fuit.",
            "enfant-m|Il est dessous !",
            "narrateur|Il soulève le livre, trop fort.",
        ],
        3: [
            "narrateur|La tasse roule, et le sac fuit.",
            "enfant-m|Il est dessous !",
            "narrateur|Il lève la tasse, trop fort.",
        ],
    }[c]
    faux = {
        1: "narrateur|Le torchon jaune ment, une seconde.",
        2: "narrateur|Le gant jaune ment, une seconde.",
        3: "narrateur|Le coussin jaune ment, une seconde.",
    }[b]
    body = {
        1: [
            "narrateur|Dans sa poitrine, ça serre, fort.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu tires, ou tu regardes ?",
            "enfant-m|Je cherche, sans foncer.",
        ],
        2: [
            "narrateur|Ses épaules baissent, un peu.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu forces, ou tu regardes ?",
            "enfant-m|J'attends, je regarde.",
        ],
        3: [
            "narrateur|L'envie de tirer lui pique les doigts.",
            "narrateur|Papa s'accroupit, près de lui.",
            "papa|Tu vois la dent, où ?",
            "enfant-m|Je cherche, sans foncer.",
        ],
    }[c]
    listen = {
        1: "narrateur|Il écoute le carrelage, puis la boucle.",
        2: "narrateur|Il écoute le banc de bois, puis la boucle.",
        3: "narrateur|Il écoute le tapis, puis la boucle.",
    }[b]
    pay = "narrateur|La dent de laitue reparaît, collée."
    gesture = {
        1: "narrateur|Il ouvre le sac, cube par cube.",
        2: "narrateur|Il ouvre le sac, page après page.",
        3: "narrateur|Il ouvre le sac, tasse après tasse.",
    }[c]
    snack = {
        1: "narrateur|La pomme se cale, au fond.",
        2: "narrateur|Le pot se cale, au fond.",
        3: "narrateur|Le pain se cale, au fond.",
    }[a]
    adult = {
        1: "maman|Tu l'as, sans forcer.",
        2: "papa|Il est à toi, maintenant.",
        3: "maman|Tu l'as repris, Victorino.",
    }[c]
    traces = {
        (1, 1): "narrateur|Un cube a laissé une marque, au tissu.",
        (1, 2): "narrateur|Une page a senti la pomme, au fond.",
        (1, 3): "narrateur|Une tasse a un rond de pomme, minuscule.",
        (2, 1): "narrateur|Un cube a un rond froid, au fond.",
        (2, 2): "narrateur|Une page a une goutte, minuscule.",
        (2, 3): "narrateur|Une tasse garde le froid du pot.",
        (3, 1): "narrateur|Un cube sent le four, au fond.",
        (3, 2): "narrateur|Une page a une miette, unique.",
        (3, 3): "narrateur|Une tasse a une miette, au bord.",
    }[(a, c)]
    almost = {
        (1, 1, 1): "narrateur|Un cube cachait la dent, presque.",
        (1, 1, 2): "narrateur|Le livre serrait trop, une seconde.",
        (1, 1, 3): "narrateur|La tasse recouvrait la boucle, presque.",
        (1, 2, 1): "narrateur|L'herbe buvait la sangle, presque.",
        (1, 2, 2): "narrateur|Le livre tirait trop, une seconde.",
        (1, 2, 3): "narrateur|La tasse gardait la boucle, presque.",
        (1, 3, 1): "narrateur|Le coussin cachait le jaune, presque.",
        (1, 3, 2): "narrateur|Le livre trompait l'œil, une seconde.",
        (1, 3, 3): "narrateur|La tasse se refermait, presque.",
        (2, 1, 1): "narrateur|Un rond froid couvrait la dent, presque.",
        (2, 1, 2): "narrateur|Le pot glissait trop, une seconde.",
        (2, 1, 3): "narrateur|Le bord pliait la sangle, presque.",
        (2, 2, 1): "narrateur|Le gant mentait, une seconde de trop.",
        (2, 2, 2): "narrateur|Le pot versait trop, une seconde.",
        (2, 2, 3): "narrateur|Une goutte cachait la dent, presque.",
        (2, 3, 1): "narrateur|Le coussin prenait la place, presque.",
        (2, 3, 2): "narrateur|Le livre trompait l'œil, une seconde.",
        (2, 3, 3): "narrateur|Le drap collait trop, une seconde.",
        (3, 1, 1): "narrateur|Le papier tenait la boucle, presque.",
        (3, 1, 2): "narrateur|Une miette couvrait la dent, presque.",
        (3, 1, 3): "narrateur|Le torchon cachait la sangle, presque.",
        (3, 2, 1): "narrateur|Le pain pesait trop, une seconde.",
        (3, 2, 2): "narrateur|Le gant mentait, une seconde de trop.",
        (3, 2, 3): "narrateur|Le bec de zinc manquait le brin, presque.",
        (3, 3, 1): "narrateur|Le coussin mélangeait les jaunes, presque.",
        (3, 3, 2): "narrateur|Un dos jaune prenait la place, presque.",
        (3, 3, 3): "narrateur|L'odeur égarait la main, presque.",
    }[(a, b, c)]
    return (
        arrive
        + snag
        + [faux]
        + body
        + [listen, pay, gesture, snack, adult, traces, almost]
    )


def ending_lines(a: int, b: int, c: int) -> list[str]:
    food = FOOD[a]
    lieu = LIEU[b]
    jeu = JEU[c]
    firsts = {
        (1, 1, 1): "Le banc de bois craque moins, au loin.",
        (1, 1, 2): "Le torchon de maman sent le carrelage.",
        (1, 1, 3): "Papa pose une tasse près de l'évier.",
        (1, 2, 1): "Un cube roule dans l'herbe, puis s'arrête.",
        (1, 2, 2): "Le sac pose son ombre au bois.",
        (1, 2, 3): "La fenêtre de la cuisine a un peu de buée.",
        (1, 3, 1): "Un cube dépasse du seuil de la chambre.",
        (1, 3, 2): "Un fil du rideau pend près des clés.",
        (1, 3, 3): "Le coussin sent la pomme, au bois.",
        (2, 1, 1): "Un rond froid sèche sur la chaise, loin.",
        (2, 1, 2): "Le métal de l'évier se tait, loin.",
        (2, 1, 3): "Un pas sur le carrelage, puis plus.",
        (2, 2, 1): "Le sac penche, sous le banc de bois.",
        (2, 2, 2): "Le cri du râteau s'arrête.",
        (2, 2, 3): "Le bec de zinc reste loin.",
        (2, 3, 1): "Le pot froid dépasse du banc.",
        (2, 3, 2): "Le livre a vu le zinc, depuis le bois.",
        (2, 3, 3): "Un rayon a bougé, sur l'oreiller.",
        (3, 1, 1): "Le pain s'endort près de la porte.",
        (3, 1, 2): "Le papier ne fait plus de bruit.",
        (3, 1, 3): "L'arrosoir se tait, goutte après goutte.",
        (3, 2, 1): "Le sac pose son ombre sur l'herbe.",
        (3, 2, 2): "Le linge attend, près des pinces.",
        (3, 2, 3): "Les clés de papa restent dans la coupelle.",
        (3, 3, 1): "Près du seuil, le pain sent le four.",
        (3, 3, 2): "Une miette rentre dans le sac, unique.",
        (3, 3, 3): "Le seuil retrouve son froid, unique.",
    }
    lasts = {
        (1, 1, 1): "Un cube dort sur la dent de laitue.",
        (1, 1, 2): "Le torchon garde un fil de sangle, minuscule.",
        (1, 1, 3): "Un rond de pomme reste coincé dans la tasse.",
        (1, 2, 1): "La sangle du sac sèche, sous le banc.",
        (1, 2, 2): "Une feuille du banc s'endort au livre.",
        (1, 2, 3): "L'ombre du sac s'endort dans l'herbe.",
        (1, 3, 1): "Du tissu reste dans le cube, au chaud.",
        (1, 3, 2): "Près du rideau, un fil jaune pend.",
        (1, 3, 3): "Sur la boucle, une dent de laitue brille.",
        (2, 1, 1): "Un rond froid sèche, collé à la dent.",
        (2, 1, 2): "Loin du sac, l'évier se tait.",
        (2, 1, 3): "Sur le bois de la chaise, un pas s'éteint.",
        (2, 2, 1): "Sous le banc, le sac penche, plein.",
        (2, 2, 2): "Le râteau s'endort, loin du zinc.",
        (2, 2, 3): "Loin d'ici, le bec de zinc reste muet.",
        (2, 3, 1): "Près du lit, un cube froid veille.",
        (2, 3, 2): "Dans le livre, un peu de zinc froid.",
        (2, 3, 3): "Sur l'oreiller, le rayon a bougé.",
        (3, 1, 1): "Près de la chaise, le pain s'endort.",
        (3, 1, 2): "Loin de la dent, le papier se tait.",
        (3, 1, 3): "La tasse garde une miette, unique.",
        (3, 2, 1): "Sur l'herbe, l'ombre du sac dort.",
        (3, 2, 2): "Près du banc, le linge attend.",
        (3, 2, 3): "Dans la laitue, une goutte se tait.",
        (3, 3, 1): "Au chaud, le cube sent le four.",
        (3, 3, 2): "Dans le sac, une dent de laitue se tait.",
        (3, 3, 3): "Au banc, le bois ne craque plus.",
    }
    qs = {
        1: "papa|Quel moment tu gardes, sous la table ?",
        2: "maman|Quel moment tu gardes, sous le banc ?",
        3: "papa|Quel moment tu gardes, près du lit ?",
    }[b]
    ans = {
        (1, 1, 1): "enfant-m|Quand le cube a parlé, sous la table.",
        (1, 1, 2): "enfant-m|Quand j'ai ouvert, sans foncer.",
        (1, 1, 3): "enfant-m|Quand la tasse a dit non, d'abord.",
        (1, 2, 1): "enfant-m|Quand la dent a parlé, sous le bois.",
        (1, 2, 2): "enfant-m|Quand le gant a menti, une seconde.",
        (1, 2, 3): "enfant-m|Quand l'escargot n'était pas arrivé.",
        (1, 3, 1): "enfant-m|Quand le coussin a pris la place.",
        (1, 3, 2): "enfant-m|Quand le livre a caché la boucle.",
        (1, 3, 3): "enfant-m|Quand j'ai cherché, sans tirer.",
        (2, 1, 1): "enfant-m|Quand le froid a quitté ma main.",
        (2, 1, 2): "enfant-m|Quand le torchon a menti, trop jaune.",
        (2, 1, 3): "enfant-m|Quand la tasse a roulé, puis tenu.",
        (2, 2, 1): "enfant-m|Quand le gant a menti, sur le bois.",
        (2, 2, 2): "enfant-m|Quand la goutte a montré la dent.",
        (2, 2, 3): "enfant-m|Quand le zinc a gardé sa goutte.",
        (2, 3, 1): "enfant-m|Quand le coussin a menti, au lit.",
        (2, 3, 2): "enfant-m|Quand le livre a senti le froid.",
        (2, 3, 3): "enfant-m|Quand le drap a voulu garder le sac.",
        (3, 1, 1): "enfant-m|Quand le pain a cessé de s'envoler.",
        (3, 1, 2): "enfant-m|Quand la miette a montré le fond.",
        (3, 1, 3): "enfant-m|Quand le torchon a cessé de mentir.",
        (3, 2, 1): "enfant-m|Quand le pain a pesé, sans tomber.",
        (3, 2, 2): "enfant-m|Quand le gant a cessé de mentir.",
        (3, 2, 3): "enfant-m|Quand le bec de zinc a veillé.",
        (3, 3, 1): "enfant-m|Quand les jaunes se sont démêlés.",
        (3, 3, 2): "enfant-m|Quand le dos jaune a perdu.",
        (3, 3, 3): "enfant-m|Quand l'odeur a ramené ma main.",
    }[(a, b, c)]
    return [
        f"narrateur|{firsts[(a, b, c)]}",
        f"narrateur|Il a glissé {food['un']}, dans le sac.",
        f"narrateur|Le camp s'est tenu {lieu['ou']}.",
        f"narrateur|Il a choisi {jeu['lab']}, pour jouer.",
        "narrateur|Voilà le sac jaune, sur le banc de bois.",
        "narrateur|Sur la boucle, la dent de laitue tient.",
        "enfant-m|Il est rentré, avec sa trace.",
        qs,
        ans,
        "enfant-m|Je raconte le moment difficile, surtout.",
        f"narrateur|{lasts[(a, b, c)]}",
    ]


def ending_note(a: int, b: int, c: int) -> str:
    return (
        f"arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
        f"destinataire=enfant; sous_texte=trace_{FOOD[a]['short']}_{LIEU[b]['short']}_{JEU[c]['short']}; "
        f"tempo=posé; sourire=léger; respiration=ample"
    )


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "arrosoir,escargot,banc")
    put(
        "CHK_T0001_P0000",
        T1_CHOICE,
        "choice",
        "",
        {"fields": {
            "option_1_label": "une pomme",
            "option_2_label": "un yaourt",
            "option_3_label": "un morceau de pain",
        }},
    )

    for a in (1, 2, 3):
        put(
            f"CHK_T0001_P000{a}",
            T1[a],
            "action",
            FOOD[a]["sons"],
            {"emphasis": FOOD[a]["short"]},
        )
        put(
            f"CHK_T0001_P000{a}_Q0001",
            T1_Q[a],
            "clue",
            "",
            {"emphasis": "sac", "fields": Q_FIELDS[a]},
        )
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            FOOD[a]["sons"],
            {"emphasis": "sac"},
        )
        put(
            f"CHK_T0001_P000{a}_T0002_P0000",
            T2_CHOICE[a],
            "choice",
            "",
            {"fields": {
                "option_1_label": "la cuisine",
                "option_2_label": "le jardin",
                "option_3_label": "la chambre",
            }},
        )
        for b in (1, 2, 3):
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}",
                t2_lines(a, b),
                "obstacle",
                LIEU[b]["sons"],
                {"emphasis": LIEU[b]["short"]},
            )
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
                T3_CHOICE[b],
                "choice",
                "",
                {"fields": {
                    "option_1_label": "les cubes",
                    "option_2_label": "le livre",
                    "option_3_label": "la dînette",
                }},
            )
            for c in (1, 2, 3):
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(
                    base,
                    t3_lines(a, b, c),
                    "resolution",
                    JEU[c]["sons"],
                    {"emphasis": "dent de laitue"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "banc,jardin",
                    {"emphasis": "dent de laitue", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = sorted(set(out_chunks) - {c["chunk_id"] for c in src["chunks"]})
    if missing or extra:
        raise SystemExit(f"missing={missing[:12]} extra={extra[:12]}")

    ends = [out_chunks[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(ends) != 27 or len(set(ends)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(ends))}/{len(ends)}")

    lasts = []
    for c in src["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        last_n = [ln for ln in out_chunks[c["chunk_id"]]["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(last_n[-1])
        low = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in low or "bravo" in low or "bon travail" in low:
            raise SystemExit(f"fin mécanique: {last_n[-1]}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images {len(set(lasts))}/27")

    t3_only = [
        out_chunks[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage" and "T0003_P000" in c["chunk_id"] and "_F0001" not in c["chunk_id"]
        and not c["chunk_id"].endswith("T0003_P0000")
    ]
    if len(t3_only) != 27 or len(set(t3_only)) != 27:
        raise SystemExit(f"T3 distincts: {len(set(t3_only))}/{len(t3_only)}")

    t2_only = [
        out_chunks[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage" and "_T0002_P000" in c["chunk_id"] and "T0003" not in c["chunk_id"]
    ]
    if len(t2_only) != 9 or len(set(t2_only)) != 9:
        raise SystemExit(f"T2 distincts: {len(set(t2_only))}/{len(t2_only)}")

    blob = "\n".join(c["script"] for c in out_chunks.values()).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"en ce moment x{blob.count('en ce moment')}")
    if "dent de laitue" not in out_chunks["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit("indice absent de l'ouverture")
    for c in src["chunks"]:
        if c["kind"] == "passage_fin":
            if "dent de laitue" not in out_chunks[c["chunk_id"]]["text"].lower() and "dent de laitue" not in out_chunks[c["chunk_id"]]["script"].lower():
                # endings mention it in the shared line
                pass
        if c["kind"] == "passage" and "T0003_P000" in c["chunk_id"] and "_F0001" not in c["chunk_id"] and not c["chunk_id"].endswith("T0003_P0000"):
            if "dent de laitue" not in out_chunks[c["chunk_id"]]["text"].lower():
                raise SystemExit(f"indice non payé: {c['chunk_id']}")

    merged = dict(src)
    merged["fil_rouge"] = (
        "Le banc de bois craque sans personne : le sac jaune a glissé. "
        "Sur la boucle, une dent de laitue tient, froide, collée. Victorino "
        "veut ce sac pour le camp de la laitue, avec un goûter, avant que "
        "l'escargot touche le cœur vert. Il tire trop vite : le sac retombe, "
        "mou, vide. Papa s'accroupit. Pomme, yaourt ou pain : à la main, "
        "patatras ; dans le sac, ça tient. Cuisine, jardin ou chambre : un "
        "faux jaune ment, la dent dit vrai. Il refuse de foncer. Cubes, "
        "livre ou dînette, la boucle se cache, avance, s'arrête. Il ouvre "
        "sans forcer. La dent paie le début. Vingt-sept traces."
    )
    merged["title"] = TITLE
    merged["characters"] = "Victorino, papa, maman"
    merged["setting"] = "jardin, arrosoir, laitue, escargot, banc de bois"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    counts = [
        sum(words(out_chunks[i]["text"]) for i in path_ids(a, b, c))
        for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)
    ]
    if min(counts) < 550 or max(counts) > 700:
        raise SystemExit(f"chemin hors barre 550-700: min {min(counts)} max {max(counts)}")
    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in merged["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types "
        "de blocs et destinations techniques inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le banc de bois craque sans personne : le sac jaune a glissé. Sur "
        "la boucle, une dent de laitue tient, froide, collée. Victorino veut "
        "ce sac pour le camp de la laitue, avec un goûter, avant que "
        "l'escargot touche le cœur vert. Il tire trop vite : le sac retombe, "
        "mou, vide. Le sourire disparaît. Papa s'accroupit. Pomme, yaourt ou "
        "pain : à la main ça glisse ; dans le sac, ça tient. Cuisine, jardin "
        "ou chambre : un torchon, un gant ou un coussin jaune ment. Il refuse "
        "de foncer. Cubes, livre ou dînette, la boucle se cache. Il ouvre "
        "sans forcer. La dent et le banc paient le début. Le sac garde une "
        "trace.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin, arrosoir, laitue, escargot, banc de bois.\n"
        "- Désir : porter le sac jaune au camp de la laitue, avant l'escargot.\n"
        "- Objet : sac jaune (dent de laitue), plus pomme / yaourt / pain.\n"
        "- Indice unique : la dent de laitue, vue dès l'ouverture, payée au climax.\n"
        "- Urgence douce : l'escargot avance vers le cœur vert.\n"
        "- Imprévu 1 : le sac vide retombe ; le goûter glisse hors de la main.\n"
        "- Cue : le sac est là, sur le bois. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : un faux jaune ment ; la dent dit vrai.\n"
        "- Revers allongé : coincé, corps (envie et peur), refus de foncer, "
        "boucle qui avance puis s'arrête, geste neuf.\n"
        "- Résolution : ouvrir sans forcer, cubes / livre / dînette.\n"
        "- Retour : dent de laitue, banc de bois, 27 traces distinctes.\n\n"
        "## Corrections éditoriales\n\n"
        "- Ouverture inventée (le banc craque sans personne), pas un gabarit v2.\n"
        "- Le premier choix n'enlève pas le sac : le goûter entre dedans.\n"
        "- Revers allongé : coincé, corps, refus, second arrêt, geste lent.\n"
        "- Neuf disparitions distinctes, vingt-sept résolutions, vingt-sept fins.\n"
        "- Leçon AUT.AFF.001 vécue (glisser dans le sac), jamais dite.\n"
        "- Monde ≠ TREE-COL-002 banc de fer Amir, ≠ TREE-COL-023 banc pomme Mila, "
        "≠ TREE-COL-017 escargot boulangerie.\n"
        "- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Troupe D16 : Victorino, papa, maman.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js.\n\n"
        "## Direction vocale\n\n"
        "Impatience de Victorino au départ, petit découragement quand le sac "
        "retombe ou disparaît, fierté calme quand il ouvre sans forcer. "
        "L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, 27 fins textuellement distinctes\n"
        f"- 27 T3 distincts, 9 T2 distincts\n"
        f"- {min(counts)} à {max(counts)} mots par chemin, moyenne {sum(counts)//27}\n"
        "- `text` et `script` synchronisés\n"
        "- `text_ssml` et `text_xai_tags` enrichis\n"
        "- `notes` présentes sur les 86 chunks\n"
        "- N2 ≤ 15 mots/phrase\n"
        "- check() OK. Pas d'apply. Pas d'audio. Pas de git.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {len(merged['chunks'])} chunks  chemins {min(counts)}-{max(counts)}")


if __name__ == "__main__":
    build()
