#!/usr/bin/env python3
"""ATOM-AUT.AFF.001-02 — La cour de Sarah (F-NAR-019, N1, linéaire)."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "ATOM-AUT.AFF.001-02"
LIM = 10
TITLE = "La cour de Sarah"
CHARS = "Sarah, maman"
SETTING = "appartement d'immeuble puis cour"
FIL = (
    "Sarah veut pincer sa serviette bleue sur le fil de la cour, maintenant. "
    "Un éclat de pince saute sur la table. Elle bourre le sac trop vite, le zip refuse. "
    "Elle arrête de forcer, range, descend. Chouchou tire vers le chat ; "
    "Sarah refuse de foncer, retrouve l'éclat, pince le tissu. "
    "Le sac repose près du pot fêlé."
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
    "grain de paille",
    "grain de toile",
    "grain de pépin",
    "grain de laine",
    "grelot",
    "parquet",
    "lavande",
    "terre grise",
    "carotte",
    "parasol",
    "éclat de thermos",
    "éclat de coquille",
    "éclat de bouton",
    "éclat de ticket",
    "éclat de goutte",
    "éclat de boucle",
    "trait de craie",
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
            "intensite=2; destinataire=enfant; sous_texte=l_eclat_de_pince_saute_sur_la_table; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=les_affaires_vont_dans_le_sac; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=elle_cesse_de_forcer_le_zip_part; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=deux_envies_qui_se_heurtent; "
            "intensite=2; destinataire=enfant; sous_texte=elle_refuse_de_foncer_retrouve_l_eclat; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=l_eclat_de_pince_paie_le_debut; "
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
    ("narrateur", "Un clac monte l'escalier de pierre."),
    ("narrateur", "C'est le drap, en bas, sur le fil."),
    ("narrateur", "Sarah connaît cette cour."),
    ("narrateur", "En bas, un pot est fêlé."),
    ("narrateur", "Une plante verte y pousse."),
    ("narrateur", "Les marches sentent le savon."),
    ("narrateur", "Au troisième, la fenêtre est ouverte."),
    ("narrateur", "La cuisine sent l'orange pressée."),
    ("narrateur", "Un éclat saute sur la table."),
    ("narrateur", "Ce n'est pas le jus."),
    ("narrateur", "C'est un éclat de pince."),
    ("narrateur", "La pince tient le drap, en bas."),
    ("maman", "Sarah, tu as vu le linge ?"),
    ("enfant-f", "Oui, maman."),
    ("enfant-f", "Il danse."),
    ("maman", "Chouchou t'attend près du pot."),
    ("enfant-f", "Je veux descendre maintenant !"),
    ("maman", "On prend le sac, d'abord."),
    ("narrateur", "En ce moment, Sarah saisit le sac vert."),
    ("narrateur", "Le tissu gratte sous ses doigts."),
    ("enfant-f", "Il est à moi."),
    ("maman", "Oui, c'est le tien."),
    ("narrateur", "Près du sac, une serviette bleue."),
    ("narrateur", "Elle est un peu humide."),
    ("enfant-f", "Je veux la pincer, là-bas !"),
    ("maman", "Mets l'eau, pour la cour."),
    ("narrateur", "Sarah pousse la gourde d'un coup."),
    ("narrateur", "La gourde bascule contre le tissu."),
    ("enfant-f", "Vite, maman !"),
    ("maman", "Ton chapeau aussi, le soleil tape."),
    ("narrateur", "Sarah cherche près de la chaise."),
    ("narrateur", "La chaise est vide."),
    ("enfant-f", "Il n'est pas là."),
    ("narrateur", "Le chapeau souple est par terre."),
    ("narrateur", "Elle le jette dans le sac."),
    ("enfant-f", "Et mon doudou ?"),
    ("maman", "Il voudra voir Chouchou."),
    ("narrateur", "Le doudou gris a les oreilles plates."),
    ("narrateur", "Il sent l'oreiller de la chambre."),
    ("narrateur", "Sarah le glisse, trop vite."),
    ("narrateur", "La sangle se coince dans le zip."),
    ("enfant-f", "Ça reste, maman !"),
    ("narrateur", "Elle tire plus fort."),
    ("narrateur", "Le zip refuse."),
    ("narrateur", "Le sourire de Sarah disparaît."),
    ("narrateur", "Dans sa poitrine, ça se bouscule."),
    ("narrateur", "Maman s'accroupit à la même hauteur."),
    ("maman", "Tu veux forcer, ou regarder ?"),
    ("enfant-f", "Je veux Chouchou."),
    ("narrateur", "Sarah tire une dernière fois."),
    ("narrateur", "Rien ne bouge."),
    ("narrateur", "Elle baisse les épaules."),
)

QUESTION = L(
    ("narrateur", "Sarah prépare le sac pour descendre."),
    ("maman", "Où met-elle les affaires ?"),
)

CONFIRM = L(
    ("enfant-f", "J'arrête de tirer."),
    ("narrateur", "Elle lâche le zip."),
    ("narrateur", "Un fil du sac brille un peu."),
    ("enfant-f", "Comme la pince."),
    ("narrateur", "Sarah pince le tissu coincé."),
    ("narrateur", "Elle le tire vers elle, sans forcer."),
    ("narrateur", "Le zip avance, petit à petit."),
    ("enfant-f", "Il part !"),
    ("maman", "Tu l'as aidé, toi."),
    ("narrateur", "Sarah glisse le chapeau, sans jeter."),
    ("enfant-f", "Toi aussi, gourde."),
    ("narrateur", "La gourde rentre, bien droite."),
    ("narrateur", "Le doudou glisse près de l'eau."),
    ("enfant-f", "Vous êtes dedans."),
    ("maman", "Tu fermes, maintenant ?"),
    ("narrateur", "Sarah appuie sur la fermeture."),
    ("narrateur", "Ça fait zzz, très bas."),
    ("narrateur", "Le sac vert est fermé."),
    ("maman", "Le sac est prêt ?"),
    ("enfant-f", "Oui, maman."),
    ("narrateur", "Sarah pose le sac contre sa jambe."),
    ("narrateur", "Le vert brille un peu."),
    ("maman", "On descend voir Chouchou ?"),
    ("enfant-f", "Oui."),
)

COURTYARD = L(
    ("narrateur", "Sarah porte le sac."),
    ("narrateur", "Les bretelles sont souples."),
    ("maman", "On va vers la porte."),
    ("narrateur", "Elles quittent l'appartement."),
    ("narrateur", "La cage d'escalier sent le savon."),
    ("maman", "Tu as ton sac ?"),
    ("enfant-f", "Oui, maman."),
    ("narrateur", "Un pas, puis un autre."),
    ("narrateur", "La rampe est lisse, un peu froide."),
    ("maman", "Tu tiens la rampe ?"),
    ("enfant-f", "Oui."),
    ("narrateur", "Les marches piquent un peu les pieds."),
    ("narrateur", "Un voisin ferme une porte, loin."),
    ("narrateur", "La cour s'ouvre, claire."),
    ("narrateur", "Le drap blanc claque sur le fil."),
    ("narrateur", "Chouchou est près du pot fêlé."),
    ("narrateur", "Sarah lève la main."),
    ("enfant-f", "Je suis là !"),
    ("narrateur", "Chouchou court vers Sarah."),
    ("enfant-f", "Viens, le chat part !"),
    ("narrateur", "Sarah veut accrocher sa serviette."),
    ("narrateur", "Les deux envies se heurtent."),
    ("narrateur", "Sarah s'arrête net."),
    ("enfant-f", "Pas maintenant."),
    ("narrateur", "Elle refuse de foncer."),
    ("narrateur", "Elle lève les yeux vers le fil."),
    ("narrateur", "L'éclat de pince est là."),
    ("narrateur", "Celui de la table, ce matin."),
    ("enfant-f", "D'abord le fil."),
    ("narrateur", "Elle sort la serviette bleue."),
    ("maman", "Tu veux une pince ?"),
    ("enfant-f", "Celle qui brille."),
    ("narrateur", "Sarah pose le tissu près du drap."),
    ("narrateur", "Elle pince, sans se presser."),
    ("narrateur", "La serviette tient."),
    ("narrateur", "Chouchou s'approche du fil."),
    ("enfant-f", "Ça brille !"),
)

ENDING = L(
    ("narrateur", "Les deux filles regardent le fil."),
    ("narrateur", "La serviette bleue danse un peu."),
    ("narrateur", "L'éclat de pince reste sur le métal."),
    ("narrateur", "Le sac vert repose près du pot."),
    ("maman", "Merci d'avoir regardé, Sarah."),
    ("maman", "Tu as vu la pince, toi ?"),
    ("enfant-f", "Elle m'a montré le fil."),
    ("narrateur", "Le doudou est au chaud, dans le sac."),
    ("narrateur", "Le drap blanc fait une ombre ronde."),
    ("narrateur", "Un chat gris passe dans l'ombre."),
    ("enfant-f", "On est dans la cour."),
    ("maman", "Oui, vous y êtes."),
    ("narrateur", "Elles se tiennent la main."),
)


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: c for c in src["chunks"]}
    scripts = {
        "CHK_T0000_P0000": ("opening", OPENING, "linge,savon", {"emphasis": "éclat de pince"}),
        "CHK_T0000_P0000_Q0001": (
            "clue",
            QUESTION,
            "",
            {
                "emphasis": "sac",
                "pause_before": 200,
                "fields": {
                    "expected_answer": "le sac",
                    "accepted_examples": "le sac | dans le sac | il met | elle met | mettre",
                    "retry_prompt": "Elle met les affaires dans le sac. Où les met Sarah ?",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": ("resolution", CONFIRM, "zip", {"emphasis": "zip"}),
        "CHK_T0000_P0000_END": ("obstacle", COURTYARD, "pas,linge", {"emphasis": "éclat de pince"}),
        "CHK_T0000_P0000_END_F0001": (
            "ending",
            ENDING,
            "linge",
            {"emphasis": "éclat de pince", "pause_before": 200},
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
    joined = "\n".join(c["script"] for c in chunks).lower()
    if "éclat de pince" not in joined:
        raise SystemExit("indice éclat de pince manquant")
    if joined.count("éclat de pince") < 2:
        raise SystemExit("indice non payé (moins de 2 mentions)")
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
            "Sarah veut pincer sa serviette bleue sur le fil, maintenant. "
            "Éclat de pince sur la table. Sac bourré, zip coincé. "
            "Elle cesse de forcer. En cour, Chouchou tire vers le chat ; "
            "Sarah refuse de foncer, retrouve l'éclat, pince le tissu. "
            "Le sac repose près du pot fêlé."
        ),
        (
            "Ouverture par le clac du drap, pas le salon. "
            "Indice unique éclat de pince, nommé puis payé. "
            "Pas de grain de miette / four / village. "
            "Tics encore/déjà/tout doux/tout calme absents. "
            "TTS notes+ssml+xai+piper par chunk. Pas apply, pas git, pas audio."
        ),
    )


if __name__ == "__main__":
    main()
