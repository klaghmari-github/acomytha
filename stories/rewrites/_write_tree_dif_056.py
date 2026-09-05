#!/usr/bin/env python3
"""TREE-DIF-056 — La bulle de Nina, sur le nez de bronze (N2, DIF.BES.001, example4 v2)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-056"
N2 = 15
TITLE = "La bulle de Nina, sur le nez de bronze"
FIL = (
    "Au parc du village, Nina veut poser une bulle sur la larme de bronze, "
    "avant la cloche. Papa veut marcher. Elle veut souffler maintenant. "
    "Elle prend le bâton, le savon ou la coupelle ; les trois viennent. "
    "L'allée soulève, le socle brûle, le tilleul claque. "
    "Neuf façons de laisser l'air se taire. La bulle tient sur la larme."
)
CHARS = "Nina, papa, maman"
SETTING = "parc du village : allée, statue de bronze, tilleul"
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
    "papa sourit",
    "maman sourit",
)
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "larme de bronze",
        "note": "arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=nina_veut_la_bulle_papa_veut_marcher; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
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
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=les_trois_affaires_partent; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=souffler_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=l_air_n_est_pas_prêt; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "larme",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=la_larme_guide_le_souffle; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "larme de bronze",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_bulle_tient_sur_la_larme; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Dans le sac, le bâton cogne la coupelle.",
    "narrateur|Une goutte de savon perle au poignet de Nina.",
    "narrateur|Le parc sent le tilleul chaud, et le gravier.",
    "narrateur|La statue de bronze tient un oiseau, trop petit.",
    "papa|Tu as vu son nez, Nina ?",
    "enfant-f|Il a une larme de bronze, plus sombre.",
    "maman|Elle n'est pas de l'eau.",
    "narrateur|Le gravier chauffe sous ses sandales.",
    "narrateur|Nina passe ici souvent, après l'école.",
    "narrateur|Cette larme, elle ne l'avait pas vue.",
    "narrateur|En ce moment, Nina serre le sac contre elle.",
    "enfant-f|Je veux une bulle, collée sur la larme.",
    "papa|La cloche va fermer le parc.",
    "maman|On marche d'abord, non ?",
    "enfant-f|Non, la bulle, maintenant.",
    "papa|Merci, tu as essuyé la goutte.",
    "narrateur|Le sac pend, trop plein pour courir.",
]

T1_CHOICE = [
    "narrateur|Près du sac, trois affaires attendent.",
    "narrateur|Un bâton, un savon, une coupelle.",
    "maman|Par quoi tu commences, Nina ?",
]

T1 = {
    1: {
        "lab": "le bâton",
        "sons": "bois,savon",
        "emphasis": "bâton",
        "passage": [
            "narrateur|Nina attrape d'abord le bâton, un peu humide.",
            "enfant-f|La bulle va s'y accrocher.",
            "maman|Garde le cercle en l'air.",
            "narrateur|Un film tremble au bout, puis tient.",
            "narrateur|Elle lève le bois, trop vite.",
            "papa|Pas si fort, le fil va casser.",
            "narrateur|Nina baisse le cercle, les joues chaudes.",
            "papa|Prends le savon, il est à tes pieds.",
            "narrateur|La coupelle glisse sous son autre bras.",
            "narrateur|Les trois partent, collés à Nina.",
            "enfant-f|Nez, j'arrive.",
            "narrateur|Le bois sent le savon, un peu.",
            "papa|Le bâton est à toi, là.",
            "narrateur|Elle veut souffler tout de suite, trop.",
            "maman|Le bronze est loin, d'abord.",
        ],
        "question": [
            "narrateur|Nina a pris le bâton d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "bâton",
            "accepted_examples": "bâton | le bâton | d'abord le bâton | le bois",
            "retry_prompt": "Nina prend le bâton d'abord.",
        },
        "confirm": [
            "narrateur|Le bâton reste contre elle, un peu humide.",
            "enfant-f|On va jusqu'au bronze.",
            "maman|La cloche n'est pas loin.",
            "papa|Tu tiens bien, Nina ?",
            "enfant-f|Oui, papa.",
            "narrateur|Un fil de savon cherche l'air.",
            "papa|On avance, sans courir.",
            "narrateur|Le cercle penche, puis se redresse.",
            "maman|Le savon et la coupelle sont avec toi.",
        ],
        "voy": "Le bâton penche vers le bronze.",
    },
    2: {
        "lab": "le savon",
        "sons": "flacon,goutte",
        "emphasis": "savon",
        "passage": [
            "narrateur|Nina dévisse d'abord le savon, sans se presser.",
            "enfant-f|Il va donner la bulle.",
            "papa|Une goutte, pas tout le flacon.",
            "narrateur|La goutte reste au pouce, puis tombe.",
            "narrateur|Elle veut souffler, tout de suite.",
            "maman|Le bâton t'attend, près du sac.",
            "narrateur|Papa pose la coupelle contre le gravier chaud.",
            "narrateur|Nina serre les trois contre son ventre.",
            "enfant-f|Savon, tu restes avec moi.",
            "narrateur|Le flacon colle un peu sa manche.",
            "maman|Le savon est ouvert, tu peux y aller.",
            "papa|Sans courir, Nina.",
            "narrateur|Elle essuie le pouce contre le bois.",
            "enfant-f|Vite, avant la cloche.",
        ],
        "question": [
            "narrateur|Nina a pris le savon d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "savon",
            "accepted_examples": "savon | le savon | d'abord le savon | le flacon",
            "retry_prompt": "Nina prend le savon d'abord.",
        },
        "confirm": [
            "narrateur|Le savon pend au poignet, un peu lâche.",
            "enfant-f|Il va filer la bulle.",
            "papa|Ça sent le savon, toi.",
            "maman|Tes mains sont prêtes ?",
            "enfant-f|Oui, maman.",
            "narrateur|Une goutte se tait, puis plus rien.",
            "maman|On avance, sans se presser.",
            "narrateur|Le flacon tape son poignet, à chaque pas.",
            "papa|Le bâton et la coupelle sont avec toi.",
        ],
        "voy": "Le savon colle à sa manche.",
    },
    3: {
        "lab": "la coupelle",
        "sons": "bol,eau",
        "emphasis": "coupelle",
        "passage": [
            "narrateur|Nina lève d'abord la coupelle, bien à plat.",
            "enfant-f|Le savon va dormir dedans.",
            "maman|Pas trop d'eau, juste un miroir.",
            "narrateur|Le rond tremble, puis s'arrête.",
            "narrateur|Elle penche le bol vers ses lèvres.",
            "papa|Pas maintenant, le bronze est loin.",
            "narrateur|Il glisse le bâton et le savon contre elle.",
            "narrateur|Le gravier reste vide, derrière eux.",
            "enfant-f|Coupelle, je te porte.",
            "narrateur|Un cercle de savon brille au fond.",
            "papa|La coupelle est prête, on avance.",
            "maman|Sans verser, tout droit.",
            "narrateur|Elle veut souffler dans le miroir, trop tôt.",
            "papa|Le nez d'abord, pas le bol.",
        ],
        "question": [
            "narrateur|Nina a pris la coupelle d'abord.",
            "maman|Elle a pris quoi, d'abord ?",
        ],
        "qfields": {
            "expected_answer": "coupelle",
            "accepted_examples": "coupelle | la coupelle | d'abord la coupelle | le bol",
            "retry_prompt": "Nina prend la coupelle d'abord.",
        },
        "confirm": [
            "narrateur|La coupelle reste plate, contre son ventre.",
            "enfant-f|Le savon ne verse pas.",
            "maman|Le rond sent le tilleul, un peu.",
            "papa|On avance, tous les trois ?",
            "enfant-f|Oui.",
            "narrateur|Le miroir de savon attend, plat.",
            "papa|On marche, sans se presser.",
            "narrateur|Le bol chauffe un peu, contre le pull.",
            "maman|Le bâton et le savon sont avec toi.",
        ],
        "voy": "La coupelle appuie contre son ventre.",
    },
}

T2 = {
    (1, 1): {
        "sons": "gravier,pas",
        "emphasis": "allée",
        "passage": [
            "narrateur|Entre ses doigts, le bois du bâton est tiède.",
            "narrateur|Le gravier de l'allée saute sous les pas.",
            "narrateur|Un fil se casse, trop vite, trop fort.",
            "enfant-f|Ma bulle a crevé !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Ici, ça n'arrête pas.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Elle lève le bâton, trop vite.",
            "narrateur|Un pas tardif soulève la poussière, gris.",
            "enfant-f|Pas maintenant.",
            "narrateur|La larme de bronze est grise, trop.",
            "maman|Tu vois comment, Nina ?",
        ],
    },
    (1, 2): {
        "sons": "bronze,soleil",
        "emphasis": "socle",
        "passage": [
            "narrateur|Entre ses doigts, le bois du bâton est tiède.",
            "narrateur|Le bronze tient tout le soleil.",
            "narrateur|Le fil fond, trop chaud, trop mince.",
            "enfant-f|Le nez brûle trop !",
            "narrateur|La bulle touche, puis crève tout de suite.",
            "narrateur|Il ne reste rien sur le bronze.",
            "papa|Ici, c'est trop chaud.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un nuage passe, et Nina lève le bois.",
            "narrateur|Le soleil revient, net, sur la larme.",
            "enfant-f|Pas maintenant.",
            "narrateur|La larme de bronze est sèche, trop pâle.",
            "maman|Tu vois comment, Nina ?",
        ],
    },
    (1, 3): {
        "sons": "feuilles,vent",
        "emphasis": "tilleul",
        "passage": [
            "narrateur|Entre ses doigts, le bois du bâton est tiède.",
            "narrateur|Le tilleul agite ses feuilles, trop vite.",
            "narrateur|Le fil claque, trop léger dans l'air.",
            "enfant-f|Le vent prend tout !",
            "narrateur|Une feuille claque, puis une autre.",
            "narrateur|La bulle part de travers, trop loin.",
            "papa|Ici, ça souffle trop.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Les feuilles se taisent, un instant.",
            "narrateur|Nina lève le bâton, trop tôt.",
            "narrateur|Un souffle tardif plie le fil.",
            "enfant-f|Pas maintenant.",
            "narrateur|La larme de bronze reste nette, elle.",
            "maman|Tu vois comment, Nina ?",
        ],
    },
    (2, 1): {
        "sons": "gravier,flacon",
        "emphasis": "allée",
        "passage": [
            "narrateur|Dans sa paume, le flacon de savon est tiède.",
            "narrateur|Le gravier de l'allée saute sous les pas.",
            "narrateur|La goutte saute, trop sèche, trop vite.",
            "enfant-f|Ma bulle a crevé !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Ici, ça n'arrête pas.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Elle ouvre le flacon, trop vite.",
            "narrateur|Un pas tardif soulève la poussière, gris.",
            "enfant-f|Pas maintenant.",
            "narrateur|La larme de bronze est grise, trop.",
            "maman|Tu vois comment, Nina ?",
        ],
    },
    (2, 2): {
        "sons": "bronze,flacon",
        "emphasis": "socle",
        "passage": [
            "narrateur|Dans sa paume, le flacon de savon est tiède.",
            "narrateur|Le bronze tient tout le soleil.",
            "narrateur|La goutte sèche, trop vite, trop chaude.",
            "enfant-f|Le nez brûle trop !",
            "narrateur|La bulle touche, puis crève tout de suite.",
            "narrateur|Il ne reste rien sur le bronze.",
            "papa|Ici, c'est trop chaud.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un nuage passe, et Nina penche le flacon.",
            "narrateur|Le soleil revient, net, sur la larme.",
            "enfant-f|Pas maintenant.",
            "narrateur|La larme de bronze est sèche, trop pâle.",
            "maman|Tu vois comment, Nina ?",
        ],
    },
    (2, 3): {
        "sons": "feuilles,flacon",
        "emphasis": "tilleul",
        "passage": [
            "narrateur|Dans sa paume, le flacon de savon est tiède.",
            "narrateur|Le tilleul agite ses feuilles, trop vite.",
            "narrateur|La goutte s'envole, trop prise par le vent.",
            "enfant-f|Le vent prend tout !",
            "narrateur|Une feuille claque, puis une autre.",
            "narrateur|La bulle part de travers, trop loin.",
            "papa|Ici, ça souffle trop.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Les feuilles se taisent, un instant.",
            "narrateur|Nina penche le flacon, trop tôt.",
            "narrateur|Un souffle tardif emporte la goutte.",
            "enfant-f|Pas maintenant.",
            "narrateur|La larme de bronze reste nette, elle.",
            "maman|Tu vois comment, Nina ?",
        ],
    },
    (3, 1): {
        "sons": "gravier,bol",
        "emphasis": "allée",
        "passage": [
            "narrateur|Contre son ventre, la coupelle reste bien plate.",
            "narrateur|Le gravier de l'allée saute sous les pas.",
            "narrateur|Le rond se plisse, trop agité, trop gris.",
            "enfant-f|Ma bulle a crevé !",
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
            "papa|Ici, ça n'arrête pas.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Elle penche le bol, trop vite.",
            "narrateur|Un pas tardif soulève la poussière, gris.",
            "enfant-f|Pas maintenant.",
            "narrateur|La larme de bronze est grise, trop.",
            "maman|Tu vois comment, Nina ?",
        ],
    },
    (3, 2): {
        "sons": "bronze,bol",
        "emphasis": "socle",
        "passage": [
            "narrateur|Contre son ventre, la coupelle reste bien plate.",
            "narrateur|Le bronze tient tout le soleil.",
            "narrateur|Le rond tremble, trop chaud, trop mince.",
            "enfant-f|Le nez brûle trop !",
            "narrateur|La bulle touche, puis crève tout de suite.",
            "narrateur|Il ne reste rien sur le bronze.",
            "papa|Ici, c'est trop chaud.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Un nuage passe, et Nina penche le bol.",
            "narrateur|Le soleil revient, net, sur la larme.",
            "enfant-f|Pas maintenant.",
            "narrateur|La larme de bronze est sèche, trop pâle.",
            "maman|Tu vois comment, Nina ?",
        ],
    },
    (3, 3): {
        "sons": "feuilles,bol",
        "emphasis": "tilleul",
        "passage": [
            "narrateur|Contre son ventre, la coupelle reste bien plate.",
            "narrateur|Le tilleul agite ses feuilles, trop vite.",
            "narrateur|Le rond se plie, trop poussé par les feuilles.",
            "enfant-f|Le vent prend tout !",
            "narrateur|Une feuille claque, puis une autre.",
            "narrateur|La bulle part de travers, trop loin.",
            "papa|Ici, ça souffle trop.",
            "narrateur|Papa s'accroupit, à la même hauteur.",
            "narrateur|Les feuilles se taisent, un instant.",
            "narrateur|Nina penche le bol, trop tôt.",
            "narrateur|Un souffle tardif plie le miroir.",
            "enfant-f|Pas maintenant.",
            "narrateur|La larme de bronze reste nette, elle.",
            "maman|Tu vois comment, Nina ?",
        ],
    },
}

T2_Q = {
    1: [
        "narrateur|Devant, l'allée soulève trop de poussière.",
        "narrateur|Le socle, lui, brûle au soleil.",
        "narrateur|Sous le tilleul, les feuilles claquent.",
        "papa|Nina, tu vas où ?",
    ],
}

T3_LABS = {
    1: ("attendre les pas", "plus bas", "le bord"),
    2: ("attendre l'ombre", "l'oiseau", "tout près"),
    3: ("attendre les feuilles", "derrière", "tout petit"),
}

T3_CHOICE = {
    1: [
        "narrateur|L'allée n'a pas fini de soulever.",
        "papa|Attendre les pas, plus bas, ou le bord ?",
    ],
    2: [
        "narrateur|Le bronze n'a pas fini de brûler.",
        "maman|Attendre l'ombre, l'oiseau, ou tout près ?",
    ],
    3: [
        "narrateur|Les feuilles n'ont pas fini de claquer.",
        "papa|Attendre les feuilles, derrière, ou tout petit ?",
    ],
}

T3_SONS = {
    (1, 1): "pas,silence",
    (1, 2): "herbe,genoux",
    (1, 3): "herbe,bord",
    (2, 1): "ombre,tilleul",
    (2, 2): "oiseau,bronze",
    (2, 3): "socle,souffle",
    (3, 1): "feuilles,silence",
    (3, 2): "tronc,abri",
    (3, 3): "bulle,petit",
}

T3_EMPH = {
    1: {1: "pas", 2: "plus bas", 3: "bord"},
    2: {1: "ombre", 2: "oiseau", 3: "tout près"},
    3: {1: "feuilles", 2: "derrière", 3: "tout petit"},
}

T3 = {
    (1, 1, 1): [
        "enfant-f|On attend les pas.",
        "narrateur|Nina tient le bâton, sans souffler.",
        "narrateur|Le gravier se tait, une fois, puis plus.",
        "narrateur|La larme de bronze redevient sombre, nette.",
        "enfant-f|Tu peux partir, maintenant.",
        "narrateur|Pendant ce temps, le bâton reste droit.",
        "papa|Les pas se sont tus, là.",
        "narrateur|La bulle part, ronde, vers la larme.",
        "maman|Tu as laissé le gravier se taire.",
    ],
    (1, 1, 2): [
        "enfant-f|Plus bas, d'abord.",
        "narrateur|Elle baisse le bâton, loin de la poussière.",
        "narrateur|Nina s'accroupit, les genoux au gravier.",
        "narrateur|L'air est plus doux, près de l'herbe.",
        "narrateur|La larme de bronze se voit d'en bas.",
        "enfant-f|Ici, tu ne crèves plus.",
        "papa|Tu as vu l'herbe, avant.",
        "narrateur|Un fil de savon cherche l'air, bas.",
        "maman|Près du sol, ça tenait mieux.",
    ],
    (1, 1, 3): [
        "enfant-f|Au bord, tout petit.",
        "narrateur|Elle glisse le bâton vers le bord d'herbe.",
        "narrateur|L'herbe tient, sans laisser la poussière.",
        "narrateur|Nina souffle bas, une seule fois.",
        "narrateur|La larme de bronze luit, hors de l'allée.",
        "papa|Le bord n'a pas soulevé.",
        "enfant-f|Tu es à l'abri.",
        "narrateur|Le rond monte, lent, jusqu'au nez.",
        "maman|Tu as dit ça tout bas.",
    ],
    (1, 2, 1): [
        "enfant-f|On attend l'ombre.",
        "narrateur|Une ombre de tilleul glisse sur le nez.",
        "narrateur|Sous l'ombre, le bâton ne fond plus.",
        "narrateur|Le bronze se tait, puis se refroidit.",
        "narrateur|La larme de bronze redevient sombre, froide.",
        "maman|Le nez est redevenu doux.",
        "enfant-f|Maintenant, tu me vois.",
        "narrateur|Pendant ce temps, le bâton reste droit.",
        "papa|Tu as laissé l'ombre arriver.",
    ],
    (1, 2, 2): [
        "enfant-f|L'oiseau, d'abord, il est plus frais.",
        "narrateur|Elle pose d'abord le fil sur l'oiseau.",
        "narrateur|L'oiseau de bronze est à l'ombre, lui.",
        "narrateur|Le rond glisse, lent, vers la larme.",
        "narrateur|Un fil de savon cherche l'air, court.",
        "papa|Tu n'as pas soufflé trop fort.",
        "enfant-f|C'est pour toi.",
        "narrateur|La larme de bronze reçoit le rond, entier.",
        "maman|L'oiseau était plus frais, tu as vu.",
    ],
    (1, 2, 3): [
        "enfant-f|Tout près, contre le bronze.",
        "narrateur|Nina se glisse contre le socle.",
        "narrateur|Tout près, le bâton n'a plus d'air chaud.",
        "narrateur|La bulle n'a plus à voyager trop loin.",
        "narrateur|La larme de bronze est là, à un souffle.",
        "papa|Tu t'es mise tout près, contre le nez.",
        "enfant-f|Le nez est là.",
        "narrateur|Pendant ce temps, le bâton reste droit.",
        "maman|Tu t'es mise tout contre.",
    ],
    (1, 3, 1): [
        "enfant-f|On attend les feuilles, d'abord.",
        "narrateur|Elle tient le bâton, puis attend les feuilles.",
        "narrateur|Les feuilles vont, reviennent, puis se taisent.",
        "narrateur|L'air redevient un seul souffle, net.",
        "narrateur|La larme de bronze ne bouge plus, du tout.",
        "papa|Le tilleul n'a plus claqué.",
        "enfant-f|Maintenant, tu peux rester.",
        "narrateur|Pendant ce temps, le bâton reste droit.",
        "maman|Tu as laissé les feuilles finir.",
    ],
    (1, 3, 2): [
        "enfant-f|Derrière, pas trop près du vent.",
        "narrateur|Derrière le tronc, le bâton ne claque plus.",
        "narrateur|Nina se glisse derrière le tronc, tout bas.",
        "narrateur|Rien ne claque, rien ne pousse plus.",
        "narrateur|La larme de bronze se voit entre deux branches.",
        "papa|Tu n'as pas couru.",
        "enfant-f|Tu es ronde, maintenant.",
        "narrateur|Un fil de savon cherche l'air, abrité.",
        "maman|Derrière, l'air était plus doux.",
    ],
    (1, 3, 3): [
        "enfant-f|Tout petit, tout serré.",
        "narrateur|Une toute petite bulle quitte le bâton.",
        "narrateur|Nina souffle à peine, sans prendre le vent.",
        "narrateur|Le tilleul se tait, plus loin, tout seul.",
        "narrateur|La larme de bronze prend le petit rond.",
        "papa|Le petit rond n'a pas volé.",
        "enfant-f|Tu restes, bulle.",
        "narrateur|Un fil de savon cherche l'air, minuscule.",
        "maman|Le petit rond a suffi.",
    ],
    (2, 1, 1): [
        "enfant-f|On attend les pas.",
        "narrateur|Nina tient le savon, sans ouvrir.",
        "narrateur|Le gravier se tait, une fois, puis plus.",
        "narrateur|La larme de bronze redevient sombre, nette.",
        "enfant-f|Tu peux partir, maintenant.",
        "narrateur|Fermé, le savon attend contre son pouce.",
        "papa|Les pas se sont tus, là.",
        "narrateur|La goutte file, ronde, vers la larme.",
        "maman|Tu as laissé le gravier se taire.",
    ],
    (2, 1, 2): [
        "enfant-f|Plus bas, d'abord.",
        "narrateur|Elle baisse le savon, loin de la poussière.",
        "narrateur|Nina s'accroupit, les genoux au gravier.",
        "narrateur|L'air est plus doux, près de l'herbe.",
        "narrateur|La larme de bronze se voit d'en bas.",
        "enfant-f|Ici, tu ne crèves plus.",
        "papa|Tu as vu l'herbe, avant.",
        "narrateur|Une goutte de savon brille, prête à filer.",
        "maman|Près du sol, ça tenait mieux.",
    ],
    (2, 1, 3): [
        "enfant-f|Au bord, tout petit.",
        "narrateur|Elle glisse le savon vers le bord d'herbe.",
        "narrateur|L'herbe tient, sans laisser la poussière.",
        "narrateur|Nina ouvre le flacon, une seule goutte.",
        "narrateur|La larme de bronze luit, hors de l'allée.",
        "papa|Le bord n'a pas soulevé.",
        "enfant-f|Tu es à l'abri.",
        "narrateur|Le rond monte, lent, jusqu'au nez.",
        "maman|Tu as dit ça tout bas.",
    ],
    (2, 2, 1): [
        "enfant-f|On attend l'ombre.",
        "narrateur|Une ombre de tilleul glisse sur le nez.",
        "narrateur|Sous l'ombre, le savon ne sèche plus.",
        "narrateur|Le bronze se tait, puis se refroidit.",
        "narrateur|La larme de bronze redevient sombre, froide.",
        "maman|Le nez est redevenu doux.",
        "enfant-f|Maintenant, tu me vois.",
        "narrateur|Fermé, le savon attend contre son pouce.",
        "papa|Tu as laissé l'ombre arriver.",
    ],
    (2, 2, 2): [
        "enfant-f|L'oiseau, d'abord, il est plus frais.",
        "narrateur|Elle pose d'abord la goutte sur l'oiseau.",
        "narrateur|L'oiseau de bronze est à l'ombre, lui.",
        "narrateur|Le rond glisse, lent, vers la larme.",
        "narrateur|Une goutte de savon brille, courte.",
        "papa|Tu n'as pas soufflé trop fort.",
        "enfant-f|C'est pour toi.",
        "narrateur|La larme de bronze reçoit le rond, entier.",
        "maman|L'oiseau était plus frais, tu as vu.",
    ],
    (2, 2, 3): [
        "enfant-f|Tout près, contre le bronze.",
        "narrateur|Nina se glisse contre le socle.",
        "narrateur|Tout près, le savon n'a plus d'air chaud.",
        "narrateur|La bulle n'a plus à voyager trop loin.",
        "narrateur|La larme de bronze est là, à un souffle.",
        "papa|Tu t'es mise tout près, contre le nez.",
        "enfant-f|Le nez est là.",
        "narrateur|Fermé, le savon attend contre son pouce.",
        "maman|Tu t'es mise tout contre.",
    ],
    (2, 3, 1): [
        "enfant-f|On attend les feuilles, d'abord.",
        "narrateur|Elle tient le savon, puis attend les feuilles.",
        "narrateur|Les feuilles vont, reviennent, puis se taisent.",
        "narrateur|L'air redevient un seul souffle, net.",
        "narrateur|La larme de bronze ne bouge plus, du tout.",
        "papa|Le tilleul n'a plus claqué.",
        "enfant-f|Maintenant, tu peux rester.",
        "narrateur|Fermé, le savon attend contre son pouce.",
        "maman|Tu as laissé les feuilles finir.",
    ],
    (2, 3, 2): [
        "enfant-f|Derrière, pas trop près du vent.",
        "narrateur|Derrière le tronc, le savon ne s'envole plus.",
        "narrateur|Nina se glisse derrière le tronc, tout bas.",
        "narrateur|Rien ne claque, rien ne pousse plus.",
        "narrateur|La larme de bronze se voit entre deux branches.",
        "papa|Tu n'as pas couru.",
        "enfant-f|Tu es ronde, maintenant.",
        "narrateur|Une goutte de savon brille, abritée.",
        "maman|Derrière, l'air était plus doux.",
    ],
    (2, 3, 3): [
        "enfant-f|Tout petit, tout serré.",
        "narrateur|Une toute petite bulle quitte le savon.",
        "narrateur|Nina souffle à peine, sans prendre le vent.",
        "narrateur|Le tilleul se tait, plus loin, tout seul.",
        "narrateur|La larme de bronze prend le petit rond.",
        "papa|Le petit rond n'a pas volé.",
        "enfant-f|Tu restes, bulle.",
        "narrateur|Une goutte de savon brille, minuscule.",
        "maman|Le petit rond a suffi.",
    ],
    (3, 1, 1): [
        "enfant-f|On attend les pas.",
        "narrateur|Nina tient la coupelle, sans verser.",
        "narrateur|Le gravier se tait, une fois, puis plus.",
        "narrateur|La larme de bronze redevient sombre, nette.",
        "enfant-f|Tu peux partir, maintenant.",
        "narrateur|Plate, la coupelle attend, sans verser.",
        "papa|Les pas se sont tus, là.",
        "narrateur|Le miroir file, rond, vers la larme.",
        "maman|Tu as laissé le gravier se taire.",
    ],
    (3, 1, 2): [
        "enfant-f|Plus bas, d'abord.",
        "narrateur|Elle baisse la coupelle, loin de la poussière.",
        "narrateur|Nina s'accroupit, les genoux au gravier.",
        "narrateur|L'air est plus doux, près de l'herbe.",
        "narrateur|La larme de bronze se voit d'en bas.",
        "enfant-f|Ici, tu ne crèves plus.",
        "papa|Tu as vu l'herbe, avant.",
        "narrateur|Le rond de savon attend, plat, bas.",
        "maman|Près du sol, ça tenait mieux.",
    ],
    (3, 1, 3): [
        "enfant-f|Au bord, tout petit.",
        "narrateur|Elle glisse la coupelle vers le bord d'herbe.",
        "narrateur|L'herbe tient, sans laisser la poussière.",
        "narrateur|Nina penche le bol, une seule fois.",
        "narrateur|La larme de bronze luit, hors de l'allée.",
        "papa|Le bord n'a pas soulevé.",
        "enfant-f|Tu es à l'abri.",
        "narrateur|Le rond monte, lent, jusqu'au nez.",
        "maman|Tu as dit ça tout bas.",
    ],
    (3, 2, 1): [
        "enfant-f|On attend l'ombre.",
        "narrateur|Une ombre de tilleul glisse sur le nez.",
        "narrateur|Sous l'ombre, la coupelle ne fume plus.",
        "narrateur|Le bronze se tait, puis se refroidit.",
        "narrateur|La larme de bronze redevient sombre, froide.",
        "maman|Le nez est redevenu doux.",
        "enfant-f|Maintenant, tu me vois.",
        "narrateur|Plate, la coupelle attend, sans verser.",
        "papa|Tu as laissé l'ombre arriver.",
    ],
    (3, 2, 2): [
        "enfant-f|L'oiseau, d'abord, il est plus frais.",
        "narrateur|Elle pose d'abord le rond sur l'oiseau.",
        "narrateur|L'oiseau de bronze est à l'ombre, lui.",
        "narrateur|Le rond glisse, lent, vers la larme.",
        "narrateur|Le rond de savon attend, court.",
        "papa|Tu n'as pas soufflé trop fort.",
        "enfant-f|C'est pour toi.",
        "narrateur|La larme de bronze reçoit le rond, entier.",
        "maman|L'oiseau était plus frais, tu as vu.",
    ],
    (3, 2, 3): [
        "enfant-f|Tout près, contre le bronze.",
        "narrateur|Nina se glisse contre le socle.",
        "narrateur|Tout près, la coupelle n'a plus d'air chaud.",
        "narrateur|La bulle n'a plus à voyager trop loin.",
        "narrateur|La larme de bronze est là, à un souffle.",
        "papa|Tu t'es mise tout près, contre le nez.",
        "enfant-f|Le nez est là.",
        "narrateur|Plate, la coupelle attend, sans verser.",
        "maman|Tu t'es mise tout contre.",
    ],
    (3, 3, 1): [
        "enfant-f|On attend les feuilles, d'abord.",
        "narrateur|Elle tient la coupelle, puis attend les feuilles.",
        "narrateur|Les feuilles vont, reviennent, puis se taisent.",
        "narrateur|L'air redevient un seul souffle, net.",
        "narrateur|La larme de bronze ne bouge plus, du tout.",
        "papa|Le tilleul n'a plus claqué.",
        "enfant-f|Maintenant, tu peux rester.",
        "narrateur|Plate, la coupelle attend, sans verser.",
        "maman|Tu as laissé les feuilles finir.",
    ],
    (3, 3, 2): [
        "enfant-f|Derrière, pas trop près du vent.",
        "narrateur|Derrière le tronc, la coupelle ne se plie plus.",
        "narrateur|Nina se glisse derrière le tronc, tout bas.",
        "narrateur|Rien ne claque, rien ne pousse plus.",
        "narrateur|La larme de bronze se voit entre deux branches.",
        "papa|Tu n'as pas couru.",
        "enfant-f|Tu es ronde, maintenant.",
        "narrateur|Le rond de savon attend, abrité.",
        "maman|Derrière, l'air était plus doux.",
    ],
    (3, 3, 3): [
        "enfant-f|Tout petit, tout serré.",
        "narrateur|Une toute petite bulle quitte la coupelle.",
        "narrateur|Nina souffle à peine, sans prendre le vent.",
        "narrateur|Le tilleul se tait, plus loin, tout seul.",
        "narrateur|La larme de bronze prend le petit rond.",
        "papa|Le petit rond n'a pas volé.",
        "enfant-f|Tu restes, bulle.",
        "narrateur|Le rond de savon attend, minuscule.",
        "maman|Le petit rond a suffi.",
    ],
}

END_SONS = {1: "bulle,gravier", 2: "bulle,bronze", 3: "bulle,tilleul"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|La bulle se pose, ronde, sur le nez de bronze.",
        "enfant-f|On a attendu les pas.",
        "papa|Le gravier s'est tu, pour toi.",
        "maman|La cloche n'a pas sonné.",
        "narrateur|Le bâton sèche près du savon, un fil collant.",
        "narrateur|Un fil de savon sèche sur le bois, près du bronze.",
    ],
    (1, 1, 2): [
        "narrateur|Plus bas, la bulle monte jusqu'au nez.",
        "enfant-f|On s'est baissées, d'abord.",
        "papa|Tu as vu l'herbe avant de souffler.",
        "maman|Essuie tes genoux, on rentre.",
        "narrateur|Le bâton sèche près du savon, un fil collant.",
        "narrateur|Un rond d'herbe reste collé au bas du socle.",
    ],
    (1, 1, 3): [
        "narrateur|Du bord d'herbe, la bulle rejoint le nez.",
        "enfant-f|Je suis restée sur l'herbe.",
        "papa|Le bord n'a pas soulevé.",
        "maman|L'herbe est retombée, plus loin.",
        "narrateur|Le bâton sèche près du savon, un fil collant.",
        "narrateur|L'allée garde un cercle de savon, loin de la larme.",
    ],
    (1, 2, 1): [
        "narrateur|Quand l'ombre a touché, la bulle a tenu.",
        "enfant-f|On a attendu le tilleul.",
        "papa|L'ombre vous a aidées.",
        "maman|Le bronze sent le soleil, moins fort.",
        "narrateur|Le bâton sèche près du savon, un fil collant.",
        "narrateur|L'ombre du tilleul glisse, et la larme tient.",
    ],
    (1, 2, 2): [
        "narrateur|De l'oiseau au nez, la bulle a glissé.",
        "enfant-f|On a commencé par l'oiseau.",
        "papa|Tu n'as pas soufflé trop fort.",
        "maman|L'oiseau était plus frais, d'abord.",
        "narrateur|Le bâton sèche près du savon, un fil collant.",
        "narrateur|L'oiseau de bronze garde un halo, sous la bulle.",
    ],
    (1, 2, 3): [
        "narrateur|Tout près, la bulle touche le nez.",
        "enfant-f|Je me suis mise tout près.",
        "papa|Tu t'es glissée, comme l'ombre.",
        "maman|Vos mains sentent le savon.",
        "narrateur|Le bâton sèche près du savon, un fil collant.",
        "narrateur|Ses genoux gardent la chaleur du socle, un moment.",
    ],
    (1, 3, 1): [
        "narrateur|Quand les feuilles se sont tues, la bulle a tenu.",
        "enfant-f|On a attendu le tilleul.",
        "papa|Le tilleul n'a plus claqué.",
        "maman|Vos manches sentent le tilleul.",
        "narrateur|Le bâton sèche près du savon, un fil collant.",
        "narrateur|Une feuille jaune s'arrête au pied du bronze.",
    ],
    (1, 3, 2): [
        "narrateur|Derrière le tronc, la bulle rejoint le nez.",
        "enfant-f|On n'est pas allées trop au vent.",
        "papa|Tu n'as pas couru.",
        "maman|Tes doigts sentent le savon.",
        "narrateur|Le bâton sèche près du savon, un fil collant.",
        "narrateur|L'écorce du tilleul sent le savon, tout bas.",
    ],
    (1, 3, 3): [
        "narrateur|Tout petit, le rond tient sur le nez.",
        "enfant-f|On a soufflé à peine.",
        "papa|Le petit rond n'a pas volé.",
        "maman|Le savon est sec, on rentre.",
        "narrateur|Le bâton sèche près du savon, un fil collant.",
        "narrateur|Le petit rond pâlit, sans quitter la larme.",
    ],
    (2, 1, 1): [
        "narrateur|La bulle se pose, ronde, sur le nez de bronze.",
        "enfant-f|On a attendu les pas.",
        "papa|Le gravier s'est tu, pour toi.",
        "maman|La cloche n'a pas sonné.",
        "narrateur|Le flacon reste fermé, une goutte au bouchon.",
        "narrateur|Une goutte reste au bouchon, face à la larme.",
    ],
    (2, 1, 2): [
        "narrateur|Plus bas, la bulle monte jusqu'au nez.",
        "enfant-f|On s'est baissées, d'abord.",
        "papa|Tu as vu l'herbe avant de souffler.",
        "maman|Essuie tes genoux, on rentre.",
        "narrateur|Le flacon reste fermé, une goutte au bouchon.",
        "narrateur|Le flacon penche dans l'herbe, bouchon fermé.",
    ],
    (2, 1, 3): [
        "narrateur|Du bord d'herbe, la bulle rejoint le nez.",
        "enfant-f|Je suis restée sur l'herbe.",
        "papa|Le bord n'a pas soulevé.",
        "maman|L'herbe est retombée, plus loin.",
        "narrateur|Le flacon reste fermé, une goutte au bouchon.",
        "narrateur|Le savon a laissé un ovale au bord de l'allée.",
    ],
    (2, 2, 1): [
        "narrateur|Quand l'ombre a touché, la bulle a tenu.",
        "enfant-f|On a attendu le tilleul.",
        "papa|L'ombre vous a aidées.",
        "maman|Le bronze sent le soleil, moins fort.",
        "narrateur|Le flacon reste fermé, une goutte au bouchon.",
        "narrateur|Le bronze tiède ne fume plus sous l'ombre.",
    ],
    (2, 2, 2): [
        "narrateur|De l'oiseau au nez, la bulle a glissé.",
        "enfant-f|On a commencé par l'oiseau.",
        "papa|Tu n'as pas soufflé trop fort.",
        "maman|L'oiseau était plus frais, d'abord.",
        "narrateur|Le flacon reste fermé, une goutte au bouchon.",
        "narrateur|L'oiseau tient un reflet de savon, minuscule.",
    ],
    (2, 2, 3): [
        "narrateur|Tout près, la bulle touche le nez.",
        "enfant-f|Je me suis mise tout près.",
        "papa|Tu t'es glissée, comme l'ombre.",
        "maman|Vos mains sentent le savon.",
        "narrateur|Le flacon reste fermé, une goutte au bouchon.",
        "narrateur|Le flacon colle à sa manche, face au socle.",
    ],
    (2, 3, 1): [
        "narrateur|Quand les feuilles se sont tues, la bulle a tenu.",
        "enfant-f|On a attendu le tilleul.",
        "papa|Le tilleul n'a plus claqué.",
        "maman|Vos manches sentent le tilleul.",
        "narrateur|Le flacon reste fermé, une goutte au bouchon.",
        "narrateur|Une feuille s'immobilise, loin du flacon.",
    ],
    (2, 3, 2): [
        "narrateur|Derrière le tronc, la bulle rejoint le nez.",
        "enfant-f|On n'est pas allées trop au vent.",
        "papa|Tu n'as pas couru.",
        "maman|Tes doigts sentent le savon.",
        "narrateur|Le flacon reste fermé, une goutte au bouchon.",
        "narrateur|Derrière le tronc, le savon ne tremble plus.",
    ],
    (2, 3, 3): [
        "narrateur|Tout petit, le rond tient sur le nez.",
        "enfant-f|On a soufflé à peine.",
        "papa|Le petit rond n'a pas volé.",
        "maman|Le savon est sec, on rentre.",
        "narrateur|Le flacon reste fermé, une goutte au bouchon.",
        "narrateur|Une toute petite goutte sèche sur la larme.",
    ],
    (3, 1, 1): [
        "narrateur|La bulle se pose, ronde, sur le nez de bronze.",
        "enfant-f|On a attendu les pas.",
        "papa|Le gravier s'est tu, pour toi.",
        "maman|La cloche n'a pas sonné.",
        "narrateur|La coupelle sèche près du gravier, un cercle de savon.",
        "narrateur|La coupelle sèche près du gravier, un cercle net.",
    ],
    (3, 1, 2): [
        "narrateur|Plus bas, la bulle monte jusqu'au nez.",
        "enfant-f|On s'est baissées, d'abord.",
        "papa|Tu as vu l'herbe avant de souffler.",
        "maman|Essuie tes genoux, on rentre.",
        "narrateur|La coupelle sèche près du gravier, un cercle de savon.",
        "narrateur|Un miroir de savon reste au fond de la coupelle.",
    ],
    (3, 1, 3): [
        "narrateur|Du bord d'herbe, la bulle rejoint le nez.",
        "enfant-f|Je suis restée sur l'herbe.",
        "papa|Le bord n'a pas soulevé.",
        "maman|L'herbe est retombée, plus loin.",
        "narrateur|La coupelle sèche près du gravier, un cercle de savon.",
        "narrateur|L'herbe a pris un rond, au bord de l'allée.",
    ],
    (3, 2, 1): [
        "narrateur|Quand l'ombre a touché, la bulle a tenu.",
        "enfant-f|On a attendu le tilleul.",
        "papa|L'ombre vous a aidées.",
        "maman|Le bronze sent le soleil, moins fort.",
        "narrateur|La coupelle sèche près du gravier, un cercle de savon.",
        "narrateur|La coupelle se tait à l'ombre, contre le socle.",
    ],
    (3, 2, 2): [
        "narrateur|De l'oiseau au nez, la bulle a glissé.",
        "enfant-f|On a commencé par l'oiseau.",
        "papa|Tu n'as pas soufflé trop fort.",
        "maman|L'oiseau était plus frais, d'abord.",
        "narrateur|La coupelle sèche près du gravier, un cercle de savon.",
        "narrateur|L'oiseau voit le rond, collé à la larme.",
    ],
    (3, 2, 3): [
        "narrateur|Tout près, la bulle touche le nez.",
        "enfant-f|Je me suis mise tout près.",
        "papa|Tu t'es glissée, comme l'ombre.",
        "maman|Vos mains sentent le savon.",
        "narrateur|La coupelle sèche près du gravier, un cercle de savon.",
        "narrateur|La coupelle reste plate, tout contre le bronze.",
    ],
    (3, 3, 1): [
        "narrateur|Quand les feuilles se sont tues, la bulle a tenu.",
        "enfant-f|On a attendu le tilleul.",
        "papa|Le tilleul n'a plus claqué.",
        "maman|Vos manches sentent le tilleul.",
        "narrateur|La coupelle sèche près du gravier, un cercle de savon.",
        "narrateur|Les feuilles se taisent, au-dessus de la coupelle.",
    ],
    (3, 3, 2): [
        "narrateur|Derrière le tronc, la bulle rejoint le nez.",
        "enfant-f|On n'est pas allées trop au vent.",
        "papa|Tu n'as pas couru.",
        "maman|Tes doigts sentent le savon.",
        "narrateur|La coupelle sèche près du gravier, un cercle de savon.",
        "narrateur|Derrière le tronc, la coupelle n'a pas versé.",
    ],
    (3, 3, 3): [
        "narrateur|Tout petit, le rond tient sur le nez.",
        "enfant-f|On a soufflé à peine.",
        "papa|Le petit rond n'a pas volé.",
        "maman|Le savon est sec, on rentre.",
        "narrateur|La coupelle sèche près du gravier, un cercle de savon.",
        "narrateur|Un tout petit miroir dort au fond, sous la larme.",
    ],
}


def t2_question(t1: int) -> list[str]:
    return [f"narrateur|{T1[t1]['voy']}"] + T2_Q[1]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "enfants_parc,bronze",
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le bâton", "le savon", "la coupelle")},
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
            {"fields": t3lab("l'allée", "le socle", "le tilleul")},
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
                    {"emphasis": "larme de bronze"},
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
        "plus de temps ou de calme",
        "la première",
        "la deuxième",
        "la troisième",
        "bravo tu as",
        "bon travail",
        "kenzo",
        "sami",
        "léa",
        "lea ",
        "tom ",
        "bac à sable",
        "toboggan",
        "balançoire",
        "capitaine",
        "plic",
        "volet jaune",
        "il faut attendre",
        "escargot",
        "balcon",
        "veau",
        "étable",
        "abreuvoir",
        "le four",
        "marché",
        "fort de coussins",
        "moulinet",
        "carrousel",
        "marelle",
        "zoé",
        "zoe",
        "canard",
        "mare",
        "miel",
        "merle",
        "tout doux",
        "tout calme",
        "j'ai compris",
        "mission accomplie",
        "aujourd'hui,",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if TIC_WORDS.search(blob):
        raise SystemExit(f"{SID} tic encore/déjà")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "nina" not in blob:
        raise SystemExit(f"{SID}: Nina absente")
    if "larme de bronze" not in blob:
        raise SystemExit(f"{SID}: larme de bronze absente")
    if "bulle" not in blob:
        raise SystemExit(f"{SID}: bulle absente")

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
        "- **Leçon :** DIF.BES.001 — plus de temps ou de calme (vécue, non dite)\n"
        "- **Personnages :** Nina, papa, maman (un seul enfant)\n"
        "- **Lieu :** parc du village : allée, statue de bronze, tilleul\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Dans le sac, le bâton cogne la coupelle. Nina veut poser une bulle "
        "sur la **larme de bronze** du nez, **avant la cloche**. Maman veut marcher "
        "d'abord ; Nina veut souffler maintenant. Première idée trop vite : le fil casse. "
        "Elle prend le bâton, le savon ou la coupelle ; les trois viennent. "
        "L'allée soulève, le socle brûle, le tilleul claque. Une 2e ruse "
        "(pas tardif, soleil qui revient, souffle tardif) : elle refuse de foncer, "
        "regarde la larme du début. Neuf façons de laisser l'air se taire. "
        "La bulle tient sur la larme. Monde ≠ TREE-DIF-043 (mare, canards).\n\n"
        "## Vécu\n\n"
        "Nina veut la bulle **maintenant**. Papa et maman veulent marcher. "
        "Poussière, chaleur, vent. Sourire disparu, poitrine bousculée, adulte accroupi. "
        "Chaque choix change l'obstacle et le climax. La leçon se voit : "
        "souffler trop tôt crève ; attendre les pas, se baisser, le bord, "
        "l'ombre, l'oiseau, tout près, les feuilles, derrière, tout petit. "
        "Indice d'ouverture payé : larme de bronze. Fin : bulle + trace unique "
        "(fil, herbe, ovale, halo, écorce, miroir).\n\n"
        "## Vu et corrigé\n\n"
        "- Slogan « Plus de temps ou de calme », Zoé, Tom/Léa/Sami, bac/toboggan, "
        "miel, merle, canards/mare, « bon travail » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (goutte essuyée). Question d'adulte. Un « en ce moment ».\n"
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
