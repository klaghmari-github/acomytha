#!/usr/bin/env python3
"""ATOM-DIF.COR.003-03 — La prune violette du marché (F-NAR-019, N2, DIF.COR.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.003-03"
TITLE = "La prune violette du marché"
N2 = LIMITS["N2"]
CHARS = "Nino, Mila, papa, maman"
SETTING = (
    "marché : toiles, caisse de prunes, filet de coton, pain, "
    "balance, banc, pommes, menthe, œufs"
)
INDICE = "éclat de cageot"
FIL = (
    "Une toile claque. Sur la caisse, un éclat de cageot brille. "
    "Nino veut une prune violette, maintenant, avec Mila. Il saisit "
    "trop vite : la prune tombe, le filet se coince. Sourire parti. "
    "Mila arrive, lunettes neuves. Un rire commence. Il ferme la "
    "bouche, tend une prune. Merci vécu. Il lève trop haut : le jus "
    "tache, les lunettes bougent. Il refuse de foncer. L'éclat de "
    "cageot tient. La prune est partagée."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(botte|bottes|limace|perron|chaise|tiroir|fraisier|cuivre|"
    r"buis|coussin|figue|robinet|planche|cerceau|émail|email|"
    r"samare|bassine|résine|resine|écorce|ecorce|pin|entrée|entree)\b",
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
    "mission accomplie",
    "on dirait que notre mission",
    "l'histoire est finie",
    "bon travail",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "il ne faut pas rire",
    "on ne rit pas",
    "on ne va pas rire",
    "rire de l'apparence",
    "tu as des lunettes",
    "lunettes aident",
    "les cheveux sont",
    "l'habit tient",
    "pas rire",
    "apparence",
    "l'amitié ne dépend",
    "l'amitie ne depend",
    "vous jouez",
    "on joue",
    "pas une blague",
    "n'est pas une blague",
    "le corps n'est pas",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "trois notes",
    "lumière couleur de miel",
    "lumiere couleur de miel",
    "éclat de caisse",
    "éclat de botte",
    "éclat de limace",
    "éclat de perron",
    "éclat de chaise",
    "éclat de tiroir",
    "éclat de fraisier",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de pin",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de résine",
    "éclat de resine",
    "éclat de papier",
    "éclat de bateau",
    "éclat de farine",
    "éclat de sac",
    "éclat de panier",
    "éclat de pomme",
    "éclat de pain",
    "éclat de filet",
    "éclat de coton",
    "éclat de balance",
    "éclat de banc",
    "éclat de menthe",
    "éclat d'œuf",
    "éclat d'oeuf",
    "éclat de lessive",
    "éclat de miette",
    "éclat de pince",
    "éclat de marche",
    "éclat de corde",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de horloge",
    "éclat de tasse",
    "éclat d'orange",
    "éclat de orange",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat de laine",
    "éclat de lampe",
    "éclat de citron",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de crayon",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de cartable",
    "éclat de pinceau",
    "éclat de zeste",
    "éclat de parapluie",
    "éclat de pavé",
    "éclat de pave",
    "éclat de bâche",
    "éclat de bache",
    "éclat de poire",
    "éclat de volet",
    "éclat de croissant",
    "éclat de réverbère",
    "éclat de reverbere",
    "éclat de cloche",
    "éclat de corbeille",
    "éclat de dorure",
    "éclat de carte",
    "éclat de boule",
    "éclat de galet",
    "éclat de cube",
    "éclat de bois",
    "éclat de couloir",
    "éclat de poussière",
    "éclat de poussiere",
    "éclat de cour",
    "éclat de plaque",
    "éclat de pierre",
    "éclat de grille",
    "éclat de couvercle",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de dalle",
    "éclat d'enveloppe",
    "éclat de enveloppe",
    "éclat d'émail",
    "éclat d'email",
    "éclat de samare",
    "éclat de bassine",
    "éclat de cerceau",
    "éclat de robinet",
    "éclat de planche",
    "éclat de figue",
    "éclat de coussin",
    "éclat de tiroir",
    "éclat de chaise",
    "éclat de perron",
    "éclat de limace",
    "éclat de botte",
    "éclat de résine",
    "grain de pin",
    "grain de miette",
    "lune d'étain",
    "lune d'etain",
    "point de gouttière",
    "point de gouttiere",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de cageot",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_prune_violette_maintenant; "
            "tempo=naturel puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="lunettes",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=il_ferme_la_bouche_tend_la_prune; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="filet",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_refuse_de_foncer_ils_posent_la_prune; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="éclat de cageot",
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=élan puis prudence; intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de cageot",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse et fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "pas rire",
    "accepted_examples": "pas rire | jouer | ensemble",
    "retry_prompt": "On ne rit pas de l'apparence. Que fait Nino ?",
    "engine_ok_text": "Oui, pas rire.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "marche,prune",
        [
            "narrateur|Une toile claque au-dessus des prunes.",
            "enfant-m|J'entends la toile, maman !",
            "maman|Tu l'entends, au-dessus ?",
            "enfant-m|Oui, elle claque.",
            "narrateur|Ça sent le sucré, un peu chaud.",
            "papa|Tu le sens, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Un cageot de bois est ouvert.",
            "narrateur|Des prunes violettes y brillent.",
            "narrateur|Sur la caisse, un éclat de cageot brille.",
            "enfant-m|Il brille, papa !",
            "papa|Tu le vois, sur le bois ?",
            "enfant-m|Oui, un petit point.",
            "maman|Le filet de coton est prêt.",
            "enfant-m|Il gratte un peu.",
            "maman|On le remplit, Nino ?",
            "enfant-m|Oui, avec une prune.",
            "narrateur|Le pain chaud tape le bras de Nino.",
            "enfant-m|Il est tiède.",
            "papa|Le papier croustille ?",
            "enfant-m|Oui, papa.",
            "narrateur|À côté, des pommes rouges attendent.",
            "enfant-m|Elles sont lisses, maman.",
            "maman|On verra les pommes après ?",
            "enfant-m|Après la prune.",
            "narrateur|Une balance fait tic, tout près.",
            "enfant-m|J'entends le tic.",
            "papa|C'est la balance ?",
            "enfant-m|Oui.",
            "narrateur|En ce moment, Nino veut une prune.",
            "enfant-m|Je veux une prune, maintenant !",
            "enfant-m|Une prune violette, maman.",
            "maman|Avec Mila, Nino ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nino saisit trop vite une prune.",
            "narrateur|La prune glisse entre ses doigts.",
            "narrateur|Elle tombe dans le cageot.",
            "enfant-m|Elle est tombée !",
            "narrateur|Nino tire le filet trop vite.",
            "narrateur|Le filet se coince au bord.",
            "enfant-m|Il est coincé !",
            "papa|Le coton, Nino ?",
            "enfant-m|Il tient au bois.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu, lourdes.",
            "narrateur|Maman s'accroupit à la même hauteur.",
            "maman|Tu veux la prune avec Mila ?",
            "enfant-m|Oui, maman.",
            "papa|Tes mains sont collantes, Nino ?",
            "enfant-m|Un peu, papa.",
            "narrateur|Mila arrive près du cageot.",
            "enfant-m|Mila !",
            "narrateur|Ses chaussures collent un peu au sol.",
            "narrateur|Mila a des lunettes neuves.",
            "papa|Tu vois Mila, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Elles brillent un peu.",
            "narrateur|Elle porte un gilet vert.",
            "enfant-m|Tu viens, Mila ?",
            "copine|Oui.",
            "narrateur|Nino ouvre la bouche.",
            "narrateur|Un petit rire commence.",
            "enfant-m|Oh.",
            "narrateur|Nino ferme la bouche.",
            "narrateur|Il regarde la caisse.",
            "narrateur|Il tend une prune.",
            "enfant-m|Pour toi.",
            "narrateur|Mila ne dit rien, d'abord.",
            "narrateur|Elle compte les prunes des yeux.",
            "copine|Celle-là.",
            "narrateur|L'éclat de cageot tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Mila a des lunettes.",
            "narrateur|Que fait Nino ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "filet,prune",
        [
            "narrateur|Nino veut une prune plus brillante.",
            "enfant-m|Celle-là brille plus !",
            "narrateur|Il avance trop vite vers la caisse.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copine|Non.",
            "narrateur|Mila recule d'un pas.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Nino refuse de foncer.",
            "narrateur|Il referme la main.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le cageot, un instant.",
            "narrateur|Nino regarde l'éclat de cageot.",
            "papa|Tu veux la prune avec Mila ?",
            "enfant-m|Tu prends celle du fond ?",
            "narrateur|Mila ne dit rien, d'abord.",
            "narrateur|Elle pose le doigt sur une prune.",
            "copine|Elle est ferme.",
            "enfant-m|D'accord.",
            "narrateur|Nino la pose dans le filet.",
            "narrateur|Le coton se tend un peu.",
            "maman|Merci, Nino.",
            "narrateur|Maman a vu la prune tendue.",
            "papa|Mila, tu as vu le filet ?",
            "copine|Oui.",
            "enfant-m|On prend une pomme aussi ?",
            "maman|Une pomme rouge, Nino ?",
            "enfant-m|Oui, maman.",
            "narrateur|Mila montre une pomme brillante.",
            "narrateur|Nino la pose dans le filet.",
            "enfant-m|Elle est lisse.",
            "papa|Le filet s'alourdit ?",
            "enfant-m|Un peu, papa.",
            "maman|Tes mains sont propres, Nino ?",
            "enfant-m|Un peu collantes.",
            "narrateur|Le ventre de Nino se desserre.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "obstacle",
        "marche,filet",
        [
            "narrateur|Nino veut montrer la prune brillante.",
            "enfant-m|Je la porte, maintenant !",
            "narrateur|Il lève le filet trop haut.",
            "copine|Attends.",
            "narrateur|Trop vite, d'un coup.",
            "narrateur|Une prune presse contre le coton.",
            "enfant-m|Ça tache !",
            "narrateur|Un peu de jus glisse sur le gilet.",
            "papa|Le gilet, Nino ?",
            "enfant-m|Il est taché.",
            "narrateur|Les lunettes de Mila bougent.",
            "narrateur|Nino ouvre la bouche.",
            "narrateur|Un petit rire revient, presque.",
            "enfant-m|Oh.",
            "narrateur|Nino refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite à voix haute.",
            "narrateur|Il observe le filet, un instant.",
            "narrateur|Il écoute le tic de la balance.",
            "narrateur|Sur la caisse, un éclat de cageot luit.",
            "enfant-m|L'éclat, papa ?",
            "papa|Tu le vois, toi ?",
            "enfant-m|Oui, sur le bois.",
            "maman|Le filet, Nino ?",
            "enfant-m|On le porte à deux.",
            "narrateur|Nino tient une anse.",
            "narrateur|Mila tient l'autre.",
            "copine|Je le tiens.",
            "narrateur|Ils marchent, sans se presser.",
            "enfant-m|C'est passé.",
            "copine|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "prune,menthe",
        [
            "narrateur|Un stand de menthe sent fort.",
            "enfant-m|Ça pique le nez, maman.",
            "maman|C'est la menthe ?",
            "enfant-m|Oui, vert et frais.",
            "papa|Tu la sens, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Ils passent près des œufs.",
            "narrateur|Les boîtes sont beiges.",
            "papa|Tu vois les boîtes, Nino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Ils s'assoient sur le banc.",
            "maman|On est bien, ici.",
            "enfant-m|On a la prune, papa.",
            "papa|Tu la vois, dans le filet ?",
            "enfant-m|Oui, avec Mila.",
            "copine|Et la pomme.",
            "narrateur|Nino pose la prune entre eux.",
            "narrateur|Mila pose la main près.",
            "enfant-m|Elle est à nous.",
            "maman|Elle est là, Nino.",
            "enfant-m|Oui, maman.",
            "narrateur|Le pain chaud reste contre le bras.",
            "enfant-m|L'éclat est là, papa.",
            "papa|Tu le vois sur le bois ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les toiles claquent un peu.",
            "narrateur|Un éclat de cageot tient sur le bois.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-m", "copine"):
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
    if n_clue != 5:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 5)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Nino = enfant-m, Mila = copine)")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Mila absente (copine)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m", "copine") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "copine" for r in roles):
        raise SystemExit(f"{SID}: copine absente")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on joue",
        "vous jouez",
        "il ne faut pas rire",
        "on ne rit pas",
        "on ne va pas rire",
        "lunettes aident",
        "tu as des lunettes",
        "apparence",
        "pas rire",
        "pas une blague",
        "le corps n'est pas",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Mila a des lunettes. Que fait Nino ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "pas rire":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != "pas rire | jouer | ensemble":
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "On ne rit pas de l'apparence. Que fait Nino ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    copine_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    ).lower()
    if "non" not in copine_txt:
        raise SystemExit(f"{SID}: Mila sans non")
    if "attends" not in copine_txt:
        raise SystemExit(f"{SID}: Mila sans attends")
    for need in ("toiles", "prune", "filet", "pain", "balance", "banc", "pomme", "menthe"):
        if need not in blob:
            raise SystemExit(f"{SID}: manque {need}")
    if "œuf" not in blob and "oeuf" not in blob and "œufs" not in blob:
        raise SystemExit(f"{SID}: manque œufs")
    for ban in (
        "éclat de caisse",
        "éclat de botte",
        "éclat de pin",
        "éclat d'écorce",
        "éclat d'ecorce",
        "grain de pin",
        "éclat de résine",
        "maya",
        "inès",
        "ines",
        "tout doux",
        "tout calme",
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
        "- **Public :** N2 (≤15 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.COR.003 — lunettes / apparence (vécue : Nino "
        "ouvre la bouche, un rire commence, il ferme, tend la prune, "
        "marche avec Mila). JAMAIS dite dans le récit.\n"
        "- **Personnages :** Nino, Mila, papa, maman. Troupe D16. "
        "Nino = enfant-m (veut maintenant, trop vite). Mila = copine "
        "(lunettes, silence, non, attends). Papa et maman parlent. "
        "Maya / Inès absents.\n"
        "- **Lieu :** marché (toiles, caisse de prunes, filet de coton, "
        "pain, balance, banc, pommes, menthe, œufs). ≠ 003-01 bateau / "
        "éclat de botte. ≠ 003-02 pin / éclat de résine.\n"
        "- **Indice unique :** éclat de cageot (brille sur la caisse → "
        "tremble → Nino le regarde → luit au refus → tient sur le bois). "
        "Pas éclat de caisse (BAN).\n"
        "- **Question moteur :** « Mila a des lunettes. Que fait Nino ? » "
        "expected **pas rire**. Retry : On ne rit pas de l'apparence. "
        "Que fait Nino ? Non récité dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une toile claque au-dessus des prunes. Sucré chaud, cageot "
        "ouvert, pain tiède, tic de balance. Sur la caisse, un éclat de "
        "cageot brille. Nino veut une prune violette **maintenant**, "
        "avec Mila. Première idée : saisir trop vite. La prune tombe. "
        "Il tire le filet : coincé. Sourire parti, poitrine, épaules. "
        "Maman s'accroupit. Mila arrive, lunettes neuves qui brillent. "
        "Un rire commence. Il ferme la bouche, regarde la caisse, tend "
        "une prune. Silence de Mila qui compte. Question. Il veut une "
        "plus brillante : Non. Il refuse de foncer. Merci vécu. Deuxième "
        "ruse : filet trop haut, jus sur le gilet, lunettes qui bougent, "
        "rire presque. Attends. Il refuse, retrouve l'éclat. Ils portent "
        "le filet à deux. Menthe, œufs, banc. Prune partagée. Un éclat "
        "de cageot tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : marché, toiles, cageot, prunes violettes, filet, "
        "pain, balance, pommes.\n"
        "- Désir : une prune violette, maintenant, avec Mila.\n"
        "- Objet : prune, filet de coton, cageot, pain.\n"
        "- Indice unique : éclat de cageot, vu dès l'ouverture, payé "
        "sur le bois. Pas éclat de caisse.\n"
        "- Urgence douce : la prune, maintenant ; Mila arrive.\n"
        "- Imprévu 1 : il saisit trop vite ; prune tombée ; filet coincé.\n"
        "- Cue : maman à la même hauteur ; un merci vécu après le geste.\n"
        "- Imprévu 2 (plus rusé) : filet trop haut ; jus ; lunettes qui "
        "bougent ; rire presque ; Attends.\n"
        "- Résolution : il ferme la bouche, refuse de foncer, tend la "
        "prune, portent le filet à deux.\n"
        "- Retour : menthe, œufs, banc, prune entre eux, éclat sur le "
        "bois.\n\n"
        "## Vécu\n\n"
        "Nino propose, veut **maintenant**. Mila prend son temps, pose "
        "une limite, se tait. Le silence compte. Maman s'accroupit, ne "
        "récite pas « on ne rit pas de l'apparence ». La leçon se voit : "
        "la bouche qui s'ouvre, qui se ferme, la prune tendue, le filet "
        "à deux, le rire qui n'arrive pas. Merci vécu après la prune "
        "dans le filet. Fin : l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé : La prune violette du marché. Lieu du "
        "dump : marché, toiles, caisse, filet, pain, balance, banc, "
        "pommes, menthe, œufs. Pas boulangerie comme autre lieu. Pas "
        "éclat de caisse / botte / pin / écorce / résine.\n"
        "- Ouverture inventée (toile qui claque, sucré chaud, cageot), "
        "pas un gabarit v2. example4 010 / 042 / 074 : corps (sourire "
        "parti, poitrine, accroupi), 2e ruse, refuse de foncer.\n"
        "- Indice unique : éclat de cageot. Pas merle-trois-notes, "
        "miel, tache / flèche / marque / symbole.\n"
        "- Tics encore / déjà / tout doux / tout calme et `aujourd'hui` "
        "retirés. Morale apparence / pas rire hors question. Maya / "
        "Inès → Nino / Mila.\n"
        "- Question moteur inchangée. expected **pas rire**. 5 chunks, "
        "kinds inchangés.\n"
        f"- {nwords} mots. N2 ≤ 15. TTS : notes, ssml, xai, piper par chunk.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n"
        "- 1 × `en ce moment`, 1 × merci adulte, 5 × éclat de cageot\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {nwords} mots")


if __name__ == "__main__":
    main()
