#!/usr/bin/env python3
"""TREE-COL-022 — Le grain de sel et le panier de Nina (F-NAR-019, N3).

Marché, planches, store rayé. Grain de sel = objet/mission.
Indice unique : un rond d'huile (pas le grain de sel).
COL.POL.001 vécu : tours de parole / ne pas couper, jamais dit.
Nina, papa, maman seulement. Panier de toile part AVEC.
T2 labels : boulangère / voisin / maîtresse — pas de rôle parlé maîtresse.
Monde ≠ TREE-AUT-045 (osier, paprika), ≠ TREE-DIF-008 (cannelle),
≠ TREE-COL-027 (toiles, osier), ≠ TREE-COL-035 (goutte, trois mots).
Texte + TTS. Pas apply. Pas audio. Pas git.
"""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, words  # noqa: E402

SID = "TREE-COL-022"
LIM = 16
TITLE = "Le grain de sel et le panier de Nina"
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà)\b", re.I)
BAD_WORLD = re.compile(
    r"\b(osier|paprika|cannelle|miel|merle|toiles rayées|croissant d'eau)\b",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="rond d'huile",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le grain veut partir trop vite, les pièces recouvrent la voix; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change l'allée; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde le rond et le grain; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la phrase est arrivée entière; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle veut le sel maintenant; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_retenue; intensite=2; destinataire=enfant; sous_texte=envie de couper, puis retenue; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="rond d'huile",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=le rond d'huile a guidé le geste; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de sel",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le grain et le rond paient le début; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def wc(s: str) -> int:
    return words(s)


def L(*rows: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    prev = ""
    run = 1
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = wc(ph)
        if n > LIM:
            raise SystemExit(f"{n}>{LIM}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        if BAD_WORLD.search(ph):
            raise SystemExit(f"monde voisin: {ph}")
        low = ph.lower()
        if "aujourd'hui," in low or "aujourd’hui," in low:
            raise SystemExit(f"aujourd'hui: {ph}")
        if role == "maitresse" or role == "maîtresse":
            raise SystemExit(f"rôle parlé maîtresse: {ph}")
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
            body = body[:i] + f'<emphasis level="moderate">{body[i:i + len(e)]}</emphasis>' + body[i + len(e):]
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


def voice(chunk: dict, ls: list[tuple[str, str]], profile: str, extra: dict | None = None) -> None:
    extra = extra or {}
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    text = " ".join(t for _, t in ls)
    script = "\n".join(f"{r}|{t}" for r, t in ls)
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
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
    chunk["pause_before_ms"] = extra.get("pauseBefore", 200 if profile in ("choice", "clue") else 0)
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


def t1_passage(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            "narrateur|Nina emporte le panier de toile, cordon rouge au poignet.",
            "narrateur|L'allée des planches mène à la boulangerie chaude.",
            "narrateur|Ça sent la croûte, et un peu de beurre fondu.",
            "enfant-f|Le grain de sel, dans le pain !",
            "narrateur|Papa parle du four, à maman, près de la vitrine.",
            "narrateur|Les mots de Nina se cassent contre le verre tiède.",
            "enfant-f|Papa, écoute le sel !",
            "narrateur|Personne ne se tourne, et le sourire s'efface.",
            "narrateur|Dans sa poitrine, ça pousse, puis ça serre.",
            "narrateur|Elle refuse de crier plus fort.",
            "narrateur|Le panier reste avec elle, anse contre la hanche.",
            "narrateur|Un papier plié garde le grain, au fond du toile.",
            "narrateur|Nina attend, les lèvres serrées, sous le store rayé.",
            "papa|Voilà, je t'écoute, Nina.",
            "enfant-f|Le grain tient dans le rond d'huile.",
            "maman|On a entendu, cette fois.",
            "narrateur|La croûte craque, tout près, sans les déranger.",
        )
    if a == 2:
        return L(
            "narrateur|Nina part avec le panier, vers l'étal des tomates.",
            "narrateur|Les planches claquent sous les sandales, sèches et chaudes.",
            "narrateur|Le store rayé jette des bandes, sur les caisses rouges.",
            "enfant-f|Une tomate, pour le sel !",
            "narrateur|Maman parle du poids, à papa, près de la balance.",
            "narrateur|Nina tend la main trop vite, au-dessus du bois.",
            "narrateur|Le papier du grain glisse, et une tomate roule.",
            "enfant-f|Maman !",
            "narrateur|Les deux voix d'adultes recouvrent la sienne.",
            "narrateur|Elle recule, les joues chaudes sous l'ombre zébrée.",
            "narrateur|Sur une planche de l'étal, un rond d'huile brille.",
            "narrateur|Nina pose le panier, et attend une oreille.",
            "maman|Oui, je t'écoute.",
            "enfant-f|Le rond d'huile, il est là, sur la planche.",
            "papa|Nous regardons avec toi.",
            "narrateur|Le panier de toile n'a pas quitté ses doigts.",
        )
    return L(
        "narrateur|Nina emporte le panier de toile, vers la fromagerie.",
        "narrateur|Le comptoir blanc sent le lait, et un peu de cave.",
        "narrateur|Une cloche de verre cache un fromage rond, pâle.",
        "enfant-f|Le sel, pour le fromage !",
        "narrateur|Papa répond à maman, au sujet de la bourse.",
        "narrateur|La phrase de Nina glisse sur le blanc, sans oreille.",
        "enfant-f|Le grain, vite !",
        "narrateur|Elle ouvre la bouche plus fort, puis la referme.",
        "narrateur|L'envie de couper lui pique la gorge, puis recule.",
        "narrateur|Le panier tape sa jambe, cordon rouge un peu gras.",
        "narrateur|Elle attend que la bourse se ferme, sans foncer.",
        "papa|La bourse est fermée, je t'écoute.",
        "enfant-f|Le panier porte le grain, contre ma hanche.",
        "maman|Tes mots sont arrivés, entiers.",
        "narrateur|Sous le store, le rond d'huile garde sa lune claire.",
    )


def t1_q(a: int) -> tuple[list[tuple[str, str]], dict]:
    if a == 1:
        return L(
            "narrateur|Dans le rond d'huile, quelque chose de blanc tient.",
            "papa|Qu'est-ce qui tient, dans le rond d'huile ?",
        ), dict(
            expected_answer="sel",
            accepted_examples="sel | grain | grain de sel | le sel | le grain | un grain de sel",
            retry_prompt="Dans le rond d'huile, sur la planche. Qu'est-ce qui est blanc ?",
        )
    if a == 2:
        return L(
            "narrateur|Sur la planche de l'étal, quelque chose brille.",
            "maman|Qu'est-ce qui brille, sur la planche ?",
        ), dict(
            expected_answer="huile",
            accepted_examples="huile | rond | rond d'huile | l'huile | le rond | un rond d'huile",
            retry_prompt="Sur le bois de l'étal. Qu'est-ce qui brille, rond ?",
        )
    return L(
        "narrateur|Nina n'a rien laissé derrière elle, à l'entrée.",
        "papa|Elle emporte quoi, avec le grain de sel ?",
    ), dict(
        expected_answer="panier",
        accepted_examples="panier | le panier | panier de toile | le panier de toile | toile",
        retry_prompt="Contre sa hanche, le cordon rouge. Elle porte quoi ?",
    )


def t1_confirm(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            "enfant-f|Le grain de sel !",
            "narrateur|Oui, le grain blanc, dans le rond d'huile.",
            "narrateur|Cette fois, papa a entendu toute la phrase.",
            "narrateur|Nina serre le panier, et le papier du grain tient.",
            "maman|On avance avec le panier, d'accord ?",
            "enfant-f|D'accord, le panier vient.",
            "narrateur|La croûte chaude suit l'allée, sous le store rayé.",
        )
    if a == 2:
        return L(
            "enfant-f|Le rond d'huile !",
            "narrateur|Oui, le rond gras, sur la planche de l'étal.",
            "narrateur|Maman a entendu, sans que Nina crie.",
            "narrateur|Le panier de toile reste dans ses doigts.",
            "papa|On continue, avec le panier.",
            "enfant-f|Le grain est dedans, dans le papier.",
            "narrateur|Une tomate luit, comme une petite lune d'huile.",
        )
    return L(
        "enfant-f|Le panier !",
        "narrateur|Oui, le panier de toile, et le grain au fond.",
        "narrateur|Papa a reçu les mots, un par un.",
        "maman|Le fromage attend, sous sa cloche.",
        "enfant-f|On y va, avec le panier.",
        "narrateur|Le comptoir blanc reflète le store, en bandes.",
        "narrateur|Le rond d'huile, derrière, reste sur sa planche.",
    )


def t2_passage(a: int, b: int) -> list[tuple[str, str]]:
    lieu = {1: "la boulangerie", 2: "l'étal", 3: "la fromagerie"}[a]
    scenes = {
        (1, 1): L(
            "narrateur|Avec le panier, ils restent à la boulangerie chaude.",
            "narrateur|La boulangère essuie une planche, torchon large.",
            "narrateur|Le torchon avance vers un rond d'huile, tout petit.",
            "enfant-f|Non, le rond !",
            "narrateur|Sa voix coupe le bruit du four, et personne n'entend.",
            "narrateur|Nina sent l'envie de tirer le torchon, trop fort.",
            "narrateur|Elle refuse de foncer, et recule d'un pas.",
            "narrateur|Elle observe le rond d'huile, collé au bois chaud.",
            "enfant-f|Quand le torchon s'arrête, je parle ?",
            "papa|Le torchon s'arrête, elle lève les yeux.",
            "narrateur|Le grain, dans le papier, pèse à peine, au fond.",
            "maman|Que glisse-t-on dans le panier, maintenant ?",
        ),
        (1, 2): L(
            "narrateur|Devant la vitrine chaude, le voisin bloque l'allée.",
            "narrateur|Son sac de toile barre les planches, trop large.",
            "narrateur|Il raconte un melon, d'une voix ronde, trop longue.",
            "enfant-f|Pardon, je veux passer !",
            "narrateur|Le melon recouvre sa phrase, et Nina serre les dents.",
            "narrateur|Entre deux planches, le rond d'huile tremble, menacé.",
            "narrateur|Un pied du voisin s'approche, et Nina ne fonce pas.",
            "narrateur|Elle écoute la fin du melon, panier contre elle.",
            "enfant-f|Quand le melon a fini, je passe ?",
            "maman|Le melon a fini, son sac se décale, on t'écoute.",
            "narrateur|Le rond d'huile reste, intact, sur sa planche.",
            "papa|Que veux-tu glisser, dans le panier de toile ?",
        ),
        (1, 3): L(
            "narrateur|Près des miches, la maîtresse parle à maman.",
            "narrateur|Elle tient une liste pliée, sans voir Nina.",
            "enfant-f|Maîtresse, j'ai le sel !",
            "narrateur|Les deux voix d'adultes se mêlent, et le mot tombe.",
            "narrateur|Nina referme la bouche, les joues qui piquent.",
            "narrateur|Elle refuse de couper la liste, et elle attend.",
            "narrateur|Derrière elles, le rond d'huile fait une lune grasse.",
            "enfant-f|Quand la liste est finie, je dis le sel ?",
            "papa|La liste est finie, maman se tourne, nous t'écoutons.",
            "narrateur|La maîtresse range le papier, liste contre le sac.",
            "narrateur|Le panier de toile pèse, chaud de la croûte.",
            "maman|Que met-on avec le grain, à présent ?",
        ),
        (2, 1): L(
            "narrateur|À l'étal, la boulangère pèse des tomates, loin du four.",
            "narrateur|L'aiguille de la balance tremble, puis s'arrête.",
            "enfant-f|Bonjour, une tomate pour le sel !",
            "narrateur|Elle parle à la balance, pas à Nina.",
            "narrateur|Un torchon traîne vers le rond d'huile de l'étal.",
            "narrateur|Nina tend le bras, puis le retire, d'un coup sec.",
            "narrateur|Elle refuse de foncer, et elle regarde le rond.",
            "enfant-f|Quand l'aiguille dort, je peux parler ?",
            "papa|L'aiguille dort, la boulangère lève les yeux.",
            "narrateur|Le store rayé claque, et les bandes bougent, lentes.",
            "narrateur|Le panier de toile attend, ouvert, près des caisses.",
            "maman|Que glisse-t-on, avec le grain de sel ?",
        ),
        (2, 2): L(
            "narrateur|Le voisin a posé son sac en travers de l'étal.",
            "narrateur|Il discute d'un prix, trop fort, trop longtemps.",
            "enfant-f|S'il te plaît, je voudrais passer !",
            "narrateur|Le prix recouvre le mot, et une caisse grince.",
            "narrateur|Nina recule, le ventre serré sous le store.",
            "narrateur|Le rond d'huile est coincé, derrière le sac.",
            "narrateur|Elle n'arrache pas le sac, et elle observe le bois.",
            "enfant-f|Quand le prix est dit, le rond est libre ?",
            "maman|Le prix est dit, son sac glisse, nous t'écoutons.",
            "narrateur|Le rond d'huile réapparaît, clair, sur la planche.",
            "narrateur|Nina souffle, et le panier n'a pas bougé de l'anse.",
            "papa|Que veux-tu mettre, maintenant que l'allée est libre ?",
        ),
        (2, 3): L(
            "narrateur|La maîtresse choisit une tomate, très lente, à l'étal.",
            "narrateur|Maman lui parle d'un cartable, à voix basse.",
            "enfant-f|Maîtresse, attends, le grain !",
            "narrateur|Le mot se perd entre la tomate et le cartable.",
            "narrateur|Nina touche le coude de maman, puis attend.",
            "narrateur|Elle ne coupe plus, et le store s'immobilise un peu.",
            "narrateur|Sur la planche, le rond d'huile garde sa forme.",
            "enfant-f|Quand la tomate est choisie, je dis le grain ?",
            "papa|La tomate est choisie, maman te regarde, nous aussi.",
            "narrateur|La maîtresse s'écarte, liste sous le bras, silencieuse.",
            "narrateur|Le panier de toile s'ouvre, cordon un peu luisant.",
            "maman|Que glisse-t-on, sous le store rayé ?",
        ),
        (3, 1): L(
            "narrateur|À la fromagerie, la boulangère est entrée, tablier blanc.",
            "narrateur|Elle demande du lait, au comptoir, d'une voix pressée.",
            "enfant-f|Bonjour, je peux parler !",
            "narrateur|Le lait recouvre sa phrase, et le blanc est froid.",
            "narrateur|Nina sent le froid aux doigts, et elle se tait.",
            "narrateur|Un torchon de la boulangère frôle un rond d'huile.",
            "narrateur|Le rond est sur une planchette, près du lait.",
            "narrateur|Nina refuse de foncer, et elle suit le rond des yeux.",
            "enfant-f|Quand le lait est dit, je parle ?",
            "papa|Le lait est dit, tes mots ont de la place.",
            "narrateur|Le panier de toile reste ouvert, près du blanc.",
            "maman|Que met-on avec le grain, sur ce comptoir ?",
        ),
        (3, 2): L(
            "narrateur|Le voisin appuie son sac sur le comptoir blanc.",
            "narrateur|Il raconte un fromage d'hier, trop long, trop fort.",
            "enfant-f|Pardon, le sel d'abord !",
            "narrateur|Le récit d'hier recouvre sa phrase, et Nina serre l'anse.",
            "narrateur|Elle recule le panier, et elle refuse de crier.",
            "narrateur|Un rond d'huile luit, coincé sous le bord du sac.",
            "narrateur|Personne ne donne la réponse, et Nina écoute le lieu.",
            "enfant-f|Quand hier est fini, je dis le grain d'à présent ?",
            "maman|Hier est fini, le comptoir t'écoute, nous aussi.",
            "narrateur|Le voisin décale le sac, et le rond d'huile respire.",
            "narrateur|Ça sent la cave, et un peu de thym, sous le store.",
            "papa|Que veux-tu glisser, dans le panier de toile ?",
        ),
        (3, 3): L(
            "narrateur|La maîtresse commande un petit fromage, pour plus tard.",
            "narrateur|Elle parle à maman d'une chanson, près du blanc.",
            "enfant-f|Maîtresse, le grain est là !",
            "narrateur|La chanson et la commande se mélangent, rien n'arrive.",
            "narrateur|Nina ferme les lèvres, l'inquiétude lui pèse au ventre.",
            "narrateur|Elle n'interrompt plus, et elle regarde le rond d'huile.",
            "narrateur|Le rond, sur une planchette, copie celui du début.",
            "enfant-f|Quand la chanson s'arrête, je peux dire le sel ?",
            "papa|La chanson s'arrête, maman se tourne, nous t'écoutons.",
            "narrateur|La maîtresse prend son fromage, sans parler à Nina.",
            "narrateur|Le panier de toile attend, froid du comptoir, ouvert.",
            "maman|Que glisse-t-on, avec le grain, maintenant ?",
        ),
    }
    key = (a, b)
    if key not in scenes:
        raise SystemExit(f"t2 manquant {lieu} {key}")
    return scenes[key]


def t3_q(_b: int) -> list[tuple[str, str]]:
    return L(
        "narrateur|Le panier peut recevoir le pain, une pomme, ou un fromage.",
        "papa|On glisse quoi, avec le grain de sel ?",
    )


def t3_body(b: int, c: int) -> list[tuple[str, str]]:
    scenes = {
        (1, 1): L(
            "narrateur|Nina choisit le pain, et elle ne fonce pas.",
            "narrateur|Une goutte d'huile tombe sur la croûte, ronde.",
            "narrateur|C'est le même rond qu'au début, plus petit.",
            "enfant-f|Le grain va là, au milieu.",
            "narrateur|Elle attend que la goutte s'arrête de glisser.",
            "narrateur|Puis elle pose le sel, tout au centre.",
            "papa|Je n'avais pas vu ce petit rond.",
            "maman|Nous avons regardé ensemble.",
        ),
        (1, 2): L(
            "narrateur|Nina choisit une pomme, et elle refuse de se presser.",
            "narrateur|La peau luit, comme le rond d'huile des planches.",
            "enfant-f|Chut, le rond me montre l'endroit.",
            "narrateur|Elle pose le grain où la pomme brille, un point.",
            "narrateur|Personne ne parle, un moment, sous le store.",
            "papa|La pomme a gardé le sel, sans rouler.",
            "maman|Le panier la tient, cordon un peu gras.",
        ),
        (1, 3): L(
            "narrateur|Nina choisit un fromage, les doigts restés lents.",
            "narrateur|Une larme d'huile fait un rond, sur la pâte pâle.",
            "enfant-f|C'est le rond de la planche.",
            "narrateur|Elle glisse le grain au milieu, sans le casser.",
            "narrateur|La boulangère, plus loin, a rangé son torchon.",
            "papa|Le fromage porte le sel, et l'huile.",
            "maman|Le panier de toile le recouvre un peu.",
        ),
        (2, 1): L(
            "narrateur|Nina prend le pain, mais le sac du voisin gêne.",
            "narrateur|Elle n'arrache rien, et elle attend le décalage.",
            "narrateur|Un rond d'huile apparaît sur la croûte, net.",
            "enfant-f|Là, comme sur la planche.",
            "narrateur|Le grain rejoint le centre, blanc sur le doré.",
            "papa|Ton attente a laissé la place au pain.",
            "maman|Le voisin a vu, lui aussi, sans parler.",
        ),
        (2, 2): L(
            "narrateur|Nina prend une pomme, et le sac bouge, enfin.",
            "narrateur|Elle observe le fruit, pas seulement le chemin.",
            "narrateur|Une tache d'huile, ronde, copie le début.",
            "enfant-f|Le grain, ici, pas plus vite.",
            "narrateur|Elle pose le sel, et la pomme ne fuit pas.",
            "papa|Tu as regardé avant de mettre la main.",
            "maman|Le panier se referme, anse contre l'épaule.",
        ),
        (2, 3): L(
            "narrateur|Nina prend un fromage, après le sac décalé.",
            "narrateur|Elle écoute le lieu : un vélo, le store, rien d'autre.",
            "narrateur|Le rond d'huile du début revient, sur la pâte.",
            "enfant-f|Je le mets au milieu, sans me presser.",
            "narrateur|Le grain tient, et un silence court suit le geste.",
            "papa|Le fromage a son grain, sans se casser.",
            "maman|On a laissé le voisin finir, d'abord.",
        ),
        (3, 1): L(
            "narrateur|Nina choisit le pain, la liste de la maîtresse close.",
            "narrateur|Elle ne coupe plus, et elle regarde la croûte.",
            "narrateur|Un rond d'huile s'y pose, fidèle à la planche.",
            "enfant-f|Le grain, maintenant.",
            "narrateur|Le sel rejoint le rond, et la miche sent le thym.",
            "papa|Ta phrase est arrivée, entière, après la liste.",
            "maman|Le panier porte le pain, et le grain.",
        ),
        (3, 2): L(
            "narrateur|Nina choisit une pomme, après la chanson finie.",
            "narrateur|Elle observe le fruit, écoute le store, retrouve le rond.",
            "enfant-f|Il est là, sur la peau, tout petit.",
            "narrateur|Le grain se pose, et la pomme luit comme la planche.",
            "narrateur|La maîtresse s'éloigne, fromage sous le bras, sans mot.",
            "papa|Tu as attendu la fin, puis tu as vu.",
            "maman|Le panier de toile garde la pomme, au frais.",
        ),
        (3, 3): L(
            "narrateur|Nina choisit un fromage, et elle laisse le silence d'abord.",
            "narrateur|Personne ne souffle la réponse, et elle cherche le rond.",
            "narrateur|Sur la pâte, l'huile refait la lune du début.",
            "enfant-f|Le grain va au centre, pas à côté.",
            "narrateur|Le sel tient, et le panier se referme, lentement.",
            "papa|Le fromage a son grain, et son rond.",
            "maman|Nous t'avons laissé finir, jusqu'au bout.",
        ),
    }
    return scenes[(b, c)]


CALLBACKS = {
    (1, 1, 1): "Le grain laisse une poussière blanche sur la croûte.",
    (1, 1, 2): "Une larme d'huile brille sur la pomme, ronde.",
    (1, 1, 3): "Le fromage garde un point de sel, luisant.",
    (1, 2, 1): "Le cordon rouge sent le pain, et l'huile.",
    (1, 2, 2): "Le cordon rouge a une tache claire, ronde.",
    (1, 2, 3): "Le cordon rouge frotte le papier du fromage.",
    (1, 3, 1): "L'ombre du store barre la miche, puis s'en va.",
    (1, 3, 2): "L'ombre du store glisse sur la pomme, lente.",
    (1, 3, 3): "L'ombre du store touche le fromage, puis part.",
    (2, 1, 1): "Une tomate du panier luit, comme le rond d'huile.",
    (2, 1, 2): "La peau de la pomme reprend le rond, minuscule.",
    (2, 1, 3): "Le fromage a un petit miroir d'huile, au centre.",
    (2, 2, 1): "Les planches gardent une lune d'huile, pâle.",
    (2, 2, 2): "Les planches sentent la pomme, et l'huile tiède.",
    (2, 2, 3): "Les planches sentent le lait, sous le store rayé.",
    (2, 3, 1): "Nina n'a pas foncé, et le pain est dans l'anse.",
    (2, 3, 2): "Nina n'a pas foncé, et la pomme est au fond.",
    (2, 3, 3): "Nina n'a pas foncé, et le fromage est au frais.",
    (3, 1, 1): "Le grain a quitté le rond, et la miche le porte.",
    (3, 1, 2): "Le grain a quitté le rond, et la pomme le porte.",
    (3, 1, 3): "Le grain a quitté le rond, et le fromage le porte.",
    (3, 2, 1): "Un silence court reste, entre le pain et le sel.",
    (3, 2, 2): "Un silence court reste, entre la pomme et le sel.",
    (3, 2, 3): "Un silence court reste, entre le fromage et le sel.",
    (3, 3, 1): "Le panier de toile pèse, pain et sel ensemble.",
    (3, 3, 2): "Le panier de toile pèse, pomme et sel ensemble.",
    (3, 3, 3): "Le panier de toile pèse, fromage et sel ensemble.",
}

CHILD1 = {
    (1, 1, 1): "J'ai mis le grain au milieu du pain.",
    (1, 1, 2): "J'ai suivi le rond, sur la pomme.",
    (1, 1, 3): "J'ai posé le sel sur le fromage.",
    (1, 2, 1): "J'ai attendu le melon, puis le pain.",
    (1, 2, 2): "J'ai attendu le sac, puis la pomme.",
    (1, 2, 3): "J'ai attendu hier, puis le fromage.",
    (1, 3, 1): "J'ai laissé finir la liste, puis le pain.",
    (1, 3, 2): "J'ai laissé finir la chanson, puis la pomme.",
    (1, 3, 3): "J'ai laissé le silence, puis le fromage.",
    (2, 1, 1): "L'aiguille a dormi, puis le pain est venu.",
    (2, 1, 2): "L'aiguille a dormi, puis la pomme est venue.",
    (2, 1, 3): "L'aiguille a dormi, puis le fromage est venu.",
    (2, 2, 1): "Le prix s'est tu, puis le pain a glissé.",
    (2, 2, 2): "Le prix s'est tu, puis la pomme a glissé.",
    (2, 2, 3): "Le prix s'est tu, puis le fromage a glissé.",
    (2, 3, 1): "La tomate choisie, le pain a suivi.",
    (2, 3, 2): "La tomate choisie, la pomme a suivi.",
    (2, 3, 3): "La tomate choisie, le fromage a suivi.",
    (3, 1, 1): "Le lait dit, le pain a pris le grain.",
    (3, 1, 2): "Le lait dit, la pomme a pris le grain.",
    (3, 1, 3): "Le lait dit, le fromage a pris le grain.",
    (3, 2, 1): "Le sac décalé, le pain a trouvé le rond.",
    (3, 2, 2): "Le sac décalé, la pomme a trouvé le rond.",
    (3, 2, 3): "Le sac décalé, le fromage a trouvé le rond.",
    (3, 3, 1): "Après la chanson, le pain a eu son sel.",
    (3, 3, 2): "Après la chanson, la pomme a eu son sel.",
    (3, 3, 3): "Après la chanson, le fromage a eu son sel.",
}

CHILD2 = {
    (1, 1, 1): "Le rond d'huile était sur la croûte.",
    (1, 1, 2): "Le rond d'huile était sur la peau.",
    (1, 1, 3): "Le rond d'huile était sur la pâte.",
    (1, 2, 1): "Le melon s'est tu, et j'ai parlé.",
    (1, 2, 2): "Le sac a bougé, et j'ai parlé.",
    (1, 2, 3): "Hier s'est tu, et j'ai parlé.",
    (1, 3, 1): "La liste close, mes mots sont arrivés.",
    (1, 3, 2): "La chanson close, mes mots sont arrivés.",
    (1, 3, 3): "Le silence m'a rendu la place.",
    (2, 1, 1): "La balance s'est tue, comme le store.",
    (2, 1, 2): "La balance s'est tue, près des caisses.",
    (2, 1, 3): "La balance s'est tue, sous les bandes.",
    (2, 2, 1): "L'allée s'est ouverte, pain au fond.",
    (2, 2, 2): "L'allée s'est ouverte, pomme au fond.",
    (2, 2, 3): "L'allée s'est ouverte, fromage au fond.",
    (2, 3, 1): "Maman s'est tournée, et le pain aussi.",
    (2, 3, 2): "Maman s'est tournée, et la pomme aussi.",
    (2, 3, 3): "Maman s'est tournée, et le fromage aussi.",
    (3, 1, 1): "Le comptoir froid a gardé le pain.",
    (3, 1, 2): "Le comptoir froid a gardé la pomme.",
    (3, 1, 3): "Le comptoir froid a gardé le fromage.",
    (3, 2, 1): "Le rond coincé s'est libéré, sous le pain.",
    (3, 2, 2): "Le rond coincé s'est libéré, sous la pomme.",
    (3, 2, 3): "Le rond coincé s'est libéré, sous le fromage.",
    (3, 3, 1): "Le grain a trouvé sa lune, sur le pain.",
    (3, 3, 2): "Le grain a trouvé sa lune, sur la pomme.",
    (3, 3, 3): "Le grain a trouvé sa lune, sur le fromage.",
}

LAST = {
    (1, 1, 1): "Sur la planche du début, le rond d'huile pâlit, vide.",
    (1, 1, 2): "Sur la planche du début, le rond d'huile copie la pomme.",
    (1, 1, 3): "Sur la planche du début, le rond d'huile copie le fromage.",
    (1, 2, 1): "L'allée des planches sent le pain, et l'huile sèche.",
    (1, 2, 2): "L'allée des planches sent la pomme, et l'huile sèche.",
    (1, 2, 3): "L'allée des planches sent le fromage, et l'huile sèche.",
    (1, 3, 1): "Le store rayé jette une bande, sur la miche du panier.",
    (1, 3, 2): "Le store rayé jette une bande, sur la pomme du panier.",
    (1, 3, 3): "Le store rayé jette une bande, sur le fromage du panier.",
    (2, 1, 1): "Une tomate, dans le toile, luit comme le premier rond.",
    (2, 1, 2): "Une tomate, dans le toile, veille près de la pomme.",
    (2, 1, 3): "Une tomate, dans le toile, veille près du fromage.",
    (2, 2, 1): "Les caisses se taisent, et le pain garde son grain.",
    (2, 2, 2): "Les caisses se taisent, et la pomme garde son grain.",
    (2, 2, 3): "Les caisses se taisent, et le fromage garde son grain.",
    (2, 3, 1): "Le cordon rouge a une tache ronde, près du pain.",
    (2, 3, 2): "Le cordon rouge a une tache ronde, près de la pomme.",
    (2, 3, 3): "Le cordon rouge a une tache ronde, près du fromage.",
    (3, 1, 1): "Le comptoir blanc reflète le pain, et plus le grain.",
    (3, 1, 2): "Le comptoir blanc reflète la pomme, et plus le grain.",
    (3, 1, 3): "Le comptoir blanc reflète le fromage, et plus le grain.",
    (3, 2, 1): "Sous le store, le pain pèse, sel au centre de la croûte.",
    (3, 2, 2): "Sous le store, la pomme pèse, sel au point de la peau.",
    (3, 2, 3): "Sous le store, le fromage pèse, sel au milieu de l'huile.",
    (3, 3, 1): "La planche du début garde une lune pâle, sans grain.",
    (3, 3, 2): "La planche du début garde une lune pâle, goût de pomme.",
    (3, 3, 3): "La planche du début garde une lune pâle, goût de cave.",
}

RETURN = {
    1: "Sous le store rayé, la boulangerie rend sa chaleur.",
    2: "Dans l'allée des planches, l'étal range ses caisses.",
    3: "Près du comptoir blanc, la fromagerie se fait plus calme.",
}

KEEP = {
    1: "Le panier de toile sent la croûte, un peu d'huile au cordon.",
    2: "Le panier de toile sent la tomate, un peu d'huile au cordon.",
    3: "Le panier de toile sent le lait, un peu d'huile au cordon.",
}


def ending(a: int, b: int, c: int) -> list[tuple[str, str]]:
    key = (a, b, c)
    return L(
        f"narrateur|{RETURN[a]}",
        "maman|À toi, Nina.",
        "maman|Nous t'écoutons.",
        "papa|Le rond d'huile, il est où, maintenant ?",
        f"enfant-f|{CHILD1[key]}",
        f"enfant-f|{CHILD2[key]}",
        f"narrateur|{KEEP[a]}",
        f"narrateur|{LAST[key]}",
    )


def t3_passage(a: int, b: int, c: int) -> list[tuple[str, str]]:
    body = list(t3_body(b, c))
    cb = CALLBACKS[(a, b, c)]
    n = wc(cb)
    if n > LIM:
        raise SystemExit(f"callback {n}: {cb}")
    body.append(("narrateur", cb))
    return body


def _check_maps() -> None:
    for dname, d in (
        ("CALLBACKS", CALLBACKS),
        ("CHILD1", CHILD1),
        ("CHILD2", CHILD2),
        ("LAST", LAST),
    ):
        if len(d) != 27:
            raise SystemExit(f"{dname} {len(d)}")
        for k, s in d.items():
            n = wc(s)
            if n > LIM:
                raise SystemExit(f"{dname} {k} {n}>{LIM}: {s}")
            marks = s.count(".") + s.count("?") + s.count("!")
            if marks != 1:
                raise SystemExit(f"{dname} {k} punct {marks}: {s}")
            if TICS.search(s):
                raise SystemExit(f"{dname} tic: {s}")
            if BAD_WORLD.search(s):
                raise SystemExit(f"{dname} monde: {s}")
    for k, s in list(KEEP.items()) + list(RETURN.items()):
        if wc(s) > LIM:
            raise SystemExit(f"map {wc(s)}>{LIM}: {s}")
        if TICS.search(s):
            raise SystemExit(f"tic map: {s}")
    if len(set(CALLBACKS.values())) != 27:
        raise SystemExit("CALLBACKS non distincts")
    if len(set(LAST.values())) != 27:
        raise SystemExit("LAST non distincts")
    if len(set(CHILD1.values())) != 27:
        raise SystemExit("CHILD1 non distincts")
    if len(set(CHILD2.values())) != 27:
        raise SystemExit("CHILD2 non distincts")


def main() -> None:
    _check_maps()
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: deepcopy(c) for c in src["chunks"]}

    voice(
        by["CHK_T0000_P0000"],
        L(
            "narrateur|Le cordon rouge a laissé un trait chaud dans sa paume.",
            "narrateur|Elle ouvre les doigts, au-dessus des planches du marché.",
            "narrateur|Le store rayé jette des bandes d'ombre, blanches et bleues.",
            "narrateur|Au milieu d'une planche, un rond d'huile brille.",
            "narrateur|Un grain de sel y tient, blanc comme un petit caillou.",
            "narrateur|Papa glisse des pièces dans une petite bourse de cuir.",
            "narrateur|En ce moment, Nina veut le grain de sel, tout de suite.",
            "enfant-f|Le sel, pour les tomates !",
            "narrateur|Elle parle pendant que papa compte, trop vite.",
            "narrateur|Les mots se perdent entre les pièces, sans oreille.",
            "narrateur|Personne ne tourne la tête, sous le store.",
            "narrateur|Le sourire de Nina disparaît, d'un coup.",
            "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
            "narrateur|Elle ferme la bouche, panier contre la hanche.",
            "narrateur|Papa s'accroupit, à la même hauteur que ses yeux.",
            "papa|Tu disais, Nina ?",
            "enfant-f|Le grain de sel, pour les tomates.",
            "maman|Nous t'écoutons, maintenant.",
            "papa|Merci d'avoir attendu.",
            "narrateur|Le rond d'huile tremble, quand le store claque.",
        ),
        "opening",
        extra={"sons": "marche,store,pieces"},
    )

    voice(
        by["CHK_T0001_P0000"],
        L(
            "narrateur|Le panier part avec elle, vers trois allées.",
            "papa|Où va le panier, d'abord ?",
            "maman|La boulangerie, l'étal, ou la fromagerie ?",
        ),
        "choice",
        extra={
            "fields": {
                "option_1_label": "la boulangerie",
                "option_2_label": "l'étal",
                "option_3_label": "la fromagerie",
            }
        },
    )

    t1_sons = {1: "four,pain", 2: "caisse,tomate", 3: "lait,verre"}
    t1_emp = {1: "grain de sel", 2: "rond d'huile", 3: "panier"}
    t2_sons = {1: "torchon,planche", 2: "sac,marche", 3: "papier,voix"}
    t2_emp = {1: "rond d'huile", 2: "rond d'huile", 3: "rond d'huile"}
    t3_emp = {1: "pain", 2: "pomme", 3: "fromage"}
    fin_sons = {1: "pain,store", 2: "tomate,store", 3: "fromage,store"}

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        voice(by[base], t1_passage(a), "action", extra={"sons": t1_sons[a], "emphasis": t1_emp[a]})
        q_lines, q_fields = t1_q(a)
        voice(
            by[f"{base}_Q0001"],
            q_lines,
            "clue",
            extra={"emphasis": t1_emp[a], "fields": q_fields},
        )
        voice(by[f"{base}_C0001"], t1_confirm(a), "confirm", extra={"emphasis": t1_emp[a]})
        voice(
            by[f"{base}_T0002_P0000"],
            L(
                "narrateur|Trois personnes sont là, tout près, sous le store.",
                "maman|On s'adresse à qui, d'abord ?",
                "papa|La boulangère, le voisin, ou la maîtresse ?",
            ),
            "choice",
            extra={
                "fields": {
                    "option_1_label": "la boulangère",
                    "option_2_label": "le voisin",
                    "option_3_label": "la maîtresse",
                }
            },
        )
        for b in (1, 2, 3):
            loc_id = f"{base}_T0002_P000{b}"
            voice(
                by[loc_id],
                t2_passage(a, b),
                "obstacle",
                extra={
                    "sons": t2_sons[b],
                    "emphasis": t2_emp[b],
                    "notes": PROFILES["obstacle"]["note"] + f"; revers=2e_ruse; lieu={a}; personne={b}",
                },
            )
            voice(
                by[f"{loc_id}_T0003_P0000"],
                t3_q(b),
                "choice",
                extra={
                    "fields": {
                        "option_1_label": "le pain",
                        "option_2_label": "une pomme",
                        "option_3_label": "un fromage",
                    }
                },
            )
            for c in (1, 2, 3):
                leaf = f"{loc_id}_T0003_P000{c}"
                voice(
                    by[leaf],
                    t3_passage(a, b, c),
                    "resolution",
                    extra={"sons": t1_sons[c] if c != 2 else "pomme,huile", "emphasis": t3_emp[c]},
                )
                voice(
                    by[f"{leaf}_F0001"],
                    ending(a, b, c),
                    "ending",
                    extra={"sons": fin_sons[a], "emphasis": "rond d'huile"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra_ids = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    fins = [by[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(fins) != 27:
        raise SystemExit(f"fins {len(fins)}")
    if len(set(fins)) != 27:
        raise SystemExit("fins non distinctes")

    t2s = [
        by[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c.get("kind") == "passage"
        and "_T0002_P000" in c["chunk_id"]
        and "_T0003_" not in c["chunk_id"]
        and not c["chunk_id"].endswith("_P0000")
    ]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"T2 distincts: {len(set(t2s))}/{len(t2s)}")

    t3s = [
        by[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c.get("kind") == "passage"
        and "_T0003_P000" in c["chunk_id"]
        and not c["chunk_id"].endswith("_P0000")
        and "_F0001" not in c["chunk_id"]
    ]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"T3 distincts: {len(set(t3s))}/{len(t3s)}")

    out = dict(src)
    out["fil_rouge"] = (
        "Sous le store rayé, un rond d'huile brille sur une planche du marché. "
        "Un grain de sel y tient. Nina veut le porter dans son panier de toile "
        "jusqu'aux tomates, maintenant. Elle parle pendant que papa compte : "
        "personne n'entend. Elle attend, papa s'accroupit, on l'écoute. "
        "Le panier part avec elle vers la boulangerie, l'étal ou la fromagerie. "
        "La boulangère, le voisin ou la maîtresse (sans rôle parlé) allongent "
        "le revers : envie de couper, retenue, rond d'huile menacé, Nina refuse "
        "de foncer. Pain, pomme ou fromage reçoivent le grain au centre du rond. "
        "À la fin, le rond pâlit, vide, et chacun l'écoute jusqu'au bout."
    )
    out["title"] = TITLE
    out["characters"] = "Nina, papa, maman"
    out["setting"] = "marché, planches et store rayé"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]

    joined = "\n".join(c["script"] for c in out["chunks"])
    if TICS.search(joined):
        raise SystemExit(f"tic global: {TICS.search(joined).group(0)}")
    if BAD_WORLD.search(joined):
        raise SystemExit(f"monde voisin global: {BAD_WORLD.search(joined).group(0)}")
    low = joined.lower()
    for bad in (
        "aujourd'hui,",
        "mission accomplie",
        "j'ai compris",
        "on va apprendre",
        "voici le geste",
        "maitresse|",
        "maîtresse|",
    ):
        if bad in low:
            raise SystemExit(f"interdit: {bad}")
    roles = {ln.split("|", 1)[0] for ln in joined.splitlines() if "|" in ln}
    if not roles <= {"narrateur", "papa", "maman", "enfant-f"}:
        raise SystemExit(f"rôles: {roles}")

    check(SID, out["age_band"], out["chunks"])

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
    lo, hi, avg = min(pw), max(pw), sum(pw) // len(pw)
    print(f"chemins {lo}-{hi} mots, moy {avg}")
    if lo < 540:
        raise SystemExit(f"chemins trop courts: {lo}")
    if hi > 720:
        raise SystemExit(f"chemins trop longs: {hi}")

    notes = [c.get("notes") or "" for c in out["chunks"]]
    if any(not n for n in notes):
        raise SystemExit("notes manquantes")
    if any(not (c.get("text_xai_tags") or "") for c in out["chunks"]):
        raise SystemExit("xai manquant")
    if any("<speak>" not in (c.get("text_ssml") or "") for c in out["chunks"]):
        raise SystemExit("ssml manquant")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés. Graphe source conservé "
        "(boulangerie / étal / fromagerie ; boulangère / voisin / maîtresse ; "
        "pain / pomme / fromage).\n\n"
        "## Promesse narrative\n\n"
        "Sous le store rayé, sur l'allée des planches, un rond d'huile brille. "
        "Un grain de sel y tient, blanc. Nina veut le porter dans son panier "
        "de toile jusqu'aux tomates, maintenant. Elle parle pendant que papa "
        "compte les pièces : personne n'entend. Elle attend, papa s'accroupit, "
        "on l'écoute. Le panier part avec elle. La boulangère, le voisin ou "
        "la maîtresse (présente, sans rôle parlé) allongent le revers : envie "
        "de couper, retenue, rond d'huile menacé, Nina refuse de foncer. "
        "Pain, pomme ou fromage reçoivent le grain au centre d'un rond d'huile "
        "qui paie l'ouverture. Le rond du début pâlit, vide.\n\n"
        "## Vécu\n\n"
        "- Désir : porter le grain de sel dans le panier jusqu'aux tomates.\n"
        "- Imprévu 1 : parole coupée par les pièces ; grain qui glisse.\n"
        "- Imprévu 2 (plus rusé) : torchon / sac / deux voix, rond d'huile menacé, "
        "Nina refuse de foncer, observe l'indice du début.\n"
        "- COL.POL.001 vécu : envie de couper, retenue, écoute réelle, plaisir "
        "d'être entendu. Jamais dit comme règle. Adulte conversationnel.\n"
        "- Merci vécu : « Merci d'avoir attendu. » (papa, ouverture).\n"
        f"- 27 fins distinctes. Chemins {lo}–{hi} mots (moyenne {avg}).\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Troupe D16 : Nina, papa, maman. Pas de 2e enfant.\n"
        "- 86 nœuds, graphe et libellés d'options conservés (y compris « la maîtresse »).\n"
        "- Pas de rôle `maîtresse|` : elle est dans la file, papa/maman parlent.\n"
        "- 27 fins, 27 T3, 9 T2 textuellement distincts.\n"
        "- Première tentative échoue. Chaque choix change l'obstacle, le climax, la dernière image.\n"
        "- Objet nommé : grain de sel (blanc, minuscule, papier, mission).\n"
        "- Équipement : panier de toile, cordon rouge — part AVEC dès T1.\n"
        "- Coin inventif : l'allée des planches, sous le store rayé.\n"
        "- Indice unique dès l'ouverture : rond d'huile, payé au climax. "
        "Pas le grain de sel (objet-titre).\n"
        "- Monde ≠ TREE-AUT-045 (osier, paprika), ≠ TREE-DIF-008 (cannelle, stores couleur), "
        "≠ TREE-COL-027 (toiles, osier), ≠ TREE-COL-035 (goutte, trois mots, farine).\n"
        "- TTS par fonction (ouverture, choix, indice, confirmation, action, obstacle, résolution, retour).\n"
        "- `slow` réservé aux choix, à l'indice et aux fins.\n"
        "- N3 ≤ 16 mots/phrase. Pas de leçon dite. Pas de tics « tout doux / encore / déjà / tout calme ».\n"
        "- Pas de refrains example3. Pas de merle / miel. Pas apply. Pas audio.\n\n"
        "## Direction vocale\n\n"
        "`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, "
        "tempo, sourire, respiration. Adulte conversationnel, pas maîtresse. Tours "
        "de parole : envie de couper, retenue, écoute réelle, plaisir d'être entendu.\n\n"
        "## Contrôles\n\n"
        "- 86 chunks, graphe `option_*_next` / `default_next` conservé\n"
        "- 27 chemins, 27 fins textuellement distinctes\n"
        f"- {lo} à {hi} mots par chemin, moyenne {avg} (N3)\n"
        "- `check()` OK (N3 ≤ 16 mots/phrase)\n"
        "- `text` et `script` synchronisés\n"
        "- `text_ssml` et `text_xai_tags` enrichis sur les 86 chunks\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
