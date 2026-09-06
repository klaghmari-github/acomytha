#!/usr/bin/env python3
"""TREE-COL-027 — Les toiles rayées du marché (N3, COL.POL.001, TTS)."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-COL-027"
LIM = LIMITS["N3"]
FOLDER = ROOT / SID
TITLE = "Les toiles rayées du marché"
CHARS = "Mila, papa, maman"
SETTING = "marché du village, toiles, étals, panier d'osier"
FIL = (
    "Sous les toiles rayées du marché, Mila veut porter le panier d'osier "
    "jusqu'au bout des étals, avant que les voiles se plient. Une écaille "
    "d'orange brille sur une rayure, puis voyage sur l'anse. Elle tire trop "
    "tôt : personne n'entend, le panier penche. Boulangerie, étal ou "
    "fromagerie changent le bruit. Boulangère, voisin ou maîtresse changent "
    "l'oreille à attendre. Pain, pomme ou fromage trouvent une place, et "
    "l'écaille du début est payée."
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="écaille d'orange",
        note="arc=installation; intention=émerveiller; emotion=envie_impatiente; intensite=1; destinataire=enfant; sous_texte=le panier veut partir trop vite; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=une_oreille_s_ouvre; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_veut_couper_pour_garder_le_panier; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_retenue; intensite=2; destinataire=enfant; sous_texte=parler_trop_tôt_casse_la_phrase; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=attendre_livre_une_vraie_oreille; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="écaille d'orange",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=l_ecaille_a_trouve_sa_place_sous_les_toiles; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp:
        e = esc(emp)
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
    if m.get("pitchTag"):
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    pause = m["pause"]
    suffix = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + suffix).strip()


def split_sents(phrase: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    for ch in phrase:
        buf.append(ch)
        if ch in ".?!":
            s = "".join(buf).strip()
            if s:
                parts.append(s)
            buf = []
    tail = "".join(buf).strip()
    if tail:
        parts.append(tail if tail.endswith((".", "?", "!")) else tail + ".")
    return parts


def L(*rows: str) -> list[str]:
    out = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        for phrase in split_sents(ph):
            n = words(phrase)
            if n > LIM:
                raise SystemExit(f"{n}>{LIM}: {phrase}")
            marks = phrase.count(".") + phrase.count("?") + phrase.count("!")
            if marks != 1:
                raise SystemExit(f"ponctuation {marks}: {phrase}")
            if not phrase.endswith((".", "?", "!")):
                raise SystemExit(f"fin: {phrase}")
            low = phrase.lower()
            for tic in ("tout doux", "tout calme", "encore", "déjà"):
                if tic in low:
                    raise SystemExit(f"tic {tic}: {phrase}")
            out.append(f"{role}|{phrase}")
    return out


def apply_voice(nc: dict, profile: str, emphasis=None, sons=None) -> dict:
    m = dict(PROFILES[profile])
    if emphasis is not None:
        m["emphasis"] = emphasis
    text = nc["text"]
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
    nc["text_ssml"] = ssml(text, m)
    nc["text_xai_tags"] = xai(text, m)
    nc["rate_wpm"] = m["wpm"]
    nc["rate_label"] = m["rate"]
    nc["speed_xai"] = m["speed"]
    nc["length_scale_piper"] = m["piper"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitchSsml"]
    nc["pitch_xai_tag"] = m["pitchTag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = m["emphasis"] or ""
    nc["pause_before_ms"] = 0
    nc["pause_after_ms"] = m["pause"]
    nc["pause_sentence_ms"] = m["sentence"]
    nc["style_energy"] = m["energy"]
    nc["style_contour"] = m["contour"]
    nc["noise_scale_piper"] = m["noise"]
    nc["kokoro_speed"] = m["speed"]
    nc["melo_speed"] = m["speed"]
    nc["espeak_amp"] = 82 if m["volume"] == "soft" else 100
    nc["espeak_pitch"] = 42 if m["pitch"] == "low" else 50
    nc["espeak_word_gap"] = 12 if m["rate"] == "slow" else 8
    nc["notes"] = m["note"]
    nc["night_policy"] = "play"
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"
    if sons is not None:
        nc["sons"] = sons
    elif not nc.get("sons"):
        nc["sons"] = ""
    return nc


def pack_chunk(src: dict, lines: list[str], profile: str, *, emphasis=None, sons=None, extra=None) -> dict:
    text, script = from_script(lines)
    nc = deepcopy(src)
    nc["text"] = text
    nc["script"] = script
    apply_voice(nc, profile, emphasis=emphasis, sons=sons)
    if extra:
        nc.update(extra)
    return nc


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str, ok: str, near: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
        "engine_ok_text": ok,
        "engine_near_text": near,
    }


def profile_for(cid: str, kind: str) -> str:
    if kind == "passage_debut":
        return "opening"
    if kind == "transition_question":
        return "choice"
    if kind == "passage_question":
        return "clue"
    if kind == "passage_fin":
        return "ending"
    if cid.endswith("_C0001"):
        return "confirm"
    if "_T0003_P" in cid and cid[-1] in "123" and "T0003_P0000" not in cid:
        return "resolution"
    if "_T0002_P" in cid and "T0003" not in cid and cid[-1] in "123":
        return "obstacle"
    return "action"


PLACES = {
    1: dict(lab="la boulangerie", ou="à la boulangerie", son="cloche,papier"),
    2: dict(lab="l'étal", ou="à l'étal", son="caisse,toile"),
    3: dict(lab="la fromagerie", ou="à la fromagerie", son="papier"),
}
PEOPLE = {
    1: dict(lab="la boulangère", son="palette,bois"),
    2: dict(lab="le voisin", son="casquette,osier"),
    3: dict(lab="la maîtresse", son="sac,regle"),
}
FOODS = {
    1: dict(lab="le pain", son="papier"),
    2: dict(lab="une pomme", son="pomme"),
    3: dict(lab="un fromage", son="papier"),
}


def opening() -> list[str]:
    return L(
        "narrateur|Une ombre à rayures court sur les pavés.",
        "narrateur|Elle est trop large pour les pieds de Mila.",
        "narrateur|Les toiles claquent au-dessus, comme des voiles basses.",
        "narrateur|Ça sent l'orange pressée, et un peu de café.",
        "narrateur|Papa tient un panier d'osier, vide, l'anse rêche.",
        "narrateur|Maman noue un foulard bleu, près d'une caisse.",
        "narrateur|Collée à une rayure rouge, une écaille d'orange brille.",
        "narrateur|Elle est fine, un peu collante, comme un petit bateau.",
        "enfant-f|Je veux porter le panier, moi.",
        "enfant-f|Je le remplis, avant que les toiles se plient.",
        "narrateur|En ce moment, Mila tire l'anse, sans attendre.",
        "narrateur|Papa parle à maman du pain, et ne se tourne pas.",
        "narrateur|Le panier penche.",
        "narrateur|L'écaille glisse de la rayure, vers une caisse.",
        "enfant-f|Le panier !",
        "narrateur|Sa voix se casse contre le claquement des toiles.",
        "narrateur|Personne ne se tourne.",
        "narrateur|Le sourire de Mila disparaît.",
        "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        "narrateur|Papa s'accroupit, à la même hauteur.",
        "papa|Tu voulais le panier, Mila ?",
        "narrateur|Mila ouvre la bouche, puis la referme.",
        "narrateur|Elle attend la fin de sa question.",
        "enfant-f|Oui.",
        "enfant-f|Je le porte jusqu'au bout des étals.",
        "papa|Merci d'avoir attendu ma phrase.",
        "maman|On t'écoute, maintenant.",
        "narrateur|Mila ramasse l'écaille, du bout des doigts.",
        "narrateur|Elle la pose sur le bord de l'osier.",
        "enfant-f|Elle voyage avec nous.",
    )


T1_PASS = {
    1: L(
        "narrateur|Mila porte le panier vers la boulangerie.",
        "narrateur|L'osier cogne son genou, à chaque pas.",
        "narrateur|L'air chaud arrive, chargé de croûte.",
        "narrateur|Une cloche fait ding, trop fort, trop proche.",
        "narrateur|De la farine blanche poudre le bois du comptoir.",
        "enfant-f|Le petit pain, je le prends !",
        "narrateur|Sa voix se casse contre la cloche.",
        "narrateur|Personne ne se tourne.",
        "narrateur|Mila serre l'anse rêche.",
        "narrateur|L'osier pique sa paume.",
        "narrateur|Elle referme la bouche.",
        "narrateur|Elle attend que la cloche se taise.",
        "papa|La cloche a fini.",
        "papa|Je t'écoute.",
        "enfant-f|Je veux porter le panier jusqu'aux croûtes.",
        "maman|On le porte ensemble, sans se presser.",
        "narrateur|Sur le seuil, une toile rayée claque.",
        "narrateur|L'écaille d'orange brille au bord de l'osier.",
    ),
    2: L(
        "narrateur|Mila avance vers l'étal, le panier contre la hanche.",
        "narrateur|Les toiles font un tunnel d'ombre, rouge et blanc.",
        "narrateur|Des caisses de fruit sentent le soleil.",
        "enfant-f|Je le mets là, vite !",
        "narrateur|Elle pousse le panier contre une caisse.",
        "narrateur|La caisse recule, trop vite.",
        "narrateur|Un citron roule, puis s'arrête contre un pied.",
        "narrateur|Papa parle à maman d'une tomate, plus loin.",
        "narrateur|Les mots de Mila se perdent sous la toile.",
        "narrateur|Elle pose le panier à terre, un instant.",
        "narrateur|Elle attend que la caisse ne bouge plus.",
        "maman|La caisse est calme.",
        "maman|Que voulais-tu dire ?",
        "enfant-f|Le panier reste avec moi, sous les toiles.",
        "papa|Il reste. On t'écoute.",
        "narrateur|L'écaille d'orange tremble au bord, dans l'ombre rayée.",
    ),
    3: L(
        "narrateur|Mila entre à la fromagerie, le panier serré.",
        "narrateur|L'air est froid, et ça sent la cave.",
        "narrateur|Un papier blanc froisse, trop fort, trop longtemps.",
        "enfant-f|J'ai le panier, regardez !",
        "narrateur|Le froissement recouvre sa phrase.",
        "narrateur|Maman plie un sachet, près du marbre.",
        "narrateur|Mila sent ses joues chauffer, malgré le froid.",
        "narrateur|Elle referme les lèvres.",
        "narrateur|Elle attend que le papier se taise.",
        "papa|Le papier a fini.",
        "papa|Je t'écoute.",
        "enfant-f|Je veux le remplir, avant les toiles pliées.",
        "maman|On le remplit. On a le temps d'entendre.",
        "narrateur|Sur le marbre, une ombre rayée passe, puis s'en va.",
        "narrateur|L'écaille d'orange brille, un peu plus froide.",
    ),
}

T1_Q = {
    1: (
        L(
            "narrateur|Un bruit a couvert la voix de Mila.",
            "maman|Qu'est-ce qui a sonné trop fort ?",
        ),
        "cloche",
        "cloche | la cloche | une cloche | ding",
        "Écoute l'indice. Qu'est-ce qui a sonné ?",
        "Oui, c'est la cloche.",
        "Tu es tout près. Qu'est-ce qui a fait ding ?",
        "cloche",
    ),
    2: (
        L(
            "narrateur|Quelque chose a tapé le panier, trop vite.",
            "papa|Qu'est-ce qui a bougé contre l'osier ?",
        ),
        "caisse",
        "caisse | la caisse | une caisse | caisses",
        "Écoute l'indice. Qu'est-ce qui a bougé ?",
        "Oui, c'est la caisse.",
        "Tu es tout près. Qu'est-ce qui a reculé ?",
        "caisse",
    ),
    3: (
        L(
            "narrateur|Un froissement a recouvert ses mots.",
            "papa|Qu'est-ce qui a parlé trop fort, près du marbre ?",
        ),
        "papier",
        "papier | le papier | un papier | sachet",
        "Écoute l'indice. Qu'est-ce qui froissait ?",
        "Oui, c'est le papier.",
        "Tu es tout près. Qu'est-ce qui se pliait ?",
        "papier",
    ),
}

T1_C = {
    1: L(
        "papa|Oui.",
        "papa|La cloche s'est tue.",
        "narrateur|Mila souffle.",
        "narrateur|Un peu de farine saute de l'anse.",
        "enfant-f|J'ai parlé trop vite.",
        "maman|Là, on t'écoute.",
        "narrateur|L'écaille tient bon, au bord de l'osier.",
        "papa|On peut remplir le panier, sans se bousculer.",
    ),
    2: L(
        "maman|Oui.",
        "maman|La caisse ne recule plus.",
        "narrateur|Mila ramène le panier contre sa hanche.",
        "enfant-f|Il est à moi, sous les toiles.",
        "papa|Il voyage avec toi.",
        "narrateur|Le citron reste contre le pied de la caisse.",
        "maman|Tes mots ont de la place, maintenant.",
        "narrateur|L'ombre rayée caresse l'écaille, puis s'en va.",
    ),
    3: L(
        "papa|Oui.",
        "papa|Le papier se tait.",
        "narrateur|Mila essuie le marbre du bout d'un doigt.",
        "narrateur|Le froid pique, puis ça passe.",
        "enfant-f|J'attendais le silence.",
        "maman|On t'a entendue, entière.",
        "narrateur|L'écaille d'orange fait un point chaud, sur le froid.",
        "papa|Le panier peut choisir, maintenant.",
    ),
}

T2_CHOICE = {
    1: L(
        "narrateur|Près des croûtes, le panier peut s'approcher de trois personnes.",
        "papa|La boulangère, le voisin, ou la maîtresse ?",
        "maman|Vers qui vas-tu, avec l'osier ?",
    ),
    2: L(
        "narrateur|Sous les toiles de l'étal, trois personnes sont là.",
        "maman|La boulangère, le voisin, ou la maîtresse ?",
        "papa|Qui écoutes-tu d'abord ?",
    ),
    3: L(
        "narrateur|Près du marbre, trois personnes parlent.",
        "papa|La boulangère, le voisin, ou la maîtresse ?",
        "maman|Qui a une oreille, pour toi ?",
    ),
}

T2_PASS = {
    (1, 1): L(
        "narrateur|La boulangère tape le pain avec une palette de bois.",
        "narrateur|Tap, tap, tap, sur la croûte dorée.",
        "enfant-f|Bonjour, je veux—",
        "narrateur|La palette recouvre le mot.",
        "narrateur|Mila sent le chaud aux joues.",
        "narrateur|Elle recule d'un pas, le panier contre elle.",
        "narrateur|Cette fois, Mila refuse de foncer.",
        "narrateur|Elle guette l'écaille, au bord de l'osier.",
        "enfant-f|Quand la palette a fini, je parle ?",
        "papa|Elle a fini.",
        "papa|Elle te regarde.",
        "narrateur|Un peu de farine colle à l'écaille, comme du givre.",
        "maman|Que veux-tu mettre dans le panier ?",
    ),
    (1, 2): L(
        "narrateur|Le voisin bloque la porte, casquette rayée sur le crâne.",
        "narrateur|Il raconte un bouton perdu, trop long, trop fort.",
        "enfant-f|Pardon, je passe—",
        "narrateur|Le bouton recouvre sa phrase.",
        "narrateur|Mila serre l'anse. L'envie de crier monte.",
        "narrateur|Elle avale le cri.",
        "narrateur|Elle refuse de foncer dans son récit.",
        "narrateur|L'écaille d'orange attend, collée à l'osier.",
        "enfant-f|Quand le bouton est trouvé, je peux dire ?",
        "maman|Le bouton est dans sa poche.",
        "maman|Il se pousse. On t'écoute.",
        "narrateur|La casquette rayée salue les toiles, un instant.",
        "papa|Que veux-tu demander, maintenant ?",
    ),
    (1, 3): L(
        "narrateur|La maîtresse tient un sac jaune, une règle qui dépasse.",
        "narrateur|Elle parle à maman d'une caisse de menthe, à la fenêtre.",
        "enfant-f|Maîtresse, le panier—",
        "narrateur|Les deux voix d'adultes se mélangent.",
        "narrateur|Le mot de Mila tombe entre la règle et le sac.",
        "narrateur|Elle touche le coude de maman, puis attend.",
        "narrateur|Elle refuse de couper la menthe.",
        "narrateur|Elle regarde l'écaille, petite lampe sur l'osier.",
        "enfant-f|Quand la menthe est dite, je parle ?",
        "maman|Elle est dite.",
        "maman|Elle se tourne. Nous t'écoutons.",
        "narrateur|La règle tapote le sac, puis se tait.",
        "papa|Que veux-tu mettre dedans, maintenant ?",
    ),
    (2, 1): L(
        "narrateur|La boulangère est sortie, tablier blanc, loin du four.",
        "narrateur|Elle pèse des tomates, les yeux sur l'aiguille.",
        "enfant-f|Bonjour, j'aimerais—",
        "narrateur|L'aiguille tremble. Elle n'entend pas.",
        "narrateur|Une toile claque au-dessus des caisses.",
        "narrateur|Mila avale son envie de crier plus fort.",
        "narrateur|Elle refuse de foncer sur la balance.",
        "narrateur|L'écaille d'orange fait un point, dans l'ombre.",
        "enfant-f|Quand l'aiguille s'arrête, je peux parler ?",
        "papa|Elle s'arrête.",
        "papa|La boulangère lève les yeux.",
        "narrateur|Une miette roule près du pied de Mila.",
        "maman|Que veux-tu mettre dans l'osier, à présent ?",
    ),
    (2, 2): L(
        "narrateur|Le voisin a posé son panier en travers de l'étal.",
        "narrateur|Il compare deux tomates, d'une voix ronde, trop large.",
        "enfant-f|S'il te plaît, je voudrais—",
        "narrateur|Les tomates recouvrent le mot.",
        "narrateur|Mila recule. Son ventre se serre.",
        "narrateur|Elle pose deux doigts sur l'anse, sans tirer.",
        "narrateur|Elle refuse de pousser son osier contre le sien.",
        "narrateur|Elle cherche l'écaille, sous une rayure d'ombre.",
        "enfant-f|Quand les tomates ont choisi, je passe ?",
        "maman|Elles ont choisi.",
        "maman|Son panier se décale. On t'écoute.",
        "narrateur|L'osier du voisin frotte le bois, un bruit sec.",
        "papa|Que veux-tu demander, le chemin libre ?",
    ),
    (2, 3): L(
        "narrateur|La maîtresse choisit un ruban rouge, très lente.",
        "narrateur|Maman lui parle d'un plaid rayé, pour le pré.",
        "enfant-f|Bonjour, maîtresse, le—",
        "narrateur|Le mot se perd entre le ruban et le plaid.",
        "narrateur|Mila touche le bord du panier, puis attend.",
        "narrateur|Elle refuse de couper le plaid.",
        "narrateur|Une toile claque. L'écaille ne bouge pas.",
        "enfant-f|Quand le ruban est choisi, je dis ?",
        "maman|Il est choisi.",
        "maman|Elle te regarde. Nous aussi.",
        "narrateur|Le sac jaune penche. La règle y fait un coin.",
        "narrateur|L'écaille d'orange garde sa forme de bateau.",
        "papa|Que veux-tu mettre dans le panier, sous les toiles ?",
    ),
    (3, 1): L(
        "narrateur|La boulangère est entrée, loin du four, pour un peu de lait.",
        "narrateur|Elle parle au marbre, d'un fromage à tartiner.",
        "enfant-f|Bonjour, je peux—",
        "narrateur|Le mot glisse sur le marbre froid, sans oreille.",
        "narrateur|Mila sent le froid aux doigts. Elle se tait.",
        "narrateur|Elle refuse de foncer sur le lait.",
        "narrateur|À la porte, l'écaille d'orange fait un point chaud.",
        "enfant-f|Quand le lait est dit, je parle ?",
        "papa|Le lait est dit.",
        "papa|Elle se tourne. Tes mots ont de la place.",
        "narrateur|Un papier blanc attend, plié, près de la balance.",
        "narrateur|La farine de son tablier fait un nuage, dans l'air frais.",
        "maman|Que veux-tu demander, sur ce marbre froid ?",
    ),
    (3, 2): L(
        "narrateur|Le voisin appuie son panier sur le comptoir de marbre.",
        "narrateur|Il raconte un fromage d'hier, trop fort, trop long.",
        "enfant-f|Pardon, s'il te plaît—",
        "narrateur|Le récit d'hier recouvre sa phrase.",
        "narrateur|Mila serre les dents, puis les desserre.",
        "narrateur|Elle recule le panier. Elle refuse de crier.",
        "narrateur|Elle fixe l'écaille, collée à l'osier, près du froid.",
        "enfant-f|Quand hier est fini, je dis mes mots, maintenant ?",
        "maman|Hier est fini.",
        "maman|Le marbre t'écoute. Nous aussi.",
        "narrateur|Le voisin décale l'osier. Un rond d'eau reste sur le blanc.",
        "narrateur|Ça sent le lait, et un peu de cave.",
        "papa|Que veux-tu mettre dans le panier, maintenant ?",
    ),
    (3, 3): L(
        "narrateur|La maîtresse commande un petit fromage, pour le goûter.",
        "narrateur|Elle parle à maman d'un jardin de pots, près du marbre.",
        "enfant-f|Maîtresse, le panier—",
        "narrateur|Le jardin et la commande se mélangent. Rien n'arrive.",
        "narrateur|Mila pose le panier à terre, pour ne plus bouger.",
        "narrateur|Elle refuse de couper les pots.",
        "narrateur|Elle attend que le jardin se ferme, comme une porte.",
        "enfant-f|Quand les pots sont finis, je peux dire ?",
        "papa|Ils sont finis.",
        "papa|Elle te regarde. Vas-y, tout entier.",
        "narrateur|Le sac jaune sent le fromage, un instant, bizarre.",
        "narrateur|L'écaille d'orange, à la porte, ne tombe pas.",
        "maman|Que veux-tu demander, maintenant que c'est ton tour ?",
    ),
}


def t3_choice(a: int, b: int) -> list[str]:
    place = PLACES[a]["ou"]
    who = PEOPLE[b]["lab"]
    if a == 1:
        return L(
            f"narrateur|{who.capitalize()} a une oreille, {place}.",
            "narrateur|Le pain, une pomme, ou un fromage peuvent entrer.",
            "maman|Que mets-tu dans le panier, maintenant ?",
        )
    if a == 2:
        return L(
            f"narrateur|{place.capitalize()}, {who} s'est poussé.",
            "narrateur|Le pain, une pomme, ou un fromage attendent l'osier.",
            "papa|Que choisis-tu, sous les toiles ?",
        )
    return L(
        f"narrateur|Près du marbre, {who} t'a entendue.",
        "narrateur|Le pain, une pomme, ou un fromage peuvent finir le geste.",
        "maman|Quel goût pour le panier ?",
    )


# 27 climaxes : autre ruse, autre paiement de l'écaille.
T3_PASS = {
    (1, 1, 1): L(
        "narrateur|Mila montre le petit pain, derrière la vitre chaude.",
        "narrateur|Elle ouvre la bouche trop tôt. La cloche fait ding.",
        "enfant-f|Attends. Pas maintenant.",
        "narrateur|Elle refuse de foncer.",
        "narrateur|Elle regarde l'écaille d'orange, au bord de l'osier.",
        "narrateur|La cloche se tait. Le silence a un trou.",
        "enfant-f|Le petit pain, s'il te plaît.",
        "narrateur|La boulangère hoche. Le sachet papier craque, tiède.",
        "papa|Toute la phrase est arrivée.",
        "maman|Tu l'as entendue, toi aussi ?",
        "narrateur|Un peu de farine tombe près de l'écaille.",
        "narrateur|Le pain chauffe l'osier, comme une petite lampe.",
    ),
    (1, 1, 2): L(
        "narrateur|Près des croûtes, une pomme rouge attend dans une caisse.",
        "narrateur|Mila parle pendant que la boulangère essuie la vitre.",
        "narrateur|Le chiffon frotte. Son mot glisse.",
        "enfant-f|Je n'aime pas ça.",
        "narrateur|Elle refuse de foncer sur le chiffon.",
        "narrateur|L'écaille d'orange guide son regard vers la pomme.",
        "enfant-f|La pomme, s'il te plaît.",
        "narrateur|Elle la pose. Un point jaune brille sur la peau.",
        "maman|Le chiffon s'est tu. Tes mots, non.",
        "papa|La pomme est à toi, entière.",
        "narrateur|Le point jaune s'aligne avec l'écaille, sur l'anse.",
        "narrateur|Deux petits soleils, l'un fruit, l'un orange.",
    ),
    (1, 1, 3): L(
        "narrateur|Un fromage en papier blanc attend, près des brioches.",
        "narrateur|Mila commence. La boulangère coupe une tranche, plus loin.",
        "narrateur|Le couteau parle. Elle, non.",
        "enfant-f|Quand le couteau dort, je dis.",
        "narrateur|Elle refuse de foncer.",
        "narrateur|Elle suit l'écaille d'orange, collée à l'osier.",
        "enfant-f|Le fromage, s'il te plaît.",
        "narrateur|Elle tend le paquet. Ça sent le lait, dans le beurre.",
        "papa|Le couteau a eu son tour. Toi, le tien.",
        "maman|Le papier blanc se tait, dans tes mains.",
        "narrateur|Un coin du papier passe près de l'écaille, comme un drapeau.",
        "narrateur|Le froid du fromage touche le chaud du four.",
    ),
    (1, 2, 1): L(
        "narrateur|Le voisin range sa casquette, près des croûtes.",
        "narrateur|Mila veut le pain pendant qu'il cherche le bouton.",
        "enfant-f|Le pain, vite—",
        "narrateur|La poche du voisin recouvre le mot.",
        "narrateur|Mila referme la bouche. Elle refuse de foncer.",
        "narrateur|L'écaille d'orange attend, patiente, sur l'anse.",
        "enfant-f|Le pain, s'il te plaît.",
        "narrateur|Le sachet arrive. La casquette rayée s'incline.",
        "papa|Son bouton est trouvé. Ton pain aussi.",
        "maman|Deux phrases, l'une après l'autre.",
        "narrateur|La croûte chauffe l'écaille, un peu collante.",
        "narrateur|Mila rit, bas, sans crier sur le marché.",
    ),
    (1, 2, 2): L(
        "narrateur|Le panier du voisin cache la caisse de pommes.",
        "narrateur|Mila avance la main trop tôt.",
        "narrateur|Une pomme roule vers sa casquette.",
        "enfant-f|Oh, elle part !",
        "narrateur|Elle refuse de foncer pour la rattraper seule.",
        "narrateur|Elle montre l'écaille, puis la pomme, sans crier.",
        "papa|On la prend ensemble, quand il a fini sa poche.",
        "enfant-f|La pomme, s'il te plaît.",
        "narrateur|Le voisin décale l'osier. La pomme tient.",
        "maman|Elle n'a pas roulé sous la porte.",
        "narrateur|L'écaille et la queue de la pomme se touchent.",
        "narrateur|Deux bouts, l'un collant, l'un dur.",
    ),
    (1, 2, 3): L(
        "narrateur|Le voisin parle d'un fromage d'hier, près du four.",
        "narrateur|Mila tend le doigt vers le paquet blanc.",
        "enfant-f|Celui-là—",
        "narrateur|Hier recouvre le présent. Le mot tombe.",
        "narrateur|Elle refuse de foncer dans son récit.",
        "narrateur|Elle regarde l'écaille d'orange, petit bateau du présent.",
        "enfant-f|Le fromage, s'il te plaît.",
        "narrateur|Le papier craque. Ça sent la cave, malgré le four.",
        "papa|Hier s'est tu. Toi, tu es là.",
        "maman|Le paquet pèse, frais, dans l'osier.",
        "narrateur|L'écaille orne le papier, comme un ticket.",
        "narrateur|La casquette rayée salue, puis s'en va.",
    ),
    (1, 3, 1): L(
        "narrateur|La maîtresse tient le sac jaune, près des croûtes.",
        "narrateur|Mila veut le pain pendant la phrase sur la menthe.",
        "enfant-f|Le pain—",
        "narrateur|La règle tapote. Le mot se casse.",
        "narrateur|Mila refuse de foncer entre la règle et le sac.",
        "narrateur|Elle cherche l'écaille d'orange, au bord.",
        "enfant-f|Le petit pain, s'il te plaît.",
        "narrateur|Le sachet tiède glisse dans l'osier.",
        "maman|La menthe a fini. Ton pain commence.",
        "papa|Elle t'a vue, entière.",
        "narrateur|Un peu de farine tache le sac jaune, minuscule.",
        "narrateur|L'écaille reste propre, collée à l'anse.",
    ),
    (1, 3, 2): L(
        "narrateur|Le sac jaune penche vers la caisse de pommes.",
        "narrateur|La règle manque la peau rouge.",
        "enfant-f|Attention, la pomme !",
        "narrateur|Mila a envie de tirer le sac. Elle ne le fait pas.",
        "narrateur|Elle refuse de foncer.",
        "narrateur|Elle montre l'écaille, puis attend la règle posée.",
        "papa|La règle dort. Vas-y.",
        "enfant-f|La pomme, s'il te plaît.",
        "narrateur|La pomme entre, loin du sac.",
        "maman|Deux objets, deux places.",
        "narrateur|L'écaille et la pomme partagent une même ombre rayée.",
        "narrateur|Le sac jaune se redresse, sans toucher l'osier.",
    ),
    (1, 3, 3): L(
        "narrateur|La maîtresse veut un fromage, pour le goûter de la classe.",
        "narrateur|Mila veut le même paquet, au même instant.",
        "enfant-f|Moi aussi—",
        "narrateur|Les deux envies se cognent, sans oreille.",
        "narrateur|Mila recule le panier. Elle refuse de foncer.",
        "narrateur|Elle regarde l'écaille d'orange, puis le papier blanc.",
        "enfant-f|Quand le tien est pris, je prends le mien ?",
        "maman|Le sien est pris. Le tien attend.",
        "enfant-f|Le fromage, s'il te plaît.",
        "papa|Deux paquets, deux tours.",
        "narrateur|L'écaille colle au papier de Mila, pas à l'autre.",
        "narrateur|Le sac jaune sent le lait, un instant, puis s'éloigne.",
    ),
    (2, 1, 1): L(
        "narrateur|Sous l'étal, la boulangère a un sachet de pain, dans le tablier.",
        "narrateur|Mila parle pendant que l'aiguille pèse.",
        "enfant-f|Le pain—",
        "narrateur|L'aiguille tremble. Rien n'arrive.",
        "narrateur|Elle refuse de foncer sur la balance.",
        "narrateur|L'écaille d'orange brille, plus sombre, sous la toile.",
        "enfant-f|Le pain, s'il te plaît.",
        "narrateur|Le sachet passe de la poche à l'osier, tiède.",
        "papa|L'aiguille s'est arrêtée. Toi, tu commences.",
        "maman|La croûte sent le four, ici, sous les fruits.",
        "narrateur|Une rayure d'ombre coupe le sachet, puis l'écaille.",
        "narrateur|Deux bandes, l'une toile, l'une pain.",
    ),
    (2, 1, 2): L(
        "narrateur|La boulangère pèse une pomme, l'aiguille capricieuse.",
        "narrateur|Mila avance le panier trop tôt.",
        "narrateur|Le bois touche le plateau. L'aiguille saute.",
        "enfant-f|Pardon.",
        "narrateur|Elle recule. Elle refuse de foncer.",
        "narrateur|Elle fixe l'écaille, puis l'aiguille, sans parler.",
        "papa|L'aiguille est sage. Demande.",
        "enfant-f|La pomme, s'il te plaît.",
        "narrateur|La pomme descend, lourde, lisse, un peu froide.",
        "maman|Le plateau est libre. Ton osier aussi.",
        "narrateur|Une rayure d'ombre coupe l'écaille, sur la pomme.",
        "narrateur|Le point jaune de la peau salue le bateau d'orange.",
    ),
    (2, 1, 3): L(
        "narrateur|Un fromage en papier vert attend, entre les tomates.",
        "narrateur|La boulangère essuie l'aiguille. Mila parle trop tôt.",
        "enfant-f|Celui-là—",
        "narrateur|Le chiffon frotte. Le mot glisse sous l'étal.",
        "narrateur|Mila refuse de foncer.",
        "narrateur|Elle retrouve l'écaille d'orange, au bord de l'osier.",
        "enfant-f|Le fromage, s'il te plaît.",
        "narrateur|Le papier vert craque. Ça sent l'herbe, et le lait.",
        "papa|Le chiffon s'est tu.",
        "maman|Le vert du papier aime les toiles.",
        "narrateur|L'écaille se cache sous le fromage, puis reparaît.",
        "narrateur|Un œil d'orange, entre deux plis.",
    ),
    (2, 2, 1): L(
        "narrateur|Le voisin discute du prix, panier en travers.",
        "narrateur|Un pain dépasse de son osier, trop près.",
        "enfant-f|J'en veux un, moi—",
        "narrateur|Le prix recouvre sa phrase.",
        "narrateur|Mila refuse de tirer le pain du voisin.",
        "narrateur|Elle regarde l'écaille, puis un pain sur l'étal, à elle.",
        "enfant-f|Celui de l'étal, s'il te plaît.",
        "narrateur|Le sachet entre. Le voisin décale enfin.",
        "maman|Le sien reste le sien. Le tien, le tien.",
        "papa|Deux paniers, deux pains, sans mélange.",
        "narrateur|L'écaille glisse dans l'osier, contre la croûte tiède.",
        "narrateur|Le prix s'est tu. Les toiles claquent, plus légères.",
    ),
    (2, 2, 2): L(
        "narrateur|Deux tomates ont choisi. Une pomme reste, ronde.",
        "narrateur|Le voisin la prend en même temps que Mila.",
        "enfant-f|C'est la mienne !",
        "narrateur|Deux mains, une pomme. Rien ne bouge.",
        "narrateur|Mila retire sa main. Elle refuse de foncer.",
        "narrateur|Elle montre l'écaille d'orange, comme un signal.",
        "papa|Il y en a une autre, à côté, plus rouge.",
        "enfant-f|Celle-là, s'il te plaît.",
        "narrateur|La pomme plus rouge entre dans l'osier.",
        "maman|Chacun a la sienne, sans se tirer dessus.",
        "narrateur|L'écaille tremble sur l'anse, et la pomme la regarde.",
        "narrateur|Le voisin part, casquette rayée dans le soleil.",
    ),
    (2, 2, 3): L(
        "narrateur|Le voisin pèse un fromage, voix ronde, trop large.",
        "narrateur|Mila veut le paquet d'à côté, plus petit.",
        "enfant-f|Le petit—",
        "narrateur|La voix ronde recouvre le petit.",
        "narrateur|Elle refuse de foncer dans sa voix.",
        "narrateur|Elle écoute l'étal, puis retrouve l'écaille.",
        "enfant-f|Le petit fromage, s'il te plaît.",
        "narrateur|Le papier blanc entre, frais, sous les toiles.",
        "papa|Sa voix a fini. La tienne a commencé.",
        "maman|Le petit pèse juste, dans l'osier.",
        "narrateur|L'écaille fait un bateau, sur le papier du fromage.",
        "narrateur|Un claquement de toile pousse le bateau, sans le jeter.",
    ),
    (2, 3, 1): L(
        "narrateur|La maîtresse plie le ruban rouge, près des caisses.",
        "narrateur|Mila veut le pain pendant le nœud.",
        "enfant-f|Le pain—",
        "narrateur|Le nœud recouvre le mot.",
        "narrateur|Elle refuse de couper le ruban.",
        "narrateur|L'écaille d'orange attend la fin du nœud.",
        "enfant-f|Le pain, s'il te plaît.",
        "narrateur|Le sachet tiède glisse, loin du ruban.",
        "maman|Le nœud est fait. Ton pain aussi.",
        "papa|Deux gestes, l'un après l'autre.",
        "narrateur|Le sac d'école s'éloigne. L'écaille reste au pain.",
        "narrateur|Une miette colle au ruban, puis tombe sur le pavé.",
    ),
    (2, 3, 2): L(
        "narrateur|Le plaid rayé de maman ressemble aux toiles.",
        "narrateur|La maîtresse le touche, et Mila veut la pomme.",
        "enfant-f|La pomme, là—",
        "narrateur|Le plaid et la pomme se mélangent dans l'air.",
        "narrateur|Mila refuse de foncer.",
        "narrateur|Elle pose le doigt sur l'écaille, puis se tait.",
        "papa|Le plaid est vu. La pomme t'écoute.",
        "enfant-f|La pomme, s'il te plaît.",
        "narrateur|La pomme entre. Le plaid reste sur le bras de maman.",
        "maman|Toiles, plaid, pomme : trois rayures différentes.",
        "narrateur|L'écaille a l'odeur de la pomme, et un peu du plaid.",
        "narrateur|Le sac jaune penche, puis se redresse, sans voler le fruit.",
    ),
    (2, 3, 3): L(
        "narrateur|La maîtresse cherche un fromage, pour le goûter.",
        "narrateur|Le sac jaune cache le paquet que Mila voulait.",
        "enfant-f|Il est dessous !",
        "narrateur|Mila a envie de soulever le sac.",
        "narrateur|Ses mains restent basses.",
        "narrateur|Cette fois, elle refuse de foncer.",
        "narrateur|Le doigt montre l'écaille, puis attend le sac levé.",
        "maman|Le sac est levé. Demande.",
        "enfant-f|Le fromage, s'il te plaît.",
        "narrateur|Le paquet blanc entre, loin du sac.",
        "papa|Deux sacs, deux places.",
        "narrateur|L'écaille colle au fromage, sous une toile qui se tait.",
        "narrateur|Le ruban rouge dort dans le sac, sans parler.",
    ),
    (3, 1, 1): L(
        "narrateur|La boulangère a posé un petit pain, près du lait.",
        "narrateur|Mila parle pendant qu'elle compte les pièces.",
        "enfant-f|Le pain—",
        "narrateur|Les pièces tintent. Le mot se casse contre le métal.",
        "narrateur|Mila refuse de foncer sur le tiroir.",
        "narrateur|Elle guette l'écaille d'orange, sur le marbre d'ombre.",
        "enfant-f|Le pain, s'il te plaît.",
        "narrateur|Le sachet glisse, tiède, sur le froid du marbre.",
        "papa|Les pièces ont fini. Toi, tu commences.",
        "maman|Chaud et froid, dans le même osier.",
        "narrateur|Le marbre froid rend l'écaille plus brillante, près du pain.",
        "narrateur|Un nuage de farine danse, puis se pose.",
    ),
    (3, 1, 2): L(
        "narrateur|Une pomme rouge sert de presse-papier, sur le marbre.",
        "narrateur|La boulangère parle du lait. Mila veut la pomme.",
        "enfant-f|Elle, là—",
        "narrateur|Le lait recouvre le fruit.",
        "narrateur|Mila refuse de foncer.",
        "narrateur|Elle suit l'écaille, puis la pomme, des yeux seulement.",
        "papa|Le lait est dit. La pomme t'écoute.",
        "enfant-f|La pomme, s'il te plaît.",
        "narrateur|La pomme quitte le marbre. Le papier du lait reste.",
        "maman|Le presse-papier a fini son travail.",
        "narrateur|L'écaille glisse vers la pomme, sur le papier blanc.",
        "narrateur|Deux ronds, l'un fruit, l'un orange, dans le froid.",
    ),
    (3, 1, 3): L(
        "narrateur|La boulangère commande le fromage à tartiner.",
        "narrateur|Mila veut un autre, plus petit, à côté.",
        "enfant-f|Le petit—",
        "narrateur|La commande recouvre le petit.",
        "narrateur|Elle refuse de foncer dans le lait.",
        "narrateur|L'écaille d'orange attend, collée à l'osier.",
        "enfant-f|Le petit fromage, s'il te plaît.",
        "narrateur|Le papier blanc entre. Ça sent deux caves.",
        "papa|Le sien est le tartiner. Le tien, le petit.",
        "maman|Deux fromages, sans se marcher dessus.",
        "narrateur|L'écaille et le fromage sentent deux caves différentes.",
        "narrateur|La farine du tablier fait un nuage, puis s'en va.",
    ),
    (3, 2, 1): L(
        "narrateur|Le voisin raconte hier, pain d'hier, fromage d'hier.",
        "narrateur|Un pain tout frais attend, sur le marbre.",
        "enfant-f|Celui-là, le frais—",
        "narrateur|Hier recouvre le présent.",
        "narrateur|Mila refuse de foncer dans le récit.",
        "narrateur|Elle touche l'écaille d'orange, pour revenir ici.",
        "enfant-f|Le pain, s'il te plaît.",
        "narrateur|Le sachet tiède pose une lampe, sur le marbre froid.",
        "maman|Hier s'est tu. Le pain, c'est maintenant.",
        "papa|Ton osier tient le présent.",
        "narrateur|L'écaille vogue sur la croûte, dans un coin d'ombre froide.",
        "narrateur|Le voisin décale enfin son panier trop large.",
    ),
    (3, 2, 2): L(
        "narrateur|Une pomme a roulé sous le panier du voisin, au marbre.",
        "narrateur|Mila veut la ramasser pendant le récit d'hier.",
        "enfant-f|Elle est dessous !",
        "narrateur|Sa phrase se perd sous l'osier du voisin.",
        "narrateur|Elle refuse de foncer pour tirer son panier.",
        "narrateur|Elle montre l'écaille, puis le dessous, sans crier.",
        "papa|Son récit a fini. On soulève ensemble.",
        "enfant-f|La pomme, s'il te plaît.",
        "narrateur|La pomme sort, un peu froide, un peu ronde.",
        "maman|Elle n'a pas disparu sous hier.",
        "narrateur|L'écaille s'arrête contre la pomme, loin du récit.",
        "narrateur|Un rond d'eau du marbre sèche sur l'osier de Mila.",
    ),
    (3, 2, 3): L(
        "narrateur|Le voisin appuie son fromage d'hier, trop fort, trop long.",
        "narrateur|Mila veut le fromage d'ici, plus petit.",
        "enfant-f|Le mien—",
        "narrateur|Hier pèse. Le mien disparaît.",
        "narrateur|Elle refuse de foncer contre son osier.",
        "narrateur|Elle écoute le marbre, puis retrouve l'écaille.",
        "enfant-f|Le fromage d'ici, s'il te plaît.",
        "narrateur|Le papier blanc entre, frais, sans hier.",
        "papa|Le sien reste d'hier. Le tien, c'est maintenant.",
        "maman|Deux temps, deux paquets.",
        "narrateur|L'écaille orne le fromage, comme une médaille minuscule.",
        "narrateur|Le voisin part. Le rond d'eau reste, souvenir.",
    ),
    (3, 3, 1): L(
        "narrateur|La maîtresse parle des pots, un pain dans le sac jaune.",
        "narrateur|Mila veut un pain, le sien, sur le marbre.",
        "enfant-f|Le mien, pas celui du sac—",
        "narrateur|Les pots recouvrent le mien.",
        "narrateur|Elle refuse de foncer dans le jardin des pots.",
        "narrateur|Elle pose un doigt sur l'écaille d'orange.",
        "enfant-f|Le pain du marbre, s'il te plaît.",
        "narrateur|Le sachet du marbre entre, loin du sac.",
        "maman|Les pots ont fini. Ton pain commence.",
        "papa|Deux pains, deux maisons.",
        "narrateur|L'écaille quitte le regard du sac, et choisit le pain.",
        "narrateur|La règle tapote, puis se tait, dans le jaune.",
    ),
    (3, 3, 2): L(
        "narrateur|Une pomme attend près des pots imaginés, sur le marbre.",
        "narrateur|La maîtresse décrit une feuille. Mila veut le fruit.",
        "enfant-f|La pomme—",
        "narrateur|La feuille recouvre le fruit.",
        "narrateur|Mila refuse de foncer dans la feuille.",
        "narrateur|Elle suit l'écaille, du sac jusqu'à la pomme.",
        "papa|La feuille est dite. La pomme t'écoute.",
        "enfant-f|La pomme, s'il te plaît.",
        "narrateur|La pomme entre. La feuille reste dans les mots.",
        "maman|On peut avoir les deux, l'un après l'autre.",
        "narrateur|L'écaille voyage de la toile jusqu'à la pomme, sans bruit.",
        "narrateur|Le sac jaune penche, puis s'éloigne vers la porte.",
    ),
    (3, 3, 3): L(
        "narrateur|La maîtresse prend son fromage de goûter, près du marbre.",
        "narrateur|Mila veut le dernier petit, collé au sien.",
        "enfant-f|Le dernier—",
        "narrateur|Le goûter recouvre le dernier.",
        "narrateur|Elle refuse de foncer sur le sac jaune.",
        "narrateur|Personne ne donne la réponse.",
        "narrateur|Mila observe le panier, écoute le marbre, retrouve l'écaille.",
        "enfant-f|Quand le tien est dans le sac, je prends le mien ?",
        "maman|Le tien attend. Demande.",
        "enfant-f|Le fromage, s'il te plaît.",
        "papa|Le dernier est le tien, entier.",
        "narrateur|L'écaille d'orange a trouvé sa place, dans l'osier plein.",
        "narrateur|Les toiles, dehors, claquent moins fort, comme une oreille.",
    ),
}


def ending(a: int, b: int, c: int) -> list[str]:
    place = {1: "la boulangerie", 2: "l'étal", 3: "la fromagerie"}[a]
    who = {1: "la boulangère", 2: "le voisin", 3: "la maîtresse"}[b]
    food = {1: "le pain", 2: "la pomme", 3: "le fromage"}[c]
    last = {
        (1, 1, 1): "L'écaille d'orange sèche sur le sachet, sous une rayure rouge.",
        (1, 1, 2): "L'écaille colle à la pomme, comme un petit soleil.",
        (1, 1, 3): "L'écaille dort dans le pli du papier, près du fromage.",
        (1, 2, 1): "L'écaille glisse dans l'osier, contre la croûte tiède.",
        (1, 2, 2): "L'écaille tremble sur l'anse, et la pomme la regarde.",
        (1, 2, 3): "L'écaille sent le fromage, et un peu d'orange.",
        (1, 3, 1): "L'écaille voyage sur le pain, sous la toile qui claque.",
        (1, 3, 2): "L'écaille et la pomme partagent une même ombre rayée.",
        (1, 3, 3): "L'écaille reste au bord du papier, comme un ticket.",
        (2, 1, 1): "Sous l'étal, l'écaille brille au fond du panier, près du pain.",
        (2, 1, 2): "Une rayure d'ombre coupe l'écaille, sur la pomme.",
        (2, 1, 3): "L'écaille se cache sous le fromage, puis reparaît.",
        (2, 2, 1): "Le voisin est parti ; l'écaille garde le pain, dans l'osier.",
        (2, 2, 2): "L'écaille et la queue de la pomme se touchent, collées.",
        (2, 2, 3): "L'écaille fait un bateau, sur le papier du fromage.",
        (2, 3, 1): "Le sac jaune s'éloigne ; l'écaille reste au pain.",
        (2, 3, 2): "L'écaille a l'odeur de la pomme, et un peu du plaid.",
        (2, 3, 3): "L'écaille colle au fromage, sous une toile qui se tait.",
        (3, 1, 1): "Le marbre froid rend l'écaille plus brillante, près du pain.",
        (3, 1, 2): "L'écaille glisse vers la pomme, sur le papier blanc.",
        (3, 1, 3): "L'écaille et le fromage sentent deux caves différentes.",
        (3, 2, 1): "L'écaille vogue sur la croûte, dans un coin d'ombre froide.",
        (3, 2, 2): "L'écaille s'arrête contre la pomme, loin du récit d'hier.",
        (3, 2, 3): "L'écaille orne le fromage, comme une médaille minuscule.",
        (3, 3, 1): "L'écaille quitte le sac jaune, et choisit le pain.",
        (3, 3, 2): "L'écaille voyage de la toile jusqu'à la pomme, sans bruit.",
        (3, 3, 3): "L'écaille d'orange a trouvé sa place, dans l'osier plein.",
    }[(a, b, c)]
    hard = {
        (1, 1): "Quand la cloche a parlé trop fort.",
        (1, 2): "Quand le bouton du voisin a recouvert mes mots.",
        (1, 3): "Quand la menthe et la règle se mélangeaient.",
        (2, 1): "Quand l'aiguille de la balance tremblait.",
        (2, 2): "Quand les tomates du voisin étaient trop larges.",
        (2, 3): "Quand le ruban et le plaid prenaient toute la place.",
        (3, 1): "Quand les pièces tintaient sur le marbre.",
        (3, 2): "Quand hier recouvrait le présent.",
        (3, 3): "Quand les pots et le sac jaune parlaient trop.",
    }[(a, b)]
    return L(
        "narrateur|Plus tard, les toiles claquent moins, au-dessus des pavés.",
        "papa|À toi, Mila.",
        "papa|Nous t'écoutons jusqu'au bout.",
        f"enfant-f|J'ai porté le panier {place}.",
        f"enfant-f|J'ai attendu {who}.",
        f"enfant-f|{food.capitalize()} est dedans, avec l'écaille.",
        "maman|Le moment difficile, tu le gardes où ?",
        f"enfant-f|{hard}",
        "narrateur|Mila pose deux doigts sur l'anse rêche.",
        f"narrateur|{last}",
    )


def main() -> None:
    src = json.loads((FOLDER / "source.json").read_text(encoding="utf-8"))
    scripts: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {}
    emph: dict[str, str | None] = {}

    scripts["CHK_T0000_P0000"] = opening()
    sons["CHK_T0000_P0000"] = "toile,osier,caisse"
    emph["CHK_T0000_P0000"] = "écaille d'orange"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|Le panier peut voyager vers trois coins du marché.",
        "papa|La boulangerie, l'étal, ou la fromagerie ?",
        "maman|Où le portes-tu, Mila ?",
    )
    extras["CHK_T0001_P0000"] = t3("la boulangerie", "l'étal", "la fromagerie")
    sons["CHK_T0001_P0000"] = ""

    for a in (1, 2, 3):
        p = f"CHK_T0001_P000{a}"
        scripts[p] = T1_PASS[a]
        sons[p] = PLACES[a]["son"]
        q_lines, ans, acc, retry, ok, near, emp = T1_Q[a]
        scripts[f"{p}_Q0001"] = q_lines
        extras[f"{p}_Q0001"] = qf(ans, acc, retry, ok, near)
        emph[f"{p}_Q0001"] = emp
        sons[f"{p}_Q0001"] = ""
        scripts[f"{p}_C0001"] = T1_C[a]
        sons[f"{p}_C0001"] = PLACES[a]["son"]
        scripts[f"{p}_T0002_P0000"] = T2_CHOICE[a]
        extras[f"{p}_T0002_P0000"] = t3("la boulangère", "le voisin", "la maîtresse")
        sons[f"{p}_T0002_P0000"] = ""
        for b in (1, 2, 3):
            pb = f"{p}_T0002_P000{b}"
            scripts[pb] = T2_PASS[(a, b)]
            sons[pb] = PEOPLE[b]["son"]
            scripts[f"{pb}_T0003_P0000"] = t3_choice(a, b)
            extras[f"{pb}_T0003_P0000"] = t3("le pain", "une pomme", "un fromage")
            sons[f"{pb}_T0003_P0000"] = ""
            for c in (1, 2, 3):
                pc = f"{pb}_T0003_P000{c}"
                scripts[pc] = T3_PASS[(a, b, c)]
                sons[pc] = FOODS[c]["son"]
                fid = f"{pc}_F0001"
                scripts[fid] = ending(a, b, c)
                sons[fid] = "toile," + FOODS[c]["son"]
                emph[fid] = "écaille d'orange"

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        prof = profile_for(cid, kind)
        by[cid] = pack_chunk(
            c,
            scripts[cid],
            prof,
            emphasis=emph.get(cid, PROFILES[prof]["emphasis"]),
            sons=sons.get(cid, c.get("sons") or ""),
            extra=extras.get(cid),
        )

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["age_band"] = "N3"
    out["lesson_id"] = "COL.POL.001"
    out["kind"] = "ramifiee"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]

    check(SID, out["age_band"], out["chunks"])

    ends = [c["text"] for c in out["chunks"] if c["kind"] == "passage_fin"]
    if len(ends) != 27 or len(set(ends)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(ends))}/{len(ends)}")
    lasts = []
    for c in out["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        nlines = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(nlines[-1])
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images: {len(set(lasts))}/27")

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for tic in (
        "tout doux", "tout calme", "on lève la main", "puis on parle",
        "on va apprendre", "mission accomplie", "j'ai compris !",
        "aujourd'hui,", "couleur de miel", "merle",
    ):
        if tic in blob:
            raise SystemExit(f"tic: {tic}")
    for name in ("léa", "tom ", "sami", "marceau", "maëlys", "raphaël"):
        if name in blob:
            raise SystemExit(f"nom: {name}")
    for bad in (
        "croissant d'eau", "grain de sel", "grain de paprika",
        "grain de cannelle", "ancre",
    ):
        if bad in blob:
            raise SystemExit(f"indice interdit: {bad}")
    if "écaille d'orange" not in blob:
        raise SystemExit("manque écaille d'orange")
    if blob.count("merci") < 1:
        raise SystemExit("manque merci")

    paths = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
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
                n = sum(words(by[i]["text"]) for i in ids)
                paths.append(n)
    print(f"chemins {min(paths)}–{max(paths)} mots, moy {sum(paths)//len(paths)}")

    (FOLDER / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    relect = f"""# {SID} — {TITLE}

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Vécu

Marché du village, toiles rayées comme des voiles, panier d'osier à l'anse rêche. Mila veut porter le panier jusqu'au bout des étals, avant que les toiles se plient. Indice unique : une **écaille d'orange** collée à une rayure, puis posée sur l'anse. Première idée : tirer sans attendre. Le panier penche, personne n'entend, le sourire disparaît. Papa s'accroupit. Un merci vécu : attendre la phrase. T1 boulangerie / étal / fromagerie : le panier part **avec**. T2 boulangère / voisin / maîtresse : labels conservés, adultes parlants = papa/maman (maîtresse narrée, pas de leçon). T3 pain / pomme / fromage : deuxième ruse, Mila refuse de foncer, retrouve l'écaille. COL.POL.001 vécue (tours : envie de couper, retenue, écoute, plaisir d'être entendue), jamais dite. 27 fins distinctes, chacune paie l'écaille.

## Vu et corrigé

- Titre noyau conservé. N3 ≤ 16. Troupe D16 : Mila, papa, maman.
- Ouverture inventée (ombre à rayures), pas un gabarit v2.
- Labels T1/T2/T3 conservés. Contenu refait. Ancien merged (trois mots récités) écarté.
- Monde distinct de TREE-COL-022 (Nina, grain de sel), TREE-COL-035 (Raphaël, croissant d'eau, store goutteux), TREE-AUT-045 (paprika), TREE-DIF-008 (cannelle).
- Questions T1 : cloche / caisse / papier (pas « bonjour » en leçon).
- Un merci vécu (papa, après la phrase achevée). Une question d'adulte. `en ce moment`.
- Pas de refrain bonjour / s'il te plaît / merci. Pas de merle, miel, encore / déjà / tout doux.
- 27 fins textuellement distinctes (dernière image narrateur unique).
- TTS par chunk (opening / choice / clue / confirm / action / obstacle / resolution / ending).
- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés. Pas apply.
- Chemins : {min(paths)}–{max(paths)} mots (moy {sum(paths)//len(paths)}).

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'`apply`.
"""
    (FOLDER / "RELECTURE.md").write_text(relect, encoding="utf-8")
    print("wrote merged.json + RELECTURE.md")


if __name__ == "__main__":
    main()
