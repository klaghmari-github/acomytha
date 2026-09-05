#!/usr/bin/env python3
"""TREE-COL-021 — La flaque et le ciré de Victorino (F-NAR-019, N1)."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, words  # noqa: E402

SID = "TREE-COL-021"
LIM = 10


def wc(s: str) -> int:
    return words(s)


def L(*rows: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = wc(ph)
        if n > LIM:
            raise SystemExit(f"{n}>{LIM}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"fin: {ph}")
        out.append((role, ph))
    return out


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp:
        e = esc(emp)
        i = body.lower().find(e.lower())
        if i >= 0:
            body = body[:i] + f'<emphasis level="moderate">{body[i:i+len(e)]}</emphasis>' + body[i + len(e) :]
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
        body = f'<{m["pitchTag"]}>{body}</{m["pitchTag"]}>'
    if m["pause"] >= 800:
        pause = "[long-pause]"
    elif m["pause"] >= 400:
        pause = "[pause]"
    else:
        pause = ""
    return f"{body} {pause}".strip()


PROFILES = {
    "opening": dict(
        rate="medium", wpm=128, speed=0.92, piper=1.18, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=300, energy="warm", contour="storytelling", noise=0.36,
        emphasis="ciré jaune",
        note="arc=installation; intention=émerveiller; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=la flaque attend et les mots se perdent; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=108, speed=0.82, piper=1.32, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=360, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=110, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=340, energy="focused", contour="rising", noise=0.32,
        emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=122, speed=0.90, piper=1.22, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=300, energy="bright", contour="falling", noise=0.34,
        emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=cette_fois_on_a_entendu; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=132, speed=0.96, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=280, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il_veut_partir_maintenant; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=120, speed=0.90, piper=1.20, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=320, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=les_voix_se_mêlent; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=126, speed=0.93, piper=1.16, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=300, energy="bright", contour="falling", noise=0.35,
        emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=la_solution_vient_de_l_attention; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=108, speed=0.82, piper=1.30, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=360, energy="calm", contour="falling", noise=0.31,
        emphasis=None,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_parole_a_trouvé_sa_place; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def voice(chunk: dict, ls: list[tuple[str, str]], profile: str, extra: dict | None = None) -> None:
    extra = extra or {}
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    text = " ".join(t for _, t in ls)
    script = "\n".join(f"{r}|{t}" for r, t in ls)
    chunk["text"] = text
    chunk["script"] = script
    chunk["sons"] = extra.get("sons", chunk.get("sons") or "")
    if chunk["sons"] is None:
        chunk["sons"] = ""
    chunk["text_ssml"] = ssml(text, m)
    chunk["text_xai_tags"] = xai(text, m)
    chunk["rate_wpm"] = m["wpm"]
    chunk["rate_label"] = m["rate"]
    chunk["speed_xai"] = m["speed"]
    chunk["length_scale_piper"] = m["piper"]
    chunk["pitch_label"] = m["pitch"]
    chunk["pitch_ssml"] = m["pitchSsml"]
    chunk["pitch_xai_tag"] = m["pitchTag"]
    chunk["volume_label"] = m["volume"]
    chunk["volume_db"] = m["db"]
    chunk["emphasis_words"] = m.get("emphasis") or ""
    chunk["pause_before_ms"] = extra.get("pauseBefore", 0)
    chunk["pause_after_ms"] = m["pause"]
    chunk["pause_sentence_ms"] = m["sentence"]
    chunk["style_energy"] = m["energy"]
    chunk["style_contour"] = m["contour"]
    chunk["noise_scale_piper"] = m["noise"]
    chunk["kokoro_speed"] = m["speed"]
    chunk["melo_speed"] = m["speed"]
    chunk["espeak_amp"] = 82 if m["volume"] == "soft" else 100
    chunk["espeak_pitch"] = 42 if m["pitch"] == "low" else 50
    chunk["espeak_word_gap"] = 12 if m["rate"] == "slow" else 10
    chunk["notes"] = extra.get("notes", m["note"])
    chunk["night_policy"] = "play"
    chunk["locale"] = "fr-FR"
    chunk["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        chunk[k] = v


STARTS = {
    1: dict(name="le ciré jaune", prop="le ciré jaune", boat="la feuille du ciré"),
    2: dict(name="les bottes", prop="les bottes", boat="la feuille de la botte"),
    3: dict(name="le bateau", prop="le bateau de papier", boat="le bateau de papier"),
}

LOCS = {
    1: dict(name="la flaque du portail", short="le portail"),
    2: dict(name="la gouttière", short="la gouttière"),
    3: dict(name="le bac", short="le bac"),
}

SOLS = {
    1: dict(name="une feuille", spoken="une feuille"),
    2: dict(name="un caillou", spoken="un caillou"),
    3: dict(name="la goutte", spoken="la goutte"),
}


def t1_passage(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            "narrateur|Victorino tire le ciré jaune.",
            "narrateur|Le capuchon lourd tape son oreille.",
            "enfant-m|Mets-le, vite !",
            "narrateur|Papa parle du cacao, à maman.",
            "narrateur|Personne ne tourne la tête.",
            "narrateur|Victorino serre le ciré contre lui.",
            "enfant-m|Le ciré !",
            "enfant-m|La flaque !",
            "narrateur|Les mots se perdent dans la vapeur.",
            "narrateur|Victorino lâche une manche.",
            "narrateur|Il touche le coude de papa.",
            "enfant-m|Quand tu as fini, le ciré.",
            "papa|Une seconde.",
            "papa|Voilà, je t'écoute.",
            "narrateur|Papa glisse une manche, puis l'autre.",
            "narrateur|Une goutte glisse du capuchon.",
            "maman|Le capuchon est mouillé.",
            "enfant-m|On y va quand même.",
        )
    if a == 2:
        return L(
            "narrateur|Victorino attrape les bottes vertes.",
            "narrateur|Une botte est tiède, l'autre froide.",
            "enfant-m|Mes bottes, pour la flaque !",
            "narrateur|Maman cherche le gant, près du radiateur.",
            "narrateur|Elle parle à papa du gant perdu.",
            "narrateur|Les mots de Victorino tombent par terre.",
            "enfant-m|Maman !",
            "narrateur|Maman ne se tourne pas.",
            "narrateur|Victorino pose une botte.",
            "narrateur|Il attend, une chaussette à la main.",
            "maman|Oui, je t'écoute.",
            "enfant-m|Il manque une chaussette.",
            "papa|Elle chauffe, sur le radiateur.",
            "narrateur|Maman tend la chaussette chaude.",
            "narrateur|Victorino enfile le coton tiède.",
            "papa|Les bottes font un petit ploc.",
        )
    return L(
        "narrateur|Victorino prend son bateau de papier.",
        "narrateur|Le papier est blanc, un peu gondolé.",
        "enfant-m|Il va sur la flaque !",
        "narrateur|Papa parle du cacao, près des tasses.",
        "narrateur|Victorino agite le bateau.",
        "narrateur|Papa voit le papier, pas les mots.",
        "papa|Joli bateau.",
        "enfant-m|Non, écoute le plan !",
        "narrateur|Les mots se mêlent au cacao.",
        "narrateur|Victorino pose le bateau.",
        "narrateur|Il attend que papa finisse.",
        "papa|Je t'écoute, maintenant.",
        "enfant-m|Le bateau va sur la flaque.",
        "maman|Avant le soleil, alors.",
        "narrateur|Le papier tremble dans sa main.",
        "narrateur|Une ombre de nuage passe sur la vitre.",
    )


def t1_q(a: int) -> tuple[list[tuple[str, str]], dict]:
    if a == 1:
        return L(
            "narrateur|Quelque chose tombe du capuchon.",
            "papa|Qu'est-ce qui tombe ?",
        ), dict(
            expected_answer="goutte",
            accepted_examples="goutte | une goutte | l'eau | de l'eau | capuchon",
            retry_prompt="Regarde le capuchon. Qu'est-ce qui tombe ?",
        )
    if a == 2:
        return L(
            "narrateur|Une botte attend son coton.",
            "maman|Que manque-t-il, pour la botte ?",
        ), dict(
            expected_answer="chaussette",
            accepted_examples="chaussette | une chaussette | le coton | coton",
            retry_prompt="Sur le radiateur, qu'est-ce qui chauffe ?",
        )
    return L(
        "narrateur|Victorino a un plan, pour l'eau.",
        "papa|Que veut-il poser sur la flaque ?",
    ), dict(
        expected_answer="bateau",
        accepted_examples="bateau | le bateau | papier | le papier",
        retry_prompt="Qu'est-ce qu'il tient, en papier ?",
    )


def t1_confirm(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            "enfant-m|Une goutte !",
            "narrateur|Oui, une goutte du capuchon.",
            "narrateur|Cette fois, papa a entendu.",
            "maman|Merci, Victorino.",
            "papa|Nous t'avons entendu.",
            "narrateur|Le ciré craque, un peu collant.",
            "narrateur|Une feuille jaune colle à la poche.",
            "narrateur|Ils avancent vers la porte.",
        )
    if a == 2:
        return L(
            "enfant-m|La chaussette !",
            "narrateur|Oui, la chaussette du radiateur.",
            "narrateur|Maman l'a entendue, cette fois.",
            "papa|Merci, Victorino.",
            "papa|Tes mots sont arrivés.",
            "narrateur|Les bottes font un petit ploc.",
            "narrateur|Une feuille colle à la botte.",
            "narrateur|La porte s'ouvre un peu.",
        )
    return L(
        "enfant-m|Le bateau !",
        "narrateur|Oui, le bateau de papier.",
        "narrateur|Papa a entendu toute la phrase.",
        "maman|Merci, Victorino.",
        "maman|Toute la phrase est arrivée.",
        "narrateur|Le bateau tremble dans sa main.",
        "narrateur|Une feuille s'est collée au papier.",
        "narrateur|La porte s'ouvre un peu.",
    )


def t2_passage(a: int, b: int) -> list[tuple[str, str]]:
    prop = STARTS[a]["prop"]
    if b == 1:
        return L(
            f"narrateur|Avec {prop}, ils vont au portail.",
            "narrateur|La flaque ronde tient le ciel.",
            "maman|Une feuille colle au bord.",
            "papa|Moi, je vois un nuage.",
            "narrateur|Ils parlent en même temps.",
            "narrateur|Victorino ne sait plus où regarder.",
            "enfant-m|Papa d'abord.",
            "enfant-m|Après, maman.",
            "narrateur|Papa montre le nuage blanc.",
            "narrateur|Maman montre la feuille collée.",
            "narrateur|Le bateau part vers la boîte.",
            "narrateur|Le soleil coupe l'eau en deux.",
        )
    if b == 2:
        return L(
            f"narrateur|Avec {prop}, ils suivent la gouttière.",
            "narrateur|L'eau court comme un ruisseau.",
            "papa|Elle va à gauche.",
            "maman|Moi, je vois la grille.",
            "narrateur|Deux chemins se mêlent.",
            "narrateur|Victorino cligne des yeux.",
            "enfant-m|Une voix, puis l'autre.",
            "narrateur|Papa montre la gauche.",
            "narrateur|Maman montre la grille noire.",
            "narrateur|Le bateau file trop vite.",
            "narrateur|Une vague le pousse.",
        )
    return L(
        f"narrateur|Avec {prop}, ils vont au bac.",
        "narrateur|Le sable est un petit lac.",
        "papa|J'ajoute un peu d'eau.",
        "narrateur|Sa main lève l'arrosoir.",
        "enfant-m|Stop, papa !",
        "enfant-m|Le bateau est dessous !",
        "narrateur|Cette fois, il n'attend pas.",
        "narrateur|Papa retient l'arrosoir.",
        "maman|Tu as bien fait.",
        "narrateur|Le bateau tremble au milieu.",
        "narrateur|Une ride d'eau arrive.",
    )


def t3_q(b: int) -> list[tuple[str, str]]:
    sit = {
        1: "Le bateau glisse vers la boîte.",
        2: "Le bateau file trop vite.",
        3: "L'arrosoir reste trop près.",
    }[b]
    return L(
        f"narrateur|{sit}",
        "papa|Une feuille, un caillou, ou la goutte ?",
    )


def t3_body(b: int, c: int) -> list[tuple[str, str]]:
    scenes = {
        (1, 1): L(
            "narrateur|Victorino choisit une feuille large.",
            "narrateur|Il la pose devant la boîte.",
            "narrateur|La feuille fait un petit quai.",
            "narrateur|Le bateau s'arrête contre le bord.",
            "enfant-m|Il a trouvé le quai !",
            "papa|Je n'avais pas vu ce quai.",
            "maman|Nous avons regardé ensemble.",
        ),
        (2, 1): L(
            "narrateur|Victorino prend une feuille de platane.",
            "narrateur|Il la pose en travers de l'eau.",
            "narrateur|L'eau passe dessous, plus lente.",
            "narrateur|Le bateau touche la feuille.",
            "enfant-m|Il essaie mon pont !",
            "narrateur|Personne ne parle, un moment.",
            "maman|Le voilà de l'autre côté.",
        ),
        (3, 1): L(
            "narrateur|Victorino plante une feuille dans le sable.",
            "narrateur|Elle se dresse comme un drapeau.",
            "enfant-m|Comme ça, on ne verse plus.",
            "papa|Je pose l'arrosoir, alors.",
            "narrateur|Le bateau glisse vers l'herbe.",
            "maman|Je garde le drapeau.",
            "narrateur|Victorino souffle, soulagé.",
        ),
        (1, 2): L(
            "narrateur|Victorino choisit un caillou clair.",
            "narrateur|Il le pose loin du bateau.",
            "narrateur|Le caillou ferme le chemin de la boîte.",
            "papa|Je vois la petite zone.",
            "narrateur|Le bateau contourne le caillou.",
            "enfant-m|Notre pierre lui laisse son chemin.",
            "maman|Bien vu.",
        ),
        (2, 2): L(
            "narrateur|Victorino choisit un caillou plat.",
            "narrateur|Avec papa, il le pose dans l'eau.",
            "narrateur|L'eau ralentit, comme une marche.",
            "maman|Le côté peu profond est là.",
            "narrateur|Victorino attend qu'elle finisse.",
            "enfant-m|Maintenant, le bord ne glisse plus.",
            "narrateur|Le bateau passe sur la pierre.",
        ),
        (3, 2): L(
            "narrateur|Victorino prend un caillou blanc.",
            "narrateur|Il le pose devant l'arrosoir.",
            "enfant-m|C'est une barrière pour l'eau.",
            "papa|Je comprends.",
            "papa|Je ne verse pas.",
            "maman|La sortie est libre, vers l'herbe.",
            "narrateur|Le bateau avance entre le caillou et le bord.",
            "narrateur|Le papier quitte le sable mouillé.",
        ),
        (1, 3): L(
            "narrateur|Victorino choisit de regarder.",
            "enfant-m|Chut.",
            "enfant-m|La goutte va nous montrer.",
            "narrateur|La famille s'accroupit près de la flaque.",
            "narrateur|Une goutte tombe du capuchon.",
            "narrateur|Puis le bateau tourne vers le bord.",
            "papa|Voilà ce que je n'avais pas vu.",
            "maman|La goutte a parlé, à sa façon.",
            "narrateur|Le bateau gagne l'herbe, sans une main.",
        ),
        (2, 3): L(
            "narrateur|Victorino choisit de regarder l'eau.",
            "narrateur|Il observe la vague, pas seulement le bateau.",
            "narrateur|Une goutte tombe, puis l'eau baisse.",
            "enfant-m|Là !",
            "enfant-m|Le passage est libre.",
            "narrateur|Le bateau avance au moment calme.",
            "papa|Je retiens la grille.",
            "maman|Je compte les secondes.",
            "narrateur|À dix, le bateau touche la mousse.",
        ),
        (3, 3): L(
            "narrateur|Victorino choisit de regarder.",
            "narrateur|Papa garde les mains loin de l'arrosoir.",
            "maman|Il avance vers toi, Victorino.",
            "narrateur|Victorino ne répond pas.",
            "narrateur|Il laisse le silence au bateau.",
            "enfant-m|Maintenant, tu peux poser l'arrosoir.",
            "narrateur|Papa attend que le papier touche l'herbe.",
        ),
    }
    return scenes[(b, c)]


CALLBACKS = {
    (1, 1, 1): "Le ciré jaune se reflète sur le quai.",
    (1, 1, 2): "Une poche du ciré touche l'herbe.",
    (1, 1, 3): "Le capuchon ne goutte plus.",
    (1, 2, 1): "Le ciré garde une éclaboussure.",
    (1, 2, 2): "Une manche du ciré luit.",
    (1, 2, 3): "Le ciré sent l'eau de la gouttière.",
    (1, 3, 1): "Le drapeau se voit sur le ciré.",
    (1, 3, 2): "Le caillou blanc brille près du ciré.",
    (1, 3, 3): "Le ciré jaune sèche au soleil du bac.",
    (2, 1, 1): "Une botte a un croissant d'eau.",
    (2, 1, 2): "Les bottes font ploc, près du caillou.",
    (2, 1, 3): "Une botte garde une goutte ronde.",
    (2, 2, 1): "Les bottes sont mouillées jusqu'au bord.",
    (2, 2, 2): "Un caillou a tapé une botte, sans mal.",
    (2, 2, 3): "Les bottes attendent la prochaine vague.",
    (2, 3, 1): "Une botte s'enfonce un peu dans le sable.",
    (2, 3, 2): "Les bottes gardent le caillou entre elles.",
    (2, 3, 3): "Une botte reflète le bac calme.",
    (3, 1, 1): "Le papier a pris un pli de quai.",
    (3, 1, 2): "Le bateau a une ride de caillou.",
    (3, 1, 3): "Une goutte a dessiné un rond sur le papier.",
    (3, 2, 1): "Le pont de feuille a mouillé le papier.",
    (3, 2, 2): "Le bateau sent la pierre mouillée.",
    (3, 2, 3): "Le papier brille, comme après la vague.",
    (3, 3, 1): "Le bateau a un grain de sable.",
    (3, 3, 2): "Le papier touche le caillou blanc.",
    (3, 3, 3): "Le bateau sèche, plat comme une feuille.",
}

CHILD1 = {
    (1, 1, 1): "Le quai a sauvé le bateau.",
    (1, 1, 2): "Le caillou a gardé la boîte.",
    (1, 1, 3): "La goutte a tourné le bateau.",
    (1, 2, 1): "Mon pont a ralenti l'eau.",
    (1, 2, 2): "La pierre a fait une marche.",
    (1, 2, 3): "J'ai regardé la vague partir.",
    (1, 3, 1): "Le drapeau a arrêté l'arrosoir.",
    (1, 3, 2): "Le caillou a parlé à papa.",
    (1, 3, 3): "Le silence a aidé le bateau.",
    (2, 1, 1): "Mes bottes ont vu le quai.",
    (2, 1, 2): "Mes bottes ont vu le caillou.",
    (2, 1, 3): "Mes bottes ont vu la goutte.",
    (2, 2, 1): "On a mis un pont, avec les bottes.",
    (2, 2, 2): "On a mis une marche, dans l'eau.",
    (2, 2, 3): "On a laissé passer la vague.",
    (2, 3, 1): "Le drapeau a gardé le bac.",
    (2, 3, 2): "Le caillou a gardé l'arrosoir.",
    (2, 3, 3): "On a laissé le bac se calmer.",
    (3, 1, 1): "Mon bateau a trouvé le quai.",
    (3, 1, 2): "Mon bateau a contourné la pierre.",
    (3, 1, 3): "Mon bateau a suivi la goutte.",
    (3, 2, 1): "Mon bateau a pris le pont.",
    (3, 2, 2): "Mon bateau a grimpé la pierre.",
    (3, 2, 3): "Mon bateau a attendu la vague.",
    (3, 3, 1): "Mon bateau a suivi le drapeau.",
    (3, 3, 2): "Mon bateau a glissé près du caillou.",
    (3, 3, 3): "Mon bateau a pris tout le silence.",
}

CHILD2 = {
    (1, 1, 1): "Le ciel est resté dans l'eau.",
    (1, 1, 2): "La boîte n'a pas pris le bateau.",
    (1, 1, 3): "Le capuchon s'est tu.",
    (1, 2, 1): "Le ciré a senti le pont.",
    (1, 2, 2): "Le ciré a senti la pierre.",
    (1, 2, 3): "Le ciré a senti la mousse.",
    (1, 3, 1): "Personne n'a versé.",
    (1, 3, 2): "Papa a compris sans verser.",
    (1, 3, 3): "L'arrosoir est resté en l'air.",
    (2, 1, 1): "Le quai était froid, comme mes bottes.",
    (2, 1, 2): "Le caillou était froid, comme mes bottes.",
    (2, 1, 3): "La goutte était ronde, comme mes bottes.",
    (2, 2, 1): "L'eau est devenue lente.",
    (2, 2, 2): "L'eau est devenue une marche.",
    (2, 2, 3): "L'eau a dit le bon moment.",
    (2, 3, 1): "Le sable a gardé le bateau.",
    (2, 3, 2): "Le sable a laissé un chemin.",
    (2, 3, 3): "Le sable est redevenu un lac.",
    (3, 1, 1): "Le papier a un pli de quai.",
    (3, 1, 2): "Le papier a une ride de pierre.",
    (3, 1, 3): "Le papier a un rond de goutte.",
    (3, 2, 1): "Le papier a un goût de feuille.",
    (3, 2, 2): "Le papier a un goût de pierre.",
    (3, 2, 3): "Le papier a un goût de mousse.",
    (3, 3, 1): "Le papier a un grain de sable.",
    (3, 3, 2): "Le papier a touché le blanc.",
    (3, 3, 3): "Le papier sèche, plat et fier.",
}

LAST = {
    (1, 1, 1): "Sous le portail, la feuille luit, jaune comme le ciré.",
    (2, 1, 1): "Sous le portail, une botte veille près du quai.",
    (3, 1, 1): "Sous le portail, le papier sèche sur le quai.",
    (1, 1, 2): "Le caillou clair a un reflet de ciré.",
    (2, 1, 2): "Le caillou clair a un croissant de botte.",
    (3, 1, 2): "Le caillou clair a une ride de papier.",
    (1, 1, 3): "La flaque tient un ciel, sans goutte de capuchon.",
    (2, 1, 3): "La flaque tient un ciel, entre deux bottes.",
    (3, 1, 3): "La flaque tient un ciel, et le papier repose.",
    (1, 2, 1): "La feuille pont sent le ciré mouillé.",
    (2, 2, 1): "La feuille pont a une trace de botte.",
    (3, 2, 1): "La feuille pont a séché le papier.",
    (1, 2, 2): "La pierre garde une perle, près du ciré.",
    (2, 2, 2): "La pierre garde une perle, près des bottes.",
    (3, 2, 2): "La pierre garde une perle, près du papier.",
    (1, 2, 3): "La mousse du mur brille, comme le ciré.",
    (2, 2, 3): "La mousse du mur brille, entre les bottes.",
    (3, 2, 3): "La mousse du mur brille, près du papier.",
    (1, 3, 1): "Le drapeau vert penche vers le ciré.",
    (2, 3, 1): "Le drapeau vert penche vers les bottes.",
    (3, 3, 1): "Le drapeau vert penche vers le papier.",
    (1, 3, 2): "Le caillou blanc reste, près du ciré.",
    (2, 3, 2): "Le caillou blanc reste, près des bottes.",
    (3, 3, 2): "Le caillou blanc reste, près du papier.",
    (1, 3, 3): "Le bac redevient un miroir, derrière le ciré.",
    (2, 3, 3): "Le bac redevient un miroir, entre les bottes.",
    (3, 3, 3): "Le bac redevient un miroir de sable.",
}

RETURN = {
    1: "À la maison, papa pose sa tasse.",
    2: "Près de la vitre, le cacao fume.",
    3: "Sur la table, deux tasses tiédissent.",
}

KEEP = {
    1: "Le ciré jaune reprend le crochet.",
    2: "Les bottes sèchent près du gant.",
    3: "Le bateau sèche près de la tasse.",
}


def ending(a: int, b: int, c: int) -> list[tuple[str, str]]:
    key = (a, b, c)
    return L(
        f"narrateur|{RETURN[b]}",
        "maman|À toi, Victorino.",
        "maman|Nous t'écoutons.",
        f"enfant-m|{CHILD1[key]}",
        f"enfant-m|{CHILD2[key]}",
        f"narrateur|{KEEP[a]}",
        f"narrateur|{LAST[key]}",
    )


def t3_passage(a: int, b: int, c: int) -> list[tuple[str, str]]:
    body = list(t3_body(b, c))
    body.append(("narrateur", CALLBACKS[(a, b, c)]))
    n = wc(CALLBACKS[(a, b, c)])
    if n > LIM:
        raise SystemExit(f"callback {n}: {CALLBACKS[(a, b, c)]}")
    return body


def main() -> None:
    for d in (CALLBACKS, CHILD1, CHILD2, LAST):
        for k, s in d.items():
            n = wc(s)
            if n > LIM:
                raise SystemExit(f"{k} {n}>10: {s}")
            marks = s.count(".") + s.count("?") + s.count("!")
            if marks != 1:
                raise SystemExit(f"{k} punct {marks}: {s}")

    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: deepcopy(c) for c in src["chunks"]}

    voice(
        by["CHK_T0000_P0000"],
        L(
            "narrateur|Sous le portail, une flaque ronde tient le ciel.",
            "narrateur|Le ciré jaune pend au crochet.",
            "narrateur|Le capuchon lourd laisse une goutte.",
            "narrateur|La goutte tombe près des bottes.",
            "narrateur|Ça sent le cacao, près de la vitre.",
            "narrateur|La vapeur dessine un nuage sur le verre.",
            "narrateur|Papa pose deux tasses tièdes.",
            "narrateur|Maman cherche un gant sur le radiateur.",
            "narrateur|Un merle parle, derrière le portail.",
            "narrateur|En ce moment, Victorino tire le ciré.",
            "enfant-m|Je veux la flaque !",
            "enfant-m|Le ciel est dedans !",
            "narrateur|Papa parle du cacao, à maman.",
            "narrateur|Les mots se cognent aux tasses.",
            "papa|Tu disais, Victorino ?",
            "enfant-m|La flaque, le ciel !",
            "narrateur|Papa écoute maman, pas lui.",
            "narrateur|Victorino ferme la bouche.",
            "narrateur|Il attend, près du crochet.",
            "narrateur|Le cacao fait un petit nuage.",
            "papa|Voilà, je t'écoute.",
            "enfant-m|Je veux aller à la flaque.",
            "maman|Avec quoi commençons-nous ?",
        ),
        "opening",
        extra={"sons": "goutte,cacao"},
    )

    voice(
        by["CHK_T0001_P0000"],
        L(
            "narrateur|Victorino peut prendre le ciré, les bottes, ou le bateau.",
            "maman|Que prends-tu pour la flaque ?",
        ),
        "choice",
        extra={
            "fields": {
                "option_1_label": "le ciré jaune",
                "option_2_label": "les bottes",
                "option_3_label": "le bateau",
            }
        },
    )

    t1_sons = {1: "crochet,goutte", 2: "bottes", 3: "papier"}
    t1_emp = {1: "ciré", 2: "bottes", 3: "bateau"}
    t1_q_emp = {1: "goutte", 2: "chaussette", 3: "bateau"}

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        voice(by[base], t1_passage(a), "action", extra={"sons": t1_sons[a], "emphasis": t1_emp[a]})
        q_lines, q_fields = t1_q(a)
        voice(
            by[f"{base}_Q0001"],
            q_lines,
            "clue",
            extra={"emphasis": t1_q_emp[a], "fields": q_fields},
        )
        voice(by[f"{base}_C0001"], t1_confirm(a), "confirm", extra={"emphasis": t1_q_emp[a]})
        voice(
            by[f"{base}_T0002_P0000"],
            L(
                "narrateur|Dehors, l'eau brille en trois endroits.",
                "papa|La flaque du portail, la gouttière, ou le bac ?",
                "maman|Où allons-nous ?",
            ),
            "choice",
            extra={
                "fields": {
                    "option_1_label": "la flaque du portail",
                    "option_2_label": "la gouttière",
                    "option_3_label": "le bac",
                }
            },
        )

        loc_sons = {1: "goutte,portail", 2: "gouttiere,eau", 3: "seau,eau"}
        sol_sons = {1: "feuille", 2: "caillou", 3: "goutte"}
        fin_sons = {1: "couverts,goutte", 2: "couverts,gouttiere", 3: "couverts,merle"}
        t3_emp = {1: "feuille", 2: "caillou", 3: "goutte"}

        for b in (1, 2, 3):
            loc_id = f"{base}_T0002_P000{b}"
            voice(
                by[loc_id],
                t2_passage(a, b),
                "obstacle",
                extra={"sons": loc_sons[b], "emphasis": "bateau"},
            )
            voice(
                by[f"{loc_id}_T0003_P0000"],
                t3_q(b),
                "choice",
                extra={
                    "fields": {
                        "option_1_label": "une feuille",
                        "option_2_label": "un caillou",
                        "option_3_label": "la goutte",
                    }
                },
            )
            for c in (1, 2, 3):
                leaf = f"{loc_id}_T0003_P000{c}"
                voice(
                    by[leaf],
                    t3_passage(a, b, c),
                    "resolution",
                    extra={"sons": sol_sons[c], "emphasis": t3_emp[c]},
                )
                voice(
                    by[f"{leaf}_F0001"],
                    ending(a, b, c),
                    "ending",
                    extra={"sons": fin_sons[b]},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra)[:8]}")

    fins = [by[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(fins) != 27:
        raise SystemExit(f"fins {len(fins)}")
    if len(set(fins)) != 27:
        raise SystemExit("fins non distinctes")

    out = dict(src)
    out["fil_rouge"] = (
        "Après la pluie, une flaque tient le ciel sous le portail. "
        "Victorino veut y aller tout de suite, avec son ciré jaune. "
        "Il crie pendant que papa et maman parlent du cacao : personne n'entend. "
        "Il attend, puis on l'écoute. Le ciré, les bottes ou le bateau lancent la sortie ; "
        "la flaque du portail, la gouttière ou le bac changent l'obstacle ; "
        "une feuille, un caillou ou la goutte sauvent le petit bateau. "
        "À la maison, chacun l'écoute jusqu'au bout."
    )
    out["title"] = "La flaque et le ciré de Victorino"
    out["characters"] = "Victorino, papa, maman"
    out["setting"] = "une petite maison après la pluie, flaque sous le portail"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    # longueur d'un chemin (racine → feuille)
    def path_words(a: int, b: int, c: int) -> int:
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
        return sum(wc(by[i]["text"]) for i in ids)

    pw = [path_words(a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins {min(pw)}-{max(pw)} mots, moy {sum(pw)//len(pw)}")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
