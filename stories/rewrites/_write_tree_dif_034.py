#!/usr/bin/env python3
"""TREE-DIF-034 — Le soleil en papier d'Amir, à l'école (F-NAR-019, N3, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-034"
N3 = 16
TITLE = "Le soleil en papier d'Amir, à l'école"
FIL = (
    "Au vestiaire des manteaux, Amir veut accrocher son soleil en papier "
    "avant que le rai du matin quitte le linoléum. Une pastille de colle, "
    "ronde et froide, dort au milieu. Nino est plus grand, et ne veut pas "
    "la même chose au même moment. Ruban jaune, pince à linge, petit tabouret : "
    "tout voyage. Patères, fenêtre, grotte des tables : neuf façons. "
    "La pastille prend la lumière, enfin."
)
CHARS = "Amir, Nino, papa, maman"
SETTING = "école : vestiaire, classe, tables"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "pastille de colle",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_joyeuse; intensite=1; destinataire=enfant; sous_texte=le_soleil_en_papier_veut_monter; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_le_geste; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "pastille de colle",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_partent_ensemble; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=trop_court_le_papier_retombe; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": "pastille de colle",
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=leurs_tailles_ne_vont_pas_au_même_endroit; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "pastille de colle",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=petit_et_grand_trouvent_ensemble; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "pastille de colle",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_pastille_de_colle_prend_la_lumière; tempo=posé; sourire=léger; respiration=ample",
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


def vet(lines: list[str]) -> list[str]:
    out = []
    prev = ""
    run = 1
    for raw in lines:
        role, ph = raw.split("|", 1)
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
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"tic {tic!r}: {ph}")
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"tic {m.group(0)!r}: {ph}")
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


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    lines = vet(lines)
    m = dict(PROFILES[profile])
    extra = extra or {}
    emphasis = extra.get("emphasis", m["emphasis"])
    text, script = from_script(lines)
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


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


OPENING = [
    "narrateur|Amir connaît le vestiaire, ses casiers et son linoléum froid.",
    "narrateur|Le couloir sent la laine mouillée, et la craie.",
    "narrateur|Un détail paraît neuf, au milieu du papier.",
    "narrateur|Une pastille de colle dort, ronde et froide.",
    "papa|Tu as vu ce rond, Amir ?",
    "enfant-m|Il brille un peu, collé au soleil.",
    "maman|Le papier attend près des casiers.",
    "narrateur|En ce moment, Amir serre son soleil en papier.",
    "narrateur|La pastille reste froide, sous son pouce.",
    "enfant-m|Je veux l'accrocher haut, avant la lumière.",
    "narrateur|Nino arrive, plus grand, les épaules jusqu'à la poignée.",
    "copain|Moi, je touche les crochets d'abord !",
    "enfant-m|Non, le soleil d'abord, Nino.",
    "narrateur|Amir lève le papier vers un casier.",
    "narrateur|Le soleil penche, trop court, et retombe.",
    "narrateur|Le sourire d'Amir disparaît, un instant.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "papa|On prépare, puis on accroche.",
    "narrateur|Papa s'accroupit, à la hauteur d'Amir.",
    "papa|Merci, tu tiens le papier bien droit.",
    "maman|Ruban, pince, tabouret : on les prend.",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près des casiers.",
    "narrateur|Le ruban jaune, la pince, le petit tabouret.",
    "maman|Tu prends quoi d'abord, Amir ?",
]

T1 = {
    1: {
        "lab": "le ruban jaune",
        "sons": "ruban,colle",
        "emphasis": "ruban jaune",
        "passage": [
            "narrateur|Amir enroule le ruban jaune, un peu collant.",
            "enfant-m|Je le lance vers le casier !",
            "narrateur|Le jaune s'envole, trop court, et retombe.",
            "enfant-m|Il ne reste pas.",
            "maman|Glisse-le autour de ton poignet.",
            "narrateur|Le jaune froisse contre la manche.",
            "papa|La pince voyage dans la poche.",
            "narrateur|Nino tire le petit tabouret, toc.",
            "copain|Les crochets, moi, plus tard.",
            "enfant-m|Le soleil d'abord.",
            "papa|Le ruban d'abord, vous l'avez.",
            "maman|Les trois affaires partent ensemble.",
        ],
        "question": [
            "narrateur|Amir a glissé le ruban jaune autour du poignet.",
            "maman|C'est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "poignet",
            "accepted_examples": "poignet | le poignet | autour du poignet | son poignet",
            "retry_prompt": "Le ruban est autour du poignet.",
        },
        "confirm": [
            "enfant-m|Autour du poignet.",
            "papa|Oui.",
            "narrateur|La pince voyage dans la poche.",
            "narrateur|Le tabouret suit, derrière les pieds.",
            "copain|Il a trop de jaune !",
            "enfant-m|C'est pour notre soleil.",
            "maman|On avance, alors ?",
            "narrateur|La pastille de colle cogne le poignet, tiède.",
        ],
    },
    2: {
        "lab": "la pince à linge",
        "sons": "pince,bois",
        "emphasis": "pince à linge",
        "passage": [
            "narrateur|Amir prend la pince à linge, un peu tiède.",
            "enfant-m|Je pince le soleil au casier !",
            "narrateur|Le bois clique à vide, puis pince le doigt.",
            "enfant-m|Aïe, elle n'a rien pris.",
            "papa|Glisse-la dans ta poche, tout droit.",
            "narrateur|Un clic de bois, minuscule.",
            "maman|Le ruban, ensuite, autour du poignet.",
            "narrateur|Nino tire le petit tabouret, toc.",
            "copain|Je veux voir la cour, moi.",
            "enfant-m|Le soleil d'abord.",
            "maman|La pince d'abord, elle est prête.",
            "papa|Les trois affaires partent ensemble.",
        ],
        "question": [
            "narrateur|Amir a glissé la pince à linge dans la poche.",
            "papa|C'est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "poche",
            "accepted_examples": "poche | la poche | dans la poche | sa poche",
            "retry_prompt": "La pince est dans la poche.",
        },
        "confirm": [
            "enfant-m|Dans la poche.",
            "maman|Oui.",
            "narrateur|Le ruban voyage autour du poignet.",
            "narrateur|Le tabouret suit, derrière les pieds.",
            "copain|J'entends le clic !",
            "enfant-m|Ne la sors pas trop tôt.",
            "papa|On avance, alors ?",
            "narrateur|La pastille de colle écoute le clic, contre le papier.",
        ],
    },
    3: {
        "lab": "le petit tabouret",
        "sons": "tabouret,linoleum",
        "emphasis": "petit tabouret",
        "passage": [
            "narrateur|Amir tire le petit tabouret, un peu rêche.",
            "enfant-m|Je monte, et j'accroche !",
            "narrateur|Le bois accroche un casier, et gratte.",
            "enfant-m|Il ne passe pas.",
            "maman|Garde-le derrière tes pieds.",
            "narrateur|Les pieds du bois font un petit choc.",
            "papa|Le ruban et la pince voyagent avec vous.",
            "narrateur|Nino les pose près des casiers.",
            "copain|Moi je reste debout, plus haut.",
            "enfant-m|Le soleil d'abord.",
            "papa|Le tabouret d'abord, il est prêt.",
            "maman|Les trois affaires partent ensemble.",
        ],
        "question": [
            "narrateur|Amir a gardé le petit tabouret derrière les pieds.",
            "maman|C'est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "pieds",
            "accepted_examples": "pieds | les pieds | derrière les pieds | ses pieds",
            "retry_prompt": "Le tabouret est derrière les pieds.",
        },
        "confirm": [
            "enfant-m|Derrière les pieds.",
            "papa|Oui.",
            "narrateur|Le ruban voyage autour du poignet.",
            "narrateur|La pince voyage dans la poche.",
            "copain|Ça sent la colle.",
            "enfant-m|Le coin de départ est là.",
            "maman|On avance, alors ?",
            "narrateur|La pastille de colle tremble au moindre choc.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le ruban tape un peu le poignet, à chaque pas.",
        "narrateur|Aux patères, les crochets brillent trop haut.",
        "narrateur|À la fenêtre, le carreau clignote.",
        "narrateur|Sous les tables, l'ombre est basse.",
        "papa|On accroche où, pour le soleil ?",
    ],
    2: [
        "narrateur|La pince cliquette dans la poche, à chaque pas.",
        "narrateur|Aux patères, les crochets brillent trop haut.",
        "narrateur|À la fenêtre, le carreau clignote.",
        "narrateur|Sous les tables, l'ombre est basse.",
        "papa|On accroche où, pour le soleil ?",
    ],
    3: [
        "narrateur|Le tabouret cogne le linoléum, à chaque pas.",
        "narrateur|Aux patères, les crochets brillent trop haut.",
        "narrateur|À la fenêtre, le carreau clignote.",
        "narrateur|Sous les tables, l'ombre est basse.",
        "papa|On accroche où, pour le soleil ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "manteau,fermeture",
        "emphasis": "pastille de colle",
        "passage": [
            "narrateur|Le ruban accroche un crochet, trop haut.",
            "narrateur|Le vestiaire sent les manteaux mouillés.",
            "copain|Moi je touche, Amir !",
            "narrateur|Nino se hausse, trop vite.",
            "narrateur|Un manteau glisse, et cache le crochet.",
            "narrateur|Le jaune se coince dans une fermeture.",
            "enfant-m|On tire, alors ?",
            "narrateur|Il s'arrête, le poignet tendu.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Il pose les mains, ouvertes.",
            "maman|Le manteau a bougé, c'est tout.",
            "papa|Lui touche le haut, toi le bas.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 1): {
        "sons": "pince,fermeture",
        "emphasis": "pastille de colle",
        "passage": [
            "narrateur|Amir entend la pince taper un crochet, toc.",
            "narrateur|Le vestiaire sent les manteaux mouillés.",
            "copain|Moi je touche, Amir !",
            "narrateur|Nino se hausse, trop vite.",
            "narrateur|Un manteau glisse, et cache le crochet.",
            "narrateur|Le clic se perd entre les laines.",
            "enfant-m|On pince, alors ?",
            "narrateur|Il s'arrête, la poche ouverte.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Il pose les mains, ouvertes.",
            "maman|Le manteau a bougé, c'est tout.",
            "papa|Lui touche le haut, toi le bas.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 1): {
        "sons": "tabouret,casier",
        "emphasis": "pastille de colle",
        "passage": [
            "narrateur|Le tabouret bute contre un casier.",
            "narrateur|Le vestiaire sent les manteaux mouillés.",
            "copain|Moi je touche, Amir !",
            "narrateur|Nino se hausse, trop vite.",
            "narrateur|Un manteau glisse, et cache le crochet.",
            "narrateur|Le bois du tabouret prend une goutte froide.",
            "enfant-m|On pousse, alors ?",
            "narrateur|Il s'arrête, les talons contre le bois.",
            "enfant-m|On ne fonce pas.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Il pose les mains, ouvertes.",
            "maman|Le manteau a bougé, c'est tout.",
            "papa|Lui touche le haut, toi le bas.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 2): {
        "sons": "vitre,buée",
        "emphasis": "pastille de colle",
        "passage": [
            "narrateur|Le ruban se colle au carreau, trop haut.",
            "enfant-m|Le carreau est à nous, Nino.",
            "copain|Je vois la cour, tout haut !",
            "narrateur|La poignée reste trop loin pour Amir.",
            "narrateur|Le jaune reste trop bas, sous la poignée.",
            "narrateur|Une buée cerne la pastille de colle.",
            "enfant-m|On saute, alors ?",
            "narrateur|Il referme la bouche.",
            "enfant-m|Attends, Nino.",
            "narrateur|Nino ferme la bouche.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|Ses bras vont jusqu'à la poignée.",
            "papa|Toi tu vois le radiateur, lui la cour.",
            "papa|Vous trouvez, tous les deux ?",
        ],
    },
    (2, 2): {
        "sons": "pince,vitre",
        "emphasis": "pastille de colle",
        "passage": [
            "narrateur|Amir voit la pince glisser vers la poignée.",
            "enfant-m|Le carreau est à nous, Nino.",
            "copain|Je vois la cour, tout haut !",
            "narrateur|La poignée reste trop loin pour Amir.",
            "narrateur|Le clic n'atteint pas le loquet.",
            "narrateur|Une buée cerne la pastille de colle.",
            "enfant-m|On pince le verre, alors ?",
            "narrateur|Il referme la bouche.",
            "enfant-m|Attends, Nino.",
            "narrateur|Nino ferme la bouche.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|Ses bras vont jusqu'à la poignée.",
            "papa|Toi tu vois le radiateur, lui la cour.",
            "papa|Vous trouvez, tous les deux ?",
        ],
    },
    (3, 2): {
        "sons": "tabouret,radiateur",
        "emphasis": "pastille de colle",
        "passage": [
            "narrateur|Le tabouret se coince sous le radiateur.",
            "enfant-m|Le carreau est à nous, Nino.",
            "copain|Je vois la cour, tout haut !",
            "narrateur|La poignée reste trop loin pour Amir.",
            "narrateur|Le tabouret n'aide pas, trop court, tout seul.",
            "narrateur|Une buée cerne la pastille de colle.",
            "enfant-m|On pousse le bois, alors ?",
            "narrateur|Il referme la bouche.",
            "enfant-m|Attends, Nino.",
            "narrateur|Nino ferme la bouche.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|Ses bras vont jusqu'à la poignée.",
            "papa|Toi tu vois le radiateur, lui la cour.",
            "papa|Vous trouvez, tous les deux ?",
        ],
    },
    (1, 3): {
        "sons": "table,craie",
        "emphasis": "pastille de colle",
        "passage": [
            "narrateur|Le ruban rampe sous une table, trop bas.",
            "enfant-m|Ici, ça sent la craie, Nino.",
            "copain|Je me glisse, trop large !",
            "narrateur|Ses épaules butent contre le bois des tables.",
            "narrateur|Le jaune prend la poussière du linoléum.",
            "narrateur|La pastille de colle s'éteint, dans l'ombre.",
            "enfant-m|On force, alors ?",
            "narrateur|Sa voix se casse, trop pressée.",
            "enfant-m|Pas trop vite.",
            "narrateur|Nino reste debout, sans répondre.",
            "narrateur|Il regarde ses épaules.",
            "maman|Il a les épaules trop larges, c'est tout.",
            "papa|Toi tu passes, lui pas.",
            "papa|Vous trouvez, tous les deux ?",
        ],
    },
    (2, 3): {
        "sons": "pince,chaise",
        "emphasis": "pastille de colle",
        "passage": [
            "narrateur|Amir voit la pince rouler sous une chaise, toc.",
            "enfant-m|Ici, ça sent la craie, Nino.",
            "copain|Je me glisse, trop large !",
            "narrateur|Ses épaules butent contre le bois des tables.",
            "narrateur|Le clic se perd entre les pieds de chaise.",
            "narrateur|La pastille de colle s'éteint, dans l'ombre.",
            "enfant-m|On rattrape, alors ?",
            "narrateur|Sa voix se casse, trop pressée.",
            "enfant-m|Pas trop vite.",
            "narrateur|Nino reste debout, sans répondre.",
            "narrateur|Il regarde ses épaules.",
            "maman|Il a les épaules trop larges, c'est tout.",
            "papa|Toi tu passes, lui pas.",
            "papa|Vous trouvez, tous les deux ?",
        ],
    },
    (3, 3): {
        "sons": "tabouret,table",
        "emphasis": "pastille de colle",
        "passage": [
            "narrateur|Le tabouret bute contre un pied de table.",
            "enfant-m|Ici, ça sent la craie, Nino.",
            "copain|Je me glisse, trop large !",
            "narrateur|Ses épaules butent contre le bois des tables.",
            "narrateur|Le bois gratte, puis s'arrête, coincé.",
            "narrateur|La pastille de colle s'éteint, dans l'ombre.",
            "enfant-m|On pousse plus fort, alors ?",
            "narrateur|Sa voix se casse, trop pressée.",
            "enfant-m|Pas trop vite.",
            "narrateur|Nino reste debout, sans répondre.",
            "narrateur|Il regarde ses épaules.",
            "maman|Il a les épaules trop larges, c'est tout.",
            "papa|Toi tu passes, lui pas.",
            "papa|Vous trouvez, tous les deux ?",
        ],
    },
}

T3_LABS = {
    1: ("les bras de Nino", "le tabouret d'Amir", "la pince ensemble"),
    2: ("la poignée de Nino", "le tabouret du radiateur", "le rebord ensemble"),
    3: ("le passage d'Amir", "soulever la table", "un dessous un dessus"),
}

T3_CHOICE = {
    1: [
        "narrateur|Les patères attendent, trop haut.",
        "narrateur|La pastille de colle s'est perdue dans la laine.",
        "papa|Les bras, le tabouret, ou la pince ensemble ?",
    ],
    2: [
        "narrateur|La poignée attend, trop loin.",
        "narrateur|La pastille de colle s'est ternie derrière la buée.",
        "maman|La poignée, le tabouret, ou le rebord ?",
    ],
    3: [
        "narrateur|L'ombre sous les tables attend.",
        "narrateur|La pastille de colle s'est cachée dans la poussière.",
        "papa|Le passage, soulever, ou un dessous un dessus ?",
    ],
}

T3_SONS = {
    (1, 1): "bras,crochet",
    (1, 2): "tabouret,bois",
    (1, 3): "pince,manteau",
    (2, 1): "poignee,vitre",
    (2, 2): "tabouret,radiateur",
    (2, 3): "rebord,loquet",
    (3, 1): "ramper,craie",
    (3, 2): "table,bois",
    (3, 3): "chaise,voix",
}

T3_EMPH = {
    1: {1: "bras", 2: "tabouret", 3: "pince"},
    2: {1: "poignée", 2: "radiateur", 3: "rebord"},
    3: {1: "passage", 2: "table", 3: "dessous"},
}

OBJ_LINE = {
    1: "Le ruban jaune attend, collé au poignet.",
    2: "La pince à linge attend, dans la poche.",
    3: "Le petit tabouret attend, derrière les pieds.",
}


def t3_pass(a: int, b: int, c: int) -> list[str]:
    obj = OBJ_LINE[a]
    if b == 1 and c == 1:
        use = {
            1: "Amir tend le ruban, bras trop courts.",
            2: "Amir tend la pince, bras trop courts.",
            3: "Amir pousse le tabouret, tout près.",
        }[a]
        return [
            "enfant-m|Attends.",
            "narrateur|Amir regarde la pastille de colle, au milieu.",
            "copain|Mes bras, alors.",
            "narrateur|Nino lève le soleil, assez haut.",
            f"narrateur|{use}",
            "enfant-m|Je tiens le bas !",
            "narrateur|Le papier glisse, faillit tomber.",
            "narrateur|La pastille de colle rattrape la lumière.",
            f"narrateur|{obj}",
            "papa|Tes bras allaient assez loin.",
            "enfant-m|Il est à nous.",
        ]
    if b == 1 and c == 2:
        wait = {
            1: "Le ruban attend au bord, plein d'ombre.",
            2: "La pince attend au bord, un peu ronde.",
            3: "Le tabouret attend au bord, un peu chaud.",
        }[a]
        return [
            "enfant-m|Je monte, Nino.",
            "papa|Tiens le bois, Amir.",
            "narrateur|Amir se hausse, plus petit que le crochet.",
            "copain|Moi je guide, tout près.",
            "narrateur|Nino tient le soleil, au-dessus.",
            "narrateur|Le papier glisse vers le métal.",
            "narrateur|La pastille de colle revoit le rai, enfin.",
            f"narrateur|{wait}",
            f"narrateur|{obj}",
            "maman|Vous le partagez, à deux hauteurs.",
            "copain|Il est à toi, un moment.",
        ]
    if b == 1 and c == 3:
        catch = {
            1: "Le ruban pince le manteau, sans tirer.",
            2: "La pince attrape le papier, clic.",
            3: "Le tabouret serre le bas, toc.",
        }[a]
        return [
            "enfant-m|On pince un peu.",
            "copain|Moi aussi, je pince.",
            "narrateur|Nino lève un manteau, tout haut.",
            "narrateur|Amir glisse le soleil, pendant l'ouverture.",
            f"narrateur|{catch}",
            "narrateur|La pastille de colle échappe à la laine.",
            f"narrateur|{obj}",
            "papa|Il est venu vers vous.",
            "copain|On l'a repris.",
            "enfant-m|Il brille, maintenant.",
            "maman|Vos cheveux sentent le manteau mouillé.",
        ]
    if b == 2 and c == 1:
        carry = {
            1: "Nino pose le ruban contre le carreau.",
            2: "Nino pose la pince contre le carreau.",
            3: "Nino pose le tabouret contre le mur.",
        }[a]
        return [
            "copain|Je me hausse, d'ici.",
            "enfant-m|Je tiens le papier, d'en bas.",
            "narrateur|Les doigts de Nino touchent la poignée.",
            "copain|Elle bouge !",
            "narrateur|Le soleil penche, puis s'accroche.",
            f"narrateur|{carry}",
            "narrateur|La pastille de colle perce la buée, ronde.",
            f"narrateur|{obj}",
            "papa|Tes doigts allaient assez loin.",
            "maman|Amir tenait bien le bas.",
            "copain|Il est à nous.",
        ]
    if b == 2 and c == 2:
        up = {
            1: "Amir pose le ruban sur le tabouret.",
            2: "Amir pose la pince sur le tabouret.",
            3: "Amir pousse le tabouret, tout près.",
        }[a]
        return [
            "enfant-m|On monte sur le tabouret ?",
            "copain|Oui, près du radiateur.",
            f"narrateur|{up}",
            "narrateur|Papa tient le radiateur, bien ferme.",
            "narrateur|Amir et Nino se haussent ensemble.",
            "enfant-m|Je vois la cour !",
            "copain|Je la sens.",
            "narrateur|La pastille de colle se réchauffe, au fer.",
            f"narrateur|{obj}",
            "maman|Vous avez regardé ensemble.",
            "papa|Le tabouret est resté stable.",
        ]
    if b == 2 and c == 3:
        two = {
            1: "Nino tend le ruban, bras tout longs.",
            2: "Nino tend la pince, bras tout longs.",
            3: "Nino pousse le tabouret, tout près.",
        }[a]
        return [
            "enfant-m|Reste en haut, Nino.",
            "copain|Je tends, d'ici.",
            f"narrateur|{two}",
            "narrateur|Nino fait basculer le loquet, sans forcer.",
            "narrateur|Le rebord prend Amir, puis lui.",
            "enfant-m|Je le tiens !",
            "narrateur|La pastille de colle frôle le carreau, enfin.",
            f"narrateur|{obj}",
            "papa|Chacun a fait sa part.",
            "copain|Il sent la craie.",
            "maman|Vos bras n'avaient pas la même longueur.",
        ]
    if b == 3 and c == 1:
        use = {
            1: "Amir pousse le ruban sous les tables.",
            2: "Amir glisse la pince sous le bois.",
            3: "Amir pousse le tabouret sous le bord.",
        }[a]
        return [
            "enfant-m|Je passe, Nino.",
            "narrateur|Amir rampe, tout petit, sous la table.",
            "copain|Doucement.",
            f"narrateur|{use}",
            "narrateur|Ses doigts trouvent une craie perdue.",
            "enfant-m|Je la tiens !",
            "narrateur|La pastille de colle reprend un rai, bas.",
            f"narrateur|{obj}",
            "papa|Tes épaules étaient assez petites.",
            "narrateur|Une grotte de lumière s'ouvre, à eux.",
            "copain|Regarde, Amir.",
        ]
    if b == 3 and c == 2:
        catch = {
            1: "Le ruban soulève la poussière, un peu.",
            2: "La pince soulève un clic, tout bas.",
            3: "Le tabouret soulève un coin, toc.",
        }[a]
        return [
            "enfant-m|On soulève un peu.",
            "copain|Moi aussi, je soulève.",
            "narrateur|Nino lève le bord de la table, un peu.",
            "narrateur|Amir se glisse, pendant l'ouverture.",
            f"narrateur|{catch}",
            "narrateur|La pastille de colle quitte l'ombre, d'un coup.",
            f"narrateur|{obj}",
            "papa|Il est venu vers vous.",
            "copain|On l'a repris.",
            "enfant-m|Il brille, maintenant.",
            "maman|Vos cheveux sentent la craie.",
        ]
    nest = {
        1: "Le ruban devient un nid, contre le bois.",
        2: "La pince devient un nid, contre le bois.",
        3: "Le tabouret devient un nid, contre le bois.",
    }[a]
    return [
        "enfant-m|Papa, écarte un peu ?",
        "papa|Je fais un chemin, sans forcer.",
        "narrateur|Une chaise s'ouvre, comme une aile.",
        "narrateur|Amir rentre, Nino reste dehors.",
        f"narrateur|{nest}",
        "copain|On se parle à travers.",
        "enfant-m|Oui.",
        "narrateur|La pastille de colle tient le secret, au milieu.",
        f"narrateur|{obj}",
        "maman|Vous y arrivez, tous les deux.",
        "narrateur|Deux voix tiennent le même secret.",
    ]


LAST = {
    (1, 1, 1): "La pastille de colle s'endort sur le crochet.",
    (1, 1, 2): "Sur le tabouret, la pastille garde une paillette de laine.",
    (1, 1, 3): "La pince tient la pastille, comme une graine.",
    (1, 2, 1): "Un rai traverse la pastille, contre le carreau.",
    (1, 2, 2): "Le fer du radiateur réchauffe la pastille de colle.",
    (1, 2, 3): "Le rebord garde la pastille, petite et chaude.",
    (1, 3, 1): "Sous le bois, la pastille brille comme une graine.",
    (1, 3, 2): "Le bord redescend, la pastille reste au chaud.",
    (1, 3, 3): "Deux voix tiennent la pastille, à travers la table.",
    (2, 1, 1): "La pince veille au bas, pastille au milieu.",
    (2, 1, 2): "Un clic de bois s'éteint près de la pastille.",
    (2, 1, 3): "La laine sèche contre la pastille de colle.",
    (2, 2, 1): "La pastille chauffe contre la vitre, ronde.",
    (2, 2, 2): "Une ombre de pastille danse au radiateur.",
    (2, 2, 3): "Une buée cerne la pastille, puis part.",
    (2, 3, 1): "Un clic bas s'éteint dans la grotte, près de la pastille.",
    (2, 3, 2): "Un rayon veille près des chaises, sur la pastille.",
    (2, 3, 3): "Sous le bois, la pastille chauffe le jaune de la pince.",
    (3, 1, 1): "Le tabouret veille au bas, pastille au crochet.",
    (3, 1, 2): "Le bois du tabouret garde une pastille tiède.",
    (3, 1, 3): "Une goutte de laine sèche sur la pastille.",
    (3, 2, 1): "Le loquet se tait, et la pastille brille.",
    (3, 2, 2): "Deux pieds s'arrêtent, la pastille au milieu.",
    (3, 2, 3): "Le papier tremble, la pastille se tait.",
    (3, 3, 1): "La poussière redevient grise, autour de la pastille.",
    (3, 3, 2): "Un rai orange s'endort sous le bois, sur la pastille.",
    (3, 3, 3): "Une chaise redevient une chaise, près de la pastille.",
}

HARD = {
    1: "Le manteau a failli garder le soleil.",
    2: "La buée a failli cacher la pastille.",
    3: "La table a failli fermer le passage.",
}

CODA = {
    1: "Le ruban jaune reste autour du poignet.",
    2: "La pince à linge rentre dans la poche.",
    3: "Le petit tabouret veille au bas.",
}

TRACE = {
    1: "Un rai jaune s'allonge sur le linoléum, puis s'arrête.",
    2: "Au couloir, ça sent la colle, tiède.",
    3: "Au loin, la cloche du préau se tait.",
}


def ending(a: int, b: int, c: int) -> list[str]:
    last = LAST[(a, b, c)]
    hard = HARD[b]
    coda = CODA[a]
    trace = TRACE[c]
    if b == 1 and c == 1:
        return [
            "narrateur|Aux patères, le soleil sent la laine mouillée.",
            "copain|Tu tenais le bas, moi j'accrochais.",
            "enfant-m|Tes bras l'ont fait monter.",
            f"narrateur|{hard}",
            "papa|Vous l'avez, enfin.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 1 and c == 2:
        return [
            "narrateur|Sur le tabouret, deux têtes se posent.",
            "enfant-m|Nino, tu l'as vue glisser.",
            "copain|Oui, tout près de tes mains.",
            f"narrateur|{hard}",
            "papa|Toi en bas, lui au-dessus, ça tenait.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 1 and c == 3:
        return [
            "narrateur|Le manteau redescend, sans bruit.",
            "copain|Il est tombé vers nous.",
            "enfant-m|On a pincé, tous les deux.",
            f"narrateur|{hard}",
            "maman|Il n'était plus trop coincé.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 1:
        return [
            "narrateur|À la fenêtre, le soleil sent le carreau.",
            "enfant-m|Tu l'as fait pencher pour moi.",
            "copain|Tu tenais le bas.",
            f"narrateur|{hard}",
            "papa|Le soleil est à vous, maintenant.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 2:
        return [
            "narrateur|Sur le tabouret, deux paires de pieds se touchent.",
            "copain|Tu l'as posé, d'en bas.",
            "enfant-m|Tes bras l'ont fait descendre.",
            f"narrateur|{hard}",
            "papa|Chacun a fait sa part, à sa hauteur.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 3:
        return [
            "narrateur|Un peu de buée reste au carreau.",
            "enfant-m|On a tiré ensemble.",
            "copain|Sans trop monter.",
            f"narrateur|{hard}",
            "papa|Le rebord est resté à sa place.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 3 and c == 1:
        return [
            "narrateur|Sous la table, la grotte sent le bois.",
            "copain|Tu es passé, moi je gardais.",
            "enfant-m|Tes épaules l'ont laissé ouvert.",
            f"narrateur|{hard}",
            "papa|Vous l'avez, enfin.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    if b == 3 and c == 2:
        return [
            "narrateur|Le bord de table redescend, sans bruit.",
            "copain|Il est tombé vers nous.",
            "enfant-m|On a soulevé, tous les deux.",
            f"narrateur|{hard}",
            "maman|Il n'était plus trop coincé.",
            f"narrateur|{coda}",
            f"narrateur|{trace}",
            f"narrateur|{last}",
        ]
    return [
        "narrateur|Deux têtes se parlent, à travers le bois.",
        "copain|On s'est parlé à travers.",
        "papa|La table vous a laissé la place.",
        f"narrateur|{hard}",
        "maman|Le secret tient, tout chaud.",
        f"narrateur|{coda}",
        f"narrateur|{trace}",
        f"narrateur|{last}",
    ]


END_SONS = {1: "laine,cloche", 2: "vitre,colle", 3: "bois,craie"}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "cloche,laine,craie",
        {"emphasis": "pastille de colle"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le ruban jaune", "la pince à linge", "le petit tabouret"), "pause_before": 200},
    )

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        out_chunks[base] = voice(
            by_src[base], T1[a]["passage"], "action", T1[a]["sons"],
            {"emphasis": T1[a]["emphasis"]},
        )
        out_chunks[f"{base}_Q0001"] = voice(
            by_src[f"{base}_Q0001"], T1[a]["question"], "clue", "",
            {"fields": T1[a]["qfields"], "emphasis": T1[a]["emphasis"]},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], T1[a]["confirm"], "confirm", T1[a]["sons"],
            {"emphasis": "pastille de colle"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("les patères", "la fenêtre", "sous les tables"), "pause_before": 200},
        )
        for b in (1, 2, 3):
            bse = f"{base}_T0002_P000{b}"
            out_chunks[bse] = voice(
                by_src[bse], T2[(a, b)]["passage"], "obstacle", T2[(a, b)]["sons"],
                {"emphasis": T2[(a, b)]["emphasis"]},
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab(*T3_LABS[b]), "pause_before": 200},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], t3_pass(a, b, c), "resolution", T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ending(a, b, c), "ending", END_SONS[a],
                    {"emphasis": "pastille de colle"},
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
        "zoé",
        "zoe",
        "sami",
        "tom ",
        "léa",
        "tout doux",
        "tout calme",
        "tout lent",
        "aujourd'hui",
        "merle",
        "couleur de miel",
        "j'ai une idée",
        "j'ai compris",
        "mission accomplie",
        "on dirait que notre mission",
        "il faut attendre",
        "ancre minuscule",
        "étoile brune",
        "fil pâle",
        "virgule d'or",
        "croissant de buée",
        "fil blanc",
        "perle de verre",
        "cran en croissant",
        "œillet de cuivre",
        "oeillet de cuivre",
        "virgule de farine",
        "marque fine",
        "ombre en forme de flèche",
        "minuscule symbole",
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "drap à pois",
        "cabane",
        "chambre",
        "pommier",
        "maîtresse",
        "jardinier",
        "grand-père",
        "tailles différentes",
        "plus petit ou plus grand",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "amir" not in blob:
        raise SystemExit(f"{SID}: Amir absent")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "pastille de colle" not in blob:
        raise SystemExit(f"{SID}: indice pastille de colle absent")
    if "enfant-m|" not in blob:
        raise SystemExit(f"{SID}: enfant-m absent")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: copain absent")
    if blob.count("merci") > 3:
        raise SystemExit(f"{SID}: merci refrain ×{blob.count('merci')}")

    fins = [c["text"] for c in story["chunks"] if c["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes {len(set(fins))}/27")
    lasts = []
    for c in story["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(last_n[-1])
        low = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in low or "bravo" in low or "bon travail" in low:
            raise SystemExit(f"fin mécanique: {last_n[-1]}")
        if "pastille" not in low:
            raise SystemExit(f"fin sans pastille: {last_n[-1]}")
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
    if min(counts) < 500:
        raise SystemExit(f"chemins trop courts: {min(counts)}")
    if max(counts) > 780:
        raise SystemExit(f"chemins trop longs: {max(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-034 — Le soleil en papier d'Amir, à l'école\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.COR.001 — tailles différentes / jouer ensemble "
        "(vécue, jamais dite)\n"
        "- **Personnages :** Amir, Nino, papa, maman\n"
        "- **Lieu :** école : vestiaire, classe, tables\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Amir connaît le vestiaire. Un détail paraît neuf : une pastille de colle, "
        "ronde et froide, au milieu du soleil en papier. Il veut l'accrocher haut "
        "avant que le rai du matin quitte le linoléum. Nino, plus grand, veut toucher "
        "les crochets d'abord. Amir lève trop court : le papier retombe. "
        "Ruban, pince, tabouret : les trois partent. Patères (manteau, fermeture), "
        "fenêtre (buée, poignée), grotte des tables (épaules trop larges). "
        "Bras de Nino, tabouret d'Amir, pince ensemble ; poignée, tabouret du radiateur, "
        "rebord ; passage, soulever, un dessous un dessus. "
        "La pastille prend la lumière, avec une trace.\n\n"
        "## Vécu\n\n"
        "Amir veut le soleil **haut, maintenant**. Nino ne veut pas la même chose. "
        "Première idée : le lancer vers un casier. Ça rate. "
        "Chaque choix change l'obstacle et le climax (laine, buée, ombre). "
        "La leçon se voit : on ne change pas Nino, on change le geste. "
        "Petit et grand trouvent ensemble. "
        "Fin : pastille de colle + image unique du chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Zoé / Tom / Léa / Sami / bac-toboggan / « on va apprendre » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Héros Amir (`enfant-m`), Nino (`copain`), rythmes distincts, silence = réponse.\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'action. 9 T2, 27 T3, 27 fins.\n"
        "- Indice unique : pastille de colle (ouverture + climax). "
        "Pas d'ancre / étoile / fil pâle / marque fine.\n"
        "- Ouverture inventée : l'enfant connaît le vestiaire ; un détail paraît neuf.\n"
        "- Corps : sourire parti ; envie et inquiétude ; papa s'accroupit.\n"
        "- Merci vécu (ouverture). Question d'adulte. Un « en ce moment ».\n"
        "- Monde ≠ TREE-DIF-032 (pas de cabane, drap à pois, chambre sous la pluie).\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
