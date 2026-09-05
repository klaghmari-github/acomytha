#!/usr/bin/env python3
"""TREE-AUT-027 — Le manteau bleu de Mila au marché (F-NAR-019, N2, AUT.AFF.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-027"
N2 = LIMITS["N2"]
TITLE = "Le manteau bleu de Mila au marché"
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
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="manteau bleu",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience_curieuse; "
            "intensite=2; destinataire=enfant; sous_texte=le_bouton_a_lune_fait_toc; "
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
            "destinataire=enfant; sous_texte=ton_choix_change_la_sortie; "
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
            "destinataire=enfant; sous_texte=elle_a_repris_le_bleu; "
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
            "destinataire=enfant; sous_texte=le_manteau_revient_sur_les_epaules; "
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
            "destinataire=enfant; sous_texte=elle_veut_partir_sans_le_bleu; "
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
            "intensite=2; destinataire=enfant; sous_texte=le_bleu_menteur_n_est_pas_le_manteau; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="bouton",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=elle_ecoute_le_toc_sans_foncer; "
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
            "destinataire=enfant; sous_texte=le_toc_et_l_orange_ont_tenu_promesse; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "manteau",
    "accepted_examples": "manteau | le manteau | son manteau | le manteau bleu",
    "retry_prompt": "Le manteau bleu. Elle a repris quoi ?",
}

LOC = {
    1: dict(name="la cuisine", short="cuisine", ici="dans la cuisine", sons="orange,menthe"),
    2: dict(name="le jardin", short="jardin", ici="dans le jardin", sons="vent,herbe"),
    3: dict(name="la chambre", short="chambre", ici="dans la chambre", sons="rideau,lit"),
}
JEU = {
    1: dict(name="les cubes", short="cubes", un="un cube", sons="cubes,bois"),
    2: dict(name="le livre", short="livre", un="le livre", sons="page,papier"),
    3: dict(name="la dînette", short="dînette", un="une tasse", sons="tasse,cuillere"),
}
MOM = {
    1: dict(name="le matin", short="matin", quand="le matin", sons="marche,bache"),
    2: dict(name="après la sieste", short="sieste", quand="après la sieste", sons="store,marche"),
    3: dict(name="le soir", short="soir", quand="le soir", sons="lampe,marche"),
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


OPENING = [
    "narrateur|Le seuil tient l'ombre ovale du panier.",
    "narrateur|Au loin, une bâche rayée claque.",
    "narrateur|Ça sent l'orange, mêlée à la menthe.",
    "narrateur|Sur le crochet, un manteau bleu attend.",
    "narrateur|Le bouton du bas a une entaille.",
    "narrateur|Elle a la forme d'une petite lune.",
    "narrateur|Le bouton fait toc contre le bois.",
    "papa|Une orange, avant que la bâche se plie.",
    "enfant-f|Je veux y aller, vite !",
    "narrateur|En ce moment, Mila court vers la porte.",
    "narrateur|Elle n'a pas pris le manteau.",
    "narrateur|Papa ouvre, et l'air pique.",
    "enfant-f|J'ai froid, papa !",
    "narrateur|Elle tire le manteau, trop fort.",
    "narrateur|Le bouton à lune accroche le bois.",
    "enfant-f|Il ne veut pas venir !",
    "narrateur|Son sourire disparaît, net.",
    "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "papa|Le bouton tient le bois, vois.",
    "narrateur|Mila lève le bouton, sans tirer.",
    "maman|Les mains, dans les poches ?",
    "enfant-f|Oui, au chaud.",
    "narrateur|Le panier tape contre le bleu.",
]

T1_CHOICE = [
    "papa|On passe où, avant le marché ?",
    "narrateur|La cuisine.",
    "narrateur|Le jardin.",
    "narrateur|Ou la chambre.",
]

T1 = {
    1: [
        "narrateur|Mila pousse la porte de la cuisine.",
        "narrateur|Les carreaux piquent, un peu froids.",
        "narrateur|Ça sent la menthe, près de l'évier.",
        "narrateur|Une orange roule vers le panier.",
        "enfant-f|Mon manteau me serre, trop chaud.",
        "narrateur|Elle ouvre tous les boutons, trop vite.",
        "narrateur|Le bleu glisse, et tombe près de l'orange.",
        "enfant-f|Je n'en ai plus besoin.",
        "narrateur|La fenêtre envoie un air vif.",
        "enfant-f|J'ai froid, sans lui.",
        "papa|Regarde le bouton, sur le sol.",
        "narrateur|L'entaille en lune brille, minuscule.",
    ],
    2: [
        "narrateur|Mila va vers le jardin, le panier à la main.",
        "narrateur|L'herbe brille, mouillée, sous les bottes.",
        "narrateur|L'air frais touche son nez.",
        "enfant-f|Je cueille la menthe, pour la poche.",
        "narrateur|Elle accroche le manteau au muret.",
        "narrateur|Le vent le pousse vers le mur.",
        "enfant-f|Il s'envole, tout seul !",
        "narrateur|Elle saisit une ombre bleue, vide.",
        "narrateur|C'est l'ombre de la bâche, au loin.",
        "enfant-f|Ce n'était pas lui.",
        "papa|Le toc, entends-tu, contre le muret ?",
        "narrateur|Le bouton à lune répond, minuscule.",
    ],
    3: [
        "narrateur|Mila entre dans la chambre, pressée.",
        "narrateur|Le rideau jaune bouge, près du lit.",
        "enfant-f|J'ai trop chaud, ici.",
        "narrateur|Elle jette le manteau sur la couverture.",
        "narrateur|Elle prend le petit panier jouet.",
        "maman|La fenêtre est ouverte, un peu.",
        "narrateur|L'air vif entre, net.",
        "enfant-f|J'ai froid, maman.",
        "narrateur|Elle saisit la couverture, trop vite.",
        "enfant-f|Ce n'est pas lui, c'est le lit.",
        "papa|Le bouton, vois, sous le drap.",
        "narrateur|L'entaille en lune brille, minuscule.",
    ],
}

T1_Q = {
    1: [
        "narrateur|Mila a froid, près de l'orange.",
        "papa|Elle a repris quoi, pour n'avoir plus froid ?",
    ],
    2: [
        "narrateur|Dans le jardin, le manteau a glissé.",
        "maman|Elle a repris quoi, à la porte ?",
    ],
    3: [
        "narrateur|Le manteau était sous le drap.",
        "papa|Elle a repris quoi, pour n'avoir plus froid ?",
    ],
}

T1_C = {
    1: [
        "narrateur|Mila se baisse vers le tissu bleu.",
        "narrateur|Elle glisse un bras, puis l'autre.",
        "enfant-f|Je le reprends, il est à moi.",
        "maman|Merci, Mila.",
        "narrateur|Elle ferme deux boutons, pas tous.",
        "papa|On emporte un jeu, dans le panier ?",
        "enfant-f|Oui, pour le marché.",
        "narrateur|L'orange attend, ronde, dans le panier.",
        "narrateur|Le col bleu reste sur ses épaules.",
    ],
    2: [
        "narrateur|Mila suit le toc, le long du muret.",
        "narrateur|Elle reprend le manteau, un peu froid.",
        "enfant-f|Je le mets, il est à moi.",
        "maman|Merci, Mila.",
        "narrateur|La menthe glisse dans la poche.",
        "papa|On emporte un jeu, pour le marché ?",
        "enfant-f|Oui, avec moi.",
        "narrateur|Une goutte brille sur l'herbe.",
        "narrateur|Le col bleu revient sur ses épaules.",
    ],
    3: [
        "narrateur|Mila soulève le drap, sans tirer.",
        "narrateur|Elle reprend le manteau, sous le lit.",
        "enfant-f|Je le remets, il est à moi.",
        "papa|Merci, Mila.",
        "narrateur|Le petit panier rentre dans la poche.",
        "maman|On emporte un jeu aussi ?",
        "enfant-f|Oui, maman.",
        "narrateur|Le rideau jaune se tait.",
        "narrateur|Le col bleu revient sur ses épaules.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Près de l'évier, un jeu l'appelle.",
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
            "narrateur|Mila pose les cubes près de l'orange.",
            "narrateur|Ils cliquent, un peu lourds, dans la boîte.",
            "papa|On fait un étal, pour le marché ?",
            "enfant-f|Oui, un étal de cubes.",
            "narrateur|Elle pose le manteau comme une bâche.",
            "narrateur|Un cube tombe, et le bleu glisse.",
            "enfant-f|Il est là, près du panier !",
            "narrateur|Elle saisit l'ombre de l'orange, vide.",
            "enfant-f|Ce n'était pas lui.",
            "narrateur|Ses épaules baissent, un instant.",
            "maman|Le toc, pas l'ombre.",
            "narrateur|Un cube garde un reflet d'orange.",
            "narrateur|Elle suit le toc, lente, et reprend le bleu.",
            "enfant-f|Il est à moi, sur mes épaules.",
        ],
        (1, 2): [
            "narrateur|Mila ouvre le livre, près de l'évier.",
            "narrateur|La couverture montre des oranges.",
            "maman|Comme la caisse, dehors.",
            "enfant-f|Oui, les vraies oranges.",
            "narrateur|Elle glisse le livre sous le manteau.",
            "narrateur|Le bleu et la page se confondent.",
            "enfant-f|Je le prends, il est là !",
            "narrateur|Sa main tient le livre, pas le tissu.",
            "enfant-f|Le manteau a disparu.",
            "narrateur|Ses épaules baissent, près du bol.",
            "papa|Le toc, pas la page.",
            "narrateur|Une miette d'orange reste au bord.",
            "narrateur|Elle suit le toc, lente, et reprend le bleu.",
            "enfant-f|Il est à moi, sur mes épaules.",
        ],
        (1, 3): [
            "narrateur|Mila sort la dînette, près du bol.",
            "narrateur|Une petite tasse sonne, creuse.",
            "papa|On sert le marché ?",
            "enfant-f|Oui, un thé de menthe.",
            "narrateur|Elle étale le manteau, comme une nappe.",
            "narrateur|La tasse penche, et le bleu glisse.",
            "enfant-f|Il est là, sous la tasse !",
            "narrateur|Elle saisit un torchon bleu, vide.",
            "enfant-f|Ce n'était pas lui.",
            "narrateur|Ses épaules baissent, près de l'évier.",
            "maman|Le toc, pas le torchon.",
            "narrateur|La petite casserole reste près du bol.",
            "narrateur|Elle suit le toc, lente, et reprend le bleu.",
            "enfant-f|Il est à moi, sur mes épaules.",
        ],
        (2, 1): [
            "narrateur|Mila pose les cubes dans l'herbe.",
            "narrateur|Un cube sent le pin, un peu.",
            "papa|On fait un étal, dehors ?",
            "enfant-f|Oui, un étal de cubes.",
            "narrateur|Elle pose le manteau sur le muret.",
            "narrateur|Le vent le pousse, et un cube roule.",
            "enfant-f|Il est là, contre le mur !",
            "narrateur|Elle saisit l'ombre de la bâche, vide.",
            "enfant-f|Ce n'était pas lui.",
            "narrateur|Ses épaules baissent, dans l'herbe.",
            "maman|Le toc, pas l'ombre.",
            "narrateur|L'herbe tache un cube, tout vert.",
            "narrateur|Elle suit le toc, lente, et reprend le bleu.",
            "enfant-f|Il est à moi, sur mes épaules.",
        ],
        (2, 2): [
            "narrateur|Mila ouvre le livre, près du muret.",
            "narrateur|Une page sent le papier, frais.",
            "maman|On le regardera près des étals.",
            "enfant-f|Oui, avec les vraies oranges.",
            "narrateur|Elle pose le livre sur le manteau.",
            "narrateur|Le vent tourne une page, trop vite.",
            "enfant-f|Le bleu est sous la page !",
            "narrateur|Sa main tient le livre, pas le tissu.",
            "enfant-f|Le manteau a disparu.",
            "narrateur|Ses épaules baissent, près du muret.",
            "papa|Le toc, pas la page.",
            "narrateur|Une feuille de menthe sert de marque-page.",
            "narrateur|Elle suit le toc, lente, et reprend le bleu.",
            "enfant-f|Il est à moi, sur mes épaules.",
        ],
        (2, 3): [
            "narrateur|Mila pose la dînette dans l'herbe.",
            "narrateur|Une petite assiette sonne, légère.",
            "papa|On sert un thé, dehors ?",
            "enfant-f|Oui, un thé de menthe.",
            "narrateur|Elle étale le manteau, comme une nappe.",
            "narrateur|Une goutte perle au bord de l'assiette.",
            "enfant-f|Il est là, sous l'assiette !",
            "narrateur|Elle saisit une feuille bleue, vide.",
            "enfant-f|Ce n'était pas lui.",
            "narrateur|Ses épaules baissent, près du muret.",
            "maman|Le toc, pas la feuille.",
            "narrateur|La petite tasse reste froide, dans l'herbe.",
            "narrateur|Elle suit le toc, lente, et reprend le bleu.",
            "enfant-f|Il est à moi, sur mes épaules.",
        ],
        (3, 1): [
            "narrateur|Mila pose les cubes près du lit.",
            "narrateur|Un cube tapote le parquet, net.",
            "papa|On fait un étal, ici ?",
            "enfant-f|Oui, un étal de cubes.",
            "narrateur|Elle pose le manteau sur l'oreiller.",
            "narrateur|Un cube roule, et le bleu glisse.",
            "enfant-f|Il est là, sous l'oreiller !",
            "narrateur|Elle saisit le drap bleu, vide.",
            "enfant-f|Ce n'était pas lui.",
            "narrateur|Ses épaules baissent, près du lit.",
            "maman|Le toc, pas le drap.",
            "narrateur|Un cube tapote le parquet, plus loin.",
            "narrateur|Elle suit le toc, lente, et reprend le bleu.",
            "enfant-f|Il est à moi, sur mes épaules.",
        ],
        (3, 2): [
            "narrateur|Mila ouvre le livre, sur le lit.",
            "narrateur|Le rideau jaune colore la page.",
            "maman|On le regardera près des étals.",
            "enfant-f|Oui, avec les vraies oranges.",
            "narrateur|Elle glisse le livre sous le manteau.",
            "narrateur|Le bleu et le rideau se confondent.",
            "enfant-f|Il est là, près de la fenêtre !",
            "narrateur|Sa main tient le rideau, pas le tissu.",
            "enfant-f|Le manteau a disparu.",
            "narrateur|Ses épaules baissent, près du lit.",
            "papa|Le toc, pas le rideau.",
            "narrateur|Une page se recourbe, sur la couverture.",
            "narrateur|Elle suit le toc, lente, et reprend le bleu.",
            "enfant-f|Il est à moi, sur mes épaules.",
        ],
        (3, 3): [
            "narrateur|Mila pose la dînette près du lit.",
            "narrateur|Une petite tasse sonne, creuse.",
            "papa|On sert un thé, ici ?",
            "enfant-f|Oui, un thé de menthe.",
            "narrateur|Elle étale le manteau, comme une nappe.",
            "narrateur|La tasse penche, et le bleu glisse.",
            "enfant-f|Il est là, sous la tasse !",
            "narrateur|Elle saisit le tapis bleu, vide.",
            "enfant-f|Ce n'était pas lui.",
            "narrateur|Ses épaules baissent, près du lit.",
            "maman|Le toc, pas le tapis.",
            "narrateur|La petite tasse reste près du panier jouet.",
            "narrateur|Elle suit le toc, lente, et reprend le bleu.",
            "enfant-f|Il est à moi, sur mes épaules.",
        ],
    }
    return table[(a, b)]


T3_CHOICE = {
    1: [
        "papa|C'est quel moment, pour le marché ?",
        "narrateur|Le matin.",
        "narrateur|Après la sieste.",
        "narrateur|Ou le soir.",
    ],
    2: [
        "maman|C'est quel moment, pour le marché ?",
        "narrateur|Le matin.",
        "narrateur|Après la sieste.",
        "narrateur|Ou le soir.",
    ],
    3: [
        "papa|C'est quel moment, pour le marché ?",
        "narrateur|Le matin.",
        "narrateur|Après la sieste.",
        "narrateur|Ou le soir.",
    ],
}

TRACE_AB = {
    (1, 1): "Un cube attrape un reflet d'orange, au stand.",
    (1, 2): "Une miette d'orange reste au bord de la page.",
    (1, 3): "La petite casserole est près du vrai bol, dehors.",
    (2, 1): "L'herbe tache un cube, tout vert, au stand.",
    (2, 2): "Une vraie feuille de menthe marque la page.",
    (2, 3): "Une goutte perle au bord de l'assiette, dehors.",
    (3, 1): "Un cube tapote le parquet, dans sa mémoire.",
    (3, 2): "Le rideau jaune colore la page, au stand.",
    (3, 3): "La petite tasse est près du lit, dans sa poche.",
}

GAME_BC = {
    (1, 1): "Je pose un cube, près de la caisse froide.",
    (1, 2): "Je pose un cube, près de la chaise tiède.",
    (1, 3): "Je pose un cube, près de la caisse des lampes.",
    (2, 1): "J'ouvre le livre, près des oranges froides.",
    (2, 2): "J'ouvre le livre, près des oranges tièdes.",
    (2, 3): "J'ouvre le livre, sous les lampes du stand.",
    (3, 1): "Je pose une tasse, près de la caisse froide.",
    (3, 2): "Je pose une tasse, près de la chaise tiède.",
    (3, 3): "Je pose une tasse, sous les lampes du stand.",
}

PLACE_AC = {
    (1, 1): "Un froid de carreaux reste sous ses chaussons.",
    (1, 2): "L'odeur de menthe de l'évier la suit.",
    (1, 3): "Le col ouvert lui tient chaud, dehors.",
    (2, 1): "Les bottes font ploc, sur les pavés froids.",
    (2, 2): "La menthe de la poche sent fort, tout vert.",
    (2, 3): "Une goutte du jardin glisse du manteau bleu.",
    (3, 1): "Le petit panier jouet tapote la caisse.",
    (3, 2): "Le rideau jaune reste derrière, à la maison.",
    (3, 3): "Le savon de la chambre reste sur le col.",
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    cores = {
        1: [
            "papa|Le marché s'ouvre, ce matin.",
            "narrateur|Ils sortent, et l'air pique le nez.",
            "narrateur|Mila pose le manteau sur une caisse.",
            "enfant-f|J'en prends une, vite !",
            "narrateur|La bâche se déroule, et recouvre le bleu.",
            "enfant-f|Il est sous la bâche, je le vois !",
            "narrateur|Elle saisit un pan rayé, trop vite.",
            "narrateur|Cette fois, elle refuse de foncer.",
            "narrateur|Le bouton à lune fait toc, sous la bâche.",
            "enfant-f|L'entaille, je la vois.",
            "narrateur|Elle soulève le pan, sans tirer.",
            "papa|Une orange, pour le panier.",
            "narrateur|Mila la choisit, toute ronde.",
        ],
        2: [
            "papa|Le marché est plus calme, après la sieste.",
            "narrateur|Ils sortent, et les pavés sont tièdes.",
            "narrateur|Mila pose le manteau sur une chaise.",
            "enfant-f|J'en prends une, tiède !",
            "narrateur|Un sac bleu pend, à côté de la chaise.",
            "enfant-f|Il est là, je le vois !",
            "narrateur|Elle saisit le sac, trop vite.",
            "narrateur|Cette fois, elle refuse de foncer.",
            "narrateur|Le bouton à lune fait toc, sous le store.",
            "enfant-f|L'entaille, je la vois.",
            "narrateur|Elle soulève le col, sans tirer.",
            "papa|Une orange, pour le panier.",
            "narrateur|Mila la choisit, un peu chaude.",
        ],
        3: [
            "papa|Le marché se range, ce soir.",
            "narrateur|Ils sortent, et la vitre est bleue.",
            "narrateur|Mila pose le manteau près de la caisse.",
            "enfant-f|J'en prends une, avant le pli !",
            "narrateur|La bâche se plie, et avale le bleu.",
            "enfant-f|Il est dans le pli, je le vois !",
            "narrateur|Elle tire le pli, trop vite.",
            "narrateur|Cette fois, elle refuse de foncer.",
            "narrateur|Le bouton à lune fait toc, dans la bâche.",
            "enfant-f|L'entaille, je la vois.",
            "narrateur|Elle soulève le pli, sans tirer.",
            "papa|Une orange, pour le panier.",
            "narrateur|Mila la choisit, parfumée.",
        ],
    }[c]
    return cores + [
        f"enfant-f|{GAME_BC[(b, c)]}",
        f"narrateur|{PLACE_AC[(a, c)]}",
        f"narrateur|{TRACE_AB[(a, b)]}",
    ]


LASTS = {
    (1, 1, 1): "Un cube garde un reflet d'orange, au crochet.",
    (1, 1, 2): "Un cube sent la casserole, près du bol.",
    (1, 1, 3): "L'ombre d'un cube danse sur le carrelage.",
    (1, 2, 1): "Une page sent la menthe, près du bol.",
    (1, 2, 2): "Le livre est tiède, près de la vitre.",
    (1, 2, 3): "La lampe dore le bord d'une page.",
    (1, 3, 1): "Une petite tasse a une goutte de menthe.",
    (1, 3, 2): "La dînette est chaude, comme la cuisine.",
    (1, 3, 3): "La petite cuillère brille sous la lampe.",
    (2, 1, 1): "Un cube a une goutte d'herbe.",
    (2, 1, 2): "Le cube sèche au soleil, tout vert.",
    (2, 1, 3): "Un cube garde une goutte, toute ronde.",
    (2, 2, 1): "Une vraie feuille de menthe marque la page.",
    (2, 2, 2): "Le livre sent l'herbe mouillée.",
    (2, 2, 3): "Un oiseau se tait, près du livre.",
    (2, 3, 1): "Une petite assiette a de la rosée.",
    (2, 3, 2): "La dînette est tiède, au soleil.",
    (2, 3, 3): "Loin de la dînette, une goutte tombe.",
    (3, 1, 1): "Un rayon pose sur la tour de cubes.",
    (3, 1, 2): "Un cube est contre l'oreiller, silencieux.",
    (3, 1, 3): "L'ombre des cubes danse sur le mur.",
    (3, 2, 1): "Le rideau jaune colore la page.",
    (3, 2, 2): "Le livre est ouvert sur la couverture.",
    (3, 2, 3): "La page sent le savon, un peu.",
    (3, 3, 1): "Une tasse miniature est près du lit.",
    (3, 3, 2): "La dînette attend au pied du lit.",
    (3, 3, 3): "Une petite assiette reflète la veilleuse.",
}

FINS = {
    (1, 1, 1): "L'orange reste dans le panier, près des cubes.",
    (1, 1, 2): "La casserole fait un tout petit pschitt.",
    (1, 1, 3): "Une miette d'orange reste sur la table.",
    (1, 2, 1): "Un oiseau chante, très loin.",
    (1, 2, 2): "La page se recourbe, près du bol.",
    (1, 2, 3): "La lampe dore le livre fermé.",
    (1, 3, 1): "La petite tasse sèche près de l'évier.",
    (1, 3, 2): "La menthe sent, près du sol.",
    (1, 3, 3): "Le bouton du manteau brille, au crochet.",
    (2, 1, 1): "Les bottes sèchent près de la porte.",
    (2, 1, 2): "L'herbe colle à un cube.",
    (2, 1, 3): "Une goutte glisse du manteau bleu.",
    (2, 2, 1): "Une feuille de menthe reste dans le livre.",
    (2, 2, 2): "Le jardin est pâle, derrière la vitre.",
    (2, 2, 3): "La flaque ne brille plus, dehors.",
    (2, 3, 1): "La petite assiette a de l'herbe.",
    (2, 3, 2): "Les bottes font un dernier ploc.",
    (2, 3, 3): "Le col bleu sèche, au crochet.",
    (3, 1, 1): "Le petit panier repose sur un cube.",
    (3, 1, 2): "L'oreiller sent le savon.",
    (3, 1, 3): "Le rideau jaune ne bouge plus.",
    (3, 2, 1): "Le petit panier sèche sur la couverture.",
    (3, 2, 2): "Une page reste ouverte, sur le lit.",
    (3, 2, 3): "La veilleuse dore le livre.",
    (3, 3, 1): "La petite tasse est près du panier jouet.",
    (3, 3, 2): "Le tapis de la chambre se tait.",
    (3, 3, 3): "Le crochet de bois attend demain.",
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
        "narrateur|Le bouton à lune fait toc, contre le bois.",
        "enfant-f|Il sèche, là.",
        f"narrateur|Mila est passée par {loc}.",
        f"narrateur|Elle a emporté {jeu}.",
        f"narrateur|C'était {mom}.",
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

    put("CHK_T0000_P0000", OPENING, "opening", "marche,porte,manteau")
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
                    {"emphasis": "bouton"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "crochet,manteau",
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
        "Le seuil tient l'ombre du panier. La bâche rayée claque. "
        "Mila veut une orange avant que le stand plie. Elle court sans "
        "le manteau bleu : l'air pique. Elle tire trop fort, le bouton "
        "à lune accroche le crochet. Cuisine, jardin ou chambre, le bleu "
        "glisse. Elle le reprend. Cubes, livre ou dînette : une ombre bleue "
        "ment, le toc dit vrai. Matin, sieste ou soir, sous la bâche, "
        "elle refuse de foncer. L'entaille paie le début. L'orange rentre."
    )
    merged["title"] = TITLE
    merged["characters"] = "Mila, papa, maman"
    merged["setting"] = "maison près du marché, puis le marché"
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
        "Réécriture éditoriale F-NAR-019. Graphe, `chunk_id`, types de blocs "
        "et destinations techniques inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le seuil tient l'ombre ovale du panier. Au loin, la bâche rayée "
        "claque. Sur le crochet, un manteau bleu attend : le bouton du bas "
        "a une entaille en lune, et fait toc contre le bois. Mila veut une "
        "orange avant que le stand plie. Elle court sans le manteau : l'air "
        "pique. Elle tire trop fort, le bouton accroche. Cuisine, jardin ou "
        "chambre, le bleu glisse. Elle le reprend. Cubes, livre ou dînette : "
        "une ombre bleue ment. Matin, sieste ou soir, sous la bâche, elle "
        "refuse de foncer. Le toc paie le début. L'orange rentre. Le manteau "
        "garde une trace.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : maison près du marché, crochet de bois, bâche rayée, oranges.\n"
        "- Désir : rapporter une orange avant que la bâche se plie.\n"
        "- Objet : manteau bleu (bouton à lune, toc), plus cubes / livre / dînette.\n"
        "- Urgence douce : le stand va plier.\n"
        "- Imprévu 1 : partir sans manteau, tirer, le bouton accroche ; le bleu glisse.\n"
        "- Cue : lever le bouton, sans tirer. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : une ombre bleue, un sac, un pli de bâche mentent.\n"
        "- Résolution : refuser de foncer, écouter le toc, retrouver l'entaille.\n"
        "- Retour : toc au crochet, orange, 27 traces distinctes.\n\n"
        "## Corrections éditoriales\n\n"
        "- Le premier choix n'enlève pas le manteau : il vient en cuisine, au jardin, en chambre.\n"
        "- Revers allongé : froid, glissade, ombre fausse, bâche, geste lent.\n"
        "- Neuf disparitions distinctes, vingt-sept résolutions, vingt-sept fins.\n"
        "- Leçon AUT.AFF.002 vécue (reprendre le manteau), jamais dite.\n"
        "- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Troupe D16 : Mila, papa, maman.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js.\n\n"
        "## Direction vocale\n\n"
        "Impatience au départ, petit découragement quand le manteau résiste "
        "ou disparaît, fierté calme quand Mila écoute le toc. "
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
