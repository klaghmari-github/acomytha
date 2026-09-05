#!/usr/bin/env python3
"""ATOM-AUT.RAN.001-02 — Le cacao de Nina (F-NAR-019, N2, linéaire)."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FORBIDDEN, ROOT, check, from_script, relecture, words  # noqa: E402

SID = "ATOM-AUT.RAN.001-02"
LIM = 15
TITLE = "Le cacao de Nina"
CHARS = "Nina, papa, maman"
SETTING = "chambre, pluie, boîte à musique, fin d'après-midi un peu froide"
FIL = (
    "Nina veut le cacao au milieu du tapis, maintenant, pour son ours. "
    "Une lune d'étain brille sur la boîte à musique. L'ours disparaît "
    "sous le pique-nique. Elle cherche le lit, pousse le tas : rien. "
    "Elle refuse de foncer, pose les tasses dans la caisse, suit la lune, "
    "trouve l'ours sous la poule. La vapeur du cacao s'accroche à la lune d'étain."
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
    "grain vanille",
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
    "pli de voile",
    "point de gouttière",
    "trait de craie",
    "trait de vitre",
    "nappe à carreaux",
    "vanille",
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
            "intensite=2; destinataire=enfant; sous_texte=la_lune_detain_sur_la_boite; "
            "tempo=naturel; sourire=léger; respiration=ample"
        ),
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note=(
            "arc=indice; intention=faire_deviner; emotion=attention; intensite=1; "
            "destinataire=enfant; sous_texte=l_ours_est_sous_le_tas; "
            "tempo=suspendu; sourire=aucun; respiration=courte_avant_question"
        ),
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note=(
            "arc=résolution; intention=faire_vivre_la_réussite; emotion=fierté_calme; "
            "intensite=2; destinataire=enfant; sous_texte=elle_suit_la_lune_trouve_l_ours; "
            "tempo=naturel; sourire=franc; respiration=relâchée"
        ),
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note=(
            "arc=obstacle; intention=alerter_sans_effrayer; emotion=deux_envies_qui_se_heurtent; "
            "intensite=2; destinataire=enfant; sous_texte=elle_refuse_de_foncer_pose_la_tasse; "
            "tempo=resserré; sourire=aucun; respiration=retenue"
        ),
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note=(
            "arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; "
            "destinataire=enfant; sous_texte=la_vapeur_s_accroche_a_la_lune_detain; "
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
    ("narrateur", "La vapeur du cacao grimpe l'escalier."),
    ("narrateur", "Elle entre dans la chambre froide."),
    ("narrateur", "Sur la vitre, la pluie trace un chemin."),
    ("narrateur", "La boîte à musique vient de se taire."),
    ("narrateur", "Un ding reste coincé dans l'air."),
    ("narrateur", "Sur le couvercle, une lune d'étain."),
    ("narrateur", "Elle capte un bout de ciel gris."),
    ("narrateur", "La lumière est basse, un peu bleue."),
    ("narrateur", "Une chaussette sèche sur la chaise."),
    ("narrateur", "Elle est un peu tiède."),
    ("narrateur", "La chambre sent le cacao chaud."),
    ("papa", "Il fait frais, ce soir."),
    ("maman", "Le cacao est sur le feu."),
    ("enfant-f", "Je le veux sur le tapis !"),
    ("enfant-f", "Maintenant, maman."),
    ("maman", "Il va refroidir vite."),
    ("narrateur", "En ce moment, Nina s'agenouille."),
    ("narrateur", "Le tapis est épais, un peu froid."),
    ("narrateur", "Un ours brun attend sur l'oreiller."),
    ("enfant-f", "Toi, tu viens au pique-nique."),
    ("narrateur", "Elle le pose au milieu du tapis."),
    ("narrateur", "Un lapin gris la rejoint."),
    ("narrateur", "Une poule jaune s'installe près de lui."),
    ("narrateur", "Nina aligne trois tasses en bois."),
    ("narrateur", "Les tasses font clic."),
    ("enfant-f", "C'est pour le vrai cacao."),
    ("maman", "Il arrive, bien chaud."),
    ("papa", "Vous soufflerez dessus."),
    ("narrateur", "Nina souffle au-dessus d'une tasse."),
    ("enfant-f", "Ffff."),
    ("narrateur", "Maman pousse la porte, une grande tasse à la main."),
    ("narrateur", "Une petite vapeur danse au bord."),
    ("enfant-f", "Pose-la au milieu !"),
    ("narrateur", "Nina cherche un rond libre."),
    ("narrateur", "La patte du lapin occupe le centre."),
    ("enfant-f", "L'ours veut le cacao, lui."),
    ("maman", "Où est ton ours, alors ?"),
    ("narrateur", "Nina se tourne vers l'oreiller."),
    ("narrateur", "L'oreiller est plat, vide."),
    ("enfant-f", "Il n'est plus sur le lit."),
    ("papa", "Sous la couverture rose ?"),
    ("narrateur", "Elle soulève la couverture."),
    ("narrateur", "Rien, seulement le drap tiède."),
    ("enfant-f", "Il est perdu !"),
    ("narrateur", "Le sourire de Nina disparaît."),
    ("narrateur", "Les peluches et les tasses couvrent le tapis."),
    ("enfant-f", "Je n'ai pas de place."),
    ("narrateur", "Nina pousse le tas d'un bras."),
    ("narrateur", "Une tasse roule vers la chaise."),
    ("narrateur", "Le tas retombe, plus mêlé."),
    ("enfant-f", "Ça ne marche pas."),
    ("narrateur", "Dans sa poitrine, ça se bouscule."),
    ("narrateur", "L'envie et l'inquiétude se heurtent."),
    ("narrateur", "Maman s'accroupit à la même hauteur."),
    ("maman", "Tu veux pousser, ou regarder ?"),
    ("enfant-f", "Je veux mon ours."),
    ("narrateur", "Nina baisse les épaules."),
)

QUESTION = L(
    ("narrateur", "Nina cherche son ours sous le tas."),
    ("maman", "Où se cache-t-il ?"),
)

CONFIRM = L(
    ("enfant-f", "J'arrête de pousser."),
    ("narrateur", "Elle lâche le tas."),
    ("narrateur", "Près de la fenêtre, la lune d'étain brille."),
    ("enfant-f", "Elle me montre le tapis."),
    ("narrateur", "Nina prend une tasse en bois."),
    ("narrateur", "Elle la pose dans la caisse ronde."),
    ("narrateur", "Clic."),
    ("papa", "La tasse a sa place."),
    ("narrateur", "La deuxième tasse suit."),
    ("enfant-f", "Toi aussi, lapin."),
    ("narrateur", "Elle glisse le lapin dans la caisse."),
    ("maman", "Tu regardes bien dessous ?"),
    ("enfant-f", "Oui, maman."),
    ("narrateur", "Un coin de tapis reparaît."),
    ("narrateur", "La poule reste au milieu."),
    ("enfant-f", "Je prends tout d'un coup."),
    ("narrateur", "Nina ouvre les deux mains."),
    ("narrateur", "Elle veut vider le tapis vite."),
    ("narrateur", "La poule bascule sur le côté."),
    ("narrateur", "Puis la dernière tasse part sous la chaise."),
    ("enfant-f", "Oh non."),
    ("narrateur", "Nina s'arrête net."),
    ("enfant-f", "Pas comme ça."),
    ("narrateur", "Elle refuse de foncer."),
    ("narrateur", "Elle lève les yeux vers la boîte."),
    ("narrateur", "La lune d'étain capte la pluie."),
    ("narrateur", "Un reflet tombe sur un petit dos."),
    ("enfant-f", "Là, sous la poule."),
    ("narrateur", "Nina soulève la poule, sans se presser."),
    ("narrateur", "Un museau brun est dessous."),
    ("enfant-f", "Mon ours !"),
    ("narrateur", "L'ours était sous la poule."),
    ("narrateur", "Une tasse en bois l'avait caché."),
    ("narrateur", "Nina le serre contre sa joue."),
    ("narrateur", "Le poil est chaud, un peu écrasé."),
    ("papa", "Merci d'avoir regardé, Nina."),
    ("enfant-f", "Il buvait en dessous."),
    ("maman", "Te voilà, petit ours."),
    ("narrateur", "La dernière tasse va dans la caisse."),
    ("narrateur", "Le tapis a un rond vide, au milieu."),
    ("narrateur", "Nina pose l'ours contre son genou."),
)

COCOA = L(
    ("narrateur", "Maman avance la vraie tasse."),
    ("narrateur", "La vapeur sent le cacao."),
    ("enfant-f", "Je la prends maintenant !"),
    ("narrateur", "Nina tend les deux mains trop vite."),
    ("narrateur", "La tasse penche, la vapeur fuit."),
    ("maman", "Elle est chaude, tu vois ?"),
    ("enfant-f", "J'attends."),
    ("narrateur", "Nina pose les mains à plat."),
    ("narrateur", "Elle souffle une fois, puis deux."),
    ("enfant-f", "Ffff."),
    ("narrateur", "La lune d'étain éclaire un rond."),
    ("enfant-f", "Là, au milieu."),
    ("narrateur", "Maman pose la tasse sur ce rond."),
    ("papa", "On souffle un peu."),
    ("narrateur", "Nina souffle avec lui."),
    ("narrateur", "Elle boit une petite gorgée."),
    ("narrateur", "Le cacao est doux, un peu sucré."),
    ("enfant-f", "L'ours a une goutte, papa."),
    ("papa", "Une toute petite goutte."),
    ("maman", "Tu en veux un peu ?"),
    ("enfant-f", "Oui, maman."),
)

ENDING = L(
    ("narrateur", "La pluie tapote plus bas."),
    ("narrateur", "La chaussette sur la chaise est sèche."),
    ("narrateur", "Nina tient l'ours d'une main."),
    ("narrateur", "De l'autre, elle tient la tasse."),
    ("narrateur", "La boîte à musique reprend un ding."),
    ("enfant-f", "On est bien, ici."),
    ("maman", "Oui, vous y êtes."),
    ("narrateur", "La vapeur s'accroche à la lune d'étain."),
)


def main() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by = {c["chunk_id"]: c for c in src["chunks"]}
    scripts = {
        "CHK_T0000_P0000": ("opening", OPENING, "pluie,boite-musique", {"emphasis": "lune d'étain"}),
        "CHK_T0000_P0000_Q0001": (
            "clue",
            QUESTION,
            "",
            {
                "emphasis": "ours",
                "pause_before": 200,
                "fields": {
                    "expected_answer": "l'ours",
                    "accepted_examples": "l'ours | ours | nounours | sous la poule | sous les peluches | dessous",
                    "retry_prompt": "Elle cherche sous les peluches. Où est l'ours ?",
                },
            },
        ),
        "CHK_T0000_P0000_C0001": ("resolution", CONFIRM, "tasse-bois,caisse", {"emphasis": "lune d'étain"}),
        "CHK_T0000_P0000_END": ("obstacle", COCOA, "cacao", {"emphasis": "lune d'étain"}),
        "CHK_T0000_P0000_END_F0001": (
            "ending",
            ENDING,
            "pluie,boite-musique",
            {"emphasis": "lune d'étain", "pause_before": 200},
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
    if "lune d'étain" not in joined:
        raise SystemExit("indice lune d'étain manquant")
    if joined.count("lune d'étain") < 2:
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
            "Nina veut le cacao au milieu du tapis, maintenant, pour l'ours. "
            "Lune d'étain sur la boîte à musique. Ours perdu sous le pique-nique. "
            "Lit, couverture, bras dans le tas : rien. Elle refuse de foncer, "
            "pose les tasses, suit la lune, trouve l'ours sous la poule. "
            "La vapeur s'accroche à la lune d'étain."
        ),
        (
            "Ouverture par la vapeur qui grimpe, pas le salon. "
            "Monde du dump : chambre, pluie, boîte à musique, fin d'après-midi froide. "
            "Indice unique lune d'étain, nommé puis payé. "
            "≠ RAN.001-01 nappe à carreaux / éclat de nappe. "
            "Leçon ranger vécue, pas dite. "
            "Tics encore/déjà/tout doux/tout calme absents. "
            "TTS notes+ssml+xai+piper par chunk. Pas apply, pas git, pas audio."
        ),
    )


if __name__ == "__main__":
    main()
