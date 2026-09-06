#!/usr/bin/env python3
"""TREE-DIF-008 — F-NAR-019. Goutte du store, stand de Raphaël. N3. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-008"
N3 = 16
TITLE = "La goutte du store et le stand de Raphaël"
FIL = (
    "Sous les toiles du marché, une goutte épingle un grain de cannelle au bois. "
    "Raphaël veut tenir le stand et offrir un fruit à Mila, tout de suite. "
    "Elle n'a pas les mêmes mains, au même moment. Il tend trop vite : silence. "
    "T1 = store jaune / rouge / vert, sans retirer balance, sac, caisse. "
    "T2 = balance / sac / caisse : le grain glisse. Il refuse de foncer. "
    "T3 = je regarde / plus tard / je prends. Le grain paie le début."
)
CHARS = "Raphaël, Mila, papa, maman"
SETTING = "au marché, sous le store"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "grain de cannelle",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=la goutte épingle le grain et Mila n_est_pas_prête; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix change le stand; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_la_couleur_de_la_toile; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": None,
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=le_stand_est_là_Mila_pas_encore; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=il_tend_trop_vite_elle_ne_prend_pas; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": "grain de cannelle",
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_découragement; intensite=2; destinataire=enfant; sous_texte=le_grain_glisse_il_refuse_de_foncer; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=il_accepte_le_rythme_de_Mila; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "grain de cannelle",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_goutte_a_séché_le_grain_a_une_place; tempo=posé; sourire=léger; respiration=ample",
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
        m = TIC_WORDS.search(low)
        if m:
            raise SystemExit(f"tic {m.group(0)!r}: {ph}")
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
    "narrateur|La goutte grossit au bord de la toile.",
    "narrateur|Elle tremble, puis choisit le bois de l'étal.",
    "narrateur|Un grain de cannelle s'y colle, brun et minuscule.",
    "narrateur|Il pique un peu, collé au bois mouillé.",
    "narrateur|Le marché assemble ses caisses, sans crier.",
    "narrateur|Des voix s'installent, plus loin, pas ici.",
    "narrateur|Ça sent l'écorce mouillée, et le fruit coupé.",
    "papa|Tu as vu ce grain, Raphaël ?",
    "enfant-m|Il est coincé dans l'eau.",
    "maman|La toile va goutter longtemps.",
    "narrateur|Une caisse glisse sur le bois mouillé.",
    "narrateur|Raphaël la rattrape des deux mains.",
    "papa|Merci, tu as tenu la caisse.",
    "enfant-m|Je tiens le stand, moi.",
    "enfant-m|Un fruit, pour Mila, tout de suite.",
    "narrateur|En ce moment, Raphaël avance le bras vers elle.",
    "narrateur|Mila arrive, les mains au fond des poches.",
    "enfant-m|Viens, c'est pour toi !",
    "narrateur|Mila ne dit rien.",
    "narrateur|Ses doigts restent cachés.",
    "narrateur|Le sourire de Raphaël disparaît.",
    "narrateur|Dans sa poitrine, l'envie et la peur se bousculent.",
    "narrateur|Papa s'accroupit, à la hauteur des deux.",
    "papa|Tu l'as vue, ses poches ?",
    "enfant-m|Elle n'a rien dit.",
    "maman|Ses mains sont restées dedans.",
]

T1_CHOICE = [
    "narrateur|Trois toiles colorent l'étal des fruits.",
    "narrateur|Le store jaune, le store rouge, ou le store vert.",
    "papa|Lequel éclaire tes fruits, Raphaël ?",
]

T1 = {
    1: {
        "lab": "le store jaune",
        "sons": "toile,citron,goutte",
        "emphasis": "store jaune",
        "coul": "jaune",
        "fruit": "citron",
        "passage": [
            "narrateur|Raphaël glisse sous le store jaune.",
            "narrateur|La toile jette des ronds d'or sur les citrons.",
            "enfant-m|Ils sentent le zeste, fort.",
            "papa|La balance, le sac et la caisse restent là.",
            "narrateur|Il cueille un citron, trop vite.",
            "enfant-m|Prends, Mila !",
            "narrateur|Mila recule d'un pas.",
            "narrateur|Le citron reste seul, dans sa paume.",
            "narrateur|Le sourire de Raphaël se plie.",
            "maman|Elle n'a pas tendu les doigts.",
            "narrateur|Maman s'accroupit, près des caisses jaunes.",
            "narrateur|Une goutte dorée tremble au bord de la toile.",
            "narrateur|Elle tombe près du grain de cannelle.",
            "enfant-m|Le grain est mouillé.",
            "papa|Tu le vois, sur le bois ?",
            "narrateur|Un client passe, sans s'arrêter.",
        ],
        "question": [
            "narrateur|La goutte a teinté le citron, sous la toile.",
            "papa|De quelle couleur est le store ?",
        ],
        "qfields": {
            "expected_answer": "jaune",
            "accepted_examples": "jaune | store jaune | citron | dorée | doré | le jaune",
            "retry_prompt": "Une goutte est tombée. De quelle couleur est le store ?",
        },
        "confirm": [
            "enfant-m|Jaune.",
            "papa|Oui, jaune comme le zeste.",
            "narrateur|La toile vibre un peu, au vent.",
            "maman|Les citrons ont plein le dos.",
            "enfant-m|Je tiens le stand.",
            "narrateur|Le grain de cannelle reste collé au bois.",
            "papa|La balance est là, le sac, la caisse.",
        ],
    },
    2: {
        "lab": "le store rouge",
        "sons": "toile,fraise,goutte",
        "emphasis": "store rouge",
        "coul": "rouge",
        "fruit": "fraise",
        "passage": [
            "narrateur|Raphaël passe sous le store rouge.",
            "narrateur|La toile chauffe les joues, d'une lumière rose.",
            "enfant-m|Les fraises sentent le sucre.",
            "maman|La balance, le sac et la caisse restent là.",
            "narrateur|Il saisit une fraise, trop vite.",
            "enfant-m|Pour toi, Mila !",
            "narrateur|Mila serre les poches.",
            "narrateur|La fraise brille, seule, entre ses doigts.",
            "narrateur|L'élan de Raphaël se casse.",
            "papa|Elle n'a pas ouvert la main.",
            "narrateur|Papa s'accroupit, au ras de la barquette.",
            "narrateur|Une goutte rose glisse le long de la toile.",
            "narrateur|Elle mouille le grain de cannelle, au bord.",
            "enfant-m|Il pique un peu, le grain.",
            "maman|Tu le sens, sur le bois ?",
            "narrateur|Une femme passe, le nez ailleurs.",
        ],
        "question": [
            "narrateur|La lumière a coloré les fraises, sous la toile.",
            "maman|De quelle couleur est le store ?",
        ],
        "qfields": {
            "expected_answer": "rouge",
            "accepted_examples": "rouge | store rouge | fraise | rose | le rouge",
            "retry_prompt": "La lumière a teinté les fraises. De quelle couleur est le store ?",
        },
        "confirm": [
            "enfant-m|Rouge.",
            "maman|Oui, rouge comme la fraise.",
            "narrateur|La toile rouge fait une ombre tiède.",
            "papa|Les fraises ont pris la lumière.",
            "enfant-m|J'offre une fraise.",
            "narrateur|Le grain de cannelle reste au bord humide.",
            "maman|La balance est là, le sac, la caisse.",
        ],
    },
    3: {
        "lab": "le store vert",
        "sons": "toile,poire,goutte",
        "emphasis": "store vert",
        "coul": "vert",
        "fruit": "poire",
        "passage": [
            "narrateur|Raphaël s'abrite sous le store vert.",
            "narrateur|La toile pose des taches vertes sur les poires.",
            "enfant-m|Elles sont lourdes.",
            "papa|La balance, le sac et la caisse restent là.",
            "narrateur|Il soulève une poire, trop vite.",
            "enfant-m|Tiens, Mila !",
            "narrateur|Mila baisse les yeux.",
            "narrateur|La poire pèse, seule, contre son ventre.",
            "narrateur|Dans sa poitrine, ça serre, fort.",
            "maman|Elle n'a pas levé les mains.",
            "narrateur|Maman s'accroupit, à hauteur de l'étal.",
            "narrateur|Une goutte verte pend, trop ronde.",
            "narrateur|Elle tombe près du grain de cannelle.",
            "enfant-m|Le grain a un point d'eau.",
            "papa|Tu le vois, collé au bois ?",
            "narrateur|Un homme passe, sans regarder l'étal.",
        ],
        "question": [
            "narrateur|Une goutte a touché la poire, sous la toile.",
            "papa|De quelle couleur est le store ?",
        ],
        "qfields": {
            "expected_answer": "vert",
            "accepted_examples": "vert | store vert | poire | verte | le vert",
            "retry_prompt": "Une goutte a touché la poire. De quelle couleur est le store ?",
        },
        "confirm": [
            "enfant-m|Vert.",
            "papa|Oui, vert comme la feuille.",
            "narrateur|La toile verte bouge, presque rien.",
            "maman|Les poires ont un peu d'eau.",
            "enfant-m|Le stand est à moi.",
            "narrateur|Le grain de cannelle reste collé, brillant.",
            "papa|La balance est là, le sac, la caisse.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Sous le store jaune, le citron attend un geste.",
        "papa|La balance, le sac, ou la caisse ?",
        "maman|Tu fais quoi, avec le citron ?",
    ],
    2: [
        "narrateur|Sous le store rouge, la fraise attend un geste.",
        "maman|La balance, le sac, ou la caisse ?",
        "papa|Tu fais quoi, avec la fraise ?",
    ],
    3: [
        "narrateur|Sous le store vert, la poire attend un geste.",
        "papa|La balance, le sac, ou la caisse ?",
        "maman|Tu fais quoi, avec la poire ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "balance,aiguille,goutte",
        "emphasis": "balance",
        "passage": [
            "narrateur|Raphaël pose le citron sur la balance.",
            "narrateur|Le plateau claque, trop fort.",
            "narrateur|L'aiguille saute, puis se perd.",
            "enfant-m|Il est lourd !",
            "narrateur|Le grain de cannelle glisse vers le trou.",
            "enfant-m|Je l'attrape !",
            "narrateur|Sa main part, puis s'arrête.",
            "narrateur|Les adultes se taisent.",
            "narrateur|Raphaël écoute les caisses, au loin.",
            "narrateur|Il retrouve le grain, collé au métal.",
            "papa|L'aiguille veut se taire, tu vois ?",
            "narrateur|Mila avance le menton, puis rien.",
            "enfant-m|Tu veux voir le chiffre ?",
            "narrateur|Mila ne répond pas.",
            "maman|Ses yeux, eux, restent là.",
        ],
    },
    (1, 2): {
        "sons": "papier,sac,goutte",
        "emphasis": "sac",
        "passage": [
            "narrateur|Raphaël ouvre un sac en papier brun.",
            "narrateur|Il y glisse le citron, trop vite.",
            "narrateur|Le papier se fend, un tout petit peu.",
            "enfant-m|Il part au fond !",
            "narrateur|Le grain de cannelle bascule vers le pli.",
            "enfant-m|Je secoue !",
            "narrateur|Il retient le sac, sans le secouer.",
            "narrateur|Personne ne dit le geste.",
            "narrateur|Il écoute le papier, qui craque.",
            "narrateur|Le grain tient au bord, brun sur brun.",
            "maman|Le sac a besoin d'air, tu vois ?",
            "narrateur|Mila touche le bord, puis retire le doigt.",
            "enfant-m|Tu veux tenir le sac ?",
            "narrateur|Mila garde les mains dans les poches.",
            "papa|Le papier attend, ouvert.",
        ],
    },
    (1, 3): {
        "sons": "caisse,bois,goutte",
        "emphasis": "caisse",
        "passage": [
            "narrateur|Raphaël soulève le citron vers la caisse.",
            "narrateur|Il le pose trop haut, sur la tour.",
            "narrateur|Le citron roule vers le bord.",
            "enfant-m|Je le rattrape !",
            "narrateur|Le grain de cannelle penche entre deux planches.",
            "narrateur|Il pose les talons, collés au sol.",
            "narrateur|Il laisse la tour, sans la bousculer.",
            "narrateur|Papa se tait, accroupi.",
            "narrateur|Raphaël écoute le bois, qui grince.",
            "narrateur|Le grain reste au bord, coincé.",
            "papa|Il y a une place, plus bas ?",
            "narrateur|Mila lève les yeux, puis les baisse.",
            "enfant-m|Tu veux un citron d'en bas ?",
            "narrateur|Mila ne bouge pas.",
            "maman|La caisse est haute, pour ses mains.",
        ],
    },
    (2, 1): {
        "sons": "balance,fraise,goutte",
        "emphasis": "balance",
        "passage": [
            "narrateur|Raphaël pose la fraise sur la balance.",
            "narrateur|Un jus rose tache le plateau.",
            "narrateur|L'aiguille bouge à peine, puis s'affole.",
            "enfant-m|Elle est légère !",
            "narrateur|Le grain de cannelle nage dans le jus.",
            "enfant-m|Vite, je l'essuie !",
            "narrateur|Il ouvre les doigts, au lieu de frotter.",
            "narrateur|Maman se tait, à sa hauteur.",
            "narrateur|Il écoute le tic minuscule de l'aiguille.",
            "narrateur|Le grain s'arrête au centre, rose et brun.",
            "maman|Le métal est froid, tu sens ?",
            "narrateur|Mila avance le menton, tout près.",
            "enfant-m|Tu veux voir le poids ?",
            "narrateur|Mila ferme la bouche.",
            "papa|L'aiguille fait un petit tic, puis rien.",
        ],
    },
    (2, 2): {
        "sons": "papier,fraise,sac",
        "emphasis": "sac",
        "passage": [
            "narrateur|Raphaël glisse la barquette dans le sac.",
            "narrateur|Le papier est trop grand, elle roule.",
            "narrateur|Les fraises se cognent, au fond.",
            "enfant-m|Elles s'écrasent !",
            "narrateur|Le grain de cannelle file vers le noir du sac.",
            "enfant-m|Je le cherche !",
            "narrateur|Il recule d'un pas, exprès.",
            "narrateur|Il tient le sac ouvert, sans plonger.",
            "narrateur|Les adultes attendent, sans parler.",
            "narrateur|Une lumière rose traverse le papier.",
            "narrateur|Le grain réapparaît, coincé dans un pli.",
            "papa|Le sac est large, tu vois ?",
            "enfant-m|Tu veux le porter, Mila ?",
            "narrateur|Mila pose un doigt, puis le retire.",
            "maman|Le papier froisse sous ce doigt-là.",
        ],
    },
    (2, 3): {
        "sons": "caisse,fraise,bois",
        "emphasis": "caisse",
        "passage": [
            "narrateur|Raphaël pose la fraise dans la caisse.",
            "narrateur|Les autres sont alignées, trop serrées.",
            "narrateur|Une fraise roule vers le bord lisse.",
            "enfant-m|Je la rattrape !",
            "narrateur|Le grain de cannelle glisse sur le bois rouge.",
            "narrateur|Il pose le fruit, puis attend.",
            "narrateur|Il laisse une place vide, à sa hauteur.",
            "narrateur|Papa ne dit pas le geste.",
            "narrateur|Raphaël écoute le marché, plus bas.",
            "narrateur|Le grain s'arrête dans le creux de la place.",
            "papa|Il reste une place, juste là ?",
            "narrateur|Mila suit la fraise des yeux.",
            "enfant-m|Tu veux ranger une fraise ?",
            "narrateur|Mila ne tend pas la main.",
            "maman|Le bois sent le sucre, un peu.",
        ],
    },
    (3, 1): {
        "sons": "balance,poire,aiguille",
        "emphasis": "balance",
        "passage": [
            "narrateur|Raphaël pose la poire sur la balance.",
            "narrateur|L'aiguille part loin, d'un coup.",
            "narrateur|Le plateau penche, trop chargé.",
            "enfant-m|Elle est trop lourde !",
            "narrateur|Le grain de cannelle dévale vers le bord.",
            "enfant-m|Je retiens le plateau !",
            "narrateur|Il laisse l'aiguille finir, sans toucher.",
            "narrateur|Sa poitrine se serre, puis se relâche.",
            "narrateur|Les adultes se taisent, accroupis.",
            "narrateur|Il retrouve le grain, contre le chiffre noir.",
            "papa|Le chiffre est grand, tu le vois ?",
            "narrateur|Mila se hausse, pour mieux voir.",
            "enfant-m|Tu veux le chiffre, Mila ?",
            "narrateur|Mila redescend, sans parler.",
            "maman|La poire ne bouge plus, maintenant.",
        ],
    },
    (3, 2): {
        "sons": "papier,poire,sac",
        "emphasis": "sac",
        "passage": [
            "narrateur|Raphaël ouvre le sac, trop large.",
            "narrateur|La poire entre, presque entière.",
            "narrateur|Le papier prend sa forme, puis se déchire.",
            "enfant-m|Elle remplit tout !",
            "narrateur|Le grain de cannelle disparaît au col du sac.",
            "enfant-m|Je plonge !",
            "narrateur|Il écoute le papier, sans le froisser.",
            "narrateur|Il tient le col ouvert, deux mains.",
            "narrateur|Personne ne montre le grain.",
            "narrateur|Une tache verte perce le brun.",
            "narrateur|Le grain est là, au col, coincé.",
            "maman|Le sucré passe à travers, tu sens ?",
            "enfant-m|Tu veux porter le sac ?",
            "narrateur|Mila pose un doigt, puis s'arrête.",
            "papa|Il est lourd, pour une seule main.",
        ],
    },
    (3, 3): {
        "sons": "caisse,poire,bois",
        "emphasis": "caisse",
        "passage": [
            "narrateur|Raphaël approche la poire de la caisse.",
            "narrateur|Les poires du haut dépassent le bord.",
            "narrateur|Celle d'en bas est trop loin, pour lui.",
            "enfant-m|Je mets la mienne en haut !",
            "narrateur|Le grain de cannelle bascule vers le vide.",
            "narrateur|Il laisse la tour, sans la rattraper trop vite.",
            "narrateur|Il choisit une poire d'en bas, à sa hauteur.",
            "narrateur|Maman se tait, les mains sur les genoux.",
            "narrateur|Il écoute le bois, qui sent le fruit.",
            "narrateur|Le grain tient sur la joue de la petite.",
            "papa|Celle d'en bas est plus près, tu vois ?",
            "narrateur|Mila regarde le rang du bas.",
            "enfant-m|Tu veux une poire d'en bas ?",
            "narrateur|Mila ne répond pas.",
            "maman|Il y en a une, juste à sa hauteur.",
        ],
    },
}

T3_CHOICE = {
    1: [
        "narrateur|Mila fixe la balance, sans parler.",
        "maman|Je regarde, plus tard, ou je prends ?",
    ],
    2: [
        "narrateur|Mila est près du sac, les poches pleines.",
        "papa|Je regarde, plus tard, ou je prends ?",
    ],
    3: [
        "narrateur|Mila lève les yeux vers la caisse.",
        "maman|Je regarde, plus tard, ou je prends ?",
    ],
}

T3_SONS = {
    1: {1: "aiguille,silence", 2: "pas,balance", 3: "plateau,mains"},
    2: {1: "papier,silence", 2: "pas,sac", 3: "papier,mains"},
    3: {1: "bois,silence", 2: "pas,caisse", 3: "fruit,mains"},
}

T3_EMPH = {
    1: {1: "aiguille", 2: "plus tard", 3: "plateau"},
    2: {1: "papier", 2: "plus tard", 3: "sac"},
    3: {1: "caisse", 2: "plus tard", 3: "place"},
}

T3 = {
    (1, 1, 1): [
        "enfant-f|Je regarde.",
        "enfant-m|D'accord.",
        "narrateur|Raphaël laisse l'aiguille se calmer.",
        "narrateur|Le citron reste sur le plateau froid.",
        "narrateur|Mila suit l'aiguille des yeux, longtemps.",
        "papa|L'aiguille s'est arrêtée, toute seule.",
        "narrateur|Le grain de cannelle tient au centre du métal.",
        "maman|Vous l'avez vue, sans la toucher.",
    ],
    (1, 1, 2): [
        "enfant-f|Plus tard.",
        "enfant-m|D'accord.",
        "enfant-m|Je te le garde.",
        "narrateur|Raphaël garde le citron sur le plateau.",
        "narrateur|Mila recule d'un pas, vers une autre odeur.",
        "papa|Le citron ne bouge plus.",
        "narrateur|Le grain de cannelle attend, au bord du métal.",
        "maman|Le zeste reste sur le plateau.",
    ],
    (1, 1, 3): [
        "enfant-f|Je prends.",
        "enfant-m|Oui.",
        "narrateur|Mila pose un doigt près de l'aiguille.",
        "narrateur|Le citron penche un peu, puis tient.",
        "narrateur|Deux petites mains encadrent le plateau.",
        "papa|Vous l'avez pesé, tous les deux.",
        "narrateur|Le grain de cannelle se coince entre métal et zeste.",
        "maman|Le plateau redevient calme.",
    ],
    (1, 2, 1): [
        "enfant-f|Je regarde.",
        "enfant-m|D'accord.",
        "narrateur|Raphaël tient le sac ouvert, sans bouger.",
        "narrateur|Un citron reste dedans, au fond brun.",
        "narrateur|Mila regarde le papier, le nez tout près.",
        "maman|Ses yeux restent sur le papier.",
        "narrateur|Le grain de cannelle brille au bord du pli.",
        "papa|Le sac respire, ouvert.",
    ],
    (1, 2, 2): [
        "enfant-f|Plus tard.",
        "enfant-m|D'accord.",
        "enfant-m|Je te le garde.",
        "narrateur|Raphaël referme un peu le sac.",
        "narrateur|Mila s'éloigne vers un autre étal.",
        "maman|Le sac sent le zeste, au chaud.",
        "narrateur|Le grain de cannelle reste au fond du papier.",
        "papa|Un citron attend, pour elle.",
    ],
    (1, 2, 3): [
        "enfant-f|Je prends.",
        "enfant-m|Oui.",
        "narrateur|Mila prend le sac par le bord.",
        "narrateur|Le citron roule au fond, sans tomber.",
        "narrateur|Le papier tient, entre deux paires de mains.",
        "maman|Vous le portez, ensemble.",
        "narrateur|Le grain de cannelle part au fond, avec le fruit.",
        "papa|Le sac se ferme, presque.",
    ],
    (1, 3, 1): [
        "enfant-f|Je regarde.",
        "enfant-m|D'accord.",
        "narrateur|Raphaël pose le citron plus bas, à sa hauteur.",
        "narrateur|Mila suit le geste, sans toucher.",
        "narrateur|Les citrons du haut brillent, trop loin.",
        "papa|Elle suit le stand, sans bouger.",
        "narrateur|Le grain de cannelle reste sur le bord de la caisse.",
        "maman|Le bois a gardé sa place d'en bas.",
    ],
    (1, 3, 2): [
        "enfant-f|Plus tard.",
        "enfant-m|D'accord.",
        "enfant-m|Je te la garde.",
        "narrateur|Raphaël laisse une place vide dans la caisse.",
        "narrateur|Mila part un peu, puis se retourne.",
        "papa|La place reste vide, pour elle.",
        "narrateur|Le grain de cannelle est posé sur cette place.",
        "maman|Les citrons attendent, autour.",
    ],
    (1, 3, 3): [
        "enfant-f|Je prends.",
        "enfant-m|Oui.",
        "narrateur|Mila glisse le citron dans la caisse.",
        "narrateur|Il trouve sa place, en bas, à sa main.",
        "narrateur|Le bois ne bouge plus.",
        "papa|Le stand a deux paires de mains.",
        "narrateur|Le grain de cannelle voyage, collé au zeste.",
        "maman|La tour tient, plus basse.",
    ],
    (2, 1, 1): [
        "enfant-f|Je regarde.",
        "enfant-m|D'accord.",
        "narrateur|Raphaël laisse le jus rose sécher.",
        "narrateur|La fraise reste sur le plateau, légère.",
        "narrateur|Mila suit l'aiguille, un long moment.",
        "papa|Le tic s'est tu, tout seul.",
        "narrateur|Le grain de cannelle tient au centre du rond rose.",
        "maman|Vous avez regardé le poids, sans le chasser.",
    ],
    (2, 1, 2): [
        "enfant-f|Plus tard.",
        "enfant-m|D'accord.",
        "enfant-m|Je te la garde.",
        "narrateur|Raphaël garde la fraise sur le métal.",
        "narrateur|Mila recule vers une autre odeur, plus loin.",
        "maman|La fraise garde sa place.",
        "narrateur|Le grain de cannelle attend, à côté du fruit.",
        "papa|Le plateau reste froid, pour elle.",
    ],
    (2, 1, 3): [
        "enfant-f|Je prends.",
        "enfant-m|Oui.",
        "narrateur|Mila pose un doigt près de l'aiguille.",
        "narrateur|La fraise penche, puis se cale.",
        "narrateur|Deux doigts encadrent le grain, sans l'écraser.",
        "papa|Vous l'avez pesée, tous les deux.",
        "narrateur|Le grain de cannelle reste sous deux doigts.",
        "maman|L'aiguille s'est tue, tout près.",
    ],
    (2, 2, 1): [
        "enfant-f|Je regarde.",
        "enfant-m|D'accord.",
        "narrateur|Raphaël tient le sac grand ouvert.",
        "narrateur|La barquette reste visible, au fond.",
        "narrateur|Mila regarde le pli, où ça brille.",
        "maman|Ses yeux restent sur le papier rose.",
        "narrateur|Le grain de cannelle est coincé dans le pli.",
        "papa|Le sac sent le sucre, un peu.",
    ],
    (2, 2, 2): [
        "enfant-f|Plus tard.",
        "enfant-m|D'accord.",
        "enfant-m|Je te le garde.",
        "narrateur|Raphaël referme le sac à moitié.",
        "narrateur|Mila s'éloigne, puis s'arrête près d'un autre étal.",
        "papa|La barquette attend au fond.",
        "narrateur|Le grain de cannelle reste sur le papier.",
        "maman|Le sac sent le sucre, pour plus tard.",
    ],
    (2, 2, 3): [
        "enfant-f|Je prends.",
        "enfant-m|Oui.",
        "narrateur|Mila prend le sac par les deux bords.",
        "narrateur|Les fraises se calment, au fond.",
        "narrateur|Le papier tient, porté à deux.",
        "maman|Vous le portez, sans le secouer.",
        "narrateur|Le grain de cannelle part dedans, avec elles.",
        "papa|Le sac froisse, puis se tait.",
    ],
    (2, 3, 1): [
        "enfant-f|Je regarde.",
        "enfant-m|D'accord.",
        "narrateur|Raphaël laisse la place vide, dans la caisse.",
        "narrateur|Les fraises restent alignées, autour.",
        "narrateur|Mila suit la rangée des yeux, lentement.",
        "papa|Elle suit le bois, sans toucher.",
        "narrateur|Le grain de cannelle reste sur le bois rouge.",
        "maman|Les fraises sont alignées, sous le rouge.",
    ],
    (2, 3, 2): [
        "enfant-f|Plus tard.",
        "enfant-m|D'accord.",
        "enfant-m|Je te la garde.",
        "narrateur|Raphaël protège la place rose, vide.",
        "narrateur|Mila part vers les voix, puis se retourne.",
        "maman|La place reste, pour elle.",
        "narrateur|Le grain de cannelle attend au creux de la place.",
        "papa|Une place rose reste dans la caisse.",
    ],
    (2, 3, 3): [
        "enfant-f|Je prends.",
        "enfant-m|Oui.",
        "narrateur|Mila glisse la fraise dans la place vide.",
        "narrateur|La fraise rattrapée ne roule plus.",
        "narrateur|Deux mains ferment la rangée.",
        "papa|Le stand a deux paires de mains.",
        "narrateur|Le grain de cannelle voyage, dessus.",
        "maman|La caisse sent le sucre, moins fort.",
    ],
    (3, 1, 1): [
        "enfant-f|Je regarde.",
        "enfant-m|D'accord.",
        "narrateur|Raphaël laisse le plateau se calmer.",
        "narrateur|La poire pèse, sans bouger.",
        "narrateur|Mila se hausse, lit le chiffre des yeux.",
        "papa|Le chiffre noir reste grand.",
        "narrateur|Le grain de cannelle tient contre le plateau.",
        "maman|Vous l'avez lu, sans le pousser.",
    ],
    (3, 1, 2): [
        "enfant-f|Plus tard.",
        "enfant-m|D'accord.",
        "enfant-m|Je te la garde.",
        "narrateur|Raphaël garde la poire sur le métal.",
        "narrateur|Mila recule vers une odeur de feuille.",
        "maman|La poire pèse, pour plus tard.",
        "narrateur|Le grain de cannelle s'abrite sous le fruit.",
        "papa|Le plateau penche moins, maintenant.",
    ],
    (3, 1, 3): [
        "enfant-f|Je prends.",
        "enfant-m|Oui.",
        "narrateur|Mila pose les deux mains près du plateau.",
        "narrateur|La poire se cale, moins penchée.",
        "narrateur|Le chiffre s'arrête, entre eux.",
        "papa|Vous l'avez pesée, tous les deux.",
        "narrateur|Le grain de cannelle reste entre deux paumes.",
        "maman|Le plateau s'est calmé, entre eux.",
    ],
    (3, 2, 1): [
        "enfant-f|Je regarde.",
        "enfant-m|D'accord.",
        "narrateur|Raphaël tient le col du sac, ouvert.",
        "narrateur|La poire reste visible, trop grande.",
        "narrateur|Mila regarde la tache verte, longtemps.",
        "maman|Ses yeux restent sur le brun.",
        "narrateur|Le grain de cannelle tient au col du sac.",
        "papa|Le sac a pris la forme de la poire.",
    ],
    (3, 2, 2): [
        "enfant-f|Plus tard.",
        "enfant-m|D'accord.",
        "enfant-m|Je te le garde.",
        "narrateur|Raphaël pose le sac contre l'étal.",
        "narrateur|Mila s'éloigne, un pas, puis deux.",
        "papa|Le papier attend, un peu lourd.",
        "narrateur|Le grain de cannelle reste, brun sur brun.",
        "maman|Le sucré reste dans le papier.",
    ],
    (3, 2, 3): [
        "enfant-f|Je prends.",
        "enfant-m|Oui.",
        "narrateur|Mila prend le sac à deux, par le col.",
        "narrateur|La poire se cale, sans déchirer.",
        "narrateur|Le papier penche, puis tient.",
        "maman|Vous le portez, sans le serrer.",
        "narrateur|Le grain de cannelle part au fond, voyageur.",
        "papa|Le sac vert-brun penche, puis tient.",
    ],
    (3, 3, 1): [
        "enfant-f|Je regarde.",
        "enfant-m|D'accord.",
        "narrateur|Raphaël montre la poire d'en bas.",
        "narrateur|Mila suit le rang du bas, des yeux.",
        "narrateur|Les poires d'en haut restent trop loin.",
        "papa|Celles d'en bas restent à hauteur.",
        "narrateur|Le grain de cannelle tient sur la plus petite.",
        "maman|Elle a vu sa poire, sans la prendre.",
    ],
    (3, 3, 2): [
        "enfant-f|Plus tard.",
        "enfant-m|D'accord.",
        "enfant-m|Je te la garde.",
        "narrateur|Raphaël laisse la petite poire à sa place.",
        "narrateur|Mila part, puis se retourne vers le vert.",
        "maman|Une poire du bas attend.",
        "narrateur|Le grain de cannelle reste sur sa joue.",
        "papa|La caisse garde sa hauteur, pour elle.",
    ],
    (3, 3, 3): [
        "enfant-f|Je prends.",
        "enfant-m|Oui.",
        "narrateur|Mila glisse la poire d'en bas vers elle.",
        "narrateur|Elle trouve sa place, contre son ventre.",
        "narrateur|Le bois d'en haut ne bouge plus.",
        "papa|Le stand a deux paires de mains.",
        "narrateur|Le grain de cannelle voyage, sur sa joue.",
        "maman|La poire d'en bas a trouvé sa place.",
    ],
}

END_SONS = {1: "balance,marche", 2: "papier,marche", 3: "bois,marche"}

ENDINGS = {
    (1, 1, 1): [
        "narrateur|Le stand a failli rester sans regard.",
        "narrateur|Mila est restée au bord, les yeux ouverts.",
        "enfant-m|Tu as regardé le chiffre.",
        "enfant-f|Oui.",
        "papa|L'aiguille ne danse plus.",
        "maman|Le citron a gardé sa place.",
        "narrateur|La goutte jaune a séché en trait d'or.",
        "narrateur|Le grain de cannelle tient sur le plateau froid.",
    ],
    (1, 1, 2): [
        "narrateur|Mila revient, les joues un peu chaudes.",
        "enfant-f|Maintenant ?",
        "enfant-m|Oui.",
        "enfant-m|C'est pour toi.",
        "narrateur|Elle s'approche de la balance.",
        "papa|Vous avez pris le temps.",
        "narrateur|La goutte jaune n'est plus qu'un trait.",
        "narrateur|Le citron attend, et le grain de cannelle brille à côté.",
    ],
    (1, 1, 3): [
        "narrateur|Le citron a failli rouler, tout à l'heure.",
        "enfant-f|On l'a pesé.",
        "enfant-m|Le stand est à nous.",
        "papa|Vous avez offert le fruit.",
        "maman|Le métal a deux traces de doigts.",
        "narrateur|La goutte jaune a quitté le zeste.",
        "narrateur|Le bois de l'étal redevient sec.",
        "narrateur|Deux doigts ont coincé le grain de cannelle entre métal et zeste.",
    ],
    (1, 2, 1): [
        "narrateur|Le sac a failli se fermer trop tôt.",
        "narrateur|Mila reste au bord, le nez sur le papier.",
        "enfant-m|Tu as regardé le fond.",
        "enfant-f|Oui.",
        "papa|Le papier est resté ouvert.",
        "maman|Le zeste habite le brun.",
        "narrateur|La goutte jaune a séché sur le pli.",
        "narrateur|Le sac brun garde une ombre de citron, et le grain de cannelle.",
    ],
    (1, 2, 2): [
        "narrateur|Mila revient, un sac d'un autre étal à la main.",
        "enfant-f|Maintenant ?",
        "enfant-m|Oui, le tien est là.",
        "narrateur|Elle s'approche du papier.",
        "papa|Vous avez pris le temps.",
        "maman|Le sac l'attendait.",
        "narrateur|La goutte jaune a quitté le col.",
        "narrateur|Le papier reste ouvert, le grain de cannelle au bord.",
    ],
    (1, 2, 3): [
        "narrateur|Le papier a failli se fendre jusqu'au bout.",
        "enfant-f|On l'a porté.",
        "enfant-m|Le stand est à nous.",
        "papa|Vous avez offert le fruit.",
        "maman|Le sac penche entre deux petites mains.",
        "narrateur|La goutte jaune a séché dans le fond.",
        "narrateur|Le bois de l'étal redevient sec.",
        "narrateur|Le sac penche entre deux petites mains, grain de cannelle au fond.",
    ],
    (1, 3, 1): [
        "narrateur|La tour a failli tout emporter.",
        "narrateur|Mila reste au bord, les yeux sur le bas.",
        "enfant-m|Tu as regardé en bas.",
        "enfant-f|Oui.",
        "papa|Les citrons du haut brillent, trop loin.",
        "maman|Le bois d'en bas est à sa hauteur.",
        "narrateur|La goutte jaune a séché sur la planche.",
        "narrateur|Les citrons du haut brillent, grain de cannelle sur le bord.",
    ],
    (1, 3, 2): [
        "narrateur|Mila revient, les poches un peu moins profondes.",
        "enfant-f|Maintenant ?",
        "enfant-m|Oui, ta place est là.",
        "narrateur|Elle s'approche de la caisse.",
        "papa|Vous avez pris le temps.",
        "maman|La place vide l'attendait.",
        "narrateur|La goutte jaune a quitté le bord.",
        "narrateur|Une place vide reste, le grain de cannelle posé dessus.",
    ],
    (1, 3, 3): [
        "narrateur|Le citron a failli tomber de la tour.",
        "enfant-f|On l'a rangé.",
        "enfant-m|Le stand est à nous.",
        "papa|Vous avez offert le fruit.",
        "maman|La tour tient, plus basse.",
        "narrateur|La goutte jaune a séché sur le zeste.",
        "narrateur|Le bois de l'étal redevient sec.",
        "narrateur|Le citron mouillé a rejoint la tour, grain de cannelle collé.",
    ],
    (2, 1, 1): [
        "narrateur|Le jus a failli emporter le grain.",
        "narrateur|Mila reste au bord, les yeux sur le rond.",
        "enfant-m|Tu as regardé le tic.",
        "enfant-f|Oui.",
        "papa|L'aiguille s'est tue.",
        "maman|La fraise a gardé sa place.",
        "narrateur|La goutte rose a séché en rond mince.",
        "narrateur|Un rond rose sèche, le grain de cannelle au centre.",
    ],
    (2, 1, 2): [
        "narrateur|Mila revient, une miette sucrée au coin des lèvres.",
        "enfant-f|Maintenant ?",
        "enfant-m|Oui.",
        "narrateur|Elle s'approche de la balance.",
        "papa|Vous avez pris le temps.",
        "maman|La fraise l'attendait.",
        "narrateur|La goutte rose n'est plus qu'un halo.",
        "narrateur|La fraise garde sa place, grain de cannelle à côté.",
    ],
    (2, 1, 3): [
        "narrateur|La fraise a failli glisser dans le jus.",
        "enfant-f|On l'a pesée.",
        "enfant-m|Le stand est à nous.",
        "papa|Vous avez offert le fruit.",
        "maman|Deux doigts ont gardé le grain.",
        "narrateur|La goutte rose a quitté le métal.",
        "narrateur|Le bois de l'étal redevient sec.",
        "narrateur|L'aiguille s'est tue, grain de cannelle sous deux doigts.",
    ],
    (2, 2, 1): [
        "narrateur|Le sac a failli avaler le grain.",
        "narrateur|Mila reste au bord, le nez dans le pli.",
        "enfant-m|Tu as regardé le pli.",
        "enfant-f|Oui.",
        "papa|Le papier est resté ouvert.",
        "maman|Le sucre habite le brun.",
        "narrateur|La goutte rose a séché dans le pli.",
        "narrateur|Le sac sent le sucre, grain de cannelle coincé dans le pli.",
    ],
    (2, 2, 2): [
        "narrateur|Mila revient, les doigts un peu collants.",
        "enfant-f|Maintenant ?",
        "enfant-m|Oui, le sac est là.",
        "narrateur|Elle s'approche du papier.",
        "papa|Vous avez pris le temps.",
        "maman|La barquette l'attendait.",
        "narrateur|La goutte rose a quitté le col.",
        "narrateur|La barquette attend, grain de cannelle sur le papier.",
    ],
    (2, 2, 3): [
        "narrateur|Les fraises ont failli s'écraser au fond.",
        "enfant-f|On l'a porté.",
        "enfant-m|Le stand est à nous.",
        "papa|Vous avez offert le fruit.",
        "maman|Le sac froisse, porté à deux.",
        "narrateur|La goutte rose a séché au fond.",
        "narrateur|Le bois de l'étal redevient sec.",
        "narrateur|Le sac froisse, porté à deux, grain de cannelle dedans.",
    ],
    (2, 3, 1): [
        "narrateur|La rangée a failli tout emporter.",
        "narrateur|Mila reste au bord, les yeux sur le bois.",
        "enfant-m|Tu as regardé la place.",
        "enfant-f|Oui.",
        "papa|Les fraises sont alignées, sous le rouge.",
        "maman|Le bois a gardé un creux.",
        "narrateur|La goutte rose a séché sur la planche.",
        "narrateur|Les fraises sont alignées, grain de cannelle sur le bois rouge.",
    ],
    (2, 3, 2): [
        "narrateur|Mila revient, une main hors de la poche.",
        "enfant-f|Maintenant ?",
        "enfant-m|Oui, ta place est là.",
        "narrateur|Elle s'approche de la caisse.",
        "papa|Vous avez pris le temps.",
        "maman|La place rose l'attendait.",
        "narrateur|La goutte rose a quitté le bord.",
        "narrateur|Une place rose reste, grain de cannelle au creux.",
    ],
    (2, 3, 3): [
        "narrateur|La fraise a failli rouler hors de la caisse.",
        "enfant-f|On l'a rangée.",
        "enfant-m|Le stand est à nous.",
        "papa|Vous avez offert le fruit.",
        "maman|La rangée tient, fermée.",
        "narrateur|La goutte rose a séché sur le fruit.",
        "narrateur|Le bois de l'étal redevient sec.",
        "narrateur|La fraise rattrapée ne roule plus, grain de cannelle dessus.",
    ],
    (3, 1, 1): [
        "narrateur|Le plateau a failli tout verser.",
        "narrateur|Mila reste au bord, les yeux sur le chiffre.",
        "enfant-m|Tu as regardé le chiffre.",
        "enfant-f|Oui.",
        "papa|Le chiffre noir reste grand.",
        "maman|La poire a gardé sa place.",
        "narrateur|La goutte verte a séché en trait d'eau.",
        "narrateur|Le chiffre noir reste grand, grain de cannelle contre le plateau.",
    ],
    (3, 1, 2): [
        "narrateur|Mila revient, une feuille collée à la chaussure.",
        "enfant-f|Maintenant ?",
        "enfant-m|Oui.",
        "narrateur|Elle s'approche de la balance.",
        "papa|Vous avez pris le temps.",
        "maman|La poire l'attendait.",
        "narrateur|La goutte verte n'est plus qu'un point.",
        "narrateur|La poire pèse, grain de cannelle à l'abri sous le fruit.",
    ],
    (3, 1, 3): [
        "narrateur|La poire a failli faire pencher tout le plateau.",
        "enfant-f|On l'a pesée.",
        "enfant-m|Le stand est à nous.",
        "papa|Vous avez offert le fruit.",
        "maman|Le plateau s'est calmé, entre eux.",
        "narrateur|La goutte verte a quitté la peau.",
        "narrateur|Le bois de l'étal redevient sec.",
        "narrateur|Le plateau s'est calmé, grain de cannelle entre eux.",
    ],
    (3, 2, 1): [
        "narrateur|Le sac a failli se déchirer jusqu'au fond.",
        "narrateur|Mila reste au bord, les yeux sur la tache.",
        "enfant-m|Tu as regardé le col.",
        "enfant-f|Oui.",
        "papa|Le sac a pris la forme de la poire.",
        "maman|Le sucré habite le brun.",
        "narrateur|La goutte verte a séché au col.",
        "narrateur|Le sac a pris la forme de la poire, grain de cannelle au col.",
    ],
    (3, 2, 2): [
        "narrateur|Mila revient, les mains hors des poches.",
        "enfant-f|Maintenant ?",
        "enfant-m|Oui, le sac est là.",
        "narrateur|Elle s'approche du papier.",
        "papa|Vous avez pris le temps.",
        "maman|Le papier l'attendait, lourd.",
        "narrateur|La goutte verte a quitté le brun.",
        "narrateur|Le papier attend, grain de cannelle brun sur le brun.",
    ],
    (3, 2, 3): [
        "narrateur|La poire a failli fendre le sac.",
        "enfant-f|On l'a portée.",
        "enfant-m|Le stand est à nous.",
        "papa|Vous avez offert le fruit.",
        "maman|Le sac penche, puis tient.",
        "narrateur|La goutte verte a séché au fond.",
        "narrateur|Le bois de l'étal redevient sec.",
        "narrateur|Le sac penche, puis tient, grain de cannelle au fond.",
    ],
    (3, 3, 1): [
        "narrateur|La tour a failli cacher toutes les poires.",
        "narrateur|Mila reste au bord, les yeux sur le bas.",
        "enfant-m|Tu as regardé en bas.",
        "enfant-f|Oui.",
        "papa|Les poires d'en bas restent à hauteur.",
        "maman|La petite a gardé sa joue.",
        "narrateur|La goutte verte a séché sur la planche.",
        "narrateur|Les poires d'en bas restent à hauteur, grain de cannelle sur la plus petite.",
    ],
    (3, 3, 2): [
        "narrateur|Mila revient, une main sur le bord de l'étal.",
        "enfant-f|Maintenant ?",
        "enfant-m|Oui, ta poire est là.",
        "narrateur|Elle s'approche de la caisse.",
        "papa|Vous avez pris le temps.",
        "maman|La petite l'attendait.",
        "narrateur|La goutte verte a quitté le bord.",
        "narrateur|Une poire du bas attend, grain de cannelle sur sa joue.",
    ],
    (3, 3, 3): [
        "narrateur|La poire d'en haut a failli tout cacher.",
        "enfant-f|On l'a prise, en bas.",
        "enfant-m|Le stand est à nous.",
        "papa|Vous avez offert le fruit.",
        "maman|La poire d'en bas a trouvé sa place.",
        "narrateur|La goutte verte a séché sur sa joue.",
        "narrateur|Le bois de l'étal redevient sec.",
        "narrateur|La poire d'en bas a trouvé sa place, grain de cannelle voyageur.",
    ],
}

RECYCLED = (
    "étoile brune", "fil pâle", "croissant d'eau", "croissant pâle",
    "virgule de farine", "bouton de nacre", "nœud de raphia", "pois ivoire",
    "grain de savon", "grain de vanille", "pastille de colle", "virgule de buée",
    "capuchon", "grain doré", "brin de safran", "anneau de liège",
    "clou à tête", "grain d'ambre", "goutte de cire", "anneau de zinc",
    "larme de bronze", "point de cire", "bracelet d'écorce", "boucle d'étain",
    "anneau de pollen", "dent de laitue", "éclat de zinc", "éclat de thym",
    "lune d'étain", "grain de grenat", "grain d'indigo", "grain de brique",
    "éclat vert", "écaille d'étain", "vis verte", "cristal de sucre",
    "écaille de lichen", "grain de cire", "dent de fermeture", "écaille de nacre",
    "grain de paprika", "écaille de boue", "point de rouille", "grain de mica",
    "marque fine", "ombre en forme", "panier d'osier", "merle",
    "couleur de miel", "gouttes au bord",
)


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "goutte,caisse,marche",
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "toile",
        {"fields": t3lab("le store jaune", "le store rouge", "le store vert"), "pause_before": 200},
    )

    for a in (1, 2, 3):
        t1 = T1[a]
        base = f"CHK_T0001_P000{a}"
        out_chunks[base] = voice(by_src[base], t1["passage"], "action", t1["sons"], {"emphasis": t1["emphasis"]})
        out_chunks[f"{base}_Q0001"] = voice(
            by_src[f"{base}_Q0001"], t1["question"], "clue", "",
            {"emphasis": t1["coul"], "fields": t1["qfields"]},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], t1["confirm"], "confirm", t1["sons"], {"emphasis": t1["coul"]},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("la balance", "le sac", "la caisse")},
        )
        for b in (1, 2, 3):
            bse = f"{base}_T0002_P000{b}"
            t2 = T2[(a, b)]
            out_chunks[bse] = voice(
                by_src[bse], t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emphasis"]},
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab("je regarde", "plus tard", "je prends")},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], T3[(a, b, c)], "resolution", T3_SONS[b][c],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ENDINGS[(a, b, c)], "ending", END_SONS[b],
                    {"emphasis": "grain de cannelle"},
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
        "bravo tu as",
        "bon travail",
        "il faut attendre",
        "inviter sans forcer",
        "j'ai compris",
        "mission accomplie",
        "aujourd'hui,",
        "encore frais",
        "tout doux",
        "tout calme",
        "kenzo",
        "panier d'osier",
        "four du boulanger",
        "nora",
        "sami",
        "léa",
        "lea ",
        "tom ",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    for rec in RECYCLED:
        if rec in whole:
            raise SystemExit(f"{SID} indice recyclé: {rec}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "raphaël" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    if "grain de cannelle" not in blob:
        raise SystemExit(f"{SID}: grain de cannelle absent")

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
        if "grain de cannelle" not in c["text"].lower() and "grain" not in last_n[-1].lower():
            raise SystemExit(f"grain non payé: {c['chunk_id']}")
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
    if min(counts) < 520 or max(counts) > 760:
        raise SystemExit(f"longueur chemins hors barre: {min(counts)}-{max(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# TREE-DIF-008 — {TITLE}\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.BES.002 — besoin / calme / plus de temps (vécue, jamais dite)\n"
        "- **Personnages :** Raphaël, Mila, papa, maman\n"
        "- **Lieu :** au marché, sous le store (étal des fruits, trois toiles)\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "La goutte du store choisit le bois, et épingle un **grain de cannelle**. "
        "Raphaël veut tenir le stand et offrir un fruit à Mila, **tout de suite**. "
        "Elle arrive, les mains dans les poches. Silence. Le sourire disparaît. "
        "Papa s'accroupit. Merci vécu : la caisse rattrapée. "
        "T1 = store jaune / rouge / vert (citrons, fraises, poires) : "
        "balance, sac et caisse restent. Il tend trop vite. "
        "T2 = balance / sac / caisse : le grain glisse, deuxième ruse. "
        "Il refuse de foncer, observe, retrouve le grain du début. "
        "T3 = je regarde / plus tard / je prends. "
        "La goutte sèche. Le grain a une place. Le dénouement a failli.\n\n"
        "## Vécu\n\n"
        "Raphaël propose, Mila prend son temps ou pose sa limite. "
        "Le silence compte. Chaque choix change l'obstacle et le climax. "
        "La leçon se voit : tendre trop tôt laisse le fruit seul ; "
        "regarder, garder pour plus tard, ou prendre ensemble, ça tient. "
        "Indice unique : grain de cannelle, payé aux 27 fins. "
        "Monde distinct de TREE-AUT-045 (panier d'osier) et TREE-DIF-030 (four, pain).\n\n"
        "## Vu et corrigé\n\n"
        "- Ouverture inventée (goutte qui choisit le bois). « encore frais » jeté.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- T1/T2/T3 changent l'action. 9 T2 distincts, 27 T3, 27 fins.\n"
        "- Merci vécu (caisse tenue). Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` "
        "(arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
        f"- N3 ≤ 16. `check()` OK. Pas apply.\n\n"
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
