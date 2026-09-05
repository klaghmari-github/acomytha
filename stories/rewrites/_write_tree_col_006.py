#!/usr/bin/env python3
"""TREE-COL-006 — Le rayon du vestiaire de Mila (F-NAR-019, N2, TTS)."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, words  # noqa: E402

SID = "TREE-COL-006"
N2 = LIMITS["N2"]
TITLE = "Le rayon du vestiaire de Mila"
FIL = (
    "Au vestiaire, un manteau trop long cache une fente de lumière. "
    "Mila accroche le sien : un rayon s'ouvre, une virgule d'or flotte. "
    "Elle veut la garder dans son miroir rond avant que le soleil quitte "
    "les manteaux. Nina veut le même crochet pour son ciré jaune, et parler "
    "de la flaque. Leurs voix se cognent. Tapis, table ou fenêtre changent "
    "l'écoute. Histoire, chanson ou dessin changent le désir. Crayon, "
    "coussin ou grelot changent le dernier geste. La virgule d'or paie la fin."
)
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="virgule d'or",
        note="arc=installation; intention=émerveiller; emotion=envie_impatiente; intensite=1; destinataire=enfant; sous_texte=deux_voix_se_cognent_sur_le_même_crochet; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_l_écoute; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_le_geste; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="virgule",
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=une_voix_a_trouvé_un_creux; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="miroir",
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=trop_vite_les_mots_tombent; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="virgule d'or",
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=envie_de_couper_puis_retenue; intensite=2; destinataire=enfant; sous_texte=écouter_ouvre_une_place; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="virgule d'or",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=la_virgule_du_début_revient; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="virgule d'or",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_virgule_a_trouvé_une_place; tempo=posé; sourire=léger; respiration=ample",
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
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        low = ph.lower()
        if "aujourd'hui," in low or "aujourd’hui," in low:
            raise SystemExit(f"aujourd'hui: {ph}")
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


def voice(nc: dict, profile: str, extra_note: str = "", emphasis: str | None | bool = False) -> None:
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
    "narrateur|Le vestiaire sent la laine mouillée, et le savon.",
    "narrateur|Un manteau trop long cache une fente de lumière.",
    "narrateur|Mila connaît chaque crochet, froid et gris.",
    "narrateur|Elle accroche le sien, et la fente s'ouvre.",
    "narrateur|Un rayon passe entre deux manteaux.",
    "narrateur|Dedans, une virgule d'or flotte, minuscule.",
    "narrateur|Le miroir rond de Mila fait clic, dans sa poche.",
    "enfant-f|Je veux la garder, cette virgule, dans le verre.",
    "narrateur|Dehors, une flaque ronde tient un bout de ciel.",
    "narrateur|Un cartable bleu penche, avec une poire en sachet.",
    "narrateur|Le papier du sachet chuchote.",
    "narrateur|Maman plie l'écharpe rouge, un fil d'or au bord.",
    "narrateur|Papa pose le cartable contre le mur.",
    "narrateur|En ce moment, Nina arrive, un ciré jaune au bras.",
    "copine|Ce crochet est à moi !",
    "copine|Il brille !",
    "enfant-f|Non, la virgule d'or d'abord !",
    "narrateur|Leurs deux voix se cognent, trop vite.",
    "narrateur|Personne ne se tourne.",
    "narrateur|Le sourire de Mila disparaît.",
    "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
    "narrateur|Papa s'accroupit, à la hauteur des deux visages.",
    "papa|Vous parlez ensemble.",
    "papa|J'entends un nuage.",
    "maman|Qui veut quoi, en premier ?",
)

T1Q = L(
    "narrateur|Le rayon glisse, lent, vers la classe.",
    "papa|Le tapis, la table, ou la fenêtre ?",
    "maman|Où poses-tu le miroir, maintenant ?",
)

T1 = {
    1: L(
        "narrateur|Le tapis de la classe est gris, un peu rêche.",
        "narrateur|Un carré de soleil s'y pose, chaud.",
        "narrateur|Nina s'assoit pile dans le carré.",
        "copine|C'est ma scène !",
        "enfant-f|Mon miroir, ici !",
        "narrateur|Mila pose le verre trop vite.",
        "narrateur|Nina parle, et les mots de Mila tombent dessus.",
        "narrateur|Le miroir bascule, sans attraper la virgule.",
        "narrateur|Mila ouvre la bouche, puis la referme.",
        "narrateur|Sa main se lève, dans le carré jaune.",
        "narrateur|Elle attend que Nina finisse.",
        "copine|J'ai dit ma scène.",
        "papa|Je t'écoute, Mila.",
        "enfant-f|La virgule d'or, dans le verre.",
        "maman|Merci, j'ai entendu la virgule.",
        "narrateur|Le carré de soleil a glissé d'un poil.",
    ),
    2: L(
        "narrateur|La table de bois est lisse, un peu froide.",
        "narrateur|Une miette de craie dort dans une rainure.",
        "narrateur|Nina tape le bois, toc, toc.",
        "copine|Moi, je fais le tambour !",
        "enfant-f|Le miroir, près de la rainure !",
        "narrateur|Mila parle pendant le toc.",
        "narrateur|Sa phrase se casse.",
        "narrateur|Le miroir tremble, trop près du bord.",
        "narrateur|Mila rentre les mots, les joues chaudes.",
        "narrateur|Elle pose les mains à plat, et attend le silence.",
        "papa|Le toc s'est tu.",
        "papa|Je t'écoute.",
        "enfant-f|Je pose le miroir, sans le toc.",
        "maman|Merci, j'ai eu toute la phrase.",
        "narrateur|La miette de craie reste blanche, dans le bois.",
    ),
    3: L(
        "narrateur|Mila s'approche de la fenêtre.",
        "narrateur|La flaque ronde garde un bout de ciel.",
        "narrateur|Le verre est froid sous ses doigts.",
        "copine|Le ciel est dans l'eau !",
        "enfant-f|La virgule, dans le rayon !",
        "narrateur|Leurs mots se mêlent contre la vitre.",
        "narrateur|Personne n'entend la virgule, ni le ciel.",
        "narrateur|Mila colle le front au verre, puis s'arrête.",
        "narrateur|Elle laisse Nina montrer la flaque.",
        "copine|Tu as vu le nuage rond ?",
        "papa|Oui, Nina.",
        "papa|Mila, à toi.",
        "enfant-f|La virgule d'or danse, là.",
        "maman|Merci, j'ai les deux secrets.",
        "narrateur|Un nuage passe dans la flaque, très lent.",
    ),
}

Q1 = {
    1: L(
        "narrateur|Dans le carré de soleil, une main reste en l'air.",
        "maman|Que lève Mila, pour son tour ?",
    ),
    2: L(
        "narrateur|Près de la rainure, un petit verre se pose.",
        "papa|Que pose Mila, sans le toc ?",
    ),
    3: L(
        "narrateur|Derrière la vitre, l'eau ronde brille.",
        "maman|Que voit-on, dans la flaque ?",
    ),
}

C1 = {
    1: L(
        "narrateur|Sa main est redescendue.",
        "narrateur|Le miroir tient un grain de lumière.",
        "papa|On a entendu la virgule.",
        "enfant-f|Le tapis est chaud, ici.",
        "maman|On continue, par où ?",
        "narrateur|Le carré jaune a bougé, un peu.",
        "narrateur|Nina garde le ciré sur les genoux.",
    ),
    2: L(
        "narrateur|Le miroir tient, loin du toc.",
        "narrateur|La rainure garde sa miette blanche.",
        "papa|On a entendu la phrase entière.",
        "enfant-f|La table est lisse.",
        "maman|On continue, par où ?",
        "narrateur|Le bois sent la craie, très fin.",
        "narrateur|Nina pose les mains à plat, elle aussi.",
    ),
    3: L(
        "narrateur|Deux secrets tiennent, contre le verre.",
        "narrateur|La flaque cligne, puis se tait.",
        "papa|On a le ciel, et la virgule.",
        "enfant-f|Le verre est froid, sous le nez.",
        "maman|On continue, par où ?",
        "narrateur|Un oiseau minuscule traverse la flaque.",
        "narrateur|Nina essuie la buée d'un doigt.",
    ),
}

T2Q = {
    1: L(
        "narrateur|Le tapis garde un peu de soleil.",
        "papa|L'histoire, la chanson, ou le dessin ?",
        "maman|Par quoi commencez-vous, toutes les deux ?",
    ),
    2: L(
        "narrateur|La table a fini son toc.",
        "papa|L'histoire, la chanson, ou le dessin ?",
        "maman|Quel jeu de voix, maintenant ?",
    ),
    3: L(
        "narrateur|La vitre a rendu les deux secrets.",
        "papa|L'histoire, la chanson, ou le dessin ?",
        "maman|Que faites-vous avec le rayon ?",
    ),
}

T2 = {
    (1, 1): L(
        "narrateur|Sur le tapis, un livre s'ouvre, près du carré.",
        "narrateur|Un loup marche dans le bois, sur l'image.",
        "copine|Le loup, c'est moi qui le dis !",
        "enfant-f|La virgule d'or, c'est mon récit !",
        "narrateur|Les deux phrases partent ensemble.",
        "narrateur|La page se referme, comme une bouche.",
        "narrateur|Mila a envie de couper, très fort.",
        "narrateur|Elle rentre les mots.",
        "narrateur|Personne ne donne la suite.",
        "narrateur|Elle écoute le tapis, la laine, le silence.",
        "narrateur|Dans le miroir, la virgule d'or revient.",
        "enfant-f|Toi le loup.",
        "copine|Toi la virgule, après.",
        "papa|J'écoute l'une, puis l'autre.",
        "narrateur|La page se rouvre, sans se battre.",
    ),
    (1, 2): L(
        "narrateur|Sur le tapis, Nina entonne une chanson de pluie.",
        "narrateur|Les mains tapent la laine, toc mou.",
        "enfant-f|Moi, le rayon !",
        "narrateur|Sa voix se perd dans la pluie de Nina.",
        "narrateur|La mélodie se casse, au milieu.",
        "narrateur|Mila serre les lèvres, trop pleine de notes.",
        "narrateur|Elle refuse de foncer.",
        "narrateur|Elle pose le miroir sur ses genoux.",
        "narrateur|La virgule d'or y tremble, la même qu'au vestiaire.",
        "enfant-f|Ta pluie d'abord.",
        "copine|Puis ton rayon.",
        "papa|Je prends les deux chansons, l'une après l'autre.",
        "maman|Le tapis a retenu le rythme.",
        "narrateur|Un petit silence s'ouvre, entre deux tocs.",
        "narrateur|Mila respire, enfin.",
    ),
    (1, 3): L(
        "narrateur|Au milieu du tapis, un grand papier blanc attend.",
        "narrateur|Un soleil à moitié rond y dort, pâle.",
        "copine|Je dessine la flaque !",
        "enfant-f|Moi la virgule !",
        "narrateur|Deux mains partent sur le même blanc.",
        "narrateur|Les traits se croisent, et le papier se plisse.",
        "narrateur|Mila lâche le bord, les doigts chauds.",
        "narrateur|Elle observe le miroir, posé dans le carré.",
        "narrateur|La virgule d'or s'y tient, minuscule.",
        "enfant-f|Toi le rond d'eau.",
        "copine|Toi le trait d'or, à côté.",
        "papa|Deux dessins, une feuille.",
        "maman|Le papier a cessé de plisser.",
        "narrateur|Le soleil pâle a de la place, autour.",
        "narrateur|Mila n'a pas foncé.",
    ),
    (2, 1): L(
        "narrateur|À la table, un livre s'ouvre sur le bois.",
        "narrateur|Le loup marche, et la rainure coupe sa patte.",
        "copine|C'est mon loup !",
        "enfant-f|C'est ma virgule !",
        "narrateur|Nina tape le bois, pour souligner.",
        "narrateur|Le toc mange les mots de Mila.",
        "narrateur|Mila a les joues serrées.",
        "narrateur|Elle pose une main à plat, pour arrêter le toc.",
        "narrateur|Elle attend que le bois se taise.",
        "narrateur|Dans le miroir, près de la miette, l'or revient.",
        "enfant-f|Le loup, toi.",
        "copine|La virgule, toi, après le toc.",
        "papa|J'ai le loup, et j'attends l'or.",
        "maman|La rainure n'a plus volé de phrase.",
        "narrateur|Une page se recourbe, sans bruit.",
    ),
    (2, 2): L(
        "narrateur|À la table, Nina tapote un rythme, toc toc.",
        "narrateur|Elle veut une chanson de tambour.",
        "enfant-f|Moi, une chanson de lumière !",
        "narrateur|Deux airs se cognent sur le bois.",
        "narrateur|Ça fait un bruit laid, trop serré.",
        "narrateur|Mila avale sa note.",
        "narrateur|Elle refuse de chanter par-dessus.",
        "narrateur|Elle écoute le toc jusqu'au bout.",
        "narrateur|Le miroir, près de la rainure, tient la virgule d'or.",
        "enfant-f|Ton tambour.",
        "copine|Ta lumière, après.",
        "papa|Deux chansons, un bois.",
        "maman|Le toc a laissé un creux.",
        "narrateur|Mila pose le miroir, et la note tient.",
        "narrateur|La miette de craie ne bouge plus.",
    ),
    (2, 3): L(
        "narrateur|À la table, un papier blanc glisse vers le bord.",
        "narrateur|La miette de craie laisse un trait pâle.",
        "copine|Ma flaque, ici !",
        "enfant-f|Ma virgule, ici !",
        "narrateur|Le papier part en biais, sous deux mains.",
        "narrateur|Un coin se froisse, près de la rainure.",
        "narrateur|Mila retire sa main, déçue.",
        "narrateur|Elle regarde le miroir, posé loin du toc.",
        "narrateur|La virgule d'or y fait un petit clignement.",
        "enfant-f|Toi le trait pâle.",
        "copine|Toi l'or, de l'autre côté.",
        "papa|La feuille a deux rives, maintenant.",
        "maman|Le bois a cessé de glisser.",
        "narrateur|Mila n'a pas tiré plus fort.",
        "narrateur|Le papier se calme, à plat.",
    ),
    (3, 1): L(
        "narrateur|Près de la fenêtre, le livre s'ouvre.",
        "narrateur|Un reflet de flaque passe sur la page.",
        "copine|Le ciel de l'eau, c'est mon récit !",
        "enfant-f|La virgule du rayon, c'est le mien !",
        "narrateur|Deux récits veulent la même page.",
        "narrateur|Le reflet tremble, et le loup disparaît.",
        "narrateur|Mila a envie de parler plus fort.",
        "narrateur|Elle se tait, le front au verre.",
        "narrateur|Elle écoute la flaque, dehors, plic.",
        "narrateur|Dans le miroir, la virgule d'or revient.",
        "enfant-f|Toi le ciel.",
        "copine|Toi l'or, après le plic.",
        "papa|J'écoute le plic, puis l'or.",
        "maman|La page a retrouvé le loup.",
        "narrateur|Le nuage de la flaque a bougé.",
    ),
    (3, 2): L(
        "narrateur|Près de la fenêtre, une chanson commence.",
        "narrateur|Nina chante la pluie d'hier, contre le verre.",
        "enfant-f|Moi, le rayon !",
        "narrateur|Sa voix se mêle à la pluie, trop tôt.",
        "narrateur|La vitre vibre, un drôle de chant.",
        "narrateur|Mila serre le miroir, les dents un peu dures.",
        "narrateur|Elle refuse de foncer.",
        "narrateur|Elle laisse la pluie finir sa phrase.",
        "narrateur|La virgule d'or cligne, dans le verre du miroir.",
        "enfant-f|Ta pluie.",
        "copine|Ton rayon, après.",
        "papa|La vitre a cessé de vibrer.",
        "maman|Deux chansons, un rebord.",
        "narrateur|Un oiseau minuscule passe dans la flaque.",
        "narrateur|Mila pose le miroir, et chante dans le creux.",
    ),
    (3, 3): L(
        "narrateur|Près de la fenêtre, un papier attend.",
        "narrateur|Le verre jette un rond clair sur le blanc.",
        "copine|Je prends le rond !",
        "enfant-f|Je prends l'or !",
        "narrateur|Deux crayons n'y sont pas, mais deux mains oui.",
        "narrateur|Le papier se colle à la vitre, un instant.",
        "narrateur|La buée mange le rond.",
        "narrateur|Mila recule, le cœur serré.",
        "narrateur|Elle observe le miroir, contre le rebord.",
        "narrateur|La virgule d'or s'y tient, nette.",
        "enfant-f|Toi le rond d'eau.",
        "copine|Toi le trait, à côté du rond.",
        "papa|La buée a séché, un peu.",
        "maman|Le papier a quitté le verre.",
        "narrateur|Mila n'a pas collé plus fort.",
    ),
}

T3Q = {
    1: L(
        "narrateur|Le livre attend un geste, pour tenir.",
        "papa|Le crayon, le coussin, ou le grelot ?",
        "maman|Quel objet, pour la suite ?",
    ),
    2: L(
        "narrateur|La chanson a un trou, au milieu.",
        "papa|Le crayon, le coussin, ou le grelot ?",
        "maman|Quel objet, pour le creux ?",
    ),
    3: L(
        "narrateur|Le papier blanc attend une main.",
        "papa|Le crayon, le coussin, ou le grelot ?",
        "maman|Quel objet, pour le blanc ?",
    ),
}

T3 = {
    (1, 1, 1): L(
        "narrateur|Sur le tapis, le crayon jaune attend près du livre.",
        "enfant-f|Je dessine la virgule !",
        "copine|Non, le loup d'abord !",
        "narrateur|Deux mains saisissent le bois en même temps.",
        "narrateur|Le crayon file, roule hors du carré de soleil.",
        "narrateur|Le sourire de Mila ne revient pas.",
        "narrateur|Elle refuse de foncer.",
        "narrateur|Elle ouvre le miroir, lentement.",
        "narrateur|La virgule d'or y tremble, la même qu'au vestiaire.",
        "enfant-f|Toi le loup.",
        "enfant-f|Moi la virgule, après.",
        "copine|D'accord.",
        "papa|Je vous entends, l'une après l'autre.",
        "narrateur|Le crayon revient, tiède, avec une trace d'or.",
    ),
    (1, 1, 2): L(
        "narrateur|Un coussin bleu dort sur le tapis, près du livre.",
        "copine|C'est ma place pour le loup !",
        "enfant-f|C'est ma place pour l'or !",
        "narrateur|Elles s'assoient ensemble, trop vite.",
        "narrateur|Le coussin glisse, et la page se ferme.",
        "narrateur|Mila a un creux dans la poitrine.",
        "narrateur|Elle se relève, sans tirer.",
        "narrateur|Sur la laine du coussin, un grain d'or brille.",
        "narrateur|C'est la virgule du vestiaire.",
        "enfant-f|Toi d'abord, pour le loup.",
        "copine|Toi après, pour l'or.",
        "maman|Deux places, un coussin.",
        "papa|Je vois le grain, sur le bleu.",
        "narrateur|Le livre reste ouvert, entre leurs genoux.",
    ),
    (1, 1, 3): L(
        "narrateur|Un grelot d'argent attend près du loup.",
        "enfant-f|Je sonne, c'est mon tour !",
        "copine|Non, moi !",
        "narrateur|Deux mains secouent le métal ensemble.",
        "narrateur|Le ding couvre le mot loup, et le mot or.",
        "narrateur|Mila lâche le grelot, les oreilles trop pleines.",
        "narrateur|Elle refuse de sonner par-dessus.",
        "narrateur|Sur le métal, une virgule d'or s'est posée.",
        "enfant-f|Un ding pour toi.",
        "copine|Un ding pour toi, après.",
        "papa|J'ai entendu le loup, puis l'or.",
        "maman|Le grelot s'est tu, entre les deux.",
        "narrateur|La page du loup reste ouverte, un moment.",
        "narrateur|Mila pose le miroir, à côté du métal.",
    ),
    (1, 2, 1): L(
        "narrateur|Sur le tapis, Nina veut le crayon comme baguette.",
        "copine|Je tape la chanson !",
        "enfant-f|Je dessine le rayon !",
        "narrateur|Le crayon sert de baguette, trop fort.",
        "narrateur|La mine casse, un petit bruit sec.",
        "narrateur|Mila recule, la chanson cassée aussi.",
        "narrateur|Elle n'attrape pas le bout cassé.",
        "narrateur|Dans le miroir, la virgule d'or reste entière.",
        "enfant-f|Ta chanson, avec les mains.",
        "copine|Ton rayon, avec le bout qui reste.",
        "papa|La mine a laissé un point d'or, sur la laine.",
        "maman|Je vois le point.",
        "narrateur|Mila dessine le rayon, sans tapoter.",
        "narrateur|Nina tape la laine, très léger.",
    ),
    (1, 2, 2): L(
        "narrateur|Le coussin bleu devient une scène, sur le tapis.",
        "copine|Ma chanson de pluie, debout dessus !",
        "enfant-f|Ma chanson de rayon, moi !",
        "narrateur|Elles montent ensemble.",
        "narrateur|Le coussin s'écrase, et le chant s'étouffe.",
        "narrateur|Mila descend, sans pousser.",
        "narrateur|Un grain d'or brille dans le creux du tissu.",
        "narrateur|C'est la virgule du rayon.",
        "enfant-f|Toi la pluie, sur le coussin.",
        "copine|Toi le rayon, à côté, sur la laine.",
        "papa|Deux scènes, un tapis.",
        "maman|Le coussin a repris un peu d'air.",
        "narrateur|Mila chante dans le creux, sans monter.",
        "narrateur|Le miroir, au sol, tient l'or.",
    ),
    (1, 2, 3): L(
        "narrateur|Le grelot veut marquer le tempo, sur le tapis.",
        "enfant-f|Ding, c'est le rayon !",
        "copine|Ding, c'est la pluie !",
        "narrateur|Deux dings, aucun air.",
        "narrateur|La chanson n'a plus de place.",
        "narrateur|Mila pose le grelot, les lèvres fermées.",
        "narrateur|Elle écoute le silence de la laine.",
        "narrateur|La virgule d'or cligne sur le métal.",
        "enfant-f|Un ding, puis ta pluie.",
        "copine|Un ding, puis ton rayon.",
        "papa|Le tempo est revenu, lent.",
        "maman|J'entends les deux airs.",
        "narrateur|Le grelot reste au milieu, sage.",
        "narrateur|Mila sourit, un peu, enfin.",
    ),
    (1, 3, 1): L(
        "narrateur|Le crayon jaune vise le papier du tapis.",
        "enfant-f|Ma virgule, au milieu !",
        "copine|Ma flaque, au milieu !",
        "narrateur|Deux pointes se touchent, et le papier se fend un peu.",
        "narrateur|Mila retire la mine, le cœur serré.",
        "narrateur|Elle refuse de tirer plus fort.",
        "narrateur|Dans le miroir, la virgule d'or n'est pas fendue.",
        "enfant-f|Toi le rond, à gauche.",
        "copine|Toi le trait, à droite.",
        "papa|La fente du papier s'arrête, petite.",
        "maman|Deux rives, une feuille.",
        "narrateur|Mila trace l'or, loin de la fente.",
        "narrateur|Nina peint l'eau, de l'autre côté.",
        "narrateur|Le soleil pâle a de l'air, autour.",
    ),
    (1, 3, 2): L(
        "narrateur|Nina pose le papier sur le coussin bleu.",
        "copine|C'est plus mou, pour la flaque !",
        "enfant-f|Trop mou, pour l'or !",
        "narrateur|Le trait de Mila s'enfonce, bizarre.",
        "narrateur|Le papier glisse dans le creux.",
        "narrateur|Mila lâche, sans crier.",
        "narrateur|Un grain d'or brille sur le bord du coussin.",
        "enfant-f|Le papier, au sol, à plat.",
        "copine|Le coussin, pour s'asseoir, à côté.",
        "papa|Le trait d'or tient, sur le dur.",
        "maman|La flaque de Nina aussi.",
        "narrateur|Mila dessine, assise sur la laine, pas sur le bleu.",
        "narrateur|Le miroir surveille, près du papier.",
        "narrateur|La virgule du vestiaire a une place nette.",
    ),
    (1, 3, 3): L(
        "narrateur|Le grelot roule sur le papier du tapis.",
        "copine|Il fait un rond, comme ma flaque !",
        "enfant-f|Il écrase mon trait !",
        "narrateur|Un ding, et le soleil pâle s'estompe.",
        "narrateur|Mila rattrape le métal, trop tard.",
        "narrateur|Elle le pose loin, sans le secouer.",
        "narrateur|Sous le grelot, une virgule d'or est restée.",
        "enfant-f|Toi le rond d'eau, sans le ding.",
        "copine|Toi le trait, sans le métal.",
        "papa|Le papier a un petit cercle, souvenir.",
        "maman|L'or est à côté, vivant.",
        "narrateur|Mila reprend le crayon, loin du grelot.",
        "narrateur|Nina dessine l'eau, sans rouler.",
        "narrateur|Le tapis garde un silence rond.",
    ),
    (2, 1, 1): L(
        "narrateur|À la table, le crayon veut entrer dans la rainure.",
        "enfant-f|Je sors l'or de la miette !",
        "copine|Je sors le loup de la page !",
        "narrateur|La mine racle la craie, un nuage blanc.",
        "narrateur|La page du loup se tache.",
        "narrateur|Mila recule, la mine trop avide.",
        "narrateur|Elle pose le crayon, et ouvre le miroir.",
        "narrateur|La virgule d'or y est, propre.",
        "enfant-f|Toi le loup, sur la page propre.",
        "copine|Toi l'or, loin de la rainure.",
        "papa|La tache blanche s'arrête, au bord.",
        "maman|Je vois le loup, et l'or.",
        "narrateur|Mila trace l'or sur le bois, pas sur le livre.",
        "narrateur|Nina dit le loup, sans le toc.",
    ),
    (2, 1, 2): L(
        "narrateur|Nina hisse le coussin sur la chaise, trop haut.",
        "copine|Je lis le loup, comme une reine !",
        "enfant-f|Je monte aussi !",
        "narrateur|Le livre glisse de la table, une page pliée.",
        "narrateur|Mila n'attrape pas le loup en l'air.",
        "narrateur|Elle reste au sol, le miroir contre elle.",
        "narrateur|La virgule d'or y tient, sans chuter.",
        "enfant-f|Le coussin, au sol.",
        "copine|Le livre, sur le bois, pas sur le bleu.",
        "papa|La page s'est dépliée, presque.",
        "maman|Deux lectrices, une table.",
        "narrateur|Mila s'assoit sur le coussin, assez bas.",
        "narrateur|Nina dit le loup, à la même hauteur.",
        "narrateur|Le bois de la table a cessé de trembler.",
    ),
    (2, 1, 3): L(
        "narrateur|Le grelot pose un ding sur la table, près du livre.",
        "enfant-f|Mon tour !",
        "copine|Mon loup !",
        "narrateur|Le ding et le toc se mêlent, trop.",
        "narrateur|Le loup n'a plus de voix.",
        "narrateur|Mila coiffe le grelot d'une main, pour le taire.",
        "narrateur|Sur le métal, la virgule d'or s'est collée.",
        "enfant-f|Un ding, puis le loup.",
        "copine|Puis l'or.",
        "papa|J'ai le silence, entre les deux.",
        "maman|La rainure n'a plus volé de mot.",
        "narrateur|Mila dit l'or, après le loup.",
        "narrateur|Le grelot reste couché, sage.",
        "narrateur|La miette de craie est blanche, intacte.",
    ),
    (2, 2, 1): L(
        "narrateur|À la table, Nina tape le crayon comme un tambour.",
        "copine|Toc toc, ma pluie !",
        "enfant-f|Moi, la lumière, avec la mine !",
        "narrateur|Deux usages, un seul bois jaune.",
        "narrateur|La mine file sous la table.",
        "narrateur|Mila se baisse, sans crier.",
        "narrateur|Sous le bois, le miroir attrape un grain d'or.",
        "narrateur|C'est la virgule, tombée avec la mine.",
        "enfant-f|Ton tambour, avec les doigts.",
        "copine|Ta lumière, avec le crayon, après.",
        "papa|La mine est revenue, entière.",
        "maman|Le toc a laissé un creux, pour l'or.",
        "narrateur|Mila dessine le rayon, sans tapoter.",
        "narrateur|Nina tapote le bois, les mains nues.",
    ),
    (2, 2, 2): L(
        "narrateur|Nina pose le coussin sur la table, pour étouffer le toc.",
        "copine|Ma chanson, plus molle !",
        "enfant-f|Ma chanson, plus claire !",
        "narrateur|Le bois ne sonne plus, trop de bleu.",
        "narrateur|Les deux airs s'étouffent.",
        "narrateur|Mila retire le coussin, sans le jeter.",
        "narrateur|Un grain d'or reste collé au tissu.",
        "enfant-f|Le coussin, sur nos genoux.",
        "copine|Le bois, pour le toc, un peu.",
        "papa|J'entends un toc, puis une note claire.",
        "maman|Deux chansons, un bois nu.",
        "narrateur|Mila chante la lumière, le coussin sur les genoux.",
        "narrateur|Nina tapote, plus léger.",
        "narrateur|La rainure a cessé de manger les notes.",
    ),
    (2, 2, 3): L(
        "narrateur|Le grelot et le toc veulent le même tempo.",
        "enfant-f|Ding, lumière !",
        "copine|Toc, pluie !",
        "narrateur|Ding toc ding toc, plus de chanson.",
        "narrateur|Mila pose le grelot dans la rainure, pour le calmer.",
        "narrateur|La virgule d'or glisse du métal à la craie.",
        "enfant-f|Un ding, dans le creux.",
        "copine|Un toc, après.",
        "papa|Le tempo a trouvé un trou.",
        "maman|J'entends la pluie, puis la lumière.",
        "narrateur|Mila chante, le grelot endormi.",
        "narrateur|Nina tapote, sans le métal.",
        "narrateur|La table a deux musiques, l'une après l'autre.",
        "narrateur|Le miroir, près du bord, tient l'or.",
    ),
    (2, 3, 1): L(
        "narrateur|À la table, le crayon jaune et la miette se disputent le papier.",
        "enfant-f|Mon or, net !",
        "copine|Ma flaque, pâle !",
        "narrateur|Le jaune et le blanc se mêlent, boueux.",
        "narrateur|Mila lâche la mine, déçue.",
        "narrateur|Elle essuie le papier d'un souffle, trop faible.",
        "narrateur|Dans le miroir, la virgule d'or reste nette.",
        "enfant-f|Toi le pâle, en haut.",
        "copine|Toi le jaune, en bas.",
        "papa|La boue s'arrête, au milieu.",
        "maman|Deux couleurs, une feuille.",
        "narrateur|Mila trace l'or, loin de la miette.",
        "narrateur|Nina frotte le pâle, loin du jaune.",
        "narrateur|Le papier a cessé de glisser.",
    ),
    (2, 3, 2): L(
        "narrateur|Nina glisse le papier sur le coussin, posé sur la table.",
        "copine|Plus doux, pour l'eau !",
        "enfant-f|Trop mou, ça danse !",
        "narrateur|Le trait d'or devient une vague, malgré Mila.",
        "narrateur|Elle retire le papier, vers le bois dur.",
        "narrateur|Un grain d'or reste dans le creux bleu.",
        "enfant-f|Le papier, sur le bois.",
        "copine|Le coussin, sous nous.",
        "papa|Le trait tient, sur le dur.",
        "maman|La flaque de Nina aussi, à côté.",
        "narrateur|Mila dessine, les coudes sur la table.",
        "narrateur|Nina s'assoit sur le bleu, et peint l'eau.",
        "narrateur|Le miroir, près de la rainure, cligne.",
        "narrateur|La virgule du vestiaire a une rive ferme.",
    ),
    (2, 3, 3): L(
        "narrateur|Le grelot traverse le dessin, ding, sur la table.",
        "copine|Il fait des ronds, comme l'eau !",
        "enfant-f|Il barre mon or !",
        "narrateur|Trois cercles écrasent le trait.",
        "narrateur|Mila arrête le métal d'une paume.",
        "narrateur|Sous le grelot, la virgule d'or a survécu.",
        "enfant-f|Toi les ronds, sans rouler.",
        "copine|Toi l'or, sans le ding.",
        "papa|Les cercles restent, souvenirs.",
        "maman|L'or est à côté, vivant.",
        "narrateur|Mila reprend le crayon, loin du métal.",
        "narrateur|Nina dessine l'eau, le grelot couché.",
        "narrateur|La table a cessé de sonner.",
        "narrateur|Le papier sent le bois, et un peu d'argent.",
    ),
    (3, 1, 1): L(
        "narrateur|Près de la fenêtre, Mila veut tracer l'or sur le verre.",
        "enfant-f|La virgule, sur la vitre !",
        "copine|Le ciel, sur la vitre !",
        "narrateur|Le crayon glisse, et un trait rate le ciel.",
        "narrateur|Nina souffle, tout bas.",
        "narrateur|Mila retire la mine, sans frotter.",
        "narrateur|Dans le miroir, la vraie virgule d'or tient.",
        "enfant-f|Toi le ciel, dans l'eau.",
        "copine|Toi l'or, sur le papier, pas sur le verre.",
        "papa|La vitre a gardé un trait pâle, souvenir.",
        "maman|Le livre a retrouvé le loup, au sec.",
        "narrateur|Mila dessine l'or sur une feuille, loin du froid.",
        "narrateur|Nina dit le ciel, en regardant la flaque.",
        "narrateur|Le nuage de l'eau a cessé de trembler.",
    ),
    (3, 1, 2): L(
        "narrateur|Toutes deux veulent le coussin, sous la fenêtre.",
        "copine|Pour voir le ciel de l'eau !",
        "enfant-f|Pour voir l'or du rayon !",
        "narrateur|Le coussin est trop étroit, pour deux visages.",
        "narrateur|Leurs têtes se cognent, un peu.",
        "narrateur|Mila recule, la joue chaude.",
        "narrateur|Sur le bleu, un grain d'or s'est posé.",
        "enfant-f|Toi le rebord, pour la flaque.",
        "copine|Toi le coussin, pour l'or.",
        "papa|Deux regards, deux places.",
        "maman|Je vois le ciel, et l'or.",
        "narrateur|Mila s'assoit, le miroir vers le rayon.",
        "narrateur|Nina colle le nez au verre, pour l'eau.",
        "narrateur|Le livre reste ouvert, entre elles, sans chute.",
    ),
    (3, 1, 3): L(
        "narrateur|Le grelot sonne contre la vitre, ding.",
        "copine|Pour appeler le ciel !",
        "enfant-f|Pour appeler l'or !",
        "narrateur|La flaque dehors se ride, toute petite.",
        "narrateur|Le loup de la page tremble.",
        "narrateur|Mila pose le métal sur le rebord, sans ding.",
        "narrateur|La virgule d'or s'y colle, au silence.",
        "enfant-f|Toi le ciel, sans le ding.",
        "copine|Toi l'or, après le plic de l'eau.",
        "papa|La flaque s'est lissée.",
        "maman|J'ai le ciel, puis l'or.",
        "narrateur|Mila dit l'or, le grelot muet.",
        "narrateur|Nina dit le ciel, le front au verre.",
        "narrateur|Le livre n'a plus peur du métal.",
    ),
    (3, 2, 1): L(
        "narrateur|Près de la fenêtre, le crayon veut siffler sur le verre.",
        "enfant-f|Une chanson de lumière, crissant !",
        "copine|Non, ma pluie, sans crisser !",
        "narrateur|Le verre crie, laid, sous la mine.",
        "narrateur|Nina se bouche une oreille.",
        "narrateur|Mila retire le crayon, les joues rouges.",
        "narrateur|Elle ouvre le miroir : la virgule d'or n'a pas crié.",
        "enfant-f|Ta pluie, avec la voix.",
        "copine|Ta lumière, avec la voix, après.",
        "papa|Le verre a cessé de crier.",
        "maman|Deux chansons, sans mine.",
        "narrateur|Mila pose le crayon, et chante le rayon.",
        "narrateur|Nina chante la pluie, le nez à la flaque.",
        "narrateur|Un oiseau minuscule traverse l'eau, sans peur.",
    ),
    (3, 2, 2): L(
        "narrateur|Elles se serrent sur le coussin, sous la fenêtre.",
        "copine|Ma pluie, tout près du verre !",
        "enfant-f|Mon rayon, tout près aussi !",
        "narrateur|Trop serrées, les deux voix s'étouffent.",
        "narrateur|Le coussin glisse du rebord.",
        "narrateur|Mila le rattrape, sans crier.",
        "narrateur|Un grain d'or brille dans le creux bleu.",
        "enfant-f|Toi au verre, pour la pluie.",
        "copine|Toi au coussin, pour le rayon.",
        "papa|Deux places, un rebord.",
        "maman|J'entends la pluie, puis la lumière.",
        "narrateur|Mila chante, assise, le miroir sur les genoux.",
        "narrateur|Nina chante, debout, le front au froid.",
        "narrateur|La vitre a cessé de vibrer.",
    ),
    (3, 2, 3): L(
        "narrateur|Le grelot et la vitre veulent vibrer ensemble.",
        "enfant-f|Ding, rayon !",
        "copine|Ding, pluie !",
        "narrateur|Le verre bourdonne, trop.",
        "narrateur|La flaque se ride, et l'oiseau s'enfuit.",
        "narrateur|Mila pose le grelot sur le coussin, pour l'étouffer.",
        "narrateur|La virgule d'or glisse du métal au bleu.",
        "enfant-f|Ta pluie, sans ding.",
        "copine|Ton rayon, après, sans ding.",
        "papa|La vitre s'est tue.",
        "maman|L'eau dehors est lisse.",
        "narrateur|Mila chante le rayon, le grelot endormi.",
        "narrateur|Nina chante la pluie, tout bas.",
        "narrateur|L'oiseau minuscule revient, dans la flaque.",
    ),
    (3, 3, 1): L(
        "narrateur|Le crayon veut deux soleils, sur le papier de la fenêtre.",
        "enfant-f|Mon or, dans le rond clair !",
        "copine|Mon eau, dans le rond clair !",
        "narrateur|Deux soleils se marchent dessus, et le rond s'éteint.",
        "narrateur|La buée revient, un peu.",
        "narrateur|Mila souffle trop fort, puis s'arrête.",
        "narrateur|Dans le miroir, la virgule d'or n'a pas bavé.",
        "enfant-f|Toi le rond d'eau, à gauche du clair.",
        "copine|Toi le trait d'or, à droite.",
        "papa|Le rond clair a de la place, autour.",
        "maman|La buée sèche, toute seule.",
        "narrateur|Mila trace l'or, loin du rond.",
        "narrateur|Nina peint l'eau, loin de l'or.",
        "narrateur|Le papier a quitté le verre, net.",
    ),
    (3, 3, 2): L(
        "narrateur|Nina plaque le papier sur le coussin, contre la vitre.",
        "copine|Pour copier le ciel !",
        "enfant-f|Pour copier l'or !",
        "narrateur|La buée colle la feuille, trop.",
        "narrateur|Un coin se déchire, minuscule.",
        "narrateur|Mila décolle, sans tirer.",
        "narrateur|Sur le bleu mouillé, un grain d'or tient.",
        "enfant-f|Le papier, au sec, sur le rebord.",
        "copine|Le coussin, loin du verre.",
        "papa|La déchirure s'arrête, petite.",
        "maman|Le ciel et l'or ont chacun un bord.",
        "narrateur|Mila dessine l'or, le papier sec.",
        "narrateur|Nina dessine l'eau, le coussin sous le bras.",
        "narrateur|La vitre n'a plus de feuille collée.",
    ),
    (3, 3, 3): L(
        "narrateur|Le grelot jette son ombre sur le papier, près du verre.",
        "copine|L'ombre, c'est ma flaque !",
        "enfant-f|L'ombre, c'est mon or !",
        "narrateur|Deux mains veulent l'ombre, et le papier bascule.",
        "narrateur|Le grelot manque la vitre, de peu.",
        "narrateur|Mila le rattrape, le cœur battant.",
        "narrateur|Sur le métal, la virgule d'or n'est pas tombée.",
        "enfant-f|Toi l'ombre d'eau, dessinée.",
        "copine|Toi l'or, hors de l'ombre.",
        "papa|Le papier est resté sur le rebord.",
        "maman|Le grelot n'a pas touché le verre.",
        "narrateur|Mila trace l'or, loin de l'ombre.",
        "narrateur|Nina peint l'eau, dans l'ombre, sans ding.",
        "narrateur|Le rayon de la fenêtre a failli tout emporter.",
    ),
}

# "tout doux" slipped into (1,2,1) — will be caught by L() if present.
# Fix that line if needed when running.

FINS = {
    (1, 1, 1): L(
        "narrateur|Le rayon du vestiaire s'amincit, entre les manteaux.",
        "narrateur|La virgule d'or a failli partir.",
        "enfant-f|Elle est sur le crayon, papa.",
        "papa|Je vois le trait d'or.",
        "narrateur|Le ciré jaune sèche, près du manteau trop long.",
        "narrateur|Nina range le loup, sans se presser.",
        "narrateur|Dans la flaque, le ciel garde un petit trait d'or.",
    ),
    (1, 1, 2): L(
        "narrateur|Le rayon du vestiaire s'amincit, presque rien.",
        "narrateur|La virgule a failli s'éteindre.",
        "enfant-f|Elle est dans le creux du coussin.",
        "maman|Je vois le grain, sur le bleu.",
        "narrateur|Papa a accroché le ciré, au bon crochet.",
        "narrateur|Le livre reste ouvert, entre deux genoux.",
        "narrateur|Le manteau trop long a rendu toute sa fente de lumière.",
    ),
    (1, 1, 3): L(
        "narrateur|Le rayon du vestiaire n'est plus qu'un fil.",
        "narrateur|La virgule a failli se taire dans le ding.",
        "enfant-f|Elle est sur le grelot, maintenant.",
        "papa|Je l'entends, sans le métal.",
        "narrateur|Maman a plié l'écharpe, le fil d'or caché.",
        "narrateur|Nina pose le grelot, sans le secouer.",
        "narrateur|Le crochet du ciré jaune fait un dernier clic, puis rien.",
    ),
    (1, 2, 1): L(
        "narrateur|Le rayon du vestiaire glisse vers le sol.",
        "narrateur|La virgule a failli se casser, avec la mine.",
        "enfant-f|Le point d'or est sur la laine.",
        "maman|Je le vois, minuscule.",
        "narrateur|Le sachet de la poire ne chuchote plus.",
        "narrateur|Nina tape la laine, très léger.",
        "narrateur|L'écharpe rouge a un fil d'or, immobile.",
    ),
    (1, 2, 2): L(
        "narrateur|Le rayon du vestiaire s'étire, puis recule.",
        "narrateur|La virgule a failli s'écraser, dans le bleu.",
        "enfant-f|Elle chante, à côté du coussin.",
        "papa|J'ai les deux airs.",
        "narrateur|Le cartable bleu ne penche plus.",
        "narrateur|Nina range le ciré, sur les genoux.",
        "narrateur|Le savon des lavabos sent moins fort, près des manteaux.",
    ),
    (1, 2, 3): L(
        "narrateur|Le rayon du vestiaire cligne, une dernière fois.",
        "narrateur|La virgule a failli se perdre dans les dings.",
        "enfant-f|Elle est au milieu, sage.",
        "maman|Le tempo est là, lent.",
        "narrateur|Papa pose le miroir, ouvert, sur le tapis.",
        "narrateur|Nina sourit, un peu, elle aussi.",
        "narrateur|Le miroir rond reste ouvert, un grain d'or au verre.",
    ),
    (1, 3, 1): L(
        "narrateur|Le rayon du vestiaire quitte le carré du tapis.",
        "narrateur|La virgule a failli se fendre, avec le papier.",
        "enfant-f|Elle est à droite, entière.",
        "papa|La fente du papier s'est arrêtée.",
        "narrateur|Maman essuie une miette de laine, sur le ciré.",
        "narrateur|Nina peint l'eau, de l'autre côté.",
        "narrateur|Le carré de soleil a quitté le tapis, sans bruit.",
    ),
    (1, 3, 2): L(
        "narrateur|Le rayon du vestiaire s'amincit, loin du bleu.",
        "narrateur|La virgule a failli s'enfoncer, dans le mou.",
        "enfant-f|Elle est nette, sur le dur.",
        "maman|Le grain du coussin brille, souvenir.",
        "narrateur|Papa a redressé le cartable, contre le mur.",
        "narrateur|Nina s'assoit sur le bleu, enfin seule.",
        "narrateur|Entre les manteaux, le rayon n'est plus qu'un fil.",
    ),
    (1, 3, 3): L(
        "narrateur|Le rayon du vestiaire s'efface, presque.",
        "narrateur|La virgule a failli partir sous le grelot.",
        "enfant-f|Elle est à côté du cercle, vivante.",
        "papa|Le silence rond est là.",
        "narrateur|Le papier du sachet ne dit plus rien.",
        "narrateur|Nina pose le métal, loin du blanc.",
        "narrateur|La miette de craie a pris une poussière d'or.",
    ),
    (2, 1, 1): L(
        "narrateur|Le rayon du vestiaire revient, très mince, sur le bois.",
        "narrateur|La virgule a failli se salir, dans la craie.",
        "enfant-f|Elle est sur la table, propre.",
        "maman|Je vois le loup, et l'or.",
        "narrateur|Nina dit le loup, sans le toc.",
        "narrateur|Papa range la poire, dans le sachet.",
        "narrateur|La rainure du bois tient un éclat minuscule.",
    ),
    (2, 1, 2): L(
        "narrateur|Le rayon du vestiaire touche le dossier de la chaise.",
        "narrateur|La virgule a failli chuter, avec le livre.",
        "enfant-f|Elle n'est pas tombée.",
        "papa|Deux lectrices, une table.",
        "narrateur|Nina s'assoit, à la même hauteur.",
        "narrateur|Maman déplie la page, du bout des doigts.",
        "narrateur|Le toc de la table s'est tu, pour de bon.",
    ),
    (2, 1, 3): L(
        "narrateur|Le rayon du vestiaire se pose sur le grelot couché.",
        "narrateur|La virgule a failli se noyer dans le ding.",
        "enfant-f|Elle est collée au métal, sans bruit.",
        "maman|J'ai le silence, entre les deux.",
        "narrateur|Nina pose une main à plat, sur le bois.",
        "narrateur|Papa ferme le sachet, un petit chuchotement.",
        "narrateur|Le cartable bleu ne penche plus, contre le mur.",
    ),
    (2, 2, 1): L(
        "narrateur|Le rayon du vestiaire rampe sous la table, un instant.",
        "narrateur|La virgule a failli rester par terre, avec la mine.",
        "enfant-f|Le miroir l'a rattrapée.",
        "papa|La mine est entière.",
        "narrateur|Nina tapote, les mains nues.",
        "narrateur|Maman pose le crayon, loin du bord.",
        "narrateur|Papa a posé le ciré jaune, à côté du manteau.",
    ),
    (2, 2, 2): L(
        "narrateur|Le rayon du vestiaire traverse le coussin, puis s'en va.",
        "narrateur|La virgule a failli s'étouffer, sous le bleu.",
        "enfant-f|Elle chante, sur nos genoux.",
        "maman|Deux chansons, un bois nu.",
        "narrateur|Nina tapote, plus léger.",
        "narrateur|Papa raccroche le ciré, au crochet voisin.",
        "narrateur|Maman a plié l'écharpe, le fil d'or caché.",
    ),
    (2, 2, 3): L(
        "narrateur|Le rayon du vestiaire entre dans la rainure, puis sort.",
        "narrateur|La virgule a failli se perdre, entre ding et toc.",
        "enfant-f|Elle dort, près du bord.",
        "papa|Le tempo a trouvé un trou.",
        "narrateur|Nina chante la pluie, sans le métal.",
        "narrateur|Maman couche le grelot, dans la rainure.",
        "narrateur|Un oiseau minuscule a quitté la flaque.",
    ),
    (2, 3, 1): L(
        "narrateur|Le rayon du vestiaire glisse sur le papier, trop vite.",
        "narrateur|La virgule a failli devenir boue, avec la craie.",
        "enfant-f|Elle est en bas, nette.",
        "maman|Deux couleurs, une feuille.",
        "narrateur|Nina frotte le pâle, loin du jaune.",
        "narrateur|Papa souffle la miette, hors du blanc.",
        "narrateur|Le verre de la fenêtre n'a plus de buée.",
    ),
    (2, 3, 2): L(
        "narrateur|Le rayon du vestiaire quitte le bois, vers la porte.",
        "narrateur|La virgule a failli danser, trop molle.",
        "enfant-f|Elle a une rive ferme, maintenant.",
        "papa|Le trait tient, sur le dur.",
        "narrateur|Nina s'assoit sur le bleu, et peint l'eau.",
        "narrateur|Maman pose le miroir, près de la rainure.",
        "narrateur|La poire attend, sage, dans son papier.",
    ),
    (2, 3, 3): L(
        "narrateur|Le rayon du vestiaire se brise sur le grelot, un éclair.",
        "narrateur|La virgule a failli partir sous les cercles.",
        "enfant-f|Elle est à côté, vivante.",
        "maman|L'or n'a pas été barré.",
        "narrateur|Nina dessine l'eau, le métal couché.",
        "narrateur|Papa range le grelot, loin du blanc.",
        "narrateur|La fente de lumière s'est refermée, entre les manteaux.",
    ),
    (3, 1, 1): L(
        "narrateur|Le rayon du vestiaire quitte la vitre, vers le couloir.",
        "narrateur|La virgule a failli rater le ciel, sur le verre.",
        "enfant-f|Elle est sur la feuille, au sec.",
        "papa|Le livre a le loup, au sec aussi.",
        "narrateur|Nina dit le ciel, en regardant la flaque.",
        "narrateur|Maman essuie le trait pâle, sur la vitre.",
        "narrateur|Le ciel de la flaque est devenu gris, sans trait.",
    ),
    (3, 1, 2): L(
        "narrateur|Le rayon du vestiaire touche deux visages, puis un seul.",
        "narrateur|La virgule a failli se cogner, trop serrée.",
        "enfant-f|Elle est sur le coussin, à moi.",
        "maman|Deux regards, deux places.",
        "narrateur|Nina colle le nez au verre, pour l'eau.",
        "narrateur|Papa ouvre le livre, entre elles, sans chute.",
        "narrateur|Le clic du miroir ne se répète pas.",
    ),
    (3, 1, 3): L(
        "narrateur|Le rayon du vestiaire tremble, avec le ding, puis s'arrête.",
        "narrateur|La virgule a failli rider toute l'eau.",
        "enfant-f|Elle est collée au silence, sur le rebord.",
        "papa|La flaque s'est lissée.",
        "narrateur|Nina dit le ciel, le front au verre.",
        "narrateur|Maman couche le grelot, loin de la vitre.",
        "narrateur|Le crochet froid garde une laine jaune, et une laine sombre.",
    ),
    (3, 2, 1): L(
        "narrateur|Le rayon du vestiaire fuit le cri du verre.",
        "narrateur|La virgule a failli crier, avec la mine.",
        "enfant-f|Elle n'a pas crié.",
        "maman|Deux chansons, sans mine.",
        "narrateur|Nina chante la pluie, le nez à la flaque.",
        "narrateur|Papa pose le crayon, loin du froid.",
        "narrateur|Une goutte de la flaque sèche sur le rebord.",
    ),
    (3, 2, 2): L(
        "narrateur|Le rayon du vestiaire glisse du rebord, trop étroit.",
        "narrateur|La virgule a failli s'étouffer, trop serrée.",
        "enfant-f|Elle chante, sur mes genoux.",
        "papa|Deux places, un rebord.",
        "narrateur|Nina chante, debout, le front au froid.",
        "narrateur|Maman rattrape le coussin, une dernière fois.",
        "narrateur|Le rayon du vestiaire n'éclaire plus que la poussière.",
    ),
    (3, 2, 3): L(
        "narrateur|Le rayon du vestiaire s'enfuit, avec l'oiseau, un instant.",
        "narrateur|La virgule a failli rider l'eau, pour toujours.",
        "enfant-f|Elle dort, sur le bleu.",
        "maman|L'eau dehors est lisse.",
        "narrateur|Nina chante la pluie, tout bas.",
        "narrateur|Papa pose le grelot, étouffé.",
        "narrateur|L'oiseau minuscule revient, dans la flaque, et s'arrête.",
    ),
    (3, 3, 1): L(
        "narrateur|Le rayon du vestiaire quitte le rond clair, trop tard.",
        "narrateur|La virgule a failli baver, dans deux soleils.",
        "enfant-f|Elle est à droite, nette.",
        "papa|Le rond clair a de la place, autour.",
        "narrateur|Nina peint l'eau, loin de l'or.",
        "narrateur|Maman souffle la buée, sans frotter.",
        "narrateur|La virgule d'or dort sur le rebord du miroir.",
    ),
    (3, 3, 2): L(
        "narrateur|Le rayon du vestiaire se colle, puis se décolle, avec la feuille.",
        "narrateur|La virgule a failli se déchirer, minuscule.",
        "enfant-f|Elle est au sec, sur le rebord.",
        "maman|La déchirure s'est arrêtée.",
        "narrateur|Nina dessine l'eau, le coussin sous le bras.",
        "narrateur|Papa écarte le papier du verre, sans tirer.",
        "narrateur|Le manteau trop long touche le sol, sans cacher le monde.",
    ),
    (3, 3, 3): L(
        "narrateur|Le rayon du vestiaire a failli tout emporter, avec l'ombre.",
        "narrateur|La virgule n'est pas tombée.",
        "enfant-f|Elle est hors de l'ombre, sur le métal.",
        "papa|Le grelot n'a pas touché le verre.",
        "narrateur|Nina peint l'eau, dans l'ombre, sans ding.",
        "narrateur|Maman pose le miroir, ouvert, sur le rebord.",
        "narrateur|Dehors, la flaque n'a plus de ciel, seulement de l'eau.",
    ),
}

SONS = {
    "CHK_T0000_P0000": "vestiaire,papier",
    "CHK_T0001_P0001": "tapis",
    "CHK_T0001_P0002": "table,toc",
    "CHK_T0001_P0003": "fenetre,flaque",
}
SONS_T2 = {1: "pages,livre", 2: "chant,laine", 3: "papier,crayon"}
SONS_T3 = {1: "crayon", 2: "coussin", 3: "grelot"}
SONS_FIN = {1: "vestiaire,silence", 2: "flaque,laine", 3: "miroir,crochet"}

QMETA = {
    1: qf(
        "main",
        "main | sa main | la main | lever la main | elle lève la main | attendre",
        "Dans le carré de soleil, que lève Mila ?",
        "Oui, sa main.",
    ),
    2: qf(
        "miroir",
        "miroir | le miroir | un miroir | le verre | attendre",
        "Près de la rainure, que pose Mila ?",
        "Oui, le miroir.",
    ),
    3: qf(
        "ciel",
        "ciel | le ciel | un bout de ciel | la flaque | flaque | attendre",
        "Dans la flaque, que voit-on ?",
        "Oui, le ciel.",
    ),
}


def build() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {
        "CHK_T0000_P0000": DEBUT,
        "CHK_T0001_P0000": T1Q,
    }
    sons: dict[str, str] = dict(SONS)
    extras: dict[str, dict] = {
        "CHK_T0001_P0000": t3("le tapis", "la table", "la fenêtre"),
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = T1[i]
        s[f"{p}_Q0001"] = Q1[i]
        extras[f"{p}_Q0001"] = QMETA[i]
        s[f"{p}_C0001"] = C1[i]
        s[f"{p}_T0002_P0000"] = T2Q[i]
        extras[f"{p}_T0002_P0000"] = t3("l'histoire", "la chanson", "le dessin")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = T2[(i, j)]
            sons[p2] = SONS_T2[j]
            s[f"{p2}_T0003_P0000"] = T3Q[j]
            extras[f"{p2}_T0003_P0000"] = t3("le crayon", "le coussin", "le grelot")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = T3[(i, j, k)]
                sons[p3] = SONS_T3[k]
                s[f"{p3}_F0001"] = FINS[(i, j, k)]
                sons[f"{p3}_F0001"] = SONS_FIN[k]
    return s, sons, extras


def path_words(scripts: dict) -> tuple[int, int, float]:
    lengths = []
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
                n = 0
                for cid in ids:
                    for ln in scripts[cid]:
                        n += words(ln.split("|", 1)[1])
                lengths.append(n)
    return min(lengths), max(lengths), sum(lengths) / len(lengths)


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
    out["characters"] = "Mila, Nina, papa, maman"
    out["setting"] = "vestiaire de l'école, rayon de poussière, flaque"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "tout doux",
        "tout calme",
        "il faut demander",
        "on doit demander",
        "bravo. tu as",
        "bon travail",
        "papa sourit",
        "maman sourit",
        "aujourd'hui,",
        "j'ai compris",
        "mission accomplie",
        "on lève la main",
        "puis on parle",
        "maîtresse",
        "maitresse",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan: {bad}")
    if TICS.search(blob):
        raise SystemExit(f"{SID} tic corpus")
    fins = [c["text"] for c in out["chunks"] if c.get("kind") == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"{SID} fins distinctes: {len(set(fins))}/{len(fins)}")
    t3s = [
        c["text"]
        for c in out["chunks"]
        if c.get("kind") == "passage"
        and re.fullmatch(r"CHK_T0001_P000[123]_T0002_P000[123]_T0003_P000[123]", c["chunk_id"])
    ]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"{SID} T3 distincts: {len(set(t3s))}/{len(t3s)}")
    t2_texts = [
        c["text"]
        for c in out["chunks"]
        if re.fullmatch(r"CHK_T0001_P000[123]_T0002_P000[123]", c["chunk_id"])
    ]
    if len(t2_texts) != 9 or len(set(t2_texts)) != 9:
        raise SystemExit(f"{SID} T2 distincts: {len(set(t2_texts))}/{len(t2_texts)}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    lo, hi, avg = path_words(scripts)
    print(f"chemins {lo}–{hi} mots (moyenne {avg:.0f})")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    s, n, e = build()
    write_tree(s, n, e)
    lo, hi, avg = path_words(s)
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Au vestiaire, un manteau trop long cache une fente de lumière. "
        "Mila accroche le sien : un rayon s'ouvre, une virgule d'or flotte. "
        "Elle veut la garder dans son miroir rond avant que le soleil quitte "
        "les manteaux. Nina veut le même crochet pour son ciré jaune, et parler "
        "de la flaque. Leurs voix se cognent. Papa s'accroupit. Tapis, table ou "
        "fenêtre changent l'écoute. Histoire, chanson ou dessin changent le "
        "désir. Crayon, coussin ou grelot changent le dernier geste. La virgule "
        "d'or, le rayon et la flaque paient la fin.\n\n"
        "## Vécu\n\n"
        "Mila veut porter la virgule d'or jusqu'au miroir avant que le rayon "
        "quitte les manteaux. Nina veut autre chose au même moment. Première "
        "tentative : les voix se cognent, le sourire disparaît. Tapis (carré de "
        "soleil, scène), table (toc, rainure, miette de craie) ou fenêtre "
        "(flaque, ciel, buée) changent l'obstacle. Histoire, chanson ou dessin "
        "changent la deuxième ruse. Crayon, coussin ou grelot changent le "
        "climax. Tours de parole : envie de couper, retenue, écoute, plaisir "
        "d'être entendue. 27 fins. "
        f"Chemins {lo}–{hi} mots (moyenne {avg:.0f}).\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Troupe D16 : Mila, Nina, papa, maman.\n"
        "- 86 nœuds, graphe et libellés d'options conservés.\n"
        "- 27 fins textuellement distinctes, 27 résolutions distinctes, 9 T2 distincts.\n"
        "- Première tentative échoue. Chaque choix change l'obstacle, le climax, la dernière image.\n"
        "- Indice unique dès l'ouverture : virgule d'or, payée au climax et au retour.\n"
        "- Objet nommé : miroir rond (clic). Coin : passage des manteaux / fente de lumière.\n"
        "- Adulte conversationnel, pas maîtresse. Un merci vécu (T1).\n"
        "- TTS par fonction (ouverture, choix, indice, confirmation, action, obstacle, résolution, retour).\n"
        "- `slow` réservé aux choix, à l'indice et aux fins.\n"
        "- N2 ≤ 15 mots/phrase. Pas de leçon dite. Pas de tics « tout doux / encore / déjà / tout calme ».\n"
        "- Monde ≠ TREE-COL-004 (cloche, crayon), ≠ TREE-COL-016 (craie, oiseau), ≠ TREE-COL-028 (cartable jaune).\n"
        "- P1 F-NAR-019. Pas apply. Pas audio.\n\n"
        "## Direction vocale\n\n"
        "`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, "
        "tempo, sourire, respiration. Adulte conversationnel, pas maîtresse. Tours "
        "de parole : envie de couper, retenue, écoute réelle, plaisir d'être entendu.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
