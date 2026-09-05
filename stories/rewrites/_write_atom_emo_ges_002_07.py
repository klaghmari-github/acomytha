#!/usr/bin/env python3
"""ATOM-EMO.GES.002-07 — Le cube rouge d'Amir (F-NAR-019, N1, EMO.GES.002)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.GES.002-07"
TITLE = "Le cube rouge d'Amir"
N1 = LIMITS["N1"]
CHARS = "Amir, papa, maman"
SETTING = (
    "chambre, plancher, torchon, boîte, cubes, bois, "
    "rayon, pli, porte"
)
INDICE = "éclat de torchon"
FIL = (
    "Une bande rouge barre le torchon plié. Sur le pli, "
    "un éclat de torchon luit. Amir veut la tour, maintenant. "
    "Les cubes tombent. Poitrine trop vite. Sourire parti. "
    "Papa s'accroupit. Il souffle, pause. Merci vécu. "
    "Deuxième ruse : la tour semble tenir, un pied accroche, "
    "un cube glisse. Il refuse de foncer. Un éclat de torchon "
    "tient sur le pli."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(tapis|rideau|plaid|balançoire|balancoire|plinthe|marelle|"
    r"banc|cour|grille|bac|flaque|botte|bottes|limace|perron|"
    r"tiroir|fraisier|cuivre|buis|coussin|figue|robinet|planche|"
    r"émail|email|samare|bassine|entrée|entree|merle|miel|"
    r"piquet|cerceau|drap|savon|bol|feuille|pierre|commode|"
    r"lacet|sauge|chiffon|parquet|gond|portail|canapé|"
    r"canape|oiseau|toboggan|comptoir|farine|nappe|casserole|"
    r"citron|wagon|bec|fraise|quille|gouttière|gouttiere|"
    r"crayon|buée|buee|croûte|croute|tableau|casier|moufle|"
    r"craie|cartable|pinceau|zeste|parapluie|pavé|pave|"
    r"bâche|bache|poire|volet|croissant|réverbère|reverbere|"
    r"cloche|corbeille|sac|panier|dorure|carte|boule|galet|"
    r"couloir|poussière|poussiere|plaque|cheminée|cheminee|"
    r"dalle|couvercle|laine|lampe|lessive|vitre|carreau|"
    r"horloge|tasse|orange|écorce|ecorce|étagère|etagere|"
    r"cire|coton|rouleau|pot|pupitre|plateau|étal|etal|"
    r"assiette|coquillage|cadre|livre|plaid|rambarde|"
    r"carotte|zinc|romarin|table|rond|sauge)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
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
    "les trois mots",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "il ne faut pas rire",
    "on ne rit pas",
    "on peut souffler",
    "tu peux souffler",
    "il faut souffler",
    "c'est bien de faire une pause",
    "souffle comme le vent",
    "souffle comme",
    "tu as soufflé",
    "tu as souffle",
    "tu as fait une pause",
    "fais une pause",
    "souffler, puis une pause",
    "souffler puis une pause",
    "on peut reprendre",
    "on reprend",
    "tu as pris ton temps",
    "tu as repris",
    "c'est le bon geste",
    "c est le bon geste",
    "tu te souviens",
    "on souffle",
    "on fait une pause",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de cube",
    "éclat de cubes",
    "éclat de tapis",
    "éclat de rideau",
    "éclat de plaid",
    "éclat de balançoire",
    "éclat de balancoire",
    "éclat de plinthe",
    "éclat de marelle",
    "éclat de toboggan",
    "éclat de comptoir",
    "éclat de pierre",
    "éclat de cerceau",
    "éclat de flaque",
    "éclat de grille",
    "éclat de cour",
    "éclat de botte",
    "éclat de portail",
    "éclat de feuille",
    "éclat de piquet",
    "éclat de commode",
    "éclat de lacet",
    "éclat de sauge",
    "éclat de chiffon",
    "éclat de parquet",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de pin",
    "éclat de pomme",
    "éclat de sève",
    "éclat de seve",
    "éclat de limace",
    "éclat de perron",
    "éclat de chaise",
    "éclat de tiroir",
    "éclat de fraisier",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de casserole",
    "éclat de citron",
    "éclat de coquille",
    "éclat de zeste",
    "éclat de coussin",
    "éclat de figue",
    "éclat de robinet",
    "éclat de planche",
    "éclat d'émail",
    "éclat d'email",
    "éclat de samare",
    "éclat de bassine",
    "éclat de nappe",
    "éclat de farine",
    "éclat de bol",
    "éclat de tablier",
    "éclat de biscuit",
    "éclat de toit",
    "éclat de volet",
    "éclat de pavé",
    "éclat de pave",
    "éclat de parapluie",
    "éclat de bâche",
    "éclat de bache",
    "éclat de poire",
    "éclat de seau",
    "éclat de pompon",
    "éclat de carotte",
    "éclat de carton",
    "éclat de mousse",
    "éclat de laine",
    "éclat de tasse",
    "éclat de crayon",
    "éclat de cartable",
    "éclat de wagon",
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de pinceau",
    "éclat de ballon",
    "éclat de manteau",
    "éclat de marche",
    "éclat de vitre",
    "éclat de grain",
    "éclat de liste",
    "éclat de cheminée",
    "éclat de cheminee",
    "éclat de couloir",
    "éclat de plaque",
    "éclat de dalle",
    "éclat de couvercle",
    "éclat de thermos",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de caillou",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat de lessive",
    "éclat de carreau",
    "éclat de coton",
    "éclat de gravier",
    "éclat de gilet",
    "éclat de lunettes",
    "éclat de résine",
    "éclat de resine",
    "éclat de banc",
    "éclat de bac",
    "éclat de canapé",
    "éclat de canape",
    "éclat de gond",
    "éclat de tour",
    "éclat de lit",
    "éclat de pot",
    "éclat de rouleau",
    "éclat d'étagère",
    "éclat d'etagere",
    "éclat de bois",
    "éclat de barre",
    "éclat de livre",
    "éclat de cadre",
    "éclat de sac",
    "éclat de panier",
    "éclat de farine",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
    "géraldine",
    "geraldine",
)

# N1 : mêmes champs que GES.002-01 (voix N1, tempos plus lents).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat de torchon",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_tour_maintenant; "
            "tempo=posé puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=104, speed=0.80, piper=1.36, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=780,
        sentence=360, energy="focused", contour="rising", noise=0.30,
        emphasis="Amir",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=la_tour_tombe_que_fait_amir; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=122, speed=0.88, piper=1.24, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=620,
        sentence=310, energy="bright", contour="falling", noise=0.33,
        emphasis="souffle",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_souffle_il_fait_une_pause; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de torchon",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=la_tour_semble_tenir_un_cube_glisse; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de torchon",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_pli; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "souffler",
    "accepted_examples": "souffler | il souffle | pause | une pause | s'asseoir",
    "retry_prompt": "Il souffle. Il s'assoit. Que fait-il ?",
    "engine_ok_text": "Oui, souffler.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "pas_escalier,cubes",
        [
            "narrateur|Une bande rouge barre le torchon plié.",
            "enfant-m|C'est de la peinture, papa ?",
            "papa|Tu vois la bande, Amir ?",
            "enfant-m|Oui, elle est rouge.",
            "maman|C'est le cube, sous le torchon.",
            "enfant-m|Le cube rouge !",
            "narrateur|Maman soulève le torchon d'un geste.",
            "narrateur|Le cube roule vers le plancher.",
            "enfant-m|Il roule !",
            "papa|Tu le rattrapes ?",
            "enfant-m|Oui, papa.",
            "narrateur|Amir attrape le cube à deux mains.",
            "enfant-m|Il est lisse.",
            "maman|Il chauffe un peu, Amir ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Le torchon est rêche, sous les doigts.",
            "enfant-m|Il gratte.",
            "maman|Tu le sens, le torchon ?",
            "enfant-m|Oui, maman.",
            "narrateur|Sur le pli, un éclat de torchon luit.",
            "enfant-m|Il brille, papa.",
            "papa|Tu le vois, le petit point ?",
            "enfant-m|Oui, un point.",
            "narrateur|Des pas s'arrêtent près de la porte.",
            "papa|Me voilà.",
            "enfant-m|La chambre est claire.",
            "narrateur|Papa pose le torchon contre le bois.",
            "enfant-m|Il sent le bois.",
            "papa|Tu le sens, le bois chaud ?",
            "enfant-m|Oui, papa.",
            "narrateur|La boîte claque, près des genoux.",
            "enfant-m|Toc.",
            "maman|Tu entends le toc, Amir ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le plancher est tiède, sous les pieds.",
            "enfant-m|Il est chaud.",
            "narrateur|Un rayon glisse sur le torchon.",
            "enfant-m|Il allume le pli.",
            "maman|On ouvre la boîte ensemble ?",
            "enfant-m|Oui, tous les rouges.",
            "narrateur|Les cubes tapent le bord de la boîte.",
            "enfant-m|Ils sont rouges.",
            "papa|Tu prends un cube, Amir ?",
            "enfant-m|Oui, celui-là.",
            "narrateur|En ce moment, Amir prend un cube.",
            "enfant-m|Je veux la tour, maintenant !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les mains serrent le bois peint.",
            "maman|Tu mets le cube dessus ?",
            "enfant-m|Oui, maman.",
            "narrateur|Amir pose un cube trop vite.",
            "narrateur|Puis un autre, trop haut.",
            "enfant-m|Plus haut !",
            "narrateur|La tour penche d'un coup.",
            "narrateur|Les cubes tombent sur le plancher.",
            "narrateur|Ça fait un bruit sec.",
            "enfant-m|Oh.",
            "narrateur|Amir reste surpris, les mains ouvertes.",
            "narrateur|Sa poitrine va trop vite.",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois les cubes, Amir ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains sont chaudes, Amir ?",
            "enfant-m|Un peu, maman.",
            "enfant-m|C'est trop.",
            "narrateur|L'éclat de torchon tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|La tour tombe.",
            "narrateur|Que fait Amir ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "cubes",
        [
            "narrateur|Amir veut empiler, tout de suite.",
            "enfant-m|Je mets tout, maintenant !",
            "narrateur|Les cubes restent par terre.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-m|Trop vite.",
            "narrateur|Amir avance les mains, trop vite.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe les cubes, un instant.",
            "narrateur|Il écoute la chambre.",
            "enfant-m|Fff.",
            "narrateur|Amir souffle une fois.",
            "narrateur|Il souffle une deuxième fois.",
            "narrateur|Il s'assoit près de la boîte.",
            "narrateur|Ses mains se posent sur ses genoux.",
            "narrateur|Il fait une pause.",
            "narrateur|La poitrine ralentit un peu.",
            "papa|Tu restes un peu, Amir ?",
            "enfant-m|Oui, papa.",
            "papa|Merci, Amir.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le bois colle un peu, sous les doigts.",
            "enfant-m|Il est tiède.",
            "narrateur|Amir reprend un cube, sans se presser.",
            "narrateur|Il le pose sur un autre.",
            "papa|Tu le vois, le cube ?",
            "enfant-m|Oui, papa.",
            "narrateur|La tour a deux cubes.",
            "enfant-m|Elle tient !",
            "papa|La tour est petite, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le ventre d'Amir se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près des cubes ?",
            "enfant-m|Oui.",
            "maman|Le rayon touche le pli ?",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "cubes",
        [
            "narrateur|Maman pousse la boîte près du plancher.",
            "narrateur|Elle est un peu sèche.",
            "enfant-m|La tour, maintenant !",
            "narrateur|La petite tour semble tenir.",
            "enfant-m|Elle tient !",
            "narrateur|Amir prend trop de cubes, tout de suite.",
            "enfant-m|Plus haut, maintenant !",
            "narrateur|Un pied accroche le torchon.",
            "narrateur|Un cube glisse au bas.",
            "enfant-m|Il glisse !",
            "narrateur|La tour penche, puis semble tenir.",
            "narrateur|Amir avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Amir refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe la tour, un instant.",
            "narrateur|Il écoute la chambre, près des cubes.",
            "narrateur|Sur le pli, un éclat de torchon luit.",
            "enfant-m|Là, sur le pli.",
            "narrateur|Amir souffle une fois.",
            "narrateur|Il fait une pause, assis un moment.",
            "enfant-m|Fff.",
            "papa|On tient le cube ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le cube sent le bois chaud.",
            "narrateur|Amir pose le cube, sans se presser.",
            "narrateur|La tour se redresse.",
            "enfant-m|Poumf.",
            "maman|Le bois est tiède, Amir ?",
            "enfant-m|Un peu.",
            "narrateur|Il pose un autre cube, au milieu.",
            "maman|Un rayon passe sur le pli.",
            "enfant-m|Il allume le point.",
            "papa|Tu vois le point, Amir ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les cubes tiennent, l'un sur l'autre.",
            "enfant-m|C'est plus facile.",
            "papa|On reste ici, Amir ?",
            "enfant-m|Oui.",
            "narrateur|La boîte reste ouverte, près de lui.",
            "enfant-m|Elle sent le bois.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la boîte.",
            "narrateur|Maman lisse un coin du torchon.",
            "enfant-m|Les cubes sont tombés, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, près du torchon.",
            "maman|On est bien, ici.",
            "narrateur|Amir tapote le pli du doigt.",
            "enfant-m|Il a une trace de doigt.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|La tour est restée, Amir.",
            "enfant-m|Oui, avec les cubes.",
            "narrateur|Ça sent le bois, un peu tiède.",
            "enfant-m|Et le torchon, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|La tour reste près de la boîte.",
            "narrateur|Un éclat de torchon tient sur le pli.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-m"):
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
    if "c'est trop" in adults or "c est trop" in adults:
        raise SystemExit(f"{SID}: refrain adulte c'est trop")
    if INDICE not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit(f"{SID}: indice absent à l'ouverture")
    if INDICE not in by["CHK_T0000_P0000_END_F0001"]["text"].lower():
        raise SystemExit(f"{SID}: indice non payé à la fin")
    n_clue = blob.count(INDICE)
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Amir = enfant-m)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé (dump sans camarade)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    if "géraldine" in blob or "geraldine" in blob:
        raise SystemExit(f"{SID}: Géraldine hors D16")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "enfant-m" for r in roles):
        raise SystemExit(f"{SID}: enfant-m absent")
    body = "\n".join(
        c["script"] for c in chunks if c["chunk_id"] != "CHK_T0000_P0000_Q0001"
    ).lower()
    for lesson in (
        "on peut souffler",
        "tu peux souffler",
        "il faut souffler",
        "souffle comme le vent",
        "tu as soufflé",
        "tu as fait une pause",
        "c'est bien de faire une pause",
        "souffler, puis une pause",
        "on peut reprendre",
        "tu as pris ton temps",
        "on souffle",
        "on fait une pause",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "La tour tombe. Que fait Amir ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "souffler":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "souffler | il souffle | pause | une pause | s'asseoir"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Il souffle. Il s'assoit. Que fait-il ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "souffle" in opening or "pause" in opening:
        raise SystemExit(f"{SID}: souffle/pause trop tôt (avant la question)")
    if "chambre" not in blob:
        raise SystemExit(f"{SID}: manque chambre")
    if "cube" not in blob:
        raise SystemExit(f"{SID}: manque cube")
    if "torchon" not in blob:
        raise SystemExit(f"{SID}: manque torchon")
    if "boîte" not in blob and "boite" not in blob:
        raise SystemExit(f"{SID}: manque boîte")
    if "s'accroupit" not in blob and "s accroupit" not in blob:
        raise SystemExit(f"{SID}: manque s'accroupit")
    if "sourire" not in blob:
        raise SystemExit(f"{SID}: manque sourire parti")
    if "glisse" not in blob:
        raise SystemExit(f"{SID}: manque cube qui glisse")
    if "accroche" not in blob:
        raise SystemExit(f"{SID}: manque pied qui accroche")
    for ban in (
        "éclat de cube",
        "éclat de tapis",
        "éclat de rideau",
        "éclat de balançoire",
        "éclat de plinthe",
        "éclat de marelle",
        "éclat de plaid",
        "éclat de tour",
        "éclat de lit",
        "éclat de comptoir",
        "éclat de pot",
        "éclat de rouleau",
        "éclat d'étagère",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        " tapis",
        "rideau",
        "balançoire",
        "plinthe",
        "marelle",
        "géraldine",
        "geraldine",
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
    if nwords < 700 or nwords > 850:
        raise SystemExit(f"{SID}: hors cible 700-850 ({nwords} mots)")

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans\n"
        "- **Leçon :** EMO.GES.002 — souffler, faire une pause "
        "(vécue : cubes tombent, poitrine trop vite, sourire parti, "
        "papa accroupi, Amir souffle, s'assoit, pause ; 2e ruse : la "
        "tour semble tenir, un pied accroche le torchon, un cube "
        "glisse, il refuse de foncer). JAMAIS dite dans le récit. "
        "Pas « on peut souffler ». Pas « tu peux souffler ». Pas "
        "« il faut souffler ». Pas « c'est bien de faire une pause ».\n"
        "- **Personnages :** Amir, papa, maman. Dump Amir/papa/maman. "
        "Amir = enfant-m (veut la tour maintenant). Pas de copain "
        "(dump sans camarade). Troupe D16. Pas de Géraldine. "
        "Pas de maîtresse.\n"
        "- **Lieu :** chambre, plancher, torchon, boîte, cubes, bois, "
        "rayon, pli, porte. BAN tapis / rideau / coussin / canapé / "
        "farine. ≠ 002-01 salon / carton. ≠ 002-05 lit / coton. "
        "≠ 002-06 étagère / cire.\n"
        "- **Indice unique :** éclat de torchon (luit à l'ouverture → "
        "tremble à la chute → luit quand la tour semble tenir → "
        "tient sur le pli). BAN éclat de cube / tapis / tour / lit / "
        "comptoir / étagère.\n"
        "- **Question moteur :** « La tour tombe. Que fait Amir ? » "
        "expected dump **souffler**. accepted dump `souffler | elle "
        "souffle | pause | une pause | s'asseoir` → `il souffle` "
        "(Amir). retry dump « Elle souffle. Elle s'assoit. Que "
        "fait-elle ? » → « Il souffle. Il s'assoit. Que fait-il ? ». "
        "Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une bande rouge barre le torchon plié. Cube rouge. Sur le "
        "pli, un éclat de torchon luit. Boîte, plancher tiède, "
        "chambre claire. Amir veut la tour **maintenant**. Les cubes "
        "tombent. Poitrine trop vite. Sourire parti. Papa "
        "s'accroupit. Il souffle, pause. Merci vécu. Deuxième ruse : "
        "la tour semble tenir, un pied accroche, un cube glisse. Il "
        "s'arrête, lit l'éclat. Un éclat de torchon tient sur le pli.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : chambre, torchon, plancher, boîte, cubes, bois.\n"
        "- Désir : empiler la tour, maintenant.\n"
        "- Objet : cubes rouges, puis tour qui tombe.\n"
        "- Indice unique : éclat de torchon, vu dès l'ouverture, payé "
        "sur le pli. Pas éclat de cube / tapis / tour.\n"
        "- Urgence douce : il pose trop vite, trop haut.\n"
        "- Imprévu 1 : cubes tombent, poitrine trop vite, sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "la pause.\n"
        "- Imprévu 2 (plus rusé) : la tour semble tenir, un pied "
        "accroche le torchon, un cube glisse au bas.\n"
        "- Résolution : il refuse de foncer, observe, écoute la "
        "chambre, retrouve l'éclat, souffle, attend.\n"
        "- Retour : poumf, tour près de la boîte, éclat sur le pli.\n\n"
        "## Vécu\n\n"
        "Amir veut la tour **maintenant**. Impatience, puis cubes par "
        "terre, sourire parti. Il souffle, s'assoit, les mains sur "
        "les genoux. Papa se baisse, pose une question, ne récite pas "
        "la règle. Ils agissent : un cube sans se presser, tour de "
        "deux. Merci vécu. Fin : l'éclat du début tient sur le pli.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le cube rouge d'Amir (noyau dump). Relance : "
        "Que fait Amir ? expected souffler.\n"
        "- Lieu du dump-meta (chambre). Maman et papa. "
        "Amir = héros enfant-m. BAN tapis / coussin dans le récit.\n"
        "- Ouverture inventée (bande rouge sur le torchon), pas un "
        "gabarit v2, pas « Le soleil chauffe le plancher » du "
        "source, pas « Amir joue dans la chambre ».\n"
        "- Indice unique : éclat de torchon. BAN éclat de cube / "
        "tapis / tour / lit / comptoir. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » du dump.\n"
        "- Leçon non dite : on la voit quand les cubes tombent, "
        "quand la poitrine va trop vite, quand Amir souffle, "
        "quand il s'assoit. Pas « on peut souffler ». Pas "
        "« tu as fait une pause ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « La tour tombe. Que fait Amir ? ». "
        "expected souffler. 5 chunks, kinds inchangés. "
        "expected dump conservé. accepted/retry elle → il (Amir).\n"
        "- example4 052 / 084 / 016 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N1.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers la tour qui semble tenir.\n"
        f"- {nwords} mots. N1 ≤ 10. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n"
        "- Q dump : La tour tombe. Que fait Amir ?\n"
        "- Indice ×4 : éclat de torchon (luit / tremble / luit / tient)\n"
        "- TTS 5/5\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")


if __name__ == "__main__":
    main()
