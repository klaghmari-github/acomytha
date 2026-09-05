#!/usr/bin/env python3
"""ATOM-DIF.COR.003-05 — Le toit rouge d'Amir (F-NAR-019, N2, DIF.COR.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.003-05"
TITLE = "Le toit rouge d'Amir"
N2 = LIMITS["N2"]
CHARS = "Amir, Nino, papa, maman"
SETTING = "école, couloir, cour, crochets, craie, manteau rouge, crayons"
INDICE = "éclat de crochet"
FIL = (
    "Un crochet penche vers le mur. Sur le métal, un "
    "éclat de crochet brille. Amir veut un toit rouge, "
    "maintenant. Nino arrive. Un rire commence. Nino se tait. "
    "Le crayon tape le sol. Amir refuse de foncer. Ils "
    "tiennent la feuille, à deux. Merci vécu. Le manteau glisse. "
    "L'éclat de crochet tient sur le métal."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(botte|bottes|résine|resine|cageot|platane|écorce|ecorce|"
    r"limace|perron|chaise|tiroir|fraisier|cuivre|buis|coussin|"
    r"figue|robinet|planche|cerceau|émail|email|samare|bassine|"
    r"entrée|entree|carreau|carreaux)\b",
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
    "pas une blague",
    "n'est pas une blague",
    "n est pas une blague",
    "tu as des lunettes",
    "pas rire",
    "apparence",
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
    "éclat de cour",
    "éclat de pince",
    "éclat d'horloge",
    "éclat de horloge",
    "éclat d'orange",
    "éclat de orange",
    "éclat d'ombre",
    "éclat de ombre",
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
    "éclat d'enveloppe",
    "éclat de enveloppe",
    "éclat de cageot",
    "éclat de platane",
    "éclat de résine",
    "éclat de resine",
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
        emphasis="éclat de crochet",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_un_toit_rouge_maintenant; "
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
            "sous_texte=pas_rire_nino_a_des_lunettes; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="feuille",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=ils_tiennent_la_feuille_a_deux; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de crochet",
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
        emphasis="éclat de crochet",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_le_metal; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "pas rire",
    "accepted_examples": (
        "pas rire | on joue | jouer | pas rire apparence"
    ),
    "retry_prompt": "Pas rire. Nino a des lunettes. Que fait-on ?",
    "engine_ok_text": "Oui, pas rire.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "cour,crayons",
        [
            "narrateur|Un crochet de manteau penche vers le mur.",
            "narrateur|Le métal est froid, près de la porte.",
            "enfant-m|Ça cliquette, papa !",
            "papa|Tu l'entends, le petit bruit ?",
            "enfant-m|Oui, un clic.",
            "narrateur|Dans le couloir, les crochets sentent le tissu.",
            "narrateur|Sur le métal, un éclat de crochet brille.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|Un bout de craie attend, côté cour.",
            "narrateur|Il est court, un peu blanc.",
            "enfant-m|J'ai vu la craie.",
            "papa|Elle est au sol, Amir ?",
            "enfant-m|Oui, papa.",
            "maman|La feuille est rêche, sous la main.",
            "enfant-m|Elle gratte un peu.",
            "narrateur|Papa pose une boîte près du banc.",
            "narrateur|Dedans, des crayons, serrés.",
            "maman|Les crayons sentent le papier, Amir ?",
            "enfant-m|Un peu, maman.",
            "narrateur|En ce moment, Amir tient une feuille.",
            "narrateur|Il veut un toit rouge, tout de suite.",
            "enfant-m|Je dessine une maison, maintenant !",
            "enfant-m|Avec un toit rouge.",
            "papa|Un toit rouge, pour maman ?",
            "enfant-m|Oui, papa.",
            "maman|Tu veux le rouge, Amir ?",
            "enfant-m|Oui, le rouge.",
            "narrateur|Nino arrive près des crochets.",
            "narrateur|Ses pas font un bruit sec.",
            "narrateur|Nino a des lunettes.",
            "narrateur|Nino a les cheveux courts.",
            "narrateur|Il porte un manteau rouge.",
            "papa|Nino, tu poses le manteau ?",
            "enfant-m|Tu colories avec moi ?",
            "copain|Oui.",
            "narrateur|Nino accroche le manteau rouge.",
            "narrateur|Le crochet penche un peu plus.",
            "narrateur|Amir regarde les lunettes, trop longtemps.",
            "narrateur|Un rire commence dans sa bouche.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Le sourire de Nino disparaît.",
            "enfant-m|Tu prends le jaune, maintenant !",
            "narrateur|Nino recule d'un pas.",
            "copain|Non.",
            "enfant-m|Oh.",
            "narrateur|Amir prend le crayon rouge, tout seul.",
            "narrateur|Le crayon roule hors de la feuille.",
            "narrateur|Il tape le sol, trop vite.",
            "narrateur|Ça fait un bruit dur.",
            "narrateur|Un peu de craie colle au rouge.",
            "enfant-m|Il ne tient pas !",
            "copain|Il est tombé.",
            "narrateur|L'éclat de crochet tremble, puis tient.",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Nino, Amir ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains sont froides, Amir ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nino a des lunettes.",
            "narrateur|Que fait-on ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "crayons",
        [
            "narrateur|Amir veut le toit rouge, tout de suite.",
            "enfant-m|Je colorie, maintenant !",
            "narrateur|Il avance trop vite vers Nino.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copain|Non.",
            "narrateur|Nino reste un peu plus loin.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Amir refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe le crayon, un instant.",
            "narrateur|Il écoute le clic du crochet.",
            "papa|Tu veux le toit avec Nino ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Tu tiens la feuille ?",
            "narrateur|Nino ne dit rien, d'abord.",
            "narrateur|Il pose les mains sur le papier.",
            "copain|Je la tiens.",
            "enfant-m|D'accord.",
            "papa|Merci, Amir.",
            "narrateur|Papa a vu les deux, près du banc.",
            "maman|La craie colle un peu, sous les doigts.",
            "enfant-m|Elle est sèche.",
            "narrateur|Ils essuient le crayon sur le banc.",
            "narrateur|Nino tient la feuille, plus près.",
            "narrateur|Le crayon redevient plus ferme, cette fois.",
            "enfant-m|Il tient !",
            "copain|Oui.",
            "papa|Tu le vois, le rouge ?",
            "enfant-m|Oui, papa.",
            "maman|Le ciel, Nino ?",
            "copain|J'y vais.",
            "narrateur|Amir trace, sans se presser.",
            "narrateur|Nino suit le trait des yeux.",
            "narrateur|Nino pose le jaune, une fois.",
            "copain|Le soleil.",
            "enfant-m|Le ciel.",
            "narrateur|Le ventre d'Amir se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste près du banc ?",
            "enfant-m|Oui.",
            "maman|Tes mains sont au chaud ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "crayons",
        [
            "narrateur|Amir trace le toit, plus vite.",
            "copain|La porte.",
            "enfant-m|La fenêtre.",
            "narrateur|Le manteau rouge bouge.",
            "narrateur|Le crochet penche.",
            "narrateur|Les lunettes restent sur le nez.",
            "enfant-m|Le rouge, maintenant !",
            "narrateur|Il colorie trop vite, tout de suite.",
            "narrateur|Il regarde les lunettes, trop longtemps.",
            "narrateur|Un rire revient dans sa bouche.",
            "copain|Attends.",
            "narrateur|Nino lâche la feuille.",
            "narrateur|Le manteau glisse du crochet.",
            "enfant-m|Ça tombe !",
            "narrateur|Amir avance les mains, trop vite.",
            "narrateur|Le pied part vers le papier.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Amir refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe le manteau, un instant.",
            "narrateur|Il écoute le clic du crochet.",
            "narrateur|Sur le métal, un éclat de crochet luit.",
            "enfant-m|Là, sur le crochet.",
            "enfant-m|Tu tiens la feuille, Nino ?",
            "narrateur|Nino ne dit rien.",
            "narrateur|Il reprend le papier, sans parler.",
            "copain|Oui.",
            "narrateur|Ils accrochent le manteau, sans se presser.",
            "narrateur|Amir colorie, tout près de Nino.",
            "narrateur|Nino pose le jaune.",
            "copain|Le soleil !",
            "enfant-m|Le toit !",
            "papa|Tu as fini le rouge ?",
            "enfant-m|Oui, papa.",
            "maman|Le manteau est chaud, Nino ?",
            "copain|Un peu.",
            "narrateur|Le crayon se pose dans la boîte.",
            "papa|On reverse les rôles ?",
            "copain|À toi le jaune.",
            "narrateur|Nino prend le rouge à son tour.",
            "narrateur|Amir pose le bleu.",
            "narrateur|Ses doigts font un trait.",
            "enfant-m|C'est plus facile.",
            "papa|Le trait est net ?",
            "enfant-m|Oui, papa.",
            "maman|Un rayon passe près des crochets.",
            "enfant-m|Il allume le manteau.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "crochets",
        [
            "narrateur|Ils restent près des crochets.",
            "narrateur|Maman essuie un peu de craie.",
            "enfant-m|On a eu le toit rouge, papa.",
            "papa|Tu l'as vu, toi ?",
            "enfant-m|Oui, sur la feuille.",
            "maman|On est bien, ici.",
            "narrateur|Amir tapote le papier du doigt.",
            "enfant-m|Il a une trace de craie.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|La feuille est restée, Amir.",
            "enfant-m|Oui, avec Nino.",
            "copain|La feuille est restée.",
            "narrateur|Ça sent le crayon, un peu tiède.",
            "enfant-m|Et le manteau, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|Le manteau rouge reste au crochet.",
            "narrateur|Un éclat de crochet tient sur le métal.",
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
        if role not in ("narrateur", "papa", "maman", "enfant-m", "copain"):
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
        raise SystemExit(f"{SID}: enfant-f (Amir = enfant-m, Nino = copain)")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: Nino absent (copain)")
    if "copine|" in blob:
        raise SystemExit(f"{SID}: copine")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-m", "copain") for r in roles):
        raise SystemExit(f"{SID}: rôle hors troupe")
    if not any(r == "papa" for r in roles):
        raise SystemExit(f"{SID}: papa absent")
    if not any(r == "maman" for r in roles):
        raise SystemExit(f"{SID}: maman absente")
    if not any(r == "copain" for r in roles):
        raise SystemExit(f"{SID}: copain absent")
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
        "l'amitié ne dépend pas",
        "apparence",
        "pas une blague",
        "pas rire",
        "tu as des lunettes",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Nino a des lunettes. Que fait-on ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "pas rire":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = str(q.get("retry_prompt") or "").lower()
    if "que fait-on" not in retry:
        raise SystemExit(f"{SID}: retry sans Que fait-on")
    if "pas rire" not in retry:
        raise SystemExit(f"{SID}: retry sans pas rire")
    copain_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copain|")
    ).lower()
    if "non" not in copain_txt:
        raise SystemExit(f"{SID}: Nino sans non")
    if "attends" not in copain_txt:
        raise SystemExit(f"{SID}: Nino sans attends")
    if "manteau rouge" not in blob:
        raise SystemExit(f"{SID}: manque manteau rouge")
    if "craie" not in blob:
        raise SystemExit(f"{SID}: manque craie")
    if "crochet" not in blob:
        raise SystemExit(f"{SID}: manque crochet")
    if "toit rouge" not in blob:
        raise SystemExit(f"{SID}: manque toit rouge")
    for ban in (
        "éclat de craie",
        "éclat de cartable",
        "éclat de couloir",
        "éclat de cour",
        "éclat de manteau",
        "éclat de crayon",
        "éclat de botte",
        "éclat de résine",
        "éclat de resine",
        "éclat de cageot",
        "éclat de platane",
        "tout doux",
        "tout calme",
        "alban",
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
        "- **Leçon :** DIF.COR.003 — Nino a des lunettes "
        "(vécue : rire qui commence, Nino se tait, crayon qui tape, "
        "manteau qui glisse, ils tiennent la feuille à deux). JAMAIS dite "
        "dans le récit.\n"
        "- **Personnages :** Amir, Nino, papa, maman. Papa ajouté. "
        "Amir = enfant-m (propose, trop vite). Nino = copain "
        "(silence, non, attends). Troupe D16. Pas de maîtresse. Pas Alban.\n"
        "- **Lieu :** école, couloir, cour, crochets de manteaux, craie, "
        "manteau rouge, crayons, banc, feuille. ≠ 003-01 botte / 003-02 "
        "résine / 003-03 cageot / 003-04 platane.\n"
        "- **Indice unique :** éclat de crochet (brille à l'ouverture → "
        "tremble au crayon → luit au refus → tient sur le métal). BAN "
        "éclat de craie / cartable / couloir / cour / manteau / crayon / "
        "botte / résine / cageot / platane.\n"
        "- **Question moteur :** « Nino a des lunettes. Que fait-on ? » "
        "expected **pas rire**. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un crochet de manteau penche vers le mur. Sur le métal, un "
        "éclat de crochet brille. Craie côté cour, crayons dans la boîte. "
        "Amir veut un toit rouge **maintenant**. Nino arrive, manteau rouge. "
        "Un rire commence. Nino se tait, recule : non. Amir colorie tout "
        "seul : le crayon tape. Sourire parti. Papa s'accroupit. Il "
        "refuse de foncer. Ils tiennent la feuille. Merci vécu. Deuxième "
        "ruse : toit trop vite, rire qui revient, manteau qui glisse, "
        "pied vers le papier. Il s'arrête, lit l'éclat. Un éclat de "
        "crochet tient sur le métal.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : école, couloir, cour, crochets, craie, crayons, banc. "
        "≠ 003-01 entrée/botte, ≠ 003-02 pin/résine.\n"
        "- Désir : un toit rouge sur la feuille, maintenant, pour maman.\n"
        "- Objet : crayon rouge, feuille, manteau rouge, crochet, craie.\n"
        "- Indice unique : éclat de crochet, vu dès l'ouverture, payé "
        "sur le métal. Pas éclat de craie / cartable / couloir / cour.\n"
        "- Urgence douce : Nino arrive, le toit attend, Amir accélère.\n"
        "- Imprévu 1 : rire sur les lunettes, Nino absent au moment "
        "de colorier, le crayon tape le sol.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« d'accord ».\n"
        "- Imprévu 2 (plus rusé) : toit trop vite, rire qui revient, "
        "manteau qui glisse du crochet, pied vers le papier.\n"
        "- Résolution : il refuse de foncer, observe, écoute le clic, "
        "retrouve l'éclat, ils accrochent le manteau, Nino reprend "
        "la feuille.\n"
        "- Retour : toit rouge, manteau au crochet, éclat sur le métal.\n\n"
        "## Vécu\n\n"
        "Amir veut le toit rouge **maintenant**. Impatience, puis "
        "rire qui commence, sourire de Nino qui part. Nino prend son "
        "temps, pose sa limite (non, attends, silence). Papa se baisse, "
        "pose une question, ne récite pas la règle. Ils agissent : "
        "feuille tenue, traits sans se presser, manteau raccroché. "
        "Merci vécu. Fin : l'éclat du début tient sur le métal.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Le toit rouge d'Amir (noyau dump). Relance : "
        "Que fait-on ? expected pas rire.\n"
        "- Lieu du dump (école, couloir, cour, crochets, craie, "
        "manteau rouge, crayons). Maman du dump. Papa ajouté. "
        "Nino = copain. Amir à la place d'Alban.\n"
        "- Ouverture inventée (crochet qui penche), pas un gabarit "
        "v2, pas « Le robinet de la cour laisse une goutte » du dump.\n"
        "- Indice unique : éclat de crochet. BAN éclat de craie / "
        "cartable / couloir / cour / manteau / crayon / botte / résine / "
        "cageot / platane. Pas tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » du dump.\n"
        "- Leçon non dite : on la voit quand le rire s'arrête, quand "
        "Nino recule, quand ils tiennent la feuille. Pas « Nino a des "
        "lunettes, on joue » hors question. Pas « on joue » / "
        "« vous jouez » / « il ne faut pas rire » / « pas rire » / "
        "« tu as des lunettes ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Nino a des lunettes. Que "
        "fait-on ? ». expected pas rire. accepted pas rire | on joue | "
        "jouer | pas rire apparence. 5 chunks, kinds inchangés.\n"
        "- example4 012 / 044 / 076 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_cor_003_02.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le toit.\n"
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
