#!/usr/bin/env python3
"""TREE-AUT-010 — Le manteau jaune de Chouchou (F-NAR-019, N3, AUT.AFF.002, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-010"
N3 = LIMITS["N3"]
TITLE = "Le manteau jaune de Chouchou"
TICS = re.compile(
    r"\b(tout doux|tout calme|encore|déjà|deja|une étape après l'autre)\b",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="manteau",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_bateau_feuille_attend_les_flaques; tempo=naturel; sourire=léger; respiration=ample",
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
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qui_s_est_passé; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="manteau",
        note="arc=confirmation; intention=relancer; emotion=élan; intensite=1; destinataire=enfant; sous_texte=les_deux_bras_puis_le_clic; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=elle_veut_lancer_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=le_bouton_reste_muet; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="manteau",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=le_clic_rend_la_poche; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="manteau",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_bouton_cloche_garde_une_goutte; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > N3:
            raise SystemExit(f"{n}>{N3}: {ph}")
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
        out.append(f"{role}|{ph}")
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
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if "note" in extra:
        m["note"] = extra["note"]
    text, script = from_script(lines)
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
    out = deepcopy(src)
    out["text"] = text
    out["script"] = script
    out["sons"] = sons if sons is not None else (src.get("sons") or "")
    if out["sons"] is None:
        out["sons"] = ""
    out["text_ssml"] = ssml(text, m)
    out["text_xai_tags"] = xai(text, m)
    out["rate_wpm"] = m["wpm"]
    out["rate_label"] = m["rate"]
    out["speed_xai"] = m["speed"]
    out["length_scale_piper"] = m["piper"]
    out["pitch_label"] = m["pitch"]
    out["pitch_ssml"] = m["pitchSsml"]
    out["pitch_xai_tag"] = m["pitchTag"]
    out["volume_label"] = m["volume"]
    out["volume_db"] = m["db"]
    out["emphasis_words"] = m.get("emphasis") or ""
    out["pause_before_ms"] = extra.get("pause_before_ms", 0)
    out["pause_after_ms"] = m["pause"]
    out["pause_sentence_ms"] = m["sentence"]
    out["style_energy"] = m["energy"]
    out["style_contour"] = m["contour"]
    out["noise_scale_piper"] = m["noise"]
    out["kokoro_speed"] = m["speed"]
    out["melo_speed"] = m["speed"]
    out["espeak_amp"] = 82 if m["volume"] == "soft" else 100
    out["espeak_pitch"] = 42 if m["pitch"] == "low" else 50
    out["espeak_word_gap"] = 12 if m["rate"] == "slow" else 8
    out["notes"] = m["note"]
    out["night_policy"] = "play"
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.items():
        if k in ("emphasis", "note", "pause_before_ms"):
            continue
        out[k] = v
    return out


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=le_manteau_garde_la_goutte_du_seuil; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


OPENING = vet(
    [
        "narrateur|Sur le chemin de l'école, la gouttière fait tic.",
        "narrateur|Une feuille mouillée colle au seuil, plate et brillante.",
        "narrateur|Ça sent la terre, et le bois du portail.",
        "narrateur|Chouchou vit là, avec papa et maman.",
        "narrateur|Sur le crochet, le manteau jaune attend, un peu lourd.",
        "narrateur|Son bouton-cloche, rond et doré, pèse contre le tissu.",
        "papa|Tu as entendu le tic, Chouchou ?",
        "enfant-f|La gouttière joue, je veux le parc !",
        "maman|Ton bateau-feuille peut dormir dans la poche.",
        "narrateur|Elle a plié la feuille, hier, contre le capuchon.",
        "narrateur|Le bouton-cloche a fait clic, net, sous son ongle.",
        "narrateur|En ce moment, Chouchou saute vers le crochet.",
        "enfant-f|Je le prends, et je cours aux flaques !",
        "narrateur|Elle enfile un bras, trop vite, de travers.",
        "narrateur|La fermeture se bloque, et le bouton reste muet.",
        "narrateur|La feuille glisse, molle, vers le seuil.",
        "enfant-f|Il ne veut pas rentrer !",
        "papa|L'autre bras d'abord, puis le clic.",
        "maman|La feuille attend, quand tes deux manches sont là.",
        "narrateur|Chouchou souffle, les épaules basses.",
        "enfant-f|Je veux mon bateau, au port des dalles.",
        "papa|Merci d'avoir dit ce que tu veux.",
        "narrateur|Elle glisse le second bras, plus lent.",
        "narrateur|Le clic parle, et la feuille rentre, au chaud.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|Le manteau tient chaud, la feuille dans la poche.",
        "narrateur|Le bac à sable, le toboggan, ou les balançoires.",
        "maman|Où vas-tu d'abord, Chouchou ?",
    ]
)

T1 = {
    1: dict(
        lab="le bac à sable",
        ans="poche",
        acc="poche | la poche | poche du manteau | le sable",
        retry="Le sable a rempli quelque chose. Qu'est-ce que le sable a rempli ?",
        ok="Oui, c'est la poche.",
        sons="sable,flaque",
        emp="poche",
        passage=vet(
            [
                "narrateur|Chouchou court vers le bac à sable, le manteau trop ouvert.",
                "narrateur|Le sable froid brille, plein de petites flaques.",
                "enfant-f|Mon bateau va nager ici, tout de suite !",
                "narrateur|Elle jette le jaune sur le rebord, trop pressée.",
                "narrateur|La poche s'écrase, et le sable mouillé y rentre.",
                "narrateur|Le bouton-cloche se tait, coincé sous un tas.",
                "enfant-f|Ma feuille, elle est partie !",
                "papa|Le sable a mangé la poche.",
                "maman|Tes deux bras n'étaient plus dedans.",
                "narrateur|Chouchou cherche, les épaules basses, les mains froides.",
                "enfant-f|Je le veux, mon bateau !",
                "narrateur|Un grain dore le bouton, comme la feuille du seuil.",
            ]
        ),
        question=vet(
            [
                "narrateur|Le sable mouillé a tout envahi.",
                "maman|Qu'est-ce que le sable a rempli ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Un grain de sable colle au bouton-cloche.",
                "enfant-f|Je remets les deux bras, après.",
                "maman|Bravo, tu as vu la poche.",
                "papa|On vide le sable, puis le clic.",
                "enfant-f|Oui, papa.",
                "narrateur|La poche redevient un nid, un peu rêche.",
            ]
        ),
    ),
    2: dict(
        lab="le toboggan",
        ans="bouton",
        acc="bouton | le bouton | bouton-cloche | le clic | capuchon",
        retry="Le clic n'a pas parlé. Qu'est-ce qui est resté muet ?",
        ok="Oui, c'est le bouton.",
        sons="toboggan,metal",
        emp="bouton",
        passage=vet(
            [
                "narrateur|Chouchou grimpe au toboggan, le manteau battant.",
                "narrateur|La rampe luit, froide, après la pluie.",
                "enfant-f|Je glisse avec mon bateau !",
                "narrateur|Elle part trop vite, le capuchon en arrière.",
                "narrateur|Le bouton-cloche s'ouvre, sans un son.",
                "narrateur|La feuille s'envole, et tombe au pied de la rampe.",
                "enfant-f|Il est parti, tout seul !",
                "papa|Le clic n'a pas parlé.",
                "maman|Un bras a quitté la manche, en haut.",
                "narrateur|Chouchou s'arrête en bas, les joues chaudes.",
                "enfant-f|Je le rattrape !",
                "narrateur|Une trace jaune, mince, court sur le fer.",
            ]
        ),
        question=vet(
            [
                "narrateur|En haut, un petit son a manqué.",
                "papa|Qu'est-ce qui est resté muet ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|La rampe garde une trace jaune, mince.",
                "enfant-f|Je boutonne, avant de glisser.",
                "papa|Le clic d'abord, puis la rampe.",
                "maman|Tes deux manches, contre toi.",
                "enfant-f|Oui, maman.",
                "narrateur|Le bouton-cloche brille, un peu mouillé.",
            ]
        ),
    ),
    3: dict(
        lab="les balançoires",
        ans="chaîne",
        acc="chaîne | la chaîne | sur la chaîne | balançoire | le fer",
        retry="Le manteau n'était plus sur elle. Où l'a-t-elle posé ?",
        ok="Oui, sur la chaîne.",
        sons="balançoire,chaine",
        emp="chaîne",
        passage=vet(
            [
                "narrateur|Chouchou court aux balançoires, le manteau trop lourd.",
                "narrateur|Les chaînes gouttent, et une flaque attend dessous.",
                "enfant-f|Je pose le manteau, et je vole !",
                "narrateur|Elle accroche le jaune à une chaîne, trop haut.",
                "narrateur|Le vent balance le capuchon, le bouton se défait.",
                "narrateur|La feuille glisse dans la flaque, sous le siège.",
                "enfant-f|Il nage sans moi !",
                "papa|Le manteau n'est plus sur toi.",
                "maman|La chaîne n'a pas de poche fermée.",
                "narrateur|Chouchou se penche, les épaules basses.",
                "enfant-f|Je le veux, près de moi !",
                "narrateur|Une goutte court le long du fer, comme au seuil.",
            ]
        ),
        question=vet(
            [
                "narrateur|Le jaune pendait, trop loin des épaules.",
                "maman|Où a-t-elle posé le manteau ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Une goutte court le long de la chaîne.",
                "enfant-f|Je le remets, le manteau.",
                "maman|Sur tes épaules, pas sur le fer.",
                "papa|Le clic, et la feuille revient.",
                "enfant-f|Oui, je l'entends.",
                "narrateur|Le capuchon retrouve sa place, un peu froid.",
            ]
        ),
    ),
}

T2_CHOICE = {
    1: vet(
        [
            "narrateur|Le sable tient dans la poche, trop lourd.",
            "narrateur|Le ballon, le seau, ou le doudou.",
            "papa|Tu prends quoi, pour vider la poche ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Le bouton est resté muet, en haut de la rampe.",
            "narrateur|Le ballon, le seau, ou le doudou.",
            "maman|Tu prends quoi, pour rattraper le bateau ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Le manteau pend à la chaîne, trop loin.",
            "narrateur|Le ballon, le seau, ou le doudou.",
            "papa|Tu prends quoi, pour l'aider à rentrer ?",
        ]
    ),
}


def t2_scene(a: int, b: int) -> list[str]:
    hip = {
        1: "Au bac, la poche a bu le sable mouillé.",
        2: "Au toboggan, le bouton-cloche est resté muet.",
        3: "Aux balançoires, le manteau pend, trop loin.",
    }[a]
    bodies = {
        (1, 1): [
            f"narrateur|{hip}",
            "narrateur|Chouchou pousse le ballon contre le rebord.",
            "enfant-f|Je secoue, et ça sort !",
            "narrateur|Le ballon tape la poche, trop fort.",
            "narrateur|Le sable saute, et la feuille s'enfonce.",
            "papa|Le bouton est terne, comme après le seuil.",
            "maman|Le ballon n'ouvre pas les manches.",
            "enfant-f|Elle est cachée, plus loin !",
            "narrateur|Chouchou s'arrête, les mains farineuses de sable.",
            "narrateur|Une poussière ronde reste sur le jaune.",
            "papa|On cherche le clic, pas la course.",
            "enfant-f|Il me faut un endroit, pour boutonner.",
        ],
        (1, 2): [
            f"narrateur|{hip}",
            "narrateur|Chouchou penche le seau au-dessus de la poche.",
            "enfant-f|L'eau va laver le sable !",
            "narrateur|Un filet froid rentre, et la feuille disparaît.",
            "narrateur|La poche devient une flaque, trop lourde.",
            "maman|La poche est un nid, pas une mare.",
            "papa|Le seau a trop donné.",
            "enfant-f|Je ne la vois plus !",
            "narrateur|Chouchou lève le tissu, les épaules basses.",
            "narrateur|Une anse froide a laissé un rond, sur le jaune.",
            "maman|On vide, puis on ferme.",
            "enfant-f|Il me faut un endroit, pour boutonner.",
        ],
        (1, 3): [
            f"narrateur|{hip}",
            "narrateur|Chouchou frotte la poche avec le doudou.",
            "enfant-f|Il va attraper la feuille !",
            "narrateur|Les poils prennent le sable, et le bateau aussi.",
            "narrateur|Le doudou devient un nuage gris, trop plein.",
            "papa|Regarde, un éclat jaune, dans le poil.",
            "maman|Comme la feuille du seuil, ce matin.",
            "enfant-f|Il l'a mangée, le doudou !",
            "narrateur|Chouchou écarte les poils, trop vite, trop fort.",
            "narrateur|Un fil brille, puis se cache.",
            "papa|On pose le doudou, et on remet le jaune.",
            "enfant-f|Il me faut un endroit, pour boutonner.",
        ],
        (2, 1): [
            f"narrateur|{hip}",
            "narrateur|Chouchou lâche le ballon, en haut de la rampe.",
            "enfant-f|Va chercher mon bateau !",
            "narrateur|Le ballon dévale, et pousse la feuille plus loin.",
            "narrateur|Deux ronds glissent, et se perdent au pied.",
            "papa|La trace jaune, c'est la feuille, pas le ballon.",
            "maman|Comme la goutte du capuchon, au départ.",
            "enfant-f|Ils filent trop vite !",
            "narrateur|Chouchou descend, les joues chaudes, sans clic.",
            "narrateur|Le fer garde une poussière ronde, et un pli.",
            "papa|On rattrape, puis on boutonne.",
            "enfant-f|Il me faut un endroit, pour le clic.",
        ],
        (2, 2): [
            f"narrateur|{hip}",
            "narrateur|Chouchou pose le seau, tout au bas de la rampe.",
            "enfant-f|Tombe dedans, petit bateau !",
            "narrateur|La feuille file à côté, et l'eau éclabousse.",
            "narrateur|Le seau sonne, vide, trop tard.",
            "maman|Elle s'est collée sous le fer, vois-tu ?",
            "papa|Le clic manquait, alors elle a volé.",
            "enfant-f|Le seau a fait du bruit pour rien !",
            "narrateur|Chouchou se penche, une goutte au nez.",
            "narrateur|Sous la rampe, un éclat jaune attend.",
            "maman|On prend le seau, et on va fermer.",
            "enfant-f|Il me faut un endroit, pour le clic.",
        ],
        (2, 3): [
            f"narrateur|{hip}",
            "narrateur|Chouchou envoie le doudou, sur la rampe froide.",
            "enfant-f|Attrape-la, toi !",
            "narrateur|Le doudou glisse, et s'étale sur la feuille.",
            "narrateur|L'eau du fer mouille l'oreille, trop vite.",
            "papa|Il a couvert le bateau, sans le voir.",
            "maman|L'oreille brille, comme la feuille du seuil.",
            "enfant-f|Il est trop mouillé, je n'ose plus !",
            "narrateur|Chouchou ramasse le doudou, lourd, froid.",
            "narrateur|Un pli jaune dépasse, collé au ventre.",
            "papa|On serre le doudou, et on remet le manteau.",
            "enfant-f|Il me faut un endroit, pour le clic.",
        ],
        (3, 1): [
            f"narrateur|{hip}",
            "narrateur|Chouchou lance le ballon vers la chaîne.",
            "enfant-f|Fais tomber le manteau, gentiment !",
            "narrateur|Le ballon tape le fer, et le jaune s'envole.",
            "narrateur|La flaque avale la feuille, plus loin.",
            "papa|Le ballon a trop poussé.",
            "maman|Le capuchon a perdu son clic, en l'air.",
            "enfant-f|Il nage trop loin !",
            "narrateur|Chouchou court au bord, les pieds mouillés.",
            "narrateur|Une poussière du ballon flotte, sur l'eau.",
            "papa|On reprend le jaune, sur tes épaules.",
            "enfant-f|Il me faut un endroit, pour le clic.",
        ],
        (3, 2): [
            f"narrateur|{hip}",
            "narrateur|Chouchou plonge le seau dans la flaque.",
            "enfant-f|Je la pêche, ma feuille !",
            "narrateur|L'eau monte, et la feuille colle au fond.",
            "narrateur|Le seau est lourd, et elle ne voit rien.",
            "maman|Elle s'est cachée contre le métal.",
            "papa|Comme sous le capuchon, au matin.",
            "enfant-f|Le seau a tout bu !",
            "narrateur|Chouchou penche, trop vite, une vague part.",
            "narrateur|Un éclat jaune reste, collé à l'anse.",
            "maman|On porte le seau, et on remet le manteau.",
            "enfant-f|Il me faut un endroit, pour le clic.",
        ],
        (3, 3): [
            f"narrateur|{hip}",
            "narrateur|Chouchou tend le doudou, vers la flaque.",
            "enfant-f|Bois l'eau, et garde la feuille !",
            "narrateur|Le doudou s'imbibe, et la feuille rentre dans un pli.",
            "narrateur|L'oreille devient lourde, trop froide.",
            "papa|Il a bu la flaque, et le bateau.",
            "maman|Un fil brille, comme au seuil.",
            "enfant-f|Il est trop lourd, je le lâche !",
            "narrateur|Chouchou serre le doudou, les bras tremblants.",
            "narrateur|Un pli jaune s'ouvre, puis se referme.",
            "papa|On presse le doudou, et on boutonne.",
            "enfant-f|Il me faut un endroit, pour le clic.",
        ],
    }
    return vet(bodies[(a, b)])


T3_CHOICE = {
    1: vet(
        [
            "narrateur|Le ballon s'est tu, et le manteau attend.",
            "narrateur|Le kiosque, la grille, ou le banc.",
            "maman|Où vas-tu fermer le bouton-cloche ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Le seau est lourd, et le manteau attend.",
            "narrateur|Le kiosque, la grille, ou le banc.",
            "papa|Où vas-tu fermer le bouton-cloche ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Le doudou est mouillé, et le manteau attend.",
            "narrateur|Le kiosque, la grille, ou le banc.",
            "maman|Où vas-tu fermer le bouton-cloche ?",
        ]
    ),
}

RES = {
    (1, 1, 1): vet(
        [
            "enfant-f|Le kiosque, il a des crochets !",
            "narrateur|Chouchou prend le manteau, sable et ballon autour.",
            "narrateur|Elle enfile un bras, puis l'autre, sans courir.",
            "narrateur|Le bouton-cloche fait clic, net, sous le kiosque.",
            "narrateur|Un grain de sable tombe, et la feuille apparaît.",
            "narrateur|Elle pose le bateau sur la flaque des dalles.",
            "papa|Tu as entendu le clic, cette fois.",
            "enfant-f|Il nage, et moi j'ai mes deux bras !",
            "maman|Le kiosque a prêté son crochet.",
            "narrateur|Une goutte dore le bouton, près du kiosque.",
        ]
    ),
    (1, 1, 2): vet(
        [
            "enfant-f|La grille des gouttes, je la connais !",
            "narrateur|Le ballon roule jusqu'aux barreaux, tout seul.",
            "narrateur|Chouchou enfile le jaune, dos à la grille.",
            "narrateur|Le clic parle, et un grain tombe entre les fers.",
            "narrateur|La feuille glisse vers la flaque, de l'autre côté.",
            "papa|Tes deux manches tiennent, contre les barreaux.",
            "enfant-f|Mon bateau passe, je reste au sec !",
            "maman|La grille a montré le chemin.",
            "narrateur|Une ligne d'eau court sur la manche, mince.",
        ]
    ),
    (1, 1, 3): vet(
        [
            "enfant-f|Le banc des capuchons, je m'assois !",
            "narrateur|Chouchou pose le ballon, pour tenir le manteau.",
            "narrateur|Elle s'assoit, un bras, puis l'autre, sans sauter.",
            "narrateur|Le clic parle, et le sable quitte la poche.",
            "narrateur|La feuille part du banc, vers le port des dalles.",
            "papa|Le bois t'a aidée, pour le bouton.",
            "enfant-f|J'ai mes deux bras, et lui nage !",
            "maman|Le banc aime les capuchons fermés.",
            "narrateur|Le capuchon garde la marque du bois, plate.",
        ]
    ),
    (1, 2, 1): vet(
        [
            "enfant-f|Le kiosque, on vide le seau là-bas !",
            "narrateur|Chouchou verse le sable mouillé, près de la gouttière du kiosque.",
            "narrateur|Elle secoue la poche, puis enfile les deux manches.",
            "narrateur|Le clic parle, et la feuille se déplie, moins lourde.",
            "narrateur|Elle la pose sur la flaque, au pied du kiosque.",
            "papa|Le nid est vide, et fermé.",
            "enfant-f|Le seau a travaillé, et moi aussi !",
            "maman|Le kiosque a bu l'eau sale.",
            "narrateur|L'anse a laissé un rond humide, dans le tissu.",
        ]
    ),
    (1, 2, 2): vet(
        [
            "enfant-f|La grille, le seau va parler aux barreaux !",
            "narrateur|Chouchou penche le seau, et la feuille colle au bord.",
            "narrateur|Elle prend le jaune, dos à la grille des gouttes.",
            "narrateur|Deux bras, un clic, et la feuille rejoint la flaque.",
            "papa|Tu l'as vue, collée au métal.",
            "enfant-f|Elle était là, tout contre l'anse !",
            "maman|La grille a gardé l'eau, pas tes épaules.",
            "narrateur|Une goutte de seau tremble au bouton, face au chemin.",
        ]
    ),
    (1, 2, 3): vet(
        [
            "enfant-f|Le banc, le seau sera mon marchepied !",
            "narrateur|Chouchou pose le seau, et s'assoit sur le banc.",
            "narrateur|Elle vide la poche, grain par grain, sans courir.",
            "narrateur|Deux bras, un clic, et la feuille glisse vers l'eau.",
            "papa|Le bois a tenu tes pieds, et le seau aussi.",
            "enfant-f|Je n'ai pas versé sur moi !",
            "maman|Le banc aime qu'on s'arrête.",
            "narrateur|Le bois du banc sent le seau, sous le manteau jaune.",
        ]
    ),
    (1, 3, 1): vet(
        [
            "enfant-f|Le kiosque, le doudou va s'y secouer !",
            "narrateur|Chouchou secoue le doudou, sous le crochet du kiosque.",
            "narrateur|Un éclat jaune tombe, et elle enfile le manteau.",
            "narrateur|Le clic parle, et la feuille rejoint la flaque.",
            "papa|Le poil a rendu ce qu'il avait pris.",
            "enfant-f|Il l'avait gardée, pour moi !",
            "maman|Le kiosque a vu le doudou travailler.",
            "narrateur|Un poil accroche le bouton-cloche, minuscule.",
        ]
    ),
    (1, 3, 2): vet(
        [
            "enfant-f|La grille, le doudou va s'y essuyer !",
            "narrateur|Chouchou presse le doudou contre les barreaux.",
            "narrateur|Un fil jaune brille, et elle reprend le manteau.",
            "narrateur|Deux bras, un clic, et la feuille passe la grille.",
            "papa|Comme au seuil, cet éclat-là.",
            "enfant-f|Je l'ai vu, dans le poil !",
            "maman|La grille a séché le doudou, un peu.",
            "narrateur|Le doudou a séché la grille, et le pli de la feuille.",
        ]
    ),
    (1, 3, 3): vet(
        [
            "enfant-f|Le banc, le doudou sera le nid !",
            "narrateur|Chouchou pose le doudou, et s'assoit tout contre.",
            "narrateur|Elle ouvre le poil, trouve la feuille, puis le jaune.",
            "narrateur|Deux bras, un clic, et le bateau part du banc.",
            "papa|Le nid du doudou a rendu le tien.",
            "enfant-f|Il m'a prêté sa poche, à lui !",
            "maman|Le banc a tenu vous deux.",
            "narrateur|L'oreille du doudou dépasse de la poche, au chaud.",
        ]
    ),
    (2, 1, 1): vet(
        [
            "enfant-f|Le kiosque, le ballon l'y emmène !",
            "narrateur|Chouchou suit le ballon, jusqu'aux crochets du kiosque.",
            "narrateur|Elle ramasse la feuille, puis enfile le manteau.",
            "narrateur|Le clic parle, et le bateau rejoint la flaque du kiosque.",
            "papa|La rampe a fini au kiosque, cette fois.",
            "enfant-f|Je l'ai rattrapé, sans glisser !",
            "maman|Le crochet a attendu tes épaules.",
            "narrateur|Le ballon a laissé une poussière ronde, sur le jaune.",
        ]
    ),
    (2, 1, 2): vet(
        [
            "enfant-f|La grille, le ballon s'y coince !",
            "narrateur|Le ballon s'arrête aux barreaux, la feuille contre lui.",
            "narrateur|Chouchou prend le jaune, dos à la grille des gouttes.",
            "narrateur|Deux bras, un clic, et le bateau passe entre les fers.",
            "papa|Le ballon a fait le mur, toi le clic.",
            "enfant-f|Il n'a plus filé, cette fois !",
            "maman|La grille a tenu le rond.",
            "narrateur|Une trace de rampe, mince, court vers le bouton.",
        ]
    ),
    (2, 1, 3): vet(
        [
            "enfant-f|Le banc, le ballon se cache dessous !",
            "narrateur|Chouchou s'agenouille, et trouve la feuille sous le banc.",
            "narrateur|Elle s'assoit, enfile les deux manches, sans se presser.",
            "narrateur|Le clic parle, et le bateau part vers les dalles.",
            "papa|Le bois t'a montrée l'ombre.",
            "enfant-f|Il était là, tout petit !",
            "maman|Le banc aime qu'on s'assoie pour boutonner.",
            "narrateur|Le capuchon garde le froid du banc, et un pli.",
        ]
    ),
    (2, 2, 1): vet(
        [
            "enfant-f|Le kiosque, le seau porte le bateau !",
            "narrateur|Chouchou glisse la feuille dans le seau, sans la serrer.",
            "narrateur|Au kiosque, elle enfile le manteau, puis le clic.",
            "narrateur|Elle pose le bateau sur la flaque, l'anse à côté.",
            "papa|Le seau a fait le voyage, toi le bouton.",
            "enfant-f|Il n'a pas volé, cette fois !",
            "maman|Le kiosque a reçu le seau, et toi.",
            "narrateur|Le seau a sonné, et le clic a répondu, tout près.",
        ]
    ),
    (2, 2, 2): vet(
        [
            "enfant-f|La grille, le seau va s'y caler !",
            "narrateur|Chouchou cale le seau entre les barreaux, la feuille au fond.",
            "narrateur|Elle remet le jaune, et le clic parle contre le fer.",
            "narrateur|Le bateau glisse vers la flaque, de l'autre côté.",
            "papa|Tu as coincé l'eau, pas tes manches.",
            "enfant-f|La grille tient le seau, moi le clic !",
            "maman|Les gouttes de la grille n'ont pas touché tes épaules.",
            "narrateur|Une goutte de rampe sèche sur le bouton-cloche.",
        ]
    ),
    (2, 2, 3): vet(
        [
            "enfant-f|Le banc, le seau s'assoit avec moi !",
            "narrateur|Chouchou pose le seau, et s'assoit, la feuille au bord.",
            "narrateur|Elle enfile les deux bras, le bois sous les cuisses.",
            "narrateur|Le clic parle, et le bateau part, sans éclabousser.",
            "papa|Le seau a attendu, toi tu as fermé.",
            "enfant-f|Je n'ai pas glissé, sur le bois !",
            "maman|Le banc a tenu l'anse, et tes pieds.",
            "narrateur|Le manteau sent le fer du toboggan, près du seau.",
        ]
    ),
    (2, 3, 1): vet(
        [
            "enfant-f|Le kiosque, le doudou va s'y presser !",
            "narrateur|Chouchou presse le doudou, sous le toit du kiosque.",
            "narrateur|La feuille se déplie, et elle enfile le manteau.",
            "narrateur|Le clic parle, et le bateau rejoint la flaque.",
            "papa|L'eau du doudou est restée au kiosque.",
            "enfant-f|Il a voyagé, tout mouillé, pour moi !",
            "maman|Le crochet a attendu tes épaules sèches.",
            "narrateur|Le doudou a une manche mouillée, et le bateau au sec.",
        ]
    ),
    (2, 3, 2): vet(
        [
            "enfant-f|La grille, le doudou s'y accroche !",
            "narrateur|Chouchou étale le doudou sur les barreaux, à sécher.",
            "narrateur|Un fil jaune brille, et elle reprend le manteau.",
            "narrateur|Deux bras, un clic, et la feuille passe la grille.",
            "papa|Le doudou sèche, toi tu fermes.",
            "enfant-f|Le fil brillait, comme au seuil !",
            "maman|La grille a prêté le vent.",
            "narrateur|Un fil du doudou brille, collé au bouton.",
        ]
    ),
    (2, 3, 3): vet(
        [
            "enfant-f|Le banc, le doudou s'y couche !",
            "narrateur|Chouchou pose le doudou, et s'assoit, la feuille au creux.",
            "narrateur|Elle enfile le jaune, sans presser l'oreille mouillée.",
            "narrateur|Le clic parle, et le bateau part du bois.",
            "papa|Le doudou a tenu le pli, toi le bouton.",
            "enfant-f|Il s'est reposé, et moi aussi !",
            "maman|Le banc a séché l'oreille, un peu.",
            "narrateur|Le doudou s'endort contre le bouton, au chaud.",
        ]
    ),
    (3, 1, 1): vet(
        [
            "enfant-f|Le kiosque, le ballon ramène le jaune !",
            "narrateur|Le manteau atterrit près du kiosque, poussé par le ballon.",
            "narrateur|Chouchou l'enfile, deux bras, le clic net.",
            "narrateur|Elle pêche la feuille, et la pose sur les dalles.",
            "papa|Le ballon a rendu le manteau, toi le clic.",
            "enfant-f|Il n'est plus à la chaîne !",
            "maman|Le crochet du kiosque aime mieux tes épaules.",
            "narrateur|Une chaîne a laissé un cling, dans le tissu jaune.",
        ]
    ),
    (3, 1, 2): vet(
        [
            "enfant-f|La grille, le ballon y pousse le manteau !",
            "narrateur|Le jaune s'accroche aux barreaux, le ballon contre.",
            "narrateur|Chouchou le reprend, deux bras, dos à la grille.",
            "narrateur|Le clic parle, et la feuille quitte la flaque, vers elle.",
            "papa|La grille a tenu le jaune, le temps du clic.",
            "enfant-f|Je l'ai, et lui aussi !",
            "maman|Les gouttes de la grille n'ont pas pris tes manches.",
            "narrateur|Le ballon a séché, collé à la poche, un instant.",
        ]
    ),
    (3, 1, 3): vet(
        [
            "enfant-f|Le banc, le ballon garde le manteau !",
            "narrateur|Chouchou pose le jaune, le ballon dessus, et s'assoit.",
            "narrateur|Elle enfile les deux manches, le bois sous elle.",
            "narrateur|Le clic parle, et la feuille revient de la flaque.",
            "papa|Le ballon a pesé, toi tu as fermé.",
            "enfant-f|Il n'a pas volé, le manteau !",
            "maman|Le banc des capuchons a fait son travail.",
            "narrateur|Le capuchon sent le vent des balançoires, plat.",
        ]
    ),
    (3, 2, 1): vet(
        [
            "enfant-f|Le kiosque, le seau porte la flaque !",
            "narrateur|Chouchou marche, le seau lourd, jusqu'au kiosque.",
            "narrateur|Elle enfile le manteau, clic, puis penche l'anse.",
            "narrateur|La feuille glisse sur les dalles, au pied du kiosque.",
            "papa|Tu as porté l'eau, et tes deux bras.",
            "enfant-f|Le seau était lourd, le clic était léger !",
            "maman|Le kiosque a reçu la flaque, pas tes épaules.",
            "narrateur|L'eau du seau a fait un rond, sous le bateau-feuille.",
        ]
    ),
    (3, 2, 2): vet(
        [
            "enfant-f|La grille, je verse, et je ferme !",
            "narrateur|Chouchou verse près des barreaux, et la feuille apparaît.",
            "narrateur|Elle remet le jaune, le clic contre la grille des gouttes.",
            "narrateur|Le bateau part, de l'autre côté du fer.",
            "papa|Tu as versé, puis tu as fermé.",
            "enfant-f|Je n'ai pas versé sur moi !",
            "maman|La grille a bu, et toi tu es sèche.",
            "narrateur|La grille goutte, loin, et le clic dort, fermé.",
        ]
    ),
    (3, 2, 3): vet(
        [
            "enfant-f|Le banc, le seau s'y pose, et moi aussi !",
            "narrateur|Chouchou s'assoit, vide le seau, grain d'eau par grain.",
            "narrateur|Elle enfile le manteau, le clic net, le bois sous elle.",
            "narrateur|La feuille part du banc, vers le port des dalles.",
            "papa|L'anse était froide, tes manches sont chaudes.",
            "enfant-f|J'ai vidé, puis j'ai fermé !",
            "maman|Le banc a tenu le seau, et toi.",
            "narrateur|Une anse froide a touché le banc, puis le tissu.",
        ]
    ),
    (3, 3, 1): vet(
        [
            "enfant-f|Le kiosque, le doudou s'y presse !",
            "narrateur|Chouchou presse le doudou, sous le toit du kiosque.",
            "narrateur|La feuille sort du pli, et elle enfile le manteau.",
            "narrateur|Le clic parle, et le bateau rejoint les dalles.",
            "papa|Le doudou a pêché, toi tu as fermé.",
            "enfant-f|Il était lourd, et maintenant il est léger !",
            "maman|Le kiosque a vu le pli s'ouvrir.",
            "narrateur|Le doudou sent la flaque, et le manteau sent le bois.",
        ]
    ),
    (3, 3, 2): vet(
        [
            "enfant-f|La grille, le doudou s'y essore !",
            "narrateur|Chouchou presse le doudou entre les barreaux.",
            "narrateur|Un poil mouillé sèche, et la feuille se déplie.",
            "narrateur|Elle remet le jaune, clic, face à la grille des gouttes.",
            "papa|Le vent de la grille a aidé.",
            "enfant-f|Le poil brillait, je l'ai vue !",
            "maman|Tes épaules sont sèches, le doudou moins.",
            "narrateur|Un poil mouillé sèche sur le bouton, face au chemin.",
        ]
    ),
    (3, 3, 3): vet(
        [
            "enfant-f|Le banc, le doudou s'y pelotonne !",
            "narrateur|Chouchou s'assoit, le doudou au creux, la feuille au bord.",
            "narrateur|Elle enfile le manteau, deux bras, le clic net.",
            "narrateur|Le bateau part du bois, vers le port des dalles.",
            "papa|Le doudou a gardé le pli, toi le bouton.",
            "enfant-f|On s'est assis, et ça a marché !",
            "maman|Le banc des capuchons a fini la chasse.",
            "narrateur|L'oreille grise et le capuchon se touchent, au chaud.",
        ]
    ),
}


def ending(a: int, b: int, c: int) -> list[str]:
    first = {
        1: "Plus tard, une graine de sable crisse sous la porte.",
        2: "Plus tard, la rampe du parc se tait, loin.",
        3: "Plus tard, une chaîne goutte, très loin du seuil.",
    }[a]
    invite = {
        1: "Tu as entendu le clic, au kiosque ?",
        2: "La grille a-t-elle rendu le bateau ?",
        3: "Le banc t'a aidée, pour le bouton ?",
    }[c]
    recap = {
        (1, 1, 1): "J'ai mis les deux bras, le clic, et un grain est tombé.",
        (1, 1, 2): "J'ai boutonné à la grille, le ballon contre les barreaux.",
        (1, 1, 3): "Je me suis assise, le ballon, et le clic a parlé.",
        (1, 2, 1): "J'ai vidé le seau au kiosque, puis j'ai fermé.",
        (1, 2, 2): "La feuille collait à l'anse, près de la grille.",
        (1, 2, 3): "Le seau était mon marchepied, sur le banc.",
        (1, 3, 1): "Le doudou a rendu la feuille, sous le crochet.",
        (1, 3, 2): "J'ai vu le fil jaune, contre la grille.",
        (1, 3, 3): "Le doudou était le nid, et moi le clic.",
        (2, 1, 1): "Le ballon a filé au kiosque, et j'ai rattrapé.",
        (2, 1, 2): "Le ballon s'est coincé, et j'ai fermé.",
        (2, 1, 3): "La feuille était sous le banc, toute petite.",
        (2, 2, 1): "Le seau a porté le bateau, moi le bouton.",
        (2, 2, 2): "J'ai calé le seau, et le clic a parlé.",
        (2, 2, 3): "Je me suis assise, sans éclabousser.",
        (2, 3, 1): "J'ai pressé le doudou, sous le toit.",
        (2, 3, 2): "Le fil brillait, comme au seuil.",
        (2, 3, 3): "Le doudou s'est reposé, et moi aussi.",
        (3, 1, 1): "Le ballon a rendu le manteau, au kiosque.",
        (3, 1, 2): "La grille a tenu le jaune, le temps du clic.",
        (3, 1, 3): "Le ballon a pesé, et je n'ai pas volé.",
        (3, 2, 1): "J'ai porté le seau, et mes deux bras.",
        (3, 2, 2): "J'ai versé, puis j'ai fermé, à la grille.",
        (3, 2, 3): "J'ai vidé, puis j'ai fermé, sur le banc.",
        (3, 3, 1): "Le doudou a pêché, et j'ai boutonné.",
        (3, 3, 2): "Le poil brillait, j'ai vu la feuille.",
        (3, 3, 3): "On s'est assis, et le clic a parlé.",
    }[(a, b, c)]
    mid = {
        1: "Le manteau jaune retrouve le crochet, un peu lourd.",
        2: "Le bouton-cloche pèse contre le tissu, comme au départ.",
        3: "La gouttière du chemin fait tic, tout près du portail.",
    }[c]
    papa_line = {
        (1, 1, 1): "Le grain a voyagé, toi aussi.",
        (1, 1, 2): "La grille a montré le passage.",
        (1, 1, 3): "Le bois a tenu tes deux bras.",
        (1, 2, 1): "Le nid est vide, et fermé.",
        (1, 2, 2): "Tu l'as vue, collée au métal.",
        (1, 2, 3): "Tes pieds n'ont pas glissé.",
        (1, 3, 1): "Le poil a rendu le bateau.",
        (1, 3, 2): "Cet éclat-là, c'était elle.",
        (1, 3, 3): "Deux nids, et un seul clic.",
        (2, 1, 1): "Tu as rattrapé, sans glisser.",
        (2, 1, 2): "Le ballon a fait le mur.",
        (2, 1, 3): "L'ombre du banc t'a aidée.",
        (2, 2, 1): "Le seau a fait le voyage.",
        (2, 2, 2): "Tu as coincé l'eau, pas tes manches.",
        (2, 2, 3): "Le bois a tenu l'anse.",
        (2, 3, 1): "L'eau est restée au kiosque.",
        (2, 3, 2): "Le vent a prêté sa main.",
        (2, 3, 3): "Le doudou a tenu le pli.",
        (3, 1, 1): "Tes épaules valent mieux que la chaîne.",
        (3, 1, 2): "La grille a attendu le clic.",
        (3, 1, 3): "Le ballon a pesé, juste assez.",
        (3, 2, 1): "Tu as porté l'eau, et le bouton.",
        (3, 2, 2): "Verser, puis fermer, ça tient.",
        (3, 2, 3): "L'anse était froide, pas toi.",
        (3, 3, 1): "Le pli s'est ouvert, au kiosque.",
        (3, 3, 2): "Le poil a parlé, toi tu as vu.",
        (3, 3, 3): "Le banc a fini la chasse.",
    }[(a, b, c)]
    last = {
        (1, 1, 1): "Un grain de sable dore le bouton-cloche, sur le crochet.",
        (1, 1, 2): "Une barre de grille a laissé une ligne sur la manche.",
        (1, 1, 3): "Le banc a marqué le capuchon, plat, près de la feuille.",
        (1, 2, 1): "L'anse du seau a laissé un rond humide, dans la poche.",
        (1, 2, 2): "Une goutte de seau tremble au bouton, face au chemin.",
        (1, 2, 3): "Le bois du banc sent le seau, sous le manteau jaune.",
        (1, 3, 1): "Un poil de doudou accroche le bouton-cloche, minuscule.",
        (1, 3, 2): "Le doudou a séché la grille, et le pli de la feuille.",
        (1, 3, 3): "L'oreille du doudou dépasse de la poche, au crochet.",
        (2, 1, 1): "Le ballon a laissé une poussière ronde, sur le jaune.",
        (2, 1, 2): "Une trace de rampe, mince, court vers le bouton.",
        (2, 1, 3): "Le capuchon garde le froid du banc, et un pli de feuille.",
        (2, 2, 1): "Le seau a sonné, et le clic a répondu, au crochet.",
        (2, 2, 2): "Une goutte de rampe sèche sur le bouton-cloche.",
        (2, 2, 3): "Le manteau sent le fer du toboggan, près du seau.",
        (2, 3, 1): "Le doudou a une manche mouillée, et le bateau au sec.",
        (2, 3, 2): "Un fil du doudou brille, collé au bouton, comme au seuil.",
        (2, 3, 3): "Le doudou s'endort contre le bouton, au crochet.",
        (3, 1, 1): "Une chaîne a laissé un cling, dans le tissu jaune.",
        (3, 1, 2): "Le ballon a séché, collé à la poche, sous le crochet.",
        (3, 1, 3): "Le capuchon sent le vent des balançoires, plat.",
        (3, 2, 1): "L'eau du seau a fait un rond, sous le bateau-feuille.",
        (3, 2, 2): "La grille goutte, loin, et le clic dort, fermé.",
        (3, 2, 3): "Une anse froide a touché le banc, puis le crochet.",
        (3, 3, 1): "Le doudou sent la flaque, et le manteau sent la maison.",
        (3, 3, 2): "Un poil mouillé sèche sur le bouton, face au chemin.",
        (3, 3, 3): "L'oreille grise et le capuchon se touchent, au crochet.",
    }[(a, b, c)]
    keepsake = {
        1: "Dans la poche, le bateau-feuille sèche, un peu rêche.",
        2: "Sur le capuchon, une goutte tremble, comme au départ.",
        3: "Près du portail, la terre sent le parc, et la pluie.",
    }[a]
    return vet(
        [
            f"narrateur|{first}",
            f"maman|{invite}",
            f"enfant-f|{recap}",
            f"narrateur|{keepsake}",
            f"narrateur|{mid}",
            f"papa|{papa_line}",
            f"narrateur|{last}",
        ]
    )


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple[list[str], str, str, dict]] = {}

    scripts["CHK_T0000_P0000"] = (OPENING, "opening", "gouttiere,manteau", {"emphasis": "manteau"})
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "le bac à sable",
            "option_2_label": "le toboggan",
            "option_3_label": "les balançoires",
        },
    )

    t2_labs = ("le ballon", "le seau", "le doudou")
    t3_labs = ("le kiosque", "la grille", "le banc")
    t2_sons = {1: "ballon", 2: "seau", 3: "doudou"}
    t2_emp = {1: "ballon", 2: "seau", 3: "doudou"}
    t3_sons = {1: "kiosque", 2: "grille", 3: "banc"}
    fin_sons = {1: "crochet,gouttiere", 2: "porte,manteau", 3: "flaque,capuchon"}

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        t1 = T1[a]
        scripts[base] = (t1["passage"], "action", t1["sons"], {"emphasis": t1["emp"]})
        scripts[f"{base}_Q0001"] = (
            t1["question"],
            "clue",
            "",
            {
                "expected_answer": t1["ans"],
                "accepted_examples": t1["acc"],
                "retry_prompt": t1["retry"],
                "engine_ok_text": t1["ok"],
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
                "emphasis": t1["ans"],
            },
        )
        scripts[f"{base}_C0001"] = (t1["confirm"], "confirm", t1["sons"], {"emphasis": "manteau"})
        scripts[f"{base}_T0002_P0000"] = (
            T2_CHOICE[a],
            "choice",
            "",
            {
                "option_1_label": t2_labs[0],
                "option_2_label": t2_labs[1],
                "option_3_label": t2_labs[2],
            },
        )
        for b in (1, 2, 3):
            leaf2 = f"{base}_T0002_P000{b}"
            scripts[leaf2] = (
                t2_scene(a, b),
                "obstacle",
                t2_sons[b],
                {"emphasis": t2_emp[b]},
            )
            scripts[f"{leaf2}_T0003_P0000"] = (
                T3_CHOICE[b],
                "choice",
                "",
                {
                    "option_1_label": t3_labs[0],
                    "option_2_label": t3_labs[1],
                    "option_3_label": t3_labs[2],
                },
            )
            for c in (1, 2, 3):
                leaf3 = f"{leaf2}_T0003_P000{c}"
                scripts[leaf3] = (
                    RES[(a, b, c)],
                    "resolution",
                    t3_sons[c],
                    {"emphasis": "manteau"},
                )
                scripts[f"{leaf3}_F0001"] = (
                    ending(a, b, c),
                    "ending",
                    fin_sons[c],
                    {"emphasis": "manteau", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra)[:8]}")

    chunks = []
    for c in src["chunks"]:
        cid = c["chunk_id"]
        lines, profile, sons, extra = scripts[cid]
        chunks.append(voice(by_src[cid], lines, profile, sons, extra))

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
    if "chouchou" not in blob:
        raise SystemExit(f"{SID}: Chouchou absente")
    if "manteau" not in blob:
        raise SystemExit(f"{SID}: manteau absent")
    for tic in ("tout doux", "tout calme", " aujourd'hui,"):
        if tic in blob:
            raise SystemExit(f"{SID}: tic {tic}")
    if TICS.search(blob):
        raise SystemExit(f"{SID}: tic corpus {TICS.search(blob).group(0)}")
    for bad in ("merle", "couleur de miel", "tom ", "léa", "sami"):
        if bad in blob:
            raise SystemExit(f"{SID}: interdit {bad}")

    out = dict(src)
    out["fil_rouge"] = (
        "Après la pluie, Chouchou veut porter son bateau-feuille jusqu'au port "
        "des dalles, dans la poche du manteau jaune, avant que le soleil boive "
        "les flaques. Le bouton-cloche du capuchon doit faire clic. Première "
        "tentative : un seul bras, fermeture de travers, la feuille tombe. Au "
        "parc, bac, toboggan ou balançoires changent l'obstacle. Ballon, seau "
        "ou doudou changent la ruse. Kiosque, grille des gouttes ou banc des "
        "capuchons changent le geste qui referme le clic. Le manteau garde une "
        "goutte et une trace de l'aventure."
    )
    out["title"] = TITLE
    out["characters"] = "Chouchou, papa, maman"
    out["setting"] = "chemin de l'école, parc après la pluie"
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
    if min(lengths) < 380:
        raise SystemExit(f"chemin trop court: {min(lengths)}")

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
        "# TREE-AUT-010 — Le manteau jaune de Chouchou\n\n"
        "- **Nouveau titre :** *Le manteau jaune de Chouchou*\n"
        "- **Public :** 5–6 ans (N3), lecture interactive familiale\n"
        "- **Leçon principale :** AUT.AFF.002 — prendre son manteau (vécue, non dite)\n"
        "- **Personnages :** Chouchou, papa, maman\n"
        "- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Après la pluie, Chouchou veut porter son bateau-feuille jusqu'au port "
        "des dalles, dans la poche du manteau jaune, avant que le soleil boive "
        "les flaques. Le bouton-cloche du capuchon doit faire clic. Elle enfile "
        "un seul bras : la fermeture se bloque, la feuille tombe. Bac, toboggan "
        "ou balançoires changent l'obstacle ; ballon, seau ou doudou changent la "
        "ruse ; kiosque, grille des gouttes ou banc des capuchons changent le "
        "geste. Le clic revient quand les deux bras sont dedans. Au crochet, une "
        "goutte paie le seuil du départ.\n\n"
        "## Améliorations appliquées\n\n"
        "- Monde (chemin de l'école, gouttière, terre, bouton-cloche) avant l'action.\n"
        "- Désir immédiat (lancer le bateau-feuille) distinct de la leçon.\n"
        "- Première idée échoue : un bras, fermeture muette, feuille au seuil.\n"
        "- Second imprévu plus rusé : sable / clic manquant / manteau à la chaîne.\n"
        "- T1/T2/T3 changent l'action, pas seulement le lieu.\n"
        "- 27 fins textuellement distinctes, dernière image unique.\n"
        "- Un merci (ouverture) et un bravo vécu (bac), pas un refrain.\n"
        "- T3 : kiosque / grille / banc (plus Tom, Léa, Sami).\n"
        "- Pas de « encore / déjà / tout doux », pas merle, pas miel, pas apply.\n\n"
        "## Direction vocale\n\n"
        "TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending) : "
        "rate, pitch, volume, pauses, text_ssml, text_xai_tags, notes d'arc.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, {min(lengths)} à {max(lengths)} mots, moyenne {sum(lengths)//len(lengths)}\n"
        "- 27 fins et 27 dernières images distinctes\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés\n"
        "- N3 ≤ 16 mots/phrase. `check()` OK.\n\n"
        "## Relu\n\n"
        "P0000, 3 L1, 9 L2, 27 résolutions, 27 fins. Questions liées à la scène "
        "(poche / bouton / chaîne). Impatience, découragement, fierté calme.\n\n"
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
