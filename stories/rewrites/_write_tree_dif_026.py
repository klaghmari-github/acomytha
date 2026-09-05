#!/usr/bin/env python3
"""TREE-DIF-026 — Le théâtre de draps de Mila. DIF.COR.003, N3. example4 v2."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-026"
N3 = 16
TITLE = "Le théâtre de draps de Mila"
FIL = (
    "Avant la soupe, Mila veut un vrai spectacle : drap à carreaux, pinces, "
    "marionnette rouge au bouton de nacre. Nino sort du bain, lunettes voilées, "
    "cheveux mouillés, pull trop long. T1 ne retire rien. Salon, couloir, chambre : "
    "on s'ajuste pour que le jeu tienne. Le bouton de nacre du début revient."
)
CHARS = "Mila, Nino, papa, maman"
SETTING = "maison : salon, couloir, chambre, avant la soupe"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "bouton de nacre",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=la_lampe_a_commencé_sans_eux; tempo=naturel; sourire=léger; respiration=ample",
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
        "emphasis": "bouton de nacre",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_partent_ensemble; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=trop_vite_le_drap_tombe; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": "bouton de nacre",
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=le_corps_de_nino_n_est_pas_le_problème; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "bouton de nacre",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=on_s_ajuste_le_jeu_tient; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "bouton de nacre",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_bouton_de_nacre_porte_une_trace; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|La lampe du salon est allumée, trop tôt.",
    "narrateur|Ce n'est pas la nuit, et pourtant elle veille.",
    "narrateur|Deux chaises se font face, comme une scène.",
    "narrateur|Un drap à carreaux dort sur le coffre.",
    "narrateur|Ça sent la soupe, loin, dans la casserole.",
    "narrateur|Le radiateur tic, irrégulier, près du tapis.",
    "narrateur|Une oreille rouge dépasse du panier.",
    "narrateur|Sur le ventre de la marionnette, un bouton de nacre.",
    "narrateur|Il prend la lumière, minuscule et rond.",
    "papa|Tu as vu la lampe, Mila ?",
    "enfant-f|Le théâtre a commencé sans nous.",
    "maman|La soupe n'est pas prête.",
    "narrateur|En ce moment, Mila glisse sa main dans la laine.",
    "enfant-f|Un vrai spectacle, avant de manger.",
    "narrateur|Des chaussons glissent dans le couloir.",
    "copain|Je viens jouer !",
    "narrateur|Les lunettes de Nino portent un voile de bain.",
    "narrateur|Ses cheveux gouttent sur un pull trop long.",
    "enfant-f|On commence maintenant.",
    "narrateur|Elle tire le drap trop vite, vers les chaises.",
    "narrateur|Le tissu retombe, et le bouton de nacre disparaît.",
    "narrateur|Le sourire de Mila s'en va.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "papa|Nino, tu es là.",
    "narrateur|Papa s'accroupit, à la hauteur des lunettes.",
    "papa|Merci d'être venu.",
    "maman|Vous emportez le drap, les pinces, la marionnette ?",
]

T1_CHOICE = [
    "narrateur|Près du coffre, le drap sent le soleil de la fenêtre.",
    "narrateur|Les pinces cliquettent dans la poche de maman.",
    "narrateur|La marionnette attend, bouton de nacre au ventre.",
    "maman|Tu prends quoi, d'abord, Mila ?",
]

T1 = {
    1: {
        "lab": "le drap à carreaux",
        "sons": "tissu,panier",
        "emphasis": "drap à carreaux",
        "passage": [
            "narrateur|Mila prend d'abord le drap à carreaux.",
            "enfant-f|Il sent le soleil de la fenêtre.",
            "maman|Glisse-le dans le panier, tout plié.",
            "narrateur|Le tissu fait un petit froissement, chaud.",
            "papa|Les pinces, ensuite, dans ta poche.",
            "narrateur|Maman noue la marionnette rouge au poignet.",
            "narrateur|Le bouton de nacre frappe le panier, toc.",
            "enfant-f|Nino, tu portes le panier ?",
            "copain|Je le tiens, même un peu flou.",
            "narrateur|Mila veut courir, puis s'arrête.",
            "papa|Le drap d'abord, vous l'avez.",
            "maman|Les trois affaires partent ensemble.",
        ],
        "question": [
            "narrateur|Le drap à carreaux est dans le panier.",
            "maman|Le drap est où ?",
        ],
        "qfields": {
            "expected_answer": "panier",
            "accepted_examples": "panier | le panier | dans le panier | au panier",
            "retry_prompt": "Le drap est dans le panier.",
        },
        "confirm": [
            "enfant-f|Dans le panier.",
            "papa|Oui.",
            "narrateur|Les pinces voyagent dans la poche.",
            "narrateur|La marionnette dort au poignet, nacre au ventre.",
            "copain|Je vois des carreaux, un peu flous.",
            "enfant-f|C'est pour notre scène.",
            "maman|On avance, alors ?",
            "narrateur|Le panier tape la hanche de Mila.",
        ],
    },
    2: {
        "lab": "les pinces",
        "sons": "metal,poche",
        "emphasis": "pinces",
        "passage": [
            "narrateur|Mila prend d'abord les pinces, froides.",
            "enfant-f|Elles cliquettent dans ma paume.",
            "papa|Range-les dans ta poche, sans te pincer.",
            "narrateur|Le métal fait un petit toc contre le tissu.",
            "maman|Le drap, ensuite, dans le panier.",
            "narrateur|Elle glisse la marionnette rouge au poignet.",
            "narrateur|Le bouton de nacre cogne une pince, tic.",
            "enfant-f|Nino, tu accroches le bord ?",
            "copain|J'essaie, mes lunettes glissent un peu.",
            "narrateur|Mila ouvre la bouche, puis la referme.",
            "maman|Les pinces d'abord, elles sont prêtes.",
            "papa|Les trois affaires partent ensemble.",
        ],
        "question": [
            "narrateur|Les pinces sont dans la poche.",
            "papa|Les pinces sont où ?",
        ],
        "qfields": {
            "expected_answer": "poche",
            "accepted_examples": "poche | la poche | dans la poche | sa poche",
            "retry_prompt": "Les pinces sont dans la poche.",
        },
        "confirm": [
            "enfant-f|Dans la poche.",
            "maman|Oui.",
            "narrateur|Le drap voyage dans le panier.",
            "narrateur|La marionnette dort au poignet, nacre au ventre.",
            "copain|Ça cliquette quand je marche.",
            "enfant-f|Ne les perds pas.",
            "papa|On avance, alors ?",
            "narrateur|Une goutte tombe d'une mèche de Nino.",
        ],
    },
    3: {
        "lab": "la marionnette rouge",
        "sons": "laine,bouton",
        "emphasis": "marionnette rouge",
        "passage": [
            "narrateur|Mila enfile d'abord la marionnette rouge.",
            "enfant-f|Elle marche sur ma main.",
            "maman|Garde-la au poignet, comme un secret.",
            "narrateur|La laine rouge chatouille la peau.",
            "papa|Le drap et les pinces, avec vous.",
            "narrateur|Il les pose près du panier, sans se tromper.",
            "narrateur|Le bouton de nacre prend la lampe, un instant.",
            "enfant-f|Nino, elle te salue !",
            "copain|Bonjour, petite laine.",
            "narrateur|Mila veut montrer le bouton trop vite.",
            "papa|La marionnette d'abord, elle est prête.",
            "maman|Les trois affaires partent ensemble.",
        ],
        "question": [
            "narrateur|La marionnette rouge est au poignet.",
            "maman|La marionnette est où ?",
        ],
        "qfields": {
            "expected_answer": "poignet",
            "accepted_examples": "poignet | au poignet | le poignet | son poignet",
            "retry_prompt": "La marionnette est au poignet.",
        },
        "confirm": [
            "enfant-f|Au poignet.",
            "papa|Oui.",
            "narrateur|Le drap voyage dans le panier.",
            "narrateur|Les pinces voyagent dans la poche.",
            "copain|Elle a un œil brodé, minuscule.",
            "enfant-f|Tu le verras mieux, tout à l'heure.",
            "maman|On avance, alors ?",
            "narrateur|Le pull de Nino cache ses poignets.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le panier tape un peu la hanche, à chaque pas.",
        "narrateur|Trois pièces de la maison attendent.",
        "narrateur|Le salon, le couloir, et la chambre.",
        "papa|Vous jouez où, pour le spectacle ?",
    ],
    2: [
        "narrateur|Les pinces cliquettent dans la poche, à chaque pas.",
        "narrateur|Trois pièces de la maison attendent.",
        "narrateur|Le salon, le couloir, et la chambre.",
        "papa|Vous jouez où, pour le spectacle ?",
    ],
    3: [
        "narrateur|La marionnette balance au poignet, nacre au ventre.",
        "narrateur|Trois pièces de la maison attendent.",
        "narrateur|Le salon, le couloir, et la chambre.",
        "papa|Vous jouez où, pour le spectacle ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "radiateur,tissu",
        "emphasis": "bouton de nacre",
        "passage": [
            "narrateur|Mila déplie le drap entre les deux chaises.",
            "narrateur|Le radiateur souffle un air tiède, trop près.",
            "copain|Un nuage sur mes lunettes !",
            "narrateur|Un voile cache la scène, et le bouton de nacre.",
            "narrateur|Mila pousse le roi trop vite, vers Nino.",
            "narrateur|Le drap retombe : Nino n'a pas vu le bord.",
            "enfant-f|On ne fonce pas.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|La chaleur a voilé ses verres, c'est tout.",
            "papa|Toi tu vois net, lui un peu flou.",
            "narrateur|Le bouton de nacre n'est plus qu'un rond pâle.",
            "papa|La scène est floue, vous faites quoi ?",
        ],
    },
    (2, 1): {
        "sons": "radiateur,metal",
        "emphasis": "bouton de nacre",
        "passage": [
            "narrateur|Mila attache le drap, pince après pince.",
            "narrateur|Le radiateur souffle un air tiède, trop près.",
            "copain|Un nuage sur mes lunettes !",
            "narrateur|Nino vise à côté : une pince tombe.",
            "narrateur|Le bouton de nacre devient un rond pâle.",
            "enfant-f|Plus vite, Nino.",
            "narrateur|Puis elle referme la bouche.",
            "enfant-f|On ne fonce pas.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|La chaleur a voilé ses verres, c'est tout.",
            "papa|Toi tu vois net, lui un peu flou.",
            "papa|La scène est floue, vous faites quoi ?",
        ],
    },
    (3, 1): {
        "sons": "radiateur,laine",
        "emphasis": "bouton de nacre",
        "passage": [
            "narrateur|La marionnette grimpe le dossier d'une chaise.",
            "narrateur|Le radiateur souffle un air tiède, trop près.",
            "copain|Un nuage sur mes lunettes !",
            "narrateur|Nino salue trop bas, loin du bouton de nacre.",
            "narrateur|Le roi rouge cherche un public qu'il ne voit pas.",
            "enfant-f|Regarde, là !",
            "narrateur|Sa voix se casse, trop pressée.",
            "enfant-f|On ne fonce pas.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|La chaleur a voilé ses verres, c'est tout.",
            "papa|Toi tu vois net, lui un peu flou.",
            "papa|La scène est floue, vous faites quoi ?",
        ],
    },
    (1, 2): {
        "sons": "crochet,goutte",
        "emphasis": "bouton de nacre",
        "passage": [
            "narrateur|Mila jette le drap vers le crochet du manteau.",
            "enfant-f|Ici, le couloir fait un rideau, Nino.",
            "copain|Mes cheveux sont lourds du bain.",
            "narrateur|Le drap glisse, accroché à une mèche mouillée.",
            "narrateur|Le bouton de nacre s'emmêle à la mèche.",
            "narrateur|Une goutte tombe sur le carrelage, toc.",
            "enfant-f|On tire, alors ?",
            "narrateur|Elle s'arrête, la main ouverte.",
            "enfant-f|On ne fonce pas.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|Ils sèchent, ce n'est rien.",
            "papa|Le rideau accroche, vous faites quoi ?",
        ],
    },
    (2, 2): {
        "sons": "pince,goutte",
        "emphasis": "bouton de nacre",
        "passage": [
            "narrateur|Mila tend une pince vers le crochet haut.",
            "enfant-f|Ici, le couloir fait un rideau, Nino.",
            "copain|Mes cheveux sont lourds du bain.",
            "narrateur|La pince pince un cheveu, pas le tissu.",
            "narrateur|Le bouton de nacre se coince sous la mèche.",
            "narrateur|Une goutte tombe sur le carrelage, toc.",
            "enfant-f|On arrache, alors ?",
            "narrateur|Elle s'arrête, la pince entre deux doigts.",
            "enfant-f|On ne fonce pas.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|Ils sèchent, ce n'est rien.",
            "papa|Le rideau accroche, vous faites quoi ?",
        ],
    },
    (3, 2): {
        "sons": "laine,goutte",
        "emphasis": "bouton de nacre",
        "passage": [
            "narrateur|La marionnette tire le drap, vers le crochet.",
            "enfant-f|Ici, le couloir fait un rideau, Nino.",
            "copain|Mes cheveux sont lourds du bain.",
            "narrateur|La laine rouge s'emmêle à une mèche humide.",
            "narrateur|Le bouton de nacre disparaît sous le savon.",
            "narrateur|Une goutte tombe sur le carrelage, toc.",
            "enfant-f|On tire la laine, alors ?",
            "narrateur|Elle s'arrête, le poignet figé.",
            "enfant-f|On ne fonce pas.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|Ils sèchent, ce n'est rien.",
            "papa|Le rideau accroche, vous faites quoi ?",
        ],
    },
    (1, 3): {
        "sons": "lit,tissu",
        "emphasis": "bouton de nacre",
        "passage": [
            "narrateur|Mila tend le drap au pied du lit.",
            "enfant-f|Le lit est notre château, Nino.",
            "copain|Mon pull me suit jusqu'aux genoux !",
            "narrateur|Une manche trop longue emporte un coin du drap.",
            "narrateur|Le bouton de nacre disparaît dans la laine du pull.",
            "enfant-f|Sors tes mains !",
            "narrateur|Sa voix se casse, trop pressée.",
            "enfant-f|On ne fonce pas.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|Le pull est un peu grand, c'est tout.",
            "papa|Toi tes manches s'arrêtent, les siennes voyagent.",
            "papa|Le pull et le roi, vous faites comment ?",
        ],
    },
    (2, 3): {
        "sons": "lit,metal",
        "emphasis": "bouton de nacre",
        "passage": [
            "narrateur|Mila attache le drap au bois du lit.",
            "enfant-f|Le lit est notre château, Nino.",
            "copain|Mon pull me suit jusqu'aux genoux !",
            "narrateur|Une manche trop longue balaie les pinces.",
            "narrateur|Le bouton de nacre disparaît dans la laine du pull.",
            "enfant-f|Sors tes mains !",
            "narrateur|Sa voix se casse, trop pressée.",
            "enfant-f|On ne fonce pas.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|Le pull est un peu grand, c'est tout.",
            "papa|Toi tes manches s'arrêtent, les siennes voyagent.",
            "papa|Le pull et le roi, vous faites comment ?",
        ],
    },
    (3, 3): {
        "sons": "lit,laine",
        "emphasis": "bouton de nacre",
        "passage": [
            "narrateur|La marionnette se cache sous l'oreiller.",
            "enfant-f|Le lit est notre château, Nino.",
            "copain|Mon pull me suit jusqu'aux genoux !",
            "narrateur|Une manche trop longue avale la marionnette.",
            "narrateur|Le bouton de nacre n'a plus de visage, sous le pull.",
            "enfant-f|Sors le roi !",
            "narrateur|Sa voix se casse, trop pressée.",
            "enfant-f|On ne fonce pas.",
            "narrateur|Nino ne dit rien.",
            "narrateur|Son silence compte, comme une réponse.",
            "maman|Le pull est un peu grand, c'est tout.",
            "papa|Toi tes manches s'arrêtent, les siennes voyagent.",
            "papa|Le pull et le roi, vous faites comment ?",
        ],
    },
}

T3_LABS = {
    1: ("le torchon de maman", "les mains de Nino", "la fenêtre ouverte"),
    2: ("la pince plus haut", "la serviette", "tenir le drap"),
    3: ("les manches retroussées", "Mila tient la marionnette", "l'élastique de maman"),
}

T3_CHOICE = {
    1: [
        "narrateur|La buée reste sur les verres.",
        "narrateur|Le bouton de nacre n'est qu'un rond pâle.",
        "papa|Le torchon, les mains, ou la fenêtre ?",
    ],
    2: [
        "narrateur|Une mèche mouillée tient le drap.",
        "narrateur|Le bouton de nacre s'est perdu dessous.",
        "maman|La pince plus haut, la serviette, ou tenir ?",
    ],
    3: [
        "narrateur|Les manches cachent le petit héros.",
        "narrateur|Le bouton de nacre n'a plus de visage.",
        "papa|Manches, marionnette, ou l'élastique de maman ?",
    ],
}

T3_SONS = {
    (1, 1): "torchon,verre",
    (1, 2): "mains,tissu",
    (1, 3): "fenetre,air",
    (2, 1): "pince,crochet",
    (2, 2): "serviette,savon",
    (2, 3): "tissu,mains",
    (3, 1): "manches,laine",
    (3, 2): "marionnette,drap",
    (3, 3): "elastique,poignet",
}

T3_EMPH = {
    1: {1: "torchon", 2: "mains", 3: "fenêtre"},
    2: {1: "pince", 2: "serviette", 3: "drap"},
    3: {1: "manches", 2: "marionnette", 3: "élastique"},
}

OBJ_LINE = {
    1: "Le drap à carreaux attend, plié entre les chaises.",
    2: "Les pinces cliquettent, prêtes, dans la poche.",
    3: "La marionnette rouge veille au poignet.",
}


def t3_pass(a: int, b: int, c: int) -> list[str]:
    obj = OBJ_LINE[a]
    if b == 1 and c == 1:
        wipe = {
            1: "Nino essuie, puis reprend le bord du drap.",
            2: "Nino essuie, puis reprend une pince.",
            3: "Nino essuie, puis salue la marionnette.",
        }[a]
        return [
            "enfant-f|Maman, le torchon, s'il te plaît.",
            "maman|Sur les verres, pas trop fort.",
            "narrateur|Nino frotte un rond, puis un autre.",
            f"narrateur|{obj}",
            f"narrateur|{wipe}",
            "narrateur|Le bouton de nacre redevient un petit astre.",
            "copain|Je vois le roi !",
            "enfant-f|Il te regardait, derrière la buée.",
            "papa|Vous avez rendu la scène, sans changer Nino.",
            "maman|Le torchon sent le tiroir, un peu.",
        ]
    if b == 1 and c == 2:
        touch = {
            1: "Nino palpe le drap, Mila parle.",
            2: "Nino palpe les pinces, Mila parle.",
            3: "Nino palpe la laine rouge, Mila parle.",
        }[a]
        return [
            "enfant-f|Tu joues avec tes mains, Nino.",
            "copain|Je touche, toi tu racontes.",
            f"narrateur|{touch}",
            "narrateur|Sous le drap, deux silhouettes avancent.",
            "enfant-f|Le roi est à gauche, tout chaud.",
            "copain|Je le tiens !",
            "narrateur|Les doigts trouvent le bouton de nacre.",
            f"narrateur|{obj}",
            "papa|Les mains ont vu à la place des verres.",
            "maman|Le salon vous a gardés.",
        ]
    if b == 1 and c == 3:
        air = {
            1: "Le drap claque un peu, puis s'apaise.",
            2: "Les pinces tintent, puis le métal se tait.",
            3: "La marionnette se penche vers l'air frais.",
        }[a]
        return [
            "enfant-f|On ouvre un peu, papa ?",
            "papa|Un doigt de fenêtre, pas plus.",
            "narrateur|L'air froid chasse la buée, lentement.",
            f"narrateur|{air}",
            "copain|Ça redevient clair !",
            "enfant-f|Le spectacle peut commencer.",
            "narrateur|Nino ajuste ses lunettes, nettes.",
            "narrateur|Le bouton de nacre prend la lumière du volet.",
            f"narrateur|{obj}",
            "maman|La chaleur est partie, le jeu reste.",
        ]
    if b == 2 and c == 1:
        high = {
            1: "Mila attache le drap plus haut, hors des mèches.",
            2: "Mila pose la pince plus haut, hors des mèches.",
            3: "La marionnette pousse le drap plus haut.",
        }[a]
        return [
            "enfant-f|On met la pince plus haut.",
            "copain|Mes cheveux restent en bas, alors.",
            f"narrateur|{high}",
            "narrateur|Le rideau tient au crochet, droit.",
            "narrateur|Les mèches de Nino pendent, libres.",
            "enfant-f|Tu peux bouger, maintenant.",
            "copain|Le drap ne m'attrape plus.",
            "narrateur|Le bouton de nacre pend, hors des cheveux.",
            f"narrateur|{obj}",
            "papa|Chacun a sa hauteur, sur le crochet.",
        ]
    if b == 2 and c == 2:
        dry = {
            1: "Le drap attend, le temps d'un frottement.",
            2: "Les pinces attendent, le temps d'un frottement.",
            3: "La marionnette attend, le temps d'un frottement.",
        }[a]
        return [
            "enfant-f|La serviette, maman ?",
            "maman|Frotte, pas trop fort.",
            "narrateur|Nino essuie une mèche, puis une autre.",
            f"narrateur|{dry}",
            "copain|Elles sont plus légères !",
            "enfant-f|On accroche, maintenant.",
            "narrateur|Le drap monte, sans emporter de cheveu.",
            "narrateur|Le bouton de nacre redevient rond, libre.",
            f"narrateur|{obj}",
            "papa|Vous avez laissé l'eau s'en aller.",
        ]
    if b == 2 and c == 3:
        hold = {
            1: "Nino tient le drap à deux mains, sans pince.",
            2: "Nino tient le bord, Mila garde les pinces.",
            3: "Nino tient le drap, la marionnette salue.",
        }[a]
        return [
            "enfant-f|Tu tiens le drap, moi j'attache à côté.",
            "copain|Mes mains font le crochet, alors.",
            f"narrateur|{hold}",
            "narrateur|Le rideau s'ouvre quand Nino recule.",
            "narrateur|Il se ferme quand il avance.",
            "enfant-f|C'est toi le rideau vivant !",
            "copain|Et toi le spectacle.",
            "narrateur|Le bouton de nacre passe dans l'ouverture.",
            f"narrateur|{obj}",
            "papa|Vous jouez avec ce que vous avez.",
        ]
    if b == 3 and c == 1:
        roll = {
            1: "Les manches remontent, le drap redevient libre.",
            2: "Les manches remontent, les pinces redeviennent visibles.",
            3: "Les manches remontent, la marionnette reparaît.",
        }[a]
        return [
            "enfant-f|On retrousse, Nino.",
            "copain|Jusqu'au coude, comme papa.",
            "narrateur|Deux rouleaux de laine tiennent, un peu épais.",
            f"narrateur|{roll}",
            "enfant-f|Je te vois les mains, maintenant.",
            "copain|Le héros n'est plus dans le pull.",
            "narrateur|Le bouton de nacre reprend sa place, au milieu.",
            f"narrateur|{obj}",
            "papa|Les manches ont laissé le jeu passer.",
            "maman|Le pull reste, plus court aux poignets.",
        ]
    if b == 3 and c == 2:
        split = {
            1: "Mila garde la marionnette, Nino lève le drap.",
            2: "Mila attache, Nino lève le drap comme un rideau.",
            3: "Mila parle avec la laine, Nino lève le drap.",
        }[a]
        return [
            "enfant-f|Moi je tiens la marionnette.",
            "copain|Moi je fais le rideau, avec le drap.",
            f"narrateur|{split}",
            "narrateur|Les manches trop longues bougent le tissu, seulement.",
            "narrateur|La petite laine reste hors du pull.",
            "copain|Le château s'ouvre !",
            "enfant-f|Le roi sort, tout rouge.",
            "narrateur|Le bouton de nacre reste visible, hors des manches.",
            f"narrateur|{obj}",
            "papa|Chacun a pris sa part, à sa taille.",
        ]
    bind = {
        1: "L'élastique tient une manche, le drap l'autre bord.",
        2: "L'élastique tient une manche, les pinces le drap.",
        3: "L'élastique tient une manche, la marionnette salue.",
    }[a]
    return [
        "enfant-f|Maman, ton élastique, s'il te plaît.",
        "maman|Un pour chaque manche.",
        "narrateur|Nino tend les poignets, maman noue.",
        f"narrateur|{bind}",
        "copain|Mes mains sont nues, maintenant.",
        "enfant-f|Le héros peut marcher.",
        "narrateur|Le rouge avance sur la couette.",
        "narrateur|Le bouton de nacre salue, hors du pull.",
        f"narrateur|{obj}",
        "papa|Vous avez demandé, et ça tient.",
    ]


LAST = {
    (1, 1, 1): "Un rond de nacre dort sur le verre essuyé.",
    (1, 1, 2): "Sous le drap, le bouton chauffe la paume de Nino.",
    (1, 1, 3): "Un filet d'air tient le bouton, face à la lampe.",
    (1, 2, 1): "Le bouton de nacre pend libre, sous le crochet haut.",
    (1, 2, 2): "Un fil de savon sèche sur le bouton de nacre.",
    (1, 2, 3): "Les mains-rideau laissent passer un éclat de nacre.",
    (1, 3, 1): "Les manches roulées montrent le bouton, au milieu du lit.",
    (1, 3, 2): "Mila garde la nacre, Nino garde le château de draps.",
    (1, 3, 3): "Deux élastiques veillent, et le bouton salue la couette.",
    (2, 1, 1): "Entre deux pinces, le bouton de nacre tremble, net.",
    (2, 1, 2): "Une pince tient le secret de nacre, dans la paume.",
    (2, 1, 3): "Le métal des pinces garde un reflet de nacre.",
    (2, 2, 1): "La pince haute laisse le bouton respirer, hors des mèches.",
    (2, 2, 2): "La serviette a rendu le bouton, sans un cheveu.",
    (2, 2, 3): "Les pinces dorment, le bouton avance au poignet.",
    (2, 3, 1): "Les pinces tiennent le château, le bouton est roi.",
    (2, 3, 2): "Le bouton reste hors des manches, au-dessus des pinces.",
    (2, 3, 3): "L'élastique a rendu les mains, le bouton salue.",
    (3, 1, 1): "L'œil brodé et le bouton se regardent, nets.",
    (3, 1, 2): "La paume de Nino connaît le rond de nacre, par cœur.",
    (3, 1, 3): "Le bouton de nacre prend la lumière de la fenêtre.",
    (3, 2, 1): "La marionnette salue, le bouton hors des mèches.",
    (3, 2, 2): "Un grain de savon sèche au creux du bouton.",
    (3, 2, 3): "Le bouton de nacre passe dans l'ouverture des mains.",
    (3, 3, 1): "Le bouton de nacre sort du pull, visible sur la couette.",
    (3, 3, 2): "Le roi rouge tient sa nacre, hors du pull trop long.",
    (3, 3, 3): "Un élastique garde une manche, le bouton l'autre secret.",
}

HARD = {
    1: "Le voile a failli tout cacher.",
    2: "La mèche a failli garder le drap.",
    3: "Le pull a failli avaler le roi.",
}

CODA = {
    1: "Le drap à carreaux retombe sur le coffre.",
    2: "Les pinces rentrent dans la poche.",
    3: "La marionnette rouge veille au bord du lit.",
}


def ending(a: int, b: int, c: int) -> list[str]:
    last = LAST[(a, b, c)]
    hard = HARD[b]
    coda = CODA[a]
    soup = {
        1: "La casserole appelle, loin, dans la cuisine.",
        2: "La soupe sent le couloir, tiède.",
        3: "Un bol attend, au bout du couloir.",
    }[c]
    if b == 1 and c == 1:
        return [
            "narrateur|Le salon sent le torchon tiède.",
            "copain|J'ai vu l'œil brodé, net.",
            "enfant-f|Tes lunettes ont trouvé le roi.",
            f"narrateur|{hard}",
            "papa|Vous avez joué, chacun avec sa vue.",
            f"narrateur|{coda}",
            f"narrateur|{soup}",
            f"narrateur|{last}",
        ]
    if b == 1 and c == 2:
        return [
            "narrateur|Sous le drap, l'air est un peu chaud.",
            "enfant-f|Tu as touché, moi j'ai raconté.",
            "copain|Mes mains ont vu le roi.",
            f"narrateur|{hard}",
            "papa|Les verres flous n'ont pas arrêté le jeu.",
            f"narrateur|{coda}",
            f"narrateur|{soup}",
            f"narrateur|{last}",
        ]
    if b == 1 and c == 3:
        return [
            "narrateur|Un filet d'air froid reste dans le salon.",
            "copain|La buée est partie, toute seule.",
            "enfant-f|On a attendu le verre clair.",
            f"narrateur|{hard}",
            "maman|La fenêtre a rendu la scène.",
            f"narrateur|{coda}",
            f"narrateur|{soup}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 1:
        return [
            "narrateur|Le crochet du couloir garde le drap.",
            "enfant-f|La pince était trop bas, d'abord.",
            "copain|Mes cheveux sont restés libres.",
            f"narrateur|{hard}",
            "papa|Chacun a eu sa hauteur, sur le bois.",
            f"narrateur|{coda}",
            f"narrateur|{soup}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 2:
        return [
            "narrateur|La serviette sent le savon du bain.",
            "copain|Tu as frotté, sans tirer.",
            "enfant-f|Puis on a accroché, sans emporter de cheveu.",
            f"narrateur|{hard}",
            "maman|L'eau s'en est allée, le jeu est resté.",
            f"narrateur|{coda}",
            f"narrateur|{soup}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 3:
        return [
            "narrateur|Les mains de Nino gardent le pli du drap.",
            "enfant-f|Tu étais le rideau vivant.",
            "copain|Toi le spectacle, moi l'ouverture.",
            f"narrateur|{hard}",
            "papa|Vous avez joué avec ce que vous aviez.",
            f"narrateur|{coda}",
            f"narrateur|{soup}",
            f"narrateur|{last}",
        ]
    if b == 3 and c == 1:
        return [
            "narrateur|Deux rouleaux de manches tiennent.",
            "enfant-f|Tes mains sont sorties du pull.",
            "copain|Le héros n'était plus avalé.",
            f"narrateur|{hard}",
            "papa|Les manches ont laissé le jeu passer.",
            f"narrateur|{coda}",
            f"narrateur|{soup}",
            f"narrateur|{last}",
        ]
    if b == 3 and c == 2:
        return [
            "narrateur|Le drap-rideau retombe au pied du lit.",
            "copain|Tu tenais le roi, moi le château.",
            "enfant-f|Tes manches bougeaient seulement le tissu.",
            f"narrateur|{hard}",
            "maman|Chacun a pris sa part, à sa taille.",
            f"narrateur|{coda}",
            f"narrateur|{soup}",
            f"narrateur|{last}",
        ]
    return [
        "narrateur|Deux élastiques veillent aux poignets.",
        "enfant-f|On a demandé, et ça tenait.",
        "copain|Mes mains étaient nues, pour le roi.",
        f"narrateur|{hard}",
        "maman|Mes élastiques rentrent dans le tiroir.",
        f"narrateur|{coda}",
        f"narrateur|{soup}",
        f"narrateur|{last}",
    ]


END_SONS = {1: "drap,soupe", 2: "pinces,soupe", 3: "laine,soupe"}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "lampe,casserole,chaussons",
        {"emphasis": "bouton de nacre"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le drap à carreaux", "les pinces", "la marionnette rouge"), "pause_before": 200},
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
            {"emphasis": "bouton de nacre"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("le salon", "le couloir", "la chambre"), "pause_before": 200},
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
                    {"emphasis": "bouton de nacre"},
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
        "escargot",
        "aniss",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "bouton de nacre" not in blob:
        raise SystemExit(f"{SID}: indice bouton de nacre absent")
    if "enfant-f|" not in blob:
        raise SystemExit(f"{SID}: enfant-f absent")
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
        "# TREE-DIF-026 — Le théâtre de draps de Mila\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.COR.003 — corps / apparence (lunettes, cheveux, habit) "
        "dans le spectacle (vécue, jamais dite)\n"
        "- **Personnages :** Mila, Nino, papa, maman\n"
        "- **Lieu :** maison : salon, couloir, chambre, avant la soupe\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La lampe du salon est allumée trop tôt. Un drap à carreaux dort sur le coffre. "
        "Sur le ventre de la marionnette rouge, un bouton de nacre prend la lumière. "
        "Mila veut un vrai spectacle avant la soupe. Nino sort du bain : lunettes voilées, "
        "cheveux mouillés, pull trop long. Elle tire trop vite, le drap retombe. "
        "Drap, pinces ou marionnette : les trois partent. Salon (buée), couloir (mèches), "
        "chambre (manches). Torchon, mains, fenêtre ; pince plus haut, serviette, tenir ; "
        "manches, Mila tient, élastique. On s'ajuste. Le bouton de nacre revient, avec une trace.\n\n"
        "## Vécu\n\n"
        "Mila veut la scène **maintenant**. Nino n'est pas prêt, et ce n'est pas « mal ». "
        "Première idée : commencer tout de suite. Ça rate. "
        "Chaque choix change l'obstacle et le climax (verre, mèche, manche). "
        "La leçon se voit : on ne change pas Nino, on change le geste pour que le jeu tienne. "
        "Fin : bouton de nacre + image unique du chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Zoé / Tom / Léa / Sami / bac-toboggan / « on va apprendre » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Héros Mila (`enfant-f`), Nino (`copain`), rythmes distincts, silence = réponse.\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'action. 9 T2, 27 T3, 27 fins.\n"
        "- Indice unique : bouton de nacre (ouverture + climax). Pas d'ancre / étoile / fil pâle.\n"
        "- Ouverture inventée : la maison a allumé la lampe trop tôt.\n"
        "- Corps : sourire parti ; envie et inquiétude ; papa s'accroupit.\n"
        "- Merci vécu (ouverture). Question d'adulte. Un « en ce moment ».\n"
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
