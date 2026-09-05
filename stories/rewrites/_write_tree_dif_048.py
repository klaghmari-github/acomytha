#!/usr/bin/env python3
"""TREE-DIF-048 — L'étoile de papier de Mila, à la fenêtre (N3, DIF.BES.001, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "TREE-DIF-048"
LIM = LIMITS["N3"]
TITLE = "L'étoile de papier de Mila, à la fenêtre"
FIL = (
    "Le carreau du dernier soleil chauffe. Mila veut accrocher son étoile de papier "
    "avant que le carré parte vers l'évier. Un brin de safran colle à une pointe. "
    "Elle prend d'abord l'étoile, le ruban ou la pince ; les trois viennent. "
    "Papa veut fermer, le vent veut partir, le rideau veut cacher, le rebord est plein. "
    "Elle fonce, ça rate. Elle refuse de foncer. Le brin guide. L'étoile reste."
)
CHARS = "Mila, papa, maman"
SETTING = "près de la fenêtre, cuisine au soleil bas"

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=500, sentence=260, energy="warm", contour="storytelling",
        noise=0.36, emphasis="brin de safran",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le soleil bas va partir; tempo=naturel; sourire=léger; respiration=ample",
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
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde ce qu elle a pris; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=450, sentence=280, energy="bright", contour="falling",
        noise=0.34, emphasis="brin de safran",
        note="arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les trois affaires viennent; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=420, sentence=250, energy="lively", contour="dynamic",
        noise=0.37, emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=elle se presse vers le carreau; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0,
        pause=520, sentence=300, energy="tense", contour="dynamic",
        noise=0.34, emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=le lieu refuse au même moment; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=560, sentence=270, energy="bright", contour="falling",
        noise=0.35, emphasis="brin de safran",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=elle refuse de foncer, le brin guide; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3,
        pause=900, sentence=340, energy="calm", contour="falling",
        noise=0.31, emphasis="brin de safran",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le brin de safran paie le début; tempo=posé; sourire=léger; respiration=ample",
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
    "balcon",
    "veau",
    "étable",
    "abreuvoir",
    "le four",
    "marché",
    "fort de coussins",
    "étoile brune",
    "ancre minuscule",
    "fil pâle",
    "virgule d'or",
    "œillet de cuivre",
    "perle de verre",
    "virgule de buée",
    "bouton de nacre",
    "nœud de raphia",
    "pois ivoire",
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
        "lab": "l'étoile",
        "ans": "étoile",
        "acc": "étoile | l'étoile | d'abord l'étoile | le papier",
        "retry": "Mila prend l'étoile d'abord.",
        "emph": "étoile",
        "sons": "papier,pli",
        "coda": "L'étoile sèche près du savon, un pli au coin.",
    },
    2: {
        "lab": "le ruban",
        "ans": "ruban",
        "acc": "ruban | le ruban | d'abord le ruban | le collant",
        "retry": "Mila prend le ruban d'abord.",
        "emph": "ruban",
        "sons": "ruban,colle",
        "coda": "Un bout de ruban reste enroulé, collant.",
    },
    3: {
        "lab": "la pince",
        "ans": "pince",
        "acc": "pince | la pince | d'abord la pince | le bois",
        "retry": "Mila prend la pince d'abord.",
        "emph": "pince",
        "sons": "bois,clic",
        "coda": "La pince garde un fil jaune, près du rebord.",
    },
}

T3_LABS = {
    1: ("attendre le vent", "plus bas", "la fente"),
    2: ("écarter", "attendre", "devant"),
    3: ("de la place", "au milieu", "contre le bois"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Mila prend l'étoile, le papier craque.",
            "enfant-f|Elle va briller à la vitre.",
            "maman|Tiens-la à plat, Mila.",
            "narrateur|Une pointe se relève, puis retombe.",
            "narrateur|Ce brin de safran reste collé, mince.",
            "narrateur|Ses joues chauffent, et elle serre trop.",
            "enfant-f|Vite, avant qu'il parte !",
            "papa|Le ruban aussi, près de toi.",
            "narrateur|Maman glisse la pince contre l'étoile.",
            "narrateur|Étoile, ruban et pince avancent avec elle.",
            "enfant-f|J'arrive, petit soleil.",
            "narrateur|Le papier sent la colle, un peu.",
            "papa|L'étoile d'abord, vous l'avez.",
        )
    if t1 == 2:
        return L(
            "narrateur|Mila prend le ruban, collant au pouce.",
            "enfant-f|Il va tenir l'étoile.",
            "papa|Déroule un peu, pas trop vite.",
            "narrateur|Un bout se colle, puis lâche.",
            "narrateur|Ses doigts collent, et ça la chatouille.",
            "enfant-f|Vite, avant qu'il parte !",
            "maman|L'étoile, ensuite, près de toi.",
            "narrateur|Papa pose la pince contre le rebord.",
            "narrateur|Elle emporte les trois, contre elle.",
            "enfant-f|Tu vas la garder, ruban.",
            "narrateur|Le collant frotte sa manche, un peu.",
            "narrateur|Sur l'étoile, le brin de safran reste.",
            "maman|Le ruban d'abord, il est prêt.",
        )
    return L(
        "narrateur|Mila prend la pince, le bois tiède.",
        "enfant-f|Elle va pincer le cadre.",
        "maman|Ouvre-la, sans claquer.",
        "narrateur|Les deux branches claquent, puis se taisent.",
        "narrateur|Sa paume chauffe autour du bois.",
        "enfant-f|Vite, avant qu'il parte !",
        "papa|L'étoile et le ruban, avec vous.",
        "narrateur|Il les pose près de l'évier.",
        "narrateur|Rien ne reste près de la table.",
        "enfant-f|Je te mets au bois.",
        "narrateur|Un fil jaune reste coincé dedans.",
        "narrateur|Ce brin de safran brille, sur l'étoile.",
        "papa|La pince d'abord, elle est prête.",
    )


def t1_q(t1: int) -> list[str]:
    o = OBJ[t1]
    return L(
        f"narrateur|Mila a pris {o['lab']} d'abord.",
        "maman|Elle a pris quoi, d'abord ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|L'étoile tient contre sa poitrine, chaude.",
            "enfant-f|Elle va à la vitre.",
            "maman|Le soleil n'attendra pas longtemps.",
            "papa|On y va, Mila ?",
            "enfant-f|Oui, papa.",
            "narrateur|Ce brin de safran brille, sur une pointe.",
            "narrateur|Un coin du papier cherche le soleil.",
            "maman|Vos mains sont prêtes.",
        )
    if t1 == 2:
        return L(
            "narrateur|Le ruban fait un bracelet lâche, au poignet.",
            "enfant-f|Il va coller l'étoile.",
            "papa|Le collant sent le papier.",
            "maman|Vos mains sont prêtes ?",
            "enfant-f|Oui, maman.",
            "narrateur|Un bout se décolle, puis se tait.",
            "narrateur|Ce brin de safran reste visible, mince.",
            "papa|On avance vers le carreau.",
        )
    return L(
        "narrateur|La pince reste fermée, contre son pouce.",
        "enfant-f|Elle va tenir le cadre.",
        "maman|Le bois sent le soleil.",
        "papa|On y va, tous les trois ?",
        "enfant-f|Oui.",
        "narrateur|Les deux branches attendent le bois.",
        "narrateur|Ce brin de safran brille, sur l'étoile.",
        "maman|Le cadre est là, devant.",
    )


def t2_question(t1: int) -> list[str]:
    head = {
        1: "L'étoile tape sa poitrine, bas.",
        2: "Le ruban frotte sa manche, un peu collant.",
        3: "La pince tape le pouce, légère.",
    }[t1]
    return L(
        f"narrateur|{head}",
        "narrateur|La vitre ouverte souffle, trop fort.",
        "narrateur|Plus loin, le rideau claque.",
        "narrateur|Sur le rebord, trop d'objets se touchent.",
        "papa|Mila, vous partez où ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        extra = {
            1: "Le papier se plie, trop vite, trop fort.",
            2: "Le ruban claque comme un fil, trop vif.",
            3: "La pince glisse, trop légère dans l'air.",
        }[t1]
        hip = {
            1: "Entre ses doigts, le papier jaune craque.",
            2: "Au poignet, le ruban colle, puis lâche.",
            3: "Dans sa paume, le bois de la pince est tiède.",
        }[t1]
        return L(
            f"narrateur|{hip}",
            "narrateur|Mila pousse le carreau, trop vite.",
            "narrateur|L'air de la rue entre, trop vif.",
            f"narrateur|{extra}",
            "enfant-f|Mon étoile s'envole !",
            "narrateur|Un souffle pousse le carreau, fort.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Elle veut recoller tout de suite, trop vite.",
            "narrateur|Dans sa poitrine, ça tape trop fort.",
            "papa|Ça souffle trop, ici.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "maman|Regarde le verre, Mila.",
            "enfant-f|On fait comment, alors ?",
            "papa|Tu trouves, Mila ?",
            "narrateur|Personne ne dit la place.",
        )
    if t2 == 2:
        extra = {
            1: "Le papier disparaît un instant, trop caché.",
            2: "Le ruban s'accroche au tissu, trop serré.",
            3: "La pince tire le rideau, trop fort.",
        }[t1]
        hip = {
            1: "Contre elle, l'étoile n'a plus de lumière.",
            2: "Sa manche tire vers le tissu, collée.",
            3: "La pince pince le rideau, par erreur.",
        }[t1]
        return L(
            f"narrateur|{hip}",
            "narrateur|Mila tire le rideau, d'un coup.",
            "narrateur|Le tissu sent la poussière, chaude.",
            f"narrateur|{extra}",
            "enfant-f|Le soleil est parti !",
            "narrateur|Le tissu va, puis revient, agité.",
            "narrateur|Le sourire de Mila disparaît.",
            "narrateur|Elle veut tirer plus fort, trop vite.",
            "narrateur|Dans sa poitrine, l'envie se serre.",
            "papa|Le rideau n'a pas fini.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Écoute le tissu, Mila.",
            "enfant-f|On fait comment, alors ?",
            "maman|Tu trouves, Mila ?",
            "narrateur|Personne ne tire à sa place.",
        )
    extra = {
        1: "L'étoile glisse entre une cuillère et le savon.",
        2: "Le ruban colle une miette, trop sale.",
        3: "La pince n'a plus de bois libre, trop plein.",
    }[t1]
    hip = {
        1: "Le papier touche le savon, puis recule.",
        2: "Une miette colle au ruban, grise.",
        3: "Les deux branches claquent sur la cuillère.",
    }[t1]
    return L(
        f"narrateur|{hip}",
        "narrateur|Mila pose trop vite, sur le rebord.",
        "narrateur|Le rebord est trop plein, trop étroit.",
        f"narrateur|{extra}",
        "enfant-f|Ça tombe tout le temps.",
        "narrateur|Une cuillère tinte, trop bruyante.",
        "narrateur|Le sourire de Mila disparaît.",
        "narrateur|Elle veut empiler, trop vite.",
        "narrateur|Dans sa poitrine, ça se bouscule.",
        "papa|Ça tape trop, ici.",
        "narrateur|Papa s'accroupit, près du bois.",
        "maman|Regarde la place, Mila.",
        "enfant-f|On fait comment, alors ?",
        "papa|Tu trouves, Mila ?",
        "narrateur|Personne ne range à sa place.",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|La vitre souffle, trop vive.",
            "papa|Attendre le vent, plus bas, ou la fente ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Le rideau claque, trop fort.",
            "maman|Écarter, attendre, ou devant ?",
        )
    return L(
        "narrateur|Le rebord tape, trop plein.",
        "papa|De la place, au milieu, ou contre le bois ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    safran = {
        1: "Sur une pointe, le brin de safran brille.",
        2: "Près du ruban, le brin de safran reste collé.",
        3: "Près de la pince, le brin de safran tremble.",
    }[t1]
    hold = {
        1: "Elle tient l'étoile contre elle, sans coller.",
        2: "Elle tient le ruban, sans le dérouler.",
        3: "Elle tient la pince fermée, sans pincer.",
    }[t1]
    if t2 == 1 and t3 == 1:
        wait = {
            1: "Pendant ce temps, l'étoile reste plate, sage.",
            2: "Enroulé, le ruban attend contre sa manche.",
            3: "Fermée, la pince reste contre son pouce.",
        }[t1]
        return L(
            "enfant-f|On attend le vent.",
            f"narrateur|{hold}",
            "narrateur|Un second souffle arrive, plus malin.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle regarde l'étoile, puis le carreau.",
            f"narrateur|{safran}",
            "enfant-f|Cette pointe, vers le soleil.",
            f"narrateur|{wait}",
            "narrateur|Le souffle passe, une fois, puis plus.",
            "papa|Le vent s'est tu, maintenant.",
            "narrateur|Le papier redevient plat.",
            "maman|Tu lui as laissé le temps.",
            "enfant-f|Tu peux rester.",
        )
    if t2 == 1 and t3 == 2:
        low = {
            1: "Elle pose l'étoile plus bas, loin du souffle.",
            2: "Elle colle le ruban plus bas, loin du souffle.",
            3: "Elle pince plus bas, loin du souffle.",
        }[t1]
        use = {
            1: "Un coin du papier cherche le soleil.",
            2: "Un bout du ruban brille, prêt à tenir.",
            3: "Les deux branches attendent le bois.",
        }[t1]
        return L(
            "enfant-f|Plus bas, d'abord.",
            "narrateur|Un second souffle rase le haut du carreau.",
            "narrateur|Mila refuse de foncer, en haut.",
            "narrateur|Elle s'accroupit, les genoux au carreau.",
            f"narrateur|{low}",
            "narrateur|L'air est plus doux, près du bois.",
            f"narrateur|{safran}",
            "enfant-f|Cette pointe, vers le soleil.",
            f"narrateur|{use}",
            "papa|Tu as regardé d'abord.",
            "enfant-f|Ici, tu ne voles plus.",
            "maman|Le bas était plus calme.",
        )
    if t2 == 1 and t3 == 3:
        crack = {
            1: "Elle glisse l'étoile dans la fente du cadre.",
            2: "Elle pousse le ruban dans la fente du cadre.",
            3: "Elle pince la fente du cadre, sans forcer.",
        }[t1]
        wait = {
            1: "Pendant ce temps, l'étoile reste plate, sage.",
            2: "Enroulé, le ruban attend contre sa manche.",
            3: "Fermée, la pince reste contre son pouce.",
        }[t1]
        return L(
            "enfant-f|Dans la fente, tout petit.",
            "narrateur|Un second souffle cherche l'ouverture.",
            "narrateur|Mila refuse d'ouvrir trop grand.",
            f"narrateur|{crack}",
            "narrateur|Le bois tient, sans laisser le vent.",
            f"narrateur|{safran}",
            "enfant-f|Cette pointe, vers le soleil.",
            f"narrateur|{wait}",
            "papa|La fente n'a pas soufflé.",
            "enfant-f|Tu es à l'abri.",
            "maman|Tu as parlé lentement.",
            "narrateur|Le carreau se tait, près du bois.",
        )
    if t2 == 2 and t3 == 1:
        draw = {
            1: "Derrière le tissu, l'étoile revoit le soleil.",
            2: "Derrière le tissu, le ruban ne s'accroche plus.",
            3: "Derrière le tissu, la pince ne tire plus.",
        }[t1]
        wait = {
            1: "Pendant ce temps, l'étoile reste plate, sage.",
            2: "Enroulé, le ruban attend contre sa manche.",
            3: "Fermée, la pince reste contre son pouce.",
        }[t1]
        return L(
            "enfant-f|J'écarte, un doigt seulement.",
            "narrateur|Le tissu veut revenir, plus malin.",
            "narrateur|Mila refuse de tirer trop fort.",
            "narrateur|Elle écarte le rideau, un doigt.",
            f"narrateur|{draw}",
            "narrateur|Le tissu s'arrête, puis se tait.",
            f"narrateur|{safran}",
            "enfant-f|Cette pointe, vers le soleil.",
            f"narrateur|{wait}",
            "maman|Le soleil est revenu, comme un carré.",
            "enfant-f|Maintenant, tu me vois.",
            "papa|Tu as attendu le silence.",
        )
    if t2 == 2 and t3 == 2:
        still = {
            1: "Elle pose l'étoile, puis attend le tissu.",
            2: "Elle pose le ruban, puis attend le tissu.",
            3: "Elle pose la pince, puis attend le tissu.",
        }[t1]
        use = {
            1: "Un coin du papier cherche le soleil.",
            2: "Un bout du ruban brille, prêt à tenir.",
            3: "Les deux branches attendent le bois.",
        }[t1]
        return L(
            "enfant-f|On attend qu'il retombe.",
            f"narrateur|{still}",
            "narrateur|Le rideau va, revient, plus rusé.",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle écoute le tissu, sans tirer.",
            "narrateur|Le rideau s'arrête, enfin.",
            "narrateur|Le soleil redevient un seul carré, net.",
            f"narrateur|{safran}",
            "enfant-f|Cette pointe, vers le soleil.",
            f"narrateur|{use}",
            "papa|Tu n'as pas tiré trop fort.",
            "enfant-f|C'est pour toi.",
            "maman|Tu as laissé le tissu parler.",
        )
    if t2 == 2 and t3 == 3:
        front = {
            1: "Devant le tissu, l'étoile touche le verre.",
            2: "Devant le tissu, le ruban colle le verre.",
            3: "Devant le tissu, la pince prend le cadre.",
        }[t1]
        wait = {
            1: "Pendant ce temps, l'étoile reste plate, sage.",
            2: "Enroulé, le ruban attend contre sa manche.",
            3: "Fermée, la pince reste contre son pouce.",
        }[t1]
        return L(
            "enfant-f|Devant, tout contre la vitre.",
            "narrateur|Le rideau claque derrière, jaloux.",
            "narrateur|Mila refuse de lutter contre le tissu.",
            "narrateur|Elle se glisse entre le rideau et le carreau.",
            f"narrateur|{front}",
            "narrateur|Le tissu reste derrière, sans cacher.",
            f"narrateur|{safran}",
            "enfant-f|Cette pointe, vers le soleil.",
            f"narrateur|{wait}",
            "papa|Tu t'es mise devant, contre le verre.",
            "enfant-f|Le soleil est là.",
            "maman|Tu as observé d'abord.",
        )
    if t2 == 3 and t3 == 1:
        room = {
            1: "Elle pose l'étoile, puis pousse la cuillère.",
            2: "Elle pose le ruban, puis pousse la cuillère.",
            3: "Elle pose la pince, puis pousse la cuillère.",
        }[t1]
        wait = {
            1: "Pendant ce temps, l'étoile reste plate, sage.",
            2: "Enroulé, le ruban attend contre sa manche.",
            3: "Fermée, la pince reste contre son pouce.",
        }[t1]
        return L(
            "enfant-f|On fait de la place, d'abord.",
            f"narrateur|{room}",
            "narrateur|L'assiette de poire veut revenir, rusée.",
            "narrateur|Mila refuse d'empiler.",
            "narrateur|Elle attend que le bois soit large.",
            "narrateur|La cuillère glisse, puis se tait.",
            "narrateur|Le savon recule, le bois redevient large.",
            f"narrateur|{safran}",
            "enfant-f|Cette pointe, vers le soleil.",
            f"narrateur|{wait}",
            "papa|Le rebord n'a plus tapé.",
            "enfant-f|Maintenant, tu peux rester.",
            "maman|Tu as préparé le chemin.",
        )
    if t2 == 3 and t3 == 2:
        mid = {
            1: "Au milieu, l'étoile tient, loin des bords.",
            2: "Au milieu, le ruban colle, loin des miettes.",
            3: "Au milieu, la pince trouve un bois libre.",
        }[t1]
        use = {
            1: "Un coin du papier cherche le soleil.",
            2: "Un bout du ruban brille, prêt à tenir.",
            3: "Les deux branches attendent le bois.",
        }[t1]
        return L(
            "enfant-f|Au milieu, pas trop près.",
            "narrateur|Les bords veulent tout prendre, rusés.",
            "narrateur|Mila refuse de se coller au savon.",
            f"narrateur|{mid}",
            "narrateur|Elle pose, puis compte un peu, bas.",
            "narrateur|Rien ne tinte, rien ne glisse plus.",
            f"narrateur|{safran}",
            "enfant-f|Cette pointe, vers le soleil.",
            f"narrateur|{use}",
            "papa|Tu n'as pas empilé.",
            "enfant-f|Tu es droite, maintenant.",
            "maman|Le milieu était assez large.",
        )
    wood = {
        1: "Contre le bois, l'étoile ne glisse plus.",
        2: "Contre le bois, le ruban tient le cadre.",
        3: "Contre le bois, la pince ferme sans bruit.",
    }[t1]
    wait = {
        1: "Pendant ce temps, l'étoile reste plate, sage.",
        2: "Enroulé, le ruban attend contre sa manche.",
        3: "Fermée, la pince reste contre son pouce.",
    }[t1]
    return L(
        "enfant-f|Contre le bois, bien serré.",
        "narrateur|Le savon veut toucher, rusé.",
        "narrateur|Mila refuse de poser sur le tas.",
        f"narrateur|{wood}",
        "narrateur|Elle pince le cadre, sans toucher le savon.",
        "narrateur|Le rebord se tait, plus loin, seul.",
        f"narrateur|{safran}",
        "enfant-f|Cette pointe, vers le soleil.",
        f"narrateur|{wait}",
        "papa|Le bois était assez large.",
        "enfant-f|Tu restes, étoile.",
        "maman|Le bord tenait assez.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    coda = OBJ[t1]["coda"]
    table = {
        (1, 1, 1): L(
            "narrateur|L'étoile brille, plate, dans le dernier soleil.",
            "enfant-f|On a attendu le vent.",
            "papa|Tu raconteras aussi le moment difficile ?",
            "enfant-f|Surtout celui-là.",
            "maman|Rentrez, la poire sent bon.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran garde un peu de soleil.",
            "narrateur|Une poussière s'arrête dans le rayon, puis plus.",
        ),
        (2, 1, 1): L(
            "narrateur|L'étoile brille, tenue par le ruban, plate.",
            "enfant-f|On a attendu le vent.",
            "papa|Tu raconteras aussi le moment difficile ?",
            "enfant-f|Surtout celui-là.",
            "maman|Rentrez, la poire sent bon.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran reste collé au ruban.",
            "narrateur|Un bout de ruban brille, collé au verre.",
        ),
        (3, 1, 1): L(
            "narrateur|L'étoile brille, pincée, dans le dernier soleil.",
            "enfant-f|On a attendu le vent.",
            "papa|Tu raconteras aussi le moment difficile ?",
            "enfant-f|Surtout celui-là.",
            "maman|Rentrez, la poire sent bon.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran passe sous la pince.",
            "narrateur|La pince garde un fil jaune, près du brin.",
        ),
        (1, 1, 2): L(
            "narrateur|Plus bas, l'étoile garde tout le jaune.",
            "enfant-f|On s'est baissées, d'abord.",
            "papa|Tu as regardé avant de coller.",
            "maman|Essuie tes genoux, sur le paillasson.",
            "enfant-f|Ça a failli s'envoler.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran pointe vers l'évier.",
            "narrateur|Un carré de soleil reste au bas du carreau.",
        ),
        (2, 1, 2): L(
            "narrateur|Plus bas, le ruban tient l'étoile, jaune.",
            "enfant-f|On s'est baissées, d'abord.",
            "papa|Tu as regardé avant de coller.",
            "maman|Essuie tes genoux, sur le paillasson.",
            "enfant-f|Ça a failli s'envoler.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran descend avec le ruban.",
            "narrateur|Plus bas, le collant a séché, net.",
        ),
        (3, 1, 2): L(
            "narrateur|Plus bas, la pince tient l'étoile, jaune.",
            "enfant-f|On s'est baissées, d'abord.",
            "papa|Tu as regardé avant de coller.",
            "maman|Essuie tes genoux, sur le paillasson.",
            "enfant-f|Ça a failli s'envoler.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran reste près du bois bas.",
            "narrateur|Plus bas, les deux branches tiennent le bois.",
        ),
        (1, 1, 3): L(
            "narrateur|Dans la fente, l'étoile ne tremble plus.",
            "enfant-f|Je n'ai pas ouvert trop grand.",
            "papa|La fente n'a pas soufflé.",
            "maman|Le bois est retombé, plus loin.",
            "enfant-f|Le vent a failli la prendre.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran se cache un peu, à l'abri.",
            "narrateur|La rue se tait, derrière le verre tiède.",
        ),
        (2, 1, 3): L(
            "narrateur|Dans la fente, le ruban tient sans bouger.",
            "enfant-f|Je n'ai pas ouvert trop grand.",
            "papa|La fente n'a pas soufflé.",
            "maman|Le bois est retombé, plus loin.",
            "enfant-f|Le vent a failli la prendre.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran glisse dans la fente.",
            "narrateur|Dans la fente, le ruban tient sans bouger.",
        ),
        (3, 1, 3): L(
            "narrateur|Dans la fente, la pince tient le cadre.",
            "enfant-f|Je n'ai pas ouvert trop grand.",
            "papa|La fente n'a pas soufflé.",
            "maman|Le bois est retombé, plus loin.",
            "enfant-f|Le vent a failli la prendre.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran s'abrite sous le bois.",
            "narrateur|Dans la fente, la pince ne claque plus.",
        ),
        (1, 2, 1): L(
            "narrateur|Derrière le rideau, l'étoile a repris le soleil.",
            "enfant-f|On a écarté, un doigt.",
            "papa|Le silence vous a aidées.",
            "maman|Le tissu sent la poussière chaude.",
            "enfant-f|Ça a failli rester noir.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran revoit le carré de soleil.",
            "narrateur|Un pli du rideau se recouche, lent.",
        ),
        (2, 2, 1): L(
            "narrateur|Derrière le rideau, le ruban ne s'accroche plus.",
            "enfant-f|On a écarté, un doigt.",
            "papa|Le silence vous a aidées.",
            "maman|Le tissu sent la poussière chaude.",
            "enfant-f|Ça a failli rester noir.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran se détache du tissu.",
            "narrateur|Enfin, le tissu a lâché le ruban.",
        ),
        (3, 2, 1): L(
            "narrateur|Derrière le rideau, la pince ne tire plus.",
            "enfant-f|On a écarté, un doigt.",
            "papa|Le silence vous a aidées.",
            "maman|Le tissu sent la poussière chaude.",
            "enfant-f|Ça a failli rester noir.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran reparaît, hors du tissu.",
            "narrateur|Derrière le rideau, la pince ne tire plus.",
        ),
        (1, 2, 2): L(
            "narrateur|Quand le tissu s'est tu, l'étoile a brillé.",
            "enfant-f|On a attendu qu'il retombe.",
            "papa|Tu n'as pas tiré trop fort.",
            "maman|Le soleil a parlé tout seul.",
            "enfant-f|Ça a failli rester caché.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran attend le carré, net.",
            "narrateur|Un carré net pâlit sur le mur.",
        ),
        (2, 2, 2): L(
            "narrateur|Quand le tissu s'est tu, le ruban a collé.",
            "enfant-f|On a attendu qu'il retombe.",
            "papa|Tu n'as pas tiré trop fort.",
            "maman|Le soleil a parlé tout seul.",
            "enfant-f|Ça a failli rester caché.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran s'allonge sur le ruban.",
            "narrateur|Plat, le ruban attend contre le carreau.",
        ),
        (3, 2, 2): L(
            "narrateur|Quand le tissu s'est tu, la pince a pincé.",
            "enfant-f|On a attendu qu'il retombe.",
            "papa|Tu n'as pas tiré trop fort.",
            "maman|Le soleil a parlé tout seul.",
            "enfant-f|Ça a failli rester caché.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran tient sous la pince, net.",
            "narrateur|Quand le tissu s'est tu, la pince a pincé.",
        ),
        (1, 2, 3): L(
            "narrateur|Devant le tissu, l'étoile touche le verre chaud.",
            "enfant-f|Je me suis mise devant.",
            "papa|Tu t'es glissée, comme la lumière.",
            "maman|Vous rentrez, les mains pleines de soleil.",
            "enfant-f|Le rideau a failli tout cacher.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran colle au verre, chaud.",
            "narrateur|Derrière, le rideau ne cache plus.",
        ),
        (2, 2, 3): L(
            "narrateur|Devant le tissu, le ruban colle le verre chaud.",
            "enfant-f|Je me suis mise devant.",
            "papa|Tu t'es glissée, comme la lumière.",
            "maman|Vous rentrez, les mains pleines de soleil.",
            "enfant-f|Le rideau a failli tout cacher.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran se plaque au verre.",
            "narrateur|Devant le tissu, le ruban colle le verre.",
        ),
        (3, 2, 3): L(
            "narrateur|Devant le tissu, la pince prend le cadre chaud.",
            "enfant-f|Je me suis mise devant.",
            "papa|Tu t'es glissée, comme la lumière.",
            "maman|Vous rentrez, les mains pleines de soleil.",
            "enfant-f|Le rideau a failli tout cacher.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran reste hors du rideau.",
            "narrateur|Devant le tissu, la pince prend le cadre.",
        ),
        (1, 3, 1): L(
            "narrateur|Quand la cuillère s'est tue, l'étoile a tenu.",
            "enfant-f|On a fait de la place.",
            "papa|Le rebord n'a plus tapé.",
            "maman|Vos manches sentent le savon.",
            "enfant-f|Ça a failli tout faire tomber.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran a de la place, enfin.",
            "narrateur|Une miette sèche sur le bois, puis plus.",
        ),
        (2, 3, 1): L(
            "narrateur|Quand la cuillère s'est tue, le ruban a tenu.",
            "enfant-f|On a fait de la place.",
            "papa|Le rebord n'a plus tapé.",
            "maman|Vos manches sentent le savon.",
            "enfant-f|Ça a failli tout faire tomber.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran n'a plus de miette.",
            "narrateur|La cuillère a laissé le ruban tranquille.",
        ),
        (3, 3, 1): L(
            "narrateur|Quand la cuillère s'est tue, la pince a tenu.",
            "enfant-f|On a fait de la place.",
            "papa|Le rebord n'a plus tapé.",
            "maman|Vos manches sentent le savon.",
            "enfant-f|Ça a failli tout faire tomber.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran a un bois libre.",
            "narrateur|La cuillère a reculé, la pince a tenu.",
        ),
        (1, 3, 2): L(
            "narrateur|Au milieu, l'étoile reste droite, calme.",
            "enfant-f|On n'est pas allées trop près.",
            "papa|Tu n'as pas empilé.",
            "maman|Tes doigts sentent le papier.",
            "enfant-f|Les bords ont failli la prendre.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran tient au centre du carré.",
            "narrateur|Plus loin, le savon reste à sa place.",
        ),
        (2, 3, 2): L(
            "narrateur|Au milieu, le ruban colle droit, calme.",
            "enfant-f|On n'est pas allées trop près.",
            "papa|Tu n'as pas empilé.",
            "maman|Tes doigts sentent le papier.",
            "enfant-f|Les bords ont failli la prendre.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran évite les miettes.",
            "narrateur|Au milieu, le ruban ne touche plus les miettes.",
        ),
        (3, 3, 2): L(
            "narrateur|Au milieu, la pince trouve un bois libre.",
            "enfant-f|On n'est pas allées trop près.",
            "papa|Tu n'as pas empilé.",
            "maman|Tes doigts sentent le papier.",
            "enfant-f|Les bords ont failli la prendre.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran tient au milieu, net.",
            "narrateur|Au milieu, la pince trouve un bois libre.",
        ),
        (1, 3, 3): L(
            "narrateur|Contre le bois, l'étoile tient, jaune.",
            "enfant-f|On a pincé le cadre.",
            "papa|Le bois était assez large.",
            "maman|Rentrez, la poire est coupée.",
            "enfant-f|Le tas a failli tout faire glisser.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran s'appuie contre le cadre.",
            "narrateur|Plus loin, le rebord se tait, seul.",
        ),
        (2, 3, 3): L(
            "narrateur|Contre le bois, le ruban tient le cadre, jaune.",
            "enfant-f|On a pincé le cadre.",
            "papa|Le bois était assez large.",
            "maman|Rentrez, la poire est coupée.",
            "enfant-f|Le tas a failli tout faire glisser.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran se cale contre le bois.",
            "narrateur|Contre le bois, le ruban tient le cadre.",
        ),
        (3, 3, 3): L(
            "narrateur|Contre le bois, la pince ferme sans bruit.",
            "enfant-f|On a pincé le cadre.",
            "papa|Le bois était assez large.",
            "maman|Rentrez, la poire est coupée.",
            "enfant-f|Le tas a failli tout faire glisser.",
            f"narrateur|{coda}",
            "narrateur|Ce brin de safran reste pincé, visible.",
            "narrateur|Contre le bois, la pince ferme sans bruit.",
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
        "narrateur|La vitre de la cuisine chauffe la paume de Mila.",
        "narrateur|Un carré de soleil marche vers l'évier, lent.",
        "narrateur|Le carreau du dernier soleil tient la chaleur.",
        "narrateur|La cuisine sent la poire, et un peu le savon.",
        "narrateur|Des pépins brillent dans le jus, sur la planche.",
        "narrateur|Sur la table, une étoile de papier attend, jaune.",
        "narrateur|Un brin de safran colle à une pointe, mince.",
        "papa|Tu as vu ce brin, Mila ?",
        "enfant-f|Il brille, comme un cheveu orange.",
        "maman|C'est collé depuis le pliage.",
        "papa|J'ai presque fini la poire.",
        "maman|J'essuie le rebord, pour les fruits.",
        "narrateur|En ce moment, Mila serre l'étoile contre elle.",
        "enfant-f|Je veux l'accrocher, avant que le soleil parte.",
        "papa|Moi, je ferme, le courant touche la poire.",
        "narrateur|Le sourire de Mila disparaît, un instant.",
        "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
        "maman|On prend les affaires, alors ?",
        "papa|Merci, tu as gardé l'étoile loin des fruits.",
    )
    sons["CHK_T0000_P0000"] = "vitre,poire,papier"
    profiles["CHK_T0000_P0000"] = "opening"
    emph["CHK_T0000_P0000"] = "brin de safran"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près du rebord.",
        "narrateur|L'étoile, le ruban, et la pince.",
        "maman|Tu prends quoi d'abord, Mila ?",
    )
    profiles["CHK_T0001_P0000"] = "choice"
    extras["CHK_T0001_P0000"] = t3lab("l'étoile", "le ruban", "la pince")

    t2_sons = {1: "vent,vitre", 2: "tissu,claque", 3: "cuillere,savon"}
    t2_emph = {1: "carreau", 2: "rideau", 3: "rebord"}
    t3_emph = {
        1: {1: "vent", 2: "plus bas", 3: "fente"},
        2: {1: "écarte", 2: "tissu", 3: "devant"},
        3: {1: "place", 2: "milieu", 3: "bois"},
    }
    t3_sons = {
        (1, 1): "vent,silence",
        (1, 2): "genoux,bois",
        (1, 3): "fente,cadre",
        (2, 1): "tissu,doigt",
        (2, 2): "tissu,silence",
        (2, 3): "verre,tissu",
        (3, 1): "cuillere,savon",
        (3, 2): "bois,milieu",
        (3, 3): "cadre,pince",
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
        emph[cid] = "brin de safran"

        t2q = f"{base}_T0002_P0000"
        scripts[t2q] = t2_question(t1)
        profiles[t2q] = "choice"
        extras[t2q] = t3lab("la vitre", "le rideau", "le rebord")

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
                sons[fin] = "soleil,papier"
                profiles[fin] = "ending"
                emph[fin] = "brin de safran"

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
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    for bad in ("déjà", "encore", "tout doux", "tout calme"):
        if bad in blob:
            raise SystemExit(f"{SID} tic corpus: {bad}")
    if "brin de safran" not in blob:
        raise SystemExit(f"{SID}: indice brin de safran absent")
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
        "Cuisine, carreau du dernier soleil, poire, savon. Mila veut accrocher "
        "son étoile de papier (ruban + pince) avant que le carré parte vers l'évier. "
        "Indice : un brin de safran collé à une pointe, vu dès l'ouverture, payé au climax. "
        "T1 = étoile / ruban / pince (les trois viennent). "
        "T2 = vitre trop venteuse / rideau trop agité / rebord trop plein. "
        "T3 = neuf manières (vent, plus bas, fente ; écarter, attendre, devant ; "
        "place, milieu, bois). Elle fonce, ça rate. Elle refuse de foncer. "
        "Le brin guide. 27 fins distinctes. Leçon DIF.BES.001 vécue : attendre, "
        "observer, laisser du temps, sans la dire.",
        "F-NAR-019 example4 v2. N3 ≤ 16. Ouverture paume sur vitre chaude, pas gabarit. "
        "Tics encore/déjà/tout doux/tout calme jetés. Kenzo, slogan, merle, miel, "
        "AUT-018 caisse, DIF-034 école jetés. Merci de papa (étoile loin des fruits). "
        "TTS par chunk (profiles example2). chunk_id inchangés. Pas apply. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
