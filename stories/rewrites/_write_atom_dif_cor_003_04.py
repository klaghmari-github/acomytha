#!/usr/bin/env python3
"""ATOM-DIF.COR.003-04 — L'étoile et la feuille (F-NAR-019, N3, DIF.COR.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.003-04"
TITLE = "L'étoile et la feuille"
N3 = LIMITS["N3"]
CHARS = "Sarah, Victorina, papa, maman"
SETTING = "parc sous les platanes, bac à feuilles, puis atelier (pâte, emporte-pièce)"
INDICE = "éclat de platane"
FIL = (
    "Un platane lâche un petit bruit, sec. Sur le bord du bac, un "
    "éclat de platane brille. Sarah veut une étoile avec une feuille, "
    "maintenant. Victorina arrive. Un rire commence. Victorina se tait. "
    "La feuille sèche casse. Sarah refuse de foncer. Elles portent la "
    "souple. Merci vécu. L'emporte-pièce trop vite. L'éclat de platane "
    "tient sur la manche."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(botte|bottes|résine|resine|cageot|limace|perron|chaise|"
    r"tiroir|fraisier|cuivre|buis|coussin|figue|robinet|planche|"
    r"cerceau|émail|email|samare|bassine|entrée|entree|givre|"
    r"toboggan)\b",
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
    "les lunettes aident",
    "les cheveux sont les cheveux",
    "l'habit tient chaud",
    "tu as des lunettes",
    "l'amitié ne dépend pas",
    "l'amitie ne depend pas",
    "vous jouez",
    "on joue",
    "pas une blague",
    "n'est pas une blague",
    "n est pas une blague",
    "pas rire",
    "apparence",
    "grain de",
    "marque fine",
    "ombre en forme",
    "minuscule symbole",
    "tache de couleur",
    "éclat de pince",
    "éclat de marche",
    "éclat de corde",
    "éclat de caisse",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cle",
    "éclat de cuillère",
    "éclat de cuillere",
    "éclat de sonnette",
    "éclat d'horloge",
    "éclat de tasse",
    "éclat d'orange",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat de farine",
    "éclat d'ombre",
    "éclat d'écorce",
    "éclat d'ecorce",
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
    "éclat de sac",
    "éclat de panier",
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
    "éclat d'émail",
    "éclat d'email",
    "éclat de samare",
    "éclat de bassine",
    "éclat de cerceau",
    "éclat de robinet",
    "éclat de planche",
    "éclat de figue",
    "éclat de coussin",
    "éclat de cuivre",
    "éclat de buis",
    "éclat de tiroir",
    "éclat de fraisier",
    "éclat de chaise",
    "éclat de perron",
    "éclat de limace",
    "éclat de botte",
    "éclat de résine",
    "éclat de resine",
    "éclat de cageot",
    "éclat de feuille",
    "éclat de pin",
    "éclat de pomme",
    "éclat de sable",
    "éclat de foin",
    "éclat de paille",
    "éclat de pépin",
    "éclat de pepin",
    "éclat de lavande",
    "éclat de miette",
    "éclat de lunettes",
    "éclat de gilet",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de platane",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=elle_veut_l_etoile_maintenant; "
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
            "sous_texte=on_ne_rit_pas_victorina_a_des_lunettes; "
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
            "destinataire=enfant; sous_texte=elles_portent_la_feuille_a_deux; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de platane",
        note=(
            "arc=action; intention=entraîner; emotion=élan puis prudence; "
            "intensite=2; destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=vif puis posé; sourire=léger; respiration=courte"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de platane",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_la_manche; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "pas rire",
    "accepted_examples": (
        "pas rire | on joue | jouer | pas rire apparence"
    ),
    "retry_prompt": "On cherche une feuille souple. Que fait-on ?",
    "engine_ok_text": "Oui, pas rire.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc,pate",
        [
            "narrateur|Un platane lâche un petit bruit, sec.",
            "enfant-f|J'ai entendu, papa !",
            "papa|Tu as entendu le platane ?",
            "enfant-f|Oui, un petit bruit.",
            "narrateur|Un éclat pâle glisse le long du tronc.",
            "enfant-f|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-f|Oui, pâle.",
            "narrateur|Il s'arrête sur le bord du bac.",
            "narrateur|Sur le bord du bac, un éclat de platane brille.",
            "papa|Le bac est froid, Sarah ?",
            "enfant-f|Un peu, papa.",
            "narrateur|Le bac sent le platane, un peu humide.",
            "maman|Tes mains sont froides, Sarah ?",
            "enfant-f|Un peu.",
            "papa|On les frotte ?",
            "enfant-f|Oui.",
            "narrateur|Sarah frotte ses mains.",
            "narrateur|Elles redeviennent tièdes.",
            "narrateur|En ce moment, Sarah cherche une feuille.",
            "enfant-f|Je veux une étoile, maintenant !",
            "enfant-f|Avec une feuille dessus.",
            "maman|On la presse dans la pâte ?",
            "enfant-f|Oui.",
            "papa|Une vraie nervure, alors ?",
            "enfant-f|Oui, papa.",
            "narrateur|Victorina arrive près du bac.",
            "narrateur|Victorina a des lunettes rondes.",
            "narrateur|Elle a les cheveux tressés.",
            "narrateur|Elle porte un gilet jaune.",
            "papa|Victorina, tu cherches aussi ?",
            "enfant-f|Tu m'aides, Victorina ?",
            "copine|Oui.",
            "narrateur|Sarah ramasse une feuille trop vite.",
            "narrateur|La feuille est sèche et fragile.",
            "narrateur|Elle s'effrite entre les doigts.",
            "enfant-f|Elle casse !",
            "narrateur|Sarah regarde les lunettes, trop longtemps.",
            "narrateur|Un rire commence dans sa bouche.",
            "narrateur|Victorina ne dit rien.",
            "narrateur|Le sourire de Victorina disparaît.",
            "enfant-f|Tu la trouves, maintenant !",
            "copine|Non.",
            "narrateur|Victorina recule d'un pas.",
            "enfant-f|Oh.",
            "narrateur|Sarah veut presser toute seule.",
            "narrateur|La feuille sèche tombe dans le bac.",
            "narrateur|Ça fait un bruit mou.",
            "narrateur|L'éclat de platane tremble, puis tient.",
            "narrateur|Le sourire de Sarah disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Victorina, Sarah ?",
            "enfant-f|Oui, papa.",
            "maman|Tes mains sont collantes, Sarah ?",
            "enfant-f|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Victorina a des lunettes.",
            "narrateur|Que fait-on ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "pate",
        [
            "narrateur|Sarah veut l'étoile, tout de suite.",
            "enfant-f|Je presse, maintenant !",
            "narrateur|Elle avance trop vite vers Victorina.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copine|Non.",
            "narrateur|Victorina reste un peu plus loin.",
            "enfant-f|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Elle observe le bac, un instant.",
            "narrateur|Elle écoute le petit bruit du platane.",
            "papa|Tu veux l'étoile avec Victorina ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-f|Tu cherches avec moi ?",
            "narrateur|Victorina ne dit rien, d'abord.",
            "narrateur|Elle se penche sur le bac.",
            "copine|Celle-ci.",
            "copine|Elle est molle.",
            "enfant-f|D'accord.",
            "papa|Merci, Sarah.",
            "narrateur|Papa a vu les deux, près du bac.",
            "maman|La feuille est souple, sous les doigts.",
            "enfant-f|Elle ne casse pas.",
            "narrateur|Sarah pose la feuille dans sa main.",
            "narrateur|Victorina reste plus près.",
            "enfant-f|On va à l'atelier ?",
            "maman|Oui.",
            "maman|La pâte nous attend.",
            "papa|Tu portes la feuille, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ils passent sous les platanes.",
            "narrateur|Le gilet jaune bouge.",
            "narrateur|Les tresses tapent le dos.",
            "narrateur|Les lunettes restent sur le nez.",
            "enfant-f|La table, maman.",
            "maman|Elle est froide et lisse.",
            "narrateur|La pâte colle un peu aux doigts.",
            "papa|On étale, sans se presser ?",
            "enfant-f|Oui.",
            "narrateur|Sarah fait un boudin.",
            "narrateur|Victorina fait une boule.",
            "enfant-f|L'étoile.",
            "copine|La feuille.",
            "maman|Tes mains sont au chaud ?",
            "enfant-f|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "pate",
        [
            "narrateur|Sarah prend l'emporte-pièce.",
            "narrateur|Le métal est froid, un peu lourd.",
            "enfant-f|L'étoile, maintenant !",
            "narrateur|Elle appuie trop vite, tout de suite.",
            "narrateur|Elle regarde les lunettes, trop longtemps.",
            "narrateur|Un rire revient dans sa bouche.",
            "copine|Attends.",
            "narrateur|Victorina lâche le bord de la pâte.",
            "narrateur|La feuille glisse sur le côté.",
            "enfant-f|Ça part !",
            "narrateur|Sarah avance les mains, trop vite.",
            "narrateur|Puis elle s'arrête net.",
            "narrateur|Sarah refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Elle observe la pâte, un instant.",
            "narrateur|Elle écoute le petit bruit du platane.",
            "narrateur|Sur la manche, un éclat de platane luit.",
            "enfant-f|Là, sur la manche.",
            "enfant-f|Tu poses la feuille, Victorina ?",
            "narrateur|Victorina ne dit rien.",
            "narrateur|Elle reprend le bord, sans parler.",
            "copine|Oui.",
            "narrateur|Sarah appuie, sans se presser.",
            "narrateur|Victorina pose la feuille.",
            "narrateur|La nervure s'imprime dans la pâte.",
            "enfant-f|Elle est restée !",
            "copine|On voit les traits.",
            "papa|Tu as pressé sans t'arrêter ?",
            "enfant-f|Oui, papa.",
            "maman|Le gilet est chaud, Victorina ?",
            "copine|Un peu.",
            "narrateur|Un peu de pâte tombe.",
            "narrateur|Ça fait un nuage tout petit.",
            "papa|On pose l'étoile ?",
            "copine|Sur l'assiette.",
            "narrateur|L'assiette est blanche et mate.",
            "enfant-f|Ma feuille est dessus.",
            "maman|Oui.",
            "maman|Elle est souple.",
            "copine|On voit même les bords.",
            "papa|La pâte a tenu, Sarah ?",
            "enfant-f|Oui, papa.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "pate",
        [
            "narrateur|Ils restent près de la table.",
            "narrateur|Maman essuie un peu de pâte.",
            "enfant-f|On a eu l'étoile, papa.",
            "papa|Tu l'as vue, toi ?",
            "enfant-f|Oui, avec la feuille.",
            "maman|On est bien, ici.",
            "narrateur|Sarah tapote l'étoile du doigt.",
            "enfant-f|Elle a une trace de nervure.",
            "maman|Tu la vois, la trace ?",
            "enfant-f|Oui, maman.",
            "papa|L'étoile est restée, Sarah.",
            "enfant-f|Oui, avec Victorina.",
            "copine|L'étoile est restée.",
            "narrateur|Ça sent le platane, un peu tiède.",
            "enfant-f|Et la pâte, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|La feuille reste sur l'étoile.",
            "narrateur|Un éclat de platane tient sur la manche.",
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
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
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
        if role not in ("narrateur", "papa", "maman", "enfant-f", "copine"):
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
    if "enfant-m|" in blob:
        raise SystemExit(f"{SID}: enfant-m (Sarah = enfant-f, Victorina = copine)")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Victorina absente (copine)")
    if "copain|" in blob:
        raise SystemExit(f"{SID}: copain")
    if "maitresse|" in blob or "maîtresse" in blob:
        raise SystemExit(f"{SID}: maîtresse inventée")
    roles = [
        ln.split("|", 1)[0]
        for c in chunks
        for ln in c["script"].splitlines()
    ]
    if any(r not in ("narrateur", "papa", "maman", "enfant-f", "copine") for r in roles):
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
        "l'amitié ne dépend pas",
        "apparence",
        "pas une blague",
        "pas rire",
        "tu as des lunettes",
        "les cheveux sont les cheveux",
        "l'habit tient chaud",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Victorina a des lunettes. Que fait-on ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "pas rire":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = str(q.get("retry_prompt") or "")
    if retry != "On cherche une feuille souple. Que fait-on ?":
        raise SystemExit(f"{SID}: retry dump altéré: {retry}")
    accepted = str(q.get("accepted_examples") or "")
    if accepted != "pas rire | on joue | jouer | pas rire apparence":
        raise SystemExit(f"{SID}: accepted_examples altéré: {accepted}")
    copine_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    ).lower()
    if "non" not in copine_txt:
        raise SystemExit(f"{SID}: Victorina sans non")
    if "attends" not in copine_txt:
        raise SystemExit(f"{SID}: Victorina sans attends")
    if "platane" not in blob:
        raise SystemExit(f"{SID}: manque platane")
    if "bac" not in blob:
        raise SystemExit(f"{SID}: manque bac")
    if "pâte" not in blob and "pate" not in blob:
        raise SystemExit(f"{SID}: manque pâte")
    if "emporte-pièce" not in blob and "emporte-piece" not in blob:
        raise SystemExit(f"{SID}: manque emporte-pièce")
    if "atelier" not in blob:
        raise SystemExit(f"{SID}: manque atelier")
    for ban in (
        "éclat de botte",
        "éclat de résine",
        "éclat de resine",
        "éclat de cageot",
        "éclat de bassine",
        "éclat de farine",
        "éclat de feuille",
        "tout doux",
        "tout calme",
        "océane",
        "oceane",
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
        "- **Public :** N3 (≤16 mots/phrase), audio familial\n"
        "- **Leçon :** DIF.COR.003 — Victorina a des lunettes "
        "(vécue : rire qui commence, Victorina se tait, feuille sèche "
        "qui casse, elles portent la souple à deux). JAMAIS dite dans "
        "le récit.\n"
        "- **Personnages :** Sarah, Victorina, papa, maman. Papa ajouté. "
        "Sarah = enfant-f (propose, trop vite). Victorina = copine "
        "(silence, non, attends, lunettes rondes, tresses, gilet jaune). "
        "Troupe D16. Pas de maîtresse. Pas d'Océane.\n"
        "- **Lieu :** parc sous les platanes, bac à feuilles, puis "
        "atelier (pâte, emporte-pièce, assiette). ≠ 003-01 entrée/botte, "
        "≠ 003-02 pin/résine, ≠ 003-03 cageot/prune.\n"
        "- **Indice unique :** éclat de platane (brille au bac → "
        "tremble à la feuille sèche → luit sur la manche → tient sur "
        "la manche). BAN éclat de bassine / farine / feuille / botte / "
        "résine / cageot.\n"
        "- **Question moteur :** « Victorina a des lunettes. Que "
        "fait-on ? » expected **pas rire**. accepted `pas rire | on "
        "joue | jouer | pas rire apparence`. retry dump. Non récitée "
        "dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / "
        "graphe inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin "
        "heureuse. `chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Un platane lâche un petit bruit, sec. Sur le bord du bac, un "
        "éclat de platane brille. Sarah veut une étoile **maintenant**, "
        "avec une vraie nervure. Victorina arrive. Un rire commence. "
        "Victorina se tait, recule : non. Sarah ramasse trop vite : la "
        "feuille casse. Sourire parti. Papa s'accroupit. Elle refuse de "
        "foncer. Elles portent la souple. Merci vécu. Deuxième ruse : "
        "emporte-pièce trop vite, rire qui revient, feuille qui glisse. "
        "Elle s'arrête, lit l'éclat. Un éclat de platane tient sur la "
        "manche.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : parc sous les platanes, bac à feuilles, atelier, "
        "pâte, emporte-pièce. ≠ 003-01 botte, ≠ 003-02 résine, ≠ 003-03 "
        "cageot.\n"
        "- Désir : une étoile de pâte avec une vraie feuille, maintenant.\n"
        "- Objet : feuille souple, emporte-pièce, pâte, gilet jaune, "
        "lunettes.\n"
        "- Indice unique : éclat de platane, vu dès l'ouverture, payé "
        "sur la manche. Pas éclat de feuille / bassine / farine.\n"
        "- Urgence douce : Victorina arrive, l'étoile attend, Sarah "
        "accélère.\n"
        "- Imprévu 1 : rire sur les lunettes, Victorina absente au "
        "moment de ramasser, la feuille sèche casse.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« d'accord ».\n"
        "- Imprévu 2 (plus rusé) : emporte-pièce trop vite, rire qui "
        "revient, feuille qui glisse sur le côté.\n"
        "- Résolution : elle refuse de foncer, observe, écoute le "
        "platane, retrouve l'éclat, Victorina reprend le bord.\n"
        "- Retour : étoile sur l'assiette, nervure imprimée, éclat sur "
        "la manche. La fin a failli (la feuille a glissé).\n\n"
        "## Vécu\n\n"
        "Sarah veut l'étoile **maintenant**. Impatience, puis rire qui "
        "commence, sourire de Victorina qui part. Victorina prend son "
        "temps, pose sa limite (non, attends, silence). Papa se baisse, "
        "pose une question, ne récite pas la règle. Elles agissent : "
        "feuille portée, pâte pressée sans se presser. Merci vécu. Fin : "
        "l'éclat du début tient sur la manche.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : L'étoile et la feuille (noyau dump). Relance : Que "
        "fait-on ? expected pas rire.\n"
        "- Lieu du dump (parc puis atelier / petite maison). Platanes, "
        "bac à feuilles, pâte, emporte-pièce. Papa ajouté. Victorina = "
        "copine.\n"
        "- Ouverture inventée (platane, petit bruit sec), pas « Sarah "
        "est au parc », pas le givre du toboggan du dump.\n"
        "- Indice unique : éclat de platane. BAN éclat de bassine / "
        "farine / feuille / botte / résine / cageot. Pas "
        "tache/flèche/marque/symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore molle » du dump.\n"
        "- Leçon non dite : on la voit quand le rire s'arrête, quand "
        "Victorina recule, quand elles portent la feuille. Pas « tu as "
        "des lunettes ». Pas « on ne va pas rire de l'apparence ». Pas "
        "« les lunettes aident / les cheveux sont les cheveux / l'habit "
        "tient chaud ». Pas « on joue » / « vous jouez » hors question.\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Victorina a des lunettes. Que "
        "fait-on ? ». expected pas rire. retry dump. 5 chunks, kinds "
        "inchangés.\n"
        "- example4 011 / 043 / 075 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_cor_003_02.py` (`voice` / `ssml` / "
        "`xai` / `PROFILES`).\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers l'emporte-pièce.\n"
        f"- {nwords} mots. N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
