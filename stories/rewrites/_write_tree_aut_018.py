#!/usr/bin/env python3
"""TREE-AUT-018 — L'étoile sous la caisse de Nina (F-NAR-019, N3, AUT.RAN.001, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-018"
N3 = LIMITS["N3"]
TITLE = "L'étoile sous la caisse de Nina"
TICS = re.compile(
    r"\b(tout doux|tout calme|encore|déjà|deja|une étape après l'autre)\b",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="croissant jaune",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le_rabat_vide_attend_le_clip; tempo=naturel; sourire=léger; respiration=ample",
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
        emphasis="étoile",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qui_manque_sur_le_sac; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="croissant jaune",
        note="arc=confirmation; intention=relancer; emotion=élan; intensite=1; destinataire=enfant; sous_texte=le_croissant_attend_au_palier; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=elle_cherche_trop_vite_ailleurs; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=amir_cache_le_croissant_sans_le_vouloir; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="étoile-clip",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=le_croissant_rend_la_pince; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="croissant jaune",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_rabat_a_sa_pince_le_croissant_reste; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
    prev = ""
    run = 1
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
        if tok and tok == prev:
            run += 1
            if run >= 4:
                raise SystemExit(f"puces {tok}: {ph}")
        else:
            run = 1
        prev = tok
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
        f"destinataire=enfant; sous_texte=le_rabat_porte_le_clip_et_le_croissant; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


# Ouverture : le rabat vide (manière neuve), puis le lieu, puis l'objet.
# Indice unique : le croissant jaune sur la corde usée.
OPENING = vet(
    [
        "narrateur|Le rabat du sac s'ouvre, vide, contre le mur.",
        "narrateur|Il manque un petit bois, sur le tissu.",
        "narrateur|L'entrée sent la pierre mouillée.",
        "narrateur|La gouttière fait tic, tic, sur le paillasson rayé.",
        "narrateur|Près des chaussures, une caisse en bois attend.",
        "narrateur|Sa corde usée porte un croissant jaune, minuscule.",
        "narrateur|Amir, du troisième, a descendu son camion rouge.",
        "enfant-f|Mon étoile-clip va sur le sac, maintenant !",
        "enfant-m|Moi, je veux les cubes, ici !",
        "papa|Vous ne voulez pas la même chose ?",
        "narrateur|En ce moment, Nina bascule la caisse, trop vite.",
        "narrateur|Cubes, livre, tasse : tout tombe près des bottes.",
        "enfant-f|Elle a disparu !",
        "narrateur|Le sourire de Nina disparaît.",
        "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
        "papa|Merci d'avoir dit le clip, pas le camion.",
        "narrateur|Papa s'accroupit, à la même hauteur.",
        "maman|Le croissant jaune, il est resté sur la corde.",
        "enfant-f|Je la veux, pour le pigeon !",
        "narrateur|Elle fouille sous le sac, sans rien.",
        "narrateur|Amir pousse le camion contre une botte, toc.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|L'étoile-clip n'est pas sous le sac.",
        "narrateur|La cuisine, le jardin, ou la chambre.",
        "maman|Tu cherches où, d'abord, Nina ?",
    ]
)

T1 = {
    1: dict(
        lab="la cuisine",
        ans="étoile",
        acc="étoile | l'étoile | étoile-clip | la pince | sous le tas | dans la caisse",
        retry="Elle manque sur le sac. Qu'est-ce que Nina cherche ?",
        ok="Oui, c'est l'étoile.",
        sons="casserole,miette",
        emp="miette",
        passage=vet(
            [
                "narrateur|Nina pousse la porte de la cuisine, trop pressée.",
                "narrateur|Les carreaux sont tièdes, et ça sent le pain grillé.",
                "narrateur|Une miette brille sur la table, ronde, presque jaune.",
                "enfant-f|Elle était près du bol !",
                "narrateur|Elle soulève le torchon rayé, d'un coup.",
                "narrateur|Pas de bois clair, pas de pince.",
                "papa|Sous l'assiette, tu veux regarder ?",
                "narrateur|Nina souffle, sans sourire, les joues chaudes.",
                "enfant-m|Les cubes, sur les carreaux, Nina !",
                "enfant-f|Non, le sac d'abord !",
                "narrateur|Amir aligne trois cubes, et la tour penche.",
                "maman|Le croissant jaune, il est resté au palier ?",
                "enfant-f|Elle est perdue.",
                "narrateur|La casserole fait un petit tic, comme dehors.",
            ]
        ),
        question=vet(
            [
                "narrateur|Nina veut la pince jaune, sur le sac.",
                "maman|Qu'est-ce qui manque, pour le sac ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|La miette brille, comme le croissant de la corde.",
                "enfant-f|Je reviens au palier.",
                "papa|Un objet dans la caisse, puis on voit dessous.",
                "maman|Amir, ton camion peut attendre une minute ?",
                "enfant-m|D'accord, une minute.",
                "narrateur|Le torchon rayé retombe, sans bois clair.",
            ]
        ),
    ),
    2: dict(
        lab="le jardin",
        ans="étoile",
        acc="étoile | l'étoile | étoile-clip | la pince | sous les bottes | au paillasson",
        retry="Près des bottes, quelque chose manque. Qu'est-ce que Nina cherche ?",
        ok="Oui, c'est l'étoile.",
        sons="gouttiere,bottes",
        emp="bottes",
        passage=vet(
            [
                "narrateur|Nina court vers le petit jardin de l'immeuble.",
                "narrateur|L'herbe est mouillée, et l'air pique le nez.",
                "narrateur|Les bottes font ploc, sur le paillasson du bas.",
                "enfant-f|Elle aimait le rebord, parfois !",
                "papa|Tes bottes sont restées au palier, non ?",
                "narrateur|Nina cherche près d'une feuille collée au seau.",
                "narrateur|Une feuille seulement, toute mouillée, sans pince.",
                "enfant-m|Mon camion roule ici, sur l'herbe !",
                "enfant-f|L'étoile d'abord, Amir !",
                "narrateur|Le camion rouge s'enfonce, et Nina a les mains froides.",
                "maman|Le croissant jaune, il est resté près des chaussures ?",
                "enfant-f|Je ne la vois plus.",
                "narrateur|La gouttière chante au-dessus, tic, tic.",
            ]
        ),
        question=vet(
            [
                "narrateur|Près des bottes, le bois clair manque.",
                "papa|Qu'est-ce que Nina cherche, pour le sac ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Une goutte d'herbe brille, trop verte pour le croissant.",
                "enfant-f|On rentre au palier des lacets.",
                "papa|Les bottes, puis la caisse.",
                "maman|Amir, le camion peut sécher une minute ?",
                "enfant-m|Il fait ploc, d'accord.",
                "narrateur|La feuille reste collée au seau, sans étoile.",
            ]
        ),
    ),
    3: dict(
        lab="la chambre",
        ans="étoile",
        acc="étoile | l'étoile | étoile-clip | la pince | sous le tas | près de l'oreiller",
        retry="Près de l'oreiller, le bois clair manque. Qu'est-ce que Nina cherche ?",
        ok="Oui, c'est l'étoile.",
        sons="rideau,tapis",
        emp="oreiller",
        passage=vet(
            [
                "narrateur|Nina revient vers la chambre, le souffle court.",
                "narrateur|Le drap est un peu chaud, et le rideau jaune bouge.",
                "enfant-f|Elle dormait près de l'oreiller !",
                "maman|L'étoile-clip, tu veux dire ?",
                "narrateur|Nina soulève un coin du drap, trop vite.",
                "narrateur|Les chaussons font un tas, sans bois clair.",
                "papa|Tu as regardé sous le livre, là-bas ?",
                "enfant-f|Le tas cache le tapis, pas elle.",
                "enfant-m|Je joue sur le lit, avec les cubes !",
                "enfant-f|Non, le sac m'attend !",
                "narrateur|Nina lisse un pli, sans sourire.",
                "maman|Le croissant jaune est resté au palier des lacets.",
                "narrateur|Le rideau touche ses épaules, léger, un peu savon.",
            ]
        ),
        question=vet(
            [
                "narrateur|Près de l'oreiller, la pince jaune manque.",
                "maman|Qu'est-ce qui doit voyager, sur le sac ?",
            ]
        ),
        confirm=vet(
            [
                "narrateur|Le rideau jaune a la couleur du croissant, pas sa forme.",
                "enfant-f|Je redescends, au palier.",
                "papa|Les chaussons, puis on voit dessous.",
                "maman|Amir, le lit peut attendre une minute ?",
                "enfant-m|Une minute, d'accord.",
                "narrateur|Le pli du drap retombe, sans clic.",
            ]
        ),
    ),
}

T2_CHOICE = {
    1: vet(
        [
            "narrateur|Au palier, la miette a voyagé, collée à un jouet.",
            "narrateur|Les cubes, le livre, ou la dînette.",
            "papa|Quel jouet tu poses, pour voir dessous ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Au palier, une goutte d'herbe brille sur le tas.",
            "narrateur|Les cubes, le livre, ou la dînette.",
            "maman|Quel jouet tu poses, pour voir dessous ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Au palier, le savon du rideau reste dans l'air.",
            "narrateur|Les cubes, le livre, ou la dînette.",
            "papa|Quel jouet tu poses, pour voir dessous ?",
        ]
    ),
}


def t2_scene(a: int, b: int) -> list[str]:
    hip = {
        1: "Au palier, la miette a voyagé, collée au bois.",
        2: "Au palier, l'herbe mouillée a suivi les bottes.",
        3: "Au palier, le savon du rideau reste dans l'air.",
    }[a]
    bodies = {
        (1, 1): [
            f"narrateur|{hip}",
            "narrateur|Amir bâtit une tour, trop haute, sur les lacets.",
            "enfant-m|Ma tour, maintenant !",
            "enfant-f|Le cube va dans la caisse !",
            "narrateur|Nina tend la main, puis la retire.",
            "enfant-f|Pas trop vite, je regarde.",
            "narrateur|La tour s'écroule, toc, contre la corde usée.",
            "narrateur|Un cube rouge cache le croissant, tout contre le bois.",
            "papa|Qu'est-ce que la corde a gardé ?",
            "narrateur|Le palier se tait, sauf le tic de la gouttière.",
            "narrateur|Nina écoute, puis penche la tête.",
            "enfant-f|Le croissant jaune, sous le cube !",
            "enfant-m|Je charge, alors.",
        ],
        (1, 2): [
            f"narrateur|{hip}",
            "narrateur|Amir pose le livre en rampe, pour le camion.",
            "enfant-m|Il descend, le rouge !",
            "enfant-f|Le livre, dans la caisse !",
            "narrateur|Le camion dévale, et le livre glisse sous une botte.",
            "narrateur|Nina veut tirer, puis s'arrête.",
            "enfant-f|Je ne fonce pas.",
            "papa|Qu'est-ce que la page a pris ?",
            "narrateur|Les voix s'arrêtent, et Nina écoute le tic, dehors.",
            "narrateur|Nina écoute, puis soulève le bord, très lent.",
            "narrateur|Le croissant jaune luit, collé à une page.",
            "enfant-f|Il a voyagé, le jaune.",
            "enfant-m|Le camion attend, sur le paillasson.",
        ],
        (1, 3): [
            f"narrateur|{hip}",
            "narrateur|Amir installe la dînette, tasse contre tasse.",
            "enfant-m|Du thé, tout de suite !",
            "enfant-f|La tasse, dans la caisse !",
            "narrateur|La tasse blanche roule, et sonne, tout creux.",
            "narrateur|Elle s'arrête comme un couvercle, sur la corde usée.",
            "narrateur|Nina lève la main, puis la laisse.",
            "enfant-f|Je regarde, d'abord.",
            "maman|Le fond de la tasse, c'est quoi ?",
            "narrateur|Autour d'eux, seulement le tic de la gouttière.",
            "narrateur|Nina penche la tasse, et le croissant jaune est là.",
            "enfant-f|Elle a couvert le jaune !",
            "enfant-m|Le camion peut être le plateau.",
        ],
        (2, 1): [
            f"narrateur|{hip}",
            "narrateur|Amir aligne des cubes mouillés, près des bottes.",
            "enfant-m|Un pont, pour le camion !",
            "enfant-f|Les cubes, dans la caisse !",
            "narrateur|Nina prend un cube, trop humide, et il glisse.",
            "narrateur|Le pont s'ouvre, et un cube tombe sous la botte.",
            "narrateur|Nina recule d'un pas, sans tirer.",
            "enfant-f|Je ne fonce pas, cette fois.",
            "papa|La goutte d'herbe, elle ressemble à quoi ?",
            "narrateur|Le tic de dehors répond, pas les adultes.",
            "narrateur|Nina se penche, et le croissant jaune brille, collé.",
            "enfant-f|Sous la botte, le jaune !",
            "enfant-m|Je pousse, tout droit.",
        ],
        (2, 2): [
            f"narrateur|{hip}",
            "narrateur|Amir ouvre le livre, une vraie feuille dedans.",
            "enfant-m|C'est un jardin, dans les pages !",
            "enfant-f|Le livre, dans la caisse !",
            "narrateur|Le vent du palier tourne une page, trop vite.",
            "narrateur|La feuille d'herbe s'envole, et le livre claque.",
            "narrateur|Nina pose les deux mains à plat, sans arracher.",
            "enfant-f|Pas trop vite.",
            "maman|La feuille a quelle couleur, près du bois ?",
            "narrateur|Le palier n'a que le tic, pour toute réponse.",
            "narrateur|Nina écarte les pages, et le croissant jaune luit.",
            "enfant-f|Entre deux feuilles, le jaune !",
            "enfant-m|Le camion garde la feuille, alors.",
        ],
        (2, 3): [
            f"narrateur|{hip}",
            "narrateur|Amir verse de la rosée dans une petite assiette.",
            "enfant-m|De l'eau du jardin, pour le thé !",
            "enfant-f|L'assiette, dans la caisse !",
            "narrateur|L'assiette penche, et la rosée file sous la botte.",
            "narrateur|Nina veut essuyer, puis s'arrête.",
            "enfant-f|Je regarde l'eau, d'abord.",
            "papa|Le rond d'eau, il montre quoi ?",
            "narrateur|Seul le tic de la gouttière parle, dehors.",
            "narrateur|Nina suit le rond, et le croissant jaune tremble.",
            "enfant-f|L'eau a montré le jaune !",
            "enfant-m|Le camion porte l'assiette, moi je pousse.",
        ],
        (3, 1): [
            f"narrateur|{hip}",
            "narrateur|Amir construit une tour contre l'oreiller oublié.",
            "enfant-m|Elle touche le ciel du palier !",
            "enfant-f|Les cubes, dans la caisse !",
            "narrateur|La tour penche vers le sac, trop haute.",
            "narrateur|Un cube tombe, et roule sous le tas de chaussons.",
            "narrateur|Nina écarte un chausson, puis s'arrête.",
            "enfant-f|Je ne fonce pas.",
            "papa|Le rayon du rideau, il pose où ?",
            "narrateur|Les adultes attendent, et le tic continue dehors.",
            "narrateur|Nina écoute, puis suit le rayon.",
            "enfant-f|Le croissant jaune, sur le bois !",
            "enfant-m|Le camion fait le chantier, d'accord.",
        ],
        (3, 2): [
            f"narrateur|{hip}",
            "narrateur|Amir ouvre le livre sur la couverture pliée.",
            "enfant-m|Une histoire, avant le clic !",
            "enfant-f|Le livre, dans la caisse !",
            "narrateur|Le rideau jaune colore une page, trop fort.",
            "narrateur|Nina veut fermer, puis laisse le livre ouvert.",
            "enfant-f|Pas trop vite, je regarde la page.",
            "maman|Cette couleur, c'est le rideau, ou le croissant ?",
            "narrateur|Le tic de la gouttière est la seule voix.",
            "narrateur|Nina tire le livre, très lent, vers elle.",
            "narrateur|Un coin de bois clair attend, collé à une page.",
            "enfant-f|Le croissant jaune, sous le papier !",
            "enfant-m|Je tiens la couverture, toi le livre.",
        ],
        (3, 3): [
            f"narrateur|{hip}",
            "narrateur|Amir sert le thé près des chaussons en tas.",
            "enfant-m|La dînette, au pied du lit d'en haut !",
            "enfant-f|Les tasses, dans la caisse !",
            "narrateur|Une petite assiette reflète la veilleuse du palier.",
            "narrateur|Nina la prend, trop vite, et elle sonne contre le mur.",
            "narrateur|Elle pose la tasse, les épaules basses.",
            "enfant-f|Je ne fonce plus.",
            "papa|Le rond de lumière, c'est quoi ?",
            "narrateur|Le tic dehors est la seule réponse.",
            "narrateur|Nina écoute, puis penche l'assiette.",
            "enfant-f|Le croissant jaune, au fond du bois !",
            "enfant-m|Le camion est le plateau, moi le serveur.",
        ],
    }
    return vet(bodies[(a, b)])


T3_CHOICE = {
    1: vet(
        [
            "narrateur|Les cubes attendent, et la corde usée aussi.",
            "narrateur|Le matin, après la sieste, ou le soir.",
            "maman|On y va à quelle heure, Nina ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Le livre attend, et la corde usée aussi.",
            "narrateur|Le matin, après la sieste, ou le soir.",
            "papa|On y va à quelle heure, Nina ?",
        ]
    ),
    3: vet(
        [
            "narrateur|La dînette attend, et la corde usée aussi.",
            "narrateur|Le matin, après la sieste, ou le soir.",
            "maman|On y va à quelle heure, Nina ?",
        ]
    ),
}


RES = {
    (1, 1, 1): vet(
        [
            "enfant-f|Le matin, le sac attend, trop lourd !",
            "narrateur|La lumière est pâle, un peu bleue, sur les lacets.",
            "narrateur|Nina prend un cube à deux mains, lisse.",
            "enfant-m|C'est pour ma tour !",
            "enfant-f|Le camion le porte, jusqu'à la caisse.",
            "narrateur|Amir pousse le rouge, et le cube tombe, toc.",
            "narrateur|La bretelle du sac accroche la corde usée.",
            "narrateur|La caisse penche, et le croissant jaune apparaît.",
            "enfant-f|Mon étoile-clip !",
            "narrateur|Elle pince le bois clair sur le sac, clic.",
            "papa|Tu l'as vue, sous le cube.",
            "maman|Le pigeon peut la regarder, en bas.",
            "narrateur|Une miette colle au croissant, puis s'en va.",
        ]
    ),
    (1, 1, 2): vet(
        [
            "enfant-f|Après la sieste, les joues sont chaudes !",
            "narrateur|La lumière est ronde, un peu chaude, sur le palier.",
            "narrateur|Nina pose un cube, sans courir, dans la caisse.",
            "enfant-m|Ma tour, plus tard !",
            "narrateur|Le paillasson rayé colle au bois, trop tiède.",
            "narrateur|Amir pousse le camion, et un cube se décolle.",
            "narrateur|Sous sa place, le croissant jaune attend, collé.",
            "enfant-f|Elle était collée, comme la miette !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|Tu as attendu, et le cube a parlé.",
            "maman|La cour peut attendre, une minute.",
            "narrateur|Le cube est tiède, comme les joues de Nina.",
        ]
    ),
    (1, 1, 3): vet(
        [
            "enfant-f|Le soir, on descend pour le pain !",
            "narrateur|Les lampes du palier sont petites et jaunes.",
            "narrateur|Nina glisse un cube, et l'ombre danse sous la lampe.",
            "enfant-m|L'ombre, c'est ma tour !",
            "narrateur|La lampe dore un cube, trop fort, trop jaune.",
            "narrateur|Amir recule le camion, et le cube laisse un trou.",
            "narrateur|Le croissant jaune brille, vrai, sous le trou.",
            "enfant-f|C'était elle, pas la lampe !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|La lampe a menti, pas le croissant.",
            "maman|Le pain sent bon, en bas.",
            "narrateur|L'ombre d'un cube touche le camion rouge.",
        ]
    ),
    (1, 2, 1): vet(
        [
            "enfant-f|Le matin, le livre rentre, puis l'école !",
            "narrateur|La lumière pâle pose sur la couverture jaune.",
            "narrateur|Nina soulève le livre aux pages froides, trop vite.",
            "narrateur|La bretelle du sac pousse le livre, sous la botte.",
            "enfant-m|Ma rampe !",
            "enfant-f|Après, Amir, après le clic.",
            "narrateur|Amir tient le camion, et Nina tire le livre, à plat.",
            "narrateur|Sous le livre, le croissant jaune attend, une miette au bord.",
            "enfant-f|Mon étoile-clip !",
            "narrateur|Elle pince le bois sur le sac, clic.",
            "papa|La page a rendu ce qu'elle cachait.",
            "maman|Le pigeon attend, sur le rebord.",
            "narrateur|Une miette reste au bord d'une page, dans la caisse.",
        ]
    ),
    (1, 2, 2): vet(
        [
            "enfant-f|Après la sieste, le livre sent le pain !",
            "narrateur|La lumière chaude dore la couverture, près du sac.",
            "narrateur|Nina ouvre une page, puis l'autre, sans claquer.",
            "enfant-m|Je vois une étoile dessinée !",
            "papa|Oui, tu as bien regardé.",
            "maman|Ce n'est pas la vraie, hein ?",
            "enfant-f|La vraie est en bois, avec la pince.",
            "narrateur|Amir pose le camion, pour tenir le livre ouvert.",
            "narrateur|Sous une page tiède, le croissant jaune apparaît.",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|Le pain a parlé, et le bois aussi.",
            "narrateur|Le livre est tiède, près d'une odeur d'assiette, loin.",
        ]
    ),
    (1, 2, 3): vet(
        [
            "enfant-f|Le soir, la lampe dore les pages !",
            "narrateur|Les lampes jaunes touchent le bord d'une page.",
            "narrateur|Nina glisse le livre, tout droit, vers la caisse.",
            "enfant-m|Ma rampe, pour le pain !",
            "narrateur|Le camion monte sur la couverture, trop lourd.",
            "narrateur|Nina l'arrête, et le livre rentre, sans bruit.",
            "narrateur|La lampe dore la cordelette rouge, puis le croissant.",
            "enfant-f|Elle était là, sous la page !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|La lampe a lu le fond, avant nous.",
            "maman|Le pain nous attend, en bas de l'escalier.",
            "narrateur|Une page garde un rond de lampe, dans la caisse.",
        ]
    ),
    (1, 3, 1): vet(
        [
            "enfant-f|Le matin, la tasse rentre, puis le sac !",
            "narrateur|La lumière pâle fait un rond, au fond d'une tasse.",
            "narrateur|Nina écarte une petite tasse, blanche, un peu froide.",
            "enfant-m|Du thé, pour l'école !",
            "enfant-f|Le camion est le plateau, pas la table.",
            "narrateur|Amir porte la tasse, trop pressé, et elle sonne.",
            "narrateur|La bretelle accroche l'anse, et la tasse penche.",
            "narrateur|Au fond, le croissant jaune brille, une miette collée.",
            "enfant-f|Mon étoile-clip !",
            "narrateur|Elle pince le bois sur le sac, clic.",
            "papa|La tasse a servi de couvercle, pas de bol.",
            "maman|Le pigeon a entendu le toc.",
            "narrateur|Une petite tasse a une miette au fond, rangée.",
        ]
    ),
    (1, 3, 2): vet(
        [
            "enfant-f|Après la sieste, on sert la caisse !",
            "narrateur|La lumière chaude pose sur la dînette, près des lacets.",
            "narrateur|Nina pose la tasse près du vrai bol, trop loin.",
            "enfant-m|Une gorgée, d'abord ?",
            "papa|D'abord la tasse, ensuite on verse, dans la caisse.",
            "narrateur|Amir pousse le plateau-camion, lent, vers le bois.",
            "narrateur|La dînette rentre, et le paillasson lâche un rond tiède.",
            "narrateur|Le croissant jaune apparaît, collé à une soucoupe.",
            "enfant-f|Elle faisait semblant de dormir !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "maman|La caisse a eu son service.",
            "narrateur|La dînette est chaude, comme une casserole lointaine.",
        ]
    ),
    (1, 3, 3): vet(
        [
            "enfant-f|Le soir, la cuillère brille, sous la lampe !",
            "narrateur|Les lampes jaunes touchent une petite cuillère.",
            "narrateur|Nina pose la cuillère, et elle sonne, tout creux.",
            "enfant-m|C'est l'heure du pain-thé !",
            "narrateur|Amir recule le camion, pour laisser la lampe.",
            "narrateur|La lampe dore le fond d'une assiette, trop jaune.",
            "narrateur|Nina soulève l'assiette, et le croissant apparaît.",
            "enfant-f|Le jaune, c'était elle !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|La cuillère a montré le chemin, sans parler.",
            "maman|Le pain sent le palier, un peu.",
            "narrateur|La petite cuillère brille sous la lampe du palier.",
        ]
    ),
    (2, 1, 1): vet(
        [
            "enfant-f|Le matin, un cube a une goutte d'herbe !",
            "narrateur|La lumière pâle pose sur un cube mouillé, près des bottes.",
            "narrateur|Nina prend le cube à deux mains, trop glissant.",
            "enfant-m|Mon pont, pour l'école !",
            "enfant-f|Le camion le porte, au sec.",
            "narrateur|Amir pousse, et la bretelle du sac tape une botte.",
            "narrateur|La botte penche, et le croissant jaune luit, rond.",
            "enfant-f|Mon étoile-clip !",
            "narrateur|Elle essuie le bois, puis pince le sac, clic.",
            "papa|La goutte d'herbe a parlé, comme au seau.",
            "maman|Le pigeon secoue une aile, plus sèche.",
            "narrateur|Un cube porte une goutte d'herbe, ronde, vers l'école.",
        ]
    ),
    (2, 1, 2): vet(
        [
            "enfant-f|Après la sieste, le cube sèche au soleil !",
            "narrateur|La lumière chaude sèche un cube, un peu vert.",
            "narrateur|Nina pose le cube dans la caisse, sans le jeter.",
            "enfant-m|Il était à moi, le vert !",
            "enfant-f|Il rentre, et toi tu pousses.",
            "narrateur|Amir pousse le camion, et le paillasson lâche le cube.",
            "narrateur|Sous sa place, le croissant jaune attend, une herbe collée.",
            "enfant-f|Elle séchait, avec lui !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|Tu as laissé le soleil travailler.",
            "maman|La cour est verte, comme le cube.",
            "narrateur|Le cube sèche au soleil, un peu vert, dans la caisse.",
        ]
    ),
    (2, 1, 3): vet(
        [
            "enfant-f|Le soir, un cube garde une goutte, près des bottes !",
            "narrateur|Les lampes jaunes touchent une goutte, sur un cube.",
            "narrateur|Nina soulève le cube, et la goutte tremble.",
            "enfant-m|Ne la casse pas !",
            "narrateur|Amir recule le camion, pour ne pas éclabousser.",
            "narrateur|La goutte tombe, et le croissant jaune apparaît, mouillé.",
            "enfant-f|Elle buvait, la petite !",
            "narrateur|Nina essuie, puis pince le sac, clic.",
            "papa|La botte a gardé l'eau, toi le clip.",
            "maman|Le pain nous attend, sans goutte.",
            "narrateur|Un cube garde une goutte, près des bottes, rangé.",
        ]
    ),
    (2, 2, 1): vet(
        [
            "enfant-f|Le matin, une vraie feuille sert de marque-page !",
            "narrateur|La lumière pâle pose sur une feuille, dans le livre.",
            "narrateur|Nina ouvre, trop vite, et la feuille d'herbe s'envole.",
            "enfant-m|Attrape-la !",
            "narrateur|Amir pose le camion dessus, comme un poids.",
            "narrateur|La bretelle du sac pousse le livre, et le fond se voit.",
            "narrateur|Sous le livre, le croissant jaune attend, une nervure collée.",
            "enfant-f|Mon étoile-clip !",
            "narrateur|Elle pince le bois sur le sac, clic.",
            "papa|La feuille a marqué la page, et le fond.",
            "maman|Le pigeon a vu la nervure, lui aussi.",
            "narrateur|Une vraie feuille sert de marque-page, dans la caisse.",
        ]
    ),
    (2, 2, 2): vet(
        [
            "enfant-f|Après la sieste, le livre sent l'herbe mouillée !",
            "narrateur|La lumière chaude sèche une page, un peu verte.",
            "narrateur|Nina referme le livre, sans claquer, vers la caisse.",
            "enfant-m|Il sent le jardin !",
            "enfant-f|Il rentre, et l'étoile aussi.",
            "narrateur|Amir tient la couverture, et Nina glisse le livre, à plat.",
            "narrateur|Le paillasson lâche une page, et le croissant jaune luit.",
            "enfant-f|Elle sentait l'herbe, elle aussi !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|Deux odeurs, et un seul clic.",
            "maman|La cour sent pareil, en bas.",
            "narrateur|Le livre sent l'herbe mouillée, contre le sac.",
        ]
    ),
    (2, 2, 3): vet(
        [
            "enfant-f|Le soir, le pigeon se tait, près du livre !",
            "narrateur|Les lampes jaunes touchent le rebord, et le livre.",
            "narrateur|Nina pose le livre, et le pigeon rentre l'aile.",
            "enfant-m|Il écoute l'histoire ?",
            "narrateur|Amir arrête le camion, pour ne pas faire toc.",
            "narrateur|La lampe dore une page, puis la corde usée.",
            "narrateur|Sous le livre, le croissant jaune apparaît, sans bruit.",
            "enfant-f|Chut, je la prends !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic, tout bas.",
            "papa|Le pigeon a fini, toi aussi.",
            "maman|Le pain peut parler, maintenant.",
            "narrateur|Le pigeon se tait près du livre, sur le rebord.",
        ]
    ),
    (2, 3, 1): vet(
        [
            "enfant-f|Le matin, une petite assiette a de la rosée !",
            "narrateur|La lumière pâle tremble dans l'assiette, près des bottes.",
            "narrateur|Nina penche l'assiette, trop vite, et la rosée file.",
            "enfant-m|Mon thé du jardin !",
            "enfant-f|Le camion porte, sans verser.",
            "narrateur|Amir pousse, et la bretelle accroche l'anse.",
            "narrateur|L'assiette penche, et le croissant apparaît, mouillé.",
            "enfant-f|Mon étoile-clip !",
            "narrateur|Elle essuie, puis pince le sac, clic.",
            "papa|La rosée a montré le fond.",
            "maman|Le pigeon a bu, lui, dehors.",
            "narrateur|Une petite assiette a de la rosée, minuscule, rangée.",
        ]
    ),
    (2, 3, 2): vet(
        [
            "enfant-f|Après la sieste, la dînette est tiède, au soleil !",
            "narrateur|La lumière chaude pose sur une tasse, près du jardin.",
            "narrateur|Nina pose la tasse dans la caisse, sans la faire sonner.",
            "enfant-m|Elle a chaud, comme moi !",
            "narrateur|Amir pousse le plateau-camion, lent, vers le bois.",
            "narrateur|Le paillasson lâche la soucoupe, et le croissant jaune luit.",
            "enfant-f|Elle se chauffait, la petite !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|Tu as posé, sans verser.",
            "maman|La cour est tiède, elle aussi.",
            "narrateur|La dînette est tiède, au soleil du jardin, dans la caisse.",
        ]
    ),
    (2, 3, 3): vet(
        [
            "enfant-f|Le soir, une goutte tombe, loin de la tasse !",
            "narrateur|Les lampes jaunes, et la gouttière fait tic, au-dessus.",
            "narrateur|Nina pose la tasse, et une goutte part vers le rebord.",
            "enfant-m|Ce n'est pas mon thé !",
            "narrateur|Amir recule le camion, pour laisser la goutte.",
            "narrateur|La goutte touche la corde usée, et le croissant brille.",
            "enfant-f|Le tic, c'était elle !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|La gouttière a parlé, depuis le départ.",
            "maman|Le pain est tout près, en bas.",
            "narrateur|Loin de la tasse, une goutte tombe de la gouttière.",
        ]
    ),
    (3, 1, 1): vet(
        [
            "enfant-f|Le matin, un rayon pose sur la tour de cubes !",
            "narrateur|La lumière pâle passe le rideau, jusqu'au palier.",
            "narrateur|Nina démonte un cube, puis un autre, sans courir.",
            "enfant-m|Ma tour de l'école !",
            "enfant-f|Le camion fait le chantier, cube après cube.",
            "narrateur|Amir pousse, et la bretelle du sac tape la tour.",
            "narrateur|La tour penche, et un rayon montre le croissant jaune.",
            "enfant-f|Mon étoile-clip !",
            "narrateur|Elle pince le bois sur le sac, clic.",
            "papa|Le rayon a travaillé, toi aussi.",
            "maman|Le pigeon a le même rayon, dehors.",
            "narrateur|Un rayon pose sur la tour de cubes, puis s'en va.",
        ]
    ),
    (3, 1, 2): vet(
        [
            "enfant-f|Après la sieste, un cube est contre l'oreiller !",
            "narrateur|La lumière chaude a suivi l'oreiller, jusqu'au palier.",
            "narrateur|Nina prend le cube, un peu tiède, comme le drap.",
            "enfant-m|Il a dormi, lui aussi !",
            "enfant-f|Il rentre, et l'étoile aussi.",
            "narrateur|Amir pousse le camion, et le cube quitte l'oreiller.",
            "narrateur|Sous sa place, le croissant jaune attend, une chaleur dedans.",
            "enfant-f|Elle avait chaud, comme moi !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|Tu as levé le cube, pas le drap.",
            "maman|La cour peut attendre, tes joues aussi.",
            "narrateur|Un cube a gardé la chaleur de l'oreiller, dans la caisse.",
        ]
    ),
    (3, 1, 3): vet(
        [
            "enfant-f|Le soir, l'ombre des cubes danse sur le mur !",
            "narrateur|Les lampes jaunes font danser les cubes, sur le palier.",
            "narrateur|Nina glisse un cube, et l'ombre recule.",
            "enfant-m|Une danse de plus !",
            "narrateur|Amir arrête le camion, pour regarder l'ombre.",
            "narrateur|L'ombre s'en va, et le croissant jaune reste, vrai.",
            "enfant-f|L'ombre mentait, elle non !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|Tu as suivi l'ombre, jusqu'au bois.",
            "maman|Le pain n'a pas d'ombre, en bas.",
            "narrateur|L'ombre des cubes danse, puis s'endort sur le mur.",
        ]
    ),
    (3, 2, 1): vet(
        [
            "enfant-f|Le matin, le rideau jaune colore la page !",
            "narrateur|La lumière pâle passe le rideau, sur le livre.",
            "narrateur|Nina ouvre une page, trop vite, et le jaune s'étale.",
            "enfant-m|C'est une étoile, sur le papier !",
            "enfant-f|La vraie, sous le livre.",
            "narrateur|Amir tient la couverture, et la bretelle pousse le livre.",
            "narrateur|Sous la page colorée, le croissant jaune attend, savon et tout.",
            "enfant-f|Mon étoile-clip !",
            "narrateur|Elle pince le bois sur le sac, clic.",
            "papa|Le rideau a prêté sa couleur, une seconde.",
            "maman|Le pigeon a le même jaune, sur l'aile.",
            "narrateur|Le rideau jaune a coloré une page, près du sac.",
        ]
    ),
    (3, 2, 2): vet(
        [
            "enfant-f|Après la sieste, le livre est ouvert sur la couverture !",
            "narrateur|La lumière chaude pose sur le livre, et sur le drap plié.",
            "narrateur|Nina referme, sans claquer, vers la caisse.",
            "enfant-m|Il sent le savon !",
            "enfant-f|Il rentre, page contre page.",
            "narrateur|Amir pose le camion, pour tenir le livre à plat.",
            "narrateur|Le paillasson lâche un coin, et le croissant jaune luit.",
            "enfant-f|Elle sentait le savon, elle aussi !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|Deux chaleurs, et un seul clic.",
            "maman|La cour n'a pas de savon, elle.",
            "narrateur|Le livre sent le savon, et le capuchon du sac aussi.",
        ]
    ),
    (3, 2, 3): vet(
        [
            "enfant-f|Le soir, la page sent le savon, un peu !",
            "narrateur|Les lampes jaunes touchent une page, près de la corde.",
            "narrateur|Nina glisse le livre, et la page reflète la veilleuse.",
            "enfant-m|Une étoile, dans le papier !",
            "narrateur|Amir arrête le camion, pour ne pas cacher la lampe.",
            "narrateur|La veilleuse dore la corde usée, puis le croissant.",
            "enfant-f|Le jaune de la lampe, c'était elle !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|La page a gardé le savon, et le fond.",
            "maman|Le pain n'a pas de savon, heureusement.",
            "narrateur|Une page reflète la veilleuse, collée à la corde usée.",
        ]
    ),
    (3, 3, 1): vet(
        [
            "enfant-f|Le matin, une tasse miniature est près du lit !",
            "narrateur|La lumière pâle pose sur une tasse, oubliée au palier.",
            "narrateur|Nina la prend, trop vite, et elle sonne contre le sac.",
            "enfant-m|Elle a voyagé, du lit !",
            "enfant-f|Le camion la ramène, à la caisse.",
            "narrateur|Amir pousse, et la bretelle accroche l'anse, toc.",
            "narrateur|La tasse penche, et le croissant apparaît, au fond.",
            "enfant-f|Mon étoile-clip !",
            "narrateur|Elle pince le bois sur le sac, clic.",
            "papa|La tasse a fait le voyage, toi le clic.",
            "maman|Le pigeon n'a pas de tasse, lui.",
            "narrateur|La tasse miniature a vu le lit, puis le palier.",
        ]
    ),
    (3, 3, 2): vet(
        [
            "enfant-f|Après la sieste, la dînette attend au pied du lit !",
            "narrateur|La lumière chaude a suivi la dînette, jusqu'aux lacets.",
            "narrateur|Nina pose une tasse, sans la faire sonner, dans la caisse.",
            "enfant-m|Le camion est le plateau, je sers !",
            "enfant-f|Tu sers la caisse, d'accord.",
            "narrateur|Amir pousse, lent, et le paillasson lâche une soucoupe.",
            "narrateur|Sous la soucoupe, le croissant jaune attend, un peu chaud.",
            "enfant-f|Elle faisait la sieste, elle aussi !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|Tu as servi, sans casser.",
            "maman|La cour n'a pas de tasse, tant mieux.",
            "narrateur|L'oreille du camion rouge touche la dînette, au chaud.",
        ]
    ),
    (3, 3, 3): vet(
        [
            "enfant-f|Le soir, une petite assiette reflète la veilleuse !",
            "narrateur|Les lampes jaunes, et l'assiette devient un petit soleil.",
            "narrateur|Nina soulève l'assiette, trop vite, et le rond saute.",
            "enfant-m|Le soleil, il est à moi !",
            "narrateur|Amir recule le camion, pour laisser le rond.",
            "narrateur|Le rond s'en va, et le croissant reste, vrai, sous l'assiette.",
            "enfant-f|Le vrai jaune, c'est elle !",
            "narrateur|Nina pince l'étoile-clip sur le sac, clic.",
            "papa|Le reflet a menti, le bois non.",
            "maman|Le pain a sa propre lumière, en bas.",
            "narrateur|La petite assiette reflète le clip, sous la lampe.",
        ]
    ),
}


def ending(a: int, b: int, c: int) -> list[str]:
    first = {
        1: "Plus tard, une miette crisse sous la porte de la cuisine.",
        2: "Plus tard, une botte sèche, loin, près du jardin.",
        3: "Plus tard, le rideau jaune ne bouge plus, en haut.",
    }[a]
    invite = {
        1: "Tu as entendu le clic, ce matin ?",
        2: "La sieste a-t-elle rendu l'étoile ?",
        3: "Le soir t'a aidée, pour la pince ?",
    }[c]
    recap = {
        (1, 1, 1): "J'ai posé le cube, le camion a poussé, et le croissant a parlé.",
        (1, 1, 2): "J'ai attendu, le paillasson a lâché le cube, et je l'ai vue.",
        (1, 1, 3): "La lampe a doré le cube, et le vrai jaune c'était elle.",
        (1, 2, 1): "Le livre était sous la botte, une miette au bord.",
        (1, 2, 2): "J'ai ouvert, Amir a tenu, et la vraie était en bois.",
        (1, 2, 3): "La lampe a lu le fond, avant nous.",
        (1, 3, 1): "La tasse a couvert le fond, le camion a porté.",
        (1, 3, 2): "On a servi la caisse, et elle faisait semblant.",
        (1, 3, 3): "La cuillère a brillé, et j'ai soulevé l'assiette.",
        (2, 1, 1): "Le cube glissait, la botte a parlé, et je l'ai essuyée.",
        (2, 1, 2): "Le soleil a séché le cube, et elle séchait avec.",
        (2, 1, 3): "La goutte est tombée, et elle buvait dessous.",
        (2, 2, 1): "La feuille d'herbe a marqué la page, et le fond.",
        (2, 2, 2): "Le livre sentait l'herbe, elle aussi.",
        (2, 2, 3): "Le pigeon s'est tu, et j'ai pris le clic, tout bas.",
        (2, 3, 1): "L'assiette a versé la rosée, et le fond s'est montré.",
        (2, 3, 2): "La tasse était tiède, et elle se chauffait dessous.",
        (2, 3, 3): "Le tic de la gouttière, c'était elle, depuis le départ.",
        (3, 1, 1): "Le rayon a montré la tour, puis le croissant.",
        (3, 1, 2): "Le cube avait chaud, comme l'oreiller, et elle aussi.",
        (3, 1, 3): "L'ombre dansait, le bois restait.",
        (3, 2, 1): "Le rideau a coloré la page, la vraie était dessous.",
        (3, 2, 2): "Le livre sentait le savon, et le sac aussi.",
        (3, 2, 3): "La veilleuse a doré la corde, puis le croissant.",
        (3, 3, 1): "La tasse a sonné contre le sac, et le fond s'est ouvert.",
        (3, 3, 2): "Amir a servi, moi j'ai pincé, sans casser.",
        (3, 3, 3): "Le rond de l'assiette mentait, le bois non.",
    }[(a, b, c)]
    mid = {
        1: "Le sac d'école attend, l'étoile-clip sur le rabat, un peu lourd.",
        2: "La cour de l'immeuble est prête, le clip contre le tissu.",
        3: "Une odeur de pain chaud monte, et le clip tient bon.",
    }[c]
    papa_line = {
        (1, 1, 1): "Le cube a voyagé, toi aussi.",
        (1, 1, 2): "Attendre a décollé le bois.",
        (1, 1, 3): "La lampe a travaillé pour vous.",
        (1, 2, 1): "La page a rendu ce qu'elle cachait.",
        (1, 2, 2): "Tu as distingué le dessin, et le bois.",
        (1, 2, 3): "La lampe a lu plus vite que nous.",
        (1, 3, 1): "La tasse a fait un couvercle, malgré elle.",
        (1, 3, 2): "Le service de la caisse était le bon.",
        (1, 3, 3): "La cuillère a montré, sans un mot.",
        (2, 1, 1): "La goutte d'herbe valait une pointe.",
        (2, 1, 2): "Le soleil a fini le geste.",
        (2, 1, 3): "Tu as essuyé, puis tu as pincé.",
        (2, 2, 1): "La nervure a parlé, comme au seau.",
        (2, 2, 2): "Deux odeurs, un seul clic.",
        (2, 2, 3): "Le silence du pigeon t'a aidée.",
        (2, 3, 1): "La rosée a lavé le fond.",
        (2, 3, 2): "Poser sans verser, ça tient.",
        (2, 3, 3): "Le tic du départ a payé.",
        (3, 1, 1): "Le rayon a choisi le bon cube.",
        (3, 1, 2): "La chaleur de l'oreiller était un indice.",
        (3, 1, 3): "L'ombre recule, le bois reste.",
        (3, 2, 1): "Le rideau a prêté sa couleur, une seconde.",
        (3, 2, 2): "Le savon a marqué la page, et le fond.",
        (3, 2, 3): "La veilleuse a lu la corde.",
        (3, 3, 1): "Le toc de l'anse a ouvert le fond.",
        (3, 3, 2): "Servir la caisse, c'était jouer juste.",
        (3, 3, 3): "Le vrai jaune tenait sous l'assiette.",
    }[(a, b, c)]
    last = {
        (1, 1, 1): "Le croissant jaune garde une miette, et le clip fait clic, sur le sac.",
        (1, 1, 2): "Un carré de cube tiède sèche sur le paillasson rayé.",
        (1, 1, 3): "Sous la lampe, l'ombre d'un cube touche le camion rouge.",
        (1, 2, 1): "La corde usée sert de marque-page, dans le livre rangé.",
        (1, 2, 2): "Une page sent le pain, collée au sac d'école.",
        (1, 2, 3): "La lampe dore la cordelette rouge, puis le clip.",
        (1, 3, 1): "La petite tasse a une miette au fond, et le pigeon écoute.",
        (1, 3, 2): "Le camion rouge garde une tasse, comme un chargement.",
        (1, 3, 3): "La cuillère reflète la lampe, près des lacets.",
        (2, 1, 1): "Un cube porte une goutte d'herbe jusqu'au sac.",
        (2, 1, 2): "Le paillasson rayé sèche un cube vert, minuscule.",
        (2, 1, 3): "Une goutte de botte brille sur le bois clair de la caisse.",
        (2, 2, 1): "Une feuille d'herbe marque la page, dans la caisse.",
        (2, 2, 2): "Le livre sent l'herbe, et le sac sent la pierre.",
        (2, 2, 3): "Le pigeon se tait, l'aile contre le livre fermé.",
        (2, 3, 1): "Une rosée tremble dans la petite assiette, puis part.",
        (2, 3, 2): "La dînette est tiède, comme les joues après la sieste.",
        (2, 3, 3): "La gouttière fait tic, loin de la tasse rangée.",
        (3, 1, 1): "Un rayon du rideau pose sur la tour, puis sur le clip.",
        (3, 1, 2): "Un cube a gardé la chaleur de l'oreiller, dans la caisse.",
        (3, 1, 3): "L'ombre des cubes danse, puis s'endort sur le mur.",
        (3, 2, 1): "Le rideau jaune a coloré une page, près du sac.",
        (3, 2, 2): "Le livre sent le savon, et le capuchon du sac aussi.",
        (3, 2, 3): "Une page reflète la veilleuse, collée à la corde usée.",
        (3, 3, 1): "La tasse miniature a vu le lit, puis le palier.",
        (3, 3, 2): "L'oreille du camion rouge touche la dînette, au chaud.",
        (3, 3, 3): "La petite assiette reflète le clip, sous la lampe.",
    }[(a, b, c)]
    keepsake = {
        1: "Dans la caisse, la corde usée pend, plus légère.",
        2: "Sur le paillasson rayé, une goutte sèche, comme au départ.",
        3: "Près des chaussures, le palier des lacets sent la pierre, et le clip.",
    }[a]
    sortie = {
        1: "On descend pour l'école, l'étoile sur le rabat.",
        2: "On descend pour la cour, l'étoile contre le tissu.",
        3: "On descend pour le pain, l'étoile tenue par la pince.",
    }[c]
    amir = {
        1: "Moi, je pousse le camion, à côté.",
        2: "Moi, je garde une place, près du sac.",
        3: "Moi, je descends, le plateau vide.",
    }[b]
    return vet(
        [
            f"narrateur|{first}",
            f"maman|{invite}",
            f"enfant-f|{recap}",
            f"narrateur|{keepsake}",
            f"narrateur|{mid}",
            f"papa|{papa_line}",
            f"enfant-m|{amir}",
            f"narrateur|{sortie}",
            f"narrateur|{last}",
        ]
    )


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple[list[str], str, str, dict]] = {}

    scripts["CHK_T0000_P0000"] = (OPENING, "opening", "gouttiere,pigeon", {"emphasis": "croissant jaune"})
    scripts["CHK_T0001_P0000"] = (
        T1_CHOICE,
        "choice",
        "",
        {
            "option_1_label": "la cuisine",
            "option_2_label": "le jardin",
            "option_3_label": "la chambre",
        },
    )

    t2_labs = ("les cubes", "le livre", "la dînette")
    t3_labs = ("le matin", "après la sieste", "le soir")
    t2_sons = {1: "cubes,bois", 2: "pages,livre", 3: "tasse,toc"}
    t2_emp = {1: "cubes", 2: "livre", 3: "dînette"}
    t3_sons = {1: "sac,pigeon", 2: "cour,paillasson", 3: "lampe,pain"}
    fin_sons = {1: "sac,gouttiere", 2: "paillasson,clip", 3: "lampe,caisse"}

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
        scripts[f"{base}_C0001"] = (t1["confirm"], "confirm", t1["sons"], {"emphasis": "croissant jaune"})
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
                    {"emphasis": "étoile-clip"},
                )
                scripts[f"{leaf3}_F0001"] = (
                    ending(a, b, c),
                    "ending",
                    fin_sons[c],
                    {"emphasis": "croissant jaune", "note": ending_note(a, b, c)},
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
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "amir" not in blob:
        raise SystemExit(f"{SID}: Amir absent")
    if "étoile" not in blob:
        raise SystemExit(f"{SID}: étoile absente")
    if "croissant jaune" not in blob:
        raise SystemExit(f"{SID}: croissant jaune absent")
    for tic in ("tout doux", "tout calme", " aujourd'hui,"):
        if tic in blob:
            raise SystemExit(f"{SID}: tic {tic}")
    if TICS.search(blob):
        raise SystemExit(f"{SID}: tic corpus {TICS.search(blob).group(0)}")
    for bad in ("merle", "couleur de miel", "grand-père", "maîtresse", "jardinier", "bibliothécaire"):
        if bad in blob:
            raise SystemExit(f"{SID}: interdit {bad}")
    for ch in chunks:
        if not ch.get("notes"):
            raise SystemExit(f"{ch['chunk_id']}: notes manquantes")
        if not ch.get("text_ssml") or "<speak>" not in ch["text_ssml"]:
            raise SystemExit(f"{ch['chunk_id']}: ssml manquant")
        if not ch.get("text_xai_tags"):
            raise SystemExit(f"{ch['chunk_id']}: xai manquant")

    out = dict(src)
    out["fil_rouge"] = (
        "Au palier des lacets, le rabat du sac est vide. Nina veut pincer "
        "son étoile-clip (bois clair, pointe jaune, clic) dessus, maintenant, "
        "pour le pigeon. Amir, du troisième, veut jouer avec les jouets tombés. "
        "Elle bascule la caisse trop vite : le tas cache la pince. Un croissant "
        "jaune, collé à la corde usée, reste comme indice. Cuisine, jardin ou "
        "chambre échouent d'abord. Cubes, livre ou dînette changent la ruse "
        "avec Amir : Nina refuse de foncer, écoute la gouttière, retrouve le "
        "croissant. Matin, sieste ou soir changent la lumière et le dernier "
        "geste. Un objet dans la caisse, le croissant rend la pince, le clip "
        "fait clic. Le rabat n'est plus vide."
    )
    out["title"] = TITLE
    out["characters"] = "Nina, Amir, papa, maman"
    out["setting"] = "entrée d'immeuble, palier des lacets, gouttière, caisse près des chaussures"
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
    if min(lengths) < 550 or max(lengths) > 700:
        raise SystemExit(f"chemins hors 550-700: {min(lengths)}-{max(lengths)}")

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
    avg = sum(lengths) // len(lengths)
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        f"- **Nouveau titre :** *{TITLE}*\n"
        "- **Public :** 5–6 ans (N3), lecture interactive familiale\n"
        "- **Leçon principale :** AUT.RAN.001 — ranger (vécue, non dite)\n"
        "- **Personnages :** Nina, Amir, papa, maman\n"
        "- **Structure conservée :** 86 nœuds, trois choix à trois options, "
        "27 chemins et 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "Au palier des lacets, le rabat du sac s'ouvre vide, comme une bouche "
        "sans sa dent. Nina veut pincer son étoile-clip (bois clair, pointe "
        "jaune, cordelette rouge, clic) dessus, maintenant, pour que le pigeon "
        "la voie. Amir, du troisième, veut jouer avec les jouets. Elle bascule "
        "la caisse trop vite. Un croissant jaune, collé à la corde usée, reste "
        "comme indice du début. Cuisine, jardin ou chambre échouent. Cubes, "
        "livre ou dînette changent la ruse : Nina refuse de foncer, écoute la "
        "gouttière, retrouve le croissant. Matin, sieste ou soir changent la "
        "lumière et le dernier geste. Le clip fait clic. Le rabat n'est plus vide.\n\n"
        "## Améliorations appliquées\n\n"
        "- Ouverture v2 : le rabat vide d'abord, puis le lieu, puis l'objet.\n"
        "- Indice unique du début : croissant jaune sur la corde usée, payé au climax.\n"
        "- Corps : sourire disparu, envie et inquiétude dans la poitrine, papa accroupi.\n"
        "- Deux enfants : Nina veut le clip, Amir veut jouer, pas la même chose.\n"
        "- Première idée échoue : caisse basculée, fouille sous le sac, rien.\n"
        "- Seconde ruse plus rusée : tour / rampe / tasse-couvercle. Nina refuse de foncer. "
        "Personne ne donne la réponse. Elle écoute la gouttière, retrouve le croissant.\n"
        "- T1 ne retire pas l'équipement : sac, caisse, clip, Amir restent.\n"
        "- T1/T2/T3 changent l'action, pas seulement le lieu.\n"
        "- 27 fins textuellement distinctes, dernière image unique.\n"
        "- Un merci vécu (ouverture), pas un refrain Bravo.\n"
        "- Pas de « encore / déjà / tout doux », pas merle, pas miel, pas apply.\n\n"
        "## Direction vocale\n\n"
        "TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending) : "
        "rate, pitch, volume, pauses, text_ssml, text_xai_tags, notes d'arc.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, {min(lengths)} à {max(lengths)} mots, moyenne {avg}\n"
        "- 27 fins et 27 dernières images distinctes\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés\n"
        "- N3 ≤ 16 mots/phrase. `check()` OK.\n\n"
        "## Relu\n\n"
        "P0000, 3 L1, 9 L2, 27 résolutions, 27 fins. Questions liées à la scène "
        "(sac / bottes / oreiller). Impatience, découragement, fierté calme.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {folder / 'merged.json'} bytes={(folder / 'merged.json').stat().st_size}")
    print(f"chemins {min(lengths)}-{max(lengths)} moy={avg}")


if __name__ == "__main__":
    main()
