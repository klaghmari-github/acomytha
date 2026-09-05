#!/usr/bin/env python3
"""ATOM-DIF.COR.003-07 — Le cerceau jusqu'au chat (F-NAR-019, N2, DIF.COR.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.003-07"
TITLE = "Le cerceau jusqu'au chat"
N2 = LIMITS["N2"]
CHARS = "Raphaël, Mila, papa, maman"
SETTING = "square, portail, gravier, cerceau bleu, banc, gourde, fourmi"
INDICE = "éclat de portail"
FIL = (
    "Le portail s'ouvre. Le fer grince. Sur le fer, un "
    "éclat de portail brille. Raphaël veut le cerceau bleu "
    "jusqu'au chat, maintenant. Mila arrive. Un rire commence. "
    "Mila se tait. Le cerceau tape la gourde. Raphaël refuse "
    "de foncer. Merci vécu. La queue du chat tombe. Il refuse, "
    "lit l'éclat. Un éclat de portail tient sur le fer."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(botte|bottes|limace|perron|chaise|tiroir|fraisier|cuivre|"
    r"buis|coussin|figue|robinet|planche|émail|email|samare|"
    r"bassine|entrée|entree|résine|resine|écorce|ecorce|pierre|"
    r"pierres|volet|volet|pin|corde|botte)\b",
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
    "les trois mots",
    "tu as bien fait",
    "on va ranger",
    "tu ranges",
    "il faut attendre",
    "on doit demander",
    "il faut demander",
    "il ne faut pas rire",
    "on ne rit pas",
    "on ne va pas rire",
    "rire de l'apparence",
    "lunettes aident",
    "l'amitié ne dépend pas",
    "l'amitie ne depend pas",
    "vous jouez",
    "on joue",
    "pas rire",
    "apparence",
    "pas une blague",
    "n'est pas une blague",
    "n est pas une blague",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat d'écorce",
    "éclat d'ecorce",
    "éclat de pin",
    "éclat de pomme",
    "éclat de sève",
    "éclat de seve",
    "éclat de botte",
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
    "éclat de cerceau",
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
    "éclat de pierre",
    "éclat de grille",
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
    "éclat de pince",
    "éclat d'horloge",
    "éclat de horloge",
    "éclat d'orange",
    "éclat de orange",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat d'écorce",
    "éclat de laine",
    "éclat de lampe",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de gouttière",
    "éclat de gouttiere",
    "éclat de croissant",
    "éclat de réverbère",
    "éclat de reverbere",
    "éclat de cloche",
    "éclat de corbeille",
    "éclat de sac",
    "éclat de panier",
    "éclat de dorure",
    "éclat de carte",
    "éclat de boule",
    "éclat de galet",
    "éclat de cube",
    "éclat de bois",
    "éclat de poussière",
    "éclat de poussiere",
    "éclat de cour",
    "éclat d'enveloppe",
    "éclat de enveloppe",
    "éclat de résine",
    "éclat de resine",
    "éclat de cageot",
    "éclat de platane",
    "éclat de crochet",
    "éclat de rotin",
    "point de gouttière",
    "point de gouttiere",
    "lune d'étain",
    "lune d'etain",
    "grain de pin",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de portail",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_le_cerceau_jusqu_au_chat; "
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
            "sous_texte=mila_a_des_lunettes_pas_rire; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="cerceau",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=ils_tiennent_le_cerceau_a_deux; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de portail",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=il_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de portail",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_fer; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "pas rire",
    "accepted_examples": (
        "pas rire | on joue | jouer | pas rire apparence"
    ),
    "retry_prompt": "Pas rire. Mila a des lunettes. Que fait-on ?",
    "engine_ok_text": "Oui, pas rire.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "cerceau,gravier",
        [
            "narrateur|Le portail s'ouvre, un peu.",
            "narrateur|Le fer grince, sec et long.",
            "enfant-m|Ça grince, papa !",
            "papa|Tu l'entends, le fer ?",
            "enfant-m|Oui, un petit cri.",
            "narrateur|Sur le fer, un éclat de portail brille.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|La gourde tape le bois du banc.",
            "narrateur|Elle fait toc, rond et sourd.",
            "enfant-m|J'ai entendu le toc.",
            "papa|La gourde, Raphaël ?",
            "enfant-m|Oui, papa.",
            "maman|Le plastique est lisse, sous la main.",
            "enfant-m|Il est un peu froid.",
            "narrateur|Une fourmi avance sur le gravier.",
            "narrateur|Le gravier fait criss, sous ses pattes.",
            "enfant-m|Elle est petite.",
            "papa|Tu la vois, la fourmi ?",
            "enfant-m|Oui, papa.",
            "narrateur|En ce moment, Raphaël tient le cerceau.",
            "narrateur|Le plastique bleu est un peu froid.",
            "enfant-m|Je veux qu'il aille au muret.",
            "enfant-m|Sans tomber, maintenant !",
            "papa|Jusqu'au chat ?",
            "enfant-m|Oui, papa.",
            "maman|Tout droit, sur le gravier ?",
            "enfant-m|Oui, tout droit.",
            "narrateur|Un chat gris dort sur le muret.",
            "narrateur|Sa queue pend un peu.",
            "enfant-m|Il dort.",
            "papa|Tout rond, Raphaël ?",
            "enfant-m|Oui.",
            "narrateur|Mila arrive près du banc.",
            "narrateur|Ses pas font criss sur le gravier.",
            "narrateur|Mila a des lunettes.",
            "narrateur|Mila a les cheveux bouclés.",
            "narrateur|Elle porte un gilet bleu.",
            "papa|Mila, tu rattrapes au muret ?",
            "enfant-m|Tu m'aides, Mila ?",
            "copine|Oui.",
            "narrateur|Raphaël regarde les lunettes, trop longtemps.",
            "narrateur|Un rire commence dans sa bouche.",
            "narrateur|Mila ne dit rien.",
            "narrateur|Le sourire de Mila disparaît.",
            "enfant-m|Tu vas au muret, maintenant !",
            "narrateur|Mila recule d'un pas.",
            "copine|Non.",
            "enfant-m|Oh.",
            "narrateur|Raphaël pousse le cerceau trop vite, tout seul.",
            "narrateur|Le cerceau tape la gourde.",
            "narrateur|Il tombe à plat.",
            "narrateur|Le plastique fait un toc mou.",
            "enfant-m|Il ne va pas !",
            "copine|La gourde est là.",
            "narrateur|L'éclat de portail tremble, puis tient.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Mila, Raphaël ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains sont froides, Raphaël ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Mila a des lunettes.",
            "narrateur|Que fait-on ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "cerceau",
        [
            "narrateur|Raphaël veut le cerceau au muret, tout de suite.",
            "enfant-m|Je pousse, maintenant !",
            "narrateur|Il avance trop vite vers Mila.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copine|Non.",
            "narrateur|Mila reste un peu plus loin.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Raphaël refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le cerceau, un instant.",
            "narrateur|Il écoute le grincement du portail.",
            "papa|Tu veux le cerceau avec Mila ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Tu rattrapes au muret ?",
            "narrateur|Mila ne dit rien, d'abord.",
            "narrateur|Elle pose les mains près du plastique.",
            "copine|Je le tiens.",
            "enfant-m|D'accord.",
            "papa|Merci, Raphaël.",
            "narrateur|Papa a vu les deux, près du banc.",
            "maman|La gourde a bougé, sous le cerceau.",
            "enfant-m|Elle est tombée.",
            "narrateur|Ils écartent la gourde du chemin.",
            "narrateur|Mila tient le plastique, plus près.",
            "narrateur|Le cerceau redevient plus léger, cette fois.",
            "enfant-m|Il tient !",
            "copine|Oui.",
            "papa|Tu le vois, le cerceau ?",
            "enfant-m|Oui, papa.",
            "maman|Au muret, Mila ?",
            "copine|J'y vais.",
            "narrateur|Raphaël pousse, sans se presser.",
            "narrateur|Mila suit le plastique des yeux.",
            "narrateur|Le cerceau avance un peu.",
            "copine|Il roule.",
            "enfant-m|Il roule.",
            "narrateur|Le ventre de Raphaël se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près du banc ?",
            "enfant-m|Oui.",
            "maman|Tes mains sont au chaud ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "cerceau",
        [
            "narrateur|Le cerceau roule, plus vite.",
            "copine|Il avance.",
            "enfant-m|Jusqu'au chat, maintenant !",
            "narrateur|Le gilet bleu bouge.",
            "narrateur|Les boucles tapent le dos.",
            "narrateur|Les lunettes restent sur le nez.",
            "narrateur|Le chat ouvre un œil.",
            "narrateur|Sa queue tombe sur le gravier.",
            "enfant-m|Il passe, maintenant !",
            "narrateur|Il pousse trop vite, tout de suite.",
            "narrateur|Il regarde les lunettes, trop longtemps.",
            "narrateur|Un rire revient dans sa bouche.",
            "copine|Attends.",
            "narrateur|Mila lâche le plastique.",
            "narrateur|Le cerceau penche vers la queue.",
            "enfant-m|Ça tombe !",
            "narrateur|Raphaël avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Raphaël refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le cerceau, un instant.",
            "narrateur|Il écoute le grincement du portail.",
            "narrateur|Sur le fer, un éclat de portail luit.",
            "enfant-m|Là, sur le fer.",
            "enfant-m|Tu rattrapes, Mila ?",
            "narrateur|Mila ne dit rien.",
            "narrateur|Elle reprend le plastique, sans parler.",
            "copine|Oui.",
            "narrateur|Ils attendent un peu.",
            "narrateur|Le chat rentre sa queue.",
            "narrateur|Raphaël pousse, sans se presser.",
            "narrateur|Mila rattrape.",
            "copine|Je l'ai !",
            "enfant-m|Il n'est pas tombé.",
            "papa|Tu as poussé sans t'arrêter ?",
            "enfant-m|Oui, papa.",
            "maman|Le gilet est chaud, Mila ?",
            "copine|Un peu.",
            "narrateur|Le cerceau se pose contre le muret.",
            "papa|On reverse les rôles ?",
            "copine|À toi le muret.",
            "narrateur|Mila pousse à son tour.",
            "narrateur|Raphaël rattrape.",
            "narrateur|Le plastique tape le bois.",
            "enfant-m|Toc.",
            "papa|Le cerceau est arrivé ?",
            "enfant-m|Oui, papa.",
            "maman|Un rayon passe sur le fer.",
            "enfant-m|Il allume le gilet.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "",
        [
            "narrateur|Ils restent près du banc.",
            "narrateur|Maman essuie un peu de gravier.",
            "enfant-m|On a eu le cerceau, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, au muret.",
            "maman|On est bien, ici.",
            "narrateur|Raphaël tapote le plastique du doigt.",
            "enfant-m|Il a une trace de gourde.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|Le cerceau est resté, Raphaël.",
            "enfant-m|Oui, avec Mila.",
            "copine|Le cerceau est resté.",
            "narrateur|Ça sent le fer, un peu tiède.",
            "enfant-m|Et le portail, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|La fourmi reste sur le gravier.",
            "narrateur|Un éclat de portail tient sur le fer.",
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
    if n_clue != 4:
        raise SystemExit(f"{SID}: {INDICE} ×{n_clue} (voulu 4)")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: manque refuse de foncer")
    if "enfant-f|" in blob:
        raise SystemExit(f"{SID}: enfant-f (Raphaël = enfant-m, Mila = copine)")
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
        "pas rire",
        "lunettes aident",
        "l'amitié ne dépend pas",
        "apparence",
        "pas une blague",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Mila a des lunettes. Que fait-on ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "pas rire":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = str(q.get("retry_prompt") or "").lower()
    if "que fait-on" not in retry:
        raise SystemExit(f"{SID}: retry sans Que fait-on")
    if "pas rire" not in retry:
        raise SystemExit(f"{SID}: retry sans pas rire")
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
    if "gourde" not in blob:
        raise SystemExit(f"{SID}: manque gourde")
    if "fourmi" not in blob:
        raise SystemExit(f"{SID}: manque fourmi")
    if "portail" not in blob:
        raise SystemExit(f"{SID}: manque portail")
    if "cerceau" not in blob:
        raise SystemExit(f"{SID}: manque cerceau")
    if "gravier" not in blob:
        raise SystemExit(f"{SID}: manque gravier")
    if "banc" not in blob:
        raise SystemExit(f"{SID}: manque banc")
    if "chat" not in blob:
        raise SystemExit(f"{SID}: manque chat")
    for ban in (
        "éclat de cerceau",
        "éclat de gravier",
        "éclat de pierre",
        "éclat de volet",
        "grain de",
        "tout doux",
        "tout calme",
        "bon travail",
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
        "- **Leçon :** DIF.COR.003 — Mila a des lunettes "
        "(vécue : rire qui commence, Mila se tait, cerceau qui tape la "
        "gourde, ils tiennent le plastique à deux). JAMAIS dite dans le récit.\n"
        "- **Personnages :** Raphaël, Mila, papa, maman. Maman ajoutée. "
        "Raphaël = enfant-m (propose, trop vite). Mila = copine "
        "(silence, non, attends, lunettes, boucles, gilet bleu). "
        "Troupe D16. Pas de maîtresse. Éléonore hors troupe.\n"
        "- **Lieu :** square, portail, gravier, cerceau bleu, banc, "
        "gourde, fourmi, muret, chat. Monde xlsx (square, portail, "
        "cerceaux). ≠ 003-01 entrée/botte, ≠ 003-02 pin/résine.\n"
        "- **Indice unique :** éclat de portail (brille à l'ouverture, "
        "fer qui grince → tremble à la gourde → luit au refus → tient "
        "sur le fer). BAN éclat de cerceau (001-04) / éclat de gravier "
        "(trop proche pierre) / grain de.\n"
        "- **Question moteur :** « Mila a des lunettes. Que fait-on ? » "
        "expected **pas rire**. accepted `pas rire | on joue | jouer | "
        "pas rire apparence`. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le portail s'ouvre. Le fer grince. Sur le fer, un "
        "éclat de portail brille. Gourde, toc, fourmi, cerceau bleu. "
        "Raphaël veut le cerceau jusqu'au chat **maintenant**. Mila "
        "arrive. Un rire commence. Mila se tait, recule : non. Raphaël "
        "pousse tout seul : le cerceau tape la gourde. Sourire parti. "
        "Papa s'accroupit. Il refuse de foncer. Ils tiennent le "
        "plastique. Merci vécu. Deuxième ruse : queue du chat sur le "
        "gravier, rire qui revient, Mila lâche. Il s'arrête, lit "
        "l'éclat. Un éclat de portail tient sur le fer.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : square, portail, gravier, banc, gourde, fourmi, "
        "muret. ≠ 003-01 entrée/botte, ≠ 003-02 pin.\n"
        "- Désir : le cerceau bleu jusqu'au chat, maintenant.\n"
        "- Objet : cerceau bleu, gourde, lunettes, gilet bleu.\n"
        "- Indice unique : éclat de portail, vu dès l'ouverture, payé "
        "sur le fer. Pas éclat de cerceau / éclat de gravier.\n"
        "- Urgence douce : Mila arrive, le chat dort, Raphaël accélère.\n"
        "- Imprévu 1 : rire sur les lunettes, Mila absente au moment "
        "de pousser, le cerceau tape la gourde.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« d'accord ».\n"
        "- Imprévu 2 (plus rusé) : queue du chat sur le chemin, rire "
        "qui revient, Mila lâche, cerceau qui penche.\n"
        "- Résolution : il refuse de foncer, observe, écoute le "
        "grincement, retrouve l'éclat, attend la queue, Mila rattrape.\n"
        "- Retour : cerceau au muret, trace de gourde, éclat sur "
        "le fer.\n\n"
        "## Vécu\n\n"
        "Raphaël veut le cerceau jusqu'au chat **maintenant**. "
        "Impatience, puis rire qui commence, sourire de Mila qui part. "
        "Mila prend son temps, pose sa limite (non, attends, silence). "
        "Papa se baisse, pose une question, ne récite pas la règle. "
        "Ils agissent : plastique tenu, poussée sans se presser. Merci "
        "vécu. Fin : l'éclat du début tient sur le fer.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le cerceau jusqu'au chat (noyau dump). Relance : "
        "Que fait-on ? expected pas rire (xlsx, pas le dump « jouer »).\n"
        "- Lieu du dump (square, muret, gravier) + monde xlsx "
        "(portail, cerceau) + gourde, fourmi, banc. Maman ajoutée. "
        "Mila = copine.\n"
        "- Ouverture inventée (portail qui s'ouvre, fer qui grince), "
        "pas un gabarit v2, pas « Un chat gris dort sur le muret » du "
        "dump, pas « Raphaël est au square ».\n"
        "- Indice unique : éclat de portail. BAN éclat de cerceau / "
        "éclat de gravier / éclat de pierre / grain de. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » / Bravo spam du dump.\n"
        "- Leçon non dite : on la voit quand le rire s'arrête, quand "
        "Mila recule, quand ils tiennent le cerceau. Pas « Mila a des "
        "lunettes, on joue » hors question. Pas « on joue » / "
        "« vous jouez » / « il ne faut pas rire » / « pas rire ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Mila a des lunettes. Que "
        "fait-on ? ». expected pas rire. 5 chunks, kinds inchangés.\n"
        "- example4 014 / 046 / 078 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_cor_003_02.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le muret.\n"
        f"- {nwords} mots. N2 ≤ 15. `check()` OK. Pas apply.\n\n"
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
