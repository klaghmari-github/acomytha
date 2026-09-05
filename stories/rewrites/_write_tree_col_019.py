#!/usr/bin/env python3
"""TREE-COL-019 — La vitre embuée de Victorino (F-NAR-019)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-COL-019"
LIM = 15
TICS = (
    "tout doux",
    "tout calme",
    "on lève la main",
    "puis on parle",
    "c'est du bon travail",
    "on va apprendre",
    "si malaise",
    "l'histoire est finie",
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
        note="arc=installation; intention=émerveiller; emotion=impatience; intensite=1; destinataire=enfant; sous_texte=l_ancre_va_s_effacer; tempo=naturel; sourire=léger; respiration=ample",
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
        note="arc=confirmation; intention=relancer; emotion=soulagement; intensite=1; destinataire=enfant; sous_texte=la_phrase_a_eu_sa_place; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=trop_vite_la_buee_part; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=decouragement; intensite=2; destinataire=enfant; sous_texte=couper_efface_l_ancre; tempo=resserre; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=resolution; intention=faire_vivre_la_reussite; emotion=fierte_calme; intensite=2; destinataire=enfant; sous_texte=demander_a_ouvert_le_quai; tempo=naturel; sourire=franc; respiration=relachee",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierte_calme; intensite=1; destinataire=enfant; sous_texte=l_ancre_a_trouve_le_bateau; tempo=pose; sourire=léger; respiration=ample",
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
        if re.search(r"\bencore\b", low) or re.search(r"\bdéjà\b", low) or re.search(r"\bdeja\b", low):
            raise SystemExit(f"{where} tic encore/déjà: {ph}")
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
    out: list[tuple[str, str]] = []
    for role, ph in rows:
        parts = re.findall(r".+?[.!?]", ph.strip())
        leftover = ph.strip()
        for p in parts:
            leftover = leftover.replace(p, "", 1)
        if leftover.strip():
            raise SystemExit(f"reste {leftover!r}: {ph}")
        if not parts:
            raise SystemExit(f"sans phrase: {ph}")
        for part in parts:
            out.append((role, part.strip()))
    return out


OPENING = L(
    ("narrateur", "Victorino connaît la vitre de la cuisine, son tic, son froid."),
    ("narrateur", "Le rideau jaune a des petits bateaux."),
    ("narrateur", "Le radiateur chante un tic irrégulier."),
    ("narrateur", "Ça sent le pain grillé, un peu brûlé."),
    ("narrateur", "Une miette dort sur la table ronde."),
    ("narrateur", "Dehors, un oiseau tape le rebord."),
    ("narrateur", "Un détail paraît nouveau, tout contre le verre."),
    ("narrateur", "Dans la buée, une ancre minuscule brille, claire."),
    ("narrateur", "Une goutte l'a dessinée, sans le vouloir."),
    ("narrateur", "Près du quai des rideaux, un bateau de carton attend."),
    ("narrateur", "Il est bleu, un peu bosselé."),
    ("narrateur", "Un fil de laine rouge tic contre le carton."),
    ("enfant-m", "Il glisse jusqu'à l'ancre, avant le soleil !"),
    ("narrateur", "Nina tient un chiffon de lin beige."),
    ("copine", "Moi, je veux voir l'oiseau."),
    ("copine", "Je l'essuie."),
    ("narrateur", "En ce moment, Victorino ouvre la bouche trop vite."),
    ("enfant-m", "C'est mon quai !"),
    ("narrateur", "Papa parle à maman, près du pain."),
    ("papa", "Le pain est chaud."),
    ("papa", "Tu en veux ?"),
    ("narrateur", "Les mots se cognent."),
    ("narrateur", "Personne n'entend le bateau."),
    ("narrateur", "Nina passe le chiffon."),
    ("narrateur", "La buée part."),
    ("narrateur", "L'ancre minuscule s'efface."),
    ("narrateur", "Le bateau bascule."),
    ("enfant-m", "Non !"),
    ("narrateur", "Le sourire de Victorino disparaît."),
    ("narrateur", "Dans sa poitrine, l'envie et l'inquiétude se bousculent."),
    ("maman", "On t'écoute."),
    ("maman", "Qu'est-ce qui est tombé ?"),
    ("enfant-m", "Mon bateau."),
    ("enfant-m", "L'ancre."),
    ("papa", "On peut recommencer, plus lentement ?"),
    ("narrateur", "Le fil rouge traîne, un peu mouillé."),
)

T1 = {
    1: dict(
        name="la cuisine",
        passage=L(
            ("narrateur", "Victorino reste au quai des rideaux jaunes."),
            ("narrateur", "Le carrelage pique sous les chaussons."),
            ("narrateur", "Il souffle sur la vitre, trop fort."),
            ("narrateur", "Un nuage informe cache le jardin."),
            ("enfant-m", "Reviens, ancre !"),
            ("narrateur", "Nina lève le chiffon, prête à tout essuyer."),
            ("copine", "Je ne vois plus l'oiseau."),
            ("narrateur", "Victorino veut crier."),
            ("narrateur", "Les mots lui montent."),
            ("narrateur", "Il les ravale."),
            ("narrateur", "Ses poings se serrent, puis s'ouvrent."),
            ("enfant-m", "S'il te plaît, on garde un coin de buée ?"),
            ("copine", "Un tout petit coin."),
            ("copine", "D'accord."),
            ("papa", "Je m'accroupis."),
            ("papa", "Ton bateau, il veut aller où ?"),
            ("enfant-m", "Jusqu'à l'ancre."),
            ("enfant-m", "Celle de tout à l'heure."),
            ("maman", "Merci d'avoir demandé, au lieu de prendre."),
            ("narrateur", "Un souffle plus fin recommence, sur le verre."),
        ),
        question="Quelle forme avait la petite marque dans la buée ?",
        expected="ancre",
        accepted="ancre | une ancre | ancre minuscule | petite ancre | l'ancre",
        retry="Regarde la forme claire, dans la buée.",
        ok="Oui, c'était une ancre.",
        confirm=L(
            ("enfant-m", "Une ancre !"),
            ("narrateur", "Oui, une ancre minuscule, claire."),
            ("papa", "J'ai entendu toute ta phrase."),
            ("narrateur", "Nina pose le chiffon, loin de la vitre."),
            ("narrateur", "Un trait mince revient, presque."),
        ),
        sons="casserole,goutte",
        choice=L(
            ("narrateur", "Trois jeux peuvent aider le bateau, ici."),
            ("maman", "Les cubes, le livre, ou la dînette ?"),
        ),
    ),
    2: dict(
        name="le jardin",
        passage=L(
            ("narrateur", "Victorino ouvre la porte du jardin, le bateau au poing."),
            ("narrateur", "L'air pique."),
            ("narrateur", "L'herbe brille, courte."),
            ("narrateur", "Dehors, la vitre n'a plus de buée."),
            ("narrateur", "On voit le rideau jaune, à l'envers."),
            ("enfant-m", "Mon ancre, elle est où ?"),
            ("narrateur", "Nina court vers le rebord."),
            ("copine", "L'oiseau d'abord."),
            ("copine", "Il picore !"),
            ("narrateur", "Victorino veut crier par-dessus."),
            ("narrateur", "Sa phrase se casse."),
            ("narrateur", "Le fil rouge s'alourdit, mouillé."),
            ("papa", "Un à la fois."),
            ("papa", "Nina finit, puis toi."),
            ("narrateur", "Il attend."),
            ("narrateur", "L'oiseau saute, puis s'en va."),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "On cherche l'ancre, de ce côté ?"),
            ("copine", "Oui."),
            ("copine", "Après l'oiseau."),
            ("maman", "Merci d'avoir laissé sa phrase aller au bout."),
            ("narrateur", "Une goutte du toit frappe le carton bleu."),
        ),
        question="Qui picorait sur le rebord ?",
        expected="oiseau",
        accepted="oiseau | un oiseau | l'oiseau | le oiseau",
        retry="Écoute le petit coup, sur le rebord.",
        ok="Oui, c'était l'oiseau.",
        confirm=L(
            ("enfant-m", "Un oiseau !"),
            ("narrateur", "Oui, l'oiseau du rebord."),
            ("papa", "J'ai entendu le mot jusqu'au bout."),
            ("narrateur", "Nina range le chiffon dans sa poche."),
            ("narrateur", "Le bateau sent l'herbe, un peu."),
        ),
        sons="oiseau,porte",
        choice=L(
            ("narrateur", "Trois jeux peuvent aider, au jardin."),
            ("papa", "Les cubes, le livre, ou la dînette ?"),
        ),
    ),
    3: dict(
        name="la chambre",
        passage=L(
            ("narrateur", "Victorino entre dans la chambre, trop vite."),
            ("narrateur", "Le tapis étouffe ses pas."),
            ("narrateur", "La vitre du lit a sa propre buée, plus fine."),
            ("enfant-m", "Un autre quai !"),
            ("narrateur", "Nina veut le doudou gris, sur l'oreiller."),
            ("copine", "D'abord le doudou."),
            ("copine", "Il a froid."),
            ("narrateur", "Deux envies se heurtent."),
            ("narrateur", "Le bateau glisse sous le lit."),
            ("enfant-m", "Il est à moi !"),
            ("narrateur", "Les mots tapent trop fort."),
            ("narrateur", "Nina se recule."),
            ("maman", "On reprend."),
            ("maman", "Une voix, puis l'autre."),
            ("narrateur", "Victorino ramasse le bateau, les joues chaudes."),
            ("enfant-m", "S'il te plaît."),
            ("enfant-m", "Je vais à la vitre, après le doudou ?"),
            ("copine", "D'accord."),
            ("copine", "Je le réchauffe."),
            ("papa", "Merci."),
            ("papa", "Là, on a tout entendu."),
            ("narrateur", "Un rai pâle touche le fil rouge."),
        ),
        question="De quelle couleur est le fil du bateau ?",
        expected="rouge",
        accepted="rouge | il est rouge | fil rouge | laine rouge",
        retry="Regarde le fil, contre le carton.",
        ok="Oui, le fil est rouge.",
        confirm=L(
            ("enfant-m", "Rouge !"),
            ("narrateur", "Oui, un fil de laine rouge."),
            ("maman", "J'ai entendu ta couleur."),
            ("narrateur", "Nina berce le doudou, sans parler."),
            ("narrateur", "La buée du lit attend, très mince."),
        ),
        sons="tissu,pas",
        choice=L(
            ("narrateur", "Trois jeux peuvent aider, dans la chambre."),
            ("maman", "Les cubes, le livre, ou la dînette ?"),
        ),
    ),
}


def t2_cubes(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Victorino prend les cubes de bois, près de la miette."),
            ("narrateur", "Ils sentent le sapin."),
            ("enfant-m", "Un quai, pour que le bateau n'attende plus par terre !"),
            ("narrateur", "Nina veut le cube rouge, pour une tour."),
            ("copine", "Le mien d'abord !"),
            ("narrateur", "Deux mains tirent."),
            ("narrateur", "La tour s'écroule."),
            ("narrateur", "Le cube rouge cache le trait de buée."),
            ("enfant-m", "Mon ancre !"),
            ("narrateur", "Il refuse de foncer."),
            ("narrateur", "Il pose les mains à plat."),
            ("papa", "Une brique après l'autre."),
            ("enfant-m", "S'il te plaît, le rouge, pour le bout du quai ?"),
            ("copine", "Prends-le."),
            ("narrateur", "Dans le grain du bois, une ancre minuscule apparaît."),
        )
    if a == 2:
        return L(
            ("narrateur", "Victorino pose les cubes sur la pierre mouillée."),
            ("narrateur", "Un cube glisse, tout savon."),
            ("enfant-m", "Le quai, vite !"),
            ("narrateur", "Nina veut une tour haute, contre l'arrosoir."),
            ("copine", "Plus haut que l'herbe !"),
            ("narrateur", "Le cube du bas part de travers."),
            ("narrateur", "Le bateau bascule dans une flaque."),
            ("enfant-m", "Il va couler !"),
            ("narrateur", "Il s'arrête."),
            ("narrateur", "Il écoute le tic du fil mouillé."),
            ("maman", "On le relève sans se bousculer ?"),
            ("enfant-m", "S'il te plaît, ta tour à côté, pas dessus ?"),
            ("copine", "D'accord."),
            ("narrateur", "Une feuille collée au cube dessine une ancre, presque."),
        )
    return L(
        ("narrateur", "Victorino aligne les cubes sur le tapis, vers la vitre."),
        ("narrateur", "Le bois claque, trop fort pour la chambre."),
        ("enfant-m", "Un chemin jusqu'au quai du lit !"),
        ("narrateur", "Nina pose le doudou au milieu, comme un roc."),
        ("copine", "Il habite là."),
        ("narrateur", "Le bateau percute le museau gris."),
        ("narrateur", "Les cubes s'écartent."),
        ("enfant-m", "Pousse-toi !"),
        ("narrateur", "Le mot sort trop vite."),
        ("narrateur", "Nina serre le doudou."),
        ("papa", "On demande, on ne pousse pas."),
        ("enfant-m", "S'il te plaît, un passage étroit, juste pour le bateau ?"),
        ("copine", "Un tout petit."),
        ("narrateur", "Sur l'oreille du doudou, le fil rouge fait une ancre."),
    )


def t2_livre(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Victorino ouvre le livre, près du bol jaune."),
            ("narrateur", "Les pages sentent le pain."),
            ("enfant-m", "Le bateau de papier, il a une ancre !"),
            ("narrateur", "Nina tourne trop vite, vers l'oiseau dessiné."),
            ("copine", "Moi, l'oiseau !"),
            ("narrateur", "Deux pages se froissent."),
            ("narrateur", "Le bateau imprimé disparaît un instant."),
            ("enfant-m", "Reviens !"),
            ("narrateur", "Il referme presque le livre, puis le rouvre."),
            ("narrateur", "Il attend que Nina finisse l'oiseau."),
            ("maman", "Une image après l'autre."),
            ("enfant-m", "S'il te plaît, la page du bateau, après ?"),
            ("copine", "Oui."),
            ("narrateur", "Au bas de la coque, une ancre minuscule est dessinée."),
        )
    if a == 2:
        return L(
            ("narrateur", "Victorino pose le livre dans l'herbe courte."),
            ("narrateur", "Le vent tourne une page, tout seul."),
            ("enfant-m", "C'est mon bateau !"),
            ("narrateur", "Nina veut garder la page de l'oiseau, du doigt."),
            ("copine", "Il va s'envoler, celui du papier !"),
            ("narrateur", "Le doigt et le vent se battent."),
            ("narrateur", "Une fourmi traverse la marge."),
            ("enfant-m", "Pas maintenant, fourmi !"),
            ("narrateur", "Sa voix recouvre celle de Nina."),
            ("narrateur", "Il se tait, les épaules hautes."),
            ("papa", "Le vent a fini."),
            ("papa", "À qui la phrase ?"),
            ("enfant-m", "S'il te plaît, on cherche l'ancre sur la page ?"),
            ("narrateur", "Nina lève le doigt."),
            ("narrateur", "Sous l'oiseau, une ancre minuscule attendait."),
        )
    return L(
        ("narrateur", "Victorino ouvre le livre sur l'oreiller tiède."),
        ("narrateur", "Une page a le creux de la sieste."),
        ("enfant-m", "Histoire de bateau, tout de suite !"),
        ("narrateur", "Nina veut l'histoire du doudou, d'abord."),
        ("copine", "Lui a froid."),
        ("narrateur", "Deux titres se marchent dessus."),
        ("narrateur", "Le livre se referme, tout seul."),
        ("enfant-m", "Non !"),
        ("narrateur", "Il pose le carton bleu sur la couverture, et attend."),
        ("maman", "Un titre, puis l'autre."),
        ("enfant-m", "S'il te plaît, le bateau, après le doudou ?"),
        ("copine", "D'accord."),
        ("narrateur", "Au coin d'une page, une ancre minuscule est cachée."),
        ("narrateur", "Le fil rouge la montre, sans crier."),
    )


def t2_dinette(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Victorino prend la petite tasse, près du bol jaune."),
            ("narrateur", "Elle sonne, creuse."),
            ("enfant-m", "C'est le port !"),
            ("narrateur", "Nina veut verser, tout de suite."),
            ("copine", "Le thé d'abord !"),
            ("narrateur", "La tasse part de travers."),
            ("narrateur", "Le bateau manque le bord."),
            ("enfant-m", "Pas dans mon port !"),
            ("narrateur", "Les mots tapent la tasse."),
            ("narrateur", "Nina recule la cuillère."),
            ("papa", "On demande le tour de la tasse."),
            ("enfant-m", "S'il te plaît, un peu de vapeur, pas trop ?"),
            ("copine", "Juste un nuage."),
            ("narrateur", "La vapeur du vrai bol dessine une ancre, sur le verre."),
        )
    if a == 2:
        return L(
            ("narrateur", "Victorino pose la dînette dans l'herbe."),
            ("narrateur", "Une cuillère miniature brille, froide."),
            ("enfant-m", "Le port, dehors !"),
            ("narrateur", "Nina veut pique-niquer, tout de suite."),
            ("copine", "On mange."),
            ("copine", "Après, ton bateau."),
            ("narrateur", "Victorino attrape la tasse pendant qu'elle parle."),
            ("narrateur", "Un peu de rosée tombe dans le carton."),
            ("enfant-m", "Il est trop lourd !"),
            ("narrateur", "Il repose la tasse."),
            ("maman", "Sa phrase n'était pas finie."),
            ("enfant-m", "S'il te plaît, le port après une bouchée ?"),
            ("copine", "Une bouchée."),
            ("narrateur", "Dans la rosée de la cuillère, une ancre minuscule tremble."),
        )
    return L(
        ("narrateur", "Victorino installe la dînette au pied du lit."),
        ("narrateur", "La petite assiette attend sur le tapis."),
        ("enfant-m", "Goûter du bateau !"),
        ("narrateur", "Nina veut servir le doudou, d'abord."),
        ("copine", "Il a faim."),
        ("narrateur", "Deux services se heurtent."),
        ("narrateur", "La tasse roule sous l'oreiller."),
        ("enfant-m", "C'est mon port !"),
        ("narrateur", "Le mot est trop fort pour le soir naissant."),
        ("papa", "On cherche ensemble, sans crier."),
        ("enfant-m", "S'il te plaît, on sert le doudou, puis le bateau ?"),
        ("copine", "Oui."),
        ("narrateur", "Sous l'oreiller, la tasse a gardé un rond de buée, en ancre."),
        ("narrateur", "Le fil rouge y entre, tout seul."),
    )


T2_FN = {1: t2_cubes, 2: t2_livre, 3: t2_dinette}
T2_SONS = {1: "bois", 2: "page", 3: "tasse"}


def t3_choice(b: int) -> list[tuple[str, str]]:
    if b == 1:
        return L(
            ("narrateur", "Le quai de cubes change selon l'heure."),
            ("maman", "Le matin, après la sieste, ou le soir ?"),
        )
    if b == 2:
        return L(
            ("narrateur", "La page du bateau attend une heure."),
            ("papa", "Le matin, après la sieste, ou le soir ?"),
        )
    return L(
        ("narrateur", "Le petit port de tasse attend une heure."),
        ("maman", "Le matin, après la sieste, ou le soir ?"),
    )


T3 = {
    (1, 1, 1): L(
        ("narrateur", "Le soleil touche le cube rouge, près de la miette."),
        ("narrateur", "La buée recule, trop vite."),
        ("enfant-m", "L'ancre va partir !"),
        ("narrateur", "Nina veut poser le dernier cube, au hasard."),
        ("copine", "Moi, le sommet !"),
        ("narrateur", "Victorino refuse de foncer."),
        ("narrateur", "Il regarde le grain du bois."),
        ("enfant-m", "S'il te plaît, on soulève le rouge ?"),
        ("narrateur", "Dessous, l'ancre minuscule du début est revenue."),
        ("papa", "On y est, tout juste."),
        ("narrateur", "Le bateau glisse."),
        ("narrateur", "Une virgule d'eau reste au flanc."),
    ),
    (1, 1, 2): L(
        ("narrateur", "Après la sieste, les cubes sont tièdes."),
        ("narrateur", "La vitre est sèche, trop nette."),
        ("enfant-m", "Plus d'ancre."),
        ("narrateur", "Nina veut une tour haute, quand même."),
        ("narrateur", "Victorino secoue la tête."),
        ("enfant-m", "S'il te plaît, on va près de la casserole ?"),
        ("maman", "Je verse."),
        ("narrateur", "Un nuage court."),
        ("narrateur", "Il manque de tout emporter."),
        ("narrateur", "Ils soufflent plus fin, ensemble."),
        ("narrateur", "L'ancre minuscule revient, pâle."),
        ("narrateur", "Le carton garde un anneau de vapeur."),
    ),
    (1, 1, 3): L(
        ("narrateur", "Au soir, la lampe fait un carré sur les cubes."),
        ("narrateur", "Une buée neuve naît, lente."),
        ("enfant-m", "On a le temps."),
        ("narrateur", "Nina a sommeil."),
        ("narrateur", "Son coude manque le quai."),
        ("enfant-m", "S'il te plaît, un cube, pas le coude ?"),
        ("copine", "Pardon."),
        ("papa", "On pose le dernier, sans bruit."),
        ("narrateur", "L'ancre minuscule s'allume dans le verre."),
        ("narrateur", "Le bateau s'amarre."),
        ("narrateur", "Le fil rouge brille, un peu humide."),
        ("maman", "Cette fois, ça a failli tomber."),
    ),
    (1, 2, 1): L(
        ("narrateur", "Le soleil chauffe la page du bateau."),
        ("narrateur", "La buée de la cuisine fond au bord."),
        ("enfant-m", "On copie l'ancre, vite !"),
        ("narrateur", "Nina veut l'oiseau, une dernière fois."),
        ("narrateur", "Victorino ouvre la bouche, puis la referme."),
        ("enfant-m", "S'il te plaît, après l'oiseau, on copie ?"),
        ("copine", "C'est bon."),
        ("narrateur", "Au bas de la coque, l'ancre minuscule est là."),
        ("narrateur", "Un souffle la pose sur le verre restant."),
        ("papa", "Pile avant le rayon."),
        ("narrateur", "Une miette colle à la proue."),
        ("narrateur", "Le bateau a mangé le pain, un peu."),
    ),
    (1, 2, 2): L(
        ("narrateur", "Après la sieste, le livre reste ouvert près du bol."),
        ("narrateur", "La vitre n'a plus rien à offrir."),
        ("enfant-m", "On n'y arrivera pas."),
        ("narrateur", "Nina pose son doigt sur l'ancre imprimée."),
        ("copine", "Elle est là, dans le livre."),
        ("narrateur", "Victorino refuse de gribouiller au hasard."),
        ("enfant-m", "S'il te plaît, un bol tiède, pour un nuage ?"),
        ("maman", "Je te le tends."),
        ("narrateur", "Un souffle, puis un autre."),
        ("narrateur", "L'ancre minuscule revient, à peine."),
        ("narrateur", "Le coin de la page a une trace de buée."),
        ("papa", "Ça a failli rester sur le papier, seulement."),
    ),
    (1, 2, 3): L(
        ("narrateur", "Au soir, maman lit tout bas, près de la lampe."),
        ("narrateur", "Victorino veut montrer la page pendant sa phrase."),
        ("narrateur", "Il attend le point."),
        ("enfant-m", "S'il te plaît, l'ancre du livre, sur la vitre ?"),
        ("maman", "Oui."),
        ("maman", "La lampe chauffe le verre."),
        ("narrateur", "Une buée ronde naît, comme un port."),
        ("narrateur", "Nina pose le doigt, sans essuyer."),
        ("narrateur", "L'ancre minuscule se dessine, nette."),
        ("papa", "On l'a eue, de justesse."),
        ("narrateur", "Le bateau veille dans l'ovale de la lampe."),
        ("narrateur", "La page reste ouverte, face au verre."),
    ),
    (1, 3, 1): L(
        ("narrateur", "Le soleil sèche le bord de la petite tasse."),
        ("narrateur", "Le port miniature devient trop chaud."),
        ("enfant-m", "Il ne peut plus s'arrêter !"),
        ("narrateur", "Nina veut verser le thé imaginaire, tout de suite."),
        ("narrateur", "Victorino pose la tasse, et attend."),
        ("enfant-m", "S'il te plaît, un peu du vrai bol, pour la vapeur ?"),
        ("maman", "Une cuillerée."),
        ("narrateur", "Le nuage manque de tout cacher."),
        ("narrateur", "Ils soufflent plus fin."),
        ("narrateur", "L'ancre minuscule apparaît au fond de la tasse."),
        ("papa", "Le port tient."),
        ("narrateur", "Une goutte de lait y dessine la même ancre."),
    ),
    (1, 3, 2): L(
        ("narrateur", "Après la sieste, la casserole miniature est froide."),
        ("narrateur", "La vitre, pareille : trop claire."),
        ("enfant-m", "Plus de port."),
        ("narrateur", "Nina secoue la tasse, impatiente."),
        ("narrateur", "Rien."),
        ("enfant-m", "S'il te plaît, de l'eau chaude, juste un nuage ?"),
        ("papa", "Je te verse, lentement."),
        ("narrateur", "La vapeur arrive tard."),
        ("narrateur", "Elle a failli ne pas venir."),
        ("narrateur", "L'ancre minuscule se pose sur le verre, pâle."),
        ("maman", "On a eu chaud."),
        ("narrateur", "Le chiffon beige garde une virgule mouillée."),
    ),
    (1, 3, 3): L(
        ("narrateur", "Au soir, un grain de sel reste dans l'assiette."),
        ("narrateur", "La lampe fait un rond jaune sur la tasse."),
        ("enfant-m", "Le port de nuit."),
        ("narrateur", "Nina veut goûter le sel, trop vite."),
        ("narrateur", "Victorino attend qu'elle recrache, gentiment."),
        ("enfant-m", "S'il te plaît, on souffle après le sel ?"),
        ("copine", "Beurk."),
        ("copine", "Oui."),
        ("narrateur", "La buée du soir encadre le bateau, sans l'effacer."),
        ("papa", "L'ancre minuscule est au milieu."),
        ("narrateur", "Le grain de sel brille, comme un phare."),
        ("maman", "Ça a failli tout piquer."),
    ),
    (2, 1, 1): L(
        ("narrateur", "Au matin, une goutte d'herbe mouille le cube vert."),
        ("narrateur", "Le soleil commence à lécher la pierre."),
        ("enfant-m", "Le quai va sécher !"),
        ("narrateur", "Nina veut empiler plus haut que l'arrosoir."),
        ("narrateur", "Victorino secoue la tête."),
        ("enfant-m", "S'il te plaît, un quai long, pas une tour ?"),
        ("copine", "Long, alors."),
        ("narrateur", "La feuille collée au cube montre l'ancre minuscule."),
        ("narrateur", "Le bateau s'aligne, juste avant le rayon."),
        ("papa", "De justesse."),
        ("narrateur", "Une plume du rebord reste sur le bois."),
        ("maman", "L'oiseau a laissé sa trace."),
    ),
    (2, 1, 2): L(
        ("narrateur", "Après la sieste, les cubes chauffent sur la pierre."),
        ("narrateur", "Plus de buée, nulle part."),
        ("enfant-m", "On est trop tard."),
        ("narrateur", "Nina souffle sur un cube, pour jouer."),
        ("narrateur", "Victorino la regarde, puis le verre, à l'envers."),
        ("enfant-m", "S'il te plaît, on souffle sur la vitre, de dehors ?"),
        ("copine", "Comme l'oiseau."),
        ("narrateur", "Deux souffles, puis un troisième."),
        ("narrateur", "Une ancre minuscule naît, à l'envers."),
        ("papa", "On la voit de ce côté."),
        ("narrateur", "Ça a failli rester un jeu de cubes, seulement."),
        ("narrateur", "Le carton a une tache d'herbe, au ventre."),
    ),
    (2, 1, 3): L(
        ("narrateur", "Au soir, un cube garde la chaleur du jour."),
        ("narrateur", "La fenêtre allumée fait un carré, dehors."),
        ("enfant-m", "Le quai de nuit."),
        ("narrateur", "Nina a froid aux doigts."),
        ("narrateur", "Elle veut rentrer, tout de suite."),
        ("enfant-m", "S'il te plaît, un cube, puis on rentre ?"),
        ("copine", "Un seul."),
        ("narrateur", "Dans la lumière, l'ancre minuscule apparaît sur le verre."),
        ("maman", "On la prend, et on rentre."),
        ("narrateur", "Le bateau s'amarre au cube chaud."),
        ("narrateur", "Le fil rouge sent la pierre."),
        ("papa", "Ça a failli rester dans le jardin, sans nous."),
    ),
    (2, 2, 1): L(
        ("narrateur", "Au matin, une fourmi passe au bord de la page."),
        ("narrateur", "Le soleil sèche l'encre, presque."),
        ("enfant-m", "L'ancre du livre, vite !"),
        ("narrateur", "Nina suit la fourmi du doigt."),
        ("narrateur", "Victorino attend la fin de la promenade."),
        ("enfant-m", "S'il te plaît, après la fourmi, l'ancre ?"),
        ("copine", "Elle est partie."),
        ("narrateur", "Sous l'oiseau imprimé, l'ancre minuscule attendait."),
        ("papa", "On souffle sur le verre, de dehors."),
        ("narrateur", "Elle se pose, à l'envers, nette."),
        ("narrateur", "Une patte de fourmi a laissé un grain de terre."),
        ("maman", "Le bateau a un caillou, maintenant."),
    ),
    (2, 2, 2): L(
        ("narrateur", "Après la sieste, le livre a une ombre ronde, sous l'arbre."),
        ("narrateur", "La vitre, vue d'ici, est trop claire."),
        ("enfant-m", "On a perdu l'ancre."),
        ("narrateur", "Nina veut dormir dans l'ombre, avec le livre."),
        ("narrateur", "Victorino refuse de fermer la page."),
        ("enfant-m", "S'il te plaît, on copie l'ancre, puis tu dors ?"),
        ("copine", "Deux minutes."),
        ("narrateur", "Ils soufflent."),
        ("narrateur", "Rien, d'abord."),
        ("narrateur", "Puis une ancre minuscule, très pâle."),
        ("papa", "Ça a failli rester une sieste, sans voyage."),
        ("narrateur", "L'ombre de l'arbre reste sur le carton bleu."),
    ),
    (2, 2, 3): L(
        ("narrateur", "Au soir, une page claque dans le vent."),
        ("narrateur", "La lampe de la cuisine allume le livre, dehors."),
        ("enfant-m", "L'ancre, avant que le vent parte !"),
        ("narrateur", "Nina veut rentrer le livre, tout de suite."),
        ("narrateur", "Victorino pose la main à plat, et attend le clac."),
        ("enfant-m", "S'il te plaît, une page, puis on rentre ?"),
        ("copine", "Celle de l'ancre."),
        ("narrateur", "Ils soufflent vers le verre allumé."),
        ("narrateur", "L'ancre minuscule s'y accroche."),
        ("maman", "On rentre."),
        ("narrateur", "Le bateau a un coin de page, un peu froissé."),
        ("papa", "Le vent a failli tout emporter."),
    ),
    (2, 3, 1): L(
        ("narrateur", "Au matin, la petite cuillère a un peu de rosée."),
        ("narrateur", "Le soleil la boit."),
        ("enfant-m", "Le port va sécher !"),
        ("narrateur", "Nina veut goûter la rosée, maintenant."),
        ("narrateur", "Victorino attend qu'elle ait fini."),
        ("enfant-m", "S'il te plaît, la tasse pour le bateau, après ?"),
        ("copine", "C'est sucré."),
        ("copine", "Tiens."),
        ("narrateur", "Dans la rosée, l'ancre minuscule tremble, puis tient."),
        ("papa", "On l'a vue, de justesse."),
        ("narrateur", "Une goutte reste dans la tasse, comme un bassin."),
        ("maman", "Le bateau y dort, le fil mouillé."),
    ),
    (2, 3, 2): L(
        ("narrateur", "Après la sieste, la dînette sent l'herbe coupée."),
        ("narrateur", "Plus de rosée."),
        ("enfant-m", "Le port est vide."),
        ("narrateur", "Nina veut ranger, tout de suite."),
        ("narrateur", "Victorino pose la tasse au soleil, puis la reprend."),
        ("enfant-m", "S'il te plaît, un peu d'eau de l'arrosoir ?"),
        ("papa", "Une goutte."),
        ("narrateur", "Pas plus."),
        ("narrateur", "Ils soufflent dessus, vers le verre."),
        ("narrateur", "Une ancre minuscule, à l'envers, apparaît."),
        ("maman", "Ça a failli partir dans le bac."),
        ("narrateur", "Le carton sent l'arrosoir, un peu métal."),
    ),
    (2, 3, 3): L(
        ("narrateur", "Au soir, un bol miniature reflète la fenêtre allumée."),
        ("narrateur", "Dehors, le froid gagne."),
        ("enfant-m", "Le port de nuit, dehors."),
        ("narrateur", "Nina claque des dents."),
        ("copine", "On rentre."),
        ("narrateur", "Victorino attend une seconde, le bateau au bord."),
        ("enfant-m", "S'il te plaît, un souffle, puis le manteau ?"),
        ("copine", "Un."),
        ("narrateur", "L'ancre minuscule se pose sur le reflet."),
        ("papa", "On a le temps de la voir."),
        ("narrateur", "Le bateau rentre, une feuille collée au flanc."),
        ("maman", "Le froid a failli tout couper."),
    ),
    (3, 1, 1): L(
        ("narrateur", "Au matin, un cube rouge reste près de l'oreiller."),
        ("narrateur", "La buée du lit est mince, pâle."),
        ("enfant-m", "Elle va partir !"),
        ("narrateur", "Nina veut recoucher le doudou, maintenant."),
        ("narrateur", "Victorino attend qu'elle l'embrasse."),
        ("enfant-m", "S'il te plaît, le cube du bout, vers la vitre ?"),
        ("copine", "Voilà."),
        ("narrateur", "Sur l'oreille du doudou, le fil rouge refait l'ancre."),
        ("narrateur", "Ils la copient sur le verre, tout juste."),
        ("papa", "Le rayon arrive."),
        ("narrateur", "Le bateau s'amarre au cube, contre l'oreiller."),
        ("maman", "Ça a failli rester un jeu de tapis."),
    ),
    (3, 1, 2): L(
        ("narrateur", "Après la sieste, les cubes dorment au pied du lit."),
        ("narrateur", "La vitre du lit est sèche."),
        ("enfant-m", "Plus de quai."),
        ("narrateur", "Nina a les joues tièdes, et veut rejouer à la tour."),
        ("narrateur", "Victorino refuse de reconstruire au hasard."),
        ("enfant-m", "S'il te plaît, on souffle d'abord, comme tout à l'heure ?"),
        ("copine", "D'accord."),
        ("narrateur", "Deux souffles."),
        ("narrateur", "Rien."),
        ("narrateur", "Le troisième ramène l'ancre minuscule, très fine."),
        ("papa", "On y croyait plus."),
        ("narrateur", "Un poil de doudou reste accroché au cube."),
    ),
    (3, 1, 3): L(
        ("narrateur", "Au soir, un cube veille près de la veilleuse."),
        ("narrateur", "La buée revient, orange, toute petite."),
        ("enfant-m", "Le quai de la nuit."),
        ("narrateur", "Nina bâille, trop près."),
        ("narrateur", "Son souffle trop large manque d'effacer l'ancre."),
        ("enfant-m", "S'il te plaît, un souffle fin, comme le mien ?"),
        ("copine", "Fin."),
        ("narrateur", "L'ancre minuscule tient dans le rond orange."),
        ("maman", "On s'arrête là."),
        ("papa", "Le bateau peut dormir."),
        ("narrateur", "Le fil rouge prend la couleur de la veilleuse."),
        ("narrateur", "Le cube ne claque plus."),
    ),
    (3, 2, 1): L(
        ("narrateur", "Au matin, le livre est ouvert sur le doudou gris."),
        ("narrateur", "Un rai pâle mange la buée du lit."),
        ("enfant-m", "La page, vite !"),
        ("narrateur", "Nina veut refermer, pour que le doudou dorme."),
        ("narrateur", "Victorino pose le bateau en signet, et attend."),
        ("enfant-m", "S'il te plaît, l'ancre du coin, avant de fermer ?"),
        ("copine", "Je la vois."),
        ("narrateur", "Ils la copient sur le verre restant."),
        ("papa", "Pile."),
        ("narrateur", "Le bateau garde un creux d'oreiller, au ventre."),
        ("maman", "Le doudou a écouté, lui aussi."),
        ("narrateur", "La page ne se ferme pas tout à fait."),
    ),
    (3, 2, 2): L(
        ("narrateur", "Après la sieste, une page a le creux de la sieste."),
        ("narrateur", "La vitre est trop claire, trop honnête."),
        ("enfant-m", "On a trop dormi."),
        ("narrateur", "Nina veut l'histoire du doudou, maintenant."),
        ("narrateur", "Victorino écoute jusqu'au point."),
        ("enfant-m", "S'il te plaît, un souffle pour l'ancre, après ?"),
        ("copine", "Après."),
        ("narrateur", "Ils soufflent."),
        ("narrateur", "L'ancre minuscule revient, comme un secret."),
        ("papa", "Ça a failli rester une histoire, sans vitre."),
        ("narrateur", "Le coin de la page sent l'oreiller."),
        ("maman", "Le bateau s'y est reposé."),
    ),
    (3, 2, 3): L(
        ("narrateur", "Au soir, maman lit tout bas, près de la veilleuse."),
        ("narrateur", "Victorino veut montrer l'ancre pendant le mot."),
        ("narrateur", "Il attend la fin de la ligne."),
        ("enfant-m", "S'il te plaît, l'ancre du livre, sur notre vitre ?"),
        ("maman", "Oui."),
        ("narrateur", "Nina tient le doudou, sans parler."),
        ("narrateur", "Un souffle orange pose l'ancre minuscule."),
        ("papa", "On l'a eue."),
        ("narrateur", "Le bateau dort dans le pli de la page."),
        ("narrateur", "La veilleuse lui fait un port."),
        ("copine", "Chut."),
        ("narrateur", "Le fil rouge ne tic plus."),
    ),
    (3, 3, 1): L(
        ("narrateur", "Au matin, la petite assiette attend sur le tapis."),
        ("narrateur", "La buée du lit fuit vers les coins."),
        ("enfant-m", "Le port, avant le soleil !"),
        ("narrateur", "Nina veut servir le doudou, d'abord."),
        ("narrateur", "Victorino laisse le service aller au bout."),
        ("enfant-m", "S'il te plaît, la tasse, pour le bateau ?"),
        ("copine", "Elle est tiède."),
        ("narrateur", "Le rond de buée sous l'oreiller guide le souffle."),
        ("papa", "L'ancre minuscule s'y pose."),
        ("narrateur", "De justesse."),
        ("narrateur", "Une miette de dînette reste dans l'assiette."),
        ("maman", "Le bateau a son grain, comme un trésor."),
    ),
    (3, 3, 2): L(
        ("narrateur", "Après la sieste, la tasse miniature a glissé sous l'oreiller."),
        ("narrateur", "La vitre n'a plus de secret."),
        ("enfant-m", "On l'a perdue."),
        ("narrateur", "Nina veut chercher en parlant, trop fort."),
        ("narrateur", "Victorino met un doigt sur ses lèvres, puis demande."),
        ("enfant-m", "S'il te plaît, on cherche sans crier ?"),
        ("copine", "D'accord."),
        ("narrateur", "La tasse est là, avec son rond d'ancre."),
        ("narrateur", "Ils soufflent vers le verre."),
        ("papa", "Elle revient, à peine."),
        ("narrateur", "Ça a failli rester sous l'oreiller, pour toujours."),
        ("narrateur", "Le carton a un fil de doudou, accroché."),
    ),
    (3, 3, 3): L(
        ("narrateur", "Au soir, la dînette range, près des chaussons."),
        ("narrateur", "La veilleuse allume la petite tasse."),
        ("enfant-m", "Port de nuit."),
        ("narrateur", "Nina veut tout ranger, trop vite."),
        ("narrateur", "Victorino pose le bateau dans la tasse, et attend."),
        ("enfant-m", "S'il te plaît, on souffle, puis on range ?"),
        ("copine", "Un souffle."),
        ("narrateur", "L'ancre minuscule s'installe, orange."),
        ("maman", "On peut éteindre, après."),
        ("papa", "Le bateau a son quai."),
        ("narrateur", "Un chausson garde le fil rouge, comme une amarre."),
        ("narrateur", "La tasse ne sonne plus."),
    ),
}


def ending(a: int, b: int, c: int) -> list[tuple[str, str]]:
    recap = {
        (1, 1, 1): "J'ai demandé le coin de buée, et le cube rouge a montré l'ancre.",
        (1, 1, 2): "Après la sieste, la casserole nous a prêté un nuage.",
        (1, 1, 3): "Le soir, on a posé le cube sans le coude de Nina.",
        (1, 2, 1): "J'ai attendu l'oiseau du livre, puis on a copié l'ancre.",
        (1, 2, 2): "Le bol tiède a rendu l'ancre, alors que la vitre était sèche.",
        (1, 2, 3): "J'ai attendu le point de maman, puis la lampe a fait le port.",
        (1, 3, 1): "J'ai demandé une cuillerée, et le lait a dessiné l'ancre.",
        (1, 3, 2): "L'eau chaude a failli ne pas venir. Puis l'ancre est revenue.",
        (1, 3, 3): "Après le sel, on a soufflé. Le grain est devenu un phare.",
        (2, 1, 1): "Au jardin, j'ai demandé un quai long. Une plume est restée.",
        (2, 1, 2): "On a soufflé de dehors, comme l'oiseau. L'ancre était à l'envers.",
        (2, 1, 3): "Nina avait froid. On a pris un cube, puis l'ancre, puis le manteau.",
        (2, 2, 1): "J'ai laissé la fourmi passer. L'ancre était sous l'oiseau.",
        (2, 2, 2): "Nina voulait dormir. On a copié l'ancre, pâle, sous l'arbre.",
        (2, 2, 3): "Le vent a claqué. On a pris une page, puis on est rentrés.",
        (2, 3, 1): "Nina a goûté la rosée. Après, la tasse a été le port.",
        (2, 3, 2): "Une goutte d'arrosoir a suffi. L'ancre est née à l'envers.",
        (2, 3, 3): "Nina claquait des dents. Un souffle, puis le bateau est rentré.",
        (3, 1, 1): "J'ai attendu le bisou au doudou. Le fil a refait l'ancre.",
        (3, 1, 2): "Trois souffles. Le troisième a ramené l'ancre, très fine.",
        (3, 1, 3): "Nina a bâillé trop large. On a soufflé fin, dans l'orange.",
        (3, 2, 1): "Le bateau a fait signet. On a copié l'ancre, avant de fermer.",
        (3, 2, 2): "J'ai écouté l'histoire du doudou. Après, l'ancre est revenue.",
        (3, 2, 3): "J'ai attendu la fin de la ligne. La veilleuse a fait le port.",
        (3, 3, 1): "Le doudou a été servi. La tasse a prêté son rond d'ancre.",
        (3, 3, 2): "On a cherché sans crier. La tasse était sous l'oreiller.",
        (3, 3, 3): "On a soufflé, puis rangé. Un chausson garde le fil.",
    }
    tails = {
        (1, 1, 1): "Le bateau dort sur le quai, une virgule d'eau au flanc.",
        (1, 1, 2): "La vapeur a laissé un anneau pâle autour de l'ancre.",
        (1, 1, 3): "Sous la lampe, le fil rouge brille, un peu humide.",
        (1, 2, 1): "Une miette de pain reste collée à la proue.",
        (1, 2, 2): "Le coin de la page garde une trace de buée, en ancre.",
        (1, 2, 3): "Le bateau veille dans l'ovale de la lampe, face à la page.",
        (1, 3, 1): "Une goutte de lait dessine une ancre, au fond de la tasse.",
        (1, 3, 2): "Le chiffon beige a une virgule mouillée, comme la vitre.",
        (1, 3, 3): "La buée du soir encadre le bateau, sans l'effacer.",
        (2, 1, 1): "Une plume du rebord reste sur le cube, près du fil.",
        (2, 1, 2): "Le carton a une tache d'herbe, au ventre.",
        (2, 1, 3): "Le bateau s'amarre au cube chaud, et le jardin s'éteint.",
        (2, 2, 1): "Un grain de terre de fourmi reste sur le carton bleu.",
        (2, 2, 2): "L'ombre de l'arbre dort sur le bateau, ronde.",
        (2, 2, 3): "Le bateau a un coin de page, un peu froissé.",
        (2, 3, 1): "Une goutte reste dans la tasse, comme un bassin.",
        (2, 3, 2): "Le carton sent l'arrosoir, un peu métal.",
        (2, 3, 3): "Une feuille collée au flanc rentre avec nous.",
        (3, 1, 1): "Le bateau s'amarre au cube, contre l'oreiller tiède.",
        (3, 1, 2): "Un poil de doudou reste accroché au bois.",
        (3, 1, 3): "Le fil rouge prend la couleur de la veilleuse.",
        (3, 2, 1): "Le bateau garde un creux d'oreiller, au ventre.",
        (3, 2, 2): "Le coin de la page sent l'oreiller, un peu tiède.",
        (3, 2, 3): "Le bateau dort dans le pli de la page, sous l'orange.",
        (3, 3, 1): "Une miette de dînette brille dans l'assiette, comme un trésor.",
        (3, 3, 2): "Le carton a un fil de doudou, accroché à l'amarre.",
        (3, 3, 3): "Un chausson garde le fil rouge, comme une amarre.",
    }
    keepsake = {
        1: "Sur le quai des rideaux jaunes, la vitre n'est plus la même.",
        2: "Dehors, le rebord est vide. Ici, le bateau a son ancre.",
        3: "La vitre du lit a gardé un coin, pour le bateau.",
    }[a]
    who = {
        1: ("maman", "Tu veux raconter le moment difficile ?"),
        2: ("papa", "Tu veux raconter le moment difficile ?"),
        3: ("maman", "Tu veux raconter le moment difficile ?"),
    }[c]
    return L(
        ("narrateur", keepsake),
        (who[0], who[1]),
        ("enfant-m", recap[(a, b, c)]),
        ("narrateur", "Voilà une trace, sur le carton."),
        ("narrateur", tails[(a, b, c)]),
    )


def path_ids(a: int, b: int, c: int) -> list[str]:
    t1 = f"CHK_T0001_P000{a}"
    t2 = f"{t1}_T0002_P000{b}"
    t3 = f"{t2}_T0003_P000{c}"
    return [
        "CHK_T0000_P0000",
        "CHK_T0001_P0000",
        t1,
        f"{t1}_Q0001",
        f"{t1}_C0001",
        f"{t1}_T0002_P0000",
        t2,
        f"{t2}_T0003_P0000",
        t3,
        f"{t3}_F0001",
    ]


def build() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "goutte,oiseau", "emphasis": "ancre minuscule"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Le bateau peut chercher l'ancre en trois coins."),
            ("maman", "La cuisine, le jardin, ou la chambre ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "la cuisine",
            "option_2_label": "le jardin",
            "option_3_label": "la chambre",
        }},
    )

    for a, t1 in T1.items():
        base = f"CHK_T0001_P000{a}"
        by[base] = voice(by_old[base], t1["passage"], "action", extra={"sons": t1["sons"], "emphasis": "bateau"})
        qid = f"{base}_Q0001"
        by[qid] = voice(
            by_old[qid],
            L(("narrateur", t1["question"])),
            "clue",
            extra={"sons": "", "emphasis": None, "fields": {
                "expected_answer": t1["expected"],
                "accepted_examples": t1["accepted"],
                "retry_prompt": t1["retry"],
                "engine_ok_text": t1["ok"],
                "engine_near_text": "C'est presque ça. Écoute l'indice.",
            }},
        )
        cid = f"{base}_C0001"
        by[cid] = voice(by_old[cid], t1["confirm"], "confirm", extra={"sons": "", "emphasis": "ancre"})
        tid = f"{base}_T0002_P0000"
        by[tid] = voice(
            by_old[tid], t1["choice"], "choice",
            extra={"sons": "", "fields": {
                "option_1_label": "les cubes",
                "option_2_label": "le livre",
                "option_3_label": "la dînette",
            }},
        )
        for b in (1, 2, 3):
            p2 = f"{base}_T0002_P000{b}"
            by[p2] = voice(
                by_old[p2], T2_FN[b](a), "obstacle",
                extra={"sons": T2_SONS[b], "emphasis": "ancre"},
            )
            t3q = f"{p2}_T0003_P0000"
            by[t3q] = voice(
                by_old[t3q], t3_choice(b), "choice",
                extra={"sons": "", "fields": {
                    "option_1_label": "le matin",
                    "option_2_label": "après la sieste",
                    "option_3_label": "le soir",
                }},
            )
            for c in (1, 2, 3):
                leaf = f"{p2}_T0003_P000{c}"
                by[leaf] = voice(
                    by_old[leaf], T3[(a, b, c)], "resolution",
                    extra={"sons": {1: "oiseau", 2: "tissu", 3: "lampe"}[c], "emphasis": "ancre minuscule"},
                )
                fin = f"{leaf}_F0001"
                by[fin] = voice(
                    by_old[fin], ending(a, b, c), "ending",
                    extra={"sons": {1: "goutte,casserole", 2: "oiseau,porte", 3: "tissu,lampe"}[a], "emphasis": "bateau"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra_ids = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    fins = [by[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(set(fins)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fins))}/27")
    last_nars = []
    for c in src["chunks"]:
        if c["kind"] != "passage_fin":
            continue
        nars = [ln.split("|", 1)[1] for ln in by[c["chunk_id"]]["script"].splitlines() if ln.startswith("narrateur|")]
        last_nars.append(nars[-1])
    if len(set(last_nars)) != 27:
        raise SystemExit(f"dernières images non distinctes: {len(set(last_nars))}/27")

    out = dict(src)
    out["fil_rouge"] = (
        "Victorino veut faire glisser son bateau de carton jusqu'à l'ancre "
        "minuscule dessinée dans la buée, avant que le soleil la mange. Nina "
        "veut essuyer la vitre pour voir l'oiseau : deux envies, le même instant. "
        "Il crie trop tôt, le chiffon efface l'ancre, le bateau bascule. Cuisine, "
        "jardin ou chambre changent l'obstacle. Cubes, livre ou dînette changent "
        "la ruse. Matin, sieste ou soir changent la buée. Chaque fin paie l'ancre "
        "et laisse une trace sur le bateau."
    )
    out["title"] = "La vitre embuée de Victorino"
    out["characters"] = "Victorino, Nina, papa, maman"
    out["setting"] = "près de la fenêtre, puis la maison"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    low = "\n".join(c["script"] for c in out["chunks"]).lower()
    for tic in TICS:
        if tic in low:
            raise SystemExit(f"tic global: {tic}")
    n_enc = len(re.findall(r"\bencore\b", low))
    n_dej = len(re.findall(r"\bdéjà\b|\bdeja\b", low))
    if n_enc > 0 or n_dej > 0:
        raise SystemExit(f"tics encore={n_enc} déjà={n_dej}")

    lengths = []
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                n = sum(words(by[i]["text"]) for i in path_ids(a, b, c))
                lengths.append(n)
    nwords = sum(words(c["text"]) for c in out["chunks"])

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        "# TREE-COL-019 — La vitre embuée de Victorino\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés. Pas d'apply.\n\n"
        "## Vécu\n"
        "Cuisine embuée, rideau jaune aux bateaux, tic du radiateur, pain grillé. "
        "Victorino connaît cette vitre ; un détail paraît nouveau : une ancre "
        "minuscule, claire, dessinée par une goutte. Mission : faire glisser son "
        "bateau de carton bleu (fil de laine rouge) jusqu'à l'ancre, avant que le "
        "soleil mange la buée. Nina, chiffon de lin beige, veut voir l'oiseau "
        "maintenant. Il crie « c'est mon quai » pendant que papa parle : le chiffon "
        "efface l'ancre, le bateau bascule. Sourire parti, poitrine bousculée.\n\n"
        "Cuisine / jardin / chambre changent l'obstacle (souffle trop fort, vitre "
        "sans buée dehors, collision avec le doudou). Cubes / livre / dînette "
        "changent la deuxième ruse (tour qui tombe, pages froissées, tasse de travers). "
        "Matin / sieste / soir changent la buée (soleil qui mange, vitre sèche, "
        "lampe qui rend un port). L'ancre du début est payée à chaque climax. "
        "Nuance : on demande au lieu de prendre ; on coupe si le bateau va couler. "
        "Chaque fin laisse une trace unique sur le carton.\n\n"
        "Leçon COL.POL.001 vécue, non dite : s'il te plaît ouvre le tour ; merci "
        "arrive quand la phrase a eu sa place. Tours de parole : envie de couper, "
        "retenue, écoute réelle, plaisir d'être entendu.\n\n"
        "## Vu et corrigé\n"
        "- Titre noyau conservé. N2 ≤ 15. Troupe D16 : Victorino, Nina, papa, maman.\n"
        "- Labels T1/T2/T3 conservés (cuisine, jardin, chambre / cubes, livre, "
        "dînette / matin, sieste, soir). Contenu refait.\n"
        "- Leçon non récitée. Pas de refrain bonjour / s'il te plaît / merci.\n"
        "- 27 fins textuellement distinctes (dernière image narrator unique).\n"
        f"- Chemins {min(lengths)}–{max(lengths)} mots, moyenne {sum(lengths)//len(lengths)}.\n"
        "- Un merci vécu (T1), pas un refrain Bravo / bon travail.\n"
        "- TTS par chunk (profils opening/choice/clue/confirm/action/obstacle/resolution/ending).\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés. Pas apply.\n"
        "- Tics « encore / déjà / tout doux / tout calme » retirés.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    print(f"OK {SID} {nwords} mots  fins={len(set(fins))}  chemins {min(lengths)}-{max(lengths)}")


if __name__ == "__main__":
    build()
