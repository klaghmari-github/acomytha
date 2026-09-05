#!/usr/bin/env python3
"""TREE-DIF-029 — Le papillon jaune de Victorino (N3, DIF.ENE.001, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-029"
LIM = LIMITS["N3"]
TITLE = "Le papillon jaune de Victorino"
FIL = (
    "À la haie des ailes, Victorino veut que le papillon jaune se pose "
    "sur la fleur de papier, avec Aniss. Un grain de lavande tient à la pince. "
    "Aniss veut courir maintenant ; Victorino veut attendre. "
    "T1 = filet vert / chapeau bleu / fleur de papier ; les trois partent. "
    "T2 = pré / lavandes / muret. La première course rate. Ils refusent de foncer. "
    "Le grain du début revient. Le jaune se pose, il a failli partir."
)
CHARS = "Victorino, Aniss, papa, maman"
SETTING = "village au bord des champs : pré, lavandes, muret — la haie des ailes"
TIC_PHRASES = (
    "tout doux",
    "tout calme",
    "tout lent",
    "miel",
    "merle",
    "aujourd'hui",
    "j'ai compris",
    "mission accomplie",
    "on va apprendre",
    "bon travail",
    "il faut attendre",
    "papa sourit",
    "maman sourit",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)
OLD_CLUES = (
    "étoile brune",
    "fil pâle",
    "croissant d'eau",
    "croissant pâle",
    "virgule farine",
    "bouton nacre",
    "nœud raphia",
    "pois ivoire",
    "grain savon",
    "grain de vanille",
    "pastille colle",
    "virgule buée",
    "capuchon penche",
    "grain doré",
    "brin safran",
    "anneau liège",
    "clou tête ronde",
    "grain d'ambre",
    "goutte de cire",
    "anneau de zinc",
    "larme de bronze",
    "point de cire",
    "bracelet d'écorce",
    "boucle d'étain",
    "anneau de pollen",
    "dent de laitue",
    "éclat de zinc",
    "éclat de thym",
    "lune d'étain",
    "grain de grenat",
    "grain d'indigo",
    "grain de brique",
    "éclat vert",
    "écaille d'étain",
    "vis verte",
    "cristal de sucre",
    "écaille de lichen",
    "grain de cire",
    "dent de fermeture",
    "écaille de nacre",
    "grain de paprika",
    "écaille de boue",
    "point de rouille",
    "grain de mica",
    "grain de cannelle",
    "grain d'ocre",
    "grain de feutre",
    "grain de sésame",
    "écaille de savon",
    "grain de suie",
    "grain de limon",
    "grain de quartz",
    "grain de sel",
    "grain de lessive",
    "grain de cerise",
    "rond d'huile",
    "écaille d'orange",
    "point d'écume",
    "grain de sève",
    "point de beurre",
    "grain de craie",
    "grain de pomme",
    "grain de bitume",
    "grain de laine",
    "grain de grelot",
    "grain de parquet",
    "trait de craie",
    "grain de foin",
)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain de lavande",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=deux_envies_le_grain_tient; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_le_geste; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "grain de lavande",
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=aniss_veut_courir_victorino_retient; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_inquiétude; intensite=2; destinataire=enfant; sous_texte=la_première_course_rate_le_silence_répond; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "grain de lavande",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=ils_refusent_de_foncer_le_grain_revient; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain de lavande",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_paie_le_début; tempo=posé; sourire=léger; respiration=ample",
    },
}


def L(*rows: str) -> list[str]:
    out: list[str] = []
    prev = ""
    run = 1
    for raw in rows:
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
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"fin: {ph}")
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"tic {tic!r}: {ph}")
        found = TIC_WORDS.search(low)
        if found:
            raise SystemExit(f"tic {found.group(0)!r}: {ph}")
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


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict, emphasis: str | None) -> str:
    body = esc(text)
    if emphasis:
        e = esc(emphasis)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict, emphasis: str | None) -> str:
    body = text
    if emphasis:
        body = body.replace(emphasis, f"<emphasis>{emphasis}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m["pitchTag"]:
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    tail = "[long-pause]" if m["pause"] >= 800 else ("[pause]" if m["pause"] >= 400 else "")
    return f"{body} {tail}".strip()


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    m = dict(PROFILES[profile])
    emphasis = extra.get("emphasis", m["emphasis"])
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else ""
    nc["text_ssml"] = ssml(text, m, emphasis)
    nc["text_xai_tags"] = xai(text, m, emphasis)
    nc["length_scale_piper"] = m["piper"]
    nc["rate_label"] = m["rate"]
    nc["rate_wpm"] = m["wpm"]
    nc["speed_xai"] = m["speed"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitchSsml"]
    nc["pitch_xai_tag"] = m["pitchTag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = emphasis or ""
    nc["pause_before_ms"] = extra.get("pause_before", 0)
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
    nc["notes"] = extra.get("notes", m["note"])
    nc["night_policy"] = "play"
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        nc[k] = v
    return nc


def path_words(by: dict, a: int, b: int, c: int) -> int:
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
    return sum(words(by[i]["text"]) for i in ids)


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


T1 = {
    1: {
        "lab": "le filet vert",
        "cap": "Le filet vert",
        "ans": "sac",
        "acc": "sac | le sac | dans le sac | son sac",
        "retry": "Le filet est dans le sac.",
        "emph": "filet vert",
        "sons": "sac,mailles",
        "coda": "narrateur|Le filet vert rentre dans le sac.",
    },
    2: {
        "lab": "le chapeau bleu",
        "cap": "Le chapeau bleu",
        "ans": "tête",
        "acc": "tête | tete | la tête | sur la tête | sa tête",
        "retry": "Le chapeau est sur la tête.",
        "emph": "chapeau bleu",
        "sons": "tissu,linge",
        "coda": "narrateur|Le chapeau bleu reste sur les cheveux.",
    },
    3: {
        "lab": "la fleur de papier",
        "cap": "La fleur de papier",
        "ans": "poche",
        "acc": "poche | la poche | dans la poche | sa poche",
        "retry": "La fleur est dans la poche.",
        "emph": "fleur de papier",
        "sons": "papier,poche",
        "coda": "narrateur|La fleur de papier rentre dans la poche.",
    },
}

T3_LABS = {
    1: ("marcher comme lui", "s'asseoir dans l'herbe", "le silence de maman"),
    2: ("souffler tout doux", "attendre le parfum", "la fleur de papa"),
    3: ("le rythme sur la pierre", "attendre en bas", "la main de maman"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Victorino prend d'abord le filet vert.",
            "enfant-m|Les mailles laissent passer le soleil.",
            "maman|Glisse-le dans le sac, bien droit.",
            "narrateur|Un peu d'ombre reste au creux de la main.",
            "papa|Le chapeau bleu va sur ta tête, juste après.",
            "narrateur|Maman glisse la fleur de papier dans la poche.",
            "narrateur|Les trois affaires restent avec eux.",
            "copain|On court, Victorino !",
            "enfant-m|On emporte tout, sans courir.",
            "papa|Le filet d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Victorino pose d'abord le chapeau bleu.",
            "enfant-m|Il sent le savon du linge.",
            "papa|Calé sur tes cheveux, un peu.",
            "narrateur|L'ombre descend jusqu'aux sourcils.",
            "maman|Le filet vert, ensuite, dans le sac.",
            "narrateur|Elle glisse la fleur de papier dans la poche.",
            "narrateur|Les trois affaires restent avec eux.",
            "copain|Je veux le jaune, maintenant !",
            "enfant-m|Le chapeau d'abord, on marche.",
            "maman|Le chapeau est prêt.",
        )
    return L(
        "narrateur|Victorino glisse la fleur de papier dans la poche.",
        "enfant-m|C'est pour attirer le jaune.",
        "maman|Serre-la, comme un secret.",
        "narrateur|Le papier sent un peu la colle.",
        "papa|Le filet et le chapeau, avec vous.",
        "narrateur|Il les pose près du sac.",
        "narrateur|Les trois affaires restent avec eux.",
        "copain|Vite, le pré !",
        "enfant-m|La fleur d'abord, je te la montre.",
        "papa|La fleur est cachée, dans la poche.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Victorino a mis le filet vert dans le sac.",
            "maman|C'est où, maintenant ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Victorino a mis le chapeau bleu sur la tête.",
            "papa|C'est où, maintenant ?",
        )
    return L(
        "narrateur|Victorino a mis la fleur de papier dans la poche.",
        "maman|C'est où, maintenant ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Dans le sac.",
            "maman|Oui.",
            "copain|On dirait une fenêtre verte !",
            "enfant-m|Le jaune aime l'ombre, un peu.",
            "narrateur|Aniss avance, recule, trop vite.",
            "narrateur|Ses lacets n'ont pas le temps de pendre.",
            "papa|La haie des ailes est juste derrière ?",
            "enfant-m|Oui, papa.",
            "narrateur|Un grain de lavande reste collé au sac.",
            "maman|Le chapeau et la fleur voyagent avec vous.",
        )
    if t1 == 2:
        return L(
            "enfant-m|Sur la tête.",
            "papa|Oui.",
            "copain|Je suis tout petit, dessous !",
            "enfant-m|Reste près de moi, d'abord.",
            "narrateur|Aniss cligne, trop vite.",
            "narrateur|Une mèche lui saute sur l'œil.",
            "maman|Le foin sent fort, dehors.",
            "copain|Oui, maman.",
            "narrateur|Un grain de lavande tient au bord du chapeau.",
            "papa|Le filet et la fleur partent avec vous.",
        )
    return L(
        "enfant-m|Dans la poche.",
        "maman|Oui.",
        "copain|Ça sent la colle.",
        "enfant-m|Le jaune va croire que c'est vrai.",
        "narrateur|Les poignets d'Aniss dépassent des manches.",
        "narrateur|Il frappe deux fois la haie, pour rien.",
        "papa|On ouvre, tous les quatre ?",
        "enfant-m|Oui.",
        "narrateur|Un grain de lavande glisse contre le papier.",
        "maman|Le filet et le chapeau partent avec la fleur.",
    )


def t2_question(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le sac tape la hanche, à chaque pas.",
            "narrateur|Le pré ondule, plus loin que la haie des ailes.",
            "narrateur|Les lavandes font un mur violet, bas.",
            "narrateur|Le muret tient la chaleur du soleil.",
            "papa|On guette où, d'abord ?",
        )
    if t1 == 2:
        return L(
            "narrateur|Le bord du chapeau coupe le soleil.",
            "narrateur|Le pré ondule, plus loin que la haie des ailes.",
            "narrateur|Les lavandes font un mur violet, bas.",
            "narrateur|Le muret tient la chaleur du soleil.",
            "narrateur|Aniss tape deux cailloux, trop fort.",
            "maman|On guette où, Victorino ?",
        )
    return L(
        "narrateur|La poche garde le papier, bien plat.",
        "narrateur|Le pré ondule, plus loin que la haie des ailes.",
        "narrateur|Les lavandes font un mur violet, bas.",
        "narrateur|Le muret tient la chaleur du soleil.",
        "narrateur|Aniss pousse la haie, trop vite.",
        "papa|On guette où, d'abord ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    table = {
        (1, 1): L(
            "narrateur|Victorino lève le filet, comme un toit.",
            "copain|Je le rattrape !",
            "enfant-m|Attends, il va se poser.",
            "narrateur|Aniss part dans l'herbe, trop loin.",
            "narrateur|Le filet racle les tiges, trop vite.",
            "narrateur|Le jaune s'envole, plus haut que leurs têtes.",
            "narrateur|Le sourire de Victorino s'efface.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|Je m'accroupis, à votre hauteur.",
            "narrateur|Aniss ouvre la bouche, puis la referme.",
            "narrateur|Un grain de lavande tombe dans l'herbe.",
            "papa|Vous trouvez, tous les deux ?",
        ),
        (2, 1): L(
            "narrateur|Victorino baisse le chapeau, pour l'ombre.",
            "copain|Je cours dessous !",
            "enfant-m|Pas d'un coup, Aniss.",
            "narrateur|Le chapeau s'envole, puis retombe.",
            "narrateur|L'herbe se lève, comme une vague.",
            "narrateur|Le jaune quitte le pré, d'un trait.",
            "enfant-m|Il est parti.",
            "narrateur|Son sourire n'est plus là.",
            "narrateur|Ça serre, juste sous la gorge.",
            "maman|Je me baisse, face à l'herbe.",
            "narrateur|Aniss ne dit rien.",
            "narrateur|Un grain de lavande reste au bord du bleu.",
            "papa|Vous faites comment, alors ?",
        ),
        (3, 1): L(
            "narrateur|Victorino pose la fleur sur une tige.",
            "copain|Moi je l'apporte au jaune !",
            "enfant-m|Elle doit attendre, elle.",
            "narrateur|Aniss plie le papier contre un genou.",
            "narrateur|La tige se couche, trop vite.",
            "narrateur|Le jaune s'éloigne au-dessus du foin.",
            "narrateur|Le sourire de Victorino se plie aussi.",
            "narrateur|L'envie et la peur se poussent, dans son ventre.",
            "papa|Je m'accroupis, près de la tige.",
            "narrateur|Aniss ferme la bouche.",
            "narrateur|Un grain de lavande roule dans un pli.",
            "maman|Vous trouvez, tous les deux ?",
        ),
        (1, 2): L(
            "narrateur|Victorino glisse le filet entre les tiges.",
            "enfant-m|Ça sent le violet, Aniss.",
            "copain|Je pousse les tiges, trop fort !",
            "narrateur|Un nuage de parfum saute, puis retombe.",
            "narrateur|La poussière violette emplit les mailles.",
            "narrateur|Le jaune quitte le violet, d'un coup.",
            "enfant-m|On a tout réveillé.",
            "narrateur|Victorino ne rit plus.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|Je m'accroupis, entre les tiges.",
            "narrateur|Aniss reste muet, les mains ouvertes.",
            "narrateur|Un grain de lavande tient à une maille.",
            "papa|Vous vous approchez comment ?",
        ),
        (2, 2): L(
            "narrateur|Victorino avance, le chapeau trop bas.",
            "copain|Je secoue le violet !",
            "enfant-m|Pas tout, Aniss.",
            "narrateur|Des brins collent à l'aile du chapeau.",
            "narrateur|Le parfum pique les yeux, trop fort.",
            "narrateur|Le jaune part au-dessus des tiges.",
            "narrateur|Le sourire d'Aniss disparaît.",
            "narrateur|Ça brûle un peu, dans la poitrine.",
            "papa|Je me mets à genoux, au ras du violet.",
            "narrateur|Aniss avale sa phrase.",
            "narrateur|Un grain de lavande reste dans le bleu.",
            "maman|Vous faites comment, tous les deux ?",
        ),
        (3, 2): L(
            "narrateur|Victorino tend la fleur vers le violet.",
            "copain|Je la mets partout !",
            "enfant-m|Un coin, pas tout le rang.",
            "narrateur|Un coude plie le papier, trop fort.",
            "narrateur|Le parfum saute, comme une poussière.",
            "narrateur|Le jaune quitte la haie, d'un trait.",
            "enfant-m|Ma fleur s'est pliée.",
            "narrateur|Son sourire s'efface.",
            "narrateur|L'envie et l'inquiétude se bousculent, sous le pull.",
            "maman|Je m'accroupis, à votre hauteur.",
            "narrateur|Aniss ne répond pas.",
            "narrateur|Un grain de lavande tient au papier.",
            "papa|Vous trouvez, tous les deux ?",
        ),
        (1, 3): L(
            "narrateur|Victorino pose le filet contre la pierre.",
            "enfant-m|La pierre est tiède, Aniss.",
            "copain|J'entends mes pieds deux fois !",
            "narrateur|Chaque clic revient, plus fort.",
            "narrateur|Les pas d'Aniss font trembler le filet.",
            "narrateur|Le jaune fuit le bruit, d'un coup.",
            "enfant-m|Il n'aime pas ça.",
            "narrateur|Le sourire de Victorino n'est plus là.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "papa|Je m'accroupis, contre le muret.",
            "narrateur|Aniss ouvre la bouche, puis plus rien.",
            "narrateur|Un grain de lavande se loge dans une fente.",
            "maman|Vous faites comment, alors ?",
        ),
        (2, 3): L(
            "narrateur|Le chapeau bleu frôle le muret chaud.",
            "copain|Je grimpe, moi !",
            "enfant-m|On reste en bas.",
            "narrateur|Le bord du chapeau tape la pierre.",
            "narrateur|Le clic rebondit le long du mur.",
            "narrateur|Le jaune quitte la pierre chaude.",
            "narrateur|Aniss ne rit plus.",
            "narrateur|Ça serre, juste sous la gorge.",
            "maman|Je me baisse, face aux pierres.",
            "narrateur|Aniss se tait, les poings ouverts.",
            "narrateur|Un grain de lavande tient dans une craquelure.",
            "papa|Vous trouvez, tous les deux ?",
        ),
        (3, 3): L(
            "narrateur|La fleur de papier attend sur la pierre.",
            "copain|Je tape, pour l'appeler !",
            "enfant-m|Le jaune n'aime pas le bruit.",
            "narrateur|La fleur glisse dans une fente.",
            "narrateur|Les clics d'Aniss remplissent le mur.",
            "narrateur|Le jaune s'envole au-dessus des champs.",
            "enfant-m|Elle est coincée.",
            "narrateur|Le sourire de Victorino se plie.",
            "narrateur|L'envie et la peur se poussent, dans son ventre.",
            "papa|Je m'accroupis, près de la fente.",
            "narrateur|Aniss ne dit mot.",
            "narrateur|Un grain de lavande brille au fond.",
            "maman|Vous faites comment, tous les deux ?",
        ),
    }
    return table[(t1, t2)]


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|L'herbe se referme derrière Aniss.",
            "papa|Marcher comme lui, s'asseoir, ou le silence ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le parfum tient, tout bas.",
            "maman|Souffler un peu, attendre, ou la fleur de papa ?",
        )
    return L(
        "narrateur|Un dernier clic roule le long du muret.",
        "papa|Le rythme, en bas, ou la main de maman ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    table = {
        (1, 1, 1): L(
            "enfant-m|On marche comme lui.",
            "copain|Moi je bats des bras, trop vite.",
            "enfant-m|Plus lent, Aniss.",
            "narrateur|Victorino refuse de foncer.",
            "narrateur|Le filet suit leurs bras, un peu.",
            "narrateur|Deux ombres avancent dans l'herbe, sans courir.",
            "narrateur|Aniss lève un pied, puis le repose.",
            "narrateur|Le grain de lavande brille sur une tige.",
            "enfant-m|Le jaune a des ailes comme ça.",
            "papa|Vous jouez à son pas.",
        ),
        (2, 1, 1): L(
            "enfant-m|On marche comme lui.",
            "copain|Dessous le chapeau, je cours !",
            "enfant-m|Un pas, pas dix.",
            "narrateur|Victorino garde son élan, pour plus tard.",
            "narrateur|Le chapeau fait une ombre, lente.",
            "narrateur|Aniss pose le talon, puis la pointe.",
            "narrateur|Le grain de lavande glisse au bord du bleu.",
            "copain|Mes pieds écoutent, là.",
            "maman|Le pré vous a laissés entrer.",
            "papa|Vous donnez un peu, pas tout.",
        ),
        (3, 1, 1): L(
            "enfant-m|On marche comme lui.",
            "copain|Je lève la fleur, trop haut !",
            "enfant-m|Elle se lève, elle se pose.",
            "narrateur|Victorino ne part pas d'un coup.",
            "narrateur|La fleur avance au rythme des ailes.",
            "narrateur|Aniss compte ses pas, tout bas.",
            "narrateur|Le grain de lavande tient au papier.",
            "enfant-m|Le jaune nous a vus.",
            "papa|Vous jouez à son pas.",
            "maman|La tige n'a pas plié.",
        ),
        (1, 1, 2): L(
            "enfant-m|On s'assoit un peu.",
            "copain|Je veux courir !",
            "narrateur|Aniss s'arrête, les genoux tremblants.",
            "narrateur|Victorino s'arrête, sans tout donner.",
            "narrateur|Le filet vert dort sur les genoux.",
            "narrateur|Une tige se redresse, contre sa chaussure.",
            "narrateur|Le grain de lavande repose dans l'herbe.",
            "copain|Je ne cours plus.",
            "papa|Vous avez attendu l'herbe.",
            "maman|Le jaune peut redescendre, maintenant.",
        ),
        (2, 1, 2): L(
            "enfant-m|On s'assoit un peu.",
            "copain|Le chapeau, je le jette en l'air !",
            "enfant-m|Il reste sur ta tête.",
            "narrateur|Victorino tient son envie, un moment.",
            "narrateur|Le chapeau bleu fait un toit, assis.",
            "narrateur|Aniss pose les genoux dans l'herbe.",
            "narrateur|Le grain de lavande tient au bord.",
            "copain|Je suis prêt.",
            "papa|Vous avez attendu, assis.",
            "maman|Une tige vous chatouille, sans rien dire.",
        ),
        (3, 1, 2): L(
            "enfant-m|On s'assoit un peu.",
            "copain|Je tends la fleur, loin !",
            "enfant-m|Elle attend, sur nos genoux.",
            "narrateur|Victorino pose son élan, à côté.",
            "narrateur|La fleur de papier tient entre deux paumes.",
            "narrateur|Aniss souffle, puis se tait.",
            "narrateur|Le grain de lavande reste dans un pli.",
            "copain|Je ne cours plus.",
            "papa|Vous avez attendu l'herbe.",
            "maman|Le jaune peut redescendre.",
        ),
        (1, 1, 3): L(
            "enfant-m|Maman, tu restes avec nous ?",
            "maman|J'écoute l'herbe.",
            "narrateur|Aniss ouvre la bouche, puis la referme.",
            "narrateur|Ce silence répond.",
            "narrateur|Victorino choisit d'attendre un peu.",
            "narrateur|Il tient le filet, sans le secouer.",
            "narrateur|Le grain de lavande dort dans une maille.",
            "copain|Je peux être silencieux.",
            "papa|Vous avez demandé, et ça tient.",
            "maman|Mon silence a tenu vos pieds.",
        ),
        (2, 1, 3): L(
            "enfant-m|Maman, tu restes avec nous ?",
            "maman|J'écoute l'herbe.",
            "narrateur|Aniss avale son cri.",
            "narrateur|Ce silence répond.",
            "narrateur|Victorino n'y va pas d'un seul geste.",
            "narrateur|Il tient le chapeau, sans le secouer.",
            "narrateur|Le grain de lavande tient au bord.",
            "copain|Moi aussi, j'écoute.",
            "papa|Un criquet reprend, tout près.",
            "maman|Mon silence a tenu vos pieds.",
        ),
        (3, 1, 3): L(
            "enfant-m|Maman, tu restes avec nous ?",
            "maman|J'écoute l'herbe.",
            "narrateur|Aniss lève un doigt, puis le baisse.",
            "narrateur|Ce silence répond.",
            "narrateur|Victorino garde une part d'élan.",
            "narrateur|Il tient la fleur, sans la secouer.",
            "narrateur|Le grain de lavande brille au creux.",
            "copain|Je peux être silencieux.",
            "enfant-m|Moi aussi, j'écoute.",
            "maman|Mon silence a tenu vos pieds.",
        ),
        (1, 2, 1): L(
            "enfant-m|On souffle un peu.",
            "copain|Comme le grand vent !",
            "enfant-m|Plus bas, Aniss.",
            "narrateur|Victorino refuse de foncer.",
            "narrateur|Il garde le filet, Aniss souffle devant.",
            "narrateur|Deux souffles passent sur la même tige.",
            "narrateur|Le grain de lavande penche, puis se tient.",
            "copain|J'ai soufflé plus bas, cette fois.",
            "papa|Vous avez joué avec l'air.",
            "maman|Les fleurs sont restées debout.",
        ),
        (2, 2, 1): L(
            "enfant-m|On souffle un peu.",
            "copain|Je souffle tout !",
            "enfant-m|Un souffle, puis on attend.",
            "narrateur|Victorino garde son élan, pour plus tard.",
            "narrateur|Il garde le chapeau, Aniss souffle devant.",
            "narrateur|Le violet penche, puis se redresse.",
            "narrateur|Le grain de lavande reste dans le bleu.",
            "enfant-m|On n'a rien cassé.",
            "papa|Vous avez joué avec l'air.",
            "maman|Les fleurs sont restées debout.",
        ),
        (3, 2, 1): L(
            "enfant-m|On souffle un peu.",
            "copain|Sur la fleur, fort !",
            "enfant-m|Sur la tige, pas sur le papier.",
            "narrateur|Victorino ne part pas d'un coup.",
            "narrateur|Il garde la fleur, Aniss souffle devant.",
            "narrateur|Deux souffles passent, puis s'arrêtent.",
            "narrateur|Le grain de lavande tient au papier.",
            "copain|J'ai soufflé plus bas.",
            "papa|Vous avez joué avec l'air.",
            "maman|Les fleurs sont restées debout.",
        ),
        (1, 2, 2): L(
            "enfant-m|J'attends le parfum.",
            "copain|Quand il retombe, on avance.",
            "narrateur|Victorino s'arrête, sans tout donner.",
            "narrateur|Il tient le filet, sans le bouger.",
            "narrateur|Aniss compte les tiges, tout bas.",
            "narrateur|Le nuage violet s'assoit, enfin.",
            "narrateur|Le grain de lavande reparaît sur une feuille.",
            "copain|C'est à toi, Victorino.",
            "papa|Le parfum vous a fait de la place.",
            "maman|Vous l'avez laissé se poser.",
        ),
        (2, 2, 2): L(
            "enfant-m|J'attends le parfum.",
            "copain|Je pousse, moi !",
            "enfant-m|On attend qu'il s'asseye.",
            "narrateur|Victorino tient son envie, un moment.",
            "narrateur|Il tient le chapeau, sans le bouger.",
            "narrateur|Aniss compte, tout bas.",
            "narrateur|Le nuage violet s'assoit.",
            "narrateur|Le grain de lavande brille au bord.",
            "papa|Le parfum vous a fait de la place.",
            "maman|Vous l'avez laissé se poser.",
        ),
        (3, 2, 2): L(
            "enfant-m|J'attends le parfum.",
            "copain|La fleur, je la sors !",
            "enfant-m|Elle attend, dans la poche.",
            "narrateur|Victorino pose son élan, à côté.",
            "narrateur|Il tient la fleur, sans la bouger.",
            "narrateur|Aniss compte les tiges, tout bas.",
            "narrateur|Le nuage violet s'assoit, enfin.",
            "narrateur|Le grain de lavande reparaît sur le papier.",
            "papa|Le parfum vous a fait de la place.",
            "maman|Vous l'avez laissé se poser.",
        ),
        (1, 2, 3): L(
            "enfant-m|Papa, tu gardes la fleur ?",
            "papa|Je la tends, un pas chacun.",
            "copain|Moi je cours le dernier !",
            "enfant-m|Un pas, Aniss.",
            "narrateur|Victorino choisit d'attendre un peu.",
            "narrateur|Papa pose la fleur près du filet.",
            "narrateur|Aniss pose un pied, puis l'autre.",
            "narrateur|Le grain de lavande glisse vers la paume.",
            "maman|Vous avez demandé, un pas chacun.",
            "papa|Ma main n'a pas bougé.",
        ),
        (2, 2, 3): L(
            "enfant-m|Papa, tu gardes la fleur ?",
            "papa|Je la tends, un pas chacun.",
            "narrateur|Victorino n'y va pas d'un seul geste.",
            "narrateur|Papa pose la fleur près du chapeau.",
            "narrateur|Aniss pose un pied, puis l'autre.",
            "narrateur|Victorino pose le même pas, plus tard.",
            "narrateur|Le grain de lavande tient au bord.",
            "copain|On a demandé, et ça va.",
            "maman|Vous avez demandé, un pas chacun.",
            "papa|Ma main n'a pas bougé.",
        ),
        (3, 2, 3): L(
            "enfant-m|Papa, tu gardes la fleur ?",
            "papa|Je la tends, un pas chacun.",
            "copain|Je la prends, d'un coup !",
            "enfant-m|Ta paume, pas tes deux mains.",
            "narrateur|Victorino garde une part d'élan.",
            "narrateur|Papa pose la fleur dans sa paume.",
            "narrateur|Aniss pose un pied, puis l'autre.",
            "narrateur|Le grain de lavande reste au creux.",
            "maman|Vous avez demandé, un pas chacun.",
            "papa|Ma main n'a pas bougé.",
        ),
        (1, 3, 1): L(
            "enfant-m|On tape une fois, puis plus.",
            "copain|Toc toc toc !",
            "enfant-m|Un toc, Aniss.",
            "narrateur|Victorino refuse de foncer.",
            "narrateur|Il pose une main sur l'épaule d'Aniss.",
            "narrateur|Le filet vert se pose après le dernier toc.",
            "narrateur|La pierre répond, puis se tait.",
            "narrateur|Le grain de lavande brille dans la fente.",
            "papa|Vous avez joué avec le bruit.",
            "maman|Un toc, puis la pierre dort.",
        ),
        (2, 3, 1): L(
            "enfant-m|On tape une fois, puis plus.",
            "copain|Moi je tambourine !",
            "enfant-m|Un toc, et j'attends.",
            "narrateur|Victorino garde son élan, pour plus tard.",
            "narrateur|Le chapeau bleu s'arrête après le dernier toc.",
            "narrateur|La pierre répond, puis se tait.",
            "narrateur|Le grain de lavande tient dans la craquelure.",
            "copain|Moi aussi, après le toc.",
            "papa|Vous avez joué avec le bruit.",
            "maman|Un toc, puis la pierre dort.",
        ),
        (3, 3, 1): L(
            "enfant-m|On tape une fois, puis plus.",
            "copain|Pour réveiller la fleur !",
            "enfant-m|Elle écoute le silence, après.",
            "narrateur|Victorino ne part pas d'un coup.",
            "narrateur|La fleur de papier s'arrête après le dernier toc.",
            "narrateur|La pierre répond, puis se tait.",
            "narrateur|Le grain de lavande brille au fond.",
            "enfant-m|Le jaune aime le silence, après.",
            "papa|Vous avez joué avec le bruit.",
            "maman|Un toc, puis la pierre dort.",
        ),
        (1, 3, 2): L(
            "enfant-m|On attend en bas.",
            "copain|Je grimpe !",
            "enfant-m|La pierre se tait, d'abord.",
            "narrateur|Victorino s'arrête, sans tout donner.",
            "narrateur|Leurs chaussures restent dans l'herbe fraîche.",
            "narrateur|Le filet vert reste dans l'herbe, en bas.",
            "narrateur|Le muret ne clique plus.",
            "narrateur|Le grain de lavande reparaît dans la fente.",
            "papa|Vous avez laissé le bruit s'en aller.",
            "maman|En bas, vos pieds sont plus doux.",
        ),
        (2, 3, 2): L(
            "enfant-m|On attend en bas.",
            "copain|Le chapeau, je le pose en haut !",
            "enfant-m|Il reste avec nous, en bas.",
            "narrateur|Victorino tient son envie, un moment.",
            "narrateur|Le chapeau bleu reste dans l'ombre, en bas.",
            "narrateur|Le muret ne clique plus.",
            "narrateur|Le grain de lavande tient dans la craquelure.",
            "copain|Maintenant, on peut regarder.",
            "papa|Vous avez laissé le bruit s'en aller.",
            "maman|En bas, vos pieds sont plus doux.",
        ),
        (3, 3, 2): L(
            "enfant-m|On attend en bas.",
            "copain|Je sors la fleur d'en haut !",
            "enfant-m|Elle reste dans l'herbe.",
            "narrateur|Victorino pose son élan, à côté.",
            "narrateur|La fleur de papier reste dans l'herbe, en bas.",
            "narrateur|Le muret ne clique plus.",
            "narrateur|Le grain de lavande brille au fond.",
            "copain|À toi, puis à moi.",
            "papa|Vous avez laissé le bruit s'en aller.",
            "maman|En bas, vos pieds sont plus doux.",
        ),
        (1, 3, 3): L(
            "enfant-m|Maman, tu tends la main ?",
            "maman|Je reste, et vous venez un peu.",
            "copain|Je dépasse ta main !",
            "enfant-m|On s'arrête dessus.",
            "narrateur|Victorino choisit d'attendre un peu.",
            "narrateur|Il lève le filet quand maman ouvre la paume.",
            "narrateur|Aniss regarde la paume, plus que ses pieds.",
            "narrateur|Le grain de lavande dort dans ses plis.",
            "papa|Vous avez demandé la main.",
            "maman|Ma paume est devenue une tige.",
        ),
        (2, 3, 3): L(
            "enfant-m|Maman, tu tends la main ?",
            "maman|Je reste, et vous venez un peu.",
            "narrateur|Victorino n'y va pas d'un seul geste.",
            "narrateur|Il touche le chapeau quand maman ouvre la paume.",
            "narrateur|Aniss s'arrête devant sa main.",
            "narrateur|Le grain de lavande glisse dans un pli.",
            "copain|Je m'arrête devant ta main.",
            "enfant-m|Moi aussi, j'écoute.",
            "papa|Vous avez demandé la main.",
            "maman|Ma paume est devenue une tige.",
        ),
        (3, 3, 3): L(
            "enfant-m|Maman, tu tends la main ?",
            "maman|Je reste, et vous venez un peu.",
            "copain|La fleur, je la pose plus loin !",
            "enfant-m|Sur sa paume, pas plus.",
            "narrateur|Victorino garde une part d'élan.",
            "narrateur|Il lève la fleur quand maman ouvre la paume.",
            "narrateur|Aniss regarde la paume, plus que ses pieds.",
            "narrateur|Le grain de lavande dort dans ses plis.",
            "papa|Vous avez demandé la main.",
            "maman|Ma paume est devenue une tige.",
        ),
    }
    return table[(t1, t2, t3)]


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = T1[t1]
    table = {
        (1, 1, 1): L(
            "narrateur|Le papillon jaune se pose, au bout d'une tige.",
            "copain|Mes bras ont fait des ailes.",
            "enfant-m|Les miennes aussi, plus lentes.",
            "papa|Vous avez marché à son pas.",
            "maman|Le pré sent le foin coupé.",
            o["coda"],
            "narrateur|Un grain de lavande dort dans une maille.",
            "enfant-m|Il est venu, Aniss.",
            "narrateur|La pince à linge cliquette, loin, sur le fil.",
        ),
        (2, 1, 1): L(
            "narrateur|Le papillon jaune se pose sous l'ombre bleue.",
            "copain|J'ai donné un pas, pas dix.",
            "enfant-m|Le chapeau a tenu.",
            "papa|Vous avez donné un peu, pas tout.",
            "maman|Le pré sent le foin coupé.",
            o["coda"],
            "narrateur|Un grain de lavande tient au bord du bleu.",
            "enfant-m|Il est venu, Aniss.",
            "narrateur|Une ombre de haie barre l'herbe, puis s'en va.",
        ),
        (3, 1, 1): L(
            "narrateur|Le papillon jaune se pose sur le papier.",
            "copain|J'ai compté mes pas.",
            "enfant-m|La tige n'a pas plié.",
            "papa|Vous avez joué à son pas.",
            "maman|Le pré sent le foin coupé.",
            o["coda"],
            "narrateur|Un grain de lavande reste au creux du papier.",
            "enfant-m|Il est venu, Aniss.",
            "narrateur|Le linge bat, une fois, puis s'arrête.",
        ),
        (1, 1, 2): L(
            "narrateur|L'herbe garde la chaleur des genoux.",
            "enfant-m|Tu t'es assis, d'abord.",
            "copain|Puis le jaune est venu, tout droit.",
            "papa|Vous avez attendu, assis.",
            "maman|Une tige vous a chatouillés, sans rien dire.",
            o["coda"],
            "narrateur|Un grain de lavande reste coincé au tissu.",
            "enfant-m|À plus tard, les tiges.",
            "narrateur|Le gravier du chemin brille, un peu.",
        ),
        (2, 1, 2): L(
            "narrateur|Le chapeau fait un nid d'ombre, assis.",
            "copain|Je suis resté dessous.",
            "enfant-m|Le jaune a choisi notre toit.",
            "papa|Vous avez attendu, assis.",
            "maman|Une tige vous a chatouillés, sans rien dire.",
            o["coda"],
            "narrateur|Un grain de lavande tient au bord du bleu.",
            "enfant-m|À plus tard, les tiges.",
            "narrateur|Un bouton de chemise tape le fil, au loin.",
        ),
        (3, 1, 2): L(
            "narrateur|La fleur de papier s'ouvre entre deux paumes.",
            "copain|Je ne cours plus.",
            "enfant-m|Il s'est posé dessus.",
            "papa|Vous avez attendu l'herbe.",
            "maman|Le jaune a choisi le papier.",
            o["coda"],
            "narrateur|Un grain de lavande reste dans un pli.",
            "enfant-m|À plus tard, les tiges.",
            "narrateur|Un brin d'herbe sèche sur le genou.",
        ),
        (1, 1, 3): L(
            "narrateur|Le silence de maman reste dans l'air, léger.",
            "copain|J'ai fermé la bouche.",
            "enfant-m|On a demandé, et ça tenait.",
            "maman|Mon silence a tenu vos pieds.",
            "papa|Le criquet a repris, pour vous.",
            "narrateur|Le filet vert pose un grain de lavande sur le bois.",
            "narrateur|Victorino touche la tige, du bout.",
            "copain|Il s'est posé.",
            "narrateur|Une ombre de haie barre l'herbe, un moment.",
        ),
        (2, 1, 3): L(
            "narrateur|Le chapeau bleu garde le silence de maman.",
            "copain|Moi aussi, j'écoute.",
            "enfant-m|Le criquet a repris.",
            "maman|Mon silence a tenu vos pieds.",
            "papa|Le jaune a choisi le calme.",
            o["coda"],
            "narrateur|Un grain de lavande tient au bord.",
            "copain|Il s'est posé.",
            "narrateur|Le fil du linge s'immobilise, au loin.",
        ),
        (3, 1, 3): L(
            "narrateur|La fleur de papier n'a pas bougé.",
            "copain|Je peux être silencieux.",
            "enfant-m|Il s'est posé sans un mot.",
            "maman|Mon silence a tenu vos pieds.",
            "papa|Le criquet a repris, pour vous.",
            o["coda"],
            "narrateur|Un grain de lavande brille au creux.",
            "copain|Il s'est posé.",
            "narrateur|Une feuille tourne, puis se couche.",
        ),
        (1, 2, 1): L(
            "narrateur|Deux souffles marquent la même tige violette.",
            "enfant-m|On n'a rien cassé.",
            "copain|J'ai soufflé plus bas.",
            "papa|Vous avez joué avec l'air.",
            "maman|Les lavandes sont restées debout.",
            o["coda"],
            "narrateur|Un grain de lavande sèche sur le tissu.",
            "enfant-m|Le parfum rentre avec nous.",
            "narrateur|La haie des ailes fait une ombre ronde.",
        ),
        (2, 2, 1): L(
            "narrateur|Le chapeau bleu sent le violet, un peu.",
            "enfant-m|On n'a rien cassé.",
            "copain|Un souffle, puis on a attendu.",
            "papa|Vous avez joué avec l'air.",
            "maman|Les lavandes sont restées debout.",
            o["coda"],
            "narrateur|Un grain de lavande reste dans le bleu.",
            "enfant-m|Le parfum rentre avec nous.",
            "narrateur|Un brin violet sèche sur l'épaule.",
        ),
        (3, 2, 1): L(
            "narrateur|La fleur de papier n'a pas volé.",
            "copain|J'ai soufflé plus bas.",
            "enfant-m|Sur la tige, pas sur le papier.",
            "papa|Vous avez joué avec l'air.",
            "maman|Les lavandes sont restées debout.",
            o["coda"],
            "narrateur|Un grain de lavande tient au papier.",
            "enfant-m|Le parfum rentre avec nous.",
            "narrateur|Une tige violette penche, puis se tient.",
        ),
        (1, 2, 2): L(
            "narrateur|Le parfum s'est assis, tout bas.",
            "copain|Quand il est retombé, on a avancé.",
            "enfant-m|J'ai attendu ta tige.",
            "maman|Le nuage vous a laissés passer.",
            "papa|Vous l'avez laissé se poser.",
            "narrateur|Le filet vert garde un grain de lavande.",
            "narrateur|Victorino souffle dessus, un peu.",
            "copain|Au revoir, les tiges.",
            "narrateur|Une abeille passe, sans se presser.",
        ),
        (2, 2, 2): L(
            "narrateur|Le parfum s'est assis sous le chapeau.",
            "copain|J'ai compté, tout bas.",
            "enfant-m|Le jaune a attendu avec nous.",
            "maman|Le nuage vous a laissés passer.",
            "papa|Vous l'avez laissé se poser.",
            o["coda"],
            "narrateur|Un grain de lavande brille au bord.",
            "copain|Au revoir, les tiges.",
            "narrateur|Le violet redevient un mur, bas.",
        ),
        (3, 2, 2): L(
            "narrateur|Le parfum s'est assis sur le papier.",
            "copain|La fleur a attendu, dans la poche.",
            "enfant-m|Puis le jaune est venu.",
            "maman|Le nuage vous a laissés passer.",
            "papa|Vous l'avez laissé se poser.",
            o["coda"],
            "narrateur|Un grain de lavande reparaît sur le papier.",
            "copain|Au revoir, les tiges.",
            "narrateur|Une poussière violette tombe, puis plus rien.",
        ),
        (1, 2, 3): L(
            "narrateur|La fleur de papa repose près du violet.",
            "enfant-m|Tu la tendais, un pas chacun.",
            "copain|On a demandé, et ça venait juste.",
            "papa|Ma main n'a pas bougé.",
            "maman|Les lavandes ont rendu le jaune.",
            o["coda"],
            "narrateur|Un grain de lavande reste sur une feuille.",
            "enfant-m|Regarde, Aniss, il brille.",
            "narrateur|Le soleil quitte le violet, un peu.",
        ),
        (2, 2, 3): L(
            "narrateur|Le chapeau bleu frôle la fleur de papa.",
            "enfant-m|Un pas, puis le même pas.",
            "copain|On a demandé, et ça va.",
            "papa|Ma main n'a pas bougé.",
            "maman|Les lavandes ont rendu le jaune.",
            o["coda"],
            "narrateur|Un grain de lavande tient au bord.",
            "enfant-m|Regarde, Aniss, il brille.",
            "narrateur|On n'avait plus besoin d'un pas.",
        ),
        (3, 2, 3): L(
            "narrateur|La fleur de papier dort dans la paume de papa.",
            "copain|Ta paume, pas mes deux mains.",
            "enfant-m|Le jaune a choisi ça.",
            "papa|Ma main n'a pas bougé.",
            "maman|Les lavandes ont rendu le jaune.",
            o["coda"],
            "narrateur|Un grain de lavande reste au creux.",
            "enfant-m|Regarde, Aniss, il brille.",
            "narrateur|La colle du papier a gardé le grain.",
        ),
        (1, 3, 1): L(
            "narrateur|Après le toc, le jaune se pose.",
            "copain|J'ai tapé une fois, puis plus.",
            "enfant-m|J'avais la main sur ton épaule.",
            "papa|La pierre a fini par dormir.",
            "maman|Un toc, puis le silence.",
            o["coda"],
            "narrateur|Un grain de lavande brille dans la fente.",
            "enfant-m|Le muret s'est tu.",
            "narrateur|Une poussière tourne, puis tombe.",
        ),
        (2, 3, 1): L(
            "narrateur|Après le toc, le jaune se pose sur le bleu.",
            "copain|Moi aussi, après le toc.",
            "enfant-m|Le chapeau n'a plus tapé.",
            "papa|La pierre a fini par dormir.",
            "maman|Un toc, puis le silence.",
            o["coda"],
            "narrateur|Un grain de lavande tient dans la craquelure.",
            "enfant-m|Le muret s'est tu.",
            "narrateur|Le chaud de la pierre redescend.",
        ),
        (3, 3, 1): L(
            "narrateur|Après le toc, le jaune se pose sur le papier.",
            "copain|Elle a écouté le silence, après.",
            "enfant-m|Un toc, pas dix.",
            "papa|La pierre a fini par dormir.",
            "maman|Un toc, puis le silence.",
            o["coda"],
            "narrateur|Un grain de lavande brille au fond.",
            "enfant-m|Le muret s'est tu.",
            "narrateur|Un oiseau passe au-dessus, sans crier.",
        ),
        (1, 3, 2): L(
            "narrateur|La pierre s'est tue, enfin, tout à fait.",
            "enfant-m|On a attendu en bas.",
            "copain|Nos chaussures sont restées dans l'herbe.",
            "papa|Le silence vous a laissé le jaune.",
            "maman|En bas, vos pieds étaient plus doux.",
            "narrateur|Le filet vert ne fait plus aucun bruit.",
            "narrateur|Victorino pose la paume sur la pierre chaude.",
            "copain|Elle est tiède.",
            "narrateur|Un grain de lavande reparaît dans la fente.",
        ),
        (2, 3, 2): L(
            "narrateur|La pierre s'est tue sous le chapeau.",
            "enfant-m|On a attendu en bas.",
            "copain|Maintenant, on peut regarder.",
            "papa|Le silence vous a laissé le jaune.",
            "maman|En bas, vos pieds étaient plus doux.",
            o["coda"],
            "narrateur|Un grain de lavande tient dans la craquelure.",
            "copain|Elle est tiède.",
            "narrateur|L'herbe fraîche garde la forme des chaussures.",
        ),
        (3, 3, 2): L(
            "narrateur|La pierre s'est tue près du papier.",
            "enfant-m|On a attendu en bas.",
            "copain|À toi, puis à moi.",
            "papa|Le silence vous a laissé le jaune.",
            "maman|En bas, vos pieds étaient plus doux.",
            o["coda"],
            "narrateur|Un grain de lavande brille au fond.",
            "copain|Elle est tiède.",
            "narrateur|Une fente du muret garde un peu d'ombre.",
        ),
        (1, 3, 3): L(
            "narrateur|La paume de maman s'ouvre, puis se referme.",
            "enfant-m|J'écoutais ta main.",
            "copain|Moi aussi, je m'arrêtais dessus.",
            "maman|Vous avez demandé le calme.",
            "papa|Un grain de lavande reste dans ses plis.",
            o["coda"],
            "narrateur|Victorino touche la pierre, du bout des doigts.",
            "enfant-m|Il s'est posé, Aniss.",
            "narrateur|La pierre garde une poussière, puis plus rien.",
        ),
        (2, 3, 3): L(
            "narrateur|La paume de maman sent le savon du linge.",
            "enfant-m|J'écoutais ta main.",
            "copain|Je m'arrête devant ta main.",
            "maman|Vous avez demandé le calme.",
            "papa|Un grain de lavande reste dans ses plis.",
            o["coda"],
            "narrateur|Victorino touche le bord du bleu.",
            "enfant-m|Il s'est posé, Aniss.",
            "narrateur|La pince à linge cliquette, loin, une fois.",
        ),
        (3, 3, 3): L(
            "narrateur|La paume de maman porte la fleur un instant.",
            "enfant-m|J'écoutais ta main.",
            "copain|Sur sa paume, pas plus.",
            "maman|Vous avez demandé le calme.",
            "papa|Un grain de lavande reste dans ses plis.",
            o["coda"],
            "narrateur|Victorino touche le papier, du bout.",
            "enfant-m|Il s'est posé, Aniss.",
            "narrateur|La haie des ailes redevient une haie, simple.",
        ),
    }
    return table[(t1, t2, t3)]


def write_tree() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    scripts: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {}
    profiles: dict[str, str] = {}
    emph: dict[str, str | None] = {}

    scripts["CHK_T0000_P0000"] = L(
        "narrateur|La pince à linge cliquette, sur le fil.",
        "narrateur|Une aile jaune copie le clic, puis part.",
        "narrateur|Sur le bois de la pince, un grain de lavande tient.",
        "enfant-m|Il est collé, gris bleu.",
        "papa|Tu l'as vu, Victorino ?",
        "enfant-m|Oui, il est minuscule.",
        "maman|Le pré commence derrière la haie des ailes.",
        "narrateur|Victorino vit ici, avec papa et maman.",
        "narrateur|Le village touche les champs.",
        "narrateur|La fleur de papier attend, dans la poche de maman.",
        "narrateur|Le filet vert et le chapeau bleu pendent près du panier.",
        "narrateur|Derrière la haie, le foin sent fort.",
        "narrateur|Le vent soulève une manche, puis la laisse.",
        "copain|Je le prends, le jaune !",
        "narrateur|Aniss arrive, trop vite, les lacets ouverts.",
        "enfant-m|Non, je veux qu'il se pose.",
        "narrateur|En ce moment, Victorino serre le grain de lavande.",
        "papa|Vous n'avez pas la même envie.",
        "enfant-m|Moi, sur la fleur de papier.",
        "copain|Moi, dans le filet, vite.",
        "narrateur|Aniss tape du pied, puis s'arrête.",
        "papa|Il reviendra, si on reste.",
        "maman|Le filet, le chapeau, et la fleur, vous les emportez.",
        "papa|Merci, tu as montré le grain.",
    )
    sons["CHK_T0000_P0000"] = "pince,vent"
    profiles["CHK_T0000_P0000"] = "opening"
    emph["CHK_T0000_P0000"] = "grain de lavande"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|Le filet vert, le chapeau bleu, la fleur de papier.",
        "narrateur|Les trois affaires restent avec eux.",
        "narrateur|Rien ne reste près du fil.",
        "narrateur|Aniss se balance d'un pied sur l'autre.",
        "maman|Tu prends quoi d'abord, Victorino ?",
    )
    profiles["CHK_T0001_P0000"] = "choice"
    extras["CHK_T0001_P0000"] = t3lab("le filet vert", "le chapeau bleu", "la fleur de papier")

    t2_sons = {1: "herbe,pas", 2: "tiges,parfum", 3: "pierre,clic"}
    t2_emph = {1: "pré", 2: "lavandes", 3: "muret"}
    t3_emph = {
        1: {1: "pas", 2: "genoux", 3: "silence"},
        2: {1: "souffle", 2: "parfum", 3: "fleur"},
        3: {1: "toc", 2: "herbe", 3: "paume"},
    }

    for t1 in (1, 2, 3):
        meta = T1[t1]
        base = f"CHK_T0001_P000{t1}"
        scripts[base] = t1_passage(t1)
        sons[base] = meta["sons"]
        profiles[base] = "action"
        emph[base] = meta["emph"]

        qid = f"{base}_Q0001"
        scripts[qid] = t1_q(t1)
        profiles[qid] = "clue"
        extras[qid] = qf(meta["ans"], meta["acc"], meta["retry"])
        emph[qid] = meta["emph"]

        cid = f"{base}_C0001"
        scripts[cid] = t1_confirm(t1)
        profiles[cid] = "confirm"
        emph[cid] = "grain de lavande"

        t2q = f"{base}_T0002_P0000"
        scripts[t2q] = t2_question(t1)
        profiles[t2q] = "choice"
        extras[t2q] = t3lab("le pré", "les lavandes", "le muret")

        for t2 in (1, 2, 3):
            p2 = f"{base}_T0002_P000{t2}"
            scripts[p2] = t2_scene(t1, t2)
            sons[p2] = t2_sons[t2]
            profiles[p2] = "obstacle"
            emph[p2] = t2_emph[t2]

            t3q = f"{p2}_T0003_P0000"
            scripts[t3q] = t3_question(t2)
            profiles[t3q] = "choice"
            extras[t3q] = t3lab(*T3_LABS[t2])

            for t3i in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{t3i}"
                scripts[p3] = t3_scene(t1, t2, t3i)
                sons[p3] = t2_sons[t2]
                profiles[p3] = "resolution"
                emph[p3] = "grain de lavande"

                fin = f"{p3}_F0001"
                scripts[fin] = fin_scene(t1, t2, t3i)
                sons[fin] = "ailes,silence"
                profiles[fin] = "ending"
                emph[fin] = "grain de lavande"

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{SID} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        extra_voice: dict = {}
        if cid in emph:
            extra_voice["emphasis"] = emph[cid]
        kind = c.get("kind") or ""
        if kind in ("passage_question", "transition_question"):
            extra_voice["pause_before"] = 200
        nc = voice(c, scripts[cid], profiles[cid], sons.get(cid, c.get("sons") or "") or "", extra_voice or None)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]

    check(SID, out["age_band"], out["chunks"])

    if len(out["chunks"]) != 86:
        raise SystemExit(f"{SID}: {len(out['chunks'])} chunks != 86")

    fins = [c for c in out["chunks"] if c.get("kind") == "passage_fin"]
    texts = [c["text"] for c in fins]
    if len(texts) != 27:
        raise SystemExit(f"fins {len(texts)} != 27")
    if len(set(texts)) != 27:
        raise SystemExit("fins non distinctes")
    lasts = []
    for c in fins:
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{c['chunk_id']} fin mécanique: {last}")
        if "grain de lavande" not in c["text"].lower():
            raise SystemExit(f"{c['chunk_id']} indice grain de lavande absent de la fin")
        lasts.append(last)
    if len(set(lasts)) != 27:
        raise SystemExit("dernières images non distinctes")

    t3s = [c for c in out["chunks"] if c["chunk_id"].endswith("T0003_P0001")
           or c["chunk_id"].endswith("T0003_P0002") or c["chunk_id"].endswith("T0003_P0003")]
    t3s = [c for c in t3s if c.get("kind") == "passage"]
    if len(t3s) != 27:
        raise SystemExit(f"T3 {len(t3s)} != 27")
    for c in t3s:
        if "refuse de foncer" not in c["text"].lower() and "grain de lavande" not in c["text"].lower():
            raise SystemExit(f"{c['chunk_id']} T3 sans ruse/indice")
        if "grain de lavande" not in c["text"].lower():
            raise SystemExit(f"{c['chunk_id']} grain absent du climax")

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for tic in TIC_PHRASES:
        if tic in blob:
            raise SystemExit(f"{SID} tic script: {tic}")
    for bad in ("déjà", "deja", "encore"):
        if re.search(rf"\b{bad}\b", blob):
            raise SystemExit(f"{SID} tic corpus: {bad}")
    for clue in OLD_CLUES:
        if clue in blob:
            raise SystemExit(f"{SID} vieux indice: {clue}")
    for calque in (
        "merle",
        "miel",
        "gouttes au bord",
        "j'ai compris",
        "mission accomplie",
        "on va apprendre",
        "portail",
        "balle rouge",
        "ticket",
        "quai",
        "grand-père",
        "maîtresse",
        "jardinier",
        "bibliothécaire",
        "gardienne",
        "sami",
        "marelle",
    ):
        if calque in blob:
            raise SystemExit(f"{SID} calque: {calque}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "victorino" not in blob or "aniss" not in blob:
        raise SystemExit(f"{SID}: troupe Victorino/Aniss absente")
    if "grain de lavande" not in blob:
        raise SystemExit(f"{SID}: indice grain de lavande absent")
    if "haie des ailes" not in blob:
        raise SystemExit(f"{SID}: coin nommé absent")
    if not all(c.get("text_xai_tags") for c in out["chunks"]):
        raise SystemExit(f"{SID}: text_xai_tags manquant")
    if not all(c.get("notes") for c in out["chunks"]):
        raise SystemExit(f"{SID}: notes manquant")
    if not all(c.get("text_ssml") for c in out["chunks"]):
        raise SystemExit(f"{SID}: text_ssml manquant")
    if any(c.get("text_xai_tags") == c.get("text") for c in out["chunks"]):
        raise SystemExit(f"{SID}: text_xai_tags = text")

    src_by = {c["chunk_id"]: c for c in src["chunks"]}
    for c in out["chunks"]:
        old = src_by[c["chunk_id"]]
        for k in ("option_1_label", "option_2_label", "option_3_label",
                  "option_1_next_chunk", "option_2_next_chunk", "option_3_next_chunk",
                  "default_next_chunk", "kind", "chunk_id"):
            if (c.get(k) or "") != (old.get(k) or "") and k not in (
                "option_1_label", "option_2_label", "option_3_label"
            ):
                if k.startswith("option_") and "label" in k:
                    continue
                if (c.get(k) or "") != (old.get(k) or ""):
                    # graph/kind/id must match; labels we set equal below
                    if k in ("kind", "chunk_id") or "next" in k:
                        if (c.get(k) or "") != (old.get(k) or ""):
                            raise SystemExit(f"{c['chunk_id']} {k} cassé")
        for k in ("option_1_label", "option_2_label", "option_3_label"):
            if (c.get(k) or "") != (old.get(k) or ""):
                raise SystemExit(f"label changé {c['chunk_id']} {k}: {c.get(k)!r} != {old.get(k)!r}")

    counts = [path_words(by, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    lo, hi, avg = min(counts), max(counts), sum(counts) // len(counts)
    if lo < 520 or hi > 780:
        raise SystemExit(f"{SID} chemins {lo}-{hi} (moy {avg}) hors 520-780")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    vecu = (
        "Village au bord des champs, haie des ailes. Victorino veut que le papillon "
        "jaune se pose sur la fleur de papier. Aniss veut le prendre maintenant. "
        "Indice unique : un grain de lavande, dès la pince à linge, payé à chaque "
        "climax et chaque fin. T1 = filet vert / chapeau bleu / fleur de papier "
        "(les trois partent). T2 = pré (course, herbe) / lavandes (parfum, tiges) / "
        "muret (clic, pierre). Première idée rate. T3 = neuf façons de doser l'élan. "
        "Ils refusent de foncer. Le silence d'Aniss répond. Leçon DIF.ENE.001 vécue "
        "(attendre / ne pas tout brûler d'un coup), jamais dite. 27 fins distinctes."
    )
    notes = (
        f"F-NAR-019 example4 v2. N3 ≤ 16. Ouverture inventée (pince à linge, aile qui "
        f"copie le clic), pas les 5 gabarits, pas « encore ». Tics encore/déjà/tout doux/"
        f"tout calme, merle, miel, Mission accomplie, J'ai compris jetés. "
        f"Monde ≠ TREE-DIF-039 (balle, portail), ≠ TREE-DIF-063 (ticket, quai). "
        f"TTS notes+ssml+xai+piper par chunk (profiles example2). "
        f"Un merci de papa (montrer le grain). Question d'adulte. Un « en ce moment ». "
        f"Chemins {lo}–{hi} mots (moyenne {avg}). 86 chunks. Pas apply. Audio non cuit."
    )
    path = ROOT / SID / "RELECTURE.md"
    path.write_text(
        f"# {SID} — {TITLE}\n\n"
        f"- **Public :** N3 (5–6 ans), audio familial\n"
        f"- **Leçon :** DIF.ENE.001 — attendre / ne pas tout brûler d'un coup (vécue, jamais dite)\n"
        f"- **Personnages :** {CHARS}\n"
        f"- **Lieu :** {SETTING}\n"
        f"- **Structure conservée :** 86 nœuds, graphe, labels, 27 chemins, 27 fins distinctes\n\n"
        f"Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        f"`chunk_id` / `kind` / graphe `option_*_next` inchangés. Labels T1/T2/T3 gardés.\n\n"
        f"## Promesse narrative\n\n"
        f"La pince à linge cliquette. Une aile jaune copie le clic, puis part. "
        f"Un **grain de lavande** tient au bois. Mission : que le papillon jaune se pose "
        f"sur la fleur de papier, à la haie des ailes, avant que le vent l'emporte. "
        f"Aniss veut courir maintenant ; Victorino veut attendre. Ils emportent le filet, "
        f"le chapeau et la fleur. Au pré l'herbe s'envole, aux lavandes le parfum saute, "
        f"au muret les pierres cliquent. Une 2e ruse : ils refusent de foncer, retrouvent "
        f"le grain du début. Neuf façons de doser. Le jaune se pose. Il a failli partir.\n\n"
        f"## Vécu\n{vecu}\n\n"
        f"## Vu et corrigé\n{notes}\n\n"
        f"## Direction vocale\n\n"
        f"`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, "
        f"tempo, sourire, respiration. `slow` = choix, indice, fin. Obstacle en "
        f"`low-pitch`. Fins `soft` / `slow` / `low-pitch`.\n\n"
        f"## Contrôles\n\n"
        f"- 86 chunks, 27 chemins, 27 fins distinctes, 27 dernières images\n"
        f"- {lo} à {hi} mots par chemin (moyenne {avg})\n"
        f"- `text` = `script` collé ; graphe et labels inchangés\n"
        f"- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes`\n\n"
        f"## Non vérifié\n"
        f"Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )
    print(f"OK {SID} chemins {lo}-{hi} moy {avg}")


def main() -> None:
    write_tree()


if __name__ == "__main__":
    main()
