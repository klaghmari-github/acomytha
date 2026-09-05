#!/usr/bin/env python3
"""TREE-AUT-009 — Le sac bleu de Victorino (F-NAR-019, N2, AUT.AFF.001, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-009"
N2 = LIMITS["N2"]
TITLE = "Le sac bleu de Victorino"
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
    "ombre en forme de flèche",
    "dent de laitue",
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
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="dent de fermeture dorée",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=le_sac_résiste_au_crochet; "
            "tempo=naturel; volume=medium; sourire=léger; respiration=ample; "
            "pause=tic_du_radiateur"
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
        emphasis="sac",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=regarde_ce_qui_s_est_passé; "
            "tempo=suspendu; volume=soft; sourire=aucun; "
            "respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="sac",
        note=(
            "arc=confirmation; intention=relancer; emotion=élan; intensite=1; "
            "destinataire=enfant; sous_texte=les_affaires_ont_une_place; "
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
            "destinataire=enfant; sous_texte=il_tire_trop_vite; "
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
            "sous_texte=l_objet_résiste_ou_disparaît; tempo=resserré; "
            "volume=medium; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="dent de fermeture dorée",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; "
            "emotion=fierté_calme; intensite=2; destinataire=enfant; "
            "sous_texte=la_dent_dorée_paie_le_début; tempo=naturel; "
            "volume=medium; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="dent de fermeture dorée",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; sous_texte=le_sac_revient_au_crochet; "
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


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=dent_dorée_au_crochet_{a}{b}{c}; "
        f"tempo={tempos[c]}; volume=soft; sourire=léger; respiration=ample; "
        f"chemin={a}{b}{c}"
    )


# Ouverture inventée : l'ombre du crochet fait un bateau sur le mur.
# Indice unique : une dent de fermeture dorée.
OPENING = vet(
    [
        "narrateur|L'ombre du crochet dessine un petit bateau, sur le mur.",
        "narrateur|Un carré de soleil s'assoit sur le tapis, chaud.",
        "narrateur|Le radiateur du salon fait tic, lent, métallique.",
        "narrateur|Ça sent le pain, près de la cuisine.",
        "narrateur|Victorino vit là, avec papa et maman.",
        "narrateur|Au crochet, le sac bleu penche, un peu lourd.",
        "narrateur|Une dent de fermeture dorée attrape le rayon.",
        "papa|Tu as vu cette dent, Victorino ?",
        "enfant-m|Elle brille, je veux sortir vite !",
        "maman|Tes affaires voyagent mieux, dans le sac.",
        "narrateur|En ce moment, Victorino tire le sac, trop fort.",
        "narrateur|La sangle résiste, coincée au crochet.",
        "enfant-m|Ça ne vient pas !",
        "narrateur|Le sourire de Victorino disparaît.",
        "narrateur|Le sac tombe, mou, presque vide.",
        "narrateur|La dent dorée reste, seule, contre le tissu.",
        "papa|Merci d'avoir dit ce que tu veux.",
        "narrateur|Papa s'accroupit, à la même hauteur.",
        "maman|Le crochet attend tes mains, pas la course.",
        "enfant-m|Je le prends, et je mets dedans.",
        "narrateur|Le tapis est doux, rêche au bord.",
        "narrateur|Une cuillère tape un bol, tout près.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|Le sac bleu est dans ses bras, un peu lourd.",
        "narrateur|La cuisine, le jardin, ou la chambre.",
        "maman|Où vas-tu d'abord, avec le sac ?",
    ]
)

T1 = {
    1: dict(
        lab="la cuisine",
        ans="tiré",
        acc="tiré | il tire | sangle | la sangle | doucement | le sac",
        retry="La sangle tenait à la chaise. Victorino a fait quoi ?",
        ok="Oui, il a tiré la sangle.",
        sons="chaise,carrelage,pain",
        emp="sangle",
        passage=vet(
            [
                "narrateur|Victorino porte le sac vers la cuisine.",
                "narrateur|Le carrelage pique, un peu froid.",
                "narrateur|Ça sent le pain, tout près du four.",
                "enfant-m|Un morceau, pour le chemin !",
                "narrateur|Il pose le pain sur la chaise, trop vite.",
                "narrateur|La sangle accroche le pied de la chaise.",
                "enfant-m|Ça tient, ça ne vient pas !",
                "narrateur|Il tire trop fort, d'un coup.",
                "narrateur|La chaise crie, un petit cri de bois.",
                "narrateur|Le sac se tord, et la dent dorée se coince.",
                "narrateur|Ses épaules baissent, près du carrelage.",
                "papa|La sangle, un cran, pas tout d'un coup.",
                "maman|Le pain voyage mieux, dans le sac.",
                "narrateur|Victorino tire, plus lent, cran par cran.",
                "narrateur|La sangle se libère, lisse sous les doigts.",
                "enfant-m|Il est dedans, le pain !",
                "narrateur|La dent dorée redevient visible, un instant.",
            ]
        ),
        question=vet(
            [
                "narrateur|La sangle tenait à la chaise.",
                "papa|Victorino a fait quoi ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Victorino a tiré la sangle, cran par cran.",
                "enfant-m|Le pain est au fond.",
                "papa|La chaise a lâché, grâce à toi.",
                "maman|Le sac vient, où tu vas.",
                "enfant-m|On choisit un jeu, alors ?",
                "narrateur|La dent dorée luit, un peu, sur le bleu.",
            ]
        ),
    ),
    2: dict(
        lab="le jardin",
        ans="au fond",
        acc="au fond | dans le sac | le sac | doudou | il était là",
        retry="Le doudou n'était pas sur la dalle. Il était où ?",
        ok="Oui, au fond du sac.",
        sons="porte,herbe,dalle",
        emp="doudou",
        passage=vet(
            [
                "narrateur|Victorino pousse la porte du jardin, le sac au bras.",
                "narrateur|L'herbe mouille le bas des chaussures.",
                "narrateur|Une dalle chaude attend, près du pas.",
                "enfant-m|Je veux voir dehors, maman !",
                "maman|Le sac vient, alors.",
                "narrateur|Le crochet du dehors a mouillé la sangle.",
                "enfant-m|Elle est froide !",
                "narrateur|Il reverse le sac, trop vite, sur la dalle.",
                "narrateur|Le tissu gris glisse, puis disparaît.",
                "enfant-m|Mon doudou n'est pas là !",
                "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
                "papa|Regarde le sac, pas seulement la dalle.",
                "maman|Personne ne dit où courir.",
                "narrateur|Il plonge la main, tout au fond.",
                "narrateur|Le doudou est là, un peu tassé.",
                "enfant-m|Au fond !",
                "narrateur|Il le serre, puis le remet, dans le bleu.",
            ]
        ),
        question=vet(
            [
                "narrateur|Le doudou n'était pas sur la dalle.",
                "maman|Il était où ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Victorino a cherché au fond du sac.",
                "enfant-m|Il était là.",
                "maman|Au fond, pas sur la dalle.",
                "papa|Le jardin est à nous, avec le sac.",
                "enfant-m|On choisit un jeu, alors ?",
                "narrateur|La dent dorée sèche, un peu, au soleil.",
            ]
        ),
    ),
    3: dict(
        lab="la chambre",
        ans="tiré",
        acc="tiré | il tire | sangle | sous le lit | le sac",
        retry="La sangle était sous le lit. Il a tiré. Il a fait quoi ?",
        ok="Oui, il a tiré la sangle.",
        sons="lit,tissu,chambre",
        emp="sangle",
        passage=vet(
            [
                "narrateur|Victorino monte le sac vers la chambre.",
                "narrateur|Un rayon passe entre les rideaux.",
                "narrateur|La couverture est douce sous la main.",
                "enfant-m|On sort, après ?",
                "papa|Oui, vers le village.",
                "narrateur|La sangle a glissé sous le lit.",
                "enfant-m|Elle est partie !",
                "narrateur|Il se jette à genoux, trop vite.",
                "narrateur|Le sac s'ouvre, et le fond se vide.",
                "enfant-m|Tout est tombé !",
                "narrateur|Ses épaules baissent, près de la poussière.",
                "maman|À genoux, un cran, pas tout d'un coup.",
                "papa|La sangle d'abord, puis le fond.",
                "narrateur|Victorino tire la sangle, centimètre par centimètre.",
                "narrateur|Une poussière vole, collée à la dent dorée.",
                "enfant-m|Je l'ai, le sac !",
                "narrateur|Il ouvre, et le doudou tient, au fond.",
            ]
        ),
        question=vet(
            [
                "narrateur|La sangle était sous le lit.",
                "papa|Victorino a fait quoi ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Victorino a tiré la sangle, hors du lit.",
                "enfant-m|Je l'ai, le sac.",
                "maman|Sous le lit, puis dans tes bras.",
                "papa|On peut choisir un jeu, maintenant.",
                "enfant-m|Oui, papa.",
                "narrateur|Une poussière brille, collée à la dent dorée.",
            ]
        ),
    ),
}

T2_CHOICE = {
    1: vet(
        [
            "narrateur|Le pain peut voyager, si quelque chose l'accompagne.",
            "papa|Les cubes, le livre, ou la dînette ?",
            "maman|Le sac bleu vient avec toi.",
        ]
    ),
    2: vet(
        [
            "narrateur|Dehors, le sac a besoin d'un jeu, pour tenir.",
            "maman|Les cubes, le livre, ou la dînette ?",
            "papa|Le sac bleu vient avec toi.",
        ]
    ),
    3: vet(
        [
            "narrateur|La chambre a des jeux, qui veulent une place.",
            "papa|Les cubes, le livre, ou la dînette ?",
            "maman|Le sac bleu vient avec toi.",
        ]
    ),
}


def t2_scene(a: int, b: int) -> list[str]:
    table = {
        (1, 1): [
            "narrateur|Près du four, les cubes attendent, sur le carrelage.",
            "narrateur|Victorino jette les cubes dans le sac, trop vite.",
            "enfant-m|Ils rentrent, d'un coup !",
            "narrateur|Ils rebondissent, et un cube file sous la chaise.",
            "narrateur|Le sac se tait, trop léger.",
            "enfant-m|Ils ne restent pas !",
            "narrateur|Le sourire de Victorino disparaît.",
            "papa|Personne ne dit où courir.",
            "maman|La chaise a un secret, peut-être.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il observe le sac, puis la dent dorée.",
            "narrateur|La dent pointe vers la chaise, minuscule.",
            "enfant-m|Il est là, le cube perdu !",
            "narrateur|Un cube bleu brille, sous le bois.",
        ],
        (1, 2): [
            "narrateur|Sur la table, le livre est trop large, près du pain.",
            "narrateur|Victorino le plante debout, dans le sac.",
            "enfant-m|Il rentre, je force !",
            "narrateur|La fermeture se coince, sur la dent dorée.",
            "narrateur|Le livre glisse vers la chaise, pages ouvertes.",
            "enfant-m|Il ne veut pas !",
            "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
            "papa|Personne ne donne la réponse.",
            "maman|Regarde la dent, pas seulement le livre.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il écoute le lieu, et le four souffle, tout près.",
            "narrateur|La dent dorée cligne, vers les pages à plat.",
            "enfant-m|Couché, pas debout !",
            "narrateur|Une page sent le pain, contre le bleu.",
        ],
        (1, 3): [
            "narrateur|Près de l'évier, la tasse de dînette tremble.",
            "narrateur|Victorino la pose sur le bord du sac.",
            "enfant-m|Elle vient, avec nous !",
            "narrateur|La tasse roule, vers le frigo, trop vite.",
            "narrateur|Il a failli laisser le sac, pour courir.",
            "enfant-m|Elle part toute seule !",
            "narrateur|Ses épaules baissent, près du carrelage.",
            "maman|Personne ne dit de foncer.",
            "papa|La tasse a un bruit, sous la table.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il s'arrête, et la dent dorée cligne, vers le bois.",
            "narrateur|Un petit son de porcelaine répond, dessous.",
            "enfant-m|Elle est là, cachée !",
            "narrateur|La tasse garde un goût de pain, minuscule.",
        ],
        (2, 1): [
            "narrateur|Sur la dalle chaude, les cubes attendent, un peu humides.",
            "narrateur|Victorino les jette dans le sac, trop vite.",
            "enfant-m|Ils rentrent, d'un coup !",
            "narrateur|Un cube file dans l'herbe, et disparaît.",
            "narrateur|La sangle mouillée pèse, trop lourde.",
            "enfant-m|Il s'est caché !",
            "narrateur|Le sourire de Victorino disparaît.",
            "papa|Personne ne dit où courir.",
            "maman|L'herbe a un secret, peut-être.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il observe le sac, puis la dent dorée.",
            "narrateur|La dent s'éteint, puis pointe vers l'herbe.",
            "enfant-m|Un coin bleu, dans le vert !",
            "narrateur|Un cube garde une goutte d'herbe, froide.",
        ],
        (2, 2): [
            "narrateur|Près du portail, le livre s'ouvre, trop large.",
            "narrateur|Victorino le plaque dans le sac, trop fort.",
            "enfant-m|Les pages, vite !",
            "narrateur|Le vent soulève une page, et la plie.",
            "narrateur|La fermeture se coince, sur la dent dorée.",
            "enfant-m|Il ne veut pas rentrer !",
            "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
            "maman|Personne ne donne la réponse.",
            "papa|Regarde la dent, pas le vent.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il écoute le jardin, et le portail claque, loin.",
            "narrateur|La dent dorée cligne, vers les pages à plat.",
            "enfant-m|Fermé, puis au fond !",
            "narrateur|Une page sent l'air du jardin, froide.",
        ],
        (2, 3): [
            "narrateur|Sur la dalle, la tasse de dînette sonne, claire.",
            "narrateur|Victorino la pose trop haut, sur le sac.",
            "enfant-m|Elle vient dehors !",
            "narrateur|Une goutte du crochet tombe, dans la tasse.",
            "narrateur|La tasse roule vers l'herbe, trop vite.",
            "enfant-m|Elle va se perdre !",
            "narrateur|Ses épaules baissent, près de la dalle.",
            "papa|Personne ne dit de foncer.",
            "maman|La tasse a un rond, qui brille.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il s'arrête, et la dent dorée cligne, vers l'herbe.",
            "narrateur|Un petit son de porcelaine répond, dans le vert.",
            "enfant-m|Je la prends, sans courir !",
            "narrateur|La tasse a un rond d'eau, minuscule.",
        ],
        (3, 1): [
            "narrateur|Sur le lit, les cubes font une petite tour.",
            "narrateur|Victorino les jette dans le sac, trop vite.",
            "enfant-m|Ils rentrent, d'un coup !",
            "narrateur|Un cube file sous le lit, et sonne.",
            "narrateur|Le sac s'ouvre, trop large, près de l'oreiller.",
            "enfant-m|Il est parti dessous !",
            "narrateur|Le sourire de Victorino disparaît.",
            "papa|Personne ne dit de plonger.",
            "maman|Le lit a un secret, peut-être.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il observe le sac, puis la dent dorée.",
            "narrateur|La dent pointe vers le bas, minuscule.",
            "enfant-m|Comme la sangle, tout à l'heure !",
            "narrateur|Un cube a pris la poussière du lit.",
        ],
        (3, 2): [
            "narrateur|Sous l'oreiller, le livre dort, trop plat.",
            "narrateur|Victorino tire le livre, d'un coup.",
            "enfant-m|Il vient, vite !",
            "narrateur|L'oreiller avale une page, et la tient.",
            "narrateur|La fermeture se coince, sur la dent dorée.",
            "enfant-m|Il ne veut pas !",
            "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
            "maman|Personne ne donne la réponse.",
            "papa|Regarde la dent, pas seulement l'oreiller.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il écoute la chambre, et un rayon tremble, au mur.",
            "narrateur|La dent dorée cligne, vers la page pliée.",
            "enfant-m|Doucement, je glisse la page !",
            "narrateur|Une page sent l'oreiller, un peu tiède.",
        ],
        (3, 3): [
            "narrateur|Dans la couverture, la tasse de dînette se cache.",
            "narrateur|Victorino secoue le drap, trop fort.",
            "enfant-m|Sors, tasse !",
            "narrateur|La tasse roule sous le lit, et sonne.",
            "narrateur|Il a failli tout vider, d'un coup.",
            "enfant-m|Elle est partie dessous !",
            "narrateur|Ses épaules baissent, près de la poussière.",
            "papa|Personne ne dit de tout jeter.",
            "maman|La tasse a un son, sous le bois.",
            "enfant-m|Je ne fonce pas.",
            "narrateur|Il s'arrête, et la dent dorée cligne, vers le lit.",
            "narrateur|Un petit son de porcelaine répond, dessous.",
            "enfant-m|Je m'allonge, et je la prends !",
            "narrateur|La tasse s'est nichée, contre le doudou.",
        ],
    }
    return vet(table[(a, b)])


T3_CHOICE = {
    1: vet(
        [
            "narrateur|Les cubes veulent une heure, pour voyager.",
            "papa|Le matin, après la sieste, ou le soir ?",
            "maman|Le sac bleu part avec toi.",
        ]
    ),
    2: vet(
        [
            "narrateur|Le livre attend une heure, pour voyager.",
            "maman|Le matin, après la sieste, ou le soir ?",
            "papa|Le sac bleu part avec toi.",
        ]
    ),
    3: vet(
        [
            "narrateur|La tasse attend une heure, pour voyager.",
            "papa|Le matin, après la sieste, ou le soir ?",
            "maman|Le sac bleu part avec toi.",
        ]
    ),
}

WHEN = {
    1: dict(lab="le matin", start="Au matin, la lumière est fraîche, près de la porte."),
    2: dict(lab="après la sieste", start="Après la sieste, le rideau fait un carré chaud."),
    3: dict(lab="le soir", start="Le soir, la lampe allume le tapis, tout près."),
}
TOY = {
    1: dict(lab="les cubes", pack="Victorino glisse un cube, puis l'autre, à plat.", child="les cubes"),
    2: dict(lab="le livre", pack="Victorino couche le livre, pages vers le fond.", child="le livre"),
    3: dict(lab="la tasse", pack="Victorino niche la tasse, contre le doudou.", child="la tasse"),
}
PLACE = {
    1: dict(lab="la cuisine", almost="Le pain a failli rester sur la chaise.", ou="dans la cuisine"),
    2: dict(lab="le jardin", almost="Le doudou a failli rester dans l'herbe.", ou="près du jardin"),
    3: dict(lab="la chambre", almost="La sangle a failli rester sous le lit.", ou="dans la chambre"),
}

T3_LAST = {
    (1, 1, 1): "Une miette de matin colle à la dent dorée.",
    (1, 1, 2): "Un cube tiède attend, sous la dent dorée.",
    (1, 1, 3): "La lampe allume un cube, derrière la dent.",
    (1, 2, 1): "Une page de matin sent le pain, au fond.",
    (1, 2, 2): "Le livre fait un toit, sous le rideau.",
    (1, 2, 3): "La lampe glisse sur la couverture du livre.",
    (1, 3, 1): "La tasse du matin sonne, toute petite.",
    (1, 3, 2): "La tasse de sieste ne roule plus.",
    (1, 3, 3): "La tasse du soir cache un reflet de lampe.",
    (2, 1, 1): "Un cube d'herbe sèche, contre la dent dorée.",
    (2, 1, 2): "Un cube tiède sent la dalle, au fond.",
    (2, 1, 3): "Un cube du soir garde une poussière d'herbe.",
    (2, 2, 1): "Une page d'air frais reste un peu froide.",
    (2, 2, 2): "Le livre de sieste sent la dalle chaude.",
    (2, 2, 3): "Le livre du soir sent le portail, fermé.",
    (2, 3, 1): "La tasse du jardin sonne, au matin clair.",
    (2, 3, 2): "La tasse de sieste a perdu sa goutte.",
    (2, 3, 3): "La tasse du soir reflète le portail.",
    (3, 1, 1): "Un cube de lit brille, sous la dent dorée.",
    (3, 1, 2): "Un cube de sieste dort, contre le doudou.",
    (3, 1, 3): "Un cube du soir garde la poussière du lit.",
    (3, 2, 1): "Le livre du matin sent l'oreiller, tiède.",
    (3, 2, 2): "Le livre de sieste fait un toit, au lit.",
    (3, 2, 3): "Le livre du soir garde un pli d'oreiller.",
    (3, 3, 1): "La tasse du lit sonne, au matin clair.",
    (3, 3, 2): "La tasse de sieste s'est nichée, au chaud.",
    (3, 3, 3): "La tasse du soir cache un rond de lampe.",
}

T3_PAPA = {
    (1, 1, 1): "Tes cubes ont une place, près du pain.",
    (1, 1, 2): "Tes cubes ont attendu la sieste, au chaud.",
    (1, 1, 3): "Tes cubes ont une place, sous la lampe.",
    (1, 2, 1): "Le livre a une place, près du four.",
    (1, 2, 2): "Le livre a attendu le rideau, à plat.",
    (1, 2, 3): "Le livre a une place, sous la lampe.",
    (1, 3, 1): "La tasse a une place, près du pain.",
    (1, 3, 2): "La tasse a attendu, sans rouler.",
    (1, 3, 3): "La tasse a une place, sous la lampe.",
    (2, 1, 1): "Tes cubes ont une place, malgré l'herbe.",
    (2, 1, 2): "Tes cubes ont séché, pendant la sieste.",
    (2, 1, 3): "Tes cubes ont une place, malgré le soir.",
    (2, 2, 1): "Le livre a une place, malgré le vent.",
    (2, 2, 2): "Le livre a attendu la dalle, à plat.",
    (2, 2, 3): "Le livre a une place, malgré le portail.",
    (2, 3, 1): "La tasse a une place, malgré la goutte.",
    (2, 3, 2): "La tasse a perdu sa goutte, au chaud.",
    (2, 3, 3): "La tasse a une place, malgré le soir.",
    (3, 1, 1): "Tes cubes ont une place, hors du lit.",
    (3, 1, 2): "Tes cubes ont dormi, puis voyagé.",
    (3, 1, 3): "Tes cubes ont une place, sous la lampe.",
    (3, 2, 1): "Le livre a une place, hors de l'oreiller.",
    (3, 2, 2): "Le livre a attendu le rideau, à plat.",
    (3, 2, 3): "Le livre a une place, hors du pli.",
    (3, 3, 1): "La tasse a une place, hors du drap.",
    (3, 3, 2): "La tasse a attendu, contre le doudou.",
    (3, 3, 3): "La tasse a une place, sous la lampe.",
}


def t3_scene(a: int, b: int, c: int) -> list[str]:
    pl, ty, wh = PLACE[a], TOY[b], WHEN[c]
    child = f"{wh['lab'].capitalize()}, {ty['child']} dans le sac !"
    if wh["lab"] == "après la sieste":
        child = f"Après la sieste, {ty['child']} dans le sac !"
    place_ok = {1: "Ils ont une place", 2: "Il a une place", 3: "Elle a une place"}[b]
    return vet(
        [
            f"narrateur|{wh['start']}",
            f"narrateur|Le sac bleu est {pl['ou']}, un peu lourd.",
            f"enfant-m|{child}",
            f"narrateur|{pl['almost']}",
            "enfant-m|Je ne force pas.",
            "narrateur|Il s'arrête, et la dent de fermeture dorée cligne.",
            f"narrateur|{ty['pack']}",
            "narrateur|La dent dorée glisse, puis tient.",
            f"papa|{T3_PAPA[(a, b, c)]}",
            f"enfant-m|{place_ok}, {wh['lab']} !",
            "maman|Le quai du tapis peut attendre dehors.",
            f"narrateur|{T3_LAST[(a, b, c)]}",
        ]
    )


END_FIRST = {
    1: "Plus tard, le salon retrouve son tic de radiateur.",
    2: "Plus tard, un carré de soleil dort sur le tapis.",
    3: "Plus tard, l'ombre du crochet redevient un bateau.",
}
END_ASK = {
    1: "Tes cubes ont voyagé, {when} ?",
    2: "Le livre a voyagé, {when} ?",
    3: "La tasse a voyagé, {when} ?",
}
END_RECAP = {
    (1, 1, 1): "J'ai glissé les cubes, le matin, près du pain.",
    (1, 1, 2): "J'ai glissé les cubes, après la sieste, au chaud.",
    (1, 1, 3): "J'ai glissé les cubes, le soir, sous la lampe.",
    (1, 2, 1): "J'ai couché le livre, le matin, près du four.",
    (1, 2, 2): "J'ai couché le livre, après la sieste, à plat.",
    (1, 2, 3): "J'ai couché le livre, le soir, sous la lampe.",
    (1, 3, 1): "J'ai niché la tasse, le matin, près du pain.",
    (1, 3, 2): "J'ai niché la tasse, après la sieste, sans rouler.",
    (1, 3, 3): "J'ai niché la tasse, le soir, sous la lampe.",
    (2, 1, 1): "J'ai glissé les cubes, le matin, malgré l'herbe.",
    (2, 1, 2): "J'ai glissé les cubes, après la sieste, tout secs.",
    (2, 1, 3): "J'ai glissé les cubes, le soir, malgré l'herbe.",
    (2, 2, 1): "J'ai couché le livre, le matin, malgré le vent.",
    (2, 2, 2): "J'ai couché le livre, après la sieste, sur la dalle.",
    (2, 2, 3): "J'ai couché le livre, le soir, malgré le portail.",
    (2, 3, 1): "J'ai niché la tasse, le matin, malgré la goutte.",
    (2, 3, 2): "J'ai niché la tasse, après la sieste, sans eau.",
    (2, 3, 3): "J'ai niché la tasse, le soir, malgré le portail.",
    (3, 1, 1): "J'ai glissé les cubes, le matin, hors du lit.",
    (3, 1, 2): "J'ai glissé les cubes, après la sieste, hors du lit.",
    (3, 1, 3): "J'ai glissé les cubes, le soir, hors du lit.",
    (3, 2, 1): "J'ai couché le livre, le matin, hors de l'oreiller.",
    (3, 2, 2): "J'ai couché le livre, après la sieste, à plat.",
    (3, 2, 3): "J'ai couché le livre, le soir, hors du pli.",
    (3, 3, 1): "J'ai niché la tasse, le matin, hors du drap.",
    (3, 3, 2): "J'ai niché la tasse, après la sieste, au doudou.",
    (3, 3, 3): "J'ai niché la tasse, le soir, hors du drap.",
}
END_PAPA = {
    (1, 1, 1): "Le pain a voyagé, toi aussi.",
    (1, 1, 2): "La sieste a aidé les cubes, et toi.",
    (1, 1, 3): "La lampe a vu tes cubes, enfin calmes.",
    (1, 2, 1): "Le four a vu le livre, à plat.",
    (1, 2, 2): "Le rideau a gardé le livre, un moment.",
    (1, 2, 3): "La lampe a lu le dos du livre.",
    (1, 3, 1): "Le pain a senti la tasse, tout près.",
    (1, 3, 2): "La sieste a arrêté la tasse, sans rouler.",
    (1, 3, 3): "La lampe a vu la tasse, nichée.",
    (2, 1, 1): "L'herbe a rendu le cube, à tes mains.",
    (2, 1, 2): "La dalle a séché tes cubes, un peu.",
    (2, 1, 3): "Le soir a gardé l'herbe, hors du sac.",
    (2, 2, 1): "Le vent n'a pas pris le livre.",
    (2, 2, 2): "La dalle a tenu le livre, à plat.",
    (2, 2, 3): "Le portail a laissé le livre, au fond.",
    (2, 3, 1): "La goutte n'a pas suivi la tasse.",
    (2, 3, 2): "La sieste a bu la goutte, presque.",
    (2, 3, 3): "Le portail a vu la tasse, nichée.",
    (3, 1, 1): "Le lit n'a pas gardé tes cubes.",
    (3, 1, 2): "La sieste a rendu tes cubes, au sac.",
    (3, 1, 3): "Le soir a laissé la poussière, au lit.",
    (3, 2, 1): "L'oreiller a rendu le livre, à plat.",
    (3, 2, 2): "Le rideau a aidé le livre, à glisser.",
    (3, 2, 3): "Le pli a lâché le livre, le soir.",
    (3, 3, 1): "Le drap n'a pas gardé la tasse.",
    (3, 3, 2): "Le doudou a tenu la tasse, au chaud.",
    (3, 3, 3): "Le soir a niché la tasse, au fond.",
}
END_LAST = {
    (1, 1, 1): "Sur le tapis, le carré de soleil a glissé.",
    (1, 1, 2): "Le radiateur reprend son tic, plus lent.",
    (1, 1, 3): "L'ombre du crochet redevient un bateau, au mur.",
    (1, 2, 1): "Une miette de pain dort dans la dent dorée.",
    (1, 2, 2): "La sangle sent le carrelage, un peu froid.",
    (1, 2, 3): "Un cube a laissé une poussière bleue, au fond.",
    (1, 3, 1): "Le bol de la cuisine s'est tu, près du sac.",
    (1, 3, 2): "Le four sent moins fort, près du crochet.",
    (1, 3, 3): "Une chaise a repris sa place, près du sac.",
    (2, 1, 1): "La porte du jardin a gardé un fil d'herbe.",
    (2, 1, 2): "La dalle chaude a séché la sangle, toute seule.",
    (2, 1, 3): "Un rond d'eau a séché, sur le bleu.",
    (2, 2, 1): "Le portail a claqué, loin, une seule fois.",
    (2, 2, 2): "L'herbe a rendu un cube, tout petit.",
    (2, 2, 3): "Une page froide s'est réchauffée, au fond.",
    (2, 3, 1): "Le crochet du salon penche, plus léger.",
    (2, 3, 2): "La lampe a éteint la dent dorée, presque.",
    (2, 3, 3): "Un rayon a quitté le mur, sans le bateau.",
    (3, 1, 1): "La poussière du lit brille, collée à la dent.",
    (3, 1, 2): "L'oreiller a rendu le livre, sans un mot.",
    (3, 1, 3): "La couverture a gardé un creux de tasse.",
    (3, 2, 1): "Le doudou chauffe le fond, contre la tasse.",
    (3, 2, 2): "Une dent de fermeture dorée veille, fermée.",
    (3, 2, 3): "Le tapis rêche a gardé une trace de pas.",
    (3, 3, 1): "La cuillère du bol s'est tue, tout près.",
    (3, 3, 2): "Le sac bleu attend, au crochet, un peu lourd.",
    (3, 3, 3): "Papa a fermé la porte, et le tic continue.",
}
END_KEEP = {
    1: "Le sac bleu revient au crochet, un peu lourd.",
    2: "La dent de fermeture dorée veille, contre le tissu.",
    3: "Le quai du tapis est vide, et le sac est plein.",
}


def ending(a: int, b: int, c: int) -> list[str]:
    ask = END_ASK[b].format(when=WHEN[c]["lab"])
    return vet(
        [
            f"narrateur|{END_FIRST[a]}",
            f"maman|{ask}",
            f"enfant-m|{END_RECAP[(a, b, c)]}",
            f"narrateur|{END_KEEP[c]}",
            "narrateur|Voilà le sac bleu, au crochet, avec sa trace.",
            f"papa|{END_PAPA[(a, b, c)]}",
            f"narrateur|{END_LAST[(a, b, c)]}",
        ]
    )


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple[list[str], str, str, dict]] = {}

    scripts["CHK_T0000_P0000"] = (
        OPENING,
        "opening",
        "radiateur,sac,crochet",
        {"emphasis": "dent de fermeture dorée"},
    )
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "la cuisine",
            "option_2_label": "le jardin",
            "option_3_label": "la chambre",
            "pause_before_ms": 200,
        },
    )

    t2_labs = ("les cubes", "le livre", "la dînette")
    t3_labs = ("le matin", "après la sieste", "le soir")
    t2_sons = {1: "cubes,bois", 2: "livre,pages", 3: "tasse,dinette"}
    t2_emp = {1: "cubes", 2: "livre", 3: "tasse"}
    t3_sons = {1: "porte,matin", 2: "rideau,sieste", 3: "lampe,soir"}
    fin_sons = {1: "radiateur,crochet", 2: "tapis,sac", 3: "porte,tic"}

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
            },
        )
        scripts[f"{base}_C0001"] = (t1["confirm"], "confirm", t1["sons"], {"emphasis": "sac"})
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
                    {"emphasis": "dent de fermeture dorée"},
                )
                scripts[f"{leaf3}_F0001"] = (
                    ending(a, b, c),
                    "ending",
                    fin_sons[c],
                    {"emphasis": "dent de fermeture dorée", "note": ending_note(a, b, c)},
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
    if "victorino" not in blob:
        raise SystemExit(f"{SID}: Victorino absent")
    if "sac bleu" not in blob:
        raise SystemExit(f"{SID}: sac bleu absent")
    if "dent de fermeture dorée" not in chunks[0]["text"].lower():
        raise SystemExit("indice absent de l'ouverture")
    for ch in chunks:
        if (
            ch["kind"] == "passage"
            and "T0003_P000" in ch["chunk_id"]
            and "_F0001" not in ch["chunk_id"]
            and not ch["chunk_id"].endswith("T0003_P0000")
        ):
            if "dent de fermeture dorée" not in ch["text"].lower():
                raise SystemExit(f"indice non payé: {ch['chunk_id']}")
    for tic in ("tout doux", "tout calme", " aujourd'hui,"):
        if tic in blob:
            raise SystemExit(f"{SID}: tic {tic}")
    if TICS.search(blob):
        raise SystemExit(f"{SID}: tic corpus {TICS.search(blob).group(0)}")
    for bad in ("merle", "couleur de miel", "tom ", "léa", "sami", "laitue", "escargot"):
        if bad in blob:
            raise SystemExit(f"{SID}: interdit {bad}")

    out = dict(src)
    out["fil_rouge"] = (
        "L'ombre du crochet dessine un bateau sur le mur du salon. "
        "Victorino veut sortir : ses affaires doivent voyager dans le sac bleu, "
        "avant que papa ouvre la porte. Il tire trop fort ; la sangle résiste, "
        "le sac tombe, presque vide. Une dent de fermeture dorée reste, seule. "
        "Papa s'accroupit. Cuisine, jardin ou chambre : le sac part avec lui. "
        "Cubes, livre ou dînette : l'objet rebondit, se coince ou disparaît. "
        "Il refuse de foncer. Matin, sieste ou soir : il glisse, sans forcer. "
        "La dent paie le début. Vingt-sept traces au crochet."
    )
    out["title"] = TITLE
    out["characters"] = "Victorino, papa, maman"
    out["setting"] = "salon, sac bleu au crochet"
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

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        "# TREE-AUT-009 — Le sac bleu de Victorino\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "- **Titre :** *Le sac bleu de Victorino*\n"
        "- **Public :** 4–5 ans (N2), lecture interactive familiale\n"
        "- **Leçon :** AUT.AFF.001 — mettre dans le sac / les affaires à leur place "
        "(vécue, jamais dite)\n"
        "- **Personnages :** Victorino, papa, maman (un seul enfant)\n"
        "- **Monde :** salon, sac bleu au crochet, quai du tapis\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "L'ombre du crochet dessine un bateau sur le mur. Victorino veut sortir "
        "maintenant : ses affaires doivent voyager dans le sac bleu, avant que "
        "papa ouvre la porte. Il tire trop fort ; la sangle résiste, le sac "
        "tombe, presque vide. Une dent de fermeture dorée reste, seule. Papa "
        "s'accroupit, sans réciter la règle. Cuisine, jardin ou chambre : le sac "
        "part avec lui. Cubes, livre ou dînette : l'objet rebondit, se coince ou "
        "disparaît. Victorino refuse de foncer, observe la dent, glisse sans "
        "forcer. Matin, sieste ou soir changent la lumière. Le sac revient au "
        "crochet, avec une trace.\n\n"
        "## Vécu\n\n"
        "Impatience au crochet, petit découragement quand l'objet résiste, "
        "fierté calme quand il agit seul. L'adulte guide peu. Leçon dans le "
        "geste (glisser, nicher, coucher), jamais annoncée.\n\n"
        "## Vu et corrigé\n\n"
        "- Ouverture inventée (bateau d'ombre au mur), pas les cinq gabarits v2.\n"
        "- Indice unique : dent de fermeture dorée, payée au climax.\n"
        "- T1 = lieux (cuisine / jardin / chambre) : le sac part AVEC, on ne le retire pas.\n"
        "- T2 = cubes / livre / dînette : deuxième ruse, il refuse de foncer.\n"
        "- T3 = matin / après la sieste / le soir : 27 dénouements qui ont failli.\n"
        "- Monde ≠ TREE-AUT-046 (pas de sac jaune, banc, laitue, escargot).\n"
        "- Un merci vécu (ouverture). Papa/maman + questions. `en ce moment` une fois.\n"
        "- Pas merle, miel, encore, déjà, tout doux. Pas apply, pas git, pas audio.\n\n"
        "## Direction vocale\n\n"
        "TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending) : "
        "rate, pitch, volume, pauses, text_ssml, text_xai_tags, notes d'arc. "
        "slow réservé aux choix, au danger doux et aux émotions sensibles.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, {min(lengths)} à {max(lengths)} mots, moyenne {sum(lengths)//len(lengths)}\n"
        "- 27 fins et 27 dernières images distinctes\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés\n"
        "- N2 ≤ 15 mots/phrase. `check()` OK.\n\n"
        "## Relu\n\n"
        "P0000, 3 L1, 9 L2, 27 résolutions, 27 fins. Questions liées à la scène "
        "(tiré / au fond / tiré).\n\n"
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
