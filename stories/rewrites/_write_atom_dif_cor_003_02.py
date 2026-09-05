#!/usr/bin/env python3
"""ATOM-DIF.COR.003-02 — Les cinq sauts sous le pin (F-NAR-019, N2, DIF.COR.003)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "ATOM-DIF.COR.003-02"
TITLE = "Les cinq sauts sous le pin"
N2 = LIMITS["N2"]
CHARS = "Victorino, Nina, papa, maman"
SETTING = "parc sous le pin, pomme de pin, résine, écorce"
INDICE = "éclat de résine"
FIL = (
    "Une goutte de résine colle au tronc. Sur l'écorce, un "
    "éclat de résine brille. Victorino veut cinq sauts, "
    "maintenant. Nina arrive. Un rire commence. Nina se tait. "
    "La corde tape l'herbe. Victorino refuse de foncer. Ils "
    "tiennent la corde, à deux. Merci vécu. Un saut trop vite. "
    "L'éclat de résine tient sur l'écorce."
)
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|tout doucement|"
    r"encore|déjà|deja)\b",
    re.I,
)
BAN_WORDS = re.compile(
    r"\b(botte|bottes|limace|perron|chaise|tiroir|fraisier|cuivre|"
    r"buis|coussin|figue|robinet|planche|cerceau|émail|email|"
    r"samare|bassine|entrée|entree)\b",
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
        emphasis="éclat de résine",
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience puis découragement; intensite=2; "
            "destinataire=enfant; sous_texte=il_veut_cinq_sauts_maintenant; "
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
            "sous_texte=on_joue_nina_a_des_lunettes; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="corde",
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=ils_tiennent_la_corde_a_deux; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="éclat de résine",
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
        emphasis="éclat de résine",
        note=(
            "arc=retour; intention=refermer; "
            "emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; "
            "sous_texte=l_eclat_du_debut_tient_sur_l_ecorce; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    "expected_answer": "jouer",
    "accepted_examples": (
        "jouer | on joue | ensemble | sauter | pas rire | les cinq sauts"
    ),
    "retry_prompt": "On joue. Nina a des lunettes. Que fait-on ?",
    "engine_ok_text": "Oui, jouer.",
    "engine_near_text": "Tu es tout près. Reprenons.",
}

SCRIPTS = {
    "CHK_T0000_P0000": (
        "opening",
        "enfants_parc,corde",
        [
            "narrateur|Une goutte de résine colle au tronc.",
            "narrateur|Elle fait un petit fil, chaud et collant.",
            "enfant-m|Ça colle, papa !",
            "papa|Tu la vois, sur l'écorce ?",
            "enfant-m|Oui, un petit fil.",
            "narrateur|Le pin sent la résine, tout près.",
            "narrateur|Sur l'écorce, un éclat de résine brille.",
            "enfant-m|Il brille, maman.",
            "maman|Tu le vois, le petit point ?",
            "enfant-m|Oui, un petit point.",
            "narrateur|Une pomme de pin roule dans l'herbe.",
            "narrateur|Elle fait toc, sec et rond.",
            "enfant-m|J'ai entendu le toc.",
            "papa|La pomme de pin ?",
            "enfant-m|Oui, papa.",
            "maman|L'écorce est rugueuse, sous la main.",
            "enfant-m|Elle pique un peu.",
            "narrateur|Papa décroche la corde de la branche.",
            "narrateur|Le coton est froid, un peu lourd.",
            "maman|Le coton sent la pluie, Victorino ?",
            "enfant-m|Il est mouillé.",
            "narrateur|En ce moment, Victorino tient un bout.",
            "narrateur|Il veut cinq sauts, tout de suite.",
            "enfant-m|Je veux tourner, maintenant !",
            "enfant-m|Nina saute cinq fois.",
            "papa|Cinq fois, sans s'arrêter ?",
            "enfant-m|Oui, papa.",
            "maman|On compte tout haut ?",
            "enfant-m|Oui, tout haut.",
            "narrateur|Nina arrive sur le gravier.",
            "narrateur|Le gravier fait criss-criss, sous ses pas.",
            "narrateur|Nina a des lunettes.",
            "narrateur|Nina a les cheveux tressés.",
            "narrateur|Elle porte un gilet rouge.",
            "papa|Nina, tu sautes au milieu ?",
            "enfant-m|Tu sautes, Nina ?",
            "copine|Oui.",
            "narrateur|Papa tient l'autre bout.",
            "narrateur|Victorino regarde les lunettes, trop longtemps.",
            "narrateur|Un rire commence dans sa bouche.",
            "narrateur|Nina ne dit rien.",
            "narrateur|Le sourire de Nina disparaît.",
            "enfant-m|Tu vas au milieu, maintenant !",
            "narrateur|Nina recule d'un pas.",
            "copine|Non.",
            "enfant-m|Oh.",
            "narrateur|Victorino tourne la corde trop vite, tout seul.",
            "narrateur|La corde tape l'herbe, trop lourde.",
            "narrateur|Ça fait un bruit mou.",
            "narrateur|Un peu de terre colle au coton.",
            "enfant-m|Elle ne monte pas !",
            "copine|Elle est mouillée.",
            "narrateur|L'éclat de résine tremble, puis tient.",
            "narrateur|Le sourire de Victorino disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Ses épaules tombent un peu.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois Nina, Victorino ?",
            "enfant-m|Oui, papa.",
            "maman|Tes mains sont collantes, Victorino ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_Q0001": (
        "clue",
        "",
        [
            "narrateur|Nina a des lunettes.",
            "narrateur|Que fait-on ?",
        ],
    ),
    "CHK_T0000_P0000_C0001": (
        "resolution",
        "corde",
        [
            "narrateur|Victorino veut les cinq sauts, tout de suite.",
            "enfant-m|Je tourne, maintenant !",
            "narrateur|Il avance trop vite vers Nina.",
            "narrateur|Les mots se bousculent dans sa bouche.",
            "copine|Non.",
            "narrateur|Nina reste un peu plus loin.",
            "enfant-m|Oh.",
            "narrateur|Le sourire ne revient pas.",
            "narrateur|Victorino refuse de foncer.",
            "narrateur|Il referme la bouche.",
            "narrateur|Personne ne parle.",
            "narrateur|Il observe la corde, un instant.",
            "narrateur|Il écoute le toc de la pomme de pin.",
            "papa|Tu veux les cinq sauts avec Nina ?",
            "narrateur|Papa reste à la même hauteur.",
            "enfant-m|Tu tiens le bout ?",
            "narrateur|Nina ne dit rien, d'abord.",
            "narrateur|Elle pose les mains sur le coton.",
            "copine|Je le tiens.",
            "enfant-m|D'accord.",
            "papa|Merci, Victorino.",
            "narrateur|Papa a vu les deux, sous le pin.",
            "maman|La résine colle un peu, sous les doigts.",
            "enfant-m|Elle est chaude.",
            "narrateur|Ils essuient la corde sur le tronc.",
            "narrateur|Nina tient le coton, plus près.",
            "narrateur|La corde redevient plus légère, cette fois.",
            "enfant-m|Elle monte !",
            "copine|Oui.",
            "papa|Tu la vois, la corde ?",
            "enfant-m|Oui, papa.",
            "maman|Au milieu, Nina ?",
            "copine|J'y vais.",
            "narrateur|Victorino tourne, sans se presser.",
            "narrateur|Nina suit la corde des yeux.",
            "narrateur|Nina saute une fois.",
            "copine|Un.",
            "enfant-m|Deux.",
            "narrateur|Le ventre de Victorino se desserre.",
            "narrateur|Les épaules se relèvent un peu.",
            "papa|On reste sous le pin ?",
            "enfant-m|Oui.",
            "maman|Tes mains sont au chaud ?",
            "enfant-m|Un peu, maman.",
        ],
    ),
    "CHK_T0000_P0000_END": (
        "action",
        "corde",
        [
            "narrateur|Nina saute, plus vite.",
            "copine|Trois.",
            "enfant-m|Quatre.",
            "narrateur|Le gilet rouge bouge.",
            "narrateur|Les tresses tapent le dos.",
            "narrateur|Les lunettes restent sur le nez.",
            "enfant-m|Cinq, maintenant !",
            "narrateur|Il tourne trop vite, tout de suite.",
            "narrateur|Il regarde les lunettes, trop longtemps.",
            "narrateur|Un rire revient dans sa bouche.",
            "copine|Attends.",
            "narrateur|Nina lâche le milieu.",
            "narrateur|La corde penche vers l'herbe.",
            "enfant-m|Ça tombe !",
            "narrateur|Victorino avance les mains, trop vite.",
            "narrateur|Puis il s'arrête net.",
            "narrateur|Victorino refuse de foncer, cette fois.",
            "narrateur|Ses mains se ferment, puis s'ouvrent.",
            "narrateur|Personne ne dit la suite.",
            "narrateur|Il observe la corde, un instant.",
            "narrateur|Il écoute le toc de la pomme de pin.",
            "narrateur|Sur l'écorce, un éclat de résine luit.",
            "enfant-m|Là, sur l'écorce.",
            "enfant-m|Tu sautes, Nina ?",
            "narrateur|Nina ne dit rien.",
            "narrateur|Elle reprend le milieu, sans parler.",
            "copine|Oui.",
            "narrateur|Victorino tourne, sans se presser.",
            "narrateur|Nina saute.",
            "copine|Cinq !",
            "enfant-m|Cinq !",
            "papa|Tu as tourné sans t'arrêter ?",
            "enfant-m|Oui, papa.",
            "maman|Le gilet est chaud, Nina ?",
            "copine|Un peu.",
            "narrateur|La corde se pose dans l'herbe.",
            "papa|On reverse les rôles ?",
            "copine|À toi le milieu.",
            "narrateur|Nina tourne à son tour.",
            "narrateur|Victorino saute.",
            "narrateur|Ses chaussures font toc.",
            "enfant-m|C'est plus facile.",
            "papa|La corde est sèche ?",
            "enfant-m|Oui, papa.",
            "maman|Un rayon passe entre les aiguilles.",
            "enfant-m|Il allume le gilet.",
        ],
    ),
    "CHK_T0000_P0000_END_F0001": (
        "ending",
        "pin",
        [
            "narrateur|Ils restent sous le pin.",
            "narrateur|Maman essuie un peu de terre.",
            "enfant-m|On a eu les cinq sauts, papa.",
            "papa|Tu les as vus, toi ?",
            "enfant-m|Oui, au milieu.",
            "maman|On est bien, ici.",
            "narrateur|Victorino tapote la corde du doigt.",
            "enfant-m|Elle a une trace de résine.",
            "maman|Tu la vois, la trace ?",
            "enfant-m|Oui, maman.",
            "papa|La corde est restée, Victorino.",
            "enfant-m|Oui, avec Nina.",
            "copine|La corde est restée.",
            "narrateur|Ça sent la résine, un peu tiède.",
            "enfant-m|Et le pin, maman.",
            "maman|Oui, dans l'air.",
            "narrateur|La pomme de pin reste dans l'herbe.",
            "narrateur|Un éclat de résine tient sur l'écorce.",
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
        raise SystemExit(f"{SID}: enfant-f (Victorino = enfant-m, Nina = copine)")
    if "copine|" not in blob:
        raise SystemExit(f"{SID}: Nina absente (copine)")
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
        "l'amitié ne dépend pas",
        "apparence",
        "pas une blague",
    ):
        if lesson in body:
            raise SystemExit(f"{SID}: leçon dite ({lesson})")
    if re.search(r"\b(jouer|joue|jouons|jouez|jouent)\b", body):
        raise SystemExit(f"{SID}: verbe jouer hors question")
    q = by["CHK_T0000_P0000_Q0001"]
    if q["text"] != "Nina a des lunettes. Que fait-on ?":
        raise SystemExit(f"{SID}: question moteur altérée: {q['text']}")
    if q.get("expected_answer") != "jouer":
        raise SystemExit(f"{SID}: expected_answer altéré")
    retry = str(q.get("retry_prompt") or "").lower()
    if "que fait-on" not in retry:
        raise SystemExit(f"{SID}: retry sans Que fait-on")
    if "jouer" not in retry and "on joue" not in retry:
        raise SystemExit(f"{SID}: retry sans jouer")
    copine_txt = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("copine|")
    ).lower()
    if "non" not in copine_txt:
        raise SystemExit(f"{SID}: Nina sans non")
    if "attends" not in copine_txt:
        raise SystemExit(f"{SID}: Nina sans attends")
    if "pomme de pin" not in blob:
        raise SystemExit(f"{SID}: manque pomme de pin")
    if "écorce" not in blob and "ecorce" not in blob:
        raise SystemExit(f"{SID}: manque écorce")
    if "résine" not in blob and "resine" not in blob:
        raise SystemExit(f"{SID}: manque résine")
    for ban in (
        "éclat d'écorce",
        "éclat d'ecorce",
        "éclat de pin",
        "grain de pin",
        "éclat de botte",
        "éclat de limace",
        "éclat de perron",
        "éclat de chaise",
        "éclat de tiroir",
        "éclat de fraisier",
        "éclat de cuivre",
        "éclat de buis",
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
        "- **Leçon :** DIF.COR.003 — Nina a des lunettes "
        "(vécue : rire qui commence, Nina se tait, corde qui tape, "
        "ils tiennent la corde à deux). JAMAIS dite dans le récit.\n"
        "- **Personnages :** Victorino, Nina, papa, maman. Maman ajoutée. "
        "Victorino = enfant-m (propose, trop vite). Nina = copine "
        "(silence, non, attends). Troupe D16. Pas de maîtresse.\n"
        "- **Lieu :** parc sous le pin, pomme de pin, résine, écorce, "
        "corde de coton, gravier, gilet rouge, tresses. ≠ 003-01 "
        "entrée/botte.\n"
        "- **Indice unique :** éclat de résine (brille à l'ouverture → "
        "tremble à la corde → luit au refus → tient sur l'écorce). BAN "
        "grain de pin / éclat d'écorce / éclat de pin / botte / limace / "
        "perron / chaise / tiroir / fraisier / cuivre / buis.\n"
        "- **Question moteur :** « Nina a des lunettes. Que fait-on ? » "
        "expected **jouer**. Non récitée dans les autres chunks.\n"
        "- **Structure conservée :** 5 chunks, `chunk_id` / `kind` / graphe "
        "inchangés\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Une goutte de résine colle au tronc. Sur l'écorce, un "
        "éclat de résine brille. Pomme de pin, toc, coton mouillé. "
        "Victorino veut cinq sauts **maintenant**. Nina arrive. Un rire "
        "commence. Nina se tait, recule : non. Victorino tourne tout "
        "seul : la corde tape. Sourire parti. Papa s'accroupit. Il "
        "refuse de foncer. Ils tiennent la corde. Merci vécu. Deuxième "
        "ruse : cinq trop vite, rire qui revient, Nina lâche. Il "
        "s'arrête, lit l'éclat. Un éclat de résine tient sur l'écorce.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : parc sous le pin, pomme de pin, résine, écorce, "
        "coton froid, gravier. ≠ 003-01 entrée/botte.\n"
        "- Désir : cinq sauts d'affilée, maintenant.\n"
        "- Objet : corde de coton, pomme de pin, gilet rouge, lunettes.\n"
        "- Indice unique : éclat de résine, vu dès l'ouverture, payé "
        "sur l'écorce. Pas grain de pin / éclat d'écorce.\n"
        "- Urgence douce : Nina arrive, les cinq sauts attendent, "
        "Victorino accélère.\n"
        "- Imprévu 1 : rire sur les lunettes, Nina absente au moment "
        "de tourner, la corde tape l'herbe.\n"
        "- Cue : papa à la même hauteur. Un merci vécu, après "
        "« d'accord ».\n"
        "- Imprévu 2 (plus rusé) : cinq trop vite, rire qui revient, "
        "Nina lâche, corde qui penche.\n"
        "- Résolution : il refuse de foncer, observe, écoute le toc, "
        "retrouve l'éclat, Nina reprend le milieu.\n"
        "- Retour : cinq sauts, corde dans l'herbe, éclat sur "
        "l'écorce.\n\n"
        "## Vécu\n\n"
        "Victorino veut les cinq sauts **maintenant**. Impatience, puis "
        "rire qui commence, sourire de Nina qui part. Nina prend son "
        "temps, pose sa limite (non, attends, silence). Papa se baisse, "
        "pose une question, ne récite pas la règle. Ils agissent : "
        "corde tenue, sauts sans se presser. Merci vécu. Fin : l'éclat "
        "du début tient sur l'écorce.\n\n"
        "## Vu et corrigé\n\n"
        "- Titre : Les cinq sauts sous le pin (noyau dump). Relance : "
        "Que fait-on ? expected jouer.\n"
        "- Lieu du dump (parc sous le pin, pomme de pin, résine, "
        "écorce). Maman ajoutée. Nina = copine.\n"
        "- Ouverture inventée (goutte de résine au tronc), pas un "
        "gabarit v2, pas « Une pomme de pin tombe dans l'herbe » du "
        "dump.\n"
        "- Indice unique : éclat de résine. BAN grain de pin / éclat "
        "d'écorce / éclat de pin / botte / limace / perron / chaise / "
        "tiroir / fraisier / cuivre / buis. Pas tache/flèche/marque/"
        "symbole.\n"
        "- Tics encore/déjà/tout doux/tout calme et `aujourd'hui` "
        "retirés. Strip « tout doux » / « encore » du dump.\n"
        "- Leçon non dite : on la voit quand le rire s'arrête, quand "
        "Nina recule, quand ils tiennent la corde. Pas « Nina a des "
        "lunettes, on joue » hors question. Pas « on joue » / "
        "« vous jouez » / « il ne faut pas rire ».\n"
        "- Un « en ce moment ». Un merci vécu. Adulte + question.\n"
        "- Question moteur inchangée : « Nina a des lunettes. Que "
        "fait-on ? ». expected jouer. 5 chunks, kinds inchangés.\n"
        "- example4 009 / 041 / 073 (manière volée, gabarit non collé). "
        "Voix : `_write_atom_dif_cor_002_01.py` (Victorino via Nino) / "
        "`_write_atom_col_eco_002_08.py`.\n"
        "- TTS complet (5) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, "
        "tempo, sourire, respiration). `slow` = question et fin. "
        "Action plus vive vers le cinq.\n"
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
