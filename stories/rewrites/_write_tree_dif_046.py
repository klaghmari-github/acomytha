#!/usr/bin/env python3
"""TREE-DIF-046 — Le moulinet rouge de Victorino, au marché (F-NAR-019, N1, TTS)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "TREE-DIF-046"
LIM = LIMITS["N1"]
TITLE = "Le moulinet rouge de Victorino, au marché"
FIL = (
    "Au marché du village, Victorino veut le moulinet rouge "
    "qui tourne dans le vent, pour rentrer. "
    "Papa sait l'étal ; Victorino dit « le fruit » trop vite. "
    "Le mot tombe. T1 = panier / ficelle / bourse ; les trois partent. "
    "T2 = étal de papier (trop mêlé) / fontaine (l'eau couvre) / "
    "auvent bleu (trop haut). "
    "T3 change l'action : clou, souffle, papier jaune ; "
    "pas, creux des mains, banc ; petit, tabouret, bras. "
    "Victorino laisse la phrase arriver. Le rouge tourne jusqu'à la maison."
)
CHARS = "Victorino, papa, maman"
SETTING = "marché du village : étal de papier, fontaine, auvent bleu"

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=500, sentence=260, energy="warm", contour="storytelling",
        noise=0.36, emphasis="moulinet rouge",
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=le_rouge_tourne_et_le_mot_de_papa_manque; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=900, sentence=330, energy="focused", contour="rising",
        noise=0.33, emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_suite; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2,
        pause=700, sentence=320, energy="focused", contour="rising",
        noise=0.32, emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=450, sentence=280, energy="bright", contour="falling",
        noise=0.34, emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=le_mot_va_venir_plus_loin; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=420, sentence=250, energy="lively", contour="dynamic",
        noise=0.37, emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=il_coupe_la_phrase_de_papa; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0,
        pause=520, sentence=300, energy="tense", contour="dynamic",
        noise=0.34, emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement; intensite=2; destinataire=enfant; sous_texte=le_mot_se_perd; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=560, sentence=270, energy="bright", contour="falling",
        noise=0.35, emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=la_phrase_peut_finir; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3,
        pause=900, sentence=340, energy="calm", contour="falling",
        noise=0.31, emphasis="moulinet rouge",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_rouge_tourne_jusqu_à_la_maison; tempo=posé; sourire=léger; respiration=ample",
    ),
}

TICS = (
    "tout doux",
    "tout calme",
    "on va apprendre",
    "voici le geste",
    "l'histoire est finie",
    "il faut attendre",
    "laisser le temps",
    "bon travail",
    "bravo tu as",
    "la première",
    "la deuxième",
    "la troisième",
)


def L(*rows: str) -> list[str]:
    out: list[str] = []
    prev = ""
    run = 1
    for raw in rows:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > LIM:
            raise SystemExit(f"{n}>{LIM}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
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


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emph = m.get("emphasis")
    if emph:
        e = esc(emph)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


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
    extra = extra or {}
    if extra.get("emphasis") is not None:
        m["emphasis"] = extra["emphasis"]
    if extra.get("note"):
        m["note"] = extra["note"]
    pause_before = extra.get("pause_before", 0)
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


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


OBJ = {
    1: {
        "lab": "le panier",
        "ans": "panier",
        "acc": "panier | le panier | l'osier | panier d'osier",
        "retry": "Victorino tient le panier. Il tient quoi ?",
        "emph": "panier",
        "sons": "osier,panier",
        "voy": "Le panier penche vers l'allée.",
    },
    2: {
        "lab": "la ficelle",
        "ans": "ficelle",
        "acc": "ficelle | la ficelle | le fil | la corde",
        "retry": "Victorino tient la ficelle. Il tient quoi ?",
        "emph": "ficelle",
        "sons": "ficelle,noeud",
        "voy": "La ficelle tape un peu sa hanche.",
    },
    3: {
        "lab": "la bourse",
        "ans": "bourse",
        "acc": "bourse | la bourse | les pièces | la monnaie",
        "retry": "Victorino tient la bourse. Il tient quoi ?",
        "emph": "bourse",
        "sons": "pieces,bourse",
        "voy": "La bourse pèse contre sa poche.",
    },
}

T3_LABS = {
    1: ("le clou bas", "le souffle", "le papier jaune"),
    2: ("le pas en arrière", "le creux des mains", "le banc"),
    3: ("le petit en bas", "le tabouret", "les bras de papa"),
}


def t1_passage(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "narrateur|Victorino prend le panier d'osier.",
            "enfant-m|Il gratte un peu.",
            "papa|L'osier a gardé une paille.",
            "narrateur|Elle pique sa paume, puis s'arrête.",
            "maman|La ficelle, ensuite, autour du bord.",
            "narrateur|Papa glisse la bourse dans la poche.",
            "enfant-m|Où est le rouge ?",
            "narrateur|Papa ouvre la bouche, puis s'arrête.",
            "enfant-m|À quel étal ?",
            "maman|Le mot n'est pas là.",
            "papa|On marche, il va venir.",
            "narrateur|Victorino serre l'osier, déçu.",
        )
    if t1 == 2:
        return L(
            "narrateur|Victorino enroule la ficelle beige.",
            "enfant-m|Elle sent le lin, un peu.",
            "maman|Un nœud dort au bout.",
            "narrateur|Le fil serre son poignet, léger.",
            "papa|Le panier, ensuite, contre lui.",
            "narrateur|Maman glisse la bourse dans la poche.",
            "enfant-m|Alors dis-moi où.",
            "narrateur|Papa inspire, les lèvres rondes.",
            "narrateur|Rien ne sort.",
            "maman|Il cherche la suite.",
            "enfant-m|J'écoute.",
            "narrateur|Le fil tape sa hanche, net.",
        )
    return L(
        "narrateur|Victorino prend la bourse ronde.",
        "enfant-m|Pour payer, après.",
        "papa|Elle cliquette un peu.",
        "narrateur|Deux pièces roulent, puis se taisent.",
        "maman|Le panier, ensuite, et la ficelle.",
        "narrateur|Papa les pose contre lui.",
        "enfant-m|Maintenant, tu dis où.",
        "narrateur|Papa ouvre la bouche, puis la referme.",
        "papa|Le mot va arriver.",
        "enfant-m|D'accord.",
        "maman|On avance, sans courir.",
        "narrateur|La bourse pèse, froide.",
    )


def t1_q(t1: int) -> list[str]:
    o = OBJ[t1]
    return L(
        f"narrateur|Victorino a pris {o['lab']}, tout près.",
        "maman|Victorino a pris quoi, d'abord ?",
    )


def t1_confirm(t1: int) -> list[str]:
    if t1 == 1:
        return L(
            "enfant-m|Le panier.",
            "papa|Oui.",
            "narrateur|La ficelle et la bourse voyagent avec.",
            "maman|Le rouge va se dire, plus loin.",
            "papa|Merci, tu tiens le panier.",
            "enfant-m|Je suis prêt.",
            "papa|On marche, alors ?",
            "enfant-m|Oui, papa.",
        )
    if t1 == 2:
        return L(
            "enfant-m|La ficelle.",
            "maman|Oui.",
            "narrateur|Le panier penche sous le bras.",
            "narrateur|La bourse dort dans la poche.",
            "papa|Le lin a un peu serré.",
            "enfant-m|J'écoute la suite.",
            "maman|On reste ensemble.",
            "papa|Le fil va servir, plus loin.",
        )
    return L(
        "enfant-m|La bourse.",
        "papa|Oui.",
        "narrateur|Le panier et la ficelle pèsent contre lui.",
        "maman|Les pièces vont parler, en marchant.",
        "enfant-m|J'attends le mot.",
        "papa|Il va venir, tout seul.",
        "maman|On avance, alors ?",
        "enfant-m|Oui, maman.",
    )


def t2_question(t1: int) -> list[str]:
    return L(
        f"narrateur|{OBJ[t1]['voy']}",
        "narrateur|Le marché a trois coins, devant.",
        "papa|L'étal, la fontaine, ou l'auvent ?",
    )


def t2_scene(t1: int, t2: int) -> list[str]:
    if t2 == 1:
        if t1 == 1:
            return L(
                "narrateur|Le panier bute une caisse de papier.",
                "narrateur|Des moulinets pendent, tous mêlés.",
                "enfant-m|C'est ici ?",
                "papa|C'est le rouge, près du.",
                "narrateur|Le mot s'arrête au milieu.",
                "enfant-m|Près du fruit ?",
                "narrateur|Victorino mord sa lèvre, un peu.",
                "maman|Ils se ressemblent tous, là-haut.",
                "papa|On fait comment, Victorino ?",
                "narrateur|L'osier racle le bois, sec.",
            )
        if t1 == 2:
            return L(
                "narrateur|La ficelle s'accroche à un clou.",
                "narrateur|Des moulinets pendent, tous mêlés.",
                "enfant-m|C'est ici ?",
                "papa|C'est le rouge, près du.",
                "narrateur|Le mot s'arrête au milieu.",
                "enfant-m|Près du clou ?",
                "narrateur|Victorino lâche le fil, puis le reprend.",
                "maman|Ils se ressemblent tous, là-haut.",
                "papa|On fait comment, Victorino ?",
                "narrateur|Le lin frotte le papier, rêche.",
            )
        return L(
            "narrateur|La bourse tape le bois, un toc.",
            "narrateur|Des moulinets pendent, tous mêlés.",
            "enfant-m|C'est ici ?",
            "papa|C'est le rouge, près du.",
            "narrateur|Le mot s'arrête au milieu.",
            "enfant-m|Près du haut ?",
            "narrateur|Victorino serre les pièces, trop fort.",
            "maman|Ils se ressemblent tous, là-haut.",
            "papa|On fait comment, Victorino ?",
            "narrateur|Une pièce glisse, puis se tait.",
        )
    if t2 == 2:
        if t1 == 1:
            return L(
                "narrateur|Le panier se mouille, au bord.",
                "enfant-m|Il est là, le rouge ?",
                "maman|Il est près de l'.",
                "narrateur|L'eau couvre le mot, trop fort.",
                "narrateur|Des gouttes tapent le bord.",
                "enfant-m|Près de l'eau ?",
                "narrateur|Victorino recule, le panier lourd.",
                "papa|On n'entend plus la fin.",
                "maman|Tu trouves comment ?",
                "narrateur|L'osier sent l'eau, froide.",
            )
        if t1 == 2:
            return L(
                "narrateur|La ficelle boit une goutte, nette.",
                "enfant-m|Il est là, le rouge ?",
                "maman|Il est près de l'.",
                "narrateur|L'eau couvre le mot, trop fort.",
                "narrateur|Des gouttes tapent le bord.",
                "enfant-m|Près de l'eau ?",
                "narrateur|Victorino essuie le fil, trop vite.",
                "papa|On n'entend plus la fin.",
                "maman|Tu trouves comment ?",
                "narrateur|Le lin pèse, mouillé.",
            )
        return L(
            "narrateur|La bourse cliquette sous l'eau qui vole.",
            "enfant-m|Il est là, le rouge ?",
            "maman|Il est près de l'.",
            "narrateur|L'eau couvre le mot, trop fort.",
            "narrateur|Des gouttes tapent le bord.",
            "enfant-m|Près de l'eau ?",
            "narrateur|Victorino cache la bourse, trop tard.",
            "papa|On n'entend plus la fin.",
            "maman|Tu trouves comment ?",
            "narrateur|Une pièce brille, mouillée.",
        )
    if t1 == 1:
        return L(
            "narrateur|Le panier reste trop bas, sous le bleu.",
            "enfant-m|Tout en haut ?",
            "papa|Tout en haut, près du.",
            "narrateur|Papa s'arrête, les lèvres rondes.",
            "enfant-m|Près du bord ?",
            "narrateur|Victorino lève le panier, trop court.",
            "maman|Le haut est trop loin, pour lui.",
            "papa|Un tabouret dort près du mur.",
            "papa|Tu fais quoi, alors ?",
            "narrateur|L'osier penche, vide.",
        )
    if t1 == 2:
        return L(
            "narrateur|La ficelle pend, trop courte, sous le bleu.",
            "enfant-m|Tout en haut ?",
            "papa|Tout en haut, près du.",
            "narrateur|Papa s'arrête, les lèvres rondes.",
            "enfant-m|Près du bord ?",
            "narrateur|Victorino tend le fil, trop court.",
            "maman|Le haut est trop loin, pour lui.",
            "papa|Un tabouret dort près du mur.",
            "papa|Tu fais quoi, alors ?",
            "narrateur|Le lin claque, vide.",
        )
    return L(
        "narrateur|La bourse n'atteint pas le bord, trop haute.",
        "enfant-m|Tout en haut ?",
        "papa|Tout en haut, près du.",
        "narrateur|Papa s'arrête, les lèvres rondes.",
        "enfant-m|Près du bord ?",
        "narrateur|Victorino lève la bourse, trop courte.",
        "maman|Le haut est trop loin, pour lui.",
        "papa|Un tabouret dort près du mur.",
        "papa|Tu fais quoi, alors ?",
        "narrateur|Les pièces se taisent, inutiles.",
    )


def t3_question(t2: int) -> list[str]:
    if t2 == 1:
        return L(
            "narrateur|Sur l'étal, la suite manque.",
            "papa|Le clou, le souffle, ou le papier ?",
        )
    if t2 == 2:
        return L(
            "narrateur|Près de l'eau, le mot n'est pas fini.",
            "maman|Le pas, les mains, ou le banc ?",
        )
    return L(
        "narrateur|Sous l'auvent, le haut attend.",
        "papa|Le petit, le tabouret, ou mes bras ?",
    )


def t3_scene(t1: int, t2: int, t3: int) -> list[str]:
    table = {
        (1, 1, 1): L(
            "enfant-m|On reste.",
            "narrateur|Ils s'arrêtent sous les papiers.",
            "papa|Le clou.",
            "enfant-m|Le clou bas.",
            "narrateur|Victorino attend, sans crier.",
            "papa|Près du clou bas.",
            "narrateur|Un moulinet rouge penche, bas.",
            "narrateur|Le panier reste contre la jambe.",
            "maman|La phrase est arrivée, toute seule.",
            "papa|Merci, Victorino.",
        ),
        (1, 1, 2): L(
            "enfant-m|Je souffle.",
            "narrateur|Un moulinet part, puis un autre.",
            "papa|Le.",
            "narrateur|Victorino ne dit rien.",
            "papa|Le rouge qui tourne.",
            "enfant-m|Je le vois, maintenant.",
            "narrateur|Le panier reste contre la jambe.",
            "maman|Le vent a aidé le mot.",
            "papa|Merci, tu as soufflé sans crier.",
        ),
        (1, 1, 3): L(
            "enfant-m|On se baisse.",
            "narrateur|Ils regardent le papier jaune, près.",
            "papa|Pas le haut.",
            "narrateur|Victorino garde sa bouche fermée.",
            "papa|Contre le jaune.",
            "enfant-m|Celui-là, tout contre la feuille.",
            "narrateur|Le panier reste contre la jambe.",
            "maman|Le rouge est là, net.",
            "papa|On l'a vu, ensemble.",
        ),
        (1, 2, 1): L(
            "enfant-m|On recule.",
            "narrateur|Les deux s'éloignent de l'eau.",
            "papa|Près de l'.",
            "narrateur|Victorino attend, les lèvres fermées.",
            "papa|Près de l'eau, le rouge.",
            "enfant-m|Je l'entends, maintenant.",
            "narrateur|Le panier sèche un peu, au bord.",
            "maman|Le mot est venu, tout seul.",
            "papa|Merci d'avoir reculé.",
        ),
        (1, 2, 2): L(
            "enfant-m|Mes mains, ici.",
            "papa|En creux, tout près des oreilles.",
            "narrateur|L'eau devient un peu plus loin.",
            "maman|Près de.",
            "narrateur|Victorino attend, les lèvres fermées.",
            "maman|Près de la pierre.",
            "narrateur|Le panier pèse entre ses genoux.",
            "papa|On a écouté ensemble.",
            "maman|La suite a eu sa place.",
        ),
        (1, 2, 3): L(
            "enfant-m|Le banc, là.",
            "papa|On s'assoit, loin des gouttes.",
            "narrateur|La pierre est froide, sous eux.",
            "maman|Le rouge.",
            "narrateur|Victorino tourne la tête, sans parler.",
            "enfant-m|Je le vois, contre la pierre.",
            "narrateur|Le panier pose son ombre, ronde.",
            "papa|Le banc a tenu le mot.",
            "maman|On a regardé ensemble.",
        ),
        (1, 3, 1): L(
            "enfant-m|Je dis rien.",
            "narrateur|Victorino baisse les yeux, sous le bleu.",
            "papa|Pas le grand.",
            "enfant-m|Le petit.",
            "narrateur|Papa tend le bras, tout bas.",
            "papa|Le petit, près du mur.",
            "narrateur|Un moulinet rouge penche, bas.",
            "narrateur|Le panier s'appuie au mur.",
            "maman|Le mot a fini sa route.",
            "papa|Merci d'avoir regardé en bas.",
        ),
        (1, 3, 2): L(
            "enfant-m|Le tabouret, dessous.",
            "papa|Je le tiens, à ta hauteur.",
            "narrateur|Victorino monte, sans crier.",
            "papa|Près du.",
            "narrateur|Victorino attend, un pied en l'air.",
            "papa|Près du bord.",
            "narrateur|Le panier reste au sol, sage.",
            "maman|Tu as laissé le mot monter.",
            "papa|Le bois a tenu tes pieds.",
        ),
        (1, 3, 3): L(
            "enfant-m|Tes bras, papa.",
            "papa|Viens, tout contre moi.",
            "narrateur|Victorino s'élève, le nez au bleu.",
            "papa|Le rouge, tout près du bord.",
            "enfant-m|Je le vois !",
            "narrateur|Un moulinet brille entre deux toiles.",
            "narrateur|Le panier attend, au sol.",
            "maman|Tes bras ont fini la phrase.",
            "papa|Chacun a fait sa part.",
        ),
        (2, 1, 1): L(
            "enfant-m|On reste.",
            "narrateur|Le fil se décroche du clou, lent.",
            "papa|Le clou.",
            "enfant-m|Le clou bas.",
            "narrateur|Victorino tient le lin, sans tirer.",
            "papa|Près du clou bas.",
            "narrateur|Un moulinet rouge penche, bas.",
            "narrateur|La ficelle attend un dernier nœud.",
            "maman|La phrase est arrivée, toute seule.",
            "papa|Merci, Victorino.",
        ),
        (2, 1, 2): L(
            "enfant-m|Je souffle.",
            "narrateur|Le fil vibre, puis les papiers partent.",
            "papa|Le.",
            "narrateur|Victorino ne dit rien.",
            "papa|Le rouge qui tourne.",
            "enfant-m|Je le vois, maintenant.",
            "narrateur|La ficelle attend un dernier nœud.",
            "maman|Le vent a aidé le mot.",
            "papa|Merci, tu as soufflé sans crier.",
        ),
        (2, 1, 3): L(
            "enfant-m|On se baisse.",
            "narrateur|Le fil glisse vers le papier jaune.",
            "papa|Pas le haut.",
            "narrateur|Victorino garde sa bouche fermée.",
            "papa|Contre le jaune.",
            "enfant-m|Celui-là, tout contre la feuille.",
            "narrateur|La ficelle attend un dernier nœud.",
            "maman|Le rouge est là, net.",
            "papa|On l'a vu, ensemble.",
        ),
        (2, 2, 1): L(
            "enfant-m|On recule.",
            "narrateur|La ficelle quitte les gouttes, nette.",
            "papa|Près de l'.",
            "narrateur|Victorino attend, les lèvres fermées.",
            "papa|Près de l'eau, le rouge.",
            "enfant-m|Je l'entends, maintenant.",
            "narrateur|La ficelle sèche contre sa hanche.",
            "maman|Le mot est venu, tout seul.",
            "papa|Merci d'avoir reculé.",
        ),
        (2, 2, 2): L(
            "enfant-m|Mes mains, ici.",
            "papa|En creux, tout près des oreilles.",
            "narrateur|Le fil reste calme, entre deux doigts.",
            "maman|Près de.",
            "narrateur|Victorino attend, les lèvres fermées.",
            "maman|Près de la pierre.",
            "narrateur|La ficelle pend, oubliée un instant.",
            "papa|On a écouté ensemble.",
            "maman|La suite a eu sa place.",
        ),
        (2, 2, 3): L(
            "enfant-m|Le banc, là.",
            "papa|On s'assoit, loin des gouttes.",
            "narrateur|La ficelle repose sur la pierre froide.",
            "maman|Le rouge.",
            "narrateur|Victorino tourne la tête, sans parler.",
            "enfant-m|Je le vois, contre la pierre.",
            "narrateur|Le fil fait un petit tas, beige.",
            "papa|Le banc a tenu le mot.",
            "maman|On a regardé ensemble.",
        ),
        (2, 3, 1): L(
            "enfant-m|Je dis rien.",
            "narrateur|La ficelle pend, trop courte, oubliée.",
            "papa|Pas le grand.",
            "enfant-m|Le petit.",
            "narrateur|Papa tend le bras, tout bas.",
            "papa|Le petit, près du mur.",
            "narrateur|Un moulinet rouge penche, bas.",
            "narrateur|La ficelle attend un dernier nœud.",
            "maman|Le mot a fini sa route.",
            "papa|Merci d'avoir regardé en bas.",
        ),
        (2, 3, 2): L(
            "enfant-m|Le tabouret, dessous.",
            "papa|Je le tiens, à ta hauteur.",
            "narrateur|Victorino monte, le fil à la main.",
            "papa|Près du.",
            "narrateur|Victorino attend, un pied en l'air.",
            "papa|Près du bord.",
            "narrateur|La ficelle pend, assez longue, maintenant.",
            "maman|Tu as laissé le mot monter.",
            "papa|Le bois a tenu tes pieds.",
        ),
        (2, 3, 3): L(
            "enfant-m|Tes bras, papa.",
            "papa|Viens, tout contre moi.",
            "narrateur|Victorino s'élève, le fil au vent.",
            "papa|Le rouge, tout près du bord.",
            "enfant-m|Je le vois !",
            "narrateur|Un moulinet brille entre deux toiles.",
            "narrateur|La ficelle frôle le bleu, légère.",
            "maman|Tes bras ont fini la phrase.",
            "papa|Chacun a fait sa part.",
        ),
        (3, 1, 1): L(
            "enfant-m|On reste.",
            "narrateur|La bourse se tait contre sa paume.",
            "papa|Le clou.",
            "enfant-m|Le clou bas.",
            "narrateur|Victorino attend, sans crier.",
            "papa|Près du clou bas.",
            "narrateur|Un moulinet rouge penche, bas.",
            "narrateur|Les pièces restent sages, dans la poche.",
            "maman|La phrase est arrivée, toute seule.",
            "papa|Merci, Victorino.",
        ),
        (3, 1, 2): L(
            "enfant-m|Je souffle.",
            "narrateur|Les pièces se taisent, le papier part.",
            "papa|Le.",
            "narrateur|Victorino ne dit rien.",
            "papa|Le rouge qui tourne.",
            "enfant-m|Je le vois, maintenant.",
            "narrateur|La bourse dort contre sa paume.",
            "maman|Le vent a aidé le mot.",
            "papa|Merci, tu as soufflé sans crier.",
        ),
        (3, 1, 3): L(
            "enfant-m|On se baisse.",
            "narrateur|La bourse cliquette, puis se tait.",
            "papa|Pas le haut.",
            "narrateur|Victorino garde sa bouche fermée.",
            "papa|Contre le jaune.",
            "enfant-m|Celui-là, tout contre la feuille.",
            "narrateur|La bourse dort contre sa paume.",
            "maman|Le rouge est là, net.",
            "papa|On l'a vu, ensemble.",
        ),
        (3, 2, 1): L(
            "enfant-m|On recule.",
            "narrateur|La bourse quitte les gouttes, ronde.",
            "papa|Près de l'.",
            "narrateur|Victorino attend, les lèvres fermées.",
            "papa|Près de l'eau, le rouge.",
            "enfant-m|Je l'entends, maintenant.",
            "narrateur|Une pièce sèche, dans la poche.",
            "maman|Le mot est venu, tout seul.",
            "papa|Merci d'avoir reculé.",
        ),
        (3, 2, 2): L(
            "enfant-m|Mes mains, ici.",
            "papa|En creux, tout près des oreilles.",
            "narrateur|La bourse pèse contre son ventre.",
            "maman|Près de.",
            "narrateur|Victorino attend, les lèvres fermées.",
            "maman|Près de la pierre.",
            "narrateur|Les pièces se taisent, oubliées.",
            "papa|On a écouté ensemble.",
            "maman|La suite a eu sa place.",
        ),
        (3, 2, 3): L(
            "enfant-m|Le banc, là.",
            "papa|On s'assoit, loin des gouttes.",
            "narrateur|La bourse dort sur la pierre froide.",
            "maman|Le rouge.",
            "narrateur|Victorino tourne la tête, sans parler.",
            "enfant-m|Je le vois, contre la pierre.",
            "narrateur|Deux pièces restent chaudes, sous la main.",
            "papa|Le banc a tenu le mot.",
            "maman|On a regardé ensemble.",
        ),
        (3, 3, 1): L(
            "enfant-m|Je dis rien.",
            "narrateur|La bourse rentre dans la poche, oubliée.",
            "papa|Pas le grand.",
            "enfant-m|Le petit.",
            "narrateur|Papa tend le bras, tout bas.",
            "papa|Le petit, près du mur.",
            "narrateur|Un moulinet rouge penche, bas.",
            "narrateur|Les pièces se taisent, sous l'auvent.",
            "maman|Le mot a fini sa route.",
            "papa|Merci d'avoir regardé en bas.",
        ),
        (3, 3, 2): L(
            "enfant-m|Le tabouret, dessous.",
            "papa|Je le tiens, à ta hauteur.",
            "narrateur|Victorino monte, la bourse à la poche.",
            "papa|Près du.",
            "narrateur|Victorino attend, un pied en l'air.",
            "papa|Près du bord.",
            "narrateur|La bourse tape sa hanche, une fois.",
            "maman|Tu as laissé le mot monter.",
            "papa|Le bois a tenu tes pieds.",
        ),
        (3, 3, 3): L(
            "enfant-m|Tes bras, papa.",
            "papa|Viens, tout contre moi.",
            "narrateur|Victorino s'élève, la bourse au ventre.",
            "papa|Le rouge, tout près du bord.",
            "enfant-m|Je le vois !",
            "narrateur|Un moulinet brille entre deux toiles.",
            "narrateur|Les pièces restent sages, tout contre lui.",
            "maman|Tes bras ont fini la phrase.",
            "papa|Chacun a fait sa part.",
        ),
    }
    return table[(t1, t2, t3)]


def fin_scene(t1: int, t2: int, t3: int) -> list[str]:
    table = {
        (1, 1, 1): L(
            "narrateur|Le bâton rentre dans le poing, un clic.",
            "enfant-m|Il tourne !",
            "papa|Sur le chemin, tout droit.",
            "maman|Bravo.",
            "narrateur|Le panier tient le bâton, tout droit.",
            "narrateur|Une paille sèche sur l'osier du panier.",
            "narrateur|L'étal redevient calme, autour des papiers.",
            "narrateur|La soupe sent, l'osier se tait.",
        ),
        (1, 1, 2): L(
            "narrateur|Le moulinet part, enfin, tout rouge.",
            "enfant-m|J'ai soufflé, d'abord.",
            "papa|Puis le mot est venu.",
            "maman|Venez, le pain est chaud.",
            "narrateur|Le panier penche, le rouge tourne dessus.",
            "narrateur|Victorino pose le bâton contre l'épaule.",
            "narrateur|Un papier reste collé à sa chaussure.",
            "narrateur|Le pain chaud attend, un papier au pied.",
        ),
        (1, 1, 3): L(
            "narrateur|Contre le jaune, le rouge tient, net.",
            "enfant-m|On s'est baissés, papa.",
            "papa|Le haut gardera son ombre.",
            "maman|Tiens bien le bâton.",
            "narrateur|Le panier tapote le papier, léger.",
            "narrateur|Une poussière s'envole, puis retombe.",
            "narrateur|Une abeille passe au-dessus du panier.",
            "narrateur|L'abeille laisse l'étal, derrière eux.",
        ),
        (1, 2, 1): L(
            "narrateur|Loin de l'eau, le rouge était là.",
            "enfant-m|Tu as fini, papa.",
            "papa|Oui, le mot était long.",
            "maman|Tu as reculé, sans crier.",
            "narrateur|Le panier tient le bâton, mouillé un peu.",
            "narrateur|Une goutte sèche sur le bâton rouge.",
            "narrateur|Victorino fait tourner le rouge, tout près.",
            "narrateur|L'osier sèche, la fontaine se tait.",
        ),
        (1, 2, 2): L(
            "narrateur|Dans le creux, le mot a parlé.",
            "enfant-m|J'ai écouté, tout contre.",
            "papa|Tes mains étaient à la bonne place.",
            "maman|Le pain t'attend.",
            "narrateur|Le panier sent le thym, près du pain.",
            "narrateur|Victorino essuie une main sur son pantalon.",
            "narrateur|Une goutte reste sur le papier.",
            "narrateur|Le thym du panier rentre avec le pain.",
        ),
        (1, 2, 3): L(
            "narrateur|Sur le banc, le rouge penche.",
            "enfant-m|Je l'ai vu, contre la pierre.",
            "papa|La pierre a gardé l'ombre.",
            "maman|Rentre le bâton, après le tour.",
            "narrateur|Le panier pose son ombre sur le banc.",
            "narrateur|Victorino souffle un peu sur les pales.",
            "narrateur|Une poussière s'envole, puis retombe.",
            "narrateur|L'ombre du panier quitte le banc.",
        ),
        (1, 3, 1): L(
            "narrateur|Tout en bas, le rouge brille.",
            "enfant-m|Tu as dit petit, à la fin.",
            "papa|Merci d'avoir regardé jusque-là.",
            "maman|Un peu de soupe, après le vent.",
            "narrateur|Le panier s'appuie au mur, sous l'auvent.",
            "narrateur|Victorino pose le bâton contre le mur.",
            "narrateur|L'auvent bleu reprend sa place, sage.",
            "narrateur|L'osier s'appuie, la soupe appelle.",
        ),
        (1, 3, 2): L(
            "narrateur|Sur le tabouret, Victorino a vu le bord.",
            "enfant-m|Le mot est monté avec moi.",
            "papa|Je remporte le tabouret, tout à l'heure.",
            "maman|Essuie tes chaussures, Victorino.",
            "narrateur|Le panier tape une marche, puis se tait.",
            "narrateur|Le moulinet tourne jusqu'au seuil, net.",
            "narrateur|Une marche se tait, puis l'autre.",
            "narrateur|Le panier tape le seuil, puis se tait.",
        ),
        (1, 3, 3): L(
            "narrateur|Dans les bras de papa, le rouge était là.",
            "enfant-m|On l'a pris, tout haut.",
            "papa|Tes yeux allaient assez loin.",
            "maman|Le haut gardera son ombre.",
            "narrateur|Le panier pose le bâton près des pavés.",
            "narrateur|Les pales touchent l'air, enfin.",
            "narrateur|Une toile claque, puis le vent se tait.",
            "narrateur|Le moulinet rouge tourne sur les pavés.",
        ),
        (2, 1, 1): L(
            "narrateur|Le bâton rentre, la ficelle le serre.",
            "enfant-m|Il tourne !",
            "papa|Sur le chemin, tout droit.",
            "maman|Bravo.",
            "narrateur|La ficelle serre le bois, net.",
            "narrateur|Un nœud dort au bout du fil.",
            "narrateur|L'étal redevient calme, autour des papiers.",
            "narrateur|La soupe sent, le nœud dort.",
        ),
        (2, 1, 2): L(
            "narrateur|Le moulinet part, le fil vibre.",
            "enfant-m|J'ai soufflé, d'abord.",
            "papa|Puis le mot est venu.",
            "maman|Venez, le pain est chaud.",
            "narrateur|La ficelle a pris un peu de poussière.",
            "narrateur|Victorino pose le bâton contre l'épaule.",
            "narrateur|Un papier reste collé à sa chaussure.",
            "narrateur|Le fil garde la poussière, jusqu'au pain.",
        ),
        (2, 1, 3): L(
            "narrateur|Contre le jaune, le fil tient le rouge.",
            "enfant-m|On s'est baissés, papa.",
            "papa|Le haut gardera son ombre.",
            "maman|Tiens bien le bâton.",
            "narrateur|La ficelle tapote le papier, légère.",
            "narrateur|Une poussière s'envole, puis retombe.",
            "narrateur|Une abeille passe au-dessus du fil.",
            "narrateur|Une abeille frôle le fil, puis s'en va.",
        ),
        (2, 2, 1): L(
            "narrateur|Loin de l'eau, le fil a trouvé le rouge.",
            "enfant-m|Tu as fini, papa.",
            "papa|Oui, le mot était long.",
            "maman|Tu as reculé, sans crier.",
            "narrateur|Une goutte glisse le long du fil.",
            "narrateur|Victorino fait tourner le rouge, tout près.",
            "narrateur|La ficelle sèche, tour après tour.",
            "narrateur|Le fil sèche, la fontaine se tait.",
        ),
        (2, 2, 2): L(
            "narrateur|Dans le creux, le fil a écouté aussi.",
            "enfant-m|J'ai écouté, tout contre.",
            "papa|Tes mains étaient à la bonne place.",
            "maman|Le pain t'attend.",
            "narrateur|La ficelle sent l'eau, puis sèche.",
            "narrateur|Victorino essuie une main sur son pantalon.",
            "narrateur|Une goutte reste sur le papier.",
            "narrateur|Le lin sent l'eau, jusqu'au pain.",
        ),
        (2, 2, 3): L(
            "narrateur|Sur le banc, le fil repose, beige.",
            "enfant-m|Je l'ai vu, contre la pierre.",
            "papa|La pierre a gardé l'ombre.",
            "maman|Rentre le bâton, après le tour.",
            "narrateur|La ficelle repose sur le banc froid.",
            "narrateur|Victorino souffle un peu sur les pales.",
            "narrateur|Une poussière s'envole, puis retombe.",
            "narrateur|Le fil beige reste sur le banc.",
        ),
        (2, 3, 1): L(
            "narrateur|Tout en bas, le fil touche le rouge.",
            "enfant-m|Tu as dit petit, à la fin.",
            "papa|Merci d'avoir regardé jusque-là.",
            "maman|Un peu de soupe, après le vent.",
            "narrateur|La ficelle pend sous l'auvent bleu.",
            "narrateur|Victorino pose le bâton contre le mur.",
            "narrateur|L'auvent bleu reprend sa place, sage.",
            "narrateur|Le fil pend, la soupe appelle.",
        ),
        (2, 3, 2): L(
            "narrateur|Sur le tabouret, le fil atteint le bord.",
            "enfant-m|Le mot est monté avec moi.",
            "papa|Je remporte le tabouret, tout à l'heure.",
            "maman|Essuie tes chaussures, Victorino.",
            "narrateur|La ficelle tape une marche, puis se tait.",
            "narrateur|Le moulinet tourne jusqu'au seuil, net.",
            "narrateur|Une marche se tait, puis l'autre.",
            "narrateur|Le fil tape le seuil, puis se tait.",
        ),
        (2, 3, 3): L(
            "narrateur|Dans les bras de papa, le fil frôle le bleu.",
            "enfant-m|On l'a pris, tout haut.",
            "papa|Tes yeux allaient assez loin.",
            "maman|Le haut gardera son ombre.",
            "narrateur|La ficelle frôle les pavés, au vent.",
            "narrateur|Les pales touchent l'air, enfin.",
            "narrateur|Une toile claque, puis le vent se tait.",
            "narrateur|Le fil frôle les pavés, jusqu'à la maison.",
        ),
        (3, 1, 1): L(
            "narrateur|Le bâton rentre, la bourse se tait.",
            "enfant-m|Il tourne !",
            "papa|Sur le chemin, tout droit.",
            "maman|Bravo.",
            "narrateur|La bourse cliquette une fois, puis se tait.",
            "narrateur|Deux pièces restent chaudes, dans la poche.",
            "narrateur|L'étal redevient calme, autour des papiers.",
            "narrateur|La soupe sent, les pièces se taisent.",
        ),
        (3, 1, 2): L(
            "narrateur|Le moulinet part, la bourse pèse.",
            "enfant-m|J'ai soufflé, d'abord.",
            "papa|Puis le mot est venu.",
            "maman|Venez, le pain est chaud.",
            "narrateur|La bourse sent le papier, un peu.",
            "narrateur|Victorino pose le bâton contre l'épaule.",
            "narrateur|Un papier reste collé à sa chaussure.",
            "narrateur|La bourse sent le papier, jusqu'au pain.",
        ),
        (3, 1, 3): L(
            "narrateur|Contre le jaune, la bourse a payé le rouge.",
            "enfant-m|On s'est baissés, papa.",
            "papa|Le haut gardera son ombre.",
            "maman|Tiens bien le bâton.",
            "narrateur|La bourse tapote le papier, ronde.",
            "narrateur|Une poussière s'envole, puis retombe.",
            "narrateur|Une abeille passe au-dessus des pièces.",
            "narrateur|Les pièces se taisent, l'abeille s'en va.",
        ),
        (3, 2, 1): L(
            "narrateur|Loin de l'eau, la bourse a trouvé le rouge.",
            "enfant-m|Tu as fini, papa.",
            "papa|Oui, le mot était long.",
            "maman|Tu as reculé, sans crier.",
            "narrateur|Une pièce brille, mouillée, puis sèche.",
            "narrateur|Victorino fait tourner le rouge, tout près.",
            "narrateur|La bourse pèse, ronde, contre sa poche.",
            "narrateur|Une pièce sèche, la fontaine se tait.",
        ),
        (3, 2, 2): L(
            "narrateur|Dans le creux, les pièces se sont tues.",
            "enfant-m|J'ai écouté, tout contre.",
            "papa|Tes mains étaient à la bonne place.",
            "maman|Le pain t'attend.",
            "narrateur|La bourse pèse contre sa poche, ronde.",
            "narrateur|Victorino essuie une main sur son pantalon.",
            "narrateur|Une goutte reste sur le papier.",
            "narrateur|La bourse rentre, le pain attend.",
        ),
        (3, 2, 3): L(
            "narrateur|Sur le banc, la bourse dort, ronde.",
            "enfant-m|Je l'ai vu, contre la pierre.",
            "papa|La pierre a gardé l'ombre.",
            "maman|Rentre le bâton, après le tour.",
            "narrateur|La bourse dort sur le banc de pierre.",
            "narrateur|Victorino souffle un peu sur les pales.",
            "narrateur|Une poussière s'envole, puis retombe.",
            "narrateur|La bourse dort, le banc se tait.",
        ),
        (3, 3, 1): L(
            "narrateur|Tout en bas, la bourse a vu le rouge.",
            "enfant-m|Tu as dit petit, à la fin.",
            "papa|Merci d'avoir regardé jusque-là.",
            "maman|Un peu de soupe, après le vent.",
            "narrateur|La bourse rentre dans la poche, sous l'auvent.",
            "narrateur|Victorino pose le bâton contre le mur.",
            "narrateur|L'auvent bleu reprend sa place, sage.",
            "narrateur|La bourse rentre, la soupe appelle.",
        ),
        (3, 3, 2): L(
            "narrateur|Sur le tabouret, la bourse tape sa hanche.",
            "enfant-m|Le mot est monté avec moi.",
            "papa|Je remporte le tabouret, tout à l'heure.",
            "maman|Essuie tes chaussures, Victorino.",
            "narrateur|La bourse tape sa hanche, à chaque marche.",
            "narrateur|Le moulinet tourne jusqu'au seuil, net.",
            "narrateur|Une marche se tait, puis l'autre.",
            "narrateur|La bourse tape le seuil, à chaque marche.",
        ),
        (3, 3, 3): L(
            "narrateur|Dans les bras de papa, la bourse se tait.",
            "enfant-m|On l'a pris, tout haut.",
            "papa|Tes yeux allaient assez loin.",
            "maman|Le haut gardera son ombre.",
            "narrateur|La bourse se tait, près des pavés.",
            "narrateur|Les pales touchent l'air, enfin.",
            "narrateur|Une toile claque, puis le vent se tait.",
            "narrateur|La bourse se tait, le rouge rentre.",
        ),
    }
    return table[(t1, t2, t3)]


def write_tree() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    scripts: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {}
    profiles: dict[str, str] = {}
    emph: dict[str, str | None] = {}

    scripts["CHK_T0000_P0000"] = L(
        "narrateur|Une toile bleue claque au-dessus des pavés.",
        "narrateur|Le marché du village sent le thym.",
        "narrateur|Un rayon tombe sur une caisse d'oranges.",
        "narrateur|Les oranges brillent, un peu mouillées.",
        "papa|Tu as vu le moulinet rouge, là-haut ?",
        "enfant-m|Il tourne dans le vent.",
        "maman|Le vent le pousse, tout seul.",
        "narrateur|En ce moment, Victorino lève le nez.",
        "enfant-m|Je le veux, pour rentrer.",
        "papa|Il est à l'étal du.",
        "narrateur|Papa cherche, la bouche ouverte.",
        "enfant-m|Du fruit, papa ?",
        "narrateur|Le mot tombe, puis s'en va.",
        "papa|Ce n'est pas le fruit.",
        "maman|La suite va arriver.",
        "papa|Prenez vos affaires, avant le vent.",
    )
    sons["CHK_T0000_P0000"] = "toiles,marche,oranges"
    profiles["CHK_T0000_P0000"] = "opening"
    emph["CHK_T0000_P0000"] = "moulinet rouge"

    scripts["CHK_T0001_P0000"] = L(
        "narrateur|Trois affaires attendent près des caisses.",
        "narrateur|Le panier, la ficelle, et la bourse.",
        "papa|Tu prends quoi, d'abord ?",
    )
    profiles["CHK_T0001_P0000"] = "choice"
    extras["CHK_T0001_P0000"] = t3lab("le panier", "la ficelle", "la bourse")

    t2_sons = {1: "papier,vent", 2: "eau,goutte", 3: "toile,vent"}
    t2_emph = {1: "papier", 2: "fontaine", 3: "auvent"}
    t3_emph = {
        1: {1: "clou", 2: "souffle", 3: "papier jaune"},
        2: {1: "pas", 2: "mains", 3: "banc"},
        3: {1: "petit", 2: "tabouret", 3: "bras"},
    }

    for t1 in (1, 2, 3):
        meta = OBJ[t1]
        base = f"CHK_T0001_P000{t1}"
        scripts[base] = t1_passage(t1)
        sons[base] = meta["sons"]
        profiles[base] = "action"
        emph[base] = meta["emph"]

        qid = f"{base}_Q0001"
        scripts[qid] = t1_q(t1)
        profiles[qid] = "clue"
        extras[qid] = qf(meta["ans"], meta["acc"], meta["retry"])
        emph[qid] = meta["emph"]

        cid = f"{base}_C0001"
        scripts[cid] = t1_confirm(t1)
        profiles[cid] = "confirm"

        t2q = f"{base}_T0002_P0000"
        scripts[t2q] = t2_question(t1)
        profiles[t2q] = "choice"
        extras[t2q] = t3lab("l'étal de papier", "la fontaine", "l'auvent bleu")

        for t2 in (1, 2, 3):
            p2 = f"{base}_T0002_P000{t2}"
            scripts[p2] = t2_scene(t1, t2)
            sons[p2] = t2_sons[t2]
            profiles[p2] = "obstacle"
            emph[p2] = t2_emph[t2]

            t3q = f"{p2}_T0003_P0000"
            scripts[t3q] = t3_question(t2)
            profiles[t3q] = "choice"
            extras[t3q] = t3lab(*T3_LABS[t2])

            for t3i in (1, 2, 3):
                p3 = f"{p2}_T0003_P000{t3i}"
                scripts[p3] = t3_scene(t1, t2, t3i)
                sons[p3] = t2_sons[t2]
                profiles[p3] = "resolution"
                emph[p3] = t3_emph[t2][t3i]

                fin = f"{p3}_F0001"
                scripts[fin] = fin_scene(t1, t2, t3i)
                sons[fin] = "moulinet,vent,pas"
                profiles[fin] = "ending"
                emph[fin] = "moulinet rouge"

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra_ids = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"{SID} missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

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
        nc.update(voice(text, profiles[cid], extra_voice or None))
        if cid in extras:
            nc.update(extras[cid])
        by[cid] = nc

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]

    check(SID, out["age_band"], out["chunks"])

    fins = [c for c in out["chunks"] if c.get("kind") == "passage_fin"]
    texts = [c["text"] for c in fins]
    if len(texts) != 27:
        raise SystemExit(f"fins {len(texts)} != 27")
    if len(set(texts)) != 27:
        raise SystemExit("fins non distinctes")
    lasts = []
    for c in fins:
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{c['chunk_id']} fin mécanique: {last}")
        lasts.append(last)
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images non distinctes: {len(set(lasts))}")

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for tic in TICS + (
        "kenzo",
        "adam",
        "toboggan",
        "balançoire",
        "bac à sable",
        "biscuit",
        "gâteau",
        "cheval",
        "dans le salon",
        "joue au salon",
        "capitaine",
        "plic",
        "volet jaune",
        "noé",
        "sami",
        "léa",
        "tom ",
    ):
        if tic in whole:
            raise SystemExit(f"{SID} slogan/calque: {tic}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "victorino" not in blob:
        raise SystemExit(f"{SID}: Victorino absent")
    for bad in ("déjà", "encore", "tout doux", "tout calme"):
        if bad in blob:
            raise SystemExit(f"{SID} tic corpus: {bad}")
    if not all(c.get("text_xai_tags") for c in out["chunks"]):
        raise SystemExit(f"{SID}: text_xai_tags manquant")
    if not all(c.get("notes") for c in out["chunks"]):
        raise SystemExit(f"{SID}: notes manquant")
    if not all(c.get("style_energy") for c in out["chunks"]):
        raise SystemExit(f"{SID}: style_energy manquant")
    for c in out["chunks"]:
        if c["text_xai_tags"] == c["text"]:
            raise SystemExit(f"{c['chunk_id']}: text_xai_tags = text")
    if len(out["chunks"]) != 86:
        raise SystemExit(f"{SID}: {len(out['chunks'])} chunks != 86")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    write_tree()
    relecture(
        SID,
        TITLE,
        "Marché, thym, oranges mouillées, toile bleue. Victorino veut le moulinet rouge "
        "qui tourne, pour rentrer. Papa commence : « à l'étal du… » ; Victorino dit "
        "« du fruit » trop vite. Le mot tombe. T1 = panier (paille) / ficelle (lin) / "
        "bourse (pièces) : il reprend trop vite, la bouche de papa se referme. "
        "T2 = étal de papier (mêlé) / fontaine (eau qui couvre) / auvent bleu (trop haut). "
        "T3 change l'action : clou bas, souffle, papier jaune ; pas en arrière, creux "
        "des mains, banc ; petit en bas, tabouret, bras de papa. La phrase finit. "
        "Le rouge tourne jusqu'à la maison. 27 fins paient le rouge, l'objet, le lieu.",
        "F-NAR-019. N1 ≤ 10. Adam / bac-toboggan-balançoires / Tom-Léa-Sami jetés. "
        "Tics « encore / déjà / tout doux / tout calme » jetés. Première idée échoue "
        "(étal du fruit). Choix T3 change l'action. TTS par chunk (profiles example2). "
        "Merci de papa (panier, reculer, souffler, regarder). Un bravo vécu (il tourne). "
        "Autre récit que DIF-018, DIF-028, DIF-038. Pas apply. Audio non cuit.",
    )


if __name__ == "__main__":
    main()
