#!/usr/bin/env python3
"""TREE-AUT-045 — Le panier d'osier de Nina au marché (F-NAR-019, N1)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-045"
N1 = LIMITS["N1"]
TITLE = "Le panier d'osier de Nina au marché"
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
    "virgule de farine",
    "virgule farine",
    "œillet de cuivre",
    "bouton de nacre",
    "nœud de raphia",
    "pois ivoire",
    "grain de savon",
    "grain savon",
    "grain de vanille",
    "pastille de colle",
    "virgule de buée",
    "capuchon",
    "grain doré",
    "brin de safran",
    "anneau de liège",
    "clou à tête",
    "grain d'ambre",
    "goutte de cire",
    "anneau de zinc",
    "larme de bronze",
    "point de cire",
    "bracelet d'écorce",
    "boucle d'étain",
    "anneau de pollen",
    "dent de laitue",
    "éclat de zinc",
    "éclat de thym",
    "lune d'étain",
    "grain de grenat",
    "grain d'indigo",
    "grain de brique",
    "éclat vert",
    "écaille d'étain",
    "vis verte",
    "cristal de sucre",
    "écaille de lichen",
    "grain de cire",
    "dent de fermeture",
    "écaille de nacre",
    "croissant d'eau",
    "croissant pâle",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de paprika",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=panier_coincé_au_clou; "
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
        emphasis="panier",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=la_nourriture_voyage_dans_le_panier; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="panier",
        note=(
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=l_osier_pèse_un_peu; "
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
            "destinataire=enfant; sous_texte=la_main_lâche_la_nourriture; "
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
            "intensite=2; destinataire=enfant; sous_texte=le_jeu_ment_l_osier_dit_vrai; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grain de paprika",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=elle_regarde_sans_foncer; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de paprika",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=le_grain_et_l_osier_paient_le_début; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

FOOD = {
    1: dict(lab="une pomme", le="la pomme", un="une pomme", short="pomme", sons="pomme"),
    2: dict(lab="un yaourt", le="le yaourt", un="un yaourt", short="yaourt", sons="pot"),
    3: dict(lab="un morceau de pain", le="le pain", un="un morceau de pain", short="pain", sons="pain"),
}
TOY = {
    1: dict(lab="le ballon", un="un ballon", le="le ballon", short="ballon", sons="ballon"),
    2: dict(lab="le seau", un="un seau", le="le seau", short="seau", sons="seau"),
    3: dict(lab="le doudou", un="le doudou", le="le doudou", short="doudou", sons="tissu"),
}
COLOR = {
    1: dict(lab="le rouge", ou="sous la nappe rouge", short="rouge", sons="fraise,marche"),
    2: dict(lab="le bleu", ou="près de la caisse bleue", short="bleu", sons="volet,caisse"),
    3: dict(lab="le vert", ou="sous la toile verte", short="vert", sons="feuilles,marche"),
}

Q_FIELDS = {
    1: {
        "expected_answer": "panier",
        "accepted_examples": "panier | le panier | dans le panier | au panier | le panier d'osier",
        "retry_prompt": "Dans le panier d'osier. Elle l'a mis où ?",
    },
    2: {
        "expected_answer": "panier",
        "accepted_examples": "panier | le panier | dans le panier | au panier | le panier d'osier",
        "retry_prompt": "Dans le panier d'osier. Elle l'a mis où ?",
    },
    3: {
        "expected_answer": "panier",
        "accepted_examples": "panier | le panier | dans le panier | au panier | le panier d'osier",
        "retry_prompt": "Dans le panier d'osier. Elle l'a mis où ?",
    },
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


# Ouverture : l'osier d'abord, un grain de paprika. Pavés mouillés sans « encore ».
OPENING = [
    "narrateur|Un grain de paprika tient dans l'osier.",
    "narrateur|Il pique un peu, tout petit.",
    "narrateur|Dehors, les pavés luisent, mouillés.",
    "narrateur|Ça sent le pain, sous le volet.",
    "narrateur|Le volet du boulanger claque une fois.",
    "narrateur|Nina connaît ce clou, près de la porte.",
    "narrateur|Le grain rouge, lui, paraît nouveau.",
    "narrateur|Papa noue son foulard gris.",
    "narrateur|Maman plie un torchon à carreaux.",
    "maman|Tu entends le marché, Nina ?",
    "enfant-f|Le panier, vite !",
    "narrateur|En ce moment, Nina tire l'osier.",
    "narrateur|Le panier résiste, coincé au clou.",
    "enfant-f|Il ne vient pas !",
    "narrateur|Le sourire de Nina disparaît.",
    "narrateur|Dans sa poitrine, ça serre, fort.",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "papa|Le clou le tient, tu vois ?",
    "enfant-f|Je le veux, pour les fraises !",
    "maman|On le décroche, puis on part ?",
    "narrateur|Nina lâche, puis reprend, plus lent.",
    "narrateur|L'osier se défait du clou.",
    "enfant-f|Il est à moi, on y va !",
]

T1_CHOICE = [
    "narrateur|Le panier d'osier vient avec nous.",
    "papa|Au marché, tu glisses quoi d'abord ?",
    "maman|Une pomme, un yaourt, ou un morceau de pain ?",
]

T1 = {
    1: [
        "narrateur|Nina saisit la pomme, trop vite.",
        "narrateur|Elle est lisse, froide de l'étal.",
        "enfant-f|Je la porte, moi !",
        "papa|À la main, jusqu'à la maison ?",
        "narrateur|La pomme glisse entre ses doigts.",
        "enfant-f|Elle tombe !",
        "narrateur|Le sourire de Nina disparaît.",
        "narrateur|Dans sa poitrine, ça serre, fort.",
        "narrateur|Maman s'accroupit, près des pavés.",
        "maman|Le panier est là, Nina.",
        "narrateur|Nina ouvre le panier d'osier.",
        "narrateur|Elle glisse la pomme au fond.",
        "narrateur|La pomme fait un petit choc.",
        "enfant-f|Elle est dedans, à l'abri.",
        "narrateur|Sur l'osier, le grain de paprika tient.",
        "papa|Elle voyage avec toi ?",
    ],
    2: [
        "narrateur|Nina saisit le yaourt, trop vite.",
        "narrateur|Le pot est froid, lisse, blanc.",
        "enfant-f|Je le serre, moi !",
        "maman|À la main, jusqu'à la maison ?",
        "narrateur|Le pot glisse, et tape un pavé.",
        "enfant-f|Il va rouler !",
        "narrateur|Le sourire de Nina disparaît.",
        "narrateur|Ses épaules baissent, près de l'étal.",
        "narrateur|Papa s'accroupit, à sa hauteur.",
        "papa|Le panier est là, Nina.",
        "narrateur|Nina ouvre le panier d'osier.",
        "narrateur|Elle glisse le pot au fond.",
        "narrateur|Le pot fait un petit toc.",
        "enfant-f|Il est dedans, au frais.",
        "narrateur|Sur l'osier, le grain de paprika tient.",
        "maman|Il voyage au froid ?",
    ],
    3: [
        "narrateur|Nina saisit le pain, trop vite.",
        "narrateur|Le papier blanc veut s'envoler.",
        "enfant-f|Je le porte, moi !",
        "papa|Le vent le prend, à la main ?",
        "narrateur|Un coin de papier file, vers le volet.",
        "enfant-f|Il part !",
        "narrateur|Le sourire de Nina disparaît.",
        "narrateur|L'envie et l'inquiétude se bousculent.",
        "narrateur|Maman s'accroupit, près du fournil.",
        "maman|Le panier est là, Nina.",
        "narrateur|Nina ouvre le panier d'osier.",
        "narrateur|Le papier froisse, au fond.",
        "narrateur|Le pain disparaît, à l'abri.",
        "enfant-f|Il est dedans, au chaud.",
        "narrateur|Sur l'osier, le grain de paprika tient.",
        "papa|Il sent le four, là ?",
    ],
}

T1_Q = {
    1: [
        "narrateur|La pomme a quitté sa main.",
        "papa|Nina l'a mise où ?",
    ],
    2: [
        "narrateur|Le pot froid a quitté sa main.",
        "maman|Nina l'a mis où ?",
    ],
    3: [
        "narrateur|Le pain a quitté sa main.",
        "papa|Nina l'a mis où ?",
    ],
}

T1_C = {
    1: [
        "narrateur|La pomme n'est plus dans sa main.",
        "enfant-f|Elle voyage, dans le panier.",
        "maman|Merci, Nina, tu l'as glissée.",
        "papa|Le jeu, on le choisit où ?",
        "enfant-f|Près des étals, avant le volet.",
        "narrateur|L'osier pèse, un peu, au bras.",
        "narrateur|Le grain de paprika reste collé.",
        "narrateur|Une goutte de fraise tache un pavé.",
    ],
    2: [
        "narrateur|Le pot n'est plus dans sa main.",
        "enfant-f|Il voyage, dans le panier.",
        "papa|Merci, Nina, tu l'as glissé.",
        "maman|Le jeu, on le choisit où ?",
        "enfant-f|Près des étals, avant le volet.",
        "narrateur|L'osier pèse, un peu, au bras.",
        "narrateur|Le grain de paprika reste collé.",
        "narrateur|Une goutte de fraise tache un pavé.",
    ],
    3: [
        "narrateur|Le pain n'est plus dans sa main.",
        "enfant-f|Il voyage, dans le panier.",
        "maman|Merci, Nina, tu l'as glissé.",
        "papa|Le jeu, on le choisit où ?",
        "enfant-f|Près des étals, avant le volet.",
        "narrateur|L'osier pèse, un peu, au bras.",
        "narrateur|Le grain de paprika reste collé.",
        "narrateur|Une miette reste, près du volet.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Un jeu veut entrer, près de la pomme.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le panier vient avec toi.",
    ],
    2: [
        "narrateur|Un jeu veut entrer, près du pot.",
        "maman|Le ballon, le seau, ou le doudou ?",
        "papa|Le panier vient avec toi.",
    ],
    3: [
        "narrateur|Un jeu veut entrer, près du pain.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le panier vient avec toi.",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    table = {
        (1, 1): [
            "narrateur|Nina porte le panier vers les étals.",
            "narrateur|Les pavés luisent, froids sous les pas.",
            "enfant-f|Le ballon, avec la pomme !",
            "narrateur|Près des fraises, un ballon rond attend.",
            "narrateur|Il est rouge, lisse, presque un fruit.",
            "enfant-f|Je prends tout, d'un coup.",
            "narrateur|Elle serre ballon et pomme, trop vite.",
            "narrateur|Le panier penche, l'osier crisse.",
            "narrateur|Le ballon rebondit, la pomme roule.",
            "enfant-f|Ils partent !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, ça serre, fort.",
            "narrateur|Papa s'accroupit, près des pavés.",
            "papa|Personne ne dit où courir.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Sur l'osier, le grain de paprika tient.",
        ],
        (1, 2): [
            "narrateur|Nina pose le panier près d'un seau.",
            "narrateur|L'anse du seau est froide, lisse.",
            "enfant-f|Le seau, pour tout porter !",
            "narrateur|Le seau est large, plus que l'osier.",
            "enfant-f|La pomme, dans le seau.",
            "narrateur|Elle bascule le panier, trop vite.",
            "narrateur|La pomme roule au fond du seau.",
            "enfant-f|Le panier est vide !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Ses épaules baissent, près des pavés.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Personne ne donne la réponse.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le seau n'est pas le panier.",
            "papa|Tu vois l'osier, Nina ?",
            "narrateur|Le grain de paprika pique, minuscule.",
        ],
        (1, 3): [
            "narrateur|Nina serre le panier contre elle.",
            "narrateur|Au clou d'un étal, un doudou pend.",
            "enfant-f|Mon doudou !",
            "narrateur|Il pend, comme le panier à la maison.",
            "enfant-f|Je le prends, et la pomme.",
            "narrateur|Elle tire le doudou, trop vite.",
            "narrateur|Le panier s'accroche, l'osier crisse.",
            "enfant-f|Il reste coincé !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "narrateur|Papa s'accroupit, près du clou.",
            "papa|Personne ne dit où tirer.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le doudou n'est pas le panier.",
            "maman|Tu vois le grain, Nina ?",
            "narrateur|Le grain de paprika reste collé.",
        ],
        (2, 1): [
            "narrateur|Nina porte le panier vers les étals.",
            "narrateur|Les pavés luisent, froids sous les pas.",
            "enfant-f|Le ballon, avec le yaourt !",
            "narrateur|Près des fraises, un ballon rond attend.",
            "narrateur|Il est blanc, lisse, presque le pot.",
            "enfant-f|Je prends tout, d'un coup.",
            "narrateur|Elle serre ballon et pot, trop vite.",
            "narrateur|Le panier penche, l'osier crisse.",
            "narrateur|Le ballon rebondit, le pot roule.",
            "enfant-f|Le froid part !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Ses épaules baissent, près des pavés.",
            "narrateur|Maman s'accroupit, près des pavés.",
            "maman|Personne ne dit où courir.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Sur l'osier, le grain de paprika tient.",
        ],
        (2, 2): [
            "narrateur|Nina pose le panier près d'un seau.",
            "narrateur|L'anse du seau est froide, lisse.",
            "enfant-f|Le seau, pour le pot !",
            "narrateur|Le seau est large, plus que l'osier.",
            "enfant-f|Le yaourt, dans le seau.",
            "narrateur|Elle bascule le panier, trop vite.",
            "narrateur|Le pot roule au fond du seau.",
            "enfant-f|Le pot a disparu !",
            "narrateur|Ses épaules baissent, près des pavés.",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Personne ne donne la réponse.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le seau n'est pas le panier.",
            "maman|Tu vois l'osier, Nina ?",
            "narrateur|Le grain de paprika pique, minuscule.",
        ],
        (2, 3): [
            "narrateur|Nina serre le panier contre elle.",
            "narrateur|Au clou d'un étal, un doudou pend.",
            "enfant-f|Mon doudou !",
            "narrateur|Il pend, comme le panier à la maison.",
            "enfant-f|Je le prends, et le pot.",
            "narrateur|Elle tire le doudou, trop vite.",
            "narrateur|Le panier s'accroche, l'osier crisse.",
            "enfant-f|Le froid reste coincé !",
            "narrateur|Ses épaules baissent, près du clou.",
            "narrateur|Maman s'accroupit, près du clou.",
            "maman|Personne ne dit où tirer.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le doudou n'est pas le panier.",
            "papa|Tu vois le grain, Nina ?",
            "narrateur|Le grain de paprika reste collé.",
            "narrateur|Le couvercle a bougé, un peu.",
        ],
        (3, 1): [
            "narrateur|Nina porte le panier vers les étals.",
            "narrateur|Les pavés luisent, froids sous les pas.",
            "enfant-f|Le ballon, avec le pain !",
            "narrateur|Près du volet, un ballon rond attend.",
            "narrateur|Le papier du pain veut s'envoler.",
            "enfant-f|Je prends tout, d'un coup.",
            "narrateur|Elle serre ballon et pain, trop vite.",
            "narrateur|Le panier penche, l'osier crisse.",
            "narrateur|Le ballon part, le papier file.",
            "enfant-f|Le pain s'envole !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "narrateur|Papa s'accroupit, près des pavés.",
            "papa|Personne ne dit où courir.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Sur l'osier, le grain de paprika tient.",
        ],
        (3, 2): [
            "narrateur|Nina pose le panier près d'un seau.",
            "narrateur|L'anse du seau est froide, lisse.",
            "enfant-f|Le seau, pour le pain !",
            "narrateur|Le seau est large, plus que l'osier.",
            "enfant-f|Le pain, dans le seau.",
            "narrateur|Elle bascule le panier, trop vite.",
            "narrateur|Le pain tombe au fond du seau.",
            "enfant-f|L'odeur a disparu !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Personne ne donne la réponse.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le seau n'est pas le panier.",
            "papa|Tu vois l'osier, Nina ?",
            "narrateur|Le grain de paprika pique, minuscule.",
        ],
        (3, 3): [
            "narrateur|Nina serre le panier contre elle.",
            "narrateur|Au clou d'un étal, un doudou pend.",
            "enfant-f|Mon doudou !",
            "narrateur|Il pend, comme le panier à la maison.",
            "enfant-f|Je le prends, et le pain.",
            "narrateur|Elle tire le doudou, trop vite.",
            "narrateur|Le panier s'accroche, l'osier crisse.",
            "enfant-f|Le pain reste coincé !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "narrateur|Papa s'accroupit, près du clou.",
            "papa|Personne ne dit où tirer.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Le doudou n'est pas le panier.",
            "maman|Tu vois le grain, Nina ?",
            "narrateur|Le grain de paprika reste collé.",
        ],
    }
    return table[(a, b)]


T3_CHOICE = {
    1: [
        "narrateur|Une couleur appelle, vers les étals.",
        "papa|Le rouge, le bleu, ou le vert ?",
        "maman|Tu vois laquelle, Nina ?",
    ],
    2: [
        "narrateur|Une couleur appelle, sous le volet.",
        "maman|Le rouge, le bleu, ou le vert ?",
        "papa|Tu vois laquelle, Nina ?",
    ],
    3: [
        "narrateur|Une couleur appelle, près du fournil.",
        "papa|Le rouge, le bleu, ou le vert ?",
        "maman|Tu vois laquelle, Nina ?",
    ],
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    arrive = {
        (1, 1): [
            "narrateur|Sous la nappe rouge, le ballon rebondit.",
            "enfant-f|Le rouge, avec le ballon, tout.",
            "narrateur|Elle prend trop, trop vite.",
        ],
        (1, 2): [
            "narrateur|Près de la caisse bleue, le ballon penche.",
            "enfant-f|Le bleu, avec le ballon, tout.",
            "narrateur|Elle pousse trop, trop vite.",
        ],
        (1, 3): [
            "narrateur|Sous la toile verte, le ballon roule.",
            "enfant-f|Le vert, avec le ballon, tout.",
            "narrateur|Elle saisit trop, trop vite.",
        ],
        (2, 1): [
            "narrateur|Sous la nappe rouge, le seau sonne.",
            "enfant-f|Le rouge, avec le seau, tout.",
            "narrateur|Elle prend trop, trop vite.",
        ],
        (2, 2): [
            "narrateur|Près de la caisse bleue, le seau sonne.",
            "enfant-f|Le bleu, avec le seau, tout.",
            "narrateur|Elle pousse trop, trop vite.",
        ],
        (2, 3): [
            "narrateur|Sous la toile verte, le seau sonne.",
            "enfant-f|Le vert, avec le seau, tout.",
            "narrateur|Elle saisit trop, trop vite.",
        ],
        (3, 1): [
            "narrateur|Sous la nappe rouge, le doudou pend.",
            "enfant-f|Le rouge, avec le doudou, tout.",
            "narrateur|Elle prend trop, trop vite.",
        ],
        (3, 2): [
            "narrateur|Près de la caisse bleue, le doudou pend.",
            "enfant-f|Le bleu, avec le doudou, tout.",
            "narrateur|Elle pousse trop, trop vite.",
        ],
        (3, 3): [
            "narrateur|Sous la toile verte, le doudou pend.",
            "enfant-f|Le vert, avec le doudou, tout.",
            "narrateur|Elle saisit trop, trop vite.",
        ],
    }[(b, c)]
    snag = {
        1: [
            "narrateur|Le panier se perd, parmi le rouge.",
            "enfant-f|Il a disparu !",
            "narrateur|Elle écarte une fraise, trop fort.",
        ],
        2: [
            "narrateur|Le panier se cache, derrière le bleu.",
            "enfant-f|Il a disparu !",
            "narrateur|Elle soulève la caisse, trop fort.",
        ],
        3: [
            "narrateur|Le panier disparaît, sous le vert.",
            "enfant-f|Il a disparu !",
            "narrateur|Elle lève la toile, trop fort.",
        ],
    }[c]
    faux = {
        1: "narrateur|Le ballon rond ment, une seconde.",
        2: "narrateur|Le seau large ment, une seconde.",
        3: "narrateur|Le doudou au clou ment, une seconde.",
    }[b]
    body = {
        1: [
            "narrateur|Dans sa poitrine, ça serre, fort.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu tires, ou tu regardes ?",
            "enfant-f|Je cherche, sans foncer.",
        ],
        2: [
            "narrateur|Ses épaules baissent, un peu.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu forces, ou tu regardes ?",
            "enfant-f|J'attends, je regarde.",
        ],
        3: [
            "narrateur|L'envie de tirer lui pique les doigts.",
            "narrateur|Papa s'accroupit, près d'elle.",
            "papa|Tu vois le grain, où ?",
            "enfant-f|Je cherche, sans foncer.",
        ],
    }[c]
    listen = {
        1: "narrateur|Elle écoute le volet, puis l'osier.",
        2: "narrateur|Elle écoute la caisse, puis l'osier.",
        3: "narrateur|Elle écoute la toile, puis l'osier.",
    }[c]
    pay = "narrateur|Le grain de paprika reparaît, collé."
    gesture = {
        1: "narrateur|Elle choisit une fraise, une seule.",
        2: "narrateur|Elle choisit une caisse, puis s'arrête.",
        3: "narrateur|Elle choisit un brin, un seul.",
    }[c]
    snack = {
        1: "narrateur|La pomme se cale, au fond.",
        2: "narrateur|Le pot se cale, au fond.",
        3: "narrateur|Le pain se cale, au fond.",
    }[a]
    adult = {
        1: "maman|Tu l'as, sans forcer.",
        2: "papa|Il est à toi, maintenant.",
        3: "maman|Tu l'as repris, Nina.",
    }[c]
    traces = {
        (1, 1): "narrateur|Une fraise a laissé une trace, à l'osier.",
        (1, 2): "narrateur|Un rond de pomme brille au bleu.",
        (1, 3): "narrateur|Un brin vert a touché la pomme.",
        (2, 1): "narrateur|Un rond froid tache le rouge.",
        (2, 2): "narrateur|Le pot a laissé sa fraîcheur, au bleu.",
        (2, 3): "narrateur|Un brin de persil touche le pot.",
        (3, 1): "narrateur|Une miette tient au rouge, minuscule.",
        (3, 2): "narrateur|Une miette brille dans le bleu.",
        (3, 3): "narrateur|Une miette sèche sous le vert.",
    }[(a, c)]
    almost = {
        (1, 1, 1): "narrateur|Le clou gardait le panier, presque.",
        (1, 1, 2): "narrateur|La nappe recouvrait l'osier, presque.",
        (1, 1, 3): "narrateur|Une fraise cachait le grain, presque.",
        (1, 2, 1): "narrateur|Le seau prenait la pomme, presque.",
        (1, 2, 2): "narrateur|La caisse bleue trompait la main, presque.",
        (1, 2, 3): "narrateur|La toile verte buvait l'osier, presque.",
        (1, 3, 1): "narrateur|Le doudou restait au clou, presque.",
        (1, 3, 2): "narrateur|Un fil bleu prenait le panier, presque.",
        (1, 3, 3): "narrateur|Le persil cachait le grain, presque.",
        (2, 1, 1): "narrateur|Le ballon cognait le pot, presque.",
        (2, 1, 2): "narrateur|Le froid fuyait sous le bleu, presque.",
        (2, 1, 3): "narrateur|Le pot roulait sous le vert, presque.",
        (2, 2, 1): "narrateur|Le seau gardait le yaourt, presque.",
        (2, 2, 2): "narrateur|La caisse serrait le pot, presque.",
        (2, 2, 3): "narrateur|L'anse se mêlait à l'osier, presque.",
        (2, 3, 1): "narrateur|Le doudou enroulait le pot, presque.",
        (2, 3, 2): "narrateur|Un fil prenait le couvercle, presque.",
        (2, 3, 3): "narrateur|Le persil collait au yaourt, presque.",
        (3, 1, 1): "narrateur|Le papier s'envolait au rouge, presque.",
        (3, 1, 2): "narrateur|Une miette couvrait le grain, presque.",
        (3, 1, 3): "narrateur|Le volet claquait trop tôt, presque.",
        (3, 2, 1): "narrateur|Le seau avalait le pain, presque.",
        (3, 2, 2): "narrateur|La croûte glissait au bleu, presque.",
        (3, 2, 3): "narrateur|Le fournil gardait le pain, presque.",
        (3, 3, 1): "narrateur|Le doudou emportait la miette, presque.",
        (3, 3, 2): "narrateur|Un fil bleu tenait le pain, presque.",
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
    toy = TOY[b]
    color = COLOR[c]
    firsts = {
        (1, 1, 1): "Une goutte de fraise sèche sur le ballon.",
        (1, 1, 2): "La nappe rouge a gardé un choc de pomme.",
        (1, 1, 3): "Le clou de l'étal reste vide, loin.",
        (1, 2, 1): "Le seau sonne, près de la porte.",
        (1, 2, 2): "Un rond de pomme brille dans le seau.",
        (1, 2, 3): "La toile verte a bougé, puis plus.",
        (1, 3, 1): "L'oreille du doudou sent la pomme.",
        (1, 3, 2): "Le doudou a un fil rouge, minuscule.",
        (1, 3, 3): "Un brin de persil reste au doudou.",
        (2, 1, 1): "Un rond froid sèche sur le ballon.",
        (2, 1, 2): "Le pot a laissé sa fraîcheur, loin.",
        (2, 1, 3): "Le volet bleu s'est tu, dehors.",
        (2, 2, 1): "Le seau garde un rond de yaourt.",
        (2, 2, 2): "La caisse bleue reste loin, vide.",
        (2, 2, 3): "Le persil a touché le seau, une fois.",
        (2, 3, 1): "Le doudou a un rond froid, minuscule.",
        (2, 3, 2): "Un fil du doudou a vu le bleu.",
        (2, 3, 3): "Le doudou sent le persil, un peu.",
        (3, 1, 1): "Une miette de pain tient au ballon.",
        (3, 1, 2): "Le papier du pain s'est tu.",
        (3, 1, 3): "Le volet a cessé de claquer.",
        (3, 2, 1): "Le seau a une miette, au fond.",
        (3, 2, 2): "La croûte a vu la caisse bleue.",
        (3, 2, 3): "Le seau sent le four, un peu.",
        (3, 3, 1): "Le doudou a une miette, à l'oreille.",
        (3, 3, 2): "Un fil du doudou sent le pain.",
        (3, 3, 3): "Le seuil retrouve le pain, unique.",
    }
    lasts = {
        (1, 1, 1): "Le ballon s'endort contre le grain.",
        (1, 1, 2): "La nappe a perdu son clou, loin.",
        (1, 1, 3): "Le grain de paprika veille, rouge.",
        (1, 2, 1): "Le seau s'est tu, près du clou.",
        (1, 2, 2): "Un rond de pomme sèche au seau.",
        (1, 2, 3): "La toile verte ne bouge plus.",
        (1, 3, 1): "L'oreille du doudou touche l'osier.",
        (1, 3, 2): "Un fil rouge s'endort au doudou.",
        (1, 3, 3): "Un brin de persil sèche à l'osier.",
        (2, 1, 1): "Un rond froid sèche contre le grain.",
        (2, 1, 2): "Loin du panier, le pot se tait.",
        (2, 1, 3): "Le volet bleu reste muet, dehors.",
        (2, 2, 1): "Au fond du seau, le froid s'endort.",
        (2, 2, 2): "La caisse bleue s'endort, loin.",
        (2, 2, 3): "Le persil s'est tu, près du seau.",
        (2, 3, 1): "Le doudou garde un rond froid.",
        (2, 3, 2): "Dans le bleu, un fil se tait.",
        (2, 3, 3): "Le doudou s'endort, près du persil.",
        (3, 1, 1): "Une miette s'endort contre le grain.",
        (3, 1, 2): "Loin du volet, le papier se tait.",
        (3, 1, 3): "Le volet du boulanger reste clos.",
        (3, 2, 1): "Au fond du seau, une miette veille.",
        (3, 2, 2): "La croûte s'endort, près du bleu.",
        (3, 2, 3): "Le seau sent le four, au silence.",
        (3, 3, 1): "L'oreille du doudou a une miette.",
        (3, 3, 2): "Un fil du doudou sent le four.",
        (3, 3, 3): "Au seuil, le pain ne croustille plus.",
    }
    qs = {
        1: "papa|Quel moment tu gardes, près du ballon ?",
        2: "maman|Quel moment tu gardes, près du seau ?",
        3: "papa|Quel moment tu gardes, près du doudou ?",
    }[b]
    ans = {
        (1, 1, 1): "enfant-f|Quand le ballon a menti, trop rond.",
        (1, 1, 2): "enfant-f|Quand j'ai ouvert, sans foncer.",
        (1, 1, 3): "enfant-f|Quand la fraise a caché le grain.",
        (1, 2, 1): "enfant-f|Quand le seau a pris la pomme.",
        (1, 2, 2): "enfant-f|Quand la caisse a trompé ma main.",
        (1, 2, 3): "enfant-f|Quand la toile a bu l'osier.",
        (1, 3, 1): "enfant-f|Quand le doudou pendait au clou.",
        (1, 3, 2): "enfant-f|Quand le fil bleu a tiré.",
        (1, 3, 3): "enfant-f|Quand le persil a caché le grain.",
        (2, 1, 1): "enfant-f|Quand le ballon a cogné le pot.",
        (2, 1, 2): "enfant-f|Quand le froid a voulu fuir.",
        (2, 1, 3): "enfant-f|Quand le pot a roulé au vert.",
        (2, 2, 1): "enfant-f|Quand le seau a gardé le yaourt.",
        (2, 2, 2): "enfant-f|Quand la caisse a serré le pot.",
        (2, 2, 3): "enfant-f|Quand l'anse a mêlé l'osier.",
        (2, 3, 1): "enfant-f|Quand le doudou a enroulé le pot.",
        (2, 3, 2): "enfant-f|Quand un fil a pris le couvercle.",
        (2, 3, 3): "enfant-f|Quand le persil a collé au pot.",
        (3, 1, 1): "enfant-f|Quand le papier a voulu s'envoler.",
        (3, 1, 2): "enfant-f|Quand la miette a montré le grain.",
        (3, 1, 3): "enfant-f|Quand le volet a failli claquer.",
        (3, 2, 1): "enfant-f|Quand le seau a avalé le pain.",
        (3, 2, 2): "enfant-f|Quand la croûte a glissé au bleu.",
        (3, 2, 3): "enfant-f|Quand le fournil a gardé le pain.",
        (3, 3, 1): "enfant-f|Quand le doudou a pris la miette.",
        (3, 3, 2): "enfant-f|Quand un fil bleu tenait le pain.",
        (3, 3, 3): "enfant-f|Quand l'odeur a ramené ma main.",
    }[(a, b, c)]
    return [
        f"narrateur|{firsts[(a, b, c)]}",
        f"narrateur|Elle a glissé {food['un']}, dans le panier.",
        f"narrateur|Elle a choisi {toy['lab']}.",
        f"narrateur|Puis {color['lab']}, sous le volet.",
        "narrateur|Voilà le panier d'osier, près de la porte.",
        "narrateur|Sur l'osier, le grain de paprika tient.",
        "enfant-f|Il est rentré, avec sa trace.",
        qs,
        ans,
        "enfant-f|Je raconte le moment difficile, surtout.",
        f"narrateur|{lasts[(a, b, c)]}",
    ]


def ending_note(a: int, b: int, c: int) -> str:
    return (
        f"arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
        f"destinataire=enfant; sous_texte=trace_{FOOD[a]['short']}_{TOY[b]['short']}_{COLOR[c]['short']}; "
        f"tempo=posé; sourire=léger; respiration=ample"
    )


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "volet,marche,osier")
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
            {"emphasis": "panier", "fields": Q_FIELDS[a]},
        )
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            FOOD[a]["sons"],
            {"emphasis": "panier"},
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
                TOY[b]["sons"],
                {"emphasis": TOY[b]["short"]},
            )
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
                T3_CHOICE[b],
                "choice",
                "",
                {"fields": {
                    "option_1_label": "le rouge",
                    "option_2_label": "le bleu",
                    "option_3_label": "le vert",
                }},
            )
            for c in (1, 2, 3):
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(
                    base,
                    t3_lines(a, b, c),
                    "resolution",
                    COLOR[c]["sons"],
                    {"emphasis": "grain de paprika"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "porte,osier",
                    {"emphasis": "grain de paprika", "note": ending_note(a, b, c)},
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
    if "grain de paprika" not in out_chunks["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit("indice absent de l'ouverture")
    for c in src["chunks"]:
        if c["kind"] == "passage" and "T0003_P000" in c["chunk_id"] and "_F0001" not in c["chunk_id"] and not c["chunk_id"].endswith("T0003_P0000"):
            if "grain de paprika" not in out_chunks[c["chunk_id"]]["text"].lower():
                raise SystemExit(f"indice non payé: {c['chunk_id']}")

    merged = dict(src)
    merged["fil_rouge"] = (
        "Un grain de paprika tient dans l'osier, au clou près de la porte. "
        "Nina connaît ce clou ; le grain rouge paraît nouveau. Elle veut le "
        "panier pour les fraises, avant que le volet du boulanger se taise. "
        "Elle tire trop vite : le panier résiste. Le sourire disparaît. Papa "
        "s'accroupit. On décroche, puis on part. Pomme, yaourt ou pain : à la "
        "main, patatras ; dans le panier, ça tient. Ballon, seau ou doudou : "
        "le jeu ment, l'osier dit vrai. Elle refuse de foncer. Rouge, bleu "
        "ou vert, le panier se perd. Le grain paie le début. Vingt-sept traces."
    )
    merged["title"] = TITLE
    merged["characters"] = "Nina, papa, maman"
    merged["setting"] = "maison puis marché, pavés, fraises, volet du boulanger, panier au clou"
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
        "Un grain de paprika tient dans l'osier, au clou près de la porte. "
        "Nina connaît ce clou ; le grain rouge paraît nouveau. Elle veut porter "
        "le panier au marché, pour les fraises, avant que le volet du boulanger "
        "se taise. Elle tire trop vite : le panier résiste. Le sourire disparaît. "
        "Papa s'accroupit. On décroche, puis on part, le panier avec eux. Pomme, "
        "yaourt ou pain : à la main ça glisse ; dans le panier, ça tient. Ballon, "
        "seau ou doudou : un rond, un large, un clou mentent. Elle refuse de "
        "foncer. Rouge, bleu ou vert, le panier se perd parmi la couleur. Le "
        "grain reparaît. Elle choisit une seule chose. L'osier garde une trace.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : maison puis marché, pavés, fraises, volet du boulanger, panier au clou.\n"
        "- Désir : porter le panier d'osier au marché, pour les fraises, avant le volet.\n"
        "- Objet : panier d'osier (grain de paprika), plus pomme / yaourt / pain.\n"
        "- Indice unique : le grain de paprika, vu dès l'ouverture, payé au climax.\n"
        "- Urgence douce : le volet du boulanger peut se taire ; les fraises partent.\n"
        "- Imprévu 1 : le panier résiste au clou ; la nourriture glisse hors de la main.\n"
        "- Cue : le panier est là. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : ballon-fruit, seau trop large, doudou au clou.\n"
        "- Revers allongé : coincé, corps (envie et peur), refus de foncer, grain.\n"
        "- Résolution : regarder l'osier, une seule chose, sans tout prendre.\n"
        "- Retour : grain de paprika, panier près de la porte, 27 traces distinctes.\n\n"
        "## Corrections éditoriales\n\n"
        "- Ouverture inventée (le grain dans l'osier, pavés mouillés sans « encore »).\n"
        "- Le premier choix n'enlève pas le panier : la nourriture entre dedans.\n"
        "- Revers allongé : coincé, corps, refus, second arrêt, geste lent.\n"
        "- Neuf obstacles T2 distincts, vingt-sept résolutions, vingt-sept fins.\n"
        "- Leçon AUT.ROU.001 vécue (une chose, puis l'autre), jamais dite.\n"
        "- Monde ≠ TREE-AUT-046 (Victorino, sac jaune, laitue), ≠ TREE-COL-017 "
        "(Amir, pain, virgule farine).\n"
        "- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Troupe D16 : Nina, papa, maman. Pas de 2e enfant.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js.\n\n"
        "## Direction vocale\n\n"
        "Impatience de Nina au départ, petit découragement quand le panier "
        "résiste ou que l'objet ment, fierté calme quand elle regarde sans "
        "foncer. L'adulte guide peu. `slow` réservé aux choix, à la question, "
        "au retour.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, 27 fins textuellement distinctes\n"
        f"- 27 T3 distincts, 9 T2 distincts\n"
        f"- {min(counts)} à {max(counts)} mots par chemin, moyenne {sum(counts)//27}\n"
        "- `text` et `script` synchronisés\n"
        "- `text_ssml` et `text_xai_tags` enrichis\n"
        "- `notes` présentes sur les 86 chunks\n"
        "- N1 ≤ 10 mots/phrase\n"
        "- check() OK. Pas d'apply. Pas d'audio. Pas de git.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"OK {SID} chemins {min(counts)}-{max(counts)} moy {sum(counts)//27}")


if __name__ == "__main__":
    build()
