#!/usr/bin/env python3
"""TREE-COL-012 — La bâche du marché d'Aniss. F-NAR-019, N2, texte seulement."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, make_chunk, words  # noqa: E402

SID = "TREE-COL-012"
LIM = LIMITS["N2"]
ROLES = {"narrateur", "papa", "maman", "enfant-m", "enfant-f", "copain", "copine"}
TICS = ("tout doux", "tout calme", "on lève la main", "puis on parle")
TIC_WORDS = re.compile(r"\b(encore|déjà)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        note="arc=installation; intention=émerveiller; emotion=envie; intensite=1; destinataire=enfant; sous_texte=la_bâche_va_se_plier; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_phrase_est_arrivée; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=parler_trop_tôt_ne_passe_pas; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=deux_envies_au_même_instant; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=attendre_le_clic_puis_demander; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=l_oeillet_a_payé_le_début; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict, emphasis: str | None) -> str:
    body = esc(text)
    if emphasis and emphasis in text:
        e = esc(emphasis)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict, emphasis: str | None) -> str:
    body = text
    if emphasis and emphasis in body:
        body = body.replace(emphasis, f"<emphasis>{emphasis}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitch_tag"):
        body = f"<{m['pitch_tag']}>{body}</{m['pitch_tag']}>"
    pause = "[long-pause]" if m["pause"] >= 800 else ("[pause]" if m["pause"] >= 400 else "")
    return f"{body} {pause}".strip()


def L(*rows: str) -> list[str]:
    out: list[str] = []
    prev = ""
    run = 1
    for raw in rows:
        if "|" not in raw:
            raise SystemExit(f"sans | : {raw}")
        role, ph = raw.split("|", 1)
        if role not in ROLES:
            raise SystemExit(f"rôle {role}: {raw}")
        parts = re.findall(r".+?[.!?]", ph.strip())
        if not parts:
            raise SystemExit(f"sans phrase: {raw}")
        leftover = ph.strip()
        for p in parts:
            leftover = leftover.replace(p, "", 1)
        if leftover.strip():
            raise SystemExit(f"reste {leftover!r}: {raw}")
        for part in parts:
            part = part.strip()
            n = words(part)
            if n > LIM:
                raise SystemExit(f"{n}>{LIM}: {part}")
            if n == 0:
                raise SystemExit(f"vide: {raw}")
            low = part.lower()
            for tic in TICS:
                if tic in low:
                    raise SystemExit(f"tic «{tic}»: {part}")
            if TIC_WORDS.search(part):
                raise SystemExit(f"tic mot: {part}")
            if role == "narrateur":
                tok = part.split()[0].lower()
                if tok == prev:
                    run += 1
                    if run >= 4:
                        raise SystemExit(f"puces « {tok} »: {part}")
                else:
                    run = 1
                    prev = tok
            else:
                run = 1
                prev = ""
            out.append(f"{role}|{part}")
    return out


def t3labs(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


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
    if "_T0003_P000" in cid and not cid.endswith("P0000"):
        return "resolution"
    if "_T0002_P000" in cid and "T0003" not in cid:
        return "obstacle"
    return "action"


def emphasis_for(name: str, text: str) -> str:
    for w in (
        "œillet de cuivre",
        "bâche rayée",
        "s'il te plaît",
        "petit pain",
        "fromage",
        "pomme",
        "filet",
        "grelot",
        "fraise",
        "marbre",
        "bâche",
        "œillet",
    ):
        if w in text:
            return w
    return ""


def voice(nc: dict, name: str, extra: dict | None = None) -> None:
    m = PROFILES[name]
    text = nc["text"]
    emph = (extra or {}).get("emphasis")
    if emph is None:
        emph = emphasis_for(name, text)
    nc["text_ssml"] = ssml(text, m, emph or None)
    nc["text_xai_tags"] = xai(text, m, emph or None)
    nc["rate_wpm"] = m["wpm"]
    nc["rate_label"] = m["rate"]
    nc["speed_xai"] = m["speed"]
    nc["length_scale_piper"] = m["piper"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitch_ssml"]
    nc["pitch_xai_tag"] = m["pitch_tag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = emph or ""
    nc["pause_before_ms"] = (extra or {}).get("pause_before", 0)
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


# ---------------------------------------------------------------------------
# Récit
# ---------------------------------------------------------------------------

T1 = {
    1: L(
        "narrateur|Aniss pousse la porte. Un grelot tinte trop fort.",
        "narrateur|L'air sent le beurre chaud et le bois mouillé.",
        "narrateur|Le filet à anse rouge cogne le bas du comptoir.",
        "enfant-m|Un petit pain, pour moi !",
        "narrateur|Papa demande le prix au même moment.",
        "narrateur|Les deux voix se cognent sous le grelot.",
        "narrateur|Personne ne sait à qui répondre.",
        "narrateur|Aniss sent l'envie et l'inquiétude se bousculer.",
        "enfant-m|Je parlais !",
        "maman|Attends. Je m'accroupis.",
        "narrateur|Maman se met à sa hauteur, près du four.",
        "narrateur|L'œillet de cuivre cliquette, dehors, sous la bâche.",
        "papa|Quand le grelot se tait, on t'écoute.",
        "enfant-m|D'accord.",
        "narrateur|Aniss referme la bouche. Ses joues restent chaudes.",
    ),
    2: L(
        "narrateur|Aniss s'arrête sous la bâche, à l'étal des fruits.",
        "narrateur|Les caisses luisent, mouillées, d'un rouge profond.",
        "narrateur|Une fraise roule vers sa chaussure.",
        "enfant-m|Celle-là !",
        "narrateur|Il la prend sans demander, trop vite.",
        "narrateur|Maman parle du thym. Sa phrase n'est pas finie.",
        "narrateur|La fraise échappe. Elle tombe dans l'ornière.",
        "enfant-m|Non !",
        "narrateur|Le sourire d'Aniss n'est plus là.",
        "papa|On s'accroupit. On regarde.",
        "narrateur|Papa se met à sa hauteur, près de l'eau.",
        "narrateur|L'œillet de cuivre jette un éclair, au-dessus.",
        "maman|La fraise, on la laisse. On demandera.",
        "enfant-m|Mes doigts ont été trop pressés.",
        "narrateur|Le filet reste vide, contre sa jambe.",
    ),
    3: L(
        "narrateur|Aniss entre dans la fromagerie, le filet serré.",
        "narrateur|Le marbre est froid sous ses doigts.",
        "narrateur|Ça sent le lait, et un peu de cave.",
        "enfant-m|Un fromage rond, vite !",
        "narrateur|Sa voix rebondit trop fort sur le marbre.",
        "narrateur|Maman n'a pas fini de dire bonjour.",
        "narrateur|Un papier blanc glisse. Personne ne le rattrape.",
        "narrateur|Aniss se crispe. Il voulait trop vite.",
        "papa|On reprend, plus bas.",
        "narrateur|Papa s'accroupit. Le marbre lui refroidit la paume.",
        "narrateur|Dehors, l'œillet de cuivre fait un clic mince.",
        "maman|Quand c'est silencieux, ta voix arrive.",
        "enfant-m|J'ai parlé trop fort.",
        "narrateur|Il pose le filet à terre, le temps d'un souffle.",
    ),
}

Q1 = {
    1: (
        L(
            "narrateur|Quelque chose a tinté en même temps qu'Aniss.",
            "maman|Qu'est-ce qui a tinté ?",
        ),
        qf(
            "grelot",
            "grelot | le grelot | une cloche | cloche | la cloche",
            "Un bruit aigu, à la porte. C'était quoi ?",
        ),
    ),
    2: (
        L(
            "narrateur|Aniss a pris trop vite un fruit rouge.",
            "papa|Quel fruit est tombé dans l'ornière ?",
        ),
        qf(
            "fraise",
            "fraise | la fraise | une fraise | le fruit rouge",
            "Un fruit rouge a roulé. C'était quoi ?",
        ),
    ),
    3: (
        L(
            "narrateur|Les doigts d'Aniss ont touché quelque chose de froid.",
            "maman|Qu'est-ce qui était froid ?",
        ),
        qf(
            "marbre",
            "marbre | le marbre | le comptoir | comptoir froid",
            "Sous ses doigts, c'était froid. C'était quoi ?",
        ),
    ),
}

C1 = {
    1: L(
        "enfant-m|Le grelot !",
        "narrateur|Oui, le grelot de la porte.",
        "narrateur|Aniss l'a nommé quand les oreilles étaient prêtes.",
        "maman|Merci. J'ai entendu toute ta phrase.",
        "papa|On peut demander, maintenant.",
        "narrateur|Le filet attend, un peu moins léger dans sa tête.",
    ),
    2: L(
        "enfant-m|La fraise !",
        "narrateur|Oui, la fraise de l'ornière.",
        "narrateur|Aniss l'a dite sans crier par-dessus.",
        "papa|Merci. On t'a entendu jusqu'au bout.",
        "maman|Le thym a fini sa phrase, lui aussi.",
        "narrateur|Le filet frotte, prêt pour une vraie demande.",
    ),
    3: L(
        "enfant-m|Le marbre !",
        "narrateur|Oui, le marbre froid.",
        "narrateur|Aniss l'a dit tout bas, cette fois.",
        "maman|Merci. Ta voix est arrivée entière.",
        "papa|Le papier blanc, on le ramasse après.",
        "narrateur|Le filet repose, ouvert, près du lait.",
    ),
}

T2 = {
    (1, 1): L(
        "narrateur|Près de la boulangère, Nino barre le comptoir.",
        "narrateur|Il veut le dernier petit pain, tout chaud.",
        "enfant-m|Moi aussi, le pain !",
        "copain|Non, le mien !",
        "narrateur|Leurs deux doigts visent la même croûte.",
        "narrateur|La boulangère lève les yeux, puis les baisse.",
        "narrateur|Elle ne sait pas qui a parlé.",
        "narrateur|Aniss sent son cœur taper trop vite.",
        "enfant-m|C'est pour le goûter !",
        "narrateur|Nino parle en même temps, plus fort.",
        "copain|Il est pour moi, celui-là.",
        "narrateur|Le grelot tinte. L'œillet cliquette dehors.",
        "narrateur|Les deux bruits mangent les deux voix.",
        "narrateur|Le petit pain reste sur la planche.",
        "narrateur|Aniss ouvre la bouche, puis la referme.",
        "maman|Tu l'as vu, toi aussi, Nino ?",
        "papa|Un pain, deux envies.",
        "enfant-m|J'attends.",
        "narrateur|Ses mains tremblent un peu, contre le filet.",
        "narrateur|Le petit pain ne bouge pas. Le temps s'étire.",
        "narrateur|Nino respire, Aniss aussi, sans se bousculer.",
    ),
    (1, 2): L(
        "narrateur|Le voisin discute près du four, un sac à la main.",
        "narrateur|Mila, elle, veut rester dans l'air tiède.",
        "copine|On reste ici. C'est chaud.",
        "enfant-m|Moi, je veux le comptoir !",
        "narrateur|Leurs deux phrases se marchent dessus.",
        "narrateur|Le voisin rit, sans les entendre vraiment.",
        "narrateur|Aniss avance d'un pas, trop tôt.",
        "narrateur|Mila recule vers la porte, trop vite.",
        "narrateur|Le filet se coince entre leurs genoux.",
        "enfant-m|Lâche !",
        "copine|Je n'ai pas fini ma phrase.",
        "narrateur|Le sourire d'Aniss disparaît.",
        "narrateur|L'œillet de cuivre cliquette, derrière la vitre.",
        "papa|Deux envies, un seul passage.",
        "maman|On écoute Mila, puis toi.",
        "enfant-m|D'accord. J'attends.",
        "narrateur|Il serre l'anse rouge, sans tirer.",
        "narrateur|Mila n'a pas fini d'aimer le chaud.",
        "narrateur|Le passage reste étroit, un moment trop long.",
    ),
    (1, 3): L(
        "narrateur|La maîtresse choisit un petit pain doré.",
        "narrateur|Sarah tient une feuille, un dessin de four.",
        "copine|Regarde le four, il fume !",
        "enfant-m|Moi, je veux demander !",
        "narrateur|Sarah n'a pas fini. Aniss a coupé.",
        "narrateur|La maîtresse tourne la tête, perdue.",
        "narrateur|Personne ne sait qui parler.",
        "narrateur|Aniss sent ses joues brûler.",
        "enfant-m|Pardon. Continue.",
        "narrateur|Sarah reprend, puis s'arrête, surprise.",
        "copine|Tu m'as coupée.",
        "narrateur|Dehors, une goutte quitte l'œillet de cuivre.",
        "maman|On laisse finir le dessin, d'abord.",
        "papa|Après, c'est ton tour, Aniss.",
        "enfant-m|J'attends la fin.",
        "narrateur|Il pose le filet. Ses doigts se calment.",
        "narrateur|Sarah reprend le four, trait après trait.",
        "narrateur|Aniss écoute, même quand ça dure.",
    ),
    (2, 1): L(
        "narrateur|La boulangère pèse une poire, à l'étal.",
        "narrateur|Nino veut cette poire, pas une autre.",
        "copain|La poire, pour moi !",
        "enfant-m|Des fraises, dans le filet !",
        "narrateur|Deux envies, un seul plateau de fer.",
        "narrateur|La boulangère ne sait plus quoi peser.",
        "narrateur|Aniss tend le filet pendant que Nino parle.",
        "narrateur|L'anse rouge heurte la poire. Elle roule.",
        "copain|Elle part !",
        "narrateur|Aniss veut crier. Il retient le cri.",
        "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
        "narrateur|L'œillet de cuivre cliquette au-dessus des caisses.",
        "papa|La poire de Nino, d'abord ?",
        "maman|Puis tes fraises, Aniss.",
        "enfant-m|J'attends la poire.",
        "narrateur|Il tient le filet contre son ventre, immobile.",
        "narrateur|Nino cherche la poire sous le plateau.",
        "narrateur|Aniss ne parle pas, même impatient.",
    ),
    (2, 2): L(
        "narrateur|Le voisin parle du thym, tout près des caisses.",
        "narrateur|Mila, elle, veut sauter l'ornière sous la bâche.",
        "copine|La flaque, c'est un lac !",
        "enfant-m|Les fruits, d'abord !",
        "narrateur|Mila court. Aniss parle. Rien n'arrive.",
        "narrateur|Une caisse tremble. Une cerise bascule.",
        "narrateur|Le voisin n'a pas vu la cerise.",
        "enfant-m|Stop, Mila !",
        "narrateur|Sa voix coupe celle du voisin, trop tard.",
        "narrateur|L'eau de l'ornière gicle sur le filet.",
        "copine|C'est mon lac.",
        "narrateur|Aniss refuse de foncer dans l'eau.",
        "narrateur|Il lève les yeux vers l'œillet de cuivre.",
        "maman|Le lac de Mila, puis tes fruits.",
        "papa|On écoute l'un, puis l'autre.",
        "enfant-m|J'attends le lac.",
        "narrateur|L'anse rouge dégoutte, lourde, sans fruit.",
        "narrateur|Mila refait un saut, puis un autre.",
        "narrateur|Aniss reste au bord, les pieds au sec.",
    ),
    (2, 3): L(
        "narrateur|La maîtresse compte des fraises, une par une.",
        "narrateur|Sarah compte avec elle, très fort.",
        "copine|Quatre, cinq, six !",
        "enfant-m|Moi, je veux en prendre !",
        "narrateur|Le compte se casse. Personne ne sait où on en est.",
        "narrateur|La maîtresse recommence, plus bas.",
        "narrateur|Aniss ouvre la bouche, puis la referme.",
        "copine|Tu as cassé le six.",
        "enfant-m|Pardon. Continue jusqu'au bout.",
        "narrateur|Sarah reprend. Aniss écoute vraiment, cette fois.",
        "narrateur|Une goutte glisse sur l'œillet de cuivre.",
        "papa|Le compte, d'abord.",
        "maman|Puis ta demande, Aniss.",
        "enfant-m|J'attends le dernier nombre.",
        "narrateur|Le filet pend, patient, entre deux caisses.",
        "narrateur|Sarah reprend à six, plus lentement.",
        "narrateur|Aniss compte dans sa tête, sans ouvrir la bouche.",
    ),
    (3, 1): L(
        "narrateur|La boulangère sent un fromage, près du marbre.",
        "narrateur|Nino veut goûter, tout de suite.",
        "copain|Un bout, pour moi !",
        "enfant-m|Un fromage entier, pour le goûter !",
        "narrateur|Deux envies, un seul couteau de bois.",
        "narrateur|La boulangère recule le plateau, surprise.",
        "narrateur|Aniss avance la main. Nino aussi.",
        "narrateur|Leurs doigts se touchent au-dessus du blanc.",
        "copain|C'est mon bout.",
        "enfant-m|C'est mon goûter.",
        "narrateur|Les deux phrases s'écrasent sur le marbre.",
        "narrateur|Aniss retire sa main, les joues chaudes.",
        "narrateur|L'œillet de cuivre cliquette, loin, sous la bâche.",
        "papa|Le bout de Nino, d'abord ?",
        "maman|Puis ta demande, entière.",
        "enfant-m|J'attends le bout.",
        "narrateur|Il pose le filet. Le marbre lui refroidit les poignets.",
        "narrateur|Nino attend le couteau, sans le prendre.",
        "narrateur|Le fromage entier reste, hors de portée.",
    ),
    (3, 2): L(
        "narrateur|Le voisin pose son sac sur le marbre froid.",
        "narrateur|Mila veut toucher le fromage, juste un doigt.",
        "copine|Il est lisse, comme une lune.",
        "enfant-m|Moi, je veux l'acheter !",
        "narrateur|Mila n'a pas fini sa lune. Aniss a parlé.",
        "narrateur|Le voisin tourne le sac. Le papier fuit.",
        "narrateur|Personne n'écoute plus personne.",
        "enfant-m|Attends, Mila.",
        "copine|Ma lune n'était pas finie.",
        "narrateur|Aniss sent l'inquiétude lui serrer la gorge.",
        "narrateur|Il refuse de reprendre la parole tout de suite.",
        "narrateur|Une ombre d'œillet tremble sur le marbre.",
        "maman|La lune de Mila, jusqu'au bout.",
        "papa|Après, c'est à toi.",
        "enfant-m|J'écoute la lune.",
        "narrateur|Le filet reste ouvert, sans rien dedans.",
        "narrateur|Mila cherche ses mots, un peu trop longtemps.",
        "narrateur|Aniss ne les lui vole pas.",
    ),
    (3, 3): L(
        "narrateur|La maîtresse attend près du comptoir frais.",
        "narrateur|Sarah veut raconter le fromage rond.",
        "copine|Il ressemble à une roue de vélo.",
        "enfant-m|Moi, je veux le fromage !",
        "narrateur|La roue de Sarah n'a pas fini de tourner.",
        "narrateur|La maîtresse ne sait plus qui écouter.",
        "narrateur|Aniss a coupé. Ses mots tombent trop tôt.",
        "copine|Ma roue.",
        "enfant-m|Pardon. Termine.",
        "narrateur|Il se tait. Sarah reprend, plus bas.",
        "narrateur|L'œillet de cuivre fait un clic, dehors.",
        "papa|On laisse la roue arriver.",
        "maman|Puis on t'écoute, Aniss.",
        "enfant-m|J'attends la fin de la roue.",
        "narrateur|Ses mains, sur le filet, ne bougent plus.",
        "narrateur|Sarah tourne sa roue, phrase après phrase.",
        "narrateur|Aniss reste, même quand ça n'en finit plus.",
    ),
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    table = {
        (1, 1, 1): L(
            "narrateur|La boulangère saisit le papier. Le pain va partir.",
            "narrateur|Nino avance la main vers la croûte chaude.",
            "narrateur|Aniss lève la sienne, puis s'arrête.",
            "narrateur|Il regarde l'œillet de cuivre, par la vitre.",
            "narrateur|La goutte tient. Le clic n'est pas venu.",
            "enfant-m|Nino, tu finis.",
            "copain|Je veux le chaud.",
            "enfant-m|S'il te plaît. Après, je demande le mien.",
            "narrateur|Nino prend le pain. Il souffle dessus.",
            "narrateur|Derrière, une croûte plus petite attend.",
            "enfant-m|S'il te plaît, celle de derrière.",
            "papa|Là, on t'a entendu.",
            "narrateur|La petite croûte glisse dans le filet.",
            "narrateur|Ça a failli ne pas arriver.",
        ),
        (1, 1, 2): L(
            "narrateur|Une coupe de pommes dore près des croûtes.",
            "narrateur|Nino veut le pain. Aniss, une pomme.",
            "narrateur|Le soleil pousse. On plie un coin de bâche.",
            "narrateur|Aniss refuse de foncer vers le fruit.",
            "narrateur|Il écoute l'œillet. Un clic, puis le silence.",
            "enfant-m|Tu prends le pain, Nino.",
            "copain|Oui.",
            "enfant-m|S'il te plaît, une pomme, après.",
            "narrateur|La boulangère tend une pomme lisse, un peu froide.",
            "papa|Tu as parlé après le clic.",
            "narrateur|La pomme entre dans le filet, ronde.",
            "narrateur|Le coin de bâche s'arrête, à moitié plié.",
        ),
        (1, 1, 3): L(
            "narrateur|Un fromage de sandwich attend près du four.",
            "narrateur|Nino serre son pain. Le fromage va rentrer.",
            "narrateur|Aniss ouvre la bouche, puis la referme.",
            "narrateur|Il suit le fil de l'œillet, jusqu'au silence.",
            "enfant-m|S'il te plaît, le fromage, pour plus tard.",
            "copain|Moi, j'ai le chaud.",
            "narrateur|La boulangère enveloppe le blanc, sans se presser.",
            "maman|On t'a entendu, après Nino.",
            "narrateur|Le fromage pèse dans le filet, frais.",
            "narrateur|Une goutte d'œillet tombe à côté, pas dessus.",
        ),
        (1, 2, 1): L(
            "narrateur|Mila a fini sa phrase, près du four.",
            "narrateur|Le voisin range son sac. Le passage s'ouvre.",
            "narrateur|Un coin de bâche glisse vers la porte.",
            "narrateur|Aniss veut courir. Il ne court pas.",
            "narrateur|Il attend que l'œillet se taise.",
            "enfant-m|S'il te plaît, un petit pain.",
            "copine|Moi, je reste au chaud.",
            "narrateur|Deux envies, deux réponses, l'une après l'autre.",
            "papa|Le pain, pour toi. Le four, pour Mila.",
            "narrateur|Le sachet rêche rejoint le filet.",
            "narrateur|La bâche s'arrête, juste avant la poignée.",
        ),
        (1, 2, 2): L(
            "narrateur|Une pomme brille dans la vitrine, près du four.",
            "narrateur|Mila veut la chaleur. Aniss veut le fruit.",
            "narrateur|Le voisin parle trop longtemps. La pomme va partir.",
            "narrateur|Aniss écoute jusqu'au bout, même trop long.",
            "enfant-m|S'il te plaît, la pomme de la vitrine.",
            "copine|Et moi, je reste.",
            "maman|On a entendu les deux.",
            "narrateur|La pomme, froide, pose dans le filet tiède.",
            "narrateur|L'œillet cliquette, puis s'endort.",
        ),
        (1, 2, 3): L(
            "narrateur|Le voisin a un fromage, tout au fond du sac.",
            "narrateur|Aniss en voudrait un, pour le goûter.",
            "narrateur|Mila barre la porte, pour garder le chaud.",
            "narrateur|Aniss ne pousse pas. Il regarde l'œillet.",
            "enfant-m|S'il te plaît, un fromage, comme le sien.",
            "copine|Vous pouvez passer, maintenant.",
            "papa|Merci d'avoir laissé le passage.",
            "narrateur|Le papier blanc fait un bruit doux, dans le filet.",
            "narrateur|Le chaud de Mila, et le frais d'Aniss, tiennent.",
        ),
        (1, 3, 1): L(
            "narrateur|Sarah a fini son dessin de four.",
            "narrateur|La maîtresse range le petit pain doré.",
            "narrateur|Il n'en reste qu'un, plus pâle, sur la planche.",
            "narrateur|Aniss refuse de le prendre sans mot.",
            "narrateur|Il attend le clic de l'œillet, puis parle.",
            "enfant-m|S'il te plaît, le pâle.",
            "copine|Mon four est fini.",
            "maman|On t'écoute, après le dessin.",
            "narrateur|Le pâle glisse dans le filet, un peu tiède.",
            "narrateur|Sarah sourit de son côté, sans se bousculer.",
        ),
        (1, 3, 2): L(
            "narrateur|Sarah montre une pomme dessinée, à côté du four.",
            "narrateur|Une vraie pomme attend dans une coupe.",
            "narrateur|La maîtresse plie son sac. La coupe va partir.",
            "narrateur|Aniss suit l'ombre de l'œillet sur le bois.",
            "enfant-m|S'il te plaît, la vraie, pas le dessin.",
            "copine|Le dessin, c'est le mien.",
            "papa|Les deux pommes ont eu leur tour.",
            "narrateur|La vraie entre dans le filet, lisse et froide.",
            "narrateur|Le dessin reste dans la feuille de Sarah.",
        ),
        (1, 3, 3): L(
            "narrateur|Sarah a raconté le four jusqu'au bout.",
            "narrateur|Un fromage de sandwich refroidit près de la vitre.",
            "narrateur|La maîtresse tend la main. Il va disparaître.",
            "narrateur|Aniss attend. L'œillet se tait.",
            "enfant-m|S'il te plaît, le fromage de la vitre.",
            "copine|Moi, j'ai le dessin.",
            "maman|Ta phrase est arrivée entière.",
            "narrateur|Le fromage pèse, frais, dans l'anse rouge.",
            "narrateur|La vitre garde une trace ronde, un moment.",
        ),
        (2, 1, 1): L(
            "narrateur|Nino a sa poire. Le plateau se vide.",
            "narrateur|Un pain dore, posé trop près des fraises.",
            "narrateur|La boulangère le reprend. Il va rentrer.",
            "narrateur|Aniss lève les yeux. L'œillet cliquette, puis non.",
            "enfant-m|S'il te plaît, le pain, après la poire.",
            "copain|J'ai la mienne.",
            "papa|Après la poire, c'était clair.",
            "narrateur|Le pain tiède rejoint le filet, loin des fruits.",
            "narrateur|La bâche rayée claque, sans tout plier.",
        ),
        (2, 1, 2): L(
            "narrateur|Nino tient sa poire. Une pomme rouge attend.",
            "narrateur|La boulangère pousse la caisse. La pomme recule.",
            "narrateur|Aniss ne court pas. Il écoute l'œillet.",
            "enfant-m|S'il te plaît, la pomme rouge.",
            "copain|La poire, c'est autre chose.",
            "maman|Deux fruits, deux phrases, l'une après l'autre.",
            "narrateur|La pomme, froide, entre dans le filet.",
            "narrateur|Une goutte d'œillet s'écrase à côté, pas dessus.",
        ),
        (2, 1, 3): L(
            "narrateur|La poire de Nino a quitté le plateau.",
            "narrateur|Un fromage blanc repose loin des fraises.",
            "narrateur|La boulangère le couvre. Il va disparaître.",
            "narrateur|Aniss attend le silence de l'œillet.",
            "enfant-m|S'il te plaît, le fromage, loin des rouges.",
            "copain|Moi, j'ai le sucré.",
            "papa|On t'a entendu, après la poire.",
            "narrateur|Le fromage glisse dans le filet, à l'ombre.",
            "narrateur|Les fraises restent, et la bâche tient.",
        ),
        (2, 2, 1): L(
            "narrateur|Mila a sauté sa dernière flaque.",
            "narrateur|Le voisin a fini le thym.",
            "narrateur|Un pain, près des caisses, prend la pluie d'œillet.",
            "narrateur|Aniss veut le sauver trop vite. Il s'arrête.",
            "narrateur|Il parle après le clic, pas pendant.",
            "enfant-m|S'il te plaît, le pain, avant la goutte.",
            "copine|Mon lac est fini.",
            "maman|Ta phrase est arrivée au sec.",
            "narrateur|Le pain entre au filet, presque mouillé.",
            "narrateur|La goutte tombe dans l'ornière, trop tard pour lui.",
        ),
        (2, 2, 2): L(
            "narrateur|Mila s'essuie. L'ornière redevient une ornière.",
            "narrateur|Une pomme a roulé au bord de l'eau.",
            "narrateur|Le voisin va la poser plus loin, trop loin.",
            "narrateur|Aniss suit l'éclair de l'œillet, puis demande.",
            "enfant-m|S'il te plaît, la pomme du bord.",
            "copine|Pas dans mon lac.",
            "papa|Le lac, puis le fruit. C'est fait.",
            "narrateur|La pomme, un peu humide, pose dans le filet.",
            "narrateur|La bâche claque. L'eau ne l'a pas prise.",
        ),
        (2, 2, 3): L(
            "narrateur|Mila quitte la flaque. Le voisin ferme son sac.",
            "narrateur|Un fromage, trop près de l'eau, va glisser.",
            "narrateur|Aniss refuse de foncer. Il écoute l'œillet.",
            "enfant-m|S'il te plaît, le fromage, hors de l'eau.",
            "copine|Le lac n'en voulait pas.",
            "maman|On t'a entendu, les pieds au sec.",
            "narrateur|Le fromage, enveloppé, rejoint le filet rêche.",
            "narrateur|Une seule goutte brille sur le cuivre.",
        ),
        (2, 3, 1): L(
            "narrateur|Sarah a dit le dernier nombre.",
            "narrateur|La maîtresse pose les fraises. Un pain attend.",
            "narrateur|Le soleil pousse. On tire un coin de bâche.",
            "narrateur|Aniss attend que l'œillet se taise.",
            "enfant-m|S'il te plaît, le pain, après le compte.",
            "copine|Six, c'était le bout.",
            "papa|Après six, on t'écoutait.",
            "narrateur|Le pain tiède entre dans le filet.",
            "narrateur|La bâche s'arrête, un coin en l'air.",
        ),
        (2, 3, 2): L(
            "narrateur|Le compte de Sarah est fini.",
            "narrateur|Une pomme reste, hors des fraises.",
            "narrateur|La maîtresse va la remettre dans une caisse.",
            "narrateur|Aniss parle après le silence, pas pendant les nombres.",
            "enfant-m|S'il te plaît, la pomme à part.",
            "copine|Je n'ai pas compté celle-là.",
            "maman|Elle n'était pas dans le six.",
            "narrateur|La pomme, lisse, descend dans le filet.",
            "narrateur|L'œillet jette un dernier éclair, puis s'endort.",
        ),
        (2, 3, 3): L(
            "narrateur|Sarah n'a plus de nombres.",
            "narrateur|Un fromage pâle attend, loin du rouge.",
            "narrateur|La maîtresse le couvre d'un linge.",
            "narrateur|Aniss regarde l'œillet. Pas de clic. Il parle.",
            "enfant-m|S'il te plaît, le pâle, sous le linge.",
            "copine|Moi, j'ai les rouges.",
            "papa|Deux couleurs, deux tours.",
            "narrateur|Le fromage pâle pèse dans le filet.",
            "narrateur|Le linge reste. La bâche tient, ouverte.",
        ),
        (3, 1, 1): L(
            "narrateur|Nino a eu son bout. Le couteau se pose.",
            "narrateur|Un pain, près du lait, va rentrer au four.",
            "narrateur|Aniss veut le rattraper. Il s'arrête.",
            "narrateur|Il attend le clic mince de l'œillet.",
            "enfant-m|S'il te plaît, le pain, après le bout.",
            "copain|J'ai goûté.",
            "maman|Après le goût, ta phrase.",
            "narrateur|Le pain tiède contraste avec le marbre.",
            "narrateur|Il entre dans le filet, et ça a failli rater.",
        ),
        (3, 1, 2): L(
            "narrateur|Le bout de Nino a quitté le plateau.",
            "narrateur|Une pomme attend sur le marbre, hors de place.",
            "narrateur|La boulangère va la rendre à l'étal.",
            "narrateur|Aniss suit l'ombre de l'œillet sur le blanc.",
            "enfant-m|S'il te plaît, la pomme du marbre.",
            "copain|Moi, j'ai le lait.",
            "papa|Le bout, puis le fruit.",
            "narrateur|La pomme, froide, glisse dans le filet.",
            "narrateur|Le marbre garde un rond d'eau, minuscule.",
        ),
        (3, 1, 3): L(
            "narrateur|Nino s'essuie la bouche. Le fromage entier reste.",
            "narrateur|La boulangère le rapproche du couteau, trop près.",
            "narrateur|Aniss ne coupe pas la main. Il écoute l'œillet.",
            "enfant-m|S'il te plaît, le rond, entier.",
            "copain|Le bout me suffit.",
            "maman|Deux faims, deux mesures.",
            "narrateur|Le fromage entier, enveloppé, pèse dans le filet.",
            "narrateur|Le couteau reste. La bâche, dehors, n'est pas pliée.",
        ),
        (3, 2, 1): L(
            "narrateur|Mila a fini sa lune. Le voisin lève le sac.",
            "narrateur|Un pain, oublié près du lait, refroidit.",
            "narrateur|Aniss veut parler trop tôt. Il reprend sa voix.",
            "narrateur|L'œillet se tait. Alors il demande.",
            "enfant-m|S'il te plaît, le pain oublié.",
            "copine|Ma lune est ronde, elle aussi.",
            "papa|Après la lune, le pain.",
            "narrateur|Le pain, un peu froid, entre dans le filet.",
            "narrateur|Le sac du voisin part. L'allée se libère.",
        ),
        (3, 2, 2): L(
            "narrateur|Mila retire son doigt. La lune n'est plus touchée.",
            "narrateur|Une pomme a roulé sous le sac du voisin.",
            "narrateur|Aniss ne plonge pas. Il attend le clic.",
            "enfant-m|S'il te plaît, la pomme sous le sac.",
            "copine|Je n'en voulais pas, moi.",
            "maman|Ta phrase est arrivée, après la lune.",
            "narrateur|La pomme sort, lisse, et pose dans le filet.",
            "narrateur|Une ombre d'œillet glisse, puis s'en va.",
        ),
        (3, 2, 3): L(
            "narrateur|Mila a dit sa lune jusqu'au bout.",
            "narrateur|Le fromage lisse va rejoindre le sac du voisin.",
            "narrateur|Aniss regarde l'œillet. Il refuse de foncer.",
            "enfant-m|S'il te plaît, un fromage, le mien.",
            "copine|Le mien, c'était juste un doigt.",
            "papa|Un doigt, puis un goûter.",
            "narrateur|Le fromage, en papier, pèse dans le filet.",
            "narrateur|Derrière eux, le voisin s'éloigne.",
            "narrateur|Sur le marbre, il ne reste plus rien.",
        ),
        (3, 3, 1): L(
            "narrateur|Sarah a fini sa roue. La maîtresse hoche la tête.",
            "narrateur|Un pain, près du lait, va être rangé.",
            "narrateur|Aniss attend le silence de l'œillet, dehors.",
            "enfant-m|S'il te plaît, le pain, après la roue.",
            "copine|Ma roue est arrivée.",
            "maman|Après la roue, on t'écoutait.",
            "narrateur|Le pain tiède entre dans le filet, contre le froid.",
            "narrateur|La maîtresse range son panier. Rien n'est plié dehors.",
        ),
        (3, 3, 2): L(
            "narrateur|La roue de Sarah s'est arrêtée.",
            "narrateur|Une pomme brille sur le marbre, trop ronde.",
            "narrateur|La maîtresse va la poser plus loin.",
            "narrateur|Aniss parle après, pas pendant.",
            "enfant-m|S'il te plaît, la ronde, pour le filet.",
            "copine|La mienne était une histoire.",
            "papa|L'histoire, puis le fruit.",
            "narrateur|La pomme, froide, descend dans l'anse rouge.",
            "narrateur|Un clic d'œillet salue, tout au loin.",
        ),
        (3, 3, 3): L(
            "narrateur|Sarah n'a plus de roue à raconter.",
            "narrateur|Le fromage rond va sous une cloche de verre.",
            "narrateur|Aniss veut lever la cloche. Il ne le fait pas.",
            "narrateur|Il écoute l'œillet, puis la place.",
            "enfant-m|S'il te plaît, le rond, pour le goûter.",
            "copine|Moi, je garde l'histoire.",
            "maman|Ta demande est arrivée, entière.",
            "narrateur|Le fromage quitte le verre, et pèse dans le filet.",
            "narrateur|La cloche se tait. La bâche, dehors, reste ouverte.",
        ),
    }
    return table[(a, b, c)]


ENDS = {
    (1, 1, 1): L(
        "narrateur|Sur le chemin, le filet sent le beurre.",
        "narrateur|Nino mange son chaud, plus loin.",
        "enfant-m|Le mien est plus petit. Il me va.",
        "papa|Tu l'as demandé après lui.",
        "maman|L'œillet s'est tu, et ta voix est passée.",
        "narrateur|Une miette reste collée à l'anse rouge.",
        "narrateur|L'œillet de cuivre garde une croûte minuscule.",
    ),
    (1, 1, 2): L(
        "narrateur|La pomme cogne doucement le filet, à chaque pas.",
        "enfant-m|Elle est froide, après le four.",
        "papa|Nino a le chaud. Toi, le lisse.",
        "maman|Deux envies, deux sacs.",
        "narrateur|Un coin de bâche reste plié, comme un salut.",
        "narrateur|Une goutte d'œillet glisse sur la pomme, puis s'arrête.",
    ),
    (1, 1, 3): L(
        "narrateur|Le fromage refroidit le filet, contre la jambe.",
        "enfant-m|Nino a le pain. J'ai le blanc.",
        "maman|Chacun a parlé à son tour.",
        "papa|La goutte est tombée à côté.",
        "narrateur|Le papier sent un peu le cuivre chaud.",
        "narrateur|La bâche rayée claque, loin, sans se plier.",
    ),
    (1, 2, 1): L(
        "narrateur|Le sachet du pain frotte, rêche, dans le filet.",
        "enfant-m|Mila est restée au chaud.",
        "papa|Toi, tu as pris le passage.",
        "maman|L'un après l'autre, la porte a suffi.",
        "narrateur|Le voisin a disparu au coin de l'allée.",
        "narrateur|La bâche claque une dernière fois, puis se tient.",
    ),
    (1, 2, 2): L(
        "narrateur|La pomme, froide, voyage contre le filet tiède.",
        "enfant-m|Mila a le four. J'ai le fruit.",
        "maman|Le voisin a parlé longtemps. Tu as attendu.",
        "papa|L'œillet s'est endormi.",
        "narrateur|Une rayure jaune luit, sèche, au-dessus des caisses.",
        "narrateur|La pomme garde un rond d'eau, minuscule.",
    ),
    (1, 2, 3): L(
        "narrateur|Le papier blanc bruisse, à chaque pas.",
        "enfant-m|Mila a gardé le chaud.",
        "papa|Toi, le frais.",
        "maman|Le passage, elle l'a laissé.",
        "narrateur|Le voisin range son sac, plus loin.",
        "narrateur|L'œillet brille, sec, au coin de la toile.",
    ),
    (1, 3, 1): L(
        "narrateur|Le pain pâle chauffe le filet, tout contre Aniss.",
        "enfant-m|Sarah a son four, sur la feuille.",
        "maman|Tu as parlé après le dessin.",
        "papa|Le pâle était le dernier.",
        "narrateur|La maîtresse part, son pain doré sous le bras.",
        "narrateur|Sarah replie son dessin. Le filet, lui, fume un peu.",
    ),
    (1, 3, 2): L(
        "narrateur|La vraie pomme luit dans le filet, pas le dessin.",
        "enfant-m|Sarah a gardé la sienne, en crayon.",
        "papa|Les deux pommes ont eu leur place.",
        "maman|La coupe n'est pas partie sans toi.",
        "narrateur|La maîtresse a refermé son sac.",
        "narrateur|La pomme garde un rond d'eau, comme une signature.",
    ),
    (1, 3, 3): L(
        "narrateur|Le fromage pèse. L'anse rouge s'enfonce un peu.",
        "enfant-m|Sarah a le dessin. J'ai le goûter.",
        "maman|Ta phrase est arrivée entière.",
        "papa|La vitre a gardé la trace ronde.",
        "narrateur|La maîtresse dit au revoir, plus loin.",
        "narrateur|L'œillet cliquette, loin, comme un salut.",
    ),
    (2, 1, 1): L(
        "narrateur|Le pain tiède voyage loin des fraises, dans le filet.",
        "enfant-m|Nino a la poire. J'ai le chaud.",
        "papa|Après la poire, c'était ton tour.",
        "maman|La bâche n'a pas tout plié.",
        "narrateur|Une fraise reste sous la toile, trop mouillée.",
        "narrateur|L'œillet s'est tu au-dessus des caisses vides.",
    ),
    (2, 1, 2): L(
        "narrateur|La pomme rouge cogne le filet, régulière.",
        "enfant-m|Nino a le sucré. J'ai le lisse.",
        "maman|Deux fruits, deux phrases.",
        "papa|La goutte est tombée à côté.",
        "narrateur|La boulangère emporte sa poire, vers le four.",
        "narrateur|L'œillet de cuivre sèche, rond, au vent.",
    ),
    (2, 1, 3): L(
        "narrateur|Le fromage, à l'ombre, refroidit le filet.",
        "enfant-m|Nino a le sucré. J'ai le blanc.",
        "papa|Après la poire, on t'a entendu.",
        "maman|Les fraises sont restées.",
        "narrateur|La bâche rayée sèche au soleil, rayure après rayure.",
        "narrateur|Un goût de lait suit Aniss, jusqu'à la maison.",
    ),
    (2, 2, 1): L(
        "narrateur|Le pain, presque mouillé, sent l'ornière et le four.",
        "enfant-m|Mila a son lac. J'ai le pain au sec.",
        "maman|La goutte est arrivée trop tard pour lui.",
        "papa|Tu as parlé après le clic.",
        "narrateur|Mila saute une dernière fois, plus loin.",
        "narrateur|L'ornière tremble. Le pain, lui, ne tombe pas.",
    ),
    (2, 2, 2): L(
        "narrateur|La pomme, un peu humide, voyage dans le filet.",
        "enfant-m|Elle a frôlé le lac de Mila.",
        "papa|Le lac, puis le fruit.",
        "maman|L'eau ne l'a pas prise.",
        "narrateur|Le voisin a fini le thym, derrière eux.",
        "narrateur|La pomme sent l'allée, juste un peu.",
    ),
    (2, 2, 3): L(
        "narrateur|Le fromage, enveloppé, ne sent plus l'eau.",
        "enfant-m|Mila a quitté la flaque.",
        "maman|Tes pieds étaient au sec, pour demander.",
        "papa|Le voisin a fermé son sac.",
        "narrateur|Un pigeon picore près d'une caisse vide.",
        "narrateur|L'œillet ne cliquette plus. Une goutte y dort.",
    ),
    (2, 3, 1): L(
        "narrateur|Le pain tiède pèse, après le compte de Sarah.",
        "enfant-m|Six, puis moi.",
        "papa|Après six, on t'écoutait.",
        "maman|Un coin de bâche reste en l'air.",
        "narrateur|La maîtresse emporte ses fraises, plus loin.",
        "narrateur|Les fraises sentent le sucre. Le pain, le beurre.",
    ),
    (2, 3, 2): L(
        "narrateur|La pomme à part roule un peu, puis s'arrête.",
        "enfant-m|Sarah n'a pas compté celle-là.",
        "maman|Elle n'était pas dans le six.",
        "papa|L'œillet s'est endormi.",
        "narrateur|Sarah a fini de compter, pour de vrai.",
        "narrateur|La pomme tient dans le filet, hors des rouges.",
    ),
    (2, 3, 3): L(
        "narrateur|Le fromage pâle pèse, loin du rouge.",
        "enfant-m|Sarah a les fraises. J'ai le pâle.",
        "papa|Deux couleurs, deux tours.",
        "maman|Le linge est resté.",
        "narrateur|La maîtresse plie son panier, sans plier la toile.",
        "narrateur|Le soleil revient sur les rayures jaunes et bleues.",
    ),
    (3, 1, 1): L(
        "narrateur|Le pain tiède réchauffe les doigts, contre le marbre oublié.",
        "enfant-m|Nino a goûté. J'ai le chaud.",
        "maman|Après le goût, ta phrase.",
        "papa|Ça a failli rentrer au four.",
        "narrateur|La boulangère referme sa porte, plus loin.",
        "narrateur|Le marbre reste froid. Le pain, lui, voyage.",
    ),
    (3, 1, 2): L(
        "narrateur|La pomme du marbre roule dans le filet, puis tient.",
        "enfant-m|Nino a le lait. J'ai le lisse.",
        "papa|Le bout, puis le fruit.",
        "maman|Un rond d'eau reste sur le blanc.",
        "narrateur|La boulangère rend le plateau, vide.",
        "narrateur|La pomme garde le froid du marbre, un moment.",
    ),
    (3, 1, 3): L(
        "narrateur|Le fromage entier pèse, plus lourd que le bout de Nino.",
        "enfant-m|Lui, un bout. Moi, le rond.",
        "maman|Deux faims, deux mesures.",
        "papa|Le couteau est resté.",
        "narrateur|Dehors, la bâche n'est pas pliée.",
        "narrateur|Le fromage blanc porte une ombre d'œillet.",
    ),
    (3, 2, 1): L(
        "narrateur|Le pain oublié, un peu froid, sent le lait.",
        "enfant-m|Mila a eu sa lune.",
        "papa|Après la lune, le pain.",
        "maman|L'allée s'est libérée.",
        "narrateur|Le voisin dit au revoir, sans se retourner.",
        "narrateur|Le pain fume à peine, tout au fond du filet.",
    ),
    (3, 2, 2): L(
        "narrateur|La pomme sous le sac luit, lisse, dans le filet.",
        "enfant-m|Mila n'en voulait pas.",
        "maman|Ta phrase est arrivée après la lune.",
        "papa|L'ombre de l'œillet s'en est allée.",
        "narrateur|Une pièce tinte, dans le porte-monnaie.",
        "narrateur|L'œillet, lui, se tait pour de bon.",
    ),
    (3, 2, 3): L(
        "narrateur|Dans le filet, le fromage en papier pèse contre la jambe.",
        "enfant-m|Mila a touché. J'ai acheté.",
        "papa|Un doigt, puis un goûter.",
        "maman|Le voisin est parti.",
        "narrateur|Le filet rêche sent le lait, et un peu de pluie.",
        "narrateur|Une ombre d'œillet n'est plus sur le blanc.",
    ),
    (3, 3, 1): L(
        "narrateur|Le pain tiède contraste avec le souvenir du marbre.",
        "enfant-m|Sarah a eu sa roue.",
        "maman|Après la roue, on t'écoutait.",
        "papa|Rien n'est plié, dehors.",
        "narrateur|La maîtresse range un livre dans son panier.",
        "narrateur|Le pain dore dans le filet, jusqu'à la maison.",
    ),
    (3, 3, 2): L(
        "narrateur|La pomme ronde luit, froide, contre l'anse rouge.",
        "enfant-m|Sarah a gardé l'histoire.",
        "papa|L'histoire, puis le fruit.",
        "maman|Un clic a salué, loin.",
        "narrateur|Sarah ferme sa feuille. La maîtresse part.",
        "narrateur|La pomme luit, ronde, comme une petite roue.",
    ),
    (3, 3, 3): L(
        "narrateur|Le fromage rond pèse. La cloche de verre s'est tue.",
        "enfant-m|Sarah garde l'histoire. Je garde le goûter.",
        "maman|Ta demande est arrivée, entière.",
        "papa|La bâche tenait, ouverte.",
        "narrateur|Ils quittent l'allée. Le filet frotte, rêche et plein.",
        "narrateur|La bâche rayée se plie. L'œillet de cuivre disparaît.",
    ),
}


def write() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    scripts: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {}

    scripts["CHK_T0000_P0000"] = L(
        "narrateur|Les dernières gouttes font la course sur la bâche rayée.",
        "narrateur|Jaune, bleu, jaune : elles glissent vers un œillet de cuivre.",
        "narrateur|Aniss les suit du doigt, sans les toucher.",
        "narrateur|Le marché du village sent l'oignon mouillé.",
        "papa|Tu entends ce petit clic, Aniss ?",
        "enfant-m|On dirait une clochette minuscule.",
        "narrateur|Le soleil pâle revient sur les rayures.",
        "narrateur|Bientôt on pliera la toile, et l'allée sera vide.",
        "narrateur|Une caisse de fraises luit, trop mouillée pour durer.",
        "narrateur|Le filet à anse rouge frotte sa jambe.",
        "narrateur|Il est vide, un peu rêche, trop léger.",
        "maman|Le goûter manque de fruits, et de pain.",
        "narrateur|En ce moment, Aniss veut demander tout de suite.",
        "enfant-m|Des fraises, des croûtes, vite !",
        "narrateur|Sa phrase saute par-dessus celle de papa.",
        "narrateur|L'œillet cliquette au même instant.",
        "narrateur|Personne ne se tourne.",
        "narrateur|Le sourire d'Aniss disparaît.",
        "enfant-m|Ils n'ont pas entendu.",
        "maman|On va trouver une façon d'être écouté.",
        "papa|Par où commences-tu ?",
    )
    sons["CHK_T0000_P0000"] = "bache,marche"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|Aniss peut commencer par trois coins du marché.",
        "maman|La boulangerie, l'étal des fruits, ou la fromagerie ?",
    )
    extras["CHK_T0001_P0000"] = t3labs("la boulangerie", "l'étal des fruits", "la fromagerie")
    sons["CHK_T0001_P0000"] = ""

    t1_sons = {1: "cloche,papier", 2: "marche,caisse", 3: "papier,marbre"}
    t2_sons = {1: "cloche,marche", 2: "marche,eau", 3: "marche,voix"}
    t3_sons = {1: "papier,pain", 2: "pomme,filet", 3: "papier,fromage"}

    for a in (1, 2, 3):
        p = f"CHK_T0001_P000{a}"
        scripts[p] = T1[a]
        sons[p] = t1_sons[a]
        q_lines, q_fields = Q1[a]
        scripts[f"{p}_Q0001"] = q_lines
        extras[f"{p}_Q0001"] = q_fields
        sons[f"{p}_Q0001"] = ""
        scripts[f"{p}_C0001"] = C1[a]
        sons[f"{p}_C0001"] = ""
        scripts[f"{p}_T0002_P0000"] = L(
            "narrateur|Quelqu'un est là, et veut autre chose.",
            "papa|La boulangère, le voisin, ou la maîtresse ?",
        )
        extras[f"{p}_T0002_P0000"] = t3labs("la boulangère", "le voisin", "la maîtresse")
        sons[f"{p}_T0002_P0000"] = ""
        for b in (1, 2, 3):
            p2 = f"{p}_T0002_P000{b}"
            scripts[p2] = T2[(a, b)]
            sons[p2] = t2_sons[b]
            scripts[f"{p2}_T0003_P0000"] = L(
                "narrateur|Le filet est prêt. Il manque une chose.",
                "maman|Le pain, une pomme, ou un fromage ?",
            )
            extras[f"{p2}_T0003_P0000"] = t3labs("le pain", "une pomme", "un fromage")
            sons[f"{p2}_T0003_P0000"] = ""
            for c in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{c}"
                scripts[p3] = t3_lines(a, b, c)
                sons[p3] = t3_sons[c]
                fin = f"{p3}_F0001"
                scripts[fin] = ENDS[(a, b, c)]
                sons[fin] = "bache,filet"

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), 1.22, "medium")
        extra_v: dict = {}
        if kind == "transition_question":
            extra_v["pause_before"] = 200
        voice(nc, profile_for(cid, kind), extra_v)
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc

    out = dict(src)
    out["fil_rouge"] = (
        "Après la pluie, les gouttes courent sur la bâche rayée vers un œillet de cuivre. "
        "Aniss veut demander le goûter tout de suite : sa phrase saute par-dessus papa, "
        "l'œillet cliquette, personne n'entend. À la boulangerie, à l'étal ou à la fromagerie, "
        "il parle trop tôt. Nino, Mila ou Sarah veulent autre chose au même instant. "
        "Quand Aniss attend le clic, puis dit s'il te plaît, le filet se remplit. "
        "L'œillet paie le début."
    )
    out["title"] = "La bâche du marché d'Aniss"
    out["characters"] = "Aniss, papa, maman, Nino, Mila, Sarah"
    out["setting"] = "marché du village, après la pluie"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    ends = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                cid = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}_F0001"
                ends.append(by[cid]["text"])
    if len(set(ends)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(ends))}")

    path_words = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                path = [
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
                n = sum(words(by[i]["text"]) for i in path)
                path_words.append(n)
    print(f"chemins {min(path_words)}–{max(path_words)} mots, moy {sum(path_words)//len(path_words)}")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    vecu = (
        "Aniss veut demander le goûter avant qu'on plie la bâche. "
        "Il parle par-dessus papa : l'œillet cliquette, personne n'entend. "
        "Chaque lieu change l'échec (grelot, fraise, marbre). "
        "Nino, Mila ou Sarah veulent autre chose au même instant : "
        "le dernier pain, le chaud, un dessin, une poire, une flaque, un compte, un bout, une lune, une roue. "
        "Aniss retient, écoute, puis dit s'il te plaît après le clic. "
        "Le filet se remplit. L'œillet de cuivre paie l'ouverture."
    )
    notes = (
        "- Titre noyau conservé. Marché du village, après la pluie. "
        "Troupe D16 : Aniss, Nino, Mila, Sarah, papa, maman.\n"
        "- Labels T1/T2/T3 inchangés. Graphe `chunk_id` / `kind` inchangés.\n"
        "- Leçon COL.POL.001 vécue (demander / tour de parole), jamais dite. "
        "Un merci adulte, vécu, dans les confirmations.\n"
        "- Première idée ratée dès l'ouverture. Revers allongé en T2 "
        "(deux enfants, deux envies, voix qui se marchent dessus).\n"
        "- Indice unique dès le début : œillet de cuivre. Payé au climax et aux 27 fins.\n"
        "- 2e ruse : bâche qui se plie, goutte, dernier objet, cloche, papier. "
        "Aniss refuse de foncer.\n"
        "- 27 fins textuellement distinctes. TTS par fonction (profiles example2).\n"
        "- Tics encore/déjà/tout doux/calme et leçon maîtresse retirés.\n"
        f"- Mots par chemin : {min(path_words)}–{max(path_words)} "
        f"(moy {sum(path_words)//len(path_words)})."
    )
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — La bâche du marché d'Aniss\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        f"## Vécu\n{vecu}\n\n"
        f"## Vu et corrigé\n{notes}\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print("wrote merged.json + RELECTURE.md")


if __name__ == "__main__":
    write()
