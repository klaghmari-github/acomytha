#!/usr/bin/env python3
"""TREE-DIF-072 — F-NAR-019. Le sac bleu de Sarah, au vestiaire. N2. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-072"
N2 = 15
TITLE = "Le sac bleu de Sarah, au vestiaire"
FIL = (
    "Au vestiaire, Sarah veut fermer son sac bleu à la dernière maille, "
    "avant la cloche, sans qu'on la presse. Un grain de grelot brille au sol. "
    "Elle tire trop vite : le curseur bloque. Elle prend le sac, le goûter "
    "ou le grelot ; les trois viennent. Sous les manteaux ça goutte, près de "
    "la porte ça pousse, au banc du fond c'est trop sombre. Neuf façons de "
    "prendre le temps. Le sac clique. Le grain de grelot rentre."
)
CHARS = "Sarah, papa, maman"
SETTING = "vestiaire de l'école : manteaux, crochets, banc du fond"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain de grelot",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_sac_doit_cliquer_avant_la_cloche; tempo=naturel; sourire=léger; respiration=ample",
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
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_objets_partent_avec_eux; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=trop_vite_le_curseur_bloque; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": "grain de grelot",
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=l_objet_résiste_puis_laisse_une_trace; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "grain de grelot",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=elle_refuse_de_foncer_et_observe; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain de grelot",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_de_grelot_a_payé_l_ouverture; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Derrière la porte vitrée, le vestiaire sent la laine mouillée.",
    "narrateur|Les crochets portent des manteaux lourds, sombres.",
    "narrateur|Une goutte quitte un col rouge, puis tombe.",
    "papa|Ton crochet a un grelot, Sarah.",
    "enfant-f|Il manque un petit grain, papa.",
    "maman|Le carrelage est froid, sous tes chaussures.",
    "narrateur|Un grain de grelot brille près du banc.",
    "narrateur|Sarah connaît ce vestiaire, presque tous ses recoins.",
    "enfant-f|Ici, c'est le passage des crochets.",
    "papa|Tu as vu le grain, Sarah ?",
    "narrateur|En ce moment, Sarah tire le sac bleu, trop vite.",
    "enfant-f|Je veux la dernière maille, avant la cloche.",
    "narrateur|Le curseur bloque, dur, trop haut.",
    "enfant-f|Il ne veut pas fermer !",
    "narrateur|Son sourire part, ça serre dans sa poitrine.",
    "enfant-f|J'ai envie, et ça serre, en même temps.",
    "narrateur|Papa s'accroupit, à la même hauteur.",
    "maman|Regarde le sac, écoute le vestiaire.",
    "maman|Le goûter attend, dans son papier.",
    "papa|Merci, tu as essuyé le crochet.",
]

T1_CHOICE = [
    "narrateur|Près du crochet, trois affaires attendent.",
    "narrateur|Un sac bleu, un goûter, un petit grelot.",
    "maman|Tu prends quoi d'abord, Sarah ?",
]

T1 = {
    1: {
        "lab": "le sac bleu",
        "sons": "fermeture,tissu",
        "emphasis": "sac bleu",
        "passage": [
            "narrateur|Sarah prend d'abord le sac bleu, ouvert.",
            "enfant-f|La dernière maille, elle est à moi.",
            "maman|Garde la fermeture bien droite.",
            "narrateur|Elle tire trop, le curseur tremble, puis bloque.",
            "papa|Prends le goûter, il est à tes pieds.",
            "narrateur|Le grelot glisse sous son autre bras.",
            "narrateur|Les trois partent, collés à Sarah.",
            "narrateur|Rien ne reste au crochet, derrière eux.",
            "enfant-f|Maille, j'arrive.",
            "enfant-f|Je veux cliquer, avant la cloche.",
            "narrateur|Le sac sent la laine mouillée, un peu.",
            "narrateur|Un grain de grelot roule contre sa chaussure.",
            "papa|Le sac d'abord, tu l'as.",
            "enfant-f|Il pèse contre mon ventre.",
            "maman|On avance, tous les trois.",
        ],
        "question": [
            "narrateur|Sarah a pris le sac d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "sac",
            "accepted_examples": "sac | le sac | d'abord le sac | le sac bleu | sac bleu",
            "retry_prompt": "Sarah prend le sac d'abord.",
        },
        "confirm": [
            "narrateur|Le sac reste contre elle, trop ouvert.",
            "enfant-f|On va jusqu'à la maille.",
            "maman|La cloche n'est pas loin.",
            "papa|Tu tiens bien, Sarah ?",
            "enfant-f|Oui, papa.",
            "narrateur|Une maille cherche le curseur, haute.",
            "enfant-f|Je veux qu'il clique.",
            "narrateur|Le grain de grelot suit sa chaussure.",
        ],
        "voy": "Le sac penche vers les crochets, lourd.",
    },
    2: {
        "lab": "le goûter",
        "sons": "papier,pli",
        "emphasis": "goûter",
        "passage": [
            "narrateur|Sarah prend d'abord le goûter, enveloppé.",
            "enfant-f|Il va dans le sac.",
            "papa|Le papier reste fermé, pas trop serré.",
            "narrateur|Elle le pousse trop vite, le pli se tord.",
            "maman|Le sac est là, près du crochet.",
            "narrateur|Papa pose le grelot contre sa manche.",
            "narrateur|Sarah serre les trois contre son ventre.",
            "narrateur|Rien ne reste au crochet, derrière eux.",
            "enfant-f|Goûter, tu restes avec moi.",
            "enfant-f|Je veux le papier dedans, avant la cloche.",
            "narrateur|Le papier colle un peu sa manche.",
            "narrateur|Un grain de grelot tinte contre le papier.",
            "maman|Le goûter d'abord, il est pris.",
            "enfant-f|Il est tiède, dans ma paume.",
            "papa|On avance, tous les trois.",
        ],
        "question": [
            "narrateur|Sarah a pris le goûter d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "goûter",
            "accepted_examples": "goûter | le goûter | d'abord le goûter | le papier | gouter | le gouter",
            "retry_prompt": "Sarah prend le goûter d'abord.",
        },
        "confirm": [
            "narrateur|Le goûter pend au poignet, un peu lâche.",
            "enfant-f|Il va dans le sac.",
            "papa|Ça sent le biscuit, toi.",
            "maman|Tes mains sont prêtes ?",
            "enfant-f|Oui, maman.",
            "narrateur|Le papier se tait, puis plus rien.",
            "enfant-f|Je le glisse, sans le presser.",
            "narrateur|Le grain de grelot roule près du papier.",
        ],
        "voy": "Le goûter colle à sa manche, tiède.",
    },
    3: {
        "lab": "le grelot",
        "sons": "grelot,metal",
        "emphasis": "grelot",
        "passage": [
            "narrateur|Sarah lève d'abord le grelot, tout petit.",
            "enfant-f|Il va sur le sac.",
            "maman|Il tinte vite, tiens-le bien.",
            "narrateur|Elle le secoue trop, le son saute, trop fort.",
            "papa|Voici le sac, et le goûter.",
            "narrateur|Il les glisse contre son genou.",
            "narrateur|Le crochet reste vide, derrière eux.",
            "enfant-f|Grelot, je te porte.",
            "enfant-f|Je veux l'anneau complet, avant la cloche.",
            "narrateur|Un tout petit son reste, puis se tait.",
            "narrateur|Elle refuse de laisser le sac ouvert.",
            "narrateur|Un grain de grelot manque à l'anneau.",
            "papa|Le grelot d'abord, il est à toi.",
            "enfant-f|Il est froid, contre mon pouce.",
            "maman|On avance, tous les trois.",
        ],
        "question": [
            "narrateur|Sarah a pris le grelot d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "grelot",
            "accepted_examples": "grelot | le grelot | d'abord le grelot | le petit grelot",
            "retry_prompt": "Sarah prend le grelot d'abord.",
        },
        "confirm": [
            "narrateur|Le grelot reste froid, contre son pouce.",
            "enfant-f|Il ne tinte plus.",
            "maman|Le métal sent la pluie, un peu.",
            "papa|On avance, tous les trois ?",
            "enfant-f|Oui.",
            "narrateur|L'anneau a un trou, tout petit.",
            "enfant-f|Le grain est au sol.",
            "narrateur|Le grain de grelot attend près du banc.",
        ],
        "voy": "Le grelot appuie contre son pouce, froid.",
    },
}

T2 = {
    (1, 1): {
        "sons": "goutte,manteau",
        "emphasis": "manteaux",
        "passage": [
            "narrateur|Contre son ventre, le sac bleu reste ouvert.",
            "narrateur|Sous les manteaux, une goutte tombe dans son cou.",
            "narrateur|Sarah tire trop vite, le curseur glisse.",
            "enfant-f|Ma maille a fui !",
            "narrateur|Le sac se cache un peu, sous la laine.",
            "narrateur|Son sourire s'en va.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Ici, ça goutte trop.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "narrateur|Personne ne donne la réponse.",
            "maman|Tu vois le grain, Sarah ?",
            "enfant-f|Je ne tire pas, je regarde.",
            "narrateur|Un grain de grelot sort de sous un manteau.",
        ],
    },
    (1, 2): {
        "sons": "vent,porte",
        "emphasis": "porte",
        "passage": [
            "narrateur|Contre son ventre, le sac bleu reste ouvert.",
            "narrateur|Près de la porte, un courant pousse, fort.",
            "narrateur|Sarah tire trop vite, la maille saute.",
            "enfant-f|Ça saute trop !",
            "narrateur|Le sac recule vers le seuil, pris.",
            "narrateur|Son sourire s'en va.",
            "narrateur|Dans sa poitrine, ça se bouscule, trop vite.",
            "papa|Ici, ça souffle trop.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "narrateur|Les adultes attendent, sans parler.",
            "papa|Tu vois le grain, Sarah ?",
            "enfant-f|Je ne fonce pas, je reste.",
            "narrateur|Un grain de grelot tinte vers la porte.",
        ],
    },
    (1, 3): {
        "sons": "bois,ombre",
        "emphasis": "banc du fond",
        "passage": [
            "narrateur|Contre son ventre, le sac bleu reste ouvert.",
            "narrateur|Au banc du fond, l'ombre cache la maille.",
            "narrateur|Sarah cherche trop vite, trop bas.",
            "enfant-f|Je ne vois plus la maille !",
            "narrateur|Le sac glisse sous le bois, disparu.",
            "narrateur|Son sourire s'en va.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Ici, c'est trop sombre.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "narrateur|La suite n'arrive pas toute faite.",
            "maman|Tu vois le grain, Sarah ?",
            "enfant-f|Je ne fonce pas, je cherche.",
            "narrateur|Un grain de grelot luit sous le banc.",
        ],
    },
    (2, 1): {
        "sons": "goutte,papier",
        "emphasis": "manteaux",
        "passage": [
            "narrateur|Dans sa paume, le goûter enveloppé est tiède.",
            "narrateur|Sous les manteaux, une goutte frappe le papier.",
            "narrateur|Sarah le pousse trop vite, le pli se mouille.",
            "enfant-f|Mon papier est mouillé !",
            "narrateur|Le goûter disparaît un peu, sous un col.",
            "narrateur|Son sourire s'en va.",
            "narrateur|Dans sa poitrine, ça serre, trop fort.",
            "papa|Ici, ça goutte trop.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "narrateur|Papa ne dit pas le geste.",
            "maman|Tu vois le grain, Sarah ?",
            "enfant-f|Je ne pousse pas, je regarde.",
            "narrateur|Un grain de grelot colle au papier mouillé.",
        ],
    },
    (2, 2): {
        "sons": "vent,papier",
        "emphasis": "porte",
        "passage": [
            "narrateur|Dans sa paume, le goûter enveloppé est tiède.",
            "narrateur|Près de la porte, l'air soulève le papier.",
            "narrateur|Sarah le serre trop vite, le pli s'envole.",
            "enfant-f|Le papier part !",
            "narrateur|Le goûter file vers le seuil, trop léger.",
            "narrateur|Son sourire s'en va.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Ici, ça souffle trop.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "narrateur|Maman ne dit pas le geste.",
            "papa|Tu vois le grain, Sarah ?",
            "enfant-f|Je ne cours pas, je reste.",
            "narrateur|Un grain de grelot roule vers le seuil.",
        ],
    },
    (2, 3): {
        "sons": "bois,papier",
        "emphasis": "banc du fond",
        "passage": [
            "narrateur|Dans sa paume, le goûter enveloppé est tiède.",
            "narrateur|Au banc du fond, l'ombre mange le papier.",
            "narrateur|Sarah le pose trop vite, trop bas.",
            "enfant-f|Je ne vois plus le pli !",
            "narrateur|Le goûter se perd sous le bois, disparu.",
            "narrateur|Son sourire s'en va.",
            "narrateur|Dans sa poitrine, ça se bouscule, trop fort.",
            "papa|Ici, c'est trop sombre.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "narrateur|Personne n'explique la suite.",
            "maman|Tu vois le grain, Sarah ?",
            "enfant-f|Je ne fonce pas, je cherche.",
            "narrateur|Un grain de grelot luit sous le papier.",
        ],
    },
    (3, 1): {
        "sons": "goutte,metal",
        "emphasis": "manteaux",
        "passage": [
            "narrateur|Entre ses doigts, le petit grelot est froid.",
            "narrateur|Sous les manteaux, une goutte frappe le métal.",
            "narrateur|Sarah le secoue trop vite, le son saute.",
            "enfant-f|Il tinte trop fort !",
            "narrateur|Le grelot glisse sous un manteau, perdu.",
            "narrateur|Son sourire s'en va.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Ici, ça goutte trop.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "narrateur|Les regards attendent, sans mot.",
            "maman|Tu vois le grain, Sarah ?",
            "enfant-f|Je ne secoue pas, je regarde.",
            "narrateur|Un grain de grelot sort de sous la laine.",
        ],
    },
    (3, 2): {
        "sons": "vent,grelot",
        "emphasis": "porte",
        "passage": [
            "narrateur|Entre ses doigts, le petit grelot est froid.",
            "narrateur|Près de la porte, l'air fait tinter le métal.",
            "narrateur|Sarah le lève trop vite, le son s'envole.",
            "enfant-f|Le bruit part trop loin !",
            "narrateur|Le grelot penche vers le seuil, pris.",
            "narrateur|Son sourire s'en va.",
            "narrateur|Dans sa poitrine, ça se bouscule, trop vite.",
            "papa|Ici, ça souffle trop.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "narrateur|Le vestiaire se tait, trop.",
            "papa|Tu vois le grain, Sarah ?",
            "enfant-f|Je ne fonce pas, je reste.",
            "narrateur|Un grain de grelot tinte vers le battant.",
        ],
    },
    (3, 3): {
        "sons": "bois,silence",
        "emphasis": "banc du fond",
        "passage": [
            "narrateur|Entre ses doigts, le petit grelot est froid.",
            "narrateur|Au banc du fond, le métal se tait, trop sombre.",
            "narrateur|Sarah cherche trop vite, trop bas.",
            "enfant-f|Je n'entends plus le grelot !",
            "narrateur|Le grelot roule sous le bois, disparu.",
            "narrateur|Son sourire s'en va.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Ici, c'est trop sombre.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "narrateur|La réponse reste dans l'air, muette.",
            "maman|Tu vois le grain, Sarah ?",
            "enfant-f|Je ne fonce pas, je cherche.",
            "narrateur|Un grain de grelot luit sous une latte.",
        ],
    },
}

T3_LABS = {
    1: ("poser le sac", "compter", "recommencer"),
    2: ("plus loin", "les mailles", "un instant"),
    3: ("la lumière", "les genoux", "tout doux"),
}

T3_CHOICE = {
    1: [
        "narrateur|Les manteaux n'ont pas fini de goutter.",
        "papa|Poser le sac, compter, ou recommencer ?",
    ],
    2: [
        "narrateur|La porte n'a pas fini de pousser.",
        "maman|Plus loin, les mailles, ou un instant ?",
    ],
    3: [
        "narrateur|Le banc n'a pas fini d'être sombre.",
        "papa|La lumière, les genoux, ou sans forcer ?",
    ],
}

T3_SONS = {
    (1, 1): "sac,carrelage",
    (1, 2): "compte,goutte",
    (1, 3): "fermeture,bas",
    (2, 1): "pas,porte",
    (2, 2): "mailles,fermeture",
    (2, 3): "souffle,silence",
    (3, 1): "verre,lumiere",
    (3, 2): "genoux,bois",
    (3, 3): "fermeture,lent",
}

T3_EMPH = {
    1: {1: "carrelage sec", 2: "gouttes", 3: "première maille"},
    2: {1: "plus loin", 2: "mailles", 3: "un instant"},
    3: {1: "lumière", 2: "genoux", 3: "sans forcer"},
}

T3 = {
    (1, 1, 1): [
        "enfant-f|Je pose le sac, au sec.",
        "narrateur|Sarah pose le sac sur le carrelage sec.",
        "narrateur|Un grain de grelot brille au bord, minuscule.",
        "enfant-f|Toi, tu restes hors des gouttes.",
        "narrateur|Elle ne fonce pas, elle observe le grain.",
        "narrateur|La fermeture avance, maille après maille.",
        "papa|Tu as posé ça, hors de l'eau.",
        "enfant-f|La dernière maille, je la tiens.",
        "maman|Le sac a trouvé le carrelage sec.",
        "narrateur|Le curseur clique, tout en haut.",
    ],
    (1, 1, 2): [
        "enfant-f|Je compte les gouttes, d'abord.",
        "narrateur|Sarah tient le sac, et compte tout bas.",
        "narrateur|Une goutte, deux gouttes, puis plus.",
        "enfant-f|Maintenant, tu peux fermer.",
        "narrateur|Un grain de grelot s'arrête au bord.",
        "narrateur|Elle ne tire pas, elle glisse le curseur.",
        "papa|Tu as compté, sans te presser.",
        "enfant-f|Les gouttes m'ont laissée faire.",
        "maman|Le sac attendait le silence.",
        "narrateur|La fermeture glisse, droite, jusqu'en haut.",
    ],
    (1, 1, 3): [
        "enfant-f|Je recommence, depuis le bas.",
        "narrateur|Sarah ramène le curseur, tout en bas.",
        "narrateur|Un grain de grelot montre la maille du bas.",
        "enfant-f|Cette fois, je ne tire pas.",
        "narrateur|Elle reprend la maille du bas, sans forcer.",
        "narrateur|La fermeture monte, dent après dent.",
        "papa|Tu as repris depuis le début.",
        "enfant-f|Cette fois, tu tiens.",
        "maman|Le sac a retrouvé sa maille.",
        "narrateur|La dernière maille reçoit le curseur, nette.",
    ],
    (1, 2, 1): [
        "enfant-f|On va plus loin, loin du courant.",
        "narrateur|Sarah recule d'un pas, le sac contre elle.",
        "narrateur|Un grain de grelot reste au seuil, puis se tait.",
        "enfant-f|Ici, l'air ne pousse plus.",
        "narrateur|Elle refuse de foncer, elle observe le grain.",
        "narrateur|La fermeture avance, hors du souffle.",
        "papa|Tu t'es mise plus loin, hors du vent.",
        "enfant-f|La maille ne saute plus.",
        "maman|Le sac a trouvé un coin calme.",
        "narrateur|Le curseur clique, loin de la porte.",
    ],
    (1, 2, 2): [
        "enfant-f|Je regarde les mailles, une par une.",
        "narrateur|Sarah suit chaque dent bleue, sans tirer.",
        "narrateur|Un grain de grelot se loge entre deux mailles.",
        "enfant-f|Celle-là, puis la suivante.",
        "narrateur|Elle ne fonce pas, elle compte les dents.",
        "narrateur|La fermeture monte, maille après maille.",
        "papa|Tu as regardé chaque maille.",
        "enfant-f|Le courant n'a plus la fermeture.",
        "maman|Les mailles ont guidé tes doigts.",
        "narrateur|Le sac se ferme, dent après dent.",
    ],
    (1, 2, 3): [
        "enfant-f|J'attends un instant, que ça passe.",
        "narrateur|Sarah reste, le sac contre son ventre.",
        "narrateur|Un grain de grelot se tait, loin du courant.",
        "enfant-f|L'air est parti, je glisse.",
        "narrateur|Elle refuse de foncer, elle écoute la porte.",
        "narrateur|La fermeture avance, le battant se tait.",
        "papa|Tu as laissé passer le souffle.",
        "enfant-f|Un instant, et ça tenait.",
        "maman|Le sac a attendu avec toi.",
        "narrateur|Le curseur clique, la porte close.",
    ],
    (1, 3, 1): [
        "enfant-f|J'apporte le sac vers la lumière.",
        "narrateur|Sarah tourne le sac vers le verre de la porte.",
        "narrateur|Un grain de grelot luit dans le rectangle clair.",
        "enfant-f|La maille, je la vois.",
        "narrateur|Elle ne fonce pas, elle suit le grain.",
        "narrateur|La fermeture avance dans le carré de verre.",
        "papa|Tu as cherché la lumière, pas l'ombre.",
        "enfant-f|Le banc n'a plus caché la maille.",
        "maman|Le verre a montré le curseur.",
        "narrateur|Le sac se ferme, net, dans la clarté.",
    ],
    (1, 3, 2): [
        "enfant-f|Je m'agenouille, près du banc.",
        "narrateur|Sarah pose les genoux sur le carrelage froid.",
        "narrateur|Un grain de grelot repose près de ses genoux.",
        "enfant-f|D'ici, je vois la maille.",
        "narrateur|Elle ne fonce pas, elle observe le grain.",
        "narrateur|La fermeture avance, à hauteur de ses yeux.",
        "papa|Tes genoux t'ont rapprochée.",
        "enfant-f|Le bois n'a plus mangé le sac.",
        "maman|À genoux, la maille est revenue.",
        "narrateur|Le curseur clique, près du bois.",
    ],
    (1, 3, 3): [
        "enfant-f|Je glisse sans forcer, tout petit.",
        "narrateur|Sarah pose deux doigts sur le curseur, lents.",
        "narrateur|Un grain de grelot dort dans sa paume.",
        "enfant-f|Sans tirer, tu vas.",
        "narrateur|Elle refuse de foncer, elle sent chaque dent.",
        "narrateur|La fermeture monte, sans un saut.",
        "papa|Tu as glissé, sans forcer.",
        "enfant-f|Le sac a dit oui.",
        "maman|Tes doigts ont trouvé le rythme.",
        "narrateur|Le curseur clique, sac fermé contre elle.",
    ],
    (2, 1, 1): [
        "enfant-f|Je pose le sac, le goûter au sec.",
        "narrateur|Sarah pose le sac, le papier hors des gouttes.",
        "narrateur|Un grain de grelot colle au papier, sec.",
        "enfant-f|Toi, tu restes hors de l'eau.",
        "narrateur|Elle ne pousse pas, elle observe le grain.",
        "narrateur|Le goûter rentre, puis la fermeture avance.",
        "papa|Tu as posé le papier, hors des gouttes.",
        "enfant-f|Le pli n'a plus d'eau.",
        "maman|Le goûter a trouvé le carrelage sec.",
        "narrateur|Le sac clique, le biscuit au chaud.",
    ],
    (2, 1, 2): [
        "enfant-f|Je compte les gouttes, le papier contre moi.",
        "narrateur|Sarah tient le goûter, et compte tout bas.",
        "narrateur|Une goutte, deux gouttes, puis plus.",
        "enfant-f|Maintenant, tu rentres.",
        "narrateur|Un grain de grelot s'arrête au bord du papier.",
        "narrateur|Elle ne pousse pas, elle glisse le goûter.",
        "papa|Tu as compté, sans te presser.",
        "enfant-f|Les gouttes m'ont laissée faire.",
        "maman|Le papier a attendu le silence.",
        "narrateur|Le sac se ferme, goûter au sec.",
    ],
    (2, 1, 3): [
        "enfant-f|Je recommence, le papier d'abord.",
        "narrateur|Sarah sort le goûter, essuie le pli.",
        "narrateur|Un grain de grelot montre le bord du papier.",
        "enfant-f|Cette fois, je ne pousse pas.",
        "narrateur|Elle reprend depuis le bas, sans forcer.",
        "narrateur|Le goûter rentre, la fermeture monte.",
        "papa|Tu as repris depuis le début.",
        "enfant-f|Cette fois, tu tiens, papier.",
        "maman|Le sac a retrouvé le goûter.",
        "narrateur|La dernière maille reçoit le curseur, sèche.",
    ],
    (2, 2, 1): [
        "enfant-f|On va plus loin, le papier contre moi.",
        "narrateur|Sarah recule d'un pas, le goûter serré.",
        "narrateur|Un grain de grelot reste au seuil, loin du vent.",
        "enfant-f|Ici, l'air ne soulève plus.",
        "narrateur|Elle refuse de foncer, elle observe le grain.",
        "narrateur|Le goûter rentre, hors du souffle.",
        "papa|Tu t'es mise plus loin, hors du vent.",
        "enfant-f|Le pli ne s'envole plus.",
        "maman|Le papier a trouvé un coin calme.",
        "narrateur|Le sac clique, loin de la porte.",
    ],
    (2, 2, 2): [
        "enfant-f|Je regarde les mailles, le goûter dedans.",
        "narrateur|Sarah suit chaque dent, le papier à sa place.",
        "narrateur|Un grain de grelot se loge entre deux mailles.",
        "enfant-f|Celle-là, puis la suivante.",
        "narrateur|Elle ne fonce pas, elle compte les dents.",
        "narrateur|La fermeture monte, le goûter reste.",
        "papa|Tu as regardé chaque maille.",
        "enfant-f|Le courant n'a plus le papier.",
        "maman|Les mailles ont gardé le goûter.",
        "narrateur|Le sac se ferme, dent après dent.",
    ],
    (2, 2, 3): [
        "enfant-f|J'attends un instant, le papier contre moi.",
        "narrateur|Sarah reste, le goûter contre son ventre.",
        "narrateur|Un grain de grelot se tait, loin du courant.",
        "enfant-f|L'air est parti, je glisse.",
        "narrateur|Elle refuse de foncer, elle écoute la porte.",
        "narrateur|Le goûter rentre, le battant se tait.",
        "papa|Tu as laissé passer le souffle.",
        "enfant-f|Un instant, et le pli tenait.",
        "maman|Le papier a attendu avec toi.",
        "narrateur|Le curseur clique, goûter au chaud.",
    ],
    (2, 3, 1): [
        "enfant-f|J'apporte le goûter vers la lumière.",
        "narrateur|Sarah tourne le papier vers le verre de la porte.",
        "narrateur|Un grain de grelot luit sur le papier, clair.",
        "enfant-f|Le pli, je le vois.",
        "narrateur|Elle ne fonce pas, elle suit le grain.",
        "narrateur|Le goûter rentre dans le carré de verre.",
        "papa|Tu as cherché la lumière, pas l'ombre.",
        "enfant-f|Le banc n'a plus mangé le papier.",
        "maman|Le verre a montré le pli.",
        "narrateur|Le sac se ferme, goûter dans la clarté.",
    ],
    (2, 3, 2): [
        "enfant-f|Je m'agenouille, le goûter près du banc.",
        "narrateur|Sarah pose les genoux, le papier à hauteur d'œil.",
        "narrateur|Un grain de grelot glisse vers ses genoux, tiède.",
        "enfant-f|D'ici, je vois le pli.",
        "narrateur|Elle ne fonce pas, elle observe le grain.",
        "narrateur|Le goûter rentre, à hauteur de ses yeux.",
        "papa|Tes genoux t'ont rapprochée.",
        "enfant-f|Le bois n'a plus mangé le papier.",
        "maman|À genoux, le pli est revenu.",
        "narrateur|Le curseur clique, près du bois.",
    ],
    (2, 3, 3): [
        "enfant-f|Je glisse sans forcer, le goûter d'abord.",
        "narrateur|Sarah pose deux doigts sur le papier, lents.",
        "narrateur|Un grain de grelot se cache dans le pli.",
        "enfant-f|Sans tirer, tu rentres.",
        "narrateur|Elle refuse de foncer, elle sent le papier.",
        "narrateur|Le goûter rentre, la fermeture monte.",
        "papa|Tu as glissé, sans forcer.",
        "enfant-f|Le papier a dit oui.",
        "maman|Tes doigts ont trouvé le rythme.",
        "narrateur|Le curseur clique, goûter au chaud.",
    ],
    (3, 1, 1): [
        "enfant-f|Je pose le sac, le grelot au sec.",
        "narrateur|Sarah pose le sac, le métal hors des gouttes.",
        "narrateur|Un grain de grelot sèche contre le métal, au sol.",
        "enfant-f|Toi, tu restes hors de l'eau.",
        "narrateur|Elle ne secoue pas, elle observe le grain.",
        "narrateur|Le grelot rentre, puis la fermeture avance.",
        "papa|Tu as posé le métal, hors des gouttes.",
        "enfant-f|Le son n'a plus d'eau.",
        "maman|Le grelot a trouvé le carrelage sec.",
        "narrateur|Le sac clique, le grelot muet.",
    ],
    (3, 1, 2): [
        "enfant-f|Je compte les gouttes, le grelot dans ma main.",
        "narrateur|Sarah tient le grelot, et compte tout bas.",
        "narrateur|Une goutte, deux gouttes, puis plus.",
        "enfant-f|Maintenant, tu te tais.",
        "narrateur|Un grain de grelot tinte une fois, puis plus.",
        "narrateur|Elle ne secoue pas, elle glisse le métal.",
        "papa|Tu as compté, sans te presser.",
        "enfant-f|Les gouttes m'ont laissée faire.",
        "maman|Le grelot a attendu le silence.",
        "narrateur|Le sac se ferme, grelot au chaud.",
    ],
    (3, 1, 3): [
        "enfant-f|Je recommence, le grelot d'abord.",
        "narrateur|Sarah essuie le métal, ramène le curseur.",
        "narrateur|Un grain de grelot rentre dans l'anneau, un clic.",
        "enfant-f|Cette fois, je ne secoue pas.",
        "narrateur|Elle reprend depuis le bas, sans forcer.",
        "narrateur|Le grelot tient, la fermeture monte.",
        "papa|Tu as repris depuis le début.",
        "enfant-f|Cette fois, tu tiens, grelot.",
        "maman|Le sac a retrouvé le métal.",
        "narrateur|La dernière maille reçoit le curseur, muette.",
    ],
    (3, 2, 1): [
        "enfant-f|On va plus loin, le grelot contre moi.",
        "narrateur|Sarah recule d'un pas, le métal serré.",
        "narrateur|Un grain de grelot reste au seuil, sans tinter.",
        "enfant-f|Ici, l'air ne fait plus de bruit.",
        "narrateur|Elle refuse de foncer, elle observe le grain.",
        "narrateur|Le grelot rentre, hors du souffle.",
        "papa|Tu t'es mise plus loin, hors du vent.",
        "enfant-f|Le son ne s'envole plus.",
        "maman|Le métal a trouvé un coin calme.",
        "narrateur|Le sac clique, loin de la porte.",
    ],
    (3, 2, 2): [
        "enfant-f|Je regarde les mailles, le grelot au bord.",
        "narrateur|Sarah suit chaque dent, le métal à sa place.",
        "narrateur|Un grain de grelot se glisse entre deux mailles.",
        "enfant-f|Celle-là, puis la suivante.",
        "narrateur|Elle ne fonce pas, elle compte les dents.",
        "narrateur|La fermeture monte, le grelot reste.",
        "papa|Tu as regardé chaque maille.",
        "enfant-f|Le courant n'a plus le métal.",
        "maman|Les mailles ont gardé le grelot.",
        "narrateur|Le sac se ferme, dent après dent.",
    ],
    (3, 2, 3): [
        "enfant-f|J'attends un instant, le grelot dans ma main.",
        "narrateur|Sarah reste, le métal contre son ventre.",
        "narrateur|Un grain de grelot se tait, grelot contre le sac.",
        "enfant-f|L'air est parti, je glisse.",
        "narrateur|Elle refuse de foncer, elle écoute la porte.",
        "narrateur|Le grelot rentre, le battant se tait.",
        "papa|Tu as laissé passer le souffle.",
        "enfant-f|Un instant, et le son tenait.",
        "maman|Le métal a attendu avec toi.",
        "narrateur|Le curseur clique, grelot au chaud.",
    ],
    (3, 3, 1): [
        "enfant-f|J'apporte le grelot vers la lumière.",
        "narrateur|Sarah tourne le métal vers le verre de la porte.",
        "narrateur|Un grain de grelot luit sous une latte du banc.",
        "enfant-f|L'anneau, je le vois.",
        "narrateur|Elle ne fonce pas, elle suit le grain.",
        "narrateur|Le grelot rentre dans le carré de verre.",
        "papa|Tu as cherché la lumière, pas l'ombre.",
        "enfant-f|Le banc n'a plus caché le métal.",
        "maman|Le verre a montré l'anneau.",
        "narrateur|Le sac se ferme, grelot dans la clarté.",
    ],
    (3, 3, 2): [
        "enfant-f|Je m'agenouille, le grelot près du banc.",
        "narrateur|Sarah pose les genoux, le métal à hauteur d'œil.",
        "narrateur|Un grain de grelot roule jusqu'à ses genoux, froid.",
        "enfant-f|D'ici, je vois l'anneau.",
        "narrateur|Elle ne fonce pas, elle observe le grain.",
        "narrateur|Le grelot rentre, à hauteur de ses yeux.",
        "papa|Tes genoux t'ont rapprochée.",
        "enfant-f|Le bois n'a plus mangé le métal.",
        "maman|À genoux, l'anneau est revenu.",
        "narrateur|Le curseur clique, près du bois.",
    ],
    (3, 3, 3): [
        "enfant-f|Je glisse sans forcer, le grelot d'abord.",
        "narrateur|Sarah pose deux doigts sur le métal, lents.",
        "narrateur|Un grain de grelot rentre dans sa poche, muet.",
        "enfant-f|Sans tirer, tu rentres.",
        "narrateur|Elle refuse de foncer, elle sent l'anneau.",
        "narrateur|Le grelot rentre, la fermeture monte.",
        "papa|Tu as glissé, sans forcer.",
        "enfant-f|Le métal a dit oui.",
        "maman|Tes doigts ont trouvé le rythme.",
        "narrateur|Le curseur clique, grelot au chaud.",
    ],
}

END_SONS = {1: "manteau,fermeture", 2: "porte,fermeture", 3: "banc,fermeture"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Le sac bleu tient, fermé, hors des manteaux.",
        "enfant-f|Tu as posé, j'ai glissé.",
        "papa|Tes mains ont trouvé le carrelage sec.",
        "maman|On rentre, la cloche n'a pas sonné.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|La fermeture garde une dent un peu luisante.",
        "narrateur|Le grain de grelot sèche sur le carrelage, hors des manteaux.",
    ],
    (1, 1, 2): [
        "narrateur|Après le compte, le sac bleu tient, fermé.",
        "enfant-f|Tu as compté, j'ai glissé.",
        "papa|Les gouttes t'ont laissée faire.",
        "maman|On rentre, ça sent la laine mouillée.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|La fermeture garde une dent un peu luisante.",
        "narrateur|Le grain de grelot reste au bord d'une goutte arrêtée.",
    ],
    (1, 1, 3): [
        "narrateur|Depuis le bas, le sac bleu tient, fermé.",
        "enfant-f|Tu as repris, j'ai glissé.",
        "papa|Tu as repris depuis le début.",
        "maman|On rentre, le crochet est essuyé.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|La fermeture garde une dent un peu luisante.",
        "narrateur|Le grain de grelot tient à la maille du bas, minuscule.",
    ],
    (1, 2, 1): [
        "narrateur|Plus loin, le sac bleu tient, fermé, hors du vent.",
        "enfant-f|Je me suis mise plus loin.",
        "papa|Tu t'es mise hors du souffle.",
        "maman|On rentre, le seuil est sec.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|La fermeture garde une dent un peu luisante.",
        "narrateur|Le grain de grelot reste collé au seuil, loin du vent.",
    ],
    (1, 2, 2): [
        "narrateur|Maille après maille, le sac bleu tient, fermé.",
        "enfant-f|J'ai regardé chaque dent.",
        "papa|Tu as regardé chaque maille.",
        "maman|On rentre, la porte se tait.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|La fermeture garde une dent un peu luisante.",
        "narrateur|Le grain de grelot se loge entre deux dents bleues.",
    ],
    (1, 2, 3): [
        "narrateur|Après un instant, le sac bleu tient, fermé.",
        "enfant-f|J'ai laissé passer l'air.",
        "papa|Tu as laissé passer le souffle.",
        "maman|On rentre, le battant reste clos.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|La fermeture garde une dent un peu luisante.",
        "narrateur|Le grain de grelot se tait, la porte close derrière.",
    ],
    (1, 3, 1): [
        "narrateur|Dans le verre, le sac bleu tient, fermé, clair.",
        "enfant-f|La lumière a montré la maille.",
        "papa|Tu as cherché le carré de verre.",
        "maman|On rentre, le banc redevient un banc.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|La fermeture garde une dent un peu luisante.",
        "narrateur|Le grain de grelot luit dans le carré de verre, net.",
    ],
    (1, 3, 2): [
        "narrateur|À genoux, le sac bleu tient, fermé, près du bois.",
        "enfant-f|Mes genoux ont vu la maille.",
        "papa|Tes genoux t'ont rapprochée.",
        "maman|On rentre, le carrelage reste froid.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|La fermeture garde une dent un peu luisante.",
        "narrateur|Le grain de grelot repose sur le bois, près des genoux.",
    ],
    (1, 3, 3): [
        "narrateur|Sans forcer, le sac bleu tient, fermé, contre elle.",
        "enfant-f|Mes doigts ont glissé, lents.",
        "papa|Tu as glissé, sans forcer.",
        "maman|On rentre, le vestiaire se tait.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|La fermeture garde une dent un peu luisante.",
        "narrateur|Le grain de grelot dort dans sa paume, sac fermé.",
    ],
    (2, 1, 1): [
        "narrateur|Le goûter rentre, le sac bleu tient, hors des manteaux.",
        "enfant-f|Tu as posé, j'ai glissé le papier.",
        "papa|Tes mains ont mis le papier au sec.",
        "maman|On rentre, ça sent le biscuit.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|Le papier du goûter garde un pli tiède.",
        "narrateur|Le grain de grelot colle au papier du goûter, sec.",
    ],
    (2, 1, 2): [
        "narrateur|Après le compte, le goûter rentre, le sac tient.",
        "enfant-f|Tu as compté, j'ai glissé le papier.",
        "papa|Les gouttes t'ont laissée faire.",
        "maman|On rentre, ça sent la laine et le biscuit.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|Le papier du goûter garde un pli tiède.",
        "narrateur|Le grain de grelot s'arrête au bord du papier, muet.",
    ],
    (2, 1, 3): [
        "narrateur|Depuis le bas, le goûter rentre, le sac tient.",
        "enfant-f|Tu as repris, j'ai glissé le papier.",
        "papa|Tu as repris depuis le début.",
        "maman|On rentre, le crochet est essuyé.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|Le papier du goûter garde un pli tiède.",
        "narrateur|Le grain de grelot retrouve l'anneau, goûter dedans.",
    ],
    (2, 2, 1): [
        "narrateur|Plus loin, le goûter rentre, hors du vent.",
        "enfant-f|Je me suis mise plus loin.",
        "papa|Tu t'es mise hors du souffle.",
        "maman|On rentre, le seuil est sec.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|Le papier du goûter garde un pli tiède.",
        "narrateur|Le grain de grelot reste au pli, loin de la porte.",
    ],
    (2, 2, 2): [
        "narrateur|Maille après maille, le goûter rentre, le sac tient.",
        "enfant-f|J'ai regardé chaque dent.",
        "papa|Tu as regardé chaque maille.",
        "maman|On rentre, la porte se tait.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|Le papier du goûter garde un pli tiède.",
        "narrateur|Le grain de grelot brille entre deux mailles du sac.",
    ],
    (2, 2, 3): [
        "narrateur|Après un instant, le goûter rentre, le sac tient.",
        "enfant-f|J'ai laissé passer l'air.",
        "papa|Tu as laissé passer le souffle.",
        "maman|On rentre, le battant reste clos.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|Le papier du goûter garde un pli tiède.",
        "narrateur|Le grain de grelot attend, le papier contre elle.",
    ],
    (2, 3, 1): [
        "narrateur|Dans le verre, le goûter rentre, le sac tient.",
        "enfant-f|La lumière a montré le pli.",
        "papa|Tu as cherché le carré de verre.",
        "maman|On rentre, le banc redevient un banc.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|Le papier du goûter garde un pli tiède.",
        "narrateur|Le grain de grelot luit sur le papier, au verre.",
    ],
    (2, 3, 2): [
        "narrateur|À genoux, le goûter rentre, près du bois.",
        "enfant-f|Mes genoux ont vu le pli.",
        "papa|Tes genoux t'ont rapprochée.",
        "maman|On rentre, le carrelage reste froid.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|Le papier du goûter garde un pli tiède.",
        "narrateur|Le grain de grelot glisse vers ses genoux, tiède.",
    ],
    (2, 3, 3): [
        "narrateur|Sans forcer, le goûter rentre, le sac tient.",
        "enfant-f|Mes doigts ont glissé, lents.",
        "papa|Tu as glissé, sans forcer.",
        "maman|On rentre, le vestiaire se tait.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|Le papier du goûter garde un pli tiède.",
        "narrateur|Le grain de grelot se cache dans le pli du goûter.",
    ],
    (3, 1, 1): [
        "narrateur|Le grelot rentre, le sac bleu tient, hors des manteaux.",
        "enfant-f|Tu as posé, j'ai glissé le métal.",
        "papa|Tes mains ont mis le métal au sec.",
        "maman|On rentre, le grelot se tait.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|L'anneau du grelot reste froid, complet.",
        "narrateur|Le grain de grelot sèche contre le métal, au sol.",
    ],
    (3, 1, 2): [
        "narrateur|Après le compte, le grelot rentre, le sac tient.",
        "enfant-f|Tu as compté, j'ai glissé le métal.",
        "papa|Les gouttes t'ont laissée faire.",
        "maman|On rentre, ça sent la laine et le métal.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|L'anneau du grelot reste froid, complet.",
        "narrateur|Le grain de grelot tinte une seule fois, puis plus.",
    ],
    (3, 1, 3): [
        "narrateur|Depuis le bas, le grelot rentre, le sac tient.",
        "enfant-f|Tu as repris, j'ai glissé le métal.",
        "papa|Tu as repris depuis le début.",
        "maman|On rentre, le crochet est essuyé.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|L'anneau du grelot reste froid, complet.",
        "narrateur|Le grain de grelot rentre dans l'anneau, un clic.",
    ],
    (3, 2, 1): [
        "narrateur|Plus loin, le grelot rentre, hors du vent.",
        "enfant-f|Je me suis mise plus loin.",
        "papa|Tu t'es mise hors du souffle.",
        "maman|On rentre, le seuil est sec.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|L'anneau du grelot reste froid, complet.",
        "narrateur|Le grain de grelot reste au seuil, sans tinter.",
    ],
    (3, 2, 2): [
        "narrateur|Maille après maille, le grelot rentre, le sac tient.",
        "enfant-f|J'ai regardé chaque dent.",
        "papa|Tu as regardé chaque maille.",
        "maman|On rentre, la porte se tait.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|L'anneau du grelot reste froid, complet.",
        "narrateur|Le grain de grelot se glisse entre deux mailles.",
    ],
    (3, 2, 3): [
        "narrateur|Après un instant, le grelot rentre, le sac tient.",
        "enfant-f|J'ai laissé passer l'air.",
        "papa|Tu as laissé passer le souffle.",
        "maman|On rentre, le battant reste clos.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|L'anneau du grelot reste froid, complet.",
        "narrateur|Le grain de grelot se tait, grelot contre le sac.",
    ],
    (3, 3, 1): [
        "narrateur|Dans le verre, le grelot rentre, le sac tient.",
        "enfant-f|La lumière a montré l'anneau.",
        "papa|Tu as cherché le carré de verre.",
        "maman|On rentre, le banc redevient un banc.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|L'anneau du grelot reste froid, complet.",
        "narrateur|Le grain de grelot luit sous une latte du banc.",
    ],
    (3, 3, 2): [
        "narrateur|À genoux, le grelot rentre, près du bois.",
        "enfant-f|Mes genoux ont vu l'anneau.",
        "papa|Tes genoux t'ont rapprochée.",
        "maman|On rentre, le carrelage reste froid.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|L'anneau du grelot reste froid, complet.",
        "narrateur|Le grain de grelot roule jusqu'à ses genoux, froid.",
    ],
    (3, 3, 3): [
        "narrateur|Sans forcer, le grelot rentre, le sac tient.",
        "enfant-f|Mes doigts ont glissé, lents.",
        "papa|Tu as glissé, sans forcer.",
        "maman|On rentre, le vestiaire se tait.",
        "enfant-f|Le moment difficile, je le garde.",
        "narrateur|L'anneau du grelot reste froid, complet.",
        "narrateur|Le grain de grelot rentre dans sa poche, muet.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "goutte,grelot"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {"fields": t3lab("le sac bleu", "le goûter", "le grelot")},
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
                "narrateur|Sous les manteaux, les gouttes tombent, froides.",
                "narrateur|Près de la porte, l'air pousse trop.",
                "narrateur|Au banc du fond, c'est trop sombre.",
                "papa|Sarah, tu vas où ?",
            ],
            "choice",
            "",
            {"fields": t3lab("sous les manteaux", "près de la porte", "le banc du fond")},
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
                    {"emphasis": T3_EMPH[b][c]},
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
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "grain de grelot" not in blob:
        raise SystemExit(f"{SID}: grain de grelot absent")
    if "vestiaire" not in blob:
        raise SystemExit(f"{SID}: vestiaire absent")
    for kid in ("enfant-m|", "victorino", "nina", "mila", "aniss", "nino", "amir", "chouchou"):
        if kid in blob:
            raise SystemExit(f"{SID}: 2e enfant {kid}")

    adults = [ln for ln in blob.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    aj = " ".join(a.split("|", 1)[1] for a in adults)
    n_merci = aj.count("merci") + aj.count("bravo")
    if n_merci != 1:
        raise SystemExit(f"{SID}: merci/bravo ×{n_merci}")

    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "plus de temps ou de calme",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "il faut attendre",
        "aujourd'hui",
        "j'ai compris",
        "mission accomplie",
        "merle",
        "miel",
        "galet",
        "poisson",
        "salon",
        "inès",
        "ines",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "bac à sable",
        "toboggan",
        "balançoire",
        "marelle",
        "citronnade",
        "tout doux",
        "tout calme",
        "étoile brune",
        "fil pâle",
        "bouton nacre",
        "nœud raphia",
        "pois ivoire",
        "grain savon",
        "grain vanille",
        "pastille colle",
        "virgule buée",
        "capuchon penche",
        "grain doré",
        "brin safran",
        "anneau liège",
        "grain d'ambre",
        "goutte de cire",
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
        "cristal de sucre",
        "écaille de lichen",
        "grain de cire",
        "dent de fermeture dorée",
        "écaille de nacre",
        "grain de paprika",
        "écaille de boue",
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
        "grain de bitume",
        "grain de laine",
        "croissant d'eau",
        "croissant pâle",
        "virgule farine",
        "ancre",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan/calque: {bad}")

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
    if min(counts) < 550:
        raise SystemExit(f"chemins trop courts min={min(counts)}<550")
    if max(counts) > 720:
        raise SystemExit(f"chemins trop longs max={max(counts)}>720")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    if len(story["chunks"]) != 86:
        raise SystemExit(f"chunks {len(story['chunks'])}≠86")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-072 — Le sac bleu de Sarah, au vestiaire\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.BES.001 — plus de temps / calme, observer (vécue, jamais dite)\n"
        "- **Personnages :** Sarah, papa, maman (pas de 2e enfant)\n"
        "- **Lieu :** vestiaire de l'école : manteaux, crochets, banc du fond\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` / labels inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Derrière la porte vitrée, le vestiaire sent la laine mouillée. "
        "Un grain de grelot brille près du banc : l'anneau du crochet en manque un. "
        "Sarah veut fermer son sac bleu **à la dernière maille, avant la cloche**. "
        "Elle tire trop vite : le curseur bloque. Première idée ratée. "
        "Elle prend le sac, le goûter ou le grelot ; les trois viennent. "
        "Sous les manteaux ça goutte, près de la porte ça pousse, au banc du fond "
        "c'est trop sombre. L'objet résiste, disparaît ou révèle le grain. "
        "Elle refuse de foncer. Neuf façons de prendre le temps "
        "(poser, compter, recommencer ; plus loin, mailles, un instant ; "
        "lumière, genoux, sans forcer). Le sac clique. Le grain rentre.\n\n"
        "## Vécu\n\n"
        "Sarah veut la maille **maintenant**. Elle tire trop tôt. Sourire parti, "
        "poitrine serrée. Papa s'accroupit. Chaque choix change l'obstacle et le climax. "
        "La leçon se voit : personne ne dit d'attendre ; poser, compter, regarder "
        "les mailles, un instant, la lumière, les genoux ou glisser sans forcer "
        "fait cliquer le sac. Fin : sac fermé + grain de grelot payé, image unique du chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Ancien F-NAR-016 (notes/xai vides, Inès, bac/toboggan) entièrement réécrit.\n"
        "- Ouverture inventée (laine, col rouge, grain manquant). Pas de « encore ».\n"
        "- Indice unique : **un grain de grelot**, vu à l'ouverture, payé au climax et à la fin.\n"
        "- Pas de 2e enfant. Monde ≠ AUT-009 (salon) ≠ DIF-045 (galet, classe).\n"
        "- Tics « encore / déjà / tout doux / tout calme » hors texte "
        "(le label graphe « tout doux » est conservé, dit « sans forcer »).\n"
        "- T1/T2/T3 changent l'action. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (crochet essuyé). Question d'adulte. Un « en ce moment ».\n"
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
