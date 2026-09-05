#!/usr/bin/env python3
"""ATOM-AUT.ROU.001-02 — Les miettes de Victorina (F-NAR-019, N1, linéaire)."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "ATOM-AUT.ROU.001-02"
LIM = 10
TITLE = "Les miettes de Victorina"
CHARS = "Victorina, papa, maman"
SETTING = "chambre puis jardin, le matin"
FIL = (
    "Victorina veut porter les miettes à l'oiseau de la barrière, maintenant. "
    "Un éclat de bec saute sur l'oiseau de bois. Elle prend coupelle et chaussure : "
    "les miettes tombent, l'oiseau part. Elle refuse de foncer, pull puis pain, "
    "puis le jardin. Le vent emporte le tas ; elle pose une à une, suit l'éclat. "
    "L'éclat de bec tient le soleil."
)
TICS = (
    "tout doux",
    "tout calme",
    "encore",
    "déjà",
    "deja",
    "aujourd'hui,",
    "aujourd'hui ",
    "j'ai compris",
    "mission accomplie",
    "merle",
    "miel",
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
            "arc=installation; intention=émerveiller; emotion=impatience_curieuse; "
            "intensite=2; destinataire=enfant; sous_texte=l_eclat_de_bec_sur_l_oiseau_de_bois; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=les_miettes_sont_sur_le_tapis; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=pull_puis_pain_puis_miettes; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=deux_envies_qui_se_heurtent; "
            "intensite=2; destinataire=enfant; sous_texte=elle_refuse_de_foncer_retrouve_l_eclat_de_bec; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=l_eclat_de_bec_tient_le_soleil; "
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
    ("narrateur", "La coupelle jaune a passé la nuit."),
    ("narrateur", "Des miettes sèches y tiennent."),
    ("narrateur", "À côté, un oiseau de bois."),
    ("narrateur", "Son bec capte un bout de soleil."),
    ("narrateur", "Un éclat de bec saute sur le bois."),
    ("narrateur", "Le rideau jaune bouge un peu."),
    ("narrateur", "Une chaise attend le pull vert."),
    ("narrateur", "Victorina ouvre un œil."),
    ("narrateur", "Le drap jaune est chaud."),
    ("narrateur", "Ça sent le linge propre."),
    ("narrateur", "Dehors, l'herbe brille, un peu froide."),
    ("narrateur", "La barrière ronde attend au fond."),
    ("papa", "Victorina, tu vois l'oiseau dehors ?"),
    ("enfant-f", "Oui, papa."),
    ("enfant-f", "Il est sur la barrière !"),
    ("maman", "Il a faim, je crois."),
    ("enfant-f", "Je lui porte les miettes maintenant !"),
    ("papa", "Le pain est à la cuisine."),
    ("narrateur", "En ce moment, Victorina saute du lit."),
    ("narrateur", "Elle est en chemise de nuit."),
    ("narrateur", "Ses pieds touchent le tapis."),
    ("narrateur", "Le tapis est chaud, un peu rêche."),
    ("enfant-f", "C'est pour lui !"),
    ("narrateur", "Victorina saisit la coupelle d'une main."),
    ("narrateur", "De l'autre, elle attrape une chaussure."),
    ("maman", "Le pull, aussi."),
    ("narrateur", "Elle penche vers le pull vert."),
    ("narrateur", "La coupelle bascule."),
    ("narrateur", "Les miettes tombent sur le tapis."),
    ("enfant-f", "Oh non !"),
    ("narrateur", "Dehors, l'oiseau s'envole."),
    ("enfant-f", "Il part !"),
    ("narrateur", "Le sourire de Victorina disparaît."),
    ("narrateur", "Dans sa poitrine, ça se bouscule."),
    ("narrateur", "L'envie et l'inquiétude se heurtent."),
    ("narrateur", "Papa s'accroupit à la même hauteur."),
    ("papa", "Tu veux courir, ou regarder ?"),
    ("enfant-f", "Je veux l'oiseau."),
    ("narrateur", "Victorina baisse les épaules."),
    ("maman", "Les miettes sont là, au sol."),
)

QUESTION = L(
    ("narrateur", "Victorina veut porter les miettes."),
    ("maman", "Où sont-elles tombées ?"),
)

CONFIRM = L(
    ("enfant-f", "J'arrête de tout prendre."),
    ("narrateur", "Elle pose la chaussure près du lit."),
    ("narrateur", "Elle ramasse trois miettes, sans se presser."),
    ("enfant-f", "Vous attendez."),
    ("narrateur", "Le pull vert est sur la chaise."),
    ("papa", "Tu le mets ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "Victorina enfile le pull."),
    ("narrateur", "Le pull sent un peu le jardin."),
    ("enfant-f", "C'est vert, comme l'herbe."),
    ("maman", "Le pain t'attend, à table."),
    ("narrateur", "Victorina va vers la cuisine."),
    ("narrateur", "Le carrelage est froid sous ses pieds."),
    ("narrateur", "La table sent le pain chaud."),
    ("narrateur", "Un bol bleu attend près du pain."),
    ("maman", "Tu manges un bout, d'abord ?"),
    ("enfant-f", "Le pain."),
    ("narrateur", "Elle s'assoit."),
    ("narrateur", "Elle croque un coin de pain."),
    ("narrateur", "Le pain est un peu dur."),
    ("narrateur", "Une miette reste au bord."),
    ("maman", "On garde des miettes ?"),
    ("enfant-f", "Pour l'oiseau."),
    ("papa", "Dans la coupelle jaune."),
    ("narrateur", "Victorina glisse les miettes dedans."),
    ("narrateur", "Sur la commode, l'éclat de bec brille."),
    ("enfant-f", "Il me montre le jardin."),
    ("narrateur", "Elle respire, un peu."),
    ("papa", "Les chaussures, après."),
    ("enfant-f", "Oui."),
)

GARDEN = L(
    ("narrateur", "Victorina enfile les deux chaussures."),
    ("narrateur", "Elles serrent un peu."),
    ("papa", "On les ajuste ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "Papa ouvre la porte."),
    ("narrateur", "L'air sent l'herbe mouillée."),
    ("narrateur", "La barrière ronde est vide."),
    ("enfant-f", "Il n'est plus là !"),
    ("narrateur", "Victorina court vers le banc."),
    ("narrateur", "Elle verse les miettes d'un coup."),
    ("narrateur", "Le vent les emporte dans l'herbe."),
    ("enfant-f", "Elles partent !"),
    ("narrateur", "La coupelle est vide."),
    ("narrateur", "Le sourire ne revient pas."),
    ("enfant-f", "Pas comme ça."),
    ("narrateur", "Elle refuse de foncer."),
    ("narrateur", "Elle reste près du banc."),
    ("narrateur", "Personne ne parle."),
    ("narrateur", "Un petit oiseau gris revient."),
    ("narrateur", "Il se pose sur la barrière."),
    ("narrateur", "Sur son bec, un éclat de bec."),
    ("enfant-f", "Comme sur le bois !"),
    ("papa", "Tu le vois, toi ?"),
    ("narrateur", "Victorina pose trois miettes, une à une."),
    ("narrateur", "L'oiseau penche la tête."),
    ("narrateur", "Il picore une miette."),
    ("enfant-f", "Il dit merci."),
    ("papa", "Merci d'avoir posé, Victorina."),
    ("narrateur", "La coupelle reste sur le banc."),
)

ENDING = L(
    ("narrateur", "L'oiseau picore près du banc."),
    ("enfant-f", "Bonjour, oiseau."),
    ("maman", "Tu lui as porté les miettes ?"),
    ("enfant-f", "Oui, maman."),
    ("narrateur", "La coupelle jaune reste sur le bois."),
    ("narrateur", "Une miette colle au banc."),
    ("narrateur", "L'éclat de bec reste sur le bec."),
    ("enfant-f", "Il brille."),
    ("narrateur", "Victorina serre le pull contre elle."),
    ("narrateur", "Le jardin sent l'herbe froide."),
    ("papa", "On reste un peu ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "L'éclat de bec tient le soleil."),
)


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: c for c in src["chunks"]}
    scripts = {
        "CHK_T0000_P0000": ("opening", OPENING, "oiseau", {"emphasis": "éclat de bec"}),
        "CHK_T0000_P0000_Q0001": (
            "clue",
            QUESTION,
            "",
            {
                "emphasis": "miettes",
                "pause_before": 200,
                "fields": {
                    "expected_answer": "le tapis",
                    "accepted_examples": (
                        "le tapis | tapis | par terre | au sol | sur le tapis | tombées"
                    ),
                    "retry_prompt": "La coupelle a basculé. Où sont les miettes ?",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": ("resolution", CONFIRM, "pain", {"emphasis": "éclat de bec"}),
        "CHK_T0000_P0000_END": ("obstacle", GARDEN, "porte,oiseau", {"emphasis": "éclat de bec"}),
        "CHK_T0000_P0000_END_F0001": (
            "ending",
            ENDING,
            "oiseau",
            {"emphasis": "éclat de bec", "pause_before": 200},
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
    if "éclat de bec" not in joined:
        raise SystemExit("indice éclat de bec manquant")
    if joined.count("éclat de bec") < 2:
        raise SystemExit("indice non payé (moins de 2 mentions)")
    if joined.count("en ce moment") != 1:
        raise SystemExit("en ce moment doit apparaître une fois")
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
            "Victorina veut porter les miettes à l'oiseau, maintenant. "
            "Éclat de bec sur l'oiseau de bois. Coupelle et chaussure : "
            "miettes au tapis, oiseau parti. Elle refuse de foncer, pull puis pain. "
            "Au jardin le vent emporte le tas ; elle pose une à une, suit l'éclat. "
            "L'éclat de bec tient le soleil."
        ),
        (
            "Ouverture par la coupelle jaune, pas le salon. "
            "Monde du dump : chambre puis jardin, le matin. "
            "Indice unique éclat de bec, nommé puis payé. "
            "≠ ROU.001-01 train de l'allée / wagon. ≠ grain de miette. "
            "Leçon routine vécue (prendre tout à la fois échoue), pas dite. "
            "Tics encore/déjà/tout doux/tout calme absents. "
            "TTS notes+ssml+xai+piper par chunk. Pas apply, pas git, pas audio."
        ),
    )


if __name__ == "__main__":
    main()
