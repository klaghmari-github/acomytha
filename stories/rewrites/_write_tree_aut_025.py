#!/usr/bin/env python3
"""TREE-AUT-025 — F-NAR-019. Nina, flaques, fontaine. N3. Pas d'apply."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, relecture, words

SID = "TREE-AUT-025"
TICS = ("tout doux", "tout calme", "encore", "déjà")
SNAIL = ("escargot", "loupe", "carnet bleu", "pots de menthe", "vélo rouge")

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "flaques",
        "note": (
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=l_eau appelle avant les bottes; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": (
            "arc=choix; intention=inviter; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; "
            "sourire=léger; respiration=pause_avant_choix"
        ),
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": "bottes",
        "note": (
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=les pieds avant l_eau; tempo=suspendu; "
            "sourire=aucun; respiration=courte_avant_question"
        ),
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "grenouilles",
        "note": (
            "arc=confirmation; intention=relancer; emotion=soulagement; intensite=1; "
            "destinataire=enfant; sous_texte=les deux grenouilles sont prêtes; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": (
            "arc=action; intention=entraîner; emotion=élan; intensite=2; "
            "destinataire=enfant; sous_texte=l_objet part vers l_eau; tempo=vif; "
            "sourire=léger; respiration=courte"
        ),
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": (
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; "
            "intensite=2; destinataire=enfant; sous_texte=une botte ne suffit pas; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": (
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=un pied puis l_autre jusqu_au_bassin; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": None,
        "note": (
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=le chhh de la fontaine a tenu sa promesse; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    },
}


def ssml(text: str, m: dict) -> str:
    body = html.escape(text, quote=False)
    if m.get("emphasis"):
        e = html.escape(m["emphasis"], quote=False)
        tagged = f'<emphasis level="moderate">{e}</emphasis>'
        body = body.replace(e, tagged, 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f"{body}</prosody><break time=\"{m['pause']}ms\"/></speak>"
    )


def xai(text: str, m: dict) -> str:
    body = text
    if m.get("emphasis"):
        e = m["emphasis"]
        body = body.replace(e, f"<emphasis>{e}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitchTag"):
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    pause = m["pause"]
    tail = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + tail).strip()


def apply_tts(src: dict, lines: list[str], sons: str, profile: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    text, script = from_script(lines)
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if extra.get("note"):
        m["note"] = extra["note"]
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
    nc["text_ssml"] = ssml(text, m)
    nc["text_xai_tags"] = xai(text, m)
    nc["rate_wpm"] = m["wpm"]
    nc["rate_label"] = m["rate"]
    nc["speed_xai"] = m["speed"]
    nc["length_scale_piper"] = m["piper"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitchSsml"]
    nc["pitch_xai_tag"] = m["pitchTag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = m["emphasis"] or ""
    nc["pause_before_ms"] = extra.get("pauseBefore", 0)
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
    nc["notes"] = m["note"]
    nc["night_policy"] = "play"
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        nc[k] = v
    return nc


def split_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    for raw in lines:
        role, phrase = raw.split("|", 1)
        parts = re.findall(r"[^.?!]+[.?!]", phrase.strip())
        if not parts:
            raise SystemExit(f"PUNCT {raw}")
        for p in parts:
            p = re.sub(r"\s+", " ", p).strip()
            out.append(f"{role}|{p}")
    return out


def preview(scripts: dict) -> None:
    n = 0
    for cid, lines in scripts.items():
        prev = ""
        run = 1
        for raw in lines:
            role, phrase = raw.split("|", 1)
            w = words(phrase)
            n += w
            if w > 16:
                raise SystemExit(f"LONG {cid} {w}>16: {phrase}")
            marks = phrase.count(".") + phrase.count("?") + phrase.count("!")
            if marks > 1:
                raise SystemExit(f"MULTI {cid}: {phrase}")
            if not phrase.endswith((".", "?", "!")):
                raise SystemExit(f"PUNCT {cid}: {phrase}")
            tok = phrase.split()[0].lower() if role == "narrateur" else ""
            if tok and tok == prev:
                run += 1
                if run >= 4:
                    raise SystemExit(f"PUCES {cid}: {tok}")
            else:
                run = 1
            prev = tok
        blob = " ".join(ln.split("|", 1)[1] for ln in lines).lower()
        for tic in TICS:
            if tic in blob:
                raise SystemExit(f"TIC {cid}: {tic}")
        for bad in SNAIL:
            if bad in blob:
                raise SystemExit(f"ESCARGOT {cid}: {bad}")
    print(f"preview {SID} {n} mots  chunks={len(scripts)}")


OPENING = [
    "narrateur|Derrière la grille du parc, le bassin de pierre fume un peu.",
    "narrateur|Nina y vient ce matin-là avec papa et maman.",
    "narrateur|La pluie vient de laver le gravier sombre.",
    "narrateur|Un filet d'eau tombe du lion de pierre.",
    "narrateur|Ça sent le buis coupé, et la terre froide.",
    "narrateur|Le banc vert tient un ciel pâle dans l'eau.",
    "narrateur|Près de la grille, deux bottes à grenouilles.",
    "narrateur|Une botte tient debout, l'autre est couchée.",
    "papa|Le banc a un bout plus sec, Nina.",
    "maman|On peut s'asseoir, si tu veux.",
    "enfant-f|Non.",
    "enfant-f|Je veux toutes les flaques !",
    "narrateur|En ce moment, Nina enfile la botte gauche à la hâte.",
    "narrateur|Le pied droit reste dans sa chaussette.",
    "narrateur|Elle court vers le premier miroir d'eau.",
    "enfant-f|Jusqu'à la fontaine !",
    "narrateur|Elle saute trop tôt.",
    "narrateur|La chaussette plonge dans le froid.",
    "enfant-f|Aïe !",
    "enfant-f|Ça pique !",
    "narrateur|Nina saute sur un pied, le visage plissé.",
    "maman|Tes orteils sont tout froids ?",
    "enfant-f|Je voulais le bassin, là-bas.",
    "papa|L'autre grenouille est restée près de la grille.",
    "narrateur|Nina regarde la botte couchée.",
    "narrateur|La fontaine fait un petit chhh, sans se presser.",
]

T1 = [
    "papa|Où poses-tu l'autre botte, Nina ?",
    "narrateur|Le bac à sable.",
    "narrateur|Le toboggan.",
    "narrateur|Les balançoires.",
]

L1 = {
    1: [
        "narrateur|Nina s'assoit sur le bord de bois du bac.",
        "narrateur|Le sable collant lui lèche les doigts.",
        "enfant-f|Il y a une flaque au milieu !",
        "narrateur|Elle se lève trop vite, une seule botte.",
        "narrateur|Le pied chaussette s'enfonce dans le sable.",
        "enfant-f|Il me tient !",
        "narrateur|Elle s'assoit, les épaules basses.",
        "papa|Le sable a pris ta chaussette, tu vois ?",
        "narrateur|Nina tapote le pied gauche, bien botté.",
        "enfant-f|Celle-là, elle est rentrée.",
        "maman|Et l'autre grenouille, dans l'herbe ?",
        "papa|Tu la vois, près de la feuille ?",
        "enfant-f|Oui, papa.",
        "narrateur|Un grain de sable reste collé au coton.",
        "narrateur|L'eau du bac attend, ronde et grise.",
    ],
    2: [
        "narrateur|Nina pose la paume sur la rampe du toboggan.",
        "narrateur|Le plastique luisant lui refroidit la main.",
        "enfant-f|Je glisse dans l'eau, en bas !",
        "narrateur|Elle grimpe deux marches, une seule botte.",
        "narrateur|Elle pousse. Rien. Ça crisse.",
        "enfant-f|Ça veut pas.",
        "narrateur|Elle s'accroche au rail, les joues chaudes.",
        "papa|La rampe est trop mouillée, tu sens ?",
        "narrateur|Nina s'assoit sur la marche du bas.",
        "maman|L'autre botte, près de l'herbe ?",
        "enfant-f|Elle brille, à côté.",
        "papa|Tu la prends avant de glisser ?",
        "enfant-f|Oui, je la vois.",
        "narrateur|Une goutte tombe de la rampe, ploc.",
        "narrateur|La flaque du bas fait un rond, puis s'arrête.",
    ],
    3: [
        "narrateur|Nina s'assoit sur le banc vert, côté mouillé.",
        "narrateur|Le bois froid lui pique les genoux.",
        "enfant-f|Je veux l'eau sous les chaînes !",
        "narrateur|Elle se lève, une botte seulement.",
        "narrateur|Une goutte de chaîne lui tombe sur l'orteil.",
        "enfant-f|Oh, c'est glacé.",
        "narrateur|Elle se rassoit, le menton un peu bas.",
        "maman|Tes orteils n'aiment pas l'eau toute seule ?",
        "narrateur|Nina enfile mieux la botte gauche.",
        "papa|L'autre, près du pied du banc ?",
        "enfant-f|Elle est là.",
        "maman|Tu as froid aux orteils ?",
        "enfant-f|Un peu, maman.",
        "narrateur|La chaîne fait un bruit de goutte, puis se tait.",
        "narrateur|Une flaque tremble sous les sièges.",
    ],
}

Q = {
    1: [
        "narrateur|Un grain de sable colle à la chaussette.",
        "maman|Nina met quoi, avant l'eau ?",
    ],
    2: [
        "narrateur|Une goutte de la rampe touche le pied nu.",
        "papa|Nina met quoi, avant de glisser ?",
    ],
    3: [
        "narrateur|La chaîne mouille l'orteil de Nina.",
        "maman|Nina met quoi, avant la flaque ?",
    ],
}

C = {
    1: [
        "narrateur|Nina secoue le sable du coton.",
        "narrateur|Elle pousse le pied droit dans la grenouille.",
        "enfant-f|Les deux, maintenant.",
        "papa|Merci, Nina.",
        "narrateur|Elle se lève. Le sable fait crac sous les semelles.",
        "maman|Tes pieds sont au chaud, pour l'eau ?",
        "enfant-f|Oui. Jusqu'à la fontaine.",
    ],
    2: [
        "narrateur|Nina attrape la botte droite, sur l'herbe.",
        "narrateur|Elle pousse, assise sur la marche froide.",
        "enfant-f|Ça y est. Les deux grenouilles.",
        "maman|Merci, ma grande.",
        "narrateur|Nina se lève près de la rampe.",
        "narrateur|Le gravier chante sous le caoutchouc.",
        "papa|La flaque du bas t'attend, sans glisser.",
    ],
    3: [
        "narrateur|Nina enfile la botte droite, sur le banc.",
        "narrateur|Le bois laisse une trace humide sur le caoutchouc.",
        "enfant-f|Mes pieds sont au chaud.",
        "papa|Merci, Nina.",
        "narrateur|Elle pose les deux pieds sur le gravier.",
        "narrateur|Les chaînes bougent un peu, au vent.",
        "maman|L'eau sous les sièges t'attend.",
    ],
}

T2 = {
    1: [
        "papa|Le sable colle. Tu prends quoi pour la suite ?",
        "narrateur|Le ballon.",
        "narrateur|Le seau.",
        "narrateur|Le doudou.",
    ],
    2: [
        "maman|La rampe a glissé. Tu emportes quoi ?",
        "narrateur|Le ballon.",
        "narrateur|Le seau.",
        "narrateur|Le doudou.",
    ],
    3: [
        "papa|Les chaînes gouttent. Tu prends quoi avec toi ?",
        "narrateur|Le ballon.",
        "narrateur|Le seau.",
        "narrateur|Le doudou.",
    ],
}

L2 = {
    (1, 1): [
        "narrateur|Dans le bac, le ballon jaune est à moitié sous le sable.",
        "narrateur|Nina le tire. Un jet de grains lui pique la joue.",
        "enfant-f|Il veut pas rebondir.",
        "narrateur|Elle le lance vers la flaque du bac.",
        "narrateur|Le ballon s'assoit, lourd, sans un saut.",
        "papa|Tu le prends à deux mains ?",
        "narrateur|Nina le serre contre sa veste.",
        "maman|Tes bottes tiennent bien ?",
        "enfant-f|Oui. Elles font flouc.",
        "papa|L'eau du parc brille, plus loin.",
        "narrateur|Nina avance d'un pas, sans sauter.",
        "narrateur|Un grain beige reste collé au jaune.",
    ],
    (1, 2): [
        "narrateur|Près de la grille du bac, le seau bleu attend.",
        "narrateur|Nina le plonge. C'est lourd.",
        "enfant-f|C'est pas de l'eau !",
        "narrateur|Elle verse le sable mouillé. Ça fait pâté.",
        "maman|Tu le prends par l'anse, cette fois ?",
        "narrateur|Nina soulève le seau vide.",
        "papa|Tes deux bottes sont mises.",
        "enfant-f|Oui, papa.",
        "maman|L'eau vraie brille, juste là.",
        "narrateur|Nina marche. Le seau tape un peu sa jambe.",
        "enfant-f|Toi, tu vas au bassin.",
        "narrateur|L'anse est lisse, un peu froide.",
    ],
    (1, 3): [
        "narrateur|Sur le bord du bac, le doudou a du sable au nez.",
        "narrateur|Nina souffle. Les grains dansent, puis tombent.",
        "enfant-f|Il va nager ?",
        "narrateur|Elle le baisse vers la flaque du bac.",
        "narrateur|Un grain se colle à l'oreille de tissu.",
        "enfant-f|Non. Toi, tu restes au sec.",
        "papa|Tu le sers contre toi ?",
        "narrateur|Nina le prend à deux mains, contre la veste.",
        "maman|Tes bottes font flouc, tu entends ?",
        "enfant-f|Oui, maman.",
        "narrateur|Nina avance vers le parc, sans sauter.",
        "narrateur|Le doudou a le nez vers la fontaine.",
    ],
    (2, 1): [
        "narrateur|Nina pose le ballon en haut de la rampe.",
        "narrateur|Il dévale, trop vite, et fait plouf en bas.",
        "enfant-f|Il va sans moi !",
        "narrateur|Elle veut glisser. Les bottes coincées, elle s'arrête.",
        "papa|Les marches, Nina ?",
        "narrateur|Elle descend marche par marche.",
        "narrateur|Le ballon a roulé vers le gravier luisant.",
        "enfant-f|Attends-moi.",
        "maman|Tu le rattrapes à deux mains ?",
        "narrateur|Nina le serre. Il est mouillé, souple.",
        "papa|La fontaine est plus loin, tu vois ?",
        "narrateur|Elle marche, le ballon contre le ventre.",
    ],
    (2, 2): [
        "narrateur|Nina accroche le seau au rail du toboggan.",
        "narrateur|L'anse glisse. Le seau sonne, clang.",
        "enfant-f|Il a voulu glisser tout seul.",
        "papa|Tu le tiens par l'anse ?",
        "narrateur|Elle rattrape l'anse, juste à temps.",
        "maman|Tes bottes tiennent sur la marche ?",
        "enfant-f|Oui. Je descends.",
        "narrateur|Nina prend les marches, une après l'autre.",
        "narrateur|Le seau tape sa jambe, vide.",
        "papa|L'eau du bas est là, sans glissade.",
        "enfant-f|On va la chercher, seau.",
        "narrateur|Une goutte de rampe roule sur le bord bleu.",
    ],
    (2, 3): [
        "narrateur|Nina pose le doudou sur la marche du haut.",
        "narrateur|Une goutte de rampe lui tombe sur la tête.",
        "enfant-f|Pauvre tête.",
        "narrateur|Elle le ramasse, le serre.",
        "maman|Tu glisses avec lui ?",
        "enfant-f|Non. Trop mouillé.",
        "papa|Les marches, alors ?",
        "narrateur|Nina descend, le doudou contre l'épaule.",
        "narrateur|Le plastique de la rampe reste vide.",
        "maman|Tes bottes font flouc, tu entends ?",
        "enfant-f|Oui. On va à l'eau.",
        "narrateur|Le doudou a une perle sur l'oreille, vite essuyée.",
    ],
    (3, 1): [
        "narrateur|Nina pose le ballon sur le siège mouillé.",
        "narrateur|Elle pousse un peu. Le siège part.",
        "enfant-f|Il tombe !",
        "narrateur|Le ballon passe entre les chaînes, roule.",
        "papa|Sans sauter, tu le rattrapes ?",
        "narrateur|Nina marche jusqu'à lui, bottes fermes.",
        "narrateur|Le ballon s'est arrêté au bord de l'eau.",
        "maman|Tu le prends à deux mains ?",
        "enfant-f|Oui. Il a failli se baigner trop tôt.",
        "papa|Les flaques sont là, plus loin.",
        "narrateur|Nina avance, le jaune contre sa veste.",
        "narrateur|Une chaîne goutte derrière elle, une fois.",
    ],
    (3, 2): [
        "narrateur|Nina pose le seau sur le siège de la balançoire.",
        "narrateur|Le siège penche. Le seau verse du vide, clang.",
        "enfant-f|Il a versé trop tôt.",
        "maman|Tu le prends par l'anse ?",
        "narrateur|Nina rattrape l'anse. Le seau est froid.",
        "papa|Tes bottes tiennent sous les chaînes ?",
        "enfant-f|Oui, papa.",
        "narrateur|Elle marche, le seau contre la jambe.",
        "maman|L'eau sous les sièges brille.",
        "enfant-f|On va la prendre, plus tard.",
        "narrateur|Nina ne saute pas.",
        "narrateur|Une goutte de chaîne sonne sur le bleu.",
    ],
    (3, 3): [
        "narrateur|Nina assied le doudou sur la balançoire.",
        "narrateur|Une goutte de chaîne lui mouille l'oreille.",
        "enfant-f|Toi, tu restes au sec.",
        "papa|Tu le sers contre toi ?",
        "narrateur|Nina le prend, le cache sous le col.",
        "maman|Tes bottes font flouc, tu entends ?",
        "enfant-f|Oui, maman.",
        "papa|L'eau brille, sous les chaînes, puis plus loin.",
        "narrateur|Nina avance, sans pousser le siège.",
        "narrateur|Le doudou a le nez vers le lion de pierre.",
        "enfant-f|On y va.",
        "narrateur|Le bois du banc reste sombre, à côté.",
    ],
}


def t3_lines(j: int) -> list[str]:
    start = {
        1: "maman|Le ballon est prêt. Quelle flaque, pour commencer ?",
        2: "papa|Le seau est prêt. Quelle flaque, pour commencer ?",
        3: "maman|Le doudou est prêt. Quelle flaque, pour commencer ?",
    }[j]
    return [
        start,
        "narrateur|D'abord la petite, mince comme une assiette.",
        "narrateur|Celle du banc, avec le ciel dedans.",
        "narrateur|Ou la grande, près du lion.",
    ]


L3 = {
    (1, 1, 1): [
        "narrateur|La petite flaque du bac est mince, comme une assiette.",
        "narrateur|Nina lance le ballon. Il ne fait aucun plouf.",
        "enfant-f|Elle est trop plate !",
        "papa|Un pied, puis l'autre ?",
        "narrateur|Nina pose le gauche. L'eau à peine, autour du caoutchouc.",
        "narrateur|Puis le droit, dans la même assiette grise.",
        "enfant-f|Ça pique un peu.",
        "maman|La flaque du banc est plus profonde, tu vois ?",
        "narrateur|Nina marche jusque-là, le ballon sous le bras.",
        "narrateur|Elle entre, gauche, puis droite.",
        "narrateur|Le ballon a un grain de sable collé.",
        "enfant-f|Ensuite le lion !",
        "narrateur|Le bassin n'est plus très loin.",
    ],
    (1, 1, 2): [
        "narrateur|L'eau du banc tient le ciel, tout gris.",
        "narrateur|Nina fait rouler le ballon. Il bute contre le pied du banc.",
        "enfant-f|Il a peur du trou.",
        "maman|Ce n'est pas un trou. C'est le ciel.",
        "narrateur|Nina pose le pied gauche près du bois.",
        "narrateur|L'eau froide lui monte au bas de la botte.",
        "narrateur|Puis le droit. Deux ronds s'ouvrent.",
        "papa|Le ballon, maintenant ?",
        "enfant-f|Il peut toucher, un instant.",
        "narrateur|Le jaune frôle l'eau. Un cercle part.",
        "maman|La grande flaque brille, vers la fontaine.",
        "narrateur|Nina marche vers le bassin, sans courir.",
        "narrateur|Le banc laisse une goutte sur le bois.",
    ],
    (1, 1, 3): [
        "narrateur|La grande flaque est large, près du bassin.",
        "narrateur|Nina veut jeter le ballon jusqu'au lion.",
        "narrateur|Il tombe trop court, et flotte.",
        "enfant-f|Il est au milieu !",
        "papa|Par le bord, Nina ?",
        "narrateur|Elle entre à gauche, tout au bord.",
        "narrateur|Puis à droite. L'eau lui prend les chevilles.",
        "enfant-f|Elle est grande, celle-là.",
        "maman|Un pas, puis l'autre, jusqu'au ballon.",
        "narrateur|Nina rejoint le jaune. Il fait des ronds.",
        "narrateur|Le lion de pierre crache son filet, juste là.",
        "enfant-f|On est arrivés.",
        "narrateur|Le ballon a une perle d'eau sur le grain de sable.",
    ],
    (1, 2, 1): [
        "narrateur|Nina plonge le seau dans la petite flaque.",
        "narrateur|Presque rien. Un fond de poussière d'eau.",
        "enfant-f|C'est trop mince !",
        "papa|Tes bottes, d'abord, dans cette assiette.",
        "narrateur|Pied gauche. Pied droit. L'eau à peine.",
        "maman|Plus loin, le banc en a davantage.",
        "narrateur|Nina marche, le seau vide qui sonne.",
        "narrateur|Elle entre dans l'eau du banc, gauche, puis droite.",
        "enfant-f|Là, il y a vraiment de l'eau.",
        "narrateur|Le seau prend une gorgée grise.",
        "papa|Tu la portes jusqu'au lion ?",
        "enfant-f|Oui. Sans la verser trop tôt.",
        "narrateur|Un peu de sable reste au fond, sous l'eau.",
    ],
    (1, 2, 2): [
        "narrateur|Nina pose le seau contre le pied du banc.",
        "narrateur|Ça sonne, tout bas, sur le bois mouillé.",
        "enfant-f|Pour l'eau du ciel.",
        "narrateur|Elle penche trop. La gorgée retombe.",
        "maman|Plus droit, tu veux ?",
        "narrateur|Nina tient l'anse à deux mains, seau plat.",
        "narrateur|Elle entre gauche, puis droite, dans l'eau du banc.",
        "enfant-f|Il a sa part, maintenant.",
        "papa|La grande flaque, vers la fontaine ?",
        "narrateur|Nina marche, le seau qui pèse un peu.",
        "narrateur|Elle ne court pas. Rien ne déborde.",
        "maman|Le lion t'attend, avec son filet.",
        "narrateur|Le banc garde un anneau sombre, où le seau a sonné.",
    ],
    (1, 2, 3): [
        "narrateur|Nina entre trop vite dans la grande flaque, seau en avant.",
        "narrateur|L'eau lui gicle sur la veste.",
        "enfant-f|Oh ! Trop fort.",
        "papa|Par le bord, plus lent ?",
        "narrateur|Elle recule, puis pose le gauche au bord.",
        "narrateur|Puis le droit. L'eau monte sans sauter.",
        "maman|Le seau, maintenant.",
        "narrateur|Nina le baisse. Le bassin lui donne une gorgée claire.",
        "enfant-f|C'est l'eau du lion.",
        "narrateur|Elle lève le seau. Rien ne déborde.",
        "papa|Tu l'as, ta fontaine.",
        "enfant-f|Oui. Dans le seau, et autour des bottes.",
        "narrateur|Un grain de sable tourne au fond, puis s'arrête.",
    ],
    (1, 3, 1): [
        "narrateur|Nina baisse le doudou vers la petite flaque.",
        "narrateur|Un grain de sable saute sur l'oreille.",
        "enfant-f|Pas toi.",
        "narrateur|Elle le relève, contre la veste.",
        "papa|Tes bottes, dans l'assiette d'eau ?",
        "narrateur|Gauche. Puis droite. L'eau mince, froide.",
        "maman|Le banc a une flaque plus ronde.",
        "narrateur|Nina marche, le doudou haut, au sec.",
        "narrateur|Elle entre près du banc, un pied, puis l'autre.",
        "enfant-f|Toi, tu regardes. Moi, je trempes.",
        "papa|Jusqu'au lion, comme ça ?",
        "enfant-f|Oui.",
        "narrateur|L'oreille du doudou a un grain, que Nina souffle.",
    ],
    (1, 3, 2): [
        "narrateur|Le doudou se penche. Le ciel du banc est dans l'eau.",
        "enfant-f|Il veut le ciel.",
        "narrateur|Nina le baisse trop. Une moustache d'eau touche le tissu.",
        "maman|Au sec, lui ?",
        "narrateur|Elle le hisse. La tache reste petite.",
        "narrateur|Puis elle entre, gauche, droite, près du bois.",
        "papa|Tes grenouilles sont dans le ciel, maintenant.",
        "enfant-f|Et lui, sur moi.",
        "maman|La grande flaque, vers le bassin.",
        "narrateur|Nina marche. Le doudou voit le lion par-dessus l'épaule.",
        "narrateur|Elle ne le baisse plus.",
        "enfant-f|On y est presque.",
        "narrateur|Le bois du banc goutte, une fois, dans l'eau grise.",
    ],
    (1, 3, 3): [
        "narrateur|Nina entre dans la grande flaque, les deux pieds ensemble.",
        "narrateur|L'eau est trop large. Elle vacille.",
        "enfant-f|Oups.",
        "papa|Un pied, puis l'autre ?",
        "narrateur|Elle reprend. Gauche au bord. Droit ensuite.",
        "narrateur|Le doudou reste haut, sous le col.",
        "maman|Le lion crache tout près.",
        "narrateur|Une goutte du filet atterrit sur le ventre du doudou.",
        "enfant-f|Une seule. D'accord.",
        "narrateur|Nina rit, tout bas, les bottes dans le bassin.",
        "papa|Vous voilà.",
        "enfant-f|Lui a vu la fontaine.",
        "narrateur|Le grain de sable du bac a disparu, essuyé au col.",
    ],
    (2, 1, 1): [
        "narrateur|Au pied du toboggan, la petite flaque est mince.",
        "narrateur|Nina pose le ballon. Il glisse un peu sur la rampe mouillée.",
        "enfant-f|Reviens.",
        "papa|Tes pieds, dans cette petite eau ?",
        "narrateur|Gauche. Droit. Presque rien autour des semelles.",
        "maman|Le banc a mieux, plus loin.",
        "narrateur|Nina marche, le ballon mouillé sous le bras.",
        "narrateur|Elle entre près du banc, un pied, puis l'autre.",
        "enfant-f|Là, il peut faire un vrai plouf.",
        "narrateur|Le jaune saute un tout petit saut, puis s'arrête.",
        "papa|Ensuite le lion ?",
        "enfant-f|Oui. Sans le lancer trop fort.",
        "narrateur|Une goutte de rampe a suivi le ballon, jusqu'ici.",
    ],
    (2, 1, 2): [
        "narrateur|Nina pose le ballon un moment sur le banc vert.",
        "narrateur|Un rond d'eau s'ouvre sous le jaune.",
        "enfant-f|Il s'assoit, lui aussi.",
        "maman|Et tes bottes, dans l'eau du banc ?",
        "narrateur|Gauche près du bois. Droit ensuite.",
        "papa|Le ballon glisse vers tes genoux.",
        "narrateur|Nina le rattrape avant le grand plouf.",
        "enfant-f|Pas trop tôt.",
        "maman|La grande flaque brille, vers la fontaine.",
        "narrateur|Nina marche. Le ballon a un cercle d'eau sur le flanc.",
        "narrateur|Elle ne court pas. Les bottes font flouc, flouc.",
        "papa|Le lion t'a vue.",
        "narrateur|Le banc garde le rond humide, vide maintenant.",
    ],
    (2, 1, 3): [
        "narrateur|Nina vise la grande flaque, au pied du bassin.",
        "narrateur|Elle lance le ballon. Plouf, trop près du lion.",
        "enfant-f|Il a fait le grand saut sans moi.",
        "papa|Toi, par le bord.",
        "narrateur|Elle entre à gauche. L'eau lui prend la cheville.",
        "narrateur|Puis à droite. Deux ronds rejoignent le ballon.",
        "maman|Tu le rattrapes sans courir ?",
        "enfant-f|Oui. Lentement.",
        "narrateur|Nina rejoint le jaune. Il flotte une seconde.",
        "papa|La rampe est loin, derrière.",
        "enfant-f|On a fini la glissade autrement.",
        "narrateur|Le filet du lion touche le ballon, une perle.",
        "narrateur|Nina le serre. Les grenouilles sont mouillées jusqu'au col.",
    ],
    (2, 2, 1): [
        "narrateur|Nina tend le seau sous la petite flaque du toboggan.",
        "narrateur|Une goutte de rampe tombe dedans, une seule.",
        "enfant-f|C'est tout ?",
        "maman|Tes bottes, dans cette mince eau.",
        "narrateur|Gauche. Droit. L'eau à peine.",
        "papa|Le banc en a plus.",
        "narrateur|Nina marche, le seau qui sonne presque vide.",
        "narrateur|Près du banc, elle entre, un pied, puis l'autre.",
        "enfant-f|Remplis-toi, maintenant.",
        "narrateur|Le seau prend l'eau du ciel, grise.",
        "maman|Jusqu'au lion, sans verser ?",
        "enfant-f|Oui.",
        "narrateur|La goutte de rampe nage au milieu, toute petite.",
    ],
    (2, 2, 2): [
        "narrateur|Nina pend le seau près du banc, au-dessus de l'eau.",
        "narrateur|L'anse glisse un peu. Elle la serre.",
        "enfant-f|Pas maintenant, seau.",
        "papa|Tes grenouilles, dans l'eau du banc ?",
        "narrateur|Gauche. Droit. L'eau froide, jusqu'au bas.",
        "maman|Maintenant, tu peux le baisser.",
        "narrateur|Le seau prend sa gorgée. Ça pèse.",
        "enfant-f|On va au lion.",
        "narrateur|Nina marche vers la grande flaque, sans courir.",
        "papa|Rien ne déborde ?",
        "enfant-f|Presque. J'y vais doucement.",
        "narrateur|Une perle court sur le bord bleu, et rentre.",
        "narrateur|Le banc goutte, à côté, sans se presser.",
    ],
    (2, 2, 3): [
        "narrateur|Nina veut verser le seau dans la grande flaque, trop tôt.",
        "narrateur|Le filet part. Elle s'arrête. Le seau est vide.",
        "enfant-f|J'ai trop pressé.",
        "papa|On le remplit au bord, ensemble ?",
        "narrateur|Elle entre gauche, puis droite, près du bassin.",
        "maman|Baisse-le, maintenant.",
        "narrateur|Le seau reprend l'eau du lion, claire.",
        "enfant-f|Je la garde.",
        "narrateur|Nina lève le seau. Un filet, puis plus rien.",
        "papa|Tu as versé, puis tu as pris.",
        "enfant-f|Dans l'ordre.",
        "narrateur|Les bottes sont dans le bassin, froides et fières.",
        "narrateur|Une goutte de rampe a séché sur l'anse, en chemin.",
    ],
    (2, 3, 1): [
        "narrateur|Le doudou a vu la rampe, depuis les bras.",
        "narrateur|Nina le baisse vers la petite flaque. Trop près.",
        "enfant-f|Ta tête, non.",
        "maman|Les bottes, elles, peuvent.",
        "narrateur|Gauche. Droit. L'eau mince du bas.",
        "papa|Le banc, ensuite.",
        "narrateur|Nina marche, le doudou haut.",
        "narrateur|Près du bois, un pied, puis l'autre.",
        "enfant-f|Toi tu regardes la rampe. Moi l'eau.",
        "maman|Le lion, après.",
        "narrateur|Nina avance. Le plastique du toboggan brille, derrière.",
        "enfant-f|On a glissé avec les pieds.",
        "narrateur|Une perle de rampe sèche sur l'oreille, essuyée.",
    ],
    (2, 3, 2): [
        "narrateur|Nina appuie le doudou un instant contre le banc.",
        "narrateur|Le bois froid lui touche le dos de tissu.",
        "enfant-f|Il se repose.",
        "papa|Tes bottes, dans l'eau, pendant ce temps ?",
        "narrateur|Gauche. Droit. Deux ronds sous le banc.",
        "maman|Tu le reprends ?",
        "enfant-f|Oui. Au sec.",
        "narrateur|Nina le serre. Elle marche vers la grande flaque.",
        "narrateur|Le doudou a vu le ciel dans l'eau, puis le lion.",
        "papa|Sans le baisser ?",
        "enfant-f|Sans le baisser.",
        "narrateur|Les bottes font flouc, flouc, jusqu'au bassin.",
        "narrateur|Le banc garde une petite trace de tissu, qui sèche.",
    ],
    (2, 3, 3): [
        "narrateur|Nina écoute la fontaine, le doudou contre la joue.",
        "narrateur|Elle veut entrer d'un saut dans la grande flaque.",
        "enfant-f|Attends. Trop large.",
        "maman|Le bord ?",
        "narrateur|Gauche au bord. Droit ensuite. L'eau aux chevilles.",
        "papa|Lui, il écoute aussi.",
        "narrateur|Le doudou a l'oreille vers le chhh du lion.",
        "enfant-f|On est arrivés.",
        "narrateur|Une goutte du filet frôle le tissu, puis tombe.",
        "maman|Juste assez.",
        "narrateur|Nina ne bouge plus une seconde, fière et calme.",
        "papa|La rampe est loin. Le bassin est là.",
        "narrateur|Les grenouilles luisent, plein le froid du bassin.",
    ],
    (3, 1, 1): [
        "narrateur|Sous les chaînes, la petite flaque tremble.",
        "narrateur|Nina fait passer le ballon dessous. Une goutte le tache.",
        "enfant-f|Merci, chaîne.",
        "papa|Tes pieds, dans cette petite eau.",
        "narrateur|Gauche. Droit. L'eau mince, qui tremble.",
        "maman|Le banc, ensuite, plus calme.",
        "narrateur|Nina marche, le ballon taché d'une perle.",
        "narrateur|Près du banc, un pied, puis l'autre.",
        "enfant-f|Là, il peut rouler jusqu'au pied du bois.",
        "papa|Puis le lion.",
        "narrateur|Nina ne pousse plus le siège.",
        "enfant-f|Les bottes, c'est mieux que la balançoire.",
        "narrateur|La chaîne goutte une dernière fois, derrière.",
    ],
    (3, 1, 2): [
        "narrateur|Nina lâche le ballon. Il roule jusqu'au pied du banc.",
        "narrateur|Il s'arrête pile dans l'eau du ciel.",
        "enfant-f|Il a choisi tout seul.",
        "maman|Et toi ?",
        "narrateur|Elle entre gauche, puis droite, près du bois.",
        "papa|Tu le reprends sans te presser ?",
        "enfant-f|Oui.",
        "narrateur|Le jaune est froid, luisant.",
        "maman|La grande flaque, vers la fontaine.",
        "narrateur|Nina marche. Les chaînes s'éloignent.",
        "enfant-f|On laisse les sièges.",
        "narrateur|Un rond d'eau reste au pied du banc, où le ballon a dormi.",
        "papa|Le lion est droit devant.",
    ],
    (3, 1, 3): [
        "narrateur|Nina pose le ballon au bord de la grande flaque.",
        "narrateur|Il s'arrête. Il ne veut pas le grand bain tout de suite.",
        "enfant-f|Moi non plus, d'un coup.",
        "papa|Le bord.",
        "narrateur|Gauche. Droit. L'eau large, aux chevilles.",
        "maman|Le ballon, tu le portes ?",
        "enfant-f|Jusqu'au lion.",
        "narrateur|Nina le prend. Elle marche dans l'eau, pas à pas.",
        "narrateur|Les chaînes sont loin. Le filet est près.",
        "papa|Vous y êtes.",
        "enfant-f|Le jaune a vu le lion.",
        "narrateur|Une goutte de chaîne a séché sur le flanc, en route.",
        "narrateur|Le bassin entoure les grenouilles, froid et rond.",
    ],
    (3, 2, 1): [
        "narrateur|Sous la balançoire, le seau est froid.",
        "narrateur|Nina le baisse dans la petite flaque. Presque rien.",
        "enfant-f|Elle tremble trop.",
        "maman|Tes bottes, d'abord.",
        "narrateur|Gauche. Droit. L'eau mince sous les chaînes.",
        "papa|Le banc tient mieux l'eau.",
        "narrateur|Nina marche, le seau vide contre la jambe.",
        "narrateur|Près du banc, un pied, puis l'autre.",
        "enfant-f|Prends, maintenant.",
        "narrateur|Le seau s'alourdit, gris.",
        "maman|Jusqu'au lion, sans te presser.",
        "enfant-f|Sans me presser.",
        "narrateur|Une goutte de chaîne sonne sur le bleu, et s'en va.",
    ],
    (3, 2, 2): [
        "narrateur|Nina plonge le seau dans l'eau du banc.",
        "narrateur|Le ciel gris entre dans le bleu.",
        "enfant-f|Il a pris le ciel.",
        "papa|Tes grenouilles, aussi.",
        "narrateur|Gauche. Droit. Deux ronds autour des bottes.",
        "maman|Tu le portes droit ?",
        "enfant-f|Oui. Il est lourd.",
        "narrateur|Nina marche vers la grande flaque, pas à pas.",
        "papa|Les chaînes, derrière, se taisent.",
        "enfant-f|On va au lion.",
        "narrateur|Rien ne déborde. L'anse est froide dans la paume.",
        "maman|Le bassin va te le rendre, plus clair.",
        "narrateur|Le banc a une tache ronde, où le seau a bu.",
    ],
    (3, 2, 3): [
        "narrateur|Nina baisse le seau dans la grande flaque, trop vite.",
        "narrateur|Il se remplit d'un coup, trop lourd.",
        "enfant-f|Aïe, mes bras.",
        "papa|Un peu moins ?",
        "narrateur|Elle reverse un filet, puis s'arrête.",
        "narrateur|Gauche au bord. Droit ensuite.",
        "maman|Le seau reflète la fontaine, un instant.",
        "enfant-f|Le lion est dedans !",
        "narrateur|Nina lève le bleu. Le lion sort du seau, reste de pierre.",
        "papa|Tu l'as vu deux fois.",
        "enfant-f|Dehors, et dedans.",
        "narrateur|Les bottes sont dans le bassin. Le seau pèse juste assez.",
        "narrateur|Une chaîne, loin, bouge sans bruit.",
    ],
    (3, 3, 1): [
        "narrateur|Une goutte de chaîne tombe sur l'oreille du doudou.",
        "enfant-f|Je t'essuie.",
        "narrateur|Nina frotte le tissu à sa manche.",
        "papa|Tes bottes, dans la petite flaque.",
        "narrateur|Gauche. Droit. L'eau qui tremble sous les sièges.",
        "maman|Lui au sec. Toi dans l'eau.",
        "enfant-f|Chacun son tour.",
        "narrateur|Nina marche vers le banc, le doudou haut.",
        "narrateur|Elle entre près du bois, un pied, puis l'autre.",
        "papa|Le lion, après.",
        "enfant-f|Il va sentir le buis, et l'eau.",
        "narrateur|La chaîne s'est tue. Les bottes parlent, flouc.",
        "narrateur|L'oreille du doudou est sèche, un peu froide.",
    ],
    (3, 3, 2): [
        "narrateur|Le doudou regarde le banc. Nina aussi.",
        "narrateur|Elle veut l'asseoir sur le bois mouillé.",
        "enfant-f|Non. Trop humide pour toi.",
        "maman|Les bottes, elles, aiment l'eau du banc.",
        "narrateur|Gauche. Droit. L'eau du ciel autour des grenouilles.",
        "papa|Tu le gardes contre toi ?",
        "enfant-f|Oui. Il voit le bois, de loin.",
        "narrateur|Nina marche vers la grande flaque.",
        "narrateur|Le doudou a le nez au lion, les pieds d'elle dans l'eau.",
        "maman|Chacun sa place.",
        "enfant-f|Oui.",
        "narrateur|Les chaînes restent derrière, inutiles et goutteuses.",
        "narrateur|Le banc brille, vide, et ça va.",
    ],
    (3, 3, 3): [
        "narrateur|Nina sent le buis, et l'eau froide, tout contre le bassin.",
        "narrateur|Elle serre le doudou. Elle veut le grand saut.",
        "enfant-f|Non. On entre proprement.",
        "papa|Le bord ?",
        "narrateur|Gauche. Droit. L'eau large, jusqu'aux chevilles.",
        "maman|Lui, il sent le buis aussi ?",
        "enfant-f|Oui. Et le lion.",
        "narrateur|Le doudou a une goutte du filet sur le ventre.",
        "papa|Une seule.",
        "narrateur|Nina ne l'essuie pas tout de suite. Elle regarde le bassin.",
        "enfant-f|On a fait tout le chemin.",
        "narrateur|Les sièges, loin, bougent un peu.",
        "narrateur|Les grenouilles sont au bout, dans l'eau du lion.",
    ],
}


FIN = {
    (1, 1, 1): [
        "narrateur|Nina a les deux grenouilles dans l'assiette d'eau, puis au bassin.",
        "enfant-f|Le ballon a un grain, maman.",
        "maman|Je le vois, beige sur le jaune.",
        "papa|Tes pieds ont fait le chemin, un puis l'autre.",
        "narrateur|Un grain de sable reste sur la grenouille gauche.",
        "narrateur|La petite flaque du bac redevient lisse.",
        "narrateur|La fontaine fait son chhh, tout près du lion.",
        "enfant-f|On est allés jusqu'ici.",
        "narrateur|Le ballon ne roule plus, contre elle.",
        "narrateur|Ça sent le buis, et le sable mouillé.",
    ],
    (1, 1, 2): [
        "narrateur|Près du banc, l'eau du ciel s'est calmé sous les semelles.",
        "enfant-f|Le ballon a touché le ciel.",
        "maman|Un instant, oui.",
        "papa|Tes grenouilles ont marché jusqu'au bois.",
        "narrateur|Le ballon garde un cercle d'eau sur le flanc.",
        "narrateur|Le banc vert goutte, une fois, puis plus.",
        "narrateur|Au bout, le lion crache son filet.",
        "enfant-f|J'entends le chhh.",
        "narrateur|Nina le serre. Les joues sont roses.",
        "narrateur|Un grain de sable a voyagé jusque sous le banc.",
    ],
    (1, 1, 3): [
        "narrateur|Voilà le bassin. L'eau large entoure les bottes.",
        "enfant-f|Le ballon a flotté, papa.",
        "papa|Tu l'as rejoint, pas à pas.",
        "maman|Le lion t'a vue arriver.",
        "narrateur|Le ballon fait un rond dans la grande flaque, puis s'arrête.",
        "narrateur|Une perle tient sur le grain de sable.",
        "narrateur|Nina ne saute plus. Elle est là.",
        "enfant-f|Toutes les flaques, presque.",
        "narrateur|Le filet tombe. Le gravier est sombre, derrière.",
        "narrateur|Les grenouilles luisent, pleines du bassin.",
    ],
    (1, 2, 1): [
        "narrateur|Le seau a pris un peu de sable mouillé, puis de l'eau vraie.",
        "enfant-f|D'abord le pâté, après l'eau.",
        "maman|Oui. Dans cet ordre-là.",
        "papa|Tes bottes ont suivi le même chemin.",
        "narrateur|La petite flaque du bac est lisse, à nouveau.",
        "narrateur|Nina tient l'anse. Ça pèse juste ce qu'il faut.",
        "narrateur|Le lion de pierre fume un peu, comme au début.",
        "enfant-f|Je lui verse une goutte.",
        "narrateur|Un filet, puis elle s'arrête.",
        "narrateur|Un grain tourne au fond du bleu, et reste.",
    ],
    (1, 2, 2): [
        "narrateur|Le seau a sonné contre le banc. Le bois a un anneau sombre.",
        "enfant-f|C'est sa marque.",
        "papa|Et tes grenouilles, leur marque à elles ?",
        "enfant-f|Deux ronds, dans l'eau du ciel.",
        "maman|Le lion t'écoute, maintenant.",
        "narrateur|Nina pose le seau au bord du bassin.",
        "narrateur|L'eau du banc est grise. Celle du lion est plus claire.",
        "narrateur|Elle ne mélange plus trop tôt.",
        "enfant-f|Chacune son tour.",
        "narrateur|Le buis sent fort. Les épaules de Nina sont hautes.",
    ],
    (1, 2, 3): [
        "narrateur|Le seau a de l'eau du bassin, au fond, claire.",
        "enfant-f|C'est l'eau du lion.",
        "maman|Tu l'as prise après les bottes, pas avant.",
        "papa|La veste a séché, un peu.",
        "narrateur|Nina regarde le filet tomber dans le bleu.",
        "narrateur|La grande flaque a des ronds, qui s'élargissent.",
        "narrateur|Elle ne verse plus d'un coup.",
        "enfant-f|Je garde ça.",
        "narrateur|Le sable du bac est loin, collé à une semelle.",
        "narrateur|La fontaine tousse son chhh, content, on dirait.",
    ],
    (1, 3, 1): [
        "narrateur|L'oreille du doudou a perdu son grain, soufflé vers le buis.",
        "enfant-f|Il a vu la petite flaque, de haut.",
        "papa|Et toi, de dedans.",
        "maman|Chacun sa place.",
        "narrateur|Nina le serre. Le tissu est sec, sauf une ombre.",
        "narrateur|La petite flaque du bac ne bouge plus.",
        "narrateur|Au bassin, le lion crache, comme tout à l'heure.",
        "enfant-f|On a fini le chemin.",
        "narrateur|Les bottes sont mouillées. Lui, presque pas.",
        "narrateur|Ça sent le buis, et le coton tiède.",
    ],
    (1, 3, 2): [
        "narrateur|Le doudou a vu le ciel dans l'eau du banc, puis le lion.",
        "enfant-f|Deux ciels.",
        "maman|Un dans l'eau, un au-dessus.",
        "papa|Tes grenouilles ont choisi l'eau.",
        "narrateur|Nina le garde haut. Une petite tache sèche sur le museau.",
        "narrateur|Le banc goutte. Le bassin attend.",
        "narrateur|Elle arrive au lion, sans le baisser.",
        "enfant-f|Toi tu regardes. Moi je trempes.",
        "narrateur|Les épaules sont basses, puis elles se relèvent, fières.",
        "narrateur|Le filet chante. Le bois reste sombre.",
    ],
    (1, 3, 3): [
        "narrateur|Le doudou a une goutte du bassin sur le ventre.",
        "enfant-f|Une seule, c'est cadeau.",
        "papa|Le grand saut, lui, tu l'as laissé.",
        "maman|Un pied, puis l'autre. Ça tenait mieux.",
        "narrateur|Nina rit. Les bottes sont dans l'eau large.",
        "narrateur|Le grain de sable du bac a disparu au col.",
        "narrateur|Le lion de pierre fume, tout proche.",
        "enfant-f|Il m'a vue vaciller, puis marcher.",
        "narrateur|Elle ne vacille plus.",
        "narrateur|Le chhh recouvre le parc, doux comme une main.",
    ],
    (2, 1, 1): [
        "narrateur|Le ballon a glissé un peu sur la rampe, puis s'est sagement tenu.",
        "enfant-f|Il a voulu glisser sans moi.",
        "papa|Toi, tu as pris les marches.",
        "maman|Puis la petite eau, puis le banc.",
        "narrateur|Une goutte de rampe brille sur le jaune.",
        "narrateur|Nina arrive au bassin, le ballon contre le ventre.",
        "narrateur|Le toboggan est vide, luisant, derrière.",
        "enfant-f|On a glissé avec les pieds, plus loin.",
        "narrateur|Les grenouilles sont mouillées. Le plastique, non.",
        "narrateur|Le lion crache. Nina souffle, les joues roses.",
    ],
    (2, 1, 2): [
        "narrateur|Le ballon s'est assis un moment sur le banc vert.",
        "enfant-f|Il a laissé un rond.",
        "maman|Le bois s'en souvient.",
        "papa|Tes bottes aussi, dans l'eau du ciel.",
        "narrateur|Nina le porte jusqu'au lion, sans le relancer.",
        "narrateur|Le cercle d'eau sur le flanc sèche à moitié.",
        "narrateur|La rampe, derrière, n'a plus personne.",
        "enfant-f|J'entends le chhh.",
        "narrateur|Elle s'arrête au bord du bassin. Fière, calme.",
        "narrateur|Le gravier chante une dernière fois sous les semelles.",
    ],
    (2, 1, 3): [
        "narrateur|Le ballon a fait plouf, tout près du bassin, trop tôt.",
        "enfant-f|Je l'ai rejoint, lentement.",
        "papa|Par le bord. Pas d'un jet.",
        "maman|Le lion a reçu le jaune, puis toi.",
        "narrateur|Nina le serre. Il est froid, luisant.",
        "narrateur|Les ronds vont jusqu'à la pierre.",
        "narrateur|La rampe est loin. Le filet est là.",
        "enfant-f|On a fini autrement que glisser.",
        "narrateur|Les grenouilles sont mouillées jusqu'au col, contentes.",
        "narrateur|Nina pose le ballon au sec, sur la pierre chaude du bord.",
    ],
    (2, 2, 1): [
        "narrateur|Le seau a reçu une goutte du toboggan, puis mieux au banc.",
        "enfant-f|D'abord une, après une gorgée.",
        "maman|Oui. Ça a grossi.",
        "papa|Tes pieds aussi, d'une flaque à l'autre.",
        "narrateur|Nina pose le seau au bord du lion.",
        "narrateur|La goutte de rampe nage, minuscule, au milieu.",
        "narrateur|Elle ne verse pas. Elle montre.",
        "enfant-f|Regarde, papa.",
        "narrateur|Papa se penche. Le bleu tient le ciel et la goutte.",
        "narrateur|Le chhh répond, comme un oui.",
    ],
    (2, 2, 2): [
        "narrateur|Le seau pend, près du banc, une perle au bord.",
        "enfant-f|Il n'a pas débordé.",
        "papa|Tu as marché sans courir.",
        "maman|Le lion peut le prendre, s'il veut.",
        "narrateur|Nina pose le bleu sur la pierre du bassin.",
        "narrateur|La perle rentre. L'eau du banc est grise, sage.",
        "narrateur|La rampe, derrière, crisse au vent.",
        "enfant-f|On a glissé nulle part. On a marché.",
        "narrateur|Les bottes sont froides. Les mains, un peu rouges.",
        "narrateur|Nina souffle. Le filet tombe, régulier.",
    ],
    (2, 2, 3): [
        "narrateur|Le seau verse un filet dans le bassin, puis s'arrête.",
        "enfant-f|J'avais versé trop tôt, tout à l'heure.",
        "papa|Là, tu as pris, puis donné.",
        "maman|Dans l'ordre.",
        "narrateur|Nina tient l'anse. Le seau est plus léger.",
        "narrateur|Les bottes restent dans l'eau large, fières.",
        "narrateur|Une goutte de rampe a séché sur le bleu.",
        "enfant-f|Le lion a notre eau, et la sienne.",
        "narrateur|Le parc est calme. Le gravier, sombre.",
        "narrateur|Nina sourit, tout bas, sans sauter.",
    ],
    (2, 3, 1): [
        "narrateur|Le doudou a vu la rampe, depuis les bras, puis la petite eau.",
        "enfant-f|Sa tête est sèche.",
        "maman|Tu l'as relevée à temps.",
        "papa|Tes grenouilles, elles, ont trempé.",
        "narrateur|Nina arrive au lion, le tissu haut.",
        "narrateur|Une perle de rampe a disparu, essuyée.",
        "narrateur|Le toboggan brille, vide.",
        "enfant-f|On a descendu les marches. C'était mieux.",
        "narrateur|Les bottes font un dernier flouc, au bord du bassin.",
        "narrateur|Le chhh recouvre la joue du doudou, sans le mouiller.",
    ],
    (2, 3, 2): [
        "narrateur|Le doudou s'est appuyé au banc. Le bois lui a refroidi le dos.",
        "enfant-f|Il s'est reposé. Moi j'ai trempé.",
        "papa|Chacun son travail.",
        "maman|Le lion, maintenant, c'est pour vous deux.",
        "narrateur|Nina le serre. Une trace de bois sèche sur le tissu.",
        "narrateur|Les bottes sont dans la grande eau, près de la pierre.",
        "narrateur|La rampe est loin, inutile.",
        "enfant-f|J'entends le filet.",
        "narrateur|Elle ne baisse plus le doudou. Elle écoute.",
        "narrateur|Le banc garde une petite ombre, qui s'en va.",
    ],
    (2, 3, 3): [
        "narrateur|Le doudou écoute la fontaine, tout contre Nina.",
        "enfant-f|Il a entendu le chhh en premier.",
        "maman|Toi, tu as entendu tes bottes.",
        "papa|Flouc, flouc, jusqu'ici.",
        "narrateur|Nina ne saute plus. L'eau large lui tient les chevilles.",
        "narrateur|Une goutte du filet a frôlé le tissu, puis le bassin.",
        "narrateur|Les joues sont roses. Les épaules, basses, contentes.",
        "enfant-f|La rampe peut attendre.",
        "narrateur|Le lion crache. Le parc sent le buis.",
        "narrateur|Les grenouilles luisent, au bout du chemin.",
    ],
    (3, 1, 1): [
        "narrateur|Le ballon a passé sous la chaîne, une perle sur le jaune.",
        "enfant-f|La chaîne l'a salué.",
        "papa|Tes pieds ont salué la petite eau.",
        "maman|Puis le banc. Puis le lion.",
        "narrateur|Nina tient le ballon. La perle sèche.",
        "narrateur|Les sièges bougent un peu, loin, sans elle.",
        "narrateur|Au bassin, le filet tombe, régulier.",
        "enfant-f|Les bottes, c'était mieux que se balancer.",
        "narrateur|Elle pose le jaune sur la pierre. Il tient.",
        "narrateur|Ça sent le fer des chaînes, et le buis.",
    ],
    (3, 1, 2): [
        "narrateur|Le ballon a roulé jusqu'au pied du banc, et s'est tenu là.",
        "enfant-f|Il a choisi l'eau du ciel.",
        "maman|Toi, tu l'as suivie, pied par pied.",
        "papa|Le lion t'attendait, droit devant.",
        "narrateur|Nina arrive, le jaune froid dans les mains.",
        "narrateur|Un rond d'eau reste au pied du banc, souvenir.",
        "narrateur|Les chaînes se taisent.",
        "enfant-f|On les a laissées.",
        "narrateur|Le bassin entoure les bottes. Nina souffle.",
        "narrateur|Le ciel du banc, et le ciel vrai, sont les mêmes.",
    ],
    (3, 1, 3): [
        "narrateur|Le ballon s'est arrêté au bord de la grande flaque.",
        "narrateur|Nina le porte ensuite dans ses bras.",
        "enfant-f|Il n'a pas voulu le grand bain d'un coup.",
        "papa|Toi non plus.",
        "maman|Le lion l'a vu arriver porté, pas lancé.",
        "narrateur|Nina le pose au sec, sur la pierre.",
        "narrateur|Une goutte de chaîne a séché sur le flanc.",
        "narrateur|Les grenouilles, elles, sont dans l'eau large.",
        "enfant-f|Chacun son bain.",
        "narrateur|Le filet chante. Les sièges, loin, sont vides.",
        "narrateur|Nina a les joues chaudes, et les pieds froids, contents.",
    ],
    (3, 2, 1): [
        "narrateur|Le seau est froid, sous la balançoire, puis plus lourd au banc.",
        "enfant-f|D'abord vide, après gris.",
        "maman|Comme tes bottes : d'abord hors de l'eau, après dedans.",
        "papa|Le lion va le voir plein.",
        "narrateur|Nina pose le bleu au bord du bassin.",
        "narrateur|Une goutte de chaîne a sonné, et s'en est allée.",
        "narrateur|Les sièges bougent. Elle, non.",
        "enfant-f|Je reste ici.",
        "narrateur|L'anse a réchauffé un peu dans la paume.",
        "narrateur|Le chhh du lion recouvre le fer des chaînes.",
    ],
    (3, 2, 2): [
        "narrateur|Le seau a pris un peu d'eau du banc. Le ciel est dedans.",
        "enfant-f|Il a bu le banc.",
        "papa|Tes grenouilles aussi.",
        "maman|Le bassin va lui donner plus clair.",
        "narrateur|Nina pose le seau. L'eau grise tremble, puis s'arrête.",
        "narrateur|Le banc a une tache ronde, souvenir du bleu.",
        "narrateur|Les chaînes, derrière, ne servent plus.",
        "enfant-f|On a mieux que se balancer.",
        "narrateur|Les bottes sont au lion. Nina les sent, froides, justes.",
        "narrateur|Le buis sent. Le fer, moins.",
    ],
    (3, 2, 3): [
        "narrateur|Le seau reflète la fontaine, un instant, puis Nina boit des yeux le lion.",
        "enfant-f|Il était dedans, et dehors.",
        "papa|Deux fois, oui.",
        "maman|Tes bras ont appris le poids, trop, puis assez.",
        "narrateur|Le seau pèse juste. Les bottes sont dans l'eau large.",
        "narrateur|Une chaîne, loin, bouge sans bruit.",
        "narrateur|Nina ne reverse plus d'un coup.",
        "enfant-f|Je garde le lion dans le bleu, un peu.",
        "narrateur|Elle sourit. Le filet tombe, inlassable.",
        "narrateur|Le gravier sombre a mené jusqu'ici, pas à pas.",
    ],
    (3, 3, 1): [
        "narrateur|Le doudou a une oreille sèche, essuyée à la manche.",
        "enfant-f|La chaîne l'avait salué trop fort.",
        "maman|Toi, tu l'as mis au sec.",
        "papa|Tes bottes, elles, ont pris la petite eau.",
        "narrateur|Nina arrive au lion, le tissu haut.",
        "narrateur|L'oreille est froide, propre.",
        "narrateur|Les sièges gouttent, loin, sans eux.",
        "enfant-f|Chacun son tour, je t'avais dit.",
        "narrateur|Les grenouilles luisent. Lui, presque pas.",
        "narrateur|Le buis, et le chhh, ferment le parc.",
    ],
    (3, 3, 2): [
        "narrateur|Le doudou a regardé le banc, de loin. Nina, de dedans.",
        "enfant-f|Trop humide pour lui. Bien pour moi.",
        "papa|Chacun sa place.",
        "maman|Le lion vous a tous les deux, maintenant.",
        "narrateur|Nina le serre. Les bottes sont au bassin.",
        "narrateur|Le banc brille, vide, et ça va.",
        "narrateur|Les chaînes restent goutteuses, inutiles.",
        "enfant-f|On n'a pas eu besoin de se balancer.",
        "narrateur|Elle écoute le filet. Les épaules descendent, contentes.",
        "narrateur|Le ciel du banc s'est tu. Celui du lion, non.",
    ],
    (3, 3, 3): [
        "narrateur|Le doudou sent le buis, et l'eau froide, contre Nina.",
        "enfant-f|On a fait tout le chemin, proprement.",
        "maman|Un pied, puis l'autre, jusqu'au lion.",
        "papa|Tes grenouilles sont au bout.",
        "narrateur|Une goutte du filet tient sur le ventre de tissu.",
        "narrateur|Nina ne l'essuie pas. Elle la garde un moment.",
        "narrateur|Les sièges, loin, bougent. Ici, rien.",
        "enfant-f|J'aime le chhh.",
        "narrateur|Les bottes sont dans l'eau du lion, jusqu'aux chevilles.",
        "narrateur|Le parc entier semble tenir dans ce petit bruit.",
    ],
}

Q_FIELDS = {
    "expected_answer": "bottes",
    "accepted_examples": "bottes | les bottes | d'abord les bottes | une puis l'autre | la botte | les deux bottes | les grenouilles",
    "retry_prompt": "Elle enfile les bottes, puis une flaque. D'abord ?",
    "engine_ok_text": "Oui, les bottes.",
    "engine_near_text": "Tu es tout près. Les pieds, avant l'eau.",
    "engine_timeout_text": "On continue.",
}

SONS = {
    "CHK_T0000_P0000": "fontaine,gravier,bottes",
}


def profile_for(cid: str, kind: str) -> str:
    if kind == "passage_debut":
        return "opening"
    if kind in {"transition_question"}:
        return "choice"
    if kind == "passage_question":
        return "clue"
    if kind == "passage_fin":
        return "ending"
    if cid.endswith("_C0001"):
        return "confirm"
    if "_T0003_P000" in cid and not cid.endswith("_P0000"):
        return "resolution"
    if "_T0002_P000" in cid and "_T0003_" not in cid:
        return "action"
    return "obstacle"


def extra_emphasis(cid: str, kind: str, profile: str) -> dict:
    extra: dict = {}
    if profile == "opening":
        extra["emphasis"] = "flaques"
    elif profile == "clue":
        extra["emphasis"] = "bottes"
    elif profile == "confirm":
        extra["emphasis"] = "grenouilles"
    elif profile == "resolution":
        extra["emphasis"] = "fontaine" if "fontaine" in "" else None
    return extra


def sons_for(cid: str, kind: str, i: int | None, j: int | None) -> str:
    if cid in SONS:
        return SONS[cid]
    if kind == "transition_question" or kind == "passage_question":
        return ""
    if cid.endswith("_C0001"):
        return "bottes,gravier"
    if kind == "passage_fin":
        return "fontaine"
    if kind == "passage" and i and "_T0002_" not in cid:
        return {1: "sable", 2: "goutte", 3: "chaine"}[i]
    if j and "_T0003_" not in cid and "_T0002_P000" in cid:
        return {1: "ballon", 2: "seau", 3: ""}[j]
    if "_T0003_P000" in cid and kind == "passage":
        return "eau,flaque"
    return ""


def build() -> tuple[dict[str, list[str]], dict[str, dict]]:
    s: dict[str, list[str]] = {}
    meta: dict[str, dict] = {}
    s["CHK_T0000_P0000"] = OPENING
    s["CHK_T0001_P0000"] = T1
    meta["CHK_T0001_P0000"] = {
        "option_1_label": "le bac à sable",
        "option_2_label": "le toboggan",
        "option_3_label": "les balançoires",
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = L1[i]
        s[f"{p}_Q0001"] = Q[i]
        s[f"{p}_C0001"] = C[i]
        s[f"{p}_T0002_P0000"] = T2[i]
        meta[f"{p}_T0002_P0000"] = {
            "option_1_label": "le ballon",
            "option_2_label": "le seau",
            "option_3_label": "le doudou",
        }
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = L2[(i, j)]
            s[f"{p2}_T0003_P0000"] = t3_lines(j)
            meta[f"{p2}_T0003_P0000"] = {
                "option_1_label": "la petite flaque",
                "option_2_label": "la flaque du banc",
                "option_3_label": "la grande flaque",
            }
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = L3[(i, j, k)]
                s[f"{p3}_F0001"] = FIN[(i, j, k)]
    s = {cid: split_lines(lines) for cid, lines in s.items()}
    return s, meta


def path_stats(scripts: dict) -> None:
    def txt(cid: str) -> str:
        return " ".join(ln.split("|", 1)[1] for ln in scripts[cid])

    lengths = []
    fins = []
    l3s = []
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            for k in (1, 2, 3):
                ids = [
                    "CHK_T0000_P0000",
                    "CHK_T0001_P0000",
                    f"CHK_T0001_P000{i}",
                    f"CHK_T0001_P000{i}_Q0001",
                    f"CHK_T0001_P000{i}_C0001",
                    f"CHK_T0001_P000{i}_T0002_P0000",
                    f"CHK_T0001_P000{i}_T0002_P000{j}",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001",
                ]
                n = sum(words(txt(c)) for c in ids)
                lengths.append(n)
                fins.append(txt(ids[-1]))
                l3s.append(txt(ids[-2]))
    if len(set(fins)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fins))}")
    if len(set(l3s)) != 27:
        raise SystemExit(f"L3 non distincts: {len(set(l3s))}")
    print(f"chemins mots min={min(lengths)} max={max(lengths)} moy={sum(lengths)//len(lengths)}")


def parse_ijk(cid: str) -> tuple[int | None, int | None]:
    i = j = None
    if "_P0001" in cid[:20] or cid.startswith("CHK_T0001_P0001"):
        pass
    # L1 id CHK_T0001_P000{i}
    import re
    m = re.search(r"CHK_T0001_P000(\d)", cid)
    if m:
        i = int(m.group(1))
    m2 = re.search(r"_T0002_P000(\d)", cid)
    if m2:
        j = int(m2.group(1))
    return i, j


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    scripts, meta = build()
    preview(scripts)
    path_stats(scripts)
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={list(extra_ids)[:8]}")
    out_chunks = []
    piper_vals = set()
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        prof = profile_for(cid, kind)
        i, j = parse_ijk(cid)
        extra = extra_emphasis(cid, kind, prof)
        if cid.endswith("_Q0001"):
            extra["fields"] = dict(Q_FIELDS)
        if cid in meta:
            extra.setdefault("fields", {}).update(meta[cid])
        # resolution emphasis if word present
        text_join = " ".join(ln.split("|", 1)[1] for ln in scripts[cid])
        if prof == "resolution":
            extra["emphasis"] = "fontaine" if "fontaine" in text_join.lower() else (
                "bassin" if "bassin" in text_join.lower() else None
            )
        elif prof == "action":
            if "ballon" in text_join.lower():
                extra["emphasis"] = "ballon"
            elif "seau" in text_join.lower():
                extra["emphasis"] = "seau"
            elif "doudou" in text_join.lower():
                extra["emphasis"] = "doudou"
        elif prof == "obstacle":
            extra["emphasis"] = None
        elif prof == "ending":
            extra["emphasis"] = "lion" if "lion" in text_join.lower() else None
        nc = apply_tts(c, scripts[cid], sons_for(cid, kind, i, j), prof, extra)
        piper_vals.add(nc["length_scale_piper"])
        out_chunks.append(nc)
    if len(piper_vals) < 4:
        raise SystemExit(f"piper trop uniforme: {piper_vals}")
    out = dict(src)
    out["fil_rouge"] = (
        "Nina veut traverser toutes les flaques jusqu'à la fontaine du parc. "
        "Elle saute trop tôt, une botte seulement : la chaussette pique. "
        "Elle enfile l'autre grenouille, prend ballon, seau ou doudou, "
        "puis une flaque, puis la suivante, jusqu'au lion de pierre."
    )
    out["title"] = "Les flaques de Nina près de la fontaine"
    out["characters"] = "Nina, papa, maman"
    out["setting"] = "parc de la fontaine après la pluie, gravier, banc vert, bottes à grenouilles"
    out["chunks"] = out_chunks
    check(SID, out["age_band"], out["chunks"])
    # TTS presence
    for c in out_chunks:
        if not c.get("notes") or "arc=" not in c["notes"]:
            raise SystemExit(f"notes manquantes {c['chunk_id']}")
        if not c.get("text_xai_tags") or c["text_xai_tags"] == c["text"]:
            raise SystemExit(f"xai trop plat {c['chunk_id']}")
        if "<speak>" not in (c.get("text_ssml") or ""):
            raise SystemExit(f"ssml plat {c['chunk_id']}")
    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size} piper={sorted(piper_vals)}")
    relecture(
        SID,
        "Les flaques de Nina près de la fontaine",
        (
            "Parc après la pluie, lion de pierre, buis, banc vert, bottes à grenouilles. "
            "Désir : traverser toutes les flaques jusqu'à la fontaine. "
            "1re tentative : une botte, saut trop tôt, chaussette glacée, visage plissé. "
            "T1 bac / toboggan / balançoires (autre obstacle pour l'autre botte). "
            "T2 ballon / seau / doudou (autre manière d'aller à l'eau). "
            "T3 petite flaque / flaque du banc / grande flaque (autre ordre, autre climax). "
            "Leçon vécue : un pied puis l'autre, une flaque puis la suivante. "
            "27 fins : grain, ciel du banc, ballon flotté, seau du lion, goutte de chaîne, chhh."
        ),
        (
            "P0 F-NAR-019. Tics encore/déjà/tout doux/calme retirés. Gabarit cassé : "
            "L1/L2/L3/fins écrits par chemin, 27 textes de fin distincts. "
            "Pas COL-015 (pas d'escargot, pas d'enquête). Léa absente. "
            "Q=bottes. Merci vécu à la 2e botte. "
            "TTS par chunk : notes arc/intention/émotion, xai_tags, ssml, piper variable. "
            "Relu ouverture + 3 L1 + 9 L2 + 27 L3/fins. Pas apply."
        ),
    )


if __name__ == "__main__":
    main()
