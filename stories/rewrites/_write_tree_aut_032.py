#!/usr/bin/env python3
"""TREE-AUT-032 — Le manteau vert de Mila près de la casserole (F-NAR-019, N3)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-032"
N3 = LIMITS["N3"]
TITLE = "Le manteau vert de Mila près de la casserole"
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
    "ombre en forme",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="bracelet d'écorce",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience_curieuse; "
            "intensite=2; destinataire=enfant; sous_texte=le_bracelet_d_ecorce_tient_le_bouton; "
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
            "destinataire=enfant; sous_texte=ton_choix_change_la_sortie_au_vert; "
            "tempo=suspendu; sourire=léger; respiration=pause_avant_choix"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="manteau",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=elle_a_repris_le_vert; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="manteau",
        note=(
            "arc=confirmation; intention=relancer; emotion=soulagement_prudent; intensite=1; "
            "destinataire=enfant; sous_texte=le_vert_revient_sur_les_epaules; "
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
            "destinataire=enfant; sous_texte=elle_veut_le_bateau_trop_vite; "
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
            "intensite=2; destinataire=enfant; sous_texte=le_vert_menteur_n_est_pas_le_manteau; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="bracelet d'écorce",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=elle_suit_le_bracelet_sans_foncer; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="crochet",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=le_bracelet_et_la_casserole_ont_tenu_promesse; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "manteau",
    "accepted_examples": "manteau | le manteau | son manteau | le manteau vert",
    "retry_prompt": "Le manteau vert. Mila a pris quoi ?",
}

LOC = {
    1: dict(name="la cuisine", short="cuisine", ici="dans la cuisine", sons="casserole,orange"),
    2: dict(name="le jardin", short="jardin", ici="dans le jardin", sons="flaque,vent"),
    3: dict(name="la chambre", short="chambre", ici="dans la chambre", sons="rideau,lit"),
}
JEU = {
    1: dict(name="les cubes", short="cubes", un="un cube", sons="cubes,bois"),
    2: dict(name="le livre", short="livre", un="le livre", sons="page,papier"),
    3: dict(name="la dînette", short="dînette", un="une tasse", sons="tasse,cuillere"),
}
MOM = {
    1: dict(name="le matin", short="matin", quand="le matin", sons="vapeur,casserole"),
    2: dict(name="après la sieste", short="sieste", quand="après la sieste", sons="torchon,casserole"),
    3: dict(name="le soir", short="soir", quand="le soir", sons="lampe,casserole"),
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
    if emp and emp in text:
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


# Ouverture : Mila connaît la cuisine ; un détail paraît nouveau.
# Indice unique = bracelet d'écorce sur le bouton du bas.
OPENING = [
    "narrateur|Mila connaît cette cuisine, ses bruits, ses recoins.",
    "narrateur|Le frigo ronronne, bas, contre le mur.",
    "narrateur|Un torchon rayé sèche sur le dossier.",
    "narrateur|Les carreaux piquent un peu, sous les pieds.",
    "narrateur|Près de la porte, un détail paraît nouveau.",
    "narrateur|Au crochet bas, le manteau vert pend.",
    "narrateur|Le bouton du bas porte un bracelet d'écorce.",
    "narrateur|Papa a pelé une orange, trop vite.",
    "narrateur|Une petite bague d'écorce s'est posée, ronde.",
    "narrateur|La casserole tremble, couvercle contre vapeur.",
    "narrateur|Ça sent l'orange chaude, vive, dans l'air.",
    "maman|Le bateau d'écorce, avant que ça se taise ?",
    "enfant-f|Je veux le lancer, dans la flaque !",
    "narrateur|En ce moment, Mila tire le manteau, trop fort.",
    "narrateur|Une manche est à l'envers, coincée.",
    "narrateur|Le bracelet d'écorce glisse, presque.",
    "enfant-f|Il ne veut pas venir !",
    "narrateur|Son sourire disparaît, net.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "papa|Le bracelet tient le bouton, vois.",
    "maman|Tu sors comment, avec lui ?",
    "narrateur|Sur la planche, le bateau d'écorce attend.",
    "narrateur|Le couvercle chante, mince, pressé.",
]

T1_CHOICE = [
    "narrateur|Le bateau d'écorce attend, près de la planche.",
    "papa|On passe où, avant la flaque ?",
    "narrateur|La cuisine.",
    "narrateur|Le jardin.",
    "narrateur|Ou la chambre.",
]

T1 = {
    1: [
        "narrateur|Mila reste près de la casserole, pressée.",
        "narrateur|La vapeur lui chauffe les joues, trop.",
        "narrateur|Elle ouvre deux boutons, trop vite.",
        "narrateur|Le vert glisse, et tombe près du feu.",
        "enfant-f|J'ai trop chaud, je n'en ai plus besoin.",
        "narrateur|Un air vif entre, sous la porte.",
        "enfant-f|J'ai froid, sans lui.",
        "narrateur|Elle saisit le torchon rayé, trop vite.",
        "enfant-f|Ce n'est pas lui, c'est le torchon.",
        "papa|Le bracelet, vois, près du bois.",
        "narrateur|La petite bague d'écorce brille, minuscule.",
        "maman|Tu le reprends, avant la flaque ?",
    ],
    2: [
        "narrateur|Mila pousse la porte du jardin, le bateau à la main.",
        "narrateur|L'herbe brille, mouillée, sous les chaussons.",
        "narrateur|Elle accroche le manteau au crochet du muret.",
        "enfant-f|Je lance, je reviens !",
        "narrateur|Le vent pousse le vert vers le mur.",
        "enfant-f|Il s'envole, tout seul !",
        "narrateur|Elle saisit une feuille, trop vite.",
        "enfant-f|Ce n'était pas lui.",
        "narrateur|Ses épaules baissent, dans l'herbe.",
        "papa|Le bracelet, entends-tu, contre le bois ?",
        "narrateur|La petite bague d'écorce répond, minuscule.",
        "maman|Tu le reprends, avant la flaque ?",
    ],
    3: [
        "narrateur|Mila entre dans la chambre, le bateau serré.",
        "narrateur|Le rideau vert bouge, près du lit.",
        "enfant-f|J'ai trop chaud, ici.",
        "narrateur|Elle jette le manteau sur la couverture.",
        "narrateur|Elle cherche une chaussette, sous le lit.",
        "maman|La fenêtre est ouverte, un peu.",
        "narrateur|L'air vif entre, net.",
        "enfant-f|J'ai froid, maman.",
        "narrateur|Elle saisit le rideau, trop vite.",
        "enfant-f|Ce n'est pas lui, c'est le rideau.",
        "papa|Le bracelet, vois, sous le drap.",
        "narrateur|La petite bague d'écorce brille, minuscule.",
    ],
}

T1_Q = {
    1: [
        "narrateur|Mila a froid, près de la casserole.",
        "papa|Elle a repris quoi, près du crochet ?",
    ],
    2: [
        "narrateur|Dans le jardin, le manteau a glissé.",
        "maman|Elle a repris quoi, près du crochet ?",
    ],
    3: [
        "narrateur|Le manteau était sous le drap.",
        "papa|Elle a repris quoi, près du crochet ?",
    ],
}

T1_C = {
    1: [
        "narrateur|Mila se baisse vers le tissu vert.",
        "narrateur|Elle glisse un bras, puis l'autre.",
        "enfant-f|Je le reprends, il est à moi.",
        "maman|Merci, Mila.",
        "narrateur|Elle ferme deux boutons, pas tous.",
        "papa|On emporte un jeu, avec le bateau ?",
        "enfant-f|Oui, pour la flaque.",
        "narrateur|Le bracelet d'écorce reste au bouton du bas.",
        "narrateur|Le col vert revient sur ses épaules.",
    ],
    2: [
        "narrateur|Mila suit le bois, le long du muret.",
        "narrateur|Elle reprend le manteau, un peu froid.",
        "enfant-f|Je le mets, il est à moi.",
        "maman|Merci, Mila.",
        "narrateur|Le bateau d'écorce rentre dans la poche.",
        "papa|On emporte un jeu, pour la flaque ?",
        "enfant-f|Oui, avec moi.",
        "narrateur|Le bracelet d'écorce reste au bouton du bas.",
        "narrateur|Le col vert revient sur ses épaules.",
    ],
    3: [
        "narrateur|Mila soulève le drap, sans tirer.",
        "narrateur|Elle reprend le manteau, sous le lit.",
        "enfant-f|Je le remets, il est à moi.",
        "papa|Merci, Mila.",
        "narrateur|La chaussette rentre dans la poche.",
        "maman|On emporte un jeu aussi ?",
        "enfant-f|Oui, maman.",
        "narrateur|Le bracelet d'écorce reste au bouton du bas.",
        "narrateur|Le col vert revient sur ses épaules.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Près de la casserole, un jeu l'appelle.",
        "maman|Les cubes, le livre, ou la dînette ?",
        "papa|Le manteau reste avec toi.",
    ],
    2: [
        "narrateur|Près du muret, un jeu l'appelle.",
        "papa|Les cubes, le livre, ou la dînette ?",
        "maman|Le manteau reste avec toi.",
    ],
    3: [
        "narrateur|Près du lit, un jeu l'appelle.",
        "maman|Les cubes, le livre, ou la dînette ?",
        "papa|Le manteau reste avec toi.",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    table = {
        (1, 1): [
            "narrateur|Mila pose les cubes près de la casserole.",
            "narrateur|Un cube vert cliquette, un peu lourd.",
            "papa|On fait un quai, pour le bateau ?",
            "enfant-f|Oui, un quai de cubes.",
            "narrateur|Elle pose le manteau comme une nappe.",
            "narrateur|Un cube roule, et le vert glisse.",
            "enfant-f|Il est là, près du feu !",
            "narrateur|Elle saisit la vapeur, vide.",
            "enfant-f|Ce n'était pas lui.",
            "narrateur|Ses épaules baissent, un instant.",
            "maman|Le bracelet, pas la vapeur.",
            "narrateur|Un cube garde un reflet d'orange.",
            "enfant-f|Je ne fonce pas.",
        ],
        (1, 2): [
            "narrateur|Mila ouvre le livre, près de l'évier.",
            "narrateur|La couverture montre des oranges.",
            "maman|Comme celle de papa, sur la planche.",
            "enfant-f|Oui, les vraies oranges.",
            "narrateur|Elle glisse le livre sous le manteau.",
            "narrateur|Le vert et la page se confondent.",
            "enfant-f|Je le prends, il est là !",
            "narrateur|Sa main tient le livre, pas le tissu.",
            "enfant-f|Le manteau a disparu.",
            "narrateur|Ses épaules baissent, près du bol.",
            "papa|Le bracelet, pas la page.",
            "narrateur|Une miette d'orange reste au bord.",
            "enfant-f|Je ne fonce pas.",
        ],
        (1, 3): [
            "narrateur|Mila sort la dînette, près du vrai feu.",
            "narrateur|Une petite casserole sonne, creuse.",
            "papa|On sert l'orange, ici ?",
            "enfant-f|Oui, un bol pour le bateau.",
            "narrateur|Elle étale le manteau, comme une nappe.",
            "narrateur|La petite casserole penche, et le vert glisse.",
            "enfant-f|Il est là, sous la tasse !",
            "narrateur|Elle saisit le torchon rayé, vide.",
            "enfant-f|Ce n'était pas lui.",
            "narrateur|Ses épaules baissent, près de l'évier.",
            "maman|Le bracelet, pas le torchon.",
            "narrateur|La petite cuillère reste près du bol.",
            "enfant-f|Je ne fonce pas.",
        ],
        (2, 1): [
            "narrateur|Mila pose les cubes dans l'herbe.",
            "narrateur|Un cube sent le pin, un peu.",
            "papa|On fait un quai, dehors ?",
            "enfant-f|Oui, un quai de cubes.",
            "narrateur|Elle pose le manteau sur le muret.",
            "narrateur|Le vent le pousse, et un cube roule.",
            "enfant-f|Il est là, contre le mur !",
            "narrateur|Elle saisit une feuille, trop vite.",
            "enfant-f|Ce n'était pas lui.",
            "narrateur|Ses épaules baissent, dans l'herbe.",
            "maman|Le bracelet, pas la feuille.",
            "narrateur|L'herbe colore un cube, tout vert.",
            "enfant-f|Je ne fonce pas.",
        ],
        (2, 2): [
            "narrateur|Mila ouvre le livre, près du muret.",
            "narrateur|Une page sent le papier, frais.",
            "maman|On le regardera près de la flaque.",
            "enfant-f|Oui, avec le vrai bateau.",
            "narrateur|Elle pose le livre sur le manteau.",
            "narrateur|Le vent tourne une page, trop vite.",
            "enfant-f|Le vert est sous la page !",
            "narrateur|Sa main tient le livre, pas le tissu.",
            "enfant-f|Le manteau a disparu.",
            "narrateur|Ses épaules baissent, près du muret.",
            "papa|Le bracelet, pas la page.",
            "narrateur|Une goutte reste sur la page.",
            "enfant-f|Je ne fonce pas.",
        ],
        (2, 3): [
            "narrateur|Mila pose la dînette dans l'herbe.",
            "narrateur|Une petite assiette sonne, légère.",
            "papa|On sert un thé, dehors ?",
            "enfant-f|Oui, un thé d'orange.",
            "narrateur|Elle étale le manteau, comme une nappe.",
            "narrateur|Une goutte perle au bord de l'assiette.",
            "enfant-f|Il est là, sous l'assiette !",
            "narrateur|Elle saisit une feuille, trop vite.",
            "enfant-f|Ce n'était pas lui.",
            "narrateur|Ses épaules baissent, près du muret.",
            "maman|Le bracelet, pas la feuille.",
            "narrateur|La petite tasse reste froide, dans l'herbe.",
            "enfant-f|Je ne fonce pas.",
        ],
        (3, 1): [
            "narrateur|Mila pose les cubes près du lit.",
            "narrateur|Un cube tapote le parquet, net.",
            "papa|On fait un quai, ici ?",
            "enfant-f|Oui, un quai de cubes.",
            "narrateur|Elle pose le manteau sur l'oreiller.",
            "narrateur|Un cube roule, et le vert glisse.",
            "enfant-f|Il est là, sous l'oreiller !",
            "narrateur|Elle saisit le drap vert, vide.",
            "enfant-f|Ce n'était pas lui.",
            "narrateur|Ses épaules baissent, près du lit.",
            "maman|Le bracelet, pas le drap.",
            "narrateur|Un cube tapote le parquet, plus loin.",
            "enfant-f|Je ne fonce pas.",
        ],
        (3, 2): [
            "narrateur|Mila ouvre le livre, sur le lit.",
            "narrateur|Le rideau vert colore la page.",
            "maman|On le regardera près de la flaque.",
            "enfant-f|Oui, avec le vrai bateau.",
            "narrateur|Elle glisse le livre sous le manteau.",
            "narrateur|Le vert et le rideau se confondent.",
            "enfant-f|Il est là, près de la fenêtre !",
            "narrateur|Sa main tient le rideau, pas le tissu.",
            "enfant-f|Le manteau a disparu.",
            "narrateur|Ses épaules baissent, près du lit.",
            "papa|Le bracelet, pas le rideau.",
            "narrateur|Une page se recourbe, sur la couverture.",
            "enfant-f|Je ne fonce pas.",
        ],
        (3, 3): [
            "narrateur|Mila pose la dînette près du lit.",
            "narrateur|Une petite tasse sonne, creuse.",
            "papa|On sert un thé, ici ?",
            "enfant-f|Oui, un thé d'orange.",
            "narrateur|Elle étale le manteau, comme une nappe.",
            "narrateur|La tasse penche, et le vert glisse.",
            "enfant-f|Il est là, sous la tasse !",
            "narrateur|Elle saisit le tapis vert, vide.",
            "enfant-f|Ce n'était pas lui.",
            "narrateur|Ses épaules baissent, près du lit.",
            "maman|Le bracelet, pas le tapis.",
            "narrateur|La petite tasse reste près du bateau.",
            "enfant-f|Je ne fonce pas.",
        ],
    }
    return table[(a, b)]


T3_CHOICE = {
    1: [
        "papa|C'est quel moment, pour la flaque ?",
        "narrateur|Le matin.",
        "narrateur|Après la sieste.",
        "narrateur|Ou le soir.",
    ],
    2: [
        "maman|C'est quel moment, pour la flaque ?",
        "narrateur|Le matin.",
        "narrateur|Après la sieste.",
        "narrateur|Ou le soir.",
    ],
    3: [
        "papa|C'est quel moment, pour la flaque ?",
        "narrateur|Le matin.",
        "narrateur|Après la sieste.",
        "narrateur|Ou le soir.",
    ],
}

TRACE_AB = {
    (1, 1): "Un cube attrape un reflet d'orange, au bouton.",
    (1, 2): "Une miette d'orange reste au bord de la page.",
    (1, 3): "La petite casserole est près du vrai feu, dehors.",
    (2, 1): "L'herbe colore un cube, tout vert, au quai.",
    (2, 2): "Une vraie goutte marque la page, dehors.",
    (2, 3): "Une goutte perle au bord de l'assiette, dehors.",
    (3, 1): "Un cube tapote le parquet, dans sa mémoire.",
    (3, 2): "Le rideau vert colore la page, au bord.",
    (3, 3): "La petite tasse est près du lit, dans sa poche.",
}

GAME_BC = {
    (1, 1): "Je pose un cube, près de la flaque froide.",
    (1, 2): "Je pose un cube, près de la flaque tiède.",
    (1, 3): "Je pose un cube, sous la lampe du jardin.",
    (2, 1): "J'ouvre le livre, près de l'eau froide.",
    (2, 2): "J'ouvre le livre, près de l'eau tiède.",
    (2, 3): "J'ouvre le livre, sous la lampe du jardin.",
    (3, 1): "Je pose une tasse, près de la flaque froide.",
    (3, 2): "Je pose une tasse, près de la flaque tiède.",
    (3, 3): "Je pose une tasse, sous la lampe du jardin.",
}

PLACE_AC = {
    (1, 1): "Un froid de carreaux reste sous ses chaussons.",
    (1, 2): "L'odeur d'orange de la casserole la suit.",
    (1, 3): "Le col ouvert lui tient chaud, dehors.",
    (2, 1): "Les chaussons font ploc, sur l'herbe froide.",
    (2, 2): "L'écorce de la poche sent fort, tout vif.",
    (2, 3): "Une goutte du jardin glisse du manteau vert.",
    (3, 1): "La chaussette tapote la poche, dehors.",
    (3, 2): "Le rideau vert reste derrière, à la maison.",
    (3, 3): "Le savon de la chambre reste sur le col.",
}

ALMOST = {
    (1, 1, 1): "La vapeur cachait le bracelet, presque.",
    (1, 1, 2): "Le torchon prenait la place, une seconde.",
    (1, 1, 3): "L'ombre du feu recouvrait le bouton, presque.",
    (1, 2, 1): "La page collait au vert, presque.",
    (1, 2, 2): "Une miette mentait, une seconde de trop.",
    (1, 2, 3): "La lampe dorait le livre, pas le tissu.",
    (1, 3, 1): "La petite casserole mentait, presque.",
    (1, 3, 2): "Le torchon rayé trompait l'œil, une seconde.",
    (1, 3, 3): "La cuillère cachait le bouton, presque.",
    (2, 1, 1): "Une feuille couvrait le bracelet, presque.",
    (2, 1, 2): "Le vent poussait trop, une seconde.",
    (2, 1, 3): "L'herbe prenait la couleur, presque.",
    (2, 2, 1): "La page volait, une seconde de trop.",
    (2, 2, 2): "Une goutte collait au livre, presque.",
    (2, 2, 3): "Le vent fermait le livre, une seconde.",
    (2, 3, 1): "L'assiette prenait la place, presque.",
    (2, 3, 2): "Une goutte mentait, une seconde de trop.",
    (2, 3, 3): "La tasse froide trompait la main, presque.",
    (3, 1, 1): "L'oreiller mélangeait les verts, presque.",
    (3, 1, 2): "Le drap prenait la place, une seconde.",
    (3, 1, 3): "Un cube tapait trop fort, une seconde.",
    (3, 2, 1): "Le rideau prenait le col, presque.",
    (3, 2, 2): "Une page se recourbait, une seconde.",
    (3, 2, 3): "La fenêtre mentait, une seconde de trop.",
    (3, 3, 1): "Le tapis mélangeait les verts, presque.",
    (3, 3, 2): "La tasse penche trop, une seconde.",
    (3, 3, 3): "La veilleuse dorait le tapis, pas le tissu.",
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    cores = {
        1: [
            "papa|La casserole chante fort, ce matin.",
            "narrateur|Ils sortent, et l'air pique le nez.",
            "narrateur|Mila pose le manteau près de la flaque.",
            "enfant-f|Je lance, vite, avant le silence !",
            "narrateur|La vapeur de la vitre dessine un vert.",
            "enfant-f|Il est sur la vitre, je le vois !",
            "narrateur|Elle saisit l'air, trop vite.",
            "narrateur|Cette fois, elle refuse de foncer.",
            "narrateur|Le bracelet d'écorce brille, au bouton du bas.",
            "enfant-f|La petite bague, je la vois.",
            "narrateur|Elle soulève le col, sans tirer.",
            "papa|Le bateau, pour la flaque ?",
            "narrateur|Mila le pose, et l'eau le prend.",
        ],
        2: [
            "papa|La casserole est plus calme, après la sieste.",
            "narrateur|Ils sortent, et les carreaux sont tièdes.",
            "narrateur|Mila pose le manteau sur le muret.",
            "enfant-f|Je lance, il est tiède !",
            "narrateur|Le torchon rayé pend, à côté du vert.",
            "enfant-f|Il est là, je le vois !",
            "narrateur|Elle saisit le torchon, trop vite.",
            "narrateur|Cette fois, elle refuse de foncer.",
            "narrateur|Le bracelet d'écorce brille, au bouton du bas.",
            "enfant-f|La petite bague, je la vois.",
            "narrateur|Elle soulève le col, sans tirer.",
            "papa|Le bateau, pour la flaque ?",
            "narrateur|Mila le pose, et l'eau le berce.",
        ],
        3: [
            "papa|La casserole se tait, ce soir.",
            "narrateur|Ils sortent, et la lampe est jaune.",
            "narrateur|Mila pose le manteau près de la flaque.",
            "enfant-f|Je lance, avant la nuit !",
            "narrateur|L'ombre du manteau allonge un faux vert.",
            "enfant-f|Il est dans l'ombre, je le vois !",
            "narrateur|Elle saisit l'ombre, trop vite.",
            "narrateur|Cette fois, elle refuse de foncer.",
            "narrateur|Le bracelet d'écorce brille, au bouton du bas.",
            "enfant-f|La petite bague, je la vois.",
            "narrateur|Elle soulève le col, sans tirer.",
            "papa|Le bateau, pour la flaque ?",
            "narrateur|Mila le pose, et l'eau le garde.",
        ],
    }[c]
    return cores + [
        f"enfant-f|{GAME_BC[(b, c)]}",
        f"narrateur|{PLACE_AC[(a, c)]}",
        f"narrateur|{TRACE_AB[(a, b)]}",
        f"narrateur|{ALMOST[(a, b, c)]}",
    ]


LASTS = {
    (1, 1, 1): "Un cube garde un reflet d'orange, au crochet.",
    (1, 1, 2): "Un cube sent la casserole, près du bol.",
    (1, 1, 3): "L'ombre d'un cube danse sur le carrelage.",
    (1, 2, 1): "Une page sent l'orange, près du bol.",
    (1, 2, 2): "Le livre est tiède, près de la vitre.",
    (1, 2, 3): "La lampe dore le bord d'une page.",
    (1, 3, 1): "Une petite tasse a une goutte d'orange.",
    (1, 3, 2): "La dînette est chaude, comme la cuisine.",
    (1, 3, 3): "La petite cuillère brille sous la lampe.",
    (2, 1, 1): "Un cube a une goutte d'herbe.",
    (2, 1, 2): "Le cube sèche au soleil, tout vert.",
    (2, 1, 3): "Un cube garde une goutte, toute ronde.",
    (2, 2, 1): "Une vraie goutte marque la page.",
    (2, 2, 2): "Le livre sent l'herbe mouillée.",
    (2, 2, 3): "Un oiseau se tait, près du livre.",
    (2, 3, 1): "Une petite assiette a de la rosée.",
    (2, 3, 2): "La dînette est tiède, au soleil.",
    (2, 3, 3): "Loin de la dînette, une goutte tombe.",
    (3, 1, 1): "Un rayon pose sur la tour de cubes.",
    (3, 1, 2): "Un cube est contre l'oreiller, silencieux.",
    (3, 1, 3): "L'ombre des cubes danse sur le mur.",
    (3, 2, 1): "Le rideau vert colore la page.",
    (3, 2, 2): "Le livre est ouvert sur la couverture.",
    (3, 2, 3): "La page sent le savon, un peu.",
    (3, 3, 1): "Une tasse miniature est près du lit.",
    (3, 3, 2): "La dînette attend au pied du lit.",
    (3, 3, 3): "Une petite assiette reflète la veilleuse.",
}

FINS = {
    (1, 1, 1): "L'orange reste sur la planche, près des cubes.",
    (1, 1, 2): "La casserole fait un tout petit pschitt.",
    (1, 1, 3): "Une miette d'orange reste sur la table.",
    (1, 2, 1): "Un oiseau chante, très loin.",
    (1, 2, 2): "La page se recourbe, près du bol.",
    (1, 2, 3): "La lampe dore le livre fermé.",
    (1, 3, 1): "La petite tasse sèche près de l'évier.",
    (1, 3, 2): "L'écorce sent, près du sol.",
    (1, 3, 3): "Le bouton du manteau brille, au crochet.",
    (2, 1, 1): "Les chaussons sèchent près de la porte.",
    (2, 1, 2): "L'herbe colle à un cube.",
    (2, 1, 3): "Une goutte glisse du manteau vert.",
    (2, 2, 1): "Une goutte reste dans le livre.",
    (2, 2, 2): "Le jardin est pâle, derrière la vitre.",
    (2, 2, 3): "La flaque ne brille plus, dehors.",
    (2, 3, 1): "La petite assiette a de l'herbe.",
    (2, 3, 2): "Les chaussons font un dernier ploc.",
    (2, 3, 3): "Le col vert sèche, au crochet.",
    (3, 1, 1): "La chaussette repose sur un cube.",
    (3, 1, 2): "L'oreiller sent le savon.",
    (3, 1, 3): "Le rideau vert ne bouge plus.",
    (3, 2, 1): "La chaussette sèche sur la couverture.",
    (3, 2, 2): "Une page reste ouverte, sur le lit.",
    (3, 2, 3): "La veilleuse dore le livre.",
    (3, 3, 1): "La petite tasse est près du bateau d'écorce.",
    (3, 3, 2): "Le tapis de la chambre se tait.",
    (3, 3, 3): "Le crochet de bois attend, bas.",
}


def ending_lines(a: int, b: int, c: int) -> list[str]:
    loc = LOC[a]["name"]
    jeu = JEU[b]["name"]
    mom = MOM[c]["quand"]
    img = LASTS[(a, b, c)]
    fin = FINS[(a, b, c)]
    return [
        "papa|C'est l'heure de rentrer.",
        "narrateur|Mila raccroche le manteau au crochet.",
        "narrateur|Le bracelet d'écorce tient le bouton du bas.",
        "enfant-f|Il sèche, là.",
        f"narrateur|Mila est passée par {loc}.",
        f"narrateur|Elle a emporté {jeu}.",
        f"narrateur|C'était {mom}.",
        "maman|Le bateau a voyagé, toi aussi.",
        f"narrateur|{img}",
        f"narrateur|{fin}",
    ]


def ending_note(a: int, b: int, c: int) -> str:
    return (
        f"arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
        f"destinataire=enfant; sous_texte=trace_{LOC[a]['short']}_{JEU[b]['short']}_{MOM[c]['short']}; "
        f"tempo=posé; sourire=léger; respiration=ample"
    )


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "casserole,orange,crochet")
    put(
        "CHK_T0001_P0000",
        T1_CHOICE,
        "choice",
        "",
        {"fields": {
            "option_1_label": "la cuisine",
            "option_2_label": "le jardin",
            "option_3_label": "la chambre",
        }},
    )

    for a in (1, 2, 3):
        put(
            f"CHK_T0001_P000{a}",
            T1[a],
            "action",
            LOC[a]["sons"],
            {"emphasis": "manteau"},
        )
        put(
            f"CHK_T0001_P000{a}_Q0001",
            T1_Q[a],
            "clue",
            "",
            {"emphasis": "manteau", "fields": Q_FIELDS},
        )
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            LOC[a]["sons"],
            {"emphasis": "manteau"},
        )
        put(
            f"CHK_T0001_P000{a}_T0002_P0000",
            T2_CHOICE[a],
            "choice",
            "",
            {"fields": {
                "option_1_label": "les cubes",
                "option_2_label": "le livre",
                "option_3_label": "la dînette",
            }},
        )
        for b in (1, 2, 3):
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}",
                t2_lines(a, b),
                "obstacle",
                JEU[b]["sons"],
                {"emphasis": JEU[b]["short"]},
            )
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
                T3_CHOICE[b],
                "choice",
                "",
                {"fields": {
                    "option_1_label": "le matin",
                    "option_2_label": "après la sieste",
                    "option_3_label": "le soir",
                }},
            )
            for c in (1, 2, 3):
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(
                    base,
                    t3_lines(a, b, c),
                    "resolution",
                    MOM[c]["sons"],
                    {"emphasis": "bracelet d'écorce"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "crochet,casserole",
                    {"emphasis": "crochet", "note": ending_note(a, b, c)},
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
        "Mila connaît la cuisine. Un détail paraît nouveau : au crochet bas, "
        "le manteau vert porte un bracelet d'écorce sur le bouton du bas. "
        "La casserole tremble. Elle veut lancer le bateau d'écorce dans la "
        "flaque avant que le couvercle se taise. Elle tire trop fort : manche "
        "à l'envers, bracelet qui glisse. Cuisine, jardin ou chambre, le vert "
        "glisse. Elle le reprend. Cubes, livre ou dînette : un faux vert ment, "
        "le bracelet dit vrai. Matin, sieste ou soir, elle refuse de foncer. "
        "La petite bague paie le début. Le manteau rentre au crochet."
    )
    merged["title"] = TITLE
    merged["characters"] = "Mila, papa, maman"
    merged["setting"] = "cuisine, casserole, orange, crochet bas près de la porte"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    counts = [
        sum(words(out_chunks[i]["text"]) for i in path_ids(a, b, c))
        for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)
    ]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")
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
        "Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, "
        "types de blocs et destinations techniques inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Mila connaît cette cuisine, ses bruits, ses recoins. Un détail paraît "
        "nouveau : au crochet bas, le manteau vert porte un bracelet d'écorce "
        "sur le bouton du bas. Papa a pelé trop vite. La casserole tremble. "
        "Mila veut lancer le bateau d'écorce dans la flaque avant que le "
        "couvercle se taise. Elle tire trop fort : manche à l'envers, bracelet "
        "qui glisse. Cuisine, jardin ou chambre, le vert glisse. Elle le "
        "reprend. Cubes, livre ou dînette : un faux vert ment. Matin, sieste "
        "ou soir, vapeur, torchon ou ombre, elle refuse de foncer. La petite "
        "bague paie le début. Le manteau rentre au crochet, avec sa trace.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : cuisine, casserole, orange, crochet bas près de la porte.\n"
        "- Désir : lancer le bateau d'écorce dans la flaque, maintenant.\n"
        "- Objet : manteau vert (bouton du bas, bracelet d'écorce).\n"
        "- Indice unique : le bracelet d'écorce, vu dès l'ouverture, payé au climax.\n"
        "- Urgence douce : le couvercle se tait, la flaque attend.\n"
        "- Imprévu 1 : tirer trop fort, manche à l'envers, vert qui glisse.\n"
        "- Cue : le bracelet tient le bouton. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : vapeur, torchon, feuille, rideau, ombre mentent.\n"
        "- Résolution : refuser de foncer, suivre le bracelet, soulever sans tirer.\n"
        "- Retour : crochet, bracelet, casserole, 27 traces distinctes.\n\n"
        "## Corrections éditoriales\n\n"
        "- Ouverture inventée (la cuisine connue, un détail nouveau), pas un gabarit v2.\n"
        "- Le premier choix n'enlève pas le manteau : il vient en cuisine, au jardin, en chambre.\n"
        "- Revers allongé : froid, glissade, faux vert, refus de foncer, geste lent.\n"
        "- Neuf disparitions distinctes, vingt-sept résolutions, vingt-sept fins.\n"
        "- Leçon AUT.AFF.002 vécue (reprendre le manteau), jamais dite.\n"
        "- Monde ≠ TREE-AUT-016 (laine Raphaël), ≠ TREE-AUT-023 (manteau rampe), "
        "≠ TREE-AUT-027 (manteau bleu marché).\n"
        "- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Troupe D16 : Mila, papa, maman.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js.\n\n"
        "## Direction vocale\n\n"
        "Impatience au départ, petit découragement quand le manteau résiste "
        "ou disparaît, fierté calme quand Mila suit le bracelet. "
        "L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, 27 fins textuellement distinctes\n"
        f"- 27 T3 distincts, 9 T2 distincts\n"
        f"- {min(counts)} à {max(counts)} mots par chemin, moyenne {sum(counts)//27}\n"
        "- `text` et `script` synchronisés\n"
        "- `text_ssml` et `text_xai_tags` enrichis\n"
        "- `notes` présentes sur les 86 chunks\n"
        "- N3 ≤ 16 mots/phrase\n"
        "- check() OK. Pas d'apply. Pas d'audio. Pas de git.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {len(merged['chunks'])} chunks  chemins {min(counts)}-{max(counts)}")


if __name__ == "__main__":
    build()
