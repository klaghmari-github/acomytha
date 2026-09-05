#!/usr/bin/env python3
"""TREE-COL-028 — Le cartable jaune près de la vitre (N2, COL.POL.001)."""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-COL-028"
N2 = LIMITS["N2"]
TITLE = "Le cartable jaune près de la vitre"
FIL = (
    "Nina veut glisser son dessin dans le cartable jaune, près de la vitre embuée, "
    "puis rejoindre le chemin de l'école. Elle tire la courroie sans attendre : "
    "le cartable glisse, personne ne l'entend. Cuisine, jardin ou chambre changent "
    "l'obstacle. Goûter, dessin ou torchon changent ce qu'elle demande. "
    "Matin, sieste ou soir transforment la buée et le jaune du cartable."
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="cartable jaune",
        note="arc=installation; intention=émerveiller; emotion=envie_impatiente; intensite=1; destinataire=enfant; sous_texte=le cartable est là, pas à elle; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_suite_s_ouvre; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="cartable",
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_veut_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_retenue; intensite=2; destinataire=enfant; sous_texte=demander_ouvre_la_main_de_l_autre; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=la_demande_a_changé_le_geste; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="vitre",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_jaune_a_traversé_la_buée; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def L(*rows: str) -> list[str]:
    out: list[str] = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        out.append(f"{role}|{ph}")
    return out


def ssml(text: str, m: dict) -> str:
    body = html.escape(text, quote=False)
    emp = m.get("emphasis")
    if emp and emp in text:
        e = html.escape(emp, quote=False)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
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
    if m.get("pitchTag"):
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    pause = m["pause"]
    suffix = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + suffix).strip()


def voice(nc: dict, profile: str, extra_note: str = "", emphasis: str | None = False) -> None:
    m = dict(PROFILES[profile])
    if emphasis is not False:
        m["emphasis"] = emphasis
    text = nc["text"]
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
    note = m["note"]
    if extra_note:
        note = note + "; " + extra_note
    nc["notes"] = note
    nc["night_policy"] = nc.get("night_policy") or "play"
    nc["locale"] = nc.get("locale") or "fr-FR"
    nc["voice_id"] = nc.get("voice_id") or "fr_FR-siwis-medium"


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str, ok: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
        "engine_ok_text": ok,
        "engine_near_text": "Tu es proche. Écoute l'indice.",
    }


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
    if "_T0003_P000" in cid and cid[-1] in "123":
        return "resolution"
    if "_T0002_P000" in cid and cid[-1] in "123":
        return "obstacle"
    return "action"


# ---------------------------------------------------------------------------
# Récit
# ---------------------------------------------------------------------------

DEBUT = L(
    "narrateur|La maison touche presque le chemin de l'école.",
    "narrateur|Le toit de la classe se devine derrière la haie.",
    "narrateur|Dans la cuisine, la vitre a pris le souffle du cacao.",
    "narrateur|Un cartable jaune s'appuie contre ce verre trouble.",
    "narrateur|On dirait un petit soleil qui n'arrive pas à sortir.",
    "narrateur|Papa pose les clés dans une soucoupe.",
    "narrateur|Elles font un bruit froid.",
    "narrateur|Maman tourne la casserole, près du feu.",
    "narrateur|Ça sent le lait chaud et le pain.",
    "enfant-f|Je veux mon cartable.",
    "enfant-f|Je mets mon dessin dedans.",
    "narrateur|En ce moment, Nina frotte un rond avec sa manche.",
    "narrateur|Le chemin apparaît, brillant comme de l'eau.",
    "narrateur|Elle tire la courroie sans rien dire.",
    "narrateur|Le cartable glisse.",
    "narrateur|La boucle tape les carreaux.",
    "enfant-f|Le cartable !",
    "narrateur|Papa parle à maman du cacao.",
    "narrateur|Leurs voix se mélangent.",
    "narrateur|Personne ne se tourne.",
    "narrateur|Le rond se recouvre de buée.",
    "enfant-f|Ils ne m'ont pas entendue.",
    "maman|Tu disais, Nina ?",
    "papa|On t'écoute, si tu attends un peu.",
)

T1Q = L(
    "narrateur|Nina peut recommencer près de la vitre.",
    "papa|La cuisine, le jardin, ou la chambre ?",
    "maman|Où vas-tu chercher le cartable ?",
)

T1 = {
    1: L(
        "narrateur|Nina revient vers la cuisine.",
        "narrateur|La bouilloire se met à chanter, très fort.",
        "narrateur|Le cartable jaune tremble contre la vitre.",
        "narrateur|Une miette dorée dort près du bol.",
        "enfant-f|Le cartable, vite !",
        "narrateur|Sa voix se casse contre le chant de l'eau.",
        "narrateur|Papa verse le cacao et ne se tourne pas.",
        "narrateur|Nina ouvre la bouche, puis la referme.",
        "narrateur|Elle pose une main sur la table et attend.",
        "narrateur|La bouilloire se tait.",
        "papa|Je t'écoute.",
        "enfant-f|Bonjour, papa.",
        "papa|Bonjour, Nina.",
        "enfant-f|Le cartable, s'il te plaît.",
        "narrateur|Papa décroche la courroie, sans tirer trop fort.",
        "enfant-f|Merci.",
        "maman|Je t'ai entendue jusqu'au bout.",
        "narrateur|La buée garde le rond de sa manche.",
    ),
    2: L(
        "narrateur|Nina pousse la porte du jardin.",
        "narrateur|Les dalles sont mouillées, lisses comme des cuillères.",
        "narrateur|Le cartable pend à un crochet, près de la vitre.",
        "narrateur|Une feuille jaune colle à la courroie.",
        "enfant-f|Je le prends !",
        "narrateur|Elle tire.",
        "narrateur|La feuille glisse.",
        "narrateur|La courroie lui échappe.",
        "narrateur|Nina a les genoux froids sur la pierre.",
        "narrateur|Elle a envie de crier.",
        "narrateur|Papa range un arrosoir, plus loin.",
        "narrateur|Elle attend qu'il pose l'arrosoir.",
        "enfant-f|Bonjour, papa.",
        "papa|Bonjour.",
        "enfant-f|La courroie, s'il te plaît.",
        "papa|La voilà.",
        "enfant-f|Merci.",
        "maman|Tes mains tremblent un peu.",
        "narrateur|Le chemin de l'école brille derrière la haie.",
    ),
    3: L(
        "narrateur|Nina entre dans la chambre.",
        "narrateur|Le cartable jaune est sur la chaise, près de la vitre.",
        "narrateur|Son dessin d'une maison jaune attend sur le lit.",
        "enfant-f|Je le mets dedans.",
        "narrateur|Elle tire la fermeture d'un coup.",
        "narrateur|La fermeture résiste.",
        "narrateur|Le dessin glisse sous le lit.",
        "enfant-f|Non !",
        "narrateur|Maman plie un pull, près de la fenêtre.",
        "narrateur|Nina avale son cri.",
        "narrateur|Elle attend la fin du pli.",
        "enfant-f|Bonjour, maman.",
        "maman|Bonjour, ma Nina.",
        "enfant-f|Le dessin, s'il te plaît.",
        "maman|On le cherchera ensemble.",
        "enfant-f|Merci.",
        "papa|La chaise garde le cartable.",
        "narrateur|Un carré de buée cache le chemin.",
    ),
}

Q1 = {
    1: L(
        "narrateur|Un bruit a couvert la voix de Nina.",
        "maman|Qu'est-ce qui chantait trop fort ?",
    ),
    2: L(
        "narrateur|La courroie a glissé des mains de Nina.",
        "papa|Qu'est-ce qui collait dessus ?",
    ),
    3: L(
        "narrateur|Le papier a disparu d'un coup.",
        "maman|Où le dessin a-t-il glissé ?",
    ),
}

C1 = {
    1: L(
        "enfant-f|La bouilloire !",
        "papa|Oui, elle chantait trop fort.",
        "narrateur|Le cartable jaune est dans les mains de Nina.",
        "narrateur|Il est un peu vide.",
        "maman|Il lui manque quelque chose, tu crois ?",
        "enfant-f|Oui.",
        "narrateur|Une goutte de cacao tache le bol.",
    ),
    2: L(
        "enfant-f|Une feuille !",
        "maman|Oui, une feuille mouillée.",
        "narrateur|Nina tient la courroie contre sa poitrine.",
        "narrateur|Le cartable sent l'herbe.",
        "papa|Il lui manque quelque chose, tu crois ?",
        "enfant-f|Oui.",
        "narrateur|Une dalle sèche au soleil, près du crochet.",
    ),
    3: L(
        "enfant-f|Sous le lit !",
        "papa|Oui, sous le lit.",
        "narrateur|Le cartable reste ouvert sur la chaise.",
        "narrateur|La poche attend le papier.",
        "maman|Il lui manque quelque chose, tu crois ?",
        "enfant-f|Oui.",
        "narrateur|Un fil de poussière danse dans le carré de lumière.",
    ),
}

T2Q = {
    1: L(
        "narrateur|Dans la cuisine, le cartable attend, un peu vide.",
        "papa|Le goûter, le dessin, ou le torchon ?",
        "maman|De quoi a-t-il besoin ?",
    ),
    2: L(
        "narrateur|Dans le jardin, le cartable attend, un peu vide.",
        "maman|Le goûter, le dessin, ou le torchon ?",
        "papa|De quoi a-t-il besoin ?",
    ),
    3: L(
        "narrateur|Dans la chambre, le cartable attend, un peu vide.",
        "papa|Le goûter, le dessin, ou le torchon ?",
        "maman|De quoi a-t-il besoin ?",
    ),
}

T2 = {
    (1, 1): L(
        "narrateur|La boîte du goûter est près de la casserole.",
        "narrateur|Le couvercle est tiède, un peu collant.",
        "enfant-f|Je la prends !",
        "narrateur|Nina avance la main.",
        "narrateur|La chaleur la fait reculer.",
        "narrateur|Maman parle du lait, sans se presser.",
        "narrateur|Nina attend la fin de la phrase.",
        "enfant-f|Le goûter, s'il te plaît.",
        "maman|Le voilà, il a refroidi.",
        "enfant-f|Merci.",
        "papa|Tu as demandé au bon moment.",
        "narrateur|La boîte glisse dans le cartable, toc.",
        "narrateur|Une odeur de cacao reste sur le couvercle.",
    ),
    (1, 2): L(
        "narrateur|Le dessin colle à la vitre de la cuisine.",
        "narrateur|La buée a mouillé un coin de la maison jaune.",
        "enfant-f|Je le décolle !",
        "narrateur|Le papier se froisse.",
        "narrateur|Papa essuie d'abord le bord du verre.",
        "narrateur|Nina serre les lèvres et attend.",
        "enfant-f|Le dessin, s'il te plaît.",
        "papa|Je le décolle par le côté sec.",
        "enfant-f|Merci.",
        "maman|La maison jaune est sauve.",
        "narrateur|Nina glisse le papier dans la poche.",
        "narrateur|Le coin humide laisse une petite fraîcheur.",
    ),
    (1, 3): L(
        "narrateur|Le torchon pend à la porte du four.",
        "narrateur|Il est un peu chaud.",
        "enfant-f|Pour la vitre !",
        "narrateur|Nina le saisit.",
        "narrateur|Ses doigts reculent.",
        "narrateur|Papa finit de poser la casserole.",
        "enfant-f|Le torchon, s'il te plaît.",
        "papa|Attends, je le plie.",
        "papa|Le voilà, plus tiède.",
        "enfant-f|Merci.",
        "maman|Tu vas voir le chemin ?",
        "narrateur|Nina essuie un ovale, lentement.",
        "narrateur|Le toit de la classe redevient net.",
    ),
    (2, 1): L(
        "narrateur|La boîte du goûter est sur la table du jardin.",
        "narrateur|Une goutte brille sur le couvercle.",
        "enfant-f|Je l'essuie !",
        "narrateur|Nina la soulève trop vite.",
        "narrateur|Le couvercle glisse.",
        "papa|J'ai les mains libres.",
        "narrateur|Nina pose la boîte et attend.",
        "enfant-f|Le couvercle, s'il te plaît.",
        "papa|Je le tiens.",
        "enfant-f|Merci.",
        "maman|Le goûter reste au sec.",
        "narrateur|La boîte entre dans le cartable, contre la toile jaune.",
        "narrateur|Une odeur d'herbe reste aux doigts.",
    ),
    (2, 2): L(
        "narrateur|Le dessin tremble au bord de la table du jardin.",
        "narrateur|Un souffle passe dans la haie.",
        "enfant-f|Il va s'envoler !",
        "narrateur|Nina le plaque avec la paume.",
        "narrateur|Maman arrive avec une pince à linge.",
        "narrateur|Nina ne parle pas tout de suite.",
        "enfant-f|La pince, s'il te plaît.",
        "maman|Pour le garder, d'accord.",
        "enfant-f|Merci.",
        "papa|Ensuite, dans la poche.",
        "narrateur|Le papier sent le thym.",
        "narrateur|La maison jaune a une veine d'herbe.",
    ),
    (2, 3): L(
        "narrateur|Un torchon sèche sur la corde, un peu rêche.",
        "narrateur|Le cartable a une courroie humide.",
        "enfant-f|Je l'essuie !",
        "narrateur|Nina tire le torchon.",
        "narrateur|La pince saute.",
        "narrateur|Papa ramasse la pince, sans grogner.",
        "enfant-f|Le torchon, s'il te plaît.",
        "papa|Le voilà, et la pince aussi.",
        "enfant-f|Merci.",
        "maman|La courroie va sécher.",
        "narrateur|Nina frotte le cuir, près du crochet.",
        "narrateur|Le jaune redevient mat, moins froid.",
    ),
    (3, 1): L(
        "narrateur|La boîte du goûter est sous un pull, dans la chambre.",
        "narrateur|Nina soulève le pull d'un coup.",
        "narrateur|Des miettes roulent sur le tapis.",
        "enfant-f|Elle est là !",
        "narrateur|Maman n'a pas fini de plier la manche.",
        "narrateur|Nina pose le pull à plat.",
        "enfant-f|Le goûter, s'il te plaît.",
        "maman|Je le sors sans tout mélanger.",
        "enfant-f|Merci.",
        "papa|Les miettes, on les prend après.",
        "narrateur|La boîte rejoint le cartable, sur la chaise.",
        "narrateur|Le pull garde un creux chaud.",
    ),
    (3, 2): L(
        "narrateur|Nina s'allonge pour voir sous le lit.",
        "narrateur|Le dessin brille, loin, contre une chaussette.",
        "enfant-f|Je le prends !",
        "narrateur|Son bras n'arrive pas.",
        "narrateur|Papa s'accroupit de l'autre côté.",
        "narrateur|Nina retire le bras et attend.",
        "enfant-f|Le dessin, s'il te plaît.",
        "papa|Je le pousse vers toi.",
        "enfant-f|Merci.",
        "maman|Il a un peu de poussière, rien de grave.",
        "narrateur|Nina souffle le papier.",
        "narrateur|La maison jaune retrouve sa place dans la poche.",
    ),
    (3, 3): L(
        "narrateur|Le torchon de la chambre est sur le radiateur.",
        "narrateur|Il est chaud comme un pain.",
        "enfant-f|Pour la vitre !",
        "narrateur|Nina le prend trop vite.",
        "narrateur|Elle le lâche.",
        "narrateur|Maman referme un tiroir, puis se tourne.",
        "enfant-f|Le torchon, s'il te plaît.",
        "maman|Avec le bord le moins chaud.",
        "enfant-f|Merci.",
        "papa|Un ovale suffit, pour voir le chemin.",
        "narrateur|Nina essuie la vitre de la chambre.",
        "narrateur|La haie redevient verte, nette.",
    ),
}

T3Q = {
    1: L(
        "narrateur|Le cartable a ce qu'il fallait.",
        "maman|Le matin, après la sieste, ou le soir ?",
        "papa|Quand part-il, d'après toi ?",
    ),
    2: L(
        "narrateur|Le cartable est presque prêt.",
        "papa|Le matin, après la sieste, ou le soir ?",
        "maman|Quand le vois-tu sur le chemin ?",
    ),
    3: L(
        "narrateur|Le cartable peut attendre, ou partir.",
        "maman|Le matin, après la sieste, ou le soir ?",
        "papa|Quelle lumière veux-tu sur le jaune ?",
    ),
}


def t3_body(i: int, j: int, k: int) -> list[str]:
    key = (i, j, k)
    return T3[key]


T3 = {
    (1, 1, 1): L(
        "narrateur|Le matin pousse un peu de soleil dans la cuisine.",
        "narrateur|Nina enfile le cartable trop vite.",
        "narrateur|La boîte tape son dos.",
        "papa|Une seconde, j'ai les clés.",
        "narrateur|Nina s'arrête au seuil.",
        "enfant-f|Les clés, s'il te plaît.",
        "papa|Les voilà.",
        "enfant-f|Merci.",
        "maman|Le cacao n'a plus de buée.",
        "narrateur|Le rond de manche est devenu une fenêtre.",
        "narrateur|Le chemin attend, clair.",
    ),
    (1, 1, 2): L(
        "narrateur|Après la sieste, la cuisine est tiède et calme.",
        "narrateur|Nina a les joues marquées par l'oreiller.",
        "narrateur|Elle veut la boîte tout de suite.",
        "maman|J'ai une phrase à finir.",
        "narrateur|Nina s'assoit, le cartable sur les genoux.",
        "enfant-f|Le goûter, s'il te plaît.",
        "maman|Il est dans la poche, tu l'as.",
        "enfant-f|Merci.",
        "papa|On le portera plus tard, vers l'école.",
        "narrateur|Un carré de soleil sèche la vitre.",
        "narrateur|La boîte fait un petit toc, au fond.",
    ),
    (1, 1, 3): L(
        "narrateur|Au soir, la lampe allume le jaune du cartable.",
        "narrateur|La soupe fume, et la vitre se trouble.",
        "enfant-f|Je le prépare pour demain.",
        "narrateur|Nina ouvre la boîte sans demander.",
        "narrateur|Une miette tombe.",
        "papa|Je peux t'aider, si tu veux.",
        "enfant-f|S'il te plaît.",
        "papa|On referme ensemble.",
        "enfant-f|Merci.",
        "maman|Demain, le chemin sera là.",
        "narrateur|La lampe fait un soleil dans la buée nouvelle.",
    ),
    (1, 2, 1): L(
        "narrateur|Le matin, Nina veut montrer le dessin par la vitre.",
        "narrateur|Elle lève le papier trop haut.",
        "maman|J'ai les mains dans l'eau.",
        "narrateur|Nina baisse le dessin et attend.",
        "enfant-f|Tu regardes, s'il te plaît ?",
        "maman|Je vois la maison jaune.",
        "enfant-f|Merci.",
        "papa|Dans la poche, et on part.",
        "narrateur|Le toit de la classe est net, au loin.",
        "narrateur|Le papier frotte la toile, un bruit doux.",
    ),
    (1, 2, 2): L(
        "narrateur|Après la sieste, le coin du dessin a séché.",
        "narrateur|Nina veut le lisser d'un coup.",
        "papa|Doucement, le papier est fatigué.",
        "narrateur|Nina pose les deux mains à plat.",
        "enfant-f|Tu m'aides, s'il te plaît ?",
        "papa|Voilà, la maison est droite.",
        "enfant-f|Merci.",
        "maman|On le mettra avant le goûter de l'école.",
        "narrateur|La vitre n'a plus de larmes.",
        "narrateur|Un rond clair reste, comme un secret.",
    ),
    (1, 2, 3): L(
        "narrateur|Le soir, Nina glisse le dessin sous le rabat.",
        "narrateur|La soupe dessine un escargot de buée.",
        "enfant-f|Il va dormir là.",
        "maman|Tu as dit bonjour à la maison jaune ?",
        "enfant-f|Bonjour, maison.",
        "papa|Et pour fermer ?",
        "enfant-f|S'il te plaît, la fermeture.",
        "papa|Merci, Nina.",
        "narrateur|La fermeture chante un petit zzz.",
        "narrateur|L'escargot de buée avance, très lent.",
    ),
    (1, 3, 1): L(
        "narrateur|Le matin, l'ovale essuyé encadre le chemin.",
        "narrateur|Nina veut un ovale plus grand.",
        "narrateur|Le torchon frotte trop vite, la buée revient.",
        "papa|Un petit ovale suffit.",
        "enfant-f|Tu tiens le torchon, s'il te plaît ?",
        "papa|Je tiens, tu guides.",
        "enfant-f|Merci.",
        "maman|Le cartable est prêt, sur le dos.",
        "narrateur|Le jaune passe dans l'ovale, puis dehors.",
        "narrateur|Le torchon reste sur la chaise, un peu jaune.",
    ),
    (1, 3, 2): L(
        "narrateur|Après la sieste, le torchon a séché sur la chaise.",
        "narrateur|La vitre est un miroir calme.",
        "enfant-f|Je la frotte, ou pas ?",
        "maman|Regarde d'abord.",
        "narrateur|Nina regarde.",
        "narrateur|Le chemin est là, sans frotter.",
        "enfant-f|Le cartable, s'il te plaît.",
        "papa|Il t'attend près du bol.",
        "enfant-f|Merci.",
        "narrateur|Le torchon n'a plus rien à faire.",
        "narrateur|Il sent un peu le four.",
    ),
    (1, 3, 3): L(
        "narrateur|Le soir, la buée revient autour d'un ovale propre.",
        "narrateur|Nina pose le torchon trop près de la lampe.",
        "papa|Pas contre la lumière.",
        "enfant-f|Où, s'il te plaît ?",
        "papa|Sur le dossier, ici.",
        "enfant-f|Merci.",
        "maman|Le cartable dort contre la vitre.",
        "narrateur|Le jaune chauffe l'ovale, comme une lune.",
        "narrateur|Dehors, le chemin de l'école est noir et calme.",
    ),
    (2, 1, 1): L(
        "narrateur|Le matin, une dalle sèche sous le crochet.",
        "narrateur|Nina veut courir vers la haie.",
        "narrateur|La boîte tape dans le cartable.",
        "maman|On ferme d'abord.",
        "enfant-f|La fermeture, s'il te plaît.",
        "maman|Zzz, c'est fait.",
        "enfant-f|Merci.",
        "papa|Le chemin brille, on y va.",
        "narrateur|La feuille mouillée reste au crochet, oubliée.",
        "narrateur|Le jaune s'éloigne vers l'école.",
    ),
    (2, 1, 2): L(
        "narrateur|Après la sieste, la table du jardin est sèche.",
        "narrateur|Une abeille tourne autour du thym.",
        "enfant-f|Le goûter, je le sors !",
        "papa|L'abeille d'abord.",
        "narrateur|Nina attend que l'abeille parte.",
        "enfant-f|Je peux, s'il te plaît ?",
        "papa|Oui.",
        "enfant-f|Merci.",
        "maman|On le reportera plus tard.",
        "narrateur|Le couvercle est tiède, plein de soleil.",
        "narrateur|Le cartable jaune fait de l'ombre au thym.",
    ),
    (2, 1, 3): L(
        "narrateur|Le soir, la porte du jardin garde un carré jaune.",
        "narrateur|C'est le cartable, vu de la cuisine.",
        "enfant-f|Il est trop loin.",
        "papa|On le rentre.",
        "enfant-f|S'il te plaît, papa.",
        "papa|Je le décroche.",
        "enfant-f|Merci.",
        "maman|Le goûter reste dedans, pour demain.",
        "narrateur|Le crochet est vide.",
        "narrateur|Une étoile se pose dans une goutte, sur le verre.",
    ),
    (2, 2, 1): L(
        "narrateur|Le matin, le dessin sent le thym dans la poche.",
        "narrateur|Nina veut le montrer à la haie.",
        "maman|Le papier a peur du vent.",
        "enfant-f|Je le garde, s'il te plaît.",
        "maman|Oui, dans la poche.",
        "enfant-f|Merci.",
        "papa|Un oiseau est sur la haie.",
        "narrateur|Nina dit bonjour, très bas, à l'oiseau.",
        "narrateur|Le chemin s'ouvre, une goutte au milieu.",
    ),
    (2, 2, 2): L(
        "narrateur|Après la sieste, le papier a une veine d'herbe sèche.",
        "narrateur|Nina veut la gratter.",
        "papa|Laisse-la, c'est son voyage.",
        "enfant-f|Je le range, s'il te plaît ?",
        "papa|Dans la poche, oui.",
        "enfant-f|Merci.",
        "maman|La vitre de la porte est nette.",
        "narrateur|On voit le banc, puis le chemin.",
        "narrateur|Le cartable attend sur le seuil, chaud.",
    ),
    (2, 2, 3): L(
        "narrateur|Le soir, un papillon frappe le verre de la porte.",
        "narrateur|Nina veut sortir le dessin pour lui.",
        "maman|Le papier reste au chaud.",
        "enfant-f|Bonjour, papillon.",
        "papa|Tu lui parles gentiment.",
        "enfant-f|Le cartable, s'il te plaît.",
        "papa|On le rentre.",
        "enfant-f|Merci.",
        "narrateur|Sous le rabat, le dessin reste à l'abri.",
        "narrateur|Vers la haie noire, le papillon s'en va.",
    ),
    (2, 3, 1): L(
        "narrateur|Le matin, la courroie est sèche, un peu rêche.",
        "narrateur|Nina veut la passer trop vite.",
        "papa|Un bras, puis l'autre.",
        "enfant-f|Tu m'aides, s'il te plaît ?",
        "papa|Le voilà, sur tes épaules.",
        "enfant-f|Merci.",
        "maman|Le torchon reste sur la corde.",
        "narrateur|Le chemin est vide et clair.",
        "narrateur|Le jaune avance entre les dalles.",
    ),
    (2, 3, 2): L(
        "narrateur|Après la sieste, les dalles ne glissent plus.",
        "narrateur|Le torchon est plié sur la marche.",
        "enfant-f|Je le range !",
        "maman|La corde d'abord, ou la marche ?",
        "narrateur|Nina réfléchit.",
        "enfant-f|La marche, s'il te plaît.",
        "maman|D'accord.",
        "enfant-f|Merci.",
        "papa|Le cartable peut attendre à l'ombre.",
        "narrateur|Un lézard part sous la feuille sèche.",
        "narrateur|Le jaune dort contre le mur.",
    ),
    (2, 3, 3): L(
        "narrateur|Le soir, Nina veut un dernier coup de torchon.",
        "narrateur|La vitre de la porte a pris la nuit.",
        "papa|Un petit rond, pas plus.",
        "enfant-f|S'il te plaît, tu tiens le sac ?",
        "papa|Je le tiens.",
        "enfant-f|Merci.",
        "maman|Le crochet est vide, c'est bien.",
        "narrateur|Un rond de lampe reste sur le verre.",
        "narrateur|Le cartable rentre, sentant le jardin.",
    ),
    (3, 1, 1): L(
        "narrateur|Le matin, le pull reste en creux sur le lit.",
        "narrateur|Nina veut le cartable et la boîte, tout de suite.",
        "maman|Les chaussettes d'abord.",
        "narrateur|Nina tapote du pied, puis s'arrête.",
        "enfant-f|Les chaussettes, s'il te plaît.",
        "maman|Les voilà.",
        "enfant-f|Merci.",
        "papa|La chaise est libre, on part.",
        "narrateur|La vitre de la chambre montre le chemin.",
        "narrateur|Le jaune quitte la pièce, un peu lourd.",
    ),
    (3, 1, 2): L(
        "narrateur|Après la sieste, l'oreiller a un creux chaud.",
        "narrateur|Nina cherche la boîte dans le cartable.",
        "papa|Elle est là, écoute.",
        "narrateur|Toc, au fond.",
        "enfant-f|Je la sors, s'il te plaît ?",
        "papa|Oui, pour plus tard.",
        "enfant-f|Merci.",
        "maman|Le soleil tient sur la fermeture.",
        "narrateur|Un grain de poussière brille, puis tombe.",
        "narrateur|Le cartable reste sur la chaise, prêt.",
    ),
    (3, 1, 3): L(
        "narrateur|Le soir, la veilleuse peint le cartable d'or.",
        "narrateur|Nina veut manger une miette du goûter.",
        "maman|C'est pour demain.",
        "enfant-f|Juste une, s'il te plaît ?",
        "maman|Une, d'accord.",
        "enfant-f|Merci.",
        "papa|On referme la boîte.",
        "narrateur|Le verre de la chambre est sombre.",
        "narrateur|Le jaune veille contre la nuit.",
    ),
    (3, 2, 1): L(
        "narrateur|Le matin, une cloche lointaine touche la chambre.",
        "narrateur|Nina serre le dessin contre elle.",
        "papa|Dans la poche, il voyagera mieux.",
        "enfant-f|Tu l'ouvres, s'il te plaît ?",
        "papa|La poche est ouverte.",
        "enfant-f|Merci.",
        "maman|La maison jaune part à l'école.",
        "narrateur|Sous le lit, il n'y a plus de papier.",
        "narrateur|Juste la chaussette, oubliée.",
    ),
    (3, 2, 2): L(
        "narrateur|Après la sieste, le papier est tiède.",
        "narrateur|Des grains de poussière dansent au soleil.",
        "enfant-f|Je le montre à la vitre.",
        "maman|La vitre d'abord, ou la poche ?",
        "narrateur|Nina choisit.",
        "enfant-f|La poche, s'il te plaît.",
        "maman|D'accord.",
        "enfant-f|Merci.",
        "papa|Le cartable est prêt, sur la chaise.",
        "narrateur|La poussière retombe, comme une neige minuscule.",
    ),
    (3, 2, 3): L(
        "narrateur|Le soir, Nina glisse le dessin sous le rabat.",
        "narrateur|Une goutte de buée descend sur le verre.",
        "papa|Il va dormir.",
        "enfant-f|Bonjour, demain.",
        "maman|C'est une jolie façon.",
        "enfant-f|La fermeture, s'il te plaît.",
        "papa|Merci, Nina.",
        "narrateur|Le rabat se ferme sur la maison jaune.",
        "narrateur|Le cartable attend, contre le verre sombre.",
    ),
    (3, 3, 1): L(
        "narrateur|Le matin, le torchon a laissé un ovale en forme de maison.",
        "narrateur|Nina veut le garder en frottant trop.",
        "maman|Si tu frottes, il part.",
        "enfant-f|Je m'arrête.",
        "enfant-f|Le cartable, s'il te plaît.",
        "papa|Sur le dos.",
        "enfant-f|Merci.",
        "narrateur|L'ovale cadre le chemin, net comme un cadre.",
        "narrateur|Le radiateur fait un petit tic, puis se tait.",
    ),
    (3, 3, 2): L(
        "narrateur|Après la sieste, le radiateur fait tic, tic.",
        "narrateur|La vitre est sèche.",
        "narrateur|Le cartable, sur la chaise, ressemble à un chat jaune.",
        "enfant-f|Je le mets ?",
        "papa|Quand tu es prête.",
        "enfant-f|S'il te plaît, tu le tends ?",
        "papa|Le voilà.",
        "enfant-f|Merci.",
        "maman|Le torchon n'a plus besoin de travailler.",
        "narrateur|Un rayon tient sur la boucle, puis glisse.",
    ),
    (3, 3, 3): L(
        "narrateur|Le soir, un ovale de lampe s'assoit sur la vitre.",
        "narrateur|Nina plie le torchon trop vite.",
        "maman|Un pli, puis l'autre.",
        "enfant-f|Tu m'aides, s'il te plaît ?",
        "maman|Voilà.",
        "enfant-f|Merci.",
        "papa|La boucle du cartable a l'air endormie.",
        "narrateur|Le jaune et la lampe se touchent, sans se mêler.",
        "narrateur|Dehors, le chemin de l'école attend demain.",
    ),
}


FINS = {
    (1, 1, 1): L(
        "narrateur|Nina marche sur le chemin, le cartable au dos.",
        "narrateur|La boîte fait un petit toc, à chaque pas.",
        "enfant-f|Il est à moi.",
        "papa|Tu l'as demandé.",
        "maman|Bravo, Nina.",
        "narrateur|Derrière elle, la vitre de la cuisine est nette.",
        "narrateur|Une miette dorée brille sur la boucle.",
        "narrateur|Le rond de manche n'est plus un nuage.",
    ),
    (1, 1, 2): L(
        "narrateur|Nina s'assoit près du bol, le cartable contre elle.",
        "narrateur|La boîte est tiède, au fond.",
        "enfant-f|On partira plus tard.",
        "maman|Oui.",
        "papa|Merci d'avoir attendu.",
        "narrateur|Un carré de soleil a fini de sécher le verre.",
        "narrateur|Plus de voix dans le cacao.",
        "narrateur|Ce jaune-là est devenu mat, paisible.",
    ),
    (1, 1, 3): L(
        "narrateur|La lampe tient le cartable comme un petit soleil.",
        "narrateur|La boîte est refermée, pour demain.",
        "enfant-f|Il va dormir.",
        "papa|Nous aussi.",
        "maman|Merci, Nina.",
        "narrateur|Un soleil de lampe reste dans la buée.",
        "narrateur|La casserole ne chante plus.",
        "narrateur|Le chemin, dehors, est noir et large.",
    ),
    (1, 2, 1): L(
        "narrateur|Sur le chemin, la poche frotte un peu le dos de Nina.",
        "narrateur|Le dessin est là, droit.",
        "enfant-f|La maison jaune vient avec moi.",
        "maman|Je l'ai vue.",
        "papa|Merci de l'avoir glissée sans la froisser.",
        "narrateur|Le toit de la classe grandit.",
        "narrateur|La vitre, derrière, garde un ovale clair.",
        "narrateur|Plus de papier collé au verre.",
    ),
    (1, 2, 2): L(
        "narrateur|Nina pose le cartable près du bol.",
        "narrateur|Le coin du dessin n'est plus mouillé.",
        "enfant-f|Elle est droite, ma maison.",
        "papa|Oui.",
        "maman|Merci d'avoir lissé sans casser.",
        "narrateur|La vitre n'a plus de larmes.",
        "narrateur|Un rond clair reste, comme une fenêtre dans la fenêtre.",
        "narrateur|Le chemin attend, sans se presser.",
    ),
    (1, 2, 3): L(
        "narrateur|Le rabat est fermé sur la maison jaune.",
        "narrateur|L'escargot de buée a fini sa route.",
        "enfant-f|Bonjour, demain.",
        "maman|Oui.",
        "papa|Merci, Nina.",
        "narrateur|La fermeture ne chante plus.",
        "narrateur|Le cartable s'appuie contre la vitre, jaune et chaud.",
        "narrateur|La soupe sent le poivre, près du feu.",
    ),
    (1, 3, 1): L(
        "narrateur|Nina passe l'ovale, le cartable au dos.",
        "narrateur|Le torchon reste sur la chaise, taché d'un peu de jaune.",
        "enfant-f|Je vois le chemin.",
        "papa|Nous aussi.",
        "maman|Merci d'avoir guidé le geste.",
        "narrateur|L'ovale encadre la haie, puis se perd.",
        "narrateur|Le toit de la classe est net.",
        "narrateur|Le cacao n'embue plus rien.",
    ),
    (1, 3, 2): L(
        "narrateur|Nina n'a pas frotté.",
        "narrateur|Le chemin était là, sans elle.",
        "enfant-f|Le torchon se repose.",
        "maman|Oui.",
        "papa|Merci d'avoir regardé d'abord.",
        "narrateur|Le torchon sent le four, sur la chaise.",
        "narrateur|La vitre est un miroir, sans travail.",
        "narrateur|Le cartable attend près du bol, prêt.",
    ),
    (1, 3, 3): L(
        "narrateur|Le torchon est sur le dossier, loin de la lampe.",
        "narrateur|Le cartable dort contre le verre.",
        "enfant-f|Le jaune fait une lune.",
        "papa|Je la vois.",
        "maman|Merci d'avoir posé le tissu ailleurs.",
        "narrateur|La buée tient autour de l'ovale, sans le manger.",
        "narrateur|Le chemin de l'école est une ligne noire.",
        "narrateur|La casserole est vide, tiède.",
    ),
    (2, 1, 1): L(
        "narrateur|Nina marche, la boîte au dos, toc, toc.",
        "narrateur|La feuille reste au crochet, comme un ticket oublié.",
        "enfant-f|Mon cartable ne glisse plus.",
        "papa|La courroie est sèche.",
        "maman|Merci d'avoir fermé avant de courir.",
        "narrateur|Les dalles ne sont plus des cuillères.",
        "narrateur|Le chemin brille, puis devient poussière claire.",
        "narrateur|Le jardin reste derrière, mouillé et calme.",
    ),
    (2, 1, 2): L(
        "narrateur|L'abeille a quitté le thym.",
        "narrateur|Nina tient le cartable à l'ombre du mur.",
        "enfant-f|Le goûter est tiède.",
        "maman|Oui.",
        "papa|Merci d'avoir attendu l'abeille.",
        "narrateur|La table du jardin est sèche, presque blanche.",
        "narrateur|Le couvercle sent l'herbe et le soleil.",
        "narrateur|Le chemin, plus loin, ne dit rien.",
    ),
    (2, 1, 3): L(
        "narrateur|Le cartable est rentré, la boîte dedans.",
        "narrateur|Le crochet de la porte est vide.",
        "enfant-f|Une étoile dans la goutte.",
        "papa|Je la vois.",
        "maman|Merci d'avoir demandé le décrochage.",
        "narrateur|Le carré jaune a quitté la porte.",
        "narrateur|Il est dans la cuisine, près des clés.",
        "narrateur|Le jardin respire, sans le sac.",
    ),
    (2, 2, 1): L(
        "narrateur|Nina marche, le dessin au chaud dans la poche.",
        "narrateur|L'oiseau a quitté la haie.",
        "enfant-f|Je lui ai dit bonjour.",
        "maman|Il a dû entendre.",
        "papa|Merci d'avoir gardé le papier.",
        "narrateur|Une goutte reste au milieu du chemin, puis sèche.",
        "narrateur|Le thym colle aux doigts.",
        "narrateur|Le jaune avance, sans voler.",
    ),
    (2, 2, 2): L(
        "narrateur|La veine d'herbe reste sur le papier, dans la poche.",
        "narrateur|Nina s'assoit sur le seuil.",
        "enfant-f|C'est son voyage.",
        "papa|Oui.",
        "maman|Merci de l'avoir laissée.",
        "narrateur|La vitre de la porte montre le banc, net.",
        "narrateur|Le cartable est chaud, contre la jambe.",
        "narrateur|Le chemin attend, large et pâle.",
    ),
    (2, 2, 3): L(
        "narrateur|Plus de papillon au verre.",
        "narrateur|Contre le carton, le dessin dort.",
        "enfant-f|Bonjour, haie.",
        "maman|Elle ne répond pas, c'est normal.",
        "papa|Merci d'avoir parlé sans ouvrir.",
        "narrateur|Le cartable est dans la maison, sentant le thym.",
        "narrateur|La porte du jardin est noire, un peu froide.",
        "narrateur|Une aile a laissé une poussière d'or, minuscule.",
    ),
    (2, 3, 1): L(
        "narrateur|Nina a le cartable sur les épaules, un bras, puis l'autre.",
        "narrateur|Le torchon flotte un peu, sur la corde.",
        "enfant-f|Ça ne glisse plus.",
        "papa|La courroie est sèche.",
        "maman|Merci d'avoir demandé l'aide.",
        "narrateur|Les dalles sont claires, vides.",
        "narrateur|Le chemin prend le jaune et l'emmène.",
        "narrateur|Le crochet ne pend plus rien.",
    ),
    (2, 3, 2): L(
        "narrateur|Le torchon est sur la marche, plié.",
        "narrateur|Le cartable dort contre le mur, à l'ombre.",
        "enfant-f|Le lézard est parti.",
        "maman|Oui.",
        "papa|Merci d'avoir choisi la marche.",
        "narrateur|Les dalles tiennent les pieds, sans glisser.",
        "narrateur|Une feuille sèche tremble, puis s'arrête.",
        "narrateur|Le jaune du mur est plus pâle que le sac.",
    ),
    (2, 3, 3): L(
        "narrateur|Le cartable rentre, sentant le jardin et le torchon.",
        "narrateur|Un rond de lampe reste sur la porte.",
        "enfant-f|Le crochet est vide.",
        "papa|Oui.",
        "maman|Merci d'avoir tenu le sac.",
        "narrateur|Nina a les doigts un peu rèches, de la toile.",
        "narrateur|La nuit a pris le chemin.",
        "narrateur|Le jaune est à l'intérieur, enfin.",
    ),
    (3, 1, 1): L(
        "narrateur|Nina quitte la chambre, le cartable un peu lourd.",
        "narrateur|Le pull garde son creux, sur le lit.",
        "enfant-f|Les chaussettes sont chaudes.",
        "maman|Oui.",
        "papa|Merci d'avoir attendu.",
        "narrateur|La vitre montre le chemin, sans buée.",
        "narrateur|La chaise est vide, un peu chaude.",
        "narrateur|La boîte tape le dos, toc, vers l'école.",
    ),
    (3, 1, 2): L(
        "narrateur|Nina écoute le toc, au fond du cartable.",
        "narrateur|La boîte est là, pour plus tard.",
        "enfant-f|Je l'ai entendue.",
        "papa|Moi aussi.",
        "maman|Merci d'avoir demandé avant de sortir.",
        "narrateur|L'oreiller reprend sa forme, lentement.",
        "narrateur|Un grain de soleil tient sur la fermeture.",
        "narrateur|La chaise garde le jaune, comme un ami.",
    ),
    (3, 1, 3): L(
        "narrateur|Une miette a goûté le soir, une seule.",
        "narrateur|La boîte est refermée.",
        "enfant-f|Demain.",
        "maman|Demain.",
        "papa|Merci d'avoir refermé.",
        "narrateur|La veilleuse tient le cartable d'or.",
        "narrateur|Le verre de la chambre est une nuit calme.",
        "narrateur|Le pull, sur le lit, n'a plus de secret.",
    ),
    (3, 2, 1): L(
        "narrateur|La cloche lointaine a fini.",
        "narrateur|La maison jaune voyage dans la poche.",
        "enfant-f|Elle n'est plus sous le lit.",
        "papa|Non.",
        "maman|Merci d'avoir demandé la poche.",
        "narrateur|La chaussette reste seule, sous le bois.",
        "narrateur|La chaise est vide.",
        "narrateur|Le chemin entre dans les yeux de Nina, clair.",
    ),
    (3, 2, 2): L(
        "narrateur|La poussière est retombée.",
        "narrateur|Le dessin est dans la poche, tiède.",
        "enfant-f|Pas à la vitre, dans le sac.",
        "maman|Oui.",
        "papa|Merci d'avoir choisi.",
        "narrateur|Le cartable, sur la chaise, a l'air prêt.",
        "narrateur|Un dernier grain brille, puis plus rien.",
        "narrateur|Le chemin, dehors, attend sans frapper au verre.",
    ),
    (3, 2, 3): L(
        "narrateur|Le rabat cache la maison jaune.",
        "narrateur|La goutte de buée a fini sa descente.",
        "enfant-f|Bonjour, demain.",
        "papa|Oui.",
        "maman|Merci, Nina.",
        "narrateur|Le cartable attend contre le verre sombre.",
        "narrateur|La chambre sent le papier et le pull.",
        "narrateur|Sous le lit, il n'y a plus d'aventure.",
    ),
    (3, 3, 1): L(
        "narrateur|L'ovale en forme de maison cadre le chemin.",
        "narrateur|Nina ne frotte plus.",
        "enfant-f|Si je frotte, il part.",
        "maman|Oui.",
        "papa|Merci de t'être arrêtée.",
        "narrateur|Le torchon reste sur le radiateur, inutile.",
        "narrateur|Le cartable quitte la chaise, jaune et net.",
        "narrateur|Le tic du radiateur s'est tu.",
    ),
    (3, 3, 2): L(
        "narrateur|Le cartable n'est plus un chat, il est sur le dos.",
        "narrateur|Le radiateur fait un dernier tic.",
        "enfant-f|Il était prêt.",
        "papa|Oui.",
        "maman|Merci d'avoir demandé qu'on le tende.",
        "narrateur|Le torchon n'a plus de travail.",
        "narrateur|Un rayon a quitté la boucle.",
        "narrateur|La vitre sèche garde le chemin, sans ovale.",
    ),
    (3, 3, 3): L(
        "narrateur|Le torchon est plié, un pli, puis l'autre.",
        "narrateur|La boucle du cartable a l'air endormie.",
        "enfant-f|Le jaune et la lampe se touchent.",
        "maman|Sans se mêler.",
        "papa|Merci, Nina.",
        "narrateur|L'ovale de lampe s'assoit sur la vitre, puis palit.",
        "narrateur|Le chemin de l'école attend demain, invisible.",
        "narrateur|La chambre sent le tissu chaud, plus le soir.",
    ),
}


SONS = {
    "CHK_T0000_P0000": "cacao,vitre",
    "CHK_T0001_P0001": "bouilloire,cacao",
    "CHK_T0001_P0002": "goutte,feuille",
    "CHK_T0001_P0003": "fermeture,tissu",
}

SONS_T2 = {1: "boite", 2: "papier", 3: "tissu"}
SONS_T3 = {1: "pas,porte", 2: "rideau", 3: "lampe,soupe"}
SONS_FIN = {1: "pas,oiseau", 2: "silence,mouche", 3: "lampe,casserole"}

QMETA = {
    1: qf(
        "bouilloire",
        "bouilloire | la bouilloire | l'eau | cacao | casserole",
        "Un bruit a couvert Nina. Qu'est-ce qui chantait ?",
        "Oui, c'était la bouilloire.",
    ),
    2: qf(
        "feuille",
        "feuille | une feuille | la feuille | feuille mouillée",
        "La courroie a glissé. Qu'est-ce qui collait dessus ?",
        "Oui, c'était une feuille.",
    ),
    3: qf(
        "lit",
        "lit | sous le lit | le lit | par terre | dessin",
        "Le papier a disparu. Où le dessin a-t-il glissé ?",
        "Oui, sous le lit.",
    ),
}


def build() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {
        "CHK_T0000_P0000": DEBUT,
        "CHK_T0001_P0000": T1Q,
    }
    sons: dict[str, str] = dict(SONS)
    extras: dict[str, dict] = {
        "CHK_T0001_P0000": t3("la cuisine", "le jardin", "la chambre"),
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = T1[i]
        s[f"{p}_Q0001"] = Q1[i]
        extras[f"{p}_Q0001"] = QMETA[i]
        s[f"{p}_C0001"] = C1[i]
        s[f"{p}_T0002_P0000"] = T2Q[i]
        extras[f"{p}_T0002_P0000"] = t3("le goûter", "le dessin", "le torchon")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = T2[(i, j)]
            sons[p2] = SONS_T2[j]
            s[f"{p2}_T0003_P0000"] = T3Q[j]
            extras[f"{p2}_T0003_P0000"] = t3("le matin", "après la sieste", "le soir")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = t3_body(i, j, k)
                sons[p3] = SONS_T3[k]
                s[f"{p3}_F0001"] = FINS[(i, j, k)]
                sons[f"{p3}_F0001"] = SONS_FIN[k]
    return s, sons, extras


def write_tree(scripts: dict, sons: dict, extras: dict) -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        scale, rate = (1.28, "slow") if kind in ("passage_question", "transition_question") else (1.22, "medium")
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        voice(nc, profile_for(cid, kind), extra_note=f"chunk={cid}")
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = "Nina, papa, maman"
    out["setting"] = "maison au bord du chemin de l'école, vitre embuée, cartable jaune"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "les trois mots",
        "tout doux",
        "tout calme",
        "il faut demander",
        "on doit demander",
        "bravo. tu as",
        "bon travail",
        "papa sourit",
        "maman sourit",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan: {bad}")
    fins = [c["text"] for c in out["chunks"] if c.get("kind") == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"{SID} fins distinctes: {len(set(fins))}/{len(fins)}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    s, n, e = build()
    write_tree(s, n, e)
    relecture(
        SID,
        TITLE,
        "Nina veut le cartable jaune près de la vitre embuée, pour y glisser "
        "son dessin et rejoindre le chemin de l'école. Elle tire sans attendre : "
        "le cartable glisse, la bouilloire, la feuille ou le lit empêchent. "
        "Elle retient sa voix, dit bonjour, s'il te plaît, merci, au moment du besoin. "
        "Cuisine / jardin / chambre, puis goûter / dessin / torchon, "
        "puis matin / sieste / soir. 27 fins : le jaune traverse la buée autrement.",
        "P0 F-NAR-019. N2≤15. COL.POL.001 vécu, pas récité. "
        "Troupe Nina, papa, maman. Monde ≠ TREE-COL-001, ≠ TREE-COL-005, "
        "≠ TREE-COL-024 (rond sur vitre). TTS par fonction (raw.js). "
        "Pas apply. Pas audio. Relu : ouverture, échec, choix qui change l'action, "
        "27 fins textuellement distinctes.",
    )


if __name__ == "__main__":
    main()
