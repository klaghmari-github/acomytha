#!/usr/bin/env python3
"""ATOM-EMO.LEX.001-01 — La fraise de Chouchou (F-NAR-019, N1, EMO.LEX.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.001-01"
TITLE = "La fraise de Chouchou"
N1 = LIMITS["N1"]
CHARS = "Chouchou, papa, maman"
SETTING = (
    "jardin, treille, terre, soleil, fraise, fil de fer, "
    "bois, feuille de vigne, jus, ombre"
)
INDICE = "éclat de treille"
FIL = (
    "La treille du fond fait de l'ombre. Sur le bois, "
    "un éclat de treille luit. Chouchou veut la fraise, maintenant. "
    "Il attrape la feuille. Puis la fraise tiède. Sourire qui arrive. "
    "Poitrine pleine. Papa s'accroupit. Il dit je suis content. "
    "Un bout pour papa. Merci vécu. Deuxième ruse : fraise trop chaude, "
    "elle glisse. Il refuse de foncer. Un bout pour maman. "
    "Un éclat de treille tient sur le bois."
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
    r"piquet|cerceau|drap|savon|bol|pierre|commode|"
    r"lacet|sauge|chiffon|parquet|gond|portail|canapé|"
    r"canape|oiseau|toboggan|comptoir|panier|torchon|cube|"
    r"carton|galet|farine|assiette|coquillage|tabouret|"
    r"étagère|etagere|rouleau|cadre)\b",
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
    "c'est de la joie",
    "c est de la joie",
    "tu as nommé",
    "tu as nomme",
    "j'ai dit : je suis",
    "j'ai dit: je suis",
    "tu as dit",
    "on peut partager",
    "la joie se partage",
    "tu as partagé",
    "tu as partage",
    "tu es content",
    "c'est bien",
    "c est bien",
    "tu as invité",
    "tu as invite",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de tour",
    "éclat de cube",
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
    "éclat de fraise",
    "éclat de panier",
    "éclat de torchon",
    "éclat de moule",
    "éclat de tuteur",
    "éclat de pot",
    "éclat de rouleau",
    "éclat de lit",
    "éclat d'étagère",
    "éclat d'etagere",
    "éclat de tabouret",
    "éclat de cadre",
    "éclat de livre",
    "éclat d'assiette",
    "éclat de coquillage",
    "éclat de galet",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

# N1 : mêmes champs que GES.002-01 (voix N1, tempos plus lents).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=124, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="warm", contour="storytelling", noise=0.34,
        emphasis="éclat de treille",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis joie; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_la_fraise_maintenant; "
            "tempo=posé puis resserré; sourire=aucun puis qui_arrive; "
            "respiration=ample puis pleine"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=104, speed=0.80, piper=1.36, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=780,
        sentence=360, energy="focused", contour="rising", noise=0.30,
        emphasis="Chouchou",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=chouchou_sourit_que_dit_il; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=122, speed=0.88, piper=1.24, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=620,
        sentence=310, energy="bright", contour="falling", noise=0.33,
        emphasis="content",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=joie puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_dit_je_suis_content_il_tend_un_bout; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de treille",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=la_fraise_glisse_trop_chaude_il_s_arrete; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de treille",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_bois; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "content",
    "accepted_examples": "content | je suis content | joie | de la joie | partager",
    "retry_prompt": "Chouchou sent de la joie. Que dit-il ?",
    "engine_ok_text": "Oui, je suis content.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "jardin,fraise",
        [
            "narrateur|La treille du fond fait de l'ombre.",
            "enfant-m|Elle fait de l'ombre, papa.",
            "papa|Tu la vois, la treille ?",
            "enfant-m|Oui, papa.",
            "narrateur|Un fil de fer vibre sous le pouce.",
            "narrateur|Ting, près du bois.",
            "maman|Tu entends le fil, Chouchou ?",
            "enfant-m|Oui, maman.",
            "narrateur|Maman s'assoit près du fil.",
            "narrateur|La terre chauffe les genoux.",
            "enfant-m|Elle est chaude.",
            "maman|Les genoux sont bien ?",
            "enfant-m|Oui, maman.",
            "narrateur|Papa soulève une feuille de vigne.",
            "narrateur|Le bois sent le soleil.",
            "papa|Tu sens le bois chaud ?",
            "enfant-m|Oui, papa.",
            "narrateur|Sur le bois, un éclat de treille luit.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, sur le bois ?",
            "enfant-m|Oui, un petit point.",
            "papa|Le soleil le touche.",
            "narrateur|Un rayon glisse sur le bord.",
            "narrateur|La treille chauffe le jardin.",
            "enfant-m|Elle est chaude.",
            "maman|Tu poses la main, Chouchou ?",
            "enfant-m|Oui.",
            "narrateur|Une fraise rouge attend sous la feuille.",
            "enfant-m|Une fraise !",
            "maman|Elle est rouge, Chouchou ?",
            "enfant-m|Oui, maman.",
            "narrateur|Elle sent un peu le sucre.",
            "enfant-m|Ça sent le sucre, papa.",
            "papa|Tu la veux, la fraise ?",
            "enfant-m|Oui, maintenant !",
            "narrateur|En ce moment, Chouchou tend la main.",
            "enfant-m|Je la prends, tout de suite !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|Chouchou attrape trop vite.",
            "narrateur|Sa main prend la feuille.",
            "enfant-m|Oh.",
            "narrateur|La fraise reste cachée.",
            "narrateur|Les doigts tiennent du vert.",
            "maman|La feuille, pas la fraise ?",
            "enfant-m|Pas la fraise.",
            "narrateur|Chouchou reste surpris, la main ouverte.",
            "narrateur|Puis il penche la tête.",
            "narrateur|Il cherche sous la feuille.",
            "enfant-m|Là.",
            "narrateur|La fraise rouge est là, tiède.",
            "narrateur|Il la cueille, sans se presser.",
            "enfant-m|Elle est à moi.",
            "narrateur|Elle pèse dans sa paume.",
            "narrateur|Elle est tiède, un peu molle.",
            "enfant-m|Elle chauffe ma main.",
            "maman|Elle est tiède, Chouchou ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un sourire arrive sur son visage.",
            "narrateur|Ses joues deviennent chaudes.",
            "narrateur|Sa poitrine se remplit, chaude.",
            "narrateur|Dans sa poitrine, c'est plein.",
            "narrateur|Ses épaules se lèvent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois la fraise, Chouchou ?",
            "enfant-m|Oui, papa.",
            "maman|Tes joues sont chaudes, Chouchou ?",
            "enfant-m|Un peu, maman.",
            "narrateur|L'éclat de treille tremble, sous le fil.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Chouchou sourit.",
            "narrateur|Que dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "jardin",
        [
            "narrateur|Chouchou serre la fraise, trop fort.",
            "enfant-m|Je la mange, maintenant !",
            "narrateur|Le jus glisse entre ses doigts.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-m|Trop vite.",
            "narrateur|Il avance la fraise vers sa bouche.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe la fraise, un instant.",
            "narrateur|Il écoute le jardin.",
            "enfant-m|Je suis content.",
            "narrateur|Sa voix est petite, près de la fraise.",
            "papa|Tu restes un peu, Chouchou ?",
            "enfant-m|Oui, papa.",
            "narrateur|Chouchou tend la fraise vers papa.",
            "enfant-m|Un bout pour toi.",
            "narrateur|Papa prend un petit bout.",
            "papa|Merci, Chouchou.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Le jus est rouge, sous les doigts.",
            "enfant-m|Il est sucré.",
            "narrateur|Chouchou garde un bout, dans la paume.",
            "papa|Tu le vois, le bout ?",
            "enfant-m|Oui, papa.",
            "maman|Il est tiède, Chouchou ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le sourire reste près de la fraise.",
            "enfant-m|Je suis content.",
            "papa|Les joues sont chaudes ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains sont rouges ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Le ventre de Chouchou se desserre.",
            "narrateur|Les épaules restent hautes.",
            "papa|On reste près de la treille ?",
            "enfant-m|Oui.",
            "maman|Le rayon touche le bois ?",
            "enfant-m|Oui, maman.",
            "narrateur|La fraise attend dans sa main.",
            "enfant-m|Je la tiens.",
            "papa|Tu la tiens, Chouchou ?",
            "enfant-m|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "jardin,fraise",
        [
            "narrateur|Maman se baisse près de la treille.",
            "narrateur|La fraise brille, trop chaude.",
            "enfant-m|Un bout pour toi, maman !",
            "narrateur|Chouchou tend la fraise, trop vite.",
            "narrateur|Elle glisse de sa main.",
            "enfant-m|Elle tombe !",
            "narrateur|La fraise penche vers la terre.",
            "narrateur|Chouchou avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Chouchou refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe la fraise, un instant.",
            "narrateur|Il écoute le jardin, près du fil.",
            "narrateur|Sur le bois, un éclat de treille luit.",
            "enfant-m|Là, sur le bois.",
            "narrateur|Il attend, les deux mains ouvertes.",
            "papa|On tient la fraise ?",
            "enfant-m|Oui, papa.",
            "narrateur|La fraise sent le sucre chaud.",
            "narrateur|Elle est là, un peu penchée.",
            "narrateur|Chouchou la reprend, sans se presser.",
            "narrateur|Il la casse en deux.",
            "enfant-m|Pour toi.",
            "maman|Le jus est tiède, Chouchou ?",
            "enfant-m|Un peu.",
            "narrateur|Il tend un bout vers maman.",
            "maman|Pour moi ?",
            "enfant-m|Oui, maman.",
            "papa|Le bout tient, Chouchou ?",
            "enfant-m|Oui, papa.",
            "maman|Un rayon passe sur le bois.",
            "enfant-m|Il allume le fil.",
            "papa|Tu vois le point, Chouchou ?",
            "enfant-m|Oui, papa.",
            "narrateur|Maman prend le bout, près des lèvres.",
            "enfant-m|Il est sucré.",
            "papa|La treille est calme ?",
            "enfant-m|Oui, papa.",
            "maman|Tes genoux sont au chaud ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Le bois reste proche, près d'eux.",
            "enfant-m|Il sent le soleil.",
            "papa|On reste ici, Chouchou ?",
            "enfant-m|Oui.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la treille.",
            "narrateur|Maman essuie un peu de jus.",
            "enfant-m|La fraise a glissé, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-m|Oui, près de la terre.",
            "maman|On est bien, ici.",
            "narrateur|Chouchou tapote le bois du doigt.",
            "enfant-m|Il a une trace de jus.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|La fraise est restée, Chouchou.",
            "enfant-m|Oui, avec un bout.",
            "narrateur|Ça sent le sucre, un peu tiède.",
            "enfant-m|Et le bois, maman.",
            "maman|Oui, dans l'air.",
            "papa|Le jardin est calme, Chouchou ?",
            "enfant-m|Oui, papa.",
            "narrateur|La fraise reste dans la paume.",
            "narrateur|Un éclat de treille tient sur le bois.",
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
    occs = re.findall(r"éclat de treille (\w+)", blob)
    if occs != ["luit", "tremble", "luit", "tient"]:
        raise SystemExit(f"{SID}: verbes indice {occs}")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Chouchou dump = enfant-m)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain inventé (dump sans camarade)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
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
        "c'est de la joie",
        "c est de la joie",
        "tu as nommé",
        "j'ai dit : je suis",
        "on peut partager",
        "la joie se partage",
        "tu as partagé",
        "tu es content",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Chouchou sourit. Que dit-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "content":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "content | je suis content | joie | de la joie | partager"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Chouchou sent de la joie. Que dit-il ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "je suis content" in opening or "content" in opening:
        raise SystemExit(f"{SID}: content trop tôt (avant la question)")
    if "joie" in opening:
        raise SystemExit(f"{SID}: joie trop tôt (avant la question)")
    if "jardin" not in blob:
        raise SystemExit(f"{SID}: manque jardin")
    if "fraise" not in blob:
        raise SystemExit(f"{SID}: manque fraise")
    if "treille" not in blob:
        raise SystemExit(f"{SID}: manque treille")
    for cid, ch in by.items():
        if cid == "CHK_T0000_P0000_Q0001":
            continue
        if ch.get("expected_answer") not in (None, ""):
            raise SystemExit(f"{SID}: {cid} expected hors Q")
        if ch.get("accepted_examples") not in (None, ""):
            raise SystemExit(f"{SID}: {cid} accepted hors Q")
        if ch.get("retry_prompt") not in (None, ""):
            raise SystemExit(f"{SID}: {cid} retry hors Q")
    for ban in (
        "éclat de fraise",
        "éclat de panier",
        "éclat de torchon",
        "éclat de fraisier",
        "éclat de tour",
        "éclat de cube",
        "éclat de tapis",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "c'est de la joie",
        "tu as nommé",
        "l'histoire est finie",
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
    if not (700 <= nwords <= 850):
        raise SystemExit(f"{SID}: mots {nwords} hors 700-850")

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans\n"
        "- **Leçon :** EMO.LEX.001 — nommer la joie et partager "
        "(vécue : sourire qui arrive, poitrine pleine, papa accroupi, "
        "Chouchou dit « je suis content », tend un bout ; 2e ruse : "
        "fraise trop chaude, elle glisse, il refuse de foncer, un bout "
        "pour maman). JAMAIS dite dans le récit. Pas « c'est de la joie ». "
        "Pas « tu as nommé ». Pas « j'ai dit : je suis ». Pas "
        "« on peut partager ».\n"
        "- **Personnages :** Chouchou, papa, maman. Dump Tom → D16 "
        "Chouchou = enfant-m (garçon, veut la fraise maintenant). "
        "Pas de copain (dump sans camarade). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** jardin, treille, terre, soleil, fraise, fil de fer, "
        "bois, feuille de vigne, jus, ombre. BAN panier / torchon / "
        "fraisier (indice dump). ≠ dump « Un petit panier attend près "
        "du gravier ».\n"
        "- **Indice unique :** éclat de treille (luit à l'ouverture → "
        "tremble au sourire → luit quand la fraise glisse → tient sur "
        "le bois). BAN éclat de fraise / panier / torchon / fraisier / "
        "tour / cube.\n"
        "- **Question moteur :** « Chouchou sourit. Que dit-il ? » "
        "expected dump **content**. accepted dump "
        "`content | je suis content | joie | de la joie | partager`. "
        "retry dump Tom → Chouchou. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La treille du fond fait de l'ombre. Ting. Sur le bois, un éclat "
        "de treille luit. Terre chaude, feuille de vigne, fraise rouge. "
        "Chouchou veut la cueillir **maintenant**. Il attrape la feuille. "
        "Puis la fraise tiède. Sourire qui arrive. Poitrine pleine. Papa "
        "s'accroupit. Il dit je suis content. Un bout pour papa. Merci "
        "vécu. Deuxième ruse : trop chaude, la fraise glisse. Il "
        "s'arrête, lit l'éclat. Un bout pour maman. Un éclat de treille "
        "tient sur le bois.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : jardin, treille, terre, soleil, fil, bois, feuille "
        "de vigne. BAN panier / torchon / fraisier.\n"
        "- Désir : cueillir la fraise, maintenant.\n"
        "- Objet : fraise rouge, tiède, trop chaude.\n"
        "- Indice unique : éclat de treille, vu dès l'ouverture, payé "
        "sur le bois. Pas éclat de fraise / panier / torchon.\n"
        "- Urgence douce : il attrape trop vite.\n"
        "- Imprévu 1 : la feuille, pas la fraise ; puis sourire qui "
        "arrive, poitrine pleine.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le bout "
        "tendu.\n"
        "- Imprévu 2 (plus rusé) : fraise trop chaude, elle glisse vers "
        "la terre.\n"
        "- Résolution : il refuse de foncer, observe, écoute le jardin, "
        "retrouve l'éclat, casse un bout.\n"
        "- Retour : trace de jus, fraise dans la paume, éclat sur le bois.\n\n"
        "## Vécu\n\n"
        "Chouchou veut la fraise **maintenant**. Impatience, puis feuille "
        "dans la main, puis fraise tiède, sourire qui arrive. Il dit je "
        "suis content, tend un bout. Papa se baisse, pose une question, "
        "ne récite pas la règle. Ils agissent : un bout sans se presser, "
        "puis un bout pour maman après la glissade. Merci vécu. Fin : "
        "l'éclat du début tient sur le bois.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : La fraise de Chouchou (noyau dump). Relance : "
        "Que dit-il ? expected content.\n"
        "- Lieu du dump-meta (jardin). Maman et papa. Chouchou = héros "
        "enfant-m (dump + mission : garçon). BAN panier / torchon / "
        "fraisier dans le récit.\n"
        "- Ouverture inventée (treille du fond, ombre, ting), pas un "
        "gabarit v2, pas panier/torchon/gravier du source, pas « Tom "
        "marche dans le jardin ».\n"
        "- Indice unique : éclat de treille. BAN éclat de fraise / "
        "panier / torchon / fraisier / tour / cube. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doucement » / « tout doux » du dump.\n"
        "- Leçon non dite : on la voit quand le sourire arrive, quand "
        "il dit je suis content, quand il tend un bout. Strip dump "
        "« c'est de la joie », « tu as nommé », « Chouchou a nommé "
        "sa joie », « tu as dit : je suis content », « L'histoire "
        "est finie ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Chouchou sourit. Que dit-il ? ». "
        "expected content. 5 chunks, kinds inchangés. expected/accepted "
        "dump conservés (labels moteur, même « de la joie »). retry "
        "Tom → Chouchou. Hors Q : expected/accepted/retry null.\n"
        "- example4 054 / 086 / 018 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N1.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers la fraise qui glisse.\n"
        f"- {nwords} mots. N1 ≤ 10. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        "- 5 chunks, graphe inchangé\n"
        f"- {nwords} mots\n"
        "- `text` = `script` collé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {path} mots={nwords} bytes={path.stat().st_size}")


if __name__ == "__main__":
    main()
