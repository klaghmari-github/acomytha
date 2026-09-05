#!/usr/bin/env python3
"""TREE-COL-014 — Le gant rouge de Nina. F-NAR-019, N1, texte seulement."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, make_chunk, words  # noqa: E402

SID = "TREE-COL-014"
LIM = LIMITS["N1"]
ROLES = {"narrateur", "papa", "maman", "enfant-m", "enfant-f"}

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le gant va échapper; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
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
        note="arc=confirmation; intention=relancer; emotion=soulagement; intensite=1; destinataire=enfant; sous_texte=la_demande_a_ouvert_la_porte; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=trop_vite_ça_glisse; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement; intensite=2; destinataire=enfant; sous_texte=prendre_sans_demander_coince; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=demander_a_changé_le_geste; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_gant_a_changé_de_place; tempo=posé; sourire=léger; respiration=ample",
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
    if m["pitch_tag"]:
        body = f"<{m['pitch_tag']}>{body}</{m['pitch_tag']}>"
    pause = "[long-pause]" if m["pause"] >= 800 else ("[pause]" if m["pause"] >= 400 else "")
    return f"{body} {pause}".strip()


def L(*rows: str) -> list[str]:
    out = []
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
    for w in ("s'il te plaît", "gant rouge", "gant", "flaque"):
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


# ---------------------------------------------------------------------------
# T1 lieux — T2 objets — T3 enfants
# ---------------------------------------------------------------------------
LIEU = {
    1: dict(lab="le bac à sable", son="sable", ou="au bac à sable"),
    2: dict(lab="le toboggan", son="toboggan", ou="au toboggan"),
    3: dict(lab="les balançoires", son="balancoire", ou="aux balançoires"),
}
OUTIL = {
    1: dict(lab="le ballon", son="ballon"),
    2: dict(lab="le seau", son="seau"),
    3: dict(lab="le doudou", son="doudou"),
}
AMI = {
    1: dict(lab="Nino", role="enfant-m", qui="Nino"),
    2: dict(lab="Mila", role="enfant-f", qui="Mila"),
    3: dict(lab="Raphaël", role="enfant-m", qui="Raphaël"),
}


T1 = {
    1: L(
        "narrateur|Nina court vers le bac à sable.",
        "narrateur|Le sable est lourd, froid, collant.",
        "narrateur|Un coin rouge dépasse, à moitié enterré.",
        "enfant-f|Là !",
        "enfant-f|Mon gant !",
        "narrateur|Elle creuse avec les deux mains.",
        "narrateur|Le sable entre dans la laine.",
        "narrateur|Le gant devient plus lourd, plus sale.",
        "enfant-f|Sors !",
        "narrateur|Papa vide une botte, près du banc.",
        "narrateur|Il n'entend pas le mot.",
        "maman|Tu m'appelles, Nina ?",
        "enfant-f|Le gant.",
        "enfant-f|Le sable le tient.",
        "narrateur|Nina a les joues chaudes, déçue.",
        "narrateur|Ses doigts grelottent, gris de sable.",
        "papa|Je finis la botte.",
        "papa|Puis je viens.",
    ),
    2: L(
        "narrateur|Nina grimpe le toboggan à l'envers.",
        "narrateur|Le métal pique ses paumes nues.",
        "narrateur|Le gant rouge a glissé en bas.",
        "enfant-f|Je l'attrape !",
        "narrateur|Son pied pousse le gant, par erreur.",
        "narrateur|Le rouge part dans une flaque de boue.",
        "enfant-f|Non !",
        "narrateur|Maman essuie le cartable, plus loin.",
        "narrateur|Elle n'a pas vu le geste.",
        "maman|Ça va, Nina ?",
        "enfant-f|Le gant.",
        "enfant-f|La boue l'a pris.",
        "narrateur|Nina serre les poings, trop petite.",
        "narrateur|Le métal lui refroidit les genoux.",
        "papa|J'arrive.",
        "papa|Attends une seconde.",
    ),
    3: L(
        "narrateur|Nina court vers les balançoires.",
        "narrateur|Une chaîne cliquette, glacée.",
        "narrateur|Le gant rouge pend à un barreau.",
        "narrateur|Il s'est accroché, trop haut.",
        "enfant-f|Viens ici !",
        "narrateur|Elle saute. Ses doigts râlent l'air.",
        "narrateur|La barrière tremble. Le gant bascule.",
        "papa|J'attache ta chaussure, une seconde.",
        "narrateur|Le cri se perd dans le cliquetis.",
        "enfant-f|Il part !",
        "maman|Tu as besoin de nous, Nina ?",
        "enfant-f|Oui.",
        "enfant-f|Trop haut.",
        "narrateur|Nina souffle, les bras fatigués.",
        "narrateur|Le barreau garde le rouge, loin.",
    ),
}

# "Elle saute. Ses doigts râlent l'air." is TWO sentences — fix later if L() catches.
# "La barrière tremble. Le gant bascule." TWO sentences.

Q1 = {
    1: (
        L(
            "narrateur|Quelque chose de rouge est sous le sable.",
            "maman|C'est quoi, d'après toi ?",
        ),
        qf("gant", "gant | le gant | gant rouge | rouge", "Un coin rouge dépasse. C'est quoi ?"),
        "gant",
    ),
    2: (
        L(
            "narrateur|Un morceau rouge a glissé dans la boue.",
            "papa|C'est quoi, ce rouge ?",
        ),
        qf("gant", "gant | le gant | gant rouge | rouge", "Le rouge est dans la boue. C'est quoi ?"),
        "gant",
    ),
    3: (
        L(
            "narrateur|Un rouge pend trop haut, à la barrière.",
            "maman|Qu'est-ce qui s'est accroché ?",
        ),
        qf("gant", "gant | le gant | gant rouge | rouge", "Quelque chose de rouge pend. C'est quoi ?"),
        "gant",
    ),
}

C1 = {
    1: L(
        "narrateur|Nina attend que papa pose la botte.",
        "enfant-f|S'il te plaît, papa.",
        "enfant-f|Mon gant est sous le sable.",
        "papa|Je t'écoute.",
        "narrateur|Il se baisse. Un pouce rouge apparaît.",
        "maman|Merci, Nina.",
        "narrateur|Le gant est là, trop mouillé pour jouer.",
    ),
    2: L(
        "narrateur|Nina reste au bas du toboggan.",
        "enfant-f|S'il te plaît, maman.",
        "enfant-f|Le gant est dans la boue.",
        "maman|Je te vois.",
        "narrateur|Elle s'accroupit près de la flaque sale.",
        "papa|Merci, Nina.",
        "narrateur|Un bout de laine rouge luit, collé.",
    ),
    3: L(
        "narrateur|Nina pose les talons à terre.",
        "enfant-f|S'il te plaît, papa.",
        "enfant-f|Le gant est trop haut.",
        "papa|Là, je t'entends.",
        "narrateur|Il lève les yeux vers le barreau.",
        "maman|Merci, Nina.",
        "narrateur|Le gant penche, hors de portée.",
    ),
}

# T2: 9 scènes
T2 = {
    (1, 1): L(
        "narrateur|Nina saisit le ballon, sans un mot.",
        "narrateur|Elle le pousse vers le coin rouge.",
        "narrateur|Le ballon recouvre le gant, plus fort.",
        "enfant-f|Bouge !",
        "narrateur|Papa regarde la botte, pas le sable.",
        "maman|Tu voulais le ballon, Nina ?",
        "enfant-f|Pour le gant.",
        "enfant-f|Il est dessous.",
        "narrateur|Nina lâche le ballon. Il roule trop loin.",
        "papa|Tu veux que je le retienne ?",
        "enfant-f|S'il te plaît.",
        "narrateur|Papa arrête le ballon du pied.",
        "narrateur|Le coin rouge redevient visible.",
    ),
    (1, 2): L(
        "narrateur|Nina attrape le seau, toute seule.",
        "narrateur|Elle verse l'eau sur le sable.",
        "narrateur|Le trou se ferme. Le rouge disparaît.",
        "enfant-f|Oh.",
        "maman|Le seau était à moi, une minute.",
        "enfant-f|Je voulais laver le gant.",
        "narrateur|Nina pose le seau, déçue.",
        "papa|Tu peux le prendre comment ?",
        "enfant-f|S'il te plaît, le seau.",
        "maman|Oui. Pour creuser, pas noyer.",
        "narrateur|Nina pousse le sable, cuillère après cuillère.",
        "narrateur|Le pouce rouge revient, un peu propre.",
    ),
    (1, 3): L(
        "narrateur|Nina prend le doudou sur le banc.",
        "narrateur|Elle l'enroule autour du gant sableux.",
        "narrateur|La laine du doudou se remplit de grains.",
        "enfant-f|Il est sale !",
        "maman|Ce doudou n'aime pas le sable.",
        "enfant-f|Je voulais le gant au chaud.",
        "papa|Le doudou, tu le prends comment ?",
        "enfant-f|S'il te plaît, un coin.",
        "maman|Un coin, oui. Pas tout le doudou.",
        "narrateur|Nina frotte le gant avec le coin.",
        "narrateur|Les grains tombent. Le rouge reparaît.",
    ),
    (2, 1): L(
        "narrateur|Nina lance le ballon vers la boue.",
        "narrateur|Le ballon tape le gant, puis s'enfonce.",
        "enfant-f|Les deux sont pris !",
        "papa|Le ballon n'était pas à toi, Nina.",
        "enfant-f|Je voulais pousser le gant.",
        "narrateur|Nina avance, les pieds qui glissent.",
        "maman|Tu peux demander, avant de lancer ?",
        "enfant-f|S'il te plaît, le ballon.",
        "papa|On le sort ensemble, alors.",
        "narrateur|Papa tire le ballon. Le gant bouge.",
        "narrateur|Un lacet rouge se décolle de la boue.",
    ),
    (2, 2): L(
        "narrateur|Nina emporte le seau jusqu'au toboggan.",
        "narrateur|Elle verse. L'eau et la boue se mêlent.",
        "narrateur|Le gant nage, plus loin, plus sale.",
        "enfant-f|Reviens !",
        "maman|Ce seau servait à rincer les bottes.",
        "enfant-f|Je voulais laver le rouge.",
        "papa|On verse où, si on demande ?",
        "enfant-f|S'il te plaît, un peu d'eau.",
        "maman|Un filet, pas tout le seau.",
        "narrateur|Nina penche, tout doucement.",
        "narrateur|La boue s'ouvre. Le gant reste.",
    ),
    (2, 3): L(
        "narrateur|Nina glisse le doudou sur le métal.",
        "narrateur|Elle veut attraper le gant, de loin.",
        "narrateur|Le doudou glisse, trop vite, dans la boue.",
        "enfant-f|Non, doudou !",
        "papa|Il n'était pas un filet, ce doudou.",
        "enfant-f|J'avais froid aux mains.",
        "maman|Tu le prends comment, la prochaine ?",
        "enfant-f|S'il te plaît, le doudou.",
        "papa|On le tient à deux, alors.",
        "narrateur|Nina tient une oreille. Papa l'autre.",
        "narrateur|Le doudou touche le gant, sans tomber.",
    ),
    (3, 1): L(
        "narrateur|Nina frappe le gant avec le ballon.",
        "narrateur|Le rouge s'envole, plus haut, plus loin.",
        "enfant-f|Reviens, gant !",
        "papa|Le ballon allait vers la chaîne.",
        "enfant-f|Je voulais le faire tomber.",
        "narrateur|Nina saute. Le ballon roule sous la balançoire.",
        "maman|Le ballon, tu le lances où ?",
        "enfant-f|S'il te plaît, on vise bas.",
        "papa|Bas, d'accord.",
        "narrateur|Papa tient le ballon, tout près du barreau.",
        "narrateur|Le gant penche, presque à portée.",
    ),
    (3, 2): L(
        "narrateur|Nina pose le seau sous la barrière.",
        "narrateur|Elle monte dessus, sans rien dire.",
        "narrateur|Le seau bascule. Nina recule.",
        "enfant-f|Ça bouge !",
        "maman|Ce seau n'est pas un tabouret.",
        "enfant-f|Le gant est trop haut.",
        "papa|Tu veux de l'aide, comment ?",
        "enfant-f|S'il te plaît, tu me portes ?",
        "maman|Oui. Les pieds au sol, d'abord.",
        "narrateur|Nina attend. Papa s'accroupit.",
        "narrateur|Le seau reste vide, à sa place.",
    ),
    (3, 3): L(
        "narrateur|Nina jette le doudou vers le barreau.",
        "narrateur|Le doudou s'accroche, à côté du gant.",
        "enfant-f|Les deux sont coincés !",
        "papa|Le doudou n'était pas un crochet.",
        "enfant-f|Je voulais tirer le rouge.",
        "maman|On le décroche comment, alors ?",
        "enfant-f|S'il te plaît, tu l'attrapes ?",
        "papa|Le doudou d'abord. Puis le gant.",
        "narrateur|Nina attend, les bras le long du corps.",
        "narrateur|Papa décroche l'oreille en peluche.",
        "narrateur|Le gant penche, presque libre.",
    ),
}


def ami_role(c: int) -> str:
    return AMI[c]["role"]


def t3_lines(a: int, b: int, c: int) -> list[str]:
    qui = AMI[c]["qui"]
    r = ami_role(c)
    key = (a, b, c)
    table = {
        (1, 1, 1): L(
            "narrateur|Nino arrive, les genoux sablés.",
            "narrateur|Il voit le ballon près du rouge.",
            f"{r}|C'est mon ballon !",
            "narrateur|Nina tend la main, trop vite.",
            "narrateur|Le ballon part. Le gant se recouvre.",
            "enfant-f|Attends.",
            "enfant-f|S'il te plaît, Nino.",
            f"{r}|Quoi ?",
            "enfant-f|On le fait rouler, lentement.",
            "narrateur|Nino pousse du bout du pied.",
            "narrateur|Le gant se dégage, grain par grain.",
            "papa|Vous avez parlé, tous les deux.",
        ),
        (1, 1, 2): L(
            "narrateur|Mila s'assoit sur le ballon, au sable.",
            "narrateur|Le rouge disparaît sous son poids.",
            "enfant-f|Mila, bouge !",
            "narrateur|Mila ne bouge pas. Elle n'a pas entendu.",
            "enfant-f|S'il te plaît, Mila.",
            "enfant-f|Mon gant est dessous.",
            f"{r}|Ah. Je me lève.",
            "narrateur|Nina attend qu'elle se lève vraiment.",
            "narrateur|Le ballon roule. Le pouce rouge luit.",
            "maman|Elle te regardait. Elle a entendu.",
            "enfant-f|Merci, Mila.",
        ),
        (1, 1, 3): L(
            "narrateur|Raphaël arrive en parlant du but.",
            "enfant-f|Le ballon, le gant, le sable !",
            "narrateur|Ses mots se mêlent aux siens.",
            f"{r}|Quoi, le but ?",
            "enfant-f|Rien.",
            "narrateur|Nina serre les lèvres, puis attend.",
            "enfant-f|S'il te plaît, Raphaël.",
            "enfant-f|Quand tu as fini, mon gant.",
            f"{r}|J'ai fini.",
            "narrateur|Il écoute. Ils poussent le ballon.",
            "narrateur|Le gant sort, plat et rouge.",
            "papa|Cette fois, on a tout entendu.",
        ),
        (1, 2, 1): L(
            "narrateur|Nino prend le seau pour un château.",
            "narrateur|Nina le rattrape par l'anse.",
            "narrateur|Le sable vole. Le gant se recouvre.",
            f"{r}|Hé !",
            "enfant-f|S'il te plaît, Nino.",
            "enfant-f|Le seau, pour mon gant.",
            f"{r}|Après mon mur ?",
            "enfant-f|Après, d'accord.",
            "narrateur|Nina attend la dernière pelletée.",
            "narrateur|Nino tend le seau, anse la première.",
            "enfant-f|Merci.",
            "narrateur|Le seau soulève le sable. Le rouge paraît.",
        ),
        (1, 2, 2): L(
            "narrateur|Mila remplit le seau, pelletée après pelletée.",
            "narrateur|Nina ouvre la bouche, puis la referme.",
            "enfant-f|S'il te plaît, Mila.",
            "enfant-f|Quand c'est plein, je creuse.",
            f"{r}|C'est plein.",
            "narrateur|Mila pose le seau entre elles.",
            "narrateur|Nina creuse à côté, pas dedans.",
            "narrateur|Le gant se dégage, un doigt, puis deux.",
            "maman|Le seau a voyagé entre vous.",
            "enfant-f|Merci, Mila.",
        ),
        (1, 2, 3): L(
            "narrateur|Raphaël parle du seau et de la mer.",
            "enfant-f|Moi aussi, le seau !",
            "narrateur|Personne ne sait qui tient l'anse.",
            "enfant-f|S'il te plaît, Raphaël.",
            "enfant-f|Tu finis. Après, je creuse.",
            f"{r}|Je finis.",
            "narrateur|Il pose le seau. Nina le prend.",
            "narrateur|Le gant sort, propre d'un côté.",
            "papa|L'anse, l'un après l'autre.",
        ),
        (1, 3, 1): L(
            "narrateur|Nino serre le doudou contre lui.",
            "narrateur|Le gant est coincé dans la peluche.",
            "enfant-f|Rends !",
            f"{r}|Il est doux.",
            "enfant-f|S'il te plaît, Nino.",
            "enfant-f|Un coin, juste un coin.",
            f"{r}|Un coin.",
            "narrateur|Nino ouvre les bras, un peu.",
            "narrateur|Nina tire le gant, sans tirer le doudou.",
            "papa|Vous avez partagé le coin.",
            "enfant-f|Merci, Nino.",
        ),
        (1, 3, 2): L(
            "narrateur|Mila réchauffe le doudou sous son manteau.",
            "narrateur|Nina attend, les pieds qui bougent.",
            "enfant-f|S'il te plaît, Mila.",
            "enfant-f|Le gant est dans le doudou.",
            f"{r}|Je le sors.",
            "narrateur|Mila pose le doudou. Le gant tombe.",
            "narrateur|Nina le ramasse, sans prendre le doudou.",
            "maman|Elle s'est tournée vers toi.",
            "enfant-f|Merci, Mila.",
        ),
        (1, 3, 3): L(
            "narrateur|Raphaël raconte une histoire au doudou.",
            "enfant-f|Mon gant !",
            "narrateur|Raphaël sursaute. Il serre plus fort.",
            "enfant-f|S'il te plaît, Raphaël.",
            "enfant-f|Quand tu as fini de parler.",
            f"{r}|J'ai fini.",
            "narrateur|Il écoute. Nina montre le pouce rouge.",
            "narrateur|Ensemble, ils libèrent le gant.",
            "papa|Il a entendu jusqu'au bout.",
        ),
        (2, 1, 1): L(
            "narrateur|Nino envoie le ballon du haut du toboggan.",
            "narrateur|Le ballon vise la boue, et le gant.",
            "enfant-f|Stop !",
            f"{r}|C'est un but !",
            "enfant-f|S'il te plaît, Nino.",
            "enfant-f|À côté, pas dessus.",
            f"{r}|À côté.",
            "narrateur|Nino vise l'herbe. Le ballon rebondit.",
            "narrateur|Papa soulève le gant, d'un doigt.",
            "maman|Vous avez changé le lancer.",
            "enfant-f|Merci, Nino.",
        ),
        (2, 1, 2): L(
            "narrateur|Mila tient le ballon en haut de la rampe.",
            "narrateur|Nina lève le bras, trop tôt.",
            "enfant-f|Donne !",
            "narrateur|Mila recule. Le ballon tremble.",
            "enfant-f|S'il te plaît, Mila.",
            "enfant-f|Tu le lâches à côté de la boue.",
            f"{r}|À côté.",
            "narrateur|Le ballon roule dans l'herbe.",
            "narrateur|Le gant reste, prêt à être pris.",
            "papa|Elle t'a entendue, cette fois.",
        ),
        (2, 1, 3): L(
            "narrateur|Raphaël compte les marches du toboggan.",
            "enfant-f|Le ballon, vite !",
            f"{r}|Quatre, cinq.",
            "narrateur|Il n'a pas entendu le mot ballon.",
            "enfant-f|S'il te plaît, Raphaël.",
            "enfant-f|Quand tu as fini de compter.",
            f"{r}|Dix. Je t'écoute.",
            "narrateur|Ils posent le ballon loin de la boue.",
            "narrateur|Nina prend le gant, deux doigts seulement.",
            "maman|Le compte s'est arrêté. On t'écoute.",
        ),
        (2, 2, 1): L(
            "narrateur|Nino rince le toboggan avec le seau.",
            "narrateur|L'eau court vers le gant, trop vite.",
            "enfant-f|Pas là !",
            f"{r}|Ça lave !",
            "enfant-f|S'il te plaît, Nino.",
            "enfant-f|L'eau, de l'autre côté.",
            f"{r}|De l'autre.",
            "narrateur|Nino verse vers l'herbe.",
            "narrateur|La boue se calme. Le gant tient.",
            "papa|Vous avez choisi le côté.",
            "enfant-f|Merci, Nino.",
        ),
        (2, 2, 2): L(
            "narrateur|Mila tape le seau sur le métal.",
            "narrateur|Le bruit couvre la voix de Nina.",
            "enfant-f|Mila !",
            "narrateur|Nina attend la fin du bruit.",
            "enfant-f|S'il te plaît, Mila.",
            "enfant-f|Le seau, pour le gant.",
            f"{r}|Je pose.",
            "narrateur|Le seau se tait. Elles versent un filet.",
            "narrateur|Le gant se décolle, lourd et propre.",
            "maman|Quand le seau s'est tu, on t'a entendue.",
        ),
        (2, 2, 3): L(
            "narrateur|Raphaël décrit la boue, très fort.",
            "enfant-f|Le seau !",
            f"{r}|C'est une rivière !",
            "narrateur|Nina attend la fin de la rivière.",
            "enfant-f|S'il te plaît, Raphaël.",
            "enfant-f|Un filet, pas une rivière.",
            f"{r}|Un filet.",
            "narrateur|Ils penchent le seau, juste un peu.",
            "narrateur|Le gant reste. L'eau part.",
            "papa|Le filet, pas la rivière.",
        ),
        (2, 3, 1): L(
            "narrateur|Nino pose le doudou en haut du toboggan.",
            "narrateur|Il veut le faire glisser, comme un luge.",
            "enfant-f|Non, il va dans la boue !",
            f"{r}|C'est drôle !",
            "enfant-f|S'il te plaît, Nino.",
            "enfant-f|On le tient. On ne le lance pas.",
            f"{r}|On le tient.",
            "narrateur|Ils tiennent les deux oreilles.",
            "narrateur|Le doudou touche le gant. Papa le saisit.",
            "maman|Vous l'avez gardé, au lieu de le jeter.",
        ),
        (2, 3, 2): L(
            "narrateur|Mila s'assoit sur le doudou, au bas.",
            "narrateur|Le gant est coincé sous son genou.",
            "enfant-f|Mila, mon gant !",
            "narrateur|Mila rit, sans comprendre.",
            "enfant-f|S'il te plaît, Mila.",
            "enfant-f|Tu te lèves. Le rouge est dessous.",
            f"{r}|Je me lève.",
            "narrateur|Le doudou se libère. Le gant aussi.",
            "papa|Elle s'est levée. Le rouge est libre.",
        ),
        (2, 3, 3): L(
            "narrateur|Raphaël invente une voix pour le doudou.",
            "enfant-f|Papa, le gant !",
            f"{r}|Le doudou dit : glisse !",
            "narrateur|Nina attend que la voix s'arrête.",
            "enfant-f|S'il te plaît, Raphaël.",
            "enfant-f|Le doudou, pour attraper le rouge.",
            f"{r}|D'accord. Il arrête de glisser.",
            "narrateur|Ils tendent le doudou, sans le lâcher.",
            "narrateur|Le gant vient. La boue reste.",
            "maman|Sa voix d'abord. La tienne après.",
        ),
        (3, 1, 1): L(
            "narrateur|Nino vise le gant avec le ballon.",
            "narrateur|Nina lève les deux mains.",
            "enfant-f|Pas trop fort !",
            f"{r}|Je touche le rouge !",
            "enfant-f|S'il te plaît, Nino.",
            "enfant-f|Tout près, pas un coup.",
            f"{r}|Tout près.",
            "narrateur|Nino pose le ballon contre le barreau.",
            "narrateur|Le gant bascule dans les mains de papa.",
            "maman|Le coup est devenu un geste.",
            "enfant-f|Merci, Nino.",
        ),
        (3, 1, 2): L(
            "narrateur|Mila fait rebondir le ballon sous les chaînes.",
            "narrateur|Nina veut le prendre, trop tôt.",
            "narrateur|Le ballon lui échappe. Le gant tremble.",
            "enfant-f|S'il te plaît, Mila.",
            "enfant-f|Tu arrêtes le ballon.",
            f"{r}|Je l'arrête.",
            "narrateur|Mila plaque le ballon au sol.",
            "narrateur|Papa décroche le gant, d'une main.",
            "papa|Le rebond s'est tu. Le rouge est à toi.",
        ),
        (3, 1, 3): L(
            "narrateur|Raphaël compte ses tirs, tout haut.",
            "enfant-f|Le gant !",
            f"{r}|Trois !",
            "narrateur|Nina attend le silence entre les nombres.",
            "enfant-f|S'il te plaît, Raphaël.",
            "enfant-f|Plus de tirs. Mon gant.",
            f"{r}|Plus de tirs.",
            "narrateur|Il pose le ballon. Papa lève le bras.",
            "narrateur|Le gant quitte le barreau, enfin.",
            "maman|Entre deux nombres, on t'a entendue.",
        ),
        (3, 2, 1): L(
            "narrateur|Nino monte sur le seau, à son tour.",
            "narrateur|Le seau penche. Nina recule.",
            "enfant-f|Ça va tomber !",
            f"{r}|Je touche !",
            "enfant-f|S'il te plaît, Nino.",
            "enfant-f|Pieds par terre. Papa nous porte.",
            f"{r}|Pieds par terre.",
            "narrateur|Nino descend. Papa s'accroupit.",
            "narrateur|Nina demande, bas, le dernier geste.",
            "enfant-f|S'il te plaît, tu l'attrapes ?",
            "papa|Voilà.",
            "narrateur|Le gant quitte le barreau, dans sa main.",
        ),
        (3, 2, 2): L(
            "narrateur|Mila pose le seau sur la balançoire.",
            "narrateur|Le seau devient un siège, trop lourd.",
            "enfant-f|Mila, le gant !",
            f"{r}|C'est mon bateau.",
            "enfant-f|S'il te plaît, Mila.",
            "enfant-f|Le seau, par terre. Papa monte.",
            f"{r}|Par terre.",
            "narrateur|Mila pose le seau. La chaîne se tait.",
            "narrateur|Papa tend le gant vers Nina.",
            "maman|Le bateau a laissé la place.",
        ),
        (3, 2, 3): L(
            "narrateur|Raphaël regarde l'eau du seau, comme un miroir.",
            "enfant-f|Le gant, là-haut !",
            f"{r}|Je vois le ciel !",
            "narrateur|Nina attend qu'il lève les yeux.",
            "enfant-f|S'il te plaît, Raphaël.",
            "enfant-f|Le seau reste. On demande à papa.",
            f"{r}|D'accord.",
            "narrateur|Ils posent le seau. Papa écoute.",
            "enfant-f|S'il te plaît, tu le décroches ?",
            "papa|Oui.",
            "narrateur|Le gant descend, un barreau à la fois.",
        ),
        (3, 3, 1): L(
            "narrateur|Nino balance le doudou sur l'autre siège.",
            "narrateur|Le doudou vole trop près du gant.",
            "enfant-f|Il va l'emmener !",
            f"{r}|C'est un copain !",
            "enfant-f|S'il te plaît, Nino.",
            "enfant-f|Le doudou, sur le banc.",
            f"{r}|Sur le banc.",
            "narrateur|Nino pose le doudou. Papa tend le bras.",
            "narrateur|Le gant glisse dans la main de Nina.",
            "maman|Le copain a laissé le rouge.",
        ),
        (3, 3, 2): L(
            "narrateur|Mila installe le doudou comme passager.",
            "narrateur|Elle pousse la balançoire. Le gant tremble.",
            "enfant-f|Mila, stop !",
            f"{r}|Il aime ça.",
            "enfant-f|S'il te plaît, Mila.",
            "enfant-f|Tu arrêtes. Papa prend le rouge.",
            f"{r}|J'arrête.",
            "narrateur|La chaîne se tait. Papa décroche.",
            "narrateur|Nina reçoit le gant, humide.",
            "papa|Le passager a attendu, lui aussi.",
        ),
        (3, 3, 3): L(
            "narrateur|Raphaël parle au doudou, très près.",
            "enfant-f|Mon gant, papa !",
            f"{r}|Le doudou a peur du haut.",
            "narrateur|Nina attend la fin de la peur.",
            "enfant-f|S'il te plaît, Raphaël.",
            "enfant-f|Tu tiens le doudou. Papa le gant.",
            f"{r}|Je tiens.",
            "narrateur|Raphaël serre le doudou. Papa le rouge.",
            "narrateur|Nina enfile un doigt, puis un autre.",
            "maman|Toi le gant. Lui le doudou.",
        ),
    }
    if key not in table:
        raise SystemExit(f"T3 manquant {key}")
    return table[key]


ENDS = {
    (1, 1, 1): L(
        "narrateur|Au banc, Nina essuie un grain sur le pouce.",
        "enfant-f|Il est à moi, maintenant.",
        "papa|Il sèche sur ta main.",
        "maman|La flaque tient un gant, minuscule.",
        "narrateur|Nino pose le ballon, loin du sable.",
        "narrateur|Le rouge ne s'enterre plus.",
    ),
    (1, 1, 2): L(
        "narrateur|Mila s'assoit sur le banc, pas sur le ballon.",
        "enfant-f|Mon gant sent le soleil.",
        "maman|Il sèche, doigt par doigt.",
        "papa|Le banc garde une laine rouge, ouverte.",
        "narrateur|La flaque n'a plus de grain dessus.",
        "narrateur|Nina ferme le poing, au chaud.",
    ),
    (1, 1, 3): L(
        "narrateur|Raphaël se tait. Nina parle jusqu'au bout.",
        "enfant-f|J'ai tiré trop vite, tout à l'heure.",
        "papa|On t'écoute, là.",
        "narrateur|La corneille penche vers un pouce rouge.",
        "maman|Le ciel dans la flaque a un point chaud.",
        "narrateur|Le ballon dort contre le cartable.",
    ),
    (1, 2, 1): L(
        "narrateur|Nino range le seau près du château.",
        "enfant-f|Le gant n'a plus de sable dans l'œil.",
        "maman|Le seau reflète un ciel, et un gant.",
        "papa|Tu as attendu son mur.",
        "narrateur|Nina souffle sur la laine. Un grain part.",
        "narrateur|Le bac à sable redevient un bac.",
    ),
    (1, 2, 2): L(
        "narrateur|Mila pose l'anse dans la main de Nina.",
        "enfant-f|Une goutte quitte le gant, enfin.",
        "papa|Elle tombe dans le seau, pas dans le sable.",
        "maman|Vos deux voix sont passées, l'une après l'autre.",
        "narrateur|Le rouge sèche, un peu rêche, un peu fier.",
        "narrateur|Le banc sent moins l'école.",
    ),
    (1, 2, 3): L(
        "narrateur|Raphaël a fini sa mer. Nina a fini de creuser.",
        "enfant-f|Le sable a un petit creux rouge.",
        "papa|C'est l'endroit du seau, maintenant.",
        "maman|Le seau reste, vide et utile.",
        "narrateur|Nina enfile le gant. Il chauffe un peu.",
        "narrateur|La flaque rend le ciel, sans le sable.",
    ),
    (1, 3, 1): L(
        "narrateur|Nino garde le doudou. Nina garde le gant.",
        "enfant-f|Le doudou sent le gant, un peu humide.",
        "maman|Un coin a suffi.",
        "papa|La barrière n'a plus de laine.",
        "narrateur|Le sable a perdu son secret rouge.",
        "narrateur|Nina frotte le pouce, propre.",
    ),
    (1, 3, 2): L(
        "narrateur|Mila rentre le doudou sous le manteau.",
        "enfant-f|Mon gant est sorti tout seul.",
        "papa|Mila t'a tendu le doudou.",
        "maman|La barrière est nue, sans rouge.",
        "narrateur|Une laine sèche sur le genou de Nina.",
        "narrateur|Le cartable cale le banc, plus léger.",
    ),
    (1, 3, 3): L(
        "narrateur|Raphaël referme l'histoire du doudou.",
        "enfant-f|J'ai attendu ta phrase.",
        "papa|Et lui, la tienne.",
        "narrateur|Nina referme le poing, au chaud.",
        "maman|Le doudou veille, sans le gant dedans.",
        "narrateur|La flaque tient seulement le ciel.",
    ),
    (2, 1, 1): L(
        "narrateur|Nino pose le ballon dans l'herbe, pas la boue.",
        "enfant-f|Le toboggan n'est plus si froid.",
        "maman|Ta main a un gant, maintenant.",
        "papa|Le lancer a changé de cible.",
        "narrateur|Une trace rouge sèche sur la rampe, mince.",
        "narrateur|Puis elle s'efface.",
    ),
    (2, 1, 2): L(
        "narrateur|Mila garde le ballon contre son ventre.",
        "enfant-f|La boue a perdu son morceau rouge.",
        "papa|Il est sur ta main, ce morceau.",
        "maman|Tu as parlé. Puis le lancer.",
        "narrateur|Le métal luit, sans laine collée.",
        "narrateur|Nina glisse un doigt, puis le retire, fière.",
    ),
    (2, 1, 3): L(
        "narrateur|Raphaël a compté jusqu'à dix, puis écouté.",
        "enfant-f|Le cartable sent moins l'école, plus le parc.",
        "maman|Après les nombres, on t'écoutait.",
        "papa|Le gant sèche, loin de la boue.",
        "narrateur|Le toboggan redevient seulement un toboggan.",
        "narrateur|La flaque, en bas, tient le ciel.",
    ),
    (2, 2, 1): L(
        "narrateur|Nino pose le seau du côté de l'herbe.",
        "enfant-f|L'eau sale reste dans le seau.",
        "papa|Le gant, lui, reste avec toi.",
        "maman|Vous avez choisi le versant.",
        "narrateur|Le seau pose une ombre ronde sur le métal.",
        "narrateur|Nina souffle. La laine se soulève.",
    ),
    (2, 2, 2): L(
        "narrateur|Mila n'a plus tapé. Le parc a un silence.",
        "enfant-f|Le gant est lourd, et propre.",
        "papa|Le bruit s'est tu pour ta voix.",
        "maman|Une goutte quitte l'index, dans le seau.",
        "narrateur|Le toboggan sonne moins. Il sèche.",
        "narrateur|Nina appuie la joue sur le rouge.",
    ),
    (2, 2, 3): L(
        "narrateur|Raphaël n'a plus de rivière. Juste un filet.",
        "enfant-f|Le gant n'a pas nagé.",
        "maman|Il a tenu, cette fois.",
        "papa|L'eau est partie. Le rouge est resté.",
        "narrateur|Nina secoue le gant. Un peu de boue saute.",
        "narrateur|Le ciel dans la flaque redevient bleu.",
    ),
    (2, 3, 1): L(
        "narrateur|Nino tient une oreille. Nina l'autre.",
        "enfant-f|Le doudou et le gant se touchent, secs.",
        "papa|Personne n'a lancé.",
        "maman|Une feuille quitte le toboggan, légère.",
        "narrateur|Le métal n'a plus de peluche dessus.",
        "narrateur|Nina range le gant contre sa joue.",
    ),
    (2, 3, 2): L(
        "narrateur|Mila se lève. Le doudou aussi.",
        "enfant-f|Mon genou n'écrase plus le rouge.",
        "papa|Il sèche à l'air, maintenant.",
        "maman|Elle s'est levée pour toi.",
        "narrateur|Le ciel dans la flaque a un point rouge.",
        "narrateur|Puis le point devient une main.",
    ),
    (2, 3, 3): L(
        "narrateur|Raphaël a rendu sa voix au doudou, puis à Nina.",
        "enfant-f|J'ai parlé après lui.",
        "maman|Et le gant a entendu, lui aussi.",
        "papa|La boue reste en bas. Vous, en haut.",
        "narrateur|Nina enfile le gant. Le métal paraît moins dur.",
        "narrateur|Le cartable attend, contre le banc.",
    ),
    (3, 1, 1): L(
        "narrateur|Nino pose le ballon au pied de la barrière.",
        "enfant-f|La chaîne des balançoires est moins glacée.",
        "papa|Ta main a une laine, maintenant.",
        "maman|Le coup est devenu un appui.",
        "narrateur|Le barreau nu brille, sans laine.",
        "narrateur|Nina serre le gant. Il ne pend plus.",
    ),
    (3, 1, 2): L(
        "narrateur|Mila plaque le ballon. Le rebond s'arrête.",
        "enfant-f|Un cliquetis court suit le gant, sur ma main.",
        "papa|La chaîne a compris que c'était fini.",
        "maman|Le rouge n'est plus un drapeau.",
        "narrateur|Nina balance un pied, la main au chaud.",
        "narrateur|Le ciel dans la flaque n'a plus de barreau.",
    ),
    (3, 1, 3): L(
        "narrateur|Raphaël n'a plus de tirs. Il a une écoute.",
        "enfant-f|Entre deux nombres, tu m'as entendue.",
        "maman|Le gant a quitté le haut.",
        "papa|Il sèche contre tes doigts.",
        "narrateur|La corneille s'envole. Le gant reste.",
        "narrateur|La balançoire se tait, vide et simple.",
    ),
    (3, 2, 1): L(
        "narrateur|Nino a les pieds par terre. Nina aussi.",
        "enfant-f|Le seau reste sous la balançoire, vide.",
        "papa|Ce n'était pas un tabouret.",
        "maman|Le rouge est descendu vers toi.",
        "narrateur|Nina enfile le gant. Le barreau est nu.",
        "narrateur|Une ombre de seau dort dans l'herbe.",
    ),
    (3, 2, 2): L(
        "narrateur|Mila a posé son bateau. La chaîne est libre.",
        "enfant-f|L'eau du gant a fait un rond, puis plus.",
        "papa|Le siège est redevenu un seau.",
        "maman|Le rouge est à sa place, sur toi.",
        "narrateur|Nina balance un pied, sans froid.",
        "narrateur|Le cartable cale le banc, comme au début.",
    ),
    (3, 2, 3): L(
        "narrateur|Raphaël a laissé le ciel dans le seau.",
        "enfant-f|J'ai attendu tes yeux.",
        "papa|Puis j'ai décroché.",
        "maman|Le gant descend, barreau après barreau, fini.",
        "narrateur|Nina souffle dans la laine. Un peu d'air chaud.",
        "narrateur|La flaque rend le ciel, sans le gant.",
    ),
    (3, 3, 1): L(
        "narrateur|Nino pose le doudou sur le banc, près du cartable.",
        "enfant-f|Le copain a laissé le rouge.",
        "maman|Le doudou veille, sans voler.",
        "papa|Ta main a le gant, pas le vent.",
        "narrateur|La barrière n'a plus rien à accrocher.",
        "narrateur|Nina serre le poing. Il répond, tiède.",
    ),
    (3, 3, 2): L(
        "narrateur|Mila arrête le passager. La chaîne se tait.",
        "enfant-f|Le gant est à moi, humide.",
        "papa|Il sèche en se balançant, sur toi.",
        "maman|Le passager a attendu, lui aussi.",
        "narrateur|Une feuille quitte la barrière, légère.",
        "narrateur|Nina sourit dans le rouge.",
    ),
    (3, 3, 3): L(
        "narrateur|Raphaël tient le doudou. Nina tient le gant.",
        "enfant-f|Chacun sa chose.",
        "papa|Toi le gant. Lui le doudou.",
        "maman|Le haut de la barrière est vide.",
        "narrateur|La flaque rend le ciel, sans le gant.",
        "narrateur|Le parc sent le sable, plus l'école.",
    ),
}


def t2_question(a: int) -> list[str]:
    ou = LIEU[a]["ou"]
    return L(
        f"narrateur|{ou.capitalize()}, Nina prend quoi ?",
        "papa|Le ballon, le seau, ou le doudou.",
    )


def t3_question(a: int, b: int) -> list[str]:
    return L(
        "narrateur|Quelqu'un arrive près du gant.",
        "maman|Nino, Mila, ou Raphaël ?",
    )


def pre(a: int) -> str:
    return f"CHK_T0001_P000{a}"


def write() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    scripts: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {}

    scripts["CHK_T0000_P0000"] = L(
        "narrateur|Après l'école, le parc fume un peu.",
        "narrateur|Une flaque tient le ciel.",
        "narrateur|Le bleu y tremble, minuscule.",
        "narrateur|Un gant rouge goutte sur la barrière.",
        "narrateur|Le toboggan luit, froid comme l'acier.",
        "narrateur|Ça sent le sable mouillé.",
        "narrateur|Le cartable de Nina cale le banc.",
        "maman|Ton gant a trop d'eau, Nina.",
        "enfant-f|Il pèse trop.",
        "papa|Je l'ai mis là.",
        "papa|Pour qu'il sèche.",
        "narrateur|En ce moment, Nina tend les doigts.",
        "enfant-f|Je le mets.",
        "enfant-f|Je veux jouer.",
        "narrateur|Elle tire le gant, sans un mot.",
        "narrateur|L'eau tombe, froide sur le sable.",
        "narrateur|Le gant glisse et disparaît.",
        "enfant-f|Gant !",
        "narrateur|Papa parle du cartable avec maman.",
        "narrateur|Le cri passe à côté.",
        "papa|Tu disais quelque chose, Nina ?",
        "enfant-f|Mon gant !",
        "enfant-f|Il est parti.",
        "maman|Il est où, ton rouge ?",
        "narrateur|Une corneille penche la tête.",
        "narrateur|Une feuille colle au toboggan.",
        "enfant-f|Je le veux tout de suite.",
        "papa|On le cherche.",
        "papa|Tu nous guides ?",
    )
    sons["CHK_T0000_P0000"] = "enfants_parc,flaque"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|Le gant rouge a rebondi quelque part.",
        "maman|Le bac à sable, le toboggan, ou les balançoires ?",
    )
    extras["CHK_T0001_P0000"] = t3labs("le bac à sable", "le toboggan", "les balançoires")
    sons["CHK_T0001_P0000"] = ""

    for a in (1, 2, 3):
        p = pre(a)
        scripts[p] = T1[a]
        sons[p] = LIEU[a]["son"]
        q_lines, q_fields, emph = Q1[a]
        scripts[f"{p}_Q0001"] = q_lines
        extras[f"{p}_Q0001"] = q_fields
        sons[f"{p}_Q0001"] = ""
        scripts[f"{p}_C0001"] = C1[a]
        sons[f"{p}_C0001"] = ""
        scripts[f"{p}_T0002_P0000"] = t2_question(a)
        extras[f"{p}_T0002_P0000"] = t3labs("le ballon", "le seau", "le doudou")
        sons[f"{p}_T0002_P0000"] = ""
        for b in (1, 2, 3):
            p2 = f"{p}_T0002_P000{b}"
            scripts[p2] = T2[(a, b)]
            sons[p2] = OUTIL[b]["son"]
            scripts[f"{p2}_T0003_P0000"] = t3_question(a, b)
            extras[f"{p2}_T0003_P0000"] = t3labs("Nino", "Mila", "Raphaël")
            sons[f"{p2}_T0003_P0000"] = ""
            for c in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{c}"
                scripts[p3] = t3_lines(a, b, c)
                sons[p3] = "enfants_parc"
                fin = f"{p3}_F0001"
                scripts[fin] = ENDS[(a, b, c)]
                sons[fin] = "flaque"

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        kind = c.get("kind") or ""
        nc = make_chunk(c, scripts[cid], sons.get(cid, c.get("sons") or ""), 1.22, "medium")
        voice(nc, profile_for(cid, kind))
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc

    out = dict(src)
    out["fil_rouge"] = (
        "Après l'école, le gant rouge de Nina goutte sur la barrière. "
        "Elle le tire sans un mot : l'eau tombe, le gant disparaît, "
        "et son cri passe à côté de papa et maman. "
        "Nina le cherche au bac, au toboggan ou aux balançoires. "
        "Le ballon, le seau ou le doudou changent la manière de l'attraper. "
        "Nino, Mila ou Raphaël arrivent : prendre sans demander recouvre le rouge. "
        "Quand Nina dit s'il te plaît et attend, le gant revient, et la flaque rend le ciel."
    )
    out["title"] = "Le gant rouge de Nina"
    out["characters"] = "Nina, papa, maman"
    out["setting"] = "au parc, après l'école"
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
        "Nina veut son gant rouge tout de suite. Elle le tire sans demander : "
        "il glisse, le cri passe à côté. Chaque lieu change l'échec "
        "(sable, boue, barreau). Chaque objet change le geste "
        "(ballon qui recouvre, seau qui noie, doudou qui s'accroche). "
        "Chaque enfant change le climax (prise, attente, parole par-dessus). "
        "La demande s'il te plaît ouvre le geste. La flaque et le gant paient le début."
    )
    notes = (
        "- Titre noyau conservé. Parc après l'école. Troupe : Nina, Nino, Mila, Raphaël, papa, maman.\n"
        "- Labels T3 : Tom/Léa/Sami → Nino/Mila/Raphaël. Graphe `chunk_id` inchangé.\n"
        "- Leçon COL.ECO.001 vécue (demande / tour de parole), jamais dite. Un merci adulte, vécu.\n"
        "- Première idée ratée dès l'ouverture, puis un échec propre à chaque T1/T2/T3.\n"
        "- 27 fins textuellement distinctes. TTS par fonction (profiles example2).\n"
        "- Tics encore/déjà/tout doux/calme et leçon maîtresse retirés.\n"
        f"- Mots par chemin : {min(path_words)}–{max(path_words)} (moy {sum(path_words)//len(path_words)})."
    )
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — Le gant rouge de Nina\n\n"
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
