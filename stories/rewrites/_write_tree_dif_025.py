#!/usr/bin/env python3
"""TREE-DIF-025 — Le défilé de Nina et les deux chapeaux (N2, DIF.COR.002, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-025"
N2 = 15
TITLE = "Le défilé de Nina et les deux chapeaux"
FIL = (
    "Au hall, un grain de feutre gris tient sur le béret. "
    "Nina veut un vrai défilé pour l'ours et la girafe, maintenant, "
    "avant que papa range les chapeaux. Elle force toute seule : les chapeaux glissent. "
    "Elle prend le tambour, le ruban ou le panier ; les trois partent. "
    "Le couloir glisse, le jardin souffle, l'escalier serre. "
    "Elle refuse de foncer, retrouve le grain, demande. "
    "Neuf façons d'attendre l'aide. Les deux chapeaux restent."
)
CHARS = "Nina, papa, maman"
SETTING = "hall de la maison, couloir, jardin, escalier"
TIC_PHRASES = (
    "tout doux",
    "tout calme",
    "tout lent",
    "miel",
    "merle",
    "aujourd'hui,",
    "j'ai compris",
    "mission accomplie",
    "on va apprendre",
    "bon travail",
    "il faut attendre",
    "il faut demander",
    "on doit demander",
    "papa sourit",
    "maman sourit",
    "plus rond ou plus mince",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain de feutre",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=nina_veut_le_defile_maintenant_le_grain_tient; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_maniere_de_demander; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_prend; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=élan_retenu; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent_avec_elle; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=elle_force_toute_seule_les_chapeaux_glissent; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_découragement; intensite=2; destinataire=enfant; sous_texte=l_objet_resiste_elle_veut_foncer; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "grain de feutre",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=le_grain_et_la_demande_sans_forcer_seule; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain de feutre",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_grain_paie_le_debut_les_chapeaux_restent; tempo=posé; sourire=léger; respiration=ample",
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


def vet(lines: list[str], where: str = "") -> list[str]:
    out = []
    prev = ""
    run = 1
    for raw in lines:
        role, ph = raw.split("|", 1)
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{where} {n}>{N2}: {ph}")
        if n == 0:
            raise SystemExit(f"{where} vide: {raw}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"{where} ponctuation {marks}: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"{where} fin: {ph}")
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"{where} tic {tic!r}: {ph}")
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"{where} tic {m.group(0)!r}: {ph}")
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
        out.append(f"{role}|{ph}")
    return out


def voice(src: dict, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    lines = vet(lines, src.get("chunk_id", "?"))
    m = dict(PROFILES[profile])
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


def t3lab(a: str, b: str, c: str) -> dict:
    return {"option_1_label": a, "option_2_label": b, "option_3_label": c}


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


OPENING = [
    "narrateur|Le hall sent les manteaux, un peu humides.",
    "narrateur|Nina connaît cette patère jaune, presque par cœur.",
    "narrateur|Un détail paraît nouveau, près du béret.",
    "narrateur|Un grain de feutre gris tient sur la laine.",
    "maman|Tu as vu ce grain, Nina ?",
    "enfant-f|Il n'était pas là.",
    "papa|Il vient du béret, je crois.",
    "narrateur|L'ours attend sur la commode, ventre chaud.",
    "narrateur|La girafe dépasse, trop haute, une oreille pliée.",
    "narrateur|En ce moment, Nina veut les deux chapeaux.",
    "enfant-f|Un vrai défilé, maintenant.",
    "papa|Je range dans une minute.",
    "enfant-f|Non, le défilé, avant.",
    "maman|Le tambour, le ruban, et le panier.",
    "papa|Merci, tu as posé le cône.",
    "narrateur|Le bois de la commode sent le savon.",
    "narrateur|Sous la patère, un chausson attend.",
    "enfant-f|Ils vont marcher, tous les deux.",
]

T1_CHOICE = [
    "narrateur|Près des chaussons, trois affaires attendent.",
    "narrateur|Le tambour, le ruban, et le panier.",
    "maman|Tu prends quoi d'abord, Nina ?",
]

T1 = {
    1: {
        "lab": "le tambour",
        "sons": "casserole,toc",
        "emphasis": "tambour",
        "passage": [
            "narrateur|Nina prend d'abord le tambour, un peu tiède.",
            "enfant-f|Ça va faire la musique.",
            "maman|Doucement, c'est une casserole.",
            "narrateur|La cuillère donne un toc, trop court.",
            "narrateur|Elle enfonce le béret, trop vite, toute seule.",
            "narrateur|Le grain de feutre tombe, puis s'arrête.",
            "enfant-f|Il glisse !",
            "papa|Le ruban aussi, près du sac.",
            "narrateur|Maman glisse le panier contre le mur.",
            "narrateur|Tambour, ruban et panier avancent avec elle.",
            "enfant-f|L'ours, le béret.",
            "narrateur|Elle enfonce la laine, un peu trop large.",
            "enfant-f|La girafe, le cône.",
            "narrateur|Le papier penche vers l'oreille, trop mince.",
            "papa|Le tambour est à toi, là.",
        ],
        "question": [
            "narrateur|Nina a pris le tambour d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "tambour",
            "accepted_examples": "tambour | le tambour | d'abord le tambour | la casserole",
            "retry_prompt": "Nina prend le tambour d'abord.",
        },
        "confirm": [
            "narrateur|Le tambour tient contre sa hanche.",
            "enfant-f|Les deux chapeaux vont marcher.",
            "maman|Le hall vous attend.",
            "papa|Tu tiens bien, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un toc court, dans le métal.",
            "papa|On avance, sans courir.",
            "narrateur|Le ruban et le panier sont avec toi.",
            "maman|Les deux chapeaux restent, avec vous.",
        ],
        "voy": "Le tambour cliquette à chaque pas.",
    },
    2: {
        "lab": "le ruban",
        "sons": "soie,tiroir",
        "emphasis": "ruban",
        "passage": [
            "narrateur|Nina déroule d'abord le ruban, trop long.",
            "enfant-f|Il va tenir les chapeaux.",
            "papa|Pas trop serré, Nina.",
            "narrateur|La soie sent le tiroir, un peu sec.",
            "narrateur|Elle noue le cône, trop vite, toute seule.",
            "narrateur|Le grain de feutre tombe, trop loin.",
            "enfant-f|Il part !",
            "maman|Le tambour, ensuite, près du sac.",
            "narrateur|Papa pose le panier contre les chaussons.",
            "narrateur|Nina serre les trois contre elle.",
            "enfant-f|Le béret sur l'ours.",
            "narrateur|La laine mange un peu ses oreilles.",
            "enfant-f|Le cône sur la girafe.",
            "narrateur|Le papier tremble, trop mince, trop léger.",
            "maman|Le ruban est prêt, tu peux y aller.",
        ],
        "question": [
            "narrateur|Nina a pris le ruban d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "ruban",
            "accepted_examples": "ruban | le ruban | d'abord le ruban | le lien",
            "retry_prompt": "Nina prend le ruban d'abord.",
        },
        "confirm": [
            "narrateur|Le ruban fait un nœud lâche, au poignet.",
            "enfant-f|Il va garder les chapeaux.",
            "papa|La soie brille un peu.",
            "maman|Tes pieds, dans les chaussons ?",
            "enfant-f|Oui, maman.",
            "narrateur|Les deux doudous se touchent, trop près.",
            "maman|On avance, sans se presser.",
            "narrateur|Le tambour et le panier sont avec toi.",
            "papa|Le nœud reste lâche, c'est mieux.",
        ],
        "voy": "Le ruban frotte le poignet, trop soyeux.",
    },
    3: {
        "lab": "le panier",
        "sons": "osier,laine",
        "emphasis": "panier",
        "passage": [
            "narrateur|Nina tire d'abord le panier, l'osier rêche.",
            "enfant-f|Ils voyageront là-dedans.",
            "maman|Tiens-le droit, Nina.",
            "narrateur|Un brin pique un doigt, puis plus.",
            "narrateur|Elle y met les deux, trop vite, toute seule.",
            "narrateur|Le grain de feutre tombe hors de l'osier.",
            "enfant-f|Il est tombé !",
            "papa|Tambour et ruban, avec vous.",
            "narrateur|Il les glisse près des chaussons.",
            "narrateur|Le hall reste vide, derrière eux.",
            "enfant-f|L'ours dans le panier.",
            "narrateur|Le béret dépasse, trop rond, trop large.",
            "enfant-f|La girafe aussi.",
            "narrateur|Le cône dépasse de l'autre bord, trop mince.",
            "papa|Le panier est prêt, on avance.",
        ],
        "question": [
            "narrateur|Nina a pris le panier d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "panier",
            "accepted_examples": "panier | le panier | d'abord le panier | le panier d'abord",
            "retry_prompt": "Nina prend le panier d'abord.",
        },
        "confirm": [
            "narrateur|Le panier penche, deux têtes dehors.",
            "enfant-f|On défile avec eux.",
            "maman|L'osier sent le grenier, un peu.",
            "papa|On y va, tous les trois ?",
            "enfant-f|Oui.",
            "narrateur|Le béret et le cône ne se ressemblent pas.",
            "papa|On marche, sans se presser.",
            "narrateur|Le tambour et le ruban sont avec toi.",
            "maman|Deux têtes regardent, trop différentes.",
        ],
        "voy": "Le panier tape le genou, un peu.",
    },
}

T2 = {
    (1, 1): {
        "sons": "carrelage,savon",
        "emphasis": "couloir",
        "passage": [
            "narrateur|Contre sa hanche, le tambour tape un toc.",
            "narrateur|Le couloir sent le savon, trop lisse.",
            "narrateur|Nina pousse l'ours, trop vite, toute seule.",
            "narrateur|Le béret glisse, le cône part de travers.",
            "enfant-f|Ils n'avancent pas !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Le carrelage est trop lisse.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de feutre glisse, puis s'arrête.",
            "enfant-f|Pas toute seule.",
            "narrateur|Elle écoute le couloir, trop savonné.",
            "narrateur|Elle regarde le grain de feutre, gris.",
            "maman|Tu vois comment, Nina ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (1, 2): {
        "sons": "vent,herbe",
        "emphasis": "jardin",
        "passage": [
            "narrateur|Contre sa hanche, le tambour tape un toc.",
            "narrateur|Le jardin sent l'herbe coupée, trop vive.",
            "narrateur|Nina lève le cône, trop vite, toute seule.",
            "narrateur|Le vent prend le papier, trop léger.",
            "enfant-f|Elle n'a plus son chapeau !",
            "narrateur|Nina sent son corps se crisper, trop.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Le vent a trop choisi.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de feutre reste, lui, sur le béret.",
            "enfant-f|Pas toute seule.",
            "narrateur|Elle écoute le jardin, trop soufflé.",
            "narrateur|Elle regarde le grain de feutre, gris.",
            "maman|Tu vois comment, Nina ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (1, 3): {
        "sons": "bois,marches",
        "emphasis": "escalier",
        "passage": [
            "narrateur|Contre sa hanche, le tambour tape un toc.",
            "narrateur|L'escalier sent le bois ciré, trop étroit.",
            "narrateur|Nina monte les deux, trop vite, toute seule.",
            "narrateur|L'ours bute, le cône tape le plafond.",
            "enfant-f|Ils ne passent pas !",
            "narrateur|Cette fois, Nina ne rit plus.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Les marches n'ont pas leur largeur.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de feutre s'accroche, trop bas.",
            "enfant-f|Pas toute seule.",
            "narrateur|Elle écoute l'escalier, trop haut.",
            "narrateur|Elle regarde le grain de feutre, gris.",
            "maman|Tu vois comment, Nina ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (2, 1): {
        "sons": "carrelage,soie",
        "emphasis": "couloir",
        "passage": [
            "narrateur|Sa paume sent le ruban, trop soyeux.",
            "narrateur|Le couloir sent le savon, trop lisse.",
            "narrateur|Nina tire le ruban, trop vite, toute seule.",
            "narrateur|Contre le mur, la soie glisse, trop lisse.",
            "enfant-f|Ils n'avancent pas !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Le carrelage est trop lisse.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de feutre glisse sous la soie.",
            "enfant-f|Pas toute seule.",
            "narrateur|Elle écoute le couloir, trop savonné.",
            "narrateur|Elle regarde le grain de feutre, gris.",
            "maman|Tu vois comment, Nina ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (2, 2): {
        "sons": "vent,soie",
        "emphasis": "jardin",
        "passage": [
            "narrateur|Sa paume sent le ruban, trop soyeux.",
            "narrateur|Le jardin sent l'herbe coupée, trop vive.",
            "narrateur|Nina lève le ruban, trop vite, toute seule.",
            "narrateur|Comme un drapeau, le ruban claque.",
            "enfant-f|Elle n'a plus son chapeau !",
            "narrateur|Nina sent son corps se crisper, trop.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Le vent a trop choisi.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de feutre reste, lui, dans la soie.",
            "enfant-f|Pas toute seule.",
            "narrateur|Elle écoute le jardin, trop soufflé.",
            "narrateur|Elle regarde le grain de feutre, gris.",
            "maman|Tu vois comment, Nina ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (2, 3): {
        "sons": "bois,soie",
        "emphasis": "escalier",
        "passage": [
            "narrateur|Sa paume sent le ruban, trop soyeux.",
            "narrateur|L'escalier sent le bois ciré, trop étroit.",
            "narrateur|Nina tire les deux, trop vite, toute seule.",
            "narrateur|À la rampe, le ruban s'accroche, puis lâche.",
            "enfant-f|Ils ne passent pas !",
            "narrateur|Cette fois, Nina ne rit plus.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Les marches n'ont pas leur largeur.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de feutre s'accroche au bois.",
            "enfant-f|Pas toute seule.",
            "narrateur|Elle écoute l'escalier, trop haut.",
            "narrateur|Elle regarde le grain de feutre, gris.",
            "maman|Tu vois comment, Nina ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (3, 1): {
        "sons": "carrelage,osier",
        "emphasis": "couloir",
        "passage": [
            "narrateur|Contre le genou, l'osier du panier penche.",
            "narrateur|Le couloir sent le savon, trop lisse.",
            "narrateur|Nina pousse le panier, trop vite, toute seule.",
            "narrateur|Sur les carreaux, le panier part tout seul.",
            "enfant-f|Ils n'avancent pas !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Le carrelage est trop lisse.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de feutre roule hors de l'osier.",
            "enfant-f|Pas toute seule.",
            "narrateur|Elle écoute le couloir, trop savonné.",
            "narrateur|Elle regarde le grain de feutre, gris.",
            "maman|Tu vois comment, Nina ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (3, 2): {
        "sons": "vent,osier",
        "emphasis": "jardin",
        "passage": [
            "narrateur|Contre le genou, l'osier du panier penche.",
            "narrateur|Le jardin sent l'herbe coupée, trop vive.",
            "narrateur|Nina lève le panier, trop vite, toute seule.",
            "narrateur|Le vent prend le papier, le panier penche.",
            "enfant-f|Elle n'a plus son chapeau !",
            "narrateur|Nina sent son corps se crisper, trop.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Le vent a trop choisi.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de feutre reste, lui, dans l'osier.",
            "enfant-f|Pas toute seule.",
            "narrateur|Elle écoute le jardin, trop soufflé.",
            "narrateur|Elle regarde le grain de feutre, gris.",
            "maman|Tu vois comment, Nina ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
    (3, 3): {
        "sons": "bois,osier",
        "emphasis": "escalier",
        "passage": [
            "narrateur|Contre le genou, l'osier du panier penche.",
            "narrateur|L'escalier sent le bois ciré, trop étroit.",
            "narrateur|Nina hisse le panier, trop vite, toute seule.",
            "narrateur|Trop large pour la marche, le panier bute.",
            "enfant-f|Ils ne passent pas !",
            "narrateur|Cette fois, Nina ne rit plus.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Les marches n'ont pas leur largeur.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un grain de feutre s'accroche à l'osier.",
            "enfant-f|Pas toute seule.",
            "narrateur|Elle écoute l'escalier, trop haut.",
            "narrateur|Elle regarde le grain de feutre, gris.",
            "maman|Tu vois comment, Nina ?",
            "enfant-f|Alors on fait quoi ?",
        ],
    },
}

T3_LABS = {
    1: ("les chaussettes", "le tapis", "les petits pas"),
    2: ("le nœud", "le mur", "le panier-tête"),
    3: ("la même marche", "descendre", "la rampe"),
}

T3_CHOICE = {
    1: [
        "narrateur|Le couloir n'a pas fini d'être lisse.",
        "papa|Les chaussettes, le tapis, ou les petits pas ?",
    ],
    2: [
        "narrateur|Le jardin n'a pas fini de souffler.",
        "maman|Le nœud, le mur, ou le panier-tête ?",
    ],
    3: [
        "narrateur|L'escalier n'a pas fini d'être étroit.",
        "papa|La même marche, descendre, ou la rampe ?",
    ],
}

T3_SONS = {
    (1, 1): "laine,chaussettes",
    (1, 2): "tapis,laine",
    (1, 3): "pas,carrelage",
    (2, 1): "nœud,vent",
    (2, 2): "mur,pierre",
    (2, 3): "panier,osier",
    (3, 1): "marche,bois",
    (3, 2): "descente,hall",
    (3, 3): "rampe,bois",
}

T3_EMPH = {
    1: {1: "chaussettes", 2: "tapis", 3: "petits pas"},
    2: {1: "nœud", 2: "mur", 3: "panier"},
    3: {1: "marche", 2: "descendre", 3: "rampe"},
}

T3 = {
    (1, 1, 1): [
        "enfant-f|Des chaussettes, aux pattes.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Maman, tu m'aides à les mettre ?",
        "maman|Oui, une patte, puis l'autre.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il montre une dalle sèche, plus loin.",
        "papa|On pose le tambour, le temps des chaussettes.",
        "narrateur|L'ours a deux chaussons de laine, trop grands.",
        "enfant-f|Vous glissez moins.",
        "papa|Chacun a sa laine, maintenant.",
        "maman|Tes mains ont demandé la laine.",
        "narrateur|Le grain de feutre reste sur la chaussette.",
    ],
    (1, 1, 2): [
        "enfant-f|Le tapis, comme une route.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu tires le tapis ?",
        "papa|Oui, je le tire, tu guides.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il s'arrête sur la laine, plus rêche.",
        "maman|Au bord du tapis, le tambour marque un toc.",
        "narrateur|Sur la laine du chemin, le béret tient.",
        "enfant-f|Vous avez une route, tous les deux.",
        "papa|Le savon reste sous le tapis.",
        "maman|Tes mains ont montré le bord.",
        "narrateur|Le grain de feutre dort dans la laine.",
    ],
    (1, 1, 3): [
        "enfant-f|Un pas, très petit.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu attends avec moi ?",
        "papa|Oui, un toc, puis un pas.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il reste entre deux carreaux, trop gris.",
        "maman|Nina tient l'ours d'une main.",
        "narrateur|L'autre main tient la girafe, plus haute.",
        "enfant-f|On va au même rythme.",
        "papa|Tes mains ont fait le couloir.",
        "maman|Tu as demandé d'attendre.",
        "narrateur|Le grain de feutre reste entre deux carreaux.",
    ],
    (1, 2, 1): [
        "enfant-f|Un nœud, pour le cône.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu noues le papier ?",
        "papa|Oui, je tiens, tu guides le nœud.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il reste sur le béret, trop lourd.",
        "maman|Dans l'herbe, le tambour attend le nœud.",
        "narrateur|Trop mince, le papier tient, maintenant lié.",
        "enfant-f|Tu as ton chapeau, toi aussi.",
        "papa|Le vent n'a plus le papier.",
        "maman|Tu as demandé le nœud.",
        "narrateur|Le grain de feutre reste au nœud.",
    ],
    (1, 2, 2): [
        "enfant-f|Le mur, sans le vent.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Maman, tu marches près du mur ?",
        "maman|Oui, je me mets de ce côté.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il frotte la pierre, trop rond.",
        "papa|Le tambour donne le pas, le long du mur.",
        "narrateur|Le cône ne s'envole plus, trop près du mur.",
        "enfant-f|Vous marchez, tous les deux.",
        "papa|L'abri était là, contre la maison.",
        "maman|Tu as demandé le mur.",
        "narrateur|Le grain de feutre reste contre la pierre.",
    ],
    (1, 2, 3): [
        "enfant-f|Les chapeaux dans le panier.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu tiens le panier ?",
        "papa|Oui, je le lève, tu poses.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il tombe au fond de l'osier, gris.",
        "maman|Le tambour pose sur le bord, un toc.",
        "narrateur|L'ours a le béret sur le ventre, trop rond.",
        "enfant-f|Vos têtes regardent, quand même.",
        "papa|Le vent prend l'osier, pas le papier.",
        "maman|Tu as demandé les mains.",
        "narrateur|Le grain de feutre dort au fond du panier.",
    ],
    (1, 3, 1): [
        "enfant-f|La même marche, pour tous.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, on reste sur cette marche ?",
        "papa|Oui, on s'assoit, sans monter.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il s'assoit sur le bois, trop large.",
        "maman|Un toc sur la marche, le défilé sur place.",
        "narrateur|L'ours s'assoit, trop large, trop rond.",
        "enfant-f|On défile ici, sans monter.",
        "papa|La marche a deux places, maintenant.",
        "maman|Tu as demandé de rester.",
        "narrateur|Le grain de feutre reste sur la marche.",
    ],
    (1, 3, 2): [
        "enfant-f|On descend, plus simple.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Maman, tu descends avec moi ?",
        "maman|Oui, une marche, puis l'autre.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il glisse vers le bas, trop gris.",
        "papa|D'une marche, le tambour descend, toc plus bas.",
        "narrateur|L'ours passe, trop large, mais ça tient.",
        "enfant-f|Vous avez la place, en bas.",
        "papa|Descendre, c'était votre largeur.",
        "maman|Tu as demandé de descendre.",
        "narrateur|Le grain de feutre rejoint le hall, en bas.",
    ],
    (1, 3, 3): [
        "enfant-f|La rampe, comme un chemin.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu tiens la rampe ?",
        "papa|Oui, je la tiens, tu glisses.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il voyage sur le bois, trop étroit.",
        "maman|Le tambour voyage sur la rampe, un toc.",
        "narrateur|L'ours glisse, le béret bien enfoncé.",
        "enfant-f|Vous partez côte à côte.",
        "papa|Le bois a fait le pont.",
        "maman|Tu as demandé la rampe.",
        "narrateur|Le grain de feutre reste sur la rampe.",
    ],
    (2, 1, 1): [
        "enfant-f|Des chaussettes, aux pattes.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Maman, tu m'aides à les mettre ?",
        "maman|Oui, une patte, puis l'autre.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il montre une dalle sèche, plus loin.",
        "papa|Elle noue une chaussette, avec le ruban.",
        "narrateur|L'ours a deux chaussons de laine, trop grands.",
        "enfant-f|Vous glissez moins.",
        "papa|Chacun a sa laine, maintenant.",
        "maman|Tes mains ont demandé la laine.",
        "narrateur|Le grain de feutre tient au bord du ruban.",
    ],
    (2, 1, 2): [
        "enfant-f|Le tapis, comme une route.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu tires le tapis ?",
        "papa|Oui, je le tire, tu guides.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il s'arrête sur la laine, plus rêche.",
        "maman|Tout le long, le ruban sert de bord.",
        "narrateur|Sur la laine du chemin, le béret tient.",
        "enfant-f|Vous avez une route, tous les deux.",
        "papa|Le savon reste sous le tapis.",
        "maman|Tes mains ont montré le bord.",
        "narrateur|Le grain de feutre suit le ruban, sur le tapis.",
    ],
    (2, 1, 3): [
        "enfant-f|Un pas, très petit.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu attends avec moi ?",
        "papa|Oui, le ruban, puis un pas.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il reste entre deux carreaux, trop gris.",
        "maman|Le ruban les relie, un pas chacun.",
        "narrateur|Nina tient l'ours d'une main.",
        "enfant-f|On va au même rythme.",
        "papa|Tes mains ont fait le couloir.",
        "maman|Tu as demandé d'attendre.",
        "narrateur|Le grain de feutre voyage entre deux pas.",
    ],
    (2, 2, 1): [
        "enfant-f|Un nœud, pour le cône.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu noues le papier ?",
        "papa|Oui, je tiens, tu guides le nœud.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il reste sur le béret, trop lourd.",
        "maman|Avec le ruban, elle noue le cône, trop mince.",
        "narrateur|Trop mince, le papier tient, maintenant lié.",
        "enfant-f|Tu as ton chapeau, toi aussi.",
        "papa|Le vent n'a plus le papier.",
        "maman|Tu as demandé le nœud.",
        "narrateur|Le grain de feutre se loge dans la soie.",
    ],
    (2, 2, 2): [
        "enfant-f|Le mur, sans le vent.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Maman, tu marches près du mur ?",
        "maman|Oui, je me mets de ce côté.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il frotte la pierre, trop rond.",
        "papa|Le ruban glisse contre la pierre, trop bas.",
        "narrateur|Le cône ne s'envole plus, trop près du mur.",
        "enfant-f|Vous marchez, tous les deux.",
        "papa|L'abri était là, contre la maison.",
        "maman|Tu as demandé le mur.",
        "narrateur|Le grain de feutre colle au crépi, gris.",
    ],
    (2, 2, 3): [
        "enfant-f|Les chapeaux dans le panier.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu tiens le panier ?",
        "papa|Oui, je le lève, tu poses.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il tombe au fond de l'osier, gris.",
        "maman|Le ruban attache les deux bords, comme un toit.",
        "narrateur|L'ours a le béret sur le ventre, trop rond.",
        "enfant-f|Vos têtes regardent, quand même.",
        "papa|Le vent prend l'osier, pas le papier.",
        "maman|Tu as demandé les mains.",
        "narrateur|Le grain de feutre se cache sous le toit de soie.",
    ],
    (2, 3, 1): [
        "enfant-f|La même marche, pour tous.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, on reste sur cette marche ?",
        "papa|Oui, on s'assoit, sans monter.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il s'assoit sur le bois, trop large.",
        "maman|Le ruban fait un cercle, autour d'eux.",
        "narrateur|L'ours s'assoit, trop large, trop rond.",
        "enfant-f|On défile ici, sans monter.",
        "papa|La marche a deux places, maintenant.",
        "maman|Tu as demandé de rester.",
        "narrateur|Le grain de feutre tient au milieu du cercle.",
    ],
    (2, 3, 2): [
        "enfant-f|On descend, plus simple.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Maman, tu descends avec moi ?",
        "maman|Oui, une marche, puis l'autre.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il glisse vers le bas, trop gris.",
        "papa|Vers le bas, le ruban les guide.",
        "narrateur|L'ours passe, trop large, mais ça tient.",
        "enfant-f|Vous avez la place, en bas.",
        "papa|Descendre, c'était votre largeur.",
        "maman|Tu as demandé de descendre.",
        "narrateur|Le grain de feutre s'arrête au palier.",
    ],
    (2, 3, 3): [
        "enfant-f|La rampe, comme un chemin.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu tiens la rampe ?",
        "papa|Oui, je la tiens, tu glisses.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il voyage sur le bois, trop étroit.",
        "maman|Le ruban les tient, le long de la rampe.",
        "narrateur|L'ours glisse, le béret bien enfoncé.",
        "enfant-f|Vous partez côte à côte.",
        "papa|Le bois a fait le pont.",
        "maman|Tu as demandé la rampe.",
        "narrateur|Le grain de feutre suit le ruban, sur le bois.",
    ],
    (3, 1, 1): [
        "enfant-f|Des chaussettes, aux pattes.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Maman, tu m'aides à les mettre ?",
        "maman|Oui, une patte, puis l'autre.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il montre une dalle sèche, plus loin.",
        "papa|Elle sort les chaussettes du panier, trop chaudes.",
        "narrateur|L'ours a deux chaussons de laine, trop grands.",
        "enfant-f|Vous glissez moins.",
        "papa|Chacun a sa laine, maintenant.",
        "maman|Tes mains ont demandé la laine.",
        "narrateur|Le grain de feutre rentre dans l'osier, avec la laine.",
    ],
    (3, 1, 2): [
        "enfant-f|Le tapis, comme une route.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu tires le tapis ?",
        "papa|Oui, je le tire, tu guides.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il s'arrête sur la laine, plus rêche.",
        "maman|Au bout, elle pose le panier, comme une arrivée.",
        "narrateur|Sur la laine du chemin, le béret tient.",
        "enfant-f|Vous avez une route, tous les deux.",
        "papa|Le savon reste sous le tapis.",
        "maman|Tes mains ont montré le bord.",
        "narrateur|Le grain de feutre attend au bout du tapis.",
    ],
    (3, 1, 3): [
        "enfant-f|Un pas, très petit.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu attends avec moi ?",
        "papa|Oui, on pose, on avance, on reprend.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il reste entre deux carreaux, trop gris.",
        "maman|Elle pose le panier, avance, le reprend.",
        "narrateur|Nina tient l'ours d'une main.",
        "enfant-f|On va au même rythme.",
        "papa|Tes mains ont fait le couloir.",
        "maman|Tu as demandé d'attendre.",
        "narrateur|Le grain de feutre cogne le genou, puis se tait.",
    ],
    (3, 2, 1): [
        "enfant-f|Un nœud, pour le cône.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu noues le papier ?",
        "papa|Oui, je tiens, tu guides le nœud.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il reste sur le béret, trop lourd.",
        "maman|Dans l'osier, elle passe le cône, puis le noue.",
        "narrateur|Trop mince, le papier tient, maintenant lié.",
        "enfant-f|Tu as ton chapeau, toi aussi.",
        "papa|Le vent n'a plus le papier.",
        "maman|Tu as demandé le nœud.",
        "narrateur|Le grain de feutre reste dans l'herbe, près de l'osier.",
    ],
    (3, 2, 2): [
        "enfant-f|Le mur, sans le vent.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Maman, tu marches près du mur ?",
        "maman|Oui, je me mets de ce côté.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il frotte la pierre, trop rond.",
        "papa|Le panier racle un peu le crépi, puis avance.",
        "narrateur|Le cône ne s'envole plus, trop près du mur.",
        "enfant-f|Vous marchez, tous les deux.",
        "papa|L'abri était là, contre la maison.",
        "maman|Tu as demandé le mur.",
        "narrateur|Le grain de feutre racle le crépi, puis tient.",
    ],
    (3, 2, 3): [
        "enfant-f|Les chapeaux dans le panier.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu tiens le panier ?",
        "papa|Oui, je le lève, tu poses.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il tombe au fond de l'osier, gris.",
        "maman|Elle rentre les chapeaux, les têtes restent dehors.",
        "narrateur|L'ours a le béret sur le ventre, trop rond.",
        "enfant-f|Vos têtes regardent, quand même.",
        "papa|Le vent prend l'osier, pas le papier.",
        "maman|Tu as demandé les mains.",
        "narrateur|Le grain de feutre se loge entre les deux bords.",
    ],
    (3, 3, 1): [
        "enfant-f|La même marche, pour tous.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, on reste sur cette marche ?",
        "papa|Oui, on s'assoit, sans monter.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il s'assoit sur le bois, trop large.",
        "maman|Le panier s'assoit sur la marche, trop juste.",
        "narrateur|L'ours s'assoit, trop large, trop rond.",
        "enfant-f|On défile ici, sans monter.",
        "papa|La marche a deux places, maintenant.",
        "maman|Tu as demandé de rester.",
        "narrateur|Le grain de feutre s'assoit sur le bois ciré.",
    ],
    (3, 3, 2): [
        "enfant-f|On descend, plus simple.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Maman, tu descends avec moi ?",
        "maman|Oui, une marche, puis l'autre.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il glisse vers le bas, trop gris.",
        "papa|D'une marche, le panier glisse, puis s'arrête.",
        "narrateur|L'ours passe, trop large, mais ça tient.",
        "enfant-f|Vous avez la place, en bas.",
        "papa|Descendre, c'était votre largeur.",
        "maman|Tu as demandé de descendre.",
        "narrateur|Le grain de feutre glisse d'une marche, puis s'arrête.",
    ],
    (3, 3, 3): [
        "enfant-f|La rampe, comme un chemin.",
        "narrateur|Nina refuse de foncer.",
        "enfant-f|Papa, tu tiens la rampe ?",
        "papa|Oui, je la tiens, tu glisses.",
        "narrateur|Elle cherche le grain de feutre.",
        "narrateur|Il voyage sur le bois, trop étroit.",
        "maman|Le panier glisse sur le bois, trop étroit.",
        "narrateur|L'ours glisse, le béret bien enfoncé.",
        "enfant-f|Vous partez côte à côte.",
        "papa|Le bois a fait le pont.",
        "maman|Tu as demandé la rampe.",
        "narrateur|Le grain de feutre suit l'osier, le long du bois.",
    ],
}

END_SONS = {1: "couloir,laine", 2: "jardin,vent", 3: "escalier,bois"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Les chaussettes de laine sentent le tiroir.",
        "enfant-f|Vous avez fini le couloir.",
        "papa|Tes mains ont demandé la laine.",
        "maman|Ils sont arrivés ensemble.",
        "enfant-f|Ça a failli glisser.",
        "papa|Puis tu as tendu les chaussettes.",
        "narrateur|Le tambour reste tiède, près des chaussons.",
        "narrateur|Le grain de feutre dort sur la chaussette.",
    ],
    (1, 1, 2): [
        "narrateur|Le tapis garde deux traces, l'une ronde.",
        "enfant-f|La route était à nous.",
        "papa|Le savon est resté dessous.",
        "maman|Deux silhouettes, une allée.",
        "enfant-f|Ça a failli partir de travers.",
        "maman|Puis tu as montré le bord.",
        "narrateur|Le tambour se tait, contre le tapis.",
        "narrateur|Le grain de feutre s'endort dans la laine du tapis.",
    ],
    (1, 1, 3): [
        "narrateur|Leurs pas ont marqué le savon, trop petits.",
        "enfant-f|On allait au même rythme.",
        "papa|Tes mains ont fait le couloir.",
        "maman|Le carrelage n'a plus gagné.",
        "enfant-f|Ça a failli trop vite.",
        "papa|Puis tu as demandé d'attendre.",
        "narrateur|Un toc s'éteint, près des carreaux.",
        "narrateur|Le grain de feutre reste entre deux carreaux.",
    ],
    (1, 2, 1): [
        "narrateur|Le nœud tient, un peu de vent dedans.",
        "enfant-f|Tu as ton chapeau, toi aussi.",
        "papa|Le vent n'a plus le papier.",
        "maman|Deux têtes, le même air.",
        "enfant-f|Ça a failli s'envoler.",
        "papa|Puis tu as demandé le nœud.",
        "narrateur|Le tambour attend dans l'herbe, un toc mouillé.",
        "narrateur|Le grain de feutre reste au nœud, trop serré.",
    ],
    (1, 2, 2): [
        "narrateur|L'ombre du mur sent la pierre.",
        "enfant-f|Vous avez marché, tous les deux.",
        "papa|L'abri était là.",
        "maman|Le jardin reste à côté.",
        "enfant-f|Ça a failli trop claquer.",
        "maman|Puis tu as demandé le mur.",
        "narrateur|Le tambour racle le crépi, un toc de pierre.",
        "narrateur|Le grain de feutre reste collé à la pierre.",
    ],
    (1, 2, 3): [
        "narrateur|Deux têtes dépassent de l'osier.",
        "enfant-f|Tête contre tête.",
        "papa|Le vent a pris l'osier, pas eux.",
        "maman|Ils ont défilé, quand même.",
        "enfant-f|Ça a failli trop pencher.",
        "papa|Puis tu as demandé les mains.",
        "narrateur|Un toc dans l'osier, puis plus.",
        "narrateur|Le grain de feutre dort au fond du panier.",
    ],
    (1, 3, 1): [
        "narrateur|La marche garde deux ronds, l'un plus large.",
        "enfant-f|On a défilé ici, sans monter.",
        "papa|La marche avait deux places.",
        "maman|Plus besoin du plafond.",
        "enfant-f|Ça a failli trop serrer.",
        "papa|Puis tu as demandé de rester.",
        "narrateur|Le tambour s'assoit, un toc sur le bois.",
        "narrateur|Le grain de feutre reste sur la marche.",
    ],
    (1, 3, 2): [
        "narrateur|En bas, le hall sent les manteaux.",
        "enfant-f|Vous aviez la place, plus bas.",
        "papa|Descendre, c'était votre largeur.",
        "maman|Le bois sent, plus bas.",
        "enfant-f|Ça a failli buter.",
        "maman|Puis tu as demandé de descendre.",
        "narrateur|Le tambour descend, un toc plus bas.",
        "narrateur|Le grain de feutre rejoint le hall, en bas.",
    ],
    (1, 3, 3): [
        "narrateur|La rampe garde un fil de laine, trop petit.",
        "enfant-f|Vous êtes partis côte à côte.",
        "papa|Le bois a fait le pont.",
        "maman|Les marches sont restées en dessous.",
        "enfant-f|Ça a failli trop étroit.",
        "papa|Puis tu as demandé la rampe.",
        "narrateur|Le tambour glisse, un toc de bois.",
        "narrateur|Le grain de feutre reste sur la rampe.",
    ],
    (2, 1, 1): [
        "narrateur|Les chaussettes de laine sentent le tiroir.",
        "enfant-f|Vous avez fini le couloir.",
        "papa|Tes mains ont demandé la laine.",
        "maman|Ils sont arrivés ensemble.",
        "enfant-f|Ça a failli glisser.",
        "papa|Puis tu as tendu les chaussettes.",
        "narrateur|Le ruban garde un pli, près de la laine.",
        "narrateur|Le grain de feutre tient au bord du ruban.",
    ],
    (2, 1, 2): [
        "narrateur|Le tapis garde deux traces, l'une ronde.",
        "enfant-f|La route était à nous.",
        "papa|Le savon est resté dessous.",
        "maman|Deux silhouettes, une allée.",
        "enfant-f|Ça a failli partir de travers.",
        "maman|Puis tu as montré le bord.",
        "narrateur|Le ruban sert de bord, trop soyeux.",
        "narrateur|Le grain de feutre suit le ruban, sur le tapis.",
    ],
    (2, 1, 3): [
        "narrateur|Leurs pas ont marqué le savon, trop petits.",
        "enfant-f|On allait au même rythme.",
        "papa|Tes mains ont fait le couloir.",
        "maman|Le carrelage n'a plus gagné.",
        "enfant-f|Ça a failli trop vite.",
        "papa|Puis tu as demandé d'attendre.",
        "narrateur|Le ruban les relie, un pas chacun.",
        "narrateur|Le grain de feutre voyage entre deux pas.",
    ],
    (2, 2, 1): [
        "narrateur|Le nœud tient, un peu de vent dedans.",
        "enfant-f|Tu as ton chapeau, toi aussi.",
        "papa|Le vent n'a plus le papier.",
        "maman|Deux têtes, le même air.",
        "enfant-f|Ça a failli s'envoler.",
        "papa|Puis tu as demandé le nœud.",
        "narrateur|Le ruban serre le nœud, trop soyeux.",
        "narrateur|Le grain de feutre se loge dans la soie.",
    ],
    (2, 2, 2): [
        "narrateur|L'ombre du mur sent la pierre.",
        "enfant-f|Vous avez marché, tous les deux.",
        "papa|L'abri était là.",
        "maman|Le jardin reste à côté.",
        "enfant-f|Ça a failli trop claquer.",
        "maman|Puis tu as demandé le mur.",
        "narrateur|Le ruban frotte le mur, trop bas.",
        "narrateur|Le grain de feutre colle au crépi, gris.",
    ],
    (2, 2, 3): [
        "narrateur|Deux têtes dépassent de l'osier.",
        "enfant-f|Tête contre tête.",
        "papa|Le vent a pris l'osier, pas eux.",
        "maman|Ils ont défilé, quand même.",
        "enfant-f|Ça a failli trop pencher.",
        "papa|Puis tu as demandé les mains.",
        "narrateur|Le ruban fait un toit, trop mince.",
        "narrateur|Le grain de feutre se cache sous le toit de soie.",
    ],
    (2, 3, 1): [
        "narrateur|La marche garde deux ronds, l'un plus large.",
        "enfant-f|On a défilé ici, sans monter.",
        "papa|La marche avait deux places.",
        "maman|Plus besoin du plafond.",
        "enfant-f|Ça a failli trop serrer.",
        "papa|Puis tu as demandé de rester.",
        "narrateur|Le ruban fait un cercle, autour d'eux.",
        "narrateur|Le grain de feutre tient au milieu du cercle.",
    ],
    (2, 3, 2): [
        "narrateur|En bas, le hall sent les manteaux.",
        "enfant-f|Vous aviez la place, plus bas.",
        "papa|Descendre, c'était votre largeur.",
        "maman|Le bois sent, plus bas.",
        "enfant-f|Ça a failli buter.",
        "maman|Puis tu as demandé de descendre.",
        "narrateur|Le ruban guide vers le bas, trop long.",
        "narrateur|Le grain de feutre s'arrête au palier.",
    ],
    (2, 3, 3): [
        "narrateur|La rampe garde un fil de laine, trop petit.",
        "enfant-f|Vous êtes partis côte à côte.",
        "papa|Le bois a fait le pont.",
        "maman|Les marches sont restées en dessous.",
        "enfant-f|Ça a failli trop étroit.",
        "papa|Puis tu as demandé la rampe.",
        "narrateur|Le ruban suit la rampe, trop soyeux.",
        "narrateur|Le grain de feutre suit le ruban, sur le bois.",
    ],
    (3, 1, 1): [
        "narrateur|Les chaussettes de laine sentent le tiroir.",
        "enfant-f|Vous avez fini le couloir.",
        "papa|Tes mains ont demandé la laine.",
        "maman|Ils sont arrivés ensemble.",
        "enfant-f|Ça a failli glisser.",
        "papa|Puis tu as tendu les chaussettes.",
        "narrateur|Un fil d'osier pique, trop rêche.",
        "narrateur|Le grain de feutre rentre dans l'osier, avec la laine.",
    ],
    (3, 1, 2): [
        "narrateur|Le tapis garde deux traces, l'une ronde.",
        "enfant-f|La route était à nous.",
        "papa|Le savon est resté dessous.",
        "maman|Deux silhouettes, une allée.",
        "enfant-f|Ça a failli partir de travers.",
        "maman|Puis tu as montré le bord.",
        "narrateur|Le panier marque l'arrivée, trop rêche.",
        "narrateur|Le grain de feutre attend au bout du tapis.",
    ],
    (3, 1, 3): [
        "narrateur|Leurs pas ont marqué le savon, trop petits.",
        "enfant-f|On allait au même rythme.",
        "papa|Tes mains ont fait le couloir.",
        "maman|Le carrelage n'a plus gagné.",
        "enfant-f|Ça a failli trop vite.",
        "papa|Puis tu as demandé d'attendre.",
        "narrateur|Le panier avance, trop bas, trop rêche.",
        "narrateur|Le grain de feutre cogne le genou, puis se tait.",
    ],
    (3, 2, 1): [
        "narrateur|Le nœud tient, un peu de vent dedans.",
        "enfant-f|Tu as ton chapeau, toi aussi.",
        "papa|Le vent n'a plus le papier.",
        "maman|Deux têtes, le même air.",
        "enfant-f|Ça a failli s'envoler.",
        "papa|Puis tu as demandé le nœud.",
        "narrateur|Le panier tient le nœud, trop rêche.",
        "narrateur|Le grain de feutre reste dans l'herbe, près de l'osier.",
    ],
    (3, 2, 2): [
        "narrateur|L'ombre du mur sent la pierre.",
        "enfant-f|Vous avez marché, tous les deux.",
        "papa|L'abri était là.",
        "maman|Le jardin reste à côté.",
        "enfant-f|Ça a failli trop claquer.",
        "maman|Puis tu as demandé le mur.",
        "narrateur|Le panier racle le mur, trop rêche.",
        "narrateur|Le grain de feutre racle le crépi, puis tient.",
    ],
    (3, 2, 3): [
        "narrateur|Deux têtes dépassent de l'osier.",
        "enfant-f|Tête contre tête.",
        "papa|Le vent a pris l'osier, pas eux.",
        "maman|Ils ont défilé, quand même.",
        "enfant-f|Ça a failli trop pencher.",
        "papa|Puis tu as demandé les mains.",
        "narrateur|Les têtes dépassent, trop différentes.",
        "narrateur|Le grain de feutre se loge entre les deux bords.",
    ],
    (3, 3, 1): [
        "narrateur|La marche garde deux ronds, l'un plus large.",
        "enfant-f|On a défilé ici, sans monter.",
        "papa|La marche avait deux places.",
        "maman|Plus besoin du plafond.",
        "enfant-f|Ça a failli trop serrer.",
        "papa|Puis tu as demandé de rester.",
        "narrateur|Le panier s'assoit, trop juste, trop rêche.",
        "narrateur|Le grain de feutre s'assoit sur le bois ciré.",
    ],
    (3, 3, 2): [
        "narrateur|En bas, le hall sent les manteaux.",
        "enfant-f|Vous aviez la place, plus bas.",
        "papa|Descendre, c'était votre largeur.",
        "maman|Le bois sent, plus bas.",
        "enfant-f|Ça a failli buter.",
        "maman|Puis tu as demandé de descendre.",
        "narrateur|Le panier glisse d'une marche, trop large.",
        "narrateur|Le grain de feutre glisse d'une marche, puis s'arrête.",
    ],
    (3, 3, 3): [
        "narrateur|La rampe garde un fil de laine, trop petit.",
        "enfant-f|Vous êtes partis côte à côte.",
        "papa|Le bois a fait le pont.",
        "maman|Les marches sont restées en dessous.",
        "enfant-f|Ça a failli trop étroit.",
        "papa|Puis tu as demandé la rampe.",
        "narrateur|Le panier suit la rampe, trop étroit.",
        "narrateur|Le grain de feutre suit l'osier, le long du bois.",
    ],
}


def t2_question(t1: int) -> list[str]:
    return [
        f"narrateur|{T1[t1]['voy']}",
        "narrateur|Le couloir brille, trop lisse.",
        "narrateur|Dehors, le jardin souffle trop.",
        "narrateur|Plus loin, l'escalier monte, étroit.",
        "papa|Nina, vous partez où ?",
    ]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "manteaux,patere",
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le tambour", "le ruban", "le panier")},
    )

    for a in (1, 2, 3):
        p = f"CHK_T0001_P000{a}"
        t1 = T1[a]
        out_chunks[p] = voice(by_src[p], t1["passage"], "action", t1["sons"], {"emphasis": t1["emphasis"]})
        out_chunks[f"{p}_Q0001"] = voice(
            by_src[f"{p}_Q0001"], t1["question"], "clue", "",
            {"emphasis": t1["emphasis"], "fields": t1["qfields"]},
        )
        out_chunks[f"{p}_C0001"] = voice(
            by_src[f"{p}_C0001"], t1["confirm"], "confirm", t1["sons"], {"emphasis": t1["emphasis"]},
        )
        out_chunks[f"{p}_T0002_P0000"] = voice(
            by_src[f"{p}_T0002_P0000"], t2_question(a), "choice", "",
            {"fields": t3lab("le couloir", "le jardin", "l'escalier")},
        )
        for b in (1, 2, 3):
            sp = f"{p}_T0002_P000{b}"
            t2 = T2[(a, b)]
            out_chunks[sp] = voice(
                by_src[sp], t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emphasis"]},
            )
            out_chunks[f"{sp}_T0003_P0000"] = voice(
                by_src[f"{sp}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab(*T3_LABS[b])},
            )
            for c in (1, 2, 3):
                leaf = f"{sp}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], T3[(a, b, c)], "resolution", T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ENDINGS[(a, b, c)], "ending", END_SONS[b],
                    {"emphasis": "grain de feutre"},
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
        "plus rond ou plus mince",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "j'ai compris",
        "mission accomplie",
        "il faut attendre",
        "il faut demander",
        "on doit demander",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "capitaine",
        "plic",
        "volet jaune",
        "merle",
        "miel",
        "tout doux",
        "tout calme",
        "aujourd'hui,",
        "larme de bronze",
        "écaille de lichen",
        "grain doré",
        "amir",
        "aniss",
        "nino",
        "raphaël",
        "chouchou",
        "mila",
        "victorino",
        "victorina",
        "sarah",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(blob):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "grain de feutre" not in blob:
        raise SystemExit(f"{SID}: grain de feutre absent")
    adults = [ln for ln in blob.splitlines() if ln.startswith("papa|") or ln.startswith("maman|")]
    aj = " ".join(a.split("|", 1)[1] for a in adults)
    if aj.count("merci") + aj.count("bravo") != 1:
        raise SystemExit(f"{SID}: merci/bravo ×{aj.count('merci') + aj.count('bravo')}")

    fins = [c["text"] for c in story["chunks"] if c["kind"] == "passage_fin"]
    if len(fins) != 27 or len(set(fins)) != 27:
        raise SystemExit(f"fins distinctes {len(set(fins))}/27")
    lasts = []
    for c in story["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        lasts.append(last_n[-1])
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
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
    if any(c.get("text_xai_tags") == c.get("text") for c in story["chunks"]):
        raise SystemExit("text_xai_tags = text")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "- **Public :** N2 (4–5 ans), audio familial\n"
        "- **Leçon :** DIF.COR.002 — demander / attendre l'aide, pas tout seul (vécue, jamais dite)\n"
        "- **Personnages :** Nina, papa, maman (un seul enfant)\n"
        "- **Lieu :** hall de la maison, couloir, jardin, escalier\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` / labels inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Nina connaît la patère jaune du hall. Un **grain de feutre** gris paraît nouveau "
        "sur le béret. Elle veut un vrai défilé pour l'ours et la girafe, **maintenant**, "
        "avant que papa range les chapeaux. Première idée trop vite, toute seule : les chapeaux "
        "glissent, le grain tombe. Elle prend le tambour, le ruban ou le panier ; les trois "
        "partent. Le couloir glisse, le jardin souffle, l'escalier serre. Une 2e ruse : "
        "le grain glisse, montre le vrai endroit. Elle refuse de foncer, écoute le lieu, "
        "demande. Neuf façons : chaussettes, tapis, petits pas ; nœud, mur, panier-tête ; "
        "même marche, descendre, rampe. Les deux chapeaux restent. Le grain paie l'ouverture.\n\n"
        "## Vécu\n\n"
        "Nina veut le défilé **maintenant**. Elle force toute seule, ça résiste. "
        "Sourire disparu, poitrine bousculée, adulte accroupi. Personne ne donne la réponse. "
        "Elle observe l'objet, écoute le lieu, retrouve le grain du début. La leçon se voit : "
        "lâcher, demander, attendre, faire à deux. Le dénouement a failli (glisser, s'envoler, "
        "buter). Le grain paie l'ouverture. Chaque fin porte une trace unique.\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan « Plus rond ou plus mince », Léa, merle, miel, tics jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés. Ouverture inventée.\n"
        "- Pas de 2e enfant (xlsx : Nina, papa, maman seulement).\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'obstacle. 9 T2, 27 T3, 27 fins.\n"
        "- Indice unique dès l'ouverture : le grain de feutre, payé au climax.\n"
        "- Merci vécu (papa : tu as posé le cône). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        f"- N2 ≤ 15. `check()` OK. Pas apply.\n\n"
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
