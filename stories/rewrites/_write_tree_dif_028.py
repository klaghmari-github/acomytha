#!/usr/bin/env python3
"""TREE-DIF-028 — Le gâteau aux fraises de Chouchou. DIF.PAR.002, N2, TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-028"
N2 = LIMITS["N2"]
TITLE = "Le gâteau aux fraises de Chouchou"
FIL = (
    "Au fournil du dimanche, Chouchou veut le gâteau aux fraises prêt pour le goûter. "
    "Un grain de vanille, noir, brille dans la rainure du saladier. "
    "Elle tire le sucre trop vite. T1 = saladier / cuillère / tablier ; les trois partent. "
    "T2 = placard (sacs jumeaux) / tiroir (recette cachée) / garde-manger (rouge mêlé). "
    "T3 change le geste. Elle refuse de foncer. Le grain du début revient. "
    "Le goûter a failli rester un nuage de sucre."
)
CHARS = "Chouchou, papa, maman"
SETTING = "cuisine, dimanche, goûter aux fraises — le fournil du dimanche"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent", "tout blanc")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain de vanille",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_goûter_attend_et_la_farine_manque; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "grain de vanille",
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=elle_coupe_la_phrase_puis_se_retient; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_inquiétude; intensite=2; destinataire=enfant; sous_texte=la_phrase_de_maman_n_est_pas_finie; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "grain",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=elle_observe_et_laisse_finir; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain de vanille",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_paie_le_début; tempo=posé; sourire=léger; respiration=ample",
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
        found = TIC_WORDS.search(low)
        if found:
            raise SystemExit(f"tic {found.group(0)!r}: {ph}")
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
    "narrateur|Le dimanche, la cuisine de Chouchou sent les fraises.",
    "narrateur|Elle connaît chaque tiroir, chaque bruit du four.",
    "narrateur|C'est le fournil du dimanche, près du four.",
    "narrateur|Ce dimanche, un détail paraît nouveau.",
    "narrateur|Un grain de vanille, noir, brille dans la rainure du saladier.",
    "enfant-f|Il est collé, là.",
    "papa|Le beurre ramollit, près de la fenêtre.",
    "narrateur|Une odeur chaude glisse sous la fenêtre.",
    "maman|Les fraises du marché gouttent dans l'évier.",
    "narrateur|En ce moment, Chouchou veut le gâteau pour le goûter.",
    "enfant-f|On le fait, maman ?",
    "maman|Oui, le gâteau aux fraises.",
    "enfant-f|Où est la farine ?",
    "narrateur|Maman ouvre la bouche, puis s'arrête.",
    "narrateur|Le sourire de Chouchou disparaît.",
    "enfant-f|La farine !",
    "narrateur|Elle tire un sac blanc, trop vite.",
    "narrateur|Un nuage sucré tombe dans le bois.",
    "papa|C'est le sucre, pas la farine.",
    "narrateur|Le bois du saladier devient collant, sucré.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "maman|Prends tes affaires.",
    "maman|On cherche ensemble.",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près de l'évier.",
    "narrateur|Le saladier, la cuillère, et le tablier.",
    "narrateur|Rien ne reste sur la table.",
    "papa|Tu prends quoi, d'abord ?",
]

T1 = {
    1: {
        "passage": [
            "narrateur|Chouchou prend le saladier de bois à deux mains.",
            "enfant-f|Le grain noir est là, dans la rainure.",
            "papa|Il pèse, ce bois.",
            "narrateur|Un peu de sucre colle au fond, du nuage.",
            "narrateur|La cuillère glisse contre le bord.",
            "maman|Le tablier, aussi.",
            "narrateur|Papa noue le tissu dans son dos.",
            "enfant-f|La farine est dans le.",
            "narrateur|Elle s'arrête, les épaules hautes.",
            "maman|On va la chercher.",
            "papa|Tes trois affaires viennent.",
            "enfant-f|Je tiens le saladier.",
            "narrateur|Le fournil du dimanche attend, près du four.",
        ],
        "question": [
            "narrateur|Le saladier de bois tient contre son ventre.",
            "maman|Chouchou a pris quoi, d'abord ?",
        ],
        "confirm": [
            "enfant-f|Le saladier.",
            "papa|Oui.",
            "narrateur|La cuillère et le tablier voyagent avec.",
            "papa|Merci, le sucre reste dans son sac.",
            "enfant-f|J'ai failli parler trop vite.",
            "maman|Le grain noir voyage aussi.",
            "narrateur|Le bois reste sucré, un peu collant.",
            "papa|On cherche où, maintenant ?",
        ],
        "emphasis": "saladier",
        "sons": "bois,tissu",
        "qfields": {
            "expected_answer": "le saladier",
            "accepted_examples": "saladier | le saladier | un saladier | le bol | bol | le bois",
            "retry_prompt": "Chouchou a pris le saladier en premier. Elle a pris quoi ?",
        },
    },
    2: {
        "passage": [
            "narrateur|Chouchou saisit la cuillère de bois, d'abord.",
            "enfant-f|Pour tourner la pâte.",
            "maman|Elle tape trop tôt, parfois.",
            "narrateur|Le manche est rêche, un peu chaud.",
            "narrateur|Un peu de sucre colle au creux.",
            "papa|Le saladier, ensuite, et le tablier.",
            "narrateur|Maman les pose contre elle, l'un après l'autre.",
            "enfant-f|Alors dis-moi où.",
            "narrateur|Maman inspire, les lèvres rondes.",
            "narrateur|Chouchou referme sa bouche, d'un coup.",
            "papa|Elle cherche la suite.",
            "enfant-f|J'attends, maman.",
            "narrateur|Le fournil du dimanche attend, près du four.",
        ],
        "question": [
            "narrateur|La cuillère de bois brille un peu, contre sa paume.",
            "papa|Chouchou a pris quoi ?",
        ],
        "confirm": [
            "enfant-f|La cuillère.",
            "maman|Oui.",
            "narrateur|Le saladier pèse contre son bras.",
            "narrateur|Le tablier dort sur ses épaules.",
            "maman|Merci, j'ai repris mon souffle.",
            "enfant-f|Le grain noir est dans le bois.",
            "narrateur|Le manche reste sucré, un peu collant.",
            "papa|On avance où, alors ?",
        ],
        "emphasis": "cuillère",
        "sons": "bois,tissu",
        "qfields": {
            "expected_answer": "la cuillère",
            "accepted_examples": "cuillère | la cuillère | une cuillère | la cuiller | cuiller | le bois",
            "retry_prompt": "La cuillère de bois brillait. Chouchou a pris quoi ?",
        },
    },
    3: {
        "passage": [
            "narrateur|Chouchou enfile d'abord le tablier, trop large.",
            "enfant-f|Pour ne pas tacher.",
            "papa|Le nœud, dans le dos.",
            "narrateur|Le tissu est rêche, un peu chaud.",
            "narrateur|Un peu de sucre colle au tablier, pâle.",
            "maman|Le saladier, ensuite, et la cuillère.",
            "narrateur|Papa les pose dans ses mains, sans bruit.",
            "enfant-f|Maintenant, tu dis où.",
            "narrateur|Maman ouvre la bouche, puis s'arrête.",
            "papa|On avance, elle va finir.",
            "enfant-f|D'accord, maman.",
            "narrateur|Le grain noir voyage dans le bois, contre elle.",
            "narrateur|Le fournil du dimanche attend, près du four.",
        ],
        "question": [
            "narrateur|Le tablier fait un pli, contre son ventre.",
            "maman|Chouchou a enfilé quoi, d'abord ?",
        ],
        "confirm": [
            "enfant-f|Le tablier.",
            "papa|Oui.",
            "narrateur|Le saladier et la cuillère pèsent contre elle.",
            "papa|Merci, le nœud du tablier tient.",
            "enfant-f|J'écoute, maman.",
            "maman|Le grain noir reste dans la rainure.",
            "narrateur|Le tissu reste sucré, un peu collant.",
            "papa|On cherche où, alors ?",
        ],
        "emphasis": "tablier",
        "sons": "tissu,bois",
        "qfields": {
            "expected_answer": "le tablier",
            "accepted_examples": "tablier | le tablier | un tablier | le tissu",
            "retry_prompt": "Le tablier faisait un pli. Elle a enfilé quoi ?",
        },
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le saladier tape un peu sa hanche, à chaque pas.",
        "narrateur|La farine manque, et le goûter attend.",
        "narrateur|Le placard, le tiroir, et le garde-manger attendent.",
        "papa|On cherche où, d'abord ?",
    ],
    2: [
        "narrateur|La cuillère claque une fois, contre le bois.",
        "narrateur|La farine manque, et le goûter attend.",
        "narrateur|Le placard, le tiroir, et le garde-manger attendent.",
        "papa|On cherche où, d'abord ?",
    ],
    3: [
        "narrateur|Le tablier fait un pli, à chaque pas.",
        "narrateur|La farine manque, et le goûter attend.",
        "narrateur|Le placard, le tiroir, et le garde-manger attendent.",
        "papa|On cherche où, d'abord ?",
    ],
}

T2 = {
    (1, 1): {
        "passage": [
            "narrateur|Le saladier pose un rond d'ombre au sol.",
            "narrateur|Devant le placard haut, les sacs blancs se ressemblent.",
            "enfant-f|C'est trop haut.",
            "narrateur|Elle tend le bras, et rien.",
            "maman|La farine est sur.",
            "enfant-f|Du milieu !",
            "narrateur|Chouchou referme la bouche, vite.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois les sacs, toi ?",
            "narrateur|Envie et inquiétude se bousculent dans sa poitrine.",
            "narrateur|Elle baisse les yeux vers le grain, un instant.",
            "narrateur|Le saladier garde son rond d'ombre.",
            "papa|Vous faites comment, toutes les deux ?",
        ],
        "sons": "placard,bois",
        "emphasis": "placard",
    },
    (1, 2): {
        "passage": [
            "narrateur|Le saladier bute contre la poignée, puis lâche.",
            "narrateur|Devant le tiroir, le bois sent le citron.",
            "enfant-f|Il y a trop de choses.",
            "narrateur|Elle tire trop fort, et les cuillères s'emmêlent.",
            "maman|La recette est sous les.",
            "enfant-f|Les fourchettes !",
            "narrateur|Chouchou recule d'un doigt.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu as vu le papier, toi ?",
            "maman|Je n'ai pas fini.",
            "narrateur|Elle pose le saladier, pour mieux voir.",
            "narrateur|Le grain noir reste dans la rainure.",
            "papa|Vous trouvez comment ?",
        ],
        "sons": "tiroir,bois",
        "emphasis": "tiroir",
    },
    (1, 3): {
        "passage": [
            "narrateur|Le saladier penche contre le seuil, lourd.",
            "narrateur|Dans le garde-manger, l'air est frais, un peu sombre.",
            "enfant-f|Les fraises, elles sont où ?",
            "narrateur|Elle pointe le bol rouge, trop vite.",
            "maman|Les belles sont dans le.",
            "enfant-f|Le bol !",
            "narrateur|Chouchou rentre le doigt.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|L'ombre mélange les formes, tu vois ?",
            "maman|Ma phrase n'est pas finie.",
            "narrateur|Le saladier penche, puis se tient.",
            "narrateur|Chouchou écoute l'ombre, sans foncer.",
            "papa|Vous faites quoi, alors ?",
        ],
        "sons": "placard,fraises",
        "emphasis": "garde-manger",
    },
    (2, 1): {
        "passage": [
            "narrateur|La cuillère s'arrête contre sa paume.",
            "narrateur|Devant le placard, les sacs blancs se ressemblent.",
            "enfant-f|C'est trop haut.",
            "narrateur|La cuillère pointe une boîte, trop tôt.",
            "maman|La farine est sur.",
            "enfant-f|Celle-là !",
            "narrateur|Chouchou baisse la cuillère, d'un coup.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois le grain noir, toi ?",
            "narrateur|Ses épaules restent hautes, puis retombent.",
            "narrateur|La cuillère descend, sans pointer.",
            "narrateur|Elle cherche le grain noir, des yeux.",
            "papa|Vous faites comment, toutes les deux ?",
        ],
        "sons": "placard,bois",
        "emphasis": "placard",
    },
    (2, 2): {
        "passage": [
            "narrateur|La cuillère glisse dans le tiroir, trop vite.",
            "narrateur|Devant le tiroir, le bois sent le citron.",
            "enfant-f|Il y a trop de choses.",
            "narrateur|Un cliquetis court, puis s'arrête.",
            "maman|La recette est sous les.",
            "enfant-f|Sous les fourchettes !",
            "narrateur|Chouchou retire la cuillère, sans un mot.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu as vu le papier, toi ?",
            "maman|Je n'ai pas fini.",
            "narrateur|La cuillère repose sur le bois, sage.",
            "narrateur|Chouchou écoute le tiroir, sans fouiller.",
            "papa|Vous trouvez comment ?",
        ],
        "sons": "tiroir,bois",
        "emphasis": "tiroir",
    },
    (2, 3): {
        "passage": [
            "narrateur|La cuillère cogne un bocal, un petit toc.",
            "narrateur|Dans le garde-manger, l'air est frais, un peu sombre.",
            "enfant-f|Les fraises, elles sont où ?",
            "narrateur|La cuillère désigne le bol rouge, trop tôt.",
            "maman|Les belles sont dans le.",
            "enfant-f|Le bol !",
            "narrateur|Chouchou serre le manche, puis se tait.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|L'ombre mélange les formes, tu vois ?",
            "maman|Ma phrase n'est pas finie.",
            "narrateur|La cuillère se tait contre sa jambe.",
            "narrateur|Chouchou écoute l'ombre, sans foncer.",
            "papa|Vous faites quoi, alors ?",
        ],
        "sons": "placard,fraises",
        "emphasis": "garde-manger",
    },
    (3, 1): {
        "passage": [
            "narrateur|Le tablier reste sage, contre son ventre.",
            "narrateur|Devant le placard haut, les sacs blancs se ressemblent.",
            "enfant-f|C'est trop haut.",
            "narrateur|Chouchou serre le tablier, sans bouger.",
            "maman|La farine est sur.",
            "enfant-f|En haut !",
            "narrateur|Elle referme la bouche, et le tissu tremble.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu vois les sacs, toi ?",
            "narrateur|Envie et inquiétude se bousculent sous le nœud.",
            "narrateur|Le tablier tremble, puis s'arrête.",
            "narrateur|Elle cherche le grain noir, des yeux.",
            "papa|Vous faites comment, toutes les deux ?",
        ],
        "sons": "placard,tissu",
        "emphasis": "placard",
    },
    (3, 2): {
        "passage": [
            "narrateur|Un coin du tablier frôle le bois.",
            "narrateur|Devant le tiroir, le bois sent le citron.",
            "enfant-f|Il y a trop de choses.",
            "narrateur|Elle tire le linge du tiroir, trop vite.",
            "maman|La recette est sous les.",
            "enfant-f|Sous le linge !",
            "narrateur|Chouchou lâche le tissu, d'un coup.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|Tu as vu le papier, toi ?",
            "maman|Je n'ai pas fini.",
            "narrateur|Le tablier se range contre son ventre.",
            "narrateur|Chouchou écoute le tiroir, sans fouiller.",
            "papa|Vous trouvez comment ?",
        ],
        "sons": "tiroir,tissu",
        "emphasis": "tiroir",
    },
    (3, 3): {
        "passage": [
            "narrateur|Le tablier accroche une anse, puis lâche.",
            "narrateur|Dans le garde-manger, l'air est frais, un peu sombre.",
            "enfant-f|Les fraises, elles sont où ?",
            "narrateur|Elle avance vers le bol rouge, trop vite.",
            "maman|Les belles sont dans le.",
            "enfant-f|Le bol !",
            "narrateur|Chouchou recule, et le tablier se tait.",
            "narrateur|Papa s'accroupit à la même hauteur.",
            "papa|L'ombre mélange les formes, tu vois ?",
            "maman|Ma phrase n'est pas finie.",
            "narrateur|Le tablier se tait, large et chaud.",
            "narrateur|Chouchou écoute l'ombre, sans foncer.",
            "papa|Vous faites quoi, alors ?",
        ],
        "sons": "placard,fraises",
        "emphasis": "garde-manger",
    },
}

T3_LABS = {
    1: ("attendre", "le tabouret", "papa porte"),
    2: ("s'asseoir", "la lampe", "le linge"),
    3: ("compter", "le panier", "le bol"),
}

T3_CHOICE = {
    1: [
        "narrateur|Devant le placard, maman n'a pas fini.",
        "narrateur|Les sacs blancs se ressemblent, trop haut.",
        "papa|Attendre, le tabouret, ou je te porte ?",
    ],
    2: [
        "narrateur|Devant le tiroir, la suite manque.",
        "narrateur|Le bois sent le citron, et le papier se cache.",
        "maman|S'asseoir, la lampe, ou le linge ?",
    ],
    3: [
        "narrateur|Dans le garde-manger, l'ombre tient les fraises.",
        "narrateur|Le rouge se mélange, bol et panier.",
        "papa|Compter, le panier, ou le bol ?",
    ],
}

T3_EMPH = {
    1: {1: "grain", 2: "tabouret", 3: "grain"},
    2: {1: "papier", 2: "lampe", 3: "linge"},
    3: {1: "panier", 2: "panier", 3: "bol rouge"},
}

T3_SONS = {
    (1, 1): "silence,placard",
    (1, 2): "bois,placard",
    (1, 3): "pas,placard",
    (2, 1): "silence,tiroir",
    (2, 2): "lampe,tiroir",
    (2, 3): "tissu,tiroir",
    (3, 1): "bocaux,silence",
    (3, 2): "panier,fraises",
    (3, 3): "bol,fraises",
}


def t3(a: int, b: int, c: int) -> list[str]:
    obj = {1: "Le saladier reste au sol, sage.", 2: "La cuillère attend un dernier tour.", 3: "Le tablier dort contre son ventre."}[a]
    if b == 1 and c == 1:
        return [
            "enfant-f|On attend.",
            "maman|Oui.",
            "narrateur|Elles restent debout, l'une contre l'autre.",
            "narrateur|Une mouche tapote la vitre, puis plus rien.",
            "maman|Celle du milieu.",
            "enfant-f|L'étagère du milieu.",
            "narrateur|Sur le sac du milieu, un grain noir brille.",
            "enfant-f|Comme dans la rainure.",
            "narrateur|Chouchou ne tend pas le bras.",
            "narrateur|Le mot se pose, entier, sur le sac.",
            f"narrateur|{obj}",
            "papa|Le sac du milieu est le bon.",
        ]
    if b == 1 and c == 2:
        return [
            "papa|Je pose le petit tabouret.",
            "narrateur|Le bois craque, un tout petit cri.",
            "maman|Derrière le.",
            "narrateur|Chouchou monte, et ne dit rien.",
            "maman|Derrière le sucre.",
            "enfant-f|Je vois le sac, maintenant.",
            "narrateur|Un grain de vanille colle au papier du sac.",
            "enfant-f|Le même grain.",
            "narrateur|Chouchou reste sur le bois, sans sauter.",
            "narrateur|Le sucre reste derrière, et le sac aussi.",
            f"narrateur|{obj}",
            "maman|Le tabouret a aidé mes mots.",
        ]
    if b == 1 and c == 3:
        return [
            "enfant-f|Tu me portes, papa ?",
            "papa|Oui, contre moi.",
            "narrateur|Sa joue touche la chemise, chaude.",
            "maman|À côté du.",
            "narrateur|Chouchou garde sa bouche fermée.",
            "maman|À côté du sel.",
            "enfant-f|Celle-là, tout près du sel.",
            "narrateur|Un point noir brille sur le sac, comme au début.",
            "narrateur|Contre la chemise, Chouchou ne parle pas.",
            "narrateur|Elle a laissé le sel, et le mot.",
            f"narrateur|{obj}",
            "papa|Le sac près du sel est le bon.",
        ]
    if b == 2 and c == 1:
        return [
            "enfant-f|On s'assoit, d'abord.",
            "narrateur|Le carrelage est froid, un peu lisse.",
            "maman|Les serviettes.",
            "narrateur|Chouchou ne finit pas la phrase.",
            "maman|Sous les serviettes.",
            "enfant-f|Sous les serviettes.",
            "narrateur|Elles soulèvent le papier, ensemble.",
            "narrateur|Un grain de vanille colle au coin jaune.",
            "narrateur|Le carrelage refroidit leurs genoux.",
            "narrateur|Le papier jaune reste plié, puis s'ouvre.",
            f"narrateur|{obj}",
            "papa|Le papier jaune est là, entier.",
        ]
    if b == 2 and c == 2:
        return [
            "papa|J'allume la petite lampe.",
            "narrateur|Un rond jaune court dans le tiroir.",
            "maman|Sous les.",
            "narrateur|Le crayon gratte, puis s'arrête.",
            "maman|Sous les cuillères.",
            "enfant-f|Comme le rond jaune.",
            "narrateur|Le grain noir apparaît sur le papier, net.",
            "enfant-f|C'est le même.",
            "narrateur|La lampe ne brûle pas les mots.",
            "narrateur|Chouchou a regardé, sans fouiller.",
            f"narrateur|{obj}",
            "papa|La lumière a tenu le mot.",
        ]
    if b == 2 and c == 3:
        return [
            "enfant-f|On lève le linge.",
            "narrateur|Le tissu sent le savon, pâle.",
            "maman|En dessous.",
            "narrateur|Chouchou tourne la tête, sans parler.",
            "maman|En dessous, le papier jaune.",
            "enfant-f|Je vois le coin, maintenant.",
            "narrateur|Un grain de vanille dort sur le jaune.",
            "enfant-f|Comme dans le saladier.",
            "narrateur|Le linge retombe, lent, sans bruit.",
            "narrateur|Le jaune est resté entier, sous le linge.",
            f"narrateur|{obj}",
            "maman|Le linge a gardé le secret.",
        ]
    if b == 3 and c == 1:
        return [
            "enfant-f|On compte les bocaux.",
            "maman|Moi aussi.",
            "narrateur|Un, deux, trois, jusqu'à sept.",
            "maman|Le panier.",
            "enfant-f|Dans le panier.",
            "narrateur|Sur l'anse, un grain noir brille, petit.",
            "enfant-f|Le grain du début.",
            "narrateur|Le compte a donné du temps au mot.",
            "narrateur|Chouchou n'a pas choisi trop tôt.",
            f"narrateur|{obj}",
            "papa|Les bocaux se sont tus, le mot aussi.",
            "maman|Les fraises sont là, enfin.",
        ]
    if b == 3 and c == 2:
        return [
            "enfant-f|On se baisse, d'abord.",
            "narrateur|L'air du bas est plus frais, et sombre.",
            "maman|Le panier bas.",
            "narrateur|Chouchou ouvre la bouche, puis la referme.",
            "enfant-f|Pas le bol.",
            "narrateur|Elles se relèvent, ensemble.",
            "narrateur|Un grain de vanille tient à l'anse du panier.",
            "enfant-f|Je l'avais vu dans le bois.",
            "narrateur|L'air frais a ralenti leurs mains.",
            "narrateur|Chouchou n'a pas pris le bol.",
            f"narrateur|{obj}",
            "papa|Se baisser a ralenti les mots.",
        ]
    return [
        "narrateur|Le bol rouge brille, plus proche que le panier.",
        "enfant-f|Le bol ?",
        "narrateur|Chouchou referme sa bouche, tout de suite.",
        "maman|Le bol rouge.",
        "enfant-f|Dans le bol rouge, d'accord.",
        "narrateur|Au fond, un grain de vanille brille, seul.",
        "enfant-f|Le même qu'au saladier.",
        "narrateur|Le vrai rouge était plus proche.",
        "narrateur|Chouchou a failli dire le panier.",
        f"narrateur|{obj}",
        "maman|Le bol rouge était le bon.",
        "papa|Le panier peut attendre.",
    ]


ENDINGS = {
    (1, 1, 1): [
        "narrateur|Le sac s'ouvre au-dessus du bois.",
        "narrateur|La farine tombe, lente, sans nuage sucré.",
        "enfant-f|Le gâteau peut commencer.",
        "maman|Les fraises, après la pâte.",
        "papa|Le four chauffe, tout près.",
        "narrateur|Dans la rainure, le grain de vanille tient.",
        "narrateur|Chouchou le laisse collé, pour le souvenir.",
        "narrateur|Le goûter a failli rester du sucre.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le saladier sent le beurre, à présent.",
    ],
    (1, 1, 2): [
        "narrateur|Derrière le sucre, le sac attendait.",
        "enfant-f|Le tabouret l'a montrée.",
        "maman|Et le mot, après.",
        "papa|La farine entre dans le bois, sans nuage.",
        "narrateur|Ils mélangent près de l'évier.",
        "narrateur|Le grain de vanille reste dans la rainure.",
        "enfant-f|Il a voyagé jusqu'ici.",
        "narrateur|Le goûter a failli manquer le four.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le tabouret garde une poussière de farine, blanche.",
    ],
    (1, 1, 3): [
        "narrateur|À côté du sel, le sac se penche.",
        "enfant-f|Il était trop près, tout en haut.",
        "maman|Le sel a gardé sa place.",
        "papa|Une fraise laisse un jus rouge sur son doigt.",
        "narrateur|Le saladier reçoit la farine, enfin.",
        "narrateur|Le grain noir brille, collé comme au début.",
        "enfant-f|On l'a, maman.",
        "narrateur|Le goûter a failli rester en l'air.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Sur l'épaule de papa, le bois sent le beurre.",
    ],
    (1, 2, 1): [
        "narrateur|Sous les serviettes, le papier est jaune.",
        "enfant-f|Comme tu avais dit, à la fin.",
        "maman|Oui.",
        "papa|On suit la recette, près du four.",
        "narrateur|Le beurre fond dans le saladier.",
        "narrateur|Le grain de vanille tient, au bord.",
        "enfant-f|Il n'est pas parti.",
        "narrateur|Le goûter a failli rester plié.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le carrelage garde un rond de bois, tiède.",
    ],
    (1, 2, 2): [
        "narrateur|Le rond jaune colle aux cuillères, un moment.",
        "maman|Le papier était le bon.",
        "enfant-f|On a lu ensemble.",
        "papa|Une fraise casse, nette, entre les dents.",
        "narrateur|La farine rejoint le beurre, dans le bois.",
        "narrateur|Le grain noir reste, luisant, dans la rainure.",
        "enfant-f|Je le vois, maman.",
        "narrateur|Le goûter a failli rester dans l'ombre.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le rond de la lampe s'éteint sur la pâte.",
    ],
    (1, 2, 3): [
        "narrateur|Sous le linge, le papier attend.",
        "enfant-f|Tu as dit en dessous, à la fin.",
        "maman|Oui, à la fin.",
        "narrateur|Ils cassent un œuf, petit, dans le bois.",
        "papa|Le four ronronne, bas.",
        "narrateur|Le grain de vanille tient contre l'œuf.",
        "enfant-f|Il a failli partir avec le linge.",
        "narrateur|Le goûter a failli rester sous le tissu.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le linge reprend sa place, une pincée de farine dessus.",
    ],
    (1, 3, 1): [
        "narrateur|Dans le panier, les fraises sentent le soleil.",
        "enfant-f|Sept bocaux, puis le mot.",
        "maman|Puis j'ai fini.",
        "papa|Une fraise chacun, avant le four.",
        "narrateur|La farine tourne dans le saladier, lente.",
        "narrateur|Le grain de vanille brille entre deux fraises.",
        "enfant-f|Il a suivi le panier.",
        "narrateur|Le goûter a failli rester dans l'ombre.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Sept bocaux se taisent, et le bois chante sous la cuillère.",
    ],
    (1, 3, 2): [
        "narrateur|Dans le panier bas, ça sent le rouge.",
        "enfant-f|Le bol n'avait rien.",
        "maman|Se baisser nous a aidées.",
        "papa|Ils croquent, les pieds sous la table.",
        "narrateur|La pâte monte, un peu, dans le saladier.",
        "narrateur|Le grain de vanille reste au bord, collé.",
        "enfant-f|Je ne l'ai pas enlevé.",
        "narrateur|Le goûter a failli rester trop bas.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Une fraise laisse un jus rose sur le bois.",
    ],
    (1, 3, 3): [
        "narrateur|Dans le bol rouge, pas dans le panier.",
        "enfant-f|J'ai failli dire le panier.",
        "maman|Le bol, pas le panier.",
        "papa|Une fraise casse, nette, entre les dents.",
        "narrateur|Le saladier reçoit les belles, une à une.",
        "narrateur|Le grain de vanille brille au fond du bol, oublié.",
        "enfant-f|On le met dans la pâte ?",
        "maman|Oui, tout petit.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le bol rouge reste vide, et le vrai gâteau cuit.",
    ],
    (2, 1, 1): [
        "narrateur|Le sac du milieu s'ouvre, sans nuage sucré.",
        "enfant-f|La cuillère peut tourner, maintenant.",
        "maman|Les fraises, après la pâte.",
        "papa|Le four chauffe, tout près.",
        "narrateur|La cuillère porte un filet de pâte, mince.",
        "narrateur|Un grain de vanille colle au dos du manche.",
        "enfant-f|Il a quitté la rainure.",
        "narrateur|Le goûter a failli rester un nuage.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|La cuillère porte un filet de pâte, mince.",
    ],
    (2, 1, 2): [
        "narrateur|Derrière le sucre, le sac attendait.",
        "enfant-f|Le tabouret m'a hissée.",
        "maman|Le mot est venu, après.",
        "papa|La cuillère tourne, lente, dans le bois.",
        "narrateur|Le manche sent la vanille, chaud.",
        "narrateur|Le grain noir brille au creux, un instant.",
        "enfant-f|Je le laisse.",
        "narrateur|Le goûter a failli rester trop haut.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le manche de bois sent la vanille, maintenant.",
    ],
    (2, 1, 3): [
        "narrateur|À côté du sel, le sac se penche.",
        "enfant-f|Papa m'a portée jusqu'au mot.",
        "maman|Le sel a gardé sa place.",
        "papa|La cuillère tape une fois, puis se tait.",
        "narrateur|La farine rejoint le beurre, sans nuage.",
        "narrateur|Un grain de vanille tient au dos de la cuillère.",
        "enfant-f|Comme au début.",
        "narrateur|Le goûter a failli rester contre la chemise.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|La cuillère tape une dernière fois, puis se tait.",
    ],
    (2, 2, 1): [
        "narrateur|Sous les serviettes, le papier est jaune.",
        "enfant-f|On s'est assises, d'abord.",
        "maman|Oui.",
        "papa|On suit la recette, près du four.",
        "narrateur|La cuillère brille, un peu blanche, sous la table.",
        "narrateur|Le grain de vanille colle au coin du papier.",
        "enfant-f|Je l'ai vu avant de parler.",
        "narrateur|Le goûter a failli rester plié.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Sous la table, la cuillère brille, un peu blanche.",
    ],
    (2, 2, 2): [
        "narrateur|Le rond jaune colle aux cuillères, un moment.",
        "maman|Le papier était le bon.",
        "enfant-f|La lampe a tenu le mot.",
        "papa|Une fraise casse, nette, entre les dents.",
        "narrateur|La cuillère tourne, et la pâte devient rose, un peu.",
        "narrateur|Un grain de vanille colle au dos de la cuillère.",
        "enfant-f|Il est venu avec la lumière.",
        "narrateur|Le goûter a failli rester dans l'ombre.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Un grain de vanille colle au dos de la cuillère.",
    ],
    (2, 2, 3): [
        "narrateur|Sous le linge, le papier attend.",
        "enfant-f|Tu as dit en dessous, à la fin.",
        "maman|Oui, à la fin.",
        "narrateur|Ils cassent un œuf, petit, dans le bois.",
        "papa|Le four ronronne, bas.",
        "narrateur|Le linge essuie le manche, sans tout prendre.",
        "enfant-f|Le grain reste.",
        "narrateur|Le goûter a failli rester sous le tissu.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le linge essuie le manche, sans l'effacer tout.",
    ],
    (2, 3, 1): [
        "narrateur|Dans le panier, les fraises sentent le soleil.",
        "enfant-f|Sept bocaux, puis le mot.",
        "maman|Puis j'ai fini.",
        "papa|Une fraise chacun, avant le four.",
        "narrateur|La cuillère compte les tours, lente, dans le bois.",
        "narrateur|Un grain de vanille brille entre deux fraises.",
        "enfant-f|Il a suivi le panier.",
        "narrateur|Le goûter a failli rester dans l'ombre.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|La cuillère compte les tours, lente, dans le bois.",
    ],
    (2, 3, 2): [
        "narrateur|Dans le panier bas, ça sent le rouge.",
        "enfant-f|Le bol n'avait rien.",
        "maman|Se baisser nous a aidées.",
        "papa|Ils croquent, les pieds sous la table.",
        "narrateur|La cuillère soulève une fraise, puis la pose.",
        "narrateur|Une graine de fraise reste au creux de la cuillère.",
        "enfant-f|Et le grain noir, à côté.",
        "narrateur|Le goûter a failli rester trop bas.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Une graine de fraise reste au creux de la cuillère.",
    ],
    (2, 3, 3): [
        "narrateur|Dans le bol rouge, pas dans le panier.",
        "enfant-f|J'ai failli dire le panier.",
        "maman|Le bol, pas le panier.",
        "papa|Une fraise casse, nette, entre les dents.",
        "narrateur|La cuillère prend les belles, une à une.",
        "narrateur|Le grain de vanille brille au fond du bol, oublié.",
        "enfant-f|On le met dans la pâte ?",
        "maman|Oui, tout petit.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le bol rouge n'a plus rien, et la cuillère a tout.",
    ],
    (3, 1, 1): [
        "narrateur|Le sac du milieu s'ouvre, sans nuage sucré.",
        "enfant-f|Le tablier a tenu, pendant l'attente.",
        "maman|Les fraises, après la pâte.",
        "papa|Le four chauffe, tout près.",
        "narrateur|Le tablier garde une carte de farine, petite.",
        "narrateur|Un grain de vanille colle au pli, près du nœud.",
        "enfant-f|Il a voyagé sur moi.",
        "narrateur|Le goûter a failli rester un nuage.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le tablier garde une carte de farine, petite.",
    ],
    (3, 1, 2): [
        "narrateur|Derrière le sucre, le sac attendait.",
        "enfant-f|Le tabouret m'a hissée, tablier large.",
        "maman|Le mot est venu, après.",
        "papa|La farine entre dans le bois, sans nuage.",
        "narrateur|Un pli du tablier sent le four, chaud.",
        "narrateur|Le grain noir brille sur le tissu, un instant.",
        "enfant-f|Je le laisse.",
        "narrateur|Le goûter a failli rester trop haut.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Un pli du tablier sent le four, chaud.",
    ],
    (3, 1, 3): [
        "narrateur|À côté du sel, le sac se penche.",
        "enfant-f|Papa m'a portée, tablier et tout.",
        "maman|Le sel a gardé sa place.",
        "papa|Une fraise laisse un jus rouge sur le tissu.",
        "narrateur|Le nœud du tablier reste contre son dos.",
        "narrateur|Un grain de vanille tient au nœud, collé.",
        "enfant-f|Comme au début.",
        "narrateur|Le goûter a failli rester contre la chemise.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le nœud du tablier reste contre son dos.",
    ],
    (3, 2, 1): [
        "narrateur|Sous les serviettes, le papier est jaune.",
        "enfant-f|On s'est assises, d'abord.",
        "maman|Oui.",
        "papa|On suit la recette, près du four.",
        "narrateur|Le tablier a un coin rose, de jus de fraise.",
        "narrateur|Le grain de vanille colle au coin du papier.",
        "enfant-f|Je l'ai vu avant de parler.",
        "narrateur|Le goûter a failli rester plié.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le tablier a un coin rose, de jus de fraise.",
    ],
    (3, 2, 2): [
        "narrateur|Le rond jaune colle aux cuillères, un moment.",
        "maman|Le papier était le bon.",
        "enfant-f|La lampe a tenu le mot.",
        "papa|Une fraise casse, nette, entre les dents.",
        "narrateur|La lampe s'éteint, et le tablier reste farineux.",
        "narrateur|Un grain de vanille brille sur le tissu, net.",
        "enfant-f|Il est venu avec la lumière.",
        "narrateur|Le goûter a failli rester dans l'ombre.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|La lampe s'éteint, et le tablier reste farineux.",
    ],
    (3, 2, 3): [
        "narrateur|Sous le linge, le papier attend.",
        "enfant-f|Tu as dit en dessous, à la fin.",
        "maman|Oui, à la fin.",
        "narrateur|Ils cassent un œuf, petit, dans le bois.",
        "papa|Le four ronronne, bas.",
        "narrateur|Le linge et le tablier se touchent, puis se séparent.",
        "enfant-f|Le grain reste sur moi.",
        "narrateur|Le goûter a failli rester sous le tissu.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le linge et le tablier se touchent, puis se séparent.",
    ],
    (3, 3, 1): [
        "narrateur|Dans le panier, les fraises sentent le soleil.",
        "enfant-f|Sept bocaux, puis le mot.",
        "maman|Puis j'ai fini.",
        "papa|Une fraise chacun, avant le four.",
        "narrateur|Le tablier sent les fraises, et un peu le bois.",
        "narrateur|Un grain de vanille brille entre deux fraises.",
        "enfant-f|Il a suivi le panier.",
        "narrateur|Le goûter a failli rester dans l'ombre.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le tablier sent les fraises, et un peu le bois.",
    ],
    (3, 3, 2): [
        "narrateur|Dans le panier bas, ça sent le rouge.",
        "enfant-f|Le bol n'avait rien.",
        "maman|Se baisser nous a aidées.",
        "papa|Ils croquent, les pieds sous la table.",
        "narrateur|Une feuille de fraise s'accroche au tablier, puis tombe.",
        "narrateur|Le grain de vanille reste au bord du panier.",
        "enfant-f|Je ne l'ai pas enlevé.",
        "narrateur|Le goûter a failli rester trop bas.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Une feuille de fraise s'accroche au tablier, puis tombe.",
    ],
    (3, 3, 3): [
        "narrateur|Dans le bol rouge, pas dans le panier.",
        "enfant-f|J'ai failli dire le panier.",
        "maman|Le bol, pas le panier.",
        "papa|Une fraise casse, nette, entre les dents.",
        "narrateur|Le tablier reçoit une goutte rose, petite.",
        "narrateur|Le grain de vanille brille au fond du bol, oublié.",
        "enfant-f|On le met dans la pâte ?",
        "maman|Oui, tout petit.",
        "narrateur|La cuisine sent le beurre et les fraises.",
        "narrateur|Le tablier a un rond de farine, comme un grain.",
    ],
}

END_SONS = {1: "four,bois", 2: "four,cuillere", 3: "four,tissu"}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "fraises,beurre",
        {"emphasis": "grain de vanille"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le saladier", "la cuillère", "le tablier")},
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
            {"emphasis": "grain de vanille"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("le placard", "le tiroir", "le garde-manger")},
        )
        for b in (1, 2, 3):
            bse = f"{base}_T0002_P000{b}"
            out_chunks[bse] = voice(
                by_src[bse], T2[(a, b)]["passage"], "obstacle", T2[(a, b)]["sons"],
                {"emphasis": T2[(a, b)]["emphasis"]},
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab(*T3_LABS[b])},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], t3(a, b, c), "resolution", T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ENDINGS[(a, b, c)], "ending", END_SONS[a],
                    {"emphasis": "grain de vanille"},
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
        "tom ",
        "tout doux",
        "tout calme",
        "tout lent",
        "aujourd'hui,",
        "j'ai compris",
        "mission accomplie",
        "merle",
        "miel",
        "grand-père",
        "maîtresse",
        "jardinier",
        "zoé",
        "lina",
        "iris",
        "léa",
        "sami",
        "ancre minuscule",
        "étoile brune",
        "fil pâle",
        "croissant d'eau",
        "croissant pâle",
        "virgule d'or",
        "virgule de farine",
        "œillet de cuivre",
        "oeillet de cuivre",
        "perle de verre",
        "marque fine",
        "ombre-flèche",
        "ombre en forme",
        "minuscule symbole",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "chouchou" not in blob:
        raise SystemExit(f"{SID}: Chouchou absente")
    if "grain de vanille" not in blob:
        raise SystemExit(f"{SID}: grain de vanille absent")

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
    if min(counts) < 520 or max(counts) > 740:
        raise SystemExit(f"chemins hors barre {min(counts)}-{max(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-028 — Le gâteau aux fraises de Chouchou\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.PAR.002 — laisser l'autre finir sa phrase (vécue, jamais dite)\n"
        "- **Personnages :** Chouchou, papa, maman (un seul enfant)\n"
        "- **Lieu :** cuisine, dimanche, goûter aux fraises — le fournil du dimanche\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Chouchou connaît la cuisine du dimanche. Un détail paraît nouveau : "
        "un **grain de vanille**, noir, collé dans la rainure du saladier. "
        "Elle veut le gâteau aux fraises prêt pour le goûter, maintenant. "
        "Maman cherche le mot. Chouchou tire le sucre : premier essai raté. "
        "Saladier, cuillère ou tablier : les trois partent. "
        "Placard (sacs jumeaux), tiroir (recette cachée) ou garde-manger (rouge mêlé). "
        "Elle refuse de foncer. Attendre, tabouret, papa porte ; "
        "s'asseoir, lampe, linge ; compter, panier, bol. "
        "Le grain du début revient. L'objet porte une trace. "
        "Le goûter a failli rester un nuage de sucre.\n\n"
        "## Vécu\n\n"
        "Chouchou propose trop vite. Maman prend son temps, cherche le mot. "
        "Le silence compte. Le sourire disparaît ; envie et inquiétude se bousculent. "
        "Papa s'accroupit à la même hauteur. Personne ne donne la réponse. "
        "Chouchou observe l'objet, écoute la cuisine, retrouve le grain. "
        "La leçon se voit : elle laisse la phrase arriver.\n\n"
        "## Vu et corrigé\n\n"
        "- Gabarit Lila / « tout doux / encore / déjà » / slogan jetés.\n"
        "- Indice unique (grain de vanille), pas ancre / étoile / virgule / œillet.\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'action. "
        "9 T2 distincts, 27 T3, 27 fins, 27 dernières images.\n"
        "- Merci vécu (sucre, souffle, nœud). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes`. "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N2 ≤ 15. `check()` OK. Pas apply. Pas git. Pas audio.\n\n"
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
