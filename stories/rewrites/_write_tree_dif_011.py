#!/usr/bin/env python3
"""TREE-DIF-011 — F-NAR-019. Parasol jaune, réponse d'Amir. N2. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-011"
N2 = 15
TITLE = "Le parasol jaune et la réponse d'Amir"
FIL = (
    "Sous le parasol jaune, un grain de parasol tient au bord de la toile. "
    "Amir veut garder l'ombre, avant que Nina emporte le seau. "
    "Nina veut jouer maintenant. Il court : le pied penche, l'ombre saute. "
    "T1 = sable / galets / ombre, les trois partent. "
    "T2 = seau / filet / livre. "
    "T3 = regarder / plus tard / un non : Amir dit sa limite, le non se voit. "
    "Le grain de parasol se cale."
)
CHARS = "Amir, Nina, papa, maman"
SETTING = "plage, sous un parasol jaune"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain de parasol",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_chaude; intensite=1; destinataire=enfant; sous_texte=nina_veut_maintenant_amir_veut_l_ombre; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_réponse; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_où_il_est; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "grain de parasol",
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=la_première_idée_a_raté; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=nina_tire_amir_perd_l_ombre; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_inquiétude; intensite=2; destinataire=enfant; sous_texte=l_objet_veut_partir_avec_nina; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_limite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=regarder_plus_tard_ou_non_se_voit; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain de parasol",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_de_parasol_se_cale_l_ombre_reste; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|La toile jaune chauffe, trop, au-dessus du sable.",
    "narrateur|Amir cligne des yeux, sous le parasol.",
    "narrateur|Un grain de parasol tient au bord de la toile.",
    "enfant-m|Il brille.",
    "narrateur|L'air sent le sel, chaud.",
    "papa|La chaise craque, près de la toile.",
    "maman|J'étale la serviette à carreaux.",
    "narrateur|Une mouette passe, trop haute.",
    "narrateur|Le rond d'ombre dort sur le sable.",
    "enfant-m|Je veux ce rond.",
    "maman|Il est à vous, s'il tient.",
    "narrateur|Des ronds d'eau claquent, plus bas.",
    "narrateur|Nina court vers l'eau, pieds mouillés.",
    "enfant-f|On joue, maintenant !",
    "narrateur|Elle tend la main vers le seau rouge.",
    "narrateur|Amir veut garder l'ombre, avant que le seau parte.",
    "enfant-m|J'y vais aussi !",
    "narrateur|Il court derrière elle.",
    "narrateur|Le pied du parasol penche, tout seul.",
    "narrateur|L'ombre saute hors de ses genoux.",
    "enfant-m|Elle part !",
    "narrateur|Le grain de parasol glisse vers le bord.",
    "narrateur|Le sourire d'Amir disparaît.",
    "papa|Tu entends la toile, Amir ?",
    "narrateur|En ce moment, il serre le pied du parasol.",
    "maman|Toi, tu veux quoi ?",
    "papa|On s'accroupit, à ta hauteur.",
    "narrateur|Le grain de parasol tremble, puis tient.",
]

T1_CHOICE = [
    "narrateur|Le parasol jaune attend, un peu penché.",
    "narrateur|Le sable, les galets, ou l'ombre.",
    "papa|Où commences-tu, Amir ?",
]

T1 = {
    1: {
        "lab": "le sable",
        "sons": "sable,vague",
        "emphasis": "sable",
        "passage": [
            "narrateur|Amir s'agenouille sur le sable chaud.",
            "narrateur|Le grain colle aux genoux, fin.",
            "enfant-m|Un château, vite !",
            "narrateur|Il pousse une colline, trop sèche.",
            "narrateur|La tour penche, puis tombe.",
            "enfant-m|Elle tombe !",
            "papa|Le sable a soif.",
            "narrateur|Un peu d'eau manque, au sommet.",
            "narrateur|Amir souffle, les genoux chauds.",
            "narrateur|Nina est près de l'eau, le seau levé.",
            "enfant-f|Viens, maintenant !",
            "narrateur|Amir se lève trop vite.",
            "narrateur|L'ombre a quitté ses genoux.",
            "narrateur|Le grain de parasol glisse, minuscule.",
            "maman|Elle t'a entendu.",
            "narrateur|Nina garde le seau, sans un mot.",
            "papa|On reste un peu, ou on court ?",
        ],
        "question": [
            "narrateur|Amir a poussé une colline.",
            "papa|Où sont ses genoux ?",
        ],
        "qfields": {
            "expected_answer": "sable",
            "accepted_examples": "sable | le sable | chaud | château | colline | genoux",
            "retry_prompt": "Amir s'agenouille. Où sont ses genoux ?",
        },
        "confirm": [
            "enfant-m|Sur le sable.",
            "papa|Oui.",
            "maman|Merci d'avoir senti le chaud.",
            "narrateur|La colline attend un peu d'eau.",
            "enfant-m|Je continue, sans courir.",
            "enfant-f|Moi, la mer.",
            "narrateur|Nina recule d'un pas, seau en main.",
            "papa|Le château n'est pas parti.",
            "narrateur|Un grain de parasol reste au bord.",
        ],
    },
    2: {
        "lab": "les galets",
        "sons": "galet,vague",
        "emphasis": "galets",
        "passage": [
            "narrateur|Amir s'accroupit près des galets.",
            "narrateur|Ils sont lisses, un peu froids.",
            "enfant-m|Un chemin, jusqu'au parasol.",
            "narrateur|Il aligne deux pierres, trop vite.",
            "narrateur|Nina lance un galet vers l'eau.",
            "enfant-f|Comme ça, maintenant !",
            "narrateur|Amir lance le sien, pour la suivre.",
            "narrateur|La file se casse, au milieu.",
            "enfant-m|Il est parti !",
            "papa|Le chemin voulait l'ombre.",
            "narrateur|Une pierre roule, hors de la file.",
            "narrateur|Amir souffle, les mains froides.",
            "narrateur|Nina se tait, les pieds dans l'écume.",
            "maman|Son silence te répond.",
            "narrateur|Le grain de parasol luit, sous la toile.",
            "papa|Vous faites comment, tous les deux ?",
        ],
        "question": [
            "narrateur|Amir aligne des pierres lisses.",
            "maman|Que pose-t-il ?",
        ],
        "qfields": {
            "expected_answer": "galets",
            "accepted_examples": "galets | galet | les galets | gris | file | pierres | pierre",
            "retry_prompt": "Amir pose des pierres lisses. Que pose-t-il ?",
        },
        "confirm": [
            "enfant-m|Des galets.",
            "maman|Oui.",
            "papa|Merci d'avoir vu le chemin.",
            "narrateur|Deux pierres tiennent, au soleil.",
            "enfant-m|Je continue, sans lancer.",
            "enfant-f|Moi, l'eau.",
            "narrateur|Nina recule vers l'écume, un pas.",
            "maman|La file n'est pas perdue.",
            "narrateur|Un grain de parasol reste au bord.",
        ],
    },
    3: {
        "lab": "l'ombre",
        "sons": "toile,vent",
        "emphasis": "ombre",
        "passage": [
            "narrateur|Amir rejoint le rond sous le parasol.",
            "narrateur|La toile jaune vibre, sèche.",
            "enfant-m|Je tiens l'ombre.",
            "narrateur|Il appuie le pied, des deux mains.",
            "narrateur|Nina tire le seau hors du rond.",
            "enfant-f|On va à l'eau !",
            "narrateur|Amir lâche le pied, pour la suivre.",
            "narrateur|L'ombre saute, le grain glisse.",
            "enfant-m|Elle part !",
            "papa|Le pied du parasol a bougé.",
            "narrateur|Un coin de toile claque, puis se tait.",
            "narrateur|Amir souffle, les mains chaudes.",
            "narrateur|Nina s'arrête au bord du rond.",
            "maman|Elle n'est pas entrée.",
            "narrateur|Amir reprend le pied, les mains chaudes.",
            "papa|Tu gardes l'ombre, comment ?",
        ],
        "question": [
            "narrateur|Le parasol fait un rond d'ombre.",
            "papa|De quelle couleur est le parasol ?",
        ],
        "qfields": {
            "expected_answer": "jaune",
            "accepted_examples": "jaune | parasol | parasol jaune | ombre | le jaune",
            "retry_prompt": "Le parasol fait l'ombre. De quelle couleur est-il ?",
        },
        "confirm": [
            "enfant-m|Jaune.",
            "papa|Oui.",
            "maman|Merci d'avoir repris le pied.",
            "narrateur|Le rond d'ombre se tient, un moment.",
            "enfant-m|Nina a une place.",
            "enfant-f|Au bord.",
            "narrateur|La toile jaune ne claque plus.",
            "papa|Le grain de parasol a cessé de glisser.",
            "narrateur|Amir garde le pied, sans lâcher.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|La colline de sable attend un geste.",
        "maman|Le seau, le filet, ou le livre ?",
        "papa|Qu'est-ce qui aide le château ?",
    ],
    2: [
        "narrateur|Le chemin de galets n'est pas fini.",
        "papa|Le seau, le filet, ou le livre ?",
        "maman|Qu'est-ce qui porte les pierres ?",
    ],
    3: [
        "narrateur|Le rond jaune veut tenir, un peu.",
        "maman|Le seau, le filet, ou le livre ?",
        "papa|Qu'est-ce qui garde l'ombre ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "seau,sable",
        "emphasis": "seau",
        "passage": [
            "narrateur|Amir prend le seau rouge, près de la colline.",
            "narrateur|Le plastique brûle un peu les doigts.",
            "enfant-m|De l'eau, pour le château.",
            "narrateur|Nina plonge le seau dans la flaque.",
            "narrateur|L'eau tiède tape contre le bord.",
            "enfant-f|Je le porte, jusqu'à la mer !",
            "narrateur|Elle tire, trop fort.",
            "narrateur|Le seau penche, le sable rentre.",
            "enfant-m|Il va partir !",
            "papa|Si tu cours, l'ombre te quitte.",
            "narrateur|Le grain de parasol glisse, au bord.",
            "narrateur|Amir refuse de foncer.",
            "maman|Nina a le seau.",
            "papa|Vous faites comment ?",
        ],
    },
    (1, 2): {
        "sons": "filet,sable",
        "emphasis": "filet",
        "passage": [
            "narrateur|Amir traîne le filet sur le sable chaud.",
            "narrateur|Les mailles sentent le sel, rêche.",
            "enfant-m|Du sable mouillé, pour la tour.",
            "narrateur|Nina tire le manche vers l'écume.",
            "enfant-f|Là-bas, maintenant !",
            "narrateur|Le vent gonfle le filet, trop fort.",
            "narrateur|Les mailles emportent Amir d'un pas.",
            "enfant-m|Il me tire !",
            "papa|Le filet veut la mer, pas le château.",
            "narrateur|Le grain de parasol penche, minuscule.",
            "narrateur|Amir plante les pieds, refuse de courir.",
            "maman|Nina a le manche.",
            "narrateur|Elle s'arrête, sans un mot.",
            "papa|Vous faites comment ?",
        ],
    },
    (1, 3): {
        "sons": "page,vent",
        "emphasis": "livre",
        "passage": [
            "narrateur|Amir ouvre le livre, près de la colline.",
            "narrateur|Un coin de page est mouillé.",
            "narrateur|Un crabe rouge est dessiné, large.",
            "enfant-m|Un château crabe !",
            "enfant-f|On le fait au soleil !",
            "narrateur|Nina emporte le livre hors de l'ombre.",
            "narrateur|Le vent tourne les pages, trop vite.",
            "enfant-m|Le crabe part !",
            "papa|Le sable rentre dans le pli.",
            "narrateur|Le grain de parasol luit, loin du livre.",
            "narrateur|Amir tend la main, puis la retire.",
            "maman|Il n'a pas couru.",
            "narrateur|Nina serre le papier, muette.",
            "papa|Vous faites comment ?",
        ],
    },
    (2, 1): {
        "sons": "seau,galet",
        "emphasis": "seau",
        "passage": [
            "narrateur|Amir glisse des galets dans le seau.",
            "narrateur|Ils sonnent, secs, contre le plastique.",
            "enfant-m|Trop lourd, pour moi.",
            "enfant-f|On les jette à l'eau !",
            "narrateur|Nina soulève le seau, penche.",
            "narrateur|Deux galets tombent hors du chemin.",
            "enfant-m|Ma file !",
            "papa|Le seau voulait la mer.",
            "narrateur|Le grain de parasol tremble sous la toile.",
            "narrateur|Amir pose une pierre, sans courir.",
            "maman|Nina a le seau, trop plein.",
            "narrateur|Elle se tait, les bras tendus.",
            "papa|Vous faites comment ?",
        ],
    },
    (2, 2): {
        "sons": "filet,vague",
        "emphasis": "filet",
        "passage": [
            "narrateur|Amir plonge le filet dans l'écume.",
            "narrateur|Une vague courte mouille les mailles.",
            "narrateur|Un galet lisse reste pris, rond.",
            "enfant-m|Je l'ai !",
            "enfant-f|Le prochain, plus loin !",
            "narrateur|Nina tire vers la vague suivante.",
            "narrateur|Le filet goutte, lourd, hors du chemin.",
            "enfant-m|Il m'emmène !",
            "papa|L'écume ruse, plus que le premier jet.",
            "narrateur|Le grain de parasol reste sous le jaune.",
            "narrateur|Amir lâche un peu le manche.",
            "maman|Nina avance.",
            "narrateur|Amir recule d'un pas.",
            "papa|Vous faites comment ?",
        ],
    },
    (2, 3): {
        "sons": "page,galet",
        "emphasis": "livre",
        "passage": [
            "narrateur|Amir pose le livre au départ du chemin.",
            "narrateur|Un galet plat tient la page ouverte.",
            "narrateur|Des galets de couleurs sont dessinés.",
            "enfant-m|Le gris, comme le mien.",
            "enfant-f|On cherche le bleu, dans l'eau !",
            "narrateur|Nina prend le livre, court un pas.",
            "narrateur|Le vent veut emporter la page.",
            "enfant-m|Le gris s'envole !",
            "papa|Le chemin reste ici, le livre aussi.",
            "narrateur|Le grain de parasol brille, au-dessus.",
            "narrateur|Amir rattrape le galet plat, sans courir.",
            "maman|Nina a fermé les mains sur le papier.",
            "papa|Vous faites comment ?",
        ],
    },
    (3, 1): {
        "sons": "seau,toile",
        "emphasis": "seau",
        "passage": [
            "narrateur|Amir pose le seau sur le pied du parasol.",
            "narrateur|Le plastique est frais, à l'ombre.",
            "enfant-m|Il tient !",
            "papa|Le seau pèse, juste assez.",
            "narrateur|Nina soulève le seau, pour l'eau.",
            "enfant-f|Je le prends, maintenant !",
            "narrateur|Le pied du parasol penche, tout seul.",
            "narrateur|L'ombre saute, le grain glisse.",
            "enfant-m|L'ombre part avec le seau !",
            "maman|Si le seau s'en va, le rond s'en va.",
            "narrateur|Amir pose les deux mains sur le pied.",
            "narrateur|Il refuse de lâcher.",
            "papa|Vous faites comment ?",
        ],
    },
    (3, 2): {
        "sons": "filet,toile",
        "emphasis": "filet",
        "passage": [
            "narrateur|Amir accroche le filet à une tige.",
            "narrateur|Les mailles font un second toit, léger.",
            "enfant-m|Plus d'ombre !",
            "enfant-f|On le met sur l'eau !",
            "narrateur|Nina tire les mailles vers la mer.",
            "narrateur|L'ombre rayée se déchire, trop vite.",
            "enfant-m|Le toit part !",
            "papa|Le filet voulait devenir voile.",
            "narrateur|Le grain de parasol glisse vers le vide.",
            "narrateur|Amir tient la tige, sans courir.",
            "maman|Nina a les mailles, toi la tige.",
            "narrateur|Elle s'arrête, les bras hauts.",
            "papa|Vous faites comment ?",
        ],
    },
    (3, 3): {
        "sons": "page,toile",
        "emphasis": "livre",
        "passage": [
            "narrateur|Amir s'assoit avec le livre, dans le rond.",
            "narrateur|La page sent le sel, un peu.",
            "enfant-m|On lit ici, Nina ?",
            "enfant-f|Au soleil, c'est mieux !",
            "narrateur|Nina tire le livre hors de l'ombre.",
            "narrateur|Le vent tourne trois pages, trop fort.",
            "enfant-m|Le crabe s'envole !",
            "papa|Hors du rond, le papier fuit.",
            "narrateur|Le grain de parasol reste, lui.",
            "narrateur|Amir pose un doigt sur le pied.",
            "narrateur|Il refuse de se lever.",
            "maman|Nina a le livre, ouvert.",
            "papa|Vous faites comment ?",
        ],
    },
}

T3_CHOICE = {
    1: [
        "narrateur|Nina tient le seau, vers l'eau.",
        "narrateur|Amir sent l'ombre sur ses genoux.",
        "papa|Tu regardes, plus tard, ou un non ?",
    ],
    2: [
        "narrateur|Nina tire le filet, vers l'écume.",
        "narrateur|Amir sent l'ombre sur ses genoux.",
        "maman|Tu regardes, plus tard, ou un non ?",
    ],
    3: [
        "narrateur|Nina ouvre le livre, hors de l'ombre.",
        "narrateur|Amir sent l'ombre sur ses genoux.",
        "papa|Tu regardes, plus tard, ou un non ?",
    ],
}

T3_SONS = {
    (1, 1): "seau,sable",
    (1, 2): "seau,silence",
    (1, 3): "seau,toile",
    (2, 1): "filet,vague",
    (2, 2): "filet,silence",
    (2, 3): "filet,toile",
    (3, 1): "page,vent",
    (3, 2): "page,silence",
    (3, 3): "page,toile",
}

T3_EMPH = {1: "Je regarde", 2: "Plus tard", 3: "Non"}


def t3_pass(a: int, b: int, c: int) -> list[str]:
    rows = {
        (1, 1, 1): [
            "enfant-m|Je regarde.",
            "narrateur|Amir s'assoit près de la colline.",
            "narrateur|Nina verse l'eau, seule.",
            "narrateur|Il suit le filet d'eau des yeux.",
            "enfant-f|Tu vois ?",
            "enfant-m|Oui.",
            "papa|La tour boit, sans se casser.",
            "narrateur|Nina se tait, seau vide à la main.",
            "narrateur|Le grain de parasol tient, au bord.",
            "narrateur|Amir n'a pas bougé les pieds.",
        ],
        (1, 1, 2): [
            "enfant-m|Plus tard.",
            "narrateur|Amir pose le seau à l'ombre du château.",
            "enfant-m|Je te le garde.",
            "narrateur|Nina recule vers la flaque, un pas.",
            "maman|L'eau attend, dans le plastique.",
            "narrateur|Nina ne dit rien.",
            "narrateur|Un filet d'eau brille au bord.",
            "narrateur|Le grain de parasol cesse de glisser.",
            "narrateur|La colline reste sèche, un moment.",
            "papa|Le seau est là, pour après.",
        ],
        (1, 1, 3): [
            "enfant-m|Non.",
            "narrateur|Amir pose le seau, d'un coup.",
            "narrateur|Il recule, les deux pieds dans l'ombre.",
            "narrateur|Nina s'arrête, la main ouverte.",
            "enfant-f|Ah.",
            "papa|Il a tenu le seau, puis l'a posé.",
            "narrateur|Amir verse une petite gorgée, seul.",
            "narrateur|La tour tient, plus basse, plus ferme.",
            "narrateur|Le grain de parasol se cale, sous la toile.",
            "maman|Nina a vu le geste.",
        ],
        (1, 2, 1): [
            "enfant-m|Je regarde.",
            "narrateur|Amir reste près de la colline, les pieds lourds.",
            "narrateur|Nina dépose la motte, contre le sable.",
            "narrateur|Il suit le manche des yeux, sans le prendre.",
            "enfant-f|C'est mouillé.",
            "enfant-m|Oui.",
            "maman|Le sable mouillé colle, lourd.",
            "narrateur|Le filet s'affaisse, vide, sur le chaud.",
            "narrateur|Le grain de parasol luit, au-dessus du manche.",
            "papa|Tu as tout vu, sans bouger.",
        ],
        (1, 2, 2): [
            "enfant-m|Plus tard.",
            "narrateur|Amir laisse le filet ouvert, à côté.",
            "enfant-m|Ta motte est là.",
            "narrateur|Nina s'éloigne vers une flaque, un instant.",
            "papa|Les mailles attendent, salées.",
            "narrateur|Nina se tait, le dos à la colline.",
            "narrateur|Une maille garde un grain, pris.",
            "narrateur|Le grain de parasol ne penche plus.",
            "maman|Le château peut attendre, lui aussi.",
            "narrateur|Amir s'assoit, l'ombre aux genoux.",
        ],
        (1, 2, 3): [
            "enfant-m|Non.",
            "narrateur|Amir pose le filet, plat, sur le sable.",
            "narrateur|Il recule d'un pas, vers le parasol.",
            "narrateur|Nina lâche le manche, surprise.",
            "enfant-f|Bon.",
            "papa|Il a posé le filet, et ça suffit.",
            "narrateur|Amir tasse la motte, du poing, seul.",
            "narrateur|Une petite tour se tient, ronde.",
            "narrateur|Le grain de parasol se cale, net.",
            "maman|Nina a vu qu'il ne venait pas.",
        ],
        (1, 3, 1): [
            "enfant-m|Je regarde.",
            "narrateur|Amir pince le sable, comme les pinces.",
            "narrateur|Nina tient le livre, hors du rond.",
            "narrateur|Il suit le crabe du regard, sans se lever.",
            "enfant-f|Deux pinces.",
            "enfant-m|Oui.",
            "papa|Deux petites pinces, dans le grain.",
            "narrateur|La page reste ouverte, entre eux.",
            "narrateur|Le grain de parasol brille, au-dessus du dessin.",
            "maman|Tu as lu, sans quitter l'ombre.",
        ],
        (1, 3, 2): [
            "enfant-m|Plus tard.",
            "narrateur|Amir laisse le livre ouvert, sur le sable.",
            "enfant-m|Le crabe t'attend.",
            "narrateur|Nina part vers la flaque, puis s'arrête.",
            "maman|Le dessin ne bouge plus.",
            "narrateur|Un grain reste dans le pli de la page.",
            "narrateur|Le grain de parasol tient, au bord.",
            "papa|La page est là, pour après.",
            "narrateur|Amir garde les genoux sous le jaune.",
            "enfant-f|Après, alors.",
        ],
        (1, 3, 3): [
            "enfant-m|Non.",
            "narrateur|Amir referme presque le livre, d'une main.",
            "narrateur|Il recule sous le parasol, le papier contre lui.",
            "narrateur|Nina ouvre la bouche, puis la referme.",
            "papa|Il a dit non, avec les pieds.",
            "narrateur|Amir fait une pince, seul, dans le grain.",
            "narrateur|Le château crabe est petit, rouge de sable.",
            "narrateur|Le grain de parasol se cale, sous la toile.",
            "maman|Nina a les mains dans le dos.",
            "narrateur|La page ne claque plus.",
        ],
        (2, 1, 1): [
            "enfant-m|Je regarde.",
            "narrateur|Amir pose un galet, puis un autre.",
            "narrateur|Nina tient le seau, trop plein.",
            "narrateur|Il compte des yeux, sans les prendre.",
            "enfant-f|Trois.",
            "enfant-m|Oui.",
            "papa|Le chemin avance, pierre par pierre.",
            "narrateur|Le seau s'allège, un peu.",
            "narrateur|Le grain de parasol luit, au bout de la file.",
            "maman|Tu as vu chaque pierre, sans courir.",
        ],
        (2, 1, 2): [
            "enfant-m|Plus tard.",
            "narrateur|Amir laisse un galet hors du seau.",
            "enfant-m|Celui-là, pour toi.",
            "narrateur|Nina s'essuie un pied, dans l'écume.",
            "maman|La pierre lisse attend, au soleil.",
            "narrateur|Nina se tait, seau contre la hanche.",
            "narrateur|Le seau tient trois galets, pas plus.",
            "narrateur|Le grain de parasol cesse de trembler.",
            "papa|Le chemin peut attendre une pierre.",
            "narrateur|Amir s'assoit, face à l'ombre.",
        ],
        (2, 1, 3): [
            "enfant-m|Non.",
            "narrateur|Amir pose le seau, d'un coup, sur le sable.",
            "narrateur|Il recule vers le parasol, les mains vides.",
            "narrateur|Nina s'arrête, le seau à terre.",
            "enfant-f|D'accord.",
            "papa|Il a posé le seau, et la file tient.",
            "narrateur|Amir finit une petite file, seul.",
            "narrateur|Elle s'arrête avant le parasol, assez.",
            "narrateur|Le grain de parasol se cale, net.",
            "maman|Nina reste dans l'eau, jusqu'aux chevilles.",
        ],
        (2, 2, 1): [
            "enfant-m|Je regarde.",
            "narrateur|Amir tire le galet hors des mailles.",
            "narrateur|Nina suit la goutte qui tombe.",
            "narrateur|Il ne la rejoint pas, dans l'écume.",
            "enfant-f|Il brille.",
            "enfant-m|Oui.",
            "maman|Il brille, mouillé.",
            "narrateur|Le filet s'égoutte, vers le chemin.",
            "narrateur|Le grain de parasol tient, au-dessus de la goutte.",
            "papa|Tu as vu la pierre, sans y aller.",
        ],
        (2, 2, 2): [
            "enfant-m|Plus tard.",
            "narrateur|Amir laisse le galet dans le filet.",
            "enfant-m|Je te le garde mouillé.",
            "narrateur|Nina recule d'une vague, puis s'arrête.",
            "papa|Les mailles tiennent la pierre.",
            "narrateur|Nina ne dit rien, les pieds froids.",
            "narrateur|Une goutte de sel perle, au bout.",
            "narrateur|Le grain de parasol ne glisse plus.",
            "maman|La vague peut attendre, un moment.",
            "narrateur|Amir s'assoit, le filet à l'ombre.",
        ],
        (2, 2, 3): [
            "enfant-m|Non.",
            "narrateur|Amir pose le filet, plat, hors de l'eau.",
            "narrateur|Il recule, un pied dans l'ombre.",
            "narrateur|Nina lâche les mailles, surprise.",
            "enfant-f|Bon.",
            "papa|Il a posé le filet, face à la vague.",
            "narrateur|Amir pose le galet du filet, seul.",
            "narrateur|La ligne va jusqu'à l'ombre, presque.",
            "narrateur|Le grain de parasol se cale, sous le jaune.",
            "maman|Nina joue avec une vague, plus loin.",
        ],
        (2, 3, 1): [
            "enfant-m|Je regarde.",
            "narrateur|Amir montre le gris du livre, du doigt.",
            "narrateur|Nina compare, des yeux, avec la pierre.",
            "narrateur|Il ne se lève pas, pour l'eau.",
            "enfant-f|Le même.",
            "enfant-m|Oui.",
            "papa|C'est le même gris.",
            "narrateur|Le galet plat tient la page.",
            "narrateur|Le grain de parasol brille, sur le dessin.",
            "maman|Tu as comparé, sans quitter le chemin.",
        ],
        (2, 3, 2): [
            "enfant-m|Plus tard.",
            "narrateur|Amir laisse le livre ouvert, sous le galet.",
            "enfant-m|Le gris t'attend.",
            "narrateur|Nina s'éloigne le long de l'eau.",
            "maman|Le vent n'emporte plus la page.",
            "narrateur|Nina se tait, une pierre à la main.",
            "narrateur|Le dessin reste au soleil, plat.",
            "narrateur|Le grain de parasol tient, au-dessus.",
            "papa|La page est là, pour après.",
            "narrateur|Amir garde le galet plat, comme un poids.",
        ],
        (2, 3, 3): [
            "enfant-m|Non.",
            "narrateur|Amir referme le livre, d'une paume.",
            "narrateur|Il recule sous le parasol, le papier contre lui.",
            "narrateur|Nina ouvre la main, vide.",
            "papa|Il a dit non, en fermant la page.",
            "narrateur|Amir choisit le gris, seul, dans le sable.",
            "narrateur|Il le pose en tête du chemin.",
            "narrateur|Le grain de parasol se cale, au bord.",
            "maman|Nina a tourné le dos, vers la mer.",
            "narrateur|La page se tait, contre sa chemise.",
        ],
        (3, 1, 1): [
            "enfant-m|Je regarde.",
            "narrateur|Amir s'assoit dans le rond, près du seau.",
            "narrateur|Nina reste au bord, les yeux sur la toile.",
            "narrateur|Il ne lève pas le seau.",
            "enfant-f|L'ombre.",
            "enfant-m|Oui.",
            "papa|Le pied ne bouge plus.",
            "narrateur|L'ombre couvre les genoux d'Amir.",
            "narrateur|Le grain de parasol tient, au-dessus du seau.",
            "maman|Tu as vu la toile, sans la quitter.",
        ],
        (3, 1, 2): [
            "enfant-m|Plus tard.",
            "narrateur|Amir laisse un coin d'ombre, vide.",
            "enfant-m|Ta place est fraîche.",
            "narrateur|Nina recule au soleil, un moment.",
            "maman|Le seau tient le pied.",
            "narrateur|Nina se tait, le front chaud.",
            "narrateur|Un bout de serviette attend, à l'ombre.",
            "narrateur|Le grain de parasol cesse de glisser.",
            "papa|Le rond est là, pour après.",
            "narrateur|Amir garde les deux mains sur le pied.",
        ],
        (3, 1, 3): [
            "enfant-m|Non.",
            "narrateur|Amir plaque les deux mains sur le pied.",
            "narrateur|Il recule le seau, sous le jaune.",
            "narrateur|Nina s'arrête, hors du rond.",
            "enfant-f|Ah.",
            "papa|Il a tenu le pied, et posé le seau.",
            "narrateur|Amir s'assoit, seul, sous le jaune.",
            "narrateur|Le seau reste lourd, sur le pied.",
            "narrateur|Le grain de parasol se cale, contre le pouce.",
            "maman|Nina marche au soleil, tout près.",
        ],
        (3, 2, 1): [
            "enfant-m|Je regarde.",
            "narrateur|Amir s'allonge sous les mailles rayées.",
            "narrateur|Nina suit la goutte, jusqu'au sable.",
            "narrateur|Il ne tire pas le filet.",
            "enfant-f|Elle tombe.",
            "enfant-m|Oui.",
            "maman|Elle tombe, lente.",
            "narrateur|Le filet fait une ombre étroite, nette.",
            "narrateur|Le grain de parasol luit, entre les mailles.",
            "papa|Tu as vu la goutte, sans bouger le toit.",
        ],
        (3, 2, 2): [
            "enfant-m|Plus tard.",
            "narrateur|Amir laisse le filet tendu, pour elle.",
            "enfant-m|Le second toit t'attend.",
            "narrateur|Nina s'éloigne vers la flaque, un instant.",
            "papa|Les mailles sèchent, salées.",
            "narrateur|Nina se tait, une maille entre les doigts.",
            "narrateur|Une ombre rayée reste sur le sable.",
            "narrateur|Le grain de parasol tient, au centre.",
            "maman|Le toit est là, pour après.",
            "narrateur|Amir garde la tige, sans la lâcher.",
        ],
        (3, 2, 3): [
            "enfant-m|Non.",
            "narrateur|Amir tient la tige, des deux mains.",
            "narrateur|Il recule le filet, sous le parasol.",
            "narrateur|Nina lâche les mailles, les bras bas.",
            "enfant-f|Bon.",
            "papa|Il a tenu la tige, et dit non.",
            "narrateur|Amir reste sous le filet, seul.",
            "narrateur|La goutte a séché, en rond.",
            "narrateur|Le grain de parasol se cale, sous les mailles.",
            "maman|Nina court un peu, hors de l'ombre.",
        ],
        (3, 3, 1): [
            "enfant-m|Je regarde.",
            "narrateur|Amir lit le crabe, bas, pour les deux.",
            "narrateur|Nina écoute depuis le bord de l'ombre.",
            "narrateur|Il ne tend pas le livre.",
            "enfant-f|J'entends.",
            "enfant-m|Oui.",
            "papa|La page ne s'envole plus.",
            "narrateur|Le doigt d'Amir tient le coin.",
            "narrateur|Le grain de parasol brille, sur le crabe.",
            "maman|Tu as lu, sans quitter le rond.",
        ],
        (3, 3, 2): [
            "enfant-m|Plus tard.",
            "narrateur|Amir laisse le livre ouvert, sur les genoux.",
            "enfant-m|Le crabe t'attend.",
            "narrateur|Nina part vers l'eau, puis se retourne.",
            "maman|Le vent n'a plus la page.",
            "narrateur|Nina se tait, une goutte aux cheveux.",
            "narrateur|Un coin d'ombre reste libre, à côté.",
            "narrateur|Le grain de parasol tient, au-dessus du papier.",
            "papa|La page est là, pour après.",
            "narrateur|Amir garde le doigt sur le pied.",
        ],
        (3, 3, 3): [
            "enfant-m|Non.",
            "narrateur|Amir referme le livre, contre sa chemise.",
            "narrateur|Il recule sous le jaune, les deux pieds au frais.",
            "narrateur|Nina s'arrête hors du rond, sèche.",
            "enfant-f|D'accord.",
            "papa|Il a fermé la page, et gardé l'ombre.",
            "narrateur|Amir garde le crabe, un moment.",
            "narrateur|Le parasol jaune ne tremble plus.",
            "narrateur|Le grain de parasol se cale, au bord.",
            "maman|Nina est hors du rond, et ça va.",
        ],
    }
    return rows[(a, b, c)]


LAST = {
    (1, 1, 1): "Le grain de parasol tient, au-dessus du château.",
    (1, 1, 2): "Le seau vide veille le grain de parasol, au frais.",
    (1, 1, 3): "Amir tient le pied, le grain de parasol à plat.",
    (1, 2, 1): "Une maille du filet porte le grain de parasol.",
    (1, 2, 2): "Le filet sèche, le grain de parasol au bord.",
    (1, 2, 3): "Amir a posé le filet, le grain de parasol calme.",
    (1, 3, 1): "La page ouverte reflète le grain de parasol.",
    (1, 3, 2): "Le livre attend, le grain de parasol sur la toile.",
    (1, 3, 3): "Amir referme le livre, le grain de parasol à sa place.",
    (2, 1, 1): "Un galet gris reflète le grain de parasol.",
    (2, 1, 2): "Le seau de pierres veille le grain de parasol.",
    (2, 1, 3): "La file s'arrête, le grain de parasol tient.",
    (2, 2, 1): "Une goutte du filet évite le grain de parasol.",
    (2, 2, 2): "Le galet mouillé sèche près du grain de parasol.",
    (2, 2, 3): "Amir a dit non, le grain de parasol ne glisse plus.",
    (2, 3, 1): "Le gris du livre touche le grain de parasol.",
    (2, 3, 2): "La page attend, le grain de parasol au-dessus.",
    (2, 3, 3): "Le livre se tait, le grain de parasol au bord.",
    (3, 1, 1): "Le seau pèse, le grain de parasol ne bouge plus.",
    (3, 1, 2): "Le coin d'ombre garde le grain de parasol.",
    (3, 1, 3): "Amir serre le pied, le grain de parasol contre le pouce.",
    (3, 2, 1): "L'ombre rayée entoure le grain de parasol.",
    (3, 2, 2): "Les mailles sèchent, le grain de parasol au centre.",
    (3, 2, 3): "Amir reste, le grain de parasol sous la toile.",
    (3, 3, 1): "Le crabe du livre regarde le grain de parasol.",
    (3, 3, 2): "Deux genoux au frais, le grain de parasol entre eux.",
    (3, 3, 3): "Le parasol jaune tient, le grain de parasol au bord.",
}

END_SONS = {1: "oiseau,vague", 2: "galet,vague", 3: "toile,vague"}


def ending(a: int, b: int, c: int) -> list[str]:
    last = LAST[(a, b, c)]
    table = {
        1: {  # T2 seau
            1: [  # regarder
                "narrateur|Nina a versé, et Amir a tout vu.",
                "enfant-m|Tu as vu l'eau.",
                "enfant-f|Oui.",
                "papa|Le seau a travaillé, sans courir.",
                "maman|Merci d'avoir regardé, Amir.",
                "narrateur|Ils se reculent sous le parasol jaune.",
            ],
            2: [
                "narrateur|Nina revient, les joues salées.",
                "enfant-f|Maintenant ?",
                "enfant-m|Oui.",
                "narrateur|Elle prend le seau, maladroite.",
                "papa|Vous avez pris le temps.",
                "maman|Merci, tous les deux.",
                "narrateur|Ils s'assoient dans le rond jaune.",
            ],
            3: [
                "narrateur|Le seau reste posé, et ça suffit.",
                "enfant-m|Pour moi, c'est assez.",
                "papa|Oui.",
                "narrateur|Nina joue plus loin, dans l'eau.",
                "maman|L'ombre t'appartient, ce matin.",
                "narrateur|Amir s'assoit dans le rond frais.",
            ],
        },
        2: {  # T2 filet
            1: [
                "narrateur|Nina a vu les mailles, jusqu'au bout.",
                "enfant-m|Tu as vu.",
                "enfant-f|Oui.",
                "papa|Le filet a travaillé.",
                "maman|Merci d'avoir regardé, Amir.",
                "narrateur|Ils gagnent l'ombre du parasol, lents.",
            ],
            2: [
                "narrateur|Nina revient vers les mailles.",
                "enfant-f|Je tiens le manche ?",
                "enfant-m|Oui.",
                "papa|Vous avez attendu le bon moment.",
                "maman|Merci.",
                "narrateur|Le filet s'affaisse, vide, au soleil.",
            ],
            3: [
                "narrateur|Le filet repose, salé, sous le jaune.",
                "enfant-m|Ça suffit.",
                "maman|Oui.",
                "narrateur|Nina court hors des mailles, légère.",
                "papa|Tu as un toit, à toi.",
                "narrateur|Amir s'allonge, les rayures sur les bras.",
            ],
        },
        3: {  # T2 livre
            1: [
                "narrateur|Nina a suivi le dessin, des yeux.",
                "enfant-m|Tu as vu le crabe.",
                "enfant-f|Oui.",
                "papa|La page a tenu.",
                "maman|Merci d'avoir regardé, Amir.",
                "narrateur|Ils laissent le livre ouvert, à l'ombre.",
            ],
            2: [
                "narrateur|Nina revient, une goutte aux cheveux.",
                "enfant-f|Le crabe ?",
                "enfant-m|Il est là.",
                "papa|Vous l'avez lu plus tard.",
                "maman|Merci.",
                "narrateur|Amir recommence la page, bas.",
            ],
            3: [
                "narrateur|Le livre reste presque fermé, sur les genoux.",
                "enfant-m|Le crabe est à moi, un moment.",
                "papa|Oui.",
                "narrateur|Nina est hors du rond, sèche.",
                "maman|L'ombre te va, seule.",
                "narrateur|Amir pose la page contre sa chemise.",
            ],
        },
    }
    # T1-specific middle image so 27 endings differ even before LAST
    place = {
        1: "La colline de sable garde un peu d'eau.",
        2: "La file de galets mène jusqu'au jaune.",
        3: "Le rond d'ombre couvre les genoux d'Amir.",
    }[a]
    body = table[b][c][:]
    # inject unique T1 line after first narrator
    body.insert(1, f"narrateur|{place}")
    body.append(f"narrateur|{last}")
    return body


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "vague,toile",
        {"emphasis": "grain de parasol"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le sable", "les galets", "l'ombre"), "pause_before": 200},
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
            {"emphasis": "grain de parasol"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("le seau", "le filet", "le livre"), "pause_before": 200},
        )
        for b in (1, 2, 3):
            bse = f"{base}_T0002_P000{b}"
            out_chunks[bse] = voice(
                by_src[bse], T2[(a, b)]["passage"], "obstacle", T2[(a, b)]["sons"],
                {"emphasis": T2[(a, b)]["emphasis"]},
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab("regarder", "plus tard", "un non"), "pause_before": 200},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], t3_pass(a, b, c), "resolution", T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ending(a, b, c), "ending", END_SONS[a],
                    {"emphasis": "grain de parasol"},
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
        "plusieurs réponses",
        "on propose",
        "on accepte",
        "regarder, c'est",
        "un non est possible",
        "bravo tu as",
        "bon travail",
        "nora",
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
        "celui où j'ai compris",
        "il faut attendre",
        "mission accomplie",
        "gouttes pendent",
        "coquille de crabe",
        "éclat de coquille",
        "fil pâle",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "amir" not in blob:
        raise SystemExit(f"{SID}: Amir absent")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "enfant-f|" not in blob:
        raise SystemExit(f"{SID}: enfant-f absent")
    if "grain de parasol" not in blob:
        raise SystemExit(f"{SID}: grain de parasol absent")

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
        if "grain de parasol" not in c["text"].lower():
            raise SystemExit(f"fin sans grain: {c['chunk_id']}")
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
        "# TREE-DIF-011 — Le parasol jaune et la réponse d'Amir\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.BES.002 — besoin / limite vécue "
        "(regarder, plus tard, un non) ; le non se voit, il n'est pas dit en règle\n"
        "- **Personnages :** Amir, Nina, papa, maman\n"
        "- **Lieu :** plage, sous un parasol jaune\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La toile jaune chauffe. Un grain de parasol tient au bord. "
        "Amir veut garder l'ombre avant que Nina emporte le seau. "
        "Nina veut jouer maintenant. Il court : le pied penche, l'ombre saute, "
        "le grain glisse. Sable, galets ou ombre : les trois partent. "
        "Seau, filet ou livre : l'objet ruse, tire vers l'eau. "
        "Amir refuse de foncer. Il regarde, dit plus tard, ou dit non "
        "(poser le seau, reculer, tenir le pied). Le grain de parasol se cale.\n\n"
        "## Vécu\n\n"
        "Amir veut l'ombre **maintenant**. Nina veut l'eau **maintenant**. "
        "Première idée : courir avec elle. Ça rate. "
        "Chaque choix change l'obstacle et le climax (seau qui part, filet-voile, "
        "livre qui fuit). La leçon se voit : regarder sans bouger, poser pour plus tard, "
        "ou reculer. Fin : grain de parasol + rond jaune + image unique du chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Nora / slogans « on propose / on accepte plusieurs réponses » / "
        "coquille de crabe jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Héros Amir (`enfant-m`), Nina (`enfant-f`), rythmes distincts, "
        "silence = réponse.\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'action. 9 T2, 27 T3, 27 fins.\n"
        "- Indice unique dès l'ouverture : le grain de parasol, payé aux 27 fins.\n"
        "- Merci vécu. Question d'adulte. Un « en ce moment ».\n"
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
