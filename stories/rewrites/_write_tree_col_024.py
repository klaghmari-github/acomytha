#!/usr/bin/env python3
"""TREE-COL-024 — Le rond sur la vitre de Nina (N2, COL.ECO.001)."""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, relecture, words  # noqa: E402

SID = "TREE-COL-024"
N2 = LIMITS["N2"]
TITLE = "Le rond sur la vitre de Nina"
FIL = (
    "Nina trace un rond dans la buée de la cuisine. Un croissant d'eau "
    "tient en bas. Elle veut porter sa lune de carton jusqu'au parc "
    "derrière la haie, pour jouer avec Aniss. Aniss veut le toboggan, "
    "elle veut le bac : leurs phrases se cognent. Elle crie trop tôt, "
    "le fil s'accroche, la lune penche. Bac, toboggan ou balançoires "
    "changent l'obstacle. Ballon, seau ou doudou changent la ruse. "
    "Banc, haie ou portillon changent la manière d'être entendue. "
    "Au retour, le rond est devenu un ovale, et le carton garde le croissant."
)
TICS = ("tout doux", "tout calme", "encore", "déjà", "aujourd'hui,")

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="croissant d'eau",
        note="arc=installation; intention=émerveiller; emotion=envie_impatiente; intensite=1; destinataire=enfant; sous_texte=deux envies se cognent derrière la haie; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_phrase_a_eu_sa_place; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="lune",
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_coupe_la_phrase_d_Aniss; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="croissant d'eau",
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_retenue; intensite=2; destinataire=enfant; sous_texte=le_croissant_apprend_à_attendre; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=écouter_a_ouvert_le_jeu; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="rond",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_rond_est_devenu_ovale; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def L(*rows: str) -> list[str]:
    out: list[str] = []
    prev = ""
    run = 1
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        low = ph.lower()
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"tic « {tic} »: {ph}")
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


def ssml(text: str, m: dict) -> str:
    body = html.escape(text, quote=False)
    emp = m.get("emphasis")
    if emp and emp in text:
        e = html.escape(emp, quote=False)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f"{body}</prosody><break time=\"{m['pause']}ms\"/></speak>"
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
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    pause = m["pause"]
    suffix = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + suffix).strip()


def voice(nc: dict, profile: str, extra_note: str = "", emphasis: str | None = False) -> None:
    m = dict(PROFILES[profile])
    if emphasis is not False:
        m["emphasis"] = emphasis
    text = nc["text"]
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
    nc["emphasis_words"] = m["emphasis"] or ""
    nc["pause_before_ms"] = 0
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
    note = m["note"]
    if extra_note:
        note = note + "; " + extra_note
    nc["notes"] = note
    nc["night_policy"] = nc.get("night_policy") or "play"
    nc["locale"] = nc.get("locale") or "fr-FR"
    nc["voice_id"] = nc.get("voice_id") or "fr_FR-siwis-medium"


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str, ok: str) -> dict:
    return {
        "expected_answer": ans,
        "accepted_examples": acc,
        "retry_prompt": retry,
        "engine_ok_text": ok,
        "engine_near_text": "Tu es proche. Écoute l'indice.",
    }


def profile_for(cid: str, kind: str) -> str:
    if kind == "passage_debut":
        return "opening"
    if kind == "transition_question":
        return "choice"
    if kind == "passage_question":
        return "clue"
    if kind == "passage_fin":
        return "ending"
    if cid.endswith("_C0001"):
        return "confirm"
    if "_T0003_P000" in cid and cid[-1] in "123":
        return "resolution"
    if "_T0002_P000" in cid and cid[-1] in "123":
        return "obstacle"
    return "action"


# ---------------------------------------------------------------------------
# Récit
# ---------------------------------------------------------------------------

DEBUT = L(
    "narrateur|Le couvercle de la soupe se pose, toc.",
    "narrateur|Un nuage tiède monte vers la vitre.",
    "narrateur|La cuisine de Nina devient un brouillard blanc.",
    "narrateur|Le reflet du couvercle s'arrondit sur le verre.",
    "enfant-f|On dirait une lune coincée !",
    "narrateur|Nina grimpe sur le tabouret, le doigt levé.",
    "narrateur|Elle trace un rond autour du reflet.",
    "narrateur|En bas du rond, un croissant d'eau tient.",
    "narrateur|Il attend, recourbé, sans se presser.",
    "narrateur|À travers le rond, on voit la haie.",
    "narrateur|Aniss est là, bonnet rouge, près du bac.",
    "narrateur|Sur la table, une lune de carton repose.",
    "narrateur|Elle est blanche, légère, avec un fil d'argent.",
    "narrateur|Le fil fait un petit clic contre l'assiette.",
    "enfant-f|Je te l'apporte, Aniss !",
    "narrateur|En ce moment, Nina veut partir vers le parc.",
    "narrateur|Aniss, derrière la haie, pointe le toboggan.",
    "copain|Le toboggan, moi !",
    "enfant-f|Non, le bac !",
    "narrateur|Le sourire de Nina disparaît.",
    "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
    "narrateur|Elle crie à travers le verre.",
    "enfant-f|Aniss, le bac, vite !",
    "narrateur|Papa parle du sel avec maman.",
    "narrateur|Leurs phrases se croisent, et personne ne se tourne.",
    "narrateur|Nina saisit la lune, trop vite.",
    "narrateur|Le fil s'accroche à la salière.",
    "narrateur|La lune penche.",
    "narrateur|Le croissant d'eau tremble.",
    "enfant-f|Elle va tomber !",
    "papa|Tu disais, Nina ?",
    "maman|On t'écoute, si tu attends un peu.",
)

T1Q = L(
    "narrateur|La lune de carton tient, de justesse.",
    "papa|Le bac, le toboggan, ou les balançoires ?",
    "maman|Où vas-tu retrouver Aniss ?",
)

T1 = {
    1: L(
        "narrateur|Nina passe le portillon, la lune contre elle.",
        "narrateur|Le fil d'argent cliquette, léger.",
        "narrateur|Aniss est accroupi dans le bac à sable.",
        "copain|Moi, je creuse une rivière.",
        "enfant-f|Non, un cratère pour la lune !",
        "narrateur|Sa phrase recouvre celle d'Aniss.",
        "narrateur|Le sable gicle.",
        "narrateur|La lune prend une poussière beige.",
        "narrateur|Aniss ferme la bouche, les joues chaudes.",
        "narrateur|Nina s'arrête.",
        "narrateur|L'envie de couper lui pince le ventre.",
        "narrateur|Papa s'accroupit à leur hauteur.",
        "papa|Je vous écoute, l'un après l'autre.",
        "narrateur|Aniss reprend sa rivière, jusqu'au bout.",
        "copain|Après, ta lune peut s'y baigner.",
        "enfant-f|D'accord.",
        "maman|Merci, Nina.",
        "narrateur|Le sable garde deux traces de genoux.",
    ),
    2: L(
        "narrateur|Nina court vers le toboggan gris.",
        "narrateur|Les marches sont tièdes, un peu rèches.",
        "narrateur|Aniss tient la barre, bonnet rouge en avant.",
        "copain|La lune glisse avec moi !",
        "enfant-f|Non, je la rattrape en bas !",
        "narrateur|Leurs mots se cognent sur le métal.",
        "narrateur|La lune bascule.",
        "narrateur|Le fil frotte la rampe.",
        "narrateur|Un clic trop fort.",
        "narrateur|Nina a les joues brûlantes.",
        "narrateur|Elle referme la bouche, les épaules hautes.",
        "narrateur|Maman s'accroupit au pied de l'échelle.",
        "maman|Une voix, puis l'autre.",
        "copain|Moi d'abord, ensuite tu l'attrapes.",
        "enfant-f|D'accord, j'attends en bas.",
        "papa|Merci, Nina.",
        "narrateur|La rampe garde une poussière d'argent.",
    ),
    3: L(
        "narrateur|Nina pousse une balançoire vide.",
        "narrateur|La chaîne grince, longue, comme une phrase.",
        "narrateur|Aniss est sur l'autre, bonnet rouge.",
        "copain|Je te raconte mon vol !",
        "enfant-f|La lune vole avec moi !",
        "narrateur|Sa voix passe sous le grincement.",
        "narrateur|Aniss n'entend que le vent.",
        "narrateur|La lune tape la chaîne, tin.",
        "narrateur|Nina se tait, le ventre serré.",
        "narrateur|Papa pose une main sur le montant.",
        "papa|On laisse la chaîne finir.",
        "narrateur|Le grincement s'arrête.",
        "copain|Maintenant, je t'écoute.",
        "enfant-f|La lune peut s'asseoir entre nous.",
        "maman|Merci d'avoir attendu.",
        "narrateur|Deux balançoires se font face, immobiles.",
    ),
}

Q1 = {
    1: L(
        "narrateur|Un nuage beige a touché le carton.",
        "maman|Qu'est-ce qui a giclé sur la lune ?",
    ),
    2: L(
        "narrateur|Un bruit trop fort a couru sur la rampe.",
        "papa|Qu'est-ce qui a frotté le métal ?",
    ),
    3: L(
        "narrateur|Un son a recouvert la voix de Nina.",
        "maman|Qu'est-ce qui grinçait si fort ?",
    ),
}

C1 = {
    1: L(
        "enfant-f|Le sable !",
        "papa|Oui, le sable du bac.",
        "narrateur|La lune de carton a une poussière beige.",
        "narrateur|Aniss souffle dessus, tout bas.",
        "maman|Il vous reste un jeu à inventer.",
        "enfant-f|Oui.",
        "narrateur|Deux genoux gardent la forme du cratère.",
    ),
    2: L(
        "enfant-f|Le fil !",
        "maman|Oui, le fil d'argent.",
        "narrateur|La rampe a pris un clic, puis le silence.",
        "narrateur|Aniss reste en haut, sans glisser.",
        "papa|Il vous reste un jeu à inventer.",
        "enfant-f|Oui.",
        "narrateur|Une poussière d'argent dort sur le métal.",
    ),
    3: L(
        "enfant-f|La chaîne !",
        "papa|Oui, la chaîne de la balançoire.",
        "narrateur|Le grincement s'est tu.",
        "narrateur|Aniss attend, les pieds dans l'herbe.",
        "maman|Il vous reste un jeu à inventer.",
        "enfant-f|Oui.",
        "narrateur|La lune pend au milieu, légère.",
    ),
}

T2Q = {
    1: L(
        "narrateur|Dans le bac, la lune attend, un peu sableuse.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Qu'est-ce qui peut aider le jeu ?",
    ),
    2: L(
        "narrateur|Au toboggan, la lune attend, un peu penchée.",
        "maman|Le ballon, le seau, ou le doudou ?",
        "papa|Qu'est-ce qui peut aider le jeu ?",
    ),
    3: L(
        "narrateur|Entre les balançoires, la lune attend.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Qu'est-ce qui peut aider le jeu ?",
    ),
}

T2 = {
    (1, 1): L(
        "narrateur|Un ballon rouge dévale le tas de sable.",
        "narrateur|Il vise le cratère, et la lune.",
        "enfant-f|Je l'arrête !",
        "narrateur|Nina tend la main, puis la retire.",
        "narrateur|Aniss n'a pas fini sa phrase.",
        "copain|Le ballon peut rouler derrière.",
        "narrateur|Personne ne dit la suite.",
        "narrateur|Nina regarde la lune de carton.",
        "narrateur|Sur le fil d'argent, un croissant d'eau brille.",
        "enfant-f|Il attend, comme sur la vitre.",
        "narrateur|Le ballon s'arrête contre une pelle.",
        "papa|Vous avez trouvé sans moi.",
        "narrateur|Le carton a une petite fraîcheur, maintenant.",
    ),
    (1, 2): L(
        "narrateur|Le seau bleu est plein d'eau sombre.",
        "narrateur|Aniss le tire vers sa rivière.",
        "enfant-f|C'est pour mon cratère !",
        "narrateur|Nina le saisit.",
        "narrateur|L'eau se renverse.",
        "narrateur|Elle pose le seau, les joues chaudes.",
        "narrateur|Personne ne donne la réponse.",
        "narrateur|Sur le bord, un croissant d'eau tient.",
        "narrateur|Comme en bas du rond, à la cuisine.",
        "enfant-f|On attend qu'il tombe.",
        "copain|Quand il tombe, on verse ensemble.",
        "maman|Vos yeux ont vu la même chose.",
        "narrateur|Le croissant glisse, lent, puis disparaît.",
        "narrateur|L'eau rejoint la rivière, sans se battre.",
    ),
    (1, 3): L(
        "narrateur|Le doudou gris d'Aniss dort près de la lune.",
        "copain|Il veut l'ombre du carton.",
        "enfant-f|La lune d'abord !",
        "narrateur|Nina parle trop tôt.",
        "narrateur|Aniss se tait.",
        "narrateur|Elle serre les lèvres, refuse de foncer.",
        "narrateur|Personne ne dit quoi faire.",
        "narrateur|Une goutte recourbée brille sur le doudou.",
        "narrateur|Un croissant d'eau, le même qu'à la vitre.",
        "enfant-f|Ton doudou a soif, lui aussi.",
        "copain|Il écoute, après.",
        "papa|Deux phrases, l'une après l'autre.",
        "narrateur|Le doudou s'adosse au carton, sans le cacher.",
        "narrateur|Son fil d'argent reste libre, un peu humide.",
    ),
    (2, 1): L(
        "narrateur|En bas du toboggan, un ballon rouge attend.",
        "copain|La lune, puis le ballon !",
        "enfant-f|Non, le ballon va la bousculer !",
        "narrateur|Nina crie pendant qu'Aniss glisse.",
        "narrateur|Sa voix se perd dans le vent de la rampe.",
        "narrateur|Elle refuse de courir au hasard.",
        "narrateur|Personne ne donne la réponse.",
        "narrateur|Sur le ballon, un croissant d'eau brille.",
        "enfant-f|Il attend, comme sur la vitre.",
        "copain|J'attends aussi, en bas.",
        "maman|La rampe a fini sa phrase.",
        "narrateur|La lune arrive dans les mains de Nina.",
        "narrateur|Le ballon reste à côté, sans frapper.",
    ),
    (2, 2): L(
        "narrateur|Un seau bleu attend au pied du toboggan.",
        "copain|Pour attraper la lune !",
        "enfant-f|Elle va se mouiller !",
        "narrateur|Nina avance trop vite.",
        "narrateur|L'eau clabousse.",
        "narrateur|Elle recule, le carton collé au cœur.",
        "narrateur|Personne ne dit la suite.",
        "narrateur|Sur le bord du seau, un croissant d'eau tient.",
        "narrateur|Le même qu'en bas du rond, à la cuisine.",
        "enfant-f|On le laisse tomber, d'abord.",
        "copain|Après, je glisse sans le seau.",
        "papa|Vos yeux ont vu le croissant.",
        "narrateur|Le croissant glisse, et le seau s'écarte.",
        "narrateur|La rampe reste sèche, pour la lune.",
    ),
    (2, 3): L(
        "narrateur|Le doudou gris d'Aniss est assis sur la rampe.",
        "copain|Il glisse avant la lune.",
        "enfant-f|Non, c'est mon tour !",
        "narrateur|Nina parle trop fort.",
        "narrateur|Le doudou bascule.",
        "narrateur|Elle le rattrape, puis se tait.",
        "narrateur|Personne ne donne la réponse.",
        "narrateur|Une goutte recourbée brille sur l'oreille du doudou.",
        "narrateur|Un croissant d'eau, le même qu'à la vitre.",
        "enfant-f|Il veut écouter, lui aussi.",
        "copain|Toi, puis moi, puis lui.",
        "maman|Trois voix, l'une après l'autre.",
        "narrateur|Le doudou redescend, sans se presser.",
        "narrateur|La lune attend en haut, le fil calme.",
    ),
    (3, 1): L(
        "narrateur|Un ballon rouge roule sous les balançoires.",
        "copain|Je le pousse avec le pied !",
        "enfant-f|Il va toucher la lune !",
        "narrateur|Nina coupe la phrase.",
        "narrateur|La chaîne reprend.",
        "narrateur|Elle se tait, refuse de foncer.",
        "narrateur|Personne ne dit quoi faire.",
        "narrateur|Sur le ballon, un croissant d'eau brille.",
        "narrateur|Comme en bas du rond, à la cuisine.",
        "enfant-f|On attend qu'il parte tout seul.",
        "copain|Quand il part, je te raconte.",
        "papa|La chaîne a de la place, à présent.",
        "narrateur|Le ballon s'en va vers l'herbe.",
        "narrateur|La lune reste assise, entre deux chaînes.",
    ),
    (3, 2): L(
        "narrateur|Un seau d'eau attend sous les balançoires.",
        "copain|Pour mouiller le sol, et glisser un peu.",
        "enfant-f|Ma lune a peur de l'eau !",
        "narrateur|Nina parle trop tôt.",
        "narrateur|Aniss hausse les épaules.",
        "narrateur|Elle pose la lune sur ses genoux.",
        "narrateur|Personne ne donne la réponse.",
        "narrateur|Sur le bord, un croissant d'eau tient.",
        "narrateur|Le même qu'à la vitre, recourbé.",
        "enfant-f|On verse plus loin, pas ici.",
        "copain|D'accord, près du bac.",
        "maman|Vos deux phrases sont arrivées.",
        "narrateur|Le seau part, sans éclabousser le carton.",
        "narrateur|Les chaînes se taisent, face à face.",
    ),
    (3, 3): L(
        "narrateur|Le doudou gris occupe la balançoire vide.",
        "copain|Il vole avec moi.",
        "enfant-f|La lune voulait cette place !",
        "narrateur|Nina tire le doudou.",
        "narrateur|Aniss dit non.",
        "narrateur|Elle lâche, le ventre serré.",
        "narrateur|Personne ne dit la suite.",
        "narrateur|Une goutte recourbée brille sur le museau.",
        "narrateur|Un croissant d'eau, le même qu'à la vitre.",
        "enfant-f|Il a sa place, la lune a la mienne.",
        "copain|On se parle, sans se pousser.",
        "papa|Deux places, deux voix.",
        "narrateur|Le doudou reste.",
        "narrateur|La lune s'assoit sur Nina.",
        "narrateur|Les chaînes bougent, l'une après l'autre.",
    ),
}

T3Q = {
    1: L(
        "narrateur|Le ballon s'est arrêté.",
        "narrateur|Trois coins attendent la fin.",
        "papa|Le banc, la haie, ou le portillon ?",
        "maman|Où racontez-vous la suite ?",
    ),
    2: L(
        "narrateur|Le seau s'est écarté.",
        "narrateur|Trois coins attendent la fin.",
        "maman|Le banc, la haie, ou le portillon ?",
        "papa|Où racontez-vous la suite ?",
    ),
    3: L(
        "narrateur|Le doudou écoute.",
        "narrateur|Trois coins attendent la fin.",
        "papa|Le banc, la haie, ou le portillon ?",
        "maman|Où racontez-vous la suite ?",
    ),
}


def t3_body(i: int, j: int, k: int) -> list[str]:
    return T3[(i, j, k)]


T3 = {
    (1, 1, 1): L(
        "narrateur|Nina et Aniss s'assoient sur le banc froid.",
        "narrateur|Le ballon rouge dort contre un pied.",
        "enfant-f|J'ai trop parlé, tout à l'heure.",
        "copain|Moi, je voulais la rivière.",
        "narrateur|Nina attend la fin, les mains sur la lune.",
        "enfant-f|On peut les deux, le cratère et l'eau.",
        "papa|Qui raconte à maman, ce soir ?",
        "enfant-f|Le moment difficile, surtout.",
        "maman|Je l'écoute, à la maison.",
        "narrateur|Le carton a un croissant d'eau, pâle.",
        "narrateur|Ça a failli ne pas se poser.",
    ),
    (1, 1, 2): L(
        "narrateur|Ils marchent jusqu'à la haie, le ballon sous le bras.",
        "narrateur|À travers les feuilles, la vitre de la cuisine.",
        "narrateur|Le rond est devenu un ovale flou.",
        "enfant-f|Le croissant n'y est plus.",
        "copain|Il est sur ta lune, regarde.",
        "narrateur|Nina écoute, sans couper.",
        "papa|Vous le voyez tous les deux ?",
        "enfant-f|Oui, une trace froide.",
        "maman|On rentrera quand vous aurez fini.",
        "narrateur|La haie sent le thym mouillé.",
        "narrateur|Le jeu a failli s'arrêter au cri.",
    ),
    (1, 1, 3): L(
        "narrateur|Le portillon grince, comme une question.",
        "narrateur|L'odeur de soupe traverse la haie.",
        "enfant-f|On rentre ?",
        "copain|Un tour, d'abord.",
        "narrateur|Nina laisse Aniss finir, le ballon entre eux.",
        "enfant-f|Un tour, d'accord.",
        "papa|Puis on raconte le cri, à table.",
        "enfant-f|Surtout ça.",
        "maman|La soupe nous attend, sans se fâcher.",
        "narrateur|Le portillon reste entrouvert, un moment.",
        "narrateur|La lune passe, avec sa trace d'eau.",
    ),
    (1, 2, 1): L(
        "narrateur|Sur le banc, le seau bleu sèche au soleil.",
        "narrateur|Nina pose la lune entre eux.",
        "copain|La rivière est faite.",
        "enfant-f|Le cratère aussi.",
        "narrateur|Elle attend qu'Aniss souffle, puis parle.",
        "papa|Qui a versé ?",
        "copain|Nous deux, après le croissant.",
        "maman|Ce soir, vous me direz le renversement.",
        "enfant-f|Oui, le moment où l'eau est partie.",
        "narrateur|Le banc garde un rond d'humidité.",
        "narrateur|Le carton, lui, garde le croissant.",
    ),
    (1, 2, 2): L(
        "narrateur|Près de la haie, le seau est vide.",
        "narrateur|La vitre, au loin, n'a plus de rond net.",
        "enfant-f|Il s'est fermé.",
        "copain|On a le croissant ici.",
        "narrateur|Nina le laisse finir, le seau contre la hanche.",
        "papa|Vous rentrerez par le thym ?",
        "enfant-f|Oui, et on raconte le seau.",
        "maman|J'écoute le difficile, pas seulement le beau.",
        "narrateur|Une feuille retient une goutte recourbée.",
        "narrateur|Nina ne la chasse pas.",
        "narrateur|Le jeu a failli finir dans l'eau versée.",
    ),
    (1, 2, 3): L(
        "narrateur|Au portillon, le seau cliquette, presque sec.",
        "narrateur|La soupe appelle, tiède.",
        "copain|On laisse le seau au bac.",
        "enfant-f|Attends, je n'ai pas fini.",
        "narrateur|Aniss s'arrête.",
        "narrateur|Nina parle jusqu'au bout.",
        "enfant-f|Merci d'attendre.",
        "papa|Le portillon peut patienter.",
        "maman|À table, le croissant aussi.",
        "narrateur|Ils posent le seau, sans le jeter.",
        "narrateur|La lune passe le seuil, tachée d'un arc pâle.",
        "narrateur|Ça a failli rester un cri, rien de plus.",
    ),
    (1, 3, 1): L(
        "narrateur|Sur le banc, le doudou gris s'adosse à Nina.",
        "copain|Il a eu sa place.",
        "enfant-f|La lune a eu la sienne.",
        "narrateur|Elle laisse le silence, puis reprend.",
        "enfant-f|J'ai eu peur de trop parler.",
        "papa|Tu peux le dire, ce soir.",
        "maman|On a des oreilles, à la maison.",
        "narrateur|Le doudou sent le sable, un peu.",
        "narrateur|Le carton sent l'eau, un peu.",
        "narrateur|Deux odeurs, deux phrases, un banc.",
        "narrateur|Le jeu a failli se casser au premier mot.",
    ),
    (1, 3, 2): L(
        "narrateur|La haie cache le doudou, puis le montre.",
        "narrateur|La vitre, derrière, est un ovale clair.",
        "copain|Ton rond est parti.",
        "enfant-f|Il a laissé le croissant sur le carton.",
        "narrateur|Nina écoute le bonnet rouge, jusqu'au bout.",
        "papa|On rentre par ici ?",
        "enfant-f|Oui, et je raconte le doudou.",
        "maman|Le moment où tu as lâché, surtout.",
        "narrateur|Le thym colle aux doigts, vert et fort.",
        "narrateur|Le fil d'argent a une fraîcheur d'oreille.",
        "narrateur|Ça a failli rester une dispute de sable.",
    ),
    (1, 3, 3): L(
        "narrateur|Au portillon, le doudou passe en premier.",
        "copain|Il rentre.",
        "copain|La lune aussi.",
        "enfant-f|J'attends que tu finisses.",
        "narrateur|Aniss sourit, sans se presser.",
        "papa|La soupe fume, on a le temps d'une phrase.",
        "enfant-f|Le difficile, c'était de me taire.",
        "maman|On l'entendra, ce soir.",
        "narrateur|Le portillon se ferme, un petit cri.",
        "narrateur|La lune tape l'épaule de Nina, clic.",
        "narrateur|Le croissant d'eau a séché en arc.",
        "narrateur|Le bac reste derrière, avec deux traces.",
    ),
    (2, 1, 1): L(
        "narrateur|Sur le banc, le ballon rouge tient entre eux.",
        "narrateur|La rampe du toboggan brille, loin.",
        "copain|J'ai glissé.",
        "copain|Tu as attrapé.",
        "enfant-f|J'ai crié trop tôt, d'abord.",
        "narrateur|Elle le laisse finir, la lune sur les genoux.",
        "papa|Qui raconte le cri, ce soir ?",
        "enfant-f|Moi.",
        "enfant-f|Surtout le cri.",
        "maman|On t'écoute, à table.",
        "narrateur|Le ballon a un croissant d'eau, pâle.",
        "narrateur|Le carton aussi, plus net.",
        "narrateur|La glissade a failli partir sans personne.",
    ),
    (2, 1, 2): L(
        "narrateur|Près de la haie, le ballon sent l'herbe.",
        "narrateur|La vitre montre un ovale, plus de rond.",
        "copain|Ta lune a survécu à la rampe.",
        "enfant-f|Grâce au croissant, j'ai attendu.",
        "narrateur|Nina laisse Aniss souffler, puis hoche la tête.",
        "papa|On rentre par le thym ?",
        "maman|Et vous me direz le clic du fil.",
        "enfant-f|Oui, le clic trop fort.",
        "narrateur|Une feuille retient le bonnet rouge, un instant.",
        "narrateur|Aniss le reprend, sans se presser.",
        "narrateur|Le jeu a failli finir sur le métal.",
    ),
    (2, 1, 3): L(
        "narrateur|Le portillon voit arriver le ballon, puis la lune.",
        "narrateur|L'odeur de soupe est plus forte.",
        "copain|Un dernier regard à la rampe.",
        "enfant-f|J'attends que tu regardes.",
        "narrateur|Aniss regarde.",
        "narrateur|Nina ne parle pas.",
        "papa|Puis on raconte, à table.",
        "enfant-f|Le moment où j'ai crié.",
        "maman|On a de la place pour ça.",
        "narrateur|Le portillon s'ouvre, sans grincer trop.",
        "narrateur|Le fil d'argent cliquette, apaisé.",
        "narrateur|La glissade a failli rester un choc.",
    ),
    (2, 2, 1): L(
        "narrateur|Sur le banc, le seau bleu est presque vide.",
        "copain|On a écarté l'eau.",
        "enfant-f|J'ai reculé, le carton collé.",
        "narrateur|Elle attend qu'Aniss pose le seau.",
        "papa|Qui a vu le croissant en premier ?",
        "enfant-f|Moi, sur le bord.",
        "copain|Moi, après.",
        "maman|Ce soir, le renversement aussi.",
        "narrateur|Le banc a une tache ronde, qui sèche.",
        "narrateur|La lune a un arc, qui reste.",
        "narrateur|Ça a failli finir dans le clabousse.",
    ),
    (2, 2, 2): L(
        "narrateur|La haie cache le seau, trop grand.",
        "narrateur|La vitre, au loin, a perdu son rond.",
        "enfant-f|Il s'est refermé.",
        "copain|On a le croissant sur le carton.",
        "narrateur|Nina écoute, le seau contre la jambe.",
        "papa|Vous rentrez les mains mouillées ?",
        "enfant-f|Un peu.",
        "enfant-f|On racontera l'eau.",
        "maman|Le difficile, pas seulement le sec.",
        "narrateur|Le thym sent plus fort, près du seau.",
        "narrateur|Une goutte recourbée tient sur une feuille.",
        "narrateur|Le toboggan a failli rester trop mouillé.",
    ),
    (2, 2, 3): L(
        "narrateur|Au portillon, le seau doit rester au parc.",
        "copain|Je le pose près de l'échelle.",
        "enfant-f|J'attends que tu le poses.",
        "narrateur|Aniss pose.",
        "narrateur|Nina passe, la lune au chaud.",
        "papa|La soupe, et le récit du clabousse.",
        "maman|On a des oreilles sèches, pour ça.",
        "enfant-f|Le croissant m'a arrêtée.",
        "narrateur|Le portillon se ferme sur le seau, dehors.",
        "narrateur|Le carton a une fraîcheur de bord.",
        "narrateur|L'échelle reste grise, sans eau.",
        "narrateur|Ça a failli être une lune trempée.",
    ),
    (2, 3, 1): L(
        "narrateur|Sur le banc, le doudou s'assoit entre eux.",
        "copain|Toi, puis moi, puis lui.",
        "enfant-f|J'ai parlé trop fort, d'abord.",
        "narrateur|Elle laisse Aniss caresser l'oreille grise.",
        "papa|Qui raconte le bascule, ce soir ?",
        "enfant-f|Moi.",
        "enfant-f|J'ai eu peur.",
        "maman|On t'écoute, sans te presser.",
        "narrateur|Le doudou a une goutte sèche, en croissant.",
        "narrateur|La lune a la même, plus nette.",
        "narrateur|Deux traces, un banc, trois souffles.",
        "narrateur|La rampe a failli garder le doudou.",
    ),
    (2, 3, 2): L(
        "narrateur|Près de la haie, le doudou sent le métal.",
        "narrateur|La vitre n'a plus de rond, seulement un ovale.",
        "copain|Ton croissant a voyagé.",
        "enfant-f|De la vitre au museau, puis au carton.",
        "narrateur|Nina le laisse finir, sans ajouter.",
        "papa|On rentre ?",
        "maman|Après la phrase d'Aniss.",
        "enfant-f|J'attends.",
        "narrateur|Le thym accroche un fil d'argent, une seconde.",
        "narrateur|Nina le détache, lentement.",
        "narrateur|Le jeu a failli rester un non trop fort.",
    ),
    (2, 3, 3): L(
        "narrateur|Au portillon, le doudou passe, puis la lune.",
        "copain|Il a glissé sans tomber.",
        "enfant-f|Parce qu'on a attendu.",
        "narrateur|Elle le dit après lui, pas dessus.",
        "papa|La soupe, et le récit du doudou.",
        "maman|Le moment où tu as rattrapé, aussi.",
        "enfant-f|Surtout ça.",
        "narrateur|Le portillon fait un petit cri, puis se tait.",
        "narrateur|Le fil d'argent ne s'accroche plus.",
        "narrateur|La rampe, derrière, est vide.",
        "narrateur|Ça a failli finir en bascule.",
    ),
    (3, 1, 1): L(
        "narrateur|Sur le banc, le ballon s'adosse à Nina.",
        "narrateur|Les balançoires, derrière, ne grincent plus.",
        "copain|Je t'ai raconté mon vol.",
        "enfant-f|J'ai attendu la chaîne.",
        "narrateur|Elle le laisse ajouter un mot, puis parle.",
        "papa|Qui raconte le grincement, ce soir ?",
        "enfant-f|Moi.",
        "enfant-f|Il a recouvert ma voix.",
        "maman|On a du silence, à table, pour ça.",
        "narrateur|Le ballon a un croissant pâle.",
        "narrateur|La lune l'a plus net, sur le fil.",
        "narrateur|Le vol a failli rester un vent sans oreilles.",
    ),
    (3, 1, 2): L(
        "narrateur|La haie tient le ballon, trop gros.",
        "narrateur|La vitre, au loin, est un ovale vide.",
        "copain|Ton rond s'est ouvert, puis fermé.",
        "enfant-f|Le croissant est resté sur le carton.",
        "narrateur|Nina écoute le bonnet, jusqu'au bout.",
        "papa|On passe par ici ?",
        "maman|Et vous me direz la chaîne.",
        "enfant-f|Oui, le tin trop fort.",
        "narrateur|Une feuille tremble, puis s'arrête.",
        "narrateur|Le fil d'argent ne tape plus.",
        "narrateur|Les balançoires ont failli garder le cri.",
    ),
    (3, 1, 3): L(
        "narrateur|Au portillon, le ballon arrive, puis deux enfants.",
        "copain|Les chaînes se taisent.",
        "enfant-f|J'attends que tu entres.",
        "narrateur|Aniss entre.",
        "narrateur|Nina le suit, la lune au chaud.",
        "papa|La soupe, et le récit du tin.",
        "maman|On a des oreilles, ce soir.",
        "enfant-f|Le difficile, c'était de me taire.",
        "narrateur|Le portillon se ferme sur l'herbe.",
        "narrateur|Plus de grincement, seulement un clic du fil.",
        "narrateur|Le croissant d'eau a séché en arc.",
        "narrateur|Ça a failli rester deux voix ensemble.",
    ),
    (3, 2, 1): L(
        "narrateur|Sur le banc, le seau est loin, près du bac.",
        "copain|On a versé plus loin.",
        "enfant-f|Ma lune n'a pas eu peur.",
        "narrateur|Elle attend qu'Aniss pose les mains.",
        "papa|Qui a vu le croissant du bord ?",
        "enfant-f|Moi, puis toi.",
        "maman|Ce soir, la peur de l'eau aussi.",
        "narrateur|Le banc est sec, les chaînes aussi.",
        "narrateur|La lune a un arc, à peine.",
        "narrateur|Deux souffles, l'un après l'autre.",
        "narrateur|Le sol a failli devenir une glissade.",
    ),
    (3, 2, 2): L(
        "narrateur|Près de la haie, plus de seau.",
        "narrateur|La vitre n'a plus de rond, un ovale seulement.",
        "copain|Ton croissant a choisi le carton.",
        "enfant-f|Il a quitté la vitre.",
        "narrateur|Nina le laisse finir, les mains sèches.",
        "papa|On rentre ?",
        "maman|Après sa phrase.",
        "enfant-f|J'attends.",
        "narrateur|Le thym sent le vert, sans eau.",
        "narrateur|Une feuille garde une goutte recourbée.",
        "narrateur|Les balançoires ont failli se mouiller.",
    ),
    (3, 2, 3): L(
        "narrateur|Au portillon, les mains sont sèches.",
        "copain|Le seau est resté au bac.",
        "enfant-f|J'attends que tu le dises jusqu'au bout.",
        "narrateur|Aniss finit.",
        "narrateur|Nina hoche la tête.",
        "papa|La soupe, et le récit du seau.",
        "maman|Le moment où tu as posé la lune.",
        "enfant-f|Surtout ça.",
        "narrateur|Le portillon s'ouvre sur l'odeur tiède.",
        "narrateur|Le fil d'argent ne goutte plus.",
        "narrateur|Les chaînes, derrière, sont immobiles.",
        "narrateur|Ça a failli être une lune mouillée.",
    ),
    (3, 3, 1): L(
        "narrateur|Sur le banc, le doudou a sa place, Nina la sienne.",
        "copain|On s'est parlé, sans se pousser.",
        "enfant-f|J'ai lâché, le ventre serré.",
        "narrateur|Elle le laisse ajouter, puis reprend.",
        "papa|Qui raconte le non, ce soir ?",
        "enfant-f|Moi.",
        "enfant-f|Aniss a dit non.",
        "maman|On écoute le non, et le lâcher.",
        "narrateur|Le doudou a une goutte sèche, en croissant.",
        "narrateur|La lune a la même, sur le fil.",
        "narrateur|Deux places, un banc, plus de chaîne.",
        "narrateur|Le jeu a failli rester un tirage.",
    ),
    (3, 3, 2): L(
        "narrateur|La haie cache le doudou, trop gris.",
        "narrateur|La vitre, au loin, est un ovale clair.",
        "copain|Ton rond est parti.",
        "enfant-f|Le croissant est resté.",
        "narrateur|Nina écoute, la lune contre l'épaule.",
        "papa|On passe le thym ?",
        "maman|Et vous me direz le lâcher.",
        "enfant-f|Oui, le moment où j'ai ouvert la main.",
        "narrateur|Une feuille accroche le fil, puis le rend.",
        "narrateur|Nina ne tire pas.",
        "narrateur|Les balançoires ont failli garder la colère.",
    ),
    (3, 3, 3): L(
        "narrateur|Au portillon, le doudou passe, la lune suit.",
        "copain|Chacun sa place.",
        "enfant-f|J'attends que tu entres.",
        "narrateur|Aniss entre.",
        "narrateur|Nina le suit, sans se pousser.",
        "papa|La soupe, et le récit des deux places.",
        "maman|Le non, aussi.",
        "maman|On l'écoute.",
        "enfant-f|Surtout le non.",
        "narrateur|Le portillon se ferme, un petit cri poli.",
        "narrateur|Le fil d'argent reste libre, sans nœud.",
        "narrateur|Derrière, deux balançoires se font face, vides.",
        "narrateur|Ça a failli rester une place volée.",
    ),
}

FINS = {
    (1, 1, 1): L(
        "narrateur|Dans la cuisine, la buée a reculé.",
        "narrateur|Le rond est un ovale, vide et clair.",
        "enfant-f|Le croissant est sur ma lune.",
        "papa|Je le vois.",
        "maman|Merci d'avoir raconté le cri.",
        "narrateur|La salière n'accroche plus le fil.",
        "narrateur|Le ballon reste au parc, rouge et loin.",
        "narrateur|La soupe sent le sel, près du feu.",
    ),
    (1, 1, 2): L(
        "narrateur|Nina pose la lune près de l'assiette.",
        "narrateur|À travers l'ovale, la haie est nette.",
        "enfant-f|Aniss a vu le croissant, lui aussi.",
        "maman|Je t'ai entendue jusqu'au bout.",
        "papa|Merci pour le thym, sur tes doigts.",
        "narrateur|Le tabouret est vide, un peu tiède.",
        "narrateur|Le carton a une trace froide, en arc.",
        "narrateur|Plus de brouillard sur le verre.",
    ),
    (1, 1, 3): L(
        "narrateur|Le portillon a laissé passer la lune.",
        "narrateur|Elle sèche près du couvercle, toc.",
        "enfant-f|On a eu un tour, d'abord.",
        "papa|Merci d'être rentrée avec la phrase.",
        "maman|La soupe n'a pas grogné.",
        "narrateur|L'ovale encadre le parc, sans Aniss.",
        "narrateur|Le bonnet rouge a quitté le verre.",
        "narrateur|Il reste un clic d'argent, très bas.",
    ),
    (1, 2, 1): L(
        "narrateur|Le seau est resté au bac, loin.",
        "narrateur|La lune, elle, a un croissant pâle.",
        "enfant-f|On a versé ensemble.",
        "maman|Merci d'avoir attendu le bord.",
        "papa|Le banc avait un rond d'eau, je l'ai vu.",
        "narrateur|L'assiette cliquette, comme le fil.",
        "narrateur|L'ovale de la vitre est sec, presque blanc.",
        "narrateur|La casserole ne fume plus, ou si peu.",
    ),
    (1, 2, 2): L(
        "narrateur|Nina a les manches un peu mouillées.",
        "narrateur|Elle pose la lune, face à l'ovale.",
        "enfant-f|Le rond s'est fermé, dehors il reste.",
        "papa|Merci pour la feuille, et la goutte.",
        "maman|J'écoute le seau, pas seulement le carton.",
        "narrateur|Le thym a suivi jusqu'à la table.",
        "narrateur|Un grain de sable dort sur le fil.",
        "narrateur|La vitre n'écrit plus rien.",
    ),
    (1, 2, 3): L(
        "narrateur|Le seau n'est pas rentré.",
        "narrateur|La lune si, tachée d'un arc pâle.",
        "enfant-f|Aniss a attendu ma phrase.",
        "maman|Merci, le portillon aussi.",
        "papa|La soupe est là, sans se fâcher.",
        "narrateur|Le seuil garde une poussière beige.",
        "narrateur|L'ovale montre le bac, vide.",
        "narrateur|Deux traces de genoux ont disparu.",
    ),
    (1, 3, 1): L(
        "narrateur|Le doudou n'est pas là, seulement son odeur.",
        "narrateur|La lune sent le sable, et l'eau.",
        "enfant-f|On a eu deux places.",
        "papa|Merci d'avoir parlé après le silence.",
        "maman|Le banc a gardé vos deux souffles.",
        "narrateur|L'ovale est clair, trop clair.",
        "narrateur|Nina pose un doigt, sans retracer.",
        "narrateur|Le croissant du carton suffit.",
    ),
    (1, 3, 2): L(
        "narrateur|Le fil d'argent a une fraîcheur d'oreille.",
        "narrateur|Nina le pose près du sel.",
        "enfant-f|J'ai lâché le doudou.",
        "maman|Merci de le raconter.",
        "papa|La haie a vu le lâcher, nous aussi.",
        "narrateur|L'ovale cadre le thym, tout vert.",
        "narrateur|Plus de bonnet dans le verre.",
        "narrateur|Le carton a un arc, comme une oreille.",
    ),
    (1, 3, 3): L(
        "narrateur|Le portillon a crié, puis s'est tu.",
        "narrateur|La lune tape l'épaule, un dernier clic.",
        "enfant-f|Le difficile, c'était de me taire.",
        "papa|Merci, on l'a entendu.",
        "maman|Le bac garde vos traces, pas vos cris.",
        "narrateur|L'ovale est vide, le parc aussi.",
        "narrateur|Le croissant a séché en arc, sur le blanc.",
        "narrateur|La soupe fait un petit nuage, sans tout cacher.",
    ),
    (2, 1, 1): L(
        "narrateur|La rampe n'est plus là, seulement son clic.",
        "narrateur|La lune a un croissant, plus net que le ballon.",
        "enfant-f|J'ai crié trop tôt, d'abord.",
        "maman|Merci de le dire, maintenant.",
        "papa|Le banc a entendu la suite.",
        "narrateur|L'ovale de la vitre est sec.",
        "narrateur|Plus de poussière d'argent sur le verre.",
        "narrateur|Le couvercle repose, rond, sans reflet.",
    ),
    (2, 1, 2): L(
        "narrateur|Nina a de l'herbe au genou, sèche.",
        "narrateur|Elle pose la lune, face à l'ovale.",
        "enfant-f|Aniss a dit que j'avais survécu.",
        "papa|Merci pour le clic trop fort, raconté.",
        "maman|La haie a rendu le bonnet, et ta phrase.",
        "narrateur|Le tabouret attend, inutile.",
        "narrateur|Le carton sent l'herbe, et le métal.",
        "narrateur|La vitre n'a plus de lune coincée.",
    ),
    (2, 1, 3): L(
        "narrateur|Le portillon s'est ouvert sans trop grincer.",
        "narrateur|La lune cliquette, apaisée.",
        "enfant-f|J'ai attendu qu'il regarde la rampe.",
        "maman|Merci, ta phrase est arrivée entière.",
        "papa|La soupe a de la place pour le cri.",
        "narrateur|L'ovale encadre l'échelle, petite.",
        "narrateur|Plus de bonnet rouge dans le cadre.",
        "narrateur|Un grain de sel brille, puis fond.",
    ),
    (2, 2, 1): L(
        "narrateur|Nina a une manche froide, près du poignet.",
        "narrateur|La lune a un arc, le banc une tache.",
        "enfant-f|J'ai vu le croissant sur le bord.",
        "papa|Merci d'avoir reculé.",
        "maman|Le clabousse a eu sa phrase, à table.",
        "narrateur|L'assiette est sèche, le verre aussi.",
        "narrateur|L'ovale ne fume plus.",
        "narrateur|Le seau, lui, est resté au pied de l'échelle.",
    ),
    (2, 2, 2): L(
        "narrateur|Les doigts de Nina sentent le thym, et l'eau.",
        "narrateur|Elle pose la lune, un peu recourbée.",
        "enfant-f|Le rond s'est refermé.",
        "maman|Merci pour le difficile, pas seulement le sec.",
        "papa|La haie a gardé une goutte, pas vous.",
        "narrateur|L'ovale est blanc, presque trop.",
        "narrateur|Le carton a le croissant, lui.",
        "narrateur|La casserole est tiède, sans nuage.",
    ),
    (2, 2, 3): L(
        "narrateur|Le seau est dehors, près de l'échelle.",
        "narrateur|La lune est dedans, fraîche au bord.",
        "enfant-f|Le croissant m'a arrêtée.",
        "papa|Merci, elle n'est pas trempée.",
        "maman|Le portillon a fermé l'eau dehors.",
        "narrateur|L'ovale montre l'échelle, grise et sèche.",
        "narrateur|Plus de clabousse dans la cuisine.",
        "narrateur|Le sel reste dans sa salière, sage.",
    ),
    (2, 3, 1): L(
        "narrateur|Le doudou est au parc.",
        "narrateur|Son odeur, ici.",
        "narrateur|La lune a la même goutte sèche, en croissant.",
        "enfant-f|J'ai eu peur, quand il a basculé.",
        "maman|Merci de raconter la peur.",
        "papa|Le banc a pris trois souffles, on en a deux.",
        "narrateur|L'ovale est calme, sans chaîne.",
        "narrateur|Le fil d'argent ne s'accroche plus à rien.",
        "narrateur|Le couvercle fait un rond, sur la table.",
    ),
    (2, 3, 2): L(
        "narrateur|Nina détache un brin de thym du fil.",
        "narrateur|Elle le pose près de l'assiette.",
        "enfant-f|J'ai attendu sa phrase, à la haie.",
        "papa|Merci, tu n'as pas ajouté dessus.",
        "maman|L'ovale a vu le détachement, lent.",
        "narrateur|Le verre n'a plus de rond, seulement le parc.",
        "narrateur|Le carton a voyagé, vitre puis museau.",
        "narrateur|La soupe attend, sans couper.",
    ),
    (2, 3, 3): L(
        "narrateur|Le portillon a fini son petit cri.",
        "narrateur|La lune n'a plus de nœud au fil.",
        "enfant-f|On a attendu, alors il n'est pas tombé.",
        "maman|Merci pour le rattrapage, raconté.",
        "papa|La rampe est vide, c'est bien.",
        "narrateur|L'ovale encadre un toboggan sans personne.",
        "narrateur|Le croissant a séché, net, sur le blanc.",
        "narrateur|Un clic, puis plus rien, près de l'assiette.",
    ),
    (3, 1, 1): L(
        "narrateur|Plus de chaîne, seulement le souvenir du tin.",
        "narrateur|La lune a un croissant, sur le fil.",
        "enfant-f|Il a recouvert ma voix.",
        "papa|Merci de le dire, maintenant qu'on entend.",
        "maman|Le banc a rendu le silence, on le garde.",
        "narrateur|L'ovale est vide, les balançoires trop petites.",
        "narrateur|Le ballon est resté dehors, rouge.",
        "narrateur|La soupe fume un filet, pas un mur.",
    ),
    (3, 1, 2): L(
        "narrateur|Nina pose la lune, le fil vers l'ovale.",
        "narrateur|Plus de tin, plus de rond coincé.",
        "enfant-f|Le croissant est resté, le rond non.",
        "maman|Merci pour la feuille, et le bonnet.",
        "papa|La haie a arrêté le tremblement.",
        "narrateur|Le tabouret est rangé, sous la table.",
        "narrateur|Le carton a un arc, comme une oreille.",
        "narrateur|À travers le verre, l'herbe est nette.",
    ),
    (3, 1, 3): L(
        "narrateur|Le portillon a fermé l'herbe dehors.",
        "narrateur|La lune a un clic, puis un arc sec.",
        "enfant-f|Le difficile, c'était de me taire.",
        "papa|Merci, ta phrase est entrée entière.",
        "maman|On a des oreilles, ce soir.",
        "narrateur|L'ovale n'a plus deux voix ensemble.",
        "narrateur|Il a le parc, vide, et le soir qui vient.",
        "narrateur|Le sel attend, pour la soupe seulement.",
    ),
    (3, 2, 1): L(
        "narrateur|Les mains de Nina sont sèches, enfin.",
        "narrateur|La lune a un arc, à peine.",
        "enfant-f|On a versé plus loin.",
        "maman|Merci d'avoir posé la lune, d'abord.",
        "papa|Le banc était sec, les chaînes aussi.",
        "narrateur|L'ovale ne goutte plus.",
        "narrateur|Le seau est au bac, invisible d'ici.",
        "narrateur|La casserole fait un petit toc, puis se tait.",
    ),
    (3, 2, 2): L(
        "narrateur|Nina a une feuille dans la poche, une seule.",
        "narrateur|Dessus, une goutte recourbée a séché.",
        "enfant-f|J'ai attendu sa phrase.",
        "papa|Merci, tes mains sont restées ouvertes.",
        "maman|La haie a gardé l'eau, pas le carton.",
        "narrateur|L'ovale est clair, le thym trop loin.",
        "narrateur|La lune n'a presque plus d'arc, ou si fin.",
        "narrateur|Le verre ne fume plus du tout.",
    ),
    (3, 2, 3): L(
        "narrateur|L'odeur tiède a gagné le seuil.",
        "narrateur|La lune n'a plus de goutte au fil.",
        "enfant-f|J'ai attendu qu'il finisse le seau.",
        "maman|Merci, surtout ce moment-là.",
        "papa|Le portillon a ouvert la soupe, pas l'eau.",
        "narrateur|L'ovale montre des chaînes immobiles, minuscules.",
        "narrateur|Plus de seau dans le cadre.",
        "narrateur|L'assiette attend, ronde, sans buée.",
    ),
    (3, 3, 1): L(
        "narrateur|Deux places, au parc.",
        "narrateur|Ici, une chaise.",
        "narrateur|La lune a un croissant, sur le fil.",
        "enfant-f|Aniss a dit non.",
        "enfant-f|J'ai lâché.",
        "papa|Merci d'écouter le non, et de le dire.",
        "maman|Le banc a rendu vos deux places.",
        "narrateur|L'ovale n'a plus de chaîne, plus de doudou.",
        "narrateur|Le carton suffit, blanc et marqué.",
        "narrateur|La soupe tourne, lentement, dans la casserole.",
    ),
    (3, 3, 2): L(
        "narrateur|Nina a ouvert la main, à la haie.",
        "narrateur|Elle l'ouvre ici, au-dessus de la table.",
        "enfant-f|Le rond est parti.",
        "enfant-f|Le croissant reste.",
        "maman|Merci pour le lâcher, raconté sans trop.",
        "papa|La feuille a rendu le fil, tu n'as pas tiré.",
        "narrateur|L'ovale est clair, presque un sourire de verre.",
        "narrateur|Plus de gris de doudou dans le cadre.",
        "narrateur|Le sel, la lune, le couvercle : trois ronds sages.",
    ),
    (3, 3, 3): L(
        "narrateur|Le portillon a crié, poli, puis plus rien.",
        "narrateur|La lune suit Nina, sans se pousser.",
        "enfant-f|Surtout le non.",
        "papa|Merci, on l'écoute.",
        "maman|Deux balançoires vides, et toi ici.",
        "narrateur|L'ovale encadre le parc, sans place volée.",
        "narrateur|Le fil d'argent reste libre, sans nœud.",
        "narrateur|Le croissant d'eau est une marque, à présent.",
    ),
}


SONS = {
    "CHK_T0000_P0000": "casserole,vitre",
    "CHK_T0001_P0001": "sable,portillon",
    "CHK_T0001_P0002": "toboggan,metal",
    "CHK_T0001_P0003": "chaine,balancoire",
}

SONS_T2 = {1: "ballon", 2: "eau,seau", 3: "tissu"}
SONS_T3 = {1: "banc", 2: "haie,feuilles", 3: "portillon,soupe"}
SONS_FIN = {1: "assiette,soupe", 2: "vitre,silence", 3: "porte,casserole"}

QMETA = {
    1: qf(
        "sable",
        "sable | le sable | du sable | sable du bac",
        "Un nuage beige a touché le carton. Qu'est-ce qui a giclé ?",
        "Oui, c'était le sable.",
    ),
    2: qf(
        "fil",
        "fil | le fil | fil d'argent | le fil d'argent | argent",
        "Un bruit trop fort a couru sur la rampe. Qu'est-ce qui a frotté ?",
        "Oui, c'était le fil.",
    ),
    3: qf(
        "chaîne",
        "chaîne | la chaîne | chaine | la chaine | balançoire",
        "Un son a recouvert la voix. Qu'est-ce qui grinçait ?",
        "Oui, c'était la chaîne.",
    ),
}


def build() -> tuple[dict, dict, dict]:
    s: dict[str, list[str]] = {
        "CHK_T0000_P0000": DEBUT,
        "CHK_T0001_P0000": T1Q,
    }
    sons: dict[str, str] = dict(SONS)
    extras: dict[str, dict] = {
        "CHK_T0001_P0000": t3("le bac à sable", "le toboggan", "les balançoires"),
    }
    for i in (1, 2, 3):
        p = f"CHK_T0001_P000{i}"
        s[p] = T1[i]
        s[f"{p}_Q0001"] = Q1[i]
        extras[f"{p}_Q0001"] = QMETA[i]
        s[f"{p}_C0001"] = C1[i]
        s[f"{p}_T0002_P0000"] = T2Q[i]
        extras[f"{p}_T0002_P0000"] = t3("le ballon", "le seau", "le doudou")
        for j in (1, 2, 3):
            p2 = f"{p}_T0002_P000{j}"
            s[p2] = T2[(i, j)]
            sons[p2] = SONS_T2[j]
            s[f"{p2}_T0003_P0000"] = T3Q[j]
            extras[f"{p2}_T0003_P0000"] = t3("le banc", "la haie", "le portillon")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = t3_body(i, j, k)
                sons[p3] = SONS_T3[k]
                s[f"{p3}_F0001"] = FINS[(i, j, k)]
                sons[f"{p3}_F0001"] = SONS_FIN[k]
    return s, sons, extras


def path_words(scripts: dict) -> list[int]:
    counts = []
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            for k in (1, 2, 3):
                ids = [
                    "CHK_T0000_P0000",
                    "CHK_T0001_P0000",
                    f"CHK_T0001_P000{i}",
                    f"CHK_T0001_P000{i}_Q0001",
                    f"CHK_T0001_P000{i}_C0001",
                    f"CHK_T0001_P000{i}_T0002_P0000",
                    f"CHK_T0001_P000{i}_T0002_P000{j}",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}",
                    f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001",
                ]
                n = 0
                for cid in ids:
                    for ln in scripts[cid]:
                        n += words(ln.split("|", 1)[1])
                counts.append(n)
    return counts


def write_tree(scripts: dict, sons: dict, extras: dict) -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")
    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        scale, rate = (1.28, "slow") if kind in ("passage_question", "transition_question") else (1.22, "medium")
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), scale, rate)
        if cid in extras:
            nc.update(extras[cid])
        voice(nc, profile_for(cid, kind), extra_note=f"chunk={cid}")
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = "Nina, Aniss, papa, maman"
    out["setting"] = "cuisine embuée, puis le parc derrière la haie"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "tout doux",
        "tout calme",
        "il faut demander",
        "on doit demander",
        "bravo. tu as",
        "bon travail",
        "papa sourit",
        "maman sourit",
        "aujourd'hui,",
        "j'ai compris",
        "mission accomplie",
        "maîtresse",
        "maitresse",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan: {bad}")
    for tic in ("encore", "déjà"):
        if tic in blob:
            raise SystemExit(f"{SID} tic: {tic}")
    fins = [c["text"] for c in out["chunks"] if c.get("kind") == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"{SID} fins distinctes: {len(set(fins))}/{len(fins)}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    counts = path_words(scripts)
    if min(counts) < 520 or max(counts) > 760:
        raise SystemExit(f"{SID} chemins {min(counts)}–{max(counts)} hors 520–760")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"chemins {min(counts)}–{max(counts)} mots, moy {sum(counts)//len(counts)}")


def main() -> None:
    s, n, e = build()
    write_tree(s, n, e)
    counts = path_words(s)
    relecture(
        SID,
        TITLE,
        "Le couvercle de la soupe s'arrondit dans la vitre embuée. Nina trace "
        "un rond : un croissant d'eau tient en bas. Elle veut porter sa lune "
        "de carton au parc derrière la haie. Aniss veut le toboggan, elle le "
        "bac. Elle crie trop tôt, le fil s'accroche à la salière, la lune "
        "penche. Bac (sable, rivière contre cratère), toboggan (fil sur la "
        "rampe) ou balançoires (chaîne qui recouvre) changent l'obstacle. "
        "Ballon, seau ou doudou : deuxième ruse, personne ne donne la "
        "réponse, le croissant d'eau revient. Banc, haie ou portillon : "
        "écoute réelle, puis le difficile se raconte. 27 fins : l'ovale "
        "à la vitre, le carton garde le croissant.",
        "P1 F-NAR-019 example4 v2. N2≤15. COL.ECO.001 vécu (tours de parole, "
        "raconter le serré). Nina, Aniss, papa, maman. Monde ≠ TREE-COL-018 "
        "(rond de soleil tapis) ≠ TREE-COL-028 (cartable jaune). T3 Tom/Léa/"
        "Sami → banc/haie/portillon. TTS par fonction (raw.js) : opening/"
        "choice/clue/confirm/action/obstacle/resolution/ending. 86 chunks, "
        f"27 fins distinctes, chemins {min(counts)}–{max(counts)} mots. "
        "Pas apply. Pas audio.",
    )


if __name__ == "__main__":
    main()
