#!/usr/bin/env python3
"""TREE-COL-013 — Le bateau sur la vitre. F-NAR-019, N3, texte seulement."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, words  # noqa: E402

SID = "TREE-COL-013"
LIM = LIMITS["N3"]
ROLES = {"narrateur", "papa", "maman", "enfant-m", "enfant-f"}
TICS = ("tout doux", "tout calme", "on lève la main", "puis on parle")
TIC_WORDS = re.compile(r"\b(encore|déjà)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le_bateau_va_rater_le_coin; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_le_geste; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_le_grain; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=soulagement; intensite=1; destinataire=enfant; sous_texte=la_demande_a_ouvert_l_oreille; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=trop_vite_le_bateau_s_etale; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement; intensite=2; destinataire=enfant; sous_texte=deux_envies_un_seul_doigt; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=attendre_puis_demander_a_changé_la_route; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_de_carotte_a_payé_le_début; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict, emphasis: str | None) -> str:
    body = esc(text)
    if emphasis and emphasis in text:
        e = esc(emphasis)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict, emphasis: str | None) -> str:
    body = text
    if emphasis and emphasis in body:
        body = body.replace(emphasis, f"<emphasis>{emphasis}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitch_tag"):
        body = f"<{m['pitch_tag']}>{body}</{m['pitch_tag']}>"
    pause = "[long-pause]" if m["pause"] >= 800 else ("[pause]" if m["pause"] >= 400 else "")
    return f"{body} {pause}".strip()


def L(*rows: str) -> list[str]:
    out: list[str] = []
    prev = ""
    run = 1
    for raw in rows:
        if "|" not in raw:
            raise SystemExit(f"sans | : {raw}")
        role, ph = raw.split("|", 1)
        if role not in ROLES:
            raise SystemExit(f"rôle {role}: {raw}")
        parts = re.findall(r".+?[.!?]", ph.strip())
        if not parts:
            raise SystemExit(f"sans phrase: {raw}")
        leftover = ph.strip()
        for p in parts:
            leftover = leftover.replace(p, "", 1)
        if leftover.strip():
            raise SystemExit(f"reste {leftover!r}: {raw}")
        for part in parts:
            part = part.strip()
            n = words(part)
            if n > LIM:
                raise SystemExit(f"{n}>{LIM}: {part}")
            if n == 0:
                raise SystemExit(f"vide: {raw}")
            low = part.lower()
            for tic in TICS:
                if tic in low:
                    raise SystemExit(f"tic «{tic}»: {part}")
            if TIC_WORDS.search(part):
                raise SystemExit(f"tic mot: {part}")
            if role == "narrateur":
                tok = part.split()[0].lower()
                if tok == prev:
                    run += 1
                    if run >= 4:
                        raise SystemExit(f"puces « {tok} »: {part}")
                else:
                    run = 1
                    prev = tok
            else:
                run = 1
                prev = ""
            out.append(f"{role}|{part}")
    return out


def t3labs(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


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
    if "_T0003_P000" in cid and not cid.endswith("P0000"):
        return "resolution"
    if "_T0002_P000" in cid and "T0003" not in cid:
        return "obstacle"
    return "action"


def emphasis_for(name: str, text: str) -> str:
    for w in (
        "grain de carotte",
        "s'il te plaît",
        "bateau",
        "buée",
        "cubes",
        "livre",
        "dînette",
        "voile",
        "vitre",
    ):
        if w in text:
            return w
    return ""


def voice(nc: dict, name: str, extra: dict | None = None) -> None:
    m = PROFILES[name]
    text = nc["text"]
    emph = (extra or {}).get("emphasis")
    if emph is None:
        emph = emphasis_for(name, text)
    nc["text_ssml"] = ssml(text, m, emph or None)
    nc["text_xai_tags"] = xai(text, m, emph or None)
    nc["rate_wpm"] = m["wpm"]
    nc["rate_label"] = m["rate"]
    nc["speed_xai"] = m["speed"]
    nc["length_scale_piper"] = m["piper"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitch_ssml"]
    nc["pitch_xai_tag"] = m["pitch_tag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = emph or ""
    nc["pause_before_ms"] = (extra or {}).get("pause_before", 0)
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


# ---------------------------------------------------------------------------
# Récit
# ---------------------------------------------------------------------------

T1 = {
    1: L(
        "narrateur|Aniss reste face à la vitre de la cuisine.",
        "narrateur|La planche sent la carotte crue, pas la casserole.",
        "narrateur|Sarah pose un doigt, à côté du sien.",
        "enfant-f|J'ajoute la voile, d'abord.",
        "enfant-m|Non, le bateau, au grain, maintenant !",
        "narrateur|Leurs deux voix se cognent contre le verre mouillé.",
        "narrateur|Aniss pousse. La coque s'étale, trop large.",
        "narrateur|Le bateau s'arrête au milieu, loin du coin promis.",
        "enfant-f|Ma phrase n'était pas finie.",
        "narrateur|Le sourire d'Aniss n'est plus là.",
        "narrateur|Une larme d'eau vise le grain de carotte.",
        "maman|Qui parlait, là, en premier ?",
        "narrateur|Aniss ouvre la bouche, puis la referme.",
        "enfant-m|S'il te plaît. Ta voile.",
        "enfant-f|Oui. Ma voile, là.",
        "papa|Là, on t'entend, tous les deux.",
    ),
    2: L(
        "narrateur|Aniss pousse la porte du jardin, le doigt mouillé de buée.",
        "narrateur|L'herbe claque sous les bottes, lourde de pluie.",
        "narrateur|Derrière le carreau, le bateau reste, flou, à l'envers.",
        "narrateur|Le grain de carotte brille, orange, vu du dehors.",
        "enfant-m|Je le pousse d'ici !",
        "narrateur|Il tape le verre. Un coup sec.",
        "narrateur|La coque se brouille. Le phare orange tremble.",
        "enfant-f|Attends. Je voyais le chemin.",
        "narrateur|Personne n'a pris son tour.",
        "papa|Qu'est-ce qui s'est brouillé, Aniss ?",
        "enfant-m|Le bateau.",
        "maman|On s'accroupit. On regarde, sans frapper.",
        "narrateur|Papa se met à leur hauteur, près des bottes.",
        "enfant-m|S'il te plaît. Montre, toi.",
        "enfant-f|Le chemin, c'est cette goutte-là.",
        "narrateur|Aniss écoute. Ses poings se desserrent.",
    ),
    3: L(
        "narrateur|Aniss va vers la chambre, Sarah sur ses talons.",
        "narrateur|Le tapis avale le bruit des pas.",
        "narrateur|La vitre de la chambre est embuée, elle aussi.",
        "enfant-f|Un bateau sœur. Il rejoint l'autre.",
        "enfant-m|Moi, je le fais !",
        "narrateur|Il trace trop vite. La ligne fuit vers le bas.",
        "narrateur|Sarah n'a pas fini de compter les gouttes.",
        "enfant-f|J'en étais à trois.",
        "narrateur|Le bateau sœur n'atteint pas le coin de cette vitre.",
        "narrateur|Dans le couloir, le grain de carotte reste visible.",
        "maman|Tu as coupé, ou tu as attendu ?",
        "narrateur|Aniss fixe ses doigts, trop pressés.",
        "enfant-m|S'il te plaît. Compte, Sarah.",
        "enfant-f|Un. Deux. Trois.",
        "narrateur|Il ne parle pas par-dessus les nombres.",
        "narrateur|Le plaisir d'être entendue lui vient aux yeux.",
    ),
}

Q1 = {
    1: (
        L(
            "narrateur|Quelqu'un voulait ajouter une voile, avant la poussée.",
            "maman|Qui n'avait pas fini sa phrase ?",
        ),
        qf(
            "Sarah",
            "sarah | sa voile | la voile | sarah voulait la voile",
            "Une fille parlait de voile. C'était qui ?",
        ),
    ),
    2: (
        L(
            "narrateur|Un coup sec a brouillé le dessin, dehors.",
            "papa|Aniss a tapé dans quoi ?",
        ),
        qf(
            "vitre",
            "vitre | la vitre | le carreau | la fenêtre | le verre",
            "Il a frappé un carreau. C'était quoi ?",
        ),
    ),
    3: (
        L(
            "narrateur|Aniss a dessiné trop vite, sur une autre vitre.",
            "maman|Cette deuxième vitre, c'est laquelle ?",
        ),
        qf(
            "chambre",
            "chambre | la chambre | vitre de la chambre | dans la chambre",
            "Ils étaient près du tapis. Quelle pièce ?",
        ),
    ),
}

C1 = {
    1: L(
        "enfant-m|Sarah.",
        "narrateur|Oui. Sarah, et sa voile pas dite.",
        "narrateur|Aniss l'a nommée sans crier par-dessus.",
        "papa|Ta phrase est arrivée entière, cette fois.",
        "maman|Le grain tient, pour l'instant.",
        "narrateur|Le doigt d'Aniss attend, collé au milieu du bateau.",
        "narrateur|La larme d'eau n'est pas tombée.",
    ),
    2: L(
        "enfant-m|La vitre.",
        "narrateur|Oui. La vitre du jardin, froide sous la pluie.",
        "narrateur|Il l'a dite bas, après le silence.",
        "maman|On t'a entendu jusqu'au bout.",
        "papa|Le grain orange, lui, n'a pas bougé.",
        "narrateur|Sarah garde sa main près du carreau, sans frapper.",
        "narrateur|Le bateau flou attend, de l'autre côté.",
    ),
    3: L(
        "enfant-m|La chambre.",
        "narrateur|Oui. La vitre de la chambre, trop vite touchée.",
        "narrateur|Il l'a dite après les trois nombres.",
        "papa|Les nombres, puis toi. Ça passe.",
        "maman|Le grain de la cuisine nous attend.",
        "narrateur|Sarah referme les lèvres, entendue.",
        "narrateur|Le bateau sœur reste, une virgule pâle sur le verre.",
    ),
}

T2 = {
    (1, 1): L(
        "narrateur|Aniss tire le bac à cubes vers la table.",
        "narrateur|Il veut un quai, tout de suite, pour poser le poignet.",
        "enfant-m|Le rouge, pour le phare !",
        "enfant-f|Le rouge, c'est le mien. Comme le grain.",
        "narrateur|Leurs deux mains prennent le même cube.",
        "narrateur|La tour penche vers la vitre.",
        "narrateur|Sarah lâche. Aniss aussi, une seconde trop tard.",
        "narrateur|Le cube rouge tape le bois, pas le verre.",
        "enfant-m|J'allais tout casser.",
        "narrateur|Il refuse de ramasser en fonçant.",
        "papa|Vous avez vu le grain, tous les deux ?",
        "narrateur|Personne ne donne la réponse. Ils regardent.",
        "narrateur|Le grain de carotte luit, juste au-dessus du quai manqué.",
        "enfant-m|S'il te plaît. Le rouge, pour le grain.",
        "enfant-f|Tiens. J'écoute ta phrase.",
        "narrateur|Aniss sent le plaisir d'être entendu, chaud aux oreilles.",
    ),
    (1, 2): L(
        "narrateur|Aniss ouvre le livre près de l'évier.",
        "narrateur|Une page montre un bateau, presque le même.",
        "enfant-m|J'essuie la larme avec le papier !",
        "enfant-f|Pas celle-là. C'est la page du voyage.",
        "narrateur|Il lève la feuille vers la vitre.",
        "narrateur|Le papier va coller le grain de carotte.",
        "narrateur|Sarah attrape le bord, sans crier.",
        "enfant-f|Tu vas l'emmener, le phare.",
        "narrateur|Aniss s'immobilise. Le sourire n'est pas revenu.",
        "maman|On écoute le livre, ou la goutte ?",
        "narrateur|Il observe la page, puis le coin orange.",
        "enfant-m|S'il te plaît. La couverture, pas le dessin.",
        "enfant-f|Oui. Un toit, pas une gomme.",
        "narrateur|Ils posent la couverture sur le rebord, comme un auvent.",
        "papa|La goutte, maintenant, tombe sur le carton.",
        "narrateur|Le grain reste. Le bateau de doigt n'a pas bougé.",
    ),
    (1, 3): L(
        "narrateur|Aniss sort la dînette, une tasse minuscule au creux.",
        "narrateur|Il veut un port, collé au coin de la vitre.",
        "enfant-m|La tasse, là, sous le grain !",
        "enfant-f|D'abord la mer. Je verse.",
        "narrateur|Sarah souffle de l'air, pour de faux, trop près.",
        "narrateur|La tasse cliquette. Le grain de carotte saute d'un poil.",
        "enfant-m|Il va tomber !",
        "narrateur|Il tend la main, puis la retire.",
        "narrateur|Ils refusent de foncer sur le verre.",
        "papa|Qui parle, là, en premier ?",
        "narrateur|Un silence. La gouttière seule répond.",
        "enfant-m|S'il te plaît. Ta mer, puis le port.",
        "enfant-f|Ma mer est prête. Ta tasse, maintenant.",
        "maman|Deux tours. Un coin.",
        "narrateur|La tasse pose à côté, pas sur le phare orange.",
        "narrateur|Aniss entend sa propre phrase, entière, et ça lui va.",
    ),
    (2, 1): L(
        "narrateur|Sous le porche, Aniss aligne des cubes mouillés.",
        "narrateur|Il veut un observatoire, pour voir le grain de l'extérieur.",
        "enfant-m|Plus haut !",
        "enfant-f|Le mien d'abord. Je vise le phare.",
        "narrateur|Le cube du dessus glisse dans une flaque.",
        "narrateur|De l'eau saute vers le carreau.",
        "enfant-m|Je l'essuie !",
        "narrateur|Sa manche se lève. Sarah pose deux doigts sur son poignet.",
        "enfant-f|Si tu frottes, le bateau part.",
        "narrateur|Aniss s'arrête. L'envie lui pique les dents.",
        "maman|Vous voyez le grain, de là ?",
        "narrateur|Ils regardent. Personne ne dicte le geste.",
        "enfant-m|S'il te plaît. Ton cube, en bas, stable.",
        "enfant-f|Le mien tient. Le tien, au-dessus.",
        "papa|L'un après l'autre, la tour tient.",
        "narrateur|Par la vitre, le grain de carotte reste un point orange.",
    ),
    (2, 2): L(
        "narrateur|Sarah ouvre le livre sous le porche, à l'abri.",
        "narrateur|Une carte de rivière, presque une vitre en papier.",
        "enfant-m|Je montre le coin, avec la page !",
        "narrateur|Le vent soulève la feuille vers le carreau mouillé.",
        "enfant-f|Elle va coller !",
        "narrateur|Aniss veut l'arracher. Il referme les doigts, vide.",
        "narrateur|Il refuse de foncer dans le vent.",
        "papa|Le livre, ou le grain, lequel d'abord ?",
        "narrateur|Ils écoutent la gouttière, puis le papier.",
        "enfant-m|S'il te plaît. Tiens le bord, toi.",
        "enfant-f|Je tiens. Toi, tu nommes le coin.",
        "enfant-m|Là. Le grain de carotte, en haut à droite.",
        "maman|Ta voix est arrivée, sans crier.",
        "narrateur|La page se pose à plat, loin du verre.",
        "narrateur|Le bateau, derrière, n'a pas bougé d'un trait.",
        "narrateur|Sarah souffle, entendue, le livre contre le manteau.",
    ),
    (2, 3): L(
        "narrateur|Aniss pose une tasse de dînette dans l'herbe rase.",
        "narrateur|La pluie y fait une mer minuscule, trop vite.",
        "enfant-m|Je la verse sur la vitre, pour le bateau !",
        "enfant-f|Non. C'est ma mer à regarder.",
        "narrateur|Il bascule la tasse. Une goutte file vers le seuil.",
        "narrateur|Sarah recule sa mer, sans crier par-dessus.",
        "enfant-m|J'ai failli tout noyer.",
        "maman|Qui voulait verser, qui voulait regarder ?",
        "narrateur|Aniss avale sa réponse trop rapide.",
        "enfant-m|S'il te plaît. On regarde, d'abord.",
        "enfant-f|Ma mer reste dans la tasse.",
        "papa|Le grain, lui, n'a pas besoin d'eau.",
        "narrateur|Ils s'accroupissent. La tasse tremble, puis tient.",
        "narrateur|Derrière le carreau, le grain de carotte ne bouge pas.",
        "narrateur|Aniss n'a pas versé. Un rire court lui échappe.",
        "narrateur|Sarah incline la tasse, juste pour lui montrer.",
    ),
    (3, 1): L(
        "narrateur|Dans la chambre, Aniss fait une file de cubes vers la porte.",
        "narrateur|Un chemin, pour ramener le doigt jusqu'à la cuisine.",
        "enfant-m|Moi le premier cube !",
        "enfant-f|Le mien, c'est le capitaine.",
        "narrateur|Deux cubes se cognent. La file se casse.",
        "enfant-m|On y va, vite !",
        "narrateur|Il s'élance. Sarah reste à genoux, le capitaine en main.",
        "narrateur|Il s'arrête au tapis. Il ne fonce pas jusqu'à la vitre.",
        "papa|Le chemin, il est à qui, là ?",
        "narrateur|Le silence de la chambre répond d'abord.",
        "enfant-m|S'il te plaît. Ton capitaine, devant.",
        "enfant-f|Devant. Toi, derrière. Jusqu'au grain.",
        "maman|On a entendu les deux phrases.",
        "narrateur|La file reprend, un cube après l'autre, sans se marcher.",
        "narrateur|Au bout du couloir, le grain de carotte luit, minuscule.",
        "narrateur|Aniss marche au rythme de Sarah, pas devant.",
    ),
    (3, 2): L(
        "narrateur|Sarah ouvre le livre sur l'oreiller.",
        "narrateur|Une image de port, avec un phare tout petit.",
        "enfant-m|On copie, vite, sur les deux vitres !",
        "narrateur|Il tourne deux pages d'un coup.",
        "enfant-f|J'avais pas fini l'image.",
        "narrateur|Le livre se referme sur son doigt, sans faire mal.",
        "narrateur|Aniss veut tirer. Il lâche.",
        "maman|On tourne, ou on regarde ?",
        "narrateur|Personne ne répond à sa place.",
        "enfant-m|S'il te plaît. Rouvre, toi.",
        "enfant-f|Le phare. Comme le grain de carotte.",
        "papa|Tu as vu la ressemblance, après elle.",
        "narrateur|Ils gardent la page ouverte, loin de la buée de la chambre.",
        "narrateur|Aniss n'a pas recopié trop vite, cette fois.",
        "narrateur|Sarah nomme le phare jusqu'au bout. Il hoche.",
        "narrateur|Dans le couloir, le vrai grain attend, orange.",
    ),
    (3, 3): L(
        "narrateur|Aniss pose la dînette près du doudou.",
        "narrateur|Un bureau de port, avant de revenir à la cuisine.",
        "enfant-f|Je sers. Tu attends ta tasse.",
        "enfant-m|On y va ! Le grain tombe !",
        "narrateur|Il se lève trop tôt. La tasse bascule sur le tissu.",
        "enfant-f|Ma phrase, elle était au milieu.",
        "narrateur|Aniss s'assoit. Il refuse de courir dans le couloir.",
        "papa|Le port, il a un tour de parole, ou pas ?",
        "narrateur|Aniss regarde la tasse couchée, puis Sarah.",
        "enfant-m|S'il te plaît. Sers. J'attends.",
        "enfant-f|Voilà. C'est du vent, mais c'est pour toi.",
        "maman|Ta demande est arrivée, entière.",
        "narrateur|Il boit l'air, sérieux, et ça lui va.",
        "narrateur|Ils emportent la tasse vide, comme une lanterne.",
        "narrateur|Au bout, le grain de carotte n'est pas tombé.",
        "narrateur|Le doudou garde une petite tache d'air, imaginaire.",
    ),
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    table = {
        (1, 1, 1): L(
            "narrateur|Le matin, la pluie tape plus fort sur le zinc.",
            "narrateur|Une larme grasse vise le cube rouge et le grain.",
            "enfant-m|J'attrape le grain !",
            "narrateur|Sa main s'arrête à un souffle du verre.",
            "enfant-f|S'il te plaît, laisse-le. Je souffle la goutte.",
            "narrateur|Aniss écoute. Il ne coupe pas.",
            "papa|La goutte est passée, à côté.",
            "enfant-m|Maintenant, le bateau. Ensemble.",
            "narrateur|Deux doigts, lents, glissent la coque jusqu'au coin.",
            "narrateur|Ça a failli tout emporter. Le grain de carotte tient.",
            "maman|Vous avez demandé, puis avancé.",
            "narrateur|Le quai de cubes reste bas, sec sur le bois.",
        ),
        (1, 1, 2): L(
            "narrateur|Après la sieste, un carré de soleil lèche la vitre.",
            "narrateur|Le grain de carotte sèche, prêt à se décoller.",
            "enfant-f|Il va tomber tout seul.",
            "enfant-m|Je le recolle avec le cube !",
            "narrateur|Il lève le rouge. Sarah secoue la tête, sans crier.",
            "narrateur|Il pose le cube. Il demande.",
            "enfant-m|S'il te plaît. On pousse le bateau, pas le grain.",
            "enfant-f|Oui. Le phare reste où il est.",
            "papa|Le soleil attend, lui aussi.",
            "narrateur|Ils glissent la coque sous le grain, sans le toucher.",
            "narrateur|Le bateau arrive. Le grain penche, puis tient.",
            "maman|Ça a failli. Vous n'avez pas foncé.",
        ),
        (1, 1, 3): L(
            "narrateur|Sous la lampe, le soir chauffe le coin de la vitre.",
            "narrateur|Le grain de carotte glisse d'un poil, vers la tour.",
            "enfant-m|La tour le rattrape !",
            "narrateur|Sarah met sa paume entre les cubes et le verre.",
            "enfant-f|S'il te plaît, pas les cubes contre.",
            "narrateur|Aniss retire la tour d'un cran, sans parler par-dessus.",
            "papa|Il reste de la place, pour un bateau.",
            "narrateur|Ils poussent, lents, sous la lumière jaune.",
            "narrateur|La coque rejoint le coin. Le grain s'arrête.",
            "maman|La lampe a vu le voyage entier.",
            "enfant-m|On a demandé le chemin.",
            "narrateur|Un cube rouge garde l'ombre du phare, sur le bois.",
        ),
        (1, 2, 1): L(
            "narrateur|Le matin, la goutte rebondit sur la couverture-auvent.",
            "narrateur|Elle cherche quand même le grain de carotte.",
            "enfant-m|J'essuie avec la page !",
            "enfant-f|S'il te plaît, non. Le dessin.",
            "narrateur|Aniss referme le livre d'images, garde le carton.",
            "papa|Le carton boit l'eau. Le grain, non.",
            "narrateur|Deux doigts glissent le bateau sous l'auvent.",
            "narrateur|La coque arrive au coin, juste à temps.",
            "maman|La page est sèche. Le phare aussi.",
            "enfant-m|Ta voile, elle est là, maintenant.",
            "enfant-f|Je l'ai dite jusqu'au bout.",
            "narrateur|Le livre reste ouvert au bateau, loin du verre.",
        ),
        (1, 2, 2): L(
            "narrateur|Après la sieste, un courant d'air ferme le livre.",
            "narrateur|Le carton bascule. Il manque le grain de carotte.",
            "enfant-f|Le toit !",
            "narrateur|Aniss veut rattraper d'un geste large. Il s'arrête.",
            "enfant-m|S'il te plaît. Pose-le, toi.",
            "enfant-f|Voilà. Tout près, pas dessus.",
            "papa|L'air a perdu. Le grain tient.",
            "narrateur|Ils font glisser la coque, sous le carton revenu.",
            "narrateur|Le bateau touche le coin. Une seconde de trop, et non.",
            "maman|Vous avez parlé chacun votre tour.",
            "narrateur|Sarah garde un doigt sur la couverture, fière.",
            "narrateur|La page du voyage n'a pas bu la buée.",
        ),
        (1, 2, 3): L(
            "narrateur|Le soir, la lampe allume le grain de carotte, comme un feu.",
            "narrateur|L'ombre du livre tombe de travers, sur la route.",
            "enfant-m|J'ôte le livre !",
            "enfant-f|S'il te plaît, on le tourne, juste.",
            "narrateur|Aniss écoute. Ils pivotent le carton, pas la vitre.",
            "papa|La route est libre, sous le feu orange.",
            "narrateur|Le bateau glisse, lent, dans la lumière.",
            "narrateur|Il gagne le coin. Le grain ne s'éteint pas.",
            "maman|Le soir a failli tout cacher. Pas cette fois.",
            "enfant-m|J'ai attendu ta phrase.",
            "enfant-f|Moi aussi, la tienne.",
            "narrateur|Le livre se ferme. Une lueur orange reste au verre.",
        ),
        (1, 3, 1): L(
            "narrateur|Le matin, Sarah verse sa mer d'air trop près du coin.",
            "narrateur|La tasse penche vers le grain de carotte.",
            "enfant-m|Je la retiens !",
            "narrateur|Il demande avant de toucher la main de Sarah.",
            "enfant-m|S'il te plaît. J'aide.",
            "enfant-f|Oui. Ensemble, on pose.",
            "papa|La tasse a un quai, à côté, pas dessus.",
            "narrateur|Le bateau part. Deux doigts, une coque, le coin.",
            "maman|La mer est restée dans la tasse.",
            "narrateur|Le grain tient, sec, au-dessus du port minuscule.",
            "enfant-f|Ma mer, tu l'as laissée finir.",
            "narrateur|Aniss hoche. Ça a failli. Ça tient.",
        ),
        (1, 3, 2): L(
            "narrateur|Après la sieste, la soucoupe sert de dock, sous le coin.",
            "narrateur|Le grain de carotte s'est collé, un instant, au bord.",
            "enfant-f|Ne le mange pas. C'est le phare.",
            "enfant-m|Je n'y avais pas pensé, comme ça.",
            "narrateur|Il voulait souffler. Il demande.",
            "enfant-m|S'il te plaît. On recule la soucoupe.",
            "papa|Un pas. Le grain reste au verre.",
            "narrateur|Ils glissent le bateau jusqu'au phare rendu.",
            "maman|Le dock n'a pas avalé le voyage.",
            "narrateur|La tasse cliquette une fois, puis se tait.",
            "enfant-f|Tu as écouté ma peur.",
            "narrateur|Aniss sent ce plaisir-là, discret, dans la poitrine.",
        ),
        (1, 3, 3): L(
            "narrateur|Le soir, trois assiettes de dînette alignent un banquet.",
            "narrateur|Aniss veut poser le grain de carotte dans l'une.",
            "enfant-f|S'il te plaît, il n'est pas à manger.",
            "narrateur|Sa main s'ouvre. Le grain reste au verre.",
            "papa|Le banquet, c'est pour le bateau, pas pour le phare.",
            "narrateur|Ils font glisser la coque entre les assiettes et la vitre.",
            "narrateur|Le coin s'offre. La lampe dore le grain.",
            "maman|Vous avez parlé avant de prendre.",
            "enfant-m|Le port est prêt. Le bateau aussi.",
            "enfant-f|Ma phrase, tu l'as prise avec toi.",
            "narrateur|Une assiette vide garde un rond de lumière orange.",
            "narrateur|Ça a failli devenir un goûter. Le phare est resté.",
        ),
        (2, 1, 1): L(
            "narrateur|Le matin, sous le porche, l'eau dégouline du toit.",
            "narrateur|Aniss veut frotter la vitre, pour mieux voir le grain.",
            "enfant-f|S'il te plaît, pas la manche.",
            "narrateur|Il baisse le bras. Les cubes tiennent, mouillés.",
            "papa|On rentre d'un pas. On pousse de l'intérieur.",
            "narrateur|Ils passent. Deux doigts retrouvent la coque floue.",
            "narrateur|Le bateau gagne le coin. Le grain de carotte reste.",
            "maman|Dehors, vous n'avez pas frappé.",
            "enfant-m|Ton cube visait juste.",
            "enfant-f|Toi, tu as attendu ma phrase.",
            "narrateur|La tour du porche penche, mais le verre est intact.",
            "narrateur|Une botte laisse une virgule d'eau, sur le seuil.",
        ),
        (2, 1, 2): L(
            "narrateur|Après la sieste, le soleil perce. Le grain orange flambe.",
            "narrateur|Vu du jardin, il semble facile à prendre.",
            "enfant-m|Je le décroche d'ici !",
            "narrateur|Sarah pose le cube haut, comme une lunette, pas un outil.",
            "enfant-f|S'il te plaît, on rentre. On glisse.",
            "papa|La lunette a montré. La main, dedans.",
            "narrateur|Ils rentrent. Le bateau part, lent, vers le feu orange.",
            "maman|Le soleil a failli le sécher trop. Pas tout à fait.",
            "narrateur|Le grain de carotte tient, un peu plus pâle.",
            "enfant-m|J'ai vu par ton cube.",
            "enfant-f|Tu as demandé avant de décrocher.",
            "narrateur|Dehors, la tour sèche, petite, sous le porche.",
        ),
        (2, 1, 3): L(
            "narrateur|Dehors, le soir, la lumière de la cuisine perce.",
            "narrateur|Le grain de carotte devient une étincelle, derrière le verre.",
            "enfant-m|Un petit coup, pour le réveiller.",
            "enfant-f|S'il te plaît, on tape pas.",
            "narrateur|Aniss retient le poing. Ils rentrent sans frapper.",
            "papa|L'étincelle n'avait pas besoin d'un coup.",
            "narrateur|Deux doigts glissent le bateau jusqu'à l'étincelle.",
            "maman|Le soir a tout rendu plus fragile. Vous avez ralenti.",
            "enfant-m|Ta phrase m'a arrêté.",
            "enfant-f|La mienne est arrivée.",
            "narrateur|Les cubes du porche restent, sombres, oubliés un moment.",
            "narrateur|Sur la vitre, le grain veille, orange, minuscule.",
        ),
        (2, 2, 1): L(
            "narrateur|Le matin, le livre sert d'auvent, sous la gouttière.",
            "narrateur|Une goutte perce quand même, vers le grain de carotte.",
            "enfant-m|Je lève le livre contre le verre !",
            "enfant-f|S'il te plaît, on rentre. Le papier a peur.",
            "narrateur|Aniss écoute le papier, et Sarah.",
            "papa|Dedans, le doigt. Dehors, le livre se ferme.",
            "narrateur|Ils glissent la coque. Le coin s'offre, juste.",
            "maman|La page n'a pas collé. Le grain tient.",
            "enfant-m|J'ai nommé le coin, après toi.",
            "enfant-f|Le bord, je l'ai tenu jusqu'au bout.",
            "narrateur|Le livre sent l'herbe mouillée, un peu, sur la couverture.",
            "narrateur|Ça a failli. Le bateau est au phare.",
        ),
        (2, 2, 2): L(
            "narrateur|Après la sieste, une page s'envole vers le carreau.",
            "narrateur|Elle manque le grain de carotte, de très peu.",
            "enfant-f|S'il te plaît, rattrape le bord, pas le verre.",
            "narrateur|Aniss pince le papier. Pas la buée.",
            "papa|La carte a survécu. Le phare aussi.",
            "narrateur|Ils rentrent. Le bateau reprend sa route, lente.",
            "narrateur|Le coin arrive. Sarah referme le livre, enfin.",
            "maman|Le vent a perdu, parce que vous avez parlé.",
            "enfant-m|Ta phrase, je l'ai prise.",
            "enfant-f|La mienne tenait le bord.",
            "narrateur|Une coin de page reste plié, souvenir du presque.",
            "narrateur|Le grain orange ne s'est pas envolé.",
        ),
        (2, 2, 3): L(
            "narrateur|Le soir, le livre fermé sert de marche, sous le porche.",
            "narrateur|Aniss veut monter pour souffler le grain de carotte.",
            "enfant-f|S'il te plaît, on souffle pas. On glisse.",
            "narrateur|Il descend. Ils rentrent, le livre sous le bras.",
            "papa|Le phare n'est pas une bougie.",
            "narrateur|Le bateau part dans la lumière de la cuisine.",
            "narrateur|Il gagne le coin. Le grain reste, comme une petite lune.",
            "maman|Vous avez choisi le doigt, pas le souffle.",
            "enfant-m|J'ai attendu ta phrase, dehors.",
            "enfant-f|Dedans, j'ai attendu la tienne.",
            "narrateur|Le livre pose sur la table, un peu humide au dos.",
            "narrateur|La lune orange veille. Le voyage a failli, puis oui.",
        ),
        (2, 3, 1): L(
            "narrateur|Le matin, la tasse de pluie déborde dans l'herbe.",
            "narrateur|Aniss veut la coller sous le grain, dehors.",
            "enfant-f|S'il te plaît, le grain n'a pas soif.",
            "narrateur|Il reverse l'eau dans l'herbe, pas sur le verre.",
            "papa|Tasse vide. Doigt dedans.",
            "narrateur|Ils rentrent. Le bateau glisse, enfin, vers le coin.",
            "maman|La mer est restée au jardin. Le phare, à la vitre.",
            "narrateur|Le grain de carotte tient, sec.",
            "enfant-m|J'ai versé à côté, grâce à toi.",
            "enfant-f|Ma mer, tu ne l'as pas jetée au bateau.",
            "narrateur|La tasse cliquette, vide, sur le rebord intérieur.",
            "narrateur|Ça a failli noyer le dessin. Il est au port.",
        ),
        (2, 3, 2): L(
            "narrateur|Après la sieste, Sarah lève la tasse, phare de porcelaine.",
            "narrateur|Le vrai grain de carotte, derrière, pâlit au soleil.",
            "enfant-m|On change. Le tien est plus grand !",
            "enfant-f|S'il te plaît, le mien, c'est pour jouer. Le vrai, on y va.",
            "narrateur|Aniss pose la tasse. Ils rentrent sans argumenter.",
            "papa|Deux phares. Un seul bateau.",
            "narrateur|La coque rejoint le vrai, orange, minuscule.",
            "maman|Le soleil a pressé. Vous n'avez pas pressé avec.",
            "enfant-m|Ta phrase a choisi le vrai.",
            "enfant-f|La tasse, elle nous a guidés, juste.",
            "narrateur|Dehors, la porcelaine sèche, blanche, sur une pierre.",
            "narrateur|Le grain reste. Le bateau le touche, à peine.",
        ),
        (2, 3, 3): L(
            "narrateur|Le soir, un cliquetis de tasse manque de faire tomber le grain.",
            "narrateur|Sarah retient la porcelaine. Aniss retient sa voix.",
            "enfant-m|S'il te plaît. On rentre, sans cliquetis.",
            "enfant-f|Oui. Pied à pied.",
            "papa|Le silence, parfois, c'est une réponse.",
            "narrateur|Ils glissent le bateau. Le coin s'ouvre, orange.",
            "maman|Le grain de carotte n'a pas sauté, cette fois.",
            "narrateur|La tasse pose loin, sur la table, enfin muette.",
            "enfant-m|J'ai parlé bas.",
            "enfant-f|Moi, j'ai tenu.",
            "narrateur|La lumière du soir tient le phare, tout contre le verre.",
            "narrateur|Le voyage a failli, au cliquetis. Il est là.",
        ),
        (3, 1, 1): L(
            "narrateur|Le matin, la file de cubes arrive au seuil de la cuisine.",
            "narrateur|Le dernier cube manque le grain de carotte, trop près.",
            "enfant-m|Je le pousse, le cube, sous le phare !",
            "enfant-f|S'il te plaît, le cube s'arrête. Le doigt continue.",
            "narrateur|Aniss pose le capitaine. Deux doigts reprennent la coque.",
            "papa|Le chemin a fait son travail. Le bateau, maintenant.",
            "narrateur|Ils glissent. Le coin. Le grain tient.",
            "maman|Le matin pressait. Vous avez ralenti au seuil.",
            "enfant-m|Ton capitaine a parlé en premier.",
            "enfant-f|Toi, tu as écouté au bout du tapis.",
            "narrateur|Une file de cubes garde la porte, comme une jetée.",
            "narrateur|Ça a failli, au dernier cube. Le bateau est au phare.",
        ),
        (3, 1, 2): L(
            "narrateur|Après la sieste, deux bateaux : chambre et cuisine.",
            "narrateur|Aniss veut les rejoindre d'un seul trait, trop long.",
            "enfant-f|S'il te plaît, un seul. Celui du grain.",
            "narrateur|Il lâche le bateau sœur. Ils viennent au vrai.",
            "papa|Un voyage. Un phare.",
            "narrateur|La coque de cuisine glisse jusqu'au grain de carotte.",
            "maman|L'autre attendra, sur le verre de la chambre.",
            "enfant-m|J'ai laissé ta sœur-bateau.",
            "enfant-f|Merci, Aniss.",
            "narrateur|Sarah le dit à lui, et ça lui va.",
            "narrateur|Le grain penche, puis se tient, après la sieste tiède.",
            "narrateur|Les cubes du couloir restent, un pont inachevé, volontaire.",
        ),
        (3, 1, 3): L(
            "narrateur|Le soir, la file de cubes est une piste sombre, vers la lampe.",
            "narrateur|Aniss trébuche. Un cube roule vers le grain de carotte.",
            "enfant-f|S'il te plaît, on le laisse. On glisse.",
            "narrateur|Il ne rattrape pas. Le cube s'arrête au bois.",
            "papa|La piste a dit assez.",
            "narrateur|Deux doigts, la coque, le coin. Le grain tient.",
            "maman|Le soir a tout rendu glissant. Pas vos phrases.",
            "enfant-m|Ta phrase a arrêté mon pied.",
            "enfant-f|La mienne a arrêté le cube.",
            "narrateur|Une piste de bois mène vers la lumière orange.",
            "narrateur|Le bateau touche le phare. Ça a failli, quand le pied a glissé.",
            "narrateur|Sarah pose le capitaine, enfin, à terre.",
        ),
        (3, 2, 1): L(
            "narrateur|Le matin, le livre ouvert montre un X, comme le grain.",
            "narrateur|Aniss veut coller la page à la vitre, pour viser.",
            "enfant-f|S'il te plaît, l'œil, pas la colle.",
            "narrateur|Il garde le livre au creux du bras, loin du verre.",
            "papa|La carte a parlé. Le doigt travaille.",
            "narrateur|Le bateau glisse vers le grain de carotte, sans papier.",
            "maman|Le matin mouillait tout. Pas cette page.",
            "enfant-m|Ton X m'a montré.",
            "enfant-f|Ta main n'a pas collé.",
            "narrateur|Sur l'oreiller, le livre se ferme, au sec.",
            "narrateur|Au vrai verre, le grain reste orange, gagné.",
            "narrateur|En chambre, le bateau sœur n'a pas été forcé.",
        ),
        (3, 2, 2): L(
            "narrateur|Après la sieste, ils relisent le port, trop longtemps.",
            "narrateur|Une goutte, à la cuisine, vise le grain de carotte.",
            "enfant-m|On y va !",
            "enfant-f|S'il te plaît, je finis la ligne.",
            "narrateur|Aniss attend la dernière ligne. Puis ils courent, sans se bousculer.",
            "papa|La ligne, puis le doigt.",
            "narrateur|La coque rattrape le coin, juste sous la goutte passée.",
            "maman|Vous avez failli rester dans le livre.",
            "enfant-m|J'ai attendu ta ligne.",
            "enfant-f|Moi, j'ai couru après, avec toi.",
            "narrateur|Sur l'oreiller, la page du port reste ouverte.",
            "narrateur|Au verre, le grain tient, un peu gras de buée.",
        ),
        (3, 2, 3): L(
            "narrateur|Le soir, le livre dort sur le lit. Ils marchent vers la lampe.",
            "narrateur|Aniss veut raconter le phare, pendant que Sarah pousse.",
            "enfant-f|S'il te plaît, d'abord le bateau. Après, tu racontes.",
            "narrateur|Il se tait. Ils glissent. Le grain de carotte les attend.",
            "papa|Le récit, après le coin.",
            "narrateur|La coque arrive. Aniss peut parler, enfin.",
            "enfant-m|Le phare du livre, c'était lui.",
            "maman|On t'écoute, maintenant. Toute la phrase.",
            "enfant-f|J'ai poussé. Toi, tu racontes.",
            "narrateur|Le soir tient le grain, comme un point de lampe.",
            "narrateur|Le livre, loin, garde l'image. La vitre, le vrai.",
            "narrateur|Ça a failli se mêler. Chaque chose a eu son tour.",
        ),
        (3, 3, 1): L(
            "narrateur|Le matin, la tasse-lanterne tremble au seuil.",
            "narrateur|Aniss veut l'accrocher sous le grain de carotte.",
            "enfant-f|S'il te plaît, lanterne à terre. Doigt au verre.",
            "narrateur|Il pose la tasse. Ils glissent la coque au coin.",
            "papa|Le port de la chambre a fini son travail.",
            "maman|Le matin éclairait trop. Vous avez posé.",
            "enfant-m|J'ai attendu le service, là-bas.",
            "enfant-f|Ici, tu as posé quand je l'ai dit.",
            "narrateur|La tasse vide garde un rond de lumière, sur le bois.",
            "narrateur|Au coin, le bateau frôle enfin le grain.",
            "narrateur|En chambre, le doudou n'a plus de tasse sur lui.",
            "narrateur|Ça a failli s'accrocher. Ça a glissé, à la place.",
        ),
        (3, 3, 2): L(
            "narrateur|Après la sieste, les yeux piquent. Le grain de carotte penche.",
            "narrateur|Aniss bâille. Il veut finir demain, dans sa tête.",
            "enfant-f|S'il te plaît, maintenant. Il tombe.",
            "narrateur|Il se frotte les yeux. Il écoute. Ils glissent.",
            "papa|La sieste a failli gagner. Pas le bateau.",
            "narrateur|Le coin. Le grain se rassoit, collé.",
            "maman|Vous avez parlé malgré le sommeil.",
            "enfant-m|Ta phrase m'a réveillé.",
            "enfant-f|La tasse, on l'a laissée. Le doigt, non.",
            "narrateur|Une tasse de dînette veille, au milieu de la table.",
            "narrateur|Le bateau est au phare, un peu de travers, vivant.",
            "narrateur|Sarah appuie son épaule à la sienne, sans parler.",
        ),
        (3, 3, 3): L(
            "narrateur|Le soir, trois assiettes de dînette font un quai, jusqu'à la vitre.",
            "narrateur|Aniss veut servir le grain de carotte, comme un plat.",
            "enfant-f|S'il te plaît, on sert le bateau. Pas le phare.",
            "narrateur|Il repose l'assiette. Ils glissent la coque au coin.",
            "papa|Le banquet est pour ceux qui ont parlé chacun leur tour.",
            "maman|Le soir a tout doré. Le grain aussi.",
            "enfant-m|J'ai posé quand tu as dit.",
            "enfant-f|J'ai dit, et tu as fait.",
            "narrateur|Une assiette vide reflète l'orange minuscule.",
            "narrateur|Le bateau touche le grain. Ça a failli être un dîner.",
            "narrateur|La tasse-lanterne s'éteint, retournée, sur le bois.",
            "narrateur|Le verre garde le voyage, entier, fragile.",
        ),
    }
    return table[(a, b, c)]


ENDS = {
    (1, 1, 1): L(
        "narrateur|Sur le bois, le cube rouge garde une ombre orange.",
        "enfant-m|Le bateau a son phare, ce matin.",
        "papa|Vous avez demandé le chemin, sous la pluie.",
        "maman|La goutte est passée à côté.",
        "narrateur|Sarah pose un doigt, loin, pour ne plus pousser.",
        "narrateur|Le grain de carotte veille au coin, minuscule, gagné.",
    ),
    (1, 1, 2): L(
        "narrateur|Le carré de soleil s'en va. Le quai de cubes reste.",
        "enfant-f|On n'a pas recollé le phare. Il est resté.",
        "papa|Après la sieste, vous n'avez pas foncé.",
        "maman|Le bateau est sous le grain, pas dessus.",
        "narrateur|Aniss essuie ses doigts au torchon, pas au verre.",
        "narrateur|Le grain de carotte, un peu pâle, tient au verre.",
    ),
    (1, 1, 3): L(
        "narrateur|La lampe dore la tour basse, et le coin du verre.",
        "enfant-m|Le rouge a fait de l'ombre, pas un mur.",
        "papa|Le soir a glissé. Vous, non.",
        "maman|Chacun a parlé, puis le bateau a bougé.",
        "narrateur|Un cube garde la chaleur de la lampe, contre le bois.",
        "narrateur|Le grain de carotte brille, comme un tout petit feu.",
    ),
    (1, 2, 1): L(
        "narrateur|La couverture du livre sèche, une goutte au dos.",
        "enfant-f|La page du voyage n'a pas bu la pluie.",
        "papa|Le carton a pris l'eau. Le phare, non.",
        "maman|Ta voile, Sarah, est arrivée jusqu'au bout.",
        "narrateur|Aniss referme le livre sur le bateau de papier.",
        "narrateur|Au verre, le grain de carotte et le bateau de doigt restent.",
    ),
    (1, 2, 2): L(
        "narrateur|Le carton a un pli, souvenir du courant d'air.",
        "enfant-m|Tu as posé le toit. J'ai demandé.",
        "papa|L'air a perdu.",
        "maman|Le livre n'a pas gommé le phare.",
        "narrateur|Sarah lisse la page, loin de la buée.",
        "narrateur|Le grain de carotte tient, juste sous le coin revenu.",
    ),
    (1, 2, 3): L(
        "narrateur|Le livre fermé garde une lueur, sur la table.",
        "enfant-f|On a tourné le toit, pas la vitre.",
        "papa|Le soir a tout allongé. Pas vos mains.",
        "maman|Deux phrases, puis une route.",
        "narrateur|Aniss souffle sur ses doigts, pas sur le grain.",
        "narrateur|Le grain de carotte reste un feu, minuscule, au verre.",
    ),
    (1, 3, 1): L(
        "narrateur|La tasse vide sent l'air de la mer de Sarah.",
        "enfant-m|Ta mer a fini. Mon port a commencé.",
        "papa|La tasse n'a pas lavé le phare.",
        "maman|Vous avez posé, ensemble.",
        "narrateur|Un rond de porcelaine brille, à côté du bois collant.",
        "narrateur|Le grain de carotte, sec, garde le bateau au coin.",
    ),
    (1, 3, 2): L(
        "narrateur|La soucoupe a un halo pâle, où le grain a failli.",
        "enfant-f|Tu as reculé le dock.",
        "papa|Le phare n'est pas un goûter.",
        "maman|Ta peur, Sarah, a été entendue.",
        "narrateur|Aniss range la tasse, lentement, sans cliquetis.",
        "narrateur|Le grain de carotte est rendu au verre, entier.",
    ),
    (1, 3, 3): L(
        "narrateur|Une assiette vide tient un rond de lampe orange.",
        "enfant-m|On n'a pas servi le phare.",
        "papa|Le banquet était pour le bateau.",
        "maman|Parler, puis prendre. Vous l'avez fait.",
        "narrateur|Sarah aligne les assiettes, loin du rebord.",
        "narrateur|Le grain de carotte dore le coin, comme une épice oubliée.",
    ),
    (2, 1, 1): L(
        "narrateur|Une virgule d'eau sèche, sur le seuil du jardin.",
        "enfant-f|On n'a pas frappé, ce matin.",
        "papa|Dedans, le doigt. Dehors, les cubes.",
        "maman|La manche est restée baissée.",
        "narrateur|Les bottes laissent deux ronds sombres, sous le porche.",
        "narrateur|Le grain de carotte, vu des deux côtés, tient au verre.",
    ),
    (2, 1, 2): L(
        "narrateur|Sous le porche, la tour sèche, petite, blanche de soleil.",
        "enfant-m|J'ai visé par ton cube. Pas décroché.",
        "papa|La lunette a suffi.",
        "maman|Le soleil a pressé. Pas vos mains.",
        "narrateur|Sarah pose le cube haut, maintenant, dans le bac.",
        "narrateur|Le grain de carotte, un peu pâle, reste le vrai phare.",
    ),
    (2, 1, 3): L(
        "narrateur|Au jardin, les cubes sombres gardent l'odeur de la pluie.",
        "enfant-f|Ton poing ne s'est pas ouvert sur le verre.",
        "papa|L'étincelle n'avait pas besoin d'un coup.",
        "maman|Le soir a tout rendu fragile. Vous avez ralenti.",
        "narrateur|Aniss essuie une botte, pas la vitre.",
        "narrateur|Le grain de carotte veille, orange, derrière le carreau.",
    ),
    (2, 2, 1): L(
        "narrateur|Le livre sent l'herbe, sur la couverture, ce matin.",
        "enfant-m|J'ai nommé le coin, après toi.",
        "papa|Le papier a eu peur. Vous l'avez entendu.",
        "maman|Dedans, le bateau. Dehors, plus de page.",
        "narrateur|Sarah essuie le dos du livre, au torchon, pas au verre.",
        "narrateur|Le grain de carotte reste, sec, au coin promis.",
    ),
    (2, 2, 2): L(
        "narrateur|Un coin de page reste plié, souvenir du vent.",
        "enfant-f|Tu as pincé le papier, pas la buée.",
        "papa|La carte a survécu.",
        "maman|Le phare n'a pas volé.",
        "narrateur|Aniss lisse le pli, tout bas, loin de la vitre.",
        "narrateur|Le grain de carotte n'a pas quitté son coin.",
    ),
    (2, 2, 3): L(
        "narrateur|Le livre, un peu humide au dos, repose près du pain.",
        "enfant-m|On n'a pas soufflé le phare.",
        "papa|Le doigt, pas le souffle.",
        "maman|Dehors, tu as attendu. Dedans, elle aussi.",
        "narrateur|Sarah pose sa joue un instant, loin du verre froid.",
        "narrateur|Le grain de carotte fait une petite lune, au coin.",
    ),
    (2, 3, 1): L(
        "narrateur|La tasse vide cliquette une dernière fois, au rebord.",
        "enfant-f|Ta mer n'est pas allée sur le bateau.",
        "papa|L'herbe a bu. Le grain, non.",
        "maman|Vous avez versé à la bonne place.",
        "narrateur|Aniss retourne la tasse, enfin muette.",
        "narrateur|Le grain de carotte, sec, garde le bateau au port.",
    ),
    (2, 3, 2): L(
        "narrateur|Dehors, la porcelaine sèche, blanche, sur une pierre.",
        "enfant-m|Le grand phare était un jeu. Le petit, le vrai.",
        "papa|Deux phares. Un voyage.",
        "maman|Ta phrase a choisi, Sarah.",
        "narrateur|Aniss salue la tasse, de loin, sans la reprendre.",
        "narrateur|Le grain de carotte, pâle de soleil, reste au verre.",
    ),
    (2, 3, 3): L(
        "narrateur|La tasse, loin, ne fait plus un bruit.",
        "enfant-f|On a marché pied à pied, ce soir.",
        "papa|Le silence a répondu, d'abord.",
        "maman|Puis vos voix, basses, et le bateau.",
        "narrateur|Aniss pose les mains à plat, sur le bois, content.",
        "narrateur|Le grain de carotte n'a pas sauté. Il veille.",
    ),
    (3, 1, 1): L(
        "narrateur|Une jetée de cubes garde la porte de la cuisine.",
        "enfant-m|Ton capitaine s'est arrêté à temps.",
        "papa|Le chemin, puis le doigt.",
        "maman|Au seuil, vous avez ralenti.",
        "narrateur|Sarah range le cube capitaine, tout contre les autres.",
        "narrateur|Le grain de carotte, au coin, a reçu le bateau.",
    ),
    (3, 1, 2): L(
        "narrateur|Dans la chambre, le bateau sœur reste, volontairement inachevé.",
        "enfant-f|Tu as laissé ma sœur-bateau. Merci.",
        "papa|Un voyage. Un phare.",
        "maman|L'autre verre attendra.",
        "narrateur|Aniss hoche, les oreilles chaudes d'avoir été remercié.",
        "narrateur|Le grain de carotte penche, puis tient, après la sieste.",
    ),
    (3, 1, 3): L(
        "narrateur|Un cube perdu dort au pied du bois, ce soir.",
        "enfant-m|Je ne l'ai pas rattrapé. Le bateau, oui.",
        "papa|La piste avait dit assez.",
        "maman|Ton pied a écouté, Aniss.",
        "narrateur|Sarah éteint le cube capitaine, en le posant à terre.",
        "narrateur|Le grain de carotte, sous la lampe, a son bateau.",
    ),
    (3, 2, 1): L(
        "narrateur|Sur l'oreiller, un X de crayon s'endort, au sec.",
        "enfant-f|Ton œil a visé. Pas la page.",
        "papa|La carte a parlé, puis s'est tue.",
        "maman|Le matin n'a pas collé le papier.",
        "narrateur|Aniss pose le livre sur l'oreiller, loin de la buée.",
        "narrateur|Le grain de carotte, au vrai verre, garde le bateau.",
    ),
    (3, 2, 2): L(
        "narrateur|Sur l'oreiller, la page du port reste ouverte.",
        "enfant-m|J'ai attendu ta ligne. Puis on a couru.",
        "papa|La ligne, puis le doigt.",
        "maman|Le livre a failli vous garder.",
        "narrateur|Sarah tire la couverture, sans fermer l'image.",
        "narrateur|Le grain de carotte tient, un peu gras de buée, au coin.",
    ),
    (3, 2, 3): L(
        "narrateur|Le soir, Aniss raconte enfin le phare, et on l'écoute.",
        "enfant-f|J'ai poussé. Toi, tu parles, maintenant.",
        "papa|Le récit, après le coin. C'est fait.",
        "maman|Toute la phrase, Aniss. On l'a.",
        "narrateur|Le livre, sur le lit, garde l'image. La vitre, le vrai.",
        "narrateur|Le grain de carotte brille, point de lampe, au bateau.",
    ),
    (3, 3, 1): L(
        "narrateur|La tasse vide fait un rond de lumière, sur le bois du matin.",
        "enfant-m|Lanterne à terre. Doigt au verre.",
        "papa|Le port de la chambre a fini.",
        "maman|Vous avez posé, quand il le fallait.",
        "narrateur|Sarah ramène le doudou, sans tasse dessus.",
        "narrateur|Le grain de carotte frôle la coque, enfin arrivée.",
    ),
    (3, 3, 2): L(
        "narrateur|Une tasse veille au milieu de la table, après la sieste.",
        "enfant-f|Tu t'es réveillé pour ma phrase.",
        "papa|Le sommeil a perdu, de peu.",
        "maman|Le bateau est un peu de travers. Tant mieux.",
        "narrateur|Aniss appuie son épaule à celle de Sarah, sans parler.",
        "narrateur|Le grain de carotte s'est rassis, collé, avec son bateau.",
    ),
    (3, 3, 3): L(
        "narrateur|Une assiette reflète l'orange, puis s'éteint avec la tasse.",
        "enfant-m|On a servi le bateau. Pas le phare.",
        "papa|Chacun son tour, jusqu'au coin.",
        "maman|Le soir a doré le grain. Vous aussi, un peu.",
        "narrateur|Sarah retourne la lanterne, pour de bon.",
        "narrateur|Le grain de carotte et le bateau restent, ensemble, au verre.",
    ),
}


def write() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    scripts: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {}

    scripts["CHK_T0000_P0000"] = L(
        "narrateur|Une goutte hésite, en haut de la vitre de la cuisine.",
        "narrateur|Aniss connaît cette pièce, la table, le tic de la gouttière.",
        "narrateur|Un détail paraît nouveau, collé tout en haut, à droite.",
        "narrateur|Un grain de carotte, orange, minuscule, au coin.",
        "papa|Tu as vu ça, Aniss ?",
        "enfant-m|On dirait un phare.",
        "narrateur|Sous le grain, un bateau de doigt attend, inachevé.",
        "narrateur|Sarah arrive, les manches mouillées, le nez luisant.",
        "enfant-f|Je fais la voile !",
        "enfant-m|Non, le bateau, au grain, moi !",
        "narrateur|Aniss pousse trop vite, et la coque s'étale.",
        "narrateur|Le bateau n'atteint pas le coin promis.",
        "narrateur|Sarah n'a pas fini sa phrase.",
        "narrateur|Le sourire d'Aniss n'est plus là.",
        "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        "maman|Tu voulais aller où, tout de suite ?",
        "enfant-m|Jusqu'au grain, avec Sarah, avant la chute.",
        "narrateur|En ce moment, la larme d'eau s'allonge, menaçante.",
        "narrateur|Papa se met à leur hauteur, près du bois collant.",
        "narrateur|Aniss ouvre la bouche, puis la referme.",
        "narrateur|Le silence répond, un instant trop long.",
        "enfant-m|S'il te plaît. Ta voile.",
        "enfant-f|D'accord.",
        "maman|Merci.",
        "maman|Là, j'ai entendu toute la phrase.",
    )
    sons["CHK_T0000_P0000"] = "pluie,vitre"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|Le bateau, le doigt, le grain : rien n'est retiré.",
        "maman|On retente où ? La cuisine, le jardin, ou la chambre ?",
    )
    extras["CHK_T0001_P0000"] = t3labs("la cuisine", "le jardin", "la chambre")
    sons["CHK_T0001_P0000"] = ""

    t1_sons = {1: "vitre,planche", 2: "pluie,porche", 3: "tapis,vitre"}
    t2_sons = {1: "cubes,bois", 2: "livre,pages", 3: "dinette,tasse"}
    t3_sons = {1: "pluie,goutte", 2: "soleil,vitre", 3: "lampe,verre"}
    t2_q = {
        1: L(
            "narrateur|Un objet de la cuisine peut aider, sans pousser trop vite.",
            "papa|Les cubes, le livre, ou la dînette ?",
        ),
        2: L(
            "narrateur|Sous le porche, un objet peut aider à voir, sans frapper.",
            "papa|Les cubes, le livre, ou la dînette ?",
        ),
        3: L(
            "narrateur|Un objet de la chambre peut aider, puis on revient.",
            "papa|Les cubes, le livre, ou la dînette ?",
        ),
    }
    t3_q = {
        1: L(
            "narrateur|La buée de la pluie change, selon l'heure.",
            "maman|Le matin, après la sieste, ou le soir ?",
        ),
        2: L(
            "narrateur|Dehors, la lumière change le grain, et le bateau.",
            "maman|Le matin, après la sieste, ou le soir ?",
        ),
        3: L(
            "narrateur|On revient à la vitre. L'heure change la buée.",
            "maman|Le matin, après la sieste, ou le soir ?",
        ),
    }

    for a in (1, 2, 3):
        p = f"CHK_T0001_P000{a}"
        scripts[p] = T1[a]
        sons[p] = t1_sons[a]
        q_lines, q_fields = Q1[a]
        scripts[f"{p}_Q0001"] = q_lines
        extras[f"{p}_Q0001"] = q_fields
        sons[f"{p}_Q0001"] = ""
        scripts[f"{p}_C0001"] = C1[a]
        sons[f"{p}_C0001"] = ""
        scripts[f"{p}_T0002_P0000"] = t2_q[a]
        extras[f"{p}_T0002_P0000"] = t3labs("les cubes", "le livre", "la dînette")
        sons[f"{p}_T0002_P0000"] = ""
        for b in (1, 2, 3):
            p2 = f"{p}_T0002_P000{b}"
            scripts[p2] = T2[(a, b)]
            sons[p2] = t2_sons[b]
            scripts[f"{p2}_T0003_P0000"] = t3_q[a]
            extras[f"{p2}_T0003_P0000"] = t3labs("le matin", "après la sieste", "le soir")
            sons[f"{p2}_T0003_P0000"] = ""
            for c in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{c}"
                scripts[p3] = t3_lines(a, b, c)
                sons[p3] = t3_sons[c]
                fin = f"{p3}_F0001"
                scripts[fin] = ENDS[(a, b, c)]
                sons[fin] = "vitre,pluie"

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    open_txt = " ".join(ln.split("|", 1)[1] for ln in scripts["CHK_T0000_P0000"])
    if "grain de carotte" not in open_txt.lower():
        raise SystemExit("indice absent à l'ouverture")
    if "en ce moment" not in open_txt.lower():
        raise SystemExit("en ce moment absent à l'ouverture")

    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), 1.22, "medium")
        extra_v: dict = {}
        if kind == "transition_question":
            extra_v["pause_before"] = 200
        voice(nc, profile_for(cid, kind), extra_v)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc

    out = dict(src)
    out["fil_rouge"] = (
        "Sous la pluie, un bateau de doigt attend sur la vitre de la cuisine, "
        "et un grain de carotte sert de phare au coin. Aniss veut le faire glisser "
        "avec Sarah avant que la buée tombe : il pousse trop vite, coupe la voile de Sarah, "
        "le bateau n'atteint pas le coin. Cuisine, jardin ou chambre, cubes, livre ou dînette, "
        "matin, sieste ou soir : la première idée échoue, le grain menace de tomber. "
        "Quand Aniss dit s'il te plaît et écoute, le bateau arrive. Le grain paie le début."
    )
    out["title"] = "Le bateau sur la vitre"
    out["characters"] = "Aniss, Sarah, papa, maman"
    out["setting"] = "maison sous la pluie, cuisine"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    ends = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                cid = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}_F0001"
                ends.append(by[cid]["text"])
                if "grain de carotte" not in by[cid]["text"].lower():
                    raise SystemExit(f"indice non payé: {cid}")
    if len(set(ends)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(ends))}")

    last_imgs = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                cid = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}_F0001"
                lasts = [ln for ln in by[cid]["script"].splitlines() if ln.startswith("narrateur|")]
                last_imgs.append(lasts[-1])
    if len(set(last_imgs)) != 27:
        raise SystemExit(f"dernières images non distinctes: {len(set(last_imgs))}")

    path_words = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                path = [
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
                n = sum(words(by[i]["text"]) for i in path)
                path_words.append(n)
    print(f"chemins {min(path_words)}–{max(path_words)} mots, moy {sum(path_words)//len(path_words)}")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    vecu = (
        "Aniss veut glisser le bateau de doigt jusqu'au grain de carotte, "
        "avec Sarah, avant que la buée tombe. Il pousse trop vite, coupe la voile : "
        "le bateau n'atteint pas le coin. Cuisine (coque étalée), jardin (vitre tapée), "
        "chambre (bateau sœur trop vite) : le choix change l'échec. Cubes, livre ou dînette "
        "menacent le grain ; Aniss refuse de foncer, dit s'il te plaît, écoute Sarah. "
        "Matin, sieste ou soir : le bateau arrive, de peu. Le grain paie l'ouverture. "
        "Un merci adulte, vécu, à l'ouverture."
    )
    notes = (
        "- Titre noyau conservé. Maison sous la pluie, cuisine. "
        "Troupe D16 : Aniss, Sarah, papa, maman. Pas Tom/Léa/Sami.\n"
        "- Labels T1/T2/T3 inchangés (cuisine/jardin/chambre ; cubes/livre/dînette ; "
        "matin/sieste/soir). Graphe `chunk_id` / `kind` inchangés. "
        "Le 1er choix ne retire pas le bateau, le doigt, le grain.\n"
        "- Leçon COL.POL.001 vécue (s'il te plaît / écouter / silence = réponse), jamais dite. "
        "Un merci adulte, une fois, à l'ouverture.\n"
        "- Première idée ratée dès l'ouverture. 2e ruse : le grain glisse, l'objet "
        "(cube, page, tasse) manque de l'emporter. Ils refusent de foncer.\n"
        "- Indice unique dès le début : grain de carotte. Payé aux 27 fins. "
        "27 dernières images distinctes.\n"
        "- Gabarit dump (soupe, épluchure, liste bonjour/s'il te plaît/merci) jeté.\n"
        "- Tics encore/déjà/tout doux/calme et leçon maîtresse retirés.\n"
        f"- Mots par chemin : {min(path_words)}–{max(path_words)} "
        f"(moy {sum(path_words)//len(path_words)})."
    )
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — Le bateau sur la vitre\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        f"## Vécu\n{vecu}\n\n"
        f"## Vu et corrigé\n{notes}\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print("wrote merged.json + RELECTURE.md")


if __name__ == "__main__":
    write()
