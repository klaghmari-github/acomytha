#!/usr/bin/env python3
"""TREE-AUT-036 — F-NAR-019 v2. Oiseau de papier, sac rouge. TTS complet. Pas d'apply."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-036"
N3 = 16
TICS = ("tout doux", "tout calme", "tout lent", " encore ", " déjà ", "aujourd'hui,")

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "virgule bleue",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le fil s_est tu; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change le ciel; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": "sac",
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_le_tissu; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "sac rouge",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=le_sac_porte_sans_forcer; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=trop_vite_l_aile_plie; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=le_jeu_vole_le_ciel; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "virgule",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=l_oiseau_s_ouvre_seul; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": None,
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_virgule_a_gardé_le_jour; tempo=posé; sourire=léger; respiration=ample",
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
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        low = f" {ph.lower()} "
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"tic {tic!r}: {ph}")
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
    nc["sons"] = sons
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


OPENING = [
    "narrateur|Sarah compte les lunes des rideaux, une par une.",
    "narrateur|Sept tissus bleus, cousus de travers.",
    "narrateur|La septième lune est pliée, un peu.",
    "narrateur|Un rayon passe dans ce pli.",
    "narrateur|Il touche l'aile gauche de l'oiseau.",
    "narrateur|Une virgule bleue y brille, minuscule.",
    "enfant-f|Je t'ai dessinée, toi.",
    "narrateur|L'oiseau de papier pend sous le plafond.",
    "narrateur|Le fil ne tourne pas.",
    "narrateur|Papa plie un pull à étoile.",
    "maman|Tu as vu l'oiseau, Sarah ?",
    "enfant-f|Oui.",
    "enfant-f|Il attend le vrai ciel.",
    "papa|Le parc, tu veux dire ?",
    "enfant-f|Oui, tout de suite !",
    "narrateur|Le sac rouge attend au pied du lit.",
    "narrateur|Les sangles pendent, molles.",
    "narrateur|Ça sent le savon de la lessive.",
    "narrateur|En ce moment, Sarah tire le fil.",
    "narrateur|Trop vite.",
    "narrateur|L'aile se plie.",
    "narrateur|La virgule bleue disparaît dans le pli.",
    "enfant-f|Oh.",
    "enfant-f|Vole, allez !",
    "narrateur|Elle pousse l'oiseau vers la fenêtre.",
    "narrateur|Le papier refuse, rêche.",
    "narrateur|Le bec glisse, pas vers le ciel.",
    "narrateur|Il tombe contre le sac rouge.",
    "narrateur|Le sourire de Sarah disparaît.",
    "narrateur|Envie et inquiétude se bousculent dans sa poitrine.",
    "papa|Il n'a pas voulu, hein ?",
    "narrateur|Papa s'accroupit, à la même hauteur.",
    "maman|Tu le forces, ou tu regardes ?",
    "enfant-f|Je ne sais pas.",
    "narrateur|Sarah pose une main sur le tissu rouge.",
    "narrateur|L'oiseau y reste, sans bouger.",
    "enfant-f|Il veut le sac.",
    "maman|Alors le sac le porte.",
    "papa|On va au parc, avec lui ?",
    "enfant-f|Oui.",
    "narrateur|Une chaussette jaune dort sur la lampe.",
]

T1_CHOICE = [
    "narrateur|Au parc, l'oiseau peut voir trois coins.",
    "papa|Le bac à sable, le toboggan, ou les balançoires ?",
    "maman|Où veux-tu l'emmener d'abord ?",
]

T1 = {
    1: {
        "lab": "le bac à sable",
        "sons": "sable,enfants_parc",
        "emphasis": "sable",
        "passage": [
            "narrateur|Sarah s'agenouille près du bac.",
            "narrateur|Le sable est frais, un peu humide.",
            "enfant-f|Un ciel jaune, pour lui !",
            "narrateur|Elle ouvre le sac d'un coup.",
            "narrateur|L'oiseau penche vers le sable.",
            "narrateur|Un grain colle à la virgule bleue.",
            "enfant-f|Oh, il ne brille plus.",
            "narrateur|Le sourire de Sarah s'en va.",
            "maman|Tu le sors, ou tu regardes ?",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "narrateur|Sarah veut le poser sur le sable.",
            "narrateur|Le papier se plie, rêche.",
            "enfant-f|Il n'aime pas.",
            "papa|Le vent du bac tire l'aile.",
            "narrateur|Sarah rentre l'oiseau, le cœur serré.",
            "narrateur|Le tissu rouge se referme.",
            "enfant-f|Le sac, alors.",
            "narrateur|Un grain reste sur la sangle.",
        ],
        "question": [
            "narrateur|L'oiseau de papier s'est calmé, près du bac.",
            "papa|Sarah l'a mis où ?",
        ],
        "qfields": {
            "expected_answer": "sac",
            "accepted_examples": "sac | le sac | dans le sac | le sac rouge | dedans",
            "retry_prompt": "Le sac rouge. Sarah a mis l'oiseau où ?",
        },
        "confirm": [
            "enfant-f|Dans le sac !",
            "narrateur|Oui, dans le sac rouge.",
            "papa|Merci, Sarah, tu l'as remis.",
            "maman|La virgule peut sécher, là.",
            "enfant-f|Il verra le sable plus tard.",
            "papa|On emporte un jeu, avec lui ?",
            "narrateur|Un grain reste collé à la sangle.",
        ],
    },
    2: {
        "lab": "le toboggan",
        "sons": "toboggan,metal",
        "emphasis": "toboggan",
        "passage": [
            "narrateur|Sarah va vers le toboggan.",
            "narrateur|Le métal est froid sous la paume.",
            "enfant-f|Un vrai vol, en bas !",
            "narrateur|Elle ouvre le sac trop vite.",
            "narrateur|L'aile colle à la marche lisse.",
            "narrateur|La virgule bleue se plie, nette.",
            "enfant-f|Il va se déchirer.",
            "narrateur|Le sourire de Sarah s'en va.",
            "papa|Tu le fais glisser, ou tu attends ?",
            "narrateur|Papa s'accroupit au pied des marches.",
            "narrateur|Sarah tire l'aile, un peu trop.",
            "narrateur|Le papier crie, rêche.",
            "enfant-f|Pardon.",
            "maman|Le sac est plus tiède, non ?",
            "narrateur|Sarah glisse l'oiseau au fond.",
            "narrateur|Le tissu rouge se referme.",
            "enfant-f|Il voyage mieux, là.",
            "narrateur|Une goutte sèche sur le métal.",
        ],
        "question": [
            "narrateur|L'aile ne penche plus, au pied du toboggan.",
            "maman|Sarah a mis l'oiseau où ?",
        ],
        "qfields": {
            "expected_answer": "sac",
            "accepted_examples": "sac | le sac | dans le sac | le sac rouge | dedans",
            "retry_prompt": "Le sac rouge. Sarah a mis l'oiseau où ?",
        },
        "confirm": [
            "enfant-f|Dans le sac !",
            "narrateur|Oui, au fond du sac rouge.",
            "maman|Merci, Sarah, l'aile se repose.",
            "papa|Le métal, lui, reste froid.",
            "enfant-f|Il verra la pente plus tard.",
            "papa|On emporte un jeu, près des marches ?",
            "narrateur|Une goutte sèche sur le plastique.",
        ],
    },
    3: {
        "lab": "les balançoires",
        "sons": "balancoire,chaine",
        "emphasis": "balançoires",
        "passage": [
            "narrateur|Sarah va vers les balançoires.",
            "narrateur|Une chaîne fait tic, légère.",
            "enfant-f|Le vent, pour lui !",
            "narrateur|Elle pose l'oiseau sur le siège.",
            "narrateur|La chaîne tire, d'un coup.",
            "narrateur|La virgule bleue part de travers.",
            "enfant-f|Il s'envole trop !",
            "narrateur|Le sourire de Sarah s'en va.",
            "maman|Tu le retiens, ou tu le ranges ?",
            "narrateur|Maman s'accroupit dans l'herbe.",
            "narrateur|Sarah rattrape l'aile, le cœur serré.",
            "narrateur|Le papier tremble, puis se tait.",
            "enfant-f|J'ai eu peur.",
            "papa|Le sac arrête le tic, lui.",
            "narrateur|Sarah rentre l'oiseau, sans le plier.",
            "narrateur|Le tissu rouge se referme.",
            "enfant-f|Il est dedans.",
            "narrateur|Un brin d'herbe colle à la sangle.",
        ],
        "question": [
            "narrateur|Le vent n'emporte plus le papier.",
            "papa|Sarah a mis l'oiseau où ?",
        ],
        "qfields": {
            "expected_answer": "sac",
            "accepted_examples": "sac | le sac | dans le sac | le sac rouge | dedans",
            "retry_prompt": "Le sac rouge. Sarah a mis l'oiseau où ?",
        },
        "confirm": [
            "enfant-f|Dans le sac !",
            "narrateur|Oui, dans le sac rouge.",
            "papa|Merci, Sarah, tu l'as rattrapé.",
            "maman|La chaîne peut tic, sans lui.",
            "enfant-f|Il verra le vent plus tard.",
            "papa|On emporte un jeu, dans l'herbe ?",
            "narrateur|Un brin d'herbe reste sur le tissu.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le bac a un jeu qui attend.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Qu'est-ce que tu prends, près du sac ?",
    ],
    2: [
        "narrateur|Près des marches, un jeu attend.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Qu'est-ce que tu prends, près du sac ?",
    ],
    3: [
        "narrateur|Dans l'herbe, un jeu attend.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Qu'est-ce que tu prends, près du sac ?",
    ],
}

T2 = {
    (1, 1): {
        "lab": "le ballon",
        "sons": "ballon,sable",
        "emphasis": "ballon",
        "passage": [
            "narrateur|Près du bac, le ballon rouge attend.",
            "enfant-f|Je dribble, et lui vole !",
            "narrateur|Sarah pose le sac pour frapper.",
            "narrateur|Le ballon tape le tissu, boum.",
            "narrateur|L'oiseau bascule, presque dehors.",
            "enfant-f|Non !",
            "narrateur|Elle retient sa main, nette.",
            "papa|Le ballon a volé trop près.",
            "maman|Tu fonces, ou tu poses le jeu ?",
            "narrateur|Sarah pose le ballon dans le sable.",
            "narrateur|Elle écoute le bac : rien, presque.",
            "enfant-f|La virgule a bougé.",
            "narrateur|Un grain colle au cuir lisse.",
        ],
    },
    (1, 2): {
        "lab": "le seau",
        "sons": "seau,sable",
        "emphasis": "seau",
        "passage": [
            "narrateur|Près du bac, le seau jaune est là.",
            "enfant-f|Un nid, comme le sac !",
            "narrateur|Sarah verse du sable dans l'anse.",
            "narrateur|Elle veut y glisser l'oiseau.",
            "narrateur|La virgule bleue disparaît au fond.",
            "enfant-f|Il ne voit plus.",
            "narrateur|Elle retient sa main, nette.",
            "papa|Le seau n'est pas un ciel.",
            "maman|Tu le sors, sans le plier ?",
            "narrateur|Sarah relève l'oiseau, grain par grain.",
            "narrateur|Elle le remet dans le sac rouge.",
            "enfant-f|Le sac, lui, a de l'air.",
            "narrateur|Du sable reste au fond du seau.",
        ],
    },
    (1, 3): {
        "lab": "le doudou",
        "sons": "tissu,sable",
        "emphasis": "doudou",
        "passage": [
            "narrateur|Près du bac, le doudou gris attend.",
            "enfant-f|Je l'essuie, hop !",
            "narrateur|Sarah frotte l'aile trop fort.",
            "narrateur|Puis elle enveloppe tout le papier.",
            "narrateur|La virgule bleue disparaît sous le gris.",
            "enfant-f|Il étouffe.",
            "narrateur|Elle retient sa main, nette.",
            "maman|Le doudou chauffe trop, non ?",
            "papa|Tu le sors, ou tu serres ?",
            "narrateur|Sarah défait le nœud, lentement.",
            "narrateur|Elle glisse l'oiseau dans le sac.",
            "enfant-f|Le sac laisse l'aile.",
            "narrateur|Le doudou a un grain sur l'oreille.",
        ],
    },
    (2, 1): {
        "lab": "le ballon",
        "sons": "ballon,metal",
        "emphasis": "ballon",
        "passage": [
            "narrateur|Près du toboggan, le ballon rouge attend.",
            "enfant-f|Il glisse sur le ballon !",
            "narrateur|Sarah pose le cuir sur la marche.",
            "narrateur|Elle pose l'oiseau dessus, vite.",
            "narrateur|Le ballon part, l'aile s'envole.",
            "enfant-f|Reviens !",
            "narrateur|Elle rattrape le papier, le cœur serré.",
            "papa|Le ballon a pris la pente.",
            "maman|Tu recommences, ou tu poses ?",
            "narrateur|Sarah pose le ballon au pied.",
            "narrateur|Elle rentre l'oiseau dans le sac.",
            "enfant-f|Pas de pente, pour lui.",
            "narrateur|Une trace de métal reste au cuir.",
        ],
    },
    (2, 2): {
        "lab": "le seau",
        "sons": "seau,metal",
        "emphasis": "seau",
        "passage": [
            "narrateur|Près du toboggan, le seau jaune attend.",
            "enfant-f|Il atterrit dedans !",
            "narrateur|Sarah pose le seau au bas des marches.",
            "narrateur|Elle veut lancer l'oiseau, comme un glissé.",
            "narrateur|L'aile touche le plastique, trop sec.",
            "enfant-f|Ça claque.",
            "narrateur|Elle retient sa main, nette.",
            "papa|Le seau n'est pas une piste.",
            "maman|Tu le poses, ou tu le lances ?",
            "narrateur|Sarah pose le seau à côté.",
            "narrateur|Elle rentre l'oiseau, sans le jeter.",
            "enfant-f|Le sac amortit, lui.",
            "narrateur|L'anse du seau a une goutte froide.",
        ],
    },
    (2, 3): {
        "lab": "le doudou",
        "sons": "tissu,metal",
        "emphasis": "doudou",
        "passage": [
            "narrateur|Près du toboggan, le doudou gris attend.",
            "enfant-f|Un tapis pour glisser !",
            "narrateur|Sarah étend le doudou sur la pente.",
            "narrateur|Elle y pose l'oiseau, trop haut.",
            "narrateur|Le tissu part, l'aile se tord.",
            "enfant-f|Doucement !",
            "narrateur|Elle retient le doudou, nette.",
            "maman|Le tapis va trop vite.",
            "papa|Tu le ranges, ou tu pousses ?",
            "narrateur|Sarah ramasse le doudou, puis l'oiseau.",
            "narrateur|Elle le glisse dans le sac rouge.",
            "enfant-f|Le sac ne glisse pas.",
            "narrateur|Le doudou a touché la marche lisse.",
        ],
    },
    (3, 1): {
        "lab": "le ballon",
        "sons": "ballon,chaine",
        "emphasis": "ballon",
        "passage": [
            "narrateur|Près des balançoires, le ballon rouge attend.",
            "enfant-f|Je tape, et lui vole !",
            "narrateur|Sarah pose le sac sur le siège.",
            "narrateur|Le ballon rebondit sous la chaîne.",
            "narrateur|La chaîne tape le tissu, tic dur.",
            "enfant-f|Le sac bascule !",
            "narrateur|Elle rattrape la sangle, nette.",
            "papa|Le ballon a réveillé la chaîne.",
            "maman|Tu tapes, ou tu poses le jeu ?",
            "narrateur|Sarah pose le ballon dans l'herbe.",
            "narrateur|Elle serre le sac contre elle.",
            "enfant-f|Plus de tic, pour lui.",
            "narrateur|Un brin d'herbe colle au cuir.",
        ],
    },
    (3, 2): {
        "lab": "le seau",
        "sons": "seau,chaine",
        "emphasis": "seau",
        "passage": [
            "narrateur|Près des balançoires, le seau jaune attend.",
            "enfant-f|Il se balance dans le seau !",
            "narrateur|Sarah pose le seau sur le siège.",
            "narrateur|Elle y glisse l'oiseau, trop vite.",
            "narrateur|La chaîne bouge, le seau penche.",
            "enfant-f|Il va tomber !",
            "narrateur|Elle retient l'anse, nette.",
            "papa|Le seau n'est pas une balançoire.",
            "maman|Tu le sors, ou tu pousses ?",
            "narrateur|Sarah sort l'oiseau, sans le plier.",
            "narrateur|Elle le remet dans le sac rouge.",
            "enfant-f|Le sac tient, lui.",
            "narrateur|L'anse du seau est froide, un peu.",
        ],
    },
    (3, 3): {
        "lab": "le doudou",
        "sons": "tissu,chaine",
        "emphasis": "doudou",
        "passage": [
            "narrateur|Près des balançoires, le doudou gris attend.",
            "enfant-f|Un siège tout chaud !",
            "narrateur|Sarah pose le doudou sur la planche.",
            "narrateur|Elle y cache l'oiseau, serré.",
            "narrateur|La virgule bleue disparaît sous l'oreille.",
            "enfant-f|Il ne peut plus.",
            "narrateur|Elle défait le pli, nette.",
            "maman|Le doudou étouffe l'aile, non ?",
            "papa|Tu le sors, ou tu le couvres ?",
            "narrateur|Sarah sort le papier, lentement.",
            "narrateur|Elle le glisse dans le sac.",
            "enfant-f|Le sac a de la place.",
            "narrateur|L'oreille du doudou est froide, un peu.",
        ],
    },
}

T3_CHOICE = {
    1: [
        "narrateur|Sarah pose le ballon, sans frapper.",
        "papa|Le banc, la grille, ou le cerisier ?",
        "maman|Où poses-tu le sac, ouvert ?",
    ],
    2: [
        "narrateur|Sarah pose le seau, sans verser.",
        "papa|Le banc, la grille, ou le cerisier ?",
        "maman|Où poses-tu le sac, ouvert ?",
    ],
    3: [
        "narrateur|Sarah pose le doudou, sans serrer.",
        "papa|Le banc, la grille, ou le cerisier ?",
        "maman|Où poses-tu le sac, ouvert ?",
    ],
}

T3 = {
    (1, 1, 1): [
        "narrateur|Le banc du parc est frais, strié.",
        "narrateur|Sarah y pose le sac, ouvert.",
        "narrateur|Le ballon reste dans le sable, loin.",
        "enfant-f|Je pourrais le pousser.",
        "narrateur|Elle retient sa main.",
        "narrateur|Le banc ne dit rien.",
        "narrateur|Elle regarde la virgule bleue.",
        "narrateur|Un grain tombe, tout seul.",
        "narrateur|L'aile se déplie, sans elle.",
        "papa|Il a choisi le bois, on dirait.",
        "enfant-f|Il s'ouvre.",
        "narrateur|Le cuir du ballon a du sable, au loin.",
    ],
    (1, 1, 2): [
        "narrateur|La grille du parc est verte, froide.",
        "narrateur|Sarah tient le sac près des barres.",
        "narrateur|Le ballon roule, presque contre.",
        "enfant-f|Je pourrais le caler là.",
        "narrateur|Elle recule le cuir, nette.",
        "narrateur|Le vent passe entre deux barres.",
        "narrateur|La virgule bleue se tourne vers lui.",
        "narrateur|L'oiseau penche, sans main.",
        "maman|Le vent de la grille, pas celui du ballon.",
        "enfant-f|Il a vu le trou.",
        "narrateur|Une feuille coincée tremble, puis se tait.",
        "narrateur|Le sac reste ouvert, contre rien.",
    ],
    (1, 1, 3): [
        "narrateur|Le cerisier penche au bord du parc.",
        "narrateur|Sarah accroche le sac à une branche basse.",
        "narrateur|Le ballon reste au bac, oublié.",
        "enfant-f|Je pourrais le jeter en l'air.",
        "narrateur|Elle laisse le cuir au sol.",
        "narrateur|Une pétale rose tombe sur l'aile.",
        "narrateur|La virgule bleue luit sous le rose.",
        "narrateur|L'oiseau se tient, comme au plafond.",
        "papa|Le fil, ici, c'est la branche.",
        "enfant-f|Il ne tombe pas.",
        "narrateur|La pétale reste, légère.",
        "narrateur|Le ballon, au loin, ne rebondit plus.",
    ],
    (1, 2, 1): [
        "narrateur|Le banc du parc sent le bois tiède.",
        "narrateur|Sarah y pose le sac, à peine ouvert.",
        "narrateur|Le seau reste plein de sable, à côté.",
        "enfant-f|Je pourrais le verser sur le bois.",
        "narrateur|Elle pose l'anse, sans verser.",
        "narrateur|Elle écoute le banc : un craquement mince.",
        "narrateur|La virgule bleue se lève, un peu.",
        "narrateur|L'aile quitte le tissu, toute seule.",
        "maman|Le bois tient, sans nid de sable.",
        "enfant-f|Il a sa place.",
        "narrateur|Du sable reste au fond du seau, loin de l'aile.",
        "narrateur|Une miette de pain brille sur le bois.",
    ],
    (1, 2, 2): [
        "narrateur|La grille du parc tient une feuille.",
        "narrateur|Sarah pose le sac contre une barre.",
        "narrateur|Le seau tapote, toc, trop près.",
        "enfant-f|Je pourrais coincer l'anse.",
        "narrateur|Elle recule le jaune, nette.",
        "narrateur|L'air file dans les trous verts.",
        "narrateur|La virgule bleue pointe le trou.",
        "narrateur|L'oiseau s'ouvre, face au parc.",
        "papa|Le seau n'a pas de vent, lui.",
        "enfant-f|La grille, si.",
        "narrateur|La feuille coincée claque, une fois.",
        "narrateur|Le sac reste, sans anse dessus.",
    ],
    (1, 2, 3): [
        "narrateur|Le cerisier fait une ombre ronde.",
        "narrateur|Sarah pose le sac dans l'herbe, ouvert.",
        "narrateur|Le seau reste au bac, lourd.",
        "enfant-f|Je pourrais l'accrocher aussi.",
        "narrateur|Elle laisse l'anse au sable.",
        "narrateur|Une pétale tombe dans le tissu rouge.",
        "narrateur|La virgule bleue la touche, puis se lève.",
        "narrateur|L'oiseau se déplie, sous les feuilles.",
        "maman|L'arbre porte, sans seau.",
        "enfant-f|Il est à lui.",
        "narrateur|La pétale reste au bord du sac.",
        "narrateur|Le seau, au bac, ne bouge plus.",
    ],
    (1, 3, 1): [
        "narrateur|Le banc du parc a une miette, et du bois.",
        "narrateur|Sarah y pose le sac, ouvert.",
        "narrateur|Le doudou reste sur ses genoux, plié.",
        "enfant-f|Je pourrais le couvrir.",
        "narrateur|Elle laisse le gris sur les genoux.",
        "narrateur|Le bois tiédit le tissu rouge.",
        "narrateur|La virgule bleue sort du pli, lente.",
        "narrateur|L'aile s'étale, sans couverture.",
        "papa|Le doudou a assez chauffé, au bac.",
        "enfant-f|Là, il respire.",
        "narrateur|L'oreille du doudou a un grain, et se tait.",
        "narrateur|La miette reste, à côté de l'aile.",
    ],
    (1, 3, 2): [
        "narrateur|La grille du parc est froide, verte.",
        "narrateur|Sarah tient le sac près d'une barre.",
        "narrateur|Le doudou glisse vers le fer.",
        "enfant-f|Je pourrais caler l'oreille.",
        "narrateur|Elle ramène le gris, nette.",
        "narrateur|Le vent de la grille lèche l'aile.",
        "narrateur|La virgule bleue se tourne, nette.",
        "narrateur|L'oiseau s'ouvre, face aux trous.",
        "maman|Le doudou n'a pas de vent.",
        "enfant-f|La grille en a.",
        "narrateur|L'oreille du doudou frotte la feuille coincée, puis recule.",
        "narrateur|Le papier tient, sans gris dessus.",
    ],
    (1, 3, 3): [
        "narrateur|Le cerisier sent la feuille tiède.",
        "narrateur|Sarah accroche le sac, un instant.",
        "narrateur|Le doudou reste dans l'herbe, loin.",
        "enfant-f|Je pourrais le nouer à la branche.",
        "narrateur|Elle laisse le gris au sol.",
        "narrateur|Une pétale se pose sur l'aile.",
        "narrateur|La virgule bleue brille sous le rose.",
        "narrateur|L'oiseau se tient, comme au fil.",
        "papa|Le doudou n'est pas un fil.",
        "enfant-f|La branche, si.",
        "narrateur|Le doudou sent la pétale, sans la prendre.",
        "narrateur|Le sac pend, et l'aile ne tombe pas.",
    ],
    (2, 1, 1): [
        "narrateur|Le banc du parc est lisse, un peu froid.",
        "narrateur|Sarah y pose le sac, ouvert.",
        "narrateur|Le ballon reste au pied du toboggan.",
        "enfant-f|Je pourrais le faire rebondir ici.",
        "narrateur|Elle laisse le cuir aux marches.",
        "narrateur|Le bois ne glisse pas.",
        "narrateur|La virgule bleue se déplie, droite.",
        "narrateur|L'aile quitte le fond, toute seule.",
        "maman|Le banc n'a pas de pente.",
        "enfant-f|Juste une place.",
        "narrateur|Le ballon a une trace de métal, au loin.",
        "narrateur|Une miette tient sur le bois, près du bec.",
    ],
    (2, 1, 2): [
        "narrateur|La grille du parc coupe le vent en lames.",
        "narrateur|Sarah tient le sac contre une barre.",
        "narrateur|Le ballon roule vers le fer.",
        "enfant-f|Je pourrais le coincer.",
        "narrateur|Elle recule le cuir, nette.",
        "narrateur|L'air des barres lèche la virgule bleue.",
        "narrateur|L'oiseau se tourne, sans pente.",
        "papa|Le toboggan glissait, la grille souffle.",
        "enfant-f|Il aime ce vent-là.",
        "narrateur|Une goutte du toboggan sèche sur la barre.",
        "narrateur|Le sac reste, sans rebond.",
        "narrateur|La feuille coincée claque, puis se tait.",
    ],
    (2, 1, 3): [
        "narrateur|Le cerisier fait un plafond de feuilles.",
        "narrateur|Sarah accroche le sac à une branche.",
        "narrateur|Le ballon reste au pied du toboggan.",
        "enfant-f|Je pourrais le lancer dans l'arbre.",
        "narrateur|Elle laisse le cuir au métal.",
        "narrateur|Une pétale tombe, plus lente qu'un ballon.",
        "narrateur|La virgule bleue la suit, puis s'arrête.",
        "narrateur|L'oiseau se tient, sous le vert.",
        "maman|Pas de pente, pas de rebond.",
        "enfant-f|Un fil d'arbre.",
        "narrateur|Le ballon, au loin, ne part plus.",
        "narrateur|La pétale reste sur l'aile, légère.",
    ],
    (2, 2, 1): [
        "narrateur|Le banc du parc a des stries, et du soleil.",
        "narrateur|Sarah y pose le sac, ouvert.",
        "narrateur|Le seau reste au bas des marches.",
        "enfant-f|Je pourrais le poser en atterrissage.",
        "narrateur|Elle laisse l'anse au plastique.",
        "narrateur|Le bois accueille le tissu, plat.",
        "narrateur|La virgule bleue sort, sans claquer.",
        "narrateur|L'aile s'ouvre, sur le banc.",
        "papa|Le seau claquait, le bois non.",
        "enfant-f|Il s'installe.",
        "narrateur|L'anse du seau a une goutte, loin du bois.",
        "narrateur|Une miette brille, près du bec.",
    ],
    (2, 2, 2): [
        "narrateur|La grille du parc est verte, trouée.",
        "narrateur|Sarah pose le sac contre une barre.",
        "narrateur|Le seau tapote trop près, toc.",
        "enfant-f|Je pourrais coincer l'anse.",
        "narrateur|Elle recule le jaune, nette.",
        "narrateur|Le vent des trous tourne la virgule bleue.",
        "narrateur|L'oiseau s'ouvre, face au parc.",
        "maman|Pas d'atterrissage, juste de l'air.",
        "enfant-f|Il n'a pas claqué.",
        "narrateur|Le seau jaune brille près de la barre, sans toucher.",
        "narrateur|La feuille coincée se tait.",
        "narrateur|Le papier tient, ouvert.",
    ],
    (2, 2, 3): [
        "narrateur|Le cerisier penche, ombre tiède.",
        "narrateur|Sarah pose le sac dans l'herbe, ouvert.",
        "narrateur|Le seau reste au toboggan, vide de vol.",
        "enfant-f|Je pourrais l'accrocher.",
        "narrateur|Elle laisse l'anse au métal.",
        "narrateur|Une pétale tombe dans le rouge.",
        "narrateur|La virgule bleue se lève dessous.",
        "narrateur|L'oiseau se déplie, sans piste.",
        "papa|L'arbre n'est pas un toboggan.",
        "enfant-f|Mieux.",
        "narrateur|L'anse du seau tient une pétale, au loin.",
        "narrateur|Le sac, lui, tient l'aile.",
    ],
    (2, 3, 1): [
        "narrateur|Le banc du parc est large, un peu rêche.",
        "narrateur|Sarah y pose le sac, ouvert.",
        "narrateur|Le doudou reste plié, sur la marche.",
        "enfant-f|Je pourrais le tapis ici.",
        "narrateur|Elle laisse le gris au métal.",
        "narrateur|Le bois ne part pas en pente.",
        "narrateur|La virgule bleue se montre, droite.",
        "narrateur|L'aile s'étale, sans tapis.",
        "maman|Le doudou glissait, le banc non.",
        "enfant-f|Il reste.",
        "narrateur|Le doudou a touché la marche, puis le bois, de loin.",
        "narrateur|Une miette tient, près du bec.",
    ],
    (2, 3, 2): [
        "narrateur|La grille du parc tient le vent, et une feuille.",
        "narrateur|Sarah tient le sac près des barres.",
        "narrateur|Le doudou glisse vers le fer.",
        "enfant-f|Je pourrais le caler.",
        "narrateur|Elle ramène le gris, nette.",
        "narrateur|L'air des barres lèche l'aile froide.",
        "narrateur|La virgule bleue se tourne vers le trou.",
        "narrateur|L'oiseau s'ouvre, sans tapis.",
        "papa|Le doudou étouffait, la grille souffle.",
        "enfant-f|Il respire.",
        "narrateur|Une goutte du toboggan sèche sur le doudou.",
        "narrateur|Le papier, lui, reste sec et ouvert.",
    ],
    (2, 3, 3): [
        "narrateur|Le cerisier fait un toit de feuilles.",
        "narrateur|Sarah accroche le sac, un instant.",
        "narrateur|Le doudou reste au pied du toboggan.",
        "enfant-f|Je pourrais le nouer.",
        "narrateur|Elle laisse le gris au métal.",
        "narrateur|Une pétale se pose, plus douce qu'un tapis.",
        "narrateur|La virgule bleue luit dessous.",
        "narrateur|L'oiseau se tient, sous la branche.",
        "maman|Pas de pente, pas de nœud.",
        "enfant-f|Un vrai plafond.",
        "narrateur|Le doudou passe sous une branche, sans s'accrocher.",
        "narrateur|Le sac pend, fidèle.",
    ],
    (3, 1, 1): [
        "narrateur|Le banc du parc est calme, sans chaîne.",
        "narrateur|Sarah y pose le sac, ouvert.",
        "narrateur|Le ballon reste dans l'herbe des balançoires.",
        "enfant-f|Je pourrais taper ici.",
        "narrateur|Elle laisse le cuir à l'herbe.",
        "narrateur|Le bois ne fait pas tic.",
        "narrateur|La virgule bleue se lève, droite.",
        "narrateur|L'aile s'ouvre, sans rebond.",
        "papa|La chaîne tapait, le banc non.",
        "enfant-f|Il s'installe.",
        "narrateur|Le ballon a pris le tic, au loin, puis s'est tu.",
        "narrateur|Une miette brille, près du bec.",
    ],
    (3, 1, 2): [
        "narrateur|La grille du parc file un vent droit.",
        "narrateur|Sarah tient le sac contre une barre.",
        "narrateur|Le ballon rebondit, trop près.",
        "enfant-f|Je pourrais le caler.",
        "narrateur|Elle recule le cuir, nette.",
        "narrateur|Le vent des barres n'est pas un tic.",
        "narrateur|La virgule bleue se tourne, lente.",
        "narrateur|L'oiseau penche, face aux trous.",
        "maman|La chaîne tirait, la grille guide.",
        "enfant-f|Il suit ce vent-là.",
        "narrateur|Le ballon frotte la feuille coincée, puis recule.",
        "narrateur|Le sac reste ouvert, sans siège.",
    ],
    (3, 1, 3): [
        "narrateur|Le cerisier penche, sans chaîne.",
        "narrateur|Sarah accroche le sac à une branche.",
        "narrateur|Le ballon reste sous les balançoires.",
        "enfant-f|Je pourrais le lancer.",
        "narrateur|Elle laisse le cuir à l'herbe.",
        "narrateur|Une pétale tombe, plus lente qu'un rebond.",
        "narrateur|La virgule bleue la suit, puis se tient.",
        "narrateur|L'oiseau pend, comme au plafond.",
        "papa|Pas de tic, pas de boum.",
        "enfant-f|Un fil d'arbre.",
        "narrateur|Un brin d'herbe colle au ballon, sous l'arbre, loin.",
        "narrateur|La pétale reste sur l'aile.",
    ],
    (3, 2, 1): [
        "narrateur|Le banc du parc est plat, sans siège qui bouge.",
        "narrateur|Sarah y pose le sac, ouvert.",
        "narrateur|Le seau reste dans l'herbe des balançoires.",
        "enfant-f|Je pourrais le poser ici.",
        "narrateur|Elle laisse l'anse à l'herbe.",
        "narrateur|Le bois ne penche pas.",
        "narrateur|La virgule bleue sort, sans anse.",
        "narrateur|L'aile s'étale, sur le banc.",
        "maman|Le seau penchait, le banc tient.",
        "enfant-f|Il a de la place.",
        "narrateur|Du sable du seau reste sur le banc, loin de l'aile.",
        "narrateur|Une miette brille, à côté.",
    ],
    (3, 2, 2): [
        "narrateur|La grille du parc est verte, immobile.",
        "narrateur|Sarah pose le sac contre une barre.",
        "narrateur|Le seau tapote, toc, trop près.",
        "enfant-f|Je pourrais coincer l'anse.",
        "narrateur|Elle recule le jaune, nette.",
        "narrateur|Le vent des trous tourne la virgule bleue.",
        "narrateur|L'oiseau s'ouvre, sans balançoire.",
        "papa|Le seau penchait, la grille non.",
        "enfant-f|Il tient.",
        "narrateur|Le seau tapote la barre, une fois, puis se tait.",
        "narrateur|La feuille coincée reste.",
        "narrateur|Le papier, lui, reste ouvert.",
    ],
    (3, 2, 3): [
        "narrateur|Le cerisier fait une ombre fixe.",
        "narrateur|Sarah pose le sac dans l'herbe, ouvert.",
        "narrateur|Le seau reste sous les balançoires.",
        "enfant-f|Je pourrais l'accrocher.",
        "narrateur|Elle laisse l'anse à l'herbe.",
        "narrateur|Une pétale tombe dans le rouge.",
        "narrateur|La virgule bleue se lève dessous.",
        "narrateur|L'oiseau se déplie, sans siège.",
        "maman|L'arbre ne penche pas comme une chaîne.",
        "enfant-f|Il reste.",
        "narrateur|Le seau jaune brille sous le cerisier, vide d'oiseau.",
        "narrateur|La pétale reste au bord du sac.",
    ],
    (3, 3, 1): [
        "narrateur|Le banc du parc est nu, sans doudou.",
        "narrateur|Sarah y pose le sac, ouvert.",
        "narrateur|Le doudou reste dans l'herbe des balançoires.",
        "enfant-f|Je pourrais le couvrir.",
        "narrateur|Elle laisse le gris à l'herbe.",
        "narrateur|Le bois laisse l'air, large.",
        "narrateur|La virgule bleue sort du fond, lente.",
        "narrateur|L'aile s'étale, sans oreille dessus.",
        "papa|Le doudou cachait, le banc montre.",
        "enfant-f|Il se voit.",
        "narrateur|L'oreille du doudou a pris le bois, de loin.",
        "narrateur|Une miette tient, près du bec.",
    ],
    (3, 3, 2): [
        "narrateur|La grille du parc file un air mince.",
        "narrateur|Sarah tient le sac près des barres.",
        "narrateur|Le doudou glisse vers le fer.",
        "enfant-f|Je pourrais caler l'oreille.",
        "narrateur|Elle ramène le gris, nette.",
        "narrateur|Le vent des barres lèche l'aile.",
        "narrateur|La virgule bleue se tourne, nette.",
        "narrateur|L'oiseau s'ouvre, sans couverture.",
        "maman|Le doudou étouffait, la grille souffle.",
        "enfant-f|Il respire.",
        "narrateur|Le doudou passe sous la barre verte, puis recule.",
        "narrateur|Le papier tient, face aux trous.",
    ],
    (3, 3, 3): [
        "narrateur|Le cerisier sent la feuille, et le jour.",
        "narrateur|Sarah accroche le sac, un instant.",
        "narrateur|Le doudou reste sous les balançoires.",
        "enfant-f|Je pourrais le nouer.",
        "narrateur|Elle laisse le gris à l'herbe.",
        "narrateur|Une pétale se pose sur l'aile.",
        "narrateur|La virgule bleue brille sous le rose.",
        "narrateur|L'oiseau se tient, comme au fil du plafond.",
        "papa|Pas de nœud, pas de siège.",
        "enfant-f|Un vrai ciel.",
        "narrateur|L'oreille du doudou a une pétale, au sol.",
        "narrateur|Le sac pend, et l'aile ne tombe pas.",
    ],
}

T3_SONS = {1: "banc,bois", 2: "grille,vent", 3: "cerisier,petale"}
T3_EMPH = {1: "banc", 2: "grille", 3: "cerisier"}
T2_EMPH = {1: "ballon", 2: "seau", 3: "doudou"}
END_SONS = {1: "ballon,chambre", 2: "seau,chambre", 3: "doudou,chambre"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Ils rentrent, le sac un peu sablé.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le grain sur la virgule.",
        "maman|Le ballon est resté au bac, lui.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|La virgule bleue brille sous la lampe, sans pli.",
    ],
    (1, 1, 2): [
        "narrateur|Ils rentrent, le vent des barres dans les oreilles.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le ballon trop près.",
        "maman|La grille a gardé sa feuille.",
        "narrateur|Sarah pose le sac, ouvert un peu.",
        "narrateur|La septième lune des rideaux s'est dépliée.",
    ],
    (1, 1, 3): [
        "narrateur|Ils rentrent, une pétale dans le rouge.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout quand j'ai voulu lancer.",
        "maman|La branche a tenu, sans toi.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|Le fil du plafond reste vide, et c'est bien.",
    ],
    (1, 2, 1): [
        "narrateur|Ils rentrent, le seau vide d'oiseau.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le nid de sable.",
        "maman|Le banc a suffi, plat.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|La chaussette jaune a glissé sur le bois de la lampe.",
    ],
    (1, 2, 2): [
        "narrateur|Ils rentrent, l'anse froide dans la main.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le fond du seau.",
        "maman|La grille a donné l'air, elle.",
        "narrateur|Sarah pose le sac, un peu ouvert.",
        "narrateur|Le pull à étoile garde un grain de sable au col.",
    ],
    (1, 2, 3): [
        "narrateur|Ils rentrent, une pétale au bord du tissu.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout quand j'ai voulu verser.",
        "maman|L'arbre n'avait pas besoin du seau.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|Les sangles du sac sentent la feuille, un peu.",
    ],
    (1, 3, 1): [
        "narrateur|Ils rentrent, le doudou plié, l'oiseau libre.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le nœud trop serré.",
        "maman|Le banc a laissé l'air.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|Un rayon manque la virgule, puis la trouve.",
    ],
    (1, 3, 2): [
        "narrateur|Ils rentrent, l'oreille du doudou un peu froide.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout quand je cachais l'aile.",
        "maman|La grille a soufflé, elle.",
        "narrateur|Sarah pose le sac, ouvert un peu.",
        "narrateur|Le savon de la lessive mélange une odeur de fer.",
    ],
    (1, 3, 3): [
        "narrateur|Ils rentrent, une pétale collée au gris.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le nœud à la branche.",
        "maman|L'arbre tenait tout seul.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|La virgule bleue regarde les lunes, de biais.",
    ],
    (2, 1, 1): [
        "narrateur|Ils rentrent, le métal loin derrière.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le ballon sur la pente.",
        "maman|Le banc n'avait pas de glissé.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|Le sac rouge sèche, ouvert, au pied du lit.",
    ],
    (2, 1, 2): [
        "narrateur|Ils rentrent, une barre dans le souvenir du papier.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le rebond trop près.",
        "maman|La grille a soufflé droit.",
        "narrateur|Sarah pose le sac, un peu ouvert.",
        "narrateur|Papa repose le pull : une sangle y pend.",
    ],
    (2, 1, 3): [
        "narrateur|Ils rentrent, une pétale plus lente qu'un ballon.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout quand j'ai voulu lancer.",
        "maman|L'arbre n'est pas une pente.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|La lampe éclaire un grain collé à l'aile.",
    ],
    (2, 2, 1): [
        "narrateur|Ils rentrent, l'anse sans atterrissage.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le clac du seau.",
        "maman|Le bois n'a pas claqué.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|Le fil vide fait un cercle d'ombre, minuscule.",
    ],
    (2, 2, 2): [
        "narrateur|Ils rentrent, le jaune loin des barres.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout quand j'ai voulu lancer.",
        "maman|La grille a donné l'air, sans toc.",
        "narrateur|Sarah pose le sac, ouvert un peu.",
        "narrateur|Une barre de grille reste dans le souvenir du papier.",
    ],
    (2, 2, 3): [
        "narrateur|Ils rentrent, une pétale au fond du rouge.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout la piste trop sèche.",
        "maman|L'arbre n'était pas un toboggan.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|La virgule pointe vers les lunes, pas vers la fenêtre.",
    ],
    (2, 3, 1): [
        "narrateur|Ils rentrent, le doudou plié, sans tapis.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le glissé trop vite.",
        "maman|Le banc est resté, lui.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|Le doudou a pris l'odeur du sac, au lit.",
    ],
    (2, 3, 2): [
        "narrateur|Ils rentrent, une goutte sèche sur le gris.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le tapis de pente.",
        "maman|La grille a soufflé, sans étouffer.",
        "narrateur|Sarah pose le sac, un peu ouvert.",
        "narrateur|L'oreille du doudou garde une goutte de métal.",
    ],
    (2, 3, 3): [
        "narrateur|Ils rentrent, un toit de feuilles dans la tête.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le nœud trop haut.",
        "maman|La branche tenait, sans doudou.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|Une pétale sèche sur l'oreille du doudou.",
    ],
    (3, 1, 1): [
        "narrateur|Ils rentrent, la chaîne loin derrière.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le tic sur le sac.",
        "maman|Le banc n'a pas tapé.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|Le ballon s'endort contre les sangles molles.",
    ],
    (3, 1, 2): [
        "narrateur|Ils rentrent, un vent droit dans les oreilles.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le ballon sous la chaîne.",
        "maman|La grille a guidé, elle.",
        "narrateur|Sarah pose le sac, ouvert un peu.",
        "narrateur|Sarah pose un doigt à côté de la virgule, sans toucher.",
    ],
    (3, 1, 3): [
        "narrateur|Ils rentrent, une pétale plus lente qu'un tic.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le lancer dans l'arbre.",
        "maman|La branche n'avait pas besoin du ballon.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|Le tissu rouge a une trace de bois, fine.",
    ],
    (3, 2, 1): [
        "narrateur|Ils rentrent, l'anse sans siège.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le seau qui penchait.",
        "maman|Le banc est resté plat.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|Les lunes des rideaux bougent, sans vent de parc.",
    ],
    (3, 2, 2): [
        "narrateur|Ils rentrent, le toc du seau oublié.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout l'anse coincée.",
        "maman|La grille n'a pas penché.",
        "narrateur|Sarah pose le sac, un peu ouvert.",
        "narrateur|L'oiseau de papier penche, comme au plafond, mais dans le sac.",
    ],
    (3, 2, 3): [
        "narrateur|Ils rentrent, une ombre d'arbre dans les yeux.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le seau sous la chaîne.",
        "maman|L'arbre était fixe, lui.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|La chaussette jaune cache un brin d'herbe.",
    ],
    (3, 3, 1): [
        "narrateur|Ils rentrent, le doudou déplié, l'oiseau vu.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout l'oreille sur l'aile.",
        "maman|Le banc a montré, sans cacher.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|Un trait d'or manque, entre deux lunes.",
    ],
    (3, 3, 2): [
        "narrateur|Ils rentrent, un air mince dans les cheveux.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le gris trop serré.",
        "maman|La grille a laissé l'aile.",
        "narrateur|Sarah pose le sac, ouvert un peu.",
        "narrateur|La virgule bleue a gardé un peu de jour.",
    ],
    (3, 3, 3): [
        "narrateur|Ils rentrent, le plafond de feuilles dans la tête.",
        "papa|Tu raconteras le moment difficile ?",
        "enfant-f|Surtout le nœud que j'ai laissé.",
        "maman|La branche a fait le fil, toute seule.",
        "narrateur|Sarah pose le sac au pied du lit.",
        "narrateur|L'oiseau penche dans le rouge, virgule au jour.",
    ],
}


def path_words(chunks_by_id: dict, a: int, b: int, c: int) -> int:
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
    return sum(words(chunks_by_id[i]["text"]) for i in ids)


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "rideau,fil,papier"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "",
        {
            "fields": {
                "option_1_label": "le bac à sable",
                "option_2_label": "le toboggan",
                "option_3_label": "les balançoires",
            }
        },
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
            {"emphasis": "sac", "fields": t1["qfields"]},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], t1["confirm"], "confirm", t1["sons"], {"emphasis": "sac rouge"}
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"],
            T2_CHOICE[a],
            "choice",
            "",
            {
                "fields": {
                    "option_1_label": "le ballon",
                    "option_2_label": "le seau",
                    "option_3_label": "le doudou",
                }
            },
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
                {
                    "fields": {
                        "option_1_label": "le banc",
                        "option_2_label": "la grille",
                        "option_3_label": "le cerisier",
                    }
                },
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf],
                    T3[(a, b, c)],
                    "resolution",
                    T3_SONS[c],
                    {"emphasis": T3_EMPH[c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin],
                    ENDINGS[(a, b, c)],
                    "ending",
                    END_SONS[b],
                    {"emphasis": T3_EMPH[c]},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = set(out_chunks) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:6]} extra={sorted(extra)[:6]}")

    story = dict(src)
    story["fil_rouge"] = (
        "Sarah veut emmener l'oiseau de papier au parc, sous le vrai ciel, dans le sac rouge. "
        "Elle tire le fil trop vite : l'aile se plie, la virgule bleue se cache. L'oiseau glisse "
        "vers le sac, pas vers la fenêtre. Au bac, au toboggan ou aux balançoires, elle ouvre trop "
        "vite. Un jeu (ballon, seau, doudou) gêne. Elle refuse de forcer. Au banc, à la grille ou "
        "sous le cerisier, la virgule se montre : l'oiseau s'ouvre tout seul."
    )
    story["title"] = "L'oiseau de papier et le sac rouge de Sarah"
    story["characters"] = "Sarah, papa, maman"
    story["setting"] = "chambre, oiseau de papier au plafond, rideaux à lunes, sac rouge"
    story["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]

    check(SID, story["age_band"], story["chunks"])

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

    counts = [path_words(out_chunks, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    joined = "\n".join(c["script"] for c in story["chunks"]).lower()
    for bad in (
        "aujourd'hui,",
        "mission accomplie",
        "j'ai compris",
        "jardinier",
        "maîtresse",
        "maitresse",
        "merle",
        "couleur de miel",
        "tout doux",
        "tout calme",
    ):
        if bad in joined:
            raise SystemExit(f"gabarit: {bad}")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-AUT-036 — L'oiseau de papier et le sac rouge de Sarah\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "- **Public :** N3 (3–6 ans), audio familial\n"
        "- **Leçon :** AUT.AFF.001 — préparer / porter sans forcer, vécue "
        "(l'oiseau va dans le sac, puis s'ouvre tout seul)\n"
        "- **Personnages :** Sarah, papa, maman (D16)\n"
        "- **Structure :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "## Vécu\n\n"
        "Chambre, oiseau de papier au plafond, rideaux à lunes, sac rouge. "
        "Sarah compte sept lunes ; la septième est pliée. Un rayon touche "
        "**la virgule bleue** de l'aile (indice unique, dès l'ouverture, payé au climax). "
        "Désir : emmener l'oiseau au parc, sous le vrai ciel, dans le sac. "
        "Première idée : tirer le fil, pousser vers la fenêtre. L'aile se plie, "
        "la virgule se cache, l'oiseau glisse vers le sac. Sourire disparu, "
        "envie et inquiétude dans la poitrine, papa s'accroupit. "
        "Au parc, le choix change la manière :\n\n"
        "- T1 lieu : le bac à sable / le toboggan / les balançoires\n"
        "- T2 jeu-ruse : le ballon / le seau / le doudou\n"
        "- T3 ouverture seule : le banc / la grille / le cerisier\n\n"
        "Personne ne donne la réponse. Sarah refuse de foncer, observe la virgule, "
        "écoute le lieu. Le dénouement a failli ne pas arriver (main retenue). "
        "Q = sac. Merci vécu quand elle remet l'oiseau. "
        "Dernière image : virgule, lunes, fil, chaussette jaune, pull à étoile.\n\n"
        "## Vu et corrigé\n\n"
        "- Zoé absente (D16 : Sarah). Monde chambre → parc, pas liste de sac.\n"
        "- Monde ≠ TREE-AUT-029 (toit rouge), ≠ TREE-AUT-031 (sac vert), ≠ TREE-COL-001 (pommes).\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Pas de gabarit v2 : aujourd'hui, merle/miel, Mission accomplie, J'ai compris, "
        "jardinier/maîtresse.\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration), `style_energy`, "
        "pauses, pitch, volume. `slow` = choix, indice, fin.\n"
        "- 27 souvenirs, 27 dernières images. Ouverture + 3 L1 + 9 L2 + 27 L3/fins relus.\n"
        f"- `check()` N3≤16, ~{min(counts)}–{max(counts)} mots/chemin. Pas apply. Pas git. Pas audio.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
