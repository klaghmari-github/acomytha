#!/usr/bin/env python3
"""TREE-DIF-031 — F-NAR-019. Panier rouge de Raphaël, potager. N2. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-031"
N2 = 15
TITLE = "Le panier rouge de Raphaël dans le potager"
FIL = (
    "Au rang des tomates, Raphaël veut remplir le panier rouge et le porter "
    "jusqu'à la marche, avant que papa coupe le pain. Un nœud de raphia "
    "tient le manche. Il tire trop vite : le nœud glisse. Nina ne veut pas "
    "la même chose. T1 = panier / chapeau / tabouret ; les trois partent. "
    "T2 = robinet (caillou) / figuier (trop chaud) / bac (gâteau). "
    "T3 = neuf façons d'inviter sans tirer. Le nœud tient. La salade arrive."
)
CHARS = "Raphaël, Nina, papa, maman"
SETTING = "potager, robinet, figuier, bac à sable"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "nœud de raphia",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le nœud paraît nouveau et Raphaël tire trop vite; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change l obstacle pas le kit; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
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
        "emphasis": "nœud de raphia",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_partent_Nina_n_est_pas_là; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=il_crie_trop_tôt_Nina_ne_vient_pas; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": "nœud de raphia",
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=Nina_a_une_autre_envie_le_nœud_rappelle_de_ne_pas_tirer; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=il_propose_et_accepte_oui_non_ou_plus_tard; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "nœud de raphia",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_nœud_paie_l_ouverture_la_salade_arrive_presque_pas; tempo=posé; sourire=léger; respiration=ample",
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
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"tic {m.group(0)!r}: {ph}")
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
    "narrateur|Raphaël connaît le potager, plant par plant.",
    "narrateur|Les feuilles de tomate sentent le soleil.",
    "narrateur|Elles collent aux doigts, chaudes.",
    "narrateur|Un grillon frotte dans l'herbe sèche.",
    "narrateur|Ça sent la terre, et le pain de la cuisine.",
    "narrateur|Le rang des tomates chauffe, bas.",
    "papa|L'arrosoir goutte, Raphaël.",
    "maman|Les dernières tomates, avant le pain.",
    "narrateur|Le panier rouge penche contre un pied.",
    "narrateur|Sur le manche, un nœud de raphia tient, plus sombre.",
    "enfant-m|Il n'était pas comme ça.",
    "narrateur|En ce moment, Raphaël touche le nœud.",
    "enfant-m|Je le remplis, avec Nina.",
    "narrateur|Il tire le panier, trop vite.",
    "narrateur|Le nœud de raphia glisse d'un cran.",
    "narrateur|Le sourire de Raphaël disparaît.",
    "narrateur|Une tomate trop rouge penche, lourde.",
    "papa|Merci, tu l'as rattrapé.",
    "maman|Tu la trouves où, Nina ?",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près des plants.",
    "narrateur|Le panier, le chapeau, et le tabouret.",
    "maman|Tu prends quoi, d'abord ?",
]

T1 = {
    1: {
        "lab": "le panier rouge",
        "sons": "osier,terre",
        "emphasis": "panier rouge",
        "passage": [
            "narrateur|Raphaël prend d'abord le panier rouge.",
            "enfant-m|Le nœud de raphia tient, plus sombre.",
            "maman|Passe-le à ton bras, sans tirer.",
            "narrateur|L'osier gratte un peu le coude.",
            "papa|Le chapeau de paille, près de toi.",
            "narrateur|Maman glisse le tabouret, contre sa jambe.",
            "narrateur|Les trois affaires partent ensemble.",
            "narrateur|Un papillon blanc passe entre les plants.",
            "enfant-m|Nina, les tomates !",
            "narrateur|Le rang des tomates ne répond pas.",
            "narrateur|Raphaël serre le manche, trop fort.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "narrateur|Il écoute le potager, un moment.",
            "papa|Il s'accroupit, à la même hauteur.",
            "papa|Tu l'invites, quand tu la trouves ?",
            "enfant-m|Oui, papa.",
        ],
        "question": [
            "narrateur|Raphaël a passé le panier rouge.",
            "maman|Il est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "bras",
            "accepted_examples": "bras | au bras | le bras | mon bras | à son bras",
            "retry_prompt": "Le panier pend au bras. Il est où ?",
        },
        "confirm": [
            "enfant-m|Au bras.",
            "maman|Oui.",
            "narrateur|Le panier rouge pend, un peu lourd.",
            "narrateur|Le nœud de raphia frotte le pouce.",
            "narrateur|Le gravier craque sous les sandales.",
            "enfant-m|Nina est dehors.",
            "papa|Je l'entends, dans le jardin.",
            "maman|Vous allez la trouver.",
            "enfant-m|Je lui propose les tomates.",
            "narrateur|Le nœud de raphia tient, d'un cran.",
            "narrateur|Le rang des tomates attend, tiède.",
        ],
        "voy": "Le panier rouge penche vers trois coins.",
    },
    2: {
        "lab": "le chapeau de paille",
        "sons": "paille,vent",
        "emphasis": "chapeau de paille",
        "passage": [
            "narrateur|Raphaël prend d'abord le chapeau de paille.",
            "enfant-m|Il gratte un peu, aux tempes.",
            "papa|Mets-le, le soleil tape fort.",
            "narrateur|La paille fait une ombre ronde.",
            "maman|Le panier, ensuite, près de toi.",
            "narrateur|Il glisse le tabouret d'une main.",
            "narrateur|Les trois affaires partent ensemble.",
            "narrateur|Un rayon tape le bord de paille.",
            "enfant-m|Nina, viens sous l'ombre !",
            "narrateur|Personne ne répond, entre les plants.",
            "narrateur|Le chapeau glisse, trop vite.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "narrateur|Il écoute le potager, un moment.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "maman|Tu lui proposes les tomates ?",
            "enfant-m|Oui, maman.",
        ],
        "question": [
            "narrateur|Raphaël a mis le chapeau de paille.",
            "maman|Il est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "tête",
            "accepted_examples": "tête | sa tête | sur sa tête | le chapeau | chapeau",
            "retry_prompt": "Le chapeau est sur sa tête. Il est où ?",
        },
        "confirm": [
            "enfant-m|Sur sa tête.",
            "papa|Oui.",
            "narrateur|Le chapeau de paille tient une ombre ronde.",
            "narrateur|Le nœud de raphia pend au bras, avec le panier.",
            "narrateur|Un grillon reprend, plus loin.",
            "enfant-m|Nina est dehors.",
            "maman|Je l'entends, dans le jardin.",
            "papa|Le soleil tape, entre les plants.",
            "enfant-m|Je lui propose les tomates.",
            "narrateur|Le nœud de raphia tient, d'un cran.",
            "narrateur|Le rang des tomates sent le chaud.",
        ],
        "voy": "Le chapeau de paille penche vers trois coins.",
    },
    3: {
        "lab": "le petit tabouret",
        "sons": "bois,toc",
        "emphasis": "petit tabouret",
        "passage": [
            "narrateur|Raphaël tire d'abord le petit tabouret.",
            "enfant-m|Les tomates du haut, avec ça.",
            "maman|Tiens-le droit, sans le traîner.",
            "narrateur|Le bois tape un petit toc.",
            "papa|Le panier et le chapeau, avec toi.",
            "narrateur|Il les pose près des sandales.",
            "narrateur|Les trois affaires partent ensemble.",
            "narrateur|Un toc répond, plus loin, dans le bois.",
            "enfant-m|Nina va tout atteindre !",
            "narrateur|Le rang des tomates reste muet.",
            "narrateur|Le tabouret bascule, trop vite.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "narrateur|Il écoute le potager, un moment.",
            "papa|Il s'accroupit, à la même hauteur.",
            "papa|Tu lui proposes, sans crier ?",
            "enfant-m|Oui.",
        ],
        "question": [
            "narrateur|Raphaël a tiré le petit tabouret.",
            "maman|Il est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "pieds",
            "accepted_examples": "pieds | les pieds | près des pieds | au sol | tabouret",
            "retry_prompt": "Le tabouret est près des pieds. Il est où ?",
        },
        "confirm": [
            "enfant-m|Près des pieds.",
            "maman|Oui.",
            "narrateur|Le petit tabouret avance, un toc après l'autre.",
            "narrateur|Le nœud de raphia frotte le manche, au bras.",
            "narrateur|La terre tiède colle aux sandales.",
            "enfant-m|Nina est dehors.",
            "papa|Je l'entends, dans le jardin.",
            "maman|Les plants laissent un sentier étroit.",
            "enfant-m|Je lui propose les tomates.",
            "narrateur|Le nœud de raphia tient, d'un cran.",
            "narrateur|Le rang des tomates attend, bas.",
        ],
        "voy": "Le petit tabouret avance vers trois coins.",
    },
}

T2 = {
    (1, 1): {
        "sons": "eau,caillou",
        "emphasis": "caillou",
        "passage": [
            "narrateur|Le panier rouge voyage vers le robinet.",
            "narrateur|Nina frotte un caillou blanc, absorbée.",
            "enfant-m|Nina, les tomates sont prêtes !",
            "narrateur|Elle ne lève pas les yeux.",
            "enfant-f|Il est sale, mon caillou.",
            "enfant-m|Tu viens cueillir ?",
            "narrateur|Nina ne dit rien.",
            "narrateur|Ce silence tient, comme une réponse.",
            "narrateur|L'eau mouille le nœud de raphia.",
            "narrateur|Raphaël veut tirer le panier, trop fort.",
            "narrateur|Il s'arrête, le pouce sur le nœud.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu proposes comment, Raphaël ?",
        ],
    },
    (2, 1): {
        "sons": "eau,paille",
        "emphasis": "caillou",
        "passage": [
            "narrateur|Le chapeau de paille penche vers le robinet.",
            "narrateur|Une éclaboussure entre dans le bord.",
            "enfant-m|Nina, viens sous l'ombre !",
            "narrateur|Elle frotte son caillou, sans lever les yeux.",
            "enfant-f|Attends.",
            "narrateur|Raphaël veut secouer le chapeau.",
            "narrateur|L'eau partirait sur le caillou.",
            "narrateur|Il refuse de foncer.",
            "narrateur|Il touche le nœud de raphia, au bras.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à la même hauteur.",
            "maman|Tu proposes comment, Raphaël ?",
        ],
    },
    (3, 1): {
        "sons": "eau,bois",
        "emphasis": "caillou",
        "passage": [
            "narrateur|Le petit tabouret avance vers le robinet.",
            "narrateur|Ses pieds trempent dans une flaque.",
            "enfant-m|Nina, les tomates du haut !",
            "narrateur|Elle frotte le caillou, collée à l'eau.",
            "enfant-f|Je n'ai pas fini.",
            "narrateur|Raphaël veut planter le tabouret, trop près.",
            "narrateur|La flaque sauterait sur le caillou.",
            "narrateur|Il recule d'un cran, le bois en main.",
            "narrateur|Le nœud de raphia frotte son pouce.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu proposes comment, Raphaël ?",
        ],
    },
    (1, 2): {
        "sons": "feuilles,vent",
        "emphasis": "figuier",
        "passage": [
            "narrateur|Le panier rouge s'arrête sous le figuier.",
            "narrateur|Nina est allongée sous les grandes feuilles.",
            "enfant-f|J'ai trop chaud, Raphaël.",
            "enfant-m|Les tomates sont là-bas.",
            "narrateur|L'osier brûle un peu les doigts.",
            "enfant-m|Tu viens ?",
            "enfant-f|Je ne veux pas bouger.",
            "narrateur|Une feuille de figue tapote son front.",
            "narrateur|Raphaël veut tirer le panier, trop vite.",
            "narrateur|Il voit le nœud de raphia, plus sombre.",
            "narrateur|Il refuse de foncer.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à la même hauteur.",
            "maman|Tu fais comment, Raphaël ?",
        ],
    },
    (2, 2): {
        "sons": "feuilles,paille",
        "emphasis": "figuier",
        "passage": [
            "narrateur|Le chapeau de paille glisse sous le figuier.",
            "narrateur|Nina reste collée à l'ombre des feuilles.",
            "enfant-m|Mon chapeau fait de l'ombre, aussi.",
            "enfant-f|Moins que le figuier.",
            "narrateur|L'ombre de paille est trop petite, pour deux.",
            "enfant-m|Tu viens cueillir ?",
            "narrateur|Nina secoue la tête, minuscule.",
            "narrateur|Ce silence tient, comme une réponse.",
            "narrateur|Raphaël veut poser le chapeau sur elle.",
            "narrateur|Il s'arrête, le nœud de raphia sous les doigts.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "maman|Elle s'accroupit, à sa hauteur.",
            "papa|Tu fais comment, Raphaël ?",
        ],
    },
    (3, 2): {
        "sons": "feuilles,bois",
        "emphasis": "figuier",
        "passage": [
            "narrateur|Le petit tabouret bute sous le figuier.",
            "narrateur|Le bois est chaud, trop chaud.",
            "enfant-m|Tu t'assois, Nina ?",
            "enfant-f|Le bois brûle, non.",
            "narrateur|Nina reste allongée, une feuille sur le front.",
            "enfant-m|Les tomates du haut t'attendent.",
            "narrateur|Nina ne dit rien, plus longtemps.",
            "narrateur|Raphaël veut la tirer, trop vite.",
            "narrateur|Il pose une main sur le nœud de raphia.",
            "narrateur|Il refuse de foncer.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à la même hauteur.",
            "maman|Tu fais comment, Raphaël ?",
        ],
    },
    (1, 3): {
        "sons": "sable,eau",
        "emphasis": "gâteau",
        "passage": [
            "narrateur|Le panier rouge pose son ombre sur le bac.",
            "narrateur|Nina patouille un gâteau de sable.",
            "enfant-f|Il n'est pas cuit.",
            "enfant-m|Les tomates m'attendent.",
            "narrateur|Le gâteau penche, mouillé.",
            "enfant-m|Tu viens cueillir ?",
            "enfant-f|Après, peut-être.",
            "narrateur|Raphaël veut poser le panier, trop près.",
            "narrateur|Le gâteau s'écraserait, net.",
            "narrateur|Il recule, le nœud de raphia serré.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "maman|Son gâteau n'est pas fini.",
            "papa|Tu proposes quoi, Raphaël ?",
        ],
    },
    (2, 3): {
        "sons": "sable,paille",
        "emphasis": "gâteau",
        "passage": [
            "narrateur|Le chapeau de paille fait un rond sur le bac.",
            "narrateur|L'ombre tombe sur le gâteau de sable.",
            "enfant-f|Pas d'ombre, il cuit.",
            "enfant-m|Les tomates, Nina.",
            "narrateur|Nina protège le gâteau, d'une main.",
            "enfant-m|Tu viens ?",
            "narrateur|Nina ne dit rien.",
            "narrateur|Ce silence tient, comme une réponse.",
            "narrateur|Raphaël veut enlever le chapeau, trop vite.",
            "narrateur|Il s'arrête, le nœud de raphia au pouce.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "papa|Il s'accroupit, à la même hauteur.",
            "maman|Tu proposes quoi, Raphaël ?",
        ],
    },
    (3, 3): {
        "sons": "sable,bois",
        "emphasis": "gâteau",
        "passage": [
            "narrateur|Le petit tabouret pose un pied près du bac.",
            "narrateur|Nina lisse un bord du gâteau.",
            "enfant-m|On cueille, après ?",
            "enfant-f|Quand il sera cuit.",
            "narrateur|Le bois menace le mur de sable.",
            "enfant-m|Je le mets là ?",
            "enfant-f|Pas contre mon gâteau.",
            "narrateur|Raphaël veut pousser le tabouret, trop près.",
            "narrateur|Il recule, le nœud de raphia sous les doigts.",
            "narrateur|Il refuse de foncer.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "maman|Le gâteau penche, fragile.",
            "papa|Tu proposes quoi, Raphaël ?",
        ],
    },
}

T3_LABS = {
    1: ("attendre un peu", "prendre le caillou", "laver une tomate"),
    2: ("apporter de l'eau", "l'ombre des plants", "garder une tomate"),
    3: ("attendre le gâteau", "déplacer le gâteau", "proposer plus tard"),
}

T3_CHOICE = {
    1: [
        "narrateur|Nina frotte son caillou blanc.",
        "narrateur|Le nœud de raphia reste mouillé.",
        "papa|Attendre, prendre le caillou, ou laver ?",
    ],
    2: [
        "narrateur|Nina reste collée à l'ombre du figuier.",
        "narrateur|Le nœud de raphia tient, plus sombre.",
        "maman|L'eau, l'ombre des plants, ou garder une tomate ?",
    ],
    3: [
        "narrateur|Le gâteau de sable penche, fragile.",
        "narrateur|Le nœud de raphia frotte le pouce.",
        "papa|Attendre, déplacer, ou plus tard ?",
    ],
}

T3_SONS = {
    (1, 1): "eau,osier",
    (1, 2): "eau,caillou",
    (1, 3): "eau,tomate",
    (2, 1): "eau,feuilles",
    (2, 2): "feuilles,terre",
    (2, 3): "tomate,feuilles",
    (3, 1): "sable,vent",
    (3, 2): "sable,osier",
    (3, 3): "sable,marche",
}

T3_EMPH = {
    1: {1: "caillou", 2: "caillou", 3: "tomate"},
    2: {1: "eau", 2: "ombre des plants", 3: "tomate"},
    3: {1: "gâteau", 2: "gâteau", 3: "plus tard"},
}

T3 = {
    (1, 1, 1): [
        "enfant-m|J'attends un peu.",
        "enfant-f|Merci, Raphaël.",
        "narrateur|Raphaël touche le nœud de raphia.",
        "narrateur|Il refuse de tirer.",
        "narrateur|L'eau coule, puis se tait.",
        "narrateur|Nina lève le caillou, propre.",
        "enfant-f|Je viens, maintenant.",
        "enfant-m|Les tomates sont chaudes.",
        "papa|Tu as laissé son caillou finir.",
        "maman|Elle a dit oui, à son heure.",
        "narrateur|Le panier rouge attend, derrière elle.",
        "narrateur|Une goutte reste au nœud de raphia.",
    ],
    (1, 1, 2): [
        "enfant-m|Ton caillou peut venir, avec nous.",
        "enfant-f|Avec les tomates ?",
        "enfant-m|Si tu veux.",
        "narrateur|Le caillou blanc entre dans le panier.",
        "narrateur|Le nœud de raphia le cale, sans serrer.",
        "enfant-f|Il va nous regarder.",
        "enfant-m|On cueille ensemble, alors.",
        "papa|Tu as pris son jeu avec toi.",
        "maman|Le caillou a sa place.",
        "narrateur|Nina pose le caillou, blanc.",
        "narrateur|L'osier sent l'eau, et la pierre.",
    ],
    (1, 1, 3): [
        "enfant-m|Je lave une tomate, avec toi.",
        "narrateur|Il pose une tomate sous le filet.",
        "narrateur|Le nœud de raphia se mouille, sans céder.",
        "narrateur|Ils frottent, côte à côte.",
        "enfant-f|Elle est propre.",
        "enfant-m|On va en chercher d'autres ?",
        "enfant-f|Oui, après celle-là.",
        "papa|Tu t'es assis à son jeu.",
        "maman|Elle a proposé la suite.",
        "narrateur|Le panier rouge reste mouillé, au bord.",
        "narrateur|Une feuille de tomate colle au nœud.",
    ],
    (1, 2, 1): [
        "enfant-m|Je t'apporte de l'eau, d'abord.",
        "narrateur|Il penche le panier, une gorgée au fond.",
        "narrateur|Le nœud de raphia sent l'eau fraîche.",
        "narrateur|Nina boit, à petites gorgées.",
        "enfant-f|C'est mieux.",
        "enfant-m|Tu viens, si tu veux.",
        "enfant-f|Oui, j'arrive.",
        "papa|Tu as attendu qu'elle ait moins chaud.",
        "maman|Elle a dit oui, après l'eau.",
        "narrateur|Une feuille de figue retombe, plus légère.",
        "narrateur|Le panier rouge reste frais, un instant.",
    ],
    (1, 2, 2): [
        "enfant-m|L'ombre des plants est fraîche, aussi.",
        "enfant-f|Moins que le figuier.",
        "enfant-m|On cueille là, si tu veux.",
        "enfant-f|D'accord, à l'ombre.",
        "narrateur|Le panier rouge glisse vers l'ombre des plants.",
        "narrateur|Le nœud de raphia frotte une feuille.",
        "narrateur|Ils glissent entre les plants, sans se presser.",
        "papa|Vous restez au frais, tous les deux.",
        "maman|Les tomates pendent, juste là.",
        "enfant-m|Celle-ci, pour toi.",
        "narrateur|Une ombre de feuille reste au nœud.",
    ],
    (1, 2, 3): [
        "enfant-f|Plus tard, Raphaël.",
        "enfant-m|D'accord.",
        "enfant-m|Je t'en garde une, alors.",
        "narrateur|Une tomate rouge attend dans le panier, à part.",
        "narrateur|Le nœud de raphia la serre, sans la blesser.",
        "narrateur|Nina ferme les yeux, un moment.",
        "enfant-f|Merci.",
        "papa|Sa tomate reste avec elle.",
        "maman|Vous vous retrouvez, tout à l'heure.",
        "narrateur|Le figuier garde son ombre ronde.",
        "narrateur|Le panier rouge veille, à part.",
    ],
    (1, 3, 1): [
        "enfant-m|Je reste jusqu'au gâteau.",
        "enfant-f|Il manque le soleil, dessus.",
        "narrateur|Le panier rouge fait un four, à côté.",
        "narrateur|Le nœud de raphia tient, sans bouger.",
        "narrateur|Ils soufflent une fois, tout bas.",
        "enfant-f|Il est cuit, maintenant.",
        "enfant-m|On cueille, alors ?",
        "enfant-f|Oui.",
        "papa|Tu as laissé le gâteau finir.",
        "maman|Le gâteau a eu son temps.",
        "narrateur|Un grain de sable brille dans le nœud.",
    ],
    (1, 3, 2): [
        "enfant-m|Le gâteau peut voyager, près des plants.",
        "enfant-f|Sans le casser ?",
        "enfant-m|Sans le casser.",
        "narrateur|Le gâteau voyage dans le panier, fragile.",
        "narrateur|Le nœud de raphia le cale, d'un cran.",
        "narrateur|Le sable tient, à peine.",
        "enfant-f|Il est venu avec nous.",
        "enfant-m|On cueille, et il nous regarde.",
        "papa|Tu as mêlé les deux jeux.",
        "maman|Rien n'a été laissé derrière.",
        "narrateur|Une miette de sable reste au nœud.",
    ],
    (1, 3, 3): [
        "enfant-m|On cueille plus tard, alors ?",
        "enfant-f|Oui, plus tard.",
        "enfant-m|D'accord.",
        "narrateur|Le panier rouge reste au bord du bac.",
        "narrateur|Nina lisse un bord, sans se presser.",
        "enfant-f|Garde-moi une tomate rouge.",
        "enfant-m|Elle t'attend.",
        "papa|Tu as proposé une autre heure.",
        "maman|Le gâteau continue, à son pas.",
        "narrateur|Le nœud de raphia attend, sans tirer.",
        "narrateur|Un grain de sable reste sous l'osier.",
    ],
    (2, 1, 1): [
        "enfant-m|J'attends, près de l'eau.",
        "enfant-f|Merci.",
        "narrateur|Nina frotte, sans parler.",
        "narrateur|Le chapeau de paille attend derrière elle.",
        "narrateur|Raphaël touche le nœud de raphia, au bras.",
        "narrateur|Nina lève le caillou, à son heure.",
        "enfant-f|Je viens sous l'ombre.",
        "enfant-m|Elle est un peu mouillée.",
        "papa|Son caillou a fini, tout seul.",
        "maman|Elle a dit oui, après.",
        "narrateur|Une goutte sèche au bord de paille.",
        "narrateur|Le nœud de raphia luisant tient.",
    ],
    (2, 1, 2): [
        "enfant-m|Ton caillou peut voyager, dans le chapeau.",
        "enfant-f|Sans tomber ?",
        "enfant-m|Je le tiens.",
        "narrateur|Le caillou blanc se pose dans le chapeau.",
        "narrateur|Le nœud de raphia serre le manche, au bras.",
        "enfant-f|Il a de l'ombre, maintenant.",
        "enfant-m|On cueille ensemble, alors.",
        "papa|Tu as pris son jeu avec toi.",
        "maman|Le caillou a sa place.",
        "narrateur|La paille sent la pierre, et l'eau.",
        "narrateur|Nina marche à son pas, le chapeau près d'elle.",
    ],
    (2, 1, 3): [
        "enfant-m|Je lave une tomate, avec toi.",
        "narrateur|Le chapeau fait de l'ombre sur leurs mains.",
        "narrateur|Le nœud de raphia se mouille, sans céder.",
        "narrateur|Ils frottent sous le filet d'eau.",
        "enfant-f|Elle est propre, maintenant.",
        "enfant-m|On va en chercher d'autres ?",
        "enfant-f|Oui, après celle-là.",
        "papa|Tu t'es assis à son jeu.",
        "maman|Elle a proposé la suite.",
        "narrateur|Une goutte tombe du bord de paille.",
        "narrateur|La paille sent la tomate, et l'eau.",
    ],
    (2, 2, 1): [
        "enfant-m|Je t'apporte de l'eau, d'abord.",
        "narrateur|Il lui tend le chapeau, pour faire de l'ombre.",
        "narrateur|Une gorgée attend dans une tasse, à part.",
        "narrateur|Nina boit, à petites gorgées.",
        "enfant-f|C'est mieux.",
        "enfant-m|Tu viens, si tu veux.",
        "enfant-f|Oui, j'arrive.",
        "papa|Tu as attendu qu'elle ait moins chaud.",
        "maman|Elle a dit oui, après l'eau.",
        "narrateur|Le nœud de raphia sent l'eau fraîche.",
        "narrateur|Le chapeau de paille reste frais, un instant.",
    ],
    (2, 2, 2): [
        "enfant-m|L'ombre des plants est fraîche, aussi.",
        "enfant-f|Moins que le figuier.",
        "enfant-m|On cueille là, si tu veux.",
        "enfant-f|D'accord, à l'ombre.",
        "narrateur|Le chapeau de paille avance vers les plants.",
        "narrateur|Le nœud de raphia frotte une feuille.",
        "narrateur|Deux ombres se mêlent, paille et plants.",
        "papa|Vous restez au frais, tous les deux.",
        "maman|Les tomates pendent, juste là.",
        "enfant-m|Celle-ci, pour toi.",
        "narrateur|L'ombre de paille reste sur les plants.",
    ],
    (2, 2, 3): [
        "enfant-f|Plus tard, Raphaël.",
        "enfant-m|D'accord.",
        "enfant-m|Je t'en garde une, alors.",
        "narrateur|Une tomate rouge attend sous le chapeau.",
        "narrateur|Le nœud de raphia la serre, sans la blesser.",
        "narrateur|Nina ferme les yeux, un moment.",
        "enfant-f|Merci.",
        "papa|Sa tomate reste avec elle.",
        "maman|Vous vous retrouvez, tout à l'heure.",
        "narrateur|Le figuier garde son ombre ronde.",
        "narrateur|Une tomate dort sous le chapeau, au secret.",
    ],
    (2, 3, 1): [
        "enfant-m|Je reste jusqu'au gâteau.",
        "enfant-f|Il manque le soleil, dessus.",
        "narrateur|Le chapeau de paille fait un toit, à côté.",
        "narrateur|Le nœud de raphia tient, sans bouger.",
        "narrateur|Ils soufflent une fois, tout bas.",
        "enfant-f|Il est cuit, maintenant.",
        "enfant-m|On cueille, alors ?",
        "enfant-f|Oui.",
        "papa|Tu as laissé le gâteau finir.",
        "maman|Le gâteau a eu son temps.",
        "narrateur|Un grain de sable colle à la paille.",
        "narrateur|Le chapeau sèche, le nœud luisant.",
    ],
    (2, 3, 2): [
        "enfant-m|Le gâteau peut voyager, sous le chapeau.",
        "enfant-f|Sans le casser ?",
        "enfant-m|Sans le casser.",
        "narrateur|Le gâteau voyage sous le chapeau, fragile.",
        "narrateur|Le nœud de raphia le cale, d'un cran.",
        "narrateur|Le sable tient, à peine.",
        "enfant-f|Il est venu avec nous.",
        "enfant-m|On cueille, et il nous regarde.",
        "papa|Tu as mêlé les deux jeux.",
        "maman|Rien n'a été laissé derrière.",
        "narrateur|Le chapeau de paille porte une miette de sable.",
    ],
    (2, 3, 3): [
        "enfant-m|On cueille plus tard, alors ?",
        "enfant-f|Oui, plus tard.",
        "enfant-m|D'accord.",
        "narrateur|Le chapeau de paille reste au bord du bac.",
        "narrateur|Nina lisse un bord, sans se presser.",
        "enfant-f|Garde-moi une tomate rouge.",
        "enfant-m|Elle t'attend.",
        "papa|Tu as proposé une autre heure.",
        "maman|Le gâteau continue, à son pas.",
        "narrateur|Le nœud de raphia attend, sans tirer.",
        "narrateur|Un grain de sable reste sous la paille.",
    ],
    (3, 1, 1): [
        "enfant-m|J'attends, près de l'eau.",
        "enfant-f|Merci.",
        "narrateur|Nina frotte, sans parler.",
        "narrateur|Le petit tabouret attend derrière elle.",
        "narrateur|Raphaël touche le nœud de raphia, au bras.",
        "narrateur|Nina lève le caillou, à son heure.",
        "enfant-f|Je viens, maintenant.",
        "enfant-m|Les tomates du haut sont chaudes.",
        "papa|Son caillou a fini, tout seul.",
        "maman|Elle a dit oui, après.",
        "narrateur|Le bois sèche, une goutte au pied.",
        "narrateur|Le nœud de raphia luisant tient.",
    ],
    (3, 1, 2): [
        "enfant-m|Ton caillou peut s'asseoir, sur le tabouret.",
        "enfant-f|Avec nous ?",
        "enfant-m|Si tu veux.",
        "narrateur|Le caillou blanc s'assoit sur le tabouret.",
        "narrateur|Le nœud de raphia serre le manche, au bras.",
        "enfant-f|Il va nous regarder.",
        "enfant-m|On cueille ensemble, alors.",
        "papa|Tu as pris son jeu avec toi.",
        "maman|Le caillou a sa place.",
        "narrateur|Le bois sent la pierre, et l'eau.",
        "narrateur|Nina marche à son pas, le tabouret près d'elle.",
    ],
    (3, 1, 3): [
        "enfant-m|Je lave une tomate, avec toi.",
        "narrateur|Il s'assoit sur le tabouret, tout près.",
        "narrateur|Le nœud de raphia se mouille, sans céder.",
        "narrateur|Ils frottent sous le filet d'eau.",
        "enfant-f|Elle est propre, maintenant.",
        "enfant-m|On va en chercher d'autres ?",
        "enfant-f|Oui, après celle-là.",
        "papa|Tu t'es assis à son jeu.",
        "maman|Elle a proposé la suite.",
        "narrateur|Une tomate mouillée brille sur le bois.",
        "narrateur|Le tabouret sent l'eau, et la tomate.",
    ],
    (3, 2, 1): [
        "enfant-m|Je t'apporte de l'eau, d'abord.",
        "narrateur|Il pose le tabouret, une tasse dessus.",
        "narrateur|Le nœud de raphia sent l'eau fraîche.",
        "narrateur|Nina boit, à petites gorgées.",
        "enfant-f|C'est mieux.",
        "enfant-m|Tu viens, si tu veux.",
        "enfant-f|Oui, j'arrive.",
        "papa|Tu as attendu qu'elle ait moins chaud.",
        "maman|Elle a dit oui, après l'eau.",
        "narrateur|Une feuille de figue retombe, plus légère.",
        "narrateur|Le petit tabouret reste frais, un instant.",
    ],
    (3, 2, 2): [
        "enfant-m|L'ombre des plants est fraîche, aussi.",
        "enfant-f|Moins que le figuier.",
        "enfant-m|On cueille là, si tu veux.",
        "enfant-f|D'accord, à l'ombre.",
        "narrateur|Le petit tabouret avance vers les plants.",
        "narrateur|Le nœud de raphia frotte une feuille.",
        "narrateur|Ils glissent entre les plants, sans se presser.",
        "papa|Vous restez au frais, tous les deux.",
        "maman|Les tomates pendent, juste là.",
        "enfant-m|Celle-ci, pour toi.",
        "narrateur|L'ombre des plants couvre le bois du tabouret.",
    ],
    (3, 2, 3): [
        "enfant-f|Plus tard, Raphaël.",
        "enfant-m|D'accord.",
        "enfant-m|Je t'en garde une, alors.",
        "narrateur|Une tomate rouge attend sur le tabouret.",
        "narrateur|Le nœud de raphia la serre, sans la blesser.",
        "narrateur|Nina ferme les yeux, un moment.",
        "enfant-f|Merci.",
        "papa|Sa tomate reste avec elle.",
        "maman|Vous vous retrouvez, tout à l'heure.",
        "narrateur|Le figuier garde son ombre ronde.",
        "narrateur|Une tomate attend, posée sur le tabouret.",
    ],
    (3, 3, 1): [
        "enfant-m|Je reste jusqu'au gâteau.",
        "enfant-f|Il manque le soleil, dessus.",
        "narrateur|Le petit tabouret fait une table, à côté.",
        "narrateur|Le nœud de raphia tient, sans bouger.",
        "narrateur|Ils soufflent une fois, tout bas.",
        "enfant-f|Il est cuit, maintenant.",
        "enfant-m|On cueille, alors ?",
        "enfant-f|Oui.",
        "papa|Tu as laissé le gâteau finir.",
        "maman|Le gâteau a eu son temps.",
        "narrateur|Un grain de sable reste sous le tabouret.",
        "narrateur|Le bois sèche, le nœud luisant.",
    ],
    (3, 3, 2): [
        "enfant-m|Le gâteau peut voyager, sur le tabouret.",
        "enfant-f|Sans le casser ?",
        "enfant-m|Sans le casser.",
        "narrateur|Le gâteau voyage sur le tabouret, fragile.",
        "narrateur|Le nœud de raphia le cale, d'un cran.",
        "narrateur|Le sable tient, à peine.",
        "enfant-f|Il est venu avec nous.",
        "enfant-m|On cueille, et il nous regarde.",
        "papa|Tu as mêlé les deux jeux.",
        "maman|Rien n'a été laissé derrière.",
        "narrateur|Le gâteau de sable veille près du bois.",
    ],
    (3, 3, 3): [
        "enfant-m|On cueille plus tard, alors ?",
        "enfant-f|Oui, plus tard.",
        "enfant-m|D'accord.",
        "narrateur|Le petit tabouret reste au bord du bac.",
        "narrateur|Nina lisse un bord, sans se presser.",
        "enfant-f|Garde-moi une tomate rouge.",
        "enfant-m|Elle t'attend.",
        "papa|Tu as proposé une autre heure.",
        "maman|Le gâteau continue, à son pas.",
        "narrateur|Le nœud de raphia attend, sans tirer.",
        "narrateur|Un grain de sable reste sous le bois.",
    ],
}

END_SONS = {1: "eau,pain", 2: "feuilles,pain", 3: "sable,pain"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Ils rentrent les tomates, chaudes.",
        "enfant-f|Mon caillou est propre, maintenant.",
        "enfant-m|Toi aussi, tu es venue.",
        "papa|La salade attend sur la marche.",
        "maman|Le pain a une croûte.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "enfant-m|J'ai presque tiré, trop fort.",
        "narrateur|Nina pose le caillou près du sel.",
        "enfant-m|C'est notre salade, maintenant.",
        "narrateur|Le nœud de raphia sèche, une goutte au bout.",
    ],
    (1, 1, 2): [
        "narrateur|Le caillou blanc veille entre les tomates.",
        "enfant-m|Tu as dit oui, avec lui.",
        "enfant-f|Il a tout vu, du panier.",
        "papa|Vous avez cueilli sans tirer.",
        "maman|Goûtez un peu, avant le soir.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina croque, le jus lui rougit le menton.",
        "enfant-m|Reste autant que tu veux.",
        "narrateur|Le sel brille sur la marche.",
        "narrateur|Le nœud de raphia tient le caillou blanc.",
    ],
    (1, 1, 3): [
        "narrateur|Après l'eau, ils glissent entre les plants.",
        "enfant-f|On a lavé ensemble, d'abord.",
        "enfant-m|Puis tu as dit : on y va.",
        "maman|Deux mains mouillées, puis deux tomates.",
        "papa|Le jardin redevient large.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina rit, tout petit.",
        "enfant-m|La salade t'a attendue.",
        "narrateur|L'arrosoir sèche, près du mur.",
        "narrateur|Une feuille de tomate reste dans le nœud.",
    ],
    (1, 2, 1): [
        "narrateur|Après l'eau, le figuier les laisse partir.",
        "enfant-f|J'avais moins chaud, alors j'ai dit oui.",
        "enfant-m|Ta tomate est celle-là.",
        "papa|Vous tenez tous les deux, entre les plants.",
        "maman|Le pain descend jusqu'à la marche.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina souffle sur une graine, légère.",
        "enfant-m|C'est le signal.",
        "narrateur|Une feuille de figue reste au seuil.",
        "narrateur|Le nœud de raphia sent l'eau du figuier.",
    ],
    (1, 2, 2): [
        "narrateur|L'ombre des plants a deux places, maintenant.",
        "enfant-m|La tienne, et la mienne.",
        "enfant-f|C'est la nôtre, Raphaël.",
        "papa|Vous avez changé d'ombre, pas de jeu.",
        "maman|La salade, au milieu, pour deux.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina souffle, puis Raphaël souffle.",
        "enfant-m|On reste un peu.",
        "narrateur|Une tomate garde sa chaleur.",
        "narrateur|Le nœud de raphia garde une ombre de feuille.",
    ],
    (1, 2, 3): [
        "narrateur|Plus tard, Nina rejoint la marche.",
        "enfant-f|Ma tomate m'a attendue.",
        "enfant-m|Tu avais dit plus tard.",
        "papa|Le plus tard a eu sa place.",
        "maman|Vous mangez ensemble, d'ici.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina tend une main, vers le sel.",
        "enfant-m|Je te la passe, d'à côté.",
        "narrateur|Le figuier laisse une ombre ronde.",
        "narrateur|Le nœud de raphia serre une tomate, à part.",
    ],
    (1, 3, 1): [
        "narrateur|Le gâteau de sable est fini.",
        "enfant-f|J'ai eu le temps, juste assez.",
        "enfant-m|Merci d'être venue.",
        "papa|Vous avez soufflé une fois, tout bas.",
        "maman|Les tomates sont dans l'assiette, maintenant.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina fait un signe vers le bac.",
        "enfant-m|Le gâteau t'a vue, une minute.",
        "narrateur|Le sable du bac redevient plat.",
        "narrateur|Un grain de sable brille dans le nœud.",
    ],
    (1, 3, 2): [
        "narrateur|Le gâteau de sable veille près des plants.",
        "enfant-m|Il a voyagé avec nous.",
        "enfant-f|Sans se casser.",
        "papa|Vous avez mêlé les deux envies.",
        "maman|Le pain sent le four.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina pose un grain de sable, plus loin.",
        "enfant-m|La salade est à nous.",
        "narrateur|Une fourmi croise une graine, puis s'en va.",
        "narrateur|Le nœud de raphia porte une miette de gâteau.",
    ],
    (1, 3, 3): [
        "narrateur|Nina arrive, le gâteau lisse.",
        "enfant-f|Plus tard, j'avais dit.",
        "enfant-m|Ta tomate t'a attendue.",
        "papa|Vous vous retrouvez sur la marche.",
        "maman|Goûtez, avant le soir.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Raphaël souffle sur une graine chaude.",
        "enfant-m|Elle t'attendait, Nina.",
        "narrateur|La marche garde un jus rouge, petit.",
        "narrateur|Le nœud de raphia attend sur la marche, sans bouger.",
    ],
    (2, 1, 1): [
        "narrateur|Ils rentrent les tomates, chaudes.",
        "enfant-f|Mon caillou est propre, maintenant.",
        "enfant-m|Toi aussi, tu es venue.",
        "papa|La salade attend sur la marche.",
        "maman|Le pain a une croûte.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "enfant-m|J'ai presque secoué le chapeau.",
        "narrateur|Nina pose le caillou près du sel.",
        "enfant-m|C'est notre salade, maintenant.",
        "narrateur|La paille sèche près du nœud luisant.",
    ],
    (2, 1, 2): [
        "narrateur|Le caillou blanc veille sous la paille.",
        "enfant-m|Tu as dit oui, avec lui.",
        "enfant-f|Il a tout vu, du chapeau.",
        "papa|Vous avez cueilli sans tirer.",
        "maman|Goûtez un peu, avant le soir.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina croque, le jus lui rougit le menton.",
        "enfant-m|Reste autant que tu veux.",
        "narrateur|Le sel brille sur la marche.",
        "narrateur|Le chapeau de paille abrite le caillou blanc.",
    ],
    (2, 1, 3): [
        "narrateur|Après l'eau, ils glissent entre les plants.",
        "enfant-f|On a lavé ensemble, d'abord.",
        "enfant-m|Puis tu as dit : on y va.",
        "maman|Deux mains mouillées, puis deux tomates.",
        "papa|Le jardin redevient large.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina rit, tout petit.",
        "enfant-m|La salade t'a attendue.",
        "narrateur|L'arrosoir sèche, près du mur.",
        "narrateur|Une goutte tombe du bord de paille.",
    ],
    (2, 2, 1): [
        "narrateur|Après l'eau, le figuier les laisse partir.",
        "enfant-f|J'avais moins chaud, alors j'ai dit oui.",
        "enfant-m|Ta tomate est celle-là.",
        "papa|Vous tenez tous les deux, entre les plants.",
        "maman|Le pain descend jusqu'à la marche.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina souffle sur une graine, légère.",
        "enfant-m|C'est le signal.",
        "narrateur|Une feuille de figue reste au seuil.",
        "narrateur|Le chapeau de paille sent l'eau fraîche.",
    ],
    (2, 2, 2): [
        "narrateur|L'ombre des plants a deux places, maintenant.",
        "enfant-m|La tienne, et la mienne.",
        "enfant-f|C'est la nôtre, Raphaël.",
        "papa|Vous avez changé d'ombre, pas de jeu.",
        "maman|La salade, au milieu, pour deux.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina souffle, puis Raphaël souffle.",
        "enfant-m|On reste un peu.",
        "narrateur|Une tomate garde sa chaleur.",
        "narrateur|L'ombre de paille reste sur les plants.",
    ],
    (2, 2, 3): [
        "narrateur|Plus tard, Nina rejoint la marche.",
        "enfant-f|Ma tomate m'a attendue.",
        "enfant-m|Tu avais dit plus tard.",
        "papa|Le plus tard a eu sa place.",
        "maman|Vous mangez ensemble, d'ici.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina tend une main, vers le sel.",
        "enfant-m|Je te la passe, d'à côté.",
        "narrateur|Le figuier laisse une ombre ronde.",
        "narrateur|Une tomate dort sous le chapeau, au secret.",
    ],
    (2, 3, 1): [
        "narrateur|Le gâteau de sable est fini.",
        "enfant-f|J'ai eu le temps, juste assez.",
        "enfant-m|Merci d'être venue.",
        "papa|Vous avez soufflé une fois, tout bas.",
        "maman|Les tomates sont dans l'assiette, maintenant.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina fait un signe vers le bac.",
        "enfant-m|Le gâteau t'a vue, une minute.",
        "narrateur|Le sable du bac redevient plat.",
        "narrateur|Un grain de sable colle à la paille.",
    ],
    (2, 3, 2): [
        "narrateur|Le gâteau de sable veille près des plants.",
        "enfant-m|Il a voyagé avec nous.",
        "enfant-f|Sans se casser.",
        "papa|Vous avez mêlé les deux envies.",
        "maman|Le pain sent le four.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina pose un grain de sable, plus loin.",
        "enfant-m|La salade est à nous.",
        "narrateur|Une fourmi croise une graine, puis s'en va.",
        "narrateur|Le chapeau de paille porte une miette de sable.",
    ],
    (2, 3, 3): [
        "narrateur|Nina arrive, le gâteau lisse.",
        "enfant-f|Plus tard, j'avais dit.",
        "enfant-m|Ta tomate t'a attendue.",
        "papa|Vous vous retrouvez sur la marche.",
        "maman|Goûtez, avant le soir.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Raphaël souffle sur une graine chaude.",
        "enfant-m|Elle t'attendait, Nina.",
        "narrateur|La marche garde un jus rouge, petit.",
        "narrateur|Le chapeau de paille sèche sur la marche.",
    ],
    (3, 1, 1): [
        "narrateur|Ils rentrent les tomates, chaudes.",
        "enfant-f|Mon caillou est propre, maintenant.",
        "enfant-m|Toi aussi, tu es venue.",
        "papa|La salade attend sur la marche.",
        "maman|Le pain a une croûte.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "enfant-m|J'ai presque planté le tabouret.",
        "narrateur|Nina pose le caillou près du sel.",
        "enfant-m|C'est notre salade, maintenant.",
        "narrateur|Le petit tabouret garde le nœud à sa hauteur.",
    ],
    (3, 1, 2): [
        "narrateur|Le caillou blanc veille sur le bois.",
        "enfant-m|Tu as dit oui, avec lui.",
        "enfant-f|Il a tout vu, du tabouret.",
        "papa|Vous avez cueilli sans tirer.",
        "maman|Goûtez un peu, avant le soir.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina croque, le jus lui rougit le menton.",
        "enfant-m|Reste autant que tu veux.",
        "narrateur|Le sel brille sur la marche.",
        "narrateur|Le caillou blanc siège sur le tabouret.",
    ],
    (3, 1, 3): [
        "narrateur|Après l'eau, ils glissent entre les plants.",
        "enfant-f|On a lavé ensemble, d'abord.",
        "enfant-m|Puis tu as dit : on y va.",
        "maman|Deux mains mouillées, puis deux tomates.",
        "papa|Le jardin redevient large.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina rit, tout petit.",
        "enfant-m|La salade t'a attendue.",
        "narrateur|L'arrosoir sèche, près du mur.",
        "narrateur|Une tomate mouillée brille sur le bois.",
    ],
    (3, 2, 1): [
        "narrateur|Après l'eau, le figuier les laisse partir.",
        "enfant-f|J'avais moins chaud, alors j'ai dit oui.",
        "enfant-m|Ta tomate est celle-là.",
        "papa|Vous tenez tous les deux, entre les plants.",
        "maman|Le pain descend jusqu'à la marche.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina souffle sur une graine, légère.",
        "enfant-m|C'est le signal.",
        "narrateur|Une feuille de figue reste au seuil.",
        "narrateur|Le petit tabouret sent l'eau du figuier.",
    ],
    (3, 2, 2): [
        "narrateur|L'ombre des plants a deux places, maintenant.",
        "enfant-m|La tienne, et la mienne.",
        "enfant-f|C'est la nôtre, Raphaël.",
        "papa|Vous avez changé d'ombre, pas de jeu.",
        "maman|La salade, au milieu, pour deux.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina souffle, puis Raphaël souffle.",
        "enfant-m|On reste un peu.",
        "narrateur|Une tomate garde sa chaleur.",
        "narrateur|L'ombre des plants couvre le bois du tabouret.",
    ],
    (3, 2, 3): [
        "narrateur|Plus tard, Nina rejoint la marche.",
        "enfant-f|Ma tomate m'a attendue.",
        "enfant-m|Tu avais dit plus tard.",
        "papa|Le plus tard a eu sa place.",
        "maman|Vous mangez ensemble, d'ici.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina tend une main, vers le sel.",
        "enfant-m|Je te la passe, d'à côté.",
        "narrateur|Le figuier laisse une ombre ronde.",
        "narrateur|Une tomate attend, posée sur le tabouret.",
    ],
    (3, 3, 1): [
        "narrateur|Le gâteau de sable est fini.",
        "enfant-f|J'ai eu le temps, juste assez.",
        "enfant-m|Merci d'être venue.",
        "papa|Vous avez soufflé une fois, tout bas.",
        "maman|Les tomates sont dans l'assiette, maintenant.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina fait un signe vers le bac.",
        "enfant-m|Le gâteau t'a vue, une minute.",
        "narrateur|Le sable du bac redevient plat.",
        "narrateur|Un grain de sable reste sous le tabouret.",
    ],
    (3, 3, 2): [
        "narrateur|Le gâteau de sable veille près des plants.",
        "enfant-m|Il a voyagé avec nous.",
        "enfant-f|Sans se casser.",
        "papa|Vous avez mêlé les deux envies.",
        "maman|Le pain sent le four.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Nina pose un grain de sable, plus loin.",
        "enfant-m|La salade est à nous.",
        "narrateur|Une fourmi croise une graine, puis s'en va.",
        "narrateur|Le gâteau de sable veille près du bois.",
    ],
    (3, 3, 3): [
        "narrateur|Nina arrive, le gâteau lisse.",
        "enfant-f|Plus tard, j'avais dit.",
        "enfant-m|Ta tomate t'a attendue.",
        "papa|Vous vous retrouvez sur la marche.",
        "maman|Goûtez, avant le soir.",
        "narrateur|Ça a failli ne pas arriver.",
        "narrateur|Le nœud de raphia tient, d'un cran.",
        "narrateur|Raphaël souffle sur une graine chaude.",
        "enfant-m|Elle t'attendait, Nina.",
        "narrateur|La marche garde un jus rouge, petit.",
        "narrateur|Le petit tabouret reste près du pain, sur la marche.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "grillon,feuilles"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {"fields": t3lab("le panier rouge", "le chapeau de paille", "le petit tabouret")},
    )

    for a in (1, 2, 3):
        t1 = T1[a]
        base = f"CHK_T0001_P000{a}"
        out_chunks[base] = voice(
            by_src[base], t1["passage"], "action", t1["sons"], {"emphasis": t1["emphasis"]}
        )
        out_chunks[f"{base}_Q0001"] = voice(
            by_src[f"{base}_Q0001"],
            t1["question"],
            "clue",
            "",
            {"emphasis": t1["emphasis"], "fields": t1["qfields"]},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], t1["confirm"], "confirm", t1["sons"], {"emphasis": t1["emphasis"]}
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"],
            [
                f"narrateur|{t1['voy']}",
                "narrateur|Nina est dans le jardin, quelque part.",
                "narrateur|Le nœud de raphia frotte le pouce.",
                "narrateur|Le robinet, le figuier, ou le bac.",
                "papa|On l'invite où, Raphaël ?",
            ],
            "choice",
            "",
            {"fields": t3lab("le robinet", "le figuier", "le bac à sable")},
        )
        for b in (1, 2, 3):
            t2 = T2[(a, b)]
            bse = f"{base}_T0002_P000{b}"
            out_chunks[bse] = voice(
                by_src[bse], t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emphasis"]}
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"],
                T3_CHOICE[b],
                "choice",
                "",
                {"fields": t3lab(*T3_LABS[b])},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf],
                    T3[(a, b, c)],
                    "resolution",
                    T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin],
                    ENDINGS[(a, b, c)],
                    "ending",
                    END_SONS[b],
                    {"emphasis": "nœud de raphia"},
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
        "il faut attendre",
        "inviter sans forcer",
        "j'ai compris",
        "mission accomplie",
        "aujourd'hui,",
        "hugo",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "zoé",
        "zoe",
        "lina",
        "iris",
        "capitaine",
        "plic",
        "volet jaune",
        "fil pâle",
        "virgule",
        "marque fine",
        "minuscule symbole",
        "croissant d",
        "étoile brune",
        "ancre minuscule",
        "œillet",
        "oeillet",
        "perle de verre",
        "tout doux",
        "tout calme",
        "maison de bois",
        "miel",
        "merle",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "raphaël" not in blob or "nina" not in blob:
        raise SystemExit(f"{SID}: troupe absente")
    if "nœud de raphia" not in blob:
        raise SystemExit(f"{SID}: indice nœud de raphia absent")

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

    counts = [path_words(out_chunks, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-031 — Le panier rouge de Raphaël dans le potager\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.BES.002 — inviter sans forcer (vécue : proposer, accepter oui / non / plus tard)\n"
        "- **Personnages :** Raphaël, Nina, papa, maman\n"
        "- **Lieu :** potager, robinet, figuier, bac à sable — le rang des tomates\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Raphaël connaît le potager. Un **nœud de raphia** sur le manche du panier rouge "
        "paraît plus sombre. Il veut remplir le panier et le porter jusqu'à la marche, "
        "**avant que papa coupe le pain**. Il tire trop vite : le nœud glisse. Nina ne veut "
        "pas la même chose au même moment. Première idée ratée. Panier, chapeau ou tabouret : "
        "les trois restent. Robinet (caillou), figuier (trop chaud), bac (gâteau). "
        "Attendre, prendre le caillou, laver ; apporter l'eau, changer d'ombre, garder une tomate ; "
        "attendre le gâteau, le déplacer, plus tard. Le nœud du début revient. L'objet porte une trace.\n\n"
        "## Vécu\n\n"
        "Raphaël propose. Nina prend son temps, ou pose sa limite. Deux rythmes, sans voix caricaturale. "
        "Le sourire disparaît ; envie et inquiétude se bousculent. Papa ou maman s'accroupit à la même "
        "hauteur. Personne ne donne la réponse. Raphaël observe l'objet, écoute le potager, retrouve "
        "le nœud de raphia. Il refuse de foncer. La leçon se voit : il invite, il accepte oui, non, "
        "ou une autre heure. Le dénouement a failli ne pas arriver.\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan « Inviter sans forcer » / Hugo / merle / miel / tics jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Monde ≠ TREE-DIF-010 (pas de maison de bois mer) : ici potager, figuier, robinet.\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'obstacle. 9 T2, 27 T3, 27 fins.\n"
        "- Indice unique dès l'ouverture : le nœud de raphia, payé au climax.\n"
        "- Merci vécu (papa : tu l'as rattrapé). Question d'adulte. Un « en ce moment ».\n"
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
