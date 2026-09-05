#!/usr/bin/env python3
"""TREE-DIF-033 — Le cheval doré de Sarah, au carrousel (F-NAR-019, N2)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-DIF-033"
LIM = 15
TITLE = "Le cheval doré de Sarah, au carrousel"
FIL = (
    "À la fête du village, Sarah veut un tour sur le cheval doré, avec Aniss. "
    "Elle le tire trop tôt : Aniss bondit, le ticket tombe, le cheval part sans eux. "
    "Ticket bleu, écharpe à pois ou clochette : on prépare. "
    "Dans la file il saute, au marchepied il bondit, sur l'or il veut galoper. "
    "Petit saut, banc, poche de papa ; deux ombres, marche, écharpe de maman ; "
    "valse, arrêt, barre de papa. Le tour se fait. La crinière d'or se tait."
)
TICS = (
    "tout doux", "tout calme", "encore", "déjà",
    "on va apprendre", "voici le geste", "bon travail",
    "c'est du bon travail", "l'histoire est finie",
    "beaucoup d'énergie", "ce n'est pas une faute",
    "il faut attendre", "on doit demander",
)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ssml(text: str, m: dict) -> str:
    body = esc(text)
    emp = m.get("emphasis")
    if emp:
        e = esc(emp)
        body = body.replace(e, f'<emphasis level="moderate">{e}</emphasis>', 1)
    return (
        f'<speak><prosody rate="{m["rate"]}" pitch="{m["pitch_ssml"]}">'
        f'{body}</prosody><break time="{m["pause"]}ms"/></speak>'
    )


def xai(text: str, m: dict) -> str:
    body = text
    emp = m.get("emphasis")
    if emp:
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
        note="arc=installation; intention=émerveiller; emotion=impatience_joyeuse; intensite=1; destinataire=enfant; sous_texte=le_cheval_doré_va_partir; tempo=naturel; sourire=léger; respiration=ample",
    ),
    "choice": dict(
        rate="slow", wpm=116, speed=0.84, piper=1.30, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=900,
        sentence=330, energy="focused", contour="rising", noise=0.33,
        note="arc=choix; intention=inviter; emotion=curiosité; intensite=1; destinataire=enfant; sous_texte=ton_choix_compte; tempo=suspendu; sourire=léger; respiration=pause_avant_choix",
    ),
    "clue": dict(
        rate="slow", wpm=120, speed=0.86, piper=1.27, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="soft", db=-2, pause=700,
        sentence=320, energy="focused", contour="rising", noise=0.32,
        note="arc=indice; intention=faire_deviner; emotion=attention; intensite=1; destinataire=enfant; sous_texte=regarde_bien; tempo=suspendu; sourire=aucun; respiration=courte_avant_question",
    ),
    "confirm": dict(
        rate="medium", wpm=132, speed=0.92, piper=1.20, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=450,
        sentence=280, energy="bright", contour="falling", noise=0.34,
        note="arc=confirmation; intention=relancer; emotion=joie_discrete; intensite=1; destinataire=enfant; sous_texte=on_peut_avancer_vers_le_tour; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=le_premier_geste_rate; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=impatience_et_decouragement; intensite=2; destinataire=enfant; sous_texte=tenir_Aniss_ne_marche_pas; tempo=resserre; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=resolution; intention=faire_vivre_la_reussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=jouer_attendre_ou_demander_change_le_tour; tempo=naturel; sourire=franc; respiration=relachee",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierte_calme; intensite=1; destinataire=enfant; sous_texte=la_criniere_dor_se_tait; tempo=pose; sourire=léger; respiration=ample",
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
    ("narrateur", "Sur la place du village, la fête sent le sucre chaud."),
    ("narrateur", "Un kiosque cuit des gaufres, juste à côté."),
    ("narrateur", "Un cuivre joue une valse, un peu boiteuse."),
    ("narrateur", "Les chevaux peints brillent, or et rouge."),
    ("papa", "Tu as vu la crinière, Sarah ?"),
    ("enfant-f", "Elle est toute en or, je la veux."),
    ("maman", "Le ticket bleu attend dans ma poche."),
    ("narrateur", "En ce moment, Sarah tire Aniss vers le bois."),
    ("enfant-f", "On y va, tout de suite !"),
    ("enfant-m", "Moi je saute jusqu'au cheval !"),
    ("narrateur", "Aniss bondit, et ses genoux tapent l'air."),
    ("narrateur", "Sarah le tire trop fort vers la rampe."),
    ("narrateur", "Le ticket bleu glisse, et tombe dans la poussière."),
    ("narrateur", "La valse part, et le cheval doré part sans eux."),
    ("enfant-f", "Il est parti, c'était notre tour !"),
    ("papa", "Le bois va revenir, on se prépare."),
    ("maman", "Ticket, écharpe, clochette : on les prend."),
    ("narrateur", "Sarah serre les poings, puis elle souffle."),
    ("enfant-f", "Je veux le tour, avec Aniss."),
)

T1 = {
    1: dict(
        name="le ticket bleu",
        passage=L(
            ("narrateur", "Sarah saisit le ticket bleu, tout craquant."),
            ("enfant-f", "Je cours, Aniss, on rattrape le cheval !"),
            ("enfant-m", "J'arrive, plus vite que toi !"),
            ("narrateur", "Aniss saute, et le papier s'envole vers le kiosque."),
            ("narrateur", "Sarah s'arrête, les joues chaudes."),
            ("enfant-f", "Le ticket, non !"),
            ("maman", "Glisse-le dans ta poche, près du cœur."),
            ("narrateur", "Le papier froisse contre le pull, et reste."),
            ("papa", "L'écharpe et la clochette voyagent avec vous."),
            ("narrateur", "Aniss prend la clochette, les pieds qui tapent."),
            ("enfant-f", "Cette fois, on le garde."),
        ),
        question="Sarah a glissé le ticket bleu où ?",
        expected="poche",
        accepted="poche | la poche | dans la poche | sa poche | près du cœur",
        retry="Le ticket est dans la poche.",
        ok="Oui, dans la poche.",
        confirm=L(
            ("narrateur", "La poche veille sur le papier bleu."),
            ("enfant-m", "Je vois l'encre, elle sent le sucre."),
            ("enfant-f", "Ne le plie pas, Aniss."),
            ("narrateur", "Une mèche d'Aniss saute quand il respire."),
            ("papa", "Merci, tu as sauvé le ticket."),
            ("maman", "Vos mains restent au-dessus de la poche ?"),
            ("enfant-f", "Oui, maman."),
        ),
        sons="papier,gaufre",
        emphasis="ticket bleu",
        choice=L(
            ("narrateur", "Aniss tapote le sol peint, léger."),
            ("narrateur", "La file serpente vers les chevaux d'or."),
            ("narrateur", "Le marchepied brille, un peu haut."),
            ("narrateur", "Le cheval doré attend, crinière d'or."),
            ("papa", "On commence où, pour le tour ?"),
        ),
    ),
    2: dict(
        name="l'écharpe à pois",
        passage=L(
            ("narrateur", "Sarah enroule l'écharpe à pois autour du cou."),
            ("enfant-f", "Pour le vent du tour, Aniss !"),
            ("enfant-m", "Je tourne, moi aussi !"),
            ("narrateur", "Aniss tourne trop vite, et un pois s'accroche."),
            ("narrateur", "L'écharpe tire, Sarah recule d'un pas."),
            ("enfant-f", "Aïe, attends !"),
            ("papa", "Autour du cou, sans danser."),
            ("narrateur", "Sarah noue le tissu, un pois contre le pull."),
            ("maman", "Le ticket et la clochette voyagent avec vous."),
            ("narrateur", "Aniss prend la clochette, genoux plus vifs."),
            ("enfant-f", "On y va, mais le pois reste."),
        ),
        question="L'écharpe à pois est autour de quoi ?",
        expected="cou",
        accepted="cou | le cou | autour du cou | son cou | du cou",
        retry="L'écharpe est autour du cou.",
        ok="Oui, autour du cou.",
        confirm=L(
            ("narrateur", "Le cou porte l'écharpe, contre le pull."),
            ("enfant-m", "Elle a trop de pois !"),
            ("enfant-f", "C'est pour le vent du tour."),
            ("narrateur", "Les pieds d'Aniss tapent le sol peint."),
            ("maman", "Merci, tu as noué le pois sans danser."),
            ("papa", "On reste près des chevaux ?"),
            ("enfant-f", "Oui, papa."),
        ),
        sons="tissu,gaufre",
        emphasis="écharpe à pois",
        choice=L(
            ("narrateur", "Un pois de l'écharpe tremble au vent sucré."),
            ("narrateur", "La file serpente vers les chevaux d'or."),
            ("narrateur", "Le marchepied brille, un peu haut."),
            ("narrateur", "Le cheval doré attend, crinière d'or."),
            ("maman", "On commence où, pour le tour ?"),
        ),
    ),
    3: dict(
        name="la clochette",
        passage=L(
            ("narrateur", "Sarah noue la clochette au poignet d'Aniss."),
            ("enfant-f", "Elle va sonner notre tour."),
            ("enfant-m", "Toc toc toc, j'agite !"),
            ("narrateur", "Le tintement couvre la valse, trop fort."),
            ("narrateur", "Un cheval peint secoue sa tête de bois."),
            ("enfant-f", "Trop fort, Aniss."),
            ("maman", "Au poignet, et on laisse la valse."),
            ("narrateur", "Aniss ouvre la main, la clochette se tait."),
            ("papa", "Le ticket et l'écharpe voyagent avec vous."),
            ("enfant-f", "Je te garde une place près de l'or."),
            ("enfant-m", "J'arrive près des chevaux."),
        ),
        question="Sarah a noué la clochette où ?",
        expected="poignet",
        accepted="poignet | le poignet | au poignet | son poignet",
        retry="La clochette est au poignet.",
        ok="Oui, au poignet.",
        confirm=L(
            ("narrateur", "La clochette cache le pouls, sans tinter."),
            ("enfant-m", "Ça sent le sucre, près du kiosque."),
            ("enfant-f", "La file de départ est là."),
            ("narrateur", "Les manches d'Aniss laissent ses poignets libres."),
            ("papa", "Merci, tu as laissé la valse parler."),
            ("maman", "On y va, tous les quatre ?"),
            ("enfant-f", "Oui."),
        ),
        sons="clochette,gaufre",
        emphasis="clochette",
        choice=L(
            ("narrateur", "La clochette repose, muette, contre la peau."),
            ("narrateur", "La file serpente vers les chevaux d'or."),
            ("narrateur", "Le marchepied brille, un peu haut."),
            ("narrateur", "Le cheval doré attend, crinière d'or."),
            ("papa", "On commence où, pour le tour ?"),
        ),
    ),
}

T2_SONS = {1: "foule,pas", 2: "bois,pas", 3: "carrousel,bois"}
T3_LABS = {
    1: ("le petit saut", "le banc du kiosque", "la poche de papa"),
    2: ("les deux ombres", "la marche de bois", "l'écharpe de maman"),
    3: ("la petite valse", "l'arrêt du cheval", "la barre de papa"),
}


def t2_file(a: int) -> list[tuple[str, str]]:
    lead = {
        1: "Sarah serre le ticket, dans la file sucrée.",
        2: "Sarah serre l'écharpe, dans la file sucrée.",
        3: "Sarah serre la clochette, dans la file sucrée.",
    }[a]
    mishap = {
        1: "Le ticket bleu tremble, puis glisse entre les doigts.",
        2: "Un pois de l'écharpe se défait, et pend.",
        3: "La clochette tinte trop fort, trop vite.",
    }[a]
    name = {1: "Le ticket", 2: "L'écharpe", 3: "La clochette"}[a]
    return L(
        ("narrateur", lead),
        ("enfant-f", "Reste près de moi, Aniss."),
        ("enfant-m", "Moi je saute, Sarah !"),
        ("narrateur", "Aniss saute entre les pieds, trop vite."),
        ("narrateur", "Un chapeau penche, puis se redresse."),
        ("narrateur", mishap),
        ("enfant-f", f"{name} n'attendait pas ça."),
        ("narrateur", "Sarah le rattrape, les épaules dures."),
        ("maman", "Regarde ses pieds, ils n'arrivent pas à s'arrêter."),
        ("papa", "Toi tu as les jambes plus longues."),
        ("enfant-m", "On joue comment, alors ?"),
        ("papa", "Vous faites comment, tous les deux ?"),
    )


def t2_step(a: int) -> list[tuple[str, str]]:
    lead = {
        1: "Sarah pose le ticket près du marchepied.",
        2: "Sarah pose l'écharpe près du marchepied.",
        3: "Sarah pose la clochette près du marchepied.",
    }[a]
    mishap = {
        1: "Le ticket frôle le bois, trop bas.",
        2: "L'écharpe accroche une vis, un instant.",
        3: "La clochette tape le fer, toc.",
    }[a]
    return L(
        ("narrateur", lead),
        ("enfant-f", "Le marchepied est à nous, Aniss."),
        ("enfant-f", "Moi je monte, tu me suis."),
        ("enfant-m", "Je monte le premier, trop vite !"),
        ("narrateur", "Ses pieds quittent le sol, puis reviennent."),
        ("narrateur", mishap),
        ("narrateur", "Un peu de poussière lève, puis retombe."),
        ("narrateur", "Sarah se cogne à son épaule, surprise."),
        ("maman", "Il a de l'élan, comme un petit vent."),
        ("papa", "Toi tu as les jambes plus longues."),
        ("enfant-f", "On peut jouer avec lui ?"),
        ("papa", "Vous trouvez, tous les deux ?"),
    )


def t2_horse(a: int) -> list[tuple[str, str]]:
    lead = {
        1: "Sarah glisse le ticket près de la crinière.",
        2: "Sarah noue l'écharpe près de la crinière.",
        3: "Sarah pose la clochette près de la crinière.",
    }[a]
    mishap = {
        1: "Le ticket frôle l'or, trop vite.",
        2: "L'écharpe claque contre le cou du cheval.",
        3: "La clochette tinte trop près de l'oreille.",
    }[a]
    name = {1: "Le ticket", 2: "L'écharpe", 3: "La clochette"}[a]
    return L(
        ("narrateur", lead),
        ("enfant-f", "Ici, ça brille, Aniss."),
        ("enfant-f", "Tu t'assois, et on tourne."),
        ("enfant-m", "Je galope, trop fort !"),
        ("narrateur", "Le cheval doré penche, un tout petit peu."),
        ("narrateur", mishap),
        ("narrateur", f"{name} attend au bord, un peu seule."),
        ("narrateur", "Sarah serre la selle, les dents serrées."),
        ("maman", "Son élan remplit tout le tour."),
        ("papa", "Toi tu vas plus loin, lui plus vite."),
        ("enfant-m", "On tourne comment, alors ?"),
        ("papa", "Vous trouvez, tous les deux ?"),
    )


T2_FN = {1: t2_file, 2: t2_step, 3: t2_horse}


def t3_choice(b: int) -> list[tuple[str, str]]:
    if b == 1:
        return L(
            ("narrateur", "Aniss saute entre les pieds de la file."),
            ("papa", "Le petit saut, le banc, ou ma poche ?"),
        )
    if b == 2:
        return L(
            ("narrateur", "Le marchepied attend, trop vif sous les pieds."),
            ("maman", "Les deux ombres, la marche, ou mon écharpe ?"),
        )
    return L(
        ("narrateur", "La crinière d'or attend, un peu penchée."),
        ("papa", "La valse, l'arrêt, ou ma barre ?"),
    )


OBJ = {
    1: dict(lab="le ticket bleu", cap="Le ticket bleu", short="ticket"),
    2: dict(lab="l'écharpe à pois", cap="L'écharpe à pois", short="écharpe"),
    3: dict(lab="la clochette", cap="La clochette", short="clochette"),
}


def t3_scene(a: int, b: int, c: int) -> list[tuple[str, str]]:
    o = OBJ[a]
    # file + play
    if b == 1 and c == 1:
        play = {
            1: "Ils se passent le ticket, dans la file.",
            2: "Ils se passent un pois, dans la file.",
            3: "Ils se passent la clochette, dans la file.",
        }[a]
        return L(
            ("enfant-f", "On saute avec toi, Aniss."),
            ("enfant-m", "À moi, puis à toi !"),
            ("narrateur", play),
            ("narrateur", "Les pieds d'Aniss dansent, pile avec le jeu."),
            ("narrateur", "Sarah avance d'un pas, pile au milieu."),
            ("papa", "Vous avez joué, et la file tient."),
            ("maman", "Ses jambes ont eu leur tour, dans le jeu."),
            ("narrateur", f"{o['cap']} reste dans la paume."),
            ("enfant-f", "On avance, maintenant."),
        )
    # file + wait
    if b == 1 and c == 2:
        wait = {
            1: "Aniss s'assoit près du kiosque, le ticket sur le genou.",
            2: "Aniss s'assoit près du kiosque, un pois sous la main.",
            3: "Aniss s'assoit près du kiosque, la clochette muette.",
        }[a]
        return L(
            ("enfant-f", "On attend un peu, Aniss."),
            ("enfant-m", "J'attends, je souffle."),
            ("narrateur", wait),
            ("narrateur", "La file repose, toute ronde, toute sage."),
            ("narrateur", "Sarah replace le pas, sans tirer."),
            ("papa", "Tes pieds ont su s'asseoir."),
            ("maman", "Le tour a eu la place."),
            ("narrateur", f"{o['cap']} ne bouge plus."),
            ("enfant-f", "Maintenant, c'est à nous."),
        )
    # file + ask
    if b == 1 and c == 3:
        hold = {
            1: "Papa tient le ticket, hors de la file.",
            2: "Papa tient le ticket, près de l'écharpe.",
            3: "Papa tient le ticket, loin de la clochette.",
        }[a]
        return L(
            ("enfant-f", "Papa, tu le tiens ?"),
            ("papa", "Je le tiens, Sarah."),
            ("narrateur", hold),
            ("narrateur", "Les mains d'Aniss sont libres, maintenant."),
            ("narrateur", "Sarah avance d'un pas, pile au milieu."),
            ("enfant-m", "Je t'aide, sans le ticket."),
            ("maman", "Vous avez demandé, et ça tient."),
            ("narrateur", f"{o['cap']} reste près d'eux."),
            ("enfant-f", "La file est prête."),
        )
    # step + play
    if b == 2 and c == 1:
        soft = {
            1: "Sarah pose le ticket, sans bruit, sur le bois.",
            2: "Sarah pose l'écharpe, sans bruit, sur le bois.",
            3: "Sarah pose la clochette, sans bruit, sur le bois.",
        }[a]
        return L(
            ("enfant-f", "On monte ensemble, Aniss."),
            ("enfant-m", "Toi derrière, moi devant !"),
            ("narrateur", soft),
            ("narrateur", "Deux ombres montent sur la même marche."),
            ("narrateur", "Aniss va plus vite, Sarah plus loin."),
            ("enfant-f", "On arrive en haut, tous les deux."),
            ("enfant-m", "J'ai attendu ta jambe, un peu."),
            ("papa", "Vous avez joué avec l'élan."),
            ("maman", "Le marchepied vous a laissés passer."),
        )
    # step + wait
    if b == 2 and c == 2:
        sit = {
            1: "Sarah tient le ticket, sur la marche.",
            2: "Sarah tient l'écharpe, sur la marche.",
            3: "Sarah tient la clochette, sur la marche.",
        }[a]
        return L(
            ("enfant-f", "On s'assoit un peu."),
            ("enfant-m", "Moi je m'assois, puis c'est toi."),
            ("narrateur", sit),
            ("narrateur", "Aniss pose les genoux sur le bois."),
            ("narrateur", "Il souffle, puis il se lève."),
            ("enfant-m", "C'est à toi, Sarah."),
            ("enfant-f", "Merci, j'y vais."),
            ("papa", "Chacun son tour, sur la marche."),
            ("maman", "L'élan a attendu le bois."),
        )
    # step + ask
    if b == 2 and c == 3:
        scarf = {
            1: "Maman tient l'écharpe, près du ticket.",
            2: "Maman tient l'écharpe, dans sa paume.",
            3: "Maman tient l'écharpe, près de la clochette.",
        }[a]
        return L(
            ("enfant-f", "Maman, tu tiens l'écharpe ?"),
            ("maman", "Je la donne, un coup chacun."),
            ("narrateur", scarf),
            ("narrateur", "Aniss la reçoit, monte un pas."),
            ("narrateur", "Sarah la reçoit, monte plus loin."),
            ("enfant-m", "On demande, et ça va !"),
            ("enfant-f", "Le haut est à nous."),
            ("papa", "Vous avez demandé, sans tirer."),
            ("maman", "Ma main a juste attendu."),
        )
    # horse + play
    if b == 3 and c == 1:
        song = {
            1: "Le ticket bleu voyage dans la poche, entre deux notes.",
            2: "L'écharpe à pois voyage au cou, entre deux notes.",
            3: "La clochette voyage au poignet, entre deux notes.",
        }[a]
        return L(
            ("enfant-f", "On chante, Aniss."),
            ("enfant-m", "La la la, j'avance !"),
            ("narrateur", "Sarah pose une main sur l'épaule d'Aniss."),
            ("narrateur", song),
            ("narrateur", "Ils chantent la même valse, l'un près de l'autre."),
            ("enfant-f", "Doucement, le cheval tient."),
            ("enfant-m", "La musique suit, puis se tait."),
            ("papa", "Vous jouez avec le bruit, ensemble."),
            ("maman", "Le tour est devenu une chanson."),
        )
    # horse + wait
    if b == 3 and c == 2:
        hush = {
            1: "Le ticket bleu reste muet, au creux.",
            2: "L'écharpe à pois reste muette, au creux.",
            3: "La clochette reste muette, au creux.",
        }[a]
        return L(
            ("enfant-f", "On attend l'arrêt."),
            ("enfant-m", "Quand il s'arrête, on galope un peu."),
            ("narrateur", hush),
            ("narrateur", "Le cheval doré ralentit, tout seul."),
            ("narrateur", "Aniss souffle, puis il ouvre les mains."),
            ("enfant-m", "C'est à nous, maintenant."),
            ("enfant-f", "Un tour, sans galoper."),
            ("papa", "Vous avez attendu la musique."),
            ("maman", "L'élan a écouté le bois."),
        )
    # horse + ask
    bar = {
        1: "Papa tient la barre, près du ticket.",
        2: "Papa tient la barre, près de l'écharpe.",
        3: "Papa tient la barre, près de la clochette.",
    }[a]
    return L(
        ("enfant-f", "Papa, tu tiens la barre ?"),
        ("papa", "Je la tiens, tout ferme."),
        ("narrateur", bar),
        ("narrateur", "Aniss pose les deux mains, tout près."),
        ("narrateur", "Sarah pose les siennes, plus loin."),
        ("enfant-m", "On demande, et ça tient !"),
        ("enfant-f", "La crinière est à nous."),
        ("maman", "Vous avez demandé, sans galoper."),
        ("papa", "Ma barre a juste attendu."),
    )


def ending(a: int, b: int, c: int) -> list[tuple[str, str]]:
    o = OBJ[a]
    # 27 textually distinct closings: unique last image + unique recap.
    if b == 1 and c == 1:
        keep = {
            1: "Le ticket bleu garde un grain de sucre.",
            2: "L'écharpe à pois garde un grain de sucre.",
            3: "La clochette garde un grain de sucre.",
        }[a]
        last = {
            1: "Un rai orange s'endort sur la crinière.",
            2: "Le cuivre redevient doux, autour des pois.",
            3: "Un toc de sucre sèche sur la clochette.",
        }[a]
        return L(
            ("narrateur", "La file s'ouvre, enfin, vers le bois peint."),
            ("enfant-m", "On a sauté, puis on a avancé."),
            ("enfant-f", "Tes pieds ont dansé avec le jeu."),
            ("papa", "Vous l'avez, le tour."),
            ("maman", "La gaufre attend au kiosque, tiède."),
            ("narrateur", keep),
            ("enfant-f", "On reste un peu, Aniss."),
            ("narrateur", last),
        )
    if b == 1 and c == 2:
        last = {
            1: "Un pois de sucre colle aux cheveux d'Aniss.",
            2: "Le kiosque sent la gaufre, et le pois se tait.",
            3: "Un tintement mince s'endort près du kiosque.",
        }[a]
        return L(
            ("narrateur", "Au bord de la file, deux têtes se calment."),
            ("enfant-f", "Aniss, tu as su t'asseoir."),
            ("enfant-m", "Oui, tout près de tes mains."),
            ("papa", "Toi debout, lui assis, ça tenait."),
            ("maman", "Vos voix sont devenues toutes petites."),
            ("narrateur", f"{o['cap']} reste dans la paume de Sarah."),
            ("enfant-m", "Je reste un peu."),
            ("narrateur", last),
        )
    if b == 1 and c == 3:
        keep = {
            1: "Le ticket bleu retombe, tout léger.",
            2: "L'écharpe à pois retombe, toute légère.",
            3: "La clochette retombe, toute légère.",
        }[a]
        last = {
            1: "Un pois d'or veille près des chevaux peints.",
            2: "La valse se tait contre le bois peint.",
            3: "La clochette retombe, légère, contre le poignet.",
        }[a]
        return L(
            ("narrateur", "Papa rend le ticket, sans le plier."),
            ("enfant-m", "Il est tombé vers nous."),
            ("enfant-f", "On a demandé, tous les deux."),
            ("maman", "Il n'était plus trop loin."),
            ("papa", "Le papier froisse dans l'air, un peu."),
            ("narrateur", keep),
            ("enfant-f", "On souffle dessus, sans sauter."),
            ("narrateur", last),
        )
    if b == 2 and c == 1:
        keep = {
            1: "Le ticket bleu garde un brin de poussière.",
            2: "L'écharpe à pois garde un brin de poussière.",
            3: "La clochette garde un brin de poussière.",
        }[a]
        last = {
            1: "L'ombre du cheval s'allonge, puis s'arrête.",
            2: "Un brin de poussière reste au pois du pull.",
            3: "La clochette garde un brin de poussière chaude.",
        }[a]
        return L(
            ("narrateur", "Sur le marchepied, ça sent le bois chaud."),
            ("enfant-m", "Mes pieds savaient le chemin."),
            ("enfant-f", "Moi, je montais plus loin."),
            ("papa", "Vous avez suivi ce qui était à vous."),
            ("maman", "Un brin de poussière reste au pull."),
            ("narrateur", keep),
            ("enfant-f", "Il est pour demain, le tour."),
            ("enfant-m", "Il est un peu chaud."),
            ("narrateur", last),
        )
    if b == 2 and c == 2:
        last = {
            1: "Une vis grince, puis se tait sur le bois.",
            2: "Le pois sèche près du kiosque, sur le bois.",
            3: "Une vis se tait, et la clochette aussi.",
        }[a]
        return L(
            ("narrateur", "Deux genoux restent, comme deux murs."),
            ("enfant-f", "J'ai poussé d'en bas."),
            ("enfant-m", "Tes bras étaient assez longs."),
            ("maman", "Le bois sent fort, sur vos mains."),
            ("papa", "Frottez-les sur le pantalon, sans frotter trop."),
            ("narrateur", f"{o['cap']} garde un brin de poussière."),
            ("enfant-m", "Je le tiens, Sarah."),
            ("narrateur", last),
        )
    if b == 2 and c == 3:
        keep = {
            1: "Le ticket bleu marque encore le bois.",
            2: "L'écharpe à pois marque encore le bois.",
            3: "La clochette marque encore le bois.",
        }
        # "encore" is banned! rewrite
        keep = {
            1: "Le ticket bleu marque le bois, une petite ligne.",
            2: "L'écharpe à pois marque le bois, un pois à la fois.",
            3: "La clochette marque le bois d'un toc heureux.",
        }[a]
        last = {
            1: "Le pois reste au chaud, sur la marche.",
            2: "L'écharpe marque le bois, un pois à la fois.",
            3: "La clochette marque le bois d'un toc heureux.",
        }[a]
        # last for a=2 and keep for a=2 same - need unique last
        last = {
            1: "Le pois reste au chaud, sur la marche.",
            2: "Une voix en haut, une voix en bas, puis plus.",
            3: "Le toc heureux s'endort sur la marche.",
        }[a]
        return L(
            ("narrateur", "Une voix en haut, une voix en bas, puis plus."),
            ("enfant-f", "Maman a tendu l'écharpe."),
            ("enfant-m", "On s'est parlé à travers."),
            ("papa", "Le marchepied vous a laissé la place."),
            ("maman", "Le secret tient, tout chaud."),
            ("narrateur", keep),
            ("enfant-f", "Regarde-le, Aniss, il brille."),
            ("enfant-m", "Je le vois, d'ici."),
            ("narrateur", last),
        )
    if b == 3 and c == 1:
        keep = {
            1: "Le ticket bleu pèse dans la poche, un peu lourd.",
            2: "L'écharpe à pois pèse au cou, un peu lourde.",
            3: "La clochette pèse au poignet, un peu lourde.",
        }[a]
        last = {
            1: "Un rai d'or traverse le ticket, dans la poche.",
            2: "Un rai d'or traverse un pois, sur le cou.",
            3: "La valse redevient petite, près du poignet.",
        }[a]
        return L(
            ("narrateur", "Les talons d'Aniss sont chauds, sur le bois."),
            ("enfant-f", "Tu as chanté pour moi."),
            ("enfant-m", "Tu tenais mon épaule."),
            ("maman", "La crinière sent le vernis, tout près."),
            ("papa", "Le tour est à vous, maintenant."),
            ("narrateur", keep),
            ("narrateur", "Sarah la pose contre le bois peint."),
            ("narrateur", last),
        )
    if b == 3 and c == 2:
        last = {
            1: "La crinière garde une ombre de ticket, toute proche.",
            2: "La crinière garde le pois, contre le vent.",
            3: "La crinière cache la clochette, un instant.",
        }[a]
        return L(
            ("narrateur", "Sur le cheval, deux paires de pieds se touchent."),
            ("enfant-m", "Tu as attendu l'arrêt."),
            ("enfant-f", "Tes mains ont su ralentir."),
            ("papa", "Chacun a fait sa part, à son rythme."),
            ("maman", "Le tissu de l'écharpe sèche, au vent."),
            ("narrateur", f"{o['cap']} pose une ombre au bois."),
            ("enfant-m", "Il brille trop, Sarah."),
            ("enfant-f", "C'est pour ça."),
            ("narrateur", last),
        )
    last = {
        1: "L'or tremble un peu, puis s'endort.",
        2: "L'or s'endort dans un pois de l'écharpe.",
        3: "L'or tremble, et la clochette ne dit plus rien.",
    }[a]
    coda = {
        1: "Le ticket bleu rentre dans la poche.",
        2: "L'écharpe à pois rentre autour du cou.",
        3: "La clochette rentre au poignet.",
    }[a]
    return L(
        ("narrateur", "Un peu de vernis reste aux paumes."),
        ("enfant-f", "On a tenu ensemble."),
        ("enfant-m", "Sans trop galoper."),
        ("papa", "La barre est restée à sa place."),
        ("maman", "Vos mains sentent le bois, un peu sucré."),
        ("narrateur", coda),
        ("enfant-m", "Tu l'as eue, enfin."),
        ("enfant-f", "Elle est à nous."),
        ("narrateur", last),
    )


T3_SONS = {1: "pas,rire", 2: "bois,souffle", 3: "valse,bois"}
FIN_SONS = {1: "gaufre,valse", 2: "bois,gaufre", 3: "valse,criniere"}


def build() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "valse,gaufre", "emphasis": "crinière"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Trois affaires attendent près du kiosque sucré."),
            ("maman", "Tu prends quoi d'abord, Sarah ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "le ticket bleu",
            "option_2_label": "l'écharpe à pois",
            "option_3_label": "la clochette",
        }},
    )

    for a, t1 in T1.items():
        base = f"CHK_T0001_P000{a}"
        by[base] = voice(
            by_old[base], t1["passage"], "action",
            extra={"sons": t1["sons"], "emphasis": t1["emphasis"]},
        )
        qid = f"{base}_Q0001"
        by[qid] = voice(
            by_old[qid],
            L(
                ("narrateur", t1["question"]),
                ("maman", "C'est où, maintenant ?"),
            ),
            "clue",
            extra={"sons": "", "emphasis": t1["emphasis"], "fields": {
                "expected_answer": t1["expected"],
                "accepted_examples": t1["accepted"],
                "retry_prompt": t1["retry"],
                "engine_ok_text": t1["ok"],
                "engine_near_text": "Tu es tout près. Reprenons l'indice.",
            }},
        )
        cid = f"{base}_C0001"
        by[cid] = voice(
            by_old[cid], t1["confirm"], "confirm",
            extra={"sons": "", "emphasis": "Merci"},
        )
        tid = f"{base}_T0002_P0000"
        by[tid] = voice(
            by_old[tid], t1["choice"], "choice",
            extra={"sons": "", "fields": {
                "option_1_label": "la file",
                "option_2_label": "le marchepied",
                "option_3_label": "le cheval doré",
            }},
        )
        for b in (1, 2, 3):
            p2 = f"{base}_T0002_P000{b}"
            by[p2] = voice(
                by_old[p2], T2_FN[b](a), "obstacle",
                extra={"sons": T2_SONS[b], "emphasis": t1["emphasis"]},
            )
            t3q = f"{p2}_T0003_P0000"
            labs = T3_LABS[b]
            by[t3q] = voice(
                by_old[t3q], t3_choice(b), "choice",
                extra={"sons": "", "fields": {
                    "option_1_label": labs[0],
                    "option_2_label": labs[1],
                    "option_3_label": labs[2],
                }},
            )
            for c in (1, 2, 3):
                leaf = f"{p2}_T0003_P000{c}"
                by[leaf] = voice(
                    by_old[leaf], t3_scene(a, b, c), "resolution",
                    extra={"sons": T3_SONS[c], "emphasis": OBJ[a]["short"]},
                )
                fin = f"{leaf}_F0001"
                by[fin] = voice(
                    by_old[fin], ending(a, b, c), "ending",
                    extra={"sons": FIN_SONS[c], "emphasis": "crinière"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra_ids = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    fins = [by[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(set(fins)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fins))}/27")

    out = dict(src)
    out["fil_rouge"] = FIL
    out["title"] = TITLE
    out["characters"] = "Sarah, Aniss, papa, maman"
    out["setting"] = "fête du village : file, marchepied, cheval doré"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    low = "\n".join(c["script"] for c in out["chunks"]).lower()
    labels = " ".join(
        f"{c.get('option_1_label') or ''} {c.get('option_2_label') or ''} {c.get('option_3_label') or ''}"
        for c in out["chunks"]
    ).lower()
    whole = low + "\n" + labels
    for bad in (
        "on va apprendre", "voici le geste", "l'histoire est finie",
        "ce n'est pas une faute", "beaucoup d'énergie",
        "la première", "la deuxième", "la troisième",
        "bravo tu as", "bon travail", "sami", "lina",
        "il ne faut pas", "hyperactif", "camarade qui bouge",
        "capitaine", "plic", "volet jaune", "bac à sable",
        "toboggan", "balançoires", "marelle", "papillon",
        "dans le jardin", "la boutique", "tout doux", "tout calme",
    ):
        if bad in whole:
            raise SystemExit(f"{SID} slogan: {bad}")
    n_enc = len(re.findall(r"\bencore\b", low))
    n_dej = len(re.findall(r"\bdéjà\b", low))
    if n_enc > 0 or n_dej > 0:
        raise SystemExit(f"{SID} tics encore={n_enc} déjà={n_dej}")
    if "sarah" not in low:
        raise SystemExit(f"{SID}: Sarah absente")
    if "aniss" not in low:
        raise SystemExit(f"{SID}: Aniss absent")
    for c in out["chunks"]:
        if c.get("kind") != "passage_fin":
            continue
        last_n = [x for x in c["script"].splitlines() if x.startswith("narrateur|")]
        last = last_n[-1].split("|", 1)[1].lower()
        if "histoire" in last or "bravo" in last or "bon travail" in last:
            raise SystemExit(f"{SID} {c['chunk_id']} fin mécanique: {last}")
        if not c.get("text_xai_tags"):
            raise SystemExit(f"{SID} {c['chunk_id']} sans text_xai_tags")
        if not c.get("notes"):
            raise SystemExit(f"{SID} {c['chunk_id']} sans notes")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        f"# {SID} — {TITLE}\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Vécu\n"
        "Fête du village, kiosque aux gaufres, valse de cuivre, chevaux peints or et rouge. "
        "Sarah veut un tour sur le cheval doré, avec Aniss, tout de suite. "
        "Elle le tire : Aniss bondit, le ticket tombe, le cheval part sans eux. "
        "T1 = ticket bleu (poche) / écharpe à pois (cou) / clochette (poignet) : "
        "premier geste trop vite, l'objet s'envole, s'accroche ou tinte trop fort. "
        "T2 = file (sauts, chapeau, objet qui glisse) / marchepied (bond, vis, poussière) / "
        "cheval doré (galop, crinière qui penche). Tenir Aniss échoue. "
        "T3 = neuf résolutions concrètes : petit saut / banc du kiosque / poche de papa ; "
        "deux ombres / marche de bois / écharpe de maman ; "
        "petite valse / arrêt du cheval / barre de papa. "
        "L'élan d'Aniss se voit (genoux, pieds, galop), jamais nommé en slogan. "
        "27 fins distinctes : grain de sucre, pois d'or, vis, vernis, crinière qui se tait. "
        "Autre récit que TREE-DIF-038 (carrousel de fête, pas cheval de bois sous l'auvent).\n\n"
        "## Vu et corrigé\n"
        "- Titre noyau conservé. N2 ≤ 15. Troupe D16 : Sarah, Aniss, papa, maman.\n"
        "- Première idée échoue (course vers le bois). Choix T1/T2/T3 changent l'action.\n"
        "- T3 Tom/Léa/Sami et « tout doux » → objets/lieux neutres.\n"
        "- Leçon DIF.ENE.001 vécue, pas récitée. Pas « camarade qui bouge / pas une faute ».\n"
        "- Tics « tout doux / encore / déjà / tout calme » retirés.\n"
        "- Un merci vécu par chemin (ticket sauvé / pois noué / valse laissée), pas un refrain Bravo.\n"
        "- 27 fins textuellement distinctes. Fin paie la crinière, la gaufre, l'objet.\n"
        "- TTS par chunk (opening/choice/clue/confirm/action/obstacle/resolution/ending).\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés. Pas apply.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(f"OK {SID} {nwords} mots  fins={len(set(fins))}")


if __name__ == "__main__":
    build()
