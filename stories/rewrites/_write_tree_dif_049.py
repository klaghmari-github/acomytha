#!/usr/bin/env python3
"""TREE-DIF-049 — Les poissons de papier de Sarah, sur le tapis (N1, F-NAR-019)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-049"
N1 = LIMITS["N1"]
TITLE = "Les poissons de papier de Sarah, sur le tapis"
FIL = (
    "Dehors le vent tord la mare. Sarah veut une pêche sur le tapis, pour Nino, "
    "tout de suite. Elle crie trop fort : le poisson tombe, Nino ne tourne pas. "
    "Elle reprend tout bas. Le bâton, le seau bleu ou le poisson jaune lance "
    "le voyage : canapé, table, tapis tiède. Nino tient sa chanson, son garage, "
    "ou un pied nu. Elle attend, glisse une autre idée, ou accepte un non. "
    "Les poissons jaunes finissent dans le seau, ou lui gardent une place."
)
CHARS = "Sarah, Nino, papa, maman"
SETTING = "salon : canapé, table, tapis près du radiateur"
TICS = ("tout doux", "tout calme", "on lève la main", "puis on parle", "c'est du bon travail")
CALQUES = (
    "on va apprendre", "voici le geste", "l'histoire est finie",
    "la première", "la deuxième", "la troisième", "bravo tu as", "bon travail",
    "inviter sans forcer", "accepter plusieurs", "kenzo", "lina", "coussin",
    "le fort", "tomate", "panier rouge", "figuier", "la cuisine", "le jardin",
    "la chambre", "les cubes", "dînette", "dinette", "wagon", "sifflet",
    "capitaine", "plic", "volet jaune", "il faut attendre",
)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp:
        e = esc(emp)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict) -> str:
    body = text
    emp = m.get("emphasis")
    if emp:
        body = body.replace(emp, f"<emphasis>{emp}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitch_tag"):
        body = f"<{m['pitch_tag']}>{body}</{m['pitch_tag']}>"
    pause = m["pause"]
    tail = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return f"{body}{tail}".strip()


PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="papier jaune",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=la_mare_dehors_refuse_et_Nino_n_entend_pas; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_pêche_peut_chercher_Nino; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=la_premiere_invite_rate; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=decouragement; intensite=2; destinataire=enfant; sous_texte=Nino_a_son_rythme; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis=None,
        note="arc=résolution; intention=faire_vivre_l_invite; emotion=soulagement; intensite=2; destinataire=enfant; sous_texte=oui_non_ou_une_autre_idee; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="poisson",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_mare_de_papier_a_trouve_sa_place; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(pairs: list[tuple[str, str]], where: str) -> None:
    prev = ""
    run = 1
    for role, ph in pairs:
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{where} {n}>{N1}: {ph}")
        if n == 0:
            raise SystemExit(f"{where} vide")
        if "|" in ph:
            raise SystemExit(f"{where} pipe: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"{where} ponctuation: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"{where} {marks} phrases: {ph}")
        low = ph.lower()
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"{where} tic « {tic} »: {ph}")
        if role == "narrateur":
            tok = ph.split()[0].lower()
            if tok == prev:
                run += 1
                if run >= 4:
                    raise SystemExit(f"{where} puces « {tok} »")
            else:
                run = 1
                prev = tok
        else:
            run = 1
            prev = ""


def voice(old: dict, pairs: list[tuple[str, str]], profile: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    vet(pairs, old["chunk_id"])
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if "note" in extra:
        m["note"] = extra["note"]
    lines = [f"{r}|{p}" for r, p in pairs]
    text, script = from_script(lines)
    out = deepcopy(old)
    out["text"] = text
    out["script"] = script
    out["sons"] = extra.get("sons", old.get("sons") or "")
    if out["sons"] is None:
        out["sons"] = ""
    out["text_ssml"] = ssml(text, m)
    out["text_xai_tags"] = xai(text, m)
    out["rate_wpm"] = m["wpm"]
    out["rate_label"] = m["rate"]
    out["speed_xai"] = m["speed"]
    out["length_scale_piper"] = m["piper"]
    out["pitch_label"] = m["pitch"]
    out["pitch_ssml"] = m["pitch_ssml"]
    out["pitch_xai_tag"] = m["pitch_tag"]
    out["volume_label"] = m["volume"]
    out["volume_db"] = m["db"]
    out["emphasis_words"] = m.get("emphasis") or ""
    out["pause_before_ms"] = extra.get("pause_before", 0)
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
    out["notes"] = extra.get("note", m["note"])
    out["night_policy"] = extra.get("night_policy", "play")
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        out[k] = v
    return out


def L(*rows: tuple[str, str]) -> list[tuple[str, str]]:
    return list(rows)


T1 = {
    1: {
        "lab": "le bâton",
        "ans": "bâton",
        "acc": "bâton | le bâton | le bois | d'abord le bâton",
        "retry": "Sarah a pris le bâton.",
        "ok": "Oui, le bâton.",
        "emphasis": "bâton",
        "sons": "bois,ficelle",
    },
    2: {
        "lab": "le seau bleu",
        "ans": "seau",
        "acc": "seau | le seau | le seau bleu | d'abord le seau",
        "retry": "Sarah a pris le seau.",
        "ok": "Oui, le seau bleu.",
        "emphasis": "seau bleu",
        "sons": "seau,bois",
    },
    3: {
        "lab": "le poisson jaune",
        "ans": "poisson",
        "acc": "poisson | le poisson | un poisson | le papier",
        "retry": "Sarah a coupé un poisson.",
        "ok": "Oui, le poisson jaune.",
        "emphasis": "poisson jaune",
        "sons": "papier,ciseaux",
    },
}

T2_LABS = ("la boîte à musique", "le camion jaune", "les chaussons")
T3_LABS = {
    1: ("attendre la chanson", "parler tout bas", "s'asseoir à côté"),
    2: ("laisser garer", "un poisson dedans", "garder le seau"),
    3: ("aider un peu", "un tout petit regard", "proposer plus tard"),
}
T2_SONS = {1: "boite-musique", 2: "roues", 3: "pas"}
T3_SONS = {
    1: {1: "boite-musique", 2: "papier", 3: "tapis"},
    2: {1: "roues", 2: "papier,roues", 3: "seau"},
    3: {1: "chausson", 2: "papier", 3: "radiateur"},
}
FIN_SONS = {
    1: "boite-musique,radiateur",
    2: "roues,seau",
    3: "chausson,radiateur",
}


OPENING = L(
    ("narrateur", "Au bord du village, le vent tord l'eau."),
    ("narrateur", "La petite maison sent le savon chaud."),
    ("narrateur", "Sarah y vit avec papa et maman."),
    ("narrateur", "Nino est venu jouer, après le goûter."),
    ("papa", "Dehors, la mare a trop de vagues."),
    ("maman", "Le tapis du salon est presque sec."),
    ("narrateur", "Un seau bleu attend près du radiateur."),
    ("narrateur", "Du papier jaune brille sur la table."),
    ("enfant-f", "Je fais une pêche, pour Nino !"),
    ("narrateur", "En ce moment, elle coupe un poisson."),
    ("narrateur", "Elle crie vers le canapé, trop fort."),
    ("enfant-f", "Nino, viens pêcher tout de suite !"),
    ("narrateur", "Nino ne tourne pas la tête."),
    ("narrateur", "Le poisson glisse et tombe à plat."),
    ("enfant-f", "Il n'a pas entendu."),
    ("papa", "Tu lui proposes, sans crier ?"),
    ("enfant-f", "Oui, je prépare d'abord."),
    ("papa", "Merci, tu as posé le poisson."),
)

T1_CHOICE = L(
    ("narrateur", "Le tapis attend, un peu rêche."),
    ("narrateur", "Trois affaires peuvent commencer la pêche."),
    ("papa", "On commence par quoi, Sarah ?"),
)


def t1_passage(t1: int) -> list[tuple[str, str]]:
    if t1 == 1:
        return L(
            ("narrateur", "Sarah prend le bâton, un peu rêche."),
            ("enfant-f", "Il sent le savon, sur la ficelle."),
            ("maman", "La ficelle fera un pont, plus tard."),
            ("narrateur", "Elle grimpe sur le canapé, vite."),
            ("enfant-f", "Nino, pêche d'en haut !"),
            ("narrateur", "Sa voix tombe trop loin, trop vite."),
            ("narrateur", "Nino ne lève pas les yeux."),
            ("enfant-f", "Il n'a pas vu le pont."),
            ("papa", "Le seau et le poisson, avec toi ?"),
            ("narrateur", "Elle les ramène sur le canapé."),
        )
    if t1 == 2:
        return L(
            ("narrateur", "Sarah prend le seau bleu, froid."),
            ("enfant-f", "Il sent un peu l'eau."),
            ("papa", "Pose-le sur la table, sans le jeter."),
            ("narrateur", "Un petit toc sonne contre le bois."),
            ("enfant-f", "Nino, le port est là !"),
            ("narrateur", "Elle pousse le seau vers ses pieds."),
            ("narrateur", "Nino contourne le bleu, sans regarder."),
            ("enfant-f", "Il n'est pas entré."),
            ("maman", "Le bâton et le poisson, près de toi ?"),
            ("narrateur", "Les trois affaires restent sur la table."),
        )
    return L(
        ("narrateur", "Sarah prend le poisson jaune, plat."),
        ("enfant-f", "Il a un œil rond."),
        ("maman", "Tiens-le à plat, sans le froisser."),
        ("narrateur", "Puis elle s'allonge sur le tapis."),
        ("enfant-f", "Nino, ma mare est tiède !"),
        ("narrateur", "Elle pose le papier sur son genou."),
        ("narrateur", "Nino le chasse d'un doigt, distrait."),
        ("enfant-f", "Il n'a pas voulu."),
        ("papa", "Le bâton et le seau, avec toi ?"),
        ("narrateur", "Rien ne reste sur la table."),
    )


def t1_q(t1: int) -> list[tuple[str, str]]:
    if t1 == 1:
        return L(
            ("narrateur", "Sarah tient le bois, contre sa joue."),
            ("maman", "Elle a pris quoi, d'abord ?"),
        )
    if t1 == 2:
        return L(
            ("narrateur", "Le plastique bleu est dans ses mains."),
            ("papa", "Elle a pris quoi, d'abord ?"),
        )
    return L(
        ("narrateur", "Le papier jaune tremble entre ses doigts."),
        ("maman", "Elle a coupé quoi ?"),
    )


def t1_confirm(t1: int) -> list[tuple[str, str]]:
    if t1 == 1:
        return L(
            ("enfant-f", "Le bâton."),
            ("maman", "Oui, le bois rêche."),
            ("narrateur", "La ficelle pend vers le tapis."),
            ("narrateur", "Le canapé fait une rive haute."),
            ("enfant-f", "Nino est dans le salon."),
            ("papa", "Je l'entends, plus loin."),
            ("maman", "Vous allez le trouver."),
            ("enfant-f", "Je lui propose la mare."),
        )
    if t1 == 2:
        return L(
            ("enfant-f", "Le seau."),
            ("papa", "Oui, le bleu de la table."),
            ("narrateur", "Une ombre ronde dort dessus."),
            ("narrateur", "Le bois tient le bord du seau."),
            ("enfant-f", "Nino est dans le salon."),
            ("maman", "Je l'entends, plus loin."),
            ("papa", "Le port attend, sur le bois."),
            ("enfant-f", "Je lui propose le seau."),
        )
    return L(
        ("enfant-f", "Le poisson."),
        ("maman", "Oui, le papier jaune."),
        ("narrateur", "Un peu d'air lève le papier."),
        ("narrateur", "Le radiateur chante, tout près."),
        ("enfant-f", "Nino est dans le salon."),
        ("papa", "Je l'entends, plus loin."),
        ("maman", "Le tapis reste sous toi."),
        ("enfant-f", "Je lui propose la mare."),
    )


def t2_choice(t1: int) -> list[tuple[str, str]]:
    if t1 == 1:
        return L(
            ("narrateur", "Nino est dans le salon, pas loin."),
            ("narrateur", "Une boîte à musique tinte, près du tapis."),
            ("narrateur", "Un camion roule entre les livres."),
            ("narrateur", "Des chaussons attendent au bord."),
            ("papa", "On va vers quoi, Sarah ?"),
        )
    if t1 == 2:
        return L(
            ("narrateur", "Nino reste dans le salon, quelque part."),
            ("narrateur", "La boîte à musique tinte, tout près."),
            ("narrateur", "Le camion jaune frotte une table."),
            ("narrateur", "Un chausson orphelin attend."),
            ("maman", "On va vers quoi, Sarah ?"),
        )
    return L(
        ("narrateur", "Nino n'a pas quitté le salon."),
        ("narrateur", "Sa boîte à musique tinte, basse."),
        ("narrateur", "Son camion cherche une place."),
        ("narrateur", "Un pied nu cherche aussi."),
        ("papa", "On va vers quoi, Sarah ?"),
    )


def t2_scene(t1: int, t2: int) -> list[tuple[str, str]]:
    if t2 == 1:
        if t1 == 1:
            return L(
                ("narrateur", "Sarah redescend du canapé, sans sauter."),
                ("narrateur", "Nino tourne la petite clé, absorbé."),
                ("enfant-f", "Nino, la mare est prête."),
                ("narrateur", "Une note tinte, toujours la même."),
                ("copain", "Elle n'a pas dit au revoir."),
                ("enfant-f", "On pêche après la note ?"),
                ("copain", "Cette chanson, d'abord."),
                ("maman", "La boîte tient sa voix."),
                ("papa", "Tu restes près de lui ?"),
            )
        if t1 == 2:
            return L(
                ("narrateur", "Sarah pose le seau près de la boîte."),
                ("narrateur", "Nino penche l'oreille, collé à la clé."),
                ("enfant-f", "Nino, le seau est bleu."),
                ("narrateur", "La clé glisse, puis reprend."),
                ("copain", "Elle n'a pas dit au revoir."),
                ("enfant-f", "Tu viens à la table ?"),
                ("copain", "Cette chanson, d'abord."),
                ("papa", "Il suit la note, sans lever les yeux."),
                ("maman", "Tu restes près de lui ?"),
            )
        return L(
            ("narrateur", "Le poisson jaune tremble près du tapis."),
            ("narrateur", "Nino tourne la clé, très bas."),
            ("enfant-f", "Nino, ma mare est tiède."),
            ("narrateur", "Le radiateur chante avec la boîte."),
            ("copain", "Elle n'a pas dit au revoir."),
            ("enfant-f", "Tu viens t'allonger ?"),
            ("copain", "Cette chanson, d'abord."),
            ("maman", "La note n'est pas partie."),
            ("papa", "Tu restes près de lui ?"),
        )
    if t2 == 2:
        if t1 == 1:
            return L(
                ("narrateur", "Un camion jaune passe sous le canapé."),
                ("narrateur", "Nino le pousse entre deux livres."),
                ("enfant-f", "Nino, on pêche d'en haut."),
                ("copain", "Il va au garage."),
                ("enfant-f", "Tu viens sur le canapé ?"),
                ("copain", "Le garage, d'abord."),
                ("narrateur", "Les roues font un petit rrr."),
                ("maman", "Il range sa route, livre par livre."),
                ("papa", "Tu fais quoi, alors ?"),
            )
        if t1 == 2:
            return L(
                ("narrateur", "Nino a son camion, à la table."),
                ("narrateur", "Le seau bleu attend tout près."),
                ("enfant-f", "Nino, tu veux un poisson ?"),
                ("copain", "Il va au garage."),
                ("enfant-f", "On le met dans le seau ?"),
                ("copain", "Le garage, d'abord."),
                ("narrateur", "Une roue frotte le bois, tout sec."),
                ("papa", "Le camion n'est pas rentré."),
                ("maman", "Tu fais quoi, alors ?"),
            )
        return L(
            ("narrateur", "Nino pousse le camion sur le tapis."),
            ("narrateur", "Une roue passe sur la ficelle."),
            ("enfant-f", "Nino, la mare est tiède."),
            ("copain", "Il va au garage."),
            ("enfant-f", "Tu t'allonges avec moi ?"),
            ("copain", "Le garage, d'abord."),
            ("narrateur", "Le poisson tremble, tout plat."),
            ("maman", "Il cherche sa place, entre les livres."),
            ("papa", "Tu fais quoi, alors ?"),
        )
    if t1 == 1:
        return L(
            ("narrateur", "Nino s'assoit au bord du tapis."),
            ("copain", "J'ai un pied froid, Sarah."),
            ("enfant-f", "On pêche d'en haut, après."),
            ("narrateur", "Un chausson manque, sous le canapé."),
            ("enfant-f", "Tu viens sur le canapé ?"),
            ("copain", "L'autre chausson, d'abord."),
            ("papa", "Il fouille, le front un peu plissé."),
            ("maman", "Le second n'est pas là."),
            ("papa", "Tu l'aides, ou tu attends ?"),
        )
    if t1 == 2:
        return L(
            ("narrateur", "Nino quitte la table, un pied nu."),
            ("copain", "J'ai un pied froid, Sarah."),
            ("enfant-f", "Le seau est vide, pour nous."),
            ("narrateur", "Le chausson droit est chaud, lui."),
            ("enfant-f", "Tu reviens au seau ?"),
            ("copain", "L'autre chausson, d'abord."),
            ("maman", "Il cherche, les épaules un peu hautes."),
            ("papa", "Le second n'est pas là."),
            ("maman", "Tu l'aides, ou tu attends ?"),
        )
    return L(
        ("narrateur", "Nino se tient près du radiateur."),
        ("copain", "J'ai un pied froid, Sarah."),
        ("enfant-f", "Ma mare est tiède, pour deux."),
        ("narrateur", "Il serre un chausson, contre lui."),
        ("enfant-f", "Tu t'allonges avec moi ?"),
        ("copain", "L'autre chausson, d'abord."),
        ("papa", "Il cherche, tout près du métal."),
        ("maman", "Le second n'est pas là."),
        ("papa", "Tu l'aides, ou tu attends ?"),
    )


def t3_choice(t2: int) -> list[tuple[str, str]]:
    if t2 == 1:
        return L(
            ("narrateur", "La boîte à musique tourne, sans fin."),
            ("papa", "Attendre, parler tout bas, ou s'asseoir ?"),
        )
    if t2 == 2:
        return L(
            ("narrateur", "Le camion n'est pas rangé."),
            ("maman", "Laisser garer, un poisson, ou garder ?"),
        )
    return L(
        ("narrateur", "Un chausson n'est pas chaussé."),
        ("papa", "Aider, un petit regard, ou plus tard ?"),
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[tuple[str, str]]:
    if t2 == 1 and t3 == 1:
        wait = {
            1: ("narrateur", "La ficelle reste haute, sans bouger."),
            2: ("narrateur", "Le seau bleu reste loin de la clé."),
            3: ("narrateur", "Le papier reste plat, sans froisser."),
        }[t1]
        return L(
            ("enfant-f", "J'attends la dernière note."),
            ("copain", "Merci, Sarah."),
            ("narrateur", "Elle compte les tintes, sur ses doigts."),
            wait,
            ("narrateur", "La boîte s'arrête, pile."),
            ("copain", "Elle a dit au revoir."),
            ("enfant-f", "Tu viens, alors ?"),
            ("copain", "Oui, j'apporte la clé."),
            ("papa", "La dernière note était à lui."),
        )
    if t2 == 1 and t3 == 2:
        near = {
            1: ("narrateur", "Elle glisse un poisson contre le canapé."),
            2: ("narrateur", "Elle glisse un poisson contre la table."),
            3: ("narrateur", "Elle glisse un poisson contre le tapis."),
        }[t1]
        return L(
            ("enfant-f", "Nino, un poisson t'écoute."),
            near,
            ("narrateur", "Sa voix reste tout bas, près de lui."),
            ("copain", "Il a une oreille, lui aussi ?"),
            ("enfant-f", "Oui, une toute petite."),
            ("copain", "Je viens, alors."),
            ("narrateur", "Il pose la clé, sans la perdre."),
            ("papa", "Tu as parlé tout contre lui."),
            ("maman", "Il a dit oui, tout seul."),
        )
    if t2 == 1 and t3 == 3:
        sit = {
            1: ("narrateur", "Sarah s'assoit au pied du canapé."),
            2: ("narrateur", "Sarah s'assoit, le seau sur les genoux."),
            3: ("narrateur", "Sarah s'assoit près du radiateur."),
        }[t1]
        return L(
            ("enfant-f", "Je m'assois à côté."),
            sit,
            ("narrateur", "Elle ne touche pas la clé."),
            ("copain", "Tu entends le ding, toi aussi ?"),
            ("enfant-f", "Oui, dans le ventre."),
            ("narrateur", "Un dernier ding les fait sauter."),
            ("copain", "On pêche, après ça."),
            ("papa", "Tu as écouté sa boîte."),
            ("maman", "C'est lui qui a dit après."),
        )
    if t2 == 2 and t3 == 1:
        wait = {
            1: ("narrateur", "Le canapé garde sa rive, sans bouger."),
            2: ("narrateur", "Le seau bleu garde son bois, sans bouger."),
            3: ("narrateur", "Le poisson jaune garde le tapis, plat."),
        }[t1]
        return L(
            ("enfant-f", "J'attends le garage."),
            ("copain", "Merci, Sarah."),
            wait,
            ("narrateur", "Le camion se glisse entre deux livres."),
            ("copain", "Il est rentré, maintenant."),
            ("enfant-f", "Tu viens, alors ?"),
            ("copain", "Oui, je laisse les roues."),
            ("papa", "Le garage a fermé tout seul."),
            ("maman", "Il a dit oui, après."),
        )
    if t2 == 2 and t3 == 2:
        offer = {
            1: ("narrateur", "Elle pose le poisson sur le capot."),
            2: ("narrateur", "Elle pose le poisson sur le bois."),
            3: ("narrateur", "Elle pose le poisson sur une roue."),
        }[t1]
        return L(
            ("enfant-f", "Nino, un poisson voyageur ?"),
            offer,
            ("copain", "Il tient, sur le camion ?"),
            ("enfant-f", "Tout plat, oui."),
            ("narrateur", "Le papier colle un peu, puis tient."),
            ("copain", "On va jusqu'au seau, alors."),
            ("enfant-f", "D'accord."),
            ("papa", "Le poisson a pris la route."),
            ("maman", "Il a choisi le voyage."),
        )
    if t2 == 2 and t3 == 3:
        side = {
            1: ("narrateur", "Le seau reste au pied du canapé."),
            2: ("narrateur", "Le seau reste sur la table."),
            3: ("narrateur", "Le seau reste près du radiateur."),
        }[t1]
        return L(
            ("copain", "Pas de poisson, Sarah."),
            ("enfant-f", "D'accord."),
            ("enfant-f", "Je pêche ici, alors."),
            side,
            ("narrateur", "Un poisson se colle à sa chaussette."),
            ("copain", "Il t'a pêchée, toi !"),
            ("enfant-f", "Je ris, d'à côté."),
            ("papa", "Tu as gardé ton seau."),
            ("maman", "Le camion est resté à lui."),
        )
    if t2 == 3 and t3 == 1:
        help_ = {
            1: ("narrateur", "Elle fouille sous le canapé, sans forcer."),
            2: ("narrateur", "Elle fouille sous la table, sans forcer."),
            3: ("narrateur", "Elle fouille près du radiateur, sans forcer."),
        }[t1]
        return L(
            ("enfant-f", "J'aide un peu."),
            help_,
            ("narrateur", "Un chausson chaud apparaît, enfin."),
            ("copain", "Il s'était caché !"),
            ("enfant-f", "Près du bord, oui."),
            ("narrateur", "Deux pieds, maintenant, tout chauds."),
            ("copain", "On peut pêcher, là."),
            ("papa", "Tu as cherché avec lui."),
            ("maman", "Le pied froid n'a plus froid."),
        )
    if t2 == 3 and t3 == 2:
        look = {
            1: ("narrateur", "Ils se penchent vers la rive du canapé."),
            2: ("narrateur", "Ils se penchent vers le seau, une seconde."),
            3: ("narrateur", "Ils se penchent vers la mare du tapis."),
        }[t1]
        return L(
            ("enfant-f", "Un tout petit regard, Nino ?"),
            ("copain", "Très petit, alors."),
            ("enfant-f", "D'accord."),
            look,
            ("narrateur", "Un poisson jaune brille, une seconde."),
            ("copain", "Il nage, presque."),
            ("narrateur", "Puis Nino reprend le chausson."),
            ("papa", "Tu as montré juste un peu."),
            ("maman", "Il a vu, puis choisi."),
        )
    later = {
        1: ("narrateur", "Le canapé garde sa rive, sans bruit."),
        2: ("narrateur", "La table garde le seau, sans bruit."),
        3: ("narrateur", "Le tapis garde sa mare, sans bruit."),
    }[t1]
    return L(
        ("enfant-f", "On pêche plus tard, alors ?"),
        ("copain", "Oui, plus tard."),
        ("enfant-f", "D'accord."),
        later,
        ("narrateur", "Nino serre le chausson, contre lui."),
        ("copain", "Garde un poisson pour moi."),
        ("enfant-f", "Il t'attend dans le seau."),
        ("papa", "Tu as dit une autre heure."),
        ("maman", "Le pied froid cherche, lui."),
    )


def fin_scene(t1: int, t2: int, t3: int) -> list[tuple[str, str]]:
    last = {
        (1, 1, 1): "Un peu de savon reste sur le papier.",
        (1, 1, 2): "La clé de la boîte dort contre le canapé.",
        (1, 1, 3): "Deux mains tiennent le bâton, collées.",
        (1, 2, 1): "Une roue jaune sent le tapis.",
        (1, 2, 2): "Un poisson plat dort sur le capot.",
        (1, 2, 3): "Deux jeux se parlent, sans se bousculer.",
        (1, 3, 1): "Un fil jaune passe sous le canapé.",
        (1, 3, 2): "Le radiateur reprend, plus bas.",
        (1, 3, 3): "La ficelle fait un pont, pour plus tard.",
        (2, 1, 1): "Le seau bleu garde un poisson plat.",
        (2, 1, 2): "La clé repose sur le bois de la table.",
        (2, 1, 3): "Deux mains tiennent le bord du seau.",
        (2, 2, 1): "Une roue jaune sent le bois de la table.",
        (2, 2, 2): "Un poisson plat dort dans le bleu.",
        (2, 2, 3): "Le camion et le seau restent chacun chez soi.",
        (2, 3, 1): "Deux chaussons chauds flanquent le seau bleu.",
        (2, 3, 2): "Le seau garde une seconde de lumière jaune.",
        (2, 3, 3): "Un poisson attend dans le bleu, à part.",
        (3, 1, 1): "Le tapis garde un fil, près du radiateur.",
        (3, 1, 2): "La clé dort sur le tapis tiède.",
        (3, 1, 3): "Deux ventres ont sauté, puis se sont allongés.",
        (3, 2, 1): "Une roue jaune a croisé la ficelle.",
        (3, 2, 2): "Un poisson voyageur s'endort dans le seau.",
        (3, 2, 3): "La chaussette de Sarah garde une écaille jaune.",
        (3, 3, 1): "Deux pieds chauds s'allongent sur la mare.",
        (3, 3, 2): "Le radiateur chante, et le seau écoute.",
        (3, 3, 3): "La mare du tapis garde un poisson pour lui.",
    }[(t1, t2, t3)]
    if t2 == 1 and t3 == 1:
        mid = {
            1: L(
                ("narrateur", "La ficelle tremble, puis un papier vient."),
                ("copain", "Il a mordu, Sarah ?"),
                ("enfant-f", "Oui, tout plat."),
                ("papa", "La chanson a laissé la place."),
                ("maman", "Le seau fait un petit bruit d'eau."),
                ("narrateur", "Nino pose la clé à côté du seau."),
                ("enfant-f", "La mare chante, maintenant."),
            ),
            2: L(
                ("narrateur", "Un papier glisse du bois vers le bleu."),
                ("copain", "Le port l'a eu, Sarah ?"),
                ("enfant-f", "Oui, il est rentré."),
                ("papa", "La note s'est tue, pile."),
                ("maman", "Le plastique bleu tient le poisson."),
                ("narrateur", "Nino pose la clé contre le seau."),
                ("enfant-f", "La table est un quai, maintenant."),
            ),
            3: L(
                ("narrateur", "Un papier nage vers le seau, tout plat."),
                ("copain", "Il a mordu, sur le tapis ?"),
                ("enfant-f", "Oui, près du radiateur."),
                ("papa", "La chanson a fini sa route."),
                ("maman", "Le tapis sent le savon, un peu."),
                ("narrateur", "Nino pose la clé près du papier."),
                ("enfant-f", "La mare est tiède, pour deux."),
            ),
        }[t1]
        return mid + L(("narrateur", last))
    if t2 == 1 and t3 == 2:
        mid = {
            1: L(
                ("narrateur", "Le poisson collé au canapé écoute, sans bouger."),
                ("enfant-f", "Il t'a attendu, tout bas."),
                ("copain", "J'ai dit oui, près de toi."),
                ("papa", "Ta voix n'a pas cassé la note."),
                ("maman", "Pêchez, maintenant, sans crier."),
                ("narrateur", "Nino tient le bâton, très calme."),
                ("enfant-f", "On tire ensemble, tout lent."),
            ),
            2: L(
                ("narrateur", "Le poisson collé au bois écoute, un peu."),
                ("enfant-f", "Il t'a attendu, contre la table."),
                ("copain", "J'ai dit oui, tout bas."),
                ("papa", "Ta voix a glissé sous la note."),
                ("maman", "Le seau peut servir, maintenant."),
                ("narrateur", "Nino tient le bord du bleu."),
                ("enfant-f", "On tire vers le port, ensemble."),
            ),
            3: L(
                ("narrateur", "Le poisson collé au tapis écoute, un peu."),
                ("enfant-f", "Il t'a attendu, près du métal."),
                ("copain", "J'ai dit oui, contre le tapis."),
                ("papa", "Ta voix n'a pas froissé le papier."),
                ("maman", "Allongez-vous, si vous voulez."),
                ("narrateur", "Nino tient le bâton, tout bas."),
                ("enfant-f", "On tire sur la mare, ensemble."),
            ),
        }[t1]
        return mid + L(("narrateur", last))
    if t2 == 1 and t3 == 3:
        mid = {
            1: L(
                ("narrateur", "Après le ding, la ficelle descend."),
                ("copain", "On a sauté, d'abord."),
                ("enfant-f", "Puis tu as dit : on pêche."),
                ("maman", "Un ding, puis un poisson."),
                ("papa", "Le salon redevient tiède."),
                ("narrateur", "Nino rit, tout petit."),
                ("enfant-f", "La mare a attendu le ding."),
            ),
            2: L(
                ("narrateur", "Après le ding, le seau avance d'un doigt."),
                ("copain", "On a sauté, près de la table."),
                ("enfant-f", "Puis tu as dit : le port."),
                ("maman", "Un ding, puis un plouf muet."),
                ("papa", "Le bois de la table est tiède."),
                ("narrateur", "Nino rit, les yeux plissés."),
                ("enfant-f", "Le seau a attendu le ding."),
            ),
            3: L(
                ("narrateur", "Après le ding, ils s'allongent enfin."),
                ("copain", "On a sauté, près du métal."),
                ("enfant-f", "Puis tu as dit : la mare."),
                ("maman", "Un ding, puis le tapis."),
                ("papa", "Le radiateur reprend sa chanson."),
                ("narrateur", "Nino rit, le nez au tapis."),
                ("enfant-f", "La mare a attendu le ding."),
            ),
        }[t1]
        return mid + L(("narrateur", last))
    if t2 == 2 and t3 == 1:
        mid = {
            1: L(
                ("narrateur", "Le camion dort entre les livres."),
                ("copain", "Le garage est fermé, Sarah."),
                ("enfant-f", "Tu as dit oui, après."),
                ("papa", "Les roues se sont tues."),
                ("maman", "Le poisson glisse vers le seau."),
                ("narrateur", "Nino souffle sur la nageoire, tout petit."),
                ("enfant-f", "Il nage, dans le bleu."),
            ),
            2: L(
                ("narrateur", "Le camion dort contre un livre, à la table."),
                ("copain", "Le garage est fermé, Sarah."),
                ("enfant-f", "Tu as dit oui, après le bois."),
                ("papa", "Les roues ne grattent plus."),
                ("maman", "Le poisson glisse du capot au seau."),
                ("narrateur", "Nino souffle, tout près du bleu."),
                ("enfant-f", "Le port est ouvert, maintenant."),
            ),
            3: L(
                ("narrateur", "Le camion dort entre deux livres, au tapis."),
                ("copain", "Le garage est fermé, Sarah."),
                ("enfant-f", "Tu as dit oui, après les roues."),
                ("papa", "Le rrr s'est tu."),
                ("maman", "Le poisson glisse vers le seau tiède."),
                ("narrateur", "Nino souffle, le nez au papier."),
                ("enfant-f", "Il nage, sur la mare."),
            ),
        }[t1]
        return mid + L(("narrateur", last))
    if t2 == 2 and t3 == 2:
        mid = {
            1: L(
                ("narrateur", "Le camion roule jusqu'au seau, sous le canapé."),
                ("enfant-f", "Le voyageur descend, tout plat."),
                ("copain", "Il a tenu sur le capot."),
                ("papa", "Vous avez fait une route, ensemble."),
                ("maman", "Le seau devient un port, maintenant."),
                ("narrateur", "Nino pousse une dernière fois, sans forcer."),
                ("enfant-f", "On reste un peu, d'en haut."),
            ),
            2: L(
                ("narrateur", "Le camion roule jusqu'au seau, sur la table."),
                ("enfant-f", "Le voyageur descend dans le bleu."),
                ("copain", "Il a tenu sur le bois."),
                ("papa", "Vous avez fait un quai, ensemble."),
                ("maman", "Le seau devient un port, trop petit."),
                ("narrateur", "Nino pousse une dernière fois, tout lent."),
                ("enfant-f", "On reste un peu, sur le bois."),
            ),
            3: L(
                ("narrateur", "Le camion roule jusqu'au seau, sur le tapis."),
                ("enfant-f", "Le voyageur descend, près du métal."),
                ("copain", "Il a tenu sur une roue."),
                ("papa", "Vous avez fait une piste, ensemble."),
                ("maman", "Le seau devient un port, tiède."),
                ("narrateur", "Nino pousse une dernière fois, tout bas."),
                ("enfant-f", "On reste un peu, sur la mare."),
            ),
        }[t1]
        return mid + L(("narrateur", last))
    if t2 == 2 and t3 == 3:
        mid = {
            1: L(
                ("narrateur", "Le camion reste sous le canapé."),
                ("copain", "Tu n'as pas pris mes roues."),
                ("enfant-f", "Tu avais dit non."),
                ("papa", "Son garage est resté à lui."),
                ("maman", "La chaussette a eu un poisson."),
                ("narrateur", "Nino rit, puis pousse, plus loin."),
                ("enfant-f", "Je pêche, tu roules."),
            ),
            2: L(
                ("narrateur", "Le camion reste au bout de la table."),
                ("copain", "Tu n'as pas pris mes roues."),
                ("enfant-f", "Tu avais dit non, au seau."),
                ("papa", "Son garage est resté sur le bois."),
                ("maman", "La chaussette a pêché, toute seule."),
                ("narrateur", "Nino rit, puis pousse vers les livres."),
                ("enfant-f", "Je pêche ici, tu roules là."),
            ),
            3: L(
                ("narrateur", "Le camion reste au bord du tapis."),
                ("copain", "Tu n'as pas pris mes roues."),
                ("enfant-f", "Tu avais dit non, à la mare."),
                ("papa", "Son garage est resté au tapis."),
                ("maman", "La chaussette a un poisson collé."),
                ("narrateur", "Nino rit, puis pousse vers le métal."),
                ("enfant-f", "Je nage, tu roules."),
            ),
        }[t1]
        return mid + L(("narrateur", last))
    if t2 == 3 and t3 == 1:
        mid = {
            1: L(
                ("narrateur", "Les deux chaussons sont chauds, enfin."),
                ("copain", "Le pied froid n'a plus froid."),
                ("enfant-f", "On peut pêcher, là."),
                ("papa", "Vous avez cherché ensemble."),
                ("maman", "Le seau attend, au pied du canapé."),
                ("narrateur", "Nino s'allonge, le pied au chaud."),
                ("enfant-f", "La mare est tiède, pour deux."),
            ),
            2: L(
                ("narrateur", "Les deux chaussons sont chauds, sous la table."),
                ("copain", "Le pied froid n'a plus froid."),
                ("enfant-f", "On peut vider le seau, là."),
                ("papa", "Vous avez fouillé ensemble."),
                ("maman", "Le seau attend, sur le bois."),
                ("narrateur", "Nino s'assoit, le pied au chaud."),
                ("enfant-f", "Le port est tiède, pour deux."),
            ),
            3: L(
                ("narrateur", "Les deux chaussons sont chauds, près du métal."),
                ("copain", "Le pied froid n'a plus froid."),
                ("enfant-f", "On peut s'allonger, là."),
                ("papa", "Vous avez cherché près du radiateur."),
                ("maman", "Le seau attend, sur le tapis."),
                ("narrateur", "Nino s'allonge, le pied au chaud."),
                ("enfant-f", "La mare est tiède, pour deux."),
            ),
        }[t1]
        return mid + L(("narrateur", last))
    if t2 == 3 and t3 == 2:
        mid = {
            1: L(
                ("narrateur", "Le petit regard est fini, sous le canapé."),
                ("copain", "Il nageait, presque."),
                ("enfant-f", "Tu as vu, une seconde."),
                ("papa", "Un œil a suffi."),
                ("maman", "Le chausson est chaussé, maintenant."),
                ("narrateur", "Nino s'assoit au bord du seau."),
                ("enfant-f", "On tire, sans crier."),
            ),
            2: L(
                ("narrateur", "Le petit regard est fini, vers le seau."),
                ("copain", "Il nageait, dans le bleu."),
                ("enfant-f", "Tu as vu, une seconde."),
                ("papa", "Un œil a suffi, sur la table."),
                ("maman", "Le chausson est chaussé, lui aussi."),
                ("narrateur", "Nino s'assoit au bord du bois."),
                ("enfant-f", "On tire vers le port, sans crier."),
            ),
            3: L(
                ("narrateur", "Le petit regard est fini, sur le tapis."),
                ("copain", "Il nageait, près du métal."),
                ("enfant-f", "Tu as vu, une seconde."),
                ("papa", "Un œil a suffi, tout bas."),
                ("maman", "Le chausson est chaussé, près du radiateur."),
                ("narrateur", "Nino s'assoit au bord de la mare."),
                ("enfant-f", "On tire, tout lent."),
            ),
        }[t1]
        return mid + L(("narrateur", last))
    mid = {
        1: L(
            ("narrateur", "Nino enfile, un instant, sous le canapé."),
            ("enfant-f", "Plus tard, il a dit."),
            ("enfant-f", "Le poisson t'attend dans le seau."),
            ("papa", "Tu as dit une autre heure."),
            ("maman", "Le pied froid cherche, lui."),
            ("narrateur", "Sarah laisse un poisson à part."),
            ("enfant-f", "La mare t'attend, Nino."),
        ),
        2: L(
            ("narrateur", "Nino enfile, un instant, sous la table."),
            ("enfant-f", "Plus tard, il a dit."),
            ("enfant-f", "Le poisson t'attend dans le bleu."),
            ("papa", "Tu as dit une autre heure, à la table."),
            ("maman", "Le pied froid cherche, sous le bois."),
            ("narrateur", "Sarah laisse un poisson au bord du seau."),
            ("enfant-f", "Le port t'attend, Nino."),
        ),
        3: L(
            ("narrateur", "Nino enfile, un instant, près du métal."),
            ("enfant-f", "Plus tard, il a dit."),
            ("enfant-f", "Le poisson t'attend sur le tapis."),
            ("papa", "Tu as dit une autre heure, tout bas."),
            ("maman", "Le pied froid cherche, près du radiateur."),
            ("narrateur", "Sarah laisse un poisson à part, plat."),
            ("enfant-f", "La mare t'attend, Nino."),
        ),
    }[t1]
    return mid + L(("narrateur", last))


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def build() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "vent,ciseaux,papier"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"], T1_CHOICE, "choice",
        extra={"sons": "", "fields": t3lab("le bâton", "le seau bleu", "le poisson jaune")},
    )

    for t1 in (1, 2, 3):
        o = T1[t1]
        p = f"CHK_T0001_P000{t1}"
        by[p] = voice(
            by_old[p], t1_passage(t1), "action",
            extra={"sons": o["sons"], "emphasis": o["emphasis"]},
        )
        by[f"{p}_Q0001"] = voice(
            by_old[f"{p}_Q0001"], t1_q(t1), "clue",
            extra={"sons": "", "emphasis": o["ans"], "fields": {
                "expected_answer": o["ans"],
                "accepted_examples": o["acc"],
                "retry_prompt": o["retry"],
                "engine_ok_text": o["ok"],
                "engine_near_text": "Tu es tout près. Reprenons l'indice.",
            }},
        )
        by[f"{p}_C0001"] = voice(
            by_old[f"{p}_C0001"], t1_confirm(t1), "confirm",
            extra={"sons": "", "emphasis": o["emphasis"]},
        )
        by[f"{p}_T0002_P0000"] = voice(
            by_old[f"{p}_T0002_P0000"], t2_choice(t1), "choice",
            extra={"sons": "", "fields": t3lab(*T2_LABS)},
        )
        for t2 in (1, 2, 3):
            sp = f"{p}_T0002_P000{t2}"
            by[sp] = voice(
                by_old[sp], t2_scene(t1, t2), "obstacle",
                extra={"sons": T2_SONS[t2], "emphasis": T2_LABS[t2 - 1].split()[-1]},
            )
            by[f"{sp}_T0003_P0000"] = voice(
                by_old[f"{sp}_T0003_P0000"], t3_choice(t2), "choice",
                extra={"sons": "", "fields": t3lab(*T3_LABS[t2])},
            )
            for t3 in (1, 2, 3):
                leaf = f"{sp}_T0003_P000{t3}"
                by[leaf] = voice(
                    by_old[leaf], t3_scene(t1, t2, t3), "resolution",
                    extra={"sons": T3_SONS[t2][t3], "emphasis": "Sarah"},
                )
                fin = f"{leaf}_F0001"
                by[fin] = voice(
                    by_old[fin], fin_scene(t1, t2, t3), "ending",
                    extra={"sons": FIN_SONS[t2], "emphasis": "poisson"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra_ids = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{SID} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    fins = [by[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(set(fins)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fins))}/27")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for bad in CALQUES + TICS:
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    n_enc = len(re.findall(r"\bencore\b", blob))
    n_dej = len(re.findall(r"\bdéjà\b", blob))
    if n_enc > 2 or n_dej > 2:
        raise SystemExit(f"{SID} tics encore={n_enc} déjà={n_dej}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "sarah" not in blob or "nino" not in blob:
        raise SystemExit(f"{SID}: troupe Sarah/Nino absente")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
        if not c.get("text_xai_tags") or not c.get("notes"):
            raise SystemExit(f"{SID} {c['chunk_id']} TTS incomplet")
        if not c.get("text_ssml", "").startswith("<speak>"):
            raise SystemExit(f"{SID} {c['chunk_id']} SSML manquant")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Vécu\n"
        "Vent sur la mare, maison au savon chaud, tapis presque sec. "
        "Sarah veut une pêche de papier pour Nino, tout de suite. "
        "Elle crie : le poisson tombe, Nino ne tourne pas. Elle reprend tout bas. "
        "T1 = bâton (rive du canapé) / seau bleu (port de la table) / poisson jaune "
        "(mare du tapis) : la première invite rate, les trois affaires viennent. "
        "T2 = boîte à musique (chanson à finir) / camion jaune (garage) / "
        "chaussons (un pied nu). "
        "T3 = attendre, glisser une autre idée, ou accepter un non. "
        "La leçon se vit : elle propose, elle accepte oui, non, ou plus tard. "
        "Fins : savon, clé, roue, chausson, seau, tapis — 27 images. "
        "Autre récit que DIF-021 (pas de fort), DIF-031 (pas de potager) "
        "et DIF-041 (pas de wagon).\n\n"
        "## Vu et corrigé\n"
        "- Titre noyau conservé. N1 ≤ 10. Troupe D16 : Sarah, Nino, papa, maman.\n"
        "- Première idée échoue (cri trop fort). Un choix change l'action.\n"
        "- Tics « tout doux / tout calme / encore / déjà » chassés.\n"
        "- 27 fins textuellement distinctes. Un merci vécu (poisson ramassé).\n"
        "- TTS par chunk (profils opening/choice/clue/confirm/action/obstacle/resolution/ending).\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés. Pas apply.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(f"OK {SID} {nwords} mots  fins={len(set(fins))}")


if __name__ == "__main__":
    build()
