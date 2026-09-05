#!/usr/bin/env python3
"""TREE-COL-020 — Le coussin tiède de Nina (texte + voix, pas d'audio)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from _lib import check, words  # noqa: E402

SID = "TREE-COL-020"
MAX_W = 16

PROFILES = {
    "opening": {
        "rate": "medium",
        "wpm": 142,
        "speed": 0.98,
        "piper": 1.12,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "medium",
        "db": 0,
        "pause": 500,
        "sentence": 260,
        "energy": "warm",
        "contour": "storytelling",
        "noise": 0.36,
        "emphasis": "coussin",
        "note": (
            "arc=installation; intention=émerveiller; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=une phrase chaude attend; tempo=naturel; "
            "sourire=léger; respiration=ample"
        ),
    },
    "choice": {
        "rate": "slow",
        "wpm": 116,
        "speed": 0.84,
        "piper": 1.30,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "medium",
        "db": 0,
        "pause": 900,
        "sentence": 330,
        "energy": "focused",
        "contour": "rising",
        "noise": 0.33,
        "emphasis": None,
        "note": (
            "arc=choix; intention=inviter; emotion=curiosité; intensite=1; "
            "destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; "
            "sourire=léger; respiration=pause_avant_choix"
        ),
    },
    "clue": {
        "rate": "slow",
        "wpm": 120,
        "speed": 0.86,
        "piper": 1.27,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "soft",
        "db": -2,
        "pause": 700,
        "sentence": 320,
        "energy": "focused",
        "contour": "rising",
        "noise": 0.32,
        "emphasis": None,
        "note": (
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; "
            "sourire=aucun; respiration=courte_avant_question"
        ),
    },
    "confirm": {
        "rate": "medium",
        "wpm": 132,
        "speed": 0.92,
        "piper": 1.20,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "medium",
        "db": 0,
        "pause": 450,
        "sentence": 280,
        "energy": "bright",
        "contour": "falling",
        "noise": 0.34,
        "emphasis": None,
        "note": (
            "arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; "
            "destinataire=enfant; sous_texte=la_piste_continue; tempo=naturel; "
            "sourire=léger; respiration=fluide"
        ),
    },
    "action": {
        "rate": "medium",
        "wpm": 146,
        "speed": 1.0,
        "piper": 1.10,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "medium",
        "db": 0,
        "pause": 420,
        "sentence": 250,
        "energy": "lively",
        "contour": "dynamic",
        "noise": 0.37,
        "emphasis": None,
        "note": (
            "arc=action; intention=entraîner; emotion=élan; intensite=2; "
            "destinataire=enfant; sous_texte=il_faut_faire_vite; tempo=vif; "
            "sourire=léger; respiration=courte"
        ),
    },
    "obstacle": {
        "rate": "medium",
        "wpm": 134,
        "speed": 0.93,
        "piper": 1.18,
        "pitch": "low",
        "pitchSsml": "-2st",
        "pitchTag": "low-pitch",
        "volume": "medium",
        "db": 0,
        "pause": 520,
        "sentence": 300,
        "energy": "tense",
        "contour": "dynamic",
        "noise": 0.34,
        "emphasis": None,
        "note": (
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; "
            "intensite=2; destinataire=enfant; sous_texte=les_mots_se_cognent; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    },
    "resolution": {
        "rate": "medium",
        "wpm": 140,
        "speed": 0.97,
        "piper": 1.14,
        "pitch": "medium",
        "pitchSsml": "medium",
        "pitchTag": None,
        "volume": "medium",
        "db": 0,
        "pause": 560,
        "sentence": 270,
        "energy": "bright",
        "contour": "falling",
        "noise": 0.35,
        "emphasis": None,
        "note": (
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; "
            "intensite=2; destinataire=enfant; sous_texte=la_phrase_trouve_sa_place; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    },
    "ending": {
        "rate": "slow",
        "wpm": 118,
        "speed": 0.85,
        "piper": 1.28,
        "pitch": "low",
        "pitchSsml": "-2st",
        "pitchTag": "low-pitch",
        "volume": "soft",
        "db": -3,
        "pause": 900,
        "sentence": 340,
        "energy": "calm",
        "contour": "falling",
        "noise": 0.31,
        "emphasis": "coussin",
        "note": (
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=la_parole_a_trouvé_sa_place; tempo=posé; "
            "sourire=léger; respiration=ample"
        ),
    },
}


def wc(s: str) -> int:
    return len(s.replace("'", " ").replace("’", " ").replace("-", " ").split())


def pack(lines: list[tuple[str, str]]) -> tuple[str, str]:
    script = "\n".join(f"{role}|{phrase}" for role, phrase in lines)
    text = " ".join(phrase for _, phrase in lines)
    return text, script


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp:
        e = esc(emp)
        if e.lower() in body.lower():
            body = re.sub(re.escape(e), f'<emphasis level="moderate">{e}</emphasis>', body, count=1, flags=re.I)
    return f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitchSsml"]}">{body}</prosody><break time="{m["pause"]}ms"/></speak>'


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
    pause = ""
    if m["pause"] >= 800:
        pause = "[long-pause]"
    elif m["pause"] >= 400:
        pause = "[pause]"
    return f"{body} {pause}".strip()


def check_lines(cid: str, lines: list[tuple[str, str]]) -> None:
    for role, phrase in lines:
        if "|" in phrase:
            raise SystemExit(f"{cid} pipe: {phrase}")
        n = wc(phrase)
        if n > MAX_W:
            raise SystemExit(f"{cid} {n}>{MAX_W}: {phrase}")
        if n == 0:
            raise SystemExit(f"{cid} vide")
        if not phrase.endswith((".", "?", "!")):
            raise SystemExit(f"{cid} punct: {phrase}")
        if phrase.count(".") + phrase.count("?") + phrase.count("!") > 1:
            raise SystemExit(f"{cid} multi: {phrase}")


def apply_chunk(src: dict, lines: list[tuple[str, str]], profile: str, sons: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    check_lines(src["chunk_id"], lines)
    m = dict(PROFILES[profile])
    if extra.get("emphasis") is not None:
        m["emphasis"] = extra["emphasis"]
    text, script = pack(lines)
    out = deepcopy(src)
    out["text"] = text
    out["script"] = script
    out["sons"] = "" if sons is None else sons
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
    out["emphasis_words"] = m["emphasis"] or ""
    out["pause_before_ms"] = extra.get("pauseBefore", 0)
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
    out["notes"] = extra.get("note", m["note"])
    out["night_policy"] = extra.get("night_policy", "play")
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    for k, v in (extra.get("fields") or {}).items():
        out[k] = v
    return out


OPENING = [
    ("narrateur", "Au bout de la rue mouillée, une petite maison fume."),
    ("narrateur", "Les gouttières laissent tomber des perles."),
    ("narrateur", "Nina vit là, avec papa et maman."),
    ("narrateur", "Ça sent le cacao, près de la cuisine."),
    ("narrateur", "Une chaussette pend au bras du fauteuil."),
    ("narrateur", "La lampe fait un rond jaune sur le tapis."),
    ("narrateur", "Le cartable de Nina s'appuie contre la table."),
    ("narrateur", "Il sent le crayon et le papier humide."),
    ("narrateur", "Le coussin du canapé reste tiède."),
    ("narrateur", "Nina s'y est assise en rentrant."),
    ("papa", "Le cacao est prêt, Nina."),
    ("maman", "Où est l'autre botte ?"),
    ("narrateur", "En ce moment, Nina presse la paume sur le coussin."),
    ("enfant-f", "Je veux aller au parc, tout de suite."),
    ("enfant-f", "Sarah m'attend près du bac."),
    ("narrateur", "Son ventre se noue, sous le gilet."),
    ("enfant-f", "Sarah a parlé trop près, à l'école."),
    ("narrateur", "Nina ouvre la bouche pendant que papa verse."),
    ("enfant-f", "Sarah a dit que le seau jaune."),
    ("papa", "La botte, maman, sous le banc ?"),
    ("narrateur", "Les mots de Nina se cognent aux leurs."),
    ("maman", "Tu disais quelque chose ?"),
    ("enfant-f", "Sarah, elle voulait."),
    ("narrateur", "La vapeur du cacao cache sa phrase."),
    ("papa", "On t'écoute dehors, d'accord ?"),
    ("maman", "Le parc est tout près."),
    ("enfant-f", "On y va."),
    ("narrateur", "Nina enfile la botte froide."),
    ("narrateur", "Derrière elle, le coussin garde sa place chaude."),
]

T1 = {
    "P0001": [
        ("narrateur", "Nina court vers le bac à sable."),
        ("narrateur", "Le sable est froid, un peu gris."),
        ("copine", "La pelle rouge est à moi."),
        ("narrateur", "Sarah creuse, le dos rond."),
        ("enfant-f", "Je la veux, Sarah !"),
        ("narrateur", "Nina parle trop fort, trop vite."),
        ("narrateur", "Sarah hausse les épaules, sans se tourner."),
        ("papa", "Le banc est mouillé, maman."),
        ("narrateur", "Les mots de Nina glissent sur le sable."),
        ("enfant-f", "Sarah a dit ça, à l'école."),
        ("copine", "Je n'écoute pas."),
        ("narrateur", "Un grain colle au doigt de Nina."),
        ("maman", "Tu voulais dire quelque chose ?"),
        ("enfant-f", "Plus tard."),
        ("narrateur", "Le ventre de Nina se noue plus fort."),
    ],
    "P0002": [
        ("narrateur", "Nina rejoint le toboggan."),
        ("narrateur", "Le métal luisant est froid sous la paume."),
        ("narrateur", "Une feuille mouillée colle en haut."),
        ("narrateur", "Sarah occupe les marches étroites."),
        ("enfant-f", "Moi d'abord, Sarah !"),
        ("narrateur", "Sarah ne baisse pas les yeux."),
        ("copine", "J'y suis."),
        ("enfant-f", "Sarah a parlé trop près, ce matin."),
        ("narrateur", "Nina gravit deux marches, trop vite."),
        ("narrateur", "Sa phrase se heurte aux chaussures de Sarah."),
        ("copine", "Attends."),
        ("maman", "Le métal glisse, Nina."),
        ("papa", "Tu voulais nous dire quoi ?"),
        ("enfant-f", "Pas là."),
        ("narrateur", "Les deux filles restent coincées, au milieu."),
    ],
    "P0003": [
        ("narrateur", "Nina va vers les balançoires."),
        ("narrateur", "Une seule assise a séché."),
        ("narrateur", "C'est la balançoire jaune."),
        ("narrateur", "Sarah pose la main sur la chaîne."),
        ("enfant-f", "Elle est à moi !"),
        ("narrateur", "Nina saisit l'autre chaîne."),
        ("narrateur", "Le siège se tord entre elles."),
        ("copine", "Je l'ai vue avant."),
        ("enfant-f", "À l'école tu as parlé trop près."),
        ("papa", "La chaîne fait tic."),
        ("maman", "Vous tirez toutes les deux ?"),
        ("narrateur", "Personne n'entend la phrase entière."),
        ("enfant-f", "Mon ventre fait mal."),
        ("narrateur", "Nina lâche un peu la chaîne."),
    ],
}

Q = {
    "P0001": {
        "lines": [
            ("narrateur", "Dans le bac, une fille tenait la pelle."),
            ("maman", "Qui tenait la petite pelle rouge ?"),
        ],
        "expected": "sarah",
        "accepted": "sarah | copine | la copine",
        "ok": "Oui, c'est Sarah.",
        "emphasis": "pelle",
    },
    "P0002": {
        "lines": [
            ("narrateur", "Sur le toboggan, quelqu'un bloquait les marches."),
            ("papa", "Qui occupait les marches ?"),
        ],
        "expected": "sarah",
        "accepted": "sarah | copine | la copine",
        "ok": "Oui, c'est Sarah.",
        "emphasis": "marches",
    },
    "P0003": {
        "lines": [
            ("narrateur", "Une balançoire a séché plus que les autres."),
            ("maman", "Quelle balançoire a séché ?"),
        ],
        "expected": "jaune",
        "accepted": "jaune | la jaune | balançoire jaune",
        "ok": "Oui, la jaune.",
        "emphasis": "balançoire",
    },
}

C = {
    "P0001": [
        ("enfant-f", "Sarah."),
        ("narrateur", "Oui, Sarah tenait la pelle."),
        ("narrateur", "Nina ferme un instant la bouche."),
        ("papa", "On peut chercher une autre manière."),
        ("maman", "Tu pourras nous le dire, plus tard."),
        ("narrateur", "Le grain de sable brille sur son doigt."),
    ],
    "P0002": [
        ("enfant-f", "Sarah."),
        ("narrateur", "Oui, Sarah était sur les marches."),
        ("narrateur", "Nina redescend d'une marche."),
        ("maman", "Il y a de la place, après."),
        ("papa", "On attend que le chemin se libère."),
        ("narrateur", "La feuille mouillée tremble en haut."),
    ],
    "P0003": [
        ("enfant-f", "La jaune."),
        ("narrateur", "Oui, la balançoire jaune a séché."),
        ("narrateur", "Nina relâche un peu plus la chaîne."),
        ("papa", "Deux mains, c'est trop pour un siège."),
        ("maman", "On va trouver une autre idée."),
        ("narrateur", "Le tic de la chaîne ralentit."),
    ],
}

T2 = {
    ("P0001", "P0001"): [  # sable + ballon
        ("narrateur", "Nina prend le ballon un peu sablé."),
        ("narrateur", "Elle le lance trop fort vers Sarah."),
        ("narrateur", "Le ballon s'enterre, puis s'arrête."),
        ("copine", "Oh !"),
        ("enfant-f", "Pardon."),
        ("narrateur", "Nina le ramasse, les joues chaudes."),
        ("enfant-f", "On le fait rouler, doucement ?"),
        ("narrateur", "Sarah pose la pelle un instant."),
        ("narrateur", "Le ballon va, puis revient."),
        ("papa", "Vous vous êtes parlé, là ?"),
        ("enfant-f", "Un peu."),
        ("maman", "Et le seau jaune, tu voulais dire ?"),
        ("enfant-f", "Pas maintenant."),
        ("narrateur", "Nina tient le ballon contre son ventre."),
    ],
    ("P0001", "P0002"): [  # sable + seau
        ("narrateur", "Nina pose le seau jaune dans le bac."),
        ("narrateur", "Elle le renverse, trop vite."),
        ("narrateur", "Le sable vole vers les genoux de Sarah."),
        ("copine", "Mes yeux !"),
        ("enfant-f", "Je voulais te le montrer."),
        ("narrateur", "Nina ramasse le seau, gênée."),
        ("enfant-f", "Tu peux mettre un peu de sable ?"),
        ("narrateur", "Sarah hésite, puis verse une pelletée."),
        ("papa", "Le seau a assez de place pour deux ?"),
        ("copine", "Peut-être."),
        ("maman", "Nina, tu avais une phrase, au salon."),
        ("enfant-f", "Elle attend."),
        ("narrateur", "Le seau jaune sonne, un peu creux."),
    ],
    ("P0001", "P0003"): [  # sable + doudou
        ("narrateur", "Nina sort le doudou de sa poche."),
        ("narrateur", "Une oreille est tiède, comme le coussin."),
        ("enfant-f", "Doudou, Sarah a pris la pelle."),
        ("narrateur", "Elle le dit trop fort."),
        ("copine", "J'ai entendu."),
        ("narrateur", "Sarah fronce le nez."),
        ("enfant-f", "Je le disais au doudou."),
        ("maman", "Tu peux le dire plus bas, à Sarah ?"),
        ("enfant-f", "Sarah, je voulais creuser avec toi."),
        ("copine", "Tu criais."),
        ("papa", "Et à l'école, qu'est-ce qui s'est passé ?"),
        ("enfant-f", "Je le dirai au doudou d'abord."),
        ("narrateur", "Nina colle l'oreille tiède contre sa joue."),
    ],
    ("P0002", "P0001"): [  # tobo + ballon
        ("narrateur", "Nina pose le ballon en haut du toboggan."),
        ("narrateur", "Il file tout seul, sans elle."),
        ("narrateur", "Il rebondit dans l'herbe mouillée."),
        ("copine", "Il est parti !"),
        ("enfant-f", "Ce n'était pas le plan."),
        ("narrateur", "Nina redescend, les mains vides."),
        ("enfant-f", "On l'envoie, chacun notre tour ?"),
        ("narrateur", "Sarah laisse une marche libre."),
        ("papa", "Un tour pour Sarah, un tour pour Nina ?"),
        ("copine", "D'accord."),
        ("maman", "Nina, ta phrase du cacao, elle vient ?"),
        ("enfant-f", "Après le ballon."),
        ("narrateur", "Le ballon luit, plein de gouttes."),
    ],
    ("P0002", "P0002"): [  # tobo + seau
        ("narrateur", "Nina veut glisser avec le seau jaune."),
        ("narrateur", "Le seau accroche la feuille du haut."),
        ("narrateur", "Tout s'arrête, au milieu du métal."),
        ("enfant-f", "Je suis coincée !"),
        ("papa", "J'arrive, je soulève le seau."),
        ("narrateur", "Sarah attend sur la marche du bas."),
        ("enfant-f", "Tu peux passer, Sarah."),
        ("copine", "Merci."),
        ("narrateur", "Sarah glisse, et Nina reste un moment."),
        ("maman", "Tu as laissé le chemin."),
        ("papa", "Et le nœud, dans ton ventre ?"),
        ("enfant-f", "Il est là."),
        ("narrateur", "Le seau pend, vide, à sa main."),
    ],
    ("P0002", "P0003"): [  # tobo + doudou
        ("narrateur", "Nina installe le doudou sur la première marche."),
        ("narrateur", "Il reste mou, sans glisser."),
        ("enfant-f", "Toi d'abord, doudou."),
        ("copine", "Il ne bouge pas."),
        ("narrateur", "Sarah est toujours au milieu."),
        ("enfant-f", "Quand tu as fini, je monte ?"),
        ("copine", "Un moment."),
        ("narrateur", "Nina attend, le doudou contre elle."),
        ("papa", "Tu as demandé, cette fois."),
        ("maman", "C'est plus clair que tout à l'heure."),
        ("enfant-f", "Au salon, vous n'entendiez pas."),
        ("papa", "On entend, maintenant."),
        ("narrateur", "L'oreille du doudou reste tiède."),
    ],
    ("P0003", "P0001"): [  # bal + ballon
        ("narrateur", "Nina tient le ballon et la chaîne."),
        ("narrateur", "Elle ne peut pas garder les deux."),
        ("narrateur", "Le ballon tombe dans une flaque."),
        ("copine", "Il est tout mouillé."),
        ("enfant-f", "Tu le gardes, le temps que je parle ?"),
        ("narrateur", "Sarah ramasse le ballon, surprise."),
        ("papa", "Tu lui as demandé, Nina."),
        ("copine", "Je le tiens."),
        ("enfant-f", "À l'école, tu as parlé trop près."),
        ("copine", "La maîtresse parlait."),
        ("maman", "Vous vous écoutez, là."),
        ("enfant-f", "Un peu."),
        ("narrateur", "La flaque tremble autour du ballon."),
    ],
    ("P0003", "P0002"): [  # bal + seau
        ("narrateur", "Nina pose le seau jaune sur le siège jaune."),
        ("narrateur", "C'est pour le garder, tout pour elle."),
        ("copine", "C'est pas juste !"),
        ("narrateur", "Sarah tire la chaîne, fâchée."),
        ("enfant-f", "Attends."),
        ("narrateur", "Nina retire le seau, les oreilles chaudes."),
        ("enfant-f", "Le siège est pour toi."),
        ("copine", "Et toi ?"),
        ("enfant-f", "Je prends l'autre, même mouillée."),
        ("papa", "Tu as changé d'idée, là."),
        ("maman", "Le seau jaune, c'était ça, au salon ?"),
        ("enfant-f", "Une partie."),
        ("narrateur", "Le seau pend entre les deux balançoires."),
    ],
    ("P0003", "P0003"): [  # bal + doudou
        ("narrateur", "Nina assied le doudou sur la balançoire jaune."),
        ("copine", "Je veux m'asseoir, pas lui."),
        ("enfant-f", "Il garde ma place."),
        ("narrateur", "Sarah croise les bras."),
        ("enfant-f", "Bon, il vient sur mes genoux."),
        ("narrateur", "Nina passe sur la balançoire humide."),
        ("narrateur", "Elle laisse la jaune à Sarah."),
        ("copine", "Merci."),
        ("papa", "Le doudou a les oreilles tièdes ?"),
        ("enfant-f", "Comme le coussin, à la maison."),
        ("maman", "Tu nous diras, sur le coussin ?"),
        ("enfant-f", "Oui."),
        ("narrateur", "Les deux balançoires avancent, pas ensemble."),
    ],
}

# T3: ours / lapin / chat — 27 scènes distinctes
T3 = {}

T3["P0001", "P0001", "P0001"] = [  # sable ballon ours
    ("narrateur", "Nina pose l'ours brun entre elle et Sarah."),
    ("enfant-f", "L'ours écoute en premier."),
    ("narrateur", "Elle fait rouler le ballon vers l'ours."),
    ("narrateur", "Puis vers Sarah, sans crier."),
    ("copine", "À moi."),
    ("enfant-f", "Après, c'est mon tour de parler."),
    ("narrateur", "Sarah pousse le ballon, et Nina attend."),
    ("enfant-f", "À l'école, tu as parlé trop près."),
    ("copine", "J'avais peur de perdre le seau."),
    ("papa", "Je prends la suite, si tu veux."),
    ("enfant-f", "Oui, dis-lui, papa."),
    ("maman", "On a toute la phrase, cette fois."),
    ("narrateur", "L'ours a du sable sur le ventre."),
]
T3["P0001", "P0001", "P0002"] = [  # sable ballon lapin
    ("narrateur", "Nina sort le lapin gris, oreilles chaudes."),
    ("enfant-f", "J'attends que Sarah finisse son trou."),
    ("narrateur", "Elle caresse l'oreille, sans parler."),
    ("narrateur", "Le ballon reste calme entre ses pieds."),
    ("copine", "C'est fini."),
    ("enfant-f", "Sarah, tu as parlé trop près, ce matin."),
    ("copine", "La maîtresse n'aimait pas."),
    ("papa", "Tu l'as dit quand c'était ton tour."),
    ("maman", "On t'écoute jusqu'au bout."),
    ("enfant-f", "Mon ventre se desserre."),
    ("narrateur", "Le lapin a un grain de sable à l'oreille."),
    ("papa", "On ramasse le ballon, et on rentre ?"),
    ("narrateur", "Nina hoche la tête, enfin légère."),
]
T3["P0001", "P0001", "P0003"] = [  # sable ballon chat
    ("narrateur", "Nina emmène le chat rayé vers le banc."),
    ("narrateur", "Elle s'assoit sur le manteau de maman."),
    ("enfant-f", "Le manteau est tiède, comme le coussin."),
    ("maman", "On t'écoute, qu'est-ce qui s'est passé ?"),
    ("enfant-f", "Sarah a parlé trop près, à l'école."),
    ("papa", "Pendant que la maîtresse parlait ?"),
    ("enfant-f", "Oui, mon ventre s'est noué."),
    ("maman", "Merci, Nina, j'ai toute la phrase."),
    ("narrateur", "Ils reviennent vers le bac."),
    ("papa", "Sarah, Nina a quelque chose à te dire."),
    ("enfant-f", "On peut partager le ballon."),
    ("copine", "D'accord."),
    ("narrateur", "Le chat rayé garde une miette de sable."),
]
T3["P0001", "P0002", "P0001"] = [  # sable seau ours
    ("narrateur", "Nina pose l'ours brun près du seau jaune."),
    ("enfant-f", "L'ours a le seau en premier."),
    ("narrateur", "Sarah pose la pelle à côté, surprise."),
    ("copine", "Pourquoi lui ?"),
    ("enfant-f", "Pour ne pas crier, comme tout à l'heure."),
    ("narrateur", "Nina verse un peu de sable, puis s'arrête."),
    ("enfant-f", "Ton tour, Sarah."),
    ("copine", "Et après on parle ?"),
    ("enfant-f", "À l'école, tu as parlé trop près."),
    ("papa", "Le seau a entendu les deux."),
    ("maman", "Nous aussi, maintenant."),
    ("narrateur", "L'ours a le museau poudreux."),
    ("enfant-f", "On peut rentrer, j'ai dit."),
]
T3["P0001", "P0002", "P0002"] = [  # sable seau lapin
    ("narrateur", "Nina tient le lapin gris contre le seau."),
    ("enfant-f", "Je compte jusqu'à trois, sans parler."),
    ("narrateur", "Sarah finit sa pelletée."),
    ("enfant-f", "Un, deux, trois."),
    ("enfant-f", "Sarah, le seau jaune n'est pas qu'à toi."),
    ("copine", "Je le sais."),
    ("papa", "Vous l'avez dit sans vous crier dessus."),
    ("maman", "Au salon, la phrase s'était perdue."),
    ("enfant-f", "Là, elle est arrivée."),
    ("narrateur", "Le lapin a les pattes sablées."),
    ("papa", "On rince le seau, puis les mains ?"),
    ("copine", "Oui."),
    ("narrateur", "Nina souffle, et le nœud lâche."),
]
T3["P0001", "P0002", "P0003"] = [  # sable seau chat
    ("narrateur", "Nina prend le chat rayé et le seau."),
    ("narrateur", "Elle rejoint papa, près de la haie."),
    ("enfant-f", "Papa, Sarah a parlé trop près."),
    ("papa", "Je t'écoute, et maman aussi."),
    ("enfant-f", "Elle a dit que le seau était à elle."),
    ("maman", "Toi, tu étais dans la classe."),
    ("enfant-f", "Oui, après, mon ventre s'est serré."),
    ("papa", "Merci de nous le dire, ici."),
    ("narrateur", "Ils retournent vers Sarah."),
    ("maman", "Le seau peut servir à deux."),
    ("copine", "On essaie."),
    ("narrateur", "Le chat rayé a une griffe de sable."),
    ("enfant-f", "Je suis prête à rentrer."),
]
T3["P0001", "P0003", "P0001"] = [  # sable doudou ours
    ("narrateur", "Nina met l'ours brun à côté du doudou."),
    ("enfant-f", "Vous deux, vous écoutez."),
    ("narrateur", "Elle parle bas, vers les peluches."),
    ("enfant-f", "Sarah a parlé trop près, à l'école."),
    ("narrateur", "Sarah se penche, pour entendre."),
    ("copine", "Je ne voulais pas faire mal."),
    ("papa", "Nina l'a dit aux peluches, puis à toi."),
    ("maman", "C'est plus doux que le cri de tout à l'heure."),
    ("enfant-f", "Mon doudou a l'oreille chaude."),
    ("copine", "Comme un petit coussin."),
    ("narrateur", "Nina sourit, surprise."),
    ("papa", "On rentre vers le vrai coussin ?"),
    ("narrateur", "Le sable reste sous les genoux."),
]
T3["P0001", "P0003", "P0002"] = [  # sable doudou lapin
    ("narrateur", "Nina attend, le lapin gris sur les genoux."),
    ("narrateur", "Le doudou est contre l'autre oreille."),
    ("enfant-f", "Quand Sarah lève la tête, je parle."),
    ("narrateur", "Sarah lève la tête."),
    ("enfant-f", "Ce matin, tu as parlé trop près."),
    ("copine", "Pardon."),
    ("maman", "Vous vous êtes dit les mots, jusqu'au bout."),
    ("papa", "Au salon, on avait trop de bruit."),
    ("enfant-f", "Là, j'ai eu le temps."),
    ("narrateur", "Deux oreilles tièdes encadrent Nina."),
    ("copine", "On se revoit ?"),
    ("enfant-f", "Oui, avec le seau, si tu veux."),
    ("narrateur", "Nina se lève, plus légère."),
]
T3["P0001", "P0003", "P0003"] = [  # sable doudou chat
    ("narrateur", "Nina porte le chat et le doudou au banc."),
    ("enfant-f", "Maman, je m'assois sur ton manteau."),
    ("maman", "Il est chaud, comme à la maison."),
    ("enfant-f", "Sarah a parlé trop près, à l'école."),
    ("papa", "Tu as gardé ça dans le ventre."),
    ("enfant-f", "Oui, au salon, vous versiez le cacao."),
    ("maman", "Merci, on a le temps, là."),
    ("narrateur", "Nina retourne au bac, les peluches sous le bras."),
    ("enfant-f", "Sarah, je te l'ai dit à maman."),
    ("copine", "D'accord, on creuse moins fort ?"),
    ("papa", "Moins fort, c'est bien."),
    ("narrateur", "Le doudou a du sable dans une couture."),
    ("enfant-f", "On rentre, le coussin m'attend."),
]
T3["P0002", "P0001", "P0001"] = [  # tobo ballon ours
    ("narrateur", "Nina installe l'ours brun en bas du toboggan."),
    ("enfant-f", "L'ours reçoit le ballon en premier."),
    ("narrateur", "Sarah envoie le ballon, et l'ours le reçoit."),
    ("enfant-f", "Mon tour de parler."),
    ("enfant-f", "À l'école, tu as parlé trop près."),
    ("copine", "Je voulais le seau jaune."),
    ("papa", "Vous avez fait un tour chacun."),
    ("maman", "La phrase a glissé, elle aussi."),
    ("narrateur", "Nina reprend le ballon contre l'ours."),
    ("enfant-f", "Je n'ai plus mal au ventre."),
    ("papa", "On rentre avant la nuit ?"),
    ("copine", "Salut, Nina."),
    ("narrateur", "Une goutte quitte le métal, puis plus."),
]
T3["P0002", "P0001", "P0002"] = [  # tobo ballon lapin
    ("narrateur", "Nina s'assoit en bas, le lapin gris sur les genoux."),
    ("enfant-f", "Je reste là jusqu'à ce que Sarah arrive."),
    ("narrateur", "Sarah glisse, et le ballon l'attend dans l'herbe."),
    ("copine", "Il est à nous deux ?"),
    ("enfant-f", "Oui, et moi, j'ai une phrase."),
    ("enfant-f", "Tu as parlé trop près, ce matin."),
    ("copine", "La maîtresse m'a regardée."),
    ("maman", "Nina te le dit après ta descente."),
    ("papa", "C'est plus simple que de crier en haut."),
    ("enfant-f", "Mon lapin a attendu avec moi."),
    ("narrateur", "L'oreille du lapin est tiède, contre le gilet."),
    ("papa", "On reprend le ballon, et la route."),
    ("narrateur", "Le toboggan reste vide, luisant."),
]
T3["P0002", "P0001", "P0003"] = [  # tobo ballon chat
    ("narrateur", "Nina descend avec le chat rayé sous le bras."),
    ("narrateur", "Elle rejoint le banc des parents."),
    ("enfant-f", "Le ballon reste en bas, pour Sarah."),
    ("maman", "Qu'est-ce que tu n'as pas pu dire ?"),
    ("enfant-f", "Sarah a parlé trop près, à l'école."),
    ("papa", "Pendant la classe."),
    ("enfant-f", "Oui, j'étais dans la classe, puis ça."),
    ("maman", "Merci, on tient la phrase, maintenant."),
    ("narrateur", "Sarah arrive, le ballon contre elle."),
    ("papa", "Nina t'a attendue en bas."),
    ("copine", "On se dit au revoir ?"),
    ("enfant-f", "Au revoir, Sarah."),
    ("narrateur", "Le chat rayé a une goutte sur le dos."),
]
T3["P0002", "P0002", "P0001"] = [  # tobo seau ours
    ("narrateur", "Nina pose l'ours brun dans le seau jaune."),
    ("enfant-f", "Toi, tu glisses avec moi, sans bousculer."),
    ("narrateur", "Sarah laisse la rampe."),
    ("narrateur", "Nina glisse, l'ours au fond du seau."),
    ("copine", "Il n'a pas crié."),
    ("enfant-f", "Moi non plus, cette fois."),
    ("enfant-f", "Sarah, à l'école tu as parlé trop près."),
    ("papa", "La phrase est arrivée en bas, entière."),
    ("maman", "Au salon, elle s'était cassée."),
    ("copine", "Pardon."),
    ("enfant-f", "Le seau est à nous deux."),
    ("narrateur", "L'ours a le museau un peu humide."),
    ("papa", "On rentre, le cacao attend."),
]
T3["P0002", "P0002", "P0002"] = [  # tobo seau lapin
    ("narrateur", "Nina compte, le lapin gris dans le seau."),
    ("enfant-f", "Un, deux, trois, Sarah, tu glisses."),
    ("narrateur", "Sarah glisse, et Nina ne parle pas pendant ce temps."),
    ("copine", "À toi."),
    ("enfant-f", "À l'école, tu as parlé trop près."),
    ("copine", "J'avais peur."),
    ("maman", "Vous avez attendu, chacune."),
    ("papa", "Le seau a servi de place d'attente."),
    ("enfant-f", "Comme le coussin, mais dehors."),
    ("narrateur", "Le lapin a une feuille collée à l'oreille."),
    ("papa", "On l'enlève, puis on rentre ?"),
    ("copine", "Salut."),
    ("narrateur", "Nina sourit vers les marches vides."),
]
T3["P0002", "P0002", "P0003"] = [  # tobo seau chat
    ("narrateur", "Nina pose le seau aux pieds de maman."),
    ("narrateur", "Le chat rayé s'assoit dans le seau, comique."),
    ("enfant-f", "Je raconte, là."),
    ("maman", "On t'écoute, le métal peut attendre."),
    ("enfant-f", "Sarah a parlé trop près, à l'école."),
    ("papa", "Tu as voulu le dire au cacao, trop tôt."),
    ("enfant-f", "Oui, les mots se sont cognés."),
    ("maman", "Merci, ils sont posés, maintenant."),
    ("narrateur", "Sarah s'approche du banc."),
    ("papa", "Nina t'a laissée glisser, avant."),
    ("copine", "On partage le seau, demain ?"),
    ("enfant-f", "Demain."),
    ("narrateur", "Le chat rayé a le seau pour trône."),
]
T3["P0002", "P0003", "P0001"] = [  # tobo doudou ours
    ("narrateur", "Nina met l'ours et le doudou sur la dernière marche."),
    ("enfant-f", "Ils écoutent, après, c'est Sarah."),
    ("narrateur", "Sarah s'assoit un peu plus haut, sans bousculer."),
    ("enfant-f", "À l'école, tu as parlé trop près."),
    ("copine", "Je ne le ferai plus."),
    ("papa", "Nina l'a dit aux peluches, puis à toi."),
    ("maman", "Les oreilles tièdes aident, on dirait."),
    ("enfant-f", "Comme le coussin, à la maison."),
    ("narrateur", "Nina descend, les deux peluches contre elle."),
    ("copine", "Je glisse après."),
    ("papa", "Chacun son tour, ça tient."),
    ("narrateur", "Le métal sonne moins fort."),
    ("enfant-f", "On peut rentrer."),
]
T3["P0002", "P0003", "P0002"] = [  # tobo doudou lapin
    ("narrateur", "Nina attend en bas, doudou et lapin croisés."),
    ("narrateur", "Sarah arrive au bout de la glissade."),
    ("enfant-f", "J'ai attendu la fin."),
    ("enfant-f", "Ce matin, tu as parlé trop près."),
    ("copine", "La maîtresse parlait des seaux."),
    ("papa", "Nina a écouté ça, puis toi."),
    ("maman", "Elle nous le dit, là, entière."),
    ("enfant-f", "Mon ventre est plus large."),
    ("narrateur", "Deux peluches tièdes pèsent contre son manteau."),
    ("copine", "Au revoir."),
    ("papa", "Au revoir, Sarah."),
    ("narrateur", "Une feuille quitte enfin le haut du toboggan."),
    ("enfant-f", "Le coussin, maintenant."),
]
T3["P0002", "P0003", "P0003"] = [  # tobo doudou chat
    ("narrateur", "Nina rejoint le banc, doudou et chat contre elle."),
    ("enfant-f", "Je m'assois sur le manteau."),
    ("maman", "Il a pris le soleil, un peu."),
    ("enfant-f", "Sarah a parlé trop près, à l'école."),
    ("papa", "Tu as voulu le crier sur les marches."),
    ("enfant-f", "Ça n'allait pas."),
    ("maman", "Merci de le poser ici."),
    ("narrateur", "Sarah glisse, seule, sans être bousculée."),
    ("papa", "Tu l'as laissée finir."),
    ("copine", "Merci, Nina."),
    ("enfant-f", "On se voit."),
    ("narrateur", "Le doudou a une oreille plus chaude que l'autre."),
    ("enfant-f", "Comme le coussin du canapé."),
]
T3["P0003", "P0001", "P0001"] = [  # bal ballon ours
    ("narrateur", "Nina pose l'ours brun sur la balançoire d'à côté."),
    ("enfant-f", "L'ours se balance, et nous, on parle."),
    ("narrateur", "Sarah garde la jaune, le ballon sur les genoux."),
    ("enfant-f", "À l'école, tu as parlé trop près."),
    ("copine", "J'étais trop pressée."),
    ("papa", "Le ballon a voyagé entre vous."),
    ("maman", "La phrase aussi, maintenant."),
    ("enfant-f", "Je n'ai plus besoin de tirer la chaîne."),
    ("narrateur", "L'ours avance, tout seul, un peu."),
    ("copine", "Il a le vertige."),
    ("papa", "On arrête les sièges, et on rentre ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "La chaîne fait un dernier tic."),
]
T3["P0003", "P0001", "P0002"] = [  # bal ballon lapin
    ("narrateur", "Nina se balance moins vite, le lapin gris contre elle."),
    ("enfant-f", "J'attends que ta balançoire s'arrête."),
    ("narrateur", "Sarah pose les pieds par terre."),
    ("enfant-f", "Sarah, tu as parlé trop près, ce matin."),
    ("copine", "Pardon, j'ai le ballon, si tu veux."),
    ("papa", "Elle te le tend, sans tirer."),
    ("maman", "Au salon, on n'avait pas entendu ça."),
    ("enfant-f", "Là, oui."),
    ("narrateur", "Le lapin a l'oreille collée au gilet."),
    ("copine", "On se revoit au bac ?"),
    ("enfant-f", "Oui, avec le seau."),
    ("papa", "On range le ballon mouillé."),
    ("narrateur", "Les deux sièges pendent, enfin calmes."),
]
T3["P0003", "P0001", "P0003"] = [  # bal ballon chat
    ("narrateur", "Nina descend, le chat rayé sous un bras."),
    ("narrateur", "Le ballon sous l'autre."),
    ("enfant-f", "Je vais au banc."),
    ("maman", "Assieds-toi, on t'écoute."),
    ("enfant-f", "Sarah a parlé trop près, à l'école."),
    ("papa", "Tu as voulu le crier à la chaîne."),
    ("enfant-f", "La chaîne faisait trop de bruit."),
    ("maman", "Merci, ta phrase est posée."),
    ("narrateur", "Sarah reste sur la jaune, sans tirer."),
    ("papa", "Nina t'a laissé le siège sec."),
    ("copine", "Merci."),
    ("enfant-f", "On rentre ?"),
    ("narrateur", "Le chat rayé a une tache d'eau sur la patte."),
]
T3["P0003", "P0002", "P0001"] = [  # bal seau ours
    ("narrateur", "Nina pose l'ours brun dans le seau, entre les sièges."),
    ("enfant-f", "L'ours garde le seau, personne ne le prend."),
    ("copine", "Alors on se balance, juste."),
    ("enfant-f", "À l'école, tu as parlé trop près."),
    ("copine", "Pour le seau."),
    ("papa", "Vous l'avez mis au milieu, maintenant."),
    ("maman", "Plus besoin de le cacher sur le siège."),
    ("enfant-f", "Mon ventre est moins dur."),
    ("narrateur", "L'ours penche un peu, dans le seau."),
    ("copine", "Il va tomber."),
    ("enfant-f", "Je le tiens."),
    ("papa", "On rentre avec le seau ?"),
    ("narrateur", "Les chaînes se taisent ensemble."),
]
T3["P0003", "P0002", "P0002"] = [  # bal seau lapin
    ("narrateur", "Nina pose le seau, le lapin gris dessus comme un couvercle."),
    ("enfant-f", "Quand Sarah a fini de se balancer, je parle."),
    ("narrateur", "Sarah s'arrête, et le siège jaune ne bouge plus."),
    ("enfant-f", "Tu as parlé trop près, à l'école."),
    ("copine", "Je voulais le seau trop fort."),
    ("maman", "Vous l'avez dit sans vous couper."),
    ("papa", "Au cacao, on s'était coupés, nous."),
    ("enfant-f", "Moi aussi, j'ai crié."),
    ("narrateur", "Le lapin a une oreille dans le seau."),
    ("copine", "Il écoute au fond."),
    ("papa", "On le sort, et on rentre."),
    ("enfant-f", "Oui."),
    ("narrateur", "Nina sent le nœud se défaire."),
]
T3["P0003", "P0002", "P0003"] = [  # bal seau chat
    ("narrateur", "Nina apporte le seau et le chat au banc."),
    ("enfant-f", "Je m'assois sur le manteau de maman."),
    ("maman", "Raconte, le parc peut attendre."),
    ("enfant-f", "Sarah a parlé trop près, à l'école."),
    ("papa", "Le seau jaune était au milieu."),
    ("enfant-f", "Oui, j'ai voulu le dire trop vite."),
    ("maman", "Merci, on a le temps, là."),
    ("narrateur", "Sarah reste sur la jaune, le pied à terre."),
    ("papa", "Nina t'a laissé le siège."),
    ("copine", "On partage le seau, après ?"),
    ("enfant-f", "Après, d'abord le coussin."),
    ("narrateur", "Le chat rayé a la tête dans le seau."),
    ("papa", "Il cherche, lui aussi."),
]
T3["P0003", "P0003", "P0001"] = [  # bal doudou ours
    ("narrateur", "Nina met l'ours et le doudou sur ses genoux mouillés."),
    ("enfant-f", "Sarah a la jaune, et moi, je parle."),
    ("enfant-f", "À l'école, tu as parlé trop près."),
    ("copine", "Je savais pas que ça serrait ton ventre."),
    ("papa", "Maintenant, si."),
    ("maman", "Nina l'a dit aux peluches, puis à toi."),
    ("enfant-f", "Le doudou est chaud, l'ours aussi."),
    ("copine", "Comme deux petits coussins."),
    ("narrateur", "Nina rit, un peu."),
    ("papa", "On arrête les chaînes ?"),
    ("enfant-f", "Oui, on rentre."),
    ("copine", "Salut."),
    ("narrateur", "Une goutte quitte la chaîne, puis plus rien."),
]
T3["P0003", "P0003", "P0002"] = [  # bal doudou lapin
    ("narrateur", "Nina attend que Sarah pose les pieds."),
    ("narrateur", "Le lapin gris et le doudou sont ses deux oreilles."),
    ("enfant-f", "C'est bon, j'ai une phrase."),
    ("enfant-f", "Tu as parlé trop près, ce matin."),
    ("copine", "Pardon, Nina."),
    ("maman", "Vous vous êtes laissé le temps."),
    ("papa", "Au salon, le cacao allait trop vite."),
    ("enfant-f", "Là, les balançoires ont ralenti."),
    ("narrateur", "Nina pose le menton sur le doudou."),
    ("copine", "On se revoit."),
    ("enfant-f", "Oui."),
    ("papa", "Les sièges peuvent dormir."),
    ("narrateur", "Nina descend, plus légère que la chaîne."),
]
T3["P0003", "P0003", "P0003"] = [  # bal doudou chat
    ("narrateur", "Nina rejoint le banc, doudou et chat contre le manteau."),
    ("enfant-f", "C'est tiède, comme à la maison."),
    ("maman", "On t'écoute, Nina."),
    ("enfant-f", "Sarah a parlé trop près, à l'école."),
    ("papa", "Tu as voulu garder la balançoire trop fort."),
    ("enfant-f", "Oui, ça n'a pas marché."),
    ("maman", "Merci d'avoir posé les mots ici."),
    ("narrateur", "Sarah se balance seule, sans tirer."),
    ("copine", "Au revoir !"),
    ("enfant-f", "Au revoir, Sarah."),
    ("papa", "Le coussin va être content."),
    ("narrateur", "Nina serre les peluches, et le nœud a lâché."),
    ("enfant-f", "On rentre."),
]

assert len(T3) == 27, len(T3)

# 27 fins : salon, coussin, détail unique
FINS = {}

def fin(
    dit: str,
    adulte: tuple[str, str],
    objet: str,
    image: str,
    merci: tuple[str, str],
    extra_papa: str,
) -> list[tuple[str, str]]:
    return [
        ("narrateur", "De retour, le salon sent le cacao."),
        ("narrateur", "Nina retrouve le coussin tiède."),
        ("enfant-f", dit),
        adulte,
        ("narrateur", objet),
        merci,
        ("papa", extra_papa),
        ("narrateur", image),
    ]


FINS["P0001", "P0001", "P0001"] = fin(
    "Sarah a parlé trop près, j'ai attendu, puis dit.",
    ("maman", "On a toute la phrase, sur le coussin."),
    "Un grain de sable brille sur le tissu tiède.",
    "Le ballon sèche près de la table, rond et sage.",
    ("papa", "Merci, Nina, l'ours a aidé, dehors."),
    "Le cacao n'a plus de vapeur entre nous.",
)
FINS["P0001", "P0001", "P0002"] = fin(
    "J'ai compté, après, Sarah m'a entendue.",
    ("papa", "Le lapin a gardé le silence, avec toi."),
    "Le ballon s'appuie contre le pied du canapé.",
    "Nina enfonce la nuque dans le coussin chaud.",
    ("maman", "Merci d'avoir attendu ton tour."),
    "Tu veux un peu de cacao, maintenant ?",
)
FINS["P0001", "P0001", "P0003"] = fin(
    "Je vous l'ai dit sur le manteau, puis à Sarah.",
    ("maman", "Le manteau était un petit coussin, dehors."),
    "Le chat rayé garde le creux du vrai coussin.",
    "La lampe jaune touche le tissu, tout bas.",
    ("papa", "Merci, on n'a rien perdu, cette fois."),
    "Le cartable sent le crayon, près de nous.",
)
FINS["P0001", "P0002", "P0001"] = fin(
    "Le seau jaune est à deux, je l'ai dit.",
    ("papa", "L'ours avait le seau, pour commencer."),
    "Une goutte du seau mouille le bord du coussin.",
    "Nina pose la joue là où c'est le plus chaud.",
    ("maman", "Merci pour le seau, et pour les mots."),
    "On laisse sécher, sans rien dire de trop.",
)
FINS["P0001", "P0002", "P0002"] = fin(
    "J'ai compté jusqu'à trois, puis parlé.",
    ("maman", "Le lapin a tenu le temps, avec toi."),
    "Le seau vide veille au pied du canapé.",
    "Nina souffle, et le coussin se creuse sous elle.",
    ("papa", "Merci, les mots sont arrivés entiers."),
    "Le sable de tes chaussettes reste à la porte.",
)
FINS["P0001", "P0002", "P0003"] = fin(
    "Je vous l'ai dit près de la haie, et Sarah a su.",
    ("papa", "Le chat a voyagé dans le seau, presque."),
    "Le coussin sent un peu le sable mouillé.",
    "Nina y glisse les poings, puis les ouvre.",
    ("maman", "Merci, on tenait le seau, et toi."),
    "Le cacao est tiède, comme le tissu.",
)
FINS["P0001", "P0003", "P0001"] = fin(
    "Les peluches ont écouté, Sarah aussi, après.",
    ("maman", "Deux oreilles dehors, et les nôtres ici."),
    "L'oreille du doudou réchauffe le coussin.",
    "L'ours brun s'endort contre le même creux.",
    ("papa", "Merci, Nina, tu as parlé bas, puis vrai."),
    "On n'a plus besoin de verser trop vite.",
)
FINS["P0001", "P0003", "P0002"] = fin(
    "Quand Sarah a levé la tête, j'ai dit.",
    ("papa", "Le lapin a attendu la bonne seconde."),
    "Le doudou et le lapin partagent le coussin.",
    "Nina rit, le nez dans le tissu chaud.",
    ("maman", "Merci d'avoir choisi ce moment-là."),
    "Tes chaussettes fument un peu, près du feu.",
)
FINS["P0001", "P0003", "P0003"] = fin(
    "Je vous l'ai dit sur le manteau, puis à Sarah.",
    ("maman", "Le manteau, le doudou, et maintenant ça."),
    "Nina pose la joue sur le coussin, doudou contre elle.",
    "Le chat rayé a du sable dans une couture.",
    ("papa", "Merci, la phrase a fait tout le chemin."),
    "Le parc est loin, et le salon est assez.",
)
FINS["P0002", "P0001", "P0001"] = fin(
    "Le ballon a fait un tour chacun, puis j'ai dit.",
    ("papa", "L'ours a reçu le ballon, en bas."),
    "Une feuille du toboggan reste collée au coussin.",
    "Nina l'enlève avec soin, sans la déchirer.",
    ("maman", "Merci, la descente a laissé la phrase."),
    "Le métal froid est loin de tes mains.",
)
FINS["P0002", "P0001", "P0002"] = fin(
    "J'ai attendu Sarah en bas, après, j'ai parlé.",
    ("maman", "Le lapin a tenu le bas du toboggan."),
    "Le ballon a une trace d'eau, près du coussin.",
    "Nina pose un doigt sur la trace, puis sur le tissu.",
    ("papa", "Merci d'avoir parlé après la glissade."),
    "On boit le cacao, sans se couper.",
)
FINS["P0002", "P0001", "P0003"] = fin(
    "Je vous l'ai dit au banc, Sarah a dit au revoir.",
    ("papa", "Le chat a pris une goutte, sur le dos."),
    "Le coussin est chaud, et le métal, on l'oublie.",
    "Nina s'enfonce jusqu'aux oreilles, presque.",
    ("maman", "Merci, on a entendu la classe, et le parc."),
    "Le ballon sèche dans l'entrée, sans rebondir.",
)
FINS["P0002", "P0002", "P0001"] = fin(
    "Le seau a glissé sans cri, j'ai dit après.",
    ("maman", "L'ours avait le museau humide, et toi aussi."),
    "Le seau jaune sonne creux, dans l'entrée.",
    "Nina écoute ce creux, puis le silence du salon.",
    ("papa", "Merci, tu as laissé Sarah passer."),
    "Le cacao n'a plus à cacher les mots.",
)
FINS["P0002", "P0002", "P0002"] = fin(
    "J'ai compté, Sarah a glissé, j'ai parlé.",
    ("papa", "Le lapin a une feuille à l'oreille, souvenir."),
    "Une perle d'eau glisse du seau vers le tapis.",
    "Nina la suit des yeux, puis ferme les siens.",
    ("maman", "Merci d'avoir compté, au lieu de crier."),
    "Le coussin prend la forme de tes genoux.",
)
FINS["P0002", "P0002", "P0003"] = fin(
    "Le chat était dans le seau, je vous ai dit.",
    ("maman", "Un trône comique, et une phrase vraie."),
    "Le coussin garde la forme des genoux de Nina.",
    "Elle y revient, plus lente qu'au parc.",
    ("papa", "Merci, demain, le seau sera à deux."),
    "La gouttière dehors a fini ses perles.",
)
FINS["P0002", "P0003", "P0001"] = fin(
    "Les peluches ont eu les marches, puis Sarah.",
    ("papa", "Chacun son tour, tu l'as fait vivre."),
    "Le doudou a glissé, et le coussin le rattrape.",
    "L'ours brun s'y ajoute, lourd et râpé.",
    ("maman", "Merci, tes mots ont descendu avec toi."),
    "On n'entend plus le métal, seulement le tissu.",
)
FINS["P0002", "P0003", "P0002"] = fin(
    "J'ai attendu la fin de la glissade, puis dit.",
    ("maman", "Deux peluches, et une phrase entière."),
    "La feuille mouillée sèche sur le rebord.",
    "Nina la voit, loin du coussin, enfin inoffensive.",
    ("papa", "Merci d'avoir gardé le bas du toboggan."),
    "Le doudou et le lapin se disputent à peine la place.",
)
FINS["P0002", "P0003", "P0003"] = fin(
    "Je me suis assise sur le manteau, j'ai raconté.",
    ("papa", "Sarah a glissé sans être bousculée."),
    "Nina enfonce les poings dans le coussin tiède.",
    "Le chat rayé et le doudou gardent ses poignets.",
    ("maman", "Merci, l'oreille chaude a trouvé la nôtre."),
    "Le salon a repris le rond jaune de la lampe.",
)
FINS["P0003", "P0001", "P0001"] = fin(
    "L'ours se balançait, et moi, j'ai parlé.",
    ("maman", "La chaîne a fini par se taire."),
    "Le ballon sèche près du coussin, sans tic.",
    "Nina pose une main sur le tissu, l'autre sur l'ours.",
    ("papa", "Merci, tu n'as plus tiré le siège."),
    "Le cacao fait un petit nuage, puis s'en va.",
)
FINS["P0003", "P0001", "P0002"] = fin(
    "J'ai attendu que sa balançoire s'arrête.",
    ("papa", "Le lapin a ralenti avec toi."),
    "Le ballon mouillé marque le tapis, près du coussin.",
    "Nina suit la marque, puis s'arrête sur le chaud.",
    ("maman", "Merci d'avoir parlé pieds à terre."),
    "Les chaînes du parc ne font plus tic, ici.",
)
FINS["P0003", "P0001", "P0003"] = fin(
    "Je suis allée au banc, la chaîne faisait trop de bruit.",
    ("maman", "Le chat a une tache d'eau, souvenir."),
    "Le rond jaune de la lampe touche le coussin.",
    "Nina s'y installe, pile dans le rond.",
    ("papa", "Merci, tu as laissé le siège sec à Sarah."),
    "Le ballon reste dans l'entrée, sage pour une fois.",
)
FINS["P0003", "P0002", "P0001"] = fin(
    "L'ours a gardé le seau, au milieu.",
    ("papa", "Plus besoin de le cacher sur le siège."),
    "Le seau jaune veille, et le coussin accueille Nina.",
    "Elle y pose le front, les yeux fermés.",
    ("maman", "Merci, le milieu, c'était une bonne place."),
    "Les chaînes se taisent, même dans ta tête.",
)
FINS["P0003", "P0002", "P0002"] = fin(
    "J'ai parlé quand le siège jaune s'est arrêté.",
    ("maman", "Le lapin écoutait au fond du seau."),
    "Nina souffle, et le coussin se creuse sous sa nuque.",
    "Une oreille de lapin dépasse du tissu.",
    ("papa", "Merci, tu n'as plus crié pour le seau."),
    "Le cacao est à deux gorgées, sans course.",
)
FINS["P0003", "P0002", "P0003"] = fin(
    "Je vous l'ai dit sur le manteau, le seau attendra.",
    ("papa", "Le chat cherchait au fond, toi aussi."),
    "Une chaussette rejoint le coussin, au chaud.",
    "Nina rit, et le chat rayé a la tête ailleurs.",
    ("maman", "Merci, d'abord les mots, après le seau."),
    "Dehors le parc s'éteint, et ici la lampe reste.",
)
FINS["P0003", "P0003", "P0001"] = fin(
    "Sarah a eu la jaune, j'ai parlé, les peluches sur moi.",
    ("maman", "Deux petits coussins, as-tu dit."),
    "L'ours et le doudou gardent le vrai coussin, à deux.",
    "Nina glisse au milieu, enfin assez large.",
    ("papa", "Merci, une goutte a quitté la chaîne."),
    "Le salon n'a plus de tic, seulement le tissu.",
)
FINS["P0003", "P0003", "P0002"] = fin(
    "J'ai attendu ses pieds par terre, puis j'ai dit.",
    ("papa", "Le lapin et le doudou étaient tes oreilles."),
    "Le lapin gris a les oreilles sur le coussin.",
    "Nina y pose les siennes, tout contre.",
    ("maman", "Merci d'avoir ralenti les balançoires."),
    "Le cacao n'a plus à cacher personne.",
)
FINS["P0003", "P0003", "P0003"] = fin(
    "Le manteau était tiède, j'ai tout posé.",
    ("maman", "Le coussin va être content, a dit papa."),
    "Le chat rayé s'endort dans le creux tiède.",
    "Nina pose la paume à côté, sans la presser trop.",
    ("papa", "Merci, Nina, on a entendu jusqu'au bout."),
    "La chaussette du fauteuil a rejoint le chaud, elle aussi.",
)

assert len(FINS) == 27, len(FINS)

# Fix a phrase that uses "tout doucement" - tic-adjacent. And "tout bas".
# Also "Cette fois" is ok. "encore" must not appear.

T2_CHOICE = {
    "P0001": [
        ("narrateur", "Un objet peut aider, près du bac."),
        ("maman", "Le ballon, le seau, ou le doudou ?"),
        ("papa", "Lequel tu prends, Nina ?"),
    ],
    "P0002": [
        ("narrateur", "Au pied du toboggan, trois objets attendent."),
        ("papa", "Le ballon, le seau, ou le doudou ?"),
        ("maman", "Lequel peut t'aider, là ?"),
    ],
    "P0003": [
        ("narrateur", "Près des chaînes, trois objets sont là."),
        ("maman", "Le ballon, le seau, ou le doudou ?"),
        ("papa", "Tu en choisis un ?"),
    ],
}

T3_CHOICE = {
    "P0001": [
        ("narrateur", "Dans le sac, trois peluches peuvent écouter."),
        ("maman", "L'ours brun, le lapin gris, ou le chat rayé ?"),
        ("papa", "Qui t'aide à dire la phrase ?"),
    ],
    "P0002": [
        ("narrateur", "Trois peluches peuvent tenir le bas du toboggan."),
        ("papa", "L'ours brun, le lapin gris, ou le chat rayé ?"),
        ("maman", "Avec qui tu parles, maintenant ?"),
    ],
    "P0003": [
        ("narrateur", "Trois peluches peuvent calmer les chaînes."),
        ("maman", "L'ours brun, le lapin gris, ou le chat rayé ?"),
        ("papa", "Qui s'assoit avec toi ?"),
    ],
}

T1_CHOICE = [
    ("narrateur", "Le parc a trois coins, après la pluie."),
    ("maman", "Le bac à sable, le toboggan, ou les balançoires ?"),
    ("papa", "Sarah est quelque part, là-bas."),
]


def main() -> None:
    folder = ROOT / SID
    source = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in source["chunks"]}
    out_chunks = []

    def add(cid: str, lines, profile: str, sons: str, extra: dict | None = None):
        out_chunks.append(apply_chunk(by_src[cid], lines, profile, sons, extra))

    add("CHK_T0000_P0000", OPENING, "opening", "pluie,cacao", {"emphasis": "coussin"})
    add(
        "CHK_T0001_P0000",
        T1_CHOICE,
        "choice",
        "enfants_parc",
        {
            "fields": {
                "option_1_label": "le bac à sable",
                "option_2_label": "le toboggan",
                "option_3_label": "les balançoires",
            }
        },
    )

    t1_sons = {"P0001": "sable", "P0002": "metal", "P0003": "chaine"}
    t2_sons = {"P0001": "ballon", "P0002": "seau", "P0003": "tissu"}
    t3_sons = {"P0001": "peluche", "P0002": "peluche", "P0003": "peluche"}
    t1_emp = {"P0001": "sable", "P0002": "toboggan", "P0003": "balançoire"}
    t2_emp = {"P0001": "ballon", "P0002": "seau", "P0003": "doudou"}
    t3_emp = {"P0001": "ours", "P0002": "lapin", "P0003": "chat"}

    parks = ("P0001", "P0002", "P0003")
    toys = ("P0001", "P0002", "P0003")
    pels = ("P0001", "P0002", "P0003")

    for p1 in parks:
        add(f"CHK_T0001_{p1}", T1[p1], "action", t1_sons[p1], {"emphasis": t1_emp[p1]})
        q = Q[p1]
        add(
            f"CHK_T0001_{p1}_Q0001",
            q["lines"],
            "clue",
            "",
            {
                "emphasis": q["emphasis"],
                "fields": {
                    "expected_answer": q["expected"],
                    "accepted_examples": q["accepted"],
                    "retry_prompt": "Écoute l'indice, puis réponds.",
                    "engine_ok_text": q["ok"],
                    "engine_near_text": "Tu es tout près. Reprenons l'indice.",
                },
            },
        )
        add(f"CHK_T0001_{p1}_C0001", C[p1], "confirm", "", {"emphasis": "Sarah"})
        add(
            f"CHK_T0001_{p1}_T0002_P0000",
            T2_CHOICE[p1],
            "choice",
            "",
            {
                "fields": {
                    "option_1_label": "le ballon",
                    "option_2_label": "le seau",
                    "option_3_label": "le doudou",
                }
            },
        )
        for p2 in toys:
            add(
                f"CHK_T0001_{p1}_T0002_{p2}",
                T2[(p1, p2)],
                "obstacle",
                t2_sons[p2],
                {"emphasis": t2_emp[p2]},
            )
            add(
                f"CHK_T0001_{p1}_T0002_{p2}_T0003_P0000",
                T3_CHOICE[p1],
                "choice",
                "",
                {
                    "fields": {
                        "option_1_label": "l'ours brun",
                        "option_2_label": "le lapin gris",
                        "option_3_label": "le chat rayé",
                    }
                },
            )
            for p3 in pels:
                add(
                    f"CHK_T0001_{p1}_T0002_{p2}_T0003_{p3}",
                    T3[(p1, p2, p3)],
                    "resolution",
                    t3_sons[p3],
                    {"emphasis": t3_emp[p3]},
                )
                add(
                    f"CHK_T0001_{p1}_T0002_{p2}_T0003_{p3}_F0001",
                    FINS[(p1, p2, p3)],
                    "ending",
                    "cacao,coussin",
                    {"emphasis": "coussin"},
                )

    # order like source
    by_new = {c["chunk_id"]: c for c in out_chunks}
    missing = [c["chunk_id"] for c in source["chunks"] if c["chunk_id"] not in by_new]
    extra = set(by_new) - {c["chunk_id"] for c in source["chunks"]}
    if missing or extra:
        raise SystemExit(f"missing={missing[:8]} extra={list(extra)[:8]}")

    chunks = [by_new[c["chunk_id"]] for c in source["chunks"]]

    # tics
    blob = "\n".join(c["script"] for c in chunks).lower()
    for tic in ("tout doux", "tout calme", " déjà ", "encore "):
        if tic in blob:
            raise SystemExit(f"tic: {tic}")
    if "déjà" in blob:
        raise SystemExit("tic: déjà")
    if re.search(r"\bencore\b", blob):
        raise SystemExit("tic: encore")

    # 27 fins distinctes
    fins = [c for c in chunks if c["kind"] == "passage_fin"]
    if len(fins) != 27:
        raise SystemExit(f"fins {len(fins)}")
    last_n = []
    texts = []
    for c in fins:
        lines = [ln for ln in c["script"].splitlines() if ln.startswith("narrateur|")]
        last_n.append(lines[-1].split("|", 1)[1])
        texts.append(c["text"])
    if len(set(last_n)) < 27:
        raise SystemExit("fins last narrator not unique")
    if len(set(texts)) < 27:
        raise SystemExit("fins text not unique")

    # chemins
    def nwords_path(p1, p2, p3):
        ids = [
            "CHK_T0000_P0000",
            "CHK_T0001_P0000",
            f"CHK_T0001_{p1}",
            f"CHK_T0001_{p1}_Q0001",
            f"CHK_T0001_{p1}_C0001",
            f"CHK_T0001_{p1}_T0002_P0000",
            f"CHK_T0001_{p1}_T0002_{p2}",
            f"CHK_T0001_{p1}_T0002_{p2}_T0003_P0000",
            f"CHK_T0001_{p1}_T0002_{p2}_T0003_{p3}",
            f"CHK_T0001_{p1}_T0002_{p2}_T0003_{p3}_F0001",
        ]
        return sum(words(by_new[i]["text"]) for i in ids)

    counts = [nwords_path(a, b, c) for a in parks for b in toys for c in pels]
    if min(counts) < 380:
        raise SystemExit(f"chemin trop court {min(counts)}")

    merged = dict(source)
    merged["fil_rouge"] = (
        "Après l'école, le coussin du canapé reste tiède. Nina veut le parc tout de suite, "
        "mais une phrase de Sarah à l'école lui noue le ventre. Au salon, le cacao et les bottes "
        "avalent ses mots. Au parc, Sarah ne veut pas la même chose. Ballon, seau ou doudou, "
        "puis ours, lapin ou chat, changent la manière de se faire entendre. De retour, Nina "
        "pose enfin toute la phrase sur le coussin chaud."
    )
    merged["title"] = "Le coussin tiède de Nina"
    merged["characters"] = "Nina, Sarah, papa, maman"
    merged["setting"] = "salon au cacao, puis parc après la pluie"
    merged["chunks"] = chunks
    check(SID, merged["age_band"], merged["chunks"])
    (folder / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"OK {SID} chemins {min(counts)}–{max(counts)} mots  "
        f"1re: {chunks[0]['script'].splitlines()[0].split('|',1)[1]}"
    )


if __name__ == "__main__":
    main()
