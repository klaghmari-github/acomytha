#!/usr/bin/env python3
"""TREE-DIF-032 — F-NAR-019 example4 v2. Cabane de Victorina, drap à pois. N3. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-032"
N3 = 16
TITLE = "La cabane de Victorina, sous le drap à pois"
FIL = (
    "La gouttière recopie les pois sur le carreau. Victorina veut une vraie cabane "
    "sous le drap à pois, avec la lampe et le coussin rond, pendant la pluie. "
    "Un pois ivoire cligne. Raphaël veut sauter : pas la même chose, pas le même moment. "
    "Elle jette trop vite : le drap glisse, le pois se cache. "
    "T1 = drap / lampe / coussin ; les trois partent. "
    "T2 = sous le lit, entre l'armoire, près de la fenêtre. "
    "T3 = neuf façons d'inventer un toit à deux tailles. Le pois ivoire revient."
)
CHARS = "Victorina, Raphaël, papa, maman"
SETTING = "chambre sous la pluie : lit, armoire, fenêtre"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "pois ivoire",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=la_pluie_écrit_des_pois_Victorina_veut_sa_cabane; tempo=naturel; sourire=léger; respiration=ample",
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
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_elle_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "pois ivoire",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=deux_rythmes_un_même_toit; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=jeter_le_drap_trop_vite_ne_suffit_pas; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "slow", "wpm": 124, "speed": 0.88, "piper": 1.24,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=ils_ne_veulent_pas_la_même_chose; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": "pois ivoire",
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=le_pois_ivoire_paie_le_début; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "pois ivoire",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_cabane_a_failli_ne_pas_arriver; tempo=posé; sourire=léger; respiration=ample",
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
        low = ph.lower()
        for tic in TIC_PHRASES:
            if tic in low:
                raise SystemExit(f"tic {tic!r}: {ph}")
        found = TIC_WORDS.search(low)
        if found:
            raise SystemExit(f"tic {found.group(0)!r}: {ph}")
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


OPENING = [
    "narrateur|La gouttière recopie les pois sur le carreau.",
    "narrateur|Victorina compte les gouttes, sur ses doigts.",
    "narrateur|Le tapis sent le savon, un peu humide.",
    "narrateur|Le drap à pois attend sur le lit.",
    "enfant-f|Il a un pois ivoire, plus clair.",
    "papa|Tu as vu ce pois, Victorina ?",
    "enfant-f|Il cligne, quand la pluie tape.",
    "maman|La lampe et le coussin rond attendent.",
    "narrateur|En ce moment, Victorina touche le tissu.",
    "enfant-f|Je veux une vraie cabane, ici, sous le drap.",
    "narrateur|Raphaël arrive, plus grand qu'elle.",
    "narrateur|Ses épaules montent jusqu'à la poignée.",
    "copain|On saute sur le lit, maintenant !",
    "enfant-f|Non, une cabane, pas un saut.",
    "narrateur|Elle jette le drap sur eux, trop vite.",
    "narrateur|Les genoux de Raphaël heurtent le matelas.",
    "narrateur|Le drap glisse, trop large pour deux.",
    "narrateur|Le pois ivoire se cache dans un pli.",
    "enfant-f|Oh.",
    "narrateur|Le sourire de Victorina disparaît.",
    "narrateur|L'envie et l'inquiétude se bousculent, dans sa poitrine.",
    "papa|Il s'accroupit, à la même hauteur.",
    "papa|Tu le prends comment, ce drap ?",
    "narrateur|Elle rattrape le coin du drap.",
    "papa|Merci, tu tiens le coin.",
    "maman|On prépare la cabane, alors ?",
]

T1_CHOICE = [
    "narrateur|Trois affaires attendent près du lit.",
    "narrateur|Le drap à pois, la lampe, le coussin rond.",
    "narrateur|Les trois voyagent, pour la cabane.",
    "maman|Tu prends quoi d'abord, Victorina ?",
]

T1 = {
    1: {
        "lab": "le drap à pois",
        "sons": "tissu,pluie",
        "emphasis": "drap à pois",
        "passage": [
            "narrateur|Victorina enroule le drap à pois, autour d'elle.",
            "enfant-f|Il sent le savon, et la pluie.",
            "maman|Glisse-le autour de tes épaules.",
            "narrateur|Les pois froissent contre le pull.",
            "papa|La lampe, ensuite, dans la poche.",
            "narrateur|Raphaël prend le coussin rond.",
            "narrateur|Les trois affaires partent, dans la pièce.",
            "copain|On saute, Victorina !",
            "enfant-f|Raphaël, viens près du lit.",
            "narrateur|Il s'arrête, les genoux trop hauts.",
            "copain|J'arrive, mais je veux sauter.",
            "enfant-f|La cabane, pas le saut.",
            "papa|Le drap d'abord, vous l'avez.",
            "narrateur|Le pois ivoire cligne, puis se cache.",
        ],
        "question": [
            "narrateur|Victorina a mis le drap à pois autour des épaules.",
            "maman|C'est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "épaules",
            "accepted_examples": "épaules | les épaules | autour des épaules | sur les épaules",
            "retry_prompt": "Le drap est autour des épaules. C'est où ?",
        },
        "confirm": [
            "narrateur|Les épaules portent le drap, contre le pull.",
            "copain|Il a trop de pois !",
            "enfant-f|C'est pour notre cabane.",
            "narrateur|Raphaël a les genoux plus hauts que Victorina.",
            "narrateur|Ses pieds touchent le bas du lit.",
            "maman|Ses genoux dépassent le sommier.",
            "papa|On reste dans la chambre ?",
            "enfant-f|Oui, papa.",
            "narrateur|Le pois ivoire attend, dans un pli.",
            "copain|Je le cherche, plus tard.",
        ],
    },
    2: {
        "lab": "la lampe de poche",
        "sons": "clic,pluie",
        "emphasis": "lampe de poche",
        "passage": [
            "narrateur|Victorina prend la lampe de poche, un peu froide.",
            "enfant-f|Elle fait un rond, sur le mur.",
            "papa|Glisse-la dans ta poche, tout droit.",
            "narrateur|Un clic, puis une petite lumière.",
            "maman|Le drap, ensuite, autour des épaules.",
            "narrateur|Raphaël prend le coussin rond.",
            "narrateur|Les trois affaires partent, dans la pièce.",
            "copain|On fait des monstres, avec le rond !",
            "enfant-f|Non, une cabane, avec la lumière.",
            "narrateur|Il s'arrête, une mèche trop haute.",
            "copain|Moi je veux les ombres.",
            "enfant-f|Raphaël, viens près du lit.",
            "maman|La lampe d'abord, elle est prête.",
            "narrateur|Le pois ivoire cligne, dans le rond.",
        ],
        "question": [
            "narrateur|Victorina a glissé la lampe de poche.",
            "papa|Elle est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "poche",
            "accepted_examples": "poche | la poche | dans la poche | sa poche",
            "retry_prompt": "La lampe est dans la poche. Elle est où ?",
        },
        "confirm": [
            "narrateur|La poche veille près de la lampe.",
            "copain|Je vois le rond !",
            "enfant-f|Ne l'allume pas tout de suite.",
            "narrateur|Raphaël a les cheveux trop courts, trop hauts.",
            "narrateur|Une mèche saute quand il se baisse.",
            "papa|Ça sent le savon, sur le drap.",
            "maman|Vos mains, au-dessus du coussin ?",
            "copain|Oui, maman.",
            "narrateur|Le pois ivoire attend, hors du rond.",
            "enfant-f|On le retrouve, dans la cabane.",
        ],
    },
    3: {
        "lab": "le coussin rond",
        "sons": "tissu,pouf",
        "emphasis": "coussin rond",
        "passage": [
            "narrateur|Victorina tire le coussin rond, un peu rêche.",
            "enfant-f|Il est tiède, sous mon bras.",
            "maman|Serre-le, pour le voyage.",
            "narrateur|Le tissu fait un petit pouf.",
            "papa|Le drap et la lampe, avec vous.",
            "narrateur|Il les pose près des chaussettes.",
            "narrateur|Les trois affaires partent, dans la pièce.",
            "copain|On le lance, Victorina !",
            "enfant-f|Non, c'est le siège de la cabane.",
            "narrateur|Une ombre trop longue passe au seuil.",
            "copain|Moi je veux le lancer.",
            "enfant-f|Raphaël, je te garde un coin.",
            "papa|Le coussin d'abord, il est prêt.",
            "narrateur|Le pois ivoire cligne, contre le pouf.",
        ],
        "question": [
            "narrateur|Victorina serre le coussin rond.",
            "maman|Il est où, maintenant ?",
        ],
        "qfields": {
            "expected_answer": "bras",
            "accepted_examples": "bras | le bras | sous le bras | son bras | sous son bras",
            "retry_prompt": "Le coussin est sous le bras. Il est où ?",
        },
        "confirm": [
            "narrateur|Le coussin rond cache le coude.",
            "copain|Ça sent le savon.",
            "enfant-f|Le coin de départ est là.",
            "narrateur|Le pull de Raphaël s'arrête trop haut.",
            "narrateur|Les manches laissent ses poignets libres.",
            "maman|La chambre est tiède, autour.",
            "papa|On y va, tous les quatre ?",
            "enfant-f|Oui.",
            "narrateur|Le pois ivoire attend, sous un pli.",
            "copain|Je le cherche, avec toi.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le drap à pois attend, un peu froissé.",
        "narrateur|Sous le lit, l'ombre est basse.",
        "narrateur|Entre l'armoire, le passage est étroit.",
        "narrateur|Près de la fenêtre, le carreau clignote.",
        "papa|On commence où, pour la cabane ?",
    ],
    2: [
        "narrateur|La lampe de poche attend, dans la poche.",
        "narrateur|Sous le lit, l'ombre est basse.",
        "narrateur|Entre l'armoire, le passage est étroit.",
        "narrateur|Près de la fenêtre, le carreau clignote.",
        "maman|On commence où, pour la cabane ?",
    ],
    3: [
        "narrateur|Le coussin rond attend, sous le bras.",
        "narrateur|Sous le lit, l'ombre est basse.",
        "narrateur|Entre l'armoire, le passage est étroit.",
        "narrateur|Près de la fenêtre, le carreau clignote.",
        "papa|On commence où, pour la cabane ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "bois,pluie",
        "emphasis": "pois ivoire",
        "passage": [
            "narrateur|Le drap accroche une latte, trop bas.",
            "narrateur|Le dessous du lit sent le bois chaud.",
            "copain|Moi je rentre, Victorina !",
            "narrateur|Raphaël se baisse, trop vite.",
            "narrateur|Ses épaules butent contre le bois.",
            "enfant-f|Le pois ivoire, il est coincé !",
            "copain|Je tire, fort !",
            "enfant-f|Non, on ne fonce pas.",
            "narrateur|Elle refuse, les mains sur le tissu.",
            "narrateur|Elle écoute la gouttière, six tapes.",
            "narrateur|Elle cherche le pois ivoire, du regard.",
            "papa|Il s'accroupit, à leur hauteur.",
            "maman|Le bois est trop bas, pour lui.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 1): {
        "sons": "bois,clic",
        "emphasis": "pois ivoire",
        "passage": [
            "narrateur|La lampe tape une latte, toc.",
            "narrateur|Un rond de lumière danse sous le sommier.",
            "copain|Moi je rentre, avec le rond !",
            "narrateur|Raphaël rampe, trop vite.",
            "narrateur|Le clic s'éteint, contre le bois.",
            "enfant-f|Le pois ivoire, je ne le vois plus !",
            "copain|Je reclique, tout de suite !",
            "enfant-f|Non, on ne fonce pas.",
            "narrateur|Elle refuse, la lampe contre sa poche.",
            "narrateur|Elle écoute la gouttière, six tapes.",
            "narrateur|Elle cherche le pois ivoire, dans l'ombre.",
            "maman|Elle s'accroupit, à leur hauteur.",
            "papa|Le bois est trop bas, pour lui.",
            "maman|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 1): {
        "sons": "bois,tissu",
        "emphasis": "pois ivoire",
        "passage": [
            "narrateur|Le coussin bute contre une latte.",
            "narrateur|Le tissu du coussin prend la poussière.",
            "copain|Moi je pousse le pouf, dessous !",
            "narrateur|Raphaël pousse, trop fort.",
            "narrateur|Ses épaules se coincent, sous le bois.",
            "enfant-f|Le pois ivoire, sous le coussin !",
            "copain|Je pousse, plus fort !",
            "enfant-f|Non, on ne fonce pas.",
            "narrateur|Elle refuse, une main sur le pouf.",
            "narrateur|Elle écoute la gouttière, six tapes.",
            "narrateur|Elle cherche le pois ivoire, au bord.",
            "papa|Il s'accroupit, à leur hauteur.",
            "maman|Le bois est trop bas, pour lui.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 2): {
        "sons": "bois,charniere",
        "emphasis": "pois ivoire",
        "passage": [
            "narrateur|Le drap se coince entre le bois et le mur.",
            "enfant-f|Le couloir est à nous, Raphaël.",
            "copain|Je me glisse, trop large !",
            "narrateur|Ses coudes frottent le bois, des deux côtés.",
            "narrateur|Les pois froissent, puis s'arrêtent.",
            "enfant-f|Le pois ivoire, dans la charnière !",
            "copain|Je tire le drap, fort !",
            "enfant-f|Non, on ne fonce pas.",
            "narrateur|Elle refuse, le tissu contre sa joue.",
            "narrateur|Elle écoute la gouttière, six tapes.",
            "narrateur|Elle cherche le pois ivoire, au gond.",
            "maman|Elle s'accroupit, à leur hauteur.",
            "papa|Ses épaules sont trop larges, ici.",
            "papa|Vous trouvez, tous les deux ?",
        ],
    },
    (2, 2): {
        "sons": "bois,clic",
        "emphasis": "pois ivoire",
        "passage": [
            "narrateur|La lampe glisse, trop vite, dans le passage.",
            "enfant-f|Le couloir est à nous, Raphaël.",
            "copain|Je me glisse, trop large !",
            "narrateur|Ses coudes frottent le bois, des deux côtés.",
            "narrateur|Le clic de la lampe se perd, au fond.",
            "enfant-f|Le pois ivoire, dans l'ombre de la porte !",
            "copain|Je force, j'entre !",
            "enfant-f|Non, on ne fonce pas.",
            "narrateur|Elle refuse, le clic dans sa poche.",
            "narrateur|Elle écoute la gouttière, six tapes.",
            "narrateur|Elle cherche le pois ivoire, près du gond.",
            "papa|Il s'accroupit, à leur hauteur.",
            "maman|Ses épaules sont trop larges, ici.",
            "maman|Vous trouvez, tous les deux ?",
        ],
    },
    (3, 2): {
        "sons": "bois,tissu",
        "emphasis": "pois ivoire",
        "passage": [
            "narrateur|Le coussin se plie, coincé, contre l'armoire.",
            "enfant-f|Le couloir est à nous, Raphaël.",
            "copain|Je me glisse, trop large !",
            "narrateur|Ses coudes frottent le bois, des deux côtés.",
            "narrateur|Un peu de laine reste collée au bois.",
            "enfant-f|Le pois ivoire, sous le coussin plié !",
            "copain|Je pousse le pouf, fort !",
            "enfant-f|Non, on ne fonce pas.",
            "narrateur|Elle refuse, le pouf contre son ventre.",
            "narrateur|Elle écoute la gouttière, six tapes.",
            "narrateur|Elle cherche le pois ivoire, sous la laine.",
            "maman|Elle s'accroupit, à leur hauteur.",
            "papa|Ses épaules sont trop larges, ici.",
            "papa|Vous trouvez, tous les deux ?",
        ],
    },
    (1, 3): {
        "sons": "pluie,vitre",
        "emphasis": "pois ivoire",
        "passage": [
            "narrateur|Le drap pèse, vers le carreau mouillé.",
            "enfant-f|Ici, ça clignote, Raphaël.",
            "copain|Je touche le rideau, tout haut !",
            "narrateur|La tringle reste trop loin pour Victorina.",
            "narrateur|Les pois restent trop bas, sous la tringle.",
            "enfant-f|Le pois ivoire, il ne regarde plus la pluie !",
            "copain|Je tire la tringle, fort !",
            "enfant-f|Non, on ne fonce pas.",
            "narrateur|Elle refuse, le coin du drap au poing.",
            "narrateur|Elle écoute la gouttière, six tapes.",
            "narrateur|Elle cherche le pois ivoire, au bas.",
            "papa|Il s'accroupit, à leur hauteur.",
            "maman|Ses bras vont jusqu'à la tringle.",
            "papa|Vous accrochez comment, tous les deux ?",
        ],
    },
    (2, 3): {
        "sons": "pluie,clic",
        "emphasis": "pois ivoire",
        "passage": [
            "narrateur|La lampe dessine un rond sur le rideau.",
            "enfant-f|Ici, ça clignote, Raphaël.",
            "copain|Je monte, je vois la pluie !",
            "narrateur|La tringle reste trop loin pour Victorina.",
            "narrateur|Le rond n'atteint pas le ciel.",
            "enfant-f|Le pois ivoire, hors du rond !",
            "copain|Je grimpe sur le rebord !",
            "enfant-f|Non, on ne fonce pas.",
            "narrateur|Elle refuse, la lampe baissée.",
            "narrateur|Elle écoute la gouttière, six tapes.",
            "narrateur|Elle cherche le pois ivoire, au bas du rideau.",
            "maman|Elle s'accroupit, à leur hauteur.",
            "papa|Ses bras vont jusqu'à la tringle.",
            "maman|Vous accrochez comment, tous les deux ?",
        ],
    },
    (3, 3): {
        "sons": "pluie,tissu",
        "emphasis": "pois ivoire",
        "passage": [
            "narrateur|Le coussin roule vers le rebord froid.",
            "enfant-f|Ici, ça clignote, Raphaël.",
            "copain|Je saute sur le pouf, je vois tout !",
            "narrateur|La tringle reste trop loin pour Victorina.",
            "narrateur|Le coussin n'aide pas, tout seul, trop bas.",
            "enfant-f|Le pois ivoire, par terre !",
            "copain|Je rebondis, plus haut !",
            "enfant-f|Non, on ne fonce pas.",
            "narrateur|Elle refuse, le pouf sous la paume.",
            "narrateur|Elle écoute la gouttière, six tapes.",
            "narrateur|Elle cherche le pois ivoire, au tapis.",
            "papa|Il s'accroupit, à leur hauteur.",
            "maman|Ses bras vont jusqu'à la tringle.",
            "papa|Vous accrochez comment, tous les deux ?",
        ],
    },
}

T3_LABS = {
    1: ("le passage de Victorina", "le bord du lit", "soulever le drap"),
    2: ("Victorina devant", "les deux chaises", "un dedans un dehors"),
    3: ("les bras de Raphaël", "le coussin levé", "le rebord ensemble"),
}

T3_CHOICE = {
    1: [
        "narrateur|Le dessous du lit attend, trop bas pour Raphaël.",
        "papa|Le passage, le bord, ou soulever le drap ?",
    ],
    2: [
        "narrateur|L'espace étroit attend, trop juste pour ses épaules.",
        "maman|Devant, les chaises, ou un dedans un dehors ?",
    ],
    3: [
        "narrateur|La tringle attend, trop haut pour Victorina.",
        "papa|Les bras, le coussin, ou le rebord ?",
    ],
}

T3_SONS = {
    (1, 1): "bois,tissu",
    (1, 2): "bois,matelas",
    (1, 3): "tissu,pluie",
    (2, 1): "bois,charniere",
    (2, 2): "chaise,tissu",
    (2, 3): "bois,voix",
    (3, 1): "tringle,tissu",
    (3, 2): "coussin,pluie",
    (3, 3): "vitre,pluie",
}

T3_EMPH = {
    1: {1: "passage", 2: "bord du lit", 3: "soulever"},
    2: {1: "devant", 2: "chaises", 3: "dedans"},
    3: {1: "bras", 2: "coussin levé", 3: "rebord"},
}

T3 = {
    (1, 1, 1): [
        "enfant-f|Je passe, Raphaël, toi tu gardes.",
        "copain|D'accord.",
        "narrateur|Victorina rampe, assez petite, sous le lit.",
        "narrateur|Ses doigts trouvent le pois ivoire, coincé.",
        "enfant-f|Je le tiens !",
        "narrateur|Elle pousse le drap sous les lattes.",
        "papa|Tes épaules étaient assez petites.",
        "narrateur|Raphaël reste au bord, trop large.",
        "copain|Je vois le pois, d'ici.",
        "enfant-f|La cabane est à nous.",
        "narrateur|Le toit de pois s'ouvre, à leur hauteur.",
    ],
    (1, 1, 2): [
        "copain|Je reste au bord, moi.",
        "papa|Assieds-toi, Raphaël.",
        "narrateur|Raphaël s'assoit, plus haut que le sommier.",
        "enfant-f|Moi je suis dessous, tout près.",
        "narrateur|Victorina tend les deux mains.",
        "narrateur|Le pois ivoire glisse vers lui, au bord.",
        "copain|Il est à toi, un moment.",
        "enfant-f|On le partage.",
        "maman|Toi assis, elle dessous, ça tient.",
        "narrateur|Le drap attend au bord, plein d'ombre.",
        "papa|Deux places, un même toit.",
    ],
    (1, 1, 3): [
        "enfant-f|On soulève un peu.",
        "copain|Moi aussi, je soulève.",
        "narrateur|Raphaël lève le drap du lit, tout haut.",
        "narrateur|Victorina se glisse, pendant l'ouverture.",
        "narrateur|Le pois ivoire tombe vers leurs mains.",
        "enfant-f|Il brille !",
        "papa|Elle est venue vers vous.",
        "copain|On l'a reprise.",
        "maman|Vos cheveux sentent le bois.",
        "narrateur|Le drap soulève la poussière, puis retombe.",
        "enfant-f|La cabane tient, de justesse.",
    ],
    (1, 2, 1): [
        "enfant-f|Je passe devant, assez mince.",
        "copain|Je te tends le drap.",
        "narrateur|Victorina se glisse, assez étroite.",
        "narrateur|Le pois ivoire se décroche de la charnière.",
        "enfant-f|Je le tiens !",
        "narrateur|Raphaël pose le drap contre le bois.",
        "papa|Tes hanches étaient à la bonne largeur.",
        "copain|Passe-le, un peu.",
        "enfant-f|Il sent le savon.",
        "maman|Toi devant, lui derrière, ça passe.",
        "narrateur|Le couloir de laine s'ouvre, un peu.",
    ],
    (1, 2, 2): [
        "enfant-f|On met les chaises, ici.",
        "copain|Une pour toi, une pour moi.",
        "narrateur|Victorina tend le drap, bras trop courts.",
        "narrateur|Deux dossiers font un mur, assez large.",
        "narrateur|Le pois ivoire se pose sur une assise.",
        "copain|Je le tiens !",
        "maman|Vos chaises ont trouvé le chemin.",
        "enfant-f|Ça sent la laine.",
        "papa|La cabane a deux murs, maintenant.",
        "narrateur|Raphaël voit le fond, Victorina le seuil.",
        "enfant-f|On entre, chacun par sa chaise.",
    ],
    (1, 2, 3): [
        "enfant-f|Papa, écarte un peu ?",
        "papa|Je fais un chemin.",
        "narrateur|La porte de l'armoire s'ouvre, comme une aile.",
        "narrateur|Victorina rentre, Raphaël reste dehors.",
        "narrateur|Le pois ivoire brille dans l'écart.",
        "copain|On se parle à travers.",
        "enfant-f|Oui.",
        "maman|Vous y arrivez, tous les deux.",
        "narrateur|Le drap devient un nid, contre l'armoire.",
        "papa|Un dedans, un dehors, un même secret.",
        "enfant-f|La cabane a deux portes.",
    ],
    (1, 3, 1): [
        "copain|Je me hausse.",
        "narrateur|Victorina garde le drap au pied.",
        "narrateur|Les doigts de Raphaël touchent la tringle.",
        "copain|Elle bouge !",
        "narrateur|Le drap penche, puis s'accroche.",
        "narrateur|Le pois ivoire se tourne vers la pluie.",
        "enfant-f|Je tiens le bas.",
        "papa|Tes doigts allaient assez loin.",
        "maman|Victorina tenait bien le bas.",
        "copain|Elle est à nous.",
        "narrateur|Deux bras, deux hauteurs, un toit.",
    ],
    (1, 3, 2): [
        "enfant-f|On monte sur le coussin ?",
        "copain|Oui, sans sauter.",
        "narrateur|Victorina pose le drap sur le coussin.",
        "narrateur|Papa tient le bois, tout ferme.",
        "narrateur|Victorina et Raphaël se haussent ensemble.",
        "narrateur|Le pois ivoire rejoint le rai de pluie.",
        "enfant-f|Je vois le ciel !",
        "copain|Je le sens.",
        "maman|Vous avez regardé ensemble.",
        "papa|Le coussin est resté ferme.",
        "narrateur|Le toit de pois atteint la tringle.",
    ],
    (1, 3, 3): [
        "enfant-f|Reste en haut, Raphaël.",
        "copain|Je tends, d'ici.",
        "narrateur|Raphaël tend le drap, bras trop longs.",
        "narrateur|Le rebord prend Victorina, puis lui.",
        "narrateur|Le pois ivoire s'assoit sur le bois froid.",
        "enfant-f|Je le tiens !",
        "papa|Chacun a fait sa part.",
        "copain|Il sent la pluie.",
        "maman|Vos bras n'avaient pas la même longueur.",
        "narrateur|Raphaël fait basculer le rideau.",
        "enfant-f|La cabane a un rebord, à nous.",
    ],
    (2, 1, 1): [
        "enfant-f|Je passe, Raphaël, toi tu gardes.",
        "copain|D'accord.",
        "narrateur|Victorina rampe, assez petite, sous le lit.",
        "narrateur|Elle glisse la lampe sous le sommier.",
        "narrateur|Le rond retrouve le pois ivoire, coincé.",
        "enfant-f|Je le vois !",
        "papa|Tes épaules étaient assez petites.",
        "narrateur|Raphaël reste au bord, trop large.",
        "copain|Le rond m'arrive, d'ici.",
        "enfant-f|La cabane est allumée.",
        "narrateur|Un toc de lampe tient sous le bois.",
    ],
    (2, 1, 2): [
        "copain|Je reste au bord, moi.",
        "papa|Assieds-toi, Raphaël.",
        "narrateur|Raphaël s'assoit, plus haut que le sommier.",
        "enfant-f|Moi je suis dessous, tout près.",
        "narrateur|Victorina tend la lampe, vers le bord.",
        "narrateur|Le pois ivoire entre dans le rond.",
        "copain|Il est à toi, un moment.",
        "enfant-f|On le partage.",
        "maman|Toi assis, elle dessous, ça tient.",
        "narrateur|La lampe attend au bord, un peu ronde.",
        "papa|Deux places, une même lumière.",
    ],
    (2, 1, 3): [
        "enfant-f|On soulève un peu.",
        "copain|Moi aussi, je soulève.",
        "narrateur|Raphaël lève le drap du lit, tout haut.",
        "narrateur|Victorina se glisse, pendant l'ouverture.",
        "narrateur|La lampe soulève un rond, tout bas.",
        "narrateur|Le pois ivoire tombe dans la lumière.",
        "papa|Elle est venue vers vous.",
        "copain|On l'a reprise.",
        "maman|Vos cheveux sentent le bois.",
        "enfant-f|La cabane tient, de justesse.",
        "narrateur|Un clic court sous le sommier.",
    ],
    (2, 2, 1): [
        "enfant-f|Je passe devant, assez mince.",
        "copain|Je te tends la lampe.",
        "narrateur|Victorina se glisse, assez étroite.",
        "narrateur|Le clic revient, près de la charnière.",
        "narrateur|Le pois ivoire sort de l'ombre.",
        "enfant-f|Je le tiens !",
        "papa|Tes hanches étaient à la bonne largeur.",
        "copain|Passe-la, un peu.",
        "enfant-f|Elle sent le métal, froid.",
        "maman|Toi devant, lui derrière, ça passe.",
        "narrateur|Raphaël pose la lampe contre le bois.",
    ],
    (2, 2, 2): [
        "enfant-f|On met les chaises, ici.",
        "copain|Une pour toi, une pour moi.",
        "narrateur|Victorina tend la lampe, bras trop courts.",
        "narrateur|Deux dossiers font un mur, assez large.",
        "narrateur|Le pois ivoire se pose dans le rond.",
        "copain|Je le tiens !",
        "maman|Vos chaises ont trouvé le chemin.",
        "enfant-f|Ça sent la laine.",
        "papa|La cabane a deux murs, maintenant.",
        "narrateur|Raphaël voit le fond, Victorina le seuil.",
        "enfant-f|On entre, chacun par sa chaise.",
    ],
    (2, 2, 3): [
        "enfant-f|Papa, écarte un peu ?",
        "papa|Je fais un chemin.",
        "narrateur|La porte de l'armoire s'ouvre, comme une aile.",
        "narrateur|Victorina rentre, Raphaël reste dehors.",
        "narrateur|La lampe devient un nid, contre l'armoire.",
        "narrateur|Le pois ivoire brille dans l'écart.",
        "copain|On se parle à travers.",
        "enfant-f|Oui.",
        "maman|Vous y arrivez, tous les deux.",
        "papa|Un dedans, un dehors, un même secret.",
        "narrateur|Deux voix tiennent le même clic.",
    ],
    (2, 3, 1): [
        "copain|Je me hausse.",
        "narrateur|Victorina garde la lampe au pied.",
        "narrateur|Les doigts de Raphaël touchent la tringle.",
        "copain|Elle bouge !",
        "narrateur|Le drap penche, puis s'accroche.",
        "narrateur|Le pois ivoire entre dans le rond de pluie.",
        "enfant-f|Je tiens le bas.",
        "papa|Tes doigts allaient assez loin.",
        "maman|Victorina tenait bien le bas.",
        "copain|Elle est à nous.",
        "narrateur|Deux bras, deux hauteurs, un toit allumé.",
    ],
    (2, 3, 2): [
        "enfant-f|On monte sur le coussin ?",
        "copain|Oui, sans sauter.",
        "narrateur|Victorina pose la lampe sur le coussin.",
        "narrateur|Papa tient le bois, tout ferme.",
        "narrateur|Victorina et Raphaël se haussent ensemble.",
        "narrateur|Le pois ivoire rejoint le rai de pluie.",
        "enfant-f|Je vois le ciel !",
        "copain|Je le sens.",
        "maman|Vous avez regardé ensemble.",
        "papa|Le coussin est resté ferme.",
        "narrateur|Le rond atteint la tringle, enfin.",
    ],
    (2, 3, 3): [
        "enfant-f|Reste en haut, Raphaël.",
        "copain|Je tends, d'ici.",
        "narrateur|Raphaël tend la lampe, bras trop longs.",
        "narrateur|Le rebord prend Victorina, puis lui.",
        "narrateur|Le pois ivoire s'assoit dans le rond.",
        "enfant-f|Je le tiens !",
        "papa|Chacun a fait sa part.",
        "copain|Il sent la pluie.",
        "maman|Vos bras n'avaient pas la même longueur.",
        "narrateur|Raphaël fait basculer le rideau.",
        "enfant-f|La cabane a un rebord, allumé.",
    ],
    (3, 1, 1): [
        "enfant-f|Je passe, Raphaël, toi tu gardes.",
        "copain|D'accord.",
        "narrateur|Victorina rampe, assez petite, sous le lit.",
        "narrateur|Elle pousse le coussin sous le bois.",
        "narrateur|Le pois ivoire glisse du pouf, coincé.",
        "enfant-f|Je le tiens !",
        "papa|Tes épaules étaient assez petites.",
        "narrateur|Raphaël reste au bord, trop large.",
        "copain|Je vois le pois, d'ici.",
        "enfant-f|La cabane a un siège.",
        "narrateur|Le pouf s'ouvre, à leur hauteur.",
    ],
    (3, 1, 2): [
        "copain|Je reste au bord, moi.",
        "papa|Assieds-toi, Raphaël.",
        "narrateur|Raphaël s'assoit, plus haut que le sommier.",
        "enfant-f|Moi je suis dessous, tout près.",
        "narrateur|Victorina pousse le coussin, tout près.",
        "narrateur|Le pois ivoire attend au bord, un peu chaud.",
        "copain|Il est à toi, un moment.",
        "enfant-f|On le partage.",
        "maman|Toi assis, elle dessous, ça tient.",
        "papa|Deux places, un même pouf.",
        "narrateur|Le coussin tient leurs coudes, chacun d'un côté.",
    ],
    (3, 1, 3): [
        "enfant-f|On soulève un peu.",
        "copain|Moi aussi, je soulève.",
        "narrateur|Raphaël lève le drap du lit, tout haut.",
        "narrateur|Victorina se glisse, pendant l'ouverture.",
        "narrateur|Le coussin soulève un coin, toc.",
        "narrateur|Le pois ivoire tombe vers le pouf.",
        "papa|Elle est venue vers vous.",
        "copain|On l'a reprise.",
        "maman|Vos cheveux sentent le bois.",
        "enfant-f|La cabane tient, de justesse.",
        "narrateur|Un pouf court sous le sommier.",
    ],
    (3, 2, 1): [
        "enfant-f|Je passe devant, assez mince.",
        "copain|Je te tends le coussin.",
        "narrateur|Victorina se glisse, assez étroite.",
        "narrateur|Le pois ivoire se décroche sous la laine.",
        "enfant-f|Je le tiens !",
        "narrateur|Raphaël pose le coussin contre le bois.",
        "papa|Tes hanches étaient à la bonne largeur.",
        "copain|Passe-le, un peu.",
        "enfant-f|Il sent le savon.",
        "maman|Toi devant, lui derrière, ça passe.",
        "narrateur|Le couloir de laine s'ouvre, un peu.",
    ],
    (3, 2, 2): [
        "enfant-f|On met les chaises, ici.",
        "copain|Une pour toi, une pour moi.",
        "narrateur|Victorina pousse le coussin, tout près.",
        "narrateur|Deux dossiers font un mur, assez large.",
        "narrateur|Le pois ivoire se pose sur une assise.",
        "copain|Je le tiens !",
        "maman|Vos chaises ont trouvé le chemin.",
        "enfant-f|Ça sent la laine.",
        "papa|La cabane a deux murs, maintenant.",
        "narrateur|Raphaël voit le fond, Victorina le seuil.",
        "enfant-f|On entre, chacun par sa chaise.",
    ],
    (3, 2, 3): [
        "enfant-f|Papa, écarte un peu ?",
        "papa|Je fais un chemin.",
        "narrateur|La porte de l'armoire s'ouvre, comme une aile.",
        "narrateur|Victorina rentre, Raphaël reste dehors.",
        "narrateur|Le coussin devient un nid, contre l'armoire.",
        "narrateur|Le pois ivoire brille dans l'écart.",
        "copain|On se parle à travers.",
        "enfant-f|Oui.",
        "maman|Vous y arrivez, tous les deux.",
        "papa|Un dedans, un dehors, un même secret.",
        "narrateur|Deux voix tiennent le même pouf.",
    ],
    (3, 3, 1): [
        "copain|Je me hausse.",
        "narrateur|Victorina garde le coussin au pied.",
        "narrateur|Les doigts de Raphaël touchent la tringle.",
        "copain|Elle bouge !",
        "narrateur|Le drap penche, puis s'accroche.",
        "narrateur|Le pois ivoire se lève avec le pouf.",
        "enfant-f|Je tiens le bas.",
        "papa|Tes doigts allaient assez loin.",
        "maman|Victorina tenait bien le bas.",
        "copain|Elle est à nous.",
        "narrateur|Deux bras, deux hauteurs, un toit moelleux.",
    ],
    (3, 3, 2): [
        "enfant-f|On monte sur le coussin ?",
        "copain|Oui, sans sauter.",
        "narrateur|Victorina pousse le coussin, tout près.",
        "narrateur|Papa tient le bois, tout ferme.",
        "narrateur|Victorina et Raphaël se haussent ensemble.",
        "narrateur|Le pois ivoire rejoint le rai de pluie.",
        "enfant-f|Je vois le ciel !",
        "copain|Je le sens.",
        "maman|Vous avez regardé ensemble.",
        "papa|Le coussin est resté ferme.",
        "narrateur|Le pouf atteint la tringle, enfin.",
    ],
    (3, 3, 3): [
        "enfant-f|Reste en haut, Raphaël.",
        "copain|Je tends, d'ici.",
        "narrateur|Raphaël pousse le coussin, tout près.",
        "narrateur|Le rebord prend Victorina, puis lui.",
        "narrateur|Le pois ivoire s'assoit sur le bois froid.",
        "enfant-f|Je le tiens !",
        "papa|Chacun a fait sa part.",
        "copain|Il sent la pluie.",
        "maman|Vos bras n'avaient pas la même longueur.",
        "narrateur|Raphaël fait basculer le rideau.",
        "enfant-f|La cabane a un rebord, moelleux.",
    ],
}

END_SONS = {1: "pluie,tissu", 2: "pluie,clic", 3: "pluie,pouf"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Sous le sommier, la cabane sent le bois.",
        "copain|Tu es passée, moi je gardais.",
        "enfant-f|Tes épaules l'ont laissé ouvert.",
        "papa|Vous l'avez, de justesse.",
        "maman|Ça a failli ne pas tenir.",
        "enfant-f|On reste un peu, Raphaël.",
        "narrateur|Le drap à pois couvre leurs genoux.",
        "narrateur|Une chaussette perdue dort sous le pois ivoire.",
    ],
    (1, 1, 2): [
        "narrateur|Au bord du lit, deux têtes se calment.",
        "enfant-f|Raphaël, tu l'as vue glisser.",
        "copain|Oui, tout près de tes mains.",
        "papa|Toi assis, elle dessous, ça tenait.",
        "maman|Vos voix sont devenues toutes petites.",
        "copain|Je reste un peu.",
        "narrateur|Le drap à pois reste dans la paume de Victorina.",
        "narrateur|Un grain de poussière tient sur le pois ivoire.",
    ],
    (1, 1, 3): [
        "narrateur|Le sommier redescend, sans bruit.",
        "copain|Elle est tombée vers nous.",
        "enfant-f|On a soulevé, tous les deux.",
        "maman|Elle n'était plus coincée.",
        "papa|Le tissu froisse, dans l'air.",
        "enfant-f|On souffle dessus.",
        "narrateur|Le drap à pois retombe, léger.",
        "narrateur|Le sommier garde un pli autour du pois ivoire.",
    ],
    (1, 2, 1): [
        "narrateur|Entre l'armoire, la cabane sent la laine.",
        "copain|Tu es passée devant, moi je tendais.",
        "enfant-f|Tes épaules restaient dehors.",
        "papa|Vous l'avez, de justesse.",
        "maman|Le gond a failli garder le pois.",
        "enfant-f|On reste un peu.",
        "narrateur|Le drap à pois garde un brin de laine.",
        "narrateur|Un brin de laine s'accroche au pois ivoire.",
    ],
    (1, 2, 2): [
        "narrateur|Deux chaises tiennent un toit de pois.",
        "enfant-f|Une pour toi, une pour moi.",
        "copain|C'est le nôtre, Victorina.",
        "papa|Vous avez élargi sans tout casser.",
        "maman|Deux dossiers, un même secret.",
        "enfant-f|On reste un peu.",
        "narrateur|Le drap à pois relie les deux assises.",
        "narrateur|Deux ombres se touchent sur le pois ivoire.",
    ],
    (1, 2, 3): [
        "narrateur|Une voix dedans, une voix dehors.",
        "copain|Tu n'es pas sortie, Victorina.",
        "enfant-f|Toi tu n'es pas entré.",
        "papa|Chacun a eu sa place.",
        "maman|Vous vous parlez, d'ici.",
        "copain|Je reste au seuil.",
        "narrateur|Le drap à pois fait un nid, contre le bois.",
        "narrateur|La charnière lâche enfin le pois ivoire.",
    ],
    (1, 3, 1): [
        "narrateur|Près de la fenêtre, la cabane sent la pluie.",
        "copain|J'ai touché la tringle, toi le bas.",
        "enfant-f|Tes bras allaient assez loin.",
        "papa|Vous l'avez, de justesse.",
        "maman|La tringle a failli rester trop haute.",
        "enfant-f|On reste un peu.",
        "narrateur|Le drap à pois penche vers le carreau.",
        "narrateur|Un rai de pluie touche le pois ivoire.",
    ],
    (1, 3, 2): [
        "narrateur|Le coussin a servi d'escalier, un moment.",
        "enfant-f|On a vu le ciel, sans sauter.",
        "copain|Le pouf est resté ferme.",
        "papa|Vous vous êtes haussés ensemble.",
        "maman|Le bois n'a pas bougé.",
        "enfant-f|On reste un peu.",
        "narrateur|Le drap à pois atteint la tringle.",
        "narrateur|Le carreau mouillé reflète le pois ivoire.",
    ],
    (1, 3, 3): [
        "narrateur|Le rebord tient deux enfants, côte à côte.",
        "copain|Moi en haut, toi près du bois.",
        "enfant-f|Chacun sa longueur de bras.",
        "papa|Chacun a fait sa part.",
        "maman|Le rideau a basculé, sans tomber.",
        "enfant-f|On reste un peu.",
        "narrateur|Le drap à pois sent la pluie, au bord.",
        "narrateur|Le rebord garde une goutte près du pois ivoire.",
    ],
    (2, 1, 1): [
        "narrateur|Sous le sommier, un rond jaune tient.",
        "copain|Tu es passée, moi je gardais.",
        "enfant-f|Tes épaules l'ont laissé ouvert.",
        "papa|Vous l'avez, de justesse.",
        "maman|Le clic a failli rester éteint.",
        "enfant-f|On reste un peu, Raphaël.",
        "narrateur|La lampe de poche fait un rond, tout bas.",
        "narrateur|La lampe dessine un rond sur le pois ivoire.",
    ],
    (2, 1, 2): [
        "narrateur|Au bord du lit, deux têtes se calment.",
        "enfant-f|Raphaël, tu as vu le rond.",
        "copain|Oui, tout près de tes mains.",
        "papa|Toi assis, elle dessous, ça tenait.",
        "maman|Vos voix sont devenues toutes petites.",
        "copain|Je reste un peu.",
        "narrateur|La lampe de poche reste dans la paume de Victorina.",
        "narrateur|Un clic se tait près du pois ivoire.",
    ],
    (2, 1, 3): [
        "narrateur|Le sommier redescend, sans bruit.",
        "copain|Elle est tombée vers nous.",
        "enfant-f|On a soulevé, tous les deux.",
        "maman|Le rond n'était plus perdu.",
        "papa|Le tissu froisse, dans l'air.",
        "enfant-f|On souffle dessus.",
        "narrateur|La lampe de poche retombe, légère.",
        "narrateur|Le tapis sent le savon sous le pois ivoire.",
    ],
    (2, 2, 1): [
        "narrateur|Entre l'armoire, un clic tient le secret.",
        "copain|Tu es passée devant, moi je tendais.",
        "enfant-f|Tes épaules restaient dehors.",
        "papa|Vous l'avez, de justesse.",
        "maman|L'ombre a failli garder le pois.",
        "enfant-f|On reste un peu.",
        "narrateur|La lampe de poche garde un peu de bois.",
        "narrateur|Un coin de drap tient le pois ivoire.",
    ],
    (2, 2, 2): [
        "narrateur|Deux chaises tiennent un toit allumé.",
        "enfant-f|Une pour toi, une pour moi.",
        "copain|C'est le nôtre, Victorina.",
        "papa|Vous avez élargi sans tout casser.",
        "maman|Deux dossiers, un même rond.",
        "enfant-f|On reste un peu.",
        "narrateur|La lampe de poche relie les deux assises.",
        "narrateur|Le coussin rond réchauffe le pois ivoire.",
    ],
    (2, 2, 3): [
        "narrateur|Une lumière dedans, une ombre dehors.",
        "copain|Tu n'es pas sortie, Victorina.",
        "enfant-f|Toi tu n'es pas entré.",
        "papa|Chacun a eu sa place.",
        "maman|Vous vous parlez, d'ici.",
        "copain|Je reste au seuil.",
        "narrateur|La lampe de poche fait un nid, contre le bois.",
        "narrateur|Une latte de bois cadre le pois ivoire.",
    ],
    (2, 3, 1): [
        "narrateur|Près de la fenêtre, un rond touche la pluie.",
        "copain|J'ai touché la tringle, toi le bas.",
        "enfant-f|Tes bras allaient assez loin.",
        "papa|Vous l'avez, de justesse.",
        "maman|La tringle a failli rester trop haute.",
        "enfant-f|On reste un peu.",
        "narrateur|La lampe de poche penche vers le carreau.",
        "narrateur|Le pull de Victorina froisse le pois ivoire.",
    ],
    (2, 3, 2): [
        "narrateur|Le coussin a servi d'escalier, un moment.",
        "enfant-f|On a vu le ciel, sans sauter.",
        "copain|Le pouf est resté ferme.",
        "papa|Vous vous êtes haussés ensemble.",
        "maman|Le bois n'a pas bougé.",
        "enfant-f|On reste un peu.",
        "narrateur|La lampe de poche atteint la tringle.",
        "narrateur|Les genoux de Raphaël veillent près du pois ivoire.",
    ],
    (2, 3, 3): [
        "narrateur|Le rebord tient deux enfants, côte à côte.",
        "copain|Moi en haut, toi près du bois.",
        "enfant-f|Chacun sa longueur de bras.",
        "papa|Chacun a fait sa part.",
        "maman|Le rideau a basculé, sans tomber.",
        "enfant-f|On reste un peu.",
        "narrateur|La lampe de poche sent la pluie, au bord.",
        "narrateur|Une chaise penche vers le pois ivoire.",
    ],
    (3, 1, 1): [
        "narrateur|Sous le sommier, le pouf sent le bois.",
        "copain|Tu es passée, moi je gardais.",
        "enfant-f|Tes épaules l'ont laissé ouvert.",
        "papa|Vous l'avez, de justesse.",
        "maman|Le coussin a failli rester coincé.",
        "enfant-f|On reste un peu, Raphaël.",
        "narrateur|Le coussin rond tient leurs coudes.",
        "narrateur|L'aile de l'armoire cache le pois ivoire.",
    ],
    (3, 1, 2): [
        "narrateur|Au bord du lit, deux têtes se calment.",
        "enfant-f|Raphaël, tu l'as senti glisser.",
        "copain|Oui, tout près de tes mains.",
        "papa|Toi assis, elle dessous, ça tenait.",
        "maman|Vos voix sont devenues toutes petites.",
        "copain|Je reste un peu.",
        "narrateur|Le coussin rond reste dans la paume de Victorina.",
        "narrateur|Le rideau frôle le pois ivoire.",
    ],
    (3, 1, 3): [
        "narrateur|Le sommier redescend, sans bruit.",
        "copain|Elle est tombée vers nous.",
        "enfant-f|On a soulevé, tous les deux.",
        "maman|Le pouf n'était plus coincé.",
        "papa|Le tissu froisse, dans l'air.",
        "enfant-f|On souffle dessus.",
        "narrateur|Le coussin rond retombe, léger.",
        "narrateur|Une goutte glisse vers le pois ivoire.",
    ],
    (3, 2, 1): [
        "narrateur|Entre l'armoire, le pouf sent la laine.",
        "copain|Tu es passée devant, moi je tendais.",
        "enfant-f|Tes épaules restaient dehors.",
        "papa|Vous l'avez, de justesse.",
        "maman|La laine a failli garder le pois.",
        "enfant-f|On reste un peu.",
        "narrateur|Le coussin rond garde un brin de laine.",
        "narrateur|Le matelas garde un creux sous le pois ivoire.",
    ],
    (3, 2, 2): [
        "narrateur|Deux chaises tiennent un toit moelleux.",
        "enfant-f|Une pour toi, une pour moi.",
        "copain|C'est le nôtre, Victorina.",
        "papa|Vous avez élargi sans tout casser.",
        "maman|Deux dossiers, un même pouf.",
        "enfant-f|On reste un peu.",
        "narrateur|Le coussin rond relie les deux assises.",
        "narrateur|Deux mains encadrent le pois ivoire.",
    ],
    (3, 2, 3): [
        "narrateur|Une voix dedans, une voix dehors.",
        "copain|Tu n'es pas sortie, Victorina.",
        "enfant-f|Toi tu n'es pas entré.",
        "papa|Chacun a eu sa place.",
        "maman|Vous vous parlez, d'ici.",
        "copain|Je reste au seuil.",
        "narrateur|Le coussin rond fait un nid, contre le bois.",
        "narrateur|Le silence de la chambre tient le pois ivoire.",
    ],
    (3, 3, 1): [
        "narrateur|Près de la fenêtre, le pouf sent la pluie.",
        "copain|J'ai touché la tringle, toi le bas.",
        "enfant-f|Tes bras allaient assez loin.",
        "papa|Vous l'avez, de justesse.",
        "maman|La tringle a failli rester trop haute.",
        "enfant-f|On reste un peu.",
        "narrateur|Le coussin rond penche vers le carreau.",
        "narrateur|Un fil de savon brille sur le pois ivoire.",
    ],
    (3, 3, 2): [
        "narrateur|Le coussin a servi d'escalier, un moment.",
        "enfant-f|On a vu le ciel, sans sauter.",
        "copain|Le pouf est resté ferme.",
        "papa|Vous vous êtes haussés ensemble.",
        "maman|Le bois n'a pas bougé.",
        "enfant-f|On reste un peu.",
        "narrateur|Le coussin rond atteint la tringle.",
        "narrateur|La poignée de l'armoire reflète le pois ivoire.",
    ],
    (3, 3, 3): [
        "narrateur|Le rebord tient deux enfants, côte à côte.",
        "copain|Moi en haut, toi près du bois.",
        "enfant-f|Chacun sa longueur de bras.",
        "papa|Chacun a fait sa part.",
        "maman|Le rideau a basculé, sans tomber.",
        "enfant-f|On reste un peu.",
        "narrateur|Le coussin rond sent la pluie, au bord.",
        "narrateur|Le plafond orange s'endort au-dessus du pois ivoire.",
    ],
}


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "gouttiere,pluie",
        {"emphasis": "pois ivoire"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le drap à pois", "la lampe de poche", "le coussin rond")},
    )

    for a in (1, 2, 3):
        base = f"CHK_T0001_P000{a}"
        out_chunks[base] = voice(
            by_src[base], T1[a]["passage"], "action", T1[a]["sons"],
            {"emphasis": T1[a]["emphasis"]},
        )
        out_chunks[f"{base}_Q0001"] = voice(
            by_src[f"{base}_Q0001"], T1[a]["question"], "clue", "",
            {"fields": T1[a]["qfields"], "emphasis": T1[a]["emphasis"]},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], T1[a]["confirm"], "confirm", T1[a]["sons"],
            {"emphasis": "pois ivoire"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("sous le lit", "entre l'armoire", "près de la fenêtre")},
        )
        for b in (1, 2, 3):
            bse = f"{base}_T0002_P000{b}"
            out_chunks[bse] = voice(
                by_src[bse], T2[(a, b)]["passage"], "obstacle", T2[(a, b)]["sons"],
                {"emphasis": T2[(a, b)]["emphasis"]},
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab(*T3_LABS[b])},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], T3[(a, b, c)], "resolution", T3_SONS[(b, c)],
                    {"emphasis": "pois ivoire"},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ENDINGS[(a, b, c)], "ending", END_SONS[a],
                    {"emphasis": "pois ivoire"},
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
        "tailles différentes",
        "plus petit ou plus grand",
        "inviter sans forcer",
        "tom ",
        "tout doux",
        "tout calme",
        "tout lent",
        "aujourd'hui,",
        "j'ai compris",
        "mission accomplie",
        "fauteuil",
        "drap à carreaux",
        "virgule de buée",
        "ancre minuscule",
        "étoile brune",
        "fil pâle",
        "croissant d'eau",
        "croissant pâle",
        "croissant de zeste",
        "virgule d'or",
        "virgule de farine",
        "œillet de cuivre",
        "perle de verre",
        "marque fine",
        "ombre-flèche",
        "minuscule symbole",
        "merle",
        "couleur de miel",
        "grand-père",
        "maîtresse",
        "jardinier",
        "zoé",
        "zoe",
        "capitaine",
        "plic",
        "volet jaune",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "victorina" not in blob:
        raise SystemExit(f"{SID}: Victorina absente")
    if "raphaël" not in blob and "raphael" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent")
    if "pois ivoire" not in blob:
        raise SystemExit(f"{SID}: pois ivoire absent")

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
        if "pois ivoire" not in c["text"].lower():
            raise SystemExit(f"{c['chunk_id']} fin sans pois ivoire")
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
        "# TREE-DIF-032 — La cabane de Victorina, sous le drap à pois\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.COR.001 — tailles différentes, jouer ensemble (vécue, non dite)\n"
        "- **Personnages :** Victorina, Raphaël, papa, maman\n"
        "- **Lieu :** chambre sous la pluie : lit, armoire, fenêtre — cabane du drap à pois\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La gouttière recopie les pois sur le carreau. Victorina compte les gouttes. "
        "Sur le drap, un **pois ivoire** cligne avec la pluie. Elle veut une vraie cabane "
        "ici, sous le drap, avec la lampe et le coussin rond. Raphaël arrive, plus grand : "
        "il veut sauter. Pas la même chose, pas le même moment. Elle jette trop vite : "
        "les genoux heurtent, le drap glisse, le pois se cache. Sourire parti. "
        "Papa s'accroupit. Merci vécu : elle tient le coin. "
        "Drap, lampe ou coussin : les trois partent. Sous le lit (trop bas), "
        "entre l'armoire (trop étroit), près de la fenêtre (tringle trop haute). "
        "Deuxième ruse : le pois ivoire perdu. Elle refuse de foncer. "
        "Passage, bord, soulever ; devant, chaises, un dedans un dehors ; "
        "bras, coussin levé, rebord. Le pois du début revient. L'objet porte une trace. "
        "La cabane a failli ne pas arriver.\n\n"
        "## Vécu\n\n"
        "Victorina propose la cabane. Raphaël propose le saut, le tir, le grimpe. "
        "Deux rythmes, sans voix caricaturale. Le silence compte. "
        "Le sourire disparaît ; envie et inquiétude se bousculent. "
        "Papa ou maman s'accroupit à la même hauteur. Personne ne donne la réponse. "
        "Victorina observe le drap, écoute la gouttière, retrouve le pois ivoire. "
        "La leçon se voit : elle passe où il ne passe pas ; ses bras atteignent "
        "ce qu'elle n'atteint pas ; un toit à deux hauteurs.\n\n"
        "## Vu et corrigé\n\n"
        "- Monde ≠ TREE-DIF-021 (pas de fort, drap à carreaux, fauteuil, virgule de buée).\n"
        "- Indice unique : pois ivoire (pas marque fine / ombre-flèche / tache / symbole).\n"
        "- Slogan tailles / Zoé / « voici le geste » jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- T1/T2/T3 changent l'action, pas seulement le décor. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (papa : le coin du drap). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, danger doux, émotion. Action plus vive.\n"
        "- N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
