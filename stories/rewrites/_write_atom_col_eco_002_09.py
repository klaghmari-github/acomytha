#!/usr/bin/env python3
"""ATOM-COL.ECO.002-09 — Le poisson orange de Mila (F-NAR-019, N2, linéaire)."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "ATOM-COL.ECO.002-09"
LIM = 15
TITLE = "Le poisson orange de Mila"
CHARS = "Mila, papa, maman"
SETTING = "cuisine à la vitre embuée, classe au bocal, puis table"
INDICE = "éclat de poisson"
FIL = (
    "Mila veut dire le poisson orange. Un éclat de poisson brille sur "
    "l'écaille. Elle coupe papa : les mots se perdent. À l'école, une "
    "voix trop près ; elle coupe, trop vite. Elle refuse de foncer, "
    "attend, raconte. Merci vécu. L'éclat de poisson tient l'orange."
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
    "grain de sucre",
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
    "éclat de buée",
    "éclat de buee",
    "éclat de croûte",
    "éclat de croute",
    "éclat de tableau",
    "éclat de casier",
    "éclat de moufle",
    "éclat de craie",
    "éclat de carotte",
    "éclat de seau",
    "éclat de crochet",
    "éclat de mousse",
    "éclat de carton",
    "éclat de pompon",
    "éclat de manteau",
    "éclat de plante",
    "éclat d'arrosoir",
    "éclat de arrosoir",
    "lune d'étain",
    "pli de voile",
    "point de gouttière",
    "trait de craie",
    "trait de vitre",
    "une chose, puis",
    "une chose puis",
    "il faut attendre",
    "toit de verre",
    "hall du marché",
    "petit pain",
    "anaïs",
    "anais",
    "arrosoir",
    "plante",
    "yaourt",
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
            "sous_texte=l_eclat_de_poisson_sur_l_ecaille; tempo=naturel; "
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
            "sous_texte=elle_attend_avant_de_parler; "
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
            "sous_texte=elle_refuse_de_foncer_retrouve_l_eclat_de_poisson; "
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
            "sous_texte=l_eclat_de_poisson_tient_l_orange; "
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
    ("narrateur", "La vitre de la cuisine est embuée."),
    ("narrateur", "Le blanc est tiède sous la paume."),
    ("narrateur", "Mila dessine une petite maison du bout du doigt."),
    ("narrateur", "Une goutte glisse sur le toit dessiné."),
    ("enfant-f", "Elle a une fenêtre ronde !"),
    ("maman", "Tu as fait le toit, toi ?"),
    ("enfant-f", "Oui, et une porte."),
    ("narrateur", "À côté, Mila dessine un poisson."),
    ("narrateur", "Le poisson est petit, un peu tordu."),
    ("narrateur", "Sur une écaille, un éclat de poisson brille."),
    ("enfant-f", "Il brille, papa !"),
    ("papa", "Tu le vois, toi ?"),
    ("enfant-f", "Oui, près de la queue."),
    ("narrateur", "Ça sent le lait tiède, près du bol."),
    ("narrateur", "Une fumée fine danse au-dessus."),
    ("enfant-f", "Le poisson est orange, dans ma tête."),
    ("enfant-f", "Je veux le dire à l'école."),
    ("papa", "On part après le bol ?"),
    ("enfant-f", "Maintenant !"),
    ("narrateur", "En ce moment, Mila coupe la phrase de papa."),
    ("enfant-f", "Il a une queue, près du toit !"),
    ("narrateur", "Les deux voix se cognent."),
    ("papa", "Tu disais, Mila ?"),
    ("enfant-f", "Le poisson."),
    ("narrateur", "Personne n'a la phrase entière."),
    ("narrateur", "Le sourire de Mila disparaît."),
    ("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
    ("narrateur", "Papa s'accroupit à la même hauteur."),
    ("papa", "Tu veux parler, ou regarder la goutte ?"),
    ("enfant-f", "Parler."),
    ("maman", "Tes bottes rouges attendent sur le paillasson."),
    ("narrateur", "Les bottes sont un peu froides."),
    ("papa", "On les enfile ?"),
    ("enfant-f", "Oui."),
    ("papa", "Une."),
    ("papa", "Puis l'autre."),
    ("maman", "Le crayon bleu est dans ta poche."),
    ("maman", "Tu l'as senti ?"),
    ("enfant-f", "Oui."),
    ("enfant-f", "Il est lisse."),
    ("narrateur", "Dehors, le brouillard sent l'herbe mouillée."),
    ("narrateur", "Les bottes font un bruit mou sur le chemin."),
    ("papa", "On tient la main ?"),
    ("enfant-f", "Oui, papa."),
    ("maman", "Au revoir, Mila."),
    ("enfant-f", "Au revoir, maman."),
    ("narrateur", "Plus tard, l'école sent la craie."),
    ("narrateur", "Dans la classe, des poissons en papier pendent."),
    ("narrateur", "Ils bougent un peu, au plafond."),
    ("narrateur", "Un bocal rond brille près du mur."),
    ("maitresse", "Bonjour."),
    ("enfant-f", "Bonjour, maîtresse."),
    ("narrateur", "Mila s'assoit sur le tapis rond."),
    ("narrateur", "Le tapis est un peu frais sous les genoux."),
    ("narrateur", "Le poisson du bocal fait un petit tour."),
    ("narrateur", "Il est orange, comme le dessin."),
    ("enfant-f", "C'est le même !"),
    ("narrateur", "Les mots lui chatouillent la bouche."),
    ("narrateur", "Elle veut le dire, ce poisson, maintenant."),
    ("narrateur", "Une voix s'approche, trop près."),
    ("narrateur", "La voix veut le poisson, elle aussi."),
    ("enfant-f", "Attends, je dois parler !"),
    ("narrateur", "Ses mots se cognent à la voix."),
    ("narrateur", "Mila referme la bouche."),
    ("narrateur", "Les mains restent à plat sur ses genoux."),
    ("enfant-f", "Je veux parler du poisson orange."),
)

QUESTION = L(
    ("narrateur", "Mila veut parler."),
    ("narrateur", "Que fait-elle d'abord ?"),
)

CONFIRM = L(
    ("narrateur", "Mila lève la main."),
    ("narrateur", "Sa main reste en l'air."),
    ("narrateur", "Les doigts tremblent un peu."),
    ("narrateur", "Une autre voix parle d'abord."),
    ("narrateur", "On entend parler d'une barque en papier."),
    ("narrateur", "Mila garde la main levée."),
    ("maitresse", "Mila ?"),
    ("narrateur", "Mila parle."),
    ("enfant-f", "Le poisson du bocal est orange."),
    ("enfant-f", "Comme le dessin de la maison."),
    ("narrateur", "Les mots arrivent entiers, cette fois."),
    ("narrateur", "Sur le flanc, l'éclat de poisson tient."),
    ("narrateur", "Le soir, les assiettes sont chaudes."),
    ("narrateur", "Ça sent le gratin."),
    ("narrateur", "La nappe a des petits carreaux."),
    ("papa", "Alors, Mila ?"),
    ("narrateur", "Mila sent l'envie revenir."),
    ("narrateur", "Elle lève la main, même à table."),
    ("narrateur", "Papa écoute maman d'abord."),
    ("maman", "Le gratin est prêt."),
    ("narrateur", "Mila attend que le silence arrive."),
    ("narrateur", "Elle pose l'autre main sur la nappe."),
    ("papa", "Mila, c'est toi."),
    ("enfant-f", "Le poisson de l'école est le même."),
    ("enfant-f", "Il nage dans le bocal."),
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
    ("enfant-f", "Le poisson, je le montre !"),
    ("narrateur", "Elle court vers la vitre de la cuisine."),
    ("narrateur", "Elle frotte d'un grand geste."),
    ("narrateur", "La maison du doigt disparaît."),
    ("narrateur", "L'éclat de poisson n'est plus là."),
    ("enfant-f", "Il est parti !"),
    ("narrateur", "Le sourire tremble."),
    ("papa", "Tu le cherches ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "Mila refuse de foncer."),
    ("narrateur", "Elle reste près de la vitre."),
    ("narrateur", "Personne ne parle."),
    ("narrateur", "Ses doigts attendent sur le bois."),
    ("narrateur", "Elle souffle sur le verre."),
    ("narrateur", "Un rideau blanc revient, minuscule."),
    ("narrateur", "Elle dessine la maison, sans se presser."),
    ("narrateur", "Puis le poisson, près du toit."),
    ("enfant-f", "Comme ce matin !"),
    ("maman", "Tu le vois, toi ?"),
    ("narrateur", "Mila pose un doigt, sans frotter."),
    ("narrateur", "L'éclat de poisson saute près de la queue."),
    ("papa", "Il est revenu."),
    ("enfant-f", "Il m'a attendue."),
    ("narrateur", "La table garde le gratin."),
)

ENDING = L(
    ("narrateur", "Maman souffle un peu sur la vitre."),
    ("narrateur", "Le poisson orange les regarde."),
    ("enfant-f", "C'est lui."),
    ("maman", "On reste un peu ?"),
    ("enfant-f", "Oui, maman."),
    ("narrateur", "Mila serre le bol contre elle."),
    ("narrateur", "Le lait n'est plus tiède."),
    ("papa", "On se dit bonne nuit dans un moment ?"),
    ("enfant-f", "Oui, papa."),
    ("narrateur", "Les bottes rouges sèchent sur le paillasson."),
    ("enfant-f", "Il est là."),
    ("maman", "On le garde des yeux ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "L'éclat de poisson tient l'orange."),
)


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: c for c in src["chunks"]}
    scripts = {
        "CHK_T0000_P0000": ("opening", OPENING, "pas,eau", {"emphasis": "éclat de poisson"}),
        "CHK_T0000_P0000_Q0001": (
            "clue",
            QUESTION,
            "",
            {
                "emphasis": "d'abord",
                "pause_before": 200,
                "fields": {
                    "expected_answer": "attendre",
                    "accepted_examples": (
                        "attendre | elle attend | lever la main | la main"
                    ),
                    "retry_prompt": "Personne ne l'entend. Que fait Mila d'abord ?",
                    "engine_ok_text": "Oui, elle attend.",
                    "engine_near_text": "Tu es tout près. Reprenons.",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": (
            "resolution",
            CONFIRM,
            "eau",
            {"emphasis": "éclat de poisson"},
        ),
        "CHK_T0000_P0000_END": (
            "obstacle",
            GARDEN,
            "pas",
            {"emphasis": "éclat de poisson"},
        ),
        "CHK_T0000_P0000_END_F0001": (
            "ending",
            ENDING,
            "",
            {"emphasis": "éclat de poisson", "pause_before": 200},
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
    if INDICE not in joined:
        raise SystemExit(f"indice {INDICE} manquant")
    if joined.count(INDICE) < 2:
        raise SystemExit("indice non payé (moins de 2 mentions)")
    if INDICE not in chunks[0]["text"].lower():
        raise SystemExit("indice absent à l'ouverture")
    if INDICE not in chunks[-1]["text"].lower():
        raise SystemExit("indice non payé à la fin")
    if "éclat de buée" in joined or "éclat de buee" in joined:
        raise SystemExit("BAN 001-02 : éclat de buée")
    if "éclat de vitre" in joined:
        raise SystemExit("BAN : éclat de vitre")
    if joined.count("en ce moment") != 1:
        raise SystemExit("en ce moment doit apparaître une fois")
    if "maya" in joined or "anaïs" in joined or "anais" in joined:
        raise SystemExit("prénom interdit dans le texte")
    if "refuse de foncer" not in joined:
        raise SystemExit("manque refuse de foncer")
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
    qtext = chunks[1]["text"]
    if qtext != "Mila veut parler. Que fait-elle d'abord ?":
        raise SystemExit(f"question moteur altérée: {qtext}")
    if chunks[1].get("expected_answer") != "attendre":
        raise SystemExit("expected_answer altéré")
    mait = " ".join(
        ln.split("|", 1)[1]
        for c in chunks
        for ln in c["script"].splitlines()
        if ln.startswith("maitresse|")
    ).lower()
    if any(x in mait for x in ("écoute", "range", "merci", "règle", "leçon", "tour")):
        raise SystemExit(f"maîtresse leçon parlée: {mait}")
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
            "Mila veut dire le poisson orange. Éclat de poisson sur l'écaille. "
            "Elle coupe papa : les mots se perdent. À l'école, une voix trop "
            "près, elle coupe trop vite. Elle lève la main, attend, raconte. "
            "À table elle attend le silence. Merci vécu. Elle frotte la vitre "
            "trop vite : l'éclat part. Elle refuse de foncer, souffle, redessine. "
            "L'éclat de poisson tient l'orange."
        ),
        (
            "Ouverture par la vitre embuée et la maison au doigt, pas le salon. "
            "Monde du dump : vitre cuisine embuée, maison dessinée, goutte, "
            "puis classe au bocal. Pas éclat de buée (BAN 001-02). Pas éclat "
            "de vitre. Indice unique éclat de poisson, nommé puis payé. "
            "≠ COL.ECO.002-01 carotte. ≠ 002-02 seau. ≠ 002-03 carton. "
            "≠ 002-04 mousse. ≠ 002-05 pompon. ≠ 002-06 manteau. "
            "≠ xlsx plante/arrosoir/miel. Anaïs retiré (dump xai). "
            "Leçon attendre avant de parler vécue, pas dite. "
            "Maîtresse label (Bonjour, Mila ?), ne récite pas. Papa ajouté. "
            "Tics encore/déjà/tout doux/tout calme/tout lent absents. "
            "TTS notes+ssml+xai+piper par chunk. Pas apply, pas git, pas audio."
        ),
    )


if __name__ == "__main__":
    main()
