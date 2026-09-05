#!/usr/bin/env python3
"""TREE-DIF-010 — F-NAR-019. Chapeau de paille, Raphaël saute. N3. TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-010"
N3 = 16
TITLE = "Le chapeau de paille et Raphaël qui saute"
FIL = (
    "Après la baignade, la maison de bois sèche, tic par tic. "
    "Sur la rampe, un chapeau de paille penche : un fil pâle se lève. "
    "Raphaël veut sauter les marches avec, avant que le vent ne l'emporte. "
    "Il s'élance trop vite : le chapeau se soulève. Sarah ne dit rien. "
    "T1 = chapeau / ruban / aile, les trois restent. "
    "T2 = chemin (le vent tire), bac (le sable trompe), rampe (le fil s'accroche). "
    "T3 = tenir, attendre, ou confier. Le fil pâle se couche. Il saute."
)
CHARS = "Raphaël, Sarah, papa, maman"
SETTING = "maison de bois au bord de la mer : rampe, chemin de sable, bac aux coquilles"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": {
        "rate": "medium", "wpm": 142, "speed": 0.98, "piper": 1.12,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 500, "sentence": 260,
        "energy": "warm", "contour": "storytelling", "noise": 0.36,
        "emphasis": "fil pâle",
        "note": "arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_fil_pale_montre_le_vent; tempo=naturel; sourire=léger; respiration=ample",
    },
    "choice": {
        "rate": "slow", "wpm": 116, "speed": 0.84, "piper": 1.30,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 900, "sentence": 330,
        "energy": "focused", "contour": "rising", "noise": 0.33,
        "emphasis": None,
        "note": "arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_le_saut; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    },
    "clue": {
        "rate": "slow", "wpm": 120, "speed": 0.86, "piper": 1.27,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "soft", "db": -2, "pause": 700, "sentence": 320,
        "energy": "focused", "contour": "rising", "noise": 0.32,
        "emphasis": None,
        "note": "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qu_il_tient; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    },
    "confirm": {
        "rate": "medium", "wpm": 132, "speed": 0.92, "piper": 1.20,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 450, "sentence": 280,
        "energy": "bright", "contour": "falling", "noise": 0.34,
        "emphasis": "chapeau de paille",
        "note": "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=la_première_idée_a_raté; tempo=naturel; sourire=léger; respiration=fluide",
    },
    "action": {
        "rate": "medium", "wpm": 146, "speed": 1.0, "piper": 1.10,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 420, "sentence": 250,
        "energy": "lively", "contour": "dynamic", "noise": 0.37,
        "emphasis": None,
        "note": "arc=action; intention=entraîner; emotion=élan_puis_décrochage; intensite=2; destinataire=enfant; sous_texte=sauter_trop_vite_fait_lever_le_chapeau; tempo=vif; sourire=léger; respiration=courte",
    },
    "obstacle": {
        "rate": "medium", "wpm": 134, "speed": 0.93, "piper": 1.18,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "medium", "db": 0, "pause": 520, "sentence": 300,
        "energy": "tense", "contour": "dynamic", "noise": 0.34,
        "emphasis": None,
        "note": "arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_inquiétude; intensite=2; destinataire=enfant; sous_texte=le_vent_ruse_plus_fort; tempo=resserré; sourire=aucun; respiration=retenue",
    },
    "resolution": {
        "rate": "medium", "wpm": 140, "speed": 0.97, "piper": 1.14,
        "pitch": "medium", "pitchSsml": "medium", "pitchTag": None,
        "volume": "medium", "db": 0, "pause": 560, "sentence": 270,
        "energy": "bright", "contour": "falling", "noise": 0.35,
        "emphasis": None,
        "note": "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=tenir_attendre_ou_confier_sauve_le_saut; tempo=naturel; sourire=franc; respiration=relâchée",
    },
    "ending": {
        "rate": "slow", "wpm": 118, "speed": 0.85, "piper": 1.28,
        "pitch": "low", "pitchSsml": "-2st", "pitchTag": "low-pitch",
        "volume": "soft", "db": -3, "pause": 900, "sentence": 340,
        "energy": "calm", "contour": "falling", "noise": 0.31,
        "emphasis": "fil pâle",
        "note": "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_fil_pale_se_couche_le_chapeau_revient; tempo=posé; sourire=léger; respiration=ample",
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
    "narrateur|Après la baignade, la maison de bois sèche.",
    "narrateur|Une planche fait tic, puis une autre.",
    "narrateur|Raphaël compte les tics avec ses orteils.",
    "narrateur|Les chaussures mouillées gardent un peu de mer.",
    "papa|J'étends la serviette, merci Sarah.",
    "narrateur|La serviette rayée claque une fois, puis se tait.",
    "maman|Le sel pique, tu le sens ?",
    "enfant-m|Ça pique le nez.",
    "narrateur|Sur la rampe, un chapeau de paille penche.",
    "narrateur|Un fil pâle se lève sur le bord.",
    "enfant-f|Le fil.",
    "narrateur|Sarah pose une main sur le bois.",
    "enfant-m|Je saute avec, jusqu'en bas !",
    "narrateur|En ce moment, il pose le chapeau.",
    "narrateur|Il plie les genoux, trop vite.",
    "narrateur|Le fil pâle se dresse, raide.",
    "narrateur|Le chapeau se soulève, presque parti.",
    "enfant-m|Il s'envole !",
    "narrateur|Le sourire de Raphaël disparaît.",
    "maman|Tu l'as senti, le vent ?",
    "narrateur|Papa s'accroupit, à la même hauteur.",
    "papa|On le garde, et on saute comment ?",
]

T1_CHOICE = [
    "narrateur|Le chapeau de paille attend, entre leurs mains.",
    "narrateur|Sur la tête, au ruban, ou contre l'aile.",
    "papa|Tu le prends comment, Raphaël ?",
]

T1 = {
    1: {
        "lab": "le chapeau",
        "sons": "paille,vent",
        "emphasis": "chapeau",
        "passage": [
            "narrateur|Raphaël pose le chapeau de paille sur sa tête.",
            "enfant-m|Il est à moi.",
            "narrateur|Le fil pâle se lève, près de son oreille.",
            "enfant-f|Le fil.",
            "narrateur|Sarah ne bouge pas.",
            "papa|Tu sautes avec, sur la tête ?",
            "enfant-m|Oui, un grand saut !",
            "narrateur|Il s'élance, les genoux trop pliés.",
            "narrateur|Le chapeau bascule, et le fil se tend.",
            "enfant-m|Il part !",
            "maman|Le vent l'a touché.",
            "narrateur|Le sourire de Raphaël disparaît.",
            "narrateur|Sarah pose deux mains sur le bois, sans un mot.",
            "papa|On le rattrape, d'abord.",
        ],
        "question": [
            "narrateur|La paille a recouvert ses cheveux.",
            "maman|Raphaël a mis quoi, sur sa tête ?",
        ],
        "qfields": {
            "expected_answer": "le chapeau",
            "accepted_examples": "chapeau | le chapeau | un chapeau | chapeau de paille | la paille",
            "retry_prompt": "Raphaël a mis le chapeau. Il a mis quoi ?",
        },
        "confirm": [
            "enfant-m|Le chapeau.",
            "papa|Oui, sur ta tête.",
            "narrateur|Raphaël le remet, un peu de travers.",
            "maman|Le fil pâle se lève moins.",
            "enfant-f|Moins.",
            "narrateur|Sarah a parlé, puis s'est tue.",
            "enfant-m|Je veux sauter, plus loin.",
            "papa|On choisit où, alors.",
            "narrateur|Le chapeau de paille reste à lui.",
        ],
    },
    2: {
        "lab": "le ruban",
        "sons": "tissu,vent",
        "emphasis": "ruban",
        "passage": [
            "narrateur|Raphaël pince le ruban rouge, mince.",
            "enfant-m|Je le tiens, comme une laisse.",
            "papa|Il est cousu au chapeau, tu vois.",
            "narrateur|Le ruban bat sa joue, puis s'étire.",
            "enfant-f|Le fil pâle, là.",
            "narrateur|Sarah montre le bord, sans se lever.",
            "enfant-m|Je tire, et je saute !",
            "narrateur|Il tire trop fort.",
            "narrateur|Le chapeau tourne, le fil indique la mer.",
            "enfant-m|Il me glisse !",
            "maman|Le ruban a filé entre tes doigts.",
            "narrateur|Dans sa poitrine, l'envie se bouscule.",
            "narrateur|Sarah reste assise, les yeux sur le fil.",
            "papa|On le reprend, sans tirer.",
        ],
        "question": [
            "narrateur|Un fil rouge reste collé à sa paume.",
            "papa|Raphaël tenait quoi ?",
        ],
        "qfields": {
            "expected_answer": "le ruban",
            "accepted_examples": "ruban | le ruban | un ruban | ruban rouge | le fil rouge",
            "retry_prompt": "Raphaël tenait le ruban. Il tenait quoi ?",
        },
        "confirm": [
            "enfant-m|Le ruban.",
            "maman|Oui.",
            "narrateur|Le ruban se calme, collé à la joue.",
            "papa|Le chapeau de paille n'est pas parti.",
            "enfant-f|Le fil, trop.",
            "narrateur|Sarah s'arrête au milieu du mot.",
            "enfant-m|Je saute plus loin.",
            "maman|On choisit l'endroit.",
            "narrateur|Le ruban reste dans sa main.",
        ],
    },
    3: {
        "lab": "l'aile",
        "sons": "paille,bois",
        "emphasis": "aile",
        "passage": [
            "narrateur|Raphaël plaque l'aile contre son ventre.",
            "enfant-m|Les deux mains, comme ça.",
            "maman|Tes pieds veulent sauter, tes mains tiennent.",
            "narrateur|Le fil pâle dépasse, entre ses pouces.",
            "enfant-f|Il se lève.",
            "narrateur|Sarah parle bas, et s'arrête.",
            "enfant-m|Je saute, les mains dessus !",
            "narrateur|Il plie les genoux, les mains occupées.",
            "narrateur|Le saut est trop petit, le chapeau penche.",
            "enfant-m|Je n'arrive pas plus haut.",
            "papa|Tes mains sont prises.",
            "narrateur|Le sourire s'en va.",
            "narrateur|Sarah pose une paume sur l'aile, légère.",
            "maman|Elle t'aide à le garder.",
        ],
        "question": [
            "narrateur|La paille est chaude contre son ventre.",
            "maman|Raphaël pressait quoi, contre lui ?",
        ],
        "qfields": {
            "expected_answer": "l'aile",
            "accepted_examples": "aile | l'aile | l aile | le bord | le chapeau | chapeau",
            "retry_prompt": "Raphaël pressait l'aile. Il pressait quoi ?",
        },
        "confirm": [
            "enfant-m|L'aile.",
            "papa|Oui, contre toi.",
            "narrateur|L'aile se réchauffe, sous ses paumes.",
            "maman|Le chapeau de paille n'a pas volé.",
            "enfant-f|Mes mains aussi.",
            "narrateur|Sarah les retire, puis se tait.",
            "enfant-m|Je veux un vrai saut.",
            "papa|On choisit où, d'abord.",
            "narrateur|L'aile reste sous ses doigts.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le chapeau penche sur ses cheveux, un peu.",
        "narrateur|Le chemin, le bac, ou la rampe.",
        "papa|Tu sautes où, Raphaël ?",
    ],
    2: [
        "narrateur|Le ruban rouge bat, puis se tait.",
        "narrateur|Le chemin, le bac, ou la rampe.",
        "maman|Tu sautes où, Raphaël ?",
    ],
    3: [
        "narrateur|L'aile reste chaude, sous ses doigts.",
        "narrateur|Le chemin, le bac, ou la rampe.",
        "papa|Tu sautes où, Raphaël ?",
    ],
}

T2 = {
    (1, 1): {
        "sons": "sable,vent",
        "emphasis": "chemin",
        "passage": [
            "narrateur|Raphaël prend le chemin de sable, chapeau sur la tête.",
            "narrateur|Le sable est tiède, et ses pieds font toc.",
            "enfant-m|Je saute loin !",
            "narrateur|Sarah reste au bord, les pieds dans l'ombre.",
            "enfant-f|Le fil, devant.",
            "narrateur|Le vent ne soulève plus : il tire vers la mer.",
            "narrateur|Le fil pâle pointe un creux, entre deux dunes.",
            "papa|Il voudrait cacher le chapeau, là-bas.",
            "enfant-m|Je cours le rattraper !",
            "narrateur|Sarah secoue la tête, minuscule.",
            "maman|Elle ne dit rien, et ça compte.",
            "narrateur|Le chapeau glisse vers l'avant, presque hors des cheveux.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 1): {
        "sons": "sable,tissu",
        "emphasis": "chemin",
        "passage": [
            "narrateur|Le ruban rouge bat sur le chemin, comme un drapeau.",
            "narrateur|Raphaël court, puis saute, et le fil claque.",
            "enfant-m|Il vole !",
            "narrateur|Sarah marche derrière, sans courir.",
            "enfant-f|Trop vite.",
            "narrateur|Le vent tire le ruban vers un creux de sable.",
            "narrateur|Le fil pâle indique le creux, pas le ciel.",
            "papa|Le chapeau veut se cacher, pas s'envoler.",
            "enfant-m|Je tire plus fort !",
            "narrateur|Sarah pose le pied, et s'arrête.",
            "maman|Elle a dit non, sans le mot.",
            "narrateur|Le ruban s'enroule un peu autour du poignet.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (3, 1): {
        "sons": "sable,paille",
        "emphasis": "chemin",
        "passage": [
            "narrateur|Raphaël serre l'aile, et entre sur le chemin.",
            "narrateur|Le sable gicle, puis retombe.",
            "enfant-m|Je saute, je le plaque !",
            "narrateur|Sarah reste deux pas en arrière.",
            "enfant-f|Tes mains.",
            "narrateur|Le vent pousse l'aile hors des paumes, vers un creux.",
            "narrateur|Le fil pâle penche vers ce trou de sable.",
            "papa|Il veut glisser là-dedans.",
            "enfant-m|Je le rattrape en courant !",
            "narrateur|Sarah ouvre la bouche, puis la referme.",
            "maman|Son silence te retient.",
            "narrateur|L'aile frotte le sable, presque lâchée.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (1, 2): {
        "sons": "sable,coquille",
        "emphasis": "bac",
        "passage": [
            "narrateur|Raphaël arrive au bac, le chapeau trop grand.",
            "narrateur|Le sable du bac est chaud, un peu rêche.",
            "enfant-m|Je saute dedans !",
            "narrateur|Il saute, et l'aile se remplit de grains.",
            "maman|On dirait un seau, ton chapeau.",
            "enfant-m|Il est lourd, maintenant.",
            "enfant-f|Lourd, c'est bien ?",
            "narrateur|Sarah s'accroupit au bord, sans sauter.",
            "narrateur|Une rafale vide l'aile, d'un seul coup.",
            "papa|Le sable trompait : le vent revient.",
            "narrateur|Le fil pâle se dresse au-dessus du bac.",
            "enfant-m|Il veut partir, là !",
            "papa|Vous faites quoi, alors ?",
        ],
    },
    (2, 2): {
        "sons": "sable,tissu",
        "emphasis": "bac",
        "passage": [
            "narrateur|Raphaël penche le ruban au-dessus du bac.",
            "narrateur|Le sable colle au fil rouge, en virgule.",
            "enfant-m|Je le garde hors du sable.",
            "papa|On saute, le ruban en l'air.",
            "narrateur|Il saute au bord, et le ruban plonge.",
            "maman|Une virgule rouge dans le bac.",
            "enfant-f|Sors-le.",
            "narrateur|Sarah ne plonge pas les mains.",
            "narrateur|Il tire, trop fort, et le chapeau penche.",
            "narrateur|Du sable tombe, puis une rafale le vide.",
            "papa|Lourd, puis léger : le vent ruse.",
            "narrateur|Le fil pâle pointe hors du bac.",
            "papa|Vous faites quoi, alors ?",
        ],
    },
    (3, 2): {
        "sons": "sable,paille",
        "emphasis": "bac",
        "passage": [
            "narrateur|Raphaël tient l'aile au-dessus du bac.",
            "narrateur|Un brin d'oyat croise le sable chaud.",
            "enfant-m|Je saute au bord !",
            "narrateur|Ses mains appuient, et l'aile se remplit.",
            "maman|Le poids le rassure, un instant.",
            "enfant-f|Attends.",
            "narrateur|Sarah reste hors du bac, les genoux pliés.",
            "narrateur|Une rafale chasse le sable, et l'aile se soulève.",
            "enfant-m|Il n'est plus lourd !",
            "papa|Le bac a menti, puis le vent a parlé.",
            "narrateur|Le fil pâle tremble au-dessus des grains.",
            "narrateur|Sarah pose une main sur le rebord, muette.",
            "papa|Vous faites quoi, alors ?",
        ],
    },
    (1, 3): {
        "sons": "bois,vent",
        "emphasis": "rampe",
        "passage": [
            "narrateur|Raphaël revient vers la rampe de bois.",
            "narrateur|C'est là que le chapeau séchait, tout à l'heure.",
            "enfant-m|Je saute les marches !",
            "narrateur|Il saute la première, trop vite.",
            "narrateur|La paille racle le bois, et le fil s'accroche.",
            "papa|Un clou a pris le fil pâle.",
            "enfant-m|Il est coincé !",
            "enfant-f|Ne tire pas.",
            "narrateur|Sarah pose le doigt près du clou, sans toucher.",
            "maman|Si tu sautes, tu déchires l'aile.",
            "narrateur|Raphaël sent l'envie et l'inquiétude, ensemble.",
            "narrateur|La rampe vibre sous ses pieds nus.",
            "papa|Vous faites comment, tous les deux ?",
        ],
    },
    (2, 3): {
        "sons": "bois,tissu",
        "emphasis": "rampe",
        "passage": [
            "narrateur|Sur la rampe, le ruban s'accroche à un clou.",
            "narrateur|Raphaël saute, et le fil tire en arrière.",
            "enfant-m|Il est coincé !",
            "maman|Le bois a pris le rouge.",
            "enfant-f|Le fil pâle aussi.",
            "narrateur|Sarah montre le clou, sans parler plus.",
            "papa|On le détache, sans tirer trop.",
            "narrateur|Il s'arrête sur la marche, le chapeau de travers.",
            "narrateur|Le ruban vibre, tendu entre le clou et lui.",
            "enfant-m|Je saute pour le libérer ?",
            "narrateur|Sarah secoue la tête.",
            "maman|Le clou est lisse, un peu de sel dessus.",
            "papa|Vous faites comment ?",
        ],
    },
    (3, 3): {
        "sons": "bois,paille",
        "emphasis": "rampe",
        "passage": [
            "narrateur|La rampe regarde la dune, tout droit.",
            "narrateur|Raphaël tient l'aile, face aux marches.",
            "enfant-m|Le vent me pousse !",
            "papa|Il vient de l'herbe, pas de la mer.",
            "narrateur|L'aile claque contre la rampe.",
            "narrateur|Le fil pâle s'enroule autour d'un clou.",
            "enfant-f|Stop.",
            "narrateur|Sarah a dit le mot, puis plus rien.",
            "enfant-m|Je saute plus haut.",
            "maman|Le fil te retient, et il peut casser.",
            "narrateur|Une graine d'oyat reste sur le bord.",
            "narrateur|Raphaël serre l'aile, trop fort.",
            "papa|Vous faites comment ?",
        ],
    },
}

T3_LABS = {
    1: ("je le tiens", "j'attends", "je le donne"),
    2: ("je le vide", "je m'accroupis", "je le pose"),
    3: ("je décroche", "je compte", "papa le garde"),
}

T3_CHOICE = {
    1: [
        "narrateur|Sur le chemin, le fil pâle penche vers le creux.",
        "narrateur|Sarah n'a pas bougé.",
        "papa|Tu le tiens, tu attends, ou tu le donnes ?",
    ],
    2: [
        "narrateur|Dans le bac, le sable a menti, puis le vent.",
        "narrateur|Le fil pâle se dresse au-dessus.",
        "maman|Tu le vides, tu t'accroupis, ou tu le poses ?",
    ],
    3: [
        "narrateur|Sur la rampe, le fil pâle tient au clou.",
        "narrateur|Sarah a dit stop, puis s'est tue.",
        "papa|Tu décroches, tu comptes, ou papa le garde ?",
    ],
}

T3_SONS = {
    (1, 1): "sable,paille",
    (1, 2): "vent,silence",
    (1, 3): "pas,serviette",
    (2, 1): "sable,grain",
    (2, 2): "sable,souffle",
    (2, 3): "bois,sable",
    (3, 1): "clou,paille",
    (3, 2): "bois,voix",
    (3, 3): "bois,vent",
}

T3_EMPH = {
    1: {1: "fil pâle", 2: "fil pâle", 3: "chapeau"},
    2: {1: "sable", 2: "fil pâle", 3: "chapeau"},
    3: {1: "fil pâle", 2: "marches", 3: "chapeau"},
}

OBJ = {
    1: "Le chapeau reste sur sa tête, un peu de travers.",
    2: "Le ruban se tait, collé à sa joue.",
    3: "L'aile se réchauffe, sous une paume.",
}


def t3_core(a: int, b: int, c: int) -> list[str]:
    obj = OBJ[a]
    if b == 1 and c == 1:
        extra = {
            1: "Il pince le fil pâle, sous le bord du chapeau.",
            2: "Il enroule le ruban, et pince le fil pâle.",
            3: "Ses deux mains tiennent l'aile, et le fil pâle.",
        }[a]
        return [
            "enfant-m|Je le tiens.",
            f"narrateur|{extra}",
            "narrateur|Sarah ne saute pas.",
            "enfant-f|Toi.",
            "narrateur|Il saute, le fil pâle entre le pouce et l'index.",
            "enfant-m|Il n'est pas parti.",
            f"narrateur|{obj}",
            "papa|Tu l'as gardé, pendant le saut.",
            "maman|Tes pieds ont dansé, tes mains aussi.",
        ]
    if b == 1 and c == 2:
        extra = {
            1: "Le chapeau repose sur ses genoux, sur le sable.",
            2: "Le ruban cesse de battre, contre sa jambe.",
            3: "L'aile s'aplatit, sur ses cuisses.",
        }[a]
        return [
            "enfant-m|J'attends.",
            "narrateur|Raphaël s'arrête sur le chemin, le souffle haut.",
            "narrateur|Sarah s'assoit, sans un mot.",
            f"narrateur|{extra}",
            "enfant-f|Le fil.",
            "narrateur|Le fil pâle se couche, lentement.",
            "papa|Maintenant, un saut.",
            "narrateur|Il saute, simple, le chapeau avec lui.",
            f"narrateur|{obj}",
        ]
    if b == 1 and c == 3:
        extra = {
            1: "Sarah reçoit le chapeau, les deux mains ouvertes.",
            2: "Sarah reçoit le ruban, puis le chapeau.",
            3: "Sarah reçoit l'aile, chaude de ses paumes.",
        }[a]
        return [
            "enfant-m|Je le donne.",
            "narrateur|Raphaël tend le chapeau de paille, chaud.",
            f"narrateur|{extra}",
            "enfant-f|Le fil, moi.",
            "narrateur|Elle pince le fil pâle, et se tait.",
            "papa|Je le vois, va.",
            "narrateur|Raphaël saute libre, les cheveux au vent.",
            "enfant-m|Plus haut !",
            f"narrateur|{obj}",
        ]
    if b == 2 and c == 1:
        extra = {
            1: "Il penche le chapeau, et l'or retombe.",
            2: "Il soulève le ruban, et les grains glissent.",
            3: "Il incline l'aile, grain après grain.",
        }[a]
        return [
            "enfant-m|Je le vide.",
            f"narrateur|{extra}",
            "narrateur|Sarah reste au bord, les mains sur le bois.",
            "enfant-f|Le fil.",
            "narrateur|Le fil pâle ne se dresse plus.",
            "papa|Vide, il peut sauter.",
            "narrateur|Il saute un petit saut, au bord du bac.",
            "enfant-m|Mes mains l'ont tenu.",
            f"narrateur|{obj}",
        ]
    if b == 2 and c == 2:
        extra = {
            1: "Le chapeau s'assoit avec lui, au bord.",
            2: "Le ruban retombe, sans plonger.",
            3: "L'aile reste à plat, sur ses genoux.",
        }[a]
        return [
            "enfant-m|Je m'accroupis.",
            "narrateur|Il s'assoit au bord du bac, l'aile à plat.",
            "narrateur|Sarah s'accroupit en face, sans parler.",
            f"narrateur|{extra}",
            "enfant-f|Plus de vent.",
            "narrateur|Le fil pâle se couche sur le sable.",
            "maman|Tu peux sauter, tout petit.",
            "narrateur|Il remet l'aile, puis saute un saut court.",
            f"narrateur|{obj}",
        ]
    if b == 2 and c == 3:
        extra = {
            1: "Le chapeau sèche hors du bac, sur une planche.",
            2: "Le ruban pend hors du bac, sans sable.",
            3: "L'aile repose à plat, hors des grains.",
        }[a]
        return [
            "enfant-m|Je le pose.",
            "narrateur|Il pose le chapeau à côté du bac.",
            "narrateur|Sarah le surveille, les yeux sur le fil pâle.",
            f"narrateur|{extra}",
            "enfant-f|Il reste.",
            "papa|Le bac est à toi, le chapeau à nous.",
            "narrateur|Raphaël saute dans le sable, les cheveux libres.",
            "enfant-m|Je saute sans lui !",
            f"narrateur|{obj}",
        ]
    if b == 3 and c == 1:
        extra = {
            1: "Le chapeau se libère, un fil de paille sur le clou.",
            2: "Le ruban quitte le clou, lisse, dans sa main.",
            3: "L'aile se dégage, le fil pâle entre ses doigts.",
        }[a]
        return [
            "enfant-m|Je décroche.",
            "narrateur|Une main sur la rampe, une main sur le fil pâle.",
            "narrateur|Il glisse le fil hors du clou, sans tirer.",
            "enfant-f|Oui.",
            "narrateur|Sarah a soufflé ce mot, puis plus rien.",
            f"narrateur|{extra}",
            "papa|Tu as tenu les deux.",
            "narrateur|Il saute la marche, court.",
            f"narrateur|{obj}",
        ]
    if b == 3 and c == 2:
        extra = {
            1: "Le chapeau attend sur la marche, pendant le compte.",
            2: "Le ruban cesse de vibrer, entre deux nombres.",
            3: "L'aile s'apaise, sous le compte de Sarah.",
        }[a]
        return [
            "enfant-m|Je compte.",
            "narrateur|Il pose le chapeau sur la marche.",
            "enfant-m|Un, deux.",
            "narrateur|Sarah ne dit pas trois.",
            "enfant-f|Le fil.",
            "narrateur|Le fil pâle se couche, le bois ne claque plus.",
            f"narrateur|{extra}",
            "papa|Le bois ne claque plus.",
            "narrateur|Il reprend l'aile, puis saute une marche.",
            f"narrateur|{obj}",
        ]
    extra = {
        1: "Papa pose le chapeau sur la rampe, droit.",
        2: "Papa tient le ruban, hors du clou.",
        3: "Papa garde l'aile, à hauteur d'enfant.",
    }[a]
    return [
        "enfant-m|Papa le garde.",
        f"narrateur|{extra}",
        "papa|Je le garde, va.",
        "narrateur|Sarah pince le fil pâle, dans les mains de papa.",
        "enfant-f|D'accord.",
        "narrateur|Raphaël saute, les mains libres, léger.",
        "enfant-m|Je saute les marches !",
        "maman|Le chapeau ne bouge plus, sur le bois.",
        f"narrateur|{obj}",
    ]


CLUE_PAY = {
    1: "Le fil pâle du début se couche, sur le bord.",
    2: "Le fil pâle du début ne pointe plus le creux.",
    3: "Le fil pâle du début a quitté le clou.",
}


def t3_pass(a: int, b: int, c: int) -> list[str]:
    rows = t3_core(a, b, c)
    rows.append(f"narrateur|{CLUE_PAY[b]}")
    return rows


END_SONS = {1: "oiseau,vague", 2: "oiseau,vague", 3: "bois,vague"}

END_CODA = {
    1: "Un grain de sel a séché sur la paille.",
    2: "Le ruban garde un grain, rouge de poussière.",
    3: "L'aile sent le bois, et un peu le soleil.",
}

LAST = {
    (1, 1, 1): "L'aile jaune ne bouge plus, sur le chemin.",
    (1, 1, 2): "Le chapeau attendait, plat, puis il a sauté.",
    (1, 1, 3): "Papa rend le jaune, après le grand saut.",
    (1, 2, 1): "Un grain d'or reste dans la paille.",
    (1, 2, 2): "Le bac garde un rond d'ombre jaune.",
    (1, 2, 3): "Le chapeau sèche dans les mains de Sarah.",
    (1, 3, 1): "La rampe a un fil de paille, mince.",
    (1, 3, 2): "Le bois attendait, le chapeau sur les genoux.",
    (1, 3, 3): "Le chapeau est revenu sur la rampe, droit.",
    (2, 1, 1): "Le ruban rouge ne claque plus.",
    (2, 1, 2): "Le ruban s'est calmé, collé à la joue.",
    (2, 1, 3): "Sarah tient le fil, sans un mot.",
    (2, 2, 1): "Un fil rouge reste dans le sable du bac.",
    (2, 2, 2): "Le bac a une virgule rouge, fine.",
    (2, 2, 3): "Maman démêle le ruban, hors du bac.",
    (2, 3, 1): "Le ruban a quitté le clou de la rampe.",
    (2, 3, 2): "Le bois garde une ombre rose.",
    (2, 3, 3): "Le ruban revient, lisse, dans sa main.",
    (3, 1, 1): "Une herbe verte reste sur l'aile.",
    (3, 1, 2): "Le chapeau a attendu dans l'ombre du chemin.",
    (3, 1, 3): "Papa rend le chapeau, face à la mer.",
    (3, 2, 1): "Un brin d'oyat croise le bac.",
    (3, 2, 2): "Le sable gris-vert s'est tu.",
    (3, 2, 3): "Maman souffle une graine hors de la paille.",
    (3, 3, 1): "La rampe a une ombre d'herbe, étroite.",
    (3, 3, 2): "Le bois sent la dune, un peu.",
    (3, 3, 3): "Le chapeau est rentré, vert d'ombre, puis sec.",
}


def ending(a: int, b: int, c: int) -> list[str]:
    cd = END_CODA[a]
    last = LAST[(a, b, c)]
    tick = "Une planche de la maison fait tic, puis se tait."

    if b == 1 and c == 1:
        return [
            "enfant-m|J'ai sauté, avec.",
            "papa|Merci d'avoir tenu le fil.",
            "narrateur|Sarah hoche la tête, sans parler.",
            f"narrateur|{cd}",
            "maman|Le chapeau de paille est à toi.",
            f"narrateur|{tick}",
            f"narrateur|{last}",
        ]
    if b == 1 and c == 2:
        return [
            "enfant-m|J'ai attendu le vent.",
            "maman|Puis tu as sauté, simple.",
            "papa|Merci d'avoir pris le temps.",
            "enfant-f|Le fil.",
            f"narrateur|{cd}",
            f"narrateur|{tick}",
            f"narrateur|{last}",
        ]
    if b == 1 and c == 3:
        return [
            "enfant-m|Vous l'avez gardé, pour moi.",
            "papa|Et toi, tu as sauté.",
            "maman|Merci, Sarah, d'avoir pincé le fil.",
            "narrateur|Il le remet, un peu de travers, puis droit.",
            f"narrateur|{cd}",
            f"narrateur|{tick}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 1:
        return [
            "enfant-m|Je l'ai vidé, puis sauté.",
            "papa|Merci d'avoir versé le sable.",
            "narrateur|Sarah essuie un grain sur l'aile.",
            f"narrateur|{cd}",
            "maman|Le bac t'a rendu le chapeau.",
            f"narrateur|{tick}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 2:
        return [
            "enfant-m|On s'est accroupis.",
            "papa|Merci d'avoir regardé le fil.",
            "enfant-f|Il s'est couché.",
            f"narrateur|{cd}",
            "narrateur|Ils restent un peu au bord, sans courir.",
            f"narrateur|{tick}",
            f"narrateur|{last}",
        ]
    if b == 2 and c == 3:
        return [
            "enfant-m|Je l'ai posé, pour sauter.",
            "maman|Merci de l'avoir laissé hors du bac.",
            "narrateur|Sarah le lui tend, le fil pâle à plat.",
            f"narrateur|{cd}",
            "papa|Le saut, et le chapeau, tous les deux.",
            f"narrateur|{tick}",
            f"narrateur|{last}",
        ]
    if b == 3 and c == 1:
        return [
            "enfant-m|Je l'ai décroché.",
            "papa|Merci d'avoir glissé le fil, sans tirer.",
            "enfant-f|Le clou.",
            f"narrateur|{cd}",
            "maman|La rampe te le rend.",
            f"narrateur|{tick}",
            f"narrateur|{last}",
        ]
    if b == 3 and c == 2:
        return [
            "enfant-m|J'ai compté.",
            "maman|Merci d'avoir laissé le trois à Sarah.",
            "narrateur|Sarah n'a pas dit trois, et ça a suffi.",
            f"narrateur|{cd}",
            "papa|Le bois a attendu avec vous.",
            f"narrateur|{tick}",
            f"narrateur|{last}",
        ]
    return [
        "enfant-m|Papa l'a gardé.",
        "papa|Merci de me l'avoir confié.",
        "narrateur|Sarah lâche le fil pâle, dans ses mains.",
        "maman|Le chapeau te revient.",
        f"narrateur|{cd}",
        f"narrateur|{tick}",
        f"narrateur|{last}",
    ]


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "bois,vague",
        {"emphasis": "fil pâle"},
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"], T1_CHOICE, "choice", "",
        {"fields": t3lab("le chapeau", "le ruban", "l'aile"), "pause_before": 200},
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
            {"emphasis": "chapeau de paille"},
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"], T2_CHOICE[a], "choice", "",
            {"fields": t3lab("le chemin", "le bac", "la rampe"), "pause_before": 200},
        )
        for b in (1, 2, 3):
            bse = f"{base}_T0002_P000{b}"
            out_chunks[bse] = voice(
                by_src[bse], T2[(a, b)]["passage"], "obstacle", T2[(a, b)]["sons"],
                {"emphasis": T2[(a, b)]["emphasis"]},
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"], T3_CHOICE[b], "choice", "",
                {"fields": t3lab(*T3_LABS[b]), "pause_before": 200},
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf], t3_pass(a, b, c), "resolution", T3_SONS[(b, c)],
                    {"emphasis": T3_EMPH[b][c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin], ending(a, b, c), "ending", END_SONS[a],
                    {"emphasis": "fil pâle"},
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
        "cette énergie n'est pas une faute",
        "on peut jouer ou attendre",
        "on peut demander à un adulte",
        "bravo tu as",
        "bon travail",
        "lina",
        "jules",
        "sami",
        "tom ",
        "léa",
        "tout doux",
        "tout calme",
        "tout lent",
        "aujourd'hui",
        "merle",
        "couleur de miel",
        "j'ai une idée",
        "j'ai compris",
        "celui où j'ai compris",
        "il faut attendre",
        "mission accomplie",
        "gouttes pendent",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan/calque: {bad}")
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "raphaël" not in blob and "raphael" not in blob:
        raise SystemExit(f"{SID}: Raphaël absent")
    if "sarah" not in blob:
        raise SystemExit(f"{SID}: Sarah absente")
    if "enfant-f|" not in blob:
        raise SystemExit(f"{SID}: enfant-f absent")
    if "fil pâle" not in blob:
        raise SystemExit(f"{SID}: fil pâle absent")

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
    if min(counts) < 500:
        raise SystemExit(f"chemins trop courts: {min(counts)}")
    if max(counts) > 780:
        raise SystemExit(f"chemins trop longs: {max(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        "# TREE-DIF-010 — Le chapeau de paille et Raphaël qui saute\n\n"
        "- **Public :** N3 (5–6 ans), audio familial\n"
        "- **Leçon :** DIF.ENE.001 — l'énergie n'est pas une faute ; "
        "jouer, attendre, demander (vécue, jamais dite)\n"
        "- **Personnages :** Raphaël, Sarah, papa, maman\n"
        "- **Lieu :** maison de bois au bord de la mer : rampe, chemin de sable, "
        "bac aux coquilles\n"
        "- **Structure conservée :** 86 nœuds, 27 chemins, 27 fins textuellement distinctes\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` / graphe `option_*_next` inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Après la baignade, la maison de bois sèche, tic par tic. "
        "Sur la rampe, un chapeau de paille penche. Un fil pâle se lève. "
        "Raphaël veut sauter les marches avec, avant que le vent ne l'emporte. "
        "Il s'élance trop vite : le chapeau se soulève. Sarah ne dit rien. "
        "Chapeau, ruban ou aile : les trois restent. "
        "Chemin (le vent tire vers un creux), bac (le sable trompe, puis le vent vide), "
        "rampe (le fil pâle s'accroche au clou). "
        "Tenir, attendre, confier ; vider, s'accroupir, poser ; décrocher, compter, "
        "papa le garde. Le fil pâle se couche. Il saute. Une planche fait tic.\n\n"
        "## Vécu\n\n"
        "Raphaël veut sauter **maintenant**, le chapeau sur la tête. "
        "Sarah prend son temps : un mot, puis le silence. "
        "Première idée : s'élancer trop vite. Ça rate. "
        "Chaque choix change l'obstacle et le climax (creux, sable menteur, clou). "
        "La leçon se voit : l'élan reste ; tenir, attendre ou confier sauve le saut. "
        "Fin : grain de sel sur la paille + tic de la maison + image unique du chemin.\n\n"
        "## Vu et corrigé\n\n"
        "- Lina / Sarah-héroïne / slogans DIF.ENE / bac-toboggan-dînette jetés.\n"
        "- Tics « encore / déjà / tout doux / tout calme / tout lent » retirés.\n"
        "- Héros Raphaël (`enfant-m`), Sarah (`enfant-f`), rythmes distincts, "
        "silence = réponse.\n"
        "- T1 ne retire pas l'équipement. T1/T2/T3 changent l'action. 9 T2, 27 T3, 27 fins.\n"
        "- Indice unique dès l'ouverture : le fil pâle, payé au climax.\n"
        "- Merci vécu. Question d'adulte. Un « en ce moment ».\n"
        "- TTS complet (86) : `text_ssml`, `text_xai_tags`, `notes` (arc, intention, émotion, "
        "intensité, destinataire, sous-texte, tempo, sourire, respiration). "
        "`slow` = choix, indice, fin. Action plus vive.\n"
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
