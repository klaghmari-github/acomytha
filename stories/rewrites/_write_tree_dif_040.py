#!/usr/bin/env python3
"""TREE-DIF-040 — Le lait de Nino et le petit veau (N3, DIF.BES.001, F-NAR-019 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-040"
LIM = LIMITS["N3"]
TITLE = "Le lait de Nino et le petit veau"
FIL = (
    "Au hangar au lait, Nino veut porter le seau tiède au petit veau "
    "avant que le lait refroidisse. Un grain de son tient sous l'anse. "
    "Il prend d'abord le seau, la brosse ou le torchon ; les trois partent. "
    "À l'étable le fer claque, au pré le vent penche, à l'abreuvoir l'eau saute. "
    "Il fonce, le veau recule. Il refuse de foncer. Le grain de son paie le début. "
    "Neuf façons de laisser du temps. Le veau boit."
)
CHARS = "Nino, papa, maman"
SETTING = "ferme du village : étable, pré, abreuvoir"

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=500, sentence=260, energy="warm", contour="storytelling",
        noise=0.36, emphasis="grain de son",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le lait fume, le veau attend, Nino veut foncer; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=900, sentence=330, energy="focused", contour="rising",
        noise=0.33, emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change la suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2,
        pause=700, sentence=320, energy="focused", contour="rising",
        noise=0.32, emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=450, sentence=280, energy="bright", contour="falling",
        noise=0.34, emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=420, sentence=250, energy="lively", contour="dynamic",
        noise=0.37, emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=il_prend_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0,
        pause=520, sentence=300, energy="tense", contour="dynamic",
        noise=0.34, emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=le_veau_recule_si_on_fonce; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=560, sentence=270, energy="bright", contour="falling",
        noise=0.35, emphasis="grain de son",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=le_grain_de_son_paie_le_début; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3,
        pause=900, sentence=340, energy="calm", contour="falling",
        noise=0.31, emphasis="grain de son",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_veau_a_bu_le_grain_reste; tempo=posé; sourire=léger; respiration=ample",
    ),
}

TICS_PHRASE = (
    "tout doux",
    "tout calme",
    "on va apprendre",
    "voici le geste",
    "l'histoire est finie",
    "mission accomplie",
    "j'ai compris",
    "aujourd'hui,",
    "bon travail",
    "bravo tu as",
    "la première",
    "la deuxième",
    "la troisième",
    "il faut attendre",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)
BAN = (
    "merle",
    "miel",
    "jardinier",
    "grand-père",
    "grand pere",
    "maîtresse",
    "maitresse",
    "seau vert",
    "croissant",
    "bâche",
    "bache",
    "marché",
    "marche ",
    "chambre",
    "bac à sable",
    "toboggan",
    "balançoire",
    "capitaine",
    "plic",
    "volet jaune",
    "plus de temps ou de calme",
    "sami",
    "léa",
    "tom ",
    "zoé",
    "lina",
    "iris",
)


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
        for tic in TICS_PHRASE:
            if tic in low:
                raise SystemExit(f"tic « {tic} »: {ph}")
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"tic {m.group(0)!r}: {ph}")
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


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emph = m.get("emphasis")
    if emph:
        e = esc(emph)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict) -> str:
    body = text
    emph = m.get("emphasis")
    if emph:
        body = body.replace(emph, f"<emphasis>{emph}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitch_tag"):
        body = f"<{m['pitch_tag']}>{body}</{m['pitch_tag']}>"
    tail = " [long-pause]" if m["pause"] >= 800 else (" [pause]" if m["pause"] >= 400 else "")
    return (body + tail).strip()


def voice(text: str, profile: str, extra: dict | None = None) -> dict:
    m = dict(PROFILES[profile])
    extra = extra or {}
    if extra.get("emphasis") is not None:
        m["emphasis"] = extra["emphasis"]
    if extra.get("note"):
        m["note"] = extra["note"]
    pause_before = extra.get("pause_before", 0)
    return {
        "text_ssml": ssml(text, m),
        "text_xai_tags": xai(text, m),
        "rate_wpm": m["wpm"],
        "rate_label": m["rate"],
        "speed_xai": m["speed"],
        "length_scale_piper": m["piper"],
        "pitch_label": m["pitch"],
        "pitch_ssml": m["pitch_ssml"],
        "pitch_xai_tag": m["pitch_tag"],
        "volume_label": m["volume"],
        "volume_db": m["db"],
        "emphasis_words": m["emphasis"] or "",
        "pause_before_ms": pause_before,
        "pause_after_ms": m["pause"],
        "pause_sentence_ms": m["sentence"],
        "style_energy": m["energy"],
        "style_contour": m["contour"],
        "noise_scale_piper": m["noise"],
        "kokoro_speed": m["speed"],
        "melo_speed": m["speed"],
        "espeak_amp": 82 if m["volume"] == "soft" else 100,
        "espeak_pitch": 42 if m["pitch"] == "low" else 50,
        "espeak_word_gap": 12 if m["rate"] == "slow" else 8,
        "notes": m["note"],
        "night_policy": "play",
        "locale": "fr-FR",
        "voice_id": "fr_FR-siwis-medium",
    }


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


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


T1 = {
    1: {
        "lab": "le seau",
        "ans": "seau",
        "acc": "seau | le seau | d'abord le seau | le lait",
        "retry": "Nino prend le seau d'abord.",
        "emph": "seau",
        "sons": "zinc,lait",
    },
    2: {
        "lab": "la brosse",
        "ans": "brosse",
        "acc": "brosse | la brosse | d'abord la brosse | les poils",
        "retry": "Nino prend la brosse d'abord.",
        "emph": "brosse",
        "sons": "poils,paille",
    },
    3: {
        "lab": "le torchon",
        "ans": "torchon",
        "acc": "torchon | le torchon | d'abord le torchon | le linge",
        "retry": "Nino prend le torchon d'abord.",
        "emph": "torchon",
        "sons": "linge,savon",
    },
}

T3_LABS = {
    1: ("attendre à la porte", "la paille", "tout bas"),
    2: ("la barrière", "poser le seau", "dans l'herbe"),
    3: ("l'eau se tait", "essuyer", "au bord"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Nino saisit le seau, trop plein, trop chaud.",
            "enfant-m|Le lait va au veau.",
            "maman|Tiens-le droit, Nino.",
            "narrateur|Une goutte saute sur sa botte.",
            "narrateur|Ses joues chauffent, et il serre trop.",
            "enfant-m|Vite, avant qu'il parte !",
            "narrateur|Le grain de son tient sous l'anse.",
            "papa|La brosse aussi, près du sac.",
            "narrateur|Maman glisse le torchon contre le zinc.",
            "narrateur|Seau, brosse et torchon avancent avec lui.",
            "enfant-m|J'arrive, petit veau.",
            "narrateur|Le zinc sent le lait, tiède.",
            "papa|Le seau d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Nino saisit la brosse, les poils rèches.",
            "enfant-m|Je le brosserai, après le lait.",
            "papa|Pas trop vite, Nino.",
            "narrateur|Il secoue les poils, et un brin s'envole.",
            "enfant-m|Oh, trop fort.",
            "maman|Le seau, ensuite, près de toi.",
            "narrateur|Papa pose le torchon contre les bottes.",
            "narrateur|Il emporte les trois, contre lui.",
            "enfant-m|Tes poils, petit veau.",
            "narrateur|La brosse frotte sa manche, rêche.",
            "narrateur|Sous l'anse du seau, le grain de son tient.",
            "maman|La brosse d'abord, elle est prête.",
        )
    return L(
        "narrateur|Nino saisit le torchon, un peu humide.",
        "enfant-m|Pour son mufle, après.",
        "maman|Plie-le, tout petit.",
        "narrateur|Le linge sent le lait et le savon.",
        "narrateur|Un coin claque, comme un drap trop vif.",
        "enfant-m|Reste avec moi.",
        "papa|Le seau et la brosse, avec vous.",
        "narrateur|Il les pose près des bottes, puis les prend.",
        "narrateur|Rien ne reste près du hangar.",
        "enfant-m|Je t'essuierai, petit veau.",
        "narrateur|Sous l'anse, le grain de son tient, sec.",
        "papa|Le torchon d'abord, il est prêt.",
    )


def t1_q(t1: int) -> list[str]:
    o = T1[t1]
    return L(
        f"narrateur|Nino a pris {o['lab']} d'abord.",
        "maman|Il a pris quoi, d'abord ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Le seau.",
            "papa|Oui, le zinc tiède.",
            "narrateur|La brosse et le torchon partent avec.",
            "maman|La ferme vous attend.",
            "papa|On avance par où ?",
            "enfant-m|Oui, papa.",
            "narrateur|Une goutte tremble au bord, puis se tait.",
            "narrateur|Le grain de son reste sous l'anse.",
        )
    if t1 == 2:
        return L(
            "enfant-m|La brosse.",
            "maman|Oui, les poils rèches.",
            "narrateur|Le seau penche sous le bras.",
            "narrateur|Le torchon dort contre sa poche.",
            "papa|Les poils sentent le foin.",
            "maman|Vos pieds, dans les bottes ?",
            "enfant-m|Oui, maman.",
            "narrateur|Un brin de paille tombe, puis plus.",
        )
    return L(
        "enfant-m|Le torchon.",
        "papa|Oui, le linge du savon.",
        "narrateur|Le seau et la brosse pèsent contre lui.",
        "maman|Le linge sent le lait, tiède.",
        "papa|On y va, tous les trois ?",
        "enfant-m|Oui.",
        "narrateur|Un coin du torchon dépasse, chaud.",
        "narrateur|Le grain de son tient, sous l'anse.",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "Le seau cliquette à chaque pas, bas.",
        2: "La brosse frotte sa manche, un peu rêche.",
        3: "Le torchon tape le poignet, léger.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|L'étable reste sombre, trop bruyante.",
        "narrateur|Plus loin, le pré souffle, trop fort.",
        "narrateur|Près de la pierre, l'eau claque.",
        "papa|Nino, vous partez où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    table = {
        (1, 1): L(
            "narrateur|Contre sa jambe, le zinc du seau cliquette.",
            "narrateur|L'étable sent le foin, trop sombre.",
            "enfant-m|Petit veau, j'ai du lait !",
            "narrateur|Nino pousse le seuil, trop vite.",
            "narrateur|Le zinc tape une barre, trop fort.",
            "narrateur|Le veau recule, le mufle contre sa mère.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "papa|Tu vois ses oreilles, Nino ?",
            "enfant-m|Elles sont hautes, il a peur.",
            "maman|On n'entre pas comme ça.",
            "narrateur|Nino veut foncer, puis il s'arrête.",
            "enfant-m|Non, pas trop vite.",
            "narrateur|Une chaîne cliquette, plus loin, rusée.",
            "narrateur|Le veau recule d'un pas, de nouveau.",
            "papa|Tu trouves, Nino ?",
        ),
        (2, 1): L(
            "narrateur|Dans sa paume, les poils de la brosse piquent.",
            "narrateur|L'étable sent le foin, trop sombre.",
            "enfant-m|Je te brosse, après le lait !",
            "narrateur|Nino agite la brosse, trop vite.",
            "narrateur|Les poils frôlent le fer, un bruit trop sec.",
            "narrateur|Le veau recule, le mufle contre sa mère.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "maman|Tu vois ses oreilles, Nino ?",
            "enfant-m|Elles sont hautes.",
            "papa|Ça claque trop, ici.",
            "narrateur|Nino lève la brosse, puis la baisse.",
            "enfant-m|Non, je ne fonce pas.",
            "narrateur|Un gond grince, rusé, trop fort.",
            "narrateur|Le veau recule d'un pas, de nouveau.",
            "papa|Tu trouves, Nino ?",
        ),
        (3, 1): L(
            "narrateur|Au poignet, le torchon humide colle un peu.",
            "narrateur|L'étable sent le foin, trop sombre.",
            "enfant-m|J'essuie ton mufle, petit veau !",
            "narrateur|Nino agite le linge, trop vite.",
            "narrateur|Le torchon accroche un clou, puis lâche.",
            "narrateur|Le veau recule, le mufle contre sa mère.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "papa|Tu vois ses oreilles, Nino ?",
            "enfant-m|Elles sont hautes, il a peur.",
            "maman|Le linge a claqué, trop fort.",
            "narrateur|Nino serre le torchon, puis il s'arrête.",
            "enfant-m|Non, pas trop vite.",
            "narrateur|Le clou sonne, rusé, une fois.",
            "narrateur|Le veau recule d'un pas, de nouveau.",
            "maman|Tu trouves, Nino ?",
        ),
        (1, 2): L(
            "narrateur|Contre sa jambe, le zinc du seau cliquette.",
            "narrateur|Le pré sent l'herbe coupée, chaude.",
            "enfant-m|Le veau est trop loin !",
            "narrateur|Nino court, et le vent penche le seau.",
            "narrateur|Le lait tremble, une goutte tombe.",
            "narrateur|Le veau lève la tête, puis recule.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Maman s'accroupit, dans l'herbe haute.",
            "maman|Tu vois comme il recule, Nino ?",
            "enfant-m|Oui, il n'aime pas le vent.",
            "papa|Le vent n'a pas fini.",
            "narrateur|Nino veut courir, puis il s'arrête.",
            "enfant-m|Non, je ne fonce pas.",
            "narrateur|Une mouche tourne, rusée, trop près.",
            "narrateur|Le veau recule d'un pas, de nouveau.",
            "papa|Tu trouves, Nino ?",
        ),
        (2, 2): L(
            "narrateur|Dans sa paume, les poils de la brosse piquent.",
            "narrateur|Le pré sent l'herbe coupée, chaude.",
            "enfant-m|Le veau est trop loin !",
            "narrateur|Nino agite la brosse, et des poils s'envolent.",
            "narrateur|Le vent les emporte, trop légers.",
            "narrateur|Le veau lève la tête, puis recule.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Papa s'accroupit, dans l'herbe haute.",
            "papa|Tu vois comme il recule, Nino ?",
            "enfant-m|Oui, les poils l'ont fait peur.",
            "maman|Le vent n'a pas fini.",
            "narrateur|Nino baisse la brosse, puis il s'arrête.",
            "enfant-m|Non, je ne fonce pas.",
            "narrateur|Une mouche tourne, rusée, trop près.",
            "narrateur|Le veau recule d'un pas, de nouveau.",
            "maman|Tu trouves, Nino ?",
        ),
        (3, 2): L(
            "narrateur|Au poignet, le torchon humide colle un peu.",
            "narrateur|Le pré sent l'herbe coupée, chaude.",
            "enfant-m|Le veau est trop loin !",
            "narrateur|Nino court, et le torchon claque comme un drap.",
            "narrateur|Le vent le gonfle, trop fort.",
            "narrateur|Le veau lève la tête, puis recule.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Maman s'accroupit, dans l'herbe haute.",
            "maman|Tu vois comme il recule, Nino ?",
            "enfant-m|Oui, le linge a trop bougé.",
            "papa|Le vent n'a pas fini.",
            "narrateur|Nino serre le torchon, puis il s'arrête.",
            "enfant-m|Non, je ne fonce pas.",
            "narrateur|Une mouche tourne, rusée, trop près.",
            "narrateur|Le veau recule d'un pas, de nouveau.",
            "papa|Tu trouves, Nino ?",
        ),
        (1, 3): L(
            "narrateur|Contre sa jambe, le zinc du seau cliquette.",
            "narrateur|L'abreuvoir claque, trop plein, trop vif.",
            "enfant-m|L'eau fait trop de bruit.",
            "narrateur|Nino s'approche, trop près, trop vite.",
            "narrateur|Une goutte du seau tombe, trop bruyante.",
            "narrateur|Le veau recule d'un pas, les oreilles hautes.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Papa s'accroupit, au bord de la pierre.",
            "papa|Tu vois la flaque, Nino ?",
            "enfant-m|Elle est large, et froide.",
            "maman|Ça éclabousse trop, ici.",
            "narrateur|Nino veut avancer, puis il s'arrête.",
            "enfant-m|Non, je ne fonce pas.",
            "narrateur|Une goutte plus loin saute, rusée.",
            "narrateur|Le veau recule d'un pas, de nouveau.",
            "papa|Tu trouves, Nino ?",
        ),
        (2, 3): L(
            "narrateur|Dans sa paume, les poils de la brosse piquent.",
            "narrateur|L'abreuvoir claque, trop plein, trop vif.",
            "enfant-m|L'eau fait trop de bruit.",
            "narrateur|Nino pose la brosse, trop vite, trop près.",
            "narrateur|La brosse glisse sur la pierre, trop rêche.",
            "narrateur|Le veau recule d'un pas, les oreilles hautes.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Maman s'accroupit, au bord de la pierre.",
            "maman|Tu vois la flaque, Nino ?",
            "enfant-m|Elle est large, et froide.",
            "papa|Ça éclabousse trop, ici.",
            "narrateur|Nino ramasse la brosse, puis il s'arrête.",
            "enfant-m|Non, je ne fonce pas.",
            "narrateur|Une goutte plus loin saute, rusée.",
            "narrateur|Le veau recule d'un pas, de nouveau.",
            "maman|Tu trouves, Nino ?",
        ),
        (3, 3): L(
            "narrateur|Au poignet, le torchon humide colle un peu.",
            "narrateur|L'abreuvoir claque, trop plein, trop vif.",
            "enfant-m|L'eau fait trop de bruit.",
            "narrateur|Nino plonge le linge, trop vite.",
            "narrateur|Le torchon s'alourdit, trop mouillé.",
            "narrateur|Le veau recule d'un pas, les oreilles hautes.",
            "narrateur|Le sourire de Nino disparaît.",
            "narrateur|Dans sa poitrine, ça se bouscule.",
            "narrateur|Papa s'accroupit, au bord de la pierre.",
            "papa|Tu vois la flaque, Nino ?",
            "enfant-m|Elle est large, et le linge a trop bu.",
            "maman|Ça éclabousse trop, ici.",
            "narrateur|Nino lève le torchon, puis il s'arrête.",
            "enfant-m|Non, je ne fonce pas.",
            "narrateur|Une goutte plus loin saute, rusée.",
            "narrateur|Le veau recule d'un pas, de nouveau.",
            "papa|Tu trouves, Nino ?",
        ),
    }
    return table[(t1, t2)]


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|L'étable claque, trop sombre.",
            "papa|Attendre à la porte, la paille, ou tout bas ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le pré souffle, trop fort.",
            "maman|La barrière, poser le seau, ou dans l'herbe ?",
        )
    return L(
        "narrateur|L'eau claque, trop vive.",
        "papa|L'eau se tait, essuyer, ou au bord ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    table = {
        (1, 1, 1): L(
            "enfant-m|On attend à la porte.",
            "narrateur|Il pose le seau près du seuil, sans entrer.",
            "narrateur|Nino regarde sous l'anse, le grain de son.",
            "narrateur|Le fer se tait, une fois, puis plus.",
            "narrateur|Le veau sort deux oreilles, lentes.",
            "enfant-m|Tu peux venir.",
            "papa|Le fer s'est tu, maintenant.",
            "maman|Tu lui as laissé le temps.",
            "narrateur|Le lait ne tremble plus, dans le zinc.",
            "narrateur|Ça a failli ne pas arriver.",
        ),
        (2, 1, 1): L(
            "enfant-m|On attend à la porte.",
            "narrateur|Il pose la brosse près du seuil, sans entrer.",
            "narrateur|Nino regarde sous l'anse, le grain de son.",
            "narrateur|Les poils ne frôlent plus le fer.",
            "narrateur|Le veau sort deux oreilles, lentes.",
            "enfant-m|Tu peux venir.",
            "papa|Le fer s'est tu, maintenant.",
            "maman|Tu lui as laissé le temps.",
            "narrateur|La brosse reste sage, contre sa jambe.",
            "narrateur|Ça a failli ne pas arriver.",
        ),
        (3, 1, 1): L(
            "enfant-m|On attend à la porte.",
            "narrateur|Il pose le torchon près du seuil, sans entrer.",
            "narrateur|Nino regarde sous l'anse, le grain de son.",
            "narrateur|Le linge ne claque plus contre le clou.",
            "narrateur|Le veau sort deux oreilles, lentes.",
            "enfant-m|Tu peux venir.",
            "papa|Le fer s'est tu, maintenant.",
            "maman|Tu lui as laissé le temps.",
            "narrateur|Le torchon pend, sans vent.",
            "narrateur|Ça a failli ne pas arriver.",
        ),
        (1, 1, 2): L(
            "enfant-m|Dans la paille, on s'assoit.",
            "narrateur|Il glisse le seau dans la paille, bas.",
            "narrateur|Nino s'assoit, les genoux dans le foin.",
            "narrateur|Sous l'anse, le grain de son reste visible.",
            "narrateur|Le veau avance d'un pas, puis d'un autre.",
            "enfant-m|Viens, je suis petit, comme toi.",
            "papa|Tu as regardé d'abord.",
            "maman|La paille a fait le calme.",
            "narrateur|Le lait fume, tout seul, près du foin.",
            "narrateur|Personne n'a dit la réponse, et il a vu.",
        ),
        (2, 1, 2): L(
            "enfant-m|Dans la paille, on s'assoit.",
            "narrateur|Il pose la brosse dans la paille, bas.",
            "narrateur|Nino s'assoit, les genoux dans le foin.",
            "narrateur|Sous l'anse, le grain de son reste visible.",
            "narrateur|Le veau avance d'un pas, puis d'un autre.",
            "enfant-m|Viens, les poils n'ont plus bougé.",
            "papa|Tu as regardé d'abord.",
            "maman|La paille a fait le calme.",
            "narrateur|Un brin reste coincé dans les poils.",
            "narrateur|Personne n'a dit la réponse, et il a vu.",
        ),
        (3, 1, 2): L(
            "enfant-m|Dans la paille, on s'assoit.",
            "narrateur|Il étale le torchon dans la paille, bas.",
            "narrateur|Nino s'assoit, les genoux dans le foin.",
            "narrateur|Sous l'anse, le grain de son reste visible.",
            "narrateur|Le veau avance d'un pas, puis d'un autre.",
            "enfant-m|Viens, le linge est couché.",
            "papa|Tu as regardé d'abord.",
            "maman|La paille a fait le calme.",
            "narrateur|Le torchon sent le foin, tiède.",
            "narrateur|Personne n'a dit la réponse, et il a vu.",
        ),
        (1, 1, 3): L(
            "enfant-m|Tout bas, c'est moi.",
            "narrateur|Il parle au seau, bas, puis au veau.",
            "narrateur|Nino répète, plus bas que le fer.",
            "narrateur|Sous l'anse, le grain de son ne bouge pas.",
            "narrateur|Le veau dresse les oreilles, sans reculer.",
            "enfant-m|Tu m'entends, maintenant.",
            "papa|Ta voix n'a pas claqué.",
            "maman|Tu as parlé lentement.",
            "narrateur|Le lait écoute, dans le zinc.",
            "narrateur|Sa gorge a failli crier, et il n'a pas crié.",
        ),
        (2, 1, 3): L(
            "enfant-m|Tout bas, c'est moi.",
            "narrateur|Il parle à la brosse, bas, puis au veau.",
            "narrateur|Nino répète, plus bas que le fer.",
            "narrateur|Sous l'anse, le grain de son ne bouge pas.",
            "narrateur|Le veau dresse les oreilles, sans reculer.",
            "enfant-m|Tu m'entends, maintenant.",
            "papa|Ta voix n'a pas claqué.",
            "maman|Tu as parlé lentement.",
            "narrateur|Les poils restent sages, contre sa manche.",
            "narrateur|Sa gorge a failli crier, et il n'a pas crié.",
        ),
        (3, 1, 3): L(
            "enfant-m|Tout bas, c'est moi.",
            "narrateur|Il parle au torchon, bas, puis au veau.",
            "narrateur|Nino répète, plus bas que le fer.",
            "narrateur|Sous l'anse, le grain de son ne bouge pas.",
            "narrateur|Le veau dresse les oreilles, sans reculer.",
            "enfant-m|Tu m'entends, maintenant.",
            "papa|Ta voix n'a pas claqué.",
            "maman|Tu as parlé lentement.",
            "narrateur|Le linge reste plié, contre son poignet.",
            "narrateur|Sa gorge a failli crier, et il n'a pas crié.",
        ),
        (1, 2, 1): L(
            "enfant-m|Derrière la barrière, d'abord.",
            "narrateur|Nino s'arrête au bois, sans courir.",
            "narrateur|Derrière le bois, le seau attend, droit.",
            "narrateur|Sous l'anse, le grain de son tient, sec.",
            "narrateur|Le vent passe, puis s'apaise un peu.",
            "enfant-m|Maintenant, tu me vois.",
            "maman|Le pré retombe, comme un mur calme.",
            "papa|Tu as attendu le silence.",
            "narrateur|Le lait ne penche plus.",
            "narrateur|Le veau s'approche du bois, lent.",
        ),
        (2, 2, 1): L(
            "enfant-m|Derrière la barrière, d'abord.",
            "narrateur|Nino s'arrête au bois, sans courir.",
            "narrateur|Derrière le bois, la brosse reste contre lui.",
            "narrateur|Sous l'anse, le grain de son tient, sec.",
            "narrateur|Le vent passe, puis s'apaise un peu.",
            "enfant-m|Maintenant, tu me vois.",
            "maman|Le pré retombe, comme un mur calme.",
            "papa|Tu as attendu le silence.",
            "narrateur|Les poils ne s'envolent plus.",
            "narrateur|Le veau s'approche du bois, lent.",
        ),
        (3, 2, 1): L(
            "enfant-m|Derrière la barrière, d'abord.",
            "narrateur|Nino s'arrête au bois, sans courir.",
            "narrateur|Derrière le bois, le torchon ne claque plus.",
            "narrateur|Sous l'anse, le grain de son tient, sec.",
            "narrateur|Le vent passe, puis s'apaise un peu.",
            "enfant-m|Maintenant, tu me vois.",
            "maman|Le pré retombe, comme un mur calme.",
            "papa|Tu as attendu le silence.",
            "narrateur|Le linge reste plié, sans drap.",
            "narrateur|Le veau s'approche du bois, lent.",
        ),
        (1, 2, 2): L(
            "enfant-m|Je pose le seau, d'abord.",
            "narrateur|Il pose le seau dans l'herbe, droit.",
            "narrateur|Nino recule d'un pas, les mains vides.",
            "narrateur|Sous l'anse, le grain de son reste au soleil.",
            "narrateur|Le lait fume, tout seul, dans l'herbe.",
            "narrateur|Le veau avance le mufle, lent.",
            "papa|Tu n'as pas couru vers lui.",
            "enfant-m|C'est pour toi.",
            "maman|Tu as laissé le seau parler.",
            "narrateur|Personne n'a poussé, et le veau a choisi.",
        ),
        (2, 2, 2): L(
            "enfant-m|Je pose le seau, d'abord.",
            "narrateur|Il pose la brosse, puis le seau, droit.",
            "narrateur|Nino recule d'un pas, les mains vides.",
            "narrateur|Sous l'anse, le grain de son reste au soleil.",
            "narrateur|Le lait fume, tout seul, dans l'herbe.",
            "narrateur|Le veau avance le mufle, lent.",
            "papa|Tu n'as pas couru vers lui.",
            "enfant-m|C'est pour toi.",
            "maman|Tu as laissé le seau parler.",
            "narrateur|Les poils attendent, à côté, sages.",
        ),
        (3, 2, 2): L(
            "enfant-m|Je pose le seau, d'abord.",
            "narrateur|Il pose le torchon sous le seau, droit.",
            "narrateur|Nino recule d'un pas, les mains vides.",
            "narrateur|Sous l'anse, le grain de son reste au soleil.",
            "narrateur|Le lait fume, tout seul, dans l'herbe.",
            "narrateur|Le veau avance le mufle, lent.",
            "papa|Tu n'as pas couru vers lui.",
            "enfant-m|C'est pour toi.",
            "maman|Tu as laissé le seau parler.",
            "narrateur|Le linge tient le zinc, sans claquer.",
        ),
        (1, 2, 3): L(
            "enfant-m|Dans l'herbe, tout petit.",
            "narrateur|Nino s'accroupit, les mains dans l'herbe.",
            "narrateur|Dans l'herbe, le seau reste bas, près de lui.",
            "narrateur|Sous l'anse, le grain de son est à sa hauteur.",
            "narrateur|Le veau le voit plus bas, moins grand.",
            "enfant-m|Viens, je t'attends.",
            "papa|Tu t'es fait petit, comme lui.",
            "maman|Tu as observé d'abord.",
            "narrateur|Le vent passe au-dessus, trop haut.",
            "narrateur|Le veau s'accroupit un peu, lui aussi.",
        ),
        (2, 2, 3): L(
            "enfant-m|Dans l'herbe, tout petit.",
            "narrateur|Nino s'accroupit, les mains dans l'herbe.",
            "narrateur|Dans l'herbe, la brosse reste contre son genou.",
            "narrateur|Sous l'anse, le grain de son est à sa hauteur.",
            "narrateur|Le veau le voit plus bas, moins grand.",
            "enfant-m|Viens, je t'attends.",
            "papa|Tu t'es fait petit, comme lui.",
            "maman|Tu as observé d'abord.",
            "narrateur|Les poils ne s'envolent plus, si bas.",
            "narrateur|Le veau s'accroupit un peu, lui aussi.",
        ),
        (3, 2, 3): L(
            "enfant-m|Dans l'herbe, tout petit.",
            "narrateur|Nino s'accroupit, les mains dans l'herbe.",
            "narrateur|Dans l'herbe, le torchon ne vole plus.",
            "narrateur|Sous l'anse, le grain de son est à sa hauteur.",
            "narrateur|Le veau le voit plus bas, moins grand.",
            "enfant-m|Viens, je t'attends.",
            "papa|Tu t'es fait petit, comme lui.",
            "maman|Tu as observé d'abord.",
            "narrateur|Le linge pèse, couché, sans drap.",
            "narrateur|Le veau s'accroupit un peu, lui aussi.",
        ),
        (1, 3, 1): L(
            "enfant-m|On attend que l'eau se taise.",
            "narrateur|Il tient le seau, sans verser, jusqu'au silence.",
            "narrateur|Nino regarde sous l'anse, le grain de son.",
            "narrateur|Les gouttes se calment, une, puis une autre.",
            "narrateur|Le veau baisse les oreilles, lentes.",
            "enfant-m|Maintenant, tu peux boire.",
            "papa|L'eau n'éclabousse plus.",
            "maman|Tu as attendu le calme.",
            "narrateur|Le zinc ne tremble plus.",
            "narrateur|L'eau a failli tout gâcher, puis elle s'est tue.",
        ),
        (2, 3, 1): L(
            "enfant-m|On attend que l'eau se taise.",
            "narrateur|Il tient la brosse, sans bouger, jusqu'au silence.",
            "narrateur|Nino regarde sous l'anse, le grain de son.",
            "narrateur|Les gouttes se calment, une, puis une autre.",
            "narrateur|Le veau baisse les oreilles, lentes.",
            "enfant-m|Maintenant, tu peux boire.",
            "papa|L'eau n'éclabousse plus.",
            "maman|Tu as attendu le calme.",
            "narrateur|Les poils restent secs, loin de l'eau.",
            "narrateur|L'eau a failli tout gâcher, puis elle s'est tue.",
        ),
        (3, 3, 1): L(
            "enfant-m|On attend que l'eau se taise.",
            "narrateur|Il tient le torchon, sans essuyer, jusqu'au silence.",
            "narrateur|Nino regarde sous l'anse, le grain de son.",
            "narrateur|Les gouttes se calment, une, puis une autre.",
            "narrateur|Le veau baisse les oreilles, lentes.",
            "enfant-m|Maintenant, tu peux boire.",
            "papa|L'eau n'éclabousse plus.",
            "maman|Tu as attendu le calme.",
            "narrateur|Le linge reste plié, sans boire.",
            "narrateur|L'eau a failli tout gâcher, puis elle s'est tue.",
        ),
        (1, 3, 2): L(
            "enfant-m|J'essuie, d'abord.",
            "narrateur|Il pose le seau, puis pousse l'eau du pied.",
            "narrateur|Sous l'anse, le grain de son reste sec.",
            "narrateur|La pierre redevient mate, moins froide.",
            "narrateur|Le veau pose un sabot, puis l'autre.",
            "enfant-m|C'est sec, viens.",
            "papa|La flaque n'a plus claqué.",
            "maman|Tu as préparé le chemin.",
            "narrateur|Le lait attend, droit, sur la pierre.",
            "narrateur|Sans la flaque, le veau a osé.",
        ),
        (2, 3, 2): L(
            "enfant-m|J'essuie, d'abord.",
            "narrateur|Les poils de la brosse chassent un peu d'eau.",
            "narrateur|Sous l'anse, le grain de son reste sec.",
            "narrateur|La pierre redevient mate, moins froide.",
            "narrateur|Le veau pose un sabot, puis l'autre.",
            "enfant-m|C'est sec, viens.",
            "papa|La flaque n'a plus claqué.",
            "maman|Tu as préparé le chemin.",
            "narrateur|Les poils sont un peu mouillés, utiles.",
            "narrateur|Sans la flaque, le veau a osé.",
        ),
        (3, 3, 2): L(
            "enfant-m|J'essuie, d'abord.",
            "narrateur|Le torchon boit la flaque, tout large.",
            "narrateur|Sous l'anse, le grain de son reste sec.",
            "narrateur|La pierre redevient mate, moins froide.",
            "narrateur|Le veau pose un sabot, puis l'autre.",
            "enfant-m|C'est sec, viens.",
            "papa|La flaque n'a plus claqué.",
            "maman|Tu as préparé le chemin.",
            "narrateur|Le linge pèse, lourd, utile.",
            "narrateur|Sans la flaque, le veau a osé.",
        ),
        (1, 3, 3): L(
            "enfant-m|Au bord, pas trop près.",
            "narrateur|Au bord, le seau reste droit, loin de l'eau.",
            "narrateur|Nino s'arrête sur la pierre sèche.",
            "narrateur|Sous l'anse, le grain de son reste sec.",
            "narrateur|Le veau s'approche du lait, pas de l'eau.",
            "enfant-m|Bois, ici.",
            "papa|Tu n'as pas penché.",
            "maman|Le bord était assez large.",
            "narrateur|L'eau claque plus loin, sans eux.",
            "narrateur|Le veau a choisi le zinc, pas la flaque.",
        ),
        (2, 3, 3): L(
            "enfant-m|Au bord, pas trop près.",
            "narrateur|Au bord, la brosse reste sèche, loin de l'eau.",
            "narrateur|Nino s'arrête sur la pierre sèche.",
            "narrateur|Sous l'anse, le grain de son reste sec.",
            "narrateur|Le veau s'approche du lait, pas de l'eau.",
            "enfant-m|Bois, ici.",
            "papa|Tu n'as pas penché.",
            "maman|Le bord était assez large.",
            "narrateur|Les poils restent secs, loin de la flaque.",
            "narrateur|Le veau a choisi le zinc, pas la flaque.",
        ),
        (3, 3, 3): L(
            "enfant-m|Au bord, pas trop près.",
            "narrateur|Au bord, le torchon reste plié, loin de l'eau.",
            "narrateur|Nino s'arrête sur la pierre sèche.",
            "narrateur|Sous l'anse, le grain de son reste sec.",
            "narrateur|Le veau s'approche du lait, pas de l'eau.",
            "enfant-m|Bois, ici.",
            "papa|Tu n'as pas penché.",
            "maman|Le bord était assez large.",
            "narrateur|Le linge reste plié, loin de la flaque.",
            "narrateur|Le veau a choisi le zinc, pas la flaque.",
        ),
    }
    return table[(t1, t2, t3)]


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    table = {
        (1, 1, 1): L(
            "narrateur|Le veau boit, le mufle dans le lait tiède.",
            "enfant-m|On a attendu à la porte.",
            "papa|Merci d'avoir laissé le fer se taire.",
            "maman|Rentrez, le pain est prêt.",
            "enfant-m|Surtout le moment difficile.",
            "narrateur|Le seau sèche près des bottes, tiède.",
            "narrateur|Un grain de son reste collé au loquet.",
        ),
        (2, 1, 1): L(
            "narrateur|Le veau boit, puis Nino passe la brosse, lente.",
            "enfant-m|On a attendu à la porte.",
            "papa|Merci d'avoir laissé le fer se taire.",
            "maman|Rentrez, le pain est prêt.",
            "enfant-m|Surtout le moment difficile.",
            "narrateur|La brosse garde un poil clair, près du savon.",
            "narrateur|Un poil de brosse reste au gond.",
        ),
        (3, 1, 1): L(
            "narrateur|Le veau boit, puis Nino essuie le mufle.",
            "enfant-m|On a attendu à la porte.",
            "papa|Merci d'avoir laissé le fer se taire.",
            "maman|Rentrez, le pain est prêt.",
            "enfant-m|Surtout le moment difficile.",
            "narrateur|Le torchon sèche sur le loquet, un pli au milieu.",
            "narrateur|Un pli du torchon pend au loquet.",
        ),
        (1, 1, 2): L(
            "narrateur|Dans la paille, le veau finit le lait.",
            "enfant-m|On s'est assis, d'abord.",
            "papa|Tu as regardé avant d'appeler.",
            "maman|Essuie tes genoux, sur le paillasson.",
            "papa|Tu raconteras aussi le moment difficile ?",
            "enfant-m|Surtout celui-là.",
            "narrateur|Le seau sèche près des bottes, tiède.",
            "narrateur|Un brin de paille dort dans le zinc.",
        ),
        (2, 1, 2): L(
            "narrateur|Dans la paille, le veau finit le lait.",
            "enfant-m|On s'est assis, d'abord.",
            "papa|Tu as regardé avant d'appeler.",
            "maman|Essuie tes genoux, sur le paillasson.",
            "papa|Tu raconteras aussi le moment difficile ?",
            "enfant-m|Surtout celui-là.",
            "narrateur|La brosse garde un poil clair, près du savon.",
            "narrateur|Un brin de foin reste dans les poils.",
        ),
        (3, 1, 2): L(
            "narrateur|Dans la paille, le veau finit le lait.",
            "enfant-m|On s'est assis, d'abord.",
            "papa|Tu as regardé avant d'appeler.",
            "maman|Essuie tes genoux, sur le paillasson.",
            "papa|Tu raconteras aussi le moment difficile ?",
            "enfant-m|Surtout celui-là.",
            "narrateur|Le torchon sèche sur le loquet, un pli au milieu.",
            "narrateur|De la paille blonde reste au pli.",
        ),
        (1, 1, 3): L(
            "narrateur|Tout bas, le veau a suivi la voix.",
            "enfant-m|Je n'ai pas parlé fort.",
            "papa|Ta voix n'a pas claqué.",
            "maman|Le fer est retombé, plus loin.",
            "enfant-m|Il a failli partir.",
            "narrateur|Le seau sèche près des bottes, tiède.",
            "narrateur|Le zinc ne sonne plus, près du grain de son.",
        ),
        (2, 1, 3): L(
            "narrateur|Tout bas, le veau a suivi la voix.",
            "enfant-m|Je n'ai pas parlé fort.",
            "papa|Ta voix n'a pas claqué.",
            "maman|Le fer est retombé, plus loin.",
            "enfant-m|Il a failli partir.",
            "narrateur|La brosse garde un poil clair, près du savon.",
            "narrateur|Les poils gardent le silence, contre sa manche.",
        ),
        (3, 1, 3): L(
            "narrateur|Tout bas, le veau a suivi la voix.",
            "enfant-m|Je n'ai pas parlé fort.",
            "papa|Ta voix n'a pas claqué.",
            "maman|Le fer est retombé, plus loin.",
            "enfant-m|Il a failli partir.",
            "narrateur|Le torchon sèche sur le loquet, un pli au milieu.",
            "narrateur|Le torchon garde un pli chaud, silencieux.",
        ),
        (1, 2, 1): L(
            "narrateur|Derrière la barrière, le veau a bu.",
            "enfant-m|On a attendu le vent.",
            "papa|Le silence vous a aidés.",
            "maman|L'herbe sent le soleil.",
            "enfant-m|Surtout le moment difficile.",
            "narrateur|Le seau sèche près des bottes, tiède.",
            "narrateur|Une herbe courte colle au zinc, côté vent.",
        ),
        (2, 2, 1): L(
            "narrateur|Derrière la barrière, le veau a bu.",
            "enfant-m|On a attendu le vent.",
            "papa|Le silence vous a aidés.",
            "maman|L'herbe sent le soleil.",
            "enfant-m|Surtout le moment difficile.",
            "narrateur|La brosse garde un poil clair, près du savon.",
            "narrateur|Une tige se recouche, près de la brosse.",
        ),
        (3, 2, 1): L(
            "narrateur|Derrière la barrière, le veau a bu.",
            "enfant-m|On a attendu le vent.",
            "papa|Le silence vous a aidés.",
            "maman|L'herbe sent le soleil.",
            "enfant-m|Surtout le moment difficile.",
            "narrateur|Le torchon sèche sur le loquet, un pli au milieu.",
            "narrateur|Le torchon ne claque plus contre le bois.",
        ),
        (1, 2, 2): L(
            "narrateur|Le seau vide fume, dans l'herbe.",
            "enfant-m|Je l'ai posé, d'abord.",
            "papa|Tu n'as pas couru vers lui.",
            "maman|Le lait a parlé tout seul.",
            "papa|Tu raconteras aussi le moment difficile ?",
            "enfant-m|Surtout celui-là.",
            "narrateur|Le seau sèche près des bottes, tiède.",
            "narrateur|Un rond clair reste dans l'herbe couchée.",
        ),
        (2, 2, 2): L(
            "narrateur|Le seau vide fume, dans l'herbe.",
            "enfant-m|Je l'ai posé, d'abord.",
            "papa|Tu n'as pas couru vers lui.",
            "maman|Le lait a parlé tout seul.",
            "papa|Tu raconteras aussi le moment difficile ?",
            "enfant-m|Surtout celui-là.",
            "narrateur|La brosse garde un poil clair, près du savon.",
            "narrateur|La brosse garde un poil d'herbe, près du seau.",
        ),
        (3, 2, 2): L(
            "narrateur|Le seau vide fume, dans l'herbe.",
            "enfant-m|Je l'ai posé, d'abord.",
            "papa|Tu n'as pas couru vers lui.",
            "maman|Le lait a parlé tout seul.",
            "papa|Tu raconteras aussi le moment difficile ?",
            "enfant-m|Surtout celui-là.",
            "narrateur|Le torchon sèche sur le loquet, un pli au milieu.",
            "narrateur|Un cercle humide reste sous le torchon.",
        ),
        (1, 2, 3): L(
            "narrateur|Dans l'herbe, le veau a trouvé Nino.",
            "enfant-m|Je me suis fait petit.",
            "papa|Tu t'es baissé, comme lui.",
            "maman|Vous rentrez, les bottes pleines d'herbe.",
            "enfant-m|Il a failli partir.",
            "narrateur|Le seau sèche près des bottes, tiède.",
            "narrateur|Les genoux de Nino gardent deux taches vertes.",
        ),
        (2, 2, 3): L(
            "narrateur|Dans l'herbe, le veau a trouvé Nino.",
            "enfant-m|Je me suis fait petit.",
            "papa|Tu t'es baissé, comme lui.",
            "maman|Vous rentrez, les bottes pleines d'herbe.",
            "enfant-m|Il a failli partir.",
            "narrateur|La brosse garde un poil clair, près du savon.",
            "narrateur|Une pâquerette reste coincée dans les poils.",
        ),
        (3, 2, 3): L(
            "narrateur|Dans l'herbe, le veau a trouvé Nino.",
            "enfant-m|Je me suis fait petit.",
            "papa|Tu t'es baissé, comme lui.",
            "maman|Vous rentrez, les bottes pleines d'herbe.",
            "enfant-m|Il a failli partir.",
            "narrateur|Le torchon sèche sur le loquet, un pli au milieu.",
            "narrateur|Un trèfle a marqué le linge, puis s'en va.",
        ),
        (1, 3, 1): L(
            "narrateur|Quand l'eau s'est tue, le veau a bu.",
            "enfant-m|On a attendu les gouttes.",
            "papa|L'eau n'éclaboussait plus.",
            "maman|Vos manches sont fraîches.",
            "enfant-m|Surtout le moment difficile.",
            "narrateur|Le seau sèche près des bottes, tiède.",
            "narrateur|Une goutte sèche sur la pierre mate.",
        ),
        (2, 3, 1): L(
            "narrateur|Quand l'eau s'est tue, le veau a bu.",
            "enfant-m|On a attendu les gouttes.",
            "papa|L'eau n'éclaboussait plus.",
            "maman|Vos manches sont fraîches.",
            "enfant-m|Surtout le moment difficile.",
            "narrateur|La brosse garde un poil clair, près du savon.",
            "narrateur|Les poils sont restés secs, loin de l'eau.",
        ),
        (3, 3, 1): L(
            "narrateur|Quand l'eau s'est tue, le veau a bu.",
            "enfant-m|On a attendu les gouttes.",
            "papa|L'eau n'éclaboussait plus.",
            "maman|Vos manches sont fraîches.",
            "enfant-m|Surtout le moment difficile.",
            "narrateur|Le torchon sèche sur le loquet, un pli au milieu.",
            "narrateur|Le torchon n'a pas bu l'abreuvoir.",
        ),
        (1, 3, 2): L(
            "narrateur|La pierre mate a gardé deux sabots.",
            "enfant-m|J'ai essuyé, d'abord.",
            "papa|La flaque n'a plus claqué.",
            "maman|Tes mains sentent l'eau.",
            "papa|Tu raconteras aussi le moment difficile ?",
            "enfant-m|Surtout celui-là.",
            "narrateur|Le seau sèche près des bottes, tiède.",
            "narrateur|Deux sabots ont marqué la pierre sèche.",
        ),
        (2, 3, 2): L(
            "narrateur|La pierre mate a gardé deux sabots.",
            "enfant-m|J'ai essuyé, d'abord.",
            "papa|La flaque n'a plus claqué.",
            "maman|Tes mains sentent l'eau.",
            "papa|Tu raconteras aussi le moment difficile ?",
            "enfant-m|Surtout celui-là.",
            "narrateur|La brosse garde un poil clair, près du savon.",
            "narrateur|Les poils ont poussé l'eau, puis se sont tus.",
        ),
        (3, 3, 2): L(
            "narrateur|La pierre mate a gardé deux sabots.",
            "enfant-m|J'ai essuyé, d'abord.",
            "papa|La flaque n'a plus claqué.",
            "maman|Tes mains sentent l'eau.",
            "papa|Tu raconteras aussi le moment difficile ?",
            "enfant-m|Surtout celui-là.",
            "narrateur|Le torchon sèche sur le loquet, un pli au milieu.",
            "narrateur|Le torchon pèse, lourd de la flaque.",
        ),
        (1, 3, 3): L(
            "narrateur|Au bord, le veau a tout bu.",
            "enfant-m|On n'est pas allés trop près.",
            "papa|Le bord était assez large.",
            "maman|Rentrez, le lait de la maison fume.",
            "enfant-m|Il a failli partir.",
            "narrateur|Le seau sèche près des bottes, tiède.",
            "narrateur|Le seau reste sur la pierre sèche, loin de l'eau.",
        ),
        (2, 3, 3): L(
            "narrateur|Au bord, le veau a tout bu.",
            "enfant-m|On n'est pas allés trop près.",
            "papa|Le bord était assez large.",
            "maman|Rentrez, le lait de la maison fume.",
            "enfant-m|Il a failli partir.",
            "narrateur|La brosse garde un poil clair, près du savon.",
            "narrateur|La brosse sèche au bord, loin de la flaque.",
        ),
        (3, 3, 3): L(
            "narrateur|Au bord, le veau a tout bu.",
            "enfant-m|On n'est pas allés trop près.",
            "papa|Le bord était assez large.",
            "maman|Rentrez, le lait de la maison fume.",
            "enfant-m|Il a failli partir.",
            "narrateur|Le torchon sèche sur le loquet, un pli au milieu.",
            "narrateur|Le torchon reste plié, loin de l'eau.",
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
        "narrateur|Le lait tape le zinc, un bruit court, chaud.",
        "narrateur|Ça sent le son, le foin, et le bois mouillé.",
        "narrateur|Au hangar au lait, Nino vit avec papa et maman.",
        "narrateur|Une vache meugle, trop loin pour le hangar.",
        "narrateur|Le soleil tape le bois, une bande chaude.",
        "narrateur|Les bottes de Nino attendent près du seau.",
        "narrateur|Le seau fume, trop plein pour courir.",
        "narrateur|Sous l'anse, un grain de son est coincé, sec.",
        "papa|Tu as vu ce grain, Nino ?",
        "enfant-m|Il tient, c'est le mien.",
        "maman|Le petit veau attend, près de sa mère.",
        "narrateur|En ce moment, Nino serre l'anse, trop fort.",
        "enfant-m|Je lui porte le lait, avant qu'il refroidisse.",
        "papa|Il recule, si le zinc claque.",
        "narrateur|Le sourire de Nino disparaît, un instant.",
        "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
        "maman|On prend les affaires, alors ?",
        "papa|Merci, tu as tenu le seau droit.",
        "enfant-m|J'arrive, petit veau.",
    )
    sons["CHK_T0000_P0000"] = "lait,zinc,hangar"
    profiles["CHK_T0000_P0000"] = "opening"
    emph["CHK_T0000_P0000"] = "grain de son"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près des bottes.",
        "narrateur|Le seau, la brosse, et le torchon.",
        "maman|Tu prends quoi d'abord, Nino ?",
    )
    profiles["CHK_T0001_P0000"] = "choice"
    extras["CHK_T0001_P0000"] = t3lab("le seau", "la brosse", "le torchon")

    t2_sons = {1: "barre,foin", 2: "vent,herbe", 3: "eau,pierre"}
    t2_emph = {1: "barre", 2: "vent", 3: "flaque"}
    t3_emph = {
        1: {1: "porte", 2: "paille", 3: "tout bas"},
        2: {1: "barrière", 2: "seau", 3: "herbe"},
        3: {1: "eau", 2: "essuyer", 3: "bord"},
    }
    t3_sons = {
        (1, 1): "seuil,silence",
        (1, 2): "paille,foin",
        (1, 3): "voix,fer",
        (2, 1): "bois,vent",
        (2, 2): "herbe,lait",
        (2, 3): "herbe,genoux",
        (3, 1): "goutte,silence",
        (3, 2): "pierre,eau",
        (3, 3): "pierre,bord",
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
        emph[cid] = "grain de son"

        t2q = f"{base}_T0002_P0000"
        scripts[t2q] = t2_question(t1)
        profiles[t2q] = "choice"
        extras[t2q] = t3lab("l'étable", "le pré", "l'abreuvoir")

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
                sons[p3] = t3_sons[(t2, t3i)]
                profiles[p3] = "resolution"
                emph[p3] = t3_emph[t2][t3i]

                fin = f"{p3}_F0001"
                scripts[fin] = fin_scene(t1, t2, t3i)
                sons[fin] = "veau,lait"
                profiles[fin] = "ending"
                emph[fin] = "grain de son"

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{SID} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        text, script = from_script(scripts[cid])
        nc = dict(c)
        nc["text"] = text
        nc["script"] = script
        nc["sons"] = sons.get(cid, c.get("sons") or "") or ""
        extra_voice = {}
        if cid in emph:
            extra_voice["emphasis"] = emph[cid]
        nc.update(voice(text, profiles[cid], extra_voice or None))
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

    fins = [c for c in out["chunks"] if c.get("kind") == "passage_fin"]
    texts = [c["text"] for c in fins]
    if len(texts) != 27:
        raise SystemExit(f"fins {len(texts)} != 27")
    if len(set(texts)) != 27:
        raise SystemExit("fins non distinctes")
    lasts = []
    for c in fins:
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(last_n[-1])
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{c['chunk_id']} fin mécanique: {last}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images {len(set(lasts))}/27")

    t3s = [c["text"] for c in out["chunks"] if re.search(r"T0003_P000[123]$", c["chunk_id"])]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"T3 distincts {len(set(t3s))}/27")

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for tic in TICS_PHRASE + BAN:
        if tic in whole:
            raise SystemExit(f"{SID} slogan/calque: {tic}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nino" not in blob:
        raise SystemExit(f"{SID}: Nino absent")
    if "grain de son" not in blob:
        raise SystemExit(f"{SID}: indice grain de son absent")
    m = TIC_WORDS.search(blob)
    if m:
        raise SystemExit(f"{SID} tic corpus: {m.group(0)}")
    if not all(c.get("text_xai_tags") for c in out["chunks"]):
        raise SystemExit(f"{SID}: text_xai_tags manquant")
    if not all(c.get("notes") for c in out["chunks"]):
        raise SystemExit(f"{SID}: notes manquant")

    t3_blobs = [
        c["script"].lower()
        for c in out["chunks"]
        if re.search(r"T0003_P000[123]$", c["chunk_id"])
    ]
    paid = sum(1 for b in t3_blobs if "grain de son" in b)
    if paid != 27:
        raise SystemExit(f"{SID}: indice payé {paid}/27 T3")

    counts = [path_words(by, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {(ROOT / SID / 'merged.json')} bytes={(ROOT / SID / 'merged.json').stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.BES.001 — plus de temps ou de calme (vécue, non dite)\n"
        "- **Personnages :** Nino, papa, maman (un seul enfant)\n"
        "- **Lieu :** ferme du village : étable, pré, abreuvoir — hangar au lait\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Au hangar au lait, Nino veut porter le seau tiède au petit veau "
        "**avant que le lait refroidisse**. Sous l'anse, un **grain de son** est coincé, sec. "
        "Il prend d'abord le seau, la brosse ou le torchon ; les trois partent. "
        "À l'étable le fer claque, au pré le vent penche, à l'abreuvoir l'eau saute. "
        "Il fonce : le veau recule. Il refuse de foncer. Le grain de son paie le début. "
        "Neuf façons (porte, paille, tout bas ; barrière, poser le seau, dans l'herbe ; "
        "l'eau se tait, essuyer, au bord). Le veau boit.\n\n"
        "## Vécu\n\n"
        "Nino veut le lait **maintenant**. Le veau ne veut pas la même chose au même moment. "
        "Sourire qui disparaît, poitrine qui se bouscule, adulte accroupi. "
        "Première idée trop vite (zinc, poils, drap). Seconde ruse (chaîne, mouche, goutte). "
        "Il refuse de foncer. Personne ne donne la réponse. Il observe l'anse, écoute le lieu. "
        "Le dénouement a failli ne pas arriver. Trace unique par chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Monde ≠ TREE-AUT-028 (seau vert, croissant de sable) ≠ TREE-COL-012 (bâche, marché).\n"
        "- Indice unique inventé : grain de son sous l'anse (pas ancre/étoile/fil/croissant/"
        "virgule/œillet/perle/marque fine/ombre-flèche/tache).\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- T1/T2/T3 changent l'action. Équipement non retiré. 9 T2, 27 T3, 27 fins, 27 dernières images.\n"
        "- Merci vécu (seau tenu droit). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        f"- N3 ≤ 16. `check()` OK. Pas apply. Pas git. Pas audio.\n"
        f"- Chemins : {min(counts)} à {max(counts)} mots (moyenne {sum(counts)//len(counts)}).\n\n"
        "## Contrôles\n\n"
        "- 86 chunks, 27 chemins, 27 fins distinctes, 27 dernières images, 27 T3 distincts\n"
        "- Indice payé aux 27 climaxes T3\n"
        "- `text` = `script` collé ; graphe inchangé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )


def main() -> None:
    write_tree()


if __name__ == "__main__":
    main()
