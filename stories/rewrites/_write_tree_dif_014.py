#!/usr/bin/env python3
"""TREE-DIF-014 — Le panier de Mila et la pomme du haut (F-NAR-019, N2, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-014"
N2 = 15
TITLE = "Le panier de Mila et la pomme du haut"
FIL = (
    "À la table du tronc, un rond de jus attend la pomme du haut. "
    "Mila la veut pour le panier, pour le goûter, maintenant. "
    "Elle saute seule : l'air seulement. Nino arrive, plus petit, sans se presser. "
    "Un grain de sève luit sur l'écorce, à sa hauteur. "
    "T1 = panier / nappe / tabouret, les trois partent. "
    "T2 = branches basses / herbe haute / banc. "
    "La pomme manque au moment de la prendre. Mila refuse de foncer. "
    "T3 = neuf façons à deux hauteurs. Le grain de sève paie le début."
)
CHARS = "Mila, Nino, papa, maman"
SETTING = "jardin, sous le pommier"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain de sève",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_rond_de_jus_attend_la_pomme_du_haut; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_a_pris; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "grain de sève",
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=la_première_idée_a_raté_la_pomme_manque; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=Mila_propose_Nino_prend_son_temps; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_et_découragement; intensite=2; destinataire=enfant; sous_texte=le_silence_de_Nino_est_une_réponse; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "grain de sève",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=faire_avec_Nino_pas_toute_seule; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain de sève",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_de_sève_paie_le_début_le_rond_se_remplit; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Sur la nappe du jardin, un rond de jus attend.",
    "narrateur|Mila y pose un doigt, tout autour.",
    "enfant-f|Ici, la pomme du haut.",
    "narrateur|Papa coupe une pomme tombée, près du tronc.",
    "narrateur|Ça sent le fruit, tiède, sous le pommier.",
    "narrateur|Un bourdon frotte l'écorce, puis s'envole.",
    "narrateur|Sur le tronc, un grain de sève luit.",
    "enfant-f|Il colle, papa.",
    "papa|Le grain de sève, tu l'as vu ?",
    "maman|Nino arrive, l'herbe à ses genoux.",
    "enfant-m|On prend la rouge ?",
    "enfant-f|Moi, je saute !",
    "narrateur|Mila saute, et ses doigts frôlent l'air.",
    "narrateur|La pomme du haut reste trop loin.",
    "narrateur|Le sourire de Mila disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "narrateur|En ce moment, le panier reste vide.",
    "papa|Je m'accroupis, à votre hauteur.",
    "maman|Merci, tu as montré le grain de sève.",
    "narrateur|Nino pose un doigt sur le tronc, sans un mot.",
    "papa|On prend les affaires, alors ?",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent sous le pommier.",
    "narrateur|Le panier, la nappe, et le tabouret.",
    "maman|Tu prends quoi d'abord, Mila ?",
]

T1 = {
    1: {
        "lab": "le panier",
        "sons": "panier,anse",
        "emphasis": "panier",
        "passage": [
            "narrateur|Mila attrape l'anse du panier, trop vite.",
            "enfant-f|Je la cueille, d'en haut.",
            "narrateur|Elle lève le panier vers la pomme du haut.",
            "narrateur|Le panier tremble, trop bas.",
            "enfant-f|Nino, pousse !",
            "narrateur|Nino pose une main sur l'anse, stop.",
            "narrateur|Il ne dit rien.",
            "papa|Sa main a parlé, Mila.",
            "narrateur|Le sourire de Mila s'en va.",
            "maman|Je me baisse, à votre hauteur.",
            "papa|La nappe et le tabouret viennent aussi.",
            "narrateur|Papa glisse le tout près des sandales.",
            "enfant-f|On y va ?",
            "narrateur|Nino hoche la tête, tout petit.",
            "papa|Le panier d'abord, vous l'avez.",
        ],
        "question": [
            "narrateur|Mila a levé le panier, trop bas.",
            "maman|Elle a levé quoi, vers la pomme ?",
        ],
        "qfields": {
            "expected_answer": "panier",
            "accepted_examples": "panier | le panier | dans le panier | l'anse | l'anse du panier",
            "retry_prompt": "Mila a levé le panier. Elle a levé quoi ?",
        },
        "confirm": [
            "narrateur|Le panier penche, vide, contre la hanche.",
            "enfant-m|La rouge n'est pas dedans.",
            "enfant-f|Elle est trop haute.",
            "maman|Le grain de sève reste sur le tronc.",
            "papa|On avance sous les feuilles ?",
            "enfant-f|Oui, papa.",
            "narrateur|Nino suit, sans se presser.",
            "narrateur|Le rond de jus attend, sur la nappe.",
        ],
    },
    2: {
        "lab": "la nappe",
        "sons": "tissu,nappe",
        "emphasis": "nappe",
        "passage": [
            "narrateur|Mila déplie la nappe, comme un filet.",
            "enfant-f|Je l'attrape, d'en bas.",
            "narrateur|Elle tend le tissu vers la pomme du haut.",
            "narrateur|La nappe retombe, trop courte.",
            "enfant-f|Nino, tire !",
            "narrateur|Nino tient un coin, sans bouger.",
            "narrateur|Il ferme la bouche.",
            "maman|Son coin a parlé, Mila.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Je m'accroupis, près du tissu.",
            "maman|Le panier et le tabouret viennent aussi.",
            "narrateur|Maman les pose près des sandales.",
            "enfant-f|Tu viens, Nino ?",
            "narrateur|Nino lâche un tout petit oui.",
            "maman|La nappe d'abord, elle est prête.",
        ],
        "question": [
            "narrateur|Mila a tendu la nappe, trop courte.",
            "papa|Elle a tendu quoi, vers la pomme ?",
        ],
        "qfields": {
            "expected_answer": "nappe",
            "accepted_examples": "nappe | la nappe | le tissu | dans la nappe | le filet",
            "retry_prompt": "Mila a tendu la nappe. Elle a tendu quoi ?",
        },
        "confirm": [
            "narrateur|La nappe reste pliée, un peu, contre le bras.",
            "enfant-f|Le filet n'a rien pris.",
            "enfant-m|La rouge est trop loin.",
            "papa|Le grain de sève luit, trop bas pour elle.",
            "maman|On avance dans l'ombre ?",
            "enfant-m|Oui, maman.",
            "narrateur|Nino marche derrière, sans se presser.",
            "narrateur|Le rond de jus attend, à la table du tronc.",
        ],
    },
    3: {
        "lab": "le tabouret",
        "sons": "bois,tabouret",
        "emphasis": "tabouret",
        "passage": [
            "narrateur|Mila tire le tabouret, tout rêche.",
            "enfant-f|Je monte, toute seule.",
            "narrateur|Elle grimpe, les talons levés.",
            "narrateur|Le bois penche, et ses doigts frôlent l'air.",
            "enfant-f|Nino, tiens-moi !",
            "narrateur|Nino pose une paume sur le bois, stop.",
            "narrateur|Il ne dit rien.",
            "papa|Sa paume a parlé, Mila.",
            "narrateur|Le sourire de Mila s'en va.",
            "maman|Je me baisse, à votre hauteur.",
            "papa|Le panier et la nappe viennent aussi.",
            "narrateur|Il les pose près des sandales.",
            "enfant-f|On y va ?",
            "narrateur|Nino appuie sur le bois, tout petit.",
            "papa|Le tabouret d'abord, il est prêt.",
        ],
        "question": [
            "narrateur|Mila a tiré le tabouret, sous l'arbre.",
            "maman|Elle a tiré quoi, sous le pommier ?",
        ],
        "qfields": {
            "expected_answer": "tabouret",
            "accepted_examples": "tabouret | le tabouret | sur le tabouret | le bois | le siège",
            "retry_prompt": "Mila a tiré le tabouret. Elle a tiré quoi ?",
        },
        "confirm": [
            "narrateur|Le tabouret reste au pied, un peu de travers.",
            "enfant-m|Tu n'as pas touché la rouge.",
            "enfant-f|Mes doigts ont touché l'air.",
            "maman|Le grain de sève reste à ta hauteur, Nino.",
            "papa|On avance vers le tronc ?",
            "enfant-f|Oui.",
            "narrateur|Nino pousse le bois, sans se presser.",
            "narrateur|Le rond de jus attend, sur la table du tronc.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Dans le panier, le vide voyage.",
        "narrateur|Les branches basses font un tunnel vert.",
        "narrateur|L'herbe haute cache le sol.",
        "narrateur|Le banc du tronc est chaud.",
        "papa|On commence où, pour la pomme du haut ?",
    ],
    2: [
        "narrateur|Dans la nappe, le vide voyage.",
        "narrateur|Les branches basses font un tunnel vert.",
        "narrateur|L'herbe haute cache le sol.",
        "narrateur|Le banc du tronc est chaud.",
        "maman|On commence où, pour la pomme du haut ?",
    ],
    3: [
        "narrateur|Près du tabouret, le vide voyage.",
        "narrateur|Les branches basses font un tunnel vert.",
        "narrateur|L'herbe haute cache le sol.",
        "narrateur|Le banc du tronc est chaud.",
        "papa|On commence où, pour la pomme du haut ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "feuilles,panier",
        "emphasis": "branches",
        "passage": [
            "narrateur|L'anse du panier frotte une feuille.",
            "narrateur|Les branches basses tapent le front de Mila.",
            "enfant-f|J'y vais, vite !",
            "narrateur|Mila penche la tête, trop haute.",
            "enfant-m|Moi, je passe.",
            "narrateur|Nino glisse sous le vert, puis s'arrête.",
            "enfant-f|Prends-la !",
            "narrateur|Nino secoue la tête, sans un mot.",
            "narrateur|La pomme du haut n'est plus dans le ciel.",
            "narrateur|Une feuille rouge ment, entre les brindilles.",
            "papa|Elle manque, juste au moment de la prendre.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle observe le panier, écoute les feuilles.",
            "narrateur|Elle retrouve le grain de sève, sur le tronc.",
            "maman|Vous passez comment, sous le vert ?",
        ],
    },
    (2, 1): {
        "sons": "feuilles,tissu",
        "emphasis": "brindille",
        "passage": [
            "narrateur|La nappe accroche une brindille, puis se tend.",
            "narrateur|Les branches basses tapent l'épaule de Mila.",
            "enfant-f|On pousse, allez !",
            "narrateur|Le tissu se coince, trop large pour le tunnel.",
            "enfant-m|Moi, je rentre.",
            "narrateur|Nino glisse, puis pose la paume, stop.",
            "enfant-f|Cherche-la !",
            "narrateur|Nino ne dit rien, et montre une ombre.",
            "narrateur|La pomme du haut n'est plus au bout du ciel.",
            "narrateur|Une feuille rouge ment, collée au bois.",
            "maman|Elle manque, au moment de la prendre.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle observe la nappe, écoute les feuilles.",
            "narrateur|Elle retrouve le grain de sève, trop bas pour elle.",
            "papa|Vous passez comment, sous le vert ?",
        ],
    },
    (3, 1): {
        "sons": "racine,bois",
        "emphasis": "racine",
        "passage": [
            "narrateur|Le tabouret bute contre une racine.",
            "narrateur|Les branches basses ferment le passage de Mila.",
            "enfant-f|On force, Nino !",
            "narrateur|Le bois se coince, Mila trop haute.",
            "enfant-m|Moi, je rampe.",
            "narrateur|Nino passe, puis s'immobilise.",
            "enfant-f|Attrape !",
            "narrateur|Nino ferme la bouche, le doigt vers le vide.",
            "narrateur|La pomme du haut n'est plus où elle pendait.",
            "narrateur|Une feuille rouge ment, dans le tunnel.",
            "papa|Elle manque, juste là.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Elle retrouve le grain de sève, sur le tronc.",
            "maman|Vous passez comment, sous le vert ?",
        ],
    },
    (1, 2): {
        "sons": "herbe,panier",
        "emphasis": "herbe",
        "passage": [
            "narrateur|Le panier penche, trop vite, dans l'herbe.",
            "narrateur|L'herbe haute arrive à la poitrine de Nino.",
            "enfant-f|Je la vois !",
            "narrateur|Mila voit par-dessus, tout clair.",
            "enfant-m|Moi, je vois que l'herbe.",
            "enfant-f|Cours, Nino !",
            "narrateur|Nino recule d'un pas, les lèvres serrées.",
            "narrateur|Le rouge qu'elle voyait n'est qu'une feuille.",
            "narrateur|La pomme du haut a disparu dans l'herbe.",
            "papa|Elle manque, au moment de la prendre.",
            "narrateur|Le sourire de Mila s'en va.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle observe le panier, écoute l'herbe.",
            "narrateur|Elle retrouve le grain de sève, à la hauteur de Nino.",
            "maman|Vous la trouvez comment, dans l'herbe ?",
        ],
    },
    (2, 2): {
        "sons": "herbe,tissu",
        "emphasis": "brin",
        "passage": [
            "narrateur|La nappe s'ouvre, un coin, dans l'herbe.",
            "narrateur|L'herbe haute avale les genoux de Nino.",
            "enfant-f|Le rond rouge, là !",
            "narrateur|Mila pointe par-dessus les brins.",
            "enfant-m|Je ne vois rien.",
            "enfant-f|Avance, vite !",
            "narrateur|Nino secoue la tête, sans un mot.",
            "narrateur|Le rond n'est qu'un pétale, collé.",
            "narrateur|La pomme du haut s'est perdue au sol.",
            "maman|Elle manque, juste au moment de la prendre.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle observe la nappe, écoute l'herbe.",
            "narrateur|Elle retrouve le grain de sève, trop bas pour elle.",
            "papa|Vous la trouvez comment, dans l'herbe ?",
        ],
    },
    (3, 2): {
        "sons": "herbe,bois",
        "emphasis": "sol",
        "passage": [
            "narrateur|Le tabouret s'enfonce un peu, dans l'herbe.",
            "narrateur|L'herbe haute cache les pieds de Nino.",
            "enfant-f|Je grimpe, je verrai !",
            "narrateur|Mila se hausse, et un rond rouge cligne.",
            "enfant-m|Attends.",
            "enfant-f|Descends la chercher !",
            "narrateur|Nino pose la paume sur le bois, stop.",
            "narrateur|Le rond n'est qu'une tache de soleil.",
            "narrateur|La pomme du haut n'est plus sur sa branche.",
            "papa|Elle manque, dans l'herbe, quelque part.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Elle retrouve le grain de sève, à la hauteur de Nino.",
            "maman|Vous la trouvez comment, dans l'herbe ?",
        ],
    },
    (1, 3): {
        "sons": "banc,panier",
        "emphasis": "banc",
        "passage": [
            "narrateur|Le panier pose un toc contre le banc.",
            "narrateur|Le banc du tronc est chaud, tout sec.",
            "enfant-f|Je monte, pour la pomme du haut.",
            "narrateur|Mila se hausse, les talons levés.",
            "narrateur|Ses doigts frôlent une tige vide.",
            "enfant-m|Mes bras sont trop courts.",
            "enfant-f|On saute, allez !",
            "narrateur|Nino recule, les deux mains ouvertes.",
            "narrateur|La pomme du haut n'est plus au bout des doigts.",
            "papa|Elle manque, au moment de la prendre.",
            "narrateur|Le sourire de Mila s'en va.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle observe le panier, écoute le bois.",
            "narrateur|Elle retrouve le grain de sève, trop bas pour elle.",
            "maman|Vous l'atteignez comment, depuis le banc ?",
        ],
    },
    (2, 3): {
        "sons": "banc,tissu",
        "emphasis": "tige",
        "passage": [
            "narrateur|La nappe glisse sur le bois du banc.",
            "narrateur|Le banc du tronc sent le soleil.",
            "enfant-f|Je grimpe, je l'attrape !",
            "narrateur|Mila tend le tissu, comme un filet.",
            "narrateur|Le filet cueille une tige, sans fruit.",
            "enfant-m|Je tiens le bas.",
            "enfant-f|Pousse-moi plus haut !",
            "narrateur|Nino secoue la tête, sans un mot.",
            "narrateur|La pomme du haut a quitté sa place.",
            "maman|Elle manque, juste au-dessus du banc.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle observe la nappe, écoute le bois.",
            "narrateur|Elle retrouve le grain de sève, sur le tronc.",
            "papa|Vous l'atteignez comment, depuis le banc ?",
        ],
    },
    (3, 3): {
        "sons": "banc,tabouret",
        "emphasis": "pied",
        "passage": [
            "narrateur|Le tabouret cogne le pied du banc.",
            "narrateur|Le banc du tronc tremble un peu.",
            "enfant-f|Les deux bois, je monte !",
            "narrateur|Mila empile trop vite, et ça penche.",
            "narrateur|Ses doigts touchent le vide, au bout.",
            "enfant-m|Stop.",
            "enfant-f|On remet, plus haut !",
            "narrateur|Nino plaque une main sur le bois.",
            "narrateur|La pomme du haut n'est plus où elle brillait.",
            "papa|Elle manque, au moment de la prendre.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Elle retrouve le grain de sève, à la hauteur de Nino.",
            "maman|Vous l'atteignez comment, depuis le banc ?",
        ],
    },
}

T3_LABS = {
    1: ("le passage de Nino", "la branche levée", "la pomme qui tombe"),
    2: ("les mains de Nino", "les yeux de Mila", "l'herbe écartée"),
    3: ("le bout des doigts", "le geste d'en bas", "le banc à deux"),
}

T3_CHOICE = {
    1: [
        "narrateur|La pomme reste cachée dans le vert.",
        "papa|Le passage de Nino, la branche levée, ou la pomme ?",
    ],
    2: [
        "narrateur|La pomme se cache dans l'herbe.",
        "maman|Les mains de Nino, les yeux de Mila, ou l'herbe ?",
    ],
    3: [
        "narrateur|La pomme du haut reste trop loin.",
        "papa|Les doigts, le geste d'en bas, ou le banc à deux ?",
    ],
}

T3_SONS = {
    (1, 1): "feuilles,pas",
    (1, 2): "branche,bois",
    (1, 3): "pomme,souffle",
    (2, 1): "herbe,mains",
    (2, 2): "herbe,voix",
    (2, 3): "herbe,brin",
    (3, 1): "banc,doigts",
    (3, 2): "bois,mains",
    (3, 3): "banc,pas",
}


def pose(a: int, key: str) -> str:
    table = {
        "sous": (
            "Nino pousse le panier sous les feuilles.",
            "Nino tend la nappe sous les brindilles.",
            "Nino glisse le tabouret sous le tunnel.",
        ),
        "attend_bas": (
            "Le panier attend en bas, plein d'ombre.",
            "La nappe attend en bas, un peu verte.",
            "Le tabouret attend en bas, un peu humide.",
        ),
        "cueille": (
            "Le panier cueille la pomme, toc.",
            "La nappe cueille la pomme, tout mou.",
            "Le tabouret cueille la pomme, tout rêche.",
        ),
        "pose_herbe": (
            "Nino pose la pomme dans le panier.",
            "Nino enveloppe la pomme dans la nappe.",
            "Nino pose la pomme sur le tabouret.",
        ),
        "tend_haut": (
            "Mila tend le panier, bras tout longs.",
            "Mila tend la nappe, bras tout longs.",
            "Mila pousse le tabouret, bras tout longs.",
        ),
        "nid": (
            "Le panier devient un nid, dans l'herbe.",
            "La nappe devient un nid, dans l'herbe.",
            "Le tabouret devient un nid, dans l'herbe.",
        ),
        "garde": (
            "Nino garde le panier au pied du banc.",
            "Nino garde la nappe au pied du banc.",
            "Nino garde le tabouret au pied du banc.",
        ),
        "tend_bas": (
            "Nino tend le panier, bras tout courts.",
            "Nino tend la nappe, bras tout courts.",
            "Nino pousse le tabouret, tout près.",
        ),
        "deux": (
            "Papa pose le panier sur le banc, entre eux.",
            "Papa pose la nappe sur le banc, entre eux.",
            "Papa pose le tabouret près du banc, entre eux.",
        ),
    }
    return "narrateur|" + table[key][a - 1]


def t3_pass(a: int, b: int, c: int) -> list[str]:
    rows: dict[tuple[int, int], list[str]] = {
        (1, 1): [
            "enfant-m|Je passe, Mila.",
            "narrateur|Nino rampe à la hauteur du grain de sève.",
            "enfant-f|J'attends ici.",
            pose(a, "sous"),
            "narrateur|Ses doigts dénouent la pomme, dans le vert.",
            "enfant-m|Je la tiens !",
            "papa|Tes épaules ont passé, Nino.",
            "narrateur|Mila observe l'objet, écoute les feuilles.",
            "narrateur|Elle retrouve le grain de sève, trop bas pour elle.",
            "enfant-f|Elle est à nous.",
            "maman|Le vert vous a laissé un passage.",
            "narrateur|La pomme rouge roule à leur hauteur.",
        ],
        (1, 2): [
            "enfant-f|Je soulève la branche.",
            "papa|Je te tiens, Mila.",
            "narrateur|Mila lève le bois, plus haute que Nino.",
            "enfant-m|Je vois la pomme !",
            pose(a, "attend_bas"),
            "narrateur|Nino tend les deux mains, sans se presser.",
            "narrateur|La pomme glisse vers lui, hors du vert.",
            "narrateur|Mila observe l'objet, écoute la branche.",
            "narrateur|Elle retrouve le grain de sève, sur le tronc.",
            "enfant-f|Elle est à toi, un moment.",
            "maman|La branche et les mains ont fait le travail.",
            "narrateur|Le grain de sève luit, à la hauteur de Nino.",
        ],
        (1, 3): [
            "enfant-f|On attend un peu.",
            "enfant-m|Moi aussi, j'attends.",
            "narrateur|Un souffle passe dans les feuilles.",
            "narrateur|La pomme se décroche, toute seule.",
            pose(a, "cueille"),
            "narrateur|Mila observe l'objet, écoute le souffle.",
            "narrateur|Elle retrouve le grain de sève, près de leurs pieds.",
            "papa|Elle est venue vers vous.",
            "enfant-m|On l'a reprise.",
            "enfant-f|Elle brille.",
            "maman|Vos cheveux sentent la feuille.",
            "narrateur|Le grain de sève reste collé, sur l'écorce.",
        ],
        (2, 1): [
            "enfant-m|Je ramasse, tout près du sol.",
            "enfant-f|Je te guide, d'en haut.",
            "narrateur|Nino écarte deux brins, à la hauteur du grain de sève.",
            "narrateur|La pomme rouge est là, collée.",
            "enfant-m|Je la tiens !",
            pose(a, "pose_herbe"),
            "narrateur|Mila observe l'objet, écoute l'herbe.",
            "narrateur|Elle retrouve le grain de sève, trop bas pour elle.",
            "papa|Tes mains étaient à la bonne hauteur.",
            "enfant-f|Passe-la, un peu.",
            "enfant-m|Elle est froide.",
            "maman|Le sol vous a rendu le fruit.",
        ],
        (2, 2): [
            "enfant-f|Je reste ici, plus haut.",
            "enfant-m|Je vais où tu dis.",
            pose(a, "tend_haut"),
            "narrateur|Mila voit le rond rouge, par-dessus.",
            "narrateur|Nino avance vers le point d'ombre.",
            "enfant-m|Je la tiens !",
            "narrateur|Mila observe l'objet, écoute l'herbe.",
            "narrateur|Elle retrouve le grain de sève, à la hauteur de Nino.",
            "maman|Tes yeux ont trouvé le chemin.",
            "enfant-f|Elle sent l'herbe.",
            "papa|Soufflez dessus, tout léger.",
            "narrateur|Le grain de sève sert de marque, dans l'ombre.",
        ],
        (2, 3): [
            "enfant-f|Papa, écarte un peu ?",
            "papa|Je fais un chemin, tout étroit.",
            "narrateur|L'herbe s'ouvre, comme une porte.",
            "narrateur|La pomme rouge apparaît, collée.",
            pose(a, "nid"),
            "enfant-m|On la prend.",
            "enfant-f|Oui.",
            "narrateur|Deux paires de mains tiennent le fruit.",
            "narrateur|Mila observe l'objet, écoute l'herbe.",
            "narrateur|Elle retrouve le grain de sève, sur le tronc.",
            "maman|Le nid dans l'herbe a tenu le fruit.",
            "narrateur|Un brin reste collé au grain de sève.",
        ],
        (3, 1): [
            "enfant-f|Je me hausse, un cran.",
            pose(a, "garde"),
            "narrateur|Les doigts de Mila touchent la peau.",
            "enfant-f|Elle bouge !",
            "narrateur|La pomme penche, puis se détache.",
            "enfant-m|Je la rattrape.",
            "narrateur|Mila observe l'objet, écoute le banc.",
            "narrateur|Elle retrouve le grain de sève, trop bas pour elle.",
            "papa|Tes doigts allaient assez loin.",
            "maman|Nino tenait bien le bas.",
            "enfant-f|Elle est à nous.",
            "narrateur|Le grain de sève luit, sous le banc du tronc.",
        ],
        (3, 2): [
            "enfant-f|Reste en bas, Nino.",
            "enfant-m|Je tends, d'ici.",
            pose(a, "tend_bas"),
            "narrateur|Mila fait basculer la pomme, tout léger.",
            "narrateur|Le fruit tombe dans les mains d'en bas.",
            "enfant-m|Je la tiens !",
            "narrateur|Mila observe l'objet, écoute les mains.",
            "narrateur|Elle retrouve le grain de sève, à la hauteur de Nino.",
            "papa|Chacun a fait sa part.",
            "enfant-f|Elle sent le soleil.",
            "maman|Tes mains d'en bas ont reçu le fruit.",
            "narrateur|Le grain de sève reste collé, comme un stop.",
        ],
        (3, 3): [
            "enfant-f|On monte à deux ?",
            "enfant-m|Oui, tout léger.",
            pose(a, "deux"),
            "narrateur|Papa tient le bois, tout ferme.",
            "narrateur|Mila et Nino tendent, sans se presser.",
            "enfant-f|Elle vient !",
            "enfant-m|Je la sens.",
            "narrateur|Mila observe l'objet, écoute le banc.",
            "narrateur|Elle retrouve le grain de sève, sur le tronc.",
            "maman|Chacun a tiré, sans se presser.",
            "papa|Le banc est resté à sa place.",
            "narrateur|Le grain de sève luit entre leurs deux ombres.",
        ],
    }
    return rows[(b, c)]


END_LEAD = {
    (1, 1): [
        "narrateur|Ils rentrent, la pomme au creux.",
        "enfant-m|Elle sent la feuille.",
        "enfant-f|Tes épaules l'ont fait descendre.",
        "papa|Le tunnel vert vous a laissés passer.",
        "maman|Posez-la sur le rond de jus.",
    ],
    (1, 2): [
        "narrateur|Sous la branche, la maison paraît petite.",
        "enfant-f|Nino, tu l'as vue glisser.",
        "enfant-m|Oui, tout près de mes mains.",
        "papa|Je t'ai tenue, pas trop longtemps.",
        "maman|Le rond de jus va se remplir.",
    ],
    (1, 3): [
        "narrateur|Le souffle du pommier les suit jusqu'à la porte.",
        "enfant-m|Elle est tombée vers nous.",
        "enfant-f|On a attendu.",
        "maman|Elle n'était plus trop mêlée.",
        "papa|Le jus perle, sur la peau.",
    ],
    (2, 1): [
        "narrateur|Ils rentrent avec de l'herbe aux genoux.",
        "enfant-m|Mes mains savaient le chemin.",
        "enfant-f|Moi, je voyais trop haut.",
        "papa|Vous avez suivi ce qui était à vous.",
        "maman|Soufflez le dernier brin, dehors.",
    ],
    (2, 2): [
        "narrateur|Ils n'ont pas couru dans tout le pré.",
        "enfant-f|Je l'ai vue par-dessus.",
        "enfant-m|Tes yeux étaient assez hauts.",
        "maman|L'herbe sent fort, sur vos mains.",
        "papa|Lavez-les, au bac, un peu.",
    ],
    (2, 3): [
        "narrateur|Leurs chaussettes portent de l'herbe.",
        "enfant-f|Papa a ouvert un chemin.",
        "enfant-m|On l'a prise.",
        "papa|L'herbe vous a laissé la place.",
        "maman|Changez le linge des pieds, d'abord.",
    ],
    (3, 1): [
        "narrateur|Le banc du tronc reste chaud, derrière eux.",
        "enfant-f|Mes doigts l'ont fait pencher.",
        "enfant-m|Moi, je l'ai rattrapée.",
        "papa|Le haut et le bas ont tenu.",
        "maman|Le rond de jus vous attend.",
    ],
    (3, 2): [
        "narrateur|Ils descendent du banc, la pomme au creux.",
        "enfant-m|Je l'ai eue d'en bas.",
        "enfant-f|Moi, je l'ai fait basculer.",
        "maman|Vos bras ont fait deux gestes.",
        "papa|Le bois n'a pas glissé.",
    ],
    (3, 3): [
        "narrateur|Le banc du tronc garde deux ombres, un moment.",
        "enfant-f|On a tiré, chacun.",
        "enfant-m|Papa tenait le bois.",
        "papa|Le banc est resté sage.",
        "maman|Le goûter peut commencer, maintenant.",
    ],
}

END_MID = {
    1: "narrateur|Le panier garde une feuille, collée à l'anse.",
    2: "narrateur|La nappe garde un brin, dans un carreau.",
    3: "narrateur|Le tabouret garde une trace de sève, tout rêche.",
}

END_CODA = {
    1: "narrateur|Mila pose un doigt près du grain de sève.",
    2: "narrateur|Nino aligne la pomme sous le grain de sève.",
    3: "narrateur|Le bois du tabouret frôle le grain de sève.",
}

LAST = {
    (1, 1, 1): "Une feuille reste collée à l'anse.",
    (1, 1, 2): "Le grain de sève luit, à la hauteur de Nino.",
    (1, 1, 3): "Un toc de pomme dort au fond du panier.",
    (1, 2, 1): "Un brin d'herbe reste dans le tressage.",
    (1, 2, 2): "Le rond de jus disparaît sous le fruit.",
    (1, 2, 3): "Un pétale sec voyage avec l'anse.",
    (1, 3, 1): "Le panier sent le bois chaud du banc.",
    (1, 3, 2): "Une auréole de jus sèche au bord de l'anse.",
    (1, 3, 3): "Deux ombres s'arrêtent sur le tressage.",
    (2, 1, 1): "Un coin de nappe reste vert, un peu.",
    (2, 1, 2): "Le tissu garde l'odeur des feuilles.",
    (2, 1, 3): "Le souffle a plissé un carreau.",
    (2, 2, 1): "Un brin reste cousu dans un carreau.",
    (2, 2, 2): "Le rond de jus mouille le tissu, puis sèche.",
    (2, 2, 3): "Un brin vert dort sous la nappe.",
    (2, 3, 1): "Le banc a tiédi un coin de nappe.",
    (2, 3, 2): "La pomme laisse un rond nouveau, sur le tissu.",
    (2, 3, 3): "Deux plis gardent la forme de leurs mains.",
    (3, 1, 1): "Une racine a marqué le bois, tout mince.",
    (3, 1, 2): "Le tabouret sent la feuille, un peu.",
    (3, 1, 3): "Un grain de sève a migré sur le pied.",
    (3, 2, 1): "L'herbe a mouillé une patte du bois.",
    (3, 2, 2): "Le rond de jus brille au bord du siège.",
    (3, 2, 3): "Un brin reste coincé sous le bois.",
    (3, 3, 1): "Le banc et le tabouret gardent la même chaleur.",
    (3, 3, 2): "La pomme roule, puis s'arrête contre le bois.",
    (3, 3, 3): "Le grain de sève luit entre les deux bois.",
}

ASK = {
    1: "papa|Tu raconteras ce qui bloquait ?",
    2: "maman|Tu gardes quoi, de l'herbe ?",
    3: "papa|Le moment difficile, tu le dis ?",
}

ANS = {
    1: "enfant-f|Surtout le tunnel vert.",
    2: "enfant-f|Surtout l'herbe haute.",
    3: "enfant-f|Surtout le banc.",
}


def ending(a: int, b: int, c: int) -> list[str]:
    rows = list(END_LEAD[(b, c)])
    rows.append(END_MID[a])
    rows.append(END_CODA[a])
    rows.append(ASK[b])
    rows.append(ANS[b])
    rows.append(f"narrateur|{LAST[(a, b, c)]}")
    return rows


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "bourdon,jus,pommier",
        {"emphasis": "grain de sève"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le panier", "la nappe", "le tabouret"), "pause_before": 200},
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
            {"emphasis": "grain de sève"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("les branches basses", "l'herbe haute", "le banc"), "pause_before": 200},
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
                    {"emphasis": "grain de sève"},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ending(a, b, c), "ending", "table,pomme",
                    {"emphasis": "grain de sève"},
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
        "lila",
        "sami",
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
        "ancre",
        "étoile brune",
        "fil pâle",
        "nichoir",
        "cerisier",
        "cuillère-capitaine",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(whole):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "enfant-f|" not in blob:
        raise SystemExit(f"{SID}: enfant-f absent")
    if "enfant-m|" not in blob:
        raise SystemExit(f"{SID}: enfant-m absent")
    if "grain de sève" not in blob:
        raise SystemExit(f"{SID}: indice grain de sève absent")
    if "refuse de foncer" not in blob:
        raise SystemExit(f"{SID}: refuse de foncer absent")
    if "bourdon" not in blob:
        raise SystemExit(f"{SID}: bourdon absent")

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
    if len(story["chunks"]) != 86:
        raise SystemExit(f"chunks {len(story['chunks'])}≠86")

    # labels inchangés vs source
    for c in src["chunks"]:
        nc = out_chunks[c["chunk_id"]]
        for k in ("option_1_label", "option_2_label", "option_3_label"):
            if (c.get(k) or "") != (nc.get(k) or ""):
                raise SystemExit(f"{c['chunk_id']} label {k}: {nc.get(k)!r} ≠ {c.get(k)!r}")
        for k in ("option_1_next_chunk", "option_2_next_chunk", "option_3_next_chunk", "default_next_chunk"):
            if (c.get(k) or "") != (nc.get(k) or ""):
                raise SystemExit(f"{c['chunk_id']} graphe {k} cassé")
        if c.get("kind") != nc.get("kind"):
            raise SystemExit(f"{c['chunk_id']} kind cassé")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK {SID} {sum(words(c['text']) for c in story['chunks'])} mots")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-014 — Le panier de Mila et la pomme du haut\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.COR.001 — faire avec Nino, pas toute seule "
        "(vécue, jamais dite)\n"
        "- **Personnages :** Mila, Nino, papa, maman\n"
        "- **Lieu :** jardin, sous le pommier — table du tronc, nappe, rond de jus\n"
        "- **Indice :** grain de sève sur l'écorce (ouverture → climax)\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` / labels inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Sur la nappe du jardin, un rond de jus attend. Mila veut y poser "
        "la pomme du haut, pour le goûter, maintenant. Un bourdon frotte "
        "l'écorce. Un grain de sève luit, à la hauteur de Nino. Mila saute "
        "seule : l'air seulement. Sourire parti. Papa s'accroupit. Merci vécu : "
        "elle a montré le grain. T1 : panier / nappe / tabouret (les trois "
        "partent). Première idée : lever, tendre, grimper seule. Ça rate. "
        "Nino pose la main, stop. Silence = réponse. T2 : branches basses "
        "(tunnel trop bas pour Mila), herbe haute (Nino ne voit rien), banc "
        "(tige vide). Deuxième ruse : la pomme du haut manque au moment de "
        "la prendre. Mila refuse de foncer. T3 : passage de Nino, branche "
        "levée, pomme qui tombe ; mains de Nino, yeux de Mila, herbe écartée ; "
        "bout des doigts, geste d'en bas, banc à deux. Le grain de sève paie. "
        "Le rond de jus se remplit. Monde ≠ TREE-DIF-053 (pas merle, pas nichoir), "
        "≠ TREE-COL-001 (pas quai des casseroles), ≠ TREE-COL-003 (pas cerisier).\n\n"
        "## Vécu\n\n"
        "Mila propose, saute, veut vite. Nino prend son temps, pose sa limite. "
        "Le silence compte. Le sourire disparaît ; envie et inquiétude se "
        "bousculent. Papa ou maman s'accroupit à la même hauteur. Personne ne "
        "donne la réponse. Mila observe l'objet, écoute le lieu, retrouve le "
        "grain de sève. La leçon se voit : elle ne passe pas sous le vert, "
        "lui si ; elle voit par-dessus l'herbe, lui touche le sol ; elle "
        "atteint le bout des doigts, lui tient le bas. Fin : pomme sur le "
        "rond + grain de sève + image unique du chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Ancien merged F-NAR-016 (notes/xai absents ou calqués) tout réécrit.\n"
        "- Ouverture inventée (rond de jus, table du tronc). Indice unique : "
        "grain de sève.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Corps : sourire parti, poitrine, adulte à la même hauteur. 2e ruse. "
        "Refuse de foncer. Dénouement qui a failli.\n"
        "- T1 ne retire pas l'équipement. 9 T2, 27 T3, 27 fins.\n"
        "- Merci vécu (montrer le grain). Question d'adulte. Un « en ce moment ».\n"
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
