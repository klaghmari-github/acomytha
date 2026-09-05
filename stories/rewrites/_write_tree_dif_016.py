#!/usr/bin/env python3
"""TREE-DIF-016 — La tarte aux fraises de Chouchou (N1, DIF.COR.003, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-016"
N1 = 10
TITLE = "La tarte aux fraises de Chouchou"
FIL = (
    "Dans le fournil jaune, Chouchou veut une tarte aux fraises pour Sarah, "
    "maintenant. Un point de beurre tient au bord du plat. Elle prend le bol bleu, "
    "la cuillère ou le tablier ; les trois restent. Sarah arrive telle qu'elle est : "
    "lunettes, cheveux courts, manteau rouge trop long. À la table le sucre manque "
    "sous la farine, à l'évier les fraises propres manquent, au bac les mûres "
    "restent trop haut. Chouchou propose, Sarah prend son temps. Un silence répond. "
    "Elles refusent de foncer. Le point de beurre guide. Sarah goûte."
)
CHARS = "Chouchou, Sarah, papa, maman"
SETTING = "cuisine jaune, évier, bac du jardin"
TIC_PHRASES = (
    "tout doux",
    "tout calme",
    "tout lent",
    "miel",
    "merle",
    "aujourd'hui,",
    "j'ai compris",
    "mission accomplie",
    "on va apprendre",
    "bon travail",
    "il faut attendre",
    "papa sourit",
    "maman sourit",
    "cristal de sucre brun",
    "grain de sel",
    "étoile brune",
    "fil pâle",
    "virgule farine",
    "bouton nacre",
    "larme de bronze",
    "gouttes au bord",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "point de beurre",
        "note": "arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=chouchou_veut_la_tarte_le_beurre_attend; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_où_va_la_fraise; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=sarah_arrive_telle_qu_elle_est; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=chouchou_propose_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": "point de beurre",
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=un_ingrédient_manque_elle_refuse_de_foncer; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "point de beurre",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=on_fait_avec_sarah_telle_qu_elle_est; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "point de beurre",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=sarah_goûte_le_beurre_reste; tempo=posé; sourire=léger; respiration=ample",
    },
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict, emphasis: str | None) -> str:
    body = esc(text)
    if emphasis:
        e = esc(emphasis)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict, emphasis: str | None) -> str:
    body = text
    if emphasis:
        body = body.replace(emphasis, f"<emphasis>{emphasis}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m["pitchTag"]:
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    tail = "[long-pause]" if m["pause"] >= 800 else ("[pause]" if m["pause"] >= 400 else "")
    return f"{body} {tail}".strip()


def vet(lines: list[str], where: str = "") -> list[str]:
    out = []
    prev = ""
    run = 1
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{where} {n}>{N1}: {ph}")
        if n == 0:
            raise SystemExit(f"{where} vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"{where} ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"{where} fin: {ph}")
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"{where} tic {tic!r}: {ph}")
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"{where} tic {m.group(0)!r}: {ph}")
        if role == "narrateur":
            tok = ph.split()[0].lower()
            if tok == prev:
                run += 1
                if run >= 4:
                    raise SystemExit(f"{where} puces « {tok} »")
            else:
                run = 1
                prev = tok
        else:
            run = 1
            prev = ""
        out.append(f"{role}|{ph}")
    return out


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    lines = vet(lines, src.get("chunk_id", "?"))
    m = dict(PROFILES[profile])
    emphasis = extra.get("emphasis", m["emphasis"])
    text, script = from_script(lines)
    if emphasis and emphasis not in text:
        emphasis = None
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else ""
    nc["text_ssml"] = ssml(text, m, emphasis)
    nc["text_xai_tags"] = xai(text, m, emphasis)
    nc["length_scale_piper"] = m["piper"]
    nc["rate_label"] = m["rate"]
    nc["rate_wpm"] = m["wpm"]
    nc["speed_xai"] = m["speed"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitchSsml"]
    nc["pitch_xai_tag"] = m["pitchTag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = emphasis or ""
    nc["pause_before_ms"] = extra.get("pause_before", 0)
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
    nc["notes"] = extra.get("notes", m["note"])
    nc["night_policy"] = "play"
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        nc[k] = v
    return nc


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def path_words(by: dict, a: int, b: int, c: int) -> int:
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
    return sum(words(by[i]["text"]) for i in ids)


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=sarah_goûte_le_beurre_reste; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


OPENING = [
    "narrateur|Le four claque une fois, dans le jaune.",
    "narrateur|Les murs gardent la chaleur du four.",
    "narrateur|Une mouche marche sur le carnet.",
    "narrateur|Au bord du plat, un point de beurre tient.",
    "enfant-f|Il est rond, trop jaune !",
    "papa|C'est le beurre du goûter, Chouchou.",
    "maman|Sarah arrive, pour la tarte.",
    "narrateur|Ça sent le plat chaud, et la fraise.",
    "narrateur|Chouchou vit ici, avec papa et maman.",
    "narrateur|Le fournil jaune colle un peu, sous les pieds.",
    "enfant-f|Je veux une tarte, pour Sarah.",
    "papa|Le four tient, chaud.",
    "maman|On prépare, avant qu'elle entre ?",
    "enfant-f|Tout mélanger, trop vite !",
    "narrateur|En ce moment, Chouchou touche le plat.",
    "papa|Merci, tu as vu le beurre.",
    "narrateur|Le bol, la cuillère, le tablier attendent.",
    "maman|Tes mains dansent, Chouchou.",
]

T1_CHOICE = [
    "narrateur|Près du plat, trois affaires attendent.",
    "narrateur|Le bol, la cuillère, et le tablier.",
    "papa|Le bol bleu, la cuillère, ou le tablier ?",
    "maman|Tu prends quoi d'abord, Chouchou ?",
]

T1 = {
    1: {
        "lab": "le bol bleu",
        "sons": "bol,fraise",
        "emphasis": "bol bleu",
        "passage": [
            "narrateur|Chouchou tire d'abord le bol bleu.",
            "enfant-f|La fraise va dedans.",
            "maman|Glisse-la, sans la presser.",
            "narrateur|Un petit toc sonne, au fond.",
            "papa|La cuillère aussi, près du bol.",
            "narrateur|Maman noue le tablier, trop lâche.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-f|Sarah va goûter ma tarte.",
            "narrateur|La porte de la cuisine s'ouvre.",
            "copine|Chouchou, je suis là.",
            "enfant-f|Viens, on mélange, trop vite !",
            "narrateur|Sarah ne dit rien.",
            "narrateur|Elle pose un doigt sur le bol.",
            "papa|Le bol d'abord, vous l'avez.",
            "maman|Les trois affaires sont avec vous.",
        ],
        "question": [
            "narrateur|Chouchou a glissé la fraise dans le bol.",
            "maman|Elle est où, la fraise ?",
        ],
        "qfields": {
            "expected_answer": "bol",
            "accepted_examples": "bol | le bol | dans le bol | au fond du bol | bol bleu",
            "retry_prompt": "La fraise est dans le bol.",
        },
        "confirm": [
            "enfant-f|Dans le bol.",
            "maman|Oui.",
            "narrateur|Le bol bleu porte la fraise, au fond.",
            "copine|Elle est trop rouge.",
            "enfant-f|C'est pour toi, Sarah.",
            "narrateur|Sarah a des lunettes, sur le nez.",
            "narrateur|Elles brillent un peu, trop sages.",
            "maman|Le beurre vous attend, sur le plat.",
            "papa|On reste à la cuisine ?",
            "enfant-f|Oui, papa.",
        ],
    },
    2: {
        "lab": "la cuillère",
        "sons": "cuillere,bois",
        "emphasis": "cuillère",
        "passage": [
            "narrateur|Chouchou prend d'abord la cuillère en bois.",
            "enfant-f|La fraise reste juste à côté.",
            "papa|Le manche sent le beurre, un peu.",
            "narrateur|Le bois est rêche, sous le pouce.",
            "maman|Le bol bleu, ensuite, sur la table.",
            "narrateur|Elle glisse le tablier par-dessus.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-f|Sarah va tout voir.",
            "narrateur|Des pas légers sonnent, dans l'entrée.",
            "copine|Me voilà, Chouchou.",
            "enfant-f|On mélange, toutes les deux ?",
            "narrateur|Sarah ne dit rien.",
            "narrateur|Elle regarde le bois, trop longtemps.",
            "maman|La cuillère d'abord, elle est prête.",
            "papa|Les trois affaires sont avec vous.",
        ],
        "question": [
            "narrateur|La fraise attend près de la cuillère.",
            "papa|Elle est où, la fraise ?",
        ],
        "qfields": {
            "expected_answer": "cuillère",
            "accepted_examples": "cuillère | la cuillère | près de la cuillère | à côté | cuillere",
            "retry_prompt": "La fraise est près de la cuillère.",
        },
        "confirm": [
            "enfant-f|Près de la cuillère.",
            "papa|Oui.",
            "narrateur|La cuillère veille près de la fraise.",
            "copine|Je vois le rouge.",
            "enfant-f|Ne touche pas, pas maintenant.",
            "narrateur|Sarah a les cheveux trop courts.",
            "narrateur|Une pince bleue tient une mèche.",
            "papa|Ça sent la vanille, trop près.",
            "maman|Vos mains, au-dessus du bois ?",
            "copine|Oui, maman.",
        ],
    },
    3: {
        "lab": "le tablier",
        "sons": "tissu,tablier",
        "emphasis": "tablier",
        "passage": [
            "narrateur|Chouchou passe la tête dans le tablier.",
            "enfant-f|Je cache la fraise ici.",
            "maman|Dans la poche, comme un secret.",
            "narrateur|Le tissu sent le savon, un peu.",
            "papa|Le bol et la cuillère, avec vous.",
            "narrateur|Il les pose près du beurre.",
            "narrateur|Les trois affaires restent ensemble.",
            "enfant-f|Sarah, vite !",
            "narrateur|Un manteau rouge apparaît, au seuil.",
            "copine|J'arrive, Chouchou.",
            "enfant-f|Je te fais une tarte.",
            "narrateur|Sarah ne dit rien.",
            "narrateur|Les manches dépassent un peu ses mains.",
            "papa|Le tablier d'abord, il est noué.",
            "maman|Les trois affaires sont avec vous.",
        ],
        "question": [
            "narrateur|Chouchou a caché la fraise dans la poche.",
            "maman|Elle est où, la fraise ?",
        ],
        "qfields": {
            "expected_answer": "poche",
            "accepted_examples": "poche | la poche | dans la poche | poche du tablier | tablier",
            "retry_prompt": "La fraise est dans la poche.",
        },
        "confirm": [
            "enfant-f|Dans la poche.",
            "maman|Oui.",
            "narrateur|Le tablier cache la fraise, trop bien.",
            "copine|Ça sent le savon.",
            "enfant-f|Elle est là, dans la poche.",
            "narrateur|Le manteau rouge de Sarah tombe long.",
            "narrateur|Les manches cachent un peu ses mains.",
            "maman|La cuisine est tiède, devant.",
            "papa|On y va, tous les quatre ?",
            "enfant-f|Oui.",
        ],
    },
}


def t2_question(t1: int) -> list[str]:
    first = {
        1: "narrateur|Le bol bleu tape un peu le bois.",
        2: "narrateur|La cuillère racle un coin de farine.",
        3: "narrateur|Le tablier frotte le bord de table.",
    }[t1]
    return [
        first,
        "narrateur|La table a un nuage, trop blanc.",
        "narrateur|L'évier attend, trop froid.",
        "narrateur|Le bac du jardin a des fraises.",
        "papa|On commence où, pour la tarte ?",
    ]


T2 = {
    (1, 1): {
        "sons": "farine,bol",
        "emphasis": "point de beurre",
        "passage": [
            "narrateur|Le bol bleu tape un peu le bois.",
            "enfant-f|Je verse la farine, trop vite !",
            "narrateur|Un nuage blanc s'élève, trop léger.",
            "enfant-f|Je ne vois plus les mots.",
            "copine|Le carnet a disparu.",
            "narrateur|La farine poudre les lunettes de Sarah.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Ici, ça vole trop.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "enfant-f|On souffle, Sarah ?",
            "narrateur|Sarah ne dit rien.",
            "narrateur|Elle essuie le verre, trop lentement.",
            "narrateur|Au fond du bol, le sucre manque.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Au bord du plat, le point de beurre luit.",
            "maman|Vous voyez comment, toutes les deux ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (1, 2): {
        "sons": "eau,bol",
        "emphasis": "point de beurre",
        "passage": [
            "narrateur|Le bol bleu penche au-dessus de l'eau.",
            "enfant-f|On lave les fraises, Sarah.",
            "narrateur|Le manteau rouge touche l'eau froide.",
            "narrateur|Les manches deviennent lourdes, trop vite.",
            "copine|Ça colle à mes poignets.",
            "enfant-f|Tes manches sont trop longues.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Le manteau peut attendre au sec.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "enfant-f|Vite, on rince !",
            "narrateur|Sarah secoue la tête, sans un mot.",
            "narrateur|Les fraises propres manquent, dans le bol.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Au bord du plat, le point de beurre reste sec.",
            "papa|Vous trouvez, toutes les deux ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (1, 3): {
        "sons": "herbe,bol",
        "emphasis": "point de beurre",
        "passage": [
            "narrateur|Le bol bleu tapote l'herbe, trop léger.",
            "enfant-f|Les fraises du bac, Sarah.",
            "narrateur|Le bac est trop haut pour leurs mains.",
            "narrateur|Chouchou se hausse, puis recule.",
            "enfant-f|Ma main n'y arrive pas.",
            "narrateur|Elle cueille trop vite, trop vert.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Mes bras vont plus haut, là-bas.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "enfant-f|Monte avec moi !",
            "narrateur|Sarah ne dit rien.",
            "narrateur|Elle ouvre les deux mains, trop bas.",
            "narrateur|Les fraises mûres manquent, dans le bol.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Au bord du plat, le point de beurre luit.",
            "maman|Vous faites comment, toutes les deux ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (2, 1): {
        "sons": "farine,cuillere",
        "emphasis": "point de beurre",
        "passage": [
            "narrateur|La cuillère racle un coin de farine.",
            "enfant-f|Je tourne trop fort, trop vite !",
            "narrateur|Un nuage blanc s'élève, trop léger.",
            "enfant-f|Je ne vois plus les mots.",
            "copine|Le carnet a disparu.",
            "narrateur|La farine reste dans ses cheveux courts.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Ici, ça vole trop.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "enfant-f|On souffle, Sarah ?",
            "narrateur|Sarah ne dit rien.",
            "narrateur|Elle pose la pince, trop lentement.",
            "narrateur|Près de la cuillère, le sucre manque.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Au bord du plat, le point de beurre luit.",
            "maman|Vous voyez comment, toutes les deux ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (2, 2): {
        "sons": "eau,cuillere",
        "emphasis": "point de beurre",
        "passage": [
            "narrateur|La cuillère tapote le bord de l'évier.",
            "enfant-f|On lave les fraises, Sarah.",
            "narrateur|Le manteau rouge touche l'eau froide.",
            "narrateur|Les manches deviennent lourdes, trop vite.",
            "copine|Ça colle à mes poignets.",
            "enfant-f|Tes manches sont trop longues.",
            "narrateur|Chouchou ne rit plus.",
            "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
            "maman|Le manteau peut attendre au sec.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "enfant-f|Vite, on rince !",
            "narrateur|Sarah secoue la tête, sans un mot.",
            "narrateur|Les fraises propres manquent, près du bois.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Au bord du plat, le point de beurre reste sec.",
            "papa|Vous trouvez, toutes les deux ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (2, 3): {
        "sons": "herbe,cuillere",
        "emphasis": "point de beurre",
        "passage": [
            "narrateur|La cuillère frôle les feuilles, trop bas.",
            "enfant-f|Les fraises du bac, Sarah.",
            "narrateur|Le bac est trop haut pour leurs mains.",
            "narrateur|Chouchou se hausse, puis recule.",
            "enfant-f|Ma main n'y arrive pas.",
            "narrateur|La cuillère racle du vert, trop vite.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Mes bras vont plus haut, là-bas.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "enfant-f|Monte avec moi !",
            "narrateur|Sarah ne dit rien.",
            "narrateur|Elle ouvre les deux mains, trop bas.",
            "narrateur|Les fraises mûres manquent, près du bois.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Au bord du plat, le point de beurre luit.",
            "maman|Vous faites comment, toutes les deux ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (3, 1): {
        "sons": "farine,tissu",
        "emphasis": "point de beurre",
        "passage": [
            "narrateur|Le tablier frotte le bord de table.",
            "enfant-f|J'essuie trop fort, trop vite !",
            "narrateur|Un nuage blanc s'élève, trop léger.",
            "enfant-f|Je ne vois plus les mots.",
            "copine|Le carnet a disparu.",
            "narrateur|La farine poudre les lunettes de Sarah.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Ici, ça vole trop.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "enfant-f|On souffle, Sarah ?",
            "narrateur|Sarah ne dit rien.",
            "narrateur|Elle essuie le verre, trop lentement.",
            "narrateur|Dans la poche, le sucre manque.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Au bord du plat, le point de beurre luit.",
            "maman|Vous voyez comment, toutes les deux ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (3, 2): {
        "sons": "eau,tissu",
        "emphasis": "point de beurre",
        "passage": [
            "narrateur|Le tablier frôle le robinet, trop mouillé.",
            "enfant-f|On lave les fraises, Sarah.",
            "narrateur|Le manteau rouge touche l'eau froide.",
            "narrateur|Les manches deviennent lourdes, trop vite.",
            "copine|Ça colle à mes poignets.",
            "enfant-f|Tes manches sont trop longues.",
            "narrateur|Chouchou ne rit plus.",
            "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
            "maman|Le manteau peut attendre au sec.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "enfant-f|Vite, on rince !",
            "narrateur|Sarah secoue la tête, sans un mot.",
            "narrateur|Les fraises propres manquent, dans la poche.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Au bord du plat, le point de beurre reste sec.",
            "papa|Vous trouvez, toutes les deux ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (3, 3): {
        "sons": "herbe,tissu",
        "emphasis": "point de beurre",
        "passage": [
            "narrateur|Le tablier reste au bord, un peu sec.",
            "enfant-f|Les fraises du bac, Sarah.",
            "narrateur|Le bac est trop haut pour leurs mains.",
            "narrateur|Chouchou se hausse, puis recule.",
            "enfant-f|Ma main n'y arrive pas.",
            "narrateur|La poche se tend, trop vite, trop haut.",
            "narrateur|Le sourire de Chouchou disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Mes bras vont plus haut, là-bas.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "enfant-f|Monte avec moi !",
            "narrateur|Sarah ne dit rien.",
            "narrateur|Elle ouvre les deux mains, trop bas.",
            "narrateur|Les fraises mûres manquent, dans la poche.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Au bord du plat, le point de beurre luit.",
            "maman|Vous faites comment, toutes les deux ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
}

T3_LABS = {
    1: ("attendre un peu", "regarder avec Sarah", "tenir le bol"),
    2: ("le crochet", "les manches", "la passoire"),
    3: ("la marche", "les bras de papa", "les fraises basses"),
}

T3_CHOICE = {
    1: [
        "narrateur|Le nuage cache le carnet, trop blanc.",
        "papa|Attendre, regarder avec Sarah, ou tenir ?",
    ],
    2: [
        "narrateur|Les manches restent trop mouillées.",
        "maman|Le crochet, les manches, ou la passoire ?",
    ],
    3: [
        "narrateur|Les fraises du bac restent trop haut.",
        "papa|La marche, mes bras, ou les basses ?",
    ],
}

T3_SONS = {
    (1, 1): "farine,attente",
    (1, 2): "lunettes,carnet",
    (1, 3): "bol,bois",
    (2, 1): "crochet,manteau",
    (2, 2): "tissu,manches",
    (2, 3): "passoire,eau",
    (3, 1): "marche,fraises",
    (3, 2): "bras,pot",
    (3, 3): "fraises,herbe",
}

T3 = {
    (1, 1, 1): [
        "enfant-f|On attend un peu.",
        "narrateur|Sarah ne dit rien.",
        "narrateur|Elle essuie le verre, trop lentement.",
        "narrateur|La farine retombe, sur le bois.",
        "narrateur|Le bol bleu attend, sous le nuage.",
        "narrateur|Le sucre manque, au fond.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "copine|Le sucre est là, près du beurre.",
        "papa|Vous l'avez vu, toutes les deux.",
        "maman|Les lunettes voient, maintenant.",
        "enfant-f|Mélange, Sarah.",
        "narrateur|Sarah tourne, à son rythme.",
        "papa|Le nuage vous a laissé la place.",
    ],
    (1, 1, 2): [
        "copine|Mes lunettes voient, un peu.",
        "enfant-f|Regarde le carnet, Sarah.",
        "narrateur|Sarah essuie un peu de farine, sur le verre.",
        "narrateur|Les mots reviennent, trop nets.",
        "narrateur|Sarah penche le bol, trop près.",
        "copine|Là, on mélange trois tours.",
        "enfant-f|Je le fais avec toi.",
        "narrateur|Le sucre manque, au fond du bleu.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "copine|Le sucre est là, près du beurre.",
        "papa|Vous lisez ensemble.",
        "maman|Les lunettes ont aidé, trop nettes.",
        "narrateur|Sarah tourne, à son rythme.",
    ],
    (1, 1, 3): [
        "enfant-f|Papa, tu tiens le bol ?",
        "papa|Je le tiens, Chouchou.",
        "narrateur|Papa tient le bol, trop stable.",
        "narrateur|Sarah guide la main de Chouchou.",
        "narrateur|La farine tourne, puis s'assoit.",
        "copine|Le carnet est libre, maintenant.",
        "enfant-f|On mélange, toutes les deux.",
        "narrateur|Le sucre manque, au fond du bleu.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "copine|Le sucre est là, près du beurre.",
        "maman|Vous y arrivez ensemble.",
        "narrateur|Un peu de blanc reste aux cheveux courts.",
        "papa|Les lunettes voient, et les mains tournent.",
    ],
    (1, 2, 1): [
        "copine|Je le mets au crochet.",
        "enfant-f|Oui, trop haut.",
        "narrateur|Sarah accroche le manteau rouge.",
        "narrateur|Les manches se taisent, trop lourdes.",
        "narrateur|Le bol bleu attend au sec, à côté.",
        "enfant-f|Tes bras sont libres, maintenant.",
        "copine|On lave les fraises.",
        "narrateur|Les fraises propres manquent, dans le bleu.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre reste sec, sur le plat.",
        "papa|Le manteau sèche à sa place.",
        "maman|L'eau reste dans l'évier.",
        "narrateur|Sarah rince, à son rythme.",
        "enfant-f|Tes manches, telles quelles, au crochet.",
    ],
    (1, 2, 2): [
        "enfant-f|On roule tes manches, Sarah.",
        "copine|Aide-moi, Chouchou.",
        "narrateur|Chouchou pose le bol près du savon.",
        "narrateur|Les deux filles plient le tissu.",
        "narrateur|Les poignets de Sarah apparaissent.",
        "copine|L'eau ne les touche plus.",
        "enfant-f|On lave, maintenant.",
        "narrateur|Les fraises propres manquent, dans le bleu.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre reste sec, sur le plat.",
        "maman|Vos manches sont au sec.",
        "papa|Les fraises peuvent briller.",
        "narrateur|Sarah rince, à son rythme.",
        "enfant-f|Tes manches longues, on les plie.",
    ],
    (1, 2, 3): [
        "enfant-f|La passoire, Sarah.",
        "copine|Je la tiens, toi tu verses.",
        "narrateur|Maman tend la passoire ronde.",
        "narrateur|Sarah tient le bol, Chouchou rince.",
        "narrateur|L'eau s'échappe, les fraises restent.",
        "enfant-f|Elles brillent, maintenant.",
        "copine|Mes manches n'ont presque rien.",
        "narrateur|Les fraises propres manquent, puis reviennent.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre reste sec, sur le plat.",
        "papa|Vous avez versé ensemble.",
        "maman|La passoire a fait le travail.",
        "narrateur|Sarah verse, à son rythme.",
        "enfant-f|Tes manches longues, sans l'eau.",
    ],
    (1, 3, 1): [
        "enfant-f|Je monte sur la marche.",
        "copine|Je te vois, trop près.",
        "narrateur|Chouchou cueille une fraise chaude.",
        "narrateur|Sarah ouvre les deux mains.",
        "enfant-f|Elle est à toi, un moment.",
        "narrateur|Le bol bleu attend au pied de la marche.",
        "copine|J'en prends une autre, plus bas.",
        "narrateur|Les fraises mûres manquent, puis reviennent.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "papa|Vous êtes à votre hauteur.",
        "maman|Le bac reste à sa place.",
        "narrateur|Sarah reçoit, à son rythme.",
        "enfant-f|Toi tu attends, moi je cueille.",
    ],
    (1, 3, 2): [
        "enfant-f|Papa, un peu plus bas.",
        "papa|Je vous le descends.",
        "narrateur|Le pot de fraises arrive au menton.",
        "narrateur|Papa pose le pot près du bol.",
        "copine|Je les vois trop bien !",
        "enfant-f|On cueille, toutes les deux.",
        "narrateur|Deux mains, deux fraises, même hauteur.",
        "narrateur|Les fraises mûres manquent, puis reviennent.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "maman|Vous les avez, enfin.",
        "papa|Mes bras ont juste aidé.",
        "narrateur|Sarah cueille, à son rythme.",
        "enfant-f|À notre menton, pas trop haut.",
    ],
    (1, 3, 3): [
        "enfant-f|On prend celles d'en bas.",
        "copine|Celles qu'on touche, sans monter.",
        "narrateur|Des fraises basses pendent, trop mûres.",
        "narrateur|Elles glissent les fraises dans le bol.",
        "narrateur|Le soleil les a trop chaudes.",
        "enfant-f|On en a assez, Sarah.",
        "copine|Pour la tarte, oui.",
        "narrateur|Les fraises mûres manquent, puis reviennent.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "papa|Vos mains allaient assez loin.",
        "maman|Le bac garde les hautes, pour plus tard.",
        "narrateur|Sarah cueille, à son rythme.",
        "enfant-f|Tes mains suffisent, trop bas.",
    ],
    (2, 1, 1): [
        "enfant-f|On attend un peu.",
        "narrateur|Sarah ne dit rien.",
        "narrateur|Elle pose la pince, trop lentement.",
        "narrateur|La farine retombe, sur le bois.",
        "narrateur|La cuillère attend, sous le nuage.",
        "narrateur|Le sucre manque, près du bois.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "copine|Le sucre est là, près du beurre.",
        "papa|Vous l'avez vu, toutes les deux.",
        "maman|Les cheveux courts gardent un peu de blanc.",
        "enfant-f|Mélange, Sarah.",
        "narrateur|Sarah tourne, à son rythme.",
        "papa|Le nuage vous a laissé la place.",
    ],
    (2, 1, 2): [
        "copine|Mes lunettes voient, un peu.",
        "enfant-f|Regarde le carnet, Sarah.",
        "narrateur|Sarah essuie un peu de farine, sur le verre.",
        "narrateur|Les mots reviennent, trop nets.",
        "narrateur|Sarah penche la cuillère, trop près.",
        "copine|Là, on mélange trois tours.",
        "enfant-f|Je le fais avec toi.",
        "narrateur|Le sucre manque, près du bois.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "copine|Le sucre est là, près du beurre.",
        "papa|Vous lisez ensemble.",
        "maman|Les lunettes ont aidé, trop nettes.",
        "narrateur|Sarah tourne, à son rythme.",
    ],
    (2, 1, 3): [
        "enfant-f|Papa, tu tiens le bol ?",
        "papa|Je le tiens, Chouchou.",
        "narrateur|Papa tient la cuillère, trop stable.",
        "narrateur|Sarah guide la main de Chouchou.",
        "narrateur|La farine tourne, puis s'assoit.",
        "copine|Le carnet est libre, maintenant.",
        "enfant-f|On mélange, toutes les deux.",
        "narrateur|Le sucre manque, près du bois.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "copine|Le sucre est là, près du beurre.",
        "maman|Vous y arrivez ensemble.",
        "narrateur|Un peu de blanc reste aux cheveux courts.",
        "papa|Les lunettes voient, et les mains tournent.",
    ],
    (2, 2, 1): [
        "copine|Je le mets au crochet.",
        "enfant-f|Oui, trop haut.",
        "narrateur|Sarah accroche le manteau rouge.",
        "narrateur|Les manches se taisent, trop lourdes.",
        "narrateur|La cuillère attend au sec, à côté.",
        "enfant-f|Tes bras sont libres, maintenant.",
        "copine|On lave les fraises.",
        "narrateur|Les fraises propres manquent, près du bois.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre reste sec, sur le plat.",
        "papa|Le manteau sèche à sa place.",
        "maman|L'eau reste dans l'évier.",
        "narrateur|Sarah rince, à son rythme.",
        "enfant-f|Tes manches, telles quelles, au crochet.",
    ],
    (2, 2, 2): [
        "enfant-f|On roule tes manches, Sarah.",
        "copine|Aide-moi, Chouchou.",
        "narrateur|Chouchou pose la cuillère près du savon.",
        "narrateur|Les deux filles plient le tissu.",
        "narrateur|Les poignets de Sarah apparaissent.",
        "copine|L'eau ne les touche plus.",
        "enfant-f|On lave, maintenant.",
        "narrateur|Les fraises propres manquent, près du bois.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre reste sec, sur le plat.",
        "maman|Vos manches sont au sec.",
        "papa|Les fraises peuvent briller.",
        "narrateur|Sarah rince, à son rythme.",
        "enfant-f|Tes manches longues, on les plie.",
    ],
    (2, 2, 3): [
        "enfant-f|La passoire, Sarah.",
        "copine|Je la tiens, toi tu verses.",
        "narrateur|Maman tend la passoire ronde.",
        "narrateur|Sarah tient la cuillère, Chouchou rince.",
        "narrateur|L'eau s'échappe, les fraises restent.",
        "enfant-f|Elles brillent, maintenant.",
        "copine|Mes manches n'ont presque rien.",
        "narrateur|Les fraises propres manquent, puis reviennent.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre reste sec, sur le plat.",
        "papa|Vous avez versé ensemble.",
        "maman|La passoire a fait le travail.",
        "narrateur|Sarah verse, à son rythme.",
        "enfant-f|Tes manches longues, sans l'eau.",
    ],
    (2, 3, 1): [
        "enfant-f|Je monte sur la marche.",
        "copine|Je te vois, trop près.",
        "narrateur|Chouchou cueille une fraise chaude.",
        "narrateur|Sarah ouvre les deux mains.",
        "enfant-f|Elle est à toi, un moment.",
        "narrateur|La cuillère attend au pied de la marche.",
        "copine|J'en prends une autre, plus bas.",
        "narrateur|Les fraises mûres manquent, puis reviennent.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "papa|Vous êtes à votre hauteur.",
        "maman|Le bac reste à sa place.",
        "narrateur|Sarah reçoit, à son rythme.",
        "enfant-f|Toi tu attends, moi je cueille.",
    ],
    (2, 3, 2): [
        "enfant-f|Papa, un peu plus bas.",
        "papa|Je vous le descends.",
        "narrateur|Le pot de fraises arrive au menton.",
        "narrateur|Papa pose le pot près de la cuillère.",
        "copine|Je les vois trop bien !",
        "enfant-f|On cueille, toutes les deux.",
        "narrateur|Deux mains, deux fraises, même hauteur.",
        "narrateur|Les fraises mûres manquent, puis reviennent.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "maman|Vous les avez, enfin.",
        "papa|Mes bras ont juste aidé.",
        "narrateur|Sarah cueille, à son rythme.",
        "enfant-f|À notre menton, pas trop haut.",
    ],
    (2, 3, 3): [
        "enfant-f|On prend celles d'en bas.",
        "copine|Celles qu'on touche, sans monter.",
        "narrateur|Des fraises basses pendent, trop mûres.",
        "narrateur|Elles glissent les fraises près de la cuillère.",
        "narrateur|Le soleil les a trop chaudes.",
        "enfant-f|On en a assez, Sarah.",
        "copine|Pour la tarte, oui.",
        "narrateur|Les fraises mûres manquent, puis reviennent.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "papa|Vos mains allaient assez loin.",
        "maman|Le bac garde les hautes, pour plus tard.",
        "narrateur|Sarah cueille, à son rythme.",
        "enfant-f|Tes mains suffisent, trop bas.",
    ],
    (3, 1, 1): [
        "enfant-f|On attend un peu.",
        "narrateur|Sarah ne dit rien.",
        "narrateur|Elle essuie le verre, trop lentement.",
        "narrateur|La farine retombe, sur le bois.",
        "narrateur|Le tablier attend, sous le nuage.",
        "narrateur|Le sucre manque, dans la poche.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "copine|Le sucre est là, près du beurre.",
        "papa|Vous l'avez vu, toutes les deux.",
        "maman|Les lunettes voient, maintenant.",
        "enfant-f|Mélange, Sarah.",
        "narrateur|Sarah tourne, à son rythme.",
        "papa|Le nuage vous a laissé la place.",
    ],
    (3, 1, 2): [
        "copine|Mes lunettes voient, un peu.",
        "enfant-f|Regarde le carnet, Sarah.",
        "narrateur|Sarah essuie un peu de farine, sur le verre.",
        "narrateur|Les mots reviennent, trop nets.",
        "narrateur|Sarah penche le tablier, trop près.",
        "copine|Là, on mélange trois tours.",
        "enfant-f|Je le fais avec toi.",
        "narrateur|Le sucre manque, dans la poche.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "copine|Le sucre est là, près du beurre.",
        "papa|Vous lisez ensemble.",
        "maman|Les lunettes ont aidé, trop nettes.",
        "narrateur|Sarah tourne, à son rythme.",
    ],
    (3, 1, 3): [
        "enfant-f|Papa, tu tiens le bol ?",
        "papa|Je le tiens, Chouchou.",
        "narrateur|Papa tient le tablier, trop stable.",
        "narrateur|Sarah guide la main de Chouchou.",
        "narrateur|La farine tourne, puis s'assoit.",
        "copine|Le carnet est libre, maintenant.",
        "enfant-f|On mélange, toutes les deux.",
        "narrateur|Le sucre manque, dans la poche.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "copine|Le sucre est là, près du beurre.",
        "maman|Vous y arrivez ensemble.",
        "narrateur|Un peu de blanc reste aux cheveux courts.",
        "papa|Les lunettes voient, et les mains tournent.",
    ],
    (3, 2, 1): [
        "copine|Je le mets au crochet.",
        "enfant-f|Oui, trop haut.",
        "narrateur|Sarah accroche le manteau rouge.",
        "narrateur|Les manches se taisent, trop lourdes.",
        "narrateur|Le tablier attend au sec, à côté.",
        "enfant-f|Tes bras sont libres, maintenant.",
        "copine|On lave les fraises.",
        "narrateur|Les fraises propres manquent, dans la poche.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre reste sec, sur le plat.",
        "papa|Le manteau sèche à sa place.",
        "maman|L'eau reste dans l'évier.",
        "narrateur|Sarah rince, à son rythme.",
        "enfant-f|Tes manches, telles quelles, au crochet.",
    ],
    (3, 2, 2): [
        "enfant-f|On roule tes manches, Sarah.",
        "copine|Aide-moi, Chouchou.",
        "narrateur|Chouchou relève le tablier, trop court.",
        "narrateur|Les deux filles plient le tissu.",
        "narrateur|Les poignets de Sarah apparaissent.",
        "copine|L'eau ne les touche plus.",
        "enfant-f|On lave, maintenant.",
        "narrateur|Les fraises propres manquent, dans la poche.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre reste sec, sur le plat.",
        "maman|Vos manches sont au sec.",
        "papa|Les fraises peuvent briller.",
        "narrateur|Sarah rince, à son rythme.",
        "enfant-f|Tes manches longues, on les plie.",
    ],
    (3, 2, 3): [
        "enfant-f|La passoire, Sarah.",
        "copine|Je la tiens, toi tu verses.",
        "narrateur|Maman tend la passoire ronde.",
        "narrateur|Sarah tient le tablier, Chouchou rince.",
        "narrateur|L'eau s'échappe, les fraises restent.",
        "enfant-f|Elles brillent, maintenant.",
        "copine|Mes manches n'ont presque rien.",
        "narrateur|Les fraises propres manquent, puis reviennent.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre reste sec, sur le plat.",
        "papa|Vous avez versé ensemble.",
        "maman|La passoire a fait le travail.",
        "narrateur|Sarah verse, à son rythme.",
        "enfant-f|Tes manches longues, sans l'eau.",
    ],
    (3, 3, 1): [
        "enfant-f|Je monte sur la marche.",
        "copine|Je te vois, trop près.",
        "narrateur|Chouchou cueille une fraise chaude.",
        "narrateur|Sarah ouvre les deux mains.",
        "enfant-f|Elle est à toi, un moment.",
        "narrateur|Le tablier attend au pied de la marche.",
        "copine|J'en prends une autre, plus bas.",
        "narrateur|Les fraises mûres manquent, puis reviennent.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "papa|Vous êtes à votre hauteur.",
        "maman|Le bac reste à sa place.",
        "narrateur|Sarah reçoit, à son rythme.",
        "enfant-f|Toi tu attends, moi je cueille.",
    ],
    (3, 3, 2): [
        "enfant-f|Papa, un peu plus bas.",
        "papa|Je vous le descends.",
        "narrateur|Le pot de fraises arrive au menton.",
        "narrateur|Papa pose le pot près du tablier.",
        "copine|Je les vois trop bien !",
        "enfant-f|On cueille, toutes les deux.",
        "narrateur|Deux mains, deux fraises, même hauteur.",
        "narrateur|Les fraises mûres manquent, puis reviennent.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "maman|Vous les avez, enfin.",
        "papa|Mes bras ont juste aidé.",
        "narrateur|Sarah cueille, à son rythme.",
        "enfant-f|À notre menton, pas trop haut.",
    ],
    (3, 3, 3): [
        "enfant-f|On prend celles d'en bas.",
        "copine|Celles qu'on touche, sans monter.",
        "narrateur|Des fraises basses pendent, trop mûres.",
        "narrateur|Elles glissent les fraises dans la poche.",
        "narrateur|Le soleil les a trop chaudes.",
        "enfant-f|On en a assez, Sarah.",
        "copine|Pour la tarte, oui.",
        "narrateur|Les fraises mûres manquent, puis reviennent.",
        "enfant-f|Je ne fonce pas.",
        "narrateur|Le point de beurre luit, sur le plat.",
        "papa|Vos mains allaient assez loin.",
        "maman|Le bac garde les hautes, pour plus tard.",
        "narrateur|Sarah cueille, à son rythme.",
        "enfant-f|Tes mains suffisent, trop bas.",
    ],
}

END_SONS = {1: "tarte,four", 2: "eau,evier", 3: "jardin,vitre"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|La tarte sort, trop chaude.",
        "copine|On a attendu le nuage, d'abord.",
        "enfant-f|Puis on a mélangé.",
        "papa|Le sucre était près du beurre.",
        "maman|Cette part est pour Sarah.",
        "narrateur|Sarah goûte, trop petit.",
        "copine|Elle est sucrée !",
        "narrateur|Le bol bleu sèche près de l'évier.",
        "narrateur|Le point de beurre dort sur le bol.",
    ],
    (1, 1, 2): [
        "narrateur|La tarte brille sous la fenêtre.",
        "enfant-f|Tes lunettes ont vu les mots.",
        "copine|Oui, trop près de mes yeux.",
        "papa|Vous avez lu ensemble.",
        "maman|Posez-la sur le rebord, au chaud.",
        "narrateur|Un peu de buée prend les verres.",
        "enfant-f|Goûte, Sarah.",
        "narrateur|Le rouge de la fraise reste au coin.",
        "narrateur|Le point de beurre luit derrière les lunettes.",
    ],
    (1, 1, 3): [
        "narrateur|Le bol a voyagé jusqu'à la table.",
        "copine|Papa le tenait, nous on tournait.",
        "enfant-f|La farine s'est assise.",
        "maman|Vos cheveux ont un peu de blanc.",
        "papa|Soufflez, trop léger, dehors.",
        "narrateur|Le bol bleu pose un cercle de farine.",
        "narrateur|Sarah goûte la part du milieu.",
        "enfant-f|Elle est à nous.",
        "narrateur|Le point de beurre fait un cercle gras.",
    ],
    (1, 2, 1): [
        "narrateur|Elles rentrent les mains trop fraîches.",
        "enfant-f|Ton manteau sèche au crochet.",
        "copine|Les fraises ont brillé, après.",
        "papa|Le rouge a attendu à sa place.",
        "maman|La tarte est prête, sur le bois.",
        "enfant-f|Elle est pour Sarah, maintenant.",
        "copine|Elle est un peu chaude.",
        "narrateur|Le bol bleu sèche près de l'évier.",
        "narrateur|Le point de beurre sèche près du crochet.",
    ],
    (1, 2, 2): [
        "narrateur|Les manches de Sarah sont restées sèches.",
        "copine|On les a roulées, toutes les deux.",
        "enfant-f|Tes poignets étaient libres.",
        "maman|L'eau n'a pas pris le tissu.",
        "papa|Lavez-vous, trop léger, un peu.",
        "narrateur|Le bol bleu garde une petite perle.",
        "copine|Je goûte, Chouchou.",
        "narrateur|La tarte craque, puis se tait.",
        "narrateur|Le point de beurre attend au sec, sur l'émail.",
    ],
    (1, 2, 3): [
        "narrateur|La passoire sèche près du robinet.",
        "enfant-f|Tu tenais, moi je versais.",
        "copine|Les fraises sont restées, l'eau est partie.",
        "papa|Vous avez versé ensemble.",
        "maman|Changez le tablier, s'il est mouillé.",
        "narrateur|Le bol bleu sèche près de l'évier.",
        "narrateur|Une perle rouge marque le carreau.",
        "enfant-f|Regarde-la, Sarah, elle brille.",
        "narrateur|Le point de beurre glisse sur la passoire.",
    ],
    (1, 3, 1): [
        "narrateur|La marche a un peu de terre.",
        "copine|Tu l'as cueillie pour moi.",
        "enfant-f|Tu tenais tes mains ouvertes.",
        "maman|Essuie tes pieds, sur le paillasson.",
        "papa|Les fraises sont chaudes, maintenant.",
        "narrateur|Sarah pose sa part contre la vitre.",
        "narrateur|Le bol bleu sèche près de l'évier.",
        "narrateur|Un rai de soleil traverse le rouge.",
        "narrateur|Le point de beurre repose au pied de la marche.",
    ],
    (1, 3, 2): [
        "narrateur|Le pot est redescendu jusqu'à la porte.",
        "enfant-f|Papa l'a mis à notre menton.",
        "copine|On a cueilli ensemble, après.",
        "papa|Le bac vous a laissé le temps.",
        "maman|La terre sèche sur vos doigts.",
        "narrateur|Le bol bleu pose un peu de terre.",
        "copine|Elle brille trop, Chouchou.",
        "enfant-f|C'est pour ça.",
        "narrateur|Le point de beurre voyage jusqu'à la porte.",
    ],
    (1, 3, 3): [
        "narrateur|Un peu de terre reste au seuil.",
        "enfant-f|On a pris celles d'en bas.",
        "copine|Sans trop monter.",
        "papa|Le bac a gardé les hautes.",
        "maman|Vos mains sentent le soleil.",
        "narrateur|Le bol bleu sèche près de l'évier.",
        "narrateur|Sarah pose sa part au rebord.",
        "enfant-f|Tu l'as goûtée, enfin.",
        "narrateur|Le point de beurre sent la terre tiède.",
    ],
    (2, 1, 1): [
        "narrateur|La tarte sort, trop chaude.",
        "copine|On a attendu le nuage, d'abord.",
        "enfant-f|Puis on a mélangé.",
        "papa|Le sucre était près du beurre.",
        "maman|Cette part est pour Sarah.",
        "narrateur|Sarah goûte, trop petit.",
        "copine|Elle est sucrée !",
        "narrateur|La cuillère sèche près de l'évier.",
        "narrateur|Le point de beurre colle au bois de cuillère.",
    ],
    (2, 1, 2): [
        "narrateur|La tarte brille sous la fenêtre.",
        "enfant-f|Tes lunettes ont vu les mots.",
        "copine|Oui, trop près de mes yeux.",
        "papa|Vous avez lu ensemble.",
        "maman|Posez-la sur le rebord, au chaud.",
        "narrateur|Un peu de buée prend les verres.",
        "enfant-f|Goûte, Sarah.",
        "narrateur|La cuillère sèche près de l'évier.",
        "narrateur|Le point de beurre tremble au bord du plat.",
    ],
    (2, 1, 3): [
        "narrateur|La cuillère a voyagé jusqu'à la table.",
        "copine|Papa la tenait, nous on tournait.",
        "enfant-f|La farine s'est assise.",
        "maman|Vos cheveux ont un peu de blanc.",
        "papa|Soufflez, trop léger, dehors.",
        "narrateur|La cuillère pose un cercle de farine.",
        "narrateur|Sarah goûte la part du milieu.",
        "enfant-f|Elle est à nous.",
        "narrateur|Le point de beurre brille au fond du bleu.",
    ],
    (2, 2, 1): [
        "narrateur|Elles rentrent les mains trop fraîches.",
        "enfant-f|Ton manteau sèche au crochet.",
        "copine|Les fraises ont brillé, après.",
        "papa|Le rouge a attendu à sa place.",
        "maman|La tarte est prête, sur le bois.",
        "enfant-f|Elle est pour Sarah, maintenant.",
        "copine|Elle est un peu chaude.",
        "narrateur|La cuillère sèche près de l'évier.",
        "narrateur|Le point de beurre ne fond plus.",
    ],
    (2, 2, 2): [
        "narrateur|Les manches de Sarah sont restées sèches.",
        "copine|On les a roulées, toutes les deux.",
        "enfant-f|Tes poignets étaient libres.",
        "maman|L'eau n'a pas pris le tissu.",
        "papa|Lavez-vous, trop léger, un peu.",
        "narrateur|La cuillère garde une petite perle.",
        "copine|Je goûte, Chouchou.",
        "narrateur|La tarte craque, puis se tait.",
        "narrateur|Le point de beurre tient au rebord mouillé.",
    ],
    (2, 2, 3): [
        "narrateur|La passoire sèche près du robinet.",
        "enfant-f|Tu tenais, moi je versais.",
        "copine|Les fraises sont restées, l'eau est partie.",
        "papa|Vous avez versé ensemble.",
        "maman|Changez le tablier, s'il est mouillé.",
        "narrateur|La cuillère sèche près de l'évier.",
        "narrateur|Une perle rouge marque le carreau.",
        "enfant-f|Regarde-la, Sarah, elle brille.",
        "narrateur|Le point de beurre marque le torchon.",
    ],
    (2, 3, 1): [
        "narrateur|La marche a un peu de terre.",
        "copine|Tu l'as cueillie pour moi.",
        "enfant-f|Tu tenais tes mains ouvertes.",
        "maman|Essuie tes pieds, sur le paillasson.",
        "papa|Les fraises sont chaudes, maintenant.",
        "narrateur|Sarah pose sa part contre la vitre.",
        "narrateur|La cuillère sèche près de l'évier.",
        "narrateur|Un rai de soleil traverse le rouge.",
        "narrateur|Le point de beurre garde un fil d'herbe.",
    ],
    (2, 3, 2): [
        "narrateur|Le pot est redescendu jusqu'à la porte.",
        "enfant-f|Papa l'a mis à notre menton.",
        "copine|On a cueilli ensemble, après.",
        "papa|Le bac vous a laissé le temps.",
        "maman|La terre sèche sur vos doigts.",
        "narrateur|La cuillère pose un peu de terre.",
        "copine|Elle brille trop, Chouchou.",
        "enfant-f|C'est pour ça.",
        "narrateur|Le point de beurre brille contre la vitre.",
    ],
    (2, 3, 3): [
        "narrateur|Un peu de terre reste au seuil.",
        "enfant-f|On a pris celles d'en bas.",
        "copine|Sans trop monter.",
        "papa|Le bac a gardé les hautes.",
        "maman|Vos mains sentent le soleil.",
        "narrateur|La cuillère sèche près de l'évier.",
        "narrateur|Sarah pose sa part au rebord.",
        "enfant-f|Tu l'as goûtée, enfin.",
        "narrateur|Le point de beurre s'endort sur la nappe.",
    ],
    (3, 1, 1): [
        "narrateur|La tarte sort, trop chaude.",
        "copine|On a attendu le nuage, d'abord.",
        "enfant-f|Puis on a mélangé.",
        "papa|Le sucre était près du beurre.",
        "maman|Cette part est pour Sarah.",
        "narrateur|Sarah goûte, trop petit.",
        "copine|Elle est sucrée !",
        "narrateur|Le tablier sèche près de l'évier.",
        "narrateur|Le point de beurre tache la poche.",
    ],
    (3, 1, 2): [
        "narrateur|La tarte brille sous la fenêtre.",
        "enfant-f|Tes lunettes ont vu les mots.",
        "copine|Oui, trop près de mes yeux.",
        "papa|Vous avez lu ensemble.",
        "maman|Posez-la sur le rebord, au chaud.",
        "narrateur|Un peu de buée prend les verres.",
        "enfant-f|Goûte, Sarah.",
        "narrateur|Le tablier sèche près de l'évier.",
        "narrateur|Le point de beurre reste au coin du carnet.",
    ],
    (3, 1, 3): [
        "narrateur|Le tablier a voyagé jusqu'à la table.",
        "copine|Papa le tenait, nous on tournait.",
        "enfant-f|La farine s'est assise.",
        "maman|Vos cheveux ont un peu de blanc.",
        "papa|Soufflez, trop léger, dehors.",
        "narrateur|Le tablier pose un cercle de farine.",
        "narrateur|Sarah goûte la part du milieu.",
        "enfant-f|Elle est à nous.",
        "narrateur|Le point de beurre sent le four, tiède.",
    ],
    (3, 2, 1): [
        "narrateur|Elles rentrent les mains trop fraîches.",
        "enfant-f|Ton manteau sèche au crochet.",
        "copine|Les fraises ont brillé, après.",
        "papa|Le rouge a attendu à sa place.",
        "maman|La tarte est prête, sur le bois.",
        "enfant-f|Elle est pour Sarah, maintenant.",
        "copine|Elle est un peu chaude.",
        "narrateur|Le tablier sèche près de l'évier.",
        "narrateur|Le point de beurre tient sous l'eau froide.",
    ],
    (3, 2, 2): [
        "narrateur|Les manches de Sarah sont restées sèches.",
        "copine|On les a roulées, toutes les deux.",
        "enfant-f|Tes poignets étaient libres.",
        "maman|L'eau n'a pas pris le tissu.",
        "papa|Lavez-vous, trop léger, un peu.",
        "narrateur|Le tablier garde une petite perle.",
        "copine|Je goûte, Chouchou.",
        "narrateur|La tarte craque, puis se tait.",
        "narrateur|Le point de beurre reste collé au plat.",
    ],
    (3, 2, 3): [
        "narrateur|La passoire sèche près du robinet.",
        "enfant-f|Tu tenais, moi je versais.",
        "copine|Les fraises sont restées, l'eau est partie.",
        "papa|Vous avez versé ensemble.",
        "maman|Changez le tablier, s'il est mouillé.",
        "narrateur|Le tablier sèche près de l'évier.",
        "narrateur|Une perle rouge marque le carreau.",
        "enfant-f|Regarde-la, Sarah, elle brille.",
        "narrateur|Le point de beurre laisse une trace ronde.",
    ],
    (3, 3, 1): [
        "narrateur|La marche a un peu de terre.",
        "copine|Tu l'as cueillie pour moi.",
        "enfant-f|Tu tenais tes mains ouvertes.",
        "maman|Essuie tes pieds, sur le paillasson.",
        "papa|Les fraises sont chaudes, maintenant.",
        "narrateur|Sarah pose sa part contre la vitre.",
        "narrateur|Le tablier sèche près de l'évier.",
        "narrateur|Un rai de soleil traverse le rouge.",
        "narrateur|Le point de beurre chauffe au soleil du bac.",
    ],
    (3, 3, 2): [
        "narrateur|Le pot est redescendu jusqu'à la porte.",
        "enfant-f|Papa l'a mis à notre menton.",
        "copine|On a cueilli ensemble, après.",
        "papa|Le bac vous a laissé le temps.",
        "maman|La terre sèche sur vos doigts.",
        "narrateur|Le tablier pose un peu de terre.",
        "copine|Elle brille trop, Chouchou.",
        "enfant-f|C'est pour ça.",
        "narrateur|Le point de beurre porte un peu de rouge.",
    ],
    (3, 3, 3): [
        "narrateur|Un peu de terre reste au seuil.",
        "enfant-f|On a pris celles d'en bas.",
        "copine|Sans trop monter.",
        "papa|Le bac a gardé les hautes.",
        "maman|Vos mains sentent le soleil.",
        "narrateur|Le tablier sèche près de l'évier.",
        "narrateur|Sarah pose sa part au rebord.",
        "enfant-f|Tu l'as goûtée, enfin.",
        "narrateur|Le point de beurre se tait, sur le plat.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "four,mouche",
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le bol bleu", "la cuillère", "le tablier")},
    )

    for a in (1, 2, 3):
        p = f"CHK_T0001_P000{a}"
        t1 = T1[a]
        out_chunks[p] = voice(by_src[p], t1["passage"], "action", t1["sons"], {"emphasis": t1["emphasis"]})
        out_chunks[f"{p}_Q0001"] = voice(
            by_src[f"{p}_Q0001"], t1["question"], "clue", "",
            {"emphasis": t1["emphasis"], "fields": t1["qfields"]},
        )
        out_chunks[f"{p}_C0001"] = voice(
            by_src[f"{p}_C0001"], t1["confirm"], "confirm", t1["sons"], {"emphasis": t1["emphasis"]},
        )
        out_chunks[f"{p}_T0002_P0000"] = voice(
            by_src[f"{p}_T0002_P0000"], t2_question(a), "choice", "",
            {"fields": t3lab("la table", "l'évier", "le bac")},
        )
        for b in (1, 2, 3):
            sp = f"{p}_T0002_P000{b}"
            t2 = T2[(a, b)]
            out_chunks[sp] = voice(
                by_src[sp], t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emphasis"]},
            )
            out_chunks[f"{sp}_T0003_P0000"] = voice(
                by_src[f"{sp}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab(*T3_LABS[b])},
            )
            for c in (1, 2, 3):
                leaf = f"{sp}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], T3[(a, b, c)], "resolution", T3_SONS[(b, c)],
                    {"emphasis": "point de beurre"},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ENDINGS[(a, b, c)], "ending", END_SONS[b],
                    {"emphasis": "point de beurre", "notes": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = set(out_chunks) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:6]} extra={sorted(extra)[:6]}")

    story = dict(src)
    story["fil_rouge"] = FIL
    story["title"] = TITLE
    story["characters"] = CHARS
    story["setting"] = SETTING
    story["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]

    check(SID, story["age_band"], story["chunks"])

    blob = "\n".join(c["script"] for c in story["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in story["chunks"]
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
        "hyperactif",
        "miel",
        "merle",
        "tout doux",
        "tout calme",
        "j'ai compris",
        "mission accomplie",
        "aujourd'hui,",
        "cristal de sucre brun",
        "grain de sel",
        "étoile brune",
        "fil pâle",
        "virgule farine",
        "larme de bronze",
        "citronnade",
        "pichet",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(blob):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "chouchou" not in blob:
        raise SystemExit(f"{SID}: Chouchou absente")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "point de beurre" not in blob:
        raise SystemExit(f"{SID}: point de beurre absent")
    if "tarte" not in blob:
        raise SystemExit(f"{SID}: tarte absente")

    fins = [c["text"] for c in story["chunks"] if c["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes {len(set(fins))}/27")
    lasts = []
    for c in story["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        lasts.append(last_n[-1])
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images {len(set(lasts))}/27")

    t3s = [c["text"] for c in story["chunks"] if re.search(r"T0003_P000[123]$", c["chunk_id"])]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"T3 distincts {len(set(t3s))}/27")

    t2s = [c["text"] for c in story["chunks"] if re.search(r"T0002_P000[123]$", c["chunk_id"])]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"T2 distincts {len(set(t2s))}/9")

    counts = [path_words(out_chunks, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    if any(c.get("text_xai_tags") == c.get("text") for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")
    if len(story["chunks"]) != 86:
        raise SystemExit(f"chunks {len(story['chunks'])}≠86")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.COR.003 — faire avec Sarah telle qu'elle est "
        "(lunettes, cheveux courts, manteau trop long) ; vécue, non dite\n"
        "- **Personnages :** Chouchou, Sarah, papa, maman\n"
        "- **Lieu :** cuisine jaune (fournil jaune), évier, bac du jardin\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés. Labels T1/T2/T3 gardés.\n\n"
        "## Promesse narrative\n\n"
        "Le four claque dans le jaune. Un **point de beurre** tient au bord du plat. "
        "Chouchou veut une tarte aux fraises pour Sarah, **maintenant**. "
        "Elle prend le bol bleu, la cuillère ou le tablier ; les trois restent. "
        "Sarah arrive telle qu'elle est. Chouchou propose, trop vite. Sarah prend son temps. "
        "Un silence compte. À la table le sucre manque sous la farine, à l'évier les fraises "
        "propres manquent, au bac les mûres restent trop haut. Elles refusent de foncer. "
        "Le point de beurre guide. Sarah goûte.\n\n"
        "## Vécu\n\n"
        "Chouchou veut la tarte **maintenant**. Papa et maman parlent. "
        "Sourire disparu, poitrine bousculée, adulte accroupi. "
        "Chaque choix change l'obstacle et le climax. La leçon se voit : "
        "on mélange avec les lunettes de Sarah, on accroche le manteau trop long, "
        "on cueille à la hauteur de ses mains. Pas de slogan. "
        "Indice d'ouverture payé : point de beurre. Fin : tarte + trace unique.\n\n"
        "## Vu et corrigé\n\n"
        "- Ancien merged F-NAR-016 sans notes/xai : tout réécrit.\n"
        "- Ouverture inventée (four qui claque, mouche sur le carnet), pas les 5 listées example4. "
        "« déjà » jeté.\n"
        "- Monde ≠ TREE-DIF-055 (citronnade, cristal) ≠ TREE-COL-022 (grain de sel).\n"
        "- T1 ne retire pas l'équipement. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (beurre vu). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes`. "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        f"- N1 ≤ 10. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks, 27 chemins, 27 fins distinctes, 27 dernières images\n"
        f"- {min(counts)} à {max(counts)} mots par chemin (moyenne {sum(counts)//len(counts)})\n"
        "- `text` = `script` collé ; graphe inchangé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
