#!/usr/bin/env python3
"""TREE-AUT-011 — Le seau jaune de Sarah (F-NAR-019, N1, AUT.AFF.003, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-011"
N1 = LIMITS["N1"]
TITLE = "Le seau jaune de Sarah"
CHILD = "enfant-f"
TICS = re.compile(
    r"\b(tout doux|tout calme|encore|déjà|deja|une étape après l'autre)\b",
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
    "étoile brune",
    "fil pâle",
    "croissant",
    "virgule",
    "bouton de nacre",
    "nœud de raphia",
    "pois ivoire",
    "grain savon",
    "grain vanille",
    "pastille colle",
    "capuchon",
    "grain doré",
    "brin safran",
    "brin de paille",
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
    "laitue",
    "escargot",
    "grain de limon",
    "grain de mica",
    "grain de cannelle",
    "grain d'ocre",
    "grain de feutre",
    "grain de sésame",
    "grain de suie",
    "grain de paprika",
    "pompe",
    "nino",
    "aniss",
    "tom ",
    "léa",
    "sami",
    "hugo",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de paille",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=l_anse_résiste_dans_la_botte; "
            "tempo=naturel; volume=medium; sourire=léger; respiration=ample; "
            "pause=craquement_de_paille"
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
            "tempo=suspendu; volume=medium; sourire=léger; "
            "respiration=pause_avant_choix"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="seau",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=une_affaire_est_restée_dans_le_seau; "
            "tempo=suspendu; volume=soft; sourire=aucun; "
            "respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="seau",
        note=(
            "arc=confirmation; intention=relancer; emotion=élan; intensite=1; "
            "destinataire=enfant; sous_texte=elle_reprend_le_seau_avec_elle; "
            "tempo=naturel; volume=medium; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note=(
            "arc=action; intention=entraîner; emotion=impatience; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_jouer_et_porter_trop_vite; "
            "tempo=vif; volume=medium; sourire=léger; respiration=courte"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=découragement_léger; intensite=2; destinataire=enfant; "
            "sous_texte=le_goûter_cache_le_grain_de_paille; tempo=resserré; "
            "volume=medium; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grain de paille",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; "
            "emotion=fierté_calme; intensite=2; destinataire=enfant; "
            "sous_texte=le_grain_de_paille_paie_le_début; tempo=naturel; "
            "volume=medium; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de paille",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; sous_texte=le_grain_reste_au_bord; "
            "tempo=posé; volume=soft; sourire=léger; respiration=ample"
        ),
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
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


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=grain_de_paille_au_bord_{a}{b}{c}; "
        f"tempo={tempos[c]}; volume=soft; sourire=léger; respiration=ample; "
        f"chemin={a}{b}{c}"
    )


OPENING = vet(
    [
        "narrateur|Sarah connaît la ferme, toit par toit.",
        "narrateur|Sous le toit rouge, la paille sent le soleil.",
        "narrateur|Un détail paraît neuf, près du hangar.",
        "narrateur|L'air sent le foin chaud, et le bois.",
        "narrateur|La botte ouverte craque, sous le vent.",
        "narrateur|Le portail de bois fait criiic, lent.",
        "narrateur|Ça sent la paille, sous les bottes.",
        "narrateur|Près de l'auge, le seau jaune attend.",
        "narrateur|Au bord, un grain de paille colle.",
        "narrateur|Il brille, minuscule, contre le plastique.",
        "narrateur|Sarah vit là, avec papa et maman.",
        "papa|Tu as vu le grain, au bord ?",
        f"{CHILD}|Oui, il est collé, tout petit.",
        "maman|L'auge du hangar attend la paille.",
        f"{CHILD}|Je veux le seau, pour l'auge !",
        f"{CHILD}|Vite, que le vent ne prenne pas la botte !",
        "narrateur|En ce moment, Sarah saisit l'anse.",
        "narrateur|Le plastique est tiède, un peu rêche.",
        "narrateur|Elle tire trop fort, d'un seul coup.",
        "narrateur|L'anse résiste, prise dans la paille.",
        f"{CHILD}|Il ne veut pas venir !",
        "narrateur|Le sourire de Sarah disparaît.",
        "narrateur|L'envie et l'inquiétude se bousculent.",
        "narrateur|Papa s'accroupit, à la même hauteur.",
        "papa|Regarde l'anse, pas tes pieds.",
        "maman|Tu l'emportes où, d'abord ?",
        f"{CHILD}|Je le prends, je cours au hangar !",
        "narrateur|Un grain de paille tremble, puis tient.",
        "papa|Merci d'avoir gardé le seau avec toi.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|Le seau jaune part avec elle, lourd.",
        "narrateur|Les cubes, le livre, ou la dînette.",
        "maman|Tu vas où, d'abord, Sarah ?",
    ]
)

T1 = {
    1: dict(
        lab="les cubes",
        ans="cube",
        acc="cube | le cube | un cube | dans le seau | seau",
        retry="Quelque chose est tombé. Qu'est-ce qui est dans le seau ?",
        ok="Oui, le cube.",
        sons="cubes,bois,paille",
        emp="cube",
        passage=vet(
            [
                "narrateur|Sarah va vers le banc de la botte.",
                "narrateur|Les cubes attendent, sur le bois rêche.",
                "narrateur|Le seau jaune part avec elle, lourd.",
                "narrateur|Ça sent la paille, près du banc.",
                f"{CHILD}|Je les mets dans le seau, papa !",
                "narrateur|Elle jette un cube, trop vite.",
                "narrateur|Le cube tape le fond, et cache le grain.",
                "narrateur|L'anse résiste, coincée sous le bois.",
                f"{CHILD}|Il ne veut pas bouger !",
                "papa|Le seau est avec toi.",
                "maman|Le cube est dedans, maintenant.",
                "narrateur|Sarah s'arrête, les épaules basses.",
                f"{CHILD}|Je veux ma tour, et l'auge !",
                "narrateur|Un grain de paille dépasse, minuscule.",
                "narrateur|Dans sa poitrine, l'envie serre un peu.",
            ]
        ),
        question=vet(
            [
                "narrateur|Un objet a tapé le fond jaune.",
                "maman|Qu'est-ce qui est tombé dans le seau ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Sarah pose le seau, un instant.",
                "narrateur|Elle sort le cube, sans le jeter.",
                f"{CHILD}|Il était à moi, là.",
                "papa|Tu l'as repris, tout seul.",
                "maman|Le seau t'attend, au pied.",
                "narrateur|Le grain de paille n'a pas bougé.",
                f"{CHILD}|On continue, avec le seau.",
            ]
        ),
    ),
    2: dict(
        lab="le livre",
        ans="paille",
        acc="paille | la paille | grain | grain de paille | botte",
        retry="La page pique. Qu'est-ce qui pique la page ?",
        ok="Oui, la paille.",
        sons="livre,pages,paille",
        emp="paille",
        passage=vet(
            [
                "narrateur|Sarah s'assoit sur la botte du hangar.",
                "narrateur|Le seau jaune part avec elle, lourd.",
                "narrateur|Le livre est ouvert, sur la paille.",
                "narrateur|La paille pique un peu, sous elle.",
                "narrateur|Elle pose le seau, trop vite, à côté.",
                f"{CHILD}|Je lis, puis je cours à l'auge !",
                "narrateur|Un souffle tourne la page, sec.",
                "narrateur|La paille pique le papier, tout net.",
                "papa|La page a un piquant, Sarah.",
                "maman|Le seau penche, vers la botte.",
                "narrateur|Sarah veut partir, le seau reste.",
                f"{CHILD}|Il est resté, là !",
                "narrateur|Les épaules baissent, le sourire part.",
                f"{CHILD}|Je le veux, avec moi.",
                "narrateur|Elle revient, l'anse un peu froide.",
                "narrateur|Le grain de paille reste au bord.",
            ]
        ),
        question=vet(
            [
                "narrateur|La page a reçu un petit piquant.",
                "papa|Qu'est-ce qui pique la page ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Sarah reprend le seau, près de la botte.",
                "narrateur|Elle souffle la page, du plat de la main.",
                f"{CHILD}|Il vient, lui aussi.",
                "maman|Le livre peut attendre, un peu.",
                "papa|L'auge t'attend, sous le toit.",
                "narrateur|Le grain de paille n'a pas bougé.",
                f"{CHILD}|Oui, avec le seau.",
            ]
        ),
    ),
    3: dict(
        lab="la dînette",
        ans="tasse",
        acc="tasse | la tasse | une tasse | dans le seau | seau",
        retry="Quelque chose a roulé. Qu'est-ce qui est dans le seau ?",
        ok="Oui, la tasse.",
        sons="tasse,dinette,etable",
        emp="tasse",
        passage=vet(
            [
                "narrateur|Sarah va vers l'étable aux tasses.",
                "narrateur|De petites tasses en bois attendent.",
                "narrateur|Elles sont près de l'étable, lisses.",
                "narrateur|Le seau jaune part avec elle.",
                f"{CHILD}|Je sers le lait, sur le seau !",
                "narrateur|Elle pose une tasse, trop vite.",
                "narrateur|Une tasse roule, et tombe dedans.",
                "narrateur|L'anse résiste, coincée contre le bois.",
                f"{CHILD}|Elle ne veut pas sortir !",
                "papa|Le seau n'est pas une table.",
                "maman|La tasse est au fond, Sarah.",
                "narrateur|Sarah s'arrête, les joues chaudes.",
                f"{CHILD}|Je veux servir, et l'auge !",
                "narrateur|Un grain de paille dépasse, au bord.",
                "narrateur|L'inquiétude serre, dans sa poitrine.",
            ]
        ),
        question=vet(
            [
                "narrateur|Un petit bois a roulé, tout seul.",
                "maman|Qu'est-ce qui a roulé dans le seau ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Sarah penche le seau, sans le secouer.",
                "narrateur|Elle sort la tasse, tout droit.",
                f"{CHILD}|Elle était à moi, là.",
                "papa|Tu l'as reprise, sans tirer.",
                "maman|Le seau t'attend, près du pied.",
                "narrateur|Le grain de paille n'a pas bougé.",
                f"{CHILD}|On continue, avec le seau.",
            ]
        ),
    ),
}

T2_CHOICE = {
    1: vet(
        [
            "narrateur|Le cube est sorti, le seau reste lourd.",
            "narrateur|Une pomme, un yaourt, un morceau de pain.",
            "papa|Tu goûtes quoi, Sarah ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Le livre attend, le seau reste avec elle.",
            "narrateur|Une pomme, un yaourt, un morceau de pain.",
            "maman|Tu goûtes quoi, Sarah ?",
        ]
    ),
    3: vet(
        [
            "narrateur|La tasse est sortie, le seau reste lourd.",
            "narrateur|Une pomme, un yaourt, un morceau de pain.",
            "papa|Tu goûtes quoi, Sarah ?",
        ]
    ),
}


def t2_scene(a: int, b: int) -> list[str]:
    bodies = {
        (1, 1): [
            "narrateur|Sur le banc, une pomme rouge attend.",
            "narrateur|Sarah croque un tout petit bout.",
            f"{CHILD}|Je la mets dans le seau !",
            "narrateur|Le jus coule, et cache le grain.",
            "narrateur|L'anse devient collante, trop vite.",
            "papa|La pomme n'est pas de la paille.",
            "maman|Le cube a laissé un coin, au fond.",
            f"{CHILD}|Je secoue, et ça sort !",
            "narrateur|Elle lève le seau, puis s'arrête.",
            "narrateur|Cette fois, elle ne fonce pas.",
            f"{CHILD}|Je veux voir, au bord.",
            "narrateur|Un grain de paille brille, sous le jus.",
        ],
        (1, 2): [
            "narrateur|Un pot de yaourt froid attend, au panier.",
            "narrateur|Sarah pose le pot, dans le seau.",
            f"{CHILD}|Il tient au chaud, papa !",
            "narrateur|Le blanc coule, et cache le grain.",
            "narrateur|Le cube glisse, collé au plastique.",
            "papa|Le seau n'est pas un bol.",
            "maman|Le yaourt a pris le bord.",
            f"{CHILD}|Je tire le pot, fort !",
            "narrateur|Elle tire, puis s'arrête.",
            "narrateur|Cette fois, elle ne fonce pas.",
            f"{CHILD}|Je veux voir, au bord.",
            "narrateur|Un grain de paille perce, sous le blanc.",
        ],
        (1, 3): [
            "narrateur|Un morceau de pain tiède attend.",
            "narrateur|Sarah pose le pain, comme un couvercle.",
            f"{CHILD}|Il garde la paille, maman !",
            "narrateur|Des miettes tombent, et cachent le grain.",
            "narrateur|Le cube disparaît, sous la croûte.",
            "papa|Le pain n'est pas un toit.",
            "maman|Les miettes ont pris le fond.",
            f"{CHILD}|Je jette le pain, dehors !",
            "narrateur|Elle lève la croûte, puis s'arrête.",
            "narrateur|Cette fois, elle ne fonce pas.",
            f"{CHILD}|Je veux voir, au bord.",
            "narrateur|Un grain de paille reste, sous une miette.",
        ],
        (2, 1): [
            "narrateur|Près du livre, une pomme rouge attend.",
            "narrateur|Sarah croque, le jus sur le pouce.",
            f"{CHILD}|Je la pose sur la page !",
            "narrateur|Une goutte menace le papier, et tient.",
            "narrateur|Elle recule, et met la pomme au seau.",
            "papa|Le livre n'aime pas le jus.",
            "maman|La pomme a taché le bord jaune.",
            f"{CHILD}|Je verse, pour laver le grain !",
            "narrateur|Elle penche, puis s'arrête.",
            "narrateur|Cette fois, elle ne fonce pas.",
            f"{CHILD}|Je veux voir, au bord.",
            "narrateur|Un grain de paille luit, sous le jus.",
        ],
        (2, 2): [
            "narrateur|Le yaourt est froid, près de la botte.",
            "narrateur|Sarah ouvre le pot, trop vite.",
            f"{CHILD}|Une cuillère, sur la page !",
            "narrateur|Une goutte blanche manque le livre.",
            "narrateur|Elle pose le pot, dans le seau.",
            "papa|Les pages n'aiment pas le blanc.",
            "maman|Le pot a caché le bord.",
            f"{CHILD}|Je sors tout, d'un coup !",
            "narrateur|Elle plonge la main, puis s'arrête.",
            "narrateur|Cette fois, elle ne fonce pas.",
            f"{CHILD}|Je veux voir, au bord.",
            "narrateur|Un grain de paille perce, sous le pot.",
        ],
        (2, 3): [
            "narrateur|Le pain tiède sent, près du livre.",
            "narrateur|Sarah en casse un bout, sec.",
            f"{CHILD}|Une miette, pour la page !",
            "narrateur|La miette colle, et pique le papier.",
            "narrateur|Elle jette le pain, dans le seau.",
            "papa|Le livre n'est pas une assiette.",
            "maman|La croûte a couvert le bord.",
            f"{CHILD}|Je secoue, vers la botte !",
            "narrateur|L'anse tape le bois, puis elle s'arrête.",
            "narrateur|Cette fois, elle ne fonce pas.",
            f"{CHILD}|Je veux voir, au bord.",
            "narrateur|Un grain de paille reste, sous la croûte.",
        ],
        (3, 1): [
            "narrateur|Près des tasses, une pomme rouge attend.",
            "narrateur|Sarah veut servir le jus, pour rire.",
            f"{CHILD}|Dans la tasse, puis dans le seau !",
            "narrateur|Le jus manque la tasse, et file.",
            "narrateur|Il cache le grain, au plastique.",
            "papa|La dînette n'aime pas le vrai jus.",
            "maman|La pomme a collé le bord.",
            f"{CHILD}|Je rince, avec de l'eau !",
            "narrateur|Elle cherche l'eau, puis s'arrête.",
            "narrateur|Cette fois, elle ne fonce pas.",
            f"{CHILD}|Je veux voir, au bord.",
            "narrateur|Un grain de paille luit, sous le jus.",
        ],
        (3, 2): [
            "narrateur|Le yaourt froid attend, près des tasses.",
            "narrateur|Sarah sert une cuillère, trop pleine.",
            f"{CHILD}|Du lait, pour papa !",
            "narrateur|Le blanc tombe, dans le seau.",
            "narrateur|La tasse glisse, et cache le grain.",
            "papa|C'est tiède, pour de rire.",
            "maman|Le pot a pris toute la place.",
            f"{CHILD}|Je tire la tasse, fort !",
            "narrateur|Elle tire, puis s'arrête.",
            "narrateur|Cette fois, elle ne fonce pas.",
            f"{CHILD}|Je veux voir, au bord.",
            "narrateur|Un grain de paille perce, sous le blanc.",
        ],
        (3, 3): [
            "narrateur|Le pain tiède attend, près de l'étable.",
            "narrateur|Sarah en met un bout, dans une tasse.",
            f"{CHILD}|Une soupe de pain, maman !",
            "narrateur|Elle pose la tasse, dans le seau.",
            "narrateur|Les miettes cachent le grain, au fond.",
            "papa|Le seau n'est pas une casserole.",
            "maman|La croûte a tout couvert.",
            f"{CHILD}|Je jette les miettes, dehors !",
            "narrateur|Elle penche, trop vite, puis s'arrête.",
            "narrateur|Cette fois, elle ne fonce pas.",
            f"{CHILD}|Je veux voir, au bord.",
            "narrateur|Un grain de paille reste, sous une miette.",
        ],
    }
    return vet(bodies[(a, b)])


T3_CHOICE = {
    1: vet(
        [
            "narrateur|La pomme cache le bord, le seau attend.",
            "narrateur|Le chat, le chien, ou la poule.",
            "maman|Qui t'accompagne, vers l'auge ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Le yaourt cache le bord, le seau attend.",
            "narrateur|Le chat, le chien, ou la poule.",
            "papa|Qui t'accompagne, vers l'auge ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Le pain cache le bord, le seau attend.",
            "narrateur|Le chat, le chien, ou la poule.",
            "maman|Qui t'accompagne, vers l'auge ?",
        ]
    ),
}


def t3_scene(a: int, b: int, c: int) -> list[str]:
    bodies = {
        (1, 1, 1): [
            f"{CHILD}|Le chat, sur le rebord de la grange !",
            "narrateur|Le chat s'assoit sur l'anse, lourd.",
            "narrateur|Sarah attend, sans le pousser.",
            "narrateur|Il part, et le grain de paille paraît.",
            f"{CHILD}|Il était là, depuis le hangar !",
            "papa|Tu l'as vu, sans secouer.",
            "narrateur|Elle pose le cube, contre le banc.",
            "narrateur|Elle essuie le jus, du plat du doigt.",
            "narrateur|Puis elle verse la paille, vers l'auge.",
            "maman|L'auge a son nid, à présent.",
            "narrateur|Le grain de paille reste au bord, mouillé.",
        ],
        (1, 1, 2): [
            f"{CHILD}|Le chien, près de sa niche de paille !",
            "narrateur|Le chien pose le museau, dans le seau.",
            "narrateur|Sarah retient l'anse, sans la jeter.",
            "narrateur|Il renifle, et le grain de paille paraît.",
            f"{CHILD}|Il n'est pas parti, papa.",
            "maman|Tu as regardé, avec lui.",
            "narrateur|Elle pose le cube, sur le banc.",
            "narrateur|Le trognon part, près de la niche.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "papa|Le chien a laissé le fond.",
            "narrateur|Le grain de paille reste, collé.",
        ],
        (1, 1, 3): [
            f"{CHILD}|La poule, sous le toit rouge !",
            "narrateur|La poule picore près du cube, sec.",
            "narrateur|Sarah ne court pas, elle observe.",
            "narrateur|Le bec montre le grain de paille.",
            f"{CHILD}|Je le vois, collé !",
            "papa|Tu as suivi son bec, sans foncer.",
            "narrateur|Elle pose le cube, près du nid.",
            "narrateur|Un pépin roule, et s'arrête.",
            "narrateur|Elle verse la paille, dans l'auge.",
            "maman|Le nid a son toit, rouge.",
            "narrateur|Le grain de paille veille, au plastique.",
        ],
        (1, 2, 1): [
            f"{CHILD}|Le chat, je sors le pot, lentement.",
            "narrateur|Le rebord de la grange est tiède.",
            "narrateur|Sarah tourne le pot, sans tirer.",
            "narrateur|Le grain de paille apparaît, au bord.",
            "papa|Tu as tourné, pas arraché.",
            f"{CHILD}|Le blanc reste dans le pot.",
            "maman|Le cube rentre, sur le banc.",
            "narrateur|Elle pose le pot, près du chat.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le chat cligne, puis s'étire.",
            "narrateur|Le grain de paille tient le bord.",
        ],
        (1, 2, 2): [
            f"{CHILD}|Le chien, j'écoute le pot d'abord.",
            "narrateur|Un petit bruit de plastique, puis rien.",
            "narrateur|Sarah soulève le pot, tout droit.",
            "narrateur|Le grain de paille brille, à l'ombre.",
            "maman|Il n'est plus caché.",
            f"{CHILD}|Il était dessous, papa.",
            "papa|Tu as levé, sans secouer.",
            "narrateur|Elle pose le cube, près de la niche.",
            "narrateur|Le pot rentre, la paille part.",
            "narrateur|Le chien frappe du pied, puis s'assoit.",
            "narrateur|Le grain de paille reste, collé.",
        ],
        (1, 2, 3): [
            f"{CHILD}|La poule, le toit montre le pot.",
            "narrateur|Une ombre ronde tombe, sur le fond.",
            "narrateur|Sarah fait tourner le pot, lent.",
            "narrateur|Le grain de paille luit, sous le blanc.",
            "papa|Tu l'as vu, collé.",
            f"{CHILD}|Je pose le pot, puis je verse.",
            "maman|La poule picore, loin du yaourt.",
            "narrateur|Elle pose le cube, contre le nid.",
            "narrateur|Elle verse, vers l'auge du hangar.",
            "narrateur|Une plume tombe, sur le bois.",
            "narrateur|Le grain de paille tremble, au plastique.",
        ],
        (1, 3, 1): [
            f"{CHILD}|Le chat, je sors le pain, lentement.",
            "narrateur|Le soleil touche le rebord, pâle.",
            "narrateur|Sarah lève la croûte, sans la jeter.",
            "narrateur|Le grain de paille apparaît, au bord.",
            "papa|Tu as levé, pas arraché.",
            f"{CHILD}|Les miettes restent dans ma main.",
            "maman|Le cube rentre, sur le banc.",
            "narrateur|Elle pose le pain, près du chat.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le chat sent, puis se recule.",
            "narrateur|Le grain de paille tient le fond.",
        ],
        (1, 3, 2): [
            f"{CHILD}|Le chien, j'écoute la croûte d'abord.",
            "narrateur|Un petit bruit de mie, puis rien.",
            "narrateur|Sarah soulève le pain, tout droit.",
            "narrateur|Le grain de paille brille, à l'ombre.",
            "maman|Les miettes ne cachent plus.",
            f"{CHILD}|Il était dessous, papa.",
            "papa|Tu as vu, sans foncer.",
            "narrateur|Elle pose le cube, près de la niche.",
            "narrateur|Une miette part, vers le chien.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le grain de paille reste, collé.",
        ],
        (1, 3, 3): [
            f"{CHILD}|La poule, le toit montre la croûte.",
            "narrateur|Une ombre de pain tombe, sur le fond.",
            "narrateur|Sarah écarte les miettes, du doigt.",
            "narrateur|Le grain de paille luit, sous le nid.",
            "papa|Tu l'as vu, collé.",
            f"{CHILD}|Je pose le pain, puis je verse.",
            "maman|La poule aime la miette, pas le seau.",
            "narrateur|Elle pose le cube, contre le nid.",
            "narrateur|Elle verse, vers l'auge du hangar.",
            "narrateur|Une miette attend, près de la poule.",
            "narrateur|Le grain de paille veille, au plastique.",
        ],
        (2, 1, 1): [
            f"{CHILD}|Le chat, je sors la pomme, au rebord.",
            "narrateur|Les pages restent au sec, sur la botte.",
            "narrateur|Sarah tire la pomme, sans la presser.",
            "narrateur|Le grain de paille apparaît, mouillé.",
            "papa|Le livre reste là, ouvert.",
            f"{CHILD}|La pomme, c'est pour plus tard.",
            "maman|Tu l'as laissée, hors de la page.",
            "narrateur|Elle referme le livre, d'une main.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le chat cligne, contre le bois.",
            "narrateur|Le grain de paille reste au seau.",
        ],
        (2, 1, 2): [
            f"{CHILD}|Le chien, je sors la pomme, à la niche.",
            "narrateur|Le livre dort, sous un coin de paille.",
            "narrateur|Sarah essuie le jus, puis elle regarde.",
            "narrateur|Le grain de paille brille, au bord.",
            "maman|Les pages n'ont pas bu.",
            f"{CHILD}|Il tenait sous la pomme, papa.",
            "papa|Tu as vu, sans verser.",
            "narrateur|Elle pose le livre, au sec.",
            "narrateur|Le chien attend, la queue basse.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le grain de paille reste, au chaud.",
        ],
        (2, 1, 3): [
            f"{CHILD}|La poule, la page montre une poule.",
            "narrateur|La vraie poule picore, sous le toit.",
            "narrateur|Sarah compare, puis sort la pomme.",
            "narrateur|Le grain de paille luit, collé.",
            "papa|Le livre reste loin du bec.",
            f"{CHILD}|Je verse, tout seul.",
            "maman|L'image reste sur le papier.",
            "narrateur|Elle pose le livre, contre la botte.",
            "narrateur|Un pépin roule, vers le nid.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le grain de paille veille, au fond.",
        ],
        (2, 2, 1): [
            f"{CHILD}|Le chat, je sors le pot, du livre.",
            "narrateur|Une page un peu collante attend.",
            "narrateur|Sarah soulève le pot, sans le presser.",
            "narrateur|Le grain de paille apparaît, au bord.",
            "papa|Tu as levé, pas froissé.",
            f"{CHILD}|La page reste presque blanche.",
            "maman|Le livre rentre, sur la botte.",
            "narrateur|Elle pose le pot, près du chat.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le chat sent le blanc, puis part.",
            "narrateur|Le grain de paille tient le bord.",
        ],
        (2, 2, 2): [
            f"{CHILD}|Le chien, j'écoute le pot d'abord.",
            "narrateur|Le livre a une tache ronde, pâle.",
            "narrateur|Sarah sort le pot, tout droit.",
            "narrateur|Le grain de paille brille, à l'ombre.",
            "maman|La tache reste, petite.",
            f"{CHILD}|Il était sous le pot, papa.",
            "papa|Tu as vu, sans foncer.",
            "narrateur|Elle pose le livre, près de la niche.",
            "narrateur|Le chien renifle, puis s'assoit.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le grain de paille reste, collé.",
        ],
        (2, 2, 3): [
            f"{CHILD}|La poule, la page blanche attend.",
            "narrateur|La poule picore, loin du yaourt.",
            "narrateur|Sarah écarte le pot, du doigt.",
            "narrateur|Le grain de paille luit, sous le nid.",
            "papa|Tu l'as vu, collé.",
            f"{CHILD}|Je pose le pot, puis je verse.",
            "maman|Le livre reste propre, presque.",
            "narrateur|Elle pose le livre, contre le nid.",
            "narrateur|Elle verse, vers l'auge du hangar.",
            "narrateur|Une plume tombe, sur la page.",
            "narrateur|Le grain de paille tremble, au plastique.",
        ],
        (2, 3, 1): [
            f"{CHILD}|Le chat, je sors le pain, du livre.",
            "narrateur|Une miette dort, sur la page.",
            "narrateur|Sarah souffle la miette, sans frotter.",
            "narrateur|Le grain de paille apparaît, au bord.",
            "papa|Tu as soufflé, pas déchiré.",
            f"{CHILD}|La miette est dans ma main.",
            "maman|Le livre rentre, sur la botte.",
            "narrateur|Elle pose le pain, près du chat.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le chat ignore la mie, et cligne.",
            "narrateur|Le grain de paille tient le fond.",
        ],
        (2, 3, 2): [
            f"{CHILD}|Le chien, le livre sent le pain.",
            "narrateur|La niche garde un coin d'ombre.",
            "narrateur|Sarah soulève la croûte, tout droit.",
            "narrateur|Le grain de paille brille, à l'ombre.",
            "maman|Les pages n'ont pas de mie.",
            f"{CHILD}|Il était dessous, papa.",
            "papa|Tu as vu, sans secouer.",
            "narrateur|Elle pose le livre, près de la niche.",
            "narrateur|Une miette part, vers le chien.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le grain de paille reste, collé.",
        ],
        (2, 3, 3): [
            f"{CHILD}|La poule du livre, et la vraie !",
            "narrateur|Sous le toit rouge, la vraie picore.",
            "narrateur|Sarah écarte les miettes, du doigt.",
            "narrateur|Le grain de paille luit, collé.",
            "papa|Le livre reste loin du bec.",
            f"{CHILD}|Je pose le pain, puis je verse.",
            "maman|La poule aime la mie, pas la page.",
            "narrateur|Elle pose le livre, contre le nid.",
            "narrateur|Elle verse, vers l'auge du hangar.",
            "narrateur|Une miette attend, près de la poule.",
            "narrateur|Le grain de paille veille, au plastique.",
        ],
        (3, 1, 1): [
            f"{CHILD}|Le chat, je sors la pomme, des tasses.",
            "narrateur|La tasse a un jus, tout au fond.",
            "narrateur|Sarah essuie le bois, du doigt.",
            "narrateur|Le grain de paille apparaît, au bord.",
            "papa|Tu as essuyé, pas jeté.",
            f"{CHILD}|La tasse peut servir, pour rire.",
            "maman|La dînette rentre, près de l'étable.",
            "narrateur|Elle pose la tasse, près du chat.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le chat sent le jus, puis part.",
            "narrateur|Le grain de paille tient le bord.",
        ],
        (3, 1, 2): [
            f"{CHILD}|Le chien, je sers, pour de rire.",
            "narrateur|Sarah tend une tasse, vers le museau.",
            "narrateur|Le chien recule, puis s'assoit.",
            "narrateur|Le grain de paille brille, au bord.",
            "maman|Il n'a pas bu, c'est un jeu.",
            f"{CHILD}|Il était sous la pomme, papa.",
            "papa|Tu as vu, sans verser.",
            "narrateur|Elle pose la tasse, près de la niche.",
            "narrateur|Le trognon part, vers le chien.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le grain de paille reste, au chaud.",
        ],
        (3, 1, 3): [
            f"{CHILD}|La poule, la tasse attend le nid.",
            "narrateur|La poule picore, loin du jus.",
            "narrateur|Sarah sort la pomme, sans presser.",
            "narrateur|Le grain de paille luit, au bord.",
            "papa|Tu l'as vu, collé.",
            f"{CHILD}|Je pose la tasse, puis je verse.",
            "maman|La poule n'aime pas le vrai jus.",
            "narrateur|Elle pose la tasse, contre le nid.",
            "narrateur|Un pépin roule, et s'arrête.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le grain de paille veille, au fond.",
        ],
        (3, 2, 1): [
            f"{CHILD}|Le chat, le yaourt a fait le lait.",
            "narrateur|Sarah sert une cuillère, pour rire.",
            "narrateur|Le chat cligne, trop près du blanc.",
            "narrateur|Elle recule le pot, puis regarde.",
            "narrateur|Le grain de paille apparaît, au bord.",
            "papa|Tu as reculé, pas versé.",
            f"{CHILD}|Le lait reste dans le pot.",
            "maman|La tasse rentre, près de l'étable.",
            "narrateur|Elle pose le pot, près du chat.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le grain de paille tient le bord.",
        ],
        (3, 2, 2): [
            f"{CHILD}|Le chien, la petite cuillère d'abord.",
            "narrateur|Sarah lèche la cuillère, puis s'arrête.",
            "narrateur|Elle sort le pot, tout droit.",
            "narrateur|Le grain de paille brille, à l'ombre.",
            "maman|La cuillère n'est plus dans le seau.",
            f"{CHILD}|Il était dessous, papa.",
            "papa|Tu as levé, sans secouer.",
            "narrateur|Elle pose la tasse, près de la niche.",
            "narrateur|Le chien attend, la queue basse.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le grain de paille reste, collé.",
        ],
        (3, 2, 3): [
            f"{CHILD}|La poule, un pot vide, et elle.",
            "narrateur|Sarah vide le reste, dans une tasse.",
            "narrateur|La poule picore, loin du blanc.",
            "narrateur|Le grain de paille luit, au bord.",
            "papa|Tu l'as vu, collé.",
            f"{CHILD}|Je pose le pot, puis je verse.",
            "maman|La poule n'aime pas le yaourt.",
            "narrateur|Elle pose la tasse, contre le nid.",
            "narrateur|Le pot vide penche, puis tient.",
            "narrateur|Elle verse, vers l'auge du hangar.",
            "narrateur|Le grain de paille tremble, au plastique.",
        ],
        (3, 3, 1): [
            f"{CHILD}|Le chat, une miette dans la tasse.",
            "narrateur|Sarah souffle la miette, sans frotter.",
            "narrateur|Le chat suit la mie, des yeux.",
            "narrateur|Le grain de paille apparaît, au bord.",
            "papa|Tu as soufflé, pas jeté.",
            f"{CHILD}|La miette est dans ma main.",
            "maman|La tasse rentre, près de l'étable.",
            "narrateur|Elle pose le pain, près du chat.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le chat ignore la mie, et cligne.",
            "narrateur|Le grain de paille tient le fond.",
        ],
        (3, 3, 2): [
            f"{CHILD}|Le chien, le pain a servi, pour rire.",
            "narrateur|Sarah tend un bout, vers le museau.",
            "narrateur|Le chien prend, puis s'assoit.",
            "narrateur|Le grain de paille brille, au bord.",
            "maman|Il a eu sa part, dehors.",
            f"{CHILD}|Il était sous la croûte, papa.",
            "papa|Tu as vu, sans secouer.",
            "narrateur|Elle pose la tasse, près de la niche.",
            "narrateur|Une miette reste, près du chien.",
            "narrateur|Elle verse la paille, vers l'auge.",
            "narrateur|Le grain de paille reste, collé.",
        ],
        (3, 3, 3): [
            f"{CHILD}|La poule, la tasse sent le foin.",
            "narrateur|Sous le toit rouge, la poule picore.",
            "narrateur|Sarah écarte les miettes, du doigt.",
            "narrateur|Le grain de paille luit, collé.",
            "papa|Le foin, c'est pour l'auge.",
            f"{CHILD}|Je pose la tasse, puis je verse.",
            "maman|La poule aime la mie, et le nid.",
            "narrateur|Elle pose la tasse, contre le nid.",
            "narrateur|Elle verse, vers l'auge du hangar.",
            "narrateur|Une miette attend, près de la poule.",
            "narrateur|Le grain de paille veille, au plastique.",
        ],
    }
    return vet(bodies[(a, b, c)])


def ending(a: int, b: int, c: int) -> list[str]:
    lines = {
        (1, 1, 1): [
            "narrateur|Sous le toit rouge, le hangar se tait.",
            f"{CHILD}|L'auge a sa paille, et le chat aussi.",
            "papa|Tu as vu le grain, ce soir ?",
            "maman|Le seau a sa place, près de l'auge.",
            "narrateur|Sarah pose l'anse, sans la jeter.",
            "narrateur|Le cube reste, un peu collant.",
            f"{CHILD}|Je l'ai gardé, avec moi.",
            "narrateur|Un cube garde le grain de paille, près du chat.",
        ],
        (1, 1, 2): [
            "narrateur|La niche de paille sent le foin.",
            f"{CHILD}|Le chien a vu le fond, avec moi.",
            "maman|Le jus brille, sur le plastique ?",
            "papa|Le seau rentre, près de l'auge.",
            "narrateur|Sarah essuie l'anse, du plat de la main.",
            "narrateur|Un trognon reste, près de la niche.",
            f"{CHILD}|Il a failli partir, le seau.",
            "narrateur|Le jus colle au grain, près du chien.",
        ],
        (1, 1, 3): [
            "narrateur|Le nid sous le toit rouge s'assombrit.",
            f"{CHILD}|La poule a montré le bord.",
            "papa|Le cube dort, près d'elle ?",
            "maman|L'auge est pleine, à présent.",
            "narrateur|Sarah pose le seau, contre le bois.",
            "narrateur|Un pépin reste, près du nid.",
            f"{CHILD}|J'ai versé, sans courir.",
            "narrateur|Un cube rouge dort près de la poule.",
        ],
        (1, 2, 1): [
            "narrateur|Le rebord de la grange garde un rond.",
            f"{CHILD}|Le pot est vide, le chat cligne.",
            "papa|La cuillère sèche, tu la vois ?",
            "maman|Le seau a trouvé l'auge.",
            "narrateur|Sarah pose l'anse, un peu blanche.",
            "narrateur|Le cube rentre, sur le banc.",
            f"{CHILD}|Je l'ai repris, le seau.",
            "narrateur|Une cuillère sèche, près du chat.",
        ],
        (1, 2, 2): [
            "narrateur|Près de la niche, le soir descend.",
            f"{CHILD}|Le chien a laissé le pot.",
            "maman|Le pot penche, tu le remets ?",
            "papa|L'auge a bu la paille.",
            "narrateur|Sarah redresse le pot, sans le jeter.",
            "narrateur|Le cube reste, un peu taché.",
            f"{CHILD}|Il a failli rester, le seau.",
            "narrateur|Le pot penche, grain vers le chien.",
        ],
        (1, 2, 3): [
            "narrateur|Une plume blanche dort, sous le toit.",
            f"{CHILD}|La poule n'a pas goûté le blanc.",
            "papa|Un trait blanc, tu le vois ?",
            "maman|Le seau rentre, près de l'auge.",
            "narrateur|Sarah essuie le bord, du doigt.",
            "narrateur|Le cube attend, contre le nid.",
            f"{CHILD}|J'ai versé, tout seul.",
            "narrateur|Un trait blanc, près de la poule.",
        ],
        (1, 3, 1): [
            "narrateur|Le chat se recroqueville, sur le rebord.",
            f"{CHILD}|Le pain a gardé une miette.",
            "papa|Elle colle au cube, tu la vois ?",
            "maman|L'auge est prête, pour la nuit.",
            "narrateur|Sarah pose le seau, contre la grange.",
            "narrateur|Une miette reste, sur le bois.",
            f"{CHILD}|Je l'ai porté, jusqu'au bout.",
            "narrateur|Une miette colle au cube, près du chat.",
        ],
        (1, 3, 2): [
            "narrateur|La niche sent le pain, un peu tiède.",
            f"{CHILD}|Le chien a eu sa miette.",
            "maman|Le pain tiède sent, tu le sens ?",
            "papa|Le seau a sa place, au hangar.",
            "narrateur|Sarah pose l'anse, un peu farineuse.",
            "narrateur|Le cube rentre, sur le banc.",
            f"{CHILD}|Il a failli rester, sous la croûte.",
            "narrateur|Le pain tiède sent, près du chien.",
        ],
        (1, 3, 3): [
            "narrateur|Sous le toit rouge, le nid se ferme.",
            f"{CHILD}|La poule a la miette, et l'auge.",
            "papa|Une miette attend, tu la laisses ?",
            "maman|Le seau rentre, lourd et sage.",
            "narrateur|Sarah pose le seau, près du nid.",
            "narrateur|Le cube reste, un peu de mie dessus.",
            f"{CHILD}|J'ai versé, sans jeter.",
            "narrateur|Une miette attend la poule, au nid.",
        ],
        (2, 1, 1): [
            "narrateur|La botte du hangar garde le livre.",
            f"{CHILD}|La page sent la pomme, un peu.",
            "papa|Le chat l'a vue, la page ?",
            "maman|L'auge a sa paille, à présent.",
            "narrateur|Sarah pose le seau, contre la botte.",
            "narrateur|Un pépin reste, sur le bois.",
            f"{CHILD}|Je l'ai repris, le seau.",
            "narrateur|La page sent la pomme, près du chat.",
        ],
        (2, 1, 2): [
            "narrateur|Près de la niche, le livre se tait.",
            f"{CHILD}|Le chien a un pépin, pour rire.",
            "maman|Le livre garde un pépin, tu le sors ?",
            "papa|Le seau a trouvé l'auge.",
            "narrateur|Sarah souffle la page, une fois.",
            "narrateur|Le pépin roule, vers le chien.",
            f"{CHILD}|Il a failli tacher, le livre.",
            "narrateur|Le livre garde un pépin, près du chien.",
        ],
        (2, 1, 3): [
            "narrateur|L'image de poule, et la vraie poule.",
            f"{CHILD}|Elles se regardent, sous le toit.",
            "papa|La vraie picore, tu la vois ?",
            "maman|L'auge est pleine, le livre au sec.",
            "narrateur|Sarah pose le seau, près du nid.",
            "narrateur|La page reste ouverte, un peu.",
            f"{CHILD}|J'ai versé, sans mouiller.",
            "narrateur|L'image montre la poule, et la vraie.",
        ],
        (2, 2, 1): [
            "narrateur|Une page collante attend, sur la botte.",
            f"{CHILD}|Le chat n'y a pas mis la patte.",
            "papa|Elle sèche, tu la laisses ?",
            "maman|Le seau rentre, près de l'auge.",
            "narrateur|Sarah referme le livre, sans frotter.",
            "narrateur|Le pot vide penche, puis tient.",
            f"{CHILD}|Je l'ai porté, le seau.",
            "narrateur|Une page collante, près du chat.",
        ],
        (2, 2, 2): [
            "narrateur|La niche reçoit le livre, un peu taché.",
            f"{CHILD}|Le yaourt a fait un rond, pâle.",
            "maman|Le yaourt a taché le livre, tu vois ?",
            "papa|L'auge a bu, le seau se pose.",
            "narrateur|Sarah pose l'anse, contre le bois.",
            "narrateur|Le chien renifle le rond, puis part.",
            f"{CHILD}|Il a failli rester, le seau.",
            "narrateur|Le yaourt a taché le livre, près du chien.",
        ],
        (2, 2, 3): [
            "narrateur|La page blanche attend la poule.",
            f"{CHILD}|Elle n'a pas picoré le papier.",
            "papa|La page blanche, tu la fermes ?",
            "maman|Le seau a sa place, au hangar.",
            "narrateur|Sarah pose le livre, contre le nid.",
            "narrateur|Une plume reste, sur la couverture.",
            f"{CHILD}|J'ai versé, tout seul.",
            "narrateur|La page blanche attend la poule.",
        ],
        (2, 3, 1): [
            "narrateur|Une miette dort, sur la page fermée.",
            f"{CHILD}|Le chat l'a regardée, sans la prendre.",
            "papa|Une miette sur la page, tu la sors ?",
            "maman|L'auge est prête, le livre au sec.",
            "narrateur|Sarah souffle, une fois, tout net.",
            "narrateur|Le pain rentre, près de la botte.",
            f"{CHILD}|Je l'ai repris, le seau.",
            "narrateur|Une miette sur la page, près du chat.",
        ],
        (2, 3, 2): [
            "narrateur|Le livre sent le pain, près du chien.",
            f"{CHILD}|La niche a une odeur de croûte.",
            "maman|Le livre sent le pain, tu le poses ?",
            "papa|Le seau rentre, lourd et sage.",
            "narrateur|Sarah pose l'anse, un peu farineuse.",
            "narrateur|Une miette reste, près de la niche.",
            f"{CHILD}|Il a failli rester, sous la croûte.",
            "narrateur|Le livre sent le pain, près du chien.",
        ],
        (2, 3, 3): [
            "narrateur|La poule du livre, sous le toit rouge.",
            f"{CHILD}|La vraie poule picore, tout près.",
            "papa|Elles se ressemblent, tu trouves ?",
            "maman|L'auge a sa paille, le nid aussi.",
            "narrateur|Sarah pose le seau, contre le nid.",
            "narrateur|Le livre se tait, une plume dessus.",
            f"{CHILD}|J'ai versé, sans courir.",
            "narrateur|La poule du livre, sous le toit rouge.",
        ],
        (3, 1, 1): [
            "narrateur|La tasse a un jus, près du chat.",
            f"{CHILD}|Je l'ai servie, pour de rire.",
            "papa|Le jus reste, tu l'essuies ?",
            "maman|Le seau a trouvé l'auge.",
            "narrateur|Sarah pose la tasse, sur l'étable.",
            "narrateur|Le chat cligne, un peu collant.",
            f"{CHILD}|Je l'ai repris, le seau.",
            "narrateur|La tasse a un jus, près du chat.",
        ],
        (3, 1, 2): [
            "narrateur|Sarah a servi le chien, pour rire.",
            f"{CHILD}|Il n'a pas bu, il a joué.",
            "maman|Tu lui as tendu la tasse ?",
            "papa|L'auge a bu la paille, elle.",
            "narrateur|Sarah pose le seau, près de la niche.",
            "narrateur|La tasse reste, un peu de jus au fond.",
            f"{CHILD}|Il a failli partir, le seau.",
            "narrateur|Sarah a servi le chien, pour rire.",
        ],
        (3, 1, 3): [
            "narrateur|La tasse attend la poule, grain au bord.",
            f"{CHILD}|Elle n'a pas picoré le bois.",
            "papa|Le grain au bord, tu le vois ?",
            "maman|L'auge est pleine, sous le toit.",
            "narrateur|Sarah pose le seau, contre le nid.",
            "narrateur|Un pépin reste, près de la tasse.",
            f"{CHILD}|J'ai versé, tout seul.",
            "narrateur|La tasse attend la poule, grain au bord.",
        ],
        (3, 2, 1): [
            "narrateur|Le blanc du yaourt, près du chat.",
            f"{CHILD}|Le lait du jeu, c'est fini.",
            "papa|Le blanc sèche, tu le vois ?",
            "maman|Le seau rentre, près de l'auge.",
            "narrateur|Sarah pose le pot, sur l'étable.",
            "narrateur|La tasse rentre, un peu blanche.",
            f"{CHILD}|Je l'ai porté, le seau.",
            "narrateur|Le blanc du yaourt, près du chat.",
        ],
        (3, 2, 2): [
            "narrateur|La petite cuillère, près du chien.",
            f"{CHILD}|Elle a travaillé, pour de rire.",
            "maman|La cuillère, tu la remets ?",
            "papa|L'auge a sa paille, à présent.",
            "narrateur|Sarah pose l'anse, contre la niche.",
            "narrateur|Le pot vide penche, puis tient.",
            f"{CHILD}|Il a failli rester, le seau.",
            "narrateur|La petite cuillère, près du chien.",
        ],
        (3, 2, 3): [
            "narrateur|Un pot vide, près de la poule.",
            f"{CHILD}|Elle n'a pas voulu le blanc.",
            "papa|Le pot vide penche, tu le poses ?",
            "maman|Le seau a sa place, au hangar.",
            "narrateur|Sarah pose la tasse, contre le nid.",
            "narrateur|Une plume reste, sur le pot.",
            f"{CHILD}|J'ai versé, sans jeter.",
            "narrateur|Un pot vide, près de la poule.",
        ],
        (3, 3, 1): [
            "narrateur|Une miette dans la tasse, près du chat.",
            f"{CHILD}|Le chat l'a vue, sans la prendre.",
            "papa|La miette, tu la sors ?",
            "maman|L'auge est prête, pour la nuit.",
            "narrateur|Sarah pose le seau, contre la grange.",
            "narrateur|La tasse rentre, un peu de mie.",
            f"{CHILD}|Je l'ai repris, le seau.",
            "narrateur|Une miette dans la tasse, près du chat.",
        ],
        (3, 3, 2): [
            "narrateur|Le pain a servi, près du chien.",
            f"{CHILD}|Il a eu sa part, dehors.",
            "maman|Le pain a servi, tu le poses ?",
            "papa|Le seau rentre, lourd et sage.",
            "narrateur|Sarah pose l'anse, un peu farineuse.",
            "narrateur|La tasse reste, près de la niche.",
            f"{CHILD}|Il a failli rester, sous la croûte.",
            "narrateur|Le pain a servi, près du chien.",
        ],
        (3, 3, 3): [
            "narrateur|La tasse sent le foin, près de la poule.",
            f"{CHILD}|Le foin, c'est pour l'auge, maman.",
            "papa|La tasse sent le foin, tu la poses ?",
            "maman|L'auge a sa paille, le nid aussi.",
            "narrateur|Sarah pose le seau, contre le nid.",
            "narrateur|Une miette reste, sous le toit rouge.",
            f"{CHILD}|J'ai versé, sans courir.",
            "narrateur|La tasse sent le foin, près de la poule.",
        ],
    }
    return vet(lines[(a, b, c)])


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple[list[str], str, str, dict]] = {}

    scripts["CHK_T0000_P0000"] = (
        OPENING,
        "opening",
        "paille,seau,portail",
        {"emphasis": "grain de paille"},
    )
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "les cubes",
            "option_2_label": "le livre",
            "option_3_label": "la dînette",
            "pause_before_ms": 200,
        },
    )

    t2_labs = ("une pomme", "un yaourt", "un morceau de pain")
    t3_labs = ("le chat", "le chien", "la poule")
    t2_sons = {1: "pomme,croque", 2: "yaourt,pot", 3: "pain,miette"}
    t2_emp = {1: "pomme", 2: "yaourt", 3: "pain"}
    t3_sons = {1: "chat,grange", 2: "chien,niche", 3: "poule,toit"}
    fin_sons = {1: "seau,auge", 2: "seau,niche", 3: "seau,nid"}

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        t1 = T1[a]
        scripts[base] = (t1["passage"], "action", t1["sons"], {"emphasis": t1["emp"]})
        scripts[f"{base}_Q0001"] = (
            t1["question"],
            "clue",
            "",
            {
                "expected_answer": t1["ans"],
                "accepted_examples": t1["acc"],
                "retry_prompt": t1["retry"],
                "engine_ok_text": t1["ok"],
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
                "emphasis": t1["ans"],
                "pause_before_ms": 200,
            },
        )
        scripts[f"{base}_C0001"] = (
            t1["confirm"],
            "confirm",
            t1["sons"],
            {"emphasis": "seau"},
        )
        scripts[f"{base}_T0002_P0000"] = (
            T2_CHOICE[a],
            "choice",
            "",
            {
                "option_1_label": t2_labs[0],
                "option_2_label": t2_labs[1],
                "option_3_label": t2_labs[2],
                "pause_before_ms": 200,
            },
        )
        for b in (1, 2, 3):
            leaf2 = f"{base}_T0002_P000{b}"
            scripts[leaf2] = (
                t2_scene(a, b),
                "obstacle",
                t2_sons[b],
                {"emphasis": t2_emp[b]},
            )
            scripts[f"{leaf2}_T0003_P0000"] = (
                T3_CHOICE[b],
                "choice",
                "",
                {
                    "option_1_label": t3_labs[0],
                    "option_2_label": t3_labs[1],
                    "option_3_label": t3_labs[2],
                    "pause_before_ms": 200,
                },
            )
            for c in (1, 2, 3):
                leaf3 = f"{leaf2}_T0003_P000{c}"
                scripts[leaf3] = (
                    t3_scene(a, b, c),
                    "resolution",
                    t3_sons[c],
                    {"emphasis": "grain de paille"},
                )
                scripts[f"{leaf3}_F0001"] = (
                    ending(a, b, c),
                    "ending",
                    fin_sons[c],
                    {"emphasis": "grain de paille", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra)[:8]}")

    chunks = []
    for c in src["chunks"]:
        cid = c["chunk_id"]
        lines, profile, sons, extra = scripts[cid]
        chunks.append(voice(by_src[cid], lines, profile, sons, extra))

    fins = [ch["text"] for ch in chunks if ch["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(fins))}/27")
    last_n = []
    for ch in chunks:
        if ch.get("kind") != "passage_fin":
            continue
        last = [x for x in ch["script"].splitlines() if x.startswith("narrateur|")][-1]
        last_n.append(last.split("|", 1)[1])
        last_low = last.split("|", 1)[1].lower()
        if "histoire" in last_low or "bravo" in last_low or "bon travail" in last_low:
            raise SystemExit(f"{ch['chunk_id']} fin mécanique: {last_low}")
    if len(set(last_n)) != 27:
        raise SystemExit(f"dernières images: {len(set(last_n))}/27")
    res_txt = [
        ch["text"]
        for ch in chunks
        if ch["kind"] == "passage"
        and "_T0003_P000" in ch["chunk_id"]
        and "_F0001" not in ch["chunk_id"]
        and not ch["chunk_id"].endswith("_T0003_P0000")
    ]
    if len(res_txt) != 27 or len(set(res_txt)) != 27:
        raise SystemExit(f"résolutions distinctes: {len(set(res_txt))}/{len(res_txt)}")
    t2_only = [
        ch["text"]
        for ch in chunks
        if ch["kind"] == "passage" and "_T0002_P000" in ch["chunk_id"] and "T0003" not in ch["chunk_id"]
    ]
    if len(t2_only) != 9 or len(set(t2_only)) != 9:
        raise SystemExit(f"T2 distincts: {len(set(t2_only))}/{len(t2_only)}")

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "seau jaune" not in blob:
        raise SystemExit(f"{SID}: seau jaune absent")
    if "grain de paille" not in chunks[0]["text"].lower():
        raise SystemExit("indice absent de l'ouverture")
    for ch in chunks:
        if (
            ch["kind"] == "passage"
            and "T0003_P000" in ch["chunk_id"]
            and "_F0001" not in ch["chunk_id"]
            and not ch["chunk_id"].endswith("T0003_P0000")
        ):
            if "grain de paille" not in ch["text"].lower():
                raise SystemExit(f"indice non payé: {ch['chunk_id']}")
    for tic in ("tout doux", "tout calme", " aujourd'hui,"):
        if tic in blob:
            raise SystemExit(f"{SID}: tic {tic}")
    if TICS.search(blob):
        raise SystemExit(f"{SID}: tic corpus {TICS.search(blob).group(0)}")
    for bad in (
        "merle",
        "couleur de miel",
        "tom ",
        "léa",
        "sami",
        "hugo",
        "nino",
        "aniss",
        "pompe",
        "laitue",
        "brin de paille",
    ):
        if bad in blob:
            raise SystemExit(f"{SID}: interdit {bad}")
    adults = [ln for ln in blob.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    aj = " ".join(a.split("|", 1)[1] if "|" in a else a for a in adults)
    if "merci" not in aj:
        raise SystemExit(f"{SID}: merci absent des adultes")

    out = dict(src)
    out["fil_rouge"] = (
        "Sarah connaît la ferme, toit par toit. Sous le toit rouge, un détail "
        "paraît neuf : un grain de paille colle au bord du seau jaune. Elle "
        "veut porter le seau jusqu'à l'auge du hangar, avant que le vent "
        "prenne la botte ouverte. Elle tire trop fort ; l'anse résiste, "
        "prise dans la paille. Papa s'accroupit. Cubes, livre ou dînette : "
        "le seau part avec elle. Un objet tombe ou reste. Elle le reprend. "
        "Pomme, yaourt ou pain cachent le grain. Elle refuse de foncer. "
        "Chat, chien ou poule : elle observe, pose, verse. Le grain paie "
        "le début. Vingt-sept traces."
    )
    out["title"] = TITLE
    out["characters"] = "Sarah, papa, maman"
    out["setting"] = "à la ferme, toit rouge, paille"
    out["chunks"] = chunks
    check(SID, out["age_band"], out["chunks"])

    def path_words(a: int, b: int, c: int) -> int:
        ids = [
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
        mp = {ch["chunk_id"]: ch for ch in chunks}
        return sum(words(mp[i]["text"]) for i in ids)

    lengths = [path_words(a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    if min(lengths) < 380:
        raise SystemExit(f"chemin trop court: {min(lengths)}")

    t1s = [next(ch["text"] for ch in chunks if ch["chunk_id"] == f"CHK_T0001_P000{i}") for i in (1, 2, 3)]
    if len(set(t1s)) < 3:
        raise SystemExit("T1 ne change pas l'histoire")
    t2s = [
        next(ch["text"] for ch in chunks if ch["chunk_id"] == f"CHK_T0001_P0001_T0002_P000{j}")
        for j in (1, 2, 3)
    ]
    if len(set(t2s)) < 3:
        raise SystemExit("T2 ne change pas l'histoire")
    t3s = [
        next(
            ch["text"]
            for ch in chunks
            if ch["chunk_id"] == f"CHK_T0001_P0001_T0002_P0001_T0003_P000{k}"
        )
        for k in (1, 2, 3)
    ]
    if len(set(t3s)) < 3:
        raise SystemExit("T3 ne change pas l'histoire")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in chunks)
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        "# TREE-AUT-011 — Le seau jaune de Sarah\n\n"
        "- **Nouveau titre :** *Le seau jaune de Sarah*\n"
        "- **Public :** 3–4 ans (N1), lecture interactive familiale\n"
        "- **Leçon principale :** AUT.AFF.003 — reprendre / ranger ses affaires "
        "(vécue, non dite)\n"
        "- **Personnages :** Sarah, papa, maman\n"
        "- **Structure conservée :** 86 nœuds, trois choix à trois options, "
        "27 chemins et 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Sarah connaît la ferme, toit par toit. Sous le toit rouge, un détail "
        "paraît neuf : un grain de paille colle au bord du seau jaune. Elle "
        "veut porter le seau jusqu'à l'auge du hangar, avant que le vent "
        "prenne la botte ouverte. Elle tire trop fort ; l'anse résiste. Papa "
        "s'accroupit. Cubes, livre ou dînette : le seau part avec elle. Un "
        "objet tombe ou reste ; elle le reprend. Pomme, yaourt ou pain "
        "cachent le grain. Elle refuse de foncer. Chat, chien ou poule : "
        "elle observe, pose, verse. Le grain paie l'ouverture. Le seau a "
        "failli rester.\n\n"
        "## Améliorations appliquées\n\n"
        "- Ouverture inventée (ferme connue, détail neuf), pas le gabarit "
        "F-NAR-016.\n"
        "- Indice unique : grain de paille, payé à chaque climax et chaque fin.\n"
        "- Corps : sourire disparu, poitrine bousculée, adulte accroupi.\n"
        "- Première idée échoue (anse prise, cube / page / tasse). Seconde "
        "ruse : le goûter cache le grain. Sarah refuse de foncer.\n"
        "- T1/T2/T3 changent l'action. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- 1er choix : le seau part avec elle.\n"
        "- Un merci vécu (ouverture). Papa et maman parlent. Une question.\n"
        "- Pas de 2e enfant. Pas « encore / déjà / tout doux ». Pas merle, "
        "pas miel, pas apply.\n"
        "- Monde ≠ TREE-AUT-008 (Aniss, seau jaune, cour), ≠ TREE-AUT-040 "
        "(Amir, ferme, pompe), ≠ TREE-AUT-019 (bidon, brin, Nino).\n\n"
        "## Direction vocale\n\n"
        "TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/"
        "ending) : notes, text_ssml, text_xai_tags, piper 1.10–1.30.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, {min(lengths)} à {max(lengths)} mots, moyenne {sum(lengths)//len(lengths)}\n"
        "- 27 fins et 27 dernières images distinctes\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés\n"
        "- N1 ≤ 10 mots/phrase. `check()` OK.\n\n"
        "## Relu\n\n"
        "P0000, 3 L1, 9 L2, 27 résolutions, 27 fins. Questions liées à la scène "
        "(cube / paille / tasse). Impatience, découragement, fierté calme.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(
        f"OK {SID} {nwords} mots  fins={len(set(fins))}  "
        f"chemins {min(lengths)}-{max(lengths)} moy {sum(lengths)//len(lengths)}  "
        f"1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}"
    )


if __name__ == "__main__":
    main()
