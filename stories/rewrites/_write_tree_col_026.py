#!/usr/bin/env python3
"""TREE-COL-026 — L'ardoise et la main d'Aniss (N3, COL.ECO.002, TTS)."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-COL-026"
LIM = LIMITS["N3"]
FOLDER = ROOT / SID

# Voix : étalon example2/raw.js (profiles).
PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="ardoise",
        note="arc=installation; intention=émerveiller; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=un secret presse avant le vent; tempo=naturel; sourire=léger; respiration=ample",
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
        emphasis="cerf-volant",
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_tache_peut_devenir_un_dessin; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il_veut_être_entendu_tout_de_suite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=parler_trop_tôt_abîme_le_dessin; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=attendre_donne_une_vraie_oreille; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis=None,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_main_et_l_ardoise_ont_trouvé_leur_place; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp:
        e = esc(emp)
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
    if m.get("pitchTag"):
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    pause = m["pause"]
    suffix = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + suffix).strip()


def L(*rows: str) -> list[str]:
    out = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > LIM:
            raise SystemExit(f"{n}>{LIM}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"fin: {ph}")
        out.append(f"{role}|{ph}")
    return out


def apply_voice(nc: dict, profile: str, emphasis=None, sons=None) -> dict:
    m = dict(PROFILES[profile])
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
    nc["notes"] = m["note"]
    nc["night_policy"] = "play"
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"
    if sons is not None:
        nc["sons"] = sons
    elif not nc.get("sons"):
        nc["sons"] = ""
    return nc


def pack_chunk(src: dict, lines: list[str], profile: str, *, emphasis=None, sons=None, extra=None) -> dict:
    text, script = from_script(lines)
    nc = deepcopy(src)
    nc["text"] = text
    nc["script"] = script
    apply_voice(nc, profile, emphasis=emphasis, sons=sons)
    if extra:
        nc.update(extra)
    return nc


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str, ok: str, near: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
        "engine_ok_text": ok,
        "engine_near_text": near,
    }


PLACES = {
    1: dict(lab="le tapis", ou="sur le tapis", son="laine,craie"),
    2: dict(lab="la table", ou="sur la table", son="pieces,miettes"),
    3: dict(lab="la fenêtre", ou="près de la fenêtre", son="volet,vent"),
}
TOOLS = {
    1: dict(lab="l'éponge", son="eau"),
    2: dict(lab="la craie", son="boite"),
    3: dict(lab="le tabouret", son="bois"),
}
FINISH = {
    1: dict(lab="le clou", son="clou"),
    2: dict(lab="le pain", son="pain"),
    3: dict(lab="le volet", son="volet"),
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
    if "_T0003_P" in cid and not cid.endswith("P0000"):
        return "resolution"
    if "_T0002_P" in cid and "T0003" not in cid and cid[-1] in "123":
        return "obstacle"
    return "action"


def opening() -> list[str]:
    return L(
        "narrateur|Au-dessus de la place, une maison sent le pain chaud.",
        "narrateur|Aniss y vit avec papa et maman.",
        "narrateur|Le soleil de fin de jour dore le plancher.",
        "narrateur|Dehors, un figuier tient un cerf-volant rouge.",
        "narrateur|Le vent tire la queue du cerf-volant.",
        "narrateur|Près de la fenêtre, une ardoise verte pend au clou.",
        "narrateur|C'est l'ardoise de papa, du temps de l'école.",
        "narrateur|Dans une boîte ronde, une craie blanche attend.",
        "narrateur|Papa parle du pain avec maman, près du four.",
        "narrateur|En ce moment, Aniss prend l'ardoise à deux mains.",
        "enfant-m|Je veux garder le cerf-volant, avant le vent !",
        "narrateur|Il lève la craie trop vite.",
        "enfant-m|Papa, maman, venez voir !",
        "narrateur|Leurs voix se mélangent, et personne n'entend Aniss.",
        "narrateur|La craie crisse, puis elle casse.",
        "narrateur|Sur l'ardoise, le cerf-volant n'est qu'une tache.",
        "narrateur|De la poussière blanche colle à sa main.",
        "enfant-m|Il va partir !",
        "maman|Tu disais quelque chose, Aniss ?",
        "narrateur|Aniss ouvre la bouche, puis il se tait.",
        "narrateur|Papa finit sa phrase sur la croûte.",
        "papa|Voilà.",
        "papa|Je t'écoute.",
        "papa|Merci d'avoir attendu ma phrase.",
        "enfant-m|Le cerf-volant est dans le figuier.",
        "enfant-m|Je veux le dessiner.",
        "maman|Montre-nous ça.",
        "narrateur|Aniss garde l'ardoise contre sa poitrine.",
    )


T1_PASS = {
    1: L(
        "narrateur|Aniss s'agenouille sur le tapis gris.",
        "narrateur|L'ardoise pose sur ses genoux, un peu froide.",
        "narrateur|Un fil de laine pique sa cheville.",
        "narrateur|Papa raconte à maman le chant du four.",
        "enfant-m|Le cerf-volant, il est coincé !",
        "narrateur|Sa voix s'enfonce dans la laine épaisse.",
        "narrateur|Personne ne tourne la tête.",
        "narrateur|Aniss serre la craie cassée.",
        "narrateur|Le bout cassé pique sa paume.",
        "narrateur|Il pose sa main sur le genou de papa.",
        "narrateur|Il attend la fin de la phrase.",
        "papa|Oui, Aniss.",
        "papa|Je t'écoute.",
        "enfant-m|Je veux le dessiner, avant le vent.",
        "maman|Alors on regarde l'ardoise ensemble.",
        "narrateur|La tache blanche tremble sur le vert.",
    ),
    2: L(
        "narrateur|Aniss pose l'ardoise au milieu de la table.",
        "narrateur|Des miettes dorées collent au bois chaud.",
        "narrateur|Papa compte des pièces.",
        "narrateur|Elles font clic, clic, clic.",
        "enfant-m|Regardez ma tache, c'est le cerf-volant !",
        "narrateur|Le bruit des pièces recouvre ses mots.",
        "narrateur|Maman répond à papa, pas à Aniss.",
        "narrateur|Aniss referme la bouche.",
        "narrateur|Ses joues deviennent chaudes.",
        "narrateur|Il attend la dernière pièce.",
        "papa|Une, deux, voilà.",
        "papa|Tu voulais dire quoi ?",
        "enfant-m|Le cerf-volant rouge, dans le figuier.",
        "maman|On le voit bien, près du pain ?",
        "narrateur|L'ardoise tient une tache, au milieu des miettes.",
    ),
    3: L(
        "narrateur|Aniss porte l'ardoise jusqu'à la fenêtre.",
        "narrateur|Le volet sent le bois chaud.",
        "narrateur|Dehors, le cerf-volant rouge tire sa queue.",
        "maman|J'avance le volet, le soleil tape.",
        "enfant-m|Non, le cerf-volant !",
        "narrateur|Le volet bouge, et l'ardoise glisse.",
        "narrateur|Aniss la rattrape, mais la tache s'étale.",
        "narrateur|Il se tait, le cœur un peu serré.",
        "narrateur|Maman pose le volet, puis elle se tourne.",
        "maman|Je t'écoute.",
        "maman|Qu'est-ce que tu montres ?",
        "enfant-m|Lui, là-bas, je veux le garder sur l'ardoise.",
        "papa|On t'aide.",
        "papa|Parle, on est prêts.",
        "narrateur|Un carré d'or tremble sur l'ardoise verte.",
    ),
}

T1_Q = {
    1: (
        L(
            "narrateur|Dans sa paume, un bout blanc n'est plus entier.",
            "papa|Qu'est-ce qui s'est cassé, Aniss ?",
        ),
        "craie",
        "craie | la craie | craie cassée | la craie cassée",
        "Écoute l'indice. Qu'est-ce qui s'est cassé ?",
        "Oui, c'est la craie.",
        "Tu es tout près. Qu'est-ce qui s'est cassé dans sa main ?",
        "craie",
    ),
    2: (
        L(
            "narrateur|Aniss voulait copier quelque chose de rouge.",
            "maman|Que veut-il dessiner sur l'ardoise ?",
        ),
        "cerf-volant",
        "cerf-volant | le cerf-volant | cerf volant | un cerf-volant",
        "Écoute l'indice. Que veut-il dessiner ?",
        "Oui, c'est le cerf-volant.",
        "Tu es tout près. Qu'est-ce qui est coincé dans le figuier ?",
        "cerf-volant",
    ),
    3: (
        L(
            "narrateur|Dehors, un arbre tient le jouet rouge.",
            "papa|Où est coincé le cerf-volant ?",
        ),
        "figuier",
        "figuier | le figuier | dans le figuier | arbre",
        "Écoute l'indice. Où est coincé le cerf-volant ?",
        "Oui, dans le figuier.",
        "Tu es tout près. Quel arbre le tient ?",
        "figuier",
    ),
}

T1_C = {
    1: L(
        "papa|Oui.",
        "papa|Je t'ai entendu, là.",
        "narrateur|Aniss souffle.",
        "narrateur|La poussière saute de sa main.",
        "enfant-m|J'ai parlé trop vite.",
        "maman|Là, on t'écoute.",
        "narrateur|Le fil de laine pique moins.",
        "papa|On peut sauver le dessin.",
    ),
    2: L(
        "papa|Oui.",
        "papa|Les pièces se taisent.",
        "narrateur|Aniss pose la craie cassée près des miettes.",
        "enfant-m|Je voulais le cerf-volant, pas une tache.",
        "maman|On recommence, sans se presser.",
        "narrateur|Le bois de la table reste chaud sous l'ardoise.",
        "papa|Ta main tremble un peu.",
        "enfant-m|C'est la poussière.",
    ),
    3: L(
        "maman|Oui.",
        "maman|Le volet ne bougera plus.",
        "narrateur|Aniss essuie la tache avec le pouce.",
        "narrateur|Ça s'étale davantage.",
        "enfant-m|Pff, c'est pire.",
        "papa|On a le temps de le refaire.",
        "narrateur|Dehors, la queue rouge danse.",
        "maman|On te regarde, maintenant.",
    ),
}

T2_CHOICE = {
    1: L(
        "narrateur|Pour sauver le dessin, l'éponge, la craie, ou le tabouret.",
        "papa|Qu'est-ce qui t'aiderait, là, sur le tapis ?",
    ),
    2: L(
        "narrateur|Sur la table, l'éponge, la craie, ou le tabouret peuvent aider.",
        "maman|Que prends-tu, près du pain ?",
    ),
    3: L(
        "narrateur|Près du volet, l'éponge, la craie, ou le tabouret attendent.",
        "papa|Comment on continue, Aniss ?",
    ),
}

T2_PASS = {
    (1, 1): L(
        "narrateur|Aniss cherche l'éponge, près du tapis.",
        "narrateur|Elle attend dans une tasse, un peu molle.",
        "narrateur|Il veut essuyer et parler en même temps.",
        "papa|Le pain a chanté, dans le four.",
        "enfant-m|Moi aussi j'ai quelque chose !",
        "narrateur|De l'eau fuit sur la laine grise.",
        "narrateur|Aniss s'arrête.",
        "narrateur|L'éponge goutte sur sa main.",
        "narrateur|Il attend que papa finisse le four.",
        "papa|Voilà, j'ai fini.",
        "papa|Montre-moi.",
        "narrateur|Aniss essuie la tache, sans presser.",
        "narrateur|Un nuage pâle apparaît.",
        "narrateur|De la place reste pour un cerf-volant.",
        "maman|Ta main est propre, à présent.",
    ),
    (1, 2): L(
        "narrateur|Aniss secoue la boîte ronde, sur le tapis.",
        "narrateur|Le couvercle résiste, puis il saute.",
        "narrateur|Deux craies roulent dans la laine.",
        "enfant-m|La jaune, la jaune !",
        "narrateur|Maman parle du sel, et n'entend pas.",
        "narrateur|Aniss ramasse la craie jaune.",
        "narrateur|Il la tend, sans crier.",
        "maman|Ah, tu as trouvé une craie neuve.",
        "maman|Je t'écoute.",
        "enfant-m|Celle-là ne cassera pas.",
        "papa|Trace un coin, pour voir.",
        "narrateur|Un trait net raye le vert.",
        "narrateur|Sa main ne tremble plus.",
        "narrateur|Le fil de laine laisse un peu de jaune.",
    ),
    (1, 3): L(
        "narrateur|Aniss tire le tabouret vers le tapis.",
        "narrateur|Les pieds râpent la laine.",
        "narrateur|Papa dit un mot sur la croûte.",
        "enfant-m|Je monte, je vois mieux !",
        "narrateur|Le tabouret bascule un peu.",
        "narrateur|L'ardoise tape son genou.",
        "narrateur|Aniss se tait, les lèvres serrées.",
        "papa|Attends, je le tiens.",
        "narrateur|Aniss attend que le bois soit ferme.",
        "enfant-m|Là, la queue est un ruban rouge.",
        "maman|Tu l'as vue, depuis là-haut ?",
        "narrateur|Il hoche la tête, sans couper maman.",
        "narrateur|Du haut, le figuier entre dans la pièce.",
        "papa|On dessine ça, quand tu veux.",
    ),
    (2, 1): L(
        "narrateur|L'éponge dort près du couteau, sur la table.",
        "narrateur|Aniss la presse trop fort.",
        "narrateur|Des miettes collent au vert mouillé.",
        "maman|Je coupe le pain, une minute.",
        "enfant-m|Regarde, ça part !",
        "narrateur|Le couteau tape la planche.",
        "narrateur|Personne n'entend la tache.",
        "narrateur|Aniss pose l'éponge.",
        "narrateur|Il attend le silence du couteau.",
        "maman|C'est bon.",
        "maman|Je te regarde.",
        "narrateur|Il essuie les miettes, une par une.",
        "enfant-m|Le cerf-volant a de la place, maintenant.",
        "papa|Ta main sent l'eau, et un peu de farine.",
    ),
    (2, 2): L(
        "narrateur|La boîte ronde est coincée sous une assiette.",
        "narrateur|Aniss tire, l'assiette chante.",
        "enfant-m|Papa, la craie !",
        "narrateur|Papa parle à maman du croûton.",
        "narrateur|Les mots d'Aniss se perdent.",
        "narrateur|Il pousse l'assiette vers papa, sans crier.",
        "papa|Ah, tu veux la boîte.",
        "papa|Tiens.",
        "narrateur|Une craie courte, presque neuve.",
        "enfant-m|Je trace le nez du cerf-volant.",
        "maman|On te voit, et on t'entend.",
        "narrateur|Le trait traverse une miette, puis il est net.",
        "narrateur|Un peu de jaune reste au bord du pain.",
        "papa|Ta main a retrouvé un outil.",
    ),
    (2, 3): L(
        "narrateur|Aniss glisse le tabouret contre la table.",
        "narrateur|Il monte pour voir le figuier par-dessus le pain.",
        "narrateur|Le bois grince.",
        "enfant-m|Il bouge, le rouge !",
        "maman|J'ai dit que le sel manque.",
        "narrateur|Leurs phrases se cognent.",
        "narrateur|Aniss referme les lèvres.",
        "narrateur|Il pose une main sur la nappe, et il attend.",
        "maman|J'ai fini le sel.",
        "maman|Que vois-tu ?",
        "enfant-m|La queue, derrière les feuilles.",
        "papa|Alors dessine-la, de là-haut.",
        "narrateur|L'ardoise tient sur le rebord de la table.",
        "narrateur|Un fil de soleil coupe le pain en deux.",
    ),
    (3, 1): L(
        "narrateur|L'éponge est sèche, sur le rebord.",
        "narrateur|Aniss souffle dessus pour l'humecter.",
        "narrateur|Une ombre de volet passe sur l'ardoise.",
        "enfant-m|Maman, la tache part !",
        "narrateur|Maman ferme le loquet, et répond à papa.",
        "narrateur|Les mots d'Aniss glissent dehors.",
        "narrateur|Il attend que le loquet fasse clic.",
        "maman|Me voilà.",
        "maman|Essuie, je te vois.",
        "narrateur|L'eau fait un petit lac froid.",
        "narrateur|La tache devient un ciel pâle.",
        "enfant-m|On peut remettre le rouge, après.",
        "papa|Ta main a l'odeur de la pluie, sans pluie.",
        "narrateur|Le figuier tapote la vitre, contre le verre.",
    ),
    (3, 2): L(
        "narrateur|La boîte ronde chauffe au soleil du rebord.",
        "narrateur|Aniss l'ouvre d'un coup.",
        "narrateur|La craie neuve roule vers le volet.",
        "enfant-m|Elle va tomber !",
        "papa|Le four est chaud.",
        "narrateur|Papa n'a pas vu la craie.",
        "narrateur|Aniss la rattrape, puis il se tait.",
        "narrateur|Il attend la fin du four.",
        "papa|Pardon.",
        "papa|Je t'écoute.",
        "enfant-m|Une craie pour le vrai cerf-volant.",
        "maman|Trace-le, pendant qu'il est là.",
        "narrateur|Le premier trait est un ruban, sur le vert.",
        "narrateur|Un grain jaune reste au loquet.",
    ),
    (3, 3): L(
        "narrateur|Aniss traîne le tabouret sous la fenêtre.",
        "narrateur|Il monte, l'ardoise contre le ventre.",
        "narrateur|Le figuier remplit ses yeux.",
        "enfant-m|Je le vois, du haut en bas !",
        "maman|Fais attention au bord.",
        "narrateur|Le tabouret bouge.",
        "narrateur|Papa pose une main sur le bois.",
        "narrateur|Aniss attend d'être stable.",
        "papa|C'est solide.",
        "papa|Parle.",
        "enfant-m|Sa queue passe entre deux feuilles.",
        "maman|Dessine cette queue-là, juste celle-là.",
        "narrateur|De si près, le rouge vibre.",
        "narrateur|Sa main blanche tient le rebord, sans trembler.",
    ),
}


def t3_choice(a: int, b: int) -> list[str]:
    place = PLACES[a]["ou"]
    tool = TOOLS[b]["lab"]
    if a == 1:
        return L(
            f"narrateur|{tool.capitalize()} a aidé {place}.",
            "narrateur|Le clou, le pain, ou le volet peuvent montrer le dessin.",
            "maman|Où montres-tu l'ardoise, maintenant ?",
        )
    if a == 2:
        return L(
            f"narrateur|{place.capitalize()}, {tool} a laissé une trace.",
            "narrateur|Le clou, le pain, ou le volet attendent le cerf-volant.",
            "papa|Où le posons-nous ?",
        )
    return L(
        f"narrateur|Près de la vitre, {tool} a changé l'ardoise.",
        "narrateur|Le clou, le pain, ou le volet peuvent finir le geste.",
        "maman|Quel chemin pour le dessin ?",
    )


# 27 climaxes : autre obstacle, autre image.
T3_PASS = {
    (1, 1, 1): L(
        "narrateur|L'ardoise est fraîche, un peu lourde.",
        "narrateur|Aniss lève les deux bras vers le clou.",
        "enfant-m|Regardez, il vole !",
        "narrateur|Papa parle de la croûte, et ne lève pas les yeux.",
        "narrateur|Une goutte quitte l'ardoise, vers le tapis.",
        "narrateur|Aniss ramène l'ardoise contre lui.",
        "narrateur|Il attend que papa tourne la tête.",
        "papa|Je te vois.",
        "papa|Accroche-la.",
        "narrateur|Le triangle pâle se cale sous le clou.",
        "enfant-m|C'est lui, celui du figuier.",
        "maman|On le reconnaît, même mouillé.",
        "narrateur|Sa main laisse une étoile d'eau sur le bois.",
    ),
    (1, 1, 2): L(
        "narrateur|Aniss porte l'ardoise humide vers le pain.",
        "narrateur|Maman coupe une tranche.",
        "enfant-m|C'est mon cerf-volant !",
        "narrateur|Le couteau parle plus fort que lui.",
        "narrateur|Une miette se colle au ciel pâle.",
        "narrateur|Aniss se tait, les épaules hautes.",
        "narrateur|Le couteau se couche sur la planche.",
        "maman|Je t'écoute.",
        "enfant-m|Celui du figuier, je l'ai gardé.",
        "papa|Il sent l'eau, et un peu de farine.",
        "narrateur|L'éponge s'assoit près du sel.",
        "narrateur|Sa main propre montre le triangle.",
        "maman|On le voit mieux, à côté de la miche.",
    ),
    (1, 1, 3): L(
        "narrateur|Aniss glisse l'ardoise vers le volet, sur le tapis.",
        "narrateur|Le vent pousse le bois.",
        "enfant-m|Pareil, pareil !",
        "narrateur|Le volet claque, et recouvre sa voix.",
        "narrateur|L'eau de l'éponge tremble.",
        "narrateur|Aniss pose une paume sur le bois.",
        "narrateur|Il attend que le vent se taise.",
        "papa|Là, c'est calme.",
        "papa|Montre.",
        "enfant-m|La queue, dehors, et la queue ici.",
        "maman|Deux rubans, l'un rouge, l'un blanc.",
        "narrateur|L'éponge sèche sur le rebord.",
        "narrateur|Sa main garde le volet, sans forcer.",
    ),
    (1, 2, 1): L(
        "narrateur|La craie jaune est courte, entre ses doigts.",
        "narrateur|Aniss veut accrocher et parler ensemble.",
        "enfant-m|Il est net, maintenant !",
        "narrateur|Papa range une miche, et répond à maman.",
        "narrateur|Le clou attend, trop haut pour les mots mêlés.",
        "narrateur|Aniss baisse l'ardoise.",
        "narrateur|Il attend la dernière miche.",
        "papa|Vas-y.",
        "narrateur|Le cerf-volant jaune se cale contre le mur.",
        "enfant-m|Regarde le trait, il ne bave pas.",
        "maman|On dirait la vraie queue.",
        "narrateur|Un grain de craie reste sous le clou.",
        "narrateur|Sa main sent le bois, et le jaune.",
    ),
    (1, 2, 2): L(
        "narrateur|Aniss pose l'ardoise à côté de la croûte.",
        "narrateur|La craie jaune roule vers le pain.",
        "enfant-m|Attention, ma ligne !",
        "narrateur|Maman rit d'une phrase de papa.",
        "narrateur|Personne n'a vu la craie.",
        "narrateur|Aniss la rattrape, puis il attend.",
        "maman|Pardon, on était loin.",
        "maman|Montre ton trait.",
        "enfant-m|Le jaune, c'est le soleil sur le rouge.",
        "papa|On croirait le figuier, en miniature.",
        "narrateur|Farine et craie se touchent, sur sa main.",
        "narrateur|Deux blancs différents, l'un chaud, l'un sec.",
        "maman|Le pain peut veiller le dessin.",
    ),
    (1, 2, 3): L(
        "narrateur|Aniss lève l'ardoise vers le volet, craie au poing.",
        "narrateur|Il veut finir la queue dehors.",
        "enfant-m|Un trait, juste un !",
        "narrateur|Le mot trop vite se perd dans le vent.",
        "narrateur|Le volet bouge, le trait dérape.",
        "narrateur|Aniss recule d'un pas, sur le tapis.",
        "narrateur|Il attend que le bois tienne.",
        "papa|Le volet est calme.",
        "papa|Finis ta queue.",
        "enfant-m|Voilà, elle rejoint la vraie.",
        "maman|Dehors et dedans se saluent.",
        "narrateur|La boîte ronde brille sur le rebord.",
        "narrateur|Sa main jaune laisse une virgule au loquet.",
    ),
    (1, 3, 1): L(
        "narrateur|Du tabouret, le clou est juste à hauteur.",
        "narrateur|Aniss tend l'ardoise, les talons levés.",
        "enfant-m|Je l'accroche !",
        "narrateur|Papa parle, et le tabouret penche.",
        "narrateur|Aniss ravalé son cri.",
        "narrateur|Il attend que papa tienne le bois.",
        "papa|Je te tiens.",
        "papa|Vas-y, doucement.",
        "narrateur|L'ardoise trouve le clou, sans choc.",
        "enfant-m|Il est plus grand que le tabouret.",
        "maman|On le voit depuis le tapis.",
        "narrateur|Le tabouret vide regarde trop haut.",
        "narrateur|Sa main quitte le rebord, un peu fière.",
    ),
    (1, 3, 2): L(
        "narrateur|Aniss redescend du tabouret, l'ardoise au ventre.",
        "narrateur|Il veut la poser près du pain, sans attendre.",
        "enfant-m|Maman, vois !",
        "narrateur|Maman souffle sur une tranche trop chaude.",
        "narrateur|Elle n'entend que le souffle.",
        "narrateur|Aniss pose un pied au sol, et il attend.",
        "maman|Ça va, je peux regarder.",
        "enfant-m|Je l'ai vu de haut, alors je l'ai copié.",
        "papa|La queue est longue, comme dehors.",
        "narrateur|Le pain et l'ardoise partagent le même or.",
        "narrateur|Le tabouret reste au bord du tapis.",
        "maman|Ta main sent le bois du tabouret.",
        "narrateur|Une miette roule contre le vert.",
    ),
    (1, 3, 3): L(
        "narrateur|Aniss, sur le tabouret, attrape le volet.",
        "narrateur|Il veut coller l'ardoise au bois.",
        "enfant-m|Regarde, c'est le même !",
        "narrateur|Le vent répond à sa place.",
        "narrateur|Le volet frappe, presque.",
        "narrateur|Aniss se tait, une main sur le loquet.",
        "papa|Je retiens le bois.",
        "papa|Parle, maintenant.",
        "enfant-m|Dehors il danse, ici il tient.",
        "maman|Deux danses, une seule histoire de queue.",
        "narrateur|Sa main haute garde le volet.",
        "narrateur|Le tabouret ne bouge plus.",
        "narrateur|Un fil de laine s'accroche à son talon.",
    ),
    (2, 1, 1): L(
        "narrateur|Des miettes voyagent avec l'ardoise mouillée.",
        "narrateur|Aniss marche vers le clou, trop vite.",
        "enfant-m|Je l'accroche avant qu'il sèche !",
        "narrateur|Papa répond à maman, près du four.",
        "narrateur|Une goutte et une miette tombent ensemble.",
        "narrateur|Aniss s'arrête, l'ardoise à bout de bras.",
        "narrateur|Il attend leurs visages.",
        "maman|On te suit.",
        "papa|Le clou est libre.",
        "narrateur|Le triangle pâle se pend, un peu lourd.",
        "enfant-m|Les miettes font des nuages.",
        "maman|On dirait le vent, autour de lui.",
        "narrateur|Sa main laisse de l'eau sur le mur.",
    ),
    (2, 1, 2): L(
        "narrateur|Aniss ramène l'ardoise humide vers la miche.",
        "narrateur|Le couteau attend, la pointe vers le pain.",
        "enfant-m|Il sèche près de toi !",
        "narrateur|Maman parle du croûton, les yeux bas.",
        "narrateur|L'éponge manque de tomber dans la farine.",
        "narrateur|Aniss la pose, puis il attend.",
        "maman|Me voilà.",
        "maman|Ton cerf-volant a un ciel propre.",
        "enfant-m|J'ai ôté la tache, sans crier.",
        "papa|Il sèche au chaud du pain.",
        "narrateur|Le couteau repose.",
        "narrateur|Le cerf-volant pâle s'installe contre la croûte.",
        "narrateur|Sa main sent l'eau, plus la poussière.",
    ),
    (2, 1, 3): L(
        "narrateur|Aniss pousse l'ardoise mouillée vers le volet.",
        "narrateur|Une goutte court sur la table, vers les pièces.",
        "enfant-m|Vite, le vrai est là !",
        "narrateur|Les pièces tintent, papa répond.",
        "narrateur|La goutte s'arrête contre une pièce.",
        "narrateur|Aniss retient sa phrase.",
        "papa|Les pièces sont sages.",
        "papa|Ouvre le volet, on compare.",
        "enfant-m|Pâle ici, rouge là-bas.",
        "maman|Deux versions, une même queue.",
        "narrateur|L'éponge laisse un rond sur le bois.",
        "narrateur|Sa main écarte le volet, sans claquer.",
        "narrateur|Le figuier entre dans la cuisine.",
    ),
    (2, 2, 1): L(
        "narrateur|La craie courte tremble au-dessus du clou.",
        "narrateur|Aniss veut un dernier point, trop tôt.",
        "enfant-m|Un œil !",
        "narrateur|Papa dit le prix du pain, à maman.",
        "narrateur|Le point devient une virgule, trop longue.",
        "narrateur|Aniss baisse la craie.",
        "narrateur|Il attend la fin du prix.",
        "papa|Trace, je te regarde.",
        "narrateur|Un petit œil rond s'installe.",
        "enfant-m|Il nous voit, depuis le mur.",
        "maman|La boîte ronde peut garder le clou.",
        "narrateur|Aniss pose la boîte au pied du mur.",
        "narrateur|Sa main jaune salue le cerf-volant.",
    ),
    (2, 2, 2): L(
        "narrateur|Aniss glisse l'ardoise entre le pain et l'assiette.",
        "narrateur|La craie jaune veut un dernier ruban.",
        "enfant-m|Là, la lumière !",
        "narrateur|Maman souffle une miette, et parle.",
        "narrateur|Le ruban croise une graine de farine.",
        "narrateur|Aniss attend qu'elle ait soufflé.",
        "maman|C'est à toi.",
        "enfant-m|Le jaune, c'est le soir sur ses ailes.",
        "papa|On dirait le vrai, collé à la croûte.",
        "narrateur|Farine et craie se mêlent au bout de ses doigts.",
        "narrateur|Deux poudres, un seul goût de pain.",
        "maman|On mange, et lui veille.",
        "narrateur|L'ardoise tient chaud, contre la miche.",
    ),
    (2, 2, 3): L(
        "narrateur|Aniss porte craie et ardoise vers le volet.",
        "narrateur|Il veut la dernière ligne pendant que papa parle.",
        "enfant-m|La nervure de la feuille !",
        "narrateur|Le volet cède d'un souffle.",
        "narrateur|La ligne part de travers.",
        "narrateur|Aniss pose la craie, les lèvres closes.",
        "papa|Je tiens le volet.",
        "papa|Recommence la nervure.",
        "enfant-m|Voilà, elle rejoint le figuier.",
        "maman|Le volet dort, la ligne est nette.",
        "narrateur|Un grain jaune reste au loquet.",
        "narrateur|Sa main ne cache plus le dessin.",
        "narrateur|Dehors, le rouge approuve, sans un mot.",
    ),
    (2, 3, 1): L(
        "narrateur|Aniss pousse le tabouret sous le clou.",
        "narrateur|La table recule d'un doigt.",
        "enfant-m|Je le mets en haut !",
        "narrateur|Une cuillère tombe, et papa s'exclame.",
        "narrateur|Les mots d'Aniss se cassent.",
        "narrateur|Il attend que la cuillère se taise.",
        "papa|C'est bon, j'ai ramassé.",
        "papa|Monte.",
        "narrateur|L'ardoise gagne le clou, au-dessus du pain.",
        "enfant-m|Il surveille la table.",
        "maman|Le tabouret rentre, l'ardoise veille.",
        "narrateur|Sa main quitte le bois, un peu blanche.",
        "narrateur|Une miette orpheline reste sur une barre.",
    ),
    (2, 3, 2): L(
        "narrateur|Du tabouret, Aniss tend l'ardoise vers le pain.",
        "narrateur|C'est trop loin, il parle trop fort.",
        "enfant-m|Prends-le, maman !",
        "narrateur|Maman a les mains farinées, et elle discute.",
        "narrateur|L'ardoise penche.",
        "narrateur|Aniss la serre, et il attend.",
        "maman|J'essuie mes mains.",
        "maman|Je la prends.",
        "enfant-m|Le cerf-volant de craie fait face à la miche.",
        "papa|Ils se ressemblent, ronds et sages.",
        "narrateur|Aniss redescend.",
        "narrateur|Le tabouret retrouve l'ombre de la table.",
        "narrateur|Sa main sent le pain, de loin.",
    ),
    (2, 3, 3): L(
        "narrateur|Aniss hisse le tabouret contre le volet.",
        "narrateur|Du haut, le figuier remplit la vitre.",
        "enfant-m|Il est énorme !",
        "narrateur|Papa veut fermer un peu, à cause du soleil.",
        "narrateur|Leurs envies se croisent.",
        "narrateur|Aniss pose l'ardoise, et il attend.",
        "papa|On laisse ouvert ?",
        "enfant-m|Oui, pour copier la grande queue.",
        "maman|Alors on compare, sans bouger le bois.",
        "narrateur|Le cerf-volant de craie salue le vrai.",
        "narrateur|Du tabouret, la place entière tient dans un cadre.",
        "narrateur|Sa main ombre un coin de l'ardoise.",
        "papa|On voit tout, grâce à toi.",
    ),
    (3, 1, 1): L(
        "narrateur|L'ardoise fraîche veut le clou, près de la vitre.",
        "narrateur|Aniss marche trop vite, l'éponge sous le bras.",
        "enfant-m|Je le mets ici, pile !",
        "narrateur|Maman cherche ses mots sur le loquet.",
        "narrateur|Une goutte file vers le rebord.",
        "narrateur|Aniss s'arrête, talons au sol.",
        "maman|Le clou est à toi.",
        "narrateur|Le triangle pâle se pend, un peu froid.",
        "enfant-m|Les feuilles tapent, contre le verre.",
        "papa|Elles applaudissent, peut-être.",
        "narrateur|L'éponge reste sur le rebord, en sentinelle.",
        "narrateur|Sa main laisse un croissant d'eau sous le clou.",
        "maman|On le verra, chaque fois qu'on ouvre.",
    ),
    (3, 1, 2): L(
        "narrateur|Aniss apporte l'ardoise mouillée vers le pain, à la fenêtre.",
        "narrateur|Le rebord est étroit.",
        "enfant-m|On mange avec lui !",
        "narrateur|Papa pose deux tasses, et compte à voix haute.",
        "narrateur|L'ardoise glisse d'un souffle.",
        "narrateur|Aniss la plaque, sans parler.",
        "narrateur|Il attend la deuxième tasse.",
        "papa|Voilà, c'est posé.",
        "papa|Ton dessin peut s'asseoir.",
        "enfant-m|Il sèche au soleil du pain.",
        "maman|On croque, et lui sèche.",
        "narrateur|Une goutte meurt sur la croûte, minuscule.",
        "narrateur|Sa main sent le tiède du rebord.",
    ),
    (3, 1, 3): L(
        "narrateur|Aniss veut coller l'ardoise mouillée au volet.",
        "narrateur|L'éponge sert de coussin.",
        "enfant-m|Comme ça, ils se touchent !",
        "narrateur|Le vent n'est pas d'accord.",
        "narrateur|Le volet pousse, l'eau fuit.",
        "narrateur|Aniss attend une pause du vent.",
        "papa|Maintenant.",
        "papa|Pose.",
        "enfant-m|L'eau et le bois, c'est son ciel.",
        "maman|L'éponge et le volet sentent la même chose.",
        "narrateur|Le cerf-volant pâle fixe le rouge.",
        "narrateur|Sa main essuie une goutte sur le loquet.",
        "narrateur|Deux odeurs, eau et bois, dans une seule paume.",
    ),
    (3, 2, 1): L(
        "narrateur|La craie jaune veut un dernier point, sous le clou.",
        "narrateur|Aniss parle pendant que maman ouvre.",
        "enfant-m|Un soleil, juste là !",
        "narrateur|Le volet prend sa phrase.",
        "narrateur|Le soleil devient une virgule.",
        "narrateur|Aniss attend que le bois s'arrête.",
        "maman|Recommence le soleil.",
        "narrateur|Un rond jaune s'installe, propre.",
        "enfant-m|Il chauffe le cerf-volant du mur.",
        "papa|Une virgule jaune reste sous le clou, en trop.",
        "narrateur|Aniss la chasse d'un doigt.",
        "narrateur|Sa main porte un petit astre.",
        "maman|Le clou a son étoile.",
    ),
    (3, 2, 2): L(
        "narrateur|Aniss cale l'ardoise contre le pain, au rebord.",
        "narrateur|La craie veut signer la croûte, presque.",
        "enfant-m|Un petit trait, pour eux !",
        "narrateur|Papa mâche, et dit un mot flou.",
        "narrateur|Aniss retient la craie.",
        "narrateur|Il attend que papa avale.",
        "papa|Je t'écoute, là.",
        "enfant-m|Le vrai, derrière le pain, salue la vitre.",
        "maman|On a le rouge et le jaune, au même dîner.",
        "narrateur|Derrière le pain, le vrai cerf-volant rouge salue.",
        "narrateur|Sa main ne touche plus la croûte.",
        "papa|Il mange des yeux, nous des dents.",
        "narrateur|La boîte ronde sert d'anneau au rebord.",
    ),
    (3, 2, 3): L(
        "narrateur|Aniss lève craie et ardoise contre le volet ouvert.",
        "narrateur|Deux cerfs-volants peuvent se regarder.",
        "enfant-m|Ils se parlent !",
        "narrateur|Maman dit le mot four, en même temps.",
        "narrateur|Aniss perd sa phrase.",
        "narrateur|Il pose la craie, et il attend.",
        "maman|C'est dit, le four.",
        "maman|À toi.",
        "enfant-m|L'un est rouge, l'un est blanc.",
        "papa|Ils se saluent, sans se bousculer.",
        "narrateur|Un grain de craie orne le loquet.",
        "narrateur|Sa main s'ouvre, enfin vide.",
        "narrateur|Le vent n'efface plus rien.",
    ),
    (3, 3, 1): L(
        "narrateur|Aniss, sur le tabouret, tend l'ardoise vers le clou.",
        "narrateur|Il ne veut pas redescendre.",
        "enfant-m|Je l'accroche d'ici !",
        "narrateur|Papa a peur du vide, et il parle trop.",
        "narrateur|Les mots d'Aniss se serrent.",
        "narrateur|Il attend que papa pose juste la main.",
        "papa|Je te tiens.",
        "papa|Accroche.",
        "narrateur|Le clou prend l'ardoise, très haut.",
        "enfant-m|La place est à moi, d'ici.",
        "maman|On la voit, depuis le carrelage.",
        "narrateur|Il redescend après, pas avant.",
        "narrateur|Sa main quitte le clou, un peu lente.",
    ),
    (3, 3, 2): L(
        "narrateur|Du tabouret, Aniss tend l'ardoise vers le pain du rebord.",
        "narrateur|C'est un pont trop long.",
        "enfant-m|Maman, prends, vite !",
        "narrateur|Maman a une tasse chaude, et elle souffle.",
        "narrateur|Aniss attend la tasse posée.",
        "maman|Mes mains sont libres.",
        "maman|Je la pose près du pain.",
        "enfant-m|Le pain sur le rebord, l'ardoise sur mes genoux.",
        "papa|Deux trésors, une seule fenêtre.",
        "narrateur|Aniss reste un moment, trop haut, trop content.",
        "narrateur|Le tabouret craque, puis il se tait.",
        "maman|Tu peux descendre, on le garde.",
        "narrateur|Sa main laisse le vert, sans le salir.",
    ),
    (3, 3, 3): L(
        "narrateur|Aniss, tabouret et volet, veut tenir trois choses.",
        "narrateur|L'ardoise, le loquet, et sa phrase.",
        "enfant-m|Regardez les trois !",
        "narrateur|Le vent, papa, et lui parlent ensemble.",
        "narrateur|Rien n'est clair.",
        "narrateur|Aniss choisit le silence, une seconde.",
        "papa|On se tait.",
        "papa|Montre.",
        "enfant-m|Le tabouret, le volet, et ma main.",
        "maman|Trois choses sages, et un cerf-volant.",
        "narrateur|Le bois, le bois, et la peau se tiennent.",
        "narrateur|Dehors, le rouge reste, pour un peu.",
        "narrateur|Sa main, au loquet, ne serre plus trop.",
    ),
}


def ending(a: int, b: int, c: int) -> list[str]:
    last = {
        (1, 1, 1): "Une goutte tombe du clou, sur la laine grise.",
        (1, 1, 2): "L'éponge humide garde une miette de pain.",
        (1, 1, 3): "Sur le tapis, l'éponge sèche près du volet ouvert.",
        (1, 2, 1): "Un grain de craie jaune dort sous le clou.",
        (1, 2, 2): "La croûte et la craie sentent le chaud, toutes les deux.",
        (1, 2, 3): "La boîte ronde brille sur le rebord du volet.",
        (1, 3, 1): "Le tabouret vide regarde l'ardoise, trop haute pour lui.",
        (1, 3, 2): "Aniss redescend ; le pain et l'ardoise partagent le soleil.",
        (1, 3, 3): "Sa main tient le volet, sans bouger, là-haut.",
        (2, 1, 1): "Des miettes collent au bord mouillé de l'ardoise.",
        (2, 1, 2): "Le couteau repose ; le cerf-volant pâle sèche au pain.",
        (2, 1, 3): "Une goutte court vers les pièces, puis s'arrête.",
        (2, 2, 1): "La boîte ronde garde le pied du clou.",
        (2, 2, 2): "Farine et craie se mêlent au bout de ses doigts.",
        (2, 2, 3): "Le volet dort ; la dernière ligne est nette.",
        (2, 3, 1): "Le tabouret rentre sous la table ; l'ardoise veille.",
        (2, 3, 2): "Le cerf-volant de craie fait face à la miche.",
        (2, 3, 3): "Du tabouret, le figuier remplit toute la vitre.",
        (3, 1, 1): "Les feuilles du figuier tapent la vitre, contre l'ardoise.",
        (3, 1, 2): "Ils croquent près de la fenêtre ; le dessin sèche.",
        (3, 1, 3): "L'éponge et le volet sentent l'eau et le bois.",
        (3, 2, 1): "Une virgule jaune de craie reste sous le clou.",
        (3, 2, 2): "Derrière le pain, le vrai cerf-volant rouge salue la vitre.",
        (3, 2, 3): "Deux cerfs-volants se regardent : l'un rouge, l'un blanc.",
        (3, 3, 1): "Aniss accroche l'ardoise sans redescendre du tabouret.",
        (3, 3, 2): "Le pain reste sur le rebord, l'ardoise sur ses genoux.",
        (3, 3, 3): "Le tabouret, le volet, et sa main restent tranquilles.",
    }[(a, b, c)]
    spoken = {
        1: "sur le tapis",
        2: "sur la table",
        3: "près de la fenêtre",
    }[a]
    tool = {1: "l'éponge", 2: "la craie neuve", 3: "le tabouret"}[b]
    fin = {1: "le clou", 2: "le pain", 3: "le volet"}[c]
    hand = {
        (1, 1): "Sa paume est propre, un peu froide.",
        (1, 2): "Un croissant jaune reste au creux de sa main.",
        (1, 3): "Sa main sent le bois du tabouret.",
        (2, 1): "Ses doigts sentent l'eau et la farine.",
        (2, 2): "Deux poudres blanches ornent ses ongles.",
        (2, 3): "Sa main a gardé la chaleur de la nappe.",
        (3, 1): "Sa main sent le rebord, et un peu d'eau.",
        (3, 2): "Un grain de craie lui tient lieu d'anneau.",
        (3, 3): "Sa main quitte le loquet, sans se presser.",
    }[(a, b)]
    body = L(
        f"narrateur|Plus tard, le pain est sur la table, et le soleil baisse.",
        "papa|À toi, Aniss.",
        "papa|Nous t'écoutons jusqu'au bout.",
        f"enfant-m|J'ai dessiné {spoken}, avec {tool}, puis {fin}.",
        "maman|On a entendu toute ta phrase.",
        f"narrateur|{hand}",
        f"narrateur|{last}",
    )
    return body


def main() -> None:
    src = json.loads((FOLDER / "source.json").read_text(encoding="utf-8"))
    scripts: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {}
    emph: dict[str, str | None] = {}

    scripts["CHK_T0000_P0000"] = opening()
    sons["CHK_T0000_P0000"] = "pain,craie"
    emph["CHK_T0000_P0000"] = "ardoise"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|L'ardoise peut voyager vers le tapis, la table, ou la fenêtre.",
        "maman|Où poses-tu l'ardoise, Aniss ?",
    )
    extras["CHK_T0001_P0000"] = t3("le tapis", "la table", "la fenêtre")
    sons["CHK_T0001_P0000"] = ""

    for a in (1, 2, 3):
        p = f"CHK_T0001_P000{a}"
        scripts[p] = T1_PASS[a]
        sons[p] = PLACES[a]["son"]
        q_lines, ans, acc, retry, ok, near, emp = T1_Q[a]
        scripts[f"{p}_Q0001"] = q_lines
        extras[f"{p}_Q0001"] = qf(ans, acc, retry, ok, near)
        emph[f"{p}_Q0001"] = emp
        sons[f"{p}_Q0001"] = ""
        scripts[f"{p}_C0001"] = T1_C[a]
        sons[f"{p}_C0001"] = PLACES[a]["son"]
        scripts[f"{p}_T0002_P0000"] = T2_CHOICE[a]
        extras[f"{p}_T0002_P0000"] = t3("l'éponge", "la craie", "le tabouret")
        sons[f"{p}_T0002_P0000"] = ""
        for b in (1, 2, 3):
            pb = f"{p}_T0002_P000{b}"
            scripts[pb] = T2_PASS[(a, b)]
            sons[pb] = TOOLS[b]["son"]
            scripts[f"{pb}_T0003_P0000"] = t3_choice(a, b)
            extras[f"{pb}_T0003_P0000"] = t3("le clou", "le pain", "le volet")
            sons[f"{pb}_T0003_P0000"] = ""
            for c in (1, 2, 3):
                pc = f"{pb}_T0003_P000{c}"
                scripts[pc] = T3_PASS[(a, b, c)]
                sons[pc] = FINISH[c]["son"]
                fid = f"{pc}_F0001"
                scripts[fid] = ending(a, b, c)
                sons[fid] = "couverts," + FINISH[c]["son"]

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        prof = profile_for(cid, kind)
        by[cid] = pack_chunk(
            c,
            scripts[cid],
            prof,
            emphasis=emph.get(cid, PROFILES[prof]["emphasis"]),
            sons=sons.get(cid, c.get("sons") or ""),
            extra=extras.get(cid),
        )

    out = dict(src)
    out["fil_rouge"] = (
        "Un cerf-volant rouge s'accroche au figuier. Aniss veut le copier "
        "sur l'ardoise verte avant le vent. Sa première phrase se perd, "
        "la craie casse, sa main se couvre de poussière. Sur le tapis, "
        "la table ou la fenêtre, il apprend à attendre la fin des voix. "
        "L'éponge, la craie ou le tabouret changent le dessin. Le clou, "
        "le pain ou le volet lui donnent enfin des oreilles. Le soir, "
        "l'ardoise garde le cerf-volant, et sa main n'est plus trop pressée."
    )
    out["title"] = "L'ardoise et la main d'Aniss"
    out["characters"] = "Aniss, papa, maman"
    out["setting"] = "maison au-dessus de la place, fin de jour, ardoise verte, figuier"
    out["age_band"] = "N3"
    out["lesson_id"] = "COL.ECO.002"
    out["kind"] = "ramifiee"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]

    check(SID, out["age_band"], out["chunks"])

    ends = [c["text"] for c in out["chunks"] if c["kind"] == "passage_fin"]
    if len(ends) != 27 or len(set(ends)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(ends))}/{len(ends)}")
    lasts = []
    for c in out["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        nlines = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(nlines[-1])
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images: {len(set(lasts))}/27")

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for tic in ("tout doux", "tout calme", "on lève la main", "puis on parle", "on attend."):
        if tic in blob:
            raise SystemExit(f"tic: {tic}")
    for name in ("léa", "tom ", "sami", "marceau"):
        if name in blob:
            raise SystemExit(f"nom: {name}")

    paths = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
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
                n = sum(words(by[i]["text"]) for i in ids)
                paths.append(n)
    print(f"chemins {min(paths)}–{max(paths)} mots, moy {sum(paths)//len(paths)}")

    (FOLDER / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    relect = f"""# TREE-COL-026 — L'ardoise et la main d'Aniss

- **Public :** N3 (5–6 ans), récit ramifié familial
- **Leçon :** COL.ECO.002 — écouter, puis parler, vécue (jamais récitée)
- **Personnages :** Aniss, papa, maman
- **Structure :** 86 nœuds, graphe conservé, 27 chemins, 27 fins distinctes
- **Voix :** profils example2 (`opening/choice/clue/confirm/action/obstacle/resolution/ending`)

## Promesse narrative

Fin de jour, maison au-dessus de la place. Un cerf-volant rouge s'accroche au figuier. Aniss veut le copier sur l'ardoise verte de papa **avant le vent**. Il crie trop tôt : personne n'entend, la craie casse, sa main se couvre de poussière. Le tapis, la table ou la fenêtre changent l'obstacle. L'éponge, la craie ou le tabouret changent le dessin. Le clou, le pain ou le volet changent la façon d'être enfin entendu. Le soir, l'image du début (ardoise, main, cerf-volant) est payée.

## Relu

- Monde d'abord, désir immédiat, première idée qui échoue, choix qui change l'action.
- Autre récit que TREE-COL-015 (trace d'argent), TREE-COL-016 (craie-oiseau sous la pluie), TREE-COL-025 (gouttière de Nina).
- T1/T2/T3 ne sont pas de simples lieux : chacun a un imprévu, un climax, une fin unique.
- Labels T3 : plus Léa/Tom/Sami (hors troupe) → le clou, le pain, le volet.
- Questions T1 : craie / cerf-volant / figuier (pas « attendre »).
- Un merci vécu (papa, après la phrase achevée). Une question d'adulte. `en ce moment`.
- Pas de « on lève la main / on attend / puis on parle ». Pas de tics tout doux / tout calme.
- `check()` N3 ≤ 16 mots/phrase. `text` = `script`. TTS renseigné sur 86 chunks.
- Chemins : {min(paths)}–{max(paths)} mots (moy {sum(paths)//len(paths)}).

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'`apply`.
"""
    (FOLDER / "RELECTURE.md").write_text(relect, encoding="utf-8")
    print("wrote merged.json + RELECTURE.md")


if __name__ == "__main__":
    main()
