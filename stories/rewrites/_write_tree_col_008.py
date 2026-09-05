#!/usr/bin/env python3
"""TREE-COL-008 — La goutte au bec de l'arrosoir (F-NAR-019, N2, TTS)."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, make_chunk, words  # noqa: E402

SID = "TREE-COL-008"
N2 = LIMITS["N2"]
TITLE = "La goutte au bec de l'arrosoir"
FIL = (
    "Au mur du thym, Nina trouve l'anse chaude. Un point de rouille "
    "brille au bec : une goutte tremble juste au-dessus. Elle veut la "
    "porter à la laitue avant qu'elle tombe sur la pierre. Elle coupe "
    "papa : on n'entend que « laitue ». L'arrosoir part avec elle. "
    "Bac, toboggan ou balançoires changent l'obstacle. Ballon, seau ou "
    "doudou changent la deuxième ruse. Papa, maman ou Amir changent "
    "l'oreille. Le point de rouille paie la fin."
)
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="point de rouille",
        note="arc=installation; intention=émerveiller; emotion=envie_impatiente; intensite=1; destinataire=enfant; sous_texte=la_goutte_va_tomber_sans_oreille; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=la_goutte_attend_une_oreille; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="goutte",
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=attendre_a_ouvert_un_creux; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis="arrosoir",
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_veut_couper; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis="goutte",
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_retenue; intensite=2; destinataire=enfant; sous_texte=couper_fait_rater_l_oreille_et_la_goutte; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="point de rouille",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=le_point_de_rouille_a_guide_l_oreille; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="goutte",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_parole_a_trouve_sa_place; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def L(*rows: str) -> list[str]:
    out: list[str] = []
    prev = ""
    run = 1
    for raw in rows:
        role, ph = raw.split("|", 1)
        parts = re.findall(r".+?[.!?]", ph.strip())
        leftover = ph.strip()
        for p in parts:
            leftover = leftover.replace(p, "", 1)
        if leftover.strip():
            raise SystemExit(f"reste {leftover!r}: {ph}")
        if not parts:
            raise SystemExit(f"sans phrase: {ph}")
        for part in parts:
            part = part.strip()
            n = words(part)
            if n > N2:
                raise SystemExit(f"{n}>{N2}: {part}")
            if TICS.search(part):
                raise SystemExit(f"tic: {part}")
            if role == "narrateur":
                tok = part.split()[0].lower()
                run = run + 1 if tok == prev else 1
                prev = tok
                if run >= 4:
                    raise SystemExit(f"puces {tok}: {part}")
            else:
                prev = ""
                run = 1
            out.append(f"{role}|{part}")
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


def voice(nc: dict, profile: str, extra_note: str = "", emphasis: str | None | bool = False) -> None:
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


def note_for(cid: str, kind: str) -> str:
    if kind == "passage_debut":
        return "chunk=ouverture; envie_de_couper_des_le_mur"
    if kind == "transition_question":
        return f"chunk={cid}; pause_avant_choix"
    if kind == "passage_question":
        return f"chunk={cid}; indice_écoute"
    if cid.endswith("_C0001"):
        return "merci_vecu; oreille_ouverte"
    if "_T0002_P000" in cid and cid[-1] in "123" and "_T0003" not in cid:
        return "2e_ruse; refuse_de_foncer; point_de_rouille"
    if "_T0003_P000" in cid and cid[-1] in "123":
        return "failli; point_de_rouille_paye; plaisir_d_etre_entendu"
    if kind == "passage_fin":
        return "souvenir_unique; goutte_placee"
    return f"chunk={cid}; envie_retenue_ecoute"


# ---------------------------------------------------------------------------
# Récit
# ---------------------------------------------------------------------------

DEBUT = L(
    "narrateur|Les doigts de Nina trouvent l'anse de l'arrosoir.",
    "narrateur|Le métal est chaud, un peu rêche, contre la paume.",
    "narrateur|Au mur du thym, une abeille tourne, toute proche.",
    "narrateur|L'arrosoir penche vers la pierre, comme toujours.",
    "narrateur|Au bec, un point de rouille brille, minuscule.",
    "narrateur|Nina le fixe, sans lui donner de nom.",
    "narrateur|Une goutte ronde tremble juste au-dessus.",
    "narrateur|Ça sent la terre, et la menthe écrasée.",
    "papa|Je pose le râteau contre le mur.",
    "maman|Oui, loin des pieds.",
    "enfant-f|La laitue a soif !",
    "narrateur|Nina parle pendant papa.",
    "narrateur|Les deux voix se cognent, près du thym.",
    "papa|Tu disais laitue, Nina ?",
    "enfant-f|Porter la goutte, avant qu'elle tombe !",
    "narrateur|En ce moment, Nina serre l'anse trop vite.",
    "maman|On t'écoute après le râteau, d'accord ?",
    "enfant-f|D'accord.",
    "narrateur|Le point de rouille montre où ça penche.",
)

T1Q = L(
    "narrateur|Nina peut partir à trois coins, avec l'arrosoir.",
    "papa|Le bac à sable, le toboggan, ou les balançoires ?",
    "maman|Où portes-tu la goutte, maintenant ?",
)

T1 = {
    1: L(
        "narrateur|Nina emporte l'arrosoir vers le bac à sable.",
        "narrateur|Le bois du bord est chaud, un peu rêche.",
        "narrateur|Amir arrive, les joues roses, les mains pleines.",
        "enfant-m|Mon château a une rivière, autour !",
        "enfant-f|La goutte, la laitue, vite !",
        "narrateur|Les mots de Nina recouvrent ceux d'Amir.",
        "narrateur|Un grain de sable saute sur le bec.",
        "narrateur|Le sourire de Nina disparaît.",
        "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        "narrateur|Papa s'accroupit, à la hauteur de l'anse.",
        "papa|J'ai fini. Je t'écoute.",
        "narrateur|Nina referme la bouche. Elle attend Amir.",
        "enfant-m|La rivière, c'est pour le château.",
        "enfant-f|Moi, je porte la goutte à la laitue.",
        "papa|Merci d'avoir attendu sa phrase.",
        "narrateur|Le point de rouille reste, près du grain.",
    ),
    2: L(
        "narrateur|Nina grimpe le toboggan, l'arrosoir contre la hanche.",
        "narrateur|Le plastique est chaud, un peu glissant.",
        "narrateur|Amir parle en haut, les deux mains au bord.",
        "enfant-m|Je glisse le premier, jusqu'à l'herbe !",
        "enfant-f|Non, la goutte d'abord !",
        "narrateur|L'arrosoir penche. La goutte glisse vers la rouille.",
        "narrateur|Le sourire de Nina disparaît.",
        "narrateur|Dans sa poitrine, l'élan et la peur se bousculent.",
        "narrateur|Elle recule l'anse. Elle refuse de foncer.",
        "maman|Je m'accroupis, près des pieds.",
        "maman|Tu veux parler, ou l'écouter d'abord ?",
        "enfant-f|L'écouter. Sinon la goutte tombe.",
        "enfant-m|D'accord. Je glisse après.",
        "papa|Merci d'avoir gardé l'arrosoir droit.",
        "narrateur|Le point de rouille redevient un petit œil.",
    ),
    3: L(
        "narrateur|Nina rejoint les balançoires, l'arrosoir serré.",
        "narrateur|Les chaînes font clic, clic, dans l'air.",
        "narrateur|Amir se balance, et parle en même temps.",
        "enfant-m|Plus haut, Nina, plus haut !",
        "enfant-f|La laitue, la goutte !",
        "narrateur|Deux voix se marchent dessus. La chaîne claque.",
        "narrateur|L'arrosoir tremble. La goutte va vers la rouille.",
        "narrateur|Le sourire de Nina disparaît.",
        "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        "narrateur|Elle attend le creux, entre deux clics.",
        "papa|Je m'accroupis, à ta hauteur.",
        "maman|Tu as laissé la chaîne finir ?",
        "enfant-f|Oui. Ensuite, j'ai dit la laitue.",
        "papa|Merci d'avoir pris le creux.",
        "narrateur|Le point de rouille cligne, puis tient.",
    ),
}

Q1 = {
    1: L(
        "narrateur|Un grain a sauté sur le bec, près du bac.",
        "maman|Qu'est-ce qui tremble, au bec ?",
    ),
    2: L(
        "narrateur|Nina a reculé l'anse, sur le toboggan.",
        "papa|Qu'est-ce qu'elle porte, contre la hanche ?",
    ),
    3: L(
        "narrateur|Nina a vu un petit œil, au bec.",
        "maman|C'était quoi, ce point ?",
    ),
}

C1 = {
    1: L(
        "enfant-f|La goutte.",
        "papa|Oui, la goutte.",
        "maman|J'ai eu toute la phrase.",
        "narrateur|L'arrosoir reste droit, près du bois.",
        "enfant-f|Je la porte jusqu'à la laitue.",
        "papa|Qu'est-ce qui peut l'aider, là ?",
    ),
    2: L(
        "enfant-f|L'arrosoir.",
        "maman|Oui.",
        "papa|Il est resté droit, cette fois.",
        "narrateur|La goutte tient, au-dessus de la rouille.",
        "enfant-f|On glisse après, pas maintenant.",
        "maman|Qu'est-ce qui peut aider le bec ?",
    ),
    3: L(
        "enfant-f|La rouille.",
        "papa|Oui, le point de rouille.",
        "maman|Tu l'as vu, dans le creux.",
        "narrateur|La chaîne se tait. L'arrosoir ne tremble plus.",
        "enfant-f|La laitue attend, tout près.",
        "papa|Qu'est-ce qui peut garder la goutte ?",
    ),
}

T2Q = {
    1: L(
        "narrateur|Près du bac, trois objets attendent la goutte.",
        "maman|Le ballon, le seau, ou le doudou ?",
        "papa|Lequel prends-tu, sans bousculer le bec ?",
    ),
    2: L(
        "narrateur|Sur le toboggan, trois objets peuvent aider.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Lequel laisse la goutte aller jusqu'au bout ?",
    ),
    3: L(
        "narrateur|Sous les chaînes, trois objets gardent un creux.",
        "maman|Le ballon, le seau, ou le doudou ?",
        "papa|Lequel prends-tu, entre deux clics ?",
    ),
}

T2 = {
    (1, 1): L(
        "narrateur|Près du bac, un ballon rouge roule vers l'anse.",
        "enfant-m|Je le rattrape comme ça, avec les deux mains !",
        "enfant-f|Stop, le bec !",
        "narrateur|Sa voix recouvre le plan d'Amir.",
        "narrateur|Personne ne voit le ballon, trop près du bec.",
        "narrateur|Nina pince les lèvres. Elle refuse de foncer.",
        "narrateur|Elle regarde le bec. Le point de rouille penche.",
        "enfant-f|Quand tu as fini, le ballon touche le bec.",
        "enfant-m|Ah. J'arrête le rouge, là.",
        "papa|Tu as laissé sa phrase aller au bout.",
        "narrateur|Le ballon s'arrête. La goutte tient.",
    ),
    (1, 2): L(
        "narrateur|Amir pose son seau bleu dans le sable.",
        "narrateur|L'anse du seau accroche celle de l'arrosoir.",
        "enfant-m|Je le remplis, pour la rivière du château !",
        "enfant-f|Décroche, vite !",
        "narrateur|Elle tire pendant qu'il parle. Le bec penche.",
        "narrateur|La goutte glisse vers le point de rouille.",
        "narrateur|Nina lâche. Elle refuse de foncer.",
        "papa|Tu vois quelque chose, au bec ?",
        "enfant-f|Le point. Il penche de ce côté.",
        "enfant-m|On décroche après ma phrase, alors.",
        "narrateur|Les deux anses se séparent, sans sable sur la goutte.",
    ),
    (1, 3): L(
        "narrateur|Le doudou beige d'Amir trône sur le château.",
        "enfant-m|C'est le roi. Il a soif, lui aussi !",
        "enfant-f|La goutte, c'est pour la laitue !",
        "narrateur|L'oreille du doudou frôle le bec.",
        "narrateur|Nina veut l'enlever pendant qu'Amir parle.",
        "narrateur|Elle s'arrête. Le sourire ne revient pas.",
        "narrateur|Le point de rouille cligne, tout près de l'oreille.",
        "enfant-f|Quand tu as fini, on recule le roi.",
        "enfant-m|D'accord. Le roi va à l'ombre.",
        "maman|Tu as laissé le roi finir sa soif.",
        "narrateur|L'oreille s'éloigne. La goutte reste ronde.",
    ),
    (2, 1): L(
        "narrateur|En bas du toboggan, un ballon attend dans l'herbe.",
        "enfant-m|On glisse, et moi je l'attrape !",
        "enfant-f|L'arrosoir d'abord !",
        "narrateur|Deux voix se battent. Le plastique glisse un peu.",
        "narrateur|Le ballon remonte, trop près du bec.",
        "narrateur|Nina recule l'anse. Elle refuse de foncer.",
        "narrateur|Elle cherche le point de rouille, au bec.",
        "enfant-f|Il penche vers le ballon. On descend après.",
        "enfant-m|Je finis. Puis on pose l'arrosoir.",
        "maman|Personne n'a donné la réponse. Toi, tu as vu.",
        "narrateur|Le ballon reste dans l'herbe. La goutte tient.",
    ),
    (2, 2): L(
        "narrateur|Un seau d'eau attend au pied du toboggan.",
        "narrateur|Si l'arrosoir glisse, le seau éclabousse le bec.",
        "enfant-m|Je verse, pour faire une rivière !",
        "enfant-f|Non, ma goutte !",
        "narrateur|Son cri coupe Amir. Une vague lèche le plastique.",
        "narrateur|Nina serre l'anse, les joues chaudes.",
        "narrateur|Elle attend qu'il finisse, sans verser.",
        "papa|Tu vois le bec, Nina ?",
        "enfant-f|Le point de rouille. Il a peur de l'eau du seau.",
        "enfant-m|Alors j'arrête le versement. Toi, tu parles.",
        "narrateur|Le seau se pose. La goutte ne se mêle pas.",
    ),
    (2, 3): L(
        "narrateur|Le doudou d'Amir est assis sur la rampe.",
        "enfant-m|Il glisse avec moi, le premier !",
        "enfant-f|Il va bousculer le bec !",
        "narrateur|Elle parle trop tôt. Le doudou bascule.",
        "narrateur|Une patte frôle la goutte, presque.",
        "narrateur|Nina rattrape le tissu, puis se tait.",
        "narrateur|Elle refuse de foncer. Elle regarde le bec.",
        "enfant-f|Le point de rouille penche vers la rampe.",
        "enfant-m|Le doudou attend en bas, alors.",
        "maman|Tu as parlé pile, puis tu as écouté.",
        "narrateur|La rampe se vide. L'arrosoir redevient droit.",
    ),
    (3, 1): L(
        "narrateur|Sous la balançoire, un ballon dort dans l'herbe.",
        "enfant-m|Si je vais plus haut, je le touche du pied !",
        "enfant-f|Le bec, le bec !",
        "narrateur|Sa voix recouvre le clic de la chaîne.",
        "narrateur|Le pied d'Amir manque le ballon, et l'anse.",
        "narrateur|Nina serre l'arrosoir. Elle refuse de foncer.",
        "narrateur|Entre deux clics, elle cherche le point de rouille.",
        "enfant-f|Il penche vers le ballon. On arrête la chaîne.",
        "enfant-m|J'ai fini. J'arrête.",
        "papa|Tu as pris le creux, cette fois.",
        "narrateur|Le ballon reste. La goutte ne bouge plus.",
    ),
    (3, 2): L(
        "narrateur|Amir pose son seau sur le siège vide.",
        "enfant-m|Ça fait un poids. Ça balance tout seul !",
        "enfant-f|Le seau va taper l'arrosoir !",
        "narrateur|Elle coupe. La chaîne part, trop vite.",
        "narrateur|Le seau penche. Une larme d'eau vise le bec.",
        "narrateur|Nina s'immobilise. L'envie et la peur se bousculent.",
        "narrateur|Elle attend le clic suivant, sans parler.",
        "maman|Tu vois quelque chose, au bec ?",
        "enfant-f|Le point de rouille. Il montre le seau.",
        "enfant-m|Je retire le poids. Après, tu parles.",
        "narrateur|Le siège se vide. La goutte reste ronde.",
    ),
    (3, 3): L(
        "narrateur|Le doudou d'Amir voyage sur l'autre balançoire.",
        "enfant-m|Je lui raconte le jardin, à lui !",
        "enfant-f|À moi aussi !",
        "narrateur|Deux récits se marchent dessus. Les chaînes s'emmêlent.",
        "narrateur|Une patte du doudou frôle le bec.",
        "narrateur|Nina ferme la bouche. Elle refuse de foncer.",
        "narrateur|Elle suit le point de rouille, entre deux clics.",
        "enfant-f|Quand tu as fini de lui parler, c'est mon tour.",
        "enfant-m|Le doudou a entendu. Toi, maintenant.",
        "papa|Chacun sa chaîne. Chacun sa phrase.",
        "narrateur|Les chaînes se séparent. La goutte tient.",
    ),
}

T3Q = {
    1: L(
        "narrateur|La goutte cherche une oreille, près du ballon.",
        "maman|Papa, maman, ou Amir ?",
        "papa|Qui t'écoute jusqu'au bout, pour la laitue ?",
    ),
    2: L(
        "narrateur|Près du seau, la goutte attend une phrase entière.",
        "papa|Papa, maman, ou Amir ?",
        "maman|À qui donnes-tu le bec, sans le bousculer ?",
    ),
    3: L(
        "narrateur|Le doudou s'est reculé. Il reste une oreille.",
        "maman|Papa, maman, ou Amir ?",
        "papa|Qui finit sa phrase, avant la laitue ?",
    ),
}

T3 = {
    (1, 1, 1): L(
        "narrateur|Près du bac, papa reprend le râteau.",
        "papa|Je range le fer, loin des orteils.",
        "enfant-f|La goutte, maintenant !",
        "narrateur|Sa voix recouvre celle de papa.",
        "narrateur|L'arrosoir penche. La goutte va vers la rouille.",
        "narrateur|Nina referme la bouche. Elle refuse de foncer.",
        "enfant-f|Il penche de ce côté. On incline ailleurs.",
        "papa|Je t'écoute. Toute la phrase.",
        "narrateur|Ensemble, ils tournent l'anse, lentement.",
        "narrateur|La goutte quitte le bec, vers la laitue.",
        "narrateur|Ça a failli tomber sur le sable.",
    ),
    (1, 1, 2): L(
        "narrateur|Maman froisse une feuille de menthe, près du bac.",
        "maman|Ça sent fort, tiens.",
        "enfant-f|La laitue, pas la menthe !",
        "narrateur|Nina coupe. La feuille cache le bec un instant.",
        "narrateur|Elle s'arrête. Le point de rouille reparaît.",
        "enfant-f|Quand tu as fini de sentir, on arrose.",
        "maman|Je t'écoute. Montre-moi le bec.",
        "narrateur|Nina incline à l'opposé du point de rouille.",
        "narrateur|La goutte glisse vers une feuille de laitue.",
        "papa|Elle a failli aller sur la menthe.",
        "narrateur|Le ballon rouge reste contre le bois.",
    ),
    (1, 1, 3): L(
        "narrateur|Amir reprend l'histoire de sa rivière, près du ballon.",
        "enfant-m|Elle tourne deux fois, puis elle entre !",
        "enfant-f|Ma goutte, elle, elle entre maintenant !",
        "narrateur|Deux rivières se battent. Le bec penche.",
        "narrateur|Nina attend la fin, les lèvres pincées.",
        "enfant-m|Voilà. J'ai fini.",
        "enfant-f|Le point de rouille penche vers le château.",
        "enfant-m|On incline vers la laitue, alors.",
        "narrateur|La goutte part. Elle a failli boire le sable.",
        "papa|Tu as eu sa fin, puis la tienne.",
        "narrateur|Le château garde sa rivière, sèche.",
    ),
    (1, 2, 1): L(
        "narrateur|Papa veut vider un peu le seau, près du bac.",
        "papa|Trop d'eau pour le château, je crois.",
        "enfant-f|Pas sur ma goutte !",
        "narrateur|Elle coupe. Une larme du seau vise le bec.",
        "narrateur|Nina recule. Elle refuse de foncer.",
        "enfant-f|Le point de rouille montre le seau.",
        "papa|J'arrête. Ensuite, toi.",
        "narrateur|Ils inclinent l'arrosoir à l'opposé.",
        "narrateur|La goutte trouve la laitue, pas le seau.",
        "maman|Ça a failli se mêler, les deux eaux.",
        "narrateur|Le seau bleu reste à l'ombre du bois.",
    ),
    (1, 2, 2): L(
        "narrateur|Maman essuie le bord du seau, d'un coin de robe.",
        "maman|Il y a du sable, ici.",
        "enfant-f|Ma goutte n'a pas de sable !",
        "narrateur|Sa phrase recouvre celle de maman.",
        "narrateur|Le tissu frôle le bec. La goutte tremble.",
        "narrateur|Nina attend que la robe s'éloigne.",
        "enfant-f|Le point de rouille. On penche ailleurs.",
        "maman|Je t'écoute. Toute la phrase.",
        "narrateur|La goutte quitte le bec, nette, vers la laitue.",
        "papa|Elle a failli prendre le sable du seau.",
        "narrateur|Un cercle d'eau sèche au bord du bleu.",
    ),
    (1, 2, 3): L(
        "narrateur|Amir compte les grains dans le seau, un par un.",
        "enfant-m|Trois, quatre, cinq.",
        "enfant-f|Assez ! La laitue !",
        "narrateur|Le compte casse. L'anse du seau retombe.",
        "narrateur|Nina se tait. Elle laisse le six arriver.",
        "enfant-m|Six. J'ai fini.",
        "enfant-f|Le point de rouille penche vers tes grains.",
        "enfant-m|On arrose la laitue, pas le seau.",
        "narrateur|La goutte part. Elle a failli boire le bleu.",
        "maman|Tu as laissé le nombre aller au bout.",
        "narrateur|Le seau garde ses six grains, au sec.",
    ),
    (1, 3, 1): L(
        "narrateur|Papa ramasse le doudou tombé près du bac.",
        "papa|Il a du sable dans l'oreille.",
        "enfant-f|L'oreille, le bec, vite !",
        "narrateur|Nina parle trop tôt. L'oreille revient vers le bec.",
        "narrateur|Elle recule. Elle refuse de foncer.",
        "enfant-f|Le point de rouille. Loin de l'oreille.",
        "papa|Je le pose à l'ombre. Ensuite, toi.",
        "narrateur|Ils inclinent l'arrosoir vers la laitue.",
        "narrateur|La goutte part. Elle a failli mouiller le tissu.",
        "maman|Le roi a eu son ombre. Toi, ta phrase.",
        "narrateur|Le doudou sèche, loin du bec.",
    ),
    (1, 3, 2): L(
        "narrateur|Maman brosse l'oreille du doudou, tout bas.",
        "maman|Un grain, puis un autre.",
        "enfant-f|Ma goutte, elle, elle n'attend pas !",
        "narrateur|Deux soins se marchent dessus. Le bec penche.",
        "narrateur|Nina attend la dernière brosse.",
        "enfant-f|Le point de rouille. On penche vers la laitue.",
        "maman|Je t'écoute, maintenant.",
        "narrateur|La goutte glisse, nette, sur une feuille.",
        "papa|Elle a failli tomber sur l'oreille.",
        "enfant-m|Le roi est propre. La laitue aussi.",
        "narrateur|Une fibre beige reste au bord du bac.",
    ),
    (1, 3, 3): L(
        "narrateur|Amir chuchote au doudou, contre le château.",
        "enfant-m|Toi, tu es le roi. Elle, la porteuse.",
        "enfant-f|Moi, je parle maintenant !",
        "narrateur|Le chuchotis casse. Le doudou bascule.",
        "narrateur|Nina attend qu'Amir repose le roi.",
        "enfant-m|Voilà. Je t'écoute.",
        "enfant-f|Le point de rouille penche vers ton roi.",
        "narrateur|Ils tournent l'anse. La goutte va à la laitue.",
        "papa|Ça a failli arroser le château.",
        "maman|Chacun a eu sa phrase, entière.",
        "narrateur|Le roi garde l'ombre, pas l'eau.",
    ),
    (2, 1, 1): L(
        "narrateur|En bas du toboggan, papa souffle sur le ballon.",
        "papa|Il a de l'herbe, collée.",
        "enfant-f|La goutte, pas l'herbe !",
        "narrateur|Elle coupe. Le ballon roule vers le bec.",
        "narrateur|Nina pose le pied, puis se tait.",
        "enfant-f|Le point de rouille penche vers le rouge.",
        "papa|Je l'arrête. Ensuite, toute ta phrase.",
        "narrateur|Ils inclinent l'arrosoir vers la laitue du bord.",
        "narrateur|La goutte part. Elle a failli boire l'herbe.",
        "maman|Le plastique ne glisse plus.",
        "narrateur|Le ballon sèche, au pied de la rampe.",
    ),
    (2, 1, 2): L(
        "narrateur|Maman tient le ballon, pour qu'il ne remonte pas.",
        "maman|J'ai les deux mains, là.",
        "enfant-f|Et moi le bec !",
        "narrateur|Deux urgences se cognent. L'arrosoir penche.",
        "narrateur|Nina attend que maman finisse de le caler.",
        "enfant-f|Le point de rouille. On penche ailleurs.",
        "maman|Je t'écoute. Le rouge est calé.",
        "narrateur|La goutte quitte le bec, vers la laitue.",
        "papa|Elle a failli rebondir sur le ballon.",
        "narrateur|Une herbe reste collée au rouge, seule.",
        "enfant-f|Ma phrase a eu la rampe, entière.",
    ),
    (2, 1, 3): L(
        "narrateur|Amir explique sa rattrape, en bas du toboggan.",
        "enfant-m|Les deux mains, puis je roule !",
        "enfant-f|L'arrosoir, lui, il ne roule pas !",
        "narrateur|Le plan d'Amir casse. Le ballon tressaute.",
        "narrateur|Nina attend le mot roule, jusqu'au bout.",
        "enfant-m|Voilà. À toi.",
        "enfant-f|Le point de rouille penche vers tes mains.",
        "narrateur|Ils tournent l'anse. La goutte va à la laitue.",
        "papa|Ça a failli glisser avec le ballon.",
        "maman|Tu as eu sa rattrape, puis le bec.",
        "narrateur|Le rouge dort dans l'herbe, sans rebond.",
    ),
    (2, 2, 1): L(
        "narrateur|Papa soulève le seau, au pied du toboggan.",
        "papa|Je l'éloigne de la rampe.",
        "enfant-f|Ma goutte d'abord !",
        "narrateur|Elle coupe. Une vague du seau lèche le plastique.",
        "narrateur|Nina recule l'anse. Elle refuse de foncer.",
        "enfant-f|Le point de rouille a peur de ta vague.",
        "papa|J'ai fini de soulever. Je t'écoute.",
        "narrateur|Ils inclinent vers la laitue, loin du seau.",
        "narrateur|La goutte part. Elle a failli se mêler.",
        "maman|Deux eaux, deux phrases, l'une après l'autre.",
        "narrateur|Le seau pose un cercle humide, dans l'herbe.",
    ),
    (2, 2, 2): L(
        "narrateur|Maman goûte une goutte du seau, du bout du doigt.",
        "maman|Tiède, celle-là.",
        "enfant-f|La mienne est pour la laitue !",
        "narrateur|Deux gouttes se disputent. Le bec penche.",
        "narrateur|Nina attend que le doigt quitte l'eau.",
        "enfant-f|Le point de rouille. On penche vers les feuilles.",
        "maman|Je t'écoute. La mienne est rentrée.",
        "narrateur|La goutte du bec rejoint la laitue.",
        "papa|Elle a failli tomber dans le seau.",
        "narrateur|Le doigt de maman sèche, sans autre goutte.",
        "enfant-f|La rampe a eu le silence, cette fois.",
    ),
    (2, 2, 3): L(
        "narrateur|Amir veut verser le seau en rivière, sous la rampe.",
        "enfant-m|Ça part d'ici, jusqu'à l'herbe !",
        "enfant-f|Ça va prendre ma goutte !",
        "narrateur|Elle coupe. Le seau penche trop.",
        "narrateur|Nina attend qu'il le redresse.",
        "enfant-m|J'ai fini. Je ne verse pas.",
        "enfant-f|Le point de rouille montrait ta rivière.",
        "narrateur|Ils arrosent la laitue, une seule goutte.",
        "papa|Ça a failli devenir une vraie rivière.",
        "maman|Tu as laissé son idée aller au bout.",
        "narrateur|Le seau reste plein, loin de la rampe.",
    ),
    (2, 3, 1): L(
        "narrateur|Papa ramasse le doudou au pied du toboggan.",
        "papa|La rampe lui a fait un pli.",
        "enfant-f|Le pli, le bec, attention !",
        "narrateur|Nina parle trop tôt. Le tissu s'envole vers l'anse.",
        "narrateur|Elle se tait. Papa finit le pli.",
        "enfant-f|Le point de rouille penche vers le tissu.",
        "papa|Il est à l'ombre. Je t'écoute.",
        "narrateur|La goutte part vers la laitue, pas vers le pli.",
        "maman|Ça a failli mouiller le doudou.",
        "narrateur|Un pli reste dans le tissu, sec.",
        "enfant-f|Ma phrase a eu toute la rampe.",
    ),
    (2, 3, 2): L(
        "narrateur|Maman berce le doudou, en bas du toboggan.",
        "maman|Il a eu peur, sur la rampe.",
        "enfant-f|Moi aussi, pour la goutte !",
        "narrateur|Deux peurs se parlent ensemble. Le bec penche.",
        "narrateur|Nina attend la fin de la berceuse.",
        "enfant-f|Le point de rouille. On penche vers la laitue.",
        "maman|Je t'écoute. Lui, il est calmé.",
        "narrateur|La goutte glisse, nette, sur une feuille.",
        "papa|Elle a failli tomber dans le berceau.",
        "narrateur|Le doudou ferme un œil, à l'ombre.",
        "enfant-f|J'ai eu le creux, après la berceuse.",
    ),
    (2, 3, 3): L(
        "narrateur|Amir installe le doudou comme juge, au pied.",
        "enfant-m|Il dit qui glisse, lui !",
        "enfant-f|Il dit rien, c'est moi qui arrose !",
        "narrateur|Le juge bascule. Une patte vise le bec.",
        "narrateur|Nina attend qu'Amir le rassoie.",
        "enfant-m|Voilà. Le juge écoute, maintenant.",
        "enfant-f|Le point de rouille penche vers lui.",
        "narrateur|Ils inclinent ailleurs. La goutte va à la laitue.",
        "papa|Ça a failli arroser le juge.",
        "maman|Chacun a eu son rôle, entier.",
        "narrateur|Le doudou garde son siège, au sec.",
    ),
    (3, 1, 1): L(
        "narrateur|Sous les balançoires, papa cale le ballon d'un pied.",
        "papa|Comme ça, plus de rebond.",
        "enfant-f|Ma goutte, elle, elle rebondit pas !",
        "narrateur|Elle coupe. La chaîne claque. Le bec penche.",
        "narrateur|Nina attend le clic suivant, sans parler.",
        "enfant-f|Le point de rouille penche vers ton pied.",
        "papa|Le rouge est calé. Je t'écoute.",
        "narrateur|Ils tournent l'anse vers la laitue du bord.",
        "narrateur|La goutte part. Elle a failli toucher le cuir.",
        "maman|La chaîne s'est tue, juste à temps.",
        "narrateur|Le ballon dort sous le siège, sans clic.",
    ),
    (3, 1, 2): L(
        "narrateur|Maman compte les clics, pour calmer la chaîne.",
        "maman|Un, deux, trois.",
        "enfant-f|Quatre, la goutte !",
        "narrateur|Le compte se mêle. La balançoire repart.",
        "narrateur|Nina laisse maman dire quatre, seule.",
        "enfant-f|Le point de rouille. On penche ailleurs.",
        "maman|Quatre. Je t'écoute.",
        "narrateur|La goutte quitte le bec, vers la laitue.",
        "papa|Elle a failli danser avec la chaîne.",
        "narrateur|Un clic sèche dans l'air, puis plus.",
        "enfant-f|J'ai eu le creux, après le quatre.",
    ),
    (3, 1, 3): L(
        "narrateur|Amir promet au ballon un dernier élan.",
        "enfant-m|Un petit, juste un, je te jure !",
        "enfant-f|Pas d'élan, le bec !",
        "narrateur|La promesse casse. Le pied part trop tôt.",
        "narrateur|Nina attend qu'il repose le pied.",
        "enfant-m|Bon. Pas d'élan. À toi.",
        "enfant-f|Le point de rouille montrait ton élan.",
        "narrateur|Ils arrosent la laitue, loin du rouge.",
        "papa|Ça a failli partir avec la chaîne.",
        "maman|Tu as laissé sa promesse se taire.",
        "narrateur|Le ballon reste, sans élan, dans l'herbe.",
    ),
    (3, 2, 1): L(
        "narrateur|Papa descend le seau du siège, tout droit.",
        "papa|Le poids, je le pose dans l'herbe.",
        "enfant-f|Le bec, plus important !",
        "narrateur|Elle coupe. Le seau penche. Une larme vise le bec.",
        "narrateur|Nina se tait. Elle laisse le poids arriver au sol.",
        "enfant-f|Le point de rouille. Loin du seau.",
        "papa|Il est à terre. Je t'écoute.",
        "narrateur|La goutte part vers la laitue, nette.",
        "maman|Ça a failli boire la larme du seau.",
        "narrateur|Le siège vide ne balance plus.",
        "enfant-f|Ma phrase a eu toute la chaîne.",
    ),
    (3, 2, 2): L(
        "narrateur|Maman essuie le siège, là où le seau a mouillé.",
        "maman|Une trace d'eau, en forme de lune.",
        "enfant-f|Ma goutte n'est pas une lune !",
        "narrateur|Deux formes se battent. Le bec tremble.",
        "narrateur|Nina attend que le tissu quitte le bois.",
        "enfant-f|Le point de rouille. On penche vers la laitue.",
        "maman|Je t'écoute. La lune sèche.",
        "narrateur|La goutte glisse sur une feuille, ronde.",
        "papa|Elle a failli imiter la lune du siège.",
        "narrateur|La trace d'eau pâlit, puis s'en va.",
        "enfant-f|J'ai eu le creux, après la lune.",
    ),
    (3, 2, 3): L(
        "narrateur|Amir veut reposer le seau, juste un instant.",
        "enfant-m|Pour voir si ça balance, un tout petit peu.",
        "narrateur|Nina ouvre la bouche, puis la referme.",
        "enfant-m|Bon. Plus de poids.",
        "enfant-f|Le point de rouille montrait ton siège.",
        "narrateur|Ils inclinent vers la laitue, loin du bleu.",
        "papa|Ça a failli repartir, la chaîne et le seau.",
        "maman|Tu as laissé son idée se poser.",
        "narrateur|Le seau reste dans l'herbe, sans balancier.",
        "enfant-f|Ma goutte a eu le silence des chaînes.",
        "narrateur|Un clic s'éteint, puis le bec se tait.",
    ),
    (3, 3, 1): L(
        "narrateur|Papa décroche le doudou de la chaîne.",
        "papa|Il s'était accroché, par une patte.",
        "enfant-f|La patte, le bec, attention !",
        "narrateur|Nina coupe. La patte revient vers le bec.",
        "narrateur|Elle se tait. Papa finit de décrocher.",
        "enfant-f|Le point de rouille penche vers la patte.",
        "papa|Il est libre. Je t'écoute.",
        "narrateur|La goutte part vers la laitue, pas vers le tissu.",
        "maman|Ça a failli mouiller la patte.",
        "narrateur|Le doudou s'assoit dans l'herbe, loin des clics.",
        "enfant-f|Ma phrase a eu toute la chaîne, entière.",
    ),
    (3, 3, 2): L(
        "narrateur|Maman raconte au doudou le jardin, tout bas.",
        "maman|Le thym, la laitue, et toi.",
        "enfant-f|Et moi, la goutte !",
        "narrateur|Deux récits se mêlent. Les chaînes s'emmêlent.",
        "narrateur|Nina attend que maman arrive au mot toi.",
        "enfant-f|Le point de rouille. On penche vers la laitue.",
        "maman|Je t'écoute. Lui, il a eu le jardin.",
        "narrateur|La goutte glisse, nette, sur une feuille.",
        "papa|Elle a failli arroser le récit.",
        "narrateur|Le doudou garde le thym, dans une oreille sèche.",
        "enfant-f|J'ai eu le creux, après son jardin.",
    ),
    (3, 3, 3): L(
        "narrateur|Amir dit au doudou la fin de son histoire.",
        "enfant-m|Après les clics, on rentre, tous les deux.",
        "enfant-f|Après les clics, on arrose !",
        "narrateur|Deux fins se cognent. Une patte frappe le bec.",
        "narrateur|Nina attend le mot deux, jusqu'au bout.",
        "enfant-m|Voilà. Tous les deux. À toi.",
        "enfant-f|Le point de rouille penche vers ta patte.",
        "narrateur|Ils inclinent ailleurs. La goutte va à la laitue.",
        "papa|Ça a failli rentrer sans arroser.",
        "maman|Chacun a eu sa fin, entière.",
        "narrateur|Le doudou et Amir se taisent, ensemble.",
    ),
}

FINS = {
    (1, 1, 1): L(
        "narrateur|La goutte s'étale sur une feuille de laitue.",
        "enfant-f|Tu as eu toute la phrase ?",
        "papa|Toute. Le râteau est rentré, lui aussi.",
        "maman|Le point de rouille est sec, maintenant.",
        "narrateur|Le ballon rouge dort contre le bois du bac.",
        "enfant-f|Je garde le moment où j'ai parlé trop tôt.",
        "papa|Surtout celui-là.",
        "narrateur|Un grain de sable reste au bord de la feuille.",
    ),
    (1, 1, 2): L(
        "narrateur|La goutte brille sur la laitue, ronde.",
        "maman|J'ai senti la menthe, puis tes mots.",
        "papa|Le point de rouille ne penche plus.",
        "enfant-f|La feuille a eu sa soif.",
        "narrateur|Une odeur de menthe reste sur les doigts de Nina.",
        "maman|Tu raconteras le moment de la feuille ?",
        "enfant-f|Surtout celui-là.",
        "narrateur|Le ballon rouge garde l'ombre du thym.",
    ),
    (1, 1, 3): L(
        "narrateur|La goutte a choisi la laitue, pas le château.",
        "enfant-m|Ma rivière, elle, elle reste sèche.",
        "papa|Deux rivières, deux phrases.",
        "maman|Le point de rouille s'est tu.",
        "narrateur|Le château garde un fossé de sable, sans eau.",
        "enfant-f|J'ai failli couper ta fin.",
        "enfant-m|Après, j'ai entendu la tienne.",
        "narrateur|Le ballon rouge s'adosse au bois, paisible.",
    ),
    (1, 2, 1): L(
        "narrateur|La goutte repose sur la laitue, loin du seau.",
        "papa|J'ai rangé le fer. Puis j'ai eu tes mots.",
        "maman|Le point de rouille est sec.",
        "enfant-f|Les deux eaux ne se sont pas mêlées.",
        "narrateur|Le seau bleu garde un cercle d'ombre, au bac.",
        "papa|Le moment du seau, tu le gardes ?",
        "enfant-f|Surtout celui-là.",
        "narrateur|Un grain reste collé au bleu, rien de plus.",
    ),
    (1, 2, 2): L(
        "narrateur|La goutte sèche au bord d'une feuille, nette.",
        "maman|J'ai essuyé le seau. Puis je t'ai eue.",
        "papa|Le point de rouille ne tremble plus.",
        "enfant-f|Pas de sable dans ma goutte.",
        "narrateur|Un cercle d'eau pâlit sur le bleu, puis s'en va.",
        "maman|Tu raconteras le frôlement de la robe ?",
        "enfant-f|Celui-là, oui.",
        "narrateur|La menthe sent plus fort, loin du bec.",
    ),
    (1, 2, 3): L(
        "narrateur|La goutte a quitté le bec, après le six.",
        "enfant-m|Mes grains, je les ai. Toi, la laitue.",
        "papa|Le compte a eu sa fin.",
        "maman|Le point de rouille s'est éteint.",
        "narrateur|Le seau garde six grains, au sec, comme un trésor.",
        "enfant-f|J'ai failli casser ton cinq.",
        "enfant-m|Après le six, j'ai entendu.",
        "narrateur|Le bois du bac tient une ombre ronde, bleue.",
    ),
    (1, 3, 1): L(
        "narrateur|La goutte brille sur la laitue, loin du tissu.",
        "papa|Le doudou a son ombre. Toi, ta phrase.",
        "maman|Le point de rouille est sec.",
        "enfant-f|L'oreille n'a pas bu.",
        "narrateur|Une fibre beige reste au bord du bac, sèche.",
        "papa|Le moment de l'oreille, tu le dis ?",
        "enfant-f|Surtout celui-là.",
        "narrateur|Le roi dort à l'ombre, sans une perle.",
    ),
    (1, 3, 2): L(
        "narrateur|La goutte s'étale, nette, sur une feuille.",
        "maman|J'ai brossé l'oreille. Puis j'ai eu tes mots.",
        "papa|Le point de rouille ne penche plus.",
        "enfant-f|Le roi est propre. La laitue aussi.",
        "narrateur|Deux grains de sable restent dans la brosse de maman.",
        "maman|Tu gardes le moment des deux soins ?",
        "enfant-f|Celui-là, oui.",
        "narrateur|Une fibre beige brille, puis se tait.",
    ),
    (1, 3, 3): L(
        "narrateur|La goutte a choisi la laitue, pas le roi.",
        "enfant-m|Lui, l'ombre. Toi, l'eau.",
        "papa|Chacun sa phrase, entière.",
        "maman|Le point de rouille s'est tu.",
        "narrateur|Le château garde son roi, sec, contre le bois.",
        "enfant-f|J'ai failli parler pendant le chuchotis.",
        "enfant-m|Après, j'ai écouté le bec.",
        "narrateur|Une oreille beige s'endort, sans perle.",
    ),
    (2, 1, 1): L(
        "narrateur|La goutte repose sur la laitue du bord.",
        "papa|J'ai soufflé l'herbe. Puis j'ai eu tes mots.",
        "maman|Le point de rouille est sec.",
        "enfant-f|Le plastique ne glisse plus.",
        "narrateur|Une herbe reste collée au ballon, au pied de la rampe.",
        "papa|Le moment du rouge, tu le gardes ?",
        "enfant-f|Surtout celui-là.",
        "narrateur|La rampe tient une trace tiède, puis plus.",
    ),
    (2, 1, 2): L(
        "narrateur|La goutte brille, ronde, sur une feuille.",
        "maman|J'ai calé le rouge. Puis je t'ai eue.",
        "papa|Le point de rouille ne penche plus.",
        "enfant-f|Ma phrase a eu toute la rampe.",
        "narrateur|Deux mains de maman quittent le ballon, vides.",
        "maman|Tu raconteras le moment des deux urgences ?",
        "enfant-f|Celui-là, oui.",
        "narrateur|Une herbe sèche sur le rouge, seule.",
    ),
    (2, 1, 3): L(
        "narrateur|La goutte a choisi la laitue, pas le rebond.",
        "enfant-m|Ma rattrape, je l'ai dite. Toi, le bec.",
        "papa|Deux plans, l'un après l'autre.",
        "maman|Le point de rouille s'est éteint.",
        "narrateur|Le ballon dort dans l'herbe, sans rouler.",
        "enfant-f|J'ai failli couper ton mot roule.",
        "enfant-m|Après, j'ai entendu l'anse.",
        "narrateur|La rampe se tait, chaude, sans glisse.",
    ),
    (2, 2, 1): L(
        "narrateur|La goutte s'étale sur la laitue, loin du seau.",
        "papa|J'ai soulevé le bleu. Puis j'ai eu tes mots.",
        "maman|Le point de rouille est sec.",
        "enfant-f|Deux eaux, deux phrases.",
        "narrateur|Un cercle humide pâlit dans l'herbe, au pied.",
        "papa|Le moment de la vague, tu le dis ?",
        "enfant-f|Surtout celui-là.",
        "narrateur|Le plastique de la rampe redevient mat.",
    ),
    (2, 2, 2): L(
        "narrateur|La goutte du bec repose, nette, sur une feuille.",
        "maman|La mienne est rentrée. La tienne a la laitue.",
        "papa|Le point de rouille ne tremble plus.",
        "enfant-f|La rampe a eu le silence.",
        "narrateur|Le doigt de maman sèche, sans autre goutte.",
        "maman|Tu gardes le moment des deux gouttes ?",
        "enfant-f|Celui-là, oui.",
        "narrateur|Le seau garde son eau tiède, loin du bec.",
    ),
    (2, 2, 3): L(
        "narrateur|Une seule goutte a rejoint la laitue.",
        "enfant-m|Ma rivière, je l'ai gardée dans le seau.",
        "papa|L'idée a eu sa fin, sans verser.",
        "maman|Le point de rouille s'est tu.",
        "narrateur|Le seau reste plein, lourd, loin de la rampe.",
        "enfant-f|J'ai failli casser ta rivière.",
        "enfant-m|Après, j'ai entendu le bec.",
        "narrateur|Une ombre bleue s'endort au pied du toboggan.",
    ),
    (2, 3, 1): L(
        "narrateur|La goutte brille sur la laitue, loin du pli.",
        "papa|J'ai fini le tissu. Puis j'ai eu tes mots.",
        "maman|Le point de rouille est sec.",
        "enfant-f|Ma phrase a eu toute la rampe.",
        "narrateur|Un pli reste dans le doudou, sec, au pied.",
        "papa|Le moment du tissu, tu le gardes ?",
        "enfant-f|Surtout celui-là.",
        "narrateur|La rampe ne porte plus que du soleil.",
    ),
    (2, 3, 2): L(
        "narrateur|La goutte s'étale, nette, après la berceuse.",
        "maman|Lui, il est calmé. Toi, tu as été entendue.",
        "papa|Le point de rouille ne penche plus.",
        "enfant-f|J'ai eu le creux, après sa peur.",
        "narrateur|Le doudou ferme un œil, à l'ombre de la rampe.",
        "maman|Tu raconteras les deux peurs ?",
        "enfant-f|Celle du bec, surtout.",
        "narrateur|Un air de berceuse s'éteint dans l'herbe.",
    ),
    (2, 3, 3): L(
        "narrateur|La goutte a choisi la laitue, pas le juge.",
        "enfant-m|Lui, le siège. Toi, les feuilles.",
        "papa|Chacun son rôle, entier.",
        "maman|Le point de rouille s'est éteint.",
        "narrateur|Le doudou garde son siège de juge, au sec.",
        "enfant-f|J'ai failli parler à sa place.",
        "enfant-m|Après, j'ai écouté le bec.",
        "narrateur|Une patte beige s'endort, sans une goutte.",
    ),
    (3, 1, 1): L(
        "narrateur|La goutte repose sur la laitue du bord.",
        "papa|Le rouge est calé. Tes mots aussi.",
        "maman|Le point de rouille est sec.",
        "enfant-f|La chaîne s'est tue, juste à temps.",
        "narrateur|Le ballon dort sous le siège, sans clic.",
        "papa|Le moment du cuir, tu le dis ?",
        "enfant-f|Surtout celui-là.",
        "narrateur|Un dernier clic sèche dans l'air, puis plus.",
    ),
    (3, 1, 2): L(
        "narrateur|La goutte brille, ronde, après le quatre.",
        "maman|J'ai compté. Puis je t'ai eue.",
        "papa|Le point de rouille ne penche plus.",
        "enfant-f|J'ai eu le creux, après le quatre.",
        "narrateur|La chaîne reste immobile, tiède, sous les doigts.",
        "maman|Tu gardes le moment du compte mêlé ?",
        "enfant-f|Celui-là, oui.",
        "narrateur|Un clic s'est perdu, sans trouver le bec.",
    ),
    (3, 1, 3): L(
        "narrateur|La goutte a choisi la laitue, pas l'élan.",
        "enfant-m|Ma promesse, je l'ai tue. Toi, tu as arrosé.",
        "papa|Le pied est resté à terre.",
        "maman|Le point de rouille s'est tu.",
        "narrateur|Le ballon reste dans l'herbe, sans élan.",
        "enfant-f|J'ai failli casser ton serment.",
        "enfant-m|Après, j'ai entendu l'anse.",
        "narrateur|Les chaînes se taisent, deux silences ronds.",
    ),
    (3, 2, 1): L(
        "narrateur|La goutte s'étale sur la laitue, loin du bleu.",
        "papa|Le poids est à terre. Tes mots aussi.",
        "maman|Le point de rouille est sec.",
        "enfant-f|Ma phrase a eu toute la chaîne.",
        "narrateur|Le siège vide ne balance plus, plus du tout.",
        "papa|Le moment de la larme, tu le gardes ?",
        "enfant-f|Surtout celui-là.",
        "narrateur|Une larme du seau sèche dans l'herbe, seule.",
    ),
    (3, 2, 2): L(
        "narrateur|La goutte glisse sur une feuille, ronde, vraie.",
        "maman|La lune du siège a séché. Toi, tu as brillé.",
        "papa|Le point de rouille ne tremble plus.",
        "enfant-f|J'ai eu le creux, après la lune.",
        "narrateur|La trace d'eau du siège a disparu.",
        "maman|Tu raconteras les deux formes ?",
        "enfant-f|Celle du bec, surtout.",
        "narrateur|Le bois du siège redevient sec, sans lune.",
    ),
    (3, 2, 3): L(
        "narrateur|La goutte a rejoint la laitue, loin du balancier.",
        "enfant-m|Mon idée, je l'ai posée. Toi, le bec.",
        "papa|La chaîne n'est pas repartie.",
        "maman|Le point de rouille s'est éteint.",
        "narrateur|Le seau reste dans l'herbe, sans balancier.",
        "enfant-f|J'ai failli parler trop tôt, un instant.",
        "enfant-m|Après, j'ai entendu le silence.",
        "narrateur|Un clic s'éteint sous les sièges, puis plus.",
    ),
    (3, 3, 1): L(
        "narrateur|La goutte brille sur la laitue, loin de la patte.",
        "papa|Le doudou est libre. Tes mots aussi.",
        "maman|Le point de rouille est sec.",
        "enfant-f|Ma phrase a eu toute la chaîne, entière.",
        "narrateur|Le doudou s'assoit dans l'herbe, loin des clics.",
        "papa|Le moment de la patte, tu le dis ?",
        "enfant-f|Surtout celui-là.",
        "narrateur|Une patte beige sèche au soleil, sans perle.",
    ),
    (3, 3, 2): L(
        "narrateur|La goutte s'étale, nette, après le jardin raconté.",
        "maman|Lui, il a eu le thym. Toi, tu as été entendue.",
        "papa|Le point de rouille ne penche plus.",
        "enfant-f|J'ai eu le creux, après son jardin.",
        "narrateur|Le doudou garde le thym, dans une oreille sèche.",
        "maman|Tu gardes le moment des deux récits ?",
        "enfant-f|Celui du bec, surtout.",
        "narrateur|Une odeur de thym reste sur le tissu, légère.",
    ),
    (3, 3, 3): L(
        "narrateur|La goutte a choisi la laitue, pas la rentrée.",
        "enfant-m|Nous, on se tait. Toi, tu as arrosé.",
        "papa|Deux fins, l'une après l'autre.",
        "maman|Le point de rouille s'est tu.",
        "narrateur|Le doudou et Amir s'assoient, sans une goutte.",
        "enfant-f|J'ai failli rentrer avec votre fin.",
        "enfant-m|Après les clics, j'ai entendu le bec.",
        "narrateur|Les chaînes pendent, immobiles, au-dessus de l'herbe.",
    ),
}

SONS = {
    "CHK_T0000_P0000": "abeille,arrosoir",
    "CHK_T0001_P0001": "sable",
    "CHK_T0001_P0002": "glisse",
    "CHK_T0001_P0003": "chaine",
}
SONS_T2 = {1: "ballon", 2: "seau", 3: "tissu"}
SONS_T3 = {1: "rateau", 2: "menthe", 3: "voix_enfant"}
SONS_FIN = {1: "laitue,silence", 2: "feuille,arrosoir", 3: "herbe,silence"}

QMETA = {
    1: qf(
        "goutte",
        "goutte | la goutte | une goutte | l'eau | eau",
        "Un grain a sauté. Qu'est-ce qui tremble, au bec ?",
        "Oui, c'est la goutte.",
    ),
    2: qf(
        "arrosoir",
        "arrosoir | l'arrosoir | un arrosoir | l'anse | anse",
        "Nina a reculé l'anse. Qu'est-ce qu'elle porte ?",
        "Oui, c'est l'arrosoir.",
    ),
    3: qf(
        "rouille",
        "rouille | la rouille | point | le point | point de rouille",
        "Nina a vu un petit œil, au bec. C'était quoi ?",
        "Oui, c'est le point de rouille.",
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
            extras[f"{p2}_T0003_P0000"] = t3("papa", "maman", "Amir")
            for k in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{k}"
                s[p3] = T3[(i, j, k)]
                sons[p3] = SONS_T3[k]
                s[f"{p3}_F0001"] = FINS[(i, j, k)]
                sons[f"{p3}_F0001"] = SONS_FIN[k]
    return s, sons, extras


def path_words(scripts: dict) -> tuple[int, int, float]:
    lengths = []
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
                lengths.append(n)
    return min(lengths), max(lengths), sum(lengths) / len(lengths)


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
        voice(nc, profile_for(cid, kind), extra_note=note_for(cid, kind))
        by[cid] = nc
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = "Nina, Amir, papa, maman"
    out["setting"] = "dans le jardin, au mur du thym"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])
    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "si malaise",
        "tout doux",
        "tout calme",
        "il faut demander",
        "on doit demander",
        "bravo. tu as",
        "bon travail",
        "papa sourit",
        "maman sourit",
        "aujourd'hui,",
        "j'ai compris !",
        "mission accomplie",
        "merle",
        "miel",
        "grand-père",
        "grand-mere",
        "grand-mère",
        "maîtresse",
        "maitresse",
        "jardinier",
        "bibliothécaire",
        "gardienne",
    ):
        if bad in blob:
            raise SystemExit(f"{SID} slogan: {bad}")
    if TICS.search(blob):
        raise SystemExit(f"{SID} tic corpus")
    fins = [c["text"] for c in out["chunks"] if c.get("kind") == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"{SID} fins distinctes: {len(set(fins))}/{len(fins)}")
    t3s = [
        c["text"]
        for c in out["chunks"]
        if c.get("kind") == "passage" and "_T0003_P000" in c["chunk_id"] and not c["chunk_id"].endswith("_P0000")
    ]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"{SID} T3 distincts: {len(set(t3s))}/{len(t3s)}")
    t2s = [
        c["text"]
        for c in out["chunks"]
        if c.get("kind") == "passage"
        and "_T0002_P000" in c["chunk_id"]
        and c["chunk_id"].endswith(("P0001", "P0002", "P0003"))
        and "_T0003" not in c["chunk_id"]
    ]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"{SID} T2 distincts: {len(set(t2s))}/{len(t2s)}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
    lo, hi, avg = path_words(scripts)
    if lo < 520 or hi > 720:
        raise SystemExit(f"{SID} chemins hors cible: {lo}–{hi} (moyenne {avg:.0f})")
    print(f"chemins {lo}–{hi} mots (moyenne {avg:.0f})")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    s, n, e = build()
    write_tree(s, n, e)
    lo, hi, avg = path_words(s)
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés. Pas d'apply.\n\n"
        "## Promesse narrative\n\n"
        "Au mur du thym, Nina trouve l'anse chaude de l'arrosoir. "
        "Un point de rouille brille au bec : une goutte tremble juste au-dessus. "
        "Elle veut la porter à la laitue avant qu'elle tombe sur la pierre. "
        "Elle coupe papa : on n'entend que « laitue ». L'arrosoir part avec elle. "
        "Bac, toboggan ou balançoires changent l'obstacle. Ballon, seau ou doudou "
        "changent la deuxième ruse. Papa, maman ou Amir changent l'oreille. "
        "Le point de rouille paie la fin.\n\n"
        "## Vécu\n\n"
        "Nina veut porter la goutte du bec jusqu'à la laitue. Première tentative : "
        "elle parle pendant papa. Bac (grain, voix d'Amir), toboggan (pente, glisse) "
        "ou balançoires (clics) changent l'échec : envie de couper, retenue, écoute. "
        "Ballon, seau ou doudou changent la ruse : si elle coupe, personne ne voit "
        "le danger. Elle refuse de foncer, retrouve le point de rouille. "
        "Papa, maman ou Amir parlent ; ça a failli ; elle attend ; la goutte part. "
        "27 fins : goutte placée, point de rouille sec, souvenir unique. "
        f"Chemins {lo}–{hi} mots (moyenne {avg:.0f}).\n\n"
        "## Vu et corrigé\n\n"
        "- Titre noyau conservé. Troupe D16 : Nina, Amir, papa, maman.\n"
        "- 86 nœuds, graphe conservé. T1/T2 libellés conservés. T3 : papa, maman, Amir "
        "(Tom/Léa/Sami hors troupe, remplacés).\n"
        "- 27 fins textuellement distinctes, 27 T3 distincts, 9 T2 distincts.\n"
        "- Première tentative échoue. Chaque choix change l'obstacle, le climax, la dernière image.\n"
        "- Indice unique dès l'ouverture : le point de rouille au bec, payé au climax.\n"
        "- Objet indispensable : l'arrosoir (anse, bec, goutte) part avec Nina.\n"
        "- Leçon COL.POL.001 vécue, non dite : laisser l'autre finir ; tours de parole.\n"
        "- Un merci vécu (T1), pas un refrain Bravo / bon travail.\n"
        "- TTS par fonction (ouverture, choix, indice, confirmation, action, obstacle, résolution, retour).\n"
        "- `slow` réservé aux choix, à l'indice et aux fins.\n"
        "- N2 ≤ 15 mots/phrase. Pas de tics « tout doux / encore / déjà / tout calme ».\n"
        "- Ouverture : doigts sur l'anse (pas les cinq gabarits v2).\n"
        "- Monde : jardin, mur du thym (≠ dalles/Raphaël, ≠ serre/Chouchou).\n"
        "- Abeille du dump conservée. Pas de merle trois notes, pas de miel, pas de gouttes-refrain.\n"
        "- P1 F-NAR-019. Pas apply. Pas audio.\n\n"
        "## Direction vocale\n\n"
        "`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, "
        "tempo, sourire, respiration. Adulte conversationnel, pas maîtresse. Tours "
        "de parole : envie de couper, retenue, écoute réelle, plaisir d'être entendu.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

