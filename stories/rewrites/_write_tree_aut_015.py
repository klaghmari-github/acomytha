#!/usr/bin/env python3
"""TREE-AUT-015 — Le sac près de la buée (F-NAR-019, N3, AUT.AFF.001, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-015"
N3 = LIMITS["N3"]
TITLE = "Le sac près de la buée"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="grain de sel",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_grain_de_sel_colle_à_la_buée; tempo=naturel; sourire=léger; respiration=ample",
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
        emphasis="sac",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=le_sac_voyage_avec_elle; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="sac",
        note="arc=confirmation; intention=relancer; emotion=élan; intensite=1; destinataire=enfant; sous_texte=le_sac_revient_près_du_jeu; tempo=naturel; sourire=léger; respiration=fluide",
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
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=l_objet_résiste_hors_du_sac; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="grain de sel",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=le_bouton_ferme_sur_le_grain; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="grain de sel",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_de_sel_garde_la_buée; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    starts: list[str] = []
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
        f"destinataire=enfant; sous_texte=le_grain_de_sel_garde_la_buée; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


OPENING = [
    "narrateur|La casserole de cacao chante contre son couvercle.",
    "narrateur|La vapeur grimpe la vitre, lente et chaude.",
    "narrateur|Un moineau tapote le rebord mouillé, bec contre verre.",
    "narrateur|Nina a les pieds qui veulent le gravier du parc.",
    "narrateur|Elle trace un chemin du doigt, dans la buée.",
    "narrateur|Son doigt bute sur un grain de sel, minuscule.",
    "papa|Tu as vu ce grain, Nina ?",
    "enfant-f|Il pique, au milieu de ma route !",
    "narrateur|Sur la chaise, un sac de toile prune attend, ouvert.",
    "narrateur|Son bouton de bois pèse, rond, un peu rêche.",
    "maman|Le parc est derrière la buée.",
    "narrateur|En ce moment, Nina saisit le sac, trop vite.",
    "enfant-f|Je veux le parc, tout de suite !",
    "narrateur|Elle tire, et le bouton de bois accroche la chaise.",
    "narrateur|Le sac reste, les sangles battent ses genoux.",
    "enfant-f|Il ne veut pas venir !",
    "narrateur|Le sourire de Nina disparaît.",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "papa|Le sac, d'abord.",
    "narrateur|Papa s'accroupit, à la même hauteur.",
    "narrateur|Nina presse le sac contre la vitre, pour voir.",
    "narrateur|Le grain de sel glisse, du verre au bouton de bois.",
    "papa|Merci d'avoir repris le sac.",
    "enfant-f|Il vient avec moi.",
]

T1_CHOICE = [
    "narrateur|Le sac prune pèse trop peu, contre l'épaule.",
    "narrateur|Le bac à sable, le toboggan, ou les balançoires.",
    "maman|Où vas-tu d'abord, Nina ?",
]

T1 = {
    1: dict(
        lab="le bac à sable",
        sons="sable,enfants_parc",
        emp="sac",
        retry="Quelque chose est resté dans l'herbe. Qu'est-ce qui est trop loin ?",
        passage=[
            "narrateur|Nina court vers la crique du bac, le sac trop loin.",
            "narrateur|Le sable froid brille, fin, entre les planches.",
            "enfant-f|Je joue, tout de suite !",
            "narrateur|Elle pose le sac dans l'herbe, loin du rebord.",
            "narrateur|Elle plonge les mains, sans lui.",
            "narrateur|Une sangle boit le sable, et le sac penche, vide.",
            "enfant-f|Il n'est plus avec moi !",
            "narrateur|Nina ne rit plus.",
            "papa|Le sac est resté derrière.",
            "narrateur|Maman s'accroupit, à hauteur de sable.",
            "enfant-f|Je le veux, près de moi !",
            "narrateur|Le grain de sel brille, trop loin, sur le bouton de bois.",
        ],
        question=[
            "narrateur|Quelque chose est resté dans l'herbe, trop loin.",
            "maman|Qu'est-ce que Nina a laissé trop loin ?",
        ],
        confirm=[
            "narrateur|Nina ramène le sac contre le rebord de bois.",
            "enfant-f|Toi près de moi, maintenant.",
            "maman|Il est là, trop léger.",
            "papa|On le garde avec nous.",
            "enfant-f|Oui, papa.",
            "narrateur|Le grain de sel tient au bouton, malgré le sable.",
            "papa|Tu l'as vu, le grain ?",
            "enfant-f|Il était sur la vitre, à la cuisine.",
        ],
    ),
    2: dict(
        lab="le toboggan",
        sons="toboggan,enfants_parc",
        emp="sac",
        retry="Quelque chose attend au pied. Qu'est-ce qui est trop loin ?",
        passage=[
            "narrateur|Nina grimpe la rampe tiède, le sac laissé en bas.",
            "narrateur|Le plastique chauffe sous ses paumes.",
            "enfant-f|Je glisse, tout de suite !",
            "narrateur|En haut, elle cherche une sangle, et ne trouve rien.",
            "narrateur|Le sac prune attend au pied, trop petit.",
            "narrateur|Elle descend, les mains vides, trop vite.",
            "enfant-f|Il n'est pas monté avec moi !",
            "narrateur|Nina fixe le bas, sans bouger.",
            "papa|Le sac est resté au pied.",
            "narrateur|Maman s'accroupit, au bas de la rampe.",
            "enfant-f|Je le veux, tout près !",
            "narrateur|Le grain de sel brille en bas, sur le bouton de bois.",
        ],
        question=[
            "narrateur|Quelque chose attend au pied, trop loin.",
            "papa|Qu'est-ce que Nina a laissé en bas ?",
        ],
        confirm=[
            "narrateur|Nina reprend le sac, contre la rampe tiède.",
            "enfant-f|Toi avec moi, cette fois.",
            "maman|Il est là, trop léger.",
            "papa|On le garde au pied, tout près.",
            "enfant-f|Oui, papa.",
            "narrateur|Le grain de sel tient au bouton, malgré la rampe.",
            "papa|Tu l'as vu, le grain ?",
            "enfant-f|Il était sur la vitre, à la cuisine.",
        ],
    ),
    3: dict(
        lab="les balançoires",
        sons="balancoire,enfants_parc",
        emp="sac",
        retry="Quelque chose pend trop loin. Qu'est-ce qui voyage avec Nina ?",
        passage=[
            "narrateur|Nina court vers le pré des chaînes, le sac au bout du bras.",
            "narrateur|L'herbe claque sous ses chaussures.",
            "enfant-f|Je me balance, tout de suite !",
            "narrateur|Elle accroche le sac à un piquet, trop loin.",
            "narrateur|La chaîne froide pique ses paumes, sans sangle.",
            "narrateur|Le sac pend, vide, et ne la suit pas.",
            "enfant-f|Je ne peux plus le prendre !",
            "narrateur|Nina serre les chaînes, les épaules basses.",
            "papa|Le sac est resté au piquet.",
            "narrateur|Maman s'accroupit, dans l'herbe.",
            "enfant-f|Je le veux, près de la chaîne !",
            "narrateur|Le grain de sel brille au piquet, sur le bouton de bois.",
        ],
        question=[
            "narrateur|Quelque chose pend au piquet, trop loin.",
            "maman|Qu'est-ce que Nina a laissé trop loin ?",
        ],
        confirm=[
            "narrateur|Nina décroche le sac, et le pose dans l'herbe proche.",
            "enfant-f|Toi près de la chaîne, maintenant.",
            "maman|Il est là, trop léger.",
            "papa|On le garde avec nous.",
            "enfant-f|Oui, papa.",
            "narrateur|Le grain de sel tient au bouton, malgré l'herbe.",
            "papa|Tu l'as vu, le grain ?",
            "enfant-f|Il était sur la vitre, à la cuisine.",
        ],
    ),
}

T2_CHOICE = {
    1: [
        "narrateur|Le sac tient au rebord, trop léger.",
        "narrateur|Le ballon, le seau, ou le doudou.",
        "papa|Tu prends quoi, pour jouer près du sac ?",
    ],
    2: [
        "narrateur|Le sac attend au pied, trop léger.",
        "narrateur|Le ballon, le seau, ou le doudou.",
        "maman|Tu prends quoi, pour jouer près du sac ?",
    ],
    3: [
        "narrateur|Le sac repose dans l'herbe, trop léger.",
        "narrateur|Le ballon, le seau, ou le doudou.",
        "papa|Tu prends quoi, pour jouer près du sac ?",
    ],
}

T2 = {
    (1, 1): [
        "narrateur|À la crique du bac, le sac tient au rebord.",
        "narrateur|Nina prend le ballon sous le bras, pas dans le sac.",
        "enfant-f|Moi je le porte, plus vite !",
        "narrateur|Le ballon glisse, rond, vers un trou de sable.",
        "narrateur|Elle creuse, trop fort.",
        "narrateur|Le trou s'écroule, et le ballon disparaît.",
        "papa|Le sable a trop aidé.",
        "enfant-f|Je ne le vois plus !",
        "narrateur|Nina s'arrête, les mains froides.",
        "narrateur|Dans sa poitrine, l'envie recule un peu.",
        "enfant-f|Pas trop vite, cette fois.",
        "narrateur|Elle écoute le sable, puis le sac.",
        "narrateur|Le grain de sel brille, sur le bouton de bois.",
        "papa|C'est celui de la vitre, tu vois ?",
        "enfant-f|Oui, il a voyagé avec nous.",
    ],
    (1, 2): [
        "narrateur|À la crique du bac, le sac tient au rebord.",
        "narrateur|Nina accroche le seau dehors, à la sangle.",
        "enfant-f|Il va remplir, tout seul !",
        "narrateur|Le sable entre, lourd, et la sangle tourne.",
        "narrateur|Le seau se renverse, et le sac penche.",
        "maman|L'outil a trop tiré.",
        "enfant-f|Le sac va s'enterrer !",
        "narrateur|Nina lâche la sangle, trop tard.",
        "narrateur|Dans sa poitrine, la peur pique.",
        "enfant-f|Je pose le seau.",
        "narrateur|Elle écoute le sable, puis le bouton.",
        "narrateur|Le grain de sel tremble, collé au bois.",
        "maman|Tu le reconnais, le grain ?",
        "enfant-f|Oui, c'est celui de la buée.",
    ],
    (1, 3): [
        "narrateur|À la crique du bac, le sac tient au rebord.",
        "narrateur|Nina assied le doudou sur la planche, pas dans le sac.",
        "enfant-f|Toi tu regardes, moi je creuse !",
        "narrateur|Le sable monte, fin, jusqu'aux oreilles.",
        "narrateur|Le doudou disparaît, sauf un bout de tissu.",
        "papa|Le rebord n'était pas un nid.",
        "enfant-f|Il a trop bu le sable !",
        "narrateur|Nina veut tout vider, d'un coup.",
        "narrateur|Dans sa poitrine, l'envie se serre.",
        "enfant-f|J'attends un peu.",
        "narrateur|Elle pose les mains, et elle écoute.",
        "narrateur|Le grain de sel luit, sur le bouton de bois.",
        "papa|C'est celui de la cuisine ?",
        "enfant-f|Oui, il a glissé de la vitre.",
    ],
    (2, 1): [
        "narrateur|À la rampe tiède, le sac attend au pied.",
        "narrateur|Nina pose le ballon sur ses genoux, pas dans le sac.",
        "enfant-f|Il glisse avec moi !",
        "narrateur|Le ballon part, plus vite qu'elle.",
        "narrateur|Il roule sous la rampe, et se tait.",
        "papa|Les genoux n'étaient pas un nid.",
        "enfant-f|Il s'est caché dessous !",
        "narrateur|Nina veut se faufiler, trop vite.",
        "narrateur|Dans sa poitrine, la peur pousse.",
        "enfant-f|Je m'arrête.",
        "narrateur|Elle écoute le plastique, puis le sac.",
        "narrateur|Le grain de sel brille, sur le bouton de bois.",
        "papa|C'est celui de la vitre, tu vois ?",
        "enfant-f|Oui, il a voyagé avec nous.",
    ],
    (2, 2): [
        "narrateur|À la rampe tiède, le sac attend au pied.",
        "narrateur|Nina pose le seau en haut, comme un bateau.",
        "enfant-f|Toi tu glisses, avant moi !",
        "narrateur|Le seau part, vide, et s'accroche à mi-pente.",
        "narrateur|Il se renverse, et rien ne tient.",
        "maman|Le seau a trop voyagé seul.",
        "enfant-f|Il n'est plus un bateau !",
        "narrateur|Nina gravit, trop pressée, les pieds chauds.",
        "narrateur|Dans sa poitrine, l'envie recule.",
        "enfant-f|Sans le lancer, alors.",
        "narrateur|Elle pose une paume sur la rampe, et attend.",
        "narrateur|Le grain de sel tremble, collé au bois.",
        "maman|Tu le reconnais, le grain ?",
        "enfant-f|Oui, c'est celui de la buée.",
    ],
    (2, 3): [
        "narrateur|À la rampe tiède, le sac attend au pied.",
        "narrateur|Nina tient le doudou, et lâche la sangle.",
        "enfant-f|Toi tu glisses contre moi !",
        "narrateur|Le doudou s'envole un peu, oreille au vent.",
        "narrateur|Nina le serre, trop fort, et la rampe file.",
        "papa|Les bras n'étaient pas un sac.",
        "enfant-f|Il a failli partir !",
        "narrateur|Nina s'arrête en bas, les joues chaudes.",
        "narrateur|Dans sa poitrine, la peur pique.",
        "enfant-f|Je le pose, d'abord.",
        "narrateur|Elle écoute le plastique, puis le bouton.",
        "narrateur|Le grain de sel luit, sur le bouton de bois.",
        "papa|C'est celui de la cuisine ?",
        "enfant-f|Oui, il a glissé de la vitre.",
    ],
    (3, 1): [
        "narrateur|Au pré des chaînes, le sac repose dans l'herbe.",
        "narrateur|Nina pose le ballon sur le siège, pas dans le sac.",
        "enfant-f|Toi tu te balances, avec moi !",
        "narrateur|Le ballon tombe derrière, sous la planche.",
        "narrateur|Il se tait, dans l'ombre de l'herbe.",
        "papa|Le siège n'était pas un nid.",
        "enfant-f|Il est passé derrière !",
        "narrateur|Nina veut ramper dessous, trop vite.",
        "narrateur|Dans sa poitrine, l'envie se serre.",
        "enfant-f|Pas trop vite, cette fois.",
        "narrateur|Elle écoute les chaînes, puis le sac.",
        "narrateur|Le grain de sel brille, sur le bouton de bois.",
        "papa|C'est celui de la vitre, tu vois ?",
        "enfant-f|Oui, il a voyagé avec nous.",
    ],
    (3, 2): [
        "narrateur|Au pré des chaînes, le sac repose dans l'herbe.",
        "narrateur|Nina pose le seau sur l'autre siège, comme un poids.",
        "enfant-f|Toi tu tiens, et moi je pars !",
        "narrateur|Le seau bascule, et la sangle s'enroule à la chaîne.",
        "narrateur|Le sac grimpe, tordu, trop haut.",
        "maman|Le poids a trop tiré.",
        "enfant-f|Le sac est coincé !",
        "narrateur|Nina tire, puis s'arrête, les mains piquées.",
        "narrateur|Dans sa poitrine, la peur pousse.",
        "enfant-f|Sans tirer, alors.",
        "narrateur|Elle écoute la chaîne, puis le bouton.",
        "narrateur|Le grain de sel tremble, collé au bois.",
        "maman|Tu le reconnais, le grain ?",
        "enfant-f|Oui, c'est celui de la buée.",
    ],
    (3, 3): [
        "narrateur|Au pré des chaînes, le sac repose dans l'herbe.",
        "narrateur|Nina cale le doudou dans la chaîne, pas dans le sac.",
        "enfant-f|Toi tu tiens, je pousse !",
        "narrateur|La chaîne pince une oreille, froide.",
        "narrateur|Le doudou reste, trop serré.",
        "papa|La chaîne n'était pas un nid.",
        "enfant-f|Il est pris !",
        "narrateur|Nina veut arracher, trop fort.",
        "narrateur|Dans sa poitrine, l'envie se tait.",
        "enfant-f|J'attends un peu.",
        "narrateur|Elle pose l'oreille près de la chaîne, et écoute.",
        "narrateur|Le grain de sel luit, sur le bouton de bois.",
        "papa|C'est celui de la cuisine ?",
        "enfant-f|Oui, il a glissé de la vitre.",
    ],
}

T3_CHOICE = {
    (1, 1): [
        "narrateur|Le ballon se tait sous le sable, le sac attend.",
        "narrateur|La gourde, le goûter, ou la casquette.",
        "maman|Qu'est-ce qui manque, dans le sac ?",
    ],
    (1, 2): [
        "narrateur|Le seau s'est tu, le sac penche un peu.",
        "narrateur|La gourde, le goûter, ou la casquette.",
        "papa|Qu'est-ce qui manque, dans le sac ?",
    ],
    (1, 3): [
        "narrateur|Le doudou attend sous le sable, le sac est creux.",
        "narrateur|La gourde, le goûter, ou la casquette.",
        "maman|Qu'est-ce qui manque, dans le sac ?",
    ],
    (2, 1): [
        "narrateur|Le ballon se tait sous la rampe, le sac attend.",
        "narrateur|La gourde, le goûter, ou la casquette.",
        "papa|Qu'est-ce qui manque, dans le sac ?",
    ],
    (2, 2): [
        "narrateur|Le seau s'est tu à mi-pente, le sac est creux.",
        "narrateur|La gourde, le goûter, ou la casquette.",
        "maman|Qu'est-ce qui manque, dans le sac ?",
    ],
    (2, 3): [
        "narrateur|Le doudou a failli filer, le sac attend.",
        "narrateur|La gourde, le goûter, ou la casquette.",
        "papa|Qu'est-ce qui manque, dans le sac ?",
    ],
    (3, 1): [
        "narrateur|Le ballon se tait derrière le siège, le sac attend.",
        "narrateur|La gourde, le goûter, ou la casquette.",
        "maman|Qu'est-ce qui manque, dans le sac ?",
    ],
    (3, 2): [
        "narrateur|Le seau s'est tu, la sangle reste tordue.",
        "narrateur|La gourde, le goûter, ou la casquette.",
        "papa|Qu'est-ce qui manque, dans le sac ?",
    ],
    (3, 3): [
        "narrateur|Le doudou attend dans la chaîne, le sac est creux.",
        "narrateur|La gourde, le goûter, ou la casquette.",
        "maman|Qu'est-ce qui manque, dans le sac ?",
    ],
}

RES = {
    (1, 1, 1): [
        "enfant-f|Le ballon dans le sac, puis la gourde, debout !",
        "narrateur|Nina cherche, sans foncer.",
        "narrateur|Elle suit le grain de sel, jusqu'au bouton de bois.",
        "narrateur|Le ballon rentre, puis la gourde, fraîche.",
        "narrateur|Le bouton ferme, net, sur le grain.",
        "papa|Le grain a parlé, sur le bois.",
        "enfant-f|Mes affaires voyagent, avec moi !",
        "maman|Le trou a failli tout garder.",
        "narrateur|Un rond de sable colle à la gourde.",
        "papa|Tu as vu le grain, sur le bouton ?",
        "enfant-f|Il était sur la vitre, à la cuisine.",
    ],
    (1, 1, 2): [
        "enfant-f|Le ballon dans le sac, et la pomme dans le creux !",
        "narrateur|Nina souffle, puis avance une main.",
        "narrateur|Le grain de sel guide sa main, vers le bouton.",
        "narrateur|Le ballon rentre, la pomme se cale, ronde.",
        "narrateur|Le sac se ferme, grain au milieu.",
        "papa|Le grain a parlé, très bas.",
        "enfant-f|La pomme a un nid, maintenant !",
        "maman|Le trou a failli tout garder.",
        "narrateur|Une miette de pomme dort dans le sable.",
        "papa|Le grain est là, tu le sens ?",
        "enfant-f|Oui, c'est celui de la buée.",
    ],
    (1, 1, 3): [
        "enfant-f|Le ballon sous la visière, dans le sac !",
        "narrateur|Nina refuse de creuser plus fort.",
        "narrateur|Nina retrouve le grain, collé au bois.",
        "narrateur|La casquette accueille le ballon, puis rentre.",
        "narrateur|Le bouton de bois pince le grain, et tient.",
        "papa|Le grain a parlé, comme une lanterne.",
        "enfant-f|La visière a fait un nid !",
        "maman|Le trou a failli tout garder.",
        "narrateur|La visière garde un voile de sable.",
        "papa|Tu reconnais le grain, du verre ?",
        "enfant-f|Il a glissé du verre, tout petit.",
    ],
    (1, 2, 1): [
        "enfant-f|Le seau vide, puis la gourde dedans, dans le sac !",
        "narrateur|Nina penche le seau, loin du sable.",
        "narrateur|Elle pose le doigt sur le grain, sans presser.",
        "narrateur|La gourde se tient, fraîche, au fond du seau.",
        "narrateur|Le bouton parle, contre le grain.",
        "papa|Le grain a parlé, sur le bois.",
        "enfant-f|Le seau est un nid, pas un poids !",
        "maman|La sangle a failli tout enterrer.",
        "narrateur|Le seau tient une goutte fraîche, collée au grain.",
        "papa|Tu as vu le grain, sur le bouton ?",
        "enfant-f|Il était sur la vitre, à la cuisine.",
    ],
    (1, 2, 2): [
        "enfant-f|La pomme dans le seau, puis le seau dans le sac !",
        "narrateur|Nina vide le sable, sans tirer.",
        "narrateur|Le grain de sel montre le bouton, minuscule.",
        "narrateur|La pomme se cale, et le seau rentre, léger.",
        "narrateur|Le sac pèse, grain sous le bois.",
        "papa|Le grain a parlé, très bas.",
        "enfant-f|Le goûter a un seau, maintenant !",
        "maman|La sangle a failli tout enterrer.",
        "narrateur|Une croûte de pain sent le sable, sous le grain.",
        "papa|Le grain est là, tu le sens ?",
        "enfant-f|Oui, c'est celui de la buée.",
    ],
    (1, 2, 3): [
        "enfant-f|La casquette en couvercle, sur le seau, dans le sac !",
        "narrateur|Nina pose la visière, sans presser le sable.",
        "narrateur|Elle écoute le sac, et retrouve le grain.",
        "narrateur|Le seau rentre, chapeau dessus, léger.",
        "narrateur|Le bouton rentre, et le grain reste.",
        "papa|Le grain a parlé, comme une lanterne.",
        "enfant-f|La visière a tenu le seau !",
        "maman|La sangle a failli tout enterrer.",
        "narrateur|La visière sert de couvercle au seau, grain dessus.",
        "papa|Tu reconnais le grain, du verre ?",
        "enfant-f|Il a glissé du verre, tout petit.",
    ],
    (1, 3, 1): [
        "enfant-f|Le doudou dans le sac, la gourde à côté !",
        "narrateur|Nina soulève le tissu, grain après grain.",
        "narrateur|Nina regarde le grain, collé au bois rêche.",
        "narrateur|Le doudou rentre, la gourde se cale, fraîche.",
        "narrateur|Le bois ferme, grain coincé, gentiment.",
        "papa|Le grain a parlé, sur le bois.",
        "enfant-f|Il a un nid, plus le rebord !",
        "maman|Le sable a failli tout garder.",
        "narrateur|L'oreille du doudou a un fil de sable, près du grain.",
        "papa|Tu as vu le grain, sur le bouton ?",
        "enfant-f|Il était sur la vitre, à la cuisine.",
    ],
    (1, 3, 2): [
        "enfant-f|La pomme dans les bras du doudou, dans le sac !",
        "narrateur|Nina souffle le sable, sans vider le bac.",
        "narrateur|Le grain brille, et sa main ralentit.",
        "narrateur|Le doudou rentre, la pomme au creux, ronde.",
        "narrateur|Le bouton tient, grain au chaud.",
        "papa|Le grain a parlé, très bas.",
        "enfant-f|Il tient le goûter, maintenant !",
        "maman|Le sable a failli tout garder.",
        "narrateur|La pomme chauffe dans les bras du doudou.",
        "papa|Le grain est là, tu le sens ?",
        "enfant-f|Oui, c'est celui de la buée.",
    ],
    (1, 3, 3): [
        "enfant-f|La casquette sur le doudou, puis dans le sac !",
        "narrateur|Nina refuse de tout vider d'un coup.",
        "narrateur|Elle cherche le grain, du doigt, sur le bois.",
        "narrateur|Le doudou rentre, casquette sur l'oreille.",
        "narrateur|Le sac se cale, grain vers le tissu.",
        "papa|Le grain a parlé, comme une lanterne.",
        "enfant-f|Il a un chapeau, et un nid !",
        "maman|Le sable a failli tout garder.",
        "narrateur|Le doudou porte la casquette, grain sur la visière.",
        "papa|Tu reconnais le grain, du verre ?",
        "enfant-f|Il a glissé du verre, tout petit.",
    ],
    (2, 1, 1): [
        "enfant-f|Le ballon dans le sac, la gourde pour le caler !",
        "narrateur|Nina se penche sous la rampe, sans se faufiler.",
        "narrateur|Nina aligne le grain, face à la rampe.",
        "narrateur|Le ballon rentre, la gourde le cale, tiède.",
        "narrateur|Le bouton ferme, tiède, sur le grain.",
        "papa|Le grain a parlé, sur le bois.",
        "enfant-f|La gourde a tenu le ballon !",
        "maman|Le dessous a failli tout garder.",
        "narrateur|La gourde est tiède, comme la rampe, sous le grain.",
        "papa|Tu as vu le grain, sur le bouton ?",
        "enfant-f|Il était sur la vitre, à la cuisine.",
    ],
    (2, 1, 2): [
        "enfant-f|Le ballon dans le sac, la pomme pour le peser !",
        "narrateur|Nina tend le bras, sans ramper.",
        "narrateur|Le grain de sel attend, sur le bouton de bois.",
        "narrateur|Le ballon rentre, la pomme pèse, ronde.",
        "narrateur|Le sac se ferme, grain contre la pomme.",
        "papa|Le grain a parlé, très bas.",
        "enfant-f|La pomme a tenu le ballon !",
        "maman|Le dessous a failli tout garder.",
        "narrateur|La pomme a un trait lisse, collé au grain de sel.",
        "papa|Le grain est là, tu le sens ?",
        "enfant-f|Oui, c'est celui de la buée.",
    ],
    (2, 1, 3): [
        "enfant-f|La casquette comme un filet, pour le ballon !",
        "narrateur|Nina glisse la visière sous la rampe, lentement.",
        "narrateur|Elle touche le grain, puis le bouton.",
        "narrateur|Le ballon roule dans la visière, puis dans le sac.",
        "narrateur|Le bouton de bois serre le grain, sans pincer.",
        "papa|Le grain a parlé, comme une lanterne.",
        "enfant-f|La visière a attrapé, sans foncer !",
        "maman|Le dessous a failli tout garder.",
        "narrateur|La visière tient une poussière de rampe, près du grain.",
        "papa|Tu reconnais le grain, du verre ?",
        "enfant-f|Il a glissé du verre, tout petit.",
    ],
    (2, 2, 1): [
        "enfant-f|Le seau en bas, la gourde pour l'accueillir !",
        "narrateur|Nina descend, une marche après l'autre.",
        "narrateur|Nina suit le grain, du pied au bois.",
        "narrateur|Le seau rentre, la gourde au fond, fraîche.",
        "narrateur|Le bouton parle, au pied de la rampe.",
        "papa|Le grain a parlé, sur le bois.",
        "enfant-f|Le seau a un nid, plus la pente !",
        "maman|La rampe a failli tout garder.",
        "narrateur|Le seau garde une goutte de rampe, sous le grain.",
        "papa|Tu as vu le grain, sur le bouton ?",
        "enfant-f|Il était sur la vitre, à la cuisine.",
    ],
    (2, 2, 2): [
        "enfant-f|La pomme dans le seau, après la rampe !",
        "narrateur|Nina attend que le seau se taise.",
        "narrateur|Le grain de sel tremble, et elle s'arrête.",
        "narrateur|La pomme se cale, le seau rentre, tiède.",
        "narrateur|Le sac pèse, grain sous la croûte.",
        "papa|Le grain a parlé, très bas.",
        "enfant-f|Le goûter a voyagé, sans glisser !",
        "maman|La rampe a failli tout garder.",
        "narrateur|Une croûte tiède sent le plastique, près du grain.",
        "papa|Le grain est là, tu le sens ?",
        "enfant-f|Oui, c'est celui de la buée.",
    ],
    (2, 2, 3): [
        "enfant-f|La casquette dans le seau, puis le seau dans le sac !",
        "narrateur|Nina refuse de relancer le seau.",
        "narrateur|Elle retrouve le grain, au milieu du bouton.",
        "narrateur|La visière se cale, le seau rentre, léger.",
        "narrateur|Le bouton rentre, visière au bord.",
        "papa|Le grain a parlé, comme une lanterne.",
        "enfant-f|La visière a voyagé, sans voile !",
        "maman|La rampe a failli tout garder.",
        "narrateur|La visière a voyagé dans le seau, grain au bord.",
        "papa|Tu reconnais le grain, du verre ?",
        "enfant-f|Il a glissé du verre, tout petit.",
    ],
    (2, 3, 1): [
        "enfant-f|Le doudou dans le sac, la gourde contre l'oreille !",
        "narrateur|Nina pose le tissu, sans le lancer.",
        "narrateur|Nina pose l'oreille près du sac, et voit le grain.",
        "narrateur|Le doudou rentre, la gourde le cale, tiède.",
        "narrateur|Le bois ferme, grain dans un pli.",
        "papa|Le grain a parlé, sur le bois.",
        "enfant-f|Il a un nid, plus le vent !",
        "maman|La rampe a failli l'emporter.",
        "narrateur|Le doudou sent la rampe, grain de sel dans un pli.",
        "papa|Tu as vu le grain, sur le bouton ?",
        "enfant-f|Il était sur la vitre, à la cuisine.",
    ],
    (2, 3, 2): [
        "enfant-f|La pomme pour le doudou, dans le sac !",
        "narrateur|Nina serre moins fort, et avance.",
        "narrateur|Le grain de sel luit, contre le bois rêche.",
        "narrateur|Le doudou rentre, la pomme au creux, ronde.",
        "narrateur|Le bouton tient, grain contre la pomme.",
        "papa|Le grain a parlé, très bas.",
        "enfant-f|Il tient le goûter, sans le vent !",
        "maman|La rampe a failli l'emporter.",
        "narrateur|La pomme sent le tissu du doudou, sous le grain.",
        "papa|Le grain est là, tu le sens ?",
        "enfant-f|Oui, c'est celui de la buée.",
    ],
    (2, 3, 3): [
        "enfant-f|La casquette sur le doudou, avant le sac !",
        "narrateur|Nina pose la visière, oreille à l'abri.",
        "narrateur|Elle garde le grain, sous l'ongle, une seconde.",
        "narrateur|Le doudou rentre, casquette contre le vent.",
        "narrateur|Le sac se cale, grain sous la visière.",
        "papa|Le grain a parlé, comme une lanterne.",
        "enfant-f|Il a un chapeau, et un nid !",
        "maman|La rampe a failli l'emporter.",
        "narrateur|Un poil de doudou colle à la visière, près du grain.",
        "papa|Tu reconnais le grain, du verre ?",
        "enfant-f|Il a glissé du verre, tout petit.",
    ],
    (3, 1, 1): [
        "enfant-f|Le ballon dans le sac, la gourde pour le nid !",
        "narrateur|Nina contourne le siège, sans ramper.",
        "narrateur|Nina contourne le grain, puis le bouton.",
        "narrateur|Le ballon rentre, la gourde le cale, fraîche.",
        "narrateur|Le bouton ferme, frais, sur le grain.",
        "papa|Le grain a parlé, sur le bois.",
        "enfant-f|La gourde a fait le nid !",
        "maman|L'ombre a failli tout garder.",
        "narrateur|La gourde a une marque d'herbe, sous le grain de sel.",
        "papa|Tu as vu le grain, sur le bouton ?",
        "enfant-f|Il était sur la vitre, à la cuisine.",
    ],
    (3, 1, 2): [
        "enfant-f|La pomme comme un siège, pour le ballon, dans le sac !",
        "narrateur|Nina tend le bras derrière, sans se coucher.",
        "narrateur|Le grain de sel pique, comme à la vitre.",
        "narrateur|Le ballon rentre, la pomme le cale, froide.",
        "narrateur|Le sac se ferme, grain contre la chaîne.",
        "papa|Le grain a parlé, très bas.",
        "enfant-f|La pomme a tenu le ballon !",
        "maman|L'ombre a failli tout garder.",
        "narrateur|La pomme est froide, comme la chaîne, près du grain.",
        "papa|Le grain est là, tu le sens ?",
        "enfant-f|Oui, c'est celui de la buée.",
    ],
    (3, 1, 3): [
        "enfant-f|La casquette comme un hamac, pour le ballon !",
        "narrateur|Nina glisse la visière sous le siège, lentement.",
        "narrateur|Elle reconnaît le grain, minuscule, sur le bois.",
        "narrateur|Le ballon roule dans la visière, puis dans le sac.",
        "narrateur|Le bouton de bois accueille le grain, et tient.",
        "papa|Le grain a parlé, comme une lanterne.",
        "enfant-f|La visière a attrapé, sans ramper !",
        "maman|L'ombre a failli tout garder.",
        "narrateur|La visière a un pli de chaîne, sous le grain de sel.",
        "papa|Tu reconnais le grain, du verre ?",
        "enfant-f|Il a glissé du verre, tout petit.",
    ],
    (3, 2, 1): [
        "enfant-f|Je décroche le seau, puis la gourde dans le sac !",
        "narrateur|Nina tourne la sangle, sans tirer.",
        "narrateur|Nina souffle sur le grain, collé au bouton.",
        "narrateur|Le seau rentre, la gourde au fond, fraîche.",
        "narrateur|Le bouton parle, seau libre.",
        "papa|Le grain a parlé, sur le bois.",
        "enfant-f|Le seau est libre, et dedans !",
        "maman|La chaîne a failli tout garder.",
        "narrateur|Le seau sent l'herbe, grain de sel au fond.",
        "papa|Tu as vu le grain, sur le bouton ?",
        "enfant-f|Il était sur la vitre, à la cuisine.",
    ],
    (3, 2, 2): [
        "enfant-f|La pomme dans le seau, quand la sangle est libre !",
        "narrateur|Nina attend que la chaîne se taise.",
        "narrateur|Le grain de sel reste, malgré la chaîne.",
        "narrateur|La pomme se cale, le seau rentre, léger.",
        "narrateur|Le sac pèse, grain près de la croûte.",
        "papa|Le grain a parlé, très bas.",
        "enfant-f|Le goûter a un seau, sans chaîne !",
        "maman|La chaîne a failli tout garder.",
        "narrateur|Une croûte garde l'ombre de la chaîne, près du grain.",
        "papa|Le grain est là, tu le sens ?",
        "enfant-f|Oui, c'est celui de la buée.",
    ],
    (3, 2, 3): [
        "enfant-f|La casquette pour ombrer le seau, dans le sac !",
        "narrateur|Nina décroche, puis pose la visière.",
        "narrateur|Elle suit le grain, de l'herbe au bois.",
        "narrateur|Le seau rentre, casquette dessus, léger.",
        "narrateur|Le bouton rentre, visière au milieu.",
        "papa|Le grain a parlé, comme une lanterne.",
        "enfant-f|La visière a ombré, sans tirer !",
        "maman|La chaîne a failli tout garder.",
        "narrateur|La visière ombre le seau, grain de sel au milieu.",
        "papa|Tu reconnais le grain, du verre ?",
        "enfant-f|Il a glissé du verre, tout petit.",
    ],
    (3, 3, 1): [
        "enfant-f|Je libère l'oreille, puis la gourde dans le sac !",
        "narrateur|Nina ouvre la chaîne, sans arracher.",
        "narrateur|Nina libère l'oreille, puis voit le grain.",
        "narrateur|Le doudou rentre, la gourde contre l'oreille.",
        "narrateur|Le bois ferme, grain contre l'oreille.",
        "papa|Le grain a parlé, sur le bois.",
        "enfant-f|L'oreille est libre, et au nid !",
        "maman|La chaîne a failli tout garder.",
        "narrateur|L'oreille du doudou sent l'herbe, sous le grain de sel.",
        "papa|Tu as vu le grain, sur le bouton ?",
        "enfant-f|Il était sur la vitre, à la cuisine.",
    ],
    (3, 3, 2): [
        "enfant-f|La pomme pour réchauffer l'oreille, dans le sac !",
        "narrateur|Nina ouvre la chaîne, un maillon après l'autre.",
        "narrateur|Le grain de sel chauffe, sous son doigt.",
        "narrateur|Le doudou rentre, la pomme contre l'oreille.",
        "narrateur|Le bouton tient, grain près de la pomme.",
        "papa|Le grain a parlé, très bas.",
        "enfant-f|L'oreille a un goûter, maintenant !",
        "maman|La chaîne a failli tout garder.",
        "narrateur|La pomme a réchauffé l'oreille, près du grain de sel.",
        "papa|Le grain est là, tu le sens ?",
        "enfant-f|Oui, c'est celui de la buée.",
    ],
    (3, 3, 3): [
        "enfant-f|La casquette sur l'oreille, puis dans le sac !",
        "narrateur|Nina ouvre la chaîne, sans tirer le tissu.",
        "narrateur|Elle pose le doigt au centre du bouton, sur le grain.",
        "narrateur|Le doudou rentre, casquette sur l'oreille libre.",
        "narrateur|Le sac se cale, grain sous le dessin.",
        "papa|Le grain a parlé, comme une lanterne.",
        "enfant-f|Il a un chapeau, et un nid !",
        "maman|La chaîne a failli tout garder.",
        "narrateur|Un dessin de chaîne reste sur la visière, sous le grain.",
        "papa|Tu reconnais le grain, du verre ?",
        "enfant-f|Il a glissé du verre, tout petit.",
    ],
}

FINS = {
    (1, 1, 1): [
        "narrateur|Ils rentrent, le sac prune lourd contre l'épaule.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle gourde tu gardes, près du cacao ?",
        "enfant-f|Celle du rond de sable.",
        "maman|Ça a failli rester sous le trou.",
        "enfant-f|Le ballon a un nid, maintenant.",
        "narrateur|Un rond de sable entoure la gourde, sous le grain de sel.",
    ],
    (1, 1, 2): [
        "narrateur|Ils rentrent, le sac prune sent la pomme.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "maman|Quelle pomme tu gardes, près du cacao ?",
        "enfant-f|Celle du creux de sable.",
        "papa|Ça a failli rester sous le trou.",
        "enfant-f|Le ballon a un goûter, maintenant.",
        "narrateur|Une miette de pomme dort dans le sable, près du grain.",
    ],
    (1, 1, 3): [
        "narrateur|Ils rentrent, le sac prune sent le soleil.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle visière tu gardes, près du cacao ?",
        "enfant-f|Celle du voile de sable.",
        "maman|Ça a failli rester sous le trou.",
        "enfant-f|Le ballon a un chapeau, maintenant.",
        "narrateur|La visière garde un voile de sable, sous le grain de sel.",
    ],
    (1, 2, 1): [
        "narrateur|Ils rentrent, le sac prune cloche un peu, seau dedans.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle gourde tu gardes, près du cacao ?",
        "enfant-f|Celle de la goutte fraîche.",
        "maman|Ça a failli s'enterrer, avec la sangle.",
        "enfant-f|Le seau a un nid, maintenant.",
        "narrateur|Le seau tient une goutte fraîche, collée au grain de sel.",
    ],
    (1, 2, 2): [
        "narrateur|Ils rentrent, le sac prune sent le pain et le sable.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "maman|Quelle croûte tu gardes, près du cacao ?",
        "enfant-f|Celle qui sent le sable.",
        "papa|Ça a failli s'enterrer, avec la sangle.",
        "enfant-f|Le seau a un goûter, maintenant.",
        "narrateur|Une croûte de pain sent le sable, sous le grain de sel.",
    ],
    (1, 2, 3): [
        "narrateur|Ils rentrent, le sac prune a un couvercle de visière.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle visière tu gardes, près du cacao ?",
        "enfant-f|Celle qui a couvert le seau.",
        "maman|Ça a failli s'enterrer, avec la sangle.",
        "enfant-f|Le seau a un chapeau, maintenant.",
        "narrateur|La visière sert de couvercle au seau, grain de sel dessus.",
    ],
    (1, 3, 1): [
        "narrateur|Ils rentrent, le sac prune sent le doudou sablé.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle gourde tu gardes, près du cacao ?",
        "enfant-f|Celle près de l'oreille sablée.",
        "maman|Ça a failli rester sous le rebord.",
        "enfant-f|Le doudou a un nid, maintenant.",
        "narrateur|L'oreille du doudou a un fil de sable, près du grain.",
    ],
    (1, 3, 2): [
        "narrateur|Ils rentrent, le sac prune sent la pomme tiède.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "maman|Quelle pomme tu gardes, près du cacao ?",
        "enfant-f|Celle des bras du doudou.",
        "papa|Ça a failli rester sous le rebord.",
        "enfant-f|Le doudou a un goûter, maintenant.",
        "narrateur|La pomme chauffe dans les bras du doudou, grain au bouton.",
    ],
    (1, 3, 3): [
        "narrateur|Ils rentrent, le sac prune a un doudou coiffé.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle visière tu gardes, près du cacao ?",
        "enfant-f|Celle sur l'oreille du doudou.",
        "maman|Ça a failli rester sous le rebord.",
        "enfant-f|Le doudou a un chapeau, maintenant.",
        "narrateur|Le doudou porte la casquette, grain de sel sur la visière.",
    ],
    (2, 1, 1): [
        "narrateur|Ils rentrent, le sac prune est tiède, comme la rampe.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle gourde tu gardes, près du cacao ?",
        "enfant-f|Celle tiède, comme la rampe.",
        "maman|Ça a failli rester sous le plastique.",
        "enfant-f|Le ballon a un nid, maintenant.",
        "narrateur|La gourde est tiède, comme la rampe, sous le grain de sel.",
    ],
    (2, 1, 2): [
        "narrateur|Ils rentrent, le sac prune sent la pomme lisse.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "maman|Quelle pomme tu gardes, près du cacao ?",
        "enfant-f|Celle du trait lisse.",
        "papa|Ça a failli rester sous le plastique.",
        "enfant-f|Le ballon a un goûter, maintenant.",
        "narrateur|La pomme a un trait lisse, collé au grain de sel.",
    ],
    (2, 1, 3): [
        "narrateur|Ils rentrent, le sac prune sent la poussière de rampe.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle visière tu gardes, près du cacao ?",
        "enfant-f|Celle de la poussière de rampe.",
        "maman|Ça a failli rester sous le plastique.",
        "enfant-f|Le ballon a un chapeau, maintenant.",
        "narrateur|La visière tient une poussière de rampe, près du grain.",
    ],
    (2, 2, 1): [
        "narrateur|Ils rentrent, le sac prune cloche, seau et gourde.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle gourde tu gardes, près du cacao ?",
        "enfant-f|Celle de la goutte de rampe.",
        "maman|Ça a failli rester à mi-pente.",
        "enfant-f|Le seau a un nid, maintenant.",
        "narrateur|Le seau garde une goutte de rampe, sous le grain de sel.",
    ],
    (2, 2, 2): [
        "narrateur|Ils rentrent, le sac prune sent le plastique tiède.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "maman|Quelle croûte tu gardes, près du cacao ?",
        "enfant-f|Celle qui sent le plastique.",
        "papa|Ça a failli rester à mi-pente.",
        "enfant-f|Le seau a un goûter, maintenant.",
        "narrateur|Une croûte tiède sent le plastique, près du grain de sel.",
    ],
    (2, 2, 3): [
        "narrateur|Ils rentrent, le sac prune a une visière au bord du seau.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle visière tu gardes, près du cacao ?",
        "enfant-f|Celle du bord du seau.",
        "maman|Ça a failli rester à mi-pente.",
        "enfant-f|Le seau a un chapeau, maintenant.",
        "narrateur|La visière a voyagé dans le seau, grain de sel au bord.",
    ],
    (2, 3, 1): [
        "narrateur|Ils rentrent, le sac prune sent le doudou chaud.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle gourde tu gardes, près du cacao ?",
        "enfant-f|Celle du pli du doudou.",
        "maman|Ça a failli filer avec le vent.",
        "enfant-f|Le doudou a un nid, maintenant.",
        "narrateur|Le doudou sent la rampe, grain de sel dans un pli.",
    ],
    (2, 3, 2): [
        "narrateur|Ils rentrent, le sac prune sent le tissu et la pomme.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "maman|Quelle pomme tu gardes, près du cacao ?",
        "enfant-f|Celle qui sent le doudou.",
        "papa|Ça a failli filer avec le vent.",
        "enfant-f|Le doudou a un goûter, maintenant.",
        "narrateur|La pomme sent le tissu du doudou, sous le grain de sel.",
    ],
    (2, 3, 3): [
        "narrateur|Ils rentrent, le sac prune a un poil sur la visière.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle visière tu gardes, près du cacao ?",
        "enfant-f|Celle du poil de doudou.",
        "maman|Ça a failli filer avec le vent.",
        "enfant-f|Le doudou a un chapeau, maintenant.",
        "narrateur|Un poil de doudou colle à la visière, près du grain.",
    ],
    (3, 1, 1): [
        "narrateur|Ils rentrent, le sac prune sent l'herbe du pré.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle gourde tu gardes, près du cacao ?",
        "enfant-f|Celle de la marque d'herbe.",
        "maman|Ça a failli rester sous le siège.",
        "enfant-f|Le ballon a un nid, maintenant.",
        "narrateur|La gourde a une marque d'herbe, sous le grain de sel.",
    ],
    (3, 1, 2): [
        "narrateur|Ils rentrent, le sac prune sent la pomme froide.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "maman|Quelle pomme tu gardes, près du cacao ?",
        "enfant-f|Celle froide, comme la chaîne.",
        "papa|Ça a failli rester sous le siège.",
        "enfant-f|Le ballon a un goûter, maintenant.",
        "narrateur|La pomme est froide, comme la chaîne, près du grain.",
    ],
    (3, 1, 3): [
        "narrateur|Ils rentrent, le sac prune a un pli de chaîne.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle visière tu gardes, près du cacao ?",
        "enfant-f|Celle du pli de chaîne.",
        "maman|Ça a failli rester sous le siège.",
        "enfant-f|Le ballon a un chapeau, maintenant.",
        "narrateur|La visière a un pli de chaîne, sous le grain de sel.",
    ],
    (3, 2, 1): [
        "narrateur|Ils rentrent, le sac prune sent l'herbe et le seau.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle gourde tu gardes, près du cacao ?",
        "enfant-f|Celle du fond du seau.",
        "maman|Ça a failli rester dans la chaîne.",
        "enfant-f|Le seau a un nid, maintenant.",
        "narrateur|Le seau sent l'herbe, grain de sel au fond.",
    ],
    (3, 2, 2): [
        "narrateur|Ils rentrent, le sac prune sent l'ombre de la chaîne.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "maman|Quelle croûte tu gardes, près du cacao ?",
        "enfant-f|Celle de l'ombre de la chaîne.",
        "papa|Ça a failli rester dans la chaîne.",
        "enfant-f|Le seau a un goûter, maintenant.",
        "narrateur|Une croûte garde l'ombre de la chaîne, près du grain.",
    ],
    (3, 2, 3): [
        "narrateur|Ils rentrent, le sac prune a une visière au milieu du seau.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle visière tu gardes, près du cacao ?",
        "enfant-f|Celle au milieu du seau.",
        "maman|Ça a failli rester dans la chaîne.",
        "enfant-f|Le seau a un chapeau, maintenant.",
        "narrateur|La visière ombre le seau, grain de sel au milieu.",
    ],
    (3, 3, 1): [
        "narrateur|Ils rentrent, le sac prune sent l'oreille libre.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle gourde tu gardes, près du cacao ?",
        "enfant-f|Celle contre l'oreille d'herbe.",
        "maman|Ça a failli rester dans la chaîne.",
        "enfant-f|Le doudou a un nid, maintenant.",
        "narrateur|L'oreille du doudou sent l'herbe, sous le grain de sel.",
    ],
    (3, 3, 2): [
        "narrateur|Ils rentrent, le sac prune sent la pomme chaude.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "maman|Quelle pomme tu gardes, près du cacao ?",
        "enfant-f|Celle qui a réchauffé l'oreille.",
        "papa|Ça a failli rester dans la chaîne.",
        "enfant-f|Le doudou a un goûter, maintenant.",
        "narrateur|La pomme a réchauffé l'oreille, près du grain de sel.",
    ],
    (3, 3, 3): [
        "narrateur|Ils rentrent, le sac prune a un dessin de chaîne.",
        "narrateur|La vitre de la cuisine est embuée, tiède.",
        "narrateur|Nina pose le sac sur la chaise, bouton vers le verre.",
        "papa|Quelle visière tu gardes, près du cacao ?",
        "enfant-f|Celle du dessin de chaîne.",
        "maman|Ça a failli rester dans la chaîne.",
        "enfant-f|Le doudou a un chapeau, maintenant.",
        "narrateur|Un dessin de chaîne reste sur la visière, sous le grain de sel.",
    ],
}


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    chunks: list[dict] = []

    def add(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        chunks.append(voice(by_src[cid], lines, profile, sons, extra))

    add("CHK_T0000_P0000", OPENING, "opening", "casserole,moineau")
    add("CHK_T0001_P0000", T1_CHOICE, "choice", "", {"pause_before_ms": 200})

    t2_sons = {1: "ballon,enfants_parc", 2: "seau,sable", 3: "tissu,doudou"}
    t3_sons = {1: "eau,gourde", 2: "pomme,gouter", 3: "tissu,casquette"}

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
                "expected_answer": "sac",
                "accepted_examples": "sac | le sac | dans le sac | le sac prune | son sac",
                "retry_prompt": t1["retry"],
                "engine_ok_text": "Oui, c'est le sac.",
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
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
                {"emphasis": "grain de sel"},
            )
            add(
                f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
                T3_CHOICE[(a, b)],
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
                    {"emphasis": "grain de sel"},
                )
                add(
                    f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}_F0001",
                    FINS[(a, b, c)],
                    "ending",
                    "casserole,vitre",
                    {"note": ending_note(a, b, c), "emphasis": "grain de sel"},
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
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "sac" not in blob:
        raise SystemExit(f"{SID}: sac absent")
    if "grain de sel" not in blob:
        raise SystemExit(f"{SID}: grain de sel absent")
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
        "sac bleu",
        "sac jaune",
        "virgule",
        "nacre",
        "laitue",
        "grain de sable",
    ):
        if bad in blob:
            raise SystemExit(f"{SID}: interdit {bad}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in chunks)
    if not tts_ok:
        raise SystemExit(f"{SID}: TTS incomplet")

    out = dict(src)
    out["fil_rouge"] = (
        "Dans la cuisine embuée, Nina veut le parc tout de suite. Un grain de sel "
        "colle à la vitre, puis glisse sur le bouton de bois du sac de toile prune. "
        "Première tentative : elle tire trop vite, le sac accroche la chaise, sourire "
        "parti. Le sac part avec elle. Bac, toboggan ou balançoires changent l'obstacle. "
        "Ballon, seau ou doudou changent la ruse : Nina refuse de foncer, écoute, "
        "retrouve le grain. Gourde, goûter ou casquette ferment le sac. Ça a failli. "
        "Au retour, le grain garde la buée."
    )
    out["title"] = TITLE
    out["characters"] = "Nina, papa, maman"
    out["setting"] = "cuisine embuée, sac sur la chaise, puis le parc"
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
        "# TREE-AUT-015 — Le sac près de la buée\n\n"
        "- **Nouveau titre :** *Le sac près de la buée*\n"
        "- **Public :** 5–6 ans (N3), lecture interactive familiale\n"
        "- **Leçon principale :** AUT.AFF.001 — mettre les affaires dans le sac "
        "(vécue, non dite)\n"
        "- **Personnages :** Nina, papa, maman\n"
        "- **Structure conservée :** 86 nœuds, trois choix à trois options, "
        "27 chemins et 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Dans la cuisine embuée, Nina veut le parc tout de suite. Un grain de sel "
        "colle à la vitre, puis glisse sur le bouton de bois du sac de toile prune. "
        "Elle tire trop vite : le sac accroche la chaise, sourire parti. Papa "
        "s'accroupit. Le sac part avec elle. La crique du bac, la rampe tiède ou le "
        "pré des chaînes changent l'obstacle ; ballon, seau ou doudou changent la "
        "ruse ; gourde, goûter ou casquette ferment le sac. Nina refuse de foncer, "
        "écoute, retrouve le grain du départ. Ça a failli. Au retour, le grain garde "
        "la buée.\n\n"
        "## Améliorations appliquées\n\n"
        "- Ouverture par le cacao, le moineau et le doigt dans la buée, pas le gabarit v2.\n"
        "- Indice unique dès le début : grain de sel, payé au climax.\n"
        "- Corps : sourire qui part, poitrine, adulte à la même hauteur.\n"
        "- Première idée échoue. Second imprévu plus rusé ; l'enfant observe.\n"
        "- T1 ne retire pas le sac. T1/T2/T3 changent l'action.\n"
        "- 27 fins textuellement distinctes, dernière image unique.\n"
        "- Un merci vécu (reprendre le sac), pas un refrain. Question d'adulte.\n"
        "- Pas de « encore / déjà / tout doux », pas merle, pas miel, pas apply.\n"
        "- Monde distinct : sac prune (pas bleu, pas jaune), cuisine puis parc "
        "(pas mer, pas laitue).\n\n"
        "## Direction vocale\n\n"
        "TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending) : "
        "rate, pitch, volume, pauses, text_ssml, text_xai_tags, notes d'arc. "
        "slow réservé aux choix, indices et retours.\n\n"
        "## Contrôles\n\n"
        "- 86 chunks\n"
        f"- 27 chemins, {min(lengths)} à {max(lengths)} mots, moyenne {sum(lengths)//len(lengths)}\n"
        "- 27 fins et 27 dernières images distinctes\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés\n"
        "- N3 ≤ 16 mots/phrase. `check()` OK.\n\n"
        "## Relu\n\n"
        "P0000, 3 L1, 9 L2, 27 résolutions, 27 fins. Questions liées à la scène "
        "(sac trop loin). Impatience, découragement, fierté calme.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"OK {SID} chemins {min(lengths)}-{max(lengths)} moy {sum(lengths)//len(lengths)}")


if __name__ == "__main__":
    main()
