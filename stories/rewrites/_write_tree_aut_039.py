#!/usr/bin/env python3
"""TREE-AUT-039 — N3 AUT.RAN.001, Nino, caisse d'osier. F-NAR-019."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, relecture, words  # noqa: E402

N3 = LIMITS["N3"]

TICS = (
    "tout doux",
    "tout calme",
    "tout calmes",
    "on va ranger",
    "après le jeu",
    "ranger, c'est",
    "tu ranges",
)


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        low = ph.lower()
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"tic « {tic} »: {ph}")
        if re.search(r"\bencore\b", low) or re.search(r"\bd[eé]j[àa]\b", low):
            raise SystemExit(f"tic encore/déjà: {ph}")
        out.append(f"{role}|{ph}")
    return out


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


PROFILES = {
    "opening": {
        "rate": "medium",
        "wpm": 142,
        "speed": 0.98,
        "piper": 1.12,
        "pitch": "medium",
        "pitch_ssml": "medium",
        "pitch_tag": None,
        "volume": "medium",
        "db": 0,
        "pause": 500,
        "sentence": 260,
        "energy": "warm",
        "contour": "storytelling",
        "noise": 0.36,
        "emphasis": "caisse d'osier",
        "note": "arc=installation; intention=émerveiller; emotion=envie; intensite=1; destinataire=enfant; sous_texte=il veut porter comme papa; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow",
        "wpm": 116,
        "speed": 0.84,
        "piper": 1.30,
        "pitch": "medium",
        "pitch_ssml": "medium",
        "pitch_tag": None,
        "volume": "medium",
        "db": 0,
        "pause": 900,
        "sentence": 330,
        "energy": "focused",
        "contour": "rising",
        "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow",
        "wpm": 120,
        "speed": 0.86,
        "piper": 1.27,
        "pitch": "medium",
        "pitch_ssml": "medium",
        "pitch_tag": None,
        "volume": "soft",
        "db": -2,
        "pause": 700,
        "sentence": 320,
        "energy": "focused",
        "contour": "rising",
        "noise": 0.32,
        "emphasis": "lièvre",
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_le_fond; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium",
        "wpm": 132,
        "speed": 0.92,
        "piper": 1.20,
        "pitch": "medium",
        "pitch_ssml": "medium",
        "pitch_tag": None,
        "volume": "medium",
        "db": 0,
        "pause": 450,
        "sentence": 280,
        "energy": "bright",
        "contour": "falling",
        "noise": 0.34,
        "emphasis": "osier",
        "note": "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; destinataire=enfant; sous_texte=on_va_voir_dessous; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium",
        "wpm": 146,
        "speed": 1.0,
        "piper": 1.10,
        "pitch": "medium",
        "pitch_ssml": "medium",
        "pitch_tag": None,
        "volume": "medium",
        "db": 0,
        "pause": 420,
        "sentence": 250,
        "energy": "lively",
        "contour": "dynamic",
        "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il_essaie_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium",
        "wpm": 134,
        "speed": 0.93,
        "piper": 1.18,
        "pitch": "low",
        "pitch_ssml": "-2st",
        "pitch_tag": "low-pitch",
        "volume": "medium",
        "db": 0,
        "pause": 520,
        "sentence": 300,
        "energy": "tense",
        "contour": "dynamic",
        "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement; intensite=2; destinataire=enfant; sous_texte=la_premiere_idee_rate; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium",
        "wpm": 140,
        "speed": 0.97,
        "piper": 1.14,
        "pitch": "medium",
        "pitch_ssml": "medium",
        "pitch_tag": None,
        "volume": "medium",
        "db": 0,
        "pause": 560,
        "sentence": 270,
        "energy": "bright",
        "contour": "falling",
        "noise": 0.35,
        "emphasis": "lièvre",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=le_fond_apparait_quand_on_remet; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow",
        "wpm": 118,
        "speed": 0.85,
        "piper": 1.28,
        "pitch": "low",
        "pitch_ssml": "-2st",
        "pitch_tag": "low-pitch",
        "volume": "soft",
        "db": -3,
        "pause": 900,
        "sentence": 340,
        "energy": "calm",
        "contour": "falling",
        "noise": 0.31,
        "emphasis": None,
        "note": "arc=retour; intention=refermer; emotion=fierté_calme; intensite=1; destinataire=enfant; sous_texte=il_porte_la_caisse; tempo=posé; sourire=léger; respiration=ample",
    },
}


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp and emp in text:
        body = body.replace(esc(emp), f'<emphasis level="moderate">{esc(emp)}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
        f"{body}</prosody><break time=\"{m['pause']}ms\"/></speak>"
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
    if m.get("pitch_tag"):
        body = f"<{m['pitch_tag']}>{body}</{m['pitch_tag']}>"
    tail = " [long-pause]" if m["pause"] >= 800 else (" [pause]" if m["pause"] >= 400 else "")
    return (body + tail).strip()


def apply_voice(nc: dict, pname: str, emphasis: str | None = None) -> None:
    m = dict(PROFILES[pname])
    if emphasis is not None:
        m["emphasis"] = emphasis
    text = nc["text"]
    nc["text_ssml"] = ssml(text, m)
    nc["text_xai_tags"] = xai(text, m)
    nc["rate_wpm"] = m["wpm"]
    nc["rate_label"] = m["rate"]
    nc["speed_xai"] = m["speed"]
    nc["length_scale_piper"] = m["piper"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitch_ssml"]
    nc["pitch_xai_tag"] = m["pitch_tag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = m["emphasis"] or ""
    nc["pause_before_ms"] = 0
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


def profile_for(cid: str, kind: str) -> str:
    if kind == "passage_debut":
        return "opening"
    if kind == "transition_question":
        return "choice"
    if kind == "passage_question":
        return "clue"
    if kind == "passage_fin":
        return "ending"
    if cid.endswith("_C0001"):
        return "confirm"
    if "_T0003_P000" in cid:
        return "resolution"
    if "_T0002_P000" in cid:
        return "obstacle"
    return "action"


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf() -> dict:
    return {
        "expected_answer": "lièvre",
        "accepted_examples": "lièvre | le lièvre | dans la caisse | au fond | l'osier | sous les jouets | dessous",
        "retry_prompt": "Il cherche au fond. Où est le lièvre ?",
    }


# ---------------------------------------------------------------------------
# Récit
# ---------------------------------------------------------------------------

OPENING = vet(
    [
        "narrateur|Au bout de la rue, un réverbère jaunit le banc de pierre.",
        "narrateur|Nino vit là, avec papa et maman.",
        "narrateur|Une goutte tombe du toit, ronde et claire.",
        "narrateur|Elle éclate sur la mousse du banc.",
        "narrateur|Le banc est froid, un peu vert.",
        "narrateur|Un bonnet de laine attend sur la pierre.",
        "narrateur|Une feuille jaune y colle, plate et fine.",
        "narrateur|Le cartable de Nino est posé à côté.",
        "narrateur|La fermeture fait un petit zzz.",
        "narrateur|Papa tient une caisse d'osier par la corde.",
        "narrateur|L'osier sent le foin sec.",
        "narrateur|Maman boutonne son manteau, près de la grille.",
        "narrateur|La grille de cave est froide et noire.",
        "maman|Tu as mis ton bonnet, Nino ?",
        "enfant-m|Oui, maman.",
        "enfant-m|Il y a une feuille dessus.",
        "papa|On la laisse.",
        "papa|Elle est jolie.",
        "narrateur|En ce moment, Nino touche la corde de l'osier.",
        "narrateur|Les jouets sont pêle-mêle, trop hauts.",
        "enfant-m|Je veux porter la caisse !",
        "enfant-m|Le lièvre vient dans la poche.",
        "papa|D'accord.",
        "narrateur|Nino tire la corde, trop vite.",
        "narrateur|La caisse penche.",
        "narrateur|Des cubes tombent sur la mousse.",
        "narrateur|Le livre glisse sous le bonnet.",
        "narrateur|Une tasse de dînette roule, toc.",
        "enfant-m|Mon lièvre ?",
        "maman|Il était dans l'osier.",
        "narrateur|Nino fouille le tas avec les deux mains.",
        "narrateur|Il cherche sous le cartable.",
        "narrateur|Rien.",
        "papa|Tu as regardé au fond ?",
        "enfant-m|Le tas est trop haut.",
        "maman|On peut chercher là où le tas est plus petit.",
        "narrateur|Le réverbère jaunit la mousse, sans bruit.",
    ]
)

T1_Q = vet(
    [
        "papa|Nino porte la caisse où, un moment ?",
        "maman|La cuisine, le jardin, ou la chambre ?",
        "narrateur|La cuisine.",
        "narrateur|Le jardin.",
        "narrateur|Ou la chambre.",
    ]
)

ARRIVE = {
    1: vet(
        [
            "narrateur|Nino pousse la porte de la cuisine.",
            "narrateur|Les carreaux sont froids sous les chaussettes.",
            "narrateur|Ça sent l'orange pelée, contre l'évier.",
            "narrateur|Un zeste brille dans l'évier.",
            "narrateur|La casserole fait un petit tic.",
            "maman|Tu cherches ici, Nino ?",
            "enfant-m|Le lièvre voulait l'orange.",
            "papa|La caisse d'osier est près de la porte.",
            "narrateur|Nino vide le tas sur la table.",
            "narrateur|Les cubes roulent vers le zeste.",
            "enfant-m|Il n'est pas sur la table.",
            "maman|Sous les cubes, peut-être.",
            "narrateur|Un cube jaune a pris un peu d'orange.",
            "papa|Le fond de l'osier reste sombre.",
            "narrateur|Une buée fine reste sur la vitre.",
        ]
    ),
    2: vet(
        [
            "narrateur|Nino ouvre la porte du jardin.",
            "narrateur|L'herbe est mouillée, basse et froide.",
            "narrateur|La grille de cave est froide et noire.",
            "narrateur|Ça sent le foin de l'osier, dehors.",
            "enfant-m|Le lièvre voulait l'herbe.",
            "papa|La caisse est posée près du pas.",
            "maman|Une feuille jaune colle au bois.",
            "narrateur|Nino secoue la caisse au-dessus de l'herbe.",
            "narrateur|Les jouets s'éparpillent, toc toc.",
            "narrateur|Une goutte lui touche le poignet.",
            "enfant-m|Il n'est pas dans l'herbe.",
            "papa|Dans l'osier, peut-être.",
            "narrateur|Un cube a glissé près de la grille.",
            "maman|Le fond de l'osier reste sombre.",
            "narrateur|Un moineau secoue une aile, sur le toit.",
        ]
    ),
    3: vet(
        [
            "narrateur|Nino pousse la porte de la chambre.",
            "narrateur|Le rideau jaune bouge, lent et léger.",
            "narrateur|Sur le lit, le drap est un peu chaud.",
            "narrateur|Le cartable est posé contre la chaise.",
            "narrateur|La fermeture fait un petit zzz.",
            "enfant-m|Le lièvre voulait le lit.",
            "maman|La caisse d'osier est au pied du lit.",
            "papa|Le bonnet de laine est sur l'oreiller.",
            "narrateur|Nino verse le tas sur la couverture.",
            "narrateur|Les jouets s'enfoncent dans le tissu.",
            "narrateur|Il soulève un coin de drap.",
            "narrateur|Le tissu sent le savon propre.",
            "enfant-m|Il n'est pas dans le nid.",
            "maman|Dans l'osier, peut-être.",
            "papa|Le fond de l'osier reste sombre.",
            "narrateur|Le rideau se tait.",
        ]
    ),
}

Q1 = {
    1: vet(
        [
            "narrateur|Le zeste brille près du cube jaune.",
            "maman|Le petit lièvre est où ?",
        ]
    ),
    2: vet(
        [
            "narrateur|L'herbe a gardé une goutte, près du cube.",
            "papa|Le petit lièvre est où ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Le rideau jaune ne bouge plus.",
            "maman|Le petit lièvre est où ?",
        ]
    ),
}

C1 = {
    1: vet(
        [
            "narrateur|Nino se penche vers l'osier.",
            "enfant-m|Au fond, peut-être.",
            "papa|Oui.",
            "papa|On peut voir dessous, cube après cube.",
            "maman|Un cube, puis un autre.",
            "narrateur|La casserole tic, très bas.",
            "papa|Merci, Nino.",
        ]
    ),
    2: vet(
        [
            "narrateur|Nino se penche vers l'osier.",
            "enfant-m|Au fond, peut-être.",
            "maman|Oui.",
            "maman|On peut voir dessous, feuille après feuille.",
            "papa|Une feuille, puis un cube.",
            "narrateur|Le moineau a quitté le toit.",
            "maman|Merci, Nino.",
        ]
    ),
    3: vet(
        [
            "narrateur|Nino se penche vers l'osier.",
            "enfant-m|Au fond, peut-être.",
            "papa|Oui.",
            "papa|On peut voir dessous, sans le tas.",
            "maman|Le bonnet attend sur l'oreiller.",
            "narrateur|La fermeture ne fait plus zzz.",
            "papa|Merci, Nino.",
        ]
    ),
}

T2_Q = {
    1: vet(
        [
            "papa|Pour voir le fond, tu commences par quoi ?",
            "narrateur|Les cubes.",
            "narrateur|Le livre.",
            "narrateur|Ou la dînette.",
        ]
    ),
    2: vet(
        [
            "maman|Pour voir le fond, tu commences par quoi ?",
            "narrateur|Les cubes.",
            "narrateur|Le livre.",
            "narrateur|Ou la dînette.",
        ]
    ),
    3: vet(
        [
            "papa|Pour voir le fond, tu commences par quoi ?",
            "narrateur|Les cubes.",
            "narrateur|Le livre.",
            "narrateur|Ou la dînette.",
        ]
    ),
}

PLAY = {
    (1, 1): vet(
        [
            "narrateur|Les cubes de bois sont près du zeste.",
            "narrateur|Nino en empile trois, pour voir le fond.",
            "narrateur|La tour penche vers l'évier.",
            "narrateur|Elle tombe, toc toc.",
            "enfant-m|Elle est cassée.",
            "papa|Les cubes, un par un, dans l'osier.",
            "enfant-m|Pas la tour ?",
            "maman|La tour cache le fond.",
            "narrateur|Le cube jaune a un peu d'orange au coin.",
            "enfant-m|Le lièvre voulait la voir.",
            "papa|Il attend dessous, peut-être.",
            "narrateur|Un cube attrape un reflet d'orange.",
        ]
    ),
    (1, 2): vet(
        [
            "narrateur|Le livre est sous le torchon de la cuisine.",
            "narrateur|Nino s'en sert comme d'une pelle.",
            "narrateur|Il pousse le tas vers le bord.",
            "narrateur|Une page se recourbe, collée au zeste.",
            "enfant-m|Un lièvre !",
            "maman|Celui du dessin, Nino.",
            "enfant-m|Le mien est en bois.",
            "papa|Le livre, à plat, dans l'osier.",
            "narrateur|La couverture est lisse, un peu froide.",
            "maman|Le dessin n'est pas le vrai.",
            "narrateur|Une miette d'orange reste sur la page.",
            "papa|Le vrai attend au fond, peut-être.",
        ]
    ),
    (1, 3): vet(
        [
            "narrateur|La dînette cliquette près de l'évier.",
            "narrateur|Nino sert un thé d'orange dans la tasse.",
            "enfant-m|Lièvre, viens goûter !",
            "narrateur|La tasse roule, ting.",
            "narrateur|Rien ne sort de l'osier.",
            "papa|La tasse, dans l'osier, d'abord.",
            "enfant-m|Il n'a pas soif ?",
            "maman|Il n'entend pas le thé.",
            "narrateur|Nino pose la tasse près du zeste.",
            "narrateur|Ça fait ting, très petit.",
            "papa|Le fond se verra après la tasse.",
            "narrateur|La casserole tic, très bas.",
        ]
    ),
    (2, 1): vet(
        [
            "narrateur|Les cubes attendent près de la grille.",
            "narrateur|Nino en pose deux sur une pierre.",
            "enfant-m|Un pont, pour qu'il revienne.",
            "narrateur|L'herbe glisse.",
            "narrateur|Le pont s'écroule, toc.",
            "enfant-m|Il n'est pas passé.",
            "maman|Les cubes, dans l'osier, un par un.",
            "papa|Le pont cache l'herbe, pas le fond.",
            "narrateur|Un cube a une goutte d'herbe dessus.",
            "enfant-m|Il n'est pas dessus.",
            "maman|Dans la caisse, peut-être.",
            "narrateur|Une feuille jaune tremble sur le cube.",
        ]
    ),
    (2, 2): vet(
        [
            "narrateur|Le livre est sur le pas de la porte.",
            "narrateur|Nino l'ouvre vers l'herbe.",
            "enfant-m|Regarde, lièvre, c'est toi !",
            "narrateur|Le vent corne une page.",
            "narrateur|Le lièvre dessiné ne bouge pas.",
            "papa|Le livre, à plat, dans l'osier.",
            "enfant-m|Le mien est en bois.",
            "maman|Le dessin reste sur le papier.",
            "narrateur|Il serre l'ouvrage contre le manteau.",
            "narrateur|Une goutte d'herbe y brille, un instant.",
            "papa|Le vrai attend au fond, peut-être.",
            "narrateur|Le moineau est revenu, loin sur le toit.",
        ]
    ),
    (2, 3): vet(
        [
            "narrateur|La dînette est dans l'herbe, près de l'osier.",
            "narrateur|Nino sert une feuille dans l'assiette.",
            "enfant-m|Un thé de goutte, lièvre !",
            "narrateur|La petite cuillère brille, froide.",
            "narrateur|Personne ne vient goûter.",
            "maman|L'assiette, dans l'osier, d'abord.",
            "enfant-m|Il voulait l'herbe.",
            "papa|L'herbe n'est pas le fond.",
            "narrateur|L'osier pique un peu les doigts.",
            "maman|Le fond se verra après la tasse.",
            "narrateur|La grille de cave reste noire.",
            "papa|On pose, puis on voit.",
        ]
    ),
    (3, 1): vet(
        [
            "narrateur|Les cubes sont au pied du lit.",
            "narrateur|Nino les aligne vers l'osier.",
            "enfant-m|Un chemin, pour qu'il rentre.",
            "narrateur|Un cube tapote le parquet.",
            "narrateur|Le chemin se casse près du bonnet.",
            "enfant-m|Il n'est pas sous le bonnet.",
            "papa|Les cubes, dans l'osier, un par un.",
            "maman|Le chemin cache le drap, pas le fond.",
            "narrateur|Le bonnet de laine a glissé.",
            "papa|Dans la caisse, peut-être.",
            "narrateur|Le rideau jaune touche son épaule.",
            "enfant-m|Je mets les cubes.",
        ]
    ),
    (3, 2): vet(
        [
            "narrateur|Sur la couverture, le livre est ouvert.",
            "narrateur|Le rideau jaune colore la page.",
            "enfant-m|Le lièvre de la page est calme.",
            "narrateur|Nino glisse l'ouvrage sous l'oreiller.",
            "narrateur|Pour le trouver plus vite.",
            "maman|Le livre, dans l'osier, pas sous l'oreiller.",
            "enfant-m|Le mien est en bois.",
            "papa|Celui du papier reste au papier.",
            "narrateur|Une page se recourbe, légère.",
            "maman|Le vrai attend au fond, peut-être.",
            "narrateur|L'oreiller sent le savon.",
            "papa|On pose le livre, puis on voit.",
        ]
    ),
    (3, 3): vet(
        [
            "narrateur|La dînette attend au pied du lit.",
            "narrateur|Nino pose la tasse sur l'osier.",
            "enfant-m|Un thé de chambre, lièvre !",
            "narrateur|Ça fait ting, très bas.",
            "narrateur|Rien ne sort du tissu.",
            "papa|La tasse, dedans, pas dessus.",
            "enfant-m|Il voulait le lit chaud.",
            "maman|Le lit n'est pas le fond.",
            "narrateur|Une petite tasse est près du cartable.",
            "papa|Le fond se verra après la tasse.",
            "narrateur|La fermeture du cartable reste sage.",
            "maman|On pose, puis on voit.",
        ]
    ),
}

T3_Q = {
    (1, 1): vet(
        [
            "narrateur|La tour de cubes s'est couchée.",
            "maman|Nino remet les cubes à quel moment ?",
            "narrateur|Le matin.",
            "narrateur|Après la sieste.",
            "narrateur|Ou le soir.",
        ]
    ),
    (1, 2): vet(
        [
            "narrateur|La page sent l'orange, un peu.",
            "papa|Nino glisse le livre à quel moment ?",
            "narrateur|Le matin.",
            "narrateur|Après la sieste.",
            "narrateur|Ou le soir.",
        ]
    ),
    (1, 3): vet(
        [
            "narrateur|La tasse a roulé vers le zeste.",
            "maman|Nino pose la dînette à quel moment ?",
            "narrateur|Le matin.",
            "narrateur|Après la sieste.",
            "narrateur|Ou le soir.",
        ]
    ),
    (2, 1): vet(
        [
            "narrateur|Le pont de cubes a glissé.",
            "papa|Nino remet les cubes à quel moment ?",
            "narrateur|Le matin.",
            "narrateur|Après la sieste.",
            "narrateur|Ou le soir.",
        ]
    ),
    (2, 2): vet(
        [
            "narrateur|Le vent a corné la page.",
            "maman|Nino glisse le livre à quel moment ?",
            "narrateur|Le matin.",
            "narrateur|Après la sieste.",
            "narrateur|Ou le soir.",
        ]
    ),
    (2, 3): vet(
        [
            "narrateur|La feuille reste dans l'assiette.",
            "papa|Nino pose la dînette à quel moment ?",
            "narrateur|Le matin.",
            "narrateur|Après la sieste.",
            "narrateur|Ou le soir.",
        ]
    ),
    (3, 1): vet(
        [
            "narrateur|Le chemin de cubes s'est cassé.",
            "maman|Nino remet les cubes à quel moment ?",
            "narrateur|Le matin.",
            "narrateur|Après la sieste.",
            "narrateur|Ou le soir.",
        ]
    ),
    (3, 2): vet(
        [
            "narrateur|Le rideau a coloré la page.",
            "papa|Nino glisse le livre à quel moment ?",
            "narrateur|Le matin.",
            "narrateur|Après la sieste.",
            "narrateur|Ou le soir.",
        ]
    ),
    (3, 3): vet(
        [
            "narrateur|La tasse a fait ting, sur l'osier.",
            "maman|Nino pose la dînette à quel moment ?",
            "narrateur|Le matin.",
            "narrateur|Après la sieste.",
            "narrateur|Ou le soir.",
        ]
    ),
}

BODY = {
    (1, 1, 1): vet(
        [
            "narrateur|La lumière est pâle, un peu bleue.",
            "narrateur|Le réverbère s'est tu, dehors.",
            "narrateur|Nino glisse le cube jaune dans l'osier.",
            "narrateur|Puis le bleu, puis le rouge.",
            "narrateur|Toc.",
            "narrateur|Sous le dernier, un coin de bois gris.",
            "enfant-m|Une oreille !",
            "papa|Te voilà, petit.",
            "narrateur|Nino le serre contre sa joue.",
            "maman|Le chemin de l'école attend.",
            "narrateur|Il prend la corde de l'osier.",
            "narrateur|La casserole tic, très bas.",
            "narrateur|Un cube a un peu d'orange au coin.",
        ]
    ),
    (1, 1, 2): vet(
        [
            "narrateur|La lumière est ronde, un peu chaude.",
            "narrateur|Les joues de Nino sont tièdes.",
            "narrateur|Il pose les cubes comme un nid.",
            "narrateur|L'osier les accueille, sans bruit.",
            "narrateur|Au fond, le lièvre a dormi.",
            "enfant-m|Il faisait dodo.",
            "maman|Oui, sous les cubes.",
            "papa|Tu l'as trouvé.",
            "narrateur|Nino souffle sur l'oreille de bois.",
            "narrateur|Le cube jaune est tiède, comme sa joue.",
            "narrateur|Il porte la caisse vers le banc.",
            "narrateur|Le banc de pierre est tiède.",
        ]
    ),
    (1, 1, 3): vet(
        [
            "narrateur|Le réverbère se rallume, jaune.",
            "narrateur|Nino pose les cubes à la lampe.",
            "narrateur|Leurs ombres dansent sur la table.",
            "narrateur|Le dernier cube découvre une oreille.",
            "enfant-m|Mon lièvre !",
            "papa|Il était sous la tour.",
            "maman|La grille de cave est noire.",
            "narrateur|Nino glisse le bois dans la poche.",
            "narrateur|Il soulève la caisse, d'un coup sûr.",
            "narrateur|Ils rentrent, passé la grille.",
            "narrateur|Dehors, les lumières des maisons s'allument.",
            "narrateur|L'ombre des cubes reste un peu.",
        ]
    ),
    (1, 2, 1): vet(
        [
            "narrateur|La lumière est pâle, un peu bleue.",
            "narrateur|Nino glisse le livre à plat.",
            "narrateur|La page sent l'orange.",
            "narrateur|Sous la couverture, un nez de bois.",
            "enfant-m|Il était caché !",
            "maman|Sous le livre, au fond.",
            "papa|Le cartable t'attend près du banc.",
            "narrateur|Nino met le lièvre dans la poche.",
            "narrateur|Il porte la caisse vers la porte.",
            "narrateur|Les chaussures font toc toc.",
            "narrateur|La rosée sèche sur le banc de pierre.",
            "narrateur|Une miette reste sur la page.",
        ]
    ),
    (1, 2, 2): vet(
        [
            "narrateur|La lumière est ronde, un peu chaude.",
            "narrateur|Nino ferme le livre, lentement.",
            "narrateur|Il le glisse dans l'osier.",
            "narrateur|Une miette reste plate, sous le plat.",
            "narrateur|Le lièvre était le signet.",
            "enfant-m|Il lisait avec moi.",
            "papa|Il attendait la fin de la page.",
            "maman|Tes joues sont chaudes.",
            "narrateur|Nino le serre, puis la corde.",
            "narrateur|Ils vont jusqu'au banc tiède.",
            "narrateur|Le livre garde l'odeur d'orange.",
            "narrateur|Les joues de Nino restent tièdes.",
        ]
    ),
    (1, 2, 3): vet(
        [
            "narrateur|Le réverbère se rallume, jaune.",
            "narrateur|Un rond de lampe tombe sur la page.",
            "narrateur|Nino glisse le livre au fond.",
            "narrateur|Le bois gris apparaît, au bord.",
            "enfant-m|Je le vois !",
            "maman|Le rond de lampe l'a montré.",
            "papa|On rentre, la rue s'allume.",
            "narrateur|Nino porte la caisse d'une main.",
            "narrateur|L'autre tient le lièvre.",
            "narrateur|La page a un rond jaune.",
            "narrateur|La grille de cave est noire.",
            "narrateur|Les maisons allument leurs fenêtres.",
        ]
    ),
    (1, 3, 1): vet(
        [
            "narrateur|La lumière est pâle, un peu bleue.",
            "narrateur|Nino pose la tasse dans l'osier.",
            "narrateur|Ting.",
            "narrateur|Derrière l'assiette, une oreille.",
            "enfant-m|Il était à table !",
            "papa|Derrière la tasse, au fond.",
            "maman|Le chemin reprend, Nino.",
            "narrateur|La petite tasse est tiède.",
            "narrateur|Il glisse le bois dans la poche.",
            "narrateur|Il porte la caisse près du cartable.",
            "narrateur|Une cuillère minuscule brille près du zeste.",
            "narrateur|La rosée sèche sur le banc.",
        ]
    ),
    (1, 3, 2): vet(
        [
            "narrateur|La lumière est ronde, un peu chaude.",
            "narrateur|Nino range l'assiette, puis la tasse.",
            "narrateur|La cuillère glisse, ting.",
            "narrateur|Le lièvre avait un couvert.",
            "enfant-m|C'était sa place.",
            "maman|Oui, au fond de l'osier.",
            "papa|Tu l'as vu, après la tasse.",
            "narrateur|Nino souffle, puis prend la corde.",
            "narrateur|Ils s'assoient au banc tiède.",
            "narrateur|La cuillère minuscule brille.",
            "narrateur|Les joues de Nino sont chaudes.",
            "narrateur|L'osier sent l'orange, un peu.",
        ]
    ),
    (1, 3, 3): vet(
        [
            "narrateur|Le réverbère se rallume, jaune.",
            "narrateur|La tasse a un reflet orange.",
            "narrateur|Nino la pose, puis l'assiette.",
            "narrateur|Le lièvre apparaît, contre le bord.",
            "enfant-m|Il a un reflet, lui aussi.",
            "papa|On rentre, petit porteur.",
            "maman|La grille est noire, vite.",
            "narrateur|Nino porte la caisse vers la porte.",
            "narrateur|Le lièvre est dans la poche.",
            "narrateur|La tasse garde un trait orange.",
            "narrateur|Dehors, les lumières s'allument.",
            "narrateur|La casserole ne tic plus.",
        ]
    ),
    (2, 1, 1): vet(
        [
            "narrateur|La lumière est pâle, un peu bleue.",
            "narrateur|Nino glisse les cubes mouillés.",
            "narrateur|Une goutte d'herbe sèche sur le bois.",
            "narrateur|Au fond, l'oreille apparaît.",
            "enfant-m|Il n'a pas eu froid ?",
            "papa|Il était au sec, dessous.",
            "maman|Le cartable t'attend au banc.",
            "narrateur|Nino essuie le cube à sa manche.",
            "narrateur|Il prend la corde, ferme.",
            "narrateur|Ils passent près de la grille.",
            "narrateur|La rosée sèche sur le banc.",
            "narrateur|Le moineau a quitté le toit.",
        ]
    ),
    (2, 1, 2): vet(
        [
            "narrateur|La lumière est ronde, un peu chaude.",
            "narrateur|Nino pose les cubes, tièdes.",
            "narrateur|Le cube a gardé la sieste.",
            "narrateur|Le lièvre était dessous, au chaud.",
            "enfant-m|On a dormi pareil.",
            "maman|Oui, l'un sous l'autre.",
            "papa|Tu portes, maintenant.",
            "narrateur|Nino prend la caisse à deux mains.",
            "narrateur|L'herbe ne le retient plus.",
            "narrateur|Ils vont au banc tiède.",
            "narrateur|Une feuille jaune tremble, puis s'arrête.",
            "narrateur|Les joues de Nino restent chaudes.",
        ]
    ),
    (2, 1, 3): vet(
        [
            "narrateur|Le réverbère se rallume, jaune.",
            "narrateur|Un cube bleu a un grain de nuit.",
            "narrateur|Nino le glisse, puis les autres.",
            "narrateur|Le lièvre sort de l'ombre du fond.",
            "enfant-m|Il avait la nuit avec lui.",
            "papa|On rentre, la grille est noire.",
            "maman|Porte, Nino, je tiens le bonnet.",
            "narrateur|La caisse passe le pas.",
            "narrateur|Le lièvre est dans la poche.",
            "narrateur|La grille de cave reste noire.",
            "narrateur|Les maisons allument leurs fenêtres.",
            "narrateur|Le cube bleu garde son grain.",
        ]
    ),
    (2, 2, 1): vet(
        [
            "narrateur|La lumière est pâle, un peu bleue.",
            "narrateur|Nino glisse le livre, page fraîche.",
            "narrateur|Sous le plat, le bois gris.",
            "enfant-m|Il lisait l'herbe ?",
            "maman|Il attendait au fond.",
            "papa|Le chemin reprend, après le pas.",
            "narrateur|Nino met le lièvre dans la poche.",
            "narrateur|Il porte la caisse, le livre dedans.",
            "narrateur|Une page reste un peu fraîche.",
            "narrateur|Ils rejoignent le banc de mousse.",
            "narrateur|La rosée sèche, fine.",
            "narrateur|Le moineau s'envole.",
        ]
    ),
    (2, 2, 2): vet(
        [
            "narrateur|La lumière est ronde, un peu chaude.",
            "narrateur|Une goutte a séché sur la couverture.",
            "narrateur|Nino glisse le livre au nid.",
            "narrateur|Le lièvre était sous la page.",
            "enfant-m|C'était sa sieste à lui.",
            "papa|Oui, entre deux feuilles.",
            "maman|Tes joues sont chaudes, comme lui.",
            "narrateur|Nino porte la caisse vers le banc.",
            "narrateur|Le banc de pierre est tiède.",
            "narrateur|La goutte n'est plus qu'une tache.",
            "narrateur|L'osier sent le jardin tiède.",
            "narrateur|Ils s'assoient un moment.",
        ]
    ),
    (2, 2, 3): vet(
        [
            "narrateur|Le réverbère se rallume, jaune.",
            "narrateur|Le livre voit les lumières du village.",
            "narrateur|Nino le pose au fond.",
            "narrateur|Le lièvre de bois apparaît, gris.",
            "enfant-m|Il regardait les fenêtres.",
            "maman|On rentre, Nino.",
            "papa|La caisse, avec toi.",
            "narrateur|Ils passent la grille noire.",
            "narrateur|Le lièvre est dans la poche.",
            "narrateur|La page garde un peu de vent.",
            "narrateur|Les maisons s'allument, une à une.",
            "narrateur|Le livre se tait.",
        ]
    ),
    (2, 3, 1): vet(
        [
            "narrateur|La lumière est pâle, un peu bleue.",
            "narrateur|Nino pose l'assiette, feuille dedans.",
            "narrateur|Puis la tasse, ting.",
            "narrateur|Le lièvre était sous l'assiette.",
            "enfant-m|Il avait un plat d'herbe.",
            "papa|Un vrai plat, au fond.",
            "maman|Le cartable t'attend.",
            "narrateur|Nino porte la caisse vers le banc.",
            "narrateur|La feuille vraie reste dans l'assiette.",
            "narrateur|La rosée sèche sur la pierre.",
            "narrateur|Ils reprennent le chemin.",
            "narrateur|L'osier sent le foin, dehors.",
        ]
    ),
    (2, 3, 2): vet(
        [
            "narrateur|La lumière est ronde, un peu chaude.",
            "narrateur|Nino pose la dînette, sans la servir.",
            "narrateur|L'osier sent le jardin tiède.",
            "narrateur|Le lièvre était sous la tasse.",
            "enfant-m|Son thé a attendu.",
            "maman|Oui, et toi aussi.",
            "papa|Tu portes, maintenant.",
            "narrateur|Nino prend la corde.",
            "narrateur|Ils vont au banc tiède.",
            "narrateur|Les joues de Nino sont chaudes.",
            "narrateur|La petite cuillère brille, moins froide.",
            "narrateur|Une feuille reste dans l'assiette.",
        ]
    ),
    (2, 3, 3): vet(
        [
            "narrateur|Le réverbère se rallume, jaune.",
            "narrateur|La petite assiette reflète la lampe.",
            "narrateur|Nino la glisse, puis la tasse.",
            "narrateur|Le lièvre apparaît, rond comme l'ombre.",
            "enfant-m|Il a un soleil dans l'assiette.",
            "papa|On rentre, la grille est noire.",
            "maman|Porte la caisse, je ferme.",
            "narrateur|Nino passe le pas, ferme.",
            "narrateur|Le lièvre est dans la poche.",
            "narrateur|L'assiette garde le rond jaune.",
            "narrateur|Les maisons s'allument.",
            "narrateur|Le moineau se tait.",
        ]
    ),
    (3, 1, 1): vet(
        [
            "narrateur|La lumière est pâle, un peu bleue.",
            "narrateur|Nino glisse les cubes, un par un.",
            "narrateur|Un cube tapote le parquet.",
            "narrateur|Au fond, l'oreille de bois.",
            "enfant-m|Le chemin l'a mené là.",
            "maman|Il était au fond, Nino.",
            "papa|Le cartable est contre la chaise.",
            "narrateur|Nino met le lièvre dans la poche.",
            "narrateur|Il porte la caisse vers la porte.",
            "narrateur|Le bonnet rejoint sa tête.",
            "narrateur|La rosée sèche sur le banc.",
            "narrateur|Le rideau jaune ne le retient plus.",
        ]
    ),
    (3, 1, 2): vet(
        [
            "narrateur|La lumière est ronde, un peu chaude.",
            "narrateur|Nino pose un cube contre l'oreiller.",
            "narrateur|Puis il le glisse dans l'osier.",
            "narrateur|Le lièvre était près du tissu chaud.",
            "enfant-m|Il a dormi avec moi.",
            "papa|Presque, juste en dessous.",
            "maman|Tes joues sont chaudes.",
            "narrateur|Nino porte la caisse au pied du lit.",
            "narrateur|Puis vers le banc tiède.",
            "narrateur|Un cube reste calme, dans l'osier.",
            "narrateur|L'oreiller sent le savon.",
            "narrateur|Les joues de Nino restent tièdes.",
        ]
    ),
    (3, 1, 3): vet(
        [
            "narrateur|Le réverbère se rallume, jaune.",
            "narrateur|L'ombre des cubes danse sur le mur.",
            "narrateur|Nino les glisse, un, deux, trois.",
            "narrateur|Le lièvre sort de l'ombre du fond.",
            "enfant-m|Il dansait aussi ?",
            "maman|Il attendait, sans danser.",
            "papa|On rentre le reste, Nino.",
            "narrateur|Il porte la caisse vers le couloir.",
            "narrateur|Le lièvre est dans la poche.",
            "narrateur|La veilleuse allume un carré.",
            "narrateur|Les maisons, dehors, s'allument.",
            "narrateur|Le rideau jaune se tait.",
        ]
    ),
    (3, 2, 1): vet(
        [
            "narrateur|La lumière est pâle, un peu bleue.",
            "narrateur|Une bande jaune colore la page.",
            "narrateur|Nino glisse le livre au fond.",
            "narrateur|Le lièvre était sous la bande.",
            "enfant-m|Le rideau l'avait caché.",
            "papa|Le livre, oui, le fond aussi.",
            "maman|Le cartable t'attend.",
            "narrateur|Nino porte la caisse, le livre dedans.",
            "narrateur|Le lièvre est dans la poche.",
            "narrateur|Ils passent près du banc de mousse.",
            "narrateur|La rosée sèche, fine.",
            "narrateur|La page garde un peu de jaune.",
        ]
    ),
    (3, 2, 2): vet(
        [
            "narrateur|La lumière est ronde, un peu chaude.",
            "narrateur|Sur la couverture, le livre reste ouvert.",
            "narrateur|Nino le ferme, puis le glisse.",
            "narrateur|Le lièvre était entre deux pages.",
            "enfant-m|C'était sa sieste de papier.",
            "maman|Et la tienne, sur l'oreiller.",
            "papa|Tu portes, maintenant.",
            "narrateur|Nino prend la corde, près du lit.",
            "narrateur|Ils vont au banc tiède.",
            "narrateur|Les joues de Nino sont chaudes.",
            "narrateur|Le livre sent le savon, un peu.",
            "narrateur|Le rideau ne bouge plus.",
        ]
    ),
    (3, 2, 3): vet(
        [
            "narrateur|Le réverbère se rallume, jaune.",
            "narrateur|Nino glisse le livre, page savon.",
            "narrateur|Le lièvre apparaît, lisse.",
            "enfant-m|Il sent le propre.",
            "papa|On rentre, la rue s'allume.",
            "maman|Porte la caisse, je prends le cartable.",
            "narrateur|Ils quittent la chambre.",
            "narrateur|Le lièvre est dans la poche.",
            "narrateur|La page sent le savon.",
            "narrateur|La veilleuse fait un petit rond.",
            "narrateur|Les maisons s'allument.",
            "narrateur|Le bonnet attend près de la porte.",
        ]
    ),
    (3, 3, 1): vet(
        [
            "narrateur|La lumière est pâle, un peu bleue.",
            "narrateur|Nino pose la tasse près du lit.",
            "narrateur|Puis il la glisse dans l'osier.",
            "narrateur|Le lièvre était sous la tasse.",
            "enfant-m|Son thé de chambre est fini.",
            "maman|Le chemin reprend, Nino.",
            "papa|Le cartable est prêt.",
            "narrateur|Nino porte la caisse vers la porte.",
            "narrateur|Une tasse miniature reste au fond.",
            "narrateur|Le lièvre est dans la poche.",
            "narrateur|La rosée sèche sur le banc.",
            "narrateur|La fermeture du cartable fait zzz.",
        ]
    ),
    (3, 3, 2): vet(
        [
            "narrateur|La lumière est ronde, un peu chaude.",
            "narrateur|La dînette attend au pied du lit.",
            "narrateur|Nino la glisse, sans ting.",
            "narrateur|Le lièvre était contre l'osier chaud.",
            "enfant-m|Il a dormi près de la tasse.",
            "papa|Oui, au fond.",
            "maman|Tes joues sont chaudes.",
            "narrateur|Nino porte la caisse, lente.",
            "narrateur|Ils vont au banc tiède.",
            "narrateur|La dînette reste sage, au fond.",
            "narrateur|Les joues de Nino restent tièdes.",
            "narrateur|Le lit se tait.",
        ]
    ),
    (3, 3, 3): vet(
        [
            "narrateur|Le réverbère se rallume, jaune.",
            "narrateur|Une petite assiette reflète la veilleuse.",
            "narrateur|Nino la glisse, puis la tasse.",
            "narrateur|Le lièvre apparaît, rond et gris.",
            "enfant-m|Il a deux lunes, la lampe et lui.",
            "maman|On rentre le reste.",
            "papa|Porte, Nino.",
            "narrateur|La caisse passe le seuil.",
            "narrateur|Le lièvre est dans la poche.",
            "narrateur|L'assiette garde le rond de veilleuse.",
            "narrateur|Les maisons, dehors, s'allument.",
            "narrateur|La chambre s'éteint, sauf la veilleuse.",
        ]
    ),
}

FIN = {
    (1, 1, 1): vet(
        [
            "narrateur|Le lièvre a le nez contre la poche.",
            "narrateur|Nino porte la caisse, la corde à la paume.",
            "enfant-m|C'est moi le porteur, papa.",
            "papa|Oui, elle est légère, maintenant.",
            "maman|Le cube jaune garde un peu d'orange.",
            "narrateur|Ils ont cherché dans la cuisine.",
            "narrateur|La casserole tic, derrière eux.",
            "narrateur|La rosée sèche sur le banc de mousse.",
            "narrateur|Nino avance, la caisse contre la hanche.",
        ]
    ),
    (1, 1, 2): vet(
        [
            "narrateur|Nino tient le bois lisse, tiède.",
            "narrateur|La caisse repose un moment sur ses genoux.",
            "enfant-m|Il a dormi sous les cubes.",
            "papa|Et toi, sous la couverture.",
            "maman|Le cube jaune a gardé ta joue.",
            "narrateur|Le banc de pierre est tiède.",
            "narrateur|L'osier sent le foin, mêlé d'orange.",
            "narrateur|Les joues de Nino restent chaudes.",
            "narrateur|Un oiseau passe, sans se poser.",
        ]
    ),
    (1, 1, 3): vet(
        [
            "narrateur|Contre la joue, le lièvre est calme.",
            "narrateur|Nino pose la caisse près de la grille.",
            "enfant-m|Les cubes font des ombres, dehors.",
            "papa|La rue les a prises.",
            "maman|Merci d'avoir porté jusqu'ici.",
            "narrateur|L'ombre des cubes danse sous la lampe.",
            "narrateur|La grille de cave est noire.",
            "narrateur|Dehors, les lumières des maisons s'allument.",
            "narrateur|La corde reste dans sa paume, sûre.",
        ]
    ),
    (1, 2, 1): vet(
        [
            "narrateur|Au chaud, le lièvre écoute les pas.",
            "narrateur|Nino porte la caisse, le livre au fond.",
            "enfant-m|La page sent l'orange.",
            "papa|Oui, et le chemin sent la mousse.",
            "maman|Le cartable te suit, à côté.",
            "narrateur|Une page du livre sent l'orange.",
            "narrateur|Les chaussures font toc toc.",
            "narrateur|La rosée sèche sur le banc de pierre.",
            "narrateur|Le réverbère s'est tu.",
        ]
    ),
    (1, 2, 2): vet(
        [
            "narrateur|Près de la caisse, Nino respire.",
            "narrateur|Le livre reste fermé, sur ses genoux.",
            "enfant-m|Il était le signet.",
            "maman|Un signet de bois, oui.",
            "papa|La miette est plate, sous le plat.",
            "narrateur|Une miette reste sous le livre, plate.",
            "narrateur|Le banc de pierre est tiède.",
            "narrateur|Les joues de Nino restent chaudes.",
            "narrateur|L'osier sent l'orange, très bas.",
        ]
    ),
    (1, 2, 3): vet(
        [
            "narrateur|Sous la lampe, le bois gris brille.",
            "narrateur|Nino rentre, la caisse contre la hanche.",
            "enfant-m|Le rond jaune est sur la page.",
            "papa|La rue a le même rond.",
            "maman|Pose-la près du manteau.",
            "narrateur|La page a un rond de lampe, jaune.",
            "narrateur|La grille de cave est noire.",
            "narrateur|Les maisons allument leurs fenêtres.",
            "narrateur|Le livre se tait, au fond.",
        ]
    ),
    (1, 3, 1): vet(
        [
            "narrateur|Dans la poche, le lièvre est trouvé.",
            "narrateur|Nino porte la caisse, la tasse au fond.",
            "enfant-m|Son thé d'orange est fini.",
            "papa|Le chemin, maintenant.",
            "maman|La petite tasse est tiède.",
            "narrateur|Une cuillère minuscule brille près du zeste.",
            "narrateur|Ils passent le banc de mousse.",
            "narrateur|La rosée sèche, fine.",
            "narrateur|Le cartable fait zzz, à côté.",
        ]
    ),
    (1, 3, 2): vet(
        [
            "narrateur|Voilà le lièvre, contre le cartable.",
            "narrateur|Nino pose la caisse sur le banc tiède.",
            "enfant-m|Il avait sa place à table.",
            "maman|Au fond, oui.",
            "papa|La cuillère a fini de briller.",
            "narrateur|Une cuillère minuscule brille moins.",
            "narrateur|Les joues de Nino sont chaudes.",
            "narrateur|L'osier sent l'orange, un peu.",
            "narrateur|La tasse miniature s'est tue, au fond.",
        ]
    ),
    (1, 3, 3): vet(
        [
            "narrateur|Les oreilles de bois sont lisses.",
            "narrateur|Nino pose la caisse près du manteau.",
            "enfant-m|La tasse a un trait orange.",
            "papa|Comme le réverbère.",
            "maman|La casserole s'est tue.",
            "narrateur|La tasse a un reflet orange sur le bord.",
            "narrateur|Dehors, les lumières des maisons s'allument.",
            "narrateur|La grille de cave est noire.",
            "narrateur|Nino souffle, puis sourit.",
        ]
    ),
    (2, 1, 1): vet(
        [
            "narrateur|Nino glisse le lièvre dans la poche.",
            "narrateur|La caisse penche moins, dans sa main.",
            "enfant-m|Le cube a séché.",
            "papa|La goutte est partie.",
            "maman|Le moineau aussi.",
            "narrateur|Une goutte d'herbe sèche sur un cube.",
            "narrateur|Ils reprennent le chemin, près du banc.",
            "narrateur|La rosée sèche sur la pierre.",
            "narrateur|L'osier sent le foin, dehors.",
        ]
    ),
    (2, 1, 2): vet(
        [
            "narrateur|Le petit bois sent le foin.",
            "narrateur|Nino pose la caisse sur l'herbe sèche.",
            "enfant-m|On a dormi pareil.",
            "maman|Toi sur le banc, lui au fond.",
            "papa|Le cube a gardé la chaleur.",
            "narrateur|Le cube a gardé la chaleur de la sieste.",
            "narrateur|Les joues de Nino restent chaudes.",
            "narrateur|Le banc de pierre est tiède.",
            "narrateur|Une feuille jaune ne tremble plus.",
        ]
    ),
    (2, 1, 3): vet(
        [
            "narrateur|Le bois gris est contre la poche.",
            "narrateur|Nino pose la caisse derrière la porte.",
            "enfant-m|Le cube bleu a un grain de nuit.",
            "papa|La rue aussi.",
            "maman|Passe la grille, Nino.",
            "narrateur|Un cube bleu a un grain de nuit.",
            "narrateur|La grille de cave reste noire.",
            "narrateur|Les maisons allument leurs fenêtres.",
            "narrateur|L'osier sent le foin, près du pas.",
        ]
    ),
    (2, 2, 1): vet(
        [
            "narrateur|Une goutte d'herbe sèche sur l'oreille.",
            "narrateur|Nino porte la caisse, le livre au fond.",
            "enfant-m|La page est fraîche.",
            "papa|Le chemin aussi.",
            "maman|Le cartable te rejoint.",
            "narrateur|Le livre a une page un peu fraîche.",
            "narrateur|La rosée sèche sur le banc de mousse.",
            "narrateur|Le moineau s'est envolé.",
            "narrateur|Le livre frais tape le fond, au rythme des pas.",
        ]
    ),
    (2, 2, 2): vet(
        [
            "narrateur|Le bonnet de laine touche le bois.",
            "narrateur|Nino s'assoit, la caisse contre le genou.",
            "enfant-m|La goutte est une tache, maintenant.",
            "maman|Oui, sur la couverture.",
            "papa|Le banc est tiède.",
            "narrateur|Une goutte a séché sur la couverture.",
            "narrateur|Les joues de Nino sont chaudes.",
            "narrateur|L'osier sent le jardin tiède.",
            "narrateur|Ils restent un moment, sans parler.",
        ]
    ),
    (2, 2, 3): vet(
        [
            "narrateur|La corde de l'osier est calme.",
            "narrateur|Nino rentre, le livre tourné vers la rue.",
            "enfant-m|Il a vu les lumières.",
            "papa|Nous aussi.",
            "maman|Pose-la près du pas.",
            "narrateur|Le livre voit les lumières du village.",
            "narrateur|La grille de cave est noire.",
            "narrateur|Les maisons s'allument, une à une.",
            "narrateur|Le vent a quitté la page.",
        ]
    ),
    (2, 3, 1): vet(
        [
            "narrateur|Nino sent le foin, près du bois.",
            "narrateur|Il porte la caisse, l'assiette au fond.",
            "enfant-m|La feuille vraie voyage avec nous.",
            "papa|Jusqu'au banc, oui.",
            "maman|Le cartable est prêt.",
            "narrateur|Une feuille vraie reste dans l'assiette.",
            "narrateur|La rosée sèche sur le banc de pierre.",
            "narrateur|Ils reprennent le chemin.",
            "narrateur|L'herbe lâche leurs chaussures.",
        ]
    ),
    (2, 3, 2): vet(
        [
            "narrateur|Dans la paume, le bois est un peu frais.",
            "narrateur|Nino pose la caisse sur le banc tiède.",
            "enfant-m|Son thé a attendu.",
            "maman|Toi aussi.",
            "papa|La cuillère est moins froide.",
            "narrateur|L'osier sent le jardin tiède.",
            "narrateur|Les joues de Nino restent chaudes.",
            "narrateur|Une feuille reste dans l'assiette.",
            "narrateur|L'herbe lâche leurs chaussures, enfin.",
        ]
    ),
    (2, 3, 3): vet(
        [
            "narrateur|Nino souffle sur l'oreille du lièvre.",
            "narrateur|L'assiette garde un rond de lampe.",
            "enfant-m|C'est son soleil.",
            "papa|La rue a le sien, jaune.",
            "maman|Passe, je ferme le pas.",
            "narrateur|La petite assiette reflète le réverbère.",
            "narrateur|La grille de cave est noire.",
            "narrateur|Les maisons s'allument.",
            "narrateur|Nino pose la caisse derrière la porte.",
        ]
    ),
    (3, 1, 1): vet(
        [
            "narrateur|Le cartable attend, sage, à côté.",
            "narrateur|Nino porte la caisse, les cubes au fond.",
            "enfant-m|Le chemin de cubes est fini.",
            "papa|Dehors, le banc t'attend.",
            "maman|Le bonnet est sur ta tête.",
            "narrateur|Un cube tapote le fond, très bas.",
            "narrateur|La rosée sèche sur le banc de mousse.",
            "narrateur|Le rideau jaune reste derrière.",
            "narrateur|Un cube tapote au rythme des pas.",
        ]
    ),
    (3, 1, 2): vet(
        [
            "narrateur|La poche est tiède, autour du bois.",
            "narrateur|Nino pose la caisse au pied du lit.",
            "enfant-m|Un cube a vu l'oreiller.",
            "maman|Puis l'osier.",
            "papa|Tes joues sont chaudes.",
            "narrateur|Un cube est contre l'osier, calme.",
            "narrateur|Le banc de pierre est tiède.",
            "narrateur|L'oreiller sent le savon.",
            "narrateur|Les joues de Nino restent tièdes.",
        ]
    ),
    (3, 1, 3): vet(
        [
            "narrateur|Le lièvre a un grain de lumière.",
            "narrateur|Nino porte la caisse dans le couloir.",
            "enfant-m|Les cubes dansaient sur le mur.",
            "papa|La veilleuse les a pris.",
            "maman|La rue s'allume, elle aussi.",
            "narrateur|L'ombre des cubes danse sur le mur.",
            "narrateur|Les maisons, dehors, s'allument.",
            "narrateur|La chambre garde un carré de veilleuse.",
            "narrateur|Le couloir sent le foin, un instant.",
        ]
    ),
    (3, 2, 1): vet(
        [
            "narrateur|Nino referme la main autour du bois.",
            "narrateur|Il porte la caisse, le livre au fond.",
            "enfant-m|Le rideau a laissé du jaune.",
            "maman|Sur la page, oui.",
            "papa|Le banc t'attend.",
            "narrateur|Une bande jaune colore la page.",
            "narrateur|La rosée sèche sur le banc de pierre.",
            "narrateur|Le cartable fait zzz.",
            "narrateur|La bande jaune voyage avec la page.",
        ]
    ),
    (3, 2, 2): vet(
        [
            "narrateur|L'osier ne cache plus rien, maintenant.",
            "narrateur|Nino s'assoit, le livre fermé contre lui.",
            "enfant-m|Sa sieste était dans les pages.",
            "papa|La tienne, sur l'oreiller.",
            "maman|Tes joues sont chaudes.",
            "narrateur|Sur la couverture, plus de livre.",
            "narrateur|Le banc de pierre est tiède.",
            "narrateur|Une odeur de savon reste sur le livre.",
            "narrateur|Derrière eux, le rideau ne bouge plus.",
        ]
    ),
    (3, 2, 3): vet(
        [
            "narrateur|Le petit lièvre est prêt pour la nuit.",
            "narrateur|Nino pose la caisse près du manteau.",
            "enfant-m|La page sent le savon.",
            "papa|La rue sent le froid.",
            "maman|Le cartable est avec moi.",
            "narrateur|La page sent le savon, un peu.",
            "narrateur|La veilleuse fait un petit rond.",
            "narrateur|Les maisons s'allument.",
            "narrateur|Le bonnet attend près de la porte.",
        ]
    ),
    (3, 3, 1): vet(
        [
            "narrateur|Nino a le bois contre le cœur.",
            "narrateur|Il porte la caisse, la tasse au fond.",
            "enfant-m|Le thé de chambre est fini.",
            "maman|Le chemin, lui, commence.",
            "papa|Le cartable fait zzz.",
            "narrateur|Une tasse miniature est au fond.",
            "narrateur|La rosée sèche sur le banc de mousse.",
            "narrateur|Zzz, le cartable se tait.",
            "narrateur|Sans ting, la tasse voyage au fond.",
        ]
    ),
    (3, 3, 2): vet(
        [
            "narrateur|Le lièvre écoute les pas, au chaud.",
            "narrateur|Nino pose la caisse au pied du lit.",
            "enfant-m|Il a dormi près de la tasse.",
            "papa|Au fond, oui.",
            "maman|Tes joues sont chaudes.",
            "narrateur|La dînette attend au fond, sage.",
            "narrateur|Le banc de pierre est tiède.",
            "narrateur|Les joues de Nino restent tièdes.",
            "narrateur|Le lit se tait, derrière eux.",
        ]
    ),
    (3, 3, 3): vet(
        [
            "narrateur|Nino porte la caisse, d'un pas sûr.",
            "narrateur|L'assiette garde le rond de veilleuse.",
            "enfant-m|Deux lunes, papa.",
            "papa|La tienne, et celle de la rue.",
            "maman|Pose-la, on ferme.",
            "narrateur|Une petite assiette reflète la veilleuse.",
            "narrateur|Les maisons, dehors, s'allument.",
            "narrateur|La chambre s'éteint, sauf la veilleuse.",
            "narrateur|L'osier sent le foin, près de la porte.",
        ]
    ),
}

SONS_T1 = {1: "casserole", 2: "goutte,oiseau", 3: "rideau"}
SONS_T2 = {1: "bois", 2: "page", 3: "tasse"}
SONS_T3 = {1: "pas", 2: "tissu", 3: "reverbere"}
SONS_FIN = {
    1: "pas,porte",
    2: "tissu,oiseau",
    3: "reverbere,porte",
}


def write_039() -> None:
    folder = ROOT / "TREE-AUT-039"
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    scripts: dict[str, list[str]] = {}
    sons: dict[str, str] = {}
    extras: dict[str, dict] = {}

    scripts["CHK_T0000_P0000"] = OPENING
    sons["CHK_T0000_P0000"] = "goutte,osier"

    scripts["CHK_T0001_P0000"] = T1_Q
    extras["CHK_T0001_P0000"] = t3lab("la cuisine", "le jardin", "la chambre")

    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        scripts[p] = ARRIVE[i]
        sons[p] = SONS_T1[i]
        scripts[f"{p}_Q0001"] = Q1[i]
        extras[f"{p}_Q0001"] = qf()
        scripts[f"{p}_C0001"] = C1[i]
        scripts[f"{p}_T0002_P0000"] = T2_Q[i]
        extras[f"{p}_T0002_P0000"] = t3lab("les cubes", "le livre", "la dînette")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            scripts[p2] = PLAY[(i, j)]
            sons[p2] = SONS_T2[j]
            scripts[f"{p2}_T0003_P0000"] = T3_Q[(i, j)]
            extras[f"{p2}_T0003_P0000"] = t3lab("le matin", "après la sieste", "le soir")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                scripts[p3] = BODY[(i, j, k)]
                sons[p3] = SONS_T3[k]
                scripts[f"{p3}_F0001"] = FIN[(i, j, k)]
                sons[f"{p3}_F0001"] = SONS_FIN[k]

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"TREE-AUT-039 missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        text, script = from_script(scripts[cid])
        nc = dict(c)
        nc["text"] = text
        nc["script"] = script
        nc["sons"] = sons.get(cid, c.get("sons") or "") or ""
        if cid in extras:
            nc.update(extras[cid])
        apply_voice(nc, profile_for(cid, c.get("kind") or ""))
        by[cid] = nc

    out = dict(src)
    out["fil_rouge"] = (
        "Nino veut porter la caisse d'osier, le lièvre de bois dans la poche. "
        "Il tire la corde trop vite : cubes, livre et tasse s'éparpillent. "
        "Il fouille le tas, rien. Cuisine, jardin ou chambre, chaque lieu a sa fausse idée. "
        "Cubes empilés, livre-pelle ou thé pour appeler : ça rate. "
        "Il ne retrouve le lièvre qu'en glissant les jouets un à un dans l'osier. "
        "Matin de chemin, sieste tiède ou soir sous le réverbère : il porte enfin la caisse."
    )
    out["title"] = "La caisse d'osier de Nino"
    out["characters"] = "Nino, papa, maman"
    out["setting"] = "rue du village, réverbère, banc de mousse, caisse d'osier, grille de cave"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]

    check("TREE-AUT-039", out["age_band"], out["chunks"])

    fins = [c["text"] for c in out["chunks"] if c.get("kind") == "passage_fin"]
    if len(fins) != 27:
        raise SystemExit(f"fins {len(fins)} != 27")
    if len(set(fins)) != 27:
        raise SystemExit("fins non distinctes")
    lasts = []
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        ns = [ln.split("|", 1)[1] for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(ns[-1])
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières lignes non uniques: {len(set(lasts))}")
    bodies = [c["text"] for c in out["chunks"] if c["chunk_id"].endswith(("T0003_P0001", "T0003_P0002", "T0003_P0003"))]
    if len(set(bodies)) != 27:
        raise SystemExit("T3 non distincts")

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for tic in TICS:
        if tic in blob:
            raise SystemExit(f"tic global: {tic}")
    if re.search(r"\bencore\b", blob) or re.search(r"\bd[eé]j[àa]\b", blob):
        raise SystemExit("tic encore/déjà global")

    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{c['chunk_id']} fin mécanique: {last}")
        if not c.get("text_xai_tags") or "<slow>" not in (c.get("text_xai_tags") or ""):
            raise SystemExit(f"{c['chunk_id']} TTS ending incomplet")
        if "arc=" not in (c.get("notes") or ""):
            raise SystemExit(f"{c['chunk_id']} notes manquantes")

    path = folder / "merged.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size} fins={len(fins)}")


def main() -> None:
    write_039()
    relecture(
        "TREE-AUT-039",
        "La caisse d'osier de Nino",
        "Rue, réverbère, banc de mousse, osier, foin. Désir: porter la caisse, "
        "lièvre dans la poche. Imprévu: corde tirée, tas, lièvre perdu. "
        "1re idée: fouiller le tas / vider / secouer. Rate. "
        "T1 cuisine (tas sur table) / jardin (caisse secouée) / chambre (tas sur le lit). "
        "T2 cubes-tour / livre-pelle / thé pour appeler : ça rate, puis on glisse dans l'osier. "
        "T3 matin-chemin / sieste-nid / soir-rentrer. 27 fins: il porte, le lièvre au chaud.",
        "Tom→Nino (D16). N3≤16. AUT.RAN.001 implicite. "
        "Pas « on va ranger » / « après le jeu » / tics tout doux, encore, déjà, tout calme. "
        "Q=lièvre. TTS profiles example2. 86 ids. "
        "Monde ≠ 012 train, ≠ 018 étoile, ≠ 004 moulin, ≠ 029 oiseau, ≠ 034 prunier. "
        "Relu ouverture + 3 L1 + 9 L2 + 27 L3/fins (textes uniques). Pas apply.",
    )


if __name__ == "__main__":
    main()
