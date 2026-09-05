#!/usr/bin/env python3
"""TREE-DIF-013 — Le sel sur les lèvres de Sarah (F-NAR-019, N2, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-013"
N2 = 15
TITLE = "Le sel sur les lèvres de Sarah"
FIL = (
    "Sarah veut le sel de l'écume sur les lèvres, maintenant. "
    "Porter le seau à deux jusqu'à la cabane, avant la vague. "
    "Aniss n'a pas le même rythme : il s'arrête, il se tait. "
    "Sarah tire seule : le seau penche, le sable rentre. "
    "Un éclat de coquille brille sur le seuil. "
    "T1 = le matin / après la sieste / le soir : ballon, seau, doudou partent. "
    "T2 = ballon rouge / seau bleu / doudou. "
    "T3 labels Tom / Léa / Sami = crabe, coquillages, dessin. "
    "Sarah refuse de foncer. L'éclat paie. Le sel pique."
)
CHARS = "Sarah, Aniss, papa, maman"
SETTING = "cabane au bord de la mer, dune et écume"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

T1_LABS = ("le matin", "après la sieste", "le soir")
T2_LABS = ("le ballon rouge", "le seau bleu", "le doudou")
T3_KEEP = ("Tom", "Léa", "Sami")

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "éclat de coquille",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_salée; intensite=1; destinataire=enfant; sous_texte=le_sel_manque_aux_lèvres_aniss_n_a_pas_le_même_rythme; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qui_s_est_passé; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "éclat de coquille",
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=la_première_idée_a_raté_le_seau_a_penché; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=Sarah_propose_Aniss_prend_son_temps; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=le_silence_d_Aniss_est_une_réponse; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "éclat de coquille",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=porter_à_deux_sans_foncer; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "éclat de coquille",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_sel_pique_les_lèvres_l_éclat_paie_le_début; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Les lèvres de Sarah sont sèches.",
    "enfant-f|Je veux le sel, maintenant.",
    "narrateur|La cabane sent le bois mouillé.",
    "narrateur|Un volet claque, une fois.",
    "narrateur|Sur le seuil, un éclat de coquille brille.",
    "narrateur|Rose et blanc, mince comme un ongle.",
    "papa|Tu as vu l'éclat de coquille ?",
    "enfant-f|Il pique un peu.",
    "narrateur|Aniss arrive, le seau contre le genou.",
    "enfant-f|On court à l'écume !",
    "narrateur|Aniss s'arrête, les yeux sur l'éclat.",
    "narrateur|Il ne dit rien.",
    "maman|Aniss regarde, Sarah.",
    "narrateur|Sarah tire le seau, toute seule.",
    "narrateur|Le seau penche, le sable y rentre.",
    "enfant-f|L'écume, elle s'en va !",
    "papa|Je me baisse, à vos genoux.",
    "maman|Merci, tu as montré l'éclat.",
    "narrateur|En ce moment, le sel manque aux lèvres.",
    "papa|On prend les affaires, alors ?",
    "narrateur|Une corde goutte, près du bateau.",
    "enfant-m|Le seau est trop lourd.",
    "papa|À deux, il avancera.",
]

T1_CHOICE = [
    "narrateur|Le sel attend, au bord de l'eau.",
    "narrateur|Le matin, après la sieste, ou le soir.",
    "maman|Vous partez quand, tous les deux ?",
]

T1 = {
    1: {
        "lab": "le matin",
        "sons": "mer,oiseaux",
        "emphasis": "écume",
        "passage": [
            "narrateur|La lumière du matin est pâle, un peu froide.",
            "narrateur|Le sable mouillé colle aux orteils.",
            "enfant-f|L'écume est là, près des pieds.",
            "narrateur|Sarah veut courir, tout de suite.",
            "narrateur|Aniss pose le doudou près de l'éclat.",
            "narrateur|Il ne bouge pas.",
            "enfant-f|Aniss, viens !",
            "narrateur|Sarah prend le seau, trop vite.",
            "papa|Le ballon et le doudou viennent aussi.",
            "narrateur|Maman glisse les trois affaires, près des tongs.",
            "enfant-m|J'arrive.",
            "narrateur|Le seau penche, le sable rentre.",
            "maman|L'écume n'est pas dedans.",
            "narrateur|Sarah ne rit plus.",
        ],
        "question": [
            "narrateur|Sarah veut le sel sur ses lèvres.",
            "maman|Elle veut le sel où ?",
        ],
        "qfields": {
            "expected_answer": "lèvres",
            "accepted_examples": "lèvres | les lèvres | sur les lèvres | sa lèvre | la bouche",
            "retry_prompt": "Sarah veut le sel sur ses lèvres. Elle veut le sel où ?",
        },
        "confirm": [
            "narrateur|Oui, sur les lèvres, le sel de l'écume.",
            "enfant-f|Le seau a pris du sable.",
            "enfant-m|Moi, je veux regarder l'éclat.",
            "papa|L'éclat de coquille reste sur le seuil.",
            "maman|On avance vers l'eau ?",
            "enfant-f|Oui, maman.",
            "narrateur|Aniss suit, sans se presser.",
            "narrateur|Ballon, seau, doudou : tout part.",
        ],
    },
    2: {
        "lab": "après la sieste",
        "sons": "mer,mouche",
        "emphasis": "seau",
        "passage": [
            "narrateur|Après la sieste, le sable brûle un peu.",
            "narrateur|L'écume s'est reculée, plus loin.",
            "enfant-f|On y va, vite !",
            "narrateur|Aniss s'assoit, le seau contre le genou.",
            "narrateur|Il serre le doudou, sans un mot.",
            "enfant-f|Lâche le seau, Aniss.",
            "narrateur|Sarah tire, trop fort.",
            "narrateur|Le ballon roule, le doudou glisse.",
            "papa|Les trois affaires restent avec vous.",
            "maman|Je glisse le ballon sous son bras.",
            "enfant-m|Attends.",
            "narrateur|Le seau penche, le sable chaud rentre.",
            "papa|L'écume n'est pas là.",
            "narrateur|Ça serre, sous la gorge de Sarah.",
        ],
        "question": [
            "narrateur|Aniss tient le seau contre son genou.",
            "papa|Il tient quoi, contre son genou ?",
        ],
        "qfields": {
            "expected_answer": "seau",
            "accepted_examples": "seau | le seau | seau bleu | le seau bleu | son seau",
            "retry_prompt": "Aniss tient le seau. Il tient quoi ?",
        },
        "confirm": [
            "narrateur|Oui, le seau, collé au genou d'Aniss.",
            "enfant-f|Il ne voulait pas courir.",
            "enfant-m|Le sable est trop chaud.",
            "maman|L'éclat de coquille luit, sur le seuil.",
            "papa|On avance, à votre pas ?",
            "enfant-m|Oui, papa.",
            "narrateur|Sarah ralentit, un cran.",
            "narrateur|Ballon, seau, doudou marchent ensemble.",
        ],
    },
    3: {
        "lab": "le soir",
        "sons": "mer,volet",
        "emphasis": "vague",
        "passage": [
            "narrateur|Le soir peint la dune, un peu orange.",
            "narrateur|Une vague revient, plus près.",
            "enfant-f|Avant la vague, le seau !",
            "narrateur|Aniss reste au seuil, l'éclat dans l'œil.",
            "narrateur|Il serre le doudou, collé au ventre.",
            "enfant-f|Aniss, la mer s'en va !",
            "narrateur|Sarah part, le seau à une main.",
            "papa|Le ballon et le doudou, avec vous.",
            "narrateur|Maman les pose dans ses bras.",
            "enfant-m|Je ne cours pas.",
            "narrateur|Le seau tape le genou, penche.",
            "narrateur|Le sable du soir y rentre.",
            "maman|L'écume n'est pas dedans.",
            "narrateur|Le volet claque, loin, une fois.",
        ],
        "question": [
            "narrateur|Un éclat de coquille brille sur le seuil.",
            "maman|Qu'est-ce qui brille, sur le seuil ?",
        ],
        "qfields": {
            "expected_answer": "éclat",
            "accepted_examples": "éclat | un éclat | éclat de coquille | coquille | la coquille",
            "retry_prompt": "Un éclat de coquille brille. Qu'est-ce qui brille ?",
        },
        "confirm": [
            "narrateur|Oui, l'éclat de coquille, rose et blanc.",
            "enfant-f|La vague va tout prendre.",
            "enfant-m|Moi, je reste près de l'éclat.",
            "papa|On avance, avant la vague ?",
            "enfant-f|Oui, mais à son pas.",
            "maman|Le ballon, le seau, le doudou partent.",
            "narrateur|Aniss hoche la tête, tout petit.",
            "narrateur|La dune sent l'iode, devant eux.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le sable froid tremble, un peu.",
        "narrateur|Voilà le ballon rouge, sablé.",
        "narrateur|Le seau bleu penche, vide.",
        "narrateur|Près des tongs, le doudou sent le bois.",
        "papa|Vous prenez quoi, pour l'écume ?",
    ],
    2: [
        "narrateur|Le sable chaud pique les talons.",
        "narrateur|Voilà le ballon rouge, un peu mou.",
        "narrateur|Le seau bleu brûle au bord.",
        "narrateur|Près des tongs, le doudou sent la sieste.",
        "maman|Vous prenez quoi, pour l'écume ?",
    ],
    3: [
        "narrateur|Le sable orangé refroidit les pieds.",
        "narrateur|Voilà le ballon rouge, vers l'eau.",
        "narrateur|Le seau bleu sonne, vide.",
        "narrateur|Près des tongs, le doudou sent le vent.",
        "papa|Vous prenez quoi, pour l'écume ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "ballon,sable",
        "emphasis": "ballon",
        "passage": [
            "narrateur|Sarah pousse le ballon rouge, vers l'écume.",
            "enfant-f|Il va la chercher !",
            "narrateur|Le ballon roule, trop vite, dans le froid.",
            "enfant-m|Moi, je le garde.",
            "narrateur|Aniss tend les mains, trop tard.",
            "narrateur|Le ballon tombe dans un trou.",
            "enfant-f|Cours, Aniss !",
            "narrateur|Aniss secoue la tête, sans un mot.",
            "narrateur|L'écume n'est pas dans le trou.",
            "papa|Le ballon a filé, tout seul.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle observe le ballon, écoute la mer.",
            "narrateur|Elle retrouve l'éclat de coquille, sur le sable.",
            "maman|Vous le reprenez comment, le ballon ?",
        ],
    },
    (1, 2): {
        "sons": "seau,eau",
        "emphasis": "seau",
        "passage": [
            "narrateur|Sarah plonge le seau bleu, trop vite.",
            "enfant-f|L'écume, je l'ai !",
            "narrateur|Le seau se remplit de sable mouillé.",
            "enfant-m|Il est trop lourd.",
            "narrateur|Aniss lâche l'anse, un doigt.",
            "enfant-f|Tiens-le, allez !",
            "narrateur|Aniss recule, les lèvres serrées.",
            "narrateur|Le seau penche, l'écume s'échappe.",
            "papa|Le blanc n'est plus dedans.",
            "narrateur|Sarah ne rit plus.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle observe le seau, écoute la mer.",
            "narrateur|Elle retrouve l'éclat de coquille, au bord.",
            "maman|Vous le remplissez comment, le seau ?",
        ],
    },
    (1, 3): {
        "sons": "tissu,vague",
        "emphasis": "doudou",
        "passage": [
            "narrateur|Sarah tend le doudou, vers l'écume froide.",
            "enfant-f|Il va l'essuyer !",
            "narrateur|Le tissu frôle l'eau, trop loin.",
            "enfant-m|Il va se mouiller.",
            "narrateur|Aniss tire le doudou, contre lui.",
            "enfant-f|Lâche, Aniss !",
            "narrateur|Aniss secoue la tête, sans un mot.",
            "narrateur|Le doudou reste sec, l'écume trop loin.",
            "papa|Le tissu n'a rien pris.",
            "narrateur|Ça serre, sous la gorge de Sarah.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle observe le doudou, écoute la mer.",
            "narrateur|Elle retrouve l'éclat de coquille, au seuil.",
            "maman|Vous l'approchez comment, le doudou ?",
        ],
    },
    (2, 1): {
        "sons": "ballon,chaleur",
        "emphasis": "ballon",
        "passage": [
            "narrateur|Sarah tape le ballon rouge, sur le chaud.",
            "enfant-f|Vers l'écume, hop !",
            "narrateur|Le ballon rebondit, trop haut, trop loin.",
            "enfant-m|Moi, je m'assois.",
            "narrateur|Aniss s'assoit, le doudou sur les genoux.",
            "enfant-f|Cours après !",
            "narrateur|Aniss ferme la bouche, et reste.",
            "narrateur|Le ballon s'arrête dans une flaque chaude.",
            "papa|L'écume n'est pas dans la flaque.",
            "narrateur|Le sourire de Sarah s'en va.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle observe le ballon, écoute la dune.",
            "narrateur|Elle retrouve l'éclat de coquille, un peu loin.",
            "maman|Vous le ramenez comment, le ballon ?",
        ],
    },
    (2, 2): {
        "sons": "seau,chaleur",
        "emphasis": "anse",
        "passage": [
            "narrateur|Sarah hisse le seau bleu, dans le chaud.",
            "enfant-f|On le porte, allez !",
            "narrateur|Le métal brûle, un peu, au bord.",
            "enfant-m|Mes mains, non.",
            "narrateur|Aniss ouvre les paumes, puis les retire.",
            "enfant-f|Aniss, tiens l'autre côté !",
            "narrateur|Aniss secoue la tête, sans un mot.",
            "narrateur|Sarah porte seule, le seau penche.",
            "papa|Le sable chaud rentre, pas l'écume.",
            "narrateur|Sarah ne rit plus.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle observe le seau, écoute la dune.",
            "narrateur|Elle retrouve l'éclat de coquille, sous l'anse.",
            "maman|Vous le portez comment, le seau ?",
        ],
    },
    (2, 3): {
        "sons": "tissu,sieste",
        "emphasis": "doudou",
        "passage": [
            "narrateur|Sarah veut le doudou, pour l'écume chaude.",
            "enfant-f|On essuie le blanc, avec.",
            "narrateur|Aniss le serre, collé à la sieste.",
            "enfant-m|Il est à moi, là.",
            "narrateur|Sarah tire un coin, trop vite.",
            "narrateur|Le doudou s'étire, Aniss ne lâche pas.",
            "enfant-f|S'il te plaît !",
            "narrateur|Aniss baisse les yeux, sans un mot.",
            "papa|Le tissu reste au creux, sec.",
            "narrateur|L'écume attend, trop loin.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle observe le doudou, écoute la dune.",
            "narrateur|Elle retrouve l'éclat de coquille, au coin.",
            "maman|Vous l'empruntez comment, le doudou ?",
        ],
    },
    (3, 1): {
        "sons": "ballon,vague",
        "emphasis": "vague",
        "passage": [
            "narrateur|Sarah envoie le ballon rouge, vers la vague.",
            "enfant-f|Avant qu'elle recule !",
            "narrateur|Le ballon roule, trop près de l'eau.",
            "enfant-m|Il va partir.",
            "narrateur|Aniss s'arrête, les pieds dans le sable.",
            "enfant-f|Cours, Aniss !",
            "narrateur|Aniss recule d'un pas, les lèvres serrées.",
            "narrateur|Une vague lèche le ballon, puis recule.",
            "papa|Le ballon est mouillé, l'écume n'est pas à vous.",
            "narrateur|Le volet claque, loin.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle observe le ballon, écoute la vague.",
            "narrateur|Elle retrouve l'éclat de coquille, sur la dune.",
            "maman|Vous le rattrapez comment, le ballon ?",
        ],
    },
    (3, 2): {
        "sons": "seau,vague",
        "emphasis": "vague",
        "passage": [
            "narrateur|Sarah avance le seau bleu, face à la vague.",
            "enfant-f|On prend le blanc, maintenant !",
            "narrateur|La vague arrive, trop grosse.",
            "enfant-m|Stop.",
            "narrateur|Aniss plaque une main sur l'anse.",
            "enfant-f|Lâche, on va la rater !",
            "narrateur|Aniss ne dit rien, et tient.",
            "narrateur|La vague passe, le seau reste vide.",
            "papa|Elle a failli tout emporter.",
            "narrateur|Sarah ne rit plus.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle observe le seau, écoute la vague.",
            "narrateur|Elle retrouve l'éclat de coquille, au bord.",
            "maman|Vous le remplissez comment, le seau ?",
        ],
    },
    (3, 3): {
        "sons": "tissu,voix",
        "emphasis": "voix",
        "passage": [
            "narrateur|Sarah tend le doudou, vers le blanc du soir.",
            "enfant-f|Un peu d'écume, dessus !",
            "narrateur|Une voix passe, au loin, sur la dune.",
            "enfant-m|J'écoute.",
            "narrateur|Aniss se tourne, le doudou serré.",
            "enfant-f|Pas par là, l'écume est ici !",
            "narrateur|Aniss reste, les yeux vers la voix.",
            "narrateur|Le doudou ne touche pas l'eau.",
            "papa|Deux chemins, un seul doudou.",
            "narrateur|Ça serre, sous la gorge de Sarah.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Elle observe le doudou, écoute la dune.",
            "narrateur|Elle retrouve l'éclat de coquille, entre eux.",
            "maman|Vous restez comment, tous les deux ?",
        ],
    },
}

T3_CHOICE = {
    1: [
        "narrateur|Le ballon s'arrête, trop seul.",
        "narrateur|Un crabe barre le sable.",
        "narrateur|Des coquillages font une crête.",
        "narrateur|Un dessin appelle, plus loin.",
        "papa|Le crabe, les coquillages, ou le dessin ?",
    ],
    2: [
        "narrateur|Le seau s'arrête, trop lourd.",
        "narrateur|Un crabe barre le sable.",
        "narrateur|Des coquillages font une crête.",
        "narrateur|Un dessin appelle, plus loin.",
        "maman|Le crabe, les coquillages, ou le dessin ?",
    ],
    3: [
        "narrateur|Le doudou s'arrête, trop sec.",
        "narrateur|Un crabe barre le sable.",
        "narrateur|Des coquillages font une crête.",
        "narrateur|Un dessin appelle, plus loin.",
        "papa|Le crabe, les coquillages, ou le dessin ?",
    ],
}

T3_SONS = {
    (1, 1): "crabe,sable",
    (1, 2): "coquillage,sable",
    (1, 3): "vent,voix",
    (2, 1): "crabe,seau",
    (2, 2): "coquillage,seau",
    (2, 3): "vent,seau",
    (3, 1): "crabe,tissu",
    (3, 2): "coquillage,tissu",
    (3, 3): "voix,tissu",
}


def air(a: int) -> str:
    return "narrateur|" + (
        "Le sable du matin colle aux talons.",
        "Le sable de la sieste brûle un peu.",
        "Le sable du soir refroidit les pieds.",
    )[a - 1]


def held(b: int) -> str:
    return "narrateur|" + (
        "Le ballon rouge attend entre eux.",
        "Le seau bleu attend entre eux.",
        "Le doudou attend entre eux.",
    )[b - 1]


def scoop(b: int) -> str:
    return "narrateur|" + (
        "Sarah pose le ballon, Aniss tend le seau.",
        "Sarah tient une anse, Aniss l'autre.",
        "Sarah tient le doudou, Aniss le seau.",
    )[b - 1]


def foam_in(b: int) -> str:
    return "narrateur|" + (
        "L'écume glisse, blanche, près du ballon.",
        "L'écume glisse, blanche, dans le seau.",
        "L'écume glisse, blanche, au bord du doudou.",
    )[b - 1]


def t3_pass(a: int, b: int, c: int) -> list[str]:
    rows: dict[tuple[int, int], list[str]] = {
        (1, 1): [
            "enfant-m|Un crabe, Sarah.",
            "narrateur|Le crabe barre le passage, pinces ouvertes.",
            "enfant-f|J'attends.",
            air(a),
            held(b),
            "narrateur|Aniss pose l'objet, loin des pinces.",
            "narrateur|Le crabe recule vers son trou.",
            "enfant-m|Il est parti.",
            scoop(b),
            "papa|Vous avez laissé le passage.",
            "narrateur|Elle retrouve l'éclat de coquille, près du trou.",
            foam_in(b),
            "enfant-f|Elle est à nous.",
            "maman|Le seau a failli tomber.",
        ],
        (1, 2): [
            "enfant-f|La crête pique, Aniss.",
            "narrateur|Des coquillages font un mur, tout mince.",
            "enfant-m|On tourne.",
            air(a),
            held(b),
            "narrateur|Aniss trouve un trou, à sa hauteur.",
            "enfant-f|Je te suis.",
            scoop(b),
            "narrateur|Ils passent à côté, sans enjamber.",
            "papa|Le mur n'a pas bougé.",
            "narrateur|Elle retrouve l'éclat de coquille, sous un bord.",
            foam_in(b),
            "enfant-m|On l'a.",
            "maman|Le blanc a failli rester derrière.",
        ],
        (1, 3): [
            "enfant-m|Un dessin, dans le sable.",
            "narrateur|Une ligne mène vers l'écume, puis casse.",
            "enfant-f|La voix, là-bas ?",
            "narrateur|Aniss montre la ligne, pas la voix.",
            air(a),
            held(b),
            "enfant-f|On suit le trait, alors.",
            scoop(b),
            "narrateur|Ils marchent sur le trait, l'un après l'autre.",
            "papa|La voix s'est tue, au loin.",
            "narrateur|Elle retrouve l'éclat de coquille, au bout.",
            foam_in(b),
            "enfant-m|Le trait nous a gardés.",
            "maman|Vous avez failli vous séparer.",
        ],
        (2, 1): [
            "enfant-f|Le crabe est sur le chemin du seau.",
            "narrateur|Les pinces touchent presque l'anse.",
            "enfant-m|On pose, d'abord.",
            air(a),
            held(b),
            "narrateur|Sarah pose, Aniss attend, sans pousser.",
            "narrateur|Le crabe part, de travers.",
            scoop(b),
            "papa|Deux mains, un seau, pas de pince.",
            "narrateur|Elle retrouve l'éclat de coquille, sous l'anse.",
            foam_in(b),
            "enfant-f|Le blanc est là.",
            "maman|Le seau a failli claquer le crabe.",
            "narrateur|Personne n'a forcé le passage.",
        ],
        (2, 2): [
            "enfant-m|Les coquillages coupent le sable.",
            "narrateur|La crête est trop haute pour Aniss.",
            "enfant-f|Je soulève un bord, toi tu glisses.",
            air(a),
            held(b),
            "narrateur|Sarah lève, Aniss passe le seau dessous.",
            scoop(b),
            "papa|Chacun a fait sa part.",
            "narrateur|Elle retrouve l'éclat de coquille, dans la crête.",
            foam_in(b),
            "enfant-m|Il est lourd, maintenant.",
            "enfant-f|C'est l'écume.",
            "maman|La crête a failli tout bloquer.",
            "narrateur|Un coquillage sonne, puis se tait.",
        ],
        (2, 3): [
            "enfant-f|Le dessin part vers la voix.",
            "narrateur|Aniss s'arrête au premier trait.",
            "enfant-m|On ne suit pas la voix.",
            air(a),
            held(b),
            "narrateur|Sarah revient, le seau contre sa hanche.",
            scoop(b),
            "papa|Le trait du sable, pas celui du vent.",
            "narrateur|Elle retrouve l'éclat de coquille, sur la ligne.",
            foam_in(b),
            "enfant-f|On est restés.",
            "maman|La voix a failli vous tirer ailleurs.",
            "narrateur|Le dessin s'arrête au bord de l'écume.",
            "enfant-m|Ici, c'est bien.",
        ],
        (3, 1): [
            "enfant-m|Le crabe touche le doudou.",
            "narrateur|Une pince accroche un fil, tout mince.",
            "enfant-f|On recule, Aniss.",
            air(a),
            held(b),
            "narrateur|Aniss tire le doudou, Sarah le seau.",
            "narrateur|Le crabe lâche, et part.",
            scoop(b),
            "papa|Le tissu est sauf, les pinces aussi.",
            "narrateur|Elle retrouve l'éclat de coquille, au fil.",
            foam_in(b),
            "enfant-f|Un peu de blanc, au bord.",
            "maman|Le doudou a failli y rester.",
            "narrateur|Sarah passe la langue, un instant trop tôt.",
        ],
        (3, 2): [
            "enfant-f|Les coquillages piquent le doudou.",
            "narrateur|La crête accroche le tissu, trop sec.",
            "enfant-m|On contourne, bas.",
            air(a),
            held(b),
            "narrateur|Aniss glisse le doudou, près du sable.",
            scoop(b),
            "papa|Le tissu n'a pas gratté.",
            "narrateur|Elle retrouve l'éclat de coquille, sous la crête.",
            foam_in(b),
            "enfant-m|Le bord est mouillé, juste assez.",
            "enfant-f|C'est l'écume, Aniss.",
            "maman|La crête a failli déchirer le coin.",
            "narrateur|Un bord blanc reste au tissu.",
        ],
        (3, 3): [
            "enfant-m|Le dessin, pas la voix.",
            "narrateur|La voix revient, plus près, sur la dune.",
            "enfant-f|On reste sur le trait.",
            air(a),
            held(b),
            "narrateur|Aniss pose le doudou sur la ligne.",
            scoop(b),
            "papa|Deux ombres, un seul trait.",
            "narrateur|Elle retrouve l'éclat de coquille, au milieu.",
            foam_in(b),
            "enfant-f|Le blanc est là, pas là-bas.",
            "maman|La voix a failli vous séparer.",
            "narrateur|Le trait s'arrête au seau, plein.",
            "enfant-m|On rentre.",
        ],
    }
    return rows[(b, c)]


END_LEAD = {
    (1, 1): [
        "narrateur|Ils rentrent, le seau entre deux hanches.",
        "enfant-m|Le crabe a son trou.",
        "enfant-f|On a attendu.",
        "papa|Le passage s'est ouvert, tout seul.",
        "maman|Goûtez, maintenant.",
    ],
    (1, 2): [
        "narrateur|Ils rentrent le long de la crête.",
        "enfant-f|On a tourné, pas enjambé.",
        "enfant-m|Le trou était à moi.",
        "papa|La crête est restée.",
        "maman|Goûtez, sur le seuil.",
    ],
    (1, 3): [
        "narrateur|Le trait de sable les ramène.",
        "enfant-m|La voix s'est tue.",
        "enfant-f|On a suivi le dessin.",
        "papa|Un seul chemin, à deux.",
        "maman|Goûtez, près de la cabane.",
    ],
    (2, 1): [
        "narrateur|Le seau sonne, un peu, sur le bois.",
        "enfant-f|Les pinces n'ont rien pris.",
        "enfant-m|On a posé, d'abord.",
        "papa|Deux mains ont suffi.",
        "maman|Goûtez, avant le volet.",
    ],
    (2, 2): [
        "narrateur|Un coquillage sonne dans une poche.",
        "enfant-m|Tu as levé, j'ai glissé.",
        "enfant-f|Le seau est lourd, maintenant.",
        "papa|Chacun sa part.",
        "maman|Goûtez, sur les marches.",
    ],
    (2, 3): [
        "narrateur|Ils n'ont pas suivi la voix.",
        "enfant-f|Le trait s'arrêtait à l'écume.",
        "enfant-m|Ici, c'était bien.",
        "papa|Le vent n'a pas gagné.",
        "maman|Goûtez, contre la cabane.",
    ],
    (3, 1): [
        "narrateur|Le doudou sent le sel, un fil.",
        "enfant-m|La pince a lâché.",
        "enfant-f|On a reculé, à temps.",
        "papa|Le tissu est sauf.",
        "maman|Goûtez, près du clou.",
    ],
    (3, 2): [
        "narrateur|Un bord de doudou reste mouillé.",
        "enfant-f|Les coquillages n'ont pas gratté.",
        "enfant-m|On a contourné, bas.",
        "papa|Le coin est entier.",
        "maman|Goûtez, sur le bois.",
    ],
    (3, 3): [
        "narrateur|Deux ombres rentrent sur le même trait.",
        "enfant-f|La voix est restée là-bas.",
        "enfant-m|Le doudou a gardé le trait.",
        "papa|Vous n'avez pas divergé.",
        "maman|Goûtez, sous le volet.",
    ],
}

END_MID = {
    1: "narrateur|La lumière pâle reste sur le seuil.",
    2: "narrateur|Le sable chaud colle aux mollets.",
    3: "narrateur|Le volet claque, loin, une fois.",
}

END_TASTE = {
    1: "enfant-f|Ça pique, sur ma lèvre.",
    2: "enfant-f|Le sel est chaud, presque.",
    3: "enfant-f|Le sel du soir, il est là.",
}

ASK = {
    1: "papa|Le seau, trop lourd, tu t'en souviens ?",
    2: "maman|Aniss n'a rien dit, tu as vu ?",
    3: "papa|La vague, tu l'as vue venir ?",
}

ANS = {
    1: "enfant-f|Oui, et ses mains sur l'anse.",
    2: "enfant-f|Oui, son silence m'a arrêtée.",
    3: "enfant-f|Oui, on a reculé à temps.",
}

LAST = {
    (1, 1, 1): "L'éclat de coquille sèche près du trou de crabe.",
    (1, 1, 2): "L'éclat de coquille sonne sous un bord de crête.",
    (1, 1, 3): "L'éclat de coquille dort au bout du trait.",
    (1, 2, 1): "L'éclat de coquille reste collé sous l'anse froide.",
    (1, 2, 2): "L'éclat de coquille brille dans un coquillage vide.",
    (1, 2, 3): "L'éclat de coquille coupe la ligne du dessin.",
    (1, 3, 1): "L'éclat de coquille accroche un fil du doudou.",
    (1, 3, 2): "L'éclat de coquille pique le coin du tissu.",
    (1, 3, 3): "L'éclat de coquille tient le milieu du trait.",
    (2, 1, 1): "L'éclat de coquille luit au fond du trou tiède.",
    (2, 1, 2): "L'éclat de coquille chauffe contre un coquillage.",
    (2, 1, 3): "L'éclat de coquille sèche au bout du dessin chaud.",
    (2, 2, 1): "L'éclat de coquille colle à l'anse, un peu brûlant.",
    (2, 2, 2): "L'éclat de coquille sonne, tiède, dans la crête.",
    (2, 2, 3): "L'éclat de coquille marque le trait, côté cabane.",
    (2, 3, 1): "L'éclat de coquille se cache au poignet du doudou.",
    (2, 3, 2): "L'éclat de coquille reste sous le coin tiède.",
    (2, 3, 3): "L'éclat de coquille garde le doudou sur la ligne.",
    (3, 1, 1): "L'éclat de coquille pâlit près du trou du soir.",
    (3, 1, 2): "L'éclat de coquille orange un bord de crête.",
    (3, 1, 3): "L'éclat de coquille s'éteint au bout du trait.",
    (3, 2, 1): "L'éclat de coquille cligne sous l'anse du soir.",
    (3, 2, 2): "L'éclat de coquille se tait dans la crête sombre.",
    (3, 2, 3): "L'éclat de coquille guide le seau jusqu'au bois.",
    (3, 3, 1): "L'éclat de coquille frôle le fil, puis sèche.",
    (3, 3, 2): "L'éclat de coquille mouille un coin, puis sèche.",
    (3, 3, 3): "L'éclat de coquille ferme le trait, sous le volet.",
}


def ending(a: int, b: int, c: int) -> list[str]:
    rows = list(END_LEAD[(b, c)])
    rows.append(END_MID[a])
    rows.append(END_TASTE[a])
    rows.append("enfant-m|Moi aussi, un peu.")
    rows.append("narrateur|Sarah passe la langue, le sel pique.")
    rows.append(ASK[b])
    rows.append(ANS[b])
    rows.append(f"narrateur|{LAST[(a, b, c)]}")
    return rows


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "mer,volet,bois",
        {"emphasis": "éclat de coquille"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab(*T1_LABS), "pause_before": 200},
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
            {"emphasis": "éclat de coquille"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab(*T2_LABS), "pause_before": 200},
        )
        for b in (1, 2, 3):
            bse = f"{base}_T0002_P000{b}"
            out_chunks[bse] = voice(
                by_src[bse], T2[(a, b)]["passage"], "obstacle", T2[(a, b)]["sons"],
                {"emphasis": T2[(a, b)]["emphasis"]},
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab(*T3_KEEP), "pause_before": 200},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], t3_pass(a, b, c), "resolution", T3_SONS[(b, c)],
                    {"emphasis": "éclat de coquille"},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ending(a, b, c), "ending", "cabane,mer",
                    {"emphasis": "éclat de coquille"},
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
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "tailles",
        "le corps n'est pas",
        "tout doux",
        "tout calme",
        "tout lent",
        "aujourd'hui",
        "merle",
        "couleur de miel",
        "j'ai une idée",
        "celui où j'ai compris",
        "mission accomplie",
        "j'ai compris",
        "gouttes au bord",
        "tout près tout loin",
        "victorino",
        "marelle",
        "pommier",
        "tarte",
        "grain de sel",
        "point d'écume",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if re.search(r"\bsara\b", blob):
        raise SystemExit(f"{SID}: Sara (hors Sarah)")
    if re.search(r"\btom\b|\bléa\b|\blea\b|\bsami\b", blob):
        raise SystemExit(f"{SID}: Tom/Léa/Sami dans le script")
    if TIC_WORDS.search(blob):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "enfant-f|" not in blob:
        raise SystemExit(f"{SID}: enfant-f absent")
    if "enfant-m|" not in blob:
        raise SystemExit(f"{SID}: enfant-m absent")
    if "éclat de coquille" not in blob:
        raise SystemExit(f"{SID}: indice éclat de coquille absent")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: refuse de foncer absent")
    if blob.count("merci") + blob.count("bravo") > 2:
        raise SystemExit(f"{SID}: trop de merci/bravo")

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
        if "éclat de coquille" not in c["text"].lower():
            raise SystemExit(f"fin sans indice: {c['chunk_id']}")
        if "lèvre" not in c["text"].lower() and "sel" not in c["text"].lower():
            raise SystemExit(f"fin sans sel/lèvres: {c['chunk_id']}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images {len(set(lasts))}/27")

    t3s = [c["text"] for c in story["chunks"] if re.search(r"T0003_P000[123]$", c["chunk_id"])]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"T3 distincts {len(set(t3s))}/27")

    t2s = [c["text"] for c in story["chunks"] if re.search(r"T0002_P000[123]$", c["chunk_id"])]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"T2 distincts {len(set(t2s))}/9")

    # labels originaux
    for c in story["chunks"]:
        if c["chunk_id"] == "CHK_T0001_P0000":
            if (c.get("option_1_label"), c.get("option_2_label"), c.get("option_3_label")) != T1_LABS:
                raise SystemExit(f"T1 labels {c.get('option_1_label')}")
        if c["chunk_id"].endswith("T0002_P0000"):
            if (c.get("option_1_label"), c.get("option_2_label"), c.get("option_3_label")) != T2_LABS:
                raise SystemExit(f"T2 labels {c['chunk_id']}")
        if re.search(r"T0003_P0000$", c["chunk_id"]):
            if (c.get("option_1_label"), c.get("option_2_label"), c.get("option_3_label")) != T3_KEEP:
                raise SystemExit(f"T3 labels {c['chunk_id']}")

    for c in src["chunks"]:
        nc = out_chunks[c["chunk_id"]]
        for k in ("option_1_next_chunk", "option_2_next_chunk", "option_3_next_chunk", "default_next_chunk"):
            if (c.get(k) or "") != (nc.get(k) or ""):
                raise SystemExit(f"{c['chunk_id']} graphe {k} cassé")
        if c.get("kind") != nc.get("kind"):
            raise SystemExit(f"{c['chunk_id']} kind cassé")

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
    if len(story["chunks"]) != 86:
        raise SystemExit(f"chunks {len(story['chunks'])}≠86")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK {SID} {sum(words(c['text']) for c in story['chunks'])} mots")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-013 — Le sel sur les lèvres de Sarah\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.COR.001 — porter à deux, pas toute seule "
        "(vécue, jamais dite)\n"
        "- **Personnages :** Sarah, Aniss, papa, maman\n"
        "- **Lieu :** cabane au bord de la mer, dune, écume\n"
        "- **Indice :** éclat de coquille (seuil → climax → 27 fins)\n"
        "- **Mission :** porter le seau d'écume à deux jusqu'à la cabane, "
        "avant la vague, pour le sel sur les lèvres\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés. "
        "Labels T1/T2/T3 d'origine restaurés.\n\n"
        "## Promesse narrative\n\n"
        "Les lèvres de Sarah sont sèches. Elle veut le sel de l'écume, "
        "maintenant. Un volet claque. Sur le seuil, un éclat de coquille "
        "brille, rose et blanc. Aniss arrive, le seau contre le genou. "
        "Sarah veut courir. Aniss s'arrête, les yeux sur l'éclat, sans un mot. "
        "Sarah tire seule : le seau penche, le sable rentre. Sourire parti. "
        "Papa se baisse à leurs genoux. Merci vécu : elle a montré l'éclat. "
        "T1 = le matin / après la sieste / le soir (moments ; ballon, seau, "
        "doudou partent tous). Première idée ratée à chaque fois. "
        "T2 = ballon rouge (roule trop loin), seau bleu (trop lourd / penche), "
        "doudou (Aniss ne lâche pas). Deuxième ruse. Sarah refuse de foncer, "
        "retrouve l'éclat. T3 labels Tom / Léa / Sami = crabe, coquillages, "
        "dessin dans le sable (voix au loin). Ils attendent, contournent, "
        "suivent le trait. Le seau a failli tomber. Le sel pique les lèvres. "
        "L'éclat paie le début. Monde ≠ marelle, ≠ pommier, ≠ tarte.\n\n"
        "## Vécu\n\n"
        "Sarah propose, tire, veut vite. Aniss prend son temps, pose sa limite. "
        "Le silence compte. Le seau penche tant qu'elle force seule. "
        "Papa ou maman se baisse à leur hauteur. Personne ne donne la réponse. "
        "Sarah observe l'objet, écoute la mer, retrouve l'éclat de coquille. "
        "La leçon se voit : à deux, le seau avance ; seule, le sable rentre. "
        "Fin : le sel pique les lèvres + éclat + image unique du chemin "
        "(trou de crabe, crête, trait, volet).\n\n"
        "## Vu et corrigé\n\n"
        "- Gabarit mer + « tout près tout loin » + tailles / jouer ensemble : tout jeté.\n"
        "- Ouverture inventée (lèvres sèches, pas les cinq formules v2). "
        "Indice unique : éclat de coquille (pas grain de sel, pas point d'écume).\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Corps : sourire parti, gorge, adulte à la même hauteur. 2e ruse. "
        "Refuse de foncer. Dénouement qui a failli.\n"
        "- T1 ne retire pas l'équipement. 9 T2, 27 T3, 27 fins, 27 dernières images.\n"
        "- Labels T1/T2/T3 d'origine. Tom/Léa/Sami absents du script (crabes, "
        "coquillages, dessin). Un pair D16 : Aniss.\n"
        "- Merci vécu (montrer l'éclat). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes`. "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N2 ≤ 15. `check()` OK. Pas apply. Pas audio. Pas git.\n\n"
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
