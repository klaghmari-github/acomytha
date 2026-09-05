#!/usr/bin/env python3
"""TREE-AUT-047 — Le manteau de Raphaël près des bottes (F-NAR-019, N2)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-047"
N2 = LIMITS["N2"]
TITLE = "Le manteau de Raphaël près des bottes"
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
    "étoile brune",
    "fil pâle",
    "bouton de nacre",
    "nœud de raphia",
    "dent de laitue",
    "bracelet d'écorce",
    "écaille d'étain",
    "écaille de lichen",
    "écaille de nacre",
    "casserole",
    "gouttière",
    "manteau vert",
    "manteau jaune",
    "manteau à pois",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="écaille de boue blonde",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=l_ecaille_tient_au_cuir; "
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
        emphasis="manteau",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=le_bleu_part_avec_lui; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="manteau",
        note=(
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=le_tissu_tient_contre_lui; "
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
            "destinataire=enfant; sous_texte=le_froid_rappelle_le_bleu; "
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
            "intensite=2; destinataire=enfant; sous_texte=un_faux_bleu_ment_l_ecaille_dit_vrai; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="écaille de boue blonde",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=il_accroche_sans_foncer; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="écaille de boue blonde",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=l_ecaille_et_les_bottes_paient_le_début; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

LIEU = {
    1: dict(lab="la cuisine", ou="dans la cuisine", short="cuisine", sons="porte,carrelage"),
    2: dict(lab="le jardin", ou="dans le jardin", short="jardin", sons="herbe,porte"),
    3: dict(lab="la chambre", ou="dans la chambre", short="chambre", sons="rideau,plancher"),
}
JEU = {
    1: dict(lab="les cubes", un="un cube", le="le cube", short="cubes", sons="cubes,bois"),
    2: dict(lab="le livre", un="le livre", le="le livre", short="livre", sons="page,livre"),
    3: dict(lab="la dînette", un="une tasse", le="la tasse", short="dînette", sons="tasse,dinette"),
}
MOM = {
    1: dict(lab="le matin", quand="le matin", short="matin", sons="cloche,bottes"),
    2: dict(lab="après la sieste", quand="après la sieste", short="sieste", sons="oreiller,bottes"),
    3: dict(lab="le soir", quand="le soir", short="soir", sons="lampe,portemanteau"),
}

Q_FIELDS = {
    1: {
        "expected_answer": "manteau",
        "accepted_examples": "manteau | le manteau | son manteau | le manteau bleu",
        "retry_prompt": "Le manteau bleu. Il a pris quoi ?",
    },
    2: {
        "expected_answer": "manteau",
        "accepted_examples": "manteau | le manteau | son manteau | le manteau bleu",
        "retry_prompt": "Le manteau bleu. Raphaël a pris quoi ?",
    },
    3: {
        "expected_answer": "manteau",
        "accepted_examples": "manteau | le manteau | son manteau | le manteau bleu",
        "retry_prompt": "Le manteau bleu. Il a pris quoi, en bas ?",
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


# Ouverture inventée : les clés, puis les bottes. Indice = écaille de boue blonde.
OPENING = [
    "narrateur|Les clés de papa tombent dans la coupelle.",
    "narrateur|Ça fait un petit choc, près de la porte.",
    "narrateur|Raphaël lève les yeux, vers les bottes jaunes.",
    "narrateur|Le paillasson est mouillé, sombre au milieu.",
    "narrateur|Sur le cuir gauche, une écaille de boue blonde tient.",
    "narrateur|Elle est plate, un peu sèche au bord.",
    "narrateur|Le portemanteau de bois penche, vers les bottes.",
    "narrateur|Un manteau bleu attend, un peu lourd.",
    "maman|Tu as vu les bottes, Raphaël ?",
    "enfant-m|Je sors, maintenant !",
    "papa|Tes bottes sont prêtes.",
    "narrateur|En ce moment, Raphaël enfile une botte.",
    "narrateur|Il tire trop vite, vers la porte.",
    "narrateur|L'air froid lui prend les bras.",
    "enfant-m|J'ai froid, papa !",
    "narrateur|Le sourire de Raphaël disparaît.",
    "narrateur|Dans sa poitrine, ça serre, fort.",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "papa|Le manteau, il est où ?",
    "enfant-m|Près des bottes, je le prends !",
]

T1_CHOICE = [
    "narrateur|Le manteau peut partir, avec lui.",
    "papa|On passe où, d'abord ?",
    "maman|La cuisine, le jardin, ou la chambre ?",
]

T1 = {
    1: [
        "narrateur|Raphaël pousse la porte de la cuisine.",
        "narrateur|Le carrelage pique, sous les bottes jaunes.",
        "enfant-m|Je joue ici, tout de suite !",
        "narrateur|Il avance trop vite, sans le manteau.",
        "narrateur|Un filet d'air glisse sur ses bras.",
        "enfant-m|J'ai froid !",
        "narrateur|Le sourire de Raphaël disparaît.",
        "narrateur|Dans sa poitrine, ça serre, fort.",
        "narrateur|Papa s'accroupit, près du carrelage.",
        "papa|Tes bras, ils disent quoi ?",
        "enfant-m|Ils veulent le bleu.",
        "narrateur|Raphaël revient vers l'entrée.",
        "narrateur|Il prend le manteau, près des bottes.",
        "narrateur|Il glisse un bras, puis l'autre.",
        "narrateur|La fermeture fait un petit tic.",
        "enfant-m|Il vient avec moi.",
        "maman|L'écaille de boue blonde reste à la botte ?",
    ],
    2: [
        "narrateur|Raphaël ouvre vers le jardin.",
        "narrateur|L'herbe mouille le bas des bottes.",
        "enfant-m|Je sors, maman !",
        "narrateur|Il pose un pied, trop vite, sans le bleu.",
        "narrateur|L'air vif lui pique les bras.",
        "enfant-m|Mes bras sont froids !",
        "narrateur|Le sourire de Raphaël disparaît.",
        "narrateur|L'envie et l'inquiétude se bousculent.",
        "narrateur|Maman s'accroupit, sur le seuil.",
        "maman|Tes bras, ils disent quoi ?",
        "enfant-m|Ils veulent le manteau.",
        "narrateur|Raphaël rentre d'un pas.",
        "narrateur|Il prend le manteau, près des bottes.",
        "narrateur|Il glisse un bras, puis l'autre.",
        "narrateur|Le col chatouille le menton.",
        "enfant-m|Il vient avec moi.",
        "papa|L'écaille de boue blonde reste au cuir ?",
    ],
    3: [
        "narrateur|Raphaël monte vers la chambre.",
        "narrateur|Le plancher fait un petit cri.",
        "enfant-m|J'ouvre la fenêtre, un peu !",
        "narrateur|Le rideau se soulève, trop vite.",
        "narrateur|L'air froid entre, net, sans le bleu.",
        "enfant-m|J'ai froid aux bras !",
        "narrateur|Le sourire de Raphaël disparaît.",
        "narrateur|Ses épaules baissent, près du lit.",
        "narrateur|Papa s'accroupit, à sa hauteur.",
        "papa|Tes bras, ils disent quoi ?",
        "enfant-m|Ils veulent le manteau.",
        "narrateur|Raphaël redescend l'escalier.",
        "narrateur|Il prend le manteau, près des bottes.",
        "narrateur|Il glisse un bras, puis l'autre.",
        "narrateur|La fermeture fait un petit tic.",
        "enfant-m|Il vient avec moi.",
        "maman|L'écaille de boue blonde reste en bas ?",
    ],
}

T1_Q = {
    1: [
        "narrateur|Raphaël n'a plus froid aux bras.",
        "papa|Il a pris quoi, près des bottes ?",
    ],
    2: [
        "narrateur|L'air ne pique plus les bras.",
        "maman|Raphaël a pris quoi ?",
    ],
    3: [
        "narrateur|Les bras sont au chaud, contre le bleu.",
        "papa|Raphaël a pris quoi, en bas ?",
    ],
}

T1_C = {
    1: [
        "narrateur|Le manteau bleu est sur lui.",
        "enfant-m|Il vient, jusqu'au jeu.",
        "papa|Merci, Raphaël, tu l'as pris.",
        "maman|On emporte un jeu, maintenant ?",
        "narrateur|La fermeture tient, contre le bleu.",
        "narrateur|L'écaille de boue blonde reste au cuir.",
        "narrateur|Les bottes attendent, sur le paillasson.",
        "enfant-m|Le carrelage peut attendre, un peu.",
    ],
    2: [
        "narrateur|Le manteau bleu est sur lui.",
        "enfant-m|Il vient, jusqu'à l'herbe.",
        "maman|Merci, Raphaël, tu l'as pris.",
        "papa|On emporte un jeu, pour le jardin ?",
        "narrateur|Le col tient, contre le menton.",
        "narrateur|L'écaille de boue blonde reste au cuir.",
        "narrateur|Une feuille tremble, collée à la botte.",
        "enfant-m|L'herbe peut attendre, un peu.",
    ],
    3: [
        "narrateur|Le manteau bleu est sur lui.",
        "enfant-m|Il vient, jusqu'au lit.",
        "papa|Merci, Raphaël, tu l'as pris.",
        "maman|On emporte un jeu, de la chambre ?",
        "narrateur|Le tissu se réchauffe, contre lui.",
        "narrateur|L'écaille de boue blonde reste au cuir.",
        "narrateur|Le portemanteau reste vide, un moment.",
        "enfant-m|Le rideau peut attendre, un peu.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Un jeu veut voyager, avec le bleu.",
        "papa|Les cubes, le livre, ou la dînette ?",
        "maman|Le manteau vient avec toi.",
    ],
    2: [
        "narrateur|Un jeu cherche une place, contre le bleu.",
        "maman|Les cubes, le livre, ou la dînette ?",
        "papa|Le manteau vient avec toi.",
    ],
    3: [
        "narrateur|Un jeu veut entrer, sous le bras.",
        "papa|Les cubes, le livre, ou la dînette ?",
        "maman|Le manteau vient avec toi.",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    table = {
        (1, 1): [
            "narrateur|Raphaël pose les cubes, sur le carrelage.",
            "narrateur|Un cube claque contre un autre.",
            "enfant-m|Une tour, tout de suite !",
            "narrateur|Le manteau bleu frotte la table.",
            "narrateur|La manche accroche un cube, trop large.",
            "enfant-m|Il me gêne !",
            "narrateur|Il jette le bleu, trop vite.",
            "narrateur|Un bol bleu attend, près de l'évier.",
            "enfant-m|Mon manteau !",
            "narrateur|Il saisit le bol, trop vite.",
            "narrateur|Ce n'est pas le manteau, c'est le bol.",
            "enfant-m|Il a disparu.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "papa|Regarde le tic, pas le bleu.",
            "maman|Personne ne dit où courir.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le manteau reste contre lui, un peu froissé.",
        ],
        (1, 2): [
            "narrateur|Raphaël ouvre le livre, sur la table.",
            "narrateur|Une page sent le pain, tout près.",
            "enfant-m|L'histoire, tout de suite !",
            "narrateur|Le manteau bleu cache un coin de page.",
            "narrateur|La manche glisse, trop large.",
            "enfant-m|Il me gêne !",
            "narrateur|Il pose le bleu, trop vite.",
            "narrateur|Un torchon bleu attend, plié.",
            "enfant-m|Mon manteau !",
            "narrateur|Il saisit le torchon, trop vite.",
            "narrateur|Ce n'est pas le manteau, c'est le linge.",
            "enfant-m|Il s'est caché.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "maman|Regarde le tic, pas le bleu.",
            "papa|Personne ne donne la réponse.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le livre garde un pli, contre le tissu.",
        ],
        (1, 3): [
            "narrateur|Raphaël soulève le panier de dînette.",
            "narrateur|Une tasse minuscule fait ting.",
            "enfant-m|Un thé, tout de suite !",
            "narrateur|Le manteau bleu fait un pli au coude.",
            "narrateur|La manche accroche l'osier, trop large.",
            "enfant-m|Il me gêne !",
            "narrateur|Il jette le bleu, trop vite.",
            "narrateur|Une serviette bleue attend, près du bol.",
            "enfant-m|Mon manteau !",
            "narrateur|Il saisit la serviette, trop vite.",
            "narrateur|Ce n'est pas le manteau, c'est le linge.",
            "enfant-m|Il a disparu.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "papa|Regarde le tic, pas le bleu.",
            "maman|Personne ne dit où chercher.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|La tasse reste dans sa main, contre le bleu.",
        ],
        (2, 1): [
            "narrateur|Raphaël pose les cubes, dans l'herbe.",
            "narrateur|Un cube brille, mouillé d'une goutte.",
            "enfant-m|Une tour, dehors !",
            "narrateur|Le manteau bleu frotte le rebord.",
            "narrateur|La manche accroche un cube, trop large.",
            "enfant-m|Il me gêne !",
            "narrateur|Il jette le bleu, trop vite.",
            "narrateur|Un arrosoir bleu attend, près des bottes du jardin.",
            "enfant-m|Mon manteau !",
            "narrateur|Il saisit l'arrosoir, trop vite.",
            "narrateur|Ce n'est pas le manteau, c'est le zinc.",
            "enfant-m|Il s'est caché.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "maman|Regarde le tic, pas le bleu.",
            "papa|Personne ne dit où courir.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|L'écaille de boue blonde reste au cuir, loin.",
        ],
        (2, 2): [
            "narrateur|Raphaël ouvre le livre, sur la marche.",
            "narrateur|Une page prend un peu d'herbe.",
            "enfant-m|L'histoire, dehors !",
            "narrateur|Le manteau bleu cache un coin de page.",
            "narrateur|La manche glisse, trop large.",
            "enfant-m|Il me gêne !",
            "narrateur|Il pose le bleu, trop vite.",
            "narrateur|Un seau bleu attend, près de l'herbe.",
            "enfant-m|Mon manteau !",
            "narrateur|Il saisit le seau, trop vite.",
            "narrateur|Ce n'est pas le manteau, c'est le seau.",
            "enfant-m|Il a disparu.",
            "narrateur|Ses épaules baissent, près de la marche.",
            "papa|Regarde le tic, pas le bleu.",
            "maman|Personne ne donne la réponse.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Une feuille tremble, collée à la botte.",
        ],
        (2, 3): [
            "narrateur|Raphaël pose la dînette, dans l'herbe.",
            "narrateur|L'osier pique un peu les doigts.",
            "enfant-m|Un thé, dehors !",
            "narrateur|Le manteau bleu fait un pli au coude.",
            "narrateur|La manche accroche l'osier, trop large.",
            "enfant-m|Il me gêne !",
            "narrateur|Il jette le bleu, trop vite.",
            "narrateur|Un gant bleu sèche, près de l'arrosoir.",
            "enfant-m|Mon manteau !",
            "narrateur|Il saisit le gant, trop vite.",
            "narrateur|Ce n'est pas le manteau, c'est le gant.",
            "enfant-m|Il s'est caché.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "maman|Regarde le tic, pas le bleu.",
            "papa|Personne ne dit où chercher.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|La petite cuillère brille, contre le bleu.",
        ],
        (3, 1): [
            "narrateur|Raphaël pose les cubes, sur le tapis.",
            "narrateur|Un cube tapote le parquet.",
            "enfant-m|Une tour, près du lit !",
            "narrateur|Le manteau bleu frotte la couverture.",
            "narrateur|La manche accroche un cube, trop large.",
            "enfant-m|Il me gêne !",
            "narrateur|Il jette le bleu, trop vite.",
            "narrateur|Un pyjama bleu attend, sur le coffre.",
            "enfant-m|Mon manteau !",
            "narrateur|Il saisit le pyjama, trop vite.",
            "narrateur|Ce n'est pas le manteau, c'est le linge.",
            "enfant-m|Il a disparu.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "papa|Regarde le tic, pas le bleu.",
            "maman|Personne ne dit où courir.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le rideau touche son épaule, un instant.",
        ],
        (3, 2): [
            "narrateur|Raphaël ouvre le livre, près de l'oreiller.",
            "narrateur|Le rideau colore un peu la page.",
            "enfant-m|L'histoire, sur le lit !",
            "narrateur|Le manteau bleu cache un coin de page.",
            "narrateur|La manche glisse, trop large.",
            "enfant-m|Il me gêne !",
            "narrateur|Il pose le bleu, trop vite.",
            "narrateur|Un coussin bleu attend, rond et mou.",
            "enfant-m|Mon manteau !",
            "narrateur|Il saisit le coussin, trop vite.",
            "narrateur|Ce n'est pas le manteau, c'est le coussin.",
            "enfant-m|Il s'est caché.",
            "narrateur|Ses épaules baissent, près du lit.",
            "maman|Regarde le tic, pas le bleu.",
            "papa|Personne ne donne la réponse.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Une page se recourbe, contre le tissu.",
        ],
        (3, 3): [
            "narrateur|Raphaël pose la dînette, au pied du lit.",
            "narrateur|Une petite tasse est près du doudou.",
            "enfant-m|Un thé, ici !",
            "narrateur|Le manteau bleu fait un pli au coude.",
            "narrateur|La manche accroche l'osier, trop large.",
            "enfant-m|Il me gêne !",
            "narrateur|Il jette le bleu, trop vite.",
            "narrateur|Le rideau bleu attend, près de la fenêtre.",
            "enfant-m|Mon manteau !",
            "narrateur|Il saisit le rideau, trop vite.",
            "narrateur|Ce n'est pas le manteau, c'est le tissu du jour.",
            "enfant-m|Il a disparu.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Regarde le tic, pas le bleu.",
            "maman|Personne ne dit où chercher.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|La petite assiette reste dans l'autre main.",
        ],
    }
    return table[(a, b)]


T3_CHOICE = {
    1: [
        "narrateur|Le manteau veut rentrer, vers les bottes.",
        "papa|C'est quel moment, pour poser le bleu ?",
        "maman|Le matin, après la sieste, ou le soir ?",
    ],
    2: [
        "narrateur|Le manteau cherche sa place, près des bottes.",
        "maman|C'est quel moment, pour poser le bleu ?",
        "papa|Le matin, après la sieste, ou le soir ?",
    ],
    3: [
        "narrateur|Le manteau veut sa place, au bois.",
        "papa|C'est quel moment, pour poser le bleu ?",
        "maman|Le matin, après la sieste, ou le soir ?",
    ],
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    time = {
        1: [
            "narrateur|Le matin, la lumière est pâle, un peu bleue.",
            "narrateur|Une cloche de vélo tinte, très loin.",
        ],
        2: [
            "narrateur|Après la sieste, les joues de Raphaël sont chaudes.",
            "narrateur|L'air de l'entrée est tiède, un peu lourd.",
        ],
        3: [
            "narrateur|Le soir, la lampe de l'entrée est ronde.",
            "narrateur|L'horloge fait un tic, très loin.",
        ],
    }[c]
    arrive = {
        (1, 1): [
            "narrateur|Sous le bras, un cube appuie le bleu.",
            "enfant-m|Je rentre, avec les cubes.",
        ],
        (1, 2): [
            "narrateur|Sous le bras, le livre appuie le bleu.",
            "enfant-m|Je rentre, avec le livre.",
        ],
        (1, 3): [
            "narrateur|Sous le bras, la tasse appuie le bleu.",
            "enfant-m|Je rentre, avec la dînette.",
        ],
        (2, 1): [
            "narrateur|Dans l'herbe du seuil, un cube brille.",
            "enfant-m|Je rentre, avec les cubes.",
        ],
        (2, 2): [
            "narrateur|Sur la marche, le livre sent l'herbe.",
            "enfant-m|Je rentre, avec le livre.",
        ],
        (2, 3): [
            "narrateur|Près du seuil, la tasse sent l'herbe.",
            "enfant-m|Je rentre, avec la dînette.",
        ],
        (3, 1): [
            "narrateur|Sur le tapis du seuil, un cube tapote.",
            "enfant-m|Je rentre, avec les cubes.",
        ],
        (3, 2): [
            "narrateur|Près des clés, le livre reste ouvert.",
            "enfant-m|Je rentre, avec le livre.",
        ],
        (3, 3): [
            "narrateur|Près de la coupelle, la tasse fait ting.",
            "enfant-m|Je rentre, avec la dînette.",
        ],
    }[(a, b)]
    ruse = {
        1: [
            "narrateur|Une chaise attend, dans la lumière pâle.",
            "enfant-m|Le manteau, il est posé !",
            "narrateur|Il jette le bleu, sur la chaise.",
            "narrateur|Ce n'est pas le crochet, c'est le bois.",
        ],
        2: [
            "narrateur|Le manteau glisse, et ressemble à une couverture.",
            "enfant-m|Il dort, par terre !",
            "narrateur|Il laisse le bleu, trop vite.",
            "narrateur|Ce n'est pas sa place, c'est le sol.",
        ],
        3: [
            "narrateur|L'ombre d'une manche touche le crochet.",
            "enfant-m|Il est accroché !",
            "narrateur|Il lâche le bleu, trop vite.",
            "narrateur|L'ombre ment : le manteau est au sol.",
        ],
    }[c]
    body = {
        1: [
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, ça serre, fort.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu poses, ou tu regardes ?",
            "enfant-m|Je regarde, sans jeter.",
        ],
        2: [
            "narrateur|Ses épaules baissent, un peu.",
            "narrateur|Dans sa poitrine, l'envie se bouscule.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu laisses, ou tu regardes ?",
            "enfant-m|J'attends, je regarde.",
        ],
        3: [
            "narrateur|L'envie de lâcher lui pique les doigts.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Papa s'accroupit, près des bottes.",
            "papa|Tu vois l'écaille, où ?",
            "enfant-m|Je cherche, sans foncer.",
        ],
    }[c]
    listen = {
        1: "narrateur|Il écoute le carrelage, puis le petit tic.",
        2: "narrateur|Il écoute l'herbe du seuil, puis le tic.",
        3: "narrateur|Il écoute le plancher, puis le petit tic.",
    }[a]
    pay = "narrateur|L'écaille de boue blonde reparaît, au cuir."
    gesture = {
        1: "narrateur|Il accroche le manteau, près des bottes.",
        2: "narrateur|Il accroche le manteau, près des bottes.",
        3: "narrateur|Il accroche le manteau, près des bottes.",
    }[b]
    adult = {
        1: "maman|Tu l'as posé, sans forcer.",
        2: "papa|Il a sa place, maintenant.",
        3: "maman|Tu l'as raccroché, Raphaël.",
    }[c]
    traces = {
        (1, 1): "narrateur|Un cube a laissé une marque, au tissu.",
        (1, 2): "narrateur|Une page a senti le pain, au bleu.",
        (1, 3): "narrateur|Une tasse a un rond de mie, minuscule.",
        (2, 1): "narrateur|Un cube a un brin d'herbe, au fond.",
        (2, 2): "narrateur|Une page a une goutte, minuscule.",
        (2, 3): "narrateur|Une tasse garde l'odeur de l'herbe.",
        (3, 1): "narrateur|Un cube a un fil de couverture, unique.",
        (3, 2): "narrateur|Une page a un pli du rideau, unique.",
        (3, 3): "narrateur|Une tasse a un peu de savon, au bord.",
    }[(a, b)]
    almost = {
        (1, 1, 1): "narrateur|Un cube cachait le crochet, presque.",
        (1, 1, 2): "narrateur|Le livre serrait trop le bleu, une seconde.",
        (1, 1, 3): "narrateur|La tasse recouvrait l'écaille, presque.",
        (1, 2, 1): "narrateur|L'herbe collait la manche, presque.",
        (1, 2, 2): "narrateur|Le livre tirait le col, une seconde.",
        (1, 2, 3): "narrateur|La tasse gardait une goutte, presque.",
        (1, 3, 1): "narrateur|Le rideau prenait le bleu, presque.",
        (1, 3, 2): "narrateur|Le livre trompait l'œil, une seconde.",
        (1, 3, 3): "narrateur|La tasse se refermait sur le tissu, presque.",
        (2, 1, 1): "narrateur|Un cube de bois couvrait le cuir, presque.",
        (2, 1, 2): "narrateur|La chaise prenait la place, une seconde.",
        (2, 1, 3): "narrateur|Le bord du bol pliait la manche, presque.",
        (2, 2, 1): "narrateur|L'arrosoir bleu mentait, une seconde de trop.",
        (2, 2, 2): "narrateur|Une goutte cachait l'écaille, presque.",
        (2, 2, 3): "narrateur|Le seau bleu prenait le crochet, presque.",
        (2, 3, 1): "narrateur|Le gant bleu prenait la place, presque.",
        (2, 3, 2): "narrateur|Le livre cachait le portemanteau, une seconde.",
        (2, 3, 3): "narrateur|L'herbe collait trop, une seconde.",
        (3, 1, 1): "narrateur|Le pyjama bleu tenait le crochet, presque.",
        (3, 1, 2): "narrateur|Une page couvrait l'écaille, presque.",
        (3, 1, 3): "narrateur|La dînette cachait la manche, presque.",
        (3, 2, 1): "narrateur|Les cubes pesaient trop le tissu, une seconde.",
        (3, 2, 2): "narrateur|Le coussin mentait, une seconde de trop.",
        (3, 2, 3): "narrateur|La lampe manquait le crochet, presque.",
        (3, 3, 1): "narrateur|L'ombre mélangeait les bleus, presque.",
        (3, 3, 2): "narrateur|Un dos bleu prenait la place, presque.",
        (3, 3, 3): "narrateur|L'odeur du soir égarait la main, presque.",
    }[(a, b, c)]
    return (
        time
        + arrive
        + ruse
        + body
        + [listen, pay, gesture, adult, traces, almost]
    )


def ending_lines(a: int, b: int, c: int) -> list[str]:
    lieu = LIEU[a]
    jeu = JEU[b]
    mom = MOM[c]
    firsts = {
        (1, 1, 1): "Les clés se taisent, dans la coupelle.",
        (1, 1, 2): "Le torchon de maman sent le carrelage.",
        (1, 1, 3): "Papa pose une tasse près de l'évier.",
        (1, 2, 1): "Un cube roule vers le seuil, puis s'arrête.",
        (1, 2, 2): "Le manteau pose son ombre au bois.",
        (1, 2, 3): "La fenêtre de la cuisine a un peu de buée.",
        (1, 3, 1): "Un cube dépasse du seuil de la chambre.",
        (1, 3, 2): "Un fil du rideau pend près des clés.",
        (1, 3, 3): "Le coussin sent le pain, au bois.",
        (2, 1, 1): "Un brin d'herbe sèche sur la chaise, loin.",
        (2, 1, 2): "Le métal de l'arrosoir se tait, loin.",
        (2, 1, 3): "Un pas sur l'herbe, puis plus.",
        (2, 2, 1): "Le manteau penche, près des bottes jaunes.",
        (2, 2, 2): "Le cri d'une feuille s'arrête.",
        (2, 2, 3): "Le seau bleu reste loin.",
        (2, 3, 1): "Le gant bleu dépasse du seuil.",
        (2, 3, 2): "Le livre a vu l'herbe, depuis le bois.",
        (2, 3, 3): "Un rayon a bougé, sur l'oreiller.",
        (3, 1, 1): "Le pyjama s'endort près de la porte.",
        (3, 1, 2): "Le plancher ne fait plus de cri.",
        (3, 1, 3): "L'horloge se tait, tic après tic.",
        (3, 2, 1): "Le manteau pose son ombre sur le tapis.",
        (3, 2, 2): "Le linge attend, près du coffre.",
        (3, 2, 3): "Les clés de papa restent dans la coupelle.",
        (3, 3, 1): "Près du seuil, la tasse sent le savon.",
        (3, 3, 2): "Un pli rentre dans le bleu, unique.",
        (3, 3, 3): "Le seuil retrouve son froid, unique.",
    }
    lasts = {
        (1, 1, 1): "Un cube dort près de l'écaille de boue blonde.",
        (1, 1, 2): "Le torchon garde un fil de manche, minuscule.",
        (1, 1, 3): "Un rond de mie reste coincé dans la tasse.",
        (1, 2, 1): "La manche du manteau sèche, près des bottes.",
        (1, 2, 2): "Une feuille du seuil s'endort au livre.",
        (1, 2, 3): "L'ombre du manteau s'endort sur le carrelage.",
        (1, 3, 1): "Du tissu reste dans le cube, au chaud.",
        (1, 3, 2): "Près du rideau, un fil bleu pend.",
        (1, 3, 3): "Sur le cuir, une écaille de boue blonde brille.",
        (2, 1, 1): "Un brin d'herbe sèche, collé à l'écaille.",
        (2, 1, 2): "Loin du manteau, l'arrosoir se tait.",
        (2, 1, 3): "Sur le bois de la chaise, un pas s'éteint.",
        (2, 2, 1): "Près des bottes, le manteau penche, posé.",
        (2, 2, 2): "La feuille s'endort, loin du cuir.",
        (2, 2, 3): "Loin d'ici, le seau bleu reste muet.",
        (2, 3, 1): "Près du lit, un cube d'herbe veille.",
        (2, 3, 2): "Dans le livre, un peu d'herbe froide.",
        (2, 3, 3): "Sur l'oreiller, le rayon a bougé.",
        (3, 1, 1): "Près de la chaise, le pyjama s'endort.",
        (3, 1, 2): "Loin de l'écaille, le plancher se tait.",
        (3, 1, 3): "La tasse garde un peu de savon, unique.",
        (3, 2, 1): "Sur le tapis, l'ombre du manteau dort.",
        (3, 2, 2): "Près du coffre, le linge attend.",
        (3, 2, 3): "Dans la lampe, un tic se tait.",
        (3, 3, 1): "Au chaud, le cube sent le savon.",
        (3, 3, 2): "Dans le bleu, une écaille de boue blonde se tait.",
        (3, 3, 3): "Au portemanteau, le bois ne penche plus.",
    }
    qs = {
        1: "papa|Quel moment tu gardes, près des bottes ?",
        2: "maman|Quel moment tu gardes, sur le seuil ?",
        3: "papa|Quel moment tu gardes, sous la lampe ?",
    }[c]
    ans = {
        (1, 1, 1): "enfant-m|Quand le cube a parlé, sous la table.",
        (1, 1, 2): "enfant-m|Quand j'ai ouvert, sans foncer.",
        (1, 1, 3): "enfant-m|Quand la tasse a dit non, d'abord.",
        (1, 2, 1): "enfant-m|Quand l'écaille a parlé, sous le bois.",
        (1, 2, 2): "enfant-m|Quand le torchon a menti, une seconde.",
        (1, 2, 3): "enfant-m|Quand le bol a pris la place.",
        (1, 3, 1): "enfant-m|Quand le rideau a pris le bleu.",
        (1, 3, 2): "enfant-m|Quand le livre a caché le tic.",
        (1, 3, 3): "enfant-m|Quand j'ai cherché, sans jeter.",
        (2, 1, 1): "enfant-m|Quand le froid a quitté mes bras.",
        (2, 1, 2): "enfant-m|Quand l'arrosoir a menti, trop bleu.",
        (2, 1, 3): "enfant-m|Quand la tasse a brillé, puis tenu.",
        (2, 2, 1): "enfant-m|Quand le seau a menti, dans l'herbe.",
        (2, 2, 2): "enfant-m|Quand la goutte a montré l'écaille.",
        (2, 2, 3): "enfant-m|Quand le gant a cessé de mentir.",
        (2, 3, 1): "enfant-m|Quand le gant a menti, au jardin.",
        (2, 3, 2): "enfant-m|Quand le livre a senti l'herbe.",
        (2, 3, 3): "enfant-m|Quand l'herbe a voulu garder le bleu.",
        (3, 1, 1): "enfant-m|Quand le pyjama a cessé de mentir.",
        (3, 1, 2): "enfant-m|Quand la page a montré le fond.",
        (3, 1, 3): "enfant-m|Quand la dînette a cessé de cacher.",
        (3, 2, 1): "enfant-m|Quand les cubes ont pesé, sans tomber.",
        (3, 2, 2): "enfant-m|Quand le coussin a cessé de mentir.",
        (3, 2, 3): "enfant-m|Quand la lampe a veillé le crochet.",
        (3, 3, 1): "enfant-m|Quand les bleus se sont démêlés.",
        (3, 3, 2): "enfant-m|Quand le dos bleu a perdu.",
        (3, 3, 3): "enfant-m|Quand l'odeur a ramené ma main.",
    }[(a, b, c)]
    return [
        f"narrateur|{firsts[(a, b, c)]}",
        f"narrateur|Il a porté le manteau, {lieu['ou']}.",
        f"narrateur|Il a choisi {jeu['lab']}, pour jouer.",
        f"narrateur|C'était {mom['quand']}, pour rentrer.",
        "narrateur|Voilà le manteau bleu, près des bottes.",
        "narrateur|Sur le cuir, l'écaille de boue blonde tient.",
        "enfant-m|Il a sa place, avec sa trace.",
        qs,
        ans,
        "enfant-m|Je raconte le moment difficile, surtout.",
        f"narrateur|{lasts[(a, b, c)]}",
    ]


def ending_note(a: int, b: int, c: int) -> str:
    return (
        f"arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
        f"destinataire=enfant; sous_texte=trace_{LIEU[a]['short']}_{JEU[b]['short']}_{MOM[c]['short']}; "
        f"tempo=posé; sourire=léger; respiration=ample"
    )


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "cles,bottes,porte")
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
            LIEU[a]["sons"],
            {"emphasis": "manteau"},
        )
        put(
            f"CHK_T0001_P000{a}_Q0001",
            T1_Q[a],
            "clue",
            "",
            {"emphasis": "manteau", "fields": Q_FIELDS[a]},
        )
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            "manteau,bottes",
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
                    {"emphasis": "écaille de boue blonde"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "portemanteau,bottes",
                    {"emphasis": "écaille de boue blonde", "note": ending_note(a, b, c)},
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
    if "écaille de boue blonde" not in out_chunks["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit("indice absent de l'ouverture")
    for c in src["chunks"]:
        if c["kind"] == "passage" and "T0003_P000" in c["chunk_id"] and "_F0001" not in c["chunk_id"] and not c["chunk_id"].endswith("T0003_P0000"):
            if "écaille de boue blonde" not in out_chunks[c["chunk_id"]]["text"].lower():
                raise SystemExit(f"indice non payé: {c['chunk_id']}")

    merged = dict(src)
    merged["fil_rouge"] = (
        "Les clés tombent dans la coupelle. Sur une botte jaune, une écaille "
        "de boue blonde tient. Raphaël veut sortir maintenant. Il tire trop "
        "vite : l'air froid lui prend les bras. Le sourire disparaît. Papa "
        "s'accroupit. Cuisine, jardin ou chambre : sans le bleu, le froid "
        "gagne ; avec le manteau, ça tient. Cubes, livre ou dînette : un faux "
        "bleu ment, le tic dit vrai. Il refuse de foncer. Matin, sieste ou "
        "soir, une chaise, un sol ou une ombre usurpent la place. Il observe, "
        "retrouve l'écaille, accroche près des bottes. Vingt-sept traces."
    )
    merged["title"] = TITLE
    merged["characters"] = "Raphaël, papa, maman"
    merged["setting"] = "entrée, paillasson mouillé, bottes jaunes, portemanteau"
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
        "Les clés de papa tombent dans la coupelle. Raphaël lève les yeux : "
        "le paillasson est mouillé, les bottes jaunes brillent, et sur le cuir "
        "gauche une écaille de boue blonde tient, plate, un peu sèche. Il veut "
        "sortir maintenant. Il tire trop vite : l'air froid lui prend les bras. "
        "Le sourire disparaît. Papa s'accroupit. Cuisine, jardin ou chambre : "
        "sans le manteau le froid gagne ; le bleu part avec lui. Cubes, livre "
        "ou dînette : un bol, un torchon, un arrosoir, un seau, un gant, un "
        "pyjama, un coussin ou un rideau bleu ment. Il refuse de foncer. "
        "Matin, après la sieste ou soir : une chaise, un sol ou une ombre "
        "usurpent la place du portemanteau. Il observe, écoute le tic, "
        "retrouve l'écaille, accroche près des bottes. Le dénouement a failli. "
        "L'écaille paie le début. Le manteau garde une trace.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : entrée, paillasson mouillé, bottes jaunes, portemanteau.\n"
        "- Désir : sortir jouer maintenant, avant que l'écaille sèche.\n"
        "- Objet : manteau bleu (fermeture à tic), près des bottes.\n"
        "- Indice unique : l'écaille de boue blonde, vue dès l'ouverture, payée au climax.\n"
        "- Urgence douce : l'air froid, l'écaille qui sèche au bord.\n"
        "- Imprévu 1 : il tire sans le bleu ; le froid gagne les bras.\n"
        "- Cue : papa ou maman s'accroupit. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : un faux bleu, puis une fausse place "
        "(chaise, sol, ombre).\n"
        "- Revers allongé : coincé, corps (envie et inquiétude), refus de foncer, "
        "écoute du tic, geste neuf.\n"
        "- Résolution : accrocher près des bottes, cubes / livre / dînette, "
        "matin / sieste / soir.\n"
        "- Retour : écaille de boue blonde, bottes jaunes, 27 traces distinctes.\n\n"
        "## Corrections éditoriales\n\n"
        "- Ouverture inventée (les clés dans la coupelle), pas le dump "
        "« Le paillasson de l'entrée est encore mouillé ».\n"
        "- Le premier choix n'enlève pas le manteau : il part avec Raphaël.\n"
        "- Revers allongé : coincé, corps, refus, second arrêt, geste lent.\n"
        "- Neuf disparitions distinctes, vingt-sept résolutions, vingt-sept fins.\n"
        "- Leçon AUT.AFF.002 vécue (accrocher près des bottes), jamais dite.\n"
        "- Monde ≠ TREE-AUT-032 (Mila, manteau vert, casserole), "
        "≠ TREE-AUT-037 (Chouchou, manteau jaune, gouttière), "
        "≠ TREE-DIF-003 (Mila, manteau à pois).\n"
        "- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Troupe D16 : Raphaël, papa, maman. Un seul enfant.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js.\n\n"
        "## Direction vocale\n\n"
        "Impatience de Raphaël au départ, petit découragement quand le manteau "
        "résiste ou qu'un faux bleu ment, fierté calme quand il accroche sans "
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
        "- N2 ≤ 15 mots/phrase\n"
        "- check() OK. Pas d'apply. Pas d'audio. Pas de git.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {len(merged['chunks'])} chunks  chemins {min(counts)}-{max(counts)}")


if __name__ == "__main__":
    build()
