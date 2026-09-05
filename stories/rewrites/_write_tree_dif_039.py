#!/usr/bin/env python3
"""TREE-DIF-039 — La balle rouge de Victorino, jusqu'au portail (F-NAR-019, N2, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-039"
N2 = LIMITS["N2"]
TITLE = "La balle rouge de Victorino, jusqu'au portail"
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà|deja)\b", re.I)
BAD_INDICE = (
    "ancre",
    "étoile brune",
    "fil pâle",
    "croissant d'eau",
    "croissant pâle",
    "virgule farine",
    "bouton nacre",
    "nœud raphia",
    "pois ivoire",
    "grain savon rose",
    "grain vanille",
    "pastille colle",
    "virgule buée",
    "capuchon penche",
    "grain doré",
    "brin safran",
    "anneau liège",
    "clou tête ronde",
    "grain d'ambre",
    "goutte de cire rouge",
    "anneau de zinc",
    "larme de bronze",
    "point de cire",
    "bracelet d'écorce",
    "boucle d'étain",
    "anneau de pollen",
    "dent de laitue",
    "éclat de zinc",
    "éclat de thym",
    "lune d'étain",
    "grain de grenat",
    "grain d'indigo",
    "grain de brique",
    "éclat vert",
    "écaille d'étain",
    "vis verte",
    "cristal de sucre brun",
    "écaille de lichen",
    "grain de cire claire",
    "dent de fermeture dorée",
    "écaille de nacre",
    "grain de paprika",
    "écaille de boue blonde",
    "point de rouille",
    "grain de mica",
    "grain de cannelle",
    "grain d'ocre",
    "grain de feutre",
    "grain de sésame",
    "écaille de savon",
    "grain de suie",
    "grain de limon",
    "grain de quartz",
    "grain de sel",
    "grain de lessive",
    "grain de cerise",
    "rond d'huile",
    "écaille d'orange",
    "point d'écume",
    "grain de sève",
    "point de beurre",
    "grain de craie",
    "grain de pomme",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="balle rouge",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le grain de bitume veut aller jusqu'au portail; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change la suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="balle",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde ce qu'il tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="portail",
        note="arc=confirmation; intention=relancer; emotion=élan; intensite=1; destinataire=enfant; sous_texte=les trois affaires partent; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il veut tout brûler d'un coup; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=la première idée rate, Aniss ne veut pas la même chose; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grain de bitume",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=il a dosé son élan, Aniss a pris son temps; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="portail",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la balle a touché le portail; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    run = 1
    prev = ""
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
        if role == "narrateur":
            tok = ph.split()[0].lower()
            if tok == prev:
                run += 1
                if run >= 4:
                    raise SystemExit(f"puces « {tok} »: {ph}")
            else:
                run = 1
                prev = tok
        else:
            run = 1
            prev = ""
        out.append(f"{role}|{ph}")
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
        f"{body}</prosody><break time=\"{m['pause']}ms\"/></speak>"
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
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if "note" in extra:
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
    out["night_policy"] = "play"
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.items():
        if k in ("emphasis", "note", "pause_before_ms"):
            continue
        out[k] = v
    return out


def ending_note(a: int, b: int, c: int) -> str:
    times = {1: "posé", 2: "lent", 3: "ample"}
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=la_balle_a_touché_le_portail; "
        f"tempo={times[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


OPENING = vet(
    [
        "narrateur|La fermeture du sac à pois se coince.",
        "enfant-m|Elle refuse, papa.",
        "narrateur|Victorino tire, trop fort.",
        "narrateur|La balle rouge roule sur le trottoir chaud.",
        "narrateur|Elle s'arrête contre un grain de bitume.",
        "enfant-m|Il est collé, là.",
        "papa|Tu le vois, ce grain noir ?",
        "maman|Ça sent le goudron, sous le soleil.",
        "copain|On court, maintenant !",
        "enfant-m|On rebondit jusqu'au portail.",
        "narrateur|En ce moment, Victorino ramasse la balle rouge.",
        "narrateur|Il la lance d'un coup, trop loin.",
        "narrateur|La balle tape, puis revient de travers.",
        "narrateur|Le grain de bitume penche, presque parti.",
        "narrateur|Son sourire s'en va.",
        "narrateur|L'envie et l'inquiétude se poussent, dans la poitrine.",
        "papa|La balle a trop sauté, là ?",
        "narrateur|Papa s'accroupit, à la même hauteur.",
        "papa|Merci, tu as vu le grain.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|Trois affaires attendent près des chaussures.",
        "narrateur|La balle rouge, le sac à pois, et la gourde bleue.",
        "maman|Tu prends quoi d'abord, Victorino ?",
    ]
)

T1 = {
    1: dict(
        lab="la balle rouge",
        ans="ventre",
        acc="ventre | le ventre | contre le ventre | son ventre",
        retry="La balle est contre le ventre.",
        sons="caoutchouc,goudron",
        emp="balle rouge",
        passage=vet(
            [
                "narrateur|Victorino prend la balle rouge, le grain de bitume dessus.",
                "enfant-m|Toi, tu vas jusqu'au portail.",
                "narrateur|Il la serre trop fort, trop vite.",
                "narrateur|Le caoutchouc claque, le grain penche.",
                "maman|Tiens-la contre le ventre, près de toi.",
                "narrateur|Victorino baisse la balle, les joues chaudes.",
                "papa|Le sac à pois vient avec nous.",
                "narrateur|Maman glisse la gourde bleue contre sa hanche.",
                "copain|Moi je cours, moi !",
                "enfant-m|Les trois, jusqu'au portail.",
                "narrateur|Aniss se tait, un pied en l'air.",
                "papa|La balle est à toi.",
                "maman|Le sac et la gourde viennent aussi.",
            ]
        ),
        question=vet(
            [
                "narrateur|Victorino a mis la balle rouge.",
                "maman|Elle est où, maintenant ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-m|Contre le ventre.",
                "maman|Oui, tout près.",
                "narrateur|Le caoutchouc chauffe, un peu.",
                "copain|Elle est trop rouge !",
                "enfant-m|C'est pour le portail.",
                "narrateur|Aniss a les genoux plus bas que Victorino.",
                "narrateur|Ses pieds n'arrêtent pas de bouger.",
                "papa|On reste sur le chemin ?",
                "enfant-m|Oui, papa.",
                "narrateur|Le grain de bitume tient, collé au rouge.",
                "maman|On avance, tous les quatre.",
            ]
        ),
    ),
    2: dict(
        lab="le sac à pois",
        ans="dos",
        acc="dos | le dos | sur le dos | son dos",
        retry="Le sac est sur le dos.",
        sons="tissu,pois",
        emp="sac à pois",
        passage=vet(
            [
                "narrateur|Victorino passe d'abord le sac à pois.",
                "enfant-m|Il gratte un peu, aux épaules.",
                "papa|Mets-le, le chemin est long.",
                "narrateur|Les pois font une ombre ronde.",
                "maman|La balle, ensuite, près de toi.",
                "narrateur|Il glisse la gourde d'une main.",
                "copain|Le sac, je le prends, moi !",
                "enfant-m|Non, on le garde pour le portail.",
                "narrateur|Aniss ouvre la bouche, puis se tait.",
                "narrateur|Un manteau trop court apparaît au seuil.",
                "papa|Le sac est prêt.",
                "maman|La balle et la gourde viennent aussi.",
            ]
        ),
        question=vet(
            [
                "narrateur|Victorino a passé le sac à pois.",
                "papa|Il est où, maintenant ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-m|Sur le dos.",
                "papa|Oui.",
                "narrateur|Les pois tapent un peu sa hanche.",
                "copain|Je vois les pois !",
                "enfant-m|On le garde pour le portail.",
                "narrateur|Aniss a les cheveux tout courts.",
                "narrateur|Une mèche saute quand il respire.",
                "maman|Ça sent le trottoir chaud.",
                "papa|Tes mains, sur le sac ?",
                "copain|Oui, papa.",
                "narrateur|Le grain de bitume reste visible, sur la balle.",
            ]
        ),
    ),
    3: dict(
        lab="la gourde bleue",
        ans="main",
        acc="main | la main | à la main | sa main",
        retry="La gourde est à la main.",
        sons="plastique,eau",
        emp="gourde bleue",
        passage=vet(
            [
                "narrateur|Victorino prend d'abord la gourde bleue.",
                "enfant-m|Elle est froide, contre la paume.",
                "maman|Garde-la à la main, tout droit.",
                "narrateur|Le plastique sent l'eau du robinet.",
                "papa|La balle et le sac, avec toi.",
                "narrateur|Il les pose près des chaussures.",
                "copain|Vite, on court !",
                "enfant-m|Je te garde la balle.",
                "narrateur|Des genoux trop petits arrivent en sautant.",
                "narrateur|Aniss s'arrête, sans un mot.",
                "papa|La gourde est prise.",
                "maman|La balle et le sac viennent aussi.",
            ]
        ),
        question=vet(
            [
                "narrateur|Victorino a pris la gourde bleue.",
                "maman|Elle est où, maintenant ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-m|À la main.",
                "maman|Oui.",
                "narrateur|La gourde bleue avance, un pas après l'autre.",
                "copain|Ça sent l'eau.",
                "enfant-m|Le départ est là.",
                "narrateur|Le manteau d'Aniss s'arrête trop haut.",
                "narrateur|Les manches laissent ses poignets libres.",
                "maman|Le chemin est tiède, devant.",
                "papa|On y va, tous les quatre ?",
                "enfant-m|Oui.",
                "narrateur|Le grain de bitume tient, sur la balle rouge.",
            ]
        ),
    ),
}

T2_CHOICE = {
    1: vet(
        [
            "narrateur|La balle tape le ventre, trop légère.",
            "narrateur|La flaque brille, un peu trop large.",
            "narrateur|Le banc du tilleul fait une ombre.",
            "narrateur|Le muret garde le portail, tout près.",
            "papa|On le rejoint où, Victorino ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Le sac à pois pèse à l'épaule, trop vif.",
            "narrateur|La flaque brille, un peu trop large.",
            "narrateur|Le banc du tilleul fait une ombre.",
            "narrateur|Le muret garde le portail, tout près.",
            "maman|On le rejoint où, Victorino ?",
        ]
    ),
    3: vet(
        [
            "narrateur|La gourde frappe la paume, trop ronde.",
            "narrateur|La flaque brille, un peu trop large.",
            "narrateur|Le banc du tilleul fait une ombre.",
            "narrateur|Le muret garde le portail, tout près.",
            "papa|On le rejoint où, Victorino ?",
        ]
    ),
}

T2 = {
    (1, 1): dict(
        sons="eau,rebond",
        emp="flaque",
        lines=vet(
            [
                "narrateur|La balle rouge avance vers la flaque.",
                "copain|Moi je saute, tout de suite !",
                "enfant-m|On rebondit, Aniss.",
                "narrateur|Victorino lance trop fort, d'un coup.",
                "narrateur|La balle tape l'eau, trop large.",
                "narrateur|Le grain de bitume penche, mouillé.",
                "enfant-m|Oh.",
                "narrateur|Son sourire n'est plus là.",
                "narrateur|Ça serre, juste sous la gorge.",
                "copain|On saute tous les ronds !",
                "narrateur|Aniss se tait, les pieds dans l'eau.",
                "narrateur|Le silence pèse, plus fort qu'un mot.",
                "papa|Je me baisse, près de l'eau.",
                "enfant-m|Je ne fonce pas.",
                "papa|Vous faites comment, tous les deux ?",
            ]
        ),
    ),
    (1, 2): dict(
        sons="bois,rebond",
        emp="banc",
        lines=vet(
            [
                "narrateur|La balle rouge s'arrête sous le tilleul.",
                "enfant-m|Le banc est à nous, Aniss.",
                "copain|Je vais jusqu'au bout, trop vite !",
                "narrateur|Victorino lance, trop fort, sur le bois.",
                "narrateur|La balle file sous le banc, toute seule.",
                "narrateur|Le bois penche, comme une pente.",
                "enfant-m|Elle part !",
                "narrateur|Son sourire s'en va.",
                "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
                "copain|On court le banc entier !",
                "narrateur|Aniss se tait, un pied sur le bois.",
                "maman|Je m'accroupis, à votre hauteur.",
                "enfant-m|Je reste.",
                "papa|Vous trouvez, tous les deux ?",
            ]
        ),
    ),
    (1, 3): dict(
        sons="pierre,rebond",
        emp="muret",
        lines=vet(
            [
                "narrateur|La balle rouge pose son ombre sur le muret.",
                "enfant-m|Ici, ça mène au portail, Aniss.",
                "copain|Je vais plus loin, moi !",
                "narrateur|Victorino jette trop fort, contre la pierre.",
                "narrateur|La balle revient de travers, trop loin.",
                "narrateur|Le trottoir penche, vers la rue.",
                "enfant-m|Elle va partir !",
                "narrateur|Son sourire n'est plus là.",
                "narrateur|Ça serre, sous les côtes.",
                "narrateur|Aniss ne dit rien, les poings fermés.",
                "narrateur|Le silence répond, plus net qu'un cri.",
                "papa|Je me baisse, face au mur.",
                "enfant-m|Je ne fonce pas.",
                "papa|Vous trouvez comment, alors ?",
            ]
        ),
    ),
    (2, 1): dict(
        sons="eau,tissu",
        emp="flaque",
        lines=vet(
            [
                "narrateur|Le sac à pois penche vers la flaque.",
                "copain|Moi je saute, Victorino !",
                "enfant-m|Le sac d'abord, Aniss.",
                "narrateur|Victorino se penche trop vite, d'un coup.",
                "narrateur|Les pois du sac se mouillent, tout bas.",
                "narrateur|Le grain de bitume glisse, sur la balle.",
                "enfant-m|Les pois !",
                "narrateur|Son sourire tombe.",
                "narrateur|Ça serre, juste sous la gorge.",
                "copain|On éclabousse tout !",
                "narrateur|Aniss se tait, les pieds dans l'eau.",
                "narrateur|Le silence pèse, plus fort qu'un mot.",
                "maman|Je me baisse, près de l'eau.",
                "enfant-m|Je ne fonce pas.",
                "papa|Vous faites comment, tous les deux ?",
            ]
        ),
    ),
    (2, 2): dict(
        sons="bois,tissu",
        emp="banc",
        lines=vet(
            [
                "narrateur|Le sac à pois glisse sous le tilleul.",
                "enfant-m|Le banc est à nous, Aniss.",
                "copain|Je vais jusqu'au bout, trop vite !",
                "narrateur|Aniss rebondit trop haut, sur le bois.",
                "narrateur|Le sac penche, puis tape le pied du banc.",
                "narrateur|Le bois penche, comme une pente.",
                "enfant-m|Le sac part !",
                "narrateur|Son sourire s'en va.",
                "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
                "copain|On court le banc entier !",
                "narrateur|Aniss se tait, un pied sur le bois.",
                "papa|Je m'accroupis, à votre hauteur.",
                "enfant-m|Je reste.",
                "maman|Vous trouvez, tous les deux ?",
            ]
        ),
    ),
    (2, 3): dict(
        sons="pierre,tissu",
        emp="muret",
        lines=vet(
            [
                "narrateur|Le sac à pois s'appuie contre le muret.",
                "enfant-m|Ici, ça mène au portail, Aniss.",
                "copain|Je vais plus loin, moi !",
                "narrateur|Aniss court après le sac, trop loin.",
                "narrateur|La sangle lâche, puis se rattrape.",
                "narrateur|Le trottoir penche, vers la rue.",
                "enfant-m|Stop !",
                "narrateur|Son sourire n'est plus là.",
                "narrateur|Ça serre, sous les côtes.",
                "narrateur|Aniss ne dit rien, les poings fermés.",
                "narrateur|Le silence répond, plus net qu'un cri.",
                "maman|Je me baisse, face au mur.",
                "enfant-m|Je ne fonce pas.",
                "papa|Vous trouvez comment, alors ?",
            ]
        ),
    ),
    (3, 1): dict(
        sons="eau,plastique",
        emp="flaque",
        lines=vet(
            [
                "narrateur|La gourde bleue avance vers la flaque.",
                "copain|Moi je saute, Victorino !",
                "enfant-m|La gourde d'abord, Aniss.",
                "narrateur|Victorino penche trop, d'un coup.",
                "narrateur|La gourde tape l'eau, un petit choc.",
                "narrateur|Le grain de bitume penche, mouillé.",
                "enfant-m|Elle a bu trop vite.",
                "narrateur|Son sourire n'est plus là.",
                "narrateur|Ça serre, juste sous la gorge.",
                "copain|On la plonge toute !",
                "narrateur|Aniss se tait, les pieds dans l'eau.",
                "narrateur|Le silence pèse, plus fort qu'un mot.",
                "papa|Je me baisse, près de l'eau.",
                "enfant-m|Je ne fonce pas.",
                "papa|Vous faites comment, tous les deux ?",
            ]
        ),
    ),
    (3, 2): dict(
        sons="bois,plastique",
        emp="banc",
        lines=vet(
            [
                "narrateur|La gourde bleue bute sous le tilleul.",
                "enfant-m|Le banc est à nous, Aniss.",
                "copain|Je vais jusqu'au bout, trop vite !",
                "narrateur|Aniss saute par-dessus la gourde, sans s'arrêter.",
                "narrateur|Le plastique roule, trop loin.",
                "narrateur|Le bois penche, comme une pente.",
                "enfant-m|Elle part !",
                "narrateur|Son sourire s'en va.",
                "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
                "copain|On court le banc entier !",
                "narrateur|Aniss se tait, un pied sur le bois.",
                "maman|Je m'accroupis, à votre hauteur.",
                "enfant-m|Je reste.",
                "papa|Vous trouvez, tous les deux ?",
            ]
        ),
    ),
    (3, 3): dict(
        sons="pierre,plastique",
        emp="muret",
        lines=vet(
            [
                "narrateur|La gourde bleue s'arrête près du muret.",
                "enfant-m|Ici, ça mène au portail, Aniss.",
                "copain|Je vais plus loin, moi !",
                "narrateur|Aniss court, la gourde reste contre la pierre.",
                "narrateur|Le plastique attend au bord, un peu seul.",
                "narrateur|Le trottoir penche, vers la rue.",
                "enfant-m|Reviens !",
                "narrateur|Son sourire n'est plus là.",
                "narrateur|Ça serre, sous les côtes.",
                "narrateur|Aniss ne dit rien, les poings fermés.",
                "narrateur|Le silence répond, plus net qu'un cri.",
                "papa|Je me baisse, face au mur.",
                "enfant-m|Je ne fonce pas.",
                "papa|Vous trouvez comment, alors ?",
            ]
        ),
    ),
}

T3_LABS = {
    1: ("jouer dans l'eau", "attendre la goutte", "la main de papa"),
    2: ("sauter ensemble", "attendre le tour", "le goûter de maman"),
    3: ("le relais de balles", "attendre le portail", "le rythme de papa"),
}

T3_Q = {
    1: vet(
        [
            "narrateur|Aniss tape l'eau, trop fort.",
            "narrateur|Victorino pose une main, sans lancer.",
            "papa|Dans l'eau, la goutte, ou ma main ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Aniss rebondit sur le banc, trop vite.",
            "narrateur|Victorino pose une main sur le bois, sans sauter.",
            "maman|Ensemble, le tour, ou le goûter ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Aniss court le long du muret, trop loin.",
            "narrateur|Victorino pose une main sur la pierre, sans jeter.",
            "papa|Le relais, le portail, ou mon rythme ?",
        ]
    ),
}


def res(a: int, b: int, c: int) -> list[str]:
    table = {
        (1, 1, 1): [
            "enfant-m|On joue dans l'eau, sans tout sauter.",
            "narrateur|Victorino regarde la balle, sans bouger.",
            "narrateur|Le grain de bitume tient, collé, comme au départ.",
            "enfant-m|Je le reconnais.",
            "narrateur|Aniss se tait, puis pose un pied.",
            "copain|Toi tu rebondis, moi je saute après.",
            "narrateur|Un rond, puis l'autre, plus petit.",
            "narrateur|Victorino refuse de foncer.",
            "enfant-m|Un rebond, pas tous.",
            "papa|Vous jouez, chacun son tour.",
            "maman|La flaque vous a gardés.",
            "narrateur|Le grain de bitume luit, un peu mouillé.",
        ],
        (1, 1, 2): [
            "enfant-m|On attend la goutte.",
            "copain|Je m'arrête, alors.",
            "narrateur|Aniss pose les genoux au bord.",
            "narrateur|La balle rouge attend près de l'eau.",
            "narrateur|Victorino observe le grain de bitume, sans lancer.",
            "enfant-m|Quand la goutte tombe, on rebondit.",
            "narrateur|Une goutte se détache, puis se tait.",
            "copain|Maintenant, avec toi.",
            "narrateur|Personne n'a dit le geste.",
            "papa|Vous avez laissé l'eau s'asseoir.",
            "maman|La flaque vous a gardés.",
            "narrateur|Le grain de bitume reste, collé au rouge.",
        ],
        (1, 1, 3): [
            "enfant-m|Papa, tu tiens Aniss ?",
            "papa|Je donne la main, un pas chacun.",
            "narrateur|Papa pose la balle près de sa main.",
            "narrateur|Aniss pose un pied, puis l'autre.",
            "narrateur|Victorino rebondit, juste à côté.",
            "narrateur|Le grain de bitume luit, entre les doigts.",
            "enfant-m|Je le vois, comme tout à l'heure.",
            "copain|On demande, et ça va.",
            "enfant-m|La flaque est à nous.",
            "maman|Vous avez demandé, sans crier.",
            "papa|Ma main a juste attendu.",
            "narrateur|Le grain de bitume tient, au creux.",
        ],
        (1, 2, 1): [
            "enfant-m|On saute ensemble, un, puis deux.",
            "copain|Toi derrière, moi devant.",
            "narrateur|Victorino garde la balle, Aniss saute devant.",
            "narrateur|Deux ombres passent sur le même banc.",
            "narrateur|Aniss va plus vite, Victorino plus loin.",
            "narrateur|Le grain de bitume tient, sur le rouge.",
            "enfant-m|On arrive au bout, tous les deux.",
            "copain|J'ai attendu ta jambe, un peu.",
            "narrateur|Victorino refuse de foncer.",
            "papa|Vous avez joué avec l'élan.",
            "maman|Le banc vous a laissés passer.",
            "narrateur|Le grain de bitume luit, au creux du bois.",
        ],
        (1, 2, 2): [
            "enfant-m|J'attends le tour.",
            "copain|Moi je finis, puis c'est toi.",
            "narrateur|Victorino tient la balle, sur le bois.",
            "narrateur|Aniss saute jusqu'au bout, tout seul d'abord.",
            "narrateur|Il souffle, puis il recule.",
            "copain|C'est à toi, Victorino.",
            "narrateur|Le grain de bitume attend, collé.",
            "enfant-m|Je le vois, je rebondis.",
            "narrateur|Personne n'a crié la suite.",
            "papa|Chacun son tour, sur le banc.",
            "maman|L'élan a attendu la place.",
            "narrateur|Le grain de bitume reste, sur le rouge.",
        ],
        (1, 2, 3): [
            "enfant-m|Maman, tu ouvres le goûter ?",
            "maman|Un morceau chacun, sans te presser.",
            "narrateur|Maman pose le pain près de la balle.",
            "narrateur|Aniss mâche, et ses pieds se posent.",
            "narrateur|Victorino mâche, la balle au calme.",
            "narrateur|Le grain de bitume luit, contre la mie.",
            "copain|On rebondit après, d'accord ?",
            "enfant-m|Après le goûter, oui.",
            "narrateur|Victorino refuse de lancer d'un coup.",
            "papa|Vous avez demandé, et ça marche.",
            "maman|Le pain a tenu l'élan.",
            "narrateur|Le grain de bitume tient, au bord du pain.",
        ],
        (1, 3, 1): [
            "enfant-m|On fait un relais de balles.",
            "copain|Je te la passe, tu me la rends.",
            "narrateur|La balle rouge voyage d'une main à l'autre.",
            "narrateur|Ils avancent le long du muret, l'un après l'autre.",
            "enfant-m|Un rebond, pas tous.",
            "narrateur|Le grain de bitume tient, à chaque passe.",
            "copain|Le portail est tout près.",
            "narrateur|Victorino refuse de foncer.",
            "papa|Vous jouez avec l'élan, ensemble.",
            "maman|Le muret est devenu une voie.",
            "enfant-m|Je la reconnais, le grain est là.",
            "narrateur|La balle a fait le tour, sans se taire.",
        ],
        (1, 3, 2): [
            "enfant-m|On attend le portail.",
            "copain|Quand il s'ouvre, je rebondis.",
            "narrateur|Un pas, puis le battant reste fermé.",
            "narrateur|La balle rouge reste muette, au creux.",
            "narrateur|Victorino observe le grain de bitume, sans jeter.",
            "narrateur|Le battant bouge, enfin.",
            "copain|Maintenant !",
            "enfant-m|À toi, puis à moi.",
            "narrateur|Personne n'a poussé le fer.",
            "papa|Vous avez laissé le battant s'ouvrir.",
            "maman|L'élan a attendu le seuil.",
            "narrateur|Le grain de bitume luit, face au fer.",
        ],
        (1, 3, 3): [
            "enfant-m|Papa, tu frappes le rythme ?",
            "papa|Tape, tape, et tu rebondis.",
            "narrateur|Aniss écoute les mains, plus que ses pieds.",
            "narrateur|Victorino lève la balle quand papa frappe.",
            "copain|Je saute sur tes mains.",
            "enfant-m|Moi aussi, j'écoute.",
            "narrateur|Le grain de bitume penche, à chaque clap.",
            "narrateur|Le muret se range derrière les claps.",
            "narrateur|Victorino refuse de lancer hors rythme.",
            "papa|Vous avez demandé le rythme.",
            "maman|Ses mains ont tenu l'élan.",
            "narrateur|Le grain de bitume tient, au creux du rouge.",
        ],
        (2, 1, 1): [
            "enfant-m|On joue dans l'eau, sans tout sauter.",
            "narrateur|Victorino regarde le sac, sans se pencher.",
            "narrateur|Le grain de bitume tient, collé à la balle.",
            "enfant-m|Je le reconnais.",
            "narrateur|Aniss se tait, puis pose un pied.",
            "copain|Toi tu tiens le sac, moi je saute après.",
            "narrateur|Un rond, puis l'autre, plus petit.",
            "narrateur|Victorino refuse de foncer.",
            "enfant-m|Un pois mouillé, pas tous.",
            "papa|Vous jouez, chacun son tour.",
            "maman|La flaque vous a gardés.",
            "narrateur|Les pois gardent une perle, près du grain.",
        ],
        (2, 1, 2): [
            "enfant-m|On attend la goutte.",
            "copain|Je m'arrête, alors.",
            "narrateur|Aniss pose les genoux au bord.",
            "narrateur|Le sac à pois attend près de l'eau.",
            "narrateur|Victorino observe le grain de bitume, sans pencher.",
            "enfant-m|Quand la goutte tombe, on avance.",
            "narrateur|Une goutte se détache, puis se tait.",
            "copain|Maintenant, avec toi.",
            "narrateur|Personne n'a dit le geste.",
            "papa|Vous avez laissé l'eau s'asseoir.",
            "maman|La flaque vous a gardés.",
            "narrateur|Le grain de bitume reste, contre un pois.",
        ],
        (2, 1, 3): [
            "enfant-m|Papa, tu tiens Aniss ?",
            "papa|Je donne la main, un pas chacun.",
            "narrateur|Papa pose le sac près de sa main.",
            "narrateur|Aniss pose un pied, puis l'autre.",
            "narrateur|Victorino avance, le sac contre lui.",
            "narrateur|Le grain de bitume luit, entre les pois.",
            "enfant-m|Je le vois, comme tout à l'heure.",
            "copain|On demande, et ça va.",
            "enfant-m|La flaque est à nous.",
            "maman|Vous avez demandé, sans crier.",
            "papa|Ma main a juste attendu.",
            "narrateur|Le grain de bitume tient, au creux du sac.",
        ],
        (2, 2, 1): [
            "enfant-m|On saute ensemble, un, puis deux.",
            "copain|Toi derrière, moi devant.",
            "narrateur|Victorino garde le sac, Aniss saute devant.",
            "narrateur|Deux ombres passent sur le même banc.",
            "narrateur|Aniss va plus vite, Victorino plus loin.",
            "narrateur|Le grain de bitume tient, contre un pois.",
            "enfant-m|On arrive au bout, tous les deux.",
            "copain|J'ai attendu ta jambe, un peu.",
            "narrateur|Victorino refuse de foncer.",
            "papa|Vous avez joué avec l'élan.",
            "maman|Le banc vous a laissés passer.",
            "narrateur|Le sac pose son ombre ronde, sur le bois.",
        ],
        (2, 2, 2): [
            "enfant-m|J'attends le tour.",
            "copain|Moi je finis, puis c'est toi.",
            "narrateur|Victorino tient le sac, sur le bois.",
            "narrateur|Aniss saute jusqu'au bout, tout seul d'abord.",
            "narrateur|Il souffle, puis il recule.",
            "copain|C'est à toi, Victorino.",
            "narrateur|Le grain de bitume attend, collé.",
            "enfant-m|Je le vois, j'avance.",
            "narrateur|Personne n'a crié la suite.",
            "papa|Chacun son tour, sur le banc.",
            "maman|L'élan a attendu la place.",
            "narrateur|Un pois du sac tient le grain, au calme.",
        ],
        (2, 2, 3): [
            "enfant-m|Maman, tu ouvres le goûter ?",
            "maman|Un morceau chacun, sans te presser.",
            "narrateur|Maman pose le pain dans le sac.",
            "narrateur|Aniss mâche, et ses pieds se posent.",
            "narrateur|Victorino mâche, le sac au calme.",
            "narrateur|Le grain de bitume luit, contre la mie.",
            "copain|On rebondit après, d'accord ?",
            "enfant-m|Après le goûter, oui.",
            "narrateur|Victorino refuse de courir d'un coup.",
            "papa|Vous avez demandé, et ça marche.",
            "maman|Le pain a tenu l'élan.",
            "narrateur|Un pois garde une mie, près du grain.",
        ],
        (2, 3, 1): [
            "enfant-m|On fait un relais de balles.",
            "copain|Je te passe le sac, tu me le rends.",
            "narrateur|Le sac à pois voyage d'une épaule à l'autre.",
            "narrateur|Ils avancent le long du muret, l'un après l'autre.",
            "enfant-m|Une passe, pas toutes.",
            "narrateur|Le grain de bitume tient, à chaque passe.",
            "copain|Le portail est tout près.",
            "narrateur|Victorino refuse de foncer.",
            "papa|Vous jouez avec l'élan, ensemble.",
            "maman|Le muret est devenu une voie.",
            "enfant-m|Je le reconnais, le grain est là.",
            "narrateur|Le sac a fait le tour, sans se taire.",
        ],
        (2, 3, 2): [
            "enfant-m|On attend le portail.",
            "copain|Quand il s'ouvre, je rebondis.",
            "narrateur|Un pas, puis le battant reste fermé.",
            "narrateur|Le sac à pois reste muet, au creux.",
            "narrateur|Victorino observe le grain de bitume, sans courir.",
            "narrateur|Le battant bouge, enfin.",
            "copain|Maintenant !",
            "enfant-m|À toi, puis à moi.",
            "narrateur|Personne n'a poussé le fer.",
            "papa|Vous avez laissé le battant s'ouvrir.",
            "maman|L'élan a attendu le seuil.",
            "narrateur|Le grain de bitume luit, dans un pois.",
        ],
        (2, 3, 3): [
            "enfant-m|Papa, tu frappes le rythme ?",
            "papa|Tape, tape, et tu rebondis.",
            "narrateur|Aniss écoute les mains, plus que ses pieds.",
            "narrateur|Victorino lève le sac quand papa frappe.",
            "copain|Je saute sur tes mains.",
            "enfant-m|Moi aussi, j'écoute.",
            "narrateur|Le grain de bitume penche, à chaque clap.",
            "narrateur|Le muret se range derrière les claps.",
            "narrateur|Victorino refuse de courir hors rythme.",
            "papa|Vous avez demandé le rythme.",
            "maman|Ses mains ont tenu l'élan.",
            "narrateur|Un pois du sac tient le grain, au creux.",
        ],
        (3, 1, 1): [
            "enfant-m|On joue dans l'eau, sans tout sauter.",
            "narrateur|Victorino regarde la gourde, sans la plonger.",
            "narrateur|Le grain de bitume tient, collé à la balle.",
            "enfant-m|Je le reconnais.",
            "narrateur|Aniss se tait, puis pose un pied.",
            "copain|Toi tu tiens la gourde, moi je saute après.",
            "narrateur|Un rond, puis l'autre, plus petit.",
            "narrateur|Victorino refuse de foncer.",
            "enfant-m|Une gorgée, pas toute l'eau.",
            "papa|Vous jouez, chacun son tour.",
            "maman|La flaque vous a gardés.",
            "narrateur|La gourde bleue garde une perle, près du grain.",
        ],
        (3, 1, 2): [
            "enfant-m|On attend la goutte.",
            "copain|Je m'arrête, alors.",
            "narrateur|Aniss pose les genoux au bord.",
            "narrateur|La gourde bleue attend près de l'eau.",
            "narrateur|Victorino observe le grain de bitume, sans plonger.",
            "enfant-m|Quand la goutte tombe, on boit.",
            "narrateur|Une goutte se détache, puis se tait.",
            "copain|Maintenant, avec toi.",
            "narrateur|Personne n'a dit le geste.",
            "papa|Vous avez laissé l'eau s'asseoir.",
            "maman|La flaque vous a gardés.",
            "narrateur|Le grain de bitume reste, au bouchon.",
        ],
        (3, 1, 3): [
            "enfant-m|Papa, tu tiens Aniss ?",
            "papa|Je donne la main, un pas chacun.",
            "narrateur|Papa pose la gourde près de sa main.",
            "narrateur|Aniss pose un pied, puis l'autre.",
            "narrateur|Victorino avance, la gourde à la paume.",
            "narrateur|Le grain de bitume luit, au bouchon.",
            "enfant-m|Je le vois, comme tout à l'heure.",
            "copain|On demande, et ça va.",
            "enfant-m|La flaque est à nous.",
            "maman|Vous avez demandé, sans crier.",
            "papa|Ma main a juste attendu.",
            "narrateur|Le grain de bitume tient, contre le bleu.",
        ],
        (3, 2, 1): [
            "enfant-m|On saute ensemble, un, puis deux.",
            "copain|Toi derrière, moi devant.",
            "narrateur|Victorino garde la gourde, Aniss saute devant.",
            "narrateur|Deux ombres passent sur le même banc.",
            "narrateur|Aniss va plus vite, Victorino plus loin.",
            "narrateur|Le grain de bitume tient, au bouchon.",
            "enfant-m|On arrive au bout, tous les deux.",
            "copain|J'ai attendu ta jambe, un peu.",
            "narrateur|Victorino refuse de foncer.",
            "papa|Vous avez joué avec l'élan.",
            "maman|Le banc vous a laissés passer.",
            "narrateur|La gourde pose son ombre bleue, sur le bois.",
        ],
        (3, 2, 2): [
            "enfant-m|J'attends le tour.",
            "copain|Moi je finis, puis c'est toi.",
            "narrateur|Victorino tient la gourde, sur le bois.",
            "narrateur|Aniss saute jusqu'au bout, tout seul d'abord.",
            "narrateur|Il souffle, puis il recule.",
            "copain|C'est à toi, Victorino.",
            "narrateur|Le grain de bitume attend, collé.",
            "enfant-m|Je le vois, j'avance.",
            "narrateur|Personne n'a crié la suite.",
            "papa|Chacun son tour, sur le banc.",
            "maman|L'élan a attendu la place.",
            "narrateur|Le plastique tiède tient le grain, au creux.",
        ],
        (3, 2, 3): [
            "enfant-m|Maman, tu ouvres le goûter ?",
            "maman|Un morceau chacun, sans te presser.",
            "narrateur|Maman pose le pain près de la gourde.",
            "narrateur|Aniss mâche, et ses pieds se posent.",
            "narrateur|Victorino mâche, la gourde au calme.",
            "narrateur|Le grain de bitume luit, contre la mie.",
            "copain|On rebondit après, d'accord ?",
            "enfant-m|Après le goûter, oui.",
            "narrateur|Victorino refuse de sauter d'un coup.",
            "papa|Vous avez demandé, et ça marche.",
            "maman|Le pain a tenu l'élan.",
            "narrateur|Un morceau de pain sèche contre la gourde bleue.",
        ],
        (3, 3, 1): [
            "enfant-m|On fait un relais de balles.",
            "copain|Je te passe la gourde, tu me la rends.",
            "narrateur|La gourde bleue voyage d'une paume à l'autre.",
            "narrateur|Ils avancent le long du muret, l'un après l'autre.",
            "enfant-m|Une passe, pas toutes.",
            "narrateur|Le grain de bitume tient, à chaque passe.",
            "copain|Le portail est tout près.",
            "narrateur|Victorino refuse de foncer.",
            "papa|Vous jouez avec l'élan, ensemble.",
            "maman|Le muret est devenu une voie.",
            "enfant-m|Je la reconnais, le grain est là.",
            "narrateur|La gourde a fait le tour, sans se taire.",
        ],
        (3, 3, 2): [
            "enfant-m|On attend le portail.",
            "copain|Quand il s'ouvre, je rebondis.",
            "narrateur|Un pas, puis le battant reste fermé.",
            "narrateur|La gourde bleue reste muette, à la main.",
            "narrateur|Victorino observe le grain de bitume, sans courir.",
            "narrateur|Le battant bouge, enfin.",
            "copain|Maintenant !",
            "enfant-m|À toi, puis à moi.",
            "narrateur|Personne n'a poussé le fer.",
            "papa|Vous avez laissé le battant s'ouvrir.",
            "maman|L'élan a attendu le seuil.",
            "narrateur|Le grain de bitume luit, au bouchon.",
        ],
        (3, 3, 3): [
            "enfant-m|Papa, tu frappes le rythme ?",
            "papa|Tape, tape, et tu rebondis.",
            "narrateur|Aniss écoute les mains, plus que ses pieds.",
            "narrateur|Victorino lève la gourde quand papa frappe.",
            "copain|Je saute sur tes mains.",
            "enfant-m|Moi aussi, j'écoute.",
            "narrateur|Le grain de bitume penche, à chaque clap.",
            "narrateur|Le muret se range derrière les claps.",
            "narrateur|Victorino refuse de lever hors rythme.",
            "papa|Vous avez demandé le rythme.",
            "maman|Ses mains ont tenu l'élan.",
            "narrateur|Le bouchon tiède garde le grain, face au bleu.",
        ],
    }
    return vet(table[(a, b, c)])


def fin(a: int, b: int, c: int) -> list[str]:
    table = {
        (1, 1, 1): [
            "narrateur|Le dernier rond de la flaque est à eux.",
            "copain|On a joué, chacun son tour.",
            "enfant-m|Tu sautais, moi je rebondissais.",
            "papa|Vous avez laissé l'élan dessiner.",
            "maman|Le chemin sent l'eau, tiède.",
            "narrateur|Ça a failli tout filer.",
            "narrateur|La balle rouge garde le grain de bitume, mouillé.",
            "enfant-m|On rentre, Aniss.",
            "narrateur|Un rond d'eau sèche autour du grain, sur la pierre.",
        ],
        (1, 1, 2): [
            "narrateur|Le bord de la flaque garde la chaleur.",
            "enfant-m|Tu t'es arrêté, d'abord.",
            "copain|Puis j'ai rebondi, tout droit.",
            "papa|L'élan s'est assis, puis il a joué.",
            "maman|La flaque redevient sage.",
            "narrateur|Ça a failli tout sauter.",
            "narrateur|La balle rouge garde le grain de bitume, collé.",
            "enfant-m|À demain, les ronds.",
            "narrateur|Une feuille collée au grain de bitume, au bord.",
        ],
        (1, 1, 3): [
            "narrateur|La main de papa reste dans l'air, légère.",
            "copain|J'ai attendu le pas.",
            "enfant-m|On a demandé, et ça allait.",
            "maman|Sa main a tenu vos pieds.",
            "papa|Le chemin vous rend le silence.",
            "narrateur|Ça a failli tout glisser.",
            "narrateur|La balle rouge pose le grain de bitume sur le bois.",
            "copain|Il est à nous.",
            "narrateur|Un rai barre la flaque, pile sur le grain.",
        ],
        (1, 2, 1): [
            "narrateur|Deux paires de chaussures marquent le bout du banc.",
            "enfant-m|Toi devant, moi derrière.",
            "copain|Tes jambes allaient plus loin.",
            "papa|Vous avez sauté avec l'élan, pas contre.",
            "maman|Le tilleul redevient chaud.",
            "narrateur|Ça a failli tout rouler.",
            "narrateur|La balle rouge garde le grain de bitume, au creux.",
            "enfant-m|On rentre, le banc reste.",
            "narrateur|Un peu de poussière sèche dans une fente du bois.",
        ],
        (1, 2, 2): [
            "narrateur|Le bout du banc attend, tout lisse.",
            "copain|J'ai fini, puis c'était toi.",
            "enfant-m|J'ai attendu ta place.",
            "maman|Chacun son tour, sur le bois.",
            "papa|L'élan a laissé la place.",
            "narrateur|Ça a failli tout prendre.",
            "narrateur|La balle rouge garde le grain de bitume, au calme.",
            "copain|On se dit au revoir, banc.",
            "narrateur|Une feuille oubliée sèche contre le pied du banc.",
        ],
        (1, 2, 3): [
            "narrateur|Le pain de maman repose sur le banc.",
            "enfant-m|Tu le donnais, un morceau chacun.",
            "copain|On a demandé, et ça allait juste.",
            "papa|Le goûter a fait le tour, rien de plus.",
            "maman|Le tilleul a rendu le calme.",
            "narrateur|Ça a failli tout manger d'un coup.",
            "narrateur|La balle rouge garde le grain de bitume, près du pain.",
            "enfant-m|Regarde, Aniss, il brille.",
            "narrateur|Un rond de mie brille, collé au grain.",
        ],
        (1, 3, 1): [
            "narrateur|Le relais s'arrête contre le portail.",
            "copain|On est arrivés, tous les deux.",
            "enfant-m|Je te la passais, tu me la rendais.",
            "papa|Le muret est redevenu un mur, simplement.",
            "maman|L'élan s'est couché.",
            "narrateur|Ça a failli tout jeter.",
            "narrateur|La balle rouge garde le grain de bitume, au fer.",
            "enfant-m|On rentre, le relais se tait.",
            "narrateur|Une poussière tourne, puis tombe sur le fer du portail.",
        ],
        (1, 3, 2): [
            "narrateur|Le battant s'est ouvert, tout à fait.",
            "enfant-m|On a attendu le portail.",
            "copain|Quand il était ouvert, on rebondissait.",
            "papa|Le seuil vous a laissé la balle.",
            "maman|L'élan a écouté le battant.",
            "narrateur|Ça a failli tout pousser.",
            "narrateur|La balle rouge ne fait plus aucun bruit.",
            "enfant-m|Il est tiède.",
            "narrateur|La paume de Victorino garde le grain, tiède.",
        ],
        (1, 3, 3): [
            "narrateur|Les claps de papa s'éteignent, un à un.",
            "enfant-m|J'écoutais tes mains.",
            "copain|Moi aussi, je sautais dessus.",
            "maman|Vous avez demandé le rythme.",
            "papa|Le muret a rendu vos pas.",
            "narrateur|Ça a failli tout frapper d'un coup.",
            "narrateur|La balle rouge garde le grain de bitume, au creux.",
            "enfant-m|Il est à nous, Aniss.",
            "narrateur|Le fer du portail garde le grain, puis se tait.",
        ],
        (2, 1, 1): [
            "narrateur|Le dernier rond de la flaque est à eux.",
            "copain|On a joué, chacun son tour.",
            "enfant-m|Tu sautais, moi je tenais le sac.",
            "papa|Vous avez laissé l'élan dessiner.",
            "maman|Le chemin sent l'eau, tiède.",
            "narrateur|Ça a failli tout mouiller.",
            "narrateur|Le sac à pois sèche une feuille, près du grain.",
            "enfant-m|On rentre, Aniss.",
            "narrateur|Les pois du sac gardent une perle, près du grain.",
        ],
        (2, 1, 2): [
            "narrateur|Le bord de la flaque garde la chaleur.",
            "enfant-m|Tu t'es arrêté, d'abord.",
            "copain|Puis j'ai rebondi, tout droit.",
            "papa|L'élan s'est assis, puis il a joué.",
            "maman|La flaque redevient sage.",
            "narrateur|Ça a failli tout sauter.",
            "narrateur|Le sac à pois garde le grain de bitume, collé.",
            "enfant-m|À demain, les ronds.",
            "narrateur|Une feuille de tilleul sèche dans le sac, contre le grain.",
        ],
        (2, 1, 3): [
            "narrateur|La main de papa reste dans l'air, légère.",
            "copain|J'ai attendu le pas.",
            "enfant-m|On a demandé, et ça allait.",
            "maman|Sa main a tenu vos pieds.",
            "papa|Le chemin vous rend le silence.",
            "narrateur|Ça a failli tout glisser.",
            "narrateur|Le sac à pois pose le grain de bitume sur le bois.",
            "copain|Il est à nous.",
            "narrateur|L'ombre ronde du sac couvre le grain, un instant.",
        ],
        (2, 2, 1): [
            "narrateur|Deux paires de chaussures marquent le bout du banc.",
            "enfant-m|Toi devant, moi derrière.",
            "copain|Tes jambes allaient plus loin.",
            "papa|Vous avez sauté avec l'élan, pas contre.",
            "maman|Le tilleul redevient chaud.",
            "narrateur|Ça a failli tout rouler.",
            "narrateur|Le sac à pois garde le grain de bitume, au creux.",
            "enfant-m|On rentre, le banc reste.",
            "narrateur|Un pois du sac tient un brin de poussière.",
        ],
        (2, 2, 2): [
            "narrateur|Le bout du banc attend, tout lisse.",
            "copain|J'ai fini, puis c'était toi.",
            "enfant-m|J'ai attendu ta place.",
            "maman|Chacun son tour, sur le bois.",
            "papa|L'élan a laissé la place.",
            "narrateur|Ça a failli tout prendre.",
            "narrateur|Le sac à pois garde le grain de bitume, au calme.",
            "copain|On se dit au revoir, banc.",
            "narrateur|Le sac pose son ombre ronde sur le bois du banc.",
        ],
        (2, 2, 3): [
            "narrateur|Le pain de maman repose sur le banc.",
            "enfant-m|Tu le donnais, un morceau chacun.",
            "copain|On a demandé, et ça allait juste.",
            "papa|Le goûter a fait le tour, rien de plus.",
            "maman|Le tilleul a rendu le calme.",
            "narrateur|Ça a failli tout manger d'un coup.",
            "narrateur|Le sac à pois garde le grain de bitume, près du pain.",
            "enfant-m|Regarde, Aniss, il brille.",
            "narrateur|Un pois garde une mie, tout petit.",
        ],
        (2, 3, 1): [
            "narrateur|Le relais s'arrête contre le portail.",
            "copain|On est arrivés, tous les deux.",
            "enfant-m|Je te le passais, tu me le rendais.",
            "papa|Le muret est redevenu un mur, simplement.",
            "maman|L'élan s'est couché.",
            "narrateur|Ça a failli tout jeter.",
            "narrateur|Le sac à pois garde le grain de bitume, au fer.",
            "enfant-m|On rentre, le relais se tait.",
            "narrateur|Le sac s'appuie au fer, le grain coincé dans un pois.",
        ],
        (2, 3, 2): [
            "narrateur|Le battant s'est ouvert, tout à fait.",
            "enfant-m|On a attendu le portail.",
            "copain|Quand il était ouvert, on rebondissait.",
            "papa|Le seuil vous a laissé le sac.",
            "maman|L'élan a écouté le battant.",
            "narrateur|Ça a failli tout pousser.",
            "narrateur|Le sac à pois ne fait plus aucun bruit.",
            "enfant-m|Il est tiède.",
            "narrateur|La sangle tiède tient le grain, contre l'épaule.",
        ],
        (2, 3, 3): [
            "narrateur|Les claps de papa s'éteignent, un à un.",
            "enfant-m|J'écoutais tes mains.",
            "copain|Moi aussi, je sautais dessus.",
            "maman|Vous avez demandé le rythme.",
            "papa|Le muret a rendu vos pas.",
            "narrateur|Ça a failli tout frapper d'un coup.",
            "narrateur|Le sac à pois garde le grain de bitume, au creux.",
            "enfant-m|Il est à nous, Aniss.",
            "narrateur|Un pois du sac se tait, grain collé.",
        ],
        (3, 1, 1): [
            "narrateur|Le dernier rond de la flaque est à eux.",
            "copain|On a joué, chacun son tour.",
            "enfant-m|Tu sautais, moi je tenais la gourde.",
            "papa|Vous avez laissé l'élan dessiner.",
            "maman|Le chemin sent l'eau, tiède.",
            "narrateur|Ça a failli tout plonger.",
            "narrateur|La gourde bleue garde le grain de bitume, mouillé.",
            "enfant-m|On rentre, Aniss.",
            "narrateur|La gourde bleue garde une perle, collée au grain.",
        ],
        (3, 1, 2): [
            "narrateur|Le bord de la flaque garde la chaleur.",
            "enfant-m|Tu t'es arrêté, d'abord.",
            "copain|Puis j'ai rebondi, tout droit.",
            "papa|L'élan s'est assis, puis il a joué.",
            "maman|La flaque redevient sage.",
            "narrateur|Ça a failli tout sauter.",
            "narrateur|La gourde bleue garde le grain de bitume, collé.",
            "enfant-m|À demain, les ronds.",
            "narrateur|Un filet d'eau sèche sur le plastique, vers le grain.",
        ],
        (3, 1, 3): [
            "narrateur|La main de papa reste dans l'air, légère.",
            "copain|J'ai attendu le pas.",
            "enfant-m|On a demandé, et ça allait.",
            "maman|Sa main a tenu vos pieds.",
            "papa|Le chemin vous rend le silence.",
            "narrateur|Ça a failli tout glisser.",
            "narrateur|La gourde bleue pose le grain de bitume sur le bois.",
            "copain|Il est à nous.",
            "narrateur|La gourde pose son ombre bleue sur le grain.",
        ],
        (3, 2, 1): [
            "narrateur|Deux paires de chaussures marquent le bout du banc.",
            "enfant-m|Toi devant, moi derrière.",
            "copain|Tes jambes allaient plus loin.",
            "papa|Vous avez sauté avec l'élan, pas contre.",
            "maman|Le tilleul redevient chaud.",
            "narrateur|Ça a failli tout rouler.",
            "narrateur|La gourde bleue garde le grain de bitume, au creux.",
            "enfant-m|On rentre, le banc reste.",
            "narrateur|La gourde bute le bois, le grain coincé au bouchon.",
        ],
        (3, 2, 2): [
            "narrateur|Le bout du banc attend, tout lisse.",
            "copain|J'ai fini, puis c'était toi.",
            "enfant-m|J'ai attendu ta place.",
            "maman|Chacun son tour, sur le bois.",
            "papa|L'élan a laissé la place.",
            "narrateur|Ça a failli tout prendre.",
            "narrateur|La gourde bleue garde le grain de bitume, au calme.",
            "copain|On se dit au revoir, banc.",
            "narrateur|Le plastique tiède tient le grain, au creux.",
        ],
        (3, 2, 3): [
            "narrateur|Le pain de maman repose sur le banc.",
            "enfant-m|Tu le donnais, un morceau chacun.",
            "copain|On a demandé, et ça allait juste.",
            "papa|Le goûter a fait le tour, rien de plus.",
            "maman|Le tilleul a rendu le calme.",
            "narrateur|Ça a failli tout manger d'un coup.",
            "narrateur|La gourde bleue garde le grain de bitume, près du pain.",
            "enfant-m|Regarde, Aniss, il brille.",
            "narrateur|Un morceau de pain sèche contre la gourde bleue.",
        ],
        (3, 3, 1): [
            "narrateur|Le relais s'arrête contre le portail.",
            "copain|On est arrivés, tous les deux.",
            "enfant-m|Je te la passais, tu me la rendais.",
            "papa|Le muret est redevenu un mur, simplement.",
            "maman|L'élan s'est couché.",
            "narrateur|Ça a failli tout jeter.",
            "narrateur|La gourde bleue garde le grain de bitume, au fer.",
            "enfant-m|On rentre, le relais se tait.",
            "narrateur|La gourde s'arrête au fer, le grain au bouchon.",
        ],
        (3, 3, 2): [
            "narrateur|Le battant s'est ouvert, tout à fait.",
            "enfant-m|On a attendu le portail.",
            "copain|Quand il était ouvert, on rebondissait.",
            "papa|Le seuil vous a laissé la gourde.",
            "maman|L'élan a écouté le battant.",
            "narrateur|Ça a failli tout pousser.",
            "narrateur|La gourde bleue ne fait plus aucun bruit.",
            "enfant-m|Il est tiède.",
            "narrateur|Le bouchon tiède garde le grain, face au portail.",
        ],
        (3, 3, 3): [
            "narrateur|Les claps de papa s'éteignent, un à un.",
            "enfant-m|J'écoutais tes mains.",
            "copain|Moi aussi, je sautais dessus.",
            "maman|Vous avez demandé le rythme.",
            "papa|Le muret a rendu vos pas.",
            "narrateur|Ça a failli tout frapper d'un coup.",
            "narrateur|La gourde bleue garde le grain de bitume, au creux.",
            "enfant-m|Il est à nous, Aniss.",
            "narrateur|Les claps se taisent ; le grain dort sur le bleu.",
        ],
    }
    return vet(table[(a, b, c)])


def path_words(mp: dict, a: int, b: int, c: int) -> int:
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
    return sum(words(mp[i]["text"]) for i in ids)


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple] = {}

    scripts["CHK_T0000_P0000"] = (OPENING, "opening", "fermeture,balle", {"emphasis": "balle rouge"})
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "la balle rouge",
            "option_2_label": "le sac à pois",
            "option_3_label": "la gourde bleue",
        },
    )

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
                "engine_ok_text": "Oui, c'est ça.",
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
                "emphasis": t1["ans"],
            },
        )
        scripts[f"{base}_C0001"] = (t1["confirm"], "confirm", t1["sons"], {"emphasis": "portail"})
        scripts[f"{base}_T0002_P0000"] = (
            T2_CHOICE[a],
            "choice",
            "",
            {
                "option_1_label": "la flaque",
                "option_2_label": "le banc du tilleul",
                "option_3_label": "le muret du portail",
            },
        )
        for b in (1, 2, 3):
            leaf2 = f"{base}_T0002_P000{b}"
            t2d = T2[(a, b)]
            scripts[leaf2] = (t2d["lines"], "obstacle", t2d["sons"], {"emphasis": t2d["emp"]})
            scripts[f"{leaf2}_T0003_P0000"] = (
                T3_Q[b],
                "choice",
                "",
                {
                    "option_1_label": T3_LABS[b][0],
                    "option_2_label": T3_LABS[b][1],
                    "option_3_label": T3_LABS[b][2],
                },
            )
            for c in (1, 2, 3):
                leaf3 = f"{leaf2}_T0003_P000{c}"
                scripts[leaf3] = (
                    res(a, b, c),
                    "resolution",
                    "rebond,pas",
                    {"emphasis": "grain de bitume"},
                )
                scripts[f"{leaf3}_F0001"] = (
                    fin(a, b, c),
                    "ending",
                    "portail,pas",
                    {"emphasis": "portail", "note": ending_note(a, b, c)},
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
    t2s = [
        ch["text"]
        for ch in chunks
        if re.search(r"T0002_P000[123]$", ch["chunk_id"])
    ]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"T2 distincts {len(set(t2s))}/9")

    blob = "\n".join(c["script"] for c in chunks).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in chunks
    ).lower()
    whole = blob + "\n" + labels
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "j'ai compris",
        "mission accomplie",
        "hyperactif",
        "ce n'est pas une faute",
        "camarade qui bouge",
        "beaucoup d'énergie",
        "cuisine",
        "jardin",
        "dînette",
        "dinette",
        "les cubes",
        "après la sieste",
        "capitaine",
        "plic",
        "volet jaune",
        "boutique",
        "marelle",
        "carrousel",
        "papillon",
        "il faut attendre",
        "on doit demander",
        "sami",
        "citronnade",
        "grillon",
        "navire",
        "bateau",
        "camp de",
        "sous la lampe",
        "hérisson",
        "renard",
        "châle",
        "cacao",
        "colline",
        "crochet",
        "dent de fermeture",
        "merle",
        "miel",
        "aujourd'hui",
        "tout doux",
        "tout calme",
        "ticket",
        "quai",
        "wagon",
        "groseilles",
        "cerceaux",
        "porte jaune",
        "classe",
        "chambre",
        "marché",
        "nino",
        "chouchou",
        "amir",
        "nina",
        "mila",
        "sarah",
        "raphaël",
        "victorina",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    for bad in BAD_INDICE:
        if bad in whole:
            raise SystemExit(f"{SID} indice interdit: {bad}")
    if TICS.search(blob):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "victorino" not in blob:
        raise SystemExit(f"{SID}: Victorino absent")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "grain de bitume" not in blob:
        raise SystemExit(f"{SID}: grain de bitume absent")
    if "balle" not in blob:
        raise SystemExit(f"{SID}: balle absente")
    adults = [ln for ln in blob.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    aj = " ".join(a.split("|", 1)[1] for a in adults)
    if aj.count("merci") + aj.count("bravo") != 1:
        raise SystemExit(f"{SID}: merci/bravo ×{aj.count('merci') + aj.count('bravo')}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in chunks)
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    if any(c.get("text_xai_tags") == c.get("text") for c in chunks):
        raise SystemExit("text_xai_tags = text")
    if len(chunks) != 86:
        raise SystemExit(f"chunks {len(chunks)}≠86")

    mp = {ch["chunk_id"]: ch for ch in chunks}
    ws = [path_words(mp, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    if min(ws) < 520 or max(ws) > 720:
        raise SystemExit(f"chemins mots hors barre: min={min(ws)} max={max(ws)}")

    out = dict(src)
    out["fil_rouge"] = (
        "Victorino veut faire rebondir sa balle rouge jusqu'au portail, avec Aniss. "
        "Un grain de bitume tient au caoutchouc. Il lance trop fort, le grain penche. "
        "Aniss veut courir maintenant ; Victorino veut rebondir. Le silence d'Aniss répond. "
        "Il prend d'abord la balle, le sac à pois ou la gourde ; les trois partent. "
        "À la flaque Aniss saute trop fort, au banc le bois penche, au muret le trottoir tire. "
        "Victorino refuse de foncer. Ils dosent l'élan. Le portail arrive. Le grain reste."
    )
    out["title"] = TITLE
    out["characters"] = "Victorino, Aniss, papa, maman"
    out["setting"] = "chemin de l'école : flaque, banc du tilleul, muret du portail"
    out["chunks"] = chunks
    check(SID, out["age_band"], out["chunks"])

    print(f"chemins mots min={min(ws)} max={max(ws)} moy={sum(ws)//len(ws)}")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"""# {SID} — {TITLE}

- **Public :** N2 (4–5 ans), audio familial
- **Leçon :** DIF.ENE.001 — attendre / ne pas tout brûler d'un coup (vécue, jamais dite)
- **Personnages :** Victorino, Aniss, papa, maman
- **Lieu :** chemin de l'école : flaque, banc du tilleul, muret du portail
- **Structure conservée :** 86 nœuds, graphe, labels, 27 chemins, 27 fins distinctes

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

La fermeture du sac à pois se coince. Victorino tire trop fort : la balle rouge roule et s'arrête contre un **grain de bitume**. Mission : la faire rebondir jusqu'au portail. Aniss veut courir maintenant ; Victorino veut rebondir. Premier lancer trop fort, grain penché, sourire parti. Papa s'accroupit. Merci vécu : tu as vu le grain.

T1 = balle rouge / sac à pois / gourde bleue (les trois partent). T2 = flaque (ronds, silence dans l'eau) / banc du tilleul (pente du bois) / muret du portail (trottoir qui tire). T3 = neuf façons de doser (jouer dans l'eau, attendre la goutte, main de papa ; sauter ensemble, attendre le tour, goûter de maman ; relais de balles, attendre le portail, rythme de papa). Le grain du début est payé. Le portail arrive. Chaque fin porte une trace unique.

Monde ≠ TREE-DIF-044 (Raphaël, groseilles, serre/treillis), ≠ TREE-DIF-050 (Aniss, cerceaux, porte jaune), ≠ TREE-DIF-063 (Victorino, ticket, quai).

## Vécu

Impatience d'Aniss, découragement quand le grain penche, fierté calme quand Victorino refuse de foncer. Rythmes distincts : l'un propose, l'autre prend son temps. Le silence d'Aniss compte comme une réponse. L'adulte guide peu, s'accroupit. La leçon se voit : un rebond, puis l'autre ; attendre la goutte, le tour, le battant. Jamais dite.

## Vu et corrigé

- Ancien merged F-NAR-016 sans notes/xai : tout réécrit.
- Ouverture inventée (fermeture coincée, balle qui roule). Pas « encore ». Pas les cinq gabarits v2.
- Indice unique : grain de bitume, dès l'ouverture, payé au climax.
- Corps : sourire parti, poitrine bousculée, adulte à la même hauteur.
- 2e ruse plus maline (eau qui retient, bois en pente, trottoir qui tire). Il refuse de foncer.
- Dénouement qui a failli. 27 fins, 27 dernières images, 27 T3, 9 T2.
- T1 ne retire pas l'équipement. Labels conservés.
- Un merci de papa lié au geste (voir le grain). Question d'adulte. Un « en ce moment ».
- Tics « encore / déjà / tout doux / tout calme », merle, miel, slogans : jetés.
- TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending).
- Chemins : {min(ws)}–{max(ws)} mots (moyenne {sum(ws)//len(ws)}). `check()` N2 OK. Pas d'apply.

## Direction vocale

`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, tempo, sourire, respiration. `slow` = choix, indice, fin. Obstacle en `low-pitch`. Fins `soft` / `slow` / `low-pitch`.

## Contrôles

- 86 chunks
- 27 chemins, 27 fins distinctes, 27 dernières images
- {min(ws)} à {max(ws)} mots par chemin (moyenne {sum(ws)//len(ws)})
- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'apply.
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
