#!/usr/bin/env python3
"""ATOM-COL.ECO.001-02 — Le rayon de Mila (F-NAR-019, N3, linéaire)."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "ATOM-COL.ECO.001-02"
LIM = 16
TITLE = "Le rayon de Mila"
CHARS = "Mila, papa, maman, maîtresse"
SETTING = "cuisine à la buée, classe au tapis d'or, puis mur rose"
FIL = (
    "Mila veut parler maintenant. Un éclat de buée saute dans le rond "
    "de la vitre. Elle coupe papa : les mots se perdent. À l'école, une "
    "voix trop près serre le ventre ; elle coupe, trop vite. Elle refuse "
    "de foncer, attend à la table ronde, raconte. Merci vécu. L'éclat de "
    "buée tient le jaune."
)
TICS = (
    "tout doux",
    "tout calme",
    "tout lent",
    "tout bas",
    "encore",
    "déjà",
    "deja",
    "aujourd'hui,",
    "aujourd'hui ",
    "j'ai compris",
    "j'ai écouté",
    "j'ai ecoute",
    "mission accomplie",
    "merle",
    "miel",
    "grand-père",
    "grand-pere",
    "bon travail",
    "l'histoire est finie",
    "c'est du bon travail",
    "grain de miette",
    "grain de foin",
    "grain de feuille",
    "grain de paille",
    "grain de pin",
    "grain de pépin",
    "grain de pomme",
    "grain de sable",
    "éclat de pince",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "éclat de corde",
    "éclat de caisse",
    "éclat de marche",
    "éclat de caillou",
    "éclat de liste",
    "éclat de clé",
    "éclat de cuillère",
    "éclat de sonnette",
    "éclat de horloge",
    "éclat de tasse",
    "éclat de orange",
    "éclat de colle",
    "éclat de lessive",
    "éclat de vitre",
    "éclat de casserole",
    "éclat de carreau",
    "éclat de grain",
    "éclat de nappe",
    "éclat de boîte",
    "éclat de farine",
    "éclat d'ombre",
    "éclat de ombre",
    "éclat d'écorce",
    "éclat de laine",
    "éclat de lampe",
    "éclat de citron",
    "éclat de wagon",
    "éclat de bec",
    "éclat de fraise",
    "éclat de quille",
    "éclat de promenade",
    "éclat de gouttière",
    "éclat de crayon",
    "lune d'étain",
    "pli de voile",
    "point de gouttière",
    "trait de craie",
    "trait de vitre",
    "une chose, puis",
    "une chose puis",
)


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
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
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
    if m.get("pitch_tag"):
        body = f"<{m['pitch_tag']}>{body}</{m['pitch_tag']}>"
    pause = m["pause"]
    tail = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return f"{body}{tail}".strip()


PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=500,
        sentence=260, energy="warm", contour="storytelling", noise=0.36,
        note=(
            "arc=installation; intention=émerveiller puis tendre; "
            "emotion=impatience_curieuse; intensite=2; destinataire=enfant; "
            "sous_texte=l_eclat_de_buee_dans_le_rond; tempo=naturel; "
            "sourire=léger puis aucun; respiration=ample puis retenue"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=elle_raconte_quand_le_silence_arrive; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note=(
            "arc=résolution; intention=faire_vivre_le_geste; "
            "emotion=retenue puis fierté_calme; intensite=2; "
            "destinataire=enfant; sous_texte=elle_attend_puis_on_l_entend; "
            "tempo=naturel; sourire=léger; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; "
            "emotion=deux_envies_qui_se_heurtent; intensite=2; "
            "destinataire=enfant; "
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat_de_buee; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; "
            "intensite=1; destinataire=enfant; "
            "sous_texte=l_eclat_de_buee_tient_le_jaune; "
            "tempo=posé; sourire=léger; respiration=ample"
        ),
    ),
}


def vet(pairs: list[tuple[str, str]], where: str) -> None:
    prev = ""
    run = 1
    for role, ph in pairs:
        n = words(ph)
        if n > LIM:
            raise SystemExit(f"{where} {n}>{LIM}: {ph}")
        if n == 0:
            raise SystemExit(f"{where} vide")
        if "|" in ph:
            raise SystemExit(f"{where} pipe: {ph}")
        if not ph.endswith((".", "?", "!")):
            raise SystemExit(f"{where} ponctuation: {ph}")
        marks = ph.count(".") + ph.count("?") + ph.count("!")
        if marks != 1:
            raise SystemExit(f"{where} {marks} phrases: {ph}")
        low = ph.lower()
        for bad in FORBIDDEN:
            if bad in low:
                raise SystemExit(f"{where} interdit « {bad} »: {ph}")
        for tic in TICS:
            if tic in low:
                raise SystemExit(f"{where} tic « {tic} »: {ph}")
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


def voice(old: dict, pairs: list[tuple[str, str]], profile: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    vet(pairs, old["chunk_id"])
    m = dict(PROFILES[profile])
    if "emphasis" in extra:
        m["emphasis"] = extra["emphasis"]
    elif "emphasis" not in m:
        m["emphasis"] = None
    lines = [f"{r}|{p}" for r, p in pairs]
    text, script = from_script(lines)
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
    out = deepcopy(old)
    out["text"] = text
    out["script"] = script
    out["sons"] = extra.get("sons", old.get("sons") or "")
    if out["sons"] is None:
        out["sons"] = ""
    out["text_ssml"] = ssml(text, m)
    out["text_xai_tags"] = xai(text, m)
    out["rate_wpm"] = m["wpm"]
    out["rate_label"] = m["rate"]
    out["speed_xai"] = m["speed"]
    out["length_scale_piper"] = m["piper"]
    out["pitch_label"] = m["pitch"]
    out["pitch_ssml"] = m["pitch_ssml"]
    out["pitch_xai_tag"] = m["pitch_tag"]
    out["volume_label"] = m["volume"]
    out["volume_db"] = m["db"]
    out["emphasis_words"] = m.get("emphasis") or ""
    out["pause_before_ms"] = extra.get("pause_before", 0)
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
    for k, v in extra.get("fields", {}).items():
        out[k] = v
    return out


def L(*rows: tuple[str, str]) -> list[tuple[str, str]]:
    return list(rows)


OPENING = L(
    ("narrateur", "Les carreaux tiennent un bout de soleil."),
    ("narrateur", "Le jaune glisse jusqu'à la table ronde."),
    ("narrateur", "Sur la vitre, la buée fait un rideau blanc."),
    ("narrateur", "Maman pose la paume au milieu du blanc."),
    ("narrateur", "Un rond clair s'ouvre, minuscule."),
    ("narrateur", "Dedans, un éclat de buée saute."),
    ("enfant-f", "Il brille, maman !"),
    ("maman", "Tu le vois, toi ?"),
    ("enfant-f", "Oui, dans le rond."),
    ("papa", "Le toit d'en face passe par là."),
    ("narrateur", "Ça sent le lait chaud, près du bol."),
    ("narrateur", "Une fumée fine danse au-dessus."),
    ("narrateur", "Une pomme rouge attend dans la boîte."),
    ("enfant-f", "Je veux dire quelque chose, maintenant !"),
    ("papa", "On t'écoute après la pomme ?"),
    ("enfant-f", "Maintenant !"),
    ("narrateur", "En ce moment, Mila coupe la phrase de papa."),
    ("enfant-f", "Le jaune, il marche sur les carreaux !"),
    ("narrateur", "Les deux voix se cognent."),
    ("papa", "Tu disais, Mila ?"),
    ("enfant-f", "Le rayon."),
    ("narrateur", "Personne n'a la phrase entière."),
    ("narrateur", "Le sourire de Mila disparaît."),
    ("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
    ("narrateur", "Papa s'accroupit à la même hauteur."),
    ("papa", "Tu veux parler, ou regarder le rond ?"),
    ("enfant-f", "Parler."),
    ("maman", "La boîte est prête."),
    ("narrateur", "Mila glisse la pomme dans la boîte."),
    ("narrateur", "Le cartable sent le cahier neuf."),
    ("narrateur", "Les chaussures attendent près de la porte."),
    ("narrateur", "Mila enfile la gauche, puis la droite."),
    ("enfant-f", "Au revoir, maman."),
    ("maman", "Au revoir, Mila."),
    ("papa", "Tu dis bonjour, là-bas ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "Un oiseau passe derrière le blanc."),
    ("narrateur", "Plus tard, l'école sent la craie."),
    ("narrateur", "Les cahiers tapent un peu, dans le casier."),
    ("narrateur", "Le rayon entre aussi dans la classe."),
    ("narrateur", "Il pose un carré d'or sur le tapis."),
    ("maitresse", "Bonjour."),
    ("enfant-f", "Bonjour, maîtresse."),
    ("narrateur", "Mila s'assoit près du carré d'or."),
    ("narrateur", "Le tapis est rêche sous ses genoux."),
    ("narrateur", "Elle veut le dire, ce carré, maintenant."),
    ("narrateur", "Une voix s'approche, trop près."),
    ("narrateur", "La voix veut le tapis, elle aussi."),
    ("narrateur", "Mila sent un malaise."),
    ("narrateur", "Son ventre se serre, minuscule."),
    ("enfant-f", "Attends, je dois parler !"),
    ("narrateur", "Ses mots se cognent à la voix."),
    ("narrateur", "La voix part vers le tapis d'or."),
    ("narrateur", "Mila referme la bouche."),
    ("narrateur", "Les mains restent à plat sur ses genoux."),
    ("narrateur", "Le soir, le rayon a quitté les carreaux."),
    ("narrateur", "Il reste une lumière rose sur le mur."),
    ("narrateur", "La porte s'ouvre."),
    ("maman", "Te voilà, Mila."),
    ("maman", "Tu as faim ?"),
    ("narrateur", "Mila pose le cartable près des chaussures."),
    ("narrateur", "Le ventre est serré."),
    ("enfant-f", "Maman, j'ai un truc !"),
    ("narrateur", "Maman range la boîte près de l'évier."),
    ("narrateur", "Les mots de Mila tombent dans le bruit."),
)

QUESTION = L(
    ("narrateur", "Mila a un malaise."),
    ("narrateur", "Que fait-elle ?"),
)

CONFIRM = L(
    ("narrateur", "Mila s'assoit à la table ronde."),
    ("narrateur", "L'assiette claque un peu contre le bois."),
    ("enfant-f", "Maman, une voix a parlé !"),
    ("narrateur", "Maman n'a pas fini de verser l'eau."),
    ("maman", "L'eau est fraîche, Mila."),
    ("narrateur", "Les deux voix se mélangent."),
    ("enfant-f", "Oh."),
    ("narrateur", "Le sourire ne revient pas."),
    ("narrateur", "Dans sa poitrine, ça se bouscule."),
    ("narrateur", "Mila refuse de foncer."),
    ("narrateur", "Elle referme la bouche."),
    ("narrateur", "Elle pose les mains à plat."),
    ("narrateur", "Elle écoute la cuisine, un instant."),
    ("papa", "La tartine est pour toi."),
    ("narrateur", "Papa pose l'assiette, sans se presser."),
    ("maman", "On t'écoute, quand tu veux."),
    ("narrateur", "Mila attend que le silence arrive."),
    ("narrateur", "Sur la vitre, l'éclat de buée revient."),
    ("enfant-f", "Je peux dire quelque chose ?"),
    ("papa", "Oui, Mila."),
    ("enfant-f", "À l'école, une voix a parlé trop près."),
    ("enfant-f", "J'ai eu un malaise, dans le ventre."),
    ("enfant-f", "Je voulais le dire tout de suite."),
    ("enfant-f", "Les mots sont restés coincés."),
    ("maman", "Merci de nous le dire, Mila."),
    ("narrateur", "Papa a entendu toute la phrase."),
    ("narrateur", "Le ventre de Mila se desserre."),
    ("papa", "Tu as soif ?"),
    ("enfant-f", "Un peu."),
    ("narrateur", "Mila prend une gorgée."),
    ("narrateur", "L'eau chante contre le verre."),
    ("enfant-f", "C'est frais."),
)

GARDEN = L(
    ("narrateur", "Mila glisse de la chaise."),
    ("enfant-f", "Le rond, je le montre !"),
    ("narrateur", "Elle court vers la vitre."),
    ("narrateur", "Elle essuie le blanc d'un grand geste."),
    ("narrateur", "La buée part d'un coup."),
    ("narrateur", "L'éclat de buée n'est plus là."),
    ("enfant-f", "Il est parti !"),
    ("narrateur", "Le sourire tremble."),
    ("papa", "Tu le cherches ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "Mila refuse de foncer."),
    ("narrateur", "Elle reste près de la vitre."),
    ("narrateur", "Personne ne parle."),
    ("narrateur", "Son souffle revient sur le verre."),
    ("narrateur", "Un petit blanc se reforme."),
    ("narrateur", "Le jaune le traverse, sans bruit."),
    ("enfant-f", "Comme ce matin !"),
    ("maman", "Tu le vois, toi ?"),
    ("narrateur", "Mila pose un doigt, sans frotter."),
    ("narrateur", "L'éclat de buée saute dans le rond."),
    ("papa", "Il est revenu."),
    ("enfant-f", "Il m'a attendue."),
    ("narrateur", "La table ronde garde la tartine."),
)

ENDING = L(
    ("narrateur", "La lumière rose tient sur le mur."),
    ("enfant-f", "On m'a entendue."),
    ("maman", "On reste un peu ?"),
    ("enfant-f", "Oui, maman."),
    ("narrateur", "Mila serre le bol contre elle."),
    ("narrateur", "Le lait n'est plus chaud."),
    ("papa", "Le toit d'en face est rose, lui aussi."),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "Le jaune repose dans le rond."),
    ("enfant-f", "Il est là."),
    ("maman", "On le garde des yeux ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "L'éclat de buée tient le jaune."),
)


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: c for c in src["chunks"]}
    scripts = {
        "CHK_T0000_P0000": ("opening", OPENING, "oiseau,porte", {"emphasis": "éclat de buée"}),
        "CHK_T0000_P0000_Q0001": (
            "clue",
            QUESTION,
            "",
            {
                "emphasis": "malaise",
                "pause_before": 200,
                "fields": {
                    "expected_answer": "raconter",
                    "accepted_examples": (
                        "raconter | elle raconte | à maman | à la maison | "
                        "écouter | elle attend | attendre | son tour"
                    ),
                    "retry_prompt": "Elle raconte à maman. Que fait Mila ?",
                    "engine_ok_text": "Oui, elle raconte.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": (
            "resolution",
            CONFIRM,
            "assiette,eau",
            {"emphasis": "éclat de buée"},
        ),
        "CHK_T0000_P0000_END": (
            "obstacle",
            GARDEN,
            "verre",
            {"emphasis": "éclat de buée"},
        ),
        "CHK_T0000_P0000_END_F0001": (
            "ending",
            ENDING,
            "",
            {"emphasis": "éclat de buée", "pause_before": 200},
        ),
    }
    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in scripts]
    extra = set(scripts) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra:
        raise SystemExit(f"{SID} chunks missing={missing} extra={extra}")
    chunks = []
    for c in src["chunks"]:
        cid = c["chunk_id"]
        profile, pairs, sons, extra = scripts[cid]
        extra = dict(extra)
        extra["sons"] = sons
        chunks.append(voice(by[cid], pairs, profile, extra))
    for c in chunks:
        if not c.get("notes") or not c.get("text_ssml") or not c.get("text_xai_tags"):
            raise SystemExit(f"{c['chunk_id']}: TTS incomplet")
        if c["text_xai_tags"] == c["text"]:
            raise SystemExit(f"{c['chunk_id']}: text_xai_tags = text")
        if "<speak>" not in c["text_ssml"]:
            raise SystemExit(f"{c['chunk_id']}: ssml nu")
        if c.get("kind") != by[c["chunk_id"]].get("kind"):
            raise SystemExit(f"{c['chunk_id']}: kind changé")
    joined = "\n".join(c["script"] for c in chunks).lower()
    if "éclat de buée" not in joined:
        raise SystemExit("indice éclat de buée manquant")
    if joined.count("éclat de buée") < 2:
        raise SystemExit("indice non payé (moins de 2 mentions)")
    if "éclat de buée" not in by["CHK_T0000_P0000"]["text"].lower() and (
        "éclat de buée" not in chunks[0]["text"].lower()
    ):
        raise SystemExit("indice absent à l'ouverture")
    if "éclat de buée" not in chunks[-1]["text"].lower():
        raise SystemExit("indice non payé à la fin")
    if joined.count("en ce moment") != 1:
        raise SystemExit("en ce moment doit apparaître une fois")
    if "maya" in joined:
        raise SystemExit("Maya (BAD_NAMES) dans le texte")
    adults = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("papa|") or ln.startswith("maman|")
    ).lower()
    if adults.count("merci") != 1:
        raise SystemExit(f"merci ×{adults.count('merci')}")
    if "bravo" in adults:
        raise SystemExit("bravo en trop")
    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = CHARS
    out["setting"] = SETTING
    out["chunks"] = chunks
    check(SID, out["age_band"], out["chunks"])
    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    relecture(
        SID,
        TITLE,
        (
            "Mila veut parler maintenant. Éclat de buée dans le rond de la "
            "vitre. Elle coupe papa : les mots se perdent. À l'école, une voix "
            "trop près, malaise, elle coupe trop vite. À table elle refuse de "
            "foncer, attend, raconte. Merci vécu. Elle essuie la buée d'un "
            "coup : l'éclat part. Souffle, attente, l'éclat tient le jaune."
        ),
        (
            "Ouverture par les carreaux qui tiennent le soleil, pas le salon. "
            "Monde du dump : école puis maison, rayon jaune, buée, table ronde, "
            "carré d'or, mur rose. Indice unique éclat de buée, nommé puis payé. "
            "≠ COL.ECO.001-01 gouttière/crayon/pluie. ≠ AUT.ROU train/miettes/"
            "pain/fraises/bateau/doudou/flaque/chocolat. "
            "Leçon écouter/attendre/raconter vécue, pas dite. "
            "Maîtresse salue, ne récite pas. Maya retirée. "
            "Tics encore/déjà/tout doux/tout calme/tout lent absents. "
            "TTS notes+ssml+xai+piper par chunk. Pas apply, pas git, pas audio."
        ),
    )


if __name__ == "__main__":
    main()
