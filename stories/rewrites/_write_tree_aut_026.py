#!/usr/bin/env python3
"""TREE-AUT-026 — Le cartable jaune de Sarah (F-NAR-019, N1, AUT.AFF.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-026"
N1 = LIMITS["N1"]
TITLE = "Le cartable jaune de Sarah"
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
    "peau d'orange",
    "marque fine",
    "ombre-flèche",
    "ombre en forme",
    "étoile brune",
    "fil pâle",
    "croissant",
    "virgule",
    "nœud raphia",
    "pois ivoire",
    "grain savon",
    "grain vanille",
    "pastille colle",
    "capuchon",
    "grain doré",
    "brin safran",
    "anneau",
    "clou tête",
    "grain d'ambre",
    "goutte de cire",
    "larme de bronze",
    "point de cire",
    "bracelet d'écorce",
    "boucle d'étain",
    "dent de laitue",
    "éclat de zinc",
    "éclat de thym",
    "lune d'étain",
    "grain de grenat",
    "grain d'indigo",
    "grain de brique",
    "éclat vert",
    "écaille",
    "vis verte",
    "cristal de sucre",
    "tom ",
    "léa",
    "sami",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de boucle",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=la_boucle_refuse_le_clic; "
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
            "destinataire=enfant; sous_texte=ton_choix_change_la_cour; "
            "tempo=suspendu; sourire=léger; respiration=pause_avant_choix"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="cartable",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=le_gouter_reste_dans_le_jaune; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="cartable",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; intensite=1; "
            "destinataire=enfant; sous_texte=elle_garde_le_jaune_avec_elle; "
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
            "destinataire=enfant; sous_texte=nina_veut_jouer_sarah_veut_fermer; "
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
            "intensite=2; destinataire=enfant; sous_texte=le_jeu_menace_la_boucle; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de boucle",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=elle_ferme_sans_taper; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de boucle",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=l_eclat_a_tenu_promesse; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "cartable",
    "accepted_examples": "sac | cartable | le sac | le cartable | dans le sac | dans le cartable | le goûter",
    "retry_prompt": "Dans le cartable jaune. Il est où ?",
}

LOC = {
    1: dict(name="le bac à sable", short="bac", sons="sable,cour"),
    2: dict(name="le toboggan", short="toboggan", sons="metal,glisse"),
    3: dict(name="les balançoires", short="balançoires", sons="chaine,bois"),
}
OBJ = {
    1: dict(name="le ballon", short="ballon", sons="ballon,rebond"),
    2: dict(name="le seau", short="seau", sons="seau,sable"),
    3: dict(name="le doudou", short="doudou", sons="tissu,doudou"),
}
TOOL = {
    1: dict(name="la craie", short="craie", sons="craie,herbe"),
    2: dict(name="le caillou", short="caillou", sons="caillou,herbe"),
    3: dict(name="la feuille", short="feuille", sons="feuille,herbe"),
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


OPENING = [
    "narrateur|Sur le bois, un soleil mince.",
    "narrateur|Sarah connaît l'escalier, marche par marche.",
    "narrateur|Un détail paraît neuf, sur le jaune.",
    "narrateur|Le cartable jaune attend, sur la marche.",
    "narrateur|Au rabat, un éclat de boucle brille.",
    "narrateur|Il est minuscule, contre le métal.",
    "narrateur|La cuisine sent le pain grillé.",
    "papa|Le pain attend, après l'école.",
    "maman|La cloche de la cour tinte, loin.",
    "narrateur|Nina serre le montant, trop pressée.",
    "copine|Moi, je descends, maintenant !",
    "enfant-f|Non, je ferme toute seule !",
    "narrateur|En ce moment, Sarah tape la boucle.",
    "narrateur|Elle tape trop fort, trop vite.",
    "narrateur|Le rabat rebondit, ouvert.",
    "narrateur|L'éclat de boucle disparaît, tordu.",
    "enfant-f|Elle ne veut pas fermer !",
    "narrateur|Le sourire de Sarah disparaît.",
    "narrateur|Ses épaules baissent, près du bois.",
    "narrateur|L'envie et l'inquiétude se bousculent.",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "papa|Tu fermes comment, la boucle ?",
    "maman|Tu le portes où, d'abord ?",
    "copine|On joue, vite, à l'école !",
    "enfant-f|Le jaune vient, je le porte.",
]

T1_CHOICE = [
    "narrateur|Le cartable jaune part avec elle.",
    "narrateur|La cour de l'école a trois coins.",
    "papa|Le bac à sable, le toboggan, ou les balançoires ?",
]

T1 = {
    1: [
        "narrateur|Sarah porte le jaune, deux mains.",
        "narrateur|Nina court vers le bac, trop vite.",
        "copine|Je creuse, maintenant !",
        "enfant-f|J'arrive, le cartable d'abord.",
        "narrateur|Le bac à sable sent l'eau.",
        "narrateur|Elle pose le jaune sur le bord.",
        "narrateur|Le rabat s'ouvre, trop vite.",
        "copine|Laisse, on joue !",
        "enfant-f|Non, je le garde.",
        "narrateur|Un château penche vers le tissu.",
        "narrateur|Du sable entre dans la boucle.",
        "enfant-f|Je n'y arrive pas.",
        "papa|Le goûter, vois, sous le rabat.",
        "maman|L'éclat de boucle s'est caché.",
        "narrateur|Ses épaules baissent, collées de grains.",
    ],
    2: [
        "narrateur|Sarah serre le jaune contre elle.",
        "narrateur|Nina grimpe les marches, trop vite.",
        "copine|Je glisse, maintenant !",
        "enfant-f|Le cartable reste, en bas.",
        "narrateur|Au toboggan, le métal est tiède.",
        "narrateur|Les marches font toc, sous les pieds.",
        "narrateur|Elle pose le jaune au pied.",
        "narrateur|Le rabat s'ouvre, un peu.",
        "copine|Monte, vite !",
        "enfant-f|Non, je le porte.",
        "narrateur|Le cartable penche, trop seul.",
        "enfant-f|Je n'y arrive pas.",
        "papa|Le goûter, vois, sous le rabat.",
        "maman|L'éclat de boucle s'est caché.",
        "narrateur|Ses épaules baissent, au bas.",
    ],
    3: [
        "narrateur|Sarah porte le jaune vers les chaînes.",
        "narrateur|Nina pousse un siège, trop vite.",
        "copine|Je me balance, maintenant !",
        "enfant-f|Le cartable va sous le banc.",
        "narrateur|La chaîne est rêche, un peu.",
        "narrateur|Le siège de bois balance, vide.",
        "narrateur|Elle glisse le jaune sous le banc.",
        "narrateur|Un vent lève le rabat, lent.",
        "copine|Pousse, vite !",
        "enfant-f|Non, je le garde.",
        "narrateur|Le tissu jaune attend, un peu ouvert.",
        "enfant-f|Je n'y arrive pas.",
        "papa|Le goûter, vois, sous le rabat.",
        "maman|L'éclat de boucle s'est caché.",
        "narrateur|Ses mains lâchent, un peu.",
    ],
}

T1_Q = {
    1: [
        "narrateur|Le château penche vers le cartable.",
        "papa|Sarah a mis le goûter où ?",
    ],
    2: [
        "narrateur|Le cartable est resté, en bas.",
        "maman|Le goûter de Sarah est où ?",
    ],
    3: [
        "narrateur|Le cartable attend sous le banc.",
        "papa|Sarah a mis le goûter où ?",
    ],
}

T1_C = {
    1: [
        "narrateur|Sarah soulève le rabat, sans forcer.",
        "narrateur|Le goûter est dedans, sous le papier.",
        "enfant-f|Il est dans le cartable.",
        "maman|Merci, le goûter est à l'abri.",
        "papa|Tu l'as gardé, avec toi.",
        "narrateur|L'éclat de boucle manque, un peu.",
        "enfant-f|Je le ferme, plus tard.",
        "copine|Alors on creuse, un peu.",
        "narrateur|Le jaune reste, près du bac.",
    ],
    2: [
        "narrateur|Sarah redescend, marche par marche.",
        "narrateur|Elle soulève le rabat, au pied.",
        "enfant-f|Il est dans le cartable.",
        "papa|Merci, le goûter est à l'abri.",
        "maman|Tu l'as gardé, avec toi.",
        "narrateur|L'éclat de boucle manque, un peu.",
        "enfant-f|Je le ferme, plus tard.",
        "copine|Alors on glisse, un peu.",
        "narrateur|Le jaune reste, au bas du métal.",
    ],
    3: [
        "narrateur|Sarah se penche sous le banc.",
        "narrateur|Elle soulève le rabat, sans forcer.",
        "enfant-f|Il est dans le cartable.",
        "maman|Merci, le goûter est à l'abri.",
        "papa|Tu l'as gardé, avec toi.",
        "narrateur|L'éclat de boucle manque, un peu.",
        "enfant-f|Je le ferme, plus tard.",
        "copine|Alors on pousse, un peu.",
        "narrateur|Le jaune reste, sous le bois.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Près du bac, un jeu l'appelle.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le cartable reste avec toi.",
    ],
    2: [
        "narrateur|Près du toboggan, un jeu l'appelle.",
        "maman|Le ballon, le seau, ou le doudou ?",
        "papa|Le cartable reste avec toi.",
    ],
    3: [
        "narrateur|Près des chaînes, un jeu l'appelle.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le cartable reste avec toi.",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    table = {
        (1, 1): [
            "narrateur|Sarah pose le jaune au bord du bac.",
            "narrateur|Nina prend le ballon, rouge, lisse.",
            "copine|Je tape, vers le château !",
            "enfant-f|Pas vers mon cartable.",
            "narrateur|Le ballon file, trop vif.",
            "narrateur|Il tape le rabat, ouvert.",
            "narrateur|Le papier du goûter craque, dedans.",
            "enfant-f|Il va tout casser !",
            "narrateur|Sarah court, puis s'arrête.",
            "copine|Relance, vite !",
            "enfant-f|J'attends, je regarde.",
            "papa|Regarde la boucle, pas le ballon.",
            "narrateur|L'éclat de boucle manque, sous le sable.",
            "maman|Il est là, minuscule, tordu.",
            "narrateur|Le ballon s'endort, loin du jaune.",
        ],
        (1, 2): [
            "narrateur|Sarah pose le jaune près du seau bleu.",
            "narrateur|Nina emplit le seau, trop vite.",
            "copine|Je verse, sur le château !",
            "enfant-f|Pas sur mon cartable.",
            "narrateur|Le seau penche, trop lourd.",
            "narrateur|Du sable mouillé touche le rabat.",
            "narrateur|La boucle boit, puis se tait.",
            "enfant-f|Elle est pleine, maintenant !",
            "narrateur|Sarah veut vider d'un coup.",
            "copine|Un seau de plus, vite !",
            "enfant-f|Je m'arrête, je vois.",
            "papa|Regarde la boucle, pas le seau.",
            "narrateur|L'éclat de boucle manque, sous le grain.",
            "maman|Il est là, minuscule, mouillé.",
            "narrateur|Le seau sonne, vide de jaune.",
        ],
        (1, 3): [
            "narrateur|Sarah pose le doudou gris, près du jaune.",
            "narrateur|Nina glisse l'oreille sous le rabat.",
            "copine|Il dort dans ton cartable !",
            "enfant-f|Non, le goûter est dedans.",
            "narrateur|Le doudou gonfle le rabat, trop.",
            "narrateur|La boucle ne peut plus joindre.",
            "narrateur|Sarah tire l'oreille, trop vite.",
            "enfant-f|Il ne veut pas sortir !",
            "copine|Laisse-le, il est bien.",
            "enfant-f|Pas trop vite, cette fois.",
            "papa|Regarde la boucle, pas l'oreille.",
            "narrateur|L'éclat de boucle manque, sous le poil.",
            "maman|Il est là, minuscule, caché.",
            "narrateur|Le doudou a du sable à l'oreille.",
            "narrateur|Le bac garde un creux, sans clic.",
        ],
        (2, 1): [
            "narrateur|Sarah pose le jaune sur une marche.",
            "narrateur|Nina prend le ballon, près du métal.",
            "copine|Il glisse, comme moi !",
            "enfant-f|Pas sur mon cartable.",
            "narrateur|Le ballon dévale, vif, trop loin.",
            "narrateur|Il heurte le jaune, au bas.",
            "narrateur|Le rabat s'ouvre, d'un coup.",
            "enfant-f|Il a tout bougé !",
            "narrateur|Sarah gravit, trop pressée, puis stop.",
            "copine|Relance du haut !",
            "enfant-f|Je reste, je vois.",
            "papa|Regarde la boucle, pas le ballon.",
            "narrateur|L'éclat de boucle manque, sur le métal.",
            "maman|Il est là, minuscule, tiède.",
            "narrateur|Le ballon s'arrête, loin du jaune.",
        ],
        (2, 2): [
            "narrateur|Sarah pose le jaune près des marches.",
            "narrateur|Nina emplit le seau bleu, au pied.",
            "copine|Je verse en haut, comme la pluie !",
            "enfant-f|Pas sur mon cartable.",
            "narrateur|L'eau du seau mouille la rampe.",
            "narrateur|Le jaune glisse, lourd, trop vite.",
            "narrateur|Le rabat s'ouvre, au bas.",
            "enfant-f|Il a bu, le pauvre !",
            "narrateur|Sarah veut courir, puis s'arrête.",
            "copine|De l'eau, de l'eau !",
            "enfant-f|Je ne cours pas, là.",
            "maman|Regarde la boucle, pas le seau.",
            "narrateur|L'éclat de boucle manque, sous la goutte.",
            "papa|Il est là, minuscule, mouillé.",
            "narrateur|Le seau goutte, sans clic dedans.",
        ],
        (2, 3): [
            "narrateur|Sarah pose le doudou contre le jaune.",
            "narrateur|Sur la marche, les deux dos se touchent.",
            "copine|Vous glissez avec moi, tous les deux.",
            "enfant-f|Le doudou, pas le cartable.",
            "narrateur|Nina pousse, le doudou sous le bras.",
            "narrateur|Le jaune reste, le rabat s'ouvre.",
            "narrateur|Au bas, un dos jaune attend, flou.",
            "enfant-f|C'est lui, ou l'ombre ?",
            "copine|On reprend, vite !",
            "enfant-f|J'attends, je regarde.",
            "papa|Regarde la boucle, pas le doudou.",
            "narrateur|L'éclat de boucle manque, sous l'oreille.",
            "maman|Il est là, minuscule, tiède.",
            "narrateur|Le doudou a une goutte, collée.",
            "narrateur|La rampe du toboggan reste nue.",
        ],
        (3, 1): [
            "narrateur|Sarah pose le jaune sous le banc.",
            "narrateur|Nina prend le ballon, près des chaînes.",
            "copine|Je lance, pendant que je pousse !",
            "enfant-f|Pas vers mon cartable.",
            "narrateur|Le ballon file, et le siège part.",
            "narrateur|Il roule sous le banc, trop près.",
            "narrateur|Le rabat s'ouvre, d'un souffle.",
            "enfant-f|Il va le coincer !",
            "narrateur|Sarah se baisse, puis s'arrête.",
            "copine|Relance, vite !",
            "enfant-f|Je me baisse, lente.",
            "maman|Regarde la boucle, pas le ballon.",
            "narrateur|L'éclat de boucle manque, sous le bois.",
            "papa|Il est là, minuscule, dans l'ombre.",
            "narrateur|Le ballon s'endort sous les chaînes.",
        ],
        (3, 2): [
            "narrateur|Sarah pose le jaune au pied de bois.",
            "narrateur|Nina emplit le seau bleu, près des chaînes.",
            "copine|Je fais un poids, pour le siège !",
            "enfant-f|Pas sur mon cartable.",
            "narrateur|Le seau pèse, et le siège part.",
            "narrateur|Du sable tombe sur le rabat.",
            "narrateur|La boucle se tait, trop pleine.",
            "enfant-f|Elle ne peut plus cliquer !",
            "narrateur|Sarah veut chasser le sable, trop vite.",
            "copine|Un seau de plus !",
            "enfant-f|Je souffle, je vois.",
            "papa|Regarde la boucle, pas le seau.",
            "narrateur|L'éclat de boucle manque, sous le grain.",
            "maman|Il est là, minuscule, poudreux.",
            "narrateur|Le seau sonne, contre le pied nu.",
        ],
        (3, 3): [
            "narrateur|Sarah pose le doudou sur le jaune.",
            "narrateur|Sous le banc, les deux dos se confondent.",
            "copine|Il se balance, lui aussi !",
            "enfant-f|Le doudou, pas le cartable.",
            "narrateur|Nina pousse, le doudou sous le bras.",
            "narrateur|Le jaune reste, le rabat s'ouvre.",
            "narrateur|Au retour, un dos jaune attend, flou.",
            "enfant-f|C'est lui, ou le doudou ?",
            "copine|On reprend, vite !",
            "enfant-f|Je reste, sans courir.",
            "maman|Regarde la boucle, pas le doudou.",
            "narrateur|L'éclat de boucle manque, sous l'oreille.",
            "papa|Il est là, minuscule, dans l'herbe.",
            "narrateur|Le doudou a l'odeur de l'herbe.",
            "narrateur|Le siège reste nu, sans clic.",
        ],
    }
    return table[(a, b)]


T3_CHOICE = {
    1: [
        "narrateur|Dans l'herbe, un petit objet attend.",
        "papa|La craie, le caillou, ou la feuille ?",
        "maman|Ça peut aider la boucle.",
    ],
    2: [
        "narrateur|Près du seau, l'herbe cache un objet.",
        "maman|La craie, le caillou, ou la feuille ?",
        "papa|Ça peut aider la boucle.",
    ],
    3: [
        "narrateur|Sous le doudou, l'herbe cache un objet.",
        "papa|La craie, le caillou, ou la feuille ?",
        "maman|Ça peut aider la boucle.",
    ],
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    found = {
        1: [
            "narrateur|Une craie jaune attend dans l'herbe.",
            "narrateur|Elle est un peu cassée, sèche.",
            "copine|Je dessine un soleil, vite !",
            "enfant-f|Attends, la boucle d'abord.",
        ],
        2: [
            "narrateur|Un caillou lisse brille, un peu chaud.",
            "narrateur|Il est rond, dans l'herbe.",
            "copine|Je le lance, loin !",
            "enfant-f|Attends, la boucle d'abord.",
        ],
        3: [
            "narrateur|Une feuille verte est tombée, nette.",
            "narrateur|Elle a des nervures, sous le doigt.",
            "copine|Je la fais voler, vite !",
            "enfant-f|Attends, la boucle d'abord.",
        ],
    }[c]
    place = {
        1: "narrateur|Sarah ramène l'objet vers le bac.",
        2: "narrateur|Sarah ramène l'objet vers le métal.",
        3: "narrateur|Sarah ramène l'objet vers le banc.",
    }[a]
    obj_line = {
        1: "narrateur|Le ballon reste à côté, sage.",
        2: "narrateur|Le seau bleu reste à côté, sage.",
        3: "narrateur|Le doudou reste à côté, sage.",
    }[b]
    ruse = {
        1: [
            "narrateur|Elle trace un trait, autour du trou.",
            "narrateur|La craie montre où presser, sans taper.",
            "enfant-f|Là, je vois le chemin.",
        ],
        2: [
            "narrateur|Elle cale le caillou sur le rabat.",
            "narrateur|Le poids tient, sans forcer.",
            "enfant-f|Tiens, toi, le temps d'un clic.",
        ],
        3: [
            "narrateur|Elle essuie le métal, avec la feuille.",
            "narrateur|La poussière part, lente.",
            "enfant-f|Je te vois, petite lumière.",
        ],
    }[c]
    gleam = {
        (1, 1): "narrateur|L'éclat de boucle revient, dans la poudre.",
        (1, 2): "narrateur|L'éclat de boucle revient, sous le grain.",
        (1, 3): "narrateur|L'éclat de boucle revient, au bord du bac.",
        (2, 1): "narrateur|L'éclat de boucle revient, sur le métal.",
        (2, 2): "narrateur|L'éclat de boucle revient, sous la goutte.",
        (2, 3): "narrateur|L'éclat de boucle revient, tiède, au bas.",
        (3, 1): "narrateur|L'éclat de boucle revient, sous le banc.",
        (3, 2): "narrateur|L'éclat de boucle revient, près des chaînes.",
        (3, 3): "narrateur|L'éclat de boucle revient, dans l'herbe.",
    }[(a, b)]
    click = [
        "narrateur|Sarah presse, lente, sans taper.",
        "narrateur|Ça fait tchac, net.",
        "enfant-f|Il est fermé, toute seule.",
        "papa|Tu l'as fait, sans foncer.",
        "narrateur|Elle porte le jaune, deux mains.",
        "copine|On peut jouer, maintenant.",
    ]
    almost = {
        (1, 1, 1): "narrateur|Le trait a failli rater le trou.",
        (1, 1, 2): "narrateur|Le caillou a failli rouler, trop.",
        (1, 1, 3): "narrateur|La feuille a failli se déchirer.",
        (1, 2, 1): "narrateur|Le sable a failli boire le trait.",
        (1, 2, 2): "narrateur|Le seau a failli chasser le caillou.",
        (1, 2, 3): "narrateur|Le grain a failli coller la feuille.",
        (1, 3, 1): "narrateur|L'oreille a failli cacher le trait.",
        (1, 3, 2): "narrateur|Le poil a failli pousser le caillou.",
        (1, 3, 3): "narrateur|Le doudou a failli prendre la feuille.",
        (2, 1, 1): "narrateur|Le métal a failli glisser le trait.",
        (2, 1, 2): "narrateur|La marche a failli jeter le caillou.",
        (2, 1, 3): "narrateur|Le vent a failli voler la feuille.",
        (2, 2, 1): "narrateur|L'eau a failli laver le trait.",
        (2, 2, 2): "narrateur|La goutte a failli noyer le caillou.",
        (2, 2, 3): "narrateur|La rampe a failli coller la feuille.",
        (2, 3, 1): "narrateur|L'ombre a failli cacher le trait.",
        (2, 3, 2): "narrateur|Le doudou a failli bouger le caillou.",
        (2, 3, 3): "narrateur|La marche a failli plier la feuille.",
        (3, 1, 1): "narrateur|La chaîne a failli cacher le trait.",
        (3, 1, 2): "narrateur|Le siège a failli chasser le caillou.",
        (3, 1, 3): "narrateur|Le vent a failli emporter la feuille.",
        (3, 2, 1): "narrateur|Le sable a failli noyer le trait.",
        (3, 2, 2): "narrateur|Le pied nu a failli bouger le caillou.",
        (3, 2, 3): "narrateur|La chaîne a failli déchirer la feuille.",
        (3, 3, 1): "narrateur|L'herbe a failli cacher le trait.",
        (3, 3, 2): "narrateur|L'oreille a failli couvrir le caillou.",
        (3, 3, 3): "narrateur|Le banc a failli pincer la feuille.",
    }[(a, b, c)]
    traces = {
        (1, 1, 1): "narrateur|Un trait de craie dort sur la boucle.",
        (1, 1, 2): "narrateur|Le caillou garde un grain, collé.",
        (1, 1, 3): "narrateur|Une nervure reste au rabat, sèche.",
        (1, 2, 1): "narrateur|La craie a du sable, au bout.",
        (1, 2, 2): "narrateur|Le caillou est mouillé, un peu.",
        (1, 2, 3): "narrateur|La feuille sent le seau bleu.",
        (1, 3, 1): "narrateur|La craie a un poil, minuscule.",
        (1, 3, 2): "narrateur|Le caillou a chaud, près de l'oreille.",
        (1, 3, 3): "narrateur|La feuille reste dans le poil gris.",
        (2, 1, 1): "narrateur|Un trait de craie sèche, sur le métal.",
        (2, 1, 2): "narrateur|Le caillou est tiède, comme la rampe.",
        (2, 1, 3): "narrateur|La feuille a un toc, du métal.",
        (2, 2, 1): "narrateur|La craie a une goutte, au milieu.",
        (2, 2, 2): "narrateur|Le caillou brille, mouillé, au bas.",
        (2, 2, 3): "narrateur|La feuille ondule, un peu humide.",
        (2, 3, 1): "narrateur|La craie a l'odeur du doudou.",
        (2, 3, 2): "narrateur|Le caillou a une ombre de poil.",
        (2, 3, 3): "narrateur|La feuille reste collée à l'oreille.",
        (3, 1, 1): "narrateur|Un trait de craie dort sous le banc.",
        (3, 1, 2): "narrateur|Le caillou a l'ombre des chaînes.",
        (3, 1, 3): "narrateur|La feuille tremble, près du siège.",
        (3, 2, 1): "narrateur|La craie a du grain, sous le bois.",
        (3, 2, 2): "narrateur|Le caillou sonne, contre le pied.",
        (3, 2, 3): "narrateur|La feuille sent le seau, et l'herbe.",
        (3, 3, 1): "narrateur|La craie a un poil d'oreille, gris.",
        (3, 3, 2): "narrateur|Le caillou reste au chaud, sous le banc.",
        (3, 3, 3): "narrateur|La feuille a l'odeur de l'herbe.",
    }[(a, b, c)]
    return found + [place, obj_line] + ruse + [gleam] + click + [almost, traces]


def ending_lines(a: int, b: int, c: int) -> list[str]:
    firsts = {
        (1, 1, 1): "Le bac garde un château, un peu penché.",
        (1, 1, 2): "Le sable tient un rond, chaud.",
        (1, 1, 3): "Une nervure sèche, au bord du bac.",
        (1, 2, 1): "Le seau bleu penche, vide, sage.",
        (1, 2, 2): "Une goutte de sable sèche, au bord.",
        (1, 2, 3): "Le château sent l'eau, un peu.",
        (1, 3, 1): "L'oreille du doudou dépasse du bac.",
        (1, 3, 2): "Un poil gris reste au sable.",
        (1, 3, 3): "Le doudou a l'odeur du grain.",
        (2, 1, 1): "Le métal du toboggan se tait, loin.",
        (2, 1, 2): "Un toc s'éteint, sur une marche.",
        (2, 1, 3): "Le ballon s'endort, au bas du métal.",
        (2, 2, 1): "Le seau goutte, loin de la rampe.",
        (2, 2, 2): "Une goutte sèche, sur le métal.",
        (2, 2, 3): "La rampe reste nue, tiède.",
        (2, 3, 1): "L'oreille molle dépasse du bas.",
        (2, 3, 2): "Le doudou a vu le métal, depuis le bois.",
        (2, 3, 3): "Une ombre de poil reste au bas.",
        (3, 1, 1): "La chaîne ne fait plus cling.",
        (3, 1, 2): "Le siège de bois s'endort, vide.",
        (3, 1, 3): "Le ballon s'endort sous les chaînes.",
        (3, 2, 1): "Le seau pose son ombre au pied.",
        (3, 2, 2): "Un grain reste collé à la chaîne.",
        (3, 2, 3): "Le pied nu a quitté le sable.",
        (3, 3, 1): "Le doudou a l'odeur de l'herbe.",
        (3, 3, 2): "Une oreille molle veille, sous le banc.",
        (3, 3, 3): "Le banc retrouve son ombre, unique.",
    }
    lasts = {
        (1, 1, 1): "Un trait de craie dort sur l'éclat de boucle.",
        (1, 1, 2): "Le caillou tiède veille près de l'éclat de boucle.",
        (1, 1, 3): "Une nervure sèche, collée à l'éclat de boucle.",
        (1, 2, 1): "La craie sablée touche l'éclat de boucle.",
        (1, 2, 2): "Le caillou mouillé garde l'éclat de boucle.",
        (1, 2, 3): "La feuille humide ombre l'éclat de boucle.",
        (1, 3, 1): "Un poil gris frôle l'éclat de boucle.",
        (1, 3, 2): "Le caillou chaud réchauffe l'éclat de boucle.",
        (1, 3, 3): "La feuille du poil cache l'éclat de boucle.",
        (2, 1, 1): "Le trait de craie luit sur l'éclat de boucle.",
        (2, 1, 2): "Le caillou tiède répond à l'éclat de boucle.",
        (2, 1, 3): "La feuille au toc garde l'éclat de boucle.",
        (2, 2, 1): "Une goutte de craie luit sur l'éclat de boucle.",
        (2, 2, 2): "Le caillou mouillé reflète l'éclat de boucle.",
        (2, 2, 3): "La feuille ondule, contre l'éclat de boucle.",
        (2, 3, 1): "La craie du doudou frôle l'éclat de boucle.",
        (2, 3, 2): "Le caillou à l'ombre tient l'éclat de boucle.",
        (2, 3, 3): "La feuille à l'oreille cache l'éclat de boucle.",
        (3, 1, 1): "Le trait sous le banc luit, éclat de boucle.",
        (3, 1, 2): "Le caillou des chaînes veille l'éclat de boucle.",
        (3, 1, 3): "La feuille tremble, près de l'éclat de boucle.",
        (3, 2, 1): "La craie au grain touche l'éclat de boucle.",
        (3, 2, 2): "Le caillou sonne, et l'éclat de boucle répond.",
        (3, 2, 3): "La feuille du seau ombre l'éclat de boucle.",
        (3, 3, 1): "La craie au poil dort sur l'éclat de boucle.",
        (3, 3, 2): "Le caillou au chaud garde l'éclat de boucle.",
        (3, 3, 3): "La feuille sent l'herbe, contre l'éclat de boucle.",
    }
    qs = {
        1: "papa|Tu as fermé comment, au bac ?",
        2: "maman|Tu as fermé comment, au métal ?",
        3: "papa|Tu as fermé comment, sous le banc ?",
    }[a]
    ans = {
        1: "enfant-f|Sans taper, avec la craie.",
        2: "enfant-f|Sans taper, avec le caillou.",
        3: "enfant-f|Sans taper, avec la feuille.",
    }[c]
    joue = {
        1: "Sarah a joué au bac.",
        2: "Sarah a joué au toboggan.",
        3: "Sarah a joué aux chaînes.",
    }[a]
    obj = OBJ[b]["name"]
    tool = TOOL[c]["name"]
    return [
        f"narrateur|{firsts[(a, b, c)]}",
        f"narrateur|{joue}",
        f"narrateur|Elle a choisi {obj}, pour le jeu.",
        f"narrateur|{tool.capitalize()} l'a menée vers le clic.",
        "narrateur|Voilà le cartable jaune, fermé.",
        "narrateur|Au rabat, l'éclat de boucle brille.",
        "enfant-f|Il est fermé, avec sa trace.",
        qs,
        ans,
        "maman|Le pain nous attend, maintenant.",
        "enfant-f|Je le porte, jusqu'à l'escalier.",
        f"narrateur|{lasts[(a, b, c)]}",
    ]


def ending_note(a: int, b: int, c: int) -> str:
    return (
        f"arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
        f"destinataire=enfant; sous_texte=eclat_{LOC[a]['short']}_{OBJ[b]['short']}_{TOOL[c]['short']}; "
        f"tempo=posé; sourire=léger; respiration=ample"
    )


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "escalier,pain,cartable")
    put(
        "CHK_T0001_P0000",
        T1_CHOICE,
        "choice",
        "",
        {"fields": {
            "option_1_label": "le bac à sable",
            "option_2_label": "le toboggan",
            "option_3_label": "les balançoires",
        }},
    )

    for a in (1, 2, 3):
        put(
            f"CHK_T0001_P000{a}",
            T1[a],
            "action",
            LOC[a]["sons"],
            {"emphasis": LOC[a]["short"]},
        )
        put(
            f"CHK_T0001_P000{a}_Q0001",
            T1_Q[a],
            "clue",
            "",
            {"emphasis": "cartable", "fields": Q_FIELDS},
        )
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            LOC[a]["sons"],
            {"emphasis": "cartable"},
        )
        put(
            f"CHK_T0001_P000{a}_T0002_P0000",
            T2_CHOICE[a],
            "choice",
            "",
            {"fields": {
                "option_1_label": "le ballon",
                "option_2_label": "le seau",
                "option_3_label": "le doudou",
            }},
        )
        for b in (1, 2, 3):
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}",
                t2_lines(a, b),
                "obstacle",
                OBJ[b]["sons"],
                {"emphasis": OBJ[b]["short"]},
            )
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
                T3_CHOICE[b],
                "choice",
                "",
                {"fields": {
                    "option_1_label": "la craie",
                    "option_2_label": "le caillou",
                    "option_3_label": "la feuille",
                }},
            )
            for c in (1, 2, 3):
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(
                    base,
                    t3_lines(a, b, c),
                    "resolution",
                    TOOL[c]["sons"],
                    {"emphasis": "éclat de boucle"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "escalier,pain,boucle",
                    {"emphasis": "éclat de boucle", "note": ending_note(a, b, c)},
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

    merged = dict(src)
    merged["fil_rouge"] = (
        "Sur l'escalier, un éclat de boucle brille au rabat du cartable jaune. "
        "Sarah veut fermer seule et descendre, avant la cour. Nina veut courir "
        "tout de suite. Sarah tape trop vite : le rabat rebondit, l'éclat "
        "disparaît. À l'école, bac, toboggan ou balançoires, le jaune reste "
        "avec elle, trop ouvert. Ballon, seau ou doudou : Nina joue, Sarah "
        "refuse de foncer. Craie, caillou ou feuille : elle observe, presse "
        "sans taper. L'éclat de boucle paie le début. Vingt-sept traces."
    )
    merged["title"] = TITLE
    merged["characters"] = "Sarah, Nina, papa, maman"
    merged["setting"] = "escalier de la maison, puis cour de l'école"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    counts = [
        sum(words(out_chunks[i]["text"]) for i in path_ids(a, b, c))
        for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)
    ]
    if min(counts) < 520 or max(counts) > 760:
        raise SystemExit(f"chemin hors barre: min {min(counts)} max {max(counts)}")
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
        "Sur le bois, un soleil mince. Sarah connaît l'escalier, mais un détail "
        "paraît neuf : au rabat du cartable jaune, un éclat de boucle brille. "
        "Elle veut fermer seule et descendre, avant la cour. Nina, trop pressée, "
        "veut courir maintenant. Sarah tape trop fort : le rabat rebondit, "
        "l'éclat disparaît, le sourire part. Papa s'accroupit. À l'école, bac, "
        "toboggan ou balançoires, le jaune reste avec elle, trop ouvert. Ballon, "
        "seau ou doudou : Nina joue, Sarah refuse de foncer. Craie, caillou ou "
        "feuille : elle observe, presse sans taper. L'éclat de boucle revient. "
        "Le clic a failli. Elle porte le jaune jusqu'à l'escalier.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : escalier de la maison, pain grillé, cloche de la cour.\n"
        "- Désir : fermer seule le cartable jaune et descendre, maintenant.\n"
        "- Objet : cartable jaune (éclat de boucle), plus ballon / seau bleu / doudou.\n"
        "- Indice unique : l'éclat de boucle, vu dès l'ouverture, payé au climax.\n"
        "- Imprévu : Nina ne veut pas la même chose ; la boucle résiste au tap.\n"
        "- 2e ruse : craie / caillou / feuille, sans foncer.\n"
        "- Retour : le clic, la trace, l'éclat.\n\n"
        "## Leçon vécue\n\n"
        "AUT.AFF.001 — porter, fermer, partir seule. Jamais dite. Nina veut "
        "jouer tout de suite ; Sarah garde le jaune, échoue, observe, ferme.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks, 27 fins distinctes, chemins {min(counts)}–{max(counts)} mots\n"
        "- N1 ≤ 10. `en ce moment`. Merci vécu. Question d'adulte.\n"
        "- Pas encore / déjà / tout doux. Pas Tom/Léa/Sami. Seau bleu, pas jaune.\n"
        "- Cour d'école, pas gare. Cartable reste au T1.\n\n"
        "## Vu et corrigé\n\n"
        "Dump gabarit (froid, peau d'orange, 72 % tics) jeté. Pair D16 : Nina. "
        "Indice unique : éclat de boucle. TTS notes+ssml+xai+piper.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"OK {SID} chemins {min(counts)}-{max(counts)} mots  1re: {OPENING[0].split('|',1)[1]}")


if __name__ == "__main__":
    build()
