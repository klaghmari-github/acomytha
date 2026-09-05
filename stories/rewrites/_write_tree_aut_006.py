#!/usr/bin/env python3
"""TREE-AUT-006 — Le manteau jaune de Nina (F-NAR-019, N2, AUT.AFF.003, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-006"
N2 = LIMITS["N2"]
TITLE = "Le manteau jaune de Nina"
TICS = re.compile(
    r"\b(tout doux|tout calme|encore|déjà|deja|une étape après l'autre)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "merle",
    "miel",
    "grand-père",
    "grand-pere",
    "maîtresse",
    "maitresse",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
    "marque fine",
    "ombre-flèche",
    "ombre en forme de flèche",
    "étoile brune",
    "fil pâle",
    "croissant",
    "virgule",
    "bouton de nacre",
    "bouton nacre",
    "nœud de raphia",
    "nœud raphia",
    "pois ivoire",
    "grain savon",
    "grain vanille",
    "pastille colle",
    "capuchon",
    "grain doré",
    "brin safran",
    "anneau",
    "clou tête",
    "grain d'ambre",
    "goutte de cire",
    "larme de bronze",
    "point de cire",
    "bracelet d'écorce",
    "boucle d'étain",
    "dent de laitue",
    "éclat de zinc",
    "éclat de thym",
    "lune d'étain",
    "grain de grenat",
    "grain d'indigo",
    "grain de brique",
    "éclat vert",
    "écaille",
    "vis verte",
    "cristal de sucre",
    "inès",
    "soupe",
    "tout lente",
    "amir",
    "aniss",
    "sarah",
    "chouchou",
    "mila",
    "nino",
    "raphaël",
    "raphael",
    "victorino",
    "victorina",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="éclat de bouton",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience_curieuse; "
            "intensite=2; destinataire=enfant; sous_texte=elle_veut_le_jaune_seule_avant_la_flaque; "
            "tempo=naturel; volume=medium; sourire=léger; respiration=ample"
        ),
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note=(
            "arc=choix; intention=inviter; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=ton_choix_change_la_manière; "
            "tempo=suspendu; volume=medium; sourire=léger; "
            "respiration=pause_avant_choix"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="manche",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=le_premier_geste_a_raté; "
            "tempo=suspendu; volume=soft; sourire=aucun; "
            "respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="manteau jaune",
        note=(
            "arc=confirmation; intention=relancer; emotion=élan_prudent; intensite=1; "
            "destinataire=enfant; sous_texte=elle_garde_le_jaune_et_ralentit; "
            "tempo=naturel; volume=medium; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note=(
            "arc=action; intention=entraîner; emotion=impatience; intensite=2; "
            "destinataire=enfant; sous_texte=elle_tire_trop_vite_le_jaune; "
            "tempo=vif; volume=medium; sourire=léger; respiration=courte"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=découragement_léger; intensite=2; destinataire=enfant; "
            "sous_texte=le_jaune_résiste_elle_refuse_de_foncer; tempo=resserré; "
            "volume=medium; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="éclat de bouton",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; "
            "emotion=fierté_calme; intensite=2; destinataire=enfant; "
            "sous_texte=elle_met_le_jaune_seule_grâce_à_l_éclat; tempo=naturel; "
            "volume=medium; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="éclat de bouton",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; sous_texte=l_éclat_paie_le_début; "
            "tempo=posé; volume=soft; sourire=léger; respiration=ample"
        ),
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    starts: list[str] = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
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
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"extra {bad}: {ph}")
        tok = ph.split()[0].lower() if role == "narrateur" else ""
        starts.append(tok)
        out.append(f"{role}|{ph}")
    run = 1
    for i in range(1, len(starts)):
        if starts[i] and starts[i] == starts[i - 1]:
            run += 1
            if run >= 4:
                raise SystemExit(f"puces {starts[i]}")
        else:
            run = 1
    return out


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp:
        e = esc(emp)
        if e in body:
            body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict) -> str:
    body = text
    emp = m.get("emphasis")
    if emp and emp in body:
        body = body.replace(emp, f"<emphasis>{emp}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    tag = m.get("pitchTag")
    if tag:
        body = f"<{tag}>{body}</{tag}>"
    pause = m["pause"]
    suffix = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + suffix).strip()


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if "note" in extra:
        m["note"] = extra["note"]
    text, script = from_script(lines)
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
    out = deepcopy(src)
    out["text"] = text
    out["script"] = script
    out["sons"] = sons if sons is not None else (src.get("sons") or "")
    if out["sons"] is None:
        out["sons"] = ""
    out["text_ssml"] = ssml(text, m)
    out["text_xai_tags"] = xai(text, m)
    out["rate_wpm"] = m["wpm"]
    out["rate_label"] = m["rate"]
    out["speed_xai"] = m["speed"]
    out["length_scale_piper"] = m["piper"]
    out["pitch_label"] = m["pitch"]
    out["pitch_ssml"] = m["pitchSsml"]
    out["pitch_xai_tag"] = m["pitchTag"]
    out["volume_label"] = m["volume"]
    out["volume_db"] = m["db"]
    out["emphasis_words"] = m.get("emphasis") or ""
    out["pause_before_ms"] = extra.get("pause_before_ms", 0)
    out["pause_after_ms"] = m["pause"]
    out["pause_sentence_ms"] = m["sentence"]
    out["style_energy"] = m["energy"]
    out["style_contour"] = m["contour"]
    out["noise_scale_piper"] = m["noise"]
    out["kokoro_speed"] = m["speed"]
    out["melo_speed"] = m["speed"]
    out["espeak_amp"] = 82 if m["volume"] == "soft" else 100
    out["espeak_pitch"] = 42 if m["pitch"] == "low" else 50
    out["espeak_word_gap"] = 12 if m["rate"] == "slow" else 8
    out["notes"] = m["note"]
    out["night_policy"] = "play"
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.items():
        if k in ("emphasis", "note", "pause_before_ms"):
            continue
        out[k] = v
    return out


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=l_éclat_de_bouton_paie_la_flaque; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


OPENING = vet(
    [
        "narrateur|La vitre de la cuisine porte une feuille collée par la pluie.",
        "narrateur|Nina connaît cette pièce, l'odeur d'orange et de laine mouillée.",
        "narrateur|Un détail paraît neuf, sur le manteau jaune.",
        "narrateur|Un éclat de bouton y tient un bout de jour.",
        "narrateur|Dehors, la flaque du jardin brille, large comme une assiette.",
        "papa|Tu as vu le jaune, Nina ?",
        "enfant-f|Je le mets, toute seule !",
        "narrateur|En ce moment, Nina tire le manteau vers elle.",
        "narrateur|Elle tire trop fort, trop vite.",
        "narrateur|Le crochet fait clac, sec.",
        "narrateur|Le manteau jaune tombe, une manche à l'envers.",
        "enfant-f|Il ne veut pas !",
        "papa|Tu veux sortir maintenant, Nina ?",
        "enfant-f|Avant que le soleil boive la flaque !",
        "maman|Le tissu est lourd, et tes bras sont pressés.",
        "narrateur|Nina souffle, les épaules basses.",
        "papa|Merci d'avoir dit ce que tu veux.",
        "narrateur|Un éclat de bouton brille, au sol, près du tapis.",
        "narrateur|Nina ramasse le manteau, froid dans ses mains.",
        "enfant-f|Je recommence, sans le crochet.",
        "maman|Tes mains d'abord, le jaune ensuite.",
        "narrateur|Le soleil lèche la flaque, dehors.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|La flaque attend, et le manteau jaune aussi.",
        "narrateur|Le matin, après la sieste, ou le soir.",
        "maman|C'est quel moment, pour sortir, Nina ?",
    ]
)

T1 = {
    1: dict(
        lab="le matin",
        ans="manche",
        acc="manche | la manche | une manche | à l'envers | envers",
        retry="Une manche est restée à l'envers. Qu'est-ce qui est à l'envers ?",
        ok="Oui, c'est la manche.",
        sons="pain,tissu",
        emp="manche",
        passage=vet(
            [
                "narrateur|Le matin, la lumière est pâle, sur le pain.",
                "narrateur|La flaque de la nuit est large, presque un lac.",
                "narrateur|Nina enfile le manteau jaune, trop pressée.",
                "enfant-f|J'y vais !",
                "narrateur|Une manche reste à l'envers, coincée.",
                "narrateur|Son poing cherche la sortie, et trouve du tissu.",
                "enfant-f|Ma main est perdue !",
                "papa|La manche, Nina.",
                "maman|Elle est à l'envers, comme un sac.",
                "narrateur|Nina tire, et le tissu se tord plus fort.",
                "enfant-f|Je veux la grande flaque !",
                "papa|Le jaune d'abord, dans le bon sens.",
            ]
        ),
        question=vet(
            [
                "narrateur|Nina a tiré trop vite, une manche restée à l'envers.",
                "maman|Qu'est-ce qui est resté à l'envers ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Nina tourne la manche, lentement.",
                "enfant-f|Le bon sens.",
                "maman|Tu as trouvé le trou.",
                "papa|Le jaune t'attend, sans courir.",
                "enfant-f|Je le tiens.",
                "narrateur|L'éclat de bouton revient, sur le tissu froid.",
                "maman|Où veux-tu le mettre, maintenant ?",
                "narrateur|Le matin reste pâle, et la flaque attend.",
            ]
        ),
    ),
    2: dict(
        lab="après la sieste",
        ans="bras",
        acc="bras | les bras | ses bras | coincé | coincés | un nœud",
        retry="Ses deux bras se sont coincés. Qu'est-ce qui s'est coincé ?",
        ok="Oui, ce sont les bras.",
        sons="draps,tissu",
        emp="bras",
        passage=vet(
            [
                "narrateur|Après la sieste, le soleil mange la flaque.",
                "narrateur|Le manteau jaune est plissé, sur le crochet.",
                "narrateur|Nina a les cheveux en bataille, les yeux plissés.",
                "enfant-f|Vite, elle part !",
                "narrateur|Elle pousse les deux bras ensemble, dans le jaune.",
                "narrateur|Les manches se croisent, et les poignets se coincent.",
                "enfant-f|Je suis un nœud !",
                "maman|Un bras, puis l'autre.",
                "papa|Le tissu plissé tient tes poignets.",
                "narrateur|Nina se débat, et le jaune la serre.",
                "enfant-f|Ça pince !",
                "papa|Tes bras se sont coincés, Nina.",
            ]
        ),
        question=vet(
            [
                "narrateur|Nina a voulu les deux bras ensemble.",
                "papa|Qu'est-ce qui s'est coincé ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Nina sort un bras, puis l'autre, sans tirer.",
                "enfant-f|Un, puis l'autre.",
                "papa|Le nœud s'est défait.",
                "maman|Le jaune n'est plus un piège.",
                "enfant-f|Je le tiens, plissé, mais à moi.",
                "narrateur|L'éclat de bouton perce un pli, tout petit.",
                "papa|Où le mets-tu, maintenant ?",
                "narrateur|La flaque a rétréci, ronde comme une tasse.",
            ]
        ),
    ),
    3: dict(
        lab="le soir",
        ans="tissu",
        acc="tissu | le tissu | manches | les manches | collé | mouillé",
        retry="Le tissu a collé. Qu'est-ce qui a collé ?",
        ok="Oui, c'est le tissu.",
        sons="goutte,tissu",
        emp="tissu",
        passage=vet(
            [
                "narrateur|Le soir, la flaque n'est plus qu'une pièce ronde.",
                "narrateur|Le manteau jaune est humide, lourd de pluie.",
                "narrateur|Nina le serre contre elle, trop fort.",
                "enfant-f|La dernière flaque, à moi !",
                "narrateur|Les manches collent, tissu contre tissu.",
                "narrateur|Elle cherche le trou, et trouve du mouillé.",
                "enfant-f|Ça colle !",
                "maman|Le tissu a bu le jardin.",
                "papa|Tes mains glissent, trop humides.",
                "narrateur|Nina secoue le jaune, et une goutte tombe.",
                "enfant-f|Il me tient !",
                "papa|Le tissu a collé, manche contre manche.",
            ]
        ),
        question=vet(
            [
                "narrateur|Le tissu mouillé a collé, manche contre manche.",
                "maman|Qu'est-ce qui a collé ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Nina écarte les manches, une goutte à la fois.",
                "enfant-f|Elles se parlent moins.",
                "maman|Le jaune s'ouvre, un peu.",
                "papa|Tes mains peuvent passer, maintenant.",
                "enfant-f|Je le tiens, lourd, mais à moi.",
                "narrateur|L'éclat de bouton tremble, sur le tissu mouillé.",
                "maman|Où le mets-tu, ce soir ?",
                "narrateur|La pièce d'eau attend, minuscule, dans l'herbe.",
            ]
        ),
    ),
}


T2_CHOICE = {
    1: vet(
        [
            "narrateur|Le manteau jaune est dans ses mains, plus sage.",
            "narrateur|La cuisine, le jardin, ou la chambre.",
            "papa|Où le mets-tu, ce matin ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Le manteau jaune n'est plus un nœud, sur elle.",
            "narrateur|La cuisine, le jardin, ou la chambre.",
            "maman|Où le mets-tu, après la sieste ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Le manteau jaune pèse moins, un peu séché.",
            "narrateur|La cuisine, le jardin, ou la chambre.",
            "papa|Où le mets-tu, ce soir ?",
        ]
    ),
}


def t2_scene(a: int, b: int) -> list[str]:
    scenes = {
        (1, 1): [
            "narrateur|Le matin, la cuisine sent l'orange, et le pain.",
            "narrateur|Nina pose le manteau sur la chaise, trop vite.",
            "enfant-f|Je boutonne, et je sors !",
            "narrateur|Ses doigts ont essuyé la feuille sur la vitre.",
            "narrateur|Les boutons glissent, et le tissu refuse.",
            "papa|Tes mains sont mouillées, Nina.",
            "maman|Le jaune n'aime pas la course.",
            "enfant-f|Rien ne marche !",
            "narrateur|Elle s'arrête, l'éclat de bouton caché dans la vapeur.",
            "enfant-f|Je ne fonce pas.",
            "papa|Tu le mets comment, maintenant ?",
            "enfant-f|Je sèche, puis je cherche le bouton.",
        ],
        (1, 2): [
            "narrateur|Le matin, l'herbe mouillée pique ses chevilles.",
            "narrateur|Nina sort, le manteau à moitié mis.",
            "enfant-f|La grande flaque, à moi !",
            "narrateur|Le vent tire une manche, trop vide.",
            "narrateur|Le jaune glisse d'une épaule, vers l'eau.",
            "papa|Le manteau va boire la flaque.",
            "maman|Une épaule ne suffit pas.",
            "enfant-f|Il part !",
            "narrateur|Elle s'arrête au bord, sans sauter.",
            "enfant-f|Pas trop vite.",
            "narrateur|Un éclat de bouton clignote, trop bas, dans l'herbe.",
            "papa|Tu le remets, avant la flaque ?",
        ],
        (1, 3): [
            "narrateur|Le matin, Nina emporte le jaune dans la chambre.",
            "narrateur|Le lit est froid, une chaussette dessus.",
            "enfant-f|Je le mets ici, toute seule !",
            "narrateur|Elle s'assoit trop pressée, une manche avale la chaussette.",
            "narrateur|Son bras cherche, et trouve du coton.",
            "enfant-f|Ma manche a un pied !",
            "maman|La chaussette n'est pas un bras.",
            "papa|Sors-la, puis passe la main.",
            "narrateur|Nina tire, et le tissu se tord.",
            "enfant-f|Je m'arrête.",
            "narrateur|Dans le miroir, l'éclat de bouton a disparu.",
            "enfant-f|Je cherche le bouton, pas la chaussette.",
        ],
        (2, 1): [
            "narrateur|Après la sieste, la cuisine est tiède, un peu sombre.",
            "narrateur|Le manteau jaune est plissé, sur la chaise.",
            "enfant-f|Je boutonne les plis, vite !",
            "narrateur|Les trous se cachent dans le tissu froissé.",
            "narrateur|Ses doigts pincent du jaune, pas le bouton.",
            "papa|Le pli cache le bouton.",
            "maman|Lisse un peu, avec la paume.",
            "enfant-f|Je ne trouve rien !",
            "narrateur|Elle s'arrête, un éclat de bouton perce un pli.",
            "enfant-f|Je ne fonce pas.",
            "papa|Tu as vu le bout de jour ?",
            "enfant-f|Je lisse, puis je ferme.",
        ],
        (2, 2): [
            "narrateur|Après la sieste, le soleil a rongé la flaque.",
            "narrateur|Nina court dehors, le jaune à l'envers sur une épaule.",
            "enfant-f|Il reste de l'eau !",
            "narrateur|Le soleil lui pique les yeux, et le manteau glisse.",
            "narrateur|Une manche traîne dans l'herbe chaude.",
            "papa|Le jaune boit l'herbe, pas toi.",
            "maman|Remets-le, avant le petit rond d'eau.",
            "enfant-f|Il fuit !",
            "narrateur|Elle s'arrête, et elle ne saute pas.",
            "enfant-f|D'abord le manteau.",
            "narrateur|Un éclat de bouton clignote, contre le soleil.",
            "papa|Tu le mets droit, Nina ?",
        ],
        (2, 3): [
            "narrateur|Après la sieste, le lit est un tas de draps.",
            "narrateur|Nina jette le manteau sur le tas, et s'y plonge.",
            "enfant-f|Je m'habille dans le nid !",
            "narrateur|Les draps et le jaune se mélangent.",
            "narrateur|Son bras entre, et se perd.",
            "enfant-f|Je suis sous le tissu !",
            "maman|Le lit n'est pas une manche.",
            "papa|Sors la tête, puis le bras.",
            "narrateur|Nina souffle, coincée, les cheveux en bataille.",
            "enfant-f|Je m'arrête.",
            "narrateur|Un éclat de bouton brille, trop loin, sous un drap.",
            "enfant-f|Je cherche le bouton, pas le nid.",
        ],
        (3, 1): [
            "narrateur|Le soir, la lampe allume la table, et l'orange.",
            "narrateur|Le manteau jaune est humide, lourd, sur la chaise.",
            "enfant-f|Je le ferme, et j'y vais !",
            "narrateur|Les boutons se cachent, le tissu brille trop.",
            "narrateur|Ses doigts glissent sur le mouillé.",
            "papa|La lampe aide, si tu ralentis.",
            "maman|Le jaune a bu le jardin.",
            "enfant-f|Je ne vois pas les trous !",
            "narrateur|Elle s'arrête, un éclat de bouton prend la lampe.",
            "enfant-f|Je ne fonce pas.",
            "papa|Ce bout de jour, c'est ton bouton.",
            "enfant-f|Je suis le point.",
        ],
        (3, 2): [
            "narrateur|Le soir, la flaque n'est plus qu'une pièce ronde.",
            "narrateur|Nina avance dans l'herbe, le jaune ouvert, lourd.",
            "enfant-f|La dernière eau, à moi !",
            "narrateur|Les manches collent, une goutte tombe dans l'herbe.",
            "narrateur|Le manteau tire vers le sol, trop mouillé.",
            "papa|Il est trop lourd, pour courir.",
            "maman|Ferme-le, avant le petit rond.",
            "enfant-f|Il me tire !",
            "narrateur|Elle s'arrête au bord, sans sauter.",
            "enfant-f|Pas trop vite.",
            "narrateur|Un éclat de bouton tremble, au-dessus de la pièce d'eau.",
            "papa|Tu le fermes, Nina ?",
        ],
        (3, 3): [
            "narrateur|Le soir, la chambre a une lampe ronde, près du lit.",
            "narrateur|Nina pose le manteau humide sur la chaise.",
            "enfant-f|Je le mets ici, pour les surprendre !",
            "narrateur|Une manche collée refuse le bras.",
            "narrateur|Le tissu mouillé fait ventouse, contre elle.",
            "maman|Décoller, puis passer.",
            "papa|Le jaune a soif de tes bras, trop vite.",
            "enfant-f|Ça colle ma main !",
            "narrateur|Elle s'arrête, et elle souffle.",
            "enfant-f|Je ne tire plus.",
            "narrateur|Un éclat de bouton prend la lampe, sur la chaise.",
            "enfant-f|Je suis le bouton, pas la colle.",
        ],
    }
    return vet(scenes[(a, b)])


T3_CHOICE = {
    1: vet(
        [
            "narrateur|Le jaune est ouvert, dans la cuisine.",
            "narrateur|Le ballon rouge, le seau bleu, ou le doudou.",
            "maman|Tu prends quoi, avec le manteau ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Le jaune est ouvert, près de la flaque.",
            "narrateur|Le ballon rouge, le seau bleu, ou le doudou.",
            "papa|Tu prends quoi, pour le jardin ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Le jaune est ouvert, sur le lit.",
            "narrateur|Le ballon rouge, le seau bleu, ou le doudou.",
            "maman|Tu prends quoi, dans la chambre ?",
        ]
    ),
}


RES = {
    (1, 1, 1): vet(
        [
            "narrateur|Dans la cuisine, le manteau jaune attend, ouvert.",
            "enfant-f|Le ballon rouge, dans la manche, et je sors !",
            "narrateur|Le ballon glisse dans la manche, et la gonfle.",
            "narrateur|Son bras cherche, et trouve du caoutchouc.",
            "enfant-f|Ma manche a un ventre !",
            "papa|Il y a un ballon, pas un bras.",
            "narrateur|Nina veut tirer, mais le tissu résiste.",
            "enfant-f|Je m'arrête.",
            "narrateur|Elle regarde, un éclat de bouton perce le jaune.",
            "narrateur|Elle sort le ballon, puis passe le bras, vide.",
            "maman|Tu as vu le trou, toute seule.",
            "enfant-f|Le jaune est à moi, le ballon aussi.",
        ]
    ),
    (1, 1, 2): vet(
        [
            "narrateur|Dans la cuisine, le seau bleu passe sous la table.",
            "enfant-f|Le seau, et le manteau, ensemble !",
            "narrateur|L'anse accroche un bouton, net.",
            "narrateur|Nina tire, le bouton penche, presque parti.",
            "enfant-f|Lâche-moi !",
            "papa|L'anse tient le bouton.",
            "narrateur|Nina lâche l'anse, et elle ne fonce plus.",
            "narrateur|Un éclat de bouton montre le point coincé.",
            "narrateur|Elle décroche, boutonne, puis prend le seau.",
            "maman|Le jaune est fermé, le seau est libre.",
            "enfant-f|Je peux verser la flaque, après.",
        ]
    ),
    (1, 1, 3): vet(
        [
            "narrateur|Le doudou est sur la table, près de l'orange.",
            "enfant-f|Lui, dans la poche, et je sors !",
            "narrateur|Elle tient le doudou, et le bouton glisse.",
            "narrateur|Il lui manque une main, et le jaune bâille.",
            "enfant-f|J'ai trop de choses !",
            "maman|Pose-le, le temps du bouton.",
            "narrateur|Nina pose le doudou, et elle regarde le tissu.",
            "narrateur|Un éclat de bouton lui montre le trou.",
            "narrateur|Elle ferme, puis glisse le doudou dans la poche.",
            "papa|Il voyage au chaud.",
            "enfant-f|Il va voir la flaque, lui aussi.",
        ]
    ),
    (1, 2, 1): vet(
        [
            "narrateur|Au bord de la flaque, le vent joue avec le jaune.",
            "enfant-f|Le ballon, sur l'eau, et moi aussi !",
            "narrateur|Le fil du ballon s'enroule autour d'un bouton.",
            "narrateur|Le ballon tire, et le manteau s'ouvre d'un coup.",
            "enfant-f|Il me déshabille !",
            "papa|Le fil a pris le bouton.",
            "narrateur|Nina ne court plus, elle suit le fil du pouce.",
            "narrateur|Un éclat de bouton montre où ça tourne.",
            "narrateur|Elle déroule, boutonne, tient le fil dans la paume.",
            "maman|Le jaune reste, le ballon aussi.",
            "enfant-f|Je tape la flaque, habillée !",
        ]
    ),
    (1, 2, 2): vet(
        [
            "narrateur|Nina penche le seau bleu vers la grande flaque.",
            "enfant-f|Je remplis, le jaune ouvert !",
            "narrateur|L'eau saute, une goutte entre dans la manche.",
            "narrateur|L'anse tape un bouton, et le jaune bascule.",
            "enfant-f|J'ai froid dans le bras !",
            "maman|Le seau d'abord posé, le bouton ensuite.",
            "narrateur|Nina pose le seau dans l'herbe, et souffle.",
            "narrateur|Un éclat de bouton brille, au-dessus de l'eau.",
            "narrateur|Elle ferme le jaune, puis puise, sans se pencher trop.",
            "papa|Le seau a de l'eau, toi tu es au sec.",
            "enfant-f|La flaque vient avec moi, un peu.",
        ]
    ),
    (1, 2, 3): vet(
        [
            "narrateur|Le doudou veut voir la grande flaque, lui aussi.",
            "enfant-f|Je le porte, et je saute !",
            "narrateur|Une oreille du doudou glisse dans la manche.",
            "narrateur|Nina saute presque, le doudou tire vers l'herbe.",
            "enfant-f|Il me retient !",
            "papa|Sors l'oreille, avant le saut.",
            "narrateur|Nina s'arrête au bord, sans sauter.",
            "narrateur|Un éclat de bouton clignote, trop près de l'eau.",
            "narrateur|Elle libère l'oreille, boutonne, prend le doudou contre elle.",
            "maman|Il a les pieds au sec, toi aussi.",
            "enfant-f|On tape ensemble, sans tomber.",
        ]
    ),
    (1, 3, 1): vet(
        [
            "narrateur|Sur le lit froid, le ballon rouge roule vers le jaune.",
            "enfant-f|Il m'aide à habiller le bras !",
            "narrateur|Le ballon entre dans la manche, comme un coude faux.",
            "narrateur|Nina pousse, le ballon rebondit contre le miroir.",
            "enfant-f|Il se moque !",
            "maman|Le ballon n'est pas un coude.",
            "narrateur|Nina le rattrape, et elle ne fonce plus.",
            "narrateur|Dans le miroir, un éclat de bouton revient, net.",
            "narrateur|Elle vide la manche, passe le bras, ferme le jaune.",
            "papa|Le miroir a vu le vrai coude.",
            "enfant-f|Le ballon peut rouler, moi je suis prête.",
        ]
    ),
    (1, 3, 2): vet(
        [
            "narrateur|Nina a traîné le seau bleu jusqu'au tapis de la chambre.",
            "enfant-f|Je le remplis après, près du lit !",
            "narrateur|L'anse accroche le pied du lit, et un bouton.",
            "narrateur|Le jaune se tend, coincé entre le bois et l'anse.",
            "enfant-f|Je suis attachée !",
            "papa|Décroche l'anse, pas le bouton.",
            "narrateur|Nina s'assoit, et elle regarde le point coincé.",
            "narrateur|Un éclat de bouton montre le fil de l'anse.",
            "narrateur|Elle libère, boutonne, pose le seau près de la porte.",
            "maman|Le seau attend le jardin, le jaune t'attend toi.",
            "enfant-f|Je sors habillée, le seau à côté.",
        ]
    ),
    (1, 3, 3): vet(
        [
            "narrateur|Le doudou est sous l'oreiller, le jaune sur les genoux.",
            "enfant-f|On s'habille tous les deux !",
            "narrateur|Elle enroule le manteau autour d'elle et du doudou.",
            "narrateur|Deux corps, une manche, et rien ne passe.",
            "enfant-f|On est trop !",
            "maman|Lui sur l'oreiller, toi dans le jaune.",
            "narrateur|Nina pose le doudou, et elle écoute le tissu.",
            "narrateur|Un éclat de bouton s'allume, sur le genou.",
            "narrateur|Elle passe les bras, ferme, loge le doudou dans la poche.",
            "papa|Deux voyageurs, un manteau.",
            "enfant-f|On va à la flaque, ensemble.",
        ]
    ),
    (2, 1, 1): vet(
        [
            "narrateur|Le ballon rouge s'est glissé sous la chaise, près des plis.",
            "enfant-f|Il vient dans la manche plissée !",
            "narrateur|Le ballon gonfle un pli, et le bouton disparaît.",
            "narrateur|Nina cherche le trou, et pince du caoutchouc.",
            "enfant-f|Le bouton est un ballon !",
            "papa|Sors le ballon, le pli s'ouvre.",
            "narrateur|Nina lâche, et lisse le jaune, sans tirer.",
            "narrateur|Un éclat de bouton perce le pli, enfin.",
            "narrateur|Elle sort le ballon, lisse, boutonne, un par un.",
            "maman|Le jaune n'est plus un nœud.",
            "enfant-f|Le ballon peut attendre, près de l'orange.",
        ]
    ),
    (2, 1, 2): vet(
        [
            "narrateur|Le seau bleu a roulé contre la chaise, sous la table.",
            "enfant-f|Je le prends, le jaune plissé ouvert !",
            "narrateur|L'anse accroche un pli, et un bouton ensemble.",
            "narrateur|Nina tire les deux, le tissu se froisse plus fort.",
            "enfant-f|Ça serre !",
            "maman|L'anse ou le bouton, pas les deux.",
            "narrateur|Nina pose le seau, et lisse le pli du plat de la main.",
            "narrateur|Un éclat de bouton revient, sorti du froissé.",
            "narrateur|Elle décroche, boutonne, reprend le seau par le bord.",
            "papa|Le bord, pas l'anse, cette fois.",
            "enfant-f|Le seau vient, le jaune reste fermé.",
        ]
    ),
    (2, 1, 3): vet(
        [
            "narrateur|Le doudou a dormi sur la chaise, dans les plis du jaune.",
            "enfant-f|On se réveille dans le manteau !",
            "narrateur|Une patte du doudou tient un bouton, comme une main.",
            "narrateur|Nina secoue, le doudou tombe, le bouton presque aussi.",
            "enfant-f|Il a volé mon bouton !",
            "papa|Ouvre la patte, doucement.",
            "narrateur|Nina déplie les doigts de tissu, un par un.",
            "narrateur|Un éclat de bouton se libère, entre les pattes.",
            "narrateur|Elle range le doudou, lisse, ferme le jaune.",
            "maman|Il n'a plus le bouton, il a la poche.",
            "enfant-f|Il voyage, sans voler.",
        ]
    ),
    (2, 2, 1): vet(
        [
            "narrateur|Près du petit rond d'eau, le ballon rouge a soif de vent.",
            "enfant-f|Il saute la flaque, moi aussi !",
            "narrateur|Le ballon part, le fil tire le bouton, le jaune s'ouvre.",
            "narrateur|Nina court un pas, puis le manteau lui fuit les épaules.",
            "enfant-f|Je suis nue au vent !",
            "maman|Le fil, avant le saut.",
            "narrateur|Nina s'arrête, le soleil pique, et elle ne fonce plus.",
            "narrateur|Un éclat de bouton clignote, trop loin, sur l'herbe.",
            "narrateur|Elle rattrape le jaune, déroule le fil, boutonne au chaud.",
            "papa|Le ballon peut voler, toi tu restes habillée.",
            "enfant-f|Je pose un pied dans le petit rond.",
        ]
    ),
    (2, 2, 2): vet(
        [
            "narrateur|Le seau bleu vise le petit rond, trop étroit.",
            "enfant-f|Je prends toute l'eau, d'un coup !",
            "narrateur|Le seau racle la terre, l'anse accroche un bouton.",
            "narrateur|Nina penche, et le jaune boit une goutte chaude.",
            "enfant-f|Il est mouillé, le pli !",
            "papa|Pose le seau, ferme, puis puise.",
            "narrateur|Nina pose, et lisse le pli mouillé, sans courir.",
            "narrateur|Un éclat de bouton sèche au soleil, sur le jaune.",
            "narrateur|Elle boutonne, puis puise la dernière eau, sans racle.",
            "maman|Le seau a le rond, toi tu as le jaune.",
            "enfant-f|J'ai sauvé la flaque, un peu.",
        ]
    ),
    (2, 2, 3): vet(
        [
            "narrateur|Le doudou traîne une oreille dans l'herbe chaude.",
            "enfant-f|Il veut le petit rond, lui aussi !",
            "narrateur|L'oreille ramasse de la terre, puis entre dans la manche.",
            "narrateur|Nina lève le bras, une mèche de terre tombe sur le bouton.",
            "enfant-f|Il est sale, mon bouton !",
            "maman|L'oreille dehors, le bouton propre.",
            "narrateur|Nina s'arrête, et souffle sur le bouton, sans frotter fort.",
            "narrateur|Un éclat de bouton reparaît, sous la terre.",
            "narrateur|Elle sort l'oreille, boutonne, porte le doudou à bout de bras.",
            "papa|Lui voit l'eau, sans la boire.",
            "enfant-f|On regarde le rond, propres.",
        ]
    ),
    (2, 3, 1): vet(
        [
            "narrateur|Sur le tas de draps, le ballon rouge fait un dos de montagne.",
            "enfant-f|Je m'habille par-dessus la montagne !",
            "narrateur|Le jaune glisse du ballon, et avale un drap.",
            "narrateur|Nina pousse le bras, et habille le lit, pas elle.",
            "enfant-f|Le lit a ma manche !",
            "papa|Le ballon à terre, le drap à part.",
            "narrateur|Nina descend du tas, et elle ne fonce plus.",
            "narrateur|Un éclat de bouton brille, tombé entre deux draps.",
            "narrateur|Elle ramasse le jaune, chasse le drap, passe les bras.",
            "maman|Le lit reste au lit, toi tu es habillée.",
            "enfant-f|Le ballon peut garder le nid.",
        ]
    ),
    (2, 3, 2): vet(
        [
            "narrateur|Le seau bleu est monté sur le lit, comme un bateau.",
            "enfant-f|On navigue, le jaune pour voile !",
            "narrateur|L'anse accroche un bouton, et un drap ensemble.",
            "narrateur|Nina tire la voile, le seau bascule vide sur l'oreiller.",
            "enfant-f|Mon oreiller a un seau !",
            "maman|Le seau à terre, le bouton libre.",
            "narrateur|Nina pose le seau, et démêle le drap du bouton.",
            "narrateur|Un éclat de bouton sort du drap, un peu froissé.",
            "narrateur|Elle lisse, boutonne, laisse le seau près de la porte.",
            "papa|La mer, c'est dehors, plus tard.",
            "enfant-f|Le jaune est ma voile, fermée.",
        ]
    ),
    (2, 3, 3): vet(
        [
            "narrateur|Le doudou est au fond du nid, sous le jaune.",
            "enfant-f|On se cache, et on s'habille !",
            "narrateur|Nina se couvre, et le doudou lui mange une manche.",
            "narrateur|Deux têtes, zéro trou, le tissu étouffe un rire.",
            "enfant-f|Je ne vois plus le jour !",
            "papa|Sors la tête, et cherche le bouton.",
            "narrateur|Nina recule le drap, et cherche, sans tirer.",
            "narrateur|Un éclat de bouton lui fait un œil, sous le nid.",
            "narrateur|Elle sort, passe les bras, ferme, prend le doudou.",
            "maman|Le nid reste, vous partez habillés.",
            "enfant-f|On a trouvé le jour, sur le bouton.",
        ]
    ),
    (3, 1, 1): vet(
        [
            "narrateur|Sous la lampe, le ballon rouge prend une ombre ronde.",
            "enfant-f|L'ombre m'aide à trouver la manche !",
            "narrateur|Nina suit l'ombre, le ballon entre, pas son bras.",
            "narrateur|La manche s'allume, trop pleine, trop ronde.",
            "enfant-f|J'ai mis la lune !",
            "papa|La lune dehors, le bras dedans.",
            "narrateur|Nina rit, puis s'arrête, et vide la manche.",
            "narrateur|Un éclat de bouton prend la lampe, à la bonne place.",
            "narrateur|Elle passe le bras, boutonne, laisse le ballon sous la table.",
            "maman|Le jaune a un vrai coude, ce soir.",
            "enfant-f|La lune peut rouler, moi je sors.",
        ]
    ),
    (3, 1, 2): vet(
        [
            "narrateur|Le seau bleu, sous la lampe, a une ombre d'anse.",
            "enfant-f|Je prends l'ombre et l'anse, avec le jaune !",
            "narrateur|L'anse vraie accroche un bouton, et l'ombre ment.",
            "narrateur|Nina tire l'ombre, et le bouton vrai penche.",
            "enfant-f|L'ombre m'a trompée !",
            "maman|Regarde le tissu, pas le mur.",
            "narrateur|Nina baisse les yeux, et elle ne fonce plus.",
            "narrateur|Un éclat de bouton, sous la lampe, dit le vrai.",
            "narrateur|Elle décroche, boutonne, prend le seau des deux mains.",
            "papa|Le seau vient, sans l'ombre.",
            "enfant-f|Je vais à la petite pièce d'eau.",
        ]
    ),
    (3, 1, 3): vet(
        [
            "narrateur|Le doudou, sous la lampe, a les yeux trop brillants.",
            "enfant-f|Il veut la poche, tout de suite !",
            "narrateur|Nina force la poche, le jaune trop ouvert.",
            "narrateur|Le doudou gonfle le côté, le bouton n'atteint pas le trou.",
            "enfant-f|La poche est trop pleine !",
            "papa|Poche après le bouton.",
            "narrateur|Nina retire le doudou, et aligne le bouton, lentement.",
            "narrateur|Un éclat de bouton marche vers le trou, sous la lampe.",
            "narrateur|Elle ferme, puis glisse le doudou, plus sage.",
            "maman|La poche a de la place, maintenant.",
            "enfant-f|Il vient voir la dernière flaque.",
        ]
    ),
    (3, 2, 1): vet(
        [
            "narrateur|Au-dessus de la pièce d'eau, le ballon rouge mange le dernier jour.",
            "enfant-f|Il éclaire la flaque, pour moi !",
            "narrateur|Nina lève le ballon, une manche se vide, trop haute.",
            "narrateur|Le jaune glisse, le fil s'enroule au bouton du bas.",
            "enfant-f|Je perds le manteau, dans la nuit !",
            "maman|Le fil, puis les épaules.",
            "narrateur|Nina s'accroupit, et elle ne lève plus le bras.",
            "narrateur|Un éclat de bouton tremble, juste au-dessus de l'eau.",
            "narrateur|Elle déroule, remonte le jaune, boutonne, tient le fil bas.",
            "papa|Le ballon éclaire, toi tu restes couverte.",
            "enfant-f|Je touche la pièce d'eau, du bout du pied.",
        ]
    ),
    (3, 2, 2): vet(
        [
            "narrateur|Nina pose le seau bleu sur la pièce d'eau, trop juste.",
            "enfant-f|Je l'emporte, la dernière goutte !",
            "narrateur|Le seau cloche, l'anse pince le bouton du bas.",
            "narrateur|Nina soulève, le jaune s'ouvre, une goutte fuit.",
            "enfant-f|Elle s'en va, ma flaque !",
            "papa|Ferme, puis lève, tout droit.",
            "narrateur|Nina pose le seau, et aligne le bouton, sans courir.",
            "narrateur|Un éclat de bouton se mire dans la pièce d'eau.",
            "narrateur|Elle boutonne, lève le seau d'aplomb, sauve la goutte.",
            "maman|La goutte est à toi, le jaune aussi.",
            "enfant-f|J'ai la dernière eau, habillée.",
        ]
    ),
    (3, 2, 3): vet(
        [
            "narrateur|Le doudou frissonne, au bord de la pièce d'eau.",
            "enfant-f|Il a froid, je le mets dans le jaune !",
            "narrateur|Elle ouvre trop, et le doudou glisse vers l'eau.",
            "narrateur|Nina rattrape une patte, le manteau tombe sur l'herbe.",
            "enfant-f|On a failli boire la flaque !",
            "maman|Lui contre toi, le jaune par-dessus.",
            "narrateur|Nina serre le doudou, et ramasse le jaune, sans sauter.",
            "narrateur|Un éclat de bouton sèche dans l'herbe, à côté de l'eau.",
            "narrateur|Elle enfile, boutonne, loge le doudou, loin du rond.",
            "papa|Personne n'a bu, ce soir.",
            "enfant-f|On salue la flaque, au sec.",
        ]
    ),
    (3, 3, 1): vet(
        [
            "narrateur|Sous la lampe ronde, le ballon rouge fait un soleil faux.",
            "enfant-f|Je m'habille à son soleil !",
            "narrateur|Nina suit la tache rouge, la manche se trompe de trou.",
            "narrateur|Son bras sort par le col, pas par la manche.",
            "enfant-f|J'ai la tête dans le bras !",
            "papa|Le vrai jour, c'est le bouton.",
            "narrateur|Nina recule, et cherche autre chose que le rouge.",
            "narrateur|Un éclat de bouton, plus petit, plus vrai, sous la lampe.",
            "narrateur|Elle retire le bras, trouve la manche, ferme le jaune.",
            "maman|Le faux soleil peut rouler, toi tu es droite.",
            "enfant-f|Je descends les surprendre, habillée.",
        ]
    ),
    (3, 3, 2): vet(
        [
            "narrateur|Le seau bleu, près de la chaise, attend le jardin de demain.",
            "enfant-f|Je le prends, au cas où la flaque vit !",
            "narrateur|L'anse accroche le dossier, et le bouton du jaune.",
            "narrateur|Nina avance, et la chaise la suit, trop collée.",
            "enfant-f|La chaise vient avec moi !",
            "maman|Décroche l'anse, laisse la chaise.",
            "narrateur|Nina s'assoit, et suit l'anse du doigt, sans tirer.",
            "narrateur|Un éclat de bouton dit où ça tient, sous la lampe.",
            "narrateur|Elle libère, boutonne, laisse le seau pour plus tard.",
            "papa|La flaque de ce soir n'a pas besoin du seau.",
            "enfant-f|Moi j'ai besoin du jaune, fermé.",
        ]
    ),
    (3, 3, 3): vet(
        [
            "narrateur|Le doudou, sur la chaise, a pris la place du jaune.",
            "enfant-f|On échange : lui le manteau, moi le lit !",
            "narrateur|Nina habille le doudou, les manches pendent, trop longues.",
            "narrateur|Elle rit, puis veut le jaune, plus de bras pour elle.",
            "enfant-f|Il a tout pris !",
            "papa|Déshabille-le, habille-toi.",
            "narrateur|Nina retire le jaune du doudou, lentement, sans fâcher.",
            "narrateur|Un éclat de bouton la salue, rendu, sous la lampe.",
            "narrateur|Elle s'enfile, boutonne, remet le doudou dans la poche.",
            "maman|Chacun sa place, ce soir.",
            "enfant-f|Moi le jaune, lui la poche, la flaque après.",
        ]
    ),
}


def ending(a: int, b: int, c: int) -> list[str]:
    recap = {
        (1, 1, 1): "J'ai sorti le ballon de la manche, puis j'ai fermé.",
        (1, 1, 2): "J'ai décroché l'anse, puis j'ai boutonné.",
        (1, 1, 3): "J'ai posé le doudou, puis la poche.",
        (1, 2, 1): "J'ai déroulé le fil, et j'ai tapé la flaque.",
        (1, 2, 2): "J'ai fermé, puis j'ai puisé, au sec.",
        (1, 2, 3): "J'ai libéré l'oreille, et on a tapé ensemble.",
        (1, 3, 1): "J'ai vidé la manche, le miroir a vu le coude.",
        (1, 3, 2): "J'ai décroché l'anse du lit, puis le jaune.",
        (1, 3, 3): "J'ai mis le doudou à part, puis nous deux.",
        (2, 1, 1): "J'ai sorti le ballon du pli, puis j'ai lissé.",
        (2, 1, 2): "J'ai pris le seau par le bord, le jaune fermé.",
        (2, 1, 3): "J'ai ouvert la patte, le bouton est revenu.",
        (2, 2, 1): "J'ai rattrapé le jaune, et un pied dans le rond.",
        (2, 2, 2): "J'ai sauvé la petite eau, sans racle.",
        (2, 2, 3): "J'ai soufflé la terre, on a regardé propres.",
        (2, 3, 1): "J'ai habillé moi, pas le lit.",
        (2, 3, 2): "J'ai laissé le seau, le jaune pour voile fermée.",
        (2, 3, 3): "J'ai trouvé le jour, sur le bouton, hors du nid.",
        (3, 1, 1): "J'ai mis le vrai coude, pas la lune.",
        (3, 1, 2): "J'ai cru l'éclat, pas l'ombre de l'anse.",
        (3, 1, 3): "J'ai fermé, puis la poche, plus sage.",
        (3, 2, 1): "J'ai tenu le fil bas, et touché l'eau.",
        (3, 2, 2): "J'ai levé d'aplomb, la goutte est à moi.",
        (3, 2, 3): "On a failli tomber, on a salué au sec.",
        (3, 3, 1): "J'ai suivi le petit éclat, pas le faux soleil.",
        (3, 3, 2): "J'ai laissé la chaise, et le seau pour demain.",
        (3, 3, 3): "Je lui ai repris le jaune, chacun sa place.",
    }[(a, b, c)]
    invite = {
        1: "Raconte, Nina, le pain est tiède.",
        2: "Dis-nous, l'orange est ouverte.",
        3: "À toi, la lampe écoute.",
    }[a]
    keepsake = {
        1: "La feuille sur la vitre a séché, un coin levé.",
        2: "L'herbe du jardin garde un rond plus pâle.",
        3: "Le lit a un creux, où le jaune a posé.",
    }[b]
    first = {
        1: "Plus tard, le pain est sur la table, tiède.",
        2: "Plus tard, l'orange est ouverte, en quartiers.",
        3: "Plus tard, la lampe de la cuisine est allumée.",
    }[a]
    mid = {
        1: "Nina a les joues chaudes, le jaune fermé.",
        2: "Une goutte sèche sur le poignet, sans courir.",
        3: "Le crochet, derrière, n'a plus rien à tenir.",
    }[c]
    papa_line = {
        (1, 1, 1): "Le ballon n'était pas un bras, toi.",
        (1, 1, 2): "L'anse a lâché, le bouton a tenu.",
        (1, 1, 3): "La poche a fait le voyage, lui aussi.",
        (1, 2, 1): "Tu as tapé l'eau, habillée.",
        (1, 2, 2): "Le seau a puisé, toi tu es sèche.",
        (1, 2, 3): "L'oreille est sortie à temps.",
        (1, 3, 1): "Le miroir a vu le vrai coude.",
        (1, 3, 2): "Le lit n'a pas gardé l'anse.",
        (1, 3, 3): "Deux voyageurs, un seul jaune.",
        (2, 1, 1): "Le pli a rendu le bouton, toi.",
        (2, 1, 2): "Le bord du seau a suffi.",
        (2, 1, 3): "La patte a rendu ce qu'elle tenait.",
        (2, 2, 1): "Un pied a suffi, pour le petit rond.",
        (2, 2, 2): "Tu as sauvé l'eau, sans la racle.",
        (2, 2, 3): "Le bouton est propre, comme l'oreille.",
        (2, 3, 1): "Le lit n'a plus ta manche.",
        (2, 3, 2): "La mer, c'était trop tôt.",
        (2, 3, 3): "Vous avez trouvé le jour, hors du nid.",
        (3, 1, 1): "Le vrai coude a chassé la lune.",
        (3, 1, 2): "Tu as cru le tissu, pas le mur.",
        (3, 1, 3): "La poche a attendu son tour.",
        (3, 2, 1): "Le fil est resté bas, toi couverte.",
        (3, 2, 2): "La goutte n'est pas partie.",
        (3, 2, 3): "Personne n'a bu, ce soir.",
        (3, 3, 1): "Le petit jour a battu le faux soleil.",
        (3, 3, 2): "La chaise est restée, toi tu es partie.",
        (3, 3, 3): "Chacun sa place, le jaune à toi.",
    }[(a, b, c)]
    last = {
        (1, 1, 1): "L'éclat de bouton garde une goutte ronde, face à la flaque.",
        (1, 1, 2): "L'éclat de bouton tient une perle d'eau, au bord du seau.",
        (1, 1, 3): "L'éclat de bouton brille contre le nez du doudou, au chaud.",
        (1, 2, 1): "L'éclat de bouton accroche un fil rouge, au-dessus de l'herbe.",
        (1, 2, 2): "L'éclat de bouton tremble dans la flaque, puis se tient.",
        (1, 2, 3): "L'éclat de bouton sèche une mèche du doudou, au vent.",
        (1, 3, 1): "L'éclat de bouton se pose dans le miroir, à côté du ballon.",
        (1, 3, 2): "L'éclat de bouton veille sur le seau, au pied du lit.",
        (1, 3, 3): "L'éclat de bouton dort près du doudou, sur l'oreiller.",
        (2, 1, 1): "L'éclat de bouton perce un pli du jaune, près de l'orange.",
        (2, 1, 2): "L'éclat de bouton sèche une goutte, au fond du seau bleu.",
        (2, 1, 3): "L'éclat de bouton réchauffe la poche, où le doudou voyage.",
        (2, 2, 1): "L'éclat de bouton suit le ballon, au-dessus du petit rond.",
        (2, 2, 2): "L'éclat de bouton se mire dans l'eau, au fond du seau.",
        (2, 2, 3): "L'éclat de bouton sèche l'oreille du doudou, trop mouillée.",
        (2, 3, 1): "L'éclat de bouton chasse l'ombre du ballon, sur le drap.",
        (2, 3, 2): "L'éclat de bouton guide l'anse, loin du tissu.",
        (2, 3, 3): "L'éclat de bouton ouvre la poche, trop pleine tout à l'heure.",
        (3, 1, 1): "L'éclat de bouton prend la lampe, sur le jaune fermé.",
        (3, 1, 2): "L'éclat de bouton tient une ombre de seau, sur la table.",
        (3, 1, 3): "L'éclat de bouton veille, pendant que le doudou s'endort.",
        (3, 2, 1): "L'éclat de bouton survit à la nuit, au-dessus de la pièce d'eau.",
        (3, 2, 2): "L'éclat de bouton tremble une dernière fois, dans le seau.",
        (3, 2, 3): "L'éclat de bouton sèche la patte du doudou, près de la flaque.",
        (3, 3, 1): "L'éclat de bouton et le ballon se disent bonjour, sous la lampe.",
        (3, 3, 2): "L'éclat de bouton reste, le seau vide, le jaune fermé.",
        (3, 3, 3): "L'éclat de bouton ferme la journée, sur le doudou endormi.",
    }[(a, b, c)]
    return vet(
        [
            f"narrateur|{first}",
            f"maman|{invite}",
            f"enfant-f|{recap}",
            f"narrateur|{keepsake}",
            f"narrateur|{mid}",
            f"papa|{papa_line}",
            f"narrateur|{last}",
        ]
    )


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple[list[str], str, str, dict]] = {}

    scripts["CHK_T0000_P0000"] = (
        OPENING,
        "opening",
        "pluie,orange,tissu",
        {"emphasis": "éclat de bouton"},
    )
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "le matin",
            "option_2_label": "après la sieste",
            "option_3_label": "le soir",
        },
    )

    t2_labs = ("la cuisine", "le jardin", "la chambre")
    t3_labs = ("le ballon rouge", "le seau bleu", "le doudou")
    t2_sons = {1: "orange,vapeur", 2: "herbe,eau", 3: "draps,tissu"}
    t2_emp = {1: "éclat de bouton", 2: "flaque", 3: "manteau"}
    t3_sons = {1: "ballon,tissu", 2: "seau,eau", 3: "doudou,tissu"}
    t3_emp = {1: "ballon", 2: "seau", 3: "doudou"}
    fin_sons = {1: "couverts,ballon", 2: "couverts,eau", 3: "couverts,doudou"}

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        t1 = T1[a]
        scripts[base] = (t1["passage"], "action", t1["sons"], {"emphasis": t1["emp"]})
        scripts[f"{base}_Q0001"] = (
            t1["question"],
            "clue",
            "",
            {
                "expected_answer": t1["ans"],
                "accepted_examples": t1["acc"],
                "retry_prompt": t1["retry"],
                "engine_ok_text": t1["ok"],
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
                "emphasis": t1["ans"],
            },
        )
        scripts[f"{base}_C0001"] = (
            t1["confirm"],
            "confirm",
            t1["sons"],
            {"emphasis": "éclat de bouton"},
        )
        scripts[f"{base}_T0002_P0000"] = (
            T2_CHOICE[a],
            "choice",
            "",
            {
                "option_1_label": t2_labs[0],
                "option_2_label": t2_labs[1],
                "option_3_label": t2_labs[2],
            },
        )
        for b in (1, 2, 3):
            leaf2 = f"{base}_T0002_P000{b}"
            scripts[leaf2] = (
                t2_scene(a, b),
                "obstacle",
                t2_sons[b],
                {"emphasis": t2_emp[b]},
            )
            scripts[f"{leaf2}_T0003_P0000"] = (
                T3_CHOICE[b],
                "choice",
                "",
                {
                    "option_1_label": t3_labs[0],
                    "option_2_label": t3_labs[1],
                    "option_3_label": t3_labs[2],
                },
            )
            for c in (1, 2, 3):
                leaf3 = f"{leaf2}_T0003_P000{c}"
                scripts[leaf3] = (
                    RES[(a, b, c)],
                    "resolution",
                    t3_sons[c],
                    {"emphasis": "éclat de bouton"},
                )
                scripts[f"{leaf3}_F0001"] = (
                    ending(a, b, c),
                    "ending",
                    fin_sons[c],
                    {"emphasis": "éclat de bouton", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra)[:8]}")

    chunks = []
    for c in src["chunks"]:
        cid = c["chunk_id"]
        lines, profile, sons, extra = scripts[cid]
        chunks.append(voice(by_src[cid], lines, profile, sons, extra))

    fins = [ch["text"] for ch in chunks if ch["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(fins))}/27")
    last_n = []
    for ch in chunks:
        if ch.get("kind") != "passage_fin":
            continue
        last = [x for x in ch["script"].splitlines() if x.startswith("narrateur|")][-1]
        last_n.append(last.split("|", 1)[1])
        last_low = last.split("|", 1)[1].lower()
        if "histoire" in last_low or "bravo" in last_low or "bon travail" in last_low:
            raise SystemExit(f"{ch['chunk_id']} fin mécanique: {last_low}")
        if "éclat de bouton" not in last_low:
            raise SystemExit(f"{ch['chunk_id']} fin sans indice: {last_low}")
    if len(set(last_n)) != 27:
        raise SystemExit(f"dernières images: {len(set(last_n))}/27")
    res_txt = [
        ch["text"]
        for ch in chunks
        if ch["kind"] == "passage"
        and "_T0003_P000" in ch["chunk_id"]
        and "_F0001" not in ch["chunk_id"]
        and not ch["chunk_id"].endswith("_T0003_P0000")
    ]
    if len(res_txt) != 27 or len(set(res_txt)) != 27:
        raise SystemExit(f"résolutions distinctes: {len(set(res_txt))}/{len(res_txt)}")

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "éclat de bouton" not in chunks[0]["text"].lower():
        raise SystemExit(f"{SID}: indice absent de l'ouverture")
    if "inès" in blob or "ines" in blob:
        raise SystemExit(f"{SID}: Inès residual")
    if "soupe" in blob:
        raise SystemExit(f"{SID}: gabarit soupe")
    merci_n = sum(
        1
        for ln in blob.splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
        if "merci" in ln or "bravo" in ln
    )
    if merci_n < 1:
        raise SystemExit(f"{SID}: merci/bravo adulte manquant")

    out = dict(src)
    out["fil_rouge"] = (
        "Dans la cuisine, une feuille de pluie colle à la vitre. Sur le manteau "
        "jaune, un éclat de bouton tient un bout de jour. Nina veut le mettre "
        "toute seule pour aller à la flaque du jardin avant que le soleil la "
        "boive. Elle tire trop vite : le manteau tombe, une manche à l'envers. "
        "Matin, sieste ou soir changent le tissu. Cuisine, jardin ou chambre "
        "changent l'obstacle. Ballon, seau ou doudou changent la ruse. Nina "
        "refuse de foncer, suit l'éclat, ferme le jaune. L'éclat paie le début."
    )
    out["title"] = TITLE
    out["characters"] = "Nina, papa, maman"
    out["setting"] = "cuisine embuée, manteau jaune, flaque du jardin"
    out["chunks"] = chunks
    check(SID, out["age_band"], out["chunks"])

    def path_words(a: int, b: int, c: int) -> int:
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
        mp = {ch["chunk_id"]: ch for ch in chunks}
        return sum(words(mp[i]["text"]) for i in ids)

    lengths = [path_words(a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    if min(lengths) < 380:
        raise SystemExit(f"chemin trop court: {min(lengths)}")

    t1s = [next(ch["text"] for ch in chunks if ch["chunk_id"] == f"CHK_T0001_P000{i}") for i in (1, 2, 3)]
    if len(set(t1s)) < 3:
        raise SystemExit("T1 ne change pas l'histoire")
    t2s = [
        next(ch["text"] for ch in chunks if ch["chunk_id"] == f"CHK_T0001_P0001_T0002_P000{j}")
        for j in (1, 2, 3)
    ]
    if len(set(t2s)) < 3:
        raise SystemExit("T2 ne change pas l'histoire")
    t3s = [
        next(
            ch["text"]
            for ch in chunks
            if ch["chunk_id"] == f"CHK_T0001_P0001_T0002_P0001_T0003_P000{k}"
        )
        for k in (1, 2, 3)
    ]
    if len(set(t3s)) < 3:
        raise SystemExit("T3 ne change pas l'histoire")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        "# TREE-AUT-006 — Le manteau jaune de Nina\n\n"
        "- **Nouveau titre :** *Le manteau jaune de Nina*\n"
        "- **Public :** 4–5 ans (N2), lecture interactive familiale\n"
        "- **Leçon principale :** AUT.AFF.003 — s'habiller / dire ce qu'on veut "
        "(vécue, non dite)\n"
        "- **Personnages :** Nina, papa, maman\n"
        "- **Structure conservée :** 86 nœuds, trois choix à trois options, "
        "27 chemins et 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Dans la cuisine, une feuille de pluie colle à la vitre. Sur le manteau "
        "jaune, un éclat de bouton tient un bout de jour. Nina veut le mettre "
        "toute seule pour aller tamponner la flaque du jardin avant que le soleil "
        "la boive. Elle tire trop vite : le manteau tombe. Matin, sieste ou soir "
        "changent le tissu (manche à l'envers, bras coincés, tissu collé). "
        "Cuisine, jardin ou chambre changent l'obstacle. Ballon, seau bleu ou "
        "doudou changent la ruse. Nina refuse de foncer, suit l'éclat, ferme le "
        "jaune. Chaque fin paie l'éclat de bouton.\n\n"
        "## Améliorations appliquées\n\n"
        "- Monde (feuille collée, orange, laine mouillée, flaque-assiette) avant l'action.\n"
        "- Désir immédiat : mettre le jaune seule, avant que la flaque sèche.\n"
        "- Première idée échoue : tir trop fort, crochet, manche à l'envers.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor.\n"
        "- Indice unique nommé à l'ouverture, payé aux 27 fins.\n"
        "- Un merci vécu (ouverture), pas un refrain.\n"
        "- Gabarit buée/soupe/tout doux/Inès jeté. Pas d'apply.\n\n"
        "## Direction vocale\n\n"
        "TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending) : "
        "rate, pitch, volume, pauses, text_ssml, text_xai_tags, notes d'arc. "
        "slow réservé aux choix, à l'indice et aux fins.\n\n"
        "## Contrôles\n\n"
        "- 86 chunks\n"
        "- 27 chemins\n"
        "- 27 fins textuellement distinctes, dernière image unique, éclat de bouton payé\n"
        f"- {min(lengths)} à {max(lengths)} mots par chemin, moyenne {sum(lengths)//len(lengths)}\n"
        "- `text` et `script` synchronisés\n"
        "- `text_ssml` et `text_xai_tags` enrichis\n"
        "- check() N2 OK\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(
        f"OK {SID} {sum(words(c['text']) for c in chunks)} mots  "
        f"chemins {min(lengths)}-{max(lengths)} moy {sum(lengths)//len(lengths)}"
    )


if __name__ == "__main__":
    main()
