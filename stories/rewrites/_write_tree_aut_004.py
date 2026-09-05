#!/usr/bin/env python3
"""TREE-AUT-004 — F-NAR-019 : petit moulin de Nina, 27 fins, TTS. Pas d'apply."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "TREE-AUT-004"
N3 = LIMITS["N3"]
CHILD = "enfant-f"
TIC_PHRASES = ("tout doux", "tout calme", "tout lent")
TIC_WORDS = re.compile(r"\b(encore|déjà|deja)\b", re.I)

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=500, sentence=260, energy="warm", contour="storytelling",
        noise=0.36, emphasis="petit moulin",
        note="arc=installation; intention=émerveiller; emotion=impatience_curieuse; intensite=1; destinataire=enfant; sous_texte=le_vent_attend_le_moulin; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=900, sentence=330, energy="focused", contour="rising",
        noise=0.33, emphasis=None,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_change_la_recherche; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2,
        pause=700, sentence=320, energy="focused", contour="rising",
        noise=0.32, emphasis=None,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=il_est_sous_le_tas; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=450, sentence=280, energy="bright", contour="falling",
        noise=0.34, emphasis=None,
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=un_jouet_posé_ouvre_un_coin; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=420, sentence=250, energy="lively", contour="dynamic",
        noise=0.37, emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=elle_vide_trop_vite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0,
        pause=520, sentence=300, energy="tense", contour="dynamic",
        noise=0.34, emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=découragement_léger; intensite=2; destinataire=enfant; sous_texte=le_tas_cache_les_pales; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=560, sentence=270, energy="bright", contour="falling",
        noise=0.35, emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_et_fierté_calme; intensite=2; destinataire=enfant; sous_texte=poser_les_jouets_fait_revenir_le_moulin; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3,
        pause=900, sentence=340, energy="calm", contour="falling",
        noise=0.31, emphasis=None,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=le_vent_du_début_a_enfin_les_pales; tempo=posé; sourire=léger; respiration=ample",
    ),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    if m.get("emphasis"):
        e = esc(m["emphasis"])
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict) -> str:
    body = text
    if m.get("emphasis"):
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
    low = phrase.lower()
    for tic in TIC_PHRASES:
        if tic in low:
            raise SystemExit(f"tic {tic!r}: {phrase}")
    m = TIC_WORDS.search(low)
    if m:
        raise SystemExit(f"tic {m.group(0)!r}: {phrase}")
    return f"{role}|{phrase}"


def L(*pairs: tuple[str, str]) -> list[str]:
    out: list[str] = []
    for role, phrase in pairs:
        for sent in split_sents(phrase):
            out.append(ln(role, sent))
    return out


def voice(src: dict, lines: list[str], profile: str, sons: str = "", extra: dict | None = None) -> dict:
    m = dict(PROFILES[profile])
    extra = extra or {}
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
    out["notes"] = extra.get("notes", m["note"])
    out["night_policy"] = extra.get("night_policy", "play")
    out["locale"] = "fr-FR"
    out["voice_id"] = "fr_FR-siwis-medium"
    out.update(extra.get("fields") or {})
    return out


Q_FIELDS = {
    "expected_answer": "sous les jouets",
    "accepted_examples": (
        "sous les jouets | sous le tas | dessous | dans le tas | sous | "
        "le moulin | moulin | sous le sable | dans l'herbe"
    ),
    "retry_prompt": "Il est sous les jouets. Nina le cherche où ?",
    "engine_ok_text": "Oui, il est sous les jouets.",
    "engine_near_text": "Tu es tout près. Écoute encore l'indice.",
}


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


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str = "", extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)

    put(
        "CHK_T0000_P0000",
        L(
            ("narrateur", "Sous les tilleuls, la rue brille après la pluie."),
            ("narrateur", "L'écorce sent le bois mouillé."),
            ("narrateur", "Une coque de châtaigne craque sous un pas."),
            ("narrateur", "Le square ouvre son banc, luisant et froid."),
            ("narrateur", "Un moineau secoue une aile grise."),
            ("narrateur", "Ça sent le pain de la boulangerie, plus loin."),
            ("narrateur", "Des feuilles jaunes collent au trottoir."),
            ("narrateur", "Papa porte une caisse de bois clair."),
            ("narrateur", "La poignée de cuir frotte sa paume."),
            ("maman", "J'ai mis une poire dans le sac."),
            ("papa", "Elle reste fraîche, contre le tissu."),
            ("narrateur", "En ce moment, Nina marche entre eux."),
            ("narrateur", "Ses chaussures font un petit clac, sur les feuilles."),
            (CHILD, "Mon moulin veut le vent, tout de suite !"),
            ("maman", "Il est dans la caisse, avec les jouets ?"),
            (CHILD, "Oui, tout au fond. Je le sors."),
            ("narrateur", "Nina soulève le couvercle. Le bois sent la pluie."),
            ("narrateur", "Des cubes, un livre, une tasse. Pas de pales."),
            (CHILD, "Il est dessous. Je vide tout !"),
            ("papa", "Le square est là, avant l'école."),
            ("narrateur", "Une flaque ronde attend près du banc."),
            ("narrateur", "Le vent pousse une feuille, puis la lâche."),
            (CHILD, "Vite, qu'il tourne avant le portail."),
            ("maman", "Tu le cherches où, d'abord ?"),
        ),
        "opening",
        "pluie-legere,caisse",
        {"emphasis": "moulin"},
    )

    put(
        "CHK_T0001_P0000",
        L(
            ("narrateur", "Nina peut chercher le moulin à trois endroits."),
            ("papa", "Le bac à sable, le toboggan, ou les balançoires ?"),
        ),
        "choice",
        "",
        {"fields": {
            "option_1_label": "le bac à sable",
            "option_2_label": "le toboggan",
            "option_3_label": "les balançoires",
        }},
    )

    put(
        "CHK_T0001_P0001",
        L(
            ("narrateur", "Nina s'agenouille près du bac."),
            ("narrateur", "Le sable est froid, un peu collant."),
            ("narrateur", "Il coule entre ses doigts, chh."),
            ("narrateur", "Papa pose la caisse à côté, ouverte."),
            (CHILD, "Je vide tout. Le moulin veut le vent !"),
            ("narrateur", "Les cubes tombent. Le livre glisse, plat."),
            ("narrateur", "La petite tasse se couche, pleine de grains."),
            (CHILD, "Où est mon moulin ?"),
            ("maman", "Sur le banc, peut-être ?"),
            ("narrateur", "Nina court au banc mouillé."),
            ("narrateur", "Le bois est vide, seulement une feuille."),
            ("papa", "Dans le sac ?"),
            ("narrateur", "Maman ouvre le sac. La poire est seule."),
            (CHILD, "Il est perdu."),
            ("narrateur", "Elle plonge les deux mains dans le tas."),
            ("narrateur", "Le sable revient, et cache tout."),
            (CHILD, "Je n'y arrive pas."),
            ("maman", "Tu prends un jouet, pour voir dessous ?"),
        ),
        "action",
        "sable,enfants_parc",
        {"emphasis": "bac"},
    )
    put(
        "CHK_T0001_P0001_Q0001",
        L(
            ("narrateur", "Nina a tout versé. Le tas cache le milieu."),
            ("maman", "Le moulin, il est où ?"),
        ),
        "clue",
        "",
        {"night_policy": "skip", "fields": Q_FIELDS, "emphasis": "moulin"},
    )
    put(
        "CHK_T0001_P0001_C0001",
        L(
            ("narrateur", "Nina prend un cube du tas."),
            ("narrateur", "Elle le glisse dans la caisse. Toc."),
            ("narrateur", "Un rond de sable reparaît, tout petit."),
            (CHILD, "Pas le moulin."),
            ("maman", "Merci, je vois un coin, maintenant."),
            ("papa", "Tu regardes bien dessous ?"),
            (CHILD, "Oui, papa. Il reste trop de jouets."),
            ("narrateur", "Le tas est moins haut, mais il tient."),
            (CHILD, "Je continue, un par un."),
            ("maman", "Quel jouet, pour ouvrir le sable ?"),
        ),
        "confirm",
        "caisse,sable",
        {"emphasis": "cube"},
    )
    put(
        "CHK_T0001_P0001_T0002_P0000",
        L(
            ("narrateur", "Près du bac, trois jouets attendent d'être posés."),
            ("maman", "Les cubes, le livre, ou la dînette ?"),
        ),
        "choice",
        "",
        {"fields": {
            "option_1_label": "les cubes",
            "option_2_label": "le livre",
            "option_3_label": "la dînette",
        }},
    )

    put(
        "CHK_T0001_P0002",
        L(
            ("narrateur", "Nina pose la main sur le toboggan."),
            ("narrateur", "Le métal est frais, un peu lisse."),
            ("narrateur", "Deux marches sonnent, creuses."),
            ("narrateur", "Papa pose la caisse au pied."),
            (CHILD, "Ils glissent avec moi. Le moulin arrivera le premier !"),
            ("narrateur", "Les cubes dévalent, clic clic, trop vite."),
            ("narrateur", "Le livre tape la dernière marche."),
            ("narrateur", "La tasse roule dans l'herbe, loin."),
            (CHILD, "Mon moulin est parti aussi ?"),
            ("papa", "Sous le toboggan, peut-être ?"),
            ("narrateur", "Nina se penche. De l'ombre, pas de pales."),
            ("maman", "Près du sac ?"),
            ("narrateur", "Le sac tient la poire, rien d'autre."),
            (CHILD, "Il n'est pas là."),
            ("narrateur", "Elle soulève le tas entier, d'un coup."),
            ("narrateur", "Tout retombe. Les marches disparaissent."),
            (CHILD, "C'est trop lourd."),
            ("papa", "Tu prends un jouet, pour voir le pied ?"),
        ),
        "action",
        "metal,enfants_parc",
        {"emphasis": "toboggan"},
    )
    put(
        "CHK_T0001_P0002_Q0001",
        L(
            ("narrateur", "Le tas est au pied du toboggan."),
            ("papa", "Le moulin, il est où ?"),
        ),
        "clue",
        "",
        {"night_policy": "skip", "fields": Q_FIELDS, "emphasis": "tas"},
    )
    put(
        "CHK_T0001_P0002_C0001",
        L(
            ("narrateur", "Nina ramasse un cube au pied."),
            ("narrateur", "Elle le pose dans la caisse. Toc."),
            ("narrateur", "Une marche grise reparaît, un bout."),
            (CHILD, "Toujours pas."),
            ("papa", "Tu regardes sous le tas ?"),
            (CHILD, "Oui. Il reste le livre, et la tasse."),
            ("maman", "Le métal sonne un peu vide, maintenant."),
            ("narrateur", "Le tas penche, moins ferme."),
            (CHILD, "Je prends la suite, sans tout soulever."),
            ("papa", "Lequel, d'abord ?"),
        ),
        "confirm",
        "caisse,metal",
        {"emphasis": "marche"},
    )
    put(
        "CHK_T0001_P0002_T0002_P0000",
        L(
            ("narrateur", "Au pied du métal, trois jouets attendent."),
            ("papa", "Les cubes, le livre, ou la dînette ?"),
        ),
        "choice",
        "",
        {"fields": {
            "option_1_label": "les cubes",
            "option_2_label": "le livre",
            "option_3_label": "la dînette",
        }},
    )

    put(
        "CHK_T0001_P0003",
        L(
            ("narrateur", "Nina s'assoit sur une balançoire."),
            ("narrateur", "La chaîne est froide, un peu rêche."),
            ("narrateur", "Elle fait un cri mince, de fer."),
            ("narrateur", "Papa pose la caisse dans l'herbe."),
            (CHILD, "Les jouets viennent au vent, avec moi !"),
            ("narrateur", "Les cubes s'éparpillent sous le siège."),
            ("narrateur", "Le livre s'ouvre sur l'herbe. Une goutte y tombe."),
            ("narrateur", "La tasse se cache dans les brins."),
            (CHILD, "Mon moulin ?"),
            ("maman", "Sous la balançoire ?"),
            ("narrateur", "Nina descend, les pieds à plat."),
            ("narrateur", "L'herbe est haute, un peu mouillée. Rien."),
            ("papa", "Derrière le sac ?"),
            ("narrateur", "Le sac est fermé, la poire dedans."),
            (CHILD, "Je ne le vois pas."),
            ("narrateur", "Elle chasse les jouets du pied, trop fort."),
            ("narrateur", "Le mont s'étale. L'herbe cache davantage."),
            (CHILD, "Ça va plus mal."),
            ("maman", "Tu ramasses par quoi, dans l'herbe ?"),
        ),
        "action",
        "chaine,herbe",
        {"emphasis": "balançoire"},
    )
    put(
        "CHK_T0001_P0003_Q0001",
        L(
            ("narrateur", "L'herbe cache les jouets, et le vent passe."),
            ("maman", "Le moulin, il est où ?"),
        ),
        "clue",
        "",
        {"night_policy": "skip", "fields": Q_FIELDS, "emphasis": "herbe"},
    )
    put(
        "CHK_T0001_P0003_C0001",
        L(
            ("narrateur", "Nina prend un cube dans l'herbe."),
            ("narrateur", "Elle le met dans la caisse. Toc."),
            ("narrateur", "Un brin d'herbe se redresse, seul."),
            (CHILD, "Ce n'est pas lui."),
            ("maman", "Tu regardes sous le mont ?"),
            (CHILD, "Oui. Il reste le livre, et la tasse."),
            ("papa", "La chaîne ne crie plus, pour l'instant."),
            ("narrateur", "Le siège de la balançoire est vide."),
            (CHILD, "Je ramasse, sans pousser avec le pied."),
            ("maman", "Tu prends quoi, dans l'herbe ?"),
        ),
        "confirm",
        "caisse,herbe",
        {"emphasis": "brin"},
    )
    put(
        "CHK_T0001_P0003_T0002_P0000",
        L(
            ("narrateur", "Dans l'herbe, trois jouets attendent d'être posés."),
            ("maman", "Les cubes, le livre, ou la dînette ?"),
        ),
        "choice",
        "",
        {"fields": {
            "option_1_label": "les cubes",
            "option_2_label": "le livre",
            "option_3_label": "la dînette",
        }},
    )

    t2 = t2_scenes()
    t2_q = {
        ("bac", "cubes"): "Les cubes ont ouvert un coin de sable. Ensuite ?",
        ("bac", "livre"): "Le livre a du sable sur la couverture. Ensuite ?",
        ("bac", "dinette"): "La tasse a bu du sable. Ensuite ?",
        ("tobo", "cubes"): "Les cubes coincés ont bougé. Ensuite ?",
        ("tobo", "livre"): "Le livre a quitté la marche. Ensuite ?",
        ("tobo", "dinette"): "La tasse a quitté l'herbe. Ensuite ?",
        ("balan", "cubes"): "Les cubes ont quitté le pied. Ensuite ?",
        ("balan", "livre"): "Le livre a quitté la goutte. Ensuite ?",
        ("balan", "dinette"): "La dînette a quitté les brins. Ensuite ?",
    }
    lieu_key = {"1": "bac", "2": "tobo", "3": "balan"}
    toy_key = {"1": "cubes", "2": "livre", "3": "dinette"}
    wind_key = {"1": "banc", "2": "caisse", "3": "chemin"}

    for li in "123":
        for ty in "123":
            lieu, toy = lieu_key[li], toy_key[ty]
            lines, sons, emph = t2[(lieu, toy)]
            cid = f"CHK_T0001_P000{li}_T0002_P000{ty}"
            put(cid, lines, "obstacle", sons, {"emphasis": emph})
            put(
                f"{cid}_T0003_P0000",
                L(
                    ("narrateur", t2_q[(lieu, toy)]),
                    ("papa", "Le banc, la caisse, ou le chemin ?"),
                ),
                "choice",
                "",
                {"fields": {
                    "option_1_label": "le banc",
                    "option_2_label": "la caisse",
                    "option_3_label": "le chemin",
                }},
            )

    scenes = t3_scenes()
    for li in "123":
        for ty in "123":
            for wi in "123":
                lieu, toy, wind = lieu_key[li], toy_key[ty], wind_key[wi]
                passage, ending, s3, se, emph = scenes[(lieu, toy, wind)]
                base = f"CHK_T0001_P000{li}_T0002_P000{ty}_T0003_P000{wi}"
                put(base, passage, "resolution", s3, {"emphasis": emph})
                put(f"{base}_F0001", ending, "ending", se, {"emphasis": "pales"})

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

    t2_only = [
        out_chunks[c["chunk_id"]]["text"]
        for c in src["chunks"]
        if c["kind"] == "passage" and "_T0002_P000" in c["chunk_id"] and "T0003" not in c["chunk_id"]
    ]
    if len(t2_only) != 9 or len(set(t2_only)) != 9:
        raise SystemExit(f"T2 distincts: {len(set(t2_only))}/{len(t2_only)}")

    merged = dict(src)
    merged["fil_rouge"] = (
        "Après la pluie, rue des tilleuls, Nina veut faire tourner son petit moulin "
        "avant le portail de l'école. Elle vide la caisse trop vite : le moulin disparaît. "
        "Banc, sac, poire : rien. Creuser, soulever le tas, chasser du pied : ça empire. "
        "Bac, toboggan ou balançoires changent l'obstacle. Cubes, livre ou dînette "
        "changent la manière de dégager les pales. Banc, caisse ou chemin changent "
        "où le vent les prend. Les jouets rentrent. Le moulin tourne. Ils reprennent le trottoir."
    )
    merged["title"] = "Le petit moulin de Nina"
    merged["characters"] = "Nina, papa, maman"
    merged["setting"] = "rue des tilleuls après la pluie, square, caisse de bois, chemin de l'école"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])
    counts = [sum(words(out_chunks[i]["text"]) for i in path_ids(a, b, c))
              for a in (1, 2, 3) for b in (1, 2, 3) for c in (1, 2, 3)]
    if min(counts) < 380:
        raise SystemExit(f"chemin trop court: min {min(counts)}")
    tts_ok = all(c.get("text_xai_tags") and c.get("notes") and c.get("style_energy") for c in merged["chunks"])
    if not tts_ok:
        raise SystemExit("TTS incomplet")
    (ROOT / SID / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    relecture(
        SID,
        "Le petit moulin de Nina",
        (
            "Nina veut le vent pour son moulin avant l'école. Elle vide la caisse : pales perdues. "
            "Première idée échoue (banc vide, poire seule, tas trop lourd, pied qui étale). "
            "T1 bac / toboggan / balançoires : trois obstacles. "
            "T2 cubes / livre / dînette : trois manières de dégager. "
            "T3 banc / caisse / chemin : trois vents. 27 fins : pales + image unique du début."
        ),
        (
            "Reprise F-NAR-019 P1. T3 couleurs → banc/caisse/chemin (l'action change). "
            "Plus de refrain ranger / après le jeu / tout doux / encore / déjà. "
            "Un merci vécu (coin de sable). Question adulte. "
            "27 fins distinctes, 27 T3, 9 T2. TTS profils opening/choice/clue/confirm/"
            "action/obstacle/resolution/ending. "
            f"N3 ≤ 16. Chemins {min(counts)}–{max(counts)} mots, moy {sum(counts)//27}. "
            "check() OK. Pas d'apply."
        ),
    )
    print(f"wrote {SID} {len(merged['chunks'])} chunks  chemins {min(counts)}-{max(counts)}")


def t2_scenes() -> dict[tuple[str, str], tuple]:
    N, E, P, M = "narrateur", CHILD, "papa", "maman"
    data = {}
    data[("bac", "cubes")] = (
        L(
            (N, "Les cubes sont sablés, un peu rudes, au milieu du bac."),
            (E, "Je refais une tour, vite. Le moulin attendra."),
            (N, "Nina empile deux cubes. Clic. Le troisième penche."),
            (N, "La tour tombe. Le sable saute, et recouvre le tas."),
            (P, "La tour cache le fond. Tu la poses où ?"),
            (E, "Dans la caisse. Un par un."),
            (N, "Elle glisse le premier. Toc. Puis le second, sablé."),
            (M, "Tu vois le sable, maintenant ?"),
            (E, "Un peu. Pas les pales."),
            (N, "Un troisième cube reste au milieu, collé."),
            (N, "Nina le soulève. Rien que du sable froid."),
            (E, "Il est plus bas."),
        ),
        "cubes,sable",
        "tour",
    )
    data[("bac", "livre")] = (
        L(
            (N, "Le livre a du sable sur la couverture, une croûte beige."),
            (E, "Je l'essuie. Il y a une lune, dessus."),
            (N, "Nina passe la main, trop vite. Des grains partent, chh."),
            (N, "Deux pages collent. Elle tire. Un petit bruit de papier."),
            (M, "Tu le mets où, ce livre ?"),
            (E, "Dans la caisse, fermé."),
            (N, "Elle referme. L'image de lune disparaît."),
            (N, "Le livre glisse dans la caisse. Toc, sourd."),
            (P, "Le bac est plus vide ?"),
            (E, "Un coin, oui. Sous le livre, du sable plat."),
            (N, "Pas de bois. Pas de pales."),
            (E, "Il est plus loin, plus bas."),
        ),
        "pages,sable",
        "livre",
    )
    data[("bac", "dinette")] = (
        L(
            (N, "La tasse est froide, de travers, pleine de sable mouillé."),
            (N, "Une soucoupe est à côté, sablée, comme une petite lune."),
            (E, "Je la vide dans le bac. Pas dans mes mains."),
            (N, "Le sable retourne au bac, un filet froid."),
            (N, "Nina pose la tasse sur la soucoupe. Ça cliquette."),
            (P, "Tu les mets dans la caisse ?"),
            (E, "Oui. La tasse d'abord."),
            (N, "Toc. La soucoupe suit, un peu de sable au bord."),
            (M, "Tu as regardé dessous ?"),
            (E, "Sous la tasse, un rond. Pas de pales."),
            (N, "Un rond de bac reparaît, plus net."),
            (E, "Le moulin est plus loin."),
        ),
        "tasse,sable",
        "tasse",
    )
    data[("tobo", "cubes")] = (
        L(
            (N, "Les cubes attendent au pied du métal, coincés sous la marche."),
            (E, "Ils sont collés. Je tire fort."),
            (N, "Nina tire. Les cubes sautent, clic, et s'éparpillent."),
            (N, "Un cube roule sous la dernière marche, plus loin."),
            (P, "Trop fort. Tu les prends un par un ?"),
            (E, "Oui. Celui-là, puis l'autre."),
            (N, "Elle sépare deux cubes collés. Clic. Toc, dans la caisse."),
            (M, "La marche reparaît ?"),
            (E, "La dernière, un peu. Pas les pales."),
            (N, "Deux cubes restent, l'un sur l'autre, contre le pied."),
            (N, "Nina les décroche, sans tirer. Elle les pose."),
            (E, "Il est sous le reste."),
        ),
        "cubes,metal",
        "marche",
    )
    data[("tobo", "livre")] = (
        L(
            (N, "Le livre est contre la dernière marche, une page un peu pliée."),
            (N, "Un brin d'herbe est pris dans le papier."),
            (E, "Je chasse la feuille, puis je ferme."),
            (N, "Nina chasse le brin du bout des doigts."),
            (N, "Elle aplatit la page, tout plat, contre le métal froid."),
            (M, "Il rentre ?"),
            (E, "Oui, tout plat, dans la caisse."),
            (N, "Le livre glisse. Toc. L'ombre du pied s'ouvre."),
            (P, "Sous le livre, tu vois ?"),
            (E, "L'herbe, et l'ombre. Pas de bois."),
            (N, "Pas de pales. Le métal sonne, un peu vide."),
            (E, "Il est plus bas, sous le tas."),
        ),
        "pages,metal",
        "page",
    )
    data[("tobo", "dinette")] = (
        L(
            (N, "La tasse a roulé dans l'herbe basse, loin du pied."),
            (N, "La soucoupe est plus près, un peu tordue, sous la marche."),
            (E, "Je les rattrape. Elles se sont séparées."),
            (N, "Nina prend la tasse, puis la soucoupe froide."),
            (N, "Elle les réunit. Ça cliquette, fin, comme une petite cloche."),
            (P, "Dans la caisse, les deux ?"),
            (E, "Oui, papa. Ensemble."),
            (N, "Toc. Toc. Le pied du toboggan est plus net."),
            (M, "Tu as regardé sous la tasse ?"),
            (E, "De l'herbe mouillée. Pas de pales."),
            (N, "Un trou d'herbe reste, rond, là où la tasse était."),
            (E, "Le moulin n'est pas là. Il est sous le fond."),
        ),
        "tasse,herbe",
        "soucoupe",
    )
    data[("balan", "cubes")] = (
        L(
            (N, "Les cubes sont dans l'herbe, sous le siège de la balançoire."),
            (E, "J'en mets un sur le siège, pour jouer un peu."),
            (N, "Le cube glisse. La chaîne crie. Le cube tombe dans l'herbe."),
            (P, "Le siège n'est pas une caisse. Tu le poses où ?"),
            (E, "Dans la caisse. Un par un, dans l'herbe."),
            (N, "Nina cherche avec les doigts. Un cube, puis un autre."),
            (N, "Clic, contre le bois. Toc."),
            (M, "L'herbe se redresse ?"),
            (E, "Un peu. Les pales, non."),
            (N, "Un cube reste coincé contre un pied de fer."),
            (N, "Nina le dégage, sans le jeter. Elle le met."),
            (E, "Plus bas, sous l'herbe."),
        ),
        "cubes,chaine",
        "siège",
    )
    data[("balan", "livre")] = (
        L(
            (N, "Le livre est ouvert sur l'herbe. Une page boit une goutte."),
            (E, "Je souffle. Ffff. La goutte bouge, puis reste."),
            (N, "Nina souffle trop fort. La page claque, un peu froissée."),
            (M, "Tu le fermes, avant que l'herbe le mange ?"),
            (E, "Oui, puis la caisse."),
            (N, "Elle referme, tout plat. Une ride reste sur le papier."),
            (N, "Le livre rentre. Toc. Des brins se relèvent."),
            (P, "Sous le livre ?"),
            (E, "Des brins, pas de bois."),
            (N, "La chaîne bouge d'un souffle, puis s'arrête."),
            (E, "Il est plus bas, dans l'herbe."),
            (N, "Le siège reste vide, un peu humide."),
        ),
        "pages,goutte",
        "goutte",
    )
    data[("balan", "dinette")] = (
        L(
            (N, "La tasse s'est cachée dans les brins, presque verte."),
            (N, "La soucoupe est froide, un peu verte aussi, collée d'herbe."),
            (E, "Je la sors de l'herbe. Elle a mangé des brins."),
            (N, "Nina pose la tasse. Ça cliquette, un peu sourd, dans l'herbe."),
            (P, "Dans la caisse ?"),
            (E, "Oui, les deux. Je chasse l'herbe d'abord."),
            (N, "Elle chasse un brin. Toc. Un trou d'herbe reste, rond."),
            (M, "Tu as regardé dans le trou ?"),
            (E, "Pas de pales."),
            (N, "Le siège de la balançoire est vide, au-dessus."),
            (E, "Le moulin est plus bas, sous le fond."),
            (N, "La chaîne ne crie plus. L'herbe sent le froid."),
        ),
        "tasse,herbe",
        "brins",
    )
    return data


def t3_scenes() -> dict[tuple[str, str, str], tuple]:
    N, E, P, M = "narrateur", CHILD, "papa", "maman"

    def S(*rows):
        return L(*rows)

    data: dict[tuple[str, str, str], tuple] = {}

    # --- BAC + CUBES ---
    data[("bac", "cubes", "banc")] = (
        S(
            (N, "Nina glisse le dernier cube. Clic, puis toc."),
            (N, "Sous le cube, un bout de bois, collé de sable."),
            (E, "Mon moulin !"),
            (N, "Elle le soulève. Une pale est un peu lourde, de grains."),
            (N, "Nina court au banc mouillé, le bois contre la poitrine."),
            (N, "Elle le pose. Une goutte du tilleul touche une pale."),
            (E, "Tourne, maintenant !"),
            (N, "La goutte pèse. Les pales hésitent, puis prennent l'air."),
            (P, "Le banc lui donne le vent des tilleuls."),
            (M, "Le cube est rentré. Les pales, elles, travaillent."),
        ),
        S(
            (N, "Ils quittent le bac. Le rond de sable reste net."),
            (E, "Il a eu peur de la goutte, puis il a tourné."),
            (P, "Tu as dégagé le bois, cube après cube."),
            (N, "Les cubes dorment dans la caisse, un peu sablés."),
            (N, "Le moulin reste un moment sur le banc, heureux."),
            (N, "Le moineau picore une miette, tout près des pales."),
        ),
        "cube,banc",
        "vent,oiseaux",
        "banc",
    )
    data[("bac", "cubes", "caisse")] = (
        S(
            (N, "Nina glisse le dernier cube. Toc, contre le bois."),
            (N, "Sous le cube, les pales sont plates, sablées."),
            (E, "Te voilà !"),
            (N, "Elle pousse le couvercle. Toc. Le cuir de la poignée se tait."),
            (N, "Nina pose le moulin sur le couvercle, un peu trop près du bord."),
            (N, "Le moulin penche. Papa rattrape la caisse, sans parler fort."),
            (E, "Au milieu, comme une maison."),
            (N, "Elle le recule. Le vent du square prend les pales."),
            (M, "La caisse porte les jouets, et le vent, dessus."),
            (N, "Les pales tournent, au-dessus des cubes endormis."),
        ),
        S(
            (N, "Papa soulève la caisse. Le moulin tient, au centre."),
            (E, "Les cubes sont dessous. Lui, il a le ciel."),
            (P, "Tu as fermé, puis tu as choisi le milieu."),
            (N, "La poignée de cuir ne frotte plus. Elle se repose."),
            (N, "Ils reprennent le trottoir, la caisse entre eux."),
            (N, "Le moulin tourne au-dessus du bois clair, en petits ronds."),
        ),
        "couvercle,cubes",
        "caisse,vent",
        "couvercle",
    )
    data[("bac", "cubes", "chemin")] = (
        S(
            (N, "Nina glisse le dernier cube. Un rond de bac s'ouvre."),
            (N, "Sous le cube, le bois du moulin, froid et sablé."),
            (E, "Je le tiens, moi, sur le chemin !"),
            (N, "Elle essuie une pale contre sa manche. Des grains tombent."),
            (N, "Nina lève le moulin. Ses chaussures font clac, sur les feuilles."),
            (N, "Le premier pas est trop vite. Les pales se cognent à sa joue."),
            (P, "Un pas, puis le vent. Pas les deux d'un coup."),
            (N, "Elle ralentit. Le vent de la rue entre dans le bois."),
            (M, "Les pales ont trouvé le clac, et le clac les suit."),
            (E, "Il tourne, jusqu'au portail."),
        ),
        S(
            (N, "Ils quittent le square. Le bac reste un rond propre."),
            (E, "Les cubes sont rentrés. Le moulin marche avec moi."),
            (P, "Tu as ralenti, et le vent a pu entrer."),
            (N, "La caisse ferme les cubes, sablés, au fond."),
            (N, "Le pain de la boulangerie revient, une odeur chaude."),
            (N, "Les pales répondent au clac des chaussures, sur les feuilles."),
        ),
        "pas,moulin",
        "trottoir,vent",
        "chemin",
    )

    # --- BAC + LIVRE ---
    data[("bac", "livre", "banc")] = (
        S(
            (N, "Nina glisse le livre, tout plat. Toc, sourd."),
            (N, "Sous le livre, les pales sont plates, marquées d'une lune de sable."),
            (E, "Il était sous la lune !"),
            (N, "Elle le porte au banc. Le bois du banc est plus froid que le sien."),
            (N, "Elle pose le moulin. Une pale colle, un instant, au banc mouillé."),
            (M, "Attends que le bois lâche la pale, puis souffle."),
            (N, "Nina attend. La pale se décolle, toute seule."),
            (N, "Le vent des tilleuls la prend, puis les autres."),
            (P, "Le livre dort. Le banc, lui, travaille."),
            (E, "Tourne, loin des pages."),
        ),
        S(
            (N, "Ils laissent le bac. Un coin de sable reste lisse."),
            (E, "Il était sous le livre, plat comme une page."),
            (M, "Tu as attendu que le banc rende la pale."),
            (N, "Le livre dort dans la caisse, une ride de sable au bord."),
            (N, "Le moulin reste sur le banc, plus libre que la lune."),
            (N, "Une page sèche au soleil, à côté du bois qui tourne."),
        ),
        "livre,banc",
        "pages,vent",
        "lune",
    )
    data[("bac", "livre", "caisse")] = (
        S(
            (N, "Nina glisse le livre. Sous la couverture, un bout de pale."),
            (E, "Je t'ai trouvé, sous la lune."),
            (N, "Elle pose le livre au fond, puis pousse le couvercle."),
            (N, "Nina met le moulin sur le bois. Une pale frotte le livre, en dessous, non."),
            (N, "Le couvercle est fermé. Le livre est à l'abri."),
            (P, "Lui, dessus. Les pages, dessous. Chacun sa place."),
            (N, "Le vent prend les pales, au-dessus du cuir."),
            (E, "Il n'écrase plus le livre."),
            (M, "Le sable reste au bac. Le vent, sur la caisse."),
            (N, "Les pales tournent, sans toucher le papier."),
        ),
        S(
            (N, "Papa porte la caisse. Le moulin tient, au milieu du couvercle."),
            (E, "Le livre dort. Lui, il a le vent."),
            (P, "Tu as séparé les pages et les pales."),
            (N, "Ils reprennent la rue des tilleuls, un peu plus sèche."),
            (N, "Le sac tape le dos, toc toc, sans déranger le bois."),
            (N, "Le livre dort sous le couvercle. Le vent a le dessus."),
        ),
        "livre,couvercle",
        "caisse,pages",
        "pages",
    )
    data[("bac", "livre", "chemin")] = (
        S(
            (N, "Nina glisse le livre. Les pales apparaissent, plates, sablées."),
            (E, "Je le prends pour la rue !"),
            (N, "Elle souffle le sable d'une pale. Ffff. Un grain part."),
            (N, "Nina lève le moulin. Le premier pas fait clac, trop fort."),
            (N, "Les pales se heurtent. Elle serre trop le bâton."),
            (M, "Lâche un peu. Le vent a besoin de place."),
            (N, "Nina desserre les doigts. L'air de la rue entre."),
            (P, "Le livre est rentré. Le chemin, c'est pour lui."),
            (E, "Il tourne, à côté du sac."),
            (N, "Les pales coupent l'odeur du pain, en petits ronds."),
        ),
        S(
            (N, "Ils quittent le bac. Le sable ne coule plus."),
            (E, "Le livre est fermé. Le moulin marche."),
            (M, "Tu as desserré, et l'air a pu passer."),
            (N, "La caisse porte le livre, plat, au fond."),
            (N, "La clochette de la boulangerie tinte, une fois, loin."),
            (N, "L'odeur du pain revient, et le moulin la coupe en ronds."),
        ),
        "pas,livre",
        "boulangerie,vent",
        "pain",
    )

    # --- BAC + DINETTE ---
    data[("bac", "dinette", "banc")] = (
        S(
            (N, "Nina glisse la dernière tasse. Ça cliquette, puis toc."),
            (N, "Sous la tasse, le moulin est sablé, un peu lourd."),
            (E, "Il avait bu du sable, lui aussi !"),
            (N, "Elle le secoue, un coup. Des grains tombent sur le bac."),
            (N, "Nina le pose sur le banc. Une pale cliquette contre le bois, puis se tait."),
            (P, "Le banc n'est pas une tasse. Il tient, sans chanter."),
            (N, "Le vent des tilleuls arrive, plus large que le bac."),
            (E, "Tourne, sans le sable."),
            (M, "La dînette est rentrée. Le banc a le vent."),
            (N, "Les pales tournent. Un grain quitte le bois, et tombe."),
        ),
        S(
            (N, "Ils laissent le bac. La tasse ne chante plus."),
            (E, "Il était sous la tasse, plein de grains."),
            (P, "Tu l'as secoué, puis tu l'as posé."),
            (N, "La soucoupe dort dans la caisse, propre, ou presque."),
            (N, "Le moulin reste sur le banc, plus léger."),
            (N, "Un grain de sable quitte la tasse, loin du banc."),
        ),
        "tasse,banc",
        "vaisselle,vent",
        "tasse",
    )
    data[("bac", "dinette", "caisse")] = (
        S(
            (N, "Nina glisse la soucoupe. Sous le rond, un bout de pale."),
            (E, "Il était dans l'assiette !"),
            (N, "Elle pose la soucoupe au fond, loin du couvercle."),
            (N, "Nina ferme. Elle met le moulin au milieu, trop près d'une rainure."),
            (N, "Une pale racle le bois. Un petit cri sec."),
            (M, "Un peu plus haut, sur le plat du couvercle."),
            (N, "Nina recule le bâton. Le vent prend, sans racle."),
            (P, "La dînette dort. Lui, il a la pluie du square, dessus."),
            (E, "Il ne cliquette plus. Il tourne."),
            (N, "Les pales rident le couvercle, sans le mordre."),
        ),
        S(
            (N, "Papa lève la caisse. Rien ne chante, sauf le vent."),
            (E, "La tasse est en bas. Le moulin, en haut."),
            (M, "Tu as choisi le plat du bois, pas la rainure."),
            (N, "Ils reprennent le trottoir. La poire roule un peu, dans le sac."),
            (N, "La soucoupe ne cliquette plus, sous les pales."),
            (N, "Le moulin tourne au-dessus de la dînette endormie."),
        ),
        "soucoupe,couvercle",
        "caisse,vaisselle",
        "rainure",
    )
    data[("bac", "dinette", "chemin")] = (
        S(
            (N, "Nina glisse la tasse. Un rond de bac s'ouvre, net."),
            (N, "Sous la tasse, le petit moulin, sablé jusqu'au bâton."),
            (E, "Je le porte, et la tasse reste !"),
            (N, "Elle chasse un grain de la pale, du pouce."),
            (N, "Nina marche. Le sac tape le dos, toc, trop près du bois."),
            (N, "Les pales se cognent au tissu. Elle écarte le sac d'un coup d'épaule."),
            (P, "Le sac a la poire. Toi, tu as le vent."),
            (N, "L'air de la rue entre. Les pales partent."),
            (M, "La dînette est rentrée. Le chemin chante autre chose."),
            (E, "Il tourne, à côté du toc du sac."),
        ),
        S(
            (N, "Ils quittent le sable. Le bac reste un rond froid."),
            (E, "La tasse ne cliquette plus. Le moulin, si."),
            (P, "Tu as écarté le sac, et le vent a eu la place."),
            (N, "La caisse ferme la dînette, un peu sablée."),
            (N, "Le sac tape le dos, toc, et les pales suivent."),
            (N, "Une feuille jaune se décolle du trottoir, sous leurs pas."),
        ),
        "sac,tasse",
        "pas,sac",
        "sac",
    )

    # --- TOBO + CUBES ---
    data[("tobo", "cubes", "banc")] = (
        S(
            (N, "Nina glisse le dernier cube du pied. Clic, puis toc."),
            (N, "Sous les cubes, entre la marche et l'herbe, le bois."),
            (E, "Il avait glissé, lui aussi !"),
            (N, "Elle le dégage du métal. Une pale est un peu froide, comme la marche."),
            (N, "Nina le porte au banc, loin du toboggan."),
            (N, "Elle le pose. Le banc ne sonne pas, contrairement aux marches."),
            (E, "Ici, pas de clic. Que le vent."),
            (N, "Les pales hésitent, puis prennent l'air du square."),
            (P, "Les cubes sont rentrés. Le banc n'est pas une marche."),
            (M, "Le métal sèche, vide, derrière vous."),
        ),
        S(
            (N, "Ils quittent le toboggan. Les marches restent grises."),
            (E, "Il était coincé, comme les cubes."),
            (P, "Tu l'as dégagé du métal, sans tirer trop fort."),
            (N, "Les cubes dorment dans la caisse, un peu d'herbe au bord."),
            (N, "Le moulin reste sur le banc, loin du clic."),
            (N, "Le toboggan sèche, gris et vide, derrière le banc."),
        ),
        "cube,metal",
        "banc,metal",
        "marche",
    )
    data[("tobo", "cubes", "caisse")] = (
        S(
            (N, "Nina glisse le dernier cube. La dernière marche reparaît, entière."),
            (N, "Sous les cubes du pied, le bois, un peu cabossé."),
            (E, "Sur la caisse, il ne glissera plus !"),
            (N, "Elle pousse le couvercle. Toc. Le cuir se tait."),
            (N, "Nina pose le moulin. La caisse bouge d'un pas de papa."),
            (N, "Le moulin glisse vers le bord, comme sur le toboggan."),
            (P, "J'arrête mes pieds. Toi, tu le mets au creux."),
            (N, "Nina le recule au creux. Les pales prennent, sans glisser."),
            (M, "Les marches sont vides. Le couvercle, lui, chante le vent."),
            (E, "Il tient. Pas comme tout à l'heure."),
        ),
        S(
            (N, "Papa marche plus lent, la caisse bien à plat."),
            (E, "Les cubes sont en bas. Lui, il ne dévale plus."),
            (P, "Tu as choisi le creux, pas le bord."),
            (N, "Les marches restent muettes. Le couvercle chante."),
            (N, "Ils quittent le métal. L'herbe se redresse au pied."),
            (N, "Le moulin tourne au-dessus des cubes, sans dévaler."),
        ),
        "couvercle,cubes",
        "caisse,metal",
        "creux",
    )
    data[("tobo", "cubes", "chemin")] = (
        S(
            (N, "Nina glisse le dernier cube. L'ombre du pied s'ouvre."),
            (N, "Entre la marche et l'herbe, les pales, un peu tordues."),
            (E, "Je le redresse, et on marche !"),
            (N, "Elle plie une pale, tout doucement, vers le ciel."),
            (N, "Nina lève le moulin. Le premier pas imite le dévalement, trop vite."),
            (N, "Les pales s'affolent. Elle s'arrête, un pied en l'air."),
            (M, "Le chemin n'est pas un toboggan. Un pas, puis un pas."),
            (N, "Nina pose le pied. Le vent de la rue entre, plus large."),
            (P, "Les cubes sont rentrés. Tes pieds, maintenant, sont sages."),
            (E, "Il tourne, sans dévaler."),
        ),
        S(
            (N, "Ils quittent le métal. Une voiture passe, bas, loin."),
            (E, "Les cubes ne dévalent plus. Le moulin non plus."),
            (M, "Tu as arrêté le pied, et le vent a pu entrer."),
            (N, "La caisse ferme les cubes, contre le livre et la tasse."),
            (N, "Le trottoir sèche par plaques, sous les pales."),
            (N, "Les pales ignorent la voiture, et gardent la rue."),
        ),
        "pas,cubes",
        "rue,metal",
        "pas",
    )

    # --- TOBO + LIVRE ---
    data[("tobo", "livre", "banc")] = (
        S(
            (N, "Nina glisse le livre, tout plat. Entre la marche et le livre, les pales."),
            (E, "Il était collé au métal !"),
            (N, "Elle le décolle. Une pale a gardé le froid de la marche."),
            (N, "Nina le porte au banc. Le bois du banc est plus tendre."),
            (N, "Elle le pose. Une pale, trop pliée, refuse le vent."),
            (P, "On la redresse, comme la page, tout à l'heure."),
            (N, "Nina redresse la pale. Le vent du square la prend."),
            (E, "La page, et la pale, toutes les deux plates."),
            (M, "Le livre est rentré. Le banc a le bois qui tourne."),
            (N, "Les pales partent, loin du métal."),
        ),
        S(
            (N, "Ils laissent le toboggan. La dernière marche sèche."),
            (E, "Il était sous le livre, froid comme la marche."),
            (P, "Tu as redressé la pale, comme la page."),
            (N, "Le livre dort dans la caisse, une ride moins forte."),
            (N, "Le moulin reste sur le banc, plus chaud que le métal."),
            (N, "La page pliée se repose, loin du métal, près du vent."),
        ),
        "livre,banc",
        "pages,metal",
        "pale",
    )
    data[("tobo", "livre", "caisse")] = (
        S(
            (N, "Nina glisse le livre. Les pales apparaissent contre le métal."),
            (E, "Sur la caisse, il n'aura plus de marche."),
            (N, "Elle pose le livre au fond, la page pliée vers le bas."),
            (N, "Nina ferme. Elle met le moulin. Une pale racle le couvercle, trop basse."),
            (M, "Un peu plus haut. Le bois de la caisse n'est pas une marche."),
            (N, "Nina lève le bâton. L'air passe sous les pales."),
            (P, "Le livre est à l'abri. Lui, il a le dessus."),
            (E, "Il ne tape plus, comme tout à l'heure."),
            (N, "Les pales tournent, au-dessus du papier endormi."),
            (N, "Le bois de la caisse sent le square, sous le moulin."),
        ),
        S(
            (N, "Papa porte la caisse, loin du toboggan."),
            (E, "Le livre ne tape plus la marche. Le moulin non plus."),
            (M, "Tu as levé le bâton, et l'air a pu passer."),
            (N, "Ils reprennent les tilleuls. Une feuille verte tremble au bord."),
            (N, "Le bois de la caisse sent le square, sous le moulin."),
            (N, "Les pales tournent, sans le bruit du métal."),
        ),
        "livre,couvercle",
        "caisse,pages",
        "bâton",
    )
    data[("tobo", "livre", "chemin")] = (
        S(
            (N, "Nina glisse le livre. Les pales, un peu pliée, quittent l'ombre."),
            (E, "Je le tiens, et on va à l'école !"),
            (N, "Elle aplatit une pale, comme elle a aplati la page."),
            (N, "Nina marche. Le clac des chaussures imite trop les marches."),
            (N, "Les pales s'emballent. Elle pose un pied, puis l'autre, plus lent."),
            (P, "Le chemin est long, pas creux. Il a le temps."),
            (N, "Le vent de la rue entre, plus large que le square."),
            (E, "Il tourne, sans taper de marche."),
            (M, "Le livre est plat, au fond. Tes pas, aussi, se sont aplatis."),
            (N, "Les pales coupent l'air du trottoir, plaque après plaque."),
        ),
        S(
            (N, "Ils quittent le métal. Le square reste derrière, plus petit."),
            (E, "La page est rentrée. Le moulin marche."),
            (P, "Tes pas se sont aplatis, comme le livre."),
            (N, "La caisse ferme le livre, loin des marches."),
            (N, "Le vent pousse une feuille verte, puis la lâche."),
            (N, "Le trottoir sèche par plaques, sous les pales."),
        ),
        "pas,livre",
        "trottoir,pages",
        "plaques",
    )

    # --- TOBO + DINETTE ---
    data[("tobo", "dinette", "banc")] = (
        S(
            (N, "Nina glisse la dernière tasse. Dans l'herbe de la tasse, le moulin."),
            (E, "Il avait roulé, comme elle !"),
            (N, "Elle le sort des brins. Une pale a un peu d'herbe, collée."),
            (N, "Nina chasse l'herbe, puis court au banc."),
            (N, "Elle pose le moulin. Une pale cliquette contre le banc, comme la tasse."),
            (M, "Le banc n'est pas une soucoupe. Pose, puis attends le vent."),
            (N, "Nina attend. Le cliquetis s'arrête. L'air arrive."),
            (E, "Tourne, sans rouler."),
            (P, "La dînette est rentrée. Le banc tient, lui."),
            (N, "Les pales partent. La tasse, loin, ne dit plus rien."),
        ),
        S(
            (N, "Ils laissent le toboggan. L'herbe du pied se redresse."),
            (E, "Il avait roulé sous la tasse."),
            (M, "Tu as attendu la fin du cliquetis."),
            (N, "La tasse dort dans la caisse, réunie à sa soucoupe."),
            (N, "Le moulin reste sur le banc, sans rouler."),
            (N, "La tasse dort. Le banc porte le petit vent."),
        ),
        "tasse,banc",
        "vaisselle,metal",
        "cliquetis",
    )
    data[("tobo", "dinette", "caisse")] = (
        S(
            (N, "Nina glisse la soucoupe. Le moulin est dans l'herbe ronde, là."),
            (E, "Je le mets en haut, elle en bas !"),
            (N, "Elle pose la soucoupe au fond, la tasse dedans, sans bruit."),
            (N, "Nina ferme. Elle met le moulin. Un brin d'herbe reste collé au couvercle."),
            (N, "Le brin chatouille une pale. Les pales refusent."),
            (P, "Chasse le brin, comme tu as chassé l'herbe de la tasse."),
            (N, "Nina chasse le brin. Le vent prend, net."),
            (E, "Plus d'herbe. Que le bois."),
            (M, "La dînette est au fond. Le brin, lui, est parti."),
            (N, "Les pales tournent. Un brin d'herbe reste collé, plus loin, inoffensif."),
        ),
        S(
            (N, "Papa porte la caisse, loin du pied du métal."),
            (E, "La tasse ne roule plus. Le moulin non plus."),
            (P, "Tu as chassé le brin, et le vent a pu entrer."),
            (N, "Ils reprennent le chemin. Un vélo sonne, tout loin."),
            (N, "Un brin d'herbe reste collé au couvercle, sous le bois."),
            (N, "Le moulin tourne au-dessus de la dînette, sans herbe dans les pales."),
        ),
        "herbe,couvercle",
        "caisse,velo",
        "brin",
    )
    data[("tobo", "dinette", "chemin")] = (
        S(
            (N, "Nina glisse la tasse. Le pied du toboggan est net."),
            (N, "Dans l'herbe de la tasse, le petit moulin, un peu vert."),
            (E, "Je le porte jusqu'au portail !"),
            (N, "Elle chasse le vert d'une pale, du pouce."),
            (N, "Nina marche. La tasse, dans la caisse, cliquette d'un pas trop vif."),
            (N, "Les pales s'énervent, comme si elles voulaient rouler aussi."),
            (M, "On pose la caisse un instant. Toi, tu donnes le vent."),
            (N, "Papa pose. Le cliquetis s'arrête. L'air de la rue entre."),
            (E, "Il tourne. La tasse se tait."),
            (P, "Le portail n'est pas loin. Le moulin a le temps."),
        ),
        S(
            (N, "Ils reprennent, plus lent. Le métal reste derrière."),
            (E, "La tasse s'est tue. Le moulin a parlé, lui."),
            (M, "Tu as laissé poser la caisse, et le vent a pu entrer."),
            (N, "La dînette dort, réunie, au fond du bois."),
            (N, "Le portail de l'école s'approche, et le moulin avance."),
            (N, "Les pales gardent la rue, sans rouler dans l'herbe."),
        ),
        "pas,tasse",
        "portail,vent",
        "portail",
    )

    # --- BALAN + CUBES ---
    data[("balan", "cubes", "banc")] = (
        S(
            (N, "Nina glisse le dernier cube de l'herbe. Clic, puis toc."),
            (N, "Sous le cube du pied, le bois, un peu d'herbe autour."),
            (E, "Il était sous le siège, lui aussi !"),
            (N, "Elle le sort. Une pale a gardé le froid de la chaîne, presque."),
            (N, "Nina le porte au banc, loin de la balançoire."),
            (N, "Elle le pose. Le banc ne crie pas, contrairement à la chaîne."),
            (E, "Ici, pas de fer. Que le vent."),
            (N, "Les pales prennent l'air des tilleuls, plus large que le siège."),
            (P, "Les cubes sont rentrés. Le banc n'est pas un siège."),
            (M, "La chaîne se tait, derrière vous."),
        ),
        S(
            (N, "Ils quittent les balançoires. L'herbe sous le siège se redresse."),
            (E, "Il était sous le cube, près du fer."),
            (P, "Tu l'as sorti de l'herbe, sans le jeter."),
            (N, "Les cubes dorment dans la caisse, un brin au bord."),
            (N, "Le moulin reste sur le banc, loin de la chaîne."),
            (N, "La chaîne de la balançoire se tait, derrière le banc."),
        ),
        "cube,banc",
        "chaine,vent",
        "chaîne",
    )
    data[("balan", "cubes", "caisse")] = (
        S(
            (N, "Nina glisse le dernier cube. Un pied de fer reparaît, net."),
            (N, "Sous le cube de l'herbe, le bois, collé d'un brin."),
            (E, "Sur la caisse, il ne tombera plus du siège !"),
            (N, "Elle pousse le couvercle. Toc. Un cube, au fond, ne bouge plus."),
            (N, "Nina pose le moulin. La caisse penche, comme le siège tout à l'heure."),
            (N, "Le moulin glisse. Elle rattrape le bâton, les joues chaudes."),
            (P, "J'arrête. Toi, tu le mets au plat, pas au bord."),
            (N, "Nina le recule. Les pales prennent, sans tomber."),
            (M, "Un cube ne bouge plus. Les pales, elles, travaillent."),
            (E, "Il tient. Pas comme sur le siège."),
        ),
        S(
            (N, "Papa porte la caisse, bien à plat, loin de la chaîne."),
            (E, "Les cubes sont en bas. Lui, il ne tombe plus."),
            (P, "Tu as rattrapé le bâton, puis choisi le plat."),
            (N, "Un cube ne bouge plus. Les pales font le travail."),
            (N, "Ils quittent l'herbe. La balançoire reste vide."),
            (N, "Le moulin tourne au-dessus des cubes, sans le cri du fer."),
        ),
        "couvercle,cubes",
        "caisse,chaine",
        "siège",
    )
    data[("balan", "cubes", "chemin")] = (
        S(
            (N, "Nina glisse le dernier cube. L'herbe sous le siège s'ouvre."),
            (N, "Sous le cube, le petit moulin, un peu d'herbe au bâton."),
            (E, "Je le tiens, et on va !"),
            (N, "Elle chasse le brin. Nina lève le bois."),
            (N, "Le premier pas balance, comme la balançoire. Les pales s'affolent."),
            (M, "Le chemin ne balance pas. Un pied, puis l'autre, à plat."),
            (N, "Nina pose les pieds, fermes. L'air de la rue entre."),
            (P, "Les cubes sont rentrés. Tes pieds, maintenant, sont des bancs."),
            (E, "Il tourne, sans balancer."),
            (N, "Une goutte tombe d'un tilleul, sans toucher le bois."),
        ),
        S(
            (N, "Ils quittent l'herbe. La chaîne reste derrière, muette."),
            (E, "Les cubes ne tombent plus. Le moulin marche."),
            (M, "Tes pieds se sont aplatis, et le vent a pu entrer."),
            (N, "La caisse ferme les cubes, loin du siège."),
            (N, "Une goutte tombe d'un tilleul, sans toucher le bois."),
            (N, "Les pales gardent la rue, sans le cri de la chaîne."),
        ),
        "pas,cubes",
        "tilleul,chaine",
        "goutte",
    )

    # --- BALAN + LIVRE ---
    data[("balan", "livre", "banc")] = (
        S(
            (N, "Nina glisse le livre. Sous le livre mouillé, les pales."),
            (E, "Il a bu une goutte, comme la page !"),
            (N, "Elle le sort. Une pale est un peu ondulée, comme le papier."),
            (N, "Nina le porte au banc, plus sec que l'herbe."),
            (N, "Elle le pose. Une goutte du tilleul vise le bois."),
            (P, "On recule d'un doigt. La goutte a l'herbe, pas les pales."),
            (N, "Nina recule le moulin. La goutte tombe dans l'herbe, à côté."),
            (E, "Tourne, sans boire."),
            (M, "Le livre est rentré. Le banc a le vent, pas l'eau."),
            (N, "Les pales partent, plus sèches que la page."),
        ),
        S(
            (N, "Ils laissent la balançoire. L'herbe garde la goutte, à elle."),
            (E, "Il était sous le livre, un peu mouillé."),
            (P, "Tu as reculé le bois, et la goutte a manqué les pales."),
            (N, "Le livre dort dans la caisse, une page un peu ondulée."),
            (N, "Le moulin reste sur le banc, plus sec."),
            (N, "Le livre a une page un peu ondulée, loin des pales."),
        ),
        "livre,banc",
        "goutte,pages",
        "goutte",
    )
    data[("balan", "livre", "caisse")] = (
        S(
            (N, "Nina glisse le livre, tout plat. Les pales quittent l'herbe."),
            (E, "Sur la caisse, plus de goutte !"),
            (N, "Elle pose le livre au fond, la page ondulée vers le bas."),
            (N, "Nina ferme. Elle met le moulin. Une pale touche une goutte du couvercle."),
            (N, "Les pales collent, un instant, comme les pages tout à l'heure."),
            (M, "Essuie le bois, comme tu as soufflé la page."),
            (N, "Nina passe la manche. La pale se décolle. Le vent prend."),
            (P, "Le livre est à l'abri. Lui, il a le dessus, sec."),
            (E, "Il ne boit plus."),
            (N, "Le vent du square reste sur le couvercle, en ronds."),
        ),
        S(
            (N, "Papa porte la caisse, loin de l'herbe mouillée."),
            (E, "La page est au fond. Le moulin, au sec."),
            (M, "Tu as essuyé, comme pour la page."),
            (N, "Ils reprennent les tilleuls. Le square reste derrière."),
            (N, "Le vent du square reste sur le couvercle, en ronds."),
            (N, "Les pales tournent, sans boire la goutte de l'herbe."),
        ),
        "livre,couvercle",
        "caisse,pages",
        "manche",
    )
    data[("balan", "livre", "chemin")] = (
        S(
            (N, "Nina glisse le livre. Sous le papier, le petit moulin, un peu humide."),
            (E, "Je souffle une pale, puis on marche !"),
            (N, "Elle souffle. Ffff. Une goutte part, pas toutes."),
            (N, "Nina lève le moulin. Le clac des chaussures envoie trop d'air, trop vite."),
            (N, "Les pales s'emballent, puis se collent, lourdes."),
            (P, "On marche moins vite. Le vent de la rue suffit."),
            (N, "Nina ralentit. L'air entre, plus sage. Les pales se séparent."),
            (E, "Il tourne, sans la goutte."),
            (M, "Le livre est fermé. Tes pas, eux, se sont fermés aussi, un peu."),
            (N, "Les feuilles jaunes collent moins, sous le clac."),
        ),
        S(
            (N, "Ils quittent l'herbe. La balançoire reste un fer muet."),
            (E, "La page ne boit plus. Le moulin non plus."),
            (P, "Tu as ralenti, et les pales se sont séparées."),
            (N, "La caisse ferme le livre, loin de la goutte."),
            (N, "Les feuilles jaunes collent moins, sous le clac."),
            (N, "Les pales gardent la rue, plus sèches à chaque pas."),
        ),
        "pas,livre",
        "feuilles,vent",
        "feuilles",
    )

    # --- BALAN + DINETTE ---
    data[("balan", "dinette", "banc")] = (
        S(
            (N, "Nina glisse la soucoupe. Sous la soucoupe, le petit moulin."),
            (E, "Il était dans l'assiette d'herbe !"),
            (N, "Elle le sort. Une pale a un brin vert, comme la soucoupe."),
            (N, "Nina chasse le brin, puis pose le moulin sur le banc."),
            (N, "Une pale cliquette contre le bois, puis se tait, plus vite que la tasse."),
            (P, "Le banc tient. Il n'est pas une soucoupe, et il n'est pas de l'herbe."),
            (N, "Le vent des tilleuls arrive. Les pales partent, nettes."),
            (E, "Tourne, sans les brins."),
            (M, "La dînette est rentrée. Le banc a le vent propre."),
            (N, "Les pales tournent. La soucoupe, loin, a perdu son herbe."),
        ),
        S(
            (N, "Ils laissent la balançoire. L'herbe sous le siège se redresse."),
            (E, "Il était sous la soucoupe, tout vert."),
            (P, "Tu as chassé le brin, puis tu as posé."),
            (N, "La soucoupe dort dans la caisse, moins verte."),
            (N, "Le moulin reste sur le banc, propre."),
            (N, "La soucoupe verte a perdu son herbe, dans la caisse."),
        ),
        "soucoupe,banc",
        "vaisselle,chaine",
        "soucoupe",
    )
    data[("balan", "dinette", "caisse")] = (
        S(
            (N, "Nina glisse la tasse. Un trou d'herbe s'ouvre, rond."),
            (N, "Sous la soucoupe, le petit moulin, un peu vert."),
            (E, "En haut, lui. En bas, elle."),
            (N, "Elle pose la dînette au fond, sans cliquetis, ou presque."),
            (N, "Nina ferme. Elle met le moulin. La poire, dans le sac, roule d'un pas."),
            (N, "Le sac tape la caisse. Les pales sautent, puis se figent."),
            (M, "Le sac a la poire. La caisse a le bois. On les sépare."),
            (N, "Nina écarte le sac. Le vent prend les pales, enfin."),
            (P, "La dînette est au fond. La poire, dans son tissu."),
            (E, "Il tourne. La poire peut rouler, elle."),
        ),
        S(
            (N, "Papa porte la caisse. Le sac, lui, reste sur l'épaule de maman."),
            (E, "La tasse est en bas. Le moulin, en haut. La poire, à part."),
            (M, "Tu as écarté le sac, et le vent a eu la place."),
            (N, "Ils reprennent le trottoir, chacun sa charge."),
            (N, "La poire roule un peu, dans le sac, à côté."),
            (N, "Le moulin tourne au-dessus de la dînette, sans le toc du sac."),
        ),
        "poire,couvercle",
        "caisse,sac",
        "poire",
    )
    data[("balan", "dinette", "chemin")] = (
        S(
            (N, "Nina glisse la soucoupe. L'herbe sous le siège s'ouvre."),
            (N, "Sous la soucoupe, le petit moulin, un brin au bâton."),
            (E, "Je le porte, jusqu'à l'écorce de la rue !"),
            (N, "Elle chasse le brin. Nina lève le bois."),
            (N, "Le premier pas fait cliqueter la caisse, et clac les chaussures, ensemble."),
            (N, "Trop de bruits. Les pales ne savent plus."),
            (P, "On écoute le clac, pas le cliquetis. Un pas plus lent."),
            (N, "Nina ralentit. La dînette se tait. L'air de la rue entre."),
            (E, "Il tourne. L'écorce sent moins la pluie."),
            (M, "La soucoupe est rentrée. Tes pales ont le chemin."),
        ),
        S(
            (N, "Ils quittent le square. Les tilleuls gardent leurs gouttes, plus haut."),
            (E, "La tasse s'est tue. Le moulin a le clac."),
            (P, "Tu as ralenti, et les pales ont choisi le vent."),
            (N, "La caisse ferme la dînette, loin de l'herbe."),
            (N, "L'écorce mouillée sèche, et le moulin garde le vent."),
            (N, "Les pales coupent la rue des tilleuls, jusqu'au portail."),
        ),
        "pas,soucoupe",
        "ecorce,vent",
        "écorce",
    )

    if len(data) != 27:
        raise SystemExit(f"t3_scenes {len(data)}")
    return data


if __name__ == "__main__":
    build()
