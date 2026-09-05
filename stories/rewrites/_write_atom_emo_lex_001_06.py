#!/usr/bin/env python3
"""ATOM-EMO.LEX.001-06 — Victorino et le galet lisse (F-NAR-019, N1, EMO.LEX.001)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-EMO.LEX.001-06"
TITLE = "Victorino et le galet lisse"
N1 = LIMITS["N1"]
CHARS = "Victorino, papa, maman"
SETTING = (
    "bord de rivière, nappe, galet, cailloux, panier, "
    "pain, herbe, eau, soleil"
)
INDICE = "éclat de berge"
FIL = (
    "Le panier craque contre l'herbe. Sur le bord, "
    "un éclat de berge luit. Victorino veut le galet, maintenant. "
    "Trop lisse : il glisse, tombe. Poitrine trop vite. Sourire parti. "
    "Papa s'accroupit. Je suis content. Merci vécu. "
    "Deuxième ruse : le galet glisse vers l'eau. "
    "Il refuse de foncer. Il fait toucher. "
    "Un éclat de berge tient près du bord."
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
    r"canape|oiseau|toboggan|comptoir|treille|moule|tuteur|"
    r"saladier|gomme|torchon|tabouret)\b",
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
    "j'ai dit",
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
    "tu as dit ta joie",
    "tu as partagé",
    "la joie est là",
    "on va apprendre",
    "c'est le bon geste",
    "c est le bon geste",
    "tu te souviens",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
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
    "éclat de treille",
    "éclat de moule",
    "éclat de tuteur",
    "éclat de saladier",
    "éclat de gomme",
    "éclat de galet",
    "éclat de tour",
    "éclat de pot",
    "éclat de rouleau",
    "éclat de lit",
    "éclat d'étagère",
    "éclat de etagere",
    "éclat de torchon",
    "éclat de tabouret",
    "éclat d'eau",
    "éclat de l'eau",
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
        emphasis="éclat de berge",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_galet_maintenant; "
            "tempo=posé puis resserré; sourire=léger puis aucun; "
            "respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=104, speed=0.80, piper=1.36, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=780,
        sentence=360, energy="focused", contour="rising", noise=0.30,
        emphasis="Victorino",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=victorino_sourit_que_dit_il; "
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
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=il_fait_toucher_le_galet; "
            "tempo=posé; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=480,
        sentence=280, energy="lively", contour="dynamic", noise=0.35,
        emphasis="éclat de berge",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=le_galet_glisse_vers_leau_il_s_arrete; "
            "tempo=un peu vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=102, speed=0.80, piper=1.36, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=980,
        sentence=380, energy="calm", contour="falling", noise=0.29,
        emphasis="éclat de berge",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_pres_du_bord; "
            "tempo=très posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "content",
    "accepted_examples": (
        "content | contente | je suis contente | joie | de la joie | partager"
    ),
    "retry_prompt": "Victorino sent de la joie. Que dit-il ?",
    "engine_ok_text": "Oui, content.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "eau",
        [
            "narrateur|Le panier craque contre l'herbe.",
            "papa|Tu poses le pain, maman ?",
            "maman|Oui, sur la nappe.",
            "narrateur|Un coin de nappe se lève.",
            "enfant-m|Il vole, papa !",
            "papa|Le vent le pousse.",
            "narrateur|Le pain sent le soleil.",
            "enfant-m|Ça sent bon.",
            "maman|Tu le sens, Victorino ?",
            "enfant-m|Oui, maman.",
            "narrateur|L'eau de la rivière fait tic.",
            "narrateur|Ça tape les cailloux, au bord.",
            "maman|Tu entends le tic ?",
            "enfant-m|Oui, le tic.",
            "narrateur|Le chemin brûle un peu les pieds.",
            "enfant-m|Il est chaud !",
            "papa|On reste dans l'herbe ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les cigales chantent, très loin.",
            "narrateur|Le soleil pique un peu le nez.",
            "enfant-m|Il pique, maman.",
            "maman|Le nez est tiède ?",
            "enfant-m|Un peu.",
            "narrateur|Maman s'assoit près du panier.",
            "enfant-m|Ça chauffe les genoux.",
            "papa|Les genoux sont bien ?",
            "enfant-m|Oui, papa.",
            "narrateur|Un éclat de berge luit.",
            "enfant-m|Il brille, papa !",
            "papa|Tu le vois, près du bord ?",
            "enfant-m|Oui, un petit point.",
            "maman|Le soleil le touche.",
            "narrateur|Un rayon glisse sur le bord.",
            "enfant-m|Il allume l'herbe.",
            "narrateur|Un galet gris attend dans l'herbe.",
            "enfant-m|Un galet !",
            "maman|Il est lisse, Victorino ?",
            "enfant-m|Je le prends !",
            "narrateur|En ce moment, Victorino veut le galet.",
            "enfant-m|Je le veux, maintenant !",
            "papa|Tout de suite ?",
            "enfant-m|Oui, papa.",
            "narrateur|Les deux mains serrent trop vite.",
            "narrateur|Le galet est trop lisse.",
            "enfant-m|Il glisse !",
            "narrateur|Le galet tombe dans l'herbe sèche.",
            "narrateur|Ça fait un bruit mou.",
            "enfant-m|Oh.",
            "narrateur|Victorino reste les mains ouvertes.",
            "narrateur|Sa poitrine va trop vite.",
            "narrateur|Le sourire de Victorino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|L'envie et la peur se heurtent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois le galet, Victorino ?",
            "enfant-m|Il est là.",
            "maman|Tes mains sont chaudes ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Victorino cherche dans l'herbe.",
            "narrateur|Le galet est tiède, sous les doigts.",
            "enfant-m|Je le tiens.",
            "narrateur|Un sourire revient, tout petit.",
            "enfant-m|Je suis content.",
            "papa|Tu le serres, Victorino ?",
            "enfant-m|Oui.",
            "maman|Il chauffe la paume ?",
            "enfant-m|Oui, maman.",
            "narrateur|L'éclat de berge tremble, puis tient.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorino sourit.",
            "narrateur|Que dit-il ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "",
        [
            "narrateur|Victorino veut montrer le galet.",
            "enfant-m|Vous touchez, maintenant !",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "enfant-m|Trop vite.",
            "narrateur|Victorino avance les mains, trop vite.",
            "narrateur|Le galet penche vers l'herbe.",
            "narrateur|Puis il s'arrête.",
            "narrateur|Il referme les doigts, puis ouvre.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le galet, un instant.",
            "narrateur|Il écoute l'eau, près du bord.",
            "enfant-m|Tu touches, papa ?",
            "papa|Je touche, Victorino ?",
            "enfant-m|Oui.",
            "narrateur|Papa pose un doigt sur le galet.",
            "enfant-m|Toi aussi, maman.",
            "maman|J'approche le doigt ?",
            "enfant-m|Oui, maman.",
            "narrateur|Maman touche le galet, tout près.",
            "papa|Il est lisse, hein ?",
            "enfant-m|Oui.",
            "enfant-m|Lisse.",
            "papa|Merci, Victorino.",
            "narrateur|Papa reste à la même hauteur.",
            "maman|Il chauffe sous le doigt ?",
            "enfant-m|Un peu.",
            "narrateur|Le ventre de Victorino se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près du galet ?",
            "enfant-m|Oui.",
            "enfant-m|Je suis content.",
            "maman|Tes genoux sont au chaud ?",
            "enfant-m|Un peu, maman.",
            "narrateur|Le galet reste dans les deux mains.",
            "enfant-m|Il est tiède.",
            "papa|Tu le vois, le galet ?",
            "enfant-m|Oui, papa.",
            "maman|La nappe attend, Victorino ?",
            "enfant-m|Après.",
            "narrateur|Un rayon passe sur le bord.",
            "enfant-m|Il allume le galet.",
            "papa|On tient ensemble ?",
            "enfant-m|Oui.",
            "narrateur|Les cailloux font tic, au bord.",
            "enfant-m|Je les entends.",
            "maman|Le pain reste dans le panier ?",
            "enfant-m|Oui, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "eau",
        [
            "narrateur|Maman tire un coin de nappe.",
            "narrateur|Le panier est un peu lourd.",
            "enfant-m|Le galet, maintenant !",
            "narrateur|Victorino serre trop fort, tout de suite.",
            "narrateur|Le galet glisse de sa main.",
            "enfant-m|Il glisse !",
            "narrateur|Le galet roule vers l'eau.",
            "narrateur|Victorino avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Victorino refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le galet, un instant.",
            "narrateur|Il écoute l'eau, près des cailloux.",
            "narrateur|Sur le bord, un éclat de berge luit.",
            "enfant-m|Là, sur le bord.",
            "narrateur|Victorino pose deux doigts, sans se presser.",
            "narrateur|Le galet s'arrête, trop lisse.",
            "papa|On tient le galet ?",
            "enfant-m|Oui, papa.",
            "narrateur|Papa pose un doigt, avec lui.",
            "narrateur|Maman pose un doigt, aussi.",
            "enfant-m|Vous touchez.",
            "maman|Il est froid, près de l'eau ?",
            "enfant-m|Un peu.",
            "narrateur|Le galet sent l'herbe tiède.",
            "narrateur|Une petite trace d'eau reste.",
            "enfant-m|Poumf.",
            "papa|Le galet tient, Victorino ?",
            "enfant-m|Oui, papa.",
            "maman|Tes genoux sont au chaud ?",
            "enfant-m|Un peu, maman.",
            "narrateur|La nappe reste ouverte, près d'eux.",
            "enfant-m|Elle sent le pain.",
            "papa|On reste ici, Victorino ?",
            "enfant-m|Oui.",
            "narrateur|Les cailloux font tic, au bord.",
            "enfant-m|Le tic est là.",
            "maman|Tu le serres sans forcer ?",
            "enfant-m|Oui, maman.",
            "papa|On touche ensemble ?",
            "enfant-m|Oui.",
            "narrateur|Trois doigts tiennent le galet.",
            "enfant-m|Il ne part plus.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près de la nappe.",
            "narrateur|Maman essuie un peu d'eau.",
            "enfant-m|Le galet a glissé, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, vers l'eau.",
            "maman|On est bien, ici.",
            "narrateur|Victorino tapote le galet du doigt.",
            "enfant-m|Il a une trace d'eau.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|Le galet est resté, Victorino.",
            "enfant-m|Oui, dans ma main.",
            "narrateur|Ça sent l'herbe, un peu tiède.",
            "enfant-m|Et le pain, maman.",
            "maman|Oui, dans l'air.",
            "papa|On reste au bord, Victorino ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le galet reste près de la nappe.",
            "narrateur|Un éclat de berge tient près du bord.",
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
        raise SystemExit(f"{SID}: enfant-f (Victorino = enfant-m)")
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
        "j'ai dit : je suis",
        "j'ai dit: je suis",
        "tu as nommé",
        "tu as dit ta joie",
        "tu as partagé",
        "la joie est là",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Victorino sourit. Que dit-il ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "content":
        raise SystemExit(f"{SID}: expected_answer altéré")
    if q.get("accepted_examples") != (
        "content | contente | je suis contente | joie | de la joie | partager"
    ):
        raise SystemExit(f"{SID}: accepted_examples altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "Victorino sent de la joie. Que dit-il ?":
        raise SystemExit(f"{SID}: retry altéré: {retry}")
    for cid, ch in by.items():
        if cid == "CHK_T0000_P0000_Q0001":
            continue
        if ch.get("expected_answer") not in (None, ""):
            raise SystemExit(f"{SID}: expected hors Q ({cid})")
        if ch.get("accepted_examples") not in (None, ""):
            raise SystemExit(f"{SID}: accepted hors Q ({cid})")
        if ch.get("retry_prompt") not in (None, ""):
            raise SystemExit(f"{SID}: retry hors Q ({cid})")
    opening = by["CHK_T0000_P0000"]["script"].lower()
    if "je suis content" not in opening:
        raise SystemExit(f"{SID}: naming trop tard (avant la question)")
    if "galet" not in blob:
        raise SystemExit(f"{SID}: manque galet")
    if "nappe" not in blob:
        raise SystemExit(f"{SID}: manque nappe")
    if "caillou" not in blob:
        raise SystemExit(f"{SID}: manque caillou")
    if "s'accroupit" not in blob and "s’accroupit" not in blob:
        raise SystemExit(f"{SID}: manque adulte accroupi")
    if "touche" not in blob:
        raise SystemExit(f"{SID}: manque faire toucher")
    for ban in (
        "éclat de galet",
        "éclat de caillou",
        "éclat de nappe",
        "éclat de pierre",
        "éclat de dalle",
        "éclat d'eau",
        "éclat de l'eau",
        "tout doux",
        "tout calme",
        "merle",
        "miel",
        "c'est de la joie",
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

    nwords = sum(words(c["text"]) for c in chunks)
    if nwords < 700 or nwords > 850:
        raise SystemExit(f"{SID}: mots {nwords} hors 700–850")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. `chunk_id` / `kind` "
        "inchangés. Texte seulement. Pas d'apply. Pas de git. Pas d'audio.\n\n"
        "- **Public :** N1 (≤10 mots/phrase), audio familial, voc 3–4 ans\n"
        "- **Leçon :** EMO.LEX.001 — nommer la joie + partager "
        "(vécue : galet trop lisse, tombe, poitrine trop vite, sourire parti, "
        "papa accroupi, « je suis content », faire toucher ; 2e ruse : le galet "
        "glisse vers l'eau, il refuse de foncer). JAMAIS dite dans le récit. "
        "Pas « c'est de la joie ». Pas « j'ai dit : je suis ». Pas « tu as nommé ».\n"
        "- **Personnages :** Victorino, papa, maman. Dump Eva → D16 Victorino "
        "= enfant-m (veut le galet maintenant). Pas de copain "
        "(dump sans camarade). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** bord de rivière, nappe, galet, cailloux, panier, pain, "
        "herbe, eau, soleil. Objets dump conservés. BAN merle / miel.\n"
        "- **Indice unique :** éclat de berge (luit à l'ouverture → "
        "tremble à la chute → luit quand le galet roule vers l'eau → "
        "tient près du bord). BAN éclat de galet / caillou / nappe / "
        "pierre / dalle / eau.\n"
        "- **Question moteur :** « Victorino sourit. Que dit-il ? » "
        "expected dump **content**. accepted dump "
        "`content | contente | je suis contente | joie | de la joie | partager`. "
        "retry dump Eva → Victorino (dit-il). Non récitée dans les autres chunks. "
        "Hors Q : null.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le panier craque contre l'herbe. Tic. Sur le bord, un éclat "
        "de berge luit. Nappe, pain, galet lisse. Victorino veut le galet "
        "**maintenant**. Trop lisse : il glisse, tombe. Poitrine trop vite. "
        "Sourire parti. Papa s'accroupit. Je suis content. Merci vécu. "
        "Deuxième ruse : le galet glisse vers l'eau. Il s'arrête, lit "
        "l'éclat, fait toucher. Un éclat de berge tient près du bord.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : bord de rivière, nappe, galet, cailloux, panier, pain.\n"
        "- Désir : prendre le galet lisse, maintenant, le faire toucher.\n"
        "- Objet : galet trop lisse, puis galet qui roule vers l'eau.\n"
        "- Indice unique : éclat de berge, vu dès l'ouverture, payé "
        "près du bord. Pas éclat de galet / caillou / nappe / pierre / dalle / eau.\n"
        "- Urgence douce : il serre trop vite, trop fort.\n"
        "- Imprévu 1 : galet trop lisse, tombe dans l'herbe, sourire parti.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après le toucher.\n"
        "- Imprévu 2 (plus rusé) : le galet glisse vers l'eau, trop lisse.\n"
        "- Résolution : il refuse de foncer, observe, écoute l'eau, "
        "retrouve l'éclat, fait toucher.\n"
        "- Retour : trace d'eau sur le galet, éclat près du bord.\n\n"
        "## Vécu\n\n"
        "Victorino veut le galet **maintenant**. Impatience, puis galet "
        "par terre, sourire parti. Il dit je suis content. Il tend le "
        "galet. Papa se baisse, pose une question, ne récite pas la joie. "
        "Ils agissent : un doigt, puis deux, puis trois. Merci vécu. "
        "Fin : l'éclat du début tient près du bord.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Victorino et le galet lisse (noyau dump). Relance : "
        "Que dit-il ? expected content.\n"
        "- Lieu du dump-meta (bord de rivière). Maman et papa. "
        "Victorino = héros enfant-m. Galet / caillou / nappe conservés.\n"
        "- Ouverture inventée (panier, nappe, pain), pas un gabarit "
        "v2, pas « L'eau fait tic, tic, tic » du source, pas Eva.\n"
        "- Indice unique : éclat de berge. BAN éclat de galet / "
        "caillou / nappe / pierre / dalle / eau. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « c'est de la joie » / « j'ai dit : je suis » / "
        "« tu as nommé ».\n"
        "- Leçon non dite : on la voit quand il dit je suis content, "
        "quand il fait toucher le galet. Pas « c'est de la joie ». "
        "Pas « tu as nommé ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur : « Victorino sourit. Que dit-il ? ». "
        "expected content. 5 chunks, kinds inchangés. expected/accepted "
        "dump conservés. retry Eva → Victorino (dit-il). Hors Q : null.\n"
        "- example4 059 / 091 / 023 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_emo_ges_002_01.py`, profiles N1.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action un peu plus vive vers le galet qui glisse.\n"
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
