#!/usr/bin/env python3
"""TREE-DIF-044 — Les groseilles de Raphaël au treillis (F-NAR-019, N2)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-044"
N2 = LIMITS["N2"]
TITLE = "Les groseilles de Raphaël au treillis"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
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
    "ancre minuscule",
    "étoile brune",
    "fil pâle",
    "croissant d'eau",
    "croissant pâle",
    "virgule de farine",
    "bouton de nacre",
    "nœud de raphia",
    "pois ivoire",
    "grain de savon",
    "grain vanille",
    "pastille de colle",
    "virgule de buée",
    "capuchon penche",
    "grain doré",
    "brin safran",
    "anneau de liège",
    "clou à tête ronde",
    "grain d'ambre",
    "goutte de cire",
    "anneau de zinc",
    "larme de bronze",
    "point de cire",
    "bracelet d'écorce",
    "boucle d'étain",
    "anneau de pollen",
    "dent de laitue",
    "gouttes pendent",
    "trois notes",
    "arrosoir",
    "statue",
    "bronze",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de grenat",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=sarah_reste_sur_la_marche; "
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
        emphasis="bol",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=regarde_ce_qu_il_porte; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="Sarah",
        note=(
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=les_trois_partent_avec_eux; "
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
            "destinataire=enfant; sous_texte=il_part_trop_vite_sans_elle; "
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
            "intensite=2; destinataire=enfant; sous_texte=sarah_pose_sa_limite; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grain de grenat",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=il_refuse_de_foncer; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de grenat",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=le_grain_de_grenat_paie_le_début; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

CONT = {
    1: dict(lab="le bol blanc", le="le bol", un="un bol", short="bol", ou="dans les mains", sons="bol,ceramique"),
    2: dict(lab="le panier d'osier", le="le panier", un="un panier", short="panier", ou="au bras", sons="panier,osier"),
    3: dict(lab="la nappe à carreaux", le="la nappe", un="une nappe", short="nappe", ou="sous le bras", sons="nappe,tissu"),
}
LIEU = {
    1: dict(lab="la serre", ou="dans la serre", short="serre", sons="serre,verre"),
    2: dict(lab="le tilleul", ou="sous le tilleul", short="tilleul", sons="tilleul,feuille"),
    3: dict(lab="le treillis", ou="au treillis", short="treillis", sons="treillis,fer"),
}
GESTE = {
    1: {
        1: dict(lab="le torchon de maman", short="torchon", sons="torchon,tissu"),
        2: dict(lab="les mains de Sarah", short="mains", sons="mains,grains"),
        3: dict(lab="un pas hors de la serre", short="pas", sons="pas,porte"),
    },
    2: {
        1: dict(lab="l'élastique de maman", short="élastique", sons="elastique,cheveux"),
        2: dict(lab="la serviette", short="serviette", sons="serviette,tissu"),
        3: dict(lab="Sarah tient le bol", short="tient", sons="bol,mains"),
    },
    3: {
        1: dict(lab="les manches retroussées", short="manches", sons="manches,ciré"),
        2: dict(lab="Raphaël tient le panier", short="tient_panier", sons="panier,osier"),
        3: dict(lab="maman noue les poignets", short="noeud", sons="noeud,ciré"),
    },
}

Q_FIELDS = {
    1: {
        "expected_answer": "mains",
        "accepted_examples": "mains | les mains | dans les mains | ses mains",
        "retry_prompt": "Le bol est dans les mains.",
    },
    2: {
        "expected_answer": "bras",
        "accepted_examples": "bras | le bras | au bras | son bras",
        "retry_prompt": "Le panier est au bras.",
    },
    3: {
        "expected_answer": "bras",
        "accepted_examples": "bras | le bras | sous le bras | son bras",
        "retry_prompt": "La nappe est sous le bras.",
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


# Ouverture : un grain tombe dans un bol vide. Indice = grain de grenat.
OPENING = [
    "narrateur|Un grain rouge tombe, dans le bol blanc.",
    "narrateur|Le bol est vide, près de la marche.",
    "narrateur|Personne ne l'a lancé.",
    "narrateur|Le treillis de fer fait tic, en séchant.",
    "narrateur|Un grain de grenat y reste collé.",
    "narrateur|Papa range les tasses, dans la cuisine.",
    "narrateur|Maman coupe le pain, pour le goûter.",
    "enfant-m|Ce grain-là, je le veux !",
    "narrateur|En ce moment, Raphaël tend la main.",
    "narrateur|La porte reste ouverte, sans Sarah.",
    "copine|J'arrive.",
    "narrateur|Sarah reste sur la marche, ciré trop long.",
    "narrateur|Ses lunettes gardent un rond de buée.",
    "narrateur|Raphaël avance, d'un pas.",
    "narrateur|Sarah ne bouge pas.",
    "narrateur|Le silence répond, à sa place.",
    "narrateur|Le sourire de Raphaël disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "papa|On cueille avec elle, avant le goûter ?",
    "enfant-m|Vite, les grains vont sécher !",
]

T1_CHOICE = [
    "narrateur|Près de la marche, trois choses attendent.",
    "narrateur|Le bol blanc, le panier d'osier, la nappe.",
    "maman|Tu prends quoi d'abord, Raphaël ?",
    "papa|Les trois partent, avec vous.",
]

T1 = {
    1: [
        "narrateur|Raphaël saisit le bol blanc, trop vite.",
        "narrateur|Le bord est froid, un peu glissant.",
        "enfant-m|Je le porte, moi !",
        "narrateur|Il part vers le jardin, sans se retourner.",
        "narrateur|Sarah reste sur la marche, les pieds collés.",
        "copine|Attends.",
        "narrateur|Raphaël s'arrête, le bol contre le ventre.",
        "narrateur|Le sourire de Raphaël disparaît.",
        "narrateur|Papa s'accroupit, près de la marche.",
        "papa|Le panier, ensuite, et la nappe.",
        "narrateur|Raphaël revient, le bol dans les mains.",
        "narrateur|Sarah prend la nappe, quand elle veut.",
        "narrateur|Le panier glisse au bras de papa.",
        "enfant-m|Le bol est à moi, dans les mains.",
        "maman|Les trois viennent, avec vous.",
        "narrateur|Sur le treillis, le grain de grenat tient.",
    ],
    2: [
        "narrateur|Raphaël saisit le panier d'osier, trop vite.",
        "narrateur|L'osier gratte, un peu mouillé.",
        "enfant-m|Je le porte, moi !",
        "narrateur|Il glisse le panier au bras, et part.",
        "narrateur|Sarah reste sur la marche, ciré trop long.",
        "copine|Attends.",
        "narrateur|Raphaël s'arrête, le panier qui penche.",
        "narrateur|Ses épaules baissent, près de la haie.",
        "narrateur|Maman s'accroupit, à sa hauteur.",
        "maman|Le bol, ensuite, et la nappe.",
        "narrateur|Raphaël revient, le panier au bras.",
        "narrateur|Sarah prend la nappe, sans se presser.",
        "narrateur|Le bol blanc passe dans les mains de papa.",
        "enfant-m|Le panier est à moi, au bras.",
        "papa|Les trois viennent, avec vous.",
        "narrateur|Sur le treillis, le grain de grenat tient.",
    ],
    3: [
        "narrateur|Raphaël saisit la nappe à carreaux, trop vite.",
        "narrateur|Le tissu claque, et se déplie.",
        "enfant-m|Je la porte, moi !",
        "narrateur|Sarah recule d'un pas, les lunettes floues.",
        "copine|Attends.",
        "narrateur|La nappe retombe, trop large, trop vite.",
        "narrateur|Le sourire de Raphaël disparaît.",
        "narrateur|L'envie et l'inquiétude se bousculent.",
        "narrateur|Papa s'accroupit, près du tissu.",
        "papa|Le bol, ensuite, et le panier.",
        "narrateur|Raphaël plie la nappe, sous le bras.",
        "narrateur|Sarah s'approche, à son pas.",
        "narrateur|Le bol et le panier partent avec eux.",
        "enfant-m|La nappe est à moi, sous le bras.",
        "maman|Les trois viennent, avec vous.",
        "narrateur|Sur le treillis, le grain de grenat tient.",
    ],
}

T1_Q = {
    1: [
        "narrateur|Le bol blanc a quitté la marche.",
        "maman|Le bol est où ?",
    ],
    2: [
        "narrateur|Le panier d'osier a quitté la marche.",
        "papa|Le panier est où ?",
    ],
    3: [
        "narrateur|La nappe à carreaux a quitté la marche.",
        "maman|La nappe est où ?",
    ],
}

T1_C = {
    1: [
        "narrateur|Le bol n'est plus sur la pierre.",
        "enfant-m|Il est dans les mains.",
        "papa|Merci, Raphaël, tu as attendu Sarah.",
        "maman|Où cueille-t-on, alors ?",
        "enfant-m|Là où le grain de grenat brille.",
        "narrateur|Sarah marche, un peu derrière.",
        "narrateur|Le panier et la nappe suivent.",
    ],
    2: [
        "narrateur|Le panier n'est plus sur la pierre.",
        "enfant-m|Il est au bras.",
        "maman|Merci, Raphaël, tu as attendu Sarah.",
        "papa|Où cueille-t-on, alors ?",
        "enfant-m|Là où le grain de grenat brille.",
        "narrateur|Sarah marche, un peu derrière.",
        "narrateur|Le bol et la nappe suivent.",
    ],
    3: [
        "narrateur|La nappe n'est plus sur la pierre.",
        "enfant-m|Elle est sous le bras.",
        "papa|Merci, Raphaël, tu as attendu Sarah.",
        "maman|Où cueille-t-on, alors ?",
        "enfant-m|Là où le grain de grenat brille.",
        "narrateur|Sarah marche, un peu derrière.",
        "narrateur|Le bol et le panier suivent.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Le jardin offre trois coins, pour cueillir.",
        "papa|La serre, le tilleul, ou le treillis ?",
        "maman|Le bol blanc vient avec toi.",
    ],
    2: [
        "narrateur|Le jardin offre trois coins, pour cueillir.",
        "maman|La serre, le tilleul, ou le treillis ?",
        "papa|Le panier d'osier vient avec toi.",
    ],
    3: [
        "narrateur|Le jardin offre trois coins, pour cueillir.",
        "papa|La serre, le tilleul, ou le treillis ?",
        "maman|La nappe à carreaux vient avec toi.",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    table = {
        (1, 1): [
            "narrateur|Raphaël porte le bol vers la serre.",
            "narrateur|Le verre est chaud, un peu trouble.",
            "enfant-m|Les grains, là, tout de suite !",
            "narrateur|Il tire la manche du ciré de Sarah.",
            "narrateur|Sarah plante les pieds, au seuil.",
            "copine|Non.",
            "narrateur|Raphaël entre seul, le bol en avant.",
            "narrateur|La buée cache les tiges, et les grains.",
            "narrateur|Sa main cueille à l'aveugle, trop vite.",
            "narrateur|Deux grains ratent le bol, et s'écrasent.",
            "enfant-m|Ils sont partis !",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, ça serre, fort.",
            "narrateur|Maman s'accroupit, au seuil de la serre.",
            "maman|Elle n'est pas entrée.",
            "papa|Personne ne dit où courir.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Derrière le verre, le grain de grenat brille.",
        ],
        (1, 2): [
            "narrateur|Raphaël porte le bol vers le tilleul.",
            "narrateur|Les feuilles lourdes touchent le ciré.",
            "enfant-m|Les grains par terre, vite !",
            "narrateur|Il court sous les branches, sans Sarah.",
            "narrateur|Sarah reste au soleil, lunettes floues.",
            "copine|Là, c'est trop mouillé.",
            "narrateur|Raphaël ramasse, trop vite, trop bas.",
            "narrateur|Le bol penche, un grain glisse dehors.",
            "enfant-m|Il tombe !",
            "narrateur|Ce n'était pas un grain, c'était une feuille.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Ses épaules baissent, sous le tilleul.",
            "narrateur|Papa s'accroupit, près de l'herbe.",
            "papa|Elle n'a pas bougé.",
            "maman|Personne ne donne la réponse.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Au fond, le grain de grenat tient au fil.",
        ],
        (1, 3): [
            "narrateur|Raphaël porte le bol vers le treillis.",
            "narrateur|Le fer fait tic, tout près du grain.",
            "enfant-m|Le grain de grenat, c'est le mien !",
            "narrateur|Il tend le bol, et tire Sarah.",
            "narrateur|La manche trop longue s'accroche au fil.",
            "copine|Attends.",
            "narrateur|Raphaël tire, une seconde de trop.",
            "narrateur|La branche plie, le bol cogne le fer.",
            "enfant-m|Il va tomber !",
            "narrateur|Sarah ne dit plus rien.",
            "narrateur|Le silence pèse, entre les fils.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "papa|Le fil a parlé, à sa place.",
            "maman|Personne ne dit de tirer.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le grain de grenat attend, collé.",
        ],
        (2, 1): [
            "narrateur|Raphaël porte le panier vers la serre.",
            "narrateur|L'osier racle le seuil de bois.",
            "enfant-m|On entre, les grains sont là !",
            "narrateur|Il pousse le panier, et la manche de Sarah.",
            "narrateur|Sarah s'arrête, les lunettes blanches de buée.",
            "copine|Je vois un nuage.",
            "narrateur|Raphaël entre seul, le panier trop large.",
            "narrateur|Une tige accroche l'osier, dans la vapeur.",
            "narrateur|Le panier se coince, et penche.",
            "enfant-m|Il est pris !",
            "narrateur|Ses épaules baissent, dans la chaleur.",
            "narrateur|Maman s'accroupit, au seuil.",
            "maman|Elle est restée dehors.",
            "papa|Personne ne dit où forcer.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|À travers le verre, le grain de grenat veille.",
        ],
        (2, 2): [
            "narrateur|Raphaël porte le panier vers le tilleul.",
            "narrateur|L'herbe mouille le bas du ciré.",
            "enfant-m|Les grains, sous les feuilles !",
            "narrateur|Il avance trop vite, le panier ouvert.",
            "narrateur|Sarah reste en bordure, les cheveux lourds.",
            "copine|Mes cheveux collent.",
            "narrateur|Une feuille mouillée tombe dans l'osier.",
            "narrateur|Raphaël cueille sans elle, à deux mains.",
            "narrateur|Le panier penche, la feuille cache le fond.",
            "enfant-m|Je ne vois plus !",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Papa s'accroupit, sous les branches.",
            "papa|Elle n'est pas venue.",
            "maman|Personne ne donne la réponse.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Au fond du jardin, le grain de grenat tient.",
        ],
        (2, 3): [
            "narrateur|Raphaël porte le panier vers le treillis.",
            "narrateur|L'osier frotte le fil, tout près.",
            "enfant-m|Le grain de grenat, dans le panier !",
            "narrateur|Il lève le panier, trop haut, trop vite.",
            "narrateur|Sarah lève une main, puis la baisse.",
            "copine|Pas si haut.",
            "narrateur|Le panier cogne le fer, et sonne.",
            "narrateur|La manche de Sarah s'enroule au fil.",
            "enfant-m|Tu es prise !",
            "narrateur|Sarah ne tire pas, elle attend.",
            "narrateur|Le silence compte, plus que les mots.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "narrateur|Maman s'accroupit, près des fils.",
            "maman|Le panier a parlé trop fort.",
            "papa|Personne ne dit de tirer.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le grain de grenat reste collé, patient.",
        ],
        (3, 1): [
            "narrateur|Raphaël porte la nappe vers la serre.",
            "narrateur|Le tissu sent la vapeur, tout de suite.",
            "enfant-m|On étend, et on cueille !",
            "narrateur|Il tire Sarah vers le verre chaud.",
            "narrateur|Sarah secoue la tête, un seul geste.",
            "copine|Dedans, je vois mal.",
            "narrateur|Raphaël entre, la nappe trop large.",
            "narrateur|La buée alourdit les carreaux du tissu.",
            "narrateur|La nappe glisse, et traîne au sol mouillé.",
            "enfant-m|Elle est trop lourde !",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Papa s'accroupit, au seuil.",
            "papa|Elle n'a pas suivi.",
            "maman|Personne ne dit où courir.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Derrière le verre, le grain de grenat brille.",
        ],
        (3, 2): [
            "narrateur|Raphaël porte la nappe vers le tilleul.",
            "narrateur|Les carreaux claquent, sous les branches.",
            "enfant-m|On s'assoit, et on cueille !",
            "narrateur|Il étend trop vite, sans regarder Sarah.",
            "narrateur|Sarah reste debout, les cheveux lourds.",
            "copine|Mes lunettes, d'abord.",
            "narrateur|Une feuille colle à la nappe, sombre.",
            "narrateur|Raphaël pose le bol, trop près du tronc.",
            "narrateur|Le tissu glisse sur l'herbe mouillée.",
            "enfant-m|Elle part !",
            "narrateur|Ses épaules baissent, sous le tilleul.",
            "narrateur|Maman s'accroupit, près du tissu.",
            "maman|Elle n'est pas assise.",
            "papa|Personne ne donne la réponse.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Au fond, le grain de grenat tient au fil.",
        ],
        (3, 3): [
            "narrateur|Raphaël porte la nappe vers le treillis.",
            "narrateur|Le tissu veut s'accrocher, aux fils.",
            "enfant-m|Le grain de grenat, sur la nappe !",
            "narrateur|Il lève la nappe, comme un drapeau.",
            "narrateur|Sarah recule, pour ne pas être prise.",
            "copine|Le fil, il pique.",
            "narrateur|Un coin de nappe s'enroule au fer.",
            "narrateur|Raphaël tire, trop fort, trop vite.",
            "narrateur|Le grain de grenat tremble, presque lâché.",
            "enfant-m|Il va tomber dans l'herbe !",
            "narrateur|Sarah ne dit plus rien.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Papa s'accroupit, près du fil.",
            "papa|La nappe a trop parlé.",
            "maman|Personne ne dit de tirer.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Le grain de grenat tient, juste.",
        ],
    }
    return table[(a, b)]


T3_CHOICE = {
    1: [
        "narrateur|La serre attend, avec Sarah au seuil.",
        "papa|Le torchon de maman, les mains de Sarah ?",
        "maman|Ou un pas hors de la serre ?",
        "narrateur|On suit le grain de grenat.",
    ],
    2: [
        "narrateur|Le tilleul attend, avec Sarah au bord.",
        "maman|L'élastique de maman, ou la serviette ?",
        "papa|Ou Sarah tient le bol ?",
        "narrateur|On suit le grain de grenat.",
    ],
    3: [
        "narrateur|Le treillis attend, le fil un peu tendu.",
        "papa|Les manches retroussées, ou tu tiens le panier ?",
        "maman|Ou je noue les poignets ?",
        "narrateur|On suit le grain de grenat.",
    ],
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    arrive = {
        (1, 1): [
            "narrateur|Maman tend le torchon, près du verre.",
            "enfant-m|J'essuie, vite, pour voir !",
            "narrateur|Il frotte trop fort, trop tôt.",
        ],
        (1, 2): [
            "narrateur|Sarah ouvre les paumes, près des tiges.",
            "enfant-m|Tes mains, les grains, tout de suite !",
            "narrateur|Il veut y poser un grain, trop vite.",
        ],
        (1, 3): [
            "narrateur|Le seuil de la serre reste mouillé.",
            "enfant-m|Un pas dehors, et on cueille !",
            "narrateur|Il tire vers la porte, trop tôt.",
        ],
        (2, 1): [
            "narrateur|Maman tend l'élastique, sous le tilleul.",
            "enfant-m|Tes cheveux, je les prends !",
            "narrateur|Il lève une mèche, trop vite.",
        ],
        (2, 2): [
            "narrateur|La serviette attend, pliée, un peu rêche.",
            "enfant-m|J'essuie tes lunettes, moi !",
            "narrateur|Il approche le tissu, trop près.",
        ],
        (2, 3): [
            "narrateur|Le bol blanc cherche une paire de mains.",
            "enfant-m|Tiens, c'est à toi, maintenant !",
            "narrateur|Il pousse le bol, trop vite.",
        ],
        (3, 1): [
            "narrateur|Les manches du ciré pendent, trop longues.",
            "enfant-m|On retrousse, et on prend le grain !",
            "narrateur|Il saisit la manche de Sarah, trop vite.",
        ],
        (3, 2): [
            "narrateur|Le panier d'osier attend, entre les fils.",
            "enfant-m|Je le tiens, toi tu cueilles !",
            "narrateur|Il tient et cueille, les deux à la fois.",
        ],
        (3, 3): [
            "narrateur|Maman tient un lien, près des poignets.",
            "enfant-m|Noue, comme ça on va plus vite !",
            "narrateur|Sarah cache les mains, dans les manches.",
        ],
    }[(b, c)]
    ruse = {
        1: [
            "narrateur|Sur le verre, un second bol apparaît.",
            "enfant-m|Il y en a deux !",
            "narrateur|Le faux bol tremble, c'est le reflet.",
        ],
        2: [
            "narrateur|Une feuille sombre imite un grain, au sol.",
            "enfant-m|Un grain, là !",
            "narrateur|Ce n'est pas un grain, c'est une feuille.",
        ],
        3: [
            "narrateur|Une ombre de fil imite une tige, rouge.",
            "enfant-m|Le grain, je le tiens !",
            "narrateur|Sa main ferme le vide, pas le grain.",
        ],
    }[b]
    body = {
        1: [
            "narrateur|Sarah ne dit rien, les mains fermées.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, ça serre, fort.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu tires, ou tu regardes ?",
            "enfant-m|Je cherche, sans foncer.",
        ],
        2: [
            "narrateur|Sarah recule d'un souffle, sans parler.",
            "narrateur|Ses épaules baissent, un peu.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu forces, ou tu regardes ?",
            "enfant-m|J'attends, je regarde.",
        ],
        3: [
            "narrateur|Sarah pose sa limite, sans un mot.",
            "narrateur|L'envie de prendre lui pique les doigts.",
            "narrateur|Papa s'accroupit, près du fil.",
            "papa|Tu vois le grain, où ?",
            "enfant-m|Je cherche, sans foncer.",
        ],
    }[c]
    listen = {
        1: "narrateur|Il écoute le verre, puis le silence de Sarah.",
        2: "narrateur|Il écoute les feuilles, puis le silence de Sarah.",
        3: "narrateur|Il écoute le fer, puis le silence de Sarah.",
    }[b]
    pay = "narrateur|Le grain de grenat reparaît, collé."
    gesture = {
        (1, 1): "narrateur|Il tend le torchon, et laisse Sarah frotter.",
        (1, 2): "narrateur|Il tient le bol, les mains de Sarah cueillent.",
        (1, 3): "narrateur|Ils font un pas hors de la serre, ensemble.",
        (2, 1): "narrateur|Sarah hoche, puis maman noue l'élastique.",
        (2, 2): "narrateur|Sarah dit quand la serviette peut venir.",
        (2, 3): "narrateur|Sarah prend le bol, quand elle veut.",
        (3, 1): "narrateur|Ils retroussent les manches, les siennes d'abord.",
        (3, 2): "narrateur|Raphaël tient le panier, Sarah cueille.",
        (3, 3): "narrateur|Sarah offre les poignets, maman noue.",
    }[(b, c)]
    together = {
        1: "narrateur|Un grain rouge roule dans le bol, enfin.",
        2: "narrateur|Un grain rouge tombe dans le panier, enfin.",
        3: "narrateur|Un grain rouge pose sa tache, sur la nappe.",
    }[a]
    adult = {
        1: "maman|Vous l'avez, sans la tirer.",
        2: "papa|Elle a cueilli, à son pas.",
        3: "maman|Le fil n'a plus parlé trop fort.",
    }[c]
    traces = {
        (1, 1): "narrateur|Le torchon garde un rond de buée, minuscule.",
        (1, 2): "narrateur|Une paume de Sarah a teinté le bord du bol.",
        (1, 3): "narrateur|Un pas hors de la serre a séché la pierre.",
        (2, 1): "narrateur|L'élastique garde une mèche, un peu froide.",
        (2, 2): "narrateur|La serviette a un carré plus sombre, unique.",
        (2, 3): "narrateur|Le bol a deux petites mains, en buée.",
        (3, 1): "narrateur|Une manche garde un fil de fer, minuscule.",
        (3, 2): "narrateur|L'osier a une écorchure, près de l'anse.",
        (3, 3): "narrateur|Le nœud des poignets laisse une marque tiède.",
    }[(b, c)]
    almost = {
        (1, 1, 1): "narrateur|Le reflet du bol mentait, presque jusqu'au bout.",
        (1, 1, 2): "narrateur|Les poings fermés de Sarah ont failli rester.",
        (1, 1, 3): "narrateur|La serre a voulu les garder, une seconde.",
        (1, 2, 1): "narrateur|La mèche mouillée a failli cacher l'élastique.",
        (1, 2, 2): "narrateur|La feuille sombre a failli entrer dans le bol.",
        (1, 2, 3): "narrateur|Le bol a failli rester dans ses seules mains.",
        (1, 3, 1): "narrateur|La manche accrochée a failli tout arrêter.",
        (1, 3, 2): "narrateur|Le panier trop haut a failli sonner trop fort.",
        (1, 3, 3): "narrateur|Les mains cachées ont failli ne jamais sortir.",
        (2, 1, 1): "narrateur|Le torchon trop vite a failli rayer le verre.",
        (2, 1, 2): "narrateur|Le grain dans sa main a failli tomber seul.",
        (2, 1, 3): "narrateur|Le panier coincé a failli rester dans la vapeur.",
        (2, 2, 1): "narrateur|La mèche a failli rester collée, trop lourde.",
        (2, 2, 2): "narrateur|La feuille dans l'osier a failli cacher le fond.",
        (2, 2, 3): "narrateur|Sarah a failli ne pas prendre le bol.",
        (2, 3, 1): "narrateur|Le fil a failli garder la manche, trop serré.",
        (2, 3, 2): "narrateur|Les deux gestes à la fois ont failli tout verser.",
        (2, 3, 3): "narrateur|Le lien a failli attendre des mains absentes.",
        (3, 1, 1): "narrateur|La nappe trop lourde a failli rester au sol.",
        (3, 1, 2): "narrateur|Les carreaux mouillés ont failli tout cacher.",
        (3, 1, 3): "narrateur|Le pas dehors a failli se faire sans elle.",
        (3, 2, 1): "narrateur|La mèche sous le tilleul a failli tout coller.",
        (3, 2, 2): "narrateur|La nappe glissante a failli partir seule.",
        (3, 2, 3): "narrateur|Le bol poussé a failli tomber dans l'herbe.",
        (3, 3, 1): "narrateur|Le coin de nappe a failli arracher le grain.",
        (3, 3, 2): "narrateur|Le drapeau de tissu a failli tout emmêler.",
        (3, 3, 3): "narrateur|Le grain de grenat a failli tomber dans l'herbe.",
    }[(a, b, c)]
    return (
        arrive
        + ruse
        + body
        + [listen, pay, gesture, together, adult, traces, almost]
    )


def ending_lines(a: int, b: int, c: int) -> list[str]:
    firsts = {
        (1, 1, 1): "Le torchon sèche, près de la fenêtre.",
        (1, 1, 2): "Deux paumes rouges se posent sur la table.",
        (1, 1, 3): "La pierre du seuil redevient claire.",
        (1, 2, 1): "Une mèche libre bouge, près du pain.",
        (1, 2, 2): "La serviette garde un carré sombre, posée.",
        (1, 2, 3): "Le bol blanc a deux traces de doigts.",
        (1, 3, 1): "Une manche retroussée reste ainsi, à table.",
        (1, 3, 2): "L'anse du panier penche, un peu, au bois.",
        (1, 3, 3): "Le nœud des poignets dort, près du pain.",
        (2, 1, 1): "Le verre de la serre se tait, au loin.",
        (2, 1, 2): "Une tige a laissé sa sève, sur l'osier.",
        (2, 1, 3): "Le seuil de bois a un pas plus clair.",
        (2, 2, 1): "L'élastique repose, près de la tasse.",
        (2, 2, 2): "Une feuille sèche, unique, sur la serviette.",
        (2, 2, 3): "Sarah garde le bol, jusqu'à la table.",
        (2, 3, 1): "Un fil de fer dort, dans une manche.",
        (2, 3, 2): "Le panier sonne moins, posé au bois.",
        (2, 3, 3): "Les poignets libres posent les grains, un à un.",
        (3, 1, 1): "La nappe à carreaux a un coin plus lourd.",
        (3, 1, 2): "Un carreau de tissu a senti la vapeur.",
        (3, 1, 3): "Un pas dehors a suivi jusqu'à la marche.",
        (3, 2, 1): "Une mèche sent le tilleul, près du pain.",
        (3, 2, 2): "La nappe a un carré d'herbe, minuscule.",
        (3, 2, 3): "Le bol a voyagé, dans les mains de Sarah.",
        (3, 3, 1): "Le fer du treillis fait tic, plus loin.",
        (3, 3, 2): "Un carreau de nappe a frôlé le fil.",
        (3, 3, 3): "Le lien de maman reste près des assiettes.",
    }
    lasts = {
        (1, 1, 1): "Sur le torchon, un grain de grenat sèche.",
        (1, 1, 2): "Dans une paume, le grain de grenat tient.",
        (1, 1, 3): "Hors de la serre, le grain de grenat brille.",
        (1, 2, 1): "Près de l'élastique, le grain de grenat veille.",
        (1, 2, 2): "Sur la serviette, le grain de grenat repose.",
        (1, 2, 3): "Au fond du bol, le grain de grenat tient.",
        (1, 3, 1): "Dans une manche, le grain de grenat a voyagé.",
        (1, 3, 2): "Au fond du panier, le grain de grenat roule.",
        (1, 3, 3): "Près du nœud, le grain de grenat s'endort.",
        (2, 1, 1): "Loin du verre, le grain de grenat se tait.",
        (2, 1, 2): "Contre l'osier, le grain de grenat s'est calé.",
        (2, 1, 3): "Sur la pierre sèche, le grain de grenat pose.",
        (2, 2, 1): "Sous une mèche, le grain de grenat a passé.",
        (2, 2, 2): "Près de la feuille, le grain de grenat reste.",
        (2, 2, 3): "Entre deux mains, le grain de grenat voyage.",
        (2, 3, 1): "Au pli d'une manche, le grain de grenat dort.",
        (2, 3, 2): "Sous l'anse, le grain de grenat ne sonne plus.",
        (2, 3, 3): "Sur un poignet libre, le grain de grenat a glissé.",
        (3, 1, 1): "Dans un carreau lourd, le grain de grenat tient.",
        (3, 1, 2): "Sous un carreau tiède, le grain de grenat brille.",
        (3, 1, 3): "Près de la marche, le grain de grenat rentre.",
        (3, 2, 1): "À côté du pain, le grain de grenat sent l'arbre.",
        (3, 2, 2): "Sur un carré d'herbe, le grain de grenat sèche.",
        (3, 2, 3): "Dans le bol de Sarah, le grain de grenat reste.",
        (3, 3, 1): "Loin du tic, le grain de grenat s'est posé.",
        (3, 3, 2): "Au bord du tissu, le grain de grenat s'est arrêté.",
        (3, 3, 3): "Près des assiettes, le grain de grenat a une place.",
    }
    qs = {
        1: "papa|Quel moment tu gardes, dans la serre ?",
        2: "maman|Quel moment tu gardes, sous le tilleul ?",
        3: "papa|Quel moment tu gardes, au treillis ?",
    }[b]
    ans = {
        (1, 1, 1): "enfant-m|Quand le torchon a cessé de frotter trop fort.",
        (1, 1, 2): "enfant-m|Quand ses mains ont cueilli, pas les miennes.",
        (1, 1, 3): "enfant-m|Quand on a fait le pas, hors de la buée.",
        (1, 2, 1): "enfant-m|Quand l'élastique a attendu son hochement.",
        (1, 2, 2): "enfant-m|Quand la serviette a attendu son oui.",
        (1, 2, 3): "enfant-m|Quand elle a pris le bol, sans que je pousse.",
        (1, 3, 1): "enfant-m|Quand on a retroussé, les siennes d'abord.",
        (1, 3, 2): "enfant-m|Quand j'ai tenu le panier, sans cueillir.",
        (1, 3, 3): "enfant-m|Quand elle a offert les poignets, toute seule.",
        (2, 1, 1): "enfant-m|Quand le reflet a menti, et que j'ai vu.",
        (2, 1, 2): "enfant-m|Quand ses poings fermés m'ont dit d'attendre.",
        (2, 1, 3): "enfant-m|Quand le panier a cessé de se coincer.",
        (2, 2, 1): "enfant-m|Quand la mèche a cessé d'être trop lourde.",
        (2, 2, 2): "enfant-m|Quand la feuille a cessé de faire le grain.",
        (2, 2, 3): "enfant-m|Quand elle a dit non, sous les branches.",
        (2, 3, 1): "enfant-m|Quand le fil a parlé, à sa place.",
        (2, 3, 2): "enfant-m|Quand le panier a sonné, et que je me suis arrêté.",
        (2, 3, 3): "enfant-m|Quand ses mains sont sorties, sans qu'on tire.",
        (3, 1, 1): "enfant-m|Quand la nappe trop lourde a cessé de glisser.",
        (3, 1, 2): "enfant-m|Quand elle a dit : je vois mal.",
        (3, 1, 3): "enfant-m|Quand le pas dehors s'est fait avec elle.",
        (3, 2, 1): "enfant-m|Quand ses lunettes ont parlé, d'abord.",
        (3, 2, 2): "enfant-m|Quand la nappe a cessé de partir seule.",
        (3, 2, 3): "enfant-m|Quand je n'ai plus poussé le bol.",
        (3, 3, 1): "enfant-m|Quand le grain a tremblé, et que j'ai lâché.",
        (3, 3, 2): "enfant-m|Quand le tissu a cessé d'être un drapeau.",
        (3, 3, 3): "enfant-m|Quand le grain de grenat a failli tomber.",
    }[(a, b, c)]
    mid = {
        1: f"narrateur|Voilà {CONT[a]['le']}, sur la nappe du goûter.",
        2: f"narrateur|Voilà {CONT[a]['le']}, près du pain coupé.",
        3: f"narrateur|Voilà {CONT[a]['le']}, au milieu de la table.",
    }[c]
    return [
        f"narrateur|{firsts[(a, b, c)]}",
        f"narrateur|Ils ont cueilli {LIEU[b]['ou']}.",
        mid,
        "narrateur|Le grain de grenat a quitté le fil.",
        "enfant-m|Il est rentré, avec sa trace.",
        "copine|On l'a pris, tous les deux.",
        qs,
        ans,
        "enfant-m|Je raconte le moment difficile, surtout.",
        "maman|Le goûter peut commencer, maintenant.",
        f"narrateur|{lasts[(a, b, c)]}",
    ]


def ending_note(a: int, b: int, c: int) -> str:
    return (
        f"arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
        f"destinataire=enfant; sous_texte=trace_{CONT[a]['short']}_{LIEU[b]['short']}_{GESTE[b][c]['short']}; "
        f"tempo=posé; sourire=léger; respiration=ample"
    )


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "bol,treillis,fer")
    put(
        "CHK_T0001_P0000",
        T1_CHOICE,
        "choice",
        "",
        {"fields": {
            "option_1_label": "le bol blanc",
            "option_2_label": "le panier d'osier",
            "option_3_label": "la nappe à carreaux",
        }},
    )

    t3_labs = {
        1: ("le torchon de maman", "les mains de Sarah", "un pas hors de la serre"),
        2: ("l'élastique de maman", "la serviette", "Sarah tient le bol"),
        3: ("les manches retroussées", "Raphaël tient le panier", "maman noue les poignets"),
    }

    for a in (1, 2, 3):
        put(
            f"CHK_T0001_P000{a}",
            T1[a],
            "action",
            CONT[a]["sons"],
            {"emphasis": CONT[a]["short"]},
        )
        put(
            f"CHK_T0001_P000{a}_Q0001",
            T1_Q[a],
            "clue",
            "",
            {"emphasis": CONT[a]["short"], "fields": Q_FIELDS[a]},
        )
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            CONT[a]["sons"],
            {"emphasis": "grain de grenat"},
        )
        put(
            f"CHK_T0001_P000{a}_T0002_P0000",
            T2_CHOICE[a],
            "choice",
            "",
            {"fields": {
                "option_1_label": "la serre",
                "option_2_label": "le tilleul",
                "option_3_label": "le treillis",
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
            labs = t3_labs[b]
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
                T3_CHOICE[b],
                "choice",
                "",
                {"fields": {
                    "option_1_label": labs[0],
                    "option_2_label": labs[1],
                    "option_3_label": labs[2],
                }},
            )
            for c in (1, 2, 3):
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(
                    base,
                    t3_lines(a, b, c),
                    "resolution",
                    GESTE[b][c]["sons"],
                    {"emphasis": "grain de grenat"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "table,gouter,grains",
                    {"emphasis": "grain de grenat", "note": ending_note(a, b, c)},
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
    if "grain de grenat" not in out_chunks["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit("indice absent de l'ouverture")
    for c in src["chunks"]:
        if c["kind"] == "passage" and "T0003_P000" in c["chunk_id"] and "_F0001" not in c["chunk_id"] and not c["chunk_id"].endswith("T0003_P0000"):
            if "grain de grenat" not in out_chunks[c["chunk_id"]]["text"].lower():
                raise SystemExit(f"indice non payé: {c['chunk_id']}")

    adult_join = " ".join(
        ln.split("|", 1)[1]
        for ch in out_chunks.values()
        for ln in ch["script"].splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
    ).lower()
    if adult_join.count("merci") + adult_join.count("bravo") > 6:
        raise SystemExit("merci/bravo trop répété")

    merged = dict(src)
    merged["fil_rouge"] = (
        "Un grain rouge tombe dans le bol blanc, vide, près de la marche. "
        "Le treillis de fer fait tic en séchant : un grain de grenat y reste "
        "collé. Raphaël veut le cueillir pour le goûter, tout de suite. Sarah "
        "reste sur la marche, ciré trop long, lunettes floues. Le silence "
        "répond. Papa s'accroupit. Bol, panier ou nappe : les trois partent. "
        "Serre, tilleul ou treillis : il tire, elle pose sa limite. Il refuse "
        "de foncer. Torchon, mains, pas ; élastique, serviette, bol ; manches, "
        "panier, nœud. Le grain de grenat paie le début. Vingt-sept traces."
    )
    merged["title"] = TITLE
    merged["characters"] = "Raphaël, Sarah, papa, maman"
    merged["setting"] = "jardin après la pluie : serre, tilleul, treillis"
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
        "Un grain rouge tombe dans le bol blanc, vide, près de la marche. "
        "Le treillis de fer fait tic en séchant : un grain de grenat y reste "
        "collé. Raphaël veut remplir le bol pour le goûter, tout de suite. "
        "Sarah reste sur la marche, ciré trop long. Le silence répond. Le "
        "sourire disparaît. Papa s'accroupit. Bol, panier ou nappe : il part "
        "trop vite, elle dit attends, les trois partent. Serre, tilleul ou "
        "treillis : il tire, elle pose sa limite, la première cueillette "
        "rate. Il refuse de foncer. Torchon, mains, pas hors de la serre ; "
        "élastique, serviette, Sarah tient le bol ; manches, panier, nœud. "
        "Le grain de grenat paie le début. Le bol rentre avec une trace.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin après la pluie, serre, tilleul, treillis de fer.\n"
        "- Désir : remplir le bol de groseilles pour le goûter, avec Sarah.\n"
        "- Objet : bol blanc / panier d'osier / nappe à carreaux (les trois partent).\n"
        "- Indice unique : le grain de grenat collé au treillis, vu dès l'ouverture, payé au climax.\n"
        "- Urgence douce : les grains vont sécher, le pain attend.\n"
        "- Imprévu 1 : Raphaël part trop vite ; Sarah reste ; la cueillette rate.\n"
        "- Cue : papa s'accroupit. Un merci vécu (tu as attendu Sarah).\n"
        "- Imprévu 2 (plus rusé) : reflet / feuille-grain / ombre de fil ; le silence de Sarah.\n"
        "- Revers : corps (sourire disparu, poitrine), refus de foncer, indice retrouvé.\n"
        "- Résolution : cueillir avec elle, à son pas, selon le geste choisi.\n"
        "- Retour : grain de grenat, 27 traces distinctes.\n\n"
        "## Corrections éditoriales\n\n"
        "- Ouverture inventée (un grain tombe dans un bol vide), pas le gabarit v2, pas « Un merle saute ».\n"
        "- Le premier choix n'enlève pas le contenant : bol, panier et nappe partent.\n"
        "- Labels T1/T2/T3 conservés. Leçon DIF.COR.003 vécue (rythmes, limite, silence), jamais dite.\n"
        "- Neuf T2 distincts, vingt-sept T3, vingt-sept fins.\n"
        "- Monde ≠ TREE-DIF-065 (Chouchou, arrosoirs), ≠ TREE-DIF-056 (statue de bronze), ≠ TREE-DIF-052 (grain d'ambre, mer).\n"
        "- Pas de refrain example3, pas de miel, pas de gouttes-refrain, pas de grand-père/maîtresse.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Troupe D16 : Raphaël, Sarah, papa, maman.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js.\n\n"
        "## Direction vocale\n\n"
        "Impatience de Raphaël au départ, petit découragement quand Sarah "
        "s'arrête, fierté calme quand il cueille sans la tirer. Le silence "
        "de Sarah compte. `slow` réservé aux choix, à la question, au retour.\n\n"
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
