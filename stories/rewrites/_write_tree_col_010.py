#!/usr/bin/env python3
"""TREE-COL-010 — N1 COL.ECO.002. Écoute vécue au marché, TTS, 27 fins."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, make_chunk, words  # noqa: E402

SID = "TREE-COL-010"
N1 = LIMITS["N1"]
TICS = ("tout doux", "tout calme", " on attend", "on lève la main", "puis on parle")
TIC_WORDS = re.compile(r"\b(encore|déjà)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        note="arc=installation; intention=émerveiller; emotion=envie; intensite=1; destinataire=enfant; sous_texte=les oranges attendent; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=on_a_entendu; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_veut_les_oranges; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=ce_n_est_pas_son_tour; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=la_pesée_peut_finir; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_jus_paie_le_marché; tempo=posé; sourire=léger; respiration=ample",
    ),
}

KIND_PROFILE = {
    "passage_debut": "opening",
    "transition_question": "choice",
    "passage_question": "clue",
    "passage_fin": "ending",
}


def L(*rows: str) -> list[str]:
    out = []
    for raw in rows:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        low = ph.lower()
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"tic «{tic}»: {ph}")
        if TIC_WORDS.search(ph):
            raise SystemExit(f"tic mot: {ph}")
        out.append(f"{role}|{ph}")
    return list(out)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp and emp in text:
        e = esc(emp)
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
    tail = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return f"{body}{tail}".strip()


def voice(nc: dict, profile: str, emphasis: str | None, sons: str) -> None:
    m = dict(PROFILES[profile])
    m["emphasis"] = emphasis
    text = nc["text"]
    nc["sons"] = sons or ""
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
    nc["emphasis_words"] = emphasis or ""
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
    nc["notes"] = m["note"]
    nc["night_policy"] = "play"
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"


def t3(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


def qf(ans: str, acc: str, retry: str) -> dict:
    return {"expected_answer": ans, "accepted_examples": acc, "retry_prompt": retry}


STARTS = {
    1: dict(lab="le petit panier", emp="panier", sons="panier,marche"),
    2: dict(lab="le filet", emp="filet", sons="filet,marche"),
    3: dict(lab="les pièces", emp="pièce", sons="pieces,marche"),
}
LOCS = {
    1: dict(lab="la balance", emp="balance", sons="balance,clic"),
    2: dict(lab="la caisse", emp="caisse", sons="bois,oranges"),
    3: dict(lab="le chariot", emp="chariot", sons="roue,marche"),
}
WAYS = {
    1: dict(lab="une orange", emp="orange", sons="clic,orange"),
    2: dict(lab="le tas", emp="tas", sons="oranges"),
    3: dict(lab="le torchon", emp="torchon", sons="tissu"),
}


def main() -> None:
    s: dict[str, list[str]] = {}
    extras: dict[str, dict] = {}
    sons: dict[str, str] = {}
    prof: dict[str, str] = {}
    emph: dict[str, str | None] = {}

    def put(cid: str, lines: list[str], profile: str, son: str, emp: str | None = None) -> None:
        s[cid] = lines
        sons[cid] = son
        prof[cid] = profile
        emph[cid] = emp

    put(
        "CHK_T0000_P0000",
        L(
            "narrateur|Sous la bâche jaune, le stand sent l'orange.",
            "narrateur|Une goutte de jus brille sur le plateau.",
            "narrateur|La balance de fer fait un clic.",
            "narrateur|Les pavés glacent le dessous des chaussures.",
            "narrateur|Un frelon tourne près de la caisse.",
            "narrateur|Le panier de maman frotte le manteau.",
            "narrateur|Il est vide, un peu rêche.",
            "narrateur|Papa cherche une pièce au fond.",
            "maman|Tu as mis ton écharpe, Mila ?",
            "enfant-f|Oui.",
            "enfant-f|Elle gratte un peu.",
            "narrateur|En ce moment, Mila veut les oranges rondes.",
            "enfant-f|Pour le jus, à la maison !",
            "narrateur|La marchande parle à un monsieur.",
            "narrateur|Il choisit des poireaux, un par un.",
            "enfant-f|Des oranges !",
            "narrateur|Ses mots tombent dans les voix.",
            "narrateur|La marchande ne se tourne pas.",
            "narrateur|Des pommes occupent le plateau.",
            "enfant-f|Elle ne m'entend pas.",
            "narrateur|Les joues de Mila deviennent chaudes.",
            "papa|On va trouver une façon.",
            "maman|Tu prends quoi, pour commencer ?",
        ),
        "opening",
        "bache,marche",
        "oranges",
    )
    put(
        "CHK_T0001_P0000",
        L(
            "narrateur|Le petit panier, le filet, ou les pièces.",
            "maman|Que prends-tu pour les oranges ?",
        ),
        "choice",
        "",
        None,
    )
    extras["CHK_T0001_P0000"] = t3("le petit panier", "le filet", "les pièces")

    put(
        "CHK_T0001_P0001",
        L(
            "narrateur|Mila saisit le petit panier d'osier.",
            "narrateur|Il sent le pain d'hier.",
            "enfant-f|Des oranges, dans ça !",
            "narrateur|Papa demande le prix du thym.",
            "narrateur|Sa voix couvre celle de Mila.",
            "narrateur|Mila ouvre la bouche, puis la ferme.",
            "narrateur|Elle pose le panier contre sa manche.",
            "enfant-f|Quand tu as fini, le panier.",
            "papa|Une seconde.",
            "papa|Voilà, je t'écoute.",
            "enfant-f|Il est pour les oranges rondes.",
            "maman|Merci d'avoir posé le panier.",
            "maman|Alors on va vers le stand.",
        ),
        "action",
        "panier,marche",
        "panier",
    )
    put(
        "CHK_T0001_P0001_Q0001",
        L(
            "narrateur|Mila a posé quelque chose contre papa.",
            "maman|Qu'est-ce que c'était ?",
        ),
        "clue",
        "",
        "panier",
    )
    extras["CHK_T0001_P0001_Q0001"] = qf(
        "panier",
        "panier | le panier | petit panier | le petit panier",
        "Elle l'a posé contre la manche. Qu'est-ce ?",
    )
    put(
        "CHK_T0001_P0001_C0001",
        L(
            "enfant-f|Le petit panier !",
            "narrateur|Oui, le panier vide.",
            "narrateur|Papa a entendu toute la phrase.",
            "narrateur|Ils avancent entre les caisses.",
            "papa|On suit ton panier ?",
            "enfant-f|Oui.",
        ),
        "confirm",
        "panier",
        "panier",
    )

    put(
        "CHK_T0001_P0002",
        L(
            "narrateur|Mila prend le filet orange.",
            "narrateur|Les mailles sont un peu rudes.",
            "enfant-f|Des oranges, s'il te plaît !",
            "narrateur|La marchande compte des tomates.",
            "narrateur|Elle dit des nombres, très vite.",
            "narrateur|Le filet s'agite sous le bras.",
            "narrateur|Personne ne lève les yeux.",
            "narrateur|Mila arrête le filet.",
            "narrateur|Elle le tient contre son ventre.",
            "narrateur|Les nombres s'arrêtent.",
            "narrateur|La marchande lève les yeux.",
            "maman|Elle te voit, maintenant.",
            "enfant-f|Le filet est pour les rondes.",
            "papa|Merci d'avoir tenu le filet.",
        ),
        "action",
        "filet,marche",
        "filet",
    )
    put(
        "CHK_T0001_P0002_Q0001",
        L(
            "narrateur|Mila tient quelque chose sans bouger.",
            "papa|Que tient-elle contre son ventre ?",
        ),
        "clue",
        "",
        "filet",
    )
    extras["CHK_T0001_P0002_Q0001"] = qf(
        "filet",
        "filet | le filet | filet orange | le filet orange",
        "Les mailles sont contre son ventre. Qu'est-ce ?",
    )
    put(
        "CHK_T0001_P0002_C0001",
        L(
            "enfant-f|Le filet !",
            "narrateur|Oui, le filet orange.",
            "narrateur|La marchande a vu le geste.",
            "narrateur|Le chemin vers les oranges s'ouvre.",
            "maman|On suit ton filet ?",
            "enfant-f|Oui.",
        ),
        "confirm",
        "filet",
        "filet",
    )

    put(
        "CHK_T0001_P0003",
        L(
            "narrateur|Papa glisse une pièce dans sa main.",
            "narrateur|Elle est froide, un peu lourde.",
            "enfant-f|Des oranges avec ça !",
            "narrateur|Mila parle et secoue la pièce.",
            "narrateur|Le tintement recouvre le mot orange.",
            "papa|J'entends la pièce, pas le mot.",
            "narrateur|Mila referme les doigts.",
            "narrateur|La pièce se tait dans la paume.",
            "papa|Là, je t'écoute.",
            "enfant-f|Les oranges rondes, pour le jus.",
            "maman|Merci pour tes doigts fermés.",
            "maman|On y va, la pièce est prête.",
        ),
        "action",
        "pieces,marche",
        "pièce",
    )
    put(
        "CHK_T0001_P0003_Q0001",
        L(
            "narrateur|Quelque chose a tinté, puis s'est tu.",
            "maman|Qu'est-ce qui tinte dans sa main ?",
        ),
        "clue",
        "",
        "pièce",
    )
    extras["CHK_T0001_P0003_Q0001"] = qf(
        "pièce",
        "pièce | la pièce | pièces | les pièces | une pièce",
        "Elle l'a tenue sans la secouer. Qu'est-ce ?",
    )
    put(
        "CHK_T0001_P0003_C0001",
        L(
            "enfant-f|La pièce !",
            "narrateur|Oui, la pièce silencieuse.",
            "narrateur|Papa a entendu le vrai mot.",
            "narrateur|Ils marchent vers les fruits ronds.",
            "papa|On garde la pièce au chaud ?",
            "enfant-f|Oui.",
        ),
        "confirm",
        "pieces",
        "pièce",
    )

    t2_pass = {
        (1, 1): L(
            "narrateur|Mila porte le panier vers la balance.",
            "narrateur|Des pommes occupent le plateau.",
            "narrateur|Elle pose le panier sur le métal.",
            "narrateur|L'aiguille saute entre pommes et osier.",
            "enfant-f|Mes oranges !",
            "narrateur|Papa demande le poids en même temps.",
            "narrateur|Les voix se mélangent au clic.",
            "narrateur|Mila reprend le panier.",
            "narrateur|Elle regarde le monsieur prendre ses pommes.",
            "narrateur|Le plateau redevient vide.",
            "enfant-f|Le panier, après les pommes.",
            "papa|Oui.",
            "papa|Le plateau est à toi.",
        ),
        (2, 1): L(
            "narrateur|Le filet s'accroche au crochet de fer.",
            "narrateur|La balance se balance, toute seule.",
            "narrateur|La marchande parle au monsieur des pommes.",
            "enfant-f|Attends, le filet !",
            "narrateur|Mila tire pendant que les autres parlent.",
            "narrateur|Personne ne voit le crochet.",
            "narrateur|Elle arrête de tirer.",
            "narrateur|Le filet pend, immobile.",
            "narrateur|Les pommes quittent le plateau.",
            "narrateur|La marchande se tourne.",
            "enfant-f|Le filet s'était accroché.",
            "maman|Je vois, maintenant.",
        ),
        (3, 1): L(
            "narrateur|Mila pose la pièce près des pommes.",
            "narrateur|L'aiguille ne sait plus que peser.",
            "enfant-f|C'est pour payer !",
            "narrateur|Papa parle du poids des pommes.",
            "narrateur|La pièce se perd dans le bruit.",
            "narrateur|Mila reprend la pièce.",
            "narrateur|Elle la serre, sans la secouer.",
            "narrateur|Le monsieur part avec son sac.",
            "narrateur|Le plateau est libre.",
            "enfant-f|La pièce est pour plus tard.",
            "papa|Bravo, l'aiguille peut respirer.",
            "maman|On pèse les oranges, là.",
        ),
        (1, 2): L(
            "narrateur|Le panier heurte le bord de la caisse.",
            "narrateur|Les oranges tremblent, tout en haut.",
            "narrateur|Maman parle du thym à la marchande.",
            "enfant-f|Attention à la caisse !",
            "narrateur|Sa phrase coupe celle de maman.",
            "narrateur|La marchande fronce un sourcil.",
            "narrateur|Mila plaque le panier contre son manteau.",
            "narrateur|Maman finit sa phrase sur le thym.",
            "narrateur|Un silence court arrive.",
            "enfant-f|Le panier a touché la caisse.",
            "maman|Je t'entends, cette fois.",
            "papa|Quelle orange tu veux ?",
        ),
        (2, 2): L(
            "narrateur|Une maille du filet pince une latte.",
            "narrateur|Mila tire, la caisse crisse.",
            "narrateur|La marchande décrit le thym à maman.",
            "enfant-f|Il est coincé !",
            "narrateur|Les deux voix couvrent la sienne.",
            "narrateur|Mila lâche la maille.",
            "narrateur|Les mots de thym s'arrêtent.",
            "narrateur|Le thym est choisi.",
            "narrateur|La marchande se tait.",
            "enfant-f|Le filet tenait la caisse.",
            "papa|On le détache ensemble.",
            "narrateur|L'orange du fond apparaît.",
        ),
        (3, 2): L(
            "narrateur|La pièce glisse entre deux oranges.",
            "enfant-f|Ma pièce !",
            "narrateur|La marchande compte le thym.",
            "narrateur|Elle n'interrompt pas son compte.",
            "narrateur|Mila reste les mains ouvertes.",
            "narrateur|Le dernier brin de thym est posé.",
            "enfant-f|Elle est entre les oranges.",
            "papa|Je la vois, près du fond.",
            "narrateur|Il tend la pièce, sans parler fort.",
            "maman|Merci d'avoir montré, sans crier.",
            "papa|On la garde pour la pesée ?",
            "enfant-f|Oui.",
        ),
        (1, 3): L(
            "narrateur|Mila pose le panier dans le chariot.",
            "narrateur|La roue tient le tapis du stand.",
            "narrateur|Papa tire, maman paie des fraises.",
            "narrateur|Deux gestes en même temps.",
            "narrateur|Le panier glisse vers le bord.",
            "narrateur|Mila l'attrape, sans crier.",
            "narrateur|Maman range la monnaie.",
            "enfant-f|Le panier allait tomber.",
            "papa|On recule le chariot, alors.",
            "narrateur|La roue quitte le tapis.",
            "narrateur|La balance reparaît.",
            "maman|On voit la balance.",
        ),
        (2, 3): L(
            "narrateur|Le filet pend et touche la roue.",
            "narrateur|Papa veut avancer le chariot.",
            "narrateur|Maman compte la monnaie des fraises.",
            "enfant-f|Stop !",
            "narrateur|Le mot tombe pendant les pièces.",
            "narrateur|Papa n'arrête pas tout de suite.",
            "narrateur|Mila tient le filet contre elle.",
            "narrateur|Maman dit merci à la marchande.",
            "enfant-f|Le filet touche la roue.",
            "papa|Je m'arrête.",
            "narrateur|Ils reculent le chariot d'un pas.",
            "maman|La roue est libre, maintenant.",
        ),
        (3, 3): L(
            "narrateur|La pièce roule sous le chariot.",
            "enfant-f|Elle est dessous !",
            "narrateur|Papa veut pousser pour chercher.",
            "narrateur|Maman tend l'argent des fraises.",
            "narrateur|La roue pourrait bouger.",
            "narrateur|Mila recule les mains.",
            "narrateur|La monnaie rejoint la poche.",
            "enfant-f|La pièce est sous le chariot.",
            "papa|On ne touche pas la roue.",
            "narrateur|Il se baisse, le chariot immobile.",
            "narrateur|La pièce reparaît, un peu poussiéreuse.",
            "maman|Merci, la pièce est là.",
        ),
    }

    t2_q = {
        1: L(
            "narrateur|Le plateau est libre, ou presque.",
            "papa|Une orange, le tas, ou le torchon ?",
            "maman|Comment on pose les fruits ?",
        ),
        2: L(
            "narrateur|Les oranges attendent dans le bois.",
            "papa|Une orange, le tas, ou le torchon ?",
            "maman|Comment on les sort ?",
        ),
        3: L(
            "narrateur|Le chariot peut recevoir les fruits.",
            "papa|Une orange, le tas, ou le torchon ?",
            "maman|Comment on les range ?",
        ),
    }

    t3_pass = {
        (1, 1): L(
            "narrateur|Mila pose une seule orange.",
            "narrateur|Sa main revient avec une deuxième.",
            "narrateur|L'aiguille n'a pas fini de bouger.",
            "narrateur|Elle retire la deuxième orange.",
            "narrateur|La balance fait clic.",
            "narrateur|L'aiguille s'arrête.",
            "papa|On peut en ajouter.",
            "enfant-f|Celle-là aussi.",
            "narrateur|Les autres suivent, une par une.",
            "maman|Le clic est net, cette fois.",
        ),
        (1, 2): L(
            "narrateur|Mila pose un petit tas d'un coup.",
            "narrateur|Une orange roule vers le bord.",
            "enfant-f|Quatre !",
            "narrateur|L'aiguille danse, le mot se perd.",
            "narrateur|Elle rattrape le fruit, sans parler.",
            "narrateur|Le tas s'immobilise.",
            "maman|Je dis le poids, maintenant ?",
            "papa|Oui, le tas est prêt.",
            "narrateur|La marchande lit l'aiguille.",
            "enfant-f|C'est lourd, ça brille.",
        ),
        (1, 3): L(
            "narrateur|Le plateau reste collant de pomme.",
            "narrateur|Mila prend le torchon rayé.",
            "narrateur|Papa approche une orange trop vite.",
            "enfant-f|Pas maintenant.",
            "narrateur|Elle essuie, puis elle regarde.",
            "narrateur|Le métal redevient mat.",
            "enfant-f|C'est sec.",
            "papa|On pose les oranges.",
            "narrateur|Le premier clic sonne net.",
            "maman|Le torchon a rendu le plateau.",
        ),
        (2, 1): L(
            "narrateur|Mila veut l'orange du fond.",
            "narrateur|Elle tire, la caisse penche.",
            "narrateur|La marchande range le thym.",
            "narrateur|Mila lâche le fruit.",
            "narrateur|La caisse se repose.",
            "narrateur|La marchande lève les yeux.",
            "enfant-f|Celle du fond, s'il te plaît.",
            "narrateur|Une main tend l'orange ronde.",
            "papa|Une seule, pour commencer.",
            "maman|Elle est froide, un peu lisse.",
        ),
        (2, 2): L(
            "narrateur|La marchande ramasse un tas.",
            "narrateur|Elle compte à voix haute.",
            "narrateur|Mila ajoute une orange au milieu.",
            "narrateur|Le compte se casse.",
            "narrateur|Elle remet le fruit dans la caisse.",
            "narrateur|Les nombres reprennent.",
            "enfant-f|Les nombres d'abord.",
            "papa|Le tas est le sien, maintenant.",
            "maman|Quatre, comme elle voulait.",
            "narrateur|Le bois de la caisse sent l'écorce.",
        ),
        (2, 3): L(
            "narrateur|Les oranges du haut sont mouillées.",
            "narrateur|Mila essuie la première au torchon.",
            "enfant-f|Quatre, s'il te plaît.",
            "narrateur|Elle parle pendant le geste.",
            "narrateur|La marchande n'a pas le nombre.",
            "narrateur|Mila finit d'essuyer.",
            "narrateur|Elle pose le torchon.",
            "enfant-f|Quatre.",
            "maman|Là, on a entendu.",
            "papa|Les ronds sont secs, prêts.",
        ),
        (3, 1): L(
            "narrateur|Mila pose une orange dans le chariot.",
            "narrateur|Elle roule vers la paroi.",
            "narrateur|Mila en ajoute une trop tôt.",
            "narrateur|Les deux se cognent.",
            "narrateur|Elle reprend la deuxième.",
            "narrateur|La première s'arrête.",
            "enfant-f|Maintenant, l'autre.",
            "papa|Une, puis l'autre.",
            "maman|Le chariot ne bouge plus.",
            "narrateur|Un petit choc, puis plus rien.",
        ),
        (3, 2): L(
            "narrateur|Mila verse un tas dans le chariot.",
            "narrateur|Les oranges roulent vers la roue.",
            "enfant-f|Elles partent !",
            "narrateur|Papa parle du chemin du retour.",
            "narrateur|Il n'a pas vu la roue.",
            "narrateur|Mila laisse papa finir.",
            "enfant-f|Le tas va vers la roue.",
            "papa|On les recule, alors.",
            "narrateur|Le tas se cale contre le bois.",
            "maman|Plus rien ne roule.",
        ),
        (3, 3): L(
            "narrateur|Le fond du chariot porte du sable.",
            "narrateur|Mila essuie avec le torchon.",
            "narrateur|Papa pose une orange trop tôt.",
            "narrateur|Le fruit frotte le grain.",
            "enfant-f|Le sable.",
            "narrateur|Papa n'entend pas, il charge.",
            "narrateur|Mila montre le torchon sale.",
            "papa|Pardon.",
            "papa|Je chargeais trop vite.",
            "narrateur|Elle finit le fond, toute seule.",
            "maman|Les oranges peuvent entrer, là.",
        ),
    }

    callbacks = {
        1: L(
            "narrateur|Les oranges rejoignent le petit panier.",
            "enfant-f|Il n'est plus vide.",
        ),
        2: L(
            "narrateur|Les oranges glissent dans le filet.",
            "enfant-f|Les mailles tiennent.",
        ),
        3: L(
            "narrateur|Mila tend la pièce, sans la secouer.",
            "enfant-f|Pour les oranges rondes.",
        ),
    }

    ends = {
        (1, 1, 1): L(
            "narrateur|À la maison, le petit panier pose sur la table.",
            "narrateur|La première orange reste à part.",
            "narrateur|Mila presse, un filet de jus tombe.",
            "papa|Tu entends ce petit clic ?",
            "enfant-f|Comme la balance.",
            "maman|Le jus est bon ?",
            "enfant-f|Il est froid, et sucré.",
            "narrateur|Deux verres s'alignent près du panier.",
            "narrateur|La première orange garde une feuille.",
        ),
        (1, 1, 2): L(
            "narrateur|Le panier déborde d'un tas lumineux.",
            "narrateur|Mila verse le jus, plus sombre.",
            "maman|Il sent fort, celui-là.",
            "enfant-f|C'est le tas entier.",
            "papa|Une a roulé sous la chaise.",
            "narrateur|Mila se baisse, sans parler.",
            "narrateur|Elle la pose au sommet du tas.",
            "narrateur|Sous la chaise, il ne reste rien.",
            "narrateur|Une orange du tas se repose, ronde.",
        ),
        (1, 1, 3): L(
            "narrateur|Le torchon rayé sèche sur la chaise.",
            "narrateur|Le panier tient les fruits propres.",
            "narrateur|Mila essuie un verre, puis presse.",
            "papa|Le plateau du marché n'est plus collant.",
            "maman|Grâce à ton torchon.",
            "enfant-f|Il sent la pomme un peu.",
            "narrateur|Une tache orange marque une rayure.",
            "narrateur|Le jus monte dans les deux verres.",
            "narrateur|Le torchon rayé sent l'orange et la pomme.",
        ),
        (1, 2, 1): L(
            "narrateur|L'orange du fond trône dans le panier.",
            "narrateur|Les autres attendent près de l'évier.",
            "enfant-f|Celle-là, d'abord.",
            "maman|Tu l'as dite après le thym.",
            "narrateur|Le jus de celle du fond est plus pâle.",
            "papa|On la reconnaît ?",
            "enfant-f|Oui.",
            "enfant-f|Elle était cachée.",
            "narrateur|Une écharde de caisse reste dans l'osier.",
            "narrateur|L'orange du fond brille toute seule.",
        ),
        (1, 2, 2): L(
            "narrateur|Le panier sent le bois de la caisse.",
            "narrateur|Le tas y tient, serré.",
            "narrateur|Mila presse deux fruits à la fois.",
            "papa|Le compte de la marchande était juste.",
            "enfant-f|J'ai remis celle en trop.",
            "maman|Le jus suffit pour trois gorgées.",
            "narrateur|Papa pose sa tasse, puis écoute.",
            "enfant-f|Il pique un peu.",
            "narrateur|Des fibres de caisse dorment dans l'osier.",
        ),
        (1, 2, 3): L(
            "narrateur|Le torchon laisse un rond d'eau.",
            "narrateur|Il brille sur le bois de la table.",
            "narrateur|Les oranges du panier sont mates, sèches.",
            "maman|Plus de goutte de marché.",
            "enfant-f|Je les ai essuyées.",
            "papa|On presse ?",
            "narrateur|Le jus tombe droit, sans glisser.",
            "narrateur|Mila pose le torchon près du panier.",
            "narrateur|Le rond d'eau rétrécit sur le bois.",
        ),
        (1, 3, 1): L(
            "narrateur|Le panier a voyagé dans le chariot.",
            "narrateur|Il pose près de la fenêtre.",
            "narrateur|La première orange n'a pas bougé.",
            "papa|Elle s'est calée, toute seule.",
            "enfant-f|Elle ne roulait plus.",
            "maman|Le jus de celle-là, pour toi.",
            "narrateur|Dehors, une roue lointaine se tait.",
            "narrateur|Mila boit, les yeux sur le panier.",
            "narrateur|Dans l'osier, la première orange tient.",
        ),
        (1, 3, 2): L(
            "narrateur|Le tas emplit le panier, un peu de travers.",
            "narrateur|Mila se souvient de la roue.",
            "enfant-f|Elles allaient partir.",
            "papa|Tu l'as dit après ma phrase.",
            "maman|Le jus va-t-il goûter la cour ?",
            "enfant-f|Un peu.",
            "enfant-f|Il est froid.",
            "narrateur|Ils boivent sur le pas de la porte.",
            "narrateur|Le panier reste à l'ombre.",
            "narrateur|La roue du chariot s'est tue dans la cour.",
        ),
        (1, 3, 3): L(
            "narrateur|Un grain de sable reste au torchon.",
            "narrateur|Le panier, lui, est propre.",
            "narrateur|Mila presse près de l'évier.",
            "papa|Sans sable dans le jus.",
            "enfant-f|J'ai montré le torchon sale.",
            "maman|On t'a vue, cette fois.",
            "narrateur|Deux verres, une pincée de sucre.",
            "narrateur|Le grain brille, oublié dans le tissu.",
            "narrateur|Le panier sent seulement l'écorce.",
        ),
        (2, 1, 1): L(
            "narrateur|Le filet pend près de la fenêtre.",
            "narrateur|Une orange reste dans un bol blanc.",
            "narrateur|Mila presse celle du clic unique.",
            "papa|Un fruit, un clic, un verre.",
            "maman|Les mailles ont gardé les autres.",
            "enfant-f|Celle-là a parlé en premier.",
            "narrateur|Une feuille reste prise dans une maille.",
            "narrateur|Le jus fait un rond sur la nappe.",
            "narrateur|Le filet pend, presque léger.",
        ),
        (2, 1, 2): L(
            "narrateur|Le filet a pris la forme du tas.",
            "narrateur|Il pose, bosselé, près des verres.",
            "enfant-f|Il était lourd, à la balance.",
            "papa|L'aiguille a dansé, puis stop.",
            "maman|On goûte le tas ?",
            "narrateur|Mila hoche la tête, la bouche pleine.",
            "narrateur|Un filet de jus fuit une maille.",
            "narrateur|Papa tend une assiette, sans parler.",
            "narrateur|Le filet garde la bosse du tas.",
        ),
        (2, 1, 3): L(
            "narrateur|Le filet et le torchon se touchent.",
            "narrateur|Ils pendent au même crochet.",
            "narrateur|Mila presse, les mains propres.",
            "maman|Plus de pomme sur les fruits.",
            "enfant-f|Le plateau était collant.",
            "papa|Ton torchon a tout pris.",
            "narrateur|Le jus tombe clair, sans fil.",
            "narrateur|Une rayure du torchon a rougi.",
            "narrateur|Le crochet tient les deux tissus.",
        ),
        (2, 2, 1): L(
            "narrateur|L'orange du fond appuie sur les mailles.",
            "narrateur|Mila la sort la dernière.",
            "enfant-f|C'est elle, la ronde.",
            "papa|Tu l'as nommée après le thym.",
            "maman|On la presse près de la fenêtre ?",
            "enfant-f|Oui.",
            "enfant-f|Pour voir la caisse, loin.",
            "narrateur|Dehors, le stand n'est plus là.",
            "narrateur|Le jus de la ronde est pâle.",
            "narrateur|Une maille garde la forme du fond.",
        ),
        (2, 2, 2): L(
            "narrateur|Une orange garde la marque du bois.",
            "narrateur|Le filet la serre avec les autres.",
            "narrateur|Mila presse celle à la marque.",
            "papa|Le compte n'a pas cassé, à la fin.",
            "enfant-f|J'ai retiré ma main.",
            "maman|Le jus porte un goût de caisse.",
            "narrateur|Ils rient, tout bas.",
            "narrateur|La marque s'estompe sous les doigts.",
            "narrateur|Le filet retombe, vide, sur la chaise.",
        ),
        (2, 2, 3): L(
            "narrateur|Une goutte tombe du filet sur le torchon.",
            "narrateur|Les oranges, essuyées, attendent.",
            "maman|Quatre, comme au stand.",
            "enfant-f|Je l'ai dit après le torchon.",
            "papa|On presse les quatre ?",
            "narrateur|Le jus emplit un pichet minuscule.",
            "narrateur|Mila tient le pichet à deux mains.",
            "narrateur|Le torchon absorbe la goutte du filet.",
            "narrateur|Il reste un rond humide, tout petit.",
        ),
        (2, 3, 1): L(
            "narrateur|Le filet repose sur le rebord du chariot.",
            "narrateur|Le chariot est rentré dans la cour.",
            "narrateur|Mila prend la première orange.",
            "papa|Celle qui ne roulait plus.",
            "enfant-f|Le choc, puis plus rien.",
            "maman|Le jus, sur le pas ?",
            "narrateur|Ils s'assoient sur la pierre froide.",
            "narrateur|Le filet pend dans la lumière.",
            "narrateur|La première orange a un goût de vent.",
        ),
        (2, 3, 2): L(
            "narrateur|Les mailles retiennent le tas, serrées.",
            "narrateur|Plus aucun bruit de roue.",
            "enfant-f|Elles voulaient la roue.",
            "papa|Tu l'as dit quand j'ai fini.",
            "maman|On partage le tas ?",
            "narrateur|Trois petites tasses, un pichet.",
            "narrateur|Mila verse sans parler.",
            "narrateur|Papa attend la dernière goutte.",
            "narrateur|Le filet garde un creux de tas.",
        ),
        (2, 3, 3): L(
            "narrateur|Le torchon a chassé le sable des mailles.",
            "narrateur|Le filet, propre, pend à la porte.",
            "papa|Pas de grain dans le jus.",
            "enfant-f|J'ai montré le tissu sale.",
            "maman|On t'a arrêtés, tous les deux.",
            "narrateur|Le jus coule, limpide.",
            "narrateur|Une maille sèche au soleil du seuil.",
            "narrateur|Mila lèche une goutte au pouce.",
            "narrateur|Le torchon, plié, sent le sable froid.",
        ),
        (3, 1, 1): L(
            "narrateur|La pièce repose près du verre de jus.",
            "narrateur|Mila presse l'orange du premier clic.",
            "papa|Elle n'a pas dansé avec les pommes.",
            "enfant-f|Je l'ai reprise.",
            "maman|Le jus paie cette pièce-là ?",
            "enfant-f|Oui.",
            "enfant-f|Sans la secouer.",
            "narrateur|Un rond de lumière touche la pièce.",
            "narrateur|Elle ne tinte plus.",
            "narrateur|Le verre s'emplit, tout près du métal.",
        ),
        (3, 1, 2): L(
            "narrateur|Papa a rendu une petite pièce.",
            "narrateur|Elle est collée d'une goutte de jus.",
            "enfant-f|Le tas était lourd.",
            "maman|L'aiguille a fini par s'arrêter.",
            "papa|On garde celle-là, collée ?",
            "narrateur|Mila la pose sur la soucoupe.",
            "narrateur|Ils boivent le jus du tas.",
            "narrateur|La goutte sèche, orange, sur le cuivre.",
            "narrateur|La soucoupe garde un petit cercle.",
        ),
        (3, 1, 3): L(
            "narrateur|La pièce sèche sur le torchon rayé.",
            "narrateur|Mila presse, les doigts propres.",
            "papa|Plus de pomme, plus de collant.",
            "enfant-f|J'ai dit : pas maintenant.",
            "maman|Le métal était prêt, lui aussi.",
            "narrateur|Le jus tombe dans un bol à fleurs.",
            "narrateur|La pièce ne glisse plus.",
            "narrateur|Une rayure du torchon brille, humide.",
            "narrateur|Le bol sent l'orange chaude.",
        ),
        (3, 2, 1): L(
            "narrateur|La pièce a payé l'orange du fond.",
            "narrateur|Rien d'autre, sur la table.",
            "enfant-f|Elle était entre les fruits.",
            "papa|Tu as montré, sans crier.",
            "maman|On la presse, celle du fond ?",
            "narrateur|Le jus est pâle, un peu acide.",
            "narrateur|Mila plisse le nez, puis reboit.",
            "narrateur|La pièce reste seule près du bol.",
            "narrateur|L'écorce du fond a une petite bosse.",
        ),
        (3, 2, 2): L(
            "narrateur|Deux pièces restent près du tas.",
            "narrateur|Mila en a tendu une, calme.",
            "papa|Le compte n'a pas cassé.",
            "enfant-f|J'ai remis l'orange.",
            "maman|Le jus du tas, pour tout le monde ?",
            "narrateur|Trois gorgées, trois sourires.",
            "narrateur|Une pièce roule, puis s'arrête.",
            "narrateur|Mila ne la ramasse pas tout de suite.",
            "narrateur|Elle finit son verre, d'abord.",
        ),
        (3, 2, 3): L(
            "narrateur|La pièce glisse dans une poche humide.",
            "narrateur|Le torchon a séché les quatre fruits.",
            "enfant-f|Quatre.",
            "enfant-f|Après le tissu.",
            "papa|On a entendu le nombre.",
            "maman|Le jus est-il moins mouillé ?",
            "enfant-f|Il est net.",
            "narrateur|Ils trinquent avec des verres trop grands.",
            "narrateur|La poche fait un bruit sourd, un coup.",
            "narrateur|Puis plus rien, sauf le jus.",
        ),
        (3, 3, 1): L(
            "narrateur|La pièce tinte une fois dans la coupe.",
            "narrateur|Mila presse l'orange qui ne roulait plus.",
            "papa|Sous le chariot, elle était poussiéreuse.",
            "enfant-f|Je n'ai pas mis la main.",
            "maman|Tu as parlé, la roue arrêtée.",
            "narrateur|Le jus couvre un peu la pièce.",
            "narrateur|Mila la sort, la pose à part.",
            "narrateur|Un silence de cuisine s'installe.",
            "narrateur|La pièce sèche, loin du verre.",
        ),
        (3, 3, 2): L(
            "narrateur|Le tas cache la pièce au fond du bol.",
            "narrateur|Mila verse le jus par-dessus.",
            "papa|Elles allaient vers la roue.",
            "enfant-f|Après tes mots, je l'ai dit.",
            "maman|On retrouve la pièce après ?",
            "narrateur|Mila plonge deux doigts, puis sourit.",
            "enfant-f|Elle est là, collée.",
            "narrateur|Ils la lavent sous l'eau froide.",
            "narrateur|Le tas, lui, a fini en jus doré.",
        ),
        (3, 3, 3): L(
            "narrateur|Le torchon enveloppe la pièce, près du verre.",
            "narrateur|Un peu de sable reste au pli.",
            "papa|Le fond du chariot est propre, maintenant.",
            "enfant-f|J'ai fini toute seule.",
            "maman|Le jus, sans grain ?",
            "enfant-f|Sans grain.",
            "narrateur|Ils boivent à petites gorgées.",
            "narrateur|Dehors, la bâche jaune n'est plus visible.",
            "narrateur|Le torchon garde la pièce au chaud.",
        ),
    }

    for a in (1, 2, 3):
        p = f"CHK_T0001_P000{a}"
        put(
            f"{p}_T0002_P0000",
            L(
                "narrateur|Les oranges attendent à trois endroits.",
                "papa|La balance, la caisse, ou le chariot ?",
                "maman|Où les met-on ?",
            ),
            "choice",
            "",
            None,
        )
        extras[f"{p}_T0002_P0000"] = t3("la balance", "la caisse", "le chariot")
        for b in (1, 2, 3):
            sp = f"{p}_T0002_P000{b}"
            put(sp, t2_pass[(a, b)], "obstacle", LOCS[b]["sons"], LOCS[b]["emp"])
            put(
                f"{sp}_T0003_P0000",
                t2_q[b],
                "choice",
                "",
                None,
            )
            extras[f"{sp}_T0003_P0000"] = t3("une orange", "le tas", "le torchon")
            for c in (1, 2, 3):
                leaf = f"{sp}_T0003_P000{c}"
                body = t3_pass[(b, c)] + callbacks[a]
                put(leaf, body, "resolution", WAYS[c]["sons"], WAYS[c]["emp"])
                fin = f"{leaf}_F0001"
                put(fin, ends[(a, b, c)], "ending", "jus,verres", "jus")

    # sanity: 27 unique endings
    fin_texts = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                cid = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}_F0001"
                txt, _ = from_script(s[cid])
                fin_texts.append(txt)
    if len(set(fin_texts)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fin_texts))}")

    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in s]
    extra_ids = set(s) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    by = {}
    for c in src["chunks"]:
        cid = c["chunk_id"]
        nc = make_chunk(c, s[cid], sons.get(cid, ""), 1.22, "medium")
        if cid in extras:
            nc.update(extras[cid])
        voice(nc, prof[cid], emph.get(cid), sons.get(cid, ""))
        by[cid] = nc

    out = dict(src)
    out["fil_rouge"] = (
        "Mila veut des oranges rondes pour le jus. Elle parle trop tôt, "
        "la marchande n'entend pas. Avec le panier, le filet ou les pièces, "
        "elle trouve comment être écoutée. À la balance, la caisse ou le chariot, "
        "un imprévu l'oblige à laisser finir l'autre. Une orange, un tas ou le torchon "
        "change la pesée. À la maison, le jus paie la goutte du plateau."
    )
    out["title"] = "La balance et les oranges de Mila"
    out["characters"] = "Mila, papa, maman"
    out["setting"] = "marché du village, stand d'oranges, puis la maison"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    blob = "\n".join(c["script"] for c in out["chunks"]).lower()
    for bad in ("on va apprendre", "voici le geste", "l'histoire est finie", "bon travail"):
        if bad in blob:
            raise SystemExit(f"reste interdit: {bad}")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{c['chunk_id']} fin mécanique: {last}")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    nwords = sum(words(c["text"]) for c in out["chunks"])
    path_lens = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
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
                path_lens.append(sum(words(by[i]["text"]) for i in ids))
    relecture = f"""# TREE-COL-010 — La balance et les oranges de Mila

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse
Mila veut les oranges rondes pour le jus. Au marché, sous la bâche jaune, elle crie trop tôt : la marchande parle aux poireaux, des pommes occupent la balance. Personne n'entend. Le panier, le filet ou les pièces changent la façon d'être écoutée. La balance, la caisse ou le chariot posent un autre obstacle. Une orange, le tas ou le torchon change la pesée. Vingt-sept fins ramènent le jus à la maison, chacune avec un objet du chemin.

## Vécu
Écouter / tour de parole : Mila parle dans le bruit, échoue, pose le panier / tient le filet / tait la pièce, puis on l'entend. À la pesée, elle laisse finir pommes, thym, monnaie, clic, compte ou essuyage. La leçon se voit, elle n'est pas dite.

## Vu et corrigé
- N1 ≤ 10 mots/phrase. Troupe D16 : Mila, papa, maman.
- Première tentative ratée dès l'ouverture.
- T1/T2/T3 changent l'action (plus seulement le lieu).
- 27 fins textuellement distinctes.
- TTS par fonction (opening/choice/clue/confirm/action/obstacle/resolution/ending).
- Un merci vécu, des questions d'adulte, `en ce moment`.
- Pas de « on lève la main / on attend / puis on parle ». Pas apply.

## Contrôles
- 86 chunks, 27 chemins
- {nwords} mots au total
- {min(path_lens)} à {max(path_lens)} mots par chemin, moyenne {sum(path_lens)//len(path_lens)}
- `check()` OK

## Non vérifié
Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.
"""
    (folder / "RELECTURE.md").write_text(relecture, encoding="utf-8")
    print(f"OK {SID} {nwords} mots  chemins {min(path_lens)}-{max(path_lens)}")


if __name__ == "__main__":
    main()
