#!/usr/bin/env python3
"""TREE-COL-033 — F-NAR-019 : chaîne tiède, galet, 27 fins, TTS. N2."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import LIMITS, ROOT, check, from_script, words  # noqa: E402

SID = "TREE-COL-033"
N2 = LIMITS["N2"]
CHILD = "enfant-m"

PROFILES = {
    "opening": dict(
        rate="medium", wpm=142, speed=0.98, piper=1.12, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=500, sentence=260, energy="warm", contour="storytelling",
        noise=0.36, emphasis="chaîne tiède",
        note="arc=installation; intention=émerveiller; emotion=envie_pressée; intensite=1; destinataire=enfant; sous_texte=un mot d'école cherche une oreille; tempo=naturel; sourire=léger; respiration=ample",
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
        note="arc=confirmation; intention=relancer; emotion=joie_discrète; intensite=1; destinataire=enfant; sous_texte=on_t_a_entendu; tempo=naturel; sourire=léger; respiration=fluide",
    ),
    "action": dict(
        rate="medium", wpm=146, speed=1.0, piper=1.10, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=420, sentence=250, energy="lively", contour="dynamic",
        noise=0.37, emphasis=None,
        note="arc=action; intention=entraîner; emotion=élan; intensite=2; destinataire=enfant; sous_texte=il_veut_dire_le_mot_tout_de_suite; tempo=vif; sourire=léger; respiration=courte",
    ),
    "obstacle": dict(
        rate="medium", wpm=134, speed=0.93, piper=1.18, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="medium", db=0,
        pause=520, sentence=300, energy="tense", contour="dynamic",
        noise=0.34, emphasis=None,
        note="arc=obstacle; intention=alerter_sans_effrayer; emotion=inquiétude_légère; intensite=2; destinataire=enfant; sous_texte=le_mot_peut_se_perdre; tempo=resserré; sourire=aucun; respiration=retenue",
    ),
    "resolution": dict(
        rate="medium", wpm=140, speed=0.97, piper=1.14, pitch="medium",
        pitch_ssml="medium", pitch_tag=None, volume="medium", db=0,
        pause=560, sentence=270, energy="bright", contour="falling",
        noise=0.35, emphasis=None,
        note="arc=résolution; intention=faire_vivre_la_réussite; emotion=soulagement_joyeux; intensite=2; destinataire=enfant; sous_texte=le_mot_trouve_une_oreille; tempo=naturel; sourire=franc; respiration=relâchée",
    ),
    "ending": dict(
        rate="slow", wpm=118, speed=0.85, piper=1.28, pitch="low",
        pitch_ssml="-2st", pitch_tag="low-pitch", volume="soft", db=-3,
        pause=900, sentence=340, energy="calm", contour="falling",
        noise=0.31, emphasis=None,
        note="arc=retour; intention=refermer; emotion=tendresse_et_fierté_calme; intensite=1; destinataire=enfant; sous_texte=la_chaîne_et_le_galet_ont_leur_place; tempo=posé; sourire=léger; respiration=ample",
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
    if n > N2:
        raise SystemExit(f"{n}>{N2}: {phrase}")
    if n == 0:
        raise SystemExit(f"vide: {role}|{phrase}")
    marks = phrase.count(".") + phrase.count("?") + phrase.count("!")
    if marks != 1:
        raise SystemExit(f"ponctuation {marks}: {phrase}")
    if not phrase.endswith((".", "?", "!")):
        raise SystemExit(f"fin: {phrase}")
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
    if m.get("emphasis") and m["emphasis"] not in text:
        m["emphasis"] = None
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


N, E, P, M = "narrateur", CHILD, "papa", "maman"


def t2_scenes() -> dict:
    return {
        ("sable", "ballon"): (
            L(
                (N, "Nino ramasse un ballon rouge, un peu rêche, près du bac."),
                (N, "Il le lance vers le trou où le galet a disparu."),
                (E, "Maman, le mot de l'école, il est là !"),
                (N, "Le ballon rebondit sur le sable et couvre le gris."),
                (N, "Maman répond à papa au sujet de la pomme."),
                (N, "La phrase de Nino se perd dans le poum."),
                (N, "Ses joues chauffent. Il arrête le ballon avec le pied."),
                (E, "Quand le filet est posé, je roule le ballon jusqu'à toi ?"),
                (M, "Oui. Le filet est là. Roule, puis on t'écoute."),
                (N, "Le ballon avance, lent, et s'arrête contre sa chaussure."),
                (P, "Le galet est sous le sable. On le suit comment ?"),
            ),
            "ballon,sable",
            "ballon rouge",
        ),
        ("sable", "seau"): (
            L(
                (N, "Nino saisit le seau bleu, lèvre un peu ébréchée."),
                (N, "Il le plonge, trop vite, pile où le galet a filé."),
                (E, "Je l'ai ! Le mot aussi !"),
                (N, "Le sable siffle. Une poussière blonde lui pique le nez."),
                (N, "Papa parle de la fermeture, sans voir le seau."),
                (N, "Nino tousse. Le mot reste collé."),
                (N, "Il pose le seau. Il attend que papa finisse."),
                (E, "Je verse tout doucement, après ta phrase ?"),
                (P, "Ma phrase est finie. Verse. Nous regardons."),
                (N, "Un filet de sable tombe. Un bord gris apparaît."),
                (M, "Le voilà. Comment veux-tu le garder, ce galet ?"),
            ),
            "seau,sable",
            "seau bleu",
        ),
        ("sable", "doudou"): (
            L(
                (N, "Nino sort le doudou gris de la poche du manteau."),
                (N, "Il parle contre l'oreille en tissu, tout près du bac."),
                (E, "Doudou, à l'école, près des crochets..."),
                (N, "Le sable colle aux poils. La voix reste dans la fourrure."),
                (N, "Maman cherche la pomme. Elle n'a pas entendu."),
                (N, "Nino recule le doudou. Son ventre se serre."),
                (N, "Il assied le doudou sur le rebord, face à maman."),
                (E, "Quand tu me regardes, je dis le mot à toi ?"),
                (M, "Je te regarde. L'oreille du doudou peut écouter aussi."),
                (N, "Un grain de sable brille sur le museau."),
                (P, "Le galet est là, sous tes doigts. On le sort ?"),
            ),
            "doudou,sable",
            "doudou gris",
        ),
        ("toboggan", "ballon"): (
            L(
                (N, "Nino gravit l'échelle, le ballon coincé sous le bras."),
                (N, "Le métal du toboggan est chaud, comme la chaîne."),
                (E, "Le ballon va porter le mot en bas !"),
                (N, "Il lâche trop tôt. Le ballon dévale, vide."),
                (N, "Le galet reste dans son poing, en haut."),
                (N, "Papa parle du cartable, au pied de l'échelle."),
                (N, "La voix de Nino rebondit dans le couloir de métal."),
                (E, "Quand vous levez la tête, je dis le mot ?"),
                (M, "On lève la tête. On te voit. On t'écoute."),
                (N, "Le ballon s'immobilise dans l'herbe, tout rond."),
                (P, "Le galet n'est pas parti. Que veux-tu en faire ?"),
            ),
            "ballon,toboggan",
            "métal du toboggan",
        ),
        ("toboggan", "seau"): (
            L(
                (N, "Nino hisse le seau bleu, galet au fond, jusqu'au palier."),
                (N, "Le seau tape un échelon. Un bruit sec part."),
                (E, "Écoutez le seau ! Il a mon mot !"),
                (N, "Papa répond à maman. Le bruit se mélange aux phrases."),
                (N, "Le seau penche. Le galet glisse vers le bord."),
                (N, "Nino rattrape le gris, sans crier."),
                (N, "Il attend que le métal se taise."),
                (E, "Quand le seau ne tape plus, je parle ?"),
                (P, "Il ne tape plus. Nous sommes en bas. Nous t'écoutons."),
                (N, "Le palier vibre un peu, puis s'arrête."),
                (M, "Le galet est sauvé. Comment le descendre ?"),
            ),
            "seau,echelle",
            "seau bleu",
        ),
        ("toboggan", "doudou"): (
            L(
                (N, "Nino pose le doudou gris sur le palier, face à la pente."),
                (N, "Il s'accroupit. Il parle à l'oreille de tissu."),
                (E, "Toi, tu écoutes. Après, maman écoutera."),
                (N, "En bas, maman parle du filet. Elle n'entend pas."),
                (N, "Le ventre de Nino se serre, comme près des crochets."),
                (N, "Il prend le doudou. Il descend marche par marche."),
                (E, "Quand j'arrive en bas, je te dis le mot ?"),
                (M, "Oui. Tes pieds sont sur l'herbe. Je t'écoute."),
                (N, "Le doudou sent le métal chaud, et un peu de poussière."),
                (P, "Le galet est dans ta main. On le pose où ?"),
            ),
            "doudou,toboggan",
            "palier",
        ),
        ("balancoires", "ballon"): (
            L(
                (N, "Nino tient la chaîne d'une main, le ballon de l'autre."),
                (N, "Il frappe le poteau, pour faire une clochette plus forte."),
                (E, "Maman, le mot, il tape comme ça !"),
                (N, "Poum, tic, poum. Papa parle par-dessus le rythme."),
                (N, "Le galet glisse dans un maillon, puis tombe."),
                (N, "Nino arrête le ballon. Il serre la chaîne, sans la bouger."),
                (E, "Quand la chaîne ne tape plus, je parle ?"),
                (P, "Elle ne tape plus. Le ballon aussi. Je t'écoute."),
                (N, "Un rond de poussière reste au pied du poteau."),
                (M, "Le galet est dans la poussière. Comment le reprendre ?"),
            ),
            "ballon,chaine",
            "poteau",
        ),
        ("balancoires", "seau"): (
            L(
                (N, "Nino glisse le seau sous le siège, pour attraper le galet."),
                (N, "La chaîne tiède balance. Le seau reçoit un coup."),
                (E, "Il est dedans ! Écoutez !"),
                (N, "Le plastique sonne. Maman répond à papa, plus loin."),
                (N, "Nino retient la chaîne. Le seau cesse de danser."),
                (N, "Il attend que leurs phrases se ferment."),
                (E, "Quand vous avez fini, je montre le fond du seau ?"),
                (M, "Nous avons fini. Montre. Nous regardons avec toi."),
                (N, "Au fond, le galet gris fait un petit poids."),
                (P, "Il est là. Que veux-tu qu'on en fasse, maintenant ?"),
            ),
            "seau,chaine",
            "fond du seau",
        ),
        ("balancoires", "doudou"): (
            L(
                (N, "Nino assied le doudou sur le siège, une oreille vers la chaîne."),
                (N, "Il lui parle, le galet contre le tissu."),
                (E, "Toi tu entends. Eux, ils parlent trop."),
                (N, "La chaîne tic. Papa n'a pas levé les yeux."),
                (N, "Nino descend le doudou. Il touche le coude de maman."),
                (E, "Quand tu te tournes, je dis le mot à toi, pas au doudou ?"),
                (M, "Je me tourne. Tes mots sont pour nous."),
                (N, "Le siège se balance, vide, un arc minuscule."),
                (P, "Le galet est chaud de ta main. On le pose où ?"),
            ),
            "doudou,chaine",
            "siège",
        ),
    }


def t3_scenes() -> dict:
    data: dict = {}

    def S(*rows):
        return L(*rows)

    # --- SABLE + BALLON ---
    data[("sable", "ballon", "banc")] = (
        S(
            (N, "Nino roule le ballon jusqu'au banc, sable aux genoux."),
            (N, "Il s'assoit. Le bois est tiède, comme la chaîne."),
            (E, "Le ballon garde la place. Moi, je dis le mot."),
            (N, "Il ouvre la bouche trop vite. Papa range le filet."),
            (M, "Attends que le filet soit posé, puis toute la phrase."),
            (N, "Nino attend. Le ballon ne bouge plus contre le pied."),
            (E, "À l'école, près des crochets, une voix a parlé trop près."),
            (E, "Ça m'a serré le ventre. La maîtresse m'a donné le galet."),
            (P, "Nous t'avons entendu jusqu'au bout."),
            (N, "Le galet repose sur une latte, un grain de sable dessus."),
        ),
        S(
            (N, "Le parc se vide. Une lampe s'allume près du portail."),
            (M, "Raconte-nous les crochets, sans rien sauter."),
            (E, "La voix était trop près. Le galet m'a gardé le mot."),
            (N, "Le ballon rouge dort sous le banc, un peu poussiéreux."),
            (N, "La chaîne tape un tic, loin, puis se tait."),
            (N, "Le galet reste sur la latte, tiède du bois."),
        ),
        "banc,ballon",
        "lampe,chaine",
        "latte",
    )
    data[("sable", "ballon", "poche")] = (
        S(
            (N, "Nino essuie le galet contre son short, puis le glisse."),
            (N, "La poche sent le sable, et un peu de craie."),
            (E, "Il rentre. Le mot aussi."),
            (N, "Il parle en marchant. Papa ferme le cartable."),
            (P, "On s'arrête. Tes pieds, puis tes mots."),
            (N, "Nino s'arrête. Le ballon reste coincé sous son coude."),
            (E, "Près des crochets, une voix a parlé trop près."),
            (E, "Mon ventre s'est serré. La maîtresse m'a mis le galet là."),
            (M, "Tes pieds sont posés. Nous avons toute la phrase."),
            (N, "Un grain de sable reste dans la couture de la poche."),
        ),
        S(
            (N, "Sur le chemin, les semelles font un bruit de gravier."),
            (P, "Le galet est où, maintenant ?"),
            (E, "Dans ma poche. Le mot aussi, il est sorti."),
            (N, "Le ballon penche dans le filet, contre la pomme."),
            (N, "Derrière eux, la chaîne du parc n'a plus de soleil."),
            (N, "Nino met la main sur le gris, rond et secret."),
        ),
        "poche,sable",
        "chemin,gravier",
        "poche",
    )
    data[("sable", "ballon", "paume")] = (
        S(
            (N, "Nino pose le ballon contre le pied de maman, comme un signal."),
            (N, "Il ouvre sa main. Le galet y laisse un rond frais."),
            (E, "Pour toi. Après, je dis le mot."),
            (N, "Maman ouvre la paume. Papa parle d'un bouton."),
            (M, "Un instant. Le bouton, puis ta pierre."),
            (N, "Nino attend. Le ballon ne roule plus."),
            (N, "Le galet passe. La paume de maman se referme, douce."),
            (E, "À l'école, une voix trop près, aux crochets."),
            (E, "Ça serrait. Elle m'a donné ça, pour vous le dire."),
            (P, "Ta pierre est arrivée. Tes mots aussi."),
        ),
        S(
            (N, "Maman garde le galet. Sa paume devient tiède, comme la chaîne."),
            (M, "On le rendra à la poche, après le goûter."),
            (E, "Le ballon a fait le signal. Vous avez pris le mot."),
            (N, "Un cercle pâle reste au milieu de sa main."),
            (N, "Le bac à sable redevient plat, sans trou."),
            (N, "Au loin, la balançoire penche, vide, sans tic."),
        ),
        "paume,ballon",
        "paume,goûter",
        "paume",
    )

    # --- SABLE + SEAU ---
    data[("sable", "seau", "banc")] = (
        S(
            (N, "Nino porte le seau jusqu'au banc, deux mains sur l'anse."),
            (N, "Il le pose. Un peu de sable fuit par le fond troué."),
            (E, "Le galet est au fond. Le mot est pour le banc."),
            (N, "Il s'assoit trop vite. Le seau vacille."),
            (P, "On pose l'anse, puis on parle. D'accord ?"),
            (N, "Nino pose l'anse. Il souffle par le nez."),
            (E, "Près des crochets, une voix a parlé trop près."),
            (E, "La maîtresse m'a donné le galet. Mon ventre s'est serré."),
            (M, "L'anse est posée. Nous t'écoutions."),
            (N, "Le galet reste dans le seau, au pied de la latte."),
        ),
        S(
            (N, "Une fourmi croise le pied du banc, puis part."),
            (P, "Le seau garde la pierre. Toi, tu gardes la phrase."),
            (E, "Oui. La voix trop près, et le galet dans le bleu."),
            (N, "Le bois sent la résine. Le plastique sent le sable."),
            (N, "La chaîne, derrière les arbres, fait un tic unique."),
            (N, "Nino pose un doigt sur l'anse, sans la soulever."),
        ),
        "banc,seau",
        "fourmi,banc",
        "anse",
    )
    data[("sable", "seau", "poche")] = (
        S(
            (N, "Nino penche le seau au-dessus de sa poche, très lent."),
            (N, "Le galet glisse, lourd, et tend le tissu."),
            (E, "Il rentre. Maintenant le mot."),
            (N, "Il parle pendant que papa secoue le seau vide."),
            (M, "Le seau d'abord, à l'envers, puis tes mots."),
            (N, "Nino attend le clac du plastique sur le rebord."),
            (E, "Aux crochets, une voix trop près. Ça serrait."),
            (E, "Elle m'a mis le galet dans la main, pour vous."),
            (P, "Le seau est calé. On a ta phrase entière."),
            (N, "Un cercle bleu reste imprimé dans le sable blond."),
        ),
        S(
            (N, "Ils quittent le bac. Le seau pend au filet, sale."),
            (M, "Ta poche est lourde. Ton mot, lui, est léger."),
            (E, "Le galet cogne le tissu, un coup minuscule."),
            (N, "Nino sourit de ce coup, pas de peur."),
            (N, "Derrière, le bac est plat. La pie a changé de miette."),
            (N, "La chaîne tiède n'a pas reçu de clochette, ce soir."),
        ),
        "poche,seau",
        "filet,seau",
        "tissu",
    )
    data[("sable", "seau", "paume")] = (
        S(
            (N, "Nino tend le seau. Maman avance la paume au-dessus."),
            (N, "Le galet tombe, un poids court, dans sa main."),
            (E, "Il est à toi le temps du mot."),
            (N, "Du sable coule entre ses doigts, fin, blond."),
            (P, "On souffle le sable, puis Nino parle. D'accord ?"),
            (N, "Nino hoche. Il attend le dernier grain."),
            (E, "Une voix trop près, aux crochets. Mon ventre s'est serré."),
            (E, "La maîtresse a dit de vous le donner, avec la pierre."),
            (M, "Ma paume a le galet. Mes oreilles ont le mot."),
            (N, "Un halo de poussière blonde reste sur sa peau."),
        ),
        S(
            (N, "Maman reverse le galet, plus tard, dans le seau propre."),
            (P, "On le lavera à la maison, sous le robinet."),
            (E, "Il aura l'eau. Vous avez eu le mot."),
            (N, "Le seau bleu se balance au retour, presque vide."),
            (N, "La chaîne du parc perd sa chaleur, maillon par maillon."),
            (N, "Nino frotte sa paume : un peu de sable y reste."),
        ),
        "paume,seau",
        "robinet,seau",
        "grain",
    )

    # --- SABLE + DOUDOU ---
    data[("sable", "doudou", "banc")] = (
        S(
            (N, "Nino installe le doudou d'abord, au milieu du banc."),
            (N, "Puis il s'assoit, galet dans la main, sable aux chaussettes."),
            (E, "Toi tu es là. Eux ils écoutent, après."),
            (N, "Il commence. Un camion passe sur la route, trop fort."),
            (M, "On attend le camion. Après, toute la phrase."),
            (N, "Le bruit file. Nino pose le galet sur les genoux du tissu."),
            (E, "Près des crochets, une voix a parlé trop près."),
            (E, "Ça serrait. Elle m'a donné le galet, pour la maison."),
            (P, "Le camion est parti. Nous avons ta phrase."),
            (N, "Une oreille de doudou penche, un peu de sable au bout."),
        ),
        S(
            (N, "Le banc garde trois chaleurs : bois, tissu, pierre."),
            (M, "Ton doudou a de la poussière. Ton mot, non."),
            (E, "On le secouera. Le mot, il est resté chez vous."),
            (N, "Nino tape deux fois le bois, sans se presser."),
            (N, "La chaîne répond, très loin, un tic paresseux."),
            (N, "Le galet glisse du tissu vers une latte, et s'arrête."),
        ),
        "banc,doudou",
        "banc,tissu",
        "oreille",
    )
    data[("sable", "doudou", "poche")] = (
        S(
            (N, "Nino glisse le galet dans la poche, le doudou par-dessus."),
            (N, "Le tissu fait un coussin. Le gris ne cogne plus."),
            (E, "Ils voyagent ensemble. Moi je dis le mot."),
            (N, "Il parle en secouant le sable de ses chaussettes."),
            (P, "Chaussettes d'abord. Après, on a les oreilles."),
            (N, "Nino arrête. Deux grains tombent sur le bois du rebord."),
            (E, "Aux crochets, une voix trop près. Mon ventre a fait mal."),
            (E, "La maîtresse a mis le galet là, pour que je vous le dise."),
            (M, "Tes chaussettes sont nettes. Tes mots aussi."),
            (N, "Le doudou dépasse de la poche, une oreille en sentinelle."),
        ),
        S(
            (N, "Au portail, Nino touche la poche : deux rondeurs, l'une molle."),
            (P, "La pierre et l'ami. Et le mot ?"),
            (E, "Le mot est sorti. Il n'est plus collé."),
            (N, "Le bac à sable est derrière, lisse, sans trou à lui."),
            (N, "Une pie reprend sa miette sous le toboggan."),
            (N, "La chaîne tiède n'a plus de soleil sur le dernier maillon."),
        ),
        "poche,doudou",
        "portail,poche",
        "sentinelle",
    )
    data[("sable", "doudou", "paume")] = (
        S(
            (N, "Nino met le doudou à cheval sur son bras, comme un témoin."),
            (N, "Il dépose le galet dans la paume de papa, sable et tout."),
            (E, "Toi tu le tiens. Moi je parle."),
            (N, "Papa souffle le grain. Maman range une lanière."),
            (M, "La lanière est bouclée. Nous t'écoutons."),
            (N, "Nino attendait ce bouclage, lèvres serrées."),
            (E, "Une voix trop près, aux crochets. Ça m'a serré."),
            (E, "Elle m'a donné le galet. Le doudou a entendu, lui aussi."),
            (P, "Ma paume a la pierre. La lanière est bouclée."),
            (N, "Le doudou penche vers la main, museau contre le pouce."),
        ),
        S(
            (N, "Papa rend le galet. Il sent la peau de la paume."),
            (M, "On le posera près du gobelet, à la maison."),
            (E, "Le doudou a vu. Vous avez entendu."),
            (N, "Un peu de sable reste dans les plis de la main de papa."),
            (N, "Nino souffle dessus, un petit vent, sans se moquer."),
            (N, "Au parc, la chaîne penche, tiède, sans pierre."),
        ),
        "paume,doudou",
        "gobelet,paume",
        "lanière",
    )

    # --- TOBOGGAN + BALLON ---
    data[("toboggan", "ballon", "banc")] = (
        S(
            (N, "Nino descend, le ballon sous le bras, le galet au poing."),
            (N, "Ils rejoignent le banc, face à la pente tiède."),
            (E, "Le ballon a dévalé tout seul. Le mot, non."),
            (N, "Il s'assoit. Le bois craque. Papa souffle."),
            (P, "Le craquement d'abord. Après, ta phrase."),
            (N, "Nino attend que le bois se taise."),
            (E, "En haut, j'ai eu le ventre serré, comme aux crochets."),
            (E, "Une voix trop près. La maîtresse m'a donné le galet."),
            (M, "Le banc s'est tu. Nous avons toute la phrase."),
            (N, "Le ballon rouge cale un pied de banc, pour ne plus rouler."),
        ),
        S(
            (N, "La pente du toboggan perd son soleil, bande après bande."),
            (M, "Ton ballon garde le banc. Ton mot garde nos oreilles."),
            (E, "Oui. La voix trop près, et le métal chaud."),
            (N, "Nino pose le galet dans une fente du bois."),
            (N, "Il ne tombe pas. Il tient, gris entre deux lattes."),
            (N, "La chaîne, de l'autre côté, tic une fois, puis plus."),
        ),
        "banc,toboggan",
        "pente,banc",
        "fente",
    )
    data[("toboggan", "ballon", "poche")] = (
        S(
            (N, "Au pied de l'échelle, Nino glisse le galet dans la poche."),
            (N, "Le ballon reste dans l'herbe, une rosace écrasée."),
            (E, "Il n'est pas parti avec le ballon. Moi non plus, le mot."),
            (N, "Il parle. Maman ramasse le ballon, et le bruit couvre."),
            (M, "Je le tiens. Plus de poum. Vas-y."),
            (N, "Nino pose une main sur la poche, l'autre sur l'échelle."),
            (E, "Aux crochets, une voix trop près. Ça serrait, en haut aussi."),
            (E, "Elle m'a donné le galet, pour que je vous le dise en bas."),
            (P, "On t'a vu descendre. On t'entend, là."),
            (N, "Un barreau de l'échelle reste chaud sous son pouce."),
        ),
        S(
            (N, "Ils laissent le toboggan. L'herbe se redresse sous le ballon."),
            (P, "Ta poche a la pierre. Nous, la phrase."),
            (E, "Le ballon a filé. Le mot a attendu le bas."),
            (N, "Nino frappe deux fois sa poche, un rythme court."),
            (N, "Le cartable, enfin fermé, tape sa hanche."),
            (N, "La chaîne du fond du parc n'a pas eu sa clochette."),
        ),
        "poche,echelle",
        "herbe,ballon",
        "barreau",
    )
    data[("toboggan", "ballon", "paume")] = (
        S(
            (N, "Maman lève les mains au bas de la pente, paumes ouvertes."),
            (N, "Nino, en haut, penche le galet. Il ne le jette pas."),
            (E, "Je le pose. Je ne le lance pas."),
            (N, "Il descend deux marches. Le galet rejoint la paume."),
            (N, "Le ballon attend dans l'herbe, témoin rond."),
            (P, "La pierre est arrivée. Maintenant le mot, s'il te plaît ?"),
            (N, "Nino pose les deux pieds dans l'herbe avant de parler."),
            (E, "Une voix trop près, aux crochets. Mon ventre s'est serré."),
            (E, "La maîtresse a dit : tu le donnes, ce soir."),
            (M, "Tu l'as donné. Tes pieds sont dans l'herbe."),
        ),
        S(
            (N, "La paume de maman se referme. Le galet y fait un nid."),
            (P, "On le mettra près de la fenêtre, pour qu'il voie le soir."),
            (E, "Le ballon a regardé. Vous aussi."),
            (N, "Le métal du toboggan retombe au gris, sans chaleur."),
            (N, "Nino touche le dos de la main de maman, puis recule."),
            (N, "Au fond, la chaîne penche, vide, un peu moins tiède."),
        ),
        "paume,pente",
        "fenetre,paume",
        "nid",
    )

    # --- TOBOGGAN + SEAU ---
    data[("toboggan", "seau", "banc")] = (
        S(
            (N, "Papa descend le seau, échelon par échelon, sans le balancer."),
            (N, "Ils le portent au banc, le galet coincé au fond."),
            (E, "Il n'a pas dévalé. Moi non plus."),
            (N, "Nino s'assoit. Il tape l'anse, trop tôt."),
            (M, "L'anse se tait, puis tu parles. D'accord ?"),
            (N, "Il lâche. Le plastique fait un dernier clac."),
            (E, "En haut, le ventre, comme aux crochets. Une voix trop près."),
            (E, "Elle m'a donné le galet. Le seau l'a gardé."),
            (P, "Le clac est passé. La phrase est entière."),
            (N, "Le seau bleu s'adosse au banc, anse vers Nino."),
        ),
        S(
            (N, "Un oiseau se pose sur le toit du toboggan, puis part."),
            (M, "Le seau a fait l'escalier. Toi, tu as fait la phrase."),
            (E, "Oui. La voix trop près, et le palier qui vibrait."),
            (N, "Nino regarde le fond : le galet y fait une ombre ronde."),
            (N, "Il ne le sort pas. Il le laisse au bleu, pour le chemin."),
            (N, "La chaîne, invisible d'ici, tic quelque part."),
        ),
        "banc,seau",
        "oiseau,toboggan",
        "escalier",
    )
    data[("toboggan", "seau", "poche")] = (
        S(
            (N, "Au dernier échelon, Nino prend le galet du seau."),
            (N, "Il le glisse dans la poche. Le seau redevient léger."),
            (E, "Le seau a fini. Le mot commence."),
            (N, "Papa pose le seau à l'envers, pour qu'il sèche."),
            (P, "Le fond vers le ciel. Puis tes mots vers nous."),
            (N, "Nino attend le plastique stable, dans l'herbe."),
            (E, "Aux crochets, une voix trop près. Ça serrait, là-haut."),
            (E, "La maîtresse m'a donné ça, pour la poche et pour vous."),
            (M, "Le seau sèche. Nous, on te reçoit."),
            (N, "Une goutte de rosée glisse sur le bleu, toute ronde."),
        ),
        S(
            (N, "Ils s'éloignent. Le seau, à l'envers, reste une minute."),
            (P, "On le reprend. Ta poche a le galet."),
            (E, "Et vous, le mot. La voix trop près."),
            (N, "Nino appuie le gris contre sa cuisse, à travers le tissu."),
            (N, "L'échelle du toboggan redevient un zigzag de métal."),
            (N, "La chaîne du parc n'a pas cliqueté, pas ce chemin-là."),
        ),
        "poche,seau",
        "rosee,seau",
        "envers",
    )
    data[("toboggan", "seau", "paume")] = (
        S(
            (N, "Papa tient le seau. Maman avance la paume au bord."),
            (N, "Nino bascule le fond, un geste court, pas une cascade."),
            (E, "Pour ta main. Pas pour l'herbe."),
            (N, "Le galet atterrit. La paume se creuse."),
            (N, "Un souffle d'air sent le métal du toboggan."),
            (P, "Il est arrivé. Tes pieds sont où ?"),
            (N, "Nino saute du dernier barreau. Deux pieds dans l'herbe."),
            (E, "Une voix trop près, aux crochets. Mon ventre s'est serré."),
            (E, "Elle a dit de le mettre dans une main de la maison."),
            (M, "Ma main est celle-là. Tu as visé la paume."),
        ),
        S(
            (N, "Le seau vide sonne un peu, léger, contre la cuisse de papa."),
            (P, "On le rentrera. La pierre voyage dans la main."),
            (E, "Le palier a tremblé. Le mot, non."),
            (N, "Maman ouvre un doigt : le galet montre un côté rêche."),
            (N, "Nino le reconnaît, celui de l'école."),
            (N, "Loin, la chaîne tiède attend une autre clochette."),
        ),
        "paume,seau",
        "seau,cuisse",
        "côté rêche",
    )

    # --- TOBOGGAN + DOUDOU ---
    data[("toboggan", "doudou", "banc")] = (
        S(
            (N, "Nino descend, doudou sous le menton, galet contre le tissu."),
            (N, "Ils s'installent au banc, la pente en face, plus sombre."),
            (E, "Il a entendu en haut. Vous, maintenant."),
            (N, "Le doudou s'affale. Nino parle dans le même temps."),
            (M, "On redresse l'ami, puis on ouvre les oreilles."),
            (N, "Nino redresse l'oreille. Il reprend, plus posé."),
            (E, "Aux crochets, une voix trop près. En haut, le ventre aussi."),
            (E, "La maîtresse m'a donné le galet. Le doudou l'a gardé chaud."),
            (P, "L'oreille est droite. Ta phrase aussi."),
            (N, "Un fil du doudou s'accroche à une écharde du banc."),
        ),
        S(
            (N, "Nino détache le fil, sans tirer trop fort."),
            (M, "Ton tissu a voyagé. Ton mot est arrivé."),
            (E, "Oui. La voix trop près, et le palier qui sentait le fer."),
            (N, "Le galet reste dans un pli du doudou, comme dans un nid."),
            (N, "Le toboggan est un long dos gris, sans personne."),
            (N, "Un tic de chaîne arrive, mince, entre les feuilles."),
        ),
        "banc,doudou",
        "fil,banc",
        "écharde",
    )
    data[("toboggan", "doudou", "poche")] = (
        S(
            (N, "Dans l'herbe, Nino glisse le galet, puis un bout de doudou."),
            (N, "La poche déborde. Une oreille reste dehors."),
            (E, "Ils se tiennent. Je peux dire."),
            (N, "Un vélo sonne sur la piste. Il parle quand même."),
            (P, "On laisse la sonnette. Après, toi."),
            (N, "La sonnette file. Nino reprend, main sur l'oreille."),
            (E, "Une voix trop près, aux crochets. Ça serrait en haut."),
            (E, "Elle m'a donné le galet. Il voyage avec le doudou."),
            (M, "La sonnette est partie. On a toute la phrase."),
            (N, "L'échelle jette une ombre en barreaux sur ses chaussures."),
        ),
        S(
            (N, "Le vélo n'est plus qu'un point, au bout de la piste."),
            (P, "Ta poche déborde d'amis. Nous, d'une phrase."),
            (E, "Le mot n'est plus collé. L'oreille le sait."),
            (N, "Nino rentre l'oreille, enfin, sous le bord du tissu."),
            (N, "Le palier du toboggan est vide, un carré de ciel dessus."),
            (N, "La chaîne, elle, garde sa tiédeur pour personne."),
        ),
        "poche,doudou",
        "velo,poche",
        "sonnette",
    )
    data[("toboggan", "doudou", "paume")] = (
        S(
            (N, "Nino garde le doudou. Il pose le galet dans la paume de maman."),
            (N, "Le tissu reste sous son nez, une odeur de lessive et de fer."),
            (E, "Lui a entendu là-haut. Toi, tu reçois la pierre."),
            (N, "Maman ferme les doigts. Papa plie le filet."),
            (P, "Le filet est plié. Tes mots peuvent sortir."),
            (N, "Nino attendait ce pli. Il lâche le menton du doudou."),
            (E, "Aux crochets, une voix trop près. Mon ventre s'est serré."),
            (E, "La maîtresse a dit de le poser dans une main, ce soir."),
            (M, "C'est fait. Le filet est plié."),
            (N, "Le doudou penche vers la paume, comme pour vérifier."),
        ),
        S(
            (N, "Ils marchent. Le doudou bat la hanche, régulier."),
            (P, "La pierre est chez maman. Le mot est chez nous."),
            (E, "Le fer du palier est derrière. Les crochets aussi."),
            (N, "Maman ouvre un instant : le galet y a pris sa chaleur."),
            (N, "Nino hoche. C'est la chaleur de la chaîne, presque."),
            (N, "Le toboggan, de dos, n'est plus qu'une lame grise."),
        ),
        "paume,doudou",
        "hanche,doudou",
        "lessive",
    )

    # --- BALANCOIRES + BALLON ---
    data[("balancoires", "ballon", "banc")] = (
        S(
            (N, "Nino laisse la chaîne. Il pousse le ballon jusqu'au banc."),
            (N, "Ils s'assoient face aux balançoires, le poteau un peu loin."),
            (E, "Le poum a fini. Le tic aussi. Le mot, maintenant."),
            (N, "Un siège vide se balance. Nino parle trop tôt."),
            (M, "On attend que le siège s'arrête, puis toute la phrase."),
            (N, "Le siège ralentit, s'immobilise, un peu de travers."),
            (E, "Aux crochets, une voix trop près. Ça m'a serré le ventre."),
            (E, "La maîtresse m'a donné le galet. Je voulais une clochette."),
            (P, "Le siège est sage. Ta phrase peut marcher."),
            (N, "Le ballon cale le pied du banc. Le galet tient sur une latte."),
        ),
        S(
            (N, "Les deux sièges pendent, jumeaux, sans personne."),
            (M, "Ta clochette n'a pas sonné. Tes mots, oui."),
            (E, "C'est mieux. La chaîne peut tic toute seule."),
            (N, "Nino regarde le maillon tiède, trop loin pour le doigt."),
            (N, "Le galet, sur le bois, a un côté plus clair, celui du soleil."),
            (N, "Une feuille tourne sous le poteau, puis s'en va."),
        ),
        "banc,ballon",
        "sieges,banc",
        "jumeaux",
    )
    data[("balancoires", "ballon", "poche")] = (
        S(
            (N, "Nino ramasse le galet dans la poussière, au pied du poteau."),
            (N, "Il le rentre. Le ballon reste contre le métal, immobile."),
            (E, "Plus de poum. Plus de tic. J'ai le mot."),
            (N, "Il parle. La chaîne, derrière, fait un arc minuscule."),
            (P, "On tient la chaîne. Toi, tu parles."),
            (N, "Papa pose deux doigts sur le maillon. Le tic meurt."),
            (E, "Une voix trop près, aux crochets. Mon ventre s'est serré."),
            (E, "Elle m'a donné le galet, pas pour le perdre sous le siège."),
            (M, "Il n'est plus perdu. Tes mots non plus."),
            (N, "Un cercle clair reste dans la poussière, là où le gris était."),
        ),
        S(
            (N, "Ils reculent. Papa lâche la chaîne. Elle ne reprend pas."),
            (P, "Ta poche a la pierre. Le poteau a le ballon, une minute."),
            (E, "On le reprend. Le mot, vous l'avez."),
            (N, "Nino touche le tissu : le galet y est, un peu poudreux."),
            (N, "La chaîne garde un dernier reflet, orange, très bas."),
            (N, "Le parc sent l'herbe coupée, plus fort qu'à l'arrivée."),
        ),
        "poche,poteau",
        "poussiere,chaine",
        "cercle clair",
    )
    data[("balancoires", "ballon", "paume")] = (
        S(
            (N, "Nino prend le galet. Il le pose dans la paume de papa."),
            (N, "Le ballon, sous le coude de maman, ne rebondit plus."),
            (E, "Pour toi. La chaîne a trop parlé, avant."),
            (N, "Papa pèse le gris. Il est plus chaud que le soir."),
            (M, "On garde le ballon sage. Nino, tes mots ?"),
            (N, "Nino pose une main sur la chaîne, sans la bouger."),
            (E, "Aux crochets, une voix trop près. Ça serrait."),
            (E, "La maîtresse m'a donné ça. Je voulais que ça clique, ici."),
            (P, "Ça a cliqué dans ma main. Tu as posé, pas lancé."),
            (N, "Un maillon laisse une marque tiède sur les doigts de Nino."),
        ),
        S(
            (N, "Papa referme les doigts. Le galet disparaît, pas le mot."),
            (M, "On le mettra près des clés, dans le bol de l'entrée."),
            (E, "Il aura un bol. Vous, vous avez les crochets."),
            (N, "Le ballon roule d'un pouce, puis maman l'arrête."),
            (N, "Les balançoires se font face, chaînes jumelles, sans pierre."),
            (N, "Le tic ne revient pas. Le soir a gagné le métal."),
        ),
        "paume,chaine",
        "cles,bol",
        "marque tiède",
    )

    # --- BALANCOIRES + SEAU ---
    data[("balancoires", "seau", "banc")] = (
        S(
            (N, "Nino soulève le seau, galet au fond, et gagne le banc."),
            (N, "La chaîne, derrière, reste tendue, sans tic."),
            (E, "Le seau a attrapé. Le banc va écouter."),
            (N, "Il pose trop près du bord. L'anse bascule."),
            (P, "Plus au milieu. Après, tes mots."),
            (N, "Nino recale. Le bleu s'immobilise entre eux."),
            (E, "Une voix trop près, aux crochets. Mon ventre s'est serré."),
            (E, "Elle m'a donné le galet. Le seau l'a rattrapé sous le siège."),
            (M, "Le seau est recalé. Nous t'écoutions."),
            (N, "Une latte du banc a une tache ronde, l'ombre du seau."),
        ),
        S(
            (N, "Ils restent un moment. Le seau fait un troisième convive."),
            (P, "On emporte le bleu. Le gris voyage au fond."),
            (E, "Et le mot voyage dans vos têtes."),
            (N, "Nino regarde les balançoires : deux sièges, zéro clochette."),
            (N, "Ça lui va. Le tic n'était pas le bon bruit."),
            (N, "Le soleil quitte le dernier maillon, sans cérémonie."),
        ),
        "banc,seau",
        "convive,seau",
        "tache ronde",
    )
    data[("balancoires", "seau", "poche")] = (
        S(
            (N, "Sous le siège, Nino prend le galet dans le seau."),
            (N, "Il le glisse. Le seau sonne, vide, un peu trop fort."),
            (E, "Chut, seau. C'est mon tour."),
            (N, "Maman pose un doigt sur le plastique. Le son meurt."),
            (M, "Il s'est tu. Nous t'écoutons."),
            (N, "Nino appuie le dos au poteau, poche lourde."),
            (E, "Aux crochets, une voix trop près. Ça serrait, ici aussi."),
            (E, "La maîtresse m'a donné le galet. Pas pour qu'il tombe."),
            (P, "Il n'est plus tombé. Ta phrase non plus."),
            (N, "Un maillon, au-dessus, garde un peu de poussière au creux."),
        ),
        S(
            (N, "Ils laissent le seau au filet. La poche de Nino tire le short."),
            (P, "Lourd, le soir. Léger, le mot."),
            (E, "Oui. La voix trop près. Le fond du seau."),
            (N, "Nino ne touche plus la chaîne. Il n'en a plus besoin."),
            (N, "Deux sièges attendent demain, métal plus froid."),
            (N, "Une pie traverse, sans miette, vers les arbres."),
        ),
        "poche,seau",
        "short,poche",
        "plastique",
    )
    data[("balancoires", "seau", "paume")] = (
        S(
            (N, "Nino tend le seau. Papa y plonge la paume, pas les deux."),
            (N, "Le galet se pose, un choc sourd, contre la peau."),
            (E, "Il est sorti du bleu. Le mot aussi."),
            (N, "La chaîne bouge d'un souffle. Nino parle trop tôt."),
            (M, "Deux doigts sur le maillon. Puis ta phrase."),
            (N, "Nino tient le maillon. Le souffle passe."),
            (E, "Une voix trop près, aux crochets. Mon ventre s'est serré."),
            (E, "Elle m'a donné ça. Je le mets dans une main, pas par terre."),
            (P, "Ma main l'a. Tu as tenu la chaîne."),
            (N, "Le seau vide reste entre ses genoux, léger comme un secret fini."),
        ),
        S(
            (N, "Papa garde le galet jusqu'au portail, paume un peu ouverte."),
            (M, "On le posera près des boutons, dans la coupelle."),
            (E, "Il aura la coupelle. Vous, les crochets."),
            (N, "Le seau tape le filet, un rythme mou, sans urgence."),
            (N, "La chaîne du parc, derrière, est un fil sombre."),
            (N, "Nino n'entend plus le tic. Il entend sa propre phrase."),
        ),
        "paume,seau",
        "coupelle,portail",
        "choc sourd",
    )

    # --- BALANCOIRES + DOUDOU ---
    data[("balancoires", "doudou", "banc")] = (
        S(
            (N, "Nino descend le doudou du siège, galet contre le ventre du tissu."),
            (N, "Ils gagnent le banc. La chaîne, seule, fait un arc minuscule."),
            (E, "Toi tu n'es plus capitaine. Eux, ils écoutent."),
            (N, "Le doudou roule. Nino le rattrape et parle ensemble."),
            (P, "L'ami d'abord, assis. Après, toi."),
            (N, "Nino cale le doudou entre eux. Il reprend."),
            (E, "Aux crochets, une voix trop près. Ça m'a serré."),
            (E, "La maîtresse m'a donné le galet. Je le disais au tissu, pas à vous."),
            (M, "Maintenant c'est à nous. L'ami est calé."),
            (N, "Une oreille du doudou touche le galet, comme une joue."),
        ),
        S(
            (N, "Le banc a quatre présences : deux adultes, un enfant, un tissu."),
            (P, "Cinq, avec la pierre."),
            (E, "Six, avec le mot. Il est sorti."),
            (N, "Nino rit, très bas, sans se moquer de la voix trop près."),
            (N, "Les balançoires, en face, n'ont plus de capitaine."),
            (N, "La chaîne penche, tiède, et se tait pour de bon."),
        ),
        "banc,doudou",
        "presences,banc",
        "capitaine",
    )
    data[("balancoires", "doudou", "poche")] = (
        S(
            (N, "Nino glisse le galet, puis tasse le doudou par-dessus, difficile."),
            (N, "La poche résiste. Une patte reste dehors, contre la chaîne."),
            (E, "Passe, patte. J'ai un mot."),
            (N, "Il parle. La patte frotte le maillon, un bruit de laine."),
            (M, "On rentre la patte. Puis tes mots, nets."),
            (N, "Nino rentre la patte. Le frottement cesse."),
            (E, "Une voix trop près, aux crochets. Mon ventre s'est serré."),
            (E, "Elle m'a donné le galet. Le doudou le cache, pour la maison."),
            (P, "La patte est rentrée. La phrase aussi, entière."),
            (N, "Le short tire de travers, lourd d'un côté seulement."),
        ),
        S(
            (N, "Au portail, Nino replace le short. La poche fait une bosse ronde."),
            (M, "Deux voyageurs. Un mot livré."),
            (E, "La chaîne n'a pas eu la clochette. Tant mieux."),
            (N, "Il caresse la bosse, à travers le tissu, un rond familier."),
            (N, "Derrière, un siège se balance d'un souffle, puis s'arrête."),
            (N, "Le métal perd sa tiédeur, maillon après maillon, sans bruit."),
        ),
        "poche,doudou",
        "bosse,portail",
        "patte",
    )
    data[("balancoires", "doudou", "paume")] = (
        S(
            (N, "Le doudou reste sur le siège, témoin. Nino avance vers maman."),
            (N, "Il pose le galet dans sa paume. La chaîne, à côté, ne tic plus."),
            (E, "Lui regarde. Toi tu reçois. Moi je dis."),
            (N, "Maman hoche. Papa tient le siège pour qu'il ne parte pas."),
            (P, "Le siège est tenu. Tes mots peuvent marcher."),
            (N, "Nino pose les deux mains derrière le dos, pour ne plus couper."),
            (E, "Aux crochets, une voix trop près. Ça m'a serré le ventre."),
            (E, "La maîtresse m'a donné le galet. Je le mets dans ta main."),
            (M, "Il y est. Tes mains sont restées derrière."),
            (N, "Le doudou, sur le siège, penche une oreille vers la paume."),
        ),
        S(
            (N, "Papa lâche le siège. Il ne balance presque plus."),
            (P, "On reprend l'ami. La pierre reste chez maman."),
            (E, "Le mot reste chez vous. Les crochets, loin."),
            (N, "Nino prend le doudou. Le siège, vide, a une chaleur de tissu."),
            (N, "La paume de maman garde un rond gris, caché par les doigts."),
            (N, "La chaîne tiède, enfin, n'a plus rien à dire."),
        ),
        "paume,doudou",
        "siege,tissu",
        "mains derrière",
    )

    return data


TICS = ("tout doux", "tout calme", " tout bas", "encore", "déjà")


def assert_clean(script: str, cid: str) -> None:
    low = script.lower()
    for t in TICS:
        if t in low:
            raise SystemExit(f"{cid} tic: {t}")


def build() -> None:
    src = json.loads((ROOT / SID / "source.json").read_text(encoding="utf-8"))
    by_src = {c["chunk_id"]: c for c in src["chunks"]}
    out_chunks: dict[str, dict] = {}

    def put(cid: str, lines: list[str], profile: str, sons: str = "", extra: dict | None = None) -> None:
        out_chunks[cid] = voice(by_src[cid], lines, profile, sons, extra)
        assert_clean(out_chunks[cid]["script"], cid)

    put(
        "CHK_T0000_P0000",
        L(
            (N, "Derrière l'école, le parc du village tient le soleil de quatre heures."),
            (N, "Les barreaux du portail sont chauds sous les doigts."),
            (N, "Nino arrive avec papa et maman, cartable contre la hanche."),
            (N, "Le banc de bois sent la résine, et un peu de craie."),
            (N, "Un manteau bleu est plié dessus, manche qui pend."),
            (N, "Dans la poche du short, un galet gris attend, lisse d'un côté."),
            (N, "Sa maîtresse l'a posé dans sa main, près des crochets."),
            (N, "La chaîne de la balançoire pend, tiède, et tape un tic contre le poteau."),
            (N, "Ça sent l'herbe coupée, et la poussière du chemin."),
            (N, "Une pie picore une miette sous le toboggan."),
            (N, "Papa lutte avec la fermeture du cartable, coincée."),
            (N, "Maman range une pomme dans le filet."),
            (N, "En ce moment, Nino serre le galet dans sa paume."),
            (E, "Il va faire clochette, sur la chaîne tiède !"),
            (E, "Maman, à l'école, près des crochets !"),
            (N, "Papa parle de la fermeture."),
            (N, "Maman lui répond, sans se tourner."),
            (N, "Les mots de Nino se cognent aux leurs, puis tombent."),
            (N, "Le galet glisse, tape le gravier, et roule sous le banc."),
            (E, "Attendez, le mot va partir !"),
            (N, "Personne ne se baisse. La chaîne tape son tic, vide."),
            (N, "Le ventre de Nino se serre, comme près des crochets."),
            (M, "Tu disais quelque chose, Nino ?"),
            (E, "Oui. Mais ça a filé avec le galet."),
            (P, "On va le chercher. Où veux-tu commencer ?"),
            (N, "Nino souffle. La clochette n'a pas sonné."),
        ),
        "opening",
        "parc,chaine",
        {"emphasis": "chaîne tiède"},
    )

    put(
        "CHK_T0001_P0000",
        L(
            (N, "Trois coins du parc peuvent recevoir le galet, et le mot."),
            (M, "Le bac à sable, le toboggan, ou les balançoires ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "le bac à sable", "option_2_label": "le toboggan", "option_3_label": "les balançoires"}},
    )

    put(
        "CHK_T0001_P0001",
        L(
            (N, "Nino ramasse le galet sous le banc, un peu poudreux."),
            (N, "Il court vers le bac. Le sable est frais, blond, collant."),
            (N, "Le bois du rebord gratte ses genoux."),
            (E, "Je le cache, puis je crie le mot !"),
            (N, "Il enfouit le gris trop vite. Une vague de sable le recouvre."),
            (N, "Maman répond à papa au sujet de la pomme."),
            (N, "La phrase de Nino s'émiette, comme le sable."),
            (N, "Son ventre se serre. Il s'arrête. Il touche la manche."),
            (E, "Quand le filet est posé, je peux dire le mot ?"),
            (M, "Oui. Le filet est là. Je t'écoute."),
            (N, "Un bord gris reparaît, minuscule, entre deux doigts."),
            (P, "Le galet est sous le sable. On le suit comment ?"),
        ),
        "action",
        "sable,rebord",
        {"emphasis": "bac"},
    )
    put(
        "CHK_T0001_P0001_Q0001",
        L(
            (N, "Nino a parlé trop vite, dans le sable."),
            (M, "Que fait-il avant de dire le mot ?"),
        ),
        "clue",
        "",
        {
            "night_policy": "skip",
            "fields": {
                "expected_answer": "attendre",
                "accepted_examples": "attendre | il attend | se taire | écouter | raconter",
                "retry_prompt": "Il touche la manche. Ensuite ?",
                "engine_ok_text": "Oui, il attend que le filet soit posé.",
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
            },
        },
    )
    put(
        "CHK_T0001_P0001_C0001",
        L(
            (M, "Oui. Il attend que le filet soit posé."),
            (N, "Papa pose le filet. La pomme s'immobilise."),
            (P, "Voilà. Tes mots ont de la place."),
            (E, "Le galet est sous le sable. Le mot, lui, est là."),
            (M, "Merci d'avoir attendu ma phrase, Nino."),
            (N, "Le bac sent le bois mouillé, et un peu de fer."),
            (N, "Nino garde un doigt sur le bord gris, sans crier."),
        ),
        "confirm",
        "filet,sable",
        {"emphasis": "filet"},
    )
    put(
        "CHK_T0001_P0001_T0002_P0000",
        L(
            (N, "Dans le sable, le galet a besoin d'une aide."),
            (P, "Le ballon, le seau, ou le doudou ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "le ballon", "option_2_label": "le seau", "option_3_label": "le doudou"}},
    )

    put(
        "CHK_T0001_P0002",
        L(
            (N, "Nino ramasse le galet. Il gravit l'échelle du toboggan."),
            (N, "Le métal est chaud, comme la chaîne, sous ses paumes."),
            (N, "En haut, le ventre se serre, comme près des crochets."),
            (E, "Maman, le mot de l'école ! Il tombe avec moi !"),
            (N, "Sa voix rebondit dans le couloir de métal, creuse."),
            (N, "Papa parle de la fermeture, en bas, sans lever la tête."),
            (N, "Le galet glisse vers la pente. Nino le rattrape."),
            (N, "Il s'assoit sur le palier. Il ne crie plus."),
            (E, "Quand vous levez la tête, je dis le mot ?"),
            (M, "On lève la tête. On te voit. On t'écoute."),
            (N, "Un nuage passe. L'ombre coupe la pente en deux."),
            (P, "Le galet n'est pas parti. Que veux-tu en faire ?"),
        ),
        "action",
        "toboggan,echelle",
        {"emphasis": "palier"},
    )
    put(
        "CHK_T0001_P0002_Q0001",
        L(
            (N, "En haut du toboggan, sa voix n'est pas arrivée."),
            (P, "Que fait Nino avant de reparler ?"),
        ),
        "clue",
        "",
        {
            "night_policy": "skip",
            "fields": {
                "expected_answer": "attendre",
                "accepted_examples": "attendre | il attend | lever la tête | écouter | se taire",
                "retry_prompt": "Il s'assoit sur le palier. Ensuite ?",
                "engine_ok_text": "Oui, il attend qu'on lève la tête.",
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
            },
        },
    )
    put(
        "CHK_T0001_P0002_C0001",
        L(
            (P, "Oui. Il attend que les visages se lèvent."),
            (N, "Maman plisse les yeux. Papa lâche la fermeture."),
            (M, "Nous te voyons, là-haut, sur le métal."),
            (E, "Le mot n'a pas dévalé. Il est resté avec moi."),
            (P, "Merci d'avoir attendu nos visages."),
            (N, "Le palier vibre un peu, puis s'arrête."),
            (N, "Le galet tient, gris, entre deux genoux."),
        ),
        "confirm",
        "palier",
        {"emphasis": "visages"},
    )
    put(
        "CHK_T0001_P0002_T0002_P0000",
        L(
            (N, "En haut, le galet a besoin d'une aide pour descendre."),
            (M, "Le ballon, le seau, ou le doudou ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "le ballon", "option_2_label": "le seau", "option_3_label": "le doudou"}},
    )

    put(
        "CHK_T0001_P0003",
        L(
            (N, "Nino ramasse le galet. Il court vers les balançoires."),
            (N, "La chaîne est tiède, un peu rêche, comme au portail."),
            (N, "Il veut coincer le gris dans un maillon, et parler."),
            (E, "Clochette, et le mot !"),
            (N, "La chaîne tape. Le tic recouvre sa voix."),
            (N, "Papa parle de la fermeture. Les deux bruits se mélangent."),
            (N, "Le galet glisse, tombe dans la poussière, sous le siège."),
            (N, "Nino retient la chaîne. Il touche le coude de papa."),
            (E, "Quand la chaîne ne tape plus, je parle ?"),
            (P, "Elle ne tape plus. Je t'écoute."),
            (N, "Un rond de poussière entoure le galet, tout gris."),
            (M, "Le galet est là. Comment veux-tu le reprendre ?"),
        ),
        "action",
        "chaine,poussiere",
        {"emphasis": "chaîne"},
    )
    put(
        "CHK_T0001_P0003_Q0001",
        L(
            (N, "La chaîne a couvert sa voix, près des balançoires."),
            (M, "Que fait Nino maintenant ?"),
        ),
        "clue",
        "",
        {
            "night_policy": "skip",
            "fields": {
                "expected_answer": "attendre",
                "accepted_examples": "attendre | il attend | tenir la chaîne | se taire | écouter",
                "retry_prompt": "Il retient la chaîne. Ensuite ?",
                "engine_ok_text": "Oui, il attend que la chaîne se taise.",
                "engine_near_text": "Tu es tout près. Écoute l'indice.",
            },
        },
    )
    put(
        "CHK_T0001_P0003_C0001",
        L(
            (M, "Oui. Il attend que la chaîne se taise."),
            (N, "Papa pose deux doigts sur le maillon. Le tic meurt."),
            (P, "Ce silence est à toi. Tes mots aussi."),
            (E, "Le galet est sous le siège. Le mot, lui, est prêt."),
            (M, "Merci d'avoir retenu la chaîne, Nino."),
            (N, "Le siège se balance d'un souffle, puis s'arrête."),
            (N, "La poussière brille, un peu, autour du gris."),
        ),
        "confirm",
        "chaine",
        {"emphasis": "maillon"},
    )
    put(
        "CHK_T0001_P0003_T0002_P0000",
        L(
            (N, "Sous le siège, le galet a besoin d'une aide."),
            (P, "Le ballon, le seau, ou le doudou ?"),
        ),
        "choice",
        "",
        {"fields": {"option_1_label": "le ballon", "option_2_label": "le seau", "option_3_label": "le doudou"}},
    )

    lieu_key = {"1": "sable", "2": "toboggan", "3": "balancoires"}
    act_key = {"1": "ballon", "2": "seau", "3": "doudou"}
    obj_key = {"1": "banc", "2": "poche", "3": "paume"}

    t2 = t2_scenes()
    t3q = {
        ("sable", "ballon"): "Le ballon a marqué le sable. Où dire le mot ?",
        ("sable", "seau"): "Le seau a montré le galet. Où dire le mot ?",
        ("sable", "doudou"): "Le doudou a une oreille prête. Où dire le mot ?",
        ("toboggan", "ballon"): "Le ballon est en bas. Où dire le mot ?",
        ("toboggan", "seau"): "Le seau a gardé le galet. Où dire le mot ?",
        ("toboggan", "doudou"): "Le doudou a descendu. Où dire le mot ?",
        ("balancoires", "ballon"): "Le ballon s'est tu. Où dire le mot ?",
        ("balancoires", "seau"): "Le seau a rattrapé le galet. Où dire le mot ?",
        ("balancoires", "doudou"): "Le doudou n'est plus capitaine. Où dire le mot ?",
    }

    for li in "123":
        for ac in "123":
            lieu, act = lieu_key[li], act_key[ac]
            lines, sons, emph = t2[(lieu, act)]
            cid = f"CHK_T0001_P000{li}_T0002_P000{ac}"
            put(cid, lines, "obstacle", sons, {"emphasis": emph})
            put(
                f"{cid}_T0003_P0000",
                L(
                    (N, t3q[(lieu, act)]),
                    (M, "Le banc, la poche, ou la paume ?"),
                ),
                "choice",
                "",
                {"fields": {"option_1_label": "le banc", "option_2_label": "la poche", "option_3_label": "la paume"}},
            )

    scenes = t3_scenes()
    for li in "123":
        for ac in "123":
            for ob in "123":
                lieu, act, obj = lieu_key[li], act_key[ac], obj_key[ob]
                passage, ending, s3, se, emph = scenes[(lieu, act, obj)]
                base = f"CHK_T0001_P000{li}_T0002_P000{ac}_T0003_P000{ob}"
                put(base, passage, "resolution", s3, {"emphasis": emph})
                put(f"{base}_F0001", ending, "ending", se, {"emphasis": "galet"})

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
        if c["kind"] == "passage"
        and "T0003_P000" in c["chunk_id"]
        and "_F0001" not in c["chunk_id"]
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
        "Après l'école, la chaîne de la balançoire est tiède et tape un tic contre le poteau. "
        "Nino serre un galet gris : la maîtresse l'a posé dans sa main, près des crochets, "
        "après qu'une voix a parlé trop près. Il veut en faire une clochette, et donner le mot. "
        "Sa première phrase se perd dans la fermeture du cartable ; le galet roule sous le banc. "
        "Le bac, le toboggan ou les balançoires changent l'obstacle. "
        "Le ballon, le seau ou le doudou changent la manière. "
        "Le banc, la poche ou la paume décident où le mot atterrit. "
        "Le soir, la chaîne n'a plus besoin de clochette : le galet a une place, et le mot aussi."
    )
    merged["title"] = "La chaîne tiède et le galet"
    merged["characters"] = "Nino, papa, maman"
    merged["setting"] = "au parc, après l'école"
    merged["chunks"] = [out_chunks[c["chunk_id"]] for c in src["chunks"]]
    check(SID, merged["age_band"], merged["chunks"])

    # mots par chemin
    def path_words(a: str, b: str, c: str) -> int:
        ids = [
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
        return sum(words(out_chunks[i]["text"]) for i in ids)

    totals = [path_words(a, b, c) for a in "123" for b in "123" for c in "123"]
    print(f"chemins {min(totals)}–{max(totals)} moy {sum(totals)//len(totals)}")

    (ROOT / SID / "merged.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / SID / "RELECTURE.md").write_text(
        "\n".join(
            [
                "# TREE-COL-033 — La chaîne tiède et le galet",
                "",
                "- **Public :** N2, 4–5 ans, lecture interactive familiale",
                "- **Leçon :** COL.ECO.001 — écouter à l'école, en parler à la maison (implicite)",
                "- **Secondaire :** COL.POL.001 — demander avec attention (implicite)",
                "- **Personnages :** Nino, papa, maman",
                "- **Lieu :** parc du village, après l'école, chaîne de balançoire, galet",
                "- **Structure conservée :** 86 nœuds, trois choix à trois options, 27 chemins et 27 fins distinctes",
                "",
                "Relu : monde, désir, imprévu, question, résolution, fin heureuse. `chunk_id` / `kind` inchangés.",
                "",
                "## Promesse narrative",
                "",
                "Après l'école, Nino veut pendre son galet à la chaîne tiède, comme une clochette, "
                "et donner à papa et maman le mot qu'il a gardé près des crochets. "
                "Sa première phrase se perd dans la fermeture du cartable ; le galet roule. "
                "Le bac, le toboggan ou les balançoires changent l'échec. "
                "Le ballon, le seau ou le doudou changent la manière de récupérer la pierre. "
                "Le banc, la poche ou la paume décident où le mot atterrit. "
                "Le soir, la chaîne n'a plus besoin de clochette.",
                "",
                "## Vécu",
                "",
                "Nino veut la clochette **maintenant**, et dire le mot tout de suite. "
                "Il coupe. Personne n'entend. Le galet file. Le ventre se serre. "
                "Il touche une manche, attend un filet, un visage, un tic qui s'arrête, puis on l'écoute. "
                "La leçon se voit : parler dans les mots des autres perd le galet ; "
                "attendre la fin de la phrase livre le mot des crochets. "
                "Pas de « on écoute la maîtresse » récité.",
                "",
                "## Améliorations",
                "",
                "- Titre noyau conservé. Kenzo → Nino. Parc après l'école, pas calque COL-015 (pas d'escargot, pas de dîner-soupe).",
                "- Première tentative ratée dès l'ouverture (fermeture du cartable, galet sous le banc).",
                "- T1/T2/T3 changent l'obstacle, pas seulement le décor.",
                "- T3 Tom/Léa/Sami → le banc, la poche, la paume.",
                "- Refrains « on va apprendre / voici le geste / si malaise on raconte / Bravo bon travail / l'histoire est finie » retirés.",
                "- Un merci vécu, lié au geste (attendre le filet, les visages, la chaîne).",
                "- 27 fins textuellement distinctes : chaîne + place unique du galet + mot entendu.",
                "- TTS par fonction (opening / choice / clue / confirm / action / obstacle / resolution / ending).",
                f"- Mots par chemin : {min(totals)}–{max(totals)} (moyenne {sum(totals)//len(totals)}).",
                "",
                "## Direction vocale",
                "",
                "Chaque segment a un `notes` : arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration. "
                "`slow` réservé aux choix, indices et fins. Action plus vive. Fins : pitch bas, volume doux, pause longue.",
                "",
                "## Contrôles",
                "",
                "- 86 chunks",
                "- 27 chemins, 27 fins distinctes, 27 climats T3 distincts, 9 T2 distincts",
                "- `text` = `script` collé, N2 ≤ 15 mots/phrase",
                "- `text_ssml` et `text_xai_tags` enrichis sur les 86 chunks",
                "- graphe `option_*_next` / `default_next` / `kind` inchangés",
                "- `check()` OK",
                "",
                "## Non vérifié",
                "",
                "Audio (pas cuit). Durée réelle à l'écoute. Playtest moteur. Pas d'apply.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {SID} {len(merged['chunks'])} chunks")


if __name__ == "__main__":
    build()
