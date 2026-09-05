#!/usr/bin/env python3
"""TREE-COL-029 — Le foin et le gilet d'école (F-NAR-019, N3, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "TREE-COL-029"
LIM = LIMITS["N3"]

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=500, sentence=260, energy="warm", contour="storytelling",
        noise=0.36, emphasis="paille d'or",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le nid doit exister avant la nuit; tempo=naturel; sourire=léger; respiration=ample",
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
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qui_vient_d_arriver; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=450, sentence=280, energy="bright", contour="falling",
        noise=0.34, emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=soulagement_discret; intensite=1; destinataire=enfant; sous_texte=la_parole_a_une_place; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=420, sentence=250, energy="lively", contour="dynamic",
        noise=0.37, emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=le_nid_n_attend_pas; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0,
        pause=520, sentence=300, energy="tense", contour="dynamic",
        noise=0.34, emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=les_mots_doivent_arriver_entiers; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=560, sentence=270, energy="bright", contour="falling",
        noise=0.35, emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=regarder_puis_parler_a_ouvert_le_chemin; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3,
        pause=900, sentence=340, energy="calm", contour="falling",
        noise=0.31, emphasis=None,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_paille_d_or_a_trouvé_sa_place; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def L(*rows: str) -> list[str]:
    out = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        parts = re.split(r"(?<=[.?!])\s+", ph)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if not part.endswith((".", "?", "!")):
                part += "."
            n = words(part)
            if n > LIM:
                raise SystemExit(f"{n}>{LIM}: {part}")
            marks = part.count(".") + part.count("?") + part.count("!")
            if marks != 1:
                raise SystemExit(f"ponctuation {marks}: {part}")
            out.append(f"{role}|{part}")
    return out


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emph = m.get("emphasis")
    if emph:
        e = esc(emph)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">{body}</prosody><break time="{m["pause"]}ms"/></speak>'


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
    if extra:
        m.update({k: v for k, v in extra.items() if k in m or k == "emphasis"})
        if extra.get("emphasis") is not None:
            m["emphasis"] = extra["emphasis"]
    pause_before = (extra or {}).get("pause_before", 0)
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


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


# --- T1 ---
T1 = {
    1: dict(
        nom="le bac à sable",
        sons="sable,linge",
        q_ans="maman",
        q_acc="maman | papa | raconter | dire | ventre",
        q_retry="Sarah attend le linge. Elle parle à qui ?",
        emph="sable",
        passage=L(
            "narrateur|Sarah s'assoit au bord du bac à sable.",
            "narrateur|Le sable est frais, un peu humide.",
            "narrateur|Des brins de foin y dorment, tout crochus.",
            "narrateur|Elle tente un nid, sable et foin mêlés.",
            "narrateur|Le tas s'écroule. Un trou reste, vide.",
            "enfant-f|Ça ne tient pas.",
            "narrateur|Maman secoue un drap rayé, trop fort.",
            "enfant-f|Maman, à l'école, une voix…",
            "narrateur|Le drap claque. Les mots s'envolent.",
            "narrateur|Sarah referme la bouche. Ses joues chauffent.",
            "narrateur|Elle pose deux doigts sur le coude de maman.",
            "narrateur|Elle attend que le drap retombe.",
            "maman|Je t'écoute, là. Le drap s'est tu.",
            "enfant-f|Une voix a parlé tout bas, trop près.",
            "enfant-f|Mon ventre s'est serré, comme une corde.",
            "maman|Merci d'avoir attendu que je t'entende.",
            "narrateur|Papa pose le panier. Un œuf tremble.",
            "papa|On cherche le nid ensemble, alors ?",
        ),
        question=L(
            "narrateur|Le drap s'est tu, près du sable.",
            "papa|Sarah a parlé à qui ?",
        ),
        confirm=L(
            "enfant-f|À maman. Puis à papa.",
            "maman|Oui. Les mots sont arrivés entiers.",
            "narrateur|Sarah souffle. Le sable reste frais.",
            "narrateur|Un brin de foin dresse une petite virgule.",
            "papa|Le nid peut recommencer, plus loin.",
            "enfant-f|Pas toute seule, cette fois.",
        ),
    ),
    2: dict(
        nom="le toboggan",
        sons="metal,vent",
        q_ans="secret",
        q_acc="secret | ventre | voix | raconter | papa",
        q_retry="Sarah est redescendue. Que veut-elle dire ?",
        emph="toboggan",
        passage=L(
            "narrateur|Sarah grimpe les marches du toboggan.",
            "narrateur|Le métal est tiède, un peu pâle.",
            "narrateur|Une botte de foin lui barre les genoux.",
            "narrateur|En haut, le pré s'ouvre jusqu'au hangar.",
            "enfant-f|Papa ! Je vois où dormirait le nid !",
            "narrateur|Le vent prend le foin, puis les mots.",
            "narrateur|Le tas glisse, jaune, jusqu'au sable.",
            "papa|Je tiens le côté. Tu disais nid ?",
            "narrateur|Sarah descend. Ses paumes piquent.",
            "narrateur|Elle attend que papa baisse les yeux.",
            "enfant-f|Pas seulement un nid.",
            "enfant-f|Une voix a parlé tout bas, à l'école.",
            "enfant-f|Mon ventre n'a pas aimé.",
            "papa|Là, je t'entends. Merci, Sarah.",
            "maman|Le foin attend en bas, éparpillé.",
            "narrateur|Le gilet a une poussière de métal.",
        ),
        question=L(
            "narrateur|Sarah est redescendue, les paumes tièdes.",
            "maman|Que veut-elle dire, maintenant ?",
        ),
        confirm=L(
            "enfant-f|Le secret. Et le ventre serré.",
            "papa|Oui. On a toute la phrase, cette fois.",
            "narrateur|Sarah essuie ses paumes sur le foin.",
            "narrateur|Les brins sentent le soleil du pré.",
            "maman|On ramasse, puis on cherche ensemble.",
            "enfant-f|Je ne crie plus du haut.",
        ),
    ),
    3: dict(
        nom="les balançoires",
        sons="corde,herbe",
        q_ans="raconter",
        q_acc="raconter | parler | dire | ventre | arrêter",
        q_retry="Sarah a posé les pieds. Elle fait quoi ?",
        emph="balançoire",
        passage=L(
            "narrateur|Sarah s'assoit sur la balançoire de bois.",
            "narrateur|La corde est rêche, un peu tiède.",
            "narrateur|Le foin repose sur ses genoux, trop haut.",
            "narrateur|La planche avance. Le foin bascule.",
            "enfant-f|Maman, une voix… a dit… un nid…",
            "narrateur|Les mots sautent, coupés par la corde.",
            "maman|J'entends des bouts. J'aimerais le milieu.",
            "narrateur|Sarah plante les talons dans l'herbe.",
            "narrateur|La planche s'arrête. Le foin reste.",
            "enfant-f|Une voix a parlé tout bas, à l'école.",
            "enfant-f|Elle a dit : ne dis rien.",
            "enfant-f|Mon ventre s'est serré tout de suite.",
            "maman|Je t'écoute jusqu'au bout, maintenant.",
            "papa|Merci d'avoir arrêté la planche.",
            "narrateur|Une alouette passe, loin, vers le saule.",
            "narrateur|Le gilet ne claque plus.",
        ),
        question=L(
            "narrateur|Les talons sont dans l'herbe, immobiles.",
            "papa|Sarah a arrêté la planche pour quoi ?",
        ),
        confirm=L(
            "enfant-f|Pour raconter, sans sauter les mots.",
            "maman|Oui. On a entendu la voix, et le ventre.",
            "narrateur|Sarah pose le foin à côté de l'herbe.",
            "narrateur|Un brin reste accroché à la corde.",
            "papa|Le nid n'aime pas les phrases coupées.",
            "enfant-f|Moi non plus.",
        ),
    ),
}

# --- T2 : 9 scènes (lieu × jouet) ---
def t2_scene(t1: int, t2: int) -> list[str]:
    lieu = T1[t1]["nom"]
    if t2 == 1:  # ballon
        if t1 == 1:
            return L(
                "narrateur|Sarah prend le ballon rouge, sablé.",
                "narrateur|Elle veut marquer l'endroit du nid.",
                "narrateur|Le ballon fuit. Il roule vers le hangar.",
                "enfant-f|Je le rattrape !",
                "narrateur|L'ombre du hangar est noire, trop vite.",
                "narrateur|Sarah s'arrête. Ses pieds freinent le sable.",
                "enfant-f|Papa, je n'y vais pas toute seule.",
                "papa|Bien. On marche ensemble, alors.",
                "narrateur|Ils rejoignent le ballon, trois ombres.",
                "enfant-f|La voix a dit : derrière le hangar.",
                "maman|Tu nous le dis, maintenant. Merci.",
                "narrateur|Le ballon garde une lune de sable.",
            )
        if t1 == 2:
            return L(
                "narrateur|Sarah pose le ballon au pied du toboggan.",
                "narrateur|C'est sa cible : ici, le nid.",
                "narrateur|Le ballon rebondit, puis file au hangar.",
                "enfant-f|Il connaît le secret, lui !",
                "narrateur|Elle veut glisser pour le rattraper.",
                "narrateur|Papa lève la main, sans parler.",
                "narrateur|Sarah attend la fin de son geste.",
                "papa|On descend les marches. Moins vite.",
                "enfant-f|La voix a dit de ne pas le dire.",
                "enfant-f|Moi, je le dis. Mon ventre l'a dit d'abord.",
                "maman|On a entendu. Le hangar peut attendre.",
                "narrateur|Le ballon s'arrête contre une botte de foin.",
            )
        return L(
            "narrateur|Sarah pose le ballon sous la balançoire.",
            "narrateur|Il doit garder la place du nid.",
            "narrateur|Une poussée trop vive. Le ballon s'échappe.",
            "narrateur|Il roule sous la corde, vers le hangar.",
            "enfant-f|Je cours !",
            "maman|Attends. Tes pieds, d'abord.",
            "narrateur|Sarah pose les pieds. Puis elle part.",
            "enfant-f|La voix a dit : un nid caché, là-bas.",
            "papa|Caché, d'accord. Pas toute seule.",
            "narrateur|Le ballon se loge dans l'herbe haute.",
            "maman|Merci d'avoir posé tes pieds avant.",
            "narrateur|Une paille d'or brille sur le cuir rouge.",
        )
    if t2 == 2:  # seau
        if t1 == 1:
            return L(
                "narrateur|Sarah emplit le seau bleu de foin.",
                "narrateur|Un peu de sable tombe au fond, rêche.",
                "narrateur|Elle le lève. Le manche pèse trop.",
                "enfant-f|Je le porte derrière le hangar.",
                "narrateur|Deux pas. Le seau penche. Le foin fuit.",
                "narrateur|Sarah s'arrête. Ses bras tremblent.",
                "enfant-f|Maman, la voix a dit : cache-le là.",
                "enfant-f|Moi, je n'aime pas cacher.",
                "maman|Alors on le porte à deux.",
                "papa|Un bord chacun. Comme ça, ça tient.",
                "narrateur|Le seau sonne, creux, entre leurs mains.",
                "narrateur|Le gilet se libère d'un brin de sable.",
            )
        if t1 == 2:
            return L(
                "narrateur|Sarah glisse le seau au pied du toboggan.",
                "narrateur|Elle y pousse le foin tombé de la rampe.",
                "narrateur|Le seau sonne, trop vide, trop pressé.",
                "enfant-f|Je le fais glisser, comme moi !",
                "narrateur|Le seau dévale. Il tape le sable.",
                "papa|Le foin n'aime pas les chutes.",
                "narrateur|Sarah descend les marches, une par une.",
                "enfant-f|La voix a dit de le cacher très vite.",
                "enfant-f|Vite, ça serrait mon ventre.",
                "maman|On va, oui. Sans le jeter.",
                "narrateur|Ils reprennent le seau, tout droit.",
                "papa|Merci d'être redescendue par les marches.",
            )
        return L(
            "narrateur|Sarah pose le seau près de la balançoire.",
            "narrateur|Elle y range le foin tombé des genoux.",
            "narrateur|La corde frôle le bord. Le seau bascule.",
            "enfant-f|Il veut aller au hangar, lui aussi.",
            "maman|Le seau n'a pas de jambes.",
            "narrateur|Sarah le redresse. L'herbe sent le lait.",
            "enfant-f|La voix a dit : un nid secret, très loin.",
            "enfant-f|Loin, j'ai eu peur.",
            "papa|Alors on reste près. Et on avance.",
            "narrateur|Trois paires de mains tiennent l'anse.",
            "maman|Merci d'avoir dit loin, et peur.",
            "narrateur|Un brin de foin reste sur la corde.",
        )
    # doudou
    if t1 == 1:
        return L(
            "narrateur|Sarah prend le doudou gris, chaud d'une oreille.",
            "narrateur|Elle veut le coucher dans le nid de sable.",
            "narrateur|Le tas s'écrase. Le doudou a du sable au poil.",
            "enfant-f|Je le cache derrière le hangar, alors.",
            "narrateur|Elle fait un pas. Son ventre se serre.",
            "narrateur|Elle s'arrête. Le doudou contre sa joue.",
            "enfant-f|La voix a dit : cache, et ne dis rien.",
            "enfant-f|Moi, je dis. Il est pour le nid, pas pour le noir.",
            "maman|On t'écoute. Le doudou aussi.",
            "papa|On cherche un vrai coin, avec de la lumière.",
            "narrateur|Un grain de sable brille sur l'oreille grise.",
            "maman|Merci d'être revenue vers nous.",
        )
    if t1 == 2:
        return L(
            "narrateur|Sarah tient le doudou sur la rampe tiède.",
            "narrateur|Elle veut lui faire faire le toboggan.",
            "narrateur|Le doudou glisse. Il s'arrête dans le foin.",
            "enfant-f|Il a trouvé le secret tout seul !",
            "narrateur|Elle veut le suivre, trop vite, trop loin.",
            "papa|Sarah. On descend, et on parle.",
            "narrateur|Elle s'assoit sur la dernière marche.",
            "enfant-f|La voix a dit de le cacher dans le foin noir.",
            "enfant-f|Le foin noir, je n'aime pas.",
            "maman|Alors on prend le foin clair, près de nous.",
            "narrateur|Le doudou a une paille d'or sur le ventre.",
            "papa|Merci d'être restée sur la marche.",
        )
    return L(
        "narrateur|Sarah assied le doudou sur la planche.",
        "narrateur|La corde bouge. Le doudou bascule dans l'herbe.",
        "enfant-f|Il veut le nid secret, lui aussi.",
        "narrateur|Elle le ramasse. L'oreille sent le foin.",
        "narrateur|Elle le serre. Puis elle le montre.",
        "enfant-f|La voix a dit : c'est notre secret à deux.",
        "enfant-f|Deux, sans vous, ça me serrait.",
        "maman|À trois, alors. Ou à quatre, avec lui.",
        "papa|On cherche un nid que tout le monde voit.",
        "narrateur|Le doudou a un brin d'herbe dans la couture.",
        "maman|Merci de nous l'avoir montré.",
        "narrateur|La balançoire ne bouge plus.",
    )


T2_SONS = {1: "ballon", 2: "seau", 3: "doudou"}
T2_NOM = {1: "le ballon", 2: "le seau", 3: "le doudou"}
T3_NOM = {1: "la poule", 2: "la chèvre", 3: "le poulain"}
T3_SONS = {1: "poule,foin", 2: "clochette,foin", 3: "poulain,foin"}


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    """Climax unique : l'animal + l'objet + le lieu changent l'action."""
    lieu, jouet, animal = T1[t1]["nom"], T2_NOM[t2], T3_NOM[t3]
    if t3 == 1:  # poule
        if t2 == 1:
            return L(
                f"narrateur|Près de {lieu}, la poule picore autour du ballon.",
                "narrateur|Elle tourne. Une plume blonde reste dans l'herbe.",
                "enfant-f|La voix a dit : son œuf est à nous.",
                "narrateur|Sarah avance la main. Puis elle la retire.",
                "narrateur|Elle se baisse. Elle regarde d'abord.",
                "narrateur|Sous l'aile, un creux tiède, un œuf.",
                "papa|On ne prend pas. On pose le foin à côté.",
                "narrateur|Le ballon sert de borne, loin de l'œuf.",
                "maman|Elle a son nid. Nous, le nôtre.",
                "enfant-f|J'ai regardé avant la main.",
                "narrateur|La poule se recouche, cot cot, rassurée.",
                "papa|Bravo. Tu as vu, puis tu as parlé.",
            )
        if t2 == 2:
            return L(
                f"narrateur|La poule s'approche du seau, près de {lieu}.",
                "narrateur|Elle saute un peu. Un grain tombe.",
                "enfant-f|La voix a dit de prendre l'œuf, vite.",
                "narrateur|Sarah pose le seau. Elle ne plonge pas.",
                "narrateur|Elle compte les plumes, une, deux, trois.",
                "maman|Tu regardes. C'est bien.",
                "narrateur|Derrière le seau, un nid bas, un œuf chaud.",
                "papa|Le foin va autour, pas dessus.",
                "narrateur|Ils font un croissant de foin, à distance.",
                "enfant-f|Son nid à elle. Le nôtre à côté.",
                "narrateur|La poule picore le bord, puis s'installe.",
                "maman|Merci d'avoir posé le seau, pas la main.",
            )
        return L(
            f"narrateur|La poule frôle le doudou, près de {lieu}.",
            "narrateur|Elle tire un fil gris, puis recule.",
            "enfant-f|La voix a dit : cache l'œuf dans le doudou.",
            "narrateur|Sarah serre le doudou. Son ventre dit non.",
            "enfant-f|L'œuf n'est pas à cacher.",
            "narrateur|Elle pose le doudou. Elle se penche.",
            "narrateur|Un nid d'herbe, un œuf, tout près du bois.",
            "papa|Le doudou veille, loin des pattes.",
            "maman|Le foin fait un mur bas, pour le vent.",
            "enfant-f|Je n'ai rien pris. J'ai dit.",
            "narrateur|La poule s'installe. L'œuf reste à elle.",
            "papa|On a deux nids, et zéro secret lourd.",
        )
    if t3 == 2:  # chèvre
        if t2 == 1:
            return L(
                f"narrateur|La chèvre pose le nez sur le ballon, près de {lieu}.",
                "narrateur|Sa clochette sonne, courte, un peu rêche.",
                "enfant-f|La voix a dit : elle ouvre le loquet, c'est drôle.",
                "narrateur|Sarah voit le loquet, à demi tiré.",
                "narrateur|Elle n'y touche pas toute seule.",
                "enfant-f|Papa, le loquet. La voix voulait que je rie.",
                "enfant-f|Moi, je n'ai pas ri.",
                "papa|On le referme ensemble, alors.",
                "narrateur|Le ballon roule hors du passage.",
                "maman|Le foin, lui, va dans son coin à elle.",
                "narrateur|La chèvre mâche. La clochette se tait.",
                "papa|Merci d'avoir dit drôle, et pas drôle.",
            )
        if t2 == 2:
            return L(
                f"narrateur|La chèvre tire le foin du seau, près de {lieu}.",
                "narrateur|L'anse penche. La clochette s'énerve.",
                "enfant-f|La voix a dit de la laisser sortir.",
                "narrateur|Sarah voit le loquet. Elle recule d'un pas.",
                "enfant-f|Maman, je n'ouvre pas. Ça me serre.",
                "maman|On ferme. On lui donne le foin ici.",
                "narrateur|Papa rabat le loquet. Clic, net.",
                "narrateur|Sarah pose le seau contre la planche.",
                "narrateur|La chèvre mange, le poil chaud, rassuré.",
                "enfant-f|Son dîner, pas la porte.",
                "papa|Bravo. Tu as fermé la phrase, et le loquet.",
                "narrateur|Un brin de foin reste sur sa barbe.",
            )
        return L(
            f"narrateur|La chèvre mâchonne le doudou, près de {lieu}.",
            "narrateur|Un fil gris pend à sa lèvre.",
            "enfant-f|Non ! Il n'est pas à manger !",
            "narrateur|Sarah tend la main, trop vite, trop près.",
            "narrateur|Elle s'arrête. Elle appelle.",
            "enfant-f|Papa, le doudou. La voix a dit : laisse-la.",
            "papa|On échange. Du foin contre le doudou.",
            "narrateur|Maman tend le foin. La chèvre lâche le fil.",
            "narrateur|Sarah reprend le doudou, un peu mouillé.",
            "enfant-f|J'ai demandé, au lieu de tirer.",
            "maman|Merci. Le loquet, on le vérifie aussi.",
            "narrateur|Clic. La clochette redevient petite.",
        )
    # poulain
    if t2 == 1:
        return L(
            f"narrateur|Le poulain souffle, près de {lieu}, loin du ballon.",
            "narrateur|Sa crinière est en bataille, un peu claire.",
            "enfant-f|La voix a dit : agite le gilet, il court.",
            "narrateur|Le gilet claque. Le poulain recule.",
            "narrateur|Sarah s'arrête. Elle dégrafe le bouton.",
            "enfant-f|Je ne veux pas qu'il ait peur.",
            "maman|On le plie, alors. Tout petit.",
            "narrateur|Papa pose le ballon, loin des sabots.",
            "narrateur|Sarah étale le foin, plat, sans le jeter.",
            "narrateur|Le poulain avance. Son nez touche le foin.",
            "enfant-f|Il mange. Il ne court plus.",
            "papa|Merci d'avoir retiré le gilet.",
        )
    if t2 == 2:
        return L(
            f"narrateur|Le poulain renifle le seau, près de {lieu}.",
            "narrateur|Le gilet claque au vent. Il recule.",
            "enfant-f|La voix a dit de faire peur, pour rire.",
            "enfant-f|Rire, là, ça me serre.",
            "narrateur|Sarah enlève le gilet. Elle le tend à maman.",
            "maman|Je le tiens, plié, contre moi.",
            "narrateur|Papa pose le seau. Le foin dépasse, calme.",
            "narrateur|Le poulain revient. Son souffle est chaud.",
            "narrateur|Il croque. Une paille d'or bouge sur sa lèvre.",
            "enfant-f|J'ai dit le rire. Puis je l'ai arrêté.",
            "papa|Bravo. Il mange, sans courir.",
            "narrateur|Le seau reste, vide, comme une auge.",
        )
    return L(
        f"narrateur|Le poulain cligne, près du doudou, vers {lieu}.",
        "narrateur|Le gilet d'école claque, trop vif.",
        "enfant-f|La voix a dit : cache-toi, puis saute.",
        "narrateur|Sarah ne saute pas. Elle s'assoit.",
        "enfant-f|Maman, prends le gilet. Il fait trop de vent.",
        "maman|Le voilà, plié. Merci.",
        "narrateur|Sarah pose le doudou loin des sabots.",
        "narrateur|Elle aplatit le foin avec la paume.",
        "narrateur|Le poulain s'approche. Il souffle sur le foin.",
        "enfant-f|On ne saute pas sur lui.",
        "papa|On lui a laissé le temps.",
        "narrateur|Sa crinière redescend, brin par brin.",
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    """27 fins : image d'ouverture payée, détail unique."""
    table = {
        (1, 1, 1): L(
            "narrateur|Le soir pose une bande rose sur le hangar.",
            "narrateur|Le ballon, sablé, dort loin de l'œuf.",
            "enfant-f|La poule a son nid. Nous, le nôtre.",
            "maman|Ton gilet sèche sur la barrière.",
            "narrateur|La paille d'or y tient, comme une broche.",
            "papa|Les œufs du panier sont rentrés, eux.",
            "narrateur|Ça sent le lait, et un peu la craie.",
            "narrateur|Une plume blonde reste dans le sable frais.",
        ),
        (1, 1, 2): L(
            "narrateur|La clochette sonne une dernière fois, courte.",
            "narrateur|Le ballon, sablé, repose hors du passage.",
            "enfant-f|Le loquet est fermé. J'ai dit, au lieu de rire.",
            "papa|Le gilet a perdu son brin de sable.",
            "narrateur|La paille d'or brille encore sur le bois.",
            "maman|Le linge rayé ne claque plus.",
            "narrateur|La chèvre mâche, le poil tiède au vent.",
            "narrateur|Le pré redevient large, jusqu'au saule.",
        ),
        (1, 1, 3): L(
            "narrateur|Le poulain a du foin au museau, tout fin.",
            "narrateur|Le ballon, sablé, fait une lune dans l'herbe.",
            "enfant-f|Je n'ai pas agité le gilet.",
            "maman|Il est plié, près des œufs tièdes.",
            "narrateur|La paille d'or reste seule sur la barrière.",
            "papa|Son souffle a réchauffé le nid.",
            "narrateur|Le hangar cache le soleil, pas le secret.",
            "narrateur|Le sable garde une trace ronde, légère.",
        ),
        (1, 2, 1): L(
            "narrateur|Le seau, vide, penche comme une petite auge.",
            "narrateur|La poule s'est recouchée, l'œuf à elle.",
            "enfant-f|On a porté le foin à deux.",
            "papa|Ton gilet n'a plus de sable aux poches.",
            "narrateur|La paille d'or tremble, puis s'immobilise.",
            "maman|Le drap rayé dort sur la corde.",
            "narrateur|Un grain de mil brille au fond du seau.",
            "narrateur|Le lait de l'étable sent plus fort, le soir.",
        ),
        (1, 2, 2): L(
            "narrateur|Le loquet a fait clic, net, dans le bois.",
            "narrateur|Le seau reste contre la planche, sage.",
            "enfant-f|J'ai dit que ça me serrait.",
            "maman|On a fermé, et donné le foin ici.",
            "narrateur|Le gilet, secoué, reprend l'odeur du foin.",
            "papa|La paille d'or n'accroche plus personne.",
            "narrateur|La chèvre a une miette blonde à la lèvre.",
            "narrateur|Le seau sonne une fois, puis se tait.",
        ),
        (1, 2, 3): L(
            "narrateur|Le poulain boit presque dans le seau vide.",
            "narrateur|Le gilet, plié, ne claque plus du tout.",
            "enfant-f|Le rire, je l'ai arrêté.",
            "papa|Il mange. C'est mieux que courir.",
            "narrateur|La paille d'or a glissé dans le foin plat.",
            "maman|Tes poches sentent le lait, plus la craie.",
            "narrateur|Le sable a gardé deux traces de seau.",
            "narrateur|Derrière le hangar, le ciel devient prune.",
        ),
        (1, 3, 1): L(
            "narrateur|Le doudou, une oreille sablée, veille au loin.",
            "narrateur|La poule couve. L'œuf n'a pas bougé.",
            "enfant-f|Je n'ai rien caché dans le gris.",
            "maman|Tu l'as montré. Ça change tout.",
            "narrateur|Le gilet sèche, ouvert, sur la barrière.",
            "papa|La paille d'or y dort, enfin sage.",
            "narrateur|Un grain de sable brille sur l'oreille.",
            "narrateur|Le pré s'assombrit, doux comme le lait.",
        ),
        (1, 3, 2): L(
            "narrateur|Le doudou a un fil un peu mouillé, repris.",
            "narrateur|La chèvre mâche le foin, plus le gris.",
            "enfant-f|J'ai demandé, au lieu de tirer.",
            "papa|Le loquet a répondu clic.",
            "narrateur|Le gilet n'a plus de paille à l'ourlet.",
            "maman|La paille d'or est restée au bois.",
            "narrateur|La clochette fait un tout petit point.",
            "narrateur|Le sable refroidit, lisse sous la paume.",
        ),
        (1, 3, 3): L(
            "narrateur|Le doudou dort loin des sabots, dans l'herbe.",
            "narrateur|Le poulain a refermé les naseaux, rassasié.",
            "enfant-f|Je me suis assise, au lieu de sauter.",
            "maman|Le gilet, plié, tient chaud au panier.",
            "narrateur|La paille d'or reste la gardienne du bois.",
            "papa|Son souffle a fait un nid invisible.",
            "narrateur|Une oreille grise a un brin, comme une broche.",
            "narrateur|Le bac à sable garde un creux, vide et calme.",
        ),
        (2, 1, 1): L(
            "narrateur|Le toboggan refroidit. Le métal perd le soleil.",
            "narrateur|Le ballon, contre le foin, marque le nid d'à côté.",
            "enfant-f|J'ai regardé avant la main.",
            "papa|La poule a compris, elle aussi.",
            "narrateur|Le gilet a une poussière de rampe, rien de plus.",
            "maman|La paille d'or brille, plus bas, sur la barrière.",
            "narrateur|Une plume blonde voyage jusqu'à la première marche.",
            "narrateur|Les œufs du panier sont rentrés avant la nuit.",
        ),
        (2, 1, 2): L(
            "narrateur|Du haut, on verrait le loquet, fermé.",
            "narrateur|Sarah ne remonte pas. Elle reste au sable.",
            "enfant-f|Je n'ai pas ri du loquet.",
            "maman|Le ballon garde le passage, vide.",
            "narrateur|Le gilet ne claque plus contre la rampe.",
            "papa|La paille d'or a choisi la barrière.",
            "narrateur|La clochette répond, loin, une seule fois.",
            "narrateur|Le toboggan garde une feuille sèche, oubliée.",
        ),
        (2, 1, 3): L(
            "narrateur|Le poulain a quitté l'ombre du toboggan.",
            "narrateur|Le ballon reste au pied, comme une borne.",
            "enfant-f|Le gilet est plié. Il ne fait plus peur.",
            "papa|Sa crinière est redescendue.",
            "narrateur|La paille d'or accroche le bois, pas le tissu.",
            "maman|Tes paumes n'ont plus le piquant du métal.",
            "narrateur|Un brin de foin glisse encore sur la rampe.",
            "narrateur|Le hangar avale le dernier rond de soleil.",
        ),
        (2, 2, 1): L(
            "narrateur|Le seau, au pied du toboggan, fait une auge basse.",
            "narrateur|La poule picore le bord, puis s'en va couver.",
            "enfant-f|Je l'ai descendu par les marches.",
            "maman|Le foin n'a pas volé, cette fois.",
            "narrateur|Le gilet sent le métal tiède, plus la craie.",
            "papa|La paille d'or attend sur la barrière.",
            "narrateur|Un grain roule dans le seau, minuscule.",
            "narrateur|La rampe perd sa chaleur, palier par palier.",
        ),
        (2, 2, 2): L(
            "narrateur|Le seau sonne contre la dernière marche, puis s'arrête.",
            "narrateur|Le loquet, en bas, a dit clic.",
            "enfant-f|Vite, ça serrait. Lent, ça va.",
            "papa|La chèvre mange ici, pas ailleurs.",
            "narrateur|Le gilet n'a plus de foin dans le dos.",
            "maman|La paille d'or a retrouvé le bois.",
            "narrateur|Une feuille sèche descend la rampe, toute seule.",
            "narrateur|Le pré s'assombrit, large, jusqu'au saule.",
        ),
        (2, 2, 3): L(
            "narrateur|Le poulain a pris le foin du seau, sans reculer.",
            "narrateur|Le seau reste au pied du toboggan, vide.",
            "enfant-f|J'ai donné le gilet, plié.",
            "maman|Il ne claque plus. Merci.",
            "narrateur|La paille d'or brille plus bas que la rampe.",
            "papa|Son souffle a séché la poussière du métal.",
            "narrateur|Les marches gardent trois grains de foin.",
            "narrateur|Le ciel, derrière le hangar, devient prune.",
        ),
        (2, 3, 1): L(
            "narrateur|Le doudou, une paille d'or au ventre, veille en bas.",
            "narrateur|La poule couve, loin de la rampe froide.",
            "enfant-f|Le foin clair, pas le foin noir.",
            "papa|On a choisi la lumière.",
            "narrateur|Le gilet sèche sur la barrière, ouvert.",
            "maman|La vraie paille d'or est restée au bois.",
            "narrateur|La dernière marche a une oreille de poussière grise.",
            "narrateur|Ça sent le lait, plus le métal.",
        ),
        (2, 3, 2): L(
            "narrateur|Le doudou a un fil repris, encore un peu humide.",
            "narrateur|La chèvre a échangé le gris contre le foin.",
            "enfant-f|J'étais sur la marche. J'ai parlé.",
            "maman|Le loquet a entendu, lui aussi.",
            "narrateur|Le gilet n'accroche plus la rampe.",
            "papa|La paille d'or garde la barrière.",
            "narrateur|Une clochette, très loin, fait un point d'or.",
            "narrateur|Le toboggan devient gris, comme le doudou.",
        ),
        (2, 3, 3): L(
            "narrateur|Le doudou dort au pied du toboggan, loin des sabots.",
            "narrateur|Le poulain a soufflé le foin, puis mangé.",
            "enfant-f|Je n'ai pas sauté.",
            "papa|Tu t'es assise. Il est venu.",
            "narrateur|Le gilet, plié, tient chaud aux œufs.",
            "maman|La paille d'or n'a plus rien à retenir.",
            "narrateur|La rampe garde une trace de poil gris.",
            "narrateur|Le hangar ferme le jour, tout doucement.",
        ),
        (3, 1, 1): L(
            "narrateur|La balançoire ne bouge plus. La corde se tait.",
            "narrateur|Le ballon, une paille d'or au cuir, marque le nid d'à côté.",
            "enfant-f|J'ai posé les pieds, puis les mots.",
            "maman|La poule a son œuf. Nous, notre foin.",
            "narrateur|Le gilet sèche, sans claquer, sur la barrière.",
            "papa|La vraie paille d'or est restée au bois.",
            "narrateur|Une plume blonde s'accroche à la corde, légère.",
            "narrateur|L'herbe sous l'assise a repris sa forme.",
        ),
        (3, 1, 2): L(
            "narrateur|Le ballon dort dans l'herbe, sous la corde arrêtée.",
            "narrateur|Le loquet, plus loin, a dit clic.",
            "enfant-f|Je n'ai pas ri. J'ai dit.",
            "papa|La chèvre mange. La planche ne bouge plus.",
            "narrateur|Le gilet a perdu son vent de balançoire.",
            "maman|La paille d'or brille, fixe, sur la barrière.",
            "narrateur|La clochette et la corde se taisent ensemble.",
            "narrateur|Un brin d'herbe reste dans l'ourlet, oublié.",
        ),
        (3, 1, 3): L(
            "narrateur|Le poulain a quitté l'ombre de la balançoire.",
            "narrateur|Le ballon, dans l'herbe, ne roule plus.",
            "enfant-f|Le gilet est plié. Plus de claquant.",
            "maman|Il mange le foin plat, sans courir.",
            "narrateur|La paille d'or reste au bois, comme au matin.",
            "papa|Tes talons ont fait le silence.",
            "narrateur|La corde garde une poussière de crinière.",
            "narrateur|Le saule prend le dernier soleil, tout seul.",
        ),
        (3, 2, 1): L(
            "narrateur|Le seau, près de l'herbe, penche comme une auge.",
            "narrateur|La poule couve, l'œuf à elle, le foin à nous.",
            "enfant-f|Loin, j'ai eu peur. Près, ça va.",
            "papa|On a porté l'anse à trois.",
            "narrateur|Le gilet n'a plus de corde dans le dos.",
            "maman|La paille d'or tient la barrière.",
            "narrateur|Un grain brille au fond du seau, minuscule.",
            "narrateur|La planche de bois est redevenue un siège.",
        ),
        (3, 2, 2): L(
            "narrateur|Le seau reste dans l'herbe, l'anse tiède.",
            "narrateur|Le loquet a fermé la journée, clic.",
            "enfant-f|J'ai dit loin, et peur.",
            "maman|La chèvre a son foin, ici.",
            "narrateur|Le gilet sent l'herbe, plus la craie.",
            "papa|La paille d'or n'accroche plus le tissu.",
            "narrateur|La corde et la clochette se sont tues.",
            "narrateur|Un brin de foin reste sur l'assise, oublié.",
        ),
        (3, 2, 3): L(
            "narrateur|Le poulain a fini le foin du seau, près de l'herbe.",
            "narrateur|Le seau, vide, sert d'auge basse.",
            "enfant-f|Le gilet, plié, ne fait plus de vent.",
            "papa|Il a soufflé, puis mangé.",
            "narrateur|La paille d'or brille sur le bois, fixe.",
            "maman|Tes talons ont arrêté la planche, et le rire.",
            "narrateur|La corde garde un poil clair, très fin.",
            "narrateur|Le hangar avale le jour, sans secret.",
        ),
        (3, 3, 1): L(
            "narrateur|Le doudou, un brin dans la couture, veille sous la corde.",
            "narrateur|La poule couve. L'œuf n'est pas dans le gris.",
            "enfant-f|À trois, le secret n'était plus lourd.",
            "maman|Tu l'as montré. On a fait le nid à côté.",
            "narrateur|Le gilet sèche sur la barrière, ouvert.",
            "papa|La paille d'or y tient, comme une broche.",
            "narrateur|L'assise de bois a gardé un poil gris.",
            "narrateur|L'herbe a repris sa place, plate et fraîche.",
        ),
        (3, 3, 2): L(
            "narrateur|Le doudou a un fil un peu mouillé, sauvé.",
            "narrateur|La chèvre mâche le foin, la clochette petite.",
            "enfant-f|Notre secret à deux, je l'ai ouvert.",
            "papa|À quatre, avec le doudou, ça tenait.",
            "narrateur|Le gilet n'a plus de corde à l'épaule.",
            "maman|La paille d'or est restée au bois.",
            "narrateur|Le loquet, plus loin, garde son clic.",
            "narrateur|La balançoire est un siège, plus un bateau.",
        ),
        (3, 3, 3): L(
            "narrateur|Le doudou dort sous la balançoire, loin des sabots.",
            "narrateur|Le poulain a refermé les naseaux, rassasié.",
            "enfant-f|Je n'ai pas sauté. Il est venu.",
            "maman|Le gilet, plié, tient chaud au panier d'œufs.",
            "narrateur|La paille d'or brille sur la barrière, seule.",
            "papa|Le foin plat sent le lait, plus la craie.",
            "narrateur|La corde garde un souffle, puis plus rien.",
            "narrateur|Le saule, au bout du pré, ferme le jour.",
        ),
    }
    return table[(t1, t2, t3)]


def apply_voice(chunk: dict, profile: str, extra: dict | None = None) -> dict:
    fields = voice(chunk["text"], profile, extra)
    chunk.update(fields)
    return chunk


def write_tree() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    scripts: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {}
    profiles: dict[str, str] = {}
    emph: dict[str, str | None] = {}

    scripts["CHK_T0000_P0000"] = L(
        "narrateur|Une paille d'or colle au bois de la barrière.",
        "narrateur|Derrière le hangar, le coq se tait.",
        "narrateur|Ça sent le foin tiède, et le lait.",
        "narrateur|Une botte de Sarah goutte près du seau.",
        "narrateur|Une goutte tremble au bord du métal.",
        "narrateur|Le pré va jusqu'au saule, large et vert.",
        "narrateur|Maman tend un linge rayé sur la corde.",
        "narrateur|Le linge claque, puis retombe.",
        "narrateur|Papa rentre, le panier d'œufs contre le bras.",
        "narrateur|Les œufs sont chauds, blancs comme la craie.",
        "maman|Sarah, ton gilet d'école sent la classe.",
        "enfant-f|Je le garde. Il me tient chaud.",
        "papa|Le soleil glisse derrière le hangar.",
        "narrateur|En ce moment, Sarah saisit une botte de foin.",
        "enfant-f|Un nid, tout de suite, avant la nuit !",
        "narrateur|Elle tire. Le gilet accroche la barrière.",
        "narrateur|La paille d'or tremble, puis se tord.",
        "narrateur|Le foin s'échappe entre les bottes.",
        "enfant-f|Papa ! Il y a un secret dans le foin !",
        "narrateur|Une poule caquette, trop fort, trop près.",
        "papa|Un secret ? J'ai entendu poule, pas secret.",
        "enfant-f|À l'école, une voix a parlé tout bas.",
        "narrateur|Papa pose le panier. Un œuf roule.",
        "narrateur|Sarah referme la bouche. Son ventre se serre.",
        "maman|Quand le linge se tait, je t'écoute.",
        "narrateur|Le nid de foin attend, inachevé.",
    )
    sons["CHK_T0000_P0000"] = "coq,foin,linge"
    profiles["CHK_T0000_P0000"] = "opening"
    emph["CHK_T0000_P0000"] = "paille d'or"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|Sarah peut parler près du bac, du toboggan, ou des balançoires.",
        "maman|Où veux-tu qu'on t'écoute, Sarah ?",
    )
    profiles["CHK_T0001_P0000"] = "choice"
    extras["CHK_T0001_P0000"] = t3("le bac à sable", "le toboggan", "les balançoires")

    for t1, meta in T1.items():
        base = f"CHK_T0001_P000{t1}"
        scripts[base] = meta["passage"]
        sons[base] = meta["sons"]
        profiles[base] = "obstacle"
        emph[base] = meta["emph"]

        qid = f"{base}_Q0001"
        scripts[qid] = meta["question"]
        profiles[qid] = "clue"
        extras[qid] = qf(meta["q_ans"], meta["q_acc"], meta["q_retry"])

        cid = f"{base}_C0001"
        scripts[cid] = meta["confirm"]
        profiles[cid] = "confirm"

        t2q = f"{base}_T0002_P0000"
        scripts[t2q] = L(
            "narrateur|Pour porter le nid, trois choses attendent.",
            "papa|Le ballon, le seau, ou le doudou ?",
        )
        profiles[t2q] = "choice"
        extras[t2q] = t3("le ballon", "le seau", "le doudou")

        for t2 in (1, 2, 3):
            p2 = f"{base}_T0002_P000{t2}"
            scripts[p2] = t2_scene(t1, t2)
            sons[p2] = T2_SONS[t2]
            profiles[p2] = "action"
            emph[p2] = T2_NOM[t2].split()[-1]

            t3q = f"{p2}_T0003_P0000"
            scripts[t3q] = L(
                "narrateur|Un animal attend, près du foin.",
                "maman|La poule, la chèvre, ou le poulain ?",
            )
            profiles[t3q] = "choice"
            extras[t3q] = t3("la poule", "la chèvre", "le poulain")

            for t3i in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{t3i}"
                scripts[p3] = t3_scene(t1, t2, t3i)
                sons[p3] = T3_SONS[t3i]
                profiles[p3] = "resolution"
                emph[p3] = T3_NOM[t3i].split()[-1]

                fin = f"{p3}_F0001"
                scripts[fin] = fin_scene(t1, t2, t3i)
                sons[fin] = "soir,foin"
                profiles[fin] = "ending"
                emph[fin] = "paille d'or"

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

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
        apply_voice(nc, profiles[cid], extra_voice or None)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc

    out = dict(src)
    out["fil_rouge"] = (
        "Après l'école, Sarah veut un nid de foin avant la nuit. "
        "Le gilet accroche la barrière, les mots se perdent. "
        "Elle attend, raconte la voix trop basse, puis regarde avant la main. "
        "Selon le bac, le toboggan ou les balançoires, le ballon, le seau ou le doudou, "
        "la poule, la chèvre ou le poulain, le nid se fait à côté, et la paille d'or reste au bois."
    )
    out["title"] = "Le foin et le gilet d'école"
    out["characters"] = "Sarah, papa, maman"
    out["setting"] = "à la ferme, près du pré, en fin de jour"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]

    check(SID, out["age_band"], out["chunks"])

    # 27 fins distinctes + pas de fin mécanique
    fins = [c for c in out["chunks"] if c.get("kind") == "passage_fin"]
    texts = [c["text"] for c in fins]
    if len(texts) != 27:
        raise SystemExit(f"fins {len(texts)} != 27")
    if len(set(texts)) != 27:
        raise SystemExit("fins non distinctes")
    for c in fins:
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{c['chunk_id']} fin mécanique: {last}")

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for tic in ("tout doux", "tout calme", "on écoute la maîtresse", "si malaise", "voici le geste"):
        if tic in blob:
            raise SystemExit(f"tic: {tic}")
    if re.search(r"\b(tom|léa|lea|sami)\b", blob):
        raise SystemExit("prénom T3 hors troupe")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    write_tree()
    relecture(
        SID,
        "Le foin et le gilet d'école",
        "Sarah veut un nid de foin avant la nuit. Le gilet accroche la barrière ; "
        "une poule couvre le premier appel. Elle attend, raconte la voix trop basse "
        "(bac / toboggan / balançoires), porte le nid (ballon / seau / doudou), "
        "puis regarde avant la main auprès de la poule, de la chèvre ou du poulain. "
        "27 fins paient la paille d'or, le gilet, le foin et l'animal du chemin.",
        "F-NAR-019. Leçon COL.ECO.001 vécue (écouter, puis raconter si le ventre se serre), "
        "jamais dite en refrain. T3 Tom/Léa/Sami → poule/chèvre/poulain. "
        "TTS par chunk (profiles example2). N3≤16. Pas apply. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
