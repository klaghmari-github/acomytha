#!/usr/bin/env python3
"""TREE-COL-016 — La craie et l'oiseau de Victorina (F-NAR-019)."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import ROOT, check, from_script, words  # noqa: E402

SID = "TREE-COL-016"
LIM = 16
TICS = ("tout doux", "tout calme", "on lève la main", "puis on parle", "c'est du bon travail")


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
        note="arc=installation; intention=émerveiller; emotion=curiosité_impatiente; intensite=1; destinataire=enfant; sous_texte=l_oiseau_tape_et_personne_n_entend; tempo=naturel; sourire=léger; respiration=ample",
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
        note="arc=confirmation; intention=relancer; emotion=joie_discrete; intensite=1; destinataire=enfant; sous_texte=la_classe_peut_continuer; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=420,
        sentence=250, energy="lively", contour="dynamic", noise=0.37,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il_faut_faire_attention_a_l_oiseau; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0, pause=520,
        sentence=300, energy="tense", contour="dynamic", noise=0.34,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=inquietude_legere; intensite=2; destinataire=enfant; sous_texte=les_voix_se_marchent_dessus; tempo=resserre; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0, pause=560,
        sentence=270, energy="bright", contour="falling", noise=0.35,
        note="arc=resolution; intention=faire_vivre_la_reussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=le_silence_a_aide_l_oiseau; tempo=naturel; sourire=franc; respiration=relachee",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3, pause=900,
        sentence=340, energy="calm", contour="falling", noise=0.31,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierte_calme; intensite=1; destinataire=enfant; sous_texte=la_craie_et_l_oiseau_se_rejoignent; tempo=pose; sourire=léger; respiration=ample",
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


# --- récit ---
OPENING = L(
    ("narrateur", "La pluie tambourine le toit de zinc du village."),
    ("narrateur", "Dans la maison, la soupe à la courge sent le sucré."),
    ("narrateur", "Papa a collé un grand carton contre le buffet."),
    ("narrateur", "Une craie jaune repose dans une coupelle ébréchée."),
    ("narrateur", "Maman a glissé trois coussins près du tapis rêche."),
    ("papa", "La petite classe peut commencer, Victorina."),
    ("narrateur", "En ce moment, un oiseau jaune s'accroche au rebord mouillé."),
    ("narrateur", "Son bec tape la vitre, une fois, puis deux."),
    ("enfant-f", "Il veut entrer, venez vite voir !"),
    ("narrateur", "Maman parle de la soupe à papa."),
    ("narrateur", "Papa lui répond près de la casserole."),
    ("narrateur", "Les mots de Victorina se cognent aux leurs."),
    ("narrateur", "Personne n'a entendu le tap-tap de l'oiseau."),
    ("narrateur", "L'oiseau recule vers la gouttière qui déborde."),
    ("enfant-f", "Non, reste !"),
    ("narrateur", "Sa voix trop forte fait rentrer la tête jaune."),
    ("maman", "Tu disais quelque chose, ma puce ?"),
    ("narrateur", "Victorina ouvre la bouche, puis la referme."),
    ("narrateur", "Elle pose la craie jaune sur le carton."),
    ("narrateur", "Elle attend que maman finisse sa phrase."),
    ("papa", "La soupe peut patienter, nous t'écoutons."),
    ("enfant-f", "L'oiseau tape, et il va partir sous la pluie."),
    ("maman", "Alors on le regarde, sans le brusquer."),
    ("narrateur", "Sur le carton, un seul trait jaune tremble."),
)

T1 = {
    1: dict(
        name="le tapis",
        passage=L(
            ("narrateur", "Victorina s'assoit sur le tapis épais."),
            ("narrateur", "Un fil rouge dépasse et chatouille son poignet."),
            ("narrateur", "De là, elle voit les pattes de l'oiseau."),
            ("narrateur", "La craie jaune roule vers le coussin."),
            ("enfant-f", "Regardez la petite plume !"),
            ("narrateur", "Maman décrit les coussins à papa."),
            ("narrateur", "Leurs voix couvrent le mot plume."),
            ("narrateur", "Victorina serre la craie, impatiente."),
            ("narrateur", "Elle pose le bâton jaune, et elle attend."),
            ("maman", "J'ai fini, je t'écoute."),
            ("enfant-f", "Une plume jaune est tombée près du tapis."),
            ("papa", "Je la vois, collée au bord de la vitre."),
            ("narrateur", "L'oiseau penche la tête vers la plume."),
        ),
        question="Quelle couleur a la petite plume près du tapis ?",
        expected="jaune",
        accepted="jaune | plume jaune | une plume jaune | jaune comme la craie",
        retry="Regarde la plume collée près du tapis.",
        ok="Oui, elle est jaune.",
        confirm=L(
            ("enfant-f", "Jaune, comme la craie !"),
            ("narrateur", "Oui, une plume jaune."),
            ("narrateur", "Victorina l'a dit quand les oreilles étaient prêtes."),
            ("maman", "Merci, j'ai entendu toute ta phrase."),
            ("narrateur", "L'oiseau reste sur le rebord, près du tapis."),
        ),
        sons="tapis,pluie",
        choice=L(
            ("narrateur", "Sur le tapis, la petite classe peut continuer de trois façons."),
            ("maman", "Une histoire, une chanson, ou un dessin ?"),
        ),
    ),
    2: dict(
        name="la table",
        passage=L(
            ("narrateur", "Victorina grimpe sur la chaise près du carton."),
            ("narrateur", "Le bois de la table est lisse et un peu froid."),
            ("narrateur", "Le trait de craie jaune tremble sous la lampe."),
            ("enfant-f", "Je dessine l'oiseau, et il tape !"),
            ("narrateur", "Papa parle du carton à maman."),
            ("narrateur", "Les deux phrases s'embrouillent."),
            ("narrateur", "Victorina s'arrête, la craie reste en l'air."),
            ("narrateur", "Elle repose le bâton jaune, puis elle attend."),
            ("papa", "Voilà, c'est à toi."),
            ("enfant-f", "Le trait, c'est son aile mouillée."),
            ("maman", "Je vois l'aile, et je vois l'oiseau vrai."),
            ("narrateur", "Une goutte de gouttière frappe près du bec."),
        ),
        question="Quel objet a tracé le trait sur le carton ?",
        expected="craie",
        accepted="craie | la craie | craie jaune | le bâton jaune",
        retry="Regarde ce qui a marqué le carton.",
        ok="Oui, c'est la craie.",
        confirm=L(
            ("enfant-f", "La craie jaune !"),
            ("narrateur", "Oui, la craie a laissé ce trait."),
            ("papa", "Merci d'avoir posé le bâton, on t'entendait."),
            ("narrateur", "Sur la table, un peu de poussière jaune brille."),
        ),
        sons="craie,table",
        choice=L(
            ("narrateur", "À la table, trois jeux peuvent aider l'oiseau."),
            ("papa", "L'histoire, la chanson, ou le dessin ?"),
        ),
    ),
    3: dict(
        name="la fenêtre",
        passage=L(
            ("narrateur", "Victorina court jusqu'à la vitre embuée."),
            ("narrateur", "Elle tape le verre pour montrer l'oiseau."),
            ("narrateur", "L'oiseau saute vers la gouttière, tout au bout."),
            ("enfant-f", "Reviens !"),
            ("narrateur", "Ses doigts restent collés au froid."),
            ("narrateur", "Elle baisse les mains, et elle attend."),
            ("maman", "On ne tape plus, on regarde."),
            ("narrateur", "L'oiseau revient, pas à pas, sur le rebord."),
            ("enfant-f", "Son bec a fait le bruit."),
            ("papa", "Je l'ai entendu, cette fois."),
            ("narrateur", "Une goutte glisse le long du verre."),
        ),
        question="Avec quoi l'oiseau a-t-il tapé la vitre ?",
        expected="bec",
        accepted="bec | son bec | le bec | avec son bec",
        retry="Écoute le petit coup sur le verre.",
        ok="Oui, c'est son bec.",
        confirm=L(
            ("enfant-f", "Avec son bec !"),
            ("narrateur", "Oui, le bec a frappé le verre."),
            ("maman", "Merci, tes mains immobiles l'ont rassuré."),
            ("narrateur", "L'oiseau reste, tout contre la fenêtre."),
        ),
        sons="pluie,oiseau",
        choice=L(
            ("narrateur", "Près de la vitre, l'oiseau attend un signe."),
            ("maman", "On lui raconte, on chante, ou on dessine ?"),
        ),
    ),
}


def t2_histoire(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Maman ouvre un livre d'images sur le tapis."),
            ("narrateur", "Une page sent le papier, un peu sec."),
            ("narrateur", "Un oiseau jaune y tremble sous un nuage."),
            ("enfant-f", "C'est le mien !"),
            ("narrateur", "Le mot sort trop vite, et maman perd sa phrase."),
            ("narrateur", "Victorina se tait, les joues chaudes."),
            ("narrateur", "Maman reprend la page jusqu'au dernier mot."),
            ("maman", "Sous le toit, l'oiseau se secoue tout seul."),
            ("narrateur", "Papa commence une explication en même temps."),
            ("enfant-f", "Un à la fois, sinon je mélange."),
            ("papa", "D'accord, maman d'abord."),
            ("narrateur", "À la dernière image, un rebord ressemble au leur."),
            ("enfant-f", "Il ne veut pas entrer, il veut un coin sec."),
        )
    if a == 2:
        return L(
            ("narrateur", "Maman pose le livre contre le carton, à la table."),
            ("narrateur", "Le trait jaune du tableau frôle l'oiseau dessiné."),
            ("narrateur", "Victorina veut crier que c'est le même."),
            ("narrateur", "Elle mord sa lèvre, et la page tourne."),
            ("maman", "Écoute la fin, le secret est là."),
            ("narrateur", "Le livre montre un oiseau sous une gouttière."),
            ("papa", "Chez nous aussi, la gouttière déborde."),
            ("narrateur", "Les deux adultes parlent ensemble, trop vite."),
            ("enfant-f", "Papa, attends que maman finisse."),
            ("papa", "Tu as raison, j'écoute la page."),
            ("narrateur", "Quand le silence revient, l'oiseau vrai penche la tête."),
            ("enfant-f", "Il cherche l'endroit où l'eau ne tombe pas."),
        )
    return L(
        ("narrateur", "Près de la vitre, maman tient le livre ouvert."),
        ("narrateur", "L'oiseau vrai regarde l'oiseau de papier."),
        ("enfant-f", "Ils se parlent !"),
        ("narrateur", "Sa phrase coupe le mot de maman."),
        ("narrateur", "Le livre se ferme un peu trop vite."),
        ("enfant-f", "Pardon, je reprends après."),
        ("maman", "Je recommence la dernière phrase."),
        ("narrateur", "Cette fois, Victorina laisse la voix aller jusqu'au point."),
        ("papa", "L'image montre un coin sec sous le toit."),
        ("narrateur", "Dehors, l'oiseau se pousse hors du filet d'eau."),
        ("enfant-f", "Il a compris le livre, lui aussi."),
    )


def t2_chanson(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Papa tapote le tapis, comme la pluie."),
            ("narrateur", "Une chanson de gouttes commence, toute simple."),
            ("enfant-f", "Moi aussi, je chante l'oiseau !"),
            ("narrateur", "Trois voix partent en même temps."),
            ("narrateur", "L'oiseau se tait, et rentre le bec."),
            ("enfant-f", "Il n'aime pas quand ça se mélange."),
            ("maman", "Et s'il répondait dans les trous ?"),
            ("narrateur", "Papa chante une ligne, puis s'arrête."),
            ("narrateur", "Un petit cri jaune arrive dans le silence."),
            ("enfant-f", "C'est son tour !"),
            ("papa", "On lui laisse la place, comme à toi."),
            ("narrateur", "Sur le tapis, le fil rouge semble suivre le rythme."),
        )
    if a == 2:
        return L(
            ("narrateur", "Papa tapote le bois de la table."),
            ("narrateur", "La craie roule et fait un petit clic."),
            ("narrateur", "La chanson de pluie part trop fort, trop serrée."),
            ("narrateur", "L'oiseau disparaît derrière la gouttière."),
            ("enfant-f", "On a chanté sur lui."),
            ("maman", "On recommence, une voix après l'autre."),
            ("narrateur", "Papa pose les mains à plat."),
            ("narrateur", "Victorina attend la fin de sa ligne."),
            ("enfant-f", "Coucou, oiseau."),
            ("narrateur", "Dans le trou, un cri répond, tout mince."),
            ("papa", "Il parlait, on ne l'entendait pas."),
            ("narrateur", "Le trait jaune du carton tremble sous la lampe."),
        )
    return L(
        ("narrateur", "Face à la vitre, papa chante tout bas."),
        ("narrateur", "Les gouttes suivent, puis se taisent."),
        ("enfant-f", "Je veux le refrain maintenant !"),
        ("narrateur", "Sa voix recouvre le dernier mot de papa."),
        ("narrateur", "L'oiseau recule d'un pas, méfiant."),
        ("papa", "Laisse-moi finir, ensuite c'est toi."),
        ("narrateur", "Victorina serre ses poings, puis les ouvre."),
        ("narrateur", "Elle attend le point, et elle pose sa note."),
        ("narrateur", "L'oiseau avance, et glisse un cri dans le trou."),
        ("maman", "Il chante avec vous, chacun son trou."),
        ("enfant-f", "On ne lui marche plus sur le bec."),
    )


def t2_dessin(a: int) -> list[tuple[str, str]]:
    if a == 1:
        return L(
            ("narrateur", "Le carton glisse du buffet jusqu'au tapis."),
            ("narrateur", "Victorina attrape la craie pendant que papa trace un nuage."),
            ("narrateur", "Le trait casse, et le nuage devient un griffonnage."),
            ("enfant-f", "L'aile, c'est moi !"),
            ("papa", "J'avais pas fini le nuage."),
            ("narrateur", "Elle rend la craie, les épaules basses."),
            ("narrateur", "Papa termine sa courbe, sans se dépêcher."),
            ("maman", "À toi, pour le bec."),
            ("narrateur", "Un bec pointu apparaît, puis deux pattes."),
            ("narrateur", "Dehors, l'oiseau picore le verre, du côté de l'aile."),
            ("enfant-f", "Son aile à lui est trop mouillée pour voler."),
        )
    if a == 2:
        return L(
            ("narrateur", "À la table, le carton est un vrai tableau."),
            ("narrateur", "Maman dessine une goutte, très lente."),
            ("enfant-f", "Je fais l'oiseau, vite !"),
            ("narrateur", "Sa main croise celle de maman."),
            ("narrateur", "La goutte et l'aile se mélangent en nuage jaune."),
            ("maman", "On dessine l'une après l'autre, sinon il n'est plus lui."),
            ("narrateur", "Victorina pose la craie, et compte jusqu'à trois."),
            ("narrateur", "Maman finit la goutte."),
            ("enfant-f", "Maintenant, son aile."),
            ("papa", "Regarde, il picore juste là, sur l'aile mouillée."),
            ("narrateur", "La poussière jaune tombe sur le bois, comme une pluie."),
        )
    return L(
        ("narrateur", "Près de la fenêtre, Victorina copie l'oiseau vrai."),
        ("narrateur", "Papa veut ajouter un nuage au même instant."),
        ("narrateur", "Deux craies grincent, et l'oiseau vrai s'effarouche."),
        ("enfant-f", "On fait trop de bruit."),
        ("papa", "Une craie à la fois, je te la passe."),
        ("narrateur", "Il attend qu'elle pose le bec."),
        ("narrateur", "Ensuite seulement, il glisse un petit nuage."),
        ("maman", "L'oiseau vrai picore l'aile de craie, derrière le verre."),
        ("enfant-f", "Cette aile-là ne peut pas s'ouvrir."),
        ("narrateur", "Le portrait et l'oiseau se regardent, enfin séparés."),
    )


T2_FN = {1: t2_histoire, 2: t2_chanson, 3: t2_dessin}
T2_SONS = {1: "page", 2: "pluie", 3: "craie"}
T2_NAME = {1: "l'histoire", 2: "la chanson", 3: "le dessin"}
T3_NAME = {1: "la poupée", 2: "l'ours", 3: "le lion"}


def t3_choice(b: int) -> list[tuple[str, str]]:
    if b == 1:
        return L(
            ("narrateur", "Le livre a montré un coin sec, sans forcer l'oiseau."),
            ("papa", "Qui peut l'aider : la poupée, l'ours, ou le lion ?"),
        )
    if b == 2:
        return L(
            ("narrateur", "L'oiseau a parlé dans un trou de la chanson."),
            ("maman", "Qui l'aide maintenant : la poupée, l'ours, ou le lion ?"),
        )
    return L(
        ("narrateur", "Le portrait montre une aile trop mouillée."),
        ("papa", "Qui l'aide sans le toucher : la poupée, l'ours, ou le lion ?"),
    )


# 27 scènes T3 : autre climax, autre geste.
T3 = {
    (1, 1, 1): L(
        ("narrateur", "Victorina prend la poupée au foulard rayé."),
        ("narrateur", "Le foulard sent le bois du tiroir."),
        ("enfant-f", "On lui fait un toit, comme dans le livre."),
        ("narrateur", "Papa ouvre un filet d'air, tout étroit."),
        ("narrateur", "Le tissu glisse sur le rebord, du côté du tapis."),
        ("narrateur", "L'oiseau hésite, puis se pousse sous le petit toit."),
        ("maman", "Il a copié la page, tout seul."),
        ("papa", "Merci d'avoir attendu le filet d'air."),
        ("narrateur", "Une goutte tombe sur le foulard, plus sur les plumes."),
    ),
    (1, 1, 2): L(
        ("narrateur", "Victorina installe l'ours brun sur ses genoux."),
        ("narrateur", "L'ours est lourd, et sent le placard."),
        ("enfant-f", "On fait comme la dernière page, on ne bouge pas."),
        ("narrateur", "Maman ferme le livre, sans le claquer."),
        ("narrateur", "Le temps passe, un peu trop long pour les pieds."),
        ("narrateur", "Victorina ouvre la bouche, puis la referme."),
        ("papa", "Regarde, il a trouvé l'angle sec tout seul."),
        ("narrateur", "L'oiseau se secoue au-dessus du tapis, derrière le verre."),
        ("maman", "Votre silence lui a laissé de la place."),
    ),
    (1, 1, 3): L(
        ("narrateur", "Papa part vers la cuisine, le livre resté ouvert."),
        ("narrateur", "La porte va claquer sur le silence du tapis."),
        ("enfant-f", "Papa, la porte !"),
        ("narrateur", "Cette fois, elle n'attend pas : le bruit ferait fuir."),
        ("narrateur", "Papa rattrape le bois, tout près du cadre."),
        ("narrateur", "Victorina glisse le lion en laine contre le bas."),
        ("papa", "Il garde la porte, moi je pose le couvercle."),
        ("narrateur", "L'oiseau se secoue, loin de la gouttière."),
        ("maman", "Tu as parlé pile au bon moment."),
    ),
    (1, 2, 1): L(
        ("narrateur", "La chanson s'arrête sur un trou, exprès."),
        ("narrateur", "Victorina tend le foulard de la poupée."),
        ("enfant-f", "Toit, pendant qu'il écoute."),
        ("narrateur", "Papa ouvre un filet d'air, sans grincer."),
        ("narrateur", "Le tissu rayé s'étend du côté du tapis."),
        ("narrateur", "Un cri jaune répond, puis l'oiseau glisse dessous."),
        ("maman", "Il a pris sa mesure, comme dans la chanson."),
        ("narrateur", "Le fil rouge du tapis aboutit au petit toit."),
    ),
    (1, 2, 2): L(
        ("narrateur", "Victorina pose l'ours contre son ventre."),
        ("narrateur", "Ils restent là, comme un silence de refrain."),
        ("enfant-f", "Chut, c'est son couplet."),
        ("narrateur", "Un cri arrive, puis un pas vers l'angle sec."),
        ("narrateur", "Elle veut crier bravo, et elle avale le mot."),
        ("papa", "Tu lui as laissé toute la chanson."),
        ("narrateur", "L'ours penche l'oreille, lourd et sage."),
        ("narrateur", "L'oiseau se secoue au-dessus du tapis rêche."),
    ),
    (1, 2, 3): L(
        ("narrateur", "Le dernier trou de la chanson reste ouvert."),
        ("narrateur", "Dans la cuisine, la porte se balance."),
        ("enfant-f", "Le lion, vite, avant le clac !"),
        ("narrateur", "Papa bloque le bois, et le lion s'y cale."),
        ("narrateur", "La note de pluie peut finir, toute seule."),
        ("maman", "Il s'est secoué sur le dernier soupir."),
        ("narrateur", "Sur le tapis, personne ne reprend trop tôt."),
        ("papa", "On a chanté avec la maison, pas contre l'oiseau."),
    ),
    (1, 3, 1): L(
        ("narrateur", "Un peu de craie jaune poudre le foulard de la poupée."),
        ("enfant-f", "C'est une aile de plus, pour le vrai."),
        ("narrateur", "Papa glisse le tissu sur le rebord, du côté du tapis."),
        ("narrateur", "L'oiseau picore d'abord le jaune, puis se pousse dessous."),
        ("maman", "Il a reconnu la couleur du carton."),
        ("narrateur", "Le portrait sur le tapis et le toit se répondent."),
        ("papa", "Ton trait a servi de pont."),
    ),
    (1, 3, 2): L(
        ("narrateur", "Victorina gèle, la craie en l'air, l'ours sur les genoux."),
        ("enfant-f", "On attend que l'aile sèche un peu."),
        ("narrateur", "Le nuage de craie reste inachevé, exprès."),
        ("narrateur", "L'oiseau se pousse vers l'angle, loin de la goutte."),
        ("narrateur", "Alors seulement, elle pose le dernier trait."),
        ("maman", "Tu as fini le dessin après lui."),
        ("narrateur", "Une poussière jaune tombe sur le poil de l'ours."),
    ),
    (1, 3, 3): L(
        ("narrateur", "Le portrait repose sur le tapis, l'aile trop lourde."),
        ("narrateur", "Papa ouvre la cuisine, et le courant d'air soulève la craie."),
        ("enfant-f", "Lion à la porte, le dessin va s'envoler !"),
        ("narrateur", "Le lion en laine cale le bois."),
        ("narrateur", "L'oiseau, rassuré, ouvre un peu l'aile mouillée."),
        ("papa", "Il s'est secoué, et ton nuage est resté."),
        ("narrateur", "La poussière jaune retombe, comme une pluie fine."),
    ),
    (2, 1, 1): L(
        ("narrateur", "À la table, la poupée a le livre contre les genoux."),
        ("enfant-f", "Son foulard va copier le toit de la page."),
        ("narrateur", "Papa ouvre un filet d'air, depuis la chaise."),
        ("narrateur", "Le tissu rayé rejoint le rebord, au niveau du carton."),
        ("narrateur", "L'oiseau glisse sous le toit, et le trait jaune le salue."),
        ("maman", "La page, le carton et l'oiseau disent la même chose."),
        ("papa", "Merci d'avoir laissé le livre aller au bout."),
    ),
    (2, 1, 2): L(
        ("narrateur", "L'ours s'assoit sur la chaise à côté du carton."),
        ("narrateur", "Victorina pose les mains à plat sur le bois."),
        ("enfant-f", "On ne tourne plus la page, on attend."),
        ("narrateur", "L'oiseau quitte la gouttière, vers l'angle sec."),
        ("narrateur", "Une miette de courge reste collée près du livre."),
        ("maman", "Il a choisi, comme à la dernière image."),
        ("narrateur", "L'ours ne bouge pas, même quand la chaise grince."),
    ),
    (2, 1, 3): L(
        ("narrateur", "Depuis la table, on voit papa pousser la porte."),
        ("enfant-f", "Le lion, sinon le livre et l'oiseau sautent !"),
        ("narrateur", "Victorina court, pose le lion contre le bois."),
        ("narrateur", "Le clac n'arrive pas."),
        ("narrateur", "L'oiseau se secoue, et le carton reste droit."),
        ("papa", "Tu as parlé assez fort, et assez juste."),
        ("maman", "La petite classe a gardé son silence."),
    ),
    (2, 2, 1): L(
        ("narrateur", "À la table, papa laisse un trou dans la chanson."),
        ("narrateur", "Victorina glisse le foulard pendant ce silence."),
        ("enfant-f", "Toit, à son tour."),
        ("narrateur", "Le tissu passe au rebord, sans frotter le carton."),
        ("narrateur", "L'oiseau répond, puis se pousse dessous."),
        ("maman", "Il a pris le trou, et le toit."),
        ("narrateur", "La craie, dans la coupelle, ne roule plus."),
    ),
    (2, 2, 2): L(
        ("narrateur", "L'ours est assis à table, comme un élève sage."),
        ("narrateur", "La chanson s'arrête, et personne ne reprend."),
        ("enfant-f", "C'est lui, maintenant."),
        ("narrateur", "Un cri, un pas, l'angle sec."),
        ("papa", "On n'a pas chanté par-dessus."),
        ("narrateur", "Victorina appuie sa joue sur le bois lisse."),
        ("narrateur", "L'ours garde le silence jusqu'au bout des plumes."),
    ),
    (2, 2, 3): L(
        ("narrateur", "Le refrain va finir, et la porte de cuisine s'ouvre."),
        ("enfant-f", "Lion, la note va se casser !"),
        ("narrateur", "Le lion cale le bois, la chanson peut mourir seule."),
        ("narrateur", "L'oiseau se secoue sur le dernier soupir."),
        ("maman", "Il a dansé sans le clac."),
        ("narrateur", "À la table, la coupelle de craie ne tinte plus."),
        ("papa", "On a laissé la maison écouter avec nous."),
    ),
    (2, 3, 1): L(
        ("narrateur", "Le portrait sur le carton a l'aile trop lourde."),
        ("narrateur", "Victorina poudre le foulard d'un peu de jaune."),
        ("enfant-f", "Aile de tissu, pour la vraie."),
        ("narrateur", "Papa pose le toit au rebord, vis-à-vis du tableau."),
        ("narrateur", "L'oiseau picore le jaune, puis s'abrite."),
        ("maman", "Il a lu ton dessin."),
        ("narrateur", "La poussière de craie reste sur la table, en petit chemin."),
    ),
    (2, 3, 2): L(
        ("narrateur", "À la table, Victorina tient la craie, et l'ours."),
        ("narrateur", "Le dernier trait de l'aile n'est pas posé."),
        ("enfant-f", "D'abord lui, après le dessin."),
        ("narrateur", "L'oiseau gagne l'angle, loin de la goutte."),
        ("narrateur", "Alors elle ferme l'aile de craie, tout léger."),
        ("papa", "Tu as fini quand lui a fini."),
        ("narrateur", "L'ours a un point jaune au museau."),
    ),
    (2, 3, 3): L(
        ("narrateur", "Le carton tremble quand la porte de cuisine s'ouvre."),
        ("enfant-f", "Lion, mon oiseau de craie va tomber !"),
        ("narrateur", "Le lion cale le bois, le tableau se tient."),
        ("narrateur", "Dehors, l'oiseau vrai ouvre un peu l'aile."),
        ("maman", "Les deux oiseaux ont eu leur calme."),
        ("papa", "Tu as gardé la classe, et la porte."),
        ("narrateur", "Un rai de lampe traverse la poussière jaune."),
    ),
    (3, 1, 1): L(
        ("narrateur", "Tout contre la vitre, la poupée voit l'oiseau de près."),
        ("enfant-f", "Son foulard, juste là, comme le toit du livre."),
        ("narrateur", "Papa ouvre un filet d'air, sans bouger trop vite."),
        ("narrateur", "Le tissu glisse à deux doigts du bec."),
        ("narrateur", "L'oiseau se pousse dessous, et la gouttière perd sa cible."),
        ("maman", "La page est devenue vraie, sous nos yeux."),
        ("narrateur", "Une goutte frappe le foulard, et s'arrête là."),
    ),
    (3, 1, 2): L(
        ("narrateur", "L'ours est chaud contre le verre froid."),
        ("narrateur", "Victorina s'accroupit, le livre fermé sur ses genoux."),
        ("enfant-f", "On ne parle plus, on le laisse choisir."),
        ("narrateur", "L'oiseau quitte le filet d'eau, pas à pas."),
        ("narrateur", "Il se secoue si près que la vitre s'embue."),
        ("papa", "On n'a rien forcé, et il a trouvé."),
        ("narrateur", "L'ours garde une petite buée sur le nez."),
    ),
    (3, 1, 3): L(
        ("narrateur", "Près de la fenêtre, on entend le pas de papa vers la soupe."),
        ("enfant-f", "La porte, le lion !"),
        ("narrateur", "Elle crie sans attendre, parce que le clac est trop près."),
        ("narrateur", "Papa rattrape, le lion cale."),
        ("narrateur", "L'oiseau, à deux centimètres, ouvre l'aile et la referme."),
        ("maman", "Tu as parlé pour lui, juste à temps."),
        ("narrateur", "Le livre reste ouvert sur le rebord intérieur."),
    ),
    (3, 2, 1): L(
        ("narrateur", "Face au verre, la chanson laisse un trou large."),
        ("narrateur", "Le foulard de la poupée passe dans ce silence."),
        ("enfant-f", "Toit, pendant son cri."),
        ("narrateur", "L'oiseau répond, puis se glisse sous le tissu."),
        ("maman", "Il a chanté, et il s'est abrité."),
        ("papa", "On n'a pas recouvert sa voix."),
        ("narrateur", "Les gouttes tapent le foulard, plus la tête jaune."),
    ),
    (3, 2, 2): L(
        ("narrateur", "L'ours et Victorina collent leur silence à la vitre."),
        ("enfant-f", "Refrain à lui."),
        ("narrateur", "Un cri tout près, un pas, l'angle sec."),
        ("narrateur", "Elle n'ajoute aucune note."),
        ("papa", "Tu as tenu ta chanson jusqu'au bout du trou."),
        ("narrateur", "L'oiseau se secoue, et des perles roulent sur le verre."),
        ("maman", "L'ours a écouté aussi fort que nous."),
    ),
    (3, 2, 3): L(
        ("narrateur", "Le dernier trou de la chanson tremble contre la vitre."),
        ("narrateur", "La porte de cuisine s'ouvre dans le dos."),
        ("enfant-f", "Lion, il va rentrer le cri !"),
        ("narrateur", "Le lion cale, le cri peut finir."),
        ("narrateur", "L'oiseau se secoue sur cette dernière note."),
        ("papa", "On a fermé le bruit, pas sa chanson."),
        ("narrateur", "Une goutte dessine une portée sur le verre."),
    ),
    (3, 3, 1): L(
        ("narrateur", "Le portrait et l'oiseau vrai se font face, de part et d'autre."),
        ("narrateur", "Victorina poudre le foulard, une aile de craie."),
        ("enfant-f", "Pour la vraie aile."),
        ("narrateur", "Papa pose le toit, tout contre le bec."),
        ("narrateur", "L'oiseau picore le jaune, puis s'abrite."),
        ("maman", "Il a choisi ton dessin comme abri."),
        ("narrateur", "Derrière le verre, l'aile de craie et l'aile vraie se calment."),
    ),
    (3, 3, 2): L(
        ("narrateur", "Près de la fenêtre, la craie s'arrête au milieu de l'aile."),
        ("narrateur", "L'ours appuie son front au verre."),
        ("enfant-f", "On attend qu'il ouvre la sienne."),
        ("narrateur", "L'oiseau gagne l'angle, et déplie un peu de plume."),
        ("narrateur", "Alors Victorina ferme le trait, sans grincer."),
        ("papa", "Deux ailes, chacune à son heure."),
        ("narrateur", "Un point de buée cache un instant le bec."),
    ),
    (3, 3, 3): L(
        ("narrateur", "Le carton est tout près de la vitre, l'aile trop lourde."),
        ("narrateur", "Un courant d'air vient de la cuisine."),
        ("enfant-f", "Lion à la porte, les deux oiseaux ont peur !"),
        ("narrateur", "Le lion cale le bois, le carton ne bascule pas."),
        ("narrateur", "L'oiseau vrai ouvre l'aile, enfin, hors de la goutte."),
        ("maman", "Tu as gardé le calme des deux côtés."),
        ("papa", "La petite classe n'a pas bougé."),
        ("narrateur", "La craie repose, et le rebord s'est tu."),
    ),
}


def ending(a: int, b: int, c: int) -> list[tuple[str, str]]:
    recap = {
        (1, 1, 1): "On a lu, et le foulard a fait un toit.",
        (1, 1, 2): "On a lu, et l'ours a attendu avec nous.",
        (1, 1, 3): "On a lu, et le lion a tenu la porte.",
        (1, 2, 1): "On a chanté, et le foulard a pris la pluie.",
        (1, 2, 2): "On a chanté, et l'ours a gardé le trou.",
        (1, 2, 3): "On a chanté, et le lion a arrêté le clac.",
        (1, 3, 1): "On a dessiné, et le foulard est devenu une aile.",
        (1, 3, 2): "On a dessiné, et l'ours a attendu la vraie aile.",
        (1, 3, 3): "On a dessiné, et le lion a sauvé le carton.",
        (2, 1, 1): "À la table, le livre et le foulard ont dit le toit.",
        (2, 1, 2): "À la table, l'ours n'a pas tourné la page trop tôt.",
        (2, 1, 3): "À la table, le lion a empêché le saut du carton.",
        (2, 2, 1): "À la table, le trou de la chanson a porté le toit.",
        (2, 2, 2): "À la table, l'ours a tenu le silence du refrain.",
        (2, 2, 3): "À la table, le lion a laissé la note mourir seule.",
        (2, 3, 1): "À la table, le jaune du foulard a guidé l'oiseau.",
        (2, 3, 2): "À la table, l'ours a laissé le dernier trait pour plus tard.",
        (2, 3, 3): "À la table, le lion a tenu le tableau droit.",
        (3, 1, 1): "Contre la vitre, le foulard a copié la page.",
        (3, 1, 2): "Contre la vitre, l'ours a réchauffé le verre.",
        (3, 1, 3): "Contre la vitre, le lion a coupé le clac.",
        (3, 2, 1): "Contre la vitre, le foulard a pris son cri.",
        (3, 2, 2): "Contre la vitre, l'ours a collé son silence.",
        (3, 2, 3): "Contre la vitre, le lion a sauvé la dernière note.",
        (3, 3, 1): "Contre la vitre, le foulard a abrité l'aile vraie.",
        (3, 3, 2): "Contre la vitre, l'ours a attendu l'aile ouverte.",
        (3, 3, 3): "Contre la vitre, le lion a gardé les deux oiseaux.",
    }
    tails = {
        (1, 1, 1): "Sous le foulard, une plume sèche au-dessus du tapis.",
        (1, 1, 2): "L'ours lourd garde le creux des genoux.",
        (1, 1, 3): "Le lion en laine reste calé, et la soupe ne claque plus.",
        (1, 2, 1): "Le fil rouge du tapis aboutit au petit toit mouillé.",
        (1, 2, 2): "Un cri jaune dort dans le poil de l'ours.",
        (1, 2, 3): "La dernière goutte tombe en rythme, sans porte.",
        (1, 3, 1): "Le foulard rayé a un nuage de craie, comme une aile.",
        (1, 3, 2): "Un point jaune brille sur le ventre de l'ours.",
        (1, 3, 3): "La poussière de craie retombe sur le tapis, toute fine.",
        (2, 1, 1): "Le livre, ouvert à table, montre le même toit.",
        (2, 1, 2): "Une miette de courge reste près de la patte de l'ours.",
        (2, 1, 3): "Le carton tient droit, et le lion tient la porte.",
        (2, 2, 1): "La coupelle de craie ne roule plus sur le bois.",
        (2, 2, 2): "L'ours élève a les pattes bien à plat sur la chaise.",
        (2, 2, 3): "La note de pluie s'est éteinte dans la courge tiède.",
        (2, 3, 1): "Un chemin de poussière jaune va de la table au rebord.",
        (2, 3, 2): "Le museau de l'ours a pris le dernier point de craie.",
        (2, 3, 3): "Un rai de lampe traverse la poussière, au-dessus du bois.",
        (3, 1, 1): "Le foulard goutte, et le bec ne tape plus le verre.",
        (3, 1, 2): "Une petite buée reste sur le nez de l'ours.",
        (3, 1, 3): "Le livre sur le rebord intérieur ne tremble plus.",
        (3, 2, 1): "Les gouttes tapent le tissu, plus la tête jaune.",
        (3, 2, 2): "Des perles d'eau descendent le verre, sans bruit de voix.",
        (3, 2, 3): "Une portée de gouttes s'efface lentement sur la vitre.",
        (3, 3, 1): "L'aile de craie et l'aile vraie se sont arrêtées ensemble.",
        (3, 3, 2): "Un point de buée cache le bec, puis le rend.",
        (3, 3, 3): "La craie repose, et le rebord ne dit plus tap-tap.",
    }
    keepsake = {
        1: "Près des coussins, la craie jaune a un peu de poussière au bout.",
        2: "Sur le carton, le premier trait est devenu une aile.",
        3: "Derrière la vitre, le rebord a cessé de sonner.",
    }
    invite = {
        1: "À toi, Victorina, on t'écoute jusqu'au bout.",
        2: "Raconte-nous, on a fini nos phrases.",
        3: "Dis-nous ce que l'oiseau a choisi.",
    }
    return L(
        ("narrateur", "Plus tard, la soupe fume dans les bols."),
        ("maman", invite[a]),
        ("enfant-f", recap[(a, b, c)]),
        ("narrateur", keepsake[a]),
        ("narrateur", tails[(a, b, c)]),
    )


T3_SONS = {1: "tissu,pluie", 2: "jardin-calme", 3: "porte"}
FIN_SONS = {1: "couverts,pluie", 2: "couverts,craie", 3: "couverts,oiseau"}


def build() -> None:
    folder = ROOT / SID
    src = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    by_old = {c["chunk_id"]: c for c in src["chunks"]}
    by: dict[str, dict] = {}

    by["CHK_T0000_P0000"] = voice(
        by_old["CHK_T0000_P0000"], OPENING, "opening",
        extra={"sons": "pluie,craie", "emphasis": "oiseau jaune"},
    )
    by["CHK_T0001_P0000"] = voice(
        by_old["CHK_T0001_P0000"],
        L(
            ("narrateur", "Pour voir l'oiseau sans le faire fuir, trois places attendent."),
            ("maman", "Le tapis, la table, ou la fenêtre ?"),
        ),
        "choice",
        extra={"sons": "", "fields": {
            "option_1_label": "le tapis",
            "option_2_label": "la table",
            "option_3_label": "la fenêtre",
        }},
    )

    for a, t1 in T1.items():
        base = f"CHK_T0001_P000{a}"
        by[base] = voice(by_old[base], t1["passage"], "action", extra={"sons": t1["sons"], "emphasis": "oiseau"})
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
                "engine_near_text": "Tu es tout près. Reprenons l'indice.",
            }},
        )
        cid = f"{base}_C0001"
        by[cid] = voice(by_old[cid], t1["confirm"], "confirm", extra={"sons": "", "emphasis": "Merci"})
        tid = f"{base}_T0002_P0000"
        by[tid] = voice(
            by_old[tid], t1["choice"], "choice",
            extra={"sons": "", "fields": {
                "option_1_label": "l'histoire",
                "option_2_label": "la chanson",
                "option_3_label": "le dessin",
            }},
        )
        for b in (1, 2, 3):
            p2 = f"{base}_T0002_P000{b}"
            by[p2] = voice(
                by_old[p2], T2_FN[b](a), "obstacle",
                extra={"sons": T2_SONS[b], "emphasis": "oiseau"},
            )
            t3q = f"{p2}_T0003_P0000"
            by[t3q] = voice(
                by_old[t3q], t3_choice(b), "choice",
                extra={"sons": "", "fields": {
                    "option_1_label": "la poupée",
                    "option_2_label": "l'ours",
                    "option_3_label": "le lion",
                }},
            )
            for c in (1, 2, 3):
                leaf = f"{p2}_T0003_P000{c}"
                by[leaf] = voice(
                    by_old[leaf], T3[(a, b, c)], "resolution",
                    extra={"sons": T3_SONS[c], "emphasis": T3_NAME[c].split()[-1]},
                )
                fin = f"{leaf}_F0001"
                by[fin] = voice(
                    by_old[fin], ending(a, b, c), "ending",
                    extra={"sons": FIN_SONS[c], "emphasis": "craie"},
                )

    missing = [c["chunk_id"] for c in src["chunks"] if c["chunk_id"] not in by]
    extra_ids = set(by) - {c["chunk_id"] for c in src["chunks"]}
    if missing or extra_ids:
        raise SystemExit(f"missing={missing[:8]} extra={sorted(extra_ids)[:8]}")

    fins = [by[c["chunk_id"]]["text"] for c in src["chunks"] if c["kind"] == "passage_fin"]
    if len(set(fins)) != 27:
        raise SystemExit(f"fins non distinctes: {len(set(fins))}/27")

    out = dict(src)
    out["fil_rouge"] = (
        "Un jour de pluie, Victorina ouvre la petite classe à la maison : "
        "carton, craie jaune, trois coussins. Un oiseau jaune tape la vitre. "
        "Elle crie trop tôt, personne n'entend, l'oiseau recule. Pour le comprendre "
        "sans le forcer, la famille s'installe sur le tapis, à la table ou près de "
        "la fenêtre ; une histoire, une chanson ou un dessin donne l'indice ; "
        "la poupée, l'ours ou le lion aident sans le toucher. Au bol de soupe, "
        "Victorina raconte, et on l'écoute jusqu'au bout."
    )
    out["title"] = "La craie et l'oiseau de Victorina"
    out["characters"] = "Victorina, papa, maman"
    out["setting"] = "petite classe à la maison, jour de pluie"
    out["chunks"] = [by[c["chunk_id"]] for c in src["chunks"]]
    check(SID, out["age_band"], out["chunks"])

    low = "\n".join(c["script"] for c in out["chunks"]).lower()
    for tic in TICS + ("l'histoire est finie", "on attend. puis", "il faut attendre"):
        if tic in low:
            raise SystemExit(f"tic global: {tic}")
    if "encore" in low or "déjà" in low:
        # un ou deux usages max
        n_enc = len(re.findall(r"\bencore\b", low))
        n_dej = len(re.findall(r"\bdéjà\b", low))
        if n_enc > 2 or n_dej > 2:
            raise SystemExit(f"tics encore={n_enc} déjà={n_dej}")

    (folder / "merged.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (folder / "RELECTURE.md").write_text(
        "# TREE-COL-016 — La craie et l'oiseau de Victorina\n\n"
        "Relu : monde, désir, imprévu, question, résolution, fin heureuse. "
        "`chunk_id` / `kind` inchangés.\n\n"
        "## Vécu\n"
        "Jour de pluie, petite classe à la maison (carton, craie jaune, coussins). "
        "Victorina veut comprendre l'oiseau qui tape la vitre et le dessiner avant "
        "qu'il parte. Elle crie trop tôt : les voix de la soupe couvrent, l'oiseau "
        "recule. Elle pose la craie, attend la fin de la phrase, puis on l'entend. "
        "Tapis / table / fenêtre changent l'angle. Histoire / chanson / dessin "
        "changent l'indice (coin sec, trou de silence, aile mouillée). Poupée / "
        "ours / lion changent l'aide (toit de foulard, attente, porte calée). "
        "Nuance : on attend pour parler, sauf si la porte va claquer. "
        "Autre récit que TREE-COL-015 (pas d'escargot, pas de jardin d'enquête).\n\n"
        "## Vu et corrigé\n"
        "- Titre noyau conservé. N3 ≤ 16. Troupe D16 : Victorina, papa, maman.\n"
        "- T3 Léa/Tom/Sami → poupée / ours / lion.\n"
        "- Leçon COL.ECO.002 vécue, pas récitée. Pas « on lève la main / puis on parle ».\n"
        "- 27 fins textuellement distinctes. Un merci vécu (T1), pas un refrain Bravo.\n"
        "- TTS par chunk (profils opening/choice/clue/confirm/action/obstacle/resolution/ending).\n"
        "- `text` / `script` / `text_ssml` / `text_xai_tags` synchronisés. Pas apply.\n\n"
        "## Non vérifié\n"
        "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur.\n",
        encoding="utf-8",
    )
    nwords = sum(words(c["text"]) for c in out["chunks"])
    print(f"OK {SID} {nwords} mots  fins={len(set(fins))}")


if __name__ == "__main__":
    build()
