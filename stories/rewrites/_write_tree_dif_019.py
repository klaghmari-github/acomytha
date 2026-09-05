#!/usr/bin/env python3
"""TREE-DIF-019 — La petite boutique de Sarah et Nino (F-NAR-019, N2, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-019"
N2 = 15
TITLE = "La petite boutique de Sarah et Nino"
FIL = (
    "Sous la toile rayée du marché, Sarah tient une pêche tiède au croissant pâle. "
    "Elle veut ouvrir une petite boutique avec Nino avant que les caisses se taisent. "
    "Sarah plante ; Nino veut courir. T1 = bac / toboggan / balançoires. "
    "T2 = ballon / seau / doudou : l'aide trop vite fait pencher l'étal. "
    "T3 = jouer, attendre, ou tendre à papa ou maman. "
    "Le croissant pâle retrouve le soleil. Ils croquent."
)
CHARS = "Sarah, Nino, papa, maman"
SETTING = "le marché du village, puis l'aire de jeux derrière les toiles"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "croissant pâle",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=la boutique attend et Nino veut courir; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change le geste; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_où_va_la_pêche; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "pêche",
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=la_première_idée_a_raté; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=Sarah_plante_Nino_court; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_et_découragement; intensite=2; destinataire=enfant; sous_texte=l_aide_trop_vite_fait_pencher; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "croissant pâle",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=jouer_attendre_ou_demander_sans_forcer; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "pêche",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_croissant_pâle_et_le_jus_paient_le_début; tempo=posé; sourire=léger; respiration=ample",
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
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
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
    "narrateur|Sarah connaît le marché du village, ses toiles rayées.",
    "narrateur|Les caisses claquent sur les pavés chauds.",
    "narrateur|Un filet d'eau court, mince, au robinet.",
    "narrateur|Ça sent le sucré, mêlé à la poussière chaude.",
    "papa|Tu entends les caisses, Sarah ?",
    "enfant-f|Elles font toc, papa.",
    "narrateur|Un détail paraît nouveau, sous la toile.",
    "narrateur|Une pêche tiède, avec un croissant pâle.",
    "narrateur|La peau est rêche, un peu sucrée.",
    "narrateur|Une abeille tourne autour d'une caisse de bois.",
    "maman|Nino arrive, son sac rouge tape sa jambe.",
    "narrateur|Un linge à carreaux dépasse du panier.",
    "narrateur|Le panier cogne la hanche de maman.",
    "narrateur|Les pieds de Nino tapent le pavé, tap tap.",
    "copain|On court à l'aire !",
    "enfant-f|Moi, je veux une boutique, comme les stands.",
    "narrateur|En ce moment, Sarah serre la pêche.",
    "narrateur|Son sourire vacille quand Nino veut courir.",
    "papa|Les caisses vont se taire, bientôt.",
    "maman|Merci, tu la tiens, la pêche.",
    "enfant-f|On l'ouvre ensemble, Nino.",
    "papa|On l'ouvre où, cette boutique ?",
]

T1_CHOICE = [
    "narrateur|Derrière les toiles, l'aire attend.",
    "narrateur|La pêche tiède voyage avec eux.",
    "narrateur|Le bac, le toboggan, les balançoires.",
    "papa|Tu vas où, d'abord, Sarah ?",
]

T1 = {
    1: {
        "lab": "le bac à sable",
        "sons": "sable,caisses",
        "emphasis": "sable",
        "passage": [
            "narrateur|Sarah court vers le bac à sable.",
            "narrateur|Le sable est tiède, un peu rêche.",
            "enfant-f|Ici, on plante la boutique !",
            "copain|J'arrive !",
            "narrateur|Nino saute dans le bac, les deux pieds.",
            "narrateur|Un nuage de sable s'élève, très fin.",
            "papa|Tes pieds dansent, Nino.",
            "narrateur|Le sourire de Sarah disparaît.",
            "enfant-f|Ma pêche penche !",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Je m'accroupis, à ta hauteur.",
            "narrateur|Sarah creuse un trou, trop vite.",
            "copain|Plus profond !",
            "maman|On l'ouvre d'ici, alors ?",
        ],
        "question": [
            "narrateur|Sarah a posé la pêche dans le bac.",
            "maman|Elle l'a posée où ?",
        ],
        "qfields": {
            "expected_answer": "dans le bac",
            "accepted_examples": "bac | le bac | dans le bac | dans le sable | sable | au bac",
            "retry_prompt": "La pêche est dans le bac. Elle l'a posée où ?",
        },
        "confirm": [
            "enfant-f|Dans le bac.",
            "maman|Oui.",
            "narrateur|La pêche dort, le croissant pâle vers le ciel.",
            "copain|Mes pieds veulent sauter.",
            "narrateur|Nino se tait, une seconde.",
            "enfant-f|La boutique, elle, reste sage.",
            "papa|Un objet du jeu, peut-être ?",
            "maman|Le ballon, le seau, ou le doudou.",
            "enfant-f|Pour ouvrir, avec Nino.",
        ],
    },
    2: {
        "lab": "le toboggan",
        "sons": "metal,pas",
        "emphasis": "pêche",
        "passage": [
            "narrateur|Sarah court vers le toboggan.",
            "narrateur|Le métal est chaud, un peu lisse.",
            "enfant-f|On livre la pêche, en glissant !",
            "copain|Moi je suis le client !",
            "narrateur|Nino dévale les marches, toc toc toc.",
            "papa|Les marches sont chaudes, Nino.",
            "narrateur|Il s'assoit en bas, puis se relève.",
            "narrateur|Ses pieds tapent le sol, sans s'arrêter.",
            "enfant-f|Attends, je la glisse !",
            "copain|Plus vite, Sarah !",
            "narrateur|Sarah sent ses épaules se crisper.",
            "maman|La pêche n'a pas glissé.",
            "papa|On reste un moment, ici ?",
        ],
        "question": [
            "narrateur|Nino attend la pêche, tout en bas.",
            "papa|Nino attend où ?",
        ],
        "qfields": {
            "expected_answer": "en bas",
            "accepted_examples": "en bas | bas | au bas | sous le toboggan | en bas du toboggan",
            "retry_prompt": "Nino attend en bas. Il attend où ?",
        },
        "confirm": [
            "enfant-f|En bas.",
            "papa|Oui.",
            "narrateur|Nino lève les yeux, sans parler.",
            "copain|Mes pieds veulent remonter.",
            "enfant-f|La pêche n'a pas glissé.",
            "maman|On prend un objet, alors ?",
            "papa|Le ballon, le seau, ou le doudou.",
            "enfant-f|Oui, pour la livraison.",
            "narrateur|Le croissant pâle brille dans sa main.",
        ],
    },
    3: {
        "lab": "les balançoires",
        "sons": "chaine,tissu",
        "emphasis": "linge",
        "passage": [
            "narrateur|Sarah court vers les balançoires.",
            "narrateur|La chaîne est froide, un peu rêche.",
            "enfant-f|L'enseigne, c'est le linge !",
            "copain|Je la fais voler !",
            "narrateur|Nino pousse le siège, très fort.",
            "narrateur|La chaîne chante un petit cri.",
            "maman|Tes pieds donnent trop d'élan, Nino.",
            "narrateur|Sarah noue le linge à carreaux.",
            "narrateur|Il pend, et il claque au vent.",
            "enfant-f|Boutique ouverte !",
            "copain|Plus haut !",
            "narrateur|Le nœud se desserre, un peu.",
            "narrateur|Sarah serre le linge, trop fort.",
            "papa|On accroche comment, alors ?",
        ],
        "question": [
            "narrateur|Sarah a noué le linge à la chaîne.",
            "maman|Le linge pend où ?",
        ],
        "qfields": {
            "expected_answer": "à la chaîne",
            "accepted_examples": "chaîne | chaine | la chaîne | à la chaîne | sur la balançoire | balançoire",
            "retry_prompt": "Le linge pend à la chaîne. Il pend où ?",
        },
        "confirm": [
            "enfant-f|À la chaîne.",
            "maman|Oui.",
            "narrateur|Le linge claque, trop fort.",
            "copain|Je veux la faire danser.",
            "narrateur|Nino regarde le nœud, sans un mot.",
            "enfant-f|L'enseigne a besoin d'un objet.",
            "papa|Le ballon, le seau, ou le doudou.",
            "maman|Tu choisis, Sarah.",
            "enfant-f|On choisit ensemble.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Au bac, la boutique n'est pas là.",
        "narrateur|Près des caisses, le ballon attend.",
        "narrateur|Un seau goutte un peu, tout près.",
        "narrateur|Du sac de Nino, le doudou dépasse.",
        "papa|Tu prends quoi, pour ouvrir ?",
    ],
    2: [
        "narrateur|Sur le toboggan, rien n'a glissé.",
        "narrateur|Près des caisses, le ballon attend.",
        "narrateur|Un seau goutte un peu, tout près.",
        "narrateur|Du sac de Nino, le doudou dépasse.",
        "papa|Tu prends quoi, pour livrer ?",
    ],
    3: [
        "narrateur|À la balançoire, l'enseigne n'est pas prête.",
        "narrateur|Près des caisses, le ballon attend.",
        "narrateur|Un seau goutte un peu, tout près.",
        "narrateur|Du sac de Nino, le doudou dépasse.",
        "papa|Tu prends quoi, pour l'enseigne ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "ballon,sable",
        "emphasis": "ballon",
        "passage": [
            "narrateur|Nino voit le ballon dans le sable.",
            "copain|Moi je le fais rouler !",
            "narrateur|Son pied part, trop vite.",
            "narrateur|Le ballon rentre dans le petit trou.",
            "enfant-f|Il penche ma pêche !",
            "papa|Tes pieds l'ont trouvé, Nino.",
            "maman|La boutique penche, un peu.",
            "narrateur|Un grain colle au cuir, près du croissant pâle.",
            "copain|Un autre coup !",
            "enfant-f|Ma pêche va tomber.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle regarde la pêche, puis le trou.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 2): {
        "sons": "eau,sable",
        "emphasis": "seau",
        "passage": [
            "narrateur|Nino tire le seau vers le bac.",
            "copain|Je verse, pour la boutique !",
            "narrateur|L'eau part d'un seul coup.",
            "narrateur|La pêche se retrouve dans une flaque.",
            "enfant-f|Elle nage, maintenant !",
            "maman|Le seau a tout donné, trop vite.",
            "papa|Tes mains ont versé d'un trait.",
            "narrateur|Le sable devient boue, tout autour.",
            "copain|C'est un lac, Sarah !",
            "enfant-f|Je ne vois plus le trou.",
            "narrateur|Sarah s'immobilise, le sourire parti.",
            "narrateur|Le croissant pâle brille sous l'eau.",
            "maman|Vous versez comment, alors ?",
        ],
    },
    (1, 3): {
        "sons": "tissu,sable",
        "emphasis": "doudou",
        "passage": [
            "narrateur|Nino plante le doudou dans le sable.",
            "copain|C'est le marchand !",
            "narrateur|Il saute autour, les deux pieds.",
            "narrateur|Le doudou bascule sur la pêche.",
            "enfant-f|Il la cache, tout entier !",
            "papa|Tes pieds ont trop bougé, Nino.",
            "maman|Le marchand s'est couché.",
            "narrateur|Une oreille de tissu dépasse, seule.",
            "copain|Il s'est endormi !",
            "enfant-f|Ma pêche, je ne la vois plus.",
            "narrateur|Sarah écoute le bac, sans bouger.",
            "narrateur|Le croissant pâle a disparu sous le tissu.",
            "papa|Vous le remettez comment ?",
        ],
    },
    (2, 1): {
        "sons": "ballon,metal",
        "emphasis": "ballon",
        "passage": [
            "narrateur|Nino pose le ballon en haut.",
            "copain|Lui, il glisse le premier !",
            "narrateur|Le ballon dévale, toc toc toc.",
            "narrateur|La pêche reste dans la main de Sarah.",
            "enfant-f|Ce n'est pas la livraison !",
            "papa|Le ballon a pris la place.",
            "maman|Tes pieds l'ont poussé, Nino.",
            "narrateur|En bas, le ballon rebondit, puis s'arrête.",
            "copain|Une autre fois !",
            "enfant-f|Ma pêche n'a pas glissé.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle regarde le croissant pâle, dans sa paume.",
            "papa|Vous livrez comment, alors ?",
        ],
    },
    (2, 2): {
        "sons": "eau,metal",
        "emphasis": "seau",
        "passage": [
            "narrateur|Nino glisse la pêche dans le seau.",
            "copain|Elle voyage dans l'eau !",
            "narrateur|Il part trop vite sur le métal.",
            "narrateur|L'eau gicle, une ligne brillante.",
            "enfant-f|Le seau a tout perdu !",
            "maman|Tes pieds ont donné un coup.",
            "papa|La pêche tape le fond, toc.",
            "narrateur|Une goutte mouille le genou de Sarah.",
            "copain|On recommence, plus fort !",
            "enfant-f|Elle est toute mouillée.",
            "narrateur|Sarah sent l'inquiétude dans sa poitrine.",
            "narrateur|Le croissant pâle a disparu sous l'eau.",
            "maman|Vous descendez comment, alors ?",
        ],
    },
    (2, 3): {
        "sons": "tissu,metal",
        "emphasis": "doudou",
        "passage": [
            "narrateur|Nino pose le doudou tout en bas.",
            "copain|Toi tu es le client !",
            "narrateur|Il remonte en sautant les marches.",
            "narrateur|Le doudou glisse, puis tombe à côté.",
            "enfant-f|Le client n'est plus à sa place !",
            "papa|Tes pieds ont trop tapé, Nino.",
            "maman|Le doudou attend dans l'herbe.",
            "narrateur|Sarah tient la pêche, en haut.",
            "copain|Je le remets, et je saute !",
            "enfant-f|Il va retomber.",
            "narrateur|Nino ouvre la bouche, puis la referme.",
            "narrateur|Le croissant pâle chauffe dans sa main.",
            "papa|Vous le gardez comment, le client ?",
        ],
    },
    (3, 1): {
        "sons": "ballon,chaine",
        "emphasis": "ballon",
        "passage": [
            "narrateur|Nino lance le ballon vers le linge.",
            "copain|Je touche l'enseigne !",
            "narrateur|Le ballon tape le tissu, pan.",
            "narrateur|Le nœud se desserre, un peu.",
            "enfant-f|L'enseigne va tomber !",
            "maman|Tes pieds ont donné l'élan, Nino.",
            "papa|Le linge claque, trop fort.",
            "narrateur|Sarah rattrape un coin, tout juste.",
            "copain|Un autre pan !",
            "enfant-f|Elle ne tient plus.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle écoute la chaîne, puis le vent.",
            "papa|Vous jouez comment, avec le ballon ?",
        ],
    },
    (3, 2): {
        "sons": "eau,chaine",
        "emphasis": "seau",
        "passage": [
            "narrateur|Nino accroche le seau à la chaîne.",
            "copain|C'est le panier de la boutique !",
            "narrateur|Il pousse, et le seau s'envole.",
            "narrateur|L'eau dessine un arc, tout court.",
            "enfant-f|Le panier verse partout !",
            "papa|La chaîne va trop vite, Nino.",
            "maman|Tes pieds ont trop poussé.",
            "narrateur|Une goutte touche le linge à carreaux.",
            "copain|C'est de la pluie !",
            "enfant-f|L'enseigne est mouillée.",
            "narrateur|Sarah s'immobilise, le sourire parti.",
            "narrateur|Le croissant pâle brille, à l'abri.",
            "maman|Vous le tenez comment, le seau ?",
        ],
    },
    (3, 3): {
        "sons": "tissu,chaine",
        "emphasis": "doudou",
        "passage": [
            "narrateur|Nino noue le doudou à l'autre chaîne.",
            "copain|Deux enseignes, plus belles !",
            "narrateur|Il se balance, très fort.",
            "narrateur|Le doudou s'envole, une seconde.",
            "enfant-f|Il va partir !",
            "maman|Tes pieds font trop de vent, Nino.",
            "papa|Le nœud glisse, trop loin.",
            "narrateur|Sarah rattrape une oreille, tout près.",
            "copain|Plus haut, doudou !",
            "enfant-f|Il n'est pas une enseigne, comme ça.",
            "narrateur|Nino baisse les yeux, sans un mot.",
            "narrateur|Sarah cherche le croissant pâle, dans sa main.",
            "papa|Vous l'attachez comment, alors ?",
        ],
    },
}

T3_LABS = {
    1: ("on joue", "on attend", "papa le tient"),
    2: ("goutte à goutte", "on s'assoit", "maman tient"),
    3: ("l'enseigne", "sur le banc", "maman l'attache"),
}

T3_CHOICE = {
    1: [
        "narrateur|Le ballon n'a pas ouvert la boutique.",
        "papa|On joue, on attend, ou je le tiens ?",
    ],
    2: [
        "narrateur|Le seau a tout versé, trop vite.",
        "maman|Goutte à goutte, on s'assoit, ou je tiens ?",
    ],
    3: [
        "narrateur|Le doudou n'est pas à sa place.",
        "papa|L'enseigne, le banc, ou maman l'attache ?",
    ],
}

T3_SONS = {
    (1, 1): "ballon,rire",
    (1, 2): "silence,sable",
    (1, 3): "ballon,voix",
    (2, 1): "eau,goutte",
    (2, 2): "eau,silence",
    (2, 3): "seau,voix",
    (3, 1): "tissu,nœud",
    (3, 2): "banc,tissu",
    (3, 3): "tissu,voix",
}

PLAY = {
    1: "narrateur|Ils se passent le ballon, dans le bac.",
    2: "narrateur|Ils se passent le ballon, près du métal.",
    3: "narrateur|Ils se passent le ballon, sous la chaîne.",
}
WAIT = {
    1: "narrateur|Nino s'assoit dans le sable, un moment.",
    2: "narrateur|Nino s'assoit au pied du métal.",
    3: "narrateur|Nino s'assoit dans l'herbe, sous la chaîne.",
}
HOLD = {
    1: "narrateur|Papa tient le ballon, hors du bac.",
    2: "narrateur|Papa tient le ballon, près du métal.",
    3: "narrateur|Papa tient le ballon, loin de la chaîne.",
}
SLOW = {
    1: "narrateur|Ils versent goutte à goutte, dans le bac.",
    2: "narrateur|Ils versent goutte à goutte, sur le métal.",
    3: "narrateur|Ils versent goutte à goutte, sous la chaîne.",
}
SIT = {
    1: "narrateur|Ils s'assoient au bord du bac.",
    2: "narrateur|Ils s'assoient au pied du toboggan.",
    3: "narrateur|Ils s'assoient sous les balançoires.",
}
MUM = {
    1: "narrateur|Maman tient le seau, au bord du bac.",
    2: "narrateur|Maman tient le seau, au pied du métal.",
    3: "narrateur|Maman tient le seau, sous la chaîne.",
}
SIGN = {
    1: "narrateur|Ils plantent le doudou derrière la pêche.",
    2: "narrateur|Ils posent le doudou au bas du métal.",
    3: "narrateur|Ils nouent le doudou à côté du linge.",
}
BENCH = {
    1: "narrateur|Le doudou s'assoit au bord du bac.",
    2: "narrateur|Le doudou s'assoit au pied du toboggan.",
    3: "narrateur|Le doudou s'assoit sur le banc, près des chaînes.",
}
PIN = {
    1: "narrateur|Maman cale le doudou contre la caisse.",
    2: "narrateur|Maman cale le doudou au pied du métal.",
    3: "narrateur|Maman noue le doudou, un nœud court.",
}

PLACE = {
    1: "narrateur|Sarah pose la pêche, croissant pâle vers le soleil.",
    2: "narrateur|Sarah glisse la pêche, croissant pâle vers le ciel.",
    3: "narrateur|Sarah place la pêche, croissant pâle vers le linge.",
}

CLUE = {
    1: "narrateur|Le croissant pâle du début retrouve le soleil.",
    2: "narrateur|Le croissant pâle du début brille sur le métal.",
    3: "narrateur|Le croissant pâle du début regarde le linge.",
}


def t3_pass(a: int, b: int, c: int) -> list[str]:
    place = PLACE[a]
    clue = CLUE[a]
    if b == 1 and c == 1:
        return [
            "enfant-f|On joue avec, Nino.",
            "copain|À moi, puis à toi !",
            PLAY[a],
            "narrateur|Les pieds de Nino dansent, pile avec le jeu.",
            "narrateur|Nino rit, puis se tait.",
            place,
            "papa|Vous avez joué, et la boutique tient.",
            "maman|Le ballon a eu son tour.",
            clue,
            "enfant-f|Boutique ouverte !",
        ]
    if b == 1 and c == 2:
        return [
            "enfant-f|On attend un peu, Nino.",
            "narrateur|Nino ne dit rien.",
            WAIT[a],
            "narrateur|Le ballon repose, rond, sage.",
            "narrateur|Ses pieds se taisent, un moment.",
            place,
            "papa|Tes pieds ont su s'asseoir.",
            "maman|La boutique a eu la place.",
            clue,
            "enfant-f|Maintenant, c'est ouvert.",
        ]
    if b == 1 and c == 3:
        return [
            "enfant-f|Papa, tu le tiens ?",
            "papa|Je le tiens, Sarah.",
            HOLD[a],
            "narrateur|Les mains de Nino sont libres, maintenant.",
            "copain|Je t'aide, sans le ballon.",
            place,
            "maman|Vous avez demandé, et ça tient.",
            "narrateur|Nino hoche la tête, sans un mot.",
            clue,
            "enfant-f|La boutique est prête.",
        ]
    if b == 2 and c == 1:
        return [
            "enfant-f|Goutte à goutte, Nino, avec moi.",
            "copain|Goutte, puis goutte.",
            SLOW[a],
            "narrateur|Les mains de Nino suivent celles de Sarah.",
            "narrateur|La pêche a juste un peu d'eau, autour.",
            place,
            "papa|Vous avez versé ensemble.",
            "maman|Le seau a gardé le reste.",
            clue,
            "enfant-f|Boutique ouverte, tout propre.",
        ]
    if b == 2 and c == 2:
        return [
            "enfant-f|On s'assoit, Nino.",
            "copain|Mes pieds, restez là.",
            SIT[a],
            "narrateur|Le seau repose entre eux, sans bouger.",
            "narrateur|L'eau ne bouge plus, un miroir.",
            place,
            "maman|Vous avez laissé l'eau s'asseoir.",
            "papa|La pêche a séché un peu.",
            clue,
            "enfant-f|On ouvre, maintenant.",
        ]
    if b == 2 and c == 3:
        return [
            "enfant-f|Maman, tu le tiens ?",
            "maman|Je le tiens, bien stable.",
            MUM[a],
            "narrateur|Nino pose un doigt sur le bord, très léger.",
            "narrateur|Il ne verse plus tout seul.",
            place,
            "papa|Vous avez demandé, et ça tient.",
            "copain|Je ne verse plus tout seul.",
            clue,
            "enfant-f|La boutique est prête.",
        ]
    if b == 3 and c == 1:
        return [
            "enfant-f|Toi tu es l'enseigne, doudou.",
            "copain|Je le tiens, tu le places.",
            SIGN[a],
            "narrateur|Les pieds de Nino s'arrêtent, le temps du nœud.",
            "narrateur|Le doudou regarde la pêche, tout droit.",
            place,
            "papa|Vous l'avez mis à sa place.",
            "maman|L'enseigne tient, cette fois.",
            clue,
            "enfant-f|Boutique ouverte !",
        ]
    if b == 3 and c == 2:
        return [
            "enfant-f|Sur le banc, Nino, un moment.",
            "copain|Toi tu regardes, doudou.",
            BENCH[a],
            "narrateur|Nino souffle, et ses pieds se taisent.",
            "narrateur|Il ne dit rien, les yeux sur l'étal.",
            place,
            "maman|Le doudou a sa place, à côté.",
            "papa|Vous avez laissé la boutique libre.",
            clue,
            "enfant-f|C'est ouvert.",
        ]
    pin_extra = {
        1: "narrateur|Un grain colle à la pêche, minuscule.",
        2: "narrateur|Un toc répond, dans le métal.",
        3: "narrateur|Un coin de linge frôle la pêche.",
    }[a]
    return [
        "enfant-f|Maman, tu l'attaches ?",
        "maman|Je l'attache, bien ferme.",
        PIN[a],
        "narrateur|Nino tient le bout, sans sauter.",
        "copain|Il ne part plus.",
        place,
        "papa|Vous avez demandé, et ça tient.",
        pin_extra,
        clue,
        "enfant-f|La boutique est prête.",
    ]


END_CODA = {
    1: "Le ballon repose, rond, à côté.",
    2: "Le seau sonne creux, après.",
    3: "Le doudou a une tache ronde, au ventre.",
}

LAST = {
    (1, 1, 1): "Un trou rond reste au milieu du bac.",
    (1, 1, 2): "Un grain de sable brille sur le croissant pâle.",
    (1, 1, 3): "Le cuir du ballon garde un grain, collé.",
    (1, 2, 1): "Une auréole d'eau sèche autour du trou.",
    (1, 2, 2): "Le seau garde une auréole, au fond.",
    (1, 2, 3): "Le bord du seau vise le ciel, vide.",
    (1, 3, 1): "Une oreille de tissu reste chaude, au bord.",
    (1, 3, 2): "Le banc du bac garde une ombre ronde.",
    (1, 3, 3): "Le sac reprend le doudou, un peu sablé.",
    (2, 1, 1): "Vide et chaud, le toboggan se tait.",
    (2, 1, 2): "Un petit toc dort dans le métal.",
    (2, 1, 3): "Le ballon reprend un petit bond, plus tard.",
    (2, 2, 1): "Une goutte sèche sur le genou de Sarah.",
    (2, 2, 2): "L'eau du seau ne bouge plus, un miroir.",
    (2, 2, 3): "Le seau repose, le bord vers le ciel.",
    (2, 3, 1): "Le doudou garde le bas du métal, sage.",
    (2, 3, 2): "Une oreille de tissu touche l'herbe.",
    (2, 3, 3): "Le nœud court reste au pied du métal.",
    (3, 1, 1): "Plus aucun cri sur la chaîne.",
    (3, 1, 2): "Un brin d'herbe reste au mollet de Sarah.",
    (3, 1, 3): "Le linge à carreaux pend, sans claquer.",
    (3, 2, 1): "Une goutte a marqué le tissu, pâle.",
    (3, 2, 2): "La chaîne se tait, sous le seau vide.",
    (3, 2, 3): "Le seau repose loin de la chaîne.",
    (3, 3, 1): "Deux tissus se touchent, sans voler.",
    (3, 3, 2): "Le banc garde une oreille de doudou, tiède.",
    (3, 3, 3): "Le nœud court tient, contre la chaîne.",
}

END_LEAD = {
    (1, 1): [
        "narrateur|Ils croquent la pêche, tiède.",
        "copain|On a joué, et elle est à nous !",
        "enfant-f|La boutique a tenu, Nino.",
        "papa|Tes pieds ont dansé dans le jeu.",
        "maman|Une bouchée pour chacun.",
    ],
    (1, 2): [
        "narrateur|Sarah tend un quartier à Nino.",
        "copain|J'ai attendu, et elle est sucrée.",
        "enfant-f|Tes pieds se sont tus, un moment.",
        "maman|Le sucré valait l'attente.",
        "papa|Le jus, sur le pouce ?",
    ],
    (1, 3): [
        "narrateur|Papa rend le ballon, après la bouchée.",
        "enfant-f|Tu l'as tenu, on a ouvert.",
        "copain|Maintenant je peux le reprendre.",
        "papa|Quand la boutique a fini, oui.",
        "maman|Essuie ton menton, Sarah.",
    ],
    (2, 1): [
        "narrateur|Ils goûtent au bord, les mains fraîches.",
        "enfant-f|On a versé goutte à goutte.",
        "copain|Mes mains ont suivi les tiennes.",
        "papa|Le seau a gardé le reste.",
        "maman|La pêche a juste un peu d'eau.",
    ],
    (2, 2): [
        "narrateur|Ils croquent assis, sans se presser.",
        "copain|On s'est assis, et l'eau s'est tue.",
        "enfant-f|Puis la boutique a ouvert.",
        "maman|Vos pieds ont su rester là.",
        "papa|Le sucré, ça valait l'assise.",
    ],
    (2, 3): [
        "narrateur|Maman pose le seau, après la part.",
        "enfant-f|Tu l'as tenu, on a ouvert.",
        "copain|Je n'ai plus tout versé.",
        "papa|Vous avez demandé, pile à temps.",
        "maman|Tes pieds pendent, sages.",
    ],
    (3, 1): [
        "narrateur|Le doudou garde la boutique, un moment.",
        "copain|Il était l'enseigne, tout droit.",
        "enfant-f|On l'a mis ensemble.",
        "papa|Tes pieds ont attendu le nœud.",
        "maman|La pêche a vu son marchand.",
    ],
    (3, 2): [
        "narrateur|Ils s'allongent un peu, près du banc.",
        "copain|Le doudou a regardé, sage.",
        "enfant-f|La boutique avait de la place.",
        "maman|Vos pieds se sont tus, un moment.",
        "papa|Une bouchée, puis une autre.",
    ],
    (3, 3): [
        "narrateur|Maman détache le doudou, plus tard.",
        "enfant-f|Tu l'avais attaché, pile.",
        "copain|Il n'est pas parti.",
        "papa|Vous avez demandé, et ça a tenu.",
        "maman|La pêche sent le soleil.",
    ],
}

END_MID = {
    1: "narrateur|Un filet sucré reste au coin.",
    2: "narrateur|Sarah retrouve le croissant pâle, sucré.",
    3: "narrateur|Trois bouches, un même sucré.",
}


def ending(a: int, b: int, c: int) -> list[str]:
    rows = list(END_LEAD[(b, c)])
    rows.append(END_MID[a])
    rows.append(f"narrateur|{END_CODA[b]}")
    rows.append("narrateur|Dans la bouchée, la pêche au croissant pâle est là.")
    rows.append(f"narrateur|{LAST[(a, b, c)]}")
    return rows


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "marche,caisses,abeille",
        {"emphasis": "croissant pâle"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le bac à sable", "le toboggan", "les balançoires"), "pause_before": 200},
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
            {"emphasis": "pêche"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("le ballon", "le seau", "le doudou"), "pause_before": 200},
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
                    {"emphasis": "croissant pâle"},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ending(a, b, c), "ending", "pêche,marche",
                    {"emphasis": "pêche"},
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
        "celui où j'ai compris",
        "il faut attendre",
        "beaucoup d'énergie",
        "hyperactif",
        "camarade qui bouge",
        "ce n'est pas une faute",
        "mission accomplie",
        "j'ai compris",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(whole):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "enfant-f|" not in blob:
        raise SystemExit(f"{SID}: enfant-f absent")
    if "copain|" not in blob:
        raise SystemExit(f"{SID}: copain absent")
    if "croissant pâle" not in blob:
        raise SystemExit(f"{SID}: indice croissant pâle absent")

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
    if not all(c.get("text_xai_tags") != c["text"] for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK {SID} {sum(words(c['text']) for c in story['chunks'])} mots")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-019 — La petite boutique de Sarah et Nino\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.ENE.001 — l'énergie n'est pas une faute ; "
        "jouer, attendre, demander (vécue, jamais dite)\n"
        "- **Personnages :** Sarah, Nino, papa, maman\n"
        "- **Lieu :** marché du village sous la toile rayée, puis l'aire derrière les toiles "
        "(bac, toboggan, balançoires)\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Sarah connaît le marché. Un détail paraît nouveau : une pêche tiède au croissant pâle. "
        "Elle veut ouvrir une petite boutique avec Nino avant que les caisses se taisent. "
        "Sarah plante ; Nino veut courir. Première idée trop vite : le trou, la glissade, "
        "le nœud. Ça rate. Ballon, seau ou doudou : l'aide trop vite penche l'étal. "
        "On joue, on attend, ou on tend à papa ou maman. Le croissant pâle retrouve le soleil. "
        "Ils croquent.\n\n"
        "## Vécu\n\n"
        "Sarah veut la boutique **maintenant**. Nino propose, tap tap. Silence = réponse. "
        "Première idée : planter trop vite. Ça rate. Chaque choix change l'obstacle "
        "(trou volé, livraison volée, enseigne mouillée). La leçon se voit : taper fait "
        "pencher ; jouer, attendre ou demander tient l'étal. Fin : jus au menton + croissant "
        "pâle du début + image unique du chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Tom / Léa / Sami / « on va apprendre » / « camarade qui bouge » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés. "
        "T3 seau : « goutte à goutte », plus « tout doux ».\n"
        "- Héros Sarah (`enfant-f`), Nino (`copain`), rythmes distincts, silence = réponse.\n"
        "- Indice unique dès l'ouverture (croissant pâle), payé au climax et à la bouchée.\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'action. 9 T2, 27 T3, 27 fins.\n"
        "- Merci vécu (tenir la pêche). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N2 ≤ 15. `check()` OK. Pas apply.\n\n"
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
