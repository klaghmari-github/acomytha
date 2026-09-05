#!/usr/bin/env python3
"""TREE-DIF-027 — Les cuillères de Sarah sous la véranda (N1, DIF.PAR.001, F-NAR-019)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-027"
N1 = 10
TITLE = "Les cuillères de Sarah sous la véranda"
FIL = (
    "Sarah veut accrocher ses cuillères sous la véranda pour qu'elles sonnent "
    "avant le vent du soir. Aniss arrive : elle veut un ding, lui répond "
    "avec les mains. T1 = cuillère / clochette / ficelle, les trois partent. "
    "T2 = étendoir (nœud rusé) / poutre (fil qui glisse) / marche (vent et limite). "
    "T3 = neuf façons d'attendre, tendre, suivre. Le grain de savon rose luit. "
    "On rentre à la soupe."
)
CHARS = "Sarah, Aniss, papa, maman"
SETTING = "cuisine, véranda, étendoir, poutre, marche du jardin"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain de savon rose",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_grain_rose_attend_Aniss_répond_avec_les_mains; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_le_geste; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_tend; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "grain de savon rose",
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=la_première_idée_a_raté_le_doigt_suffit; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=elle_veut_un_ding_Aniss_touche; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=le_lieu_ruse_Aniss_pose_sa_limite; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "grain de savon rose",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=attendre_tendre_suivre_le_doigt; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain de savon rose",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_rose_paie_l_ouverture; tempo=posé; sourire=léger; respiration=ample",
    },
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict, emphasis: str | None) -> str:
    body = esc(text)
    if emphasis:
        e = esc(emphasis)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict, emphasis: str | None) -> str:
    body = text
    if emphasis:
        body = body.replace(emphasis, f"<emphasis>{emphasis}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m["pitchTag"]:
        body = f"<{m['pitchTag']}>{body}</{m['pitchTag']}>"
    tail = "[long-pause]" if m["pause"] >= 800 else ("[pause]" if m["pause"] >= 400 else "")
    return f"{body} {tail}".strip()


def vet(lines: list[str]) -> list[str]:
    out = []
    prev = ""
    run = 1
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > N1:
            raise SystemExit(f"{n}>{N1}: {ph}")
        if n == 0:
            raise SystemExit(f"vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"fin: {ph}")
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"tic {tic!r}: {ph}")
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"tic {m.group(0)!r}: {ph}")
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


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    lines = vet(lines)
    m = dict(PROFILES[profile])
    extra = extra or {}
    emphasis = extra.get("emphasis", m["emphasis"])
    text, script = from_script(lines)
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else ""
    nc["text_ssml"] = ssml(text, m, emphasis)
    nc["text_xai_tags"] = xai(text, m, emphasis)
    nc["length_scale_piper"] = m["piper"]
    nc["rate_label"] = m["rate"]
    nc["rate_wpm"] = m["wpm"]
    nc["speed_xai"] = m["speed"]
    nc["pitch_label"] = m["pitch"]
    nc["pitch_ssml"] = m["pitchSsml"]
    nc["pitch_xai_tag"] = m["pitchTag"]
    nc["volume_label"] = m["volume"]
    nc["volume_db"] = m["db"]
    nc["emphasis_words"] = emphasis or ""
    nc["pause_before_ms"] = extra.get("pause_before", 0)
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
    nc["notes"] = extra.get("notes", m["note"])
    nc["night_policy"] = "play"
    nc["locale"] = "fr-FR"
    nc["voice_id"] = "fr_FR-siwis-medium"
    for k, v in extra.get("fields", {}).items():
        nc[k] = v
    return nc


def path_words(by: dict, a: int, b: int, c: int) -> int:
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
    return sum(words(by[i]["text"]) for i in ids)


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


T3_LABS = {
    1: ("le linge", "la cuillère", "le panier"),
    2: ("le tabouret", "le clou plus bas", "les mains d'Aniss"),
    3: ("le vent", "le linge", "le pilier"),
}


OPENING = [
    "narrateur|Sarah connaît la cuisine, ses odeurs.",
    "narrateur|La soupe fume, près du verre.",
    "narrateur|Les carreaux de la véranda restent tièdes.",
    "narrateur|Le rideau souffle vers le jardin.",
    "narrateur|Un détail paraît neuf, ce soir.",
    "narrateur|Dans le creux, un grain de savon rose.",
    "papa|Ça tinte, Sarah.",
    "enfant-f|Mes cuillères vont chanter, dehors.",
    "maman|Avant le vent du soir ?",
    "enfant-f|Oui, sous la véranda.",
    "narrateur|En ce moment, le sac d'Aniss frotte.",
    "enfant-f|Dis ding !",
    "narrateur|Aniss pose un doigt sur le métal.",
    "narrateur|Le sourire de Sarah part.",
    "narrateur|Dans sa poitrine, ça se bouscule.",
    "papa|Il a répondu, avec le doigt.",
    "maman|Tu peux lui tendre, et attendre.",
    "papa|Merci, tu as vu son doigt.",
]

T1_CHOICE = [
    "narrateur|Le panier reste ouvert, près des pieds.",
    "narrateur|Une cuillère y brille, tiède.",
    "narrateur|Une clochette, puis une ficelle, à côté.",
    "papa|Tu prends quoi d'abord, Sarah ?",
]

T1 = {
    1: {
        "sons": "metal,panier",
        "emphasis": "cuillère",
        "passage": [
            "narrateur|Sarah prend d'abord la cuillère tiède.",
            "enfant-f|Elle sent le savon.",
            "papa|Le grain rose est dans le creux.",
            "narrateur|Le métal est un peu mouillé.",
            "narrateur|Elle la tend vers Aniss, trop vite.",
            "enfant-f|Dis ding !",
            "narrateur|Aniss pose un doigt, sans mot.",
            "narrateur|Ça fait un tout petit tic.",
            "maman|La clochette et la ficelle viennent aussi.",
            "narrateur|Papa glisse le tout dans le panier.",
            "narrateur|Rien ne reste sur la table.",
            "enfant-f|Aniss, on part ?",
            "narrateur|Aniss hoche la tête, minuscule.",
            "papa|La cuillère d'abord, vous l'avez.",
        ],
        "question": [
            "narrateur|Sarah a tendu la cuillère, tout près.",
            "maman|Elle tend quoi, à Aniss ?",
        ],
        "qfields": {
            "expected_answer": "cuillère",
            "accepted_examples": "cuillère | la cuillère | le métal | tendre",
            "retry_prompt": "Elle tend la cuillère. Elle tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss prend la cuillère contre lui.",
            "enfant-f|Elle est à toi, un moment.",
            "narrateur|Sarah attend, les mains ouvertes.",
            "narrateur|Un tic se fait, minuscule.",
            "narrateur|Le grain de savon rose reste au creux.",
            "maman|Le métal est tiède, maintenant.",
            "papa|On accroche le fil où ?",
            "enfant-f|Sous la véranda.",
            "narrateur|Aniss ne dit rien, et c'est une réponse.",
        ],
    },
    2: {
        "sons": "clochette,panier",
        "emphasis": "clochette",
        "passage": [
            "narrateur|Sarah prend d'abord la clochette froide.",
            "enfant-f|Elle va tinter.",
            "maman|Le métal est un peu rêche.",
            "narrateur|Elle la tend vers Aniss, trop vite.",
            "enfant-f|Dis ding !",
            "narrateur|Aniss la tient à deux mains.",
            "narrateur|Ça tinte une fois, puis s'arrête.",
            "papa|La cuillère et la ficelle viennent aussi.",
            "narrateur|Maman les pose près du panier.",
            "narrateur|Tout part ensemble, dans le sac.",
            "enfant-f|Aniss, tu viens ?",
            "narrateur|Aniss lève la clochette, bas.",
            "narrateur|Le grain rose voyage avec le métal.",
            "maman|La clochette d'abord, vous l'avez.",
        ],
        "question": [
            "narrateur|Sarah a tendu la clochette, tout près.",
            "papa|Elle tend quoi, à Aniss ?",
        ],
        "qfields": {
            "expected_answer": "clochette",
            "accepted_examples": "clochette | la clochette | la cloche | tendre",
            "retry_prompt": "Elle tend la clochette. Elle tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss garde la clochette contre sa jambe.",
            "enfant-f|Elle est à toi, un moment.",
            "narrateur|Sarah attend, sans répéter ding.",
            "narrateur|Le métal sent le tiroir.",
            "narrateur|Le grain de savon rose reste au creux.",
            "maman|Le fil peut grandir, après.",
            "papa|On accroche le fil où ?",
            "enfant-f|Sous la véranda.",
            "narrateur|Aniss appuie le métal, sans un mot.",
        ],
    },
    3: {
        "sons": "ficelle,panier",
        "emphasis": "ficelle",
        "passage": [
            "narrateur|Sarah prend d'abord la ficelle douce.",
            "enfant-f|C'est pour le fil.",
            "papa|Elle sent le tiroir.",
            "narrateur|Elle tend le peloton vers Aniss, trop vite.",
            "enfant-f|Dis fil !",
            "narrateur|Aniss enroule un bout, lent.",
            "narrateur|Le fil se fait, sans un mot.",
            "maman|La cuillère et la clochette viennent aussi.",
            "narrateur|Papa les glisse près du sac.",
            "narrateur|Le panier les garde, toutes les trois.",
            "enfant-f|Aniss, c'est bon ?",
            "narrateur|Aniss appuie sur le fil, minuscule.",
            "narrateur|Le grain rose voyage dans le creux.",
            "papa|La ficelle d'abord, elle tient.",
        ],
        "question": [
            "narrateur|Sarah a tendu la ficelle, tout près.",
            "maman|Elle tend quoi, à Aniss ?",
        ],
        "qfields": {
            "expected_answer": "ficelle",
            "accepted_examples": "ficelle | la ficelle | le fil | tendre",
            "retry_prompt": "Elle tend la ficelle. Elle tend quoi ?",
        },
        "confirm": [
            "narrateur|Aniss tient la ficelle, tout près.",
            "enfant-f|Elle est à toi, un moment.",
            "narrateur|Sarah attend, les lèvres fermées.",
            "narrateur|Le fil bouge un peu, puis s'arrête.",
            "narrateur|Le grain de savon rose reste au creux.",
            "papa|La véranda va le voir, plus tard.",
            "maman|On accroche le fil où ?",
            "enfant-f|Dehors, au bois.",
            "narrateur|Aniss serre le peloton, sans un mot.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|La cuillère voyage dans le panier.",
        "narrateur|Dehors, le fil peut aller en trois coins.",
        "narrateur|Un linge mouillé barre l'étendoir.",
        "narrateur|Plus haut, un clou attend sur la poutre.",
        "narrateur|Plus bas, le vent pousse la marche.",
        "papa|On commence où, pour le fil ?",
    ],
    2: [
        "narrateur|La clochette voyage dans le panier.",
        "narrateur|Dehors, le fil peut aller en trois coins.",
        "narrateur|Un linge mouillé barre l'étendoir.",
        "narrateur|Plus haut, un clou attend sur la poutre.",
        "narrateur|Plus bas, le vent pousse la marche.",
        "maman|On commence où, pour le fil ?",
    ],
    3: [
        "narrateur|La ficelle voyage dans le panier.",
        "narrateur|Dehors, le fil peut aller en trois coins.",
        "narrateur|Un linge mouillé barre l'étendoir.",
        "narrateur|Plus haut, un clou attend sur la poutre.",
        "narrateur|Plus bas, le vent pousse la marche.",
        "papa|On commence où, pour le fil ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "linge,nœud",
        "emphasis": "étendoir",
        "passage": [
            "narrateur|La cuillère frotte le linge mouillé.",
            "narrateur|Un torchon barre le bois de l'étendoir.",
            "enfant-f|Pousse-le, Aniss !",
            "narrateur|Sarah tire le nœud, trop fort.",
            "narrateur|Le nœud se resserre, rusé.",
            "enfant-f|Dis-moi où !",
            "narrateur|Aniss montre le nœud, du doigt.",
            "narrateur|Le sourire de Sarah ne revient pas.",
            "enfant-f|Je veux le ding, maintenant.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "maman|Le linge reste lourd, au milieu.",
            "narrateur|Aniss ouvre un peu le panier.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 1): {
        "sons": "linge,clochette",
        "emphasis": "étendoir",
        "passage": [
            "narrateur|La clochette s'accroche au linge.",
            "narrateur|Un torchon étouffe le tintement, au bois.",
            "enfant-f|Pousse-le, Aniss !",
            "narrateur|Sarah tire le nœud, trop fort.",
            "narrateur|Le nœud se resserre, rusé.",
            "enfant-f|Dis ding, pour trouver !",
            "narrateur|Aniss montre le nœud, du doigt.",
            "narrateur|Le sourire de Sarah ne revient pas.",
            "enfant-f|Je veux le ding, maintenant.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Maman s'accroupit, à leur hauteur.",
            "papa|Le linge reste lourd, au milieu.",
            "narrateur|Aniss pose la clochette, dans le panier.",
            "maman|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 1): {
        "sons": "linge,ficelle",
        "emphasis": "étendoir",
        "passage": [
            "narrateur|La ficelle s'enroule dans le linge.",
            "narrateur|Un torchon avale le peloton, au bois.",
            "enfant-f|Pousse-le, Aniss !",
            "narrateur|Sarah tire le nœud, trop fort.",
            "narrateur|Le nœud se resserre, rusé.",
            "enfant-f|Dis où, Aniss !",
            "narrateur|Aniss montre le nœud, du doigt.",
            "narrateur|Le sourire de Sarah ne revient pas.",
            "enfant-f|Je veux le fil, maintenant.",
            "narrateur|Sarah refuse de foncer.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "maman|Le linge reste lourd, au milieu.",
            "narrateur|Aniss tient un bout, sans tirer.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 2): {
        "sons": "bois,fil",
        "emphasis": "poutre",
        "passage": [
            "narrateur|La cuillère n'atteint pas le clou.",
            "enfant-f|Le clou est trop haut.",
            "narrateur|Sarah lève les talons, trop petite.",
            "enfant-f|Pousse, Aniss !",
            "narrateur|Aniss lève les bras.",
            "narrateur|Ses doigts frôlent le bois, pas plus.",
            "narrateur|Le fil glisse, rusé, vers le sol.",
            "enfant-f|Je veux le ding, là-haut.",
            "narrateur|Sarah refuse de sauter.",
            "narrateur|Maman s'accroupit, à leur hauteur.",
            "papa|Le tabouret dort près du seuil.",
            "narrateur|Un clou plus bas brille aussi.",
            "narrateur|Aniss recule d'un pas, les bras bas.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 2): {
        "sons": "bois,clochette",
        "emphasis": "poutre",
        "passage": [
            "narrateur|La clochette tinte trop bas, sous le bois.",
            "enfant-f|Le clou est trop haut.",
            "narrateur|Sarah lève les talons, trop petite.",
            "enfant-f|Pousse, Aniss !",
            "narrateur|Aniss lève les bras.",
            "narrateur|Ses doigts frôlent le bois, pas plus.",
            "narrateur|Le fil glisse, rusé, vers le sol.",
            "enfant-f|Je veux le ding, là-haut.",
            "narrateur|Sarah refuse de sauter.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "maman|Le tabouret dort près du seuil.",
            "narrateur|Un clou plus bas brille aussi.",
            "narrateur|Aniss couvre la clochette, d'une main.",
            "maman|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 2): {
        "sons": "bois,ficelle",
        "emphasis": "poutre",
        "passage": [
            "narrateur|La ficelle pend, trop courte, sous la poutre.",
            "enfant-f|Le clou est trop haut.",
            "narrateur|Sarah lève les talons, trop petite.",
            "enfant-f|Pousse, Aniss !",
            "narrateur|Aniss lève les bras.",
            "narrateur|Ses doigts frôlent le bois, pas plus.",
            "narrateur|Le fil glisse, rusé, vers le sol.",
            "enfant-f|Je veux le fil, là-haut.",
            "narrateur|Sarah refuse de sauter.",
            "narrateur|Maman s'accroupit, à leur hauteur.",
            "papa|Le tabouret dort près du seuil.",
            "narrateur|Un clou plus bas brille aussi.",
            "narrateur|Aniss enroule le peloton, contre lui.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 3): {
        "sons": "vent,cuillere",
        "emphasis": "marche",
        "passage": [
            "narrateur|La cuillère claque au vent, trop fort.",
            "enfant-f|Le vent est trop grand.",
            "narrateur|Les cuillères se cognent, trop fort.",
            "enfant-f|Aniss, on court ?",
            "narrateur|Aniss recule d'un pas, près du pilier.",
            "narrateur|Il serre le métal contre lui.",
            "narrateur|Le fil fouette, rusé, vers le jardin.",
            "enfant-f|Je veux le ding, dehors.",
            "narrateur|Sarah refuse de courir.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "maman|Le fil n'aime pas ce vent.",
            "papa|Un linge sec attend sur la marche.",
            "narrateur|Aniss cache le creux, des deux mains.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 3): {
        "sons": "vent,clochette",
        "emphasis": "marche",
        "passage": [
            "narrateur|La clochette chante trop vite, au vent.",
            "enfant-f|Le vent est trop grand.",
            "narrateur|Les cuillères se cognent, trop fort.",
            "enfant-f|Aniss, on court ?",
            "narrateur|Aniss recule d'un pas, près du pilier.",
            "narrateur|Il serre le métal contre lui.",
            "narrateur|Le fil fouette, rusé, vers le jardin.",
            "enfant-f|Je veux le ding, dehors.",
            "narrateur|Sarah refuse de courir.",
            "narrateur|Maman s'accroupit, à leur hauteur.",
            "papa|Le fil n'aime pas ce vent.",
            "maman|Un linge sec attend sur la marche.",
            "narrateur|Aniss bouche la clochette, d'une paume.",
            "maman|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 3): {
        "sons": "vent,ficelle",
        "emphasis": "marche",
        "passage": [
            "narrateur|La ficelle fouette la marche, trop sec.",
            "enfant-f|Le vent est trop grand.",
            "narrateur|Les cuillères se cognent, trop fort.",
            "enfant-f|Aniss, on court ?",
            "narrateur|Aniss recule d'un pas, près du pilier.",
            "narrateur|Il serre le peloton contre lui.",
            "narrateur|Le fil fouette, rusé, vers le jardin.",
            "enfant-f|Je veux le fil, dehors.",
            "narrateur|Sarah refuse de courir.",
            "narrateur|Papa s'accroupit, à leur hauteur.",
            "maman|Le fil n'aime pas ce vent.",
            "papa|Un linge sec attend sur la marche.",
            "narrateur|Aniss cache le peloton, sous le linge.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
}

T3_CHOICE = {
    1: [
        "narrateur|Le nœud du linge reste fermé.",
        "narrateur|Sarah retient ses mains.",
        "papa|Le linge, la cuillère, ou le panier ?",
    ],
    2: [
        "narrateur|Le clou reste trop haut.",
        "narrateur|Sarah retient ses talons.",
        "maman|Le tabouret, le clou, ou les mains ?",
    ],
    3: [
        "narrateur|Le vent tient les cuillères.",
        "narrateur|Sarah retient ses pieds.",
        "papa|Le vent, le linge, ou le pilier ?",
    ],
}

T3 = {
    (1, 1, 1): [
        "enfant-f|On attend.",
        "narrateur|Aniss tire le linge, lent.",
        "narrateur|Sarah garde ses mains ouvertes.",
        "narrateur|Le nœud s'ouvre, un peu.",
        "narrateur|La cuillère attend près du nœud.",
        "narrateur|Aniss accroche le fil au bois libre.",
        "narrateur|Le grain de savon rose luit.",
        "enfant-f|Tic.",
        "papa|Le nœud n'est plus un nœud.",
        "maman|Vous avez laissé le temps au linge.",
        "narrateur|Le fil a failli rester coincé.",
        "narrateur|Puis il chante, une fois.",
    ],
    (1, 1, 2): [
        "enfant-f|Pour toi.",
        "narrateur|Sarah tend la cuillère vers Aniss.",
        "narrateur|Aniss lève le torchon avec le métal.",
        "narrateur|Sarah attend, sans répéter ding.",
        "narrateur|Le bois redevient libre.",
        "enfant-f|Il passe !",
        "maman|Le fil a pris le bord.",
        "papa|Le métal a trouvé le linge.",
        "narrateur|Le grain rose glisse, puis tient.",
        "narrateur|Le fil a failli rester sous le linge.",
        "narrateur|Puis un tic net se fait.",
    ],
    (1, 1, 3): [
        "enfant-f|Le panier, Aniss.",
        "narrateur|Aniss pose le fil dedans, sans un mot.",
        "narrateur|Sarah attend, puis suit sa main.",
        "narrateur|La cuillère attend dans le panier.",
        "narrateur|Ils accrochent, après, au bois libre.",
        "enfant-f|Ça tient.",
        "papa|Le panier a tenu le fil.",
        "maman|Le linge peut sécher, plus loin.",
        "narrateur|Le grain rose brille au fond du panier.",
        "narrateur|Le fil a failli rester plié.",
        "narrateur|Puis il se tend, au bois.",
    ],
    (1, 2, 1): [
        "enfant-f|Le tabouret, dessous.",
        "papa|Je vous le tends, à votre hauteur.",
        "narrateur|Aniss monte, Sarah tend le fil.",
        "narrateur|La cuillère monte avec le tabouret.",
        "narrateur|Aniss accroche, lent, sans parler.",
        "enfant-f|Ça tient !",
        "papa|Le bois a tenu le tabouret.",
        "maman|Aniss a poussé, à son rythme.",
        "narrateur|Le grain rose tremble sur le tabouret.",
        "narrateur|Le fil a failli glisser des doigts.",
        "narrateur|Puis le clou le prend.",
    ],
    (1, 2, 2): [
        "enfant-f|On recommence plus bas.",
        "narrateur|Aniss pointe le petit clou, du doigt.",
        "narrateur|Sarah attend, puis suit le doigt.",
        "narrateur|La cuillère trouve le clou plus bas.",
        "narrateur|Le fil glisse, net, sur le fer.",
        "enfant-f|Il glisse.",
        "maman|Le haut garde son ombre, plus loin.",
        "papa|Le bas est plus facile, ici.",
        "narrateur|Le grain rose attrape un rayon, plus bas.",
        "narrateur|Le fil a failli manquer le fer.",
        "narrateur|Puis il s'arrête, accroché.",
    ],
    (1, 2, 3): [
        "enfant-f|Tes mains, Aniss.",
        "narrateur|Sarah tend le fil, tout près.",
        "narrateur|Aniss lève les bras, longs.",
        "narrateur|La cuillère part au bout des mains d'Aniss.",
        "narrateur|Le fil traverse comme un pont.",
        "enfant-f|On tient ensemble.",
        "maman|Vos mains suffisent, toutes les deux.",
        "papa|Le tabouret restera après.",
        "narrateur|Le grain rose voyage au bout des mains.",
        "narrateur|Le fil a failli retomber entre vous.",
        "narrateur|Puis le pont tient.",
    ],
    (1, 3, 1): [
        "enfant-f|On attend le vent.",
        "narrateur|Aniss s'assoit sur la marche, d'abord.",
        "narrateur|Sarah s'assoit aussi, les genoux contre lui.",
        "narrateur|La cuillère attend sur le seuil.",
        "narrateur|Le vent tombe, une feuille s'arrête.",
        "enfant-f|Maintenant.",
        "papa|Le fil ne fouette plus.",
        "maman|Vous avez laissé le vent finir.",
        "narrateur|Le grain rose sèche, sans vent.",
        "narrateur|Le fil a failli s'envoler.",
        "narrateur|Puis il pend, droit.",
    ],
    (1, 3, 2): [
        "enfant-f|Le linge, autour.",
        "narrateur|Sarah tend le linge vers Aniss.",
        "narrateur|Aniss l'enroule, lent, sans un mot.",
        "narrateur|La cuillère se cache un peu dans le linge.",
        "narrateur|Les cuillères ne claquent plus.",
        "enfant-f|C'est doux.",
        "maman|Le vent garde son souffle, plus loin.",
        "papa|Le linge a tenu le métal.",
        "narrateur|Le grain rose se cache dans le linge.",
        "narrateur|Le fil a failli claquer trop fort.",
        "narrateur|Puis un tic étouffé se fait.",
    ],
    (1, 3, 3): [
        "enfant-f|Le pilier, Aniss.",
        "narrateur|Aniss pointe l'ombre, du doigt.",
        "narrateur|Sarah attend, puis suit le doigt.",
        "narrateur|La cuillère suit le pilier, pierre après pierre.",
        "narrateur|Le fil prend le chemin de l'abri.",
        "enfant-f|Il évite le vent.",
        "papa|Le bois a montré la route.",
        "maman|Vos pieds restent au sec, aussi.",
        "narrateur|Le grain rose reste à l'ombre du pilier.",
        "narrateur|Le fil a failli sortir dans le vent.",
        "narrateur|Puis l'abri le tient.",
    ],
    (2, 1, 1): [
        "enfant-f|On attend.",
        "narrateur|Aniss tire le linge, lent.",
        "narrateur|Sarah garde la clochette, muette.",
        "narrateur|Le nœud s'ouvre, un peu.",
        "narrateur|La clochette attend près du nœud.",
        "narrateur|Aniss accroche le fil au bois libre.",
        "narrateur|Le grain rose tinte avec la clochette.",
        "enfant-f|Ding.",
        "papa|Le nœud n'est plus un nœud.",
        "maman|Vous avez laissé le temps au linge.",
        "narrateur|La clochette a failli rester étouffée.",
        "narrateur|Puis elle chante, une fois.",
    ],
    (2, 1, 2): [
        "enfant-f|Pour toi.",
        "narrateur|Sarah tend la cuillère vers Aniss.",
        "narrateur|Aniss lève le torchon avec le métal.",
        "narrateur|La clochette reste dans sa paume.",
        "narrateur|Sarah attend, sans répéter ding.",
        "narrateur|Le bois redevient libre.",
        "enfant-f|Elle peut tinter !",
        "maman|Le fil a pris le bord.",
        "papa|Le métal a trouvé le linge.",
        "narrateur|Le grain rose luit sous la clochette.",
        "narrateur|La clochette a failli rester sous le linge.",
        "narrateur|Puis un ding net se fait.",
    ],
    (2, 1, 3): [
        "enfant-f|Le panier, Aniss.",
        "narrateur|Aniss pose la clochette dedans, sans un mot.",
        "narrateur|Sarah attend, puis suit sa main.",
        "narrateur|La clochette attend dans le panier.",
        "narrateur|Ils accrochent, après, au bois libre.",
        "enfant-f|Ça tient.",
        "papa|Le panier a tenu le métal.",
        "maman|Le linge peut sécher, plus loin.",
        "narrateur|Le grain rose brille près de la clochette.",
        "narrateur|La clochette a failli rester pliée au fond.",
        "narrateur|Puis elle penche, au bois.",
    ],
    (2, 2, 1): [
        "enfant-f|Le tabouret, dessous.",
        "papa|Je vous le tends, à votre hauteur.",
        "narrateur|Aniss monte, Sarah tend la clochette.",
        "narrateur|La clochette monte avec le tabouret.",
        "narrateur|Aniss accroche, lent, sans parler.",
        "enfant-f|Ça tient !",
        "papa|Le bois a tenu le tabouret.",
        "maman|Aniss a poussé, à son rythme.",
        "narrateur|Le grain rose tremble sous la clochette.",
        "narrateur|La clochette a failli choir du tabouret.",
        "narrateur|Puis le clou la prend.",
    ],
    (2, 2, 2): [
        "enfant-f|On recommence plus bas.",
        "narrateur|Aniss pointe le petit clou, du doigt.",
        "narrateur|Sarah attend, puis suit le doigt.",
        "narrateur|La clochette trouve le clou plus bas.",
        "narrateur|Le fil glisse, net, sur le fer.",
        "enfant-f|Il glisse.",
        "maman|Le haut garde son ombre, plus loin.",
        "papa|Le bas est plus facile, ici.",
        "narrateur|Le grain rose attrape un rayon, sous le métal.",
        "narrateur|La clochette a failli manquer le fer.",
        "narrateur|Puis elle s'arrête, accrochée.",
    ],
    (2, 2, 3): [
        "enfant-f|Tes mains, Aniss.",
        "narrateur|Sarah tend la clochette, tout près.",
        "narrateur|Aniss lève les bras, longs.",
        "narrateur|La clochette part au bout des mains d'Aniss.",
        "narrateur|Le fil traverse comme un pont.",
        "enfant-f|On tient ensemble.",
        "maman|Vos mains suffisent, toutes les deux.",
        "papa|Le tabouret restera après.",
        "narrateur|Le grain rose voyage au bout du métal.",
        "narrateur|La clochette a failli retomber entre vous.",
        "narrateur|Puis le pont tinte.",
    ],
    (2, 3, 1): [
        "enfant-f|On attend le vent.",
        "narrateur|Aniss s'assoit sur la marche, d'abord.",
        "narrateur|Sarah s'assoit aussi, les genoux contre lui.",
        "narrateur|La clochette attend sur le seuil.",
        "narrateur|Le vent tombe, une feuille s'arrête.",
        "enfant-f|Maintenant.",
        "papa|Le fil ne fouette plus.",
        "maman|Vous avez laissé le vent finir.",
        "narrateur|Le grain rose sèche sous la clochette.",
        "narrateur|La clochette a failli s'envoler.",
        "narrateur|Puis elle pend, droite.",
    ],
    (2, 3, 2): [
        "enfant-f|Le linge, autour.",
        "narrateur|Sarah tend le linge vers Aniss.",
        "narrateur|Aniss l'enroule, lent, sans un mot.",
        "narrateur|La clochette se cache un peu dans le linge.",
        "narrateur|Les cuillères ne claquent plus.",
        "enfant-f|C'est doux.",
        "maman|Le vent garde son souffle, plus loin.",
        "papa|Le linge a tenu le métal.",
        "narrateur|Le grain rose se cache près de la clochette.",
        "narrateur|La clochette a failli claquer trop fort.",
        "narrateur|Puis un ding étouffé se fait.",
    ],
    (2, 3, 3): [
        "enfant-f|Le pilier, Aniss.",
        "narrateur|Aniss pointe l'ombre, du doigt.",
        "narrateur|Sarah attend, puis suit le doigt.",
        "narrateur|La clochette court le long du pilier.",
        "narrateur|Le fil prend le chemin de l'abri.",
        "enfant-f|Il évite le vent.",
        "papa|Le bois a montré la route.",
        "maman|Vos pieds restent au sec, aussi.",
        "narrateur|Le grain rose reste à l'ombre, sous le métal.",
        "narrateur|La clochette a failli sortir dans le vent.",
        "narrateur|Puis l'abri la tient.",
    ],
    (3, 1, 1): [
        "enfant-f|On attend.",
        "narrateur|Aniss tire le linge, lent.",
        "narrateur|Sarah garde le peloton, ouvert.",
        "narrateur|Le nœud s'ouvre, un peu.",
        "narrateur|La ficelle attend près du nœud.",
        "narrateur|Aniss accroche le fil au bois libre.",
        "narrateur|Le grain rose suit la ficelle, au bois.",
        "enfant-f|Fil.",
        "papa|Le nœud n'est plus un nœud.",
        "maman|Vous avez laissé le temps au linge.",
        "narrateur|La ficelle a failli rester coincée.",
        "narrateur|Puis elle chante, une fois.",
    ],
    (3, 1, 2): [
        "enfant-f|Pour toi.",
        "narrateur|Sarah tend la cuillère vers Aniss.",
        "narrateur|Aniss lève le torchon avec le métal.",
        "narrateur|La ficelle reste autour de son poignet.",
        "narrateur|Sarah attend, sans répéter fil.",
        "narrateur|Le bois redevient libre.",
        "enfant-f|Elle passe !",
        "maman|Le fil a pris le bord.",
        "papa|Le métal a trouvé le linge.",
        "narrateur|Le grain rose luit au bout du fil.",
        "narrateur|La ficelle a failli rester sous le linge.",
        "narrateur|Puis un tic net se fait.",
    ],
    (3, 1, 3): [
        "enfant-f|Le panier, Aniss.",
        "narrateur|Aniss pose le peloton dedans, sans un mot.",
        "narrateur|Sarah attend, puis suit sa main.",
        "narrateur|La ficelle attend dans le panier.",
        "narrateur|Ils accrochent, après, au bois libre.",
        "enfant-f|Ça tient.",
        "papa|Le panier a tenu le fil.",
        "maman|Le linge peut sécher, plus loin.",
        "narrateur|Le grain rose brille au fond, près du fil.",
        "narrateur|La ficelle a failli rester pelotonnée.",
        "narrateur|Puis elle se tend, au bois.",
    ],
    (3, 2, 1): [
        "enfant-f|Le tabouret, dessous.",
        "papa|Je vous le tends, à votre hauteur.",
        "narrateur|Aniss monte, Sarah tend le peloton.",
        "narrateur|La ficelle monte avec le tabouret.",
        "narrateur|Aniss accroche, lent, sans parler.",
        "enfant-f|Ça tient !",
        "papa|Le bois a tenu le tabouret.",
        "maman|Aniss a poussé, à son rythme.",
        "narrateur|Le grain rose tremble au bout du fil.",
        "narrateur|La ficelle a failli glisser du tabouret.",
        "narrateur|Puis le clou la prend.",
    ],
    (3, 2, 2): [
        "enfant-f|On recommence plus bas.",
        "narrateur|Aniss pointe le petit clou, du doigt.",
        "narrateur|Sarah attend, puis suit le doigt.",
        "narrateur|La ficelle trouve le clou plus bas.",
        "narrateur|Le fil glisse, net, sur le fer.",
        "enfant-f|Il glisse.",
        "maman|Le haut garde son ombre, plus loin.",
        "papa|Le bas est plus facile, ici.",
        "narrateur|Le grain rose attrape un rayon, au fil.",
        "narrateur|La ficelle a failli manquer le fer.",
        "narrateur|Puis elle s'arrête, accrochée.",
    ],
    (3, 2, 3): [
        "enfant-f|Tes mains, Aniss.",
        "narrateur|Sarah tend le peloton, tout près.",
        "narrateur|Aniss lève les bras, longs.",
        "narrateur|La ficelle part au bout des mains d'Aniss.",
        "narrateur|Le fil traverse comme un pont.",
        "enfant-f|On tient ensemble.",
        "maman|Vos mains suffisent, toutes les deux.",
        "papa|Le tabouret restera après.",
        "narrateur|Le grain rose voyage au bout du fil.",
        "narrateur|La ficelle a failli retomber entre vous.",
        "narrateur|Puis le pont tient.",
    ],
    (3, 3, 1): [
        "enfant-f|On attend le vent.",
        "narrateur|Aniss s'assoit sur la marche, d'abord.",
        "narrateur|Sarah s'assoit aussi, les genoux contre lui.",
        "narrateur|La ficelle retombe, enfin, contre le bois.",
        "narrateur|Le vent tombe, une feuille s'arrête.",
        "enfant-f|Maintenant.",
        "papa|Le fil ne fouette plus.",
        "maman|Vous avez laissé le vent finir.",
        "narrateur|Le grain rose sèche au bout du fil.",
        "narrateur|La ficelle a failli s'envoler.",
        "narrateur|Puis elle pend, droite.",
    ],
    (3, 3, 2): [
        "enfant-f|Le linge, autour.",
        "narrateur|Sarah tend le linge vers Aniss.",
        "narrateur|Aniss l'enroule, lent, sans un mot.",
        "narrateur|La ficelle se cache un peu dans le linge.",
        "narrateur|Les cuillères ne claquent plus.",
        "enfant-f|C'est doux.",
        "maman|Le vent garde son souffle, plus loin.",
        "papa|Le linge a tenu le fil.",
        "narrateur|Le grain rose se cache au bout du fil.",
        "narrateur|La ficelle a failli claquer trop fort.",
        "narrateur|Puis un tic étouffé se fait.",
    ],
    (3, 3, 3): [
        "enfant-f|Le pilier, Aniss.",
        "narrateur|Aniss pointe l'ombre, du doigt.",
        "narrateur|Sarah attend, puis suit le doigt.",
        "narrateur|La ficelle tient derrière le pilier, droite.",
        "narrateur|Le fil prend le chemin de l'abri.",
        "enfant-f|Il évite le vent.",
        "papa|Le bois a montré la route.",
        "maman|Vos pieds restent au sec, aussi.",
        "narrateur|Le grain rose reste à l'ombre, au fil.",
        "narrateur|La ficelle a failli sortir dans le vent.",
        "narrateur|Puis l'abri la tient.",
    ],
}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Le fil chante une fois, un petit tic.",
        "enfant-m|Tic.",
        "enfant-f|Il est accroché.",
        "papa|Le linge a laissé le bois.",
        "maman|La soupe est prête, dans la cuisine.",
        "narrateur|Aniss pose une main sur le fil.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Une miette de pain attend sur la table.",
    ],
    (1, 1, 2): [
        "narrateur|Le fil a contourné le linge, jusqu'au bout.",
        "enfant-f|Aniss l'a levé, tout seul.",
        "papa|Tu as tendu, d'abord.",
        "maman|Venez, le pain est chaud.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss s'assoit près du panier.",
        "enfant-m|Ding.",
        "narrateur|Le torchon sèche, tordu, au vent.",
    ],
    (1, 1, 3): [
        "narrateur|Le fil court jusqu'au bois, tout droit.",
        "enfant-f|On a posé le panier.",
        "papa|Le fil a repris sa place.",
        "maman|Lavez-vous les mains, lent.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss tapote une cuillère, léger.",
        "narrateur|Le métal a un peu de poussière.",
        "narrateur|La soupe fume derrière la porte.",
    ],
    (1, 2, 1): [
        "narrateur|Le fil glisse sur le clou, puis tinte.",
        "enfant-f|Le tabouret était juste assez.",
        "papa|Le haut n'a plus pris vos bras.",
        "maman|Rentrez le tabouret, après le chant.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "enfant-m|Tic.",
        "narrateur|Une marche se tait, puis l'autre.",
        "narrateur|Le tabouret garde une ombre ronde.",
    ],
    (1, 2, 2): [
        "narrateur|Le petit clou tient le fil, net.",
        "enfant-f|On tenait, tous les deux.",
        "papa|Je remporte le tabouret, tout à l'heure.",
        "maman|Le pain vous attend.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss essuie une main sur son pantalon.",
        "narrateur|Le fil sent le vent chaud.",
        "narrateur|Un grain de savon reste sur le bois.",
    ],
    (1, 2, 3): [
        "narrateur|Les mains d'Aniss laissent le fil chanter.",
        "enfant-f|C'était plus facile, là.",
        "papa|Tes bras ont guidé le fil.",
        "maman|Le haut gardera son ombre.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss pose un doigt sur une cuillère.",
        "narrateur|Elle bouge, minuscule.",
        "narrateur|Un rai de soleil barre le bois.",
    ],
    (1, 3, 1): [
        "narrateur|Le fil chante, maintenant que le vent s'est tu.",
        "enfant-f|On a attendu, Aniss.",
        "papa|Le métal n'a pas volé.",
        "maman|Rentrez, le seuil est sec.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss pose une feuille sur la marche.",
        "narrateur|La feuille ne bouge plus.",
        "narrateur|Une feuille ne bouge plus, sur la marche.",
    ],
    (1, 3, 2): [
        "narrateur|Le linge, tout près, laisse le fil tinter.",
        "enfant-f|On l'a enroulé, tous les deux.",
        "papa|Le vent est resté à sa place.",
        "maman|Essuie tes chaussures, Sarah.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss souffle un peu sur le métal.",
        "narrateur|Le savon blanchit, puis s'arrête.",
        "narrateur|Le pain grillé sent, derrière la porte.",
    ],
    (1, 3, 3): [
        "narrateur|Le fil suit le pilier, jusqu'à l'abri.",
        "enfant-f|L'ombre était douce.",
        "papa|Le bois a tenu, tout droit.",
        "maman|Le vent n'a plus rien à dire.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss touche le fil, un instant.",
        "narrateur|Une cuillère revient contre le bois.",
        "narrateur|Une abeille passe, puis le jardin se tait.",
    ],
    (2, 1, 1): [
        "narrateur|La clochette chante une fois, un petit ding.",
        "enfant-m|Ding.",
        "enfant-f|Elle est accrochée.",
        "papa|Le linge a laissé le bois.",
        "maman|La soupe est prête, dans la cuisine.",
        "narrateur|Aniss pose une main sur le métal.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Le creux garde un rond rose, minuscule.",
    ],
    (2, 1, 2): [
        "narrateur|La clochette a contourné le linge, jusqu'au bout.",
        "enfant-f|Aniss l'a levée, tout seul.",
        "papa|Tu as tendu, d'abord.",
        "maman|Venez, le pain est chaud.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss s'assoit près du panier.",
        "enfant-m|Tic.",
        "narrateur|La clochette penche, puis se tait.",
    ],
    (2, 1, 3): [
        "narrateur|La clochette court jusqu'au bois, tout droit.",
        "enfant-f|On a posé le panier.",
        "papa|Le métal a repris sa place.",
        "maman|Lavez-vous les mains, lent.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss tapote la clochette, léger.",
        "narrateur|Le métal a un peu de poussière.",
        "narrateur|Le panier dort près du seuil.",
    ],
    (2, 2, 1): [
        "narrateur|La clochette glisse sur le clou, puis tinte.",
        "enfant-f|Le tabouret était juste assez.",
        "papa|Le haut n'a plus pris vos bras.",
        "maman|Rentrez le tabouret, après le chant.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "enfant-m|Ding.",
        "narrateur|Une marche se tait, puis l'autre.",
        "narrateur|La véranda reprend son ombre tiède.",
    ],
    (2, 2, 2): [
        "narrateur|Le petit clou tient la clochette, net.",
        "enfant-f|On tenait, tous les deux.",
        "papa|Je remporte le tabouret, tout à l'heure.",
        "maman|Le pain vous attend.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss essuie une main sur son pantalon.",
        "narrateur|Le fil sent le vent chaud.",
        "narrateur|Un oiseau se tait, sur le toit.",
    ],
    (2, 2, 3): [
        "narrateur|Les mains d'Aniss laissent la clochette chanter.",
        "enfant-f|C'était plus facile, là.",
        "papa|Tes bras ont guidé le métal.",
        "maman|Le haut gardera son ombre.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss pose un doigt sur la clochette.",
        "narrateur|Elle bouge, minuscule.",
        "narrateur|Le clou plus bas tient tout seul.",
    ],
    (2, 3, 1): [
        "narrateur|La clochette chante, maintenant que le vent s'est tu.",
        "enfant-f|On a attendu, Aniss.",
        "papa|Le métal n'a pas volé.",
        "maman|Rentrez, le seuil est sec.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss pose une feuille sur la marche.",
        "narrateur|La feuille ne bouge plus.",
        "narrateur|La marche garde une trace de pied.",
    ],
    (2, 3, 2): [
        "narrateur|Le linge, tout près, laisse la clochette tinter.",
        "enfant-f|On l'a enroulée, tous les deux.",
        "papa|Le vent est resté à sa place.",
        "maman|Essuie tes chaussures, Sarah.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss souffle un peu sur le métal.",
        "narrateur|Le savon blanchit, puis s'arrête.",
        "narrateur|Le linge sec sent le soleil.",
    ],
    (2, 3, 3): [
        "narrateur|La clochette suit le pilier, jusqu'à l'abri.",
        "enfant-f|L'ombre était douce.",
        "papa|Le bois a tenu, tout droit.",
        "maman|Le vent n'a plus rien à dire.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss touche le métal, un instant.",
        "narrateur|Une clochette revient contre le bois.",
        "narrateur|Le pilier reste frais, du côté du jardin.",
    ],
    (3, 1, 1): [
        "narrateur|La ficelle chante une fois, un petit tic.",
        "enfant-m|Tic.",
        "enfant-f|Elle est accrochée.",
        "papa|Le linge a laissé le bois.",
        "maman|La soupe est prête, dans la cuisine.",
        "narrateur|Aniss pose une main sur le fil.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|La ficelle reste contre le bois, droite.",
    ],
    (3, 1, 2): [
        "narrateur|La ficelle a contourné le linge, jusqu'au bout.",
        "enfant-f|Aniss l'a levée, tout seul.",
        "papa|Tu as tendu, d'abord.",
        "maman|Venez, le pain est chaud.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss s'assoit près du panier.",
        "enfant-m|Fil.",
        "narrateur|Un fil d'eau sèche sur le métal.",
    ],
    (3, 1, 3): [
        "narrateur|La ficelle court jusqu'au bois, tout droit.",
        "enfant-f|On a posé le panier.",
        "papa|Le fil a repris sa place.",
        "maman|Lavez-vous les mains, lent.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss tapote le peloton, léger.",
        "narrateur|Le fil a un peu de poussière.",
        "narrateur|Le nœud du linge dort, ouvert.",
    ],
    (3, 2, 1): [
        "narrateur|La ficelle glisse sur le clou, puis tinte.",
        "enfant-f|Le tabouret était juste assez.",
        "papa|Le haut n'a plus pris vos bras.",
        "maman|Rentrez le tabouret, après le chant.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "enfant-m|Tic.",
        "narrateur|Une marche se tait, puis l'autre.",
        "narrateur|Une goutte de soupe perle au bord.",
    ],
    (3, 2, 2): [
        "narrateur|Le petit clou tient la ficelle, net.",
        "enfant-f|On tenait, tous les deux.",
        "papa|Je remporte le tabouret, tout à l'heure.",
        "maman|Le pain vous attend.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss essuie une main sur son pantalon.",
        "narrateur|Le fil sent le vent chaud.",
        "narrateur|Le verre de la cuisine tinte, loin.",
    ],
    (3, 2, 3): [
        "narrateur|Les mains d'Aniss laissent la ficelle chanter.",
        "enfant-f|C'était plus facile, là.",
        "papa|Tes bras ont guidé le fil.",
        "maman|Le haut gardera son ombre.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss pose un doigt sur le peloton.",
        "narrateur|Il bouge, minuscule.",
        "narrateur|Le rideau retombe, sans vent.",
    ],
    (3, 3, 1): [
        "narrateur|La ficelle chante, maintenant que le vent s'est tu.",
        "enfant-f|On a attendu, Aniss.",
        "papa|Le fil n'a pas volé.",
        "maman|Rentrez, le seuil est sec.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss pose une feuille sur la marche.",
        "narrateur|La feuille ne bouge plus.",
        "narrateur|Aniss laisse le métal, sans mot.",
    ],
    (3, 3, 2): [
        "narrateur|Le linge, tout près, laisse la ficelle tinter.",
        "enfant-f|On l'a enroulée, tous les deux.",
        "papa|Le vent est resté à sa place.",
        "maman|Essuie tes chaussures, Sarah.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss souffle un peu sur le fil.",
        "narrateur|Le savon blanchit, puis s'arrête.",
        "narrateur|Une fourmi traverse la marche.",
    ],
    (3, 3, 3): [
        "narrateur|La ficelle suit le pilier, jusqu'à l'abri.",
        "enfant-f|L'ombre était douce.",
        "papa|Le bois a tenu, tout droit.",
        "maman|Le vent n'a plus rien à dire.",
        "narrateur|Un peu de savon rose brille dans le creux.",
        "narrateur|Aniss touche le fil, un instant.",
        "narrateur|Une ficelle revient contre le bois.",
        "narrateur|Le grain rose a quitté le creux.",
    ],
}

T3_SONS = {
    (1, 1): "linge,tic",
    (1, 2): "metal,linge",
    (1, 3): "panier,bois",
    (2, 1): "tabouret,bois",
    (2, 2): "clou,fil",
    (2, 3): "mains,fil",
    (3, 1): "vent,feuille",
    (3, 2): "linge,vent",
    (3, 3): "pierre,abri",
}

END_SONS = {
    1: "soupe,couverts",
    2: "clochette,soupe",
    3: "ficelle,soupe",
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "soupe,rideau",
        {"emphasis": "grain de savon rose"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("la cuillère", "la clochette", "la ficelle"), "pause_before": 200},
    )

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        t1 = T1[a]
        out_chunks[base] = voice(
            by_src[base], t1["passage"], "action", t1["sons"],
            {"emphasis": t1["emphasis"]},
        )
        out_chunks[f"{base}_Q0001"] = voice(
            by_src[f"{base}_Q0001"], t1["question"], "clue", "",
            {"fields": t1["qfields"], "emphasis": t1["emphasis"]},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], t1["confirm"], "confirm", t1["sons"],
            {"emphasis": "grain de savon rose"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("l'étendoir", "la poutre", "la marche"), "pause_before": 200},
        )
        for b in (1, 2, 3):
            bse = f"{base}_T0002_P000{b}"
            t2 = T2[(a, b)]
            out_chunks[bse] = voice(
                by_src[bse], t2["passage"], "obstacle", t2["sons"],
                {"emphasis": t2["emphasis"]},
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab(*T3_LABS[b]), "pause_before": 200},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], T3[(a, b, c)], "resolution", T3_SONS[(b, c)],
                    {"emphasis": "grain de savon rose"},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ENDINGS[(a, b, c)], "ending", END_SONS[a],
                    {"emphasis": "grain de savon rose"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = set(out_chunks) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:6]} extra={sorted(extra)[:6]}")

    story = dict(src)
    story["fil_rouge"] = FIL
    story["title"] = TITLE
    story["characters"] = CHARS
    story["setting"] = SETTING
    story["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]

    check(SID, story["age_band"], story["chunks"])

    blob = "\n".join(c["script"] for c in story["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in story["chunks"]
    ).lower()
    whole = blob + "\n" + labels
    for bad in (
        "on va apprendre",
        "voici le geste",
        "l'histoire est finie",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "sara ",
        "hugo",
        "parle peu",
        "camarade",
        "timide",
        "forcer la parole",
        "il faut attendre",
        "un camarade",
        "parc",
        "toboggan",
        "balançoire",
        "capitaine",
        "mission accomplie",
        "j'ai compris",
        "aujourd'hui",
        "tout doux",
        "tout calme",
        "tout lent",
        "merle",
        "miel",
        "grand-père",
        "maîtresse",
        "jardinier",
        "zoé",
        "sami",
        "lina",
        "iris",
        "léa",
        "tom ",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "aniss" not in blob:
        raise SystemExit(f"{SID}: Aniss absent")
    if "grain de savon rose" not in blob:
        raise SystemExit(f"{SID}: indice grain de savon rose manquant")

    fins = [c["text"] for c in story["chunks"] if c["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes {len(set(fins))}/27")
    lasts = []
    for c in story["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        last_n = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(last_n[-1])
        low = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in low or "bravo" in low or "bon travail" in low:
            raise SystemExit(f"fin mécanique: {last_n[-1]}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images {len(set(lasts))}/27")

    t3s = [c["text"] for c in story["chunks"] if re.search(r"T0003_P000[123]$", c["chunk_id"])]
    if len(t3s) != 27 or len(set(t3s)) != 27:
        raise SystemExit(f"T3 distincts {len(set(t3s))}/27")

    t2s = [c["text"] for c in story["chunks"] if re.search(r"T0002_P000[123]$", c["chunk_id"])]
    if len(t2s) != 9 or len(set(t2s)) != 9:
        raise SystemExit(f"T2 distincts {len(set(t2s))}/9")

    counts = [path_words(out_chunks, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-027 — Les cuillères de Sarah sous la véranda\n\n"
        "- **Public :** N1 (3–4 ans), audio familial\n"
        "- **Leçon :** DIF.PAR.001 — attendre, tendre, ne pas forcer la parole (vécue)\n"
        "- **Personnages :** Sarah, Aniss, papa, maman\n"
        "- **Lieu :** cuisine, véranda, étendoir, poutre, marche du jardin\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Sarah connaît la cuisine. Un détail paraît neuf : un **grain de savon rose** "
        "dans le creux d'une cuillère. Elle veut accrocher ses cuillères sous la véranda "
        "pour qu'elles sonnent **avant le vent du soir**. Aniss arrive. Elle veut un ding "
        "tout de suite ; lui répond avec le doigt. Première idée ratée. "
        "Cuillère, clochette ou ficelle : les trois partent. "
        "Étendoir (nœud rusé), poutre (fil qui glisse) ou marche (vent et limite d'Aniss). "
        "Sarah refuse de foncer. Papa ou maman s'accroupit. "
        "Neuf façons : attendre le linge, tendre la cuillère, poser le panier ; "
        "tabouret, clou plus bas, mains d'Aniss ; vent, linge, pilier. "
        "Le grain rose luit. On rentre à la soupe.\n\n"
        "## Vécu\n\n"
        "Sarah veut le ding **maintenant**. Aniss touche, recule, ou couvre le métal. "
        "Le silence compte. Chaque choix change l'obstacle et le climax. "
        "La leçon se voit : elle tend, elle attend, elle suit le doigt. "
        "Fin : le fil chante + le grain rose + une image unique du chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Gabarit Sara / parc / slogan PAR / « on va apprendre » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Ouverture v2 : lieu connu, détail neuf (grain rose), pas « Aujourd'hui, je mène ». "
        "Corps : sourire parti, poitrine bousculée, adulte accroupi. "
        "2e ruse plus rusée ; Sarah refuse de foncer. Dénouement qui a failli.\n"
        "- T1 ne retire pas l'équipement. 9 T2 distincts, 27 T3, 27 fins, 27 dernières images.\n"
        "- Merci vécu (papa : tu as vu son doigt). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        "- N1 ≤ 10. `check()` OK. Pas apply.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks, 27 chemins, 27 fins distinctes, 27 dernières images\n"
        f"- {min(counts)} à {max(counts)} mots par chemin (moyenne {sum(counts)//len(counts)})\n"
        "- `text` = `script` collé ; graphe inchangé\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur des 27 chemins.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
