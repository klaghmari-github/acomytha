#!/usr/bin/env python3
"""TREE-AUT-019 — Le bidon de lait de Sarah (F-NAR-019, N1, AUT.ROU.001, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-019"
N1 = LIMITS["N1"]
TITLE = "Le bidon de lait de Sarah"
TICS = re.compile(
    r"\b(tout doux|tout calme|encore|déjà|deja|une étape après l'autre)\b",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="bidon",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_lait_chaud_attend_les_bols; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="bidon",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=une_chose_le_bidon; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="bidon",
        note="arc=confirmation; intention=relancer; emotion=élan; intensite=1; destinataire=enfant; sous_texte=le_banc_reprend_le_bidon; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=deux_envies_en_même_temps; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=le_lait_bascule; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="bidon",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=la_paille_sort_puis_le_lait; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="bidon",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_dent_garde_une_trace; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    prev = ""
    run = 1
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
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        tok = ph.split()[0].lower() if role == "narrateur" else ""
        if tok and tok == prev:
            run += 1
            if run >= 4:
                raise SystemExit(f"puces {tok}: {ph}")
        else:
            run = 1
        prev = tok
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
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=la_dent_garde_la_trace_du_brin; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


Q_FIELDS = {
    "expected_answer": "une chose",
    "accepted_examples": (
        "une chose | puis l'autre | d'abord | une chose puis l'autre | "
        "puis la suivante | le bidon | le lait | le banc"
    ),
    "retry_prompt": "Elle fait une chose, puis l'autre. Comment ?",
    "engine_ok_text": "Oui, une chose.",
    "engine_near_text": "Tu es près. Écoute l'indice.",
}


OPENING = vet(
    [
        "narrateur|La cuisine de pierre sent le pain.",
        "narrateur|Une lucarne pose un rond jaune.",
        "narrateur|Sarah vit ici, avec papa et maman.",
        "narrateur|Nino est venu, les joues roses.",
        "narrateur|Papa pose le bidon crème sur le banc.",
        "narrateur|L'anse de cuivre sonne ding.",
        "narrateur|Le bidon a une dent, sur le flanc.",
        "narrateur|Un brin de paille dort dans la dent.",
        "narrateur|Ça sent le lait chaud, sous le couvercle.",
        "narrateur|Le pain dore, dans le four.",
        "narrateur|En ce moment, Sarah veut verser.",
        "enfant-f|Je verse, et on boit !",
        "narrateur|Nino tire vers la porte, impatient.",
        "enfant-m|On joue dehors, tout de suite !",
        "narrateur|Sarah prend le bidon et la main de Nino.",
        "narrateur|Le lait bascule, lourd, contre le flanc.",
        "narrateur|Le couvercle cliquette, de travers.",
        "narrateur|Une goutte tombe sur la pierre froide.",
        "enfant-f|Oh, il se sauve !",
        "narrateur|Sarah baisse les épaules, le bidon trop lourd.",
        "papa|Le banc de la laiterie, d'abord ?",
        "maman|Tu verses, ou tu cours, Sarah ?",
        "papa|Le pain va sortir, tout chaud.",
        "narrateur|Nino tape du pied, près du seuil.",
        "enfant-m|Moi, je veux le dehors !",
        "enfant-f|Moi, le lait, dans les bols !",
        "maman|Le bidon reste avec nous.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|Nino veut jouer, Sarah veut le lait.",
        "narrateur|Le bac à sable.",
        "narrateur|Le toboggan.",
        "narrateur|Les balançoires.",
        "maman|Nino joue où, après le lait ?",
    ]
)

T1 = {
    1: vet(
        [
            "narrateur|Nino court vers le bac à sable.",
            "narrateur|Le sable est pâle, un peu frais.",
            "narrateur|Il glisse entre les doigts, chh.",
            "enfant-m|Viens, Sarah !",
            "enfant-m|On creuse !",
            "narrateur|Sarah suit, le bidon contre elle.",
            "narrateur|Elle pose un genou, et le bidon.",
            "narrateur|La dent s'enfonce dans le sable mou.",
            "narrateur|Le couvercle penche, et cliquette.",
            "enfant-f|Il ne reste pas droit !",
            "narrateur|Elle tire le bidon, trop vite.",
            "narrateur|Une autre goutte mouille le sable.",
            "narrateur|Sarah souffle, les épaules basses.",
            "papa|Deux mains, sous le bidon.",
            "narrateur|Papa le soulève, sans le vider.",
            "maman|Les bols attendent, à la laiterie.",
            "enfant-f|Je veux le sable, et le lait !",
            "papa|Une chose, le bidon sur le banc.",
            "narrateur|Un grain de sable colle à la dent.",
            "narrateur|La poule picore, loin du bac.",
        ]
    ),
    2: vet(
        [
            "narrateur|Nino grimpe vers le toboggan.",
            "narrateur|Le métal est froid sous la paume.",
            "narrateur|Les marches font toc, toc.",
            "enfant-m|Je glisse, Sarah !",
            "enfant-m|Viens !",
            "narrateur|Sarah monte, le bidon contre l'épaule.",
            "narrateur|Le couvercle frotte une marche, cling.",
            "narrateur|Le lait penche, trop près du bord.",
            "enfant-f|Il va tomber !",
            "narrateur|Elle recule, un pied trop vite.",
            "narrateur|Une feuille colle à l'anse de cuivre.",
            "narrateur|Sarah serre les dents, déçue.",
            "papa|Le bidon n'aime pas les marches.",
            "maman|Tes pieds d'abord, puis le lait.",
            "enfant-f|Je veux glisser, et verser !",
            "papa|Une chose, le bidon sur le banc.",
            "narrateur|La feuille tremble, sur l'anse.",
            "narrateur|Le métal se tait, un instant.",
            "narrateur|Nino reste en haut, impatient.",
            "narrateur|Sarah garde le bidon, trop lourd.",
        ]
    ),
    3: vet(
        [
            "narrateur|Nino court vers les balançoires.",
            "narrateur|La corde est un peu rêche.",
            "narrateur|Le siège est lisse, un peu froid.",
            "enfant-m|Pousse-moi, Sarah !",
            "narrateur|Sarah tient le bidon, et la corde.",
            "narrateur|L'anse de cuivre tape le bois, ding.",
            "narrateur|Le lait danse, contre le couvercle.",
            "enfant-f|Mes deux mains ne suffisent pas !",
            "narrateur|Elle lâche la corde, trop tard.",
            "narrateur|Le siège part, et le bidon penche.",
            "narrateur|Une goutte file le long de la dent.",
            "narrateur|Sarah cligne des yeux, les bras lourds.",
            "papa|Une main pour le bidon, pas deux jeux.",
            "maman|La corde attend, le lait aussi.",
            "enfant-f|Je veux pousser, et verser !",
            "papa|Une chose, le bidon sur le banc.",
            "narrateur|La corde fait cling, puis se tait.",
            "narrateur|Le vent touche son nez, froid.",
        ]
    ),
}

T1_Q = {
    1: vet(
        [
            "narrateur|Sarah a le sable, et le bidon.",
            "maman|Elle fait comment ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Sarah a les marches, et le bidon.",
            "papa|Elle fait comment ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Sarah a la corde, et le bidon.",
            "maman|Elle fait comment ?",
        ]
    ),
}

T1_C = {
    1: vet(
        [
            "narrateur|Sarah pose le bidon sur le banc.",
            "papa|Une chose, Sarah.",
            "enfant-f|Après, le sable.",
            "maman|Merci, Sarah.",
            "narrateur|Nino souffle, mais il attend.",
            "narrateur|Un grain reste sur sa joue.",
            "narrateur|Le bidon tient, droit, sur la pierre.",
            "enfant-m|D'accord, le lait d'abord.",
        ]
    ),
    2: vet(
        [
            "narrateur|Sarah redescend, le bidon contre elle.",
            "papa|Une chose, les pieds par terre.",
            "enfant-f|Les bottes, puis le lait.",
            "maman|Bravo, Sarah.",
            "narrateur|Une feuille de rampe bouge.",
            "narrateur|Le bidon brille, à la laiterie.",
            "enfant-m|D'accord, je descends.",
            "narrateur|Nino pose les deux pieds, enfin.",
        ]
    ),
    3: vet(
        [
            "narrateur|Sarah pose un pied au sol.",
            "maman|Une chose, puis le bol.",
            "enfant-f|Ensuite le lait, dans le bol.",
            "papa|Oui, tes mains sont prêtes.",
            "narrateur|La corde retombe, sans bruit.",
            "narrateur|Le bidon attend près de la pierre.",
            "enfant-m|D'accord, je lâche la corde.",
        ]
    ),
}

T2_CHOICE = {
    1: vet(
        [
            "narrateur|Nino veut un jeu, près du bac.",
            "narrateur|Le ballon.",
            "narrateur|Le seau.",
            "narrateur|Le doudou.",
            "papa|Tu prends quel jeu, Nino ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Nino veut un jeu, près des marches.",
            "narrateur|Le ballon.",
            "narrateur|Le seau.",
            "narrateur|Le doudou.",
            "maman|Tu prends quel jeu, Nino ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Nino veut un jeu, près des cordes.",
            "narrateur|Le ballon.",
            "narrateur|Le seau.",
            "narrateur|Le doudou.",
            "papa|Tu prends quel jeu, Nino ?",
        ]
    ),
}


def t2_scene(a: int, b: int) -> list[str]:
    hip = {
        1: "Près du bac, le bidon attend sur le banc.",
        2: "Près des marches, le bidon luit, trop plein.",
        3: "Près des cordes, le bidon tient, un peu penché.",
    }[a]
    bodies = {
        (1, 1): [
            f"narrateur|{hip}",
            "narrateur|Nino saisit le ballon rouge, souple.",
            "enfant-m|Il vient avec nous !",
            "narrateur|Le ballon bondit, trop près du flanc.",
            "narrateur|Il tape l'anse de cuivre, ding.",
            "narrateur|Un filet de lait fuit, tout mince.",
            "enfant-f|Le couvercle est fermé, pourtant !",
            "maman|Regarde la dent, Sarah.",
            "narrateur|Sarah voit le brin, coincé, secret.",
            "papa|Le lait fuit par là, tout bas.",
            "enfant-m|Moi, je veux jouer au ballon !",
            "enfant-f|Moi, je veux fermer le bidon !",
            "narrateur|Le grain de sable brille, dans la dent.",
            "narrateur|Sarah serre l'anse, sans courir.",
        ],
        (1, 2): [
            f"narrateur|{hip}",
            "narrateur|Nino soulève le seau bleu, l'anse froide.",
            "enfant-m|On met le lait dedans !",
            "narrateur|Il penche le seau sous le bidon.",
            "narrateur|Sarah tire le bidon, trop vite.",
            "narrateur|Un filet de lait fuit, tout mince.",
            "enfant-f|Le seau n'est pas un bol !",
            "papa|Le seau pose le bidon, s'il est droit.",
            "narrateur|Sarah voit le brin, coincé, secret.",
            "maman|La dent cache quelque chose, là.",
            "enfant-m|Moi, je veux le seau de sable !",
            "enfant-f|Moi, je veux les bols !",
            "narrateur|Du sable fin dort au fond du seau.",
            "narrateur|Sarah pose le seau, sans verser.",
        ],
        (1, 3): [
            f"narrateur|{hip}",
            "narrateur|Nino serre le doudou gris, l'oreille molle.",
            "enfant-m|Il a soif, lui aussi !",
            "narrateur|Il tend le doudou sous le couvercle.",
            "narrateur|Sarah recule le bidon, trop vite.",
            "narrateur|Un filet de lait fuit, tout mince.",
            "enfant-f|Le doudou n'est pas un bol !",
            "maman|Le doudou peut caler la dent, après.",
            "narrateur|Sarah voit le brin, coincé, secret.",
            "papa|Un brin tient le couvercle, de travers.",
            "enfant-m|Moi, je veux nourrir mon doudou !",
            "enfant-f|Moi, je veux les bols !",
            "narrateur|Un peu de sable colle à l'oreille.",
            "narrateur|Sarah pose le doudou sur la chaise.",
        ],
        (2, 1): [
            f"narrateur|{hip}",
            "narrateur|Nino prend le ballon rouge, un peu froid.",
            "enfant-m|Il glisse avec moi !",
            "narrateur|Le ballon roule sur une marche, toc.",
            "narrateur|Il heurte le bidon, trop près.",
            "narrateur|Un filet de lait fuit, tout mince.",
            "enfant-f|Le couvercle est fermé, pourtant !",
            "papa|Regarde la dent, sous l'anse.",
            "narrateur|Sarah voit le brin, coincé, secret.",
            "maman|La feuille de la rampe tremble aussi.",
            "enfant-m|Moi, je veux le toboggan !",
            "enfant-f|Moi, je veux fermer le lait !",
            "narrateur|Une feuille jaune colle au ballon.",
            "narrateur|Sarah rattrape le ballon, sans verser.",
        ],
        (2, 2): [
            f"narrateur|{hip}",
            "narrateur|Nino met le seau bleu sur sa tête.",
            "enfant-m|C'est mon casque, pour glisser !",
            "narrateur|Il veut le bidon, comme un second seau.",
            "narrateur|Sarah le retient, trop près des marches.",
            "narrateur|Un filet de lait fuit, tout mince.",
            "enfant-f|Le bidon n'est pas un casque !",
            "papa|Le seau peut tenir le bidon, droit.",
            "narrateur|Sarah voit le brin, coincé, secret.",
            "maman|La dent cache le brin, sous le couvercle.",
            "enfant-m|Moi, je veux glisser avec le seau !",
            "enfant-f|Moi, je veux les bols !",
            "narrateur|Sarah pose le seau au bas des marches.",
        ],
        (2, 3): [
            f"narrateur|{hip}",
            "narrateur|Nino pose le doudou sur une marche.",
            "enfant-m|Il glisse, lui aussi !",
            "narrateur|Il veut le bidon, juste derrière.",
            "narrateur|Sarah recule, le métal trop froid.",
            "narrateur|Un filet de lait fuit, tout mince.",
            "enfant-f|Le doudou n'est pas un bol !",
            "maman|Le doudou peut caler le flanc, après.",
            "narrateur|Sarah voit le brin, coincé, secret.",
            "papa|Un brin tient le couvercle, de travers.",
            "enfant-m|Moi, je veux le doudou sur la rampe !",
            "enfant-f|Moi, je veux verser !",
            "narrateur|L'oreille molle dépasse près de la rampe.",
            "narrateur|Sarah reprend le doudou, sans glisser.",
        ],
        (3, 1): [
            f"narrateur|{hip}",
            "narrateur|Nino pousse le ballon sous le siège.",
            "enfant-m|Pousse-moi, et le ballon !",
            "narrateur|Sarah tient le bidon, trop occupée.",
            "narrateur|Le ballon tape l'anse, ding.",
            "narrateur|Un filet de lait fuit, tout mince.",
            "enfant-f|Le couvercle est fermé, pourtant !",
            "papa|Regarde la dent, Sarah.",
            "narrateur|Sarah voit le brin, coincé, secret.",
            "maman|La corde peut attendre, une minute.",
            "enfant-m|Moi, je veux la balançoire !",
            "enfant-f|Moi, je veux le lait dans les bols !",
            "narrateur|Un brin d'herbe colle au ballon.",
            "narrateur|Sarah pose le ballon, loin de l'anse.",
        ],
        (3, 2): [
            f"narrateur|{hip}",
            "narrateur|Nino pose le seau bleu sur le siège.",
            "enfant-m|Le bidon s'assoit, à côté !",
            "narrateur|Sarah refuse, le bidon trop lourd.",
            "narrateur|Le seau bascule, et frotte le flanc.",
            "narrateur|Un filet de lait fuit, tout mince.",
            "enfant-f|Le seau n'est pas un siège !",
            "papa|Le seau peut caler le bidon, au sol.",
            "narrateur|Sarah voit le brin, coincé, secret.",
            "maman|La dent cache le brin, sous le couvercle.",
            "enfant-m|Moi, je veux le seau sur la corde !",
            "enfant-f|Moi, je veux verser !",
            "narrateur|Sarah pose le seau au pied du bois.",
        ],
        (3, 3): [
            f"narrateur|{hip}",
            "narrateur|Nino installe le doudou sur le siège.",
            "enfant-m|Il se balance, et il boit !",
            "narrateur|Il tend le doudou vers le bidon.",
            "narrateur|Sarah recule, la corde trop près.",
            "narrateur|Un filet de lait fuit, tout mince.",
            "enfant-f|Le doudou n'est pas un bol !",
            "maman|Le doudou peut caler la dent, après.",
            "narrateur|Sarah voit le brin, coincé, secret.",
            "papa|Un brin tient le couvercle, de travers.",
            "enfant-m|Moi, je veux pousser le doudou !",
            "enfant-f|Moi, je veux les bols !",
            "narrateur|L'oreille grise pend, près de la corde.",
            "narrateur|Sarah pose le doudou, loin du bois.",
        ],
    }
    return vet(bodies[(a, b)])


T3_CHOICE = {
    1: vet(
        [
            "narrateur|Quelqu'un attend, près du lait chaud.",
            "narrateur|Le veau.",
            "narrateur|La poule.",
            "narrateur|Ou le chat.",
            "papa|Qui attend Sarah, près du lait ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Un ami de la ferme s'approche, curieux.",
            "narrateur|Le veau.",
            "narrateur|La poule.",
            "narrateur|Ou le chat.",
            "maman|Qui attend Sarah, près du lait ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Un souffle chaud passe, près du banc.",
            "narrateur|Le veau.",
            "narrateur|La poule.",
            "narrateur|Ou le chat.",
            "papa|Qui attend Sarah, près du lait ?",
        ]
    ),
}


def res(a: int, b: int, c: int) -> list[str]:
    """27 ruses distinctes : lieu × jouet × animal."""
    place_bit = {
        1: "Un grain de sable brille dans la dent.",
        2: "La feuille de la rampe tremble, sur l'anse.",
        3: "Un cling lointain reste dans l'air.",
    }[a]
    toy_ruse = {
        1: [
            "narrateur|Sarah cale le ballon contre le flanc.",
            "narrateur|Le bidon ne peut plus rouler.",
        ],
        2: [
            "narrateur|Sarah pose le bidon dans le seau.",
            "narrateur|Le seau le tient, droit, sans bouger.",
        ],
        3: [
            "narrateur|Sarah glisse le doudou sous la dent.",
            "narrateur|Le doudou cale le flanc, tout net.",
        ],
    }[b]
    # "tout net" is not tout doux/calme — OK
    animal = {
        1: [
            "narrateur|Le veau attend près de la porte.",
            "narrateur|Son souffle est chaud, sur la pierre.",
            "enfant-m|Il a faim, papa ?",
            "enfant-f|Les bols d'abord, pas lui.",
            "narrateur|Le nez du veau touche la dent.",
            "narrateur|Le brin de paille bouge, enfin visible.",
        ],
        2: [
            "narrateur|La poule picore près de la pierre.",
            "narrateur|Ses pas font tic, tout secs.",
            "enfant-m|Elle veut un grain.",
            "enfant-f|Pas le lait, poule !",
            "narrateur|Elle pique le brin, dans la dent.",
            "narrateur|Le brin de paille sort, tout droit.",
        ],
        3: [
            "narrateur|Le chat est sur la pierre froide.",
            "narrateur|Sa gorge fait ronron, tout bas.",
            "enfant-m|Il a chaud, maman.",
            "enfant-f|Pas sur le bidon, chat !",
            "narrateur|Une patte tape le brin, dans la dent.",
            "narrateur|Le brin de paille roule, sur le banc.",
        ],
    }[c]
    pull = {
        1: "narrateur|Sarah tire le brin, sans verser.",
        2: "narrateur|Sarah souffle le brin, tout loin.",
        3: "narrateur|Sarah pince le brin, et le pose.",
    }[c]
    pours = {
        1: {
            1: "Elle verse au bol, le ballon en garde.",
            2: "Elle verse au bol, le seau autour.",
            3: "Elle verse au bol, le doudou dessous.",
        },
        2: {
            1: "Elle verse au bol, loin des marches.",
            2: "Elle verse au bol, le seau comme nid.",
            3: "Elle verse au bol, le doudou au chaud.",
        },
        3: {
            1: "Elle verse au bol, loin de la corde.",
            2: "Elle verse au bol, le seau au pied.",
            3: "Elle verse au bol, le doudou à côté.",
        },
    }[a][b]
    child_ok = {
        1: "enfant-m|Le veau peut regarder, sans boire.",
        2: "enfant-m|La poule a son grain, plus loin.",
        3: "enfant-m|Le chat a sa pierre, au chaud.",
    }[c]
    lines = [
        *animal,
        "enfant-f|Le brin, c'était lui !",
        pull,
        *toy_ruse,
        f"narrateur|{pours}",
        "enfant-f|C'est chaud.",
        "papa|Tu as fait une chose, puis l'autre.",
        child_ok,
        f"narrateur|{place_bit}",
        "narrateur|Le couvercle tient, sans fuites.",
    ]
    return vet(lines)


def fin(a: int, b: int, c: int) -> list[str]:
    starts = [
        "Sarah a le lait chaud dans le ventre.",
        "Voilà le bol vide, près du bidon.",
        "Contre la pierre, le bidon ne fait plus ding.",
        "Au chaud, Sarah respire, plus légère.",
        "Près de la porte, le lait est fini.",
        "Sous la lampe, le bol brille, vide.",
        "Dans ses mains, le jouet est prêt.",
        "Enfin le lait est là, tout bu.",
        "Voilà le bol vide, près du pain.",
        "Sarah essuie une moustache de lait.",
        "Nino boit, lui aussi, sans courir.",
        "Le four ouvre, et le pain sent bon.",
        "Une croûte chaude attend, sur la table.",
        "Sarah pose le bidon, plus léger.",
        "L'anse de cuivre se tait, vide.",
        "Le rond jaune de la lucarne a bougé.",
        "Maman coupe le pain, tout chaud.",
        "Papa range le couvercle, net.",
        "Sarah lèche une goutte, sur sa lèvre.",
        "Nino a une miette, au coin.",
        "Le banc de la laiterie est libre.",
        "La pierre garde un rond de lait, minuscule.",
        "Sarah range le brin, sur le rebord.",
        "Nino tend son bol, vide, fier.",
        "Le lait n'est plus dans le bidon.",
        "Sarah touche la dent, sans paille.",
        "Le silence de la cuisine est doux.",
    ]
    first = starts[(a - 1) * 9 + (b - 1) * 3 + (c - 1)]
    toy_fin = {
        1: "Voilà le ballon, près d'elle.",
        2: "Voilà le seau, près des bottes.",
        3: "Contre Sarah, le doudou est au chaud.",
    }[b]
    place_go = {
        1: "enfant-f|Le bac, maman.",
        2: "enfant-f|Le toboggan, maman.",
        3: "enfant-f|Les balançoires, maman.",
    }[a]
    adult = {
        1: "maman|Oui, on y va, maintenant.",
        2: "papa|Oui, tes pieds sont prêts.",
        3: "maman|Oui, la corde t'attend.",
    }[c]
    place_fin = {
        1: "Un grain reste sous l'ongle de Sarah.",
        2: "Une feuille colle sur la rampe.",
        3: "La corde ne fait plus cling.",
    }[a]
    animal_fin = {
        1: "Le veau referme les yeux, près de la porte.",
        2: "La poule picore, plus loin, sans le lait.",
        3: "Le chat s'endort, près du bidon vide.",
    }[c]
    traces = {
        (1, 1, 1): "Un grain de sable colle au ballon rouge.",
        (1, 1, 2): "Une miette de pain reste au bord du ballon.",
        (1, 1, 3): "Un poil de chat reste sur le ballon.",
        (1, 2, 1): "Du sable fin brille dans le seau.",
        (1, 2, 2): "L'anse du seau touche le bidon, un instant.",
        (1, 2, 3): "Un grain minuscule roule au fond du seau.",
        (1, 3, 1): "L'oreille grise a un peu de sable.",
        (1, 3, 2): "Du lait chaud a touché le doudou.",
        (1, 3, 3): "Un fil gris pend près du bol.",
        (2, 1, 1): "Près de la rampe, le ballon est un peu froid.",
        (2, 1, 2): "Une feuille jaune colle au ballon.",
        (2, 1, 3): "Le ballon rouge a vu le veau.",
        (2, 2, 1): "Contre une marche, le seau sonne toc.",
        (2, 2, 2): "Près du seau, le métal du toboggan se tait.",
        (2, 2, 3): "Une goutte de lait brille dans le seau.",
        (2, 3, 1): "Le doudou gris a vu le toboggan.",
        (2, 3, 2): "L'oreille molle dépasse près de la rampe.",
        (2, 3, 3): "La rampe brille, loin du doudou.",
        (3, 1, 1): "Un brin d'herbe colle au ballon.",
        (3, 1, 2): "La chaîne a fait cling, près du ballon.",
        (3, 1, 3): "Le chat a touché le ballon, sans bruit.",
        (3, 2, 1): "L'anse du seau est froide, près de la corde.",
        (3, 2, 2): "Un cling lointain, et le seau.",
        (3, 2, 3): "Près du chat, le seau pose son ombre.",
        (3, 3, 1): "Le doudou a senti le vent de la corde.",
        (3, 3, 2): "La corde se tait, près du doudou.",
        (3, 3, 3): "L'oreille grise dépasse près du chat.",
    }
    lasts = {
        (1, 1, 1): "La dent du bidon garde un grain, secret.",
        (1, 1, 2): "Le rond jaune luit sur le ballon vide.",
        (1, 1, 3): "Un poil reste, et le ding s'est tu.",
        (1, 2, 1): "Le seau porte un peu de sable, et de lait.",
        (1, 2, 2): "L'anse de cuivre touche l'anse du seau.",
        (1, 2, 3): "Un grain roule, puis le silence.",
        (1, 3, 1): "L'oreille du doudou sent le bac, pâle.",
        (1, 3, 2): "Une tache de lait sèche sur le tissu.",
        (1, 3, 3): "Le fil gris pend, et le four se tait.",
        (2, 1, 1): "Le ballon froid garde une goutte, minuscule.",
        (2, 1, 2): "La feuille jaune voyage, collée au cuir.",
        (2, 1, 3): "Le veau a vu le rouge, puis s'endort.",
        (2, 2, 1): "Le toc du seau reste dans la rampe.",
        (2, 2, 2): "Le métal se tait, le bidon aussi.",
        (2, 2, 3): "Une goutte brille, puis s'éteint.",
        (2, 3, 1): "Le doudou a la rampe dans l'oreille.",
        (2, 3, 2): "L'oreille molle garde un peu de froid.",
        (2, 3, 3): "La rampe luit, vide, loin du tissu.",
        (3, 1, 1): "L'herbe au ballon sent le pré, tout près.",
        (3, 1, 2): "Le cling s'en va, avec le ballon.",
        (3, 1, 3): "Le chat a laissé sa chaleur au cuir.",
        (3, 2, 1): "L'anse froide a touché la corde, un instant.",
        (3, 2, 2): "Le seau garde le cling, tout au fond.",
        (3, 2, 3): "L'ombre du seau dort, près du chat.",
        (3, 3, 1): "Le doudou a le vent de la corde, dedans.",
        (3, 3, 2): "La corde et le doudou se taisent, ensemble.",
        (3, 3, 3): "L'oreille grise veille, près du chat endormi.",
    }
    souvenir = {
        1: "Sarah garde le geste : poser, puis verser.",
        2: "Nino a attendu, les deux pieds au sol.",
        3: "Sarah pose le brin, sur le rebord.",
    }[c]
    pain = {
        1: "Ça sent le pain du four, tout près.",
        2: "Une odeur de pain chaud entre, tout près.",
        3: "Le four sent bon, tout près.",
    }[a]
    return vet(
        [
            f"narrateur|{first}",
            f"narrateur|{toy_fin}",
            place_go,
            adult,
            f"narrateur|{place_fin}",
            f"narrateur|{traces[(a, b, c)]}",
            f"narrateur|{animal_fin}",
            f"narrateur|{pain}",
            f"narrateur|{souvenir}",
            "enfant-f|Le bidon a fini, Nino.",
            "enfant-m|On peut jouer, maintenant.",
            f"narrateur|{lasts[(a, b, c)]}",
        ]
    )


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple] = {}

    scripts["CHK_T0000_P0000"] = (
        OPENING,
        "opening",
        "bidon,pain",
        {"emphasis": "bidon"},
    )
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "le bac à sable",
            "option_2_label": "le toboggan",
            "option_3_label": "les balançoires",
        },
    )

    t1_sons = {1: "sable,poule", 2: "metal,feuille", 3: "corde,vent"}
    t2_sons = {1: "ballon,lait", 2: "seau,lait", 3: "doudou,lait"}
    t3_sons = {1: "veau,lait", 2: "poule,lait", 3: "chat,lait"}
    t2_emp = {1: "ballon", 2: "seau", 3: "doudou"}
    t3_emp = {1: "veau", 2: "poule", 3: "chat"}

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        scripts[base] = (T1[a], "obstacle", t1_sons[a], {"emphasis": "bidon"})
        scripts[f"{base}_Q0001"] = (T1_Q[a], "clue", "", dict(Q_FIELDS))
        scripts[f"{base}_C0001"] = (T1_C[a], "confirm", "", {"emphasis": "bidon"})
        scripts[f"{base}_T0002_P0000"] = (
            T2_CHOICE[a],
            "choice",
            "",
            {
                "option_1_label": "le ballon",
                "option_2_label": "le seau",
                "option_3_label": "le doudou",
            },
        )
        for b in (1, 2, 3):
            leaf2 = f"{base}_T0002_P000{b}"
            scripts[leaf2] = (
                t2_scene(a, b),
                "obstacle",
                t2_sons[b],
                {"emphasis": t2_emp[b]},
            )
            scripts[f"{leaf2}_T0003_P0000"] = (
                T3_CHOICE[b],
                "choice",
                "",
                {
                    "option_1_label": "le veau",
                    "option_2_label": "la poule",
                    "option_3_label": "le chat",
                },
            )
            for c in (1, 2, 3):
                leaf3 = f"{leaf2}_T0003_P000{c}"
                scripts[leaf3] = (
                    res(a, b, c),
                    "resolution",
                    t3_sons[c],
                    {"emphasis": t3_emp[c]},
                )
                scripts[f"{leaf3}_F0001"] = (
                    fin(a, b, c),
                    "ending",
                    "lait,pain",
                    {"emphasis": "bidon", "note": ending_note(a, b, c)},
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

    blob = "\n".join(c["script"] for c in chunks).lower()
    if "en ce moment" not in blob:
        raise SystemExit(f"{SID}: manque en ce moment")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "bidon" not in blob:
        raise SystemExit(f"{SID}: bidon absent")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    for tic in ("tout doux", "tout calme", "aujourd'hui,"):
        if tic in blob:
            raise SystemExit(f"{SID}: tic {tic}")
    if TICS.search(blob):
        raise SystemExit(f"{SID}: tic corpus {TICS.search(blob).group(0)}")
    for bad in ("merle", "couleur de miel", "tom ", "léa", "sami", "grand-père", "maîtresse"):
        if bad in blob:
            raise SystemExit(f"{SID}: interdit {bad}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in chunks)
    if not tts_ok:
        raise SystemExit(f"{SID}: TTS incomplet")

    out = dict(src)
    out["fil_rouge"] = (
        "À la ferme, Sarah veut verser le lait chaud du bidon crème "
        "jusqu'aux bols, au banc de la laiterie, avant que le pain sorte. "
        "Nino veut jouer dehors tout de suite. Première tentative : bidon "
        "et jeu ensemble, le lait bascule. Un brin de paille, vu dès le "
        "ding, coince le couvercle. Sarah pose, retire le brin, verse, "
        "puis ils jouent. Le bidon garde une trace dans sa dent."
    )
    out["title"] = TITLE
    out["characters"] = "Sarah, Nino, papa, maman"
    out["setting"] = "ferme, cuisine de pierre, bidon de lait"
    out["chunks"] = chunks
    check(SID, out["age_band"], out["chunks"])

    def path_words(a: int, b: int, c: int) -> int:
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
        mp = {ch["chunk_id"]: ch for ch in chunks}
        return sum(words(mp[i]["text"]) for i in ids)

    lengths = [path_words(a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    if min(lengths) < 550 or max(lengths) > 700:
        raise SystemExit(f"chemins hors 550-700: {min(lengths)}-{max(lengths)}")

    t1s = [next(ch["text"] for ch in chunks if ch["chunk_id"] == f"CHK_T0001_P000{i}") for i in (1, 2, 3)]
    if len(set(t1s)) < 3:
        raise SystemExit("T1 ne change pas l'histoire")
    t2s = [
        next(ch["text"] for ch in chunks if ch["chunk_id"] == f"CHK_T0001_P0001_T0002_P000{j}")
        for j in (1, 2, 3)
    ]
    if len(set(t2s)) < 3:
        raise SystemExit("T2 ne change pas l'histoire")
    t3s = [
        next(
            ch["text"]
            for ch in chunks
            if ch["chunk_id"] == f"CHK_T0001_P0001_T0002_P0001_T0003_P000{k}"
        )
        for k in (1, 2, 3)
    ]
    if len(set(t3s)) < 3:
        raise SystemExit("T3 ne change pas l'histoire")

    folder = ROOT / SID
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    moy = sum(lengths) // len(lengths)
    (folder / "RELECTURE.md").write_text(
        "# TREE-AUT-019 — Le bidon de lait de Sarah\n\n"
        "- **Nouveau titre :** *Le bidon de lait de Sarah*\n"
        "- **Public :** 3–4 ans (N1), lecture interactive familiale\n"
        "- **Leçon principale :** AUT.ROU.001 — une chose, puis l'autre (vécue, non dite)\n"
        "- **Personnages :** Sarah, Nino, papa, maman\n"
        "- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Dans la cuisine de pierre, au banc de la laiterie, Sarah veut verser "
        "le lait chaud du bidon crème (anse de cuivre, dent, ding) avant que "
        "le pain sorte. Nino veut jouer dehors tout de suite. Ensemble, le "
        "bidon bascule. Un brin de paille, vu dès l'ouverture dans la dent, "
        "coince le couvercle : le lait fuit. Bac, toboggan ou balançoires "
        "allongent le revers. Ballon, seau ou doudou changent la ruse. Veau, "
        "poule ou chat révèlent le brin. Sarah pose, retire, verse, puis ils "
        "jouent. La dent garde une trace.\n\n"
        "## Améliorations appliquées\n\n"
        "- Monde (ferme, lucarne, pain, ding) avant l'action.\n"
        "- Désir immédiat (verser le lait) distinct de la leçon.\n"
        "- Deux enfants, deux envies : lait / dehors.\n"
        "- Première idée échoue, allongée : genou, marches ou corde + bidon.\n"
        "- Second imprévu plus rusé : filet malgré le couvercle fermé, brin coincé.\n"
        "- T1/T2/T3 changent l'action, pas seulement le lieu.\n"
        "- 1er choix ne retire pas le bidon.\n"
        "- 27 fins textuellement distinctes, dernière image unique.\n"
        "- Un merci (bac) et un bravo vécu (toboggan), pas un refrain.\n"
        "- T3 : veau / poule / chat (plus Tom, Léa, Sami).\n"
        "- Pas de « encore / déjà / tout doux », pas merle, pas miel, pas apply.\n\n"
        "## Direction vocale\n\n"
        "TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending) : "
        "rate, pitch, volume, pauses, text_ssml, text_xai_tags, notes d'arc.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, {min(lengths)} à {max(lengths)} mots, moyenne {moy}\n"
        "- 27 fins et 27 dernières images distinctes\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés\n"
        "- N1 ≤ 10 mots/phrase. `check()` OK.\n\n"
        "## Relu\n\n"
        "P0000, 3 L1, 9 L2, 27 résolutions, 27 fins. Question liée à la scène "
        "(une chose). Impatience, découragement, fierté calme.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(
        f"OK {SID} {nwords} mots  fins={len(set(fins))}  "
        f"chemins {min(lengths)}-{max(lengths)} moy {moy}  "
        f"1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}"
    )


if __name__ == "__main__":
    main()
