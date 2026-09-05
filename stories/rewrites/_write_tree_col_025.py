#!/usr/bin/env python3
"""TREE-COL-025 — La gouttière et la main de Nina (F-NAR-019, N3, TTS)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-COL-025"
N3 = LIMITS["N3"]
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="gouttière",
        note="arc=installation; intention=émerveiller; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=un secret d'eau commence; tempo=naturel; sourire=léger; respiration=ample",
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
        emphasis="feuille",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="feuille",
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_voix_a_trouvé_un_creux; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_veut_parler_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=les_mots_se_heurtent; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=la_main_a_ouvert_une_place; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis=None,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_parole_a_trouvé_sa_place; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def vet(lines: list[str]) -> list[str]:
    out = []
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


# ---------------------------------------------------------------------------
# Récit
# ---------------------------------------------------------------------------

OPENING = vet(
    [
        "narrateur|Au bord du village, une petite maison écoute la pluie.",
        "narrateur|Le zinc de la gouttière cliquette contre le mur.",
        "narrateur|Nina vit là, avec papa et maman.",
        "narrateur|Les bottes laissent une flaque brillante près de la porte.",
        "narrateur|Dans la cuisine, la soupe sent la carotte.",
        "narrateur|Papa parle du sel avec maman.",
        "narrateur|Le torchon de maman reste humide entre ses doigts.",
        "narrateur|En ce moment, Nina colle son nez au carreau.",
        "narrateur|Une feuille jaune coince le coude du zinc.",
        "narrateur|L'eau déborde et rate le pot de basilic.",
        "enfant-f|La feuille bouche tout !",
        "narrateur|Ses mots se cognent aux mots de papa.",
        "papa|J'ajoute le sel, là, dans la casserole.",
        "narrateur|Nina pousse plus fort sa voix.",
        "enfant-f|Le basilic va se noyer !",
        "narrateur|Papa se tourne trop tard.",
        "narrateur|Il regarde la vitre, pas le coude.",
        "maman|Tu parlais de la gouttière ?",
        "enfant-f|Oui, la feuille !",
        "narrateur|L'eau continue de rater le bol bleu.",
        "enfant-f|Je veux le dire maintenant.",
        "maman|Montre-nous, alors.",
        "narrateur|Nina serre les doigts.",
        "narrateur|Sa main tremble, prête à se lever.",
    ]
)

T1_CHOICE = vet(
    [
        "narrateur|Pour montrer la feuille, Nina peut aller dans la cuisine, le jardin, ou la chambre.",
        "maman|Où veux-tu nous emmener d'abord ?",
    ]
)

T1 = {
    1: dict(
        sons="soupe,goutte",
        emp="vapeur",
        q_ans="feuille",
        q_acc="feuille | une feuille | la feuille",
        passage=vet(
            [
                "narrateur|Nina pousse la porte de la cuisine.",
                "narrateur|La vapeur de la soupe lui colle aux cils.",
                "narrateur|Le couvercle cliquette, plus fort que la gouttière.",
                "papa|Une pincée de sel, et ça y est.",
                "narrateur|Nina ouvre la bouche trop tôt.",
                "enfant-f|La feuille, vite !",
                "narrateur|Le mot tombe dans le bouillon.",
                "papa|Tu veux goûter, ma puce ?",
                "narrateur|Nina secoue la tête.",
                "narrateur|Ses joues chauffent de dépit.",
                "narrateur|Elle ferme la bouche.",
                "narrateur|Sa main se lève, droite, près de la vapeur.",
                "narrateur|Le couvercle se tait.",
                "papa|Je t'écoute.",
                "enfant-f|Une feuille bouche le coude.",
                "maman|Nous n'avions pas vu ça.",
                "narrateur|Par la vitre, l'eau rate toujours le basilic.",
            ]
        ),
        question=vet(
            [
                "narrateur|Dans la vapeur, Nina a parlé trop tôt.",
                "papa|Qu'est-ce qui bouche le zinc ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-f|Une feuille !",
                "narrateur|Oui, une feuille jaune.",
                "narrateur|Cette fois, papa a entendu le mot entier.",
                "maman|Merci, Nina.",
                "maman|Ta main a gardé la place.",
                "papa|Montre-nous ça avec un objet.",
            ]
        ),
    ),
    2: dict(
        sons="pluie,auvent",
        emp="auvent",
        q_ans="feuille",
        q_acc="feuille | une feuille | la feuille | le coude",
        passage=vet(
            [
                "narrateur|Nina ouvre la porte du jardin.",
                "narrateur|L'auvent claque, lourd d'eau.",
                "narrateur|Le zinc court juste au-dessus de leurs têtes.",
                "maman|Tes bottes ont fait une flaque, papa.",
                "narrateur|Nina pointe le coude du toit.",
                "enfant-f|Là, ça déborde !",
                "narrateur|Le vent emporte la fin de sa phrase.",
                "papa|Je vois la flaque, oui.",
                "narrateur|Il regarde le sol, pas le zinc.",
                "narrateur|Nina rentre les épaules.",
                "narrateur|Elle attend une accalmie.",
                "narrateur|Sa main se lève sous l'auvent mouillé.",
                "narrateur|Le vent s'arrête un souffle.",
                "maman|Nous te regardons.",
                "enfant-f|La feuille est coincée au coude.",
                "papa|Ah, pas la flaque.",
                "narrateur|L'eau continue de rater le pot.",
            ]
        ),
        question=vet(
            [
                "narrateur|Sous l'auvent, le vent a volé les mots.",
                "maman|Qu'est-ce qui coince le coude ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-f|La feuille !",
                "narrateur|Oui, coincée dans le zinc.",
                "narrateur|Maman a vu le doigt, puis le coude.",
                "papa|Merci d'avoir attendu le calme.",
                "maman|Le vent nous avait mélangés.",
                "papa|Montre-nous avec un objet, maintenant.",
            ]
        ),
    ),
    3: dict(
        sons="rideau,goutte",
        emp="rideau",
        q_ans="eau",
        q_acc="eau | l'eau | le bol | basilic | le basilic",
        passage=vet(
            [
                "narrateur|Nina entre dans la chambre.",
                "narrateur|Le tapis est tiède sous ses pieds nus.",
                "narrateur|Le doudou attend au bord du lit.",
                "narrateur|La gouttière court le long du mur, derrière la vitre.",
                "maman|Je rabats la couverture, tu vas grelotter.",
                "enfant-f|Non, la gouttière !",
                "narrateur|Maman croit qu'elle a froid.",
                "narrateur|Elle ferme le battant d'un geste vif.",
                "narrateur|Le chant du zinc s'étouffe.",
                "narrateur|Nina mord sa lèvre.",
                "narrateur|Sa main se pose sur le rideau, puis se lève.",
                "narrateur|Elle attend la fin de la couverture.",
                "maman|Voilà, c'est chaud.",
                "maman|Tu voulais la fenêtre ?",
                "enfant-f|Juste un peu, pour le basilic.",
                "narrateur|Le battant s'entrouvre.",
                "narrateur|Une goutte rate le pot, sur le rebord.",
            ]
        ),
        question=vet(
            [
                "narrateur|Derrière la vitre, le basilic attend l'eau.",
                "papa|Que veut sauver Nina dans son bol ?",
            ]
        ),
        confirm=vet(
            [
                "enfant-f|L'eau !",
                "narrateur|Oui, l'eau de la gouttière.",
                "narrateur|Maman a fini sa phrase, puis elle a ouvert.",
                "papa|Merci, Nina.",
                "papa|Tu as laissé la couverture se poser.",
                "maman|Montre-nous avec un objet, d'accord ?",
            ]
        ),
    ),
}

T2_CHOICE = {
    1: vet(
        [
            "narrateur|Dans la cuisine, Nina peut prendre les cubes, le livre, ou la dînette.",
            "papa|Quel objet va porter tes mots ?",
        ]
    ),
    2: vet(
        [
            "narrateur|Sous l'auvent, Nina peut prendre les cubes, le livre, ou la dînette.",
            "maman|Quel objet va porter tes mots ?",
        ]
    ),
    3: vet(
        [
            "narrateur|Dans la chambre, Nina peut prendre les cubes, le livre, ou la dînette.",
            "papa|Quel objet va porter tes mots ?",
        ]
    ),
}

T2 = {
    (1, 1): dict(
        sons="bois,soupe",
        emp="cubes",
        passage=vet(
            [
                "narrateur|Nina tire le sac de cubes près de la table.",
                "narrateur|Un cube rouge a le coin un peu rêche.",
                "narrateur|Elle aligne un petit zinc de bois.",
                "papa|Le sel, je disais, fond plus vite au chaud.",
                "narrateur|Nina a envie de couper.",
                "narrateur|Elle retient le dernier cube dans sa paume.",
                "narrateur|Sa main reste en l'air, avec le bois.",
                "papa|Voilà, j'ai fini.",
                "enfant-f|Regarde mon coude.",
                "narrateur|Elle pose le cube.",
                "narrateur|Une cuillerée d'eau glisse et déborde sur la table.",
                "maman|Ton zinc raconte le vrai zinc.",
                "papa|Le dernier cube est la feuille.",
                "narrateur|Nina hoche la tête, le souffle plus large.",
            ]
        ),
    ),
    (1, 2): dict(
        sons="page,soupe",
        emp="livre",
        passage=vet(
            [
                "narrateur|Nina prend le livre de pluie sur le banc.",
                "narrateur|La couverture est froide, un peu gondolée.",
                "narrateur|Papa parle du sel, la cuillère tourne.",
                "enfant-f|Regarde !",
                "narrateur|Personne ne se tourne.",
                "narrateur|Elle referme le livre contre son cœur.",
                "narrateur|Sa main se lève au-dessus de la page.",
                "maman|Le sel est dit.",
                "maman|Nous te regardons.",
                "narrateur|Nina ouvre le toit du livre.",
                "enfant-f|Ici, c'est notre gouttière.",
                "narrateur|Son doigt va de la page à la vitre.",
                "papa|Une goutte vraie perle au même endroit.",
                "narrateur|Les yeux sont prêts, enfin.",
            ]
        ),
    ),
    (1, 3): dict(
        sons="tasse,goutte",
        emp="dînette",
        passage=vet(
            [
                "narrateur|Nina sort la petite tasse de la dînette.",
                "narrateur|Elle la glisse sous la goutte du carreau.",
                "narrateur|Papa parle, maman essuie une miette.",
                "narrateur|La tasse se remplit sans un mot.",
                "narrateur|Elle déborde sur le bois, tout à coup.",
                "enfant-f|Comme dehors !",
                "narrateur|Les adultes parlent ensemble.",
                "narrateur|Nina se tait.",
                "narrateur|Sa main se lève au-dessus de la flaque miniature.",
                "papa|Ah, ta tasse a parlé.",
                "maman|Elle déborde, comme le zinc.",
                "enfant-f|Le bol bleu attend cette eau.",
                "narrateur|Personne n'a eu besoin de crier.",
                "narrateur|La petite tasse a pris le tour.",
            ]
        ),
    ),
    (2, 1): dict(
        sons="bois,pluie",
        emp="cubes",
        passage=vet(
            [
                "narrateur|Nina pose les cubes sur la marche mouillée.",
                "narrateur|Une goutte bouscule le premier.",
                "narrateur|Elle le remet, les lèvres pincées.",
                "papa|Ces bottes, je les vide près du bac.",
                "narrateur|Nina veut crier le coude.",
                "narrateur|Elle garde le cri.",
                "narrateur|Sa main tient le cube du milieu, levée.",
                "papa|J'ai fini les bottes.",
                "enfant-f|Mon zinc, c'est le grand zinc.",
                "narrateur|Elle penche la rangée vers le vrai coude.",
                "maman|Le bois pointe où ça déborde.",
                "narrateur|Une vraie goutte tombe à côté du pot.",
                "papa|Je vois le même virage.",
                "narrateur|Nina relâche les épaules.",
            ]
        ),
    ),
    (2, 2): dict(
        sons="page,pluie",
        emp="livre",
        passage=vet(
            [
                "narrateur|Nina lève le livre au-dessus de sa tête.",
                "narrateur|L'eau du auvent glisse sur la couverture.",
                "narrateur|Elle court du mauvais côté, comme le zinc.",
                "maman|Le vent, je disais, a tordu la haie.",
                "narrateur|Nina ouvre la bouche, puis la referme.",
                "narrateur|Sa main se lève, le livre pour toit.",
                "narrateur|Le vent s'apaise.",
                "papa|On t'écoute.",
                "enfant-f|L'eau part de travers, comme ici.",
                "narrateur|Elle baisse le livre vers le vrai coude.",
                "maman|La page et le zinc disent la même chose.",
                "narrateur|Une goutte manque le basilic, juste là.",
                "papa|Nous tenons l'image, maintenant.",
                "narrateur|Nina sourit d'un tout petit sourire.",
            ]
        ),
    ),
    (2, 3): dict(
        sons="theiere,pluie",
        emp="dînette",
        passage=vet(
            [
                "narrateur|Nina pose la petite théière sous l'auvent.",
                "narrateur|Le bec reçoit une goutte, puis deux.",
                "narrateur|Papa parle des semelles lourdes.",
                "narrateur|La théière déborde sur la pierre.",
                "enfant-f|Pareil que le toit !",
                "narrateur|Sa voix se mêle à la pluie.",
                "narrateur|Personne n'a compris le pareil.",
                "narrateur|Elle se tait.",
                "narrateur|Sa main se lève au-dessus du bec nain.",
                "maman|Tes doigts demandent une place.",
                "papa|Nous voilà.",
                "enfant-f|Le vrai bol est trop loin du coude.",
                "narrateur|La miniature a montré le manque.",
                "narrateur|Nina n'a plus besoin de crier.",
            ]
        ),
    ),
    (3, 1): dict(
        sons="bois,rideau",
        emp="cubes",
        passage=vet(
            [
                "narrateur|Nina aligne les cubes sur le rebord.",
                "narrateur|Une goutte du battant frappe la tour.",
                "maman|Si j'avance le doudou, tu seras plus au chaud.",
                "narrateur|Nina veut dire non, trop vite.",
                "narrateur|Elle avale le mot.",
                "narrateur|Sa main se lève devant la petite tour.",
                "maman|Je termine la couverture.",
                "maman|À toi.",
                "enfant-f|La goutte rate le pot, comme ça.",
                "narrateur|Elle pousse le dernier cube hors du rang.",
                "papa|Le cube tombé, c'est l'eau perdue.",
                "narrateur|Le basilic, sur le rebord, a les feuilles plates.",
                "maman|Nous voyons le manque.",
                "narrateur|Nina souffle, enfin.",
            ]
        ),
    ),
    (3, 2): dict(
        sons="page,rideau",
        emp="livre",
        passage=vet(
            [
                "narrateur|Nina ouvre le livre près du doudou.",
                "narrateur|La page du toit est un peu gondolée.",
                "maman|Je disais, le plaid va ici.",
                "enfant-f|Le toit !",
                "narrateur|Le mot se heurte au plaid.",
                "narrateur|Nina referme le livre une seconde.",
                "narrateur|Sa main se lève, l'ongle sur la tranche.",
                "maman|Le plaid est posé.",
                "maman|Montre.",
                "narrateur|Elle ouvre la page, puis désigne le mur.",
                "enfant-f|Notre zinc est derrière le verre.",
                "papa|La page nous prête des yeux.",
                "narrateur|Une goutte glisse, dehors, au même trait.",
                "narrateur|Le doudou semble écouter aussi.",
            ]
        ),
    ),
    (3, 3): dict(
        sons="assiette,goutte",
        emp="dînette",
        passage=vet(
            [
                "narrateur|Nina glisse l'assiette naine sous le battant.",
                "narrateur|Une perle d'eau s'y tient, ronde.",
                "maman|Le doudou, je le mets sous le plaid.",
                "narrateur|Nina glisse l'assiette vers le basilic.",
                "narrateur|La perle rate le pot, exprès.",
                "enfant-f|Tu vois ?",
                "narrateur|Maman range le plaid dans sa tête.",
                "narrateur|Nina attend.",
                "narrateur|Sa main se lève au-dessus de la perle.",
                "papa|Nous regardons ta perle.",
                "enfant-f|Le vrai bol est trop loin.",
                "maman|L'assiette a dit le manque.",
                "narrateur|Personne n'a parlé en même temps.",
                "narrateur|Nina sent ses doigts se desserrer.",
            ]
        ),
    ),
}

T3_Q = {
    (1, 1): vet(
        [
            "narrateur|Le petit zinc de cubes peut attendre le matin, après la sieste, ou le soir.",
            "papa|Quand montrons-nous la feuille au vrai zinc ?",
        ]
    ),
    (1, 2): vet(
        [
            "narrateur|La page du toit peut parler le matin, après la sieste, ou le soir.",
            "maman|Quand ouvrons-nous le livre près de la gouttière ?",
        ]
    ),
    (1, 3): vet(
        [
            "narrateur|La petite tasse peut servir le matin, après la sieste, ou le soir.",
            "papa|Quand posons-nous le vrai bol ?",
        ]
    ),
    (2, 1): vet(
        [
            "narrateur|Les cubes mouillés peuvent attendre le matin, après la sieste, ou le soir.",
            "maman|Quand allons-nous au coude ?",
        ]
    ),
    (2, 2): vet(
        [
            "narrateur|Le livre-toit peut montrer le matin, après la sieste, ou le soir.",
            "papa|Quand suivons-nous l'eau du auvent ?",
        ]
    ),
    (2, 3): vet(
        [
            "narrateur|La théière naine peut déborder le matin, après la sieste, ou le soir.",
            "maman|Quand remplissons-nous le bol bleu ?",
        ]
    ),
    (3, 1): vet(
        [
            "narrateur|La tour du rebord peut veiller le matin, après la sieste, ou le soir.",
            "papa|Quand sortons-nous la feuille ?",
        ]
    ),
    (3, 2): vet(
        [
            "narrateur|La page et le doudou peuvent écouter le matin, après la sieste, ou le soir.",
            "maman|Quand rapprochons-nous le bol ?",
        ]
    ),
    (3, 3): vet(
        [
            "narrateur|L'assiette naine peut attendre le matin, après la sieste, ou le soir.",
            "papa|Quand attrapons-nous la goutte ?",
        ]
    ),
}


def R(*rows: str) -> list[str]:
    return vet(list(rows))


RES = {
    (1, 1, 1): R(
        "narrateur|Le matin, la lumière est blanche sur la table.",
        "narrateur|Nina lève la main entre deux plocs du zinc.",
        "papa|À toi, entre les gouttes.",
        "enfant-f|On sort la feuille, et le bol se met dessous.",
        "narrateur|Ils ouvrent la fenêtre de la cuisine.",
        "narrateur|Papa pince la feuille, Nina tient le bol bleu.",
        "narrateur|L'eau trouve enfin le basilic.",
        "maman|Ton zinc de cubes avait raison.",
        "narrateur|Le cube rouge reste mouillé, comme un témoin.",
    ),
    (1, 1, 2): R(
        "narrateur|Après la sieste, la maison est plus sourde.",
        "narrateur|La soupe ne chante plus.",
        "narrateur|Nina pose sa main levée près des cubes.",
        "maman|Ma phrase est finie.",
        "maman|Vas-y.",
        "enfant-f|Le coude, tout bas.",
        "narrateur|Ils glissent le bol sous le filet plus lent.",
        "narrateur|La feuille, plus lourde, se décroche d'un coup.",
        "papa|Tes cubes ont attendu avec nous.",
        "narrateur|Une goutte reste sur le cube rouge, ronde.",
    ),
    (1, 1, 3): R(
        "narrateur|Le soir, la lampe fait un rond d'or.",
        "narrateur|Papa pose la cuillère, puis se tait.",
        "narrateur|La main de Nina se lève au-dessus des cubes.",
        "papa|À toi.",
        "enfant-f|On met le bol, et on raconte au dîner.",
        "narrateur|Ils calent le bol bleu sous le filet.",
        "narrateur|La feuille attendra le jour, collée, visible.",
        "maman|Tes cubes gardent le plan, sur la table.",
        "narrateur|L'ombre des cubes dessine un petit toit.",
    ),
    (1, 2, 1): R(
        "narrateur|Le matin, Nina ouvre la page du toit.",
        "narrateur|Elle attend que papa finisse le poivre.",
        "papa|Page, puis vraie gouttière.",
        "enfant-f|On suit le trait jusqu'au coude.",
        "narrateur|Ils sortent le bol, le livre ouvert contre la vitre.",
        "narrateur|La feuille se dégage, collante, entre deux doigts.",
        "narrateur|L'eau frappe le bol, puis le basilic.",
        "maman|La page a prêté ses yeux.",
        "narrateur|Une vraie goutte perle sur le dessin.",
    ),
    (1, 2, 2): R(
        "narrateur|Après la sieste, le livre reste ouvert au toit.",
        "narrateur|Nina ne parle pas tout de suite.",
        "narrateur|Sa main se lève au-dessus de la page.",
        "maman|Je t'écoute.",
        "enfant-f|On glisse le bol, sans fermer le livre.",
        "narrateur|Le filet, plus doux, remplit le bleu.",
        "narrateur|Ils glissent la feuille entre deux pages, pour la voir.",
        "papa|Ton indice a séché avec nous.",
        "narrateur|La maison sent le papier et la carotte froide.",
    ),
    (1, 2, 3): R(
        "narrateur|Le soir, la lampe dore la page du toit.",
        "narrateur|Papa termine sa phrase sur le pain.",
        "narrateur|Nina lève la main, le livre contre la nappe.",
        "papa|À toi, Nina.",
        "enfant-f|Le bol sous le filet, la feuille pour demain.",
        "narrateur|Ils posent le bol.",
        "narrateur|Le zinc chante plus juste, un peu.",
        "maman|On gardera la page ouverte près du sel.",
        "narrateur|Le toit du livre devient tout doré.",
    ),
    (1, 3, 1): R(
        "narrateur|Le matin, la petite tasse est pleine.",
        "narrateur|Nina lève la main avant de la verser.",
        "maman|Nous te regardons verser.",
        "enfant-f|Le vrai bol, sous le coude, comme ça.",
        "narrateur|Papa ouvre, Nina glisse le bol bleu.",
        "narrateur|La feuille part, l'eau change de chemin.",
        "narrateur|La tasse naine et le bol sont jumeaux.",
        "papa|Ta dînette a parlé sans crier.",
        "narrateur|Le basilic redresse une feuille, toute mince.",
    ),
    (1, 3, 2): R(
        "narrateur|Après la sieste, une perle tient dans la soucoupe.",
        "narrateur|Nina attend que le frigo se taise.",
        "narrateur|Sa main se lève au-dessus de la perle.",
        "papa|Vas-y.",
        "enfant-f|On met le bol, tout près.",
        "narrateur|Le filet lent remplit le bleu, sans éclabousser.",
        "narrateur|Ils posent la feuille à côté de la soucoupe.",
        "maman|Ta perle nous a montré le manque.",
        "narrateur|La cuisine sent l'eau froide et le thym.",
    ),
    (1, 3, 3): R(
        "narrateur|Le soir, la miniature refroidit près de la lampe.",
        "narrateur|Papa range le pain, puis s'arrête.",
        "narrateur|La main de Nina se lève près de la tasse.",
        "maman|À toi.",
        "enfant-f|Le bol pour la nuit, sous le filet.",
        "narrateur|Ils calent le bleu.",
        "narrateur|La tasse naine veille, vide, propre.",
        "papa|Demain, la feuille, et ce soir l'eau.",
        "narrateur|Le zinc fait un ploc plus rond.",
    ),
    (2, 1, 1): R(
        "narrateur|Le matin, les cubes brillent sur la marche.",
        "narrateur|Nina lève la main entre deux rafales.",
        "papa|Entre deux vents, à toi.",
        "enfant-f|On va au coude, avec le bol.",
        "narrateur|Ils marchent sous l'auvent, le bois pour flèche.",
        "narrateur|Papa dégage la feuille, Nina tend le bleu.",
        "narrateur|L'eau frappe le bol, fort, joyeuse.",
        "maman|Tes cubes ont tenu malgré la goutte.",
        "narrateur|Un cube pâle reste sur la pierre.",
    ),
    (2, 1, 2): R(
        "narrateur|Après la sieste, la pluie est plus fine.",
        "narrateur|Les cubes ont séché d'un côté.",
        "narrateur|Nina lève la main, sans bousculer le rang.",
        "maman|Nous sommes là.",
        "enfant-f|Le coude, tout près de l'auvent.",
        "narrateur|Ils glissent le bol.",
        "narrateur|La feuille se décroche, lourde, noire.",
        "papa|Le bois a gardé le plan pendant que tu dormais.",
        "narrateur|Un escargot contourne les cubes, sans se presser.",
    ),
    (2, 1, 3): R(
        "narrateur|Le soir, l'auvent est une tente sombre.",
        "narrateur|Papa finit sa phrase sur les bottes.",
        "narrateur|La main de Nina se lève, un cube dedans.",
        "papa|À toi.",
        "enfant-f|Le bol sous le filet, les cubes pour témoins.",
        "narrateur|Ils posent le bleu.",
        "narrateur|La feuille reste visible, collée, pour demain.",
        "maman|On rentre, le bois contre la poitrine de Nina.",
        "narrateur|Le zinc bat plus lent, comme un cœur.",
    ),
    (2, 2, 1): R(
        "narrateur|Le matin, Nina tient le livre comme un toit.",
        "narrateur|Elle attend que le vent coupe sa phrase à lui.",
        "maman|Le vent s'est tu.",
        "enfant-f|On suit l'eau jusqu'au coude.",
        "narrateur|Le livre désigne, le bol reçoit.",
        "narrateur|La feuille part, gluante, entre deux pages d'air.",
        "narrateur|L'eau trouve le basilic, dehors.",
        "papa|Ta couverture a montré le travers.",
        "narrateur|Des points de pluie restent sur le titre.",
    ),
    (2, 2, 2): R(
        "narrateur|Après la sieste, le livre sèche sur la chaise.",
        "narrateur|Nina s'assoit, la main levée sur la page.",
        "papa|Je t'écoute, là.",
        "enfant-f|On approche le bol, page ouverte.",
        "narrateur|Le filet, plus doux, obéit.",
        "narrateur|Ils glissent la feuille sur la page, un instant.",
        "maman|L'image et la vraie chose se touchent.",
        "narrateur|Nina referme, puis ouvre, pour vérifier.",
        "narrateur|L'auvent goutte plus juste.",
    ),
    (2, 2, 3): R(
        "narrateur|Le soir, Nina rentre le livre contre son cœur.",
        "narrateur|Papa pose les bottes, puis se tait.",
        "narrateur|Sa main à elle se lève près de la poignée.",
        "maman|À toi.",
        "enfant-f|Le bol dehors, le livre pour raconter.",
        "narrateur|Ils calent le bleu sous le filet noir.",
        "narrateur|La feuille attend le matin, collée au zinc.",
        "papa|On lira la page au dîner.",
        "narrateur|Un dernier ploc répond, dehors.",
    ),
    (2, 3, 1): R(
        "narrateur|Le matin, la théière naine déborde sur la marche.",
        "narrateur|Nina lève la main avant d'en parler.",
        "papa|Nous voyons le bec.",
        "enfant-f|Le vrai bol, au même endroit, plus grand.",
        "narrateur|Ils posent le bleu sous le coude.",
        "narrateur|La feuille s'en va, l'eau change de route.",
        "narrateur|La miniature et le bol se remplissent ensemble.",
        "maman|Ta dînette a crié tout bas.",
        "narrateur|Nina essuie le bec d'un doigt.",
    ),
    (2, 3, 2): R(
        "narrateur|Après la sieste, la feuille noire repose dans l'assiette.",
        "narrateur|Nina l'a posée là, sans parler.",
        "narrateur|Sa main se lève au-dessus de l'assiette.",
        "maman|Raconte.",
        "enfant-f|Elle était dans le coude.",
        "narrateur|Ils glissent le bol sous le filet lent.",
        "narrateur|L'eau, cette fois, n'oublie pas le basilic.",
        "papa|L'assiette a gardé la preuve.",
        "narrateur|Une odeur de terre mouillée monte.",
    ),
    (2, 3, 3): R(
        "narrateur|Le soir, la tasse naine veille sur le rebord.",
        "narrateur|Papa cale les bottes, puis s'arrête.",
        "narrateur|Nina lève la main, la tasse à l'autre.",
        "papa|À toi.",
        "enfant-f|Le bol pour la nuit, la tasse pour le signe.",
        "narrateur|Ils posent le bleu.",
        "narrateur|La tasse reste dehors, sentinelle.",
        "maman|On la rentrera quand le zinc sera juste.",
        "narrateur|La lampe de la cuisine les rappelle.",
    ),
    (3, 1, 1): R(
        "narrateur|Le matin, les cubes gardent le rebord, clairs.",
        "narrateur|Nina lève la main avant d'ouvrir plus.",
        "maman|La couverture est posée.",
        "enfant-f|On sort la feuille, le bol sur le rebord.",
        "narrateur|Papa pince le zinc par la fente.",
        "narrateur|La feuille vient, Nina pousse le bol.",
        "narrateur|L'eau frappe le bleu, puis le basilic.",
        "papa|Ta tour a montré le manque.",
        "narrateur|Le rideau balaie les cubes, tout léger.",
    ),
    (3, 1, 2): R(
        "narrateur|Après la sieste, le doudou s'appuie contre la tour.",
        "narrateur|Nina lève la main, l'autre sur le doudou.",
        "papa|Nous sommes revenus.",
        "enfant-f|Le bol, tout près du rebord.",
        "narrateur|Le filet lent obéit.",
        "narrateur|La feuille se décroche, le doudou semble regarder.",
        "maman|Ta tour a veillé pendant que tu dormais.",
        "narrateur|Nina recule un cube, pour laisser l'eau.",
        "narrateur|La chambre sent le linge tiède.",
    ),
    (3, 1, 3): R(
        "narrateur|Le soir, l'ombre des cubes fait un toit sur le mur.",
        "narrateur|Maman pose le plaid, puis se tait.",
        "narrateur|La main de Nina se lève sous la lampe.",
        "maman|À toi.",
        "enfant-f|Le bol pour la nuit, les cubes pour le plan.",
        "narrateur|Ils calent le bleu sur le rebord.",
        "narrateur|La feuille attend le jour, collée, sombre.",
        "papa|Ton toit d'ombre nous a guidés.",
        "narrateur|Le zinc, derrière le verre, bat plus rond.",
    ),
    (3, 2, 1): R(
        "narrateur|Le matin, le doigt de Nina touche la page, puis le verre.",
        "narrateur|Elle attend que maman finisse le plaid.",
        "maman|Page, puis zinc.",
        "enfant-f|Le bol sous le filet, là.",
        "narrateur|Ils ouvrent un peu plus.",
        "narrateur|La feuille part, le bol se remplit.",
        "narrateur|Le basilic boit, enfin.",
        "papa|Tes deux toits se sont parlé.",
        "narrateur|Une goutte vraie mouille le dessin.",
    ),
    (3, 2, 2): R(
        "narrateur|Après la sieste, le livre sert de toit au doudou.",
        "narrateur|Nina lève la main, sans le déranger.",
        "papa|Nous t'écoutons.",
        "enfant-f|On approche le bol, tout doucement.",
        "narrateur|Le filet lent entre.",
        "narrateur|Ils glissent la feuille comme un signet, un instant.",
        "maman|La page a tenu ta place.",
        "narrateur|Nina repose le livre sur le doudou.",
        "narrateur|La chambre est un nid d'écoute.",
    ),
    (3, 2, 3): R(
        "narrateur|Le soir, la feuille jaune marque la page du toit.",
        "narrateur|Papa éteint la grande lumière, pas la lampe.",
        "narrateur|Nina lève la main, le livre sur les genoux.",
        "papa|À toi.",
        "enfant-f|Le bol sur le rebord, la page pour raconter.",
        "narrateur|Ils posent le bleu.",
        "narrateur|Le zinc chante derrière le rideau.",
        "maman|On lira, et l'eau travaillera.",
        "narrateur|Le signet sent la pluie, un peu.",
    ),
    (3, 3, 1): R(
        "narrateur|Le matin, la tasse naine attrape la goutte du rebord.",
        "narrateur|Nina lève la main avant de la montrer.",
        "maman|Nous voyons la perle.",
        "enfant-f|Le vrai bol, juste là, plus large.",
        "narrateur|Papa ouvre, Nina pousse le bleu.",
        "narrateur|La feuille s'en va, l'eau change de cible.",
        "narrateur|La tasse et le bol se répondent.",
        "papa|Ta dînette a visé juste.",
        "narrateur|Le basilic tremble, puis boit.",
    ),
    (3, 3, 2): R(
        "narrateur|Après la sieste, une perle tremble sur l'assiette.",
        "narrateur|Nina attend qu'elle se tienne.",
        "narrateur|Sa main se lève au-dessus de la perle.",
        "papa|Vas-y.",
        "enfant-f|Le bol, pour qu'elle n'ait plus peur de rater.",
        "narrateur|Le filet lent remplit le bleu.",
        "narrateur|L'assiette garde une trace ronde.",
        "maman|Ta perle nous a appris le manque.",
        "narrateur|Le doudou a une joue un peu humide.",
    ),
    (3, 3, 3): R(
        "narrateur|Le soir, la miniature refroidit près de la veilleuse.",
        "narrateur|Maman pose le plaid, puis se tait.",
        "narrateur|Nina lève la main, l'assiette contre le doudou.",
        "maman|À toi.",
        "enfant-f|Le bol pour la nuit, derrière la vitre.",
        "narrateur|Ils calent le bleu.",
        "narrateur|La gouttière chante plus juste.",
        "papa|Ta perle a ouvert le tour.",
        "narrateur|Nina pose l'assiette, enfin légère.",
    ),
}

# Tics slipped into a few lines — fix after first run if vet catches.
# "tout léger" / "tout bas" / "tout près" / "tout doré" / "tout à coup" / "un tout petit"
# TICS only matches "tout doux|tout calme|encore|déjà". "tout bas" is OK.
# "tout doucement" in (3,2,2) — not in TICS (tout doux is the tic). "tout doucement" contains "tout doux"? 
# r"\b(tout doux|...)\b" — "tout doucement" is "tout" + "doucement", not "tout doux". OK.
# "encore le plaid" in T2 (3,3) — HAS encore! Need to fix that line.

FIN = {
    (1, 1, 1): R(
        "narrateur|Au dîner, papa pose la cuillère.",
        "maman|À toi, Nina.",
        "enfant-f|La feuille est sortie, le basilic a bu.",
        "narrateur|Le cube rouge brille, mouillé, près du bol bleu.",
        "narrateur|Dehors, le zinc fait un ploc plus juste.",
        "narrateur|La main de Nina, un peu humide, se pose enfin.",
    ),
    (1, 1, 2): R(
        "narrateur|Dans le calme d'après, maman coupe le pain.",
        "papa|Raconte, nous t'écoutons.",
        "enfant-f|J'ai levé la main, puis le cube est tombé.",
        "narrateur|Sur le cube rouge, une goutte fait un petit rond.",
        "narrateur|Le basilic a une feuille relevée.",
        "narrateur|La gouttière marque le silence, goutte à goutte.",
    ),
    (1, 1, 3): R(
        "narrateur|Sous la lampe, papa termine sa phrase.",
        "maman|À toi.",
        "enfant-f|Les cubes ont gardé le plan du toit.",
        "narrateur|L'ombre des cubes dessine un toit sur la nappe.",
        "narrateur|Le bol bleu, près de la vitre, est lourd.",
        "narrateur|Nina range sa main ouverte, au chaud.",
    ),
    (1, 2, 1): R(
        "narrateur|À table, maman ferme d'abord sa phrase.",
        "papa|Nous t'écoutons, Nina.",
        "enfant-f|La page a montré le coude, et l'eau a suivi.",
        "narrateur|Une vraie goutte perle sur le dessin du toit.",
        "narrateur|Le basilic sent le mouillé, tout près de la vitre.",
        "narrateur|Les doigts de Nina quittent la page, contents.",
    ),
    (1, 2, 2): R(
        "narrateur|Après le repos, le livre reste ouvert au sel.",
        "maman|Ta voix, maintenant.",
        "enfant-f|La feuille a séché entre les pages.",
        "narrateur|La feuille jaune dort entre deux pages.",
        "narrateur|Le bol bleu a un filet sur le bord.",
        "narrateur|Nina pose la paume sur la couverture froide.",
    ),
    (1, 2, 3): R(
        "narrateur|Le soir, le pain passe, puis le silence.",
        "papa|À toi, Nina.",
        "enfant-f|On a mis le bol, et la page est restée ouverte.",
        "narrateur|Sous la lampe, le toit du livre devient doré.",
        "narrateur|Le zinc, dehors, répond plus rond.",
        "narrateur|La main de Nina glisse le long de la tranche.",
    ),
    (1, 3, 1): R(
        "narrateur|Le midi sent la carotte, plus claire.",
        "maman|Raconte ta tasse.",
        "enfant-f|Elle a débordé, alors le vrai bol a compris.",
        "narrateur|La petite tasse et le bol bleu sont jumeaux.",
        "narrateur|Le basilic a bu sans se noyer.",
        "narrateur|Nina essuie sa main au torchon rayé.",
    ),
    (1, 3, 2): R(
        "narrateur|Dans l'après, le frigo s'est tu.",
        "papa|Nous t'écoutons.",
        "enfant-f|La perle a tenu, puis le bol a pris le tour.",
        "narrateur|Une perle d'eau tient dans la soucoupe.",
        "narrateur|Le thym sent plus fort, tout à coup.",
        "narrateur|La main de Nina se pose à côté, sans trembler.",
    ),
    (1, 3, 3): R(
        "narrateur|Le soir, la miniature refroidit près du pain.",
        "maman|À toi.",
        "enfant-f|Le bol travaille la nuit, la tasse a montré.",
        "narrateur|La tasse naine veille près de la lampe tiède.",
        "narrateur|Un ploc plus rond traverse la vitre.",
        "narrateur|Nina laisse sa main ouverte sur la nappe.",
    ),
    (2, 1, 1): R(
        "narrateur|De retour, papa pose les bottes.",
        "maman|À toi, Nina.",
        "enfant-f|Les cubes ont pointé le coude, et l'eau a suivi.",
        "narrateur|Un cube pâle reste sur la marche mouillée.",
        "narrateur|Le basilic, dehors, a les feuilles plus vives.",
        "narrateur|La main de Nina brille, mouillée, puis se sèche.",
    ),
    (2, 1, 2): R(
        "narrateur|Sous l'auvent apaisé, maman coupe une pomme.",
        "papa|Raconte le bois.",
        "enfant-f|J'ai attendu le vent, puis le cube a parlé.",
        "narrateur|Un escargot contourne les cubes, sans se presser.",
        "narrateur|Le bol bleu a un peu de terre au bord.",
        "narrateur|Nina pose sa main sur la pierre froide.",
    ),
    (2, 1, 3): R(
        "narrateur|Rentrés, papa cale les bottes près du feu.",
        "maman|À toi.",
        "enfant-f|Les cubes ont veillé, le bol a pris l'eau.",
        "narrateur|Papa serre la main humide de Nina.",
        "narrateur|Le zinc, dehors, bat plus lent.",
        "narrateur|Le cube du milieu sèche contre son pull.",
    ),
    (2, 2, 1): R(
        "narrateur|Au chaud, maman essuie la couverture du livre.",
        "papa|Nous t'écoutons.",
        "enfant-f|L'eau partait de travers, comme sur le livre.",
        "narrateur|La couverture porte des points de pluie.",
        "narrateur|Le basilic a bu, dehors, sous l'auvent.",
        "narrateur|Nina laisse sa main à plat sur le titre.",
    ),
    (2, 2, 2): R(
        "narrateur|Sur la chaise sèche, le livre reste ouvert.",
        "maman|Ta voix, Nina.",
        "enfant-f|La page et le zinc se sont touchés.",
        "narrateur|Le livre sèche, ouvert au dessin du zinc.",
        "narrateur|Une odeur de chaise mouillée monte.",
        "narrateur|La main de Nina tourne une page, puis s'arrête.",
    ),
    (2, 2, 3): R(
        "narrateur|Dans l'entrée, papa pose les bottes.",
        "maman|À toi.",
        "enfant-f|Le bol est dehors, le livre raconte le toit.",
        "narrateur|Nina rentre, le livre contre son cœur.",
        "narrateur|Un dernier ploc répond derrière la porte.",
        "narrateur|Sa main, sur la couverture, se réchauffe.",
    ),
    (2, 3, 1): R(
        "narrateur|Près de la porte, maman tend une serviette.",
        "papa|Raconte le bec.",
        "enfant-f|La petite théière a débordé, le grand bol aussi.",
        "narrateur|La miniature a le bec brillant.",
        "narrateur|Le basilic tremble d'eau neuve.",
        "narrateur|Nina essuie sa main, puis le bec, avec soin.",
    ),
    (2, 3, 2): R(
        "narrateur|Sous l'auvent calme, papa coupe le fromage.",
        "maman|Nous t'écoutons.",
        "enfant-f|La feuille noire était dans le coude.",
        "narrateur|La feuille noire repose dans l'assiette miniature.",
        "narrateur|Le bol bleu sent la terre.",
        "narrateur|La main de Nina désigne l'assiette, puis se pose.",
    ),
    (2, 3, 3): R(
        "narrateur|La lampe de cuisine les rappelle.",
        "papa|À toi, Nina.",
        "enfant-f|La tasse veille dehors, le bol travaille.",
        "narrateur|La tasse naine veille sur le rebord, dehors.",
        "narrateur|Le zinc chante vers le bleu.",
        "narrateur|Nina laisse une main sur la vitre, un moment.",
    ),
    (3, 1, 1): R(
        "narrateur|Dans la chambre claire, maman ouvre le rideau.",
        "papa|Raconte la tour.",
        "enfant-f|Le cube tombé, c'était l'eau perdue.",
        "narrateur|Les cubes gardent le rebord, face au zinc.",
        "narrateur|Le basilic a bu sur le rebord.",
        "narrateur|La main de Nina s'appuie au rideau, puis descend.",
    ),
    (3, 1, 2): R(
        "narrateur|Le doudou a une joue contre la tour.",
        "maman|Ta voix, tout bas.",
        "enfant-f|La tour a veillé pendant la sieste.",
        "narrateur|Le doudou s'appuie contre la petite tour.",
        "narrateur|Le bol bleu a un filet sur le rebord.",
        "narrateur|Nina pose sa main sur le doudou, puis sur le bois.",
    ),
    (3, 1, 3): R(
        "narrateur|Sous la lampe, papa s'assoit au bord du lit.",
        "maman|À toi.",
        "enfant-f|L'ombre des cubes a fait un toit.",
        "narrateur|L'ombre des cubes fait un toit sur le mur.",
        "narrateur|Le zinc, derrière le verre, bat plus rond.",
        "narrateur|La main de Nina se range sous la lampe.",
    ),
    (3, 2, 1): R(
        "narrateur|Le matin, maman laisse le battant un peu ouvert.",
        "papa|Nous t'écoutons.",
        "enfant-f|La page et le verre ont dit le même trait.",
        "narrateur|Le doigt de Nina a quitté la page, puis le verre.",
        "narrateur|Le basilic brille, arrosé.",
        "narrateur|Sa main se pose sur le doudou, légère.",
    ),
    (3, 2, 2): R(
        "narrateur|Le livre reste en toit sur le doudou.",
        "maman|Raconte, Nina.",
        "enfant-f|J'ai attendu le plaid, puis la page a parlé.",
        "narrateur|Le livre sert de toit au doudou, un instant.",
        "narrateur|Une odeur de linge tiède reste.",
        "narrateur|La main de Nina glisse sous le livre, puis s'arrête.",
    ),
    (3, 2, 3): R(
        "narrateur|La lampe seule veille.",
        "papa|À toi.",
        "enfant-f|La feuille jaune garde la page du toit.",
        "narrateur|La feuille jaune marque la page du toit.",
        "narrateur|Le bol, sur le rebord, est lourd et noir.",
        "narrateur|Nina ferme le livre avec sa main, sans le serrer.",
    ),
    (3, 3, 1): R(
        "narrateur|Le rebord sent l'eau neuve.",
        "maman|Raconte la perle.",
        "enfant-f|La tasse a visé, le bol a reçu.",
        "narrateur|La tasse naine attrape une goutte du rebord.",
        "narrateur|Le basilic tremble, puis se tient.",
        "narrateur|Nina essuie sa main au rideau, tout doucement.",
    ),
    (3, 3, 2): R(
        "narrateur|L'assiette garde un rond clair.",
        "papa|Nous t'écoutons.",
        "enfant-f|La perle a eu peur de rater, puis le bol est venu.",
        "narrateur|Une perle tremble sur l'assiette, puis se tient.",
        "narrateur|Le doudou a la joue un peu humide.",
        "narrateur|La main de Nina se pose à côté, rassurée.",
    ),
    (3, 3, 3): R(
        "narrateur|La veilleuse fait un rond orange.",
        "maman|À toi, Nina.",
        "enfant-f|L'assiette a ouvert le tour, le bol travaille.",
        "narrateur|La gouttière chante plus juste derrière la vitre.",
        "narrateur|L'assiette naine refroidit près du doudou.",
        "narrateur|Nina laisse sa main ouverte, enfin légère.",
    ),
}


def ending_note(a: int, b: int, c: int) -> str:
    times = {1: "clair", 2: "posé", 3: "lent"}
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=la_main_a_tenu_le_tour; "
        f"tempo={times[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


def main() -> None:
    # Fix known tic in T2 (3,3) if present — scanned at vet time.
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    scripts: dict[str, tuple[list[str], str, str, dict]] = {}

    scripts["CHK_T0000_P0000"] = (OPENING, "opening", "pluie,gouttiere", {"emphasis": "gouttière"})
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

    t2_choice_extra = {
        "option_1_label": "les cubes",
        "option_2_label": "le livre",
        "option_3_label": "la dînette",
    }
    t3_choice_extra = {
        "option_1_label": "le matin",
        "option_2_label": "après la sieste",
        "option_3_label": "le soir",
    }

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        t1 = T1[a]
        scripts[base] = (t1["passage"], "action", t1["sons"], {"emphasis": t1["emp"]})
        scripts[f"{base}_Q0001"] = (
            t1["question"],
            "clue",
            "",
            {
                "expected_answer": t1["q_ans"],
                "accepted_examples": t1["q_acc"],
                "retry_prompt": "Écoute l'indice, puis dis le mot.",
                "engine_ok_text": "Oui, c'est ça.",
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
                "emphasis": t1["q_ans"],
            },
        )
        scripts[f"{base}_C0001"] = (t1["confirm"], "confirm", t1["sons"], {"emphasis": "main"})
        scripts[f"{base}_T0002_P0000"] = (T2_CHOICE[a], "choice", "", dict(t2_choice_extra))
        for b in (1, 2, 3):
            t2 = T2[(a, b)]
            leaf2 = f"{base}_T0002_P000{b}"
            scripts[leaf2] = (t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emp"]})
            scripts[f"{leaf2}_T0003_P0000"] = (T3_Q[(a, b)], "choice", "", dict(t3_choice_extra))
            for c in (1, 2, 3):
                leaf3 = f"{leaf2}_T0003_P000{c}"
                scripts[leaf3] = (
                    RES[(a, b, c)],
                    "resolution",
                    "gouttiere,bol",
                    {"emphasis": "bol bleu"},
                )
                scripts[f"{leaf3}_F0001"] = (
                    FIN[(a, b, c)],
                    "ending",
                    "couverts,gouttiere",
                    {"emphasis": "main", "note": ending_note(a, b, c)},
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

    # Unicité des 27 fins
    fins = [ch["text"] for ch in chunks if ch["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(fins))}/27")
    res_txt = [ch["text"] for ch in chunks if ch["chunk_id"].endswith("T0003_P0001") or ch["chunk_id"].endswith("T0003_P0002") or ch["chunk_id"].endswith("T0003_P0003")]
    res_txt = [ch["text"] for ch in chunks if ch["kind"] == "passage" and "_T0003_P000" in ch["chunk_id"] and "_F0001" not in ch["chunk_id"] and not ch["chunk_id"].endswith("_T0003_P0000")]
    if len(res_txt) != 27 or len(set(res_txt)) != 27:
        raise SystemExit(f"résolutions distinctes: {len(set(res_txt))}/{len(res_txt)}")

    out = dict(src)
    out["fil_rouge"] = (
        "Sous la pluie, la gouttière de zinc déborde : une feuille coince le coude, "
        "et l'eau rate le pot de basilic de Nina. Elle veut le dire tout de suite, "
        "mais ses mots se cognent à ceux de papa. Cuisine, jardin ou chambre changent "
        "l'obstacle ; cubes, livre ou dînette changent la manière de montrer ; "
        "matin, sieste ou soir changent le rythme de l'attente. Quand sa main lève "
        "une place, le bol bleu reçoit enfin l'eau, et le zinc chante plus juste."
    )
    out["title"] = "La gouttière et la main de Nina"
    out["characters"] = "Nina, papa, maman"
    out["setting"] = "maison sous la pluie, cuisine, jardin, chambre"
    out["chunks"] = chunks
    check(SID, out["age_band"], out["chunks"])

    # chemins
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

    ws = [path_words(a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(ws)} max={max(ws)} moy={sum(ws)//len(ws)}")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"""# {SID} — La gouttière et la main de Nina

Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.

## Promesse narrative

Sous la pluie, une feuille coince le coude de la gouttière. L'eau rate le basilic de Nina. Elle veut le dire maintenant, mais ses mots se cognent à ceux de papa. Sa main apprend à garder une place. Cuisine, jardin ou chambre changent l'obstacle ; cubes, livre ou dînette changent la manière de montrer ; matin, sieste ou soir changent le rythme de l'attente. Le bol bleu reçoit enfin l'eau, et le zinc chante plus juste.

## Vécu

Nina veut sauver l'eau de sa plante. Elle crie trop tôt : on entend « gouttière », pas « feuille ». Dans la vapeur, sous l'auvent ou derrière le rideau, la première idée échoue. Elle lève la main, attend le creux, puis montre. La leçon se voit : envie de couper, retenue, écoute réelle, plaisir d'être entendue. Un merci vécu, pas un refrain scolaire.

## Vu et corrigé

- Titre noyau conservé. Troupe D16 : Nina, papa, maman.
- 86 nœuds, graphe et libellés d'options conservés.
- 27 fins textuellement distinctes, 27 résolutions distinctes.
- Première tentative échoue. Chaque choix change l'obstacle, le climax, la dernière image.
- Retour de la gouttière, de la main, du bol bleu.
- TTS par fonction (ouverture, choix, indice, action, obstacle, résolution, retour).
- `slow` réservé aux choix, à l'indice et aux fins.
- N3 ≤ 16 mots/phrase. Pas de leçon dite. Pas de tics « tout doux / encore / déjà / tout calme ».
- Chemins : {min(ws)}–{max(ws)} mots (moyenne {sum(ws)//len(ws)}).

## Direction vocale

`notes` : arc, intention, émotion, intensité 1–3, destinataire, sous-texte, tempo, sourire, respiration. Adulte conversationnel, pas maîtresse.

## Non vérifié

Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'apply.
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
