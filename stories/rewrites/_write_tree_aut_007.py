#!/usr/bin/env python3
"""TREE-AUT-007 — Le volet de Victorina (F-NAR-019, N3, AUT.ROU.001, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-007"
N3 = LIMITS["N3"]
TITLE = "Le volet de Victorina"
TICS = re.compile(
    r"\b(tout doux|tout calme|encore|déjà|deja|une étape après l'autre)\b",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="volet",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=l_oiseau_de_papier_attend_la_rue; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="volet",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qui_s_est_passé; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="volet",
        note="arc=confirmation; intention=relancer; emotion=élan; intensite=1; destinataire=enfant; sous_texte=on_peut_continuer_sans_tirer_trop_vite; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_veut_tout_en_même_temps; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=le_premier_geste_rate; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="volet",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=une_chose_finie_ouvre_le_bois; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="volet",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_volet_et_le_pain_se_rejoignent; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
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
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        out.append(f"{role}|{ph}")
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
        f"destinataire=enfant; sous_texte=le_volet_a_ouvert_sur_la_rue; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


OPENING = vet(
    [
        "narrateur|Sur le bois jaune, une fente de soleil tremble.",
        "narrateur|Le volet de la petite maison sent la nuit.",
        "narrateur|Une odeur de pain chaud grimpe l'escalier.",
        "narrateur|Victorina vit là, avec papa et maman.",
        "narrateur|Dehors, un moineau picore la gouttière.",
        "papa|Tu as entendu le moineau, Victorina ?",
        "enfant-f|Il tape mon volet !",
        "maman|Ton oiseau de papier dort entre les lattes.",
        "narrateur|Hier soir, elle a glissé l'oiseau dans le volet.",
        "narrateur|Il a dormi contre les étoiles, tout plat.",
        "narrateur|En ce moment, Victorina saute du lit.",
        "enfant-f|J'ouvre, il veut la rue !",
        "narrateur|Elle tire la poignée, trop vite, trop fort.",
        "narrateur|Le bois gonflé par la nuit fait clac, et reste.",
        "narrateur|Ses pieds nus trouvent le parquet froid.",
        "enfant-f|Il ne veut pas !",
        "papa|Le bois a bu la nuit, il est lourd.",
        "maman|Tes mains sont petites, et tu grelottes.",
        "narrateur|Victorina souffle, les épaules basses.",
        "enfant-f|Je veux mon oiseau, et le pain.",
        "papa|Merci d'avoir dit ce que tu veux.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|Le volet attend, coincé, trop lourd pour ses bras.",
        "narrateur|La chambre, la salle d'eau, ou la cuisine.",
        "maman|Où vas-tu d'abord, Victorina ?",
    ]
)

T1 = {
    1: dict(
        lab="la chambre",
        ans="volet",
        acc="volet | le volet | le bois | la poignée | il n'ouvre pas",
        retry="Le bois est resté fermé. Qu'est-ce qui n'a pas ouvert ?",
        ok="Oui, c'est le volet.",
        sons="volet,tissu",
        emp="volet",
        passage=vet(
            [
                "narrateur|Victorina reste près du volet, dans la chambre.",
                "narrateur|Un tabouret dort sous un tas de linge.",
                "enfant-f|Je grimpe, et je tire plus fort !",
                "narrateur|Elle tire sans le tabouret, trop petite.",
                "narrateur|La poignée lui échappe, froide, trop haute.",
                "papa|Tu grelottes, tes dents claquent.",
                "maman|Le linge de la chaise est à toi.",
                "narrateur|Victorina veut le volet et le linge ensemble.",
                "narrateur|Elle attrape une manche, et tire la poignée.",
                "narrateur|La manche tombe, et le volet reste fermé.",
                "enfant-f|Rien ne marche !",
                "papa|Tes mains nues glissent, trop froides.",
            ]
        ),
        question=vet(
            [
                "narrateur|Victorina a tiré trop vite, trop fort.",
                "maman|Qu'est-ce qui n'a pas ouvert ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Le volet reste coincé, une fente de soleil au bord.",
                "enfant-f|Je m'habille, après je pousse.",
                "maman|Bravo, Victorina.",
                "papa|Le tabouret t'attend, sous le linge.",
                "enfant-f|Mes pieds d'abord, sur le tapis.",
                "narrateur|Elle pose les deux pieds, sans tirer.",
            ]
        ),
    ),
    2: dict(
        lab="la salle d'eau",
        ans="mains",
        acc="mains | ses mains | les mains | elle a glissé | glissé",
        retry="Ses mains ont glissé. Qu'est-ce qui a glissé ?",
        ok="Oui, ce sont ses mains.",
        sons="eau,savon",
        emp="savon",
        passage=vet(
            [
                "narrateur|Victorina court vers la salle d'eau, les mains moites.",
                "narrateur|La poignée du volet a glissé, trop humide.",
                "enfant-f|Je me lave, après je tire !",
                "narrateur|L'eau froide pique ses doigts, trop vite ouverts.",
                "narrateur|Le savon lui fuit entre les paumes.",
                "maman|Le savon n'aime pas la course.",
                "papa|Avec des mains mouillées, la poignée glisse.",
                "narrateur|Elle veut se rincer et courir en même temps.",
                "narrateur|Une goutte file sur le carrelage, et elle glisse.",
                "enfant-f|Aïe, mes pieds !",
                "maman|On sèche, puis on revient au bois.",
                "narrateur|Le miroir garde une buée ronde, comme un œil.",
            ]
        ),
        question=vet(
            [
                "narrateur|La poignée a glissé sous ses doigts.",
                "papa|Qu'est-ce qui a glissé, sur la poignée ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Ses mains sentent le savon, plus sèches.",
                "enfant-f|Maintenant, je peux tenir.",
                "papa|Tes pieds aussi, le carrelage est froid.",
                "maman|Tu reviens au volet, quand tu es prête.",
                "enfant-f|Oui, maman.",
                "narrateur|Une goutte sèche sur le rebord, sans bruit.",
            ]
        ),
    ),
    3: dict(
        lab="la cuisine",
        ans="pain",
        acc="pain | le pain | une odeur de pain | odeur | le four",
        retry="L'odeur du pain grimpe. Quelle odeur ?",
        ok="Oui, c'est le pain.",
        sons="pain,couverts",
        emp="pain",
        passage=vet(
            [
                "narrateur|Victorina descend vers la cuisine, pieds nus.",
                "narrateur|L'odeur du pain chaud lui tape le ventre.",
                "enfant-f|Le pain, et le volet, maintenant !",
                "narrateur|Les carreaux froids piquent ses talons.",
                "papa|J'ai une goutte d'huile, pour le bois.",
                "narrateur|Elle tend les deux mains, trop vides, trop pressées.",
                "narrateur|L'huile vacille, une goutte tombe près du bol.",
                "maman|Tu grelottes, on ne peut pas porter ça.",
                "enfant-f|Je veux tout, là, tout de suite !",
                "papa|Le pain reste au four, et le bois aussi.",
                "narrateur|Victorina serre les poings, le ventre vide.",
                "maman|Tes pieds d'abord, les carreaux piquent.",
            ]
        ),
        question=vet(
            [
                "narrateur|L'odeur chaude a suivi Victorina, jusque là.",
                "maman|Quelle odeur grimpe l'escalier ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Le pain dore, sous le linge du four.",
                "enfant-f|Je reviens m'habiller, pour l'huile.",
                "papa|L'huile attend, près du bol.",
                "maman|Tu pourras pousser, avec des mains chaudes.",
                "enfant-f|Oui, papa.",
                "narrateur|Une miette dorée brille, sur la table.",
            ]
        ),
    ),
}


T2_CHOICE = {
    1: vet(
        [
            "narrateur|Le linge de la chaise attend, un peu froid.",
            "narrateur|Le t-shirt, les chaussettes, ou le gilet.",
            "papa|Tu mets quoi, pour pousser le bois ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Ses bras et ses pieds sont froids, trop nus.",
            "narrateur|Le t-shirt, les chaussettes, ou le gilet.",
            "maman|Tu mets quoi, avant de revenir au volet ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Les carreaux piquent, et l'huile attend.",
            "narrateur|Le t-shirt, les chaussettes, ou le gilet.",
            "papa|Tu mets quoi, pour porter l'huile ?",
        ]
    ),
}


def t2_scene(a: int, b: int) -> list[str]:
    hip = {
        1: "Dans la chambre, le volet reste coincé, trop lourd.",
        2: "Ses mains sentent le savon, plus sèches, plus prêtes.",
        3: "L'odeur du pain suit ses pas, jusque sous le bois.",
    }[a]
    if b == 1:
        body = {
            1: [
                f"narrateur|{hip}",
                "narrateur|Victorina prend le t-shirt, le coton froid.",
                "enfant-f|Je le mets, et je tire !",
                "narrateur|Elle enfile trop vite, une manche se coince.",
                "narrateur|Son épaule reste coincée, comme le volet.",
                "papa|Sors le bras, sans tirer le bois.",
                "maman|Le coton d'abord, ensuite la poignée.",
                "enfant-f|La manche me tient !",
                "narrateur|Elle ralentit, et le bras passe, tout net.",
                "narrateur|Le t-shirt sent le soleil, contre sa peau.",
                "papa|Tu peux pousser, avec l'épaule.",
                "enfant-f|J'ai le coton, et après ?",
            ],
            2: [
                f"narrateur|{hip}",
                "narrateur|Victorina prend le t-shirt, près du lavabo.",
                "enfant-f|Je le mets, et je cours au bois !",
                "narrateur|Une goutte mouille le coton, trop vite enfilé.",
                "narrateur|La manche colle, froide, contre son bras.",
                "maman|Sèche, puis passe la tête.",
                "papa|Le coton mouillé glisse, comme la poignée.",
                "enfant-f|Il me tient le coude !",
                "narrateur|Elle s'arrête, et la goutte sèche sur le rebord.",
                "narrateur|Le t-shirt passe, plus lent, plus chaud.",
                "maman|Tes épaules sont prêtes, pour le bois.",
                "enfant-f|J'ai le coton, et après ?",
            ],
            3: [
                f"narrateur|{hip}",
                "narrateur|Victorina prend le t-shirt, près du four.",
                "enfant-f|Je le mets, et je prends l'huile !",
                "narrateur|Elle enfile trop vite, le coton se tord.",
                "narrateur|Une manche frôle le bol, trop près de l'huile.",
                "papa|Le bras d'abord, le bol ensuite.",
                "maman|Le pain dore, et toi, tu grelottes moins.",
                "enfant-f|La manche a failli tout tacher !",
                "narrateur|Elle ralentit, et le t-shirt tombe droit.",
                "narrateur|Le coton garde un peu de chaleur du four.",
                "papa|Avec ça, tu peux porter l'huile.",
                "enfant-f|J'ai le coton, et après ?",
            ],
        }[a]
    elif b == 2:
        body = {
            1: [
                f"narrateur|{hip}",
                "narrateur|Victorina prend les chaussettes, un peu froides.",
                "enfant-f|Je les mets, et je grimpe !",
                "narrateur|Elle enfile une seule, et court au tabouret.",
                "narrateur|Le pied nu glisse sur le parquet, trop lisse.",
                "papa|Les deux pieds, sinon le tabouret part.",
                "maman|Une chaussette, puis l'autre, sans sauter.",
                "enfant-f|J'ai failli tomber !",
                "narrateur|Elle s'assoit, et la deuxième chaussette passe.",
                "narrateur|Le parquet n'attrape plus ses talons.",
                "papa|Tu peux grimper, sans glisser.",
                "enfant-f|J'ai les deux, et après ?",
            ],
            2: [
                f"narrateur|{hip}",
                "narrateur|Victorina prend les chaussettes, près de l'eau.",
                "enfant-f|Je les mets, et je repars !",
                "narrateur|Une chaussette touche une goutte, et colle.",
                "narrateur|Elle saute vers la porte, un pied trop lourd.",
                "maman|On sèche le pied, puis on enfile.",
                "papa|Un pied mouillé, le tabouret glisse.",
                "enfant-f|Elle me tient les orteils !",
                "narrateur|Elle s'arrête, et la goutte sèche sur le carreau.",
                "narrateur|Les deux chaussettes passent, l'une, puis l'autre.",
                "maman|Tes pieds sont prêts, pour le bois.",
                "enfant-f|J'ai les deux, et après ?",
            ],
            3: [
                f"narrateur|{hip}",
                "narrateur|Victorina prend les chaussettes, sous la table.",
                "enfant-f|Je les mets, et je prends l'huile !",
                "narrateur|Elle enfile trop vite, un talon reste plié.",
                "narrateur|Sur les carreaux, le talon plié la fait pencher.",
                "papa|Le talon d'abord, l'huile ensuite.",
                "maman|Les carreaux piquent moins, avec ça.",
                "enfant-f|Mon talon me chatouille !",
                "narrateur|Elle s'assoit, et le talon se déplie, net.",
                "narrateur|Les deux chaussettes tiennent, chaudes, sous la table.",
                "papa|Avec ça, tu peux porter l'huile.",
                "enfant-f|J'ai les deux, et après ?",
            ],
        }[a]
    else:
        body = {
            1: [
                f"narrateur|{hip}",
                "narrateur|Victorina prend le gilet, la laine un peu rêche.",
                "enfant-f|Je le mets, et je pousse !",
                "narrateur|Elle enfile trop vite, un bouton saute.",
                "narrateur|La poignée froide lui pique la paume, trop nue.",
                "papa|Le bouton d'abord, ensuite le bois.",
                "maman|La laine tiédit tes épaules, et tes mains.",
                "enfant-f|Le bouton m'a échappé !",
                "narrateur|Elle le retrouve, sous la chaise, sans courir.",
                "narrateur|Le gilet ferme, et la poche attend, vide.",
                "papa|Tu peux pousser, l'épaule au chaud.",
                "enfant-f|J'ai la laine, et après ?",
            ],
            2: [
                f"narrateur|{hip}",
                "narrateur|Victorina prend le gilet, près de la buée.",
                "enfant-f|Je le mets, et je repars !",
                "narrateur|La laine accroche une goutte, trop pressée.",
                "narrateur|Un bouton reste ouvert, face au miroir.",
                "maman|Le bouton d'abord, la poignée ensuite.",
                "papa|La laine mouillée pique, comme le savon.",
                "enfant-f|Il me tient le ventre, tout ouvert !",
                "narrateur|Elle s'arrête, et le bouton rentre, net.",
                "narrateur|Le gilet sent le savon, et un peu de laine.",
                "maman|Tes épaules sont prêtes, pour le bois.",
                "enfant-f|J'ai la laine, et après ?",
            ],
            3: [
                f"narrateur|{hip}",
                "narrateur|Victorina prend le gilet, près du four tiède.",
                "enfant-f|Je le mets, et je prends l'huile !",
                "narrateur|Elle enfile trop vite, la poche se retourne.",
                "narrateur|L'huile frôle la laine, trop près du bol.",
                "papa|La poche d'abord, le bol ensuite.",
                "maman|La laine tiédit, comme le pain.",
                "enfant-f|La poche voulait tout avaler !",
                "narrateur|Elle la remet, sans toucher l'huile.",
                "narrateur|Le gilet ferme, et une poche attend, nette.",
                "papa|Avec ça, tu peux porter l'huile.",
                "enfant-f|J'ai la laine, et après ?",
            ],
        }[a]
    # "tout net" / "tout ouvert" / "tout de suite" — "tout ouvert" might be ok.
    # "tout de suite" is in T1 cuisine enfant line already... wait I have
    # "Je veux tout, là, tout de suite !" in T1=3. "tout de suite" is not in TICS.
    # "tout ouvert" in gilet salle d'eau: "Il me tient le ventre, tout ouvert !"
    # TICS is tout doux / tout calme. OK.
    # "tout net" in t-shirt chambre: "Le bras passe, tout net." OK.
    return vet(body)


T3_CHOICE = {
    1: vet(
        [
            "narrateur|Le coton tient, et le volet, lui, attend.",
            "narrateur|Le sac, le manteau, ou le doudou.",
            "maman|Tu prends quoi, pour finir près du bois ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Les pieds tiennent, et le volet, lui, attend.",
            "narrateur|Le sac, le manteau, ou le doudou.",
            "papa|Tu prends quoi, pour finir près du bois ?",
        ]
    ),
    3: vet(
        [
            "narrateur|La laine tient, et le volet, lui, attend.",
            "narrateur|Le sac, le manteau, ou le doudou.",
            "maman|Tu prends quoi, pour finir près du bois ?",
        ]
    ),
}


# 27 résolutions : lieu × vêtement × objet, climax et geste uniques.
RES = {
    (1, 1, 1): vet(
        [
            "enfant-f|Le sac, pour l'oiseau.",
            "narrateur|Victorina pose le sac sur le tabouret, comme une marche.",
            "narrateur|Le t-shirt serre son épaule, contre le bois.",
            "narrateur|Elle pousse sans tirer, le sac sous le pied.",
            "narrateur|Le volet grince, puis s'ouvre d'un cran.",
            "narrateur|L'oiseau de papier glisse dans le sac, tout plat.",
            "papa|Tu as poussé, sans t'énerver.",
            "enfant-f|Il a la rue, dans mon sac !",
            "maman|Le bois a compris, cette fois.",
            "narrateur|Une fente de soleil tombe dans le sac ouvert.",
        ]
    ),
    (1, 1, 2): vet(
        [
            "enfant-f|Le manteau, j'ai froid à la fente.",
            "narrateur|Victorina enfile le manteau par-dessus le t-shirt.",
            "narrateur|L'épaule ouatée pousse le bois, sans secouer.",
            "narrateur|Le volet cède, un peu, puis plus large.",
            "narrateur|L'air de la rue entre, froid, dans les manches.",
            "narrateur|L'oiseau de papier tremble, libre, sur le rebord.",
            "papa|Tu as poussé au chaud, cette fois.",
            "enfant-f|Je peux rester, près de la rue !",
            "maman|Le manteau a tenu le vent.",
            "narrateur|Un carré de soleil s'assoit sur le manteau.",
        ]
    ),
    (1, 1, 3): vet(
        [
            "enfant-f|Le doudou, il veut voir aussi.",
            "narrateur|Victorina pose le doudou sur le rebord, face au bois.",
            "narrateur|Le t-shirt lui laisse les deux mains libres.",
            "narrateur|Elle pousse, et le doudou garde la fente, sans tomber.",
            "narrateur|Le volet s'ouvre, et l'oiseau de papier se lève.",
            "narrateur|Le doudou regarde la rue, le menton sur la latte.",
            "papa|Tes deux mains ont suffi.",
            "enfant-f|Il a vu le moineau !",
            "maman|Le doudou a tenu sa place.",
            "narrateur|Une plume de papier frôle le nez du doudou.",
        ]
    ),
    (1, 2, 1): vet(
        [
            "enfant-f|Le sac, je grimpe avec.",
            "narrateur|Victorina grimpe, les chaussettes collées au bois du tabouret.",
            "narrateur|Elle pose le sac contre la poignée, comme un coussin.",
            "narrateur|La paume pousse le sac, le sac pousse le bois, sans clac.",
            "narrateur|Le volet s'ouvre, et l'oiseau glisse dans le sac.",
            "papa|Tes pieds n'ont pas glissé.",
            "enfant-f|Le sac a reçu la rue !",
            "maman|Le tabouret est resté droit.",
            "narrateur|Une chaussette garde un peu de parquet, sous le sac.",
        ]
    ),
    (1, 2, 2): vet(
        [
            "enfant-f|Le manteau, pour la rue froide.",
            "narrateur|Victorina grimpe en chaussettes, le manteau sur les épaules.",
            "narrateur|Elle pousse le volet du coude, le tissu épais.",
            "narrateur|Le bois cède, et l'air entre, sans la faire grelotter.",
            "narrateur|L'oiseau de papier s'envole d'un souffle, puis se pose.",
            "papa|Tes pieds tenaient, et tes épaules aussi.",
            "enfant-f|Je peux descendre, après, chercher le pain.",
            "maman|Le manteau a fermé le froid.",
            "narrateur|Les chaussettes, près du manteau, sentent le vent.",
        ]
    ),
    (1, 2, 3): vet(
        [
            "enfant-f|Le doudou, sur le tabouret.",
            "narrateur|Victorina pose le doudou, coussin sur le tabouret.",
            "narrateur|Ses chaussettes tiennent, et elle pousse le bois, sans sauter.",
            "narrateur|Le volet s'ouvre, et le doudou ne tombe pas.",
            "narrateur|L'oiseau de papier atterrit près du doudou, tout plat.",
            "papa|Tu as grimpé, sans te presser.",
            "enfant-f|Ils voient le moineau, tous les deux !",
            "maman|Le tabouret n'a pas bougé.",
            "narrateur|Une chaussette, sous le doudou, garde le bois tiède.",
        ]
    ),
    (1, 3, 1): vet(
        [
            "enfant-f|Le sac, dans la poche du gilet.",
            "narrateur|Victorina glisse le sac vide contre la poignée.",
            "narrateur|Le gilet tiédit ses mains, et elle pousse, lentement.",
            "narrateur|Le volet s'ouvre, et l'oiseau tombe dans le sac.",
            "narrateur|Elle range le sac dans la poche, l'oiseau à l'abri.",
            "papa|Tes mains n'ont plus glissé.",
            "enfant-f|Il est dans ma poche, il a vu la rue !",
            "maman|La laine a tenu le bois.",
            "narrateur|Une plume reste collée à la poche du gilet.",
        ]
    ),
    (1, 3, 2): vet(
        [
            "enfant-f|Le manteau, par-dessus le gilet.",
            "narrateur|Victorina superpose le manteau, deux chaleurs, une poussée.",
            "narrateur|L'épaule double pousse le volet, sans claquer.",
            "narrateur|Le bois s'ouvre, et l'oiseau de papier se redresse.",
            "narrateur|Elle reste là, au chaud, face à la gouttière.",
            "papa|Deux couches, et le bois a cédé.",
            "enfant-f|Je ne grelotte plus !",
            "maman|Le manteau a dit bonjour au gilet.",
            "narrateur|Le manteau et le gilet se touchent, devant le vide.",
        ]
    ),
    (1, 3, 3): vet(
        [
            "enfant-f|Le doudou, dans le gilet.",
            "narrateur|Victorina loge le doudou dans la poche du gilet.",
            "narrateur|Ses mains libres poussent le volet, la laine au chaud.",
            "narrateur|Le bois s'ouvre, et le doudou sort le nez, vers la rue.",
            "narrateur|L'oiseau de papier vient se poser contre la poche.",
            "papa|La poche a gardé ta place.",
            "enfant-f|Ils sont deux, à voir le moineau !",
            "maman|Le doudou s'est endormi au chaud.",
            "narrateur|Le doudou s'endort dans le gilet, le volet ouvert.",
        ]
    ),
    (2, 1, 1): vet(
        [
            "enfant-f|Le sac, mes mains sont sèches.",
            "narrateur|Victorina revient, le t-shirt sec, le sac à la main.",
            "narrateur|Elle essuie la poignée avec le fond du sac.",
            "narrateur|Puis elle pousse, et le volet s'ouvre, sans glisser.",
            "narrateur|L'oiseau de papier tombe dans le sac, une odeur de savon.",
            "papa|Tes mains ont tenu, cette fois.",
            "enfant-f|Le sac a pris le vent, et le savon !",
            "maman|La poignée n'a plus fui.",
            "narrateur|Dans le sac, l'oiseau sent le savon, et le vent.",
        ]
    ),
    (2, 1, 2): vet(
        [
            "enfant-f|Le manteau, l'eau m'a refroidie.",
            "narrateur|Victorina enfile le manteau sur le t-shirt, près du lavabo.",
            "narrateur|Une goutte sèche sur le tissu, puis plus rien.",
            "narrateur|Elle pousse le volet du poignet, le manteau entre elle et le froid.",
            "narrateur|Le bois s'ouvre, et l'oiseau de papier se lève.",
            "papa|Tu es sèche, et le bois aussi.",
            "enfant-f|Je peux rester, sans grelotter !",
            "maman|Le manteau a bu la dernière goutte.",
            "narrateur|Le manteau sèche une goutte, près de la poignée.",
        ]
    ),
    (2, 1, 3): vet(
        [
            "enfant-f|Le doudou, il n'aime pas l'eau.",
            "narrateur|Victorina tient le doudou loin du lavabo, le t-shirt sec.",
            "narrateur|Elle pousse le volet d'une main, le doudou de l'autre.",
            "narrateur|Le bois s'ouvre, et une buée du miroir fond, plus loin.",
            "narrateur|L'oiseau de papier vient au doudou, tout plat.",
            "papa|Tes mains sèches ont suffi.",
            "enfant-f|Il n'a pas eu d'eau, lui !",
            "maman|Le doudou a les joues sèches.",
            "narrateur|Le doudou a les joues humides de joie, face à la rue.",
        ]
    ),
    (2, 2, 1): vet(
        [
            "enfant-f|Le sac, mes pieds sont secs.",
            "narrateur|Victorina revient en chaussettes, le sac comme un coussin.",
            "narrateur|Elle pose le sac sous la poignée, sans glisser.",
            "narrateur|Le volet s'ouvre, et l'oiseau glisse dans le sac.",
            "narrateur|Une chaussette laisse une trace ronde, sur le parquet.",
            "papa|Tes pieds n'ont plus sauté.",
            "enfant-f|Le sac a la rue, et mes pieds aussi !",
            "maman|Le carrelage n'a plus gagné.",
            "narrateur|Une chaussette laisse une trace ronde, sous le sac.",
        ]
    ),
    (2, 2, 2): vet(
        [
            "enfant-f|Le manteau, pour ne plus glisser.",
            "narrateur|Victorina enfile le manteau, les chaussettes sèches.",
            "narrateur|Elle pousse le volet, un pied bien à plat.",
            "narrateur|Le bois s'ouvre, et l'air sent le savon, et la rue.",
            "narrateur|L'oiseau de papier se pose sur la manche.",
            "papa|Tu es restée droite, cette fois.",
            "enfant-f|Je n'ai plus sauté !",
            "maman|Le manteau sent le savon, un peu.",
            "narrateur|Le manteau sent le savon, et la rue entre.",
        ]
    ),
    (2, 2, 3): vet(
        [
            "enfant-f|Le doudou, loin des gouttes.",
            "narrateur|Victorina pose le doudou sur le rebord, loin du lavabo.",
            "narrateur|Ses chaussettes tiennent, et elle pousse le bois, sans sauter.",
            "narrateur|Le volet s'ouvre, et le doudou voit le moineau.",
            "narrateur|L'oiseau de papier s'assoit entre ses pattes.",
            "papa|Tes pieds sont restés sages.",
            "enfant-f|Il a les pieds au chaud, lui aussi !",
            "maman|Le doudou n'a pas eu d'eau.",
            "narrateur|Le doudou, les pieds au chaud, voit le moineau.",
        ]
    ),
    (2, 3, 1): vet(
        [
            "enfant-f|Le sac, dans le gilet, loin de l'eau.",
            "narrateur|Victorina glisse le sac dans la poche du gilet.",
            "narrateur|La laine sent le savon, et elle pousse le volet, lentement.",
            "narrateur|Le bois s'ouvre, l'oiseau tombe dans la poche, puis dans le sac.",
            "papa|Tes mains de laine n'ont pas glissé.",
            "enfant-f|Il est au sec, dans ma poche !",
            "maman|Le savon et la laine se sont dit bonjour.",
            "narrateur|La poche du gilet sent le savon, près du sac.",
        ]
    ),
    (2, 3, 2): vet(
        [
            "enfant-f|Le manteau, par-dessus le gilet mouillé.",
            "narrateur|Victorina boutonne le manteau sur le gilet, près du miroir.",
            "narrateur|La buée recule, et elle pousse le volet, deux tissus.",
            "narrateur|Le bois s'ouvre, et l'oiseau de papier se redresse.",
            "papa|Le froid de l'eau s'en va.",
            "enfant-f|Je suis un nuage chaud !",
            "maman|Le manteau a boutonné le gilet.",
            "narrateur|Le manteau boutonne le gilet, face au soleil.",
        ]
    ),
    (2, 3, 3): vet(
        [
            "enfant-f|Le doudou, sous le gilet, au sec.",
            "narrateur|Victorina abrite le doudou sous le gilet, loin des gouttes.",
            "narrateur|Elle pousse le volet, et le bois s'ouvre, net.",
            "narrateur|L'oiseau de papier se glisse près du doudou, au chaud.",
            "papa|Ils sont deux, au sec.",
            "enfant-f|Personne n'a d'eau, cette fois !",
            "maman|Le gilet a fait un toit.",
            "narrateur|Le doudou s'abrite dans le gilet, le bois ouvert.",
        ]
    ),
    (3, 1, 1): vet(
        [
            "enfant-f|Le sac, pour l'huile et l'oiseau.",
            "narrateur|Victorina met la fiole d'huile dans le sac, le t-shirt chaud.",
            "narrateur|Papa pose une goutte sur le bois, près du bord.",
            "narrateur|Elle pousse, et le volet s'ouvre, sans clac, tout huilé.",
            "narrateur|L'oiseau de papier glisse dans le sac, près d'une miette.",
            "papa|L'huile a parlé au bois.",
            "enfant-f|Le sac a le pain, et la rue !",
            "maman|La goutte n'a plus tremblé.",
            "narrateur|Le sac, près du bol, garde l'oiseau et une miette.",
        ]
    ),
    (3, 1, 2): vet(
        [
            "enfant-f|Le manteau, je descends au pain.",
            "narrateur|Victorina enfile le manteau sur le t-shirt, près du four.",
            "narrateur|Papa huile le bois, et elle pousse, l'épaule ouatée.",
            "narrateur|Le volet s'ouvre, et l'odeur du pain croise celle de la rue.",
            "narrateur|L'oiseau de papier se pose sur le manteau, une miette au bec.",
            "papa|Tu pourras descendre, au chaud.",
            "enfant-f|Le pain, et la rue, ensemble !",
            "maman|Le manteau a pris un fil de soleil.",
            "narrateur|Le manteau, près du pain, tient un fil de soleil.",
        ]
    ),
    (3, 1, 3): vet(
        [
            "enfant-f|Le doudou, il veut le four, et la rue.",
            "narrateur|Victorina tient le doudou, le t-shirt chaud du four.",
            "narrateur|Papa huile, et elle pousse le volet, le doudou contre elle.",
            "narrateur|Le bois s'ouvre, et le doudou voit le moineau, et le pain.",
            "narrateur|L'oiseau de papier s'assoit sur son ventre.",
            "papa|Il a deux odeurs, lui.",
            "enfant-f|Le four, et la gouttière !",
            "maman|Le doudou a une miette sur le nez.",
            "narrateur|Le doudou, près du four, regarde le volet ouvert.",
        ]
    ),
    (3, 2, 1): vet(
        [
            "enfant-f|Le sac, mes pieds ne piquent plus.",
            "narrateur|Victorina, en chaussettes, pose le sac près du bol.",
            "narrateur|Papa huile, et elle pousse le volet, les pieds bien à plat.",
            "narrateur|Le bois s'ouvre, l'oiseau glisse dans le sac, une miette suit.",
            "papa|Les carreaux n'ont plus piqué.",
            "enfant-f|Mes pieds, et le sac, et la rue !",
            "maman|Le pain dore, le bois aussi.",
            "narrateur|Les chaussettes, sous la table, sentent le pain chaud.",
        ]
    ),
    (3, 2, 2): vet(
        [
            "enfant-f|Le manteau, je veux le pain dehors.",
            "narrateur|Victorina enfile le manteau, les chaussettes sous les carreaux.",
            "narrateur|Papa huile, et elle pousse, puis regarde l'escalier.",
            "narrateur|Le volet s'ouvre, et l'odeur du pain part vers la rue.",
            "narrateur|L'oiseau de papier s'envole d'un cran, puis revient.",
            "papa|Tu pourras descendre, sans piquer tes pieds.",
            "enfant-f|Le pain va voir le moineau !",
            "maman|Le manteau gardera le vent, en bas.",
            "narrateur|Le manteau, sur la chaise de cuisine, garde le vent.",
        ]
    ),
    (3, 2, 3): vet(
        [
            "enfant-f|Le doudou, sous la table, puis le bois.",
            "narrateur|Victorina ramasse le doudou sous la table, en chaussettes.",
            "narrateur|Papa huile, et elle pousse le volet, le doudou sous le bras.",
            "narrateur|Le bois s'ouvre, et une miette tombe sur le nez du doudou.",
            "papa|Il a le pain, et la rue.",
            "enfant-f|Il a une miette, il est content !",
            "maman|Tes pieds n'ont plus piqué.",
            "narrateur|Le doudou a une miette sur le nez, et la rue.",
        ]
    ),
    (3, 3, 1): vet(
        [
            "enfant-f|Le sac, dans le gilet, près du four.",
            "narrateur|Victorina glisse le sac dans la poche du gilet, une miette avec.",
            "narrateur|Papa huile, et elle pousse le volet, la laine tiède.",
            "narrateur|Le bois s'ouvre, et l'oiseau rejoint la miette, dans le sac.",
            "papa|La poche a fait le voyage.",
            "enfant-f|Il a du pain, et du vent !",
            "maman|Le gilet sent le four.",
            "narrateur|La poche du gilet tient une miette, et l'oiseau.",
        ]
    ),
    (3, 3, 2): vet(
        [
            "enfant-f|Le manteau, par-dessus le gilet du four.",
            "narrateur|Victorina superpose le manteau, le gilet chaud du four.",
            "narrateur|Papa huile, et elle pousse, deux chaleurs contre le bois.",
            "narrateur|Le volet s'ouvre, et l'odeur du pain sort, vers le moineau.",
            "papa|Le four a prêté sa chaleur.",
            "enfant-f|Je suis le pain, moi aussi !",
            "maman|Le manteau a pris le gilet sous le bras.",
            "narrateur|Le manteau et le gilet, près du four, sentent le pain.",
        ]
    ),
    (3, 3, 3): vet(
        [
            "enfant-f|Le doudou, dans le gilet, près du pain.",
            "narrateur|Victorina loge le doudou dans le gilet, une odeur de four.",
            "narrateur|Papa huile, et elle pousse le volet, sans se presser.",
            "narrateur|Le bois s'ouvre, et le doudou écoute le moineau, tout loin.",
            "papa|Il a le four, et la gouttière.",
            "enfant-f|Il écoute, sans crier !",
            "maman|Le gilet a bercé le doudou.",
            "narrateur|Le doudou, dans le gilet, écoute le moineau, loin.",
        ]
    ),
}


def ending(a: int, b: int, c: int) -> list[str]:
    recap = {
        (1, 1, 1): "J'ai mis le t-shirt, le sac, et le volet a ouvert.",
        (1, 1, 2): "J'ai mis le t-shirt, le manteau, et le vent est entré.",
        (1, 1, 3): "J'ai mis le t-shirt, le doudou a vu la rue.",
        (1, 2, 1): "J'ai mis les chaussettes, le sac, et j'ai grimpé.",
        (1, 2, 2): "J'ai mis les chaussettes, le manteau, sans glisser.",
        (1, 2, 3): "J'ai mis les chaussettes, le doudou sur le tabouret.",
        (1, 3, 1): "J'ai mis le gilet, le sac dans la poche, et ça a ouvert.",
        (1, 3, 2): "J'ai mis le gilet, le manteau, deux chaleurs.",
        (1, 3, 3): "J'ai mis le gilet, le doudou dans la poche.",
        (2, 1, 1): "J'ai séché mes mains, le t-shirt, le sac a pris l'oiseau.",
        (2, 1, 2): "J'ai séché, le t-shirt, le manteau a bu la goutte.",
        (2, 1, 3): "J'ai séché, le t-shirt, le doudou n'a pas eu d'eau.",
        (2, 2, 1): "J'ai mis les chaussettes sèches, le sac sous la poignée.",
        (2, 2, 2): "J'ai mis les chaussettes, le manteau, sans sauter.",
        (2, 2, 3): "J'ai mis les chaussettes, le doudou loin des gouttes.",
        (2, 3, 1): "J'ai mis le gilet, le sac au sec, loin de l'eau.",
        (2, 3, 2): "J'ai mis le gilet, le manteau a boutonné.",
        (2, 3, 3): "J'ai mis le gilet, le doudou sous le toit de laine.",
        (3, 1, 1): "J'ai mis le t-shirt, le sac a l'huile et l'oiseau.",
        (3, 1, 2): "J'ai mis le t-shirt, le manteau, et le pain a vu la rue.",
        (3, 1, 3): "J'ai mis le t-shirt, le doudou a le four et la rue.",
        (3, 2, 1): "J'ai mis les chaussettes, le sac près du bol.",
        (3, 2, 2): "J'ai mis les chaussettes, le manteau, pour le pain dehors.",
        (3, 2, 3): "J'ai mis les chaussettes, le doudou a une miette.",
        (3, 3, 1): "J'ai mis le gilet, le sac a une miette et l'oiseau.",
        (3, 3, 2): "J'ai mis le gilet, le manteau, on sentait le four.",
        (3, 3, 3): "J'ai mis le gilet, le doudou écoute le moineau.",
    }[(a, b, c)]
    invite = {
        1: "Raconte, Victorina, on t'écoute.",
        2: "Dis-nous, le pain est prêt.",
        3: "À toi, on a fini nos phrases.",
    }[a]
    keepsake = {
        1: "Sur la chaise de la chambre, le linge s'est tu.",
        2: "Dans la salle d'eau, le miroir n'a plus d'œil de buée.",
        3: "Sur la table, le pain fume, une miette à part.",
    }[a]
    last = {
        (1, 1, 1): "L'oiseau de papier dort dans le sac, face à la rue.",
        (1, 1, 2): "Un carré de soleil tient sur le manteau, près du bois ouvert.",
        (1, 1, 3): "Le doudou regarde la rue, le menton sur la latte.",
        (1, 2, 1): "Une chaussette garde un peu de parquet, sous le sac ouvert.",
        (1, 2, 2): "Le manteau, près des chaussettes, sent le pain et le vent.",
        (1, 2, 3): "Le doudou, assis sur une chaussette, voit le moineau.",
        (1, 3, 1): "La poche du gilet garde une plume, collée au sac.",
        (1, 3, 2): "Le manteau et le gilet se touchent, chauds, devant le vide.",
        (1, 3, 3): "Le doudou s'endort dans le gilet, le volet ouvert.",
        (2, 1, 1): "Dans le sac, l'oiseau sent le savon, et le vent.",
        (2, 1, 2): "Le manteau sèche une goutte, près de la poignée.",
        (2, 1, 3): "Le doudou a les joues humides, et il rit vers la rue.",
        (2, 2, 1): "Une chaussette laisse une trace ronde, sous le sac.",
        (2, 2, 2): "Le manteau sent le savon, et la rue entre.",
        (2, 2, 3): "Le doudou, les pieds au chaud, voit le moineau.",
        (2, 3, 1): "La poche du gilet sent le savon, près du sac.",
        (2, 3, 2): "Le manteau boutonne le gilet, face au soleil.",
        (2, 3, 3): "Le doudou s'abrite dans le gilet, le bois ouvert.",
        (3, 1, 1): "Le sac, près du bol, garde l'oiseau et une miette.",
        (3, 1, 2): "Le manteau, près du pain, tient un fil de soleil.",
        (3, 1, 3): "Le doudou, près du four, regarde le volet ouvert.",
        (3, 2, 1): "Les chaussettes, sous la table, sentent le pain chaud.",
        (3, 2, 2): "Le manteau, sur la chaise de cuisine, garde le vent.",
        (3, 2, 3): "Le doudou a une miette sur le nez, et la rue.",
        (3, 3, 1): "La poche du gilet tient une miette, et l'oiseau.",
        (3, 3, 2): "Le manteau et le gilet, près du four, sentent le pain.",
        (3, 3, 3): "Le doudou, dans le gilet, écoute le moineau, loin.",
    }[(a, b, c)]
    mid = {
        1: "À table, le pain casse, tiède, sous les doigts.",
        2: "À table, une goutte de lait fait un rond.",
        3: "À table, le moineau chante, trop loin pour le bol.",
    }[c]
    return vet(
        [
            "narrateur|Plus tard, le pain est sur la table, tout chaud.",
            f"maman|{invite}",
            f"enfant-f|{recap}",
            f"narrateur|{keepsake}",
            f"narrateur|{mid}",
            "papa|Tu as ouvert, sans tout tirer d'un coup.",
            f"narrateur|{last}",
        ]
    )


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple[list[str], str, str, dict]] = {}

    scripts["CHK_T0000_P0000"] = (OPENING, "opening", "volet,pain,moineau", {"emphasis": "volet"})
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "la chambre",
            "option_2_label": "la salle d'eau",
            "option_3_label": "la cuisine",
        },
    )

    t2_labs = ("le t-shirt", "les chaussettes", "le gilet")
    t3_labs = ("le sac", "le manteau", "le doudou")
    t2_sons = {1: "tissu", 2: "chaussettes", 3: "laine"}
    t2_emp = {1: "t-shirt", 2: "chaussettes", 3: "gilet"}
    t3_sons = {1: "sac", 2: "manteau", 3: "doudou"}
    fin_sons = {1: "couverts,moineau", 2: "couverts,pain", 3: "couverts,volet"}

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
        scripts[f"{base}_C0001"] = (t1["confirm"], "confirm", t1["sons"], {"emphasis": "volet"})
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
                    {"emphasis": "volet"},
                )
                scripts[f"{leaf3}_F0001"] = (
                    ending(a, b, c),
                    "ending",
                    fin_sons[c],
                    {"emphasis": "volet", "note": ending_note(a, b, c)},
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
    if "victorina" not in blob:
        raise SystemExit(f"{SID}: Victorina absente")
    if "volet" not in blob:
        raise SystemExit(f"{SID}: volet absent")
    if "maya" in blob:
        raise SystemExit(f"{SID}: Maya residual")

    out = dict(src)
    out["fil_rouge"] = (
        "Dans la petite maison jaune, Victorina a glissé un oiseau de papier "
        "entre les lattes du volet. Au matin, elle veut l'ouvrir tout de suite "
        "pour la rue, le moineau et le pain. Elle tire trop vite : le bois gonflé "
        "fait clac et reste. Chambre, salle d'eau ou cuisine changent l'obstacle. "
        "T-shirt, chaussettes ou gilet changent le corps qui pousse. Sac, manteau "
        "ou doudou changent le geste qui ouvre. Le volet cède quand elle finit "
        "une chose, puis la suivante. À table, le pain paie le début."
    )
    out["title"] = TITLE
    out["characters"] = "Victorina, papa, maman"
    out["setting"] = "petite maison jaune, volet de bois, matin, odeur de pain"
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

    t1_txt = [by_src and ""]  # placeholder to keep lint quiet
    del t1_txt
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
        "# TREE-AUT-007 — Le volet de Victorina\n\n"
        "- **Nouveau titre :** *Le volet de Victorina*\n"
        "- **Public :** 5–6 ans (N3), lecture interactive familiale\n"
        "- **Leçon principale :** AUT.ROU.001 — une chose, puis la suivante (vécue, non dite)\n"
        "- **Personnages :** Victorina, papa, maman\n"
        "- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Victorina a glissé un oiseau de papier entre les lattes. Au matin, "
        "elle veut ouvrir le volet tout de suite : la rue, le moineau, le pain. "
        "Elle tire trop vite, le bois gonflé fait clac. Chambre, savon ou cuisine "
        "changent l'obstacle ; t-shirt, chaussettes ou gilet changent le corps ; "
        "sac, manteau ou doudou changent le geste. Le volet s'ouvre quand elle "
        "finit une chose avant l'autre. À table, le pain paie le début.\n\n"
        "## Améliorations appliquées\n\n"
        "- Monde (bois jaune, fente de soleil, pain, moineau) avant l'action.\n"
        "- Désir immédiat (ouvrir, libérer l'oiseau) distinct de la leçon.\n"
        "- Première idée échoue : tir trop fort, pieds nus, bois gonflé.\n"
        "- T1/T2/T3 changent l'action, pas seulement le lieu.\n"
        "- 27 fins textuellement distinctes, dernière image unique.\n"
        "- Un merci (ouverture) et un bravo vécu (chambre), pas un refrain.\n"
        "- Pas de « une étape après l'autre », pas Maya, pas apply.\n\n"
        "## Direction vocale\n\n"
        "TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending) : "
        "rate, pitch, volume, pauses, text_ssml, text_xai_tags, notes d'arc.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, {min(lengths)} à {max(lengths)} mots, moyenne {sum(lengths)//len(lengths)}\n"
        "- 27 fins et 27 dernières images distinctes\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés\n"
        "- N3 ≤ 16 mots/phrase. `check()` OK.\n\n"
        "## Relu\n\n"
        "P0000, 3 L1, 9 L2, 27 résolutions, 27 fins. Questions liées à la scène "
        "(volet / mains / pain). Option labels conservés.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(
        f"OK {SID} {nwords} mots  fins={len(set(fins))}  "
        f"chemins {min(lengths)}-{max(lengths)} moy {sum(lengths)//len(lengths)}  "
        f"1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}"
    )


if __name__ == "__main__":
    main()
