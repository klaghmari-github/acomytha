#!/usr/bin/env python3
"""TREE-AUT-035 — F-NAR-019. Texte seulement. Pas d'audio. Pas d'apply."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _lib import FORBIDDEN, ROOT, check, from_script, words  # noqa: E402

HERE = Path(__file__).resolve().parent
SID = "TREE-AUT-035"
LIM = 16
TICS = re.compile(r"\b(encore|déjà|deja|tout doux|tout calme)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="fil d'argent",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=la cour l'appelle trop vite; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change la suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="radiateur",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=le métal a réchauffé les doigts; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="gant",
        note="arc=confirmation; intention=relancer; emotion=soulagement; intensite=1; destinataire=enfant; sous_texte=les mains peuvent tenir; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle veut trop vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=sans le gant ça glisse; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=la suite vient des mains tièdes; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="fil d'argent",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le fil a attendu; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > LIM:
            raise SystemExit(f"{n}>{LIM}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
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
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict) -> str:
    body = text
    emp = m.get("emphasis")
    if emp and emp in text:
        body = body.replace(emp, f"<emphasis>{emp}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitchTag"):
        body = f'<{m["pitchTag"]}>{body}</{m["pitchTag"]}>'
    tail = "[long-pause]" if m["pause"] >= 800 else ("[pause]" if m["pause"] >= 400 else "")
    return f"{body} {tail}".strip()


def apply_profile(src: dict, lines: list[str], profile: str, sons: str | None = None,
                  extra: dict | None = None, emphasis: str | None = None) -> dict:
    text, script = from_script(vet(lines))
    m = dict(PROFILES[profile])
    if emphasis is not None:
        m["emphasis"] = emphasis
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = "" if sons is None else sons
    nc["text_ssml"] = ssml(text, m)
    nc["text_xai_tags"] = xai(text, m)
    nc["length_scale_piper"] = m["piper"]
    nc["rate_label"] = m["rate"]
    nc["rate_wpm"] = m["wpm"]
    nc["speed_xai"] = m["speed"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitchSsml"]
    nc["pitch_xai_tag"] = m["pitchTag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = m.get("emphasis") or ""
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
    if extra:
        nc.update(extra)
    return nc


PLACE = {
    1: dict(lab="le bac à sable", ou="près du bac", son="sable,radiateur"),
    2: dict(lab="le toboggan", ou="près du toboggan", son="toboggan,goutte"),
    3: dict(lab="les balançoires", ou="près des balançoires", son="balancoire,chaine"),
}
OBJ = {
    1: dict(lab="le ballon", un="le ballon rouge", son="ballon"),
    2: dict(lab="le seau", un="le seau bleu", son="seau"),
    3: dict(lab="le doudou", un="le doudou beige", son="tissu"),
}
DEST = {
    1: dict(lab="le préau", ou="sous le préau", son="bois,pas"),
    2: dict(lab="la fontaine", ou="près de la fontaine", son="eau,goutte"),
    3: dict(lab="le cartable", ou="près du cartable", son="boucle,radiateur"),
}

OPENING = [
    "narrateur|Devant l'école du village, les dalles fumantes luisent.",
    "narrateur|Nina y arrive avec papa et maman.",
    "narrateur|Une averse vient de laver la cour.",
    "narrateur|Sur la vitre du vestiaire, un fil d'argent brille.",
    "narrateur|Il descend tout droit, mince comme un cheveu.",
    "narrateur|Dans la cour, une flaque ronde tient un morceau de ciel.",
    "narrateur|Les manteaux pèsent sur les crochets froids.",
    "narrateur|Un gant rouge a perdu sa paire, contre le mur.",
    "narrateur|Le radiateur fait tic, tic, près du zinc.",
    "narrateur|Papa frotte une botte sur le paillasson rêche.",
    "narrateur|Maman déboutonne le petit cartable bleu.",
    "maman|Tu as vu ce fil, Nina ?",
    "enfant-f|Oui, il file jusqu'à la flaque !",
    "narrateur|En ce moment, Nina tire la manche de son manteau.",
    "enfant-f|Je cours à la flaque, tout de suite !",
    "papa|Tes boutons, Nina ?",
    "narrateur|Elle pousse la porte sans fermer le manteau.",
    "narrateur|Le tissu lourd claque contre ses genoux.",
    "narrateur|Un gant rouge tombe près du radiateur.",
    "narrateur|Dehors, le vent pince ses doigts nus.",
    "enfant-f|Aïe, je n'arrive pas à tenir la poignée !",
    "narrateur|Nina s'arrête, les épaules basses.",
]

T1_CHOICE = [
    "narrateur|Nina veut la cour, malgré les doigts pincés.",
    "maman|On commence où, avec tes mains comme ça ?",
    "narrateur|Le bac à sable, le toboggan, ou les balançoires.",
]

ARRIVE = {
    1: [
        "narrateur|Nina court vers le bac, le manteau ouvert.",
        "narrateur|Le sable mouillé luit, gris et froid.",
        "narrateur|Une petite pelle jaune attend au bord.",
        "enfant-f|La pelle, je la prends !",
        "narrateur|Sa main nue serre le manche.",
        "narrateur|Le bois pique, et la pelle reste collée.",
        "enfant-f|Je n'y arrive pas.",
        "papa|Ton autre gant, il est où ?",
        "narrateur|Nina rentre au vestiaire, les épaules basses.",
        "narrateur|Les crochets sont froids sous ses doigts.",
        "narrateur|Le radiateur fait tic, contre le zinc.",
        "narrateur|Elle accroche le manteau, lourd, d'un coup.",
        "narrateur|Le gant rouge attend contre le mur.",
        "enfant-f|Toi, je t'avais oublié.",
        "narrateur|En le ramassant, sa main nue touche le zinc.",
        "narrateur|Le métal est tiède, et ses doigts s'ouvrent dessus.",
        "enfant-f|La pelle, maintenant.",
        "narrateur|Nina s'agenouille près du bac.",
        "narrateur|Le sable reste frais, mais ses mains tiennent.",
    ],
    2: [
        "narrateur|Nina pose un pied sur la marche du toboggan.",
        "narrateur|Le plastique jaune est mouillé, glissant.",
        "narrateur|Le manteau ouvert claque contre ses genoux.",
        "enfant-f|Je monte !",
        "narrateur|Sa main nue cherche la rampe.",
        "narrateur|Le métal pince, et elle lâche tout.",
        "enfant-f|C'est trop froid.",
        "papa|Le gant rouge est resté derrière.",
        "narrateur|Nina revient vers le vestiaire, sans parler.",
        "narrateur|Le radiateur ronronne, bas, contre le mur.",
        "narrateur|Elle accroche le manteau, et les boutons tapent.",
        "narrateur|L'autre gant rouge attend au pied du zinc.",
        "maman|Tu as trouvé le tiède ?",
        "narrateur|Elle pose les deux mains, et le tic marque le temps.",
        "enfant-f|Mes doigts reviennent.",
        "papa|La rampe t'attendra.",
        "narrateur|Nina reprend la première marche.",
        "narrateur|Une goutte pend sous le rebord, ronde.",
        "narrateur|Les deux gants tiennent la rampe, sans lâcher.",
    ],
    3: [
        "narrateur|Nina s'assoit sur le siège des balançoires.",
        "narrateur|Le bois est frais, et les chaînes font cling.",
        "narrateur|Une main gantée tient, l'autre reste nue.",
        "enfant-f|J'y vais !",
        "narrateur|La chaîne nue pince sa paume.",
        "narrateur|Elle ne peut pas pousser des deux côtés.",
        "enfant-f|Il me manque un gant.",
        "maman|Il est près du radiateur, je crois.",
        "narrateur|Nina quitte le siège, les épaules basses.",
        "narrateur|Au vestiaire, le radiateur fait tic, tic.",
        "narrateur|Elle accroche le manteau sur le crochet bas.",
        "narrateur|La paire de gants se retrouve, rouge contre rouge.",
        "papa|Le zinc est tiède, tu sens ?",
        "narrateur|Oui, les doigts se colorent, roses.",
        "enfant-f|Ils sont chauds.",
        "maman|Les chaînes, si tu veux.",
        "narrateur|Nina reprend le siège.",
        "narrateur|Les deux mains tiennent, et les chaînes acceptent.",
        "narrateur|La cour sent l'herbe mouillée, tout autour.",
    ],
}

# "tout autour" is not "tout calme" / "tout doux" - OK
# "Je n'y arrive pas." has one period.

Q = {
    1: [
        "narrateur|Nina n'arrivait pas à tenir la pelle, près du bac.",
        "maman|Elle a posé les mains où, près du tic ?",
    ],
    2: [
        "narrateur|Nina a lâché la rampe du toboggan, trop froide.",
        "papa|Elle a posé les mains où, au vestiaire ?",
    ],
    3: [
        "narrateur|Nina ne tenait qu'une chaîne, l'autre piquait.",
        "maman|Elle a posé les mains où, au vestiaire ?",
    ],
}

C = {
    1: [
        "papa|Oui, sur le radiateur.",
        "maman|Le gant rouge a retrouvé ta main.",
        "enfant-f|Mes doigts sont roses.",
        "papa|Merci d'être revenue le chercher.",
        "narrateur|Un grain de sable brille sur son genou.",
        "narrateur|La pelle jaune attend, et le manche cède.",
    ],
    2: [
        "maman|Oui, sur le radiateur.",
        "papa|Le manteau pèse au crochet, fermé.",
        "enfant-f|Je n'ai plus froid.",
        "maman|Merci pour tes boutons, Nina.",
        "narrateur|La goutte sous le rebord tombe, plic.",
        "narrateur|Le plastique jaune accepte ses deux gants.",
    ],
    3: [
        "papa|Oui, les mains sur le radiateur.",
        "maman|La paire de gants est complète.",
        "enfant-f|Je peux tenir les deux chaînes.",
        "papa|Merci, tes deux mains tiennent.",
        "narrateur|Une ombre d'oiseau passe sur le bois.",
        "narrateur|Le siège reste frais, mais les paumes tiennent.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Près du bac, trois choses l'attendent dans l'herbe.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Qu'est-ce que tes mains prennent ?",
    ],
    2: [
        "narrateur|Au pied du toboggan, trois choses brillent un peu.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Qu'est-ce que tes mains prennent ?",
    ],
    3: [
        "narrateur|Entre les chaînes, trois choses attendent leur tour.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Qu'est-ce que tes mains prennent ?",
    ],
}

PLAY = {
    (1, 1): [
        "narrateur|Le ballon rouge luit dans l'herbe courte, près du bac.",
        "enfant-f|Le ballon !",
        "narrateur|Nina le pousse trop vite, d'une main.",
        "narrateur|Il file vers la flaque et s'arrête au bord.",
        "enfant-f|Reviens !",
        "narrateur|Elle souffle, puis elle met les deux gants.",
        "narrateur|Les deux paumes rattrapent la peau mouillée.",
        "papa|Tu le tiens ?",
        "enfant-f|Oui, des deux mains.",
        "narrateur|Un grain de sable colle au ballon, doré.",
        "maman|Il reste avec toi ?",
        "enfant-f|Oui, maman.",
    ],
    (1, 2): [
        "narrateur|Le seau bleu a une anse qui brille, près du bac.",
        "enfant-f|Le seau !",
        "narrateur|Nina attrape l'anse trop vite.",
        "narrateur|Ting, le seau bascule, vide.",
        "enfant-f|Il m'a échappé.",
        "papa|Tu veux réessayer des deux mains ?",
        "narrateur|Elle reprend l'anse, et le métal ne pique plus.",
        "maman|Tu remplis un peu ?",
        "enfant-f|Oui, un peu de sable.",
        "narrateur|Le sable coule, chh, dans le bleu.",
        "narrateur|Nina pose le seau au bord du bac.",
        "papa|Il est à toi, maintenant.",
    ],
    (1, 3): [
        "narrateur|Le doudou beige attend sur le banc, près du bac.",
        "narrateur|Une oreille est pliée, un peu humide.",
        "enfant-f|Le doudou !",
        "narrateur|Nina le serre contre sa joue.",
        "narrateur|Le tissu froid la fait grimacer.",
        "enfant-f|Il a froid, lui aussi.",
        "maman|L'oreille, tu la mets où, au sec ?",
        "narrateur|Elle secoue, et un grain de sable tombe.",
        "narrateur|Elle l'assoit sur le bord de bois du bac.",
        "papa|Il t'attend, pendant que tu creuses ?",
        "enfant-f|Oui, il regarde la pelle.",
        "narrateur|Le tissu reprend une chaleur de main.",
    ],
    (2, 1): [
        "narrateur|Le ballon rouge attend dans l'herbe, au pied du toboggan.",
        "enfant-f|Le ballon, papa.",
        "narrateur|Nina le lance vers la rampe, trop fort.",
        "narrateur|Il rebondit et part vers la flaque.",
        "enfant-f|Oh non.",
        "papa|Deux mains, plus près de toi.",
        "narrateur|Elle le rattrape contre son manteau fermé.",
        "narrateur|La peau du ballon fait un petit bruit mou.",
        "maman|Tu as fini de le tenir ?",
        "enfant-f|Je le pose au pied de la rampe.",
        "narrateur|Le ballon reste, sans rouler.",
        "papa|Il ne part plus.",
    ],
    (2, 2): [
        "narrateur|Le seau bleu attend au pied des marches jaunes.",
        "enfant-f|Le seau, maman.",
        "narrateur|Nina soulève l'anse d'un coup.",
        "narrateur|Ting, une goutte du rebord tombe dedans.",
        "enfant-f|Il a pris l'eau tout seul.",
        "papa|Où tes pieds ne le pousseront pas ?",
        "narrateur|Elle le cale contre la première marche.",
        "maman|Il est à sa place ?",
        "enfant-f|Oui, papa.",
        "narrateur|L'anse ne pique plus sous le gant.",
        "narrateur|Un oiseau crie une fois, très haut.",
        "papa|On entend même le seau se taire.",
    ],
    (2, 3): [
        "narrateur|Le doudou beige attend sur le banc du préau.",
        "narrateur|Une oreille pliée touche le bois humide.",
        "enfant-f|Le doudou, maman.",
        "narrateur|Nina le prend, et le tissu sent la pluie.",
        "enfant-f|Il est mouillé.",
        "maman|Mets-le près de la rampe, du côté sec.",
        "narrateur|Elle cherche le côté où le plastique a séché.",
        "narrateur|Elle y pose le doudou, l'oreille dépliée.",
        "papa|Il est bien, là ?",
        "enfant-f|Oui, il va me voir glisser.",
        "narrateur|Le tissu se réchauffe contre le jaune.",
        "narrateur|Nina pose un gant sur l'oreille, une seconde.",
    ],
    (3, 1): [
        "narrateur|Le ballon rouge attend dans l'herbe, sous les chaînes.",
        "enfant-f|Le ballon, papa.",
        "narrateur|Nina le glisse entre deux chaînes, trop haut.",
        "narrateur|Les chaînes le pinceraient, alors il tombe.",
        "enfant-f|Pas là.",
        "papa|Plus bas, entre tes pieds.",
        "narrateur|Elle le pose dans l'herbe, contre le pied du cadre.",
        "narrateur|Le ballon fait un petit bruit de peau.",
        "maman|Il reste là ?",
        "enfant-f|Oui, il me regarde me balancer.",
        "narrateur|Les chaînes font cling, loin de lui.",
        "papa|Tu le regardes, un peu ?",
        "enfant-f|Un peu, papa.",
    ],
    (3, 2): [
        "narrateur|Le seau bleu attend sous le siège des balançoires.",
        "enfant-f|Le seau, maman.",
        "narrateur|Nina le pousse trop loin sous le bois.",
        "narrateur|Ting, l'anse cogne une chaîne.",
        "enfant-f|Il va se prendre les pieds.",
        "papa|Sors-le un peu, devant toi.",
        "narrateur|Elle le tire, et l'anse brille, sans piquer.",
        "maman|Il est à sa place ?",
        "enfant-f|Oui, papa.",
        "narrateur|Le seau reste vide, sage, dans l'herbe.",
        "narrateur|Une ombre d'oiseau passe sur le bleu.",
        "papa|On se balance, et lui attend.",
    ],
    (3, 3): [
        "narrateur|Le doudou beige attend sur le banc, face aux chaînes.",
        "narrateur|Une oreille pliée touche le bois frais.",
        "enfant-f|Le doudou, maman.",
        "narrateur|Nina l'assoit trop près d'une chaîne.",
        "narrateur|Le cling frôle l'oreille, alors elle recule le tissu.",
        "enfant-f|Pas trop près.",
        "maman|Sur le bois, un peu à côté.",
        "narrateur|Elle l'installe, et le tissu est chaud de ses mains.",
        "papa|Il est bien, là ?",
        "enfant-f|Oui, il attend son tour.",
        "narrateur|Les chaînes se taisent un moment.",
        "narrateur|Nina tient les deux chaînes, et le doudou la voit.",
    ],
}

# T2 (3,1) has 13 lines and last is enfant - 12-13 OK
# "On entend même le seau se taire." - 7 words

T3_Q = {
    (1, 1): [
        "narrateur|Le ballon a du sable, et Nina peut changer de place.",
        "maman|Le préau, la fontaine, ou le cartable ?",
        "papa|Où tes mains l'emmènent-elles ?",
    ],
    (1, 2): [
        "narrateur|Le seau a du sable, et le matin n'est pas fini.",
        "maman|Le préau, la fontaine, ou le cartable ?",
        "papa|Où vas-tu avec l'anse ?",
    ],
    (1, 3): [
        "narrateur|Le doudou a l'oreille sablée, près du bac.",
        "maman|Le préau, la fontaine, ou le cartable ?",
        "papa|Où l'emmènes-tu ?",
    ],
    (2, 1): [
        "narrateur|Le ballon luit au pied de la rampe.",
        "maman|Le préau, la fontaine, ou le cartable ?",
        "papa|Quelle suite, Nina ?",
    ],
    (2, 2): [
        "narrateur|Le seau garde une goutte, au pied des marches.",
        "maman|Le préau, la fontaine, ou le cartable ?",
        "papa|Quelle suite, Nina ?",
    ],
    (2, 3): [
        "narrateur|Le doudou sèche près de la rampe jaune.",
        "maman|Le préau, la fontaine, ou le cartable ?",
        "papa|Quelle suite, Nina ?",
    ],
    (3, 1): [
        "narrateur|Le ballon reste dans l'herbe, sous les chaînes.",
        "maman|Le préau, la fontaine, ou le cartable ?",
        "papa|Où le ballon t'accompagne-t-il ?",
    ],
    (3, 2): [
        "narrateur|Le seau attend devant le siège, vide et bleu.",
        "maman|Le préau, la fontaine, ou le cartable ?",
        "papa|Où l'anse t'emmène-t-elle ?",
    ],
    (3, 3): [
        "narrateur|Le doudou te regarde depuis le banc.",
        "maman|Le préau, la fontaine, ou le cartable ?",
        "papa|Où l'emmènes-tu ?",
    ],
}


def dest_preau(obj_line: str, unique: str, sit: str) -> list[str]:
    return [
        "narrateur|Sous le préau, des piliers de bois clair font de l'ombre.",
        "narrateur|Le sol dessous est sec, net, presque chaud.",
        "papa|On s'assoit un moment ?",
        "enfant-f|J'y vais.",
        "narrateur|Nina marche jusqu'au pilier. Ses bottes font toc toc.",
        sit,
        obj_line,
        "maman|Tu as faim, un peu ?",
        "enfant-f|Oui, un petit bout.",
        "narrateur|Maman sort un morceau de pomme, froid et sucré.",
        "narrateur|Nina le tient des deux mains roses.",
        unique,
    ]


def dest_fontaine(obj_line: str, unique: str, rinse: str) -> list[str]:
    return [
        "narrateur|La fontaine de la cour est une pierre grise, ronde.",
        "narrateur|Une goutte pend, puis tombe, plic.",
        "maman|Les mains, si tu veux.",
        "enfant-f|J'y vais.",
        "narrateur|Nina va jusqu'à la pierre. L'eau pince, puis passe.",
        rinse,
        obj_line,
        "papa|Tes mains sont propres ?",
        "enfant-f|Oui, elles sont froides un peu.",
        "narrateur|Papa tend un coin de mouchoir. Ça sent le savon.",
        "narrateur|Nina essuie paume après paume.",
        unique,
    ]


def dest_cartable(obj_line: str, unique: str, close: str) -> list[str]:
    return [
        "narrateur|Le cartable bleu attend près du vestiaire, un peu lourd.",
        "narrateur|La boucle est froide sous le pouce.",
        "papa|On ouvre ?",
        "enfant-f|J'ouvre.",
        "narrateur|Nina ouvre la boucle. Clic.",
        "narrateur|Un dessin à la craie est plié au fond.",
        close,
        obj_line,
        "maman|Tu refermes ?",
        "enfant-f|Oui.",
        "narrateur|Clic, le cartable redevient un carré fermé.",
        unique,
    ]


# dest_fontaine "Oui, elles sont froides un peu." OK
# dest_preau "Nina marche jusqu'au pilier. Ses bottes font toc toc." TWO SENTENCES - fix in actual calls

BODY_PARTS = {
    # i,j,k -> (obj_line, unique, extra_for_dest)
    (1, 1, 1): (
        "narrateur|Le ballon sablé se cale contre le pied du pilier.",
        "narrateur|Un grain de sable brille sur le rouge, sous le bois.",
        "narrateur|Elle s'assoit, et le bois lisse accepte son manteau fermé.",
    ),
    (1, 1, 2): (
        "narrateur|Nina passe le ballon sous le filet, une seconde.",
        "narrateur|Le grain de sable part avec l'eau.",
        "narrateur|Elle rince aussi la paume qui a tenu la pelle.",
    ),
    (1, 1, 3): (
        "narrateur|Le ballon sablé attend contre sa jambe, le temps du clic.",
        "narrateur|Le gant rouge a retrouvé sa paire, près de la boucle.",
        "narrateur|Elle pousse le dessin, tout au fond, sans le froisser.",
    ),
    (1, 2, 1): (
        "narrateur|Le seau pose son anse contre le pilier clair.",
        "narrateur|Nina pose la pomme un instant sur le bord du seau.",
        "narrateur|Elle s'assoit, et le bois lisse sent le sec.",
    ),
    (1, 2, 2): (
        "narrateur|Une goutte de fontaine tombe dans le seau sablé.",
        "narrateur|Nina mélange un peu, puis verse à côté, dans l'herbe.",
        "narrateur|Elle rince l'anse, là où le gant a tenu.",
    ),
    (1, 2, 3): (
        "narrateur|Le seau bleu se pose à côté de la boucle.",
        "narrateur|Le seau veille, et la paire rouge se touche.",
        "narrateur|Elle pousse le dessin au fond, puis reprend l'anse.",
    ),
    (1, 3, 1): (
        "narrateur|Le doudou s'assoit sur les genoux de Nina, sous le bois.",
        "narrateur|Un grain de sable quitte l'oreille pliée, sans bruit.",
        "narrateur|Elle s'assoit, et le doudou sent la pomme, tout près.",
    ),
    (1, 3, 2): (
        "narrateur|Nina pose le doudou sur la pierre sèche, loin du jet.",
        "narrateur|Elle rince ses doigts, pas le tissu.",
        "narrateur|L'oreille sablée attend, à l'abri.",
    ),
    (1, 3, 3): (
        "narrateur|Le doudou glisse contre le cartable, l'oreille sablée.",
        "narrateur|Le tissu touche la laine du manteau, au crochet.",
        "narrateur|Nina souffle le grain, puis pousse le dessin au fond.",
    ),
    (2, 1, 1): (
        "narrateur|Le ballon garde une trace mouillée de la rampe.",
        "narrateur|Nina le cale entre deux pieds de pilier, au sec.",
        "narrateur|Elle s'assoit, et la pomme réchauffe ses paumes roses.",
    ),
    (2, 1, 2): (
        "narrateur|Nina passe le ballon sous le filet, une seconde.",
        "narrateur|La trace de rampe s'en va avec l'eau.",
        "narrateur|Elle rince aussi la paume qui a tenu la rampe.",
    ),
    (2, 1, 3): (
        "narrateur|Le ballon attend au pied du cartable, un peu luisant.",
        "narrateur|Nina pousse le dessin au fond, la voile de craie pliée.",
        "narrateur|Le manteau, au crochet, ne claque plus.",
    ),
    (2, 2, 1): (
        "narrateur|Le seau sonne plus sourd, sous le bois du préau.",
        "narrateur|Nina y pose la pomme, le temps de s'asseoir.",
        "narrateur|Elle s'assoit, et l'anse ne pique plus.",
    ),
    (2, 2, 2): (
        "narrateur|L'anse du seau reçoit une goutte, et Nina l'essuie.",
        "narrateur|Elle verse l'eau du seau dans l'herbe, tout près.",
        "narrateur|Elle rince les doigts qui ont tenu la rampe.",
    ),
    (2, 2, 3): (
        "narrateur|Le seau tapote la boucle, ting, puis se tait.",
        "narrateur|L'anse reste contre le cuir, sans coincer.",
        "narrateur|Nina pousse le dessin au fond, à côté d'un crayon.",
    ),
    (2, 3, 1): (
        "narrateur|Le doudou sent le plastique jaune, même sous le préau.",
        "narrateur|Nina l'assoit contre le pilier, l'oreille dépliée.",
        "narrateur|Elle s'assoit, et la pomme se partage avec personne, juste lui.",
    ),
    (2, 3, 2): (
        "narrateur|Nina essuie l'oreille du doudou, loin de l'eau.",
        "narrateur|Elle rince ses propres doigts, pas le tissu.",
        "narrateur|Le doudou reste sur la pierre sèche, face à elle.",
    ),
    (2, 3, 3): (
        "narrateur|Le doudou veille près du dessin plié.",
        "narrateur|Nina pousse le dessin au fond, tout plat.",
        "narrateur|Le tissu se blottit contre la laine du manteau.",
    ),
    (3, 1, 1): (
        "narrateur|Le ballon se cale entre deux pieds de pilier.",
        "narrateur|Nina s'assoit, les chaînes loin, silencieuses.",
        "narrateur|La pomme tient dans ses deux gants.",
    ),
    (3, 1, 2): (
        "narrateur|Nina lave une poussière de chaîne, collée au ballon.",
        "narrateur|L'eau emporte le cling invisible.",
        "narrateur|Elle rince aussi la paume qui a tenu le fer.",
    ),
    (3, 1, 3): (
        "narrateur|Le ballon s'adosse au crochet du manteau.",
        "narrateur|Nina pousse le dessin au fond, sans coincer le rouge.",
        "narrateur|Les gants, par paire, se posent sur la boucle un instant.",
    ),
    (3, 2, 1): (
        "narrateur|Le seau fait une ombre ronde sous le préau.",
        "narrateur|Nina y pose la pomme, puis s'assoit contre le bois.",
        "narrateur|L'anse brille, loin des chaînes.",
    ),
    (3, 2, 2): (
        "narrateur|Nina pose le seau près de la pierre, pas dessous.",
        "narrateur|Elle rince ses doigts au-dessus de l'herbe, pas du bleu.",
        "narrateur|Une goutte choisit la pierre, pas l'anse.",
    ),
    (3, 2, 3): (
        "narrateur|Le seau bleu reste à côté de la boucle.",
        "narrateur|Ting, le cartable et le seau se taisent ensemble.",
        "narrateur|Nina pousse le dessin au fond, puis tapote l'anse.",
    ),
    (3, 3, 1): (
        "narrateur|Le doudou s'adosse au pilier, loin des chaînes.",
        "narrateur|Nina s'assoit, et l'oreille pliée se déplie sur ses genoux.",
        "narrateur|La pomme sent le tissu, tout près.",
    ),
    (3, 3, 2): (
        "narrateur|Le doudou écoute la goutte, sans s'approcher.",
        "narrateur|Nina rince ses doigts, le tissu au sec sur la pierre.",
        "narrateur|L'oreille reste dépliée, face à l'eau.",
    ),
    (3, 3, 3): (
        "narrateur|Le doudou se blottit contre la laine du manteau.",
        "narrateur|Nina pousse le dessin au fond, l'oreille hors du cartable.",
        "narrateur|Le crochet porte le manteau, et le doudou le garde.",
    ),
}

# Fix two-sentence issues in dest_* helpers - I'll not use the two-sentence versions.
# dest_preau has: "narrateur|Nina marche jusqu'au pilier. Ses bottes font toc toc."
# I'll pass sit as that line split, and rewrite helpers.


def body(i: int, j: int, k: int) -> list[str]:
    obj_line, unique, extra = BODY_PARTS[(i, j, k)]
    if k == 1:
        return [
            "narrateur|Sous le préau, des piliers de bois clair font de l'ombre.",
            "narrateur|Le sol dessous est sec, net, presque chaud.",
            "papa|On s'assoit un moment ?",
            "enfant-f|J'y vais.",
            "narrateur|Nina marche jusqu'au pilier, bottes en toc toc.",
            extra,
            obj_line,
            "maman|Tu as faim, un peu ?",
            "enfant-f|Oui, un petit bout.",
            "narrateur|Maman sort un morceau de pomme, froid et sucré.",
            "narrateur|Nina le tient des deux mains roses.",
            unique,
        ]
    if k == 2:
        return [
            "narrateur|La fontaine de la cour est une pierre grise, ronde.",
            "narrateur|Une goutte pend, puis tombe, plic.",
            "maman|Les mains, si tu veux.",
            "enfant-f|J'y vais.",
            "narrateur|Nina va jusqu'à la pierre. L'eau pince, puis passe.",
            extra,
            obj_line,
            "papa|Tes mains sont propres ?",
            "enfant-f|Oui, elles sont froides un peu.",
            "narrateur|Papa tend un coin de mouchoir. Ça sent le savon.",
            unique,
        ]
    return [
        "narrateur|Le cartable bleu attend près du vestiaire, un peu lourd.",
        "narrateur|La boucle est froide sous le pouce.",
        "papa|On ouvre ?",
        "enfant-f|J'ouvre.",
        "narrateur|Nina ouvre la boucle, clic, sans la forcer.",
        "narrateur|Un dessin à la craie est plié au fond.",
        extra,
        obj_line,
        "maman|Tu refermes ?",
        "enfant-f|Oui.",
        "narrateur|Clic. Le cartable redevient un carré fermé.",
        unique,
    ]


# body k=2 has two two-sentence lines:
# "Nina va jusqu'à la pierre. L'eau pince, puis passe."
# "Papa tend un coin de mouchoir. Ça sent le savon."
# k=3: "Clic. Le cartable redevient un carré fermé."
# I'll fix in the function below by rewriting those lines when I clean.

# Also k=1 extra for (3,1,1): "Nina s'assoit. Les chaînes sont loin, enfin silencieuses." TWO
# Several BODY_PARTS extras have two sentences. I need to fix ALL of them.

# Let me rewrite BODY_PARTS and body() cleanly in a second pass after running vet.

FINS: dict[tuple[int, int, int], list[str]] = {}


def make_fins() -> None:
    data = {
        (1, 1, 1): [
            "narrateur|Sous le préau, un grain de sable brille sur le ballon.",
            "enfant-f|Il a voyagé avec moi.",
            "maman|Tes deux mains l'ont gardé.",
            "narrateur|Nina croque la pomme, les paumes restent roses.",
            "narrateur|Derrière la vitre, le fil d'argent tient bon.",
            "narrateur|Une goutte glisse le long du fil, sans le casser.",
            "papa|La flaque tient toujours son bout de ciel.",
            "narrateur|Au vestiaire, le radiateur fait tic, très bas.",
        ],
        (1, 1, 2): [
            "narrateur|Sur le ballon, plus de sable : l'eau l'a pris.",
            "enfant-f|Il ne glisse plus.",
            "papa|Tes gants l'ont rattrapé, à la fin.",
            "narrateur|Nina essuie la dernière goutte avec le mouchoir.",
            "narrateur|Dans la flaque, le fil d'argent se reflète, mince.",
            "maman|Tu le vois, depuis la pierre ?",
            "enfant-f|Oui, il va jusqu'à l'eau.",
            "narrateur|Le radiateur, derrière, continue son tic patient.",
        ],
        (1, 1, 3): [
            "narrateur|Le ballon s'appuie contre le cartable fermé.",
            "enfant-f|Le dessin est au chaud.",
            "maman|Et tes gants sont deux, sur la boucle.",
            "narrateur|Nina pose la paire, rouge contre rouge.",
            "narrateur|Le manteau pèse au crochet, sans claquer.",
            "papa|Le fil d'argent touche presque le gant, dans la vitre.",
            "enfant-f|Il m'a attendue.",
            "narrateur|Le radiateur répond, tic, tout près du zinc.",
        ],
        (1, 2, 1): [
            "narrateur|La pomme a laissé un cercle humide sur le seau.",
            "enfant-f|Mon seau a servi d'assiette.",
            "papa|Tes mains tenaient l'anse, et la pomme.",
            "narrateur|Nina rit, bas, sous le bois clair.",
            "narrateur|Le fil d'argent coupe la vitre en deux parts nettes.",
            "maman|L'une pour la cour, l'autre pour nous.",
            "narrateur|Au loin, le bac garde un trou de pelle.",
            "narrateur|Le radiateur, lui, garde son tic.",
        ],
        (1, 2, 2): [
            "narrateur|Dans le seau, plus de sable : une goutte propre.",
            "enfant-f|Je l'ai versé dans l'herbe.",
            "maman|L'anse n'a plus piqué.",
            "narrateur|Nina essuie le bleu avec le coin du mouchoir.",
            "narrateur|Le fil d'argent tremble quand la goutte de fontaine tombe.",
            "papa|Il est solide, ce cheveu de vitre.",
            "enfant-f|Comme l'anse, maintenant.",
            "narrateur|Le tic du radiateur arrive jusqu'ici, très mince.",
        ],
        (1, 2, 3): [
            "narrateur|Le seau bleu veille la boucle, comme un gardien.",
            "enfant-f|Le dessin est derrière, au fond.",
            "papa|Tu as ouvert, puis fermé.",
            "narrateur|Nina tapote l'anse, ting, une dernière fois.",
            "narrateur|Sur la vitre, le fil d'argent passe au-dessus du crochet.",
            "maman|Ton manteau est là, et toi ici.",
            "enfant-f|Mes gants aussi.",
            "narrateur|Le radiateur fait tic, et le seau se tait.",
        ],
        (1, 3, 1): [
            "narrateur|Le doudou a senti la pomme, sous le préau.",
            "enfant-f|Il n'a plus l'oreille sablée.",
            "maman|Tu l'as installé au sec.",
            "narrateur|Nina pose sa joue un instant sur le tissu.",
            "narrateur|Le fil d'argent brille, mince, au-dessus du banc.",
            "papa|Il n'a pas bougé, pendant que tu creusais.",
            "enfant-f|Moi si, et je suis revenue.",
            "narrateur|Le radiateur tic, et l'oreille reste dépliée.",
        ],
        (1, 3, 2): [
            "narrateur|Le doudou reste sur la pierre sèche, loin du jet.",
            "enfant-f|Lui n'a pas d'eau, moi si.",
            "papa|Tes doigts sont propres, son oreille aussi.",
            "narrateur|Nina essuie ses paumes, puis touche le tissu.",
            "narrateur|Le fil d'argent se mire dans la flaque, pas dans la fontaine.",
            "maman|Deux eaux, et lui au milieu, au sec.",
            "enfant-f|C'est sa place.",
            "narrateur|Le tic du radiateur reste derrière la porte.",
        ],
        (1, 3, 3): [
            "narrateur|Le doudou se blottit contre la laine, près du cartable.",
            "enfant-f|Il garde le manteau.",
            "maman|Et le dessin dort au fond.",
            "narrateur|Nina ferme la boucle d'un pouce ganté.",
            "narrateur|Le fil d'argent descend jusqu'au gant, dans le reflet.",
            "papa|La paire est complète, contre le zinc.",
            "enfant-f|Je peux rentrer, si tu veux.",
            "narrateur|Le radiateur répond tic, comme une petite horloge.",
        ],
        (2, 1, 1): [
            "narrateur|Le ballon a séché entre les pieds du pilier.",
            "enfant-f|La rampe ne l'a pas gardé.",
            "papa|Tes deux gants, si.",
            "narrateur|Nina pose la pomme, puis le ballon, contre son genou.",
            "narrateur|Le fil d'argent coupe un carré de ciel, sur la vitre.",
            "maman|Tu l'as vu, avant de courir ?",
            "enfant-f|Oui, et il est toujours là.",
            "narrateur|Le radiateur, au vestiaire, reprend son tic.",
        ],
        (2, 1, 2): [
            "narrateur|L'eau a pris la trace de rampe, sur le ballon.",
            "enfant-f|Il est lisse, maintenant.",
            "maman|Comme tes paumes, après le mouchoir.",
            "narrateur|Nina souffle sur une goutte, et elle part.",
            "narrateur|Le fil d'argent suit la pente de la vitre, vers la flaque.",
            "papa|La même pente que le toboggan, presque.",
            "enfant-f|Mais sans le froid.",
            "narrateur|Le tic du métal tiède reste dans ses doigts.",
        ],
        (2, 1, 3): [
            "narrateur|Le ballon luisant veille le cartable fermé.",
            "enfant-f|Le dessin a une voile, au fond.",
            "papa|Comme toi, sur la rampe.",
            "narrateur|Nina pose un gant sur le cuir, une seconde.",
            "narrateur|Le fil d'argent passe devant le crochet, dans la vitre.",
            "maman|Le manteau ne claque plus.",
            "enfant-f|Les boutons tiennent.",
            "narrateur|Le radiateur fait tic, et la boucle se tait.",
        ],
        (2, 2, 1): [
            "narrateur|La pomme a sonné sourd, posée dans le seau.",
            "enfant-f|Mon seau fait une table, sous le bois.",
            "maman|L'anse n'a plus piqué, depuis les gants.",
            "narrateur|Nina croque, et le préau sent la pomme froide.",
            "narrateur|Le fil d'argent reste droit, mince comme un cheveu.",
            "papa|Il n'a pas glissé, lui.",
            "enfant-f|Moi, au début, si.",
            "narrateur|Le radiateur tic, et Nina sourit vers la vitre.",
        ],
        (2, 2, 2): [
            "narrateur|Nina a versé l'eau du seau dans l'herbe, près de la pierre.",
            "enfant-f|L'anse est sèche.",
            "papa|Tes doigts aussi, grâce au mouchoir.",
            "narrateur|Une goutte de fontaine choisit la pierre, pas le bleu.",
            "narrateur|Le fil d'argent tremble, puis se calme sur le verre.",
            "maman|Tu l'as regardé, avant la rampe ?",
            "enfant-f|Oui, il m'a fait de l'œil.",
            "narrateur|Le tic du radiateur lui répond, de loin.",
        ],
        (2, 2, 3): [
            "narrateur|Le seau et le cartable se taisent, côte à côte.",
            "enfant-f|Ting, puis clic, c'est fini.",
            "maman|Ouvert, puis fermé, comme tes boutons.",
            "narrateur|Nina pose l'anse contre le cuir, sans la coincer.",
            "narrateur|Le fil d'argent barre la vitre au-dessus du zinc.",
            "papa|Le gant rouge est à sa place, contre le mur.",
            "enfant-f|Les deux.",
            "narrateur|Le radiateur tic, et le vestiaire sent la laine.",
        ],
        (2, 3, 1): [
            "narrateur|Le doudou sent le jaune du toboggan, même au sec.",
            "enfant-f|Il m'a vue glisser.",
            "papa|Toi, tu l'as mis du côté sec.",
            "narrateur|Nina partage la pomme avec personne, juste le tissu.",
            "narrateur|Le fil d'argent brille au-dessus de la rampe, dans la vitre.",
            "maman|Il descendait vers la flaque, ce matin.",
            "enfant-f|J'y suis allée, après le gant.",
            "narrateur|Le radiateur tic, et l'oreille reste dépliée.",
        ],
        (2, 3, 2): [
            "narrateur|Le doudou reste sur la pierre sèche, l'oreille propre.",
            "enfant-f|L'eau, c'est pour mes mains.",
            "maman|Pas pour lui.",
            "narrateur|Nina essuie ses paumes, puis caresse le tissu.",
            "narrateur|Le fil d'argent se mire dans la flaque, loin de la fontaine.",
            "papa|Deux eaux, et une oreille au sec.",
            "enfant-f|C'est bien comme ça.",
            "narrateur|Le tic du radiateur reste au vestiaire, patient.",
        ],
        (2, 3, 3): [
            "narrateur|Le doudou veille le dessin, contre la laine.",
            "enfant-f|Il n'est pas dans le cartable.",
            "papa|Il a sa place, au crochet, avec le manteau.",
            "narrateur|Nina ferme la boucle, et le tissu reste dehors, au chaud.",
            "narrateur|Le fil d'argent touche le reflet du gant rouge.",
            "maman|La paire est là.",
            "enfant-f|Je l'ai cherchée.",
            "narrateur|Le radiateur tic, tout contre le zinc.",
        ],
        (3, 1, 1): [
            "narrateur|Le ballon dort entre les pieds du pilier, loin des chaînes.",
            "enfant-f|Il ne s'envole plus.",
            "maman|Tu l'as mis trop haut, au premier essai.",
            "narrateur|Nina croque la pomme, les deux gants fermés sur le fruit.",
            "narrateur|Le fil d'argent coupe le ciel de la vitre, très net.",
            "papa|Les chaînes se taisent, de l'autre côté.",
            "enfant-f|Moi, je tiens les deux, maintenant.",
            "narrateur|Le radiateur tic, et le bois du préau sent le sec.",
        ],
        (3, 1, 2): [
            "narrateur|L'eau a pris la poussière de chaîne, sur le ballon.",
            "enfant-f|Plus de cling sur la peau.",
            "papa|Tes paumes non plus ne piquent plus.",
            "narrateur|Nina essuie le rouge, puis le pose sur l'herbe sèche.",
            "narrateur|Le fil d'argent descend vers la flaque, comme une piste.",
            "maman|Tu voulais y courir, trop vite.",
            "enfant-f|J'ai pris le gant, avant.",
            "narrateur|Le tic du radiateur lui a marqué les doigts.",
        ],
        (3, 1, 3): [
            "narrateur|Le ballon s'adosse au crochet, sous le manteau.",
            "enfant-f|Les gants sont sur la boucle, un instant.",
            "maman|Puis dans tes poches, si tu veux.",
            "narrateur|Nina glisse la paire, rouge, dans la poche droite.",
            "narrateur|Le fil d'argent barre le gant, dans le reflet de la vitre.",
            "papa|Le cartable est fermé, le siège est vide.",
            "enfant-f|Les chaînes peuvent attendre.",
            "narrateur|Le radiateur tic, et le zinc est tiède.",
        ],
        (3, 2, 1): [
            "narrateur|L'ombre ronde du seau dort sous le préau.",
            "enfant-f|L'anse a quitté les chaînes.",
            "papa|Tu l'as tiré devant toi, à temps.",
            "narrateur|Nina pose la pomme dans le bleu, puis la reprend.",
            "narrateur|Le fil d'argent reste droit, au-dessus de la cour.",
            "maman|Il n'a pas bougé, lui.",
            "enfant-f|Le seau, si, et c'est mieux.",
            "narrateur|Le radiateur tic, loin du cling.",
        ],
        (3, 2, 2): [
            "narrateur|Une goutte choisit la pierre, pas l'anse du seau.",
            "enfant-f|Mon bleu reste sec.",
            "maman|Tes doigts, eux, ont pris l'eau, puis le mouchoir.",
            "narrateur|Nina pose le seau dans l'herbe, à côté de la fontaine.",
            "narrateur|Le fil d'argent tremble dans la flaque, pas dans le jet.",
            "papa|Tu as séparé les deux eaux.",
            "enfant-f|Oui, pour l'anse.",
            "narrateur|Le tic du radiateur arrive, mince, jusqu'à la pierre.",
        ],
        (3, 2, 3): [
            "narrateur|Le seau et le cartable se taisent, ting puis clic.",
            "enfant-f|Ils font une paire, eux aussi.",
            "papa|Comme tes gants.",
            "narrateur|Nina pose l'anse contre le cuir, puis recule d'un pas.",
            "narrateur|Le fil d'argent passe au-dessus du crochet, dans la vitre.",
            "maman|Le manteau est là, fermé.",
            "enfant-f|Je l'ai accroché, avant les chaînes.",
            "narrateur|Le radiateur tic, et le vestiaire sent le savon du mouchoir.",
        ],
        (3, 3, 1): [
            "narrateur|Le doudou a déplié son oreille, sur les genoux de Nina.",
            "enfant-f|Les chaînes sont loin.",
            "maman|Tu l'as reculé, quand le cling l'a frôlé.",
            "narrateur|Nina pose la pomme, puis le tissu, puis sa joue.",
            "narrateur|Le fil d'argent brille, mince, au-dessus du banc vide.",
            "papa|Il t'a attendue, ce fil.",
            "enfant-f|Moi aussi, je l'ai regardé, après.",
            "narrateur|Le radiateur tic, et le préau garde leur silence.",
        ],
        (3, 3, 2): [
            "narrateur|Le doudou écoute la goutte, l'oreille au sec.",
            "enfant-f|Il n'a pas bougé vers l'eau.",
            "papa|Toi, tu as rincé tes doigts, pas lui.",
            "narrateur|Nina essuie ses paumes, puis caresse le tissu.",
            "narrateur|Le fil d'argent se mire dans la flaque, ronde comme un œil.",
            "maman|C'est le ciel de ce matin, là-dedans.",
            "enfant-f|Et le fil, dessus.",
            "narrateur|Le tic du radiateur reste derrière, au chaud.",
        ],
        (3, 3, 3): [
            "narrateur|Le doudou garde le manteau, l'oreille hors du cartable.",
            "enfant-f|Le dessin est au fond, pas lui.",
            "maman|Chacun sa place.",
            "narrateur|Nina ferme la boucle, et le crochet porte tout le lourd.",
            "narrateur|Le fil d'argent descend jusqu'au gant, dans le verre.",
            "papa|La paire rouge se touche, enfin.",
            "enfant-f|Je l'ai faite, la paire.",
            "narrateur|Le radiateur tic, et la vitre rend le fil, tout mince.",
        ],
    }
    # "enfin" in (3,3,3) papa line - not a tic
    # "tout mince" not "tout doux"
    # (2,2,2) "se calme" - not "tout calme"
    FINS.update(data)


make_fins()


def fix_two_sentences() -> None:
    """Rewrite body() lines that contain two sentence marks — handled in body()."""
    return


# Rewrite body() without two-sentence lines.
def body(i: int, j: int, k: int) -> list[str]:  # noqa: F811
    obj_line, unique, extra = BODY_PARTS[(i, j, k)]
    # Split extras that contain two sentences at runtime via vet.
    if k == 1:
        return [
            "narrateur|Sous le préau, des piliers de bois clair font de l'ombre.",
            "narrateur|Le sol dessous est sec, net, presque chaud.",
            "papa|On s'assoit un moment ?",
            "enfant-f|J'y vais.",
            "narrateur|Nina marche jusqu'au pilier, bottes en toc toc.",
            extra,
            obj_line,
            "maman|Tu as faim, un peu ?",
            "enfant-f|Oui, un petit bout.",
            "narrateur|Maman sort un morceau de pomme, froid et sucré.",
            "narrateur|Nina le tient des deux mains roses.",
            unique,
        ]
    if k == 2:
        return [
            "narrateur|La fontaine de la cour est une pierre grise, ronde.",
            "narrateur|Une goutte pend, puis tombe, plic.",
            "maman|Les mains, si tu veux.",
            "enfant-f|J'y vais.",
            "narrateur|Nina va jusqu'à la pierre, où l'eau pince puis passe.",
            extra,
            obj_line,
            "papa|Tes mains sont propres ?",
            "enfant-f|Oui, elles sont froides un peu.",
            "narrateur|Papa tend un coin de mouchoir, et ça sent le savon.",
            unique,
        ]
    return [
        "narrateur|Le cartable bleu attend près du vestiaire, un peu lourd.",
        "narrateur|La boucle est froide sous le pouce.",
        "papa|On ouvre ?",
        "enfant-f|J'ouvre.",
        "narrateur|Nina ouvre la boucle, clic, sans la forcer.",
        "narrateur|Un dessin à la craie est plié au fond.",
        extra,
        obj_line,
        "maman|Tu refermes ?",
        "enfant-f|Oui.",
        "narrateur|Clic, le cartable redevient un carré fermé.",
        unique,
    ]


Q_EXTRA = {
    "expected_answer": "radiateur",
    "accepted_examples": "radiateur | le radiateur | vestiaire | le vestiaire | le gant | manteau | le manteau | les mains | le métal",
    "retry_prompt": "Le métal fait tic, contre le mur. Où a-t-elle posé les mains ?",
}


def path_words(scripts: dict, a: int, b: int, c: int) -> int:
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
    n = 0
    for i in ids:
        n += words(from_script(scripts[i])[0])
    return n


def build() -> None:
    src = json.loads((HERE / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, list[str]] = {}
    out_chunks = []

    def put(cid: str, lines: list[str], profile: str, sons: str = "", extra: dict | None = None,
            emphasis: str | None = None) -> None:
        scripts[cid] = vet(lines)
        out_chunks.append(
            apply_profile(by_src[cid], scripts[cid], profile, sons=sons, extra=extra, emphasis=emphasis)
        )

    put("CHK_T0000_P0000", OPENING, "opening", sons="radiateur,goutte,vitre")
    put("CHK_T0001_P0000", T1_CHOICE, "choice", extra={
        "option_1_label": "le bac à sable",
        "option_2_label": "le toboggan",
        "option_3_label": "les balançoires",
    })

    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        put(p, ARRIVE[i], "obstacle", sons=PLACE[i]["son"])
        put(f"{p}_Q0001", Q[i], "clue", extra=dict(Q_EXTRA), emphasis="mains")
        put(f"{p}_C0001", C[i], "confirm", sons="radiateur")
        put(f"{p}_T0002_P0000", T2_CHOICE[i], "choice", extra={
            "option_1_label": "le ballon",
            "option_2_label": "le seau",
            "option_3_label": "le doudou",
        })
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            put(p2, PLAY[(i, j)], "action", sons=OBJ[j]["son"])
            put(f"{p2}_T0003_P0000", T3_Q[(i, j)], "choice", extra={
                "option_1_label": "le préau",
                "option_2_label": "la fontaine",
                "option_3_label": "le cartable",
            })
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                put(p3, body(i, j, k), "resolution", sons=DEST[k]["son"])
                put(f"{p3}_F0001", FINS[(i, j, k)], "ending", sons="radiateur,vitre")

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in {x["chunk_id"] for x in out_chunks}]
    extra_ids = {x["chunk_id"] for x in out_chunks} - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    # Keep source order
    order = {c["chunk_id"]: i for i, c in enumerate(src["chunks"])}
    out_chunks.sort(key=lambda c: order[c["chunk_id"]])

    # Path word counts
    counts = [path_words(scripts, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    fins_txt = [from_script(FINS[k])[0] for k in FINS]
    if len(set(fins_txt)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fins_txt))}")

    # No mechanical last narrator line
    for c in out_chunks:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"fin mécanique {c['chunk_id']}: {last}")

    out = dict(src)
    out["title"] = "Le fil d'argent et le radiateur de Nina"
    out["fil_rouge"] = (
        "Nina veut courir jusqu'à la flaque pour voir si le fil d'argent de la vitre "
        "la rejoint. Elle pousse la porte, manteau ouvert : un gant tombe, les doigts "
        "pincés ne tiennent plus la poignée, la pelle, la rampe ni les chaînes. "
        "Elle revient au vestiaire, accroche le manteau, retrouve le gant, pose les "
        "paumes sur le radiateur. Alors le bac, le toboggan ou les balançoires "
        "acceptent ses mains ; le ballon, le seau ou le doudou cessent de lui échapper ; "
        "le préau, la fontaine ou le cartable ferment la matinée. Le fil attend sur la vitre."
    )
    out["characters"] = "Nina, papa, maman"
    out["setting"] = "école du village, vitre, vestiaire, radiateur, cour"
    out["chunks"] = out_chunks

    check(SID, out["age_band"], out["chunks"])
    print(f"chemins {min(counts)}–{max(counts)} mots, moy {sum(counts)//len(counts)}")
    (HERE / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {HERE / 'merged.json'} bytes={(HERE / 'merged.json').stat().st_size}")


RELECTURE = """# TREE-AUT-035 — relecture éditoriale

- **Titre noyau conservé :** *Le fil d'argent et le radiateur de Nina*
- **Public :** 5–6 ans (N3)
- **Leçon :** AUT.ROU.001 — enchaîner le matin, vécue (manteau, gant, radiateur, puis la cour)
- **Personnages :** Nina, papa, maman
- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes

## Promesse narrative

Après l'averse, un fil d'argent descend la vitre du vestiaire vers une flaque qui tient un morceau de ciel. Nina veut y courir tout de suite. Elle pousse la porte, manteau ouvert : le gant rouge tombe, les doigts nus ne tiennent plus la poignée. Selon le jeu choisi, la pelle, la rampe ou les chaînes refusent sa main nue. Elle revient au tic du radiateur, accroche, retrouve la paire, réchauffe les paumes. Alors seulement le ballon, le seau ou le doudou cessent de lui échapper, et le préau, la fontaine ou le cartable ferment la matinée. Le fil est toujours sur la vitre.

## Améliorations

- Désir ≠ leçon : Nina veut la flaque et le fil, pas « apprendre à s'habiller ».
- Imprévu concret : gant tombé, poignée, pelle, rampe ou chaîne trop froides.
- Première tentative ratée à l'ouverture, puis une autre dans chaque lieu, puis un raté d'objet (ballon qui file, seau qui bascule, doudou trop près de l'eau ou des chaînes).
- T1/T2/T3 changent l'action, pas seulement le décor.
- Le rangement et l'enchaînement se voient (crochet, paire, paumes sur le métal, boucle clic) ; ils ne se disent pas.
- Papa et maman parlent, questionnent, remercient une fois le gant revenu. Pas de règle récitée.
- Chaque fin paie le fil, le tic, ou la flaque, avec un souvenir unique du chemin.
- Tics « encore / déjà / tout doux / tout calme » écartés. Pas d'escargot COL-015.

## Direction vocale

Chaque chunk a `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration), plus `text_ssml`, `text_xai_tags`, pauses, pitch, volume. `slow` réservé aux choix, à la question et aux fins. Action plus vive.

## Relu

Ouverture, 3 passages T1, 3 questions, 3 confirmations, 9 passages T2, 9 choix T3, 27 résolutions, 27 fins. `chunk_id` / `kind` / graphe inchangés.

## Contrôles

- 86 chunks
- 27 chemins
- 27 fins textuellement distinctes
- `text` et `script` synchronisés
- `text_ssml` et `text_xai_tags` sur les 86
- `check()` N3 ≤ 16, 631 à 682 mots par chemin
- aucune occurrence de « on va apprendre », « une étape après l'autre », « on va ranger »

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
"""


if __name__ == "__main__":
    build()
    (HERE / "RELECTURE.md").write_text(RELECTURE, encoding="utf-8")
    print("wrote RELECTURE.md")
