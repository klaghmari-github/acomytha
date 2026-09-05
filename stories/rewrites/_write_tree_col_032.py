#!/usr/bin/env python3
"""TREE-COL-032 — Le presse-agrumes de Nina (F-NAR-019, N3, TTS). Pas apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, _listy_run, check, from_script, words  # noqa: E402

SID = "TREE-COL-032"
N3 = LIMITS["N3"]
TICS = re.compile(r"\b(tout doux|tout calme|encore|déjà)\b", re.I)
CHILD = "enfant-f"
PEER = "enfant-m"

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=500, sentence=260, energy="warm", contour="storytelling",
        noise=0.36, emphasis="presse-agrumes",
        note="arc=installation; intention=émerveiller; emotion=envie_impatiente; intensite=1; destinataire=enfant; sous_texte=deux envies se heurtent sur la manivelle; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=900, sentence=330, energy="focused", contour="rising",
        noise=0.33, emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton choix compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2,
        pause=700, sentence=320, energy="focused", contour="rising",
        noise=0.32, emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=450, sentence=280, energy="bright", contour="falling",
        noise=0.34, emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=on_t_a_entendue; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=420, sentence=250, energy="lively", contour="dynamic",
        noise=0.37, emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_veut_tourner_tout_de_suite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0,
        pause=520, sentence=300, energy="tense", contour="dynamic",
        noise=0.34, emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_puis_retenue; intensite=2; destinataire=enfant; sous_texte=demander_ouvre_le_tour_de_l_autre; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=560, sentence=270, energy="bright", contour="falling",
        noise=0.35, emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=la_demande_a_changé_le_geste; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3,
        pause=900, sentence=340, energy="calm", contour="falling",
        noise=0.31, emphasis="presse-agrumes",
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_croissant_de_zeste_a_sa_place; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    if m.get("emphasis"):
        e = esc(m["emphasis"])
        if e in body:
            body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict) -> str:
    body = text
    if m.get("emphasis") and m["emphasis"] in body:
        em = m["emphasis"]
        body = body.replace(em, f"<emphasis>{em}</emphasis>", 1)
    if m["rate"] == "slow":
        body = f"<slow>{body}</slow>"
    if m["volume"] == "soft":
        body = f"<soft>{body}</soft>"
    if m.get("pitch_tag"):
        tag = m["pitch_tag"]
        body = f"<{tag}>{body}</{tag}>"
    pause = m["pause"]
    suffix = " [long-pause]" if pause >= 800 else (" [pause]" if pause >= 400 else "")
    return (body + suffix).strip()


def split_sents(phrase: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    for ch in phrase:
        buf.append(ch)
        if ch in ".?!":
            s = "".join(buf).strip()
            if s:
                parts.append(s)
            buf = []
    tail = "".join(buf).strip()
    if tail:
        parts.append(tail if tail.endswith((".", "?", "!")) else tail + ".")
    return parts


def ln(role: str, phrase: str) -> str:
    n = words(phrase)
    if n > N3:
        raise SystemExit(f"{n}>{N3}: {phrase}")
    if n == 0:
        raise SystemExit(f"vide: {role}|{phrase}")
    marks = phrase.count(".") + phrase.count("?") + phrase.count("!")
    if marks != 1:
        raise SystemExit(f"ponctuation {marks}: {phrase}")
    if not phrase.endswith((".", "?", "!")):
        raise SystemExit(f"fin: {phrase}")
    if TICS.search(phrase):
        raise SystemExit(f"tic: {phrase}")
    return f"{role}|{phrase}"


def L(*pairs: tuple[str, str]) -> list[str]:
    out: list[str] = []
    for role, phrase in pairs:
        for sent in split_sents(phrase):
            out.append(ln(role, sent))
    return out


def voice(src: dict, lines: list[str], profile: str, sons: str = "", extra: dict | None = None) -> dict:
    m = dict(PROFILES[profile])
    if extra:
        if "emphasis" in extra:
            m["emphasis"] = extra["emphasis"]
        if "note" in extra:
            m["note"] = extra["note"]
    text, script = from_script(lines)
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
    out["pitch_ssml"] = m["pitch_ssml"]
    out["pitch_xai_tag"] = m["pitch_tag"]
    out["volume_label"] = m["volume"]
    out["volume_db"] = m["db"]
    out["emphasis_words"] = m["emphasis"] or ""
    out["pause_before_ms"] = (extra or {}).get("pause_before", 0)
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
    out["night_policy"] = (extra or {}).get("night_policy", "play")
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    fields = (extra or {}).get("fields") or {}
    out.update(fields)
    return out


N, F, G, P, M = "narrateur", CHILD, PEER, "papa", "maman"


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str = "", extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put(
        "CHK_T0000_P0000",
        L(
            (N, "Les bottes d'Aniss laissent deux flaques mates, près du paillasson."),
            (N, "La pluie les a suivis jusque dans l'entrée."),
            (N, "Nina vit ici avec papa et maman."),
            (N, "Aniss est venu, son jardin est trop mouillé."),
            (N, "Dans la cuisine, un bol d'oranges attend, rond et froid."),
            (N, "Le presse-agrumes de bois dort au milieu de la table."),
            (N, "Un croissant de zeste est coincé sous la vis, mince et parfumé."),
            (N, "Papa essuie le bois avec un torchon à pois."),
            (N, "Maman pose le pichet vide, près de la fenêtre."),
            (N, "Dehors, la gouttière tape un rythme irrégulier."),
            (N, "Ça sent le zeste, vif comme une piqûre."),
            (N, "En ce moment, Nina veut du jus, tout de suite."),
            (F, "C'est moi qui tourne la manivelle !"),
            (G, "Non, je presse l'orange à deux mains !"),
            (N, "Ils parlent l'un dans l'autre, trop fort."),
            (N, "Nina tire. Aniss pousse. Le jus gicle."),
            (N, "Le croissant de zeste s'enfonce sous la vis."),
            (N, "Le sourire de Nina disparaît."),
            (N, "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
            (P, "Vous parlez en même temps. On n'entend plus rien."),
            (M, "Qui veut quoi, là, sur la table ?"),
            (N, "Nina ouvre la bouche, puis la referme."),
        ),
        "opening",
        "pluie,presse",
        {"emphasis": "presse-agrumes"},
    )

    put(
        "CHK_T0001_P0000",
        L(
            (N, "Le presse-agrumes peut voyager un peu, dans la maison."),
            (M, "La cuisine, le jardin, ou la chambre ?"),
            (P, "Où recommencez-vous, sans vous couper ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "la cuisine", "option_2_label": "le jardin", "option_3_label": "la chambre"}},
    )

    # --- T1 ---
    put(
        "CHK_T0001_P0001",
        L(
            (N, "Nina reste à la table collante, le pichet tout près."),
            (N, "Aniss tient l'orange, trop serrée, au-dessus du cône."),
            (N, "Papa parle du torchon à pois, mouillé jusqu'au bord."),
            (F, "La manivelle, vite, c'est moi !"),
            (N, "Sa voix se casse contre celle de papa."),
            (N, "Le jus gicle. Une goutte atteint le torchon."),
            (N, "Le croissant de zeste bloque la vis, plus fort."),
            (N, "Nina a envie de crier. Elle referme les lèvres."),
            (N, "Elle touche le coude de papa, et attend."),
            (N, "Papa s'accroupit, à la même hauteur que la table."),
            (P, "Je t'écoute. Tu veux quoi, Nina ?"),
            (F, "La manivelle, s'il te plaît."),
            (G, "Moi, je veux presser l'orange, pas tourner."),
            (M, "Deux envies. Un tour chacun, après la phrase."),
            (N, "Le pichet tremble, presque vide. La vis attend."),
        ),
        "action",
        "presse,torchon",
        {"emphasis": "manivelle"},
    )
    put(
        "CHK_T0001_P0001_Q0001",
        L(
            (N, "Sous la vis, quelque chose coince, mince et parfumé."),
            (M, "Qu'est-ce qui bloque la manivelle ?"),
        ),
        "clue",
        "",
        {
            "night_policy": "skip",
            "fields": {
                "expected_answer": "zeste",
                "accepted_examples": "zeste | le zeste | croissant | croissant de zeste",
                "retry_prompt": "C'est coincé sous la vis. Un petit morceau d'orange ?",
                "engine_ok_text": "Oui, un croissant de zeste.",
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
            },
        },
    )
    put(
        "CHK_T0001_P0001_C0001",
        L(
            (F, "Le zeste !"),
            (P, "Oui. Un croissant de zeste, sous la vis."),
            (N, "Papa le lève d'un ongle, sans forcer."),
            (M, "Merci d'avoir attendu ma phrase, Nina."),
            (N, "Aniss relâche un peu l'orange. Elle ne fuit plus."),
            (N, "Le pichet a une première larme, orange et claire."),
            (G, "Je tiens. Toi, tu tournes, après moi."),
        ),
        "confirm",
        "presse",
        {"emphasis": "zeste"},
    )
    put(
        "CHK_T0001_P0001_T0002_P0000",
        L(
            (N, "À la table, le jus peut mieux se partager."),
            (P, "Les cubes, le livre, ou la dînette ?"),
            (M, "Quel jeu vous aide à prendre chacun votre tour ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "les cubes", "option_2_label": "le livre", "option_3_label": "la dînette"}},
    )

    put(
        "CHK_T0001_P0002",
        L(
            (N, "Ils portent le presse-agrumes jusqu'au seuil de l'étendoir."),
            (N, "La dalle est mouillée, lisse comme une cuillère."),
            (N, "Une caisse d'oranges sent le bois et la pluie."),
            (G, "On presse dehors, comme une fontaine !"),
            (F, "Non, le pichet reste ici, à l'abri !"),
            (N, "Nina tire la caisse. Aniss tire l'autre bord."),
            (N, "Une orange roule, fuit vers la gouttière."),
            (N, "Nina a envie de crier. Elle serre les dents."),
            (N, "Papa range un cintre, plus loin, sous le toit."),
            (N, "Elle attend qu'il pose le cintre."),
            (N, "Papa s'accroupit, les genoux dans une flaque mince."),
            (F, "L'orange, s'il te plaît."),
            (P, "Je l'attrape. Ensuite, on écoute chacun."),
            (M, "Deux envies. La dalle n'en tient qu'une à la fois."),
            (N, "Le croissant de zeste brille, mouillé, sous la vis."),
        ),
        "action",
        "pluie,orange",
        {"emphasis": "orange"},
    )
    put(
        "CHK_T0001_P0002_Q0001",
        L(
            (N, "Sur la dalle mouillée, un rond orange a fui."),
            (P, "Qu'est-ce qui a roulé vers la gouttière ?"),
        ),
        "clue",
        "",
        {
            "night_policy": "skip",
            "fields": {
                "expected_answer": "orange",
                "accepted_examples": "orange | une orange | l'orange",
                "retry_prompt": "Un fruit a glissé. Lequel ?",
                "engine_ok_text": "Oui, une orange.",
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
            },
        },
    )
    put(
        "CHK_T0001_P0002_C0001",
        L(
            (F, "L'orange !"),
            (M, "Oui. Celle qui voulait partir toute seule."),
            (N, "Papa la pose dans la caisse, sans la lancer."),
            (P, "Merci d'avoir attendu le cintre, Nina."),
            (N, "Aniss essuie ses mains à son manteau."),
            (G, "Je veux la fontaine. Toi, tu veux le pichet."),
            (N, "Le presse-agrumes attend sous l'étendoir, vis brillante."),
        ),
        "confirm",
        "caisse",
        {"emphasis": "orange"},
    )
    put(
        "CHK_T0001_P0002_T0002_P0000",
        L(
            (N, "Sous l'étendoir, le jus a besoin d'un jeu pour les tours."),
            (M, "Les cubes, le livre, ou la dînette ?"),
            (P, "Quel jeu pose un tour, puis l'autre ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "les cubes", "option_2_label": "le livre", "option_3_label": "la dînette"}},
    )

    put(
        "CHK_T0001_P0003",
        L(
            (N, "Ils montent le plateau jusqu'à la chambre."),
            (N, "L'abat-jour a des étoiles pâles. L'horloge fait tic."),
            (N, "Le presse-agrumes voyage sur un plateau de bois."),
            (G, "On joue au restaurant, tout de suite !"),
            (F, "D'abord le jus, dans le pichet !"),
            (N, "Nina ouvre la manivelle. Aniss tire le plateau."),
            (N, "Une goutte tombe. Elle tache le plateau, ronde."),
            (N, "Le sourire d'Aniss disparaît, lui aussi."),
            (N, "Maman plie un pull, près de la fenêtre."),
            (N, "Nina avale son cri. Elle attend la fin du pli."),
            (N, "Maman s'accroupit, à hauteur du plateau."),
            (F, "Le plateau, s'il te plaît. Il glisse."),
            (M, "Je le tiens. Maintenant, je t'écoute."),
            (P, "Deux envies. Le lit n'est pas une table de course."),
            (N, "Le croissant de zeste a glissé, collé au bois."),
        ),
        "action",
        "horloge,plateau",
        {"emphasis": "plateau"},
    )
    put(
        "CHK_T0001_P0003_Q0001",
        L(
            (N, "Sur le bois du plateau, une tache ronde est née."),
            (M, "Qu'est-ce qui a taché le plateau ?"),
        ),
        "clue",
        "",
        {
            "night_policy": "skip",
            "fields": {
                "expected_answer": "jus",
                "accepted_examples": "jus | le jus | une goutte | goutte",
                "retry_prompt": "Une goutte est tombée. De quoi ?",
                "engine_ok_text": "Oui, une goutte de jus.",
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
            },
        },
    )
    put(
        "CHK_T0001_P0003_C0001",
        L(
            (F, "Le jus !"),
            (P, "Oui. Une goutte, trop pressée."),
            (N, "Maman glisse un torchon sous le plateau."),
            (M, "Merci d'avoir attendu mon pull, Nina."),
            (N, "Aniss pose les deux mains à plat, loin de la vis."),
            (G, "Le restaurant peut attendre le pichet."),
            (N, "Le croissant de zeste reste collé, comme un secret."),
        ),
        "confirm",
        "plateau",
        {"emphasis": "jus"},
    )
    put(
        "CHK_T0001_P0003_T0002_P0000",
        L(
            (N, "Sur le lit, le restaurant a besoin d'un vrai tour."),
            (P, "Les cubes, le livre, ou la dînette ?"),
            (M, "Quel jeu vous empêche de parler en même temps ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "les cubes", "option_2_label": "le livre", "option_3_label": "la dînette"}},
    )

    t2 = t2_scenes()
    t2_q = {
        "cuisine": {
            "cubes": "Sur la table, la tour peut garder le pichet.",
            "livre": "Sur la table, la page peut montrer le tour.",
            "dinette": "Sur la table, les tasses attendent chacune leur filet.",
        },
        "jardin": {
            "cubes": "Sous l'étendoir, les cubes peuvent caler la caisse.",
            "livre": "Sous l'étendoir, la page a peur de la pluie.",
            "dinette": "Sous l'étendoir, les tasses peuvent recevoir le filet.",
        },
        "chambre": {
            "cubes": "Sur le plateau, les cubes peuvent faire un quai.",
            "livre": "Près de l'oreiller, la page peut poser le tour.",
            "dinette": "Près de l'abat-jour, les tasses veulent leur restaurant.",
        },
    }
    lieu_key = {"1": "cuisine", "2": "jardin", "3": "chambre"}
    jouet_key = {"1": "cubes", "2": "livre", "3": "dinette"}
    moment_key = {"1": "matin", "2": "sieste", "3": "soir"}

    for li in "123":
        lieu = lieu_key[li]
        for jo in "123":
            jouet = jouet_key[jo]
            lines, sons, emph = t2[(lieu, jouet)]
            cid = f"CHK_T0001_P000{li}_T0002_P000{jo}"
            put(cid, lines, "obstacle", sons, {"emphasis": emph})
            put(
                f"{cid}_T0003_P0000",
                L(
                    (N, t2_q[lieu][jouet]),
                    (P, "Le matin, après la sieste, ou le soir ?"),
                    (M, "Quand le croissant de zeste aura-t-il sa place ?"),
                ),
                "choice",
                "",
                {"fields": {"option_1_label": "le matin", "option_2_label": "après la sieste", "option_3_label": "le soir"}},
            )

    scenes = t3_scenes()
    for li in "123":
        for jo in "123":
            for mo in "123":
                lieu, jouet, moment = lieu_key[li], jouet_key[jo], moment_key[mo]
                passage, ending, s3, se, emph = scenes[(lieu, jouet, moment)]
                base = f"CHK_T0001_P000{li}_T0002_P000{jo}_T0003_P000{mo}"
                put(base, passage, "resolution", s3, {"emphasis": emph})
                put(f"{base}_F0001", ending, "ending", se, {"emphasis": "presse-agrumes"})

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in out_chunks]
    extra = sorted(set(out_chunks) - {c["chunk_id"] for c in src["chunks"]})
    if missing or extra:
        raise SystemExit(f"missing={missing[:12]} extra={extra[:12]}")

    ends = [out_chunks[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(ends) != 27 or len(set(ends)) != 27:
        raise SystemExit(f"fins distinctes: {len(set(ends))}/{len(ends)}")

    t3_only = [
        out_chunks[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage" and "T0003_P000" in c["chunk_id"] and "_F0001" not in c["chunk_id"]
        and not c["chunk_id"].endswith("T0003_P0000")
    ]
    if len(t3_only) != 27 or len(set(t3_only)) != 27:
        raise SystemExit(f"T3 distincts: {len(set(t3_only))}/{len(t3_only)}")

    blob = "\n".join(out_chunks[c["chunk_id"]]["script"] for c in src["chunks"])
    if TICS.search(blob):
        raise SystemExit(f"tic restant: {TICS.search(blob).group(0)}")

    merged = dict(src)
    merged["fil_rouge"] = (
        "Un jour de pluie, Aniss arrive bottes mouillées. Nina veut remplir le pichet "
        "avec le presse-agrumes, tout de suite. Aniss veut presser l'orange à deux mains. "
        "Ils parlent ensemble : le jus gicle, un croissant de zeste s'enfonce sous la vis. "
        "Cuisine, jardin ou chambre changent l'obstacle. Cubes, livre ou dînette changent "
        "la manière de prendre son tour. Matin, sieste ou soir paient le croissant de zeste. "
        "La demande, après l'écoute, ouvre la manivelle."
    )
    merged["title"] = "Le presse-agrumes de Nina"
    merged["characters"] = "Nina, Aniss, papa, maman"
    merged["setting"] = "maison, un jour de pluie, jus d'orange"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])

    # chemins
    def path_words(i: str, j: str, k: str) -> int:
        ids = [
            "CHK_T0000_P0000",
            "CHK_T0001_P0000",
            f"CHK_T0001_P000{i}",
            f"CHK_T0001_P000{i}_Q0001",
            f"CHK_T0001_P000{i}_C0001",
            f"CHK_T0001_P000{i}_T0002_P0000",
            f"CHK_T0001_P000{i}_T0002_P000{j}",
            f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P0000",
            f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}",
            f"CHK_T0001_P000{i}_T0002_P000{j}_T0003_P000{k}_F0001",
        ]
        return sum(words(out_chunks[x]["text"]) for x in ids)

    lengths = [path_words(i, j, k) for i in "123" for j in "123" for k in "123"]
    print(f"chemins {min(lengths)}–{max(lengths)} moy {sum(lengths)//len(lengths)}")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / SID / "RELECTURE.md").write_text(
        "\n".join(
            [
                "# TREE-COL-032 — Le presse-agrumes de Nina",
                "",
                "- **Public :** N3, 5–6 ans, lecture interactive familiale",
                "- **Leçon :** COL.POL.001 — demander avec attention et respect (implicite) ; tours de parole vécus",
                "- **Personnages :** Nina, Aniss, papa, maman",
                "- **Lieu :** maison sous la pluie, cuisine, seuil de l'étendoir, chambre",
                "- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes",
                "",
                "Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.",
                "",
                "## Promesse narrative",
                "",
                "Un jour de pluie, Aniss arrive bottes mouillées. Nina veut remplir le pichet "
                "avec le presse-agrumes **maintenant**. Aniss veut presser l'orange à deux mains. "
                "Ils parlent en même temps : le jus gicle, un croissant de zeste s'enfonce sous la vis. "
                "Cuisine (table collante), jardin (seuil de l'étendoir) ou chambre (plateau) changent l'obstacle. "
                "Cubes, livre ou dînette changent la manière de prendre son tour. "
                "Matin, sieste ou soir paient l'indice du début. La demande, après l'écoute, ouvre la manivelle.",
                "",
                "## Vécu",
                "",
                "Nina veut tourner. Aniss veut presser. Première tentative : ils tirent ensemble, personne "
                "n'entend, le zeste coince. Envies de couper, retenue, écoute réelle, plaisir d'être entendu. "
                "Papa et maman s'accroupissent, conversationnels. Le croissant de zeste, vu à l'ouverture, "
                "revient au climax. 27 fins : le presse-agrumes porte une trace unique.",
                "",
                "## Améliorations",
                "",
                "- P1 F-NAR-019 / example4 v2 : ouverture par les bottes mouillées, pas le gabarit.",
                "- Indice unique : croissant de zeste sous la vis, payé à chaque climax.",
                "- Deux enfants, deux envies. Première idée échoue. 2e ruse plus maline.",
                "- T1/T2/T3 changent l'action, pas seulement le décor. Presse-agrumes conservé partout.",
                "- Refrains Bonjour / s'il te plaît / merci récités, Bravo bon travail, l'histoire est finie : retirés.",
                "- Tics encore / déjà / tout doux / tout calme : retirés.",
                "- Revers allongé : T3 et fins plus incarnés, souvenir distinct.",
                "- Un merci vécu. TTS par fonction (opening/choice/clue/confirm/action/obstacle/resolution/ending).",
                f"- Chemins {min(lengths)}–{max(lengths)} mots (moyenne {sum(lengths)//len(lengths)}).",
                "- `check()` OK. Pas d'apply. Pas d'audio.",
                "",
                "## Direction vocale",
                "",
                "Chaque segment a un `notes` : arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration. "
                "`slow` réservé aux choix, indices et fins. Action plus vive. Fins : pitch bas, volume doux, pause longue.",
                "",
                "## Contrôles",
                "",
                "- 86 chunks",
                "- 27 chemins, 27 fins distinctes, 27 climats T3 distincts",
                "- `text` = `script` collé, N3 ≤ 16 mots/phrase",
                "- `text_ssml` et `text_xai_tags` enrichis",
                "- graphe `option_*_next` / `default_next` / `kind` inchangés",
                "",
                "## Non vérifié",
                "",
                "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'apply.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"wrote {SID} {len(merged['chunks'])} chunks")


def t2_scenes() -> dict[tuple[str, str], tuple]:
    data = {}
    data[("cuisine", "cubes")] = (
        L(
            (N, "Nina sort les cubes de bois, l'un orange, l'autre clair."),
            (N, "Elle veut une tour, pour caler le pichet."),
            (G, "Je mets le cube sous la manivelle !"),
            (N, "Aniss glisse un cube trop vite. La vis se bloque."),
            (N, "Le croissant de zeste recule, coincé plus bas."),
            (F, "Attends. Je refuse de foncer."),
            (N, "Personne ne donne la réponse. Nina observe la vis."),
            (N, "Elle écoute le petit crac du bois, sous le cube."),
            (P, "Tu veux quelque chose, Nina ?"),
            (F, "Le cube, s'il te plaît. Pas sous la vis."),
            (G, "D'accord. Moi, je tiens la tour."),
            (N, "La tour se dresse. Le pichet ne tremble plus."),
        ),
        "cubes,presse",
        "cube",
    )
    data[("cuisine", "livre")] = (
        L(
            (N, "Maman pose le livre près du pichet, loin du jus."),
            (N, "Une page montre un oranger, rond et chargé."),
            (G, "Je tourne la page, c'est moi !"),
            (N, "Aniss tire pendant que Nina veut la manivelle."),
            (N, "La page se plisse. Une goutte menace l'oranger."),
            (F, "Stop. On ne fonce pas."),
            (N, "Nina regarde le livre, puis la vis, puis Aniss."),
            (N, "Le croissant de zeste fait la même courbe que la page."),
            (M, "Qui parle en premier, sans couper ?"),
            (F, "La page, s'il te plaît. Ensuite, je tourne."),
            (G, "Je tiens le livre. Toi, tu tournes après."),
            (N, "L'oranger reste sec. La vis peut céder."),
        ),
        "pages,presse",
        "oranger",
    )
    data[("cuisine", "dinette")] = (
        L(
            (N, "Nina aligne deux tasses froides, lisses, près du pichet."),
            (N, "Aniss saisit la théière miniature, trop pleine d'air."),
            (G, "Je verse tout, dans toutes les tasses !"),
            (N, "Il penche trop tôt. Rien ne sort, puis trop d'élan."),
            (N, "Le pichet bascule. Le croissant de zeste tremble."),
            (F, "Une tasse. Pas toutes."),
            (N, "Nina refuse de foncer. Elle pose la théière."),
            (N, "Elle écoute le silence de la vis, un petit métal."),
            (P, "Tu demandes quoi, pour le filet ?"),
            (F, "Un filet, s'il te plaît, dans ma tasse d'abord."),
            (G, "Ensuite la mienne. J'attends."),
            (N, "Les deux tasses attendent, vides, prêtes, sans se bousculer."),
        ),
        "tasse,presse",
        "tasses",
    )
    data[("jardin", "cubes")] = (
        L(
            (N, "Nina pose trois cubes sur la dalle, pour caler la caisse."),
            (N, "L'eau les rend glissants, comme des savons."),
            (G, "Je mets le plus gros sous le presse-agrumes !"),
            (N, "Le gros cube bascule. La caisse penche vers la gouttière."),
            (N, "Le croissant de zeste s'enfonce d'un cran."),
            (F, "Non. On pose, on n'envoie pas."),
            (N, "Nina s'immobilise. Elle écoute la dalle, le clapot."),
            (N, "Elle retrouve le croissant, luisant sous la vis."),
            (M, "Tu veux de l'aide, comment ?"),
            (F, "Le cube stable, s'il te plaît, contre la caisse."),
            (G, "Je le tiens. Toi, tu tournes."),
            (N, "La caisse ne glisse plus. La vis peut respirer."),
        ),
        "cubes,dalle",
        "cube",
    )
    data[("jardin", "livre")] = (
        L(
            (N, "Maman ouvre le livre sous l'étendoir, à l'abri."),
            (N, "L'oranger de la page a une feuille brillante."),
            (G, "Je montre la page à la pluie !"),
            (N, "Aniss avance trop. Une goutte vise le papier."),
            (N, "Nina rattrape le livre. Son cœur tape."),
            (F, "Pas dehors. Ici, sous le toit."),
            (N, "Elle refuse de foncer. Elle observe la vis."),
            (N, "Le croissant de zeste imite la feuille de la page."),
            (P, "Que demandes-tu, pour la page ?"),
            (F, "Tu la tiens, s'il te plaît. Loin de la gouttière."),
            (G, "Je tiens. Après, c'est ton tour de manivelle."),
            (N, "La page reste sèche. Le seuil sent l'orange et le bois."),
        ),
        "pages,pluie",
        "page",
    )
    data[("jardin", "dinette")] = (
        L(
            (N, "Nina pose deux tasses sur la caisse, près du pichet."),
            (N, "Aniss veut remplir la sienne avec la pluie."),
            (G, "La mienne, c'est de l'eau du toit !"),
            (N, "Il lève la tasse. Une goutte sale y tombe."),
            (N, "Nina secoue la tête. Le sourire est parti."),
            (F, "Le jus, pas la gouttière."),
            (N, "Elle pose la tasse. Elle écoute la vis, un crac fin."),
            (N, "Le croissant de zeste est là, comme au début."),
            (M, "Tu veux quoi, dans ta tasse ?"),
            (F, "Le jus, s'il te plaît. Un filet, pas la pluie."),
            (G, "D'accord. Ma tasse attend le vrai orange."),
            (N, "Les deux tasses sont vides, propres, prêtes pour le filet."),
        ),
        "tasse,pluie",
        "tasse",
    )
    data[("chambre", "cubes")] = (
        L(
            (N, "Nina construit un quai de cubes, autour du plateau."),
            (N, "Le plus haut cube frôle l'abat-jour aux étoiles."),
            (G, "Je fais une tour plus haute, moi !"),
            (N, "Aniss ajoute trop vite. Le plateau bascule d'un doigt."),
            (N, "Le croissant de zeste glisse vers le bord du bois."),
            (F, "On arrête. Le jus d'abord."),
            (N, "Nina refuse de foncer. Elle écoute l'horloge."),
            (N, "Tic. Puis elle retrouve le croissant, collé."),
            (P, "Que demandes-tu, pour le quai ?"),
            (F, "Tes cubes, s'il te plaît, plus bas que le pichet."),
            (G, "Je baisse. Toi, tu tournes."),
            (N, "Le quai tient. Le plateau ne voyage plus tout seul."),
        ),
        "cubes,plateau",
        "quai",
    )
    data[("chambre", "livre")] = (
        L(
            (N, "Sur l'oreiller, le livre s'ouvre, l'oranger bien net."),
            (N, "Aniss veut lire à voix haute, pendant la manivelle."),
            (G, "Moi je raconte, toi tu tournes, en même temps !"),
            (N, "Les deux voix se mêlent. L'horloge les coupe."),
            (N, "Une goutte du plateau menace la page."),
            (F, "Un après l'autre. Pas ensemble."),
            (N, "Nina observe la vis. Le croissant de zeste luit."),
            (N, "Il a la même courbe que l'oranger du livre."),
            (M, "Qui commence, si on s'écoute ?"),
            (F, "La page, s'il te plaît, jusqu'au bout. Après, je tourne."),
            (G, "Je lis. Puis je me tais."),
            (N, "La page finit. Le plateau attend, sans bouger."),
        ),
        "pages,horloge",
        "page",
    )
    data[("chambre", "dinette")] = (
        L(
            (N, "Nina pose la dînette au pied de l'abat-jour."),
            (N, "Deux tasses, une théière, un plat trop grand."),
            (G, "Restaurant ouvert, tout le monde à table !"),
            (N, "Il tape une tasse contre le plateau. Le pichet tressaille."),
            (N, "Le croissant de zeste bascule, presque à terre."),
            (F, "Le restaurant attend le jus."),
            (N, "Nina ramasse le croissant, sans crier."),
            (N, "Elle écoute l'horloge, puis la vis, puis Aniss."),
            (P, "Tu veux quoi, pour ouvrir le restaurant ?"),
            (F, "Un filet, s'il te plaît, dans ta tasse et dans la mienne."),
            (G, "J'attends le serveur. C'est toi."),
            (N, "Les tasses sont sages. Le plateau redevient une table."),
        ),
        "tasse,plateau",
        "restaurant",
    )
    return data


def t3_scenes() -> dict[tuple[str, str, str], tuple]:
    data: dict[tuple[str, str, str], tuple] = {}

    def S(*rows):
        return L(*rows)

    # CUISINE + CUBES
    data[("cuisine", "cubes", "matin")] = (
        S(
            (N, "Le matin, la lumière est pâle sur la table collante."),
            (N, "Le plancher est froid. Un oiseau parle, loin."),
            (N, "Les oranges sont dures, trop froides pour le jus."),
            (G, "Je tourne plus fort !"),
            (N, "Aniss force. Un cube de la tour glisse."),
            (N, "Nina refuse. Elle observe la vis, écoute le bois."),
            (N, "Le croissant de zeste du début est là, coincé."),
            (F, "On le lève, s'il te plaît, avant de tourner."),
            (N, "Papa le lève. Aniss tient la tour. Nina tourne."),
            (N, "Un filet lent arrive, clair, dans le pichet."),
            (M, "Chacun a parlé. Chacun a écouté."),
        ),
        S(
            (N, "Plus tard, l'oiseau s'est tu derrière la vitre."),
            (P, "Raconte le tour difficile, jusqu'au bout."),
            (F, "Le cube a glissé. On a levé le zeste, puis tourné."),
            (G, "J'ai tenu la tour. Nina a demandé."),
            (M, "Merci d'avoir parlé chacun votre tour."),
            (N, "Le presse-agrumes sèche, vis propre, près du pichet."),
            (N, "Le croissant de zeste orne le cube orange, tout en haut."),
            (N, "La table n'est plus collante. Le matin sent l'écorce."),
        ),
        "cubes,oiseau",
        "presse,verre",
        "croissant de zeste",
    )
    data[("cuisine", "cubes", "sieste")] = (
        S(
            (N, "Après la sieste, l'air est tiède. Un rideau bouge."),
            (N, "Nina a une joue un peu marquée par l'oreiller."),
            (N, "Le jus du pichet s'est séparé : clair dessus, pulpe au fond."),
            (G, "Je veux la pulpe !"),
            (F, "Moi, le clair !"),
            (N, "Aniss penche trop. Un cube tombe dans le filet."),
            (N, "Nina s'arrête. Elle retrouve le croissant sous la vis."),
            (F, "Le cube, s'il te plaît, hors du pichet."),
            (N, "Aniss le retire. Ils versent : clair d'abord, pulpe ensuite."),
            (P, "Deux envies, deux temps. La vis a dit oui."),
            (N, "Le rideau se pose. Le pichet a deux couleurs."),
        ),
        S(
            (N, "Le rideau ne bouge plus. La cuisine est tiède."),
            (M, "Dis-nous la pulpe, et le clair."),
            (F, "On n'a pas tout versé d'un coup."),
            (G, "J'ai eu la pulpe. Nina a eu le clair."),
            (P, "Merci d'avoir retiré le cube, Aniss."),
            (N, "Le presse-agrumes repose, un peu poisseux au cône."),
            (N, "Le croissant de zeste sèche sur le cube tombé."),
            (N, "Deux taches restent au fond du pichet, l'une claire."),
        ),
        "rideau,pulpe",
        "pichet,tissu",
        "pulpe",
    )
    data[("cuisine", "cubes", "soir")] = (
        S(
            (N, "Au soir, la lampe allume un rond chaud sur la tour."),
            (N, "Dehors, un vélo passe, loin, sur le pavé mouillé."),
            (N, "Il reste une orange, la dernière, un peu molle."),
            (G, "C'est la mienne !"),
            (F, "On la partage."),
            (N, "Nina ne fonce pas. Elle cherche le croissant de zeste."),
            (N, "La lampe le fait briller, coincé sous la vis."),
            (F, "On le sort, s'il te plaît, puis un demi-tour chacun."),
            (N, "Aniss sort le zeste. Nina tourne. Aniss tourne."),
            (M, "La dernière orange a suffi, parce que vous avez demandé."),
            (N, "Le filet tombe, court, précieux, dans le pichet."),
        ),
        S(
            (N, "La lampe garde son rond. Le vélo s'est tu."),
            (P, "On t'écoute, Nina. Toute la dernière orange."),
            (F, "Un demi-tour pour moi, un demi-tour pour Aniss."),
            (G, "Le zeste brillait, comme une lune miniature."),
            (M, "Merci d'avoir partagé sans crier."),
            (N, "Le presse-agrumes sèche près de la lampe."),
            (N, "Le croissant de zeste dort sur le cube le plus haut."),
            (N, "Le pichet n'a qu'un doigt de jus, et il suffit."),
        ),
        "lampe,velo",
        "lampe,bois",
        "orange",
    )

    # CUISINE + LIVRE
    data[("cuisine", "livre", "matin")] = (
        S(
            (N, "Le matin, la page de l'oranger est froide comme la table."),
            (N, "Un oiseau parle. Les oranges, elles, restent muettes."),
            (G, "Je lis, et je tourne, en même temps !"),
            (N, "La page se plisse. Le jus n'arrive pas, trop froid."),
            (N, "Nina pose le livre. Elle refuse de forcer."),
            (N, "Elle retrouve le croissant de zeste, sous la vis."),
            (F, "On réchauffe l'orange dans les mains, s'il te plaît."),
            (N, "Aniss la roule. Nina demande la manivelle, ensuite."),
            (N, "Le filet vient, lent. L'oranger de la page reste sec."),
            (P, "La page a attendu. La vis aussi."),
            (N, "Une empreinte de jus, minuscule, orne le bas du livre."),
        ),
        S(
            (N, "L'oiseau s'est tu. Le livre reste ouvert, loin du pichet."),
            (M, "Montre l'empreinte, sans la cacher."),
            (F, "C'est le moment difficile, là, le petit doigt de jus."),
            (G, "J'ai roulé l'orange. Nina a demandé."),
            (P, "Merci d'avoir laissé la page finir."),
            (N, "Le presse-agrumes sèche. La vis est libre."),
            (N, "Le croissant de zeste sert de signet, dans l'oranger."),
            (N, "Le matin sent le papier et l'écorce, mêlés."),
        ),
        "pages,froid",
        "livre,presse",
        "empreinte",
    )
    data[("cuisine", "livre", "sieste")] = (
        S(
            (N, "Après la sieste, une goutte a collé la page au bois."),
            (N, "Le rideau bouge. Nina a la joue chaude."),
            (G, "J'arrache la page !"),
            (N, "Nina pose une main. Elle ne fonce pas."),
            (N, "Elle écoute le papier, un bruit de peau."),
            (N, "Le croissant de zeste, sous la vis, a la même courbe."),
            (F, "On décolle, s'il te plaît, tout lentement."),
            (N, "Maman souffle. La page se lève, sans se déchirer."),
            (N, "Ensuite, Aniss tient le livre. Nina tourne."),
            (M, "Le papier a eu son tour. La manivelle, le sien."),
            (N, "Le pichet se remplit d'un jus un peu trouble, tiède."),
        ),
        S(
            (N, "Le rideau s'est arrêté. La page est libre."),
            (P, "Raconte le décollage, pas seulement le jus."),
            (F, "On a soufflé. On n'a pas tiré."),
            (G, "J'ai failli déchirer. Nina a demandé d'attendre."),
            (M, "Merci d'avoir parlé avant d'arracher."),
            (N, "Le presse-agrumes brille, un peu collant au cône."),
            (N, "Le croissant de zeste sèche au coin de la page."),
            (N, "Une vague blanche reste où le papier s'était collé."),
        ),
        "page,rideau",
        "papier,pichet",
        "page",
    )
    data[("cuisine", "livre", "soir")] = (
        S(
            (N, "Au soir, la lampe allume l'oranger de la page."),
            (N, "Un vélo passe. Il reste une orange, ridée."),
            (G, "Je dessine le presse-agrumes, dans la marge !"),
            (N, "Aniss prend le crayon trop tôt. La vis attend."),
            (N, "Nina observe. Elle retrouve le croissant de zeste."),
            (F, "D'abord le jus, s'il te plaît. Après, le dessin."),
            (N, "Aniss pose le crayon. Ils tournent, un chacun."),
            (N, "Le filet est court. Puis Aniss dessine la vis."),
            (P, "La marge a attendu. Elle a mieux dessiné."),
            (N, "Dans la marge, un petit croissant imite le zeste."),
            (M, "Le livre garde le soir, et le dernier tour."),
        ),
        S(
            (N, "La lampe baisse un peu. Le vélo s'éloigne."),
            (M, "Montre la marge, jusqu'au croissant."),
            (F, "Aniss l'a dessiné après le jus, pas pendant."),
            (G, "C'est le presse-agrumes, et le zeste coincé."),
            (P, "Merci d'avoir posé le crayon, Aniss."),
            (N, "Le vrai presse-agrumes sèche, vis ouverte."),
            (N, "Le croissant de zeste repose sur la marge, comme un modèle."),
            (N, "Le pichet n'a qu'un fond, orange sous la lampe."),
        ),
        "crayon,lampe",
        "livre,lampe",
        "marge",
    )

    # CUISINE + DINETTE
    data[("cuisine", "dinette", "matin")] = (
        S(
            (N, "Le matin, les tasses de dînette sont froides, trop vides."),
            (N, "Un oiseau parle. Les oranges, dures, rendent peu."),
            (G, "Je remplis les deux d'un seul coup !"),
            (N, "La théière penche. Rien, puis trop. Une tasse déborde."),
            (N, "Nina s'arrête. Elle cherche le croissant sous la vis."),
            (F, "Un filet, s'il te plaît, dans une tasse, puis l'autre."),
            (N, "Aniss attend. Nina tourne. Un filet mince arrive."),
            (N, "Ils versent : d'abord Nina, ensuite Aniss."),
            (M, "Deux tasses. Deux tours. Pas de cascade."),
            (N, "Au fond d'une tasse, le croissant de zeste flotte, comme une lune."),
            (P, "Le matin a eu son jus, sans se bousculer."),
        ),
        S(
            (N, "L'oiseau s'est tu. Les tasses restent sur la table."),
            (P, "Raconte la cascade qui n'a pas eu lieu."),
            (F, "On a versé l'une, puis l'autre."),
            (G, "Ma tasse a une lune de zeste."),
            (M, "Merci d'avoir attendu le filet, Aniss."),
            (N, "Le presse-agrumes sèche, cône luisant."),
            (N, "La lune de zeste sèche au bord de la tasse d'Aniss."),
            (N, "Le pichet a servi de carafe, pour deux petites soifs."),
        ),
        "tasse,oiseau",
        "dinette,table",
        "lune",
    )
    data[("cuisine", "dinette", "sieste")] = (
        S(
            (N, "Après la sieste, une mousse a pris au goulot du pichet."),
            (N, "Le rideau bouge. Nina a la joue chaude."),
            (G, "Je veux la mousse !"),
            (F, "Moi, le jus d'en dessous !"),
            (N, "Aniss plonge la théière trop vite. La mousse s'effondre."),
            (N, "Nina refuse de plonger. Elle observe la vis."),
            (N, "Le croissant de zeste est coincé, comme au début."),
            (F, "On lève le zeste, s'il te plaît, puis on verse lentement."),
            (N, "La mousse revient, mince. Aniss la reçoit. Nina le clair."),
            (P, "Deux envies, deux hauteurs dans le pichet."),
            (N, "Le rideau se pose. Les tasses n'ont plus soif de se couper."),
        ),
        S(
            (N, "La cuisine est tiède. La mousse a disparu."),
            (M, "Dis-nous qui a eu le dessus, qui a eu le dessous."),
            (F, "Aniss la mousse. Moi le clair. On a demandé."),
            (G, "J'ai failli tout casser. Nina a dit s'il te plaît."),
            (P, "Merci d'avoir levé le zeste avant de plonger."),
            (N, "Le presse-agrumes repose, un peu de mousse au cône."),
            (N, "Le croissant de zeste sèche dans la théière miniature."),
            (N, "Deux cercles restent au fond des tasses, l'un plus pâle."),
        ),
        "mousse,rideau",
        "tasse,pichet",
        "mousse",
    )
    data[("cuisine", "dinette", "soir")] = (
        S(
            (N, "Au soir, la lampe se mire dans les deux tasses vides."),
            (N, "Un vélo passe. Il reste une orange."),
            (G, "Restaurant de nuit, je sers tout le monde !"),
            (N, "Il veut verser avant la manivelle. Nina pose la théière."),
            (N, "Elle retrouve le croissant de zeste, allumé par la lampe."),
            (F, "D'abord la vis, s'il te plaît. Après, tu sers."),
            (N, "Ils tournent, un chacun. Un filet court naît."),
            (N, "Aniss sert Nina. Nina sert Aniss."),
            (M, "Le restaurant a ouvert, parce que vous avez demandé."),
            (N, "Dans chaque tasse, un rond de lampe tremble."),
            (P, "La dernière orange a fait deux invités, pas une dispute."),
        ),
        S(
            (N, "La lampe reste. Le vélo s'est tu."),
            (P, "Raconte le service, pas seulement le goût."),
            (F, "Aniss m'a servi. Je l'ai servi."),
            (G, "On a demandé la vis, avant le restaurant."),
            (M, "Merci d'avoir posé la théière, Nina."),
            (N, "Le presse-agrumes sèche près des tasses."),
            (N, "Le croissant de zeste flotte, sec, dans la plus petite."),
            (N, "Deux ronds de lampe s'éteignent doucement, au fond."),
        ),
        "lampe,tasse",
        "dinette,lampe",
        "restaurant",
    )

    # JARDIN + CUBES
    data[("jardin", "cubes", "matin")] = (
        S(
            (N, "Le matin, la dalle est froide sous l'étendoir."),
            (N, "Un oiseau parle. Les cubes luisent, mouillés."),
            (G, "Je cale avec le cube le plus lourd !"),
            (N, "Le cube glisse. La caisse part vers la gouttière."),
            (N, "Nina rattrape. Elle refuse de forcer la vis."),
            (N, "Elle retrouve le croissant de zeste, luisant de pluie."),
            (F, "Un cube sec, s'il te plaît, contre la caisse."),
            (N, "Papa tend un cube pris sous le toit, plus sec."),
            (N, "Aniss cale. Nina tourne. Un filet naît, malgré le froid."),
            (M, "La dalle a eu son tour. La vis, le sien."),
            (N, "L'oiseau se tait. Le pichet a un fond clair."),
        ),
        S(
            (N, "Sous l'étendoir, la dalle sèche par petites peaux."),
            (P, "Raconte le cube qui a glissé."),
            (F, "On a demandé un cube sec. Pas le plus lourd."),
            (G, "J'ai calé. Nina a tourné."),
            (M, "Merci d'avoir rattrapé la caisse, Nina."),
            (N, "Le presse-agrumes sèche sur un cube, hors de l'eau."),
            (N, "Le croissant de zeste orne le cube lourd, oublié."),
            (N, "La gouttière chante, plus loin, sans eux."),
        ),
        "dalle,cubes",
        "etendoir,bois",
        "cube",
    )
    data[("jardin", "cubes", "sieste")] = (
        S(
            (N, "Après la sieste, l'étendoir a séché un pan de toile."),
            (N, "Un cube, oublié, est tiède au soleil pâle."),
            (G, "Je le jette comme un dé !"),
            (N, "Le cube tape le cône. La vis se coince."),
            (N, "Nina s'immobilise. Elle écoute le bois, puis la pluie."),
            (N, "Le croissant de zeste a bougé, plus profond."),
            (F, "On le sort, s'il te plaît, sans jeter."),
            (N, "Aniss ramasse le cube. Papa lève le zeste."),
            (N, "Ils tournent, un chacun, le pichet à l'abri."),
            (P, "Le dé n'était pas un tour. La demande, si."),
            (N, "Le cube tiède sert de socle, enfin sage."),
        ),
        S(
            (N, "La toile de l'étendoir claque, puis s'arrête."),
            (M, "Dis-nous le dé, et le vrai tour."),
            (F, "Aniss a jeté. Après, il a demandé avec moi."),
            (G, "Le cube est devenu un socle, pas un dé."),
            (P, "Merci d'avoir ramassé, Aniss."),
            (N, "Le presse-agrumes sèche sur le cube tiède."),
            (N, "Le croissant de zeste sèche au bord de la caisse."),
            (N, "Une empreinte mouillée reste, où le dé a tapé."),
        ),
        "toile,cube",
        "etendoir,caisse",
        "socle",
    )
    data[("jardin", "cubes", "soir")] = (
        S(
            (N, "Au soir, la cuisine allume le seuil, un carré jaune."),
            (N, "Un vélo passe. Les cubes sont sombres, un peu froids."),
            (N, "Il reste une orange, prise dans la caisse."),
            (G, "Je construis un phare, autour du pichet !"),
            (N, "La tour penche vers la gouttière. Nina pose un cube."),
            (N, "Elle retrouve le croissant de zeste, allumé par la cuisine."),
            (F, "Le phare, s'il te plaît, plus loin de l'eau."),
            (N, "Aniss recule la tour. Ils tournent, un chacun."),
            (N, "Le filet est court. Le phare tient."),
            (M, "La dernière orange a vu le phare, et la demande."),
            (N, "Le carré jaune de la cuisine s'allonge sur la dalle."),
        ),
        S(
            (N, "Le vélo s'est tu. Le seuil garde son carré jaune."),
            (P, "Raconte le phare, jusqu'au filet."),
            (F, "On l'a reculé. On a demandé. On a tourné."),
            (G, "Mon phare n'est pas tombé dans la gouttière."),
            (M, "Merci d'avoir reculé les cubes, Aniss."),
            (N, "Le presse-agrumes sèche au pied du phare."),
            (N, "Le croissant de zeste orne le cube du sommet."),
            (N, "Dehors, la dalle brille, une dernière fois."),
        ),
        "phare,velo",
        "seuil,lampe",
        "phare",
    )

    # JARDIN + LIVRE
    data[("jardin", "livre", "matin")] = (
        S(
            (N, "Le matin, une goutte vise la page, sous l'étendoir."),
            (N, "Un oiseau parle. L'oranger du livre a peur."),
            (G, "Je lis plus fort que l'oiseau !"),
            (N, "Sa voix couvre Nina, qui veut la manivelle."),
            (N, "Nina se tait. Elle observe la vis, luisante."),
            (N, "Le croissant de zeste imite la feuille de la page."),
            (F, "Ta page, s'il te plaît, à voix basse. Après, je tourne."),
            (N, "Aniss lit bas. La goutte tombe à côté, sur le bois."),
            (N, "Nina tourne. Un filet froid naît, malgré l'orange dure."),
            (P, "L'oiseau a parlé. Vous, chacun votre tour."),
            (N, "La page est sèche. Un petit point d'eau orne le bois."),
        ),
        S(
            (N, "L'oiseau s'est tu. L'étendoir sent le papier sec."),
            (M, "Raconte la goutte qui a manqué la page."),
            (F, "Aniss a lu bas. J'ai tourné après."),
            (G, "J'ai failli crier. Nina a demandé tout bas."),
            (P, "Merci d'avoir baissé la voix, Aniss."),
            (N, "Le presse-agrumes sèche, à l'abri, vis ouverte."),
            (N, "Le croissant de zeste sert de signet, loin de la goutte."),
            (N, "Le point d'eau sèche sur le bois, comme un oubli."),
        ),
        "page,oiseau",
        "livre,etendoir",
        "goutte",
    )
    data[("jardin", "livre", "sieste")] = (
        S(
            (N, "Après la sieste, le livre sent le bois mouillé."),
            (N, "Une veine d'eau a séché au milieu de l'oranger."),
            (G, "Je gratte la veine !"),
            (N, "Nina pose sa main. Elle ne fonce pas."),
            (N, "Elle écoute la toile de l'étendoir, un clac lent."),
            (N, "Le croissant de zeste, sous la vis, a la même veine."),
            (F, "On laisse la veine, s'il te plaît. C'est son voyage."),
            (N, "Aniss lâche. Ils tournent, un chacun, le pichet à l'abri."),
            (N, "Le jus sent un peu le bois. Il est tiède."),
            (M, "La page a gardé sa veine. Vous, votre tour."),
            (N, "Sous l'étendoir, le livre respire, ouvert, sans gratter."),
        ),
        S(
            (N, "La toile s'est tue. Le livre reste au sec."),
            (P, "Montre la veine, sans la cacher."),
            (F, "On ne l'a pas grattée. On a demandé le tour."),
            (G, "C'est le voyage de la page, pas le mien."),
            (M, "Merci d'avoir lâché, Aniss."),
            (N, "Le presse-agrumes sèche près du livre."),
            (N, "Le croissant de zeste sèche le long de la veine, sans la toucher."),
            (N, "Le pichet a un goût de bois et d'orange, mêlés."),
        ),
        "veine,toile",
        "livre,bois",
        "veine",
    )
    data[("jardin", "livre", "soir")] = (
        S(
            (N, "Au soir, la cuisine allume une page, sous l'étendoir."),
            (N, "Un vélo passe. Il reste une orange."),
            (G, "Je montre l'oranger au vélo !"),
            (N, "Il avance le livre. Le vent de la rue le menace."),
            (N, "Nina le ramène. Elle retrouve le croissant de zeste."),
            (F, "Le livre, s'il te plaît, sous le toit. Puis on tourne."),
            (N, "Aniss recule. Ils tournent, un chacun, un filet court."),
            (N, "La page voit le carré jaune, pas la rue."),
            (P, "Le vélo a passé. Vous, vous avez demandé."),
            (N, "Dans la lumière, le croissant de zeste imite l'oranger."),
            (M, "La dernière orange a suffi, à l'abri."),
        ),
        S(
            (N, "Le vélo s'est tu. Le seuil garde un livre ouvert."),
            (M, "Raconte le vent, et le toit."),
            (F, "On a reculé. On a tourné après la demande."),
            (G, "L'oranger n'a pas vu la rue. Il a vu la lampe."),
            (P, "Merci d'avoir ramené le livre, Nina."),
            (N, "Le presse-agrumes sèche, vis vers la cuisine."),
            (N, "Le croissant de zeste dort sur l'oranger, comme une feuille."),
            (N, "Le pichet n'a qu'un fond, allumé par la porte."),
        ),
        "vent,page",
        "livre,seuil",
        "oranger",
    )

    # JARDIN + DINETTE
    data[("jardin", "dinette", "matin")] = (
        S(
            (N, "Le matin, les tasses sont froides, posées sur la caisse."),
            (N, "Un oiseau parle. Aniss lève sa tasse vers le toit."),
            (G, "Un peu de pluie, pour mélanger !"),
            (N, "Une goutte sale y tombe. Nina secoue la tête."),
            (N, "Elle refuse. Elle observe la vis, le croissant de zeste."),
            (F, "On vide ta tasse, s'il te plaît. Ensuite, le vrai jus."),
            (N, "Aniss verse l'eau sur la dalle. Nina tourne."),
            (N, "Un filet clair arrive, trop précieux pour la gouttière."),
            (P, "La tasse a eu son vrai tour, pas celui du toit."),
            (N, "Deux tasses reçoivent, l'une après l'autre."),
            (M, "L'oiseau a parlé. Vous, vous avez demandé."),
        ),
        S(
            (N, "L'oiseau s'est tu. Les tasses sentent l'orange, pas le toit."),
            (P, "Raconte l'eau versée, et le filet gardé."),
            (F, "On a vidé la goutte. On a demandé le jus."),
            (G, "Ma tasse a eu le vrai orange."),
            (M, "Merci d'avoir versé l'eau dehors, Aniss."),
            (N, "Le presse-agrumes sèche sur la caisse."),
            (N, "Le croissant de zeste orne la tasse d'Aniss, au bord."),
            (N, "Sur la dalle, la goutte sale sèche, oubliée."),
        ),
        "tasse,pluie",
        "dinette,caisse",
        "goutte",
    )
    data[("jardin", "dinette", "sieste")] = (
        S(
            (N, "Après la sieste, une tasse, oubliée, est tiède sur la dalle."),
            (N, "Le rideau de l'étendoir claque, lent."),
            (G, "Celle-là, c'est la mienne, elle a chauffé !"),
            (F, "Moi aussi je la veux !"),
            (N, "Deux mains sur une tasse. Le pichet penche."),
            (N, "Nina lâche. Elle retrouve le croissant sous la vis."),
            (F, "On en a deux, s'il te plaît. La tiède, et l'autre."),
            (N, "Aniss prend la tiède. Nina la fraîche. Ils tournent."),
            (N, "Le filet va d'abord dans la fraîche, puis dans la tiède."),
            (M, "Deux tasses. Deux mains. Plus de bagarre."),
            (N, "La toile se pose. Le jus a deux températures."),
        ),
        S(
            (N, "La toile s'est tue. Les deux tasses restent sur la caisse."),
            (P, "Dis-nous qui a eu le chaud, qui a eu le frais."),
            (F, "Aniss la tiède. Moi la fraîche. On a demandé."),
            (G, "J'ai lâché quand Nina a dit s'il te plaît."),
            (M, "Merci d'avoir lâché, Nina, pour parler."),
            (N, "Le presse-agrumes sèche, un peu de jus au cône."),
            (N, "Le croissant de zeste sèche dans la tasse tiède."),
            (N, "Deux ronds restent sur la dalle, où les tasses ont vécu."),
        ),
        "tasse,toile",
        "dinette,dalle",
        "tasse",
    )
    data[("jardin", "dinette", "soir")] = (
        S(
            (N, "Au soir, une tasse reflète la lampe de la cuisine."),
            (N, "Un vélo passe. Il reste une orange."),
            (G, "Je sers le vélo, comme un client !"),
            (N, "Il lève la tasse vers la rue. Nina la rattrape."),
            (N, "Elle retrouve le croissant de zeste, allumé."),
            (F, "Le client, s'il te plaît, c'est nous. Sous le toit."),
            (N, "Aniss recule. Ils tournent, un chacun, un filet court."),
            (N, "Ils se servent, face à la porte, pas face à la rue."),
            (P, "Le vélo n'avait pas commandé. Vous, si."),
            (N, "Dans la tasse, le rond de lampe tremble, orange."),
            (M, "La dernière orange a fait deux clients, à l'abri."),
        ),
        S(
            (N, "Le vélo s'est tu. Le seuil garde deux tasses."),
            (M, "Raconte le client qui n'était pas un vélo."),
            (F, "On s'est servis. On a demandé la vis."),
            (G, "Le vrai client, c'était Nina, et moi."),
            (P, "Merci d'avoir rattrapé la tasse, Nina."),
            (N, "Le presse-agrumes sèche, tourné vers la cuisine."),
            (N, "Le croissant de zeste flotte, sec, dans le reflet."),
            (N, "Le pichet n'a qu'un fond, et la dalle s'assombrit."),
        ),
        "tasse,velo",
        "dinette,seuil",
        "reflet",
    )

    # CHAMBRE + CUBES
    data[("chambre", "cubes", "matin")] = (
        S(
            (N, "Le matin, l'abat-jour aux étoiles est pâle."),
            (N, "Le plancher est froid. Un oiseau parle, derrière le volet."),
            (N, "Le quai de cubes frôle le pichet, trop près."),
            (G, "Plus haut, jusqu'aux étoiles !"),
            (N, "La tour penche. Nina pose un cube. Elle refuse."),
            (N, "Elle écoute l'horloge, puis retrouve le croissant de zeste."),
            (F, "Plus bas, s'il te plaît, sous le pichet, pas dessus."),
            (N, "Aniss baisse. Ils tournent, un chacun, malgré le froid."),
            (N, "Un filet lent arrive. L'horloge marque le tour."),
            (P, "Les étoiles ont attendu. La vis, non."),
            (N, "Le plateau tient. L'oiseau se tait."),
        ),
        S(
            (N, "L'abat-jour reste pâle. L'horloge avance, sans se presser."),
            (M, "Raconte la tour trop haute."),
            (F, "On l'a baissée. On a demandé. On a tourné."),
            (G, "Mon quai est un quai, plus un phare d'étoiles."),
            (P, "Merci d'avoir baissé les cubes, Aniss."),
            (N, "Le presse-agrumes sèche sur le plateau, vis libre."),
            (N, "Le croissant de zeste orne le cube le plus bas, sage."),
            (N, "Une étoile de l'abat-jour se pose dans le pichet, pâle."),
        ),
        "cubes,horloge",
        "plateau,abat-jour",
        "quai",
    )
    data[("chambre", "cubes", "sieste")] = (
        S(
            (N, "Après la sieste, un cube a glissé sous l'oreiller."),
            (N, "Nina a la joue chaude. Le rideau bouge."),
            (G, "C'est mon cube secret !"),
            (F, "Il nous faut, pour le quai !"),
            (N, "Deux mains sous l'oreiller. Le plateau tressaille."),
            (N, "Nina lâche. Elle retrouve le croissant sous la vis."),
            (F, "Le cube, s'il te plaît. On le pose, on ne se tire pas."),
            (N, "Aniss le sort. Ils calent le pichet. Ils tournent."),
            (N, "Le jus est tiède, un peu de pulpe au fond."),
            (M, "Le secret est devenu un quai, parce que vous avez demandé."),
            (N, "Le rideau se pose. L'oreiller a un creux, vide."),
        ),
        S(
            (N, "La chambre est tiède. L'oreiller garde un creux carré."),
            (P, "Dis-nous le cube secret, jusqu'au quai."),
            (F, "On a demandé. On n'a pas tiré l'oreiller."),
            (G, "Mon secret a calé le pichet."),
            (M, "Merci d'avoir lâché, Nina, pour parler."),
            (N, "Le presse-agrumes sèche, un peu de pulpe au cône."),
            (N, "Le croissant de zeste sèche dans le creux de l'oreiller."),
            (N, "Le pichet a deux couleurs, comme la joue de Nina."),
        ),
        "oreiller,cube",
        "chambre,pulpe",
        "secret",
    )
    data[("chambre", "cubes", "soir")] = (
        S(
            (N, "Au soir, la lampe fait un phare des cubes, sur le plateau."),
            (N, "Un vélo passe. Il reste une orange, sur le bois."),
            (G, "Le phare, c'est moi qui l'allume !"),
            (N, "Il ajoute un cube trop près de la vis."),
            (N, "Nina observe. Elle retrouve le croissant de zeste, allumé."),
            (F, "Ce cube, s'il te plaît, plus loin. Ensuite, on tourne."),
            (N, "Aniss recule le cube. Ils tournent, un chacun."),
            (N, "Le filet est court. Le phare tient, sans toucher la vis."),
            (P, "La dernière orange a eu son phare, et sa demande."),
            (N, "Une étoile de l'abat-jour tombe dans le jus, en reflet."),
            (M, "Le vélo s'éloigne. Vous, vous restez allumés."),
        ),
        S(
            (N, "Le vélo s'est tu. Le phare de cubes reste allumé."),
            (M, "Raconte le cube trop près de la vis."),
            (F, "On l'a reculé. On a demandé. On a tourné."),
            (G, "Mon phare n'a pas coincé le zeste."),
            (P, "Merci d'avoir reculé, Aniss."),
            (N, "Le presse-agrumes sèche au pied du phare."),
            (N, "Le croissant de zeste orne le cube du sommet, comme une flamme."),
            (N, "Le pichet n'a qu'un fond, et l'étoile y nage."),
        ),
        "phare,velo",
        "cubes,lampe",
        "phare",
    )

    # CHAMBRE + LIVRE
    data[("chambre", "livre", "matin")] = (
        S(
            (N, "Le matin, le livre est froid sur l'oreiller."),
            (N, "Un oiseau parle. L'oranger de la page a la même pâleur."),
            (G, "Je lis très fort, pour l'oiseau !"),
            (N, "Sa voix couvre la manivelle. Nina se tait."),
            (N, "Elle observe la vis. Le croissant de zeste est là."),
            (F, "Ta page, s'il te plaît, jusqu'au bout, tout bas."),
            (N, "Aniss lit bas. Nina tourne. Un filet froid naît."),
            (N, "Le croissant de zeste glisse en signet, dans l'oranger."),
            (P, "L'oiseau a eu le dehors. Vous, le plateau."),
            (N, "L'horloge marque le tour, sans se presser."),
            (M, "La page a fini. Le jus a commencé."),
        ),
        S(
            (N, "L'oiseau s'est tu. Le livre reste sur l'oreiller."),
            (P, "Raconte la voix trop forte, puis la voix basse."),
            (F, "Aniss a lu bas. J'ai tourné après."),
            (G, "Le zeste est un signet, maintenant."),
            (M, "Merci d'avoir baissé la voix, Aniss."),
            (N, "Le presse-agrumes sèche sur le plateau, vis libre."),
            (N, "Le croissant de zeste dort dans l'oranger, comme une feuille."),
            (N, "Une étoile pâle se pose sur la page, et s'en va."),
        ),
        "livre,oiseau",
        "oreiller,presse",
        "signet",
    )
    data[("chambre", "livre", "sieste")] = (
        S(
            (N, "Après la sieste, la page est tiède contre la joue de Nina."),
            (N, "Le rideau bouge. Une goutte du plateau a séché au coin."),
            (G, "Je tourne la page, vite !"),
            (N, "Le coin collé résiste. Nina pose sa main."),
            (N, "Elle refuse. Elle retrouve le croissant sous la vis."),
            (F, "On décolle, s'il te plaît, puis tu lis, puis je tourne."),
            (N, "Maman souffle. La page se lève. Aniss lit. Nina tourne."),
            (N, "Le jus est tiède, un peu trouble, comme la joue."),
            (P, "Le coin a eu son souffle. La vis, son tour."),
            (N, "Le rideau se pose. Le livre respire, ouvert."),
            (M, "Personne n'a déchiré. Tout le monde a demandé."),
        ),
        S(
            (N, "La chambre est tiède. La page est libre."),
            (M, "Raconte le coin collé, pas seulement le jus."),
            (F, "On a soufflé. On n'a pas tiré."),
            (G, "J'ai lu après. Nina a tourné après."),
            (P, "Merci d'avoir posé ta main, Nina."),
            (N, "Le presse-agrumes sèche, un peu de trouble au cône."),
            (N, "Le croissant de zeste sèche au coin autrefois collé."),
            (N, "Une vague blanche reste, où la joue s'était posée."),
        ),
        "page,joue",
        "livre,rideau",
        "coin",
    )
    data[("chambre", "livre", "soir")] = (
        S(
            (N, "Au soir, la lampe allume l'oranger, sur l'oreiller."),
            (N, "Un vélo passe. Il reste une orange, sur le plateau."),
            (G, "Je ferme le livre, c'est trop long !"),
            (N, "Nina retient la page. Elle ne fonce pas."),
            (N, "Elle retrouve le croissant de zeste, allumé."),
            (F, "La page, s'il te plaît, jusqu'à la fin. Après, on tourne."),
            (N, "Aniss finit. Ils tournent, un chacun, un filet court."),
            (N, "Le livre se ferme, le zeste dans le pli, comme un secret."),
            (M, "La dernière orange a attendu la dernière phrase."),
            (N, "Une étoile de l'abat-jour se mire dans le pichet."),
            (P, "Le vélo s'éloigne. La page, elle, est finie."),
        ),
        S(
            (N, "Le vélo s'est tu. Le livre est fermé, lourd d'un zeste."),
            (P, "Raconte la phrase qu'Aniss a finie."),
            (F, "On n'a pas fermé trop tôt. On a demandé."),
            (G, "J'ai fini. Après, on a pressé."),
            (M, "Merci d'avoir retenu la page, Nina."),
            (N, "Le presse-agrumes sèche, vis vers la lampe."),
            (N, "Le croissant de zeste dort dans le pli, entre deux feuilles."),
            (N, "Le pichet n'a qu'un fond, et l'étoile s'y éteint."),
        ),
        "page,velo",
        "livre,lampe",
        "pli",
    )

    # CHAMBRE + DINETTE
    data[("chambre", "dinette", "matin")] = (
        S(
            (N, "Le matin, les tasses sont froides, au pied de l'abat-jour."),
            (N, "Un oiseau parle. L'horloge fait tic, lent."),
            (G, "Restaurant du matin, j'ouvre !"),
            (N, "Il tape une tasse. Le plateau tressaille."),
            (N, "Nina ramasse. Elle retrouve le croissant sous la vis."),
            (F, "On ouvre, s'il te plaît, après un filet, pas avant."),
            (N, "Aniss attend. Nina tourne. Un filet froid naît."),
            (N, "Ils servent, l'un après l'autre, près de l'oreiller."),
            (P, "Le restaurant a ouvert, parce que la vis a parlé."),
            (N, "Une tasse, posée trop haut, frôle une étoile de tissu."),
            (M, "L'oiseau s'est tu. Vous, vous avez demandé."),
        ),
        S(
            (N, "L'horloge avance. Les tasses restent au pied de l'abat-jour."),
            (M, "Raconte l'ouverture, pas le tapage."),
            (F, "On a demandé. On a tourné. On a servi."),
            (G, "Mon restaurant a attendu le filet."),
            (P, "Merci d'avoir attendu, Aniss."),
            (N, "Le presse-agrumes sèche sur le plateau."),
            (N, "Le croissant de zeste orne la tasse du haut, près de l'étoile."),
            (N, "Le pichet a servi de carafe, pour deux petites soifs froides."),
        ),
        "tasse,horloge",
        "dinette,chambre",
        "restaurant",
    )
    data[("chambre", "dinette", "sieste")] = (
        S(
            (N, "Après la sieste, une tasse a roulé contre la joue de Nina."),
            (N, "Elle est tiède. Le rideau bouge."),
            (G, "C'est la tasse du dodo, elle est à moi !"),
            (F, "Elle a touché ma joue !"),
            (N, "Deux voix. Nina se tait. Elle observe la vis."),
            (N, "Le croissant de zeste est là, comme au début."),
            (F, "On a deux tasses, s'il te plaît. La tiède, et l'autre."),
            (N, "Aniss prend la tiède. Nina la fraîche. Ils tournent."),
            (N, "Le jus est un peu trouble, comme le réveil."),
            (M, "La joue a eu sa tasse. L'autre aussi."),
            (N, "Le rideau se pose. Le restaurant du dodo s'ouvre, enfin."),
        ),
        S(
            (N, "La chambre est tiède. Deux tasses veillent près de l'oreiller."),
            (P, "Dis-nous la tasse du dodo, et l'autre."),
            (F, "Aniss la tiède. Moi la fraîche. On a demandé."),
            (G, "J'ai parlé trop fort. Après, j'ai écouté."),
            (M, "Merci d'avoir parlé chacun, sans vous tirer la tasse."),
            (N, "Le presse-agrumes sèche, un peu de trouble au cône."),
            (N, "Le croissant de zeste sèche dans la tasse tiède, celle du dodo."),
            (N, "Un rond reste sur l'oreiller, où la tasse a dormi."),
        ),
        "tasse,joue",
        "dinette,oreiller",
        "dodo",
    )
    data[("chambre", "dinette", "soir")] = (
        S(
            (N, "Au soir, deux tasses attendent sous l'abat-jour aux étoiles."),
            (N, "Un vélo passe. Il reste une orange, sur le plateau."),
            (G, "Je sers les étoiles !"),
            (N, "Il lève la tasse trop haut. Nina la rattrape."),
            (N, "Elle retrouve le croissant de zeste, allumé par la lampe."),
            (F, "Les étoiles, s'il te plaît, après nous. D'abord le filet."),
            (N, "Aniss baisse la tasse. Ils tournent, un chacun."),
            (N, "Un filet court. Ils se servent, sous les étoiles de tissu."),
            (P, "Les étoiles n'avaient pas soif. Vous, si."),
            (N, "Dans chaque tasse, une étoile se mire, puis s'en va."),
            (M, "La dernière orange a fait deux invités, pas une chute."),
        ),
        S(
            (N, "Le vélo s'est tu. L'abat-jour garde ses étoiles."),
            (M, "Raconte la tasse trop haute."),
            (F, "On l'a baissée. On a demandé. On s'est servis."),
            (G, "Les étoiles n'ont pas bu. Nous, un peu."),
            (P, "Merci d'avoir rattrapé, Nina."),
            (N, "Le presse-agrumes sèche sous l'abat-jour, vis propre."),
            (N, "Le croissant de zeste dort dans la plus petite tasse."),
            (N, "Deux ronds de jus s'éteignent, et la chambre redevient silencieuse."),
        ),
        "tasse,etoiles",
        "dinette,abat-jour",
        "étoiles",
    )

    return data


if __name__ == "__main__":
    build()
