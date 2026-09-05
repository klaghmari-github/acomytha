#!/usr/bin/env python3
"""TREE-AUT-016 — Le manteau de laine de Raphaël (F-NAR-019, N1, AUT.AFF.002, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-016"
N1 = LIMITS["N1"]
TITLE = "Le manteau de laine de Raphaël"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="manteau",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=la_boucle_rousse_attend_sur_la_poche; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="manteau",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qui_pèse_sur_les_épaules; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="manteau",
        note="arc=confirmation; intention=relancer; emotion=élan; intensite=1; destinataire=enfant; sous_texte=les_épaules_ont_gardé_le_beige; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=il_veut_lancer_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=l_outil_aggrave_la_perte; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="manteau",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=la_boucle_rousse_rend_la_poche; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="manteau",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_boucle_rousse_garde_une_goutte; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    starts: list[str] = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"fin: {ph}")
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        tok = ph.split()[0].lower() if role == "narrateur" else ""
        starts.append(tok)
        out.append(f"{role}|{ph}")
    run = 1
    for i in range(1, len(starts)):
        if starts[i] and starts[i] == starts[i - 1]:
            run += 1
            if run >= 4:
                raise SystemExit(f"puces {starts[i]}")
        else:
            run = 1
    return out


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp:
        e = esc(emp)
        if e in body:
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
    tag = m.get("pitchTag")
    if tag:
        body = f"<{tag}>{body}</{tag}>"
    pause = m["pause"]
    suffix = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + suffix).strip()


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    lines = vet(lines)
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if extra.get("note"):
        m["note"] = extra["note"]
    text, script = from_script(lines)
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
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
    nc["emphasis_words"] = m.get("emphasis") or ""
    nc["pause_before_ms"] = extra.get("pause_before_ms", 0)
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
    for k, v in extra.items():
        if k in ("emphasis", "note", "pause_before_ms"):
            continue
        nc[k] = v
    return nc


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=la_boucle_rousse_garde_la_goutte; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


OPENING = [
    "narrateur|Les pieds de Raphaël tapent le tapis beige.",
    "narrateur|Il veut la flaque, là, tout de suite.",
    "narrateur|La pluie a fait des bateaux sur la vitre.",
    "narrateur|Le radiateur fait tic, contre le crochet.",
    "narrateur|Au crochet bas, un manteau de laine attend.",
    "narrateur|Il est beige, lourd, un peu rêche.",
    "narrateur|Son bouton-gland pèse, rond comme un gland.",
    "narrateur|Une boucle rousse pend de la poche.",
    "papa|Tu as vu la boucle, Raphaël ?",
    "enfant-m|Je veux la flaque, et mon bateau !",
    "maman|Le bateau-feuille peut dormir dans la poche.",
    "narrateur|En ce moment, Raphaël saute vers le crochet.",
    "enfant-m|Je le prends, et je cours dehors !",
    "narrateur|Il enfile un bras, trop vite, de travers.",
    "narrateur|La manche est à l'envers, coincée.",
    "narrateur|Le bouton-gland reste muet, sans toc.",
    "narrateur|La feuille glisse vers le tapis beige.",
    "enfant-m|Il ne veut pas rentrer !",
    "narrateur|Le sourire de Raphaël disparaît.",
    "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
    "papa|L'autre bras d'abord, puis le toc.",
    "narrateur|Papa s'accroupit, à la même hauteur.",
    "enfant-m|Je veux mon bateau, à la flaque !",
    "maman|La feuille attend tes deux manches.",
    "narrateur|Il glisse le second bras, plus lent.",
    "narrateur|Le toc parle, et la feuille rentre.",
    "papa|Merci d'avoir mis tes deux bras.",
    "narrateur|La boucle rousse dépasse, mince, vers le sol.",
]

T1_CHOICE = [
    "narrateur|Le manteau tient chaud, la feuille dans la poche.",
    "narrateur|La cuisine, le jardin, ou la chambre.",
    "maman|Où vas-tu d'abord, Raphaël ?",
]

T1 = {
    1: dict(
        lab="la cuisine",
        sons="soupe,vapeur",
        emp="vapeur",
        retry="Le manteau est resté. Qu'est-ce qui pèse ?",
        passage=[
            "narrateur|Raphaël pousse la porte du fournil.",
            "narrateur|Ça sent la soupe dans la casserole.",
            "narrateur|Les carreaux sont tièdes sous les bottes.",
            "narrateur|La vitre de la cuisine est embuée.",
            "enfant-m|Je montre la mer à mon bateau !",
            "narrateur|Il presse la poche contre la buée.",
            "narrateur|Trop vite, la feuille colle au verre.",
            "narrateur|Le manteau beige se cache dans la vapeur.",
            "enfant-m|Je ne le vois plus !",
            "narrateur|Le sourire de Raphaël part.",
            "papa|La vapeur a pris ta poche.",
            "narrateur|Maman s'accroupit, près des bottes jaunes.",
            "enfant-m|Je le veux, mon bateau !",
            "narrateur|La boucle rousse brille, collée à la buée.",
            "papa|Le manteau est sur toi, lui pas.",
        ],
        question=[
            "narrateur|La vapeur a caché quelque chose de lourd.",
            "maman|Qu'est-ce qui est resté sur ses épaules ?",
        ],
        confirm=[
            "narrateur|La boucle rousse tremble sur la vitre.",
            "enfant-m|Je remets la feuille, après.",
            "maman|Tes épaules ont gardé le manteau.",
            "papa|On prend la feuille, puis le toc.",
            "enfant-m|Oui, papa.",
            "narrateur|La poche redevient un nid, un peu humide.",
            "papa|Tu l'as vue, la boucle ?",
            "enfant-m|Elle était là, sous la vapeur.",
        ],
    ),
    2: dict(
        lab="le jardin",
        sons="pluie,bottes",
        emp="vent",
        retry="Le manteau pèse. Qu'est-ce qui pèse dehors ?",
        passage=[
            "narrateur|Raphaël ouvre la porte du jardin.",
            "narrateur|Le phare des dalles brille, plein d'eau.",
            "enfant-m|Mon bateau va nager, tout de suite !",
            "narrateur|Le vent tourne la manche, trop fort.",
            "narrateur|La poche se vide vers une botte.",
            "narrateur|Le bouton-gland se tait, mouillé.",
            "enfant-m|Il est parti dans l'eau !",
            "narrateur|Le sourire de Raphaël part.",
            "papa|Le vent a trop poussé.",
            "narrateur|Maman s'accroupit, à la même hauteur.",
            "enfant-m|Je le veux, près de moi !",
            "narrateur|La boucle rousse colle à la botte.",
            "papa|Le manteau reste sur tes épaules.",
            "narrateur|Une dalle luit, comme un petit port.",
            "enfant-m|Elle brille trop, je n'ose plus.",
        ],
        question=[
            "narrateur|Le vent a trop poussé la poche.",
            "papa|Qu'est-ce qui pèse sur ses épaules ?",
        ],
        confirm=[
            "narrateur|La boucle rousse colle au caoutchouc jaune.",
            "enfant-m|Je remets la feuille, après.",
            "papa|Tes épaules ont gardé le manteau.",
            "maman|On prend la feuille, puis le toc.",
            "enfant-m|Oui, maman.",
            "narrateur|La poche redevient un nid, un peu mouillé.",
            "papa|Tu l'as vue, la boucle ?",
            "enfant-m|Elle était là, malgré le vent.",
        ],
    ),
    3: dict(
        lab="la chambre",
        sons="tissu,doudou",
        emp="sommier",
        retry="Le manteau est sur lui. Qu'est-ce qui pèse ?",
        passage=[
            "narrateur|Raphaël entre dans le hangar du lit.",
            "narrateur|Le doudou attend, capitaine du bateau.",
            "enfant-m|Toi dans la poche, on part !",
            "narrateur|Il s'agenouille trop vite, près du lit.",
            "narrateur|La poche se vide sous le sommier.",
            "narrateur|Le bouton-gland frotte le drap, sans toc.",
            "enfant-m|Il s'est caché dessous !",
            "narrateur|Le sourire de Raphaël part.",
            "papa|Le manteau est sur toi.",
            "narrateur|Maman s'accroupit, près du doudou.",
            "enfant-m|Je le veux, mon bateau !",
            "narrateur|La boucle rousse pointe sous le lit.",
            "papa|Tes épaules l'ont, lui pas.",
            "narrateur|Le doudou penche l'oreille, trop loin.",
            "enfant-m|C'est trop noir, dessous.",
        ],
        question=[
            "narrateur|La feuille a glissé, pas le tissu.",
            "maman|Qu'est-ce qui est resté sur ses épaules ?",
        ],
        confirm=[
            "narrateur|La boucle rousse pointe sous le sommier.",
            "enfant-m|Je remets la feuille, après.",
            "maman|Tes épaules ont gardé le manteau.",
            "papa|On prend la feuille, puis le toc.",
            "enfant-m|Oui, papa.",
            "narrateur|La poche redevient un nid, un peu rêche.",
            "papa|Tu l'as vue, la boucle ?",
            "enfant-m|Elle était là, sur moi.",
        ],
    ),
}

T2_CHOICE = {
    1: [
        "narrateur|La feuille colle à la buée, trop haut.",
        "narrateur|Les cubes, le livre, ou la dînette.",
        "papa|Tu prends quoi, pour la rattraper ?",
    ],
    2: [
        "narrateur|La feuille colle à la botte, trop loin.",
        "narrateur|Les cubes, le livre, ou la dînette.",
        "maman|Tu prends quoi, pour la rattraper ?",
    ],
    3: [
        "narrateur|La feuille attend sous le lit, trop loin.",
        "narrateur|Les cubes, le livre, ou la dînette.",
        "papa|Tu prends quoi, pour la rattraper ?",
    ],
}

T2 = {
    (1, 1): [
        "narrateur|Au fournil, la feuille colle à la buée.",
        "narrateur|Raphaël empile les cubes vers la vitre.",
        "enfant-m|Je monte, et je l'attrape !",
        "narrateur|La tour penche.",
        "narrateur|Un cube tombe.",
        "narrateur|La vapeur pousse la feuille plus haut.",
        "papa|Elle a grimpé, plus loin.",
        "enfant-m|Elle est trop haute, maintenant !",
        "narrateur|Raphaël s'arrête, les mains tièdes.",
        "narrateur|Dans sa poitrine, l'envie recule un peu.",
        "enfant-m|Pas trop vite, cette fois.",
        "narrateur|Il écoute la casserole, puis le tic.",
        "narrateur|La boucle rousse tremble, trop haut.",
        "papa|C'est celle du crochet, tu vois ?",
        "enfant-m|Oui, elle pendait à la poche.",
    ],
    (1, 2): [
        "narrateur|Au fournil, la feuille colle à la buée.",
        "narrateur|Raphaël évente le verre avec le livre.",
        "enfant-m|La mer va s'en aller !",
        "narrateur|La buée part, puis revient plus épaisse.",
        "narrateur|La feuille disparaît dans le nuage.",
        "maman|La soupe répond, plus chaude.",
        "enfant-m|Je ne la vois plus du tout !",
        "narrateur|Raphaël baisse le livre, trop lourd.",
        "narrateur|Dans sa poitrine, la peur pousse fort.",
        "enfant-m|J'attends un peu.",
        "narrateur|Il pose le livre, et il écoute.",
        "narrateur|La casserole chante, tout près du verre.",
        "narrateur|La boucle rousse brille, puis se cache.",
        "maman|Elle était au salon, tu te souviens ?",
        "enfant-m|Oui, sur la poche, dès le tapis.",
    ],
    (1, 3): [
        "narrateur|Au fournil, la feuille colle à la buée.",
        "narrateur|Raphaël lève une tasse vers le verre.",
        "enfant-m|Entre, petit bateau !",
        "narrateur|La tasse se remplit d'eau de vapeur.",
        "narrateur|La feuille colle au fond, invisible.",
        "papa|L'outil a caché ce qu'il prenait.",
        "enfant-m|Elle est au fond, je ne vois rien !",
        "narrateur|Raphaël penche la tasse, trop vite.",
        "narrateur|Dans sa poitrine, l'envie se serre.",
        "enfant-m|Je regarde d'abord.",
        "narrateur|Il pose la tasse, sans verser.",
        "narrateur|La petite cuillère tinte, comme un toc.",
        "narrateur|La boucle rousse reste collée au bord.",
        "papa|Tu la reconnais, la boucle ?",
        "enfant-m|Oui, c'est celle du manteau.",
    ],
    (2, 1): [
        "narrateur|Au phare des dalles, la feuille colle.",
        "narrateur|Raphaël pose des cubes vers la flaque.",
        "enfant-m|Un chemin, pour mon bateau !",
        "narrateur|La pluie renverse deux cubes, net.",
        "narrateur|La manche traîne le dernier, dans l'eau.",
        "papa|Ta manche a trop aidé.",
        "enfant-m|Elle est sous le cube, maintenant !",
        "narrateur|Raphaël retire la manche, trop tard.",
        "narrateur|Dans sa poitrine, la peur pique.",
        "enfant-m|Je m'arrête.",
        "narrateur|Il écoute la pluie, et les dalles.",
        "narrateur|Un cube luit, plein d'eau de dalle.",
        "narrateur|La boucle rousse flotte, collée au bois.",
        "papa|C'est la boucle du salon ?",
        "enfant-m|Oui, elle montre où il est.",
    ],
    (2, 2): [
        "narrateur|Au phare des dalles, la feuille colle.",
        "narrateur|Raphaël pose le livre, comme un toit.",
        "enfant-m|À l'abri, petit bateau !",
        "narrateur|Le vent tourne les pages, trop vite.",
        "narrateur|Le toit devient une voile, et part.",
        "maman|Le livre a trop voyagé.",
        "enfant-m|Ils s'envolent tous les deux !",
        "narrateur|Raphaël court au bord, les joues froides.",
        "narrateur|Dans sa poitrine, l'envie recule.",
        "enfant-m|Je pose le livre.",
        "narrateur|Il écoute le vent, puis les dalles.",
        "narrateur|Une page a une trace d'eau, mince.",
        "narrateur|La boucle rousse reste sur une page.",
        "maman|Elle pendait au crochet, tu te souviens ?",
        "enfant-m|Oui, près du bouton-gland.",
    ],
    (2, 3): [
        "narrateur|Au phare des dalles, la feuille colle.",
        "narrateur|Raphaël pose une assiette, comme un quai.",
        "enfant-m|Accoste ici, petit bateau !",
        "narrateur|La pluie remplit l'assiette, trop vite.",
        "narrateur|L'assiette devient un couvercle, et cache.",
        "papa|Le quai a trop bu.",
        "enfant-m|Je ne peux plus la voir !",
        "narrateur|Raphaël touche le bord, trop froid.",
        "narrateur|Dans sa poitrine, la peur se serre.",
        "enfant-m|Doucement, maintenant.",
        "narrateur|Il pose l'oreille près de l'anse.",
        "narrateur|L'assiette sonne, comme un petit toc.",
        "narrateur|La boucle rousse sort, collée à l'anse.",
        "papa|Tu l'as reconnue ?",
        "enfant-m|Oui, c'est la mienne, du manteau.",
    ],
    (3, 1): [
        "narrateur|Au hangar du lit, la feuille attend.",
        "narrateur|Raphaël bâtit une tour, pour voir.",
        "enfant-m|Un phare, pour le bateau !",
        "narrateur|La tour tombe sur le manteau.",
        "narrateur|Le bouton-gland disparaît sous un cube.",
        "papa|Le bruit a poussé la feuille plus loin.",
        "enfant-m|Je n'entends plus rien !",
        "narrateur|Raphaël s'assoit, les épaules basses.",
        "narrateur|Dans sa poitrine, l'envie se tait.",
        "enfant-m|Je construis trop haut.",
        "narrateur|Il écoute le doudou, et le tic.",
        "narrateur|Un cube garde la poussière du lit.",
        "narrateur|La boucle rousse tremble sous le sommier.",
        "papa|C'est celle du tapis, tu vois ?",
        "enfant-m|Oui, elle pendait, dès le salon.",
    ],
    (3, 2): [
        "narrateur|Au hangar du lit, la feuille attend.",
        "narrateur|Raphaël glisse le livre sous le sommier.",
        "enfant-m|Ramène-le, comme un radeau !",
        "narrateur|Le livre pousse la feuille, plus loin.",
        "narrateur|Il fait le balai, sans le vouloir.",
        "maman|L'outil a trop avancé.",
        "enfant-m|Le livre l'a chassée !",
        "narrateur|Raphaël retire le livre, trop vite.",
        "narrateur|Dans sa poitrine, la peur pique.",
        "enfant-m|Le radeau a trop poussé.",
        "narrateur|Il pose le livre, et il attend.",
        "narrateur|La page a un pli du sommier.",
        "narrateur|La boucle rousse reste sur la page.",
        "maman|Tu la vois, la boucle du début ?",
        "enfant-m|Oui, elle était à la poche.",
    ],
    (3, 3): [
        "narrateur|Au hangar du lit, la feuille attend.",
        "narrateur|Raphaël tend une cuillère sous le lit.",
        "enfant-m|Accroche-toi, petit bateau !",
        "narrateur|La cuillère attrape la boucle rousse.",
        "narrateur|Il tire : la poche se retourne.",
        "papa|Tu as la boucle, pas la feuille.",
        "enfant-m|Elle vient de la poche, pas d'elle !",
        "narrateur|Raphaël lâche, les mains tremblantes.",
        "narrateur|Dans sa poitrine, l'envie se serre.",
        "enfant-m|Sans tirer, alors.",
        "narrateur|Il pose la cuillère, sans tirer.",
        "narrateur|La cuillère tient la boucle, mince.",
        "narrateur|La boucle rousse brille, trop tendue.",
        "papa|C'est la boucle du crochet ?",
        "enfant-m|Oui, je l'ai vue au salon.",
    ],
}

T3_CHOICE = {
    1: [
        "narrateur|Les cubes se taisent, le manteau attend.",
        "narrateur|Le matin, après la sieste, ou le soir.",
        "maman|Quand la boucle peut-elle parler ?",
    ],
    2: [
        "narrateur|Le livre se tait, le manteau attend.",
        "narrateur|Le matin, après la sieste, ou le soir.",
        "papa|Quand la boucle peut-elle parler ?",
    ],
    3: [
        "narrateur|La dînette se tait, le manteau attend.",
        "narrateur|Le matin, après la sieste, ou le soir.",
        "maman|Quand la boucle peut-elle parler ?",
    ],
}

RES = {
    (1, 1, 1): [
        "enfant-m|Le matin, des marches basses, pas une tour !",
        "narrateur|Raphaël pose trois cubes, loin de la vapeur.",
        "narrateur|Il suit la boucle rousse, jusqu'à la feuille.",
        "narrateur|Les deux bras rentrent, et le toc parle.",
        "narrateur|Ils sortent par derrière, vers la flaque claire.",
        "papa|La boucle a parlé, ce matin.",
        "enfant-m|Mon bateau nage, et j'ai mes deux bras !",
        "maman|Ça a failli rester collé au verre.",
        "narrateur|Un cube garde une miette, près du bouton.",
        "papa|Tu as entendu la gouttière ?",
        "enfant-m|Elle fait tic, comme le radiateur.",
        "narrateur|La boucle rousse tremble, une goutte au bout.",
        "maman|On rentre, le manteau est lourd.",
        "narrateur|Raphaël touche le gland, chaud, fermé.",
    ],
    (1, 1, 2): [
        "enfant-m|Après la sieste, les cubes font un quai !",
        "narrateur|La maison chuchote.",
        "narrateur|La casserole s'est tue.",
        "narrateur|Raphaël aligne les cubes sur la table.",
        "narrateur|Il suit la boucle, et la feuille se pose.",
        "narrateur|Les deux bras rentrent, dans le silence.",
        "narrateur|Ils vont à la flaque, pas longtemps.",
        "papa|La boucle a parlé, très bas.",
        "enfant-m|Il nage, et moi je reste chaud !",
        "maman|Ça a failli rester collé au verre.",
        "narrateur|Le cube tiède cache une goutte de soupe.",
        "papa|Tu as attendu, cette fois ?",
        "enfant-m|Oui, le temps d'un toc.",
        "narrateur|La boucle rousse sent la vapeur, un peu.",
    ],
    (1, 1, 3): [
        "enfant-m|Le soir, les cubes font un sentier !",
        "narrateur|La vitre a des perles, noires et rondes.",
        "narrateur|Raphaël pose les cubes vers la porte.",
        "narrateur|Il suit la boucle, sans presser la feuille.",
        "narrateur|Les deux bras rentrent, face aux perles.",
        "narrateur|La flaque est sombre, et le bateau part.",
        "papa|La boucle a parlé, comme une lanterne.",
        "enfant-m|Il nage dans le noir, je le vois !",
        "maman|Ça a failli rester collé au verre.",
        "narrateur|Un cube brille, perle de buée dessus.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "narrateur|La boucle rousse tient une perle, minuscule.",
        "maman|On rentre, le manteau goutte un peu.",
    ],
    (1, 2, 1): [
        "enfant-m|Le matin, le livre attend, sans souffler !",
        "narrateur|Raphaël pose le livre, ouvert, sous la vitre.",
        "narrateur|La buée tombe en gouttes, sur la page.",
        "narrateur|La boucle rousse guide la feuille, et il la prend.",
        "narrateur|Les deux bras rentrent, dans la lumière pâle.",
        "narrateur|Ils sortent vers la flaque, le livre au sec.",
        "papa|La boucle a parlé, ce matin.",
        "enfant-m|La page a fait le quai !",
        "maman|Ça a failli filer dans le nuage.",
        "narrateur|La page a un bateau d'eau, minuscule.",
        "papa|Tu as vu la boucle, sur le bord ?",
        "enfant-m|Oui, elle montre le chemin.",
        "narrateur|Le bouton-gland est chaud, contre le livre.",
        "maman|On rentre, le manteau sent le papier.",
    ],
    (1, 2, 2): [
        "enfant-m|Après la sieste, je tourne une page, seule !",
        "narrateur|La maison chuchote.",
        "narrateur|Raphaël ouvre le livre.",
        "narrateur|Une page, puis il attend la buée.",
        "narrateur|La boucle rousse apparaît, collée au coin.",
        "narrateur|Les deux bras rentrent, dans le silence.",
        "narrateur|Ils vont à la flaque, le livre fermé.",
        "papa|La boucle a parlé, très bas.",
        "enfant-m|J'ai attendu la page, cette fois !",
        "maman|Ça a failli filer dans le nuage.",
        "narrateur|La page sent la vapeur, chaude.",
        "papa|Tu as vu le bateau, sur le papier ?",
        "enfant-m|Il était dessiné par l'eau.",
        "narrateur|La boucle rousse marque la page, mince.",
    ],
    (1, 2, 3): [
        "enfant-m|Le soir, le livre est un toit, immobile !",
        "narrateur|La vitre a des perles.",
        "narrateur|Raphaël cale le livre.",
        "narrateur|Il ne souffle plus.",
        "narrateur|La buée descend.",
        "narrateur|La boucle rousse glisse sous le toit, puis sort.",
        "narrateur|Les deux bras rentrent, face aux perles.",
        "narrateur|La flaque est sombre, et le bateau part.",
        "papa|La boucle a parlé, comme une lanterne.",
        "enfant-m|Le toit a tenu, cette fois !",
        "maman|Ça a failli filer dans le nuage.",
        "narrateur|Un bateau de buée dort sur la page.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "narrateur|La boucle rousse tient une perle, sur le livre.",
    ],
    (1, 3, 1): [
        "enfant-m|Le matin, je penche la tasse, lentement !",
        "narrateur|Raphaël penche la tasse au-dessus de l'évier.",
        "narrateur|L'eau de vapeur part.",
        "narrateur|La boucle rousse apparaît, puis la feuille.",
        "narrateur|Les deux bras rentrent, dans la lumière pâle.",
        "narrateur|Ils sortent vers la flaque, la tasse vide.",
        "papa|La boucle a parlé, ce matin.",
        "enfant-m|Le puits a rendu le bateau !",
        "maman|Ça a failli rester au fond.",
        "narrateur|La petite tasse tient la boucle rousse.",
        "papa|Tu as vu le gland, sur le bord ?",
        "enfant-m|Il a fait toc, contre la tasse.",
        "narrateur|Le bouton-gland est tiède, un peu humide.",
        "maman|On rentre, le manteau sent la soupe.",
    ],
    (1, 3, 2): [
        "enfant-m|Après la sieste, la cuillère va chercher !",
        "narrateur|La maison chuchote.",
        "narrateur|Raphaël plonge la cuillère.",
        "narrateur|Il suit la boucle, sans presser la feuille.",
        "narrateur|Les deux bras rentrent, dans le silence.",
        "narrateur|Ils vont à la flaque, la tasse au sec.",
        "papa|La boucle a parlé, très bas.",
        "enfant-m|La cuillère a été un crochet, gentil !",
        "maman|Ça a failli rester au fond.",
        "narrateur|Une cuillère garde une goutte de soupe.",
        "papa|Tu as attendu, avant de plonger ?",
        "enfant-m|Oui, le temps d'un tic.",
        "narrateur|La boucle rousse sèche sur l'anse, mince.",
        "maman|On rentre, le manteau est tiède.",
    ],
    (1, 3, 3): [
        "enfant-m|Le soir, la tasse est une lanterne !",
        "narrateur|La vitre a des perles.",
        "narrateur|Raphaël lève la tasse.",
        "narrateur|Un rond de lumière tombe sur la feuille.",
        "narrateur|Il suit la boucle, sans verser.",
        "narrateur|Les deux bras rentrent, face aux perles.",
        "narrateur|La flaque est sombre, et le bateau part.",
        "papa|La boucle a parlé, comme une lanterne.",
        "enfant-m|J'ai vu le bateau, dans le rond !",
        "maman|Ça a failli rester au fond.",
        "narrateur|La tasse reflète un bateau de pluie.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "narrateur|La boucle rousse tient une perle, au bord.",
    ],
    (2, 1, 1): [
        "enfant-m|Le matin, un cube, pas tout le chemin !",
        "narrateur|Raphaël soulève un cube, près de la botte.",
        "narrateur|La boucle rousse mène à la feuille, collée.",
        "narrateur|Il la glisse dans la poche, sans courir.",
        "narrateur|Les deux bras rentrent, dans la lumière pâle.",
        "narrateur|La flaque claire reçoit le bateau, net.",
        "papa|La boucle a parlé, ce matin.",
        "enfant-m|Un cube a suffi, pas dix !",
        "maman|Ça a failli rester sous le bois.",
        "narrateur|Un cube a du sable, collé à la boucle.",
        "papa|Ta manche est rentrée, cette fois ?",
        "enfant-m|Oui, les deux, et le toc.",
        "narrateur|Le bouton-gland goutte, une perle ronde.",
        "maman|On rentre, le manteau est lourd d'eau.",
    ],
    (2, 1, 2): [
        "enfant-m|Après la sieste, les cubes font un quai sec !",
        "narrateur|La maison a chuchoté.",
        "narrateur|Dehors, la pluie tombe moins.",
        "narrateur|Raphaël pose deux cubes, loin de la manche.",
        "narrateur|Il suit la boucle, sans traîner le tissu.",
        "narrateur|Les deux bras rentrent, dans le calme.",
        "narrateur|La flaque reçoit le bateau, tout près.",
        "papa|La boucle a parlé, très bas.",
        "enfant-m|Ma manche n'a rien poussé !",
        "maman|Ça a failli rester sous le bois.",
        "narrateur|Le cube sèche, une dalle dessinée dessus.",
        "papa|Tu as vu la boucle, sur le bois ?",
        "enfant-m|Oui, elle montrait la feuille.",
        "narrateur|La boucle rousse sèche, mince, sur le cube.",
    ],
    (2, 1, 3): [
        "enfant-m|Le soir, les cubes font des lanternes !",
        "narrateur|Les dalles ont des perles, noires et rondes.",
        "narrateur|Raphaël pose trois cubes autour de la flaque.",
        "narrateur|Il suit la boucle, sans la manche dans l'eau.",
        "narrateur|Les deux bras rentrent, face aux perles.",
        "narrateur|Le bateau part, une lanterne de cube derrière.",
        "papa|La boucle a parlé, comme une lanterne.",
        "enfant-m|Les cubes gardent le port, pas moi !",
        "maman|Ça a failli rester sous le bois.",
        "narrateur|Un cube luit, perle de flaque au coin.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "narrateur|La boucle rousse tient une perle, au cube.",
        "maman|On rentre, le manteau goutte un peu.",
    ],
    (2, 2, 1): [
        "enfant-m|Le matin, le livre reste fermé, comme un quai !",
        "narrateur|Raphaël pose le livre, fermé, près de la botte.",
        "narrateur|La boucle rousse y glisse, sans les pages.",
        "narrateur|Il prend la feuille, puis la poche.",
        "narrateur|Les deux bras rentrent, dans la lumière pâle.",
        "narrateur|La flaque claire reçoit le bateau, net.",
        "papa|La boucle a parlé, ce matin.",
        "enfant-m|Pas de voile, cette fois !",
        "maman|Ça a failli filer avec le vent.",
        "narrateur|La page a une trace de dalle mouillée.",
        "papa|Tu as tenu le livre, sans l'ouvrir ?",
        "enfant-m|Oui, fermé, comme un quai.",
        "narrateur|Le bouton-gland est froid, puis chaud.",
        "maman|On rentre, le manteau sent le papier mouillé.",
    ],
    (2, 2, 2): [
        "enfant-m|Après la sieste, une page, puis j'arrête !",
        "narrateur|La pluie tombe moins.",
        "narrateur|Raphaël ouvre une page.",
        "narrateur|Il attend.",
        "narrateur|Le vent se tait.",
        "narrateur|La boucle rousse est là, collée au coin.",
        "narrateur|Les deux bras rentrent, dans le calme.",
        "narrateur|La flaque reçoit le bateau, tout près.",
        "papa|La boucle a parlé, très bas.",
        "enfant-m|Le vent n'a pas pris la page !",
        "maman|Ça a failli filer avec le vent.",
        "narrateur|La page sent l'herbe, et la boucle.",
        "papa|Tu as vu la boucle, sur le papier ?",
        "enfant-m|Oui, elle montrait le bateau.",
        "narrateur|La boucle rousse sèche sur la page, mince.",
    ],
    (2, 2, 3): [
        "enfant-m|Le soir, le livre est un toit, coincé !",
        "narrateur|Raphaël cale le livre sous une botte.",
        "narrateur|Le vent ne tourne plus les pages.",
        "narrateur|La boucle rousse glisse, et il prend la feuille.",
        "narrateur|Les deux bras rentrent, face aux perles.",
        "narrateur|La flaque sombre reçoit le bateau, net.",
        "papa|La boucle a parlé, comme une lanterne.",
        "enfant-m|La botte a tenu le toit !",
        "maman|Ça a failli filer avec le vent.",
        "narrateur|Un bateau d'eau glisse sur la page.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "narrateur|La boucle rousse tient une perle, sur le livre.",
        "maman|On rentre, le manteau goutte un peu.",
    ],
    (2, 3, 1): [
        "enfant-m|Le matin, je soulève l'assiette, sans verser !",
        "narrateur|Raphaël lève l'assiette, tout près de la botte.",
        "narrateur|La boucle rousse mène à la feuille, au fond.",
        "narrateur|Il la glisse dans la poche, sans courir.",
        "narrateur|Les deux bras rentrent, dans la lumière pâle.",
        "narrateur|La flaque claire reçoit le bateau, net.",
        "papa|La boucle a parlé, ce matin.",
        "enfant-m|Le couvercle est devenu un quai !",
        "maman|Ça a failli rester sous l'eau.",
        "narrateur|L'assiette a un rond de flaque.",
        "papa|Tu as soulevé, sans tout verser ?",
        "enfant-m|Oui, tout près, très lentement.",
        "narrateur|Le bouton-gland goutte, une perle ronde.",
        "maman|On rentre, le manteau est lourd d'eau.",
    ],
    (2, 3, 2): [
        "enfant-m|Après la sieste, la tasse va au bord !",
        "narrateur|La pluie tombe moins.",
        "narrateur|Raphaël pose la tasse.",
        "narrateur|Il y glisse la feuille, comme un nid.",
        "narrateur|Puis la poche, puis le toc.",
        "narrateur|Les deux bras rentrent, dans le calme.",
        "narrateur|La flaque reçoit le bateau, tout près.",
        "papa|La boucle a parlé, très bas.",
        "enfant-m|La tasse a été le nid, une seconde !",
        "maman|Ça a failli rester sous l'eau.",
        "narrateur|La tasse sent la terre mouillée.",
        "papa|Tu as vu la boucle, sur l'anse ?",
        "enfant-m|Oui, elle montrait le bateau.",
        "narrateur|La boucle rousse sèche sur l'anse, mince.",
    ],
    (2, 3, 3): [
        "enfant-m|Le soir, la cuillère est une lanterne !",
        "narrateur|Les dalles ont des perles.",
        "narrateur|Raphaël lève la cuillère.",
        "narrateur|Un éclat montre la feuille, sous l'assiette.",
        "narrateur|Il suit la boucle, sans verser.",
        "narrateur|Les deux bras rentrent, face aux perles.",
        "narrateur|La flaque sombre reçoit le bateau, net.",
        "papa|La boucle a parlé, comme une lanterne.",
        "enfant-m|J'ai vu le bateau, dans l'éclat !",
        "maman|Ça a failli rester sous l'eau.",
        "narrateur|Une cuillère tient une perle de pluie.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "narrateur|La boucle rousse tient une perle, à l'anse.",
    ],
    (3, 1, 1): [
        "enfant-m|Le matin, un cube-phare, pas une tour !",
        "narrateur|Raphaël pose un cube, loin du bouton.",
        "narrateur|La lumière pâle glisse sous le sommier.",
        "narrateur|Il suit la boucle, puis prend la feuille.",
        "narrateur|Les deux bras rentrent, près du lit.",
        "narrateur|Ils vont à la flaque, le doudou capitaine.",
        "papa|La boucle a parlé, ce matin.",
        "enfant-m|Un cube a suffi, pour voir !",
        "maman|Ça a failli dormir sous le lit.",
        "narrateur|Un cube garde la poussière du sommier.",
        "papa|Tu as posé, sans faire tomber ?",
        "enfant-m|Oui, un seul, tout près.",
        "narrateur|Le bouton-gland est chaud, contre le cube.",
        "maman|On rentre, le manteau sent le drap.",
    ],
    (3, 1, 2): [
        "enfant-m|Après la sieste, les cubes font un quai !",
        "narrateur|La maison chuchote.",
        "narrateur|Raphaël aligne deux cubes.",
        "narrateur|Il glisse la main, sans bruit.",
        "narrateur|La boucle rousse vient, et la feuille aussi.",
        "narrateur|Les deux bras rentrent, dans le silence.",
        "narrateur|Ils vont à la flaque, pas longtemps.",
        "papa|La boucle a parlé, très bas.",
        "enfant-m|Le doudou a vu, sans crier !",
        "maman|Ça a failli dormir sous le lit.",
        "narrateur|Le cube est chaud, comme le drap.",
        "papa|Tu as attendu, avant de prendre ?",
        "enfant-m|Oui, le temps d'un tic.",
        "narrateur|La boucle rousse sèche sur le cube, mince.",
    ],
    (3, 1, 3): [
        "enfant-m|Le soir, le cube est une lanterne !",
        "narrateur|La lampe allume le hangar du lit.",
        "narrateur|Raphaël pose un cube, et le rond glisse.",
        "narrateur|La boucle rousse apparaît, la feuille autour.",
        "narrateur|Les deux bras rentrent, face à la lampe.",
        "narrateur|Ils vont à la flaque, sombre et ronde.",
        "papa|La boucle a parlé, comme une lanterne.",
        "enfant-m|J'ai vu le bateau, dans le rond !",
        "maman|Ça a failli dormir sous le lit.",
        "narrateur|Un cube luit sous la lampe, boucle autour.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "narrateur|La boucle rousse tient une perle, au cube.",
        "maman|On rentre, le manteau goutte un peu.",
    ],
    (3, 2, 1): [
        "enfant-m|Le matin, le livre attend, sans pousser !",
        "narrateur|Raphaël pose le livre, ouvert, sous le lit.",
        "narrateur|Il n'avance plus.",
        "narrateur|La boucle rousse monte seule, puis la feuille.",
        "narrateur|Les deux bras rentrent, dans la lumière pâle.",
        "narrateur|Ils vont à la flaque, le livre au sec.",
        "papa|La boucle a parlé, ce matin.",
        "enfant-m|Le radeau a attendu, cette fois !",
        "maman|Ça a failli filer au fond.",
        "narrateur|La page a un pli du sommier.",
        "papa|Tu as vu la boucle, sur le papier ?",
        "enfant-m|Oui, elle montrait le bateau.",
        "narrateur|Le bouton-gland est chaud, contre le livre.",
        "maman|On rentre, le manteau sent le papier.",
    ],
    (3, 2, 2): [
        "enfant-m|Après la sieste, une page, puis j'arrête !",
        "narrateur|La maison chuchote.",
        "narrateur|Raphaël glisse une page.",
        "narrateur|Il attend.",
        "narrateur|La boucle rousse se pose dessus.",
        "narrateur|Les deux bras rentrent, dans le silence.",
        "narrateur|Ils vont à la flaque, pas longtemps.",
        "papa|La boucle a parlé, très bas.",
        "enfant-m|Le livre n'a pas chassé, cette fois !",
        "maman|Ça a failli filer au fond.",
        "narrateur|La page sent le doudou, un peu rêche.",
        "papa|Tu as attendu, avant de tirer ?",
        "enfant-m|Oui, le temps d'un tic.",
        "narrateur|La boucle rousse sèche sur la page, mince.",
        "narrateur|Le doudou a l'oreille dehors, capitaine.",
    ],
    (3, 2, 3): [
        "enfant-m|Le soir, le livre est un toit dessous !",
        "narrateur|La lampe allume le hangar.",
        "narrateur|Raphaël cale le livre.",
        "narrateur|La boucle rousse glisse au sec, sur la page.",
        "narrateur|Il prend la feuille, sans pousser.",
        "narrateur|Les deux bras rentrent, face à la lampe.",
        "narrateur|Ils vont à la flaque, sombre et ronde.",
        "papa|La boucle a parlé, comme une lanterne.",
        "enfant-m|Le toit a tenu, dessous !",
        "maman|Ça a failli filer au fond.",
        "narrateur|Un bateau au crayon dort sur la page.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "narrateur|La boucle rousse tient une perle, sur le livre.",
    ],
    (3, 3, 1): [
        "enfant-m|Le matin, je suis la boucle, sans tirer !",
        "narrateur|Raphaël suit la boucle rousse, sous le lit.",
        "narrateur|La boucle mène à la feuille, tout près.",
        "narrateur|Il prend les deux, sans retourner la poche.",
        "narrateur|Les deux bras rentrent, dans la lumière pâle.",
        "narrateur|Ils vont à la flaque, la cuillère au sec.",
        "papa|La boucle a parlé, ce matin.",
        "enfant-m|La boucle a montré le chemin !",
        "maman|Ça a failli retourner la poche.",
        "narrateur|La cuillère a attrapé la boucle rousse.",
        "papa|Tu as suivi, sans tirer fort ?",
        "enfant-m|Oui, comme un chemin, pas une corde.",
        "narrateur|Le bouton-gland est chaud, contre la cuillère.",
        "maman|On rentre, le manteau sent le drap.",
    ],
    (3, 3, 2): [
        "enfant-m|Après la sieste, la tasse est un nid !",
        "narrateur|La maison chuchote.",
        "narrateur|Raphaël pose la tasse.",
        "narrateur|Il y glisse la feuille, puis la boucle.",
        "narrateur|Les deux bras rentrent, dans le silence.",
        "narrateur|Ils vont à la flaque, pas longtemps.",
        "papa|La boucle a parlé, très bas.",
        "enfant-m|La poche n'a pas bougé, cette fois !",
        "maman|Ça a failli retourner la poche.",
        "narrateur|La tasse tient un poil du doudou.",
        "papa|Tu as posé, sans tirer la boucle ?",
        "enfant-m|Oui, le nid d'abord.",
        "narrateur|La boucle rousse sèche sur l'anse, mince.",
        "narrateur|Le doudou a l'oreille dehors, capitaine.",
    ],
    (3, 3, 3): [
        "enfant-m|Le soir, l'assiette reflète le bateau !",
        "narrateur|La lampe allume le hangar.",
        "narrateur|Raphaël lève l'assiette.",
        "narrateur|Un rond montre la feuille, et la boucle.",
        "narrateur|Il les prend, sans retourner la poche.",
        "narrateur|Les deux bras rentrent, face à la lampe.",
        "narrateur|Ils vont à la flaque, sombre et ronde.",
        "papa|La boucle a parlé, comme une lanterne.",
        "enfant-m|J'ai vu le bateau, dans le rond !",
        "maman|Ça a failli retourner la poche.",
        "narrateur|La petite assiette reflète la vitre noire.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "narrateur|La boucle rousse tient une perle, à l'anse.",
        "maman|On rentre, le manteau goutte un peu.",
    ],
}

FINS = {
    (1, 1, 1): [
        "narrateur|Au salon, Raphaël raccroche le manteau.",
        "narrateur|Le bouton-gland fait toc, contre le radiateur.",
        "papa|Quel cube tu gardes, près du crochet ?",
        "enfant-m|Celui qui a la miette.",
        "maman|Le fournil a laissé sa trace.",
        "enfant-m|Mon bateau a nagé, ce matin.",
        "narrateur|Un cube garde une miette, près de la boucle rousse.",
    ],
    (1, 1, 2): [
        "narrateur|Raphaël pose le manteau au crochet bas.",
        "narrateur|Le radiateur reprend son tic, près du tissu.",
        "maman|Le cube est tiède, tu le sens ?",
        "enfant-m|Oui, comme la soupe.",
        "papa|Le silence de la sieste est resté.",
        "enfant-m|Mon bateau a nagé, après le repos.",
        "narrateur|Le cube tiède cache une goutte de soupe.",
    ],
    (1, 1, 3): [
        "narrateur|Le soir, le manteau goutte au crochet.",
        "narrateur|Une perle glisse du bouton-gland, ronde.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "maman|Le fournil a gardé sa chaleur.",
        "enfant-m|Mon bateau a nagé dans le noir.",
        "narrateur|Un cube brille, perle de buée dessus.",
    ],
    (1, 2, 1): [
        "narrateur|Raphaël raccroche le manteau, le livre au sec.",
        "narrateur|Le bouton-gland fait toc, contre le radiateur.",
        "papa|Quelle page tu gardes, près du crochet ?",
        "enfant-m|Celle du bateau d'eau.",
        "maman|Le fournil a laissé son nuage.",
        "enfant-m|Mon bateau a nagé, ce matin.",
        "narrateur|La page a un bateau d'eau, minuscule.",
    ],
    (1, 2, 2): [
        "narrateur|Après la sieste, le manteau retrouve le crochet.",
        "narrateur|Le radiateur tic, le livre sent la vapeur.",
        "maman|La page est chaude, tu la sens ?",
        "enfant-m|Oui, comme le fournil.",
        "papa|Tu as attendu la page, cette fois.",
        "enfant-m|Mon bateau a nagé, sans courir.",
        "narrateur|La page sent la vapeur, chaude.",
    ],
    (1, 2, 3): [
        "narrateur|Le soir, le livre reste ouvert au salon.",
        "narrateur|Une perle de pluie dort sur la page.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "maman|Le toit du livre a tenu.",
        "enfant-m|Mon bateau a nagé sous les perles.",
        "narrateur|Un bateau de buée dort sur la page.",
    ],
    (1, 3, 1): [
        "narrateur|Raphaël raccroche le manteau, la tasse près du sel.",
        "narrateur|Le bouton-gland fait toc, contre le radiateur.",
        "papa|Quelle tasse tu gardes, près du crochet ?",
        "enfant-m|Celle qui a la boucle.",
        "maman|Le fournil a versé, puis rendu.",
        "enfant-m|Mon bateau a nagé, ce matin.",
        "narrateur|La petite tasse tient la boucle rousse.",
    ],
    (1, 3, 2): [
        "narrateur|Après la sieste, la cuillère tinte au salon.",
        "narrateur|Raphaël pose le manteau, le gland chaud.",
        "maman|La cuillère a une goutte, tu la vois ?",
        "enfant-m|Oui, une goutte de soupe.",
        "papa|Le silence a aidé le toc.",
        "enfant-m|Mon bateau a nagé, sans plonger trop vite.",
        "narrateur|Une cuillère garde une goutte de soupe.",
    ],
    (1, 3, 3): [
        "narrateur|Le soir, la tasse reflète la vitre noire.",
        "narrateur|Le manteau goutte, une perle au bouton.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "maman|La lanterne de tasse a montré le chemin.",
        "enfant-m|Mon bateau a nagé dans le rond.",
        "narrateur|La tasse reflète un bateau de pluie.",
    ],
    (2, 1, 1): [
        "narrateur|Au salon, Raphaël raccroche le manteau mouillé.",
        "narrateur|Le bouton-gland goutte, puis fait toc.",
        "papa|Quel cube tu gardes, près des bottes ?",
        "enfant-m|Celui qui a le sable.",
        "maman|Le phare des dalles a rendu la feuille.",
        "enfant-m|Mon bateau a nagé, ce matin.",
        "narrateur|Un cube a du sable, collé à la boucle.",
    ],
    (2, 1, 2): [
        "narrateur|Après la sieste, le manteau sèche au crochet.",
        "narrateur|Un cube pose une dalle minuscule, dessus.",
        "maman|Le cube sèche, tu le sens ?",
        "enfant-m|Oui, comme la dalle.",
        "papa|Ta manche n'a rien poussé, cette fois.",
        "enfant-m|Mon bateau a nagé, sans la manche.",
        "narrateur|Le cube sèche, une dalle dessinée dessus.",
    ],
    (2, 1, 3): [
        "narrateur|Le soir, trois cubes gardent le souvenir du port.",
        "narrateur|Le manteau goutte, une perle au gland.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "maman|Les lanternes de cubes ont veillé.",
        "enfant-m|Mon bateau a nagé entre les lanternes.",
        "narrateur|Un cube luit, perle de flaque au coin.",
    ],
    (2, 2, 1): [
        "narrateur|Raphaël raccroche le manteau, le livre fermé.",
        "narrateur|Le bouton-gland fait toc, un peu froid.",
        "papa|Quelle page tu gardes, près des bottes ?",
        "enfant-m|Celle de la dalle mouillée.",
        "maman|Le quai fermé a tenu.",
        "enfant-m|Mon bateau a nagé, sans voile.",
        "narrateur|La page a une trace de dalle mouillée.",
    ],
    (2, 2, 2): [
        "narrateur|Après la sieste, le livre sent l'herbe.",
        "narrateur|Raphaël pose le manteau, le gland tiède.",
        "maman|La page sent l'herbe, tu la sens ?",
        "enfant-m|Oui, et la boucle aussi.",
        "papa|Le vent n'a pas pris la page.",
        "enfant-m|Mon bateau a nagé, une page à la fois.",
        "narrateur|La page sent l'herbe, et la boucle.",
    ],
    (2, 2, 3): [
        "narrateur|Le soir, le livre reste calé sous une botte.",
        "narrateur|Une perle glisse sur la page, ronde.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "maman|La botte a tenu le toit.",
        "enfant-m|Mon bateau a nagé sous le toit.",
        "narrateur|Un bateau d'eau glisse sur la page.",
    ],
    (2, 3, 1): [
        "narrateur|Raphaël raccroche le manteau, l'assiette au sec.",
        "narrateur|Le bouton-gland goutte, puis fait toc.",
        "papa|Quelle assiette tu gardes, près des bottes ?",
        "enfant-m|Celle du rond de flaque.",
        "maman|Le couvercle est devenu un quai.",
        "enfant-m|Mon bateau a nagé, ce matin.",
        "narrateur|L'assiette a un rond de flaque.",
    ],
    (2, 3, 2): [
        "narrateur|Après la sieste, la tasse sent la terre.",
        "narrateur|Raphaël pose le manteau, le gland tiède.",
        "maman|La tasse sent la terre, tu la sens ?",
        "enfant-m|Oui, comme le jardin.",
        "papa|Le nid d'une seconde a suffi.",
        "enfant-m|Mon bateau a nagé, depuis la tasse.",
        "narrateur|La tasse sent la terre mouillée.",
    ],
    (2, 3, 3): [
        "narrateur|Le soir, la cuillère tient une perle.",
        "narrateur|Le manteau goutte, face à la vitre noire.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "maman|L'éclat de cuillère a montré le bateau.",
        "enfant-m|Mon bateau a nagé dans l'éclat.",
        "narrateur|Une cuillère tient une perle de pluie.",
    ],
    (3, 1, 1): [
        "narrateur|Au hangar du lit, puis au crochet.",
        "narrateur|Raphaël raccroche le manteau, un cube à côté.",
        "papa|Quel cube tu gardes, près du doudou ?",
        "enfant-m|Celui de la poussière du sommier.",
        "maman|Un phare a suffi, pas une tour.",
        "enfant-m|Mon bateau a nagé, ce matin.",
        "narrateur|Un cube garde la poussière du sommier.",
    ],
    (3, 1, 2): [
        "narrateur|Après la sieste, le cube est chaud.",
        "narrateur|Raphaël pose le manteau, le gland tiède.",
        "maman|Le cube est chaud, comme le drap ?",
        "enfant-m|Oui, comme le lit.",
        "papa|Le doudou a vu, sans crier.",
        "enfant-m|Mon bateau a nagé, sans bruit.",
        "narrateur|Le cube est chaud, comme le drap.",
    ],
    (3, 1, 3): [
        "narrateur|Le soir, le cube luit sous la lampe.",
        "narrateur|Le manteau goutte, la boucle autour du bois.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "maman|Le rond de lampe a montré le bateau.",
        "enfant-m|Mon bateau a nagé dans le rond.",
        "narrateur|Un cube luit sous la lampe, boucle autour.",
    ],
    (3, 2, 1): [
        "narrateur|Raphaël raccroche le manteau, le livre au sec.",
        "narrateur|Le bouton-gland fait toc, contre le radiateur.",
        "papa|Quelle page tu gardes, près du doudou ?",
        "enfant-m|Celle du pli du sommier.",
        "maman|Le radeau a attendu, cette fois.",
        "enfant-m|Mon bateau a nagé, ce matin.",
        "narrateur|La page a un pli du sommier.",
    ],
    (3, 2, 2): [
        "narrateur|Après la sieste, la page sent le doudou.",
        "narrateur|Raphaël pose le manteau, l'oreille dehors.",
        "maman|La page sent le doudou, tu la sens ?",
        "enfant-m|Oui, un peu rêche.",
        "papa|Le livre n'a pas chassé, cette fois.",
        "enfant-m|Mon bateau a nagé, une page à la fois.",
        "narrateur|La page sent le doudou, un peu rêche.",
    ],
    (3, 2, 3): [
        "narrateur|Le soir, un bateau au crayon dort.",
        "narrateur|Le manteau goutte, le livre ouvert au salon.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "maman|Le toit sous le lit a tenu.",
        "enfant-m|Mon bateau a nagé sous le toit.",
        "narrateur|Un bateau au crayon dort sur la page.",
    ],
    (3, 3, 1): [
        "narrateur|Raphaël raccroche le manteau, la cuillère au sec.",
        "narrateur|Le bouton-gland fait toc, contre le radiateur.",
        "papa|Quelle cuillère tu gardes, près du doudou ?",
        "enfant-m|Celle qui a suivi la boucle.",
        "maman|La boucle a montré le chemin.",
        "enfant-m|Mon bateau a nagé, ce matin.",
        "narrateur|La cuillère a attrapé la boucle rousse.",
    ],
    (3, 3, 2): [
        "narrateur|Après la sieste, la tasse tient un poil.",
        "narrateur|Raphaël pose le manteau, le doudou capitaine.",
        "maman|La tasse a un poil, tu le vois ?",
        "enfant-m|Oui, un poil du doudou.",
        "papa|Le nid d'abord, pas la corde.",
        "enfant-m|Mon bateau a nagé, depuis le nid.",
        "narrateur|La tasse tient un poil du doudou.",
    ],
    (3, 3, 3): [
        "narrateur|Le soir, l'assiette reflète la vitre noire.",
        "narrateur|Le manteau goutte, une perle au bouton.",
        "papa|Tu as vu les bateaux sur la vitre ?",
        "enfant-m|Ils étaient là, dès le départ.",
        "maman|Le rond d'assiette a montré le bateau.",
        "enfant-m|Mon bateau a nagé dans le rond.",
        "narrateur|La petite assiette reflète la vitre noire.",
    ],
}


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    chunks: list[dict] = []

    def add(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        chunks.append(voice(by_src[cid], lines, profile, sons, extra))

    add("CHK_T0000_P0000", OPENING, "opening", "pluie,radiateur")
    add("CHK_T0001_P0000", T1_CHOICE, "choice", "", {"pause_before_ms": 200})

    t2_sons = {1: "bois,cubes", 2: "pages,livre", 3: "vaisselle,dinette"}
    t3_sons = {1: "radiateur,matin", 2: "silence,sieste", 3: "pluie,soir"}

    for a in (1, 2, 3):
        t1 = T1[a]
        add(f"CHK_T0001_P000{a}", t1["passage"], "action", t1["sons"], {"emphasis": t1["emp"]})
        add(
            f"CHK_T0001_P000{a}_Q0001",
            t1["question"],
            "clue",
            "",
            {
                "pause_before_ms": 200,
                "expected_answer": "manteau",
                "accepted_examples": "manteau | le manteau | son manteau | le manteau de laine",
                "retry_prompt": t1["retry"],
            },
        )
        add(f"CHK_T0001_P000{a}_C0001", t1["confirm"], "confirm", t1["sons"])
        add(f"CHK_T0001_P000{a}_T0002_P0000", T2_CHOICE[a], "choice", "", {"pause_before_ms": 200})
        for b in (1, 2, 3):
            add(
                f"CHK_T0001_P000{a}_T0002_P000{b}",
                T2[(a, b)],
                "obstacle",
                t2_sons[b],
                {"emphasis": "boucle rousse"},
            )
            add(
                f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
                T3_CHOICE[b],
                "choice",
                "",
                {"pause_before_ms": 200},
            )
            for c in (1, 2, 3):
                add(
                    f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}",
                    RES[(a, b, c)],
                    "resolution",
                    t3_sons[c],
                    {"emphasis": "manteau"},
                )
                add(
                    f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}_F0001",
                    FINS[(a, b, c)],
                    "ending",
                    "radiateur,crochet",
                    {"note": ending_note(a, b, c), "emphasis": "manteau"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in {x["chunk_id"] for x in chunks}]
    extra = {x["chunk_id"] for x in chunks} - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"chunks missing={missing[:8]} extra={sorted(extra)[:8]}")
    order = {c["chunk_id"]: i for i, c in enumerate(src["chunks"])}
    chunks.sort(key=lambda c: order[c["chunk_id"]])

    fins = [ch["text"] for ch in chunks if ch["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(fins))}/27")
    last_n = []
    for ch in chunks:
        if ch.get("kind") != "passage_fin":
            continue
        last = [x for x in ch["script"].splitlines() if x.startswith("narrateur|")][-1]
        last_n.append(last.split("|", 1)[1])
        last_low = last.split("|", 1)[1].lower()
        if "histoire" in last_low or "bravo" in last_low or "bon travail" in last_low:
            raise SystemExit(f"{ch['chunk_id']} fin mécanique: {last_low}")
    if len(set(last_n)) != 27:
        raise SystemExit(f"dernières images: {len(set(last_n))}/27")
    res_txt = [
        ch["text"]
        for ch in chunks
        if ch["kind"] == "passage"
        and "_T0003_P000" in ch["chunk_id"]
        and "_F0001" not in ch["chunk_id"]
        and not ch["chunk_id"].endswith("_T0003_P0000")
    ]
    if len(res_txt) != 27 or len(set(res_txt)) != 27:
        raise SystemExit(f"résolutions distinctes: {len(set(res_txt))}/{len(res_txt)}")

    blob = "\n".join(c["script"] for c in chunks).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "raphaël" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent")
    if "manteau" not in blob:
        raise SystemExit(f"{SID}: manteau absent")
    if "boucle rousse" not in blob:
        raise SystemExit(f"{SID}: boucle rousse absente")
    for tic in ("tout doux", "tout calme", " aujourd'hui,"):
        if tic in blob:
            raise SystemExit(f"{SID}: tic {tic}")
    if TICS.search(blob):
        raise SystemExit(f"{SID}: tic corpus {TICS.search(blob).group(0)}")
    for bad in (
        "merle",
        "couleur de miel",
        "tom ",
        "léa",
        "sami",
        "grand-père",
        "maîtresse",
        "jardinier",
        "mission accomplie",
        "j'ai compris",
        "marque fine",
        "ombre en forme",
        "minuscule symbole",
    ):
        if bad in blob:
            raise SystemExit(f"{SID}: interdit {bad}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in chunks)
    if not tts_ok:
        raise SystemExit(f"{SID}: TTS incomplet")

    out = dict(src)
    out["fil_rouge"] = (
        "Sous la pluie, Raphaël veut porter son bateau-feuille jusqu'à la flaque, "
        "dans la poche du manteau de laine beige, avant que les bateaux de la vitre "
        "s'effacent. Une boucle rousse pend de la poche dès le départ. Première "
        "tentative : un seul bras, manche à l'envers, feuille au tapis, sourire parti. "
        "Cuisine, jardin ou chambre changent l'obstacle. Cubes, livre ou dînette "
        "changent la ruse : Raphaël refuse de foncer, écoute, retrouve la boucle. "
        "Matin, sieste ou soir changent le geste. Le toc revient. La boucle garde une goutte."
    )
    out["title"] = TITLE
    out["characters"] = "Raphaël, papa, maman"
    out["setting"] = "salon sous la pluie, puis cuisine, jardin ou chambre"
    out["chunks"] = chunks
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
        mp = {ch["chunk_id"]: ch for ch in chunks}
        return sum(words(mp[i]["text"]) for i in ids)

    lengths = [path_words(a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    if min(lengths) < 550:
        raise SystemExit(f"chemin trop court: {min(lengths)}")
    if max(lengths) > 720:
        raise SystemExit(f"chemin trop long: {max(lengths)}")

    t1s = [next(ch["text"] for ch in chunks if ch["chunk_id"] == f"CHK_T0001_P000{i}") for i in (1, 2, 3)]
    if len(set(t1s)) < 3:
        raise SystemExit("T1 ne change pas l'histoire")
    t2s = [
        next(ch["text"] for ch in chunks if ch["chunk_id"] == f"CHK_T0001_P0001_T0002_P000{j}")
        for j in (1, 2, 3)
    ]
    if len(set(t2s)) < 3:
        raise SystemExit("T2 ne change pas l'histoire")
    t3s = [
        next(
            ch["text"]
            for ch in chunks
            if ch["chunk_id"] == f"CHK_T0001_P0001_T0002_P0001_T0003_P000{k}"
        )
        for k in (1, 2, 3)
    ]
    if len(set(t3s)) < 3:
        raise SystemExit("T3 ne change pas l'histoire")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        "# TREE-AUT-016 — Le manteau de laine de Raphaël\n\n"
        "- **Nouveau titre :** *Le manteau de laine de Raphaël*\n"
        "- **Public :** 3–4 ans (N1), lecture interactive familiale\n"
        "- **Leçon principale :** AUT.AFF.002 — prendre son manteau (vécue, non dite)\n"
        "- **Personnages :** Raphaël, papa, maman\n"
        "- **Structure conservée :** 86 nœuds, trois choix à trois options, "
        "27 chemins et 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Les pieds de Raphaël tapent le tapis : il veut la flaque tout de suite. "
        "Une boucle rousse pend de la poche du manteau de laine beige. Il enfile "
        "un seul bras : manche à l'envers, toc muet, feuille au tapis. Le sourire "
        "part. Papa s'accroupit. Cuisine (fournil), jardin (phare des dalles) ou "
        "chambre (hangar du lit) changent l'obstacle ; cubes, livre ou dînette "
        "changent la ruse ; matin, sieste ou soir changent le geste. Raphaël refuse "
        "de foncer, écoute, retrouve la boucle du départ. Ça a failli ne pas arriver. "
        "Au crochet, la boucle garde une goutte.\n\n"
        "## Améliorations appliquées\n\n"
        "- Ouverture par le corps (pieds, impatience), pas le gabarit v2.\n"
        "- Indice unique dès le début : boucle rousse, payée au climax.\n"
        "- Corps : sourire qui part, poitrine, adulte à la même hauteur.\n"
        "- Première idée échoue. Second imprévu plus rusé ; l'enfant observe.\n"
        "- T1 ne retire pas le manteau. T1/T2/T3 changent l'action.\n"
        "- 27 fins textuellement distinctes, dernière image unique.\n"
        "- Un merci vécu (deux bras), pas un refrain. Question d'adulte.\n"
        "- Pas de « encore / déjà / tout doux », pas merle, pas miel, pas apply.\n\n"
        "## Direction vocale\n\n"
        "TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending) : "
        "rate, pitch, volume, pauses, text_ssml, text_xai_tags, notes d'arc. "
        "slow réservé aux choix, indices et retours.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, {min(lengths)} à {max(lengths)} mots, moyenne {sum(lengths)//len(lengths)}\n"
        "- 27 fins et 27 dernières images distinctes\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés\n"
        "- N1 ≤ 10 mots/phrase. `check()` OK.\n\n"
        "## Relu\n\n"
        "P0000, 3 L1, 9 L2, 27 résolutions, 27 fins. Questions liées à la scène "
        "(épaules / manteau). Impatience, découragement, fierté calme.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(
        f"OK {SID} {nwords} mots  fins={len(set(fins))}  "
        f"chemins {min(lengths)}-{max(lengths)} moy {sum(lengths)//len(lengths)}  "
        f"1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}"
    )


if __name__ == "__main__":
    main()
