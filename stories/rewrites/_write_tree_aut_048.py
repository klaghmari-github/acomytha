#!/usr/bin/env python3
"""TREE-AUT-048 — Le seau rouge de Nina près de la flaque (F-NAR-019, N1)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-048"
N1 = LIMITS["N1"]
TITLE = "Le seau rouge de Nina près de la flaque"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)
EXTRA_BAD = (
    "aujourd'hui",
    "merle",
    "miel",
    "grand-père",
    "grand-pere",
    "maîtresse",
    "maitresse",
    "jardinier",
    "bibliothécaire",
    "bibliothecaire",
    "gardienne",
    "j'ai compris",
    "mission accomplie",
    "on dirait que notre mission",
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="perle de verre",
        note=(
            "arc=installation; intention=émerveiller; emotion=impatience; "
            "intensite=2; destinataire=enfant; sous_texte=deux_désirs_une_flaque; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note=(
            "arc=choix; intention=inviter; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=ton_choix_change_la_manière; "
            "tempo=suspendu; sourire=léger; respiration=pause_avant_choix"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="seau",
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=elle_reprend_ce_qui_est_à_elle; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="seau",
        note=(
            "arc=confirmation; intention=relancer; emotion=espoir_discret; intensite=1; "
            "destinataire=enfant; sous_texte=l_objet_revient_dans_les_mains; "
            "tempo=naturel; sourire=léger; respiration=fluide"
        ),
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note=(
            "arc=action; intention=entraîner; emotion=impatience; intensite=2; "
            "destinataire=enfant; sous_texte=elle_pose_le_seau_trop_vite; "
            "tempo=vif; sourire=léger; respiration=courte"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; "
            "intensite=2; destinataire=enfant; sous_texte=un_faux_rouge_ment_la_perle_dit_vrai; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="perle de verre",
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=elle_soulève_sans_tirer; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="perle",
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=la_perle_et_le_dernier_rond_paient_le_début; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}

Q_FIELDS = {
    1: {
        "expected_answer": "seau",
        "accepted_examples": "seau | le seau | seau rouge | le seau rouge",
        "retry_prompt": "Le seau rouge. Nina a pris quoi ?",
    },
    2: {
        "expected_answer": "manteau",
        "accepted_examples": "manteau | le manteau | manteau gris | le manteau gris",
        "retry_prompt": "Le manteau. Nina a pris quoi ?",
    },
    3: {
        "expected_answer": "doudou",
        "accepted_examples": "doudou | le doudou | doudou beige | le doudou beige",
        "retry_prompt": "Le doudou. Nina a pris quoi ?",
    },
}

LOC = {
    1: dict(name="le bac à sable", short="bac", sons="sable,seau"),
    2: dict(name="le toboggan", short="toboggan", sons="metal,glisse"),
    3: dict(name="les balançoires", short="balançoires", sons="chaine,bois"),
}
OBJ = {
    1: dict(name="le ballon", short="ballon", sons="ballon,rebond"),
    2: dict(name="le seau", short="seau", sons="seau,eau"),
    3: dict(name="le doudou", short="doudou", sons="tissu,doudou"),
}
LIEU = {
    1: dict(name="le banc", short="banc", sons="pierre,mousse"),
    2: dict(name="le portail", short="portail", sons="loquet,portail"),
    3: dict(name="la haie", short="haie", sons="feuilles,haie"),
}


def vet(lines: list[str]) -> list[str]:
    out: list[str] = []
    starts: list[str] = []
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
        if TICS.search(ph):
            raise SystemExit(f"tic: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"interdit {bad}: {ph}")
        for bad in EXTRA_BAD:
            if bad in low:
                raise SystemExit(f"extra {bad}: {ph}")
        tok = ph.split()[0].lower() if role == "narrateur" else ""
        starts.append(tok)
        out.append(f"{role}|{ph}")
    run = 1
    for i in range(1, len(starts)):
        if starts[i] and starts[i] == starts[i - 1]:
            run += 1
            if run >= 4:
                raise SystemExit(f"puces {starts[i]}")
        else:
            run = 1
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
    lines = vet(lines)
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if extra.get("note"):
        m["note"] = extra["note"]
    text, script = from_script(lines)
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
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
    out["night_policy"] = extra.get("night_policy", "play")
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    out.update(extra.get("fields") or {})
    for k, v in extra.items():
        if k in ("emphasis", "note", "pause_before_ms", "night_policy", "fields"):
            continue
        out[k] = v
    return out


def path_ids(a: int, b: int, c: int) -> list[str]:
    return [
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


# Ouverture : le lampadaire agit en cuillère. Indice unique = perle de verre.
OPENING = [
    "narrateur|Le lampadaire penche son ombre, comme une cuillère.",
    "narrateur|La cuillère touche la flaque du chemin.",
    "narrateur|Ploc.",
    "narrateur|Un seau rouge attend, près de l'eau.",
    "narrateur|L'anse est en corde, un peu rêche.",
    "narrateur|Sur la corde, une perle de verre brille.",
    "narrateur|Elle fait un éclair blanc, dans l'eau.",
    "narrateur|Un manteau gris sèche sur la pierre.",
    "maman|Nino, la flaque n'est pas un bain.",
    "copain|Je veux sauter, maintenant !",
    "enfant-f|Moi, je veux les ronds, dans le seau.",
    "narrateur|En ce moment, Nina touche l'anse.",
    "enfant-f|Les ronds, avant que le soleil les boive !",
    "papa|Tu le prends, le seau ?",
    "enfant-f|Oui, papa.",
    "narrateur|Elle plonge le seau, trop vite.",
    "narrateur|Nino saute, au même instant.",
    "narrateur|Les ronds se cassent, d'un coup.",
    "narrateur|Le sourire de Nina disparaît.",
    "enfant-f|Ils sont partis !",
    "narrateur|Papa s'accroupit, à sa hauteur.",
    "papa|Regarde la perle, Nina.",
    "maman|Où commences-tu, avec le seau ?",
]

T1_CHOICE = [
    "narrateur|Le parc a trois coins, pour commencer.",
    "papa|Le bac à sable, le toboggan, ou les balançoires ?",
    "maman|Le seau vient avec toi.",
]

T1 = {
    1: [
        "narrateur|Nina serre le seau, deux mains.",
        "narrateur|La perle de verre tape, contre elle.",
        "copain|Je fais une montagne, dans le bac !",
        "enfant-f|Moi, les ronds, dans le sable.",
        "narrateur|Elle pose le seau, trop vite.",
        "narrateur|Le sable mouillé avale l'anse, lourd.",
        "narrateur|Nino verse du sable, par-dessus.",
        "narrateur|Les ronds n'existent pas, ici.",
        "enfant-f|Il est trop lourd, maintenant.",
        "narrateur|Elle tire, et le sable vole.",
        "enfant-f|Je n'y arrive pas.",
        "narrateur|Le sourire de Nina disparaît.",
        "papa|La perle, vois, au bord.",
        "maman|Elle brille, pas sous le tas.",
        "narrateur|Ses mains s'arrêtent, collées de grains.",
    ],
    2: [
        "narrateur|Nina serre le seau contre elle.",
        "narrateur|Le métal du toboggan est froid, luisant.",
        "narrateur|Le manteau gris sèche sur une marche.",
        "copain|Je glisse, le premier !",
        "enfant-f|Mon seau glisse, comme un bateau.",
        "narrateur|Elle pose le seau en haut.",
        "narrateur|Il dévale, trop vite, et verse.",
        "narrateur|Le manteau glisse, lui aussi, loin.",
        "enfant-f|Tout est parti, en bas !",
        "narrateur|Le sourire de Nina disparaît.",
        "papa|Le seau, d'abord, puis le tissu.",
        "maman|La perle, vois, au bas du métal.",
        "narrateur|Ses épaules baissent, au bas.",
        "papa|Tu reprends le manteau, Nina ?",
        "narrateur|Une goutte glisse de la manche.",
    ],
    3: [
        "narrateur|Nina porte le seau vers les cordes.",
        "narrateur|Une chaîne fait tic, dans le vent.",
        "narrateur|Le doudou beige est sous le siège.",
        "copain|C'est ma balançoire, maintenant !",
        "enfant-f|Mon seau attrape les ronds, d'en haut.",
        "narrateur|Elle pose le seau sous le siège.",
        "narrateur|Nino pousse, trop fort, trop vite.",
        "narrateur|L'eau vole, et le doudou tombe.",
        "enfant-f|Tout est mouillé, par terre !",
        "narrateur|Le sourire de Nina disparaît.",
        "maman|Le doudou, vois, sous le bois.",
        "papa|La perle, elle, reste au seau.",
        "narrateur|Ses mains lâchent, un peu.",
        "papa|Tu reprends le doudou, Nina ?",
        "narrateur|La chaîne ne fait plus tic.",
    ],
}

T1_Q = {
    1: [
        "narrateur|L'anse rouge dépasse du sable.",
        "papa|Nina a pris quoi ?",
    ],
    2: [
        "narrateur|Le tissu gris était sur la marche.",
        "maman|Nina a pris quoi ?",
    ],
    3: [
        "narrateur|Le doudou était sous le siège.",
        "papa|Nina a pris quoi ?",
    ],
}

T1_C = {
    1: [
        "narrateur|Nina se baisse vers la corde.",
        "narrateur|Elle écarte le sable, grain par grain.",
        "narrateur|La perle de verre reparaît, froide.",
        "enfant-f|Je le reprends, il vient.",
        "maman|Merci, Nina, il est avec toi.",
        "papa|Tu le portes, pour les ronds ?",
        "enfant-f|Oui, je le garde.",
        "narrateur|Un grain reste au fond du seau.",
        "narrateur|Le manteau reste sur la pierre.",
        "enfant-f|Il ne s'enfonce plus.",
    ],
    2: [
        "narrateur|Nina descend les marches, une à une.",
        "narrateur|Elle ramasse le tissu gris, au bas.",
        "narrateur|Le seau l'attend, près du métal.",
        "enfant-f|Je le reprends, il est froid.",
        "papa|Merci, Nina, il est avec toi.",
        "maman|Tu le portes, pour la maison ?",
        "enfant-f|Oui, je le serre.",
        "narrateur|Une feuille reste collée au tissu.",
        "narrateur|La perle de verre cliquette, contre elle.",
        "enfant-f|Le seau ne glisse plus.",
    ],
    3: [
        "narrateur|Nina tient la chaîne, puis le doudou.",
        "narrateur|Elle le presse, oreille un peu froide.",
        "narrateur|Le seau reste au pied de bois.",
        "enfant-f|Je le reprends, il est à moi.",
        "maman|Merci, Nina, il est avec toi.",
        "papa|Tu le portes, contre toi ?",
        "enfant-f|Oui, contre moi.",
        "narrateur|Un brin de corde reste au doudou.",
        "narrateur|La perle de verre veille, au seau.",
        "enfant-f|Il ne tombe plus.",
    ],
}

T2_CHOICE = {
    1: [
        "narrateur|Près du bac, un jeu l'appelle.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le seau rouge reste avec toi.",
    ],
    2: [
        "narrateur|Près du toboggan, un jeu l'appelle.",
        "maman|Le ballon, le seau, ou le doudou ?",
        "papa|Le seau rouge reste avec toi.",
    ],
    3: [
        "narrateur|Près des cordes, un jeu l'appelle.",
        "papa|Le ballon, le seau, ou le doudou ?",
        "maman|Le seau rouge reste avec toi.",
    ],
}


def t2_lines(a: int, b: int) -> list[str]:
    table = {
        (1, 1): [
            "narrateur|Nina pose le seau au bord du bac.",
            "narrateur|Elle prend le ballon, lisse, un peu froid.",
            "copain|Moi, je le jette dans la flaque !",
            "enfant-f|Non, les ronds sont à moi.",
            "narrateur|Le ballon file, rouge, vers l'eau.",
            "narrateur|Elle court, le seau reste derrière.",
            "narrateur|Au retour, un rond rouge attend, flou.",
            "enfant-f|Mon seau !",
            "narrateur|Elle saisit le ballon, mouillé.",
            "narrateur|Le bac est vide, sans seau.",
            "enfant-f|Ce n'était pas lui.",
            "narrateur|Le sourire de Nina disparaît.",
            "papa|Regarde la perle, pas le rouge.",
            "narrateur|La perle de verre brille, dans l'herbe.",
            "maman|Personne ne dit où.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Elle écoute le bac, puis la flaque.",
        ],
        (1, 2): [
            "narrateur|Nina veut les ronds, avec le seau.",
            "narrateur|Elle creuse, l'anse froide dans la paume.",
            "copain|C'est mon château, pas tes ronds !",
            "enfant-f|Le seau est à moi.",
            "narrateur|Ils tirent l'anse, trop vite, trop fort.",
            "narrateur|Le seau bascule, plein de sable mouillé.",
            "narrateur|Une pelle rouge brille, dans le tas.",
            "enfant-f|Le voilà, mon seau !",
            "narrateur|Elle saisit la pelle, pas l'anse.",
            "narrateur|Le vrai seau s'enfonce, plus loin.",
            "enfant-f|La pelle a menti.",
            "papa|La perle, vois, pas le rouge.",
            "narrateur|La perle de verre sort du sable.",
            "maman|Personne ne donne la réponse.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Elle écoute le bac, puis la corde.",
        ],
        (1, 3): [
            "narrateur|Nina pose le doudou dans le seau.",
            "narrateur|L'oreille beige frotte l'anse en corde.",
            "copain|Il s'assoit sur ma montagne !",
            "enfant-f|Il voyage, avec mes ronds.",
            "narrateur|Nino tire le doudou, trop vite.",
            "narrateur|Le seau bascule, et s'enfonce.",
            "narrateur|Un dos beige cache l'anse, flou.",
            "enfant-f|Mon seau est dessous !",
            "narrateur|Elle saisit le doudou, trop occupée.",
            "narrateur|Sous le doudou, le sable est nu.",
            "enfant-f|Il s'est caché, le rusé.",
            "maman|La perle, vois, pas le doudou.",
            "narrateur|La perle de verre fuit sous une planche.",
            "papa|L'oreille a menti, la perle dit vrai.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Elle écoute le bac, puis la perle.",
        ],
        (2, 1): [
            "narrateur|Nina pose le seau sur une marche.",
            "narrateur|Elle prend le ballon, près du métal.",
            "copain|Il glisse dans la flaque, avec moi !",
            "enfant-f|Non, les ronds restent au seau.",
            "narrateur|Le ballon dévale, vif, trop loin.",
            "narrateur|Elle court au bas, sans le seau.",
            "narrateur|En haut, un rond rouge tient la rampe.",
            "enfant-f|Il m'attend, là-haut !",
            "narrateur|Elle gravit, et le rond se casse.",
            "narrateur|Le métal est nu, tiède, vide.",
            "enfant-f|Ce n'était que l'eau.",
            "papa|La perle, vois, sur le métal.",
            "narrateur|La perle de verre descend, marche par marche.",
            "maman|Personne ne dit où courir.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Elle écoute le métal, puis la flaque.",
        ],
        (2, 2): [
            "narrateur|Nina emplit le seau, au pied du métal.",
            "enfant-f|Je verse en haut, comme la pluie !",
            "copain|Je m'assois, c'est mon tour !",
            "narrateur|Nino s'assoit, trop vite, trop lourd.",
            "narrateur|L'eau du seau mouille la rampe, vive.",
            "narrateur|Le seau file, puis se cache dans l'herbe.",
            "narrateur|Une feuille rouge reste, plate, sur le métal.",
            "enfant-f|Il est collé, je le vois !",
            "narrateur|C'est la feuille, pas le seau.",
            "enfant-f|Il a disparu, mouillé.",
            "maman|La perle, vois, le long du métal.",
            "narrateur|La perle de verre fuit vers le jardin.",
            "papa|La feuille a menti, la perle dit vrai.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Elle écoute le toboggan, puis l'herbe.",
        ],
        (2, 3): [
            "narrateur|Nina pose le doudou contre le seau.",
            "narrateur|Sur la marche, les deux dos se touchent.",
            "copain|On glisse, tous les deux !",
            "enfant-f|Vous glissez avec moi, les deux.",
            "narrateur|Elle monte, le doudou sous le bras.",
            "narrateur|Au bas, un dos rouge attend, flou.",
            "enfant-f|Mon seau m'attend !",
            "narrateur|Elle saisit l'air, et le doudou.",
            "narrateur|Le seau n'est plus sur la marche.",
            "enfant-f|L'ombre a pris sa place.",
            "papa|La perle, vois, pas le doudou.",
            "narrateur|La perle de verre court sous le métal.",
            "maman|Personne ne donne la réponse.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Elle écoute la rampe, puis l'herbe.",
            "narrateur|Le doudou a une feuille, collée.",
        ],
        (3, 1): [
            "narrateur|Nina pose le seau sous le siège.",
            "narrateur|Elle prend le ballon, près des cordes.",
            "copain|Je me balance, c'est à moi !",
            "enfant-f|Le seau attrape les ronds, en bas.",
            "narrateur|Le ballon file, et le siège part.",
            "narrateur|Elle court, le seau reste derrière.",
            "narrateur|Au retour, un dos rouge balance, vide.",
            "enfant-f|Il se balance, je le vois !",
            "narrateur|Elle saisit l'ombre, sur le bois.",
            "narrateur|Le siège est nu, un peu tiède.",
            "enfant-f|Ce n'était que l'ombre.",
            "maman|La perle, vois, sur la corde.",
            "narrateur|La perle de verre tremble, puis fuit.",
            "papa|L'ombre a menti, la perle dit vrai.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Elle écoute la chaîne, puis la flaque.",
        ],
        (3, 2): [
            "narrateur|Nina emplit le seau, près des cordes.",
            "enfant-f|Je fais un poids, pour le siège !",
            "copain|Pousse-moi, plus fort !",
            "narrateur|Le seau pèse, et le siège part.",
            "narrateur|L'anse s'accroche, puis se libère.",
            "narrateur|Elle regarde Nino, trop occupée.",
            "narrateur|Un siège rouge reste, au vent.",
            "enfant-f|Il est là, contre le bois !",
            "narrateur|C'est le siège, pas le seau.",
            "enfant-f|Le seau a disparu.",
            "papa|La perle, vois, autour de la corde.",
            "narrateur|La perle de verre fuit vers le jardin.",
            "maman|La corde a menti, la perle dit vrai.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Elle écoute le bois, puis l'herbe.",
        ],
        (3, 3): [
            "narrateur|Nina pose le doudou sur le siège.",
            "narrateur|Le seau attend, au pied de bois.",
            "copain|Il se balance avec moi !",
            "enfant-f|Vous vous balancez, tous les deux.",
            "narrateur|Elle pousse, le doudou sous le bras.",
            "narrateur|Au retour, un dos rouge attend, flou.",
            "enfant-f|Mon seau se balance !",
            "narrateur|Elle saisit le doudou, trop vite.",
            "narrateur|Le siège est nu, sans seau.",
            "enfant-f|L'ombre a pris sa place.",
            "maman|La perle, vois, pas le doudou.",
            "narrateur|La perle de verre court dans l'herbe.",
            "papa|Le siège a menti, la perle dit vrai.",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Elle écoute la chaîne, puis la perle.",
            "narrateur|Le doudou sent l'herbe, un peu.",
        ],
    }
    return table[(a, b)]


T3_CHOICE = {
    1: [
        "narrateur|La perle mène vers trois coins.",
        "papa|Le banc, le portail, ou la haie ?",
        "maman|On suit la perle, pas le ballon.",
    ],
    2: [
        "narrateur|La perle mène vers trois coins.",
        "maman|Le banc, le portail, ou la haie ?",
        "papa|On suit la perle, pas le rouge.",
    ],
    3: [
        "narrateur|La perle mène vers trois coins.",
        "papa|Le banc, le portail, ou la haie ?",
        "maman|On suit la perle, pas le doudou.",
    ],
}


def t3_lines(a: int, b: int, c: int) -> list[str]:
    arrive = {
        1: [
            "narrateur|La perle court vers le banc de pierre.",
            "narrateur|La mousse verte brille, un peu froide.",
            "enfant-f|L'anse est dessous, je la vois !",
        ],
        2: [
            "narrateur|La perle court vers le portail.",
            "narrateur|Le loquet est froid, un peu rêche.",
            "enfant-f|L'anse est accrochée, je la vois !",
        ],
        3: [
            "narrateur|La perle court vers la haie.",
            "narrateur|Les feuilles gouttent, une à une.",
            "enfant-f|L'anse est prise, je la vois !",
        ],
    }[c]
    snag = {
        1: [
            "narrateur|Elle tire l'anse, trop vite.",
            "narrateur|La corde se coince entre deux pierres.",
            "enfant-f|Elle tient, entre les pierres !",
        ],
        2: [
            "narrateur|Elle tire l'anse, trop vite.",
            "narrateur|La corde s'enroule autour du loquet.",
            "enfant-f|Le loquet la mange !",
        ],
        3: [
            "narrateur|Elle tire l'anse, trop vite.",
            "narrateur|La corde s'accroche dans les branches.",
            "enfant-f|La haie la garde !",
        ],
    }[c]
    body = {
        1: [
            "narrateur|Le sourire de Nina disparaît.",
            "narrateur|L'envie et l'inquiétude se bousculent.",
            "narrateur|Papa s'accroupit, à sa hauteur.",
            "papa|Tu regardes, ou tu tires ?",
            "enfant-f|Je cherche, sans tirer.",
            "narrateur|Elle écoute la pierre, puis l'anse.",
            "narrateur|La perle de verre brille, minuscule.",
        ],
        2: [
            "narrateur|Ses épaules baissent, près du fer.",
            "narrateur|Dans sa poitrine, ça serre, trop fort.",
            "narrateur|Maman s'accroupit, à sa hauteur.",
            "maman|Tu forces, ou tu regardes ?",
            "enfant-f|J'attends, je regarde.",
            "narrateur|Elle écoute le fer, puis l'anse.",
            "narrateur|La perle de verre clignote, minuscule.",
        ],
        3: [
            "narrateur|Nina fixe la branche, sans bouger.",
            "narrateur|L'envie de tirer lui pique les doigts.",
            "narrateur|Papa s'accroupit, près de la haie.",
            "papa|Tu vois la perle, où ?",
            "enfant-f|Je cherche, sans tirer.",
            "narrateur|Elle écarte une feuille, lente.",
            "narrateur|La perle de verre brille, sous le brin.",
        ],
    }[c]
    again = {
        1: "narrateur|L'anse avance, puis s'arrête.",
        2: "narrateur|La corde glisse, puis se bloque.",
        3: "narrateur|Un brin cède, puis refuse.",
    }[c]
    helper = {
        1: {
            1: "narrateur|Elle cale le ballon sous la pierre.",
            2: "narrateur|Elle glisse l'anse sous la pierre.",
            3: "narrateur|Elle glisse le doudou sous la pierre.",
        },
        2: {
            1: "narrateur|Elle cale le ballon contre le loquet.",
            2: "narrateur|Elle glisse l'anse sous le loquet.",
            3: "narrateur|Elle glisse le doudou sous le loquet.",
        },
        3: {
            1: "narrateur|Elle cale le ballon sous la branche.",
            2: "narrateur|Elle glisse l'anse sous la branche.",
            3: "narrateur|Elle glisse le doudou sous la branche.",
        },
    }[c][b]
    gesture = {
        1: "enfant-f|Je soulève la pierre, sans tirer.",
        2: "enfant-f|Je soulève le loquet, sans tirer.",
        3: "enfant-f|J'écarte la branche, sans tirer.",
    }[c]
    free = {
        1: "narrateur|L'anse se libère, lente, pleine.",
        2: "narrateur|L'anse se libère, lente, froide.",
        3: "narrateur|L'anse se libère, lente, rêche.",
    }[c]
    traces = {
        (1, 1): "narrateur|Un grain de sable reste à la perle.",
        (1, 2): "narrateur|L'anse du seau a laissé du sable.",
        (1, 3): "narrateur|L'oreille du doudou a du sable.",
        (2, 1): "narrateur|Une feuille du toboggan reste au seau.",
        (2, 2): "narrateur|Une goutte du seau sèche à la perle.",
        (2, 3): "narrateur|Une feuille reste sur le doudou.",
        (3, 1): "narrateur|Un brin de corde reste à la perle.",
        (3, 2): "narrateur|L'anse a senti la chaîne, froide.",
        (3, 3): "narrateur|Le doudou a l'odeur de l'herbe.",
    }[(a, b)]
    almost = {
        (1, 1, 1): "narrateur|Un grain cachait la perle, presque.",
        (1, 1, 2): "narrateur|Le loquet serrait trop, une seconde.",
        (1, 1, 3): "narrateur|La feuille recouvrait l'anse, presque.",
        (1, 2, 1): "narrateur|Le sable buvait l'anse, presque.",
        (1, 2, 2): "narrateur|L'anse tirait trop, une seconde.",
        (1, 2, 3): "narrateur|La branche gardait la corde, presque.",
        (1, 3, 1): "narrateur|Le doudou cachait le rouge, presque.",
        (1, 3, 2): "narrateur|Le fer mordait l'anse, une seconde.",
        (1, 3, 3): "narrateur|Le brin se refermait, presque.",
        (2, 1, 1): "narrateur|Une feuille couvrait la perle, presque.",
        (2, 1, 2): "narrateur|Le métal glissait trop, une seconde.",
        (2, 1, 3): "narrateur|Le bord pliait la corde, presque.",
        (2, 2, 1): "narrateur|L'eau mentait, une seconde de trop.",
        (2, 2, 2): "narrateur|Le seau versait trop, une seconde.",
        (2, 2, 3): "narrateur|Une goutte cachait la perle, presque.",
        (2, 3, 1): "narrateur|L'oreille prenait la place, presque.",
        (2, 3, 2): "narrateur|Le doudou trompait l'œil, une seconde.",
        (2, 3, 3): "narrateur|La feuille collait trop, une seconde.",
        (3, 1, 1): "narrateur|La corde tenait l'anse, presque.",
        (3, 1, 2): "narrateur|Un tic couvrait la perle, presque.",
        (3, 1, 3): "narrateur|L'herbe cachait l'anse, presque.",
        (3, 2, 1): "narrateur|Le seau pesait trop, une seconde.",
        (3, 2, 2): "narrateur|La chaîne mentait, une seconde de trop.",
        (3, 2, 3): "narrateur|Le pied nu manquait le brin, presque.",
        (3, 3, 1): "narrateur|Le siège mélangeait les dos, presque.",
        (3, 3, 2): "narrateur|Un dos flou prenait la place, presque.",
        (3, 3, 3): "narrateur|L'odeur égarait la main, presque.",
    }[(a, b, c)]
    obj = OBJ[b]["name"]
    adult = {
        1: "maman|Tu l'as, sans forcer.",
        2: "papa|Il est à toi, maintenant.",
        3: "maman|Tu l'as repris, Nina.",
    }[c]
    return (
        arrive
        + snag
        + body
        + [again, helper, gesture, free, adult]
        + [
            f"narrateur|Voici {obj}, près d'elle.",
            traces,
            almost,
        ]
    )


def ending_lines(a: int, b: int, c: int) -> list[str]:
    obj = OBJ[b]["name"]
    lieu = LIEU[c]["name"]
    firsts = {
        (1, 1, 1): "Le lampadaire penche moins, sur le chemin.",
        (1, 1, 2): "La serviette de papa sent le fer mouillé.",
        (1, 1, 3): "Nino secoue une botte, près du seuil.",
        (1, 2, 1): "Un grain roule sur une dalle.",
        (1, 2, 2): "Le seau pose son ombre au bois.",
        (1, 2, 3): "La fenêtre a un peu de buée.",
        (1, 3, 1): "L'oreille du doudou dépasse du seuil.",
        (1, 3, 2): "Un fil du doudou pend près des clés.",
        (1, 3, 3): "Le doudou sent le sable, au bois.",
        (2, 1, 1): "Une feuille sèche sur le banc, loin.",
        (2, 1, 2): "Le métal du toboggan se tait, loin.",
        (2, 1, 3): "Un pas sur la dalle, puis plus.",
        (2, 2, 1): "Le seau penche, sous la fenêtre.",
        (2, 2, 2): "Le criiic du portail s'arrête.",
        (2, 2, 3): "La rampe du toboggan reste loin.",
        (2, 3, 1): "L'oreille molle dépasse du banc.",
        (2, 3, 2): "Le doudou a vu le métal, depuis le bois.",
        (2, 3, 3): "Un rayon a bougé, sur la pierre.",
        (3, 1, 1): "Le ballon s'endort près de la porte.",
        (3, 1, 2): "La chaîne ne fait plus tic.",
        (3, 1, 3): "Le lampadaire se tait, goutte après goutte.",
        (3, 2, 1): "Le seau pose son ombre sur la dalle.",
        (3, 2, 2): "La serviette attend, près des chaussures.",
        (3, 2, 3): "Les clés de papa restent dans la coupelle.",
        (3, 3, 1): "Près du seuil, le doudou sent l'herbe.",
        (3, 3, 2): "Une goutte rentre dans le seau, unique.",
        (3, 3, 3): "Le seuil retrouve son froid, unique.",
    }
    lasts = {
        (1, 1, 1): "Un grain de sable dort sur la perle.",
        (1, 1, 2): "Le loquet garde un fil de corde, minuscule.",
        (1, 1, 3): "Un grain reste coincé dans la haie.",
        (1, 2, 1): "L'anse du seau sèche, sous le banc.",
        (1, 2, 2): "Une goutte du seau s'endort au loquet.",
        (1, 2, 3): "L'ombre du seau s'endort dans les feuilles.",
        (1, 3, 1): "Du sable reste dans l'oreille du doudou.",
        (1, 3, 2): "Près du loquet, un fil beige pend.",
        (1, 3, 3): "Sur la perle, un grain de sable brille.",
        (2, 1, 1): "Une feuille sèche, collée à la perle.",
        (2, 1, 2): "Loin du seau, le métal se tait.",
        (2, 1, 3): "Sur le bois du toboggan, un pas s'éteint.",
        (2, 2, 1): "Sous le banc, le seau penche, vide.",
        (2, 2, 2): "Le criiic du portail s'endort, loin.",
        (2, 2, 3): "Loin d'ici, la rampe du toboggan reste muette.",
        (2, 3, 1): "Près du banc, une oreille molle veille.",
        (2, 3, 2): "Dans l'oreille, un peu de métal froid.",
        (2, 3, 3): "Sur la pierre, le rayon a bougé.",
        (3, 1, 1): "Près de la chaîne, le ballon s'endort.",
        (3, 1, 2): "Loin de la perle, la chaîne se tait.",
        (3, 1, 3): "La balançoire garde un tic, unique.",
        (3, 2, 1): "Sur la pierre, l'ombre du seau dort.",
        (3, 2, 2): "Près du portail, la serviette attend.",
        (3, 2, 3): "Dans la haie, une goutte se tait.",
        (3, 3, 1): "Au chaud, le doudou sent l'herbe.",
        (3, 3, 2): "Dans le seau, une perle de verre se tait.",
        (3, 3, 3): "Au banc, la mousse ne brille plus.",
    }
    qs = {
        1: "papa|Quel moment tu gardes, sous le banc ?",
        2: "maman|Quel moment tu gardes, au loquet ?",
        3: "papa|Quel moment tu gardes, dans la haie ?",
    }[c]
    ans = {
        1: "enfant-f|Quand la perle a parlé, entre les pierres.",
        2: "enfant-f|Quand j'ai soulevé, sans tirer.",
        3: "enfant-f|Quand la branche a dit non, d'abord.",
    }[c]
    joue = {
        1: "Nina a joué au bac.",
        2: "Nina a joué au toboggan.",
        3: "Nina a joué aux cordes.",
    }[a]
    return [
        f"narrateur|{firsts[(a, b, c)]}",
        f"narrateur|{joue}",
        f"narrateur|Elle a choisi {obj}, pour le jeu.",
        f"narrateur|La perle l'a menée vers {lieu}.",
        "narrateur|Voilà le seau rouge, près du seuil.",
        "narrateur|Sur l'anse, la perle de verre brille.",
        "enfant-f|Il est rentré, avec sa trace.",
        qs,
        ans,
        "enfant-f|Je raconte le moment difficile, surtout.",
        f"narrateur|{lasts[(a, b, c)]}",
    ]


def ending_note(a: int, b: int, c: int) -> str:
    return (
        f"arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
        f"destinataire=enfant; sous_texte=trace_{LOC[a]['short']}_{OBJ[b]['short']}_{LIEU[c]['short']}; "
        f"tempo=posé; sourire=léger; respiration=ample"
    )


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str, extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put("CHK_T0000_P0000", OPENING, "opening", "lampadaire,flaque,seau")
    put(
        "CHK_T0001_P0000",
        T1_CHOICE,
        "choice",
        "",
        {"fields": {
            "option_1_label": "le bac à sable",
            "option_2_label": "le toboggan",
            "option_3_label": "les balançoires",
        }},
    )

    for a in (1, 2, 3):
        put(
            f"CHK_T0001_P000{a}",
            T1[a],
            "action",
            LOC[a]["sons"],
            {"emphasis": LOC[a]["short"]},
        )
        put(
            f"CHK_T0001_P000{a}_Q0001",
            T1_Q[a],
            "clue",
            "",
            {"emphasis": Q_FIELDS[a]["expected_answer"], "fields": Q_FIELDS[a]},
        )
        emp_c = {1: "seau", 2: "manteau", 3: "doudou"}[a]
        put(
            f"CHK_T0001_P000{a}_C0001",
            T1_C[a],
            "confirm",
            LOC[a]["sons"],
            {"emphasis": emp_c},
        )
        put(
            f"CHK_T0001_P000{a}_T0002_P0000",
            T2_CHOICE[a],
            "choice",
            "",
            {"fields": {
                "option_1_label": "le ballon",
                "option_2_label": "le seau",
                "option_3_label": "le doudou",
            }},
        )
        for b in (1, 2, 3):
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}",
                t2_lines(a, b),
                "obstacle",
                OBJ[b]["sons"],
                {"emphasis": OBJ[b]["short"]},
            )
            put(
                f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P0000",
                T3_CHOICE[b],
                "choice",
                "",
                {"fields": {
                    "option_1_label": "le banc",
                    "option_2_label": "le portail",
                    "option_3_label": "la haie",
                }},
            )
            for c in (1, 2, 3):
                base = f"CHK_T0001_P000{a}_T0002_P000{b}_T0003_P000{c}"
                put(
                    base,
                    t3_lines(a, b, c),
                    "resolution",
                    LIEU[c]["sons"],
                    {"emphasis": "perle de verre"},
                )
                put(
                    f"{base}_F0001",
                    ending_lines(a, b, c),
                    "ending",
                    "flaque,maison",
                    {"emphasis": "perle", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = sorted(set(out_chunks) - {c["chunk_id"] for c in src["chunks"]})
    if missing or extra:
        raise SystemExit(f"missing={missing[:12]} extra={extra[:12]}")

    ends = [out_chunks[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(ends) != 27 or len(set(ends)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(ends))}/{len(ends)}")

    lasts = []
    for c in src["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        last_n = [ln for ln in out_chunks[c["chunk_id"]]["script"].splitlines() if ln.startswith("narrateur|")]
        lasts.append(last_n[-1])
        low = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in low or "bravo" in low or "bon travail" in low:
            raise SystemExit(f"fin mécanique: {last_n[-1]}")
    if len(set(lasts)) != 27:
        raise SystemExit(f"dernières images {len(set(lasts))}/27")

    t3_only = [
        out_chunks[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage" and "T0003_P000" in c["chunk_id"] and "_F0001" not in c["chunk_id"]
        and not c["chunk_id"].endswith("T0003_P0000")
    ]
    if len(t3_only) != 27 or len(set(t3_only)) != 27:
        raise SystemExit(f"T3 distincts: {len(set(t3_only))}/{len(t3_only)}")

    t2_only = [
        out_chunks[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage" and "_T0002_P000" in c["chunk_id"] and "T0003" not in c["chunk_id"]
    ]
    if len(t2_only) != 9 or len(set(t2_only)) != 9:
        raise SystemExit(f"T2 distincts: {len(set(t2_only))}/{len(t2_only)}")

    merged = dict(src)
    merged["fil_rouge"] = (
        "Après la pluie, le lampadaire penche son ombre comme une cuillère "
        "dans la flaque du chemin. Sur l'anse en corde du seau rouge, une "
        "perle de verre fait un éclair blanc. Nina veut les ronds du "
        "lampadaire dans son seau avant que le soleil les boive. Nino veut "
        "sauter dans la même flaque, maintenant. Elle plonge trop vite : les "
        "ronds se cassent. Papa s'accroupit. Au bac, au toboggan ou aux "
        "balançoires, elle pose le seau pour jouer : première idée, patatras. "
        "Elle le reprend. Ballon, seau ou doudou : un faux rouge ment, la "
        "perle dit vrai. Elle refuse de foncer. Banc, portail ou haie, l'anse "
        "se coince, avance, s'arrête. Elle soulève sans tirer. La perle paie "
        "le début. Vingt-sept traces."
    )
    merged["title"] = TITLE
    merged["characters"] = "Nina, Nino, papa, maman"
    merged["setting"] = "parc après la pluie, lampadaire, flaque du chemin, banc de pierre"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    counts = [
        sum(words(out_chunks[i]["text"]) for i in path_ids(a, b, c))
        for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)
    ]
    if min(counts) < 550 or max(counts) > 700:
        raise SystemExit(f"chemin hors barre 550-700: min {min(counts)} max {max(counts)}")
    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in merged["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Réécriture éditoriale F-NAR-019, example4 v2. Graphe, `chunk_id`, types "
        "de blocs et destinations techniques inchangés.\n\n"
        "## Promesse narrative\n\n"
        "Le lampadaire penche son ombre comme une cuillère dans la flaque. "
        "Sur l'anse en corde du seau rouge, une perle de verre fait un éclair "
        "blanc. Nina veut les ronds du lampadaire dans son seau avant que le "
        "soleil les boive. Nino veut sauter dans la même flaque, maintenant. "
        "Elle plonge trop vite : les ronds se cassent, le sourire disparaît. "
        "Papa s'accroupit. Au bac, au toboggan ou aux balançoires, elle pose "
        "le seau pour jouer : première idée, patatras. Elle le reprend. "
        "Ballon, seau ou doudou : un faux rouge ment, la perle dit vrai. Elle "
        "refuse de foncer. Banc, portail ou haie, l'anse se coince, avance, "
        "s'arrête. Elle soulève sans tirer. La perle et le dernier rond paient "
        "le début. Le seau garde une trace.\n\n"
        "## Arc dramatique\n\n"
        "- Monde : parc après la pluie, lampadaire, flaque du chemin, banc de pierre.\n"
        "- Désir : attraper les ronds du lampadaire dans le seau rouge, maintenant.\n"
        "- Objet : seau rouge (perle de verre), plus ballon / seau / doudou.\n"
        "- Indice unique : la perle de verre, vue dès l'ouverture, payée au climax.\n"
        "- Urgence douce : le soleil boit les ronds.\n"
        "- Imprévu 1 : Nino saute, le seau plonge trop vite, les ronds se cassent.\n"
        "- Cue : la perle, pas la force. Un merci vécu.\n"
        "- Imprévu 2 (plus rusé) : un faux rouge ment ; la perle dit vrai.\n"
        "- Revers allongé : coincé, corps (envie et peur), refus de foncer, "
        "anse qui avance puis s'arrête, geste neuf.\n"
        "- Résolution : soulever sans tirer, au banc, au portail, à la haie.\n"
        "- Retour : dernier rond, perle, 27 traces distinctes.\n\n"
        "## Corrections éditoriales\n\n"
        "- Ouverture inventée (le lampadaire-cuillère), pas un gabarit v2.\n"
        "- Le premier choix n'enlève pas le seau : il vient au parc.\n"
        "- Deux enfants, deux désirs : Nina les ronds, Nino le saut.\n"
        "- Revers allongé : coincé, corps, refus, second arrêt, geste lent.\n"
        "- Neuf disparitions distinctes, vingt-sept résolutions, vingt-sept fins.\n"
        "- Leçon AUT.AFF.003 vécue (reprendre seau, manteau, doudou), jamais dite.\n"
        "- Pas de refrain example3, pas de merle/miel, pas de grand-père/maîtresse.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n"
        "- Troupe D16 : Nina, Nino, papa, maman.\n"
        "- Voix : notes + ssml + xai + piper par chunk, profils raw.js.\n\n"
        "## Direction vocale\n\n"
        "Impatience de Nina au départ, petit découragement quand l'objet "
        "résiste ou disparaît, fierté calme quand elle soulève sans tirer. "
        "L'adulte guide peu. `slow` réservé aux choix, à la question, au retour.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, 27 fins textuellement distinctes\n"
        f"- 27 T3 distincts, 9 T2 distincts\n"
        f"- {min(counts)} à {max(counts)} mots par chemin, moyenne {sum(counts)//27}\n"
        "- `text` et `script` synchronisés\n"
        "- `text_ssml` et `text_xai_tags` enrichis\n"
        "- `notes` présentes sur les 86 chunks\n"
        "- N1 ≤ 10 mots/phrase\n"
        "- check() OK. Pas d'apply. Pas d'audio. Pas de git.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {len(merged['chunks'])} chunks  chemins {min(counts)}-{max(counts)}")


if __name__ == "__main__":
    build()
