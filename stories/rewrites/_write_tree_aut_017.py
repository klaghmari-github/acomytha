#!/usr/bin/env python3
"""TREE-AUT-017 — Le citron dans le bol bleu (F-NAR-019, N2, AUT.AFF.003, TTS)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-AUT-017"
N2 = 15
TITLE = "Le citron dans le bol bleu"
TICS = re.compile(
    r"\b(tout doux|tout calme|tout lent|tout bas|encore|déjà|deja)\b",
    re.I,
)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        emphasis="citron",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_clic_nouveau_appelle_le_soleil; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_maniere; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        emphasis="seau",
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_ce_qui_reste; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        emphasis="seau",
        note="arc=confirmation; intention=relancer; emotion=élan_prudent; intensite=1; destinataire=enfant; sous_texte=seau_manteau_citron_viennent; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        emphasis=None,
        note="arc=action; intention=entraîner; emotion=impatience; intensite=2; destinataire=enfant; sous_texte=elle_veut_le_soleil_tout_de_suite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=la_seconde_ruse_cache_le_jaune; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitchSsml="medium", pitchTag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        emphasis="citron",
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; intensite=2; destinataire=enfant; sous_texte=le_sac_rassemble_et_la_feuille_guide; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitchSsml="-2st", pitchTag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        emphasis="bol bleu",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_bol_a_son_soleil_la_virgule_a_voyagé; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def explode(lines: list[str]) -> list[str]:
    out = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        parts = re.findall(r".+?[.?!]", ph)
        if not parts:
            raise SystemExit(f"sans phrase: {raw}")
        leftover = ph
        for p in parts:
            leftover = leftover.replace(p, "", 1)
        if leftover.strip():
            raise SystemExit(f"reste {leftover!r} dans {raw}")
        for p in parts:
            out.append(f"{role}|{p.strip()}")
    return out


def vet(lines: list[str]) -> list[str]:
    out = []
    starts: list[str] = []
    for raw in lines:
        role, ph = raw.split("|", 1)
        ph = ph.strip()
        n = words(ph)
        if n > N2:
            raise SystemExit(f"{n}>{N2}: {ph}")
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
    lines = vet(explode(lines))
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    if extra.get("note"):
        m["note"] = extra["note"]
    text, script = from_script(lines)
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
    nc = dict(src)
    nc["text"] = text
    nc["script"] = script
    nc["sons"] = sons if sons is not None else (src.get("sons") or "")
    if nc["sons"] is None:
        nc["sons"] = ""
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
    nc["emphasis_words"] = m.get("emphasis") or ""
    nc["pause_before_ms"] = extra.get("pause_before_ms", 0)
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
    for k, v in extra.get("fields", {}).items():
        nc[k] = v
    return nc


# Ouverture : deux bruits se répondent (toc / clic). Indice unique : virgule verte.
OPENING = [
    "narrateur|L'horloge du salon répond à un clic, plus petit.",
    "narrateur|Mila connaît ce campement de coussins.",
    "narrateur|Ce clic-là, non.",
    "narrateur|Ses yeux tombent sur le bol bleu.",
    "narrateur|Dedans, un citron lisse attend.",
    "narrateur|Une feuille verte, mince, reste collée dessus.",
    "narrateur|On dirait une virgule.",
    "papa|La limonade voudra ce citron, plus tard.",
    "enfant-f|D'abord, il vient au parc !",
    "enfant-f|Il sera mon soleil.",
    "maman|Tu le ramènes dans le bol, après ?",
    "enfant-f|Oui.",
    "narrateur|En ce moment, Mila attrape trop vite.",
    "narrateur|Le citron fuit sous sa paume.",
    "narrateur|Alors le bol bascule.",
    "enfant-f|Il est parti !",
    "narrateur|Le jaune disparaît sous le plaid.",
    "narrateur|Elle cherche dans le seau jaune, d'abord.",
    "narrateur|Le sourire de Mila disparaît.",
    "papa|Je m'accroupis.",
    "papa|On cherche ensemble ?",
    "narrateur|Dans sa poitrine, l'envie et l'inquiétude se bousculent.",
    "narrateur|Mila soulève le coin tricoté.",
    "narrateur|La feuille brille, minuscule.",
    "enfant-f|Je t'ai.",
    "maman|Le seau et le manteau, avec nous ?",
    "narrateur|Mila prend le seau jaune, puis le manteau rouge.",
    "narrateur|Le bol vide garde un rond de lumière.",
]

T1_CHOICE = [
    "narrateur|Derrière la grille, le parc ouvre trois coins.",
    "maman|Où portes-tu le citron, d'abord ?",
    "narrateur|Le bac à sable.",
    "narrateur|Le toboggan.",
    "narrateur|Ou les balançoires.",
]

T1 = {
    1: {
        "lab": "le bac à sable",
        "sons": "sable,seau",
        "emphasis": "citron",
        "passage": [
            "narrateur|Derrière la grille, le bac sent la terre froide.",
            "narrateur|Mila verse le seau d'un seul geste.",
            "enfant-f|Un château, tout de suite !",
            "narrateur|Alors le château s'affaisse.",
            "narrateur|Elle pose le citron au sommet, comme un soleil.",
            "narrateur|Le jaune roule, se perd dans les grains.",
            "enfant-f|Je ne le vois plus !",
            "papa|Je m'accroupis, Mila.",
            "papa|Tu entends quoi, près du bois ?",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle écoute le bac.",
            "narrateur|Une petite feuille brille entre deux grains.",
            "enfant-f|La virgule !",
            "narrateur|Elle le soulève.",
            "maman|Le manteau reste sur le banc, tu vois ?",
            "narrateur|Le seau jaune attend au bord du bois.",
        ],
        "question": [
            "narrateur|Le seau jaune reste au bord du bac.",
            "papa|Que prend Mila, pour l'emmener ?",
        ],
        "qfields": {
            "expected_answer": "seau",
            "accepted_examples": (
                "seau | le seau | seau jaune | le seau jaune | manteau | "
                "le manteau | affaires | ses affaires | le citron"
            ),
            "retry_prompt": "Près du bac, un objet jaune attend. Que prend-elle ?",
        },
        "confirm": [
            "narrateur|Mila se tourne vers le bord du bois.",
            "enfant-f|Le seau, je le prends.",
            "narrateur|L'anse est froide.",
            "narrateur|Un grain chante au fond.",
            "papa|Et le manteau rouge, sur le banc ?",
            "narrateur|Elle le plie, mal, contre son ventre.",
            "maman|Le citron, lui, reste dans ta main ?",
            "enfant-f|Oui.",
            "enfant-f|Il a du sable.",
            "papa|Merci.",
            "narrateur|La virgule verte a un grain collé.",
        ],
    },
    2: {
        "lab": "le toboggan",
        "sons": "toboggan,metal",
        "emphasis": "citron",
        "passage": [
            "narrateur|Le toboggan luit, tiède sous la paume.",
            "narrateur|Mila grimpe.",
            "narrateur|Les marches font toc.",
            "enfant-f|Toi aussi tu glisses, citron !",
            "narrateur|Elle le pose en haut, trop vite.",
            "narrateur|Le jaune file vers la grille du bas.",
            "enfant-f|Non !",
            "narrateur|La feuille verte accroche le métal, juste à temps.",
            "papa|Je t'attends en bas.",
            "papa|Tu le prends ?",
            "narrateur|Mila glisse.",
            "narrateur|Ses joues sont chaudes.",
            "narrateur|Elle ramasse le citron.",
            "narrateur|Le cœur tape.",
            "maman|Je m'accroupis.",
            "maman|Tu l'as vu comment, tout à coup ?",
            "enfant-f|Sa virgule a tenu.",
            "narrateur|Le seau est resté près des marches.",
            "narrateur|Le manteau rouge dort sur le banc.",
        ],
        "question": [
            "narrateur|Le manteau rouge dort sur le banc.",
            "maman|Que prend Mila, pour l'emmener ?",
        ],
        "qfields": {
            "expected_answer": "manteau",
            "accepted_examples": (
                "manteau | le manteau | manteau rouge | le manteau rouge | "
                "seau | le seau | affaires | ses affaires"
            ),
            "retry_prompt": "Sur le banc, un tissu rouge attend. Que prend-elle ?",
        },
        "confirm": [
            "narrateur|Mila s'arrête au bas du toboggan.",
            "enfant-f|Le manteau, je le prends.",
            "narrateur|Le tissu sent le soleil du banc.",
            "papa|Le seau, près des marches, vient aussi ?",
            "narrateur|Elle croche l'anse avec deux doigts.",
            "maman|Le citron a glissé.",
            "maman|Il est là ?",
            "enfant-f|Dans ma poche.",
            "enfant-f|Sa feuille dépasse.",
            "papa|Merci.",
            "narrateur|Une feuille de rampe colle à la manche.",
        ],
    },
    3: {
        "lab": "les balançoires",
        "sons": "balancoire,corde",
        "emphasis": "citron",
        "passage": [
            "narrateur|Les balançoires sentent la corde et le bois.",
            "narrateur|Mila s'assoit.",
            "narrateur|Le citron tient sur ses genoux.",
            "enfant-f|Plus haut, maman !",
            "maman|J'y vais.",
            "maman|Tu le tiens ?",
            "narrateur|La poussée est trop forte.",
            "narrateur|Le citron saute.",
            "narrateur|Il disparaît dans l'herbe.",
            "enfant-f|Il est tombé !",
            "narrateur|Elle pose les pieds.",
            "narrateur|L'herbe est partout, verte.",
            "papa|Je m'accroupis, à ta hauteur.",
            "papa|Tu cherches l'herbe, ou autre chose ?",
            "narrateur|Mila refuse de foncer.",
            "narrateur|Elle écoute l'herbe.",
            "narrateur|Une ombre en virgule.",
            "enfant-f|La feuille !",
            "narrateur|Mila le reprend, les lèvres pincées.",
            "narrateur|Le seau reste au pied de bois.",
            "maman|Le manteau, lui, attend sur le banc.",
        ],
        "question": [
            "narrateur|Le seau reste au pied de bois.",
            "papa|Que prend Mila, pour l'emmener ?",
        ],
        "qfields": {
            "expected_answer": "seau",
            "accepted_examples": (
                "seau | le seau | seau jaune | le seau jaune | manteau | "
                "le manteau | affaires | ses affaires"
            ),
            "retry_prompt": "Au pied de bois, un seau attend. Que prend-elle ?",
        },
        "confirm": [
            "narrateur|Mila pose un pied au sol, puis l'autre.",
            "enfant-f|Le seau, je le prends.",
            "maman|Le manteau du banc, avec nous ?",
            "narrateur|Elle l'enroule autour du seau, un peu de travers.",
            "papa|Le citron a voyagé.",
            "papa|Il est là ?",
            "enfant-f|Sur mes genoux.",
            "papa|Merci.",
            "narrateur|Un brin d'herbe s'est pris dans la virgule.",
        ],
    },
}

T2_CHOICE = {
    1: [
        "narrateur|Le sable colle aux doigts, et au citron.",
        "papa|Quel jeu garde le citron avec toi ?",
        "narrateur|Le ballon, le seau, ou le doudou.",
    ],
    2: [
        "narrateur|Le métal du toboggan reste tiède, derrière.",
        "maman|Quel jeu garde le citron avec toi ?",
        "narrateur|Le ballon, le seau, ou le doudou.",
    ],
    3: [
        "narrateur|La corde des balançoires se tait, un peu.",
        "papa|Quel jeu garde le citron avec toi ?",
        "narrateur|Le ballon, le seau, ou le doudou.",
    ],
}

T2 = {
    (1, 1): {
        "lab": "le ballon",
        "sons": "ballon,sable",
        "emphasis": "ballon",
        "passage": [
            "narrateur|Mila pose le citron contre le ballon rouge.",
            "enfant-f|Deux soleils.",
            "enfant-f|Un petit, un gros.",
            "narrateur|Un souffle pousse le ballon vers le chemin.",
            "narrateur|Le citron, rond comme lui, roule derrière.",
            "enfant-f|Reviens !",
            "narrateur|L'ombre rouge avale le jaune.",
            "narrateur|Mila cherche.",
            "narrateur|Ses mains tremblent un peu.",
            "papa|Je m'accroupis.",
            "papa|Tu fonces, ou tu regardes ?",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Personne ne montre la feuille.",
            "narrateur|Mila observe le ballon, écoute le sable.",
            "narrateur|La feuille verte dépasse du rouge.",
            "enfant-f|Toi dans cette main.",
            "enfant-f|Toi dans l'autre.",
            "maman|Le seau et le manteau restent près du bac.",
            "narrateur|Un grain de sable colle au cuir du ballon.",
        ],
    },
    (1, 2): {
        "lab": "le seau",
        "sons": "seau,sable",
        "emphasis": "seau",
        "passage": [
            "narrateur|Mila glisse le citron au fond du seau.",
            "enfant-f|Tu es à l'abri, soleil.",
            "narrateur|Elle verse du sable par-dessus, trop.",
            "narrateur|Le jaune disparaît.",
            "narrateur|Plus de clic.",
            "enfant-f|Oh.",
            "enfant-f|Je l'ai caché trop bien.",
            "narrateur|Elle secoue.",
            "narrateur|Rien.",
            "narrateur|Les épaules tombent.",
            "papa|Je m'accroupis, à ta hauteur.",
            "papa|Au salon, il faisait quel bruit ?",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Mila écoute le seau.",
            "narrateur|Un petit clic, sous le sable.",
            "enfant-f|La virgule !",
            "maman|Le manteau, lui, n'a pas bougé du banc.",
            "narrateur|Du sable fin brille dans le seau jaune.",
        ],
    },
    (1, 3): {
        "lab": "le doudou",
        "sons": "doudou,sable",
        "emphasis": "doudou",
        "passage": [
            "narrateur|Mila assied le citron dans les bras du doudou.",
            "enfant-f|Tu le gardes, gris.",
            "narrateur|Le doudou bascule.",
            "narrateur|L'oreille molle recouvre le jaune.",
            "narrateur|On ne voit plus que du gris, et du sable.",
            "enfant-f|Il a mangé mon soleil !",
            "narrateur|Elle fouille le sable.",
            "narrateur|Pas de clic.",
            "maman|Je m'accroupis.",
            "maman|Tu cherches le gris, ou autre chose ?",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Personne ne montre la feuille.",
            "narrateur|Mila observe l'oreille, écoute le doudou.",
            "narrateur|Une pointe verte sort de la fourrure.",
            "enfant-f|Pardon, doudou.",
            "enfant-f|Je te soulève.",
            "narrateur|Le citron est tiède, contre le ventre gris.",
            "papa|Le seau attend au bord, tout jaune.",
            "narrateur|L'oreille grise a un peu de sable.",
        ],
    },
    (2, 1): {
        "lab": "le ballon",
        "sons": "ballon,toboggan",
        "emphasis": "ballon",
        "passage": [
            "narrateur|Mila veut que le ballon glisse, après le citron.",
            "enfant-f|Vous descendez ensemble !",
            "narrateur|Le ballon rebondit.",
            "narrateur|Le citron file sous le toboggan.",
            "narrateur|Là-dessous, l'ombre est froide, étroite.",
            "enfant-f|Je ne le vois plus, papa.",
            "narrateur|Elle se penche.",
            "narrateur|Le métal lui touche le front.",
            "papa|Je m'accroupis, près de la rampe.",
            "papa|Tu fonces dessous, ou tu regardes ?",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Mila observe le métal, écoute le dessous.",
            "narrateur|La feuille verte pince une vis, au fond.",
            "enfant-f|Je te sors.",
            "maman|Le seau, près des marches, n'a pas glissé.",
            "narrateur|Le ballon est un peu froid, près de la rampe.",
        ],
    },
    (2, 2): {
        "lab": "le seau",
        "sons": "seau,toboggan",
        "emphasis": "seau",
        "passage": [
            "narrateur|Mila monte les marches, le seau à la main.",
            "enfant-f|Le citron voyage dans le seau.",
            "narrateur|À la troisième marche, l'anse penche.",
            "narrateur|Le citron bascule vers la rampe, presque.",
            "enfant-f|Oh non.",
            "narrateur|Elle s'assoit sur la marche, le seau serré.",
            "papa|Je m'accroupis, sur la marche d'en bas.",
            "papa|Deux mains, comme au bol ?",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Personne ne tient l'anse à sa place.",
            "narrateur|Mila observe le seau, écoute le plastique.",
            "narrateur|Un petit clic contre le plastique.",
            "enfant-f|Tu restes.",
            "enfant-f|On descend ensemble.",
            "maman|Le manteau n'a pas grimpé, lui.",
            "narrateur|Elle descend, marche après marche, le seau droit.",
        ],
    },
    (2, 3): {
        "lab": "le doudou",
        "sons": "doudou,toboggan",
        "emphasis": "doudou",
        "passage": [
            "narrateur|Mila glisse le citron dans la poche, le doudou contre elle.",
            "enfant-f|Toi tu regardes.",
            "enfant-f|Lui il voyage.",
            "narrateur|En bas, la poche est plate.",
            "narrateur|Vide.",
            "enfant-f|Il a disparu !",
            "narrateur|Le doudou a un foulard.",
            "narrateur|Un coin dépasse, jaune.",
            "papa|Je m'accroupis.",
            "papa|Tu entends le foulard, ou le clic ?",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Personne ne dénoue à sa place.",
            "narrateur|Mila observe le foulard, écoute le tissu.",
            "narrateur|La virgule verte est là.",
            "enfant-f|Tu t'es caché, vilain.",
            "maman|Le seau, près des marches, n'a rien volé.",
            "narrateur|Elle serre doudou et citron, cette fois à vue.",
            "papa|La rampe brille.",
            "narrateur|Le doudou a vu le toboggan, tout gris.",
        ],
    },
    (3, 1): {
        "lab": "le ballon",
        "sons": "ballon,balancoire",
        "emphasis": "ballon",
        "passage": [
            "narrateur|Mila tient le fil du ballon, et le citron.",
            "enfant-f|Le ballon vole.",
            "narrateur|Une rafale tire le fil.",
            "narrateur|Elle lâche le citron.",
            "narrateur|Le jaune tombe.",
            "narrateur|Le ballon roule dessus.",
            "enfant-f|Je l'ai perdu sous le rouge !",
            "narrateur|L'herbe cache tout.",
            "maman|Je m'accroupis, dans l'herbe.",
            "maman|Tu cherches le rouge, ou autre chose ?",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Mila observe le cuir, écoute l'herbe.",
            "narrateur|Sous le ballon, une pointe verte.",
            "enfant-f|Fil dans cette main.",
            "enfant-f|Citron dans l'autre.",
            "papa|Le seau, au pied de bois, n'a pas volé.",
            "narrateur|Elle sépare les deux ronds, enfin.",
            "narrateur|Un brin d'herbe colle au ballon.",
        ],
    },
    (3, 2): {
        "lab": "le seau",
        "sons": "seau,balancoire",
        "emphasis": "seau",
        "passage": [
            "narrateur|Mila pose le seau sous la balançoire.",
            "enfant-f|Si tu tombes, tu atterris là.",
            "narrateur|Le seau gêne ses pieds.",
            "narrateur|Ça cogne.",
            "narrateur|Le citron, sur les genoux, glisse vers le bord.",
            "enfant-f|Attends !",
            "narrateur|Elle arrête la balançoire avec les talons.",
            "papa|Je m'accroupis, près de la corde.",
            "papa|Le seau est un nid, s'il est trop loin ?",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Personne ne ramène le seau à sa place.",
            "narrateur|Mila observe ses tibias, écoute l'anse.",
            "narrateur|Elle ramène le seau contre ses tibias.",
            "narrateur|Le citron fait clic, au fond, bien tenu.",
            "enfant-f|Maintenant tu es mon nid.",
            "maman|Le manteau du banc n'a pas bougé.",
        ],
    },
    (3, 3): {
        "lab": "le doudou",
        "sons": "doudou,balancoire",
        "emphasis": "doudou",
        "passage": [
            "narrateur|Mila met le doudou sur l'autre balançoire.",
            "enfant-f|Je te passe le soleil !",
            "narrateur|Le citron vole.",
            "narrateur|Il tombe entre les deux sièges.",
            "narrateur|Plus de jaune.",
            "enfant-f|Je suis fâchée.",
            "papa|Je m'accroupis, entre les sièges.",
            "papa|On cherche, ou on se fâche ?",
            "enfant-f|Je ne fonce pas.",
            "narrateur|Personne ne donne la réponse.",
            "narrateur|Mila observe les pieds de bois, écoute le vent.",
            "narrateur|Entre les pieds de bois, une virgule verte.",
            "enfant-f|Toi avec moi.",
            "enfant-f|Le doudou à côté.",
            "maman|Le seau, au pied, n'a rien reçu.",
            "narrateur|Elle tient le citron contre sa joue, cette fois.",
            "papa|Le passage, on le fait avec les mains.",
        ],
    },
}

T3_CHOICE = {
    (1, 1): [
        "narrateur|Le ballon a du sable.",
        "narrateur|Le citron aussi.",
        "papa|Quel sac rassemble nos affaires ?",
        "narrateur|Le sac à étoiles, le sac à carreaux, ou le sac à ronds.",
    ],
    (1, 2): [
        "narrateur|Le seau est lourd de sable, et de citron.",
        "maman|Quel sac rassemble nos affaires ?",
        "narrateur|Le sac à étoiles, le sac à carreaux, ou le sac à ronds.",
    ],
    (1, 3): [
        "narrateur|Le doudou a du sable à l'oreille.",
        "papa|Quel sac rassemble nos affaires ?",
        "narrateur|Le sac à étoiles, le sac à carreaux, ou le sac à ronds.",
    ],
    (2, 1): [
        "narrateur|Le ballon est froid, près de la rampe.",
        "maman|Quel sac rassemble nos affaires ?",
        "narrateur|Le sac à étoiles, le sac à carreaux, ou le sac à ronds.",
    ],
    (2, 2): [
        "narrateur|Le seau a sonné contre les marches.",
        "papa|Quel sac rassemble nos affaires ?",
        "narrateur|Le sac à étoiles, le sac à carreaux, ou le sac à ronds.",
    ],
    (2, 3): [
        "narrateur|Le doudou sent le métal du toboggan.",
        "maman|Quel sac rassemble nos affaires ?",
        "narrateur|Le sac à étoiles, le sac à carreaux, ou le sac à ronds.",
    ],
    (3, 1): [
        "narrateur|Le ballon a un brin d'herbe au cuir.",
        "papa|Quel sac rassemble nos affaires ?",
        "narrateur|Le sac à étoiles, le sac à carreaux, ou le sac à ronds.",
    ],
    (3, 2): [
        "narrateur|Le seau a servi de nid, un moment.",
        "maman|Quel sac rassemble nos affaires ?",
        "narrateur|Le sac à étoiles, le sac à carreaux, ou le sac à ronds.",
    ],
    (3, 3): [
        "narrateur|Le doudou a senti le vent des cordes.",
        "papa|Quel sac rassemble nos affaires ?",
        "narrateur|Le sac à étoiles, le sac à carreaux, ou le sac à ronds.",
    ],
}

T3 = {}
ENDINGS = {}

T3[(1, 1, 1)] = [
    "narrateur|Le soleil du château n'a plus de sommet.",
    "enfant-f|J'ai le citron.",
    "enfant-f|On rentre.",
    "narrateur|Le ballon reste contre le bac, oublié.",
    "papa|Attends.",
    "papa|Le jaune du parc n'est pas le nôtre.",
    "narrateur|Le sac à étoiles pend à la barrière, trop haut.",
    "enfant-f|Je n'arrive pas au zip.",
    "maman|Monte sur le bord.",
    "narrateur|Mila ouvre.",
    "narrateur|Une étoile de tissu brille.",
    "narrateur|Elle glisse le manteau, le seau, le ballon.",
    "enfant-f|Le citron dessus, pour voir sa feuille.",
    "papa|Merci.",
    "papa|Tu as trouvé sa virgule dans le sable.",
    "narrateur|Un grain rouge colle au sac bleu.",
    "enfant-f|Le bol nous attend.",
]
ENDINGS[(1, 1, 1)] = [
    "narrateur|Le campement du salon a gardé son rond de lumière.",
    "narrateur|Mila pose le citron dans le bol bleu.",
    "enfant-f|Du sable, sur ta feuille.",
    "maman|La limonade aura un goût de château.",
    "papa|Le plaid, Mila ?",
    "narrateur|Elle le remet dans le creux du canapé.",
    "narrateur|Le sac à étoiles s'affaisse près du fauteuil.",
    "enfant-f|L'étoile a un grain.",
    "narrateur|La feuille verte pose un grain au bord du bol.",
]

T3[(1, 1, 2)] = [
    "narrateur|Le sable refroidit sous les paumes.",
    "enfant-f|Le ballon vient.",
    "enfant-f|Le citron aussi.",
    "narrateur|Elle part.",
    "narrateur|Le manteau reste plié sur le banc.",
    "maman|Le banc n'est pas la maison, ma grande.",
    "narrateur|Le sac à carreaux est ouvert sur le banc, large.",
    "papa|Les carreaux aident à plier, un par un.",
    "narrateur|Mila plie le manteau sur un carré rouge.",
    "narrateur|Le seau entre.",
    "narrateur|Le ballon entre.",
    "enfant-f|Le citron, tout seul, sur le dernier carré.",
    "maman|Merci.",
    "maman|Le sac à carreaux tient tout.",
    "narrateur|Le ballon laisse une trace ronde au tissu.",
    "papa|Le bol, au salon, a son rond à lui.",
    "enfant-f|On y va.",
]
ENDINGS[(1, 1, 2)] = [
    "narrateur|Le bol bleu a attendu, vide, sur la table.",
    "narrateur|Mila y pose le citron, tout rond.",
    "enfant-f|Ta feuille a un carré d'ombre, maman.",
    "papa|C'est le sac.",
    "papa|Il a marqué le zeste.",
    "narrateur|Elle ramasse le plaid, le pose dans le creux.",
    "maman|La limonade peut commencer ?",
    "enfant-f|Oui.",
    "enfant-f|Un peu de sable, c'est rien.",
    "narrateur|Le sac à carreaux s'assoit contre le fauteuil.",
    "narrateur|Un carré d'ombre reste sur le zeste.",
]

T3[(1, 1, 3)] = [
    "narrateur|Un nuage passe sur le bac.",
    "narrateur|Le château pâlit.",
    "enfant-f|Vite, le citron rentre.",
    "narrateur|Elle serre le ballon.",
    "narrateur|Le seau reste au bord.",
    "papa|Le seau a chanté, tout à l'heure.",
    "papa|Il vient.",
    "narrateur|Le sac à ronds attend près de la grille.",
    "narrateur|Un gros bouton de bois ferme la bouche.",
    "enfant-f|Ronds, comme le citron, comme le ballon.",
    "maman|Tu comptes, puis tu glisses tout dedans.",
    "narrateur|Manteau.",
    "narrateur|Seau.",
    "narrateur|Ballon.",
    "narrateur|Citron.",
    "papa|Merci.",
    "papa|Tu as compté jusqu'au jaune.",
    "narrateur|Un brin d'herbe reste au sac vert.",
    "enfant-f|La virgule a voyagé.",
]
ENDINGS[(1, 1, 3)] = [
    "narrateur|L'horloge du salon fait toc, puis toc.",
    "narrateur|Mila glisse le citron dans le bol bleu.",
    "enfant-f|Quatre choses sont rentrées.",
    "papa|Le bouton de bois a bien tenu.",
    "narrateur|Le plaid retrouve le canapé, un peu de travers.",
    "maman|On presse le zeste ?",
    "enfant-f|Après.",
    "enfant-f|Il se repose.",
    "narrateur|Le sac à ronds s'adosse à la porte.",
    "narrateur|Un grain jaune reste dans la coupelle des clés.",
]

T3[(1, 2, 1)] = [
    "narrateur|Le seau est lourd.",
    "narrateur|Le citron y fait clic.",
    "enfant-f|On rentre.",
    "enfant-f|J'ai tout.",
    "narrateur|Le manteau, sur le banc, n'est pas dans le seau.",
    "maman|Le clic du seau n'emporte pas le rouge.",
    "narrateur|Le sac à étoiles pend.",
    "narrateur|Mila tire le zip, crcr.",
    "papa|L'anse d'abord, puis le tissu.",
    "narrateur|Elle met le seau, le manteau, le citron au-dessus.",
    "enfant-f|Sa feuille, je la vois dans le zip.",
    "papa|Merci.",
    "papa|Le clic rentre avec nous.",
    "narrateur|Du sable fin brille dans le sac bleu.",
    "maman|Le bol, lui, n'a pas de sable.",
    "enfant-f|Le citron va le remplir.",
    "narrateur|Une étoile de tissu garde un grain.",
]
ENDINGS[(1, 2, 1)] = [
    "narrateur|Sous le portemanteau, Mila pose le seau.",
    "narrateur|Le citron rejoint le bol bleu, un clic.",
    "enfant-f|C'est le même clic qu'au parc.",
    "papa|Et le même qu'au salon, ce matin.",
    "maman|La limonade va chanter, elle aussi.",
    "narrateur|Le plaid est remis.",
    "narrateur|Le creux revient.",
    "enfant-f|La virgule a du sable, un peu.",
    "narrateur|Le sac à étoiles s'accroche à la poignée.",
    "narrateur|Le seau sèche sous le portemanteau, anse tournée.",
]

T3[(1, 2, 2)] = [
    "narrateur|Mila veut partir le seau contre la hanche.",
    "enfant-f|Le citron est dedans.",
    "enfant-f|C'est bon.",
    "papa|Le banc a ton manteau.",
    "papa|Le bol n'a rien, lui.",
    "narrateur|Le sac à carreaux est sur le banc, bouche ouverte.",
    "maman|Un carreau pour le seau.",
    "maman|Un carreau pour le rouge.",
    "narrateur|Mila pose l'anse sur un carré, le manteau sur l'autre.",
    "enfant-f|Le citron, je le sors.",
    "enfant-f|Il va sur le bleu du sac.",
    "narrateur|La virgule verte touche un carreau clair.",
    "maman|Merci.",
    "maman|Tu as sorti le soleil du sable.",
    "narrateur|L'anse jaune touche le sac rouge.",
    "papa|Au salon, le bol est bleu, pas rouge.",
    "enfant-f|Il va retrouver son bleu.",
    "narrateur|Un grain reste au fond du seau, oublié.",
]
ENDINGS[(1, 2, 2)] = [
    "narrateur|Le rond de lumière du bol est toujours là.",
    "narrateur|Mila y pose le citron.",
    "narrateur|Le rond s'emplit.",
    "enfant-f|Tu étais au parc.",
    "enfant-f|Te voilà.",
    "papa|Un grain de sable a voyagé, au fond du seau.",
    "maman|On le verse dehors, plus tard.",
    "narrateur|Elle remet le plaid.",
    "narrateur|Ça sent le zeste.",
    "enfant-f|La limonade, après le repos.",
    "narrateur|Le sac à carreaux s'affaisse, bouche fermée.",
    "narrateur|Le rond de lumière du bol entoure le citron rentré.",
]

T3[(1, 2, 3)] = [
    "narrateur|Un oiseau picore trop près du seau.",
    "enfant-f|Ce n'est pas à toi !",
    "enfant-f|C'est mon soleil.",
    "narrateur|Elle couvre le seau de sa main.",
    "narrateur|L'oiseau s'en va.",
    "papa|Le sac à ronds, près de la grille, est plus sûr.",
    "narrateur|Le bouton de bois résiste.",
    "narrateur|Mila le tourne.",
    "maman|Seau, manteau, citron.",
    "maman|Trois ronds.",
    "narrateur|Elle glisse tout.",
    "narrateur|Un coquillage minuscule roule au fond.",
    "enfant-f|Il était dans le sable.",
    "papa|Merci.",
    "papa|Tu as gardé le jaune pour le bol.",
    "narrateur|Un coquillage minuscule roule au sac vert.",
    "maman|Le bol n'a pas de coquillage.",
    "enfant-f|Je le lui rends.",
    "narrateur|La virgule verte a un grain, et une poussière de coquille.",
]
ENDINGS[(1, 2, 3)] = [
    "narrateur|La poussière du salon ne danse plus.",
    "narrateur|Mila pose le citron.",
    "narrateur|Le bol bleu fait clic.",
    "enfant-f|Le coquillage reste dans le sac.",
    "maman|C'est un souvenir du bac, pas de la limonade.",
    "papa|Le zeste, lui, rentre dans le verre.",
    "narrateur|Le plaid est chaud, remis dans le creux.",
    "enfant-f|La feuille est un peu rêche, maintenant.",
    "narrateur|Le sac à ronds garde le coquillage, près de la porte.",
    "narrateur|L'horloge fait toc, et le zeste répond, minuscule.",
]

T3[(1, 3, 1)] = [
    "narrateur|Le doudou a l'oreille pleine de sable.",
    "enfant-f|On rentre, toi et le soleil.",
    "narrateur|Le seau reste au bord.",
    "narrateur|Le manteau aussi.",
    "papa|Le gris n'emporte pas le jaune du seau.",
    "narrateur|Le sac à étoiles pend.",
    "narrateur|Mila saute un peu.",
    "maman|Zip.",
    "maman|Doudou d'abord, tête vers le haut.",
    "narrateur|L'oreille dépasse.",
    "narrateur|Puis le manteau.",
    "narrateur|Puis le seau.",
    "enfant-f|Le citron contre l'oreille, pour qu'il n'ait pas froid.",
    "papa|Merci.",
    "papa|Tu as sorti le sable de l'oreille, aussi.",
    "maman|Le bol va voir un soleil un peu tiède.",
    "enfant-f|Il a dormi contre le doudou.",
    "narrateur|Un fil gris pend, pris dans le zip.",
]
ENDINGS[(1, 3, 1)] = [
    "narrateur|Le campement de coussins a un creux pour le doudou.",
    "narrateur|Mila pose le citron dans le bol bleu.",
    "enfant-f|L'oreille a gardé du sable, un peu.",
    "maman|On la secoue, dehors, demain.",
    "papa|La limonade n'a pas besoin de sable.",
    "narrateur|Le plaid couvre les genoux, puis le creux.",
    "enfant-f|La virgule est chaude, côté doudou.",
    "narrateur|Le sac à étoiles s'endort contre un coussin.",
    "narrateur|L'oreille du doudou dépasse du campement de coussins.",
]

T3[(1, 3, 2)] = [
    "narrateur|Mila serre le doudou.",
    "narrateur|Le citron est contre le gris.",
    "enfant-f|On a fini le château.",
    "maman|Le banc a le manteau.",
    "maman|Le bord a le seau.",
    "narrateur|Le sac à carreaux attend, plié en deux sur le banc.",
    "papa|Un carreau gris, un carreau rouge, un carreau jaune.",
    "narrateur|Doudou.",
    "narrateur|Manteau.",
    "narrateur|Seau.",
    "narrateur|Puis le citron au milieu.",
    "enfant-f|Il est au centre, comme au château.",
    "maman|Merci.",
    "maman|Tu as remis le soleil au milieu.",
    "narrateur|Le doudou sent le sable, contre le sac rouge.",
    "papa|Au salon, le bol est le milieu, lui.",
    "enfant-f|J'y pense.",
    "narrateur|Un fil de laine du doudou reste au carreau.",
]
ENDINGS[(1, 3, 2)] = [
    "narrateur|Le bol bleu est seul, au milieu de la table.",
    "narrateur|Mila y pose le citron.",
    "narrateur|Le milieu est plein.",
    "enfant-f|Comme au château.",
    "enfant-f|Mais sans sable.",
    "papa|Un fil gris est resté au sac.",
    "maman|Le doudou peut le retrouver.",
    "narrateur|Elle remet le plaid.",
    "narrateur|Le campement se tait.",
    "enfant-f|La limonade, quand il sera froid.",
    "narrateur|Le sac à carreaux s'adosse au fauteuil.",
    "narrateur|Le citron luit, froid, la virgule verte un peu pliée.",
]

T3[(1, 3, 3)] = [
    "narrateur|Un vent lève un peu de sable.",
    "narrateur|Le doudou cligne.",
    "enfant-f|On part, avant qu'il ait trop de grains.",
    "papa|La grille.",
    "papa|Le sac à ronds a un bouton, pas de sable.",
    "narrateur|Mila tourne le bouton.",
    "narrateur|Ça résiste, puis ça cède.",
    "maman|Rond le doudou, rond le seau, rond le citron.",
    "narrateur|Elle glisse le manteau en dernier, comme un toit.",
    "enfant-f|Le toit du château, pour rentrer.",
    "papa|Merci.",
    "papa|Tu as fermé le bouton, toute seule.",
    "narrateur|Un fil gris pend du sac vert.",
    "maman|Le bol n'a pas de toit.",
    "maman|Il a un rond de lumière.",
    "enfant-f|Je lui rends son soleil.",
    "narrateur|La virgule verte a un grain, pris dans le fil.",
]
ENDINGS[(1, 3, 3)] = [
    "narrateur|La bande de soleil a bougé, sur le tapis.",
    "narrateur|Mila pose le citron.",
    "narrateur|Le bol bleu l'accueille.",
    "enfant-f|Le toit du manteau, je l'ai mis au crochet.",
    "maman|Bien.",
    "maman|Le campement a son soleil, et son plaid.",
    "papa|On presse, quand tu veux.",
    "narrateur|Le doudou s'installe dans le creux.",
    "enfant-f|La feuille a un fil, tout petit.",
    "narrateur|La bande de soleil a bougé, elle touche le bol.",
]

T3[(2, 1, 1)] = [
    "narrateur|La rampe du toboggan se tait.",
    "enfant-f|Le ballon et le citron, je les ai.",
    "narrateur|Le seau, près des marches, n'a pas bougé.",
    "papa|Le ballon n'emporte pas l'anse.",
    "narrateur|Le sac à étoiles pend à la barrière du toboggan.",
    "enfant-f|Le zip, j'y arrive, cette fois.",
    "narrateur|Elle ouvre.",
    "narrateur|Une étoile, puis le manteau, le seau, le ballon.",
    "maman|Le citron au-dessus.",
    "maman|Sa feuille a vu la rampe.",
    "papa|Merci.",
    "papa|Tu l'as sorti de sous le métal.",
    "narrateur|La feuille jaune de la rampe colle au sac bleu.",
    "enfant-f|C'est sa médaille.",
    "maman|Le bol préférera le zeste à la médaille.",
    "narrateur|Le ballon s'enfonce, un peu froid.",
]
ENDINGS[(2, 1, 1)] = [
    "narrateur|Le manteau rouge retrouve le fauteuil.",
    "narrateur|Mila pose le citron dans le bol bleu.",
    "enfant-f|Il a glissé.",
    "enfant-f|Il est rentré.",
    "papa|La feuille de rampe, on la met près des clés ?",
    "maman|Un souvenir, oui.",
    "maman|Pas dans la limonade.",
    "narrateur|Le plaid reprend le creux.",
    "narrateur|L'horloge toque.",
    "enfant-f|La virgule a une pliure de poche.",
    "narrateur|Le sac à étoiles s'accroche au portemanteau.",
    "narrateur|Le manteau rouge retrouve le fauteuil, une feuille de rampe dans la poche.",
]

T3[(2, 1, 2)] = [
    "narrateur|Le ballon est un peu froid, près de la rampe.",
    "enfant-f|On rentre.",
    "enfant-f|J'ai mon soleil.",
    "maman|Le banc a le manteau.",
    "maman|Les marches ont le seau.",
    "narrateur|Le sac à carreaux est posé sur le banc du toboggan.",
    "papa|Carré pour le ballon.",
    "papa|Carré pour le seau.",
    "narrateur|Mila range.",
    "narrateur|Le citron, elle le garde au creux de la main.",
    "enfant-f|Toi, tu ne glisses plus.",
    "enfant-f|Tu rentres.",
    "maman|Merci.",
    "maman|Tu as gardé le jaune hors de la rampe.",
    "narrateur|Le ballon est un peu froid, près du sac rouge.",
    "papa|Au salon, le bol est tiède, lui.",
    "enfant-f|Il va le réchauffer.",
    "narrateur|Une feuille de rampe sèche au bord du sac.",
]
ENDINGS[(2, 1, 2)] = [
    "narrateur|Les clés de papa sont dans la coupelle.",
    "narrateur|Mila pose le citron.",
    "narrateur|Le bol bleu cligne, on dirait.",
    "enfant-f|Il est froid, comme la rampe.",
    "papa|Le salon va le tiédir.",
    "maman|La feuille de rampe sèche près des clés.",
    "narrateur|Elle remet le plaid.",
    "narrateur|Ça sent le zeste et le métal.",
    "enfant-f|Plus de houuu.",
    "enfant-f|Juste le toc de l'horloge.",
    "narrateur|Le sac à carreaux s'assoit sous la table.",
    "narrateur|Une feuille sèche près des clés de papa.",
]

T3[(2, 1, 3)] = [
    "narrateur|Une goutte tombe de la rampe, lente.",
    "enfant-f|Le ballon va rentrer, avant d'être mouillé.",
    "papa|Le seau, les marches, le manteau.",
    "papa|Avec nous.",
    "narrateur|Le sac à ronds est près de la grille du toboggan.",
    "narrateur|Le bouton de bois est humide.",
    "narrateur|Mila le tourne.",
    "maman|Ronds : ballon, citron, bouton.",
    "narrateur|Elle glisse le seau, le manteau, le ballon.",
    "enfant-f|Le citron au milieu, au sec.",
    "papa|Merci.",
    "papa|Tu l'as sorti de la goutte.",
    "narrateur|Une goutte glisse vers le sac vert, puis s'arrête.",
    "maman|Le bol, au salon, n'a pas de goutte.",
    "enfant-f|Que du clic.",
    "narrateur|La virgule verte a une perle d'eau, minuscule.",
]
ENDINGS[(2, 1, 3)] = [
    "narrateur|Ça sent le citron, un peu, dans le salon.",
    "narrateur|Mila le pose dans le bol bleu.",
    "narrateur|Clic.",
    "enfant-f|Ta perle d'eau a séché.",
    "maman|Le zeste a l'odeur du vent du toboggan.",
    "papa|La limonade aura un goût de rampe, peut-être.",
    "narrateur|Le plaid est remis.",
    "narrateur|Le campement reprend.",
    "enfant-f|Plus de grille, en bas.",
    "narrateur|Le sac à ronds sèche près de la porte.",
    "narrateur|Le citron a l'odeur du vent, dans le bol bleu.",
]

T3[(2, 2, 1)] = [
    "narrateur|Le seau a sonné contre les marches, toute la descente.",
    "enfant-f|On a fini de glisser.",
    "narrateur|Le manteau, sur le banc, n'a pas sonné.",
    "maman|Il vient, lui aussi, sans musique.",
    "narrateur|Le sac à étoiles pend.",
    "narrateur|Mila tire, crcr.",
    "papa|Le seau droit, comme sur les marches.",
    "narrateur|Elle le pose, anse vers le zip, pour le tenir.",
    "enfant-f|Le citron au-dessus.",
    "enfant-f|Plus de pente.",
    "papa|Merci.",
    "papa|Tes deux mains ont tenu l'anse.",
    "narrateur|Le seau sonne, très bas, contre le sac bleu.",
    "maman|Au salon, le bol n'a pas de pente.",
    "enfant-f|Il est plat.",
    "enfant-f|Il attend.",
    "narrateur|Une étoile de tissu a un choc de plastique.",
]
ENDINGS[(2, 2, 1)] = [
    "narrateur|Le seau penche un peu, sous le portemanteau.",
    "narrateur|Mila pose le citron.",
    "narrateur|Le bol bleu le reçoit à plat.",
    "enfant-f|Plus de marches.",
    "enfant-f|Plus de pente.",
    "papa|Le clic, ici, est sage.",
    "maman|La limonade n'a pas besoin de rampe.",
    "narrateur|Le plaid reprend le creux.",
    "narrateur|L'horloge toque.",
    "enfant-f|La virgule n'a pas glissé.",
    "narrateur|Le sac à étoiles s'accroche, zip fermé.",
    "narrateur|Le seau penche, une goutte de rampe au fond.",
]

T3[(2, 2, 2)] = [
    "narrateur|Le métal du toboggan se tait, près du banc.",
    "enfant-f|Le seau rentre.",
    "enfant-f|Le citron aussi.",
    "papa|Le manteau, sur le banc, n'est pas une marche.",
    "narrateur|Le sac à carreaux est ouvert, comme une rampe douce.",
    "maman|On glisse les affaires, sans les jeter.",
    "narrateur|Mila glisse le seau, puis le manteau, puis le citron.",
    "enfant-f|Une glissade sage, celle-là.",
    "maman|Merci.",
    "maman|Tu as choisi la pente du sac.",
    "narrateur|Le métal du toboggan se tait, près du sac rouge.",
    "papa|Le bol, lui, n'est pas une rampe.",
    "enfant-f|Je le sais.",
    "enfant-f|Je le remplis.",
    "narrateur|Un carreau garde une trace d'anse.",
]
ENDINGS[(2, 2, 2)] = [
    "narrateur|Le plaid a glissé.",
    "narrateur|Mila le remet.",
    "narrateur|Le citron rentre dans le bol bleu, sans pente.",
    "enfant-f|Une glissade sage, tu as dit.",
    "maman|Oui.",
    "maman|Et un bol plein.",
    "papa|La limonade peut attendre une minute.",
    "narrateur|Le seau s'assoit sous le portemanteau.",
    "enfant-f|La feuille a une trace de plastique.",
    "narrateur|Le sac à carreaux s'endort contre le canapé.",
    "narrateur|Mila remet le plaid, et le bol a son citron.",
]

T3[(2, 2, 3)] = [
    "narrateur|Un pas sur la rampe, derrière.",
    "narrateur|Personne.",
    "enfant-f|C'est le vent.",
    "enfant-f|On rentre.",
    "maman|Seau, manteau, citron.",
    "maman|Avant le vent.",
    "narrateur|Le sac à ronds est près de la grille, bouton clair.",
    "papa|Tu tournes.",
    "papa|Tu glisses.",
    "papa|Tu fermes.",
    "narrateur|Mila tourne le bouton.",
    "narrateur|Le seau entre, droit.",
    "enfant-f|Le citron, je le tiens jusqu'à la maison.",
    "papa|Merci.",
    "papa|Tu n'as pas relâché l'anse.",
    "narrateur|Un pas sur la rampe, puis le sac vert se ferme.",
    "maman|Le bol n'a pas de vent.",
    "enfant-f|Je lui porte son soleil.",
    "narrateur|La virgule verte a un souffle de rampe, on dirait.",
]
ENDINGS[(2, 2, 3)] = [
    "narrateur|Loin, le toboggan se tait.",
    "narrateur|Ici, le citron fait clic dans le bol bleu.",
    "enfant-f|Le vent n'est pas venu.",
    "maman|Le campement est au chaud.",
    "papa|On presse le zeste, quand tu seras prête.",
    "narrateur|Le plaid est remis.",
    "narrateur|Les coussins tiennent.",
    "enfant-f|La feuille sent le métal, un peu.",
    "narrateur|Le sac à ronds s'adosse à la porte close.",
    "narrateur|Loin, le toboggan se tait, ici le clic du citron.",
]

T3[(2, 3, 1)] = [
    "narrateur|Le doudou a vu le toboggan, tout gris.",
    "enfant-f|On rentre.",
    "enfant-f|Le soleil est dans le foulard, plus.",
    "papa|Il est dans ta main, maintenant.",
    "papa|Le seau aussi.",
    "narrateur|Le sac à étoiles pend.",
    "narrateur|Mila ouvre, le doudou d'abord.",
    "maman|Tête vers le zip, pour qu'il respire.",
    "narrateur|Manteau.",
    "narrateur|Seau.",
    "narrateur|Citron contre l'oreille, à vue.",
    "enfant-f|Plus de poche.",
    "enfant-f|Plus de cachette.",
    "papa|Merci.",
    "papa|Tu as dénoué le foulard, tout à l'heure.",
    "narrateur|Le doudou a vu le toboggan, dans le sac bleu.",
    "maman|Le bol va voir un soleil, lui.",
    "enfant-f|Sans foulard.",
    "narrateur|Un fil du foulard reste au zip.",
]
ENDINGS[(2, 3, 1)] = [
    "narrateur|L'oreille du doudou dépasse du fauteuil.",
    "narrateur|Mila pose le citron dans le bol bleu.",
    "enfant-f|Plus de foulard.",
    "enfant-f|Plus de cachette.",
    "maman|Le zeste est à l'air.",
    "papa|Le fil du zip, on le range demain.",
    "narrateur|Le plaid couvre le creux.",
    "narrateur|L'horloge toque.",
    "enfant-f|Il a l'odeur du vent du toboggan.",
    "narrateur|Le sac à étoiles s'affaisse, une étoile pliée.",
    "narrateur|L'oreille grise a l'odeur du vent du toboggan.",
]

T3[(2, 3, 2)] = [
    "narrateur|L'oreille molle dépasse, près de la rampe.",
    "enfant-f|On a fini de glisser, doudou.",
    "maman|Le banc.",
    "maman|Le seau.",
    "maman|Le manteau.",
    "narrateur|Le sac à carreaux est sur le banc, un carreau plié.",
    "papa|Doudou sur le gris du sac.",
    "papa|Citron à côté, pas dessous.",
    "narrateur|Mila range.",
    "narrateur|Elle ne recouvre plus le jaune.",
    "enfant-f|Je te vois, soleil.",
    "maman|Merci.",
    "maman|Tu as laissé la virgule à l'air.",
    "narrateur|L'oreille molle dépasse du sac rouge.",
    "papa|Le bol, au salon, laissera la feuille à l'air, trop.",
    "enfant-f|Oui.",
    "enfant-f|Pour la reconnaître.",
    "narrateur|Un carreau garde une odeur de métal.",
]
ENDINGS[(2, 3, 2)] = [
    "narrateur|Le citron est lisse, un peu froid, dans la main.",
    "narrateur|Mila le pose.",
    "narrateur|Le bol bleu le tient.",
    "enfant-f|Ta virgule est à l'air.",
    "papa|On la verra, pour la limonade.",
    "maman|Le doudou a l'oreille hors du fauteuil.",
    "narrateur|Elle remet le plaid.",
    "narrateur|Le campement se referme.",
    "enfant-f|Plus de rampe dans la poche.",
    "narrateur|Le sac à carreaux s'assoit, oreille dehors.",
    "narrateur|La virgule verte a une pliure de poche.",
]

T3[(2, 3, 3)] = [
    "narrateur|La rampe brille.",
    "narrateur|Le doudou cligne, on dirait.",
    "enfant-f|On n'y remet pas le jaune.",
    "papa|On le met dans le sac à ronds, près de la grille.",
    "narrateur|Le bouton de bois.",
    "narrateur|Mila le tourne, deux fois.",
    "maman|Rond le doudou, rond le citron, rond le bouton.",
    "narrateur|Elle glisse le seau, le manteau, le gris, le jaune.",
    "enfant-f|Tous visibles, dans la bouche du sac.",
    "papa|Merci.",
    "papa|Tu n'as rien caché sous le foulard.",
    "narrateur|La rampe brille, loin du sac vert.",
    "maman|Le bol n'a pas de rampe.",
    "enfant-f|Je le remplis.",
    "narrateur|La virgule verte a une poussière de métal.",
]
ENDINGS[(2, 3, 3)] = [
    "narrateur|Le rayon d'après-midi a bougé, sur le tapis.",
    "narrateur|Mila pose le citron.",
    "narrateur|Le bol bleu l'arrête.",
    "enfant-f|Plus de pente.",
    "enfant-f|Il s'arrête.",
    "maman|Le campement a son soleil, arrêté.",
    "papa|La limonade peut tourner, elle, dans le verre.",
    "narrateur|Le plaid est remis.",
    "narrateur|Le doudou s'assoit.",
    "enfant-f|La feuille a une poussière de rampe.",
    "narrateur|Le sac à ronds s'adosse, bouton vers le mur.",
    "narrateur|Le rayon a quitté le tapis, il dore le bol.",
]

T3[(3, 1, 1)] = [
    "narrateur|Les cordes se taisent.",
    "narrateur|Le ballon penche.",
    "enfant-f|J'ai le fil.",
    "enfant-f|J'ai le citron.",
    "narrateur|Le seau, au pied de bois, n'a pas de fil.",
    "papa|Il vient quand même.",
    "narrateur|Le sac à étoiles pend à la barrière des balançoires.",
    "enfant-f|Le zip, et le fil du ballon, c'est pareil un peu.",
    "narrateur|Elle ouvre.",
    "narrateur|Manteau.",
    "narrateur|Seau.",
    "narrateur|Ballon.",
    "narrateur|Citron à l'air.",
    "maman|Deux ronds, deux mains, tout à l'heure.",
    "papa|Merci.",
    "papa|Tu n'as pas relâché le jaune pour le fil.",
    "narrateur|La chaîne a fait cling, près du sac bleu.",
    "enfant-f|Le bol n'a pas de fil.",
    "narrateur|Un brin d'herbe reste au cuir, dans le sac.",
]
ENDINGS[(3, 1, 1)] = [
    "narrateur|Le ballon s'endort près du canapé, près du bol.",
    "narrateur|Mila pose le citron.",
    "narrateur|Le bol bleu le berce, on dirait.",
    "enfant-f|Plus de fil.",
    "enfant-f|Plus de rafale.",
    "papa|Le cling des cordes, on ne l'entend plus.",
    "maman|L'horloge toque, plus bas.",
    "narrateur|Le plaid reprend le creux.",
    "narrateur|Le campement se pose.",
    "enfant-f|La virgule a un brin, tout petit.",
    "narrateur|Le sac à étoiles s'affaisse, une étoile tordue.",
    "narrateur|Le ballon s'endort contre un coussin, près du bol.",
]

T3[(3, 1, 2)] = [
    "narrateur|Le ballon a touché le sable, près des balançoires.",
    "enfant-f|On rentre.",
    "enfant-f|Le rouge et le jaune.",
    "maman|Le pied de bois a le seau.",
    "maman|Le banc a le manteau.",
    "narrateur|Le sac à carreaux est sur le banc des balançoires.",
    "papa|Un carreau pour le fil, enroulé.",
    "papa|Un carreau pour le jaune.",
    "narrateur|Mila enroule le fil.",
    "narrateur|Elle pose le citron à part.",
    "enfant-f|Vous ne vous mélangez plus.",
    "maman|Merci.",
    "maman|Tu as séparé l'ombre rouge du jaune.",
    "narrateur|Le ballon a touché le sable, près du sac rouge.",
    "papa|Le bol n'a pas d'ombre rouge.",
    "enfant-f|Que du bleu, et mon soleil.",
    "narrateur|Un carreau garde un brin d'herbe.",
]
ENDINGS[(3, 1, 2)] = [
    "narrateur|Le creux du canapé attend Mila.",
    "narrateur|Elle pose d'abord le citron dans le bol bleu.",
    "enfant-f|Séparés, le rouge et le jaune.",
    "papa|Le ballon près du coussin.",
    "papa|Le citron dans le bleu.",
    "maman|La limonade n'aura pas de fil.",
    "narrateur|Le plaid la rejoint, dans le creux.",
    "enfant-f|La feuille n'a plus d'ombre de ballon.",
    "narrateur|Le sac à carreaux s'assoit sous le banc du salon.",
    "narrateur|Le creux du canapé attend Mila, citron rentré.",
]

T3[(3, 1, 3)] = [
    "narrateur|Un nuage passe au-dessus des balançoires.",
    "enfant-f|Le ballon baisse.",
    "enfant-f|On rentre.",
    "papa|Seau, manteau, citron.",
    "papa|Avant que le nuage reste.",
    "narrateur|Le sac à ronds est près de la grille, bouton pâle.",
    "maman|Tu tournes.",
    "maman|Tu comptes les ronds.",
    "narrateur|Ballon.",
    "narrateur|Citron.",
    "narrateur|Bouton.",
    "narrateur|Seau.",
    "narrateur|Manteau.",
    "enfant-f|Cinq.",
    "enfant-f|Tous là.",
    "papa|Merci.",
    "papa|Tu as compté le jaune, pas seulement le rouge.",
    "narrateur|Un nuage passe au-dessus du sac vert.",
    "maman|Le bol, sous le toit, n'a pas de nuage.",
    "enfant-f|Il a un rond de lumière.",
    "narrateur|La virgule verte a une ombre de nuage, un instant.",
]
ENDINGS[(3, 1, 3)] = [
    "narrateur|Ça sent le zeste et l'herbe, dans le salon.",
    "narrateur|Mila pose le citron.",
    "narrateur|Le bol bleu l'abrite.",
    "enfant-f|Plus de nuage.",
    "enfant-f|Plus de fil.",
    "maman|Le toit de la maison suffit.",
    "papa|La limonade aura un goût d'herbe, un peu ?",
    "narrateur|Elle rit.",
    "narrateur|Le plaid la couvre.",
    "enfant-f|Un tout petit goût.",
    "narrateur|Le sac à ronds s'adosse, le ballon dedans.",
    "narrateur|Ça sent le zeste et l'herbe, près du bol.",
]

T3[(3, 2, 1)] = [
    "narrateur|Le seau a servi de nid, sous la balançoire.",
    "enfant-f|On rentre.",
    "enfant-f|Le nid vient.",
    "maman|Le banc a le manteau.",
    "maman|Il n'est pas un nid.",
    "narrateur|Le sac à étoiles pend.",
    "narrateur|Mila hisse le seau.",
    "papa|L'anse, deux mains, comme tout à l'heure.",
    "narrateur|Le seau entre.",
    "narrateur|Le manteau.",
    "narrateur|Le citron au fond, à vue.",
    "enfant-f|Un nid qui voyage, pour le bol.",
    "papa|Merci.",
    "papa|Tes tibias ont ramené le seau.",
    "narrateur|L'anse du seau est froide, contre le sac bleu.",
    "maman|Le bol n'a pas d'anse.",
    "enfant-f|Je connais son bord.",
    "narrateur|Une étoile de tissu a une trace d'herbe.",
]
ENDINGS[(3, 2, 1)] = [
    "narrateur|L'ombre du seau, ronde, touche le tapis beige.",
    "narrateur|Mila pose le citron dans le bol bleu.",
    "enfant-f|Le nid a voyagé.",
    "enfant-f|Le soleil aussi.",
    "papa|Le bol est un nid, maintenant.",
    "maman|Pour la limonade, après le repos.",
    "narrateur|Le plaid reprend le creux.",
    "narrateur|L'horloge toque.",
    "enfant-f|L'anse est moins froide.",
    "narrateur|Le sac à étoiles s'accroche, anse dedans.",
    "narrateur|L'ombre du seau, ronde, touche le tapis beige.",
]

T3[(3, 2, 2)] = [
    "narrateur|Un cling lointain.",
    "narrateur|Une autre balançoire, loin.",
    "enfant-f|La nôtre s'est arrêtée.",
    "enfant-f|On rentre.",
    "papa|Nid, manteau, citron.",
    "papa|Avant le cling des autres.",
    "narrateur|Le sac à carreaux est sur le banc, un carreau ouvert.",
    "maman|Le seau sur le carreau du bas.",
    "maman|Le citron sur le clair.",
    "narrateur|Mila range.",
    "narrateur|Elle ne met plus le seau sous ses pieds.",
    "enfant-f|Le nid, dans le sac.",
    "enfant-f|Pas sous les talons.",
    "maman|Merci.",
    "maman|Tu as changé la place du seau.",
    "narrateur|Un cling lointain, et le sac rouge se ferme.",
    "papa|Le bol n'a pas de cling.",
    "enfant-f|Je le lui rends, le clic.",
    "narrateur|Un carreau garde une trace de tibia, de poussière.",
]
ENDINGS[(3, 2, 2)] = [
    "narrateur|Le plaid tricoté est chaud, sur les genoux.",
    "narrateur|Le bol bleu est à côté, le citron dedans.",
    "enfant-f|Le clic est rentré.",
    "papa|Plus de cling.",
    "papa|Que le toc de l'horloge.",
    "maman|La limonade, on la fera près du plaid.",
    "narrateur|Le seau s'assoit, ombre ronde.",
    "enfant-f|La feuille a une poussière de banc.",
    "narrateur|Le sac à carreaux s'endort sous la table.",
    "narrateur|Le plaid est chaud sur les genoux, bol à côté.",
]

T3[(3, 2, 3)] = [
    "narrateur|Le seau jaune pose son ombre au pied de bois.",
    "enfant-f|L'ombre rentre, elle aussi.",
    "maman|Le manteau.",
    "maman|Le seau.",
    "maman|Le citron.",
    "narrateur|Le sac à ronds est près de la grille, bouton rond.",
    "papa|L'ombre du seau, ronde, rentre dans un rond.",
    "narrateur|Mila glisse le seau, le manteau, le citron au milieu.",
    "enfant-f|Le nid au milieu, comme sous la balançoire.",
    "enfant-f|Mais fermé.",
    "papa|Merci.",
    "papa|Tu as fermé le nid, cette fois.",
    "narrateur|Le seau jaune pose son ombre au sac vert.",
    "maman|Le bol a un rond de lumière, pas d'ombre de seau.",
    "enfant-f|Je lui donne le soleil, pas l'ombre.",
    "narrateur|La virgule verte a une poussière de pied de bois.",
]
ENDINGS[(3, 2, 3)] = [
    "narrateur|Les clés de papa restent dans la coupelle.",
    "narrateur|Le citron, lui, rentre dans le bol bleu.",
    "enfant-f|Le soleil, pas l'ombre.",
    "maman|La limonade sera claire, alors.",
    "papa|Le seau sèche.",
    "papa|Son ombre est sage.",
    "narrateur|Le plaid reprend le creux.",
    "narrateur|Le campement se tait.",
    "enfant-f|La feuille a vu le pied de bois.",
    "narrateur|Le sac à ronds s'adosse, ombre courte.",
    "narrateur|Les clés restent dans la coupelle, le citron dans le bleu.",
]

T3[(3, 3, 1)] = [
    "narrateur|Le doudou a senti le vent, entre les sièges.",
    "enfant-f|On ne se passe plus le soleil en l'air.",
    "papa|On le passe dans le sac à étoiles, à la barrière.",
    "narrateur|Mila ouvre le zip.",
    "narrateur|Le doudou entre, assis.",
    "maman|Le citron à côté, pas entre les sièges.",
    "narrateur|Seau.",
    "narrateur|Manteau.",
    "narrateur|Jaune à vue, contre le gris.",
    "enfant-f|Les mains, pas l'air.",
    "papa|Merci.",
    "papa|Tu as cherché la virgule, pas la colère.",
    "narrateur|Le doudou a senti le vent, dans le sac bleu.",
    "maman|Le bol n'a pas de vent.",
    "enfant-f|Je lui porte le soleil, dans les mains.",
    "narrateur|Un fil gris pend, pris dans une étoile.",
]
ENDINGS[(3, 3, 1)] = [
    "narrateur|Le doudou a l'odeur de l'herbe, au salon.",
    "narrateur|Mila pose le citron dans le bol bleu.",
    "enfant-f|Dans les mains, pas en l'air.",
    "maman|Le zeste a voyagé, sans tomber.",
    "papa|La limonade n'a pas besoin de vent.",
    "narrateur|Le plaid couvre le creux.",
    "narrateur|L'horloge toque.",
    "enfant-f|La virgule a de la poussière de pied de bois.",
    "narrateur|Le sac à étoiles s'endort, une étoile tordue.",
    "narrateur|Le doudou a l'odeur de l'herbe des balançoires.",
]

T3[(3, 3, 2)] = [
    "narrateur|La chaîne se tait, près du banc.",
    "enfant-f|Le doudou rentre.",
    "enfant-f|Le citron aussi.",
    "maman|Le seau au pied.",
    "maman|Le manteau au banc.",
    "narrateur|Le sac à carreaux est sur le banc, un carreau pour le gris.",
    "papa|Doudou.",
    "papa|Seau.",
    "papa|Manteau.",
    "papa|Citron à part, visible.",
    "narrateur|Mila ne lance plus.",
    "narrateur|Elle pose.",
    "enfant-f|Posé, pas lancé.",
    "maman|Merci.",
    "maman|Tes mains ont appris le passage.",
    "narrateur|La chaîne se tait, près du sac rouge.",
    "papa|Le bol n'a pas de chaîne.",
    "enfant-f|Je pose, sur le bord.",
    "narrateur|Un carreau garde une poussière de siège.",
]
ENDINGS[(3, 3, 2)] = [
    "narrateur|Le citron rentre.",
    "narrateur|La feuille verte tremble, puis s'arrête.",
    "narrateur|Le bol bleu le tient, sans balançoire.",
    "enfant-f|Posé.",
    "enfant-f|Pas lancé.",
    "papa|Le campement a son soleil, posé.",
    "maman|La limonade, on la posera aussi, dans les verres.",
    "narrateur|Le plaid est remis.",
    "narrateur|Le doudou s'assoit.",
    "enfant-f|Plus de siège vide, à côté.",
    "narrateur|Le sac à carreaux s'assoit, comme un banc.",
    "narrateur|Le citron rentre, et la feuille verte tremble, puis s'arrête.",
]

T3[(3, 3, 3)] = [
    "narrateur|L'oreille grise dépasse, entre les deux sièges vides.",
    "enfant-f|On rentre.",
    "enfant-f|Le vent peut garder les cordes.",
    "papa|Le sac à ronds, près de la grille, garde le reste.",
    "narrateur|Mila tourne le bouton.",
    "narrateur|Ça cède.",
    "maman|Rond l'oreille, rond le citron, rond le bouton.",
    "narrateur|Elle glisse le doudou, le seau, le manteau, le jaune.",
    "enfant-f|Le campement du salon va tout revoir.",
    "papa|Merci.",
    "papa|Tu as ramassé entre les pieds de bois.",
    "narrateur|L'oreille grise dépasse du sac vert.",
    "maman|Le bol a un rond de lumière, qui t'attend.",
    "enfant-f|Je lui rends son soleil.",
    "narrateur|La virgule verte a de la poussière, et de l'herbe.",
]
ENDINGS[(3, 3, 3)] = [
    "narrateur|Le campement du salon a retrouvé son soleil.",
    "narrateur|Mila pose le citron dans le bol bleu.",
    "enfant-f|Promis, j'ai tenu.",
    "maman|La limonade peut commencer, quand tu veux.",
    "papa|Le rond de lumière n'est plus vide.",
    "narrateur|Le plaid reprend le creux.",
    "narrateur|L'horloge toque.",
    "enfant-f|La virgule a voyagé.",
    "enfant-f|Elle est rentrée.",
    "narrateur|Le sac à ronds s'adosse.",
    "narrateur|L'oreille dépasse.",
    "narrateur|Le campement du salon a retrouvé son soleil.",
]

T3_SONS = {1: "zip,sac", 2: "sac,banc", 3: "bouton,grille"}
T3_EMPH = {1: "sac à étoiles", 2: "sac à carreaux", 3: "sac à ronds"}
END_SONS = {1: "sable,salon", 2: "toboggan,salon", 3: "balancoire,salon"}


def ending_note(a: int, b: int, c: int) -> str:
    emos = {1: "fierté_calme", 2: "tendresse", 3: "chaleur"}
    tempos = {1: "posé", 2: "lent", 3: "ample"}
    return (
        f"arc=retour; intention=refermer; emotion={emos[c]}; intensite=1; "
        f"destinataire=enfant; sous_texte=le_bol_a_son_soleil; "
        f"tempo={tempos[c]}; sourire=léger; respiration=ample; chemin={a}{b}{c}"
    )


def path_words(chunks_by_id: dict, a: int, b: int, c: int) -> int:
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
    return sum(words(chunks_by_id[i]["text"]) for i in ids)


def listy_debug(chunks: list[dict]) -> str | None:
    starts: list[tuple[str, str]] = []
    for c in chunks:
        for ln in c["script"].splitlines():
            if "|" not in ln:
                continue
            role, phrase = ln.split("|", 1)
            if role != "narrateur":
                starts.append(("", c["chunk_id"]))
                continue
            tok = phrase.strip().split()[0].lower() if phrase.strip().split() else ""
            starts.append((tok, c["chunk_id"]))
    run = 1
    for i in range(1, len(starts)):
        if starts[i][0] and starts[i][0] == starts[i - 1][0]:
            run += 1
            if run >= 4:
                window = starts[i - 3 : i + 1]
                return f"{starts[i][0]} @ {window}"
        else:
            run = 1
    return None


def main() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    missing_t3 = [k for k in ((a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)) if k not in T3]
    missing_e = [k for k in ((a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)) if k not in ENDINGS]
    if missing_t3 or missing_e:
        raise SystemExit(f"missing T3={missing_t3[:4]} END={missing_e[:4]}")

    out_chunks["CHK_T0000_P0000"] = voice(
        by_src["CHK_T0000_P0000"], OPENING, "opening", "horloge,bol,plaid"
    )
    out_chunks["CHK_T0001_P0000"] = voice(
        by_src["CHK_T0001_P0000"],
        T1_CHOICE,
        "choice",
        "grille,parc",
        {
            "pause_before_ms": 200,
            "fields": {
                "option_1_label": "le bac à sable",
                "option_2_label": "le toboggan",
                "option_3_label": "les balançoires",
            },
        },
    )

    for a in (1, 2, 3):
        t1 = T1[a]
        base = f"CHK_T0001_P000{a}"
        out_chunks[base] = voice(
            by_src[base], t1["passage"], "action", t1["sons"], {"emphasis": t1["emphasis"]}
        )
        out_chunks[f"{base}_Q0001"] = voice(
            by_src[f"{base}_Q0001"],
            t1["question"],
            "clue",
            "",
            {"emphasis": t1["emphasis"], "pause_before_ms": 200, "fields": t1["qfields"]},
        )
        out_chunks[f"{base}_C0001"] = voice(
            by_src[f"{base}_C0001"], t1["confirm"], "confirm", t1["sons"], {"emphasis": t1["emphasis"]}
        )
        out_chunks[f"{base}_T0002_P0000"] = voice(
            by_src[f"{base}_T0002_P0000"],
            T2_CHOICE[a],
            "choice",
            "",
            {
                "pause_before_ms": 200,
                "fields": {
                    "option_1_label": "le ballon",
                    "option_2_label": "le seau",
                    "option_3_label": "le doudou",
                },
            },
        )
        for b in (1, 2, 3):
            t2 = T2[(a, b)]
            bse = f"{base}_T0002_P000{b}"
            out_chunks[bse] = voice(
                by_src[bse], t2["passage"], "obstacle", t2["sons"], {"emphasis": t2["emphasis"]}
            )
            out_chunks[f"{bse}_T0003_P0000"] = voice(
                by_src[f"{bse}_T0003_P0000"],
                T3_CHOICE[(a, b)],
                "choice",
                "",
                {
                    "pause_before_ms": 200,
                    "fields": {
                        "option_1_label": "le sac à étoiles",
                        "option_2_label": "le sac à carreaux",
                        "option_3_label": "le sac à ronds",
                    },
                },
            )
            for c in (1, 2, 3):
                leaf = f"{bse}_T0003_P000{c}"
                out_chunks[leaf] = voice(
                    by_src[leaf],
                    T3[(a, b, c)],
                    "resolution",
                    T3_SONS[c],
                    {"emphasis": T3_EMPH[c]},
                )
                fin = f"{leaf}_F0001"
                out_chunks[fin] = voice(
                    by_src[fin],
                    ENDINGS[(a, b, c)],
                    "ending",
                    END_SONS[a],
                    {"emphasis": "bol bleu", "note": ending_note(a, b, c)},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = set(out_chunks) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:6]} extra={sorted(extra)[:6]}")

    story = dict(src)
    story["fil_rouge"] = (
        "Mila veut porter le citron du bol bleu au parc pour qu'il soit le soleil "
        "du jeu, puis le ramener avant la limonade. Elle l'attrape trop vite : il "
        "roule sous le plaid. La virgule verte le trahit. Au parc, la première "
        "idée rate. Ballon, seau ou doudou cachent le jaune plus malin. "
        "Sac à étoiles, à carreaux ou à ronds rassemblent seau, manteau, jeu et "
        "citron. Vingt-sept fins : le bol retrouve son soleil, la feuille a voyagé."
    )
    story["title"] = TITLE
    story["characters"] = "Mila, papa, maman"
    story["setting"] = "salon (campement), puis parc"
    story["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]

    listed = listy_debug(story["chunks"])
    if listed:
        raise SystemExit(f"puces globales: {listed}")

    blob = "\n".join(c["script"] for c in story["chunks"]).lower()
    if blob.count("en ce moment") != 1:
        raise SystemExit(f"{SID}: en ce moment ×{blob.count('en ce moment')}")
    if "mila" not in blob:
        raise SystemExit(f"{SID}: Mila absente")
    for tic in ("tout doux", "tout calme", " aujourd'hui,", "merle", "couleur de miel", "mission accomplie"):
        if tic in blob:
            raise SystemExit(f"{SID}: tic {tic}")
    if TICS.search(blob):
        raise SystemExit(f"{SID}: tic corpus {TICS.search(blob).group(0)}")
    for bad in ("tom ", "léa", "sami", "grand-père", "maîtresse", "jardinier", "bibliothécaire", "gardienne"):
        if bad in blob:
            raise SystemExit(f"{SID}: interdit {bad}")

    check(SID, story["age_band"], story["chunks"])

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

    res_txt = [
        c["text"]
        for c in story["chunks"]
        if c["kind"] == "passage"
        and "_T0003_P000" in c["chunk_id"]
        and "_F0001" not in c["chunk_id"]
        and not c["chunk_id"].endswith("_T0003_P0000")
    ]
    if len(res_txt) != 27 or len(set(res_txt)) != 27:
        raise SystemExit(f"résolutions distinctes {len(set(res_txt))}/27")

    counts = [path_words(out_chunks, a, b, c) for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    print(f"chemins mots min={min(counts)} max={max(counts)} moy={sum(counts)//len(counts)}")
    if min(counts) < 550:
        raise SystemExit(f"chemin trop court: {min(counts)}")
    if max(counts) > 720:
        raise SystemExit(f"chemin trop long: {max(counts)}")

    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in story["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")

    path = ROOT / SID / "merged.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} bytes={path.stat().st_size}")

    (ROOT / SID / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "- **Nouveau titre :** *Le citron dans le bol bleu*\n"
        "- **Public :** N2 (3–6 ans), lecture interactive familiale\n"
        "- **Leçon principale :** AUT.AFF.003 — reprendre ses affaires (vécue, non dite)\n"
        "- **Personnages :** Mila, papa, maman\n"
        "- **Structure conservée :** 86 nœuds, trois choix à trois options, "
        "27 chemins et 27 fins distinctes\n\n"
        "## Promesse narrative\n\n"
        "L'horloge du salon répond au clic du citron dans le bol bleu. Mila veut "
        "porter ce citron au parc pour qu'il soit le soleil du jeu, puis le ramener "
        "avant la limonade. Une feuille verte, mince, reste collée dessus : une "
        "virgule. Elle l'attrape trop vite : le bol bascule, le jaune file sous le "
        "plaid. Bac, toboggan ou balançoires changent l'obstacle ; ballon, seau ou "
        "doudou cachent le jaune plus malin ; sac à étoiles, à carreaux ou à ronds "
        "rassemblent seau, manteau, jeu et citron. Au retour, le bol retrouve son "
        "soleil, et la virgule a voyagé.\n\n"
        "## Améliorations appliquées\n\n"
        "- Ouverture : deux bruits se répondent (toc / clic), puis l'objet. "
        "Pas « Aujourd'hui, je mène la mission ».\n"
        "- Indice unique du début : la virgule verte, payée à chaque fin.\n"
        "- Corps : sourire disparu, envie et inquiétude dans la poitrine, "
        "adulte accroupi à la même hauteur.\n"
        "- Première idée échoue (paume trop vite, château, rampe, herbe).\n"
        "- Seconde ruse : Mila refuse de foncer ; personne ne donne la réponse ; "
        "elle observe, écoute, retrouve la virgule.\n"
        "- T1 ne retire pas l'équipement (citron, seau, manteau).\n"
        "- T3 : sacs (plus Tom / Léa / Sami). Leçon dans le geste de rassembler.\n"
        "- 27 fins textuellement distinctes, dernière image unique.\n"
        "- Un merci vécu (confirmations et sacs), question d'adulte.\n"
        "- Pas de « encore / déjà / tout doux », pas merle, pas miel, pas apply.\n\n"
        "## Direction vocale\n\n"
        "TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending) : "
        "rate, pitch, volume, pauses, text_ssml, text_xai_tags, notes d'arc. "
        "slow réservé aux choix, indices et retours.\n\n"
        "## Contrôles\n\n"
        f"- 86 chunks\n"
        f"- 27 chemins, {min(counts)} à {max(counts)} mots, moyenne {sum(counts)//len(counts)}\n"
        "- 27 fins et 27 dernières images distinctes\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés\n"
        "- N2 ≤ 15 mots/phrase. `check()` OK.\n\n"
        "## Relu\n\n"
        "P0000, 3 L1, 9 L2, 27 résolutions, 27 fins. Questions liées à la scène "
        "(seau / manteau). Impatience, découragement, fierté calme.\n\n"
        "## Non vérifié\n\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
