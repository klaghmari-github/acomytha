#!/usr/bin/env python3
"""TREE-DIF-030 — Le pain chaud d'Amir et le four du marché (N1, DIF.BES.001)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "TREE-DIF-030"
LIM = LIMITS["N1"]
TITLE = "Le pain chaud d'Amir et le four du marché"
FIL = (
    "La soupe attend à la maison, sans pain. Au marché, Amir veut le pain rond "
    "du four, bien chaud, pour le partager avec Chouchou. Un grain de sésame "
    "colle au sac. Ils emportent sac, serviette et pièce. Au four la boîte de "
    "sésame est vide, la file saute, le banc est trop agité. Amir fonce, ça rate. "
    "Il refuse de foncer. Le grain guide. Le pain rentre, tiède."
)
CHARS = "Amir, Chouchou, papa, maman"
SETTING = "marché du village, four du boulanger"

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=500, sentence=260, energy="warm", contour="storytelling",
        noise=0.36, emphasis="grain de sésame",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=la soupe attend sans pain; tempo=naturel; sourire=léger; respiration=ample",
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
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde ce qu il a pris; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=450, sentence=280, energy="bright", contour="falling",
        noise=0.34, emphasis="grain de sésame",
        note="arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les trois affaires viennent; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=420, sentence=250, energy="lively", contour="dynamic",
        noise=0.37, emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=il se presse vers le pain; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0,
        pause=520, sentence=300, energy="tense", contour="dynamic",
        noise=0.34, emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=un ingrédient manque au moment décisif; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=560, sentence=270, energy="bright", contour="falling",
        noise=0.35, emphasis="grain de sésame",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=il refuse de foncer, le grain guide; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3,
        pause=900, sentence=340, energy="calm", contour="falling",
        noise=0.31, emphasis="grain de sésame",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le grain de sésame paie le début; tempo=posé; sourire=léger; respiration=ample",
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
    "plus de temps ou de calme",
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
    "kenzo",
    "sami",
    "léa",
    "lea ",
    "tom ",
    "zoé",
    "lina",
    "iris",
    "bac à sable",
    "toboggan",
    "balançoire",
    "capitaine",
    "plic",
    "volet jaune",
    "escargot",
    "virgule de farine",
    "virgule farine",
    "sachet kraft",
    "volet blond",
    "store",
    "panier d'osier",
    "goutte de fraise",
    "étoile brune",
    "ancre minuscule",
    "fil pâle",
    "croissant d'eau",
    "croissant pâle",
    "virgule farine",
    "bouton nacre",
    "nœud raphia",
    "pois ivoire",
    "grain savon rose",
    "grain vanille",
    "pastille colle",
    "virgule buée",
    "capuchon penche",
    "grain doré",
    "brin safran",
    "brin de safran",
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
    "marque fine",
    "ombre-flèche",
    "ombre en forme",
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


OBJ = {
    1: {
        "lab": "le sac",
        "ans": "sac",
        "acc": "sac | le sac | dans le sac | là-dedans",
        "retry": "Le pain ira dans le sac.",
        "emph": "sac",
        "sons": "tissu,sac",
        "coda": "Le sac sèche près des souliers.",
        "hold": "Le sac reste ouvert, contre sa hanche.",
        "grip": "Amir tient le sac, sans le serrer.",
        "lead": "Le sac tape un peu sa hanche.",
    },
    2: {
        "lab": "la serviette",
        "ans": "serviette",
        "acc": "serviette | la serviette | dans la serviette | le linge",
        "retry": "Le pain ira dans la serviette.",
        "emph": "serviette",
        "sons": "linge,pli",
        "coda": "La serviette sèche près des souliers.",
        "hold": "La serviette reste pliée, comme un nid.",
        "grip": "Amir tient la serviette, sans la tordre.",
        "lead": "La serviette frôle sa joue, tiède.",
    },
    3: {
        "lab": "la pièce",
        "ans": "poche",
        "acc": "poche | la poche | dans la poche | la pièce",
        "retry": "La pièce est dans la poche.",
        "emph": "pièce",
        "sons": "piece,tissu",
        "coda": "Près du pain, la pièce repose.",
        "hold": "Au fond, la pièce reste sans tinter.",
        "grip": "Amir tient la pièce, sans la faire sonner.",
        "lead": "Au fond du sac, la pièce tinte.",
    },
}

T3_LABS = {
    1: ("attendre un peu", "reculer", "derrière la farine"),
    2: ("son tour", "le bord", "répéter"),
    3: ("le pigeon", "s'asseoir", "l'ombre"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Amir glisse la main dans le sac.",
            "enfant-m|Le pain ira là-dedans.",
            "maman|Tiens-le ouvert, Amir.",
            "narrateur|Le tissu sent la farine, tiède.",
            "narrateur|Le grain de sésame reste collé, beige.",
            "papa|La serviette aussi, près de toi.",
            "narrateur|Maman y pose la pièce, légère.",
            "narrateur|Le sac emmène tout, avec eux.",
            "enfant-m|Chouchou, on va au four.",
            "narrateur|Elle hoche la tête, sans parler.",
            "papa|Le sac d'abord, vous l'avez.",
            "enfant-m|Vite !",
            "narrateur|Il serre trop la lanière, un instant.",
            "narrateur|Puis il lâche un peu, pour elle.",
        )
    if t1 == 2:
        return L(
            "narrateur|Amir prend la serviette, tiède au pouce.",
            "enfant-m|J'enveloppe le pain avec.",
            "papa|Plie-la, comme un nid.",
            "narrateur|Le linge sent le soleil séché.",
            "narrateur|Le grain de sésame brille, sur le sac.",
            "maman|Le sac, ensuite, près des pieds.",
            "narrateur|Elle glisse la pièce dans le tissu.",
            "narrateur|La serviette emmène tout, avec eux.",
            "enfant-m|Chouchou, on y va.",
            "narrateur|Elle pose un pied, puis l'autre.",
            "maman|La serviette d'abord, elle est prête.",
            "enfant-m|Vite !",
            "narrateur|Il plie trop vite, un instant.",
            "narrateur|Puis il attend qu'elle arrive.",
        )
    return L(
        "narrateur|Amir prend la pièce, toute ronde.",
        "enfant-m|C'est pour le pain chaud.",
        "maman|Glisse-la dans ta poche.",
        "narrateur|Un petit tintement sonne contre le tissu.",
        "narrateur|Le grain de sésame reste collé au sac.",
        "papa|Le sac et la serviette, avec vous.",
        "narrateur|Il les pose près des sandales.",
        "narrateur|La pièce part avec le reste.",
        "enfant-m|Chouchou, viens !",
        "narrateur|Elle avance, les pas petits.",
        "papa|La pièce d'abord, elle est prête.",
        "enfant-m|Vite !",
        "narrateur|Il serre trop la pièce, un instant.",
        "narrateur|Puis il ouvre la main, pour elle.",
    )


def t1_q(t1: int) -> list[str]:
    if t1 == 3:
        return L(
            "narrateur|Amir a glissé la pièce dans la poche.",
            "maman|Elle est où, la pièce ?",
        )
    o = OBJ[t1]
    return L(
        f"narrateur|Amir a préparé le pain {('dans le sac' if t1 == 1 else 'dans la serviette')}.",
        "maman|Le pain ira où ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Le sac reste ouvert, contre sa hanche.",
            "enfant-f|Ça sent le chaud.",
            "enfant-m|On le mettra dedans.",
            "maman|Chouchou, tu viens avec nous ?",
            "narrateur|Elle hoche, sans un mot.",
            "papa|On avance vers le four ?",
            "enfant-m|Oui, papa.",
            "narrateur|Le grain de sésame brille, beige.",
            "maman|Vos pieds, dans les sandales.",
        )
    if t1 == 2:
        return L(
            "narrateur|La serviette pend, comme un nid.",
            "enfant-m|Le pain va dormir là.",
            "enfant-f|Pas trop vite, d'accord ?",
            "papa|Le four fume, là-bas.",
            "maman|Vos pieds, dans les sandales ?",
            "enfant-m|Oui, maman.",
            "narrateur|Le grain de sésame reste visible, mince.",
            "narrateur|Un bout de linge cherche le chaud.",
            "papa|On avance vers les caisses.",
        )
    return L(
        "narrateur|La pièce tinte, dans la poche.",
        "enfant-m|Je la tiens, bien fort.",
        "enfant-f|Moi, je marche lentement.",
        "maman|Le four vous attend, blanc.",
        "papa|On y va, tous les quatre ?",
        "enfant-m|Oui.",
        "narrateur|Le grain de sésame brille, sur le sac.",
        "narrateur|Un tintement court répond au four.",
        "maman|La pièce est prête.",
    )


def t2_question(t1: int) -> list[str]:
    head = OBJ[t1]["lead"]
    return L(
        f"narrateur|{head}",
        "narrateur|Le four fume devant, blanc.",
        "narrateur|Puis la file avance, trop vite.",
        "narrateur|Plus loin, un banc attend.",
        "papa|Vous allez où, tous les deux ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    o = OBJ[t1]
    flavor = {
        1: "Le tissu du sac frotte sa hanche, lent.",
        2: "Le linge de la serviette chauffe sa joue.",
        3: "Au fond, la pièce reste muette.",
    }[t1]
    if t2 == 1:
        extra = {
            1: "Le sac tape trop vite sa hanche.",
            2: "La serviette claque trop près du chaud.",
            3: "Trop tôt, la pièce tinte trop fort.",
        }[t1]
        return L(
            f"narrateur|{flavor}",
            "narrateur|Amir avance trop vite vers le four.",
            "narrateur|Le souffle brûle les joues.",
            f"narrateur|{extra}",
            "enfant-f|Trop fort.",
            "narrateur|Chouchou met les mains contre ses oreilles.",
            "enfant-m|Le pain est là !",
            "narrateur|La boîte de sésame est vide.",
            "narrateur|Une vague de chaleur pousse le pain.",
            "enfant-m|Je le prends, vite !",
            "narrateur|Il tend la main, puis la retire.",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "papa|On s'accroupit, à votre hauteur.",
            "narrateur|Cette fois, Amir refuse de foncer.",
            "narrateur|Il regarde le grain de sésame, sur le sac.",
            "narrateur|Chouchou ne dit rien.",
            "enfant-m|On fait comment, alors ?",
            "papa|Vous trouvez, tous les deux ?",
        )
    if t2 == 2:
        extra = {
            1: "Le sac se serre, trop près des genoux.",
            2: "La serviette se plie, trop vite.",
            3: "Soudain, la pièce se perd.",
        }[t1]
        return L(
            f"narrateur|{flavor}",
            f"narrateur|{extra}",
            "narrateur|Des gens poussent, trop près des genoux.",
            "enfant-f|Mes pieds n'y arrivent pas.",
            "narrateur|Chouchou s'arrête, collée au sac.",
            "enfant-m|Le pain va partir sans nous.",
            "narrateur|À la caisse, personne ne répond.",
            "narrateur|La boîte de sésame n'est pas là.",
            "narrateur|Un dos passe devant, trop vite.",
            "enfant-m|Je glisse, vite !",
            "narrateur|Il lève le pied, puis le pose.",
            "narrateur|Le sourire d'Amir disparaît.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "maman|On s'accroupit, à votre hauteur.",
            "narrateur|Cette fois, Amir refuse de foncer.",
            "narrateur|Il regarde le grain de sésame, sur le sac.",
            "narrateur|Chouchou ne dit rien.",
            "enfant-m|On fait comment, Chouchou ?",
            "maman|Vous trouvez, tous les deux ?",
        )
    extra = {
        1: "Le sac bute contre le pied du banc.",
        2: "La serviette glisse vers le bois chaud.",
        3: "Contre le banc, la pièce tinte.",
    }[t1]
    return L(
        f"narrateur|{flavor}",
        f"narrateur|{extra}",
        "narrateur|Autour du banc, les voix sont trop fortes.",
        "enfant-f|Le pigeon a trop bougé.",
        "narrateur|Chouchou recule, les mains aux oreilles.",
        "enfant-m|On s'assoit pour le pain ?",
        "narrateur|Le pain n'est pas sur le bois.",
        "narrateur|La boîte de sésame manque, près des caisses.",
        "narrateur|Le pigeon picore trop près du bois.",
        "enfant-m|Je chasse l'oiseau, vite !",
        "narrateur|Il lève le bras, puis le baisse.",
        "narrateur|Le sourire d'Amir disparaît.",
        "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        "papa|On s'accroupit, à votre hauteur.",
        "narrateur|Cette fois, Amir refuse de foncer.",
        "narrateur|Il regarde le grain de sésame, sur le sac.",
        "narrateur|Chouchou ne dit rien.",
        "enfant-m|On fait comment, alors ?",
        "papa|Vous trouvez, tous les deux ?",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Le four souffle trop fort.",
            "papa|Attendre, reculer, ou derrière la farine ?",
        )
    if t2 == 2:
        return L(
            "narrateur|La file avance trop vite.",
            "maman|Son tour, le bord, ou répéter ?",
        )
    return L(
        "narrateur|Le banc reste trop agité.",
        "papa|Le pigeon, s'asseoir, ou l'ombre ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    o = OBJ[t1]
    hold, grip = o["hold"], o["grip"]
    if t2 == 1 and t3 == 1:
        return L(
            "enfant-m|On attend.",
            "enfant-f|Moi aussi.",
            "narrateur|Le souffle du four baisse, lent.",
            "narrateur|Chouchou baisse les mains, peu à peu.",
            f"narrateur|{hold}",
            f"narrateur|{grip}",
            "papa|Il chante moins, maintenant.",
            "enfant-m|Tu peux regarder.",
            "narrateur|Le grain de sésame brille, sur le sac.",
            "narrateur|La boîte revient, pleine de grains.",
            "maman|Vous avez regardé, tous les deux.",
            "enfant-f|Je vois le pain rond.",
            "narrateur|Le pain a failli rester, trop chaud.",
        )
    if t2 == 1 and t3 == 2:
        step = {
            1: "Amir recule avec le sac, un pas.",
            2: "Amir recule avec la serviette, un pas.",
            3: "Amir recule, la pièce dans la poche.",
        }[t1]
        return L(
            "enfant-m|On recule, un pas.",
            "enfant-f|Plus loin du chaud.",
            f"narrateur|{step}",
            "narrateur|Le bruit devient petit, comme un souffle.",
            "narrateur|Chouchou lève un peu les yeux.",
            f"narrateur|{grip}",
            "papa|Vous avez regardé d'abord.",
            "enfant-m|On avance, maintenant ?",
            "maman|Quand elle est prête.",
            "enfant-f|Le pain est là.",
            "narrateur|Le grain de sésame vise le four, beige.",
            "narrateur|La pelle de bois retrouve sa place.",
            "narrateur|Le pain a failli brûler trop fort.",
        )
    if t2 == 1 and t3 == 3:
        hide = {
            1: "Amir glisse le sac derrière la farine.",
            2: "Amir glisse la serviette derrière la farine.",
            3: "La pièce tinte, derrière le sac de farine.",
        }[t1]
        return L(
            "enfant-m|Derrière la farine, ça souffle moins.",
            "enfant-f|Je viens, près de toi.",
            f"narrateur|{hide}",
            "narrateur|Le sac de farine fait un mur blanc.",
            "narrateur|Le four reste de l'autre côté.",
            f"narrateur|{hold}",
            "papa|Ici, ça ne souffle plus.",
            "enfant-m|On observe d'abord.",
            "maman|Vous avez trouvé le coin tranquille.",
            "enfant-f|Je vois le pain, par ici.",
            "narrateur|Le grain de sésame se lit, sur le blanc.",
            "narrateur|La boîte revient, contre le mur blanc.",
            "narrateur|Le pain a failli se cacher trop loin.",
        )
    if t2 == 2 and t3 == 1:
        return L(
            "enfant-m|On attend notre tour.",
            "enfant-f|Je compte les pieds, lentement.",
            "narrateur|Un pas, puis un autre, puis le silence.",
            f"narrateur|{hold}",
            f"narrateur|{grip}",
            "narrateur|Chouchou avance quand le dos bouge.",
            "papa|Vous n'avez pas poussé.",
            "enfant-m|C'est à nous, maintenant.",
            "maman|Elle a pu suivre.",
            "enfant-f|Le pain est chaud.",
            "narrateur|Le grain de sésame n'a pas sauté.",
            "narrateur|La boîte revient, à la caisse.",
            "narrateur|Le pain a failli partir avec un dos.",
        )
    if t2 == 2 and t3 == 2:
        edge = {
            1: "Amir glisse le sac le long du bord.",
            2: "Amir glisse la serviette le long du bord.",
            3: "La pièce tinte, tout au bord.",
        }[t1]
        return L(
            "enfant-m|On prend le bord, Chouchou.",
            "enfant-f|Pas au milieu, d'accord.",
            f"narrateur|{edge}",
            "narrateur|Ils longent les caisses, sans se bousculer.",
            "narrateur|Chouchou pose un pied, puis l'autre.",
            f"narrateur|{grip}",
            "papa|Vous avez vu le chemin, d'abord.",
            "enfant-m|On y est.",
            "maman|Le bord était assez large.",
            "enfant-f|Je n'ai pas couru.",
            "narrateur|Le grain de sésame tient, près de la hanche.",
            "narrateur|La boîte glisse le long des caisses.",
            "narrateur|Le pain a failli rester au bord.",
        )
    if t2 == 2 and t3 == 3:
        again = {
            1: "Amir reprend le sac, au début.",
            2: "Amir reprend la serviette, au début.",
            3: "Amir reprend la pièce, au début.",
        }[t1]
        return L(
            "enfant-m|On recommence, plus lent.",
            "enfant-f|Je te suis, cette fois.",
            f"narrateur|{again}",
            "narrateur|Ils refont le chemin, pas après pas.",
            "narrateur|Chouchou répète chaque pas, sans courir.",
            f"narrateur|{hold}",
            "papa|Vous avez repris le même sentier.",
            "enfant-m|Tu peux, maintenant.",
            "maman|Le même chemin a aidé.",
            "enfant-f|J'y suis arrivée.",
            "narrateur|Le grain de sésame revient sous les yeux.",
            "narrateur|La boîte revient, au même endroit.",
            "narrateur|Le pain a failli attendre un autre tour.",
        )
    if t2 == 3 and t3 == 1:
        return L(
            "enfant-m|On attend le pigeon.",
            "enfant-f|Il va se poser, je crois.",
            "narrateur|L'oiseau se tait, une patte, puis l'autre.",
            f"narrateur|{hold}",
            f"narrateur|{grip}",
            "narrateur|Chouchou baisse les mains, lentement.",
            "papa|Il n'a plus bougé trop fort.",
            "enfant-m|On peut s'asseoir.",
            "maman|Vous avez regardé, d'abord.",
            "enfant-f|Il est calme, maintenant.",
            "narrateur|Le grain de sésame reste, sans trembler.",
            "narrateur|La boîte revient, près des caisses.",
            "narrateur|Le pain a failli fuir le pigeon.",
        )
    if t2 == 3 and t3 == 2:
        sit = {
            1: "Amir pose le sac sur le bois.",
            2: "Amir pose la serviette sur le bois.",
            3: "Amir pose la pièce sur le bois.",
        }[t1]
        return L(
            "enfant-m|On s'assoit, d'abord.",
            "enfant-f|Moi aussi, je m'assois.",
            f"narrateur|{sit}",
            "narrateur|Le bois du banc est tiède, un peu rêche.",
            "narrateur|Chouchou pose les mains, sans les coller.",
            f"narrateur|{grip}",
            "papa|Ici, on ne court plus.",
            "enfant-m|Après, on prend le pain.",
            "maman|Vous vous êtes arrêtés, ensemble.",
            "enfant-f|Mes oreilles vont mieux.",
            "narrateur|Le grain de sésame repose, sur les genoux.",
            "narrateur|La boîte revient, au pied du banc.",
            "narrateur|Le pain a failli rater le banc.",
        )
    shade = {
        1: "Amir glisse le sac vers l'ombre.",
        2: "Amir glisse la serviette vers l'ombre.",
        3: "La pièce tinte, vers l'ombre du banc.",
    }[t1]
    return L(
        "enfant-m|L'ombre, au bout du banc.",
        "enfant-f|Là, ça parle moins.",
        f"narrateur|{shade}",
        "narrateur|Un bout de toile fait un toit gris.",
        "narrateur|Chouchou s'y glisse, contre le bois.",
        f"narrateur|{hold}",
        "papa|Le soleil n'entre pas, là.",
        "enfant-m|On reste ici.",
        "maman|Vous avez trouvé le coin lent.",
        "enfant-f|Je suis prête, après.",
        "narrateur|Le grain de sésame brille à l'ombre.",
        "narrateur|La boîte revient, sous la toile grise.",
        "narrateur|Le pain a failli manquer l'ombre.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    table = {
        (1, 1, 1): L(
            "narrateur|Le pain rond entre dans le sac, tiède.",
            "enfant-f|On a attendu, et il est venu.",
            "enfant-m|Il sent la croûte, bien chaud.",
            "papa|Vous avez regardé le four, ensemble.",
            "maman|La soupe est prête, dedans.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame reste collé, beige.",
            "narrateur|Une miette tiède colle au rebord de l'assiette.",
        ),
        (1, 1, 2): L(
            "narrateur|Ils rentrent, le pain contre le sac.",
            "enfant-m|On a reculé, d'abord.",
            "enfant-f|Le four n'était plus trop fort.",
            "papa|Vous avez vu avant d'avancer.",
            "maman|Rentrez, le pain refroidit.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame a glissé sur la croûte.",
            "narrateur|La croûte craque dans l'assiette, minuscule.",
        ),
        (1, 1, 3): L(
            "narrateur|Derrière la farine, le pain les suit.",
            "enfant-f|Ce coin-là était le bon.",
            "enfant-m|Il n'a pas trop chanté.",
            "maman|Vous avez changé de place.",
            "papa|Le four souffle plus loin.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame brille dans la farine du seuil.",
            "narrateur|Au seuil, l'air sent la croûte chaude.",
        ),
        (1, 2, 1): L(
            "narrateur|Le pain tiède pose une ombre sur la table.",
            "enfant-m|On a attendu notre tour.",
            "enfant-f|J'ai compté les pieds.",
            "papa|Vous n'avez pas poussé.",
            "maman|Lavez les mains, avant la soupe.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame dort dans le pli du sac.",
            "narrateur|Une odeur de farine reste dans l'entrée.",
        ),
        (1, 2, 2): L(
            "narrateur|Ils n'ont pas couru dans toute la file.",
            "enfant-f|Le bord était assez large.",
            "enfant-m|Tes pas y allaient, Chouchou.",
            "maman|Le pain est chaud, sur la table.",
            "papa|Chacun a marché à son rythme.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame pointe la nappe, beige.",
            "narrateur|Une miette brille près de la fenêtre.",
        ),
        (1, 2, 3): L(
            "narrateur|Le même chemin les ramène, plus lent.",
            "enfant-m|On a recommencé, tous les deux.",
            "enfant-f|Cette fois, j'ai suivi.",
            "papa|Le chemin repris a ouvert la file.",
            "maman|Coupez-le en deux, pour la soupe.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame voyage avec la part de Chouchou.",
            "narrateur|Deux parts tièdes attendent dans l'assiette.",
        ),
        (1, 3, 1): L(
            "narrateur|Le pigeon reste sur la caisse, silencieux.",
            "enfant-f|On l'a regardé, d'abord.",
            "enfant-m|Puis le pain est venu.",
            "maman|Essuie tes pieds, sur le paillasson.",
            "papa|Le pain est à vous, maintenant.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame a vu le pigeon.",
            "narrateur|Dehors, le pigeon se tait sur une caisse.",
        ),
        (1, 3, 2): L(
            "narrateur|Un peu de soleil les suit jusqu'à la porte.",
            "enfant-m|On s'est assis, d'abord.",
            "enfant-f|Mes oreilles ont eu le temps.",
            "papa|Le banc vous a gardés un moment.",
            "maman|Le pain sèche, sur le linge.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame se cache sous la croûte.",
            "narrateur|La vitre garde une odeur de croûte.",
        ),
        (1, 3, 3): L(
            "narrateur|Un peu de poussière de farine reste au seuil.",
            "enfant-f|L'ombre était plus douce.",
            "enfant-m|On y est resté un peu.",
            "papa|Le coin du banc était le bon.",
            "maman|Vos mains sentent le pain.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame garde l'ombre de la toile.",
            "narrateur|Un nuage de farine dort au seuil.",
        ),
        (2, 1, 1): L(
            "narrateur|Le pain rond s'endort dans la serviette, tiède.",
            "enfant-f|On a attendu, près du four.",
            "enfant-m|Il sent le linge, et la croûte.",
            "papa|Vous avez laissé le souffle baisser.",
            "maman|La soupe fume, dans les bols.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame reste dans le pli du linge.",
            "narrateur|La serviette garde un rond chaud, au dos.",
        ),
        (2, 1, 2): L(
            "narrateur|Ils rentrent, le pain niché dans le linge.",
            "enfant-m|Un pas en arrière a suffi.",
            "enfant-f|Mes oreilles ont dit oui.",
            "papa|Vous avez reculé, puis regardé.",
            "maman|Posez le linge, près des bols.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame a suivi le recul, beige.",
            "narrateur|Un fil de vapeur quitte la croûte, lent.",
        ),
        (2, 1, 3): L(
            "narrateur|Derrière la farine, le linge sent le chaud.",
            "enfant-f|Le mur blanc nous a gardés.",
            "enfant-m|Le pain nous a trouvés.",
            "maman|Vous avez changé de coin.",
            "papa|Le four chante plus loin.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame se lit contre le blanc.",
            "narrateur|Le linge sent le four, près des souliers.",
        ),
        (2, 2, 1): L(
            "narrateur|Le pain tiède marque la serviette, rond.",
            "enfant-m|J'ai compté, sans pousser.",
            "enfant-f|Les pieds ont dit notre tour.",
            "papa|La file vous a laissés passer.",
            "maman|Lavez les mains, le linge attend.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame reste dans le pliage.",
            "narrateur|Des grains de sésame restent dans le pliage.",
        ),
        (2, 2, 2): L(
            "narrateur|Ils ont longé les caisses, le linge contre eux.",
            "enfant-f|Le bord m'a suffi.",
            "enfant-m|Tes pas collaient aux miens.",
            "maman|Le pain est chaud, sous le linge.",
            "papa|Personne n'a couru.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame n'est pas tombé.",
            "narrateur|La nappe reçoit une ombre ronde, tiède.",
        ),
        (2, 2, 3): L(
            "narrateur|Le chemin repris ramène le pain, lent.",
            "enfant-m|On a refait les pas.",
            "enfant-f|Cette fois, je savais.",
            "papa|Recommencer a ouvert la file.",
            "maman|Coupez-le, le linge dessous.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame a refait la route.",
            "narrateur|Deux croûtes se touchent, dans l'assiette.",
        ),
        (2, 3, 1): L(
            "narrateur|Le pigeon laisse le banc, et le pain vient.",
            "enfant-f|On l'a laissé se poser.",
            "enfant-m|Puis le linge a reçu le chaud.",
            "maman|Essuie tes pieds, le linge est plein.",
            "papa|L'oiseau vous a laissé la place.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame n'a pas tremblé.",
            "narrateur|Le bois du banc garde une chaleur ronde.",
        ),
        (2, 3, 2): L(
            "narrateur|Assis d'abord, ils rentrent le pain au linge.",
            "enfant-m|On s'est arrêtés.",
            "enfant-f|Mes oreilles ont dit merci au bois.",
            "papa|Le banc vous a tenus.",
            "maman|Le pain sèche, dans le nid de linge.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame s'est posé, comme eux.",
            "narrateur|Les oreilles de Chouchou se reposent, enfin.",
        ),
        (2, 3, 3): L(
            "narrateur|Sous la toile, le pain rejoint le linge.",
            "enfant-f|L'ombre parlait moins.",
            "enfant-m|On y a resté.",
            "papa|Le toit gris était le bon.",
            "maman|Vos mains sentent le linge chaud.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame brille sous la toile, beige.",
            "narrateur|L'ombre de la toile reste dans leurs yeux.",
        ),
        (3, 1, 1): L(
            "narrateur|Le pain rond arrive, la pièce se tait.",
            "enfant-f|On a attendu le souffle.",
            "enfant-m|Je paie, maintenant.",
            "papa|Vous avez regardé le four baisser.",
            "maman|La soupe attend la croûte.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame reste près de la pièce.",
            "narrateur|La pièce tinte une dernière fois, puis silence.",
        ),
        (3, 1, 2): L(
            "narrateur|Ils rentrent, la pièce tiède contre le pain.",
            "enfant-m|On a reculé, d'abord.",
            "enfant-f|Le chaud n'a plus mordu.",
            "papa|Un pas en arrière a ouvert le four.",
            "maman|Posez la pièce, près des bols.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame a reculé avec eux.",
            "narrateur|Un cercle de chaleur reste dans la poche.",
        ),
        (3, 1, 3): L(
            "narrateur|Derrière la farine, la pièce tinte, puis se tait.",
            "enfant-f|Le mur blanc était calme.",
            "enfant-m|J'ai payé, sans courir.",
            "maman|Vous avez changé de côté.",
            "papa|Le four reste loin.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame se pose près de la pièce.",
            "narrateur|Près du pain, la pièce repose, mate.",
        ),
        (3, 2, 1): L(
            "narrateur|Le pain tiède, la pièce a fait son tour.",
            "enfant-m|J'ai attendu, pièce au fond.",
            "enfant-f|Les pieds ont compté avec moi.",
            "papa|Vous n'avez pas sauté la file.",
            "maman|Lavez les mains, la pièce reste.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame n'a pas tinté.",
            "narrateur|Un tintement court s'endort dans le tissu.",
        ),
        (3, 2, 2): L(
            "narrateur|Au bord des caisses, la pièce a suffi.",
            "enfant-f|On n'a pas pris le milieu.",
            "enfant-m|J'ai tendu la pièce, au bord.",
            "maman|Le pain est chaud, près de la pièce.",
            "papa|Le bord vous a gardés.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame a suivi le bord.",
            "narrateur|La pièce brille à côté de la miette.",
        ),
        (3, 2, 3): L(
            "narrateur|Le chemin repris, la pièce ouvre la file.",
            "enfant-m|On a recommencé, pièce en main.",
            "enfant-f|Cette fois, j'ai suivi le tintement.",
            "papa|Reprendre le sentier a payé.",
            "maman|Coupez-le, la pièce au milieu.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame a recommencé la route.",
            "narrateur|Deux parts, et la pièce au milieu.",
        ),
        (3, 3, 1): L(
            "narrateur|Le pigeon se tait, la pièce paie le pain.",
            "enfant-f|On l'a regardé se poser.",
            "enfant-m|Puis j'ai tendu la pièce.",
            "maman|Essuie tes pieds, la pièce est rentrée.",
            "papa|L'oiseau vous a laissé le banc.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame a attendu l'oiseau.",
            "narrateur|La pièce ne tinte plus, près du pigeon.",
        ),
        (3, 3, 2): L(
            "narrateur|Assis d'abord, la pièce réchauffe le pain.",
            "enfant-m|On s'est assis, pièce sur le bois.",
            "enfant-f|Mes oreilles ont dit oui.",
            "papa|Le banc a tenu la pièce.",
            "maman|Le pain sèche, près de la pièce.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame s'est assis avec eux.",
            "narrateur|La pièce se réchauffe contre le pain.",
        ),
        (3, 3, 3): L(
            "narrateur|Sous l'ombre, la pièce paie le pain.",
            "enfant-f|Là, ça parlait moins.",
            "enfant-m|J'ai payé, sous la toile.",
            "papa|Le toit gris était assez large.",
            "maman|Vos mains sentent le pain, et le métal.",
            f"narrateur|{coda}",
            "narrateur|Le grain de sésame brille près de la pièce.",
            "narrateur|La pièce garde un peu de farine, blanche.",
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
        "narrateur|La porte du four claque, comme une bouche.",
        "narrateur|Une odeur de croûte marche dans la rue.",
        "narrateur|La soupe attend à la maison, sans pain.",
        "narrateur|Le marché du village s'ouvre, large.",
        "narrateur|Sous la toile grise, les caisses sont tièdes.",
        "narrateur|Un grain de sésame colle au sac.",
        "narrateur|Il brille près de la lanière, beige.",
        "papa|Tu as vu ce grain, Amir ?",
        "enfant-m|Il est collé au tissu.",
        "maman|Le pain rond va sortir.",
        "narrateur|Papa tient la pièce, ronde, tiède.",
        "narrateur|Maman plie la serviette, comme un nid.",
        "narrateur|En ce moment, le four souffle blanc.",
        "enfant-m|Je le veux, bien chaud !",
        "narrateur|Chouchou arrive, les pas petits.",
        "narrateur|Elle fixe le grain, sans parler.",
        "papa|On prépare, avant le four ?",
        "enfant-m|Vite, Chouchou !",
        "narrateur|Elle ne répond pas.",
        "narrateur|Sa main serre la lanière.",
        "maman|Le sac, la serviette, et la pièce.",
        "papa|Merci, tu as regardé Chouchou.",
        "narrateur|Sur la planche, une boîte attend, vide.",
        "enfant-m|Le pain, pour la soupe !",
    )
    sons["CHK_T0000_P0000"] = "four,toile,caisse"
    profiles["CHK_T0000_P0000"] = "opening"
    emph["CHK_T0000_P0000"] = "grain de sésame"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près des caisses.",
        "narrateur|Le sac, la serviette, et la pièce.",
        "maman|Tu prends quoi d'abord, Amir ?",
    )
    profiles["CHK_T0001_P0000"] = "choice"
    extras["CHK_T0001_P0000"] = t3lab("le sac", "la serviette", "la pièce")

    t2_sons = {1: "four,souffle", 2: "pas,foule", 3: "bois,pigeon"}
    t2_emph = {1: "four", 2: "file", 3: "banc"}
    t3_emph = {
        1: {1: "grain de sésame", 2: "grain de sésame", 3: "grain de sésame"},
        2: {1: "grain de sésame", 2: "grain de sésame", 3: "grain de sésame"},
        3: {1: "grain de sésame", 2: "grain de sésame", 3: "grain de sésame"},
    }
    t3_sons = {
        (1, 1): "four,silence",
        (1, 2): "pas,four",
        (1, 3): "farine,sac",
        (2, 1): "pas,silence",
        (2, 2): "caisse,pas",
        (2, 3): "pas,tissu",
        (3, 1): "pigeon,bois",
        (3, 2): "bois,silence",
        (3, 3): "toile,ombre",
    }

    for t1 in (1, 2, 3):
        meta = OBJ[t1]
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
        emph[cid] = "grain de sésame"

        t2q = f"{base}_T0002_P0000"
        scripts[t2q] = t2_question(t1)
        profiles[t2q] = "choice"
        extras[t2q] = t3lab("le four", "la file", "le banc")

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
                sons[fin] = "pain,porte"
                profiles[fin] = "ending"
                emph[fin] = "grain de sésame"

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
    lasts = [c["script"].splitlines()[-1] for c in fins]
    if len(set(lasts)) != 27:
        raise SystemExit("dernières lignes de fin non distinctes")
    for c in fins:
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{c['chunk_id']} fin mécanique: {last}")

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
    if "amir" not in blob or "chouchou" not in blob:
        raise SystemExit(f"{SID}: Amir/Chouchou absents")
    for bad in ("déjà", "encore", "tout doux", "tout calme"):
        if bad in blob:
            raise SystemExit(f"{SID} tic corpus: {bad}")
    if "grain de sésame" not in blob:
        raise SystemExit(f"{SID}: indice grain de sésame absent")
    if not all(c.get("text_xai_tags") for c in out["chunks"]):
        raise SystemExit(f"{SID}: text_xai_tags manquant")
    if not all(c.get("notes") for c in out["chunks"]):
        raise SystemExit(f"{SID}: notes manquant")
    if not all(c.get("text_ssml", "").startswith("<speak>") for c in out["chunks"]):
        raise SystemExit(f"{SID}: text_ssml incomplet")

    pw = [path_words(by, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    if min(pw) < 550:
        raise SystemExit(f"{SID}: chemin trop court ({min(pw)})")
    if max(pw) > 780:
        raise SystemExit(f"{SID}: chemin trop long ({max(pw)})")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"chemins {min(pw)}–{max(pw)} mots")


def main() -> None:
    write_tree()
    relecture(
        SID,
        TITLE,
        "La porte du four claque comme une bouche. La soupe attend à la maison, "
        "sans pain. Amir veut le pain rond du marché, bien chaud, pour Chouchou. "
        "Indice : un grain de sésame collé au sac, vu dès l'ouverture, payé au climax. "
        "T1 = sac / serviette / pièce (les trois partent). "
        "T2 = four trop fort (boîte de sésame vide) / file trop vite (personne à la caisse) / "
        "banc trop agité (pain absent, pigeon). Amir fonce, ça rate. Il refuse de foncer. "
        "T3 = neuf manières (attendre, reculer, derrière la farine ; son tour, le bord, "
        "répéter ; pigeon, s'asseoir, l'ombre). Le grain guide. 27 fins distinctes. "
        "Leçon DIF.BES.001 vécue : attendre, observer, laisser du temps, sans la dire. "
        "Amir propose, Chouchou prend son temps, silence = réponse.",
        "F-NAR-019 example4 v2. N1 ≤ 10. 86 chunks, 27 fins distinctes, chemins 590–620 mots. "
        "Ouverture porte-bouche + soupe sans pain, pas gabarit. "
        "Tics encore/déjà/tout doux/tout calme jetés. COL-017 (virgule farine, escargot, école), "
        "DIF-008 (store, stand), AUT-045 (panier d'osier) évités. Merci de papa (regarder Chouchou). "
        "TTS par chunk (notes+ssml+xai+piper). chunk_id / graphe / labels inchangés. Pas apply. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
