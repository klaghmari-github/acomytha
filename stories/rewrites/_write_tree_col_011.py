#!/usr/bin/env python3
"""TREE-COL-011 — Le toit de la gare de Victorino. F-NAR-019, N2, texte seulement."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, make_chunk, words  # noqa: E402

SID = "TREE-COL-011"
LIM = LIMITS["N2"]
ROLES = {"narrateur", "papa", "maman", "enfant-m", "enfant-f", "copain", "copine"}
TICS = ("tout doux", "tout calme", "on lève la main", "puis on parle", "on va apprendre")
TIC_WORDS = re.compile(r"\b(encore|déjà)\b", re.I)
BAD_IN_TEXT = re.compile(r"\b(tom|léa|lea|sami)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        note="arc=installation; intention=faire_tomber_la_goutte; emotion=envie; intensite=1; destinataire=enfant; sous_texte=le_toit_lache_puis_l_eclat; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_l_eclat; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=il_a_cesse_de_forcer; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=deux_envies_un_seul_lieu; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=le_couvercle_resiste; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=s_il_te_plait_apres_l_eclat; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=l_eclat_paie_le_toit; tempo=posé; sourire=léger; respiration=ample",
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
            if BAD_IN_TEXT.search(part):
                raise SystemExit(f"prénom label: {part}")
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


def emphasis_for(text: str) -> str:
    for w in (
        "éclat de thermos",
        "s'il te plaît",
        "toit de la gare",
        "bac à sable",
        "toboggan",
        "balançoires",
        "thermos",
        "éclat",
    ):
        if w in text:
            return w
    return ""


def voice(nc: dict, name: str, extra: dict | None = None) -> None:
    m = PROFILES[name]
    text = nc["text"]
    emph = (extra or {}).get("emphasis")
    if emph is None:
        emph = emphasis_for(text)
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

OPENING = L(
    "narrateur|Le zinc du toit retient une dernière goutte.",
    "narrateur|Elle hésite, puis lâche.",
    "narrateur|Elle frappe la manche de Victorino, sur le quai.",
    "narrateur|Le sifflet du train coupe la goutte en deux.",
    "papa|Tu as tes chaussettes sèches, Victorino ?",
    "enfant-m|Oui, papa.",
    "narrateur|Papa serre le thermos contre son manteau.",
    "narrateur|Sur le couvercle, un éclat de thermos capte le gris.",
    "narrateur|C'est un petit éclat, couleur de cuivre.",
    "enfant-m|La soupe, pour le parc !",
    "narrateur|En ce moment, le train avale le quai.",
    "narrateur|Le toit de la gare recule dans la vitre.",
    "narrateur|Ça sent le poireau, tout chaud, dans le métal.",
    "maman|On descend au village, près des rails.",
    "enfant-m|Nina m'attend, au parc !",
    "narrateur|Victorino tire le thermos, trop vite.",
    "narrateur|La soupe claque contre le couvercle.",
    "narrateur|Son sourire disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "papa|Attends.",
    "papa|Je m'accroupis.",
    "narrateur|Papa se met à sa hauteur, entre les sièges.",
    "papa|Le parc est là.",
    "papa|La soupe aussi.",
    "enfant-m|Je voulais l'ouvrir, maintenant.",
    "maman|On verra, au parc.",
    "narrateur|L'éclat de thermos tremble, puis se tient.",
)

T1_CHOICE = L(
    "narrateur|Le parc s'ouvre, juste après les rails.",
    "maman|Le bac à sable, le toboggan, ou les balançoires ?",
)

T1 = {
    1: L(
        "narrateur|Le train s'arrête. L'air sent le fer mouillé.",
        "narrateur|Victorino court vers le bac à sable.",
        "narrateur|Nina est là, les deux mains dans le sable froid.",
        "copine|Mon tunnel, jusqu'à la mer !",
        "enfant-m|Le thermos, pour la tour !",
        "narrateur|Deux envies, un seul bac.",
        "narrateur|Il plante le thermos au milieu du tunnel.",
        "copine|Tu casses tout !",
        "narrateur|Du sable entre dans le couvercle.",
        "narrateur|L'éclat de thermos disparaît sous la poussière.",
        "narrateur|Victorino veut crier. Il retient le cri.",
        "narrateur|Papa s'accroupit, à la même hauteur.",
        "papa|Le tunnel de Nina, d'abord ?",
        "enfant-m|Je voulais la tour, tout de suite.",
        "narrateur|Il refuse de replanter le thermos.",
        "narrateur|Il souffle sur l'éclat, sans forcer.",
    ),
    2: L(
        "narrateur|Les marches du toboggan luisent, après la pluie.",
        "narrateur|Nina grimpe, les deux mains sur le métal froid.",
        "copine|Je glisse, maintenant !",
        "enfant-m|La soupe, d'abord !",
        "narrateur|Deux envies, une seule rampe.",
        "narrateur|Victorino pose le thermos pile au milieu, en bas.",
        "copine|Je ne peux plus arriver !",
        "narrateur|Le pied de Nina heurte le couvercle.",
        "narrateur|La soupe claque. L'éclat de thermos penche.",
        "narrateur|Le sourire de Victorino s'efface.",
        "papa|Je m'accroupis.",
        "narrateur|Papa se met à sa hauteur, près de la rampe.",
        "enfant-m|Je voulais l'ouvrir, tout de suite.",
        "narrateur|Il reprend le thermos. Il refuse de le reposer là.",
        "narrateur|L'éclat tremble, un peu de travers.",
    ),
    3: L(
        "narrateur|Les balançoires grincent, près des rails.",
        "narrateur|Nina va, vient, les cheveux au vent du train.",
        "copine|Plus haut !",
        "enfant-m|Tu t'arrêtes, pour la soupe !",
        "narrateur|Deux envies, une seule chaîne.",
        "narrateur|Victorino attrape la chaîne, trop tôt.",
        "copine|Aïe !",
        "narrateur|La balançoire donne un à-coup.",
        "narrateur|Le thermos bascule contre sa hanche.",
        "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        "narrateur|Papa s'accroupit, à la même hauteur.",
        "papa|La chaîne, d'abord ?",
        "enfant-m|Je voulais qu'elle s'arrête.",
        "narrateur|Il lâche. Il refuse de rattraper la chaîne.",
        "narrateur|L'éclat de thermos clignote, contre le ciel.",
    ),
}

T1_Q = {
    1: L(
        "narrateur|Du sable a caché quelque chose, sur le couvercle.",
        "maman|Qu'est-ce qui brille, sous le sable ?",
    ),
    2: L(
        "narrateur|Quelque chose bloquait le bas de la rampe.",
        "papa|Qu'est-ce que Victorino a posé trop tôt ?",
    ),
    3: L(
        "narrateur|Victorino a lâché quelque chose, juste à temps.",
        "maman|Qu'est-ce qu'il a lâché ?",
    ),
}

T1_Q_EXTRA = {
    1: qf(
        "éclat",
        "éclat | l'éclat | éclat de thermos | le éclat | thermos",
        "Ça brille sous le sable, sur le couvercle. Qu'est-ce ?",
    ),
    2: qf(
        "thermos",
        "thermos | le thermos | le couvercle | couvercle",
        "Il l'a posé au milieu, en bas. Qu'est-ce ?",
    ),
    3: qf(
        "chaîne",
        "chaîne | la chaîne | chaines | les chaînes",
        "Il tenait ça, puis il a ouvert les doigts. Qu'est-ce ?",
    ),
}

T1_C = {
    1: L(
        "enfant-m|L'éclat de thermos !",
        "narrateur|Oui, l'éclat, sous le sable.",
        "narrateur|Nina reprend son tunnel, plus bas.",
        "maman|Merci d'avoir soufflé, sans replanter.",
        "enfant-m|Après le tunnel, d'accord.",
        "copine|Après, d'accord.",
        "papa|Le sac s'ouvre, à côté.",
    ),
    2: L(
        "enfant-m|Le thermos !",
        "narrateur|Oui, le thermos, trop au milieu.",
        "narrateur|Nina reprend la rampe, sans se presser.",
        "maman|Merci d'avoir reculé, devant la rampe.",
        "enfant-m|Après ta glisse, d'accord.",
        "copine|Après, d'accord.",
        "papa|Le sac s'ouvre, au pied.",
    ),
    3: L(
        "enfant-m|La chaîne !",
        "narrateur|Oui, la chaîne, trop tôt saisie.",
        "narrateur|Nina finit son va-et-vient, plus lentement.",
        "maman|Merci d'avoir lâché la chaîne.",
        "enfant-m|Après ta balançoire, d'accord.",
        "copine|Après, d'accord.",
        "papa|Le sac s'ouvre, sous le banc.",
    ),
}

T2_CHOICE = {
    1: L(
        "narrateur|Le sac de toile s'ouvre, près du bac.",
        "papa|Les cubes, le livre, ou la dînette ?",
    ),
    2: L(
        "narrateur|Le sac de toile s'ouvre, au pied de la rampe.",
        "papa|Les cubes, le livre, ou la dînette ?",
    ),
    3: L(
        "narrateur|Le sac de toile s'ouvre, sous le banc.",
        "papa|Les cubes, le livre, ou la dînette ?",
    ),
}

T2 = {
    (1, 1): L(
        "narrateur|Victorino sort les cubes, près du bac.",
        "narrateur|Nina veut un mur, pour le tunnel.",
        "copine|Le mur, d'abord !",
        "enfant-m|Une table, pour le thermos !",
        "narrateur|Il empile trop vite. La pile penche.",
        "narrateur|Un cube frappe le couvercle. Le couvercle se bloque.",
        "narrateur|Victorino veut forcer. Il s'arrête.",
        "narrateur|L'éclat de thermos est du mauvais côté.",
        "enfant-m|Je ne force pas.",
        "papa|Tu regardes le couvercle ?",
        "enfant-m|L'éclat, oui.",
        "narrateur|Nina pose son mur, cube après cube.",
        "narrateur|Il attend, les cubes contre son genou.",
        "narrateur|Le thermos reste fermé, lourd, tiède.",
    ),
    (1, 2): L(
        "narrateur|Victorino sort le livre, près du sable.",
        "copine|Le toit de mon tunnel !",
        "enfant-m|La page de la soupe !",
        "narrateur|Deux envies, une seule couverture.",
        "narrateur|Il ouvre trop vite. La page humide colle.",
        "narrateur|Il tire. Le papier crie, tout mince.",
        "narrateur|Il lâche. Il refuse de déchirer.",
        "narrateur|L'éclat de thermos se mire dans le brillant.",
        "papa|La page, ou le tunnel ?",
        "enfant-m|Le tunnel, d'abord.",
        "copine|Après, on ouvre.",
        "narrateur|Nina pose le livre en toit, sans l'enfoncer.",
        "narrateur|Victorino garde le thermos contre lui.",
        "narrateur|La page reste entière, un peu ondulée.",
    ),
    (1, 3): L(
        "narrateur|Victorino sort la dînette, près du bac.",
        "copine|Mes tasses, de sable !",
        "enfant-m|Les tasses, de soupe !",
        "narrateur|Nina remplit une tasse de sable mouillé.",
        "narrateur|Il approche le thermos. Presque trop près.",
        "narrateur|Le couvercle refuse de tourner.",
        "narrateur|Il veut forcer. Il s'arrête.",
        "narrateur|L'éclat de thermos montre l'autre sens.",
        "enfant-m|Pas sur le sable.",
        "maman|Tu attends les vraies tasses ?",
        "enfant-m|Oui.",
        "narrateur|Nina finit sa tasse de sable, toute seule.",
        "narrateur|Il tient la dînette propre, sans verser.",
        "narrateur|Le thermos reste fermé, l'éclat visible.",
    ),
    (2, 1): L(
        "narrateur|Victorino sort les cubes, au pied du toboggan.",
        "copine|Des marches, pour monter plus vite !",
        "enfant-m|Une table, en bas !",
        "narrateur|Nina pose un cube sur une marche.",
        "narrateur|Il tire le cube. Nina bascule un peu.",
        "copine|Hé !",
        "narrateur|Il remet le cube. Il refuse de reprendre.",
        "narrateur|L'éclat de thermos cogne son poignet.",
        "papa|Les marches de Nina, d'abord ?",
        "enfant-m|Oui.",
        "narrateur|Elle pose deux cubes, puis grimpe.",
        "narrateur|Il garde les autres, pour plus tard.",
        "narrateur|Le thermos attend, fermé, contre sa jambe.",
        "narrateur|La rampe reste libre, au milieu.",
    ),
    (2, 2): L(
        "narrateur|Victorino sort le livre, près de la rampe.",
        "copine|Je glisse avec !",
        "enfant-m|On lit, en bas !",
        "narrateur|Nina serre le livre. Elle s'élance.",
        "narrateur|Les pages battent. Une s'envole presque.",
        "narrateur|Il tend la main, puis la retire.",
        "narrateur|Il refuse d'arrêter la glisse.",
        "narrateur|L'éclat de thermos reste sous la couverture.",
        "maman|Tu la laisses arriver ?",
        "enfant-m|Oui.",
        "copine|J'arrive !",
        "narrateur|Le livre atterrit, un peu de travers.",
        "narrateur|Nina souffle. Les pages se calment.",
        "narrateur|Il n'ouvre pas. Pas tout de suite.",
    ),
    (2, 3): L(
        "narrateur|Victorino sort la dînette, au pied du toboggan.",
        "copine|La tasse, c'est un bateau !",
        "enfant-m|C'est pour la soupe !",
        "narrateur|Nina pose une tasse en haut, puis la lâche.",
        "narrateur|La tasse dévale, cliquetante.",
        "narrateur|Il veut barrer la rampe. Il ne barre pas.",
        "narrateur|Il se pousse sur le côté.",
        "narrateur|L'éclat de thermos appuie dans sa paume.",
        "papa|Tu la laisses finir sa course ?",
        "enfant-m|Oui.",
        "narrateur|La tasse s'arrête dans l'herbe, sur le bord.",
        "narrateur|Nina rit. Il ne verse rien.",
        "narrateur|Le thermos reste fermé, lourd, tiède.",
        "narrateur|La rampe redevient vide.",
    ),
    (3, 1): L(
        "narrateur|Victorino sort les cubes, sous les balançoires.",
        "copine|Des copains, sur le siège !",
        "enfant-m|Une table, pour le thermos !",
        "narrateur|Nina pose trois cubes sur l'autre siège.",
        "narrateur|Il avance la main, pour tout enlever.",
        "narrateur|Les cubes vacillent. Il s'arrête.",
        "narrateur|Il refuse de les jeter.",
        "narrateur|L'éclat de thermos tape le bois du siège vide.",
        "maman|Les copains de Nina, d'abord ?",
        "enfant-m|Oui.",
        "narrateur|Elle balance les cubes, sans à-coup.",
        "narrateur|Il attend sur le banc, le thermos fermé.",
        "narrateur|La chaîne de Nina chante, sans à-coup.",
        "narrateur|Son siège à lui reste libre, un moment.",
    ),
    (3, 2): L(
        "narrateur|Victorino sort le livre, sous les balançoires.",
        "copine|Je lis en l'air !",
        "enfant-m|On lit arrêtés !",
        "narrateur|Nina met le livre sur ses genoux.",
        "narrateur|Les pages claquent au vent des rails.",
        "narrateur|Il veut retenir la chaîne. Il n'y touche pas.",
        "narrateur|Ses mains restent sur le thermos.",
        "narrateur|L'éclat cogne un bouton, tout petit.",
        "papa|Tu attends qu'elle pose le livre ?",
        "enfant-m|Oui.",
        "narrateur|Nina ralentit, toute seule.",
        "narrateur|Le livre se repose, un peu froissé.",
        "narrateur|Il n'ouvre pas la page. Pas maintenant.",
        "narrateur|La chaîne se tait, presque.",
    ),
    (3, 3): L(
        "narrateur|Victorino sort la dînette, sous les balançoires.",
        "copine|Le goûter volant !",
        "enfant-m|La vraie soupe !",
        "narrateur|Nina pose deux tasses sur le siège qui bouge.",
        "narrateur|Les tasses dansent. Elles vont tomber.",
        "narrateur|Il lève le thermos. Il le rabaise.",
        "narrateur|Il refuse de verser en l'air.",
        "narrateur|L'éclat de thermos reste contre son pouce.",
        "maman|Tu attends l'arrêt ?",
        "enfant-m|Oui.",
        "narrateur|Nina pose les pieds. Le siège se calme.",
        "narrateur|Les tasses tiennent, vides, un peu froides.",
        "narrateur|Il ne verse pas. Pas tout de suite.",
        "narrateur|La chaîne fait un dernier grincement.",
    ),
}

T3_CHOICE = {
    1: L(
        "narrateur|Un compagnon peut aider, près du bac.",
        "maman|L'ours, le dessin, ou la voix au loin ?",
    ),
    2: L(
        "narrateur|Un compagnon peut aider, près du livre.",
        "maman|L'ours, le dessin, ou la voix au loin ?",
    ),
    3: L(
        "narrateur|Un compagnon peut aider, près des tasses.",
        "maman|L'ours, le dessin, ou la voix au loin ?",
    ),
}

T3 = {
    (1, 1, 1): L(
        "narrateur|Nina pose le dernier cube du mur.",
        "narrateur|Victorino tient l'ours contre le thermos.",
        "enfant-m|Lui, il goûte en premier !",
        "copine|L'ours garde mon tunnel !",
        "narrateur|Deux phrases, un seul ours.",
        "narrateur|Il avance l'ours. Le mur tremble.",
        "narrateur|Un cube tombe. Le thermos penche.",
        "narrateur|Victorino s'arrête. Il refuse de foncer.",
        "narrateur|Il tourne le couvercle vers l'éclat de thermos.",
        "narrateur|Le couvercle cède, sans forcer.",
        "enfant-m|S'il te plaît, un coin, pour la soupe.",
        "copine|Le coin près du bois, pas le tunnel.",
        "narrateur|Il pose le thermos. L'éclat reste visible.",
        "narrateur|Une seconde plus tard, le cube recouvrait tout.",
    ),
    (1, 1, 2): L(
        "narrateur|Nina plante un cube, comme un mât.",
        "narrateur|Victorino sort le dessin d'une fille à tasse.",
        "enfant-m|Elle a une tasse, comme nous !",
        "copine|C'est le drapeau du tunnel !",
        "narrateur|Il veut montrer la tasse. Nina veut le mât.",
        "narrateur|Le papier se plie. Presque trop.",
        "narrateur|Il refuse de l'arracher.",
        "narrateur|L'éclat de thermos luit sur le dessin.",
        "narrateur|Il tourne le couvercle vers cette lueur.",
        "enfant-m|S'il te plaît, un coin, après le drapeau.",
        "copine|Le drapeau, puis le coin.",
        "papa|On t'a entendu, après le mât.",
        "narrateur|La soupe trouve le coin, près du bois.",
        "narrateur|Le dessin reste entier, un peu plié.",
    ),
    (1, 1, 3): L(
        "narrateur|Nina finit le mur. Un sifflet coupe l'air.",
        "narrateur|Une voix de garçon, au loin, réclame le bac.",
        "narrateur|Victorino se lève, presque pour courir.",
        "copine|Mon mur !",
        "enfant-m|J'allais y aller.",
        "narrateur|Il se rassied. Il refuse de foncer.",
        "narrateur|L'éclat de thermos capte le zinc, très loin.",
        "narrateur|Le toit de la gare brille, au-dessus des rails.",
        "narrateur|Il tourne le couvercle vers cette lumière.",
        "enfant-m|S'il te plaît, un coin, ici.",
        "copine|Ici, près du bois.",
        "maman|La voix, elle peut attendre.",
        "narrateur|La soupe pose, tiède, à l'abri du mur.",
        "narrateur|La voix s'éloigne, sans lui.",
    ),
    (1, 2, 1): L(
        "narrateur|Nina a son toit de livre, sur le tunnel.",
        "narrateur|Victorino glisse l'ours sous le bord.",
        "enfant-m|Il lit avec nous !",
        "copine|Il va faire tomber le toit !",
        "narrateur|L'ours pousse. La page humide glisse.",
        "narrateur|Il retire l'ours. Il refuse de pousser.",
        "narrateur|L'éclat de thermos se mire dans l'œil de l'ours.",
        "narrateur|Il tourne le couvercle vers ce petit cuivre.",
        "enfant-m|S'il te plaît, un coin, sous le livre.",
        "copine|Sous le bord, pas au milieu.",
        "papa|Le toit tient.",
        "narrateur|La soupe entre, juste sous la page.",
        "narrateur|Sans l'ours, le livre retombait.",
        "narrateur|L'éclat reste au sec, contre le papier.",
    ),
    (1, 2, 2): L(
        "narrateur|Nina soulève le livre-toit, un instant.",
        "narrateur|Le dessin de la fille à tasse apparaît.",
        "enfant-m|On copie sa tasse !",
        "copine|On referme, le sable entre !",
        "narrateur|Il veut garder la page. Nina veut le toit.",
        "narrateur|Le sable rampe vers le dessin.",
        "narrateur|Il referme, sans tirer.",
        "narrateur|L'éclat de thermos reste dehors, sur le bord.",
        "narrateur|Il tourne le couvercle vers ce bord.",
        "enfant-m|S'il te plaît, un coin, à côté.",
        "copine|À côté, d'accord.",
        "maman|La page est sauvée.",
        "narrateur|La soupe pose hors du tunnel, tiède.",
        "narrateur|Le dessin reste propre, dans le noir du livre.",
    ),
    (1, 2, 3): L(
        "narrateur|Un vent de train soulève le livre-toit.",
        "narrateur|Une voix de garçon, au loin, crie après le vent.",
        "narrateur|Victorino court presque. Nina plaque le livre.",
        "copine|Mon toit !",
        "enfant-m|J'allais le rattraper.",
        "narrateur|Il s'arrête. Il refuse de foncer vers la voix.",
        "narrateur|L'éclat de thermos clignote sous une page.",
        "narrateur|Il tourne le couvercle vers cette lueur.",
        "enfant-m|S'il te plaît, un coin, quand le vent s'arrête.",
        "copine|Il s'arrête.",
        "papa|Le livre est là.",
        "narrateur|La soupe pose, à l'abri, près du bois.",
        "narrateur|La voix se perd dans les rails.",
        "narrateur|Sans ce stop, le livre partait.",
    ),
    (1, 3, 1): L(
        "narrateur|Nina a sa tasse de sable, pleine.",
        "narrateur|Victorino assied l'ours devant la dînette propre.",
        "enfant-m|Lui, il a la vraie !",
        "copine|La mienne, c'est la mer !",
        "narrateur|Il penche le thermos vers l'ours.",
        "narrateur|Une goutte menace la tasse de sable.",
        "narrateur|Il redresse. Il refuse de mélanger.",
        "narrateur|L'éclat de thermos montre le bon sens.",
        "narrateur|Il tourne. Le couvercle s'ouvre, net.",
        "enfant-m|S'il te plaît, une tasse vide.",
        "copine|Celle-là, près de l'ours.",
        "papa|Deux tasses, deux goûters.",
        "narrateur|La soupe tombe dans le propre, pas dans le sable.",
        "narrateur|L'ours a une goutte sur l'oreille, minuscule.",
    ),
    (1, 3, 2): L(
        "narrateur|Nina aligne ses tasses de sable.",
        "narrateur|Victorino pose le dessin de la fille à tasse.",
        "enfant-m|Elle a une vraie, elle !",
        "copine|Les miennes, c'est le port !",
        "narrateur|Il veut verser sur le dessin. Nina recouvre.",
        "narrateur|Le papier tache, presque.",
        "narrateur|Il recule le thermos. Il refuse de tacher.",
        "narrateur|L'éclat de thermos luit au bord d'une tasse vide.",
        "narrateur|Il tourne le couvercle vers ce bord.",
        "enfant-m|S'il te plaît, la tasse vide.",
        "copine|La vide, pas le port.",
        "maman|Le dessin reste clair.",
        "narrateur|La soupe trouve la tasse propre.",
        "narrateur|Une goutte de plus, et la fille disparaissait.",
    ),
    (1, 3, 3): L(
        "narrateur|Les tasses de dînette tintent, trop fort.",
        "narrateur|Une voix de garçon, au loin, imite le tintement.",
        "narrateur|Victorino veut répondre, tasse contre tasse.",
        "copine|Mes tasses à moi !",
        "enfant-m|J'allais jouer avec lui.",
        "narrateur|Il pose les tasses. Il refuse de foncer.",
        "narrateur|L'éclat de thermos se tait dans le silence.",
        "narrateur|Il tourne le couvercle, tout bas.",
        "enfant-m|S'il te plaît, une tasse, pour la soupe.",
        "copine|Une, pas toutes.",
        "papa|On t'entend, sans le tintement.",
        "narrateur|La soupe entre, sans bruit de guerre.",
        "narrateur|La voix au loin s'ennuie, puis part.",
        "narrateur|Sans ce silence, personne n'aurait tendu la tasse.",
    ),
    (2, 1, 1): L(
        "narrateur|Nina a fini ses marches de cubes.",
        "narrateur|Victorino pose l'ours au pied du toboggan.",
        "enfant-m|Il amortit, en bas !",
        "copine|Il va se faire écraser !",
        "narrateur|Il veut laisser l'ours. Nina le tire.",
        "narrateur|L'ours se tord. Le thermos penche.",
        "narrateur|Il recule l'ours. Il refuse de le planter là.",
        "narrateur|L'éclat de thermos capte le métal de la rampe.",
        "narrateur|Il tourne le couvercle vers ce reflet.",
        "enfant-m|S'il te plaît, un coin, à côté de l'herbe.",
        "copine|À côté, pas sur ma piste.",
        "papa|L'ours reste entier.",
        "narrateur|La soupe pose hors de la rampe, tiède.",
        "narrateur|Sans ce recul, l'ours prenait le pied.",
    ),
    (2, 1, 2): L(
        "narrateur|Nina compte ses cubes-marches, tout haut.",
        "narrateur|Victorino montre le dessin : une rampe, une tasse.",
        "enfant-m|Elle glisse, puis elle boit !",
        "copine|Moi, je glisse maintenant !",
        "narrateur|Il barre presque, le dessin en l'air.",
        "narrateur|Nina s'élance. Il se pousse.",
        "narrateur|Il refuse de la stopper.",
        "narrateur|L'éclat de thermos luit après son passage.",
        "narrateur|Il tourne le couvercle, dans ce calme.",
        "enfant-m|S'il te plaît, un coin, maintenant.",
        "copine|Maintenant, oui.",
        "maman|Ta phrase est arrivée après la glisse.",
        "narrateur|La soupe pose au bord, pas sur le métal.",
        "narrateur|Le dessin reste plié, sans froissure.",
    ),
    (2, 1, 3): L(
        "narrateur|Nina est en haut. Une voix de garçon l'appelle.",
        "narrateur|La voix veut la rampe, tout de suite.",
        "narrateur|Victorino lève le thermos, pour dire stop.",
        "copine|C'est mon tour !",
        "enfant-m|J'allais crier.",
        "narrateur|Il baisse le bras. Il refuse de crier.",
        "narrateur|L'éclat de thermos reste dans l'ombre de sa manche.",
        "narrateur|Il attend la fin de la glisse, puis tourne.",
        "enfant-m|S'il te plaît, un coin, à nous.",
        "copine|À nous, après ma glisse.",
        "papa|La voix, elle a entendu l'attente.",
        "narrateur|La soupe pose, hors de la piste.",
        "narrateur|La voix prend un autre jeu, plus loin.",
        "narrateur|Sans cette pause, tout le monde se marchait dessus.",
    ),
    (2, 2, 1): L(
        "narrateur|Nina pose le livre, après sa glisse.",
        "narrateur|Victorino assied l'ours sur la couverture.",
        "enfant-m|Il tourne les pages !",
        "copine|Il va les froisser !",
        "narrateur|L'ours s'appuie. Une page se plie.",
        "narrateur|Il relève l'ours. Il refuse de forcer.",
        "narrateur|L'éclat de thermos passe sous une page, puis revient.",
        "narrateur|Il tourne le couvercle vers cette lueur.",
        "enfant-m|S'il te plaît, on pose la soupe à côté.",
        "copine|À côté du livre, pas dessus.",
        "papa|L'ours a les pattes en l'air, maintenant.",
        "narrateur|La soupe pose dans l'herbe, hors des pages.",
        "narrateur|Sans ce relevé, la page se cassait.",
        "narrateur|L'éclat sèche au vent de la rampe.",
    ),
    (2, 2, 2): L(
        "narrateur|Nina ouvre le livre, à la fille à tasse.",
        "copine|Elle glisse, dans le dessin !",
        "enfant-m|Elle boit, après !",
        "narrateur|Deux lectures, une seule image.",
        "narrateur|Il veut tourner. Nina retient le coin.",
        "narrateur|Le papier crisse. Il lâche le coin.",
        "narrateur|Il refuse de voler la page.",
        "narrateur|L'éclat de thermos se pose sur la tasse dessinée.",
        "narrateur|Il tourne le couvercle vers ce petit cuivre.",
        "enfant-m|S'il te plaît, la soupe, après ta page.",
        "copine|Ma page, puis ta soupe.",
        "maman|Les deux tours, l'un après l'autre.",
        "narrateur|La soupe arrive quand le dessin a fini de glisser.",
        "narrateur|Une seconde trop tôt, la page partait.",
    ),
    (2, 2, 3): L(
        "narrateur|Les pages battent. Une voix de garçon imite le vent.",
        "narrateur|Victorino se tourne vers les rails.",
        "copine|Le livre !",
        "enfant-m|J'écoutais la voix.",
        "narrateur|Une page se lève. Il la plaque, sans crier.",
        "narrateur|Il refuse d'aller vers la voix.",
        "narrateur|L'éclat de thermos clignote entre deux pages.",
        "narrateur|Il tourne le couvercle, tout près du livre.",
        "enfant-m|S'il te plaît, un coin, ici.",
        "copine|Ici, contre le bois.",
        "papa|La voix peut jouer, plus loin.",
        "narrateur|La soupe pose. Les pages se tiennent.",
        "narrateur|La voix s'éloigne le long des rails.",
        "narrateur|Sans la main sur le livre, tout s'envolait.",
    ),
    (2, 3, 1): L(
        "narrateur|La tasse-bateau dort dans l'herbe.",
        "narrateur|Victorino met l'ours à la barre, pour rire.",
        "enfant-m|Il ramène la tasse !",
        "copine|C'est mon bateau !",
        "narrateur|Il pousse l'ours. La tasse roule vers la rampe.",
        "narrateur|Il rattrape, puis s'arrête.",
        "narrateur|Il refuse de renvoyer le bateau.",
        "narrateur|L'éclat de thermos luit dans le creux de la tasse.",
        "narrateur|Il tourne le couvercle vers ce creux.",
        "enfant-m|S'il te plaît, cette tasse, pour la soupe.",
        "copine|Après le bateau, d'accord.",
        "papa|Le bateau a fini sa mer.",
        "narrateur|La soupe entre, sans redescendre la rampe.",
        "narrateur|L'ours a de l'herbe au ventre, rien de plus.",
    ),
    (2, 3, 2): L(
        "narrateur|Nina compare la tasse au dessin de la fille.",
        "copine|La sienne est ronde, comme la mienne !",
        "enfant-m|On verse dans la ronde !",
        "narrateur|Il penche trop tôt. Nina n'a pas fini de comparer.",
        "narrateur|Une goutte tremble au bord.",
        "narrateur|Il redresse. Il refuse de couper sa phrase.",
        "narrateur|L'éclat de thermos attend, au-dessus de la tasse.",
        "narrateur|Quand elle a fini, il tourne vers l'éclat.",
        "enfant-m|S'il te plaît, on verse maintenant.",
        "copine|Maintenant, oui.",
        "maman|Ta demande est arrivée entière.",
        "narrateur|La soupe tombe, ronde, dans la tasse ronde.",
        "narrateur|Le dessin reste sec, sur l'herbe.",
        "narrateur|Sans cette pause, la goutte coupait les mots.",
    ),
    (2, 3, 3): L(
        "narrateur|La tasse roule. Une voix de garçon crie : la mienne.",
        "narrateur|Victorino court presque vers la voix.",
        "copine|C'est ma tasse !",
        "enfant-m|J'allais la lui porter.",
        "narrateur|Il se fige. Il refuse de foncer.",
        "narrateur|L'éclat de thermos capte une goutte de ciel.",
        "narrateur|Le toit de la gare, très loin, rend la même goutte.",
        "narrateur|Il tourne le couvercle vers ces deux lueurs.",
        "enfant-m|S'il te plaît, la tasse, pour nous.",
        "copine|Pour nous, ici.",
        "papa|La voix a d'autres jeux.",
        "narrateur|La soupe entre. La tasse ne reprend pas la rampe.",
        "narrateur|La voix cherche un caillou, plus loin.",
        "narrateur|Sans ce stop, la tasse partait pour de bon.",
    ),
    (3, 1, 1): L(
        "narrateur|Nina balance ses cubes-copains, tout bas.",
        "narrateur|Victorino hisse l'ours sur le siège libre.",
        "enfant-m|Lui, il attend la soupe !",
        "copine|Il va tomber !",
        "narrateur|L'ours glisse. Victorino le rattrape.",
        "narrateur|Il ne le rassied pas de force.",
        "narrateur|Il refuse de foncer vers la chaîne.",
        "narrateur|L'éclat de thermos clignote au creux du siège.",
        "narrateur|Il tourne le couvercle vers ce creux.",
        "enfant-m|S'il te plaît, le siège, pour poser.",
        "copine|Quand mes copains ont fini.",
        "papa|Tes copains ont fini.",
        "narrateur|La soupe pose sur le bois, l'ours à côté.",
        "narrateur|Sans le rattrapage, l'ours prenait la boue.",
    ),
    (3, 1, 2): L(
        "narrateur|Nina aligne les cubes sur le siège.",
        "narrateur|Victorino montre le dessin : une fille, une chaîne.",
        "enfant-m|Elle s'arrête, pour boire !",
        "copine|Moi, je finis mes copains !",
        "narrateur|Il veut poser le thermos. Les cubes occupent tout.",
        "narrateur|Il recule. Il refuse de balayer les cubes.",
        "narrateur|L'éclat de thermos se faufile entre deux bois.",
        "narrateur|Il tourne le couvercle vers cette fente.",
        "enfant-m|S'il te plaît, un bout de siège.",
        "copine|Le bout près de la chaîne fixe.",
        "maman|Les copains ont leur place. Toi, la tienne.",
        "narrateur|La soupe pose sur le bout libre, sans chute.",
        "narrateur|Le dessin reste sur ses genoux, sans tache.",
        "narrateur|Sans ce bout, tout tombait ensemble.",
    ),
    (3, 1, 3): L(
        "narrateur|Une voix de garçon réclame l'autre balançoire.",
        "narrateur|Victorino se lève, le thermos en avant.",
        "copine|Mes cubes !",
        "enfant-m|J'allais lui dire d'attendre.",
        "narrateur|Il se rassied. Il refuse de foncer vers la voix.",
        "narrateur|Les cubes de Nina finissent leur voyage, tout seuls.",
        "narrateur|L'éclat de thermos capte le zinc du toit, très loin.",
        "narrateur|Il tourne le couvercle vers cette lueur de gare.",
        "enfant-m|S'il te plaît, le siège, pour nous.",
        "copine|Pour nous, oui.",
        "papa|La voix a trouvé l'autre chaîne.",
        "narrateur|La soupe pose. Les cubes restent passagers.",
        "narrateur|La voix chante, plus loin, sans les déranger.",
        "narrateur|Sans cette pause, les cubes volaient.",
    ),
    (3, 2, 1): L(
        "narrateur|Nina a posé le livre, les pieds à terre.",
        "narrateur|Victorino met l'ours sur la première page.",
        "enfant-m|Il lit la soupe !",
        "copine|Il cache les mots !",
        "narrateur|L'ours couvre une ligne. Nina fronce le nez.",
        "narrateur|Il retire l'ours. Il refuse de garder la place.",
        "narrateur|L'éclat de thermos glisse en marge, tout cuivre.",
        "narrateur|Il tourne le couvercle vers la marge.",
        "enfant-m|S'il te plaît, la soupe, à côté du livre.",
        "copine|À côté, je vois les mots.",
        "papa|L'ours a sa place, sur le banc.",
        "narrateur|La soupe pose hors des pages, tiède.",
        "narrateur|Sans le retrait, la phrase de Nina restait cachée.",
        "narrateur|L'éclat sèche au vent de la chaîne.",
    ),
    (3, 2, 2): L(
        "narrateur|Nina ouvre le livre, à la fille sur une chaîne.",
        "copine|C'est moi !",
        "enfant-m|Elle s'arrête, pour la tasse !",
        "narrateur|Il veut tourner la page. Nina la plaque.",
        "narrateur|Le papier souffle. Il lâche.",
        "narrateur|Il refuse de voler l'image.",
        "narrateur|L'éclat de thermos se pose sur la tasse dessinée.",
        "narrateur|Il attend la fin de sa phrase, puis tourne le couvercle.",
        "enfant-m|S'il te plaît, on pose la soupe, comme elle.",
        "copine|Comme elle, après ma page.",
        "maman|Ta page, puis sa tasse.",
        "narrateur|La soupe arrive quand le dessin a fini de se balancer.",
        "narrateur|Une page trop tôt, et l'image partait.",
        "narrateur|L'éclat reste au bord, comme un point.",
    ),
    (3, 2, 3): L(
        "narrateur|Le vent des rails feuillette le livre.",
        "narrateur|Une voix de garçon appelle, trop fort.",
        "narrateur|Victorino tourne la tête. Une page s'échappe.",
        "copine|La page !",
        "enfant-m|J'écoutais.",
        "narrateur|Il plaque la page. Il refuse d'aller vers la voix.",
        "narrateur|L'éclat de thermos clignote sous le coin retenu.",
        "narrateur|Il tourne le couvercle, sans quitter le livre.",
        "enfant-m|S'il te plaît, un coin, ici, pour la soupe.",
        "copine|Ici, contre moi.",
        "papa|La voix peut crier, plus loin.",
        "narrateur|La soupe pose. La page reste dans le livre.",
        "narrateur|La voix cherche un caillou, le long des rails.",
        "narrateur|Sans la main, la page prenait le vent.",
    ),
    (3, 3, 1): L(
        "narrateur|Nina a arrêté le siège. Les tasses tiennent.",
        "narrateur|Victorino assied l'ours entre deux tasses.",
        "enfant-m|Il sert !",
        "copine|Il va tout faire tomber !",
        "narrateur|L'ours penche. Une tasse bascule.",
        "narrateur|Il rattrape. Il retire l'ours.",
        "narrateur|Il refuse de le remettre au milieu.",
        "narrateur|L'éclat de thermos luit au fond d'une tasse vide.",
        "narrateur|Il tourne le couvercle vers ce fond.",
        "enfant-m|S'il te plaît, cette tasse, pour la soupe.",
        "copine|Celle de gauche, pas les deux.",
        "papa|L'ours a le banc, les tasses le siège.",
        "narrateur|La soupe entre à gauche, sans chute.",
        "narrateur|Sans le retrait, tout le goûter partait par terre.",
    ),
    (3, 3, 2): L(
        "narrateur|Nina aligne les tasses, comme le dessin.",
        "copine|Un goûter de fille, en l'air !",
        "enfant-m|Un goûter vrai, posé !",
        "narrateur|Il penche le thermos. Le siège avance d'un poil.",
        "narrateur|Il recule. Il refuse de verser en mouvement.",
        "narrateur|L'éclat de thermos attend que le bois se taise.",
        "narrateur|Quand la chaîne se tait, il tourne le couvercle.",
        "enfant-m|S'il te plaît, on verse, maintenant.",
        "copine|Maintenant, c'est calme.",
        "maman|Le dessin, lui, ne verse pas.",
        "narrateur|La soupe tombe droit, dans la tasse du milieu.",
        "narrateur|Le dessin reste sec, sur ses genoux.",
        "narrateur|Une seconde trop tôt, la tasse buvait le ciel.",
        "narrateur|L'éclat se mire dans le rond de soupe.",
    ),
    (3, 3, 3): L(
        "narrateur|Les tasses tintent. Une voix de garçon imite.",
        "narrateur|Victorino lève une tasse, pour répondre.",
        "copine|Mes tasses !",
        "enfant-m|J'allais faire le même bruit.",
        "narrateur|Il repose. Il refuse de foncer vers la voix.",
        "narrateur|L'éclat de thermos se tait dans le silence revenu.",
        "narrateur|Le toit de la gare, au loin, garde une goutte.",
        "narrateur|Il tourne le couvercle vers cette goutte de zinc.",
        "enfant-m|S'il te plaît, une tasse, pour la soupe.",
        "copine|Une, pour nous deux.",
        "papa|La voix a son jeu. Nous, le nôtre.",
        "narrateur|La soupe entre, sans guerre de tintements.",
        "narrateur|La voix s'éloigne le long des rails.",
        "narrateur|Sans ce silence, personne n'aurait tendu la tasse.",
    ),
}

ENDS = {
    (1, 1, 1): L(
        "narrateur|Ils s'assoient près du bac, le mur intact.",
        "narrateur|L'ours a un grain de sable sur l'oreille.",
        "narrateur|Une goutte de soupe tient sur l'éclat de thermos.",
        "papa|Tu le vois, le petit cuivre ?",
        "enfant-m|Il brille.",
        "copine|Mon tunnel va à la mer, tout seul.",
        "maman|On remonte, avant le prochain train ?",
        "enfant-m|Oui.",
        "narrateur|Dans la flaque, le toit de la gare se mire, tout petit.",
        "narrateur|L'éclat répond, cuivre contre zinc.",
    ),
    (1, 1, 2): L(
        "narrateur|Le drapeau de cube tient, un peu de travers.",
        "narrateur|Le dessin a un pli, pas une déchirure.",
        "narrateur|L'éclat de thermos sèche au bord du bois.",
        "papa|Le coin a suffi ?",
        "enfant-m|Oui.",
        "copine|Le tunnel aussi.",
        "maman|On garde le dessin dans le sac ?",
        "enfant-m|Oui, plié comme ça.",
        "narrateur|Une goutte quitte le zinc, très loin.",
        "narrateur|L'éclat la prend, puis la laisse.",
    ),
    (1, 1, 3): L(
        "narrateur|Le mur de cubes garde le vent des rails.",
        "narrateur|La voix s'est tue. Le bac est à eux.",
        "narrateur|L'éclat de thermos capte un bout de toit.",
        "papa|C'était loin, cette voix.",
        "enfant-m|Je suis resté.",
        "copine|Moi aussi.",
        "maman|On reprend le train, les chaussettes sèches ?",
        "enfant-m|Oui.",
        "narrateur|Le zinc du toit, au loin, n'a plus de goutte.",
        "narrateur|L'éclat, lui, en garde une, minuscule.",
    ),
    (1, 2, 1): L(
        "narrateur|Le livre-toit a séché, un peu bosselé.",
        "narrateur|L'ours a la patte propre, hors du sable.",
        "narrateur|L'éclat de thermos reste au sec, contre la page.",
        "papa|La soupe a trouvé sa place ?",
        "enfant-m|Sous le bord.",
        "copine|Mon toit n'est pas tombé.",
        "maman|On rentre, avec le poireau au fond ?",
        "enfant-m|Il reste chaud.",
        "narrateur|Le toit de la gare passe dans un nuage bas.",
        "narrateur|L'éclat le salue, tout cuivre.",
    ),
    (1, 2, 2): L(
        "narrateur|Nina referme le livre. Le dessin dort.",
        "narrateur|Un grain de sable reste dehors, pas dedans.",
        "narrateur|L'éclat de thermos a une ombre de page.",
        "papa|La fille à tasse est au sec ?",
        "enfant-m|Oui.",
        "copine|Le tunnel aussi.",
        "maman|On file, avant la pluie du zinc ?",
        "enfant-m|Oui.",
        "narrateur|Une goutte hésite, sur le toit de la gare.",
        "narrateur|L'éclat, dans la main, ne la reçoit pas.",
    ),
    (1, 2, 3): L(
        "narrateur|Le livre pèse, plein de vent calmé.",
        "narrateur|La voix a pris les rails, sans eux.",
        "narrateur|L'éclat de thermos a un fil de buée, puis plus.",
        "papa|Le toit a tenu ?",
        "enfant-m|On l'a plaqué.",
        "copine|Moi, j'ai tenu le bord.",
        "maman|On remonte, le sac fermé ?",
        "enfant-m|Oui.",
        "narrateur|Le zinc, au loin, rend un dernier éclat.",
        "narrateur|Le leur, sur le couvercle, répond.",
    ),
    (1, 3, 1): L(
        "narrateur|Deux tasses, deux goûters, l'un sable, l'un soupe.",
        "narrateur|L'ours a une goutte sur l'oreille, presque sèche.",
        "narrateur|L'éclat de thermos sent le poireau, tout près.",
        "papa|La vraie tasse était vide ?",
        "enfant-m|Oui.",
        "copine|La mienne, c'est la mer.",
        "maman|On garde l'oreille de l'ours comme ça ?",
        "enfant-m|C'est sa médaille.",
        "narrateur|Le toit de la gare se découpe, net, derrière les arbres.",
        "narrateur|L'éclat le copie, tout petit.",
    ),
    (1, 3, 2): L(
        "narrateur|Le dessin de la fille reste clair, sans tache.",
        "narrateur|La tasse propre a un rond orange, au fond.",
        "narrateur|L'éclat de thermos s'y mire, cuivre dans l'orange.",
        "papa|Une goutte de plus ?",
        "enfant-m|Elle partait sur la fille.",
        "copine|Le port de sable est resté le port.",
        "maman|On rentre, le papier au sec ?",
        "enfant-m|Oui.",
        "narrateur|Une goutte quitte le zinc, ailleurs.",
        "narrateur|Ici, l'éclat reste net.",
    ),
    (1, 3, 3): L(
        "narrateur|Les tasses se taisent. Le bac aussi.",
        "narrateur|La voix a cherché un autre tintement, plus loin.",
        "narrateur|L'éclat de thermos brille, sans bruit.",
        "papa|On t'a entendu, tout bas.",
        "enfant-m|J'ai demandé la tasse.",
        "copine|Une, pas toutes.",
        "maman|On reprend le quai ?",
        "enfant-m|Oui.",
        "narrateur|Le toit de la gare n'a plus de sifflet.",
        "narrateur|L'éclat, lui, garde le silence du goûter.",
    ),
    (2, 1, 1): L(
        "narrateur|L'herbe au pied du toboggan sent le fer.",
        "narrateur|L'ours a le ventre propre, hors de la piste.",
        "narrateur|L'éclat de thermos a pris un reflet de rampe.",
        "papa|Le coin d'herbe a suffi ?",
        "enfant-m|Oui.",
        "copine|Ma piste est libre.",
        "maman|On remonte, avant le long souffle ?",
        "enfant-m|Oui.",
        "narrateur|Le toit de la gare apparaît au bout de la rampe, minuscule.",
        "narrateur|L'éclat le vise, tout cuivre.",
    ),
    (2, 1, 2): L(
        "narrateur|Nina a de la pluie sèche aux genoux.",
        "narrateur|Le dessin de la rampe n'a pas de pli nouveau.",
        "narrateur|L'éclat de thermos sèche au bord, hors du métal.",
        "papa|Ta phrase est arrivée après la glisse ?",
        "enfant-m|Oui.",
        "copine|J'ai glissé, puis j'ai dit oui.",
        "maman|On file, le sac à l'épaule ?",
        "enfant-m|Le thermos est moins lourd.",
        "narrateur|Une goutte ancienne quitte le zinc, très loin.",
        "narrateur|L'éclat ne la rattrape pas. Il n'en a plus besoin.",
    ),
    (2, 1, 3): L(
        "narrateur|La rampe est vide. La voix a changé de jeu.",
        "narrateur|Deux cubes restent, trop petits pour les pieds.",
        "narrateur|L'éclat de thermos a pris la lumière du zinc, très loin.",
        "papa|Tu n'as pas crié ?",
        "enfant-m|Non.",
        "copine|J'ai glissé, sans bousculade.",
        "maman|On reprend le quai, les mains libres ?",
        "enfant-m|Le thermos est moins lourd.",
        "narrateur|Le toit de la gare cligne, au bout des rails.",
        "narrateur|L'éclat cligne avec lui, plus près.",
    ),
    (2, 2, 1): L(
        "narrateur|Le livre a une page un peu pliée, pas cassée.",
        "narrateur|L'ours a les pattes en l'air, hors des mots.",
        "narrateur|L'éclat de thermos sèche au vent de la rampe.",
        "papa|La soupe était à côté ?",
        "enfant-m|Dans l'herbe.",
        "copine|Mes pages sont là.",
        "maman|On remonte, avant le sifflet ?",
        "enfant-m|Oui.",
        "narrateur|Le zinc du toit, au loin, n'a plus rien à lâcher.",
        "narrateur|L'éclat, lui, garde une lueur de page.",
    ),
    (2, 2, 2): L(
        "narrateur|Nina referme le livre, à la fille qui glisse.",
        "narrateur|Un coin de page est chaud, sous son pouce.",
        "narrateur|L'éclat de thermos a un point de soupe, tout rond.",
        "papa|Les deux tours sont passés ?",
        "enfant-m|Sa page, puis ma tasse.",
        "copine|Puis le train.",
        "maman|On file, le dessin au sec ?",
        "enfant-m|Oui.",
        "narrateur|Le toit de la gare se penche dans une flaque.",
        "narrateur|L'éclat le recopie, cuivre sur métal.",
    ),
    (2, 2, 3): L(
        "narrateur|Le livre pèse contre le bois, les pages sages.",
        "narrateur|La voix a pris un caillou, le long des rails.",
        "narrateur|L'éclat de thermos a un fil de vent, puis plus.",
        "papa|Ta main a tenu le coin ?",
        "enfant-m|Oui.",
        "copine|Moi aussi, un peu.",
        "maman|On rentre, le sac fermé ?",
        "enfant-m|Oui.",
        "narrateur|Une goutte ancienne quitte le zinc, ailleurs.",
        "narrateur|Ici, l'éclat reste, collé au couvercle.",
    ),
    (2, 3, 1): L(
        "narrateur|La tasse-bateau a fini sa mer d'herbe.",
        "narrateur|L'ours a de l'herbe au ventre, rien de plus.",
        "narrateur|L'éclat de thermos luit au fond, comme un phare minuscule.",
        "papa|On n'a pas renvoyé le bateau ?",
        "enfant-m|Non.",
        "copine|Il a fini.",
        "maman|On remonte, la tasse rincée plus tard ?",
        "enfant-m|Elle sent le poireau.",
        "narrateur|Le toit de la gare coupe le ciel, net.",
        "narrateur|L'éclat le coupe aussi, tout petit.",
    ),
    (2, 3, 2): L(
        "narrateur|Le dessin de la tasse reste sec, sur l'herbe.",
        "narrateur|La vraie tasse a un rond orange, au fond.",
        "narrateur|L'éclat de thermos s'y mire, puis s'en va.",
        "papa|Sa phrase était finie ?",
        "enfant-m|Oui.",
        "copine|La ronde, comme la mienne.",
        "maman|On file, avant que le métal refroidisse ?",
        "enfant-m|Il est tiède.",
        "narrateur|Le zinc, au loin, n'a plus de goutte à offrir.",
        "narrateur|L'éclat reste, cuivre, sur le doigt.",
    ),
    (2, 3, 3): L(
        "narrateur|La tasse ne reprend pas la rampe.",
        "narrateur|La voix cherche un caillou, plus loin.",
        "narrateur|L'éclat de thermos a deux lueurs, ciel et zinc.",
        "papa|Tu t'es figé, juste à temps ?",
        "enfant-m|Oui.",
        "copine|La tasse est à nous.",
        "maman|On reprend le quai ?",
        "enfant-m|Oui.",
        "narrateur|Le toit de la gare rend la goutte du début.",
        "narrateur|L'éclat la prend, tout petit, puis se tait.",
    ),
    (3, 1, 1): L(
        "narrateur|Le bois du siège sent la chaîne froide.",
        "narrateur|L'ours a un peu de boue évitée, aux pattes.",
        "narrateur|L'éclat de thermos cligne au creux, puis s'endort.",
        "papa|Il allait tomber ?",
        "enfant-m|Je l'ai rattrapé.",
        "copine|Mes copains ont fini.",
        "maman|On remonte, le siège vide ?",
        "enfant-m|Oui.",
        "narrateur|Le toit de la gare se tient, sans goutte.",
        "narrateur|L'éclat se tient avec lui, sur le couvercle.",
    ),
    (3, 1, 2): L(
        "narrateur|Les cubes ont leur place. Le bout de siège aussi.",
        "narrateur|Le dessin n'a pas de tache, sur les genoux.",
        "narrateur|L'éclat de thermos sèche dans la fente du bois.",
        "papa|Le bout libre a suffi ?",
        "enfant-m|Oui.",
        "copine|Mes copains n'ont pas volé.",
        "maman|On file, la chaîne arrêtée ?",
        "enfant-m|Oui.",
        "narrateur|Une lueur de zinc traverse les arbres.",
        "narrateur|L'éclat la prend, tout cuivre.",
    ),
    (3, 1, 3): L(
        "narrateur|Les cubes restent passagers, sages, sur le bois.",
        "narrateur|La voix chante, plus loin, sans les déranger.",
        "narrateur|L'éclat de thermos a gardé le toit, dans sa lueur.",
        "papa|Tu t'es rassis ?",
        "enfant-m|Oui.",
        "copine|Pour nous, le siège.",
        "maman|On reprend le train, les cubes au sac ?",
        "enfant-m|Oui.",
        "narrateur|Le zinc du toit n'appelle plus.",
        "narrateur|L'éclat, lui, reste, collé, tranquille.",
    ),
    (3, 2, 1): L(
        "narrateur|Le livre a ses mots visibles, hors de l'ours.",
        "narrateur|L'ours a le banc, les pattes pendantes.",
        "narrateur|L'éclat de thermos sèche au vent de la chaîne.",
        "papa|La phrase n'était plus cachée ?",
        "enfant-m|Je l'ai retiré.",
        "copine|J'ai vu les mots.",
        "maman|On remonte, le livre fermé ?",
        "enfant-m|Oui.",
        "narrateur|Le toit de la gare passe entre deux nuages.",
        "narrateur|L'éclat le suit, tout petit, sur le métal.",
    ),
    (3, 2, 2): L(
        "narrateur|Nina garde le livre ouvert, un moment.",
        "narrateur|La fille dessinée a fini de se balancer.",
        "narrateur|L'éclat de thermos fait un point, au bord de la page.",
        "papa|Comme elle ?",
        "enfant-m|On a posé, après sa page.",
        "copine|Après ma page.",
        "maman|On file, avant le long souffle ?",
        "enfant-m|Oui.",
        "narrateur|Le zinc, au loin, n'a plus rien à lâcher.",
        "narrateur|L'éclat a son point, et le garde.",
    ),
    (3, 2, 3): L(
        "narrateur|La page est rentrée. Le vent des rails s'est tu.",
        "narrateur|La voix a un caillou, maintenant, pas le livre.",
        "narrateur|L'éclat de thermos cligne sous le coin, puis s'arrête.",
        "papa|Ta main a tenu ?",
        "enfant-m|Oui.",
        "copine|Contre moi.",
        "maman|On rentre, le sac fermé ?",
        "enfant-m|Oui.",
        "narrateur|Le toit de la gare rend une dernière lueur.",
        "narrateur|L'éclat la prend, et la pose sur le couvercle.",
    ),
    (3, 3, 1): L(
        "narrateur|La tasse de gauche a un fond orange, tiède.",
        "narrateur|L'ours a le banc, loin des bords.",
        "narrateur|L'éclat de thermos s'est tu, au fond, comme un secret.",
        "papa|Tout le goûter allait tomber ?",
        "enfant-m|Je l'ai retiré.",
        "copine|Celle de gauche, pas les deux.",
        "maman|On remonte, les tasses au sac ?",
        "enfant-m|Oui.",
        "narrateur|Le zinc du toit se découpe, net, derrière les chaînes.",
        "narrateur|L'éclat le recopie, une dernière fois.",
    ),
    (3, 3, 2): L(
        "narrateur|La tasse du milieu a bu droit, sans ciel.",
        "narrateur|Le dessin reste sec, sur les genoux de Nina.",
        "narrateur|L'éclat de thermos se mire dans le rond de soupe.",
        "papa|Le bois s'était tu ?",
        "enfant-m|Oui.",
        "copine|C'était le moment.",
        "maman|On file, avant que ça refroidisse trop ?",
        "enfant-m|Il reste tiède.",
        "narrateur|Une goutte hésite, très loin, sur le toit de la gare.",
        "narrateur|Ici, l'éclat n'hésite plus.",
    ),
    (3, 3, 3): L(
        "narrateur|Les tasses se taisent. Les chaînes aussi.",
        "narrateur|La voix s'éloigne le long des rails, sans guerre.",
        "narrateur|L'éclat de thermos a pris la goutte de zinc, et la garde.",
        "papa|On a eu notre tasse ?",
        "enfant-m|Une, pour nous deux.",
        "copine|Sans tintement.",
        "maman|On reprend le train, le couvercle fermé ?",
        "enfant-m|Oui.",
        "narrateur|Le toit de la gare, au loin, n'a plus rien à lâcher.",
        "narrateur|Sur le couvercle, l'éclat reste, cuivre, et suffit.",
    ),
}


def write() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    scripts: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {}

    def put(cid: str, lines: list[str], son: str = "") -> None:
        scripts[cid] = lines
        sons[cid] = son

    put("CHK_T0000_P0000", OPENING, "goutte,sifflet,train")
    put("CHK_T0001_P0000", T1_CHOICE, "")
    extras["CHK_T0001_P0000"] = t3labs("le bac à sable", "le toboggan", "les balançoires")

    t1_son = {1: "sable,parc", 2: "metal,parc", 3: "chaine,parc"}
    t2_son = {1: "bois,cubes", 2: "page,livre", 3: "tasse,dinette"}
    t3_son = {1: "tissu,ours", 2: "papier,dessin", 3: "rails,voix"}

    for a in (1, 2, 3):
        p = f"CHK_T0001_P000{a}"
        put(p, T1[a], t1_son[a])
        put(f"{p}_Q0001", T1_Q[a], "")
        extras[f"{p}_Q0001"] = T1_Q_EXTRA[a]
        put(f"{p}_C0001", T1_C[a], t1_son[a])
        put(f"{p}_T0002_P0000", T2_CHOICE[a], "")
        extras[f"{p}_T0002_P0000"] = t3labs("les cubes", "le livre", "la dînette")
        for b in (1, 2, 3):
            sp = f"{p}_T0002_P000{b}"
            put(sp, T2[(a, b)], t2_son[b])
            put(f"{sp}_T0003_P0000", T3_CHOICE[b], "")
            extras[f"{sp}_T0003_P0000"] = t3labs("Tom", "Léa", "Sami")
            for c in (1, 2, 3):
                leaf = f"{sp}_T0003_P000{c}"
                put(leaf, T3[(a, b, c)], t3_son[c])
                put(f"{leaf}_F0001", ENDS[(a, b, c)], "train,thermos")

    by: dict[str, dict] = {}
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
        "Une goutte quitte le zinc du toit de la gare et frappe la manche de Victorino. "
        "Sur le thermos, un éclat de cuivre capte le gris. Il veut offrir la soupe à Nina, "
        "au parc près des rails, avant que le couvercle ne refroidisse. Il tire trop vite, "
        "puis plante, barre ou retient : Nina veut autre chose au même instant. "
        "Quand il refuse de foncer et tourne le couvercle vers l'éclat, "
        "il dit s'il te plaît. L'éclat paie le toit."
    )
    out["title"] = "Le toit de la gare de Victorino"
    out["characters"] = "Victorino, papa, maman, Nina"
    out["setting"] = "gare, train, puis petit parc près des rails"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    ends = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                cid = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}_F0001"
                ends.append(by[cid]["text"])
                if "éclat" not in by[cid]["text"].lower():
                    raise SystemExit(f"{cid}: éclat absent de la fin")
    if len(set(ends)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(ends))}")
    if "éclat" not in by["CHK_T0000_P0000"]["text"].lower():
        raise SystemExit("éclat absent de l'ouverture")

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
        "Victorino veut offrir le thermos de soupe à Nina, au parc près des rails, "
        "avant que le couvercle ne refroidisse. Une goutte quitte le toit de la gare ; "
        "un éclat de thermos capte le gris. Il tire trop vite, puis plante, barre ou retient : "
        "Nina veut le tunnel, la glisse ou la chaîne, pas la soupe au même instant. "
        "Cubes, livre ou dînette changent la ruse (couvercle coincé, page collée, tasse qui dévale). "
        "Ours, dessin ou voix au loin. Il refuse de foncer, tourne vers l'éclat, dit s'il te plaît. "
        "L'éclat paie le zinc du toit."
    )
    notes = (
        "- Titre noyau conservé. Gare réelle, train, parc près des rails "
        "(bac, toboggan, balançoires restent). Troupe D16 : Victorino, Nina, papa, maman.\n"
        "- Labels T1/T2/T3 inchangés (Tom/Léa/Sami = ours / dessin / voix au loin, "
        "jamais dits). Graphe `chunk_id` / `kind` inchangés.\n"
        "- Leçon COL.POL.001 vécue (attendre, tendre, s'il te plaît), jamais listée. "
        "Un merci adulte, vécu, dans les confirmations.\n"
        "- Première idée ratée dès l'ouverture (thermos tiré). Revers allongé au parc "
        "(deux enfants, deux envies).\n"
        "- Indice unique dès le début : éclat de thermos. Payé au climax et aux 27 fins.\n"
        "- 2e ruse : couvercle du mauvais côté, page humide, tasse-bateau, voix au loin. "
        "Victorino refuse de foncer.\n"
        "- 27 fins textuellement distinctes. TTS par fonction (profiles example2).\n"
        "- Tics encore/déjà/tout doux/calme et leçon maîtresse retirés.\n"
        f"- Mots par chemin : {min(path_words)}–{max(path_words)} "
        f"(moy {sum(path_words)//len(path_words)})."
    )
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — Le toit de la gare de Victorino\n\n"
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

