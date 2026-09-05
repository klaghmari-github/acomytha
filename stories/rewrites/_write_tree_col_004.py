#!/usr/bin/env python3
"""TREE-COL-004 — La cloche et le crayon jaune de Sarah (F-NAR-019, N3, TTS)."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, words  # noqa: E402

SID = "TREE-COL-004"
N3 = LIMITS["N3"]
TITLE = "La cloche et le crayon jaune de Sarah"
FIL = (
    "Dans le couloir des casiers, Sarah veut dessiner la cloche "
    "avec le crayon jaune avant la prochaine sonnerie, puis le laisser à Nina. "
    "Sa phrase se perd dans le tin de la cloche. "
    "Table, casier ou rebord changent l'obstacle. "
    "Taille-crayon, gomme ou cahier cachent le jaune. "
    "Cloche, soleil ou fleur changent le dessin et la dernière image. "
    "Le cran en croissant paie la fin."
)
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="cran en croissant",
        note="arc=installation; intention=émerveiller; emotion=envie_impatiente; intensite=1; destinataire=enfant; sous_texte=la_phrase_va_se_perdre_dans_le_tin; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="boîte",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=le_jaune_cherche_sa_place; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="boîte",
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=le_tic_a_rendu_le_jaune; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="crayon jaune",
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_veut_parler_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_retenue; intensite=2; destinataire=enfant; sous_texte=couper_fait_perdre_la_phrase; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=écouter_a_ouvert_la_boîte; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="cloche",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_cran_et_le_tin_reviennent; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def L(*rows: str) -> list[str]:
    out: list[str] = []
    prev = ""
    run = 1
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        low = ph.lower()
        for bad in ("maîtresse", "maitresse", "aujourd'hui,"):
            if bad in low:
                raise SystemExit(f"interdit: {ph}")
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
    "narrateur|Sarah connaît le couloir de l'école, ses carreaux froids.",
    "narrateur|L'air sent la craie, et le savon des mains.",
    "narrateur|Au bout, la cloche de métal attend, ronde.",
    "narrateur|Elle fait dong, puis un petit tin, mince.",
    "narrateur|Un rayon glisse sur les casiers, étroit.",
    "narrateur|Les casiers alignés font un village de métal.",
    "narrateur|Un cartable sent le goûter à la pomme.",
    "narrateur|La porte de la classe reste entrouverte, un peu.",
    "narrateur|Papa et maman sont venus, près des sacs.",
    "copine|Il me manque le jaune, Sarah !",
    "narrateur|En ce moment, un crayon jaune dépasse du sac.",
    "narrateur|Près de la bague, le bois a un cran en croissant.",
    "narrateur|Le crayon pèse peu, lisse, sauf au cran.",
    "enfant-f|Nina, le jaune, la cloche !",
    "narrateur|La cloche sonne dong, puis le tin.",
    "narrateur|Les mots de Sarah se perdent dans le tin.",
    "narrateur|Son sourire disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "enfant-f|Attends, le jaune !",
    "narrateur|Papa parle à maman, des manteaux.",
    "narrateur|Sarah ouvre la bouche, puis la referme.",
    "narrateur|Maman s'accroupit, à la même hauteur.",
    "narrateur|Ses genoux touchent le carreau froid.",
    "maman|Tu voulais dire quoi ?",
    "papa|On t'écoute, après le tin.",
    "narrateur|Sarah serre le crayon, et le cran pique un peu.",
)

T1Q = L(
    "narrateur|Sarah s'installe où, avec le jaune ?",
    "narrateur|Le jaune cherche une place, vite.",
    "papa|La table, le casier, ou le rebord ?",
    "maman|Tu choisis.",
)

T1 = {
    1: L(
        "narrateur|Sarah pose les coudes à la table du milieu.",
        "narrateur|Le bois est lisse, un peu froid.",
        "narrateur|La boîte des crayons attend, ouverte.",
        "narrateur|Le jaune reste dans sa main, chaud.",
        "enfant-f|Nina, je veux le jaune !",
        "narrateur|Papa parle des manteaux, trop fort.",
        "narrateur|Les mots se cognent, et personne n'entend.",
        "narrateur|Sarah a envie de couper, les dents serrées.",
        "narrateur|Elle referme la bouche, et le cran pique.",
        "maman|Tu nous disais, Sarah ?",
        "narrateur|Sarah glisse le crayon dans la boîte.",
        "narrateur|Le cran fait tic, contre le bois.",
        "enfant-f|Il est là, pour toi.",
        "copine|Je t'ai entendue, là.",
    ),
    2: L(
        "narrateur|Sarah s'arrête près du casier, froid.",
        "narrateur|La porte de métal pique les doigts.",
        "narrateur|Le crayon jaune dépasse du cartable.",
        "enfant-f|Il est à moi !",
        "narrateur|Sa voix part pendant le tin.",
        "copine|Quoi ?",
        "narrateur|Sarah a envie de crier plus fort.",
        "narrateur|Elle rentre le cri, les joues chaudes.",
        "papa|Il dépasse, tu as vu ?",
        "narrateur|Sarah retire le crayon du sac.",
        "narrateur|Elle traverse jusqu'à la boîte.",
        "narrateur|Le cran fait tic, au milieu.",
        "enfant-f|Plus dans le sac.",
        "copine|Là, je vois.",
    ),
    3: L(
        "narrateur|Sarah s'approche du rebord de la fenêtre.",
        "narrateur|La vitre est froide, un peu embuée.",
        "narrateur|Le crayon glisse vers le vide.",
        "enfant-f|Oh !",
        "narrateur|Elle le rattrape, près du bord.",
        "copine|Donne, je le prends !",
        "narrateur|Sarah le serre contre elle, trop fort.",
        "narrateur|Dans sa poitrine, ça se bouscule.",
        "maman|Il est lisse, ce bois ?",
        "narrateur|Sarah revient vers la table, lentement.",
        "narrateur|Elle pose le jaune dans la boîte.",
        "narrateur|Le cran fait tic, sans tomber.",
        "enfant-f|Il ne tombe plus.",
        "copine|Je l'ai vu, tic.",
    ),
}

Q1 = {
    1: L(
        "narrateur|Le jaune manque dans la boîte.",
        "maman|Sarah le pose où ?",
    ),
    2: L(
        "narrateur|Le jaune dépasse du cartable.",
        "papa|Sarah le met où ?",
    ),
    3: L(
        "narrateur|Le crayon glisse vers la vitre.",
        "maman|Sarah le met où, à la fin ?",
    ),
}

C1 = {
    1: L(
        "maman|Oui.",
        "maman|Dans la boîte.",
        "enfant-f|Nina peut le prendre.",
        "papa|Merci, Sarah.",
        "narrateur|Un copeau reste sur le bois.",
        "copine|Le tic, je l'ai.",
    ),
    2: L(
        "papa|Oui.",
        "papa|Dans la boîte, plus dans le sac.",
        "enfant-f|Le jaune est au milieu.",
        "maman|Merci, Sarah.",
        "narrateur|Le métal du casier ne bouge plus.",
        "copine|Il ne dépasse plus.",
    ),
    3: L(
        "maman|Oui.",
        "maman|Dans la boîte.",
        "papa|Il ne tombe plus.",
        "enfant-f|Nina l'a vu.",
        "papa|Merci, Sarah.",
        "narrateur|La buée sèche un peu, sur la vitre.",
    ),
}

T2Q = {
    1: L(
        "narrateur|À la table, Sarah prend un objet.",
        "papa|Le taille-crayon, la gomme, ou le cahier ?",
        "maman|Tu choisis.",
    ),
    2: L(
        "narrateur|Près du casier, Sarah prend un objet.",
        "papa|Le taille-crayon, la gomme, ou le cahier ?",
        "maman|Tu choisis.",
    ),
    3: L(
        "narrateur|Au rebord, Sarah prend un objet.",
        "papa|Le taille-crayon, la gomme, ou le cahier ?",
        "maman|Tu choisis.",
    ),
}

T2 = {
    (1, 1): L(
        "narrateur|Sarah prend le taille-crayon, près de la boîte.",
        "narrateur|Le bois du jaune est un peu émoussé.",
        "narrateur|Elle tourne, et un copeau tombe, fin.",
        "narrateur|Le taille-crayon tapote, trop fort.",
        "enfant-f|Nina, regarde le copeau !",
        "narrateur|Le bruit mange la fin.",
        "copine|Le quoi ?",
        "narrateur|Sarah veut recommencer, plus vite.",
        "narrateur|Elle refuse, et elle écoute le bois.",
        "narrateur|Le cran cogne, une fois, dans le taille-crayon.",
        "enfant-f|Le jaune, après le copeau.",
        "narrateur|Elle retire le crayon, le pose dans la boîte.",
        "maman|Le tic, tu l'as entendu ?",
    ),
    (1, 2): L(
        "narrateur|Sarah prend la gomme, blanche, un peu rêche.",
        "narrateur|Un trait jaune s'efface, lentement.",
        "narrateur|La gomme sent le caoutchouc.",
        "enfant-f|J'efface, et je parle !",
        "narrateur|Nina parle du cartable, en même temps.",
        "narrateur|Deux voix, zéro phrase.",
        "narrateur|Sarah rentre les mots, la gomme arrêtée.",
        "copine|Moi, j'ai fini.",
        "enfant-f|Le jaune, après toi.",
        "narrateur|Elle pose la gomme, puis le crayon.",
        "papa|Là, on t'a entendue.",
        "narrateur|Un grain blanc reste sur le bois.",
    ),
    (1, 3): L(
        "narrateur|Sarah ouvre le cahier, et la page est froide.",
        "narrateur|Le crayon jaune repose sur la reliure.",
        "enfant-f|Ma page, Nina, je commence !",
        "narrateur|Le crayon roule dans le pli, caché.",
        "copine|Il est où, le jaune ?",
        "narrateur|Sarah a envie de dire trop vite.",
        "narrateur|Elle ouvre le pli, sans parler.",
        "narrateur|Le cran brille, dans la colle.",
        "enfant-f|Il dormait là.",
        "narrateur|Elle le glisse dans la boîte.",
        "maman|Tu as cherché, avant de crier ?",
        "narrateur|La page sent un peu la colle.",
    ),
    (2, 1): L(
        "narrateur|Près du casier, Sarah prend le taille-crayon.",
        "narrateur|Le métal amplifie le bruit, rêche.",
        "narrateur|Un copeau jaune tombe sur le loquet.",
        "enfant-f|Nina, le copeau, c'est le cran !",
        "narrateur|Le loquet claque, et la fin s'enfuit.",
        "copine|Je n'ai pas eu le mot.",
        "narrateur|Sarah serre les poings, puis les ouvre.",
        "narrateur|Elle attend que le métal se taise.",
        "enfant-f|Le jaune, après le clac.",
        "narrateur|Le cran cogne dans le taille-crayon, net.",
        "narrateur|Elle pose le crayon dans la boîte.",
        "papa|Le casier t'a coupée, cette fois.",
        "maman|Le tic est revenu, plus clair.",
    ),
    (2, 2): L(
        "narrateur|Près du casier, Sarah prend la gomme.",
        "narrateur|Un grain blanc glisse vers la fente.",
        "enfant-f|Attention, la gomme glisse !",
        "narrateur|Nina cherche le jaune, dans le sac.",
        "narrateur|Sarah parle pendant la recherche.",
        "copine|Attends, je fouille.",
        "narrateur|Sarah rentre la phrase, les joues chaudes.",
        "narrateur|Elle rattrape le grain, près du métal.",
        "enfant-f|Le jaune, quand tu sors la tête.",
        "narrateur|Nina sort, et Sarah pose le crayon.",
        "papa|Tu as attendu sa tête.",
        "narrateur|La gomme sent le caoutchouc, froid.",
    ),
    (2, 3): L(
        "narrateur|Près du casier, Sarah ouvre le cahier.",
        "narrateur|La page manque de tomber dans le métal.",
        "enfant-f|Ma page, et le jaune aussi !",
        "narrateur|Le crayon glisse vers le cartable, de nouveau.",
        "copine|Il va rentrer dans le sac !",
        "narrateur|Sarah a envie de crier stop, trop fort.",
        "narrateur|Elle pose la main à plat, sans voix.",
        "narrateur|Le cran luit, contre le carton.",
        "enfant-f|Pas le sac, la boîte !",
        "narrateur|Elle le glisse au milieu, droit.",
        "maman|Le loquet n'a pas eu le jaune.",
        "papa|Ta main a parlé, avant ta bouche.",
    ),
    (3, 1): L(
        "narrateur|Au rebord, Sarah prend le taille-crayon.",
        "narrateur|Un copeau s'envole vers la buée.",
        "enfant-f|Le copeau, Nina, c'est le cran !",
        "narrateur|Le vent de la fenêtre mange le mot.",
        "copine|Le quoi, le copeau ?",
        "narrateur|Sarah veut courir après le copeau, et parler.",
        "narrateur|Elle s'arrête, et elle écoute la vitre.",
        "narrateur|Le cran frotte le taille-crayon, sec.",
        "enfant-f|Le jaune, sans le vent.",
        "narrateur|Elle pose le crayon dans la boîte.",
        "maman|Le tin de dehors s'est tu.",
        "papa|Le copeau reste au carreau, en croissant.",
    ),
    (3, 2): L(
        "narrateur|Au rebord, Sarah prend la gomme.",
        "narrateur|Un trait jaune s'efface sur la buée.",
        "enfant-f|Je fais une place, et j'explique !",
        "narrateur|Nina parle du dehors, en même temps.",
        "narrateur|La vitre rend les deux voix, mêlées.",
        "copine|Un oiseau, là-bas !",
        "narrateur|Sarah ferme la bouche, la gomme en l'air.",
        "narrateur|Elle attend que l'oiseau parte.",
        "enfant-f|Le jaune, après l'oiseau.",
        "narrateur|Elle pose gomme et crayon, au milieu.",
        "papa|L'oiseau a eu son tour.",
        "maman|Toi, le tien, après.",
    ),
    (3, 3): L(
        "narrateur|Au rebord, Sarah ouvre le cahier.",
        "narrateur|La page se recourbe, froide comme la vitre.",
        "enfant-f|Ma page, je commence ici !",
        "narrateur|Le crayon roule vers le vide, de biais.",
        "copine|Il tombe !",
        "narrateur|Sarah le rattrape, et elle veut crier trop vite.",
        "narrateur|Elle tient le bois, sans parler.",
        "narrateur|Le cran pique, contre sa paume.",
        "enfant-f|Il reste, dans la boîte.",
        "narrateur|Elle le pose, loin du rebord.",
        "maman|Ça a failli finir par terre.",
        "papa|Le tic, cette fois, est au milieu.",
    ),
}

T3Q = {
    1: L(
        "narrateur|Sarah dessine à la table.",
        "maman|La cloche, le soleil, ou la fleur ?",
        "papa|Tu choisis.",
    ),
    2: L(
        "narrateur|Sarah dessine près du casier.",
        "maman|La cloche, le soleil, ou la fleur ?",
        "papa|Tu choisis.",
    ),
    3: L(
        "narrateur|Sarah dessine au rebord.",
        "maman|La cloche, le soleil, ou la fleur ?",
        "papa|Tu choisis.",
    ),
}

T3 = {
    (1, 1, 1): L(
        "narrateur|Sarah prend le jaune, juste un trait.",
        "narrateur|Elle trace la cloche, ronde, sur la page.",
        "enfant-f|Elle sonne, Nina, comme dehors !",
        "narrateur|Le tin de la vraie cloche recouvre la fin.",
        "narrateur|Sarah s'immobilise, le crayon en l'air.",
        "narrateur|Elle refuse de foncer, et elle écoute.",
        "narrateur|Le tin s'éteint, et le cran luit, mince.",
        "enfant-f|Comme ça, la cloche.",
        "copine|Je t'entends, toute la phrase.",
        "narrateur|Sarah pose le crayon dans la boîte.",
        "narrateur|Nina ajoute un cercle, puis rend le bois.",
        "papa|Ça a failli rester dans ta main.",
    ),
    (1, 1, 2): L(
        "narrateur|Sarah trace un soleil, chaud, au milieu.",
        "narrateur|Le cran attrape la lumière, comme une lune.",
        "enfant-f|C'est mon cran, Nina, donc à moi !",
        "narrateur|Nina n'a pas fini sa phrase, à côté.",
        "copine|Moi, je voulais le jaune !",
        "narrateur|Sarah a envie de garder le bois, à cause du cran.",
        "narrateur|Elle regarde le croissant, puis la boîte.",
        "enfant-f|Le cran reste, même au milieu.",
        "narrateur|Elle pose le jaune, et Nina prend le soleil.",
        "narrateur|Un copeau dore le centre, fin.",
        "maman|Tu as vu le croissant, sans le garder.",
        "papa|Le soleil a son grain de bois.",
    ),
    (1, 1, 3): L(
        "narrateur|Sarah trace une fleur, cinq pétales.",
        "narrateur|Un copeau colle à un pétale, en croissant.",
        "enfant-f|Une fleur, Nina, et le jaune aussi !",
        "narrateur|Le taille-crayon roule, et couvre sa voix.",
        "copine|Je n'ai pas le dernier mot.",
        "narrateur|Sarah rattrape le bois, sans parler.",
        "narrateur|Elle attend le silence du taille-crayon.",
        "enfant-f|Le jaune, pour tes pétales.",
        "narrateur|Nina dessine deux feuilles, puis rend.",
        "narrateur|Le crayon rentre, tic.",
        "papa|Le copeau est resté, sur la fleur.",
        "maman|La phrase, elle, est arrivée entière.",
    ),
    (1, 2, 1): L(
        "narrateur|Sarah reprend le jaune, sous la cloche dessinée.",
        "narrateur|La gomme a pâli un bord, trop vite.",
        "enfant-f|Je répare, et je te le rends !",
        "narrateur|Nina commence : le tin, dehors.",
        "copine|J'entends la cloche, moi aussi.",
        "narrateur|Sarah ferme la bouche, la gomme posée.",
        "narrateur|Elle écoute Nina jusqu'au bout.",
        "enfant-f|Moi, après, le jaune est là.",
        "narrateur|Elle pose le crayon, et Nina trace un dong.",
        "narrateur|Un peu de jaune reste sous la gomme.",
        "papa|Tu as laissé sa cloche parler.",
        "maman|La tienne a attendu, puis elle a sonné.",
    ),
    (1, 2, 2): L(
        "narrateur|Sarah trace un soleil, puis s'arrête.",
        "narrateur|La gomme a mangé un rayon, par erreur.",
        "enfant-f|Attends, je corrige !",
        "narrateur|Nina parle d'un vrai soleil, à la vitre.",
        "narrateur|Sarah veut corriger, et couper.",
        "narrateur|Elle pose la gomme, et elle écoute.",
        "copine|Il est pâle, dehors.",
        "enfant-f|Le mien, après toi, plus net.",
        "narrateur|Elle rend le jaune, et Nina ajoute un rond.",
        "narrateur|Un grain blanc brille sur le soleil.",
        "maman|Le grain raconte l'erreur, sans honte.",
        "papa|Ta phrase est venue, entière, après la sienne.",
    ),
    (1, 2, 3): L(
        "narrateur|Sarah trace une fleur, un pétale trop fort.",
        "narrateur|La gomme l'adoucit, puis le crayon reste collé.",
        "enfant-f|Il est à ma main !",
        "copine|Sarah, j'ai besoin du jaune !",
        "narrateur|Sarah entend le début, et veut finir pour elle.",
        "narrateur|Elle ouvre les doigts, et le cran se décolle.",
        "enfant-f|Je t'écoute.",
        "copine|Un pétale, pour moi.",
        "narrateur|Nina prend le jaune, dessine, rend.",
        "narrateur|La fleur a un trait un peu pâle.",
        "papa|Ça a failli rester collé.",
        "maman|Tes doigts ont dit oui, avant ta bouche.",
    ),
    (1, 3, 1): L(
        "narrateur|Sarah ouvre le cahier, à la cloche.",
        "narrateur|Le crayon veut dormir dans le pli.",
        "enfant-f|Ma cloche, Nina, écoute-moi !",
        "narrateur|La page se referme, et mange le mot.",
        "copine|Je n'ai rien eu.",
        "narrateur|Sarah rouvre, lentement, sans crier.",
        "narrateur|Le cran brille dans la reliure, comme un indice.",
        "enfant-f|Il était là, pour toi, maintenant.",
        "narrateur|Elle le pose, et Nina dessine un battant.",
        "narrateur|La cloche du papier a un pli, mince.",
        "papa|La page a failli garder le bois.",
        "maman|Ta phrase est sortie, page ouverte.",
    ),
    (1, 3, 2): L(
        "narrateur|Sarah dessine un soleil, sur la page froide.",
        "narrateur|Le crayon glisse dans le pli, chaud.",
        "enfant-f|Il est à ma page !",
        "copine|Le mien n'a pas de jaune.",
        "narrateur|Sarah veut dire trop, trop vite.",
        "narrateur|Elle sort le bois, et elle attend Nina.",
        "copine|Je peux, un rayon ?",
        "enfant-f|Oui, après, la boîte.",
        "narrateur|Nina trace un rayon, rend le cran.",
        "narrateur|La page garde le soleil, un peu bombée.",
        "maman|Le pli n'a pas gagné.",
        "papa|Le cran est revenu au milieu.",
    ),
    (1, 3, 3): L(
        "narrateur|Sarah trace une fleur, dans le cahier.",
        "narrateur|La colle de la reliure sent fort.",
        "enfant-f|Cinq pétales, et j'ai fini !",
        "narrateur|Nina compte, en même temps, à voix haute.",
        "copine|Un, deux, trois, j'arrive !",
        "narrateur|Sarah s'arrête au quatrième, la bouche fermée.",
        "narrateur|Elle laisse Nina arriver à cinq.",
        "enfant-f|Le jaune, pour le cinquième.",
        "narrateur|Nina le prend, pose le dernier pétale, rend.",
        "narrateur|La reliure a une poussière jaune.",
        "papa|Tu as compté avec elle, sans couper.",
        "maman|La fleur est complète, et la boîte aussi.",
    ),
    (2, 1, 1): L(
        "narrateur|Près du casier, Sarah trace la cloche.",
        "narrateur|Le métal renvoie un faux tin, trop tôt.",
        "enfant-f|Elle sonne, Nina, écoute !",
        "narrateur|Le loquet claque, et coupe le mot.",
        "copine|Recommence, j'ai perdu.",
        "narrateur|Sarah a envie de frapper le métal.",
        "narrateur|Elle pose la main à plat, et elle attend.",
        "enfant-f|Dong, puis tin, comme ça.",
        "narrateur|Nina écoute, puis dessine le tin.",
        "narrateur|Le crayon rentre, et le casier se tait.",
        "papa|Le faux tin n'a pas eu ta phrase.",
        "maman|Le vrai, lui, t'a laissée finir.",
    ),
    (2, 1, 2): L(
        "narrateur|Près du casier, Sarah trace un soleil.",
        "narrateur|Un copeau tombe sur le métal, doré.",
        "enfant-f|C'est le cran, Nina, donc à moi !",
        "copine|Moi, je n'ai pas de soleil.",
        "narrateur|Sarah serre le taille-crayon, trop.",
        "narrateur|Elle le pose, et elle écoute Nina.",
        "copine|Un rayon, s'il te plaît.",
        "enfant-f|Le jaune, après ton rayon.",
        "narrateur|Nina dessine, rend, et le cran fait tic.",
        "narrateur|Le copeau sèche sur le métal, en croissant.",
        "papa|Le casier a gardé le copeau, pas le bois.",
        "maman|Toi, tu as gardé l'écoute.",
    ),
    (2, 1, 3): L(
        "narrateur|Près du casier, Sarah trace une fleur.",
        "narrateur|Le cartable est fermé, enfin.",
        "enfant-f|Cinq pétales, écoute-moi !",
        "narrateur|Un enfant claque un autre loquet, loin.",
        "narrateur|Sarah veut parler plus fort, par-dessus.",
        "narrateur|Elle attend le silence du couloir.",
        "copine|Je suis là.",
        "enfant-f|Le jaune, pour une feuille.",
        "narrateur|Nina dessine la feuille, rend le crayon.",
        "narrateur|Un copeau colle au loquet, mince.",
        "papa|Le clac d'à côté n'a pas gagné.",
        "maman|Ta fleur a eu toute la phrase.",
    ),
    (2, 2, 1): L(
        "narrateur|Près du casier, Sarah répare la cloche à la gomme.",
        "narrateur|Un bord trop noir s'en va, lentement.",
        "enfant-f|Le dong, Nina, il est là !",
        "narrateur|La gomme crisse, et mange le mot.",
        "copine|Le crissement, c'est tout.",
        "narrateur|Sarah arrête la gomme, et elle respire.",
        "enfant-f|Le dong, puis le tin.",
        "narrateur|Nina hoche la tête, prend le jaune.",
        "narrateur|Elle ajoute le tin, rend le bois.",
        "narrateur|La gomme a un peu de jaune, sous la cloche.",
        "papa|Le crissement a eu son tour.",
        "maman|Ta cloche, le sien, après.",
    ),
    (2, 2, 2): L(
        "narrateur|Près du casier, Sarah gomme un rayon de trop.",
        "narrateur|Le métal est froid, sous sa manche.",
        "enfant-f|Le soleil, il est à nous !",
        "copine|Attends, mon sac.",
        "narrateur|Sarah veut finir pendant le sac.",
        "narrateur|Elle tient le crayon, sans tracer.",
        "copine|Voilà, je t'écoute.",
        "enfant-f|Le jaune, un rayon pour toi.",
        "narrateur|Nina trace, rend, et un grain reste.",
        "narrateur|Le grain brille sur le soleil, près du métal.",
        "maman|Le sac a parlé, puis toi.",
        "papa|Le cran n'a pas quitté le milieu.",
    ),
    (2, 2, 3): L(
        "narrateur|Près du casier, Sarah gomme un pétale trop large.",
        "narrateur|Un rayon quitte le métal, lent.",
        "enfant-f|La fleur, Nina, elle est prête !",
        "narrateur|Nina chuchote au loquet, occupée.",
        "narrateur|Sarah a envie de la tirer par la manche.",
        "narrateur|Elle attend que Nina se tourne.",
        "copine|Oui ?",
        "enfant-f|Le jaune, un pétale net.",
        "narrateur|Nina dessine, rend, et la gomme reste ronde.",
        "narrateur|Un rayon manque, sur le casier, plus.",
        "papa|Tu n'as pas tiré la manche.",
        "maman|Elle s'est tournée, puis elle t'a eue.",
    ),
    (2, 3, 1): L(
        "narrateur|Près du casier, Sarah ouvre le cahier, cloche.",
        "narrateur|Le cahier veut rentrer dans le métal.",
        "enfant-f|Pas le casier, Nina, la page !",
        "narrateur|Le loquet claque sur le mot cloche.",
        "copine|La quoi ?",
        "narrateur|Sarah montre la page, sans crier.",
        "narrateur|Le cran luit, sur le papier.",
        "enfant-f|La cloche, le jaune, pour toi.",
        "narrateur|Nina dessine le battant, rend.",
        "narrateur|Le cahier rentre dans le casier, sans le bois.",
        "papa|Le loquet a eu le cahier, pas le jaune.",
        "maman|Ta main a montré, quand la voix a manqué.",
    ),
    (2, 3, 2): L(
        "narrateur|Près du casier, Sarah dessine un soleil, page entrevue.",
        "narrateur|Le crayon glisse vers le carton du sac.",
        "enfant-f|Il veut le sac, trop vite !",
        "narrateur|Sarah se tait, surprise du mot.",
        "narrateur|Elle rattrape le bois, sans phrase.",
        "copine|Tu disais ?",
        "enfant-f|Le jaune, un soleil, puis la boîte.",
        "narrateur|Nina ajoute un rond, rend le cran.",
        "narrateur|Une page jaune reste entrevue, dans le casier.",
        "papa|Le sac n'a pas gagné, cette fois.",
        "maman|Ta phrase est arrivée, sans le sac.",
        "narrateur|Le loquet tient, calme, sans clac.",
    ),
    (2, 3, 3): L(
        "narrateur|Près du casier, Sarah trace une fleur, page froide.",
        "narrateur|Le loquet du casier tient, prêt à claquer.",
        "enfant-f|Cinq, Nina, écoute-moi !",
        "copine|Je range, une seconde.",
        "narrateur|Sarah veut compter par-dessus le rangement.",
        "narrateur|Elle pose le crayon, et elle attend.",
        "copine|C'est bon.",
        "enfant-f|Le jaune, le cinquième pétale.",
        "narrateur|Nina le pose, rend, tic.",
        "narrateur|Le loquet tient, sans avoir le bois.",
        "papa|Le rangement a eu sa seconde.",
        "maman|Toi, ta fleur, après.",
    ),
    (3, 1, 1): L(
        "narrateur|Au rebord, Sarah trace la cloche, sur le cahier.",
        "narrateur|La buée a séché, un rond pâle.",
        "enfant-f|Dong, Nina, puis le tin !",
        "narrateur|Un vrai tin arrive, dehors, trop fort.",
        "copine|J'ai le tin, pas le dong.",
        "narrateur|Sarah veut crier le dong, par-dessus.",
        "narrateur|Elle attend que le tin finisse.",
        "enfant-f|Dong d'abord, puis ton tin.",
        "narrateur|Nina dessine le tin, rend le crayon.",
        "narrateur|La buée a disparu, autour de la cloche.",
        "papa|Le tin dehors a failli tout prendre.",
        "maman|Vous l'avez partagé, dong et tin.",
    ),
    (3, 1, 2): L(
        "narrateur|Au rebord, Sarah trace un soleil, contre la vitre.",
        "narrateur|Un copeau colle au rebord, en croissant.",
        "enfant-f|C'est le cran, donc à nous !",
        "copine|Le mien n'a pas de lumière.",
        "narrateur|Sarah veut garder le bois, pour le croissant.",
        "narrateur|Elle le pose, et elle écoute Nina.",
        "copine|Un peu de jaune, s'il te plaît.",
        "enfant-f|Le soleil, puis la boîte.",
        "narrateur|Nina dore un bord, rend.",
        "narrateur|Le copeau reste au rebord, collé.",
        "papa|Le croissant de bois n'est plus une excuse.",
        "maman|Il montre le chemin, vers le milieu.",
    ),
    (3, 1, 3): L(
        "narrateur|Au rebord, Sarah trace une fleur, près du froid.",
        "narrateur|Le rebord est nu, sans cahier un instant.",
        "enfant-f|Une fleur, Nina, pour toi !",
        "narrateur|Le taille-crayon bascule vers la vitre.",
        "copine|Il glisse !",
        "narrateur|Sarah le rattrape, et elle veut parler et tenir.",
        "narrateur|Elle tient d'abord, puis elle parle.",
        "enfant-f|Le jaune, un pétale, à toi.",
        "narrateur|Nina dessine, rend, et le rebord reste nu.",
        "narrateur|Un copeau manque, emporté par rien.",
        "papa|Tes mains ont choisi l'ordre.",
        "maman|Tenir, puis dire, la fleur est là.",
    ),
    (3, 2, 1): L(
        "narrateur|Au rebord, Sarah gomme un trop de buée sur la cloche.",
        "narrateur|La gomme sèche près de la fenêtre.",
        "enfant-f|La cloche, elle sonne !",
        "narrateur|Nina parle d'un nuage, dehors.",
        "copine|Le nuage cache le toit.",
        "narrateur|Sarah rentre son mot, la gomme arrêtée.",
        "enfant-f|Après le nuage, le jaune.",
        "narrateur|Nina prend, trace un battant, rend.",
        "narrateur|La gomme a un peu de jaune, près du carreau.",
        "papa|Le nuage a eu sa phrase.",
        "maman|La cloche, la tienne, ensuite.",
        "narrateur|La vitre ne fume plus, autour du dessin.",
    ),
    (3, 2, 2): L(
        "narrateur|Au rebord, Sarah gomme un rayon trop long.",
        "narrateur|Un rond de soleil reste au carreau.",
        "enfant-f|Le soleil, Nina, il est à moi !",
        "copine|À nous, si tu finis.",
        "narrateur|Sarah veut dire à moi, trop vite.",
        "narrateur|Elle écoute le à nous, jusqu'au bout.",
        "enfant-f|À nous, le jaune, au milieu.",
        "narrateur|Nina dore le rond, rend le cran.",
        "narrateur|Le carreau garde un soleil, pâle.",
        "papa|À nous a changé ta phrase.",
        "maman|Le cran a dit oui, dans la boîte.",
        "narrateur|La gomme repose, ronde, près du bois.",
    ),
    (3, 2, 3): L(
        "narrateur|Au rebord, Sarah gomme un pétale trop large.",
        "narrateur|La vitre ne fume plus, nette.",
        "enfant-f|La fleur, je la finis !",
        "narrateur|Un oiseau tapote le carreau, une fois.",
        "copine|Il a parlé, lui.",
        "narrateur|Sarah attend le tapotement, sans couper.",
        "enfant-f|Le jaune, après l'oiseau.",
        "narrateur|Nina dessine une feuille, rend.",
        "narrateur|La vitre reste nette, sans buée.",
        "papa|L'oiseau a eu son toc.",
        "maman|Toi, ta fleur, entière.",
        "narrateur|Un grain de gomme brille au rebord.",
    ),
    (3, 3, 1): L(
        "narrateur|Au rebord, Sarah ouvre le cahier, cloche ronde.",
        "narrateur|Le cahier voit le couloir, un peu.",
        "enfant-f|La cloche, Nina, comme dehors !",
        "narrateur|Une page se recourbe, et cache le dessin.",
        "copine|Je ne vois plus.",
        "narrateur|Sarah a envie d'aplatir et de parler ensemble.",
        "narrateur|Elle aplatit d'abord, puis elle parle.",
        "enfant-f|Comme dehors, le jaune, pour le tin.",
        "narrateur|Nina trace le tin, rend.",
        "narrateur|Le cahier voit le couloir, cloche visible.",
        "papa|La page recourbée a failli tout cacher.",
        "maman|Vous l'avez rouverte, ensemble.",
    ),
    (3, 3, 2): L(
        "narrateur|Au rebord, Sarah dessine un soleil, page recourbée.",
        "narrateur|La page se recourbe, froide, vers le vide.",
        "enfant-f|Elle tombe, le jaune aussi !",
        "copine|Tiens le bord !",
        "narrateur|Sarah tient, et elle veut expliquer trop vite.",
        "narrateur|Elle tient, sans expliquer, une seconde.",
        "enfant-f|Le jaune, un soleil, puis la boîte.",
        "narrateur|Nina aide à aplatir, dessine, rend.",
        "narrateur|La page se recourbe moins, soleil sauvé.",
        "papa|Tes mains ont parlé avant tes mots.",
        "maman|Le cran est au milieu, pas au vide.",
        "narrateur|Un pli reste, comme un sourire de papier.",
    ),
    (3, 3, 3): L(
        "narrateur|Au rebord, Sarah trace une fleur, poussière jaune.",
        "narrateur|Le rebord garde une poussière jaune, fine.",
        "enfant-f|Cinq pétales, et le cran aussi !",
        "copine|Le cran, c'est quoi ?",
        "narrateur|Sarah veut tout dire, d'un coup.",
        "narrateur|Elle montre le croissant, sans avaler Nina.",
        "enfant-f|Une marque, le jaune, pour toi.",
        "narrateur|Nina regarde, dessine, rend le bois.",
        "narrateur|La poussière jaune reste, sur le rebord.",
        "papa|Tu as montré, sans recouvrir sa question.",
        "maman|Le cran a servi, enfin.",
        "narrateur|La fleur a cinq pétales, et un tic au milieu.",
    ),
}

FINS = {
    (1, 1, 1): L(
        "narrateur|Ils partent, le cahier sous le bras.",
        "narrateur|Sur la page, la cloche a un copeau en croissant.",
        "enfant-f|C'est le cran, collé.",
        "maman|On a entendu ta phrase, à la fin.",
        "papa|Le tin s'est tu, dans le couloir.",
        "narrateur|La boîte garde le jaune, au milieu.",
        "narrateur|Un tic minuscule reste dans le bois de la table.",
    ),
    (1, 1, 2): L(
        "narrateur|Le soleil de la page dore la table, un peu.",
        "narrateur|Un copeau reste au centre, comme une lune.",
        "enfant-f|Nina a mis un rond.",
        "papa|Le cran a attrapé la lumière, puis lâché.",
        "maman|Le jaune est au milieu, pas dans ta poche.",
        "narrateur|La cloche, au bout, ne fait plus tin.",
        "narrateur|Un grain de bois dore le soleil, sans bouger.",
    ),
    (1, 1, 3): L(
        "narrateur|La fleur a cinq pétales, et un copeau.",
        "narrateur|Le taille-crayon se tait, près du bois.",
        "enfant-f|Nina a mis les feuilles.",
        "maman|Ta phrase est arrivée, après le bruit.",
        "papa|Le jaune est rentré, tic.",
        "narrateur|Les carreaux du couloir sont froids, sous les pas.",
        "narrateur|Un copeau colle à un pétale, et n'en bouge plus.",
    ),
    (1, 2, 1): L(
        "narrateur|La boîte est pleine, au milieu.",
        "narrateur|La gomme a un peu de jaune, sous la cloche.",
        "enfant-f|Nina a dessiné le dong.",
        "papa|Tu as laissé sa cloche parler.",
        "maman|La tienne a sonné, après.",
        "narrateur|Dehors, plus de tin, seulement des pas.",
        "narrateur|Un bord pâle garde le souvenir de la gomme.",
    ),
    (1, 2, 2): L(
        "narrateur|Le soleil a un grain blanc, sur un rayon.",
        "narrateur|La gomme est ronde, près de la boîte.",
        "enfant-f|Le vrai, dehors, était pâle.",
        "maman|Le tien a attendu, puis il a brillé.",
        "papa|Le jaune n'est plus collé à ta paume.",
        "narrateur|Papa prend les manteaux, sans parler par-dessus.",
        "narrateur|Un grain de gomme brille sur le soleil, oublié.",
    ),
    (1, 2, 3): L(
        "narrateur|Un grain blanc reste sur le bois.",
        "narrateur|La fleur a un trait un peu pâle.",
        "enfant-f|Mes doigts ont dit oui.",
        "papa|Avant ta bouche, oui.",
        "maman|Nina a eu son pétale.",
        "narrateur|Le savon des mains sent moins, dans le couloir.",
        "narrateur|La gomme garde une virgule jaune, secrète.",
    ),
    (1, 3, 1): L(
        "narrateur|Le cahier se ferme, sur la cloche à pli.",
        "narrateur|La reliure sent un peu la colle.",
        "enfant-f|Le battant, c'est Nina.",
        "maman|La page a failli garder le bois.",
        "papa|Il est au milieu, maintenant.",
        "narrateur|La vraie cloche, au bout, reste ronde, muette.",
        "narrateur|Un pli mince traverse la cloche de papier.",
    ),
    (1, 3, 2): L(
        "narrateur|Une page garde le soleil, un peu bombée.",
        "narrateur|Le crayon n'est plus dans le pli.",
        "enfant-f|Nina a mis un rayon.",
        "papa|Le cran est revenu au milieu.",
        "maman|Le pli n'a pas gagné.",
        "narrateur|Les casiers reçoivent un dernier rayon, étroit.",
        "narrateur|La page, fermée, tient le soleil au chaud.",
    ),
    (1, 3, 3): L(
        "narrateur|La reliure a une poussière jaune.",
        "narrateur|La fleur est complète, cinq et cinq.",
        "enfant-f|On a compté jusqu'au bout.",
        "maman|Sans se couper, oui.",
        "papa|Le jaune est dans la boîte.",
        "narrateur|Le couloir sent la colle, et le savon.",
        "narrateur|Une poussière jaune dort dans la reliure, paisible.",
    ),
    (2, 1, 1): L(
        "narrateur|Le casier ne claque plus.",
        "narrateur|Sur la page, le tin de Nina est net.",
        "enfant-f|Le faux tin n'a pas gagné.",
        "papa|Le vrai t'a laissée finir.",
        "maman|Le jaune est au milieu.",
        "narrateur|Le métal du loquet est froid, sans voix.",
        "narrateur|Un silence rond reste dans le couloir des casiers.",
    ),
    (2, 1, 2): L(
        "narrateur|Un copeau sèche sur le métal, en croissant.",
        "narrateur|Le soleil de Nina a un rayon de plus.",
        "enfant-f|Le casier a gardé le copeau.",
        "maman|Pas le bois, lui.",
        "papa|Toi, tu as gardé l'écoute.",
        "narrateur|Le cartable est fermé, sans jaune qui dépasse.",
        "narrateur|Le croissant de bois dore le loquet, minuscule.",
    ),
    (2, 1, 3): L(
        "narrateur|Le cartable est fermé, près du casier.",
        "narrateur|Un copeau colle au loquet, mince.",
        "enfant-f|Le clac d'à côté s'est tu.",
        "papa|Ta fleur a eu toute la phrase.",
        "maman|Nina a mis la feuille.",
        "narrateur|Les carreaux froids mènent vers la porte.",
        "narrateur|Un copeau jaune veille au loquet, comme un secret.",
    ),
    (2, 2, 1): L(
        "narrateur|La gomme tient près du casier, tachée.",
        "narrateur|Sous la cloche, un peu de jaune reste.",
        "enfant-f|Nina a mis le tin.",
        "maman|Le crissement a eu son tour.",
        "papa|Puis ta cloche.",
        "narrateur|Le métal ne renvoie plus de faux dong.",
        "narrateur|Une tache jaune dort sous la cloche de papier.",
    ),
    (2, 2, 2): L(
        "narrateur|Le métal est froid, sous un grain de gomme.",
        "narrateur|Le grain brille sur le soleil, près du casier.",
        "enfant-f|Le sac a parlé, puis moi.",
        "papa|Le cran n'a pas quitté le milieu.",
        "maman|Nina a eu son rayon.",
        "narrateur|Papa ouvre la porte, sans couvrir les voix.",
        "narrateur|Un grain blanc reste, accroché au soleil de page.",
    ),
    (2, 2, 3): L(
        "narrateur|Un rayon quitte le casier, puis plus.",
        "narrateur|La gomme reste ronde, près de la fleur.",
        "enfant-f|Je n'ai pas tiré la manche.",
        "maman|Elle s'est tournée, seule.",
        "papa|Le jaune est rentré.",
        "narrateur|Le couloir sent moins la craie, vers la sortie.",
        "narrateur|Un pétale net garde la place de Nina, claire.",
    ),
    (2, 3, 1): L(
        "narrateur|Le cahier rentre dans le casier, sans le bois.",
        "narrateur|Sur la page, le battant de Nina tient.",
        "enfant-f|Ma main a montré la cloche.",
        "papa|Quand la voix a manqué, oui.",
        "maman|Le loquet n'a pas eu le jaune.",
        "narrateur|Le tin de dehors s'éloigne, mince.",
        "narrateur|Un battant de papier garde le silence du métal.",
    ),
    (2, 3, 2): L(
        "narrateur|Une page jaune reste entrevue, dans le casier.",
        "narrateur|Le soleil de Nina a un rond, plein.",
        "enfant-f|Le sac n'a pas gagné.",
        "maman|Ta phrase est arrivée, nette.",
        "papa|Le loquet tient, sans clac.",
        "narrateur|Le cartable pèse moins, sans le crayon.",
        "narrateur|Une page entrevue dore l'ombre du casier.",
    ),
    (2, 3, 3): L(
        "narrateur|Le loquet du casier tient, sans le bois.",
        "narrateur|La fleur a son cinquième pétale, de Nina.",
        "enfant-f|Le rangement a eu sa seconde.",
        "papa|Toi, ta fleur, après.",
        "maman|Tic, au milieu.",
        "narrateur|Les sacs quittent le couloir, un à un.",
        "narrateur|Un loquet tient le silence, comme une oreille.",
    ),
    (3, 1, 1): L(
        "narrateur|La buée a séché, sur la vitre.",
        "narrateur|Dong et tin sont sur la page, ensemble.",
        "enfant-f|On a partagé la cloche.",
        "papa|Le tin dehors a failli tout prendre.",
        "maman|Vous l'avez coupé, juste.",
        "narrateur|Le rebord est froid, sans crayon qui glisse.",
        "narrateur|Un rond pâle de buée encadre la cloche de papier.",
    ),
    (3, 1, 2): L(
        "narrateur|Un copeau colle au rebord, en croissant.",
        "narrateur|Le soleil de Nina a un bord doré.",
        "enfant-f|Le croissant n'est plus une excuse.",
        "maman|Il montre le milieu, maintenant.",
        "papa|Le jaune est dans la boîte.",
        "narrateur|La vitre laisse un dernier rayon, étroit.",
        "narrateur|Le copeau du rebord dore le bois, sans partir.",
    ),
    (3, 1, 3): L(
        "narrateur|Le rebord est nu, froid, sans taille-crayon.",
        "narrateur|La fleur de Nina a un pétale de plus.",
        "enfant-f|Tenir, puis dire.",
        "papa|Tes mains ont choisi l'ordre.",
        "maman|Le jaune n'est pas par terre.",
        "narrateur|Un oiseau passe, dehors, sans tapoter.",
        "narrateur|Le rebord nu garde une trace de copeau, absente.",
    ),
    (3, 2, 1): L(
        "narrateur|La gomme sèche près de la fenêtre, tachée.",
        "narrateur|La vitre ne fume plus, autour de la cloche.",
        "enfant-f|Le nuage a eu sa phrase.",
        "maman|Puis ta cloche.",
        "papa|Nina a mis le battant.",
        "narrateur|Le couloir mène vers les manteaux, sans tin.",
        "narrateur|Un peu de jaune dort sur la gomme, près du carreau.",
    ),
    (3, 2, 2): L(
        "narrateur|Un rond de soleil reste au carreau.",
        "narrateur|La gomme repose, ronde, près du bois.",
        "enfant-f|À nous, elle a dit.",
        "papa|Ça a changé ta phrase.",
        "maman|Le cran a dit oui, au milieu.",
        "narrateur|Papa tend le manteau, et attend la fin.",
        "narrateur|Le carreau garde un soleil pâle, comme un secret.",
    ),
    (3, 2, 3): L(
        "narrateur|La vitre reste nette, sans buée.",
        "narrateur|Un grain de gomme brille au rebord.",
        "enfant-f|L'oiseau a eu son toc.",
        "maman|Toi, ta fleur, entière.",
        "papa|Nina a mis la feuille.",
        "narrateur|Le savon des mains sent, près de la porte.",
        "narrateur|Un grain blanc veille au rebord, oublié exprès.",
    ),
    (3, 3, 1): L(
        "narrateur|Le cahier voit le couloir, cloche visible.",
        "narrateur|La page n'est plus recourbée, sur le tin.",
        "enfant-f|On l'a rouverte, ensemble.",
        "papa|Elle a failli tout cacher.",
        "maman|Le jaune est au milieu.",
        "narrateur|La vraie cloche, au bout, reste ronde, sans tin.",
        "narrateur|Le cahier, sous le bras, voit les carreaux froids.",
    ),
    (3, 3, 2): L(
        "narrateur|La page se recourbe moins, soleil sauvé.",
        "narrateur|Un pli reste, comme un sourire de papier.",
        "enfant-f|Mes mains ont parlé.",
        "maman|Avant tes mots, oui.",
        "papa|Le cran n'est pas au vide.",
        "narrateur|Le rebord n'a plus de crayon qui roule.",
        "narrateur|Le pli-sourire garde le soleil, tout contre.",
    ),
    (3, 3, 3): L(
        "narrateur|Le rebord garde une poussière jaune, fine.",
        "narrateur|La fleur a cinq pétales, et un tic.",
        "enfant-f|Le cran a servi.",
        "papa|Tu as montré, sans recouvrir.",
        "maman|Nina a eu sa réponse, entière.",
        "narrateur|Ils quittent le couloir des casiers, sans se presser.",
        "narrateur|La poussière jaune reste, un croissant sur le rebord.",
    ),
}


SONS = {
    "CHK_T0000_P0000": "cloche,couloir",
    "CHK_T0001_P0001": "table,craie",
    "CHK_T0001_P0002": "casier,metal",
    "CHK_T0001_P0003": "vitre,buée",
}
SONS_T2 = {1: "taille-crayon,copeau", 2: "gomme", 3: "cahier,page"}
SONS_T3 = {1: "cloche", 2: "crayon", 3: "papier"}
SONS_FIN = {1: "cloche,silence", 2: "pas,porte", 3: "vitre"}

QMETA = {
    1: qf(
        "la boîte",
        "la boîte | boite | la boite | au milieu | dans la boîte",
        "La boîte est vide, au milieu. Le crayon va où ?",
        "Oui, dans la boîte.",
    ),
    2: qf(
        "la boîte",
        "la boîte | boite | la boite | au milieu | plus dans le sac",
        "Il dépasse du cartable. Sarah le met où ?",
        "Oui, dans la boîte.",
    ),
    3: qf(
        "la boîte",
        "la boîte | boite | la boite | au milieu | elle le pose",
        "Il glissait vers la vitre. Sarah le met où ?",
        "Oui, dans la boîte.",
    ),
}


def build() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {
        "CHK_T0000_P0000": DEBUT,
        "CHK_T0001_P0000": T1Q,
    }
    sons: dict[str, str] = dict(SONS)
    extras: dict[str, dict] = {
        "CHK_T0001_P0000": t3("la table", "le casier", "le rebord"),
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = T1[i]
        s[f"{p}_Q0001"] = Q1[i]
        extras[f"{p}_Q0001"] = QMETA[i]
        s[f"{p}_C0001"] = C1[i]
        s[f"{p}_T0002_P0000"] = T2Q[i]
        extras[f"{p}_T0002_P0000"] = t3("le taille-crayon", "la gomme", "le cahier")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = T2[(i, j)]
            sons[p2] = SONS_T2[j]
            s[f"{p2}_T0003_P0000"] = T3Q[i]
            extras[f"{p2}_T0003_P0000"] = t3("la cloche", "le soleil", "la fleur")
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
    out["characters"] = "Sarah, Nina, papa, maman"
    out["setting"] = "école, cloche, couloir des casiers, crayon jaune au cran en croissant"
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
        "il faut attendre",
        "bravo. tu as",
        "bon travail",
        "papa sourit",
        "maman sourit",
        "maîtresse",
        "maitresse",
        "aujourd'hui,",
        "mission accomplie",
        "j'ai compris !",
        "on dirait que notre mission",
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
        if c.get("kind") == "passage" and "_T0003_P000" in c["chunk_id"] and not c["chunk_id"].endswith("_P0000")
    ]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"{SID} T3 distincts: {len(set(t3s))}/{len(t3s)}")
    t2s = [
        c["text"]
        for c in out["chunks"]
        if c.get("kind") == "passage"
        and "_T0002_P000" in c["chunk_id"]
        and c["chunk_id"].count("_T000") == 2
        and not c["chunk_id"].endswith("_P0000")
        and "_T0003" not in c["chunk_id"]
    ]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"{SID} T2 distincts: {len(set(t2s))}/{len(t2s)}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    lo, hi, avg = path_words(scripts)
    print(f"chemins {lo}–{hi} mots (moyenne {avg:.0f})")
    if lo < 550 or hi > 720:
        raise SystemExit(f"{SID} longueur chemins {lo}–{hi} hors 550–720")
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
        "Sarah connaît le couloir des casiers. Un détail paraît neuf : le crayon "
        "jaune a un cran en croissant, et la cloche finit par un tin mince. "
        "Elle veut dessiner la cloche avant la prochaine sonnerie, puis laisser "
        "le jaune à Nina. Sa phrase se perd dans le tin. Table, casier ou rebord "
        "changent l'obstacle. Taille-crayon, gomme ou cahier cachent le jaune. "
        "Cloche, soleil ou fleur changent le dessin. Le cran et le tin paient la fin.\n\n"
        "## Vécu\n\n"
        "Sarah veut dessiner avec le crayon jaune avant la sonnerie, et le laisser "
        "à Nina. Première tentative : elle parle pendant le tin, personne n'entend. "
        "Sourire disparu, poitrine bousculée, maman s'accroupit. Table (voix qui "
        "se cognent), casier (crayon dans le sac), rebord (crayon vers le vide). "
        "Deuxième ruse : le jaune se cache dans le taille-crayon, la gomme ou le "
        "pli du cahier. Elle refuse de foncer, écoute, retrouve le cran. 27 fins : "
        f"copeau, grain, pli, buée, loquet, tin. Chemins {lo}–{hi} mots "
        f"(moyenne {avg:.0f}).\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Troupe D16 : Sarah, Nina, papa, maman. Pas de maîtresse.\n"
        "- 86 nœuds, graphe et libellés d'options conservés (table/casier/rebord ; "
        "taille-crayon/gomme/cahier ; cloche/soleil/fleur).\n"
        "- 27 fins textuellement distinctes, 27 T3 distincts, 9 T2 distincts.\n"
        "- Première tentative échoue. Chaque choix change l'obstacle, le climax, la dernière image.\n"
        "- Indice d'ouverture payé : cran en croissant, tin de la cloche, carreaux froids.\n"
        "- Tours de parole vécus : envie de couper, retenue, écoute réelle, plaisir d'être entendu.\n"
        "- TTS par fonction (ouverture, choix, indice, confirmation, action, obstacle, résolution, retour).\n"
        "- `slow` réservé aux choix, à l'indice et aux fins.\n"
        "- N3 ≤ 16 mots/phrase. Pas de leçon dite. Pas de tics « tout doux / encore / déjà / tout calme ».\n"
        "- Monde ≠ TREE-COL-002 (banc), ≠ TREE-COL-016 (craie, oiseau), ≠ TREE-COL-006 (vestiaire).\n"
        "- P1 F-NAR-019. Pas apply. Pas audio.\n\n"
        "## Direction vocale\n\n"
        "`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, "
        "tempo, sourire, respiration. Adulte conversationnel, pas maîtresse. "
        "Un merci vécu à la confirmation, pas un refrain Bravo.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
